"""DEL-11-03 replacement packet rules RP-R1...RP-R9 (prototype for EU-F1; not product code).

Owner O-F, run APP-V4-DESIGN-PASS-4-20261003. Design text: DEL-11-03
Design/REPLACEMENT_PACKET.md (RP-v0.6). Rulings: R23-32 (F-R1...F-R16), R23-33
(EXP candidate_subject is the canonical App candidate identity), R23-36 (LHQ-v0.2 CI-5).

Python 3 standard library plus `jsonschema` (Draft 2020-12). Reads only.
"""

import hashlib
import json
import os
import re

# --- Locations (relative to projects/chirality-app-v4/execution) -------------

EXEC_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))
P09 = "PKG-09_Candidate examination and connected journeys/1_Working"
P11 = "PKG-11_Adoption and replacement continuity/1_Working"
P02 = "PKG-02_Workflow and role portability/1_Working"

PATHS = {
    "sq_examples": P09 + "/DEL-09-02_Standalone App candidate qualification/Design/sq.dossier.valid.examples.json",
    "sq_schema": P09 + "/DEL-09-02_Standalone App candidate qualification/Design/sq.dossier.schema.json",
    "lhq_manifest_examples": P09 + "/DEL-09-07_Local host candidate qualification/Design/lhq.dossier-manifest.valid.examples.json",
    "lhq_manifest_schema": P09 + "/DEL-09-07_Local host candidate qualification/Design/lhq.dossier-manifest.schema.json",
    "lhq_cir_examples": P09 + "/DEL-09-07_Local host candidate qualification/Design/lhq.candidate-identification.valid.examples.json",
    "lhq_cir_schema": P09 + "/DEL-09-07_Local host candidate qualification/Design/lhq.candidate-identification.schema.json",
    "exp_result_schema": P09 + "/DEL-09-01_Candidate examination infrastructure and evidence protocol/Design/exam.result-record.schema.json",
    "ce_schema": P02 + "/DEL-02-03_Workflow execution compatibility and round-trip support/Design/checkpoint-record-entries.schema.json",
    "rp_manifest_schema": P11 + "/DEL-11-03_Owner replacement evidence packet/Design/rp.packet-manifest.schema.json",
    "rp_disposition_schema": P11 + "/DEL-11-03_Owner replacement evidence packet/Design/rp.disposition.schema.json",
    "references": "../reference/REFERENCES.md",
    "ca_schema": P11 + "/DEL-11-01_Preserved history and coexistence account/Design/ca.continuity-account.schema.json",
    "ca_handoff": "_Coordination/AgentRuns/APP-V4-DESIGN-PASS-4-20261003/F/ca/records/CA-1.handoff.json",
    "aa_schema": P11 + "/DEL-11-02_Consumer-specific renewed-basis adoption/Design/aa.adoption-account.schema.json",
    "aa_status": "_Coordination/AgentRuns/APP-V4-DESIGN-PASS-4-20261003/F/aa/records/AA-1.status.json",
}


HERE_F = os.path.dirname(os.path.abspath(__file__))
# R23-44: supplier bytes this unit relies on are vendored in F/vendor/ (see VENDOR.json) and read from there.
VENDORED = {k: os.path.join(HERE_F, "vendor", os.path.basename(PATHS[k]))
            for k in ["sq_examples", "sq_schema", "lhq_manifest_examples", "lhq_manifest_schema", "lhq_cir_examples",
                      "lhq_cir_schema", "exp_result_schema", "ce_schema"]}


def live_path(key):
    """The supplier's live file (for the drift notice only; never used for derivation)."""
    return os.path.normpath(os.path.join(EXEC_ROOT, PATHS[key]))


def abspath(key_or_rel):
    if key_or_rel in VENDORED:
        return VENDORED[key_or_rel]
    rel = PATHS.get(key_or_rel, key_or_rel)
    return os.path.normpath(os.path.join(EXEC_ROOT, rel))


