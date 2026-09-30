#!/usr/bin/env python3
"""SH-1, the simulated host specified in DEL-03-01 C-v0.8 §10.8 (R12-4).

A test double, not product code and not a model of any real host. It holds a
small part of the invented fixture FX-PIPE-01 (C §10) in a state file and
offers it on BOTH native paths the App v4 design considers (R12-4):

  * the MCP-tool path:  `simhost.py mcp --state DIR`   (newline-delimited
    JSON-RPC 2.0 on stdin/stdout, methods `initialize`, `tools/list`,
    `tools/call`), and
  * the command-line path: `simhost.py cli --state DIR <command> ...`
    (one host document as JSON on stdout; exit status 0 when a host document
    was produced, whatever its outcome).

Both paths reach the same host core and the same state, so one host state is
observable through either path. The person's acts and the host's own steps are
separate controls (`person ...`, `host ...`) that no agent path reaches; they
stand for the host's own interface and are fixture acts, not act capture.

Every document the double returns follows the PROPOSED Chirality schemas
(catalog, edition_change_event, read_result, proposal_state). Their property
names are Chirality's semantic labels. The double's tool names, command words,
`_meta` key and content-identity method `m-sh1` (a truncated sha256 over sorted
JSON) are the double's own labels: none of them selects a host wire field, a
transport or an identity algorithm (TBD-003, TBD-007).

Python 3 standard library only.
"""

import argparse
import copy
import hashlib
import json
import os
import sys
from pathlib import Path

HOST = "SH-1"
METHOD = "m-sh1"
PERSON = "Engineer A"


def cid(obj):
    raw = json.dumps(obj, sort_keys=True, separators=(",", ":")).encode()
    return "sh1:" + hashlib.sha256(raw).hexdigest()[:16]


# --------------------------------------------------------------------- state

def initial_state(profile, edition):
    model = {
        "R-100": {"kind": "run", "from": "N-1", "to": "N-2",
                  "supports": ["S-1", "S-2", "S-3", "S-4"]},
        "S-1": {"kind": "support", "run": "R-100", "location_m": 0.5,
                "type": "guide", "stiffness": "2.0e6", "label": "G-1"},
        "S-2": {"kind": "support", "run": "R-100", "location_m": 2.0,
                "type": "rigid", "stiffness": "rigid", "label": "R-2"},
        "S-3": {"kind": "support", "run": "R-100", "location_m": 8.4,
                "type": "rigid", "stiffness": "rigid", "label": "R-3"},
        "S-4": {"kind": "support", "run": "R-100", "location_m": 11.0,
                "type": "guide", "stiffness": "2.0e6", "label": "G-4a"},
    }
    return {
        "host_identity": HOST,
        "profile": profile,
        "edition": edition,
        "edition_events": [],
        "endpoint": "up",
        "enablement": {"record": "not_in_force"},
        "clock": 0,
        "workspace": "FX-W1",
        "generation": "g1",
        "revision": 12,
        "model": model,
        "history": {"12": copy.deepcopy(model)},
        "solve": {"LC-1": 12},
        "settings": {"P-03": {"display_state": "effective_policy_default",
                              "grant_value": "propose", "scope": [],
                              "reference": "set-1"}},
        "proposals": {},
        "next_receipt": 1,
        "next_act": 1,
        "next_ticket": 1,
    }


def load(state_dir):
    return json.loads((Path(state_dir) / "state.json").read_text())


def save(state_dir, st):
    (Path(state_dir) / "state.json").write_text(json.dumps(st, indent=1, sort_keys=True))


def tick(st):
    st["clock"] += 1
    return f"t{st['clock']:04d}"


# ----------------------------------------------------------------- catalogue

def lineage_value(st, value):
    if st["profile"] == "no-lineage":
        return {"not_supplied": "host_declares_none"}
    return value


def basis(st, revision=None, model=None, content=None):
    revision = st["revision"] if revision is None else revision
    model = st["model"] if model is None else model
    content = model if content is None else content
    return {
        "workspace_identity": lineage_value(st, st["workspace"]),
        "generation": lineage_value(st, st["generation"]),
        "model_revision": f"r{revision}",
        "canonical_content_identity": cid(content),
        "identity_method": METHOD,
    }


def basis_profile(st):
    lineage = "not_supplied" if st["profile"] == "no-lineage" else "supplied"
    return {"workspace_identity": lineage, "generation": lineage,
            "model_revision": "supplied", "canonical_content_identity": "supplied",
            "subject_content_identity": "per_subject",
            "staleness_scope": "per_item_relied_on_targets"}


