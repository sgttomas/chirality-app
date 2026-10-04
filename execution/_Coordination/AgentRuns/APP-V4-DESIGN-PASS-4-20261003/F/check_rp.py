"""Check an EU-F1 fixture and the replacement packet rules (RP-v0.4). Prototype, not product code.

Part A: the fixture as written (integrity, schemas, copies equal their vendored sources, rules recomputed,
thesis identity, terms, excerpts, receipts, points of need, evidence before status, legend, vendoring).
Part B: rule cases RP-R1...RP-R7, positive and negative, on in-memory variants of supplier records.
Reads only; writes nothing.

Usage: python3 -B check_rp.py [--fixture FX-RP1-4]

Run with --fixture FX-RP1, FX-RP1-2 or FX-RP1-3 to reproduce which current checks the earlier fixtures
fail (RV3 N4). Part B does not depend on the fixture.
"""

import copy
import glob
import json
import os
import subprocess
import sys

import rplib as L
import build_fx_rp1 as BUILD  # TERMS, CODE_RE, EXCERPTS, reader_texts; importing runs nothing

HERE = os.path.dirname(os.path.abspath(__file__))
ARGS = sys.argv[1:]
FX_NAME = ARGS[1] if ARGS[:1] == ["--fixture"] else "FX-RP1-4"
FX = os.path.join(HERE, "fixtures", FX_NAME)
REPO = os.path.normpath(os.path.join(L.EXEC_ROOT, "..", "..", ".."))
results, notices = [], []


def expect(name, fn, detail=""):
    try:
        ok = bool(fn() if callable(fn) else fn)
        err = ""
    except Exception as exc:  # a check that cannot run on this fixture fails, with its reason
        ok, err = False, "%s: %s" % (type(exc).__name__, exc)
    results.append((name, ok, detail if not ok and detail else err))


def fx(rel):
    with open(os.path.join(FX, rel), encoding="utf-8") as fh:
        return json.load(fh)


def one(pattern):
    found = glob.glob(os.path.join(FX, pattern))
    if len(found) != 1:
        raise FileNotFoundError(pattern)
    return os.path.relpath(found[0], FX)


def resolved_for(record, run_basis="candidate"):
    out = {}
    for scn in record["scenarios"]:
        for st in scn["steps"]:
            if "result_record" in st:
                out[st["result_record"]] = {"run_basis": run_basis, "outcome": st["outcome"]}
    return out


