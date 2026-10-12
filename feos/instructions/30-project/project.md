---
id: PROJECT-STD
status: approved
owner: "@mjtpena"
---
# L4 Project Standards — frontier-engineering-os

This repository hosts the FEOS framework itself. Agents treat empty sections as "use L1–L3 defaults".

## Stack
- Languages / frameworks: Python 3.12 (CI) for `scripts/` and `feos-tests/`; YAML, JSON Schema, Markdown for the framework
- Hosting: none (no deployed service); CI on GitHub Actions
- Data stores: none
- IaC: none yet (`feos.config.yaml > iac` applies to projects built on FEOS)

## Commands (agents run these verbatim)
```yaml
install: pip install -r scripts/requirements.txt pytest
build:   python -m compileall -q scripts
lint:    python scripts/feos_validate.py && python scripts/feos_render.py --check
test:    python -m pytest -q feos-tests
e2e:     none
format:  none   # no formatter configured
coverage: TBD(@mjtpena, add pytest-cov with --cov-fail-under={min_coverage} once project code lands)
```
`feos_gate.py record` runs `build`, `lint`, `test` and `coverage` itself for G3 (`none` passes, `TBD` fails). In `coverage`, `{min_coverage}` is replaced with `quality.min_coverage` from `feos.config.yaml`.

## Patterns & conventions
- Framework changes are made in the canonical files under `feos/`, then `python scripts/feos_render.py` regenerates the adapters.
- Every behavioural change to `scripts/` comes with a test in `feos-tests/` that fails without it.

## Out of bounds
- Do not edit the generated adapters (`.claude/agents/`, `.github/agents/`) by hand.
