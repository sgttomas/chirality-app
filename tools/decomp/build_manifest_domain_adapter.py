#!/usr/bin/env python3
"""Build manifest-backed DOMAIN_DECOMP Batch 0 adapter artifacts.

This tool adapts a domain source manifest of live repo Markdown paths to the
DOMAIN_DECOMP Phase 1 companion layout without copying source files into the
domain pack as source truth.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import subprocess
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path


HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
WORD_RE = re.compile(r"\S+")

GROUP_PREFIX = {
    "ROOT_DOCS": "RT",
    "ROOT_GOVERNANCE_DOCS": "DG",
    "AGENT_CONTRACTS": "AG",
    "SKILL_CONTRACTS": "SK",
    "TOOL_REGISTRY_DOCS": "TL",
    "HARNESS_EXPORT_DOCS": "HX",
}


PREFIX_FIELDS = [
    "SourceDocID",
    "SourcePrefix",
    "SourceName",
    "RepoRelPath",
    "SourceGroup",
    "AuthorityRole",
    "IncludeInIndex",
    "ArchiveState",
    "ExpectedSha256",
    "AtomizeInV1",
    "InOutDefault",
    "CatalogRelPath",
    "SourceRefBase",
    "Disposition",
    "DispositionReason",
    "AssetManifestPath",
    "SkeletonPath",
    "DispatchPlanPath",
    "ReviewHtmlPath",
    "SectionNodesPath",
]

TELEMETRY_FIELDS = [
    "SourceDocID",
    "SourcePrefix",
    "RepoRelPath",
    "SourceGroup",
    "Status",
    "AtomizeInV1",
    "InOutDefault",
    "LineCount",
    "HeadingCount",
    "SectionCount",
    "InScopeSectionCount",
    "DispatchUnitCount",
    "OversizedDispatchUnitCount",
    "BuildMethod",
    "IssueID",
    "Notes",
]

OPEN_ISSUE_FIELDS = [
    "IssueID",
    "Status",
    "Severity",
    "Surface",
    "Issue",
    "RequiredDisposition",
    "Recommendation",
]

VALIDATION_FIELDS = ["CheckID", "Status", "Evidence", "Notes"]

COMPANION_FIELDS = ["Filename", "PackageRole", "Description"]


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--repo-root", type=Path, default=Path("."))
    p.add_argument("--domain-root", type=Path, default=Path("domains/chirality"))
    p.add_argument("--source-manifest", type=Path, default=None)
    p.add_argument("--decomp-root", type=Path, default=None)
    p.add_argument("--budget-tokens", type=int, default=15000)
    p.add_argument("--section-split-threshold", type=int, default=25000)
    return p.parse_args()


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sha1_12(text: str) -> str:
    return hashlib.sha1(text.strip().encode("utf-8")).hexdigest()[:12]


def rel_to_repo(path: Path, repo_root: Path) -> str:
    return path.resolve().relative_to(repo_root.resolve()).as_posix()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, fields: list[str], rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def load_existing_prefixes(path: Path) -> dict[str, str]:
    if not path.exists():
        return {}
    rows = read_csv(path)
    return {
        r["SourceDocID"]: r["SourcePrefix"]
        for r in rows
        if r.get("SourceDocID") and r.get("SourcePrefix")
    }


def assign_prefixes(rows: list[dict[str, str]], existing: dict[str, str]) -> dict[str, str]:
    assigned: dict[str, str] = {}
    used = set(existing.values())
    counters: Counter[str] = Counter()

    for r in rows:
        group = r["SourceGroup"]
        base = GROUP_PREFIX.get(group, "SR")
        if r["SourceDocID"] in existing:
            assigned[r["SourceDocID"]] = existing[r["SourceDocID"]]
            continue
        while True:
            counters[base] += 1
            candidate = f"{base}{counters[base]:03d}"
            if candidate not in used:
                assigned[r["SourceDocID"]] = candidate
                used.add(candidate)
                break
    return assigned


def count_tokens(lines: list[str], line_start: int, line_end: int) -> int:
    words = 0
    for raw in lines[line_start - 1:line_end]:
        words += len(WORD_RE.findall(raw))
    return int(round(words * 1.35))


def headings_in(lines: list[str]) -> list[tuple[int, int, str]]:
    out = []
    for i, raw in enumerate(lines, start=1):
        m = HEADING_RE.match(raw)
        if m:
            out.append((i, len(m.group(1)), m.group(2).strip()))
    return out


def minimal_asset_manifest(row: dict[str, str], prefix: str, manifest_sha: str) -> dict:
    return {
        "schema_version": "chirality-domain-md-adapter/v1",
        "doc_stem": row["SourceDocID"],
        "source_doc_id": row["SourceDocID"],
        "source_name": row["SourceName"],
        "source_prefix": prefix,
        "repo_rel_path": row["RepoRelPath"],
        "catalog_rel_path": f"@repo/{row['RepoRelPath']}",
        "source_manifest_sha256": manifest_sha,
        "assets": [],
        "pages": [],
    }


def in_scope_section_overrides(row: dict[str, str], prefix: str) -> list[str]:
    """Return section IDs that Batch 0 admits despite generic back-matter heuristics."""
    if (
        row.get("SourceDocID") == "SRC-DOCS-THESIS-GLOSSARY"
        or row.get("RepoRelPath") == "docs/thesis/glossary.md"
    ):
        return [f"SEC-{prefix}-0001"]
    return []


def run_tool(cmd: list[str], repo_root: Path) -> tuple[int, str, str]:
    proc = subprocess.run(
        cmd,
        cwd=repo_root,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    return proc.returncode, proc.stdout, proc.stderr


def build_headingless_license_skeleton(
    source_path: Path,
    asset_manifest_path: Path,
    skeleton_path: Path,
    dispatch_plan_path: Path,
    source_doc_id: str,
    prefix: str,
    budget_tokens: int,
    split_threshold: int,
) -> tuple[int, int]:
    lines = source_path.read_text(encoding="utf-8").splitlines()
    total_lines = len(lines)
    section_id = f"SEC-{prefix}-0001"
    tokens = count_tokens(lines, 1, max(total_lines, 1)) if total_lines else 0
    skeleton = {
        "schema_version": 1,
        "source": source_doc_id,
        "source_prefix": prefix,
        "md_path": str(source_path),
        "asset_manifest_path": str(asset_manifest_path),
        "total_md_lines": total_lines,
        "section_count": 1,
        "generated_utc": utc_now(),
        "adapter_method": "headingless_source_synthetic_section",
        "adapter_note": (
            "Source has no Markdown headings. A synthetic review section was "
            "created without copying or modifying the source. Section defaults "
            "OUT and dispatch is deferred pending Gate 1 acceptance."
        ),
        "sections": [
            {
                "section_id": section_id,
                "depth": 1,
                "title": "LICENSE",
                "section_number": None,
                "parent_section_id": None,
                "line_start": 1,
                "line_end": total_lines,
                "page_first": None,
                "page_last": None,
                "estimated_md_tokens": tokens,
                "is_front_matter": False,
                "is_back_matter": False,
                "in_scope_default": False,
                "figure_refs": [],
                "table_refs": [],
                "equation_refs": [],
                "asset_ids": [],
            }
        ],
    }
    dispatch_plan = {
        "schema_version": 1,
        "source": source_doc_id,
        "source_prefix": prefix,
        "skeleton_path": str(skeleton_path),
        "md_path": str(source_path),
        "budget_tokens": budget_tokens,
        "section_split_threshold": split_threshold,
        "unit_count": 0,
        "generated_utc": utc_now(),
        "adapter_method": "headingless_source_deferred",
        "adapter_note": "LICENSE.md is headingless legal/license text; AtomizeInV1=NO unless human overrides Gate 1.",
        "units": [],
    }
    skeleton_path.parent.mkdir(parents=True, exist_ok=True)
    dispatch_plan_path.parent.mkdir(parents=True, exist_ok=True)
    skeleton_path.write_text(json.dumps(skeleton, indent=2) + "\n", encoding="utf-8")
    dispatch_plan_path.write_text(json.dumps(dispatch_plan, indent=2) + "\n", encoding="utf-8")
    return 1, 0


def render_source(
    repo_root: Path,
    source_path: Path,
    asset_manifest_path: Path,
    skeleton_path: Path,
    sidecar_dir: Path,
    html_path: Path,
    section_nodes_path: Path,
    source_doc_id: str,
) -> tuple[int, str, str]:
    sidecar_dir.mkdir(parents=True, exist_ok=True)
    cmd = [
        sys.executable,
        "tools/decomp/render_source_html.py",
        "--md",
        str(source_path),
        "--asset-manifest",
        str(asset_manifest_path),
        "--skeleton",
        str(skeleton_path),
        "--audit-dir",
        str(sidecar_dir),
        "--output-html",
        str(html_path),
        "--output-section-nodes",
        str(section_nodes_path),
        "--mode",
        "structure",
        "--title",
        f"{source_doc_id} - structure review",
    ]
    return run_tool(cmd, repo_root)


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def latest_snapshot(domain_root: Path) -> tuple[str, str, dict]:
    latest_path = domain_root / "_LocalIndexes" / "_LATEST.md"
    latest_text = latest_path.read_text(encoding="utf-8") if latest_path.exists() else ""
    latest = ""
    for line in latest_text.splitlines():
        if line.startswith("Latest:"):
            latest = line.split(":", 1)[1].strip()
            break
    meta = {}
    if latest:
        meta_path = domain_root / "_LocalIndexes" / latest / "meta.json"
        if meta_path.exists():
            meta = load_json(meta_path)
    return latest, latest_text, meta


def build_main_doc(
    decomp_root: Path,
    repo_root: Path,
    domain_root: Path,
    manifest_sha: str,
    latest_snapshot_rel: str,
    catalog_meta: dict,
    summary: dict,
    group_rows: list[dict],
    open_issues: list[dict],
    companion_rows: list[dict],
) -> None:
    rel_decomp = rel_to_repo(decomp_root, repo_root)
    manifest_rel = rel_to_repo(domain_root / "_Sources" / "Source_Manifest.csv", repo_root)
    latest_rel = f"{rel_to_repo(domain_root / '_LocalIndexes', repo_root)}/{latest_snapshot_rel}" if latest_snapshot_rel else "TBD"
    companion_table = "\n".join(
        f"| `{r['Filename']}` | {r['PackageRole']} | {r['Description']} |"
        for r in companion_rows[:80]
    )
    if len(companion_rows) > 80:
        companion_table += (
            f"\n| `Companion_Inventory.csv` | authoritative companion register | "
            f"Full file-level inventory for all {len(companion_rows)} generated companion entries. |"
        )

    group_table = "\n".join(
        "| {SourceGroup} | {SourceCount} | {SkeletonCount} | {DeferredCount} | {SectionCount} | {InScopeSectionCount} | {DispatchUnitCount} | {OversizedDispatchUnitCount} |".format(**r)
        for r in group_rows
    )
    issue_table = "\n".join(
        f"| `{r['IssueID']}` | {r['Status']} | {r['Issue']} | {r['Recommendation']} |"
        for r in open_issues
    )

    doc = f"""# Chirality Domain Decomposition

