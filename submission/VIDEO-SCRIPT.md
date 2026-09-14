# Demo narration

This video presents actual saved outputs from the verified Bedrock run in chapters.

## ShiftRescue
When a food pantry volunteer cancels, someone has to find a qualified replacement, send messages, and follow up. ShiftRescue is a volunteer coverage assistant built with the Strands Agents SDK. It helps food pantry coordinators manage that work.

## The problem came from coordinators
We contacted food assistance organizations before building. One coordinator described daily coverage emails and being unable to send them after hours. Another described difficulty finding qualified volunteers and remembering follow-ups. These conversations informed our prototype. We have not run a pilot or measured time savings.

## A real agent run
This demonstration presents the saved output and database evidence from a successful real Bedrock run on September fourteenth. The model calls and tool effects are real. The volunteers, dates, messages, and reply events are simulated. The browser dashboard is a separate offline replay.

## 1. Approved outreach → Blair
The application records coordinator approval. The agent inspects coverage and advances the workflow through its tools. Application rules exclude candidates who are unreviewed, unavailable, unqualified, or not opted in. The first simulated offer goes to Blair. This is the actual saved model response.

## 2. Decline → next eligible backup
The application records a scripted decline from Blair. The agent reads the changed state and advances coverage again. The workflow creates an offer for Casey. The agent does not manufacture a volunteer response or bypass the approved candidate pool.

## 3. Acceptance → verified booking
The application records Casey’s explicit scripted acceptance. The resulting database shows status covered, with volunteer v three, Casey, booked for shift zero zero one. Blair’s offer is declined, and Casey’s is accepted. The runner verifies the persisted result. No external email was delivered.

## Built with clear boundaries
Python enforces the rules, while Strands orchestrates through narrow tools. SQLite persists offers and an activity trail. Our local dashboard also demonstrates one follow-up per offer and escalation when no backups remain. Fifteen automated tests pass, including duplicate acceptance and qualification-review checks.

## What comes next
Next we will connect the browser to the live agent, add background scheduling and authenticated reply channels, and explore existing volunteer platform integrations. ShiftRescue’s goal is to reduce coordination work while keeping qualification review and volunteer acceptance explicit. The code, MIT license, setup instructions, and run evidence are public on GitHub.