#!/usr/bin/env python3
"""Shared helpers for the Chirality source database V2 tools.

This module is deterministic and has no external dependencies. The source
database is a derived local catalog over filesystem truth; it never owns or
copies source artifacts.
"""
from __future__ import annotations

import csv
import hashlib
import json
import mimetypes
import re
import sqlite3
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


SCHEMA_VERSION = "chirality-source-db/v2"
DEFAULT_DOMAIN_ROOT = Path("domains/piping-design")
DEFAULT_OUT_ROOT_NAME = "_LocalIndexes"
SNAPSHOT_PREFIX = "SRCIDX"
REPO_PATH_PREFIX = "@repo/"

ARTIFACT_COLUMNS = [
    "artifact_id",
    "source_doc_id",
    "rel_path",
    "artifact_role",
    "media_type",
    "extension",
    "size_bytes",
    "mtime_ns",
    "sha256",
    "archive_state",
    "generated_from_artifact_id",
    "indexable",
]

SOURCE_DOC_COLUMNS = [
    "source_doc_id",
    "source_name",
    "source_root_rel_path",
    "archive_state",
    "primary_md_artifact_id",
    "section_nodes_artifact_id",
    "audit_dir_rel_path",
]

AUDIT_STATE_COLUMNS = [
    "audit_id",
    "source_doc_id",
    "artifact_id",
    "audit_kind",
    "audit_role",
    "rel_path",
    "status_count",
    "archive_state",
]

CHUNK_COLUMNS = [
    "chunk_id",
    "artifact_id",
    "source_doc_id",
    "chunk_type",
    "rel_path",
    "source_ref",
    "heading",
    "page_label",
    "chunk_ordinal",
    "text_hash",
    "text",
    "category_id",
    "knowledge_type_id",
    "subject_id",
    "atomic_unit_id",
    "audit_kind",
    "audit_state",
    "archive_state",
]


@dataclass(frozen=True)
class Artifact:
    artifact_id: str
    source_doc_id: str | None
    rel_path: str
    artifact_role: str
    media_type: str
    extension: str
    size_bytes: int
    mtime_ns: int
    sha256: str
    archive_state: str
    generated_from_artifact_id: str | None
    indexable: int


@dataclass(frozen=True)
class SourceDoc:
    source_doc_id: str
    source_name: str
    source_root_rel_path: str
    archive_state: str
    primary_md_artifact_id: str | None
    section_nodes_artifact_id: str | None
    audit_dir_rel_path: str | None


@dataclass(frozen=True)
class AuditState:
    audit_id: str
    source_doc_id: str | None
    artifact_id: str
    audit_kind: str
    audit_role: str
    rel_path: str
    status_count: int | None
    archive_state: str


@dataclass(frozen=True)
class Chunk:
    chunk_id: str
    artifact_id: str
    source_doc_id: str | None
    chunk_type: str
    rel_path: str
    source_ref: str | None
    heading: str | None
    page_label: str | None
    chunk_ordinal: int
    text_hash: str
    text: str
    category_id: str | None
    knowledge_type_id: str | None
    subject_id: str | None
    atomic_unit_id: str | None
    audit_kind: str | None
    audit_state: str | None
    archive_state: str


def stable_id(prefix: str, *parts: object, length: int = 20) -> str:
    payload = "\0".join("" if p is None else str(p) for p in parts)
    return f"{prefix}-{hashlib.sha1(payload.encode('utf-8')).hexdigest()[:length]}"


def sha256_file(path: Path, chunk_size: int = 1024 * 1024) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(chunk_size), b""):
            h.update(chunk)
    return h.hexdigest()


def text_hash(text: str) -> str:
    return hashlib.sha1(text.encode("utf-8")).hexdigest()[:16]


def rel_to(root: Path, path: Path) -> str:
    return path.resolve().relative_to(root.resolve()).as_posix()


def is_repo_rel_path(rel_path: str) -> bool:
    return rel_path.startswith(REPO_PATH_PREFIX)


def repo_rel_path(rel_path: str) -> str:
    if not is_repo_rel_path(rel_path):
        raise ValueError(f"not a repo-relative catalog path: {rel_path}")
    return rel_path[len(REPO_PATH_PREFIX):]


