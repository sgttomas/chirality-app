#!/usr/bin/env python3
"""Runs DEL-01-02's designed cases against the recovery model and the
supplier stub (EXECUTION_AND_RECOVERY.md §11; RECOVERY-v0.2).

Prototype only (run APP-V4-DESIGN-PASS-3-20261001, node D1, rounds 1 and 2). Python 3
standard library only; no network; Codex is never started. Exit status 0 when
every result is as expected. "pass (model)" means the design's rules ran as
written against the stub, under every stub variant the case lists; it is never
a VER pass (no App candidate exists) and says nothing about which variant the
supplier really shows (OBS-2 pending).

The JSON Schema validator is DEL-01-01's `jsonschema_subset.py`, imported
read-only from that deliverable's prototype folder (DEL-01-02 consumes
DEL-01-01: DEP-01-02-018, admitted).
"""
import itertools
import json
import os
import re
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
DESIGN = os.path.dirname(HERE)
PKG = os.path.dirname(os.path.dirname(DESIGN))
HOSTING_PROTO = os.path.join(PKG, "DEL-01-01_Stock Codex hosting and supplier contract", "Design", "prototype")
sys.path.insert(0, HERE)
sys.path.insert(1, HOSTING_PROTO)

import jsonschema_subset as V  # noqa: E402
import recovery_model as M  # noqa: E402
from supplier_stub import CONTENT_MARKER, VARIANTS, Store  # noqa: E402

SCHEMAS = {}
for name in ("stop-request", "custody-event", "app-ledger-entry"):
    with open(os.path.join(DESIGN, "recovery.%s.schema.json" % name)) as f:
        SCHEMAS[name] = json.load(f)

RESULTS = []
TRACE_ALL = set()


def result(case, ok, detail):
    RESULTS.append((case, ok, detail))
    print("%-6s %-5s %s" % (case, "PASS" if ok else "FAIL", detail))


def new_world(variant=None):
    tmp = tempfile.mkdtemp(prefix="del0102-")
    return Store(), os.path.join(tmp, "ledger.jsonl"), variant or {}


def check_records(app):
    """Every emitted custody event, stop record and ledger entry is valid."""
    errs = []
    for ev in app.events:
        errs += ["event %s: %s" % (ev["kind"], e) for e in V.errors(ev, SCHEMAS["custody-event"])]
    for le in app.ledger_written:
        errs += ["ledger %s: %s" % (le["kind"], e) for e in V.errors(le, SCHEMAS["app-ledger-entry"])]
        if le["kind"] == "stop_request":
            errs += ["stop %s: %s" % (le["record"]["state"], e) for e in V.errors(le["record"], SCHEMAS["stop-request"])]
    TRACE_ALL.update(t for t, _ in app.trace)
    return errs


def live_turn_world(variant, with_request=True, with_child=False):
    store, ledger, v = new_world(variant)
    app = M.AppSession(store, ledger, 1, v)
    app.start_supplier()
    tid = app.new_conversation()
    app.send_message(tid)
    turn = app.convs[tid]["liveTurn"]
    rid = None
    if with_request:
        item = app.supplier().add_item(tid, turn, "commandExecution")
        rid = app.supplier().raise_request(tid, turn, item, "item/commandExecution/requestApproval")
    if with_child:
        app.supplier().spawn_child(tid)
    return store, ledger, v, app, tid, turn, rid


# ---- C-01 observer loss (VER-001) ---------------------------------------
def c01():
    _, _, _, app, tid, turn, rid = live_turn_world({})
    ob = app.attach("window-1")
    pos = ob["position"]
    writes_before = len(app.supplier().writes)
    sent = app.detach("window-1")
    app.supplier().add_item(tid, turn, "agentMessage", text="%s more" % CONTENT_MARKER, complete=True)
    ob = app.attach("window-1", position=pos, rendered={tid: {"state": "loaded-idle", "liveTurn": None}})
    replayed = [p for g, p in ob["received"] if g != "custody"]
    no_dup = len(replayed) == len(set(replayed))
    contiguous = replayed == list(range(replayed[0], replayed[-1] + 1)) if replayed else False
    app.hide("window-1")
    stale_overwritten = ob["rendered"][tid]["state"] == "turn-live" and ob["rendered"][tid]["outstanding"] == [rid]
    ok = (sent == 0 and len(app.supplier().writes) == writes_before and app.list_outstanding()[0]["requestIdentity"] == rid
          and app.convs[tid]["state"] == "turn-live" and no_dup and contiguous and stale_overwritten
          and ob["gap"] is None)
    # beyond the journal: rebuilt from supplier, gap marked
    app.detach("window-1")
    for _ in range(M.JOURNAL_RETENTION + 5):
        app.supplier().add_item(tid, turn, "reasoning", complete=True)
    ob2 = app.attach("window-1", position=pos)
    ok = ok and ob2["gap"] is not None
    errs = check_records(app)
    result("C-01", ok and not errs, "observer loss: 0 frames sent on close/reload; request %s still outstanding; "
           "replay from position without gap or duplicate; hide changes nothing; stale render replaced; "
           "position outside journal → rebuilt with gap marker%s" % (rid, "; " + "; ".join(errs[:3]) if errs else ""))


