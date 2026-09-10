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