def catalog_path(domain_root: Path, rel_path: str, repo_root: Path | None = None) -> Path:
    if is_repo_rel_path(rel_path):
        if repo_root is None:
            raise ValueError(f"repo_root is required to resolve {rel_path}")
        return repo_root / repo_rel_path(rel_path)
    return domain_root / rel_path


def is_archive_path(path: Path) -> bool:
    return any(part.lower() in {"_archive", ".archive", "archive"} for part in path.parts)


def should_skip_dir(path: Path, include_archive_metadata: bool) -> bool:
    if include_archive_metadata:
        return False
    return is_archive_path(path)


def source_doc_id_for_rel(rel_path: str) -> str | None:
    if is_repo_rel_path(rel_path):
        return "SRC-" + slug_token(Path(repo_rel_path(rel_path)).with_suffix("").as_posix())
    parts = Path(rel_path).parts
    if not parts:
        return None
    if (
        parts[0] == "_Decomposition"
        and len(parts) >= 3
        and parts[1] == "source_section_nodes"
        and parts[-1].endswith("_section_nodes.csv")
    ):
        return parts[-1][: -len("_section_nodes.csv")]
    if parts[0] == "_Sources" and len(parts) >= 2:
        name = parts[1]
        if name == "_LATEST.md":
            return None
        if name.endswith("_pdf2md_work"):
            name = name[: -len("_pdf2md_work")]
        if "." in name:
            name = Path(name).stem
        if name.lower() == "_archive":
            return "SRC-ARCHIVE"
        return "SRC-" + slug_token(name)
    if parts[0] == "_Decomposition":
        return None
    return None


def source_root_for_rel(rel_path: str) -> str | None:
    if is_repo_rel_path(rel_path):
        return rel_path
    parts = Path(rel_path).parts
    if parts and parts[0] == "_Sources" and len(parts) >= 2:
        name = parts[1]
        if name == "_LATEST.md":
            return None
        if name.endswith("_pdf2md_work"):
            name = name[: -len("_pdf2md_work")]
        return f"_Sources/{name}"
    if parts and parts[0] == "_Decomposition":
        return "_Decomposition"
    return None


def slug_token(value: str) -> str:
    token = re.sub(r"[^A-Za-z0-9]+", "-", value.strip()).strip("-").upper()
    return token or "UNKNOWN"


def artifact_role(rel_path: str) -> str:
    p = Path(repo_rel_path(rel_path) if is_repo_rel_path(rel_path) else rel_path)
    parts = p.parts
    suffix = p.suffix.lower()
    name = p.name.lower()
    parent_names = {part.lower() for part in parts}

    if name.endswith("_section_nodes.csv"):
        return "SECTION_NODES_CSV"
    if parts and parts[0] == "_Decomposition":
        if suffix == ".csv":
            if name == "atomic_domain_ledger.csv":
                return "DECOMPOSITION_LEDGER_CSV"
            return "DECOMPOSITION_CSV"
        if suffix == ".md":
            return "DECOMPOSITION_MARKDOWN"
    if "audit" in parent_names:
        if suffix == ".html":
            return "AUDIT_HTML"
        if suffix == ".jsonl":
            return "AUDIT_JSONL"
        if suffix == ".json":
            return "AUDIT_SIDECAR_JSON"
    if name.endswith("_assets_manifest.json"):
        return "ASSET_MANIFEST_JSON"
    if parts[:2] == ("_Sources", "_LATEST.md"):
        return "SOURCE_POINTER"
    if "_pdf2md_work" in rel_path:
        if suffix == ".md":
            return "PAGE_MARKDOWN"
        if suffix == ".png":
            return "PAGE_RASTER_PNG"
        if suffix == ".json":
            return "PAGE_WORK_JSON"
    if "figures" in parent_names and suffix == ".png":
        return "FIGURE_PNG"
    if "images" in parent_names and suffix == ".png":
        return "IMAGE_PNG"
    if "tables" in parent_names:
        if suffix == ".png":
            return "TABLE_PNG"
        if suffix == ".xlsx":
            return "TABLE_XLSX"
        if suffix == ".json":
            return "TABLE_JSON"
        if suffix == ".csv":
            return "TABLE_CSV"
    if suffix == ".md":
        return "SOURCE_MARKDOWN"
    if suffix == ".pdf":
        return "SOURCE_PDF"
    if suffix == ".zip":
        return "SOURCE_ZIP"
    if suffix in {".xlsx", ".xls", ".xlsm"}:
        return "SPREADSHEET"
    if suffix in {".json", ".jsonl"}:
        return "JSON"
    if suffix == ".html":
        return "HTML"
    return "OTHER"


