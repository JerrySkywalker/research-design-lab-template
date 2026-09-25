# Contributing to the template

Open an issue or pull request for reusable template defects and documentation improvements. Keep real project data, credentials, private paths, managed attachments, generated output, and heavyweight assets out of this public template. Actual research repositories are outside this template's review scope.

State the proposed change, released baseline, affected contract, and validation evidence. Run `pwsh -File tests/validate-template.ps1`; for pair changes, also check the Vault contract at exact heads. Attach only synthetic or cleared evidence. A passing validator does not admit evidence, prove a scientific claim, or make an Owner decision.

The source repository's CI checks this public template on Windows and Linux. It runs only in `JerrySkywalker/research-design-lab-template`; a repository created from the template should replace or remove the inherited source-template workflow when it defines its own checks. For versioned pair releases, follow [the maintainer release procedure](docs/RELEASING.md).
