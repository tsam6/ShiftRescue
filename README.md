# ShiftRescue

Volunteer shift coverage assistant built with the Strands Agents SDK.
**Local prototype; synthetic data only. No external messages are sent.**

## What it is for
A small food pantry has a willing backup volunteer pool, but its coordinator
manually checks eligibility, contacts people, follows up, and updates the roster.
ShiftRescue aims to take that coordination work off their plate.

## Current implementation
- Seven fictional volunteers and one fictional pantry shift.
- Working deterministic checks for role, full-shift availability, backup opt-in,
  cancellation, and overlapping commitments.
- Outreach order prioritizes people who received fewer recent backup requests.
- Offline CLI to inspect the proposed plan without an AWS account.
- Real Strands agent constructor and read-only tool for explaining that plan using Bedrock.
- Focused tests for eligibility, conflicts, and no-backup escalation.

Local simulated offers, explicit scripted replies, expiry, and transactional SQLite
bookings are implemented. Real email delivery, authenticated reply endpoints,
coordinator UI, and deployment are **not implemented yet**. The offline demo is not evidence of an autonomous agent run.

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
The Strands entry point still only explains the read-only eligibility plan; wiring
the agent to the new workflow tools is a subsequent milestone.
