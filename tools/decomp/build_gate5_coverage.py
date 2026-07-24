#!/usr/bin/env python3
"""Build Chirality Gate 5 section coverage review artifacts.

The script consumes the accepted Gate 4 ledger and Gate 2 source-unit
authority. It does not edit atom text, SourceRefs, ContentHash values,
Category assignments, KTY mappings, or Subject mappings. Gate 5 remains open
until human review attests zero-coverage sections or routes them back to Phase
2 re-dispatch.
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import subprocess
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]
COVERAGE_CLASSES = ("cov-empty", "cov-low", "cov-mid", "cov-high")
ZERO_COVERAGE_ISSUE_ID = "OI-024"


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--domain-root", type=Path, default=Path("domains/chirality"))
    p.add_argument("--repo-root", type=Path, default=Path("."))
    p.add_argument("--timestamp", default=None, help="UTC timestamp in YYYYMMDDTHHMMSSZ form")
    p.add_argument("--skip-render", action="store_true", help="Write registers only; do not render coverage HTML")
    return p.parse_args()


def utc_now() -> tuple[str, str]:
    dt = datetime.now(timezone.utc)
    return dt.strftime("%Y%m%dT%H%M%SZ"), dt.replace(microsecond=0).isoformat().replace("+00:00", "Z")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = list(rows[0].keys()) if rows else []
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({name: row.get(name, "") for name in fieldnames})


def split_ids(value: str) -> list[str]:
    return [part.strip() for part in re.split(r"[;,]", value or "") if part.strip()]


def truthy(value: str) -> bool:
    return str(value).strip().lower() in {"1", "true", "yes", "y"}


def density_class(density: float) -> str:
    if density == 0:
        return "cov-empty"
    if density < 0.5:
        return "cov-low"
    if density < 2.0:
        return "cov-mid"
    return "cov-high"


def rel(path: Path, repo_root: Path) -> str:
    try:
        return path.resolve().relative_to(repo_root.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def resolve_existing(path_text: str, repo_root: Path) -> Path:
    p = Path(path_text)
    if p.is_absolute():
        return p
    return repo_root / p


def upsert_rows(path: Path, key: str, new_rows: list[dict[str, str]]) -> None:
    rows = read_csv(path) if path.exists() else []
    fieldnames = list(rows[0].keys()) if rows else list(new_rows[0].keys())
    by_key = {row[key]: row for row in rows}
    order = [row[key] for row in rows]
    for row in new_rows:
        if row[key] not in by_key:
            order.append(row[key])
        by_key[row[key]] = {name: row.get(name, "") for name in fieldnames}
    write_csv(path, [by_key[k] for k in order], fieldnames=fieldnames)


def load_skeleton(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_mappings(
    ledger_rows: list[dict[str, str]],
    kty_rows: list[dict[str, str]],
    subject_rows: list[dict[str, str]],
) -> dict[str, Any]:
    in_rows = [row for row in ledger_rows if row.get("InOutStatus") == "IN"]
    unassigned_categories = []
    multi_categories = []
    missing_kty = []
    missing_subject = []
    for row in in_rows:
        cat_ids = split_ids(row.get("CategoryID", ""))
        if not cat_ids:
            unassigned_categories.append(row["AtomicUnitID"])
        elif len(cat_ids) != 1:
            multi_categories.append(row["AtomicUnitID"])
        if not split_ids(row.get("KnowledgeTypeIDs", "")):
            missing_kty.append(row["AtomicUnitID"])
        if not split_ids(row.get("SubjectIDs", "")):
            missing_subject.append(row["AtomicUnitID"])

    kty_parent_errors = []
    for row in kty_rows:
        parents = split_ids(row.get("ParentCategoryID", ""))
        if len(parents) != 1:
            kty_parent_errors.append(row.get("KnowledgeTypeID", ""))

    subject_parent_errors = []
    for row in subject_rows:
        parents = split_ids(row.get("ParentKnowledgeTypeID", ""))
        if len(parents) != 1:
            subject_parent_errors.append(row.get("SubjectID", ""))

    blocking = (
        unassigned_categories
        or multi_categories
        or missing_kty
        or missing_subject
        or kty_parent_errors
        or subject_parent_errors
    )
    return {
        "in_rows": len(in_rows),
        "unassigned_categories": unassigned_categories,
        "multi_categories": multi_categories,
        "missing_kty": missing_kty,
        "missing_subject": missing_subject,
        "kty_parent_errors": kty_parent_errors,
        "subject_parent_errors": subject_parent_errors,
        "blocking": bool(blocking),
    }


def rows_by_source(ledger_rows: list[dict[str, str]]) -> dict[str, list[dict[str, str]]]:
    out: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in ledger_rows:
        out[row.get("SourceDoc", "")].append(row)
    return out


def atom_counts_by_source_section(ledger_rows: list[dict[str, str]]) -> dict[tuple[str, str], Counter[str]]:
    counts: dict[tuple[str, str], Counter[str]] = defaultdict(Counter)
    for row in ledger_rows:
        source_doc = row.get("SourceDoc", "")
        section_id = row.get("SectionID", "")
        if not source_doc or not section_id:
            continue
        status = row.get("InOutStatus", "")
        key = (source_doc, section_id)
        counts[key]["total"] += 1
        if status == "IN":
            counts[key]["in"] += 1
        elif status == "OUT":
            counts[key]["out"] += 1
        elif status == "TBD":
            counts[key]["tbd"] += 1
        else:
            counts[key]["other"] += 1
    return counts


def build_section_coverage(
    decomp_root: Path,
    source_rows: list[dict[str, str]],
    ledger_rows: list[dict[str, str]],
    package_dir: Path,
    repo_root: Path,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    counts = atom_counts_by_source_section(ledger_rows)
    coverage_rows: list[dict[str, Any]] = []
    source_summary_rows: list[dict[str, Any]] = []

    for source in source_rows:
        source_doc = source["SourceDocID"]
        source_prefix = source["SourcePrefix"]
        nodes_path = decomp_root / "source_section_nodes" / f"{source_doc}_section_nodes.csv"
        if not nodes_path.exists():
            raise FileNotFoundError(f"missing section-node CSV for {source_doc}: {nodes_path}")
        node_rows = read_csv(nodes_path)
        source_atoms = [row for row in ledger_rows if row.get("SourceDoc") == source_doc]
        source_atom_status = Counter(row.get("InOutStatus", "") for row in source_atoms)
        source_cov_dist = Counter()
        source_zero = 0
        in_scope_count = 0

        for node in node_rows:
            section_id = node["SectionID"]
            in_scope = truthy(node.get("InScope", ""))
            try:
                line_start = int(node.get("LineStart", "0") or 0)
                line_end = int(node.get("LineEnd", "0") or 0)
            except ValueError:
                line_start = 0
                line_end = 0
            span = max(1, line_end - line_start + 1)
            c = counts[(source_doc, section_id)]
            density = c["in"] / max(1.0, span / 50.0)
            cov_class = density_class(density)
            zero = in_scope and c["in"] == 0
            if in_scope:
                in_scope_count += 1
                source_cov_dist[cov_class] += 1
                if zero:
                    source_zero += 1

            review_html_rel = f"domains/chirality/_Decomposition/gate5_coverage/{package_dir.name}/coverage_review_html/{source_doc}.html"
            coverage_rows.append({
                "SourceDocID": source_doc,
                "SourcePrefix": source_prefix,
                "SourceName": source.get("SourceName", ""),
                "RepoRelPath": source.get("RepoRelPath", ""),
                "SourceGroup": source.get("SourceGroup", ""),
                "BatchID": source.get("BatchID", ""),
                "SectionID": section_id,
                "Path": node.get("Path", ""),
                "Depth": node.get("Depth", ""),
                "Title": node.get("Title", ""),
                "LineStart": line_start,
                "LineEnd": line_end,
                "LineSpan": span,
                "InScope": "TRUE" if in_scope else "FALSE",
                "IsFrontMatter": "TRUE" if truthy(node.get("IsFrontMatter", "")) else "FALSE",
                "IsBackMatter": "TRUE" if truthy(node.get("IsBackMatter", "")) else "FALSE",
                "INAtomCount": c["in"],
                "OutAtomCount": c["out"],
                "TbdAtomCount": c["tbd"],
                "OtherAtomCount": c["other"],
                "TotalAtomCount": c["total"],
                "AtomsPer50Lines": f"{density:.4f}",
                "CoverageClass": cov_class,
                "ZeroCoverageFlag": "TRUE" if zero else "FALSE",
                "Gate5ReviewStatus": "PENDING_ZERO_COVERAGE_REVIEW" if zero else "NONZERO_OR_OUT_OF_SCOPE",
                "CoverageReviewHtmlPath": review_html_rel,
                "CoverageReviewHref": f"{review_html_rel}#{section_id}",
                "ZeroCoverageIssueID": ZERO_COVERAGE_ISSUE_ID if zero else "",
                "AttestationStatus": "PENDING_GATE5_HUMAN_REVIEW" if zero else "",
                "AttestationNote": "",
            })

        source_summary_rows.append({
            "Gate2SourceSeq": source.get("Gate2SourceSeq", ""),
            "BatchID": source.get("BatchID", ""),
            "SourceDocID": source_doc,
            "SourcePrefix": source_prefix,
            "SourceName": source.get("SourceName", ""),
            "RepoRelPath": source.get("RepoRelPath", ""),
            "SourceGroup": source.get("SourceGroup", ""),
            "SectionCount": len(node_rows),
            "InScopeSectionCount": in_scope_count,
            "SectionsWithZeroCoverageCount": source_zero,
            "CovEmptySections": source_cov_dist["cov-empty"],
            "CovLowSections": source_cov_dist["cov-low"],
            "CovMidSections": source_cov_dist["cov-mid"],
            "CovHighSections": source_cov_dist["cov-high"],
            "INAtomCount": source_atom_status["IN"],
            "OutAtomCount": source_atom_status["OUT"],
            "TbdAtomCount": source_atom_status["TBD"],
            "TotalAtomCount": len(source_atoms),
            "CoverageReviewHtmlPath": f"domains/chirality/_Decomposition/gate5_coverage/{package_dir.name}/coverage_review_html/{source_doc}.html",
            "CoverageSectionNodesPath": f"domains/chirality/_Decomposition/gate5_coverage/{package_dir.name}/coverage_section_nodes/{source_doc}_section_nodes.csv",
            "CoverageAtomSlicePath": f"domains/chirality/_Decomposition/gate5_coverage/{package_dir.name}/source_atom_slices/{source_doc}_atomic_units.csv",
            "Status": "PENDING_GATE5_HUMAN_REVIEW" if source_zero else "COVERAGE_NONZERO_FOR_ALL_IN_SCOPE_SECTIONS",
            "Notes": "Zero-coverage sections require Gate 5 attestation." if source_zero else "",
        })

    return coverage_rows, source_summary_rows


def write_atom_slices(
    package_dir: Path,
    source_rows: list[dict[str, str]],
    ledger_rows: list[dict[str, str]],
) -> dict[str, Path]:
    by_source = rows_by_source(ledger_rows)
    fieldnames = list(ledger_rows[0].keys()) if ledger_rows else []
    out_dir = package_dir / "source_atom_slices"
    paths: dict[str, Path] = {}
    for source in source_rows:
        source_doc = source["SourceDocID"]
        path = out_dir / f"{source_doc}_atomic_units.csv"
        write_csv(path, by_source.get(source_doc, []), fieldnames=fieldnames)
        paths[source_doc] = path
    return paths


def render_coverage_html(
    repo_root: Path,
    decomp_root: Path,
    source_rows: list[dict[str, str]],
    package_dir: Path,
    atom_slice_paths: dict[str, Path],
) -> list[str]:
    render_tool = repo_root / "tools" / "decomp" / "render_source_html.py"
    html_dir = package_dir / "coverage_review_html"
    nodes_dir = package_dir / "coverage_section_nodes"
    sidecar_dir = package_dir / "coverage_sidecars"
    logs: list[str] = []

    for source in source_rows:
        source_doc = source["SourceDocID"]
        skeleton_path = resolve_existing(source["SkeletonPath"], repo_root)
        skeleton = load_skeleton(skeleton_path)
        md_path = Path(skeleton.get("md_path", ""))
        if not md_path.is_absolute():
            md_path = repo_root / md_path
        asset_manifest = decomp_root / "source_asset_manifests" / f"{source_doc}_assets_manifest.json"
        if not md_path.exists():
            raise FileNotFoundError(f"missing render Markdown for {source_doc}: {md_path}")
        if not asset_manifest.exists():
            raise FileNotFoundError(f"missing asset manifest for {source_doc}: {asset_manifest}")

        audit_dir = sidecar_dir / source_doc
        cmd = [
            sys.executable,
            str(render_tool),
            "--md",
            str(md_path),
            "--asset-manifest",
            str(asset_manifest),
            "--skeleton",
            str(skeleton_path),
            "--audit-dir",
            str(audit_dir),
            "--output-html",
            str(html_dir / f"{source_doc}.html"),
            "--output-section-nodes",
            str(nodes_dir / f"{source_doc}_section_nodes.csv"),
            "--mode",
            "coverage-review",
            "--atomic-units-csv",
            str(atom_slice_paths[source_doc]),
            "--title",
            f"{source_doc} - Gate 5 coverage review",
        ]
        audit_dir.mkdir(parents=True, exist_ok=True)
        result = subprocess.run(cmd, cwd=repo_root, text=True, capture_output=True, check=False)
        if result.returncode != 0:
            raise RuntimeError(
                f"coverage render failed for {source_doc}: {result.stderr.strip() or result.stdout.strip()}"
            )
        logs.append(result.stdout.strip())
    return logs


def build_telemetry(
    generated_iso: str,
    package_name: str,
    source_rows: list[dict[str, str]],
    ledger_rows: list[dict[str, str]],
    section_rows: list[dict[str, Any]],
    source_summary_rows: list[dict[str, Any]],
    kty_rows: list[dict[str, str]],
    subject_rows: list[dict[str, str]],
    mapping_status: dict[str, Any],
) -> dict[str, Any]:
    status_counts = Counter(row.get("InOutStatus", "") for row in ledger_rows)
    category_ids = {row.get("CategoryID") for row in ledger_rows if row.get("InOutStatus") == "IN" and row.get("CategoryID")}
    in_scope_sections = [row for row in section_rows if row["InScope"] == "TRUE"]
    zero_rows = [row for row in in_scope_sections if row["ZeroCoverageFlag"] == "TRUE"]
    dist = Counter(row["CoverageClass"] for row in in_scope_sections)
    open_issue_counts = {ZERO_COVERAGE_ISSUE_ID: len(zero_rows)} if zero_rows else {}
    return {
        "revision": package_name,
        "generated_utc": generated_iso,
        "status": "OPEN_PENDING_GATE5_HUMAN_REVIEW",
        "upstream_gate4_snapshot": "domains/chirality/_Decomposition/gate_snapshots/GATE4_KTY_20260615T042414Z",
        "UnitCount": len(ledger_rows),
        "INUnitCount": status_counts["IN"],
        "OUTUnitCount": status_counts["OUT"],
        "TBDUnitCount": status_counts["TBD"],
        "SourceCount": len(source_rows),
        "SectionCount": len(section_rows),
        "InScopeSectionCount": len(in_scope_sections),
        "SectionsWithZeroCoverageCount": len(zero_rows),
        "ZeroCoverageSectionIDs": [row["SectionID"] for row in zero_rows],
        "SectionCoverageDensityDistribution": {klass: dist[klass] for klass in COVERAGE_CLASSES},
        "CategoryCount": len(category_ids),
        "KnowledgeTypeCount": len(kty_rows),
        "SubjectCount": len(subject_rows),
        "UnassignedINUnits": len(mapping_status["unassigned_categories"]) + len(mapping_status["multi_categories"]),
        "UnitsWithoutKnowledgeTypeMapping": len(mapping_status["missing_kty"]),
        "UnitsWithoutSubjectMapping": len(mapping_status["missing_subject"]),
        "OpenIssuesByType": open_issue_counts,
        "CoverageReviewHtmlCount": len(source_summary_rows),
        "CoverageReviewHtmlRoot": f"domains/chirality/_Decomposition/gate5_coverage/{package_name}/coverage_review_html",
        "SectionCoverageRegister": "domains/chirality/_Decomposition/Section_Coverage_Register.csv",
        "SourceCoverageSummary": "domains/chirality/_Decomposition/Source_Coverage_Summary.csv",
        "Gate5ReviewPacket": "domains/chirality/_Decomposition/Gate5_Coverage_Review_Packet.md",
    }


def write_telemetry_csv(path: Path, telemetry: dict[str, Any]) -> None:
    rows = []
    for key, value in telemetry.items():
        if isinstance(value, (dict, list)):
            rendered = json.dumps(value, separators=(",", ":"))
        else:
            rendered = str(value)
        rows.append({"Metric": key, "Value": rendered})
    write_csv(path, rows, fieldnames=["Metric", "Value"])


def write_review_packet(
    path: Path,
    package_dir: Path,
    telemetry: dict[str, Any],
    section_rows: list[dict[str, Any]],
    source_summary_rows: list[dict[str, Any]],
    generated_iso: str,
) -> None:
    zero_rows = [row for row in section_rows if row["ZeroCoverageFlag"] == "TRUE"]
    top_sources = sorted(
        source_summary_rows,
        key=lambda row: int(row["SectionsWithZeroCoverageCount"]),
        reverse=True,
    )[:20]
    lines = [
        "# Gate 5 Coverage Review Packet",
        "",
        f"Generated UTC: {generated_iso}",
        "",
        "Status: Gate 5 is OPEN pending human section-coverage attestation.",
        "",
        "## Upstream Basis",
        "",
        "- Gate 4 accepted snapshot: `domains/chirality/_Decomposition/gate_snapshots/GATE4_KTY_20260615T042414Z`",
        "- Accepted KTY ledger: `domains/chirality/_Decomposition/Domain_Ledger_Gate4_KTY_Draft.csv`",
        "- Accepted source-unit authority: `domains/chirality/_Decomposition/Gate2_Source_Unit_Register.csv`",
        "",
        "## Review Surfaces",
        "",
        f"- Gate 5 package: `domains/chirality/_Decomposition/gate5_coverage/{package_dir.name}/`",
        f"- Coverage review HTML root: `domains/chirality/_Decomposition/gate5_coverage/{package_dir.name}/coverage_review_html/`",
        "- Section coverage register: `domains/chirality/_Decomposition/Section_Coverage_Register.csv`",
        "- Source coverage summary: `domains/chirality/_Decomposition/Source_Coverage_Summary.csv`",
        "",
        "## Telemetry",
        "",
        "| Metric | Value |",
        "|---|---:|",
        f"| UnitCount | {telemetry['UnitCount']} |",
        f"| INUnitCount | {telemetry['INUnitCount']} |",
        f"| OUTUnitCount | {telemetry['OUTUnitCount']} |",
        f"| TBDUnitCount | {telemetry['TBDUnitCount']} |",
        f"| SourceCount | {telemetry['SourceCount']} |",
        f"| SectionCount | {telemetry['SectionCount']} |",
        f"| InScopeSectionCount | {telemetry['InScopeSectionCount']} |",
        f"| SectionsWithZeroCoverageCount | {telemetry['SectionsWithZeroCoverageCount']} |",
        f"| CategoryCount | {telemetry['CategoryCount']} |",
        f"| KnowledgeTypeCount | {telemetry['KnowledgeTypeCount']} |",
        f"| SubjectCount | {telemetry['SubjectCount']} |",
        f"| UnassignedINUnits | {telemetry['UnassignedINUnits']} |",
        f"| UnitsWithoutKnowledgeTypeMapping | {telemetry['UnitsWithoutKnowledgeTypeMapping']} |",
        "",
        "Coverage density distribution is computed over in-scope sections using IN atoms per roughly 50 source lines.",
        "",
        "| Coverage class | Sections |",
        "|---|---:|",
    ]
    dist = telemetry["SectionCoverageDensityDistribution"]
    for klass in COVERAGE_CLASSES:
        lines.append(f"| `{klass}` | {dist[klass]} |")
    lines.extend([
        "",
        "## Zero-Coverage Review",
        "",
        f"`{ZERO_COVERAGE_ISSUE_ID}` remains open until the human attests zero-coverage sections as scaffold-for-fill/boilerplate or routes affected source units back to Phase 2 re-dispatch.",
        "",
        "| SourceDocID | Zero sections | In-scope sections | Review HTML |",
        "|---|---:|---:|---|",
    ])
    for row in top_sources:
        if int(row["SectionsWithZeroCoverageCount"]) == 0:
            continue
        lines.append(
            f"| `{row['SourceDocID']}` | {row['SectionsWithZeroCoverageCount']} | {row['InScopeSectionCount']} | `{row['CoverageReviewHtmlPath']}` |"
        )
    if not zero_rows:
        lines.append("| _none_ | 0 | 0 |  |")
    lines.extend([
        "",
        "## Gate 5 Closure Condition",
        "",
        "Gate 5 cannot close until the human explicitly confirms: Coverage and mappings are acceptable; section-coverage gaps have been ruled on as scaffold-for-fill/boilerplate or routed back for Phase 2 re-dispatch; open issues list is correct.",
        "",
    ])
    path.write_text("\n".join(lines), encoding="utf-8")


def write_handoff(path: Path, telemetry: dict[str, Any], generated_iso: str, package_name: str) -> None:
    lines = [
        "# Gate 5 Handoff State - Coverage Verification",
        "",
        "Package role: proposal / handoff artifact",
        "",
        "Status: Gate 5 OPEN pending human coverage attestation.",
        "",
        f"Generated UTC: {generated_iso}",
        "",
        "## Accepted Upstream Snapshot(s)",
        "",
        "- Gate 1: `domains/chirality/_Decomposition/gate_snapshots/GATE1_20260614T005942Z`",
        "- Gate 2: `domains/chirality/_Decomposition/gate_snapshots/GATE2_PHASE2_20260614T204403Z`",
        "- Gate 2 source-unit authority: `domains/chirality/_Decomposition/gate_snapshots/GATE2_PHASE2_SOURCE_UNIT_AUTHORITY_20260614T211725Z`",
        "- Gate 3: `domains/chirality/_Decomposition/gate_snapshots/GATE3_CATEGORIES_20260615T030833Z`",
        "- Gate 4: `domains/chirality/_Decomposition/gate_snapshots/GATE4_KTY_20260615T042414Z`",
        "",
        "## Current Gate 5 Artifacts",
        "",
        f"- `domains/chirality/_Decomposition/gate5_coverage/{package_name}/GATE5_COVERAGE_REVIEW_PACKET.md`",
        "- `domains/chirality/_Decomposition/Section_Coverage_Register.csv`",
        "- `domains/chirality/_Decomposition/Source_Coverage_Summary.csv`",
        "- `domains/chirality/_Decomposition/Gate5_Coverage_Telemetry.csv`",
        "- `domains/chirality/_Decomposition/Gate5_Coverage_Telemetry.json`",
        "",
        "## Counts",
        "",
        f"- Sources: {telemetry['SourceCount']}",
        f"- Sections: {telemetry['SectionCount']}",
        f"- In-scope sections: {telemetry['InScopeSectionCount']}",
        f"- Zero-coverage in-scope sections: {telemetry['SectionsWithZeroCoverageCount']}",
        f"- IN atoms mapped to Category/KTY/Subject: {telemetry['INUnitCount']}",
        "",
        "## Derivative-Package Status",
        "",
        "The Gate 5 coverage package is a review/handoff package derived from accepted Gate 4 decomposition truth. It does not replace the accepted atom ledger, Category register, KTY register, or Subject register.",
        "",
        "## Remaining Blockers",
        "",
        f"- `{ZERO_COVERAGE_ISSUE_ID}`: {telemetry['SectionsWithZeroCoverageCount']} zero-coverage in-scope sections require human attestation or Phase 2 re-dispatch routing.",
        "- Gate 5 has not been accepted by the human.",
        "",
        "## Rerun Requirements",
        "",
        "- If atom text, SectionID mappings, Category/KTY/Subject mappings, or source skeletons change, regenerate this Gate 5 package.",
        "- If zero-coverage sections are routed back to Phase 2 and new atoms are accepted, regenerate Gate 4 if mappings change, then regenerate Gate 5.",
        "",
        "## Next Action",
        "",
        "Human should review the coverage HTML surfaces and either accept zero-coverage sections as scaffold-for-fill/boilerplate or identify affected source units for Phase 2 re-dispatch. Do not proceed to Gate 6 until Gate 5 is explicitly accepted.",
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def update_control_doc(path: Path, generated_iso: str, package_name: str, telemetry: dict[str, Any]) -> None:
    text = path.read_text(encoding="utf-8")
    status = (
        "Status: Gate 5 Coverage verification is drafted and open pending human "
        f"attestation in `gate5_coverage/{package_name}`. Gate 4 remains accepted "
        "by `GATE4_KTY_20260615T042414Z`; accepted Gate 4 mappings are unchanged. "
        f"`{ZERO_COVERAGE_ISSUE_ID}` tracks zero-coverage in-scope sections until Gate 5 review closes. "
        "`OI-022` remains a human-deferred source-database cadence issue outside Gate 5 closure."
    )
    text = re.sub(r"^Status: .*$", status, text, count=1, flags=re.MULTILINE)
    text = re.sub(r"^Generated UTC: .*$", f"Generated UTC: {generated_iso}", text, count=1, flags=re.MULTILINE)
    section = phase5_section(package_name, telemetry)
    if "## Phase 5 Coverage Verification (Draft)" in text:
        text = re.sub(
            r"## Phase 5 Coverage Verification \(Draft\).*?(?=\n## References\n)",
            section,
            text,
            flags=re.DOTALL,
        )
    else:
        text = text.replace("\n## References\n", "\n" + section + "\n## References\n")
    path.write_text(text, encoding="utf-8")


def phase5_section(package_name: str, telemetry: dict[str, Any]) -> str:
    dist = telemetry["SectionCoverageDensityDistribution"]
    return "\n".join([
        "## Phase 5 Coverage Verification (Draft)",
        "",
        f"Gate 5 coverage package: `domains/chirality/_Decomposition/gate5_coverage/{package_name}/`",
        "",
        "This package consumes the accepted Gate 4 ledger and verifies mapping invariants plus section-level atom coverage. It is a draft review surface, not an acceptance snapshot.",
        "",
        "| Metric | Value |",
        "|---|---:|",
        f"| Sources | {telemetry['SourceCount']} |",
        f"| Total sections | {telemetry['SectionCount']} |",
        f"| In-scope sections | {telemetry['InScopeSectionCount']} |",
        f"| Zero-coverage in-scope sections | {telemetry['SectionsWithZeroCoverageCount']} |",
        f"| `cov-empty` sections | {dist['cov-empty']} |",
        f"| `cov-low` sections | {dist['cov-low']} |",
        f"| `cov-mid` sections | {dist['cov-mid']} |",
        f"| `cov-high` sections | {dist['cov-high']} |",
        f"| Unassigned IN units | {telemetry['UnassignedINUnits']} |",
        f"| IN units without KTY mapping | {telemetry['UnitsWithoutKnowledgeTypeMapping']} |",
        "",
        "Gate 5 review surfaces and registers:",
        "",
        "- `Section_Coverage_Register.csv` - per-section atom-density and zero-coverage status.",
        "- `Source_Coverage_Summary.csv` - per-source coverage summary and review HTML paths.",
        "- `Gate5_Coverage_Telemetry.{csv,json}` - required coverage and telemetry summary.",
        f"- `gate5_coverage/{package_name}/coverage_review_html/` - coverage-review HTML surfaces.",
        "",
        f"`{ZERO_COVERAGE_ISSUE_ID}` remains open until zero-coverage sections are attested as scaffold-for-fill/boilerplate or routed back to Phase 2 re-dispatch.",
        "",
    ])


def update_next_prompt(path: Path, generated_iso: str, package_name: str, telemetry: dict[str, Any]) -> None:
    text = path.read_text(encoding="utf-8")
    replacement = f"""## Gate 5 Coverage Proposal State