# ---- C-02 person interrupt under every interrupt variant (VER-002) ------
def c02():
    rows, all_ok = [], True
    for mode, pend, child in itertools.product(VARIANTS["interrupt"], VARIANTS["pending_on_interrupt"],
                                               VARIANTS["child_after_interrupt"]):
        _, _, _, app, tid, turn, rid = live_turn_world(
            {"interrupt": mode, "pending_on_interrupt": pend, "child_after_interrupt": child}, with_child=True)
        sid = app.interrupt(tid)
        again = app.interrupt(tid)
        s = app.stops[sid]
        if mode == "interrupted":
            ok = s["state"] == "settled" and s["turnOutcome"] == "interrupted" and s["outcomeLabel"] == "interrupted by the person"
            # G-4: the command item opened in the turn never completed; settled at turn end
            ok = ok and any(i["itemType"] == "commandExecution" for i in s.get("itemsNotCompleted", []))
            # a child observed active when the parent's turn ended is reported; whether it then stops is O-4
            ok = ok and bool(s["descendantsActiveAtOutcome"]) and (bool(app._active_children(tid)) == (child == "survives"))
            entry = app.register[rid]
            ok = ok and ((entry["state"] == "closed" and entry["endedAs"] == "resolved-by-supplier")
                         if pend == "resolved-by-supplier" else entry["state"] == "listed")
            ok = ok and again == "refused: no-live-turn"
        elif mode == "completes-first":
            ok = s["state"] == "settled" and s["turnOutcome"] == "completed" and s["outcomeLabel"] == "completed (stop requested)" \
                and "SR-12" in [t for t, _ in app.trace] and s.get("itemsCompletedAfterRequest")
        elif mode == "no-response":
            ok = s["state"] == "sent" and again == "refused: stop-already-requested" and app.convs[tid]["state"] == "interrupt-pending"
            app.end_wait(sid)
            app.supplier_exits()
            ok = ok and s["state"] == "outcome-unknown" and s["outcomeLabel"] == "outcome unknown (stop requested)"
        else:  # error
            ok = s["state"] == "refused" and app.convs[tid]["state"] == "turn-live" and app.told[-1].startswith("stop refused")
            app.supplier().finish_turn(tid, turn, "completed")
            ok = ok and s["state"] == "settled" and s["turnOutcome"] == "completed"
        # no stop request comes from observer loss, and no run end is ever produced
        ok = ok and not any(e["kind"] not in SCHEMAS["custody-event"]["$defs"] for e in app.events)
        errs = check_records(app)
        all_ok = all_ok and ok and not errs
        rows.append("%s/%s/%s:%s" % (mode, pend, child, "ok" if ok and not errs else "FAIL " + "; ".join(errs[:2])))
    # write failure: the process died, exit not yet observed
    _, _, _, app, tid, turn, rid = live_turn_world({})
    app.supplier().alive = False
    r = app.interrupt(tid)
    s = list(app.stops.values())[-1]
    wf = r == "not-sent" and s["state"] == "not-sent" and s["send"] == "not-sent(write-failed)" and app.convs[tid]["state"] == "turn-live"
    errs = check_records(app)
    all_ok = all_ok and wf and not errs
    result("C-02", all_ok, "interrupt across %d variant combinations (%s); write failure → not-sent, turn stays as observed (%s)"
           % (len(rows), ", ".join(rows), "ok" if wf else "FAIL"))


