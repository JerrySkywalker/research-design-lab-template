# Conversation-to-repository ingestion

Use this procedure when a long Owner/assistant research discussion contains material worth preserving. It is suitable for Web ChatGPT because it requires a compact provenance reference, not a raw transcript export.

1. Read the repository first: charter, decision log, registers, relevant hypotheses, experiments, sources, and prior syntheses. Do not restate or overwrite existing Owner-adopted state.
2. Create a concise discussion reference in the research log: date/range, participants or roles, topic, and a non-secret conversation reference if available. Record `provenance: Owner/assistant research discussion`. Do not copy a raw chat transcript into the repository.
3. Extract statements into three groups: **OWNER-PROVIDED** facts/constraints and explicit decisions; assistant proposals or summaries; and unresolved alternatives/questions. Attribute each group. Treat an assistant proposal as an inference unless the Owner explicitly adopted it.
4. Compare extracted material to existing records. Add or amend a source, hypothesis, experiment, or log entry only when its statement and provenance are supportable. Preserve conflicting alternatives rather than silently normalizing them.
5. Write a compact synthesis using `SYNTHESIS_TEMPLATE.md`: inputs, facts, inference, gaps, alternatives, and an optional recommendation. Link to conversation reference and affected records.
6. Update registers with only supported IDs/statuses. Do not change `project/` from discussion alone. If an explicit Owner decision exists, record it in the decision log with evidence links; then and only then update the affected adopted project state.
7. Review for accidental private material, credentials, raw transcript text, unsupported claims, and implied promotion. Keep access or provenance limits explicit.

If a statement cannot be distinguished as Owner-provided, assistant-proposed, or unresolved, retain it as unresolved rather than assigning decision status.
