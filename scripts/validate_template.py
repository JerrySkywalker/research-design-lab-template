#!/usr/bin/env python3
"""Portable public Design Lab template checks; no instance policy or science gate."""

from __future__ import annotations

import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = (
    "AGENTS.md", "README.md", "CHANGELOG.md", "CONTRIBUTING.md", "SECURITY.md",
    ".gitignore", ".github/workflows/template-checks.yml", "docs/SPECIALIZATION.md",
    "docs/UPGRADE.md", "docs/TERMINOLOGY.md", "docs/GOVERNANCE.md",
    "docs/INTEGRATIONS.md", "docs/RELEASING.md", "tests/fixtures/v0.2-instance-lifecycle.md",
    "tests/validate-template.ps1", "scripts/validate_template.py",
    "terminology/REGISTER.md", "terminology/LOCAL_TERM_TEMPLATE.md",
    "project/CHARTER_TEMPLATE.md", "project/DECISION_LOG_TEMPLATE.md",
    "hypotheses/REGISTER.md", "hypotheses/HYPOTHESIS_TEMPLATE.md",
    "experiments/REGISTER.md", "experiments/EXPERIMENT_TEMPLATE.md",
    "experiments/RUN_EVIDENCE_MANIFEST_TEMPLATE.yaml",
    "sources/REGISTER.md", "sources/SOURCE_TEMPLATE.md",
    "research/RESEARCH_LOG_TEMPLATE.md", "research/SYNTHESIS_TEMPLATE.md",
    "research/CONVERSATION_INGESTION.md", "research/PRIOR_ART_WORKFLOW.md",
)
LIFECYCLE_TERMS = (
    "TEMPLATE_OWNED", "INSTANCE_OWNED", "INSTANCE_SPECIALIZED", "BOOTSTRAP_ONLY",
    "PORT", "ADAPT", "SKIP", "ALREADY_PRESENT",
    "Generated from", "Last reviewed", "Reconciled through",
)
IGNORED = (
    "generated/validator-probe.txt", "scratch/validator-probe.txt",
    "cache/validator-probe.txt", "work/validator-probe.txt",
    "research.local.toml", ".env", "validator-probe.pem", "validator-probe.key",
)
EXTERNAL_HEAVY = {".zip", ".7z", ".tar", ".gz", ".sqlite", ".db", ".h5", ".hdf5", ".parquet", ".mp4", ".mov", ".avi"}
SECRET_ASSIGNMENT = re.compile(
    r"^\s*(?:[A-Z0-9_]*?(?:TOKEN|SECRET|PASSWORD|API_KEY)|aws_access_key_id)\s*[:=]\s*(?!<)(?!TBD)(?!none\b)(?!not-applicable\b).+",
    re.IGNORECASE | re.MULTILINE,
)
ABSOLUTE_USER_PATH = re.compile(r"(?:[A-Z]:\\Users\\|/home/[^/]+/|/Users/[^/]+/)", re.IGNORECASE)
SECRET_MARKERS = (
    re.compile(r"-----BEGIN (?:[A-Z0-9]+ )*PRIVATE KEY-----"),
    re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    re.compile(r"\bghp_[A-Za-z0-9]{36}\b"),
    re.compile(r"\bsk-(?:proj-)?[A-Za-z0-9_-]{20,}\b"),
)


