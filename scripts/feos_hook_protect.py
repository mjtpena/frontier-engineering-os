#!/usr/bin/env python3
"""Claude Code PreToolUse hook: block agent edits to FEOS-protected paths.
Reads the hook JSON from stdin; exit code 2 blocks the tool call and shows stderr to Claude.
A human deliberately changing the framework sets FEOS_FRAMEWORK_EDIT=1 for that session."""
import fnmatch, json, os, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from feos_guard import PROTECTED

def main():
    if os.environ.get("FEOS_FRAMEWORK_EDIT") == "1":
        return 0
    try:
        data = json.load(sys.stdin)
    except Exception:
        return 0
    fp = (data.get("tool_input") or {}).get("file_path") or ""
    root = Path(data.get("cwd") or os.getcwd()).resolve()
    try:
        rel = Path(fp).resolve().relative_to(root).as_posix()
    except Exception:
        rel = fp
    if any(fnmatch.fnmatch(rel, g) for g in PROTECTED):
        print(f"FEOS: '{rel}' is protected (constitution Art. 8.2). Ask the human; framework changes need a human-approved PR.", file=sys.stderr)
        return 2
    return 0

if __name__ == "__main__":
    sys.exit(main())
