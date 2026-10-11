"""Shared helpers for FEOS scripts. Requires: pyyaml, jsonschema."""
from __future__ import annotations
import json, re, sys
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parent.parent
FM_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.S)

def load_yaml(p): 
    with open(ROOT / p if not Path(p).is_absolute() else p, encoding="utf-8") as f:
        return yaml.safe_load(f)

def load_json(p):
    with open(ROOT / p, encoding="utf-8") as f:
        return json.load(f)

def front_matter(path: Path):
    text = path.read_text(encoding="utf-8")
    m = FM_RE.match(text)
    if not m:
        return None, text
    return yaml.safe_load(m.group(1)) or {}, text[m.end():]

def config():
    return load_yaml("feos.config.yaml")

class Report:
    def __init__(self, name): self.name, self.errors, self.warnings, self.ok = name, [], [], 0
    def err(self, msg): self.errors.append(msg)
    def warn(self, msg): self.warnings.append(msg)
    def passed(self): self.ok += 1
    def finish(self) -> int:
        for w in self.warnings: print(f"WARN  {w}")
        for e in self.errors: print(f"FAIL  {e}")
        status = "PASS" if not self.errors else "FAIL"
        print(f"[{self.name}] {status}: {self.ok} checks ok, {len(self.warnings)} warnings, {len(self.errors)} errors")
        return 0 if not self.errors else 1
