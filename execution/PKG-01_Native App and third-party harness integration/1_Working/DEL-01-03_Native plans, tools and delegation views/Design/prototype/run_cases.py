#!/usr/bin/env python3
"""Run the DEL-01-03 prototype cases (NPTD-v0.1 §15.3). Python 3 standard library only.

Usage (from this folder):  python3 run_cases.py
Reads (never writes) the committed 0.158.0 JSON Schema bundle of DEL-01-01. Writes the
constructed scenario fixtures to fixtures/native/ (deterministic). Prints one line per
case and a summary; exit code 0 when every case gave its expected result.
A case that passes shows that the rules of the Design file run as written against
constructed native frames. It passes no VER criterion (no App candidate exists).
"""
import copy
import json
import os
import re
import sys

import jsonschema_subset as V
import npt_model as M
import scenarios as S

HERE = os.path.dirname(os.path.abspath(__file__))
DESIGN = os.path.dirname(HERE)
BUNDLE = os.path.join(DESIGN, "..", "..", "DEL-01-01_Stock Codex hosting and supplier contract", "Design",
                      "generated", "0.158.0", "json-schema", "experimental",
                      "codex_app_server_protocol.v2.schemas.json")
MDFILE = os.path.join(DESIGN, "NATIVE_PLANS_TOOLS_DELEGATION.md")
ROOT = json.load(open(BUNDLE, encoding="utf-8"))
SCHEMAS = {n: json.load(open(os.path.join(DESIGN, "npt.%s.schema.json" % n), encoding="utf-8"))
           for n in ("plan-revision", "item-anchor", "delegation-export")}
RESULTS = []


def result(case, ok, detail):
    RESULTS.append(ok)
    print("%s %s: %s" % ("PASS" if ok else "FAIL", case, detail))


def run(events, model=None):
    m = model or M.Model()
    for ev in events:
        m.apply(ev)
    return m


def vschema(name, inst):
    return V.errors(inst, SCHEMAS[name])


# ---------------------------------------------------------------------------
def pc01_bundle_conformance():
    n, bad = 0, []
    reads = {"thread/items/list": "#/definitions/ThreadItemsListResponse",
             "thread/turns/list": "#/definitions/ThreadTurnsListResponse",
             "thread/read": "#/definitions/ThreadReadResponse"}
    os.makedirs(os.path.join(HERE, "fixtures", "native"), exist_ok=True)
    for name, fn in S.SCENARIOS.items():
        evs = fn()
        with open(os.path.join(HERE, "fixtures", "native", name + ".jsonl"), "w", encoding="utf-8") as fh:
            for ev in evs:
                rec = dict(ev)
                rec["standing"] = "constructed" if ev["ev"] in ("frame", "read") else "model-input"
                fh.write(json.dumps(rec, sort_keys=True) + "\n")
        for ev in evs:
            if ev["ev"] == "frame":
                frame = {k: v for k, v in ev["frame"].items() if k != "emittedAtMs"}
                errs = V.validate_against(frame, ROOT, "#/definitions/ServerNotification")
            elif ev["ev"] == "read":
                errs = V.validate_against(ev["result"], ROOT, reads[ev["method"]])
            else:
                continue
            n += 1
            if errs:
                bad.append((name, ev.get("frame", {}).get("method") or ev.get("method"), errs[:1]))
    extra = [({"data": [{"name": "Plan", "mode": "plan", "model": None, "reasoning_effort": None}]},
              "#/definitions/CollaborationModeListResponse"),
             ({"data": [{"name": "constructed_delegation_feature", "stage": "beta", "displayName": None,
                         "description": None, "announcement": None, "enabled": True, "defaultEnabled": False}],
               "nextCursor": None}, "#/definitions/ExperimentalFeatureListResponse")]
    for inst, ref in extra:
        n += 1
        errs = V.validate_against(inst, ROOT, ref)
        if errs:
            bad.append((ref, errs[:1]))
    result("PC-01 bundle conformance", not bad,
           "%d constructed frames and read results valid against the committed 0.158.0 bundle "
           "(emittedAtMs is TS-envelope only, HOSTING §5, and is checked beside the frame)%s"
           % (n, "" if not bad else "; %s" % bad[:3]))


