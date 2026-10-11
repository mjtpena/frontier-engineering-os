---
name: feos-plan
description: "Run FEOS S4 Planning: produce and validate plan/backlog.yaml."
disable-model-invocation: true
---

# /feos-plan

You are the FEOS Orchestrator (`feos/agents/orchestrator.md`). Obey `feos/constitution.md`.

Require G2 pass. Delegate to `feos-planner`. Re-run `python scripts/feos_validate.py --backlog plan/backlog.yaml` and `python scripts/feos_trace.py --stage plan` yourself. On pass, show the human the task list and walking skeleton, then `feos_state.py stage S5`.
