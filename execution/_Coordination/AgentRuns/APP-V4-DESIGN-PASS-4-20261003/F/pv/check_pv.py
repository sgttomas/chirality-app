"""Check DEL-09-12's records and rules (PV-v0.3). Prototype, not product code. Reads only.

K-1..K-13 check the real records and the examples. Each rule about the real records is a function of them;
each N-case breaks a real record (or the schema text, for F-R12) in memory and runs the same function, naming
the rule that must refuse it. PRACTITIONER_VALIDATION.md §8 lists what has a negative case and what does not.

Usage: python3 -B check_pv.py
"""

import copy
import glob
import hashlib
import json
import os
import re

from jsonschema import Draft202012Validator

import pvlib as P

HERE = os.path.dirname(os.path.abspath(__file__))
results = []


def expect(name, fn, detail=""):
    try:
        ok, err = bool(fn() if callable(fn) else fn), ""
    except Exception as exc:
        ok, err = False, "%s: %s" % (type(exc).__name__, exc)
    results.append((name, ok, err or ("" if ok else detail)))


def def_errors(schema, d, rec):
    """Errors against one record kind's $def (not the top-level oneOf, so a refusal names its own reason)."""
    return [e.message for e in Draft202012Validator({"$ref": "#/$defs/" + d, "$defs": schema["$defs"]}).iter_errors(rec)]


def state_errors(arr, std):
    """K-4: the real state as it is today."""
    ok = (arr["state"] == "not_agreed" and arr["agreement"] is None and arr["period"] is None
          and all(not e["activities"] and e["availability"]["state"] == "blocked" for e in arr["expressions"])
          and std["standing"] == "not_agreed" and std["observations"] == [] and std["is_replacement_condition"] is False)
    return [] if ok else ["K-4 the records do not state today's state"]


def fr12_errors(schema):
    """K-7 (F-R12): no record kind has an outcome, verdict or score field."""
    return ["K-7 %s" % k for k in ('"outcome"', '"score"', '"verdict"', '"pass"') if k in json.dumps(schema)]


def method_note_errors(schema, at):
    """K-11: the method note carries exactly UC §5's fields, and nothing else."""
    ok = set(P.uc_fields(at)) == set(P.UC_TO_PV) and set(f for fs in P.UC_TO_PV.values() for f in fs) == set(schema["$defs"]["method_note"]["properties"])
    return [] if ok else ["K-11 method_note fields differ from UC §5"]


def handover_errors(std, schema, at):
    """K-12 (PV1-R5): every field of DEL-11-03's first-cut $defs/practitioner_standing (read at the commit) is in the
    hand-over with the same name, type, const and enum, except the differences P.HANDOVER_CHANGES states; and the
    record, with the stated differences undone, is valid against the first cut."""
    rp_all = json.loads(P.text_at(at, P.RP_SCHEMA))
    rp, pv = rp_all["$defs"]["practitioner_standing"], schema["$defs"]["standing"]
    errs = []
    added = sorted(set(pv["properties"]) - set(rp["properties"]))
    if added != sorted(P.HANDOVER_CHANGES["added"]):
        errs.append("K-12 fields added beyond the stated ones: %s" % added)
    for f, rdef in rp["properties"].items():
        pdef = pv["properties"].get(f)
        if pdef is None:
            errs.append("K-12 first-cut field %s missing" % f)
            continue
        if f in P.HANDOVER_CHANGES["changed"]:
            if (rdef.get("const"), pdef.get("const")) != P.HANDOVER_CHANGES["changed"][f]:
                errs.append("K-12 %s changed other than stated" % f)
            continue
        for k in ("type", "const", "enum"):
            if k in rdef and rdef[k] != pdef.get(k):
                errs.append("K-12 %s: %s %r differs from the first cut's %r" % (f, k, pdef.get(k), rdef[k]))
    if not set(rp["required"]) <= set(pv["required"]):
        errs.append("K-12 a first-cut required field is optional here")
    undone = {k: v for k, v in std.items() if k not in P.HANDOVER_CHANGES["added"]}
    undone["format"] = P.HANDOVER_CHANGES["changed"]["format"][0]
    errs += ["K-12 vs first cut: " + e.message for e in Draft202012Validator(dict(rp, **{"$defs": rp_all["$defs"]})).iter_errors(undone)]
    return errs