def arg(name, meaning, kind, required=True, target=False, unit=None):
    return {"argument_name": name, "meaning": meaning, "value_kind": kind,
            "unit": unit, "required": required, "identifies_target": target}


def cls(value, record=None, standing="INTEGRATION", reason=None):
    c = {"class_value": value, "value_standing": standing,
         "consequence_statement": None, "host_adoption": "not_evidenced"}
    if value == "no_policy_basis":
        c["no_policy_basis_reason"] = reason
    else:
        c["policy_record_reference"] = record
    return c


EXPOSED = {"H": "exposed", "E": "exposed", "X": "exposed"}


def entries(st):
    run_pre = {"precondition_identity": "run-exists", "meaning": "the run exists in the workspace",
               "reason_identity": "R-run-not-found", "reason_statement": "Run not found in this workspace"}
    read = {"kind": "none"}
    change = {"kind": "change", "affected_object_kinds": ["support", "run"],
              "old_new_reporting": ["location_m", "type", "stiffness", "label"],
              "resulting_objects_reported": True}
    e = [
        {"operation_identity": "OP-C1", "operation_version": "v1",
         "purpose": "Lists supports on a run with type, location, stiffness and label",
         "input": {"arguments": [arg("run", "the run whose supports are listed", "identity", target=True),
                                 arg("requested_basis", "an earlier basis to read at (historical read)", "basis_descriptor", required=False)],
                   "accepts_requested_basis": True},
         "availability": [run_pre], "effects": read,
         "result": {"content_kinds": ["table", "host_check"], "named_host_checks": ["equilibrium", "unit-consistency"]},
         "errors": [{"error_identity": "E-invalid-run", "meaning": "the run argument is malformed", "raised_at": "evaluation", "effect": "none"}],
         "class": cls("none", "fixture-read"), "exposure": EXPOSED},
        {"operation_identity": "OP-C2", "operation_version": "v1",
         "purpose": "Stresses and support loads for a load case",
         "input": {"arguments": [arg("run", "the run", "identity", target=True),
                                 arg("load_case", "the load case", "identity")],
                   "accepts_requested_basis": False},
         "availability": [run_pre,
                          {"precondition_identity": "current-solve-exists", "meaning": "a solve exists at the present revision for the load case",
                           "reason_identity": "R-no-current-solve", "reason_statement": "No current solve for LC-1 at this revision",
                           "remedy": "the load case must be solved at the present revision"}],
         "effects": read,
         "result": {"content_kinds": ["result_value", "host_check"], "named_host_checks": ["equilibrium", "unit-consistency"]},
         "errors": [{"error_identity": "E-unknown-load-case", "meaning": "no such load case", "raised_at": "evaluation", "effect": "none"}],
         "class": cls("none", "fixture-read"), "exposure": EXPOSED},
        {"operation_identity": "OP-C3", "operation_version": "v1",
         "purpose": "Lists spans exceeding a requester-stated limit, as the requester's findings",
         "input": {"arguments": [arg("run", "the run", "identity", target=True),
                                 arg("spacing_limit_m", "the requester's limit", "number", unit="m")],
                   "accepts_requested_basis": False},
         "availability": [run_pre], "effects": read,
         "result": {"content_kinds": ["finding"], "named_host_checks": []},
         "errors": [{"error_identity": "E-invalid-limit", "meaning": "limit not positive", "raised_at": "evaluation", "effect": "none"}],
         "class": cls("none", "fixture-read"), "exposure": EXPOSED},
        {"operation_identity": "OP-C4", "operation_version": "v1",
         "purpose": "Adds a support at a location on a run",
         "input": {"arguments": [arg("run", "the run", "identity", target=True),
                                 arg("location_m", "location along the run", "number", unit="m"),
                                 arg("type", "support type", "enumeration")],
                   "accepts_requested_basis": False},
         "availability": [run_pre], "effects": change,
         "result": {"content_kinds": ["applied_association", "proposal_state"], "named_host_checks": []},
         "errors": [{"error_identity": "E-location-occupied", "meaning": "a support already stands there", "raised_at": "validation", "effect": "none"},
                    {"error_identity": "E-apply-interrupted", "meaning": "application interrupted", "raised_at": "application", "effect": "unknown"}],
         "class": cls("may_apply_within_granted_autonomy", "P-03", "DERIVED"), "exposure": EXPOSED},
        {"operation_identity": "OP-C5", "operation_version": "v1",
         "purpose": "Changes a support's stiffness",
         "input": {"arguments": [arg("support", "the support", "identity", target=True),
                                 arg("stiffness", "new stiffness", "text", unit="N/m")],
                   "accepts_requested_basis": False},
         "availability": [], "effects": change,
         "result": {"content_kinds": ["applied_association", "proposal_state"], "named_host_checks": []},
         "errors": [{"error_identity": "E-invalid-stiffness", "meaning": "stiffness not valid", "raised_at": "validation", "effect": "none"}],
         "class": cls("may_apply_within_granted_autonomy", "P-03", "DERIVED"), "exposure": EXPOSED},
        {"operation_identity": "OP-C6", "operation_version": "v1",
         "purpose": "Performs the person's A4 on a row's content",
         "input": {"arguments": [arg("row", "the row", "identity", target=True)], "accepts_requested_basis": False},
         "availability": [], "effects": {"kind": "change", "affected_object_kinds": ["host act state"], "resulting_objects_reported": False},
         "result": {"content_kinds": ["result_value"], "named_host_checks": []},
         "errors": [], "class": cls("reserved_to_the_person", "P-02", "DERIVED"), "exposure": EXPOSED},
        {"operation_identity": "OP-C7", "operation_version": "v1",
         "purpose": "Performs the person's A5 on one or more change items",
         "input": {"arguments": [arg("proposal", "the proposal", "identity", target=True), arg("items", "items", "text")], "accepts_requested_basis": False},
         "availability": [], "effects": {"kind": "change", "affected_object_kinds": ["proposal item dispositions"], "resulting_objects_reported": False},
         "result": {"content_kinds": ["result_value"], "named_host_checks": []},
         "errors": [], "class": cls("reserved_to_the_person", "P-02", "DERIVED"), "exposure": EXPOSED},
        {"operation_identity": "OP-C8", "operation_version": "v1",
         "purpose": "Performs the person's A10",
         "input": {"arguments": [arg("proposal", "the proposal", "identity", target=True), arg("items", "items", "text")], "accepts_requested_basis": False},
         "availability": [], "effects": {"kind": "change", "affected_object_kinds": ["proposal item dispositions"], "resulting_objects_reported": False},
         "result": {"content_kinds": ["result_value"], "named_host_checks": []},
         "errors": [], "class": cls("reserved_to_the_person", "P-02", "DERIVED"), "exposure": EXPOSED},
        {"operation_identity": "OP-C12", "operation_version": "v1",
         "purpose": "Runs the host's named check 'support spacing' with host-defined limits",
         "input": {"arguments": [arg("run", "the run", "identity", target=True)], "accepts_requested_basis": False},
         "availability": [], "effects": read,
         "result": {"content_kinds": ["host_check"], "named_host_checks": ["support-spacing"]},
         "errors": [{"error_identity": "E-check-unavailable", "meaning": "check cannot run", "raised_at": "evaluation", "effect": "none"}],
         "class": cls("none", "fixture-read"), "exposure": EXPOSED},
    ]
    if st["edition"] == "e2":
        e.insert(8, {"operation_identity": "OP-C9", "operation_version": "v1",
                     "purpose": "Changes a support's display label",
                     "input": {"arguments": [arg("support", "the support", "identity", target=True),
                                             arg("label", "new label", "text")], "accepts_requested_basis": False},
                     "availability": [], "effects": change,
                     "result": {"content_kinds": ["applied_association", "proposal_state"], "named_host_checks": []},
                     "errors": [{"error_identity": "E-label-too-long", "meaning": "label too long", "raised_at": "validation", "effect": "none"}],
                     "class": cls("may_apply_within_granted_autonomy", "P-03", "DERIVED"), "exposure": EXPOSED})
    return e


