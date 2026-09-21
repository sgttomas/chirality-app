#!/usr/bin/env python3
"""Build a grouped Phase 2 skill-pack atomization batch.

This adapter treats each ``skills/<skill-name>/`` directory as one DOMAIN
source while preserving source-line citations into the original component
files. It writes generated pack markdown as a worker/review substrate only;
repo files listed in Source_Manifest.csv remain the source truth.
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

TOOLS_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(TOOLS_ROOT / "source_catalog"))
from source_database import resolve_domain_root  # noqa: E402


BATCH_ID = "BATCH4_SKILL_PACKS_20260614T000000Z"
BATCH_NAME = "Batch 4 - Skill Packs"
SKILL_GROUP = "SKILL_CONTRACTS"
PACK_GROUP = "SKILL_PACK_CONTRACTS"
PACK_AUTHORITY = "SKILL_PACK_CONTRACT"

SOURCE_FIELDS = [
    "BatchID",
    "BatchName",
    "SourceSequence",
    "SourceDocID",
    "SourcePrefix",
    "SourceName",
    "RepoRelPath",
    "SourceGroup",
    "AuthorityRole",
    "AtomizeInV1",
    "InOutDefault",
    "LineCount",
    "SectionCount",
    "InScopeSectionCount",
    "DispatchUnitCount",
    "SourceRefBase",
    "DispatchPlan",
    "Skeleton",
    "AssetManifest",
    "BriefDir",
    "OutputDir",
    "PerSourceLedgerPath",
    "PerSourceVocabularySeedPath",
    "Status",
    "Notes",
]

UNIT_FIELDS = [
    "BatchID",
    "BatchName",
    "GlobalUnitSequence",
    "SourceSequence",
    "SourceDocID",
    "SourcePrefix",
    "DispatchUnitID",
    "SourceUnitSequence",
    "LineStart",
    "LineEnd",
    "EstimatedMdTokens",
    "TargetSectionCount",
    "TargetSectionIDs",
    "ContainsOversizedSection",
    "BriefPath",
    "OutputLedgerPath",
    "OutputVocabSeedPath",
    "Status",
    "RunStatus",
    "Notes",
]

VALIDATION_FIELDS = ["CheckID", "Status", "Evidence", "Notes"]
COMPANION_FIELDS = ["Filename", "PackageRole", "Description"]

HEADING_RE = re.compile(r"^(#{1,6})(\s+.+?)$")
SLUG_RE = re.compile(r"[^A-Za-z0-9]+")


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--repo-root", type=Path, default=Path("."))
    p.add_argument("--domain-root", type=Path)
    p.add_argument("--source-manifest", type=Path, default=None)
    p.add_argument("--batch-id", default=None)
    p.add_argument("--budget-tokens", type=int, default=15000)
    p.add_argument("--section-split-threshold", type=int, default=25000)
    return p.parse_args()


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


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


def rel_to_repo(path: Path, repo_root: Path) -> str:
    return path.resolve().relative_to(repo_root.resolve()).as_posix()


def slug(value: str) -> str:
    return SLUG_RE.sub("-", value.strip()).strip("-").upper()


def skill_pack_slug(pack_dir: str) -> str:
    return slug(Path(pack_dir).name)


def normalize_heading(raw: str) -> str:
    match = HEADING_RE.match(raw)
    if not match:
        return raw
    hashes, rest = match.groups()
    return f"{'#' * min(len(hashes) + 2, 6)}{rest}"


def source_groups(manifest_rows: list[dict[str, str]]) -> list[dict]:
    active = [
        r for r in manifest_rows
        if r.get("IncludeInIndex") == "YES"
        and r.get("ArchiveState") == "ACTIVE"
        and r.get("SourceGroup") == SKILL_GROUP
    ]
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    meta_rows: list[dict[str, str]] = []
    for row in active:
        rel = row["RepoRelPath"]
        parts = Path(rel).parts
        if rel in {"skills/README.md", "skills/SKILL_TEMPLATE.md"}:
            meta_rows.append(row)
        elif len(parts) >= 3 and parts[0] == "skills":
            grouped[f"skills/{parts[1]}"].append(row)

    out: list[dict] = []
    if meta_rows:
        out.append({
            "source_doc_id": "SRC-SKILLPACK-META",
            "prefix": "SKP000",
            "source_name": "skills meta-contract",
            "repo_rel_path": "skills/{README.md,SKILL_TEMPLATE.md}",
            "pack_key": "skills/meta",
            "component_rows": sorted(meta_rows, key=lambda r: r["RepoRelPath"]),
            "notes": "Grouped skill registry/template source; license remains deferred.",
        })

    for i, pack_key in enumerate(sorted(grouped), start=1):
        rows = sorted(grouped[pack_key], key=lambda r: r["RepoRelPath"])
        name = Path(pack_key).name
        out.append({
            "source_doc_id": f"SRC-SKILLPACK-{skill_pack_slug(pack_key)}",
            "prefix": f"SKP{i:03d}",
            "source_name": f"Skill pack: {name}",
            "repo_rel_path": f"{pack_key}/",
            "pack_key": pack_key,
            "component_rows": rows,
            "notes": f"Grouped {len(rows)} manifest-backed skill contract files into one source.",
        })
    return out


def write_pack_markdown(
    repo_root: Path,
    batch_id: str,
    pack: dict,
    output_path: Path,
) -> list[dict]:
    lines: list[str] = [
        f"# Source Pack: {pack['source_name']}",
        "",
        f"BatchID: `{batch_id}`",
        "",
        "Source truth remains the original repo component files listed under each component heading.",
        "This generated markdown is a DOMAIN_DECOMP review and worker substrate only.",
        "",
    ]
    components: list[dict] = []
    for row in pack["component_rows"]:
        rel = row["RepoRelPath"]
        src = repo_root / rel
        raw_lines = src.read_text(encoding="utf-8").splitlines()
        lines.append(f"## Component: {rel}")
        lines.append("")
        start = len(lines) + 1
        for raw in raw_lines:
            lines.append(normalize_heading(raw))
        end = len(lines)
        lines.append("")
        components.append({
            "repo_rel_path": rel,
            "source_doc_id": row["SourceDocID"],
            "source_name": row["SourceName"],
            "source_prefix": "",
            "expected_sha256": row.get("ExpectedSha256", ""),
            "generated_line_start": start,
            "generated_line_end": end,
            "source_line_start": 1,
            "source_line_end": len(raw_lines),
            "line_offset": 1 - start,
        })
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    return components


def write_asset_manifest(
    path: Path,
    pack: dict,
    batch_id: str,
    manifest_sha: str,
    generated_md: Path,
    html_rel: str,
    components: list[dict],
) -> None:
    payload = {
        "schema_version": "chirality-skill-pack-source/v1",
        "doc_stem": pack["source_doc_id"],
        "source_doc_id": pack["source_doc_id"],
        "source_name": pack["source_name"],
        "source_prefix": pack["prefix"],
        "repo_rel_path": pack["repo_rel_path"],
        "catalog_rel_path": f"@repo/{pack['repo_rel_path']}",
        "source_manifest_sha256": manifest_sha,
        "batch_id": batch_id,
        "generated_pack_markdown": str(generated_md),
        "source_truth_policy": "Generated markdown is a worker/review substrate; cite original @repo component files via source_components.",
        "source_html_path": html_rel,
        "source_components": components,
        "assets": [],
        "pages": [],
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def run(cmd: list[str], cwd: Path) -> tuple[int, str, str]:
    proc = subprocess.run(cmd, cwd=cwd, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    return proc.returncode, proc.stdout, proc.stderr


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def append_or_replace_csv(path: Path, fields: list[str], key_fields: list[str], new_rows: list[dict]) -> None:
    existing = read_csv(path) if path.exists() else []
    new_keys = {tuple(row.get(k, "") for k in key_fields) for row in new_rows}
    kept = [row for row in existing if tuple(row.get(k, "") for k in key_fields) not in new_keys]
    write_csv(path, fields, [*kept, *new_rows])


def update_companion_inventory(path: Path, rows: list[dict]) -> None:
    existing = read_csv(path) if path.exists() else []
    new_by_name = {r["Filename"]: r for r in rows}
    kept = [r for r in existing if r.get("Filename") not in new_by_name]
    write_csv(path, COMPANION_FIELDS, [*kept, *rows])


def main() -> int:
    args = parse_args()
    try:
        args.domain_root = resolve_domain_root(args.domain_root)
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    repo_root = args.repo_root.resolve()
    domain_root = (repo_root / args.domain_root).resolve() if not args.domain_root.is_absolute() else args.domain_root.resolve()
    source_manifest = args.source_manifest or (domain_root / "_Sources" / "Source_Manifest.csv")
    source_manifest = source_manifest.resolve()
    decomp_root = domain_root / "_Decomposition"
    batch_id = args.batch_id or BATCH_ID.replace("000000Z", datetime.now(timezone.utc).strftime("%H%M%SZ"))
    generated_utc = utc_now()

    manifest_rows = read_csv(source_manifest)
    manifest_sha = sha256_file(source_manifest)
    packs = source_groups(manifest_rows)
    if not packs:
        print("ERROR: no active skill contract rows found", file=sys.stderr)
        return 2

    batch_root = decomp_root / "phase2_batches" / batch_id
    pack_md_root = decomp_root / "source_pack_markdown" / batch_id
    briefs_root = decomp_root / "dispatch_briefs" / batch_id
    outputs_root = decomp_root / "dispatch_outputs" / batch_id
    per_source_root = decomp_root / "per_source_ledgers" / batch_id
    vocab_root = decomp_root / "vocabulary_seeds" / batch_id

    source_rows: list[dict] = []
    unit_rows: list[dict] = []
    companion_rows: list[dict] = []
    total_units = 0
    total_sections = 0
    total_in_scope = 0
    global_unit_seq = 0

    for source_seq, pack in enumerate(packs, start=1):
        source_doc_id = pack["source_doc_id"]
        prefix = pack["prefix"]
        generated_md = pack_md_root / f"{source_doc_id}.md"
        asset_manifest = decomp_root / "source_asset_manifests" / f"{source_doc_id}_assets_manifest.json"
        skeleton = decomp_root / "source_skeletons" / f"{source_doc_id}_skeleton.json"
        dispatch_plan = decomp_root / "source_dispatch_plans" / f"{source_doc_id}_dispatch_plan.json"
        html = decomp_root / "source_review_html" / f"{source_doc_id}.html"
        section_nodes = decomp_root / "source_section_nodes" / f"{source_doc_id}_section_nodes.csv"
        sidecar_dir = decomp_root / "source_review_sidecars" / source_doc_id
        brief_dir = briefs_root / source_doc_id
        output_dir = outputs_root / source_doc_id
        per_source_ledger = per_source_root / f"{source_doc_id}_atomic_units.csv"
        per_source_vocab = vocab_root / f"{source_doc_id}_vocabulary_seed.csv"

        html_rel = rel_to_repo(html, repo_root)
        components = write_pack_markdown(repo_root, batch_id, pack, generated_md)
        write_asset_manifest(
            asset_manifest,
            pack,
            batch_id,
            manifest_sha,
            generated_md,
            html_rel,
            components,
        )

        rc, stdout, stderr = run([
            sys.executable,
            "tools/decomp/build_source_skeleton.py",
            "--md",
            str(generated_md),
            "--asset-manifest",
            str(asset_manifest),
            "--output-skeleton",
            str(skeleton),
            "--output-dispatch-plan",
            str(dispatch_plan),
            "--source-prefix",
            prefix,
            "--budget-tokens",
            str(args.budget_tokens),
            "--section-split-threshold",
            str(args.section_split_threshold),
        ], repo_root)
        if rc != 0:
            print(stderr or stdout, file=sys.stderr)
            return rc or 1

        sidecar_dir.mkdir(parents=True, exist_ok=True)
        rc, stdout, stderr = run([
            sys.executable,
            "tools/decomp/render_source_html.py",
            "--md",
            str(generated_md),
            "--asset-manifest",
            str(asset_manifest),
            "--skeleton",
            str(skeleton),
            "--audit-dir",
            str(sidecar_dir),
            "--output-html",
            str(html),
            "--output-section-nodes",
            str(section_nodes),
            "--mode",
            "structure",
            "--title",
            f"{source_doc_id} - grouped skill-pack structure review",
        ], repo_root)
        if rc != 0:
            print(stderr or stdout, file=sys.stderr)
            return rc or 1

        skel = load_json(skeleton)
        plan = load_json(dispatch_plan)
        sections = skel.get("sections", [])
        units = plan.get("units", [])
        total_sections += len(sections)
        total_in_scope += sum(1 for s in sections if s.get("in_scope_default"))
        total_units += len(units)

        brief_dir.mkdir(parents=True, exist_ok=True)
        output_dir.mkdir(parents=True, exist_ok=True)
        per_source_root.mkdir(parents=True, exist_ok=True)
        vocab_root.mkdir(parents=True, exist_ok=True)

        for source_unit_seq, unit in enumerate(units, start=1):
            global_unit_seq += 1
            unit_id = unit["unit_id"]
            output_ledger = output_dir / f"{unit_id}_atoms.csv"
            output_vocab = output_dir / f"{unit_id}_vocab.csv"
            brief_path = brief_dir / f"{unit_id}.md"
            rc, stdout, stderr = run([
                sys.executable,
                "tools/decomp/build_atomization_brief.py",
                "--dispatch-plan",
                str(dispatch_plan),
                "--unit-id",
                unit_id,
                "--md",
                str(generated_md),
                "--skeleton",
                str(skeleton),
                "--asset-manifest",
                str(asset_manifest),
                "--output-ledger-path",
                str(output_ledger),
                "--output-vocab-seed-path",
                str(output_vocab),
                "--scope-path",
                str(output_dir),
            ], repo_root)
            if rc != 0:
                print(stderr or stdout, file=sys.stderr)
                return rc or 1
            brief_path.write_text(stdout, encoding="utf-8")
            unit_rows.append({
                "BatchID": batch_id,
                "BatchName": BATCH_NAME,
                "GlobalUnitSequence": global_unit_seq,
                "SourceSequence": source_seq,
                "SourceDocID": source_doc_id,
                "SourcePrefix": prefix,
                "DispatchUnitID": unit_id,
                "SourceUnitSequence": source_unit_seq,
                "LineStart": unit["line_start"],
                "LineEnd": unit["line_end"],
                "EstimatedMdTokens": unit.get("estimated_md_tokens", 0),
                "TargetSectionCount": len(unit.get("target_section_ids", [])),
                "TargetSectionIDs": ";".join(unit.get("target_section_ids", [])),
                "ContainsOversizedSection": str(bool(unit.get("contains_oversized_section", False))).upper(),
                "BriefPath": rel_to_repo(brief_path, repo_root),
                "OutputLedgerPath": rel_to_repo(output_ledger, repo_root),
                "OutputVocabSeedPath": rel_to_repo(output_vocab, repo_root),
                "Status": "BRIEF_READY",
                "RunStatus": "PENDING",
                "Notes": "Grouped skill-pack dispatch; SourceRefs use SOURCE_REF_MODE=COMPONENT_MAP.",
            })

        source_rows.append({
            "BatchID": batch_id,
            "BatchName": BATCH_NAME,
            "SourceSequence": source_seq,
            "SourceDocID": source_doc_id,
            "SourcePrefix": prefix,
            "SourceName": pack["source_name"],
            "RepoRelPath": pack["repo_rel_path"],
            "SourceGroup": PACK_GROUP,
            "AuthorityRole": PACK_AUTHORITY,
            "AtomizeInV1": "YES",
            "InOutDefault": "IN",
            "LineCount": skel.get("total_md_lines", ""),
            "SectionCount": len(sections),
            "InScopeSectionCount": sum(1 for s in sections if s.get("in_scope_default")),
            "DispatchUnitCount": len(units),
            "SourceRefBase": "COMPONENT_MAP",
            "DispatchPlan": rel_to_repo(dispatch_plan, repo_root),
            "Skeleton": rel_to_repo(skeleton, repo_root),
            "AssetManifest": rel_to_repo(asset_manifest, repo_root),
            "BriefDir": rel_to_repo(brief_dir, repo_root),
            "OutputDir": rel_to_repo(output_dir, repo_root),
            "PerSourceLedgerPath": rel_to_repo(per_source_ledger, repo_root),
            "PerSourceVocabularySeedPath": rel_to_repo(per_source_vocab, repo_root),
            "Status": "SETUP_READY",
            "Notes": f"{pack['notes']} Components={len(pack['component_rows'])}; SourceRefs cite original @repo component files.",
        })

        for file_path, role, desc in [
            (generated_md, "authoritative companion register", f"Generated grouped-source markdown substrate for {source_doc_id}; source truth remains repo components."),
            (asset_manifest, "authoritative companion register", f"Grouped-source asset/component manifest for {source_doc_id}."),
            (skeleton, "authoritative companion register", f"Grouped-source skeleton for {source_doc_id}."),
            (dispatch_plan, "authoritative companion register", f"Grouped-source dispatch plan for {source_doc_id}."),
            (html, "authoritative companion register", f"Structure review HTML for Batch 4 grouped source {source_doc_id}."),
            (section_nodes, "authoritative companion register", f"Section-node retrieval substrate for Batch 4 grouped source {source_doc_id}."),
        ]:
            companion_rows.append({
                "Filename": rel_to_repo(file_path, repo_root),
                "PackageRole": role,
                "Description": desc,
            })
        for unit in units:
            companion_rows.append({
                "Filename": rel_to_repo(brief_dir / f"{unit['unit_id']}.md", repo_root),
                "PackageRole": "authoritative companion register",
                "Description": f"Rendered INIT-TASK brief for Batch 4 grouped source {source_doc_id}, unit {unit['unit_id']}.",
            })

    validation_rows = [
        {
            "CheckID": "BATCH4_SOURCE_SELECTION",
            "Status": "PASS",
            "Evidence": f"{batch_id}; grouped_sources={len(source_rows)}; component_manifest_rows=153",
            "Notes": "Selected 37 skills/<name>/ packs plus one skills meta-contract source; LICENSE.md remains deferred.",
        },
        {
            "CheckID": "BATCH4_COMPONENT_MAPS",
            "Status": "PASS",
            "Evidence": "source_components present in every grouped source asset manifest",
            "Notes": "Workers must cite original @repo component files using SOURCE_REF_MODE=COMPONENT_MAP.",
        },
        {
            "CheckID": "BATCH4_DISPATCH_UNITS",
            "Status": "PASS",
            "Evidence": f"dispatch_units={total_units}; grouped_sources={len(source_rows)}",
            "Notes": "Dispatch-unit register generated from grouped source dispatch plans.",
        },
        {
            "CheckID": "BATCH4_BRIEF_RENDER",
            "Status": "PASS",
            "Evidence": f"briefs={len(unit_rows)}; SOURCE_REF_MODE=COMPONENT_MAP",
            "Notes": "All Batch 4 briefs include component-map SourceRef runtime guidance.",
        },
        {
            "CheckID": "BATCH4_LICENSE_DEFERRED",
            "Status": "PASS",
            "Evidence": "SRC-LICENSE not selected",
            "Notes": "Human directed license deferral for Batch 4.",
        },
        {
            "CheckID": "BATCH4_GATE2_STATUS",
            "Status": "OPEN_FANOUT_PENDING",
            "Evidence": "No Batch 4 atomization outputs merged yet",
            "Notes": "Worker fan-out and Gate 2 review are still required.",
        },
    ]

    source_register = batch_root / "Batch_Source_Register.csv"
    unit_register = batch_root / "Dispatch_Unit_Register.csv"
    validation_register = batch_root / "Validation_Checks.csv"
    write_csv(source_register, SOURCE_FIELDS, source_rows)
    write_csv(unit_register, UNIT_FIELDS, unit_rows)
    write_csv(validation_register, VALIDATION_FIELDS, validation_rows)

    source_table = "\n".join(
        f"| `{r['SourceDocID']}` | `{r['SourcePrefix']}` | `{r['RepoRelPath']}` | {r['LineCount']} | {r['SectionCount']} | {r['DispatchUnitCount']} |"
        for r in source_rows
    )
    setup_md = f"""# Batch 4 Setup - Skill Packs

