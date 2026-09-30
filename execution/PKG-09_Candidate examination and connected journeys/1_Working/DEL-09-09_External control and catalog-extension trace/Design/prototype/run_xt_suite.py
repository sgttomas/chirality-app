#!/usr/bin/env python3
"""XT suite rehearsal on the simulated host SH-1 (DEL-09-09 XT-v0.6 §3.4–§3.6,
§5.1.1; run APP-V4-DESIGN-PASS-2-20260930, node B7).

Prototype only (R12-3): Python 3 standard library, no package, no network,
not product code. It runs the XC and TR rehearsals that SH-1 can carry, in
the suite order of XT §3.5 (segments, saved branch points, set-up and reset
per case), writes one XT result record per case (`xt-result-record.schema.json`)
and the V-ED1 work account (`xt-work-account.schema.json`), validates them,
and checks the committed example instances.

What it drives (round-1 prototypes, used read-only and unchanged):
  * SH-1, the one simulated host (DEL-03-01 C-v0.8 §10.8; `simhost.py` through
    `run_fixture.py`), over both native paths;
  * the ADAPTER-v0.6 §4.6 mapper (`observe_map.py`) for the App-side dispatch
    records (J-3, J-8 in part) the App would write from those items.

Evidence label: test_double (not_observed where a part did not run). Nothing
here is an observation of Codex, of SWBPIPE or of any host; no record counts
toward V4-EXM-25 or V4-EXM-24 (XT §0, §3.3, §4.5).

Usage:  python3 -B run_xt_suite.py [--out DIR] [--write-examples]
Exit status 0 only if every check holds.
"""

import sys

sys.dont_write_bytecode = True

import argparse  # noqa: E402
import copy  # noqa: E402
import datetime  # noqa: E402
import hashlib  # noqa: E402
import json  # noqa: E402
import os  # noqa: E402
import platform  # noqa: E402
import shutil  # noqa: E402
from pathlib import Path  # noqa: E402

HERE = Path(__file__).resolve().parent
DESIGN = HERE.parent
EXEC_ROOT = DESIGN.parents[3]
C_PROTO = next(EXEC_ROOT.glob("PKG-03_*/1_Working/DEL-03-01_*/Design/prototype"))
A_PROTO = next(EXEC_ROOT.glob("PKG-03_*/1_Working/DEL-03-03_*/Design/prototype"))
for p in (C_PROTO, A_PROTO):
    sys.path.insert(0, str(p))

import schema_subset as ss   # noqa: E402  (DEL-03-01; the validator subset)
import run_fixture as rf     # noqa: E402  (DEL-03-01; SH-1 driver)
import observe_map as om     # noqa: E402  (DEL-03-03; OM-1…OM-10)

RESULT_SCHEMA = DESIGN / "xt-result-record.schema.json"
ACCOUNT_SCHEMA = DESIGN / "xt-work-account.schema.json"
EXAMPLES = {
    "xt-result-record.example.valid.json": RESULT_SCHEMA,
    "xt-result-record.example.invalid.json": RESULT_SCHEMA,
    "xt-work-account.example.valid.json": ACCOUNT_SCHEMA,
    "xt-work-account.example.invalid.json": ACCOUNT_SCHEMA,
}
TODAY = datetime.date.today().isoformat()
FAILS = []

# XT §3.5 suite plan: (order, case, segment, starts from, reset after). The prose table in §3.5 is the definition;
# this list is its executable copy and is checked against the order actually run.
SUITE = [
    (1, "XC-00", "M", "fresh fixture state", "none (identification only)"),
    (2, "XC-01", "M", "fresh fixture state, channel never enabled", "none: continue M with the channel enabled"),
    (3, "XC-11", "M", "M at r12 (T3)", "none: continue M"),
    (4, "XC-03", "M", "M after T4a", "none: continue M at r13"),
    (5, "XC-02", "M", "M at r13 after T8 (saves BP-T9, BP-T10, BP-T11)", "none: continue M at r14"),
    (6, "XC-09", "M", "M after T12 (reads XC-02's records)", "none: continue M"),
    (7, "XC-05", "M", "M after T12", "none: continue M"),
    (8, "XC-06", "M", "M after XC-05", "none: continue M"),
    (9, "XC-10", "M", "M after XC-06 (r14, <set-1>)", "none: TR-05 reads the same steps"),
    (10, "TR-05", "M", "M during XC-10 (T15-T16 on X)", "discard M"),
    (11, "XC-12", "B-T10", "BP-T10 (PR-2 queued, channel enabled)", "discard B-T10"),
    (12, "XC-07", "B-T11", "BP-T11 (items decided, not applied)", "discard"),
    (13, "XC-08", "B-T11", "BP-T11", "discard"),
    (14, "XC-05", "B-T9", "BP-T9 (B2 read, PR-2 not yet submitted): variant L-XT-2", "discard"),
    (15, "XC-04", "B-T10", "BP-T10", "discard"),
    (16, "TR-01", "B-E1", "fresh fixture state on edition e1", "discard"),
]


def check(label, cond, detail=""):
    print(("PASS " if cond else "FAIL ") + label + ((" -- " + detail) if detail and not cond else ""))
    if not cond:
        FAILS.append(label)
    return cond


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def rel(p):
    return str(Path(p).relative_to(EXEC_ROOT))


FILES = [C_PROTO / "simhost.py", C_PROTO / "run_fixture.py", A_PROTO / "observe_map.py"]
DOUBLE = {"double_identity": "SH-1 (with the ADAPTER-v0.6 mapper for App-side records)",
          "specified_in": "DEL-03-01 C-v0.8 §10.8",
          "files": [{"path": rel(f), "sha256": sha(f)} for f in FILES],
          "invented_material": "FX-PIPE-01 (C §10); SH-1 holds a subset (C §10.8)"}
CFG = {"realization_family": "both_on_double", "native_path": "both", "endpoint": "SH-1 local process (stdio) and command",
       "host_profile": "SH-1 full",
       "model_destination": {"not_observed": "the App's Codex is imitated, not run (OBS-1 pending)"}}
HOST_JOINS = ("an identified SWBPIPE candidate; host joins and caller naming deferred", "SWBPIPE owner (DECISION-3)", "SQ-27")
APP_CAND = ("an identified App candidate", "App construction (later undertaking)")
A13 = ("host A13 enablement facility with capture-evidence reference", "SWBPIPE owner", "SQ-28")


