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
