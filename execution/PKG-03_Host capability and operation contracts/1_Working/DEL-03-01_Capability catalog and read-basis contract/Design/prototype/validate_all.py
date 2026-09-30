#!/usr/bin/env python3
"""Validate the PKG-03 PROPOSED schemas and their example instances.

Prototype only (R12-3). Finds every `*.schema.json` in the Design folders of
DEL-03-01, DEL-03-02 and DEL-03-03, checks that each uses only the keyword
subset of schema_subset.py, validates each `<name>.example-valid*.json`
(must pass) and `<name>.example-invalid*.json` (must fail, and the errors are
printed), and, with --run DIR, validates every host document SH-1 produced in
that run against the schema it claims to follow.
"""

import argparse
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from schema_subset import check_subset, load_registry, validate  # noqa: E402

WORKING = HERE.parents[2]
DESIGNS = sorted(p / "Design" for p in WORKING.glob("DEL-03-0[123]_*"))


def schema_files():
    return sorted(f for d in DESIGNS for f in d.glob("*.schema.json"))


def by_id(schemas):
    return {s["$id"]: s for s in schemas.values()}


def doc_schema(doc):
    if "entries" in doc:
        return "urn:chirality:app-v4:proposed:catalog"
    if "kind" in doc:
        return "urn:chirality:app-v4:proposed:proposal-state"
    if "outcome" in doc:
        return "urn:chirality:app-v4:proposed:read-result"
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", help="an SH-1 run directory (run_fixture.py --out)")
    a = ap.parse_args()
    files = schema_files()
    reg, schemas = load_registry(files)
    ids = by_id(schemas)
    bad = 0
    print(f"Schemas found: {len(files)}")
    for f in files:
        s = schemas[str(f)]
        extra = check_subset(s)
        print(f"  {f.parent.parent.name[:9]} {f.name:40} subset {'ok' if not extra else 'OUTSIDE: ' + ', '.join(extra)}")
        bad += len(extra)
        stem = f.name[: -len(".schema.json")]
        for ex in sorted(f.parent.glob(f"{stem}.example-*.json")):
            inst = json.loads(ex.read_text())
            errs = validate(inst, s, reg)
            want_valid = ".example-valid" in ex.name
            ok = (not errs) if want_valid else bool(errs)
            bad += 0 if ok else 1
            print(f"    {'PASS' if ok else 'FAIL'} {ex.name}: {'valid' if not errs else 'invalid'}"
                  + ("" if not errs else f" -> {errs[0]}" + (f" (+{len(errs) - 1} more)" if len(errs) > 1 else "")))
    if a.run:
        run = Path(a.run)
        n = 0
        for line in (run / "host_docs.jsonl").read_text().splitlines():
            rec = json.loads(line)
            doc = rec["doc"]
            targets = []
            if "events" in doc:
                targets = [(e, "urn:chirality:app-v4:proposed:edition-change-event") for e in doc["events"]]
            else:
                targets = [(doc, doc_schema(doc))]
            for inst, sid in targets:
                n += 1
                errs = validate(inst, ids[sid], reg) if sid else ["no schema claimed"]
                if errs:
                    bad += 1
                    print(f"  FAIL host doc {rec['run']}/{rec['step']}/{rec['path']} vs {sid}: {errs[:3]}")
        print(f"Host documents from {run.name}: {n} validated")
        m = 0
        for line in (run / "native_items.jsonl").read_text().splitlines():
            rec = json.loads(line)
            item = rec["item"]
            req = None
            if item.get("type") == "mcpToolCall" and item.get("tool") == "submit-proposal":
                req = item["arguments"]["proposal"]
            elif item.get("type") == "commandExecution" and item["command"].startswith("sh1 cli submit"):
                req = json.loads(item["command"].split("--json ", 1)[1].strip("'"))
            if req is not None:
                m += 1
                errs = validate(req, ids["urn:chirality:app-v4:proposed:proposal"], reg)
                if errs:
                    bad += 1
                    print(f"  FAIL request {rec['run']}/{rec['step']}: {errs[:3]}")
        print(f"Change requests from {run.name}: {m} validated against proposal.schema.json")
    print("RESULT:", "all checks passed" if bad == 0 else f"{bad} failure(s)")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
