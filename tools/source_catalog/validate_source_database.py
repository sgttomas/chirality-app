#!/usr/bin/env python3
"""Validate a Chirality source database V2 snapshot.

Usage:
  python3 tools/source_catalog/validate_source_database.py \
      --snapshot domains/piping-design/_LocalIndexes/_LATEST.md

Inputs:
  --snapshot          Snapshot directory or _LATEST.md pointer. Defaults to
                      <domain-root>/_LocalIndexes/_LATEST.md.
  --domain-root       Domain root override. May be omitted when meta.json
                      records it or CWD contains domain-pack.yaml.
  --repo-root         Repository root for @repo/ manifest-backed source paths.
                      Defaults to repo_root recorded in meta.json when present.
  --skip-hash-verify  Check hash shape but do not re-hash source files.
  --json              Emit machine-readable findings.

Outputs:
  PASS/finding summary on stdout. Exit 0 for pass/warnings, 1 for blockers,
  2 for invalid invocation or unreadable snapshot.
"""
from __future__ import annotations

import argparse
import json
import sqlite3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from source_database import (  # noqa: E402
    DEFAULT_DOMAIN_ROOT,
    SCHEMA_VERSION,
    catalog_path,
    is_repo_rel_path,
    resolve_domain_root,
    sha256_file,
    text_hash,
)


REQUIRED_TABLES = {
    "source_docs",
    "artifacts",
    "audit_state",
    "chunks",
    "index_rows",
    "index_builds",
}

REQUIRED_EXPORTS = [
    "Artifacts.csv",
    "SourceDocs.csv",
    "AuditState.csv",
    "Chunks.csv",
    "meta.json",
    "QA_Report.md",
]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--snapshot", type=Path)
    ap.add_argument("--domain-root", type=Path, default=DEFAULT_DOMAIN_ROOT)
    ap.add_argument("--repo-root", type=Path)
    ap.add_argument("--skip-hash-verify", action="store_true")
    ap.add_argument("--json", action="store_true", dest="emit_json")
    args = ap.parse_args()

    try:
        snapshot = resolve_snapshot(args.snapshot, args.domain_root)
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    findings: list[dict] = []
    meta_path = snapshot / "meta.json"
    if not meta_path.exists():
        print(f"ERROR: missing meta.json under {snapshot}", file=sys.stderr)
        return 2
    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    try:
        domain_root = Path(
            meta.get("domain_root") or resolve_domain_root(args.domain_root)
        ).resolve()
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    repo_root = Path(args.repo_root or meta.get("repo_root") or Path.cwd()).resolve()

    check_exports(snapshot, findings)
    check_schema(snapshot, findings)
    check_counts(snapshot, meta, findings)
    check_paths_and_hashes(snapshot, domain_root, repo_root, args.skip_hash_verify, findings)
    check_chunks(snapshot, findings)
    check_audit_surfaces(snapshot, domain_root, findings)

    blockers = [f for f in findings if f["severity"] == "BLOCKER"]
    warnings = [f for f in findings if f["severity"] == "WARNING"]
    payload = {
        "snapshot": str(snapshot),
        "schema_version": meta.get("schema_version"),
        "blocker_count": len(blockers),
        "warning_count": len(warnings),
        "findings": findings,
    }
    if args.emit_json:
        print(json.dumps(payload, indent=2))
    else:
        status = "PASS" if not blockers else "FAIL"
        print(
            f"{status}: {snapshot} "
            f"({len(blockers)} blockers, {len(warnings)} warnings)"
        )
        for f in findings[:80]:
            print(f"{f['severity']}: {f['code']}: {f['message']}")
        if len(findings) > 80:
            print(f"... {len(findings) - 80} more findings omitted")
    return 1 if blockers else 0


def resolve_snapshot(snapshot_arg: Path | None, domain_root: Path | None) -> Path:
    if snapshot_arg is None:
        domain_root = resolve_domain_root(domain_root)
        snapshot_arg = domain_root / "_LocalIndexes" / "_LATEST.md"
    path = snapshot_arg.resolve()
    if path.is_dir():
        if not (path / "catalog.sqlite").exists():
            raise FileNotFoundError(f"snapshot dir has no catalog.sqlite: {path}")
        return path
    if path.is_file() and path.name == "_LATEST.md":
        latest = parse_latest(path)
        candidate = (path.parent / latest).resolve()
        if not candidate.exists():
            raise FileNotFoundError(f"_LATEST.md points to missing snapshot: {candidate}")
        return candidate
    raise FileNotFoundError(f"snapshot not found or not recognized: {path}")


def parse_latest(path: Path) -> str:
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("Latest:"):
            latest = line.split(":", 1)[1].strip()
            if latest:
                return latest
    raise ValueError(f"no Latest line found in {path}")


def add(findings: list[dict], severity: str, code: str, message: str) -> None:
    findings.append({"severity": severity, "code": code, "message": message})


def check_exports(snapshot: Path, findings: list[dict]) -> None:
    for name in REQUIRED_EXPORTS:
        if not (snapshot / name).exists():
            add(findings, "BLOCKER", "MISSING_EXPORT", f"missing {name}")
    meta = json.loads((snapshot / "meta.json").read_text(encoding="utf-8"))
    if meta.get("schema_version") != SCHEMA_VERSION:
        add(
            findings,
            "BLOCKER",
            "SCHEMA_VERSION",
            f"expected {SCHEMA_VERSION}, found {meta.get('schema_version')}",
        )
    if meta.get("source_files_copied") is not False:
        add(findings, "BLOCKER", "SOURCE_COPY_POLICY", "meta does not assert source_files_copied=false")


