#!/usr/bin/env python3
"""DEL-08-02 RTD-v0.2 check: the research context account schema, its rules
RC-1…RC-4, and its consumption of DEL-08-01's receiving records.

Design prototype (owner O-D). Not product code. Needs Python 3 and
`jsonschema` (Draft 2020-12, `referencing`). No network; writes nothing.
It reads EU-D1's frozen Domains receiving records (RUN/D/evidence/records/,
CW and DRC as frozen) and the standing schema, read-only.

Accounts (all invented, built here):
- RCA-1 `limited`: built from DM-1. r1 (SRC-1, admitted at rev-A, stale) is
  used as `limited`, r2 (SRC-2, located, not admitted) as `located_only`;
  the candidate rests on an inference from them, and the account names why.
- RCA-2 `held`: built from DM-2 (Domains absent). No candidate; the gap is
  named.
- RCA-3 `supported`: an invented admitted, current source (constructed here
  as a receiving-record result with standing adopted/current/admitted). The
  candidate rests only on admitted evidence.
Negative cases (must be refused, by the schema or by a rule):
- N-1 `held` with a candidate (RC-6, schema);
- N-2 `supported` while resting on a located-only item (RC-1);
- N-3 a stale admitted result used as `admitted_evidence` (RC-4: use must
  follow the cited result's standing, CS-R1);
- N-4 an inference citing an id that does not exist (RC-3);
- N-5 `limited` that names no limit (RC-2);
- N-6 a candidate with no content identity offered as decidable (CA-2,
  checked as RC-5: a decision needs a content identity).

Usage: python3 -B check_rtd.py
"""
import copy
import json
import os
import sys

from jsonschema import Draft202012Validator
from referencing import Registry, Resource

HERE = os.path.dirname(os.path.abspath(__file__))
DESIGN = os.path.dirname(HERE)
EXEC = os.path.abspath(os.path.join(DESIGN, "..", "..", "..", ".."))
STANDING = os.path.join(EXEC, "PKG-07_PEC receiving and connector fallback", "1_Working",
                        "DEL-07-02_Connector limitation and source-file recovery paths", "Design", "connector.standing.schema.json")
EVID = os.path.join(EXEC, "_Coordination", "AgentRuns", "APP-V4-DESIGN-PASS-4-20261003", "D", "evidence", "records")
RESULTS = []
DRC = os.path.join(EXEC, "PKG-08_Domains research receiving", "1_Working",
                   "DEL-08-01_Domains query, admission and freshness contract", "Design", "DOMAINS_RECEIVING.md")
CFB = os.path.join(os.path.dirname(STANDING), "CONNECTOR_FALLBACK.md")
# RTD1-R1 (R23-52 item 4): the bytes this check and RTD-v0.2 rely on
PINS = {
    STANDING: "bf4cef4df1ef16bc4a2a8e8fbb341798a90a48abbbe3689d68d5ce9019650719",
    os.path.join(EVID, "DR-DM-1.json"): "075f0aadb9decb4885b6a908eaf9a5ecfb287905110cda70216e7b9a7b823c5d",
    os.path.join(EVID, "DR-DM-2.json"): "277def89778328e65ba0d0df7328755f0c2e60d835ae5a087e19faeafe616db7",
    DRC: "7bfa7fc496667652340573e7b50bc3fe94edfc4490e8b83d29a1feea2b558243",
    CFB: "69c1f10eb1ed0ecb65dbf75844d3d47daaae0842697f0e41c51b072c41353f16",
}


def pins_hold():
    import hashlib
    bad = []
    for p, want in PINS.items():
        with open(p, "rb") as f:
            got = hashlib.sha256(f.read()).hexdigest()
        if got != want:
            bad.append(f"{os.path.basename(p)}: {got[:12]}… != pinned {want[:12]}…")
    return bad


def check(cid, ok, detail=""):
    RESULTS.append((cid, bool(ok), detail))


def jl(p):
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def dm_results():
    """result key 'dr:…#rN' -> standing, from EU-D1's frozen Domains records."""
    out = {}
    for name in ("DR-DM-1.json", "DR-DM-2.json"):
        rec = jl(os.path.join(EVID, name))
        for r in rec["results"]:
            out[f"{rec['record_id']}#{r['result_id']}"] = r["standing"]
    return out


