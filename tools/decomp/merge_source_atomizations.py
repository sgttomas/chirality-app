#!/usr/bin/env python3
"""Two-stage merge of per-unit atomization CSVs into a domain ledger.

Stage 1 (`per-source`):
  Walk a source's per-unit dispatch CSVs (one per UNIT-<prefix>-NNNN) in
  skeleton order, assign final stable IDs (HBA-<prefix>-NNNNN), validate
  LocalSeq monotonicity within each unit, dedupe by ContentHash, and write
  a per-source `<book>_atomic_units.csv`.

Stage 2 (`cross-source`):
  Concatenate per-source ledgers into one `Atomic_Domain_Ledger.csv`, verify
  no ID-prefix collisions, surface unresolved cross-source `Corrects`
  references, and add SourceDoc / SourcePrefix columns when not present.

Per-unit CSV input schema (produced by `domain-source-atomize`):
  LocalSeq, UnitStatement, SourceRef, ContentHash, InOutStatus,
  SectionID, DispatchUnitID, Corrects, Notes

Optional columns are passed through verbatim. Empty `UnitStatement` rows
fail-fast.

Stable ID format: HBA-<SOURCE_PREFIX>-NNNNN (5 digits, left-padded).
Final IDs are assigned in document order (dispatch units walked in plan
order; rows within a unit walked in LocalSeq order).

Usage:
  # Stage 1 — one source
  python3 tools/decomp/merge_source_atomizations.py per-source \\
      --dispatch-plan <book>_dispatch_plan.json \\
      --unit-csv-glob '<work>/<book>_dispatch_*_atoms.csv' \\
      --source-prefix PSE \\
      --source-name Pipe-Stress-Engineering \\
      --output <book>_atomic_units.csv

  # Stage 2 — cross-source merge
  python3 tools/decomp/merge_source_atomizations.py cross-source \\
      --per-source <book1>_atomic_units.csv \\
      --per-source <book2>_atomic_units.csv \\
      --output Atomic_Domain_Ledger.csv
"""
from __future__ import annotations

import argparse
import csv
import glob
import hashlib
import json
import sys
from pathlib import Path

REQUIRED_COLUMNS = [
    "LocalSeq",
    "UnitStatement",
    "SourceRef",
    "ContentHash",
    "InOutStatus",
    "SectionID",
    "DispatchUnitID",
]
OPTIONAL_COLUMNS = ["Corrects", "Notes"]
FINAL_COLUMNS_PER_SOURCE = [
    "AtomicUnitID",
    "LocalSeq",
    "UnitStatement",
    "SourceRef",
    "ContentHash",
    "InOutStatus",
    "SectionID",
    "DispatchUnitID",
    "Corrects",
    "Notes",
]
FINAL_COLUMNS_CROSS = [
    "AtomicUnitID",
    "SourceDoc",
    "SourcePrefix",
    "LocalSeq",
    "UnitStatement",
    "SourceRef",
    "ContentHash",
    "InOutStatus",
    "SectionID",
    "DispatchUnitID",
    "Corrects",
    "Notes",
]


def fail(msg: str, code: int = 2) -> int:
    print(f"ERROR: {msg}", file=sys.stderr)
    return code


def sha1_12(text: str) -> str:
    return hashlib.sha1(text.strip().encode("utf-8")).hexdigest()[:12]


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="stage", required=True)

    a = sub.add_parser("per-source", help="Merge per-unit CSVs for one source.")
    a.add_argument("--dispatch-plan", required=True, type=Path)
    a.add_argument("--unit-csv-glob", required=True,
                   help="Glob for the per-unit atom CSVs (must include unit_id substring)")
    a.add_argument("--source-prefix", required=True)
    a.add_argument("--source-name", required=True)
    a.add_argument("--output", required=True, type=Path)
    a.add_argument("--strict-coverage", action="store_true",
                   help="Fail if any dispatch unit lacks a per-unit CSV.")

    b = sub.add_parser("cross-source", help="Merge per-source ledgers into the domain ledger.")
    b.add_argument("--per-source", required=True, action="append", type=Path,
                   help="Repeat for each per-source ledger.")
    b.add_argument("--output", required=True, type=Path)

    return p.parse_args()


def load_csv_rows(path: Path) -> list[dict]:
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def validate_per_unit_rows(rows: list[dict], path: Path) -> None:
    for col in REQUIRED_COLUMNS:
        if col not in (rows[0] if rows else {}):
            raise RuntimeError(f"{path}: missing required column {col}")
    prev = 0
    for i, r in enumerate(rows, start=1):
        if not r.get("UnitStatement", "").strip():
            raise RuntimeError(f"{path} row {i}: empty UnitStatement")
        if not r.get("ContentHash", "").strip():
            raise RuntimeError(f"{path} row {i}: empty ContentHash")
        try:
            seq = int(r["LocalSeq"])
        except ValueError as exc:
            raise RuntimeError(f"{path} row {i}: LocalSeq not int: {r['LocalSeq']}") from exc
        if seq <= prev:
            raise RuntimeError(f"{path} row {i}: LocalSeq {seq} not strictly increasing (prev {prev})")
        prev = seq
        # Defensive: ContentHash recomputable from UnitStatement
        expected = sha1_12(r["UnitStatement"])
        if r["ContentHash"] != expected:
            raise RuntimeError(
                f"{path} row {i}: ContentHash mismatch — declared {r['ContentHash']!r}, "
                f"expected sha1(UnitStatement)[:12] = {expected!r}"
            )


