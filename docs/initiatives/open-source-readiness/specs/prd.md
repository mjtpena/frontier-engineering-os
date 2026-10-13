---
id: PRD
title: Product requirements
status: review
owner: "@mjtpena"
version: 0.1
trace: [BRD]
---

# Product Requirements Document

## Personas

| Persona | Goal | Primary concern |
|---|---|---|
| Maintainer / product owner | Decide whether the candidate revision is ready for public release | Every claim is evidenced and every human decision is explicit |
| Contributor | Understand how to propose, discuss, review, and govern a change | Participation and conduct expectations are discoverable before contributing |
| User / adopter | Install and use the framework within declared boundaries | Instructions, compatibility, maintenance, and release information match the candidate revision |
| Security reporter | Report a suspected vulnerability without public disclosure | A verified confidential route and response expectations are published |
| Release manager | Assemble and evaluate a repeatable release candidate | Artefacts, version, checks, blockers, decisions, and rollback boundary are unambiguous |
| Repository administrator | Verify controls that are not represented by local files | Host-setting evidence is tied to the target repository and candidate revision |
| Human legal or licensing reviewer | Review permissions, provenance, and obligations | No automated output is presented as legal approval |
| Australian Government domain owner | Decide whether the configured domain layer applies | Applicability, framework versions, and required reviews are recorded by a human |

## User journeys

1. **Readiness assessment:** The maintainer identifies the candidate repository and approved baseline, records evidence for every criterion, assigns gaps, and sees unresolved human decisions as blockers rather than inferred answers.
2. **Contribution:** A prospective contributor finds participation, review, governance, and conduct rules before opening a change or reporting a community incident.
3. **Adoption:** A user follows verified setup and usage guidance, checks declared compatibility and maintenance boundaries, and finds release-change information.
4. **Security reporting:** A reporter finds a confidential channel, confirms its fallback route, and reads the human-approved acknowledgement and remediation expectations.
5. **Release decision:** The release manager reviews current validation and host evidence, legal and security decisions, requirement coverage, open risks, and candidate artefacts before requesting human approval.
6. **Domain applicability:** The domain owner records whether Australian Government requirements apply; applicable obligations enter the baseline and non-applicable obligations retain a rationale.

## Functional requirements
<!-- One block per FR. Keep IDs stable; never reuse a retired ID. -->

Each FR below explicitly covers happy, negative, authorization, boundary, and dependency-failure paths. No path class is marked not applicable: even publicly readable repository information has an authorization boundary because reading must not require repository write permission, while approval or alteration remains restricted to the named human authority.

### FR-001 — Define the readiness assessment
- **Traces:** BR-001
- **Priority:** Must
- **Description:** The readiness process shall identify the candidate repository, candidate revision, assessment date, approved baseline version, criterion owner, and permitted criterion outcomes.
- **Acceptance criteria:**
  - AC1 — Given a human-approved baseline and an identified candidate revision, When an assessment is opened, Then it records the repository, immutable revision identifier, date, baseline version, owner, and the outcomes met, unmet, not applicable with rationale, or blocked by a named decision.
  - AC2 (negative) — Given no human-approved baseline or no immutable candidate revision identifier, When an assessment is requested, Then the assessment is marked blocked and does not report a readiness result.
  - AC3 (authorization) — Given an actor is not recorded as the human baseline approval authority, When that actor attempts to approve or alter the baseline used by an assessment, Then the attempted change is rejected and the approved baseline remains unchanged.
  - AC4 (boundary) — Given an approved baseline containing one criterion and one immutable candidate revision identifier, When an assessment is opened, Then the single criterion and revision are recorded without requiring a second criterion or revision.
  - AC5 (dependency failure) — Given the approved baseline record or candidate-revision record cannot be retrieved, When an assessment is opened, Then the assessment is marked blocked and no readiness result is reported from cached or historical evidence.