Package role: working surface

Status: Gate 1 intake packet awaiting human acceptance. Phase 2 atomization has not started.

Generated UTC: {utc_now()}

## Source Model

The Chirality domain pack uses manifest-backed live repository files as source truth. Source files are not copied into `_Sources/`; decomposition companions point back to `@repo/<RepoRelPath>`.

Accepted manifest for this Batch 0 packet: `{manifest_rel}`

Current source manifest SHA-256: `{manifest_sha}`

Current source catalog snapshot: `{latest_rel}`

Catalog schema: `{catalog_meta.get('schema_version', 'TBD')}`

Catalog validation result: `{summary.get('catalog_validation_status', 'TBD')}`

Source files copied: `{str(catalog_meta.get('source_files_copied', 'TBD')).lower()}`

Retrieval index status: `{catalog_meta.get('retrieval_index', {}).get('status', 'TBD')}`

Retrieval smoke query: `{summary.get('retrieval_smoke_status', 'TBD')}`

## Intake Summary

| Metric | Value |
|---|---:|
| Manifest source rows | {summary['source_count']} |
| Catalog artifacts | {catalog_meta.get('artifact_count', 'TBD')} |
| Catalog source docs | {catalog_meta.get('source_doc_count', 'TBD')} |
| Catalog chunks | {catalog_meta.get('chunk_count', 'TBD')} |
| Skeletons generated | {summary['skeleton_count']} |
| Review HTML files generated | {summary['review_html_count']} |
| Section-node CSVs generated | {summary['section_nodes_count']} |
| Total sections | {summary['section_count']} |
| In-scope sections | {summary['in_scope_section_count']} |
| Dispatch units | {summary['dispatch_unit_count']} |
| Oversized dispatch units | {summary['oversized_dispatch_unit_count']} |
| Deferred sources | {summary['deferred_count']} |
| Skeleton failures | {summary['failure_count']} |

