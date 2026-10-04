#!/usr/bin/env python3
"""Reach check for a proposed register row (DEL-10-04 DA §5 step 1; R23-2).

Design prototype, not product code. Read-only. Reads the accepted DAG named by
`_DAG/_LATEST.md` (admitted `DependencyEdges.csv` plus held `CandidateEdges.csv`),
with arcs read consumer -> supplier (a DOWNSTREAM row's endpoints are reversed).

  python3 dag_reach.py CONSUMER SUPPLIER   # e.g. DEL-02-04 DEL-10-03 (reads _LATEST.md's version)
  python3 dag_reach.py --dag DAG-004 CONSUMER SUPPLIER   # a named version
  python3 dag_reach.py --self-test         # always DAG-004, whose facts the cases record

The script prints the DAG version it read (R23-51). This is the project's
reach script (R23-51).

A proposed row C -> S (C consumes S's contribution) forms a cycle exactly when
S already reaches C over both layers. Exit 0: no cycle. Exit 2: SCC-forming
(a departure for its owner and `scc-resolution-case`). Exit 1: input error.
An arc C -> S that already exists is reported as such (no new arc).
"""
import argparse
import csv
import pathlib
import re
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent


SELF_TEST_VERSION = "DAG-004"


def dag_root() -> pathlib.Path:
    top = pathlib.Path(subprocess.run(["git", "-C", str(HERE), "rev-parse", "--show-toplevel"],
                                      capture_output=True, text=True, check=True).stdout.strip())
    return top / "projects/chirality-app-v4/execution/_DAG"


def dag_dir(version=None):
    """(directory, how it was chosen)."""
    root = dag_root()
    if version:
        return root / version, "named with --dag"
    latest = re.search(r"^Latest:\s*(\S+)", (root / "_LATEST.md").read_text(), re.M).group(1)
    return root / latest, "from _DAG/_LATEST.md"


def arcs(path: pathlib.Path) -> set:
    out = set()
    for r in csv.DictReader(open(path)):
        a, b = r["FromDeliverableID"], r["TargetDeliverableID"]
        if not (b or "").startswith("DEL-"):
            continue
        if r["Direction"] == "DOWNSTREAM":
            a, b = b, a
        out.add((a, b))
    return out


def reach(edges: set, start: str) -> set:
    seen, stack = set(), [start]
    while stack:
        x = stack.pop()
        for a, b in edges:
            if a == x and b not in seen:
                seen.add(b)
                stack.append(b)
    return seen


def verdict(edges: set, c: str, s: str) -> int:
    if c == s:
        print(f"{c} -> {s}: a self-arc is a cycle")
        return 2
    if (c, s) in edges:
        print(f"{c} -> {s}: this arc already exists in the accepted DAG (no new arc)")
        return 0
    if c in reach(edges, s):
        print(f"{c} -> {s}: SCC-FORMING. {s} already reaches {c} over the admitted and held layers")
        return 2
    print(f"{c} -> {s}: no cycle. {s} does not reach {c}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("consumer", nargs="?")
    ap.add_argument("supplier", nargs="?")
    ap.add_argument("--self-test", action="store_true")
    ap.add_argument("--dag", help="a DAG version folder name, for example DAG-004")
    a = ap.parse_args()
    if a.self_test:
        d, how = dag_dir(SELF_TEST_VERSION)
        how = f"pinned for the self-test; its cases record {SELF_TEST_VERSION} facts"
        if not (d / "DependencyEdges.csv").is_file():
            print(f"NOTICE: {SELF_TEST_VERSION} not found; self-test skipped")
            return 0
    else:
        d, how = dag_dir(a.dag)
        if not (d / "DependencyEdges.csv").is_file():
            print(f"DAG version {d.name} not found")
            return 1
    edges = arcs(d / "DependencyEdges.csv") | arcs(d / "CandidateEdges.csv")
    print(f"DAG read: {d.name} ({how}); arcs over both layers: {len(edges)}")
    if a.self_test:
        # Facts read from DAG-004 by O-E (S2-E survey; DA §5): DEL-10-03 consumes DEL-02-04
        # (admitted); DEL-06-01 does not reach PKG-10; DEL-10-02 <-> DEL-10-04 is held SCC-005.
        cases = [("DEL-02-04", "DEL-10-03", 2), ("DEL-06-01", "DEL-10-02", 0),
                 ("DEL-10-03", "DEL-02-04", 0), ("DEL-10-01", "DEL-10-01", 2),
                 ("DEL-10-01", "DEL-10-04", 2)]
        bad = 0
        for c, s, want in cases:
            got = verdict(edges, c, s)
            bad += got != want
            print(f"  expected {want}, got {got}{'' if got == want else '  <-- WRONG'}")
        return 0 if not bad else 1
    if not (a.consumer and a.supplier):
        ap.error("give CONSUMER SUPPLIER, or --self-test")
    return verdict(edges, a.consumer, a.supplier)


if __name__ == "__main__":
    sys.exit(main())
