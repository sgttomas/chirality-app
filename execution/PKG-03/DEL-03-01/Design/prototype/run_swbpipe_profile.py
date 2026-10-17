#!/usr/bin/env python3
"""Drive SH-1 profile `swbpipe` (simhost_swbpipe.py) over both native paths.

Prototype only (R12-3); Python 3 standard library. Like run_fixture.py it plays
the App's Codex and imitates the supplier's `mcpToolCall` / `commandExecution`
items; nothing here observes Codex or SWBPIPE. It APPENDS its run (named
`swbpipe`) to an SH-1 run directory, so validate_all.py --run, the ADAPTER
mapper (DEL-03-03 observe_map.py --run) and the P state check (DEL-03-02
proposal_states.py --check) check it beside the full-profile run:

  python3 run_fixture.py --out "$D" && python3 run_swbpipe_profile.py --out "$D"

It prints one PASS/FAIL line per check; exit status 1 if any check fails.
`--write-examples` rewrites `../swbpipe-profile-documents.json`, the profile's
documents that the App's receiving tests read (app/src-tauri/tests/
swbpipe_receiving.rs); without it the run checks that file equals this run's.
Evidence label: test-double. It establishes nothing about SWBPIPE.
"""

import sys

sys.dont_write_bytecode = True

import argparse  # noqa: E402
import json  # noqa: E402
import os  # noqa: E402
import subprocess  # noqa: E402
from pathlib import Path  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent))
import run_fixture as rf  # noqa: E402

SWBSIM = [sys.executable, "-B", str(rf.PROTO / "simhost_swbpipe.py")]
EXAMPLES = rf.PROTO.parent / "swbpipe-profile-documents.json"


