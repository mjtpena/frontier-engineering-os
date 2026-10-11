---
id: PRD
title: Leave balance assistant
status: approved
owner: Jane Citizen
version: 1.0
trace: [BRD]
---
# PRD
## Functional requirements
### FR-001 — Show leave balance
- **Traces:** BR-001
- **Acceptance criteria:**
  - AC1 — Given an authenticated employee When they ask for their balance Then the balance from the HR system is shown
  - AC2 (negative) — Given an unauthenticated user When they ask Then access is denied with 401

## Non-functional requirements
| ID | Category | Requirement (measurable) | Measurement method | Traces |
|---|---|---|---|---|
| NFR-001 | Performance | p95 latency <= 300 ms at 50 RPS | load test in staging | BR-001 |