def aggregate(parts):
    outs = [p["outcome"] for p in parts]
    if "failed" in outs:
        return "failed"
    if "blocked" in outs:
        return "blocked"
    if all(o == "passed" for o in outs):
        return "passed"
    if all(o == "not_run" for o in outs):
        return "not_run"
    return "inconclusive"


def part(name, expectation, ok, *, chain=(), built_on=(), obs=(), not_run_because=None):
    p = {"part": name, "expectation": expectation}
    if not_run_because:
        p["outcome"], p["not_run_because"] = "not_run", not_run_because
    else:
        p["outcome"] = "passed" if ok else "failed"
    if chain:
        p["chain_elements"] = list(chain)
    if built_on:
        p["built_on"] = list(built_on)
    if obs:
        p["observations"] = [{"what": w, "reference": {"kind": k, "ref": r}, "linked_not_copied": True} for w, k, r in obs]
    return p


def record(case, parts, *, order, rehearsal_of=(), limits=(), missing=(), acts=(), comparisons=None, state="AWAITING INPUT"):
    plan = next(s for s in SUITE if s[1] == case and s[0] == order) if order else None
    ran = any(p["outcome"] != "not_run" for p in parts)
    rec = {"record_kind": "xt_result", "format": "proposed-0.1", "record_id": f"{case}/{order or 0}/{TODAY}",
           "case": case, "witness": "V4-EXM-24" if case.startswith("TR-") else "V4-EXM-25",
           "phase_reading": "current", "run_kind": "rehearsal" if plan else "definition_check",
           "evidence_label": ("test_double" if ran else "not_observed"),
           "case_state_at_run": state,
           "subject_of_run": DOUBLE if plan else {"definition_label": "DEL-09-09/XT-v0.6 §3.2, §4.4"},
           "configuration": CFG if plan else {"realization_family": "not_selected", "native_path": "not_applicable"},
           "date": TODAY,
           "suite_position": {"segment": plan[2], "order": plan[0], "starts_from": plan[3], "reset_after": plan[4]} if plan
           else {"segment": "none", "order": 99, "starts_from": "not run", "reset_after": "none"},
           "outcome": aggregate(parts), "parts": parts, "evidence_limits": sorted(set(limits)),
           "missing_inputs": [dict(zip(("input", "supplier", "relay_question"), m)) for m in missing],
           "completion": {"counts_toward_witness": False,
                          "reason": "a rehearsal on a test double never completes a joined case (XT §0, §3.3)" if plan
                          else "not run"}}
    if rehearsal_of:
        rec["rehearsal_of"] = list(rehearsal_of)
    if acts:
        rec["act_records_cited"] = list(acts)
    if comparisons is not None:
        rec["comparisons"] = comparisons
    return rec


# ------------------------------------------------------------------ SH-1 plumbing

class Seg:
    """One segment: an SH-1 state and the App's items so far (forks copy both)."""

    def __init__(self, out, name, edition="e2", parent=None):
        self.r = rf.Run(Path(out), name, edition=edition)
        self.name = name
        if parent is not None:
            shutil.copy(parent.r.state / "state.json", self.r.state / "state.json")
            self.r.items = [dict(copy.deepcopy(x), run=name) for x in parent.r.items]
            self.r.n = parent.r.n
        self.d = {}

    def mcp(self):
        assert self.r.start_mcp() is None

    def stop(self):
        self.r.stop_mcp()

    def state(self):
        return json.loads((self.r.state / "state.json").read_text())

    def dispatch(self):
        m = om.Mapper()
        return [m.map(x) for x in self.r.items]


def by_step(recs, step):
    return [x for x in recs if x["observed_at"] == step]


def discovery(seg, step):
    seg.r.mcp_status(step)
    seg.r.mcp_call(step, "read-catalog", {})
    seg.r.cli(step, ["catalog"])


# ------------------------------------------------------------------ the suite