def pc02_checklist():
    m = run(S.sc_plans())
    revs = m.checklist_revisions(S.P, "turn-fixture-3")
    ids = [r["revisionId"] for r in revs]
    ok = (len(revs) == 3 and [r["ordinal"] for r in revs] == [1, 2, 3]
          and ids[0].startswith("cl:%s:turn-fixture-3:g1:p" % S.P)
          and revs[1]["unchangedFromPrevious"] and not revs[2]["unchangedFromPrevious"]
          and m.checklist_state(S.P, "turn-fixture-3") == "ended"
          and all(not vschema("plan-revision", r) for r in revs))
    result("PC-02 checklist revisions", ok,
           "3 revisions, ids by generation and receipt position %s; second marked unchanged from the "
           "first (kept, not merged); state ended at turn end; each valid against npt.plan-revision" % ids)


def pc03_plan_items():
    m = run(S.sc_plans())
    revs = m.plan_revisions(S.P)
    pi1 = m.plan_items[(S.P, "item-fixture-plan-1")]
    ok = (len(revs) == 2 and revs[0]["content"]["text"].startswith("1. Read the invented")
          and pi1["deltasDiffered"] and revs[0]["contentIdentity"] != revs[1]["contentIdentity"]
          and revs[1]["ordinal"] == 2 and all(not vschema("plan-revision", r) for r in revs)
          and not pi1.get("liveDifferedFromHistory"))
    result("PC-03 plan items", ok,
           "2 plan-item revisions; the completed text replaced the delta preview (deltas differed, as "
           "PlanDeltaNotification warns); content identities differ; the on-demand history read agreed "
           "(PL-10); each valid against npt.plan-revision")


def pc04_incomplete():
    m = run(S.sc_plan_incomplete())
    pi = m.plan_items[(S.P, "item-fixture-plan-5")]
    ok = (pi["state"] == "incomplete" and m.plan_revisions(S.P) == []
          and m.checklist_state(S.P, "turn-fixture-5") == "ended"
          and m.checklists[(S.P, "turn-fixture-5")].get("observationEnded"))
    try:
        m.apply({"ev": "frame", "g": 1, "pos": 99, "frame": {"method": "turn/plan/updated", "params": {
            "threadId": S.P, "turnId": "turn-fixture-5", "explanation": None, "plan": []}}})
        late = "accepted"
    except M.TransitionRefused:
        late = "refused"
    ok = ok and late == "refused"
    m = run(S.sc_recovery_reads(), m)
    pi = m.plan_items[(S.P, "item-fixture-plan-5")]
    row = m.tool_row(S.P, "item-fixture-cmd-5")
    ok = ok and pi["state"] == "completed" and pi["standing"] == "recovered-from-supplier" \
        and row["displayState"] == "declined" and row["anchor"]["standing"] == "recovered-from-supplier"
    result("PC-04 incomplete and recovered", ok,
           "plan item started by a delta only, generation closed: incomplete, no revision; checklist "
           "ended with observation ended; a frame of the closed generation %s; later history read in the "
           "same session: plan item completed (recovered from supplier), unknown command item declined" % late)


def pc05_reload_and_relaunch():
    ev = S.sc_plans()
    a, b = run(ev), run(ev)  # window reload: re-attach by replaying host-kept events from position 0
    same = (a.checklist_revisions(S.P, "turn-fixture-3") == b.checklist_revisions(S.P, "turn-fixture-3")
            and a.plan_revisions(S.P) == b.plan_revisions(S.P))
    r = run(S.sc_plans_history())  # relaunch: a fresh model, history reads only
    live_ids = [x["revisionId"] for x in a.plan_revisions(S.P)]
    rec = r.plan_revisions(S.P)
    ok = (same and [x["revisionId"] for x in rec] == live_ids
          and [x["ordinal"] for x in rec] == [x["ordinal"] for x in a.plan_revisions(S.P)]
          and all(x["standing"] == "recovered-from-supplier" for x in rec)
          and r.checklist_revisions(S.P, "turn-fixture-3") == []
          and r.checklist_state(S.P, "turn-fixture-3") == "not-recoverable"
          and r.tool_row(S.P, "item-fixture-cmd-9")["displayState"] == "unknown")
    result("PC-05 reload and relaunch", ok,
           "reload: identical revision ids and ordinals; relaunch: plan-item revisions recovered from "
           "history with the same ids and ordinals, checklist revisions of turn-fixture-3 not recoverable "
           "after relaunch (R17-4), an in-progress history item shown unknown")


