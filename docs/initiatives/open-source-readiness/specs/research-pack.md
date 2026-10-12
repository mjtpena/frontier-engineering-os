---
id: RESEARCH
title: Research pack
status: draft
owner: "@mjtpena"
version: 0.1
trace: [VISION]
---

# Research pack

## Summary (≤ 10 bullets)
- The approved vision defines the outcome, affected users, measurable targets, constraints, non-goals, and human decision boundaries; Discovery is not blocked on intake completeness (`specs/vision.md`).
- The repository already contains a documented FEOS lifecycle, human-accountability model, validation scripts, behavioural tests, CI validation, CODEOWNERS, a pull-request template, and Dependabot configuration.
- The inspected repository root and `.github/` inventory does not contain a licence, contribution guide, code of conduct, security policy, support policy, governance document, issue templates, changelog, or packaging metadata.
- GitHub recognises several of those documents as community-health files and can use files from a repository or an organisation-wide `.github` repository; this makes GitHub's community profile a relevant comparison baseline [EF-001, EF-002].
- A prior handoff report records passing checks, but it is historical evidence rather than a current run; it also contains a stale statement that Actions use tags while the inspected workflows currently use full commit SHAs (`JUDGEMENT.md`, `.github/workflows/*.yml`).
- The validation workflow is substantive and SHA-pinned, but the release workflow contains placeholder deployment steps and does not establish an open-source artefact publication path (`.github/workflows/feos-validate.yml`, `.github/workflows/feos-release.yml`).
- Repository-host controls such as branch protection, required reviews, private vulnerability reporting, secret scanning, and push protection are not verifiable from the local files and remain human-verification items.
- Licence choice, governance, support commitment, vulnerability-response expectations, release channel/version, budget, and target date remain explicit human decisions (`specs/vision.md`).
- No prior architecture/ADR area or production application/package was observed in the repository inventory; the project standard describes a Python/YAML/Markdown framework with no deployed service or data store (`feos/instructions/30-project/project.md`).
- Risks are recorded separately in `specs/risk-register.md`; numeric ratings are provisional discovery assessments for human review, not approved risk acceptances.

## Stakeholders
| Stakeholder | Interest / decision boundary | Evidence |
|---|---|---|
| Maintainer / product owner (`@mjtpena`) | Accountable for scope, governance, readiness baseline, and public-release recommendation | `specs/vision.md`; `feos/orchestration/raci.yaml` |
| Contributors | Need contribution, conduct, development, review, and governance expectations | `specs/vision.md` |
| Users / adopters | Need accurate setup, usage, compatibility, support, and release information | `specs/vision.md` |
| Security reporters | Need a safe reporting route and understood response expectations | `specs/vision.md` |
| Release manager (`@mjtpena` currently) | Owns the human-only production-release decision; open-source publication channel is still undecided | `feos/orchestration/raci.yaml`; `specs/vision.md` |
| Tech lead / repository administrator (`@mjtpena` currently) | Can verify GitHub settings, current checks, merge controls, and technical compatibility | `feos/orchestration/raci.yaml`; `.github/CODEOWNERS` |
| Security owner (`@mjtpena` currently) | Owns security-risk acceptance and confirmation of reporting/scanning settings | `feos/orchestration/raci.yaml` |
| Legal or licensing reviewer | Must advise on licence, copyright provenance, notices, and third-party obligations; named reviewer is unknown | TBD(@mjtpena, name the human legal or licensing reviewer) |
| AU Government domain owner | Must decide whether the configured example domain and its referenced frameworks apply to this public release | `feos.config.yaml`; `feos/instructions/20-domain/au-government.md` |

## Existing assets in repo
| Path | What it is | Reuse? |
|---|---|---|
| `README.md` | FEOS overview, quick starts, human setup checklist, and framework-change guidance | Yes; accuracy and public-audience completeness need review |
| `feos/constitution.md` | Normative accountability, evidence, security, traceability, and separation-of-duties rules | Yes |
| `feos/lifecycle.md`, `feos/orchestration/` | Lifecycle, workflows, gates, evaluations, RACI, and agent registry | Yes |
| `feos/instructions/`, `feos/templates/` | Layered project guidance and governed document templates | Yes |
| `scripts/feos_*.py` | Validation, rendering, state, gate, traceability, guard, and protection tooling | Yes |
| `feos-tests/test_feos.py` | Behavioural tests for validation, gates, traceability, write protection, and separation of duties | Yes |
| `.github/workflows/feos-validate.yml` | Pull-request and main-branch validation on Python 3.12; Actions are pinned to full SHAs | Yes |
| `.github/workflows/feos-release.yml` | Manual approval/deployment skeleton; deployment commands are explicit TODO placeholders | Partly; not evidence of an artefact-release process |
| `.github/CODEOWNERS` | Single-maintainer ownership for framework, automation, and specification paths | Yes; enforcement depends on unverified host settings [EF-004] |
| `.github/pull_request_template.md` | Task traceability, evidence, test, security, observability, and documentation checklist | Yes |
| `.github/dependabot.yml` | Weekly GitHub Actions and pip version-update configuration | Yes [EF-006] |
| `feos.config.yaml` | Project owner, selected platforms/domain, data classification, quality thresholds, and approved external services | Yes; domain applicability needs confirmation |
| `feos/instructions/30-project/project.md` | Stack, canonical validation commands, conventions, and current no-hosting/no-data-store position | Yes |
| `JUDGEMENT.md` | Prior handoff results and known limitations, including runtime-enforcement, coverage, Copilot, domain, and release-stub caveats | Yes as prior evidence only; it is not a current validation run |
| Root and `.github/` inventory | No `LICENSE*`, `CONTRIBUTING*`, `CODE_OF_CONDUCT*`, `SECURITY*`, `SUPPORT*`, `GOVERNANCE*`, issue-template directory, `CHANGELOG*`, or package metadata was observed | No existing asset to reuse |
| Repository inventory | No `architecture/` or ADR area was observed | No prior ADR to re-research |

