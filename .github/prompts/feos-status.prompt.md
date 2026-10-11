---
description: "Show FEOS stage, gate results, rework counters, pending human decisions and the next step."
agent: feos-orchestrator
---

# feos-status

Input (if any): ${input:args:none}

You are the FEOS Orchestrator. Obey `feos/constitution.md`. Where these steps say "delegate to `feos-<role>`", invoke the custom agent `feos-<role>` as a subagent; where they say `$ARGUMENTS`, use the input above.

Run `python scripts/feos_state.py show`, read the workflow for the current stage, and print the status report format from `feos/agents/orchestrator.md`. Make no changes.
