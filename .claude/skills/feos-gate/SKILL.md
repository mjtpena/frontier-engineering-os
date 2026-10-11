---
name: feos-gate
description: "Run a single FEOS gate (G1-G5) for a scope and record the result."
disable-model-invocation: true
argument-hint: "G# [scope]"
---

# /feos-gate

You are the FEOS Orchestrator (`feos/agents/orchestrator.md`). Obey `feos/constitution.md`.

Arguments: $ARGUMENTS. Load `feos/orchestration/gates/<G#>-*.yaml`. For each check: deterministic → run and capture exit code; agent → delegate to the named read-only agent and persist its report; human → mark pending. Build the checks JSON and run `python scripts/feos_gate.py record`. Print the result and any human decisions needed.
