#!/usr/bin/env python3
"""FEOS traceability checker.

  python scripts/feos_trace.py --stage requirements   # FR/NFR -> BR
  python scripts/feos_trace.py --stage architecture   # NFR -> mechanism + verification (architecture/nfr.md)
  python scripts/feos_trace.py --stage plan           # FR/NFR -> story
  python scripts/feos_trace.py --stage tests          # FR -> test tagged '@covers FR-###'
  python scripts/feos_trace.py                        # every stage whose inputs exist
Exit 1 on any orphan.
"""
from __future__ import annotations
import argparse, re, sys
from feos_common import ROOT, Report, load_yaml

FR_HEAD = re.compile(r"^#{2,4}\s+(FR-\d{3,})\b.*$", re.M)
TRACES = re.compile(r"\*\*Traces:\*\*\s*(.+)")
ID = lambda p: re.compile(rf"\b{p}-\d{{3,}}\b")

def prd_requirements():
    text = (ROOT / "specs/prd.md").read_text(encoding="utf-8")
    reqs = {}
    heads = list(FR_HEAD.finditer(text))
    for i, m in enumerate(heads):
        block = text[m.end(): heads[i + 1].start() if i + 1 < len(heads) else len(text)]
        block = re.split(r"^##\s", block, maxsplit=1, flags=re.M)[0]
        t = TRACES.search(block)
        reqs[m.group(1)] = set(ID("BR").findall(t.group(1))) if t else set()
    for line in text.splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if cells and re.fullmatch(r"NFR-\d{3,}", cells[0]):
            reqs[cells[0]] = set(ID("BR").findall(cells[-1]))
    return reqs

def brs():
    p = ROOT / "specs/brd.md"
    return set(ID("BR").findall(p.read_text(encoding="utf-8"))) if p.exists() else set()

def stage_requirements(r):
    reqs, known = prd_requirements(), brs()
    if not reqs: r.err("no FR/NFR found in specs/prd.md")
    for rid, parents in reqs.items():
        if not parents: r.err(f"{rid}: no BR trace")
        elif parents - known: r.err(f"{rid}: traces to unknown {sorted(parents - known)}")
        else: r.passed()

def stage_architecture(r):
    nfrs = [k for k in prd_requirements() if k.startswith("NFR")]
    p = ROOT / "architecture/nfr.md"
    if not p.exists(): r.err("architecture/nfr.md missing"); return
    rows = {}
    for line in p.read_text(encoding="utf-8").splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if cells and re.fullmatch(r"NFR-\d{3,}", cells[0]): rows[cells[0]] = cells
    for n in nfrs:
        c = rows.get(n)
        if not c: r.err(f"{n}: not mapped in architecture/nfr.md")
        elif len(c) < 3 or not c[1] or not c[2]: r.err(f"{n}: mechanism or verification empty")
        else: r.passed()

def stage_plan(r):
    reqs = prd_requirements()
    bl = load_yaml("plan/backlog.yaml")
    covered = {c for ep in bl["epics"] for ft in ep["features"] for st in ft["stories"] for c in st["covers"]}
    for rid in reqs:
        r.passed() if rid in covered else r.err(f"{rid}: not covered by any story")
    for c in covered - set(reqs): r.err(f"backlog covers unknown requirement {c}")

COVERS = re.compile(r"@covers\s+((?:N?FR-\d{3,}[,\s]*)+)")

def stage_tests(r):
    reqs = [k for k in prd_requirements() if k.startswith("FR")]
    tagged = set()
    for d in ("tests", "evals"):
        base = ROOT / d
        if not base.exists(): continue
        for f in base.rglob("*"):
            if not f.is_file() or f.suffix in {".png", ".jpg", ".zip", ".bin", ".pyc"}: continue
            try: text = f.read_text(encoding="utf-8", errors="ignore")
            except OSError: continue
            for group in COVERS.findall(text):
                tagged |= set(re.findall(r"N?FR-\d{3,}", group))
    for rid in reqs:
        r.passed() if rid in tagged else r.err(f"{rid}: no test tagged '@covers {rid}'")

STAGES = {"requirements": (stage_requirements, ["specs/prd.md"]),
          "architecture": (stage_architecture, ["specs/prd.md"]),
          "plan": (stage_plan, ["specs/prd.md", "plan/backlog.yaml"]),
          "tests": (stage_tests, ["specs/prd.md"])}

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--stage", choices=list(STAGES))
    a = ap.parse_args()
    r = Report("feos_trace")
    todo = [a.stage] if a.stage else [s for s, (_, req) in STAGES.items() if all((ROOT / p).exists() for p in req)]
    if not todo: r.err("nothing to trace (specs/prd.md missing)")
    for s in todo:
        fn, req = STAGES[s]
        missing = [p for p in req if not (ROOT / p).exists()]
        if missing: r.err(f"stage {s}: missing {missing}"); continue
        fn(r)
    return r.finish()

if __name__ == "__main__":
    sys.exit(main())
