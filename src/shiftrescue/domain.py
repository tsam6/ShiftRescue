"""Deterministic eligibility rules; the model cannot relax these constraints."""
from datetime import datetime
from importlib.resources import files
import json


def load_scenario():
    return json.loads(files("shiftrescue").joinpath("data/scenario.json").read_text())


def instant(value):
    parsed = datetime.fromisoformat(value)
    if parsed.tzinfo is None:
        raise ValueError("Timestamps must include a UTC offset")
    return parsed


def rejection_reasons(volunteer, shift):
    start, end = instant(shift["start"]), instant(shift["end"])
    if end <= start:
        raise ValueError("Shift must end after it starts")
    reasons = []
    if volunteer["id"] == shift["cancelled_volunteer_id"]:
        reasons.append("Cancelled this shift")
    if not volunteer["backup_opt_in"]:
        reasons.append("Not opted in to backup requests")
    if shift["role"] not in volunteer["roles"]:
        reasons.append("Missing required role")
    if not any(instant(w["start"]) <= start and instant(w["end"]) >= end
               for w in volunteer["availability"]):
        reasons.append("Unavailable for the full shift")
    if any(instant(w["start"]) < end and instant(w["end"]) > start
           for w in volunteer["commitments"]):
        reasons.append("Overlapping commitment")
    return reasons


def coverage_plan(scenario):
    eligible, excluded = [], []
    for volunteer in scenario["volunteers"]:
        reasons = rejection_reasons(volunteer, scenario["shift"])
        if reasons:
            excluded.append({"id": volunteer["id"], "name": volunteer["name"], "reasons": reasons})
        else:
            eligible.append({"id": volunteer["id"], "name": volunteer["name"],
                             "recent_backup_requests": volunteer["recent_backup_requests"]})
    eligible.sort(key=lambda v: (v["recent_backup_requests"], v["id"]))
    return {"synthetic": True, "shift": scenario["shift"], "eligible": eligible,
            "excluded": excluded, "status": "awaiting_coordinator_review" if eligible else "needs_coordinator",
            "outreach_sent": False}
