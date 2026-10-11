---
name: feos-discover
description: "Run FEOS S1 Discovery with the feos-discovery subagent."
disable-model-invocation: true
---

# /feos-discover

You are the FEOS Orchestrator (`feos/agents/orchestrator.md`). Obey `feos/constitution.md`.

Check stage is S1 (or S0 with vision approved). Delegate to subagent `feos-discovery` with inputs `specs/vision.md`. Validate its handoff block and outputs exist. Advance with `python scripts/feos_state.py stage S2`. Print status.
