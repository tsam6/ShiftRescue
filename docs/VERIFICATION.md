# Current status — September 14, 2026

Real Bedrock covered-workflow execution succeeded; 15 tests pass; the public GitHub
repository and MIT license are verified. Browser replay, simulated replies and
persistence are implemented. Live delivery, background scheduling and browser-agent
integration remain future work. The dated entries below are historical checkpoints.

# Day-one verification — September 8, 2026

Environment: Python 3.14, macOS; Strands Agents 1.55.0.

Passed:
- Editable package installation, including console entry point.
- Three pytest cases: eligible backup filtering, empty-pool escalation, adjacent commitment boundary.
- Offline demo: Blair then Casey eligible; five other fixture volunteers excluded with reasons.
- pip dependency consistency check: no broken requirements.
- Strands Agent construction with mocked AWS session (no network or inference).
- Decorated coverage tool call returns the read-only plan.

Not verified yet:
- Live Bedrock credentials, model access, or model tool use.
- Email sending, responses, persistence, coordinator UI, or deployment (not implemented).
- Public GitHub repository and AWS Builder ID ownership.

requirements.lock captures installed dependency versions, excluding the editable local
project and installer tooling. No measured customer benefit is claimed.

## Local workflow verification — September 8, 2026

Eight tests pass, including the three original eligibility tests and five workflow
tests covering approval gating, decline-to-acceptance, restart persistence, timeout
and stale acceptance, simultaneous duplicate acceptance, clock/shift-start checks,
invalid tokens, and repeated approval.
Both CLI replays passed: covered by Casey after Blair declines; escalated after
Casey's offer expires. No AWS model, external email, or hosted service was used.
Real email, live replies, UI, and deployment remain pending; local persistence and
scripted replies are now implemented, superseding the day-one status above.

## Strands workflow integration — September 9, 2026

11 tests pass. The new integration test executes the actual Strands event loop
with an explicitly scripted local model: inspect tool, advance tool, final response.
It verifies a persistent offer is created. Additional checks ensure approval gating,
no token exposure to the model, and the model-call guard. This proves SDK/tool wiring,
not real-model reasoning or Bedrock access. No paid calls were made.

Live runner supports covered and unfilled branches, asserts persisted outcomes, and
saves model explanations. AWS credentials are absent locally; credit and Bedrock
verification require the owner's sign-in. GitHub publication also awaits sign-in.

September 9 AWS connectivity check: CLI STS succeeded; Python authentication
succeeded after installing AWS CRT. First inference request was blocked by AWS
account verification, before any model response. Full live demo remains unverified.

## Coordinator review and follow-ups — September 13, 2026

15 tests pass. Added coverage for unreviewed-candidate exclusion and approval rollback,
restriction to the selected backup pool, one reminder per offer with none after
acceptance, and dashboard actions with non-destructive new-demo creation.

Browser verification passed on the local dashboard: approve Blair/Casey, advance
10 minutes, observe one reminder, decline as Blair, accept as Casey, and observe
confirmed coverage with no pending follow-ups. Desktop layout was visually checked.
This supersedes the earlier UI-pending status. No model or external email was used.
Qualification review is a fixture field; service-hour grouping and retention
follow-ups are not implemented.

## Real Bedrock verification — September 14, 2026

After refreshing expired AWS credentials, the bounded live-demo runner succeeded
using us.amazon.nova-lite-v1:0 in us-east-1. The real Strands agent called workflow
tools to create Blair’s offer, advance to Casey after a scripted decline, and
report the persisted booking after a scripted acceptance. The runner verified
status covered. Published evidence removes local offer tokens and model thinking
blocks; raw local artifacts remain in the ignored runtime directory.
The browser UI remains an offline replay; no real emails were sent.

## Final submission review — September 14, 2026

- Fresh test run: 15 passed; no submission-blocking workflow defect identified.
- Isolated wheel build succeeded. Both the JSON fixture and browser HTML are bundled.
- Unpacked wheel ran its offline CLI successfully from outside the repository.
- Relative Markdown file links checked: none missing.
- Polished video decoded successfully: 1:47, 1920×1080, 24 fps; quiet stereo music.
- Public Devpost text correctly distinguishes the browser replay and Bedrock runner.
- Owner is replacing the public video; latest hosted video URL is not yet verified.
