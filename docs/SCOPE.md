# Scope — September 14, 2026

## Audience and problem
A food pantry coordinator with a roster of approved backup volunteers must check
eligibility, contact people, follow up, and update coverage after a cancellation.
Coordinator conversations support this problem; no pilot or measured savings are claimed.
The project does not solve a shortage of willing volunteers.

## Implemented prototype
- One fictional organization, one canceled position, and eight fictional volunteers.
- Qualification review, role, availability, opt-in, cancellation and conflict checks.
- Coordinator selection and approval of an eligible outreach pool.
- Sequential simulated offers, one follow-up per offer, expiry and fallback.
- Explicit simulated acceptance with transactional booking and persistent audit.
- Escalation when approved candidates are exhausted.
- Offline browser interface and separate Strands/Bedrock runner.
- Successful real Bedrock covered-workflow verification on September 14.

The cancellation is preloaded in the fixture. The browser is a replay rather than
a live cancellation intake. Reminders and expiry require workflow advancement.

## Next implementation steps
Connect the real agent to the browser, add a background worker, authenticated
volunteer reply channels, and an authorized email adapter. Explore integrations
with existing volunteer platforms only with organizational approval.

## Outside current scope
Public deployment, CRM migration, live email/SMS, multi-organization accounts,
service-hour categories, post-shift retention automation, mapping, automatic inbox
cancellation detection, partial-shift negotiation, and predictive no-show scoring.

## Evaluation plan
With a willing organization, measure coordinator time, time to confirmed coverage,
fill rate, and unnecessary outreach. Treat improved retention and reduced staffing
shortages as hypotheses until demonstrated.
