from copy import deepcopy
from shiftrescue.domain import coverage_plan, load_scenario


def test_only_available_qualified_opted_in_backups_are_recommended():
    result = coverage_plan(load_scenario())
    assert [v["id"] for v in result["eligible"]] == ["v2", "v3"]
    excluded = {v["id"]: v["reasons"] for v in result["excluded"]}
    assert "Cancelled this shift" in excluded["v1"]
    assert "Missing required role" in excluded["v4"]
    assert "Unavailable for the full shift" in excluded["v5"]
    assert "Not opted in to backup requests" in excluded["v6"]
    assert "Overlapping commitment" in excluded["v7"]


def test_no_backups_escalates_instead_of_claiming_coverage():
    scenario = deepcopy(load_scenario())
    for volunteer in scenario["volunteers"]:
        volunteer["backup_opt_in"] = False
    result = coverage_plan(scenario)
    assert result["eligible"] == []
    assert result["status"] == "needs_coordinator"
    assert result["outreach_sent"] is False


def test_adjacent_commitment_does_not_conflict():
    scenario = load_scenario()
    scenario["volunteers"][1]["commitments"] = [
        {"start": "2026-09-12T08:00:00-04:00", "end": "2026-09-12T09:00:00-04:00"}]
    assert "v2" in [v["id"] for v in coverage_plan(scenario)["eligible"]]
