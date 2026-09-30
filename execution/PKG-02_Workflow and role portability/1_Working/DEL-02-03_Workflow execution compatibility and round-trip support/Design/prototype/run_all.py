"""Run the EXEC-v0.6 design prototype: MT cases on the required-tool check,
CH cases on the current-phase recorder, and schema validation of every report,
every entries document and the committed example instances.

Usage:  python3 run_all.py [--write-examples]
Exit status 0 only if every check holds. Not product code.
"""

import copy
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DESIGN = os.path.dirname(HERE)
sys.path.insert(0, HERE)

from jsonschema_subset import validate                     # noqa: E402
from fx_double import catalog, workflow                    # noqa: E402
from required_tool_check import check, statement           # noqa: E402
from checkpoint_recorder import Recorder                   # noqa: E402

REPORT_SCHEMA = json.load(open(os.path.join(DESIGN, "compatibility-report.schema.json")))
ENTRIES_SCHEMA = json.load(open(os.path.join(DESIGN, "checkpoint-record-entries.schema.json")))
FAIL = []


def expect(label, cond, detail=""):
    print(("  ok   " if cond else "  FAIL ") + label + ((" -- " + detail) if detail and not cond else ""))
    if not cond:
        FAIL.append(label)


DEST_X = {"selected": "local model server (fixture)", "class": "local", "information_only": True}

# ---------------------------------------------------------------- MT cases (§7.1)
# (case, workflow, catalog kwargs, surface, run kind, check kwargs,
#  expected current-phase result, expected governance-phase result,
#  expected per-reference outcomes, expected governance hold values)
MT = [
    ("MT-1", "E1-rev-3", {}, "E", "host", {}, "passes", "passes",
     {"OP-C1": "present", "OP-C3": "present", "OP-C4": "present", "OP-C5": "present", "OP-C12": "present"},
     {"CP-accept": "enforced_by_the_host_loop", "CP-check": "enforced_by_the_host_loop"}),
    ("MT-2", "E1-rev-A2", {}, "X", "app", {"model_destination": DEST_X}, "passes", "does_not_pass",
     {"OP-C4": "present"}, {"CP-accept": "not_enforceable", "CP-check": "not_enforceable"}),
    ("MT-3", "E1-rev-3", {"variants": ["OP-C4-absent"]}, "E", "host", {}, "does_not_pass", "does_not_pass",
     {"OP-C4": "missing"}, None),
    ("MT-4", "E1-rev-3", {"variants": ["OP-C5-absent"]}, "E", "host", {}, "passes", "passes",
     {"OP-C5": "missing"}, None),
    ("MT-5 (X)", "E1c", {"variants": ["V-X1"]}, "X", "app", {"model_destination": DEST_X},
     "does_not_pass", "does_not_pass", {"OP-C9": "not_exposed_on_this_surface"},
     {"CP-check": "not_enforceable"}),
    ("MT-5 (E)", "E1c", {"variants": ["V-X1"]}, "E", "host", {}, "passes", "passes",
     {"OP-C9": "present"}, {"CP-check": "enforced_by_the_host_loop"}),
    ("MT-6", "requires-OP-C2", {"revision": "r13"}, "E", "host", {"readiness": True}, "passes", "passes",
     {"OP-C2": "present_currently_unavailable"}, None),
    ("MT-7", "E1-OP-C1-v1", {"variants": ["OP-C1-v2"]}, "E", "host", {}, "does_not_pass", "does_not_pass",
     {"OP-C1": "version_mismatch"}, None),
    ("MT-8", "E1-harness-file-writing", {}, "E", "host", {}, "not_established", "not_established",
     {"file writing": "not_established"}, None),
    ("MT-9", "E5", {}, "E", "host", {}, "not_established", "not_established", {}, None),
    ("MT-10", "E6", {}, "E", "host", {"seat_has_delegation": False}, "does_not_pass", "does_not_pass", {}, None),
    ("MT-12 (e1)", "E1c", {"edition": "e1"}, "E", "host", {}, "does_not_pass", "does_not_pass",
     {"OP-C9": "missing"}, None),
    ("MT-12 (e2)", "E1c", {"edition": "e2"}, "E", "host", {"occasion": "CK-3"}, "passes", "passes",
     {"OP-C9": "present"}, None),
    ("MT-13", "requires-OP-C11", {}, "E", "host", {}, "passes", "passes", {"OP-C11": "present"}, None),
    ("MT-14", "E1-rev-A2", {}, "X", "app", {"channel_enabled": False, "model_destination": DEST_X},
     "does_not_pass", "does_not_pass", {"OP-C1": "channel_not_enabled"}, None),
    ("MT-15", "E1d-harness-grant", {}, "X", "app", {"model_destination": DEST_X},
     "not_established", "does_not_pass", {"shell command": "not_established", "OP-C9": "present"},
     {"CP-grant": "not_enforceable", "CP-check": "not_enforceable"}),
    ("MT-16", "E1d", {}, "X", "app", {"model_destination": DEST_X}, "passes", "does_not_pass",
     {"OP-C9": "present"}, {"CP-grant": "not_enforceable", "CP-check": "not_enforceable"}),
    ("MT-17 (X)", "E1-rev-A2g", {}, "X", "app", {"model_destination": DEST_X}, "passes", "does_not_pass",
     {"OP-C4": "present"}, {"CP-accept": "not_enforceable"}),
    ("MT-17 (E)", "E1-rev-A2g", {}, "E", "host", {}, "passes", "passes",
     {"OP-C4": "present"}, {"CP-accept": "enforced_by_the_host_loop"}),
]


