"""Executable model of DEL-01-04/NIR-v0.2 (NATIVE_INTERACTION_RECEIVING.md).

Design prototype only (R17-1; R12-3). Not product code, not an App candidate,
not the OI-008 placement. Python 3 standard library only; no network; the
Codex binary is never started. Every supplier name below is a fact of the
generated types at the 0.158.0 definition pin (observed-in-generated-types)
unless the design file says otherwise.

What it models:
  * the request-card model per 0.158.0 server-request kind (NIR §4.1-§4.3);
  * a register double that applies HOSTING-v0.8 §6.2.1 RT-01...RT-13 and the
    U-26 refusal order, used only to drive the card states (NIR §4.4);
  * the card display state for every register state (NIR §4.4);
  * turn/outcome labels (NIR §5), the conversation start display (NIR §5.4);
  * attachment supply records and substitution checks (NIR §6);
  * the draft receiving machine (NIR §7);
  round 2 (NIR-v0.2): turn composition with collaborationMode (C-06), the
  start display's wording and role preselection (C-09, C-15), the App-level
  indicator of waiting requests (C-24), the "Start <workflow>" offer after an
  agent proposal (R19-2 (b)), "Continue as <role>" (R19-3, R19-8), and items
  never completed by turn end (G-4).
"""

import copy
import hashlib
import json

# ---------------------------------------------------------------------------
# NIR §4.1  Kinds at 0.158.0 (HOSTING §6.1 partition, U-20; DEL-01-04's answer-path position)
# ---------------------------------------------------------------------------

A14 = "a14"
PERSON_INPUT = "person-input"
SERVICE = "named-service"
NONE = "none"

# App wording for A14 forms (NIR LB-1...LB-4): the App's own prose never uses
# "accept", "approve", "approval" or "approved" for tool permission (ACT §9,
# AS DS-1). The native value is shown beside the words, verbatim, as a code span.
A14_WORDS = {
    "accept": "Allow once",
    "acceptForSession": "Allow for this session",
    "acceptWithExecpolicyAmendment": "Allow, and add the proposed rule to your Codex exec policy",
    "applyNetworkPolicyAmendment": "Apply the proposed network rule for this host",
    "decline": "Don't allow; the agent continues the turn",
    "cancel": "Don't allow, and interrupt the turn",
    # legacy v1 ReviewDecision
    "approved": "Allow once",
    "approved_for_session": "Allow for this session",
    "approved_execpolicy_amendment": "Allow, and add the proposed rule to your Codex exec policy",
    "approved_mcp_policy_amendment": "Allow, and amend the MCP tool policy for future calls",
    "network_policy_amendment": "Apply the proposed network rule for this host",
    "denied": "Don't allow; the agent tries something else",
    "abort": "Don't allow; the agent waits for your next message",
}
NEGATIVE_FORMS = {"decline", "cancel", "denied", "abort"}
FORBIDDEN_APP_WORDS = ("accept", "approve", "approval", "approved")

KINDS = {
    "item/commandExecution/requestApproval": {
        "originClass": A14, "card": "tool-permission", "title": "Tool permission: run a command",
        "generated": ["accept", "acceptForSession", "acceptWithExecpolicyAmendment",
                      "applyNetworkPolicyAmendment", "decline", "cancel"],
    },
    "item/fileChange/requestApproval": {
        "originClass": A14, "card": "tool-permission", "title": "Tool permission: change files",
        "generated": ["accept", "acceptForSession", "decline", "cancel"],
    },
    "item/permissions/requestApproval": {
        "originClass": A14, "card": "permission-grant", "title": "Tool permission: extra permissions",
        "generated": ["grant-requested", "grant-part", "grant-none"],
    },
    "execCommandApproval": {
        "originClass": A14, "card": "tool-permission", "title": "Tool permission: run a command (legacy request)",
        "generated": ["approved", "approved_for_session", "approved_execpolicy_amendment",
                      "approved_mcp_policy_amendment", "network_policy_amendment", "denied", "abort"],
    },
    "applyPatchApproval": {
        "originClass": A14, "card": "tool-permission", "title": "Tool permission: change files (legacy request)",
        "generated": ["approved", "approved_for_session", "denied", "abort"],
    },
    "item/tool/requestUserInput": {
        "originClass": PERSON_INPUT, "card": "question", "title": "Question from the agent",
        "generated": ["answers", "no-answer"],
    },
    "mcpServer/elicitation/request": {
        "originClass": PERSON_INPUT, "card": "elicitation", "title": "Request for input from an MCP server or the agent",
        "generated": ["accept", "decline", "cancel"],
    },
    "item/tool/call": {"originClass": NONE, "card": None, "unsupported_rule": "app-rule:no-dynamic-tools"},
    "account/chatgptAuthTokens/refresh": {"originClass": NONE, "card": None,
                                          "unsupported_rule": "app-rule:external-token-login-not-adopted"},
    "attestation/generate": {"originClass": NONE, "card": None, "unsupported_rule": "app-rule:no-attestation",
                             "needs_capability": "requestAttestation"},
    "currentTime/read": {"originClass": SERVICE, "card": None, "service_rule": "app-rule:current-time",
                         "needs_capability": "experimentalApi"},
}


