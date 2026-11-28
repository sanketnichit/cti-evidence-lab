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
from examples.query_fidelity_benchmark import markdown as query_markdown, run_benchmark
from scripts.audit_pilot_sources import audit, verified_text
from scripts.summarize_exploratory_review import DEFAULT, summarize
from scripts.audit_rdp_case import CASE as RDP_CASE, verify as verify_rdp_source
from scripts.analyze_rdp_case import analyze as analyze_rdp_case
from scripts.analyze_sequence_case import CASE as SEQUENCE_CASE, analyze as analyze_sequence_case
from scripts.audit_rank_two_review import DIRECTORY as RANK_TWO, audit as audit_rank_two, summarize as summarize_rank_two, validate_recorded_audit
from scripts.analyze_incident_sequences import CASE as INCIDENT_CASE, analyze as analyze_incident_case
from examples.investigation_benchmark import run_checks as run_investigation_checks
from examples.interpretation_sensitivity import run as run_interpretation_sensitivity, summarize as summarize_sensitivity
from examples.interpretation_error_study import run as run_input_error_study, summarize as summarize_input_errors
from scripts.build_investigation import build as build_investigator
from scripts.evaluate_external_sequences import DIRECTORY as EXTERNAL, load_records as load_external_records, run_evaluation, audit_sources as audit_external_sources, validate_recorded_source_audit
from examples.bounded_mapping_checks import run_checks as run_bounded_mapping_checks
from examples.discovery_bound_sensitivity import RESULTS as DISCOVERY_RESULTS, run as run_discovery_bounds
from examples.sequence_index_storage import RESULTS as INDEX_RESULTS, run as run_index_storage
from examples.profile_coherence import RESULTS as COHERENCE_RESULTS, run as run_profile_coherence
from examples.profile_uncertainty import RESULTS as PROFILE_UNCERTAINTY_RESULTS, run as run_profile_uncertainty
from examples.netsupport_identity_sensitivity import RESULTS as IDENTITY_RESULTS, run as run_netsupport_identity
from examples.profile_conflicts import RESULTS as CONFLICT_RESULTS, run as run_profile_conflicts
from examples.ordering_evidence_sensitivity import RESULTS as ORDERING_RESULTS, run as run_ordering_sensitivity
from examples.domain_controller_citation_roles import run as run_citation_roles
from examples.profile_omission import RESULTS as OMISSION_RESULTS, run as run_profile_omission
from examples.shared_source_sensitivity import RESULTS as SHARED_SOURCE_RESULTS, run as run_shared_source
from examples.profile_coherence_summary import verify_table as verify_profile_table
from scripts.compare_sequence_profiles import export as profile_export, verify as verify_profile_export
from scripts.investigate_sequence import certificate as investigation_certificate, load_case as load_investigation_case
from scripts.evaluate_incident_holdout import DIRECTORY as HOLDOUT, run as run_holdout
from scripts.evaluate_cisa_extension import DIRECTORY as CISA, run as run_cisa
from scripts.evaluate_microsoft_series import DIRECTORY as MICROSOFT, run as run_microsoft


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
    parser.add_argument("--rdp-source-html", type=Path, help="Optional saved publisher HTML for the separate RDP case")
    parser.add_argument("--incident-source-html", type=Path, help="Optional saved publisher HTML for the next chronological incident case")
    parser.add_argument("--holdout-source-directory", type=Path, help="Saved HTML for both DFIR holdout reports")
    parser.add_argument("--cisa-pdf-directory", type=Path, help="Saved PDFs for both CISA advisories")
    parser.add_argument("--microsoft-pdf-directory", type=Path, help="Saved Microsoft incident PDF and mislinked PDF")
    parser.add_argument("--attack-taxonomy", type=Path, help="Pinned ATT&CK STIX file for checking the discovery tactic lists")
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
    query_results = run_benchmark()
    write_json(destination / "query_fidelity.json", query_results)
    (destination / "query_fidelity.md").write_text(query_markdown(query_results), encoding="utf-8", newline="")
    decisions = json.loads((DEFAULT / "review_decisions.json").read_text(encoding="utf-8"))
    source_audit = json.loads((DEFAULT / "source_integrity.json").read_text(encoding="utf-8"))
    result["source_audit_mode"] = "RECORDED_AUDIT_ONLY"
    if args.corpus_root:
        source_audit = audit(args.corpus_root, recover_crlf=args.recover_crlf)
        result["source_audit_mode"] = "LOCAL_CORPUS_RECHECKED"
        result["critical_review_spans_verified"] = verify_critical_evidence(args.corpus_root, args.recover_crlf)
    write_json(destination / "source_integrity.json", source_audit)
    write_json(destination / "exploratory_review.json", summarize(decisions, source_audit))
    extension_selection = json.loads((RANK_TWO / "selection.json").read_text(encoding="utf-8"))
    extension_review = json.loads((RANK_TWO / "review.json").read_text(encoding="utf-8"))
    write_json(destination / "rank_two_review.json", summarize_rank_two(extension_selection, extension_review))
    extension_audit = validate_recorded_audit(extension_selection, extension_review, json.loads((RANK_TWO / "source_integrity.json").read_text(encoding="utf-8")))
    result["rank_two_source_audit_mode"] = "RECORDED_AUDIT_ONLY"
    if args.corpus_root:
        extension_audit = audit_rank_two(args.corpus_root, extension_selection, extension_review, recover_crlf=args.recover_crlf)
        result["rank_two_source_audit_mode"] = "LOCAL_CORPUS_RECHECKED"
    write_json(destination / "rank_two_source_integrity.json", extension_audit)
    rdp_case = json.loads(RDP_CASE.read_text(encoding="utf-8"))
    write_json(destination / "rdp_case_results.json", analyze_rdp_case(rdp_case))
    rdp_audit = json.loads((RDP_CASE.parent / "source_integrity.json").read_text(encoding="utf-8"))
    result["rdp_source_audit_mode"] = "RECORDED_AUDIT_ONLY"
    if args.rdp_source_html:
        rdp_audit = verify_rdp_source(args.rdp_source_html.read_bytes(), rdp_case)
        result["rdp_source_audit_mode"] = "LOCAL_HTML_RECHECKED"
    write_json(destination / "rdp_source_integrity.json", rdp_audit)
    sequence_case = json.loads(SEQUENCE_CASE.read_text(encoding="utf-8"))
    write_json(destination / "sequence_case_results.json", analyze_sequence_case(sequence_case))
    sequence_audit = json.loads((SEQUENCE_CASE.parent / "source_integrity.json").read_text(encoding="utf-8"))
    result["sequence_source_audit_mode"] = "RECORDED_AUDIT_ONLY"
    if args.rdp_source_html:
        sequence_audit = verify_rdp_source(args.rdp_source_html.read_bytes(), sequence_case)
        result["sequence_source_audit_mode"] = "LOCAL_HTML_RECHECKED"
    write_json(destination / "sequence_source_integrity.json", sequence_audit)
    incident_case = json.loads(INCIDENT_CASE.read_text(encoding="utf-8"))
    incident_selection = json.loads((INCIDENT_CASE.parent / "selection.json").read_text(encoding="utf-8"))
    write_json(destination / "incident_sequence_results.json", analyze_incident_case(incident_case, incident_selection))
    incident_audit = json.loads((INCIDENT_CASE.parent / "source_integrity.json").read_text(encoding="utf-8"))
    result["incident_source_audit_mode"] = "RECORDED_AUDIT_ONLY"
    if args.incident_source_html:
        incident_audit = verify_rdp_source(args.incident_source_html.read_bytes(), incident_case)
        result["incident_source_audit_mode"] = "LOCAL_HTML_RECHECKED"
    write_json(destination / "incident_source_integrity.json", incident_audit)
    write_json(destination / "investigation_checks.json", run_investigation_checks())
    sensitivity = run_interpretation_sensitivity()
    expected_sensitivity = ROOT / "research/experiments/interpretation_sensitivity_v0.1/results.json"
    if json.loads(json.dumps(summarize_sensitivity(sensitivity))) != json.loads(expected_sensitivity.read_text(encoding="utf-8")):
        raise ValueError("Interpretation sensitivity summary differs from the published results")
    write_json(destination / "interpretation_sensitivity.json", sensitivity)
    input_errors = run_input_error_study()
    expected_errors = expected_sensitivity.with_name("input_error_results.json")
    if json.loads(json.dumps(summarize_input_errors(input_errors))) != json.loads(expected_errors.read_text(encoding="utf-8")):
        raise ValueError("Input error summary differs from the published results")
    write_json(destination / "interpretation_input_errors.json", input_errors)
    for filename, recorded, runner, local_source, mode_key, local_mode in (
        ("incident_holdout_results.json", HOLDOUT, run_holdout, args.holdout_source_directory,
         "holdout_source_audit_mode", "LOCAL_HTML_RECHECKED"),
        ("cisa_extension_results.json", CISA, run_cisa, args.cisa_pdf_directory,
         "cisa_source_audit_mode", "LOCAL_PDFS_RECHECKED"),
        ("microsoft_series_results.json", MICROSOFT, run_microsoft, args.microsoft_pdf_directory,
         "microsoft_source_audit_mode", "LOCAL_INCIDENT_AND_MISLINKED_PDFS_RECHECKED"),
    ):
        report = runner(local_source)
        if json.loads(json.dumps(report)) != json.loads((recorded / "results.json").read_text(encoding="utf-8")):
            raise ValueError(f"Incident comparison differs from published results: {filename}")
        write_json(destination / filename, report)
        result[mode_key] = local_mode if local_source is not None else "RECORDED_AUDIT_ONLY"
    write_json(destination / "bounded_mapping_checks.json", run_bounded_mapping_checks())
    discovery = run_discovery_bounds(args.attack_taxonomy)
    if discovery != json.loads(DISCOVERY_RESULTS.read_text(encoding="utf-8")):
        raise ValueError("Discovery mapping sensitivity differs from the published results")
    write_json(destination / "discovery_mapping_sensitivity.json", discovery)
    result["discovery_taxonomy_verification_mode"] = (
        "LOCAL_PINNED_STIX_RECHECKED" if args.attack_taxonomy is not None else "RECORDED_TACTIC_LISTS_ONLY"
    )
    index_storage = run_index_storage()
    if index_storage != json.loads(INDEX_RESULTS.read_text(encoding="utf-8")):
        raise ValueError("Answer-index storage differs from the published results")
    write_json(destination / "answer_index_storage.json", index_storage)
    coherence = run_profile_coherence()
    if coherence != json.loads(COHERENCE_RESULTS.read_text(encoding="utf-8")):
        raise ValueError("Profile coherence differs from the published results")
    write_json(destination / "profile_coherence.json", coherence)
    profile_uncertainty = run_profile_uncertainty()
    if profile_uncertainty != json.loads(PROFILE_UNCERTAINTY_RESULTS.read_text(encoding="utf-8")):
        raise ValueError("Profile uncertainty differs from the published results")
    write_json(destination / "profile_uncertainty.json", profile_uncertainty)
    identity = run_netsupport_identity()
    if identity != json.loads(IDENTITY_RESULTS.read_bytes()):
        raise ValueError("NetSupport identity sensitivity differs from the recorded results")
    write_json(destination / "netsupport_identity_sensitivity.json", identity)
    conflicts = run_profile_conflicts()
    if conflicts != json.loads(CONFLICT_RESULTS.read_bytes()):
        raise ValueError("Profile conflict explanations differ from the recorded results")
    write_json(destination / "profile_conflicts.json", conflicts)
    ordering_sensitivity = run_ordering_sensitivity()
    if ordering_sensitivity != json.loads(ORDERING_RESULTS.read_bytes()):
        raise ValueError("Ordering-evidence sensitivity differs from the recorded results")
    write_json(destination / "ordering_evidence_sensitivity.json", ordering_sensitivity)
    write_json(destination / "domain_controller_citation_roles.json", run_citation_roles())
    omission = run_profile_omission()
    if omission != json.loads(OMISSION_RESULTS.read_bytes()):
        raise ValueError("Profile omission differs from the recorded results")
    write_json(destination / "profile_omission.json", omission)
    shared_source = run_shared_source()
    if shared_source != json.loads(SHARED_SOURCE_RESULTS.read_bytes()):
        raise ValueError("Shared-source sensitivity differs from the recorded results")
    write_json(destination / "shared_source_sensitivity.json", shared_source)
    verify_profile_table(profile_uncertainty, identity, shared_source)
    profile_example = profile_export("netsupport-identity", ["T1562", "T1047", "T1053"])
    verify_profile_export(profile_example)
    write_json(destination / "profile_comparison_example.json", profile_example)
    bounds = json.loads((ROOT / "research/experiments/bounded_mapping_v0.1/archive_bound_assumption.json").read_text(encoding="utf-8"))
    write_json(destination / "bounded_mapping_assumption_example.json", investigation_certificate(
        "domain-controller", load_investigation_case("domain-controller"), "archive_mapping_withheld",
        ["T1059", "T1059", "T1059"], mapping_constraints=bounds))
    external_selection, external_review = load_external_records()
    write_json(destination / "external_sequence_results.json", run_evaluation(external_selection, external_review))
    external_audit = validate_recorded_source_audit(external_selection, external_review, json.loads((EXTERNAL / "source_integrity.json").read_text(encoding="utf-8")))
    result["external_source_audit_mode"] = "RECORDED_AUDIT_ONLY"
    if args.corpus_root:
        external_audit = audit_external_sources(external_selection, external_review, args.corpus_root, args.recover_crlf)
        result["external_source_audit_mode"] = "LOCAL_CORPUS_RECHECKED"
    write_json(destination / "external_sequence_source_integrity.json", external_audit)
    build_investigator(destination / "sequence_investigator.html")
    result["status"] = "PASS_EXPLORATORY_REPRODUCTION_NOT_GOLD_VALIDATION"
    write_json(destination / "validation.json", result)
    generated_names = ["representation_controls.json", "representation_controls.md", "finite_checks.json",
                       "source_integrity.json", "exploratory_review.json", "validation.json",
                       "query_fidelity.json", "query_fidelity.md",
                       "rdp_case_results.json", "rdp_source_integrity.json",
                       "sequence_case_results.json", "sequence_source_integrity.json",
                       "rank_two_review.json", "rank_two_source_integrity.json",
                       "incident_sequence_results.json", "incident_source_integrity.json",
                       "investigation_checks.json", "sequence_investigator.html", "interpretation_sensitivity.json",
                       "interpretation_input_errors.json",
                       "incident_holdout_results.json", "cisa_extension_results.json", "microsoft_series_results.json",
                       "external_sequence_results.json", "external_sequence_source_integrity.json",
                       "bounded_mapping_checks.json", "bounded_mapping_assumption_example.json",
                       "discovery_mapping_sensitivity.json", "answer_index_storage.json", "profile_coherence.json",
                       "profile_uncertainty.json", "netsupport_identity_sensitivity.json", "profile_conflicts.json",
                       "profile_comparison_example.json", "ordering_evidence_sensitivity.json",
                       "domain_controller_citation_roles.json", "profile_omission.json", "shared_source_sensitivity.json"]
    if args.pdf:
        from scripts.build_report_pdf import build
        build(destination / "CTI_Evidence_Lab_Report.pdf",
              revision=result["repository_commit"] if not dirty else "main")
        generated_names.append("CTI_Evidence_Lab_Report.pdf")
    files = subprocess.check_output(["git", "ls-files"], cwd=ROOT, text=True).splitlines()
    if args.allow_dirty:
        files += subprocess.check_output(["git", "ls-files", "--others", "--exclude-standard"], cwd=ROOT, text=True).splitlines()
    files = sorted(p for p in set(files) if (ROOT / p).is_file())
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
    rechecked = [name for name, mode in result.items()
                 if (name.endswith("_audit_mode") or name.endswith("_verification_mode")) and mode.startswith("LOCAL_")]
    print("Local verification:", ", ".join(rechecked) if rechecked else "recorded evidence only")
    print(package.relative_to(ROOT).as_posix())


if __name__ == "__main__":
    main()
