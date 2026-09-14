import pytest
from shiftrescue.server import Demo
from shiftrescue.domain import coverage_plan, load_scenario
from shiftrescue.workflow import Workflow
T='2026-09-11T18:00:00-04:00'


def test_unreviewed_nearby_volunteer_cannot_receive_offer(tmp_path):
    f=Workflow(tmp_path/'review.sqlite3'); f.start(load_scenario(),T)
    p=coverage_plan(load_scenario())
    assert 'Coordinator qualification review required' in next(v['reasons'] for v in p['excluded'] if v['id']=='v8')
    with pytest.raises(ValueError): f.approve(T,candidate_ids=['v8'])
    assert f.snapshot()['approved'] is False
    assert f.snapshot()['outbox']==[]


def test_selection_limits_outreach_and_acceptance(tmp_path):
    f=Workflow(tmp_path/'pool.sqlite3'); f.start(load_scenario(),T)
    s=f.approve(T,candidate_ids=['v3'])
    assert s['offers'][0]['volunteer_id']=='v3'
    s=f.reply(s['offers'][0]['token'],'decline',T)
    assert s['status']=='needs_coordinator'
    assert len(s['offers'])==1


def test_reminder_once_and_no_reminder_after_confirmation(tmp_path):
    f=Workflow(tmp_path/'reminder.sqlite3'); f.start(load_scenario(),T); f.approve(T)
    assert len(f.tick('2026-09-11T18:09:00-04:00')['outbox'])==1
    s=f.tick('2026-09-11T18:10:00-04:00')
    assert s['offers'][0]['followed_up']
    f.tick('2026-09-11T18:10:00-04:00')
    assert len(f.snapshot()['outbox'])==2
    f.reply(s['offers'][0]['token'],'accept','2026-09-11T18:11:00-04:00')
    assert len(f.tick('2026-09-11T18:30:00-04:00')['outbox'])==3


def test_demo_actions_and_new_run_preserve_original(tmp_path):
    app=Demo(tmp_path/'demo.sqlite3')
    app.action('approve',{'candidates':['v2','v3']})
    app.action('time',{'minutes':10})
    token=app.view()['state']['offers'][0]['token']
    app.action('reply',{'token':token,'decision':'decline'})
    assert app.view()['state']['offers'][-1]['volunteer_id']=='v3'
    app.action('new',{})
    assert app.view()['state']['approved'] is False
    assert Workflow(tmp_path/'demo.sqlite3').snapshot()['approved'] is True