### FR-002 — Record criterion evidence and gaps
- **Traces:** BR-001, BR-008
- **Priority:** Must
- **Description:** The readiness process shall associate each baseline criterion with evidence, an outcome, and an accountable owner for unmet or blocked criteria.
- **Acceptance criteria:**
  - AC1 — Given an approved criterion, When it is assessed, Then its record contains an outcome, evidence reference, assessment date, and an accountable human owner for each unmet or blocked outcome.
  - AC2 (negative) — Given a criterion with no evidence reference or required rationale, When readiness is calculated, Then that criterion is reported as blocked and is not counted as met.
  - AC3 (authorization) — Given an actor is not recorded in the approved baseline as the criterion owner or delegated assessor, When that actor attempts to alter the criterion outcome, Then the alteration is rejected and the prior outcome remains unchanged.
  - AC4 (boundary) — Given an approved baseline containing one criterion, When criterion coverage is calculated, Then exactly one criterion record is required and duplicate records do not increase coverage.
  - AC5 (dependency failure) — Given a referenced evidence item cannot be retrieved at assessment time, When the criterion is evaluated, Then its outcome is blocked and the inaccessible reference is not counted as evidence.

### FR-003 — Retain the licence decision
- **Traces:** BR-002
- **Priority:** Must
- **Description:** The readiness process shall retain the human-selected licence, the candidate licence material, and the named human licensing review evidence.
- **Acceptance criteria:**
  - AC1 — Given a human licence decision and completed licensing review, When legal readiness is assessed, Then the selected licence, decision owner, reviewer, decision date, and reviewed candidate material are referenced.
  - AC2 (negative) — Given the licence choice or named human review is unresolved, When public-release readiness is assessed, Then legal readiness is blocked and no licence is inferred.
  - AC3 (authorization) — Given a licence decision or review record is submitted by a person other than the recorded human decision owner or reviewer, When legal readiness is assessed, Then that record is rejected as approval evidence and legal readiness remains blocked.
  - AC4 (boundary) — Given the reviewed licence material omits one artefact included in the candidate release, When legal readiness is assessed, Then licence coverage is incomplete and legal readiness remains blocked.
  - AC5 (dependency failure) — Given the retained licence decision, candidate licence material, or human review evidence cannot be retrieved, When legal readiness is assessed, Then legal readiness remains blocked and the missing record is identified.

### FR-004 — Retain provenance and notice review
- **Traces:** BR-002
- **Priority:** Must
- **Description:** The readiness process shall retain human review results for copyright ownership, contribution provenance, third-party material, generated material, and notice obligations in the candidate release.
- **Acceptance criteria:**
  - AC1 — Given the candidate contents and history, When the named human reviewer completes provenance review, Then the reviewed scope, findings, required notices, dispositions, reviewer, and date are recorded.
  - AC2 (negative) — Given an unresolved provenance or notice finding, When legal readiness is assessed, Then the finding remains a release blocker unless a human with authority records its disposition.
  - AC3 (authorization) — Given a person is not the recorded human licensing reviewer or disposition authority, When that person attempts to close a provenance or notice finding, Then the attempted disposition is rejected and the finding remains open.
  - AC4 (boundary) — Given the approved review scope has lower and upper history bounds and a defined candidate-content set, When review coverage is assessed, Then evidence covers both history bounds and every item in the candidate-content set or legal readiness remains blocked.
  - AC5 (dependency failure) — Given a required history, provenance, or notice source cannot be inspected, When the review is completed, Then the inaccessible scope is recorded and legal readiness remains blocked rather than treating it as reviewed.

### FR-005 — Publish contribution expectations
- **Traces:** BR-003
- **Priority:** Must
- **Description:** The repository shall state how contributors propose changes, prepare and validate changes, submit changes, obtain review, and report contribution-process concerns.
- **Acceptance criteria:**
  - AC1 — Given approved contribution expectations, When a prospective contributor follows the repository guidance, Then the proposal, development, validation, submission, review, and concern-reporting steps are identifiable.
  - AC2 (negative) — Given a contribution path depends on an unavailable tool, permission, or contact, When the guidance is reviewed, Then the path is marked blocked until a verified alternative is documented.
  - AC3 (authorization) — Given a prospective contributor has no repository write permission, When the contributor opens the contribution guidance, Then every contribution and concern-reporting step is readable without write permission.
  - AC4 (boundary) — Given one of the proposal, development, validation, submission, review, or concern-reporting steps is omitted, When contribution readiness is assessed, Then the criterion is unmet; when all six are present, Then the completeness check passes.
  - AC5 (dependency failure) — Given a referenced contribution tool, permission-request route, or contact cannot be reached, When the documented path is tested, Then that path is marked blocked and is not represented as usable.