# ---- C-03 requests: grant, deny, answer, decline, silence (VER-003) -----
def c03():
    store, ledger, v = new_world({})
    app = M.AppSession(store, ledger, 1, v)
    app.start_supplier()
    tid = app.new_conversation()
    app.send_message(tid)
    turn = app.convs[tid]["liveTurn"]
    sup = app.supplier()
    r_grant = sup.raise_request(tid, turn, sup.add_item(tid, turn, "commandExecution"), "item/commandExecution/requestApproval")
    r_deny = sup.raise_request(tid, turn, sup.add_item(tid, turn, "fileChange"), "item/fileChange/requestApproval")
    r_input = sup.raise_request(tid, turn, sup.add_item(tid, turn, "dynamicToolCall"), "item/tool/requestUserInput")
    r_decl = sup.raise_request(tid, turn, sup.add_item(tid, turn, "mcpToolCall"), "mcpServer/elicitation/request")
    r_quiet = sup.raise_request(tid, turn, sup.add_item(tid, turn, "commandExecution"), "item/commandExecution/requestApproval")
    app.attach("w")
    app.detach("w")                                   # observer lost while all are outstanding
    still = sorted(e["requestIdentity"] for e in app.list_outstanding())
    a1 = app.answer(r_grant, "accept")
    a2 = app.answer(r_deny, "decline")
    a3 = app.answer(r_input, "answer-content")
    a4 = app.answer(r_decl, "decline", origin="app-rule:example-decline")
    a5 = app.answer(r_quiet, "accept", origin="app-rule:example")          # App-rule affirmative refused
    a6 = app.answer(r_grant, "accept")                                      # second answer
    for _ in range(50):                                                     # silence: time passes, nothing answers
        app.clock.now()
    quiet = app.register[r_quiet]
    ok = (len(still) == 5 and a1 == a2 == a3 == a4 == "accepted-for-write" and a5 == "refused: origin-not-permitted"
          and a6 == "refused: already-settled" and quiet["state"] == "listed"
          and app.register[r_grant]["ack"] == "observed" and app.register[r_deny]["endedAs"] == "declined"
          and app.register[r_decl]["origin"] == "app-rule:example-decline")
    # the person interrupts; the silent request ends only by the supplier or the generation, never by the App
    app.supplier_exits()
    ok = ok and quiet["endedAs"] == "ended-unanswered(process-exit)" and app.answer(r_quiet, "accept") == "refused: generation-closed"
    errs = check_records(app)
    result("C-03", ok and not errs, "grant, deny, user-input answer, App-rule decline recorded with true origins; App-rule "
           "affirmative refused; silence answers nothing; outstanding survives observer loss; exit → ended unanswered, "
           "answer refused generation-closed%s" % ("; " + "; ".join(errs[:3]) if errs else ""))


# ---- C-04 unknown request and lost acknowledgment (VER-004) -------------
def c04():
    store, ledger, v = new_world({})
    app = M.AppSession(store, ledger, 1, v)
    app.start_supplier()
    tid = app.new_conversation()
    app.send_message(tid)
    turn = app.convs[tid]["liveTurn"]
    unk = app.supplier().raise_unknown_request()
    e_unk = app.register[unk]
    errored_frame = [w for w in app.supplier().writes if w.get("id") == unk and "error" in w]
    # a written answer whose acknowledgment never arrives: the stub's reply handler is bypassed
    rid = app.supplier().raise_request(tid, turn, app.supplier().add_item(tid, turn, "commandExecution"),
                                     "item/commandExecution/requestApproval")
    app.supplier()._on_reply = lambda frame: None
    app.answer(rid, "accept")
    app.supplier_exits()
    lost = [e for e in app.events if e["kind"] == "acknowledgment_not_observed"]
    ok = (e_unk["endedAs"] == "errored" and e_unk["origin"] == "app-explicit-error" and len(errored_frame) == 1
          and ("RQ-08", unk) in app.trace and len(lost) == 1 and app.register[rid]["ack"] == "not-observed"
          and app.register[rid]["endedAs"] == "answered")
    errs = check_records(app)
    result("C-04", ok and not errs, "unknown request: explicit error written at receipt (DEL-01-01 path), summary RQ-08; "
           "written answer with no acknowledgment → acknowledgment_not_observed at generation close, never 'received'%s"
           % ("; " + "; ".join(errs[:3]) if errs else ""))