## Group Telemetry

| SourceGroup | Sources | Skeletons | Deferred | Sections | In-scope Sections | Dispatch Units | Oversized Units |
|---|---:|---:|---:|---:|---:|---:|---:|
{group_table}

## SourceRef Adapter Policy

The manifest-backed SourceRef form is accepted for Phase 2 atomization:

```text
@repo/<RepoRelPath>:L####|domains/chirality/_Decomposition/source_review_html/<SourceDocID>.html#<SectionID>
```

This preserves live repo provenance and keeps the HTML half pointed at the Batch 0 review surface. `tools/decomp/build_atomization_brief.py` emits `SOURCE_REF_BASE` for the worker, and `skills/domain-source-atomize` explicitly accepts the repo-backed form for manifest-backed sources.

## LICENSE.md Disposition

`SRC-LICENSE` is headingless legal/license text. Batch 0 created a synthetic one-section review skeleton without copying or modifying `LICENSE.md`, marked the section OUT by default, and set `AtomizeInV1=NO`. This is a proposed deferred-source decision for Gate 1 acceptance, not a closed ruling.

## Gate 1.5 Asset Surface Policy

Per-kind asset audit surfaces are N/A for this Markdown-only manifest because the generated minimal asset manifests contain no assets or pages. The section review HTML remains required and has been generated under `{rel_decomp}/source_review_html/`.

## References

- `{manifest_rel}` - manifest-backed source membership.
- `{rel_to_repo(domain_root / '_Sources' / 'SOURCE_BOUNDARY.md', repo_root)}` - source boundary.
- `{rel_to_repo(domain_root / '_LocalIndexes' / '_LATEST.md', repo_root)}` - latest source catalog pointer.
- `{latest_rel}` - current validated source catalog snapshot.

## Companion Inventory

| Filename | PackageRole | Description |
|---|---|---|
{companion_table}

## Open Issues

| IssueID | Status | Issue | Recommendation |
|---|---|---|---|
{issue_table}

## Decision Log / Change Log

