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
    ("P6 notes assert no work", lambda a: a["cases"]["P6"].update(notes="So no work remains in this undertaking."), {("P6", "K6"): "referred"}),
    ("DM-1 claims admitted support", lambda a: a["cases"]["DM-1"].update(admitted_current_support_for_3_0_m=True), {("DM-1", "K7"): "not met"}),
    ("P4 change list short", lambda a: a["cases"]["P4"]["answer"].update(c=a["cases"]["P4"]["answer"]["c"][:5]), {("P4", "K3"): "not met"}),
    ("independence answered yes", lambda a: a["cases"].update(independence="Yes, PEC absence makes Domains unknown."), {("INDEPENDENCE", "K9"): "not met"}),
]
bad = 0
for name, f, expect in CASES:
    a = copy.deepcopy(acc)
    f(a)
    got = {(r["case"], r["item"]): r["verdict"] for r in C.score(a, key)}
    ok = all(got[k] == v for k, v in expect.items())
    bad += not ok
    print(("BITES  " if ok else "MISSED ") + name)
print(f"\n{len(CASES) - bad}/{len(CASES)} alterations caught")
sys.exit(1 if bad else 0)
