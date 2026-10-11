---
description: "Run one FEOS task end to end: red tests, implementation, independent review, Gate G3, PR."
agent: feos-orchestrator
---

# feos-task

Input (if any): ${input:args:TK-###}

You are the FEOS Orchestrator. Obey `feos/constitution.md`. Where these steps say "delegate to `feos-<role>`", invoke the custom agent `feos-<role>` as a subagent; where they say `$ARGUMENTS`, use the input above.

Task: $ARGUMENTS
1. `python scripts/feos_state.py task $ARGUMENTS`. Confirm the task is `ready` and dependencies are `done`. Create branch `feat/$ARGUMENTS-<slug>` from up-to-date `main`.
2. Unless task type is docs/spike/infra: delegate to `feos-tester` (red tests + `evidence/tasks/$ARGUMENTS/tests-red.txt`).
3. Delegate to `feos-builder` (same branch; commits with trailers `Refs: $ARGUMENTS` and `FEOS-Agent: builder`).
4. Run G3 deterministic checks yourself: project build/lint/test commands, `python scripts/feos_validate.py --task-evidence $ARGUMENTS`, `python scripts/feos_guard.py --base origin/main`.
5. Delegate to `feos-reviewer` with gate G3; persist to `evidence/tasks/$ARGUMENTS/review.md`; score with `python scripts/feos_gate.py score evidence/tasks/$ARGUMENTS/review.md` (add `--signals tests_failed` etc. from step 4).
6. Record G3 (`feos_gate.py record --gate G3 --scope $ARGUMENTS ...`). On fail: `feos_state.py rework $ARGUMENTS` (exit 3 → escalate and stop) and route defects to builder (or tester for test defects).
7. On pending_human: push the branch and open a PR using `.github/pull_request_template.md`; tell the human to review. Never merge.
