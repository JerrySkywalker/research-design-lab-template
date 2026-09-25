# External integration boundaries

This Lab remains an ordinary, portable Git repository. External bibliography, asset storage, editors, and agent providers may be unavailable without invalidating its project state or validator. Tools can produce candidates and output; they cannot admit evidence, interpret it as an Owner decision, or change adopted project state on their own.

## Bibliography and project source use

Zotero owns managed bibliographic records and attachments. The Lab owns project-local screening, source use, and provenance. A citekey is a convenient citation label, not a guaranteed stable identity. A Zotero item key points to a managed record, not to the work universally. A DOI identifies a registered work where available; a URL, page, archive reference, or other locator identifies the source consulted. Record available identities and access limits in `sources/`, and never invent a missing identifier. A Vault literature note may synthesize cross-project meaning, but does not replace the Lab's local source-use record.

No Zotero plugin is mandatory. If a specialized project uses another bibliography manager, retain the same separation between managed records/attachments and project-local use, and retain a portable DOI or locator. Do not put another provider's ID into a field labeled as a Zotero item key.

## Durable assets

An `asset_ref` is a logical durable identity, never an absolute host path. Its provider may be a local library, cloud folder, or future storage system; no provider is required by this template. A tracked run manifest should connect a referenced asset to its producer run, hash and byte size when meaningful, relevant historical revision, reproduction or retrieval steps, and interpretation limits. A moved asset can keep its logical identity if its content and provenance remain verifiable; changed content requires a new recorded hash or revision. Do not commit bulk material solely to make a provider reachable.

## Editor, host, and agent substitution

Markdown, relative links, YAML manifests, and Git history are the durable contract. Obsidian is optional for a Lab; any editor may read the files. Host paths map the logical source, work/build, cache, artifact, and durable-asset roles locally and never become canonical IDs.

Web ChatGPT, Codex, local models, and future agents follow `AGENTS.md` and `docs/GOVERNANCE.md` equally. Provider choice does not change `CAPTURE`, `ROUTINE_UPDATE`, or `CANONICAL_CHANGE` authority, Owner decision gates, evidence provenance, or conflict review. No agent runtime, MCP endpoint, automatic Lab-to-Vault promotion, or synchronization is required.
