---
description: "Run a single FEOS gate (G1-G5) for a scope and record the result."
agent: feos-orchestrator
---

# feos-gate

Input (if any): ${input:args:G# [scope]}

You are the FEOS Orchestrator. Obey `feos/constitution.md`. Where these steps say "delegate to `feos-<role>`", invoke the custom agent `feos-<role>` as a subagent; where they say `$ARGUMENTS`, use the input above.

Arguments: $ARGUMENTS. Load `feos/orchestration/gates/<G#>-*.yaml`. For each check: deterministic with cmd `python scripts/…` or `project.<key>` → nothing to do, `record` runs it; other deterministic (CI, external scanner) → its status and evidence (run URL or report path) go in the claims JSON; agent → delegate to the named read-only agent, persist its report, and put its verdict with evidence in the claims JSON; human → nothing, `record` reads `.feos/state.json`. Run `python scripts/feos_gate.py record --gate <G#> --scope <scope> --checks <claims.json>`, adding `--review <persisted reviewer report>` for G1–G3. Print the result and any human decisions needed.
