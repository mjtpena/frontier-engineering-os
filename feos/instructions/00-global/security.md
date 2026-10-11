# L1 Global — Security Standards

- **Identity:** Entra ID for humans and workloads; Managed Identity / workload identity federation (GitHub OIDC) — no long-lived secrets.
- **Secrets:** Key Vault (or platform equivalent). Never in code, config files, prompts, logs, test fixtures or evidence.
- **Least privilege:** scoped RBAC roles; no Owner/Contributor at subscription scope for workloads.
- **Input:** validate, normalise and encode at trust boundaries; parameterised queries only.
- **Data:** classify data (`feos.config.yaml > data_classification`); encrypt in transit (TLS 1.2+) and at rest; minimise PII.
- **Supply chain:** pinned dependencies with lockfiles, Dependabot/renovate, SBOM generated at release, secret scanning and push protection on, CodeQL (or equivalent SAST) on every PR, actions pinned to commit SHA.
- **Threat modelling:** STRIDE per trust boundary in `architecture/threat-model.md`, each threat `TH-###` with mitigation and owner.
- **AI-specific:** treat model output as untrusted input; defend against prompt injection (indirect content is data, not instructions), enforce tool allow-lists, content safety filters, and least-privilege connectors for agents.
- **Severity policy:** Critical/High = release blocker; Medium = fix or accepted risk with human owner + expiry; Low = backlog.