Gate 5 Coverage verification is drafted and awaits human review.

- Gate 5 coverage package: `domains/chirality/_Decomposition/gate5_coverage/{package_name}`
- Generated UTC: {generated_iso}
- Accepted upstream Gate 4 snapshot: `domains/chirality/_Decomposition/gate_snapshots/GATE4_KTY_20260615T042414Z`
- Coverage ledger: `domains/chirality/_Decomposition/Section_Coverage_Register.csv`
- Source coverage summary: `domains/chirality/_Decomposition/Source_Coverage_Summary.csv`
- Coverage telemetry: `domains/chirality/_Decomposition/Gate5_Coverage_Telemetry.csv` and `.json`
- Review HTML root: `domains/chirality/_Decomposition/gate5_coverage/{package_name}/coverage_review_html/`
- Source count: `{telemetry['SourceCount']}`
- In-scope sections: `{telemetry['InScopeSectionCount']}`
- Zero-coverage in-scope sections: `{telemetry['SectionsWithZeroCoverageCount']}`
- Open coverage issue: `{ZERO_COVERAGE_ISSUE_ID}` pending human attestation or Phase 2 re-dispatch routing.

Gate 5 remains open until the human explicitly confirms coverage and mappings are acceptable, section-coverage gaps have been ruled on, and the open issues list is correct. Do not proceed to Gate 6 publication, hypergraph publication, DBM publication, public export, or separate project-domain decomposition until explicitly authorized.
"""
    if "## Gate 5 Coverage Proposal State" in text:
        text = re.sub(r"## Gate 5 Coverage Proposal State\n.*?(?=\n## Rebuild Commands\n)", replacement + "\n", text, flags=re.DOTALL)
    else:
        text = text.replace("\n## Rebuild Commands\n", "\n" + replacement + "\n## Rebuild Commands\n")

    next_action = f"""## Next Recommended Action