def run_suite(out):
    run_order, recs = [], []
    M = Seg(out, "M")
    # 1 XC-00
    run_order.append("XC-00")
    recs.append(record("XC-00", [
        part("identification recorded before any result", "the double, its file digests, configuration and date are recorded first",
             True, obs=[(f"SH-1 digests; python {platform.python_version()}; {TODAY}", "run_output", "xt_results.jsonl#XC-00")]),
        part("App candidate (IN-01)", "build, stock Codex version, model and server", False, not_run_because="no App candidate (later undertaking)"),
        part("SWBPIPE candidate (IN-02)", "identified candidate and configuration", False,
             not_run_because="SQ-27 answered: a scheme, no candidate; host joins deferred (DECISION-3)"),
    ], order=1, missing=[APP_CAND, HOST_JOINS]))
    # 2 XC-01
    run_order.append("XC-01")
    M.mcp()
    off_m = M.r.mcp_status("CH-0")
    off_c = M.r.cli("CH-0", ["call", "OP-C1"], json.dumps({"run": "R-100"}))
    M.stop()
    M.r.person("stop-endpoint")
    down = M.r.cli("XF-06", ["call", "OP-C1"], json.dumps({"run": "R-100"}))
    err = M.r.start_mcp()
    M.r.person("start-endpoint")
    M.r.person("enable")
    cap = M.state()["enablement"]
    M.mcp()
    discovery(M, "D-1")
    recs.append(record("XC-01", [
        part("(a) never enabled: the App makes no host request and reports channel not enabled itself", "App-side configuration absent", False,
             not_run_because="SH-1 has no App side; the App-side states are ADAPTER's CT-1…CT-3, run in ADAPTER's prototype, not here"),
        part("(b) App configured, host off: host-reported channel not enabled on both paths", "same refusal on N-MCP and N-CLI; channel disabled",
             off_m["outcome"] == off_c["outcome"] == "channel_not_enabled" and off_c["reporter"] == "host",
             chain=["J-1"], built_on=["XF-02"], obs=[("CH-0 channel_not_enabled (host)", "host_document", "M/CH-0")]),
        part("(c) endpoint stopped: endpoint unavailable with reason", "CLI exits non-zero with no host document; MCP server does not start",
             down is None and err is not None, chain=["J-1"], built_on=["XF-06"], obs=[("XF-06 " + (err or ""), "run_output", "M/XF-06")]),
        part("(d) the person's A13 in the host facility: enabled, with the facility's capture reference", "enablement in force with a capture reference; grants unchanged",
             cap.get("record") == "in_force" and cap.get("capture_evidence_reference", "").startswith("SH1-CAP-")
             and M.state()["settings"]["P-03"]["grant_value"] == "propose",
             chain=["J-1"], built_on=["XF-01", "XF-03"], obs=[("enablement " + cap.get("capture_evidence_reference", "?"), "act_record", "M/enable")]),
        part("model destination shown and recorded, never gating", "per turn where reported", False, not_run_because="no supplier turn (OBS-1 pending)"),
    ], order=2, rehearsal_of=["XF-01", "XF-02", "XF-03", "XF-06"], missing=[A13, HOST_JOINS]))
    # 3 XC-11 (reads, check, unavailability; X paths only)
    run_order.append("XC-11")
    b1m = M.r.mcp_call("T3", "OP-C1", {"run": "R-100"})
    b1c = M.r.cli("T3", ["call", "OP-C1"], json.dumps({"run": "R-100"}))
    t4 = M.r.cli("T4", ["call", "OP-C3"], json.dumps({"run": "R-100", "spacing_limit_m": 6}))
    t4a = M.r.mcp_call("T4a", "OP-C12", {"run": "R-100"})
    B1 = b1m["basis"]
    s1, run1 = rf.rows_of(b1m, "supports"), rf.rows_of(b1m, "run")
    pr1 = rf.proposal("PR-1", B1, s1, rf.items_pr(s1, run1, "rigid"))
    # 4 XC-03 (intervening edit, stale); T8 unavailability for XC-11 on the way
    run_order.append("XC-03")
    M.r.person("edit", "S-3", "stiffness", "1.5e6")                                           # T6
    t7 = M.r.cli("T7", ["submit"], json.dumps(pr1))
    t8m = M.r.mcp_call("T8", "OP-C2", {"run": "R-100", "load_case": "LC-1"})
    t8c = M.r.cli("T8", ["call", "OP-C2"], json.dumps({"run": "R-100", "load_case": "LC-1"}))
    xc11_parts = [
        part("T3 read on X: same content, basis and subject identities on both native paths", "identical read documents", b1m == b1c,
             built_on=["XF-11", "VC-C-02"], obs=[("T3 basis " + B1["model_revision"], "host_document", "M/T3")]),
        part("T4 findings are the requester's (A3), T4a is a named host check with its basis; findings never 'checked'",
             "finding content only; host check failed: support spacing, evaluated at r12",
             "finding" in json.dumps(t4) and not (t4.get("standing") or {}).get("host_checks")
             and t4a["standing"]["host_checks"][0]["verdict"] == "failed",
             built_on=["XF-12"], obs=[("T4a host check failed", "host_document", "M/T4a")]),
        part("T8 unavailable with the same reason and evaluated basis on both paths", "unavailable, R-no-current-solve, basis r13",
             t8m == t8c and t8m["outcome"] == "unavailable" and t8m["unavailable_reason"]["reason_identity"] == "R-no-current-solve",
             built_on=["XF-08"], obs=[("T8 unavailable", "host_document", "M/T8")]),
        part("V-X1: host-reported not exposed on X", "element 9", False, built_on=["XF-09"],
             not_run_because="SH-1 has no per-surface exposure element (C §10.8)"),
        part("same meaning across H, E and X", "parity of meaning (S-3)", False, not_run_because="SH-1 has no H or E surface"),
    ]
    stale_ok = all(i["state"] == "refused_stale" and i["refusal"]["failing_targets"] == ["S-3"]
                   and i["refusal"]["relied_on_basis"] == B1 and i["refusal"]["evaluated_basis"]["model_revision"] == "r13"
                   for i in t7["items"])
    # 5 XC-02 (inspect → submit → accept → receipt), saving BP-T9, BP-T10, BP-T11
    run_order.append("XC-02")
    b2 = M.r.cli("T9", ["call", "OP-C1"], json.dumps({"run": "R-100"}))
    B2 = b2["basis"]
    s2, run2 = rf.rows_of(b2, "supports"), rf.rows_of(b2, "run")
    pr2 = rf.proposal("PR-2", B2, s2, rf.items_pr(s2, run2, "1.5e6"), lineage="PR-1", reason="Reduce thermal restraint")
    M.stop()
    BP9 = Seg(out, "BP-T9", parent=M)
    M.mcp()
    t10 = M.r.mcp_call("T10", "submit-proposal", {"proposal": pr2})
    M.stop()
    BP10 = Seg(out, "BP-T10", parent=M)
    M.r.person("accept", "PR-2", "1")
    M.r.person("reject", "PR-2", "2")                                                          # T11
    t11 = M.r.cli("T11o", ["observe", "PR-2"])
    BP11 = Seg(out, "BP-T11", parent=M)
    M.r.host("apply", "PR-2")                                                                  # T12
    M.mcp()
    t12 = M.r.mcp_call("T12o", "observe-proposal", {"proposal_identity": "PR-2"})
    disp = M.dispatch()
    t10d = by_step(disp, "T10")[0]
    it1 = t12["items"][0]
    dec = t11["items"][0]["decision"]
    recs.append(record("XC-11", xc11_parts, order=3, rehearsal_of=["XF-08", "XF-09", "XF-11", "XF-12"],
                       missing=[("exposure element", "SWBPIPE owner", "SQ-11"), ("E surface", "SWBPIPE owner", "SQ-20"),
                                ("stable host view references", "SWBPIPE owner", "SQ-22"), HOST_JOINS]))
    recs.append(record("XC-03", [
        part("per-item refused — stale against the original inspected basis", "failing target S-3; relied B1; current r13; nothing refreshed",
             stale_ok, chain=["J-2", "J-3", "J-4"], built_on=["XF-14", "XF-15", "T7"], obs=[("T7 refused_stale x2", "host_document", "M/T7")]),
        part("the App's record says refused — stale, never applied or queued", "dispatch outcome refused_stale",
             by_step(disp, "T7")[0]["outcome"]["value"] == "refused_stale", chain=["J-8"], obs=[("T7 dispatch record", "dispatch_record", "M/T7")]),
        part("re-draft is a new proposal with lineage (T9)", "PR-2 lineage PR-1", t10.get("lineage_replaces") == "PR-1", built_on=["T9"]),
        part("whole-model staleness scope shown unnarrowed (SWBPIPE form)", "failing target not supplied", False,
             not_run_because="SH-1 has only a per-item staleness profile (returned to C; XT F-25)"),
    ], order=4, rehearsal_of=["XF-14", "XF-15"], missing=[("per-item staleness on the original basis (whole-model only)", "SWBPIPE owner", "SQ-07"), HOST_JOINS]))
    recs.append(record("XC-02", [
        part("J-2 read with full basis and subject identities", "B2 at r13 with per-row identities", B2["model_revision"] == "r13" and all(
            "subject_content_identity" in v for v in s2.values()), chain=["J-2"], obs=[("T9 basis B2", "host_document", "M/T9")]),
        part("J-3, J-4 submission queued; the App reports queued, never accepted, until J-5 is read", "T10 dispatch outcome queued",
             t10["derived_state"]["summary"] == "queued" and t10d["outcome"]["value"] == "queued", chain=["J-3", "J-4", "J-8"],
             built_on=["XF-16"], obs=[("T10 queued", "dispatch_record", "M/T10")]),
        part("J-5 the person's A5 (item 1) and A10 (item 2) in the host facility, read over X", "per-item decisions with actor and capture reference",
             [i["state"] for i in t11["items"]] == ["accepted", "rejected"] and dec["capture_evidence_reference"].startswith("SH1-CAP-"),
             chain=["J-5"], built_on=["XF-18"], obs=[(f"T11 {dec['act_reference']}", "act_record", "M/T11o")]),
        part("J-6 application: receipt, resulting revision and objects; A5 not lapsed by application", "RC-1 at r14; S-5 created, R-100 changed; decision kept",
             it1["state"] == "applied" and it1["applied"]["receipt_reference"] == "RC-1" and it1["decision"]["act_kind"] == "A5",
             chain=["J-6"], obs=[("T12 RC-1", "host_receipt", "M/T12o/RC-1")]),
        part("J-6 origin mark linked", "origin mark on the applied association", False,
             not_run_because="SH-1's applied association carries no origin mark (returned to C; XT F-25)"),
        part("J-7 host views show old and new values", "host proposal view", False, not_run_because="SH-1 has no host views (H)"),
        part("J-8 faithful App record of J-5 citing its reference", "RS §6 human-act entry by the App writer", False,
             not_run_because="the RS writer is not exercised here (RS-v0.8 §15 prototype runs on its own logs)"),
    ], order=5, rehearsal_of=["XF-11", "XF-16", "XF-18"], acts=[{"record_id": dec["act_reference"], "act_kind": "A5",
        "actor": "Engineer A (fixture person)", "recorder": "SH-1 facility (the double's own)",
        "capture_evidence": {"reference": dec["capture_evidence_reference"]}}],
        limits=["unverified_caller_identity"],
        missing=[("capture-evidence reference", "SWBPIPE owner", "SQ-01"), ("the engineer's actual acceptance", "the person (DEP-09-09-016)"),
                 ("host views with old and new values", "SWBPIPE owner", "SQ-22"), HOST_JOINS]))
    # 6 XC-09 (acts: positive and negatives)
    run_order.append("XC-09")
    M.r.cli("XF-34", ["call", "OP-C1"], json.dumps({"run": "R-100"}), declined=True)
    disp = M.dispatch()
    no_act = all("decision" not in i for i in t10["items"]) and "decision" not in json.dumps(t4a) and "decision" not in json.dumps(t4)
    xf34 = by_step(disp, "XF-34")[0]
    recs.append(record("XC-09", [
        part("(+) T11 A5 read over X: actor Engineer A, recorder not the actor, capture reference, bound change item", "decision with capture reference",
             dec["actor"] == "Engineer A" and "change_item_content_identity" in t11["items"][0], built_on=["XF-18"],
             obs=[(dec["act_reference"], "act_record", "M/T11o")]),
        part("(−) queued, receipt, host check, findings and a declined A14 establish no act", "no decision on T10 items; RC-1, T4a, T4 carry none; XF-34 declined without a host request",
             no_act and xf34["outcome"]["value"] == "tool_execution_declined", built_on=["XF-31", "XF-32", "XF-33"],
             obs=[("XF-34 declined", "dispatch_record", "M/XF-34")]),
        part("(−) model text 'the engineer accepted' and a user-input or elicitation answer establish no act", "no act", False,
             built_on=["L-ADAPTER-4"], not_run_because="no model turn (the App's Codex is imitated; OBS-1 pending)"),
        part("(±) T2 A4 on S-2 with no acceptance predecessor; lapsed after T14", "independent A4; lapse visible", False,
             not_run_because="SH-1 has no A4 facility (returned to C; XT F-25)"),
    ], order=6, rehearsal_of=["XF-18", "XF-31", "XF-32", "XF-33"], missing=[("capture-evidence reference", "SWBPIPE owner", "SQ-01"), HOST_JOINS]))
    # 7 XC-05 on M (retry after an observed application)
    run_order.append("XC-05")
    before = M.state()
    t13 = M.r.cli("T13", ["submit"], json.dumps(pr2))
    after = M.state()
    one_effect = (after["revision"] == before["revision"] and after["next_receipt"] == before["next_receipt"]
                  and t13["answered_from_recorded_state"])
    # 8 XC-06 on M: endpoint restart, lost acknowledgement, observe first, retry; and a seek-before-resubmit violation
    run_order.append("XC-06")
    M.stop()
    M.r.person("stop-endpoint")
    M.r.person("start-endpoint")
    M.mcp()
    M.r.mcp_call("T13x", "submit-proposal", {"proposal": pr2}, drop=True)
    t13o = M.r.cli("T13o", ["observe", "PR-2"])
    t13r = M.r.cli("T13r", ["submit"], json.dumps(pr2))
    M.r.mcp_call("T13v", "submit-proposal", {"proposal": pr2}, drop=True)
    M.r.cli("T13w", ["submit"], json.dumps(pr2))                                               # no observation first
    disp = M.dispatch()
    lost = by_step(disp, "T13x")[0]
    viol = by_step(disp, "T13w")[0]
    # 9 XC-10 on M
    run_order.append("XC-10")
    xf22 = M.r.cli("XF-22", ["call", "OP-C4"], json.dumps({"run": "R-100", "location_m": 5.0, "type": "guide"}))
    xf27 = M.r.mcp_call("XF-27", "OP-C6", {"row": "S-1"})
    M.r.person("grant-direct", "S-4")
    pre = M.r.mcp_call("T16pre", "OP-C1", {"run": "R-100"})
    s16 = rf.rows_of(pre, "supports")

    def label_item(sid, old):
        return [{"item_identity": "1", "operation_identity": "OP-C9", "operation_version": "v1",
                 "affected_object": {"object_identity": sid}, "relied_on_targets": [rf.target(s16, sid)],
                 "attribute": "label", "old_value": old, "new_value": "G-X"}]
    t16 = M.r.cli("T16", ["submit"], json.dumps(rf.proposal("PR-3", pre["basis"], s16, label_item("S-4", "G-4a"), mode="apply_directly")))
    t16b = M.r.cli("T16b", ["submit"], json.dumps(rf.proposal("PR-4", pre["basis"], s16, label_item("S-3", "R-3"), mode="apply_directly")))
    M.stop()
    recs.append(record("XC-05", [
        part("T13 repeat answered from recorded state; one domain effect shown from domain evidence", "no new revision, no new receipt; answered from recorded state",
             one_effect, chain=["J-6"], built_on=["XF-19", "T13"],
             obs=[(f"revision r{after['revision']} unchanged; receipts issued {after['next_receipt'] - 1}", "host_document", "M/T13")]),
        part("durable de-duplication across a host restart", "SWBPIPE form: within one controller session only (SQ-08)", False,
             not_run_because="SH-1 does not simulate restart of its own records; its de-duplication scope is durable (C §10.8)"),
    ], order=7, rehearsal_of=["XF-19"], missing=[("durable de-duplication across restart", "SWBPIPE owner", "SQ-08"), HOST_JOINS]))
    recs.append(record("XC-06", [
        part("lost acknowledgement after an endpoint restart: outcome unknown, observer App", "T13x outcome unknown with 'lost_acknowledgement'",
             lost["outcome"]["value"] == "outcome_unknown" and "lost_acknowledgement" in lost["evidence_limits"],
             chain=["J-8"], built_on=["XF-19", "L-ADAPTER-5"], obs=[("T13x", "dispatch_record", "M/T13x")]),
        part("seek observation by identity first; retry with the same identity answered from recorded state, never stale", "T13o recorded state; T13r answered from recorded state",
             t13o["kind"] == "recorded_state" and t13r["answered_from_recorded_state"], chain=["J-6"], built_on=["XF-21"]),
        part("seek-before-resubmit violated: recorded as an evidence limit, not prevented", "T13w carries 'resubmission_without_prior_observation'",
             "resubmission_without_prior_observation" in viol["evidence_limits"], built_on=["PI-2"],
             obs=[("T13w", "dispatch_record", "M/T13w")]),
        part("non-durable host restart: retry outcome unknown, one effect unevidenced", "SWBPIPE form (SQ-08, SQ-09)", False,
             not_run_because="SH-1 does not simulate restart of its own records (C §10.8)"),
        part("App restart with a submission in flight (L-XT-3 = L-ADAPTER-12)", "outcome unknown, observer App, last observed submitted; channel re-established without silent re-enable",
             False, built_on=["XF-41"], not_run_because="App relaunch custody is DEL-01-02's (later); the RS limit labels await R13 (R12-9, RS FC-9)"),
    ], order=8, rehearsal_of=["XF-19", "XF-21", "XF-41"], limits=["lost_acknowledgement", "resubmission_without_prior_observation"],
        missing=[("durable receipts", "SWBPIPE owner", "SQ-09"), HOST_JOINS]))
    t16i, t16bi = t16["items"][0], t16b["items"][0]
    recs.append(record("XC-10", [
        part("XF-22 direct OP-C4 under ⟨set-1⟩: not permitted naming the treatment", "not_permitted, P-03 propose",
             xf22["outcome"] == "not_permitted" and xf22["governing_treatment"]["reference"].startswith("P-03"), built_on=["XF-22"]),
        part("XF-27 reserved OP-C6: not permitted, A8 offered, never not exposed", "not_permitted with a8_offered",
             xf27["outcome"] == "not_permitted" and xf27.get("a8_offered") is True, built_on=["XF-27"]),
        part("XF-23 T15 → T16: direct OP-C9 on S-4 under ⟨set-2⟩ applied, no acceptance recorded", "applied direct_under_grant; no decision",
             t16i["state"] == "applied" and t16i["applied"]["branch"] == "direct_under_grant" and "decision" not in t16i, built_on=["XF-23", "T15", "T16"],
             obs=[(t16i["applied"]["receipt_reference"], "host_receipt", "M/T16")]),
        part("direct OP-C9 on S-3 under ⟨set-2⟩ (outside the grant scope): not permitted", "refused_not_permitted naming P-03 set-2",
             t16bi["state"] == "refused_not_permitted", built_on=["TR-05"]),
        part("XF-24, XF-25, XF-26, XF-28, XF-42", "host channel rule; constraint cases; OP-C11; continued past", False,
             not_run_because="SH-1 holds no checkpoint declarations and does not implement OP-C11 (C §10.8)"),
        part("each outcome over X equals the embedded and human routes' outcome", "parity (ADAPTER RP-2)", False, not_run_because="SH-1 has no H or E surface"),
    ], order=9, rehearsal_of=["XF-22", "XF-23", "XF-27"], missing=[("host adoption of D2/D3 and grant states", "SWBPIPE owner", "SQ-05"), HOST_JOINS]))
    run_order.append("TR-05")
    # 11 XC-12 on BP-T10
    run_order.append("XC-12")
    B10 = Seg(out, "B-T10", parent=BP10)
    B10.r.person("disable")
    B10.mcp()
    new_m = B10.r.mcp_status("XC12-a")
    new_c = B10.r.cli("XC12-a", ["call", "OP-C1"], json.dumps({"run": "R-100"}))
    B10.r.person("accept", "PR-2", "1")
    st10 = B10.state()
    B10.stop()
    d10 = B10.dispatch()
    last = [x for x in d10 if x.get("proposal_identity") == "PR-2"][-1]["outcome"]["value"]
    recs.append(record("XC-12", [
        part("new requests refused channel not enabled (host-reported) after the person disables access", "both paths",
             new_m["outcome"] == new_c["outcome"] == "channel_not_enabled", built_on=["XF-35"]),
        part("PR-2 stays queued in the host and the engineer can still decide it; nothing withdrawn by disabling", "item 1 accepted after the disable",
             st10["proposals"]["PR-2"]["items"][0]["state"] == "accepted" and st10["proposals"]["PR-2"]["items"][1]["state"] == "queued"),
        part("the App shows last observed queued", "last App observation of PR-2 is queued", last == "queued"),
        part("'channel since disabled' shown", "ADAPTER channel status CT-5", False, not_run_because="the channel-status machine is ADAPTER's (its prototype), not run here"),
    ], order=11, rehearsal_of=["XF-35"], missing=[A13, HOST_JOINS]))
    # 11 XC-07 on BP-T11: neither T12 nor T13 observed
    run_order.append("XC-07")
    B11 = Seg(out, "B-T11a", parent=BP11)
    B11.r.host("apply", "PR-2")
    B11.mcp()
    B11.r.mcp_call("T13", "submit-proposal", {"proposal": pr2}, drop=True)
    later = B11.r.cli("T13o", ["observe", "PR-2"])
    B11.stop()
    d11 = B11.dispatch()
    unk = by_step(d11, "T13")[0]
    recs.append(record("XC-07", [
        part("outcome unknown, observer App, last observed state kept", "outcome_unknown with last observed 'mixed' (item 1 accepted, item 2 rejected)",
             unk["outcome"]["value"] == "outcome_unknown" and unk["outcome"]["observer"] == "app" and unk["outcome"]["last_observed_state"] == "mixed",
             built_on=["XF-20", "V-OU1"], obs=[("T13 outcome_unknown", "dispatch_record", "B-T11a/T13")]),
        part("a later observation is its own event and does not back-fill", "T13o recorded state; the T13 record unchanged",
             later["kind"] == "recorded_state" and by_step(d11, "T13")[0]["outcome"]["value"] == "outcome_unknown"),
    ], order=12, rehearsal_of=["XF-20"], missing=[("outcome resolvable beyond one controller session", "SWBPIPE owner", "SQ-09"), HOST_JOINS]))
    # 12 XC-08 on BP-T11: accepted, then stale at application
    run_order.append("XC-08")
    B8 = Seg(out, "B-T11b", parent=BP11)
    B8.r.person("edit", "S-2", "stiffness", "3.0e6")                                          # V-S1
    B8.r.host("apply", "PR-2")
    s8 = B8.state()["proposals"]["PR-2"]["items"][0]
    recs.append(record("XC-08", [
        part("accepted by Engineer A — not applied: refused — stale; A5 not lapsed", "item 1 refused_stale after acceptance, decision kept",
             s8["state"] == "refused_stale" and s8["decision"]["act_kind"] == "A5" and s8["refusal"]["failing_targets"] == ["S-2"],
             built_on=["XF-30", "V-S1"]),
    ], order=13, rehearsal_of=["XF-30"], missing=[("per-item acceptance before application (SWBPIPE Apply is both)", "SWBPIPE owner", "SQ-01"), HOST_JOINS]))
    # 13 XC-05 variant L-XT-2 on BP-T9
    run_order.append("XC-05")
    V = Seg(out, "B-T9", parent=BP9)
    V.mcp()
    V.r.mcp_call("L-XT-2a", "submit-proposal", {"proposal": pr2}, drop=True)
    V.r.mcp_call("L-XT-2b", "submit-proposal", {"proposal": pr2}, drop=True)
    vo = V.r.cli("L-XT-2o", ["observe", "PR-2"])
    pr2b = copy.deepcopy(pr2)
    pr2b["proposal_identity"]["value"] = "PR-2b"
    V.r.mcp_call("L-XT-2c", "submit-proposal", {"proposal": pr2b}, drop=True)
    vob = V.r.cli("L-XT-2p", ["observe", "PR-2b"])
    V.stop()
    dv = V.dispatch()
    vst = V.state()
    recs.append(record("XC-05", [
        part("two sends before any acknowledgement: each recorded separately, neither reported queued", "two dispatch records, each outcome unknown",
             [x["outcome"]["value"] for x in by_step(dv, "L-XT-2a") + by_step(dv, "L-XT-2b")] == ["outcome_unknown", "outcome_unknown"],
             built_on=["XF-40", "L-ADAPTER-11"]),
        part("the host answers from recorded state: one proposal, two submissions, items queued once", "one proposal PR-2 with submissions 2",
             vo["submissions_recorded"] == 2 and vo["derived_state"]["counts"] == {"queued": 2}),
        part("a new identity on the second send is two proposals, each reported as observed", "PR-2 and PR-2b both present",
             {"PR-2", "PR-2b"} <= set(vst["proposals"]) and vst["proposals"]["PR-2b"]["submissions"] == 1
             and vob["kind"] == "recorded_state"),
    ], order=14, rehearsal_of=["XF-40"], limits=["lost_acknowledgement"], missing=[HOST_JOINS]))
    # 14 XC-04: not runnable on SH-1
    run_order.append("XC-04")
    recs.append(record("XC-04", [part("later selection in the host UI cannot retarget", "bound targets unchanged at application", False,
                                      built_on=["XF-17"], not_run_because="SH-1 has no host UI selection (C §10.8)")],
                       order=15, rehearsal_of=["XF-17"], missing=[("host proposal view with bound targets", "SWBPIPE owner", "SQ-22"), HOST_JOINS]))
    # 15 TR-01 on a fresh e1 state (V-ED1), X only
    run_order.append("TR-01")
    E = Seg(out, "B-E1", edition="e1")
    E.r.person("enable")
    E.mcp()
    E.r.mcp_status("V-ED1-0")
    e1m = E.r.mcp_call("V-ED1-1", "read-catalog", {})
    e1c = E.r.cli("V-ED1-1", ["catalog"])
    tools_e1 = {t for t in E.r.items[0]["item"]["tools"]}
    ev = E.r.person("publish-edition")
    evd = E.r.mcp_call("V-ED1-2", "read-edition-events", {})
    E.r.mcp_status("V-ED1-3")
    e2m = E.r.mcp_call("V-ED1-3", "read-catalog", {})
    e2c = E.r.cli("V-ED1-3", ["catalog"])
    call9 = E.r.mcp_call("V-ED1-4", "OP-C9", {"support": "S-4", "label": "G-4"})
    E.stop()
    de = E.dispatch()
    tools_e2 = E.r.items[[i for i, x in enumerate(E.r.items) if x["step"] == "V-ED1-3"][0]]["item"]["tools"]
    ids = lambda doc: [e["operation_identity"] for e in doc["entries"]]  # noqa: E731
    op9 = next(e for e in e2m["entries"] if e["operation_identity"] == "OP-C9")
    mapped = by_step(de, "V-ED1-4")[0]
    tr01_ok = ("OP-C9" not in ids(e1m) and "OP-C9" not in ids(e1c) and len(evd["events"]) == 1 and evd["events"][0]["reporter"] == "host"
               and "OP-C9" in ids(e2m) and ids(e2m) == ids(e2c) and "OP-C9" in tools_e2 and "OP-C9" not in tools_e1)
    comps = [{"category": c, "result": "not_comparable", "surfaces_observed": ["X"],
              "detail": "only X observed; SH-1 has no H or E surface (C §10.8)"} for c in ("CMP-01", "CMP-02", "CMP-04")]
    recs.append(record("TR-01", [
        part("TS-0 on e1: OP-C9 missing on X (both paths), a discovery finding", "absent from discovery; never not exposed or unavailable",
             "OP-C9" not in ids(e1m) and "OP-C9" not in ids(e1c), built_on=["V-ED1", "TS-0"]),
        part("TS-1 one host-reported edition addition event e1 → e2", "one event, host-reported, no model revision change",
             len(evd["events"]) == 1 and evd["events"][0]["added"][0]["operation_identity"] == "OP-C9"
             and E.state()["revision"] == 12, built_on=["C CI-4"], obs=[("edition event e1→e2", "host_document", "B-E1/V-ED1-2")]),
        part("TS-2 rediscovery on X: full entry and native mapping on both paths", "OP-C9 v1 with its elements; host-supplied mapping on the MCP path",
             tr01_ok and mapped["operation"].get("operation_identity") == "OP-C9", built_on=["TS-2"],
             obs=[("OP-C9 entry keys " + ",".join(sorted(op9)), "host_document", "B-E1/V-ED1-3")]),
        part("TS-2 on H and E", "each surface discovers OP-C9", False, not_run_because="SH-1 has no H or E surface"),
    ], order=16, comparisons=comps, missing=[("the new operation and its edition event", "SWBPIPE owner", "SQ-26"),
                                               ("embedded surface", "SWBPIPE owner", "SQ-20"), HOST_JOINS]))
    # TR-05 (X part, from XC-10) and the TR cases SH-1 cannot carry
    recs.append(record("TR-05", [
        part("direct OP-C9 on S-4 under ⟨set-2⟩ applied; on S-3 not permitted (X)", "CMP-07, CMP-12 on X", t16i["state"] == "applied" and t16bi["state"] == "refused_not_permitted",
             built_on=["XC-10", "T15", "T16"], obs=[(t16i["applied"]["receipt_reference"], "host_receipt", "M/T16")]),
        part("the same on H and E", "comparison across surfaces", False, not_run_because="SH-1 has no H or E surface"),
    ], order=10, comparisons=[{"category": "CMP-07", "result": "not_comparable", "surfaces_observed": ["X"], "detail": "X only"},
                             {"category": "CMP-12", "result": "not_comparable", "surfaces_observed": ["X"], "detail": "X only"}],
        missing=[("grant states", "SWBPIPE owner", "SQ-05"), HOST_JOINS]))
    for tr, why, miss in [
        ("TR-02", "OP-C9's precondition on a support that does not exist is not modelled by SH-1", ("embedded surface", "SWBPIPE owner", "SQ-20")),
        ("TR-03", "SH-1 declares E-label-too-long but does not validate label length", ("the new operation", "SWBPIPE owner", "SQ-26")),
        ("TR-04", "SH-1 has no host proposal view (H)", ("host views", "SWBPIPE owner", "SQ-22")),
        ("TR-06", "not run in this pass on SH-1; no H or E surface to compare", ("staleness rule", "SWBPIPE owner", "SQ-07")),
        ("TR-07", "which checks relate to OP-C9 is a host input", ("the new operation's checks", "SWBPIPE owner", "SQ-26")),
        ("TR-08", "not run in this pass; no H or E surface to compare", ("durable receipts", "SWBPIPE owner", "SQ-09")),
        ("TR-09", "SH-1 does not implement OP-C10 undo", ("undo route", "SWBPIPE owner", "SQ-10")),
        ("TR-10", "SH-1 has no per-surface exposure element", ("exposure element", "SWBPIPE owner", "SQ-11"))]:
        recs.append(record(tr, [part(f"{tr} as designed (XT §4.4)", "comparison across H, E and X", False, not_run_because=why)],
                           order=None, missing=[miss, HOST_JOINS]))
    return run_order, recs, (e1m, e2m, tools_e1, tools_e2, ev, mapped)


