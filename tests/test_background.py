"""Autonomous follow-up processing: eligible pending offers advance without the
coordinator pressing time buttons, and nothing happens after coverage is confirmed.
Deterministic and offline — no model calls or email delivery."""
from shiftrescue.domain import load_scenario
from shiftrescue.workflow import Workflow

T = '2026-09-11T18:00:00-04:00'


def _flow(tmp_path, name):
    f = Workflow(tmp_path / name)
    f.start(load_scenario(), T)
    return f


def test_next_due_is_none_before_approval(tmp_path):
    f = _flow(tmp_path, 'pre.sqlite3')
    assert Workflow.next_due(f.snapshot()) is None


def test_run_due_before_deadline_sends_one_reminder_only(tmp_path):
    f = _flow(tmp_path, 'reminder.sqlite3')
    f.approve(T)  # first offer -> v2, follow-up at +10m, expiry at +15m
    # Advance to just past the reminder time but before expiry.
    state = f.run_due('2026-09-11T18:11:00-04:00')
    assert state['offers'][0]['followed_up'] is True
    assert sum(m['kind'] == 'follow_up' for m in state['outbox']) == 1
    assert state['offers'][0]['status'] == 'pending'  # still waiting, not expired
    # Re-running at the same clock must not duplicate the reminder.
    state = f.run_due('2026-09-11T18:11:00-04:00')
    assert sum(m['kind'] == 'follow_up' for m in state['outbox']) == 1


def test_run_due_expires_and_rolls_to_next_candidate_then_escalates(tmp_path):
    f = _flow(tmp_path, 'escalate.sqlite3')
    f.approve(T)
    # Run far past both offers' deadlines in one autonomous sweep.
    state = f.run_due('2026-09-11T19:30:00-04:00')
    volunteers = [o['volunteer_id'] for o in state['offers']]
    assert volunteers == ['v2', 'v3']  # rolled to the next approved candidate
    assert all(o['status'] == 'expired' for o in state['offers'])
    assert state['status'] == 'needs_coordinator'
    assert state['booking'] is None


def test_run_due_takes_no_action_after_coverage_confirmed(tmp_path):
    f = _flow(tmp_path, 'covered.sqlite3')
    first = f.approve(T)['offers'][0]
    booked = f.reply(first['token'], 'accept', T)
    assert booked['status'] == 'covered'
    before = len(booked['outbox'])
    assert Workflow.next_due(booked) is None
    state = f.run_due('2026-09-11T20:00:00-04:00')
    assert state['status'] == 'covered'
    assert len(state['outbox']) == before  # nothing added after confirmation


def test_run_due_matches_manual_tick_outcome(tmp_path):
    # Autonomous sweep reaches the same escalation a coordinator would by clicking.
    auto = _flow(tmp_path, 'auto.sqlite3')
    auto.approve(T)
    auto_state = auto.run_due('2026-09-11T19:00:00-04:00')

    manual = _flow(tmp_path, 'manual.sqlite3')
    manual.approve(T)
    manual.tick('2026-09-11T18:15:00-04:00')  # first expiry -> rolls to v3
    manual_state = manual.tick('2026-09-11T18:30:00-04:00')  # second expiry

    assert auto_state['status'] == manual_state['status'] == 'needs_coordinator'
    assert [o['status'] for o in auto_state['offers']] == [o['status'] for o in manual_state['offers']]


def test_demo_auto_toggle_processes_without_time_buttons(tmp_path):
    from shiftrescue.server import Demo
    app = Demo(tmp_path / 'serve.sqlite3')
    app.action('approve', {'candidates': ['v2', 'v3']})
    assert app.view()['auto'] is False
    app.action('auto', {'enabled': True})
    assert app.view()['auto'] is True
    # Drive the accelerated background step directly, as the server thread would,
    # until it reports idle. No '+N minutes' button was ever pressed.
    for _ in range(500):
        if not app.tick_auto():
            break
    v = app.view()
    assert v['state']['status'] == 'needs_coordinator'
    assert v['auto_idle'] is True
    assert [o['status'] for o in v['state']['offers']] == ['expired', 'expired']


def test_demo_auto_stops_at_coverage(tmp_path):
    from shiftrescue.server import Demo
    app = Demo(tmp_path / 'serve2.sqlite3')
    app.action('approve', {'candidates': ['v2', 'v3']})
    app.action('auto', {'enabled': True})
    # Accept as the first volunteer, then confirm autonomous mode does nothing more.
    token = app.view()['state']['offers'][0]['token']
    app.action('reply', {'token': token, 'decision': 'accept'})
    v = app.view()
    assert v['state']['status'] == 'covered'
    assert v['auto_idle'] is True
    before = len(v['state']['outbox'])
    for _ in range(5):
        assert app.tick_auto() is False
    assert len(app.view()['state']['outbox']) == before


def test_demo_new_run_disables_auto(tmp_path):
    from shiftrescue.server import Demo
    app = Demo(tmp_path / 'serve3.sqlite3')
    app.action('auto', {'enabled': True})
    app.action('new', {})
    assert app.view()['auto'] is False

