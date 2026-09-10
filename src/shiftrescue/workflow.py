"""Local simulation with transactional persistence. Never sends email or calls AI."""
from contextlib import contextmanager
from datetime import timedelta
import json
import secrets
import sqlite3
from .domain import coverage_plan, instant


class Workflow:
    def __init__(self, path):
        self.path = str(path)
        with sqlite3.connect(self.path) as db:
            db.execute('CREATE TABLE IF NOT EXISTS workflow (id INTEGER PRIMARY KEY CHECK(id=1), state TEXT NOT NULL)')

    @contextmanager
    def transaction(self):
        with sqlite3.connect(self.path, timeout=10) as db:
            db.execute('BEGIN IMMEDIATE')
            row = db.execute('SELECT state FROM workflow WHERE id=1').fetchone()
            state = json.loads(row[0]) if row else None
            yield db, state

    def save(self, db, state):
        db.execute('INSERT OR REPLACE INTO workflow VALUES (1, ?)', (json.dumps(state),))

    def start(self, scenario, now):
        instant(now)
        if not scenario.get('synthetic'):
            raise ValueError('This prototype only accepts synthetic scenarios')
        with self.transaction() as (db, state):
            if state is not None:
                raise ValueError('Database already contains a scenario; use a new database')
            state = dict(scenario=scenario, status='awaiting_review', approved=False,
                         offers=[], outbox=[], events=[], booking=None, last_time=now)
            self.event(state, now, 'cancellation_recorded', scenario['shift']['cancelled_volunteer_id'])
            self.save(db, state)
        return self.snapshot()

    def snapshot(self):
        with self.transaction() as (_, state):
            if state is None:
                raise ValueError('No scenario loaded')
            return state

    @staticmethod
    def event(state, now, kind, detail):
        state['events'].append(dict(time=now, kind=kind, detail=detail))

    @staticmethod
    def check_time(state, now):
        if state is None:
            raise ValueError('No scenario loaded')
        if instant(now) < instant(state['last_time']):
            raise ValueError('Simulation clock cannot move backwards')
        state['last_time'] = now

    def advance(self, state, now):
        if state['booking'] or not state['approved']:
            return
        for offer in state['offers']:
            if offer['status'] == 'pending':
                if instant(now) < instant(offer['expires']):
                    return
                offer['status'] = 'expired'
                self.event(state, now, 'offer_expired', offer['volunteer_id'])
        attempted = {o['volunteer_id'] for o in state['offers']}
        candidates = [v for v in coverage_plan(state['scenario'])['eligible'] if v['id'] not in attempted]
        shift = state['scenario']['shift']
        if not candidates or instant(now) >= instant(shift['start']):
            if state['status'] != 'needs_coordinator':
                state['status'] = 'needs_coordinator'
                self.event(state, now, 'escalated', 'Shift started' if instant(now) >= instant(shift['start']) else 'No eligible untried backups')
            return
        volunteer = candidates[0]
        expires = min(instant(now) + timedelta(minutes=15), instant(shift['start'])).isoformat()
        offer = dict(token=secrets.token_urlsafe(24), volunteer_id=volunteer['id'], status='pending', expires=expires)
        state['offers'].append(offer)
        state['outbox'].append(dict(kind='coverage_request', volunteer_id=volunteer['id'],
                                    simulated=True, delivered=False, body=f"Can you cover {shift['role']} from {shift['start']} to {shift['end']}?", expires=expires))
        state['status'] = 'seeking_coverage'
        self.event(state, now, 'request_simulated', volunteer['id'])

    def approve(self, now, dispatch=True):
        with self.transaction() as (db, state):
            self.check_time(state, now)
            if not state['approved']:
                state['approved'] = True
                self.event(state, now, 'coordinator_approved', 'Synthetic backup outreach')
            if dispatch:
                self.advance(state, now)
            self.save(db, state)
        return self.snapshot()

    def tick(self, now):
        with self.transaction() as (db, state):
            self.check_time(state, now)
            self.advance(state, now)
            self.save(db, state)
        return self.snapshot()

    def reply(self, token, decision, now, dispatch=True):
        if decision not in ('accept', 'decline'):
            raise ValueError('Reply must be accept or decline')
        with self.transaction() as (db, state):
            self.check_time(state, now)
            self.advance(state, now)
            offer = next((o for o in state['offers'] if secrets.compare_digest(o['token'], token)), None)
            if offer is None or offer['status'] != 'pending' or state['booking']:
                self.event(state, now, 'reply_ignored', 'Invalid, expired, or already resolved offer')
            elif decision == 'decline':
                offer['status'] = 'declined'
                self.event(state, now, 'declined', offer['volunteer_id'])
                if dispatch:
                    self.advance(state, now)
            else:
                eligible = {v['id'] for v in coverage_plan(state['scenario'])['eligible']}
                if offer['volunteer_id'] not in eligible:
                    offer['status'] = 'ineligible'
                    self.event(state, now, 'acceptance_rejected', offer['volunteer_id'])
                    self.advance(state, now)
                else:
                    offer['status'] = 'accepted'
                    state['booking'] = dict(shift_id=state['scenario']['shift']['id'], volunteer_id=offer['volunteer_id'])
                    state['status'] = 'covered'
                    state['outbox'].append(dict(kind='confirmation', volunteer_id=offer['volunteer_id'], simulated=True, delivered=False))
                    self.event(state, now, 'coverage_confirmed', offer['volunteer_id'])
            self.save(db, state)
        return self.snapshot()
