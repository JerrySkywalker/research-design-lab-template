# Safe instance upgrade

## Purpose and boundary

A specialized Design Lab instance reviews an upgrade as a semantic three-way comparison:

```text
previous exact template release + new exact template release + current specialized instance
```

Use ordinary Git diffs, an admitted review branch or PR, and human/agent semantic review. Shared Git ancestry is not required. This contract creates no updater, automatic synchronization, custom merge engine, machine-readable manifest, registry, or migration service. A new template release never authorizes a project mutation.

## Shared lifecycle vocabulary

Use only these ownership roles:

| Role | Meaning and default review behavior |
| --- | --- |
| `TEMPLATE_OWNED` | Reusable guidance, blank form, or generic validator. Normally propose `PORT`; use `ADAPT` if local intent diverged. |
| `INSTANCE_OWNED` | Real research, project, evidence, code, or decision state. Preserve it; a template delta never replaces it. |
| `INSTANCE_SPECIALIZED` | Template-derived identity, governance, or configuration intentionally adapted locally. Use semantic three-way review, normally `ADAPT`. |
| `BOOTSTRAP_ONLY` | Seed/onboarding material whose original lifecycle ends at or after specialization. Do not reintroduce or refresh it automatically. |

Do not add per-file ownership metadata. Derive ownership from documented path, content, and lifecycle semantics. In particular, a populated register or completed charter becomes instance-owned even though it started from a blank template path.

Use only these final delta dispositions:

| Final disposition | Meaning |
| --- | --- |
| `PORT` | Apply the template intent substantially as released. |
| `ADAPT` | Apply the new intent while preserving instance identity, governance, configuration, or project state. |
| `SKIP` | Explicitly decide not to adopt the reviewed template change. This is final and must have a rationale. |
| `ALREADY_PRESENT` | Equivalent intent already exists in the instance; cite evidence. |

An unresolved row is not a fifth disposition: leave its disposition blank or mark it pending review in a separate issue/gate field. It keeps the review open. `SKIP` is final; once every row is final and required work/validation is complete, it may coexist with reconciliation.

## Metadata

Instances create `TEMPLATE_BASELINE.md` and `TEMPLATE_UPGRADES.md` at specialization; see [SPECIALIZATION.md](SPECIALIZATION.md).

- **Generated from** is the immutable release and exact commit used to create the instance. It never advances.
- **Last reviewed** is the newest exact template release against which the complete delta has been evaluated. It may advance while work remains open.
- **Reconciled through** is the newest exact template release for which every applicable delta since the previous reconciliation point has a final disposition, all required instance changes are merged, and required validation is complete. It means accounted for, not identical.

For example, `Generated from: v0.2.0`, `Last reviewed: v0.4.0`, and `Reconciled through: v0.3.0` is valid while v0.4 work remains unresolved or unmerged. A final documented `SKIP` can still allow the reconciliation point to advance.

Keep the baseline small. Store cumulative detail in `TEMPLATE_UPGRADES.md`:

```markdown
## Review <old release> -> <new release> — <YYYY-MM-DD>

- Previous reconciliation point: <release> (`<commit>`)
- Reviewed release: <release> (`<commit>`)
- Review result: OPEN | CLOSED | CLOSED_WITH_DEVIATIONS
- Resulting reconciliation point: <release and commit, or unchanged>
- Review change: <PR and/or merge commit>

| Template change | Ownership | Disposition | Instance action | Issue / Owner gate | Rationale / evidence |
| --- | --- | --- | --- | --- | --- |
```

`OPEN`, `CLOSED`, and `CLOSED_WITH_DEVIATIONS` describe the whole review, not individual dispositions. A closed review with one or more `SKIP` rows is `CLOSED_WITH_DEVIATIONS`; no JSON/YAML companion manifest is required or permitted by this contract.

## Design Lab review rules

- `project/` holds Owner-adopted state. A real charter, decision log, or adopted design is instance-owned and must not be replaced, rewritten, or reinterpreted by an upgrade.
- Populated hypotheses, experiments, sources, research logs, syntheses, evidence manifests, methods, source code, tests, shared material, and deliverables are instance-owned. Preserve them byte-for-byte unless an admitted reviewed adaptation explicitly names the change.
- Populated `terminology/` notes and register are instance-owned. The blank local term form and generic terminology guidance are template-owned review candidates; do not overwrite local wording or silently follow changed Vault terms.
- Reusable blank forms and generic workflow documents are template-owned. A new form/workflow can be ported for future use without altering real state created from an older form.
- A populated starter register is instance-owned. Review a later template column/instruction as `ADAPT`, preserving every existing row and identifier.
- README and AGENTS require specialization-aware review. Preserve project identity and local Owner/agent authority; never restore template onboarding or pull v0.5 governance forward.
- The validator is template-owned implementation, but a ported validator must tolerate legitimate specialization. It must not require blank registers, template README identity, generic AGENTS text, or template-only research state.
- `.gitignore` and `.gitattributes` are specialized safety/portability rules. Merge generic intent semantically while preserving local rules. `generated/` and `scratch/` remain ignored/local and are never synchronized.
- Consumed `.gitkeep`, quick-start prose, blank placeholders, and template identity are bootstrap-only. Do not restore them to a specialized project.

## Review sequence and stop conditions

1. Verify admitted instance scope, known-clean state, baseline/history metadata, local governance, and exact old/new template commits.
2. Inventory the complete old-to-new template delta, including additions, deletions, renames, mode changes, validator changes, and documentation semantics.
3. Classify each coherent delta by its current lifecycle role and record it in the cumulative table.
4. Implement only finalizable `PORT` and `ADAPT` rows on a review branch. Preserve instance-owned state and document `SKIP`/`ALREADY_PRESENT` evidence.
5. Run instance-appropriate validation and preservation assertions. A template validator is not proof that a project upgrade is complete.
6. Advance `Reconciled through` only after every applicable row is final, required changes are merged, and required validation is complete. If any row remains unresolved, retain an open review and leave reconciliation unchanged.

Stop and leave the review open when exact releases cannot be proven, the full delta is not inventoried, project state is unexplained, an Owner gate is unresolved, preservation checks fail, or a proposed change requires a data migration, custom merge engine, or automation outside this contract.

Owner review is required for explicit Owner decisions, adopted project state, identity/legal posture, local AGENTS authority, safety/storage/provenance boundaries, a normative-policy `SKIP`, or a destructive/lossy change to instance-owned material.