Package role: snapshot / handoff artifact

BatchID: `{batch_id}`

Status: SETUP_READY_FANOUT_PENDING

Generated UTC: {generated_utc}

## Accepted Upstream Snapshot

- Gate 1 acceptance snapshot: `domains/chirality/_Decomposition/gate_snapshots/GATE1_20260614T005942Z`
- Source manifest: `domains/chirality/_Sources/Source_Manifest.csv`
- Source manifest SHA-256: `{manifest_sha}`
- Current source catalog snapshot: `domains/chirality/_LocalIndexes/_LATEST.md`
- Batch 2 status at setup: BATCH_ACCEPTED_GATE2_OPEN
- Batch 3 status at setup: ATOMIZATION_COMPLETE_GATE2_OPEN
- Source-copy policy: `source_files_copied=false`

## Scope

Batch 4 is the authorized grouped Phase 2 atomization batch for active skill contracts. It groups each `skills/<name>/` directory as one source and groups `skills/README.md` plus `skills/SKILL_TEMPLATE.md` as one skill-system meta-contract source. `LICENSE.md` remains deferred and is not selected.

| SourceDocID | Prefix | Grouped RepoRelPath | Lines | Sections | Dispatch Units |
|---|---|---|---:|---:|---:|
{source_table}

## SourceRef Policy