def sha256_file(path):
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def load(key_or_rel):
    with open(abspath(key_or_rel), encoding="utf-8") as fh:
        return json.load(fh)


def dumps(obj):
    """Canonical bytes for files this prototype writes: sorted keys, 2-space indent, LF, trailing newline."""
    return (json.dumps(obj, indent=2, sort_keys=True, ensure_ascii=False) + "\n").encode("utf-8")


# --- Schema helpers ------------------------------------------------------------

def def_validator(schema_key, def_name):
    """A Draft 2020-12 validator for one $def of a schema file (read-only use of another owner's schema)."""
    from jsonschema import Draft202012Validator

    s = load(schema_key)
    wrapper = {"$schema": s.get("$schema"), "$defs": s["$defs"], "$ref": "#/$defs/" + def_name}
    return Draft202012Validator(wrapper)


def file_validator(schema_key):
    from jsonschema import Draft202012Validator

    return Draft202012Validator(load(schema_key))


def errors(validator, instance):
    return sorted(e.message for e in validator.iter_errors(instance))


# --- RP-R1 core-loop obligation (DEL-11-03 REQ-001, VER-001; EXAMINATION §7) ------

CORE_LOOP_ELEMENTS = ["planning", "execution", "workflow saving", "reuse", "approvals", "interruption", "restart"]
CORE_LOOP_SCENARIOS = ["V4-EXM-10", "V4-EXM-11"]


OUTCOME_ORDER = ["fail", "blocked", "not-run", "inconclusive", "pass"]  # EXP-v0.2 $defs/outcome, worst first


def _causes(st):
    """The step's own stated causes for a non-pass outcome (SQ stimuli not produced; blocked_by), copied."""
    out = []
    for stim in st.get("stimuli", []):
        if stim.get("produced") == "not_produced":
            out.append("%s not produced: %s" % (stim.get("id"), stim.get("cause", "no cause stated")))
    if st.get("blocked_by"):
        out.append(str(st["blocked_by"]))
    return out


