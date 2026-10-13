#!/usr/bin/env python3
"""FEOS validator.

  python scripts/feos_validate.py                    # framework self-check (manifests, workflows, gates, schemas, adapters)
  python scripts/feos_validate.py --backlog plan/backlog.yaml
  python scripts/feos_validate.py --artifacts specs  # front-matter on every .md in a folder
  python scripts/feos_validate.py --task-evidence TK-001
"""
from __future__ import annotations
import argparse, re, sys
from pathlib import Path
import yaml
from jsonschema import Draft202012Validator
from feos_common import ROOT, Report, load_yaml, load_json, front_matter, config

SPECIAL_ACTORS = {"orchestrator", "human", "ci"}

def framework(r: Report):
    cfg = config()
    for key in ("feos_version", "platforms", "domain", "quality", "orchestration"):
        (r.passed() if key in cfg else r.err(f"feos.config.yaml missing '{key}'"))
    for p in cfg.get("platforms", []):
        f = ROOT / f"feos/instructions/10-platform/{p}.md"
        r.passed() if f.exists() else r.err(f"platform '{p}' has no instruction file {f.relative_to(ROOT)}")
    d = cfg.get("domain")
    if d and not (ROOT / f"feos/instructions/20-domain/{d}.md").exists():
        r.err(f"domain '{d}' has no instruction file")
    q = cfg.get("quality", {})
    if not (0 < q.get("release_threshold", 0) <= 100): r.err("quality.release_threshold must be 1..100")
    if not (0 < q.get("min_coverage", 0) <= 100): r.err("quality.min_coverage must be 1..100")
    if cfg.get("orchestration", {}).get("max_rework_loops", 0) < 1: r.err("orchestration.max_rework_loops must be >= 1")

    # schemas are valid JSON Schema
    for s in sorted((ROOT / "feos/schemas").glob("*.json")):
        try:
            Draft202012Validator.check_schema(load_json(s.relative_to(ROOT))); r.passed()
        except Exception as e:
            r.err(f"invalid schema {s.name}: {e}")

    # agents manifest
    man = load_yaml("feos/orchestration/agents.manifest.yaml")
    ids = set()
    for a in man["agents"]:
        ids.add(a["id"])
        for key in ("id", "name", "description", "prompt", "copilot", "instruction_layers"):
            if key not in a: r.err(f"agent {a.get('id')} missing '{key}'")
        if not (ROOT / a["prompt"]).exists(): r.err(f"agent {a['id']}: prompt {a['prompt']} missing")
        for layer in a["instruction_layers"]:
            if not (ROOT / layer).exists(): r.err(f"agent {a['id']}: instruction layer {layer} missing")
        for t in a.get("templates", []):
            if not (ROOT / "feos/templates" / t).exists(): r.err(f"agent {a['id']}: template {t} missing")
        if a.get("read_only") and a.get("writes"): r.err(f"agent {a['id']} is read_only but declares writes")
        if a.get("read_only") and a["id"] != "orchestrator":
            tools = a["claude"]["tools"]
            if any(t in tools for t in ("Write", "Edit")): r.err(f"read-only agent {a['id']} has write tools in Claude adapter")
            if "edit" in a["copilot"]["tools"]: r.err(f"read-only agent {a['id']} has edit tool in Copilot adapter")
        r.passed()
    # adapter frontmatter + drift
    from feos_render import render
    for a in man["agents"]:
        for rel, content in render(a).items():
            p = ROOT / rel
            if not p.exists(): r.err(f"adapter missing: {rel}"); continue
            fm, _ = front_matter(p)
            if not fm or not fm.get("description"): r.err(f"adapter {rel}: invalid front-matter")
            if p.read_text(encoding="utf-8") != content: r.err(f"adapter drift: {rel} (run scripts/feos_render.py)")
            else: r.passed()
    actors = ids | SPECIAL_ACTORS

    # raci
    raci = load_yaml("feos/orchestration/raci.yaml")
    decisions = set(raci["decisions"].keys()) | {"declare_incident"}
    for name, d in raci["decisions"].items():
        for agent in d.get("R", []):
            if agent not in actors: r.err(f"raci {name}: unknown agent {agent}")
        if d.get("A") not in raci["roles"]: r.err(f"raci {name}: accountable role {d.get('A')} not in roles")

    # gates
    from feos_gate import project_commands
    project_keys = set(project_commands())
    gate_ids = set()
    for g in sorted((ROOT / "feos/orchestration/gates").glob("*.yaml")):
        gate = yaml.safe_load(g.read_text())
        gate_ids.add(gate["id"])
        has_human = False
        for c in gate["checks"]:
            for key in ("id", "type", "hard", "desc"):
                if key not in c: r.err(f"{g.name} check {c.get('id')}: missing {key}")
            if c["type"] == "agent" and c.get("agent") not in ids: r.err(f"{g.name} {c['id']}: unknown agent {c.get('agent')}")
            if c["type"] == "human":
                has_human = True
                if c.get("decision") not in decisions: r.err(f"{g.name} {c['id']}: unknown decision {c.get('decision')}")
            m = re.search(r"python scripts/(\S+\.py)", c.get("cmd", ""))
            if m and not (ROOT / "scripts" / m.group(1)).exists(): r.err(f"{g.name} {c['id']}: script {m.group(1)} missing")
            m = re.fullmatch(r"project\.(\w+)", c.get("cmd", ""))
            if m and m.group(1) not in project_keys: r.err(f"{g.name} {c['id']}: project.md has no '{m.group(1)}' command")
            r.passed()
        if not has_human: r.err(f"{g.name}: every gate must contain a human check")
        if gate.get("on_fail", {}).get("route_to") not in ids: r.err(f"{g.name}: on_fail.route_to unknown")
        rub = gate.get("scoring", {}).get("rubric")
        if rub and not (ROOT / rub).exists(): r.err(f"{g.name}: rubric {rub} missing")

    # workflows
    for w in sorted((ROOT / "feos/orchestration/workflows").glob("*.yaml")):
        wf = yaml.safe_load(w.read_text())
        steps = wf.get("steps") or wf.get("foreach", {}).get("steps", [])
        if not steps: r.err(f"{w.name}: no steps")
        for s in steps:
            if s["actor"] not in actors: r.err(f"{w.name} step {s['id']}: unknown actor {s['actor']}")
            if "gate" in s and s["gate"] not in gate_ids: r.err(f"{w.name} step {s['id']}: unknown gate {s['gate']}")
            if s["actor"] == "human" and s.get("decision") not in decisions: r.err(f"{w.name} step {s['id']}: unknown decision {s.get('decision')}")
            if "template" in s and not (ROOT / s["template"]).exists(): r.err(f"{w.name}: template {s['template']} missing")
            for c in s.get("commands", []):
                m = re.search(r"python scripts/(\S+\.py)", c)
                if m and not (ROOT / "scripts" / m.group(1)).exists(): r.err(f"{w.name}: script {m.group(1)} missing")
            r.passed()
        for req in wf.get("entry", {}).get("requires_gates", []):
            if req not in gate_ids: r.err(f"{w.name}: requires unknown gate {req}")

    # rubric weights
    q = load_yaml("feos/orchestration/evaluations/quality.yaml")
    total = sum(d["weight"] for d in q["dimensions"].values())
    r.passed() if total == 100 else r.err(f"quality.yaml weights sum to {total}, expected 100")

    # skills
    for sk in sorted((ROOT / ".claude/skills").glob("*/SKILL.md")):
        fm, _ = front_matter(sk)
        if not fm or fm.get("name") != sk.parent.name or not fm.get("description"):
            r.err(f"skill {sk.parent.name}: front-matter name must equal folder and have description")
        else: r.passed()

