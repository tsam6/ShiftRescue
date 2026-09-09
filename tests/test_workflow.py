from concurrent.futures import ThreadPoolExecutor
import pytest
from shiftrescue.domain import load_scenario
from shiftrescue.workflow import Workflow

T='2026-09-11T18:00:00-04:00'

@pytest.fixture
def flow(tmp_path):
    f=Workflow(tmp_path/'state.sqlite3')
    f.start(load_scenario(), T)
    return f


def test_approval_decline_accept_and_restart(flow):
    assert flow.tick(T)['outbox'] == []
    first=flow.approve(T)['offers'][0]
    assert first['volunteer_id']=='v2'
    state=flow.reply(first['token'],'decline',T)
    second=state['offers'][-1]
    assert second['volunteer_id']=='v3'
    flow.reply(second['token'],'accept',T)
    state=Workflow(flow.path).snapshot()
    assert state['booking']['volunteer_id']=='v3'
    assert all(m['simulated'] and not m['delivered'] for m in state['outbox'])


def test_expiry_stale_acceptance_and_exhaustion(flow):
    token=flow.approve(T)['offers'][0]['token']
    state=flow.reply(token,'accept','2026-09-11T18:15:00-04:00')
    assert state['booking'] is None
    assert state['offers'][0]['status']=='expired'
    assert state['offers'][1]['volunteer_id']=='v3'
    state=flow.tick('2026-09-11T18:30:00-04:00')
    assert state['status']=='needs_coordinator'
    assert len(state['outbox'])==2


def test_concurrent_duplicate_acceptance_only_books_once(flow):
    token=flow.approve(T)['offers'][0]['token']
    with ThreadPoolExecutor(max_workers=2) as pool:
        list(pool.map(lambda _: Workflow(flow.path).reply(token,'accept',T), range(2)))
    state=flow.snapshot()
    assert sum(m['kind']=='confirmation' for m in state['outbox'])==1
    assert state['booking']['volunteer_id']=='v2'


def test_shift_start_and_clock_guard(flow):
    assert flow.approve('2026-09-12T09:00:00-04:00')['status']=='needs_coordinator'
    with pytest.raises(ValueError, match='backwards'):
        flow.tick(T)


def test_invalid_token_and_repeated_approval(flow):
    flow.approve(T)
    flow.approve(T)
    state=flow.reply('wrong-token','accept',T)
    assert state['booking'] is None
    assert len(state['outbox'])==1