def run_mt():
    print("Required-tool check (EXEC §3.3-§3.6) on the FX-PIPE-01 test double")
    reports = {}
    for case, wf_name, cat_kw, surface, run_kind, kw, exp_cur, exp_gov, exp_out, exp_hold in MT:
        wf, cat = workflow(wf_name), catalog(**cat_kw)
        cur = check(wf, cat, surface, run_kind, "current", report_id=case + "/current", **kw)
        gov = check(wf, cat, surface, run_kind, "governance", report_id=case + "/governance", **kw)
        reports[case] = (cur, gov)
        outs = {r["reference"]: r["outcome"] for r in cur["requirements"]}
        holds = {c["name"]: c["hold_support"]["value"] for c in gov["checkpoints"]
                 if c["phase_reading"] == "governance_value"}
        ok = (cur["check_result"] == exp_cur and gov["check_result"] == exp_gov
              and all(outs.get(k) == v for k, v in exp_out.items())
              and (exp_hold is None or holds == exp_hold)
              and not any("hold_support" in c for c in cur["checkpoints"]))
        expect("%-11s current=%s governance=%s %s" % (case, cur["check_result"], gov["check_result"],
               ("holds=" + json.dumps(holds, sort_keys=True)) if holds else ""), ok,
               "expected current=%s governance=%s outcomes=%s holds=%s; got outcomes=%s"
               % (exp_cur, exp_gov, exp_out, exp_hold, outs))
        for rep in (cur, gov):
            errs = validate(rep, REPORT_SCHEMA)
            expect("    %s report validates" % rep["phase"], not errs, "; ".join(errs[:5]))
    s = statement(reports["MT-1"][0])
    expect("PS-2 wording for MT-1: " + s, s.startswith("requirement check passes against e2 on E")
           and not any(w in s for w in ("compatible", "will run", "runnable")))
    expect("PS-4 wording for MT-9", statement(reports["MT-9"][0]) ==
           "requirements undeclared — check not established")
    return reports


# ---------------------------------------------------------------- CH cases (§7.2)
WF_E1 = {"kind": "workflow", "origin": "project", "source_root": "fx-proj", "name": "supports-adjust",
         "revision": "rev-A2"}
WF_E1B = {"kind": "workflow", "origin": "project", "source_root": "fx-proj", "name": "spacing-review",
          "revision": "rev-B1"}
WF_SIGN = {"kind": "workflow", "origin": "project", "source_root": "fx-proj", "name": "report-signoff",
           "revision": "rev-S1"}


def ch8():
    """CH-7 then CH-8 (L-WDEX-1; WD-EX R-4 (ii)): lapse after resume, then an A4 on S-3 only."""
    r = Recorder("run-12a", WF_E1, "app_codex_via_X")
    for ref, ci in (("S-5", "S-5@r14"), ("R-100", "R-100@r14"), ("S-3", "S-3@r14")):
        r.content(ref, ci, "T12")
    r.listed("CP-check", "T0", act="A4", rw="b", subject_class="objects changed by a named outcome",
             purpose="engineer records their own checking of the changed supports", scope="those objects",
             evaluability=("evaluable_with_limit", "message-output designation per WD (B1, R10-8); OBS-1 pending"))
    r.arrive("CP-check", {"S-5": "S-5@r14", "R-100": "R-100@r14", "S-3": "S-3@r14"}, "T14b",
             event_ref="item:agentMessage/examination-report", purpose="engineer records their own checking",
             scope="S-5, R-100, S-3")
    r.request("person_input_request", "req:ask-checked-mark", "T14c")
    r.act("A4-a1", "A4", {"S-5": "S-5@r14", "R-100": "R-100@r14", "S-3": "S-3@r14"}, "T14d")
    r.action("item:agentMessage/summary-start", "T14e")
    r.content("S-3", "S-3@r15", "T14f")                      # Engineer A edits S-3 after resume
    r.action("item:fileChange/summary.md", "T14g")           # may carry "continued past"
    r.act("A4-a2", "A4", {"S-3": "S-3@r15"}, "T14h")         # narrower act (JA-1)
    return r


