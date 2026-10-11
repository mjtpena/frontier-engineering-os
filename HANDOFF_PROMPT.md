# Claude Code handoff prompt — install and prove FEOS

> Paste everything below the line into Claude Code, opened at the root of the target repository, with `feos-kit.zip` placed in that root.

---

You are installing and proving the **Frontier Engineering Operating System (FEOS) v1.0** kit in this repository. The kit is in `./feos-kit.zip`. Your job is to make it **operational and proven**, not to redesign it.

## Ground rules
- Unzip and read first: `README.md`, `JUDGEMENT.md`, `feos/constitution.md`, `feos/lifecycle.md`, `feos/agents/orchestrator.md`. The constitution is binding on you from the moment it is installed.
- **Do not weaken anything** to make checks pass: no edits that relax gates, rubrics, schemas, tests, the guard, the hook, or the constitution. If you believe something in `feos/` is wrong, write it up as a proposed change (Phase 5). Do not silently change it.
- Do not invent values. Every `TBD` (owners, commands, roles, platforms) → collect into one question list for me.
- Never push to `main`, never deploy, never record a human decision on my behalf.
- Evidence or it didn't happen: for every claim, show the command and exit code.

## Phase 1 — Install (branch `chore/feos-install`)
1. `unzip feos-kit.zip -d /tmp/feos-kit` and inventory it. Merge it into the repo root **without clobbering existing files**: if `CLAUDE.md`, `AGENTS.md`, `.github/copilot-instructions.md`, `.github/CODEOWNERS`, `.github/pull_request_template.md`, `.gitignore` or `.claude/settings.json` already exist, merge the content and show me the diff for each.
2. `pip install -r scripts/requirements.txt pytest`.
3. Run and paste the results: `python scripts/feos_validate.py`, `python scripts/feos_render.py --check`, `pytest -q feos-tests`. All must pass. If anything fails, diagnose the root cause and report it before changing anything.

## Phase 2 — Verify the integration with the real tools (don't trust the kit's assumptions)
1. Fetch the current official docs for Claude Code subagents, skills, hooks and settings permissions, and for GitHub Copilot custom agents, `.instructions.md` and `.prompt.md` files. Compare them with the kit's front-matter and file locations (`.claude/agents`, `.claude/skills/*/SKILL.md`, `.claude/settings.json` hooks/permissions, `.github/agents/*.agent.md`, `.github/instructions`, `.github/prompts`). Pay particular attention to `JUDGEMENT.md` L4: the prompt-file `agent:` key and the Copilot tool aliases. Report each mismatch with a doc link.
2. Prove the Claude side in this session:
   - (a) The 9 `feos-*` subagents load. (Claude Code 2.1.x removed the `/agents` list; check the agents in a new session's init output, e.g. `claude -p --output-format stream-json --verbose`, or invoke one.)
   - (b) The `/feos-*` skills are available.
   - (c) Attempt an Edit to `feos/constitution.md` **without** `FEOS_FRAMEWORK_EDIT=1` and confirm the hook blocks it, then revert any change.
   - (d) Confirm the permission deny rules load.
3. Fix only adapter-level format issues (`scripts/feos_render.py`, skill/prompt front-matter), then re-run Phase 1 step 3.

## Phase 3 — Dry run on the sample project (branch `chore/feos-dryrun`, throwaway)
Use `feos-tests/fixtures/sample` as the project content (copy `specs/`, `architecture/`, `plan/`, `tests/` into a scratch folder or a throwaway branch). Then:
1. `/feos-init v0.0.1-dryrun`.
2. Run G1 via `/feos-gate G1 specs`. Show the reviewer report, the computed score, and the gate record JSON. It must end `pending_human`.
3. I will reply with an approval. Resolve it via `feos_state.py resolve`, re-record the gate, and show `/feos-status`.
4. Run one task end-to-end with `/feos-task TK-002`, using a trivial Python implementation:
   - The tester commits red tests (evidence `tests-red.txt`).
   - The builder makes them green.
   - The reviewer scores the work.
   - Run `feos_guard.py --base main`, then record G3. It must end `pending_human`; do not merge.
5. Negative test: as the builder, modify one of the tester's tests in a commit with the `FEOS-Agent: builder` trailer, and show that `feos_guard.py` fails. Then reset that commit.
6. Delete the dry-run branch afterwards unless I say otherwise.

## Phase 4 — Configure for real
Give me one consolidated question list covering:
- every `TBD` in `feos.config.yaml`, `raci.yaml`, `CODEOWNERS` and `project.md`
- which platform layers apply
- which domain layer applies

Also give me a checklist of the GitHub settings that I must apply manually:
- branch protection and required checks
- the `production` environment with its reviewers
- secret scanning and push protection
- Dependabot and code scanning
- Actions pinned to SHAs

Do not proceed past this point until I answer.

## Phase 5 — Report
Open a PR from `chore/feos-install` containing only the installation plus any adapter-format fixes. The PR description must include:
- **Proof:** every command you ran with its exit code.
- **Doc mismatches:** each one found in Phase 2, with links.
- **Dry-run transcript:** a summary of Phase 3.
- **Proposed framework changes:** each with rationale, risk, and the exact diff. These are not applied; they are for my approval.
- **Open questions:** the Phase 4 list.

Finish with the FEOS status report block.