# ---- C-05 unexpected supplier exit and recovery (VER-005) ---------------
def c05():
    rows, all_ok = [], True
    for persisted in VARIANTS["persisted_after_exit"]:
        store, ledger, v, app, tid, turn, rid = live_turn_world({"persisted_after_exit": persisted})
        inflight = app.supplier().add_item(tid, turn, "mcpToolCall")
        stale = {tid: {"state": "loaded-idle", "liveTurn": None, "outstanding": []}}   # a stale render: "done"
        app.attach("w", rendered=stale)
        app.supplier_exits()
        lost = [e for e in app.events if e["kind"] == "observation_lost"][-1]
        app.start_supplier()                                         # HOSTING restart → ready(g2)
        rec = [e for e in app.events if e["kind"] == "observation_recovered"][-1]
        out = [e for e in app.events if e["kind"] == "turn_outcome"][-1]
        exp = {"interrupted": ("interrupted", "recovered-from-supplier"), "inProgress": ("unknown", "not-observed"),
               "missing-turn": ("unknown", "not-observed")}[persisted]
        ok = (any(i["itemId"] == inflight for i in lost["inFlightItems"]) and lost["liveTurns"][0]["turnId"] == turn
              and (out["outcome"], out["source"]) == exp and app.convs[tid]["state"] == "indexed"
              and app.register[rid]["endedAs"] == "ended-unanswered(process-exit)"
              and not [w for w in app.supplier().writes if w.get("method") == "turn/start"])   # no prompt re-sent
        ob = app.attach("w2", rendered=stale)
        ok = ok and ob["rendered"][tid]["state"] == "indexed" and ob["gap"] is not None
        errs = check_records(app)
        all_ok = all_ok and ok and not errs
        rows.append("%s→%s/%s%s" % (persisted, out["outcome"], out["source"], "" if ok and not errs else " FAIL " + "; ".join(errs[:2])))
    # a read that fails, a retry, and a second exit during recovery
    store, ledger, v, app, tid, turn, rid = live_turn_world({})
    app.supplier_exits()
    saved = store.threads.pop(tid)
    app.start_supplier()
    unavailable = app.convs[tid]["state"] == "unavailable"
    store.threads[tid] = saved
    app.retry(tid)
    retried = app.convs[tid]["state"] == "indexed"
    app.resume(tid)
    app.send_message(tid)
    app.hang_reads = True
    app.supplier_exits()
    app.start_supplier()                     # reads in flight (no response)
    recovering = app.convs[tid]["state"] == "recovering"
    app.supplier_exits()                     # closes during recovery → CV-22
    pending = app.convs[tid]["state"] == "recovery-pending"
    app.hang_reads = False
    app.start_supplier()
    done = app.convs[tid]["state"] == "indexed"
    # a system error status and a thread closed by the supplier
    app.resume(tid)
    app.supplier().report_system_error(tid)
    se = app.convs[tid]["state"] == "system-error"
    app.supplier().report_idle(tid)
    app.supplier().close_thread(tid)
    closed = app.convs[tid]["state"] == "indexed"
    app.crash()
    app_b = M.AppSession(store, ledger, 2, {})
    closed = closed and app_b.convs[tid]["state"] == "indexed" and ("CV-20", tid) in app_b.trace
    errs = check_records(app) + check_records(app_b)
    extra = unavailable and retried and recovering and pending and done and se and closed
    all_ok = all_ok and extra and not errs
    result("C-05", all_ok, "exit with live turn, outstanding request, in-flight item; restart; recovery read per O-2 variant "
           "(%s); stale render replaced; no prompt re-sent; read failure → unavailable → retry; exit during recovery → "
           "recovery-pending → recovered; system error and thread/closed (%s)" % (", ".join(rows), "ok" if extra else "FAIL"))