def part_a():
    listed = {}
    for line in open(os.path.join(FX, "MANIFEST.sha256"), encoding="utf-8"):
        h, p = line.rstrip("\n").split("  ", 1)
        listed[p] = h
    actual = {}
    for root, _, names in os.walk(FX):
        for n in names:
            if n != "MANIFEST.sha256":
                p = os.path.join(root, n)
                actual[os.path.relpath(p, FX)] = L.sha256_file(p)
    expect("A-1 every fixture file is listed in MANIFEST.sha256 with its sha256, and nothing else", listed == actual)

    mp, pp, dp = one("packet/*.packet-manifest.json"), one("package/*.json"), one("records/*.json")
    m, pkg, disp = fx(mp), fx(pp), fx(dp)
    m_sha, p_sha = actual[mp], actual[pp]
    expect("A-2 packet manifest valid against the current rp.packet-manifest.schema.json",
           lambda: not L.errors(L.file_validator("rp_manifest_schema"), m), L.errors(L.file_validator("rp_manifest_schema"), m)[:3])
    expect("A-3 package valid against DEL-02-03 $defs/decisionPackageFile and RP-R6 (with the manifest)", lambda: not L.check_package(pkg, m_sha, m),
           L.check_package(pkg, m_sha, m))
    expect("A-4 disposition valid against rp.disposition.schema.json and RP-R7", lambda: not L.check_disposition(disp, pkg, p_sha))
    expect("A-5 candidate subject valid against DEL-09-01 EXP $defs/candidate_subject (R23-33)",
           lambda: not L.errors(L.def_validator("exp_result_schema", "candidate_subject"), m["candidate"]["subject"]))
    sup = {s["item_id"]: s for s in m["supplied"]}
    expect("A-6 every supplied item's sha256 in the manifest equals the file",
           lambda: all(actual.get(s["path"]) == s["sha256"] for s in m["supplied"]))
    own = {"sq_dossier": lambda: L.file_validator("sq_schema"), "lhq_dossier_manifest": lambda: L.file_validator("lhq_manifest_schema"),
           "lhq_cir": lambda: L.file_validator("lhq_cir_schema"),
           "continuity_input_first_cut": lambda: L.def_validator("rp_manifest_schema", "continuity_input"),
           "continuity_input": lambda: L.def_validator("ca_schema", "continuity_handoff"),
           "practitioner_standing": lambda: L.def_validator("rp_manifest_schema", "practitioner_standing")}
    expect("A-7 every supplied item is valid against its owner's schema (vendored) or the first-cut $def",
           lambda: not [s["item_id"] for s in m["supplied"]
                        if L.errors(own[s["role"] + ("_first_cut" if s["role"] == "continuity_input" and s["source_kind"] == "shape_only" else "")](), fx(s["path"]))])

    def copies_equal():
        for s in m["supplied"]:
            if s["source_kind"] != "copied_record":
                continue
            key = [k for k, v in L.PATHS.items() if v == s["source"]["path"]][0]
            src = L.load(key)
            idf = "dossier_id" if s["role"] == "lhq_dossier_manifest" else "record_id"
            rec = [r for r in src if r.get(idf) == s["source"]["record_id"]] if isinstance(src, list) else [src]
            if not (rec and rec[0] == fx(s["path"]) and L.sha256_file(L.abspath(key)) == s["source"]["sha256"]):
                return False
        return True
    expect("A-8 each copied supplier record equals its record in the vendored source, at the sha256 named", copies_equal)

    def recompute():
        sq, dos, cir = fx(sup["S-1"]["path"]), fx(sup["S-2"]["path"]), fx(sup["S-3"]["path"])
        cl, jr = L.core_loop(sq), L.journey(dos)
        subj, why = L.map_cir_candidate(cir)
        rec = L.reconcile(L.map_sq_candidate(sq["candidate"]), subj, why)
        jr = dict(jr, source_item="S-2", cir_item="S-3")
        if "host_contributions" in m["journey"]:
            jr["host_contributions"] = L.host_contributions(cir)
        return (dict(cl, source_item="S-1") == m["core_loop"] and jr == m["journey"]
                and rec == m["candidate"]["reconciliation"] and L.replacement_evidence_complete(cl, jr, rec) == m["replacement_evidence"])
    expect("A-9 RP-R1...RP-R4 recomputed from the supplied copies equal the manifest", recompute)

    def thesis():
        h = fx(sup["S-4"]["path"])
        cont = h["thesis_check"]
        at = cont.get("at_commit") or h["at_commit"]  # first cut (RP-v0.1-3) or DEL-11-01's CA hand-over (RP-v0.4)
        expected = cont.get("expected_tree") or cont["expected"]
        observed = (cont.get("observed_tree") or cont["observed"]).split()[0]
        tree = subprocess.run(["git", "-C", REPO, "rev-parse", at + ":projects/chirality-app-v4/foundation/thesis"],
                              capture_output=True, text=True).stdout.strip()
        return tree == expected == observed == "47fc49e96c2931ba18090f1a82d56a49f230b3ee"
    expect("A-10 thesis tree at the recorded commit equals docs/PRD.md §11's tree", thesis)
    expect("A-11 all six never-established items are listed; disposition not_presented; no decision element",
           lambda: set(m["not_established"]) == {"replacement_decision", "public_release", "retirement", "professional_reliance",
                                                 "consumer_adoption", "practitioner_validation"}
           and disp["state"] == "not_presented" and "decision" not in disp)
    expect("A-12 practitioner validation is not a replacement condition and is not listed as a gap",
           lambda: m["practitioner"]["is_replacement_condition"] is False
           and not any("DEL-09-12" in g["supplier"] or "practitioner" in g["what"].lower() for g in m["gaps"]))
    expect("A-13 every code in the package, packet, disposition, excerpts and legend has a term in the packet",
           lambda: not BUILD.undefined_codes([pkg, m, disp], BUILD.reader_texts(FX)) and m["terms"] == BUILD.TERMS,
           sorted(BUILD.undefined_codes([pkg, m, disp], BUILD.reader_texts(FX))) if os.path.isdir(FX) else "")

    def excerpts():
        ok = actual.get(m["basis_excerpts"]["path"]) == m["basis_excerpts"]["sha256"]
        text = open(os.path.join(FX, m["basis_excerpts"]["path"]), encoding="utf-8").read()
        for rel, a, b, _ in BUILD.EXCERPTS:
            path = L.abspath(rel)
            lines = open(path, encoding="utf-8").read().split("\n")[a - 1:b]
            ok = ok and ("sha256 %s" % L.sha256_file(path)) in text and "\n".join(lines) in text
        return ok
    expect("A-14 basis excerpts: listed sha256 holds; each equals its source lines at the source's current sha256", excerpts)

    def receipts():
        dos = fx(sup["S-2"]["path"])
        refs = {r["ref"] for r in dos["handoff_del_11_03"]["receipts"]} | {e["ref"] for e in dos.get("host_evidence", []) if e["kind"] == "host_receipt"} \
            | {r["ref"] for r in (dos.get("handoff_del_09_11") or {}).get("receipt_refs", [])}
        got = {r["ref"] for r in m["journey"]["receipts"]["in_handoff"] + m["journey"]["receipts"]["elsewhere_in_dossier"]}
        return refs == got and m["journey"]["receipts"]["total_distinct"] == len(refs)
    expect("A-15 every receipt reference anywhere in the supplied dossier is in the packet, kept apart by where it appears", receipts)

    def points():
        for g in m["gaps"]:
            pn = g["point_of_need"]
            if "presented" in pn and "does not hold back putting the packet to the owner" not in pn:
                return False  # no presentation gate, either way (R23-43)
            if "presentation is not gated" in pn:
                return False  # RP-v0.2's attribution to AX-001, which AX-001 does not state
            if pn.startswith("before the packet can claim replacement qualification") and \
                    "cannot claim replacement qualification until both applicable witnesses hold" not in pn:
                return False  # cites AX-001 in its own words
        return True
    expect("A-16 points of need gate only the qualification claim, quoting AX-001's own words; none gates presentation (R23-43)", points)

    def evidence_first():
        for e in m["core_loop"]["elements"]:
            if e["status"] == "met" and not (e["evidence_resolved"] and e["recorded"] == "recorded_pass"):
                return False
            if e["status"] == "not_met" and not any(s.get("resolved") and s.get("outcome") == "fail" for s in e["steps"]):
                return False
        return True
    expect("A-17 met needs every counted step resolved and passed; not_met needs a resolved fail (RP-R1)", evidence_first)
    expect("A-18 the fixture carries its legend, equal to the current Design schemas",
           lambda: all(actual.get("legend/" + n) == L.sha256_file(L.abspath(L.PATHS["rp_manifest_schema"].replace("rp.packet-manifest.schema.json", n)))
                       for n in ("rp.packet-manifest.schema.json", "rp.disposition.schema.json")))
    expect("A-19 the package states the choice as the owner's act on the evidence as presented, and claims qualification only if complete (R23-43)",
           lambda: L.CHOICE_SENTENCE in pkg["purpose"]
           and (("it claims replacement qualification" in pkg["purpose"]) == m["replacement_evidence"]["complete"]))
    expect("A-20 an unidentified, illustrative candidate is only ever in a fixture, and the purpose opens with the fixture notice (RV3 Addendum 4)",
           lambda: m["fixture"] is True and m["candidate"]["identified"] is False and pkg["purpose"].startswith(L.FIXTURE_NOTICE))
    expect("A-21 the continuity input is DEL-11-01's own CA hand-over, not a first cut, and the packet repeats its results",
           lambda: sup["S-4"]["source_kind"] == "copied_record" and sup["S-4"]["standing"] == "owner_record"
           and m["continuity"]["thesis_identity"] == fx(sup["S-4"]["path"])["thesis_check"]["result"]
           and m["continuity"]["archives_verify"] == fx(sup["S-4"]["path"])["archives"]["verify"])
    return {"m": m, "pkg": pkg, "disp": disp, "m_sha": m_sha, "p_sha": p_sha}


