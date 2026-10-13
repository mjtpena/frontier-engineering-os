---
id: RISKS
title: Risk register
status: draft
owner: "@mjtpena"
version: 0.1
trace: [VISION]
---

# Risk register

Ratings are provisional Discovery assessments on a 1 (low) to 5 (high) scale. They support prioritisation only; the named human owner validates treatment and retains any acceptance decision.

| ID | Risk | Category | Likelihood (1-5) | Impact (1-5) | Mitigation | Owner | Status |
|---|---|---|---:|---:|---|---|---|
| RK-001 | Public release without a selected and reviewed licence could leave users without clear permissions and expose the project to legal/provenance disputes. | regulatory | 5 | 5 | Obtain a human licence decision and licensing/provenance review; retain the decision and reviewer evidence before release consideration. | Product owner (`@mjtpena`) | open |
| RK-002 | Copyright ownership, third-party material, generated content, or notice obligations may be unknown even after a licence is selected. | regulatory | 3 | 5 | Inventory provenance and notices across the candidate release and history; escalate interpretations to a named human legal/licensing reviewer. | Product owner (`@mjtpena`) | open |
| RK-003 | Treating the configured AU Government example layer as applicable—or ignoring it when it is applicable—could produce an unsupported regulatory posture. | regulatory | 3 | 4 | Have a named domain owner confirm applicability and framework versions, then record non-applicable items explicitly. | Product owner (`@mjtpena`) | open |
| RK-004 | Secrets, credentials, personal information, classified material, or sensitive history could become public despite the project declaring no data store. | data | 3 | 5 | Obtain current secret/history scan evidence and human review of candidate release content; remove or remediate findings through an approved process rather than merely deleting the latest file. | Security owner (`@mjtpena`) | open |
| RK-005 | No stated readiness or maintenance budget may leave legal review, security work, documentation, or ongoing dependency maintenance incomplete. | budget | 4 | 4 | Product owner records staffing and budget boundaries and explicitly defers or accepts only through the applicable human decision process. | Product owner (`@mjtpena`) | open |
| RK-006 | No target date or chosen release channel/version may cause indefinite scope growth or a rushed release once a date is imposed. | timeline | 4 | 3 | Release manager records a target decision window, candidate scope, and unresolved blockers after requirements are approved. | Release manager (`@mjtpena`) | open |
| RK-007 | Historical passing results in `JUDGEMENT.md` may be mistaken for current evidence, masking failing build, lint, render, or test checks. | tech | 3 | 5 | Run the documented commands on the candidate revision and retain command outputs with exit codes; label historical evidence as such. | Tech lead (`@mjtpena`) | open |
| RK-008 | Local CODEOWNERS and workflow files may create false confidence if branch protection, required reviews/checks, security features, or Actions settings are not enabled on GitHub. | tech | 4 | 5 | Repository administrator verifies host settings directly and records evidence; unresolved settings remain explicit human actions. | Tech lead (`@mjtpena`) | open |
| RK-009 | The checked-in release workflow contains deployment placeholders and does not identify the open-source distribution artefact, so release execution may be ambiguous or misleading. | tech | 4 | 4 | Release manager defines the release channel and artefact set; evaluate the placeholder workflow only against that approved scope. | Release manager (`@mjtpena`) | open |
| RK-010 | Absence of a security policy and confirmed private reporting route may cause vulnerabilities to be disclosed publicly or sent to an unsafe/unmonitored contact. | security | 5 | 5 | Security owner selects and verifies a reporting route and human response expectations, including a fallback when private reporting is unavailable. | Security owner (`@mjtpena`) | open |
| RK-011 | A single-maintainer ownership model may delay reviews, security response, releases, and succession, or weaken practical separation of duties. | governance | 4 | 4 | Product owner decides the governance and backup-owner model and records where independent human review is required. | Product owner (`@mjtpena`) | open |
| RK-012 | Missing contribution and conduct guidance may create inconsistent reviews, inaccessible participation, or unmanaged community incidents. | community | 5 | 4 | Product owner agrees community governance boundaries and assigns human contacts before corresponding documentation is approved. | Product owner (`@mjtpena`) | open |
| RK-013 | Undefined support and compatibility boundaries may lead adopters to rely on untested Python, editor, agent, or platform combinations. | support | 4 | 4 | Maintainer identifies supported combinations and the support commitment, with validation evidence separated from aspirational coverage. | Tech lead (`@mjtpena`) | open |
| RK-014 | Stale or contradictory documentation may undermine trust; for example, `JUDGEMENT.md` says Actions use tags while inspected workflows use full SHAs. | documentation | 4 | 3 | Review public documentation against the candidate revision and distinguish current behaviour, historical evidence, examples, and TODOs. | Product owner (`@mjtpena`) | open |
| RK-015 | Undefined versioning, changelog, and migration practices may make compatibility and upgrade impact unclear after publication. | release | 3 | 4 | Release manager obtains human decisions on public API, versioning, release notes, and migration communication before selecting release evidence. | Release manager (`@mjtpena`) | open |

Constraint-category coverage: regulatory (`RK-001`–`RK-003`), data (`RK-004`), budget (`RK-005`), timeline (`RK-006`), and tech (`RK-007`–`RK-009`).
