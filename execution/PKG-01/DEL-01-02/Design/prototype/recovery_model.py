#!/usr/bin/env python3
"""Executable model of DEL-01-02's recovery design
(EXECUTION_AND_RECOVERY.md, DEL-01-02/RECOVERY-v0.2).

Prototype only (run APP-V4-DESIGN-PASS-3-20261001, node D1, rounds 1 and 2).
NOT product code, NOT an App candidate, NOT the OI-008 O-1 proposal
realized. It models the five transition tables of the Design file (AS, CV,
OA, SR, RQ) on top of a minimal stand-in for the DEL-01-01 boundary's seam
S-1 (generations, a register of server requests, client requests), driving
supplier_stub.py.

Round 2 (DECISION-L L-1; R19-4): one Codex process per App-owned home
(H-acct, and H-key for API-key conversations); every conversation belongs to
one home; quit, Stop Codex and Restart Codex apply to each home's process;
a generation's identity is {App session, App home, spawn counter}.

The parts of HOSTING-BOUNDARY-v0.8 this model re-implements (register states,
the explicit error for an unfamiliar request, generation close) are a
simplified stand-in for that seam; HOSTING's own prototype is the model of
those rules. Numbers the design leaves open are TEST VALUES.

Frames the stub emits while the App is writing are buffered and delivered
after the write returns, as a reader thread would deliver them; this keeps
"record before send" and "state change after a successful write" honest.
"""
import json
import os

from supplier_stub import SupplierProcess, Store

# ---- TEST VALUES (open implementation choices; Design U-R4) -------------
JOURNAL_RETENTION = 40        # frames kept per generation for re-attachment
FAMILIAR_REQUESTS = {         # HOSTING §6.1 proposed partition (U-20)
    "item/commandExecution/requestApproval": "A14",
    "item/fileChange/requestApproval": "A14",
    "item/permissions/requestApproval": "A14",
    "item/tool/requestUserInput": "person-input",
    "mcpServer/elicitation/request": "person-input",
}
NEGATIVE = {"decline", "cancel"}
DEFAULT_HOME = "H-acct"

# ---- The five transition tables (checked against the Design file) ------
AS = {
    "AS-01": (("—",), "app-launched", "starting"),
    "AS-02": (("starting",), "ledger-opened", "running"),
    "AS-03": (("running",), "quit-requested", "quitting"),
    "AS-04": (("running",), "quit-requested", "quit-confirming"),
    "AS-05": (("quit-confirming",), "person-cancelled", "running"),
    "AS-06": (("quit-confirming",), "person-confirmed", "quitting"),
    "AS-07": (("quit-confirming",), "live-work-changed", "quit-confirming"),
    "AS-08": (("quitting",), "interrupts-settled-or-wait-ended", "quitting"),
    "AS-09": (("quitting",), "supplier-stopped", "ended"),
    "AS-10": (("running", "quit-confirming", "quitting"), "system-termination-notice", "ended"),
}
CV = {
    "CV-01": (("indexed",), "thread-loaded", "loaded-idle"),
    "CV-02": (("loaded-idle",), "turn-started", "turn-live"),
    "CV-03": (("turn-live",), "thread-status-changed", "turn-live"),
    "CV-04": (("turn-live",), "interrupt-sent", "interrupt-pending"),
    "CV-05": (("turn-live",), "turn-completed", "loaded-idle"),
    "CV-06": (("interrupt-pending",), "turn-completed", "loaded-idle"),
    "CV-07": (("interrupt-pending",), "interrupt-refused", "turn-live"),
    "CV-08": (("loaded-idle", "system-error"), "generation-closed", "observation-lost"),
    "CV-09": (("turn-live",), "generation-closed", "observation-lost"),
    "CV-10": (("interrupt-pending",), "generation-closed", "observation-lost"),
    "CV-11": (("observation-lost",), "supplier-ready", "recovering"),
    "CV-12": (("recovery-pending",), "supplier-ready", "recovering"),
    "CV-13": (("recovering",), "read-completed", "indexed"),
    "CV-14": (("recovering",), "read-failed", "unavailable"),
    "CV-15": (("unavailable",), "retry-requested", "recovering"),
    "CV-16": (("loaded-idle", "turn-live"), "system-error-reported", "system-error"),
    "CV-17": (("system-error",), "thread-status-changed", "loaded-idle"),
    "CV-18": (("loaded-idle",), "thread-closed", "indexed"),
    "CV-19": (("—",), "session-started", "recovery-pending"),
    "CV-20": (("—",), "session-started", "indexed"),
    "CV-21": (("—",), "thread-started", "loaded-idle"),
    "CV-22": (("recovering",), "generation-closed", "recovery-pending"),
}
OA = {
    "OA-01": (("detached",), "attach", "attached"),
    "OA-02": (("detached",), "attach", "attached"),
    "OA-03": (("attached",), "observer-lost", "detached"),
    "OA-04": (("attached",), "window-hidden", "attached"),
    "OA-05": (("attached",), "generation-closed", "attached"),
}
SR = {
    "SR-01": (("—",), "interrupt-requested", "requested"),
    "SR-02": (("requested",), "write-succeeded", "sent"),
    "SR-03": (("requested",), "write-failed-or-not-ready", "not-sent"),
    "SR-04": (("sent",), "result-observed", "accepted"),
    "SR-05": (("sent",), "error-observed", "refused"),
    "SR-06": (("sent", "accepted", "refused"), "turn-completed-interrupted", "settled"),
    "SR-07": (("sent", "accepted", "refused"), "turn-completed-other", "settled"),
    "SR-08": (("sent", "accepted", "refused"), "generation-closed", "outcome-unknown"),
    "SR-09": (("outcome-unknown",), "recovery-read", "outcome-recovered"),
    "SR-10": (("sent",), "wait-limit", "sent"),
    "SR-11": (("requested", "sent", "accepted"), "interrupt-requested-again", "same"),
    "SR-12": (("settled",), "response-observed", "settled"),
}
RQ = {
    "RQ-01": (("—",), "entry-outstanding", "listed"),
    "RQ-02": (("listed",), "observer-lost", "listed"),
    "RQ-03": (("listed",), "entry-settled", "closed"),
    "RQ-04": (("listed",), "generation-closed", "closed"),
    "RQ-05": (("closed",), "generation-closed", "closed"),
    "RQ-06": (("listed",), "session-start-reading", "closed"),
    "RQ-07": (("—",), "entry-outstanding-same-item", "listed"),
    "RQ-08": (("—",), "entry-errored-at-receipt", "closed"),
    "RQ-09": (("closed",), "acknowledgment-observed", "closed"),
}
TABLES = {"AS": AS, "CV": CV, "OA": OA, "SR": SR, "RQ": RQ}
UNSETTLED_STOP = ("sent", "accepted", "refused")
GRACEFUL = ("app-quit", "supplier-stop", "system-termination")
NOT_COMPLETED = "not completed (turn ended)"


