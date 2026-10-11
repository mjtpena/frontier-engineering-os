# L2 Platform — Azure

- Infrastructure as Code only (Bicep or Terraform, per `feos.config.yaml > iac`). No portal-only changes; drift is a defect.
- Azure Verified Modules preferred where available.
- Landing zone aligned: workloads in subscriptions/resource groups per environment; naming per Cloud Adoption Framework abbreviations; mandatory tags `owner`, `env`, `costCenter`, `dataClass`.
- Managed Identity for all service-to-service auth; Key Vault with RBAC; private endpoints for data services in non-dev environments.
- Diagnostics to Log Analytics / Application Insights; alerts as code.
- Well-Architected Framework pillars are the architecture review checklist (reliability, security, cost, operational excellence, performance).
- Cost: every architecture includes a monthly estimate with assumptions and a budget alert.
