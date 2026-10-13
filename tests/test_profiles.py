"""The coverage plan must expose rich, internally consistent volunteer profiles so
the UI can show context (history, reliability, cancellations) on demand."""
from shiftrescue.domain import coverage_plan, load_scenario


def test_every_volunteer_has_a_profile():
    plan = coverage_plan(load_scenario())
    ids = {v['id'] for v in load_scenario()['volunteers']}
    assert set(plan['profiles']) == ids
    for p in plan['profiles'].values():
        assert 'name' in p and 'shifts_completed' in p and 'history' in p


def test_profile_stats_are_internally_consistent():
    for p in coverage_plan(load_scenario())['profiles'].values():
        assert p['total_assignments'] == p['shifts_completed'] + p['shifts_cancelled'] + p['no_shows']
        if p['total_assignments']:
            assert p['reliability_pct'] == round(100 * p['shifts_completed'] / p['total_assignments'])
        else:
            assert p['reliability_pct'] is None


def test_cancelled_volunteer_profile_is_inspectable():
    scenario = load_scenario()
    plan = coverage_plan(scenario)
    cid = scenario['shift']['cancelled_volunteer_id']
    alex = plan['profiles'][cid]
    assert alex['is_cancelled'] is True
    # The canceller is excluded from outreach but still has a viewable record.
    assert cid not in {v['id'] for v in plan['eligible']}
    assert alex['shifts_cancelled'] >= 1
    assert any(h['outcome'] == 'cancelled' for h in alex['history'])


def test_history_outcomes_are_known_kinds():
    allowed = {'completed', 'cancelled', 'no_show'}
    for p in coverage_plan(load_scenario())['profiles'].values():
        for h in p['history']:
            assert h['outcome'] in allowed
            assert h['date'] and h['role']


def test_hours_pattern_fields_present_and_consistent():
    for p in coverage_plan(load_scenario())['profiles'].values():
        assert 'hours_logged' in p and 'hours_target' in p and 'needs_hours' in p
        assert p['pickup_likelihood'] in {'high', 'medium', 'low', 'unknown'}
        if p['hours_target'] is None:
            assert p['hours_remaining'] is None and p['needs_hours'] is False
        else:
            assert p['hours_remaining'] == max(0, p['hours_target'] - p['hours_logged'])
            assert p['needs_hours'] == (p['hours_remaining'] > 0)


def test_no_history_means_unknown_pickup_likelihood():
    profiles = coverage_plan(load_scenario())['profiles']
    for p in profiles.values():
        if p['total_assignments'] == 0:
            assert p['pickup_likelihood'] == 'unknown'
