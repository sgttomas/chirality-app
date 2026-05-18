#!/usr/bin/env python3
"""
KA coverage audit — diagnostic preflight for KTY/KA authoring dispatch.

Reads the merged ledger and the KA file tree, reports per-KTY:
  - Pool size (HBAs available, by KnowledgeTypeID(s) membership)
  - Citation count (unique HBAs cited across all KAs under the KTY)
  - Per-KA word counts and citation counts
  - Missing-vs-lean classification

Output is informational. NOT a coverage target. Used as a preflight
before each KA dispatch to surface MISSING/LEAN/WELL_COVERED defects
for human ruling. The skill's "Relationship to the HBA / atomic-ledger
layer" section in skills/domain-documents/SKILL.md describes the
intent (KA-as-contextualizer; coverage% is diagnostic, not target).

Usage:
  ka_coverage_audit.py <KTY-ID>          # single-KTY markdown report
  ka_coverage_audit.py --all              # all KTYs, sorted by class
  ka_coverage_audit.py --json <KTY-ID>    # JSON for programmatic use
  ka_coverage_audit.py --all --json       # JSON, all KTYs
"""

import argparse
import csv
import glob
import json
import os
import re
import sys
from collections import defaultdict

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
LEDGER_CSV = os.path.join(
    REPO_ROOT,
    "domains/piping-design/_Decomposition/Atomic_Domain_Ledger.csv",
)
KA_GLOB = os.path.join(
    REPO_ROOT, "domains/piping-design/CAT-*/1_Working/KTY-*/KA-*.md"
)

STUB_WORDS = 200
STUB_CITATIONS = 3
EMPTY_WORDS = 50

KTY_RE = re.compile(r"KTY-\d+-\d+")
HBA_RE = re.compile(r"HBA-\d{6}")


def load_pool_by_kty():
    """Map KTY-ID → set of HBA-IDs assigned to it via KnowledgeTypeID(s)."""
    pool = defaultdict(set)
    with open(LEDGER_CSV) as f:
        reader = csv.DictReader(f)
        for row in reader:
            ktys = row.get("KnowledgeTypeID(s)", "")
            for kty in KTY_RE.findall(ktys):
                pool[kty].add(row["AtomicUnitID"])
    return pool


def scan_ka_files():
    """Map KTY-ID → list of {path, wordcount, citations:set, classification}."""
    ka_by_kty = defaultdict(list)
    for ka_path in sorted(glob.glob(KA_GLOB)):
        m = KTY_RE.search(ka_path)
        if not m:
            continue
        kty = m.group(0)
        with open(ka_path) as f:
            text = f.read()
        wordcount = len(text.split())
        citations = set(HBA_RE.findall(text))
        if wordcount < EMPTY_WORDS and not citations:
            status = "empty"
        elif wordcount < STUB_WORDS or len(citations) < STUB_CITATIONS:
            status = "stub"
        else:
            status = "substantive"
        ka_by_kty[kty].append(
            {
                "path": os.path.relpath(ka_path, REPO_ROOT),
                "wordcount": wordcount,
                "citations": citations,
                "status": status,
            }
        )
    return ka_by_kty


def classify_kty(kas, pool_size, cited):
    """MISSING | LEAN_BUT_SUBSTANTIVE | WELL_COVERED."""
    if not kas:
        return "MISSING"
    if all(k["status"] in ("empty", "stub") for k in kas):
        return "MISSING"
    coverage_pct = 100 * len(cited) / pool_size if pool_size else 0
    if coverage_pct >= 50:
        return "WELL_COVERED"
    return "LEAN_BUT_SUBSTANTIVE"


def audit_kty(kty, pool, ka_by_kty):
    pool_set = pool.get(kty, set())
    kas = ka_by_kty.get(kty, [])
    cited = set()
    for k in kas:
        cited |= k["citations"]
    classification = classify_kty(kas, len(pool_set), cited)
    return {
        "kty": kty,
        "pool_size": len(pool_set),
        "citation_count": len(cited),
        "ka_count": len(kas),
        "kas": [
            {
                "path": k["path"],
                "wordcount": k["wordcount"],
                "citations": len(k["citations"]),
                "status": k["status"],
            }
            for k in kas
        ],
        "classification": classification,
    }


def render_markdown(report):
    pool = report["pool_size"]
    cited = report["citation_count"]
    pct = 100 * cited / pool if pool else 0
    lines = [
        f"## {report['kty']}",
        "",
        f"  Pool size:           {pool} HBAs available (from ledger)",
        f"  Citation count:      {cited} unique HBAs cited across {report['ka_count']} KAs",
        f"  Citation coverage:   {pct:.1f}% (informational only — not a target)",
        f"  Classification:      **{report['classification']}**",
        "",
        "  KA file inventory:",
    ]
    if not report["kas"]:
        lines.append("    (none)")
    else:
        for k in report["kas"]:
            name = os.path.basename(k["path"])
            lines.append(
                f"    {name}  {k['wordcount']:>5} words, {k['citations']:>3} HBAs, status={k['status']}"
            )
    lines.append("")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "kty", nargs="?", help="KTY ID (e.g., KTY-08-05). Required unless --all."
    )
    parser.add_argument("--all", action="store_true", help="Audit all KTYs.")
    parser.add_argument("--json", action="store_true", help="JSON output.")
    args = parser.parse_args()

    if not args.all and not args.kty:
        parser.error("KTY ID required unless --all is specified.")

    pool = load_pool_by_kty()
    ka_by_kty = scan_ka_files()
    all_ktys = sorted(set(list(pool.keys()) + list(ka_by_kty.keys())))

    targets = all_ktys if args.all else [args.kty]
    reports = [audit_kty(k, pool, ka_by_kty) for k in targets]

    if args.json:
        print(json.dumps(reports if args.all else reports[0], indent=2))
        return

    if args.all:
        # Sort: MISSING first, then LEAN_BUT_SUBSTANTIVE, then WELL_COVERED
        order = {"MISSING": 0, "LEAN_BUT_SUBSTANTIVE": 1, "WELL_COVERED": 2}
        reports.sort(key=lambda r: (order[r["classification"]], r["kty"]))
        # Summary header
        counts = defaultdict(int)
        for r in reports:
            counts[r["classification"]] += 1
        print("# KA Coverage Audit — All KTYs\n")
        print(f"Total KTYs: {len(reports)}")
        for cls in ("MISSING", "LEAN_BUT_SUBSTANTIVE", "WELL_COVERED"):
            print(f"  {cls}: {counts[cls]}")
        print()
        print(
            "Coverage % is informational. Classification is based on KA file existence "
            "and substance (not on citation %)."
        )
        print()
    for r in reports:
        print(render_markdown(r))


if __name__ == "__main__":
    main()
