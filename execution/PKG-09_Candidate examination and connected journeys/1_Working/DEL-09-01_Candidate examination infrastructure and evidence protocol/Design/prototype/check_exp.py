#!/usr/bin/env python3
"""DEL-09-01 EXP-v0.2 design prototype: checks the three PROPOSED schemas, their
example sets, the rules EXP-R1...EXP-R9 a schema cannot express, and the
vocabulary mapping of EXP §3 against the actual supplier and sibling files.

Not product code and not an App candidate. A pass here shows that the
definition's rules run as written on illustrative records; it passes no VER
criterion of DEL-09-01 (EXP §12). Needs Python 3 and the `jsonschema` package
(Draft 2020-12); no network, writes nothing.

    python3 check_exp.py            # from Design/prototype/
"""
import json
import os
import re
import sys

try:
    from jsonschema import Draft202012Validator
except ImportError:  # pragma: no cover
    print("jsonschema package not available; cannot run", file=sys.stderr)
    sys.exit(2)

HERE = os.path.dirname(os.path.abspath(__file__))
DESIGN = os.path.dirname(HERE)
EXEC = os.path.abspath(os.path.join(DESIGN, "..", "..", "..", ".."))
HOSTING = os.path.join(EXEC, "PKG-01_Native App and third-party harness integration", "1_Working",
                       "DEL-01-01_Stock Codex hosting and supplier contract", "Design", "HOSTING_BOUNDARY.md")
PKG09 = os.path.join(EXEC, "PKG-09_Candidate examination and connected journeys", "1_Working")
W14 = os.path.join(PKG09, "DEL-09-06_Connected activity contract and workflow round trip", "Design",
                   "w14-result-record.schema.json")
XT = os.path.join(PKG09, "DEL-09-09_External control and catalog-extension trace", "Design",
                  "xt-result-record.schema.json")

RESULTS = []


def check(case, ok, detail=""):
    RESULTS.append((case, bool(ok), detail))


def load(name):
    with open(os.path.join(DESIGN, name), encoding="utf-8") as f:
        return json.load(f)


def validator(schema_name):
    schema = load(schema_name)
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema)


# ---------------------------------------------------------------- rules
NATIVE = {"native_development", "native_packaged"}
ORDER = ["fail", "blocked"]  # W-R6 order, in HOSTING §9.3 labels


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


# ---------------------------------------------------------------- run
def run_examples(prefix, schema_name, rules=None):
    val = validator(schema_name)
    check(f"SCHEMA {schema_name} is valid 2020-12", True)
    valid = load(f"{prefix}.valid.examples.json")
    for rec in valid:
        errs = list(val.iter_errors(rec))
        check(f"VALID {rec['record_id']}", not errs, "; ".join(e.message for e in errs[:2]))
    for item in load(f"{prefix}.invalid.examples.json"):
        errs = list(val.iter_errors(item["record"]))
        check(f"INVALID {item['record']['record_id']} ({item['why']})", errs, "schema accepted it" if not errs else "")
    rv = load(f"{prefix}.rule-violations.examples.json")
    for item in rv:
        errs = list(val.iter_errors(item["record"]))
        check(f"RULE-SCHEMA {item['record']['record_id']} schema-valid", not errs,
              "; ".join(e.message for e in errs[:2]))
    return valid, rv


def main():
    results, res_rv = run_examples("exam.result-record", "exam.result-record.schema.json")
    for rec in results:
        check(f"RULES {rec['record_id']} none violated", not rule_violations(rec), str(rule_violations(rec)))
    for item in res_rv:
        got = rule_violations(item["record"])
        check(f"RULES {item['record']['record_id']} {item['rule']} detected", item["rule"] in got, str(got))

    reviews, rev_rv = run_examples("exam.review-record", "exam.review-record.schema.json")
    for r in reviews:
        check(f"RULES {r['record_id']} none violated", not review_violations(r), str(review_violations(r)))
    for item in rev_rv:
        got = review_violations(item["record"])
        check(f"RULES {item['record']['record_id']} {item['rule']} detected", item["rule"] in got, str(got))

    cis, ci_rv = run_examples("exam.change-impact", "exam.change-impact.schema.json")
    by_id = {r["record_id"]: r for r in results}
    for ci in cis:
        check(f"RULES {ci['record_id']} none violated", not impact_violations(ci, by_id), str(impact_violations(ci, by_id)))
    for item in ci_rv:
        got = impact_violations(item["record"], by_id)
        check(f"RULES {item['record']['record_id']} {item['rule']} detected", item["rule"] in got, str(got))

    # EXP-R9 vocabulary mapping against the actual files (R23-1)
    schema = load("exam.result-record.schema.json")
    exp_out = schema["$defs"]["outcome"]["enum"]
    exp_fix = schema["$defs"]["evidence"]["properties"]["fixture_standing"]["enum"]
    with open(HOSTING, encoding="utf-8") as f:
        h = f.read()
    m = re.search(r"\*\*Outcome labels\*\* per case: (.*?), bound to", h, re.S)
    hosting_out = re.findall(r"`([a-z-]+)`", m.group(1)) if m else []
    check("EXP-R9 outcome values equal HOSTING §9.3 labels", hosting_out == exp_out, f"HOSTING={hosting_out}")
    m2 = re.search(r"### 9\.2 Fixture standing labels\s+(.*?)\. The W11", h, re.S)
    hosting_fix = re.findall(r"`([a-z-]+)`", m2.group(1)) if m2 else []
    check("EXP-R9 fixture standing equals HOSTING §9.2 labels", hosting_fix == exp_fix, f"HOSTING={hosting_fix}")
    mapping = {"pass": "passed", "fail": "failed", "blocked": "blocked", "not-run": "not_run", "inconclusive": "inconclusive"}
    for path, label in ((W14, "W14"), (XT, "XT")):
        with open(path, encoding="utf-8") as f:
            s = json.load(f)
        enum = s["properties"]["outcome"]["enum"]
        check(f"EXP-R9 mapping EXP->{label} is one-to-one onto its outcome enum",
              sorted(mapping.values()) == sorted(enum) and len(set(mapping.values())) == 5, f"{label}={enum}")

    # the rule table of EXP §3.5 lists EXP-R1...EXP-R9 (RV EXP-R-E)
    with open(os.path.join(DESIGN, "EXAMINATION_PROTOCOL.md"), encoding="utf-8") as f:
        md = f.read()
    sec = md.split("### 3.5", 1)[1].split("\n## ", 1)[0] if "### 3.5" in md else ""
    listed = re.findall(r"^\| \*\*(EXP-R[0-9])\*\*", sec, re.M)
    check("RULE TABLE EXP §3.5 lists EXP-R1...EXP-R9 once each", listed == [f"EXP-R{i}" for i in range(1, 10)], str(listed))

    # either pin (R23-3): examples exist for both pins and both validate
    pins = {r["configuration"]["codex_pin"] for r in results}
    check("PIN examples cover 0.158.0 and 0.160.0", {"0.158.0", "0.160.0"} <= pins, str(sorted(pins)))

    fails = [r for r in RESULTS if not r[1]]
    for case, ok, detail in RESULTS:
        print(f"{'PASS' if ok else 'FAIL'}  {case}" + (f"  -- {detail}" if (detail and not ok) else ""))
    print(f"TOTAL {len(RESULTS)}, FAIL {len(fails)}")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
