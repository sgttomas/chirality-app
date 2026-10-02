"""Run the DEL-01-04 design cases that a local prototype can run (NIR-v0.2 §13, AAC-v0.2 §8).

    python3 run_cases.py            # one line per check; exit status 0 when all are as expected

Design prototype only (R17-1; R12-3). Python 3 standard library only, plus two
read-only imports of first-increment prototypes: DEL-04-03's validator and
record writer (minischema.py, record_store.py) and DEL-01-01's validator
(jsonschema_subset.py), so the entries this prototype makes are checked by the
owners' own PROPOSED schemas. If the already-installed `jsonschema` package is
importable, the five DEL-01-04 schemas are also cross-checked with it; nothing
is installed. No network; Codex is never started; all content is invented.
A pass here is evidence about the design ("pass (model)"), never a VER pass:
no App candidate exists.
"""

import copy
import glob
import hashlib
import json
import os
import sys
import tempfile

sys.dont_write_bytecode = True     # never write caches into this or the imported prototypes' folders

HERE = os.path.dirname(os.path.abspath(__file__))
DESIGN = os.path.dirname(HERE)
WORKING = os.path.dirname(os.path.dirname(DESIGN))           # .../PKG-01.../1_Working
EXEC_ROOT = os.path.dirname(os.path.dirname(WORKING))        # .../execution
RS_DESIGN = glob.glob(os.path.join(EXEC_ROOT, "PKG-04_*", "1_Working", "DEL-04-03_*", "Design"))[0]
ACT_DESIGN = glob.glob(os.path.join(EXEC_ROOT, "PKG-04_*", "1_Working", "DEL-04-01_*", "Design"))[0]
AS_DESIGN = glob.glob(os.path.join(EXEC_ROOT, "PKG-04_*", "1_Working", "DEL-04-02_*", "Design"))[0]
HOSTING_DESIGN = glob.glob(os.path.join(WORKING, "DEL-01-01_*", "Design"))[0]
WR_DESIGN = glob.glob(os.path.join(EXEC_ROOT, "PKG-02_*", "1_Working", "DEL-02-02_*", "Design"))[0]
WD_DESIGN = glob.glob(os.path.join(EXEC_ROOT, "PKG-02_*", "1_Working", "DEL-02-01_*", "Design"))[0]

sys.path.insert(0, HERE)
sys.path.insert(1, os.path.join(RS_DESIGN, "prototype"))
sys.path.insert(2, os.path.join(HOSTING_DESIGN, "prototype"))

from minischema import Registry, validate, check_supported   # noqa: E402  (DEL-04-03, read only)
from record_store import Writer, Reader, WriteFailed          # noqa: E402  (DEL-04-03, read only)
import jsonschema_subset as hosting_js                        # noqa: E402  (DEL-01-01, read only)
import nir_model as nm                                        # noqa: E402
from act_control import ActControl, NATIVE_SOURCE, from_wr_descriptor   # noqa: E402

FAIL = []
COUNT = [0]


def check(cond, label):
    COUNT[0] += 1
    print(("PASS " if cond else "FAIL ") + label)
    if not cond:
        FAIL.append(label)


def load(p):
    with open(p, encoding="utf-8") as fh:
        return json.load(fh)


SCHEMAS = ["nir.answer-submission", "nir.attachment-supply-record", "nir.draft-transition",
           "aac.offer", "aac.capture-evidence"]


