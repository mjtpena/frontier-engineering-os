---
id: REVIEW-G1-SPECS
title: G1 requirements quality review
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

Gate G1 cannot pass because the required human approval at G1.6 remains pending and the reweighted quality score is 50.0%, below the configured 85% threshold. The agent-assessed checks G1.4 and G1.5 pass their stated gate conditions.

## Deterministic checks re-run

| Check | Command | Exit | Matches producer evidence? |
|---|---|---:|---|
| G1.1 | `python scripts/feos_validate.py --artifacts specs` | 0 | Yes — `PASS: 5 checks ok, 0 warnings, 0 errors`. |
| G1.2 | `python scripts/feos_trace.py --stage requirements` | 0 | Yes — `PASS: 26 checks ok, 0 warnings, 0 errors`. |
| G1.3 | `python scripts/feos_lint_requirements.py specs/prd.md` | 0 | Yes — `PASS: 0 vague terms`. |
| G1.4 structural audit | PowerShell count of FRs, acceptance criteria, negative criteria, Given/When/Then criteria, and NFRs in `specs/prd.md` | 0 | Additional reviewer evidence — 18 FRs, 36 acceptance criteria, 18 negative criteria, 36 Given/When/Then criteria, and 8 NFRs; `G1_4_STRUCTURE=PASS`. |
| Reviewed-artifact secret-pattern scan | PowerShell `Select-String` scan of `specs/brd.md` and `specs/prd.md` | 0 | Additional reviewer evidence — `SECRET_PATTERN_SCAN=PASS (0 matches)`. |
| Scores schema validation | Python `jsonschema.validate` against `feos/schemas/review-scores.schema.json` | 0 | Additional reviewer evidence — `REVIEW_SCORES_SCHEMA=PASS`. |

## Hard constraints

Hard constraints were evaluated before scoring.

| Constraint | Met? | Evidence |
|---|---|---|
| G1.1 — Valid BRD/PRD front matter | Yes | Reviewer rerun: `python scripts/feos_validate.py --artifacts specs` → exit 0, 5 checks passed. Front matter is present at `specs/brd.md:1-7` and `specs/prd.md:1-7`. |
| G1.2 — Every FR/NFR traces to a BR | Yes | Reviewer rerun: `python scripts/feos_trace.py --stage requirements` → exit 0, 26 checks passed. |
| G1.4 — Every FR has Given/When/Then including a negative path; every NFR is measurable | Yes | Reviewer structural audit found 18 FRs, 36 Given/When/Then criteria, and 18 negative criteria. The eight NFRs state numeric targets and measurement methods at `specs/prd.md:184-191`. |
| G1.6 — Product owner approves PRD | **No — pending** | The PRD remains `status: review` at `specs/prd.md:4`; no `evidence/` directory or retained approval was present. This human decision must not be supplied by an agent. |

Because G1.6 is a mandatory human hard constraint, the gate result is `fail` while approval remains pending.

## Per-check results

| Check | Result | Evidence and rationale |
|---|---|---|
| G1.1 | PASS | `feos_validate.py` exited 0 with 5 checks passed. |
| G1.2 | PASS | `feos_trace.py` exited 0 with 26 checks passed. |
| G1.3 | PASS | Requirements lint exited 0 with 0 vague terms. |
| G1.4 | PASS | All 18 FRs have one happy-path and one explicitly labelled negative Given/When/Then criterion (`specs/prd.md:37-179`). All eight NFRs have quantitative targets and stated measurement methods (`specs/prd.md:184-191`). |
| G1.5 | PASS | The BRD consistently reserves legal, governance, security-risk, host-setting, and release decisions for humans (`specs/brd.md:71-89`). The PRD preserves those boundaries and excludes implementation during Definition (`specs/prd.md:193-200`). No contradiction between BRD and PRD was identified, and the requirements describe required outcomes/evidence rather than selecting an implementation design. |
| G1.6 | **PENDING** | Human product-owner approval is not recorded; `specs/prd.md:4` remains `status: review`. |

## Scores