### FR-006 — Publish governance expectations
- **Traces:** BR-003
- **Priority:** Must
- **Description:** The repository shall state the human-approved maintainer roles, decision authority, change process, succession approach, and contributor-recognition process.
- **Acceptance criteria:**
  - AC1 — Given a human-approved governance model, When a contributor reads the governance information, Then each listed role, decision boundary, change mechanism, succession rule, and recognition mechanism is stated.
  - AC2 (negative) — Given the governance model is not approved, When governance readiness is assessed, Then the requirement is blocked with `TBD(@mjtpena, approve the governance and maintainer model)` and no model is inferred from CODEOWNERS.
  - AC3 (authorization) — Given governance information is submitted as approved by a person who is not the recorded human governance decision owner, When governance readiness is assessed, Then the approval claim is rejected and the requirement remains blocked.
  - AC4 (boundary) — Given exactly one required governance element is absent from the listed roles, decision boundaries, change mechanism, succession rule, or recognition mechanism, When completeness is checked, Then governance readiness is unmet.
  - AC5 (dependency failure) — Given the retained governance decision or a referenced governance process cannot be retrieved, When governance readiness is assessed, Then the affected governance element is blocked and is not inferred from repository permissions.

### FR-007 — Publish conduct expectations
- **Traces:** BR-003
- **Priority:** Must
- **Description:** The repository shall publish human-approved conduct rules, enforcement responsibilities, confidential incident-reporting routes, and enforcement review boundaries.
- **Acceptance criteria:**
  - AC1 — Given approved conduct rules and verified human contacts, When a participant reviews the conduct information, Then expected behaviour, prohibited behaviour, reporting routes, enforcement responsibility, and review boundaries are stated.
  - AC2 (negative) — Given a reporting contact is unverified or exposes sensitive personal information, When conduct readiness is assessed, Then the route is rejected and the criterion remains blocked.
  - AC3 (authorization) — Given conduct rules are submitted as approved by a person who is not the recorded human conduct decision owner, When conduct readiness is assessed, Then the approval claim is rejected and the prior approved rules remain unchanged.
  - AC4 (boundary) — Given one required conduct element is absent from expected behaviour, prohibited behaviour, reporting routes, enforcement responsibility, or review boundaries, When completeness is checked, Then conduct readiness is unmet.
  - AC5 (dependency failure) — Given a confidential incident-reporting route cannot receive a test contact or its responsible human cannot be verified, When the route is assessed, Then the route is marked unavailable and conduct readiness remains blocked.

### FR-008 — Publish vulnerability-reporting information
- **Traces:** BR-004
- **Priority:** Must
- **Description:** The repository shall publish the in-scope release lines, confidential primary and fallback vulnerability-reporting routes, requested report contents, disclosure boundaries, and human-approved response expectations.
- **Acceptance criteria:**
  - AC1 — Given verified reporting routes and human-approved response expectations, When a reporter reviews the security information, Then scope, primary route, fallback route, requested details, disclosure boundaries, and expectations are stated.
  - AC2 (negative) — Given either reporting route is unverified or response expectations are undecided, When security readiness is assessed, Then the criterion remains blocked and no response time is invented.
  - AC3 (authorization) — Given a reporter has no repository write permission, When the reporter reads the security information and uses a published reporting route, Then repository write permission is not required to read the instructions or submit the report.
  - AC4 (boundary) — Given one release line is declared in scope and one is declared out of scope, When the security information is reviewed, Then each line has exactly one scope classification and neither is presented with both classifications.
  - AC5 (dependency failure) — Given the primary reporting route is unavailable, When a reporter follows the published instructions, Then the verified fallback route is identifiable; if the fallback route is also unavailable, Then security readiness remains blocked.

