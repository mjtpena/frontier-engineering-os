# Frontier Engineering Operating System (FEOS) — v1.0 kit

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

## Changing the framework
Edit canonical files under `feos/`, run `python scripts/feos_render.py`, open a PR (CODEOWNERS). In Claude Code, set `FEOS_FRAMEWORK_EDIT=1` for that session, otherwise the protection hook blocks edits.

See `JUDGEMENT.md` for the pre-handoff review, verified behaviour and known limitations.
