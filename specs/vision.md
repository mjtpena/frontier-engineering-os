---
id: VISION
title: Frontier Engineering OS open-source readiness
status: approved
owner: "@mjtpena"
version: 0.1
trace: []
---

# Vision

## Problem
The repository is intended for public open-source use, but its readiness has not
yet been assessed through the FEOS lifecycle. Prospective users, contributors,
maintainers, and security reporters need a repository whose legal, community,
security, support, release, documentation, packaging, testing, and CI posture is
explicit, verifiable, and suitable for public release.

## Desired outcome
Assess the repository against a documented open-source readiness baseline,
identify concrete gaps, and close approved gaps through traceable FEOS tasks.
Prepare evidence for a human decision on whether the repository is ready for a
public open-source release without inventing legal decisions, approvals, or
repository-host settings.

## Users / stakeholders
| Group | Need | Influence |
|---|---|---|
| Maintainer / product owner | A governed, evidence-backed public-release decision | Accountable |
| Contributors | Clear contribution, governance, conduct, development, and review expectations | High |
| Users / adopters | Accurate setup, usage, compatibility, support, and release information | High |
| Security reporters | A safe, explicit vulnerability-reporting path and response expectations | High |
| Release manager | Repeatable readiness, release, and rollback evidence | High |

## Success metrics
| Metric | Baseline | Target | How measured |
|---|---|---|---|
| Approved readiness requirements covered | TBD(@mjtpena, approve the readiness scope and requirements) | 100% of approved requirements traced to evidence | FEOS traceability and gate evidence |
| Identified critical public-release blockers unresolved | TBD(discovery, assess the repository) | 0 at release approval | Readiness assessment, risk register, G4/G5 evidence |
| Required community, security, governance, legal, and support decisions documented | TBD(discovery, establish applicable baseline) | 100% of approved baseline | Repository audit and human approvals |
| Project validation commands passing | TBD(discovery, capture current evidence) | All configured hard checks pass | Recorded build, lint, and test command outputs |

## Constraints & non-goals
- Human owners retain all legal, licensing, security-risk, architecture, merge,
  and public-release decisions.
- No implementation starts without an approved PRD, passed architecture gate,
  and an approved `TK-###` in `plan/backlog.yaml`.
- The assessment must cover licensing; contribution and governance guidance;
  community health; security reporting; code of conduct; support policy;
  release/readiness; and, where applicable, packaging, documentation, tests,
  and CI.
- Repository-host settings that cannot be verified locally must be recorded as
  human actions or unknowns, not claimed as complete.
- Existing FEOS controls, gates, schemas, tests, CI workflows, and linter
  configuration must not be weakened or edited to expedite release.
- Production deployment is outside this initiative unless separately approved.

## Open questions
- TBD(@mjtpena, which open-source licence should govern the repository?)
- TBD(@mjtpena, what governance and maintainer model should apply?)
- TBD(@mjtpena, what support commitment and vulnerability-response expectations are acceptable?)
- TBD(@mjtpena, what public-release channel and version should be targeted?)
- TBD(discovery, which repository files and GitHub settings are currently absent or incomplete?)
