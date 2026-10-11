# Instruction Layers and Precedence

Layers are loaded in this order; **later layers specialise earlier ones but may only override them through a recorded exception**
(`templates/exception-request.md`, approved by the layer owner in `raci.yaml`).

| Layer | Path | Owner | Example |
|---|---|---|---|
| L0 Constitution | `feos/constitution.md` | Engineering leadership | Humans own approval |
| L1 Global | `feos/instructions/00-global/` | Engineering leadership | Secure by default |
| L2 Platform | `feos/instructions/10-platform/` | Platform owners | Azure: Managed Identity |
| L3 Domain | `feos/instructions/20-domain/` | Domain lead | Government: PSPF/ISM alignment |
| L4 Project | `feos/instructions/30-project/project.md` | Tech lead | Use .NET 9 + Container Apps |
| L5 Task | `plan/backlog.yaml` task `instructions` | Planner (human-reviewed) | Implement refund endpoint |

Conflict rule: if two layers conflict and no approved exception exists, the **stricter** rule applies and the agent records the conflict in its output under `## Conflicts`.

Agents load only the layers relevant to their work (declared in `feos/orchestration/agents.manifest.yaml > instruction_layers`), to keep context small.
Platform files are selected by `feos.config.yaml > platforms`.
