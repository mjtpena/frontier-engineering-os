#!/usr/bin/env python3
"""FEOS run state (.feos/state.json).

  python scripts/feos_state.py init [--release v0.1.0]
  python scripts/feos_state.py show
  python scripts/feos_state.py stage S3
  python scripts/feos_state.py task TK-001|none
  python scripts/feos_state.py rework <scope>       # exit 3 when max_rework_loops reached → escalate
  python scripts/feos_state.py escalate --decision approve_architecture_G2 --scope architecture --summary "..."
  python scripts/feos_state.py resolve --decision approve_architecture_G2 --scope architecture --by "<human>" --outcome approved
"""
from __future__ import annotations
import argparse, json, sys
from datetime import datetime, timezone
from jsonschema import Draft202012Validator
from feos_common import ROOT, load_json, config

P = ROOT / ".feos/state.json"
now = lambda: datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def load():
    if not P.exists(): raise SystemExit("FAIL  .feos/state.json missing — run: python scripts/feos_state.py init")
    return json.loads(P.read_text())

def save(s):
    Draft202012Validator(load_json("feos/schemas/state.schema.json")).validate(s)
    P.parent.mkdir(exist_ok=True); P.write_text(json.dumps(s, indent=2))

def event(s, ev, **kw): s["history"].append({"at": now(), "event": ev, **kw})

def record_gate(key, result, evidence):
    s = load(); s["gates"][key] = {"result": result, "evidence": evidence, "at": now()}
    event(s, "gate", gate=key, result=result); save(s)

def main():
    ap = argparse.ArgumentParser(); sub = ap.add_subparsers(dest="cmd", required=True)
    i = sub.add_parser("init"); i.add_argument("--release", default="v0.1.0"); i.add_argument("--force", action="store_true")
    sub.add_parser("show")
    st = sub.add_parser("stage"); st.add_argument("stage")
    tk = sub.add_parser("task"); tk.add_argument("task")
    rw = sub.add_parser("rework"); rw.add_argument("scope")
    es = sub.add_parser("escalate"); es.add_argument("--decision", required=True); es.add_argument("--summary", required=True)
    es.add_argument("--scope")
    rs = sub.add_parser("resolve"); rs.add_argument("--decision", required=True); rs.add_argument("--by", required=True)
    rs.add_argument("--scope")
    rs.add_argument("--outcome", choices=["approved", "rejected"], required=True)
    a = ap.parse_args()

    if a.cmd == "init":
        if P.exists() and not a.force: print("state exists (use --force to reset)"); return 0
        s = {"feos_version": config()["feos_version"], "stage": "S0", "release": a.release, "current_task": None,
             "gates": {}, "rework": {}, "escalations": [], "history": []}
        event(s, "init"); save(s); print("initialised .feos/state.json"); return 0
    s = load()
    if a.cmd == "show":
        open_esc = [e for e in s["escalations"] if e.get("status") == "open"]
        print(json.dumps({"stage": s["stage"], "release": s.get("release"), "current_task": s.get("current_task"),
                          "gates": s["gates"], "rework": s["rework"], "waiting_on_human": open_esc}, indent=2)); return 0
    if a.cmd == "stage":
        prev = s["stage"]; s["stage"] = a.stage; event(s, "stage", frm=prev, to=a.stage)
    elif a.cmd == "task":
        s["current_task"] = None if a.task == "none" else a.task; event(s, "task", task=a.task)
    elif a.cmd == "rework":
        cap = config()["orchestration"]["max_rework_loops"]
        n = s["rework"].get(a.scope, 0) + 1; s["rework"][a.scope] = n; event(s, "rework", scope=a.scope, n=n)
        save(s)
        if n >= cap:
            print(f"ESCALATE: rework cap {cap} reached for {a.scope}"); return 3
        print(f"rework {a.scope}: {n}/{cap}"); return 0
    elif a.cmd == "escalate":
        s["escalations"].append({"decision": a.decision, "scope": a.scope, "summary": a.summary, "status": "open", "at": now()})
        event(s, "escalate", decision=a.decision)
    elif a.cmd == "resolve":
        hits = [e for e in s["escalations"] if e["decision"] == a.decision and e["status"] == "open"
                and (a.scope is None or e.get("scope") == a.scope)]
        if not hits:
            print(f"FAIL  no open escalation for decision {a.decision}" + (f" scope {a.scope}" if a.scope else "")); return 1
        for e in hits:
            e.update(status=a.outcome, by=a.by, resolved_at=now())
        event(s, "resolve", decision=a.decision, by=a.by, outcome=a.outcome)
    save(s); print("ok"); return 0

if __name__ == "__main__":
    sys.exit(main())