def ch20():
    """CH-20 (L-EXEC-30): T2's A4 on S-2 before CP-review's arrival at T4; S-3 answered later."""
    r = Recorder("run-e1b-1", WF_E1B, "app_codex_via_X")
    r.content("S-2", "S-2@r12", "T1"); r.content("S-3", "S-3@r12", "T1")
    r.act("A4-T2", "A4", {"S-2": "S-2@r12"}, "T2")
    r.listed("CP-review", "T3", act="A4", rw="b", subject_class="objects a named output concerns",
             purpose="engineer marks the examined rows checked", scope="rows the findings identify")
    r.arrive("CP-review", {"S-2": "S-2@r12", "S-3": "S-3@r12"}, "T4", event_ref="item:agentMessage/findings",
             purpose="engineer marks the examined rows checked", scope="S-2, S-3")
    r.act("A4-S3", "A4", {"S-3": "S-3@r12"}, "T4b")
    return r


def ch31_i():
    """CH-31 (i) (L-EXEC-31): T2's A4 on S-2 is no longer current at a later arrival (T14 edited S-2)."""
    r = Recorder("run-14", WF_E1B, "app_codex_via_X")
    r.content("S-2", "S-2@r12", "T1"); r.content("S-3", "S-3@r12", "T1")
    r.act("A4-T2", "A4", {"S-2": "S-2@r12"}, "T2")
    r.content("S-3", "S-3@r13", "T6"); r.content("S-2", "S-2@r15", "T14")
    r.listed("CP-review", "T14a", act="A4", rw="b", subject_class="objects a named output concerns",
             purpose="engineer marks the examined rows checked", scope="rows the findings identify")
    r.arrive("CP-review", {"S-2": "S-2@r15", "S-3": "S-3@r13"}, "T14c", event_ref="item:agentMessage/findings",
             purpose="engineer marks the examined rows checked", scope="S-2, S-3")
    r.act("A4-new", "A4", {"S-2": "S-2@r15", "S-3": "S-3@r13"}, "T14d")
    return r


def ch31_ii():
    """CH-31 (ii) (L-EXEC-32): an earlier A6 on AF-1 counts at CP-approve and is another kind at CP-check."""
    r = Recorder("run-sign-1", WF_SIGN, "app_content")
    r.content("AF-1", "AF-1@f1", "t0")
    r.act("A6-1", "A6", {"AF-1": "AF-1@f1"}, "t1", surface="app_interface")
    for cp, act in (("CP-check", "A4"), ("CP-approve", "A6")):
        r.listed(cp, "t2", act=act, rw="b", subject_class="named output",
                 purpose="the person's own %s of the report" % {"A4": "checking", "A6": "approval"}[act],
                 scope="AF-1")
    for cp in ("CP-check", "CP-approve"):
        r.arrive(cp, {"AF-1": "AF-1@f1"}, "t3", event_ref="app-file:reports/supports-review.md",
                 source="app_file_observation", time_source="app_observation_time",
                 purpose="report sign-off", scope="AF-1", method="m-fx-file")
    return r


def ch10():
    """CH-10: lapse after the run ended (WD-EX R-4 (iii))."""
    r = Recorder("run-12b", WF_E1, "app_codex_via_X")
    r.content("S-3", "S-3@r14", "T12")
    r.listed("CP-check", "T0", act="A4", rw="b", subject_class="objects changed by a named outcome",
             purpose="engineer records their own checking", scope="S-3")
    r.arrive("CP-check", {"S-3": "S-3@r14"}, "T14b", event_ref="item:agentMessage/examination-report",
             purpose="engineer records their own checking", scope="S-3")
    r.act("A4-b1", "A4", {"S-3": "S-3@r14"}, "T14d")
    r.end("T15", by="person", cause="stopped by the person")
    r.content("S-3", "S-3@r16", "T16")
    r.act("A4-b2", "A4", {"S-3": "S-3@r16"}, "T17")
    return r


def kinds(r):
    return [e["kind"] for e in r.doc["entries"]]


