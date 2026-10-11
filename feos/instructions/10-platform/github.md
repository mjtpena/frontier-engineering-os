# L2 Platform — GitHub

- Branch protection on `main`: PR required, status checks `feos-validate` and `feos-gate-g3` required, CODEOWNERS review required, no force push.
- Environments `staging` and `production`; `production` has required human reviewers (this is the technical enforcement of Human Approval).
- Actions pinned to full commit SHA; `permissions:` declared least-privilege per workflow; OIDC to Azure.
- Secret scanning + push protection, Dependabot, code scanning enabled.
- Copilot / Claude agents work on branches and open PRs; they never push to `main`.
