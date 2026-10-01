"""Required-tool check over a test-double catalog (EXEC-v0.6 §3.3-§3.6).

Design prototype for DEL-02-03. Not product code. It renders the report as
the PROPOSED `compatibility-report.schema.json` instance so the schema can be
exercised; field names are Chirality's own and select no wire format.

Rules implemented:
- §3.4 EV-1…EV-11 per required tool reference (first match decides);
- §3.5 three-valued check result, current phase (no checkpoint enters it,
  PH-3) and governance phase (hold support for governed checkpoints, or, for
  fixture readings, checkpoints read "as if governed", GV-5);
- §3.6 HS-1, HS-2, HS-5, HS-4, HS-3 in that order (by held actions, R6-1).
"""

OUTCOME_BLOCKS = {"missing", "not_exposed_on_this_surface", "version_mismatch",
                  "channel_not_enabled"}


def evaluate_reference(req, cat, surface, channel_enabled, readiness):
    """EV-1 is handled at workflow level. Returns (outcome, reason, entry, exposure, availability)."""
    if req.get("unrecognized"):                                   # EV-2
        return "not_established", "unrecognized element in the required-tool category", None, None, None
    if req["class"] == "harness_capability":                      # EV-3
        return ("not_established", "harness capability names unresolved (WD U-08; U-E10)",
                None, None, None)
    if not cat["readable"]:                                       # EV-4
        return "not_established", "catalog unreadable", None, None, None
    entry = cat["entries"].get(req["reference"])
    if entry is None:                                             # EV-5
        return "missing", "no entry in edition " + cat["edition"], None, None, None
    found = {"operation_id": req["reference"], "version": entry["version"]}
    if req["declared_versions"] and entry["version"] not in req["declared_versions"]:   # EV-6
        return ("version_mismatch", "declared %s; edition carries %s; no compatibility statement (equality only)"
                % (",".join(req["declared_versions"]), entry["version"]), found, None, None)
    exposure = entry["exposure"][surface]
    if exposure == "unagreed":                                    # EV-7
        return "not_established", "exposure unagreed on " + surface, found, "unagreed", None
    if exposure == "not exposed":                                 # EV-8
        return ("not_exposed_on_this_surface", "element 9: not exposed on " + surface,
                found, "not_exposed_on_this_surface", None)
    if not channel_enabled:                                       # EV-9
        return "channel_not_enabled", "surface-level: channel not enabled", found, "exposed", None
    if readiness:                                                 # EV-10
        for pre, reason in entry["preconditions"]:
            if pre == "a current solve exists" and cat["no_current_solve"]:
                avail = {"result": "unavailable", "reason": reason,
                         "evaluated_basis": "B2 = FX-W1/g1/%s" % cat["revision"]}
                return "present_currently_unavailable", reason, found, "exposed", avail
        return "present", "", found, "exposed", {"result": "available", "reason": "",
                                                 "evaluated_basis": "FX-W1/g1/%s" % cat["revision"]}
    return "present", "", found, "exposed", None                  # EV-11


def hold_support(cp, surface, run_kind, cat, sq02="answered_no_route"):
    """§3.6 governance-phase value; returns (value, hs_row). Order HS-1, HS-2, HS-5, HS-4, HS-3."""
    if not cp["valid"]:
        return None, "HS-1"
    if surface == "E" and run_kind == "host":
        return "enforced_by_the_host_loop", "HS-2"
    if cp["held_actions"]["app_side"]:
        return "not_enforceable", "HS-5"
    # every held action is a host operation (App run on X)
    unagreed = False  # FXA-1: no unagreed exposure in the fixture
    if unagreed and sq02 != "answered_no_route":
        return "not_established", "HS-4"
    return {"answered_with_route": "enforced_on_the_host_route",
            "unanswered": "not_established",
            "answered_no_route": "not_enforceable"}[sq02], "HS-3"