def pc06_tools():
    m = run(S.sc_tools())
    rows = {k: m.tool_row(S.P, k) for k in ("item-fixture-cmd-1", "item-fixture-fc-1", "item-fixture-mcp-1",
                                             "item-fixture-dyn-1", "item-fixture-cmd-2", "item-fixture-cmd-3")}
    c1 = rows["item-fixture-cmd-1"]
    ok = (c1["displayState"] == "completed" and c1["nativeStatus"] == "completed"
          and c1["source"] == {"atStart": "agent", "atCompletion": "unifiedExecStartup"}
          and c1["request"] == {"requestId": "srv-fixture-1", "settlementOrigin": "person-via-interaction"}
          and c1["result"] == "supplied"
          and rows["item-fixture-fc-1"]["displayState"] == "declined"
          and "request" not in rows["item-fixture-fc-1"]
          and rows["item-fixture-mcp-1"]["displayState"] == "failed"
          and rows["item-fixture-mcp-1"]["native"]["error"]["message"].startswith("invented")
          and rows["item-fixture-dyn-1"]["result"] == "not supplied by Codex"
          and rows["item-fixture-cmd-2"]["displayState"] == "unknown"
          and rows["item-fixture-cmd-3"]["displayState"] == "unknown"
          and all(not vschema("item-anchor", r["anchor"]) for r in rows.values()))
    result("PC-06 tool activity", ok,
           "command: waiting on its request, then completed, source shown at start (agent) and completion "
           "(unifiedExecStartup), settlement origin as the register supplied it; file change declined "
           "while its request was outstanding (no origin invented); MCP failed with the native error; "
           "dynamic tool completed with no result element (unavailable); two items unknown at an "
           "interrupted turn; anchors valid against npt.item-anchor")


def pc07_no_translation():
    m = run(S.sc_tools())
    bad = []
    for (th, iid), row in m.tools.items():
        out = m.tool_row(th, iid)
        native = out["native"]
        if native["type"] != row["kind"] or out["anchor"]["nativeKind"] != native["type"]:
            bad.append(iid)
        if "status" in native and out["nativeStatus"] != native["status"]:
            bad.append(iid)
        orig = [o for o in row["observations"] if o["method"] == "item/completed"]
        if orig and native.get("status") != orig[-1]["status"]:
            bad.append(iid)
    ok = not bad and m.inferred_acts() == []
    result("PC-07 no translation, no invented act", ok,
           "every row carries the native item unchanged with the supplier's type and status values; display "
           "states sit beside them; the userMessage 'Approved, I accept the sizing.' and every tool success "
           "produced no act (inferred acts: %d)" % len(m.inferred_acts()))


def pc08_delegation():
    m = run(S.sc_delegation())
    exp = m.delegation_export(S.P, S.T0 + 50, "exp-pc08")
    n = exp["nodes"][0]
    lines = m.delegation_lines(S.P)
    ok = (len(exp["nodes"]) == 1 and n["threadId"] == S.C1 and n["parentThreadId"] == S.P
          and n["spawnedBy"]["itemId"] == "item-fixture-spawn-1"
          and n["lastObserved"]["status"].startswith("active")
          and m.turn_status[(S.P, "turn-fixture-7")] == "completed"
          and m.nodes[S.C1]["state"] == "observed"
          and not vschema("delegation-export", exp)
          and not any(w in json.dumps(exp) for w in ("returned", "integrated\":", "reviewed\":")))
    result("PC-08 delegation with completed parent", ok,
           "parent turn completed while the child was last observed active; the child keeps state "
           "'observed' (no transition on parent completion); export valid against npt.delegation-export "
           "with no return/review/integration element; display: %s" % " | ".join(lines))


def pc09_observation_end_and_reads():
    m = run(S.sc_delegation_end_and_read())
    exp = m.delegation_export(S.P, S.T0 + 300, "exp-pc09")
    by = {x["threadId"]: x for x in exp["nodes"]}
    ok = (set(by) == {S.C1, S.C2} and by[S.C1]["parentSource"] == "thread/read"
          and by[S.C1]["agentRole"] == "reviewer" and by[S.C1]["sessionId"] == "ses-fixture-1"
          and by[S.C1]["lastObserved"]["source"] == "thread/read"
          and by[S.C2]["depth"] == 2 and by[S.C2]["parentThreadId"] == S.C1
          and not vschema("delegation-export", exp))
    m2 = run(S.sc_delegation() + [{"ev": "closed", "g": 1, "reason": "exited-unexpectedly"}])
    n = m2.nodes[S.C1]
    ok = ok and n["state"] == "observation-ended" and n["observationEnded"] \
        and n["lastObserved"]["status"].startswith("active")
    m3 = run(S.sc_not_found())
    ok = ok and m3.nodes[S.C1]["state"] == "not-found" and m3.nodes[S.C2]["state"] == "observed" \
        and m3.nodes[S.C2]["lastObserved"]["source"] == "thread/read"
    result("PC-09 observation end and child reads", ok,
           "generation closed: child observation ended, last observed value kept (never 'completed'); "
           "after restart a child frame and thread/read restore it with Codex's parent, session, role and "
           "depth; a grandchild found by thread/read joins the export; notFound kept as reported")


