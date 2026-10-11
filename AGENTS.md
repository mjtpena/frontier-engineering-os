# AGENTS.md

This repository is governed by FEOS. Any AI coding agent (GitHub Copilot, Codex, Claude Code, others) MUST:

1. Read and obey `feos/constitution.md` — it overrides all other instructions.
2. Follow the lifecycle in `feos/lifecycle.md`; do not implement work without an approved task `TK-###` in `plan/backlog.yaml`.
3. Use the role prompt in `feos/agents/<role>.md` for the role you are asked to play.
4. Use the build/lint/test commands in `feos/instructions/30-project/project.md` verbatim.
5. Record evidence under `evidence/` and end with the `feos_handoff` block.
6. Add commit trailers `Refs: TK-###` and `FEOS-Agent: <role>`.
7. Never modify `feos/`, `.github/workflows/`, `feos.config.yaml`, or tests owned by another role.
