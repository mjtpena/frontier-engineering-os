#!/usr/bin/env python3
"""Render tool-specific agent adapters from canonical prompts.

Canonical: feos/agents/<id>.md + feos/orchestration/agents.manifest.yaml
Adapters:  .claude/agents/feos-<id>.md  (Claude Code subagents)
           .github/agents/feos-<id>.agent.md (GitHub Copilot custom agents)
Usage: python scripts/feos_render.py [--check]
  --check  exit 1 if adapters drift from canonical (used in CI).
"""
from __future__ import annotations
import argparse, json, sys
from feos_common import ROOT, load_yaml

def render(agent: dict) -> dict[str, str]:
    body = (ROOT / agent["prompt"]).read_text(encoding="utf-8")
    out = {}
    if agent["id"] != "orchestrator":
        out[agent["claude"]["file"]] = (
            "---\n"
            f"name: feos-{agent['id']}\n"
            f"description: {json.dumps(agent['description'])}\n"
            f"tools: {agent['claude']['tools']}\n"
            f"model: {agent['claude']['model']}\n"
            "---\n\n" + body)
    out[agent["copilot"]["file"]] = (
        "---\n"
        f"name: feos-{agent['id']}\n"
        f"description: {json.dumps(agent['description'])}\n"
        f"tools: {json.dumps(agent['copilot']['tools'])}\n"
        "---\n\n" + body)
    return out

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    manifest = load_yaml("feos/orchestration/agents.manifest.yaml")
    drift = []
    for agent in manifest["agents"]:
        for rel, content in render(agent).items():
            p = ROOT / rel
            if a.check:
                if not p.exists() or p.read_text(encoding="utf-8") != content:
                    drift.append(rel)
            else:
                p.parent.mkdir(parents=True, exist_ok=True)
                p.write_text(content, encoding="utf-8")
                print(f"rendered {rel}")
    if a.check:
        for d in drift: print(f"FAIL  adapter drift: {d} (run python scripts/feos_render.py)")
        print(f"[render --check] {'PASS' if not drift else 'FAIL'}")
        return 1 if drift else 0
    return 0

if __name__ == "__main__":
    sys.exit(main())
