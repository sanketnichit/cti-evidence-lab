"""Reproduce the exploratory study and package a source-text-free submission.

Python 3.11+, standard library only. Optional corpus audit is local and never
exports source text. A passing run is software verification, not gold review.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import platform
import subprocess
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from examples.exhaustive_projection_checks import run_checks
from examples.representation_controls import markdown, run_controls
from scripts.audit_pilot_sources import audit, verified_text
from scripts.summarize_exploratory_review import DEFAULT, summarize


def write_json(path, value):
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="")


def verify_package_checksums():
    base = ROOT / "research/schema_reconstruction/CTI_Annotation_Schema_RECON_v0.1"
    paths = set()
    for line in (base / "SHA256SUMS.txt").read_text(encoding="utf-8").splitlines():
        digest, relative = line.split("  ", 1)
        path = (base / relative).resolve()
        if not path.is_relative_to(base.resolve()) or relative in paths:
            raise ValueError("Invalid or duplicate package checksum path")
        paths.add(relative)
        if hashlib.sha256(path.read_bytes()).hexdigest() != digest:
            raise ValueError(f"Package checksum mismatch: {relative}")
    return len(paths)


def verify_critical_evidence(corpus_root, recover_crlf):
    evidence = json.loads((DEFAULT / "critical_evidence.json").read_text(encoding="utf-8"))
    cache = {}
    for row in evidence["spans"]:
        rid = row["report_id"]
        if rid not in cache:
            cache[rid], _ = verified_text((corpus_root / "text" / (rid + ".txt")).read_bytes(), row["source_text_sha256"], recover_crlf)
        text = cache[rid]
        if hashlib.sha256(text.encode()).hexdigest() != row["source_text_sha256"]:
            raise ValueError("Inconsistent critical-review source binding")
        start, end = row["char_start"], row["char_end"]
        if not 0 <= start < end <= len(text):
            raise ValueError("Critical review offset outside source")
        if hashlib.sha256(text[start:end].encode()).hexdigest() != row["span_sha256"]:
            raise ValueError("Critical review evidence hash mismatch")
        if text.count("\n", 0, start) + 1 != row["source_line_number"]:
            raise ValueError("Critical review line mismatch")
    return len(evidence["spans"])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=ROOT / "outputs/submission")
    parser.add_argument("--corpus-root", type=Path)
    parser.add_argument("--recover-crlf", action="store_true")
    parser.add_argument("--allow-dirty", action="store_true", help="Development only; manifest records uncommitted inputs")
    parser.add_argument("--pdf", action="store_true", help="Render the report; requires reportlab")
    args = parser.parse_args()
    destination = args.output_dir.resolve()
    if not destination.is_relative_to((ROOT / "outputs").resolve()):
        parser.error("Output must be under ignored outputs/ to prevent committing generated source data")
    dirty = bool(subprocess.check_output(["git", "status", "--porcelain"], cwd=ROOT).strip())
    if dirty and not args.allow_dirty:
        parser.error("Commit the working tree first, or use --allow-dirty for a clearly marked development build")
    destination.mkdir(parents=True, exist_ok=True)
    result = {"repository_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
              "working_tree_dirty": dirty, "python_version": platform.python_version(),
              "package_checksums_verified": verify_package_checksums(), "test_suites": []}
    suites = ["tests"] + [f"research/schema_reconstruction/CTI_Annotation_Schema_RECON_v0.{v}/tests" for v in range(1, 5)]
    for suite in suites:
        check = subprocess.run([sys.executable, "-m", "unittest", "discover", "-s", suite, "-q"], cwd=ROOT, capture_output=True, text=True, encoding="utf-8")
        entry = {"suite": suite, "exit_code": check.returncode, "output": check.stdout + check.stderr}
        result["test_suites"].append(entry)
        write_json(destination / "validation.json", result)
        if check.returncode:
            raise SystemExit(f"Test failure in {suite}; see validation.json")
    controls = run_controls()
    write_json(destination / "representation_controls.json", controls)
    (destination / "representation_controls.md").write_text(markdown(controls), encoding="utf-8", newline="")
    write_json(destination / "finite_checks.json", run_checks())
    decisions = json.loads((DEFAULT / "review_decisions.json").read_text(encoding="utf-8"))
    source_audit = json.loads((DEFAULT / "source_integrity.json").read_text(encoding="utf-8"))
    result["source_audit_mode"] = "RECORDED_AUDIT_ONLY"
    if args.corpus_root:
        source_audit = audit(args.corpus_root, recover_crlf=args.recover_crlf)
        result["source_audit_mode"] = "LOCAL_CORPUS_RECHECKED"
        result["critical_review_spans_verified"] = verify_critical_evidence(args.corpus_root, args.recover_crlf)
    write_json(destination / "source_integrity.json", source_audit)
    write_json(destination / "exploratory_review.json", summarize(decisions, source_audit))
    result["status"] = "PASS_EXPLORATORY_REPRODUCTION_NOT_GOLD_VALIDATION"
    write_json(destination / "validation.json", result)
    generated_names = ["representation_controls.json", "representation_controls.md", "finite_checks.json",
                       "source_integrity.json", "exploratory_review.json", "validation.json"]
    if args.pdf:
        from scripts.build_report_pdf import build
        build(destination / "CTI_Evidence_Lab_Report.pdf")
        generated_names.append("CTI_Evidence_Lab_Report.pdf")
    files = subprocess.check_output(["git", "ls-files"], cwd=ROOT, text=True).splitlines()
    if args.allow_dirty:
        files += subprocess.check_output(["git", "ls-files", "--others", "--exclude-standard"], cwd=ROOT, text=True).splitlines()
    files = sorted(set(files))
    if any(p.startswith(("data/raw/", "outputs/")) and not p.endswith(".gitkeep") for p in files):
        raise ValueError("Refusing to package tracked raw sources or private outputs")
    package = destination / "CTI_Evidence_Lab_Submission.zip"
    payload = {"cti-evidence-lab/" + p: (ROOT / p).read_bytes() for p in files}
    payload.update({"generated/" + name: (destination / name).read_bytes() for name in generated_names})
    manifest = {"repository_commit": result["repository_commit"], "working_tree_dirty": dirty,
                "files_sha256": {name: hashlib.sha256(data).hexdigest() for name, data in sorted(payload.items())}}
    write_json(destination / "manifest.json", manifest)
    payload["manifest.json"] = (destination / "manifest.json").read_bytes()
    with zipfile.ZipFile(package, "w", zipfile.ZIP_DEFLATED) as archive:
        for name, data in sorted(payload.items()):
            archive.writestr(name, data)
    with zipfile.ZipFile(package) as archive:
        if archive.testzip() is not None:
            raise ValueError("Submission archive integrity failure")
    print("PASS: five test suites, package checksums, representation controls and submission archive.")
    print("Source verification mode:", result["source_audit_mode"])
    print(package.relative_to(ROOT).as_posix())


if __name__ == "__main__":
    main()
