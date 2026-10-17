#!/usr/bin/env python3
"""SH-1 profile `swbpipe` (C-v0.8 §10.8): the simulated host in SWBPIPE's form.

A test double, not product code and not a model of SWBPIPE's implementation.
It reuses SH-1 (`simhost.py`, imported and left unchanged, so the SH-1 files
that other deliverables' rehearsal records pin keep their bytes) and changes
only what SWBPIPE's sources show at the commit pinned in DEL-03-02
`Design/swbpipe-corpus-pins.json`:

  * one identity, over the whole model, standing for every subject (SQ-03;
    R8-4); no workspace identity or generation (SQ-07 (a), host declares none);
    staleness scope: the whole model (SQ-07 (d));
  * no act-performing entries (SQ-01): no A4, A5 or A10 operation;
  * a submission is validated as a whole (atomic batch, SQ-09 (b); P VP-2): one
    failure refuses every item; a relied-on basis that is not the current
    whole-model identity refuses every item stale, failing targets not supplied;
  * no direct mode and no direct change call: host-reported *not exposed on
    this surface* (unsupported_method, SQ-06), never *not permitted*;
  * no observation by identity on main (SQ-08): *observe* is not offered and is
    answered *not exposed*; no de-duplication by identity (SQ-08), so a
    resubmission is checked like a first receipt, against the current model;
  * no enablement facility (SQ-13, SQ-28): the host answers without an A13;
  * the person's controls are SWBPIPE's: **apply** (one atomic application of a
    queued submission, one commit, recording only the host-stated acceptance
    basis "user_initiated_apply_in_local_session" and a session receipt, both in
    the double's own state, readable by no agent path, and no per-item act),
    **clear** (discards queued submissions with no record) and **restart**
    (session records lost). There is no accept, reject, grant or enable control.

Elements the App schemas require that SWBPIPE does not supply are supplied by
the double and are not SWBPIPE behaviour: the change-item content identity
(method ⟨m-sh1⟩; SWBPIPE NR-04), the model revision (SWBPIPE NR-06) and the
recorded-state fields of a submission answer (SWBPIPE NR-08). The whole-model
identity label ⟨m-sh1-wm⟩ is the double's own; SWBPIPE's is sha256 over RFC 8785
canonical JSON of the model payload.

Usage is SH-1's: `simhost_swbpipe.py init|mcp|cli|person|dump ... --state DIR`.
Person verbs: apply PID, clear, restart, edit SID ATTR VALUE, stop-endpoint,
start-endpoint. Python 3 standard library only.
"""

import sys

sys.dont_write_bytecode = True

import argparse  # noqa: E402
import copy  # noqa: E402
import json  # noqa: E402
from pathlib import Path  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent))
import simhost as sh  # noqa: E402

WM_METHOD = "m-sh1-wm"
PROFILE = "swbpipe"
ACCEPTANCE = {"acceptance_basis": "user_initiated_apply_in_local_session",     # host-stated; no actor, act or time
              "acceptance_is_professional_approval": False,
              "persistence_status": "session_state_only_not_yet_saved"}
_entries, _read_op = sh.entries, sh.read_op


def whole(model):
    return sh.cid(model)


def basis(st, revision=None, model=None, content=None):
    revision = st["revision"] if revision is None else revision
    model = st["model"] if model is None else model
    return {"workspace_identity": {"not_supplied": "host_declares_none"},
            "generation": {"not_supplied": "host_declares_none"},
            "model_revision": f"r{revision}",
            "canonical_content_identity": whole(model),       # the read-level identity is the whole model's
            "identity_method": WM_METHOD}


def basis_profile(st):
    return {"workspace_identity": "not_supplied", "generation": "not_supplied", "model_revision": "supplied",
            "canonical_content_identity": "supplied", "subject_content_identity": "whole_model_only",
            "staleness_scope": "whole_model"}


def entries(st):
    return [e for e in _entries(st) if e["operation_identity"] not in ("OP-C6", "OP-C7", "OP-C8")]


def read_op(st, op, args):
    doc = _read_op(st, op, args)
    if doc.get("outcome") != "success":
        return doc
    rev = doc["basis"]["model_revision"].lstrip("r")
    model = st["history"].get(rev, st["model"])
    for view in doc["views"]:
        for table in view["tables"]:
            for row in table["rows"]:
                row["subject"] = {"subject_identity": row["subject"]["subject_identity"],
                                  "subject_content_identity": whole(model), "identity_method": WM_METHOD,
                                  "identity_scope": "whole_model"}
    return doc


