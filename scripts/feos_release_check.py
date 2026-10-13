#!/usr/bin/env python3
"""Release approval check (Human Approval). Run by .github/workflows/feos-release.yml before any deployment job.

  python scripts/feos_release_check.py v1.2.3

Passes only if evidence/release/<version>/approval.md is for that release, records decision: approved,
and names a human approver. The version is validated before it is used in a path, so workflow input
can neither traverse directories nor inject code.
"""
from __future__ import annotations
import re, sys
from feos_common import ROOT, front_matter

VERSION = re.compile(r"v\d+\.\d+\.\d+")

def main(argv) -> int:
    if len(argv) != 2 or not VERSION.fullmatch(argv[1]):
        print(f"FAIL  version must be vX.Y.Z, got {argv[1:]!r}"); return 1
    v = argv[1]
    p = ROOT / "evidence/release" / v / "approval.md"
    if not p.exists():
        print(f"FAIL  {p.relative_to(ROOT)} missing"); return 1
    fm, _ = front_matter(p)
    fm = fm or {}
    approver = str(fm.get("approver") or "").strip()
    fails = []
    if str(fm.get("release", "")) != v: fails.append(f"approval.md is for release {fm.get('release')!r}, not {v}")
    if fm.get("decision") != "approved": fails.append(f"decision is {fm.get('decision')!r}, not 'approved'")
    if not approver or approver.upper().startswith("TBD"): fails.append("approver is empty or TBD")
    for f in fails: print(f"FAIL  {f}")
    print(f"[release_check] {'PASS' if not fails else 'FAIL'}: {p.relative_to(ROOT)}")
    return 1 if fails else 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))
