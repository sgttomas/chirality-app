#!/usr/bin/env python3
"""Build a Chirality source database V2 snapshot for a domain.

Usage:
  python3 tools/source_catalog/build_source_database.py \
      --domain-root domains/piping-design

  python3 tools/source_catalog/build_source_database.py \
      --domain-root domains/chirality \
      --repo-root . \
      --source-manifest domains/chirality/_Sources/Source_Manifest.csv

Inputs:
  --domain-root                Domain package root. Defaults to piping-design.
  --out-root                   Output root. Defaults to <domain-root>/_LocalIndexes.
  --repo-root                  Repository root used to resolve @repo/ catalog paths.
  --source-manifest            CSV of repo-relative source files. When provided,
                               manifest rows define catalog membership.
  --include-archive-metadata   Catalog archive files as ARCHIVE metadata. Archive
                               files are never indexable.

Outputs:
  <out-root>/snapshots/SRCIDX_<UTC>/
    catalog.sqlite
    Artifacts.csv
    SourceDocs.csv
    AuditState.csv
    Chunks.csv
    meta.json
    QA_Report.md
  <out-root>/_LATEST.md

The snapshot is derived, local-only, and rebuildable. It references source
artifacts in place by relative path and hash; it does not copy source files.
"""
from __future__ import annotations

