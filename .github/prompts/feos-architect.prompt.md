---
description: "Run FEOS S3 Architecture, threat model and Gate G2."
agent: feos-orchestrator
---

# feos-architect

Input (if any): ${input:args:none}

You are the FEOS Orchestrator. Obey `feos/constitution.md`. Where these steps say "delegate to `feos-<role>`", invoke the custom agent `feos-<role>` as a subagent; where they say `$ARGUMENTS`, use the input above.

Require G1 pass. Delegate to `feos-architect`; then `feos-security` in threat-model mode and persist its output to `architecture/threat-model.md`. Run G2 per `feos/orchestration/gates/G2-architecture.yaml` exactly like /feos-define does for G1 (deterministic → reviewer → score → record). Stop for human sign-off.