def classify(method, declared):
    """HOSTING §6.1 familiar set limited by declared capabilities; returns (classification, originClass)."""
    k = KINDS.get(method)
    if k is None:
        return "unfamiliar", NONE
    cap = k.get("needs_capability")
    if cap and not declared.get(cap, False):
        return "unfamiliar", NONE
    if k.get("unsupported_rule"):
        return "known-app-unsupported", NONE
    return "known-answerable", k["originClass"]


def _form_name(form):
    return form if isinstance(form, str) else next(iter(form))


def offered_forms(method, params):
    """NIR §4.2 FO-1...FO-6: the native answer forms a card offers, never one the request does not."""
    k = KINDS[method]
    if method == "item/commandExecution/requestApproval":
        avail = params.get("availableDecisions")
        if avail:                                   # FO-1: exactly what the request lists
            return [copy.deepcopy(f) for f in avail], "availableDecisions"
        forms = []
        for name in k["generated"]:                 # FO-2: generated set, compound forms only when proposed
            if name == "acceptWithExecpolicyAmendment":
                if params.get("proposedExecpolicyAmendment"):
                    forms.append({name: {"execpolicy_amendment": params["proposedExecpolicyAmendment"]}})
            elif name == "applyNetworkPolicyAmendment":
                for amend in params.get("proposedNetworkPolicyAmendments") or []:
                    forms.append({name: {"network_policy_amendment": amend}})
            else:
                forms.append(name)
        return forms, "generated types (no availableDecisions in the request)"
    if method in ("execCommandApproval", "applyPatchApproval"):
        # FO-3: "timed_out" is never offered: it is no person's answer (R3, R17-9)
        return [f for f in k["generated"] if f not in ("approved_execpolicy_amendment", "network_policy_amendment")
                or params.get("proposedExecpolicyAmendment")], "generated types (legacy)"
    return list(k["generated"]), "generated types"


def decline_form(method, params):
    """NIR §4.3 DM-1...DM-6: the explicit decline per kind, or why there is none."""
    if method == "item/commandExecution/requestApproval":
        forms, _ = offered_forms(method, params)
        names = [_form_name(f) for f in forms]
        if "decline" in names:
            return {"native": {"decision": "decline"}, "standing": "native form"}
        if "cancel" in names:
            return {"native": {"decision": "cancel"}, "standing": "native form; also interrupts the turn (supplier's description)"}
        return {"native": None, "standing": "no negative form offered by this request"}
    if method == "item/fileChange/requestApproval":
        return {"native": {"decision": "decline"}, "standing": "native form"}
    if method in ("execCommandApproval", "applyPatchApproval"):
        return {"native": {"decision": {"denied": {"rejection": ""}}}, "standing": "native form (legacy)"}
    if method == "item/permissions/requestApproval":
        return {"native": {"permissions": {}, "scope": "turn"},
                "standing": "PROPOSED: an empty grant; its effect is not observed"}
    if method == "item/tool/requestUserInput":
        return {"native": {"answers": {}}, "standing": "PROPOSED: an empty answer map; its effect is not observed"}
    if method == "mcpServer/elicitation/request":
        return {"native": {"action": "decline", "content": None, "_meta": None}, "standing": "native form"}
    return {"native": None, "standing": "not a card"}


def is_negative(method, native):
    """Which native contents the card submits as a decline (HOSTING RT-08 guard; join J-H3)."""
    if isinstance(native, str):
        return native in NEGATIVE_FORMS
    if isinstance(native, dict):
        if "denied" in native:
            return True
        if native.get("action") in ("decline", "cancel"):
            return True
        if method == "item/tool/requestUserInput" and native.get("answers") == {}:
            return True
        if method == "item/permissions/requestApproval" and native.get("permissions") == {}:
            return True
        if "decision" in native:
            return is_negative(method, native["decision"])
    return False


