#!/usr/bin/env python3
"""Ambiguity lint for requirements (soft check, G1.3). Usage: python scripts/feos_lint_requirements.py specs/prd.md"""
import re, sys
from pathlib import Path
VAGUE = ["fast", "quick", "user-friendly", "easy", "intuitive", "flexible", "robust", "seamless", "efficient",
         "as appropriate", "as needed", "etc", "and/or", "approximately", "minimal", "maximise", "maximize",
         "minimise", "minimize", "state-of-the-art", "best practice", "sufficient", "adequate", "some", "several", "TBC"]
PAT = re.compile(r"\b(" + "|".join(re.escape(v) for v in VAGUE) + r")\b", re.I)
def main():
    if len(sys.argv) != 2: print(__doc__); return 2
    hits = 0
    in_code = False
    for n, line in enumerate(Path(sys.argv[1]).read_text(encoding="utf-8").splitlines(), 1):
        if line.strip().startswith("```"): in_code = not in_code
        if in_code or line.startswith("<!--"): continue
        for m in PAT.finditer(line):
            hits += 1; print(f"{sys.argv[1]}:{n}: vague term '{m.group(0)}': {line.strip()[:100]}")
    print(f"[lint_requirements] {'PASS' if not hits else 'FAIL'}: {hits} vague terms")
    return 1 if hits else 0
if __name__ == "__main__": sys.exit(main())
