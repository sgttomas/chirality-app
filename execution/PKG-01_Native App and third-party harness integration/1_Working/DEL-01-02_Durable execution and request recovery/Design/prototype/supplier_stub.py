#!/usr/bin/env python3
"""In-memory stand-in for the parts of stock Codex App Server 0.158.0 that
DEL-01-02's recovery design depends on.

Prototype only (DEL-01-02 Design, EXECUTION-AND-RECOVERY-v0.1, run
APP-V4-DESIGN-PASS-3-20261001 node D1). NOT product code, NOT an App
candidate, NOT the supplier. Python 3 standard library only; no network; the
Codex binary is never started.

Every behaviour here is CONSTRUCTED from the generated protocol types at
0.158.0 (ThreadStatus, TurnStatus, turn/interrupt, thread/resume, thread/read,
thread/turns/list, serverRequest/resolved, thread/closed, Thread.parentThreadId)
and from the design's assumptions. Where the supplier's live behaviour is not
observed (OBS-2 pending: O-1, O-2, O-3, O-4), the stub offers VARIANTS so that
each designed case can be run under every plausible answer. A case passing
under all variants shows that the design's labels stay truthful whichever
answer OBS-2 returns; it shows nothing about which answer is true.

Content strings are invented. The marker CONTENT_MARKER is placed in every
message, command and request payload so that the runner can check that the
App-kept ledger never copies conversation content (R17-4).
"""
import copy

CONTENT_MARKER = "INVENTED-CONTENT-7f3a"

# Variant axes (all OBS-2 pending; values are constructed possibilities).
VARIANTS = {
    # O-1: what turn/interrupt does
    "interrupt": ["interrupted", "completes-first", "no-response", "error"],
    # O-1: what happens to a pending request in the interrupted turn
    "pending_on_interrupt": ["resolved-by-supplier", "stays-pending"],
    # O-2: what Codex's history shows for a turn live when the process ended
    "persisted_after_exit": ["interrupted", "inProgress", "missing-turn"],
    # O-2: whether a request pending at process end is raised again on resume
    "reraise_on_resume": [False, True],
    # O-4: whether a delegated child thread keeps running after the parent's
    # turn is interrupted
    "child_after_interrupt": ["stops", "survives"],
}

DEFAULT_VARIANT = {
    "interrupt": "interrupted",
    "pending_on_interrupt": "resolved-by-supplier",
    "persisted_after_exit": "interrupted",
    "reraise_on_resume": False,
    "child_after_interrupt": "stops",
}


class Store:
    """Codex's on-disk thread history (survives process ends). Only what the
    generated types say a read returns: thread metadata, turns with status and
    items. Constructed."""

    def __init__(self):
        self.threads = {}  # tid -> {"parent": tid|None, "turns": [turn dicts]}
        self.pending = {}  # tid -> list of request dicts pending at process end

    def snapshot(self):
        return copy.deepcopy(self.threads)