def indexable_for_role(role: str, archive_state: str) -> int:
    if archive_state != "ACTIVE":
        return 0
    return 1 if role in {
        "SOURCE_MARKDOWN",
        "PAGE_MARKDOWN",
        "SECTION_NODES_CSV",
        "DECOMPOSITION_LEDGER_CSV",
        "AUDIT_SIDECAR_JSON",
        "AUDIT_JSONL",
    } else 0


def media_type_for(path: Path) -> str:
    mt, _ = mimetypes.guess_type(path.name)
    return mt or "application/octet-stream"


def audit_kind_and_role(rel_path: str) -> tuple[str, str]:
    p = Path(rel_path)
    name = p.name.lower()
    if name.endswith(".html"):
        return (p.stem.lower(), "surface")
    kind = "unknown"
    for candidate in ("equations", "figures", "tables", "images", "folios", "sections", "atoms", "prose"):
        if candidate in name or candidate in [part.lower() for part in p.parts]:
            kind = candidate
            break
    role = "sidecar"
    for candidate in ("verified", "flagged", "backcheck", "rejected", "validation", "proposal"):
        if candidate in name:
            role = candidate
            break
    if name.endswith(".jsonl"):
        role = "jsonl"
    return kind, role


def count_json_entries(path: Path) -> int | None:
    try:
        if path.suffix.lower() == ".jsonl":
            return sum(1 for line in path.read_text(encoding="utf-8", errors="replace").splitlines() if line.strip())
        data = json.loads(path.read_text(encoding="utf-8", errors="replace"))
    except Exception:
        return None
    if isinstance(data, list):
        return len(data)
    if isinstance(data, dict):
        return len(data)
    return 1


def markdown_chunks(text: str) -> list[tuple[str | None, str]]:
    chunks: list[tuple[str | None, str]] = []
    heading: str | None = None
    buf: list[str] = []
    heading_re = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
    for line in text.splitlines():
        m = heading_re.match(line)
        if m and buf:
            chunk = "\n".join(buf).strip()
            if chunk:
                chunks.append((heading, chunk))
            heading = m.group(2).strip()
            buf = [line]
        else:
            if m:
                heading = m.group(2).strip()
            buf.append(line)
    chunk = "\n".join(buf).strip()
    if chunk:
        chunks.append((heading, chunk))
    return chunks


def truncate_text(text: str, max_chars: int = 24000) -> str:
    clean = re.sub(r"\n{3,}", "\n\n", text.strip())
    if len(clean) <= max_chars:
        return clean
    return clean[:max_chars].rstrip() + "\n[TRUNCATED]"


def load_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", errors="replace", newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, fieldnames: list[str], rows: Iterable[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def parse_latest_pointer(path: Path) -> str:
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("Latest:"):
            latest = line.split(":", 1)[1].strip()
            if latest:
                return latest
    raise ValueError(f"no Latest line found in {path}")


def resolve_snapshot_path(snapshot_arg: Path | None, domain_root: Path) -> Path:
    if snapshot_arg is None:
        snapshot_arg = domain_root / DEFAULT_OUT_ROOT_NAME / "_LATEST.md"
    path = snapshot_arg.resolve()
    if path.is_dir():
        if not (path / "catalog.sqlite").exists():
            raise FileNotFoundError(f"snapshot dir has no catalog.sqlite: {path}")
        return path
    if path.is_file() and path.name == "_LATEST.md":
        latest = parse_latest_pointer(path)
        candidate = (path.parent / latest).resolve()
        if not candidate.exists():
            raise FileNotFoundError(f"_LATEST.md points to missing snapshot: {candidate}")
        return candidate
    raise FileNotFoundError(f"snapshot not found or not recognized: {path}")