import argparse
import json
import os
import sqlite3
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from source_database import (  # noqa: E402
    ARTIFACT_COLUMNS,
    AUDIT_STATE_COLUMNS,
    CHUNK_COLUMNS,
    DEFAULT_DOMAIN_ROOT,
    DEFAULT_OUT_ROOT_NAME,
    REPO_PATH_PREFIX,
    SCHEMA_VERSION,
    SNAPSHOT_PREFIX,
    SOURCE_DOC_COLUMNS,
    AuditState,
    Chunk,
    Artifact,
    SourceDoc,
    artifact_role,
    catalog_path,
    audit_kind_and_role,
    count_json_entries,
    indexable_for_role,
    init_schema,
    insert_many,
    is_archive_path,
    load_csv_rows,
    markdown_chunks,
    media_type_for,
    rel_to,
    sha256_file,
    should_skip_dir,
    source_doc_id_for_rel,
    source_root_for_rel,
    stable_id,
    text_hash,
    truncate_text,
    write_csv,
)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--domain-root", type=Path, default=DEFAULT_DOMAIN_ROOT)
    ap.add_argument("--out-root", type=Path)
    ap.add_argument("--repo-root", type=Path, help="Repository root for @repo manifest paths")
    ap.add_argument("--source-manifest", type=Path, help="CSV manifest of repo-relative source files to index")
    ap.add_argument("--include-archive-metadata", action="store_true")
    args = ap.parse_args()

    domain_root = args.domain_root.resolve()
    if not domain_root.exists():
        print(f"ERROR: domain root not found: {domain_root}", file=sys.stderr)
        return 2
    sources_root = domain_root / "_Sources"
    if not sources_root.exists():
        print(f"ERROR: _Sources not found under domain root: {sources_root}", file=sys.stderr)
        return 2

    out_root = (args.out_root or (domain_root / DEFAULT_OUT_ROOT_NAME)).resolve()
    repo_root = args.repo_root.resolve() if args.repo_root else Path.cwd().resolve()
    source_manifest = args.source_manifest.resolve() if args.source_manifest else None
    snapshot_dir = create_snapshot_dir(out_root)
    started = datetime.now(timezone.utc)

    print(f"[1/6] Scanning artifacts under {domain_root}")
    artifacts, source_metadata = collect_artifacts(
        domain_root,
        args.include_archive_metadata,
        repo_root=repo_root,
        source_manifest=source_manifest,
    )
    print(f"      {len(artifacts):,} artifacts")

    print("[2/6] Resolving source documents and generated-from relations")
    artifacts = assign_generated_from(artifacts)
    source_docs = collect_source_docs(domain_root, artifacts, source_metadata)
    print(f"      {len(source_docs):,} source docs")

    print("[3/6] Extracting audit state")
    audit_state = collect_audit_state(domain_root, artifacts, repo_root=repo_root)
    print(f"      {len(audit_state):,} audit rows")

    print("[4/6] Building searchable chunks")
    chunks = collect_chunks(domain_root, artifacts, repo_root=repo_root)
    source_docs = ensure_source_docs_for_chunks(source_docs, chunks)
    print(f"      {len(chunks):,} chunks")

    print("[5/6] Writing SQLite catalog and CSV exports")
    db_path = snapshot_dir / "catalog.sqlite"
    con = sqlite3.connect(str(db_path))
    init_schema(con)
    insert_many(con, "source_docs", SOURCE_DOC_COLUMNS, [source_doc_to_row(r) for r in source_docs])
    insert_many(con, "artifacts", ARTIFACT_COLUMNS, [artifact_to_row(r) for r in artifacts])
    insert_many(con, "audit_state", AUDIT_STATE_COLUMNS, [audit_to_row(r) for r in audit_state])
    insert_many(con, "chunks", CHUNK_COLUMNS, [chunk_to_row(r) for r in chunks])
    con.close()

    write_csv(snapshot_dir / "SourceDocs.csv", SOURCE_DOC_COLUMNS, [source_doc_to_row(r) for r in source_docs])
    write_csv(snapshot_dir / "Artifacts.csv", ARTIFACT_COLUMNS, [artifact_to_row(r) for r in artifacts])
    write_csv(snapshot_dir / "AuditState.csv", AUDIT_STATE_COLUMNS, [audit_to_row(r) for r in audit_state])
    write_csv(snapshot_dir / "Chunks.csv", CHUNK_COLUMNS, [chunk_to_row(r) for r in chunks])

    print("[6/6] Writing metadata, QA report, and _LATEST.md")
    finished = datetime.now(timezone.utc)
    meta = {
        "schema_version": SCHEMA_VERSION,
        "build_utc": finished.isoformat(timespec="seconds"),
        "domain_root": str(domain_root),
        "repo_root": str(repo_root) if source_manifest else None,
        "source_manifest": str(source_manifest) if source_manifest else None,
        "out_root": str(out_root),
        "snapshot_dir": str(snapshot_dir),
        "include_archive_metadata": bool(args.include_archive_metadata),
        "artifact_count": len(artifacts),
        "source_doc_count": len(source_docs),
        "audit_state_count": len(audit_state),
        "chunk_count": len(chunks),
        "elapsed_seconds": round((finished - started).total_seconds(), 2),
        "artifacts_sha256": sha256_file(snapshot_dir / "Artifacts.csv"),
        "chunks_sha256": sha256_file(snapshot_dir / "Chunks.csv"),
        "derived_only": True,
        "source_files_copied": False,
    }
    (snapshot_dir / "meta.json").write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")
    write_qa_report(snapshot_dir / "QA_Report.md", meta, artifacts, source_docs, audit_state, chunks)
    write_latest(out_root, snapshot_dir, meta)

    print(f"DONE: {snapshot_dir}")
    return 0


def create_snapshot_dir(out_root: Path) -> Path:
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    base = out_root / "snapshots" / f"{SNAPSHOT_PREFIX}_{stamp}"
    candidate = base
    i = 1
    while candidate.exists():
        candidate = Path(f"{base}_{i:02d}")
        i += 1
    candidate.mkdir(parents=True)
    return candidate


def iter_catalog_paths(
    domain_root: Path,
    include_archive_metadata: bool,
    root_names: tuple[str, ...] = ("_Sources", "_Decomposition"),
):
    for root_name in root_names:
        root = domain_root / root_name
        if not root.exists():
            continue
        for current, dirs, files in os.walk(root):
            current_path = Path(current)
            dirs[:] = sorted(
                d for d in dirs
                if not should_skip_dir(current_path / d, include_archive_metadata)
            )
            for name in sorted(files):
                path = current_path / name
                if path.name == ".DS_Store":
                    continue
                if is_archive_path(path) and not include_archive_metadata:
                    continue
                yield path