def catalog_doc(st):
    doc = {"host_identity": HOST, "edition": st["edition"], "completeness": "complete",
           "basis_profile": basis_profile(st), "entries": entries(st)}
    if st["edition"] == "e2" and st["edition_events"]:
        doc["previous_edition"] = "e1"
    return doc


def entry(st, op):
    for e in entries(st):
        if e["operation_identity"] == op:
            return e
    return None


# ------------------------------------------------------------------- results

def non_success(outcome, reporter="host", **kw):
    d = {"outcome": outcome, "reporter": reporter}
    d.update(kw)
    return d


def opref(op):
    return {"operation_identity": op, "operation_version": "v1"}


def subject_row(st, sid, model):
    attrs = model[sid]
    return {"subject": {"subject_identity": sid, "subject_content_identity": cid(attrs),
                        "identity_method": METHOD, "identity_scope": "per_subject"},
            "cells": {"location_m": attrs["location_m"], "type": attrs["type"],
                      "stiffness": attrs["stiffness"], "label": attrs["label"]}}


def solve_checks(st):
    rev = st["solve"]["LC-1"]
    b = basis(st, rev, st["history"][str(rev)])
    return [{"check_name": "equilibrium", "verdict": "passed", "evaluated_basis": b},
            {"check_name": "unit-consistency", "verdict": "passed", "evaluated_basis": b}]