def card_for(method, params, declared):
    """Build the card a person sees for one register entry (NIR §4.2)."""
    classification, origin = classify(method, declared)
    if classification != "known-answerable" or KINDS[method]["card"] is None:
        return {"method": method, "card": None, "classification": classification}
    k = KINDS[method]
    forms, source = offered_forms(method, params)
    card = {"method": method, "card": k["card"], "title": k["title"], "originClass": origin,
            "formsSource": source, "forms": [], "notes": [], "decline": decline_form(method, params)}
    if origin == A14:
        for f in forms:
            name = _form_name(f)
            card["forms"].append({"words": A14_WORDS.get(name, name), "native": f})
        if params.get("grantRoot"):
            card["notes"].append("asks for write access under a folder for the session (supplier marks this UNSTABLE)")
        if method == "item/permissions/requestApproval":
            card["forms"] = [
                {"words": "Grant the requested permissions", "native": {"permissions": params.get("permissions"), "scope": "turn"}},
                {"words": "Grant part of them", "native": "subset of the requested profile, scope turn or session"},
                {"words": "Grant nothing", "native": {"permissions": {}, "scope": "turn"}},
            ]
        card["notes"].append("tool permission only: it never stands for marking checked, accepting, "
                             "engineering approval or reliance (HOSTING R8)")
    elif method == "item/tool/requestUserInput":
        for q in params.get("questions", []):
            card["forms"].append({"question": q["id"], "header": q["header"], "options": q.get("options"),
                                  "freeText": q.get("isOther", False), "secret": q.get("isSecret", False)})
        if not params.get("isBlocking", True):
            card["notes"].append("the agent continues while this waits (isBlocking false)")
        if params.get("autoResolutionMs") is not None:
            card["notes"].append("Codex may resolve this itself (deprecated autoResolutionMs set); "
                                 "the App never answers it by itself")
        card["notes"].append("your answer goes to the agent as conversation input; it is never a recorded act (CAP-6)")
    elif method == "mcpServer/elicitation/request":
        mode = params.get("mode")
        card["mode"] = mode
        card["requester"] = f"MCP server {params.get('serverName')!r} or the agent (not established)"
        card["forms"] = [{"words": "Send", "native": "accept"}, {"words": "Decline", "native": "decline"},
                         {"words": "Cancel", "native": "cancel"}]
        if mode == "url":
            card["notes"].append("the App shows the address and never opens it by itself")
        if mode == "openai/userVerification":
            card["notes"].append("identity verification challenge: only you can complete it; the App never does")
        card["notes"].append("your answer goes to the agent as conversation input; it is never a recorded act (CAP-6)")
    return card


def app_prose(card):
    """All App-authored words on a card (titles, form words, notes), without native values."""
    words = [card.get("title", "")]
    for f in card.get("forms", []):
        words.append(f.get("words", ""))
    words += [n for n in card.get("notes", []) if "never stands for" not in n]
    return " ".join(words).lower()


# ---------------------------------------------------------------------------
# NIR §4.4  Register double: HOSTING §6.2.1 RT-01...RT-13, U-26 refusal order
# ---------------------------------------------------------------------------

REFUSAL_ORDER = ["no-such-request", "generation-closed", "already-resolved", "already-settled",
                 "origin-not-permitted", "invalid-answer"]