def init_schema(con: sqlite3.Connection) -> None:
    cur = con.cursor()
    cur.execute("PRAGMA foreign_keys = ON")
    cur.executescript(
        """
        CREATE TABLE source_docs (
          source_doc_id TEXT PRIMARY KEY,
          source_name TEXT NOT NULL,
          source_root_rel_path TEXT NOT NULL,
          archive_state TEXT NOT NULL CHECK (archive_state IN ('ACTIVE', 'ARCHIVE')),
          primary_md_artifact_id TEXT,
          section_nodes_artifact_id TEXT,
          audit_dir_rel_path TEXT
        );

        CREATE TABLE artifacts (
          artifact_id TEXT PRIMARY KEY,
          source_doc_id TEXT REFERENCES source_docs(source_doc_id),
          rel_path TEXT NOT NULL UNIQUE,
          artifact_role TEXT NOT NULL,
          media_type TEXT NOT NULL,
          extension TEXT NOT NULL,
          size_bytes INTEGER NOT NULL,
          mtime_ns INTEGER NOT NULL,
          sha256 TEXT NOT NULL,
          archive_state TEXT NOT NULL CHECK (archive_state IN ('ACTIVE', 'ARCHIVE')),
          generated_from_artifact_id TEXT REFERENCES artifacts(artifact_id),
          indexable INTEGER NOT NULL CHECK (indexable IN (0, 1))
        );

        CREATE TABLE audit_state (
          audit_id TEXT PRIMARY KEY,
          source_doc_id TEXT REFERENCES source_docs(source_doc_id),
          artifact_id TEXT NOT NULL REFERENCES artifacts(artifact_id),
          audit_kind TEXT NOT NULL,
          audit_role TEXT NOT NULL,
          rel_path TEXT NOT NULL,
          status_count INTEGER,
          archive_state TEXT NOT NULL CHECK (archive_state IN ('ACTIVE', 'ARCHIVE'))
        );

        CREATE TABLE chunks (
          chunk_id TEXT PRIMARY KEY,
          artifact_id TEXT NOT NULL REFERENCES artifacts(artifact_id),
          source_doc_id TEXT REFERENCES source_docs(source_doc_id),
          chunk_type TEXT NOT NULL,
          rel_path TEXT NOT NULL,
          source_ref TEXT,
          heading TEXT,
          page_label TEXT,
          chunk_ordinal INTEGER NOT NULL,
          text_hash TEXT NOT NULL,
          text TEXT NOT NULL,
          category_id TEXT,
          knowledge_type_id TEXT,
          subject_id TEXT,
          atomic_unit_id TEXT,
          audit_kind TEXT,
          audit_state TEXT,
          archive_state TEXT NOT NULL CHECK (archive_state IN ('ACTIVE', 'ARCHIVE'))
        );

        CREATE TABLE index_rows (
          index_name TEXT NOT NULL,
          row_index INTEGER NOT NULL,
          chunk_id TEXT NOT NULL REFERENCES chunks(chunk_id),
          PRIMARY KEY (index_name, row_index),
          UNIQUE (index_name, chunk_id)
        );

        CREATE TABLE index_builds (
          index_name TEXT PRIMARY KEY,
          built_utc TEXT NOT NULL,
          embedding_model TEXT,
          embedding_dim INTEGER,
          row_count INTEGER NOT NULL,
          bm25_dir TEXT,
          embeddings_path TEXT,
          embeddings_norm_path TEXT,
          input_chunks_sha256 TEXT NOT NULL,
          status TEXT NOT NULL
        );

        CREATE INDEX idx_artifacts_source_doc ON artifacts(source_doc_id);
        CREATE INDEX idx_artifacts_role ON artifacts(artifact_role);
        CREATE INDEX idx_artifacts_archive ON artifacts(archive_state);
        CREATE INDEX idx_chunks_source_doc ON chunks(source_doc_id);
        CREATE INDEX idx_chunks_type ON chunks(chunk_type);
        CREATE INDEX idx_chunks_structural ON chunks(category_id, knowledge_type_id, subject_id);
        CREATE INDEX idx_chunks_archive ON chunks(archive_state);
        """
    )
    con.commit()


def insert_many(con: sqlite3.Connection, table: str, columns: list[str], rows: Iterable[dict]) -> None:
    placeholders = ",".join("?" for _ in columns)
    sql = f"INSERT INTO {table} ({','.join(columns)}) VALUES ({placeholders})"
    con.executemany(sql, ([row.get(col) for col in columns] for row in rows))
    con.commit()