def spans(model, run):
    sup = sorted((model[s]["location_m"], s) for s in model[run]["supports"])
    return [(a[1], b[1], round(b[0] - a[0], 3)) for a, b in zip(sup, sup[1:])]


def read_op(st, op, args):
    e = entry(st, op)
    run = args.get("run")
    if op in ("OP-C1", "OP-C2", "OP-C3", "OP-C12") and run not in st["model"]:
        return non_success("unavailable", operation=opref(op), edition=st["edition"], surface="X",
                           evaluated_basis=basis(st),
                           unavailable_reason={"reason_identity": "R-run-not-found",
                                               "reason_statement": "Run not found in this workspace",
                                               "failed_precondition": "run-exists", "evaluated_basis": basis(st)})
    if op == "OP-C1":
        model, rev, currency = st["model"], st["revision"], "current"
        requested = args.get("requested_basis")
        if requested is not None:
            r = str(requested.get("model_revision", "")).lstrip("r")
            if r not in st["history"]:
                return non_success("unavailable", operation=opref(op), edition=st["edition"], surface="X",
                                   evaluated_basis=basis(st),
                                   unavailable_reason={"reason_identity": "R-historical-basis-not-held",
                                                       "reason_statement": "The requested earlier basis is not held by this host",
                                                       "failed_precondition": "historical-basis-held", "evaluated_basis": basis(st)})
            model, rev, currency = st["history"][r], int(r), ("historical" if int(r) != st["revision"] else "current")
        rows = [subject_row(st, s, model) for s in model[run]["supports"]]
        table = {"table_identity": f"supports-{run}", "meaning": f"supports on {run}",
                 "columns": [{"column_identity": "location_m", "meaning": "location along the run", "unit": "m", "value_kind": "number"},
                             {"column_identity": "type", "meaning": "support type", "unit": None, "value_kind": "enumeration"},
                             {"column_identity": "stiffness", "meaning": "stiffness", "unit": "N/m", "value_kind": "text"},
                             {"column_identity": "label", "meaning": "display label", "unit": None, "value_kind": "text"}],
                 "rows": rows}
        rattrs = model[run]
        run_table = {"table_identity": f"run-{run}", "meaning": f"geometry of {run}",
                     "columns": [{"column_identity": "from", "meaning": "start node", "unit": None, "value_kind": "identity"},
                                 {"column_identity": "to", "meaning": "end node", "unit": None, "value_kind": "identity"}],
                     "rows": [{"subject": {"subject_identity": run, "subject_content_identity": cid(rattrs),
                                           "identity_method": METHOD, "identity_scope": "per_subject"},
                               "cells": {"from": rattrs["from"], "to": rattrs["to"]}}]}
        content = {"table": [r["cells"] | {"id": r["subject"]["subject_identity"]} for r in rows],
                   "run": cid(rattrs)}
        doc = {"outcome": "success", "operation": opref(op), "edition": st["edition"], "surface": "X",
               "basis": basis(st, rev, model, content),
               "views": [{"view_identity": "main", "tables": [table, run_table], "results": [], "diagnostics": []}],
               "standing": {"currency": currency, "host_checks": solve_checks(st),
                            "known_limitations": ["linear supports assumed"], "human_act_evidence": []}}
        if requested is not None:
            doc["requested_basis"] = requested
        return doc
    if op == "OP-C2":
        if args.get("load_case") != "LC-1":
            return non_success("error", operation=opref(op), evaluated_basis=basis(st),
                               error={"error_identity": "E-unknown-load-case", "meaning": "no such load case", "effect": "none"})
        if st["solve"]["LC-1"] != st["revision"]:
            b = basis(st)
            return non_success("unavailable", operation=opref(op), edition=st["edition"], surface="X",
                               evaluated_basis=b,
                               unavailable_reason={"reason_identity": "R-no-current-solve",
                                                   "reason_statement": "No current solve for LC-1 at this revision",
                                                   "failed_precondition": "current-solve-exists",
                                                   "remedy": "the load case must be solved at the present revision",
                                                   "evaluated_basis": b})
        results = [{"result_identity": f"load-{s}", "meaning": f"sustained load at {s}", "value": 1000 + i,
                    "unit": "N", "subject_identity": s} for i, s in enumerate(st["model"][run]["supports"])]
        return {"outcome": "success", "operation": opref(op), "edition": st["edition"], "surface": "X",
                "basis": basis(st, content={"results": results}),
                "views": [{"view_identity": "main", "tables": [], "results": results, "diagnostics": []}],
                "standing": {"currency": "current", "host_checks": solve_checks(st),
                             "known_limitations": ["linear supports assumed"], "human_act_evidence": []}}
    if op == "OP-C3":
        limit = float(args.get("spacing_limit_m", 0))
        if limit <= 0:
            return non_success("error", operation=opref(op), evaluated_basis=basis(st),
                               error={"error_identity": "E-invalid-limit", "meaning": "limit not positive", "effect": "none"})
        findings = [{"finding_identity": f"F-{a}-{b}", "author_kind": "requester",
                     "statement": f"span {a}->{b} is {d} m, over the requester's limit {limit} m",
                     "attachments": [{"attaches_to": "subject", "reference": a}, {"attaches_to": "subject", "reference": b}]}
                    for a, b, d in spans(st["model"], run) if d > limit]
        return {"outcome": "success", "operation": opref(op), "edition": st["edition"], "surface": "X",
                "basis": basis(st, content={"findings": findings}),
                "views": [{"view_identity": "main", "tables": [], "results": [], "diagnostics": [], "findings": findings}],
                "standing": {"currency": "current", "host_checks": [], "known_limitations": [], "human_act_evidence": []}}
    if op == "OP-C12":
        over = [(a, b, d) for a, b, d in spans(st["model"], run) if d > 6.0]
        b = basis(st)
        check = {"check_name": "support-spacing", "verdict": "failed" if over else "passed", "evaluated_basis": b}
        if over:
            check["exceedances"] = [{"attaches_to": "subject", "reference": f"{a}->{bb}"} for a, bb, d in over]
        return {"outcome": "success", "operation": opref(op), "edition": st["edition"], "surface": "X",
                "basis": b,
                "views": [{"view_identity": "main", "tables": [], "results": [], "diagnostics": []}],
                "standing": {"currency": "current", "host_checks": [check], "known_limitations": [], "human_act_evidence": []}}
    raise KeyError(op)