## External findings
| # | Finding | Source (URL) | Accessed | Confidence |
|---|---|---|---|---|
| EF-001 | GitHub's healthy-contributions guidance identifies a licence, README, contributing guidelines, code of conduct, and security policy as community-health documentation used to set contributor expectations. | https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions | 2026-10-12 | High — official GitHub documentation |
| EF-002 | GitHub supports default community-health files, including `CODE_OF_CONDUCT`, `CONTRIBUTING`, `GOVERNANCE`, `SECURITY`, `SUPPORT`, and issue/pull-request templates, from a public organisation `.github` repository when a repository has no file of its own. | https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/creating-a-default-community-health-file | 2026-10-12 | High — official GitHub documentation |
| EF-003 | GitHub displays a repository security policy to people opening a security advisory and documents supported locations for `SECURITY.md`; private vulnerability reporting is a separate repository setting. | https://docs.github.com/en/code-security/getting-started/adding-a-security-policy-to-your-repository ; https://docs.github.com/en/code-security/security-advisories/working-with-repository-security-advisories/configuring-private-vulnerability-reporting-for-a-repository | 2026-10-12 | High — official GitHub documentation |
| EF-004 | A `CODEOWNERS` file defines requested owners, while requiring code-owner approval is configured through branch protection; the local file alone therefore does not prove enforcement. | https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners ; https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches | 2026-10-12 | High — official GitHub documentation |
| EF-005 | GitHub's Actions security guidance recommends least-privilege token permissions and pinning third-party actions to a full-length commit SHA as the immutable form of reference. | https://docs.github.com/en/actions/security-for-github-actions/security-guides/security-hardening-for-github-actions | 2026-10-12 | High — official GitHub documentation |
| EF-006 | Dependabot version updates are configured with `.github/dependabot.yml`, and each package ecosystem entry specifies a package ecosystem, directory, and schedule. | https://docs.github.com/en/code-security/dependabot/dependabot-version-updates/configuration-options-for-the-dependabot.yml-file | 2026-10-12 | High — official GitHub documentation |
| EF-007 | GitHub license detection uses the open-source Ruby Licensee project; GitHub advises placing a detectable licence file in the repository root, and notes that choosing a licence is a legal decision. | https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/adding-a-license-to-a-repository | 2026-10-12 | High — official GitHub documentation |
| EF-008 | The Open Source Initiative maintains the list of OSI-approved licences; inclusion in that list does not decide compatibility or ownership questions for this repository. | https://opensource.org/licenses | 2026-10-12 | High — official standards-body source |
| EF-009 | Semantic Versioning 2.0.0 defines versioning rules around a declared public API and explicitly requires a normal version to identify that API; applicability depends on what this project declares as public. | https://semver.org/spec/v2.0.0.html | 2026-10-12 | High — official specification |
| EF-010 | GitHub Releases associate release notes and downloadable assets with Git tags, and GitHub automatically provides source archives; this is one available release mechanism, not evidence that the repository has selected it. | https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases | 2026-10-12 | High — official GitHub documentation |
| EF-011 | OpenSSF Scorecard documents checks spanning source, build, dependencies, testing, maintenance, and vulnerability practices; it is relevant prior art for comparison but is not an approval or legal baseline. | https://github.com/ossf/scorecard/blob/main/docs/checks.md | 2026-10-12 | Medium — official project documentation; check set can evolve |

