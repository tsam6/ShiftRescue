# Submission readiness — September 14, 2026

## Verified
- Public source repository: https://github.com/tsam6/ShiftRescue
- MIT license detected by GitHub; About description identifies the license.
- README, bundled fixture/interface, and setup instructions are present.
- AWS authentication and a real Strands/Bedrock covered-workflow run succeeded.
- Model used: `us.amazon.nova-lite-v1:0`, region `us-east-1`.
- 15 automated tests pass.
- Architecture image and demo video files are included.
- Public Devpost page: https://devpost.com/software/shiftrescue

## Owner-managed submission fields
- Confirm the AWS Builder ID field using the owner's Builder account/profile.
  Builder ID is not an AWS account number or access key.
- Upload the chosen demo video to a supported public/unlisted video host and save
  that URL in Devpost. The polished music and silent versions are both 1:47.
- Confirm the final saved video and submission status in Devpost.

## Optional items
A hosted live demo, AgentCore deployment, and AWS Builder Center blog post are not
implemented or claimed. The localhost URL is only for running the project locally.

## AWS setup for reviewers
Use your own AWS credential profile and an accessible Bedrock model or inference
profile. AWS credits can offset costs but are not required to run the application.
No credentials or real volunteer data are included in this repository. Offline
replays and the coordinator dashboard do not make AWS calls.