# --------------------------------------------------------- proposal route

OPEN = {"drafted", "validated", "queued", "accepted"}


def derived(items):
    counts = {}
    for it in items:
        counts[it["state"]] = counts.get(it["state"], 0) + 1
    summary = next(iter(counts)) if len(counts) == 1 else "mixed"
    decided = all(("decision" in it) or it["state"] in
                  {"refused_stale", "refused_invalid", "refused_not_permitted", "withdrawn", "left_queue"}
                  for it in items)
    return {"summary": summary, "counts": counts,
            "open": any(it["state"] in OPEN for it in items), "all_items_decided": decided}


def state_doc(st, p, answered=False):
    items = copy.deepcopy(p["items"])
    return {"kind": "recorded_state", "proposal_identity": p["proposal_identity"],
            **({"lineage_replaces": p["lineage"]} if p.get("lineage") else {}),
            "host_handles": [{"handle_kind": "ticket", "value": p["ticket"], "scope": "durable"}],
            "dedup_scope": "durable", "submissions_recorded": p["submissions"],
            "answered_from_recorded_state": answered, "items": items,
            "derived_state": derived(items), "observed_at": tick(st),
            "current_basis": basis(st)}


def item_content(it, relied):
    return cid({k: it.get(k) for k in ("operation_identity", "operation_version", "affected_object",
                                         "relied_on_targets", "attribute", "old_value", "new_value")} | {"basis": relied})


def stale_targets(st, it):
    bad = []
    for t in it["relied_on_targets"]:
        sid = t["subject_identity"]
        cur = cid(st["model"][sid]) if sid in st["model"] else None
        if cur != t["subject_content_identity"]:
            bad.append(sid)
    return bad


