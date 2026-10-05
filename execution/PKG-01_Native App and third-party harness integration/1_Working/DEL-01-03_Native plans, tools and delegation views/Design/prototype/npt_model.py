#!/usr/bin/env python3
"""DEL-01-03 view model: native plans, tool activity and delegation.

Prototype only (DEL-01-03 Design, NPTD-v0.2; run APP-V4-DESIGN-PASS-3-20261001,
node D2, rounds 1 and 2). Not product code, not an App candidate. Python 3 standard library.

It executes the rules of NATIVE_PLANS_TOOLS_DELEGATION.md over a stream of
native frames as the host would deliver them (HOSTING S-2: the frame
unchanged, with generation and receipt position beside it), history reads,
lifecycle events and runtime values handed in by other deliverables. It keeps
nothing across a relaunch (R17-4): `relaunch()` returns a fresh model.

Numbers and identity methods the Design file leaves open are marked
TEST VALUE.
"""
import base64
import copy
import hashlib
import json

# --- Transition tables (must equal NATIVE_PLANS_TOOLS_DELEGATION.md §13) ---
# Each row: ID -> (from, event, to)
PL_TABLE = {
    "PL-01": ("absent", "item-started", "streaming"),
    "PL-02": ("absent", "plan-delta", "streaming"),
    "PL-03": ("streaming", "plan-delta", "streaming"),
    "PL-04": ("streaming", "item-completed", "completed"),
    "PL-05": ("absent", "item-completed", "completed"),
    "PL-06": ("streaming", "turn-ended", "incomplete"),
    "PL-07": ("streaming", "generation-closed", "incomplete"),
    "PL-08": ("absent", "history-read", "completed"),
    "PL-09": ("incomplete", "history-read", "completed"),
    "PL-10": ("completed", "history-read", "completed"),
}
CL_TABLE = {
    "CL-01": ("none", "plan-updated", "live"),
    "CL-02": ("live", "plan-updated", "live"),
    "CL-03": ("live", "turn-ended", "ended"),
    "CL-04": ("ended", "plan-updated", "ended"),
    "CL-05": ("live", "generation-closed", "ended"),
    "CL-06": ("none", "history-read", "not-recoverable"),
    "CL-07": ("ended", "view-rebuilt", "not-recoverable"),
}
TI_TABLE = {
    "TI-01": ("absent", "item-started", "in-progress"),
    "TI-02": ("in-progress", "request-outstanding", "waiting-on-request"),
    "TI-03": ("waiting-on-request", "request-settled", "in-progress"),
    "TI-04": ("in-progress", "item-completed", "final"),
    "TI-05": ("waiting-on-request", "item-completed", "final"),
    "TI-06": ("absent", "item-completed", "final"),
    "TI-07": ("in-progress", "turn-ended", "not-completed"),
    "TI-08": ("waiting-on-request", "turn-ended", "not-completed"),
    "TI-09": ("in-progress", "generation-closed", "unknown"),
    "TI-10": ("waiting-on-request", "generation-closed", "unknown"),
    "TI-11": ("absent", "history-read", "final"),
    "TI-12": ("unknown", "history-read", "final"),
    "TI-13": ("absent", "history-read-in-progress", "unknown"),
    "TI-14": ("unknown", "history-turn-ended", "not-completed"),
    "TI-15": ("not-completed", "history-read", "final"),
}
DS_TABLE = {
    "DS-01": ("absent", "collab-call", "observed"),
    "DS-02": ("absent", "subagent-activity", "observed"),
    "DS-03": ("observed", "child-observation", "observed"),
    "DS-04": ("observed", "generation-closed", "observation-ended"),
    "DS-05": ("observation-ended", "thread-read", "observed"),
    "DS-06": ("observed", "not-found-reported", "not-found"),
    "DS-07": ("absent", "thread-read", "observed"),
    "DS-08": ("observation-ended", "child-observation", "observed"),
    "DS-09": ("observed", "thread-read", "observed"),
}
TABLES = {"PL": PL_TABLE, "CL": CL_TABLE, "TI": TI_TABLE, "DS": DS_TABLE}

# Final display states by native status value (TI "final"); supplier values unchanged.
FINAL_BY_STATUS = {
    "completed": "completed",
    "failed": "failed",
    "declined": "declined",
    "interrupted": "interrupted",
}
STATUS_KINDS = {"commandExecution", "fileChange", "mcpToolCall", "dynamicToolCall",
                "collabAgentToolCall", "imageGeneration"}