class RegisterDouble:
    """Stands in for DEL-01-01's register (custody DEL-01-02). Not a model of HOSTING; a driver for cards."""

    def __init__(self, declared=None):
        self.declared = declared or {"experimentalApi": False, "requestAttestation": False}
        self.entries = {}
        self.order = []
        self.rt_seen = set()
        self.position = 0
        self.closed_generations = set()

    def _rt(self, rid, rt, **changes):
        self.entries[rid].update(changes)
        self.rt_seen.add(rt)
        self.entries[rid].setdefault("_history", []).append(rt)

    def receive(self, rid, method, params, generation=1):
        self.position += 1
        e = {"recordKind": "server-request-entry", "requestIdentity": rid, "generation": generation,
             "method": method, "classification": None, "originClass": NONE, "receiptPosition": self.position,
             "state": "received", "replyWriteResult": "not-attempted",
             "acknowledgmentObservation": {"status": "not-observed"}, "nativeParameters": params}
        refs = {k: params[k2] for k, k2 in (("thread", "threadId"), ("turn", "turnId"), ("item", "itemId"))
                if k2 in params}
        if refs:
            e["subjectReferences"] = refs
        self.entries[rid] = e
        self.order.append(rid)
        self.rt_seen.add("RT-01")
        e["_history"] = ["RT-01"]
        classification, origin = classify(method, self.declared)
        e["classification"], e["originClass"] = classification, origin
        if classification == "unfamiliar":
            self._rt(rid, "RT-02", state="errored", replyWriteResult="written",
                     settlement={"kind": "error", "nativeContent": {"code": -32601, "message": "unknown request"},
                                 "origin": {"class": "app-explicit-error"}})
        elif classification == "known-app-unsupported":
            self._rt(rid, "RT-03", state="errored", replyWriteResult="written",
                     settlement={"kind": "error", "nativeContent": {"code": -32601, "message": "not provided by the App"},
                                 "origin": {"class": "app-rule", "ruleName": KINDS[method]["unsupported_rule"]}})
        else:
            self._rt(rid, "RT-04", state="outstanding")
        return e

    def answer(self, rid, native, origin, generation=None, write_ok=True):
        """HOSTING §6.4 'answer'; returns (accepted, reason)."""
        reasons = []
        e = self.entries.get(rid)
        if e is None:
            reasons.append("no-such-request")
        else:
            gen = e["generation"] if generation is None else generation
            if gen != e["generation"] or e["generation"] in self.closed_generations:
                reasons.append("generation-closed")
            if e["state"] == "resolved-by-supplier":
                reasons.append("already-resolved")
            if e["state"] in ("answered", "declined", "errored", "settling", "settle-write-failed"):
                reasons.append("already-settled")
            oc = e["originClass"]
            negative = is_negative(e["method"], native)
            if origin["class"] == "app-rule" and oc in (A14, PERSON_INPUT) and not negative:
                reasons.append("origin-not-permitted")
            if origin["class"] == "person-via-interaction" and not origin.get("actorRef"):
                reasons.append("origin-not-permitted")
            if not self._valid(e, native):
                reasons.append("invalid-answer")
        if reasons:
            reason = sorted(reasons, key=REFUSAL_ORDER.index)[0]
            if e is not None and e["state"] == "outstanding":
                self._rt(rid, "RT-05")
                e["_lastRefusal"] = reason
            return False, reason
        kind = "decline" if is_negative(e["method"], native) else "answer"
        self._rt(rid, "RT-06", state="settling", settlement={"kind": kind, "nativeContent": native, "origin": origin})
        if not write_ok:
            self._rt(rid, "RT-09", state="settle-write-failed", replyWriteResult="write-failed")
        elif kind == "decline":
            self._rt(rid, "RT-08", state="declined", replyWriteResult="written")
        else:
            self._rt(rid, "RT-07", state="answered", replyWriteResult="written")
        e.pop("_lastRefusal", None)
        return True, None

    def _valid(self, e, native):
        method, params = e["method"], e.get("nativeParameters", {})
        if method in ("item/commandExecution/requestApproval", "item/fileChange/requestApproval",
                      "execCommandApproval", "applyPatchApproval"):
            if not isinstance(native, dict) or "decision" not in native:
                return False
            forms, _ = offered_forms(method, params)
            return native["decision"] in forms or _form_name(native["decision"]) in [_form_name(f) for f in forms]
        if method == "item/tool/requestUserInput":
            if not isinstance(native, dict) or not isinstance(native.get("answers"), dict):
                return False
            ids = {q["id"] for q in params.get("questions", [])}
            return all(k in ids and isinstance(v, dict) and isinstance(v.get("answers"), list)
                       for k, v in native["answers"].items())
        if method == "mcpServer/elicitation/request":
            return isinstance(native, dict) and native.get("action") in ("accept", "decline", "cancel")
        if method == "item/permissions/requestApproval":
            return isinstance(native, dict) and native.get("scope") in ("turn", "session") and "permissions" in native
        if method == "currentTime/read":
            return isinstance(native, dict)
        return False

    def supplier_resolved(self, rid, cause=None):
        e = self.entries[rid]
        if e["state"] == "outstanding":
            self._rt(rid, "RT-10", state="resolved-by-supplier",
                     supplierResolution={"source": "serverRequest/resolved", "cause": cause})
        elif e["state"] == "answered":
            self._rt(rid, "RT-12", acknowledgmentObservation={
                "status": "observed", "what": "serverRequest/resolved after the written reply"})
        elif e["state"] == "declined":
            self._rt(rid, "RT-13", acknowledgmentObservation={
                "status": "observed", "what": "serverRequest/resolved after the written reply"})

    def close_generation(self, generation):
        self.closed_generations.add(generation)
        for rid in self.order:
            e = self.entries[rid]
            if e["generation"] == generation and e["state"] == "outstanding":
                self._rt(rid, "RT-11", state="ended-unanswered", endCause="process-exit")

    def list_outstanding(self):
        return [self.entries[r] for r in self.order if self.entries[r]["state"] == "outstanding"]

    def public(self, rid):
        """The entry as HOSTING's schema describes it (private keys removed)."""
        return {k: v for k, v in self.entries[rid].items() if not k.startswith("_")}


def card_state(entry):
    """NIR §4.4 CS-0...CS-7: the card's display state for a register entry. One label per state."""
    s = entry["state"]
    origin = (entry.get("settlement") or {}).get("origin", {})
    ack = entry["acknowledgmentObservation"]["status"] == "observed"
    if s == "received":
        return "CS-0", "not shown yet (being classified)"
    if s == "errored":
        if origin.get("class") == "app-explicit-error":
            return "CS-E", f"Unrecognized request from Codex ({entry['method']}): answered with an error"
        return "CS-U", (f"Codex asked for something the App does not provide ({entry['method']}): "
                        f"answered with an error by rule {origin.get('ruleName')}")
    if s == "outstanding":
        refusal = entry.get("_lastRefusal")
        return "CS-1", "Waiting for your answer" + (f" (last answer not taken: {refusal})" if refusal else "")
    if s == "settling":
        return "CS-2", "Sending your answer: not yet written to Codex"
    if s == "answered":
        return ("CS-3a", "Your answer was written; Codex reported the request resolved") if ack else \
               ("CS-3", "Your answer was written to Codex; Codex has not confirmed it")
    if s == "declined":
        if origin.get("class") == "app-rule":
            return "CS-4r", f"Declined by App rule {origin.get('ruleName')}, not by you"
        return ("CS-4a", "You declined; written; Codex reported the request resolved") if ack else \
               ("CS-4", "You declined; written to Codex; Codex has not confirmed it")
    if s == "settle-write-failed":
        return "CS-5", "Your answer could not be written; whether Codex received it is unknown"
    if s == "resolved-by-supplier":
        cause = (entry.get("supplierResolution") or {}).get("cause")
        return "CS-6", "Resolved by Codex before you answered (cause: " + (cause or "not reported") + ")"
    if s == "ended-unanswered":
        return "CS-7", "Ended unanswered: the Codex process ended"
    raise ValueError(s)