def work_account(e1m, e2m, tools_e1, tools_e2, ev, mapped):
    """§5.1 / §5.1.1: rows per surface × element for OP-C9 on SH-1, tied to C §8 rows."""
    op9 = next(e for e in e2m["entries"] if e["operation_identity"] == "OP-C9")
    host_elems = [("entry_discovery", "Entry discovery", "operation_identity"), ("exposure", "Exposure per surface", "exposure"),
                  ("input_schema", "Input schema / argument checking", "input"), ("availability_and_reason", "Availability + reason", "availability"),
                  ("effects_and_resulting_objects", "Effects / affected objects / resulting objects", "effects"),
                  ("result_and_standing", "Result content + standing", "result"), ("errors", "Errors", "errors"),
                  ("class_element", "Class element", "class"), ("constraint_receipt", "Governing checkpoint constraint", None),
                  ("read_basis", "Read basis, subject content identities, method designation", None),
                  ("proposal_views", "Proposal views", None), ("catalog_level_interface", "Catalog-level interface", "event")]
    recv = [("native_mapping", "X"), ("loop_tool_offering", "E"), ("app_receiving_configuration", "App-X")]
    rows = []
    unobs = {"production_route_before": "not_observed", "change_made": "not_observed", "other_changes_required": "unknown"}
    for surf in ("H", "E", "X", "App-X"):
        for el, c8, key in host_elems:
            if surf == "App-X":
                continue
            row = {"surface": surf, "element": el, "c8_row": c8, "contributor": "not observed",
                   "evidence": {"not_observed": "SH-1 has no H or E surface" if surf != "X" else "not exercised by the TR-01 rehearsal"},
                   "limits": "test-double; says nothing about any host"} | unobs
            if surf == "X" and key == "event":
                row |= {"production_route_before": "generated", "change_made": "generated_automatically", "other_changes_required": "no",
                        "contributor": "SH-1's own publish step", "evidence": {"link": "B-E1/V-ED1-2 (edition event)"}}
            elif surf == "X" and key and key in op9 and el != "exposure":
                row |= {"production_route_before": "generated", "change_made": "generated_automatically", "other_changes_required": "no",
                        "contributor": "SH-1's own publish step (the double renders entries from its edition)",
                        "evidence": {"link": f"B-E1/V-ED1-3 catalog entry OP-C9 '{key}'"}}
            rows.append(row)
    for el, surf in recv:
        row = {"surface": surf, "element": el, "c8_row": "none (receiving side)", "contributor": "not observed",
               "evidence": {"not_observed": "no E surface on SH-1" if surf == "E" else "not exercised"},
               "limits": "test-double; says nothing about any host or the App"} | unobs
        if el == "native_mapping":
            ok = "OP-C9" in tools_e2 and tools_e2["OP-C9"]["_meta"]["sh1/catalog"]["mapping_source"] == "host-supplied"
            if ok:
                row |= {"production_route_before": "generated", "change_made": "generated_automatically", "other_changes_required": "no",
                        "contributor": "SH-1 (host-supplied mapping in its tool list)", "evidence": {"link": "B-E1/V-ED1-3 tools/list"}}
        if el == "app_receiving_configuration" and mapped["operation"].get("operation_identity") == "OP-C9":
            row |= {"production_route_before": "not_observed", "change_made": "none", "other_changes_required": "no",
                    "contributor": "ADAPTER mapper (App-side double), unchanged",
                    "evidence": {"link": "B-E1/V-ED1-4 dispatch record names OP-C9 v1"}}
        rows.append(row)
    return {"account_kind": "xt_work_account", "format": "proposed-0.1",
            "operation": {"operation_identity": "OP-C9", "operation_version": "v1",
                          "edition_addition_event": {"from_edition": ev["from_edition"], "to_edition": ev["to_edition"], "reporter": "host",
                                                     "observed_at": ev["published_at"]}},
            "evidence_label": "test_double", "subject_of_run": "SH-1 (C-v0.8 §10.8), rehearsal TR-01", "date": TODAY, "rows": rows,
            "disposition": {"original_promise": "V4-PAR-05 / V4-HI-03: adding an operation makes it available to the person, the embedded agent and the external agent without separate work",
                            "status": "UNRESOLVED{OI-003}",
                            "while_unruled": "evidence only: no extension criterion and no pass are established; no weaker criterion is adopted"}}