### FR-009 — Verify repository-host controls
- **Traces:** BR-004
- **Priority:** Must
- **Description:** The readiness process shall record direct evidence for each approved repository-host criterion, including merge protection, required checks and reviews, automation permissions, security scanning, push protection, and private vulnerability reporting.
- **Acceptance criteria:**
  - AC1 — Given access to the target repository settings, When the repository administrator verifies an approved host criterion, Then the setting value, target repository, evidence date, and verifier are recorded.
  - AC2 (negative) — Given a host setting cannot be accessed or verified, When the criterion is assessed, Then it is marked blocked or unmet and local configuration is not accepted as proof of the host setting.
  - AC3 (authorization) — Given host-setting evidence is submitted by a person who is not the recorded repository administrator or delegated verifier, When the corresponding criterion is assessed, Then the evidence is rejected and the criterion remains blocked.
  - AC4 (boundary) — Given the approved host baseline contains one criterion, When host-control coverage is calculated, Then exactly one dated setting record for the target repository is required and duplicate records do not increase coverage.
  - AC5 (dependency failure) — Given verification of the host-settings source returns at least one retrievable criterion and at least one inaccessible criterion, When verification is performed, Then each inaccessible criterion is blocked, each retrieved criterion retains its own result, and no repository-wide pass is reported.

### FR-010 — Record candidate security review
- **Traces:** BR-004
- **Priority:** Must
- **Description:** The readiness process shall retain candidate-revision and history review evidence for exposed credentials, sensitive information, dependency findings, and third-party material, with a human disposition for each release-blocking finding.
- **Acceptance criteria:**
  - AC1 — Given an identified candidate revision and approved review scope, When security review is completed, Then the scope, revision, methods, dated results, reviewer, and finding dispositions are recorded.
  - AC2 (negative) — Given a critical finding lacks human remediation or risk disposition, When release readiness is assessed, Then the candidate is reported as not ready and the finding remains open.
  - AC3 (authorization) — Given a person is not the recorded security-risk disposition authority, When that person attempts to accept or close a release-blocking finding, Then the disposition is rejected and the finding remains open.
  - AC4 (boundary) — Given the approved history review has lower and upper bounds, When review coverage is assessed, Then evidence identifies both bounds and the candidate revision or the security review is incomplete.
  - AC5 (dependency failure) — Given an approved security-review method cannot complete or its results cannot be retrieved, When security readiness is assessed, Then the affected review scope is marked incomplete and the candidate is not reported ready.

### FR-011 — Publish compatibility boundaries
- **Traces:** BR-005
- **Priority:** Must
- **Description:** The repository shall state the human-approved Python, operating-system, editor, agent, and integration combinations covered by validation evidence.
- **Acceptance criteria:**
  - AC1 — Given approved compatibility boundaries and validation results, When a user reviews compatibility information, Then each covered combination and its evidence status are identifiable.
  - AC2 (negative) — Given a combination has no retained validation evidence, When compatibility is published, Then it is labelled unverified or excluded rather than claimed as covered.
  - AC3 (authorization) — Given a user has no repository write permission, When the user opens the compatibility information, Then every published compatibility boundary and evidence status is readable without write permission.
  - AC4 (boundary) — Given a tested combination and a combination that differs from it by one declared compatibility dimension, When compatibility is published, Then only combinations within the human-approved boundary are labelled covered and the adjacent unapproved combination is labelled unverified or excluded.
  - AC5 (dependency failure) — Given a declared validation environment cannot be provisioned or its retained result cannot be retrieved, When compatibility is assessed, Then affected combinations are labelled unverified and are not counted as covered.