def answer_submission(entry, native, person, offered, submitted_at):
    """NIR §4.5: the format DEL-01-04 hands to the register's answer operation."""
    return {"format": "chirality.nir.answer-submission", "formatVersion": "0.1",
            "requestIdentity": entry["requestIdentity"], "generation": entry["generation"],
            "method": entry["method"], "nativeAnswer": native,
            "origin": {"class": "person-via-interaction", "actorRef": person_ref(person)},
            "formsOffered": [_form_name(f) if not isinstance(f, dict) or len(f) == 1 else "structured"
                             for f in offered],
            "submittedAt": submitted_at,
            "secretValuesPresent": False}


def person_ref(person):
    parts = [p for p in (person.get("displayName"), person.get("osAccount"), person.get("codexAccount")) if p]
    return "person:" + "/".join(parts) + " (identity not verified)"


# ---------------------------------------------------------------------------
# NIR §5  Turn and outcome presentation; §5.4 conversation start display
# ---------------------------------------------------------------------------

def turn_label(observed_status, observation, cause=None, descendants=None):
    """Only observed facts; unknown stays unknown; primary completion never implies descendants finished."""
    if observation == "lost" and observed_status in (None, "inProgress"):
        base = "TO-6 Outcome unknown: observation was lost before Codex reported an end"
    elif observed_status == "inProgress":
        base = "TO-1 In progress"
    elif observed_status == "completed":
        base = "TO-3 Completed"
    elif observed_status == "interrupted":
        why = {"person": "interrupted by you", "quit": "interrupted by quit",
               "codex-stop": "interrupted by Stop Codex",
               "cancel-answer": "interrupted after your `cancel` tool-permission answer"}.get(cause)
        base = "TO-4 Interrupted" + (f" ({why})" if why else " (cause not observed)")
    elif observed_status == "failed":
        base = "TO-5 Failed" + (f": {cause}" if cause else "")
    elif observed_status is None:
        base = "TO-0 Not started"
    else:
        raise ValueError(observed_status)
    if descendants:
        active = [d for d, s in descendants.items() if s in ("pendingInit", "running")]
        unknown = [d for d, s in descendants.items() if s is None]
        if active:
            base += f"; {len(active)} delegated agent(s) last reported running"
        if unknown:
            base += f"; {len(unknown)} delegated agent(s) with no reported state"
    return base


def start_view(selection, last_choice, workflow_run=False, roles=None, default_role=None):
    """K-3 and R18-2 (C-09): no model until the person chooses; the last choice is offered, never applied.
    ST-5 (C-15): the role preselected from the registry's default_for_new_chat, clearable; "no role" allowed."""
    view = {}
    if selection is None:
        refusal = "run not started — no model selected" if workflow_run else "not started — no model selected"
        view = {"model": None, "label": "No model selected", "sendable": False,
                "sendResult": refusal + " (your message is kept)"}
        if last_choice:
            view["offer"] = {"label": f"Use {last_choice['model']} via {last_choice['provider']} "
                                      f"(your last choice for this project, {last_choice['chosenAt']})",
                             "applied": False}
    else:
        view = {"model": selection, "label": f"{selection['model']} via {selection['provider']}", "sendable": True}
    if roles is not None:
        options = list(roles) + ["no role"]
        pre = default_role if default_role in roles else None
        view["role"] = {"options": options, "preselected": pre or "no role", "clearable": True,
                        "label": (f"Role: {pre} (preselected; you can change or clear it)" if pre else "Role: no role"),
                        "fixedForConversation": True}
    return view


def choose_role(view, choice):
    """The person may change or clear the preselection before the first send; afterwards it is fixed (L-2)."""
    if choice not in view["role"]["options"]:
        return False, f"{choice!r} is not a role in the registry"
    view["role"]["chosen"] = choice
    return True, choice


# ---------------------------------------------------------------------------
# NIR §5.6  Turn composition (C-06): DEL-01-04 composes turn/start
# ---------------------------------------------------------------------------

def compose_turn(conv, text, attachments=(), plan_chosen=False, plan_element=None, run_start_text=None,
                 run_end_line=None):
    """Returns (params, why). conv: {threadId, model, usedPlanMode}. plan_element: NPTD §5.4's value.
    TC-2: the run-start text (TC-3) or, when a run ended and none starts, DEL-02-02's run-end line (R20-3; WR TX-5),
    then the person's text, then the attachments (text elements, image inputs, named paths; §6)."""
    if conv.get("model") is None:
        return None, "not started — no model selected"
    if run_start_text is not None and run_end_line is not None:
        return None, "a run start carries its own chain line; no separate run-end line (WR TX-5)"
    inputs = []
    if run_start_text is not None:      # R19-7: DEL-02-02's run-start text, its own element, first
        inputs.append({"type": "text", "text": run_start_text, "text_elements": []})
    if run_end_line is not None:        # R20-3: the run-end line, first, before the person's own text
        inputs.append({"type": "text", "text": run_end_line, "text_elements": []})
    if text:
        inputs.append({"type": "text", "text": text, "text_elements": []})
    for a in attachments:
        inputs.append(a)
    params = {"threadId": conv["threadId"], "input": inputs}
    if plan_chosen:
        if plan_element is None or "notOffered" in plan_element:
            return None, "plan mode not offered" + (f" ({plan_element['notOffered']})" if plan_element else "")
        params["collaborationMode"] = plan_element["collaborationMode"]
        conv["usedPlanMode"] = True
    elif conv.get("usedPlanMode"):
        # O-8: plan mode persists until the default mode is sent; send it explicitly on every later turn
        params["collaborationMode"] = {"mode": "default",
                                       "settings": {"model": conv["model"]["model"], "reasoning_effort": None,
                                                    "developer_instructions": None}}
    return params, None


