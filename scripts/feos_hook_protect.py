#!/usr/bin/env python3
"""Claude Code PreToolUse hook: block agent edits to FEOS-protected paths.
Reads the hook JSON from stdin; exit code 2 blocks the tool call and shows stderr to Claude.
A human deliberately changing the framework sets FEOS_FRAMEWORK_EDIT=1 for that session.
Paths are resolved against the repository root (this script's parent's parent), not the session cwd,
so a session started in a subdirectory is still protected. Unreadable input fails closed."""
import fnmatch, json, os, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from feos_guard import PROTECTED

ROOT = Path(__file__).resolve().parent.parent

def main():
    if os.environ.get("FEOS_FRAMEWORK_EDIT") == "1":
        return 0
    try:
        data = json.load(sys.stdin)
    except Exception:
        print("FEOS: hook input unreadable; blocking edit (fail closed).", file=sys.stderr)
        return 2
    ti = data.get("tool_input") or {}
    fp = ti.get("file_path") or ti.get("notebook_path") or ""
    if not fp:
        return 0
    p = Path(fp)
    if not p.is_absolute():
        p = Path(data.get("cwd") or os.getcwd()) / p
    try:
        rel = p.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return 0  # outside the repository
    if any(fnmatch.fnmatch(rel, g) for g in PROTECTED):
        print(f"FEOS: '{rel}' is protected (constitution Art. 8.2). Ask the human; framework changes need a human-approved PR.", file=sys.stderr)
        return 2
    return 0

if __name__ == "__main__":
    sys.exit(main())
