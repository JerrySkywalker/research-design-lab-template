# Research Design Lab Agent Contract

## Canonical state

This repository is canonical for this project's executable research state. The Research Vault is a knowledge consumer and promotion destination, not a replacement for project evidence, code, or decisions.

`hypotheses/` contains candidate research. `project/` contains explicitly Owner-adopted design only. No result, directory name, score, ranking, recommendation, or synthesis promotes a hypothesis. Promotion requires an explicit Owner decision and traceable evidence.

## Claim and experiment discipline

Material statements distinguish **SOURCE FACT**, **OWNER-PROVIDED**, **INFERENCE**, **ASSUMPTION**, **DESIGN CHOICE**, and **CALCULATION / RESULT**. Unknowns remain explicit.

Every material experiment or run records a stable identifier, method/configuration reference, input/source identity, relevant tool or environment versions, output inventory or hash where relevant, status, failure or block record, and interpretation boundary. Preserve failures. Do not overwrite sealed evidence.

## Git and output boundary

Commit source code, methods, configuration, tests, source metadata, compact manifests, compact canonical datasets, selected decision-relevant figures, reviews, and verification/decision records. Do not normally commit raw parameter sweeps, dense histories, large data or simulations, tool databases, large media, or rebuildable output.

`generated/` is ignored local output. `scratch/` is ignored disposable work. Neither is authoritative until compact evidence is deliberately promoted; never force-add either merely because a run succeeded.

Heavy work uses a machine-local external workspace. A local convention may be documented as an example, but tracked records use relative paths, run IDs, and logical `asset_ref` values rather than machine paths.

## Durable assets, Zotero, and vault promotion

Durable heavyweight assets belong in `ResearchLibrary`. For example:

```yaml
asset_ref: projects/<project>/runs/<run-id>/<artifact>
```

Tracked evidence records an asset reference, producer run, content hash, size, reproduction instructions, and interpretation boundary where meaningful.

Zotero owns bibliography and managed attachments. Store only citation/source metadata needed for traceability. Promote compact knowledge beyond project execution to the Research Vault; never duplicate raw project state.

## Agent discipline

Agents mutate only admitted scope, preserve Owner decisions, and never select an architecture by implication. Do not add credentials, canonical machine-specific paths, or middleware without demonstrated need.