def core_loop(sq, resolved_exp_records=None, resolved_reviews=None):
    """Per-element account from an SQ dossier record (RP-R1, RP-v0.3).

    `recorded` is what the dossier records, in EXP's outcome vocabulary (worst counted outcome first:
    fail, blocked, not-run, inconclusive, pass), or `not_recorded`. `status` is what the evidence supports:
    `met` only when every counted step resolves to a candidate EXP record with outcome pass; `not_met` only
    when a counted step resolves to a candidate record with outcome **fail**. A blocked, not-run or
    inconclusive step is a missing result, never a failure (SQ-R4; R23-20): its element is `not_evidenced`,
    with the outcome and the step's own causes shown in `status_reason` (RV3 EUF1-R1).
    """
    resolved_exp_records = resolved_exp_records or {}
    resolved_reviews = resolved_reviews or {}
    by_el = {e: [] for e in CORE_LOOP_ELEMENTS}
    uncounted, outside, interface_errors = [], [], []
    for sc in sq["scenarios"]:
        if sc["scenario"] not in CORE_LOOP_SCENARIOS:
            outside.append({"scenario": sc["scenario"], "steps": len(sc["steps"]),
                            "reason": "not core-loop evidence under EXAMINATION §7"})
            continue
        for st in sc["steps"]:
            el = st["core_loop_element"]
            row = {"scenario": sc["scenario"], "step": st["step"], "state": st["state"]}
            if "outcome" in st:
                row["outcome"] = st["outcome"]
            if "result_record" in st:
                row["result_record"] = st["result_record"]
            if el not in CORE_LOOP_ELEMENTS:
                interface_errors.append({"scenario": sc["scenario"], "step": st["step"], "element": el})
                continue
            if not st["counts"]:
                uncounted.append(dict(row, element=el, dossier_reason=st.get("added_reason", "not stated")))
                continue
            causes = _causes(st)
            if causes:
                row["causes"] = causes
            rec = resolved_exp_records.get(st.get("result_record"))
            row["resolved"] = bool(rec and rec.get("run_basis") == "candidate" and rec.get("outcome") == st.get("outcome"))
            by_el[el].append((row, st.get("v3_reference")))
    elements, unresolved = [], []
    for el in CORE_LOOP_ELEMENTS:
        rows = [r for r, _ in by_el[el]]
        outs = [r.get("outcome") for r in rows if r["state"] == "recorded"]
        if not rows or not outs:
            recorded = "not_recorded"
        else:
            worst = min(outs, key=lambda o: OUTCOME_ORDER.index(o) if o in OUTCOME_ORDER else -1)
            recorded = "recorded_" + worst.replace("-", "_") if len(outs) == len(rows) or worst != "pass" else "not_recorded"
        resolved = bool(rows) and all(r["resolved"] for r in rows)
        unresolved += [r["step"] for r in rows if not r["resolved"]]
        resolved_fail = any(r["resolved"] and r.get("outcome") == "fail" for r in rows)
        reasons = []
        if resolved_fail:
            status = "not_met"
            reasons.append("a counted step failed on a candidate record")
        elif resolved and recorded == "recorded_pass":
            status = "met"
        else:
            status = "not_evidenced"
            for r in rows:
                if r["state"] == "recorded" and r.get("outcome") != "pass":
                    reasons.append("%s recorded %s%s" % (r["step"], r.get("outcome"),
                                   (" (" + "; ".join(r["causes"]) + ")") if r.get("causes") else "")
                                   + (": a missing result, not a failure" if r.get("outcome") != "fail" else ""))
            if not resolved:
                reasons.append("results not resolved to records of an identified candidate")
            if recorded == "not_recorded":
                reasons.append("no recorded result for every counted step")
        refs = []
        for _, v3 in by_el[el]:
            if v3 and v3 not in refs:
                refs.append(v3)
        elements.append({"element": el, "recorded": recorded, "evidence_resolved": resolved, "status": status,
                         "status_reason": "; ".join(reasons) if reasons else "every counted step passed on a candidate record",
                         "steps": rows, "v3_references": refs})
    statuses = [e["status"] for e in elements]
    if interface_errors:
        obligation = "not_evidenced"
    elif all(s == "met" for s in statuses):
        obligation = "met"
    elif any(s == "not_met" for s in statuses):
        obligation = "not_met"
    else:
        obligation = "not_evidenced"
    why = []
    if obligation != "met":
        why.append("obligation_" + obligation)
    if not sq["handoff"]["handed_over"]:
        why.append("dossier_not_handed_over")
    if not sq["handoff"]["reported_as_independent"]:
        why.append("dossier_not_independently_examined")
    if unresolved:
        why.append("result_records_not_resolved_to_candidate_records")
    if interface_errors:
        why.append("interface_error_element_outside_closed_list")
    examiner = sq.get("examiner", {})
    ref = examiner.get("review_record", "")
    if ref and ref in resolved_reviews:
        rstate = "present"
    elif ref:
        rstate = "named_not_resolved"
    else:
        rstate = "absent"
    if rstate != "present":
        why.append("dossier_review_not_resolved")
    return {
        "elements": elements,
        "uncounted_steps": uncounted,
        "outside_core_loop": outside,
        "interface_errors": interface_errors,
        "obligation": obligation,
        "established": not why,
        "not_established_because": why,
        "unresolved_steps": unresolved,
        "dossier_review": {"state": rstate, "review_record": ref,
                           "dossier_states_independent": bool(sq["handoff"]["reported_as_independent"]),
                           "covers": "the standalone scenarios V4-EXM-10/11/12 only (DEL-09-02); the journey has its own review (journey.independent_review)"},
    }


# --- RP-R2 journey obligation (DEL-11-03 REQ-002, VER-002; DOS §4 DH-1 as written) ---

