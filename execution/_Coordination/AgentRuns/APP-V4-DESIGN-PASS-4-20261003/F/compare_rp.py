"""EU-F1 examiner comparison: a reader's account against the frozen answer key. Prototype; reads only.

Usage:
  python3 -B compare_rp.py [--set N] --self-check     # the key agrees with the fixture's own records
  python3 -B compare_rp.py [--set N] <account.json>   # compare a reader's account

--set 1 (default): IS-FX-RP1-1, fixture FX-RP1, key EU-F1.answer-key.json (frozen 2026-10-04; read by RR-EUF1).
--set 2: IS-FX-RP1-2, fixture FX-RP1-2, key EU-F1-2.answer-key.json (RP-v0.2).

Fields compare exactly (set fields as sets). Statements and issues are never scored automatically:
they are printed as REFERRED for the examiner to read for contradictions with the records.
"""

import json
import os
import sys

from jsonschema import Draft202012Validator

import glob

HERE = os.path.dirname(os.path.abspath(__file__))
SETS = {"1": ("IS-FX-RP1-1", "FX-RP1", "EU-F1.answer-key.json"),
        "2": ("IS-FX-RP1-2", "FX-RP1-2", "EU-F1-2.answer-key.json")}
IS_ID, FX_NAME, KEY = SETS["1"]
FX = os.path.join(HERE, "fixtures", FX_NAME)


def one(pattern):
    found = glob.glob(os.path.join(FX, pattern))
    assert len(found) == 1, (pattern, found)
    return found[0]


def load(p):
    with open(p, encoding="utf-8") as fh:
        return json.load(fh)


def self_check(key):
    """The key must agree with the fixture records wherever a record states the answer directly."""
    m = load(one("packet/*.packet-manifest.json"))
    pkg = load(one("package/*.json"))
    d = load(one("records/*.json"))
    e = key["expected"]
    checks = [
        ("Q-1 package_id", e["Q-1"]["package_id"] == pkg["packageId"] and e["Q-1"]["act_kind"] == pkg["actKind"]),
        ("Q-2 revision", e["Q-2"]["subject_revision"] == m["candidate"]["subject"]["app_candidate"]["revision"]),
        ("Q-2 reconciliation", e["Q-2"]["reconciliation"] == m["candidate"]["reconciliation"]),
        ("Q-3 elements", e["Q-3"]["elements"] == {x["element"]: x["status"] for x in m["core_loop"]["elements"]}),
        ("Q-3 obligation", e["Q-3"]["obligation"] == m["core_loop"]["obligation"] and e["Q-3"]["established"] == m["core_loop"]["established"]),
        ("Q-3 outside", set(e["Q-3"]["outside_scenarios"]) == {o["scenario"] for o in m["core_loop"]["outside_core_loop"]}),
        ("Q-4", e["Q-4"] == {"status": m["journey"]["status"], "counts_as_completed_witness": m["journey"]["counts_as_completed_witness"],
                             "acceptance_acts": m["journey"]["acceptance_acts"], "independent_review": m["journey"]["independent_review"]}),
        ("Q-5", e["Q-5"]["replacement_evidence_complete"] == m["replacement_evidence"]["complete"]),
        ("Q-6 ids", set(e["Q-6"]["gap_ids"]) == {g["gap_id"] for g in m["gaps"]}),
        ("Q-6 suppliers", set(e["Q-6"]["gap_supplier_deliverables"]) == {g["supplier"][:9] for g in m["gaps"]}),
        ("Q-7 alternatives", set(e["Q-7"]) == {a["id"] for a in pkg["alternatives"]}),
        ("Q-8", e["Q-8"]["decision_state"] == d["state"]),
        ("Q-9", e["Q-9"]["standing"] == m["practitioner"]["standing"]),
        ("Q-10", set(e["Q-10"]["never_established"]) == set(m["not_established"])),
        ("Q-11", e["Q-11"]["thesis_identity"] == m["continuity"]["thesis_identity"]
         and e["Q-11"]["continuing_obligations"] == m["continuity"]["continuing_obligations"]
         and e["Q-11"]["adoption_status"] == m["adoption"]["status"]),
        ("Q-12", e["Q-12"]["evidence_standing"] == m["evidence_standing"]),
    ]
    for name, ok in checks:
        print(("HOLDS " if ok else "FAILS ") + "key agrees with fixture: " + name)
    return all(ok for _, ok in checks)


def compare(key, account):
    errs = sorted(err.message for err in Draft202012Validator(load(os.path.join(HERE, "rp.reader-account.schema.json"))).iter_errors(account))
    print(("HOLDS " if not errs else "FAILS ") + "account valid against rp.reader-account.schema.json" + ("" if not errs else " -> %s" % errs))
    inset = open(os.path.join(HERE, IS_ID + ".input-set.sha256"), "rb").read()
    import hashlib
    ok_set = account.get("input_set", {}).get("sha256") == hashlib.sha256(inset).hexdigest()
    print(("HOLDS " if ok_set else "FAILS ") + "account names input set %s by its sha256" % IS_ID)
    held, total = 0, 0
    sets = set(key["set_fields"])
    for q, exp in key["expected"].items():
        got = account.get("answers", {}).get(q, {}).get("fields", {})
        for f, v in exp.items():
            total += 1
            g = got.get(f)
            ok = (set(g or []) == set(v)) if ("%s.%s" % (q, f)) in sets else (g == v)
            held += ok
            print(("HOLDS " if ok else "FAILS ") + "%s.%s" % (q, f) + ("" if ok else "  expected %r, got %r" % (v, g)))
    for q in sorted(account.get("answers", {})):
        print("REFERRED %s statement: %s" % (q, account["answers"][q].get("statement")))
    for i in account.get("issues", []):
        print("REFERRED issue (%s): %s" % (i.get("about"), i.get("statement")))
    print("%d/%d fields held; %d issues referred" % (held, total, len(account.get("issues", []))))
    return not errs and ok_set and held == total


def main():
    global IS_ID, FX_NAME, KEY, FX
    args = sys.argv[1:]
    if args[:1] == ["--set"]:
        IS_ID, FX_NAME, KEY = SETS[args[1]]
        FX = os.path.join(HERE, "fixtures", FX_NAME)
        args = args[2:]
    print("set %s: %s, fixture %s, key %s" % (IS_ID[-1], IS_ID, FX_NAME, KEY))
    key = load(os.path.join(HERE, KEY))
    if args == ["--self-check"]:
        ok = self_check(key)
    else:
        ok = compare(key, load(args[0]))
    raise SystemExit(0 if ok else 1)


if __name__ == "__main__":
    main()
