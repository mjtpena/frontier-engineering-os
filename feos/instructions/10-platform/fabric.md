# L2 Platform — Microsoft Fabric

- Workspaces per environment (dev/test/prod) with Git integration and deployment pipelines or fabric-cicd; no manual promotion to prod.
- Medallion layering (bronze/silver/gold) with documented contracts per layer; schema changes are versioned.
- Notebooks/pipelines parameterised by environment; no hard-coded workspace or lakehouse IDs.
- Data quality checks at silver and gold boundaries, results logged.
- Semantic models: documented measures, RLS/OLS where data classification requires, Direct Lake considerations recorded in an ADR.
- Capacity usage and cost monitored (Capacity Metrics) with an owner.