def _receipts(manifest):
    """Every receipt reference the whole dossier carries, kept apart by where it appears (RP-v0.2; finding EUF1-D2)."""
    h = manifest["handoff_del_11_03"]
    in_handoff = [{"ref": r["ref"], "resolution_at_write": r["resolution_at_write"]} for r in h["receipts"]]
    seen = {r["ref"] for r in in_handoff}
    elsewhere = []
    for e in manifest.get("host_evidence", []):
        if e.get("kind") == "host_receipt" and e["ref"] not in seen:
            elsewhere.append({"ref": e["ref"], "resolution_at_write": e["resolution_at_write"], "where": "host_evidence"})
            seen.add(e["ref"])
    for r in (manifest.get("handoff_del_09_11") or {}).get("receipt_refs", []):
        if r["ref"] not in seen:
            elsewhere.append({"ref": r["ref"], "resolution_at_write": r["resolution_at_write"], "where": "handoff_del_09_11"})
            seen.add(r["ref"])
    allr = in_handoff + elsewhere
    return {"in_handoff": in_handoff, "elsewhere_in_dossier": elsewhere, "total_distinct": len(allr),
            "unresolvable": sum(1 for r in allr if r["resolution_at_write"] == "unresolvable")}


def host_contributions(cir):
    """The CIR's host contributions by ladder standing (RR-EUF3 #3): 'answered' commits, delivers and adopts nothing."""
    counts = {}
    for c in cir.get("external_contributions", []):
        counts[c.get("standing", "unstated")] = counts.get(c.get("standing", "unstated"), 0) + 1
    beyond = sum(n for k, n in counts.items() if k in ("committed", "delivered", "adopted", "examined"))  # LHQ ladder
    return {"by_standing": counts, "committed_delivered_adopted_or_examined": beyond}


def journey(manifest, resolved_exp_records=None):
    resolved_exp_records = resolved_exp_records or {}
    h = manifest["handoff_del_11_03"]
    reasons = []
    if not h["counts_as_completed_witness"]:
        reasons.append("p20a_not_counted_as_completed_witness")
    if not h["acceptance_acts"]:
        reasons.append("no_acceptance_act_cited")
    if any(a["actor"] == a["recorder"] for a in h["acceptance_acts"]):
        reasons.append("acceptance_act_actor_equals_recorder")
    if not manifest.get("independent_review_ref"):
        reasons.append("no_independent_review_record")
    status = "completed_witness" if not reasons else "incomplete"
    rec = resolved_exp_records.get(h["p20a_result_ref"])
    if rec is None or rec.get("run_basis") != "candidate" or rec.get("outcome") != "pass":
        reasons.append("p20a_result_not_resolved_to_candidate_pass")
    receipts = _receipts(manifest)
    if receipts["elsewhere_in_dossier"]:
        reasons.append("receipts_in_dossier_missing_from_handoff")
    return {
        "dossier_id": manifest["dossier_id"],
        "dossier_version": manifest["version"],
        "p20a_result_ref": h["p20a_result_ref"],
        "counts_as_completed_witness": h["counts_as_completed_witness"],
        "acceptance_acts": len(h["acceptance_acts"]),
        "independent_review": "present" if manifest.get("independent_review_ref") else "absent",
        "receipts": receipts,
        "status": status,
        "established": not reasons,
        "not_established_because": reasons,
    }


# --- RP-R3 candidate identity (R23-33: EXP candidate_subject is canonical) ---------

def map_sq_candidate(sq_candidate):
    """SQ `candidate` -> EXP candidate_subject. codex_pin is configuration, not identity (EXP §3)."""
    app = {"revision": sq_candidate["revision"], "build_identity": sq_candidate["build_identity"],
           "packaged": "package_record" in sq_candidate}
    if "package_record" in sq_candidate:
        app["package_record"] = sq_candidate["package_record"]
    return {"kind": "candidate", "app_candidate": app}


