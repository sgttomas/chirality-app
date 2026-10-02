"""Required-tool check over a test-double catalog (EXEC-v0.6 §3.3-§3.6).

Design prototype for DEL-02-03. Not product code. It renders the report as
the PROPOSED `compatibility-report.schema.json` instance so the schema can be
exercised; field names are Chirality's own and select no wire format.

Rules implemented:
- §3.4 EV-1…EV-11 per required tool reference (first match decides), with
  EV-3's presence rule read through the EV-3a table (node G);
- §3.5 three-valued check result, current phase (no checkpoint enters it,
  PH-3) and governance phase (hold support for governed checkpoints, or, for
  fixture readings, checkpoints read "as if governed", GV-5);
- §3.6 HS-1, HS-2, HS-5, HS-4, HS-3 in that order (by held actions, R6-1).
"""

OUTCOME_BLOCKS = {"missing", "not_exposed_on_this_surface", "version_mismatch",
                  "channel_not_enabled"}


# EV-3 presence rule and EV-3a readings at pin 0.158.0 (EXEC-v0.7 §3.4; PROPOSED;
# active per group from node G, R16-3). The signals are HOSTING-BOUNDARY-v0.8
# §8.4's; `signals` is the App's reading for the thread, or None (not read).
APP_CODEX_PIN = "App Codex 0.158.0"


def _settings(s):
    ts = s.get("thread_start")
    if ts is None or "approvalPolicy" not in ts or "sandbox" not in ts:
        return None
    return True


def _web(s):
    caps, mode = s.get("provider_capabilities"), s.get("web_search_mode")
    if caps is None or "webSearch" not in caps or mode is None:
        return None
    return bool(caps["webSearch"]) and mode != "disabled"


def _delegation(s):
    # EXEC-v0.7 EV-3a (R18-1 C-04, C-05; R20-2): `Model.multiAgentVersion` from
    # model/list, `namespaceTools` from modelProvider/capabilities/read, and the
    # stable feature `multi_agent` in the effective configuration. The v0.6
    # signal `multiAgentMode` is "@deprecated Ignored" at 0.158.0 and is not read.
    ver = s.get("model_multi_agent_version")
    if ver is None:
        return None                                   # null or not read
    features = (s.get("effective_config") or {}).get("features") or {}
    if ver == "disabled" or features.get("multi_agent") is False:
        return False
    caps = s.get("provider_capabilities")
    if caps is None or "namespaceTools" not in caps:
        return None
    if caps["namespaceTools"] is False:
        return "limit"
    return True


def _mcp(s):
    servers = s.get("mcp_server_status")
    if servers is None:
        return None
    if any(srv.get("tools") and srv.get("runtimeStatus") == "connected" for srv in servers):
        caps = s.get("provider_capabilities") or {}
        if caps.get("namespaceTools") is False:
            return "limit"
        return True
    if any(srv.get("toolsError") or srv.get("runtimeStatus") in
           (None, "notStarted", "starting", "authenticationRequired", "failed") for srv in servers):
        return None
    return False


def _dynamic(s):
    ts = s.get("thread_start")
    return None if ts is None or "dynamicTools" not in ts else bool(ts["dynamicTools"])


def _imagegen(s):
    caps = s.get("provider_capabilities")
    return None if caps is None or "imageGeneration" not in caps else bool(caps["imageGeneration"])


# name: (HOSTING §8.4 group, reading or None when the rule is inactive, inactive reason)
EV3A = {
    "shell-command": ("HCG-A02", _settings, None),
    "file-change": ("HCG-A03", _settings, None),
    "web-search": ("HCG-A10", _web, None),
    "agent-delegation": ("HCG-A08", _delegation, None),
    "mcp-tool-call": ("HCG-A05", _mcp, None),
    "dynamic-tool-call": ("HCG-A06", _dynamic, None),
    "image-generation": ("HCG-A11", _imagegen, None),
    "person-input-request": ("HCG-A07", None, "no availability signal stated (HOSTING §8.4)"),
    "image-view": ("HCG-A11", None, "no availability signal stated for image viewing (HOSTING §8.4; WD §4.2.5)"),
    "plan-update": ("HCG-A09", None, "no availability signal stated (HOSTING §8.4: stability only)"),
}


def harness_presence(name, harness, signals):
    """EV-3 with EV-3a. Returns (outcome, reason)."""
    if harness != APP_CODEX_PIN:
        return "not_established", "no supplier account for the acting harness (WD HC-1)"
    if name not in EV3A:
        return "not_established", "not a WD-v0.8 §4.2.5 name"
    group, reading, inactive = EV3A[name]
    if reading is None:
        return "not_established", "presence rule inactive for %s: %s" % (group, inactive)
    value = None if signals is None else reading(signals)
    if value is None:
        return "not_established", "availability signal of %s not read" % group
    if value == "limit":
        if name == "agent-delegation":
            return "not_established", "provider may not receive delegation tools (namespaceTools false; OBS-2 O-4, through an adapter)"
        return "not_established", "provider may not receive MCP tools (namespaceTools false; OBS-1 inference)"
    if value:
        return "present", ""
    return "missing", "availability signal of %s reads unavailable" % group


def evaluate_reference(req, cat, surface, channel_enabled, readiness, harness=None, harness_signals=None):
    """EV-1 is handled at workflow level. Returns (outcome, reason, entry, exposure, availability)."""
    if req.get("unrecognized"):                                   # EV-2
        return "not_established", "unrecognized element in the required-tool category", None, None, None
    if req["class"] == "harness_capability":                      # EV-3, EV-3a
        outcome, reason = harness_presence(req["reference"], harness, harness_signals)
        return outcome, reason, None, None, None
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
          evaluated_at="2026-09-30T00:00:00Z", model_destination=None, as_if_governed=True,
          harness=None, harness_signals=None):
    """Return a report dict (PROPOSED schema). phase is 'current' or 'governance'."""
    reqs, runtime_holds, limitations = [], [], []
    whole_not_established = wf["required_tools_category"] != "declared" or \
        wf["declared_part_status"] in ("undeclared", "not_established")      # EV-1
    if not whole_not_established:
        for r in wf["requirements"]:
            outcome, reason, entry, exposure, avail = evaluate_reference(
                r, cat, surface, channel_enabled, readiness, harness, harness_signals)
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
