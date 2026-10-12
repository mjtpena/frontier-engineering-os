# Security policy

## Supported versions

FEOS has no tagged releases yet. Security fixes land on `main`; use the latest commit on `main`.

## Reporting a vulnerability

**Do not open a public issue, discussion or pull request for a suspected vulnerability.**

Report it privately through GitHub's private vulnerability reporting:
<https://github.com/mjtpena/frontier-engineering-os/security/advisories/new>

Please include:
- the affected file(s) or script(s) and commit SHA,
- steps to reproduce, or a proof of concept,
- the impact you expect (for example, a gate that can be bypassed, a guard or hook that can be evaded, or prompt injection that changes agent behaviour).

## What to expect

This is a volunteer-maintained project. Reports are handled on a best-effort basis, with no guaranteed response or fix times.
The maintainer will acknowledge the report, agree a disclosure timeline with you, and credit you in the advisory unless you prefer otherwise.

## In scope

The enforcement layer is the security boundary of FEOS, so the following are especially relevant:
- `scripts/feos_guard.py`: separation-of-duties bypasses
- `scripts/feos_hook_protect.py`: protected-path edits that get past the hook
- `scripts/feos_gate.py`: gates that can be recorded as passed without the required evidence or human decision
- `.github/workflows/`: injection or privilege escalation in CI
- agent prompts under `feos/agents/` that can be steered by untrusted content (issues, web pages, documents)

Known design limitations are listed in [JUDGEMENT.md](JUDGEMENT.md). For example, the Claude hook does not cover shell writes. Please report a limitation only if you can show impact beyond what is documented there.