# ---------------------------------------------------------------------------
# NIR §4.8  App-level indicator of waiting requests (C-24)
# ---------------------------------------------------------------------------

def waiting_indicator(registers, open_windows):
    """Counts supplier requests waiting for the person, per conversation, whether or not a window shows them.
    Arrivals never count (NR-7). open_windows: conversation -> number of windows showing it."""
    rows = []
    for conv, reg in registers.items():
        n = len(reg.list_outstanding())
        if n:
            rows.append({"conversation": conv, "waiting": n, "windowsOpen": open_windows.get(conv, 0)})
    total = sum(r["waiting"] for r in rows)
    return {"total": total, "label": (f"{total} request(s) waiting for your answer" if total else None),
            "conversations": rows}


# ---------------------------------------------------------------------------
# NIR §5.7  Runs in a conversation: the "Start <workflow>" offer (R19-2 (b))
# ---------------------------------------------------------------------------

PROPOSAL_PREFIX = "Next workflow: "
FINISHED_PREFIX = "Workflow finished: "


def _lines(text):
    return [l.strip() for l in (text or "").splitlines() if l.strip()]


def start_offer(final_message_text, registered, run_in_progress, finished=False):
    """RN-3…RN-5 (R20-5, R20-9, R20-11 (1), (2)): an offer only when the message's last non-empty line is
    'Next workflow: <origin>:<name>', that line form appears once, and it names exactly one registered workflow.
    With no run in force the offer is 'Start <B>'; during a run it is only 'End <A> and start <B>' (enabled), whose
    press ends A with cause 'ended to start <B>', or 'completed' on a finished report (RN-7). It starts nothing by itself."""
    lines = _lines(final_message_text)
    if sum(1 for l in lines if l.startswith(PROPOSAL_PREFIX)) != 1 or not lines[-1].startswith(PROPOSAL_PREFIX):
        return None
    named = lines[-1][len(PROPOSAL_PREFIX):].strip()
    matches = [r for r in registered if f"{r['origin']}:{r['name']}" == named]
    if len(matches) != 1:
        return {"offer": None, "note": f"the agent proposed {named!r}, which names no single registered workflow"}
    r = matches[0]
    offer = {"workflow": r, "startsNothingByItself": True, "recordsNothing": True, "enabled": True}
    if run_in_progress:
        offer["label"] = f"End {run_in_progress} and start {r['name']}"
        offer["endsRun"] = {"run": run_in_progress, "by": "the person (DEF-4)",
                            "cause": "completed" if finished else f"ended to start {r['name']}"}
    else:
        offer["label"] = f"Start {r['name']} (proposed by the agent)"
    return offer


def finished_offer(final_message_text, run_in_force):
    """RN-7 (R20-1, R20-9, R20-11 (2)): 'End run' when 'Workflow finished: <origin>:<name>' appears once, as the last
    non-empty line or the line immediately before the proposal line, naming the run in force. Nothing ends by itself."""
    lines = _lines(final_message_text)
    if not run_in_force or sum(1 for l in lines if l.startswith(FINISHED_PREFIX)) != 1:
        return None
    cand = lines[-1]
    if lines[-1].startswith(PROPOSAL_PREFIX) and len(lines) >= 2:
        cand = lines[-2]
    if cand != FINISHED_PREFIX + f"{run_in_force['origin']}:{run_in_force['name']}":
        return None
    return {"label": "End run", "endsRun": {"run": run_in_force["run"], "by": "the person (DEF-4)", "cause": "completed"},
            "endsNothingByItself": True, "recordsNothing": True}


def confirm_start(offer):
    """The person's click hands a selection to DEL-02-02 / DEL-02-03; the agent's line never does."""
    if not offer or not offer.get("enabled"):
        return None
    return {"selectedBy": "the person", "workflow": offer["workflow"], "source": "confirmed agent proposal"}


# ---------------------------------------------------------------------------
# NIR §5.8  "Continue as <role>" (R19-3, R19-8)
# ---------------------------------------------------------------------------

def continue_as(source, role, parts):
    """CA-1, CA-2 (R19-3, R19-8, R20-6): a new conversation with the role's guidance. The App asks the source
    conversation's agent, in a visible turn of that conversation, to draft the handoff summary; nothing is sent to
    the new conversation."""
    header = f"Handoff from conversation {source['threadId']} ({source.get('role') or 'no role'})."
    request = ("Please draft a handoff summary for a new conversation, covering: " + "; ".join(parts) + ".")
    return {"newConversation": True, "role": role, "fork": False, "model": None,
            "sourceTurn": {"threadId": source["threadId"], "visible": True, "text": request},
            "composer": {"header": header, "text": header, "editable": True, "sent": False},
            "note": "a fork keeps the source's role at 0.158.0 (OBS-3 W-6); this is a new conversation"}