def map_cir_candidate(cir):
    """LHQ CIR -> EXP candidate_subject, or the reason it cannot be mapped.

    LHQ-v0.2 CI-5 (R23-36) adds the optional `app_candidate_subject`, a checked copy of EXP's
    `candidate_subject.app_candidate`, present only while `elements.app_candidate` is supplied. Without it
    the element is one string (`value`), which cannot be split without inventing a convention.
    """
    el = cir["elements"]["app_candidate"]
    if el.get("standing") == "not_supplied":
        return None, "not_supplied"
    proposed = cir.get("app_candidate_subject")  # LHQ-v0.2 CI-5
    if isinstance(proposed, dict):
        subj = {"kind": "candidate", "app_candidate": proposed}
        if cir["elements"].get("host_candidate", {}).get("value"):
            subj["host_candidate"] = cir["elements"]["host_candidate"]["value"]
        subj["identification_record"] = cir["record_id"]
        return subj, "mapped"
    return None, "not_mappable_single_string"


def identity_key(subject):
    """EXP-v0.2 identity of an App candidate: revision, build_identity, packaged (absent means false) and,
    when packaged, package_record. Not a literal object comparison (RV3 EUF1-R4)."""
    a = subject["app_candidate"]
    packaged = bool(a.get("packaged", False))
    return (a["revision"], a["build_identity"], packaged, a.get("package_record") if packaged else None)


def reconcile(sq_subject, cir_subject, cir_reason, change_impact_refs=None):
    change_impact_refs = change_impact_refs or []
    if sq_subject is None or cir_subject is None:
        return "not_established"
    if identity_key(sq_subject) == identity_key(cir_subject):
        return "reconciled"
    return "reconciled_by_applicability" if change_impact_refs else "differ"


# --- RP-R4 completeness; RP-R5 practitioner standing is never a condition ----------

def replacement_evidence_complete(cl, jr, reconciliation):
    reasons = []
    if not cl["established"]:
        reasons.append("core_loop_not_established")
    if not jr["established"]:
        reasons.append("journey_not_established")
    if reconciliation not in ("reconciled", "reconciled_by_applicability"):
        reasons.append("candidate_not_reconciled")
    return {"complete": not reasons, "not_complete_because": reasons,
            "practitioner_validation_is_condition": False}


# --- RP-R6 package file -------------------------------------------------------------

ALTERNATIVE_IDS = ["ALT-OWN-USE", "ALT-PUBLISHED", "ALT-DEFER", "ALT-DECLINE"]
CHOICE_SENTENCE = "Choosing any alternative remains the owner's act, on the evidence as presented"
FIXTURE_NOTICE = "FIXTURE, NOT FOR THE OWNER: no real candidate is identified"
PLACEHOLDER_RE = re.compile(r"illustrative|invented|example|placeholder", re.I)


def derive_standing(supplied, subject, unresolved_steps):
    """EUF4-R1: evidence_standing and candidate.identified are derived, never declared.

    evidence_standing is `illustrative` if any supplied item is illustrative or a first cut; else `candidate`.
    identified needs a mapped subject whose revision and build carry no placeholder marker, and no unresolved
    core-loop step (every counted result resolves to a record of an identified candidate).
    """
    standing = "illustrative" if any(s.get("standing") in ("illustrative", "first_cut_interface") for s in supplied) else "candidate"
    a = (subject or {}).get("app_candidate") or {}
    marked = any(PLACEHOLDER_RE.search(str(a.get(k, ""))) for k in ("revision", "build_identity"))
    identified = bool(a.get("revision") and a.get("build_identity") and not marked and not unresolved_steps)
    return standing, identified
REQUIRED_RESERVED_BY = ["docs/PRD.md §8", "docs/EXAMINATION.md §7"]


