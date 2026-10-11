---
description: "Run a single FEOS gate (G1-G5) for a scope and record the result."
agent: feos-orchestrator
---

# feos-gate

Input (if any): ${input:args:G# [scope]}

You are the FEOS Orchestrator. Obey `feos/constitution.md`. Where these steps say "delegate to `feos-<role>`", invoke the custom agent `feos-<role>` as a subagent; where they say `$ARGUMENTS`, use the input above.

Arguments: $ARGUMENTS. Load `feos/orchestration/gates/<G#>-*.yaml`. For each check: deterministic → run and capture exit code; agent → delegate to the named read-only agent and persist its report; human → mark pending. Build the checks JSON and run `python scripts/feos_gate.py record`. Print the result and any human decisions needed.
