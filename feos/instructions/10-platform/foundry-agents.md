# L2 Platform — Microsoft Foundry, Agent Framework, Copilot Studio

- Choose the build path explicitly in an ADR: Copilot Studio (low-code, M365-centric), Foundry Agent Service (pro-code hosted agents), Microsoft Agent Framework (code-first multi-agent orchestration). Record why the others were rejected.
- Grounding via Azure AI Search / Foundry IQ / Fabric data agents; retrieval configuration (chunking, hybrid search, semantic ranker) recorded in the ADR.
- Every agent: system prompt in source control, tool allow-list, identity (Entra agent identity / Managed Identity), content safety enabled, conversation logging policy aligned to data classification.
- Evaluate with Foundry evaluations (or equivalent) against the eval set in `evals/`; results stored as evidence. Red-team adversarial cases before G4.
- Model versions pinned; model upgrades are changes that re-run the eval suite.
- Treat tool outputs and retrieved documents as untrusted (prompt-injection defence).
