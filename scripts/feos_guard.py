#!/usr/bin/env python3
"""Separation-of-duties guard (G3.6). Inspects commits on the current branch since --base.

Rules (only for commits carrying a 'FEOS-Agent: <id>' trailer — human commits are governed by CODEOWNERS):
  1. No agent commit may touch protected paths (framework, CI, config, linter settings).
  2. Builder commits may not modify or delete test files that existed at the merge base
     or that were added on this branch by a tester commit (tests are owned by the tester role).
Usage: python scripts/feos_guard.py --base origin/main
"""
from __future__ import annotations
import argparse, fnmatch, subprocess, sys

PROTECTED = ["feos/*", "feos.config.yaml", ".github/workflows/*", ".github/CODEOWNERS", "CLAUDE.md", "AGENTS.md",
             ".claude/settings.json", "scripts/feos_*", ".eslintrc*", "eslint.config.*", ".editorconfig",
             "pyproject.toml", "setup.cfg", ".flake8", "ruff.toml", ".ruff.toml", "*.ruleset", ".github/copilot-instructions.md"]
TEST_GLOBS = ["tests/*", "test/*", "*/tests/*", "*.test.*", "*.spec.*", "*_test.*", "test_*.py", "*/test_*.py"]

def git(*args):
    return subprocess.run(["git", *args], check=True, capture_output=True, text=True).stdout

def match(path, globs): return any(fnmatch.fnmatch(path, g) for g in globs)

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--base", default="origin/main")
    a = ap.parse_args()
    base = git("merge-base", a.base, "HEAD").strip()
    errors = []
    tester_files: set[str] = set()
    for sha in reversed(git("rev-list", f"{base}..HEAD").split()):   # oldest first
        trailers = git("log", "-1", "--format=%(trailers:key=FEOS-Agent,valueonly)", sha).strip().lower()
        if not trailers: continue
        agent = trailers.splitlines()[0].strip()
        for line in git("show", "--name-status", "--format=", sha).splitlines():
            parts = line.split("\t"); status, path = parts[0], parts[-1]
            old_path = parts[1] if status[0] == "R" else path
            if match(path, PROTECTED): errors.append(f"{sha[:8]} ({agent}) touched protected path {path}")
            if agent == "tester" and match(path, TEST_GLOBS): tester_files.add(path)
            if agent == "builder" and match(old_path, TEST_GLOBS) and status[0] in "MDR":
                at_base = subprocess.run(["git", "cat-file", "-e", f"{base}:{old_path}"], capture_output=True).returncode == 0
                if at_base or old_path in tester_files:
                    errors.append(f"{sha[:8]} (builder) modified/deleted tester-owned or existing test {old_path}")
    for e in errors: print(f"FAIL  {e}")
    print(f"[feos_guard] {'PASS' if not errors else 'FAIL'}: {len(errors)} violations")
    return 1 if errors else 0

if __name__ == "__main__":
    sys.exit(main())
