"""Check FX-RP1-2 and the replacement packet rules (EU-F1, RP-v0.2). Prototype, not product code.

Part A: the fixture as written (integrity, schemas, copies equal their sources, rules recomputed equal).
Part B: rule cases RP-R1...RP-R7, positive and negative, on in-memory variants of the supplied records.
Reads only; writes nothing. Usage: python3 -B check_rp.py
"""

import copy
import json
import os
import subprocess

import rplib as L

HERE = os.path.dirname(os.path.abspath(__file__))
FX = os.path.join(HERE, "fixtures", "FX-RP1-2")
import build_fx_rp1 as BUILD  # TERMS, CODE_RE, EXCERPTS; importing runs nothing
REPO = os.path.normpath(os.path.join(L.EXEC_ROOT, "..", "..", ".."))
results = []


def expect(name, ok, detail=""):
    results.append((name, bool(ok), detail))


def fx(rel):
    with open(os.path.join(FX, rel), encoding="utf-8") as fh:
        return json.load(fh)


def part_a():
    # A-1 manifest integrity
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

    m = fx("packet/RP-FX-RP1.v2.packet-manifest.json")
    pkg = fx("package/PKG-REPLACEMENT-FX-RP1-2.json")
    disp = fx("records/RPD-FX-RP1-2.disposition.json")
    m_sha = actual["packet/RP-FX-RP1.v2.packet-manifest.json"]
    p_sha = actual["package/PKG-REPLACEMENT-FX-RP1-2.json"]

    # A-2 schemas
    expect("A-2 packet manifest valid against rp.packet-manifest.schema.json",
           not L.errors(L.file_validator("rp_manifest_schema"), m), L.errors(L.file_validator("rp_manifest_schema"), m))
    expect("A-3 package valid against DEL-02-03 $defs/decisionPackageFile and RP-R6", not L.check_package(pkg, m_sha),
           L.check_package(pkg, m_sha))
    expect("A-4 disposition valid against rp.disposition.schema.json and RP-R7", not L.check_disposition(disp, pkg, p_sha),
           L.check_disposition(disp, pkg, p_sha))
    expect("A-5 candidate subject valid against DEL-09-01 EXP $defs/candidate_subject (R23-33)",
           not L.errors(L.def_validator("exp_result_schema", "candidate_subject"), m["candidate"]["subject"]))

    # A-6 supplied items: listed hash, own schema, equal to the source record
    sup = {s["item_id"]: s for s in m["supplied"]}
    ok_hash = all(actual.get(s["path"]) == s["sha256"] for s in m["supplied"])
    expect("A-6 every supplied item's sha256 in the manifest equals the file", ok_hash)
    own = {"sq_dossier": L.file_validator("sq_schema"), "lhq_dossier_manifest": L.file_validator("lhq_manifest_schema"),
           "lhq_cir": L.file_validator("lhq_cir_schema"),
           "continuity_input": L.def_validator("rp_manifest_schema", "continuity_input"),
           "practitioner_standing": L.def_validator("rp_manifest_schema", "practitioner_standing")}
    bad = [s["item_id"] for s in m["supplied"] if L.errors(own[s["role"]], fx(s["path"]))]
    expect("A-7 every supplied item is valid against its owner's schema (or the first-cut $def)", not bad, bad)
    eq = True
    for s in m["supplied"]:
        if s["standing"] != "illustrative":
            continue
        src = L.load(s["source"]["path"])
        idf = "dossier_id" if s["role"] == "lhq_dossier_manifest" else "record_id"
        rec = [r for r in src if r.get(idf) == s["source"]["record_id"]]
        eq = eq and rec and rec[0] == fx(s["path"]) and L.sha256_file(L.abspath(s["source"]["path"])) == s["source"]["sha256"]
    expect("A-8 each copied supplier record equals its record in the source file, at the source sha256 named", eq)

    # A-9 rules recomputed from the supplied copies equal what the manifest states
    sq, dos, cir = fx(sup["S-1"]["path"]), fx(sup["S-2"]["path"]), fx(sup["S-3"]["path"])
    cl, jr = L.core_loop(sq), L.journey(dos)
    subj, why = L.map_cir_candidate(cir)
    rec = L.reconcile(L.map_sq_candidate(sq["candidate"]), subj, why)
    same = (dict(cl, source_item="S-1") == m["core_loop"] and dict(jr, source_item="S-2", cir_item="S-3") == m["journey"]
            and rec == m["candidate"]["reconciliation"]
            and L.replacement_evidence_complete(cl, jr, rec) == m["replacement_evidence"])
    expect("A-9 RP-R1...RP-R4 recomputed from the supplied copies equal the manifest", same)

    # A-10 thesis identity re-observed at the recorded commit
    cont = fx(sup["S-4"]["path"])["thesis_check"]
    tree = subprocess.run(["git", "-C", REPO, "rev-parse", cont["at_commit"] + ":projects/chirality-app-v4/foundation/thesis"],
                          capture_output=True, text=True).stdout.strip()
    expect("A-10 thesis tree at the recorded commit equals docs/PRD.md §11's tree", tree == cont["expected_tree"] == cont["observed_tree"])

    # A-11 nothing establishes what the packet must never establish; no owner act
    expect("A-11 all six never-established items are listed; disposition is not_presented; no decision element",
           set(m["not_established"]) == {"replacement_decision", "public_release", "retirement", "professional_reliance",
                                         "consumer_adoption", "practitioner_validation"}
           and disp["state"] == "not_presented" and "decision" not in disp)
    expect("A-12 practitioner validation is not a replacement condition and is not listed as a gap",
           m["practitioner"]["is_replacement_condition"] is False
           and not any("DEL-09-12" in g["supplier"] or "practitioner" in g["what"].lower() for g in m["gaps"]))
    expect("A-13 every code in the package, packet and disposition has a term in the packet (RP-v0.2; reader I-1, I-6)",
           not BUILD.undefined_codes([pkg, m, disp]) and m["terms"] == BUILD.TERMS, sorted(BUILD.undefined_codes([pkg, m, disp])))
    ex_ok = actual.get(m["basis_excerpts"]["path"]) == m["basis_excerpts"]["sha256"]
    text = open(os.path.join(FX, m["basis_excerpts"]["path"]), encoding="utf-8").read()
    for rel, a, b, _ in BUILD.EXCERPTS:
        path = L.abspath(rel)
        lines = open(path, encoding="utf-8").read().split("\n")[a - 1:b]
        ex_ok = ex_ok and ("sha256 %s" % L.sha256_file(path)) in text and "\n".join(lines) in text
    expect("A-14 basis excerpts: listed sha256 holds; each excerpt equals its source lines at the source's current sha256 (reader I-7)", ex_ok)
    refs = {r["ref"] for r in dos["handoff_del_11_03"]["receipts"]} | {e["ref"] for e in dos.get("host_evidence", []) if e["kind"] == "host_receipt"} \
        | {r["ref"] for r in (dos.get("handoff_del_09_11") or {}).get("receipt_refs", [])}
    got = {r["ref"] for r in m["journey"]["receipts"]["in_handoff"] + m["journey"]["receipts"]["elsewhere_in_dossier"]}
    expect("A-15 every receipt reference anywhere in the supplied dossier is in the packet, kept apart by where it appears (finding EUF1-D2)",
           refs == got and m["journey"]["receipts"]["total_distinct"] == len(refs))
    expect("A-16 no gap's point of need gates presentation (DEL-11-03 AX-001; reader I-10)",
           not any("before the package is presented" in g["point_of_need"] for g in m["gaps"]))
    expect("A-17 no element is met or not_met unless its evidence resolved (RP-R1 repaired; finding EUF1-D1)",
           all(e["status"] == "not_evidenced" or e["evidence_resolved"] for e in m["core_loop"]["elements"]))
    return sq, dos, cir, pkg, disp, m_sha, p_sha