def change_entry(st, op):
    e = sh.entry(st, op)
    return e if e is not None and e["effects"]["kind"] == "change" else None


def not_exposed(name, version="unknown"):
    return sh.non_success("not_exposed_on_this_surface", "host",
                          operation={"operation_identity": name, "operation_version": version}, surface="X")


def answer(st, pid, items):
    return {"kind": "recorded_state", "proposal_identity": pid, "dedup_scope": "not_stated",
            "submissions_recorded": 1, "answered_from_recorded_state": False, "items": items,
            "derived_state": sh.derived(items), "observed_at": sh.tick(st), "current_basis": basis(st)}


def submit(st, req):
    pid = req["proposal_identity"]["value"]
    first = req["items"][0]
    if req["requested_mode"] != "propose":                      # SQ-06: unsupported_method
        return not_exposed(first["operation_identity"], first["operation_version"])
    if any(change_entry(st, it["operation_identity"]) is None for it in req["items"]):   # unsupported_change
        bad = next(it for it in req["items"] if change_entry(st, it["operation_identity"]) is None)
        return not_exposed(bad["operation_identity"], bad["operation_version"])
    relied = req["relied_on_basis"][0]
    items = [{"item_identity": it["item_identity"], "change_item_content_identity": sh.item_content(it, relied),
              "identity_method": sh.METHOD} for it in req["items"]]          # double-supplied (SWBPIPE NR-04)
    now_basis = basis(st)
    if relied.get("canonical_content_identity") != whole(st["model"]):
        refusal = {"reason": "the model changed since the relied-on basis (host scope: whole model)",
                   "failing_targets_not_supplied": True, "staleness_scope": "whole_model",
                   "relied_on_basis": relied, "evaluated_basis": now_basis}
        for rec in items:
            rec |= {"state": "refused_stale", "refusal": dict(refusal),
                    "item_left": sh.item_left(st, "refused_stale", now_basis)}
    else:
        failing = [it["item_identity"] for it in req["items"] if it["operation_identity"] == "OP-C4" and any(
            st["model"][s]["location_m"] == it["new_value"]
            for s in st["model"][it["affected_object"].get("object_identity", "R-100")]["supports"])]
        if failing:                                              # atomic: one failure refuses every item (VP-2)
            refusal = {"reason": f"submission refused as a whole: item {', '.join(failing)}: a support already stands there",
                       "error_identity": "E-location-occupied", "evaluated_basis": now_basis}
            for rec in items:
                rec |= {"state": "refused_invalid", "refusal": dict(refusal),
                        "item_left": sh.item_left(st, "refused_invalid", now_basis)}
        else:
            for rec in items:
                rec["state"] = "queued"
            st["swb_queue"].append({"proposal_identity": pid, "request": req, "items": copy.deepcopy(items),
                                    "status": "queued"})
    return answer(st, pid, items)


def handle(st, name, args):
    """No enablement facility: the host answers without an A13 (SQ-13, SQ-28)."""
    if name in ("read-catalog", "catalog"):
        return sh.catalog_doc(st), False
    if name in ("read-edition-events", "events"):
        return {"host_identity": sh.HOST, "edition": st["edition"], "events": st["edition_events"]}, False
    if name in ("submit-proposal", "submit"):
        return submit(st, args["proposal"]), True
    if name in ("observe-proposal", "observe"):               # SQ-08: no observation by identity on main
        return not_exposed("observe-proposal"), False
    e = sh.entry(st, name)
    if e is None or e["effects"]["kind"] == "change":         # SQ-06: no direct change call
        return not_exposed(name, e["operation_version"] if e else "unknown"), False
    return read_op(st, name, args), False


def mcp_main(state_dir):
    st0 = sh.load(state_dir)
    if st0["endpoint"] != "up":
        sys.stderr.write("SH-1/swbpipe: endpoint unavailable (controller not running)\n")
        return 69
    for line in sys.stdin:
        if not line.strip():
            continue
        req = json.loads(line)
        st = sh.load(state_dir)
        rid, method, params = req.get("id"), req.get("method"), req.get("params", {})
        out = {"jsonrpc": "2.0", "id": rid}
        if method == "initialize":
            out["result"] = {"serverInfo": {"name": "sh1-simulated-host-swbpipe-profile", "version": "0.1-test-double"},
                             "capabilities": {"tools": {}}}
        elif method == "tools/list":
            out["result"] = {"tools": sh.tool_list(st)}
        elif method == "tools/call":
            doc, _ = handle(st, params["name"], params.get("arguments", {}))
            out["result"] = {"content": [{"type": "text", "text": json.dumps(doc, sort_keys=True)}], "structuredContent": doc}
            sh.save(state_dir, st)
        else:
            out["error"] = {"code": -32601, "message": f"method not found: {method}"}
        sys.stdout.write(json.dumps(out) + "\n")
        sys.stdout.flush()
    return 0


