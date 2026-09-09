# Scope locked — September 8, 2026

## Audience and outcome
One small food pantry with recurring shifts, a roster of approved backups, and
manual coordinator outreach. Reduce coordination effort and uncovered shifts.
This does not solve a shortage of willing volunteers. No customer validation or
measured savings are claimed; outreach has been sent by the project owner.

## MVP acceptance criteria
1. Coordinator records a cancellation and reviews eligible backup candidates.
2. Coordinator authorizes outreach to an approved backup pool.
3. Agent prepares requests; email adapter sends only within authorized scope.
4. Declines and timed-out offers advance to another eligible person.
5. Explicit, authenticated acceptance fills the gap exactly once.
6. Roster and activity log persist across restarts.
7. Exhausted candidates produce an actionable escalation.

## Decisions
Python + Strands + Amazon Bedrock. One agent with narrowly scoped tools.
One organization, one uncovered position, full-shift coverage, email only.
Deterministic eligibility rules and transactional booking; model explains and
coordinates but cannot waive rules or invent acceptance. Start with a synthetic
outbox and test replies before connecting a real delivery provider.
Next: SQLite persistence and a small API; coordinator interface on September 11.

## Not in the initial version
SMS, multi-organization accounts, automatic inbox cancellation detection, partial
shift negotiation, calendar integration, predictive no-show scoring, and payments.

## Schedule
- Sep 8: local repo, scaffold, roster, demo specification; owner confirms accounts.
- Sep 9: complete cancellation/request/acceptance flow with test inboxes.
- Sep 10: declines, offer expiry, duplicate acceptance, no-backup escalation.
- Sep 11: coordinator interface and synthetic public demo deployment.
- Sep 12: verification, setup documentation, diagram, description, video script.
- Sep 13: video and submission; optional AWS build post if ready.
- Sep 14: buffer and final submission verification.

## Validation gate — Sep 10
Use coordinator responses to adjust terminology and operating rules. If no response,
retain the documented synthetic scenario and clearly disclose lack of a pilot.
Measure coordinator minutes, time to confirmed coverage, fill rate, and erroneous
or unnecessary outreach only when there is real evidence to measure.
