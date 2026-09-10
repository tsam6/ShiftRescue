# Accounts and publication

## Owner action: AWS Builder ID
Status: owner reports an existing AWS Builder Center account; Builder ID sign-in
not independently verified. Profile: https://profile.aws.amazon.com/. Account creation requires the owner's identity, email verification, and
password or chosen identity provider. Record confirmation, not credentials, here.
Guide: https://docs.aws.amazon.com/signin/latest/userguide/create-builder-id.html

## Bedrock access
Status: owner believes an AWS Console account exists; Bedrock access remains unverified. Builder ID is separate from AWS
account credentials. Confirm a region, allowed model ID, and a credential profile
with model invocation permission. Never paste secret keys into documentation.

## Public repository
Local Git repository is prepared. Remote GitHub publication remains pending;
no GitHub CLI was found during initial setup. Before submission publish this
project folder, confirm public visibility, README rendering, MIT license detection,
and About description. Keep .venv, .env, runtime data and credentials excluded.

## Submission checklist
- [ ] Public code URL and complete setup instructions
- [ ] MIT license detected and About description mentions MIT
- [ ] Text description: audience, problem, workflow, honest implementation status
- [ ] Architecture diagram matching final system
- [ ] Working demo video <= 5 minutes
- [ ] AWS Builder ID confirmed
- [ ] Optional synthetic live demo URL
- [ ] Optional AWS Builder Center post with Agents for Humans in title

## AWS credit status
Owner reports receiving hackathon credits. Applied balance, expiry, and eligible
services have not been verified; AWS billing currently requires sign-in. Do not invoke paid
models or deploy billable resources without explicit owner approval. Local simulation
requires no AWS credentials or network services.

## Credit verification — September 9, 2026
Verified in signed-in AWS Billing console: total remaining $150, comprising $100
AWS Free Tier credit (expires September 9, 2027) and $50 promotional credit
(expires October 31, 2026). The $50 credit lists Amazon Bedrock and Bedrock
AgentCore among applicable services. Displayed usage is $0; billing estimates
update approximately daily. Browser sign-in is working; local SDK authentication
and model invocation are still unverified.
