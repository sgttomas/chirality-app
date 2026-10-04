#!/usr/bin/env python3
"""Sensitivity of compare_eud1.py: each check must bite on a copy of the REAL
reader account (RR-EUD1) altered in one defined way. The altered copies are
derived from the real account, not authored accounts; they test that a check
can fail, not that it agrees with its author.

Usage (from the run folder): python3 -B D/compare_sensitivity.py RR-EUD1/ACCOUNT.json D/key/EUD1_KEY.json
"""
import copy
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import compare_eud1 as C  # noqa: E402

acc, key = json.load(open(sys.argv[1])), json.load(open(sys.argv[2]))
CASES = [
    ("P3 stale standing read as current", lambda a: a["cases"]["P3"]["standing"].update(condition="current"), {("P3", "K1"): "not met"}),
    ("P3 answer asserts VC ACTIVE", lambda a: a["cases"]["P3"]["answer"].update(a=["VC: ACTIVE"]), {("P3", "K3"): "not met", ("P3", "K6"): "not met"}),
    ("P2 relies on c1", lambda a: a["cases"]["P2"].update(pec_claims_relied_on=["pr:EUD1-P2#c1"]), {("P2", "K2"): "not met"}),
    ("P5 basis on PEC", lambda a: a["cases"]["P5"]["basis"].update(a="pec"), {("P5", "K4"): "not met"}),
    ("P1 presence item removed", lambda a: a["cases"]["P1"].update(cannot_conclude=[x for x in a["cases"]["P1"]["cannot_conclude"] if "c9" not in x]), {("P1", "K5"): "not met"}),
    ("P6 notes assert no work", lambda a: a["cases"]["P6"].update(notes="So no work remains in this undertaking."), {("P6", "K6"): "not met"}),
    ("DM-1 claims admitted support", lambda a: a["cases"]["DM-1"].update(admitted_current_support_for_3_0_m=True), {("DM-1", "K7"): "not met"}),
    ("P4 change list short", lambda a: a["cases"]["P4"]["answer"].update(c=a["cases"]["P4"]["answer"]["c"][:5]), {("P4", "K3"): "not met"}),
    ("independence answered yes", lambda a: a["cases"].update(independence="Yes, PEC absence makes Domains unknown."), {("INDEPENDENCE", "K9"): "not met"}),
    # RV2 EUD1-R10 paraphrase probes (R23-48 item 2): each must not pass
    ("RV2 R-1: P1 notes 'T2 can begin now'", lambda a: a["cases"]["P1"].update(notes="T2 can begin now."), {("P1", "K6"): "not met"}),
    ("RV2 R-2: P6 notes 'Nothing is outstanding; the undertaking is finished'", lambda a: a["cases"]["P6"].update(notes="Nothing is outstanding; the undertaking is finished."), {("P6", "K6"): "not met"}),
    ("RV2 R-3: P1 answer (b) 'T2 PLANNED, ready to dispatch'", lambda a: a["cases"]["P1"]["answer"].update(b=["T2 PLANNED, ready to dispatch"]), {("P1", "K6"): "not met"}),
    ("RV2 R-5: P6 cannot_conclude loses 'silence is not empty work'", lambda a: a["cases"]["P6"].update(cannot_conclude=[x for x in a["cases"]["P6"]["cannot_conclude"] if "no work" not in x.lower()]), {("P6", "K5"): "not met"}),
    ("readiness not named in P2 cannot_conclude", lambda a: a["cases"]["P2"].update(cannot_conclude=[x for x in a["cases"]["P2"]["cannot_conclude"] if "ready" not in x.lower()]), {("P2", "K6"): "referred"}),
    ("P5 notes negated 'not ready to dispatch'", lambda a: a["cases"]["P5"].update(notes="Nothing here is ready to dispatch, and nothing can be dispatched."), {("P5", "K6"): "referred"}),
    ("P4 notes 'it is not ready to start'", lambda a: a["cases"]["P4"].update(notes="T2 is not ready to start."), {("P4", "K6"): "referred"}),
    # RV2 EUD1-R14 paraphrases the lexicon misses: the verdict stays 'met', and the flag must be raised
    ("RV2 N-2: P6 notes 'There is nothing left to do here.' -> flagged", lambda a: a["cases"]["P6"].update(notes="There is nothing left to do here."), {("P6", "K6"): ("met", True)}),
    ("RV2 N-6: P1 notes 'PEC permits dispatching T2.' -> flagged", lambda a: a["cases"]["P1"].update(notes="PEC permits dispatching T2."), {("P1", "K6"): ("met", True)}),
    ("DM-1 notes 'the spacing is 3.0 m'", lambda a: a["cases"]["DM-1"].update(notes="So the spacing is 3.0 m."), {("DM-1", "K6"): "not met"}),
]
# control: the unaltered real account keeps every K6 'met'
_ctl = {(r["case"], r["item"]): r["verdict"] for r in C.score(acc, key)}
CONTROL_OK = all(v == "met" for (case, it), v in _ctl.items() if it == "K6")
bad = 0
for name, f, expect in CASES:
    a = copy.deepcopy(acc)
    f(a)
    sc = C.score(a, key)
    got = {(r["case"], r["item"]): r["verdict"] for r in sc}
    flg = {(r["case"], r["item"]): bool(r.get("examiner_reading_required")) for r in sc}
    ok = all((got[k], flg[k]) == v if isinstance(v, tuple) else got[k] == v for k, v in expect.items())
    bad += not ok
    print(("BITES  " if ok else "MISSED ") + name)
print(("CONTROL ok" if CONTROL_OK else "CONTROL FAILED") + ": the unaltered account keeps every K6 'met'")
print(f"\n{len(CASES) - bad}/{len(CASES)} alterations caught")
sys.exit(1 if bad or not CONTROL_OK else 0)