# ---- C-06 quit with live work (K-4) and relaunch (VER-006) --------------
def c06():
    rows, all_ok = [], True
    for mode, reraise in itertools.product(["interrupted", "no-response", "completes-first"], VARIANTS["reraise_on_resume"]):
        store, ledger, v, app, tid, turn, rid = live_turn_world({"interrupt": mode, "pending_on_interrupt": "stays-pending",
                                                                 "reraise_on_resume": reraise})
        ask = app.request_quit()
        app.cancel_quit()
        still_running = app.as_state == "running" and app.convs[tid]["state"] == "turn-live"
        ask2 = app.request_quit()
        app.live_work_changed()
        app.confirm_quit()
        s = [x for x in app.stops.values() if x["cause"] == "quit"][0]
        exp_label = {"interrupted": "interrupted by quit", "no-response": "interrupted by quit (final status not observed)",
                     "completes-first": "completed (quit requested)"}[mode]
        ok = ask["ask"] and ask2["ask"] and still_running and app.as_state == "ended" and s["outcomeLabel"] == exp_label \
            and app.register[rid]["endedAs"] in ("ended-unanswered(process-exit)", "resolved-by-supplier")
        errs = check_records(app)
        # relaunch
        app2 = M.AppSession(store, ledger, 2, v)
        restart = [e for e in app2.events if e["kind"] == "app_restart_interruption"]
        reading_ok = app2.prev_reading == "quit-with-live-work"
        app2.start_supplier()
        conv = app2.convs[tid]
        recovered = [e for e in app2.events if e["kind"] == "observation_recovered"]
        ok = ok and reading_ok and conv["state"] == "indexed" and recovered and recovered[-1]["priorEvents"] == "accessible"
        if mode != "completes-first":
            ok = ok and len(restart) == 1
        # nothing is resumed until the person chooses; then no prompt is re-sent
        auto = [w for w in app2.supplier().writes if w.get("method") in ("thread/resume", "turn/start")]
        r = app2.resume(tid)
        old_answer = app2.answer(rid, "accept")
        reraised = [e for e in app2.register.values() if e["state"] == "listed"]
        ok = ok and not auto and r == "resumed" and old_answer == "refused: no-such-request"
        if mode == "no-response":     # G-5: the turn was live when the quit closed Codex's input
            ok = ok and any(t.get("historyNote") for t in recovered[-1]["turns"])
        if reraise and mode == "no-response":
            ok = ok and len(reraised) == 1 and reraised[0].get("sameItemAs") and ("RQ-07", reraised[0]["requestIdentity"]) in app2.trace
        elif not reraise:
            ok = ok and not reraised
        app2.send_message(tid)
        ok = ok and app2.convs[tid]["state"] == "turn-live"
        errs += check_records(app2)
        all_ok = all_ok and ok and not errs
        rows.append("%s/reraise=%s:%s" % (mode, reraise, "ok" if ok and not errs else "FAIL " + "; ".join(errs[:2])))
    # quit with no live work: no question
    store, ledger, v = new_world({})
    app = M.AppSession(store, ledger, 1, v)
    app.start_supplier()
    app.new_conversation()
    q = app.request_quit()
    quiet = (not q["ask"]) and app.as_state == "ended"
    app2 = M.AppSession(store, ledger, 2, v)
    quiet = quiet and app2.prev_reading == "clean" and not [e for e in app2.events if e["kind"] == "app_restart_interruption"]
    # system termination during the question
    _, ledger3, _, app3, tid3, _, _ = live_turn_world({})
    app3.request_quit()
    app3.system_termination()
    app4 = M.AppSession(app3.stores, ledger3, 2, {})
    sysok = app4.prev_reading == "system-terminated"
    errs = check_records(app) + check_records(app2) + check_records(app3) + check_records(app4)
    all_ok = all_ok and quiet and sysok and not errs
    result("C-06", all_ok, "quit asks with live work, cancel keeps running, confirm interrupts and stops; labels per O-1 "
           "variant; relaunch reads 'quit-with-live-work', recovers from Codex, resumes only on the person's choice, "
           "no prompt re-sent, old request never answered; re-raised request is a new entry with 'same item reference' "
           "(%s); quit without live work asks nothing; system termination read at relaunch (%s)"
           % (", ".join(rows), "ok" if quiet and sysok else "FAIL"))


# ---- C-07 App ended without a record (crash) (VER-006) ------------------
def c07():
    rows, all_ok = [], True
    for persisted in VARIANTS["persisted_after_exit"]:
        store, ledger, v, app, tid, turn, rid = live_turn_world({"persisted_after_exit": persisted, "interrupt": "no-response"})
        sid = app.interrupt(tid)               # the person had asked to stop; no answer yet
        app.crash()
        app2 = M.AppSession(store, ledger, 2, v)
        reading = app2.prev_reading
        ended = [e for e in app2.events if e["kind"] == "request_ended_unanswered" and e["context"] == "app-ended-without-record"]
        app2.start_supplier()
        s = app2.stops[sid]
        out = [e for e in app2.events if e["kind"] == "turn_outcome"][-1]
        exp_state = "outcome-recovered" if persisted == "interrupted" else "outcome-unknown"
        ok = (reading == "ended-without-record" and len(ended) == 1 and s["state"] == exp_state
              and out["cause"] == "person-interrupt" and ("RQ-06", (M.generation_ref("sess-1", "H-acct", 1), rid)) in app2.trace)
        errs = check_records(app) + check_records(app2)
        all_ok = all_ok and ok and not errs
        rows.append("%s→%s%s" % (persisted, s["state"], "" if ok and not errs else " FAIL " + "; ".join(errs[:2])))
    result("C-07", all_ok, "App killed with a live turn, a pending stop and an outstanding request: relaunch reads "
           "'ended without a record', ends the request unanswered (RQ-06), closes the stop (SR-08) and recovers it from "
           "Codex where Codex reports a final status (%s)" % ", ".join(rows))


