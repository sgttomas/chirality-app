#!/usr/bin/env python3
"""DEL-09-02 SQ-v0.2 design prototype: checks the PROPOSED dossier schema, its
example sets, the rules SQ-R1...SQ-R10 a schema cannot express, and that every
supplier case the step map cites exists as a designed-case row in that
supplier's actual Design file (SQ-R6).

Not product code. A pass shows the rules run as written on illustrative
dossiers; it passes no VER criterion (SQ §10). Needs Python 3 and `jsonschema`
(Draft 2020-12); reads only.

    python3 check_sq.py
"""
import glob
import copy
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
CORE_LOOP = {"planning", "execution", "workflow saving", "reuse", "approvals", "interruption", "restart"}  # DEL-11-03 REQ-001


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


def map_steps(step_map):
    return {s["step"]: s for v in step_map["scenarios"].values() for s in v}


def violations(d, step_map):
    v = []
    ms = map_steps(step_map)
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
    # SQ-R4 a scenario outcome only once every counted step is recorded; it is their aggregate
    for s in d["scenarios"]:
        counted = [st for st in s["steps"] if st.get("counts", True)]
        if "outcome" in s:
            if any(st["state"] != "recorded" for st in counted) or aggregate([st["outcome"] for st in counted]) != s["outcome"]:
                v.append("SQ-R4")
                break
    if not NOT_CLAIMED <= set(d["handoff"]["not_claimed"]):
        v.append("SQ-R5")
    for s in d["scenarios"]:
        for st in s["steps"]:
            if any(not case_exists(c["deliverable"], c["file"], c["case_id"]) for c in st["supplier_cases"]):
                v.append("SQ-R6")
                break
    for s in d["scenarios"]:
        want = [x["step"] for x in step_map["scenarios"].get(s["scenario"], [])]
        if [st["step"] for st in s["steps"]] != want:
            v.append("SQ-R7")
            break
    # SQ-R8 handover as qualification, and independence
    h = d["handoff"]
    if h["handed_over"]:
        all_recorded = all(st["state"] == "recorded" for s in d["scenarios"] for st in s["steps"] if st.get("counts", True))
        if not all_recorded or any("outcome" not in s for s in d["scenarios"]) or not d["examiner"].get("review_record"):
            v.append("SQ-R8")
    if h["reported_as_independent"] and (d["examiner"]["separation"] == "not_separate" or not d["examiner"].get("review_record")):
        v.append("SQ-R8")
    # SQ-R9 stimuli: a recorded counted step lists every stimulus its map declares; one not produced cannot pass
    for s in d["scenarios"]:
        for st in s["steps"]:
            if st["state"] != "recorded" or not st.get("counts", True):
                continue
            declared = set(ms.get(st["step"], {}).get("stimuli", []))
            given = {x["id"]: x for x in st.get("stimuli", [])}
            no_replay = {x["id"] for x in step_map["stimuli"] if not x.get("replay_counterpart")}
            if (declared - set(given)
                    or any(x["produced"] == "replay" and i in no_replay for i, x in given.items())
                    or (any(x["produced"] == "not_produced" for x in given.values())
                        and st["outcome"] not in ("blocked", "fail"))):
                v.append("SQ-R9")
                break
    # SQ-R10 a counted step's map entry carries counts consistently
    for s in d["scenarios"]:
        for st in s["steps"]:
            if st["step"] in ms and st.get("counts", True) != ms[st["step"]]["counts"]:
                v.append("SQ-R10")
                break
    return sorted(set(v))


def main():
    schema = load("sq.dossier.schema.json")
    Draft202012Validator.check_schema(schema)
    val = Draft202012Validator(schema)
    check("SCHEMA sq.dossier.schema.json is valid 2020-12", True)
    step_map = load("sq.step-map.json")
    n = 0
    for scen, steps in step_map["scenarios"].items():
        for st in steps:
            for c in st["supplier_cases"]:
                n += 1
                check(f"SQ-R6 step map {scen} {st['step']} {c['case_id']} exists in {c['file']}",
                      case_exists(c["deliverable"], c["file"], c["case_id"]))
    elements = {s["core_loop_element"] for s in sum(step_map["scenarios"].values(), [])}
    check("MAP covers DEL-11-03 REQ-001's seven core-loop elements", CORE_LOOP <= elements, str(sorted(elements)))
    check("MAP every step has a v3 reference", all(s.get("v3_reference") for s in sum(step_map["scenarios"].values(), [])))
    ids = {x["id"] for x in step_map["stimuli"]}
    used = {i for s in sum(step_map["scenarios"].values(), []) for i in s["stimuli"]}
    check("MAP every stimulus declared is used and every used one declared", ids == used, f"{sorted(ids)} vs {sorted(used)}")
    check("MAP added steps are not counted and give their reason",
          all((not s["counts"]) == s["step"].endswith("R") and (s["counts"] or s.get("added_reason"))
              for s in sum(step_map["scenarios"].values(), [])))
    check("MAP no act-control case for A4 joined at a registration step (RV2 SQ-R-C)",
          not any(c["case_id"] == "VC-AAC-04" for s in sum(step_map["scenarios"].values(), []) for c in s["supplier_cases"]))
    check("MAP VC-R-14 cited at every V4-EXM-11 step (one execution)",
          all(any(c["case_id"] == "VC-R-14" for c in s["supplier_cases"]) for s in step_map["scenarios"]["V4-EXM-11"]))
    # CC-SQ-J2-ST4: the prose stages delegation at J-2, not only recovery.
    check("MAP SQ §3.1/§3.4 ST-4 carried at J-2, S11-1 and S11-6",
          {s["step"] for s in map_steps(step_map).values() if "ST-4" in s["stimuli"]}
          == {"J-2", "S11-1", "S11-6"})
    # Paired probes prevent another stimulus or rule failure from masking omission.
    baseline = next(d for d in load("sq.dossier.valid.examples.json") if d["record_id"] == "SQ-EX-03")
    for produced, outcome, expected in [(None, "pass", ["SQ-R9"]),
                                         ("not_produced", "pass", ["SQ-R9"]),
                                         ("not_produced", "blocked", []),
                                         ("replay", "pass", [])]:
        probe = copy.deepcopy(baseline)
        scenario = next(s for s in probe["scenarios"] if s["scenario"] == "V4-EXM-10")
        step = next(s for s in scenario["steps"] if s["step"] == "J-2")
        step["stimuli"] = ([] if produced is None else
                           [{"id": "ST-4", "produced": produced,
                             **({"cause": "ILLUSTRATIVE delegation and recording unavailable"}
                                if produced == "not_produced" else
                                {"evidence": "ILLUSTRATIVE recorded delegation counterpart"})}])
        step["outcome"] = outcome
        scenario["outcome"] = aggregate([s["outcome"] for s in scenario["steps"] if s["counts"]])
        check(f"CC-SQ J-2 {produced}/{outcome}: schema valid and exact rules {expected}",
              not list(val.iter_errors(probe)) and violations(probe, step_map) == expected,
              str(violations(probe, step_map)))
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