def treatment(st, it, mode):
    """Treatment on the route (R-3 point 1), from the double's settings."""
    op = it["operation_identity"]
    e = entry(st, op)
    if e is None:
        return ("not_exposed", None)
    if e["class"]["class_value"] == "reserved_to_the_person":
        return ("not_permitted", {"kind": "policy_record", "reference": "P-02"})
    if mode == "propose":
        return ("propose", None)
    s = st["settings"]["P-03"]
    target = it["affected_object"].get("object_identity")
    if s["grant_value"] == "direct" and target in s["scope"]:
        return ("direct", None)
    return ("not_permitted", {"kind": "policy_record", "reference": f"P-03 ({s['reference']}: {s['grant_value']})"})


def submit(st, req):
    pid = req["proposal_identity"]["value"]
    content = cid(req)
    if pid in st["proposals"]:                              # de-duplication first (R2-13)
        p = st["proposals"][pid]
        if p["content"] != content:
            return {"kind": "identity_conflict", "proposal_identity": pid,
                    "recorded_content_identity": p["content"], "submitted_content_identity": content,
                    "effect": "none", "observed_at": tick(st)}
        p["submissions"] += 1
        return state_doc(st, p, answered=True)
    relied = req["relied_on_basis"][0]
    items = []
    applied_any = False
    for it in req["items"]:
        rec = {"item_identity": it["item_identity"], "change_item_content_identity": item_content(it, relied),
               "identity_method": METHOD}
        tr, gov = treatment(st, it, req["requested_mode"])
        bad = stale_targets(st, it)
        if tr == "not_permitted":
            rec |= {"state": "refused_not_permitted", "refusal": {"reason": "treatment forbids the requested mode",
                    "evaluated_basis": basis(st), "governing_treatment": gov}}
        elif bad:
            rec |= {"state": "refused_stale", "refusal": {"reason": f"{', '.join(bad)} changed since {relied['model_revision']}",
                    "failing_targets": bad, "staleness_scope": "per_item_relied_on_targets",
                    "relied_on_basis": relied, "evaluated_basis": basis(st)}}
        elif it["operation_identity"] == "OP-C4" and any(
                st["model"][s]["location_m"] == it["new_value"] for s in st["model"][it["affected_object"].get("object_identity", "R-100")]["supports"]):
            rec |= {"state": "refused_invalid", "refusal": {"reason": "a support already stands there",
                    "error_identity": "E-location-occupied", "evaluated_basis": basis(st)}}
        elif tr == "direct":
            rec |= {"state": "validated"}
            rec = apply_item(st, it, rec, relied, "direct_under_grant")
            applied_any = True
        else:
            rec |= {"state": "queued"}
        items.append(rec)
    p = {"proposal_identity": pid, "lineage": (req.get("lineage") or {}).get("replaces"),
         "content": content, "request": req, "items": items, "submissions": 1,
         "ticket": f"TK-{st['next_ticket']}"}
    st["next_ticket"] += 1
    st["proposals"][pid] = p
    return state_doc(st, p)


def commit(st):
    st["revision"] += 1
    st["history"][str(st["revision"])] = copy.deepcopy(st["model"])


def apply_item(st, it, rec, relied, branch):
    op = it["operation_identity"]
    objs = []
    if op == "OP-C4":
        n = 1 + max(int(k.split("-")[1]) for k in st["model"] if k.startswith("S-"))
        sid = f"S-{n}"
        run = it["affected_object"].get("object_identity", "R-100")
        st["model"][sid] = {"kind": "support", "run": run, "location_m": it["new_value"], "type": "guide",
                            "stiffness": "2.0e6", "label": f"G-{n}"}
        st["model"][run]["supports"].append(sid)
        objs = [(sid, "created"), (run, "changed")]
    else:
        sid = it["affected_object"]["object_identity"]
        st["model"][sid][it["attribute"]] = it["new_value"]
        objs = [(sid, "changed")]
    commit(st)
    receipt = f"RC-{st['next_receipt']}"
    st["next_receipt"] += 1
    rec["state"] = "applied"
    rec["applied"] = {"branch": branch, "receipt_reference": receipt, "relied_on_basis": relied,
                      "resulting_revision": f"r{st['revision']}",
                      "resulting_objects": [{"object_identity": o, "relation": r,
                                             "subject_content_identity": cid(st["model"][o]),
                                             "identity_method": METHOD} for o, r in objs]}
    return rec


