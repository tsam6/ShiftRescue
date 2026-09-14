# Demo scenario

All organizations, people, emails, and events below are fictional. All email
addresses use example.org; no real volunteer data is required.

## Setup
Harbor Community Pantry (fictional), September 12, 2026, 09:00–12:00 America/New_York.
Role: pantry_distribution. Alex cancels one position the evening before.
This is a replay fixture with fixed dates, not a live shift.

## Today's runnable checkpoint
`shiftrescue demo` identifies Blair and Casey as eligible, in that order. Drew has
the wrong role, Eden cannot cover the full shift, Finley has not opted into backup
requests, Gray has a conflicting commitment, Alex canceled, and Harper awaits qualification review. Nothing is sent.
`shiftrescue agent` adds a real model explanation when Bedrock is configured.

## Target end-to-end demo (local scripted replay implemented; local UI implemented; live delivery pending)
1. Coordinator records Alex's cancellation; review panel shows one open position.
2. Coordinator approves contacting eligible backups.
3. Agent requests Blair's help; a test volunteer explicitly declines.
4. Agent requests Casey's help; Casey accepts through the simulated volunteer inbox. Production reply authentication remains pending.
5. Transaction fills exactly one position and records confirmations in the outbox.
6. UI shows who filled the gap and the sequence of actions.

## Failure branch
Both backups decline or their offers expire. Agent does not mark coverage complete;
it escalates with the shift, candidates tried, and reason the gap remains.

## Additional acceptance check
A stale or duplicate acceptance cannot replace the confirmed volunteer or add a
second booking. Test with structured reply events, not model-generated consent.

## Evidence for the video
Show actual tool execution, persisted roster change, and messages in test inboxes.
Label simulated timeouts and synthetic volunteers. Do not present offline fixture
output as an autonomous production run or claim unmeasured hours saved.

## Coordinator screen walkthrough — September 13
1. Run `shiftrescue serve --database runtime/coordinator.sqlite3`.
2. Review Blair and Casey; expand exclusions to see Harper needs qualification review.
3. Approve selected backups. Blair receives a simulated invitation.
4. Click **+10 minutes**. One reminder appears in the message log.
5. Click **Decline**. Casey becomes the active invitee.
6. Click **Accept shift**. Casey is confirmed and no follow-ups remain.

This screen drives deterministic workflow code. It does not invoke the Strands
agent. Use the separate `live-demo` runner for actual model/tool execution.