def resolved_for(record, run_basis="candidate"):
    out = {}
    for scn in record["scenarios"]:
        for st in scn["steps"]:
            if "result_record" in st:
                out[st["result_record"]] = {"run_basis": run_basis, "outcome": st["outcome"]}
    return out


def part_b(sq, dos, cir, pkg, disp, m_sha, p_sha):
    ex = {r["record_id"]: r for r in L.load("sq_examples")}
    allpass, jfail = ex["SQ-EX-03"], ex["SQ-EX-04"]

    cl = L.core_loop(allpass)
    expect("B-1 all counted steps recorded pass but unresolved -> every element recorded_pass yet not_evidenced; obligation not_evidenced (EUF1-D1)",
           all(e["recorded"] == "recorded_pass" and e["status"] == "not_evidenced" for e in cl["elements"])
           and cl["obligation"] == "not_evidenced" and not cl["established"])
    res = resolved_for(allpass)
    expect("B-2 positive control: every result resolved to a candidate record -> all met; established",
           L.core_loop(allpass, res)["obligation"] == "met" and L.core_loop(allpass, res)["established"])
    half = dict(res)
    half["EXP-S11-1 (ILLUSTRATIVE)"] = dict(half["EXP-S11-1 (ILLUSTRATIVE)"], run_basis="rehearsal")
    r = L.core_loop(allpass, half)
    expect("B-3 one result resolved to a rehearsal record -> that element not_evidenced; not established (EXP-R3)",
           [e["status"] for e in r["elements"] if e["element"] == "interruption"] == ["not_evidenced"] and not r["established"])
    r = L.core_loop(sq, resolved_for(sq))
    expect("B-4 resolved candidate record of S11-6 blocked -> restart not_met; obligation not_met",
           [e["status"] for e in r["elements"] if e["element"] == "restart"] == ["not_met"] and r["obligation"] == "not_met")
    expect("B-5 the same blocked record unresolved -> restart recorded_not_pass but not_evidenced (no claim either way)",
           [(e["recorded"], e["status"]) for e in L.core_loop(sq)["elements"] if e["element"] == "restart"] == [("recorded_not_pass", "not_evidenced")])
    v = copy.deepcopy(allpass)
    v["scenarios"][1]["steps"] = [s for s in v["scenarios"][1]["steps"] if s["core_loop_element"] != "restart"]
    r = L.core_loop(v, res)
    expect("B-6 no counted restart step -> restart not_recorded, not_evidenced; obligation not met",
           [(e["recorded"], e["status"]) for e in r["elements"] if e["element"] == "restart"] == [("not_recorded", "not_evidenced")]
           and r["obligation"] != "met")
    v = copy.deepcopy(allpass)
    v["scenarios"][1]["steps"][0]["core_loop_element"] = "model access"
    r = L.core_loop(v, res)
    expect("B-7 a V4-EXM-11 step outside the seven elements -> interface error; never established",
           r["interface_errors"] and not r["established"])
    r = L.core_loop(jfail, resolved_for(jfail))
    expect("B-8 an uncounted step that failed (J-8R) changes no element",
           r["obligation"] == "met" and any(u["step"] == "J-8R" and u["outcome"] == "fail" for u in r["uncounted_steps"]))
    v = copy.deepcopy(allpass)
    v["handoff"]["handed_over"] = False
    expect("B-9 dossier not handed over -> not established", not L.core_loop(v, res)["established"])
    expect("B-10 V4-EXM-12 steps are outside the core loop (EXAMINATION §7)",
           [o["scenario"] for o in L.core_loop(allpass)["outside_core_loop"]] == ["V4-EXM-12"])
    expect("B-11 the standalone dossier's own review is reported separately from the journey's (reader I-5)",
           L.core_loop(sq)["dossier_review"]["state"] == "present" and L.journey(dos)["independent_review"] == "absent")

    # Journey (RP-R2)
    good = copy.deepcopy(dos)
    good["handoff_del_11_03"].update({"counts_as_completed_witness": True,
                                      "acceptance_acts": [{"record_ref": "ACT-1", "actor": "the person", "recorder": "host recorder"}],
                                      "receipts": [{"ref": "RC-1 (invented)", "resolution_at_write": "unresolvable"}]})
    good["independent_review_ref"] = "EXP-RX-LHQ"
    jres = {good["handoff_del_11_03"]["p20a_result_ref"]: {"run_basis": "candidate", "outcome": "pass"}}
    expect("B-12 positive control: counted P20-A, an acceptance act, review, candidate pass, all receipts in the handoff -> established",
           L.journey(good, jres)["established"])
    v = copy.deepcopy(good)
    v["handoff_del_11_03"]["acceptance_acts"][0]["recorder"] = "the person"
    expect("B-13 acceptance act with actor = recorder -> incomplete", L.journey(v, jres)["status"] == "incomplete")
    v = copy.deepcopy(good)
    del v["independent_review_ref"]
    expect("B-14 no independent review record -> incomplete (DOS §1)", L.journey(v, jres)["status"] == "incomplete")
    v = copy.deepcopy(good)
    v["handoff_del_11_03"]["receipts"] = []
    r = L.journey(v, jres)
    expect("B-15 a receipt in the dossier's DEL-09-11 handoff but not in the DEL-11-03 handoff -> listed elsewhere; not established (EUF1-D2)",
           r["receipts"]["elsewhere_in_dossier"][0]["where"] == "handoff_del_09_11" and not r["established"])
    v["host_evidence"] = [{"ref": "RC-9", "kind": "host_receipt", "resolution_at_write": "resolved"}]
    r = L.journey(v, jres)
    expect("B-16 a receipt only in the host evidence index -> listed elsewhere, counted once",
           {x["ref"] for x in r["receipts"]["elsewhere_in_dossier"]} == {"RC-1 (invented)", "RC-9"} and r["receipts"]["total_distinct"] == 2)
    expect("B-17 fixture journey: P20-A not run -> incomplete, not established",
           L.journey(dos)["status"] == "incomplete" and not L.journey(dos)["established"])

    # Candidate (R23-33; LHQ-v0.2 CI-5, R23-36), on O-C's real example
    cirs = {r["record_id"]: r for r in L.load("lhq_cir_examples")}
    mapped = cirs["LHQ-CIR-EXAMPLE-MAPPED (invented)"]
    expect("B-18 LHQ-v0.2's mapped CIR example is valid against the current LHQ CIR schema",
           not L.errors(L.file_validator("lhq_cir_schema"), mapped))
    cs, why = L.map_cir_candidate(mapped)
    expect("B-19 it maps to a valid EXP candidate_subject (R23-33)",
           why == "mapped" and not L.errors(L.def_validator("exp_result_schema", "candidate_subject"), cs))
    sq_subj = L.map_sq_candidate(allpass["candidate"])
    expect("B-20 SQ candidate maps to a valid EXP candidate_subject",
           not L.errors(L.def_validator("exp_result_schema", "candidate_subject"), sq_subj))
    expect("B-21 illustrative SQ candidate vs the mapped CIR, no change-impact record -> differ (results not joined)",
           L.reconcile(sq_subj, cs, why) == "differ")
    same = L.map_sq_candidate({"revision": mapped["app_candidate_subject"]["revision"],
                               "build_identity": mapped["app_candidate_subject"]["build_identity"],
                               "codex_pin": "0.158.0", "package_record": mapped["app_candidate_subject"]["package_record"]})
    expect("B-22 SQ candidate with the same identity -> reconciled", L.reconcile(same, cs, why) == "reconciled")
    expect("B-23 differing identity with an EXP change-impact record named -> reconciled_by_applicability",
           L.reconcile(sq_subj, cs, why, ["EXP-CI-1"]) == "reconciled_by_applicability")
    v = copy.deepcopy(mapped)
    del v["app_candidate_subject"]
    expect("B-24 a supplied App candidate without CI-5's mapping (one string) -> not mappable",
           L.map_cir_candidate(v) == (None, "not_mappable_single_string"))
    expect("B-25 the fixture's CIR (App candidate not supplied) -> not_supplied, so reconciliation not_established", L.map_cir_candidate(cir)[1] == "not_supplied")

    # Completeness (RP-R4, RP-R5)
    clp, jrp = L.core_loop(allpass, res), L.journey(good, jres)
    expect("B-26 both established and reconciled -> complete; practitioner standing not consulted",
           L.replacement_evidence_complete(clp, jrp, "reconciled")["complete"])
    expect("B-27 journey not established -> never complete", not L.replacement_evidence_complete(clp, L.journey(dos), "reconciled")["complete"])
    expect("B-28 candidates differ -> never complete", not L.replacement_evidence_complete(clp, jrp, "differ")["complete"])

    # Package (RP-R6)
    v = copy.deepcopy(pkg)
    v["requester"] = "O-F"
    expect("B-29 a recorder element in the package file is refused (R23-24)", L.check_package(v, m_sha))
    v = copy.deepcopy(pkg)
    v["alternatives"] = [a for a in v["alternatives"] if a["id"] != "ALT-PUBLISHED"]
    expect("B-30 a package without ALT-PUBLISHED is refused (F-R5)", L.check_package(v, m_sha))
    v = copy.deepcopy(pkg)
    v["subject"][1] = "packet manifest sha256:" + "0" * 64
    expect("B-31 a package bound to another manifest is refused", L.check_package(v, m_sha))
    v = copy.deepcopy(pkg)
    v["alternatives"][1]["consequences"] = ["v3.0.1 is replaced", "old projects are retired"]
    expect("B-32 an alternative that does not state it retires nothing is refused", L.check_package(v, m_sha))

    # Disposition (RP-R7)
    dec = copy.deepcopy(disp)
    dec.pop("not_presented_because")
    dec.update({"state": "decided", "fallback_status": "per the chosen alternative",
                "presented": {"when": "2026-10-05", "by": "HELP_HUMAN", "how": "chat"},
                "decision": {"chosen_alternative": "ALT-DEFER", "actor": "the owner", "recorder": "HELP_HUMAN",
                             "record_ref": "OWNER_DECISIONS_n.md (INVENTED)", "exact_text": "INVENTED",
                             "custody": "the owner's chat message, transcribed by the recorder; no platform timestamp",
                             "act_time": {"available": False}}})
    expect("B-33 positive control: an invented decided record with an act reference is accepted by the rules",
           not L.check_disposition(dec, pkg, p_sha), L.check_disposition(dec, pkg, p_sha))
    v = copy.deepcopy(dec)
    del v["decision"]
    expect("B-34 decided without the owner's act -> refused", L.check_disposition(v, pkg, p_sha))
    v = copy.deepcopy(dec)
    v["decision"]["recorder"] = "the owner"
    expect("B-35 actor equals recorder -> refused", L.check_disposition(v, pkg, p_sha))
    v = copy.deepcopy(dec)
    v["decision"]["chosen_alternative"] = "ALT-REPLACE-ALL"
    expect("B-36 an alternative the package does not name -> refused", L.check_disposition(v, pkg, p_sha))
    expect("B-37 package changed after the decision -> lapsed", L.check_disposition(dec, pkg, "1" * 64))
    v = copy.deepcopy(disp)
    v["fallback_status"] = "v4 in use"
    expect("B-38 an undecided disposition that drops v3.0.1 as the fallback -> refused", L.check_disposition(v, pkg, p_sha))
    v = copy.deepcopy(dec)
    v["decision"]["act_time"] = {"available": False, "value": "2026-10-05T10:00Z"}
    expect("B-39 an act time stated as unavailable yet given a value -> refused", L.check_disposition(v, pkg, p_sha))
    v = copy.deepcopy(disp)
    v.update({"state": "presented_no_decision", "presented": {"when": "x", "by": "y", "how": "z"}})
    v.pop("not_presented_because")
    v["decision"] = dec["decision"]
    expect("B-40 a decision element on a presented-but-undecided record -> refused", L.check_disposition(v, pkg, p_sha))


def main():
    part_b(*part_a())
    for name, ok, detail in results:
        print(("HOLDS " if ok else "FAILS ") + name + ("" if ok or not detail else "  -> %s" % (detail,)))
    failed = sum(1 for _, ok, _ in results if not ok)
    print("%d/%d expectations held" % (len(results) - failed, len(results)))
    raise SystemExit(1 if failed else 0)


if __name__ == "__main__":
    main()