def observe(st, pid):
    p = st["proposals"].get(pid)
    if p is None:
        return {"kind": "not_known_to_host", "proposal_identity": pid, "dedup_scope": "durable",
                "scope_covers_since": "t0000", "observed_at": tick(st)}
    return state_doc(st, p)


# ------------------------------------------------------------- agent entry

ROUTE_TOOLS = {"read-catalog": "catalog", "read-edition-events": "events",
               "submit-proposal": "submit", "observe-proposal": "observe"}


def handle(st, name, args):
    """One agent-path request. Returns (host document, changed?)."""
    if st["enablement"]["record"] != "in_force":
        return non_success("channel_not_enabled", "host", channel_state="disabled"), False
    if name in ("read-catalog", "catalog"):
        return catalog_doc(st), False
    if name in ("read-edition-events", "events"):
        return {"host_identity": HOST, "edition": st["edition"], "events": st["edition_events"]}, False
    if name in ("submit-proposal", "submit"):
        doc = submit(st, args["proposal"])
        return doc, True
    if name in ("observe-proposal", "observe"):
        return observe(st, args["proposal_identity"]), True
    e = entry(st, name)
    if e is None:
        return non_success("not_exposed_on_this_surface", "host", operation={"operation_identity": name, "operation_version": "unknown"},
                           surface="X"), False
    if e["class"]["class_value"] == "reserved_to_the_person":
        return non_success("not_permitted", operation=opref(name), evaluated_basis=basis(st),
                           governing_treatment={"kind": "policy_record", "reference": "P-02"}, a8_offered=True), False
    if e["effects"]["kind"] == "change":
        return non_success("not_permitted", operation=opref(name), evaluated_basis=basis(st),
                           governing_treatment={"kind": "policy_record", "reference": "P-03 (set-1: propose); submit a proposal"},
                           a8_offered=False), False
    return read_op(st, name, args), False


# -------------------------------------------------------------------- paths

def tool_list(st):
    tools = []
    for e in entries(st):
        props = {a["argument_name"]: {"type": "string" if a["value_kind"] != "number" else "number"}
                 for a in e["input"]["arguments"] if a["value_kind"] != "basis_descriptor"}
        tools.append({"name": e["operation_identity"], "description": e["purpose"],
                      "inputSchema": {"type": "object", "properties": props},
                      "_meta": {"sh1/catalog": {"operation_identity": e["operation_identity"],
                                                "operation_version": e["operation_version"],
                                                "edition": st["edition"], "mapping_source": "host-supplied"}}})
    for name, kind in ROUTE_TOOLS.items():
        tools.append({"name": name, "description": f"{kind} (catalog or route interface; not a catalog entry)",
                      "inputSchema": {"type": "object"},
                      "_meta": {"sh1/interface": kind}})
    return tools


def mcp_main(state_dir):
    st0 = load(state_dir)
    if st0["endpoint"] != "up":
        sys.stderr.write("SH-1: endpoint unavailable (controller not running)\n")
        return 69
    for line in sys.stdin:
        if not line.strip():
            continue
        req = json.loads(line)
        st = load(state_dir)
        rid, method, params = req.get("id"), req.get("method"), req.get("params", {})
        err = {"code": -32601, "message": f"method not found: {method}"}
        if method == "initialize":
            res = {"serverInfo": {"name": "sh1-simulated-host", "version": "0.1-test-double"}, "capabilities": {"tools": {}}}
        elif method == "tools/list" and st["enablement"]["record"] != "in_force":
            res = None
            err = {"code": -32000, "message": "channel not enabled",
                   "data": non_success("channel_not_enabled", "host", channel_state="disabled")}
        elif method == "tools/list":
            res = {"tools": tool_list(st)}
        elif method == "tools/call":
            doc, changed = handle(st, params["name"], params.get("arguments", {}))
            res = {"content": [{"type": "text", "text": json.dumps(doc, sort_keys=True)}], "structuredContent": doc}
            save(state_dir, st)
        else:
            res = None
        out = {"jsonrpc": "2.0", "id": rid}
        if res is None:
            out["error"] = err
        else:
            out["result"] = res
        sys.stdout.write(json.dumps(out) + "\n")
        sys.stdout.flush()
    return 0