def pc10_task_role():
    m = run(S.sc_delegation(task_role=True))
    exp = m.delegation_export(S.P, S.T0 + 50, "exp-pc10")
    lines = m.delegation_lines(S.P)
    ok = (exp["nodes"][0]["delegatingRole"] == {"role": "TASK", "statement": "stated-not-enforced"}
          and any("stated, not enforced" in x for x in lines) and not vschema("delegation-export", exp))
    m0 = run(S.sc_delegation())
    ok = ok and m0.delegation_export(S.P, 0, "x")["nodes"][0]["delegatingRole"] is None
    result("PC-10 task-agent delegation (K-10)", ok,
           "a spawn by a conversation whose role (a runtime value from DEL-02-04) is TASK is shown and "
           "exported as 'stated, not enforced'; nothing blocks it; without the role value nothing is marked")


def pc11_version():
    m = run([S.ready(1)])
    l1 = m.version_lines()
    m2 = run([S.ready(1, label="codex-cli 0.159.0")])
    l2 = m2.version_lines()
    m3 = run([S.ready(1, result="mismatch", detail="mismatch(distribution content identity)")])
    l3 = m3.version_lines()
    m4 = run([S.ready(1, result="verified")])
    l4 = m4.version_lines()
    ok = ("unverified development run" in l1[0] and "definition pin, not qualified" in l1[1]
          and "compatibility not verified" in l2[1] and "mismatch(distribution content identity)" in l3[0]
          and "verified" in l4[0] and "no qualification reference supplied" in l4[0]
          and not any("verified" in x and "not" not in x and "unverified" not in x for x in l1 + l2))
    result("PC-11 version identity display", ok,
           "development run (U-06): %r / %r; label 0.159.0: %r; mismatch: %r; 'verified' shown only from "
           "a verified result: %r" % (l1[0], l1[1], l2[1], l3[0], l4[0]))


def pc12_experimental_and_plan_mode():
    masks = {"ev": "mode-list", "result": {"data": [{"name": "Plan", "mode": "plan", "model": None,
                                                     "reasoning_effort": None}]}}
    sel = {"ev": "runtime", "kind": "model-selection", "threadId": S.P, "model": "fixture-local-model"}
    nosel = {"ev": "runtime", "kind": "model-selection", "threadId": S.P, "model": None}
    off = run([S.ready(1, experimental=False), masks, sel])
    on = run([S.ready(1), masks, sel])
    on_nomodel = run([S.ready(1), masks, nosel])
    off_c = off.plan_mode_control()
    on_c = on.plan_mode_control()
    p = on.turn_start(S.P, "Plan the invented sizing.", "plan")
    carry = on.turn_start(S.P, "Carry out this plan.", "default")
    refused = on_nomodel.turn_start(S.P, "Plan it.", "plan")
    e1 = V.validate_against(p["params"], ROOT, "#/definitions/TurnStartParams")
    e2 = V.validate_against(carry["params"], ROOT, "#/definitions/TurnStartParams")
    stable_still = run([S.ready(1, experimental=False)] + S.sc_plans()[1:])
    M.FEATURE_NAMES_FOR_SURFACE["delegation"] = {"constructed_delegation_feature"}
    on.apply({"ev": "feature-list", "result": {"data": [{"name": "constructed_delegation_feature", "stage": "beta",
                                                         "displayName": None, "description": None,
                                                         "announcement": None, "enabled": True,
                                                         "defaultEnabled": False}], "nextCursor": None}})
    lab_deleg = on.experimental_label("delegation")
    M.FEATURE_NAMES_FOR_SURFACE["delegation"] = set()
    lab_deleg_none = on.experimental_label("delegation")
    ok = (not off_c["offered"] and on_c == {"offered": True, "label": "experimental"}
          and p["params"]["collaborationMode"]["mode"] == "plan"
          and p["params"]["collaborationMode"]["settings"]["developer_instructions"] is None
          and not e1 and not e2 and carry["actRecorded"] is False
          and carry["params"]["collaborationMode"]["mode"] == "default"
          and refused == {"refused": M.NO_MODEL}
          and len(stable_still.checklist_revisions(S.P, "turn-fixture-3")) == 3
          and on.experimental_label("plan-mode", "turn/start.collaborationMode")
          and lab_deleg and not lab_deleg_none)
    result("PC-12 experimental surfaces and plan mode (K-5, K-3, R17-9)", ok,
           "opt-in not declared: control absent (%s) while stable plan items still render; declared with a "
           "plan preset: offered, labelled experimental; plan turn/start and 'carry out this plan' "
           "(collaborationMode default, no act recorded) valid against TurnStartParams; no model selected: "
           "'%s'; delegation labelled experimental only when a mapped Codex feature is beta "
           "(constructed name; real name OBS-2 pending)" % (off_c["reason"], M.NO_MODEL))


