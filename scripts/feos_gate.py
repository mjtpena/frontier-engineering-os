#!/usr/bin/env python3
"""FEOS gate scoring and recording.

  python scripts/feos_gate.py score  <review.md> [--profile implementation] [--signals tests_failed,secret_in_diff]
  python scripts/feos_gate.py ai-eval <ai-eval.json>
  python scripts/feos_gate.py record --gate G3 --scope TK-001 --checks claims.json [--review review.md] [--signals ...]

'record' does not take the caller's word for anything it can check itself:
  - deterministic checks whose cmd is 'python scripts/...' or 'project.<key>' (the command block of
    feos/instructions/30-project/project.md) run here; the exit code decides, output goes to evidence/gates/<record>/;
  - human checks come from the escalations in .feos/state.json (feos_state.py resolve), never from the claims file;
  - a scored gate (quality rubric: G1-G3) is scored here from the reviewer's report (--review).
What it cannot check (agent judgements; checks run by CI or external scanners) comes from the claims file,
is labelled verified_by: caller, and a 'pass' without evidence fails.
Hard constraints always win: the gate fails if any hard check is not 'pass'
(checks with status 'skipped_not_applicable' are allowed only for checks that declare 'when').
"""
from __future__ import annotations
import argparse, json, re, shlex, subprocess, sys
from datetime import datetime, timezone
from pathlib import Path
import yaml
from jsonschema import Draft202012Validator
from feos_common import ROOT, load_yaml, load_json, config

def extract_scores(md: Path) -> dict:
    text = md.read_text(encoding="utf-8")
    for block in re.findall(r"```ya?ml\s*\n(.*?)```", text, re.S):
        data = yaml.safe_load(block)
        if isinstance(data, dict) and "scores" in data:
            return data
    raise SystemExit(f"FAIL  no ```yaml scores:``` block in {md}")

def compute(scores: dict, profile: str, signals: set[str]):
    rubric = load_yaml("feos/orchestration/evaluations/quality.yaml")
    dims = rubric["dimensions"]
    use = rubric["profiles"][profile]["use"]
    use = list(dims) if use == "all" else use
    missing = [d for d in use if d not in scores]
    if missing: raise SystemExit(f"FAIL  reviewer did not score: {missing}")
    total_w = sum(dims[d]["weight"] for d in use)
    floor = config()["quality"]["dimension_floor"]
    detail, total, floor_breaches = {}, 0.0, []
    for d in use:
        s = scores[d]["score"]
        if not scores[d].get("evidence") and not scores[d].get("na"):
            s = 0  # Reviewer constitution: no evidence → 0
        for cap in dims[d].get("caps", []):
            if cap["if"] in signals: s = min(s, cap["max"])
        pct = s / 4 * 100
        if pct < floor: floor_breaches.append(f"{d}={pct:.0f}%")
        w = dims[d]["weight"] / total_w * 100
        total += w * s / 4
        detail[d] = {"score": s, "weight_normalised": round(w, 2)}
    return round(total, 2), detail, floor_breaches

def cmd_score(a):
    data = extract_scores(Path(a.review))
    Draft202012Validator(load_json("feos/schemas/review-scores.schema.json")).validate(data)
    signals = set(filter(None, (a.signals or "").split(",")))
    total, detail, breaches = compute(data["scores"], a.profile, signals)
    thr = config()["quality"]["release_threshold"]
    hard = data.get("hard_constraints", {})
    failed_hard = [k for k, v in hard.items() if v is False]
    ok = total >= thr and not breaches and not failed_hard
    print(json.dumps({"score": total, "threshold": thr, "dimensions": detail, "floor_breaches": breaches,
                      "failed_hard_constraints": failed_hard, "result": "pass" if ok else "fail"}, indent=2))
    return 0 if ok else 1

