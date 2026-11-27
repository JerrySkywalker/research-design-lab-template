"""Build and audit the reviewed synthetic Formal Mathematics sample."""

import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "FormalExample/OddSum.lean"
LIBRARY = ROOT / "FormalExample.lean"
EVIDENCE = ROOT / "review/Evidence.yaml"
MATHLIB_REV = "fc4f59e577feb1a4956671bc04ac18aaaf8cd842"
TOOLCHAIN = "leanprover/lean4:v4.36.0"
AXIOMS = ["propext", "Classical.choice", "Quot.sound"]


def digest(path):
    return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def run(*command):
    # Elan installs executable shims on both supported platforms.
    result = subprocess.run(
        command, cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
        check=False, encoding="utf-8", errors="replace",
    )
    if result.returncode:
        raise ValueError(f"{' '.join(command)} exited {result.returncode}\n{result.stdout}")
    return result.stdout.strip()


def check_materialized_dependencies(packages, required=False):
    for name, package in packages.items():
        package_dir = ROOT / ".lake/packages" / name
        if not required and not package_dir.exists():
            continue
        if run("git", "-C", str(package_dir), "rev-parse", "HEAD") != package["rev"]:
            raise ValueError(f"resolved dependency does not match lock: {name}")
        if run("git", "-C", str(package_dir), "status", "--porcelain"):
            raise ValueError(f"dirty dependency: {name}")


def audit():
    evidence = json.loads(EVIDENCE.read_text(encoding="utf-8"))
    formal = evidence["formal"]
    if (
        formal["claim"] != "ODD-SUM/r1"
        or formal["lock_rev"] != formal["claim"]
        or formal["source_path"] != "FormalExample/OddSum.lean"
        or formal["declaration"] != "FormalExample.oddSum_eq_square"
        or not formal["source_provenance"].strip()
        or not formal["artifact_ref"].startswith("projects/synthetic-odd-sum/runs/")
        or formal["approved_axioms"] != AXIOMS
        or formal["review_state"] != "PENDING"
    ):
        raise ValueError("missing or inconsistent synthetic evidence provenance")

    if (ROOT / "lean-toolchain").read_text(encoding="utf-8").strip() != TOOLCHAIN:
        raise ValueError("stale Lean toolchain")
    if digest(ROOT / "lake-manifest.json") != formal["dependency_lock_sha256"]:
        raise ValueError("stale dependency lock")
    if digest(ROOT / "lakefile.toml") != formal["package_config_sha256"]:
        raise ValueError("stale package configuration")

    manifest = json.loads((ROOT / "lake-manifest.json").read_text(encoding="utf-8"))
    packages = {package["name"]: package for package in manifest["packages"]}
    if packages["mathlib"]["rev"] != MATHLIB_REV or any(
        not re.fullmatch(r"[0-9a-f]{40}", package["rev"]) for package in packages.values()
    ):
        raise ValueError("invalid dependency revision")

    lean = run("lean", "--version")
    lake = run("lake", "--version")
    if "version 4.36.0," not in lean:
        raise ValueError(f"unexpected toolchain: {lean}")
    check_materialized_dependencies(packages)
    run("lake", "clean", "formalExample")
    build = run("lake", "build", "FormalExample")
    check_materialized_dependencies(packages, required=True)
    axioms = run("lake", "env", "lean", "review/StatementLock.lean")
    if any(f"{name} axioms:" not in axioms for name in (
        "FormalExample.oddSum", formal["declaration"]
    )):
        raise ValueError("incomplete axiom audit")
    return {
        "claim": formal["claim"],
        "source_sha256": digest(SOURCE),
        "root_sha256": digest(LIBRARY),
        "statement_lock_sha256": digest(ROOT / "review/StatementLock.lean"),
        "manifest_sha256": digest(ROOT / "lake-manifest.json"),
        "lean": lean,
        "lake": lake,
        "mathlib": MATHLIB_REV,
        "build": build,
        "statement_and_dependency_comparison": "pass",
        "axiom_audit": axioms,
        "review_state": formal["review_state"],
        "artifact_ref": formal["artifact_ref"],
    }


def self_test():
    source = SOURCE.read_text(encoding="utf-8")
    root = LIBRARY.read_text(encoding="utf-8")
    manifest = ROOT / "lake-manifest.json"
    dependency_lock = manifest.read_text(encoding="utf-8")
    evidence = EVIDENCE.read_text(encoding="utf-8")
    start = source.index("  induction n")
    end = source.index("\nend FormalExample")
    theorem = source[source.index("theorem "):start]
    lemma_type = "(n : Nat) : oddSum n = n ^ 2"
    direct_sorry = source[:start] + "  sorry\n" + source[end:]
    indirect_sorry = source.replace(theorem, f"private theorem helper {lemma_type} := by sorry\n\n{theorem}")
    indirect_sorry = indirect_sorry[:indirect_sorry.index("  induction n")] + "  exact helper n\n" + source[end:]
    indirect_axiom = indirect_sorry.replace("private theorem helper " + lemma_type + " := by sorry",
                                           "private axiom helper " + lemma_type)
    changed_conclusion = source[:start].replace("oddSum n = n ^ 2", "oddSum n = oddSum n") + "  rfl\n" + source[end:]
    changed_assumptions = source.replace("(n : Nat) : oddSum", "(n : Nat) (_extra : True) : oddSum")
    changed_definition = source.replace("2 * n + 1", "n * 2 + 1")
    missing_provenance = json.loads(evidence)
    missing_provenance["formal"]["source_provenance"] = ""
    forged_review = json.loads(evidence)
    forged_review["formal"]["review_state"] = "APPROVED"
    cases = [
        ("direct sorry", SOURCE, direct_sorry, "unapproved axiom sorryAx"),
        ("indirect sorry", SOURCE, indirect_sorry, "unapproved axiom sorryAx"),
        ("indirect custom axiom", SOURCE, indirect_axiom, "unapproved axiom"),
        ("changed conclusion", SOURCE, changed_conclusion, "locked statement changed"),
        ("added assumption", SOURCE, changed_assumptions, "locked statement changed"),
        ("changed definition", SOURCE, changed_definition, "locked definition changed"),
        ("draft import", LIBRARY, root + "import Drafts.Unreviewed\n", "unexpected module in accepted import graph: Drafts.Unreviewed"),
        ("stale lockfile", manifest, dependency_lock + "\n", "stale dependency lock"),
        ("missing provenance", EVIDENCE, json.dumps(missing_provenance), "evidence provenance"),
        ("fabricated review", EVIDENCE, json.dumps(forged_review), "evidence provenance"),
    ]
    for label, path, changed, expected in cases:
        original = path.read_bytes()
        try:
            path.write_bytes(changed.encode("utf-8"))
            try:
                audit()
            except ValueError as error:
                if expected not in str(error):
                    raise ValueError(f"{label} rejected for the wrong reason: {error}") from error
                print(f"Rejected {label}: {expected}", flush=True)
            else:
                raise ValueError(f"unexpected acceptance: {label}")
        finally:
            path.write_bytes(original)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test", action="store_true",
                        help="temporarily mutate the example in a disposable checkout")
    args = parser.parse_args()
    try:
        print(json.dumps(audit(), indent=2), flush=True)
        if args.self_test:
            self_test()
            print(json.dumps(audit(), indent=2), flush=True)
    except (KeyError, OSError, ValueError) as error:
        print(f"Verification failed: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