def vendoring():
    v = json.load(open(os.path.join(HERE, "vendor", "VENDOR.json"), encoding="utf-8"))
    ok = all(L.sha256_file(os.path.join(HERE, f["vendored"])) == f["sha256"] for f in v["files"])
    expect("V-1 every vendored supplier file equals the sha256 recorded at vendoring (R23-44)", ok)
    for f in v["files"]:
        live = L.live_path(f["key"])
        now = L.sha256_file(live) if os.path.exists(live) else "missing"
        if now != f["sha256"]:
            notices.append("NOTICE the live supplier file for %s has moved since vendoring (%s -> %s); re-pin deliberately (R23-21)"
                           % (f["key"], f["sha256"][:12], now[:12]))


def part_b(ctx):
    ex = {r["record_id"]: r for r in L.load("sq_examples")}
    allpass, jfail, sq05 = ex["SQ-EX-03"], ex["SQ-EX-04"], ex["SQ-EX-05"]
    res = resolved_for(allpass)

    cl = L.core_loop(allpass)
    expect("B-1 all counted steps recorded pass but unresolved -> every element recorded_pass yet not_evidenced",
           all(e["recorded"] == "recorded_pass" and e["status"] == "not_evidenced" for e in cl["elements"])
           and cl["obligation"] == "not_evidenced" and not cl["established"])
    reviews = {allpass["examiner"]["review_record"]: {"resolved": True}}
    expect("B-2 positive control: every result resolved to a candidate record and the review resolved -> all met; established",
           L.core_loop(allpass, res, reviews)["obligation"] == "met" and L.core_loop(allpass, res, reviews)["established"])
    half = dict(res)
    half["EXP-S11-1 (ILLUSTRATIVE)"] = dict(half["EXP-S11-1 (ILLUSTRATIVE)"], run_basis="rehearsal")
    r = L.core_loop(allpass, half, reviews)
    expect("B-3 one result resolved to a rehearsal record -> that element not_evidenced; not established (EXP-R3)",
           [e["status"] for e in r["elements"] if e["element"] == "interruption"] == ["not_evidenced"] and not r["established"])
    r = L.core_loop(sq05, resolved_for(sq05), reviews)
    rs = [e for e in r["elements"] if e["element"] == "restart"][0]
    expect("B-4 S11-6 blocked, resolved to a candidate record -> restart recorded_blocked and not_evidenced, NOT not_met (RV3 EUF1-R1b)",
           rs["recorded"] == "recorded_blocked" and rs["status"] == "not_evidenced" and r["obligation"] == "not_evidenced"
           and "not a failure" in rs["status_reason"] and "U-SQ-5" in rs["status_reason"])
    v = copy.deepcopy(sq05)
    [s for s in v["scenarios"][1]["steps"] if s["step"] == "S11-6"][0]["outcome"] = "fail"
    r = L.core_loop(v, resolved_for(v), reviews)
    expect("B-5 the same step recorded fail on a candidate record -> restart not_met; obligation not_met",
           [e["status"] for e in r["elements"] if e["element"] == "restart"] == ["not_met"] and r["obligation"] == "not_met")
    for outcome in ("not-run", "inconclusive"):
        [s for s in v["scenarios"][1]["steps"] if s["step"] == "S11-6"][0]["outcome"] = outcome
        r = L.core_loop(v, resolved_for(v), reviews)
        expect("B-6 S11-6 %s on a candidate record -> restart not_evidenced, recorded_%s" % (outcome, outcome.replace("-", "_")),
               [(e["status"], e["recorded"]) for e in r["elements"] if e["element"] == "restart"] == [("not_evidenced", "recorded_" + outcome.replace("-", "_"))])
    v = copy.deepcopy(allpass)
    v["scenarios"][1]["steps"] = [s for s in v["scenarios"][1]["steps"] if s["core_loop_element"] != "restart"]
    r = L.core_loop(v, res, reviews)
    expect("B-7 no counted restart step -> restart not_recorded, not_evidenced; obligation not met",
           [(e["recorded"], e["status"]) for e in r["elements"] if e["element"] == "restart"] == [("not_recorded", "not_evidenced")]
           and r["obligation"] != "met")
    v = copy.deepcopy(allpass)
    v["scenarios"][1]["steps"][0]["core_loop_element"] = "model access"
    expect("B-8 a V4-EXM-11 step outside the seven elements -> interface error; never established",
           L.core_loop(v, res, reviews)["interface_errors"] and not L.core_loop(v, res, reviews)["established"])
    r = L.core_loop(jfail, resolved_for(jfail), reviews)
    expect("B-9 an uncounted step that failed (J-8R) changes no element; its dossier reason is carried",
           r["obligation"] == "met" and any(u["step"] == "J-8R" and u["outcome"] == "fail" and "TT-7" in u["dossier_reason"]
                                             for u in r["uncounted_steps"]))
    v = copy.deepcopy(allpass)
    v["handoff"]["handed_over"] = False
    expect("B-10 dossier not handed over -> not established", not L.core_loop(v, res, reviews)["established"])
    expect("B-11 V4-EXM-12 steps are outside the core loop (EXAMINATION §7)",
           [o["scenario"] for o in L.core_loop(allpass)["outside_core_loop"]] == ["V4-EXM-12"])
    expect("B-12 an illustrative review record is named_not_resolved, never present (RR-EUF2); resolved -> present",
           L.core_loop(sq05)["dossier_review"]["state"] == "named_not_resolved"
           and "dossier_review_not_resolved" in L.core_loop(allpass, res)["not_established_because"]
           and L.core_loop(allpass, res, reviews)["dossier_review"]["state"] == "present")

    # Journey (RP-R2), on O-C's repaired DOS examples
    dosx = {r["dossier_id"]: r for r in L.load("lhq_manifest_examples")}
    pop, plain = dosx["DOS-EXAMPLE-INVENTED-POPULATED"], dosx["DOS-EXAMPLE-INVENTED"]
    r = L.journey(pop)
    expect("B-13 DOS-EXAMPLE-INVENTED-POPULATED: RC-1 in the handoff, the index and the DEL-09-11 handoff -> one receipt, in the handoff; no missing-receipt reason",
           [x["ref"] for x in r["receipts"]["in_handoff"]] == ["RC-1 (invented)"] and not r["receipts"]["elsewhere_in_dossier"]
           and r["receipts"]["total_distinct"] == 1 and "receipts_in_dossier_missing_from_handoff" not in r["not_established_because"])
    v = copy.deepcopy(pop)
    v["handoff_del_11_03"]["receipts"] = []
    r = L.journey(v)
    expect("B-14 the same record with RC-1 dropped from the DEL-11-03 handoff -> listed elsewhere; not established (EUF1-D2)",
           {x["where"] for x in r["receipts"]["elsewhere_in_dossier"]} == {"host_evidence"} and "receipts_in_dossier_missing_from_handoff" in r["not_established_because"])
    expect("B-15 repaired DOS-EXAMPLE-INVENTED names no receipt anywhere -> zero receipts, no missing-receipt reason",
           L.journey(plain)["receipts"]["total_distinct"] == 0 and "receipts_in_dossier_missing_from_handoff" not in L.journey(plain)["not_established_because"])
    good = copy.deepcopy(pop)
    good["handoff_del_11_03"].update({"counts_as_completed_witness": True,
                                      "acceptance_acts": [{"record_ref": "ACT-1", "actor": "the person", "recorder": "host recorder"}]})
    good["independent_review_ref"] = "EXP-RX-LHQ"
    jres = {good["handoff_del_11_03"]["p20a_result_ref"]: {"run_basis": "candidate", "outcome": "pass"}}
    expect("B-16 positive control: counted P20-A, an acceptance act, review, candidate pass, receipts in the handoff -> established",
           L.journey(good, jres)["established"], L.journey(good, jres)["not_established_because"])
    v = copy.deepcopy(good)
    v["handoff_del_11_03"]["acceptance_acts"][0]["recorder"] = "the person"
    expect("B-17 acceptance act with actor = recorder -> incomplete", L.journey(v, jres)["status"] == "incomplete")
    v = copy.deepcopy(good)
    del v["independent_review_ref"]
    expect("B-18 no independent review record -> incomplete (DOS §1)", L.journey(v, jres)["status"] == "incomplete")

    # Candidate (R23-33; LHQ-v0.2 CI-5)
    cirs = {r["record_id"]: r for r in L.load("lhq_cir_examples")}
    mapped = cirs["LHQ-CIR-EXAMPLE-MAPPED (invented)"]
    expect("B-19 LHQ-v0.2's mapped CIR example is valid against the vendored LHQ CIR schema",
           not L.errors(L.file_validator("lhq_cir_schema"), mapped))
    cs, why = L.map_cir_candidate(mapped)
    expect("B-20 it maps to a valid EXP candidate_subject", why == "mapped"
           and not L.errors(L.def_validator("exp_result_schema", "candidate_subject"), cs))
    sq_subj = L.map_sq_candidate(allpass["candidate"])
    expect("B-21 illustrative SQ candidate vs the mapped CIR, no change-impact record -> differ", L.reconcile(sq_subj, cs, why) == "differ")
    m = mapped["app_candidate_subject"]
    same = L.map_sq_candidate({"revision": m["revision"], "build_identity": m["build_identity"], "codex_pin": "0.158.0",
                               "package_record": m["package_record"]})
    expect("B-22 SQ candidate with the same identity -> reconciled", L.reconcile(same, cs, why) == "reconciled")
    expect("B-23 differing identity with an EXP change-impact record named -> reconciled_by_applicability",
           L.reconcile(sq_subj, cs, why, ["EXP-CI-1"]) == "reconciled_by_applicability")
    unpack = copy.deepcopy(mapped)
    unpack["app_candidate_subject"] = {"revision": "r1", "build_identity": "b1"}
    cu, wu = L.map_cir_candidate(unpack)
    sq_r1 = L.map_sq_candidate({"revision": "r1", "build_identity": "b1", "codex_pin": "0.158.0"})
    expect("B-24 CIR omitting `packaged` vs SQ's explicit unpackaged candidate -> reconciled (EXP identity semantics; RV3 EUF1-R4)",
           not L.errors(L.file_validator("lhq_cir_schema"), unpack) and L.reconcile(sq_r1, cu, wu) == "reconciled")
    pk = copy.deepcopy(unpack)
    pk["app_candidate_subject"].update({"packaged": True, "package_record": "PKG-REC-9"})
    cp, wp = L.map_cir_candidate(pk)
    expect("B-25 packaged vs unpackaged with the same revision and build -> differ", L.reconcile(sq_r1, cp, wp) == "differ")
    sq_pk = L.map_sq_candidate({"revision": "r1", "build_identity": "b1", "codex_pin": "0.158.0", "package_record": "PKG-REC-8"})
    expect("B-26 both packaged, different package records -> differ", L.reconcile(sq_pk, cp, wp) == "differ")
    v = copy.deepcopy(mapped)
    del v["app_candidate_subject"]
    expect("B-27 a supplied App candidate without CI-5's mapping (one string) -> not mappable",
           L.map_cir_candidate(v) == (None, "not_mappable_single_string"))

    # Completeness (RP-R4, RP-R5)
    clp, jrp = L.core_loop(allpass, res, reviews), L.journey(good, jres)
    expect("B-28 both established and reconciled -> complete; practitioner standing not consulted",
           L.replacement_evidence_complete(clp, jrp, "reconciled")["complete"])
    expect("B-29 journey not established -> never complete", not L.replacement_evidence_complete(clp, L.journey(plain), "reconciled")["complete"])
    expect("B-30 candidates differ -> never complete", not L.replacement_evidence_complete(clp, jrp, "differ")["complete"])

    # Package (RP-R6)
    pkg, disp, m_sha, p_sha = ctx["pkg"], ctx["disp"], ctx["m_sha"], ctx["p_sha"]
    v = copy.deepcopy(pkg)
    v["requester"] = "O-F"
    expect("B-31 a recorder element in the package file is refused (R23-24)", L.check_package(v, m_sha))
    v = copy.deepcopy(pkg)
    v["alternatives"] = [a for a in v["alternatives"] if a["id"] != "ALT-PUBLISHED"]
    expect("B-32 a package without ALT-PUBLISHED is refused (F-R5)", L.check_package(v, m_sha))
    v = copy.deepcopy(pkg)
    v["subject"][1] = "packet manifest sha256:" + "0" * 64
    expect("B-33 a package bound to another manifest is refused", L.check_package(v, m_sha))
    v = copy.deepcopy(pkg)
    v["alternatives"][2]["consequences"] = ["v3.0.1 remains the fallback", "old projects are retired"]
    expect("B-34 an alternative that does not state it retires nothing is refused", L.check_package(v, m_sha))
    v = copy.deepcopy(pkg)
    v["alternatives"][1]["consequences"] = ["v3.0.1 is no longer the fallback for the published product",
                                            "This is also a public-release act, which the owner decides separately", "No retirement: nothing"]
    expect("B-35 RP-v0.2's ALT-PUBLISHED wording (release act unclear) is refused (RV3 EUF1-R2)",
           any("does not perform the public-release act" in e for e in L.check_package(v, m_sha)))
    v = copy.deepcopy(pkg)
    v["purpose"] = v["purpose"].replace(L.CHOICE_SENTENCE, "The owner chooses")
    expect("B-36 a purpose without 'the owner's act, on the evidence as presented' is refused (R23-43)",
           any("evidence as presented" in e for e in L.check_package(v, m_sha)))

    m = ctx["m"]
    v = copy.deepcopy(m)
    v["fixture"] = False
    expect("B-45 the same illustrative packet presented as a real one (not a fixture) is refused (RV3 Addendum 4)",
           any("refused in a packet that is not a fixture" in e for e in L.check_package(pkg, m_sha, v)))
    v = copy.deepcopy(pkg)
    pub = [a for a in v["alternatives"] if a["id"] == "ALT-PUBLISHED"][0]
    pub["consequences"] = [c.replace("manual update check", "update check").replace("on request ", "") for c in pub["consequences"]]
    expect("B-46 ALT-PUBLISHED's inference without 'manual' and 'on request' is refused (RV3 Addendum 4)",
           any("drops 'manual' or 'on request'" in e for e in L.check_package(v, m_sha, m)))
    real = copy.deepcopy(m)
    real.update({"fixture": False, "evidence_standing": "candidate"})
    real["candidate"]["identified"] = True
    v = copy.deepcopy(pkg)
    v["purpose"] = v["purpose"][v["purpose"].index("The owner decides"):]
    expect("B-47 positive control: an identified candidate in a real packet needs no fixture notice",
           not [e for e in L.check_package(v, m_sha, real) if "fixture" in e])

    # Disposition (RP-R7)
    dec = copy.deepcopy(disp)
    dec.pop("not_presented_because")
    dec.update({"state": "decided", "fallback_status": "per the chosen alternative",
                "presented": {"when": "2026-10-05", "by": "HELP_HUMAN", "how": "chat"},
                "decision": {"chosen_alternative": "ALT-DEFER", "actor": "the owner", "recorder": "HELP_HUMAN",
                             "record_ref": "OWNER_DECISIONS_n.md (INVENTED)", "exact_text": "INVENTED",
                             "custody": "the owner's chat message, transcribed by the recorder; no platform timestamp",
                             "act_time": {"available": False}}})
    expect("B-37 positive control: an invented decided record with an act reference is accepted by the rules",
           not L.check_disposition(dec, pkg, p_sha), L.check_disposition(dec, pkg, p_sha))
    v = copy.deepcopy(dec)
    del v["decision"]
    expect("B-38 decided without the owner's act -> refused", L.check_disposition(v, pkg, p_sha))
    v = copy.deepcopy(dec)
    v["decision"]["recorder"] = "the owner"
    expect("B-39 actor equals recorder -> refused", L.check_disposition(v, pkg, p_sha))
    v = copy.deepcopy(dec)
    v["decision"]["chosen_alternative"] = "ALT-REPLACE-ALL"
    expect("B-40 an alternative the package does not name -> refused", L.check_disposition(v, pkg, p_sha))
    expect("B-41 package changed after the decision -> lapsed", L.check_disposition(dec, pkg, "1" * 64))
    v = copy.deepcopy(disp)
    v["fallback_status"] = "v4 in use"
    expect("B-42 an undecided disposition that drops v3.0.1 as the fallback -> refused", L.check_disposition(v, pkg, p_sha))
    v = copy.deepcopy(dec)
    v["decision"]["act_time"] = {"available": False, "value": "2026-10-05T10:00Z"}
    expect("B-43 an act time stated as unavailable yet given a value -> refused", L.check_disposition(v, pkg, p_sha))
    v = copy.deepcopy(disp)
    v.update({"state": "presented_no_decision", "presented": {"when": "x", "by": "y", "how": "z"}})
    v.pop("not_presented_because")
    v["decision"] = dec["decision"]
    expect("B-44 a decision element on a presented-but-undecided record -> refused", L.check_disposition(v, pkg, p_sha))


def main():
    print("fixture %s" % FX_NAME)
    ctx = part_a()
    vendoring()
    if FX_NAME == "FX-RP1-4":
        part_b(ctx)
    for name, ok, detail in results:
        print(("HOLDS " if ok else "FAILS ") + name + ("" if ok or not detail else "  -> %s" % (detail,)))
    for n in notices:
        print(n)
    failed = sum(1 for _, ok, _ in results if not ok)
    print("%d/%d expectations held" % (len(results) - failed, len(results)))
    raise SystemExit(1 if failed else 0)


if __name__ == "__main__":
    main()