| DecisionID | Date | Decision |
|---|---|---|
| DEC-001 | 2026-06-14 | Repaired `SRC-INIT` manifest path from `INIT.md` to `init/INIT.md` after validation found the root path missing. SourceDocID and content hash were preserved. |
| DEC-002 | 2026-06-14 | Generated Batch 0 adapter companions from live repo paths; no source files were copied into `_Sources/`. |
| DEC-003 | 2026-06-14 | Proposed `SRC-LICENSE` as headingless OUT/deferred for v1 atomization pending Gate 1 acceptance. |
| DEC-004 | 2026-06-14 | Accepted repo-backed SourceRefs for manifest-backed atomization: `@repo/<RepoRelPath>:L####|domains/chirality/_Decomposition/source_review_html/<SourceDocID>.html#<SectionID>`. |
| DEC-005 | 2026-06-14 | Forced standalone `SRC-DOCS-THESIS-GLOSSARY` in scope for v1 atomization; the generic late-document glossary back-matter heuristic remains unchanged for other sources. |

## Gate 1 Confirmation Packet

Gate 1 is awaiting human confirmation. To close Gate 1, the human must explicitly confirm:

```text
The manifest-backed source set, source-prefix map, skeleton inventory, and deferred-source decisions are accepted as the intended Chirality DOMAIN_DECOMP intake.
```

