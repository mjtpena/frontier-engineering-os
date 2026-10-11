# L1 Global — Documentation & Writing

- Docs live next to code, in Markdown, updated in the same PR as the change.
- Every artifact starts with front-matter: `id`, `title`, `status (draft|review|approved|superseded)`, `owner` (human), `version`, `trace` (parent IDs).
- Write for a reader who was not in the room: decisions, rationale, alternatives.
- Mark unknowns as `TBD(owner, question)`. Never invent numbers, versions, SLAs, prices or citations.
- Diagrams as code (Mermaid) so they diff.
