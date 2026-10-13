# Frontier Engineering Operating System (FEOS)

[![feos-validate](https://github.com/mjtpena/frontier-engineering-os/actions/workflows/feos-validate.yml/badge.svg)](https://github.com/mjtpena/frontier-engineering-os/actions/workflows/feos-validate.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

An AI-native delivery operating system for Microsoft-centric engineering teams: **specifications → specialist agents → gates → human approval → production**.
Works with **Claude Code** (subagents, skills, hooks) and **GitHub Copilot** (custom agents, instructions, prompt files) from one canonical source.

## How it works
| Layer | Where | Enforced by |
|---|---|---|
| Constitution (binding rules) | `feos/constitution.md` | every agent prompt; CI; hooks |
| Lifecycle & state machine | `feos/lifecycle.md`, `feos/orchestration/workflows/*.yaml`, `.feos/state.json` | orchestrator + `scripts/feos_state.py` |
| Specialist agents (canonical) | `feos/agents/*.md`, registry `feos/orchestration/agents.manifest.yaml` | rendered to `.claude/agents/` and `.github/agents/` by `scripts/feos_render.py` |
| Instruction layers L1–L5 | `feos/instructions/` (`precedence.md`) | agents load per manifest |
| Templates | `feos/templates/` | `feos_validate.py --artifacts` |
| Gates G1–G5 | `feos/orchestration/gates/*.yaml` | `feos_gate.py`, CI, CODEOWNERS, GitHub environments |
| Quality / security / AI rubrics | `feos/orchestration/evaluations/*.yaml` | `feos_gate.py score`, `feos_gate.py ai-eval` |
| Separation of duties | read-only reviewer/security; tester owns tests | tool allow-lists, `feos_guard.py`, Claude hook `feos_hook_protect.py` |
| Who decides | `feos/orchestration/raci.yaml` | human-only decisions can't be recorded by agents |

> **Status:** v1.0 pilot kit, with no tagged releases yet. The deterministic layer (scripts, CI, hook, branch protection) is tested. The workflows themselves are followed by LLM agents, not by a runtime engine. Read [JUDGEMENT.md](JUDGEMENT.md) for what is verified and what is not.

## Adopting FEOS in your repository
1. Copy `feos/`, `scripts/`, `feos-tests/`, `.claude/`, `.github/`, `CLAUDE.md`, `AGENTS.md` and `feos.config.yaml` into the root of your repository. Merge, rather than overwrite, any of these files you already have.
2. Do the human set-up below. In particular, fill the `TBD` values and choose your platform and domain layers in `feos.config.yaml`.
3. Run the quick start for your tool. [HANDOFF_PROMPT.md](HANDOFF_PROMPT.md) is a scripted install-and-prove run for Claude Code.

## Quick start (Claude Code)
```bash
pip install -r scripts/requirements.txt
python scripts/feos_validate.py && python scripts/feos_render.py --check && pytest -q feos-tests
claude            # then: /feos-init  →  /feos-status  →  /feos-next
```
## Quick start (GitHub Copilot, VS Code)
Select agent **feos-orchestrator** in Chat, or run prompt files `/feos-init`, `/feos-next`, `/feos-task TK-001`.

## Human set-up you must do (agents can't)
1. Fill `TBD` values in `feos.config.yaml`, `feos/orchestration/raci.yaml`, `.github/CODEOWNERS`, `feos/instructions/30-project/project.md`.
2. Branch protection on `main`: PR + required checks `feos-validate` + CODEOWNERS review.
3. GitHub environment `production` with required reviewers (this is the technical enforcement of Human Approval).
4. Enable secret scanning + push protection, Dependabot, code scanning. Pin Actions to commit SHAs.
5. Calibrate and approve AI thresholds in `feos/orchestration/evaluations/ai-quality.yaml` (set `approved_by`).
6. Claude Code: open the repository interactively once and accept the workspace-trust prompt. Until then the project `allow` rules in `.claude/settings.json` are ignored (deny rules always apply).
7. Claude Code: if `.claude/agents/` or `.claude/skills/` did not exist when a session started, that session may not load them; start a new session (or run `/reload-skills`).

## Changing the framework
Edit canonical files under `feos/`, run `python scripts/feos_render.py`, open a PR (CODEOWNERS). In Claude Code, set `FEOS_FRAMEWORK_EDIT=1` for that session, otherwise the protection hook blocks edits.

See [JUDGEMENT.md](JUDGEMENT.md) for the pre-handoff review, verified behaviour and known limitations.

## Contributing
Contributions are welcome. Read [CONTRIBUTING.md](CONTRIBUTING.md) and the [code of conduct](CODE_OF_CONDUCT.md). For help, see [SUPPORT.md](SUPPORT.md). Changes are tracked in [CHANGELOG.md](CHANGELOG.md).

## Security
Please report vulnerabilities privately, as described in [SECURITY.md](SECURITY.md). Do not use public issues.

## Licence
[MIT](LICENSE) © 2026 Michael John Peña.