class SwbRun(rf.Run):
    def sim(self, mode, *words, json_arg=None, env=None, profile=None, edition=None):
        cmd = SWBSIM + [mode] + list(words) + ["--state", str(self.state)]
        if json_arg is not None:
            cmd += ["--json", json_arg]
        if edition:
            cmd += ["--edition", edition]
        e = dict(os.environ)
        e.update(env or {})
        return subprocess.run(cmd, capture_output=True, text=True, env=e)

    def start_mcp(self):
        self.mcp = subprocess.Popen(SWBSIM + ["mcp", "--state", str(self.state)], stdin=subprocess.PIPE,
                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        self.rpc_id = 0
        if self.rpc("initialize", {}) is None:
            err = self.mcp.stderr.read()
            self.mcp = None
            return err.strip()
        return None

    def state_doc(self):
        return json.loads((self.state / "state.json").read_text())


def subjects_identical_to_whole_model(doc):
    whole = doc["basis"]["canonical_content_identity"]
    rows = [r["subject"] for t in doc["views"][0]["tables"] for r in t["rows"]]
    return rows and all(s["subject_content_identity"] == whole and s["identity_scope"] == "whole_model" for s in rows)


def timeline(out, checks):
    r = SwbRun(out, "swbpipe", profile="swbpipe")
    # Channel facts in SWBPIPE's form (SQ-13, SQ-28): no A13 facility; the host answers anyway.
    for ev in ({"event": "app_configuration_added", "directed_by": "person", "path": "N-MCP", "locus": "per_thread_configuration"},
               {"event": "app_configuration_added", "directed_by": "person", "path": "N-CLI", "locus": "command_on_path"},
               {"event": "endpoint_ready", "locality": "local_process"},
               {"event": "host_enablement_observed", "record": "no_facility"},
               {"event": "host_answer_without_A13"}):
        r.chan(**ev)
    assert r.start_mcp() is None
    r.mcp_status("SW-D")
    status = r.items[-1]
    cat_m = r.mcp_call("SW-D", "read-catalog", {})
    cat_c = r.cli("SW-D", ["catalog"])
    ops = [e["operation_identity"] for e in cat_c["entries"]]
    checks.append(("SW-D discovery identical on both paths; basis profile whole-model only, scope whole model, "
                   "no workspace identity or generation; no act-performing entries; no observe tool",
                   cat_m == cat_c and cat_c["basis_profile"] == {
                       "workspace_identity": "not_supplied", "generation": "not_supplied", "model_revision": "supplied",
                       "canonical_content_identity": "supplied", "subject_content_identity": "whole_model_only",
                       "staleness_scope": "whole_model"}
                   and not {"OP-C6", "OP-C7", "OP-C8"} & set(ops) and "observe-proposal" not in status["item"]["tools"]))
    rm = r.mcp_call("SW-R1", "OP-C1", {"run": "R-100"})
    rc = r.cli("SW-R1", ["call", "OP-C1"], json.dumps({"run": "R-100"}))
    B1 = rc["basis"]
    checks.append(("SW-R1 read identical on both paths; every row's subject identity is the whole-model identity "
                   "(scope whole_model); workspace identity and generation host_declares_none",
                   rm == rc and subjects_identical_to_whole_model(rc)
                   and B1["workspace_identity"] == B1["generation"] == {"not_supplied": "host_declares_none"}))
    s1, run1 = rf.rows_of(rc, "supports"), rf.rows_of(rc, "run")
    w1 = rf.proposal("PR-W1", B1, s1, [
        {"item_identity": "1", "operation_identity": "OP-C5", "operation_version": "v1",
         "affected_object": {"object_identity": "S-3"}, "relied_on_targets": [rf.target(s1, "S-3")],
         "attribute": "stiffness", "old_value": "rigid", "new_value": "1.8e6"},
        {"item_identity": "2", "operation_identity": "OP-C9", "operation_version": "v1",
         "affected_object": {"object_identity": "S-4"}, "relied_on_targets": [rf.target(s1, "S-4")],
         "attribute": "label", "old_value": "G-4a", "new_value": "G-4b"}], reason="Relax S-3; relabel S-4")
    p1 = r.cli("SW-P1", ["submit"], json.dumps(w1))
    checks.append(("SW-P1 PR-W1 queued (2 items); de-duplication scope not stated; no host handle; nothing accepted",
                   p1["derived_state"] == {"summary": "queued", "counts": {"queued": 2}, "open": True, "all_items_decided": False}
                   and p1["dedup_scope"] == "not_stated" and "host_handles" not in p1
                   and all("decision" not in i for i in p1["items"])))
    w2 = rf.proposal("PR-W2", B1, s1, [
        {"item_identity": "1", "operation_identity": "OP-C5", "operation_version": "v1",
         "affected_object": {"object_identity": "S-1"}, "relied_on_targets": [rf.target(s1, "S-1")],
         "attribute": "stiffness", "old_value": "2.0e6", "new_value": "2.5e6"}], reason="Stiffen S-1")
    p2 = r.mcp_call("SW-P2", "submit-proposal", {"proposal": w2})
    checks.append(("SW-P2 PR-W2 queued (1 item)", p2["derived_state"]["summary"] == "queued"))
    om = r.mcp_call("SW-O", "observe-proposal", {"proposal_identity": "PR-W1"})
    oc = r.cli("SW-O", ["observe", "PR-W1"])
    checks.append(("SW-O no observation by identity: host-reported not exposed on both paths (SQ-08)",
                   om == oc and oc["outcome"] == "not_exposed_on_this_surface" and oc["reporter"] == "host"))
    w3 = dict(w2, proposal_identity={"value": "PR-W3", "minted_by": "proposer"}, requested_mode="apply_directly")
    d3 = r.cli("SW-X1", ["submit"], json.dumps(w3))
    dc = r.mcp_call("SW-X2", "OP-C5", {"support": "S-1", "stiffness": "2.5e6"})
    checks.append(("SW-X direct submission and direct change call: not exposed (unsupported_method), never not permitted",
                   d3["outcome"] == dc["outcome"] == "not_exposed_on_this_surface"))
    applied = r.person("apply", "PR-W1")                                   # the person's Apply in the host
    st = r.state_doc()
    queue = {e["proposal_identity"]: e for e in st["swb_queue"]}
    checks.append(("SW-A1 the person's Apply applies PR-W1 as one batch (one commit, r13); the host keeps only its "
                   "stated acceptance basis and a session receipt, no per-item act; no agent path can read either",
                   applied["result"]["status"] == "applied_in_session" and st["revision"] == 13
                   and applied["result"]["acceptance"]["acceptance_basis"] == "user_initiated_apply_in_local_session"
                   and all("decision" not in i for i in queue["PR-W1"]["items"])
                   and "actor" not in json.dumps(st["swb_receipts"])))
    r2 = r.cli("SW-R2", ["call", "OP-C1"], json.dumps({"run": "R-100"}))
    s2 = rf.rows_of(r2, "supports")
    checks.append(("SW-R2 after Apply every subject identity changed, including S-1 and S-2 whose content did not "
                   "(whole model: errs toward reporting a change, R8-4)",
                   r2["basis"]["model_revision"] == "r13" and subjects_identical_to_whole_model(r2)
                   and all(s2[k]["subject_content_identity"] != s1[k]["subject_content_identity"] for k in ("S-1", "S-2"))))
    stale_apply = r.person("apply", "PR-W2")
    checks.append(("SW-A2 the person's Apply of PR-W2 is refused stale inside the host (whole-model scope); nothing "
                   "applied; no agent path observes it", stale_apply["result"] == "refused_stale_at_apply"
                   and r.state_doc()["revision"] == 13))
    w4 = rf.proposal("PR-W4", B1, s1, [w2["items"][0]], reason="Stiffen S-1 (stale basis)")
    p4 = r.mcp_call("SW-P4", "submit-proposal", {"proposal": w4})
    checks.append(("SW-P4 a submission on the earlier basis: every item refused stale, scope whole model, failing "
                   "targets not supplied, relied B1 and current r13, item-left event, no act",
                   all(i["state"] == "refused_stale" and i["refusal"]["staleness_scope"] == "whole_model"
                       and i["refusal"]["failing_targets_not_supplied"] and i["refusal"]["relied_on_basis"] == B1
                       and i["refusal"]["evaluated_basis"]["model_revision"] == "r13"
                       and i["item_left"]["cause"] == "refused_stale" and "decision" not in i for i in p4["items"])))
    B2, run2 = r2["basis"], rf.rows_of(r2, "run")
    w5 = rf.proposal("PR-W5", B2, s2, [
        {"item_identity": "1", "operation_identity": "OP-C5", "operation_version": "v1",
         "affected_object": {"object_identity": "S-2"}, "relied_on_targets": [rf.target(s2, "S-2")],
         "attribute": "stiffness", "old_value": "rigid", "new_value": "3.0e6"},
        {"item_identity": "2", "operation_identity": "OP-C4", "operation_version": "v1",
         "affected_object": {"object_identity": "R-100"}, "relied_on_targets": [rf.target(run2, "R-100")],
         "attribute": "created", "old_value": None, "new_value": 2.0}], reason="Stiffen S-2; add a support at 2.0 m")
    p5 = r.cli("SW-P5", ["submit"], json.dumps(w5))
    checks.append(("SW-P5 atomic validation: one invalid item refuses both items with the same reason (VP-2), "
                   "item-left events, no act",
                   [i["state"] for i in p5["items"]] == ["refused_invalid", "refused_invalid"]
                   and len({i["refusal"]["reason"] for i in p5["items"]}) == 1
                   and all(i["item_left"]["cause"] == "refused_invalid" for i in p5["items"])))
    w6 = rf.proposal("PR-W6", B2, s2, [dict(w5["items"][0])], reason="Stiffen S-2")
    r.mcp_call("SW-P6", "submit-proposal", {"proposal": w6}, drop=True)
    o6 = r.cli("SW-P6o", ["observe", "PR-W6"])
    checks.append(("SW-P6 a submission whose answer is lost cannot be observed (not exposed): its outcome stays unknown",
                   o6["outcome"] == "not_exposed_on_this_surface"))
    cleared = r.person("clear")
    checks.append(("SW-C the person's Clear discards PR-W6 with no record (no A10, no item-left event in the host)",
                   cleared["result"].startswith("1 ") and all(e["proposal_identity"] != "PR-W6" for e in r.state_doc()["swb_queue"])))
    again = r.cli("SW-P7", ["submit"], json.dumps(w1))
    checks.append(("SW-P7 resubmitting applied PR-W1 is not de-duplicated: it is checked like a first receipt and "
                   "refused stale by its own effect (contrary to P §5 precedence; SWBPIPE NR-08)",
                   not again["answered_from_recorded_state"] and all(i["state"] == "refused_stale" for i in again["items"])))
    r.person("restart")
    checks.append(("SW-S restart: session records (queue and receipts) are lost; the model is kept",
                   r.state_doc()["swb_queue"] == [] and r.state_doc()["swb_receipts"] == [] and r.state_doc()["revision"] == 13))
    r.stop_mcp()
    r.requests = {"PR-W1": w1, "PR-W4": w4, "PR-W6": w6}
    return r


def documents(r):
    """The documents the App's receiving tests read: N-CLI copies (the MCP ones are checked identical above)."""
    doc = {d["step"]: d["doc"] for d in r.docs if d["path"] == "N-CLI"}
    return {"document_kind": "sh1_swbpipe_profile_documents", "evidence_label": "test-double",
            "statement": ("Host documents of SH-1 profile swbpipe (C-v0.8 section 10.8), in the App's PROPOSED schemas. "
                          "A test double: they establish nothing about SWBPIPE. Change-item content identities and "
                          "model revisions are supplied by the double (SWBPIPE NR-04, NR-06)."),
            "generator": "DEL-03-01 Design/prototype/run_swbpipe_profile.py --write-examples",
            "catalog": doc["SW-D"], "read_before_apply": doc["SW-R1"], "read_after_apply": doc["SW-R2"],
            "requests": r.requests,
            "states": {"PR-W1 queued": doc["SW-P1"], "PR-W4 refused stale": next(d["doc"] for d in r.docs if d["step"] == "SW-P4"),
                       "PR-W5 refused invalid": doc["SW-P5"], "PR-W1 resubmitted after Apply": doc["SW-P7"]},
            "observation_not_exposed": doc["SW-O"]}


def append(out, name, rows):
    with open(out / name, "a") as f:
        for x in rows:
            f.write(json.dumps(x) + "\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True, help="an SH-1 run directory (run_fixture.py --out); the run is appended")
    ap.add_argument("--write-examples", action="store_true")
    a = ap.parse_args()
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    checks = []
    r = timeline(out, checks)
    append(out, "native_items.jsonl", r.items)
    append(out, "host_docs.jsonl", r.docs)
    append(out, "channel_events.jsonl", r.channel)
    (out / "summary-swbpipe.json").write_text(json.dumps({"checks": [[n, ok] for n, ok in checks]}, indent=1))
    docs = documents(r)
    if a.write_examples:
        EXAMPLES.write_text(json.dumps(docs, indent=1, sort_keys=True) + "\n")
    checks.append((f"{EXAMPLES.name} equals this run's profile documents",
                   EXAMPLES.exists() and json.loads(EXAMPLES.read_text()) == docs))
    failed = 0
    print("SH-1 profile swbpipe, run appended to:", out)
    for name, ok in checks:
        print(("PASS " if ok else "FAIL ") + name)
        failed += 0 if ok else 1
    print(f"\n{len(checks) - failed} of {len(checks)} checks passed; items recorded: {len(r.items)}; "
          f"host documents: {len(r.docs)}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
