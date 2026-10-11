# L1 Global — Responsible AI

Applies to any feature that calls an AI model or agent.

1. **Impact assessment** (`templates/rai-impact-assessment.md`) completed in S3, covering intended use, misuse, affected stakeholders, failure modes, and human oversight.
2. **Evaluation set**: ≥ 50 representative cases incl. adversarial, out-of-scope and fairness slices, versioned under `evals/`.
3. **Metrics and thresholds** declared in `feos/orchestration/evaluations/ai-quality.yaml` before implementation (groundedness, relevance, task success, safety defect rate, jailbreak resistance). Defaults are starting points and MUST be calibrated by a human.
4. **Grounding**: answers that assert enterprise facts must be grounded in retrieved sources and cite them; abstain when retrieval is empty.
5. **Human oversight**: decisions with legal, financial, employment, health or safety effect require human-in-the-loop.
6. **Transparency**: users are told they are interacting with AI; outputs are labelled as AI-generated where relevant.
7. **Monitoring**: production telemetry for quality drift, safety incidents and cost, with an owner.