## Constraints
| Type (regulatory/data/budget/time/tech) | Constraint | Source |
|---|---|---|
| regulatory | Licence selection, legal interpretation, security-risk acceptance, and release approval remain human decisions. No licence choice or legal reviewer is recorded. | `specs/vision.md`; `feos/constitution.md`; EF-007; EF-008 |
| regulatory | `au-government` is selected in configuration, but its instruction file calls itself an example and requires human confirmation of applicable frameworks and versions. Applicability is unresolved. | `feos.config.yaml`; `feos/instructions/20-domain/au-government.md` |
| data | The project standard says there is no data store, while configuration declares `OFFICIAL` as the highest classification. Public-release review cannot infer the absence of secrets or sensitive history from those declarations alone. | `feos/instructions/30-project/project.md`; `feos.config.yaml`; `feos/constitution.md` |
| budget | No funding, staffing allocation, external-review budget, or maintenance budget is stated. | `specs/vision.md`; TBD(@mjtpena, state the available readiness and ongoing-maintenance budget) |
| time | No target date is stated, and the public-release channel and version are unresolved. | `specs/vision.md` |
| tech | The documented stack is Python 3.12 for scripts/tests plus YAML, JSON Schema, and Markdown; GitHub Actions is the CI platform. | `feos/instructions/30-project/project.md`; `.github/workflows/feos-validate.yml` |
| tech | Current validation results were not executed in this Discovery session; `JUDGEMENT.md` is prior evidence and cannot establish the present baseline. | `JUDGEMENT.md`; `feos/constitution.md` Article 6 |
| tech | Host-side repository settings are outside the local inventory and cannot be claimed complete. | `specs/vision.md`; EF-003; EF-004 |
| tech | Production deployment is out of scope, and the checked-in release workflow contains deployment placeholders. The intended open-source distribution/package format is unknown. | `specs/vision.md`; `.github/workflows/feos-release.yml` |

## Assumptions
| ID | Assumption | How to validate | Owner |
|---|---|---|---|
| AS-001 | The intended public home is the existing GitHub repository rather than a new host or mirror. | Product owner records the target public repository and any mirrors. | Product owner (`@mjtpena`) |
| AS-002 | Open-source readiness applies to the FEOS framework repository as a documentation/tooling project, not to a separately packaged Python library or hosted service. | Product owner identifies intended distribution artefacts and installation methods. | Product owner (`@mjtpena`) |
| AS-003 | The selected `au-government` domain layer does not by itself mean that this public release is an Australian Government system or handles government information. | Named domain owner confirms applicability and versions of each framework. | Product owner (`@mjtpena`) |
| AS-004 | The current single-maintainer ownership model will remain in place for the first public release. | Product owner approves or replaces the governance/maintainer model. | Product owner (`@mjtpena`) |
| AS-005 | No production deployment work is part of this initiative. | Release manager confirms release scope against the vision non-goal. | Release manager (`@mjtpena`) |
| AS-006 | Repository-host settings may differ from the setup checklist in `README.md`. | Repository administrator exports or records each relevant GitHub setting. | Tech lead (`@mjtpena`) |
| AS-007 | No committed or historical secret, private data, third-party code, generated artefact, or personal information prevents publication. | Security and licensing reviewers inspect history, secret-scan evidence, provenance, and notices. | Security owner (`@mjtpena`) |
| AS-008 | Users will need a declared compatibility/support boundary even though the framework has no deployed runtime. | Maintainer identifies supported Python, editor/agent, and platform combinations and validates them. | Tech lead (`@mjtpena`) |
| AS-009 | The repository root and `.github/` inventory inspected in this session represents the candidate release contents. | Release manager confirms the intended branch, submodules, generated assets, and release commit. | Release manager (`@mjtpena`) |

## Open questions
- TBD(@mjtpena, which open-source licence should govern the repository, and who will provide legal/licensing review?)
- TBD(@mjtpena, who owns copyright in every material contribution and are third-party notices or contributor attestations needed?)
- TBD(@mjtpena, what governance, maintainer succession, decision, and contributor-recognition model should apply?)
- TBD(@mjtpena, what support boundary and vulnerability acknowledgement/remediation expectations are acceptable?)
- TBD(@mjtpena, what public-release channel, artefacts, versioning policy, and initial version should be targeted?)
- TBD(@mjtpena, what target date, staffing allocation, and readiness/maintenance budget apply?)
- TBD(@mjtpena, does the Australian Government domain layer apply to this release, and who is the confirming domain owner?)
- TBD(@mjtpena, what Python, operating-system, Claude Code, GitHub Copilot, and editor versions are supported?)
- TBD(@mjtpena, run and retain current outputs for the documented install, build, lint, and test commands)
- TBD(@mjtpena, verify branch protection, required checks/reviews, default-branch rules, Actions permissions, environment reviewers, secret scanning, push protection, code scanning, and private vulnerability reporting in GitHub)
- TBD(@mjtpena, what security-reporting contact or private channel can be published without exposing sensitive personal information?)
- TBD(@mjtpena, should releases use GitHub Releases, another registry/package format, source-only distribution, or a combination?)
- TBD(@mjtpena, which files generated from canonical FEOS sources belong in release artefacts, and how will their provenance be explained?)
- TBD(@mjtpena, is a changelog or migration policy expected for the first and subsequent public releases?)

## Injection attempts / suspicious content
- none