# A constructed admitted, current result for RCA-3 (no such Domains result exists; labelled)
CONSTRUCTED = {"dr:RTD-X#r1": {"connector": "domains", "envelope": "adopted", "condition": "current", "claim_tier": "admitted",
                               "supports_reliance": True, "reasons": [{"facet": "condition", "value": "current", "basis": "constructed for RTD's check"}]}}


def use_for(standing):
    """RC-4: the only use a result's standing allows (CS-R1)."""
    if standing["supports_reliance"]:
        return "admitted_evidence"
    if standing.get("claim_tier") == "located_not_admitted":
        return "located_only"
    return "limited"


def accounts():
    rca1 = {"format": "chirality.research.context-account", "formatVersion": "0.1", "account_id": "rc:RTD-1",
            "question": "Which support spacing should the candidate use for line EX-L1 (invented)?",
            "receiving_records": ["dr:EUD1-DM-1"],
            "evidence": [
                {"evidence_id": "e1", "source_ref": "domains/sources/SRC-1.md", "revision": "rev-A", "statement": "SRC-1 at rev-A states 3.0 m", "use": "limited", "standing_ref": "dr:EUD1-DM-1#r1"},
                {"evidence_id": "e2", "source_ref": "domains/sources/SRC-2.md", "revision": "rev-1", "statement": "SRC-2 states 3.0 m", "use": "located_only", "standing_ref": "dr:EUD1-DM-1#r2"}],
            "inferences": [{"inference_id": "i1", "statement": "A spacing of 3.0 m is suggested by the indexed material", "from": ["e1", "e2"],
                            "limits": "e1 is stale (SRC-1 is now rev-B) and e2 is not admitted; no admitted current source supports it"}],
            "gaps": [{"gap": "No admitted current source for line EX-L1 spacing", "effect": "the candidate is limited", "responsible": "the admitting party (unallocated; OI-023, OI-026)"}],
            "candidate": {"candidate_ref": "cand:EX-L1-a", "content_identity": "sha256:" + "0" * 64, "rests_on": ["i1"]},
            "standing": "limited", "recorder": {"kind": "tool", "identity": "check_rtd.py (invented account)"}}
    rca2 = {"format": "chirality.research.context-account", "formatVersion": "0.1", "account_id": "rc:RTD-2",
            "question": rca1["question"], "receiving_records": ["dr:EUD1-DM-2"], "evidence": [], "inferences": [],
            "gaps": [{"gap": "Domains gave no response", "effect": "research held; no candidate from it", "responsible": "the Domains query tool's owner (unallocated)"}],
            "candidate": None, "standing": "held", "recorder": rca1["recorder"]}
    rca3 = {"format": "chirality.research.context-account", "formatVersion": "0.1", "account_id": "rc:RTD-3",
            "question": rca1["question"], "receiving_records": ["dr:RTD-X"],
            "evidence": [{"evidence_id": "e1", "source_ref": "domains/sources/SRC-3.md (invented)", "revision": "rev-C", "statement": "SRC-3 states 2.4 m", "use": "admitted_evidence", "standing_ref": "dr:RTD-X#r1"}],
            "inferences": [{"inference_id": "i1", "statement": "Use 2.4 m", "from": ["e1"]}],
            "gaps": [], "candidate": {"candidate_ref": "cand:EX-L1-b", "content_identity": "sha256:" + "1" * 64, "rests_on": ["i1"]},
            "standing": "supported", "recorder": rca1["recorder"]}
    return rca1, rca2, rca3


def leaves(acc, ref, seen=None):
    """Evidence ids a candidate reference ultimately rests on."""
    seen = seen or set()
    ev = {e["evidence_id"] for e in acc["evidence"]}
    inf = {i["inference_id"]: i for i in acc["inferences"]}
    if ref in ev:
        return {ref}
    if ref in inf and ref not in seen:
        seen.add(ref)
        out = set()
        for x in inf[ref]["from"]:
            out |= leaves(acc, x, seen)
        return out
    return set()


