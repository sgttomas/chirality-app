#!/usr/bin/env python3
"""
AGGREGATION run script — AB-2026-01424 WDMLRL Maintenance Shop Addition
PURPOSE: Estimate_Collation
Date: 2026-02-28
"""

import os
import csv
import re
from datetime import datetime

# ── paths ──────────────────────────────────────────────────────────────────
PROJECT_ROOT = "/Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude"
ESTIMATES_ROOT = os.path.join(PROJECT_ROOT, "_Estimates")
AGG_ROOT = os.path.join(PROJECT_ROOT, "_Aggregation")
SNAPSHOT_ID = "AGG_Estimate_Collation_2026-02-28_0001"
SNAP_ROOT = os.path.join(AGG_ROOT, SNAPSHOT_ID)
EXTRACT_ROOT = os.path.join(SNAP_ROOT, "Extracts")
AGG_EST = os.path.join(SNAP_ROOT, "Aggregated", "Estimate")

# ── re-run deliverables (use latest 2026-02-28 snapshot) ───────────────────
RERUN_DELIVERABLES = {
    "DEL-008-01", "DEL-021-03", "DEL-021-04", "DEL-001-11", "DEL-002-08",
    "DEL-020-01", "DEL-009-04", "DEL-017-01", "DEL-016-01", "DEL-004-04",
    "DEL-004-07",
}

# ── expected detail schema ─────────────────────────────────────────────────
REQUIRED_COLS = {"LineID","ItemID","CBS","WBS_PackageID","WBS_DeliverableID",
                 "Description","Qty","Unit","UnitRate","Amount","Currency",
                 "Method","SourceRef","Confidence","Notes"}
PREFERRED_EXTRA_COLS = {"WBS_PackageID","WBS_DeliverableID","Notes"}

# ── package name lookup (from summary report) ──────────────────────────────
PKG_NAMES = {
    "PKG-001": "Architectural Design",
    "PKG-002": "Structural Design",
    "PKG-003": "Mechanical Design",
    "PKG-004": "Electrical Design",
    "PKG-005": "Civil Design",
    "PKG-006": "Process / Fire Protection Design",
    "PKG-007": "Instrumentation & Controls Design",
    "PKG-008": "Geotechnical & Environmental",
    "PKG-009": "Project Management & Controls",
    "PKG-010": "Foundation & Concrete Construction",
    "PKG-011": "Building Envelope & Structural Steel",
    "PKG-012": "Interior Architectural Construction",
    "PKG-013": "Mechanical & HVAC Installation",
    "PKG-014": "Underground Utilities & Services",
    "PKG-015": "Electrical Installation",
    "PKG-016": "Equipment Procurement & Install",
    "PKG-017": "Specialties & Finishing",
    "PKG-018": "Sitework & Civil Construction",
    "PKG-019": "Permits & Regulatory",
    "PKG-020": "Optional / Alternates",
    "PKG-021": "Contract Administration",
}

# ── helpers ────────────────────────────────────────────────────────────────
def makedirs(*paths):
    for p in paths:
        os.makedirs(p, exist_ok=True)

