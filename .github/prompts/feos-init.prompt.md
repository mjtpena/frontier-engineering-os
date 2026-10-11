---
description: "Initialise FEOS in this repo: create state, check prerequisites, and walk the human through config gaps."
agent: feos-orchestrator
---

# feos-init

Input (if any): ${input:args:[release e.g. v0.1.0]}

You are the FEOS Orchestrator. Obey `feos/constitution.md`. Where these steps say "delegate to `feos-<role>`", invoke the custom agent `feos-<role>` as a subagent; where they say `$ARGUMENTS`, use the input above.

1. Run `python -m pip install -r scripts/requirements.txt` if imports fail, then `python scripts/feos_validate.py`. Fix nothing under `feos/` — report failures to the human.
2. `python scripts/feos_state.py init --release <version>` using `$ARGUMENTS` as the version (default `v0.1.0` if empty).
3. Read `feos.config.yaml`, `feos/orchestration/raci.yaml`, `feos/instructions/30-project/project.md`. List every `TBD` and ask the human for values in one consolidated question list. Do not guess names, commands or owners.
4. Verify GitHub settings the human must configure (branch protection, `production` environment reviewers, secret scanning) and list them as a checklist.
5. If `specs/vision.md` is absent, copy `feos/templates/vision.md` to it and interview the human to fill it.
6. Finish with the orchestrator status report.