def apply_effects(st, it):
    op = it["operation_identity"]
    if op == "OP-C4":
        n = 1 + max(int(k.split("-")[1]) for k in st["model"] if k.startswith("S-"))
        run = it["affected_object"].get("object_identity", "R-100")
        st["model"][f"S-{n}"] = {"kind": "support", "run": run, "location_m": it["new_value"], "type": "guide",
                                 "stiffness": "2.0e6", "label": f"G-{n}"}
        st["model"][run]["supports"].append(f"S-{n}")
    else:
        st["model"][it["affected_object"]["object_identity"]][it["attribute"]] = it["new_value"]


def person_main(state_dir, words):
    st = sh.load(state_dir)
    verb, out = words[0], {"ok": words[0]}
    if verb == "apply":                      # the person's Apply: one atomic application, no per-item act
        entry = next((e for e in reversed(st["swb_queue"]) if e["proposal_identity"] == words[1]
                      and e["status"] == "queued"), None)
        if entry is None:
            out["result"] = "nothing queued under that identity"
        elif entry["request"]["relied_on_basis"][0].get("canonical_content_identity") != whole(st["model"]):
            entry["status"] = "refused_stale_at_apply"          # whole-model scope; nothing applied, no record of an act
            out["result"] = entry["status"]
        else:
            for it in entry["request"]["items"]:
                apply_effects(st, it)
            sh.commit(st)                                       # one batch = one application
            receipt = f"applied-{len(st['swb_receipts']) + 1}"
            st["swb_receipts"].append({"receipt_id": receipt, "proposal_identity": words[1],
                                       "applied_model_identity": whole(st["model"]), "acceptance": dict(ACCEPTANCE)})
            entry["status"] = "applied_in_session"
            out["result"] = {"status": entry["status"], "session_receipt": receipt, "acceptance": dict(ACCEPTANCE)}
    elif verb == "clear":                    # discards every queued submission with no record (SQ-01)
        n = sum(1 for e in st["swb_queue"] if e["status"] == "queued")
        st["swb_queue"] = [e for e in st["swb_queue"] if e["status"] != "queued"]
        out["result"] = f"{n} queued submission(s) discarded; no record kept"
    elif verb == "restart":                  # session records are lost (SQ-01, SQ-08 (c))
        st["swb_queue"], st["swb_receipts"] = [], []
    elif verb in ("edit", "stop-endpoint", "start-endpoint"):
        return sh.person_main(state_dir, words)
    else:
        raise SystemExit(f"profile swbpipe has no person control '{verb}' (no accept, reject, grant or enable)")
    sh.tick(st)
    sh.save(state_dir, st)
    print(json.dumps(out))
    return 0


def install():
    """Route SH-1's own functions to the profile's (module globals are looked up at call time)."""
    sh.basis, sh.basis_profile, sh.entries, sh.read_op = basis, basis_profile, entries, read_op
    sh.handle = handle
    sh.ROUTE_TOOLS = {k: v for k, v in sh.ROUTE_TOOLS.items() if v != "observe"}


def main(argv=None):
    install()
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("mode", choices=["init", "mcp", "cli", "person", "dump"])
    ap.add_argument("words", nargs="*")
    ap.add_argument("--state", required=True)
    ap.add_argument("--json")
    ap.add_argument("--profile", default=PROFILE, choices=[PROFILE])
    ap.add_argument("--edition", default="e2", choices=["e1", "e2"])
    a = ap.parse_args(argv)
    if a.mode == "init":
        Path(a.state).mkdir(parents=True, exist_ok=True)
        st = sh.initial_state(PROFILE, a.edition)
        st["enablement"] = {"record": "no_facility"}
        st["settings"] = {}
        st |= {"swb_queue": [], "swb_receipts": []}
        sh.save(a.state, st)
        return 0
    if a.mode == "mcp":
        return mcp_main(a.state)
    if a.mode == "cli":
        return sh.cli_main(a.state, a.words, a.json)
    if a.mode == "person":
        return person_main(a.state, a.words)
    print(json.dumps(sh.load(a.state), indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