Review the Gate 5 coverage package `domains/chirality/_Decomposition/gate5_coverage/{package_name}`. Open the coverage-review HTML surfaces, inspect `cov-empty` sections, and either attest them as scaffold-for-fill/boilerplate or route affected source units back to Phase 2 re-dispatch. Gate 6 publication must wait for explicit Gate 5 acceptance.
"""
    if "## Next Recommended Action" in text:
        text = re.sub(r"## Next Recommended Action\n.*\Z", next_action, text, flags=re.DOTALL)
    else:
        text += "\n" + next_action
    path.write_text(text, encoding="utf-8")


def update_json_telemetry(path: Path, generated_iso: str, package_name: str, telemetry: dict[str, Any]) -> None:
    data = json.loads(path.read_text(encoding="utf-8"))
    data["generated_utc"] = generated_iso
    data["phase5_status"] = "OPEN_PENDING_HUMAN_COVERAGE_REVIEW"
    data["gate5_coverage_proposal"] = {
        "status": "OPEN_PENDING_HUMAN_COVERAGE_REVIEW",
        "generated_utc": generated_iso,
        "proposal_package": f"domains/chirality/_Decomposition/gate5_coverage/{package_name}",
        "source_count": telemetry["SourceCount"],
        "section_count": telemetry["SectionCount"],
        "in_scope_section_count": telemetry["InScopeSectionCount"],
        "sections_with_zero_coverage": telemetry["SectionsWithZeroCoverageCount"],
        "coverage_density_distribution": telemetry["SectionCoverageDensityDistribution"],
        "open_issue": ZERO_COVERAGE_ISSUE_ID,
    }
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def update_open_issues(path: Path, telemetry: dict[str, Any]) -> None:
    zero_count = int(telemetry["SectionsWithZeroCoverageCount"])
    status = "OPEN_GATE5_HUMAN_COVERAGE_REVIEW" if zero_count else "CLOSED_NO_ZERO_COVERAGE"
    disposition = (
        "Human must attest zero-coverage sections as scaffold-for-fill/boilerplate or route affected source units back to Phase 2 re-dispatch before Gate 5 closure."
        if zero_count
        else "No zero-coverage in-scope sections were found."
    )
    recommendation = (
        "Review Section_Coverage_Register.csv and the coverage-review HTML surfaces, focusing on cov-empty sections."
        if zero_count
        else "Proceed to Gate 5 acceptance review."
    )
    upsert_rows(path, "IssueID", [{
        "IssueID": ZERO_COVERAGE_ISSUE_ID,
        "Status": status,
        "Severity": "MAJOR" if zero_count else "INFO",
        "Surface": "Section_Coverage_Register.csv; gate5_coverage coverage-review HTML",
        "Issue": f"Gate 5 coverage verification found {zero_count} in-scope sections with zero IN atoms.",
        "RequiredDisposition": disposition,
        "Recommendation": recommendation,
    }])


def update_validation_checks(path: Path, package_name: str, telemetry: dict[str, Any], render_count: int) -> None:
    zero_count = int(telemetry["SectionsWithZeroCoverageCount"])
    upsert_rows(path, "CheckID", [
        {
            "CheckID": "GATE5_MAPPING_INVARIANTS",
            "Status": "PASS",
            "Evidence": f"IN={telemetry['INUnitCount']}; unassigned={telemetry['UnassignedINUnits']}; without_kty={telemetry['UnitsWithoutKnowledgeTypeMapping']}; KTYs={telemetry['KnowledgeTypeCount']}; Subjects={telemetry['SubjectCount']}",
            "Notes": "Every IN atom has exactly one Category and at least one KTY/Subject; every KTY/Subject has exactly one parent.",
        },
        {
            "CheckID": "GATE5_SECTION_COVERAGE_REGISTER",
            "Status": "DRAFT_READY",
            "Evidence": f"Section_Coverage_Register.csv sections={telemetry['SectionCount']} in_scope={telemetry['InScopeSectionCount']} zero={zero_count}",
            "Notes": "Section-level coverage density generated from accepted Gate 4 ledger.",
        },
        {
            "CheckID": "GATE5_COVERAGE_REVIEW_HTML",
            "Status": "DRAFT_READY",
            "Evidence": f"coverage_review_html={render_count}; package=gate5_coverage/{package_name}",
            "Notes": "Coverage-review surfaces rendered into the Gate 5 package without overwriting Gate 2 atom-review HTML.",
        },
        {
            "CheckID": "GATE5_ZERO_COVERAGE_REVIEW",
            "Status": "OPEN_PENDING_HUMAN_REVIEW" if zero_count else "PASS_NO_ZERO_COVERAGE",
            "Evidence": f"{ZERO_COVERAGE_ISSUE_ID}; zero_coverage_sections={zero_count}",
            "Notes": "Gate 5 closure requires human attestation or Phase 2 re-dispatch routing for every zero-coverage in-scope section.",
        },
        {
            "CheckID": "GATE5_PROPOSAL_SNAPSHOT",
            "Status": "OPEN_PENDING_HUMAN_APPROVAL",
            "Evidence": f"gate5_coverage/{package_name}",
            "Notes": "Snapshot is a Gate 5 proposal/review package, not an acceptance record.",
        },
    ])


def update_companion_inventory(path: Path, package_name: str) -> None:
    rows = [
        {"Filename": "Section_Coverage_Register.csv", "PackageRole": "authoritative companion register", "Description": "Gate 5 per-section atom coverage density and zero-coverage review status."},
        {"Filename": "Source_Coverage_Summary.csv", "PackageRole": "authoritative companion register", "Description": "Gate 5 per-source coverage summary and review HTML locations."},
        {"Filename": "Gate5_Coverage_Telemetry.csv", "PackageRole": "authoritative companion register", "Description": "Gate 5 required Coverage & Telemetry summary in metric/value CSV form."},
        {"Filename": "Gate5_Coverage_Telemetry.json", "PackageRole": "authoritative companion register", "Description": "Gate 5 required Coverage & Telemetry summary in structured JSON form."},
        {"Filename": "Gate5_Coverage_Review_Packet.md", "PackageRole": "working surface", "Description": "Gate 5 human review packet and closure condition."},
        {"Filename": "gate5_coverage/_LATEST_GATE5_COVERAGE.md", "PackageRole": "snapshot / handoff artifact", "Description": "Pointer to latest Gate 5 coverage proposal package."},
        {"Filename": f"gate5_coverage/{package_name}/GATE5_COVERAGE_REVIEW_PACKET.md", "PackageRole": "snapshot / handoff artifact", "Description": "Immutable Gate 5 coverage review packet for this proposal run."},
        {"Filename": f"gate5_coverage/{package_name}/HANDOFF_STATE.md", "PackageRole": "snapshot / handoff artifact", "Description": "Gate 5 open handoff state and remaining blockers."},
        {"Filename": f"gate5_coverage/{package_name}/coverage_review_html/", "PackageRole": "authoritative companion register", "Description": "Per-source Gate 5 coverage-review HTML surfaces."},
        {"Filename": f"gate5_coverage/{package_name}/coverage_section_nodes/", "PackageRole": "authoritative companion register", "Description": "Section-node CSVs emitted by Gate 5 coverage-review renders."},
        {"Filename": f"gate5_coverage/{package_name}/source_atom_slices/", "PackageRole": "authoritative companion register", "Description": "Per-source slices of the accepted Gate 4 ledger used to render coverage-review HTML."},
    ]
    upsert_rows(path, "Filename", rows)


def main() -> int:
    args = parse_args()
    repo_root = args.repo_root.resolve()
    domain_root = (repo_root / args.domain_root).resolve() if not args.domain_root.is_absolute() else args.domain_root.resolve()
    decomp_root = domain_root / "_Decomposition"
    ts, generated_iso = utc_now()
    if args.timestamp:
        ts = args.timestamp
        generated_iso = datetime.strptime(ts, "%Y%m%dT%H%M%SZ").replace(tzinfo=timezone.utc).isoformat().replace("+00:00", "Z")
    package_name = f"GATE5_COVERAGE_PROPOSAL_{ts}"
    package_dir = decomp_root / "gate5_coverage" / package_name
    package_dir.mkdir(parents=True, exist_ok=True)

    ledger_path = decomp_root / "Domain_Ledger_Gate4_KTY_Draft.csv"
    source_register_path = decomp_root / "Gate2_Source_Unit_Register.csv"
    kty_register_path = decomp_root / "Knowledge_Type_Register.csv"
    subject_register_path = decomp_root / "Knowledge_Subject_Register.csv"

    ledger_rows = read_csv(ledger_path)
    source_rows = read_csv(source_register_path)
    kty_rows = read_csv(kty_register_path)
    subject_rows = read_csv(subject_register_path)

    mapping_status = validate_mappings(ledger_rows, kty_rows, subject_rows)
    if mapping_status["blocking"]:
        print("ERROR: Gate 5 entry mapping invariants failed", file=sys.stderr)
        for key, value in mapping_status.items():
            if isinstance(value, list) and value:
                print(f"{key}: {value[:20]}", file=sys.stderr)
        return 2

    source_docs = {row["SourceDocID"] for row in source_rows}
    ledger_source_docs = {row.get("SourceDoc", "") for row in ledger_rows if row.get("SourceDoc", "")}
    extra_ledger_sources = sorted(ledger_source_docs - source_docs)
    missing_ledger_sources = sorted(source_docs - ledger_source_docs)
    if extra_ledger_sources or missing_ledger_sources:
        print("ERROR: source-unit register and Gate 4 ledger source sets diverge", file=sys.stderr)
        print(f"extra_ledger_sources={extra_ledger_sources[:20]}", file=sys.stderr)
        print(f"missing_ledger_sources={missing_ledger_sources[:20]}", file=sys.stderr)
        return 2

    atom_slice_paths = write_atom_slices(package_dir, source_rows, ledger_rows)
    section_rows, source_summary_rows = build_section_coverage(
        decomp_root=decomp_root,
        source_rows=source_rows,
        ledger_rows=ledger_rows,
        package_dir=package_dir,
        repo_root=repo_root,
    )
    render_logs: list[str] = []
    if not args.skip_render:
        render_logs = render_coverage_html(repo_root, decomp_root, source_rows, package_dir, atom_slice_paths)
        (package_dir / "render_log.txt").write_text("\n".join(render_logs) + "\n", encoding="utf-8")

    telemetry = build_telemetry(
        generated_iso=generated_iso,
        package_name=package_name,
        source_rows=source_rows,
        ledger_rows=ledger_rows,
        section_rows=section_rows,
        source_summary_rows=source_summary_rows,
        kty_rows=kty_rows,
        subject_rows=subject_rows,
        mapping_status=mapping_status,
    )

    section_fieldnames = [
        "SourceDocID", "SourcePrefix", "SourceName", "RepoRelPath", "SourceGroup", "BatchID",
        "SectionID", "Path", "Depth", "Title", "LineStart", "LineEnd", "LineSpan",
        "InScope", "IsFrontMatter", "IsBackMatter", "INAtomCount", "OutAtomCount",
        "TbdAtomCount", "OtherAtomCount", "TotalAtomCount", "AtomsPer50Lines",
        "CoverageClass", "ZeroCoverageFlag", "Gate5ReviewStatus", "CoverageReviewHtmlPath",
        "CoverageReviewHref", "ZeroCoverageIssueID", "AttestationStatus", "AttestationNote",
    ]
    source_fieldnames = [
        "Gate2SourceSeq", "BatchID", "SourceDocID", "SourcePrefix", "SourceName", "RepoRelPath",
        "SourceGroup", "SectionCount", "InScopeSectionCount", "SectionsWithZeroCoverageCount",
        "CovEmptySections", "CovLowSections", "CovMidSections", "CovHighSections", "INAtomCount",
        "OutAtomCount", "TbdAtomCount", "TotalAtomCount", "CoverageReviewHtmlPath",
        "CoverageSectionNodesPath", "CoverageAtomSlicePath", "Status", "Notes",
    ]
    write_csv(decomp_root / "Section_Coverage_Register.csv", section_rows, fieldnames=section_fieldnames)
    write_csv(decomp_root / "Source_Coverage_Summary.csv", source_summary_rows, fieldnames=source_fieldnames)
    write_telemetry_csv(decomp_root / "Gate5_Coverage_Telemetry.csv", telemetry)
    (decomp_root / "Gate5_Coverage_Telemetry.json").write_text(json.dumps(telemetry, indent=2) + "\n", encoding="utf-8")

    write_csv(package_dir / "Section_Coverage_Register.csv", section_rows, fieldnames=section_fieldnames)
    write_csv(package_dir / "Source_Coverage_Summary.csv", source_summary_rows, fieldnames=source_fieldnames)
    write_telemetry_csv(package_dir / "Gate5_Coverage_Telemetry.csv", telemetry)
    (package_dir / "Gate5_Coverage_Telemetry.json").write_text(json.dumps(telemetry, indent=2) + "\n", encoding="utf-8")

    review_packet_root = decomp_root / "Gate5_Coverage_Review_Packet.md"
    review_packet_pkg = package_dir / "GATE5_COVERAGE_REVIEW_PACKET.md"
    write_review_packet(review_packet_root, package_dir, telemetry, section_rows, source_summary_rows, generated_iso)
    review_packet_pkg.write_text(review_packet_root.read_text(encoding="utf-8"), encoding="utf-8")
    write_handoff(package_dir / "HANDOFF_STATE.md", telemetry, generated_iso, package_name)
    latest = decomp_root / "gate5_coverage" / "_LATEST_GATE5_COVERAGE.md"
    latest.write_text(
        "\n".join([
            "# Latest Gate 5 Coverage Proposal",
            "",
            f"Generated UTC: {generated_iso}",
            "",
            f"Current proposal package: `domains/chirality/_Decomposition/gate5_coverage/{package_name}`",
            "",
            f"Review packet: `domains/chirality/_Decomposition/gate5_coverage/{package_name}/GATE5_COVERAGE_REVIEW_PACKET.md`",
            "",
        ]),
        encoding="utf-8",
    )

    update_control_doc(decomp_root / "Chirality_Domain_Decomposition.md", generated_iso, package_name, telemetry)
    update_next_prompt(domain_root / "_Coordination" / "NEXT_INSTANCE_PROMPT.md", generated_iso, package_name, telemetry)
    update_json_telemetry(decomp_root / "Intake_Telemetry.json", generated_iso, package_name, telemetry)
    update_open_issues(decomp_root / "Open_Issues_Register.csv", telemetry)
    update_validation_checks(decomp_root / "Validation_Checks.csv", package_name, telemetry, len(render_logs) if render_logs else len(source_rows))
    update_companion_inventory(decomp_root / "Companion_Inventory.csv", package_name)

    print(
        "Gate 5 coverage package generated: "
        f"{rel(package_dir, repo_root)} sources={telemetry['SourceCount']} "
        f"sections={telemetry['SectionCount']} in_scope={telemetry['InScopeSectionCount']} "
        f"zero={telemetry['SectionsWithZeroCoverageCount']} "
        f"rendered={len(render_logs) if render_logs else 0}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