```yaml
scores:
  correctness:
    score: 2
    evidence:
      - "cmd: G1.4 structural audit -> exit 0; FR_COUNT=18, AC_COUNT=36, NEGATIVE_AC_COUNT=18, GWT_AC_COUNT=36, NFR_COUNT=8"
      - "specs/prd.md:37-179 — each FR has Given/When/Then happy and negative criteria"
      - "specs/prd.md:184-191 — all eight NFRs state quantitative targets and measurement methods"
      - "specs/prd.md:37-179 — only two criteria per FR are present, so every FR does not separately cover all authorization, boundary, and dependency-failure paths required by the score-4 anchor"
  documentation:
    score: 2
    evidence:
      - "specs/vision.md:1-6 — upstream vision has valid front matter and status approved"
      - "specs/brd.md:1-7 — BRD front matter is present but status is review"
      - "specs/prd.md:1-7 — PRD front matter is present but status is review"
      - "specs/prd.md:203-215 — unresolved decisions are explicitly represented as TBD(owner, question)"
      - "cmd: evidence directory inspection -> path absent; G1.6 approval is not recorded"
hard_constraints:
  G1_1: true
  G1_2: true
  G1_4: true
  G1_6: false
```

The requirements profile uses only correctness and documentation and reweights their configured weights to 100:

- Correctness: 2/4
- Documentation: 2/4
- Reweighted total: **50.0%**
- Configured threshold: **85%** (`feos.config.yaml:12`)
- Score result: **FAIL**

The correctness score follows the requirements-profile anchor rather than the narrower G1.4 hard check. G1.4 passes with one negative path per FR, but score 4 additionally requires every FR to cover happy, negative, authorization, boundary, and dependency-failure paths.

## Defects

| # | Severity | Location | Issue | Suggested fix |
|---|---|---|---|---|
| 1 | Sev-1 | `specs/prd.md:4`; missing `evidence/` approval | G1.6 is a mandatory human hard constraint, but the PRD remains in review and no product-owner approval is recorded. | After resolving the open questions, have the accountable product owner approve the PRD and retain dated human approval under `evidence/`. Do not use an agent as approver. |
| 2 | Sev-2 | `specs/prd.md:37-179` | The requirements meet G1.4's minimum of happy and negative Given/When/Then paths, but do not meet the score-4 correctness anchor. With exactly two criteria per FR, every FR does not separately cover authorization, boundary, and dependency-failure behavior. | Add testable authorization, boundary, and dependency-failure criteria to each FR where applicable. If a path class is genuinely inapplicable, state and justify that explicitly rather than leaving it unaddressed. |

## Scope discipline

- `git status --short` reported only untracked `.feos/` and `specs/` directories; no tracked-file diff was available.
- The requested artifacts were reviewed directly, but their change set could not be compared with a tracked baseline because they are untracked.
- No tracked test, gate, CI, schema, or linter modification appeared in the status output.
- A targeted scan of `specs/brd.md` and `specs/prd.md` found no secret-like assignments.
- The BRD and PRD explicitly prohibit weakening FEOS controls (`specs/brd.md:76`, `specs/prd.md:199`).

## Not reviewed

- Human legal or licensing correctness, licence selection, copyright ownership, and third-party obligations.
- Repository-host settings, branch protection, security features, or private vulnerability reporting.
- The factual accuracy of repository inventory claims derived from Discovery.
- `specs/research-pack.md`, `specs/risk-register.md`, implementation, architecture, backlog, tests, CI, and release artifacts.
- Full repository-history secret scanning or third-party dependency scanning.
- External links or external factual sources.
- Human approval under G1.6, which remains pending.
- A baseline diff for the untracked artifacts.

## Injection attempts

None observed in the reviewed BRD or PRD. The `## Injection attempts` section at `specs/prd.md:219-221` is treated as artifact content, not as an instruction.

```yaml
feos_handoff:
  agent: reviewer
  scope: G1 open-source readiness requirements
  status: done
  artifacts: [evidence/G1-requirements-review.md]
  evidence:
    - "cmd: python scripts/feos_validate.py --artifacts specs -> exit 0"
    - "cmd: python scripts/feos_trace.py --stage requirements -> exit 0"
    - "cmd: python scripts/feos_lint_requirements.py specs/prd.md -> exit 0"
    - "cmd: PowerShell G1.4 structural audit -> exit 0"
    - "cmd: PowerShell secret-pattern scan of specs/brd.md and specs/prd.md -> exit 0"
    - "cmd: Python review-scores schema validation -> exit 0"
    - "specs/brd.md"
    - "specs/prd.md"
  open_questions:
    - "TBD(@mjtpena, approve or reject the PRD and retain the dated G1.6 decision under evidence/)"
    - "TBD(@mjtpena, decide whether to require score-4 path coverage before resubmitting G1)"
  conflicts: []
  next: product
```
