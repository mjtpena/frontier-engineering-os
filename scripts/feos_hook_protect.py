#!/usr/bin/env python3
"""Claude Code PreToolUse hook: block agent edits to FEOS-protected paths.
Reads the hook JSON from stdin; exit code 2 blocks the tool call and shows stderr to Claude.
A human deliberately changing the framework sets FEOS_FRAMEWORK_EDIT=1 for that session.
The decision ledger (.feos/, gate records in evidence/gates/, the human fields of approval.md) stays blocked even then:
scripts write it (feos_state.py, feos_gate.py) and humans record decisions, never an agent's file tools.
Paths are resolved against the repository root (this script's parent's parent), not the session cwd,
so a session started in a subdirectory is still protected. Unreadable input fails closed.
Uses the standard library only: if it cannot run, the settings.json wrapper blocks the edit."""
import fnmatch, json, os, re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from feos_guard import PROTECTED

ROOT = Path(__file__).resolve().parent.parent
TS = "[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]T[0-9][0-9][0-9][0-9][0-9][0-9]Z"
# Gate records and their command logs (feos_gate.py record); the orchestrator's own inputs there (G1-review.md, claims) stay writable.
LEDGER = [".feos/*", f"evidence/gates/G?-*-{TS}*"]
APPROVAL = "evidence/release/*/approval.md"
HUMAN_FIELD = re.compile(r"^(decision|approver)\s*:\s*['\"]?([^'\"#\r\n]*)", re.M)

def fills_human_fields(text: str) -> bool:
    """True if approval.md front-matter records a decision or an approver (HUMAN ONLY in the template)."""
    m = re.match(r"^---\s*\n(.*?)\n---", text, re.S)
    fields = {k: v.strip() for k, v in HUMAN_FIELD.findall(m.group(1))} if m else {}
    approver = fields.get("approver", "")
    return fields.get("decision", "pending") not in ("pending", "") or bool(approver and not approver.upper().startswith("TBD"))

def resulting_text(p: Path, tool: str, ti: dict) -> str:
    if tool == "Write": return ti.get("content", "")
    text = p.read_text(encoding="utf-8")
    for e in ti.get("edits") or [ti]:   # MultiEdit carries a list; Edit is a single edit
        old, new = e.get("old_string", ""), e.get("new_string", "")
        text = text.replace(old, new) if e.get("replace_all") else text.replace(old, new, 1)
    return text

def block(msg):
    print(msg, file=sys.stderr); return 2

def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        return block("FEOS: hook input unreadable; blocking edit (fail closed).")
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
    if any(fnmatch.fnmatch(rel, g) for g in LEDGER):
        return block(f"FEOS: '{rel}' is the decision ledger; only scripts/feos_state.py and scripts/feos_gate.py write it "
                     "(constitution Art. 1, 6). Ask the human to record decisions.")
    if fnmatch.fnmatch(rel, APPROVAL):
        try:
            filled = fills_human_fields(resulting_text(p, data.get("tool_name", ""), ti))
        except Exception:
            return block(f"FEOS: cannot check '{rel}' for human-only fields; blocking edit (fail closed).")
        if filled:
            return block(f"FEOS: '{rel}': 'decision' and 'approver' are HUMAN ONLY (constitution Art. 1.1). Leave decision: pending.")
    if os.environ.get("FEOS_FRAMEWORK_EDIT") == "1":
        return 0
    if any(fnmatch.fnmatch(rel, g) for g in PROTECTED):
        return block(f"FEOS: '{rel}' is protected (constitution Art. 8.2). Ask the human; framework changes need a human-approved PR.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
