"""Maintained EXP-v0.2 rules transcribed unchanged from pinned Design prototype.
Call after schema checks; file consistency never establishes an observation.
"""
NATIVE={"native_development","native_packaged"}


def aggregate(parts):
    """EXP-R1: same order as CA W-R6, in EXP's labels."""
    outs = [p["outcome"] for p in parts]
    if "fail" in outs:
        return "fail"
    if "blocked" in outs:
        return "blocked"
    if outs and all(o == "pass" for o in outs):
        return "pass"
    if all(o == "not-run" for o in outs):
        return "not-run"
    return "inconclusive"


def rule_violations(rec):
    v = []
    # EXP-R1 aggregation over the applicable parts (R23-19); a declared
    # not-applicable part is listed apart and never also run
    if rec.get("parts"):
        if aggregate(rec["parts"]) != rec["outcome"]:
            v.append("EXP-R1")
    na = {p["part"] for p in rec.get("parts_not_applicable", [])}
    if na & {p["part"] for p in rec.get("parts", [])}:
        v.append("EXP-R1")
    # EXP-R3 only a candidate-basis record stands for a scenario (V4-EXM-nn), whatever its outcome
    if rec["case"].get("scenario") and rec["run_basis"] != "candidate" and rec["outcome"] != "not-run":
        v.append("EXP-R3")
    # EXP-R4 a part or record needing native evidence cannot pass on browser/replay evidence only
    units = rec.get("parts") or []
    for u in units:
        if u.get("needs_native") and u["outcome"] == "pass":
            routes = {e.get("route", rec["configuration"]["route"]["kind"]) for e in u.get("evidence", [])}
            if not routes & NATIVE:
                v.append("EXP-R4")
                break
    # EXP-R5 every cited act names an actor other than its recorder
    for a in rec.get("acts_cited", []):
        if a["actor"].strip().lower() == a["recorder"].strip().lower():
            v.append("EXP-R5")
            break
    return v


def review_violations(r):
    v = []
    author_ids = {a["identity"] for a in r["authors"]}
    if r["reported_as_independent"] and (r["reviewer"]["identity"] in author_ids
                                         or r["reviewer"].get("separation") == "not_separate"):
        v.append("EXP-R6")
    if r["family_claim"] == "different_family_observed":
        ids = [r["reviewer"]["model_identity"]] + [a["model_identity"] for a in r["authors"]]
        if any(not isinstance(i, dict) for i in ids):
            v.append("EXP-R6")
        else:
            fams = {i["family"] for i in ids[1:]}
            if ids[0]["family"] in fams:
                v.append("EXP-R6")
    states = [f["disposition"]["state"] for f in r["findings"]]
    if r["standing"] == "findings_dispositioned" and ("open" in states or not states):
        v.append("EXP-R7")
    if r["standing"] == "no_findings" and states:
        v.append("EXP-R7")
    if r["standing"] == "findings_open" and "open" not in states:
        v.append("EXP-R7")
    return v


def impact_violations(ci, results_by_id):
    """EXP-R8: every affected prior result is historical or reopened and cites this record."""
    v = []
    for a in ci["affected"]:
        prior = results_by_id.get(a["prior_result"])
        if prior is None:
            v.append("EXP-R8")
            continue
        cur = prior["currency"]
        if cur["state"] == "current" or cur.get("change_ref") != ci["record_id"]:
            v.append("EXP-R8")
    return v
