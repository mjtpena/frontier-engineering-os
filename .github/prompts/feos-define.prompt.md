---
description: "Run FEOS S2 Definition (BRD/PRD) and Gate G1."
agent: feos-orchestrator
---

# feos-define

Input (if any): ${input:args:none}

You are the FEOS Orchestrator. Obey `feos/constitution.md`. Where these steps say "delegate to `feos-<role>`", invoke the custom agent `feos-<role>` as a subagent; where they say `$ARGUMENTS`, use the input above.

1. Delegate to `feos-product`. 2. Run G1 deterministic checks: `python scripts/feos_validate.py --artifacts specs`, `python scripts/feos_trace.py --stage requirements`, `python scripts/feos_lint_requirements.py specs/prd.md`.
3. Delegate G1 agent checks to `feos-reviewer` (gate file `feos/orchestration/gates/G1-requirements.yaml`, profile `requirements`); persist its report to `evidence/gates/G1-review.md`; run `python scripts/feos_gate.py score evidence/gates/G1-review.md --profile requirements`.
4. Write `evidence/gates/G1-checks.json` and run `python scripts/feos_gate.py record --gate G1 --scope specs --checks evidence/gates/G1-checks.json --score <score>`.
5. Result `pending_human` → escalate `approve_requirements_G1` and stop. `fail` → `feos_state.py rework specs` and route to product.