def check(wf, cat, surface, run_kind, phase, *, channel_enabled=True, readiness=False,
          seat_has_delegation=True, occasion="CK-1", report_id="R-1",
          evaluated_at="2026-09-30T00:00:00Z", model_destination=None, as_if_governed=True):
    """Return a report dict (PROPOSED schema). phase is 'current' or 'governance'."""
    reqs, runtime_holds, limitations = [], [], []
    whole_not_established = wf["required_tools_category"] != "declared" or \
        wf["declared_part_status"] in ("undeclared", "not_established")      # EV-1
    if not whole_not_established:
        for r in wf["requirements"]:
            outcome, reason, entry, exposure, avail = evaluate_reference(
                r, cat, surface, channel_enabled, readiness)
            reqs.append({"reference": r["reference"], "class": r["class"],
                         "necessity": r["necessity"], "purpose": r["purpose"],
                         "declared_versions": r["declared_versions"], "entry": entry,
                         "exposure": exposure or "not_read", "availability": avail,
                         "outcome": outcome, "reason": reason})
            if outcome == "present_currently_unavailable":
                runtime_holds.append({"reference": r["reference"], "reason": reason,
                                      "evaluated_basis": avail["evaluated_basis"]})
            if outcome == "version_mismatch":
                limitations.append("version compatibility: equality only (U-C9)")
    unsupported = []
    if wf["delegation_needed"] and not seat_has_delegation:
        unsupported.append({"reason_kind": "delegation", "checkpoints": []})

    # Checkpoints (CR-9)
    cps, gov_values = [], []
    for cp in wf["checkpoints"]:
        base = {"name": cp["name"], "required_act": cp["required_act"],
                "reached_when_kind": cp["reached_when_kind"], "subject_class": cp["subject_class"],
                "held_actions": cp["held_actions"]["form"], "governed": bool(cp.get("governed")),
                "declaration_status": "valid" if cp["valid"] else "invalid"}
        governed_reading = cp.get("governed") or (as_if_governed and not any(
            c.get("governed") for c in wf["checkpoints"]))
        if phase == "governance" and governed_reading:
            value, row = hold_support(cp, surface, run_kind, cat)
            item = dict(base, phase_reading="governance_value",
                        hold_support={"value": value, "hs_row": row})
            gov_values.append((cp["name"], value))
        else:
            item = dict(base, phase_reading="guidance")
        cps.append(item)
    if phase == "governance":
        ne = [n for n, v in gov_values if v == "not_enforceable"]
        if ne:
            unsupported.append({"reason_kind": "hold_not_enforceable", "checkpoints": ne})

    # §3.5 check result
    required = [r for r in reqs if r["necessity"] == "required"]
    if unsupported or any(r["outcome"] in OUTCOME_BLOCKS for r in required):
        result = "does_not_pass"
    elif whole_not_established or any(r["outcome"] == "not_established" for r in required) or \
            (phase == "governance" and any(v in (None, "not_established") for _, v in gov_values)):
        result = "not_established"
    else:
        result = "passes"
    if surface == "E" and run_kind == "host" and phase == "governance" and gov_values:
        limitations.append("hold support subject to host evidence (DEP-001)")
    limitations.append("evaluated on a test double (FX-PIPE-01)")
    limitations.append("exposure is a fixture assumption (FXA-1)")
    report = {
        "format": "exec-compatibility-report/proposed-0.6", "phase": phase,
        "report_id": report_id,
        "workflow": {"identity": wf["identity"], "holding_library": wf["identity"]["source_root"]},
        "declared_part_status": wf["declared_part_status"],
        "host": {"host_id": "FX-PIPE-01 test double", "catalog_edition": cat["edition"],
                 "catalog_readable": cat["readable"]},
        "surface": {"surface": surface, "channel_state": "enabled" if channel_enabled else "not_enabled"},
        "occasion": {"occasion": occasion, "evaluated_at": evaluated_at},
        "requirements": reqs, "workflow_unsupported": unsupported, "checkpoints": cps,
        "check_result": result, "runtime_holds": runtime_holds, "limitations": limitations,
        "evidence_standing": "test_double", "model_destination": model_destination,
    }
    return report


def statement(report):
    """PS-2 wording for a pass; never 'compatible', 'will run' or 'runnable'."""
    if report["check_result"] == "passes":
        return "requirement check passes against %s on %s at %s" % (
            report["host"]["catalog_edition"], report["surface"]["surface"],
            report["occasion"]["evaluated_at"])
    if report["declared_part_status"] == "undeclared":
        return "requirements undeclared — check not established"
    return "requirement check: " + report["check_result"].replace("_", " ")