def pc13_acts():
    m = run(S.sc_plans())
    rev = m.plan_revisions(S.P)[1]
    anchor = {"anchorKind": "plan-revision", "threadId": S.P, "turnId": rev["turnId"],
              "revisionId": rev["revisionId"], "standing": "live-observed"}
    good = {"subject": anchor, "actKind": "A5", "decisionActor": {"name": "Fixture Person"},
            "recorder": "App", "boundContent": rev["contentIdentity"]["value"][:12],
            "scope": "plan revision 2", "purpose": "fixture: accept the proposed plan as a proposal"}
    bad = dict(good, decisionActor={"name": "App"})
    m.apply({"ev": "runtime", "kind": "act-record", "record": good})
    m.apply({"ev": "runtime", "kind": "act-record", "record": bad})
    lines = m.acts_for(anchor)
    ok = (not vschema("item-anchor", anchor) and len(lines) == 2
          and "A5 by Fixture Person (identity not verified) · recorded by App" in lines[0]
          and lines[1].startswith("record not shown: non-conformant") and m.inferred_acts() == [])
    result("PC-13 truthful actor (REQ-005)", ok,
           "a supplied act record on a plan-revision anchor shown with actor and recorder apart and "
           "'identity not verified'; a record naming the recorder as actor not shown as an act; no act "
           "inferred from any item. Synthetic subjects; no real decision")


def pc14_schema_fixtures():
    lines, ok = [], True
    for n in SCHEMAS:
        for kind in ("valid", "invalid"):
            inst = json.load(open(os.path.join(HERE, "fixtures", "%s.%s.json" % (n, kind)), encoding="utf-8"))["instance"]
            errs = vschema(n, inst)
            good = (not errs) if kind == "valid" else bool(errs)
            ok &= good
            lines.append("%s.%s: %s" % (n, kind, "valid" if not errs else "invalid (%s)" % errs[0]))
    result("PC-14 schema fixtures", ok, " | ".join(lines))


def pc15_tables():
    """Every row of the four tables reached by the scenarios; the Design file's tables equal the model's."""
    used = set()
    for name, fn in S.SCENARIOS.items():
        m = run(fn())
        used |= m.used
    m = run(S.sc_plan_incomplete())
    m = run(S.sc_recovery_reads(), m)
    used |= m.used
    all_ids = {rid for t in M.TABLES.values() for rid in t}
    missing = sorted(all_ids - used)
    text = open(MDFILE, encoding="utf-8").read()
    md = {}
    for line in text.splitlines():
        mm = re.match(r"^\| ((?:PL|CL|TI|DS)-\d\d) \| `([^`]+)` \| ([a-z-]+) \| `([^`]+)` \|", line)
        if mm:
            md[mm.group(1)] = (mm.group(2), mm.group(3), mm.group(4))
    model = {rid: row for t in M.TABLES.values() for rid, row in t.items()}
    diff = sorted(set(md.items()) ^ set(model.items()))
    probe = M.Model()
    try:
        probe._step("TI", "completed", "item-started")
        refused = False
    except M.TransitionRefused:
        refused = True
    ok = not missing and not diff and refused
    result("PC-15 transition tables", ok,
           "%d/%d rows reached (missing %s); Design-file tables equal the model's (%d rows; differences %s); "
           "a transition outside the tables is refused" % (len(all_ids) - len(missing), len(all_ids),
                                                           missing or "none", len(md), diff[:4] or "none"))


def main():
    for f in (pc01_bundle_conformance, pc02_checklist, pc03_plan_items, pc04_incomplete,
              pc05_reload_and_relaunch, pc06_tools, pc07_no_translation, pc08_delegation,
              pc09_observation_end_and_reads, pc10_task_role, pc11_version,
              pc12_experimental_and_plan_mode, pc13_acts, pc14_schema_fixtures, pc15_tables):
        try:
            f()
        except Exception as e:  # a crash is a failed case, reported
            result(f.__name__, False, "exception %s: %s" % (type(e).__name__, e))
    print("SUMMARY %d/%d cases gave their expected result" % (sum(RESULTS), len(RESULTS)))
    return 0 if all(RESULTS) else 1


if __name__ == "__main__":
    sys.exit(main())