def open_db(snapshot: Path) -> sqlite3.Connection:
    con = sqlite3.connect(str(snapshot / "catalog.sqlite"))
    con.row_factory = sqlite3.Row
    con.execute("PRAGMA foreign_keys = ON")
    return con


def check_schema(snapshot: Path, findings: list[dict]) -> None:
    db = snapshot / "catalog.sqlite"
    if not db.exists():
        add(findings, "BLOCKER", "MISSING_SQLITE", "missing catalog.sqlite")
        return
    con = open_db(snapshot)
    tables = {
        r["name"] for r in con.execute(
            "SELECT name FROM sqlite_master WHERE type='table'"
        ).fetchall()
    }
    for table in sorted(REQUIRED_TABLES - tables):
        add(findings, "BLOCKER", "MISSING_TABLE", f"missing table {table}")
    for row in con.execute("PRAGMA foreign_key_check").fetchall():
        add(findings, "BLOCKER", "FOREIGN_KEY", repr(dict(row)))
    con.close()


def check_counts(snapshot: Path, meta: dict, findings: list[dict]) -> None:
    con = open_db(snapshot)
    for table, meta_key in [
        ("artifacts", "artifact_count"),
        ("source_docs", "source_doc_count"),
        ("audit_state", "audit_state_count"),
        ("chunks", "chunk_count"),
    ]:
        count = con.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
        if count != int(meta.get(meta_key, -1)):
            add(findings, "BLOCKER", "COUNT_MISMATCH", f"{table}: db={count}, meta={meta.get(meta_key)}")
    for table, key in [
        ("artifacts", "artifact_id"),
        ("source_docs", "source_doc_id"),
        ("audit_state", "audit_id"),
        ("chunks", "chunk_id"),
    ]:
        total = con.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
        distinct = con.execute(f"SELECT COUNT(DISTINCT {key}) FROM {table}").fetchone()[0]
        if total != distinct:
            add(findings, "BLOCKER", "DUPLICATE_ID", f"{table}.{key}: {total} rows, {distinct} distinct")
    con.close()


def check_paths_and_hashes(
    snapshot: Path,
    domain_root: Path,
    repo_root: Path,
    skip_hash_verify: bool,
    findings: list[dict],
) -> None:
    con = open_db(snapshot)
    for row in con.execute("SELECT artifact_id, rel_path, sha256 FROM artifacts").fetchall():
        try:
            path = catalog_path(domain_root, row["rel_path"], repo_root)
        except Exception as exc:
            add(findings, "BLOCKER", "BAD_PATH_ROOT", f"{row['artifact_id']} cannot resolve {row['rel_path']}: {exc}")
            continue
        if not path.exists():
            add(findings, "BLOCKER", "MISSING_PATH", f"{row['artifact_id']} path missing: {row['rel_path']}")
            continue
        digest = row["sha256"]
        if len(digest) != 64 or any(c not in "0123456789abcdef" for c in digest):
            add(findings, "BLOCKER", "BAD_SHA256", f"{row['artifact_id']} has invalid sha256")
            continue
        if not skip_hash_verify:
            actual = sha256_file(path)
            if actual != digest:
                add(findings, "BLOCKER", "HASH_MISMATCH", f"{row['artifact_id']} hash mismatch: {row['rel_path']}")
    con.close()


def check_chunks(snapshot: Path, findings: list[dict]) -> None:
    con = open_db(snapshot)
    for row in con.execute("SELECT chunk_id, text, text_hash FROM chunks").fetchall():
        if text_hash(row["text"]) != row["text_hash"]:
            add(findings, "BLOCKER", "TEXT_HASH_MISMATCH", f"{row['chunk_id']} text_hash mismatch")
    stale = con.execute(
        """
        SELECT c.chunk_id FROM chunks c
        LEFT JOIN artifacts a ON a.artifact_id = c.artifact_id
        WHERE a.artifact_id IS NULL
        """
    ).fetchall()
    for row in stale:
        add(findings, "BLOCKER", "STALE_CHUNK", f"{row['chunk_id']} references missing artifact")
    con.close()


def check_audit_surfaces(snapshot: Path, domain_root: Path, findings: list[dict]) -> None:
    con = open_db(snapshot)
    expected = ["equations.html", "figures.html", "tables.html", "images.html"]
    for src in con.execute(
        """
        SELECT source_doc_id, audit_dir_rel_path
        FROM source_docs
        WHERE archive_state='ACTIVE' AND audit_dir_rel_path IS NOT NULL
        """
    ).fetchall():
        if is_repo_rel_path(src["audit_dir_rel_path"] or ""):
            continue
        audit_dir = domain_root / src["audit_dir_rel_path"]
        for name in expected:
            if not (audit_dir / name).exists():
                add(
                    findings,
                    "WARNING",
                    "MISSING_AUDIT_SURFACE",
                    f"{src['source_doc_id']} missing {src['audit_dir_rel_path']}/{name}",
                )
    con.close()


if __name__ == "__main__":
    raise SystemExit(main())
