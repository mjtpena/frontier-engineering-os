# L2 Platform — GitHub

- Branch protection on `main`: PR required, status check `feos-validate` required, CODEOWNERS review required, no force push.
  `feos-gate-g3` is not produced by any workflow yet: TBD(tech-lead, add a CI job that runs G3 or drop this check) — requiring a check that never reports blocks every merge.
- Environments `staging` and `production`; `production` has required human reviewers (this is the technical enforcement of Human Approval).
- Actions pinned to full commit SHA; `permissions:` declared least-privilege per workflow; OIDC to Azure.
- Secret scanning + push protection, Dependabot, code scanning enabled.
- Copilot / Claude agents work on branches and open PRs; they never push to `main`.