def handoff_composer(plan, agent_draft):
    """CA-2: the source agent's draft goes under the App header; the person edits it; nothing is sent. If the source
    turn failed or was interrupted (draft None), the composer holds the header only (PROPOSED)."""
    comp = dict(plan["composer"])
    comp["text"] = comp["header"] + ("\n\n" + agent_draft if agent_draft else "")
    comp["draftedBy"] = "source conversation's agent (visible turn)" if agent_draft else "none (source turn failed)"
    return comp


# ---------------------------------------------------------------------------
# NIR §5.1 TO-9  Items opened and never completed (G-4)
# ---------------------------------------------------------------------------

def settle_items_at_turn_end(items, turn_status):
    """Message and reasoning items still open when the turn ends settle 'not completed (turn ended)'."""
    out = {}
    for item_id, state in items.items():
        out[item_id] = state if state == "completed" else f"not completed (turn ended {turn_status})"
    return out


# ---------------------------------------------------------------------------
# NIR §6  Attachments: supplied-content identity
# ---------------------------------------------------------------------------

ILLUSTRATION_METHOD = "illustration: sha-256 over file bytes (method unselected; RS U-04, HOSTING U-08)"


def content_identity(data):
    return {"method": ILLUSTRATION_METHOD, "value": hashlib.sha256(data).hexdigest()}


# R21-2 (V21-A M-2; OBS-3 W-3, W-1 at Codex 0.158.0): an attachment is carried as a text element (text files, the
# file named), as an image input (images), or by naming its path for the agent to read with its tools (any other
# file). Only the first two are "supplied". `mention` and `skill` are not attachment forms: `mention` delivered nothing
# to the model and `skill` was honoured only for a discovered SKILL.md at its canonical path.
SUPPLIED = "supplied"
NAMED = "named; read only if a tool item shows it"
SUPPLIER_READ = {
    "text-element": "not applicable: the bytes are in the turn's own text element",
    "localImage": "not observed: Codex reads the path itself",
    "image-url": "not applicable: content passed by reference",
    "image-fileId": "not applicable: content passed by reference",
    "path-named": "not observed: read only if a tool item shows it",
}
NOT_ATTACHMENT_FORMS = {"mention": "delivers nothing to the model at 0.158.0 (OBS-3 W-3)",
                        "skill": "honoured only for a discovered SKILL.md at its canonical path (OBS-3 W-1)"}
IMAGE_SUFFIXES = (".png", ".jpg", ".jpeg", ".gif", ".webp")
TEXT_BOUND = 256 * 1024          # PROPOSED bound for carrying a text file in the turn (U-NIR-10)


def text_identity(text):
    return {"method": "sha256 over UTF-8 text", "value": hashlib.sha256(text.encode("utf-8")).hexdigest()}


def carrier_for(name, data):
    """AT-9/AT-10 (PROPOSED): the carrier the App uses for a file's bytes."""
    if name.lower().endswith(IMAGE_SUFFIXES):
        return "localImage"
    if data is not None and len(data) <= TEXT_BOUND and b"\x00" not in data:
        try:
            data.decode("utf-8")
            return "text-element"
        except UnicodeDecodeError:
            pass
    return "path-named"


def attachment_input(form, name, path, data):
    """The turn input element for one attachment (UserInput at 0.158.0). Returns (element, element_text or None).
    The naming lines are App-written; they name the file and instruct nothing beyond R21-2's 'read it with your
    tools' for a named path (PROPOSED wording, AT-9, AT-10)."""
    if form in NOT_ATTACHMENT_FORMS:
        raise ValueError(f"{form} is not an attachment form: {NOT_ATTACHMENT_FORMS[form]}")
    ident = content_identity(data)["value"][:12] if data is not None else "not obtainable"
    if form == "text-element":
        text = f'[Chirality] Attached file "{name}" ({path}; content {ident}). Its bytes follow this line.\n' + data.decode("utf-8")
        return {"type": "text", "text": text, "text_elements": []}, text
    if form == "localImage":
        return {"type": "localImage", "path": path}, None
    if form == "path-named":
        text = (f'[Chirality] File named, not supplied: "{name}" at {path} (content {ident} when attached). '
                "Read it with your tools if you need it.")
        return {"type": "text", "text": text, "text_elements": []}, text
    raise ValueError(form)


