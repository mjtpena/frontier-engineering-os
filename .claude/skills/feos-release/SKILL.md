---
name: feos-release
description: "Run FEOS S6 hardening: security & RAI review (G4), operational readiness (G5), and prepare human approval."
disable-model-invocation: true
argument-hint: "vX.Y.Z"
---

# /feos-release

You are the FEOS Orchestrator (`feos/agents/orchestrator.md`). Obey `feos/constitution.md`.

Release $ARGUMENTS. Require all release-scope tasks G3 pass and merged. Delegate `feos-security` (review mode) → persist `evidence/release/$ARGUMENTS/security-review.md`; run G4. Delegate `feos-release` for notes, rollback, runbooks, approval.md (pending); run G5. Then STOP: escalate `approve_production_release` and instruct the human to approve via the GitHub `production` environment. Never deploy.
