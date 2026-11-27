# Optional Formal Mathematics profile

See the portal for [released Core Pair compatibility](https://github.com/JerrySkywalker/ResearchFabric/tree/main/compatibility).

Use the profile when a hypothesis depends on definitions or claims that benefit from machine checking. The ordinary Design Lab setup and validators use Git and Python and do not require Lean, Elan, Mathlib, an editor plugin, or a Vault connection.

## Start with an example

1. Read the [synthetic Blueprint](../examples/formal-mathematics/BLUEPRINT.md) and [verification method](../examples/formal-mathematics/METHOD.md).
2. Install user-level [Elan](https://github.com/leanprover/elan) and make its bin directory available in a fresh shell. Git, Python 3.11 or later and a working TLS connection suffice for the example. The Lean editor extension is optional.
3. From a fresh clone, enter `examples/formal-mathematics/src/lean`. Run `lean --version` and `lake --version` from the package so Elan selects its pinned toolchain.
4. Run `lake exe cache get Mathlib.Tactic.Ring`, then `python verify.py`. The checker builds the accepted target, runs the trusted lock, and records the observed transitive axioms. Run `python verify.py --self-test` in a disposable copy for the documented rejection cases.
5. To opt in on an admitted branch of a project, copy or adapt the package under `src/lean/`. Put the project's Blueprint under `research/mathematics/`, the verification method under `methods/`, and the admitted run record under `experiments/`. Replace the synthetic names, lock and fixture; retain the toolchain, reviewed dependency resolution and ignore rules.

The package's `FormalExample.lean` explicitly imports its accepted topic modules. `Drafts/` and any `Challenges/` remain outside that import closure. The project's research DAG links claims, definitions, assumptions and evidence; the Lean import DAG orders code modules. A research claim can depend on a reviewed result without importing its exploratory proofs.

## Setup and troubleshooting

Use separate native clones and caches on Windows and Linux, including on an existing WSL distro. In WSL, clone/build on the Linux filesystem and install Linux Elan there. Do not share `.lake` or the Mathlib cache between Windows and WSL. Quote the checkout path when it contains spaces.

Commit `lean-toolchain`, Lake configuration and `lake-manifest.json`. Run `lake update` only as a reviewed dependency change; compare the full transitive lock, retest the statement and consumer imports, and note compatibility changes. A fresh checkout needs Git access to the pinned repositories and the toolchain download. The [Mathlib cache](https://github.com/leanprover-community/mathlib4/blob/v4.36.0/Cache/README.md) accelerates builds. Offline reuse requires an already installed toolchain and materialized matching dependencies and build cache. If downloading fails, check the official endpoints, TLS trust and whether the proxy is configured in the current shell. Record the status code and tool versions with any authorization headers and proxy credentials removed.

Keep `.lake`, cache and logs out of Git. Retain compact reviewed outputs or a logical artifact ID and hash. To reclaim space after a run, remove the disposable checkout and its local cache when no other process uses them. Avoid deleting shared global toolchains or caches.

## Review and promotion

Use the existing evidence, interpretation and decision lifecycle. A formal check says the accepted declaration has the reviewed type and permitted dependency closure under the named toolchain and trust assumptions. A human reviews what the locked statement means and whether the run is admissible. An Owner separately decides what the project adopts.

Semantic promotion proposes a reviewed explanatory note in the Vault with source context and an exact repository, commit, path and declaration. Formal promotion separately proposes original, reusable code in an independent Lake library or upstream. Preserve the originating proof and evidence, check license and confidentiality, review public surface and assumptions, and verify clean downstream Lake imports pinned to an exact revision. The source and the note evolve independently.

For populated instances, use the [three-way upgrade process](UPGRADE.md). Port reusable instructions or skip the optional scaffold with a documented rationale. Adapt specialized README or ignore rules only when wanted. Keep existing code, claims, manifests, evidence, ownership and Git modes. Accepting a template revision does not opt a project in to Lean.
