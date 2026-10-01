#!/usr/bin/env python3
"""Executable model of DEL-01-02's recovery design
(EXECUTION_AND_RECOVERY.md, DEL-01-02/EXECUTION-AND-RECOVERY-v0.1).

Prototype only (run APP-V4-DESIGN-PASS-3-20261001, node D1). NOT product
code, NOT an App candidate, NOT the OI-008 O-1 proposal realized. It models
the five transition tables of the Design file (AS, CV, OA, SR, RQ) on top of a
minimal stand-in for the DEL-01-01 boundary's seam S-1 (generations, a
register of server requests, client requests), driving supplier_stub.py.

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

from supplier_stub import SupplierProcess

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


class TransitionRefused(Exception):
    pass


class Clock:
    def __init__(self, start=0):
        self.n = start

    def now(self):
        self.n += 1
        s, ms = divmod(self.n, 1000)
        return "2026-10-01T%02d:%02d:%02d.%03dZ" % (9 + s // 3600, (s // 60) % 60, s % 60, ms)


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


class AppSession:
    """One run of the App process. `store` is Codex's on-disk history and the
    ledger is the App-kept record; both survive. Everything else is memory
    and ends with the process."""

    def __init__(self, store, ledger_path, session_no, variant=None):
        self.store = store
        self.ledger = Ledger(ledger_path)
        self.session = "sess-%d" % session_no
        self.variant = variant or {}
        self.clock = Clock(session_no * 100000)
        self.trace = []             # (table id, subject)
        self.events = []            # custody events (recovery.custody-event)
        self.ledger_written = []    # ledger entries written by this session
        self.stops = {}
        self.convs = {}
        self.children = {}          # child thread id -> {"parent", "liveTurn"}
        self.register = {}
        self.journal = {}
        self.observers = {}
        self.pending = {}
        self.told = []
        self.hang_reads = False
        self._buf, self._in_write = [], False
        self.closed_gens = set()
        self._cid = self._gn = self._sid = self._eid = 0
        self.g, self.supplier, self.hosting = None, None, "absent"
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
            self._event("app_restart_interruption", threadId=tid, priorSession=prev,
                        priorSessionEnd=self.prev_reading, liveTurnsAtEnd=turns)
        for tid, e in index.items():
            last = e["lastObservedExecution"]
            conv = self._conv(tid, e["project"], e["tags"])
            if last["state"] in unsettled or last.get("liveTurn"):
                conv["state"] = self._t("CV-19", "—", tid)
                if last.get("liveTurn"):
                    conv["lostTurn"] = last["liveTurn"]
                    conv["lostCause"] = last.get("lostCause") or (
                        "app-quit" if self.prev_reading == "quit-with-live-work" else "app-ended-without-record")
            else:
                conv["state"] = self._t("CV-20", "—", tid)
        # stop requests of the previous session that never settled: their generation is closed
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

    def _conv(self, tid, project="project:ex-1", tags=None):
        c = self.convs.get(tid)
        if c is None:
            c = {"state": None, "liveTurn": None, "flags": [], "project": project,
                 "tags": list(tags or []), "inflight": {}, "loadedIn": None,
                 "lostTurn": None, "lostCause": None}
            self.convs[tid] = c
        return c

    def _index(self, tid):
        c = self.convs[tid]
        ex = {"state": c["state"], "at": self.clock.now()}
        live = c["liveTurn"] or (c["lostTurn"] if c["state"] in ("observation-lost", "recovery-pending") else None)
        if live:
            ex["liveTurn"] = live
        if c["lostCause"] and c["state"] in ("observation-lost", "recovery-pending"):
            ex["lostCause"] = c["lostCause"]
        body = {"threadId": tid, "project": c["project"], "tags": c["tags"], "lastObservedExecution": ex}
        if c["loadedIn"]:
            body["lastLoadedGeneration"] = c["loadedIn"]
        self._ledger("conversation_index", **body)

    # ---- the DEL-01-01 seam stand-in (generations, frames) --------------
    def start_supplier(self):
        self._gn += 1
        self.g = "%s/g%d" % (self.session, self._gn)
        self.journal[self.g] = []
        self.supplier = SupplierProcess(self.store, self._sink, self.variant, self.g)
        self.hosting = "ready"
        self._ledger("lifecycle_ref", generation=self.g, transition="LT-09", state="ready")
        for tid, c in list(self.convs.items()):
            if c["state"] == "observation-lost":
                c["state"] = self._t("CV-11", c["state"], tid)
                self._recover(tid)
            elif c["state"] == "recovery-pending":
                c["state"] = self._t("CV-12", c["state"], tid)
                self._recover(tid)

    def _write(self, frame):
        if self.supplier is None or self.hosting != "ready":
            return False
        self._in_write = True
        try:
            return self.supplier.write(frame)
        finally:
            self._in_write = False

    def _drain(self):
        while self._buf:
            g, fr = self._buf.pop(0)
            self._process(g, fr)

    def _send(self, method, params, cb=None):
        self._cid += 1
        cid = "cr-%s-%d" % (self.g, self._cid)
        if cb:
            self.pending[cid] = cb
        ok = self._write({"id": cid, "method": method, "params": params})
        if not ok:
            self.pending.pop(cid, None)
        self._drain()
        return cid, ok

    def _sink(self, g, frame):
        if self._in_write:
            self._buf.append((g, frame))
        else:
            self._process(g, frame)

    def _process(self, g, frame):
        if g != self.g:
            return  # H5: nothing crosses generations
        if "method" not in frame:
            cb = self.pending.pop(frame["id"], None)
            if cb:
                cb(frame)
            return
        pos = len(self.journal[g]) and self.journal[g][-1][0]
        pos += 1
        self.journal[g].append((pos, frame))
        if len(self.journal[g]) > JOURNAL_RETENTION:
            self.journal[g].pop(0)
        for ob in self.observers.values():
            if ob["state"] == "attached":
                ob["received"].append((g, pos))
                ob["position"] = (g, pos)
        if "id" in frame:
            self._on_server_request(frame)
        else:
            self._on_notification(frame["method"], frame["params"])

    # ---- notifications → CV, SR, RQ ---------------------------------------
    def _on_notification(self, m, p):
        if m == "thread/started" and p["thread"].get("parentThreadId"):
            self.children[p["thread"]["id"]] = {"parent": p["thread"]["parentThreadId"], "liveTurn": None}
            return
        tid = p.get("threadId")
        if tid in self.children:
            if m == "turn/started":
                self.children[tid]["liveTurn"] = p["turn"]["id"]
            elif m == "turn/completed":
                self.children[tid]["liveTurn"] = None
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
            for s in list(self.stops.values()):
                if s["turnId"] == turn_id and s["state"] in UNSETTLED_STOP:
                    rid = "SR-06" if status == "interrupted" else "SR-07"
                    s["state"] = self._t(rid, s["state"], s["stopRequestId"])
                    s["turnOutcome"], s["outcomeSource"] = status, "observed"
                    s["outcomeLabel"] = self._label(s["cause"], status)
                    s["descendantsActiveAtOutcome"] = self._active_children(tid)
                    s["transition"] = rid
                    self._persist_stop(s)
            stop = self._stop_for(turn_id)
            if c["state"] == "interrupt-pending":
                c["state"] = self._t("CV-06", c["state"], tid)
            elif c["state"] == "turn-live":
                c["state"] = self._t("CV-05", c["state"], tid)
            c["liveTurn"], c["flags"] = None, []
            ev = {"threadId": tid, "turnId": turn_id, "outcome": status, "source": "observed"}
            if stop is not None:
                ev["cause"], ev["stopRequest"] = stop["cause"], stop["stopRequestId"]
            children = self._active_children(tid)
            if children:
                ev["descendantsActive"] = children
            self._event("turn_outcome", **ev)
            self._index(tid)
        elif m == "serverRequest/resolved":
            e = self.register.get(p["requestId"])
            if e and e["g"] == self.g:
                if e["state"] == "listed":
                    e["endedAs"] = "resolved-by-supplier"
                    self._close_entry(e, "RQ-03")
                elif e["state"] == "closed" and e.get("replyWrite") == "written" and e.get("ack") != "observed":
                    e["ack"] = "observed"
                    self._t("RQ-09", "closed", e["requestIdentity"])
                    self._summary(e, "RQ-09")
        elif m == "thread/closed" and c and c["state"] == "loaded-idle":
            c["state"] = self._t("CV-18", c["state"], tid)
            c["loadedIn"] = None
            self._index(tid)

    @staticmethod
    def _label(cause, status):
        if cause == "quit":
            return {"interrupted": "interrupted by quit",
                    "unknown": "interrupted by quit (final status not observed)"}.get(
                        status, "%s (quit requested)" % status)
        return {"interrupted": "interrupted by the person",
                "unknown": "outcome unknown (stop requested)"}.get(status, "%s (stop requested)" % status)

    def _active_children(self, tid):
        return [{"kind": "child-thread", "ref": ct, "observedStatus": "active"}
                for ct, ch in self.children.items() if ch["parent"] == tid and ch["liveTurn"]]

    def _stop_for(self, turn_id):
        found = [s for s in self.stops.values() if s["turnId"] == turn_id]
        return found[-1] if found else None

    # ---- server requests → register stand-in + RQ ------------------------
    def _on_server_request(self, frame):
        m, rid, p = frame["method"], frame["id"], frame.get("params", {})
        e = {"g": self.g, "requestIdentity": rid, "method": m, "threadId": p.get("threadId"),
             "turnId": p.get("turnId"), "itemId": p.get("itemId")}
        self.register[rid] = e
        if m not in FAMILIAR_REQUESTS:
            # DEL-01-01's boundary writes the explicit error at receipt (HOSTING R1, R2; §6.5 split)
            ok = self._write({"id": rid, "error": {"code": -32601, "message": "unfamiliar request"}})
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

    def answer(self, rid, decision, origin="person-via-interaction"):
        """Stand-in for HOSTING §6.4 answer (DEL-01-04 calls DEL-01-01 directly)."""
        e = self.register.get(rid)
        if e is None:
            return "refused: no-such-request"
        if e["g"] != self.g or e["g"] in self.closed_gens:
            return "refused: generation-closed"
        if e.get("endedAs") == "resolved-by-supplier":
            return "refused: already-resolved"
        if e["state"] != "listed":
            return "refused: already-settled"
        if origin.startswith("app-rule:") and decision not in NEGATIVE:
            return "refused: origin-not-permitted"
        ok = self._write({"id": rid, "result": {"decision": decision}})
        e["origin"], e["replyWrite"] = origin, ("written" if ok else "write-failed")
        e["endedAs"] = ("declined" if decision in NEGATIVE else "answered") if ok else "settle-write-failed"
        self._close_entry(e, "RQ-03")
        self._drain()
        return "accepted-for-write"

    def list_outstanding(self, tid=None):
        return [e for e in self.register.values() if e["state"] == "listed"
                and (tid is None or e["threadId"] == tid)]

    # ---- operations offered (Design §4) ----------------------------------
    def new_conversation(self, project="project:ex-1", tags=None):
        result = {}
        self._send("thread/start", {}, lambda fr: result.update(fr.get("result", {})))
        tid = result["thread"]["id"]
        c = self._conv(tid, project, tags)
        c["loadedIn"] = self.g
        c["state"] = self._t("CV-21", "—", tid)
        self._index(tid)
        return tid

    def tag(self, tid, owner, value):
        """Opaque receiver tag handed at run time (for example a run
        reference). Stored and returned, never interpreted (R17-10)."""
        self.convs[tid]["tags"].append({"owner": owner, "value": value})
        self._index(tid)

    def lookup_tag(self, owner, value):
        return [tid for tid, c in self.convs.items() if {"owner": owner, "value": value} in c["tags"]]

    def send_message(self, tid):
        c = self.convs[tid]
        if c["state"] != "loaded-idle":
            return "refused: conversation not loaded (%s)" % c["state"]
        self._send("turn/start", {"threadId": tid})
        return "sent"

    def resume(self, tid):
        """The person's choice to continue a conversation; never automatic,
        and no prompt is re-sent."""
        c = self.convs[tid]
        if c["state"] != "indexed":
            return "refused: %s" % c["state"]
        result = {}
        self._send("thread/resume", {"threadId": tid}, lambda fr: result.update(fr))
        if "result" not in result:
            return "refused: %s" % result.get("error", {}).get("message", "no response")
        c["loadedIn"] = self.g
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
        self._sid += 1
        s = {"kind": "stop_request", "stopRequestId": "stop:%s:%d" % (self.session, self._sid),
             "appSession": self.session, "generation": self.g, "threadId": tid,
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
        cid = "cr-%s-%d" % (self.g, self._cid)
        self.pending[cid] = on_response
        ok = self._write({"id": cid, "method": "turn/interrupt",
                          "params": {"threadId": tid, "turnId": s["turnId"]}})
        if not ok:
            self.pending.pop(cid, None)
            s["send"] = "not-sent(write-failed)" if self.hosting == "ready" else "not-sent(not-ready)"
            s["response"] = "unknown-no-response" if self.hosting == "ready" else "not-applicable"
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
    def attach(self, name, position=None, rendered=None):
        ob = self.observers.setdefault(name, {"state": "detached", "position": None, "received": []})
        ob["stale"] = dict(rendered or {})
        kept = [p for p, _ in self.journal.get(self.g, [])] if self.g else []
        if position and position[0] == self.g and kept and kept[0] <= position[1] + 1:
            ob["state"] = self._t("OA-01", ob["state"], name)
            replay = [(self.g, p) for p in kept if p > position[1]]
            ob["received"].extend(replay)
            ob["position"] = replay[-1] if replay else position
            ob["gap"] = None
        else:
            ob["state"] = self._t("OA-02", ob["state"], name)
            ob["gap"] = "events before %s rebuilt from Codex history" % self.clock.now()
            ob["position"] = (self.g, kept[-1]) if kept else None
        ob["rendered"] = self.snapshot()      # stale rendered state establishes nothing
        return ob

    def detach(self, name):
        ob = self.observers[name]
        before = len(self.supplier.writes) if self.supplier else 0
        ob["state"] = self._t("OA-03", ob["state"], name)
        for e in self.list_outstanding():
            self._t("RQ-02", e["state"], e["requestIdentity"])
        return (len(self.supplier.writes) if self.supplier else 0) - before   # frames sent: must be 0

    def hide(self, name):
        ob = self.observers[name]
        ob["state"] = self._t("OA-04", ob["state"], name)

    def snapshot(self):
        return {tid: {"state": c["state"], "liveTurn": c["liveTurn"], "flags": list(c["flags"]),
                      "outstanding": [e["requestIdentity"] for e in self.list_outstanding(tid)]}
                for tid, c in self.convs.items()}

    # ---- generation close (supplier exit, stop, quit) ---------------------
    def close_generation(self, cause):
        g = self.g
        self.closed_gens.add(g)
        lost, live, inflight = [], [], []
        for tid, c in self.convs.items():
            if c["state"] in ("loaded-idle", "system-error", "turn-live", "interrupt-pending"):
                lost.append(tid)
                if c["liveTurn"]:
                    live.append({"threadId": tid, "turnId": c["liveTurn"]})
                    c["lostTurn"], c["lostCause"] = c["liveTurn"], cause
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
                    and e.get("endedAs") in ("answered", "declined"):
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
            self._event("observation_lost", generation=g, cause=cause, conversations=lost,
                        liveTurns=live, inFlightItems=inflight, outstandingEntries=outstanding)
        for name, ob in self.observers.items():
            if ob["state"] == "attached":
                ob["state"] = self._t("OA-05", ob["state"], name)
        for tid in lost:
            c = self.convs[tid]
            c["inflight"], c["liveTurn"], c["loadedIn"], c["flags"] = {}, None, None, []
            self._index(tid)
        for ch in self.children.values():
            ch["liveTurn"] = None
        self.pending.clear()
        self.hosting = "stopped" if cause in ("supplier-stop", "app-quit", "system-termination") else "exited"
        self._ledger("lifecycle_ref", generation=g,
                     transition="LT-23" if self.hosting == "stopped" else "LT-12", state=self.hosting)

    def supplier_exits(self):
        """Unexpected exit (HOSTING §4.3): the child ends with no stop record."""
        self.supplier.end()
        self.close_generation("supplier-exit")

    # ---- recovery reads ----------------------------------------------------
    def _recover(self, tid):
        c = self.convs[tid]
        if self.hang_reads:
            return
        res = {}
        self._send("thread/read", {"threadId": tid}, lambda fr: res.update(read=fr))
        if "result" not in res.get("read", {}):
            reason = res.get("read", {}).get("error", {}).get("message", "no response")
            c["state"] = self._t("CV-14", c["state"], tid)
            self._event("observation_recovered", threadId=tid, generation=self.g, via="thread/read",
                        priorEvents="unavailable", unavailableReason=reason, turns=[])
            self._index(tid)
            return
        self._send("thread/turns/list", {"threadId": tid}, lambda fr: res.update(turns=fr))
        statuses = {t["id"]: t["status"] for t in res["turns"]["result"]["data"]}
        recovered = []
        lost_turn = c["lostTurn"]
        if lost_turn:
            st = statuses.get(lost_turn)
            outcome = st if st in ("interrupted", "completed", "failed") else "unknown"
            if c["lostCause"] in ("app-quit", "system-termination"):
                reading = "interrupted by quit; Codex reports: %s" % (st or "no such turn")
            elif outcome != "unknown":
                reading = "recovered from Codex: %s" % st
            elif st == "inProgress":
                reading = "outcome unknown (Codex history reports inProgress for a turn whose process ended)"
            else:
                reading = "outcome unknown (turn not in Codex history)"
            recovered.append({"turnId": lost_turn, "supplierStatus": st or "absent", "appReading": reading})
            ev = {"threadId": tid, "turnId": lost_turn, "outcome": outcome,
                  "source": "recovered-from-supplier" if outcome != "unknown" else "not-observed"}
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
            self._event("turn_outcome", **ev)
        c["state"] = self._t("CV-13", c["state"], tid)
        c["lostTurn"], c["lostCause"] = None, None
        self._event("observation_recovered", threadId=tid, generation=self.g, via="thread/read",
                    priorEvents="accessible", turns=recovered)
        self._index(tid)

    def retry(self, tid):
        c = self.convs[tid]
        c["state"] = self._t("CV-15", c["state"], tid)
        self._recover(tid)

    # ---- quit (K-4) ----------------------------------------------------------
    def quit_assessment(self):
        live = [{"threadId": t, "turnId": c["liveTurn"]} for t, c in self.convs.items() if c["liveTurn"]]
        out = [self._entry_ref(e) for e in self.list_outstanding()]
        desc = [d for t, c in self.convs.items() for d in self._active_children(t)]
        return live, out, desc

    def request_quit(self, actor="person:ex-1"):
        live, out, desc = self.quit_assessment()
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
        live, out, desc = self.quit_assessment()
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
        if self.supplier is not None and self.hosting == "ready":
            self.supplier.end()
            self.close_generation("app-quit")
        outcomes = [{"stopRequestId": s["stopRequestId"], "state": s["state"]}
                    for s in self.stops.values() if s["cause"] == "quit"]
        self.as_state = self._t("AS-09", self.as_state, self.session)
        self._ledger("session_ended", how="quit", stopRequests=outcomes)

    def system_termination(self):
        self.as_state = self._t("AS-10", self.as_state, self.session)
        self._ledger("session_ended", how="system-terminated", stopRequests=[])
        if self.supplier is not None and self.hosting == "ready":
            self.supplier.end()
            self.close_generation("system-termination")

    def crash(self):
        """The App process is killed: nothing more is written."""
        if self.supplier is not None:
            self.supplier.end()
        self.hosting = "absent"