class SupplierProcess:
    """One generation of the supplier child. Delivers frames to `sink`
    (the App's main-process boundary) synchronously, in order."""

    def __init__(self, store, sink, variant, generation):
        self.store = store
        self.sink = sink
        self.v = dict(DEFAULT_VARIANT)
        self.v.update(variant or {})
        self.g = generation
        self.alive = True
        self.loaded = {}       # tid -> {"status": ThreadStatus dict}
        self.requests = {}     # request id -> dict
        self._rid = 0
        self._iid = 0
        self.writes = []       # every App->supplier frame (for checks)

    # ---- helpers -------------------------------------------------------
    def _emit(self, method, params):
        if self.alive:
            self.sink(self.g, {"method": method, "params": params})

    def _respond(self, rid, result=None, error=None):
        if self.alive:
            frame = {"id": rid}
            if error is not None:
                frame["error"] = error
            else:
                frame["result"] = result if result is not None else {}
            self.sink(self.g, frame)

    def _turn(self, tid, turn_id):
        for t in self.store.threads[tid]["turns"]:
            if t["id"] == turn_id:
                return t
        return None

    def _set_status(self, tid, status):
        self.loaded.setdefault(tid, {})["status"] = status
        self._emit("thread/status/changed", {"threadId": tid, "status": status})

    # ---- App -> supplier ----------------------------------------------
    def write(self, frame):
        """Returns False when the write fails (process gone)."""
        if not self.alive:
            return False
        self.writes.append(copy.deepcopy(frame))
        method = frame.get("method")
        if method is None:          # a reply to a server request
            self._on_reply(frame)
            return True
        handler = getattr(self, "_m_" + method.replace("/", "_"), None)
        if handler is None:
            self._respond(frame["id"], error={"code": -32600,
                                              "message": "Invalid request: unknown variant"})
        else:
            handler(frame["id"], frame.get("params", {}))
        return True

    def _m_thread_start(self, rid, p):
        tid = "thr-%s-%d" % (self.g, len(self.store.threads) + 1)
        self.store.threads[tid] = {"parent": None, "turns": []}
        self.loaded[tid] = {"status": {"type": "idle"}}
        self._respond(rid, {"thread": {"id": tid, "status": {"type": "idle"},
                                       "parentThreadId": None, "turns": []}})
        self._emit("thread/started", {"thread": {"id": tid, "parentThreadId": None}})

    def spawn_child(self, parent_tid):
        """A delegated child thread the agent starts (Thread.parentThreadId;
        constructed: delegation is experimental at 0.158.0, K-5)."""
        ctid = "thr-%s-%d" % (self.g, len(self.store.threads) + 1)
        self.store.threads[ctid] = {"parent": parent_tid, "turns": []}
        self.loaded[ctid] = {"status": {"type": "idle"}}
        self._emit("thread/started", {"thread": {"id": ctid, "parentThreadId": parent_tid}})
        turn_id = "turn-%s-c%d" % (self.g, len(self.store.threads))
        self.store.threads[ctid]["turns"].append({"id": turn_id, "status": "inProgress", "items": []})
        self._set_status(ctid, {"type": "active", "activeFlags": []})
        self._emit("turn/started", {"threadId": ctid, "turn": {"id": turn_id, "status": "inProgress"}})
        return ctid, turn_id

    def report_system_error(self, tid):
        self._set_status(tid, {"type": "systemError"})

    def report_idle(self, tid):
        self._set_status(tid, {"type": "idle"})

    def close_thread(self, tid):
        self.loaded.pop(tid, None)
        self._emit("thread/closed", {"threadId": tid})

    def _m_thread_resume(self, rid, p):
        tid = p["threadId"]
        if tid not in self.store.threads:
            self._respond(rid, error={"code": -32602, "message": "thread not found"})
            return
        self.loaded[tid] = {"status": {"type": "idle"}}
        self._respond(rid, {"thread": {"id": tid, "status": {"type": "idle"}, "turns": []},
                            "turnsBackwardsCursor": None, "itemsBackwardsCursor": None})
        if self.v["reraise_on_resume"]:
            for req in self.store.pending.pop(tid, []):
                self.raise_request(tid, req["turnId"], req["itemId"], req["method"])

    def _m_thread_read(self, rid, p):
        tid = p["threadId"]
        if tid not in self.store.threads:
            self._respond(rid, error={"code": -32602, "message": "thread not found"})
            return
        status = self.loaded.get(tid, {}).get("status", {"type": "notLoaded"})
        self._respond(rid, {"thread": {"id": tid, "status": status, "turns": [],
                                       "parentThreadId": self.store.threads[tid]["parent"]}})

    def _m_thread_turns_list(self, rid, p):
        tid = p["threadId"]
        if tid not in self.store.threads:
            self._respond(rid, error={"code": -32602, "message": "thread not found"})
            return
        turns = [{"id": t["id"], "status": t["status"], "items": [],
                  "itemsView": "notLoaded"} for t in self.store.threads[tid]["turns"]]
        turns.reverse()  # descending, as the generated default says
        self._respond(rid, {"data": turns, "nextCursor": None})

    def _m_turn_start(self, rid, p):
        tid = p["threadId"]
        turn_id = "turn-%s-%d" % (self.g, sum(len(t["turns"]) for t in self.store.threads.values()) + 1)
        turn = {"id": turn_id, "status": "inProgress", "items": []}
        self.store.threads[tid]["turns"].append(turn)
        self._respond(rid, {"turn": {"id": turn_id, "status": "inProgress", "items": []}})
        self._set_status(tid, {"type": "active", "activeFlags": []})
        self._emit("turn/started", {"threadId": tid, "turn": {"id": turn_id, "status": "inProgress"}})
        # one agent message item, carrying invented content
        self.add_item(tid, turn_id, "agentMessage", text="%s message" % CONTENT_MARKER, complete=True)

    def _m_turn_interrupt(self, rid, p):
        tid, turn_id = p["threadId"], p["turnId"]
        turn = self._turn(tid, turn_id)
        mode = self.v["interrupt"]
        if turn is None or turn["status"] != "inProgress":
            self._respond(rid, error={"code": -32602, "message": "no active turn"})
            return
        if mode == "error":
            self._respond(rid, error={"code": -32603, "message": "interrupt failed (constructed)"})
            return
        if mode == "no-response":
            return  # nothing until the process ends
        if mode == "completes-first":
            self._complete_open_items(tid, turn_id)
            self._finish_turn(tid, turn_id, "completed")
            self._respond(rid, {})
            return
        # "interrupted"
        self._respond(rid, {})
        self._settle_pending_on_interrupt(tid, turn_id)
        self._finish_turn(tid, turn_id, "interrupted")
        self._children_after_interrupt(tid)

    # ---- supplier-initiated -------------------------------------------
    def add_item(self, tid, turn_id, item_type, text=None, complete=False):
        self._iid += 1
        item_id = "item-%s-%d" % (self.g, self._iid)
        item = {"id": item_id, "type": item_type, "status": "inProgress"}
        if text is not None:
            item["text"] = text
        self._turn(tid, turn_id)["items"].append(item)
        self._emit("item/started", {"threadId": tid, "turnId": turn_id, "item": dict(item)})
        if complete:
            self.complete_item(tid, turn_id, item_id)
        return item_id

    def complete_item(self, tid, turn_id, item_id):
        for it in self._turn(tid, turn_id)["items"]:
            if it["id"] == item_id:
                it["status"] = "completed"
                self._emit("item/completed", {"threadId": tid, "turnId": turn_id, "item": dict(it)})

    def _complete_open_items(self, tid, turn_id):
        for it in self._turn(tid, turn_id)["items"]:
            if it["status"] == "inProgress":
                self.complete_item(tid, turn_id, it["id"])

    def _finish_turn(self, tid, turn_id, status):
        self._turn(tid, turn_id)["status"] = status
        self._set_status(tid, {"type": "idle"})
        self._emit("turn/completed", {"threadId": tid, "turn": {"id": turn_id, "status": status}})

    def finish_turn(self, tid, turn_id, status="completed"):
        self._complete_open_items(tid, turn_id)
        self._finish_turn(tid, turn_id, status)

    def raise_request(self, tid, turn_id, item_id, method):
        self._rid += 1
        rid = "sr-%s-%d" % (self.g, self._rid)
        params = {"threadId": tid, "turnId": turn_id, "itemId": item_id,
                  "command": "%s cmd" % CONTENT_MARKER}
        self.requests[rid] = {"threadId": tid, "turnId": turn_id, "itemId": item_id,
                              "method": method, "open": True}
        flag = "waitingOnUserInput" if method == "item/tool/requestUserInput" else "waitingOnApproval"
        self._set_status(tid, {"type": "active", "activeFlags": [flag]})
        self.sink(self.g, {"id": rid, "method": method, "params": params})
        return rid

    def _on_reply(self, frame):
        req = self.requests.get(frame["id"])
        if req is None or not req["open"]:
            return
        req["open"] = False
        self._emit("serverRequest/resolved", {"threadId": req["threadId"], "requestId": frame["id"]})
        self._set_status(req["threadId"], {"type": "active", "activeFlags": []})

    def _settle_pending_on_interrupt(self, tid, turn_id):
        if self.v["pending_on_interrupt"] != "resolved-by-supplier":
            return
        for rid, req in self.requests.items():
            if req["open"] and req["threadId"] == tid and req["turnId"] == turn_id:
                req["open"] = False
                self._emit("serverRequest/resolved", {"threadId": tid, "requestId": rid})

    def _children_after_interrupt(self, tid):
        if self.v["child_after_interrupt"] != "stops":
            return
        for ctid, th in self.store.threads.items():
            if th["parent"] == tid:
                for t in th["turns"]:
                    if t["status"] == "inProgress":
                        self._finish_turn(ctid, t["id"], "interrupted")

    def raise_unknown_request(self, method="example/unknownKind"):
        self._rid += 1
        rid = "sr-%s-%d" % (self.g, self._rid)
        self.sink(self.g, {"id": rid, "method": method, "params": {}})
        return rid

    # ---- process end --------------------------------------------------
    def end(self):
        """The process ends (stop or crash). What Codex's history then shows
        for a live turn follows the variant (O-2)."""
        if not self.alive:
            return
        self.alive = False
        mode = self.v["persisted_after_exit"]
        for tid, th in self.store.threads.items():
            for t in list(th["turns"]):
                if t["status"] == "inProgress":
                    if mode == "interrupted":
                        t["status"] = "interrupted"
                    elif mode == "missing-turn":
                        th["turns"].remove(t)
                    # "inProgress": left as written
        for rid, req in self.requests.items():
            if req["open"]:
                self.store.pending.setdefault(req["threadId"], []).append(dict(req))
        self.loaded = {}
