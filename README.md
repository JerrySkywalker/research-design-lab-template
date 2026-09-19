# Research Design Lab Template

An agent-native, executable research project template for keeping research candidates, evidence, code, decisions, and durable assets distinct and traceable.

## State model

This repository is canonical for executable project state. `hypotheses/` contains candidate research; `project/` contains only Owner-adopted design. The lifecycle is hypothesis → evidence → explicit Owner promotion. Results, rankings, and recommendations never select an architecture on their own.

## Directory roles

- `project/` — adopted design, charter, decisions, and verification records.
- `hypotheses/` — candidates and their lifecycle.
- `experiments/` — admitted experiments and compact evidence/provenance.
- `research/`, `sources/`, `methods/` — synthesis, traceable source metadata, and reproducible methods.
- `src/`, `tests/`, `shared/`, `deliverables/` — implementation, verification, small reusable project material, and communication artifacts.
- `generated/` and `scratch/` — ignored, non-authoritative local output and disposable work.

## Storage boundaries

Light generated output may be local. Heavy work uses a machine-local external workspace; paths are examples only and are not canonical research identity. Durable heavyweight assets live in `ResearchLibrary` and are referenced logically:

```yaml
asset_ref: projects/<project>/runs/<run-id>/<artifact>
```

Record source identity, run ID, hashes or output inventory, status, failures, and interpretation boundaries with material evidence.

## Related systems

The Research Vault receives only compact cross-project knowledge and never replaces project evidence. Zotero remains authoritative for bibliography and managed attachments; this repository stores only the metadata needed for traceability.

## Agent-native operation

Agents work within admitted scope, preserve Owner decisions, make claims with explicit type, and keep changes reviewable. Do not introduce middleware, services, databases, or custom tooling without a demonstrated requirement.

## Quick start and template evolution

Create a private repository from this template, define a charter without inventing requirements, admit hypotheses and experiments explicitly, and commit compact decision-relevant evidence. Generated repositories are independent: template changes are versioned, reviewed for applicability, and ported through an explicit branch or PR. No automatic sync, submodule, subtree, or template remote is used.
