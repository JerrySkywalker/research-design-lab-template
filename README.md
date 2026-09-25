# Research Design Lab Template

An intentionally small, agent-native starting point for executable research. It separates candidate research, evidence, and explicit Owner-adopted project state so a new project can begin work without inheriting a domain or an architecture.

## Start a new project

1. Create a new repository from this template and replace this README's title and opening paragraph with the project's private identity. Do not retain `Research Design Lab Template` as a second title or copy the generic introduction below a project-specific introduction.
2. Create the concise `TEMPLATE_BASELINE.md` and cumulative `TEMPLATE_UPGRADES.md` described in [specialization](docs/SPECIALIZATION.md). They record provenance and review state; they are not a continuing link or synchronization mechanism.
3. Complete `project/CHARTER_TEMPLATE.md` as a project charter. Keep unknowns as unknowns.
4. Add candidates to `hypotheses/REGISTER.md`; admit research or experiments through their templates before treating an output as evidence.
5. Keep compact, reviewable evidence in the repository and keep generated or heavyweight material at the storage boundary described below.

Framework sections that may remain after specialization are **State model**, **Directory roles**, **Storage boundaries**, and **Working with agents**. Replace any template branding, placeholder project name, template quick-start text, and example-only identity content. Delete instructions that no longer fit rather than leaving two competing repository identities.

Use [safe instance upgrades](docs/UPGRADE.md) when reviewing a later template release. It defines the shared ownership roles, exact version semantics, four final delta dispositions, and the rule that populated project research is never overwritten by a template upgrade.

## State model

`question -> hypothesis -> admitted experiment/research -> evidence -> interpretation -> Owner decision -> adopted project state`

Each transition must remain traceable. Evidence does not automatically become design. An assistant recommendation, score, ranking, or synthesis is not an Owner decision. Failed and blocked work remains evidence, with its limits recorded. A synthesis can recommend a next step but cannot promote a candidate. Only an explicit Owner decision, linked to its supporting evidence, can place adopted state in `project/`.

## Directory roles

- `project/` — Owner-adopted charter, decisions, and design state only.
- `hypotheses/` — candidate research and its register.
- `experiments/` — admitted research/experiment records and compact evidence manifests.
- `research/` — research log, conversation ingestion, prior-art workflow, and syntheses.
- `sources/` — source metadata and screening state; Zotero remains authoritative for managed bibliography and attachments.
- `terminology/` — project-local bilingual terms, optional canonical Vault references, and promotion history.
- `methods/`, `src/`, `tests/`, `shared/`, `deliverables/` — reproducible methods, implementation, checks, small reusable material, and communication artifacts.

The starter files are templates, not assertions that a project has a mission, a hypothesis, a method, a result, or a chosen design.

Use [project terminology guidance](docs/TERMINOLOGY.md) for local wording, optional Git-native Vault references, and explicit promotion. A project works without a mounted or live Vault.

See [external integration boundaries](docs/INTEGRATIONS.md) for bibliography identifiers, durable asset provenance, editor/host portability, and provider-neutral agents.

## Storage boundaries

| Kind | Location | Commit rule |
| --- | --- | --- |
| Light generated output | `<repo>/generated/` | Ignored and non-authoritative; promote only compact, deliberate evidence. |
| Heavy work | Machine-local external work root | Do not put machine paths in tracked records; record method, run ID, and logical references. |
| Durable large asset | `ResearchLibrary` | Reference logically, for example `projects/<project>/runs/<run-id>/<artifact>`. |
| Tracked evidence | Repository | Commit compact provenance, hashes/inventory, interpretation boundary, and decision-relevant outputs. |

Do not require Git LFS or an asset manager. `scratch/` is ignored disposable work. Do not force-add ignored output merely because a run completed.

Use portable roles: **source** is reviewable Git state; **work/build** is disposable execution; **cache** is rebuildable data; **artifact** holds retained run receipts and audit evidence; **durable asset** holds large material whose logical reference and provenance belong in Git. Each host maps these roles locally. The repository must not depend on a particular drive, cloud folder, or mounted provider.

Tracked source, methods, configuration, tests, source metadata, compact manifests, and selected decision-relevant evidence are normal Git material. A larger compact figure or dataset requires deliberate review for value, provenance, and repository-growth cost; size alone does not make it invalid evidence. Raw sweeps, dense histories, tool databases, archives, videos, and rebuildable bulk output are external-heavy material. Record a logical `asset_ref`, producer run, hash and size when meaningful, and reproduction or retrieval context. Keep generated and cache data out of canonical Git state. No asset service or Git LFS is required.

## Working with agents and conversations

Read [research/CONVERSATION_INGESTION.md](research/CONVERSATION_INGESTION.md) before converting a research conversation into project state. It preserves Owner-provided statements and unresolved alternatives while avoiding raw transcript copies. Read [research/PRIOR_ART_WORKFLOW.md](research/PRIOR_ART_WORKFLOW.md) before a prior-art pass.

The [governance contract](docs/GOVERNANCE.md) defines `CAPTURE`, `ROUTINE_UPDATE`, and `CANONICAL_CHANGE`, the human and Owner review gates, evidence and decision boundaries, and ordinary Git handling for concurrent work.

Claims use explicit labels: **SOURCE FACT**, **OWNER-PROVIDED**, **INFERENCE**, **ASSUMPTION**, **DESIGN CHOICE**, or **CALCULATION / RESULT**. Agents work within admitted scope, preserve Owner decisions, and do not add services, databases, RAG, middleware, or custom workflow tooling without a demonstrated requirement.

## Validation

Before proposing source-template changes, run `python scripts/validate_template.py` with Python 3 and Git. The existing `pwsh -File tests/validate-template.ps1` entry point remains available and is checked in source CI. These are small public-template contract checks, not workflow, instance-policy, migration, or scientific validity engines. A specialized project may adapt or replace them for its own paths and policy.

Template source contributors should read [contributing guidance](CONTRIBUTING.md), the [changelog](CHANGELOG.md), and the [maintainer release procedure](docs/RELEASING.md). The source repository runs template checks on Windows and Linux; a generated instance may replace that source-only CI with its own checks.
