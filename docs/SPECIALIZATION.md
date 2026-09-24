# Specializing an instance

An instance is an independent project repository, not a branded copy that tracks this template automatically. Specialization establishes project identity, records source provenance, and starts the lifecycle in [UPGRADE.md](UPGRADE.md).

## Establish instance identity and metadata

Replace the template README title/opening, placeholder project identity, example-only onboarding, and any template-specific references with the project's identity. Keep reusable framework sections only when they remain true. Root README becomes `INSTANCE_SPECIALIZED` after specialization: it must not be blindly replaced by a later template README.

Create these two Markdown files at the instance root:

`TEMPLATE_BASELINE.md` is a concise replaceable current-state snapshot:

```markdown
# Template baseline

- Template source: <canonical repository URL or stable identity>
- Generated from: <release> (`<commit>`)
- Generated on: <YYYY-MM-DD>
- Last reviewed: <release> (`<commit>`)
- Reconciled through: <release> (`<commit>`)
- Open delta: <none or link to TEMPLATE_UPGRADES.md>
- Current intentional deviations: <none or concise summary/link>
```

`Generated from` is immutable historical origin. `Last reviewed` is the newest release whose complete delta has been evaluated. `Reconciled through` is the newest release for which every applicable delta has a final disposition, all required changes are merged, and required validation is complete. It means all changes are accounted for, not that the instance equals the template byte-for-byte.

`TEMPLATE_UPGRADES.md` is cumulative and append-oriented. Add a human-readable section for each review with its old/new exact releases, review change, result, and delta table. Keep history there rather than extending the baseline. Do not add a JSON/YAML upgrade manifest or a per-file ownership registry.

## Lifecycle ownership rules

Ownership follows documented path and lifecycle semantics; do not add per-file ownership metadata.

| Path or lifecycle role | Instance ownership and upgrade behavior |
| --- | --- |
| Root README, AGENTS, `.gitignore`, `.gitattributes` | `INSTANCE_SPECIALIZED`. README carries project identity; AGENTS carries local authority; ignore/attribute rules may contain safety or portability rules. Three-way review them, never replace blindly. |
| `project/` | Real charter, adopted design, and decision state are `INSTANCE_OWNED`. The completed charter and decision log become instance-owned at their first real project fact or explicit decision. Preserve append/supersession history. |
| `hypotheses/`, `experiments/`, `sources/` | Blank reusable forms remain `TEMPLATE_OWNED`. Their blank starter `REGISTER.md` files are `BOOTSTRAP_ONLY`; after the first real identifier/row they become `INSTANCE_OWNED`. A template column or instruction is an `ADAPT` candidate, never authority to replace rows. |
| `terminology/` | The blank local term form is `TEMPLATE_OWNED`; the starter register is `BOOTSTRAP_ONLY` until populated. Real local notes and populated register rows are `INSTANCE_OWNED`. Port guidance without replacing project wording or context. |
| `research/` | Workflow documents and blank log/synthesis forms are `TEMPLATE_OWNED`; populated research logs and syntheses are `INSTANCE_OWNED`. |
| `methods/`, `src/`, `tests/`, `shared/`, `deliverables/` | `.gitkeep` is `BOOTSTRAP_ONLY`. Real methods, code, test suites, shared project material, and deliverables are `INSTANCE_OWNED`; a template update does not rewrite them. |
| `generated/`, `scratch/` | Ignored disposable/local outputs are not a template upgrade destination. Their storage boundary is controlled by the specialized `.gitignore`; never force-add or synchronize them. |
| Blank templates and blank registers | Reusable blank source forms are `TEMPLATE_OWNED`; starter artifacts filled in place are `BOOTSTRAP_ONLY` only until their first real research/project content. |
| Evidence manifests | The reusable evidence-manifest template is `TEMPLATE_OWNED`; a concrete evidence manifest, its hashes, and interpretation boundary are `INSTANCE_OWNED` and must never be overwritten or normalized automatically. |

The ownership transition is explicit:

```text
blank hypotheses/REGISTER.md
    BOOTSTRAP_ONLY
        ↓ first real hypothesis
    INSTANCE_OWNED
```

The same transition applies to the experiments and sources registers, `project/CHARTER_TEMPLATE.md` when it becomes an actual charter, `project/DECISION_LOG_TEMPLATE.md` when it holds real decisions, and a research-log template when it becomes a real research log. Content and documented lifecycle semantics control; a populated path does not need an ownership annotation to be protected.

Template changes arrive only through an admitted, reviewable branch or PR. Metadata is durable context, not synchronization machinery.
