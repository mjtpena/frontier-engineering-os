# Initiative archive: open-source readiness (FEOS dogfooding run)

This folder is a **record**, not live project state. It is the FEOS lifecycle run on this repository to assess its own readiness for public open-source use. It was copied here from the working paths (`specs/`, `evidence/`, `.feos/state.json`).

| Item | State at archive (2026-10-13) |
|---|---|
| Vision | Approved by @mjtpena (2026-10-11) |
| S2 Definition | BRD and PRD written: 18 FRs, 8 NFRs |
| Gate G1 (requirements) | `pending_human`. G1.1–G1.5 pass, and the reviewer score is 92.9% (threshold 85). The human approval G1.6 was **not** recorded |
| S3–S6 | Not started |

The baseline items the PRD tracks (licence, contribution, conduct, security reporting and support) were added directly at the owner's request, outside the lifecycle. See the root `LICENSE`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SECURITY.md` and `SUPPORT.md`. The open questions in [`specs/prd.md`](specs/prd.md) (governance model, maintenance commitments, compatibility matrix, release policy, domain applicability) remain open.

## Why it is not at the FEOS working paths
At `specs/`, CI's traceability step (`scripts/feos_trace.py`) would require the architecture and `@covers` tests for all 18 FRs, and those stages have not run. Archiving the run keeps the required `feos-validate` check honest without weakening it.

Paths inside these files (for example `evidence/gates/...`) are relative to the repository root at the time they were written.

## Contents
- `specs/`: vision, research pack, risk register, BRD, PRD
- `evidence/`: G1 reviewer reports, check results, gate record
- `state/state.json`: snapshot of the FEOS state ledger
