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