def main():
    scratch = tempfile.mkdtemp(prefix="d3-del-01-04-")
    reg = Registry()
    ids = {}
    print("== S schemas and examples ==")
    for name in SCHEMAS:
        ids[name] = reg.load(os.path.join(DESIGN, name + ".schema.json"))
        check(True, f"S-1 {name}.schema.json loads; every keyword is in the validator's subset")
    for name, d, f in (("ACT", ACT_DESIGN, "ACT_POLICY_CLASS_RECORD.schema.json"),
                       ("AS", AS_DESIGN, "AS_SETTINGS_IN.schema.json"),
                       ("RS", RS_DESIGN, "RS_RECORD.schema.json")):
        ids[name] = reg.load(os.path.join(d, f))
    rs_entry = {"$ref": ids["RS"] + "#/$defs/entry"}
    for name in SCHEMAS:
        schema = reg.by_id[ids[name]]
        vf = load(os.path.join(DESIGN, name + ".example.valid.json"))
        for v in vf.get("instances") or [vf["instance"]]:
            errs = validate(v, schema, reg)
            check(not errs, f"S-2 {name} valid example is valid {errs[:1] if errs else ''}")
        for c in load(os.path.join(DESIGN, name + ".example.invalid.json")):
            errs = validate(c["instance"], schema, reg)
            check(bool(errs), f"S-3 {name} {c['case']} invalid as expected -> {errs[0][:100] if errs else 'NOT REJECTED'}")
    try:
        import jsonschema
        from importlib.metadata import version as _version
        ok = True
        for name in SCHEMAS:
            schema = load(os.path.join(DESIGN, name + ".schema.json"))
            jsonschema.Draft202012Validator.check_schema(schema)
            val = jsonschema.Draft202012Validator(schema)
            vf = load(os.path.join(DESIGN, name + ".example.valid.json"))
            ok &= all(val.is_valid(v) for v in (vf.get("instances") or [vf["instance"]]))
            ok &= all(not val.is_valid(c["instance"]) for c in load(os.path.join(DESIGN, name + ".example.invalid.json")))
        check(ok, f"S-4 optional third-party cross-check with the installed jsonschema {_version("jsonschema")}: same verdicts on all examples")
    except ImportError:
        print("SKIP S-4 jsonschema not importable (optional third-party cross-check; nothing installed)")

    hosting_schema = load(os.path.join(HOSTING_DESIGN, "hosting.server-request-entry.schema.json"))

    def hosting_valid(entry):
        return hosting_js.errors(entry, hosting_schema)

    person = {"displayName": "Engineer A", "osAccount": "enga", "identityVerified": False}

    # ------------------------------------------------------------------ C cards
    print("\n== C request cards (NIR §4.1-§4.3; VER-001) ==")
    off = {"experimentalApi": False, "requestAttestation": False}
    on = {"experimentalApi": True, "requestAttestation": True}
    cls_off = {m: nm.classify(m, off)[0] for m in nm.KINDS}
    cls_on = {m: nm.classify(m, on)[0] for m in nm.KINDS}
    check(sum(1 for m in nm.KINDS if nm.KINDS[m]["card"]) == 7 and len(nm.KINDS) == 11,
          "C-1 11 server-request kinds at 0.158.0; 7 are person cards, 4 are not")
    check(cls_off["currentTime/read"] == "unfamiliar" and cls_off["attestation/generate"] == "unfamiliar"
          and cls_on["currentTime/read"] == "known-answerable" and cls_on["attestation/generate"] == "known-app-unsupported",
          "C-2 classification follows the declared capabilities (HOSTING §6.1 familiar set)")
    ob5 = {"threadId": "thr-ex-1", "turnId": "turn-ex-1", "itemId": "item-ex-1", "startedAtMs": 1, "kind": "command",
           "command": "/bin/zsh -lc 'echo ok'", "proposedExecpolicyAmendment": ["echo"],
           "availableDecisions": ["accept", {"acceptWithExecpolicyAmendment": {"execpolicy_amendment": ["echo"]}}, "cancel"]}
    card = nm.card_for("item/commandExecution/requestApproval", ob5, off)
    names = [nm._form_name(f["native"]) for f in card["forms"]]
    check(names == ["accept", "acceptWithExecpolicyAmendment", "cancel"] and card["formsSource"] == "availableDecisions",
          f"C-3 a request's availableDecisions are offered exactly (OB-5 shape): {names}")
    check(card["decline"]["native"] == {"decision": "cancel"} and "interrupts the turn" in card["decline"]["standing"],
          f"C-4 with no `decline` offered, the decline is the native `cancel`, shown as also interrupting the turn")
    gen = dict(ob5)
    gen.pop("availableDecisions")
    gen.pop("proposedExecpolicyAmendment")
    names = [nm._form_name(f["native"]) for f in nm.card_for("item/commandExecution/requestApproval", gen, off)["forms"]]
    check(names == ["accept", "acceptForSession", "decline", "cancel"],
          f"C-5 without availableDecisions, generated forms; amendment forms only when proposed: {names}")
    leaks = []
    for m in nm.KINDS:
        if nm.KINDS[m]["card"] and nm.KINDS[m]["originClass"] == nm.A14:
            prose = nm.app_prose(nm.card_for(m, {"proposedExecpolicyAmendment": ["x"], "permissions": {}}, off))
            leaks += [(m, w) for w in nm.FORBIDDEN_APP_WORDS if w in prose]
    check(not leaks, f"C-6 no tool-permission card uses 'accept', 'approve', 'approval' or 'approved' as App words (ACT §9; AS DS-1) {leaks}")
    dm = {m: nm.decline_form(m, gen if m == "item/commandExecution/requestApproval" else {})
          for m in nm.KINDS if nm.KINDS[m]["card"]}
    check(all(v["native"] is not None for v in dm.values()),
          "C-7 every card kind has an explicit decline: " + "; ".join(f"{m.split('/')[-1]}={v['standing']}" for m, v in dm.items()))
    q = {"threadId": "thr-ex-1", "turnId": "turn-ex-2", "itemId": "item-ex-9", "isBlocking": False, "autoResolutionMs": 60000,
         "questions": [{"id": "q1", "header": "Token", "question": "Paste the test token", "isOther": True, "isSecret": True, "options": None}]}
    qc = nm.card_for("item/tool/requestUserInput", q, off)
    check(qc["forms"][0]["secret"] and any("isBlocking false" in n for n in qc["notes"])
          and any("never answers it by itself" in n for n in qc["notes"]),
          "C-8 question card: secret input masked; non-blocking and supplier auto-resolution shown as information, no App countdown")
    el = nm.card_for("mcpServer/elicitation/request", {"threadId": "t", "turnId": None, "serverName": "ex-server",
                                                       "mode": "openai/userVerification", "title": "x", "description": "y",
                                                       "challenge": "z", "_meta": None}, off)
    check("not established" in el["requester"] and any("only you can complete it" in n for n in el["notes"]),
          "C-9 elicitation card names the requester 'MCP server or the agent (not established)'; verification mode never completed by the App")

    # ------------------------------------------------------------------ R register walk
    print("\n== R card states over the register (NIR §4.4; HOSTING §6.2.1) ==")
    rd = nm.RegisterDouble(declared=off)
    pid = nm.person_ref(person)
    P = {"class": "person-via-interaction", "actorRef": pid}
    # RT-01, RT-02 unfamiliar; RT-03 app-unsupported
    rd.receive("r-unf", "attestation/generate", {}, 1)
    rd.receive("r-dyn", "item/tool/call", {"threadId": "thr-ex-1"}, 1)
    # RT-04, RT-05 (invalid), RT-06, RT-07, RT-12
    rd.receive("r1", "item/commandExecution/requestApproval", ob5, 1)
    ok, why = rd.answer("r1", {"decision": "decline"}, P)            # not offered by the request
    check(not ok and why == "invalid-answer" and nm.card_state(rd.entries["r1"])[0] == "CS-1",
          f"R-1 an answer the request does not offer is refused '{why}'; the card keeps waiting with the reason")
    sub = nm.answer_submission(rd.entries["r1"], {"decision": "accept"}, person, ob5["availableDecisions"], "t1")
    sub["submittedAs"] = "answer"
    check(not validate(sub, reg.by_id[ids["nir.answer-submission"]], reg), "R-2 the card's answer submission is valid against its schema")
    ok, _ = rd.answer("r1", sub["nativeAnswer"], sub["origin"])
    s3 = nm.card_state(rd.entries["r1"])
    rd.supplier_resolved("r1")
    s3a = nm.card_state(rd.entries["r1"])
    check(ok and s3[0] == "CS-3" and s3a[0] == "CS-3a",
          f"R-3 written is not acknowledged: '{s3[1]}' then '{s3a[1]}'")
    ok, why = rd.answer("r1", {"decision": "accept"}, P)
    check(not ok and why == "already-settled", f"R-4 a second answer is refused '{why}'")
    # RT-08, RT-13: decline by the person (cancel)
    rd.receive("r2", "item/commandExecution/requestApproval", ob5, 1)
    rd.answer("r2", {"decision": "cancel"}, P)
    s4 = nm.card_state(rd.entries["r2"])
    rd.supplier_resolved("r2")
    check(s4[0] == "CS-4" and nm.card_state(rd.entries["r2"])[0] == "CS-4a", f"R-5 the person's decline: '{s4[1]}'")
    # RT-09 write failure
    rd.receive("r3", "item/fileChange/requestApproval", {"threadId": "t", "turnId": "u", "itemId": "i", "startedAtMs": 2}, 1)
    rd.answer("r3", {"decision": "accept"}, P, write_ok=False)
    check(nm.card_state(rd.entries["r3"])[0] == "CS-5", f"R-6 write failure: '{nm.card_state(rd.entries['r3'])[1]}'")
    # silence: nothing happens however long; RT-10 supplier resolution
    rd.receive("r4", "item/tool/requestUserInput", q, 1)
    before = copy.deepcopy(rd.public("r4"))
    for _ in range(24 * 60):        # a simulated day of minutes passes; the model has no timer at all
        pass
    check(rd.public("r4") == before and nm.card_state(rd.entries["r4"])[0] == "CS-1",
          "R-7 silence: after a simulated day the question still waits; no automatic decline exists (R17-9)")
    view1 = [nm.card_state(e) for e in rd.list_outstanding()]
    view2 = [nm.card_state(e) for e in rd.list_outstanding()]          # window closed and reopened: rebuilt from the register
    check(view1 == view2 and rd.entries["r4"]["state"] == "outstanding",
          "R-8 observer closure and reload rebuild the same cards from 'list outstanding'; closing answers nothing")
    rd.supplier_resolved("r4", cause=None)
    check(nm.card_state(rd.entries["r4"])[0] == "CS-6" and "not reported" in nm.card_state(rd.entries["r4"])[1],
          f"R-9 resolved by Codex before an answer: '{nm.card_state(rd.entries['r4'])[1]}'")
    ok, why = rd.answer("r4", {"answers": {"q1": {"answers": ["x"]}}}, P)
    check(not ok and why == "already-resolved", f"R-10 answering a supplier-resolved request is refused '{why}'")
    # empty answer map as decline (PROPOSED)
    rd.receive("r5", "item/tool/requestUserInput", q, 1)
    rd.answer("r5", {"answers": {}}, P)
    check(rd.entries["r5"]["state"] == "declined", "R-11 PROPOSED decline of a question: the empty answer map, settled as a decline")
    # RT-11 generation closed
    rd.receive("r6", "mcpServer/elicitation/request", {"threadId": "t", "turnId": "u", "serverName": "ex", "mode": "form",
                                                      "message": "m", "requestedSchema": {}, "_meta": None}, 1)
    rd.close_generation(1)
    ok, why = rd.answer("r6", {"action": "accept", "content": {}, "_meta": None}, P)
    check(nm.card_state(rd.entries["r6"])[0] == "CS-7" and why == "generation-closed",
          f"R-12 Codex ended: '{nm.card_state(rd.entries['r6'])[1]}'; a late answer is refused '{why}'")
    ok, why = rd.answer("r-none", {"decision": "accept"}, P)
    check(not ok and why == "no-such-request", f"R-13 unknown identity refused '{why}'")
    # app rule cannot answer affirmatively
    rd2 = nm.RegisterDouble(declared=off)
    rd2.receive("x1", "item/fileChange/requestApproval", {"threadId": "t"}, 1)
    ok, why = rd2.answer("x1", {"decision": "accept"}, {"class": "app-rule", "ruleName": "auto"})
    check(not ok and why == "origin-not-permitted", f"R-14 an App rule's affirmative answer is refused '{why}' (R9)")
    check(rd.rt_seen | rd2.rt_seen == {f"RT-{i:02d}" for i in range(1, 14)},
          f"R-15 all 13 register rows reached and each maps to one card state: {sorted(rd.rt_seen | rd2.rt_seen)}")
    bad = [(r, hosting_valid(rd.public(r))[:1]) for r in rd.order if hosting_valid(rd.public(r))]
    check(not bad, f"R-16 every register entry the walk produced is valid against HOSTING's PROPOSED entry schema {bad}")
    states = {nm.card_state(rd.entries[r])[0] for r in rd.order}
    print("     final card states of the walk:", ", ".join(sorted(states)))

    # ------------------------------------------------------------------ O outcomes
    print("\n== O turn and outcome presentation (NIR §5; VER-002) ==")
    lbl = {
        "live": nm.turn_label("inProgress", "live"),
        "lost": nm.turn_label(None, "lost"),
        "lost-in-progress": nm.turn_label("inProgress", "lost"),
        "you": nm.turn_label("interrupted", "live", "person"),
        "quit": nm.turn_label("interrupted", "live", "quit"),
        "codex-stop": nm.turn_label("interrupted", "live", "codex-stop"),
        "cancel": nm.turn_label("interrupted", "live", "cancel-answer"),
        "plain": nm.turn_label("interrupted", "live"),
        "desc": nm.turn_label("completed", "live", descendants={"thr-c1": "running", "thr-c2": "completed", "thr-c3": None}),
    }
    for k, v in lbl.items():
        print(f"     {k}: {v}")
    check(lbl["lost"].startswith("TO-6") and lbl["lost-in-progress"].startswith("TO-6"),
          "O-1 observation lost before an end: outcome unknown, never completed or interrupted")
    check("1 delegated agent(s) last reported running" in lbl["desc"] and "no reported state" in lbl["desc"],
          "O-2 primary completion with a running delegated agent says so; it never implies the descendant finished")
    check(all("Stopped" not in v and "stopped" not in v for v in lbl.values()) and "cause not observed" in lbl["plain"],
          "O-3 an interruption is never called 'stopped' (R17-3); its cause is shown only when observed")
    check(lbl["codex-stop"] == "TO-4 Interrupted (interrupted by Stop Codex)" and lbl["quit"].endswith("(interrupted by quit)"),
          "O-3a TO-4 uses RECOVERY-v0.2 §3.4's labels: 'interrupted by quit', 'interrupted by Stop Codex' (V21-A MINOR 4)")
    v0 = nm.start_view(None, {"model": "qwen/qwen3.5-9b", "provider": "lmstudio", "chosenAt": "2026-09-30"})
    check(v0["model"] is None and not v0["sendable"] and v0["offer"]["applied"] is False
          and v0["sendResult"].startswith("not started — no model selected"),
          "O-4 K-3: a new conversation starts with no model; the last choice is offered, never applied; sending keeps the message")
    vr = nm.start_view(None, None, workflow_run=True)
    check(vr["sendResult"].startswith("run not started — no model selected"),
          "O-5 R18-2 (C-09): a workflow run reads 'run not started — no model selected'; a conversation 'not started — …'")
    v5 = nm.start_view({"model": "m", "provider": "p"}, None, roles=["HELP_HUMAN", "WORKING_ITEMS", "HELPS_HUMANS", "TASK"],
                       default_role="HELP_HUMAN")
    okc, _ = nm.choose_role(v5, "no role")
    check(v5["role"]["preselected"] == "HELP_HUMAN" and v5["role"]["clearable"] and okc and v5["role"]["chosen"] == "no role",
          "O-6 ST-5 (C-15): role preselected from default_for_new_chat, clearable; 'no role' allowed")
    st_items = nm.settle_items_at_turn_end({"msg-1": "completed", "rsn-1": "in progress"}, "interrupted")
    check(st_items["rsn-1"] == "not completed (turn ended interrupted)" and st_items["msg-1"] == "completed",
          "O-7 G-4: an item still open at turn end settles 'not completed (turn ended …)'")
    # C-06 turn composition
    conv = {"threadId": "thr-ex-9", "model": {"model": "qwen/qwen3.5-9b", "provider": "lmstudio"}}
    plan_el = {"collaborationMode": {"mode": "plan", "settings": {"model": "qwen/qwen3.5-9b", "reasoning_effort": None,
                                                                  "developer_instructions": None}}}
    t0, _ = nm.compose_turn(conv, "hello")
    t1, _ = nm.compose_turn(conv, "plan this", plan_chosen=True, plan_element=plan_el)
    t2, _ = nm.compose_turn(conv, "carry out this plan")
    tr, _ = nm.compose_turn(conv, "go", run_start_text="[run start text composed by DEL-02-02]")
    att_in = [nm.attachment_input("text-element", "notes.md", "data/notes.md", b"alpha\n")[0],
              nm.attachment_input("localImage", "crack.png", "/ex/p/site/crack.png", b"\x89PNG")[0],
              nm.attachment_input("path-named", "beam.xlsx", "data/beam.xlsx", b"PK\x03\x04")[0]]
    ta, _ = nm.compose_turn(conv, "see attached", attachments=att_in,
                            run_end_line="[run end line composed by DEL-02-02]")
    tn, whyn = nm.compose_turn({"threadId": "t", "model": None}, "hi")
    check("collaborationMode" not in t0 and t1["collaborationMode"]["mode"] == "plan"
          and t2["collaborationMode"]["mode"] == "default" and tr["collaborationMode"]["mode"] == "default"
          and tr["input"][0]["text"].startswith("[run start") and tn is None,
          "O-8 C-06: plan mode from NPTD's element; every later turn sends mode 'default' explicitly (O-8); run-start text first")
    try:
        import jsonschema
        bundle = load(os.path.join(HOSTING_DESIGN, "generated", "0.158.0", "json-schema", "experimental",
                                   "codex_app_server_protocol.v2.schemas.json"))
        tsp = dict(bundle["definitions"]["TurnStartParams"])
        tsp["definitions"] = bundle["definitions"]
        val = jsonschema.Draft7Validator(tsp)
        check(all(val.is_valid(x) for x in (t0, t1, t2, tr, ta)),
              "O-9 composed turn/start parameters, with a run-end line and the three attachment carriers, are valid against "
              "the committed 0.158.0 TurnStartParams (optional third-party cross-check: installed jsonschema)")
    except ImportError:
        print("SKIP O-9 jsonschema not importable (optional third-party cross-check)")
    check([x["type"] for x in ta["input"]] == ["text", "text", "text", "localImage", "text"]
          and ta["input"][0]["text"].startswith("[run end") and ta["input"][1]["text"] == "see attached",
          "O-8a TC-2: the run-end line (R20-3; WR TX-5) first, then the person's text, then the attachments (text element, "
          "image input, named path)")
    # C-24 indicator
    regA = nm.RegisterDouble(declared=off); regA.receive("a1", "item/tool/requestUserInput", q, 1)
    regB = nm.RegisterDouble(declared=off); regB.receive("b1", "item/fileChange/requestApproval", {"threadId": "t"}, 1)
    regB.receive("b2", "item/fileChange/requestApproval", {"threadId": "t"}, 1)
    ind = nm.waiting_indicator({"conv-A": regA, "conv-B": regB}, {"conv-B": 2})
    regB.answer("b1", {"decision": "accept"}, {"class": "person-via-interaction", "actorRef": pid})
    okw, whyw = regB.answer("b1", {"decision": "decline"}, {"class": "person-via-interaction", "actorRef": pid})
    ind2 = nm.waiting_indicator({"conv-A": regA, "conv-B": regB}, {"conv-B": 2})
    check(ind["total"] == 3 and {r["conversation"] for r in ind["conversations"]} == {"conv-A", "conv-B"}
          and ind2["total"] == 2 and not okw and whyw == "already-settled",
          "O-10 C-24: an App-level count of waiting requests, with or without a window; a second window's answer is refused")
    # R19-2 (b) start offer
    registered = [{"origin": "project", "name": "load-check", "revision": "rev-1"},
                  {"origin": "project", "name": "supports-adjust", "revision": "rev-5"}]
    of1 = nm.start_offer("Done.\nNext workflow: project:load-check", registered, None)
    of2 = nm.start_offer("Next workflow: project:load-check", registered, "supports-adjust#1")
    of3 = nm.start_offer("You might want to run load-check next.", registered, None)
    of4 = nm.start_offer("Next workflow: project:unknown", registered, None)
    of5 = nm.start_offer("Next workflow: project:load-check\nThat is my suggestion.", registered, None)
    of6 = nm.start_offer("Next workflow: project:supports-adjust\nNext workflow: project:load-check", registered, None)
    sel = nm.confirm_start(of1)
    check(of1["enabled"] and of1["startsNothingByItself"] and of1["label"].startswith("Start load-check")
          and of2["enabled"] and of2["label"] == "End supports-adjust#1 and start load-check"
          and of2["endsRun"]["cause"] == "ended to start load-check"
          and of3 is None and of4["offer"] is None and of5 is None and of6 is None and sel["selectedBy"] == "the person",
          "O-11 R19-2 (b), R20-11 (1), (2), (4): 'Start ‹B›' only with no run; during a run only 'End ‹A› and start ‹B›' (cause 'ended to start ‹B›'); the proposal line must be the last line, once")
    # RN-7 finished report (R20-1, R20-9, R20-11 (2))
    run = {"run": "supports-adjust#1", "origin": "project", "name": "supports-adjust"}
    fo1 = nm.finished_offer("All checked.\nWorkflow finished: project:supports-adjust", run)
    fo2 = nm.finished_offer("Workflow finished: project:supports-adjust\nNext workflow: project:load-check", run)
    of7 = nm.start_offer("Workflow finished: project:supports-adjust\nNext workflow: project:load-check", registered,
                         "supports-adjust#1", finished=fo2 is not None)
    fo3 = nm.finished_offer("Workflow finished: project:supports-adjust\nLet me know.", run)
    fo4 = nm.finished_offer("Workflow finished: project:load-check", run)
    fo5 = nm.finished_offer("Workflow finished: project:supports-adjust", None)
    check(fo1 and fo1["label"] == "End run" and fo1["endsRun"]["cause"] == "completed" and fo1["endsNothingByItself"]
          and fo2 and of7["endsRun"]["cause"] == "completed" and fo3 is None and fo4 is None and fo5 is None,
          "O-13 RN-7: 'End run' on the exact finished line (last line, or just before the proposal line) naming the run in force; with a proposal, 'End ‹A› and start ‹B›' ends A 'completed'; nothing otherwise")
    # R19-3/R19-8 continue as role
    ca = nm.continue_as({"threadId": "thr-ex-9", "role": "HELP_HUMAN"}, "WORKING_ITEMS",
                        ["the person's last request", "the last workflow run and how it ended", "the attachments supplied"])
    comp = nm.handoff_composer(ca, "The person asked for … Run supports-adjust rev-5 ended by the person.")
    comp0 = nm.handoff_composer(ca, None)
    check(ca["newConversation"] and not ca["fork"] and ca["model"] is None
          and ca["sourceTurn"]["threadId"] == "thr-ex-9" and ca["sourceTurn"]["visible"]
          and comp["header"] == "Handoff from conversation thr-ex-9 (HELP_HUMAN)." and comp["text"].startswith(comp["header"])
          and comp["editable"] and not comp["sent"] and comp0["text"] == comp0["header"] and not comp0["sent"],
          "O-12 R19-3/R19-8, R20-6: 'Continue as ‹role›' opens a new conversation; the source agent drafts the summary in a visible turn there; the person edits it under an App header; nothing sent")

    # ------------------------------------------------------------------ A attachments
    print("\n== A attachments (NIR §6; VER-003; R21-2) ==")
    att_schema = reg.by_id[ids["nir.attachment-supply-record"]]
    el1, tx1 = nm.attachment_input("text-element", "notes.md", "/ex/p/notes.md", b"alpha\n")
    r1, d1 = nm.supply_record("att-1", "notes.md", "text-element", "/ex/p/notes.md", b"alpha\n", b"alpha\n", "turn:t/1", "t1",
                              element_text=tx1)
    check(d1 == "sent" and not validate(r1, att_schema, reg) and tx1.endswith("alpha\n") and "notes.md" in tx1.split("\n")[0]
          and r1["supplyStanding"] == "supplied" and r1["elementIdentity"] == nm.text_identity(el1["text"]),
          "A-1 a text file is supplied as a text element naming the file, then its bytes; the supply record is valid")
    r2, d2 = nm.supply_record("att-2", "notes.md", "text-element", "/ex/p/notes.md", b"alpha\n", b"alpha-changed\n", "turn:t/2", "t2")
    check(d2.startswith("held") and not validate(r2, att_schema, reg),
          f"A-2 content changed between selection and submission is held, never sent silently: '{d2}'")
    r3, _ = nm.supply_record("att-3", "notes.md", "text-element", "/ex/q/notes.md", b"beta\n", b"beta\n", "turn:t/3", "t3",
                             element_text=nm.attachment_input("text-element", "notes.md", "/ex/q/notes.md", b"beta\n")[1])
    check(nm.same_name_distinct([r1, r3]) == {"notes.md": 2}, "A-3 two same-named files with different content stay two attachments")
    r4, d4 = nm.supply_record("att-4", "gone.md", "text-element", "/ex/p/gone.md", b"x", None, "turn:t/4", "t4")
    check(d4.startswith("held") and not validate(r4, att_schema, reg), f"A-4 a file missing at submission: '{d4}'")
    xlsx = b"PK\x03\x04 invented workbook bytes \x00\x01"
    eln, txn = nm.attachment_input("path-named", "beam.xlsx", "/ex/p/beam.xlsx", xlsx)
    rn, dn = nm.supply_record("att-5", "beam.xlsx", "path-named", "/ex/p/beam.xlsx", xlsx, xlsx, "turn:t/5", "t5", element_text=txn)
    ri, di = nm.supply_record("att-6", "crack.png", "localImage", "/ex/p/crack.png", b"\x89PNG", b"\x89PNG", "turn:t/6", "t6")
    check(r1["providerAdoption"] == "not observed" and rn["providerAdoption"] == "not observed"
          and rn["supplyStanding"] == "named; read only if a tool item shows it" and rn["supplierRead"].startswith("not observed")
          and ri["supplyStanding"] == "supplied" and ri["supplierRead"] == "not observed: Codex reads the path itself"
          and dn == "sent (named, not supplied)" and not validate(rn, att_schema, reg) and not validate(ri, att_schema, reg),
          "A-5 per form (R21-2): text element and image 'supplied'; other files 'named; read only if a tool item shows it'; "
          "no record claims provider adoption")
    nm.tool_read(rn, {"threadId": "t", "turnId": "5", "itemId": "item-cmd-1", "observedAt": "t5+40s"})
    check(rn["supplyStanding"].startswith("named") and len(rn["toolReads"]) == 1 and not validate(rn, att_schema, reg),
          "A-6 a tool item that reads a named path is recorded beside it; the record stays 'named' (which bytes were read is not observed)")
    refused = [nm.supply_record("att-x", "f", f, "/ex/f", b"a", b"a", "turn:t/7", "t7")[1] for f in ("mention", "skill")]
    forms = [nm.carrier_for("a.md", b"text\n"), nm.carrier_for("b.png", b"\x89PNG"), nm.carrier_for("c.bin", b"\x00\x01"),
             nm.carrier_for("d.txt", b"x" * (nm.TEXT_BOUND + 1))]
    check(all(r.startswith("refused") for r in refused) and forms == ["text-element", "localImage", "path-named", "path-named"],
          f"A-7 'mention' and 'skill' are never attachment forms (OBS-3 W-3, W-1); carriers chosen by content: {forms}")
    wf = b"---\nname: supports-adjust\n---\n# Adjust supports\n"
    eld, txd = nm.attachment_input("text-element", "WORKFLOW.md (draft supports-adjust)",
                                   ".chirality/workflow-drafts/supports-adjust/WORKFLOW.md", wf)
    rd_, dd = nm.supply_record("att-8", "WORKFLOW.md (draft supports-adjust)", "text-element",
                               ".chirality/workflow-drafts/supports-adjust/WORKFLOW.md", wf, wf, "turn:t/8", "t8", element_text=txd,
                               draft={"location": "project", "name": "supports-adjust",
                                      "content": {"method": "proto-sha256-list-0 (illustration)", "value": "rev-A3"}})
    check(dd == "sent" and not validate(rd_, att_schema, reg) and rd_["draft"]["standing"].startswith("draft — not a registered workflow"),
          "A-8 AT-8 (K-7): a draft's WORKFLOW.md tried in an ordinary conversation is a supplied text element, shown as a draft, never a run")

    # ------------------------------------------------------------------ D drafts
    print("\n== D draft receiving (NIR §7; WR-v0.1 §5.1 events; VER-004) ==")
    dt_schema = reg.by_id[ids["nir.draft-transition"]]
    H = {"method": "m-fx", "value": "c1"}
    H2 = {"method": "m-fx", "value": "c2"}
    key = {"draft_location": "project", "draft_root": ".chirality/workflow-drafts", "name": "w"}

    def T(event, frm, to, **kw):
        t = {"record_kind": "draft_transition", "event": event, "draft": key, "from": frm, "to": to,
             "cause": "invented", "time": "t", "attribution": {"kind": "not observed"}}
        t.update(kw)
        return t
    seq = [T("written", "absent", "draft", content=H), T("review shown", "draft", "under review", content=H),
           T("review stale", "under review", "changed since review"),
           T("review shown", "changed since review", "under review", content=H2),
           T("registered", "under review", "registered, unchanged since", content=H2, disposition="new workflow",
             a15_record="rec:app-interface:0001", revision="project:.chirality/workflows:w@rev-1")]
    dv = nm.DraftView()
    res = [dv.receive(t) for t in seq]
    check(all(r[0] for r in res) and dv.state == "registered, unchanged since"
          and ("review stale", "changed since review") in dv.log,
          f"D-1 WR §5.1 walk; a change during review makes it stale and registration needs the new review: {[x for _, x in dv.log]}")
    check(all(not validate(t, dt_schema, reg) for t in seq), "D-2 every transition of the walk is valid against the receiving schema")
    dv2 = nm.DraftView()
    for t in seq[:2]:
        dv2.receive(t)
    ok1, why1 = dv2.receive(T("registered", "under review", "registered, unchanged since", content=H, disposition="new workflow"))
    ok2, why2 = dv2.receive(T("registered", "under review", "registered, unchanged since", content=H2, disposition="new workflow",
                              a15_record="rec:x", revision="r"))
    check(not ok1 and not ok2, f"D-3 'registered' without the A15 record, or for other content, is refused: '{why1}'; '{why2}'")
    ok3, why3 = dv2.local("mark registered")
    check(not ok3, f"D-4 a local UI action never registers or reviews: '{why3}'")
    dv3 = nm.DraftView()
    dv3.receive(T("written", "absent", "draft", content=H))
    tref = T("registration refused", "draft", "draft", disposition="refused: name taken")
    ok4, st = dv3.receive(tref)
    check(ok4 and st == "draft" and not validate(tref, dt_schema, reg),
          "D-5 'refused: name taken' (K-6) keeps the draft a draft and asks for a new name")
    dv4 = nm.DraftView()
    for t in seq[:2]:
        dv4.receive(t)
    tnc = T("registration not completed", "under review", "draft", a15_record="rec:app-interface:0002")
    ok5, st5 = dv4.receive(tnc)
    check(ok5 and st5 == "draft" and not validate(tnc, dt_schema, reg),
          "D-6 a registration that did not complete returns the draft to 'draft' and cites the recorded act")
    dv5 = nm.DraftView()
    for t in seq[:4]:
        dv5.receive(t)
    bare = T("registered", "under review", "registered, unchanged since", content=H2, disposition="new workflow")
    okb, _ = dv5.receive(bare)
    okl, stl = dv5.receive(bare, library_entry={"a15_record": "rec:app-interface:0001",
                                                "revision": "project:.chirality/workflows:w@rev-1"})
    check(not okb and okl and stl == "registered, unchanged since" and not validate(bare, dt_schema, reg),
          "D-7 C-02 read side: without the A15 record nothing is shown registered; from WR's library_entry it is")

    # ------------------------------------------------------------------ K act control
    print("\n== K App act control (AAC; VER-005 positive case by model only) ==")
    files = {"AF-1": b"result table v1\n", "draft:w@d-2": b"workflow package bytes v1\n"}
    clock = iter(f"2026-10-01T12:{i:02d}:00Z" for i in range(60))
    writers = {}

    def writer_for(run_id):
        key = run_id or "acts"
        if key not in writers:
            path = os.path.join(scratch, key.replace(":", "_").replace("/", "_") + ".jsonl")
            writers[key] = Writer(path, reg, {"role": "App interface (capturing surface)", "identity": "app-interface:local"},
                                  {"surface": "App"}, run_id, fail=fail_hook)
        return writers[key]
    fail_state = {"armed": False}

    def fail_hook(entry):
        if fail_state["armed"]:
            fail_state["armed"] = False
            return True
        return False
    reg_state = {"ok": True}

    def registrar(cap, entry):
        return (True, entry["revision"]) if reg_state["ok"] else (False, "library write failed (invented)")
    current = {"ok": True}
    rs_rel = reg.by_id[ids["RS"]]["$defs"]["humanAct"]["properties"]["relations"]["properties"]
    rs_form = "relations" if "reviewedDraft" in rs_rel else "derivedFrom"
    print(f"     RS_RECORD.schema.json as found: A15 relations form '{rs_form}' "
          f"(sha256 {hashlib.sha256(open(os.path.join(RS_DESIGN, 'RS_RECORD.schema.json'), 'rb').read()).hexdigest()[:16]})")
    ac = ActControl(lambda: dict(person, codexAccount="ChatGPT account (no email reported)"), lambda ref: files.get(ref),
                    registrar, writer_for, lambda: next(clock), descriptor_current=lambda d: current["ok"],
                    rs_a15_form=rs_form)

    def tup(name, rev):
        return {"kind": "workflow", "origin": "project", "sourceRoot": ".chirality/workflows", "name": name,
                "revision": rev, "revisionMethod": "illustration"}

    def descriptor(n, location, prior, name="w"):
        """One WR a15_descriptor (one reviewed draft), in the control's spelling (R21-3)."""
        ident = ac._identity(files[location])
        return {"descriptorId": f"a15d:{name}:{n}", "descriptorKind": "a15_descriptor",
                "entries": [{"subject": f"project:.chirality/workflows:{name}@rev-{n}",
                             "reviewedDraft": {"draft": f"draft:project:{name}@{ident['value'][:16]}", "content": ident},
                             "priorRevision": prior, "location": location}]}

    def multi_descriptor(tag, names):
        """One WR a15_multi_descriptor: library entries reviewed in place (L-4; WR §4.7; R21-3)."""
        ents = []
        for name in names:
            loc = f"entry:{name}"
            ident = ac._identity(files[loc])
            ents.append({"subject": f"workflow revision project:{name}@{ident['value'][:16]}",
                         "reviewedDraft": {"draft": f"entry:project:{name}@{ident['value'][:16]}", "content": ident},
                         "priorRevision": None, "location": loc})
        return {"descriptorId": f"a15m:{tag}", "descriptorKind": "a15_multi_descriptor", "entries": ents}
    offer_schema = reg.by_id[ids["aac.offer"]]
    cap_schema = reg.by_id[ids["aac.capture-evidence"]]
    refused = {k: ac.compose(k, "AF-1", "AF-1", "p")[1] for k in ("A12", "A5", "A13")}
    check(all(v and v.startswith("not offered") for v in refused.values()),
          "K-1 A12, A5 and A13 are not offered by the App act control in this increment, each with its reason")
    o1, _ = ac.compose("A4", "AF-1", "AF-1", "App output checked", arrival={"checkpoint": "CP-out", "arrivalOrdinal": 1},
                       run_id="run:R-300/1", request_ref="rec:app:run-1:0004")
    check(not validate(o1, offer_schema, reg), "K-2 an A4 offer bound to the file's content identity is valid against the offer schema")
    ac.present(o1["offerId"])
    for src in ("agent-tool", "mcp-operation", "app-rule", "supplier-request", "webview-script"):
        st, why = ac.operate(o1["offerId"], src, "act")
        check(st == "AC-R refused" and not ac.captures, f"K-3 operation from {src!r} refused; nothing captured")
    # supplier request outstanding while acting (CAP-9)
    rd3 = nm.RegisterDouble(declared=off)
    rd3.receive("q9", "item/tool/requestUserInput", q, 1)
    st, rec = ac.operate(o1["offerId"], NATIVE_SOURCE, "act")
    cap1 = next(iter(ac.captures.values()))
    check(st == "AC-7 recorded" and not validate(cap1, cap_schema, reg), f"K-4 the person's native confirmation captures A4: {rec}")
    check(rd3.entries["q9"]["state"] == "outstanding", "K-5 acting answered no pending supplier request (CAP-9)")
    st2, why2 = ac.operate(o1["offerId"], NATIVE_SOURCE, "act")
    check(st2 == "AC-R refused" and len(ac.captures) == 1, f"K-5a a second capture from one offer is refused: '{why2}'")
    od, _ = ac.compose("A4", "AF-1", "AF-1", "checked")
    ac.present(od["offerId"])
    std, whyd = ac.operate(od["offerId"], NATIVE_SOURCE, "dismiss")
    check(std == "AC-5 dismissed" and len(ac.captures) == 1, f"K-5b dismissing the control records nothing: '{whyd}'")
    log1 = Reader(reg).read_log(writers["run:R-300/1"].path)
    e = log1["entries"][-1]
    check(e["kind"] == "human_act" and e["body"]["recordingMode"] == "direct capture"
          and e["recorder"]["role"] == "App interface (capturing surface)"
          and e["body"]["relations"]["arrivalAnswered"]["checkpoint"] == "CP-out" and not validate(e, rs_entry, reg),
          "K-6 the RS human_act (direct capture, actor ≠ recorder, arrival and request cited) is valid against RS's schema")
    o2, _ = ac.compose("A6", "AF-1", "AF-1", "engineering approval of the result table")
    ac.present(o2["offerId"])
    st, rec = ac.operate(o2["offerId"], NATIVE_SOURCE, "decline")
    e2 = Reader(reg).read_log(writers["acts"].path)["entries"][-1]
    check(st == "AC-7 recorded" and e2["kind"] == "act_declined" and not validate(e2, rs_entry, reg),
          "K-7 a decline makes an RS act_declined event, valid against RS's schema; it is not an act of that kind")
    o3, _ = ac.compose("A4", "AF-1", "AF-1", "App output checked")
    ac.present(o3["offerId"])
    files["AF-1"] = b"result table v2\n"
    st, why = ac.operate(o3["offerId"], NATIVE_SOURCE, "act")
    check(st == "AC-6 stale", f"K-8 content changed after it was shown: '{why}'")
    # A15 success, failure, decline
    o4, _ = ac.compose("A15", None, "project library .chirality/workflows", "make it available in the project library",
                       descriptor=descriptor(2, "draft:w@d-2", tup("w", "rev-1")))
    _, why0 = ac.compose("A15", "draft:w@d-2", "project library", "make it available in the project library")
    check(why0 and "no A15 descriptor" in why0, f"K-8a an A15 is offered only from the workspace's descriptor: '{why0}'")
    check(not validate(o4, offer_schema, reg) and o4["declineAvailable"] is False and "derivedFrom" not in str(o4)
          and o4["entries"][0]["reviewedDraft"]["draft"].startswith("draft:project:w@")
          and o4["entries"][0]["priorRevision"]["kind"] == "workflow",
          "K-9 an A15 offer from the descriptor: no decline; reviewedDraft (WR ID-3) and priorRevision (RS tuple) (C-01)")
    ac.present(o4["offerId"])
    st, why = ac.operate(o4["offerId"], NATIVE_SOURCE, "decline")
    check(st == "AC-R refused", f"K-10 A15 has no decline: '{why}'")
    st, rec = ac.operate(o4["offerId"], NATIVE_SOURCE, "act")
    capA15 = [c for c in ac.captures.values() if c["actKind"] == "A15"][-1]
    eA15 = Reader(reg).read_log(writers["acts"].path)["entries"][-1]
    check(st == "AC-7 recorded" and eA15["body"]["actKind"] == "A15" and not validate(eA15, rs_entry, reg)
          and not validate(capA15, cap_schema, reg) and capA15["entries"][0]["priorRevision"]["revision"] == "rev-1"
          and capA15["entries"][0]["outcome"] == {"registration": "completed",
                                                   "revisionIdentity": "project:.chirality/workflows:w@rev-2"},
          "K-11 A15: captured and recorded, then registered by the workspace; RS entry and capture evidence valid")
    reg_state["ok"] = False
    files["draft:w@d-3"] = b"workflow package bytes v3\n"
    o5, _ = ac.compose("A15", None, "project library", "make it available in the project library",
                       descriptor=descriptor(3, "draft:w@d-3", None))
    ac.present(o5["offerId"])
    n_before = len(Reader(reg).read_log(writers["acts"].path)["entries"])
    st, why = ac.operate(o5["offerId"], NATIVE_SOURCE, "act")
    capF = [c for c in ac.captures.values() if c["offerId"] == o5["offerId"]][0]
    check(st == "AC-9 recorded; registration not completed"
          and len(Reader(reg).read_log(writers["acts"].path)["entries"]) == n_before + 1
          and not validate(capF, cap_schema, reg),
          f"K-12 the act is recorded; the registration's failure is reported beside it: '{capF['entries'][0]['outcome']['reason']}'")
    files["draft:w@d-5"] = b"workflow package bytes v5\n"
    o9, _ = ac.compose("A15", None, "project library", "make it available in the project library",
                       descriptor=descriptor(5, "draft:w@d-5", tup("w", "rev-2")))
    ac.present(o9["offerId"])
    current["ok"] = False                                # WR RB-3: the slot's latest revision moved on
    st9, why9 = ac.operate(o9["offerId"], NATIVE_SOURCE, "act")
    current["ok"] = True
    check(st9 == "AC-6 stale", f"K-12a the workspace withdrew the descriptor (RB-3): nothing captured: '{why9}'")
    # L-4 (as clarified; R21-3): library entries registered in place, several in one act, from ONE multi descriptor
    reg_state["ok"] = True
    files["entry:notes-a"] = b"workflow notes-a (library entry without a registration record)\n"
    files["entry:notes-b"] = b"workflow notes-b (library entry without a registration record)\n"
    _, whys = ac.compose("A15", None, "project library", "make them available in the project library",
                         descriptor=multi_descriptor("rv-0", ["notes-a"]))
    check(whys is not None and "two or more library entries" in whys,
          f"K-12d an a15_multi_descriptor with one entry is not offered (WR §4.7 ME-1): '{whys}'")
    om, _ = ac.compose("A15", None, "project library", "make them available in the project library",
                       descriptor=multi_descriptor("rv-1", ["notes-a", "notes-b"]))
    ac.present(om["offerId"])
    files["entry:notes-b"] = b"workflow notes-b edited after review\n"
    stm, whym = ac.operate(om["offerId"], NATIVE_SOURCE, "act")
    check(stm == "AC-6 stale" and "notes-b" in whym and "notes-a" not in whym,
          f"K-12b a several-entry A15 is refused whole when one entry changed (WR ME-4): '{whym}'")
    om2, _ = ac.compose("A15", None, "project library", "make them available in the project library",
                        descriptor=multi_descriptor("rv-2", ["notes-a", "notes-b"]))
    ac.present(om2["offerId"])
    stm2, recm = ac.operate(om2["offerId"], NATIVE_SOURCE, "act")
    capM = [c for c in ac.captures.values() if c["offerId"] == om2["offerId"]][0]
    eM = Reader(reg).read_log(writers["acts"].path)["entries"][-1]
    check(stm2 == "AC-7 recorded" and om2["wording"] == "register workflow revisions" and om2["descriptorId"] == "a15m:rv-2"
          and len(capM["entries"]) == 2 and len(eM["body"]["boundSubject"]) == 2
          and all(x["reviewedDraft"]["draft"].startswith("entry:project:") for x in eM["body"]["relations"]["registeredEntries"])
          and not validate(capM, cap_schema, reg) and not validate(eM, rs_entry, reg)
          and not validate(om2, offer_schema, reg),
          "K-12c L-4: one multi descriptor, one A15 act over two library entries in place ('entry:'; plural wording): "
          "one capture, one RS record naming both, each entry's outcome beside it")
    # write failure and late write
    reg_state["ok"] = True
    files["AF-2"] = b"another output\n"
    o6, _ = ac.compose("A7", "AF-2", "AF-2", "relied on for the design check")
    ac.present(o6["offerId"])
    fail_state["armed"] = True
    st, why = ac.operate(o6["offerId"], NATIVE_SOURCE, "act")
    check(st == "AC-8 record pending", "K-13 a record write failure keeps the capture and reports it")
    files["AF-3"] = b"third output\n"
    o7, _ = ac.compose("A4", "AF-3", "AF-3", "checked")
    ac.present(o7["offerId"])
    ac.operate(o7["offerId"], NATIVE_SOURCE, "act")
    tail = [(x["kind"], x["body"].get("label", x["body"].get("actKind"))) for x in
            Reader(reg).read_log(writers["acts"].path)["entries"][-3:]]
    check(tail == [("human_act", "A7"), ("human_act", "A4"), ("evidence_limit", "record write failed")]
          and ac.states[o6["offerId"]] == "AC-7 recorded",
          f"K-14 the pending A7 is written late, in order, then 'record write failed' (RS FC-1): {tail}")
    # recovery after a crash between registration and record
    files["draft:w@d-4"] = b"workflow package bytes v4\n"
    o8, _ = ac.compose("A15", None, "project library", "make it available in the project library",
                       descriptor=descriptor(4, "draft:w@d-4", tup("w", "rev-2")))
    ac.present(o8["offerId"])
    real_record = ac._record
    ac._record = lambda cap: ("crashed", None)          # the App ends after the capture, before the record is written
    ac.operate(o8["offerId"], NATIVE_SOURCE, "act")
    ac._record = real_record
    present = {x["recordId"] for w in writers.values() for x in Reader(reg).read_log(w.path)["entries"]}
    rec_done = ac.recover(present)
    check(len(rec_done) == 1 and rec_done[0][0] == "AC-7 recorded",
          "K-15 relaunch: a capture whose record was never written gets its record, late (AC-R1)")
    # R21-3 cross-check: DEL-02-02's own descriptors (WR-v0.2's valid examples) through this control's offer and
    # capture into RS's writer; then RS's L-4 act-log example (record 4) against this control's capture format.
    wd_schema = load(os.path.join(WD_DESIGN, "workflow-declaration.schema.json"))
    reg.add(wd_schema)                       # WD uses keywords outside the subset (WR's prototype does the same)
    wr_id = reg.load(os.path.join(WR_DESIGN, "workspace-registration.schema.json"))
    wr_lines = [json.loads(x) for x in open(os.path.join(WR_DESIGN, "workspace-registration.valid.examples.jsonl"),
                                            encoding="utf-8") if x.strip()]
    wr_desc = {d["record_kind"]: d for d in wr_lines if d.get("record_kind") in ("a15_descriptor", "a15_multi_descriptor")}
    wr_ok = all(not validate(d, {"$ref": wr_id + "#/$defs/" + k}, reg) for k, d in wr_desc.items())
    live = {}                                # stub: each location's live identity is WR's own example value
    acx = ActControl(lambda: dict(person, codexAccount="enga@example.invalid"), lambda ref: live.get(ref),
                     registrar, writer_for, lambda: next(clock), descriptor_current=lambda d: True, rs_a15_form=rs_form)
    acx._identity = lambda data: {"method": "proto-sha256-list-0", "value": data.decode("utf-8")}
    xres = {}
    for k, wr in sorted(wr_desc.items()):
        values = ([wr["relations"]["reviewed_draft"]["content"]["value"]] if k == "a15_descriptor"
                  else [e["bound_content"]["value"] for e in wr["entries"]])
        locs = [f"wr:{k}:{i}" for i in range(len(values))]
        for loc, v in zip(locs, values):
            live[loc] = v.encode("utf-8")
        d = from_wr_descriptor(wr, locs)
        ox, whyx = acx.compose("A15", None, d["scope"], d["purpose"], descriptor=d)
        if ox is None:
            xres[k] = whyx
            continue
        acx.present(ox["offerId"])
        stx, _ = acx.operate(ox["offerId"], NATIVE_SOURCE, "act")
        capx = [c for c in acx.captures.values() if c["offerId"] == ox["offerId"]][0]
        ex = Reader(reg).read_log(writers["acts"].path)["entries"][-1]
        rel = ex["body"]["relations"]
        if k == "a15_descriptor":
            dk = wr["relations"]["reviewed_draft"]["draft"]
            same = (rel["reviewedDraft"]["draft"] == f"draft:{dk['draft_location']}:{dk['name']}@{values[0]}"
                    and rel["priorRevision"]["revision"] == wr["relations"]["prior_revision"]["revision"]
                    and rel["priorRevision"]["sourceRoot"] == wr["relations"]["prior_revision"]["source_root"])
        else:
            same = ([x["reviewedDraft"]["draft"] for x in rel["registeredEntries"]] == [e["reviewed_entry"] for e in wr["entries"]]
                    and all(x["priorRevision"] is None for x in rel["registeredEntries"]))
        xres[k] = (stx == "AC-7 recorded" and ox["wording"] == wr["wording"] and ox["descriptorId"] == wr["descriptor_id"]
                   and ox["purpose"] == wr["purpose"] and not validate(ox, offer_schema, reg)
                   and not validate(capx, cap_schema, reg) and not validate(ex, rs_entry, reg) and same)
    check(wr_ok and xres == {"a15_descriptor": True, "a15_multi_descriptor": True},
          "K-17 R21-3 cross-check: WR-v0.2's own a15_descriptor and a15_multi_descriptor examples (valid against WR's schema) "
          "pass through this control's offer and capture into RS's writer; offer, capture and RS entry valid; "
          f"wording, descriptor, purpose and reviewed content carried unchanged {xres}")
    rs4 = [json.loads(x) for x in open(os.path.join(RS_DESIGN, "RS_RECORD.valid.act-log.example.jsonl"), encoding="utf-8")
           if x.strip()][3]
    b4 = rs4["body"]
    cap4 = {"format": "chirality.aac.capture-evidence", "formatVersion": "0.3", "captureId": b4["captureEvidence"][0]["ref"],
            "offerId": "offer:rs-act-log-4", "offerDigest": {"method": "illustration", "value": "rs-act-log-4"},
            "choice": "act", "actKind": "A15", "actor": b4["decisionActor"], "boundSubject": b4["boundSubject"],
            "boundContent": b4["boundContent"], "scope": b4["scope"], "purpose": b4["purpose"],
            "capturedAt": b4["captureTime"], "surface": "App interface", "inputSource": "host-native-confirmation",
            "answers": {"standing": "no arrival: a standing act (RC-6)"}, "descriptorId": "a15m:rs-act-log-4",
            "descriptorKind": "a15_multi_descriptor",
            "entries": [{"revision": x["subject"], "reviewedDraft": x["reviewedDraft"], "priorRevision": x["priorRevision"]}
                        for x in b4["relations"]["registeredEntries"]],
            "recordId": rs4["recordId"], "evidenceLimits": b4["evidenceLimits"]}
    _, kind4, body4 = acx._entry(cap4)
    check(not validate(cap4, cap_schema, reg) and kind4 == "human_act" and body4["relations"] == b4["relations"]
          and body4["boundSubject"] == b4["boundSubject"] and body4["boundContent"] == b4["boundContent"]
          and body4["decisionActor"] == b4["decisionActor"] and body4["captureEvidence"][0]["ref"] == "cap:reg-in-place-2",
          "K-17b RS's L-4 act-log example (record 4: 'entry:' strings, capture cap:reg-in-place-2) has capture evidence this "
          "control's format accepts, and this control writes the same relations, subjects, content and actor from it")
    allent = Reader(reg).read_log(writers["acts"].path)["entries"] + log1["entries"]
    bad = [x["recordId"] for x in allent if validate(x, rs_entry, reg)]
    check(not bad, f"K-16 all {len(allent)} RS entries the act control wrote are valid against RS_RECORD.schema.json {bad}")

    print(f"\n{COUNT[0]} checks, {len(FAIL)} failed. Scratch logs under $TMPDIR (d3-del-01-04-*)")
    return 1 if FAIL else 0


if __name__ == "__main__":
    sys.exit(main())