def check_package(pkg, manifest_sha256, manifest=None):
    errs = errors(def_validator("ce_schema", "decisionPackageFile"), pkg)
    if pkg.get("actKind") != "A16":
        errs.append("RP-R6: actKind must be A16 (decide)")
    refs = [r.get("ref", "") for r in pkg.get("reservedBy", [])]
    for need in REQUIRED_RESERVED_BY:
        if not any(r.startswith(need) for r in refs):
            errs.append("RP-R6: reservedBy lacks " + need)
    if [a.get("id") for a in pkg.get("alternatives", [])] != ALTERNATIVE_IDS:
        errs.append("RP-R6: alternatives must be exactly " + ", ".join(ALTERNATIVE_IDS))
    if ("packet manifest sha256:" + manifest_sha256) not in pkg.get("subject", []):
        errs.append("RP-R6: subject does not bind the packet manifest's content identity")
    for a in pkg.get("alternatives", []):
        text = " ".join(a.get("consequences", [])).lower()
        if "no retirement" not in text:
            errs.append("RP-R6: %s does not state that it retires nothing" % a.get("id"))
        if a.get("id") == "ALT-PUBLISHED" and "does not perform the public-release act" not in text:
            errs.append("RP-R6: ALT-PUBLISHED does not state that choosing it does not perform the public-release act (RV3 EUF1-R2)")
    for a in pkg.get("alternatives", []):
        for c in a.get("consequences", []):
            if "BUILD_AND_RELEASE" in c and not ("manual" in c and "on request" in c):
                errs.append("RP-R6: %s's inference from BUILD_AND_RELEASE drops 'manual' or 'on request'" % a.get("id"))
    if manifest is not None:
        d_standing, d_identified = derive_standing(manifest.get("supplied", []), manifest["candidate"].get("subject"),
                                                   manifest.get("core_loop", {}).get("unresolved_steps", ["unknown"]))
        if manifest.get("evidence_standing") != d_standing or manifest["candidate"].get("identified") != d_identified:
            errs.append("RP-R6: the manifest's declared standing or identification disagrees with what its supplied items and subject derive (EUF4-R1)")
        illustrative = d_standing == "illustrative" or not d_identified
        if illustrative and not manifest.get("fixture", False):
            errs.append("RP-R6: an illustrative or unidentified candidate is refused in a packet that is not a fixture (REQ-004; R23-43)")
        if illustrative and not pkg.get("purpose", "").startswith(FIXTURE_NOTICE):
            errs.append("RP-R6: the purpose does not open with the fixture notice for an unidentified candidate")
    if CHOICE_SENTENCE not in pkg.get("purpose", ""):
        errs.append("RP-R6: purpose does not state that the choice remains the owner's act on the evidence as presented")
    return errs


# --- RP-R7 disposition (DEL-11-03 REQ-004, VER-004; F-R4 OWNER_DECISIONS form) ------

def check_disposition(disp, pkg, pkg_sha256, manifest=None):
    errs = errors(file_validator("rp_disposition_schema"), disp)
    if manifest is not None and manifest.get("fixture") and disp.get("state") in ("presented_no_decision", "decided"):
        errs.append("RP-R7: a fixture package is never presented or decided (EUF4-R1)")
    if disp.get("package_id") != pkg.get("packageId"):
        errs.append("RP-R7: disposition names another package")
    if disp.get("package_file", {}).get("sha256") != pkg_sha256:
        errs.append("RP-R7: package changed after presentation or decision; the disposition has lapsed")
    if disp.get("state") == "decided":
        d = disp.get("decision", {})
        if d.get("chosen_alternative") not in [a["id"] for a in pkg.get("alternatives", [])]:
            errs.append("RP-R7: chosen alternative is not one the package names")
        if d.get("actor") == d.get("recorder"):
            errs.append("RP-R7: actor equals recorder")
    else:
        if "v3.0.1 remains the fallback" not in disp.get("fallback_status", ""):
            errs.append("RP-R7: an undecided disposition must keep v3.0.1 as the fallback")
    return errs