def git(*args: str, check: bool = True) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, check=check)


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def main() -> None:
    failures: list[str] = []
    for path in REQUIRED:
        if not (ROOT / path).is_file():
            failures.append(f"Missing required template contract file: {path}")

    if not failures:
        upgrade = read("docs/UPGRADE.md")
        specialization = read("docs/SPECIALIZATION.md")
        fixture = read("tests/fixtures/v0.2-instance-lifecycle.md")
        for term in LIFECYCLE_TERMS:
            if term not in upgrade:
                failures.append(f"Upgrade contract missing lifecycle term: {term}")
        for term in ("TEMPLATE_BASELINE.md", "TEMPLATE_UPGRADES.md", "per-file ownership metadata"):
            if term not in specialization:
                failures.append(f"Specialization contract missing lifecycle boundary: {term}")
        for term in ("020fc7343e8bb7ec7182b3898c75ec7fc03ba447", "OS-local temporary directory", "Formal execution"):
            if term not in fixture:
                failures.append(f"Synthetic scenario definition is incomplete: {term}")
        if "JSON/YAML" not in upgrade:
            failures.append("Upgrade contract does not prohibit a machine-readable upgrade manifest.")
        governance = read("docs/GOVERNANCE.md")
        for term in ("CAPTURE", "ROUTINE_UPDATE", "CANONICAL_CHANGE", "Generated output", "Evidence", "Interpretation", "Decision", "nested `AGENTS.md`"):
            if term not in governance:
                failures.append(f"Governance contract missing: {term}")
        term_guide = read("docs/TERMINOLOGY.md")
        term_form = read("terminology/LOCAL_TERM_TEMPLATE.md")
        if "project-local" not in term_guide:
            failures.append("Terminology guide missing project-local authority.")
        for term in ("Canonical Vault repository", "Canonical Vault note", "Canonical revision used", "Promotion review"):
            if term not in term_form:
                failures.append(f"Local term form missing: {term}")

    ignore = read(".gitignore")
    for entry in ("/generated/", "/scratch/", "/cache/", "/work/", "research.local.toml", ".env", "*.pem", "*.key"):
        if entry not in ignore:
            failures.append(f".gitignore missing: {entry}")
    for path in IGNORED:
        if git("check-ignore", "--quiet", "--", path, check=False).returncode:
            failures.append(f"Documented ignored path is not ignored: {path}")

    tracked = sorted(path.decode("utf-8") for path in git("ls-files", "-z").stdout.split(b"\0") if path)
    generated = [path for path in tracked if path.startswith(("generated/", "scratch/", "cache/", "work/"))]
    if generated:
        failures.append(f"Generated/cache/work file(s) are tracked: {', '.join(generated)}")
    heavy = [path for path in tracked if Path(path).suffix.lower() in EXTERNAL_HEAVY]
    if heavy:
        failures.append(f"External-heavy material is tracked: {', '.join(heavy)}")
    large = [path for path in tracked if (ROOT / path).is_file() and (ROOT / path).stat().st_size > 1024 * 1024]
    if large:
        print("REVIEW: tracked material over 1 MiB requires documented value, provenance, and repository-growth review: " + ", ".join(large))

    for path in tracked:
        if path in {"tests/validate-template.ps1", "scripts/validate_template.py"}:
            continue
        if Path(path).suffix.lower() not in {".md", ".yaml", ".yml", ".ps1", ".txt"} and path not in {"README.md", "AGENTS.md", ".gitignore"}:
            continue
        content = read(path)
        if SECRET_ASSIGNMENT.search(content):
            failures.append(f"Possible credential assignment in: {path}")
        if ABSOLUTE_USER_PATH.search(content):
            failures.append(f"Private absolute path in: {path}")
        for marker in SECRET_MARKERS:
            if marker.search(content):
                failures.append(f"Possible secret material in: {path}")

    for path, term in (
        ("README.md", "Owner decision"),
        ("README.md", "assistant recommendation"),
        ("research/CONVERSATION_INGESTION.md", "raw chat transcript"),
        ("research/PRIOR_ART_WORKFLOW.md", "access limitations"),
        ("experiments/RUN_EVIDENCE_MANIFEST_TEMPLATE.yaml", "interpretation_boundary"),
    ):
        if term.lower() not in read(path).lower():
            failures.append(f"Required generic safety wording missing: {path} [{term}]")

    if failures:
        for failure in failures:
            print(f"FAIL: {failure}")
        raise SystemExit(1)
    print(f"PASS: {len(REQUIRED)} required contract files; ignored boundaries, public-safety scan, size scan, and generic-state checks passed.")


if __name__ == "__main__":
    main()