def cmd_ai_eval(a):
    res = json.loads(Path(a.file).read_text())
    Draft202012Validator(load_json("feos/schemas/ai-eval-result.schema.json")).validate(res)
    spec = load_yaml("feos/orchestration/evaluations/ai-quality.yaml")
    fails = []
    if str(spec.get("approved_by", "TBD")).startswith("TBD"):
        fails.append("ai-quality.yaml thresholds not approved by RAI owner (approved_by is TBD)")
    if res["cases"] < spec["min_eval_cases"]: fails.append(f"cases {res['cases']} < {spec['min_eval_cases']}")
    def check(metrics, label):
        for name, m in spec["metrics"].items():
            if name not in metrics: fails.append(f"{label}: metric {name} missing"); continue
            op, val = re.match(r"(>=|<=)\s*([\d.]+)", m["threshold"]).groups()
            v = metrics[name]
            if (op == ">=" and v < float(val)) or (op == "<=" and v > float(val)):
                fails.append(f"{label}: {name}={v} violates {m['threshold']}")
    check(res["metrics"], "overall")
    for sl in spec.get("slices", []):
        if sl not in res.get("slices", {}): fails.append(f"slice {sl} missing")
        else: check(res["slices"][sl], f"slice {sl}")
    for f in fails: print(f"FAIL  {f}")
    print(f"[ai-eval] {'PASS' if not fails else 'FAIL'}")
    return 1 if fails else 0

SCOPE = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]*")   # substituted into commands and paths
QUALITY = "feos/orchestration/evaluations/quality.yaml"

def project_commands() -> dict:
    """The command block of the human-owned L4 project.md."""
    text = (ROOT / "feos/instructions/30-project/project.md").read_text(encoding="utf-8")
    for block in re.findall(r"```ya?ml\s*\n(.*?)```", text, re.S):
        data = yaml.safe_load(block)
        if isinstance(data, dict) and "build" in data: return data
    return {}

def resolve_cmd(cmd: str, scope: str):
    """(command, None) to run here; ('', None) if project.md declares it 'none'; (None, reason) if it is not
    configured; (None, None) if it is checked elsewhere (CI, external scanner)."""
    m = re.fullmatch(r"project\.(\w+)", cmd.strip())
    if m:
        val = str(project_commands().get(m.group(1)) or "TBD").strip()
        if val.startswith("TBD"): return None, f"project.md command '{m.group(1)}' is not configured: {val}"
        if val == "none": return "", None
        cmd = val
    elif cmd.startswith("python scripts/"):
        cmd = shlex.quote(sys.executable) + cmd[len("python"):]   # the interpreter running FEOS, not whatever is on PATH
    else:
        return None, None
    for k, v in {"{task}": scope, "{version}": scope, "{min_coverage}": str(config()["quality"]["min_coverage"])}.items():
        cmd = cmd.replace(k, v)
    return cmd, None

def run_check(cid: str, cmd: str, logdir: Path):
    if cmd == "": return "pass", ["project.md declares this command 'none'"]
    r = subprocess.run(cmd, shell=True, cwd=ROOT, capture_output=True, text=True)
    logdir.mkdir(parents=True, exist_ok=True)
    log = logdir / f"{cid}.txt"
    log.write_text(f"$ {cmd}\n{r.stdout}{r.stderr}\nexit {r.returncode}\n", encoding="utf-8")
    return ("pass" if r.returncode == 0 else "fail"), [f"cmd: {cmd} -> exit {r.returncode}", str(log.relative_to(ROOT))]

def human_status(state: dict, decision: str, scope: str):
    hits = [e for e in state.get("escalations", []) if e.get("decision") == decision and e.get("scope") == scope]
    if not hits: return "pending", [f"no escalation {decision} for scope {scope} in .feos/state.json"]
    e = hits[-1]
    st = {"approved": "pass", "rejected": "fail"}.get(e.get("status"), "pending")
    return st, [f"{decision}: {e.get('status')}" + (f" by {e['by']} at {e.get('resolved_at')}" if e.get("by") else "")]

def review_score(gate: dict, review: str | None, signals: set[str]):
    """(score, failures) for a gate scored with the quality rubric; (None, []) for unscored gates."""
    sc = gate.get("scoring") or {}
    if sc.get("rubric") != QUALITY: return None, []
    if not review: return None, ["scored gate: pass the reviewer's report with --review"]
    data = extract_scores(Path(review))
    Draft202012Validator(load_json("feos/schemas/review-scores.schema.json")).validate(data)
    total, _, breaches = compute(data["scores"], sc.get("profile", "implementation"), signals)
    fails = [f"dimension below floor: {b}" for b in breaches]
    fails += [f"reviewer hard constraint failed: {k}" for k, v in (data.get("hard_constraints") or {}).items() if v is False]
    thr = config()["quality"]["release_threshold"]
    if total < thr: fails.append(f"score {total} < threshold {thr}")
    return total, fails