def invalid_result(valid):
    bad = copy.deepcopy(valid)
    bad["completion"]["counts_toward_witness"] = True           # X-R1
    bad["witness"] = "V4-EXM-24"                                 # X-R3 (an XC case)
    bad["parts"][1].pop("expectation")                           # a part without its expectation
    return bad


def invalid_account(valid):
    bad = copy.deepcopy(valid)
    r = next(x for x in bad["rows"] if x["change_made"] == "not_observed")
    r["other_changes_required"] = "no"                           # A-R1: unknown is never read as no
    n = next(x for x in bad["rows"] if x["element"] == "native_mapping")
    n["c8_row"] = "Entry discovery"                              # A-R2: receiving side ties to no C §8 cell
    bad["rows"][0]["effort_hours"] = 3                           # no effort, time or cost figure
    bad["disposition"]["criterion_examined"] = "retain"          # only with a ruling
    return bad


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.path.join(os.environ.get("TMPDIR", "/tmp"), "b7-xt"))
    ap.add_argument("--write-examples", action="store_true")
    a = ap.parse_args()
    out = Path(a.out)
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)
    rs, acs = json.loads(RESULT_SCHEMA.read_text()), json.loads(ACCOUNT_SCHEMA.read_text())
    reg = ss.Registry()
    reg.add(rs)
    reg.add(acs)
    for name, s in (("xt-result-record", rs), ("xt-work-account", acs)):
        check(f"{name}.schema.json uses only the validator subset", not ss.check_subset(s), str(ss.check_subset(s)))
    order, recs, tr = run_suite(out)
    planned = [s[1] for s in SUITE]
    check("cases ran in the §3.5 suite order", order == planned, f"{order} vs {planned}")
    acct = work_account(*tr)
    with open(out / "xt_results.jsonl", "w") as fh:
        for r in recs:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    (out / "xt_work_account.json").write_text(json.dumps(acct, indent=1, ensure_ascii=False))
    print(f"\n{'#':>3} {'case':6} {'segment':7} {'outcome':12} parts passed/not run/failed")
    for r in sorted(recs, key=lambda x: x["suite_position"]["order"]):
        c = [p["outcome"] for p in r["parts"]]
        print(f"{r['suite_position']['order']:>3} {r['case']:6} {r['suite_position']['segment']:7} {r['outcome']:12} "
              f"{c.count('passed')}/{c.count('not_run')}/{c.count('failed')}")
    print()
    for r in recs:
        tag = f"{r['case']} #{r['suite_position']['order']}"
        errs = ss.validate(r, rs, reg)
        check(f"{tag} record validates", not errs, "; ".join(errs[:4]))
        check(f"{tag} no part failed", all(p["outcome"] != "failed" for p in r["parts"]),
              "; ".join(p["part"] for p in r["parts"] if p["outcome"] == "failed"))
    check("no record counts toward a witness", not any(r["completion"]["counts_toward_witness"] for r in recs))
    errs = ss.validate(acct, acs, reg)
    check("V-ED1 work account validates", not errs, "; ".join(errs[:4]))
    elems = {(x["surface"], x["element"]) for x in acct["rows"]}
    host = {"entry_discovery", "catalog_level_interface", "exposure", "input_schema", "availability_and_reason", "effects_and_resulting_objects",
            "result_and_standing", "errors", "class_element", "constraint_receipt", "read_basis", "proposal_views"}
    want = {(s, e) for s in ("H", "E", "X") for e in host} | {("X", "native_mapping"), ("E", "loop_tool_offering"), ("App-X", "app_receiving_configuration")}
    check(f"work account has every surface × element row ({len(want)})", elems == want, str(want ^ elems))
    valid_r = next(r for r in recs if r["case"] == "XC-02")
    if a.write_examples:
        for name, doc in (("xt-result-record.example.valid.json", valid_r), ("xt-result-record.example.invalid.json", invalid_result(valid_r)),
                          ("xt-work-account.example.valid.json", acct), ("xt-work-account.example.invalid.json", invalid_account(acct))):
            (DESIGN / name).write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n")
    strip = lambda d: {k: v for k, v in d.items() if k not in ("date", "record_id")}  # noqa: E731
    for name, schema in EXAMPLES.items():
        doc = json.loads((DESIGN / name).read_text())
        errs = ss.validate(doc, json.loads(schema.read_text()), reg)
        if ".valid." in name:
            regen = valid_r if name.startswith("xt-result") else acct
            check(f"{name} validates and equals the regenerated instance (date aside)", not errs and strip(doc) == strip(regen),
                  "; ".join(errs[:4]))
        else:
            check(f"{name} is rejected ({len(errs)} errors)", bool(errs))
            for e in errs:
                print("       " + e)
    print(f"\nrun directory: {out}")
    print(f"{'ALL CHECKS HOLD' if not FAILS else 'FAILED'}: {len(FAILS)} failure(s)")
    return 1 if FAILS else 0


if __name__ == "__main__":
    sys.exit(main())
