#!/usr/bin/env python3
"""Validate the PKG-03 PROPOSED schemas and their example instances.

Prototype only (R12-3). Finds every `*.schema.json` in the Design folders of
DEL-03-01, DEL-03-02 and DEL-03-03, checks that each uses only the keyword
subset of schema_subset.py, validates each `<name>.example-valid*.json`
(must pass) and `<name>.example-invalid*.json` (must fail, and the errors are
printed), and, with --run DIR, validates every host document SH-1 produced in
that run against the schema it claims to follow.

Beyond the keyword subset, catalog instances are also checked against the
conformance rules a JSON Schema cannot state (C-v0.8 §3.5): CX-1, an
external-contact declaration of form 'from_argument' names an argument of the
same entry. An invalid example passes this script when the schema or a
conformance rule rejects it. Since the RP-2 repair the script also applies
the three mutations of V18-3 R-7 to `catalog.example-valid-2.json`; each must
be rejected.
"""

import argparse
import copy
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from schema_subset import check_subset, load_registry, validate  # noqa: E402

WORKING = HERE.parents[2]
DESIGNS = sorted(p / "Design" for p in WORKING.glob("DEL-03-0[123]"))


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


CATALOG_ID = "urn:chirality:app-v4:proposed:catalog"


def conformance(inst, sid):
    """Conformance rules beyond the schema (C §3.5). Returns error strings."""
    errs = []
    if sid != CATALOG_ID:
        return errs
    for i, e in enumerate(inst.get("entries", [])):
        xc = e.get("effects", {}).get("external_contact")
        if xc and xc.get("destination_form") == "from_argument":
            names = [a.get("argument_name") for a in e.get("input", {}).get("arguments", [])]
            if xc.get("argument_name") not in names:
                errs.append(f"$.entries[{i}]: CX-1 from_argument names '{xc.get('argument_name')}', "
                            f"not an argument of the entry {names}")
    return errs


def mutations(design, schema, reg):
    """V18-3 R-7: three mutations of catalog.example-valid-2.json, each must be rejected."""
    base = json.loads((design / "catalog.example-valid-2.json").read_text())
    dr = next(i for i, e in enumerate(base["entries"]) if e.get("entry_kind") == "destination_request")
    fa = next(i for i, e in enumerate(base["entries"])
              if e["effects"].get("external_contact", {}).get("destination_form") == "from_argument")
    cases = []
    m = copy.deepcopy(base)
    m["entries"][dr]["exposure"].update({"H": "exposed", "X": "exposed"})
    cases.append(("destination request entry exposed on H and X", m))
    m = copy.deepcopy(base)
    m["entries"][dr]["input"]["arguments"] = [a for a in m["entries"][dr]["input"]["arguments"]
                                              if a["value_kind"] != "carried_call"]
    cases.append(("destination request entry without its carried_call argument", m))
    m = copy.deepcopy(base)
    m["entries"][fa]["effects"]["external_contact"]["argument_name"] = "address"
    cases.append(("from_argument naming an argument the entry lacks", m))
    bad = 0
    for name, inst in cases:
        errs = validate(inst, schema, reg) + conformance(inst, CATALOG_ID)
        bad += 0 if errs else 1
        print(f"    {'PASS' if errs else 'FAIL'} mutation (V18-3 R-7) {name}: "
              + (f"rejected -> {errs[0]}" if errs else "accepted"))
    return bad


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
            errs = validate(inst, s, reg) + conformance(inst, s["$id"])
            want_valid = ".example-valid" in ex.name
            ok = (not errs) if want_valid else bool(errs)
            bad += 0 if ok else 1
            print(f"    {'PASS' if ok else 'FAIL'} {ex.name}: {'valid' if not errs else 'invalid'}"
                  + ("" if not errs else f" -> {errs[0]}" + (f" (+{len(errs) - 1} more)" if len(errs) > 1 else "")))
        if s["$id"] == CATALOG_ID:
            bad += mutations(f.parent, s, reg)
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
                errs = (validate(inst, ids[sid], reg) + conformance(inst, sid)) if sid else ["no schema claimed"]
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