REQUIRED_SOURCE_MANIFEST_COLUMNS = [
    "SourceDocID",
    "SourceName",
    "RepoRelPath",
    "SourceGroup",
    "AuthorityRole",
    "IncludeInIndex",
    "ArchiveState",
    "ExpectedSha256",
    "Notes",
]


def collect_artifacts(
    domain_root: Path,
    include_archive_metadata: bool,
    *,
    repo_root: Path | None = None,
    source_manifest: Path | None = None,
) -> tuple[list[Artifact], dict[str, dict[str, str]]]:
    source_metadata: dict[str, dict[str, str]] = {}
    if source_manifest:
        if repo_root is None:
            raise ValueError("--repo-root is required with --source-manifest")
        artifacts, source_metadata = collect_manifest_artifacts(source_manifest, repo_root)
        artifacts.extend(
            collect_local_artifacts(
                domain_root,
                include_archive_metadata,
                root_names=("_Decomposition",),
                include_rel_path=is_manifest_companion_artifact,
            )
        )
    else:
        artifacts = collect_local_artifacts(domain_root, include_archive_metadata)
    seen: set[str] = set()
    for art in artifacts:
        if art.rel_path in seen:
            raise ValueError(f"duplicate artifact rel_path: {art.rel_path}")
        seen.add(art.rel_path)
    artifacts.sort(key=lambda a: a.rel_path)
    return artifacts, source_metadata


def collect_local_artifacts(
    domain_root: Path,
    include_archive_metadata: bool,
    *,
    root_names: tuple[str, ...] = ("_Sources", "_Decomposition"),
    include_rel_path=None,
) -> list[Artifact]:
    artifacts: list[Artifact] = []
    for path in iter_catalog_paths(domain_root, include_archive_metadata, root_names):
        if not path.is_file():
            continue
        rel_path = rel_to(domain_root, path)
        if include_rel_path is not None and not include_rel_path(rel_path):
            continue
        archive_state = "ARCHIVE" if is_archive_path(Path(rel_path)) else "ACTIVE"
        role = artifact_role(rel_path)
        stat = path.stat()
        digest = sha256_file(path)
        artifacts.append(
            Artifact(
                artifact_id=stable_id("ART", rel_path, digest),
                source_doc_id=source_doc_id_for_rel(rel_path),
                rel_path=rel_path,
                artifact_role=role,
                media_type=media_type_for(path),
                extension=path.suffix.lower().lstrip("."),
                size_bytes=stat.st_size,
                mtime_ns=stat.st_mtime_ns,
                sha256=digest,
                archive_state=archive_state,
                generated_from_artifact_id=None,
                indexable=indexable_for_role(role, archive_state),
            )
        )
    return artifacts


def is_manifest_companion_artifact(rel_path: str) -> bool:
    role = artifact_role(rel_path)
    return role in {
        "SECTION_NODES_CSV",
        "DECOMPOSITION_LEDGER_CSV",
        "AUDIT_SIDECAR_JSON",
        "AUDIT_JSONL",
    }


