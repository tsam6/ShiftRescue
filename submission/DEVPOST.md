# ShiftRescue

Elevator pitch: ShiftRescue helps food pantries fill last-minute volunteer gaps by finding qualified backups, following up, and confirming coverage.

Track: Good Neighbor Agents

Repository: https://github.com/tsam6/ShiftRescue

## Inspiration
We contacted food assistance organizations to understand volunteer coordination. One coordinator described daily emails to fill open shifts, with after-hours cancellations leaving the team in a bind. Another described difficulty finding qualified volunteers and remembering follow-ups during busy periods. ShiftRescue grew from those conversations.

## What it does
ShiftRescue handles the workflow between a canceled shift and a confirmed replacement. It checks qualification-review status, role, availability, existing commitments, and backup opt-in. After coordinator approval, it progresses through eligible backups, follows up, handles declines and expired offers, and records a booking only after explicit acceptance. If no candidates remain, it escalates to the coordinator.

Our prototype uses fictional volunteers, simulated messages, and scripted reply events. A browser dashboard demonstrates review, approval, reminders, and acceptance. A separate live agent runner uses real Amazon Bedrock calls to operate the persistent workflow.

## How we built it
We used Python, the Strands Agents SDK, Amazon Bedrock with Amazon Nova Lite, SQLite, and a lightweight browser interface. The agent inspects coverage and advances approved outreach through tools. Application code enforces eligibility, approval, expiry, and booking uniqueness. The agent cannot invent volunteer responses, override qualification requirements, or directly create bookings.

A real Bedrock run successfully created Blair’s offer, advanced to Casey after a scripted decline, and verified Casey’s booking after an explicit scripted acceptance. The repository includes sanitized run evidence and reproducible setup instructions.

## Challenges we ran into
Organizations described different problems, including retention, location matching, qualification review, and cancellations. We kept the build focused on coverage while adding review safeguards. We also handled stale replies, duplicate acceptances, and repeated reminders. AWS account verification initially blocked inference; after refreshing credentials, the live Bedrock workflow succeeded.

## Accomplishments that we're proud of
We translated coordinator conversations into a working local workflow, verified a real Strands/Bedrock run, and passed 15 automated tests. The browser walkthrough confirms that approval leads to outreach, a reminder, a decline, and an accepted replacement. State persists in SQLite, and unreviewed candidates remain excluded even if nearby.

## What we learned
Posting a shift does not eliminate the coordination required to fill it. Interest, qualification, availability, and acceptance are distinct facts. Useful automation must respect those distinctions and show coordinators what happened. Our interviews support the problem; they are not a completed pilot or evidence of measured time savings.

## What's next for ShiftRescue
Connect the live agent to the browser interface, add background scheduling and authenticated reply channels, and explore authorized integrations with existing volunteer platforms. Then test with a willing organization and measure coordination time and coverage outcomes. Real email delivery, CRM integration, public hosting, and retention follow-ups are not implemented in this prototype.

## Built with
Python, Strands Agents SDK, Amazon Bedrock, Amazon Nova Lite, SQLite, HTML, CSS, JavaScript.

## Submission checklist
- Public repository above, including README and MIT license.
- Attach architecture.png.
- Upload ShiftRescue-polished-music.mp4 (or the silent version with your narration) to a supported public or unlisted video host and paste the video URL.
- Supply your AWS Builder ID (not an AWS account number).
- Do not use the localhost URL as a public live demo link.
- Confirm the updated video URL and final submission status in Devpost.