class TransitionRefused(Exception):
    pass


class Clock:
    def __init__(self, start=0):
        self.n = start

    def now(self):
        self.n += 1
        s, ms = divmod(self.n, 1000)
        return "2026-10-02T%02d:%02d:%02d.%03dZ" % (9 + s // 3600, (s // 60) % 60, s % 60, ms)


class Ledger:
    """The App-kept record (Design §7): append-only, one JSON object per
    line. Location and technology are unselected (TBD-002); a file under
    $TMPDIR stands in."""

    def __init__(self, path):
        self.path = path

    def append(self, entry):
        with open(self.path, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, sort_keys=True) + "\n")

    def read(self):
        if not os.path.exists(self.path):
            return []
        with open(self.path, encoding="utf-8") as f:
            return [json.loads(line) for line in f if line.strip()]


from generation_ref import generation_ref


class AppSession:
    """One run of the App process. `stores` maps each App-owned home to
    Codex's on-disk history in that home (sessions live under each
    CODEX_HOME); a single Store stands for H-acct. Stores and the ledger
    survive; everything else is memory and ends with the process."""

    def __init__(self, stores, ledger_path, session_no, variant=None):
        self.stores = stores if isinstance(stores, dict) else {DEFAULT_HOME: stores}
        self.ledger = Ledger(ledger_path)
        self.session = "sess-%d" % session_no
        self.variant = variant or {}
        self.clock = Clock(session_no * 100000)
        self.trace, self.events, self.ledger_written = [], [], []
        self.stops, self.convs, self.children, self.register = {}, {}, {}, {}
        self.journal, self.observers, self.pending = {}, {}, {}
        self.told = []
        self.hang_reads = False
        self._buf, self._in_write = [], False
        self.closed_gens = set()
        self.homes = {}             # home -> {"gn", "g", "supplier", "hosting"}
        self.cancel_answers = {}    # turn id -> request id answered `cancel`
        self._cid = self._sid = self._eid = 0
        self.quit_actor = "person:ex-1"
        self._launch()

    # ---- bookkeeping ----------------------------------------------------
    def _t(self, tid, subject_state, subject=None):
        froms, _event, to = TABLES[tid[:2]][tid]
        if subject_state not in froms:
            raise TransitionRefused("%s not allowed from %r" % (tid, subject_state))
        self.trace.append((tid, subject))
        return subject_state if to == "same" else to

    def _ledger(self, kind, **body):
        entry = {"kind": kind, "session": self.session, "at": self.clock.now()}
        entry.update(body)
        self.ledger.append(entry)
        self.ledger_written.append(entry)
        return entry

    def _event(self, kind, **body):
        self._eid += 1
        ev = {"kind": kind, "eventId": "cev:%s:%d" % (self.session, self._eid),
              "appSession": self.session, "at": self.clock.now(), "standing": "App-observed"}
        ev.update(body)
        self.events.append(ev)
        for ob in self.observers.values():
            if ob["state"] == "attached":
                ob["received"].append(("custody", ev["kind"]))
        return ev

    @staticmethod
    def _person(actor):
        return {"kind": "person", "identity": actor, "identityStatus": "identity not verified"}

    def _home(self, home):
        return self.homes.setdefault(home, {"gn": 0, "g": None, "supplier": None, "hosting": "absent"})

    def g(self, home=DEFAULT_HOME):
        return self._home(home)["g"]

    def supplier(self, home=DEFAULT_HOME):
        return self._home(home)["supplier"]

    # ---- App session start: the reading of the previous session ----------
    def _launch(self):
        self.as_state = self._t("AS-01", "—", self.session)
        prior = self.ledger.read()
        sessions = [e["session"] for e in prior if e["kind"] == "session_started"]
        prev = sessions[-1] if sessions else None
        self.prev_reading = "none"
        if prev:
            mine = [e for e in prior if e.get("session") == prev]
            ended = [e for e in mine if e["kind"] == "session_ended"]
            confirmed = any(e["kind"] == "quit_answered" and e["answer"] == "confirmed" for e in mine)
            asked = any(e["kind"] == "quit_requested" and e["liveTurns"] for e in mine)
            if not ended:
                self.prev_reading = "ended-without-record"
            elif ended[-1]["how"] == "system-terminated":
                self.prev_reading = "system-terminated"
            elif confirmed and asked:
                self.prev_reading = "quit-with-live-work"
            else:
                self.prev_reading = "clean"
        body = {"previousSessionEnd": self.prev_reading, "candidate": "model-only (no App candidate)"}
        if prev:
            body["previousSession"] = prev
        self._ledger("session_started", **body)
        index, summaries, stops = {}, {}, {}
        for e in prior:
            if e["kind"] == "conversation_index":
                index[e["threadId"]] = e
            elif e["kind"] == "register_entry_summary":
                summaries[(e["generation"], e["requestIdentity"])] = e
            elif e["kind"] == "stop_request":
                stops[e["record"]["stopRequestId"]] = e["record"]
        self.prior_summaries = summaries
        unsettled = ("turn-live", "interrupt-pending", "observation-lost", "recovery-pending",
                     "recovering", "unavailable")
        live_at_end = {}
        if self.prev_reading == "quit-with-live-work":
            asked = [e for e in prior if e.get("session") == prev and e["kind"] == "quit_requested"]
            for t in asked[-1]["liveTurns"]:
                live_at_end.setdefault(t["threadId"], []).append(t)
        elif self.prev_reading in ("ended-without-record", "system-terminated"):
            for tid, e in index.items():
                if e["lastObservedExecution"].get("liveTurn"):
                    live_at_end[tid] = [{"threadId": tid, "turnId": e["lastObservedExecution"]["liveTurn"]}]
        for tid, turns in live_at_end.items():
            self._event("app_restart_interruption", threadId=tid, home=index[tid]["home"], priorSession=prev,
                        priorSessionEnd=self.prev_reading, liveTurnsAtEnd=turns)
        for tid, e in index.items():
            last = e["lastObservedExecution"]
            conv = self._conv(tid, e["home"], e["project"], e["tags"], e.get("forkedFrom"))
            if last["state"] in unsettled or last.get("liveTurn"):
                conv["state"] = self._t("CV-19", "—", tid)
                if last.get("liveTurn"):
                    conv["lostTurn"] = last["liveTurn"]
                    conv["lostCause"] = last.get("lostCause") or (
                        "app-quit" if self.prev_reading == "quit-with-live-work" else "app-ended-without-record")
                    conv["lostItems"] = list(last.get("openItems", []))
                    conv["markerExpected"] = bool(last.get("abortNoteExpected"))
            else:
                conv["state"] = self._t("CV-20", "—", tid)
        for sid, s in stops.items():
            if s["appSession"] == prev and s["state"] in UNSETTLED_STOP:
                s = dict(s)
                s["state"] = self._t("SR-08", s["state"], sid)
                if s["response"] == "pending":
                    s["response"] = "unknown-no-response"
                s["turnOutcome"], s["outcomeSource"] = "unknown", "not-observed"
                s["outcomeLabel"] = self._label(s["cause"], "unknown")
                s["transition"] = "SR-08"
                self.stops[sid] = s
                self._persist_stop(s)
            elif s["appSession"] == prev and s["state"] == "outcome-unknown":
                self.stops[sid] = dict(s)
        for key, s in summaries.items():
            if s["state"] == "listed" and s["session"] == prev:
                self._t("RQ-06", "listed", key)
                closed = {k: v for k, v in s.items() if k not in ("kind", "at", "session")}
                closed.update({"state": "closed", "endedAs": "ended-unanswered(process-exit)",
                               "context": "app-ended-without-record", "transition": "RQ-06"})
                self._ledger("register_entry_summary", **closed)
                self._event("request_ended_unanswered", entry=self._entry_ref(closed),
                            context="app-ended-without-record")
        self.as_state = self._t("AS-02", self.as_state, self.session)

    def _conv(self, tid, home=DEFAULT_HOME, project="project:ex-1", tags=None, forked_from=None):
        c = self.convs.get(tid)
        if c is None:
            c = {"state": None, "home": home, "liveTurn": None, "flags": [], "project": project,
                 "tags": list(tags or []), "inflight": {}, "loadedIn": None, "forkedFrom": forked_from,
                 "lostTurn": None, "lostCause": None, "lostItems": []}
            self.convs[tid] = c
        return c

    def _index(self, tid):
        c = self.convs[tid]
        ex = {"state": c["state"], "at": self.clock.now()}
        lost_state = c["state"] in ("observation-lost", "recovery-pending")
        live = c["liveTurn"] or (c["lostTurn"] if lost_state else None)
        if live:
            ex["liveTurn"] = live
        if c["lostCause"] and lost_state:
            ex["lostCause"] = c["lostCause"]
        if c.get("markerExpected") and lost_state:
            ex["abortNoteExpected"] = True
        items = list(c["inflight"].values()) if c["liveTurn"] else (c["lostItems"] if lost_state else [])
        if items:
            ex["openItems"] = [{"itemId": i["itemId"], "itemType": i["itemType"]} for i in items]
        body = {"threadId": tid, "home": c["home"], "project": c["project"], "tags": c["tags"],
                "lastObservedExecution": ex}
        if c["loadedIn"]:
            body["lastLoadedGeneration"] = c["loadedIn"]
        if c["forkedFrom"]:
            body["forkedFrom"] = c["forkedFrom"]
        self._ledger("conversation_index", **body)

    # ---- the DEL-01-01 seam stand-in, one child per App home ---------------
    def start_supplier(self, home=DEFAULT_HOME):
        h = self._home(home)
        h["gn"] += 1
        h["g"] = generation_ref(self.session, home, h["gn"])   # {App session, App home, spawn counter}
        self.journal[h["g"]] = []
        store = self.stores.setdefault(home, Store())
        h["supplier"] = SupplierProcess(store, lambda g, f, home=home: self._sink(home, g, f), self.variant, h["g"])
        h["hosting"] = "ready"
        self._ledger("lifecycle_ref", home=home, generation=h["g"], transition="LT-09", state="ready")
        for tid, c in list(self.convs.items()):
            if c["home"] != home:
                continue
            if c["state"] == "observation-lost":
                c["state"] = self._t("CV-11", c["state"], tid)
                self._recover(tid)
            elif c["state"] == "recovery-pending":
                c["state"] = self._t("CV-12", c["state"], tid)
                self._recover(tid)

    def _write(self, home, frame):
        h = self._home(home)
        if h["supplier"] is None or h["hosting"] != "ready":
            return False
        self._in_write = True
        try:
            return h["supplier"].write(frame)
        finally:
            self._in_write = False

    def _drain(self):
        while self._buf:
            home, g, fr = self._buf.pop(0)
            self._process(home, g, fr)

    def _send(self, home, method, params, cb=None):
        self._cid += 1
        cid = "cr-%s-%d" % (self.g(home), self._cid)
        if cb:
            self.pending[cid] = cb
        ok = self._write(home, {"id": cid, "method": method, "params": params})
        if not ok:
            self.pending.pop(cid, None)
        self._drain()
        return cid, ok

    def _sink(self, home, g, frame):
        if self._in_write:
            self._buf.append((home, g, frame))
        else:
            self._process(home, g, frame)

    def _process(self, home, g, frame):
        if g != self.g(home):
            return  # H5: nothing crosses generations
        if "method" not in frame:
            cb = self.pending.pop(frame["id"], None)
            if cb:
                cb(frame)
            return
        pos = (self.journal[g][-1][0] if self.journal[g] else 0) + 1
        self.journal[g].append((pos, frame))
        if len(self.journal[g]) > JOURNAL_RETENTION:
            self.journal[g].pop(0)
        for ob in self.observers.values():
            if ob["state"] == "attached":
                ob["received"].append((g, pos))
                ob["positions"][home] = (g, pos)
        if "id" in frame:
            self._on_server_request(home, frame)
        else:
            self._on_notification(home, frame["method"], frame["params"])

    # ---- notifications → CV, SR, RQ ---------------------------------------
    def _on_notification(self, home, m, p):
        tid = p.get("threadId")
        if m == "item/completed" and p["item"]["type"] == "collabAgentToolCall":
            # a child is announced by the parent's item (no thread/started; OBS-2 §6.2, via adapter)
            for ct in p["item"].get("receiverThreadIds", []):
                self.children.setdefault(ct, {"parent": tid, "liveTurn": None, "home": home})
        if tid in self.children or (tid and tid not in self.convs and m in ("turn/started", "turn/completed")):
            ch = self.children.setdefault(tid, {"parent": None, "liveTurn": None, "home": home})
            if m == "turn/started":
                ch["liveTurn"] = p["turn"]["id"]
            elif m == "turn/completed":
                ch["liveTurn"] = None
            return
        c = self.convs.get(tid) if tid else None
        if m == "thread/status/changed" and c:
            st = p["status"]
            if st["type"] == "systemError" and c["state"] in ("loaded-idle", "turn-live"):
                c["state"] = self._t("CV-16", c["state"], tid)
                self._index(tid)
            elif c["state"] == "system-error" and st["type"] in ("idle", "active"):
                c["state"] = self._t("CV-17", c["state"], tid)
            elif c["state"] in ("turn-live", "interrupt-pending") and st["type"] == "active":
                c["flags"] = list(st.get("activeFlags", []))
                if c["state"] == "turn-live":
                    c["state"] = self._t("CV-03", c["state"], tid)
        elif m == "turn/started" and c:
            c["liveTurn"] = p["turn"]["id"]
            c["state"] = self._t("CV-02", c["state"], tid)
            self._index(tid)
        elif m == "item/started" and c:
            c["inflight"][p["item"]["id"]] = {"threadId": tid, "turnId": p["turnId"],
                                              "itemId": p["item"]["id"], "itemType": p["item"]["type"],
                                              "lastObservedStatus": "inProgress"}
        elif m == "item/completed" and c:
            c["inflight"].pop(p["item"]["id"], None)
            for s in self.stops.values():
                if s["turnId"] == p["turnId"] and s["state"] in UNSETTLED_STOP:
                    s.setdefault("itemsCompletedAfterRequest", []).append(
                        {"itemId": p["item"]["id"], "itemType": p["item"]["type"]})
        elif m == "turn/completed" and c:
            turn_id, status = p["turn"]["id"], p["turn"]["status"]
            # G-4 (R18-7): items opened and never completed settle at turn end
            open_items = [{"itemId": i["itemId"], "itemType": i["itemType"], "settled": NOT_COMPLETED}
                          for i in c["inflight"].values() if i["turnId"] == turn_id]
            for s in list(self.stops.values()):
                if s["turnId"] == turn_id and s["state"] in UNSETTLED_STOP:
                    rid = "SR-06" if status == "interrupted" else "SR-07"
                    s["state"] = self._t(rid, s["state"], s["stopRequestId"])
                    s["turnOutcome"], s["outcomeSource"] = status, "observed"
                    s["outcomeLabel"] = self._label(s["cause"], status)
                    s["descendantsActiveAtOutcome"] = self._active_children(tid)
                    if open_items:
                        s["itemsNotCompleted"] = [{"itemId": i["itemId"], "itemType": i["itemType"]} for i in open_items]
                    s["transition"] = rid
                    self._persist_stop(s)
            stop = self._stop_for(turn_id)
            if c["state"] == "interrupt-pending":
                c["state"] = self._t("CV-06", c["state"], tid)
            elif c["state"] == "turn-live":
                c["state"] = self._t("CV-05", c["state"], tid)
            c["liveTurn"], c["flags"] = None, []
            c["inflight"] = {k: v for k, v in c["inflight"].items() if v["turnId"] != turn_id}
            ev = {"threadId": tid, "turnId": turn_id, "outcome": status, "source": "observed"}
            if stop is not None:
                ev["cause"], ev["stopRequest"] = stop["cause"], stop["stopRequestId"]
            elif status == "interrupted" and turn_id in self.cancel_answers:
                # C-13 (R18-1): the person's `cancel` answer declined the item and interrupted the turn
                ev["cause"] = "cancel-answer"
                ev["causeRequest"] = self.cancel_answers[turn_id]
            if open_items:
                ev["itemsNotCompleted"] = open_items
            children = self._active_children(tid)
            if children:
                ev["descendantsActive"] = children
            self._event("turn_outcome", **ev)
            self._index(tid)
        elif m == "serverRequest/resolved":
            e = self.register.get(p["requestId"])
            if e and e["g"] == self.g(home) and e["g"] not in self.closed_gens:
                if e["state"] == "listed":
                    e["endedAs"] = "resolved-by-supplier"
                    self._close_entry(e, "RQ-03")
                elif e["state"] == "closed" and e.get("replyWrite") == "written" and e.get("ack") != "observed" and (
                        e.get("endedAs") in ("answered", "declined") or
                        e.get("endedAs") == "errored" and e.get("laterProtocolError")):
                    # RT-12/13 existing answer/decline; RT-15 only RT-14 later error.
                    e["ack"] = "observed"
                    self._t("RQ-09", "closed", e["requestIdentity"])
                    self._summary(e, "RQ-09")
        elif m == "thread/closed" and c and c["state"] == "loaded-idle":
            c["state"] = self._t("CV-18", c["state"], tid)
            c["loadedIn"] = None
            self._index(tid)

    @staticmethod
    def _label(cause, status):
        words = {"quit": ("interrupted by quit", "quit requested"),
                 "codex-stop": ("interrupted by Stop Codex", "Stop Codex requested"),
                 "person-interrupt": ("interrupted by the person", "stop requested")}[cause]
        if status == "interrupted":
            return words[0]
        if status == "unknown":
            return ("outcome unknown (stop requested)" if cause == "person-interrupt"
                    else "%s (final status not observed)" % words[0])
        return "%s (%s)" % (status, words[1])

    def _active_children(self, tid):
        return [{"kind": "child-thread", "ref": ct, "observedStatus": "active"}
                for ct, ch in self.children.items() if ch["parent"] == tid and ch["liveTurn"]]

    def _stop_for(self, turn_id):
        found = [s for s in self.stops.values() if s["turnId"] == turn_id]
        return found[-1] if found else None

    # ---- server requests → register stand-in + RQ ------------------------
    def _on_server_request(self, home, frame):
        m, rid, p = frame["method"], frame["id"], frame.get("params", {})
        e = {"g": self.g(home), "home": home, "requestIdentity": rid, "method": m, "threadId": p.get("threadId"),
             "turnId": p.get("turnId"), "itemId": p.get("itemId")}
        self.register[rid] = e
        if m not in FAMILIAR_REQUESTS:
            ok = self._write(home, {"id": rid, "error": {"code": -32601, "message": "unfamiliar request"}})
            e.update({"state": "closed", "endedAs": "errored", "origin": "app-explicit-error",
                      "replyWrite": "written" if ok else "write-failed"})
            self._t("RQ-08", "—", rid)
            self._summary(e, "RQ-08")
            self._drain()
            return
        same = [s for s in self.prior_summaries.values()
                if e["itemId"] and s.get("subject", {}).get("itemId") == e["itemId"]]
        same += [x for x in self.register.values() if x is not e and e["itemId"]
                 and x.get("itemId") == e["itemId"] and x["state"] == "closed"]
        if same:
            e["state"] = self._t("RQ-07", "—", rid)
            e["sameItemAs"] = "%s %s" % (same[0].get("generation", same[0].get("g")), same[0]["requestIdentity"])
            self._summary(e, "RQ-07")
        else:
            e["state"] = self._t("RQ-01", "—", rid)
            self._summary(e, "RQ-01")

    def _summary(self, e, transition):
        body = {"generation": e["g"], "requestIdentity": e["requestIdentity"], "method": e["method"],
                "state": e["state"], "transition": transition}
        subject = {k: e[k] for k in ("threadId", "turnId", "itemId") if e.get(k)}
        if subject:
            body["subject"] = subject
        for k in ("endedAs", "origin", "replyWrite", "context", "sameItemAs"):
            if e.get(k):
                body[k] = e[k]
        if e.get("ack"):
            body["acknowledgment"] = e["ack"]
        self._ledger("register_entry_summary", **body)

    @staticmethod
    def _entry_ref(e):
        ref = {"generation": e.get("generation", e.get("g")), "requestIdentity": e["requestIdentity"],
               "method": e["method"]}
        subj = e.get("subject") or {k: e[k] for k in ("threadId", "turnId", "itemId") if e.get(k)}
        if subj:
            ref["subject"] = subj
        return ref

    def _close_entry(self, e, tid):
        e["state"] = self._t(tid, e["state"], e["requestIdentity"])
        self._summary(e, tid)

    def protocol_error(self, rid, error, origin):
        """CC-REC-RT-LINK: stand-in boundary RT-14/RT-09 result for R9 later error.
        Not a second production error authority or human content answer.
        """
        e = self.register.get(rid)
        if e is None:
            return "refused: no-such-request"
        if e["g"] != self.g(e["home"]) or e["g"] in self.closed_gens:
            return "refused: generation-closed"
        if e.get("endedAs") == "resolved-by-supplier":
            return "refused: already-resolved"
        if e["state"] != "listed":
            return "refused: already-settled"
        if FAMILIAR_REQUESTS.get(e["method"]) != "person-input" or not (
                origin == "app-explicit-error" or origin.startswith("app-rule:") and len(origin) > len("app-rule:")):
            return "refused: origin-not-permitted"
        if not isinstance(error, dict) or not isinstance(error.get("code"), int) or isinstance(error["code"], bool) or not isinstance(error.get("message"), str):
            return "refused: invalid-answer"
        ok = self._write(e["home"], {"id": rid, "error": error})
        e["origin"], e["replyWrite"] = origin, ("written" if ok else "write-failed")
        e["endedAs"] = "errored" if ok else "settle-write-failed"
        e["laterProtocolError"] = True  # identifies RT-14 branch for RT-15, never receipt RT-02/03
        self._close_entry(e, "RQ-03")
        self._drain()
        return "accepted-for-write"

    def answer(self, rid, decision, origin="person-via-interaction"):
        """Stand-in for HOSTING §6.4 answer (DEL-01-04 calls DEL-01-01 directly)."""
        e = self.register.get(rid)
        if e is None:
            return "refused: no-such-request"
        if e["g"] != self.g(e["home"]) or e["g"] in self.closed_gens:
            return "refused: generation-closed"
        if e.get("endedAs") == "resolved-by-supplier":
            return "refused: already-resolved"
        if e["state"] != "listed":
            return "refused: already-settled"
        if origin.startswith("app-rule:") and decision not in NEGATIVE:
            return "refused: origin-not-permitted"
        ok = self._write(e["home"], {"id": rid, "result": {"decision": decision}})
        e["origin"], e["replyWrite"] = origin, ("written" if ok else "write-failed")
        e["endedAs"] = ("declined" if decision in NEGATIVE else "answered") if ok else "settle-write-failed"
        if ok and decision == "cancel" and FAMILIAR_REQUESTS[e["method"]] == "A14":
            self.cancel_answers[e["turnId"]] = rid
        self._close_entry(e, "RQ-03")
        self._drain()
        return "accepted-for-write"

    def list_outstanding(self, tid=None):
        return [e for e in self.register.values() if e["state"] == "listed"
                and (tid is None or e["threadId"] == tid)]

    # ---- operations offered (Design §4) ----------------------------------
    def new_conversation(self, home=DEFAULT_HOME, project="project:ex-1", tags=None, fork_of=None):
        result = {}
        if fork_of:
            self._send(home, "thread/fork", {"threadId": fork_of}, lambda fr: result.update(fr.get("result", {})))
        else:
            self._send(home, "thread/start", {}, lambda fr: result.update(fr.get("result", {})))
        tid = result["thread"]["id"]
        c = self._conv(tid, home, project, tags, result["thread"].get("forkedFromId"))
        c["loadedIn"] = self.g(home)
        c["state"] = self._t("CV-21", "—", tid)
        self._index(tid)
        return tid

    def tag(self, tid, owner, value):
        """Opaque receiver tag handed at run time (for example a run
        reference). Several per owner and conversation, kept in order, so
        runs can follow one another in one conversation (R19-2). Stored and
        returned, never interpreted (R17-10)."""
        tags = self.convs[tid]["tags"]
        tags.append({"owner": owner, "value": value, "seq": len(tags) + 1})
        self._index(tid)

    def lookup_tag(self, owner, value):
        return [tid for tid, c in self.convs.items()
                if any(t["owner"] == owner and t["value"] == value for t in c["tags"])]

    def tags_of(self, tid, owner):
        return [t["value"] for t in sorted(self.convs[tid]["tags"], key=lambda t: t["seq"]) if t["owner"] == owner]

    def send_message(self, tid):
        c = self.convs[tid]
        if c["state"] != "loaded-idle":
            return "refused: conversation not loaded (%s)" % c["state"]
        self._send(c["home"], "turn/start", {"threadId": tid})
        return "sent"

    def resume(self, tid):
        """The person's choice to continue a conversation; never automatic,
        no prompt re-sent, and no guidance input (R19-3; O-5: ignored)."""
        c = self.convs[tid]
        if c["state"] != "indexed":
            return "refused: %s" % c["state"]
        result = {}
        self._send(c["home"], "thread/resume", {"threadId": tid}, lambda fr: result.update(fr))
        if "result" not in result:
            return "refused: %s" % result.get("error", {}).get("message", "no response")
        c["loadedIn"] = self.g(c["home"])
        c["state"] = self._t("CV-01", c["state"], tid)
        self._index(tid)
        return "resumed"

    def interrupt(self, tid, actor="person:ex-1", cause="person-interrupt"):
        c = self.convs.get(tid)
        if c is None or c["liveTurn"] is None:
            return "refused: no-live-turn"
        prior = self._stop_for(c["liveTurn"])
        if prior and prior["state"] in ("requested", "sent", "accepted"):
            self._t("SR-11", prior["state"], prior["stopRequestId"])
            return "refused: stop-already-requested"
        if c["state"] != "turn-live":
            return "refused: %s" % c["state"]
        home = c["home"]
        self._sid += 1
        s = {"kind": "stop_request", "stopRequestId": "stop:%s:%d" % (self.session, self._sid),
             "appSession": self.session, "home": home, "generation": self.g(home), "threadId": tid,
             "turnId": c["liveTurn"], "cause": cause, "requestedBy": self._person(actor),
             "requestedAt": self.clock.now(), "send": "pending", "response": "pending",
             "turnOutcome": "pending", "outcomeSource": "not-observed"}
        s["state"] = self._t("SR-01", "—", s["stopRequestId"])
        s["transition"] = "SR-01"
        self.stops[s["stopRequestId"]] = s
        self._persist_stop(s)                       # written before sending

        def on_response(fr):
            if "error" in fr:
                s["response"], s["responseError"] = "error", fr["error"]["message"]
                if s["state"] == "sent":
                    s["state"] = self._t("SR-05", s["state"], s["stopRequestId"])
                    s["transition"] = "SR-05"
                    if c["state"] == "interrupt-pending":
                        c["state"] = self._t("CV-07", c["state"], tid)
                    self.told.append("stop refused by Codex: %s" % s["responseError"])
                else:
                    s["state"] = self._t("SR-12", s["state"], s["stopRequestId"])
                    s["transition"] = "SR-12"
            else:
                s["response"] = "result"
                rid = "SR-04" if s["state"] == "sent" else "SR-12"
                s["state"] = self._t(rid, s["state"], s["stopRequestId"])
                s["transition"] = rid
            self._persist_stop(s)

        self._cid += 1
        cid = "cr-%s-%d" % (self.g(home), self._cid)
        self.pending[cid] = on_response
        ok = self._write(home, {"id": cid, "method": "turn/interrupt",
                                "params": {"threadId": tid, "turnId": s["turnId"]}})
        if not ok:
            self.pending.pop(cid, None)
            ready = self._home(home)["hosting"] == "ready"
            s["send"] = "not-sent(write-failed)" if ready else "not-sent(not-ready)"
            s["response"] = "unknown-no-response" if ready else "not-applicable"
            s["state"] = self._t("SR-03", s["state"], s["stopRequestId"])
            s["transition"] = "SR-03"
            self.told.append("stop not sent")
            self._persist_stop(s)
            return "not-sent"
        s["clientRequest"], s["send"] = cid, "sent"
        s["state"] = self._t("SR-02", s["state"], s["stopRequestId"])
        s["transition"] = "SR-02"
        c["state"] = self._t("CV-04", c["state"], tid)
        self._persist_stop(s)
        self._drain()
        return s["stopRequestId"]

    def end_wait(self, stop_id):
        s = self.stops[stop_id]
        s["state"] = self._t("SR-10", s["state"], stop_id)
        s["waitingEnded"], s["transition"] = True, "SR-10"
        self._persist_stop(s)

    def _persist_stop(self, s):
        self._ledger("stop_request", record=json.loads(json.dumps(s)))

    # ---- observers (OA) ----------------------------------------------------
    def attach(self, name, position=None, rendered=None, home=DEFAULT_HOME):
        ob = self.observers.setdefault(name, {"state": "detached", "positions": {}, "received": []})
        ob["stale"] = dict(rendered or {})
        g = self.g(home)
        kept = [p for p, _ in self.journal.get(g, [])] if g else []
        if position and position[0] == g and kept and kept[0] <= position[1] + 1:
            ob["state"] = self._t("OA-01", ob["state"], name)
            replay = [(g, p) for p in kept if p > position[1]]
            ob["received"].extend(replay)
            ob["positions"][home] = replay[-1] if replay else position
            ob["gap"] = None
        else:
            ob["state"] = self._t("OA-02", ob["state"], name)
            ob["gap"] = "events before %s rebuilt from Codex history" % self.clock.now()
            ob["positions"][home] = (g, kept[-1]) if kept else None
        ob["position"] = ob["positions"][home]
        ob["rendered"] = self.snapshot()      # stale rendered state establishes nothing
        return ob

    def detach(self, name):
        ob = self.observers[name]
        before = sum(len(h["supplier"].writes) for h in self.homes.values() if h["supplier"])
        ob["state"] = self._t("OA-03", ob["state"], name)
        for e in self.list_outstanding():
            self._t("RQ-02", e["state"], e["requestIdentity"])
        return sum(len(h["supplier"].writes) for h in self.homes.values() if h["supplier"]) - before

    def hide(self, name):
        ob = self.observers[name]
        ob["state"] = self._t("OA-04", ob["state"], name)

    def snapshot(self):
        return {tid: {"state": c["state"], "home": c["home"], "liveTurn": c["liveTurn"], "flags": list(c["flags"]),
                      "outstanding": [e["requestIdentity"] for e in self.list_outstanding(tid)]}
                for tid, c in self.convs.items()}

    # ---- generation close (supplier exit, stop, quit), per home ------------
    def close_generation(self, home, cause):
        h = self._home(home)
        g = h["g"]
        self.closed_gens.add(g)
        graceful = cause in GRACEFUL
        lost, live, inflight = [], [], []
        for tid, c in self.convs.items():
            if c["home"] != home:
                continue
            if c["state"] in ("loaded-idle", "system-error", "turn-live", "interrupt-pending"):
                lost.append(tid)
                if c["liveTurn"]:
                    live.append({"threadId": tid, "turnId": c["liveTurn"]})
                    c["lostTurn"], c["lostCause"] = c["liveTurn"], cause
                    c["lostItems"] = list(c["inflight"].values())
                    c["markerExpected"] = graceful   # G-5: Codex writes its abort note on a graceful stop
                inflight.extend(c["inflight"].values())
                rid = {"loaded-idle": "CV-08", "system-error": "CV-08", "turn-live": "CV-09",
                       "interrupt-pending": "CV-10"}[c["state"]]
                c["state"] = self._t(rid, c["state"], tid)
            elif c["state"] == "recovering":
                c["state"] = self._t("CV-22", c["state"], tid)
        outstanding = []
        for e in self.register.values():
            if e["g"] != g:
                continue
            if e["state"] == "listed":
                outstanding.append(self._entry_ref(e))
                e["endedAs"], e["context"] = "ended-unanswered(process-exit)", cause
                self._close_entry(e, "RQ-04")
                self._event("request_ended_unanswered", entry=self._entry_ref(e), context=cause)
            elif e["state"] == "closed" and e.get("replyWrite") == "written" and e.get("ack") != "observed" \
                    and (e.get("endedAs") in ("answered", "declined") or e.get("endedAs") == "errored" and e.get("laterProtocolError")):
                e["ack"] = "not-observed"
                self._t("RQ-05", "closed", e["requestIdentity"])
                self._summary(e, "RQ-05")
                self._event("acknowledgment_not_observed", entry=self._entry_ref(e),
                            settlementOrigin=e["origin"], context=cause)
        for s in self.stops.values():
            if s["generation"] == g and s["state"] in UNSETTLED_STOP:
                s["state"] = self._t("SR-08", s["state"], s["stopRequestId"])
                if s["response"] == "pending":
                    s["response"] = "unknown-no-response"
                s["turnOutcome"], s["outcomeSource"] = "unknown", "not-observed"
                s["outcomeLabel"] = self._label(s["cause"], "unknown")
                s["transition"] = "SR-08"
                self._persist_stop(s)
        if lost:
            self._event("observation_lost", home=home, generation=g, cause=cause, conversations=lost,
                        liveTurns=live, inFlightItems=inflight, outstandingEntries=outstanding)
        for name, ob in self.observers.items():
            if ob["state"] == "attached":
                ob["state"] = self._t("OA-05", ob["state"], name)
        for tid in lost:
            c = self.convs[tid]
            c["inflight"], c["liveTurn"], c["loadedIn"], c["flags"] = {}, None, None, []
            self._index(tid)
        for ch in self.children.values():
            if ch["home"] == home:
                ch["liveTurn"] = None
        self.pending.clear()
        h["hosting"] = "stopped" if graceful else "exited"
        self._ledger("lifecycle_ref", home=home, generation=g,
                     transition="LT-23" if graceful else "LT-12", state=h["hosting"])

    def supplier_exits(self, home=DEFAULT_HOME):
        """Unexpected exit (HOSTING §4.3): the child ends with no stop record."""
        self.supplier(home).end(graceful=False)
        self.close_generation(home, "supplier-exit")

    def _stop_process(self, home, cause):
        """HOSTING §4.5: stop record, close input (graceful), then the tree."""
        h = self._home(home)
        if h["supplier"] is not None and h["hosting"] == "ready":
            h["supplier"].end(graceful=True)
            self.close_generation(home, cause)

    # ---- recovery reads ----------------------------------------------------
    def _recover(self, tid):
        c = self.convs[tid]
        home = c["home"]
        if self.hang_reads:
            return
        res = {}
        self._send(home, "thread/read", {"threadId": tid}, lambda fr: res.update(read=fr))
        if "result" not in res.get("read", {}):
            reason = res.get("read", {}).get("error", {}).get("message", "no response")
            c["state"] = self._t("CV-14", c["state"], tid)
            self._event("observation_recovered", threadId=tid, home=home, generation=self.g(home),
                        via="thread/read", priorEvents="unavailable", unavailableReason=reason, turns=[])
            self._index(tid)
            return
        self._send(home, "thread/turns/list", {"threadId": tid}, lambda fr: res.update(turns=fr))
        statuses = {t["id"]: t["status"] for t in res["turns"]["result"]["data"]}
        recovered = []
        lost_turn = c["lostTurn"]
        if lost_turn:
            st = statuses.get(lost_turn)
            outcome = st if st in ("interrupted", "completed", "failed") else "unknown"
            if c["lostCause"] in ("app-quit", "system-termination"):
                reading = "interrupted by quit; Codex reports: %s" % (st or "no such turn")
            elif c["lostCause"] == "supplier-stop":
                reading = "interrupted by Stop Codex; Codex reports: %s" % (st or "no such turn")
            elif outcome != "unknown":
                reading = "recovered from Codex: %s" % st
            elif st == "inProgress":
                reading = "outcome unknown (Codex history reports inProgress for a turn whose process ended)"
            else:
                reading = "outcome unknown (turn not in Codex history)"
            row = {"turnId": lost_turn, "supplierStatus": st or "absent", "appReading": reading}
            if c.get("markerExpected"):
                row["historyNote"] = "graceful-stop abort note (Codex 0.158.0, observed OBS-2)"
            recovered.append(row)
            ev = {"threadId": tid, "turnId": lost_turn, "outcome": outcome,
                  "source": "recovered-from-supplier" if outcome != "unknown" else "not-observed"}
            if c["lostItems"] and outcome != "unknown":
                ev["itemsNotCompleted"] = [{"itemId": i["itemId"], "itemType": i["itemType"], "settled": NOT_COMPLETED}
                                           for i in c["lostItems"]]
            stop = self._stop_for(lost_turn)
            if stop is not None:
                ev["cause"], ev["stopRequest"] = stop["cause"], stop["stopRequestId"]
                if stop["state"] == "outcome-unknown" and outcome != "unknown":
                    stop["state"] = self._t("SR-09", stop["state"], stop["stopRequestId"])
                    stop["turnOutcome"], stop["outcomeSource"] = outcome, "recovered-from-supplier"
                    stop["outcomeLabel"] = self._label(stop["cause"], outcome)
                    stop["transition"] = "SR-09"
                    self._persist_stop(stop)
            elif c["lostCause"] in ("app-quit", "system-termination"):
                ev["cause"] = "quit"
            elif c["lostCause"] == "supplier-stop":
                ev["cause"] = "codex-stop"
            self._event("turn_outcome", **ev)
        c["state"] = self._t("CV-13", c["state"], tid)
        c["lostTurn"], c["lostCause"], c["lostItems"], c["markerExpected"] = None, None, [], False
        self._event("observation_recovered", threadId=tid, home=home, generation=self.g(home), via="thread/read",
                    priorEvents="accessible", turns=recovered)
        self._index(tid)

    def retry(self, tid):
        c = self.convs[tid]
        c["state"] = self._t("CV-15", c["state"], tid)
        self._recover(tid)

    # ---- live work, quit (K-4), Stop and Restart Codex (C-12) ---------------
    def assess_live_work(self, homes=None):
        sel = lambda h: homes is None or h in homes  # noqa: E731
        live = [{"threadId": t, "turnId": c["liveTurn"]} for t, c in self.convs.items()
                if c["liveTurn"] and sel(c["home"])]
        out = [self._entry_ref(e) for e in self.list_outstanding() if sel(e["home"])]
        desc = [d for t, c in self.convs.items() if c["liveTurn"] and sel(c["home"]) for d in self._active_children(t)]
        return live, out, desc

    def request_quit(self, actor="person:ex-1"):
        live, out, desc = self.assess_live_work()
        self.quit_actor = actor
        self._ledger("quit_requested", actor=self._person(actor), liveTurns=live,
                     outstandingEntries=out, activeDescendants=desc)
        if live or out or desc:
            self.as_state = self._t("AS-04", self.as_state, self.session)
            return {"ask": True, "liveTurns": live, "outstanding": out, "descendants": desc}
        self.as_state = self._t("AS-03", self.as_state, self.session)
        self._finish_quit()
        return {"ask": False}

    def live_work_changed(self):
        live, out, desc = self.assess_live_work()
        self.as_state = self._t("AS-07", self.as_state, self.session)
        self._ledger("quit_requested", actor=self._person(self.quit_actor), liveTurns=live,
                     outstandingEntries=out, activeDescendants=desc)

    def cancel_quit(self):
        self.as_state = self._t("AS-05", self.as_state, self.session)
        self._ledger("quit_answered", answer="cancelled", actor=self._person(self.quit_actor))

    def confirm_quit(self):
        self.as_state = self._t("AS-06", self.as_state, self.session)
        self._ledger("quit_answered", answer="confirmed", actor=self._person(self.quit_actor))
        for tid, c in list(self.convs.items()):
            if c["liveTurn"] and c["state"] == "turn-live":
                self.interrupt(tid, actor=self.quit_actor, cause="quit")
        self._finish_quit()

    def _finish_quit(self):
        self.as_state = self._t("AS-08", self.as_state, self.session)
        for home in list(self.homes):            # each App-owned home's process (L-1)
            self._stop_process(home, "app-quit")
        outcomes = [{"stopRequestId": s["stopRequestId"], "state": s["state"]}
                    for s in self.stops.values() if s["cause"] == "quit"]
        self.as_state = self._t("AS-09", self.as_state, self.session)
        self._ledger("session_ended", how="quit", stopRequests=outcomes)

    def stop_codex(self, homes=None, restart=False, actor="person:ex-1"):
        """DEL-01-04's "Stop Codex" / "Restart Codex" (C-12), after the
        person answered the live-work question (DEL-01-04 asks, using
        assess_live_work). DEF-5a for each selected home."""
        homes = list(homes or self.homes)
        live, out, desc = self.assess_live_work(homes)
        self._ledger("codex_stop", actor=self._person(actor), homes=homes, restart=restart,
                     liveTurns=live, outstandingEntries=out)
        for tid, c in list(self.convs.items()):
            if c["home"] in homes and c["liveTurn"] and c["state"] == "turn-live":
                self.interrupt(tid, actor=actor, cause="codex-stop")
        for home in homes:
            self._stop_process(home, "supplier-stop")
        if restart:
            for home in homes:
                self.start_supplier(home)

    def system_termination(self):
        self.as_state = self._t("AS-10", self.as_state, self.session)
        self._ledger("session_ended", how="system-terminated", stopRequests=[])
        for home in list(self.homes):
            self._stop_process(home, "system-termination")

    def crash(self):
        """The App process is killed: nothing more is written."""
        for h in self.homes.values():
            if h["supplier"] is not None:
                h["supplier"].end(graceful=False)
            h["hosting"] = "absent"