def read_source_manifest(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise FileNotFoundError(str(path))
    rows = load_csv_rows(path)
    if not rows:
        return []
    missing = [name for name in REQUIRED_SOURCE_MANIFEST_COLUMNS if name not in rows[0]]
    if missing:
        raise ValueError(f"source manifest missing columns: {', '.join(missing)}")
    return rows


def collect_manifest_artifacts(
    source_manifest: Path,
    repo_root: Path,
) -> tuple[list[Artifact], dict[str, dict[str, str]]]:
    artifacts: list[Artifact] = []
    source_metadata: dict[str, dict[str, str]] = {}
    for line_num, row in enumerate(read_source_manifest(source_manifest), start=2):
        source_doc_id = row.get("SourceDocID", "").strip()
        repo_rel = row.get("RepoRelPath", "").strip()
        include = row.get("IncludeInIndex", "").strip().upper()
        archive_state = (row.get("ArchiveState", "").strip().upper() or "ACTIVE")
        expected_sha = row.get("ExpectedSha256", "").strip().lower()
        if not source_doc_id:
            raise ValueError(f"source manifest line {line_num}: SourceDocID is required")
        if not repo_rel:
            raise ValueError(f"source manifest line {line_num}: RepoRelPath is required")
        if include not in {"YES", "NO"}:
            raise ValueError(f"source manifest line {line_num}: IncludeInIndex must be YES or NO")
        if archive_state not in {"ACTIVE", "ARCHIVE"}:
            raise ValueError(f"source manifest line {line_num}: ArchiveState must be ACTIVE or ARCHIVE")
        rel_candidate = Path(repo_rel)
        if rel_candidate.is_absolute() or ".." in rel_candidate.parts:
            raise ValueError(f"source manifest line {line_num}: RepoRelPath must stay inside repo root")
        path = (repo_root / rel_candidate).resolve()
        try:
            path.relative_to(repo_root.resolve())
        except ValueError as exc:
            raise ValueError(f"source manifest line {line_num}: RepoRelPath escapes repo root") from exc
        if not path.is_file():
            raise FileNotFoundError(f"source manifest line {line_num}: source file not found: {repo_rel}")
        rel_path = f"{REPO_PATH_PREFIX}{rel_candidate.as_posix()}"
        role = artifact_role(rel_path)
        if include == "YES" and role != "SOURCE_MARKDOWN":
            raise ValueError(
                f"source manifest line {line_num}: IncludeInIndex=YES is only supported "
                f"for Markdown files in v1, found role={role}"
            )
        actual_sha = sha256_file(path)
        digest = expected_sha or actual_sha
        stat = path.stat()
        artifacts.append(
            Artifact(
                artifact_id=stable_id("ART", rel_path, digest),
                source_doc_id=source_doc_id,
                rel_path=rel_path,
                artifact_role=role,
                media_type=media_type_for(path),
                extension=path.suffix.lower().lstrip("."),
                size_bytes=stat.st_size,
                mtime_ns=stat.st_mtime_ns,
                sha256=digest,
                archive_state=archive_state,
                generated_from_artifact_id=None,
                indexable=1 if archive_state == "ACTIVE" and include == "YES" else 0,
            )
        )
        source_metadata[source_doc_id] = {
            "SourceName": row.get("SourceName", "").strip() or source_doc_id.removeprefix("SRC-"),
            "SourceGroup": row.get("SourceGroup", "").strip(),
            "AuthorityRole": row.get("AuthorityRole", "").strip(),
            "RepoRelPath": rel_candidate.as_posix(),
            "ExpectedSha256": expected_sha,
        }
    return artifacts, source_metadata


def assign_generated_from(artifacts: list[Artifact]) -> list[Artifact]:
    primary_pdf_by_source: dict[str, str] = {}
    for art in artifacts:
        if art.source_doc_id and art.artifact_role == "SOURCE_PDF":
            primary_pdf_by_source.setdefault(art.source_doc_id, art.artifact_id)

    generated_roles = {
        "SOURCE_MARKDOWN",
        "PAGE_MARKDOWN",
        "PAGE_RASTER_PNG",
        "PAGE_WORK_JSON",
        "ASSET_MANIFEST_JSON",
        "SECTION_NODES_CSV",
        "FIGURE_PNG",
        "IMAGE_PNG",
        "TABLE_PNG",
        "TABLE_XLSX",
        "TABLE_JSON",
        "TABLE_CSV",
        "AUDIT_HTML",
        "AUDIT_JSONL",
        "AUDIT_SIDECAR_JSON",
    }
    out: list[Artifact] = []
    for art in artifacts:
        generated_from = art.generated_from_artifact_id
        if art.source_doc_id and art.artifact_role in generated_roles:
            generated_from = primary_pdf_by_source.get(art.source_doc_id)
        out.append(
            Artifact(
                artifact_id=art.artifact_id,
                source_doc_id=art.source_doc_id,
                rel_path=art.rel_path,
                artifact_role=art.artifact_role,
                media_type=art.media_type,
                extension=art.extension,
                size_bytes=art.size_bytes,
                mtime_ns=art.mtime_ns,
                sha256=art.sha256,
                archive_state=art.archive_state,
                generated_from_artifact_id=generated_from,
                indexable=art.indexable,
            )
        )
    return out


def collect_source_docs(
    domain_root: Path,
    artifacts: list[Artifact],
    source_metadata: dict[str, dict[str, str]] | None = None,
) -> list[SourceDoc]:
    source_metadata = source_metadata or {}
    grouped: dict[str, list[Artifact]] = defaultdict(list)
    roots: dict[str, str] = {}
    for art in artifacts:
        if not art.source_doc_id:
            continue
        grouped[art.source_doc_id].append(art)
        root = source_root_for_rel(art.rel_path)
        if root:
            current = roots.get(art.source_doc_id)
            if current is None or (Path(current).suffix and not root.startswith("_Decomposition")):
                roots[art.source_doc_id] = root

    source_docs: list[SourceDoc] = []
    for source_doc_id, group in grouped.items():
        primary_md = first_artifact_id(group, "SOURCE_MARKDOWN")
        section_nodes = first_artifact_id(group, "SECTION_NODES_CSV")
        source_root = roots.get(source_doc_id, "")
        meta = source_metadata.get(source_doc_id, {})
        audit_dir = None
        if source_root and (domain_root / source_root / "audit").exists():
            audit_dir = f"{source_root}/audit"
        archive_state = "ARCHIVE" if all(a.archive_state == "ARCHIVE" for a in group) else "ACTIVE"
        source_docs.append(
            SourceDoc(
                source_doc_id=source_doc_id,
                source_name=meta.get("SourceName") or source_doc_id.removeprefix("SRC-"),
                source_root_rel_path=source_root,
                archive_state=archive_state,
                primary_md_artifact_id=primary_md,
                section_nodes_artifact_id=section_nodes,
                audit_dir_rel_path=audit_dir,
            )
        )
    source_docs.sort(key=lambda s: s.source_doc_id)
    return source_docs


def ensure_source_docs_for_chunks(source_docs: list[SourceDoc], chunks: list[Chunk]) -> list[SourceDoc]:
    existing = {s.source_doc_id for s in source_docs}
    additions: list[SourceDoc] = []
    for source_doc_id in sorted({c.source_doc_id for c in chunks if c.source_doc_id} - existing):
        additions.append(
            SourceDoc(
                source_doc_id=source_doc_id,
                source_name=source_doc_id.removeprefix("SRC-"),
                source_root_rel_path="",
                archive_state="ACTIVE",
                primary_md_artifact_id=None,
                section_nodes_artifact_id=None,
                audit_dir_rel_path=None,
            )
        )
    return sorted([*source_docs, *additions], key=lambda s: s.source_doc_id)


def first_artifact_id(group: list[Artifact], role: str) -> str | None:
    for art in sorted(group, key=lambda a: a.rel_path):
        if art.artifact_role == role and art.archive_state == "ACTIVE":
            return art.artifact_id
    return None


def collect_audit_state(
    domain_root: Path,
    artifacts: list[Artifact],
    *,
    repo_root: Path | None = None,
) -> list[AuditState]:
    rows: list[AuditState] = []
    for art in artifacts:
        if art.artifact_role not in {"AUDIT_HTML", "AUDIT_JSONL", "AUDIT_SIDECAR_JSON"}:
            continue
        kind, role = audit_kind_and_role(art.rel_path)
        status_count = None
        if art.artifact_role in {"AUDIT_JSONL", "AUDIT_SIDECAR_JSON"}:
            status_count = count_json_entries(catalog_path(domain_root, art.rel_path, repo_root))
        rows.append(
            AuditState(
                audit_id=stable_id("AUD", art.rel_path, art.sha256),
                source_doc_id=art.source_doc_id,
                artifact_id=art.artifact_id,
                audit_kind=kind,
                audit_role=role,
                rel_path=art.rel_path,
                status_count=status_count,
                archive_state=art.archive_state,
            )
        )
    rows.sort(key=lambda r: r.rel_path)
    return rows


def collect_chunks(
    domain_root: Path,
    artifacts: list[Artifact],
    *,
    repo_root: Path | None = None,
) -> list[Chunk]:
    chunks: list[Chunk] = []
    for art in artifacts:
        if not art.indexable:
            continue
        path = catalog_path(domain_root, art.rel_path, repo_root)
        try:
            if art.artifact_role in {"SOURCE_MARKDOWN", "PAGE_MARKDOWN"}:
                chunks.extend(chunks_from_markdown(path, art))
            elif art.artifact_role == "SECTION_NODES_CSV":
                chunks.extend(chunks_from_section_nodes(path, art))
            elif art.artifact_role == "DECOMPOSITION_LEDGER_CSV":
                chunks.extend(chunks_from_ledger(path, art))
            elif art.artifact_role in {"AUDIT_SIDECAR_JSON", "AUDIT_JSONL"}:
                chunks.extend(chunks_from_audit(path, art))
        except Exception as exc:
            chunks.append(error_chunk(art, f"chunk extraction failed: {exc!r}"))
    chunks.sort(key=lambda c: (c.rel_path, c.chunk_ordinal, c.chunk_id))
    return chunks


def chunks_from_markdown(path: Path, art: Artifact) -> list[Chunk]:
    text = path.read_text(encoding="utf-8", errors="replace")
    out: list[Chunk] = []
    page_label = page_label_from_path(path)
    for i, (heading, body) in enumerate(markdown_chunks(text), start=1):
        searchable = truncate_text(body)
        h = text_hash(searchable)
        out.append(
            Chunk(
                chunk_id=stable_id("CHK", "markdown", art.artifact_id, i, h),
                artifact_id=art.artifact_id,
                source_doc_id=art.source_doc_id,
                chunk_type="MARKDOWN_SECTION",
                rel_path=art.rel_path,
                source_ref=f"{art.rel_path}:chunk-{i:04d}",
                heading=heading,
                page_label=page_label,
                chunk_ordinal=i,
                text_hash=h,
                text=searchable,
                category_id=None,
                knowledge_type_id=None,
                subject_id=None,
                atomic_unit_id=None,
                audit_kind=None,
                audit_state=None,
                archive_state=art.archive_state,
            )
        )
    return out


def chunks_from_section_nodes(path: Path, art: Artifact) -> list[Chunk]:
    rows = load_csv_rows(path)
    out: list[Chunk] = []
    for i, row in enumerate(rows, start=1):
        section_id = row.get("SectionID") or row.get("section_id") or f"row-{i}"
        title = row.get("Title") or row.get("title") or ""
        body = row.get("Text") or row.get("text") or ""
        source_doc_id = (
            source_doc_id_from_source_doc(row.get("SourceDoc") or row.get("SourceDocID"))
            or art.source_doc_id
        )
        searchable = truncate_text((title + "\n\n" + body).strip())
        if not searchable:
            continue
        h = text_hash(searchable)
        source_ref = row.get("HtmlAnchor") or row.get("html_anchor") or f"{art.rel_path}#{section_id}"
        out.append(
            Chunk(
                chunk_id=stable_id("CHK", "section", art.artifact_id, section_id, h),
                artifact_id=art.artifact_id,
                source_doc_id=source_doc_id,
                chunk_type="SECTION_NODE",
                rel_path=art.rel_path,
                source_ref=source_ref,
                heading=title or None,
                page_label=row.get("PageFirst") or None,
                chunk_ordinal=i,
                text_hash=h,
                text=searchable,
                category_id=None,
                knowledge_type_id=None,
                subject_id=None,
                atomic_unit_id=None,
                audit_kind=None,
                audit_state=None,
                archive_state=art.archive_state,
            )
        )
    return out


def chunks_from_ledger(path: Path, art: Artifact) -> list[Chunk]:
    rows = load_csv_rows(path)
    out: list[Chunk] = []
    for i, row in enumerate(rows, start=1):
        statement = row.get("UnitStatement") or row.get("AtomicStatement") or ""
        if not statement.strip():
            continue
        searchable = truncate_text(statement)
        h = text_hash(searchable)
        atomic_id = row.get("AtomicUnitID") or row.get("UnitID") or None
        out.append(
            Chunk(
                chunk_id=stable_id("CHK", "ledger", atomic_id or i, h),
                artifact_id=art.artifact_id,
                source_doc_id=source_doc_id_from_source_doc(row.get("SourceDoc")) or art.source_doc_id,
                chunk_type="LEDGER_ATOM",
                rel_path=art.rel_path,
                source_ref=row.get("SourceRef") or f"{art.rel_path}:row-{i}",
                heading=row.get("UnitType") or None,
                page_label=None,
                chunk_ordinal=i,
                text_hash=h,
                text=searchable,
                category_id=row.get("CategoryID") or None,
                knowledge_type_id=row.get("KnowledgeTypeID(s)") or row.get("KnowledgeTypeIDs") or None,
                subject_id=row.get("SubjectID(s)") or row.get("SubjectIDs") or None,
                atomic_unit_id=atomic_id,
                audit_kind=None,
                audit_state=None,
                archive_state=art.archive_state,
            )
        )
    return out


def chunks_from_audit(path: Path, art: Artifact) -> list[Chunk]:
    kind, role = audit_kind_and_role(art.rel_path)
    entries: list[str] = []
    if path.suffix.lower() == ".jsonl":
        entries = [line for line in path.read_text(encoding="utf-8", errors="replace").splitlines() if line.strip()]
    else:
        try:
            data = json.loads(path.read_text(encoding="utf-8", errors="replace"))
        except Exception as exc:
            entries = [f"Invalid JSON audit sidecar: {exc!r}"]
        else:
            if isinstance(data, list):
                entries = [json.dumps(v, ensure_ascii=False, sort_keys=True) for v in data]
            elif isinstance(data, dict):
                entries = [
                    f"{k}: {json.dumps(v, ensure_ascii=False, sort_keys=True)}"
                    for k, v in sorted(data.items(), key=lambda kv: str(kv[0]))
                ]
            else:
                entries = [json.dumps(data, ensure_ascii=False, sort_keys=True)]
    out: list[Chunk] = []
    for i, entry in enumerate(entries, start=1):
        searchable = truncate_text(entry, max_chars=8000)
        if not searchable:
            continue
        h = text_hash(searchable)
        out.append(
            Chunk(
                chunk_id=stable_id("CHK", "audit", art.artifact_id, i, h),
                artifact_id=art.artifact_id,
                source_doc_id=art.source_doc_id,
                chunk_type="AUDIT_SIDECAR",
                rel_path=art.rel_path,
                source_ref=f"{art.rel_path}:entry-{i:04d}",
                heading=None,
                page_label=None,
                chunk_ordinal=i,
                text_hash=h,
                text=searchable,
                category_id=None,
                knowledge_type_id=None,
                subject_id=None,
                atomic_unit_id=None,
                audit_kind=kind,
                audit_state=role,
                archive_state=art.archive_state,
            )
        )
    return out


def error_chunk(art: Artifact, message: str) -> Chunk:
    h = text_hash(message)
    return Chunk(
        chunk_id=stable_id("CHK", "error", art.artifact_id, h),
        artifact_id=art.artifact_id,
        source_doc_id=art.source_doc_id,
        chunk_type="EXTRACTION_ERROR",
        rel_path=art.rel_path,
        source_ref=art.rel_path,
        heading=None,
        page_label=None,
        chunk_ordinal=0,
        text_hash=h,
        text=message,
        category_id=None,
        knowledge_type_id=None,
        subject_id=None,
        atomic_unit_id=None,
        audit_kind=None,
        audit_state=None,
        archive_state=art.archive_state,
    )


def page_label_from_path(path: Path) -> str | None:
    m = __import__("re").search(r"page[_-](\d+)", path.name, flags=__import__("re").IGNORECASE)
    return m.group(1) if m else None


def source_doc_id_from_source_doc(value: str | None) -> str | None:
    if not value:
        return None
    token = __import__("re").sub(r"[^A-Za-z0-9]+", "-", Path(value.strip()).stem).strip("-").upper()
    if not token:
        return None
    if token.startswith("SRC-"):
        return token
    return "SRC-" + token


def artifact_to_row(a: Artifact) -> dict:
    return a.__dict__


def source_doc_to_row(s: SourceDoc) -> dict:
    return s.__dict__


def audit_to_row(a: AuditState) -> dict:
    return a.__dict__


def chunk_to_row(c: Chunk) -> dict:
    return c.__dict__


def write_latest(out_root: Path, snapshot_dir: Path, meta: dict) -> None:
    out_root.mkdir(parents=True, exist_ok=True)
    rel_snapshot = snapshot_dir.relative_to(out_root).as_posix()
    text = (
        f"Latest: {rel_snapshot}\n"
        f"Updated: {meta['build_utc']}\n"
        f"Schema: {meta['schema_version']}\n"
        f"Artifacts: {meta['artifact_count']}\n"
        f"Chunks: {meta['chunk_count']}\n"
        f"Derived-only: true\n"
    )
    (out_root / "_LATEST.md").write_text(text, encoding="utf-8")


def write_qa_report(
    path: Path,
    meta: dict,
    artifacts: list[Artifact],
    source_docs: list[SourceDoc],
    audit_state: list[AuditState],
    chunks: list[Chunk],
) -> None:
    role_counts = Counter(a.artifact_role for a in artifacts)
    chunk_counts = Counter(c.chunk_type for c in chunks)
    archive_counts = Counter(a.archive_state for a in artifacts)
    missing_audit = [
        s.source_doc_id for s in source_docs
        if s.archive_state == "ACTIVE"
        and s.source_root_rel_path.startswith("_Sources/")
        and s.audit_dir_rel_path is None
    ]
    lines = [
        "# Source Database QA Report",
        "",
        f"- Schema: `{meta['schema_version']}`",
        f"- Build UTC: `{meta['build_utc']}`",
        f"- Domain root: `{meta['domain_root']}`",
        f"- Repo root: `{meta.get('repo_root') or 'N/A'}`",
        f"- Source manifest: `{meta.get('source_manifest') or 'N/A'}`",
        f"- Snapshot: `{meta['snapshot_dir']}`",
        f"- Source files copied: `{str(meta['source_files_copied']).lower()}`",
        "",
        "## Counts",
        "",
        f"- Source docs: {len(source_docs)}",
        f"- Artifacts: {len(artifacts)}",
        f"- Audit rows: {len(audit_state)}",
        f"- Chunks: {len(chunks)}",
        "",
        "## Artifact Roles",
        "",
    ]
    lines.extend(f"- `{role}`: {count}" for role, count in sorted(role_counts.items()))
    lines.extend(["", "## Chunk Types", ""])
    lines.extend(f"- `{role}`: {count}" for role, count in sorted(chunk_counts.items()))
    lines.extend(["", "## Archive State", ""])
    lines.extend(f"- `{state}`: {count}" for state, count in sorted(archive_counts.items()))
    lines.extend(["", "## Findings", ""])
    if missing_audit:
        lines.append(f"- WARNING: active source docs without audit directory: {', '.join(missing_audit)}")
    else:
        lines.append("- PASS: active source docs with expected audit directories were detected where present.")
    if any(c.chunk_type == "EXTRACTION_ERROR" for c in chunks):
        lines.append("- WARNING: one or more artifacts produced `EXTRACTION_ERROR` chunks.")
    else:
        lines.append("- PASS: no chunk extraction errors recorded.")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    raise SystemExit(main())