### FR-012 — Publish maintenance and user-assistance boundaries
- **Traces:** BR-005
- **Priority:** Must
- **Description:** The repository shall state the human-approved maintenance period, user-assistance channels, eligible request types, response commitment, and end-of-maintenance communication process.
- **Acceptance criteria:**
  - AC1 — Given approved maintenance and user-assistance decisions, When a user reviews the policy, Then the period, channels, eligible requests, response commitment, and end-of-maintenance process are stated.
  - AC2 (negative) — Given any commitment remains undecided, When readiness is assessed, Then the undecided commitment is shown as `TBD(@mjtpena, approve maintenance and user-assistance commitments)` and is not replaced by an implied service level.
  - AC3 (authorization) — Given a maintenance or user-assistance commitment is submitted by a person who is not its recorded human decision owner, When readiness is assessed, Then the commitment is rejected and the corresponding decision remains unresolved.
  - AC4 (boundary) — Given a published maintenance end date, When the policy is checked for the periods before, on, and after that date, Then it states the maintenance status and user-assistance route for each period without extending the approved commitment.
  - AC5 (dependency failure) — Given a published user-assistance channel cannot receive a test request, When the channel is assessed, Then it is labelled unavailable and an approved alternative is stated or readiness remains blocked.

### FR-013 — Verify public user documentation
- **Traces:** BR-005, BR-007
- **Priority:** Must
- **Description:** The readiness process shall verify that public overview, prerequisites, setup, validation, usage, troubleshooting, and limitation statements match the candidate revision.
- **Acceptance criteria:**
  - AC1 — Given the candidate revision and its public documentation, When each documented command and referenced path is checked, Then the result and revision are recorded and each limitation or placeholder affecting use is identified.
  - AC2 (negative) — Given a documented command, path, claim, or link does not match the candidate revision, When documentation readiness is assessed, Then the discrepancy is recorded as unmet and stale historical evidence is not treated as a passing result.
  - AC3 (authorization) — Given a user has no repository write permission, When the user opens public overview, setup, usage, troubleshooting, and limitation information, Then each published page is readable without write permission.
  - AC4 (boundary) — Given the public documentation contains one command and one referenced repository path, When verification is performed, Then both items receive separate results and neither may be omitted from the completeness count.
  - AC5 (dependency failure) — Given a required command environment, internal-link checker, or referenced path cannot be accessed, When documentation readiness is assessed, Then the affected check is blocked and is not recorded as passing.

### FR-014 — Retain the release definition
- **Traces:** BR-006
- **Priority:** Must
- **Description:** The readiness process shall retain human decisions for the release channel, candidate artefacts, included and excluded generated material, public API boundary, versioning rules, initial version, target repository, and target decision date.
- **Acceptance criteria:**
  - AC1 — Given human release decisions, When the release definition is reviewed, Then each decision, owner, date, candidate revision, included artefact, and excluded artefact is recorded.
  - AC2 (negative) — Given a required release decision is unresolved, When release readiness is assessed, Then release execution remains blocked and the checked-in deployment placeholders are not treated as an artefact-publication process.
  - AC3 (authorization) — Given a release definition is submitted as approved by a person who is not the recorded human release decision owner, When release readiness is assessed, Then the approval claim is rejected and release execution remains blocked.
  - AC4 (boundary) — Given the candidate inventory contains one artefact, When the release definition is checked, Then that artefact is classified exactly once as included or excluded; any unclassified or doubly classified artefact blocks release execution.
  - AC5 (dependency failure) — Given the candidate artefact inventory or retained release decision cannot be retrieved, When the release definition is reviewed, Then completeness cannot be established and release execution remains blocked.

### FR-015 — Publish release-change information
- **Traces:** BR-006
- **Priority:** Must
- **Description:** The repository shall communicate the candidate version, material changes, compatibility impact, known limitations, upgrade actions, and security-sensitive disclosure boundaries using the human-approved release policy.
- **Acceptance criteria:**
  - AC1 — Given an approved release policy and candidate revision, When release-change information is prepared, Then the version, changes, compatibility impact, limitations, upgrade actions, and disclosure boundaries are stated.
  - AC2 (negative) — Given versioning, changelog, migration, or disclosure policy is undecided, When release-change information is requested, Then publication is blocked by the corresponding named human decision.
  - AC3 (authorization) — Given release-change information is submitted for publication by a person who is not the recorded human release owner or delegate, When publication is requested, Then the request is rejected and no approved-release status is shown.
  - AC4 (boundary) — Given the candidate has zero material changes or zero upgrade actions under the approved release policy, When release-change information is prepared, Then the corresponding field explicitly states none with the approved rationale rather than being omitted.
  - AC5 (dependency failure) — Given candidate change history, compatibility results, or security-disclosure decisions cannot be retrieved, When release-change information is prepared, Then publication remains blocked and the unavailable source is identified.

