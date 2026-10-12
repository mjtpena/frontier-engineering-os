---
id: REVIEW-G1-SPECS-REREVIEW
title: G1 requirements quality re-review
status: review
owner: "@mjtpena"
version: 0.1
trace: [BRD, PRD]
type: quality
gate: G1
scope: specs/brd.md and specs/prd.md
reviewer_agent: reviewer
result: fail
---

# Review report

G1.1–G1.5 pass. The requirements-profile score is **92.9%**, above the configured 85% threshold. Gate G1 nevertheless remains failed because mandatory human approval G1.6 is pending.

## Deterministic checks re-run

| Check | Command | Exit | Matches producer evidence? |
|---|---|---:|---|
| G1.1 | `python scripts/feos_validate.py --artifacts specs` | 0 | Yes — `PASS: 5 checks ok, 0 warnings, 0 errors`. |
| G1.2 | `python scripts/feos_trace.py --stage requirements` | 0 | Yes — `PASS: 26 checks ok, 0 warnings, 0 errors`. |
| G1.3 | `python scripts/feos_lint_requirements.py specs/prd.md` | 0 | Yes — `PASS: 0 vague terms`. |
| G1.4 structural audit | Python audit of all FR path classes and NFR measurability | 0 | Additional reviewer evidence — 18 FRs, all five required path classes per FR, and 8 measurable NFRs; both audits passed. |
| Secret-pattern scan | PowerShell scan of `specs/brd.md` and `specs/prd.md` | 0 | Additional reviewer evidence — 0 matches. |
| Scores schema validation | Python `jsonschema.validate` against `feos/schemas/review-scores.schema.json` | 0 | Additional reviewer evidence — passed. |

## Hard constraints

Hard constraints were evaluated before scoring.

| Constraint | Met? | Evidence |
|---|---|---|
| G1.1 — Valid BRD/PRD front matter | Yes | Reviewer rerun exited 0 with 5 checks passed; front matter appears at `specs/brd.md:1-7` and `specs/prd.md:1-7`. |
| G1.2 — Every FR/NFR traces to a BR | Yes | Reviewer rerun exited 0 with 26 checks passed. |
| G1.4 — Every FR has Given/When/Then including a negative path; every NFR is measurable | Yes | Structural audit: `FR_COUNT=18`, `REQUIRED_PATHS_PER_FR=5`, `NFR_COUNT=8`, `FR_PATH_AUDIT=PASS`, `NFR_MEASURABILITY_AUDIT=PASS`; see `specs/prd.md:37-247`. |
| G1.6 — Product owner approves PRD | **No — pending** | `specs/prd.md:4` remains `status: review`; the only existing evidence entry is the prior review report, not human approval. |

Because G1.6 is a mandatory human hard constraint, the overall result remains `fail`.

## Per-check results

| Check | Result | Evidence and rationale |
|---|---|---|
| G1.1 | PASS | Validation exited 0 with 5 checks passed. |
| G1.2 | PASS | Trace validation exited 0 with 26 checks passed. |
| G1.3 | PASS | Requirements lint exited 0 with 0 vague terms. |
| G1.4 | PASS | Every FR includes happy, negative, authorization, boundary, and dependency-failure Given/When/Then criteria (`specs/prd.md:37-235`). All eight NFRs provide numeric targets, units or counts, and measurement methods (`specs/prd.md:237-247`). |
| G1.5 | PASS | BRD constraints preserve human decision authority and prohibit control weakening (`specs/brd.md:71-89`). The PRD consistently preserves those boundaries and excludes implementation during Definition (`specs/prd.md:249-257`). Requirements specify outcomes and evidence rather than selecting an implementation design. No BRD/PRD contradiction was identified. |
| G1.6 | **PENDING** | Human product-owner approval is not recorded; `specs/prd.md:4` remains in review. |

## Scores