# ---- C-08 the handoff makes no stronger claim (VER-007) -----------------
def c08():
    negatives = {
        "human act kind": {"kind": "human_act", "eventId": "cev:x:1", "appSession": "x", "at": "t", "standing": "App-observed"},
        "observer loss as observation loss": json.load(open(os.path.join(DESIGN, "recovery.custody-event.example.invalid.json"))),
        "outcome claimed without observation": {"kind": "turn_outcome", "eventId": "cev:x:2", "appSession": "x", "at": "t",
                                                "standing": "App-observed", "threadId": "a", "turnId": "b",
                                                "outcome": "interrupted", "source": "not-observed"},
        "authority claimed": {"kind": "turn_outcome", "eventId": "cev:x:3", "appSession": "x", "at": "t",
                              "standing": "authoritative", "threadId": "a", "turnId": "b", "outcome": "completed", "source": "observed"},
        "run end from an interrupt": {"kind": "run_ended", "eventId": "cev:x:4", "appSession": "x", "at": "t", "standing": "App-observed"},
        "cancel-answer claimed with a stop request": {"kind": "turn_outcome", "eventId": "cev:x:5", "appSession": "x", "at": "t",
                                                      "standing": "App-observed", "threadId": "a", "turnId": "b",
                                                      "outcome": "interrupted", "source": "observed", "cause": "cancel-answer",
                                                      "causeRequest": "sr-1", "stopRequest": "stop:x:1"},
    }
    stop_neg = {
        "identity verified": dict(json.load(open(os.path.join(DESIGN, "recovery.stop-request.example.valid.json"))),
                                  requestedBy={"kind": "person", "identity": "p", "identityStatus": "verified"}),
        "settled from an unobserved outcome": json.load(open(os.path.join(DESIGN, "recovery.stop-request.example.invalid.json"))),
        "cause observer loss": dict(json.load(open(os.path.join(DESIGN, "recovery.stop-request.example.valid.json"))),
                                    cause="window-closed"),
    }
    bad = [k for k, inst in negatives.items() if not V.errors(inst, SCHEMAS["custody-event"])]
    bad += [k for k, inst in stop_neg.items() if not V.errors(inst, SCHEMAS["stop-request"])]
    # an actual person's answer stays recorded with its origin; the recorder is not the actor
    _, _, _, app, tid, turn, rid = live_turn_world({})
    app.answer(rid, "accept")
    summ = [le for le in app.ledger_written if le["kind"] == "register_entry_summary" and le["requestIdentity"] == rid][-1]
    ok = not bad and summ["origin"] == "person-via-interaction" and "actor" not in summ
    kinds = {e["kind"] for e in app.events}
    ok = ok and not (kinds & {"human_act", "run_ended", "approval"})
    errs = check_records(app)
    result("C-08", ok and not errs, "%d constructed stronger claims refused by the schemas (%s); the person's answer keeps "
           "origin person-via-interaction (actor supplied by DEL-01-04 to DEL-01-01, not copied here); no human-act, run-end or "
           "approval kind exists%s" % (len(negatives) + len(stop_neg), ", ".join(sorted(list(negatives) + list(stop_neg))),
                                       "; NOT REFUSED: " + ", ".join(bad) if bad else ""))


# ---- C-09 schemas and examples -------------------------------------------
def c09():
    out, ok = [], True
    for name in SCHEMAS:
        for kind, expect_valid in (("valid", True), ("invalid", False)):
            with open(os.path.join(DESIGN, "recovery.%s.example.%s.json" % (name, kind))) as f:
                inst = json.load(f)
            errs = V.errors(inst, SCHEMAS[name])
            good = (not errs) == expect_valid
            ok = ok and good
            out.append("%s.%s:%s" % (name, kind, ("valid" if not errs else "invalid (" + errs[0] + ")")))
    result("C-09", ok, "; ".join(out))


