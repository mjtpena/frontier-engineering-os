---
name: feos-init
description: "Initialise FEOS in this repo: create state, check prerequisites, and walk the human through config gaps."
disable-model-invocation: true
argument-hint: "[release e.g. v0.1.0]"
---

# /feos-init

You are the FEOS Orchestrator (`feos/agents/orchestrator.md`). Obey `feos/constitution.md`.

1. Run `python -m pip install -r scripts/requirements.txt` if imports fail, then `python scripts/feos_validate.py`. Fix nothing under `feos/` — report failures to the human.
2. `python scripts/feos_state.py init --release <version>` using `$ARGUMENTS` as the version (default `v0.1.0` if empty).
3. Read `feos.config.yaml`, `feos/orchestration/raci.yaml`, `feos/instructions/30-project/project.md`. List every `TBD` and ask the human for values in one consolidated question list. Do not guess names, commands or owners.
4. Verify GitHub settings the human must configure (branch protection, `production` environment reviewers, secret scanning) and list them as a checklist.
5. If `specs/vision.md` is absent, copy `feos/templates/vision.md` to it and interview the human to fill it.
6. Finish with the orchestrator status report.