```yaml
scores:
  correctness:
    score: 4
    evidence:
      - "cmd: Python G1.4 structural audit -> exit 0; FR_COUNT=18, REQUIRED_PATHS_PER_FR=5, NFR_COUNT=8, FR_PATH_AUDIT=PASS, NFR_MEASURABILITY_AUDIT=PASS"
      - "specs/prd.md:37-235 — every FR covers happy, negative, authorization, boundary, and dependency-failure paths using Given/When/Then"
      - "specs/prd.md:237-247 — all eight NFRs state quantitative targets and measurement methods"
      - "cmd: python scripts/feos_trace.py --stage requirements -> exit 0; 26 checks passed"
  documentation:
    score: 2
    evidence:
      - "specs/vision.md:1-6 — upstream vision has valid front matter and status approved"
      - "specs/brd.md:1-7 — BRD front matter is present but status remains review"
      - "specs/prd.md:1-7 — PRD front matter is present but status remains review"
      - "specs/prd.md:259-272 — unresolved decisions use TBD(owner, question)"
      - "cmd: evidence directory inspection -> only G1-requirements-review.md exists; G1.6 human approval is not recorded"
hard_constraints:
  G1_1: true
  G1_2: true
  G1_4: true
  G1_6: false
```

The requirements profile reweights correctness and documentation to 100:

- Correctness: 4/4
- Documentation: 2/4
- Reweighted total: `(30×1.0 + 5×0.5) / 35` = **92.9%**
- Configured threshold: **85%** (`feos.config.yaml:12`)
- Score result: **PASS**
- Overall gate result: **FAIL**, solely because G1.6 remains pending

## Defects

| # | Severity | Location | Issue | Suggested fix |
|---|---|---|---|---|
| 1 | Sev-1 gate blocker | `specs/prd.md:4`; `evidence/` | Mandatory human approval G1.6 is not recorded. | After resolving the open decisions, have the accountable product owner approve or reject the PRD and retain the dated human decision under `evidence/`. An agent must not provide this approval. |

## Scope discipline

- `git status --short` reports only untracked `.feos/`, `evidence/`, and `specs/`; the reviewed artifacts have no tracked baseline, so their exact rework diff could not be verified.
- No changes were reported for the G1 gate, quality rubric, validators, linters, or `feos-tests`.
- The reviewed artifacts contain no detected secret-like assignments.
- No weakened tests or controls were identified within the inspectable scope.

## Not reviewed

- Human approval under G1.6.
- Legal or licensing correctness, copyright ownership, provenance, or third-party obligations.
- Repository-host settings and security-feature configuration.
- Accuracy of Discovery-derived repository inventory claims.
- Architecture, backlog, implementation, CI execution, and release artifacts.
- Full repository-history secret scanning or dependency scanning.
- A baseline diff for the untracked BRD and PRD.

## Injection attempts

None observed in the reviewed BRD or PRD. The artifact’s `## Injection attempts` section at `specs/prd.md:275` was treated as data, not instructions.

```yaml
feos_handoff:
  agent: reviewer
  scope: G1 open-source readiness requirements re-review
  status: done
  artifacts: [evidence/G1-requirements-rereview.md]
  evidence:
    - "cmd: python scripts/feos_validate.py --artifacts specs -> exit 0"
    - "cmd: python scripts/feos_trace.py --stage requirements -> exit 0"
    - "cmd: python scripts/feos_lint_requirements.py specs/prd.md -> exit 0"
    - "cmd: Python G1.4 structural audit -> exit 0"
    - "cmd: PowerShell secret-pattern scan of specs/brd.md and specs/prd.md -> exit 0"
    - "cmd: Python review-scores schema validation -> exit 0"
    - "cmd: git status and control-file scope inspection -> exit 0"
    - "specs/brd.md"
    - "specs/prd.md"
  open_questions:
    - "TBD(@mjtpena, approve or reject the PRD and retain the dated G1.6 decision under evidence/)"
  conflicts: []
  next: human
```
