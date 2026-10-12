#!/usr/bin/env python3
"""Separation-of-duties guard (G3.6). Inspects commits on the current branch since --base.

Rules (role rules apply to commits carrying a 'FEOS-Agent: <id>' line — human commits are governed by CODEOWNERS):
  1. No agent commit may touch protected paths (framework, CI, config, linter settings).
  2. Builder commits may not modify or delete test files that existed at the merge base
     or that were added on this branch by a tester commit (tests are owned by the tester role).
  3. Builder commits may not add, change or delete test-runner configuration (conftest.py, pytest.ini,
     jest/vitest config, test scripts in package.json, ...): it decides which tests run. Set it up via the tester or a human.
  4. The id must be a known agent (agents.manifest.yaml) or 'human'.
  5. On task branches (feat/TK-*), every non-merge commit must carry the line: agents their role id,
     humans 'FEOS-Agent: human'. A missing line would otherwise exempt the commit from rules 1-3.
Usage: python scripts/feos_guard.py --base origin/main [--branch feat/TK-001-x]
"""
from __future__ import annotations
import argparse, fnmatch, json, os, re, subprocess, sys
from pathlib import PurePosixPath

PROTECTED = ["feos/*", "feos.config.yaml", ".github/workflows/*", ".github/CODEOWNERS", "CLAUDE.md", "AGENTS.md",
             ".claude/settings.json", "scripts/feos_*", ".eslintrc*", "eslint.config.*", ".editorconfig",
             "pyproject.toml", "setup.cfg", ".flake8", "ruff.toml", ".ruff.toml", "*.ruleset", ".github/copilot-instructions.md",
             ".claude/*", ".github/*", "feos-tests/*", "scripts/requirements.txt"]
# Any line "FEOS-Agent: <id>" in the message counts, not only git's final trailer block
# (a later Co-Authored-By paragraph must not hide the agent identity from the guard).
AGENT_RE = re.compile(r"^FEOS-Agent:\s*(\S+)", re.I | re.M)
TEST_GLOBS = ["tests/*", "test/*", "*/tests/*", "*.test.*", "*.spec.*", "*_test.*", "test_*.py", "*/test_*.py"]
TEST_CONFIG = ["conftest.py", "pytest.ini", "tox.ini", "noxfile.py", ".coveragerc", "jest.config.*", "vitest.config.*",
               "vitest.workspace.*", "karma.conf.*", "playwright.config.*", "cypress.config.*", ".mocharc*", ".nycrc*",
               ".c8rc*", "phpunit.xml*", "*.runsettings"]   # matched against the file name, at any depth
PKG_TEST_SECTIONS = ("jest", "vitest", "mocha", "nyc", "c8", "ava")
TASK_BRANCHES = ["feat/TK-*"]   # created by the orchestrator (delivery.yaml, /feos-task)

def git(*args):
    return subprocess.run(["git", *args], check=True, capture_output=True, text=True).stdout

def match(path, globs): return any(fnmatch.fnmatch(path, g) for g in globs)

def is_test_config(path): return match(PurePosixPath(path).name, TEST_CONFIG)

def pkg_test_config(rev, path):
    """Test scripts and test-runner sections of a package.json at a revision (empty if absent or unparsable)."""
    try: data = json.loads(git("show", f"{rev}:{path}"))
    except (subprocess.CalledProcessError, ValueError): data = {}
    if not isinstance(data, dict): data = {}
    scripts = data.get("scripts") if isinstance(data.get("scripts"), dict) else {}
    return ({k: v for k, v in scripts.items() if re.search(r"test|cov", k, re.I)},
            {k: data.get(k) for k in PKG_TEST_SECTIONS})

def known_agents():
    from feos_common import load_yaml   # lazy: the Claude hook imports PROTECTED from here using the stdlib only
    return {a["id"] for a in load_yaml("feos/orchestration/agents.manifest.yaml")["agents"]} | {"human"}

def current_branch(arg):
    if arg: return arg
    b = git("rev-parse", "--abbrev-ref", "HEAD").strip()
    return b if b != "HEAD" else os.environ.get("GITHUB_HEAD_REF", "")   # CI checks out a detached PR merge commit

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--base", default="origin/main"); ap.add_argument("--branch")
    a = ap.parse_args()
    base = git("merge-base", a.base, "HEAD").strip()
    branch = current_branch(a.branch)
    task_branch = match(branch, TASK_BRANCHES)
    agents = known_agents()
    errors = []
    tester_files: set[str] = set()
    for sha in reversed(git("rev-list", f"{base}..HEAD").split()):   # oldest first
        m = AGENT_RE.search(git("log", "-1", "--format=%B", sha))
        if not m:
            merge = len(git("log", "-1", "--format=%P", sha).split()) > 1
            if task_branch and not merge:
                errors.append(f"{sha[:8]} on task branch {branch} has no 'FEOS-Agent: <id>' line (humans: 'FEOS-Agent: human')")
            continue
        agent = m.group(1).strip().lower()
        if agent not in agents:
            errors.append(f"{sha[:8]} names unknown agent '{agent}' (known: {', '.join(sorted(agents))})"); continue
        if agent == "human": continue
        for line in git("show", "--name-status", "--format=", sha).splitlines():
            parts = line.split("\t"); status, path = parts[0], parts[-1]
            old_path = parts[1] if status[0] == "R" else path
            if match(path, PROTECTED): errors.append(f"{sha[:8]} ({agent}) touched protected path {path}")
            if agent == "tester" and match(path, TEST_GLOBS): tester_files.add(path)
            if agent != "builder": continue
            if match(old_path, TEST_GLOBS) and status[0] in "MDR":
                at_base = subprocess.run(["git", "cat-file", "-e", f"{base}:{old_path}"], capture_output=True).returncode == 0
                if at_base or old_path in tester_files:
                    errors.append(f"{sha[:8]} (builder) modified/deleted tester-owned or existing test {old_path}")
            if is_test_config(path) or is_test_config(old_path):
                errors.append(f"{sha[:8]} (builder) changed test-runner configuration {path}")
            if PurePosixPath(path).name == "package.json" and pkg_test_config(f"{sha}^", old_path) != pkg_test_config(sha, path):
                errors.append(f"{sha[:8]} (builder) changed test scripts or test-runner config in {path}")
    for e in errors: print(f"FAIL  {e}")
    print(f"[feos_guard] {'PASS' if not errors else 'FAIL'}: {len(errors)} violations")
    return 1 if errors else 0

if __name__ == "__main__":
    sys.exit(main())
