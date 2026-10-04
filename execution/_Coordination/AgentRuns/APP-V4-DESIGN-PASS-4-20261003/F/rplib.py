"""DEL-11-03 replacement packet rules RP-R1...RP-R9 (prototype for EU-F1; not product code).

Owner O-F, run APP-V4-DESIGN-PASS-4-20261003. Design text: DEL-11-03
Design/REPLACEMENT_PACKET.md (RP-v0.2). Rulings: R23-32 (F-R1...F-R16), R23-33
(EXP candidate_subject is the canonical App candidate identity), R23-36 (LHQ-v0.2 CI-5).

Python 3 standard library plus `jsonschema` (Draft 2020-12). Reads only.
"""

import hashlib
import json
import os

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
}


def abspath(key_or_rel):
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


def core_loop(sq, resolved_exp_records=None):
    """Per-element account from an SQ dossier record (RP-R1 as repaired in RP-v0.2).

    `recorded` is what the dossier records; `status` is what the evidence supports. A step's result stands
    only when its `result_record` resolves to a supplied EXP result record whose run_basis is `candidate`
    and whose outcome equals the step's (EXP-R3). An element whose counted steps do not all resolve is
    `not_evidenced`, whatever the dossier records (RP-v0.1 derived `met` from records alone: finding EUF1-D1).
    """
    resolved_exp_records = resolved_exp_records or {}
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
                uncounted.append(dict(row, element=el))
                continue
            rec = resolved_exp_records.get(st.get("result_record"))
            row["resolved"] = bool(rec and rec.get("run_basis") == "candidate" and rec.get("outcome") == st.get("outcome"))
            by_el[el].append((row, st.get("v3_reference")))
    elements, unresolved = [], []
    for el in CORE_LOOP_ELEMENTS:
        rows = [r for r, _ in by_el[el]]
        if not rows or any(r["state"] != "recorded" for r in rows):
            recorded = "not_recorded" if not any(r["state"] == "recorded" and r.get("outcome") != "pass" for r in rows) else "recorded_not_pass"
        elif all(r.get("outcome") == "pass" for r in rows):
            recorded = "recorded_pass"
        else:
            recorded = "recorded_not_pass"
        resolved = bool(rows) and all(r["resolved"] for r in rows)
        unresolved += [r["step"] for r in rows if not r["resolved"]]
        if not resolved:
            status = "not_evidenced"
        elif recorded == "recorded_pass":
            status = "met"
        elif recorded == "recorded_not_pass":
            status = "not_met"
        else:
            status = "not_evidenced"
        refs = []
        for _, v3 in by_el[el]:
            if v3 and v3 not in refs:
                refs.append(v3)
        elements.append({"element": el, "recorded": recorded, "evidence_resolved": resolved, "status": status,
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
    reasons = []
    if obligation != "met":
        reasons.append("obligation_" + obligation)
    if not sq["handoff"]["handed_over"]:
        reasons.append("dossier_not_handed_over")
    if not sq["handoff"]["reported_as_independent"]:
        reasons.append("dossier_not_independently_examined")
    if unresolved:
        reasons.append("result_records_not_resolved_to_candidate_records")
    if interface_errors:
        reasons.append("interface_error_element_outside_closed_list")
    examiner = sq.get("examiner", {})
    return {
        "elements": elements,
        "uncounted_steps": uncounted,
        "outside_core_loop": outside,
        "interface_errors": interface_errors,
        "obligation": obligation,
        "established": not reasons,
        "not_established_because": reasons,
        "unresolved_steps": unresolved,
        "dossier_review": {"state": "present" if examiner.get("review_record") and sq["handoff"]["reported_as_independent"] else "absent",
                           "review_record": examiner.get("review_record", ""),
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


def reconcile(sq_subject, cir_subject, cir_reason, change_impact_refs=None):
    change_impact_refs = change_impact_refs or []
    if sq_subject is None or cir_subject is None:
        return "not_established"
    if sq_subject["app_candidate"] == cir_subject["app_candidate"]:
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
REQUIRED_RESERVED_BY = ["docs/PRD.md §8", "docs/EXAMINATION.md §7"]


def check_package(pkg, manifest_sha256):
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
    return errs


# --- RP-R7 disposition (DEL-11-03 REQ-004, VER-004; F-R4 OWNER_DECISIONS form) ------

def check_disposition(disp, pkg, pkg_sha256):
    errs = errors(file_validator("rp_disposition_schema"), disp)
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