def manifest_errors(files, manifest):
    return ["K-2 %s" % f for h, f in (l.split("  ", 1) for l in manifest.splitlines()) if hashlib.sha256(files[f]).hexdigest() != h]


def main():
    at = open(os.path.join(HERE, "records", "BUILT_AT")).read().strip()
    schema = json.load(open(os.path.join(P.REPO, P.SCHEMA), encoding="utf-8"))
    V = Draft202012Validator(schema)
    rec = {n: json.load(open(os.path.join(HERE, "records", n), encoding="utf-8")) for n in ("PV-ARR-1.arrangement.json", "PV-STANDING-1.json")}
    design = os.path.join(P.REPO, P.DESIGN)
    valid = json.load(open(os.path.join(design, "pv.examples.valid.json"), encoding="utf-8"))
    invalid = json.load(open(os.path.join(design, "pv.examples.invalid.json"), encoding="utf-8"))

    files = {f: open(os.path.join(HERE, "records", f), "rb").read() for f in os.listdir(os.path.join(HERE, "records"))}
    expect("K-1 the real records (arrangement, standing) are valid", lambda: all(not list(V.iter_errors(r)) for r in rec.values()))
    expect("K-2 records/MANIFEST.sha256 holds", not manifest_errors(files, files["MANIFEST.sha256"].decode()))
    expect("K-3 rebuilding at the recorded commit reproduces the records exactly", lambda: P.build(at) == rec)
    arr, std = rec["PV-ARR-1.arrangement.json"], rec["PV-STANDING-1.json"]
    expect("K-4 the real state: not agreed, no agreement, no activity proposed or selected, both expressions blocked with their causes; standing not_agreed, 0 observations, not a replacement condition",
           not state_errors(arr, std))
    arrs = {P.arrangement_key(x): x for x in [arr] + [v["record"] for v in valid if v["record"].get("record_kind") == "pv_arrangement"]}
    expect("K-5 every valid example passes the schema and the rules PV-R1..PV-R5",
           lambda: all(not list(V.iter_errors(v["record"])) and not P.rule_errors(v["record"], at, arrs) for v in valid),
           [(v["why"], [e.message for e in V.iter_errors(v["record"])], P.rule_errors(v["record"], at, arrs)) for v in valid
            if list(V.iter_errors(v["record"])) or P.rule_errors(v["record"], at, arrs)])
    KIND_DEF = {"pv_arrangement": "arrangement", "pv_observation": "observation", "pv_disposition": "disposition", "practitioner_standing": "standing"}

    def invalid_bad():
        bad = []
        for v in invalid:
            schema_errs = def_errors(schema, KIND_DEF[v["record"]["record_kind"]], v["record"])  # its own kind's $def (RV2 PV1-R7)
            rule_errs = P.rule_errors(v["record"], at, arrs)
            if v["refused_by"] == "schema" and not schema_errs:
                bad.append(v["why"])
            if v["refused_by"].startswith("rule"):
                code = v["refused_by"].split()[1]
                if schema_errs or not any(e.startswith(code) for e in rule_errs):
                    bad.append(v["why"])  # a rule case must pass the schema and fail for its own rule
        return bad
    bad_inv = invalid_bad()
    expect("K-6 every invalid example is refused, each by what it names (its own kind's $def, or its own rule with the schema passing)", not bad_inv, bad_inv)
    expect("K-7 F-R12: no record kind has an outcome, verdict or score field",
           not fr12_errors(schema))

    def fr14():
        texts = [open(f, encoding="utf-8").read() for f in glob.glob(os.path.join(design, "*")) if not f.endswith("pv.examples.invalid.json")]
        # the invalid examples hold one deliberate F-R14 negative; every other invalid example must still be clean
        texts += [json.dumps(v["record"]) for v in invalid if not v["why"].startswith("F-R14")]
        texts += [open(f, encoding="utf-8").read() for f in glob.glob(os.path.join(HERE, "records", "*.json"))]
        return not any(P.fr14_violations(t) for t in texts)
    expect("K-8 F-R14: every OI-016 in DEL-09-12's Design files and records is qualified (the one deliberate F-R14 negative example excepted)", fr14)
    expect("K-9 F-R14 rule refuses an unqualified mention and accepts both qualified forms",
           lambda: P.fr14_violations("the period is OI-016.") and not P.fr14_violations("OI-016 (App v4) and SWBPIPE OI-016"))
    expect("K-10 F-R13 routing on the real ScopeLedger: V4-EXE-01 -> DEL-01-02; V4-EXM-41 -> DEL-09-12; SOW-209 -> DEL-09-12; method -> DEL-10-02; an unknown anchor -> unresolved",
           lambda: P.route(at, "V4-EXE-01", "feature") == (["DEL-01-02"], "scope_ledger")
           and P.route(at, "V4-EXM-41", "feature") == (["DEL-09-12"], "scope_ledger")
           and P.route(at, "SOW-209", "feature") == (["DEL-09-12"], "scope_ledger")
           and P.route(at, "anything", "method") == (["DEL-10-02"], "method_feedback_to_DEL-10-02")
           and P.route(at, "V4-NONEXISTENT-99", "feature") == (["unresolved"], "unresolved"))
    expect("K-11 the method note carries exactly DEL-10-02 UC §5's fields (read from UC at the commit), and nothing else",
           lambda: not method_note_errors(schema, at))
    expect("K-12 the standing hand-over has every field of DEL-11-03's first-cut $defs/practitioner_standing (at the commit) with its name and type, differs only as stated (format; added arrangement_ref, is_replacement_condition), and the record is valid against the first cut with those undone (PV1-R5)",
           lambda: not handover_errors(std, schema, at), handover_errors(std, schema, at))
    expect("K-13 no home path in the records or Design files",
           lambda: not any(re.search(r"/Users/|/home/", open(f, encoding="utf-8").read())
                           for f in glob.glob(os.path.join(HERE, "records", "*")) + glob.glob(os.path.join(design, "*"))))

    # --- Negatives: break a real record in memory; the named rule must refuse it (coordinator's audit) ---
    def neg(name, ok, rule):
        expect(name + " [refused by: %s]" % rule, ok)

    a = copy.deepcopy(arr)
    a["state"] = "agreed"
    neg("N-1 the real arrangement declared agreed with no agreement record (a plan offered as agreement)", def_errors(schema, "arrangement", a), "schema")
    agreement = {"actor": "the owner", "recorder": "HELP_HUMAN", "recorder_stated_by_record": True, "record_ref": "OWNER_DECISIONS_n.md (INVENTED)",
                 "exact_text": "INVENTED", "custody": "INVENTED"}
    a = copy.deepcopy(arr)
    a.update({"state": "agreed", "agreement": agreement, "period": {"kind": "one_for_both", "value": "INVENTED"}})
    a["expressions"][0].update({"availability": {"state": "available", "cause": "INVENTED"}, "material": "invented",
                                "candidate": {"app_candidate": {"revision": "INVENTED", "build_identity": "INVENTED"}},
                                "activities": [{"activity_id": "ACT-INVENTED", "description": "INVENTED", "selected_by": "proposed_not_selected"}]})
    neg("N-2 the real arrangement agreed (schema-valid) with an activity the owner did not select",
        not def_errors(schema, "arrangement", a) and any(e.startswith("PV-R2") for e in P.rule_errors(a, at)), "PV-R2 (schema passing)")
    s_ = copy.deepcopy(std)
    s_["observations"] = ["PV-OBS-INVENTED-1", "PV-OBS-INVENTED-2"]
    neg("N-3 the real standing with observations while not agreed", def_errors(schema, "standing", s_), "schema")
    s_ = copy.deepcopy(std)
    s_["agreement_ref"] = "INVENTED"
    neg("N-4 the real standing with an agreement while not agreed", def_errors(schema, "standing", s_), "schema")
    s_ = copy.deepcopy(std)
    s_["is_replacement_condition"] = True
    neg("N-5 practitioner validation made a replacement condition (F-R3)", def_errors(schema, "standing", s_) and state_errors(arr, s_), "schema, K-4")
    a = copy.deepcopy(arr)
    a["open_issue"] = "OI-016"
    neg("N-6 the real arrangement's open issue unqualified (F-R14)", def_errors(schema, "arrangement", a) and P.fr14_violations(json.dumps(a)), "schema, K-8")
    a = copy.deepcopy(arr)
    a["limits"] = a["limits"] + ["period pending OI-016."]
    neg("N-7 an unqualified OI-016 in a real record's text (F-R14)", P.fr14_violations(json.dumps(a)), "K-8")
    a = copy.deepcopy(arr)
    a["expressions"][1]["activities"] = [{"activity": "INVENTED", "selected_by": "proposed_not_selected"}]
    neg("N-8 an activity proposed in today's arrangement", state_errors(a, std), "K-4")
    sc = copy.deepcopy(schema)
    sc["$defs"]["observation"]["properties"]["score"] = {"type": "number"}
    neg("N-9 a score field added to the observation kind (F-R12)", fr12_errors(sc), "K-7")
    sc = copy.deepcopy(schema)
    sc["$defs"]["method_note"]["properties"]["severity"] = {"type": "string"}
    neg("N-10 a method-note field UC §5 does not have", method_note_errors(sc, at), "K-11")
    s_ = copy.deepcopy(std)
    s_["open_issue"] = "SWBPIPE OI-016"
    neg("N-11 the standing hand-over naming the other register's OI-016", handover_errors(s_, schema, at), "K-12")
    bad = dict(files)
    bad["PV-STANDING-1.json"] = files["PV-STANDING-1.json"].replace(b"not_agreed", b"agreed")
    neg("N-12 a record byte changed after the manifest was written", manifest_errors(bad, files["MANIFEST.sha256"].decode()), "K-2")
    built = P.build(at)
    built["PV-STANDING-1.json"] = dict(built["PV-STANDING-1.json"], observations=1)
    neg("N-13 a record that is not what the builder makes at the commit", built != rec, "K-3")

    # PV-v0.3 (RV2-PV1): each repaired rule broken on the real records, and PV-R4 both ways
    a = copy.deepcopy(arr)
    a["expressions"][1] = copy.deepcopy(a["expressions"][0])
    neg("N-15 RV2 probe A on the real arrangement: two 'app' expressions, no 'swbpipe' (PV1-R2)", def_errors(schema, "arrangement", a), "schema")
    a2 = copy.deepcopy(arr)
    a2.update({"state": "agreed", "agreement": agreement, "period": {"kind": "one_for_both", "value": "INVENTED"}})
    a2["expressions"][0]["availability"] = {"state": "available", "cause": "INVENTED"}
    neg("N-16 RV2 probe B on the real arrangement: agreed, an available expression with no candidate and no material (PV1-R3)",
        def_errors(schema, "arrangement", a2), "schema")
    s_ = dict(std, standing="in_use")
    neg("N-17 RV2 probe H on the real standing: in use with no agreement reference (PV1-R3)", def_errors(schema, "standing", s_), "schema")
    s_ = dict(std, observations=0)
    neg("N-18 the real standing with PV-v0.2's integer count, which DEL-11-03's first cut does not read (PV1-R5)",
        def_errors(schema, "standing", s_) and handover_errors(s_, schema, at), "schema, K-12")
    sc = copy.deepcopy(schema)
    sc["$defs"]["standing"]["properties"]["validated"] = {"type": "boolean"}
    neg("N-19 a hand-over field the stated differences do not list", handover_errors(std, sc, at), "K-12")
    # PV-R4: an in-memory agreed arrangement with an identified-looking candidate (INVENTED; never written to disk)
    real_c = {"app_candidate": {"revision": "a1b2c3d", "build_identity": "4.0.0+a1b2c3d"}}
    ag = copy.deepcopy(arr)
    ag.update({"arrangement_id": "PV-ARR-9", "state": "agreed", "agreement": agreement, "period": {"kind": "one_for_both", "value": "INVENTED"}})
    ag["expressions"][0].update({"availability": {"state": "available", "cause": "INVENTED"}, "material": "invented", "candidate": real_c,
                                 "activities": [{"activity_id": "ACT-9", "description": "INVENTED", "selected_by": "the owner"}]})
    ob = copy.deepcopy([v["record"] for v in valid if v["record"].get("observation_id") == "PV-OBS-EX-1"][0])
    ob.update({"standing": "actual_use", "arrangement_ref": "PV-ARR-9 v1", "activity_id": "ACT-9", "candidate": copy.deepcopy(real_c)})
    ctx = dict(arrs, **{"PV-ARR-9 v1": ag})
    neg("P-1 positive control: actual use under an agreed arrangement, on an owner-selected activity, on that expression's candidate",
        not def_errors(schema, "observation", ob) and not def_errors(schema, "arrangement", ag) and not P.rule_errors(ob, at, ctx), "none")

    def r4(mut_arr=None, mut_obs=None):
        a_, o_ = copy.deepcopy(ag), copy.deepcopy(ob)
        (mut_arr or (lambda x: None))(a_)
        (mut_obs or (lambda x: None))(o_)
        return [e for e in P.rule_errors(o_, at, dict(arrs, **{"PV-ARR-9 v1": a_})) if e.startswith("PV-R4")]
    neg("N-20 the same under a proposed (not agreed) arrangement", r4(lambda a_: a_.update(state="proposed", agreement=None, period=None)), "PV-R4")
    neg("N-21 the same on an activity the owner did not select", r4(mut_obs=lambda o_: o_.update(activity_id="ACT-NOWHERE")), "PV-R4")
    neg("N-22 the same on another candidate", r4(mut_obs=lambda o_: o_.update(candidate={"app_candidate": {"revision": "ffff", "build_identity": "other"}})), "PV-R4")
    neg("N-23 the same naming an arrangement that is not supplied", r4(mut_obs=lambda o_: o_.update(arrangement_ref="PV-ARR-77 v1")), "PV-R4")
    neg("N-24 RV2 probe C on the real PV-ARR-1 (not agreed; activity in no arrangement)",
        [e for e in P.rule_errors(dict(ob, arrangement_ref="PV-ARR-1 v1", activity_id="ACT-NOWHERE"), at, arrs) if e.startswith("PV-R4")], "PV-R4")

    neg("N-14 a home path in a record", re.search(r"/Users/|/home/", json.dumps(dict(std, limits=["see /" + "Users/someone/notes"]))), "K-13")

    for name, ok, detail in results:
        print(("HOLDS " if ok else "FAILS ") + name + ("" if ok or not detail else "  -> %s" % (detail,)))
    failed = sum(1 for _, ok, _ in results if not ok)
    print("%d/%d expectations held (examples: %d valid, %d invalid)" % (len(results) - failed, len(results), len(valid), len(invalid)))
    raise SystemExit(1 if failed else 0)


if __name__ == "__main__":
    main()