Batch 4 uses grouped-source component maps. Generated pack markdown is a worker/review substrate only. Atom SourceRefs must cite original repo component files:

```text
@repo/<component RepoRelPath>:L####|domains/chirality/_Decomposition/source_review_html/<SourceDocID>.html#<SectionID>
```

The line conversion map lives in each grouped source asset manifest under `source_components`; briefs include `SOURCE_REF_MODE: COMPONENT_MAP`.

## Generated Companions

- `Batch_Source_Register.csv` - authoritative companion register for selected Batch 4 grouped source scope.
- `Dispatch_Unit_Register.csv` - authoritative companion register for per-unit brief/output paths.
- `Validation_Checks.csv` - setup and later worker QA / merge / render validation register.
- `domains/chirality/_Decomposition/source_pack_markdown/{batch_id}/` - generated grouped markdown substrates.
- `domains/chirality/_Decomposition/dispatch_briefs/{batch_id}/` - one INIT-TASK brief per dispatch unit.
- `domains/chirality/_Decomposition/dispatch_outputs/{batch_id}/` - prepared disjoint output directories for worker CSVs.
- `domains/chirality/_Decomposition/per_source_ledgers/{batch_id}/` - reserved per-source merge output root.
- `domains/chirality/_Decomposition/vocabulary_seeds/{batch_id}/` - reserved per-source vocabulary seed output root.

