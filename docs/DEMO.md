# Demo guide

All organizations, volunteers, email addresses, and reply events are fictional.
Harbor Community Pantry has one canceled pantry-distribution position on September
12, 2026, 09:00–12:00 America/New_York. Fixed dates are a replay, not a live shift.

## Browser walkthrough — no model calls
1. Run `shiftrescue serve --database runtime/coordinator.sqlite3`.
2. Open http://127.0.0.1:8765 and review Blair and Casey.
3. Expand exclusions: Alex canceled; Drew lacks the role; Eden cannot cover the
   full shift; Finley has not opted in; Gray has a conflict; Harper awaits review.
4. Approve selected backups. The workflow prepares Blair's simulated invitation.
5. Click **+10 minutes** to record one follow-up.
6. Decline as Blair. The workflow prepares Casey's invitation.
7. Accept as Casey. The booking is persisted and follow-ups stop.

The screen runs deterministic workflow code. It is not connected to the Strands agent.

## Separate real Bedrock demonstration
Configure AWS as described in the README, then run:

```sh
shiftrescue live-demo --database runtime/live-covered.sqlite3
```

The application records scripted approval and replies; the real agent inspects state
and advances offers through tools. It created Blair's offer, advanced to Casey after
a decline, and reported Casey's actual persisted booking in the verified September 14
run. See `submission/evidence` for sanitized model responses and final state.

## Failure and duplicate-response checks
`shiftrescue simulate --outcome unfilled --database runtime/unfilled.sqlite3`
demonstrates timeout and escalation without a model. The live runner also supports
`--outcome unfilled`, but that branch has not been verified with Bedrock.
Automated tests cover stale and duplicate acceptances, preventing a second booking.

## Video files
- `submission/ShiftRescue-polished-music.mp4`: 1:47 captured-interface walkthrough
  with captions, original instrumental background music, and no narration.
- `submission/ShiftRescue-polished-silent.mp4`: same timing, no audio.
- `submission/VOICEOVER-GUIDE.md`: optional narration prompts.

These use actual interface captures, not continuous cursor footage. The closing
agent-evidence section describes the separate verified run. Earlier draft videos
remain in the repository but are superseded by these versions.
