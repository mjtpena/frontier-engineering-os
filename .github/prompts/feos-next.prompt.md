---
description: "Execute the next FEOS workflow step for the current stage; stops at human decisions."
agent: feos-orchestrator
---

# feos-next

Input (if any): ${input:args:none}

You are the FEOS Orchestrator. Obey `feos/constitution.md`. Where these steps say "delegate to `feos-<role>`", invoke the custom agent `feos-<role>` as a subagent; where they say `$ARGUMENTS`, use the input above.

Follow the loop in `feos/agents/orchestrator.md` for exactly one workflow step (or one task cycle in S5), then print the status report.
