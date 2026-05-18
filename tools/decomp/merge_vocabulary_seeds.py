#!/usr/bin/env python3
"""Consolidate per-source vocabulary seed CSVs into a single Vocabulary_Map.csv.

Each source's `<book>_vocabulary_seed.csv` is produced by the
`domain-source-atomize` skill alongside the atom ledger. Rows are
candidate canonical terms with optional definition and synonyms drawn
from one source's text. This tool unions those rows across all sources
into a single Vocabulary_Map for persona review at Gate 2.

Per-source seed schema (minimum columns):
  CandidateTerm, Synonyms, Definition, SourceRefs, Notes

Output schema:
  CanonicalTerm, Synonyms, Definition, SourceDocs, SourceRefs, Notes, SourceCount

Grouping is case-insensitive on CandidateTerm. The first non-empty
casing wins for CanonicalTerm display. Synonyms/SourceRefs/Notes
columns are unioned (semicolon-separated, deduped, deterministic order).
SourceDocs is the union of source documents that surfaced the term.
SourceCount is the integer count of sources where the term appeared
(useful for prioritizing review).

Usage:
  python3 tools/decomp/merge_vocabulary_seeds.py \\
      --seed <book1>_vocabulary_seed.csv --source-doc <book1> \\
      --seed <book2>_vocabulary_seed.csv --source-doc <book2> \\
      --output Vocabulary_Map.csv
"""
from __future__ import annotations

import argparse
import csv
import sys
from collections import OrderedDict
from pathlib import Path

REQUIRED_COLUMNS = ["CandidateTerm"]
OPTIONAL_COLUMNS = ["Synonyms", "Definition", "SourceRefs", "Notes"]
FINAL_COLUMNS = [
    "CanonicalTerm",
    "Synonyms",
    "Definition",
    "SourceDocs",
    "SourceRefs",
    "Notes",
    "SourceCount",
]


def fail(msg: str, code: int = 2) -> int:
    print(f"ERROR: {msg}", file=sys.stderr)
    return code


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--seed", action="append", type=Path, required=True,
                   help="Per-source vocabulary seed CSV (repeat per source)")
    p.add_argument("--source-doc", action="append", required=True,
                   help="Source document label paired with each --seed (in order)")
    p.add_argument("--output", required=True, type=Path)
    return p.parse_args()


def split_semis(value: str) -> list[str]:
    if not value:
        return []
    return [v.strip() for v in value.split(";") if v.strip()]


def join_semis(items: list[str]) -> str:
    return ";".join(items)


def union_ordered(existing: list[str], new: list[str]) -> list[str]:
    seen = set(existing)
    out = list(existing)
    for v in new:
        if v and v not in seen:
            seen.add(v)
            out.append(v)
    return out


def main() -> int:
    args = parse_args()
    if len(args.seed) != len(args.source_doc):
        return fail("each --seed must be paired with one --source-doc (same order)")

    merged: "OrderedDict[str, dict]" = OrderedDict()

    for seed_path, source_doc in zip(args.seed, args.source_doc):
        if not seed_path.exists():
            return fail(f"missing seed CSV: {seed_path}")
        with seed_path.open("r", encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            if not reader.fieldnames or "CandidateTerm" not in reader.fieldnames:
                return fail(f"{seed_path}: missing required CandidateTerm column")
            for row in reader:
                term = (row.get("CandidateTerm") or "").strip()
                if not term:
                    continue
                key = term.lower()
                entry = merged.get(key)
                if entry is None:
                    entry = {
                        "CanonicalTerm": term,
                        "Synonyms": [],
                        "Definition": [],
                        "SourceDocs": [],
                        "SourceRefs": [],
                        "Notes": [],
                        "SourceCount": 0,
                    }
                    merged[key] = entry
                entry["Synonyms"] = union_ordered(
                    entry["Synonyms"], split_semis(row.get("Synonyms", ""))
                )
                defn = (row.get("Definition") or "").strip()
                if defn:
                    entry["Definition"] = union_ordered(entry["Definition"], [defn])
                if source_doc not in entry["SourceDocs"]:
                    entry["SourceDocs"].append(source_doc)
                    entry["SourceCount"] += 1
                entry["SourceRefs"] = union_ordered(
                    entry["SourceRefs"], split_semis(row.get("SourceRefs", ""))
                )
                note = (row.get("Notes") or "").strip()
                if note:
                    entry["Notes"] = union_ordered(entry["Notes"], [note])

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FINAL_COLUMNS)
        writer.writeheader()
        for entry in merged.values():
            writer.writerow({
                "CanonicalTerm": entry["CanonicalTerm"],
                "Synonyms": join_semis(entry["Synonyms"]),
                "Definition": join_semis(entry["Definition"]),
                "SourceDocs": join_semis(entry["SourceDocs"]),
                "SourceRefs": join_semis(entry["SourceRefs"]),
                "Notes": join_semis(entry["Notes"]),
                "SourceCount": entry["SourceCount"],
            })

    multi_source = sum(1 for e in merged.values() if e["SourceCount"] > 1)
    print(
        f"sources={len(args.seed)} terms={len(merged)} "
        f"multi_source={multi_source} output={args.output.name}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