# Item kinds this deliverable renders as tool activity (HOSTING §8.4 Part A groups).
TOOL_KINDS = {
    "commandExecution": "HCG-A02", "fileChange": "HCG-A03", "mcpToolCall": "HCG-A05",
    "dynamicToolCall": "HCG-A06", "functionCallOutput": "HCG-A06",
    "collabAgentToolCall": "HCG-A08", "subAgentActivity": "HCG-A08",
    "webSearch": "HCG-A10", "imageView": "HCG-A11", "imageGeneration": "HCG-A11",
    "enteredReviewMode": "HCG-A12", "exitedReviewMode": "HCG-A12",
    "contextCompaction": "HCG-A13", "sleep": "HCG-A14", "hookPrompt": "HCG-A15",
}
# Result elements whose null value at completion means "result not supplied".
RESULT_ELEMENTS = {
    "commandExecution": ["aggregatedOutput", "exitCode"],
    "fileChange": ["changes"],
    "mcpToolCall": ["result", "error"],
    "dynamicToolCall": ["contentItems", "success"],
}
# Experimental-only protocol elements by variant diff at 0.158.0 that the views use (EX-1).
# Only plan mode is labelled "experimental" (R18-1 C-05); delegation is a stable surface.
EXPERIMENTAL_ELEMENTS = {"turn/start.collaborationMode", "collaborationMode/list"}
LIMIT_SHOWN = {  # K-10 standing as handed by DEL-02-04 (R18-1 C-08), shown in these words
    "stated-not-enforced": "the task role states that a task agent does not delegate (stated, not enforced)",
    "enforced-by-supplier": "enforced by Codex (mechanism named by DEL-02-04)",
    "unknown": "not known whether the supplied guidance states this",
}
GOAL_NOTE = "Codex's goal status; not a workflow run, checkpoint or acceptance"

CONTENT_METHOD = "sha256/canonical-json/npt-v0 (TEST VALUE; HOSTING U-08)"
TYPES_PIN = "0.158.0"
TYPES_MANIFEST = "42b95826d7bd6d58df7941da7420064ee55d54a347a2eab22eafbfa16231569e"
NO_MODEL = "no model selected"  # the composer (DEL-01-04) words it per R18-2
EXPORT_LIMITS = [
    "Child completion, return, review and integration are not inferred from any observation here.",
    "A parent turn's completion says nothing about its children.",
    "Status values are the last observed value from the named source at the named time.",
    "Identities are Codex's; this export is App-observed, not authority for what Codex holds.",
]


def content_identity(obj):
    canon = json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return {"method": CONTENT_METHOD, "value": hashlib.sha256(canon.encode("utf-8")).hexdigest()}


class TransitionRefused(Exception):
    pass


def generation_key(g):
    """Closed H5 identity: no legacy scalar, implicit scope or bool counter."""
    if not isinstance(g, dict) or set(g) != {"appSession", "home", "spawnCounter"}:
        raise TransitionRefused("generation must carry the complete H5 identity")
    if any(not isinstance(g[k], str) or not g[k] for k in ("appSession", "home")):
        raise TransitionRefused("generation session/home must be nonempty strings")
    if type(g["spawnCounter"]) is not int or g["spawnCounter"] < 1:
        raise TransitionRefused("spawn counter must be a positive integer")
    return (g["appSession"], g["home"], g["spawnCounter"])


def generation_object(key):
    return dict(zip(("appSession", "home", "spawnCounter"), key))


def revision_key(kind, thread, turn, item=None, generation=None, position=None):
    """Operational, lossless component encoding; independent of content identity U-08."""
    def enc(value):
        return base64.urlsafe_b64encode(value.encode("utf-8")).decode("ascii").rstrip("=")
    if kind == "pi":
        parts = [enc(thread), enc(turn), enc(item)]
    else:
        session, home, counter = generation_key(generation)
        parts = [enc(session), enc(home), str(counter), enc(thread), enc(turn), str(position)]
    return kind + ":v2:" + ".".join(parts)


def reference_identity_matches(reference):
    """Semantic component check additional to JSON Schema shape checks."""
    try:
        if reference["kind"] == "plan-item":
            expected = revision_key("pi", reference["threadId"], reference["turnId"], reference["itemId"])
        elif reference["kind"] == "checklist":
            expected = revision_key("cl", reference["threadId"], reference["turnId"],
                                    generation=reference["generation"], position=reference["receiptPosition"])
        else:
            return False
        return reference["revisionId"] == expected
    except (KeyError, TypeError, AttributeError, TransitionRefused):
        return False


