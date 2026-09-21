#!/usr/bin/env python3
"""Check whether a source-database snapshot is fresh against the live source tree.

Compares each recorded artifact's SHA-256 (and presence) against the current live
source files and reports changed / missing / unchanged counts plus a FRESH|STALE
verdict, WITHOUT rebuilding the snapshot (honours the "no silent refresh" research
invariant). This answers "is the retrieval evidence still current?" before that
evidence enters authority.

Usage:
  python3 tools/source_catalog/check_snapshot_freshness.py \
      --snapshot domains/chirality-app-dev/_LocalIndexes/_LATEST.md \
      --json

Inputs:
  --snapshot          Snapshot directory or _LATEST.md pointer.
  --domain-root       Domain root override. Defaults to meta.json domain_root.
  --repo-root         Repo root for @repo/ manifest-backed paths. Defaults to meta.json repo_root.
  --json              Emit JSON.
  --csv PATH          Also write a per-artifact drift CSV.
  --skip-hash-verify  Compare presence only (skip re-hashing); fast path for large corpora.

Outputs:
  Human or JSON drift report + FRESH|STALE verdict.
  Exit 0 FRESH, 1 STALE (drift), 2 invalid invocation / unreadable snapshot.

Scope: covers drift of indexed artifacts (changed/missing). Coverage of newly added,
not-yet-indexed source files is out of scope (rebuild to index new material).
"""
from __future__ import annotations

import argparse
import csv as csvmod
import json
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "tools" / "source_catalog"))
from source_database import (  # noqa: E402
    DEFAULT_DOMAIN_ROOT,
    catalog_path,
    resolve_domain_root,
    resolve_snapshot_path,
    sha256_file,
)


def open_db(snapshot: Path) -> sqlite3.Connection:
    con = sqlite3.connect(str(snapshot / "catalog.sqlite"))
    con.row_factory = sqlite3.Row
    return con


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument("--snapshot", type=Path)
    ap.add_argument("--domain-root", type=Path, default=DEFAULT_DOMAIN_ROOT)
    ap.add_argument("--repo-root", type=Path)
    ap.add_argument("--json", action="store_true", dest="emit_json")
    ap.add_argument("--csv", type=Path)
    ap.add_argument("--skip-hash-verify", action="store_true")
    args = ap.parse_args()

    try:
        snapshot = resolve_snapshot_path(args.snapshot, args.domain_root)
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

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

    con = open_db(snapshot)
    try:
        artifacts = con.execute(
            "SELECT artifact_id, rel_path, sha256 FROM artifacts"
        ).fetchall()
    finally:
        con.close()

    changed: list[str] = []
    missing: list[str] = []
    unchanged = 0
    rows: list[dict] = []
    for r in artifacts:
        rel = r["rel_path"]
        try:
            path = catalog_path(domain_root, rel, repo_root)
        except Exception as exc:
            missing.append(r["artifact_id"])
            rows.append({"artifact_id": r["artifact_id"], "rel_path": rel,
                         "status": "UNRESOLVABLE", "detail": str(exc)})
            continue
        if not path.exists():
            missing.append(r["artifact_id"])
            rows.append({"artifact_id": r["artifact_id"], "rel_path": rel,
                         "status": "MISSING", "detail": str(path)})
            continue
        if args.skip_hash_verify:
            unchanged += 1
            continue
        if sha256_file(path) != r["sha256"]:
            changed.append(r["artifact_id"])
            rows.append({"artifact_id": r["artifact_id"], "rel_path": rel,
                         "status": "CHANGED", "detail": ""})
        else:
            unchanged += 1

    counts = {
        "unchanged": unchanged,
        "changed": len(changed),
        "missing": len(missing),
        "total_recorded": len(artifacts),
    }
    drift = counts["changed"] + counts["missing"]
    verdict = "FRESH" if drift == 0 else "STALE"

    if args.csv:
        args.csv.parent.mkdir(parents=True, exist_ok=True)
        with args.csv.open("w", encoding="utf-8", newline="") as f:
            writer = csvmod.DictWriter(
                f, fieldnames=["artifact_id", "rel_path", "status", "detail"]
            )
            writer.writeheader()
            writer.writerows(rows)

    payload = {
        "snapshot": str(snapshot),
        "snapshot_name": snapshot.name,
        "build_utc": meta.get("build_utc"),
        "checked_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "domain_root": str(domain_root),
        "skip_hash_verify": bool(args.skip_hash_verify),
        "counts": counts,
        "verdict": verdict,
        "reason": "" if verdict == "FRESH" else "CONTENT_DRIFT",
        "changed": changed,
        "missing": missing,
    }
    if args.emit_json:
        print(json.dumps(payload, indent=2))
    else:
        print(
            f"{verdict}: {snapshot.name} (build_utc={meta.get('build_utc')}, "
            f"{counts['changed']} changed / {counts['missing']} missing / "
            f"{counts['unchanged']} unchanged of {counts['total_recorded']})"
        )
    return 0 if verdict == "FRESH" else 1


if __name__ == "__main__":
    raise SystemExit(main())
