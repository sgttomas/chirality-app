"""Executable model of DEL-01-04/NIR-v0.1 (NATIVE_INTERACTION_RECEIVING.md).

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
  * the draft receiving machine (NIR §7).
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


def start_view(selection, last_choice):
    """K-3: no model chosen until the person chooses; the last explicit choice is offered, never applied."""
    if selection is None:
        view = {"model": None, "label": "No model selected", "sendable": False,
                "sendResult": "not started: no model selected (your message is kept)"}
        if last_choice:
            view["offer"] = {"label": f"Use {last_choice['model']} via {last_choice['provider']} "
                                      f"(your last choice for this project, {last_choice['chosenAt']})",
                             "applied": False}
        return view
    return {"model": selection, "label": f"{selection['model']} via {selection['provider']}", "sendable": True}


# ---------------------------------------------------------------------------
# NIR §6  Attachments: supplied-content identity
# ---------------------------------------------------------------------------

ILLUSTRATION_METHOD = "illustration: sha-256 over file bytes (method unselected; RS U-04, HOSTING U-08)"


def content_identity(data):
    return {"method": ILLUSTRATION_METHOD, "value": hashlib.sha256(data).hexdigest()}


def supply_record(attachment_id, name, form, path, bytes_at_selection, bytes_at_submission, turn_ref, at):
    """AT-1...AT-6. Returns (record, decision). The App never sends bytes other than those it showed."""
    sel = content_identity(bytes_at_selection) if bytes_at_selection is not None else None
    sub = content_identity(bytes_at_submission) if bytes_at_submission is not None else None
    rec = {"format": "chirality.nir.attachment-supply", "formatVersion": "0.1", "attachmentId": attachment_id,
           "displayName": name, "suppliedAs": form, "localPath": path,
           "identityAtSelection": sel if sel else {"notObtainable": True, "reason": "not read at selection"},
           "turnRef": turn_ref, "recordedAt": at,
           "supplierRead": "not observed: Codex reads the path itself",
           "providerAdoption": "not observed"}
    if sub is None:
        rec["identityAtSubmission"] = {"notObtainable": True, "reason": "file missing at submission"}
        return rec, "held: file missing at submission; not sent"
    rec["identityAtSubmission"] = sub
    if sel and sel["value"] != sub["value"]:
        return rec, "held: content changed since you selected it; confirm the current content before sending"
    rec["byteLength"] = len(bytes_at_submission)
    return rec, "sent"


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

    def receive(self, t):
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