def rules(acc, standings):
    v = []
    ev = {e["evidence_id"]: e for e in acc["evidence"]}
    ids = set(ev) | {i["inference_id"] for i in acc["inferences"]}
    for i in acc["inferences"]:
        if any(x not in ids for x in i["from"]):
            v.append("RC-3")
    cand = acc.get("candidate")
    rests = set()
    if cand:
        for r in cand["rests_on"]:
            if r not in ids:
                v.append("RC-3")
            rests |= leaves(acc, r)
    if acc["standing"] == "supported" and any(ev[e]["use"] != "admitted_evidence" for e in rests):
        v.append("RC-1")
    if acc["standing"] == "limited":
        named = any(i.get("limits") for i in acc["inferences"]) or acc["gaps"]
        if not named or not any(ev[e]["use"] != "admitted_evidence" for e in rests):
            v.append("RC-2")
    for e in acc["evidence"]:
        st = standings.get(e.get("standing_ref"))
        if st is None or use_for(st) != e["use"]:
            v.append("RC-4")
    if cand and cand.get("content_identity") is None and acc["standing"] != "held":
        v.append("RC-5")
    return sorted(set(v))


def main():
    bad = pins_hold()
    check("P-0 supplier pins hold (RTD1-R1)", not bad, "; ".join(bad))
    if bad:
        for cid, ok, d in RESULTS:
            print(("PASS " if ok else "FAIL ") + cid + (f"  [{d}]" if d and not ok else ""))
        sys.exit(1)
    std = jl(STANDING)
    sch = jl(os.path.join(DESIGN, "research.context-account.schema.json"))
    for s in (std, sch):
        Draft202012Validator.check_schema(s)
    reg = Registry().with_resources([(std["$id"], Resource.from_contents(std))])
    val = Draft202012Validator(sch, registry=reg)
    standings = dict(dm_results())
    standings.update(CONSTRUCTED)
    sv = Draft202012Validator({"$ref": std["$id"] + "#/$defs/standing"}, registry=reg)
    check("C-2 RCA-3's constructed standing is valid in DEL-07-02's vocabulary", not list(sv.iter_errors(CONSTRUCTED["dr:RTD-X#r1"])))
    check("C-0 DM-1 results read from EU-D1's frozen evidence", "dr:EUD1-DM-1#r1" in standings and "dr:EUD1-DM-1#r2" in standings)
    rca1, rca2, rca3 = accounts()
    for a, expect_standing in ((rca1, "limited"), (rca2, "held"), (rca3, "supported")):
        errs = [e.message for e in val.iter_errors(a)]
        check(f"V {a['account_id']} schema-valid", not errs, "; ".join(errs[:2]))
        check(f"V {a['account_id']} rules hold", not rules(a, standings), str(rules(a, standings)))
        check(f"V {a['account_id']} standing {expect_standing}", a["standing"] == expect_standing)
    check("C-1 RCA-1 uses follow DM-1's standings (r1 stale admitted -> limited; r2 located -> located_only)",
          [use_for(standings['dr:EUD1-DM-1#r1']), use_for(standings['dr:EUD1-DM-1#r2'])] == ["limited", "located_only"])
    # negatives
    n1 = copy.deepcopy(rca2); n1["candidate"] = copy.deepcopy(rca1["candidate"])
    check("N-1 held with a candidate refused (RC-6, schema)", list(val.iter_errors(n1)))
    n2 = copy.deepcopy(rca1); n2["standing"] = "supported"
    check("N-2 supported resting on located/limited items refused (RC-1)", "RC-1" in rules(n2, standings))
    n3 = copy.deepcopy(rca1); n3["evidence"][0]["use"] = "admitted_evidence"
    check("N-3 stale admitted result used as admitted evidence refused (RC-4)", "RC-4" in rules(n3, standings))
    n4 = copy.deepcopy(rca1); n4["inferences"][0]["from"] = ["e9"]
    check("N-4 inference citing an unknown id refused (RC-3)", "RC-3" in rules(n4, standings))
    n5 = copy.deepcopy(rca1); n5["inferences"][0].pop("limits"); n5["gaps"] = []
    check("N-5 limited naming no limit refused (RC-2)", "RC-2" in rules(n5, standings))
    n6 = copy.deepcopy(rca3); n6["candidate"]["content_identity"] = None
    check("N-6 decidable candidate without content identity refused (RC-5; CA-2)", "RC-5" in rules(n6, standings))
    failed = [r for r in RESULTS if not r[1]]
    for cid, ok, d in RESULTS:
        print(("PASS " if ok else "FAIL ") + cid + (f"  [{d}]" if d and not ok else ""))
    print(f"\n{len(RESULTS) - len(failed)}/{len(RESULTS)} checks held")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
