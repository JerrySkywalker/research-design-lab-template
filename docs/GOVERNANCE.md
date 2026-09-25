# Research Design Lab governance

This Git-native contract applies to human researchers, agents, automation scripts, and external contributors. An admitted task defines its paths and permitted actions. A branch, commit, or PR makes a proposed change reviewable; it does not grant scientific authority. No agent runtime or permission service is required.

## Classify each mutation

| Class | Use | Review and authority |
| --- | --- | --- |
| `CAPTURE` | Record a provisional source, question, observation, candidate hypothesis, or conversation extract with provenance and uncertainty. | Follow the admitted scope and local review rule. Capture stays provisional even after commit or merge. |
| `ROUTINE_UPDATE` | Fix links, formatting, indexes, or other mechanical/editorial detail without changing meaning or authority. | Check the diff for semantic changes. A routine label cannot admit evidence or change adopted state. |
| `CANONICAL_CHANGE` | Admit traceable evidence, change an interpretation used for research decisions, change project-local terminology meaning, or propose adopted project state or an explicit decision. | Prepare a reviewable diff with provenance. A human reviewer must explicitly accept scientific or semantic changes. Only an explicit Owner decision can adopt a hypothesis, change `project/` state, or alter an Owner decision. |

Classify by effect, not by actor, path, file size, or whether a tool generated the text. Split mixed changes so the canonical part receives its review. If classification is uncertain, keep the material provisional and request human review. Existing experiment and decision procedures still apply.

## Authority and state

1. **Generated output** is a tool or agent product in `generated/`, external work space, or a proposed diff. Retain producer, inputs, and limits. It is not evidence by default.
2. **Evidence** is a traceable observation or output deliberately admitted under repository rules, with provenance and limitations. A Git commit or successful run alone does not admit it.
3. **Interpretation** explains what admitted evidence may mean. Identify inference and uncertainty; it is not a decision.
4. **Decision** is explicit Owner adoption, rejection, or deferral recorded with supporting evidence and scope in the decision log.

No transition follows automatically from the previous state, a passing validator, a merge, or a persuasive synthesis. Agents and contributors may propose, draft, analyze, run admitted work, and prepare diffs. Automation may validate and perform admitted mechanical maintenance. Neither may independently admit evidence, adopt a hypothesis, change `project/`, alter an Owner decision, or canonicalize a Vault term. Project-local terminology remains local unless separately reviewed for Vault promotion.

Candidate hypotheses, research notes, and generated outputs may remain provisional. Living registers, logs, navigation, and syntheses are reviewed mutable state. Explicit decisions, sealed evidence and run receipts, and release/audit receipts are append-oriented: correct them with a linked superseding record, not a silent rewrite. Git history alone is not a substitute for visible supersession. A failed or blocked run remains recorded with its limits.

## Concurrent work and nested instructions

Use ordinary Git branches or worktrees, commits, reviewable diffs or PRs, and merge conflict resolution. When concurrent edits conflict on meaning or authority, preserve both proposals and obtain human semantic resolution before merging. A clean textual merge does not prove semantic agreement.

A nested `AGENTS.md` may narrow paths, actions, and review requirements for its subtree. It cannot weaken this repository's authority, evidence, provenance, review, or safety rules. Resolve contradictory instructions at the stricter boundary and escalate an unresolved authority conflict to the Owner or human reviewer.

For conversation capture, follow [the ingestion procedure](../research/CONVERSATION_INGESTION.md). For evidence, follow the [run manifest](../experiments/RUN_EVIDENCE_MANIFEST_TEMPLATE.yaml); for decisions, follow the [decision log](../project/DECISION_LOG_TEMPLATE.md).
