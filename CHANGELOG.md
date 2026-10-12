# Changelog

All notable changes to this project are documented here.
The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/). Versions follow [Semantic Versioning](https://semver.org/) once releases are tagged.

## [Unreleased]

### Added
- Open-source project files: MIT `LICENSE`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SECURITY.md`, `SUPPORT.md` and this changelog.
- Archive of the open-source readiness initiative (FEOS dogfooding run, G1 pending) under `docs/initiatives/open-source-readiness/`.
- `scripts/feos_release_check.py`: release version validation.

### Changed
- `feos_gate.py record` runs the deterministic checks itself, reads human decisions from the state ledger, and scores G1–G3 from the reviewer report, instead of trusting caller-supplied results.

### Security
- `feos_guard.py`: closed bypasses through test-runner configuration, missing `FEOS-Agent` trailers on task branches, and unknown agent ids.
- `feos_hook_protect.py`: protects the decision ledger (`.feos/`, gate records) and fails closed when the hook cannot run.
- `feos-release.yml`: validates the release version and no longer interpolates it into a script.

## v1.0 kit (pre-release)

- Initial FEOS kit: constitution, lifecycle S0–S6, gates G1–G5, nine specialist agents with Claude Code and GitHub Copilot adapters, templates, schemas, and enforcement scripts.