# ---- C-10 the Design file's tables equal the model's ----------------------
def c10():
    path = os.path.join(DESIGN, "EXECUTION_AND_RECOVERY.md")
    if not os.path.exists(path):
        result("C-10", False, "Design file not found")
        return
    rows = {}
    for line in open(path, encoding="utf-8"):
        m = re.match(r"^\|\s*((AS|CV|OA|SR|RQ)-\d\d)\s*\|", line)
        if m:
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            froms = tuple(x.strip().strip("`") for x in cells[1].split(","))
            rows[cells[0]] = (froms, cells[2].strip("`"), cells[4].strip("`"))
    diffs = []
    for prefix, table in M.TABLES.items():
        for tid, (froms, ev, to) in table.items():
            got = rows.get(tid)
            if got is None:
                diffs.append(tid + " missing in file")
            elif set(got[0]) != set(froms) or got[1] != ev or got[2] != to:
                diffs.append("%s file %r model %r" % (tid, got, (froms, ev, to)))
    extra = [t for t in rows if t[:2] in M.TABLES and t not in M.TABLES[t[:2]]]
    diffs += [t + " in file only" for t in extra]
    n = sum(len(t) for t in M.TABLES.values())
    result("C-10", not diffs, "%d rows in five tables compared with the model%s" % (n, "; " + "; ".join(diffs) if diffs else ": equal"))


# ---- C-11 the ledger keeps no conversation content (R17-4) --------------
def c11():
    store, ledger, v, app, tid, turn, rid = live_turn_world({})
    app.answer(rid, "accept")
    app.request_quit()
    app.confirm_quit()
    text = open(ledger, encoding="utf-8").read()
    in_store = CONTENT_MARKER in json.dumps(store.threads)
    ok = CONTENT_MARKER not in text and in_store
    result("C-11", ok, "ledger of %d entries holds no message, command or request payload text (marker absent); "
           "content stays in Codex's history (marker present there: %s)" % (len(text.splitlines()), in_store))


# ---- round 2 ---------------------------------------------------------------

# ---- C-13 two App-owned homes (DECISION-L L-1; C-11, C-20) ----------------
def c13():
    stores = {"H-acct": Store(), "H-key": Store()}
    tmp = tempfile.mkdtemp(prefix="del0102-")
    ledger = os.path.join(tmp, "ledger.jsonl")
    app = M.AppSession(stores, ledger, 1, {})
    app.start_supplier("H-acct")
    app.start_supplier("H-key")
    a = app.new_conversation("H-acct")
    k = app.new_conversation("H-key")
    app.send_message(a)
    app.send_message(k)
    ga, gk = app.g("H-acct"), app.g("H-key")
    ids = ga != gk and ga == M.generation_ref("sess-1", "H-acct", 1) and gk == M.generation_ref("sess-1", "H-key", 1)
    app.supplier_exits("H-key")
    lost = [e for e in app.events if e["kind"] == "observation_lost"][-1]
    isolated = (app.convs[k]["state"] == "observation-lost" and app.convs[a]["state"] == "turn-live"
                and lost["home"] == "H-key" and lost["conversations"] == [k])
    app.start_supplier("H-key")
    recovered = app.convs[k]["state"] == "indexed" and app.g("H-key") == M.generation_ref("sess-1", "H-key", 2)
    app.resume(k)
    app.send_message(k)
    q = app.request_quit()
    app.confirm_quit()
    stopped = sorted(le["home"] for le in app.ledger_written if le["kind"] == "lifecycle_ref" and le["transition"] == "LT-23")
    ok = ids and isolated and recovered and q["ask"] and len(q["liveTurns"]) == 2 and stopped == ["H-acct", "H-key"]
    app2 = M.AppSession(stores, ledger, 2, {})
    app2.start_supplier("H-acct")
    app2.start_supplier("H-key")
    reads = {le["home"] for le in app2.ledger_written if le["kind"] == "conversation_index" and le["lastObservedExecution"]["state"] == "indexed"}
    ok = ok and reads == {"H-acct", "H-key"} and app2.convs[a]["home"] == "H-acct" and app2.convs[k]["home"] == "H-key"
    errs = check_records(app) + check_records(app2)
    result("C-13", ok and not errs, "two App-owned homes: generation identities {session, home, counter} distinct; an exit of H-key's "
           "process loses only H-key's conversations; quit asks once for both homes' live turns and stops each process "
           "(LT-23 ×2); relaunch recovers each conversation from its own home%s" % ("; " + "; ".join(errs[:3]) if errs else ""))


# ---- C-14 a cancel answer interrupts the turn (C-13 of F0; OBS-2 §5.1) -----
def c14():
    _, _, _, app, tid, turn, rid = live_turn_world({})
    app.answer(rid, "cancel")
    out = [e for e in app.events if e["kind"] == "turn_outcome"][-1]
    ok = (out["outcome"] == "interrupted" and out.get("cause") == "cancel-answer" and out["causeRequest"] == rid
          and "stopRequest" not in out and not app.stops and app.register[rid]["endedAs"] == "declined"
          and not out.get("itemsNotCompleted"))
    errs = check_records(app)
    result("C-14", ok and not errs, "the person's cancel answer: item declined, turn interrupted, outcome cause 'cancel-answer' "
           "citing the request; no stop request is made%s" % ("; " + "; ".join(errs[:3]) if errs else ""))