def merge_per_source(args: argparse.Namespace) -> int:
    plan = json.loads(args.dispatch_plan.read_text(encoding="utf-8"))
    plan_units = [u["unit_id"] for u in plan.get("units", [])]
    unit_csvs = sorted(glob.glob(args.unit_csv_glob))
    csv_by_unit: dict[str, Path] = {}
    for path in unit_csvs:
        p = Path(path)
        # Map filename → unit_id by substring presence
        match = next((uid for uid in plan_units if uid in p.name), None)
        if match:
            csv_by_unit[match] = p

    missing = [uid for uid in plan_units if uid not in csv_by_unit]
    if missing and args.strict_coverage:
        return fail(
            f"missing per-unit CSVs for {len(missing)} dispatch units: "
            f"{', '.join(missing[:5])}{'...' if len(missing) > 5 else ''}"
        )

    all_rows: list[dict] = []
    seen_hashes: set[str] = set()
    counter = 0
    for uid in plan_units:
        path = csv_by_unit.get(uid)
        if path is None:
            continue
        rows = load_csv_rows(path)
        if not rows:
            continue
        try:
            validate_per_unit_rows(rows, path)
        except RuntimeError as exc:
            return fail(str(exc))
        for r in rows:
            ch = r["ContentHash"]
            if ch in seen_hashes:
                continue
            seen_hashes.add(ch)
            counter += 1
            atomic_id = f"HBA-{args.source_prefix}-{counter:05d}"
            r_out = {col: r.get(col, "") for col in FINAL_COLUMNS_PER_SOURCE}
            r_out["AtomicUnitID"] = atomic_id
            r_out["DispatchUnitID"] = uid
            all_rows.append(r_out)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FINAL_COLUMNS_PER_SOURCE)
        writer.writeheader()
        for r in all_rows:
            writer.writerow(r)

    print(
        f"source={args.source_name} prefix={args.source_prefix} "
        f"units_with_csvs={len(csv_by_unit)}/{len(plan_units)} "
        f"rows={len(all_rows)} output={args.output.name} "
        f"missing_units={len(missing)}"
    )
    return 0


def merge_cross_source(args: argparse.Namespace) -> int:
    all_rows: list[dict] = []
    prefix_seen: dict[str, Path] = {}
    id_to_source: dict[str, str] = {}
    for src_path in args.per_source:
        if not src_path.exists():
            return fail(f"missing per-source ledger: {src_path}")
        rows = load_csv_rows(src_path)
        if not rows:
            print(f"  warning: {src_path} has no rows", file=sys.stderr)
            continue
        first_id = rows[0]["AtomicUnitID"]
        try:
            _, prefix, _ = first_id.split("-", 2)
        except ValueError:
            return fail(f"{src_path}: malformed AtomicUnitID {first_id!r}")
        if prefix in prefix_seen and prefix_seen[prefix] != src_path:
            return fail(
                f"prefix collision: {prefix} appears in {prefix_seen[prefix]} and {src_path}"
            )
        prefix_seen[prefix] = src_path
        source_doc = src_path.stem.replace("_atomic_units", "")
        for r in rows:
            aid = r["AtomicUnitID"]
            if aid in id_to_source:
                return fail(f"duplicate AtomicUnitID {aid} from {src_path} and {id_to_source[aid]}")
            id_to_source[aid] = str(src_path)
            r_out = {col: r.get(col, "") for col in FINAL_COLUMNS_CROSS}
            r_out["AtomicUnitID"] = aid
            r_out["SourceDoc"] = source_doc
            r_out["SourcePrefix"] = prefix
            all_rows.append(r_out)

    # Cross-source `Corrects` resolution
    unresolved: list[tuple[str, str]] = []
    for r in all_rows:
        cor = (r.get("Corrects") or "").strip()
        if not cor:
            continue
        for ref in [x.strip() for x in cor.split(";") if x.strip()]:
            if ref not in id_to_source:
                unresolved.append((r["AtomicUnitID"], ref))
    if unresolved:
        print(
            f"  warning: {len(unresolved)} unresolved cross-source Corrects references "
            f"(first 5): {unresolved[:5]}",
            file=sys.stderr,
        )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FINAL_COLUMNS_CROSS)
        writer.writeheader()
        for r in all_rows:
            writer.writerow(r)

    print(
        f"sources={len(args.per_source)} prefixes={sorted(prefix_seen.keys())} "
        f"rows={len(all_rows)} unresolved_corrects={len(unresolved)} "
        f"output={args.output.name}"
    )
    return 0


def main() -> int:
    args = parse_args()
    if args.stage == "per-source":
        return merge_per_source(args)
    if args.stage == "cross-source":
        return merge_cross_source(args)
    return fail("unknown stage")


if __name__ == "__main__":
    raise SystemExit(main())
