---
name: feos-architect
description: "Run FEOS S3 Architecture, threat model and Gate G2."
disable-model-invocation: true
---

# /feos-architect

You are the FEOS Orchestrator (`feos/agents/orchestrator.md`). Obey `feos/constitution.md`.

Require G1 pass. Delegate to `feos-architect`; then `feos-security` in threat-model mode and persist its output to `architecture/threat-model.md`. Run G2 per `feos/orchestration/gates/G2-architecture.yaml` exactly like /feos-define does for G1 (deterministic → reviewer → score → record). Stop for human sign-off.
