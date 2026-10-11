#!/usr/bin/env python3
"""FEOS gate scoring and recording.

  python scripts/feos_gate.py score  <review.md> [--profile implementation] [--signals tests_failed,secret_in_diff]
  python scripts/feos_gate.py ai-eval <ai-eval.json>
  python scripts/feos_gate.py record --gate G3 --scope TK-001 --checks checks.json [--score 91.5]

Hard constraints always win: 'record' fails the gate if any hard check is not 'pass'
(checks with status 'skipped_not_applicable' are allowed only for checks that declare 'when').
"""
from __future__ import annotations
import argparse, json, re, sys
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

def cmd_record(a):
    gate_file = next((ROOT / "feos/orchestration/gates").glob(f"{a.gate}-*.yaml"))
    gate = yaml.safe_load(gate_file.read_text())
    checks = json.loads(Path(a.checks).read_text())
    by_id = {c["id"]: c for c in checks}
    failed, pending = [], []
    out_checks = []
    for c in gate["checks"]:
        got = by_id.get(c["id"], {"status": "pending"})
        st = got["status"]
        if st == "skipped_not_applicable" and "when" not in c:
            st = "fail"; got.setdefault("evidence", []).append("skipped but check is unconditional")
        out_checks.append({"id": c["id"], "type": c["type"], "hard": c["hard"], "status": st, "evidence": got.get("evidence", [])})
        if c["hard"] and st == "fail": failed.append(c["id"])
        if c["hard"] and st == "pending": pending.append(c["id"])
    thr = config()["quality"]["release_threshold"] if a.score is not None else None
    types = {c["id"]: c["type"] for c in gate["checks"]}
    non_human_pending = [p for p in pending if types[p] != "human"]
    failed += non_human_pending          # missing machine/agent evidence = fail
    if failed or (a.score is not None and a.score < thr): result = "fail"
    elif pending: result = "pending_human"
    else: result = "pass"
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    rec = {"gate": a.gate, "scope": a.scope, "timestamp": ts, "result": result, "score": a.score, "threshold": thr,
           "checks": out_checks, "failed_hard_checks": failed,
           "route_to": gate["on_fail"]["route_to"] if result == "fail" else None}
    Draft202012Validator(load_json("feos/schemas/gate-result.schema.json")).validate(rec)
    out = ROOT / "evidence/gates" / f"{a.gate}-{a.scope}-{ts.replace(':', '')}.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(rec, indent=2))
    import feos_state
    feos_state.record_gate(f"{a.gate}:{a.scope}", result, str(out.relative_to(ROOT)))
    print(json.dumps({"result": result, "failed_hard_checks": failed, "pending": pending, "evidence": str(out.relative_to(ROOT))}, indent=2))
    return 0 if result == "pass" else (2 if result == "pending_human" else 1)

def main():
    ap = argparse.ArgumentParser(); sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("score"); s.add_argument("review"); s.add_argument("--profile", default="implementation"); s.add_argument("--signals")
    e = sub.add_parser("ai-eval"); e.add_argument("file")
    r = sub.add_parser("record"); r.add_argument("--gate", required=True); r.add_argument("--scope", required=True)
    r.add_argument("--checks", required=True); r.add_argument("--score", type=float)
    a = ap.parse_args()
    return {"score": cmd_score, "ai-eval": cmd_ai_eval, "record": cmd_record}[a.cmd](a)

if __name__ == "__main__":
    sys.exit(main())