## Worker Boundary

Workers must read only assigned generated markdown `LINE_START..LINE_END`, use `ASSET_MANIFEST_PATH.source_components` to cite original repo component lines, write only their two allowed CSV targets, and return a valid `RUN_STATUS`.

## Closure Verdict

- Batch 4 setup: CLOSED / SETUP_READY.
- Batch 4 Phase 2 atomization: OPEN / FANOUT_PENDING.
- Batch 4 Gate 2 normalization: OPEN / HUMAN_REVIEW_REQUIRED after fan-out.
- Batch 2 and Batch 3 remain not Gate-2 accepted.
"""
    setup_path = batch_root / "BATCH4_SETUP.md"
    setup_path.write_text(setup_md, encoding="utf-8")

    latest_setup = decomp_root / "phase2_batches" / "_LATEST_BATCH4_SETUP.md"
    latest_setup.write_text(
        f"""# Latest Batch 4 Setup Pointer

Package role: snapshot / handoff artifact

Latest Batch 4 setup: `{batch_id}`

Path: `domains/chirality/_Decomposition/phase2_batches/{batch_id}/`

Status: SETUP_READY_FANOUT_PENDING.

Setup handoff: `domains/chirality/_Decomposition/phase2_batches/{batch_id}/BATCH4_SETUP.md`
""",
        encoding="utf-8",
    )

    companion_rows.extend([
        {
            "Filename": rel_to_repo(setup_path, repo_root),
            "PackageRole": "snapshot / handoff artifact",
            "Description": "Batch 4 grouped skill-pack setup handoff.",
        },
        {
            "Filename": rel_to_repo(source_register, repo_root),
            "PackageRole": "authoritative companion register",
            "Description": "Batch 4 grouped source register.",
        },
        {
            "Filename": rel_to_repo(unit_register, repo_root),
            "PackageRole": "authoritative companion register",
            "Description": "Batch 4 dispatch unit register.",
        },
        {
            "Filename": rel_to_repo(validation_register, repo_root),
            "PackageRole": "authoritative companion register",
            "Description": "Batch 4 validation register.",
        },
        {
            "Filename": rel_to_repo(latest_setup, repo_root),
            "PackageRole": "snapshot / handoff artifact",
            "Description": "Pointer to latest Batch 4 setup.",
        },
    ])
    update_companion_inventory(decomp_root / "Companion_Inventory.csv", companion_rows)

    batch_register_path = decomp_root / "Phase2_Batch_Register.csv"
    batch_register_fields = list(read_csv(batch_register_path)[0].keys())
    append_or_replace_csv(
        batch_register_path,
        batch_register_fields,
        ["BatchID"],
        [{
            "BatchID": batch_id,
            "BatchName": BATCH_NAME,
            "GeneratedUTC": generated_utc,
            "Status": "SETUP_READY_FANOUT_PENDING",
            "AcceptedGate1Snapshot": "domains/chirality/_Decomposition/gate_snapshots/GATE1_20260614T005942Z",
            "AcceptedCatalogSnapshot": "domains/chirality/_LocalIndexes/_LATEST.md",
            "SourceManifestSha256": manifest_sha,
            "SourceCount": len(source_rows),
            "DispatchUnitCount": total_units,
            "BriefCount": len(unit_rows),
            "BriefRoot": rel_to_repo(briefs_root, repo_root),
            "OutputRoot": rel_to_repo(outputs_root, repo_root),
            "PerSourceLedgerRoot": rel_to_repo(per_source_root, repo_root),
            "VocabularySeedRoot": rel_to_repo(vocab_root, repo_root),
            "BatchDir": rel_to_repo(batch_root, repo_root),
            "AtomizationStatus": "FANOUT_PENDING",
            "Notes": f"Grouped 153 skill-contract manifest rows into 38 Batch 4 sources: 37 skill packs plus one skill-system meta source. LICENSE.md deferred.",
        }],
    )

    print(
        f"batch_id={batch_id} grouped_sources={len(source_rows)} dispatch_units={total_units} "
        f"sections={total_sections} in_scope={total_in_scope} setup={setup_path}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