# ---- C-15 runs in sequence in one conversation; fork (R19-2, R19-8) --------
def c15():
    store, ledger, v = new_world({})
    app = M.AppSession(store, ledger, 1, v)
    app.start_supplier()
    tid = app.new_conversation()
    app.tag(tid, "DEL-02-03 run", "run:A")
    app.send_message(tid)
    app.supplier().finish_turn(tid, app.convs[tid]["liveTurn"])
    app.tag(tid, "DEL-02-03 run", "run:B")
    app.send_message(tid)
    order = app.tags_of(tid, "DEL-02-03 run") == ["run:A", "run:B"]
    both = app.lookup_tag("DEL-02-03 run", "run:A") == [tid] == app.lookup_tag("DEL-02-03 run", "run:B")
    app.crash()
    app2 = M.AppSession(store, ledger, 2, v)
    kept = app2.tags_of(tid, "DEL-02-03 run") == ["run:A", "run:B"]
    restart = [e for e in app2.events if e["kind"] == "app_restart_interruption" and e["threadId"] == tid]
    app2.start_supplier()
    fork = app2.new_conversation(fork_of=tid)
    forked = app2.convs[fork]["forkedFrom"] == tid and app2.convs[fork]["tags"] == []
    ok = order and both and kept and len(restart) == 1 and forked
    errs = check_records(app) + check_records(app2)
    result("C-15", ok and not errs, "two runs tagged in sequence in one conversation, order kept across a relaunch, each "
           "found by its tag; the relaunch fact names the conversation and the receiver picks the run current at the end; "
           "a fork is a new conversation with forkedFrom and no tags%s" % ("; " + "; ".join(errs[:3]) if errs else ""))


# ---- C-16 Stop Codex and Restart Codex (C-12; DEF-5a) ----------------------
def c16():
    rows, all_ok = [], True
    for mode, restart in itertools.product(["interrupted", "no-response"], [True, False]):
        store, ledger, v, app, tid, turn, rid = live_turn_world({"interrupt": mode, "pending_on_interrupt": "stays-pending"})
        live, out, desc = app.assess_live_work()
        app.stop_codex(restart=restart)
        s = [x for x in app.stops.values() if x["cause"] == "codex-stop"][0]
        if not restart:
            app.start_supplier()                 # the person starts Codex later
        exp = "interrupted by Stop Codex"
        ok = (len(live) == 1 and s["outcomeLabel"] == exp and app.convs[tid]["state"] == "indexed"
              and app.register[rid]["endedAs"] in ("ended-unanswered(process-exit)",)
              and app.as_state == "running")
        if mode == "no-response":
            ok = ok and s["state"] == "outcome-recovered" and ("SR-09", s["stopRequestId"]) in app.trace
            rec = [e for e in app.events if e["kind"] == "observation_recovered"][-1]
            ok = ok and rec["turns"][0].get("historyNote")        # G-5: the turn was live at the graceful stop
        errs = check_records(app)
        all_ok = all_ok and ok and not errs
        rows.append("%s/restart=%s:%s" % (mode, restart, "ok" if ok and not errs else "FAIL " + "; ".join(errs[:2])))
    result("C-16", all_ok, "Stop Codex and Restart Codex: live turns interrupted (cause codex-stop), the process stopped "
           "gracefully, the App session keeps running; recovery on the next start; a turn live at the stop carries the "
           "graceful-stop history note (%s)" % ", ".join(rows))


def coverage():
    allrows = {t for table in M.TABLES.values() for t in table}
    missing = sorted(allrows - TRACE_ALL)
    result("C-17", not missing, "every row of the five tables taken at least once across C-01…C-16 (%d/%d)%s"
           % (len(allrows) - len(missing), len(allrows), "; not taken: " + ", ".join(missing) if missing else ""))


if __name__ == "__main__":
    for case in (c01, c02, c03, c04, c05, c06, c07, c08, c09, c10, c11, c13, c14, c15, c16):
        try:
            case()
        except Exception as exc:  # report, do not hide
            import traceback
            traceback.print_exc()
            result(case.__name__.upper().replace("C", "C-", 1), False, "exception: %r" % exc)
    coverage()
    failed = [c for c, ok, _ in RESULTS if not ok]
    print("\n%d results, %d as expected, %d not" % (len(RESULTS), len(RESULTS) - len(failed), len(failed)))
    sys.exit(1 if failed else 0)