def cmd_record(a):
    if not SCOPE.fullmatch(a.scope): raise SystemExit(f"FAIL  scope must match {SCOPE.pattern}, got {a.scope!r}")
    gate_file = next((ROOT / "feos/orchestration/gates").glob(f"{a.gate}-*.yaml"), None)
    if gate_file is None: raise SystemExit(f"FAIL  unknown gate {a.gate}")
    gate = yaml.safe_load(gate_file.read_text())
    claims = {c["id"]: c for c in json.loads(Path(a.checks).read_text())} if a.checks else {}
    import feos_state
    state = feos_state.load()
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    name = f"{a.gate}-{a.scope}-{ts.replace(':', '')}"
    failed, pending, out_checks = [], [], []
    for c in gate["checks"]:
        got = claims.get(c["id"], {})
        st, ev, by = got.get("status", "pending"), list(got.get("evidence", [])), "caller"
        if st == "skipped_not_applicable" and "when" in c:
            pass   # the condition (e.g. uses_ai) is declared by the caller
        elif c["type"] == "human":
            (st, ev), by = human_status(state, c.get("decision"), a.scope), "escalation"
        elif c["type"] == "deterministic":
            cmd, why = resolve_cmd(c.get("cmd", ""), a.scope)
            if why: st, ev, by = "fail", [why], "record"
            elif cmd is not None: (st, ev), by = run_check(c["id"], cmd, ROOT / "evidence/gates" / name), "record"
        if by == "caller" and st == "pass" and not ev:
            st = "fail"; ev = ["claimed pass without evidence"]
        if st == "skipped_not_applicable" and "when" not in c:
            st = "fail"; ev.append("skipped but check is unconditional")
        if st == "pending" and c["type"] != "human":
            st = "fail"; ev.append("no result for this check")   # missing machine/agent evidence = fail
        out_checks.append({"id": c["id"], "type": c["type"], "hard": c["hard"], "status": st, "verified_by": by, "evidence": ev})
        if c["hard"] and st == "fail": failed.append(c["id"])
        if c["hard"] and st == "pending": pending.append(c["id"])
    signals = set(filter(None, (a.signals or "").split(",")))
    score, score_fails = review_score(gate, a.review, signals)
    thr = config()["quality"]["release_threshold"] if (gate.get("scoring") or {}).get("rubric") == QUALITY else None
    if failed or score_fails: result = "fail"
    elif pending: result = "pending_human"
    else: result = "pass"
    rec = {"gate": a.gate, "scope": a.scope, "timestamp": ts, "result": result, "score": score, "threshold": thr,
           "review": a.review, "score_failures": score_fails, "checks": out_checks, "failed_hard_checks": failed,
           "route_to": gate["on_fail"]["route_to"] if result == "fail" else None}
    Draft202012Validator(load_json("feos/schemas/gate-result.schema.json")).validate(rec)
    out = ROOT / "evidence/gates" / f"{name}.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(rec, indent=2))
    feos_state.record_gate(f"{a.gate}:{a.scope}", result, str(out.relative_to(ROOT)))
    print(json.dumps({"result": result, "score": score, "failed_hard_checks": failed, "score_failures": score_fails,
                      "pending": pending, "evidence": str(out.relative_to(ROOT))}, indent=2))
    return 0 if result == "pass" else (2 if result == "pending_human" else 1)

def main():
    ap = argparse.ArgumentParser(); sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("score"); s.add_argument("review"); s.add_argument("--profile", default="implementation"); s.add_argument("--signals")
    e = sub.add_parser("ai-eval"); e.add_argument("file")
    r = sub.add_parser("record"); r.add_argument("--gate", required=True); r.add_argument("--scope", required=True)
    r.add_argument("--checks", help="claims JSON: results of agent checks and of checks run by CI/external scanners")
    r.add_argument("--review", help="reviewer report with the ```yaml scores:``` block (required for G1-G3)")
    r.add_argument("--signals", help="deterministic caps, e.g. tests_failed,secret_in_diff")
    a = ap.parse_args()
    return {"score": cmd_score, "ai-eval": cmd_ai_eval, "record": cmd_record}[a.cmd](a)

if __name__ == "__main__":
    sys.exit(main())
