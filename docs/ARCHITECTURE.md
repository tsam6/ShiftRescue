# Architecture

## Implemented today
```mermaid
flowchart LR
    UI[Local coordinator dashboard] --> API[Loopback HTTP API]
    API --> Workflow[Local simulation workflow]
    CLI[CLI] --> Workflow
    Workflow --> Store[(SQLite state, booking, outbox, audit)]
    Workflow --> Rules
    CLI --> Rules[Deterministic eligibility checks]
    Data[Synthetic JSON roster and shift] --> Rules
    Rules --> Plan[Coverage plan for review]
    Agent[Strands agent / Bedrock] --> Tool[Inspect and advance tools]
    Tool --> Rules
    Tool --> Workflow
```

## Planned MVP
```mermaid
flowchart LR
    UI[Coordinator interface] --> API[Application API]
    API --> DB[(SQLite: shifts, offers, bookings, audit)]
    API --> Agent[Strands agent on Bedrock]
    Agent --> Tools[Eligibility, offers, status, escalation tools]
    Tools --> DB
    Tools --> Outbox[Authorized email outbox]
    Outbox --> Email[Email delivery adapter]
    Reply[Authenticated acceptance / decline] --> API
    Timer[Offer expiry worker] --> API
```
The final architecture diagram must reflect the deployed implementation.
Booking uniqueness, expiry, role checks, and consent are enforced outside the model.