### FR-016 — Retain current validation evidence
- **Traces:** BR-007
- **Priority:** Must
- **Description:** The readiness process shall execute the configured install, build, lint, and test commands against the candidate revision and retain each command, revision, timestamp, exit code, and output reference.
- **Acceptance criteria:**
  - AC1 — Given an identified candidate revision and the approved project commands, When validation is run, Then every configured command has a command string, revision, timestamp, exit code, and retained output reference.
  - AC2 (negative) — Given a configured hard command fails, is skipped, or lacks retained output, When engineering readiness is assessed, Then the hard-check result is failed and historical output is not substituted.
  - AC3 (authorization) — Given an actor is not authorized by the recorded project-command decision owner to alter the configured command set, When the actor substitutes, removes, or weakens a command, Then results from the altered set are rejected as readiness evidence.
  - AC4 (boundary) — Given the approved command set contains one hard command, When validation is run, Then that command executes once against the candidate revision and one complete evidence record is required for hard-check readiness.
  - AC5 (dependency failure) — Given a required execution environment or command dependency is unavailable, When validation is run, Then the affected command records a non-passing result and retained output rather than being skipped or replaced with historical output.

### FR-017 — Produce the readiness decision package
- **Traces:** BR-008
- **Priority:** Must
- **Description:** The readiness process shall produce a candidate-specific package containing requirement coverage, criterion outcomes, evidence references, open risks, blockers, deferred items, accountable owners, and recorded human decisions.
- **Acceptance criteria:**
  - AC1 — Given completed readiness records, When the decision package is generated, Then every approved requirement maps to evidence or a named blocker and the package identifies the candidate revision and accountable human decision owner.
  - AC2 (negative) — Given a critical blocker remains open or an approved requirement lacks evidence, When a release recommendation is requested, Then the package reports not ready and does not record AI output as approval or risk acceptance.
  - AC3 (authorization) — Given an actor is not the recorded accountable human release decision owner, When that actor or an AI agent attempts to change the package decision to approved, Then the attempt is rejected and no human approval is recorded.
  - AC4 (boundary) — Given exactly one approved requirement lacks both evidence and a named blocker, When package completeness is calculated, Then coverage is below 100% and the package cannot recommend ready.
  - AC5 (dependency failure) — Given the trace report, risk record, or evidence index cannot be retrieved, When the decision package is generated, Then the missing dependency is identified, the package is incomplete, and no ready recommendation is issued.

### FR-018 — Record domain applicability
- **Traces:** BR-009
- **Priority:** Must
- **Description:** The readiness process shall retain the named human domain owner's decision on Australian Government domain applicability and, when applicable, the selected framework versions, resulting criteria, and required human reviews.
- **Acceptance criteria:**
  - AC1 — Given a named domain owner, When applicability is decided, Then the decision, rationale, date, applicable framework versions, resulting criteria, and required reviews are recorded.
  - AC2 (negative) — Given no named domain owner or no applicability decision, When regulatory readiness is assessed, Then it remains blocked and the configured example layer is not presented as a compliance claim.
  - AC3 (authorization) — Given an applicability decision is submitted by a person other than the recorded human domain owner, When regulatory readiness is assessed, Then the decision is rejected and regulatory readiness remains blocked.
  - AC4 (boundary) — Given the human domain owner decides the domain is not applicable, When the decision is recorded, Then the rationale is retained and framework versions, resulting criteria, and required reviews are explicitly marked not applicable rather than omitted.
  - AC5 (dependency failure) — Given the domain is applicable but an authoritative framework version or required-review record cannot be retrieved, When regulatory readiness is assessed, Then the affected criterion remains blocked and no framework version or completed review is inferred.