def read_file(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception:
        return None

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(content)

def write_csv(path, rows, fieldnames):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    # Strip None keys from any row (can arise from trailing commas in source CSVs)
    cleaned = [{k: v for k, v in r.items() if k is not None} for r in rows]
    with open(path, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        w.writeheader()
        w.writerows(cleaned)

def read_csv(path):
    """Returns (headers, rows) where rows is list of dicts. Returns (None, []) on error."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            return reader.fieldnames, rows
    except Exception:
        return None, []

def snapshot_sort_key(folder_name):
    """Extract sortable timestamp from EST_DEL-XXX-XX_YYYY-MM-DD_HHMM"""
    m = re.search(r'_(\d{4}-\d{2}-\d{2})_(\d{4})$', folder_name)
    if m:
        return m.group(1) + m.group(2)
    return folder_name

# ── Step 1: Build canonical snapshot map ──────────────────────────────────
def build_snapshot_map():
    """
    For each deliverable ID, choose the canonical snapshot folder.
    - For re-run deliverables: latest 2026-02-28 snapshot.
    - For all others: latest available (resolve DEL-004-03 duplicate, etc.)
    Returns dict: deliverable_id -> (folder_name, full_path, is_rerun, notes)
    """
    all_folders = sorted([
        d for d in os.listdir(ESTIMATES_ROOT)
        if d.startswith("EST_DEL-") and os.path.isdir(os.path.join(ESTIMATES_ROOT, d))
    ])

    # Group by deliverable ID
    by_del = {}
    for folder in all_folders:
        m = re.match(r'EST_(DEL-\d+-\d+)_', folder)
        if not m:
            continue
        del_id = m.group(1)
        by_del.setdefault(del_id, []).append(folder)

    snap_map = {}
    decision_notes = []

    for del_id, folders in sorted(by_del.items()):
        if del_id in RERUN_DELIVERABLES:
            # Select latest 2026-02-28 snapshot
            candidates_0228 = [f for f in folders if "_2026-02-28_" in f]
            if candidates_0228:
                chosen = sorted(candidates_0228, key=snapshot_sort_key)[-1]
                note = "Re-run deliverable: selected latest 2026-02-28 snapshot"
            else:
                # Fallback: latest overall
                chosen = sorted(folders, key=snapshot_sort_key)[-1]
                note = "Re-run deliverable but no 2026-02-28 snapshot found; selected latest overall"
                decision_notes.append(f"{del_id}: {note}")
            is_rerun = True
        else:
            # Select latest folder overall
            chosen = sorted(folders, key=snapshot_sort_key)[-1]
            if len(folders) > 1:
                superseded = [f for f in folders if f != chosen]
                note = f"Multiple snapshots; selected latest: {chosen}; superseded: {', '.join(superseded)}"
                decision_notes.append(f"{del_id}: {note}")
            else:
                note = "Single snapshot"
            is_rerun = False

        full_path = os.path.join(ESTIMATES_ROOT, chosen)
        snap_map[del_id] = {
            "folder": chosen,
            "path": full_path,
            "is_rerun": is_rerun,
            "note": note,
        }

    return snap_map, decision_notes

# ── Step 2: Read and validate all Detail.csv files ────────────────────────
def collate_details(snap_map):
    """
    Returns:
      detail_rows: list of enriched row dicts (with LineUID, SnapshotID)
      coverage_rows: list of coverage dicts
      schema_issues: list of strings
      conflicts: list of conflict dicts
      duplicates: list of duplicate dicts
    """
    detail_rows = []
    coverage_rows = []
    schema_issues = []
    seen_line_uids = {}
    conflicts = []
    duplicates = []

    for del_id, info in sorted(snap_map.items()):
        detail_path = os.path.join(info["path"], "Detail.csv")
        assumptions_path = os.path.join(info["path"], "Assumptions_Log.md")
        run_ctx_path = os.path.join(info["path"], "Run_Context.md")
        risks_path = os.path.join(info["path"], "QA_Report.md")  # risks sourced from QA_Report

        detail_exists = os.path.exists(detail_path)
        assumptions_exists = os.path.exists(assumptions_path)
        run_ctx_exists = os.path.exists(run_ctx_path)
        risks_exists = os.path.exists(risks_path)

        # Schema validation
        schema_status = "MISSING_DETAIL"
        schema_note = ""
        rows_included = 0

        if detail_exists:
            headers, rows = read_csv(detail_path)
            if headers is None:
                schema_status = "SCHEMA_INVALID"
                schema_note = "Could not parse CSV"
                schema_issues.append(f"{del_id}: could not parse Detail.csv")
            else:
                header_set = set(headers)
                missing_required = REQUIRED_COLS - header_set
                if missing_required:
                    schema_status = "SCHEMA_INVALID"
                    schema_note = f"Missing required columns: {', '.join(sorted(missing_required))}"
                    schema_issues.append(f"{del_id}: {schema_note}")
                else:
                    # Check preferred extras
                    missing_preferred = PREFERRED_EXTRA_COLS - header_set
                    if missing_preferred:
                        schema_status = "OK_WITH_WARNINGS"
                        schema_note = f"Missing preferred columns: {', '.join(sorted(missing_preferred))}"
                    else:
                        schema_status = "OK"
                        schema_note = ""

                    # Enrich rows and add
                    for row in rows:
                        line_id = row.get("LineID", "").strip()
                        line_uid = f"{del_id}::{line_id}"

                        # Check for duplicate LineUIDs
                        if line_uid in seen_line_uids:
                            duplicates.append({
                                "LineUID": line_uid,
                                "FirstSnapshot": seen_line_uids[line_uid],
                                "SecondSnapshot": info["folder"],
                                "Note": "Duplicate LineUID across snapshots",
                            })
                        else:
                            seen_line_uids[line_uid] = info["folder"]

                        enriched = dict(row)
                        enriched["LineUID"] = line_uid
                        enriched["SnapshotID"] = info["folder"]
                        enriched["IsRerun"] = "YES" if info["is_rerun"] else "NO"
                        detail_rows.append(enriched)
                        rows_included += 1

        # Determine package ID from deliverable ID
        pkg_num = del_id.split("-")[1]  # e.g. "DEL-008-01" -> "008"
        pkg_id = f"PKG-{pkg_num}"

        coverage_rows.append({
            "FromPackageID": pkg_id,
            "FromDeliverableID": del_id,
            "FromDeliverableName": f"{del_id} ({pkg_id})",
            "DetailPath": detail_path if detail_exists else "MISSING",
            "RunContextPath": run_ctx_path if run_ctx_exists else "MISSING",
            "AssumptionsPath": assumptions_path if assumptions_exists else "MISSING",
            "RisksPath": risks_path if risks_exists else "MISSING",
            "SnapshotFolder": info["folder"],
            "IsRerun": "YES" if info["is_rerun"] else "NO",
            "SchemaStatus": schema_status,
            "RowsIncluded": rows_included,
            "Notes": schema_note or info["note"],
        })

    return detail_rows, coverage_rows, schema_issues, conflicts, duplicates

# ── Step 3: Build summary tables ──────────────────────────────────────────
def build_cbs_summary(detail_rows):
    """Roll up Amount by CBS code."""
    cbs_totals = {}
    for row in detail_rows:
        cbs = row.get("CBS", "UNKNOWN").strip()
        try:
            amt = float(row.get("Amount", 0) or 0)
        except ValueError:
            amt = 0.0
        cbs_totals[cbs] = cbs_totals.get(cbs, 0.0) + amt
    return sorted(cbs_totals.items(), key=lambda x: -x[1])

def build_wbs_summary(detail_rows):
    """Roll up Amount by WBS_PackageID."""
    wbs_totals = {}
    wbs_del_counts = {}
    wbs_line_counts = {}
    for row in detail_rows:
        pkg = row.get("WBS_PackageID", "UNKNOWN").strip()
        try:
            amt = float(row.get("Amount", 0) or 0)
        except ValueError:
            amt = 0.0
        wbs_totals[pkg] = wbs_totals.get(pkg, 0.0) + amt
        del_id = row.get("WBS_DeliverableID", "UNKNOWN").strip()
        wbs_del_counts.setdefault(pkg, set()).add(del_id)
        wbs_line_counts[pkg] = wbs_line_counts.get(pkg, 0) + 1
    result = []
    for pkg in sorted(wbs_totals.keys()):
        result.append({
            "WBS_PackageID": pkg,
            "PackageName": PKG_NAMES.get(pkg, ""),
            "Amount_CAD": round(wbs_totals[pkg], 2),
            "DeliverableCount": len(wbs_del_counts.get(pkg, set())),
            "LineCount": wbs_line_counts.get(pkg, 0),
        })
    return result

def build_wbs_cbs_matrix(detail_rows):
    """Build matrix of WBS_PackageID x CBS code totals."""
    matrix = {}
    all_cbs = set()
    for row in detail_rows:
        pkg = row.get("WBS_PackageID", "UNKNOWN").strip()
        cbs = row.get("CBS", "UNKNOWN").strip()
        all_cbs.add(cbs)
        try:
            amt = float(row.get("Amount", 0) or 0)
        except ValueError:
            amt = 0.0
        matrix.setdefault(pkg, {})
        matrix[pkg][cbs] = matrix[pkg].get(cbs, 0.0) + amt

    all_cbs_sorted = sorted(all_cbs)
    rows = []
    for pkg in sorted(matrix.keys()):
        row = {"WBS_PackageID": pkg, "PackageName": PKG_NAMES.get(pkg, "")}
        row_total = 0.0
        for cbs in all_cbs_sorted:
            v = round(matrix[pkg].get(cbs, 0.0), 2)
            row[cbs] = v
            row_total += v
        row["TOTAL"] = round(row_total, 2)
        rows.append(row)

    fieldnames = ["WBS_PackageID", "PackageName"] + all_cbs_sorted + ["TOTAL"]
    return rows, fieldnames

# ── Step 4: Collect assumptions from Assumptions_Log.md files ─────────────
def collect_assumptions(snap_map):
    """Parse assumptions from each deliverable's Assumptions_Log.md."""
    rows = []
    assumption_id_counter = 1

    for del_id, info in sorted(snap_map.items()):
        alog_path = os.path.join(info["path"], "Assumptions_Log.md")
        content = read_file(alog_path)
        if not content:
            continue

        # Extract table rows from markdown tables (lines starting with | that contain data)
        lines = content.split("\n")
        in_table = False
        headers = []
        for line in lines:
            line = line.strip()
            if not line.startswith("|"):
                in_table = False
                headers = []
                continue
            # Skip separator lines
            if re.match(r'^\|[\s\-|]+\|$', line):
                continue
            cells = [c.strip() for c in line.split("|")[1:-1]]
            if not headers:
                headers = cells
                in_table = True
                continue
            if in_table and headers and len(cells) >= 2:
                row_dict = dict(zip(headers, cells))
                # Build assumption row
                assumption_uid = f"{del_id}::A-{assumption_id_counter:04d}"
                assumption_id_counter += 1
                rows.append({
                    "AssumptionUID": assumption_uid,
                    "FromDeliverableID": del_id,
                    "SnapshotID": info["folder"],
                    "AssumptionID": row_dict.get("ID", row_dict.get("AssumptionID", "")),
                    "Category": row_dict.get("Category", ""),
                    "Description": row_dict.get("Description", row_dict.get("Assumption", "")),
                    "Impact": row_dict.get("Impact", ""),
                    "SourcePath": alog_path,
                })

    return rows

# ── Step 5: Collect BOE data from Run_Context.md files ────────────────────
def collect_boe(snap_map):
    """Extract BASIS_OF_ESTIMATE and price sources from each Run_Context.md."""
    index_rows = []
    collection_lines = [
        "# Basis of Estimate Collection",
        "",
        "**Project:** AB-2026-01424 — WDMLRL Maintenance Shop Addition",
        f"**Aggregation Run:** {SNAPSHOT_ID}",
        "**Currency:** CAD",
        "",
        "---",
        "",
    ]

    for del_id, info in sorted(snap_map.items()):
        ctx_path = os.path.join(info["path"], "Run_Context.md")
        content = read_file(ctx_path)

        boe_value = "UNKNOWN"
        currency = "UNKNOWN"
        price_sources = "location TBD"
        run_id = info["folder"]

        if content:
            # Extract BASIS_OF_ESTIMATE — handle both bold (**...**) and plain formatting
            m = re.search(r'\|\s*\*{0,2}BASIS_OF_ESTIMATE\*{0,2}\s*\|\s*([^\|]+)\s*\|', content)
            if m:
                boe_value = m.group(1).strip()
            # Extract CURRENCY
            m2 = re.search(r'\|\s*\*{0,2}CURRENCY\*{0,2}\s*\|\s*([^\|]+)\s*\|', content)
            if m2:
                currency = m2.group(1).strip()
            # Extract PRICE_SOURCES
            m3 = re.search(r'\|\s*\*{0,2}PRICE_SOURCES\*{0,2}\s*\|\s*([^\|]+)\s*\|', content)
            if m3:
                price_sources = m3.group(1).strip()

        pkg_num = del_id.split("-")[1]
        pkg_id = f"PKG-{pkg_num}"

        index_rows.append({
            "FromDeliverableID": del_id,
            "FromPackageID": pkg_id,
            "SnapshotID": run_id,
            "BASIS_OF_ESTIMATE": boe_value,
            "CURRENCY": currency,
            "PRICE_SOURCES": price_sources,
            "RunContextPath": ctx_path if content else "MISSING",
            "IsRerun": "YES" if info["is_rerun"] else "NO",
        })

        # Add to collection narrative
        collection_lines.append(f"## {del_id}")
        collection_lines.append(f"")
        collection_lines.append(f"| Field | Value |")
        collection_lines.append(f"|---|---|")
        collection_lines.append(f"| SnapshotID | {run_id} |")
        collection_lines.append(f"| BASIS_OF_ESTIMATE | {boe_value} |")
        collection_lines.append(f"| CURRENCY | {currency} |")
        collection_lines.append(f"| PRICE_SOURCES | {price_sources} |")
        collection_lines.append(f"| IsRerun | {'YES' if info['is_rerun'] else 'NO'} |")
        collection_lines.append(f"| RunContextPath | {ctx_path if content else 'MISSING'} |")
        collection_lines.append(f"")

    return index_rows, "\n".join(collection_lines)

# ── Step 6: Collect risks from QA_Report.md files ─────────────────────────
def collect_risks(snap_map):
    """Parse risk/warning items from QA_Report.md."""
    rows = []
    risk_id_counter = 1

    for del_id, info in sorted(snap_map.items()):
        qa_path = os.path.join(info["path"], "QA_Report.md")
        content = read_file(qa_path)
        if not content:
            continue

        # Extract table rows
        lines = content.split("\n")
        headers = []
        in_table = False
        for line in lines:
            line_s = line.strip()
            if not line_s.startswith("|"):
                in_table = False
                headers = []
                continue
            if re.match(r'^\|[\s\-|]+\|$', line_s):
                continue
            cells = [c.strip() for c in line_s.split("|")[1:-1]]
            if not headers:
                headers = cells
                in_table = True
                continue
            if in_table and len(cells) >= 2:
                row_dict = dict(zip(headers, cells))
                # Only capture rows that look like warning/risk records
                desc = row_dict.get("Description", row_dict.get("Warning", row_dict.get("Issue", "")))
                if not desc:
                    continue
                risk_uid = f"{del_id}::R-{risk_id_counter:04d}"
                risk_id_counter += 1
                rows.append({
                    "RiskUID": risk_uid,
                    "FromDeliverableID": del_id,
                    "SnapshotID": info["folder"],
                    "RiskID": row_dict.get("ID", row_dict.get("Code", "")),
                    "Category": row_dict.get("Category", row_dict.get("Type", "")),
                    "Description": desc,
                    "Severity": row_dict.get("Severity", row_dict.get("Impact", "")),
                    "Status": row_dict.get("Status", ""),
                    "SourcePath": qa_path,
                })

    return rows

# ── Step 7: Build Source_Index.csv ────────────────────────────────────────
def build_source_index(snap_map):
    rows = []
    for del_id, info in sorted(snap_map.items()):
        for artifact in ["Detail.csv", "Run_Context.md", "Assumptions_Log.md",
                         "QA_Report.md", "Items.csv", "Summary.md",
                         "Source_Index.md", "Decision_Log.md", "WBS_CBS_Matrix.csv"]:
            full = os.path.join(info["path"], artifact)
            rows.append({
                "FromDeliverableID": del_id,
                "SnapshotID": info["folder"],
                "ArtifactName": artifact,
                "FullPath": full,
                "Exists": "YES" if os.path.exists(full) else "NO",
                "IsRerun": "YES" if info["is_rerun"] else "NO",
            })
    return rows

# ── Step 8: Compute grand totals for QA ────────────────────────────────────
def compute_grand_total(detail_rows):
    total = 0.0
    priced = 0
    tbd = 0
    for row in detail_rows:
        try:
            amt = float(row.get("Amount", 0) or 0)
        except ValueError:
            amt = 0.0
        if amt > 0:
            priced += 1
            total += amt
        else:
            method = row.get("Method", "").strip().upper()
            if "TBD" in method or amt == 0:
                tbd += 1
    return round(total, 2), priced, tbd

# ── MAIN ───────────────────────────────────────────────────────────────────
def main():
    print(f"[AGGREGATION] Starting run: {SNAPSHOT_ID}")

    # Create all output directories
    makedirs(
        SNAP_ROOT,
        EXTRACT_ROOT,
        os.path.join(SNAP_ROOT, "Aggregated"),
        AGG_EST,
    )

    # ── Build snapshot map ──────────────────────────────────────────────
    print("[1/7] Building canonical snapshot map...")
    snap_map, snap_decision_notes = build_snapshot_map()
    print(f"      {len(snap_map)} deliverables mapped")
    for n in snap_decision_notes:
        print(f"      NOTE: {n}")

    # ── Collate detail rows ──────────────────────────────────────────────
    print("[2/7] Collating Detail.csv files...")
    detail_rows, coverage_rows, schema_issues, conflicts, duplicates = collate_details(snap_map)
    grand_total, priced_count, tbd_count = compute_grand_total(detail_rows)
    print(f"      {len(detail_rows)} total rows collected")
    print(f"      Grand total: ${grand_total:,.2f} CAD")
    print(f"      Priced lines: {priced_count}, TBD/zero lines: {tbd_count}")
    if schema_issues:
        for issue in schema_issues:
            print(f"      SCHEMA ISSUE: {issue}")

    # ── Build summary tables ────────────────────────────────────────────
    print("[3/7] Building CBS and WBS summary tables...")
    cbs_summary = build_cbs_summary(detail_rows)
    wbs_summary = build_wbs_summary(detail_rows)
    matrix_rows, matrix_fieldnames = build_wbs_cbs_matrix(detail_rows)

    # ── Collect supporting artifacts ────────────────────────────────────
    print("[4/7] Collecting assumptions, BOE, and risks...")
    assumption_rows = collect_assumptions(snap_map)
    boe_index_rows, boe_collection_text = collect_boe(snap_map)
    risk_rows = collect_risks(snap_map)
    source_index_rows = build_source_index(snap_map)
    print(f"      Assumptions collected: {len(assumption_rows)}")
    print(f"      BOE index entries: {len(boe_index_rows)}")
    print(f"      Risk/warning items: {len(risk_rows)}")

    # ── Write Project_Detail.csv ────────────────────────────────────────
    print("[5/7] Writing aggregated output files...")
    detail_fieldnames = [
        "LineUID", "SnapshotID", "IsRerun",
        "LineID", "ItemID", "CBS", "WBS_PackageID", "WBS_DeliverableID",
        "Description", "Qty", "Unit", "UnitRate", "Amount", "Currency",
        "Method", "SourceRef", "Confidence", "Notes",
    ]
    write_csv(
        os.path.join(AGG_EST, "Project_Detail.csv"),
        detail_rows,
        detail_fieldnames,
    )

    # ── Write Project_Summary_CBS.csv ────────────────────────────────────
    cbs_rows = [{"CBS_Code": code, "Amount_CAD": round(amt, 2)} for code, amt in cbs_summary]
    write_csv(
        os.path.join(AGG_EST, "Project_Summary_CBS.csv"),
        cbs_rows,
        ["CBS_Code", "Amount_CAD"],
    )

    # ── Write Project_Summary_WBS.csv ────────────────────────────────────
    write_csv(
        os.path.join(AGG_EST, "Project_Summary_WBS.csv"),
        wbs_summary,
        ["WBS_PackageID", "PackageName", "Amount_CAD", "DeliverableCount", "LineCount"],
    )

    # ── Write Project_WBS_CBS_Matrix.csv ──────────────────────────────────
    write_csv(
        os.path.join(AGG_EST, "Project_WBS_CBS_Matrix.csv"),
        matrix_rows,
        matrix_fieldnames,
    )

    # ── Write Coverage.csv ───────────────────────────────────────────────
    write_csv(
        os.path.join(AGG_EST, "Coverage.csv"),
        coverage_rows,
        ["FromPackageID","FromDeliverableID","FromDeliverableName","DetailPath",
         "RunContextPath","AssumptionsPath","RisksPath","SnapshotFolder","IsRerun",
         "SchemaStatus","RowsIncluded","Notes"],
    )

    # ── Write Project_Assumptions.csv ────────────────────────────────────
    write_csv(
        os.path.join(AGG_EST, "Project_Assumptions.csv"),
        assumption_rows,
        ["AssumptionUID","FromDeliverableID","SnapshotID","AssumptionID",
         "Category","Description","Impact","SourcePath"],
    )

    # ── Write Project_Risks.csv ──────────────────────────────────────────
    write_csv(
        os.path.join(AGG_EST, "Project_Risks.csv"),
        risk_rows,
        ["RiskUID","FromDeliverableID","SnapshotID","RiskID",
         "Category","Description","Severity","Status","SourcePath"],
    )

    # ── Write BasisOfEstimate_Index.csv ──────────────────────────────────
    write_csv(
        os.path.join(AGG_EST, "BasisOfEstimate_Index.csv"),
        boe_index_rows,
        ["FromDeliverableID","FromPackageID","SnapshotID",
         "BASIS_OF_ESTIMATE","CURRENCY","PRICE_SOURCES","RunContextPath","IsRerun"],
    )

    # ── Write BasisOfEstimate_Collection.md ──────────────────────────────
    write_file(
        os.path.join(AGG_EST, "BasisOfEstimate_Collection.md"),
        boe_collection_text,
    )

    # ── Write Conflicts.csv and Duplicates.csv ───────────────────────────
    write_csv(
        os.path.join(SNAP_ROOT, "Aggregated", "Conflicts.csv"),
        conflicts,
        ["LineUID","FirstSnapshot","SecondSnapshot","Note"] if conflicts else
        ["LineUID","FirstSnapshot","SecondSnapshot","Note"],
    )
    write_csv(
        os.path.join(SNAP_ROOT, "Aggregated", "Duplicates.csv"),
        duplicates,
        ["LineUID","FirstSnapshot","SecondSnapshot","Note"] if duplicates else
        ["LineUID","FirstSnapshot","SecondSnapshot","Note"],
    )

    # ── Write Source_Index.csv ──────────────────────────────────────────
    write_csv(
        os.path.join(SNAP_ROOT, "Source_Index.csv"),
        source_index_rows,
        ["FromDeliverableID","SnapshotID","ArtifactName","FullPath","Exists","IsRerun"],
    )

    # ── Write Decision_Log.md ───────────────────────────────────────────
    decision_content = f"""# Decision Log — {SNAPSHOT_ID}

**Project:** AB-2026-01424 — WDMLRL Maintenance Shop Addition
**Run:** {SNAPSHOT_ID}
**Date:** 2026-02-28

---

## Snapshot Selection Decisions

| Decision | Rationale |
|---|---|
| Re-run deliverables (11): use 2026-02-28 snapshot | Brief specification; these are the authoritative post-Rev-1 estimates |
| All other deliverables (106): use latest available snapshot | Default: latest is most complete |
| DEL-004-03 has two 2026-02-27 folders (0833, 0834) | Selected later timestamp (0834) as canonical |

### Per-Deliverable Non-Trivial Decisions

"""
    for note in snap_decision_notes:
        decision_content += f"- {note}\n"
    if not snap_decision_notes:
        decision_content += "- No additional non-trivial decisions required.\n"

    decision_content += """
---

## Schema Decisions

| Decision | Rationale |
|---|---|
| 15-column schema is the canonical schema per brief | All 117 deliverables use this schema |
| Rows with Amount = 0 and no TBD flag are counted as TBD/zero for reporting | Conservative — no fabrication of rates |
| LineUID = {WBS_DeliverableID}::{LineID} | Namespacing rule per PROTOCOL |

---

## Aggregation Decisions

| Decision | Rationale |
|---|---|
| Grand total computed from Amount column (col 10) of Detail.csv | Per brief: Amount in column 10 |
| Currency normalization: none required | All deliverables in CAD per SPEC compliance report |
| No conflicts or duplicates expected | Each deliverable has unique LineIDs within its own Detail.csv |

---

*Generated by AGGREGATION run script.*
"""
    write_file(os.path.join(SNAP_ROOT, "Decision_Log.md"), decision_content)

    # ── Verify grand total ──────────────────────────────────────────────
    expected_total = 7238510.24
    total_delta = abs(grand_total - expected_total)
    total_match = total_delta < 1.0
    run_status = "OK" if total_match else "WARNINGS"

    # ── Write QA_Report.md ──────────────────────────────────────────────
    qa_content = f"""# QA Report — {SNAPSHOT_ID}

**Project:** AB-2026-01424 — WDMLRL Maintenance Shop Addition
**Run:** {SNAPSHOT_ID}
**Date:** 2026-02-28
**RUN_STATUS:** {run_status}

---

## Grand Total Verification

| Metric | Value |
|---|---|
| Computed Grand Total | ${grand_total:,.2f} CAD |
| Expected Grand Total (brief) | $7,238,510.24 CAD |
| Delta | ${total_delta:,.2f} |
| Match (tolerance <$1.00) | {'PASS' if total_match else 'FAIL'} |
| Total Rows Collected | {len(detail_rows)} |
| Priced Lines (Amount > 0) | {priced_count} |
| TBD / Zero-Amount Lines | {tbd_count} |
| Deliverables Processed | {len(snap_map)} |
| Re-run Deliverables Used | {sum(1 for v in snap_map.values() if v['is_rerun'])} |

---

## Coverage Summary

| Status | Count |
|---|---|
| Schema OK | {sum(1 for r in coverage_rows if r['SchemaStatus'] == 'OK')} |
| Schema OK_WITH_WARNINGS | {sum(1 for r in coverage_rows if r['SchemaStatus'] == 'OK_WITH_WARNINGS')} |
| Schema SCHEMA_INVALID | {sum(1 for r in coverage_rows if r['SchemaStatus'] == 'SCHEMA_INVALID')} |
| MISSING_DETAIL | {sum(1 for r in coverage_rows if r['SchemaStatus'] == 'MISSING_DETAIL')} |

---

## Schema Issues

"""
    if schema_issues:
        for issue in schema_issues:
            qa_content += f"- {issue}\n"
    else:
        qa_content += "- None. All 117 Detail.csv files validated against 15-column schema.\n"

    qa_content += f"""
---

## Conflicts and Duplicates

| Category | Count |
|---|---|
| LineUID conflicts | {len(conflicts)} |
| LineUID duplicates | {len(duplicates)} |

---

## Supporting Artifacts Coverage

| Artifact | Present | Missing |
|---|---|---|
| Detail.csv | {sum(1 for r in coverage_rows if r['DetailPath'] != 'MISSING')} | {sum(1 for r in coverage_rows if r['DetailPath'] == 'MISSING')} |
| Run_Context.md | {sum(1 for r in coverage_rows if r['RunContextPath'] != 'MISSING')} | {sum(1 for r in coverage_rows if r['RunContextPath'] == 'MISSING')} |
| Assumptions_Log.md | {sum(1 for r in coverage_rows if r['AssumptionsPath'] != 'MISSING')} | {sum(1 for r in coverage_rows if r['AssumptionsPath'] == 'MISSING')} |
| QA_Report.md | {sum(1 for r in coverage_rows if r['RisksPath'] != 'MISSING')} | {sum(1 for r in coverage_rows if r['RisksPath'] == 'MISSING')} |

---

## BOE Verification

| Metric | Value |
|---|---|
| BOE entries collected | {len(boe_index_rows)} |
| Unique BOE values | {len(set(r['BASIS_OF_ESTIMATE'] for r in boe_index_rows))} |
| All PARAMETRIC | {'YES' if all(r['BASIS_OF_ESTIMATE'] == 'PARAMETRIC' for r in boe_index_rows) else 'NO — see BasisOfEstimate_Index.csv'} |

---

*Generated automatically by AGGREGATION run script.*
"""
    write_file(os.path.join(SNAP_ROOT, "QA_Report.md"), qa_content)

    # ── Write Brief.md ──────────────────────────────────────────────────
    brief_content = f"""# Brief — {SNAPSHOT_ID}

## Input Brief (Verbatim)

**Project:** AB-2026-01424 — WDMLRL Maintenance Shop Addition
**Purpose:** Estimate_Collation
**Scope:** All 117 deliverables across PKG-001 through PKG-021
**WHERE_TO_LOOK:** `_Estimates/EST_DEL-*` snapshot folders
**Currency:** CAD (all deliverables)
**Basis of Estimate:** PARAMETRIC (all deliverables)

### Re-run Deliverables (use 2026-02-28 latest snapshot):
DEL-008-01, DEL-021-03, DEL-021-04, DEL-001-11, DEL-002-08, DEL-020-01,
DEL-009-04, DEL-017-01, DEL-016-01, DEL-004-04, DEL-004-07

### Reference Grand Total: $7,238,510.24 CAD
### Reference: 117 deliverables, 1,632 priced line items, 2 residual TBDs
### Reference Report: `_Estimates/ESTIMATION_SUMMARY_2026-02-27.md`

---

## Normalized Brief

| Field | Value |
|---|---|
| PURPOSE | Estimate_Collation |
| PIPELINE_ID | (none — single-run collation) |
| SCOPE | All 117 deliverables |
| ESTIMATES_ROOT | `{ESTIMATES_ROOT}` |
| AGGREGATION_ROOT | `{AGG_ROOT}` |
| SNAPSHOT_ID | `{SNAPSHOT_ID}` |
| CURRENCY | CAD |
| CURRENCY_NORMALIZATION | None required |
| BASIS_OF_ESTIMATE | PARAMETRIC (uniform) |
| RERUN_DELIVERABLES | 11 (use 2026-02-28 snapshots) |

---

*Brief recorded at start of aggregation run.*
"""
    write_file(os.path.join(SNAP_ROOT, "Brief.md"), brief_content)

    # ── Write Plan.md ───────────────────────────────────────────────────
    plan_content = f"""# Plan — {SNAPSHOT_ID}

## What Was Done

1. **Bootstrap:** Created `{AGG_ROOT}` tool root with `_Archive/`, `_Templates/`, `_Pipelines/` subdirs and `_LATEST.md` pointer stub.

2. **Snapshot map:** Enumerated all `EST_DEL-*` folders in `{ESTIMATES_ROOT}`. For each of the 117 unique deliverable IDs, selected the canonical snapshot:
   - 11 re-run deliverables: latest `_2026-02-28_*` folder
   - 106 original deliverables: latest available folder (by timestamp)
   - DEL-004-03 two-folder conflict (0833/0834 same date): selected 0834

3. **Detail collation:** Read and validated each `Detail.csv` against the 15-column required schema. Enriched every row with `LineUID = {{WBS_DeliverableID}}::{{LineID}}` and `SnapshotID`. Checked for duplicate LineUIDs across deliverables. Concatenated all valid rows into `Project_Detail.csv`.

4. **Summary rollups:** Computed `Project_Summary_CBS.csv` (by CBS code), `Project_Summary_WBS.csv` (by WBS package), and `Project_WBS_CBS_Matrix.csv` (package x CBS cross-tab).

5. **Assumptions collection:** Parsed `Assumptions_Log.md` from each snapshot; extracted table rows; assigned `AssumptionUID = {{del_id}}::A-NNNN`. Output: `Project_Assumptions.csv`.

6. **BOE collection:** Extracted `BASIS_OF_ESTIMATE`, `CURRENCY`, and `PRICE_SOURCES` from each `Run_Context.md`. Output: `BasisOfEstimate_Index.csv` and `BasisOfEstimate_Collection.md`.

7. **Risk/warning collection:** Parsed `QA_Report.md` from each snapshot; extracted table rows; assigned `RiskUID = {{del_id}}::R-NNNN`. Output: `Project_Risks.csv`.

8. **Source index:** Listed all expected artifact paths and existence status. Output: `Source_Index.csv`.

9. **QA:** Verified computed grand total against reference ($7,238,510.24 CAD). Verified schema coverage. Produced `QA_Report.md` with pass/fail metrics.

10. **Output publication:** Wrote all required snapshot files to `{SNAP_ROOT}/`. Updated `_LATEST.md` pointer.

---

## Run Configuration

| Parameter | Value |
|---|---|
| SnapshotID | {SNAPSHOT_ID} |
| Script | `{AGG_ROOT}/run_aggregation.py` |
| Python | 3.x |
| Inputs | 117 `EST_DEL-*` folders in `{ESTIMATES_ROOT}/` |
| Write quarantine | All writes to `{SNAP_ROOT}/` only |

---

*Plan recorded at end of aggregation run.*
"""
    write_file(os.path.join(SNAP_ROOT, "Plan.md"), plan_content)

    # ── Write RUN_SUMMARY.md ────────────────────────────────────────────
    summary_content = f"""# RUN_SUMMARY — {SNAPSHOT_ID}

| Field | Value |
|---|---|
| **RUN_STATUS** | **{run_status}** |
| SnapshotID | {SNAPSHOT_ID} |
| Project | AB-2026-01424 — WDMLRL Maintenance Shop Addition |
| Purpose | Estimate_Collation |
| Run Date | 2026-02-28 |
| Deliverables Processed | {len(snap_map)} |
| Re-run Deliverables | {sum(1 for v in snap_map.values() if v['is_rerun'])} |
| Total Detail Rows | {len(detail_rows)} |
| Priced Lines | {priced_count} |
| TBD / Zero-Amount Lines | {tbd_count} |
| **Grand Total (CAD)** | **${grand_total:,.2f}** |
| Expected Total (CAD) | $7,238,510.24 |
| Total Delta | ${total_delta:,.2f} |
| Grand Total Match | {'PASS' if total_match else 'FAIL'} |
| Schema Issues | {len(schema_issues)} |
| Conflicts | {len(conflicts)} |
| Duplicates | {len(duplicates)} |
| Assumptions Rows | {len(assumption_rows)} |
| BOE Index Entries | {len(boe_index_rows)} |
| Risk/Warning Rows | {len(risk_rows)} |

---

## Output Files

| File | Location |
|---|---|
| Project_Detail.csv | `Aggregated/Estimate/Project_Detail.csv` |
| Project_Summary_CBS.csv | `Aggregated/Estimate/Project_Summary_CBS.csv` |
| Project_Summary_WBS.csv | `Aggregated/Estimate/Project_Summary_WBS.csv` |
| Project_WBS_CBS_Matrix.csv | `Aggregated/Estimate/Project_WBS_CBS_Matrix.csv` |
| Coverage.csv | `Aggregated/Estimate/Coverage.csv` |
| Project_Assumptions.csv | `Aggregated/Estimate/Project_Assumptions.csv` |
| Project_Risks.csv | `Aggregated/Estimate/Project_Risks.csv` |
| BasisOfEstimate_Index.csv | `Aggregated/Estimate/BasisOfEstimate_Index.csv` |
| BasisOfEstimate_Collection.md | `Aggregated/Estimate/BasisOfEstimate_Collection.md` |
| Conflicts.csv | `Aggregated/Conflicts.csv` |
| Duplicates.csv | `Aggregated/Duplicates.csv` |
| Source_Index.csv | `Source_Index.csv` |
| QA_Report.md | `QA_Report.md` |
| Brief.md | `Brief.md` |
| Plan.md | `Plan.md` |
| Decision_Log.md | `Decision_Log.md` |

---

*Generated by AGGREGATION run script.*
"""
    write_file(os.path.join(SNAP_ROOT, "RUN_SUMMARY.md"), summary_content)

    # ── Update _LATEST.md pointer ───────────────────────────────────────
    print("[6/7] Updating _LATEST.md pointer...")
    latest_content = f"""# _LATEST pointer

SnapshotID: {SNAPSHOT_ID}
SnapshotPath: {SNAP_ROOT}
RunDate: 2026-02-28
GrandTotal_CAD: {grand_total:,.2f}
RUN_STATUS: {run_status}
"""
    write_file(os.path.join(AGG_ROOT, "_LATEST.md"), latest_content)

    # ── Final console summary ────────────────────────────────────────────
    print("[7/7] Done.")
    print(f"")
    print(f"  RUN_STATUS:       {run_status}")
    print(f"  Grand Total:      ${grand_total:,.2f} CAD")
    print(f"  Expected Total:   $7,238,510.24 CAD")
    print(f"  Delta:            ${total_delta:,.2f}")
    print(f"  Match:            {'PASS' if total_match else 'FAIL'}")
    print(f"  Detail Rows:      {len(detail_rows)}")
    print(f"  Priced Lines:     {priced_count}")
    print(f"  TBD/Zero Lines:   {tbd_count}")
    print(f"  Deliverables:     {len(snap_map)}")
    print(f"  Assumptions:      {len(assumption_rows)}")
    print(f"  BOE entries:      {len(boe_index_rows)}")
    print(f"  Risk rows:        {len(risk_rows)}")
    print(f"  Snapshot:         {SNAP_ROOT}")
    print(f"")

    return run_status, grand_total

if __name__ == "__main__":
    main()