class Model:
    def __init__(self, home=None):
        if home is not None and (not isinstance(home, str) or not home):
            raise ValueError("view home must be a nonempty App-owned identity")
        self.home = home
        self.g = None
        self.ready = {}                    # g -> ready(g) record
        self.closed = set()
        self.scope = None                  # immutable (appSession, home) for this view instance
        self.last_position = {}            # complete generation key -> last receipt position
        self.plan_items = {}               # (thread, turn, item) -> dict
        self.plan_order = {}               # thread -> [item keys in completion order]
        self.checklists = {}               # (thread, turn) -> dict(state, revisions)
        self.turn_order = {}               # thread -> [turn ids as first seen]
        self.tools = {}                    # (thread, item) -> dict
        self.nodes = {}                    # child thread -> node
        self.limits = {}                   # thread -> K-10 label {role, limitId, standing} (runtime value, DEL-02-04 ROLE O-6)
        self.goals = {}                    # thread -> {goal, source, at, turnId}
        self.run_markers = {}              # thread -> [(turnId, kind, label)] (runtime value; R19-2)
        self.model_selection = {}          # thread -> model or None (runtime value, DEL-01-05)
        self.mode_list = None              # last collaborationMode/list result
        self.features = None               # last experimentalFeature/list result
        self.acts = []                     # supplied act records (runtime values)
        self.used = set()                  # transition IDs used
        self.refused = []                  # (table, from, event) refused
        self.turn_status = {}              # (thread, turn) -> native turn status

    # ---------- transitions ----------
    def _step(self, table, frm, event):
        for rid, (f, e, t) in TABLES[table].items():
            if f == frm and e == event:
                self.used.add(rid)
                return rid, t
        self.refused.append((table, frm, event))
        raise TransitionRefused("%s: no row from %s on %s" % (table, frm, event))

    def _try(self, table, frm, event):
        try:
            return self._step(table, frm, event)
        except TransitionRefused:
            return None, frm

    # ---------- inputs ----------
    def apply(self, ev):
        kind = ev["ev"]
        if kind == "ready":
            g = generation_key(ev["g"])
            if g in self.closed:
                raise TransitionRefused("ready of closed generation")
            if self.scope is not None and g[:2] != self.scope:
                raise TransitionRefused("ready outside this view's session/home")
            if self.g is not None and self.g != g and self.g not in self.closed:
                raise TransitionRefused("active generation must close before replacement")
            if g in self.ready:
                raise TransitionRefused("duplicate ready generation")
            if self.home is not None and self.home != g[1]:
                raise TransitionRefused("ready outside this view's owning home")
            self.home = g[1]
            self.scope = g[:2]
            self.g = g
            self.ready[g] = copy.deepcopy(ev["record"])
            self._rebuild_after_close()
        elif kind == "closed":
            self._generation_closed(ev["g"])
        elif kind == "frame":
            self._frame(ev["g"], ev["pos"], ev["frame"])
        elif kind == "read":
            self._read(ev)
        elif kind == "runtime":
            self._runtime(ev)
        elif kind == "mode-list":
            self.mode_list = ev["result"]
        elif kind == "feature-list":
            self.features = ev["result"]
        else:
            raise ValueError("unknown input " + kind)

    def _rebuild_after_close(self):
        """C-03 (R18-1): after a generation closed, views rebuild from Codex history; checklist
        revisions of the closed generation are not recoverable, as after a relaunch."""
        for cl in self.checklists.values():
            if cl["state"] == "ended" and any(generation_key(r["generation"]) in self.closed for r in cl["revisions"]):
                _, cl["state"] = self._step("CL", "ended", "view-rebuilt")
                cl["revisions"] = []

    def _note_turn(self, thread, turn):
        order = self.turn_order.setdefault(thread, [])
        if turn not in order:
            order.append(turn)

    def _frame(self, g, pos, frame):
        g = generation_key(g)
        if g in self.closed:
            raise TransitionRefused("frame of closed generation %s" % (g,))
        if g != self.g or g not in self.ready:
            raise TransitionRefused("frame outside the ready generation")
        if type(pos) is not int or pos < 0 or pos <= self.last_position.get(g, -1):
            raise TransitionRefused("receipt position must increase within the complete generation")
        self.last_position[g] = pos
        m = frame.get("method")
        p = frame.get("params", {})
        thread = p.get("threadId")
        if thread in self.nodes:
            self._child_observation(thread, m, p, frame.get("emittedAtMs"))
        if m == "turn/started":
            self._note_turn(thread, p["turn"]["id"])
        elif m == "turn/plan/updated":
            self._note_turn(thread, p["turnId"])
            self._checklist_update(g, pos, p)
        elif m == "item/plan/delta":
            self._plan_delta(p)
        elif m in ("item/started", "item/completed"):
            self._note_turn(thread, p["turnId"])
            item = p["item"]
            t = item["type"]
            if t == "plan":
                self._plan_item(m, p)
            if t in TOOL_KINDS:
                self._tool(m, p, frame.get("emittedAtMs"))
            if t in ("collabAgentToolCall", "subAgentActivity"):
                self._delegation_item(p, frame.get("emittedAtMs"))
        elif m == "turn/completed":
            self._turn_ended(thread, p["turn"]["id"], p["turn"]["status"])
        elif m == "thread/goal/updated":
            self.goals[thread] = {"goal": p["goal"], "source": m, "turnId": p.get("turnId"),
                                  "at": frame.get("emittedAtMs")}
        elif m == "thread/goal/cleared":
            self.goals[thread] = {"goal": None, "source": m, "turnId": None, "at": frame.get("emittedAtMs")}

    # ---------- plans ----------
    def _checklist_update(self, g, pos, p):
        key = (p["threadId"], p["turnId"])
        cl = self.checklists.setdefault(key, {"state": "none", "revisions": []})
        if cl["state"] == "not-recoverable":
            # New live observations start a new sequence; history never restores the old one.
            cl = self.checklists[key] = {"state": "none", "revisions": []}
        rid, cl["state"] = self._step("CL", cl["state"], "plan-updated")
        content = {"explanation": p.get("explanation"), "plan": p["plan"]}
        prev = cl["revisions"][-1] if cl["revisions"] else None
        cid = content_identity({"kind": "checklist", **content})
        cl["revisions"].append({
            "revisionId": revision_key("cl", key[0], key[1], generation=generation_object(g), position=pos),
            "kind": "checklist", "threadId": key[0], "turnId": key[1],
            "generation": generation_object(g), "receiptPosition": pos,
            "ordinal": len(cl["revisions"]) + 1,
            "content": {"explanation": p.get("explanation"),
                        "steps": [{"step": s["step"], "status": s["status"]} for s in p["plan"]]},
            "contentIdentity": cid,
            "unchangedFromPrevious": bool(prev and prev["contentIdentity"] == cid),
            "afterTurnEnd": rid == "CL-04",
            "standing": "live-observed",
            "typesPin": TYPES_PIN,
        })

    def _plan_delta(self, p):
        key = (p["threadId"], p["turnId"], p["itemId"])
        pi = self.plan_items.setdefault(key, {"state": "absent", "turnId": p["turnId"],
                                              "preview": "", "startObserved": False})
        _, pi["state"] = self._step("PL", pi["state"], "plan-delta")
        pi["preview"] += p["delta"]

    def _plan_item(self, m, p):
        item = p["item"]
        key = (p["threadId"], p["turnId"], item["id"])
        pi = self.plan_items.setdefault(key, {"state": "absent", "turnId": p["turnId"],
                                              "preview": "", "startObserved": False})
        if m == "item/started":
            _, pi["state"] = self._step("PL", pi["state"], "item-started")
            pi["startObserved"] = True
        else:
            _, pi["state"] = self._step("PL", pi["state"], "item-completed")
            pi["text"] = item["text"]
            pi["deltasDiffered"] = bool(pi["preview"]) and pi["preview"] != item["text"]
            pi["standing"] = "live-observed"
            self.plan_order.setdefault(p["threadId"], []).append(key)

    def plan_revisions(self, thread):
        out = []
        for i, key in enumerate(self.plan_order.get(thread, []), 1):
            pi = self.plan_items[key]
            out.append({
                "revisionId": revision_key("pi", thread, pi["turnId"], key[2]),
                "kind": "plan-item", "threadId": thread, "turnId": pi["turnId"],
                "itemId": key[2], "ordinal": i,
                "content": {"text": pi["text"]},
                "contentIdentity": content_identity({"kind": "plan-item", "text": pi["text"]}),
                "standing": pi["standing"],
                "typesPin": TYPES_PIN,
            })
        return out

    def checklist_revisions(self, thread, turn):
        return copy.deepcopy(self.checklists.get((thread, turn), {}).get("revisions", []))

    def checklist_state(self, thread, turn):
        return self.checklists.get((thread, turn), {"state": "none"})["state"]

    # ---------- tool activity ----------
    def _tool(self, m, p, at):
        item = p["item"]
        key = (p["threadId"], item["id"])
        row = self.tools.setdefault(key, {"state": "absent", "kind": item["type"],
                                          "group": TOOL_KINDS[item["type"]],
                                          "turnId": p["turnId"], "observations": []})
        row["observations"].append({"method": m, "status": item.get("status"),
                                    "source": item.get("source"), "at": at})
        if m == "item/started":
            _, row["state"] = self._step("TI", row["state"], "item-started")
            row["sourceAtStart"] = item.get("source")
        else:
            _, final = self._step("TI", row["state"], "item-completed")
            row["state"] = self._final(item)
            row["item"] = item
            row["sourceAtCompletion"] = item.get("source")
        row.setdefault("item", item)

    def _final(self, item):
        if item["type"] in STATUS_KINDS and item["type"] != "imageGeneration":
            return FINAL_BY_STATUS.get(item["status"], "unknown")
        return "completed"

    def tool_row(self, thread, item_id):
        row = self.tools[(thread, item_id)]
        item = row["item"]
        out = {
            "anchor": {"anchorKind": "item", "threadId": thread, "turnId": row["turnId"],
                       "itemId": item_id, "nativeKind": row["kind"],
                       "displayState": row["state"],
                       "standing": row.get("standing", "live-observed")},
            "group": row["group"],
            "nativeStatus": item.get("status"),
            "displayState": row["state"],
            "native": item,                      # carried unchanged (no translation)
        }
        if row["state"] == "not-completed":
            out["result"] = "not completed (turn ended)"
        elif row["state"] in ("completed", "failed", "declined", "interrupted"):
            missing = [e for e in RESULT_ELEMENTS.get(row["kind"], []) if item.get(e) is None]
            elems = RESULT_ELEMENTS.get(row["kind"], [])
            out["result"] = ("not supplied by Codex" if elems and len(missing) == len(elems)
                             else "supplied" if elems else "no result element in this item kind")
        else:
            out["result"] = "unknown" if row["state"] == "unknown" else "pending"
        if "sourceAtStart" in row or "sourceAtCompletion" in row:
            out["source"] = {"atStart": row.get("sourceAtStart"),
                             "atCompletion": row.get("sourceAtCompletion")}
        if row.get("request"):
            out["request"] = row["request"]      # as the register supplies it
        return out

    # ---------- turns and generations ----------
    def _turn_ended(self, thread, turn, status):
        self.turn_status[(thread, turn)] = status
        for (th, native_turn, iid), pi in self.plan_items.items():
            if th == thread and pi["turnId"] == turn and pi["state"] == "streaming":
                _, pi["state"] = self._step("PL", "streaming", "turn-ended")
        cl = self.checklists.get((thread, turn))
        if cl and cl["state"] == "live":
            _, cl["state"] = self._step("CL", "live", "turn-ended")
        for (th, iid), row in self.tools.items():
            if th == thread and row["turnId"] == turn and row["state"] in ("in-progress", "waiting-on-request"):
                _, row["state"] = self._step("TI", row["state"], "turn-ended")
        # Deliberately no descendant transition: a parent turn's end changes no child (AC-003).

    def _generation_closed(self, g):
        g = generation_key(g)
        if g in self.closed:
            return  # repeat closure cannot end a successor's observations
        if g != self.g or g not in self.ready:
            raise TransitionRefused("closure outside the ready generation")
        self.closed.add(g)
        for pi in self.plan_items.values():
            if pi["state"] == "streaming":
                _, pi["state"] = self._step("PL", "streaming", "generation-closed")
        for cl in self.checklists.values():
            if cl["state"] == "live":
                _, cl["state"] = self._step("CL", "live", "generation-closed")
                cl["observationEnded"] = True
        for row in self.tools.values():
            if row["state"] in ("in-progress", "waiting-on-request"):
                _, row["state"] = self._step("TI", row["state"], "generation-closed")
        for node in self.nodes.values():
            if node["state"] == "observed":
                _, node["state"] = self._step("DS", "observed", "generation-closed")
                node["observationEnded"] = True

    # ---------- history reads (after relaunch or on demand) ----------
    def _read(self, ev):
        # Receiving context is beside the unchanged Codex response, never a native field.
        if self.home is None or ev.get("home") != self.home:
            raise TransitionRefused("history source does not match this view's owning home")
        m = ev["method"]
        if m == "thread/items/list":
            thread = ev["params"]["threadId"]
            for entry in ev["result"]["data"]:
                self._history_item(thread, entry["turnId"], entry["item"], ev["at"])
        elif m == "thread/turns/list":
            thread = ev["params"]["threadId"]
            for turn in ev["result"]["data"]:
                self._note_turn(thread, turn["id"])
                self.turn_status[(thread, turn["id"])] = turn["status"]
                key = (thread, turn["id"])
                cl = self.checklists.setdefault(key, {"state": "none", "revisions": []})
                if cl["state"] == "none":
                    _, cl["state"] = self._step("CL", "none", "history-read")
                if turn["status"] != "inProgress":
                    for (th, iid), row in self.tools.items():
                        if th == thread and row["turnId"] == turn["id"] and row["state"] == "unknown":
                            _, row["state"] = self._step("TI", "unknown", "history-turn-ended")
                            row["standing"] = "recovered-from-supplier"
                            row["note"] = "turn %s in Codex history; item not completed" % turn["status"]
        elif m == "thread/read":
            self._thread_read(ev["result"]["thread"], ev["at"])
        elif m == "thread/goal/get":
            self.goals[ev["params"]["threadId"]] = {"goal": ev["result"].get("goal"), "source": m,
                                                    "turnId": None, "at": ev["at"]}
        else:
            raise ValueError("unsupported read " + m)

    def _history_item(self, thread, turn, item, at):
        self._note_turn(thread, turn)
        t = item["type"]
        if t == "plan":
            key = (thread, turn, item["id"])
            pi = self.plan_items.setdefault(key, {"state": "absent", "turnId": turn,
                                                  "preview": "", "startObserved": False})
            before = pi["state"]
            _, pi["state"] = self._step("PL", before, "history-read")
            if before == "completed" and pi.get("text") != item["text"]:
                pi["liveDifferedFromHistory"] = True
            pi["text"] = item["text"]
            if before != "completed":
                pi["standing"] = "recovered-from-supplier"
                self.plan_order.setdefault(thread, []).append(key)
        if t in TOOL_KINDS:
            key = (thread, item["id"])
            row = self.tools.setdefault(key, {"state": "absent", "kind": t, "group": TOOL_KINDS[t],
                                              "turnId": turn, "observations": []})
            ended = self.turn_status.get((thread, turn)) not in (None, "inProgress")
            if item.get("status") == "inProgress":
                if row["state"] == "absent":
                    _, row["state"] = self._step("TI", "absent", "history-read-in-progress")
                    row["unknownReason"] = ("turn ended without a completion" if ended
                                            else "in progress at the read")
            elif row["state"] in ("absent", "unknown", "not-completed"):
                _, _ = self._step("TI", row["state"], "history-read")
                row["state"] = self._final(item)
            else:
                # Already observed live: a consistency check, not a transition.
                if self._final(item) != row["state"]:
                    row["liveDifferedFromHistory"] = True
            row["item"] = item
            row["standing"] = "recovered-from-supplier"
            row["readAt"] = at
        if t in ("collabAgentToolCall", "subAgentActivity"):
            self._delegation_item({"threadId": thread, "turnId": turn, "item": item}, at,
                                  source_suffix=" (history)")

    # ---------- delegation ----------
    def _node(self, child):
        return self.nodes.setdefault(child, {
            "threadId": child, "state": "absent", "parentThreadId": None,
            "parentSource": "not-observed", "sessionId": None, "agentPath": None,
            "agentNickname": None, "agentRole": None, "depth": None, "spawnedBy": None,
            "requested": None, "lastObserved": None, "observationEnded": False,
            "delegatingRole": None})

    def _observe(self, node, status, source, at, event):
        frm = node["state"]
        if status == "notFound" and frm == "observed":
            _, node["state"] = self._step("DS", frm, "not-found-reported")
        elif frm == "absent":
            _, node["state"] = self._step("DS", frm, event)
        elif frm in ("observed", "observation-ended") and event != "thread-read":
            _, node["state"] = self._step("DS", frm, "child-observation")
            node["observationEnded"] = False
        elif event == "thread-read" and frm in ("observed", "observation-ended"):
            _, node["state"] = self._step("DS", frm, "thread-read")
            node["observationEnded"] = False
        if status is not None:
            node["lastObserved"] = {"status": status, "source": source, "at": at}

    def _delegation_item(self, p, at, source_suffix=""):
        item = p["item"]
        sender = p["threadId"]
        if item["type"] == "collabAgentToolCall":
            for child in item["receiverThreadIds"]:
                node = self._node(child)
                state = item["agentsStates"].get(child)
                if node["parentThreadId"] is None:
                    node["parentThreadId"] = item["senderThreadId"]
                    node["parentSource"] = "collabAgentToolCall"
                if item["tool"] == "spawnAgent" and node["spawnedBy"] is None:
                    node["spawnedBy"] = {"threadId": item["senderThreadId"], "turnId": p["turnId"],
                                         "itemId": item["id"]}
                    node["requested"] = {"model": item.get("model"),
                                         "reasoningEffort": item.get("reasoningEffort")}
                    lim = self.limits.get(item["senderThreadId"])
                    if lim and lim["role"] == "TASK":
                        node["delegatingRole"] = {"role": "TASK", "limitId": lim["limitId"],
                                                  "standing": lim["standing"]}
                self._observe(node, state["status"] if state else None,
                              "collabAgentToolCall.agentsStates" + source_suffix, at, "collab-call")
        else:  # subAgentActivity
            node = self._node(item["agentThreadId"])
            node["agentPath"] = item["agentPath"]
            if node["parentThreadId"] is None:
                node["parentThreadId"] = sender
                node["parentSource"] = "subAgentActivity (thread of the item; inference)"
            self._observe(node, item["kind"], "subAgentActivity" + source_suffix, at,
                          "subagent-activity")

    def _child_observation(self, child, method, params, at):
        node = self.nodes[child]
        if method == "thread/status/changed":
            self._observe(node, params["status"]["type"], "thread/status/changed", at,
                          "child-observation")
        else:
            self._observe(node, "active (frame observed: %s)" % method, "child frame", at,
                          "child-observation")

    def _thread_read(self, thread, at):
        if not thread.get("parentThreadId"):
            return
        node = self._node(thread["id"])
        node["parentThreadId"] = thread["parentThreadId"]
        node["parentSource"] = "thread/read"
        node["sessionId"] = thread["sessionId"]
        node["agentNickname"] = thread.get("agentNickname")
        node["agentRole"] = thread.get("agentRole")
        src = thread.get("source")
        if isinstance(src, dict) and "subAgent" in src and isinstance(src["subAgent"], dict) \
                and "thread_spawn" in src["subAgent"]:
            ts = src["subAgent"]["thread_spawn"]
            node["depth"] = ts["depth"]
            node["agentPath"] = node["agentPath"] or ts.get("agent_path")
        self._observe(node, thread["status"]["type"], "thread/read", at, "thread-read")

    def delegation_export(self, root, produced_at, export_id):
        nodes = []
        for child, n in sorted(self.nodes.items()):
            if not self._descends_from(child, root):
                continue
            nodes.append({k: n[k] for k in (
                "threadId", "parentThreadId", "parentSource", "sessionId", "agentPath",
                "agentNickname", "agentRole", "depth", "spawnedBy", "requested",
                "lastObserved", "observationEnded", "delegatingRole")})
        rec = self.ready.get(self.g) or {}
        return {
            "exportId": export_id, "producedAt": produced_at,
            "producer": {"deliverable": "DEL-01-03", "typesPin": TYPES_PIN,
                         "observedVersionLabel": rec.get("observedLabel")},
            "rootThreadId": root, "nodes": nodes, "limits": list(EXPORT_LIMITS),
        }

    def _descends_from(self, child, root):
        seen = set()
        cur = child
        while cur and cur not in seen:
            seen.add(cur)
            parent = self.nodes.get(cur, {}).get("parentThreadId")
            if parent == root:
                return True
            cur = parent
        return False

    def delegation_lines(self, root):
        lines = []
        for (th, turn), st in self.turn_status.items():
            if th == root:
                lines.append("Parent turn %s: %s (native turn status)" % (turn, st))
        for n in self.delegation_export(root, 0, "view")["nodes"]:
            lo = n["lastObserved"]
            s = ("%s — last observed %s (%s, at %s)" % (n["threadId"], lo["status"], lo["source"], lo["at"])
                 if lo else "%s — status not reported" % n["threadId"])
            if n["observationEnded"]:
                s += "; observation ended"
            if n["delegatingRole"]:
                s += "; delegated by a task agent: " + LIMIT_SHOWN[n["delegatingRole"]["standing"]]
            lines.append(s)
        return lines

    # ---------- runtime values handed in ----------
    def _runtime(self, ev):
        k = ev["kind"]
        if k == "limit-label":
            self.limits[ev["threadId"]] = {"role": ev["role"], "limitId": ev["limitId"],
                                           "standing": ev["standing"]}
        elif k == "run-marker":
            self.run_markers.setdefault(ev["threadId"], []).append((ev["turnId"], ev["boundary"], ev["label"]))
        elif k == "model-selection":
            self.model_selection[ev["threadId"]] = ev["model"]
        elif k == "register":
            row = self.tools.get((ev["threadId"], ev["itemId"]))
            if row is None:
                return
            if ev["state"] == "outstanding" and row["state"] == "in-progress":
                _, row["state"] = self._step("TI", "in-progress", "request-outstanding")
            elif ev["state"] == "settled":
                if row["state"] == "waiting-on-request":
                    _, row["state"] = self._step("TI", "waiting-on-request", "request-settled")
                row["request"] = {"requestId": ev["requestId"], "settlementOrigin": ev["origin"]}
        elif k == "act-record":
            self.acts.append(ev["record"])
        else:
            raise ValueError("unknown runtime value " + k)

    # ---------- version identity, experimental surfaces, plan mode ----------
    def version_lines(self):
        rec = self.ready.get(self.g)
        if rec is None:
            return ["Codex not ready: no version identity to show"]
        v = rec["verification"]
        if v["result"] == "verified":
            sup = "Codex %s · verified (%s)" % (rec["observedLabel"], rec.get("qualificationRef") or
                                                "no qualification reference supplied")
        elif v["result"] == "development-unverified":
            sup = "Codex %s · unverified development run (HOSTING U-06) — not the pinned supplier" % rec["observedLabel"]
        else:
            sup = "Codex not started: %s" % v.get("detail")
        label_pin = rec["observedLabel"].split()[-1] if rec.get("observedLabel") else None
        if label_pin == TYPES_PIN:
            types = ("Views built from generated types at %s (manifest %s…), definition pin, "
                     "not qualified; the running label matches" % (TYPES_PIN, TYPES_MANIFEST[:8]))
        else:
            types = ("Views built from generated types at %s; the running supplier reports %s — "
                     "compatibility not verified" % (TYPES_PIN, label_pin))
        exp = rec.get("declaredCapabilities", {}).get("experimentalApi")
        opt = "Experimental protocol opt-in: %s (generation %s)" % (
            "declared" if exp else "not declared", self.g)
        return [sup, types, opt]

    def experimental_label(self, element):
        """EX-1: only protocol elements experimental-only by the pin's variant diff (plan mode)."""
        return element in EXPERIMENTAL_ELEMENTS

    def delegation_availability(self, model_entry, capabilities, effective_features):
        """R21-1 (from C-04, R18-1), read in this order: Model.multiAgentVersion = disabled -> missing; effective
        features.multi_agent = false -> missing; provider capabilities report namespaceTools false -> missing; any of
        the three not read -> not established; otherwise present. Inputs are run-time reads (R19-5): the model/list
        entry (None, or multiAgentVersion null: not read), modelProvider/capabilities/read (None, or namespaceTools
        null: not read), and the effective configuration's features (None: configuration not read; {} : read, nothing
        set, since features are absent unless set, OBS-2 O-8). RV21: v0.2's code read a configuration never read as
        "nothing set" and answered present where R21-1 says not established."""
        version = (model_entry or {}).get("multiAgentVersion")
        if version == "disabled":
            return ("missing", "this model declares no multi-agent runtime")
        if effective_features is not None and effective_features.get("multi_agent") is False:
            return ("missing", "delegation is turned off in the Codex configuration (features.multi_agent)")
        ns = (capabilities or {}).get("namespaceTools")
        if ns is False:
            return ("missing", "this provider does not accept the namespace tools delegation travels in")
        unread = [name for name, unread_ in (("model multi-agent version", version is None),
                                             ("Codex configuration", effective_features is None),
                                             ("provider capabilities", ns is None)) if unread_]
        if unread:
            return ("not-established", "not read: " + ", ".join(unread))
        return ("present", None)

    def goal_line(self, thread):
        g = self.goals.get(thread)
        if g is None:
            return None
        if g["goal"] is None:
            return "No Codex goal (%s)" % g["source"]
        goal = g["goal"]
        return "Codex goal: %s — %s (%s; from %s)" % (goal["objective"], goal["status"], GOAL_NOTE, g["source"])

    def run_in_force(self, thread, turn):
        """R19-2: the run marked in force at a turn, from run markers handed in (display only)."""
        order = self.turn_order.get(thread, [])
        if turn not in order:
            return None
        idx = order.index(turn)
        current = None
        for i, tid in enumerate(order[:idx + 1]):
            for (mt, kind, label) in self.run_markers.get(thread, []):
                if mt != tid:
                    continue
                if kind == "start":
                    current = label
                elif i < idx:      # a run that ended at an earlier turn's end
                    current = None
        return current

    def plan_mode_control(self):
        rec = self.ready.get(self.g) or {}
        if not rec.get("declaredCapabilities", {}).get("experimentalApi"):
            return {"offered": False, "reason": "experimental opt-in not declared"}
        masks = (self.mode_list or {}).get("data", [])
        if not any(m.get("mode") == "plan" for m in masks):
            return {"offered": False, "reason": "no plan preset in collaborationMode/list"}
        return {"offered": True, "label": "experimental"}

    def turn_start(self, thread, text, mode):
        """Compose turn/start params for plan mode or for 'carry out this plan'."""
        model = self.model_selection.get(thread)
        if model is None:
            return {"refused": NO_MODEL}
        params = {"threadId": thread, "input": [{"type": "text", "text": text}]}
        if mode in ("plan", "default"):
            if not self.plan_mode_control()["offered"]:
                if mode == "plan":
                    return {"refused": "plan mode not offered"}
                return {"params": params, "actRecorded": False}
            params["collaborationMode"] = {"mode": mode, "settings": {
                "model": model, "reasoning_effort": None, "developer_instructions": None}}
        return {"params": params, "actRecorded": False}

    # ---------- truthful actor (REQ-005) ----------
    def acts_for(self, anchor):
        lines = []
        for r in self.acts:
            if r["subject"] != anchor:
                continue
            if r["decisionActor"]["name"] == r["recorder"]:
                lines.append("record not shown: non-conformant (decision actor equals recorder)")
                continue
            lines.append("%s by %s (identity not verified) · recorded by %s · content %s · scope %s · purpose %s"
                         % (r["actKind"], r["decisionActor"]["name"], r["recorder"],
                            r["boundContent"], r["scope"], r["purpose"]))
        return lines

    def inferred_acts(self):
        """No act is ever derived from native items (TA-1). Always empty."""
        return []
