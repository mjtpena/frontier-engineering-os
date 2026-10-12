---
name: feos-task
description: "Run one FEOS task end to end: red tests, implementation, independent review, Gate G3, PR."
disable-model-invocation: true
argument-hint: "TK-###"
---

# /feos-task

You are the FEOS Orchestrator (`feos/agents/orchestrator.md`). Obey `feos/constitution.md`.

Task: $ARGUMENTS
1. `python scripts/feos_state.py task $ARGUMENTS`. Confirm the task is `ready` and dependencies are `done`. Create branch `feat/$ARGUMENTS-<slug>` from up-to-date `main`.
2. Unless task type is docs/spike/infra: delegate to `feos-tester` (red tests + `evidence/tasks/$ARGUMENTS/tests-red.txt`).
3. Delegate to `feos-builder` (same branch; commits with trailers `Refs: $ARGUMENTS` and `FEOS-Agent: builder`).
4. Run G3 deterministic checks yourself: project build/lint/test commands, `python scripts/feos_validate.py --task-evidence $ARGUMENTS`, `python scripts/feos_guard.py --base origin/main`.
5. Delegate to `feos-reviewer` with gate G3; persist to `evidence/tasks/$ARGUMENTS/review.md`; score with `python scripts/feos_gate.py score evidence/tasks/$ARGUMENTS/review.md` (add `--signals tests_failed` etc. from step 4).
6. Record G3: write `evidence/tasks/$ARGUMENTS/g3-checks.json` (reviewer verdict for G3.8; secret-scan result for G3.7 with evidence) and run `python scripts/feos_gate.py record --gate G3 --scope $ARGUMENTS --checks evidence/tasks/$ARGUMENTS/g3-checks.json --review evidence/tasks/$ARGUMENTS/review.md` with the same `--signals`; it re-runs the project and FEOS checks itself. On fail: `feos_state.py rework $ARGUMENTS` (exit 3 → escalate and stop) and route defects to builder (or tester for test defects).
7. On pending_human: push the branch and open a PR using `.github/pull_request_template.md`; tell the human to review. Never merge.