def run_ch():
    print("Current-phase recorder (EXEC §2.4) on scripted observations")
    r = ch8()
    f = r.final()[("CP-check", 1)]
    expect("CH-7/CH-8 final: performed, ordinal 2, answered by A4-a1 (R-100, S-5) and A4-a2 (S-3)",
           f[0] == "performed" and f[1] == 2 and f[2] == {"S-5": "A4-a1", "R-100": "A4-a1", "S-3": "A4-a2"},
           str(f))
    k = kinds(r)
    expect("CH-7: lapse after resume recorded; no disposition entry says waiting after it",
           "act_lapsed" in k and all(e["disposition"] != "waiting" for e in r.doc["entries"][k.index("act_lapsed"):]
                                     if e["kind"] == "disposition"))
    expect("CH-7: continued-past annotation on the later agent action", "continued_past" in k)
    expect("CH-7: request observed and associated",
           any(e["kind"] == "request_observed" and e["association"] == "associated" for e in r.doc["entries"]))
    r20 = ch20()
    f = r20.final()[("CP-review", 1)]
    expect("CH-20: T2's A4 counts for S-2 as an earlier act; performed after the A4 on S-3 (JA-1)",
           f[0] == "performed" and f[2] == {"S-2": "A4-T2", "S-3": "A4-S3"} and
           any(e["kind"] == "act_counted" and e["relation"] == "earlier_act" for e in r20.doc["entries"]), str(f))
    r31 = ch31_i()
    ents = r31.doc["entries"]
    first_disp = next(e for e in ents if e["kind"] == "disposition")
    expect("CH-31 (i): T2's A4 not counted (content no longer current); arrival waiting with "
           "'prior act not counted'",
           any(e["kind"] == "act_not_counted" and e["reason"] == "content_no_longer_current"
               and e["captured_before_arrival"] for e in ents)
           and first_disp["disposition"] == "waiting" and "prior act not counted" in first_disp["annotations"])
    expect("CH-31 (i): a new A4 on S-2 and S-3 -> performed",
           r31.final()[("CP-review", 1)][0] == "performed")
    r31b = ch31_ii()
    fin = r31b.final()
    expect("CH-31 (ii): earlier A6 counts at CP-approve (performed); at CP-check it is another kind "
           "(not counted; waiting)",
           fin[("CP-approve", 1)][0] == "performed" and fin[("CP-check", 1)][0] == "waiting"
           and any(e["kind"] == "act_not_counted" and e["reason"] == "other_kind" for e in r31b.doc["entries"]))
    r10 = ch10()
    f = r10.final()[("CP-check", 1)]
    expect("CH-10: lapse after run end -> lapsed; post-end act shown, changes nothing",
           f[0] == "lapsed" and "act_after_run_end" in kinds(r10), str(f))
    for name, rec in (("CH-8", r), ("CH-20", r20), ("CH-31 (i)", r31), ("CH-31 (ii)", r31b), ("CH-10", r10)):
        errs = validate(rec.doc, ENTRIES_SCHEMA)
        expect("    %s entries validate (%d entries)" % (name, len(rec.doc["entries"])), not errs,
               "; ".join(errs[:5]))
    return r


def invalid_report(valid):
    bad = copy.deepcopy(valid)
    bad["checkpoints"][0]["hold_support"] = {"value": "not_enforceable", "hs_row": "HS-5"}  # PH-3
    bad["requirements"][0]["outcome"] = "compatible"                                        # PS-2
    del bad["check_result"]                                                                  # CR-10
    return bad


def invalid_entries(valid):
    bad = copy.deepcopy(valid)
    bad["phase"] = "governance"
    bad["entries"].append({"entry_id": "x1", "order": 99, "kind": "action_during_hold",
                           "observed_at": "T99", "action_ref": "item:x"})
    for e in bad["entries"]:
        if e["kind"] == "disposition":
            e["disposition"] = "held"
            break
    for e in bad["entries"]:
        if e["kind"] == "act_counted":
            del e["act"]
            break
    return bad


def examples(reports, rec, write):
    print("Committed example instances")
    ex = {
        "compatibility-report.example.valid.json": reports["MT-1"][0],
        "compatibility-report.example.invalid.json": invalid_report(reports["MT-1"][0]),
        "checkpoint-record-entries.example.valid.json": rec.doc,
        "checkpoint-record-entries.example.invalid.json": invalid_entries(rec.doc),
    }
    for fname, doc in ex.items():
        path = os.path.join(DESIGN, fname)
        if write:
            with open(path, "w") as fh:
                json.dump(doc, fh, indent=2, ensure_ascii=False)
                fh.write("\n")
        on_disk = json.load(open(path))
        schema = REPORT_SCHEMA if fname.startswith("compatibility") else ENTRIES_SCHEMA
        errs = validate(on_disk, schema)
        if ".valid." in fname:
            expect("%s validates and equals the regenerated instance" % fname, not errs and on_disk == doc,
                   "; ".join(errs[:5]))
        else:
            expect("%s is rejected (%d errors)" % (fname, len(errs)), bool(errs))
            for e in errs[:8]:
                print("         " + e)


if __name__ == "__main__":
    reports = run_mt()
    rec = run_ch()
    examples(reports, rec, "--write-examples" in sys.argv)
    print("\n%s: %d failure(s)" % ("FAILED" if FAIL else "ALL CHECKS HOLD", len(FAIL)))
    sys.exit(1 if FAIL else 0)
