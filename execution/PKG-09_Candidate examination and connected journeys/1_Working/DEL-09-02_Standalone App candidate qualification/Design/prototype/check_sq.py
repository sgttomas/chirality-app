#!/usr/bin/env python3
"""DEL-09-02 SQ-v0.1 design prototype: checks the PROPOSED dossier schema, its
example sets, the rules SQ-R1...SQ-R7 a schema cannot express, and that every
supplier case the step map cites exists as a designed-case row in that
supplier's actual Design file (SQ-R6).

Not product code. A pass shows the rules run as written on illustrative
dossiers; it passes no VER criterion (SQ §10). Needs Python 3 and `jsonschema`
(Draft 2020-12); reads only.

    python3 check_sq.py
"""
import glob
import json
import os
import re
import sys

from jsonschema import Draft202012Validator

HERE = os.path.dirname(os.path.abspath(__file__))
DESIGN = os.path.dirname(HERE)
EXEC = os.path.abspath(os.path.join(DESIGN, "..", "..", "..", ".."))
RESULTS = []
SCENARIOS = ["V4-EXM-10", "V4-EXM-11", "V4-EXM-12"]
NOT_CLAIMED = {"joined_host_witness", "replacement", "public_release", "retirement",
               "professional_reliance", "practitioner_validation"}


def check(n, ok, d=""):
    RESULTS.append((n, bool(ok), d))


def load(n):
    with open(os.path.join(DESIGN, n), encoding="utf-8") as f:
        return json.load(f)


def supplier_file(deliverable, name):
    hits = glob.glob(os.path.join(EXEC, "PKG-*", "1_Working", f"{deliverable}_*", "Design", name))
    return hits[0] if len(hits) == 1 else None


_case_cache = {}


def case_exists(deliverable, name, case_id):
    p = supplier_file(deliverable, name)
    if not p:
        return False
    if p not in _case_cache:
        with open(p, encoding="utf-8") as f:
            _case_cache[p] = f.read()
    return re.search(r"^\| " + re.escape(case_id) + r"\b", _case_cache[p], re.M) is not None


def aggregate(outs):
    if "fail" in outs:
        return "fail"
    if "blocked" in outs:
        return "blocked"
    if outs and all(o == "pass" for o in outs):
        return "pass"
    if all(o == "not-run" for o in outs):
        return "not-run"
    return "inconclusive"


def violations(d, step_map):
    v = []
    names = [s["scenario"] for s in d["scenarios"]]
    if sorted(names) != SCENARIOS:
        v.append("SQ-R1")
    by = {s["scenario"]: s for s in d["scenarios"]}
    if "V4-EXM-10" in by and "V4-EXM-11" in by and by["V4-EXM-10"]["run_ref"] != by["V4-EXM-11"]["run_ref"]:
        v.append("SQ-R2")
    m12 = by.get("V4-EXM-12")
    if m12:
        modes = m12.get("access_modes", [])
        kinds = sorted(m["kind"] for m in modes)
        homes = {m["kind"]: m["home"] for m in modes}
        convs = [m["conversation_ref"] for m in modes]
        if (kinds != ["api_key", "chatgpt_account", "local_provider"] or homes.get("api_key") != "H-key"
                or homes.get("chatgpt_account") != "H-acct" or len(set(convs)) != 3):
            v.append("SQ-R3")
    for s in d["scenarios"]:
        outs = [st.get("outcome", "not-run") if st["state"] == "recorded" else "not-run" for st in s["steps"]]
        if aggregate(outs) != s["outcome"]:
            v.append("SQ-R4")
            break
    if not NOT_CLAIMED <= set(d["handoff"]["not_claimed"]):
        v.append("SQ-R5")
    for s in d["scenarios"]:
        for st in s["steps"]:
            for c in st["supplier_cases"]:
                if not case_exists(c["deliverable"], c["file"], c["case_id"]):
                    v.append("SQ-R6")
                    break
    for s in d["scenarios"]:
        want = [x["step"] for x in step_map.get(s["scenario"], [])]
        if [st["step"] for st in s["steps"]] != want:
            v.append("SQ-R7")
            break
    return sorted(set(v))


def main():
    schema = load("sq.dossier.schema.json")
    Draft202012Validator.check_schema(schema)
    val = Draft202012Validator(schema)
    check("SCHEMA sq.dossier.schema.json is valid 2020-12", True)
    step_map = load("sq.step-map.json")
    n = 0
    for scen, steps in step_map.items():
        for st in steps:
            for c in st["supplier_cases"]:
                n += 1
                check(f"SQ-R6 step map {scen} {st['step']} {c['case_id']} exists in {c['file']}",
                      case_exists(c["deliverable"], c["file"], c["case_id"]))
    for d in load("sq.dossier.valid.examples.json"):
        errs = list(val.iter_errors(d))
        check(f"VALID {d['record_id']}", not errs, "; ".join(e.message[:120] for e in errs[:2]))
        check(f"RULES {d['record_id']} none violated", not violations(d, step_map), str(violations(d, step_map)))
    for i in load("sq.dossier.invalid.examples.json"):
        check(f"INVALID {i['record']['record_id']} ({i['why']})", list(val.iter_errors(i["record"])))
    for i in load("sq.dossier.rule-violations.examples.json"):
        errs = list(val.iter_errors(i["record"]))
        check(f"RULE-SCHEMA {i['record']['record_id']} schema-valid", not errs, "; ".join(e.message[:120] for e in errs[:2]))
        got = violations(i["record"], step_map)
        check(f"RULES {i['record']['record_id']} {i['rule']} detected", i["rule"] in got, str(got))
    fails = [r for r in RESULTS if not r[1]]
    for name, ok, d in RESULTS:
        print(f"{'PASS' if ok else 'FAIL'}  {name}" + (f"  -- {d}" if d and not ok else ""))
    print(f"TOTAL {len(RESULTS)}, FAIL {len(fails)}  ({n} supplier case citations checked)")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
