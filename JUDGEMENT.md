# Pre-handoff judgement — FEOS kit v1.0

## Verdict
**Fit for handoff as a v1.0 pilot kit.** The framework's own checks pass, and the enforcement scripts behave as intended in tests.
It is **not** a workflow engine. The YAML workflows are declarative contracts that the orchestrator (an LLM) follows.
Hard guarantees come only from the deterministic layer: scripts, CI, the hook, branch protection and GitHub environments.

## What was verified (executed, not assumed)
| Check | Result |
|---|---|
| `python scripts/feos_validate.py` (124 cross-reference checks: agents, layers, templates, gates, workflows, RACI, schemas, adapters, skills) | PASS |
| `python scripts/feos_render.py --check` (Claude/Copilot adapters identical to canonical prompts) | PASS |
| `pytest feos-tests` (20 behavioural tests on sample project) | 20 passed |
| All YAML parses; all JSON Schemas valid (Draft 2020-12) | PASS |
| Adapter front-matter parses as YAML (name, description, tools) | PASS |

Behaviours proven by tests:
- Read-only agents given write tools are rejected.
- Gates without a human check are rejected.
- Adapter drift is detected.
- Backlog validation catches dependency cycles and tasks over 8 h.
- Orphan FRs are detected at the requirements and tests stages.
- The vague-term lint works.
- A score without evidence counts as 0, and a capped dimension fails the gate.
- AI eval fails while thresholds are not human-approved, and fails on a slice breach.
- A hard-check failure beats a 99 score; missing machine evidence fails the gate; outstanding human checks return `pending_human`.
- The rework cap escalates on the 3rd loop.
- The hook blocks edits to `feos/` and `.github/workflows/`.
- The guard blocks a builder from editing pre-existing tests **and** tests added on the branch by the tester.

## Defects found during judging and fixed
1. Agent descriptions containing `: ` produced **invalid YAML front-matter** (e.g. reviewer). Fixed: descriptions are now JSON-quoted by the renderer.
2. Workflow outputs like `[evidence/tasks/{task}/x]` were **invalid YAML flow sequences**. Fixed: quoted.
3. **Separation-of-duties hole:** the builder could rewrite the tester's red tests, because they were added on the same branch rather than at the base. Fixed: the guard now tracks tester-owned files per branch. A regression test was added.
4. **Branch ordering:** the tester ran before a branch existed. Fixed: the orchestrator creates the task branch first. Tester and builder commit with `FEOS-Agent` trailers.
5. **No path to resume after human decisions.** Fixed: `feos_state.py resolve` was added, and the orchestrator protocol re-records the gate using the human's stated name.
6. `${ARGUMENTS:-default}` is not supported substitution in skills. Fixed.
7. Gate `record` logic for pending checks was convoluted. Rewritten: missing machine/agent evidence = fail, and only human checks may be pending.

## Known limitations / residual risks (be aware)
| # | Limitation | Mitigation in kit | Your action |
|---|---|---|---|
| L1 | Workflows and agent write-scopes are followed by LLMs, not enforced by a runtime. | Hook (protected paths), CI guard, gate scripts, branch protection | Treat CI and human PR review as the real control |
| L2 | Reviewer scores are LLM judgement. | Evidence-or-zero rule, deterministic caps, hard checks dominate | Calibrate on 5–10 real PRs before trusting thresholds |
| L3 | The Claude hook covers Edit/Write/MultiEdit, not shell writes (e.g. `sed -i`). Copilot has no hook equivalent. | `feos_guard.py` in CI catches committed changes | Keep `feos-validate` a required check |
| L4 | The Copilot prompt-file key `agent:` and tool aliases (`read`, `edit`, `search`, `execute`, `web`, `agent`, `todo`) were not exercised here. | — | Verify in your VS Code/Copilot version (Claude Code handoff prompt includes this) |
| L5 | `feos_trace.py` parses the template formats (FR headings + `**Traces:**`, NFR tables). | Templates enforce the format | Don't restructure the PRD/NFR tables |
| L6 | The G3 coverage check depends on project tooling output. | Declared in `project.md` | Configure the coverage reporter per stack |
| L7 | AI thresholds and the AU-Government domain layer are **placeholders/examples**. | `ai-eval` refuses to pass until `approved_by` is set | Human RAI/domain owners confirm |
| L8 | `feos-release.yml` deploy steps are TODO stubs. | Approval-file check + environments are real | Implement per project IaC |
| L9 | Actions are referenced by tag for readability. | Comment in workflow | Pin to SHAs |
