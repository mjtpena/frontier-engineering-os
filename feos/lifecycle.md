# FEOS Lifecycle, Stages and Gates

## State machine

```
            ┌──────────── rework (≤ max_rework_loops) ────────────┐
            ▼                                                      │
S0 Intake → S1 Discovery → S2 Definition ─G1→ S3 Architecture ─G2→ S4 Planning
                                                                        │
     ┌──────────────────────── per task ────────────────────────────────┘
     ▼
S5 Implementation (Test-first → Build → Verify) ─G3→ (merge task)
     │  all release-scope tasks merged
     ▼
S6 Hardening (Security + RAI + Ops review) ─G4→ ─G5→ HA (Human Approval) → S7 Release → S8 Operate
                                                                                      │
                                                hotfix / next iteration ◄─────────────┘
```

| Stage | Owner agent | Primary outputs | Exit gate |
|---|---|---|---|
| S0 Intake | orchestrator | `specs/vision.md` (draft), `.feos/state.json` | human confirms vision |
| S1 Discovery | discovery | `specs/research-pack.md`, `specs/risk-register.md` | — |
| S2 Definition | product | `specs/brd.md`, `specs/prd.md` | **G1 Requirements** |
| S3 Architecture | architect (+ security for threat model) | `architecture/architecture.md`, `architecture/adrs/*`, `architecture/nfr.md`, `architecture/threat-model.md` | **G2 Architecture** (+ human sign-off) |
| S4 Planning | planner | `plan/backlog.yaml` | schema-valid backlog, traceability complete |
| S5 Implementation | tester → builder → reviewer | tests, code, `evidence/tasks/TK-###/` | **G3 Implementation** (per task) |
| S6 Hardening | security, reviewer, release | `evidence/release/<ver>/` | **G4 Security & RAI**, **G5 Operational readiness** |
| HA | human | `evidence/release/<ver>/approval.md` + GitHub environment approval | human only |
| S7 Release | release | release notes, deployment, rollback plan | deployment verified |
| S8 Operate | release | runbooks, incident records | feeds next iteration |

## Gate mechanics
Each gate in `feos/orchestration/gates/` declares checks of three types:

- `deterministic` — a command; pass/fail from exit code. `feos_gate.py record` runs `python scripts/…` and `project.<key>` (project.md) commands itself. Checks run by CI or external scanners are asserted by the orchestrator with evidence and recorded as `verified_by: caller`.
- `agent` — a read-only agent judges against a rubric and MUST cite evidence (file:line, command output). A verdict without evidence fails.
- `human` — a named human records a decision (`feos_state.py resolve`); `record` reads it from `.feos/state.json`. Never satisfiable by an agent.

Gate result = **FAIL** if any hard check fails; otherwise the weighted score, computed by `record` from the reviewer's report, is compared to the threshold.
Results are written to `evidence/gates/<gate>-<scope>-<timestamp>.json` (schema `feos/schemas/gate-result.schema.json`) and summarised in `.feos/state.json`.

## Rework routing
On FAIL, the gate's `on_fail.route_to` agent receives the failed checks as its input. The counter
`state.rework[<scope>]` increments; at `max_rework_loops` the orchestrator escalates to a human.
