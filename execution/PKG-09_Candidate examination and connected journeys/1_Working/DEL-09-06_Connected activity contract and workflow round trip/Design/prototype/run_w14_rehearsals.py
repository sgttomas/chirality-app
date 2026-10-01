#!/usr/bin/env python3
"""W14 rehearsals on the simulated host SH-1 and EXEC's recorder double
(DEL-09-06 CA-v0.6 §8.4, §8.5; run APP-V4-DESIGN-PASS-2-20260930, node B7).

Prototype only (R12-3): Python 3 standard library, no package, no network,
not product code. It writes one W14 result record (CA §8.4,
`w14-result-record.schema.json`) per W14 case and phase reading, validates
every record, and checks the committed example instances.

What it drives, all round-1 prototypes used read-only and unchanged:
  * SH-1, the one simulated host (DEL-03-01 C-v0.8 §10.8; `simhost.py` through
    its driver `run_fixture.py`), over both native paths;
  * the ADAPTER-v0.6 §4.6 mapper (`observe_map.py`) for the App-side dispatch
    records the App would write from those items;
  * EXEC-v0.6's current-phase recorder and required-tool check
    (`checkpoint_recorder.py`, `required_tool_check.py` through `run_all.py`).

Every result carries the evidence label test_double (or not_observed where a
part did not run). Nothing here is an observation of Codex, of SWBPIPE or of
any other host, and no record counts toward OUT-003 (CA §8.1, §8.3).

Usage:  python3 -B run_w14_rehearsals.py [--out DIR] [--write-examples]
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
EXEC_ROOT = DESIGN.parents[3]          # projects/chirality-app-v4/execution
C_PROTO = next(EXEC_ROOT.glob("PKG-03_*/1_Working/DEL-03-01_*/Design/prototype"))
A_PROTO = next(EXEC_ROOT.glob("PKG-03_*/1_Working/DEL-03-03_*/Design/prototype"))
E_PROTO = next(EXEC_ROOT.glob("PKG-02_*/1_Working/DEL-02-03_*/Design/prototype"))
for p in (C_PROTO, A_PROTO, E_PROTO):
    sys.path.insert(0, str(p))

import schema_subset as ss            # noqa: E402  (DEL-03-01; the validator subset)
import run_fixture as rf              # noqa: E402  (DEL-03-01; SH-1 driver)
import observe_map as om              # noqa: E402  (DEL-03-03; OM-1…OM-10)
import run_all as ex                  # noqa: E402  (DEL-02-03; CH and MT scripts)
from checkpoint_recorder import Recorder  # noqa: E402

SCHEMA_PATH = DESIGN / "w14-result-record.schema.json"
EX_VALID = DESIGN / "w14-result-record.example.valid.json"
EX_INVALID = DESIGN / "w14-result-record.example.invalid.json"
TODAY = datetime.date.today().isoformat()
FAILS = []

# RS R11 evidence-limit labels in RS's own spelling (V18-4 m-2; RP-4). The mapper's
# tokens (ADAPTER-v0.6 `external_dispatch_record.schema.json`) are mapped once, here,
# and every label a W14 record carries is checked against RS's list.
RS_SCHEMA = next(EXEC_ROOT.glob("PKG-04_*/1_Working/DEL-04-03_*/Design/RS_RECORD.schema.json"))
ADAPTER_TO_RS = {"lost_acknowledgement": "lost acknowledgement",
                 "unverified_caller_identity": "unverified caller identity",
                 "resubmission_without_prior_observation": "resubmission without prior observation",
                 "app_restart_interruption": "App-restart interruption",
                 "basis_lineage_not_supplied": "basis lineage not supplied",
                 "dedup_scope_exceeded": "de-duplication scope exceeded",
                 "host_result_not_isolated": "host result not isolated",
                 "dispatch_recognized_from_compound_command": "dispatch recognized from compound command",
                 "agent_written_configuration": "agent-written configuration"}  # RQ (V19-A M-1)


def rs_r11_labels():
    defs = json.loads(RS_SCHEMA.read_text())["$defs"]
    if "evidenceLimitLabel" in defs:
        return set(defs["evidenceLimitLabel"]["enum"])
    return set(defs["evidenceLimit"]["properties"]["label"]["enum"])


def check(label, cond, detail=""):
    print(("PASS " if cond else "FAIL ") + label + ((" -- " + detail) if detail and not cond else ""))
    if not cond:
        FAILS.append(label)
    return cond


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def rel(p):
    return str(Path(p).relative_to(EXEC_ROOT))


SH1_FILES = [C_PROTO / "simhost.py", C_PROTO / "run_fixture.py"]
MAP_FILES = [A_PROTO / "observe_map.py"]
REC_FILES = [E_PROTO / "checkpoint_recorder.py", E_PROTO / "run_all.py"]
CHK_FILES = [E_PROTO / "required_tool_check.py", E_PROTO / "fx_double.py", E_PROTO / "run_all.py"]


def double(files, identity):
    return {"double_identity": identity, "specified_in": "DEL-03-01 C-v0.8 §10.8 (SH-1); DEL-02-03 EXEC-v0.6 §7.4 (recorder and catalog doubles)",
            "files": [{"path": rel(f), "sha256": sha(f)} for f in dict.fromkeys(files)],
            "invented_material": "FX-PIPE-01 (C §10); SH-1 holds a subset (C §10.8)"}


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


def part(name, expectation, ok, built_on=(), obs=(), not_run_because=None):
    p = {"part": name, "expectation": expectation}
    if not_run_because:
        p["outcome"] = "not_run"
        p["not_run_because"] = not_run_because
    else:
        p["outcome"] = "passed" if ok else "failed"
    if built_on:
        p["built_on"] = list(built_on)
    if obs:
        p["observations"] = [{"what": w, "reference": {"kind": k, "ref": r}, "linked_not_copied": True} for w, k, r in obs]
    return p


def record(case, phase, parts, *, subject, config, limits=(), missing=(), acts=(), variant=None, state=None,
           blocked_by=None):
    outcome = aggregate(parts)
    rehearsal = "files" in subject
    ran = any(p["outcome"] != "not_run" for p in parts)
    rec = {"record_kind": "w14_result", "format": "proposed-0.1", "record_id": f"{case}/{phase}/{TODAY}",
           "case": case, "phase_reading": phase,
           "run_kind": "rehearsal" if rehearsal else "definition_check",
           "evidence_label": ("test_double" if ran else "not_observed") if rehearsal
           else ("illustrative" if ran else "not_observed"),
           "subject_of_run": subject, "configuration": config, "date": TODAY, "outcome": outcome,
           "parts": parts, "evidence_limits": sorted({ADAPTER_TO_RS.get(x, x) for x in limits}),
           "missing_inputs": [dict(zip(("input", "supplier", "relay_question"), m)) if len(m) == 3 else
                              dict(zip(("input", "supplier"), m)) for m in missing],
           "completion": {"counts_toward_out003": False,
                          "reason": "a rehearsal on a test double never completes a W14 case (CA §8.1, §8.3)" if rehearsal
                          else "a definition check completes nothing (CA §8.1)"}}
    if variant:
        rec["variant"] = variant
    if state:
        rec["case_state_at_run"] = state
    if acts:
        rec["act_records_cited"] = list(acts)
    if blocked_by:
        rec["blocked_by"] = blocked_by
    return rec


CFG_X = {"acting_surface_variant": "CA/X", "native_path": "both", "host_profile": "SH-1 full",
         "model_destination": {"not_observed": "the App's Codex is imitated, not run; no App run exists (OBS-1 observed supplier turns at pin 0.158.0 on one local route, not App runs)"}}
CFG_APP = {"acting_surface_variant": "app_only", "native_path": "not_applicable"}
CFG_NONE = {"acting_surface_variant": "not_applicable", "native_path": "not_applicable"}

HOST_JOINS = ("an identified SWBPIPE host candidate; host joins deferred", "SWBPIPE owner (DECISION-3)", "SQ-27")
APP_CAND = ("an identified App candidate (build, stock Codex version actually used, model and server)",
            "App construction (later undertaking)")


# ---------------------------------------------------------------- SH-1 run

class Sim:
    """One SH-1 run through the main timeline, with the App-side dispatch records (ADAPTER mapper)."""

    def __init__(self, out):
        self.out = Path(out)
        self.r = rf.Run(self.out, "w14main")
        self.docs = {}

    def discover(self, step="D-1"):
        r = self.r
        r.person("enable")
        assert r.start_mcp() is None
        r.mcp_status(step)
        r.mcp_call(step, "read-catalog", {})
        r.cli(step, ["catalog"])

    def timeline(self):
        r, d = self.r, self.docs
        self.discover()
        b1 = r.mcp_call("T3", "OP-C1", {"run": "R-100"})
        d["T4a"] = r.mcp_call("T4a", "OP-C12", {"run": "R-100"})
        r.person("edit", "S-3", "stiffness", "1.5e6")                                     # T6
        b2 = r.cli("T9", ["call", "OP-C1"], json.dumps({"run": "R-100"}))
        s2, run2 = rf.rows_of(b2, "supports"), rf.rows_of(b2, "run")
        self.pr2 = rf.proposal("PR-2", b2["basis"], s2, rf.items_pr(s2, run2, "1.5e6"), lineage="PR-1",
                               reason="Reduce thermal restraint")
        d["T10"] = r.mcp_call("T10", "submit-proposal", {"proposal": self.pr2})
        r.person("accept", "PR-2", "1")
        r.person("reject", "PR-2", "2")                                                    # T11
        d["T11o"] = r.cli("T11o", ["observe", "PR-2"])
        r.host("apply", "PR-2")                                                            # T12
        d["T12o"] = r.mcp_call("T12o", "observe-proposal", {"proposal_identity": "PR-2"})
        r.mcp_call("T13", "submit-proposal", {"proposal": self.pr2}, drop=True)            # ack lost
        d["T13o"] = r.cli("T13o", ["observe", "PR-2"])
        d["T13r"] = r.cli("T13r", ["submit"], json.dumps(self.pr2))
        r.stop_mcp()
        r.person("stop-endpoint")                                                          # L-ADAPTER-5
        r.person("start-endpoint")
        assert r.start_mcp() is None
        d["T13r2"] = r.cli("T13r2", ["submit"], json.dumps(self.pr2))
        r.cli("XF-34", ["call", "OP-C1"], json.dumps({"run": "R-100"}), declined=True)     # A14 declined
        # W14-04 (i') and (ii'): grant change to <set-2> and a direct application on S-4.
        r.person("grant-direct", "S-4")
        pre = r.mcp_call("T16pre", "OP-C1", {"run": "R-100"})
        s16 = rf.rows_of(pre, "supports")
        pr3 = rf.proposal("PR-3", pre["basis"], s16, [{
            "item_identity": "1", "operation_identity": "OP-C9", "operation_version": "v1",
            "affected_object": {"object_identity": "S-4"}, "relied_on_targets": [rf.target(s16, "S-4")],
            "attribute": "label", "old_value": "G-4a", "new_value": "G-4"}], mode="apply_directly", reason="Relabel S-4")
        d["T16"] = r.cli("T16", ["submit"], json.dumps(pr3))
        d["T16read"] = r.mcp_call("T16read", "OP-C1", {"run": "R-100"})
        r.stop_mcp()
        m = om.Mapper()
        self.dispatch = [m.map(x) for x in r.items]
        return self

    def rec(self, step):
        return [x for x in self.dispatch if x["observed_at"] == step]


def edition_e1(out):
    r = rf.Run(Path(out), "w14e1", edition="e1")
    r.person("enable")
    assert r.start_mcp() is None
    m = r.mcp_call("E1-D", "read-catalog", {})
    c = r.cli("E1-D", ["catalog"])
    r.stop_mcp()
    return [e["operation_identity"] for e in m["entries"]], [e["operation_identity"] for e in c["entries"]]


# ---------------------------------------------------------------- cases

def w14_00():
    ident = {"python": platform.python_version(), "platform": platform.system(), "date": TODAY}
    parts = [
        part("identification recorded before any result",
             "the subject of every later record (the double, its file digests, the invented material, date) is recorded first",
             True, obs=[("double SH-1 with the EXEC recorder and catalog doubles; " + json.dumps(ident), "run_output", "w14_results.jsonl#W14-00")]),
        part("App candidate identified", "build, stock Codex version actually used, model and server",
             False, not_run_because="no App candidate exists (App construction is a later undertaking)"),
        part("host candidate identified", "source revision, build, configuration",
             False, not_run_because="SWBPIPE identifies contributions by commit and CI records (SQ-27) but no candidate is identified; host joins deferred (DECISION-3)"),
    ]
    return record("W14-00", "current", parts, subject=double(SH1_FILES + REC_FILES + CHK_FILES, "SH-1 + EXEC-v0.6 doubles"),
                  config=CFG_NONE, missing=[APP_CAND, HOST_JOINS], state="AWAITING INPUT")


def not_run_case(case, why, missing, state, built_on=()):
    p = part(f"{case} as designed (CA §8.2)", "observed on identified App and host candidates", False,
             built_on=built_on, not_run_because=why)
    return record(case, "current", [p], subject={"definition_label": "DEL-09-06/CA-v0.6 §8.2, §8.5"}, config=CFG_NONE,
                  missing=missing, state=state)


def mt_reports():
    rows = {}
    for case in ("MT-2", "MT-16", "MT-17 (X)"):
        spec = next(m for m in ex.MT if m[0] == case)
        _, wf_name, cat_kw, surface, run_kind, kw, exp_cur, exp_gov, exp_out, exp_hold = spec
        wf, cat = ex.workflow(wf_name), ex.catalog(**cat_kw)
        cur = ex.check(wf, cat, surface, run_kind, "current", report_id=case + "/current", **kw)
        gov = ex.check(wf, cat, surface, run_kind, "governance", report_id=case + "/governance", **kw)
        holds = {c["name"]: c["hold_support"]["value"] for c in gov["checkpoints"] if c["phase_reading"] == "governance_value"}
        rows[case] = (cur, gov, holds, exp_cur, exp_gov, exp_hold)
    return rows


def w14_03(rows, e1_mcp, e1_cli):
    cur_ok = all(r[0]["check_result"] == r[3] == "passes" and not any("hold_support" in c for c in r[0]["checkpoints"])
                 for r in rows.values())
    missing_ok = "OP-C9" not in e1_mcp and "OP-C9" not in e1_cli
    parts_cur = [
        part("(Phase 1) App-route values: E1 via X (MT-2) and E1d via X (MT-16) pass on required tools and the channel; checkpoints listed as guidance, no hold value",
             "current-phase check result 'passes' for MT-2, MT-16 and MT-17 (X), with no hold-support value in any report",
             cur_ok, built_on=["MT-2", "MT-16", "MT-17"],
             obs=[(f"{c}: current={r[0]['check_result']}", "compatibility_report", f"{c}/current") for c, r in rows.items()]),
        part("one explicit missing outcome observed, no fabricated tool execution",
             "on edition e1 OP-C9 is absent from discovery on both native paths (a discovery finding, never 'not exposed' or 'unavailable'); nothing is dispatched to it",
             missing_ok, built_on=["V-ED1 step 1", "TS-0"],
             obs=[("SH-1 e1 discovery (N-MCP, N-CLI): OP-C9 absent", "host_document", "w14e1/E1-D")]),
        part("the report shown to the person", "the person sees the explicit missing or unsupported outcome",
             False, not_run_because="display is DEL-01-04's (later undertaking); nothing is shown by a double"),
        part("compatibility report computed from the host's actual edition",
             "EXEC's checker evaluates against the edition the host reports",
             False, not_run_because="EXEC's checker runs on its own catalog double (EXEC §7.4); SH-1's catalog documents are not fed to it"),
    ]
    gov_ok = all(r[1]["check_result"] == r[4] and r[2] == r[5] for r in rows.values())
    parts_gov = [
        part("(governance phase, retained) E1, E1d, E1 ⟨rev-A2g⟩ via X: governed checkpoints not enforceable, workflow unsupported",
             "MT-2 and MT-16 'does_not_pass' with CP-accept/CP-grant not enforceable (HS-3 (c)) and CP-check not enforceable (HS-5); MT-17 (X) CP-accept not enforceable",
             gov_ok, built_on=["MT-2", "MT-16", "MT-17"],
             obs=[(f"{c}: governance={r[1]['check_result']} holds={json.dumps(r[2], sort_keys=True)}", "compatibility_report", f"{c}/governance") for c, r in rows.items()]),
    ]
    subj = double(CHK_FILES + SH1_FILES, "EXEC-v0.6 catalog double + SH-1")
    return (record("W14-03", "current", parts_cur, subject=subj, config=CFG_X,
                   missing=[("SWBPIPE catalog edition with exposure (no exposure element; no workflow reader)", "SWBPIPE owner", "SQ-11"),
                            HOST_JOINS], state="AWAITING INPUT"),
            record("W14-03", "governance", parts_gov, subject=subj, config=CFG_X,
                   missing=[HOST_JOINS], state="AWAITING INPUT"))


def recorder_w14_04(sim):
    """(i') and (ii') on the recorder: CP-accept never arrives (no proposal queued); CP-check waits on S-4."""
    rec = Recorder("run-w14-04", {"kind": "workflow", "origin": "project", "source_root": "fx-proj",
                                   "name": "supports-label", "revision": "rev-E1c"}, "app_codex_via_X")
    s4 = rf.rows_of(sim.docs["T16read"], "supports")["S-4"]
    rec.listed("CP-accept", "t-start", act="A5", rw="host_outcome", subject_class="change items of a named proposal",
               purpose="engineer accepts or rejects the proposed items", scope="the proposal's items")
    rec.listed("CP-check", "t-start", act="A4", rw="output_produced", subject_class="objects changed by a named outcome",
               purpose="engineer records their own checking of S-4", scope="S-4")
    rec.content("S-4", s4["subject_content_identity"], "T16")
    rec.arrive("CP-check", {"S-4": s4["subject_content_identity"]}, "T16c", event_ref="item:agentMessage/label-report",
               purpose="engineer records their own checking of S-4", scope="S-4", method="m-sh1")
    rec.action("item:mcpToolCall/OP-C1", "T16d")                                             # continued past
    rec.end("T16e")
    return rec


def w14_04(sim, rows):
    t16 = sim.docs["T16"]["items"][0]
    rec = recorder_w14_04(sim)
    # EXEC-v0.6 recorder outputs {kind, observedAt, body} after R14-1 (RP-1): RS entry kinds with CE bodies
    kinds = [o["kind"] for o in rec.outputs]
    arr = [o["body"] for o in rec.outputs if o["kind"] == "checkpoint_arrival"]
    no_accept = not any(b["checkpoint"] == "CP-accept" for b in arr)
    fin = rec.final()
    entry_errs = [x for o in rec.outputs for x in ex.validate(o, ex.ENTRIES_SCHEMA)]
    allowed = {"checkpoint_listed", "checkpoint_arrival", "disposition_change", "continued_past", "run_ended"}
    parts = [
        part("(i′) direct application under ⟨set-2⟩: CP-accept not reached",
             "OP-C9 on S-4 applied directly (receipt, no decision recorded); no proposal queued, so no CP-accept arrival, nothing requested by reason of it, no A5 forced or recorded",
             t16["state"] == "applied" and "decision" not in t16 and no_accept and not entry_errs,
             built_on=["CH-27", "XF-23", "T15", "T16"],
             obs=[(f"T16 {t16['state']} {t16['applied']['receipt_reference']} branch {t16['applied']['branch']}", "host_receipt", "w14main/T16"),
                  ("recorder entries: no CP-accept arrival", "exec_entries", "run-w14-04")]),
        part("(ii′) E1c CP-check after the direct application: arrival recorded, nothing held, no request issued by the product",
             "CP-check arrival on ⟨S-4@r16⟩ recorded 'waiting' (reached; act not yet recorded); a later agent action carries only 'continued past'; the recorder writes entries only (RC-4)",
             fin[("CP-check", 1)][0] == "waiting" and "continued_past" in kinds and set(kinds) <= allowed,
             built_on=["CH-1"], obs=[("recorder entries: " + ", ".join(sorted(set(kinds))), "exec_entries", "run-w14-04")]),
        part("(ii′) the A4 recorded only when the person performs it",
             "an A4 on S-4 in the host's facility answers CP-check", False,
             not_run_because="SH-1 has no person control for A4 (OP-C6 is reserved and its call returns not permitted); no A4 is scripted here"),
        part("(iii′) E1 as an App run on X", "decided by required tools and the channel; nothing unsupported for a hold reason",
             rows["MT-2"][0]["check_result"] == "passes" and not any("hold_support" in c for c in rows["MT-2"][0]["checkpoints"]),
             built_on=["MT-2"], obs=[("MT-2 current=" + rows["MT-2"][0]["check_result"], "compatibility_report", "MT-2/current")]),
    ]
    gov_parts = [
        part("(i) direct request not permitted naming the constraint (V-CP1)", "host route refuses on the constraint", False,
             built_on=["V-CP1"], not_run_because="needs a host-held route; SQ-02 answered: route (iv), none; SH-1 holds no checkpoint declaration"),
        part("(ii) the run on E waits for A4 on S-4", "host-loop hold", False, built_on=["CH-1", "CH-33"],
             not_run_because="no host-loop or hold-machine double exists (EXEC §7.4); SWBPIPE has no host loop (SQ-20)"),
        part("(iii) E1 via X unsupported", "CP-accept and CP-check not enforceable (MT-2 governance)",
             rows["MT-2"][1]["check_result"] == "does_not_pass"
             and rows["MT-2"][2] == {"CP-accept": "not_enforceable", "CP-check": "not_enforceable"}, built_on=["MT-2"],
             obs=[("MT-2 governance=" + rows["MT-2"][1]["check_result"] + " holds=" + json.dumps(rows["MT-2"][2], sort_keys=True),
                   "compatibility_report", "MT-2/governance")]),
    ]
    subj = double(SH1_FILES + MAP_FILES + REC_FILES, "SH-1 + EXEC-v0.6 recorder double")
    missing = [("capture-evidence reference for host-captured acts", "SWBPIPE owner", "SQ-01"),
               ("grant states (⟨set-2⟩ has no SWBPIPE counterpart)", "SWBPIPE owner", "SQ-05"),
               ("the person's A12 and A4 on invented material", "the person (DEP-09-06-024)"), HOST_JOINS]
    return (record("W14-04", "current", parts, subject=subj, config=CFG_X, missing=missing, state="AWAITING INPUT"),
            record("W14-04", "governance", gov_parts, subject=subj, config=CFG_X,
                   missing=[("host-held checkpoint route", "SWBPIPE owner", "SQ-02"), ("host loop", "SWBPIPE owner", "SQ-20")],
                   state="AWAITING INPUT"))


def w14_05(sim):
    t10, t11, t12 = sim.docs["T10"], sim.docs["T11o"], sim.docs["T12o"]
    no_act_queued = all("decision" not in i for i in t10["items"])
    receipt = t12["items"][0]["applied"]["receipt_reference"]
    no_act_disp = all(not any("human_act" in k or k == "act_reference" for k in x) for x in sim.dispatch)
    a14 = sim.rec("XF-34")[0]
    t4a = sim.docs["T4a"]
    dec = t11["items"][0]["decision"]
    pos_ok = dec["act_kind"] == "A5" and dec["actor"] == "Engineer A" and dec["capture_evidence_reference"].startswith("SH1-CAP-")
    r20, r31, r31b = ex.ch20(), ex.ch31_i(), ex.ch31_ii()
    f20 = r20.final()[("CP-review", 1)]
    e31 = r31.outputs
    first = next(o["body"] for o in e31 if o["kind"] == "disposition_change")
    ok31i = (any(o["kind"] == "act_not_counted" and o["body"]["reason"] == "content no longer current"
                 and o["body"]["capturedBeforeArrival"] for o in e31)
             and first["disposition"] == "waiting" and "prior act not counted" in [x["label"] for x in first["annotations"]])
    fin = r31b.final()
    ok31ii = (fin[("CP-approve", 1)][0] == "performed" and fin[("CP-check", 1)][0] == "waiting"
              and any(o["kind"] == "act_not_counted" and o["body"]["reason"] == "another act kind" for o in r31b.outputs))
    entry_errs = sum(len(ex.validate(o, ex.ENTRIES_SCHEMA)) for x in (r20, r31, r31b) for o in x.outputs)
    parts = [
        part("negatives: success, queued, receipt, host check and A14 yield no act",
             "T10 queued document carries no decision; T12's receipt, T4a's host check and the declined A14 (XF-34) create no act; no App dispatch record carries a human-act reference",
             no_act_queued and no_act_disp and a14["outcome"]["value"] == "tool_execution_declined" and "decision" not in json.dumps(t4a),
             built_on=["CH-2", "CH-28", "CAP-6", "ADAPTER XF-31", "ADAPTER XF-33"],
             obs=[("T10 queued, no decision", "host_document", "w14main/T10"), (f"T12 {receipt}", "host_receipt", "w14main/T12o"),
                  ("XF-34 declined, no host request", "dispatch_record", "w14main/XF-34")]),
        part("positive: the A5 captured by the host facility, actor ≠ recorder, with capture evidence",
             "item 1 decision A5 by Engineer A with the facility's capture reference, read over X; the App would record it faithfully citing that reference (RS §6; the RS writer is not exercised here)",
             pos_ok, built_on=["T11", "ADAPTER S-9"],
             obs=[(f"T11 item 1 {dec['act_kind']} {dec['act_reference']} capture {dec['capture_evidence_reference']}", "act_record", f"w14main/T11o/{dec['act_reference']}")]),
        part("earlier act on current content counts (CH-20)", "T2's A4 counts for S-2, cited with its time; A4 on S-3 completes the answer (JA-1)",
             f20[0] == "performed" and f20[2] == {"S-2": ex.rid("run-e1b-1", "A4-T2"), "S-3": ex.rid("run-e1b-1", "A4-S3")} and entry_errs == 0, built_on=["CH-20"],
             obs=[("recorder entries CH-20", "exec_entries", "run-e1b-1")]),
        part("earlier act on content no longer current: 'prior act not counted' (CH-31 (i); R11-9)",
             "T2's A4 on ⟨S-2@r12⟩ at a run-14 arrival binding ⟨S-2@r15⟩ is recorded 'prior act not counted' (content no longer current); the arrival waits; a new A4 answers",
             ok31i and r31.final()[("CP-review", 1)][0] == "performed", built_on=["CH-31"],
             obs=[("recorder entries CH-31 (i)", "exec_entries", "run-14")]),
        part("earlier act of another kind: 'prior act not counted' (CH-31 (ii))",
             "an earlier A6 counts at CP-approve and is 'prior act not counted' (another act kind) at CP-check",
             ok31ii, built_on=["CH-31"], obs=[("recorder entries CH-31 (ii)", "exec_entries", "run-sign-1")]),
        part("App-side variant: A4, A6, A7 on AF-1 kept apart (CH-23, CH-32)", "each arrival answered only by its own kind; A7 actor with its evidence limit",
             False, built_on=["CH-23", "CH-32"],
             not_run_because="App act control not built (DEL-01-04, later); CH-32's arrival event is OBS-1 pending"),
        part("the person's actual act on invented material", "a real person performs A5/A4 in the host facility",
             False, not_run_because="no person act is performed in a rehearsal; SWBPIPE offers no capture-evidence reference (SQ-01)"),
    ]
    acts = [
        {"record_id": dec["act_reference"], "act_kind": "A5", "actor": "Engineer A (fixture person, SH-1 facility)",
         "recorder": "SH-1 facility (the double's own)", "capture_evidence": {"reference": dec["capture_evidence_reference"]},
         "counted_as": "not evaluated"},
        {"record_id": ex.rid("run-14", "A4-T2"), "act_kind": "A4", "actor": "Engineer A (scripted)", "recorder": "EXEC recorder double",
         "capture_evidence": {"absent": "scripted observation; no capture facility in the recorder double"},
         "counted_as": "prior act not counted", "not_counted_reason": "content no longer current"},
    ]
    return record("W14-05", "current", parts, subject=double(SH1_FILES + MAP_FILES + REC_FILES, "SH-1 + EXEC-v0.6 recorder double"),
                  config=CFG_X, acts=acts,
                  limits=["unverified_caller_identity"],
                  missing=[("capture-evidence reference for host-captured acts", "SWBPIPE owner", "SQ-01"),
                           ("an actual person performing the act on invented material", "the person (DEP-09-06-024)"),
                           ("App act control for the AF-1 variant and for a joined CH-31 (ii)", "DEL-01-04 (later undertaking)"), HOST_JOINS],
                  state="AWAITING INPUT")


def w14_06():
    r8, r10 = ex.ch8(), ex.ch10()
    f8 = r8.final()[("CP-check", 1)]
    k8 = [o["kind"] for o in r8.outputs]
    after = k8.index("act_lapsed")
    no_wait = all(o["body"]["disposition"] != "waiting" for o in r8.outputs[after:] if o["kind"] == "disposition_change")
    f10 = r10.final()[("CP-check", 1)]
    errs = sum(len(ex.validate(o, ex.ENTRIES_SCHEMA)) for x in (r8, r10) for o in x.outputs)
    parts = [
        part("lapse after the resume point: 'act lapsed at ‹t›', nothing says waiting (CH-7)", "act-lapsed recorded; no later disposition says waiting",
             no_wait and errs == 0, built_on=["CH-7"], obs=[("recorder entries CH-7/CH-8", "exec_entries", "run-12a")]),
        part("partial lapse answered by a new act on the changed rows with the earlier act (CH-8; JA-1)", "performed, ordinal 2, answered by two acts",
             f8[0] == "performed" and f8[1] == 2, built_on=["CH-8"]),
        part("lapse after run end: lapsed per referent; post-end act changes nothing (CH-10)", "lapsed; act_after_run_end",
             f10[0] == "lapsed" and "act_after_run_end" in [o["kind"] for o in r10.outputs], built_on=["CH-10"],
             obs=[("recorder entries CH-10", "exec_entries", "run-12b")]),
        part("lapse from a content change on the host (SH-1)", "a host edit to a row bound by an A4 lapses it", False,
             built_on=["T14"], not_run_because="SH-1 has no A4 facility; the lapse rule runs on the recorder double over scripted content identities only"),
        part("whole-model identity: any model change lapses every bound act (over-lapse, R8-4)", "SWBPIPE-form identity received for every covered subject",
             False, not_run_because="SH-1 has per-subject identities only; no whole-model profile exists (returned to C; CA F-26)"),
        part("CH-6, CH-30 (other lapse cases)", "as EXEC §7.2", False, built_on=["CH-6", "CH-30"],
             not_run_because="not prototyped in EXEC-v0.6 (§7.4)"),
    ]
    return record("W14-06", "current", parts, subject=double(REC_FILES, "EXEC-v0.6 recorder double"), config=CFG_X,
                  missing=[("per-object content identities (whole-model only)", "SWBPIPE owner", "SQ-03"),
                           ("host lapse display (DESIGN only)", "SWBPIPE owner", "SQ-23"), HOST_JOINS],
                  state="AWAITING INPUT")


def w14_07(sim):
    t13 = sim.rec("T13")[0]
    t13o = sim.rec("T13o")[0]
    t13r, t13r2 = sim.docs["T13r"], sim.docs["T13r2"]
    lost_ok = (t13["outcome"]["value"] == "outcome_unknown" and t13["outcome"]["observer"] == "app"
               and "lost_acknowledgement" in t13["evidence_limits"])
    recovered_ok = t13o["outcome"]["value"] == "recorded_state" and sim.rec("T13")[0]["outcome"]["value"] == "outcome_unknown"
    retry_ok = (t13r["answered_from_recorded_state"] and t13r["items"][0]["applied"]["receipt_reference"] == "RC-1"
                and t13r2["answered_from_recorded_state"] and t13r2["items"][0]["state"] == "applied")
    parts = [
        part("observation lost: outcome unknown, observer App", "the lost acknowledgement leaves outcome unknown with its limit",
             lost_ok, built_on=["CH-3", "RP-1"], obs=[("T13 outcome_unknown", "dispatch_record", "w14main/T13")]),
        part("recovery by observation by identity, not back-filled", "the later observation is its own record; the T13 record stays outcome unknown",
             recovered_ok, built_on=["RP-1", "P PM-4"], obs=[("T13o recorded_state", "dispatch_record", "w14main/T13o")]),
        part("retry with the same identity answered from recorded state, never stale; also after an endpoint restart (durable double)",
             "T13r and T13r2 answered from recorded state (RC-1)", retry_ok, built_on=["T13", "L-ADAPTER-5"],
             obs=[("T13r, T13r2 answered from recorded state", "host_document", "w14main/T13r2")]),
        part("interruption is not run end; dispositions rebuilt from the record (RC-10)", "rebuild after interruption", False,
             built_on=["CH-4", "CH-21", "RP-1…RP-8"], not_run_because="no interruption double and no rebuild in the recorder prototype (EXEC §7.4)"),
        part("run ended while waiting; continuation is a new run (CH-9)", "continues ⟨run⟩ inherits nothing", False,
             built_on=["CH-9"], not_run_because="not prototyped in EXEC-v0.6"),
        part("non-durable host restart: the retry is outcome unknown and one effect unevidenced", "SWBPIPE-form session-only receipts (SQ-09 (c))",
             False, not_run_because="SH-1 does not simulate restart of its own records (C §10.8)"),
    ]
    return record("W14-07", "current", parts, subject=double(SH1_FILES + MAP_FILES, "SH-1"), config=CFG_X,
                  limits=["lost_acknowledgement", "unverified_caller_identity"],
                  missing=[("durable receipts; outcome resolvable across restart", "SWBPIPE owner", "SQ-09"),
                           ("host run records", "SWBPIPE owner", "SQ-19"), HOST_JOINS], state="AWAITING INPUT")


def invalid_from(valid):
    bad = copy.deepcopy(valid)
    bad["completion"]["counts_toward_out003"] = True                  # W-R1: a rehearsal never counts
    bad["parts"][0]["hold_support"] = "enforced_by_the_host_loop"     # W-R4: no hold value in the current phase
    bad["act_records_cited"][1].pop("not_counted_reason")             # 'prior act not counted' needs its reason
    return bad


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.path.join(os.environ.get("TMPDIR", "/tmp"), "b7-w14"))
    ap.add_argument("--write-examples", action="store_true")
    a = ap.parse_args()
    out = Path(a.out)
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)
    schema = json.loads(SCHEMA_PATH.read_text())
    reg = ss.Registry()
    reg.add(schema)
    check("w14-result-record.schema.json uses only the validator subset", not ss.check_subset(schema),
          str(ss.check_subset(schema)))
    sim = Sim(out).timeline()
    e1m, e1c = edition_e1(out)
    rows = mt_reports()
    recs = [w14_00(),
            not_run_case("W14-01", "SH-1 has no workflow library and no transfer-tracer double exists (EXEC §7.4: RT-1…RT-10 not run)",
                         [("host workflow library and reader", "SWBPIPE owner", "SQ-17"), ("registration", "DEL-02-02 (later undertaking)"), HOST_JOINS],
                         "AWAITING INPUT", ["RT-1", "TR-1…TR-6"]),
            not_run_case("W14-02", "no host workflows or adaptation exist on SH-1 or SWBPIPE",
                         [("host adaptation with derived-from", "SWBPIPE owner", "SQ-18"), HOST_JOINS], "AWAITING INPUT", ["RT-2", "RT-3"]),
            *w14_03(rows, e1m, e1c), *w14_04(sim, rows), w14_05(sim), w14_06(), w14_07(sim),
            not_run_case("W14-08", "no App run exists: OBS-1 observed supplier turns at pin 0.158.0 on one local route (no model element on the turn), not an App run's supplied guidance; no host loop or host run record exists",
                         [("App-side supplied guidance and destination per turn at pin 0.158.0, observed in an App run", "App construction (later undertaking); DEL-01-01"),
                          ("host run records and supplied guidance", "SWBPIPE owner", "SQ-19"), HOST_JOINS], "AWAITING INPUT", ["RT-5", "CR-14"]),
            not_run_case("W14-09", "no host revision to relay, no library double, no DEL-02-02 registration",
                         [("host workflows", "SWBPIPE owner", "SQ-18"), ("registration and drafts", "DEL-02-02 (later undertaking)")],
                         "AWAITING INPUT", ["RT-6", "RT-8"]),
            not_run_case("W14-10", "no host workflows and no library double",
                         [("host workflows and revision history", "SWBPIPE owner", "SQ-18")], "AWAITING INPUT", ["RT-7", "RP-5"])]
    print()
    with open(out / "w14_results.jsonl", "w") as fh:
        for r in recs:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"{'case':8} {'phase':10} {'outcome':12} parts (passed/not run/failed)")
    for r in recs:
        c = [p["outcome"] for p in r["parts"]]
        print(f"{r['case']:8} {r['phase_reading']:10} {r['outcome']:12} {c.count('passed')}/{c.count('not_run')}/{c.count('failed')}")
    print()
    for r in recs:
        errs = ss.validate(r, schema, reg)
        check(f"{r['case']} ({r['phase_reading']}) record validates", not errs, "; ".join(errs[:4]))
        check(f"{r['case']} ({r['phase_reading']}) no part failed", all(p["outcome"] != "failed" for p in r["parts"]),
              "; ".join(p["part"] for p in r["parts"] if p["outcome"] == "failed"))
        check(f"{r['case']} ({r['phase_reading']}) counts toward OUT-003: no", r["completion"]["counts_toward_out003"] is False)
    rs_labels = rs_r11_labels()
    used = sorted({x for r in recs for x in r["evidence_limits"]})
    check(f"every evidence limit is an RS R11 label in RS's spelling ({len(used)} distinct: {', '.join(used)})",
          all(x in rs_labels for x in used), str([x for x in used if x not in rs_labels]))
    cited = [ac for r in recs for ac in r.get("act_records_cited", [])]
    check("every cited act names an actor different from its recorder", all(ac["actor"] != ac["recorder"] for ac in cited))
    valid = next(r for r in recs if r["case"] == "W14-05")
    if a.write_examples:
        EX_VALID.write_text(json.dumps(valid, indent=2, ensure_ascii=False) + "\n")
        EX_INVALID.write_text(json.dumps(invalid_from(valid), indent=2, ensure_ascii=False) + "\n")
    on_disk = json.loads(EX_VALID.read_text())
    strip = lambda d: {k: v for k, v in d.items() if k not in ("date", "record_id")}  # noqa: E731
    check("w14-result-record.example.valid.json validates and equals the regenerated W14-05 record (date aside)",
          not ss.validate(on_disk, schema, reg) and strip(on_disk) == strip(valid))
    bad = json.loads(EX_INVALID.read_text())
    errs = ss.validate(bad, schema, reg)
    check(f"w14-result-record.example.invalid.json is rejected ({len(errs)} errors)", bool(errs))
    for e in errs:
        print("       " + e)
    print(f"\nrun directory: {out}")
    print(f"{'ALL CHECKS HOLD' if not FAILS else 'FAILED'}: {len(FAILS)} failure(s)")
    return 1 if FAILS else 0


if __name__ == "__main__":
    sys.exit(main())