def backlog(r: Report, path: str):
    data = load_yaml(path)
    v = Draft202012Validator(load_json("feos/schemas/backlog.schema.json"))
    errs = sorted(v.iter_errors(data), key=lambda e: list(e.path))
    for e in errs: r.err(f"schema: {'/'.join(map(str, e.path))}: {e.message}")
    if errs: return
    seen, stories = set(), {}
    for ep in data["epics"]:
        for ft in ep["features"]:
            for st in ft["stories"]:
                if st["id"] in seen: r.err(f"duplicate id {st['id']}")
                seen.add(st["id"]); stories[st["id"]] = st
    tasks = {}
    for t in data["tasks"]:
        if t["id"] in tasks: r.err(f"duplicate task {t['id']}")
        tasks[t["id"]] = t
    for t in tasks.values():
        st = stories.get(t["story"])
        if not st: r.err(f"{t['id']}: unknown story {t['story']}"); continue
        extra = set(t["covers"]) - set(st["covers"])
        if extra: r.err(f"{t['id']}: covers {sorted(extra)} not covered by its story {st['id']}")
        for d in t["depends_on"]:
            if d not in tasks: r.err(f"{t['id']}: depends on unknown {d}")
        if t["type"] == "impl" and not t["covers"]: r.err(f"{t['id']}: impl task must cover >= 1 FR/NFR")
        r.passed()
    # cycle detection
    state = {}
    def visit(n, stack):
        if state.get(n) == 1: r.err(f"dependency cycle: {' -> '.join(stack + [n])}"); return
        if state.get(n) == 2: return
        state[n] = 1
        for d in tasks.get(n, {}).get("depends_on", []): visit(d, stack + [n])
        state[n] = 2
    for n in tasks: visit(n, [])
    for sid in stories:
        if not any(t["story"] == sid for t in tasks.values()): r.warn(f"story {sid} has no tasks")

def artifacts(r: Report, folder: str):
    base = ROOT / folder
    if not base.exists(): r.err(f"{folder}/ does not exist"); return
    v = Draft202012Validator(load_json("feos/schemas/artifact-frontmatter.schema.json"))
    files = sorted(base.rglob("*.md"))
    if not files: r.err(f"no artifacts in {folder}/")
    for f in files:
        fm, _ = front_matter(f)
        if fm is None: r.err(f"{f.relative_to(ROOT)}: missing front-matter"); continue
        for e in v.iter_errors(fm): r.err(f"{f.relative_to(ROOT)}: {e.message}")
        if str(fm.get("owner", "")).startswith("TBD"): r.warn(f"{f.relative_to(ROOT)}: owner is TBD")
        r.passed()

def task_evidence(r: Report, task: str):
    bl = load_yaml("plan/backlog.yaml")
    t = next((t for t in bl["tasks"] if t["id"] == task), None)
    if not t: r.err(f"{task} not in backlog"); return
    d = ROOT / "evidence/tasks" / task
    need = ["build.txt", "summary.md"] + (["tests-red.txt"] if t["type"] == "impl" else [])
    for n in need:
        r.passed() if (d / n).exists() else r.err(f"{task}: missing evidence {d.relative_to(ROOT)}/{n}")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--backlog"); ap.add_argument("--artifacts"); ap.add_argument("--task-evidence")
    a = ap.parse_args()
    r = Report("feos_validate")
    if a.backlog: backlog(r, a.backlog)
    elif a.artifacts: artifacts(r, a.artifacts)
    elif a.task_evidence: task_evidence(r, a.task_evidence)
    else: framework(r)
    return r.finish()

if __name__ == "__main__":
    sys.exit(main())