Do not proceed to Phase 2 atomization until Gate 1 is accepted.
"""
    (decomp_root / "Chirality_Domain_Decomposition.md").write_text(doc, encoding="utf-8")


def main() -> int:
    args = parse_args()
    repo_root = args.repo_root.resolve()
    domain_root = (repo_root / args.domain_root).resolve() if not args.domain_root.is_absolute() else args.domain_root.resolve()
    source_manifest = args.source_manifest or (domain_root / "_Sources" / "Source_Manifest.csv")
    source_manifest = source_manifest.resolve()
    decomp_root = (args.decomp_root or (domain_root / "_Decomposition")).resolve()

    if not source_manifest.exists():
        print(f"ERROR: source manifest not found: {source_manifest}", file=sys.stderr)
        return 2

    rows = [r for r in read_csv(source_manifest) if r.get("IncludeInIndex") == "YES"]
    manifest_sha = sha256_file(source_manifest)
    prefix_path = decomp_root / "Source_Decomp_Prefix_Map.csv"
    prefixes = assign_prefixes(rows, load_existing_prefixes(prefix_path))

    dirs = {
        "asset": decomp_root / "source_asset_manifests",
        "skeleton": decomp_root / "source_skeletons",
        "dispatch": decomp_root / "source_dispatch_plans",
        "html": decomp_root / "source_review_html",
        "section": decomp_root / "source_section_nodes",
        "sidecar": decomp_root / "source_review_sidecars",
    }
    for d in dirs.values():
        d.mkdir(parents=True, exist_ok=True)

    prefix_rows = []
    telemetry_rows = []
    validation_rows = []
    companion_rows = []
    open_issues: list[dict] = []
    failures = []

    latest_rel, _, catalog_meta = latest_snapshot(domain_root)

    validation_cmd = [
        sys.executable,
        "tools/source_catalog/validate_source_database.py",
        "--snapshot",
        str(domain_root / "_LocalIndexes" / "_LATEST.md"),
        "--domain-root",
        str(domain_root),
        "--repo-root",
        str(repo_root),
    ]
    validation_rc, validation_stdout, validation_stderr = run_tool(validation_cmd, repo_root)
    validation_output = (validation_stdout or validation_stderr).strip()

    retrieval_cmd = [
        sys.executable,
        "tools/retrieval/query_source_index.py",
        "--snapshot",
        str(domain_root / "_LocalIndexes" / "_LATEST.md"),
        "--query",
        "derivative-package rule",
        "--k",
        "10",
    ]
    retrieval_rc, retrieval_stdout, retrieval_stderr = run_tool(retrieval_cmd, repo_root)
    retrieval_output = (retrieval_stdout or retrieval_stderr).strip()
    retrieval_smoke_pass = retrieval_rc == 0 and "@repo/AGENTS.md" in retrieval_output

    validation_rows.append({
        "CheckID": "CATALOG_VALIDATION",
        "Status": "PASS" if validation_rc == 0 else "FAIL",
        "Evidence": validation_output.splitlines()[0] if validation_output else "",
        "Notes": "Required run-start source database validation.",
    })
    validation_rows.append({
        "CheckID": "CATALOG_SNAPSHOT",
        "Status": "PASS" if latest_rel else "FAIL",
        "Evidence": latest_rel,
        "Notes": f"chunks={catalog_meta.get('chunk_count', 'TBD')} retrieval={catalog_meta.get('retrieval_index', {}).get('status', 'TBD')}",
    })
    validation_rows.append({
        "CheckID": "RETRIEVAL_SMOKE_QUERY",
        "Status": "PASS" if retrieval_smoke_pass else "FAIL",
        "Evidence": "derivative-package rule -> @repo/AGENTS.md" if retrieval_smoke_pass else retrieval_output.splitlines()[0] if retrieval_output else "",
        "Notes": "BM25-only query check against accepted governance surface.",
    })
    validation_rows.append({
        "CheckID": "SOURCE_MANIFEST_SHA256",
        "Status": "RECORDED",
        "Evidence": manifest_sha,
        "Notes": "Computed at adapter build time.",
    })

    for index, row in enumerate(rows, start=1):
        source_doc_id = row["SourceDocID"]
        prefix = prefixes[source_doc_id]
        source_path = repo_root / row["RepoRelPath"]
        asset_manifest_path = dirs["asset"] / f"{source_doc_id}_assets_manifest.json"
        skeleton_path = dirs["skeleton"] / f"{source_doc_id}_skeleton.json"
        dispatch_plan_path = dirs["dispatch"] / f"{source_doc_id}_dispatch_plan.json"
        html_path = dirs["html"] / f"{source_doc_id}.html"
        section_nodes_path = dirs["section"] / f"{source_doc_id}_section_nodes.csv"
        sidecar_dir = dirs["sidecar"] / source_doc_id

        asset_manifest = minimal_asset_manifest(row, prefix, manifest_sha)
        asset_manifest_path.write_text(json.dumps(asset_manifest, indent=2) + "\n", encoding="utf-8")

        prefix_base = {
            "SourceDocID": source_doc_id,
            "SourcePrefix": prefix,
            "SourceName": row["SourceName"],
            "RepoRelPath": row["RepoRelPath"],
            "SourceGroup": row["SourceGroup"],
            "AuthorityRole": row["AuthorityRole"],
            "IncludeInIndex": row["IncludeInIndex"],
            "ArchiveState": row["ArchiveState"],
            "ExpectedSha256": row["ExpectedSha256"],
            "CatalogRelPath": f"@repo/{row['RepoRelPath']}",
            "SourceRefBase": f"@repo/{row['RepoRelPath']}:L####|domains/chirality/_Decomposition/source_review_html/{source_doc_id}.html#<SectionID>",
            "AssetManifestPath": rel_to_repo(asset_manifest_path, repo_root),
            "SkeletonPath": rel_to_repo(skeleton_path, repo_root),
            "DispatchPlanPath": rel_to_repo(dispatch_plan_path, repo_root),
            "ReviewHtmlPath": rel_to_repo(html_path, repo_root),
            "SectionNodesPath": rel_to_repo(section_nodes_path, repo_root),
        }

        if not source_path.exists():
            issue_id = f"OI-AUTO-{len(open_issues) + 1:03d}"
            failures.append(source_doc_id)
            telemetry_rows.append({
                "SourceDocID": source_doc_id,
                "SourcePrefix": prefix,
                "RepoRelPath": row["RepoRelPath"],
                "SourceGroup": row["SourceGroup"],
                "Status": "FAILED_MISSING_SOURCE",
                "AtomizeInV1": "NO",
                "InOutDefault": "TBD",
                "IssueID": issue_id,
                "Notes": "Source path missing during adapter build.",
            })
            prefix_rows.append({
                **prefix_base,
                "AtomizeInV1": "NO",
                "InOutDefault": "TBD",
                "Disposition": "FAILED",
                "DispositionReason": "Source path missing during adapter build.",
            })
            open_issues.append({
                "IssueID": issue_id,
                "Status": "OPEN",
                "Severity": "BLOCKER",
                "Surface": source_doc_id,
                "Issue": f"Source path missing: {row['RepoRelPath']}",
                "RequiredDisposition": "Repair manifest or source file before atomization.",
                "Recommendation": "Do not dispatch Phase 2 for this source.",
            })
            continue

        actual_sha = sha256_file(source_path)
        if actual_sha != row["ExpectedSha256"]:
            issue_id = f"OI-AUTO-{len(open_issues) + 1:03d}"
            open_issues.append({
                "IssueID": issue_id,
                "Status": "OPEN",
                "Severity": "BLOCKER",
                "Surface": source_doc_id,
                "Issue": f"Hash mismatch for {row['RepoRelPath']}",
                "RequiredDisposition": "Rebuild source catalog after manifest update.",
                "Recommendation": "Do not dispatch Phase 2 for this source until the hash is accepted.",
            })

        lines = source_path.read_text(encoding="utf-8").splitlines()
        headings = headings_in(lines)
        build_method = "build_source_skeleton.py"
        atomize = "YES"
        inout_default = "IN"
        disposition = "ACTIVE"
        disposition_reason = "Heading-bearing Markdown source processed by existing DOMAIN_DECOMP tools."
        issue_id = ""
        force_in_scope = in_scope_section_overrides(row, prefix)
        if force_in_scope:
            build_method = "build_source_skeleton.py + in_scope_override"
            disposition_reason = (
                "Standalone admitted glossary forced in scope by Batch 0 adapter policy."
            )

        if not headings:
            if source_doc_id == "SRC-LICENSE" or Path(row["RepoRelPath"]).name == "LICENSE.md":
                build_method = "headingless_license_adapter"
                atomize = "NO"
                inout_default = "OUT"
                disposition = "DEFERRED_HEADINGLESS_OUT"
                disposition_reason = "Headingless legal/license text; synthetic review section generated; no Phase 2 dispatch until human acceptance."
                issue_id = "OI-001"
                build_headingless_license_skeleton(
                    source_path=source_path,
                    asset_manifest_path=asset_manifest_path,
                    skeleton_path=skeleton_path,
                    dispatch_plan_path=dispatch_plan_path,
                    source_doc_id=source_doc_id,
                    prefix=prefix,
                    budget_tokens=args.budget_tokens,
                    split_threshold=args.section_split_threshold,
                )
            else:
                issue_id = f"OI-AUTO-{len(open_issues) + 1:03d}"
                failures.append(source_doc_id)
                build_method = "failed_no_headings"
                atomize = "NO"
                inout_default = "TBD"
                disposition = "FAILED_NO_HEADINGS"
                disposition_reason = "No Markdown headings and no adapter rule matched."
                open_issues.append({
                    "IssueID": issue_id,
                    "Status": "OPEN",
                    "Severity": "BLOCKER",
                    "Surface": source_doc_id,
                    "Issue": f"No Markdown headings found in {row['RepoRelPath']}",
                    "RequiredDisposition": "Defer source or define a synthetic-section adapter rule.",
                    "Recommendation": "Do not dispatch Phase 2 for this source.",
                })
        else:
            cmd = [
                sys.executable,
                "tools/decomp/build_source_skeleton.py",
                "--md",
                str(source_path),
                "--asset-manifest",
                str(asset_manifest_path),
                "--output-skeleton",
                str(skeleton_path),
                "--output-dispatch-plan",
                str(dispatch_plan_path),
                "--source-prefix",
                prefix,
                "--budget-tokens",
                str(args.budget_tokens),
                "--section-split-threshold",
                str(args.section_split_threshold),
            ]
            if force_in_scope:
                cmd.extend(["--in-scope-overrides", json.dumps(force_in_scope)])
            rc, stdout, stderr = run_tool(cmd, repo_root)
            if rc != 0:
                issue_id = f"OI-AUTO-{len(open_issues) + 1:03d}"
                failures.append(source_doc_id)
                atomize = "NO"
                inout_default = "TBD"
                disposition = "FAILED_SKELETON_BUILD"
                disposition_reason = f"build_source_skeleton.py failed: {stderr.strip() or stdout.strip()}"
                open_issues.append({
                    "IssueID": issue_id,
                    "Status": "OPEN",
                    "Severity": "BLOCKER",
                    "Surface": source_doc_id,
                    "Issue": f"Skeleton build failed for {row['RepoRelPath']}",
                    "RequiredDisposition": "Repair input/tool issue before atomization.",
                    "Recommendation": disposition_reason[:240],
                })

        render_status = "NOT_RENDERED"
        render_note = ""
        if skeleton_path.exists():
            rc, stdout, stderr = render_source(
                repo_root=repo_root,
                source_path=source_path,
                asset_manifest_path=asset_manifest_path,
                skeleton_path=skeleton_path,
                sidecar_dir=sidecar_dir,
                html_path=html_path,
                section_nodes_path=section_nodes_path,
                source_doc_id=source_doc_id,
            )
            if rc == 0:
                render_status = "RENDERED"
            else:
                render_status = "RENDER_FAILED"
                render_note = stderr.strip() or stdout.strip()
                issue_id = issue_id or f"OI-AUTO-{len(open_issues) + 1:03d}"
                open_issues.append({
                    "IssueID": issue_id,
                    "Status": "OPEN",
                    "Severity": "BLOCKER",
                    "Surface": source_doc_id,
                    "Issue": f"Review HTML render failed for {row['RepoRelPath']}",
                    "RequiredDisposition": "Repair render issue before Gate 1.5 review.",
                    "Recommendation": render_note[:240],
                })

        section_count = 0
        in_scope_count = 0
        unit_count = 0
        oversized_count = 0
        if skeleton_path.exists():
            skeleton = load_json(skeleton_path)
            section_count = len(skeleton.get("sections", []))
            in_scope_count = sum(1 for s in skeleton.get("sections", []) if s.get("in_scope_default"))
        if dispatch_plan_path.exists():
            dispatch = load_json(dispatch_plan_path)
            unit_count = len(dispatch.get("units", []))
            oversized_count = sum(1 for u in dispatch.get("units", []) if u.get("contains_oversized_section"))

        status = "READY" if disposition == "ACTIVE" and render_status == "RENDERED" else disposition
        if render_status == "RENDER_FAILED":
            status = "FAILED_RENDER"

        telemetry_rows.append({
            "SourceDocID": source_doc_id,
            "SourcePrefix": prefix,
            "RepoRelPath": row["RepoRelPath"],
            "SourceGroup": row["SourceGroup"],
            "Status": status,
            "AtomizeInV1": atomize,
            "InOutDefault": inout_default,
            "LineCount": len(lines),
            "HeadingCount": len(headings),
            "SectionCount": section_count,
            "InScopeSectionCount": in_scope_count,
            "DispatchUnitCount": unit_count,
            "OversizedDispatchUnitCount": oversized_count,
            "BuildMethod": build_method,
            "IssueID": issue_id,
            "Notes": render_note or disposition_reason,
        })
        prefix_rows.append({
            **prefix_base,
            "AtomizeInV1": atomize,
            "InOutDefault": inout_default,
            "Disposition": disposition,
            "DispositionReason": disposition_reason,
        })

        if index % 25 == 0:
            print(f"processed {index}/{len(rows)} sources", file=sys.stderr)

    open_issues.extend([
        {
            "IssueID": "OI-001",
            "Status": "AWAITING_GATE_1_ACCEPTANCE",
            "Severity": "MAJOR",
            "Surface": "SRC-LICENSE",
            "Issue": "LICENSE.md is headingless and legal/license text.",
            "RequiredDisposition": "Human accepts OUT/deferred disposition or requests a different adapter before Phase 2.",
            "Recommendation": "Keep AtomizeInV1=NO and InOutDefault=OUT for v1 unless human says license terms are in-domain.",
        },
        {
            "IssueID": "OI-002",
            "Status": "ACCEPTED_FOR_PHASE_2",
            "Severity": "INFO",
            "Surface": "Phase 2 SourceRef policy",
            "Issue": "DOMAIN_DECOMP source atomization docs specify older <book>.md:L#### SourceRefs.",
            "RequiredDisposition": "Closed by accepted repo-backed SourceRef adapter policy.",
            "Recommendation": "@repo/<RepoRelPath>:L####|domains/chirality/_Decomposition/source_review_html/<SourceDocID>.html#<SectionID>",
        },
        {
            "IssueID": "OI-004",
            "Status": "AWAITING_GATE_1_ACCEPTANCE",
            "Severity": "MINOR",
            "Surface": "Gate 1.5 asset surfaces",
            "Issue": "Per-kind asset surfaces are N/A for Markdown-only manifest rows.",
            "RequiredDisposition": "Human accepts N/A policy for equations/figures/tables/images/folios in Batch 0.",
            "Recommendation": "Use section review HTML only unless future sources carry actual asset manifests.",
        },
        {
            "IssueID": "OI-005",
            "Status": "OPEN_FOR_PHASE_2_PLANNING",
            "Severity": "MAJOR",
            "Surface": "Phase 2 staging",
            "Issue": "Full 242-file atomization is too large for one unbatched review gate.",
            "RequiredDisposition": "Run staged authority batches after Gate 1.",
            "Recommendation": "Start with Batch 1 binding governance seed after Gate 1 and SourceRef acceptance.",
        },
    ])

    # Deduplicate open issues by IssueID, preferring the later explicit row.
    issue_by_id = {}
    for item in open_issues:
        issue_by_id[item["IssueID"]] = item
    open_issues = [issue_by_id[k] for k in sorted(issue_by_id)]

    write_csv(prefix_path, PREFIX_FIELDS, prefix_rows)
    write_csv(decomp_root / "Intake_Telemetry.csv", TELEMETRY_FIELDS, telemetry_rows)
    write_csv(decomp_root / "Open_Issues_Register.csv", OPEN_ISSUE_FIELDS, open_issues)

    group_summary = []
    for group in sorted({r["SourceGroup"] for r in rows}):
        group_items = [r for r in telemetry_rows if r["SourceGroup"] == group]
        group_summary.append({
            "SourceGroup": group,
            "SourceCount": len(group_items),
            "SkeletonCount": sum(1 for r in group_items if int(r.get("SectionCount") or 0) > 0),
            "DeferredCount": sum(1 for r in group_items if r.get("AtomizeInV1") == "NO"),
            "SectionCount": sum(int(r.get("SectionCount") or 0) for r in group_items),
            "InScopeSectionCount": sum(int(r.get("InScopeSectionCount") or 0) for r in group_items),
            "DispatchUnitCount": sum(int(r.get("DispatchUnitCount") or 0) for r in group_items),
            "OversizedDispatchUnitCount": sum(int(r.get("OversizedDispatchUnitCount") or 0) for r in group_items),
        })

    summary = {
        "generated_utc": utc_now(),
        "source_count": len(rows),
        "source_manifest": rel_to_repo(source_manifest, repo_root),
        "source_manifest_sha256": manifest_sha,
        "catalog_snapshot": latest_rel,
        "catalog_meta": catalog_meta,
        "catalog_validation_status": "PASS" if validation_rc == 0 else "FAIL",
        "catalog_validation_evidence": validation_output,
        "retrieval_smoke_status": "PASS" if retrieval_smoke_pass else "FAIL",
        "retrieval_smoke_evidence": "derivative-package rule -> @repo/AGENTS.md" if retrieval_smoke_pass else retrieval_output,
        "skeleton_count": sum(1 for r in telemetry_rows if int(r.get("SectionCount") or 0) > 0),
        "review_html_count": sum(1 for r in telemetry_rows if (dirs["html"] / f"{r['SourceDocID']}.html").exists()),
        "section_nodes_count": sum(1 for r in telemetry_rows if (dirs["section"] / f"{r['SourceDocID']}_section_nodes.csv").exists()),
        "section_count": sum(int(r.get("SectionCount") or 0) for r in telemetry_rows),
        "in_scope_section_count": sum(int(r.get("InScopeSectionCount") or 0) for r in telemetry_rows),
        "dispatch_unit_count": sum(int(r.get("DispatchUnitCount") or 0) for r in telemetry_rows),
        "oversized_dispatch_unit_count": sum(int(r.get("OversizedDispatchUnitCount") or 0) for r in telemetry_rows),
        "deferred_count": sum(1 for r in telemetry_rows if r.get("AtomizeInV1") == "NO"),
        "failure_count": len(failures),
        "groups": group_summary,
    }
    (decomp_root / "Intake_Telemetry.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")

    zero_dispatch_atomize = [
        r["SourceDocID"]
        for r in telemetry_rows
        if r.get("AtomizeInV1") == "YES" and int(r.get("DispatchUnitCount") or 0) == 0
    ]
    validation_rows.extend([
        {
            "CheckID": "SOURCE_PREFIX_UNIQUENESS",
            "Status": "PASS" if len(set(prefixes.values())) == len(prefixes) else "FAIL",
            "Evidence": f"{len(set(prefixes.values()))}/{len(prefixes)} unique prefixes",
            "Notes": "Prefixes are explicit in Source_Decomp_Prefix_Map.csv.",
        },
        {
            "CheckID": "SKELETON_INVENTORY",
            "Status": "PASS" if summary["failure_count"] == 0 and summary["skeleton_count"] == len(rows) else "FAIL",
            "Evidence": f"skeletons={summary['skeleton_count']} sources={len(rows)} failures={summary['failure_count']}",
            "Notes": "SRC-LICENSE uses a synthetic OUT/deferred skeleton.",
        },
        {
            "CheckID": "REVIEW_HTML_INVENTORY",
            "Status": "PASS" if summary["review_html_count"] == summary["skeleton_count"] else "FAIL",
            "Evidence": f"html={summary['review_html_count']} skeletons={summary['skeleton_count']}",
            "Notes": "Structure-mode section review surfaces only.",
        },
        {
            "CheckID": "DISPATCH_ELIGIBILITY",
            "Status": "PASS" if not zero_dispatch_atomize else "FAIL",
            "Evidence": "no AtomizeInV1=YES source has zero dispatch units"
            if not zero_dispatch_atomize
            else ";".join(zero_dispatch_atomize),
            "Notes": "Only explicitly deferred sources may have zero dispatch units.",
        },
        {
            "CheckID": "PHASE_2_ATOMIZATION",
            "Status": "NOT_RUN",
            "Evidence": "Gate 1 pending",
            "Notes": "No TASK + domain-source-atomize dispatch was started.",
        },
    ])
    write_csv(decomp_root / "Validation_Checks.csv", VALIDATION_FIELDS, validation_rows)

    # File-level companion inventory.
    static_files = [
        ("Chirality_Domain_Decomposition.md", "working surface", "Main Batch 0 control surface and Gate 1 packet."),
        ("Source_Decomp_Prefix_Map.csv", "authoritative companion register", "Stable source-prefix map and SourceRef adapter metadata."),
        ("Intake_Telemetry.csv", "authoritative companion register", "Per-source intake, skeleton, render, and dispatch telemetry."),
        ("Intake_Telemetry.json", "authoritative companion register", "Batch 0 summary telemetry."),
        ("Open_Issues_Register.csv", "authoritative companion register", "Gate 1 open issues and required human rulings."),
        ("Validation_Checks.csv", "authoritative companion register", "Batch 0 validation checks."),
        ("Companion_Inventory.csv", "authoritative companion register", "File-level inventory of generated companion artifacts."),
    ]
    for filename, role, desc in static_files:
        companion_rows.append({"Filename": filename, "PackageRole": role, "Description": desc})
    for r in prefix_rows:
        companion_rows.extend([
            {"Filename": r["AssetManifestPath"], "PackageRole": "authoritative companion register", "Description": f"Minimal Markdown-only asset manifest for {r['SourceDocID']}."},
            {"Filename": r["SkeletonPath"], "PackageRole": "authoritative companion register", "Description": f"Source skeleton for {r['SourceDocID']}."},
            {"Filename": r["DispatchPlanPath"], "PackageRole": "authoritative companion register", "Description": f"Phase 2 dispatch plan for {r['SourceDocID']}."},
            {"Filename": r["ReviewHtmlPath"], "PackageRole": "authoritative companion register", "Description": f"Structure-mode section review HTML for {r['SourceDocID']}."},
            {"Filename": r["SectionNodesPath"], "PackageRole": "authoritative companion register", "Description": f"Section-node retrieval substrate for {r['SourceDocID']}."},
        ])
    write_csv(decomp_root / "Companion_Inventory.csv", COMPANION_FIELDS, companion_rows)

    build_main_doc(
        decomp_root=decomp_root,
        repo_root=repo_root,
        domain_root=domain_root,
        manifest_sha=manifest_sha,
        latest_snapshot_rel=latest_rel,
        catalog_meta=catalog_meta,
        summary=summary,
        group_rows=group_summary,
        open_issues=open_issues,
        companion_rows=companion_rows,
    )

    print(json.dumps({
        "status": "PASS" if summary["failure_count"] == 0 else "FAIL",
        "sources": summary["source_count"],
        "skeletons": summary["skeleton_count"],
        "review_html": summary["review_html_count"],
        "sections": summary["section_count"],
        "dispatch_units": summary["dispatch_unit_count"],
        "deferred": summary["deferred_count"],
        "failures": summary["failure_count"],
        "manifest_sha256": manifest_sha,
        "catalog_snapshot": latest_rel,
    }, indent=2))
    return 0 if summary["failure_count"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