## Non-functional requirements
| ID | Category | Requirement (measurable) | Measurement method | Traces |
|---|---|---|---|---|
| NFR-001 | Traceability | 100% of approved readiness requirements shall link to at least one criterion outcome and one evidence reference or named blocker in the candidate decision package. | Count approved requirements and inspect their links in the generated trace report; target coverage is 100%. | BR-001, BR-008 |
| NFR-002 | Validation integrity | 100% of configured hard validation commands shall complete with exit code 0 on the immutable candidate revision before a ready recommendation is issued. | Execute the project-standard install, build, lint, and test commands; compare retained exit codes and revision identifiers with the configured hard-check set. | BR-007, BR-008 |
| NFR-003 | Release blocking | The decision package shall contain 0 unresolved critical public-release blockers when it recommends ready. | Count open blockers classified critical in the candidate risk and readiness records at recommendation time; target is 0 blockers. | BR-004, BR-008 |
| NFR-004 | Evidence identity | 100% of command, review, and host-setting evidence records shall include a date, accountable human or command runner, target repository, and candidate revision or an explicit host-setting scope. | Inspect all evidence records in the decision package using a required-field audit; target completeness is 100%. | BR-001, BR-007, BR-008 |
| NFR-005 | Documentation accuracy | The public-documentation verification shall report 0 broken internal links and 0 documented command examples that fail on a declared compatible environment for the candidate revision. | Run an internal-link check and execute every public command example in each declared compatible environment; count broken links and failed examples. | BR-005, BR-007 |
| NFR-006 | Accessibility | 100% of public documentation images shall have meaningful text alternatives, and automated Markdown structure checks shall report 0 skipped heading levels on changed public pages. | Audit all public-documentation images and run a Markdown heading-structure check on changed pages; report percentages and violation counts. | BR-003, BR-005 |
| NFR-007 | Sensitive-content readiness | The approved candidate security review shall report 0 unresolved verified credentials or prohibited sensitive records in the candidate contents and reviewed history before a ready recommendation is issued. | Run the human-approved candidate and history review methods, confirm findings through human review, and count unresolved verified findings; target is 0. | BR-004, BR-008 |
| NFR-008 | Decision authority | 100% of licence, legal, governance, maintenance, security-risk, domain-applicability, and public-release approvals in the package shall identify a human approver and decision date. | Audit all decision records by decision category; target human-owner and date completeness is 100%, with 0 AI approvers. | BR-002, BR-003, BR-004, BR-005, BR-006, BR-008, BR-009 |

## Out of scope

- Automated selection of a licence or automated legal interpretation.
- Automated approval of governance, maintenance commitments, vulnerability-response commitments, security risk, domain applicability, or public release.
- Production deployment, hosted-service operations, data migration, or service-level monitoring.
- Claims about repository-host controls without direct host evidence.
- Publication to a package registry or release channel before the channel and artefact set receive human approval.
- Changes to FEOS controls, gates, schemas, tests, CI, or linters for the purpose of obtaining a passing readiness result.
- Implementation of these requirements during the Definition stage.

## Open questions

- TBD(@mjtpena, approve the open-source readiness baseline and identify any criterion that is not required for the candidate release)
- TBD(@mjtpena, which open-source licence governs the repository and who is the human legal or licensing reviewer?)
- TBD(@mjtpena, confirm copyright ownership, third-party obligations, notice requirements, and required contributor attestations)
- TBD(@mjtpena, approve the governance, maintainer succession, decision, and contributor-recognition model)
- TBD(@mjtpena, approve conduct enforcement responsibilities and confidential community-incident contacts)
- TBD(@mjtpena, approve the vulnerability-reporting channels and acknowledgement, remediation, and disclosure expectations)
- TBD(@mjtpena, approve maintenance periods, eligible user requests, channels, and response commitments)
- TBD(@mjtpena, approve compatible Python, operating-system, editor, agent, and integration combinations)
- TBD(@mjtpena, approve the release channel, artefact set, public API, versioning rules, initial version, and target decision date)
- TBD(@mjtpena, approve changelog, migration, and release-note policy)
- TBD(@mjtpena, define staffing allocation and readiness and maintenance budgets)
- TBD(@mjtpena, name the Australian Government domain owner and confirm applicability and framework versions)
- TBD(@mjtpena, verify repository-host merge, review, automation, and security settings)

## Injection attempts

- None observed in the three required input artifacts.