def supply_record(attachment_id, name, form, path, bytes_at_selection, bytes_at_submission, turn_ref, at,
                  element_text=None, draft=None):
    """AT-1...AT-10. Returns (record, decision). The App never sends bytes other than those it showed, and records
    per form what it sent: supplied (text element, image input) or named (a path for the agent's tools)."""
    if form in NOT_ATTACHMENT_FORMS:
        return None, f"refused: {form} is not an attachment form ({NOT_ATTACHMENT_FORMS[form]})"
    sel = content_identity(bytes_at_selection) if bytes_at_selection is not None else None
    sub = content_identity(bytes_at_submission) if bytes_at_submission is not None else None
    rec = {"format": "chirality.nir.attachment-supply", "formatVersion": "0.2", "attachmentId": attachment_id,
           "displayName": name, "suppliedAs": form, "supplyStanding": NAMED if form == "path-named" else SUPPLIED,
           "localPath": path,
           "identityAtSelection": sel if sel else {"notObtainable": True, "reason": "not read at selection"},
           "turnRef": turn_ref, "recordedAt": at,
           "supplierRead": SUPPLIER_READ[form],
           "providerAdoption": "not observed"}
    if element_text is not None:
        rec["elementIdentity"] = text_identity(element_text)
    if draft is not None:
        rec["draft"] = dict(draft, standing="draft — not a registered workflow; this conversation is not a workflow run")
    if sub is None:
        rec["identityAtSubmission"] = {"notObtainable": True, "reason": "file missing at submission"}
        return rec, "held: file missing at submission; not sent"
    rec["identityAtSubmission"] = sub
    if sel and sel["value"] != sub["value"]:
        return rec, "held: content changed since you selected it; confirm the current content before sending"
    rec["byteLength"] = len(bytes_at_submission)
    return rec, ("sent (named, not supplied)" if form == "path-named" else "sent")


def tool_read(record, item):
    """AT-10: a tool item that names a named path is recorded beside it; the standing stays 'named'."""
    if record["suppliedAs"] != "path-named":
        raise ValueError("tool reads belong to a named path only")
    record.setdefault("toolReads", []).append(item)
    return record


def same_name_distinct(records):
    """AT-4: attachments are told apart by content identity, never merged by name."""
    seen = {}
    for r in records:
        seen.setdefault(r["displayName"], set()).add(r["identityAtSubmission"].get("value"))
    return {n: len(v) for n, v in seen.items()}


# ---------------------------------------------------------------------------
# NIR §7  Draft receiving (OUT-004): DEL-02-02's WR-v0.1 §5.1 transitions, as DEL-01-04 receives them
# ---------------------------------------------------------------------------

# (from, event) -> the 'to' states WR §5.1 allows. "any" stands for every state.
DRAFT_ALLOWED = {
    ("absent", "written"): {"draft", "not valid"},
    ("draft", "changed"): {"draft", "not valid"},
    ("not valid", "changed"): {"draft", "not valid"},
    ("draft", "review shown"): {"under review"},
    ("changed since review", "review shown"): {"under review"},
    ("draft", "registration refused"): {"draft", "not valid"},
    ("not valid", "registration refused"): {"not valid"},
    ("changed since review", "registration refused"): {"draft", "not valid", "changed since review"},
    ("under review", "review stale"): {"changed since review"},
    ("under review", "registered"): {"registered, unchanged since"},
    ("under review", "registration not completed"): {"draft"},
    ("registered, unchanged since", "changed"): {"draft"},
    ("any", "removed"): {"removed"},
}
DRAFT_WORDS = {
    "draft": "draft — not registered",
    "not valid": "draft — not valid for registration (see findings)",
    "under review": "under review",
    "changed since review": "changed since review — review again before registering",
    "registered, unchanged since": "registered as {revision} (A15 {a15_record})",
    "removed": "removed",
}


class DraftView:
    def __init__(self):
        self.state = "absent"
        self.reviewed = None
        self.revision = None
        self.log = []

    def receive(self, t, library_entry=None):
        """C-02 read side: the A15 record and revision come from the transition when present, else from
        WR's library_entry for the same draft; without either, 'registered' is not shown."""
        if library_entry:
            t = dict(t)
            t.setdefault("a15_record", library_entry.get("a15_record"))
            t.setdefault("revision", library_entry.get("revision"))
        if t["from"] != self.state:
            return False, f"'from' {t['from']!r} is not the view's state {self.state!r}: re-read the draft reference"
        allowed = DRAFT_ALLOWED.get((self.state, t["event"])) or DRAFT_ALLOWED.get(("any", t["event"]))
        if not allowed or t["to"] not in allowed:
            return False, f"event {t['event']!r} to {t['to']!r} is not a WR §5.1 transition from {self.state!r}"
        if t["event"] == "registered":
            if not str(t.get("a15_record", "")).startswith("rec:") or not t.get("revision"):
                return False, "registered without the A15 record and revision: refused (no invented registration)"
            if (t.get("content") or {}).get("value") != (self.reviewed or {}).get("value"):
                return False, "registered content differs from the reviewed content: refused"
            self.revision = t["revision"]
        if t["event"] == "registration not completed" and not str(t.get("a15_record", "")).startswith("rec:"):
            return False, "registration not completed without the recorded act it follows: refused"
        if t["event"] == "review shown":
            self.reviewed = t["content"]
        self.state = t["to"]
        self.log.append((t["event"], self.state))
        return True, self.state

    def words(self, t=None):
        w = DRAFT_WORDS.get(self.state, self.state)
        return w.format(revision=self.revision, a15_record=(t or {}).get("a15_record"))

    def local(self, action):
        """A local UI action can never move a draft to reviewed or registered (REQ-004, VER-004)."""
        return False, f"local action {action!r} refused: only the workspace's transitions move a draft"


def canonical(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