def cli_main(state_dir, words, json_arg):
    if not (Path(state_dir) / "state.json").exists() or load(state_dir)["endpoint"] != "up":
        sys.stderr.write("sh1: endpoint unavailable (controller not running)\n")
        return 69
    st = load(state_dir)
    args = json.loads(json_arg) if json_arg else {}
    if words[0] == "call":
        name = words[1]
    elif words[0] == "observe":
        name, args = "observe", {"proposal_identity": words[1]}
    elif words[0] == "submit":
        name, args = "submit", {"proposal": args}
    else:
        name = words[0]
    doc, changed = handle(st, name, args)
    save(state_dir, st)
    if os.environ.get("SH1_STDERR_NOTE"):
        sys.stderr.write("sh1: note: controller log rotated\n")
    sys.stdout.write(json.dumps(doc, sort_keys=True) + "\n")
    return 0


# ------------------------------------------------- person and host controls

def person_main(state_dir, words):
    st = load(state_dir)
    verb = words[0]
    out = {}
    if verb == "enable":
        st["enablement"] = {"record": "in_force", "capture_evidence_reference": f"SH1-CAP-{st['next_act']}"}
        st["next_act"] += 1
    elif verb == "disable":
        st["enablement"] = {"record": "not_in_force"}
    elif verb == "stop-endpoint":
        st["endpoint"] = "down"
    elif verb == "start-endpoint":
        st["endpoint"] = "up"
    elif verb == "edit":
        sid, attr, value = words[1], words[2], words[3]
        st["model"][sid][attr] = value
        commit(st)
    elif verb in ("accept", "reject"):
        pid, item = words[1], words[2]
        for it in st["proposals"][pid]["items"]:
            if it["item_identity"] == item and it["state"] == "queued":
                kind = "A5" if verb == "accept" else "A10"
                it["state"] = "accepted" if verb == "accept" else "rejected"
                it["decision"] = {"act_kind": kind, "actor": PERSON, "act_reference": f"ACT-{st['next_act']}",
                                  "capture_evidence_reference": f"SH1-CAP-{st['next_act']}"}
                st["next_act"] += 1
    elif verb == "grant-direct":
        st["settings"]["P-03"] = {"display_state": "effective_person_set", "grant_value": "direct",
                                  "scope": words[1:], "reference": "set-2"}
    elif verb == "publish-edition":
        old = st["edition"]
        st["edition"] = "e2"
        ev = {"host_identity": HOST, "from_edition": old, "to_edition": "e2",
              "added": [{"operation_identity": "OP-C9", "operation_version": "v1"}], "removed": [], "changed": [],
              "published_at": tick(st), "reporter": "host"}
        st["edition_events"].append(ev)
        out = ev
    else:
        raise SystemExit(f"unknown person verb {verb}")
    tick(st)
    save(state_dir, st)
    print(json.dumps(out or {"ok": verb}))
    return 0


def host_main(state_dir, words):
    st = load(state_dir)
    if words[0] == "apply":
        p = st["proposals"][words[1]]
        relied = p["request"]["relied_on_basis"][0]
        for rec in p["items"]:
            if rec["state"] != "accepted":
                continue
            it = next(i for i in p["request"]["items"] if i["item_identity"] == rec["item_identity"])
            bad = stale_targets(st, it)
            if bad:
                rec["state"] = "refused_stale"
                rec["refusal"] = {"reason": f"{', '.join(bad)} changed after acceptance", "failing_targets": bad,
                                  "staleness_scope": "per_item_relied_on_targets", "relied_on_basis": relied,
                                  "evaluated_basis": basis(st)}
            else:
                apply_item(st, it, rec, relied, "after_acceptance")
    tick(st)
    save(state_dir, st)
    print(json.dumps({"ok": words[0]}))
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("mode", choices=["init", "mcp", "cli", "person", "host", "dump"])
    ap.add_argument("words", nargs="*")
    ap.add_argument("--state", required=True)
    ap.add_argument("--json")
    ap.add_argument("--profile", default="full", choices=["full", "no-lineage"])
    ap.add_argument("--edition", default="e2", choices=["e1", "e2"])
    a = ap.parse_args(argv)
    if a.mode == "init":
        Path(a.state).mkdir(parents=True, exist_ok=True)
        save(a.state, initial_state(a.profile, a.edition))
        return 0
    if a.mode == "mcp":
        return mcp_main(a.state)
    if a.mode == "cli":
        return cli_main(a.state, a.words, a.json)
    if a.mode == "person":
        return person_main(a.state, a.words)
    if a.mode == "host":
        return host_main(a.state, a.words)
    if a.mode == "dump":
        print(json.dumps(load(a.state), indent=1))
        return 0


if __name__ == "__main__":
    sys.exit(main())
