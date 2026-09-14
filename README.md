# ShiftRescue

Volunteer shift coverage assistant built with the Strands Agents SDK.
**Local prototype; synthetic data only. No external messages are sent.**

## What it is for
A small food pantry has a willing backup volunteer pool, but its coordinator
manually checks eligibility, contacts people, follows up, and updates the roster.
ShiftRescue aims to take that coordination work off their plate.

## Current implementation
- Eight fictional volunteers and one fictional pantry shift.
- Working deterministic checks for coordinator qualification review, role, full-shift availability, backup opt-in,
  cancellation, and overlapping commitments.
- Outreach order prioritizes people who received fewer recent backup requests.
- Local coordinator dashboard with candidate reasons, selected-pool approval, simulated replies,
  and a follow-up desk with one reminder per offer.
- Offline CLI to inspect the proposed plan without an AWS account.
- Strands workflow tools for inspecting persisted state and advancing approved coverage requests.
- A bounded live-demo runner that uses Bedrock with scripted volunteer replies.
- Focused tests for eligibility, conflicts, and no-backup escalation.

Local simulated offers, explicit scripted replies, expiry, and transactional SQLite
bookings are implemented. Real email delivery, authenticated reply endpoints,
and deployment are **not implemented yet**. The coordinator UI is local and uses a replay clock. The offline demo is not evidence of an autonomous agent run.

## Setup
Python 3.10+:

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.lock
python -m pip install --no-deps -e .
shiftrescue demo
python -m pytest
```

The lock file records the packages tested in the development environment; use
`python -m pip install -e '.[dev]'` to resolve dependencies for a different supported Python version.
Sample data is bundled with the package, so the CLI works outside the repo directory.

## Run the Strands agent
Use your existing AWS credential profile with Bedrock invocation permissions.
An AWS Builder ID alone does not supply Bedrock credentials.

```sh
export AWS_PROFILE=your-configured-profile
export AWS_DEFAULT_REGION=us-east-1
export BEDROCK_MODEL_ID=your-accessible-model-or-inference-profile-id
shiftrescue agent
```

Model invocation may incur AWS charges. `.env.example` documents settings but is not
automatically loaded. Do not commit credentials, real volunteer rosters, or inbox data.

## Project guide
- [Scope and milestones](docs/SCOPE.md)
- [Demo scenario](docs/DEMO.md)
- [Architecture](docs/ARCHITECTURE.md)
- [Account and publication checklist](docs/ACCOUNTS.md)
- [Verification record](docs/VERIFICATION.md)

## License
MIT — see [LICENSE](LICENSE). When published, set the repository About description to
“Volunteer shift coverage assistant built with Strands Agents SDK · MIT licensed”.

## References
- https://strandsagents.com/docs/user-guide/quickstart/python/
- https://docs.aws.amazon.com/signin/latest/userguide/create-builder-id.html
- https://docs.aws.amazon.com/signin/latest/userguide/differences-builder-id.html

## Replay the local coverage workflow (no AWS charges)

```sh
shiftrescue simulate --database runtime/covered.sqlite3
shiftrescue simulate --outcome unfilled --database runtime/unfilled.sqlite3
```

Use a new database filename for each replay; existing runs are never overwritten.
The first replay records a cancellation, approves simulated outreach, records Blair's
decline and Casey's acceptance, and persists the booking. The second lets Casey's
offer expire and escalates. Timestamps and replies are scripted, not live events.
No model is invoked. Simulated outbox entries have `delivered=false`.

The local store handles one scenario per database. It serializes updates with SQLite
transactions; duplicate and stale acceptances cannot create another booking.
Offer expiry is processed when the workflow is advanced, not by a background worker.
Tokens are local test capabilities, not a complete authentication implementation.
The `agent` command explains the read-only plan. The `live-demo` command connects
Strands to the persistent workflow, with explicit scripted replies outside the model.

## Run the integrated Bedrock demo

First confirm AWS credits are applied and cover Bedrock, then configure a credential
profile, region, and an accessible model ID as above. Do not run this command until
credit coverage is verified or you have approved paying for inference.

```sh
shiftrescue live-demo --database runtime/live-covered.sqlite3
# Optional second run, after inspecting the first run and usage:
shiftrescue live-demo --outcome unfilled --database runtime/live-unfilled.sqlite3
```

Each run uses a new database. The application records coordinator approval, then
the agent reads state and advances outreach via tools. Scripted volunteers provide
explicit decline/acceptance events outside the agent. The model cannot approve
outreach, fabricate a response, change the clock, access offer tokens, or bypass
eligibility. The tool effects are real local SQLite writes; messages are simulated.

The runner verifies each expected offer and final state, saving model explanations
beside the database as `.transcript.json`. A limit of 12 model calls per agent and
600 output tokens per model response bounds the run; SDK model-loop retries and
Bedrock client retries are disabled. This is not a dollar-denominated billing cap.
A real Amazon Bedrock run succeeded on September 14, 2026 using Amazon Nova Lite
through Strands. It created two offers and verified Casey’s accepted booking.
See [run evidence](submission/evidence/bedrock-transcript.json). Volunteer replies
and email delivery remain simulated. The browser screen is a separate offline replay.

## Open the coordinator dashboard

```sh
shiftrescue serve --database runtime/coordinator.sqlite3 --port 8765
```

Open http://127.0.0.1:8765. This loopback-only screen makes no AWS calls and sends
no emails. Approve the selected backups, advance 10 minutes to see a reminder,
decline as Blair, then accept as Casey. Coverage and the activity trail persist.
Use **New demo** for another run; it preserves the previous database and creates a
new file. Restarting the server opens the database named on the command line.

Unreviewed candidates are excluded even when nearby. Qualifications are fixture
inputs, not AI assessments; the UI approves outreach, not qualification status.
Distance and prior experience are shown as context. Service-hour categories,
post-shift retention follow-ups, CRM integration, and live scheduling are not implemented.
