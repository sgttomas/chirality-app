#!/usr/bin/env python3
"""Destination flow prototype (LOOP-v0.8 §5.3; node B5). Not product code.

Python 3 standard library only (R12-3). It runs the one account of a host
agent's network destinations on a scripted native layer and a scripted
host control:

  DF-3  the allow rule A-1...A-7 (DECISION-K1 K1-5 for switches and entries);
  DF-4  V-D after V-3 and before dispatch, and the check at contact;
  DF-5  the in-work request Q-1...Q-9 with a carried call;
  DF-6  the request states and the result each gives in TL-2's classes;
  DF-7  the stateless MCP evidence SE-1...SE-3 (as scripted discovery answers);
  DF-8  the RS R15 / R11 entries the flow leaves.

Every RS entry it produces is validated against DEL-04-03's
RS_RECORD.schema.json with DEL-04-03's minischema.py (which also loads the
ACT and AS schemas the RS schema refers to), and every request record
against ../LOOP_DESTINATION_REQUEST.schema.json with ./schema_subset.py.
Each case of LOOP §5.2 (MS-14...MS-27) is compared with its expected result.

  python3 -B destination_flow.py                # run the cases
  python3 -B destination_flow.py --emit PATH    # also write the E-14 run log

The E-14 log written with --emit is the fixture of record
DEL-04-03 RS_RECORD.valid.host-destinations.example.jsonl.

Nothing here observes a host, a native layer or an MCP server. The MCP
discovery answers are scripted from the published revision 2026-07-28 as
LOOP §5.3 DF-7 quotes it; no server was contacted.
"""

import glob
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DESIGN = os.path.dirname(HERE)
EXEC_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(DESIGN))))
PKG04 = glob.glob(os.path.join(EXEC_ROOT, "PKG-04_*", "1_Working"))[0]
RS_DIR = glob.glob(os.path.join(PKG04, "DEL-04-03_*", "Design"))[0]
AS_DIR = glob.glob(os.path.join(PKG04, "DEL-04-02_*", "Design"))[0]
ACT_DIR = glob.glob(os.path.join(PKG04, "DEL-04-01_*", "Design"))[0]

sys.path.insert(0, HERE)
import schema_subset  # noqa: E402  (LOOP's subset validator)
sys.path.insert(0, os.path.join(RS_DIR, "prototype"))
from minischema import Registry, validate as rs_validate  # noqa: E402

REVISION = "2026-07-28"
DECLINE = "destination not allowed by the person"
NOT_ALLOWED = "destination not allowed"
CATEGORIES = ("web access", "MCP servers", "other APIs")


# --------------------------------------------------------------------------
# Scripted native layer: DF-3 (the allow rule) and DF-7 (stateless evidence)
# --------------------------------------------------------------------------
def stateless_evidence(server):
    """DF-7: SE-1 discovery lists the revision; SE-2 modern requests only;
    SE-3 no session identifier seen. Returns the RS statelessEvidence body."""
    se1 = REVISION in server.get("discover_supported", [])
    se2 = server.get("modern_only", False)
    se3_ok = not server.get("session_id_seen", False)
    verdict = "stateless revision declared" if (se1 and se2 and se3_ok) else "not stateless"
    return {"discoverListsRevision": se1, "modernRequestsOnly": se2,
            "sessionIdentifierSeen": not se3_ok, "verdict": verdict, "time": "t0"}


class NativeLayer:
    def __init__(self, settings):
        self.s = settings
        self.grants = []            # in-work grants in force: dicts

    def allow(self, category, destination, traffic="call", carried_for=None, run="run"):
        """DF-3 A-1...A-7. Returns (step, allowed, reason, allowed_by)."""
        s = self.s
        if destination in s["model_service"]:                              # A-1
            return "A-1", True, None, {"kind": "model choice"}
        if traffic in s.get("always_off", {}):                             # A-2
            if s["always_off"][traffic]:
                return "A-2", True, None, {"kind": "category"}
            return "A-2", False, "always-off item", None
        if category == "MCP servers":                                      # A-3
            srv = s.get("mcp", {}).get(destination)
            if srv is None or stateless_evidence(srv)["verdict"] != "stateless revision declared":
                return "A-3", False, "not stateless MCP (2026-07-28)", None
        if (category, destination) in s.get("named", set()):              # A-4
            return "A-4", True, None, {"kind": "named entry"}
        if s.get("switches", {}).get(category):                            # A-5
            return "A-5", True, None, {"kind": "category"}
        for g in self.grants:                                              # A-6
            if g["state"] != "in force":
                continue
            covers = g["target"].get("destination") == destination or (
                "destination" not in g["target"] and g["target"]["category"] == category)
            if not covers:
                continue
            if g["scope"] == "once" and g["carried_for"] != carried_for:
                continue
            return "A-6", True, None, {"kind": "in-work grant", "grantRef": g["ref"], "scope": g["scope"]}
        return "A-7", False, "not allowed", None                          # A-7


# --------------------------------------------------------------------------
# The loop side: V-D, the in-work request, results in TL-2 classes
# --------------------------------------------------------------------------
class Run:
    def __init__(self, run_id, settings, prompt_available=True):
        self.run_id = run_id
        self.nl = NativeLayer(settings)
        self.prompt_available = prompt_available
        self.entries = []
        self.requests = {}
        self.results = {}
        self.seq = 0

    # RS entry writer (header per RS §13.2)
    def rs(self, kind, body, role):
        self.seq += 1
        rid = f"rec:host-E:{self.run_id.split(':')[1].lower()}:{self.seq:04d}"
        ident = {"host loop": "host-loop:E", "host native layer": "host-native:E",
                 "host control": "host-control:E"}[role]
        self.entries.append({"format": "chirality.rs.record", "formatVersion": "0.1", "recordId": rid,
                             "kind": kind, "recorder": {"role": role, "identity": ident},
                             "context": {"surface": "host", "hostIdentity": "FX-PIPE-01"},
                             "runId": self.run_id, "seq": self.seq, "writtenAt": f"w{self.seq:03d}",
                             "body": body})
        return rid

    def contact(self, category, destination, allowed_by, t, model_class=None):
        body = {"destination": destination, "category": category, "allowedBy": allowed_by, "time": t}
        if model_class:
            body["modelServiceClass"] = model_class
        return self.rs("destination_contacted", body, "host native layer")

    def model_request(self, t="t1"):
        step, ok, reason, by = self.nl.allow("model service", self.nl.s["model_service"][0], traffic="model")
        assert ok and step == "A-1"
        self.contact("model service", self.nl.s["model_service"][0], by, t, self.nl.s["model_class"])

    def traffic(self, kind, category, destination, t):
        """Traffic not from a declared call (e.g. a library's telemetry): at contact only."""
        step, ok, reason, by = self.nl.allow(category, destination, traffic=kind)
        if ok:
            self.contact(category, destination, by, t)
            return "sent"
        self.rs("boundary_refusal", {"destination": destination, "category": category, "stage": "at contact",
                                     "reason": reason, "time": t}, "host native layer")
        return "refused"

    def start_server(self, server_id, t):
        srv = self.nl.s["mcp"][server_id]
        ev = stateless_evidence(srv)
        if ev["verdict"] != "stateless revision declared":
            self.rs("boundary_refusal", {"destination": server_id, "category": "MCP servers", "stage": "at contact",
                                         "reason": "not stateless MCP (2026-07-28)", "time": t}, "host native layer")
            return "not started"
        limit = None
        body = {"processId": server_id, "declaredDestinations": srv.get("declares", []),
                "sandboxed": srv.get("sandboxed", False), "statelessEvidence": ev}
        pid = self.rs("outside_process", body, "host loop")
        if not body["sandboxed"]:
            limit = self.rs("evidence_limit", {"label": "process network not observed", "subjectRef": server_id},
                            "host loop")
        self.rs("evidence_limit", {"label": "stateless revision declared, not verified", "subjectRef": server_id},
                "host loop")
        return "started" + (" (process network not observed)" if limit else "")

    def direct_call(self, call, category, destination, t):
        """A call to an entry with an external-contact declaration: V-D (DF-4 (b))."""
        step, ok, reason, by = self.nl.allow(category, destination, carried_for=call)
        if ok:
            self.contact(category, destination, by, t)
            if by["kind"] == "in-work grant" and by["scope"] == "once":
                self.consume(by["grantRef"])
            self.results[call] = {"class": 3, "label": "success (ran)", "reporter": "host"}
        else:
            self.rs("boundary_refusal", {"destination": destination, "category": category, "stage": "V-D",
                                         "reason": reason, "requestingCall": call, "time": t}, "host native layer")
            r = {"class": 2, "label": NOT_ALLOWED, "reporter": "native layer", "reason": reason}
            if reason == "not allowed":
                r["offer"] = "a destination request may be made"
            self.results[call] = r
        return self.results[call]

    def plain_call(self, call):
        """A call to an entry without an external-contact declaration: no V-D (DF-1)."""
        self.results[call] = {"class": 3, "label": "success (ran)", "reporter": "host"}
        return self.results[call]

    def consume(self, grant_ref):
        for g in self.nl.grants:
            if g["ref"] == grant_ref and g["scope"] == "once":
                g["state"] = "consumed"

    def request(self, call, target, purpose, scope, carried=None, t="t"):
        """DF-5 Q-1...Q-5. carried = (operation reference, category, destination)."""
        rec = {"basis": "LOOP-v0.8 §5.3", "requestCall": call, "requester": "host-agent:E",
               "target": target, "purpose": purpose, "scopeSought": scope}
        if carried:
            rec["carriedCall"] = {"operationReference": carried[0], "argumentText": json.dumps({"to": carried[2]}),
                                  "destination": {"category": carried[1], "destination": carried[2]}}
        # Q-2: V-3 on the request entry: scope once requires a carried call (ACT ND-A2)
        if scope == "once" and not carried:
            self.results[call] = {"class": 1, "label": "schema", "reporter": "loop"}
            return "rejected at V-3"
        cat = target["category"]
        dest = target.get("destination", carried[2] if carried else None)
        step, ok, reason, by = self.nl.allow(cat, dest, carried_for=call)
        rec["check"] = {"step": step, "allowed": ok}
        if reason:
            rec["check"]["reason"] = reason
        self.requests[call] = rec
        if ok:                                                     # Q-3 already allowed
            if carried:
                self.dispatch_carried(call, t)
            else:
                self.results[call] = {"class": 3, "label": "already allowed", "reporter": "native layer"}
            self.requests.pop(call)
            return "already allowed"
        body = {"requester": "host-agent:E", "target": target, "purpose": purpose, "scopeSought": scope,
                "requestingCall": call, "time": t}
        if carried:
            body["carriedCall"] = carried[0]
        if reason in ("not stateless MCP (2026-07-28)", "always-off item"):   # Q-3 not grantable
            rec["req_ref"] = self.rs("destination_requested", body, "host loop")
            return self.close(call, "not granted", reason="not grantable", t=t, result_reason=reason)
        if not self.prompt_available:                              # DF-F4
            rec["req_ref"] = self.rs("destination_requested", body, "host loop")
            return self.close(call, "not granted", reason="prompt not shown", t=t, result_reason="prompt not shown")
        rec["req_ref"] = self.rs("destination_requested", body, "host loop")    # Q-4
        rec["state"] = "pending"
        rec["interimNotice"] = "waiting for the person's answer"         # Q-5
        return "pending"

    def dispatch_carried(self, call, t):
        rec = self.requests[call]
        cc = rec["carriedCall"]["destination"]
        step, ok, reason, by = self.nl.allow(cc["category"], cc["destination"], carried_for=call)
        assert ok, (call, step, reason)
        self.contact(cc["category"], cc["destination"], by, t)
        if by["kind"] == "in-work grant" and by["scope"] == "once":
            self.consume(by["grantRef"])
        self.results[call] = {"class": 3, "label": "success (ran)", "reporter": "host", "deferred": True}
        rec["result"] = self.results[call]

    def close(self, call, state, reason=None, cause=None, t="t", result_reason=None):
        rec = self.requests[call]
        rec["state"] = state
        body = {"requestRef": rec["req_ref"], "state": state, "carriedCallSent": False, "time": t}
        if reason:
            body["reason"] = reason
            rec["stateReason"] = reason
        if cause:
            body["cause"] = cause
            rec["endCause"] = cause
        self.rs("destination_request_closed", body, "host loop")
        if state == "not granted":
            r = {"class": 2, "label": NOT_ALLOWED, "reporter": "native layer" if reason == "not grantable"
                 else "host control", "reason": result_reason or reason, "deferred": reason == "grant refused by control"}
            self.results[call] = r
            rec["result"] = r
        return state

    def answer(self, call, answer, scope=None, t="t"):
        """DF-5 Q-6...Q-9."""
        rec = self.requests[call]
        assert rec.get("state") == "pending"
        if answer in ("run ended", "turn cancelled"):                          # Q-9
            return self.close(call, "unanswered at end", cause=answer, t=t)
        if answer == "decline":                                                # Q-8
            decl = self.rs("act_declined", ACT_DECLINED(call, rec, t), "host control")
            self.rs("destination_declined", {"target": rec["target"], "time": t, "requestingCall": call,
                                             "requestRef": rec["req_ref"], "actDeclinedRef": decl,
                                             "reportedToAgent": DECLINE}, "host control")
            rec["state"] = "declined"
            rec["result"] = self.results[call] = {"class": 2, "label": DECLINE, "reporter": "host control",
                                                  "deferred": True}
            return "declined"
        effect = {"grant": "established", "control refuses": "refused", "confirmation lost": "unconfirmed"}[answer]
        a12 = self.rs("human_act", A12(call, rec, scope, t, effect), "host control")               # Q-6
        if effect == "refused":
            return self.close(call, "not granted", reason="grant refused by control", t=t,
                              result_reason="grant refused by control: not stateless MCP (2026-07-28)")
        if effect == "unconfirmed":                                            # DF-F5: stays pending
            return "pending"
        gref = self.rs("destination_grant", {"form": "in-work grant", "target": rec["target"], "scope": scope,
                                             "time": t, "source": "in-work", "a12ActRef": a12,
                                             "requestRef": rec["req_ref"]}, "host control")
        self.nl.grants.append({"ref": gref, "target": rec["target"], "scope": scope, "state": "in force",
                               "carried_for": call})
        if scope == "always":
            tgt = rec["target"]
            if "destination" in tgt:
                self.nl.s.setdefault("named", set()).add((tgt["category"], tgt["destination"]))
            else:
                self.nl.s.setdefault("switches", {})[tgt["category"]] = True
        rec["state"] = "granted"
        rec["grantScope"] = scope
        if "carriedCall" in rec:                                               # Q-7
            self.dispatch_carried(call, t)
        else:
            rec["result"] = self.results[call] = {"class": 3, "label": f"granted: {scope}",
                                                  "reporter": "host control", "deferred": True}
        return "granted"

    def loop_record(self, call):
        rec = {k: v for k, v in self.requests[call].items() if k != "req_ref"}
        if rec.get("state") != "pending":
            rec.pop("interimNotice", None) if rec.get("state") in (None,) else None
        return rec


def A12(call, rec, scope, t, effect):
    target = rec["target"]
    subj = f"destination {target.get('destination', target['category'])} ({target['category']})"
    return {"actKind": "A12", "a12Subclass": "network-destination grant",
            "actClass": {"value": "reserved to the person"},
            "governingPolicy": {"policyRevision": "DEL-04-01/ACT-POLICY-v0.8", "recordId": "P-01"},
            "decisionActor": {"hostActor": "Engineer A", "identityVerified": False},
            "recordingMode": "direct capture", "boundSubject": [subj],
            "boundContent": [{"method": "setting content", "value": f"{target.get('destination', target['category'])}/{scope}/{call}"}],
            "scope": f"{scope}: {call}", "purpose": "allow the destination the agent asked for",
            "captureEvidence": [{"kind": "capture evidence", "ref": f"cap:grant-{call}", "resolutionAtWrite": "resolved"}],
            "captureTime": t, "evidenceLimits": ["identity not verified"],
            "relations": {"requestRef": rec["req_ref"], "controlEffect": {"state": effect}}}


def ACT_DECLINED(call, rec, t):
    target = rec["target"]
    return {"actor": {"hostActor": "Engineer A", "identityVerified": False}, "declinedKind": "A12",
            "a12Subclass": "network-destination grant",
            "subject": [f"destination {target.get('destination', target['category'])} ({target['category']})"],
            "time": t, "captureEvidence": [{"kind": "capture evidence", "ref": f"cap:decline-{call}",
                                            "resolutionAtWrite": "resolved"}]}


# --------------------------------------------------------------------------
# Settings and cases (LOOP §5.2 MS-14...MS-27; invented subjects)
# --------------------------------------------------------------------------
def base_settings(**kw):
    s = {"model_service": ["M1 model service"], "model_class": "cloud",
         "switches": {"web access": True, "MCP servers": False, "other APIs": False},
         "named": {("MCP servers", "M-1")},
         "always_off": {"telemetry": False},
         "mcp": {"M-1": {"discover_supported": [REVISION], "modern_only": True, "declares": ["D-1"], "sandboxed": False},
                 "M-2": {"discover_supported": ["2025-11-25"], "modern_only": False},
                 "M-3": {"legacy": True},
                 "M-4": {"discover_supported": [REVISION], "modern_only": True, "session_id_seen": True}}}
    s.update(kw)
    return s


def case_ms14(r):
    return r.direct_call("call:1", "web access", "W-1", "t2")["label"]


def case_ms15(r):
    started = r.start_server("M-1", "t2")
    res = r.direct_call("call:2", "MCP servers", "M-1", "t3")
    return f"{started}; {res['label']}"


def case_ms16(r):
    r.request("call:3", {"category": "other APIs", "destination": "A-1"}, "read invented table", "once",
              carried=("OP-A1", "other APIs", "A-1"), t="t3")
    r.answer("call:3", "grant", "once", "t4")
    again = r.direct_call("call:4", "other APIs", "A-1", "t5")
    return f"{r.results['call:3']['label']}; later call: {again['label']}"


def case_ms17(r):
    r.request("call:5", {"category": "other APIs", "destination": "A-1"}, "read invented table", "this run", t="t3")
    r.answer("call:5", "grant", "this run", "t4")
    return f"{r.results['call:5']['label']}; within run: {r.direct_call('call:6', 'other APIs', 'A-1', 't5')['label']}"


def case_ms18(r):
    r.request("call:7", {"category": "other APIs"}, "read invented tables", "always", t="t3")
    r.answer("call:7", "grant", "always", "t4")
    return f"{r.results['call:7']['label']}; switch other APIs on: {r.nl.s['switches']['other APIs']}"


def case_ms19(r):
    r.request("call:8", {"category": "other APIs", "destination": "A-2"}, "upload invented summary", "once",
              carried=("OP-A2", "other APIs", "A-2"), t="t3")
    r.answer("call:8", "decline", t="t4")
    return r.results["call:8"]["label"]


def case_ms20(r):
    r.request("call:9", {"category": "MCP servers", "destination": "M-2"}, "use invented tool", "this run", t="t3")
    return f"{r.requests['call:9']['state']} ({r.requests['call:9']['stateReason']}); {r.results['call:9']['label']}"


def case_ms21(r):
    return r.start_server("M-1", "t2")


def case_ms22(r):
    # An agent-written list entry is never a grant: the settings are unchanged, V-D still refuses.
    return r.direct_call("call:10", "other APIs", "A-3", "t3")["label"]


def case_ms23(r):
    r.nl.s["switches"]["web access"] = False      # MS-23: web access switched off
    res = r.direct_call("call:11", "web access", "W-2", "t3")
    return f"{res['label']} ({res['reason']}); {res.get('offer', '')}"


def case_ms24(r):
    case_ms23(r)
    r.request("call:12", {"category": "web access", "destination": "W-2"}, "read invented standard table", "once",
              carried=("OP-W1", "web access", "W-2"), t="t4")
    other = r.plain_call("call:13")     # an OP-C1 read of R-100 (no external contact) runs meanwhile (NW-12)
    r.answer("call:12", "grant", "once", "t5")
    consumed = [g["state"] for g in r.nl.grants]
    return f"{r.results['call:12']['label']}; other call {other['label']}; grant {consumed}"


def case_ms25a(r):
    r.nl.s["switches"]["web access"] = False
    r.request("call:14", {"category": "web access", "destination": "W-2"}, "read invented table", "once",
              carried=("OP-W1", "web access", "W-2"), t="t4")
    return r.answer("call:14", "turn cancelled", t="t5") + f"; result delivered: {'call:14' in r.results}"


def case_ms25b(r):
    r.nl.s["switches"]["web access"] = False
    r.request("call:15", {"category": "web access", "destination": "W-2"}, "read invented table", "once",
              carried=("OP-W1", "web access", "W-2"), t="t4")
    return r.answer("call:15", "run ended", t="t5") + f"; result delivered: {'call:15' in r.results}"


def case_ms26(r):
    out = [r.start_server(x, "t2") for x in ("M-1", "M-3", "M-4")]
    vd = r.direct_call("call:16", "MCP servers", "M-4", "t3")
    return f"{'; '.join(out)}; V-D M-4: {vd['label']} ({vd['reason']})"


def case_ms27(r_factory):
    r = r_factory(prompt_available=False)
    a = r.request("call:17", {"category": "other APIs", "destination": "A-4"}, "read invented table", "once",
                  carried=("OP-A4", "other APIs", "A-4"), t="t3")
    r2 = r_factory()
    r2.request("call:18", {"category": "other APIs", "destination": "A-5"}, "read invented table", "once",
               carried=("OP-A5", "other APIs", "A-5"), t="t3")
    b = r2.answer("call:18", "control refuses", "once", "t4")
    r3 = r_factory()
    r3.request("call:19", {"category": "other APIs", "destination": "A-6"}, "read invented table", "once",
               carried=("OP-A6", "other APIs", "A-6"), t="t3")
    c = r3.answer("call:19", "confirmation lost", "once", "t4")
    return (f"(a) {a} ({r.requests['call:17']['stateReason']}); (b) {b} ({r2.requests['call:18']['stateReason']}); "
            f"(c) {c}, carried call sent: {'call:19' in r3.results}"), [r, r2, r3]


def case_ms06(r):
    return r.traffic("telemetry", "web access", "T-9", "t2")


CASES = [
    ("MS-06", case_ms06, "refused"),
    ("MS-14", case_ms14, "success (ran)"),
    ("MS-15", case_ms15, "started (process network not observed); success (ran)"),
    ("MS-16", case_ms16, "success (ran); later call: destination not allowed"),
    ("MS-17", case_ms17, "granted: this run; within run: success (ran)"),
    ("MS-18", case_ms18, "granted: always; switch other APIs on: True"),
    ("MS-19", case_ms19, DECLINE),
    ("MS-20", case_ms20, "not granted (not grantable); destination not allowed"),
    ("MS-21", case_ms21, "started (process network not observed)"),
    ("MS-22", case_ms22, NOT_ALLOWED),
    ("MS-23", case_ms23, "destination not allowed (not allowed); a destination request may be made"),
    ("MS-24", case_ms24, "success (ran); other call success (ran); grant ['consumed']"),
    ("MS-25a", case_ms25a, "unanswered at end; result delivered: False"),
    ("MS-25b", case_ms25b, "unanswered at end; result delivered: False"),
    ("MS-26", case_ms26, "started (process network not observed); not started; not started; "
                         "V-D M-4: destination not allowed (not stateless MCP (2026-07-28))"),
    ("MS-27", None, "(a) not granted (prompt not shown); (b) not granted (grant refused by control); "
                    "(c) pending, carried call sent: False"),
]


def main(argv):
    emit = argv[argv.index("--emit") + 1] if "--emit" in argv else None
    reg = Registry()
    ids = {}
    for name, d, f in (("ACT", ACT_DIR, "ACT_POLICY_CLASS_RECORD.schema.json"),
                       ("AS", AS_DIR, "AS_SETTINGS_IN.schema.json"),
                       ("RS", RS_DIR, "RS_RECORD.schema.json")):
        ids[name] = reg.load(os.path.join(d, f))
    rs_schema = reg.by_id[ids["RS"]]
    loop_schema = json.load(open(os.path.join(DESIGN, "LOOP_DESTINATION_REQUEST.schema.json"), encoding="utf-8"))
    ok = True
    n_entries = n_records = 0
    for name, fn, expect in CASES:
        runs = []

        def factory(prompt_available=True, _name=name):
            r = Run(f"run:{_name}", base_settings(), prompt_available)
            r.model_request()
            runs.append(r)
            return r
        if fn is None:
            got, _ = case_ms27(factory)
        else:
            got = fn(factory())
        good = got == expect
        errs = []
        for r in runs:
            for e in r.entries:
                n_entries += 1
                errs += [f"{e['recordId']} {x}" for x in rs_validate(e, rs_schema, reg)[:1]]
            for call in r.requests:
                n_records += 1
                errs += [f"{call} {x}" for x in schema_subset.validate(r.loop_record(call), loop_schema)[:1]]
        good = good and not errs
        ok &= good
        print(f"{'PASS' if good else 'FAIL'} {name:7s} {got}" + ("" if got == expect else f"   expected: {expect}"))
        for x in errs:
            print("     schema:", x)
    # The invalid LOOP example must be refused, the valid one accepted.
    v = schema_subset.validate(json.load(open(os.path.join(DESIGN, "LOOP_DESTINATION_REQUEST.example.valid.json"))), loop_schema)
    iv = schema_subset.validate(json.load(open(os.path.join(DESIGN, "LOOP_DESTINATION_REQUEST.example.invalid.json"))), loop_schema)
    print(f"{'PASS' if not v else 'FAIL'} example valid accepted; {'PASS' if iv else 'FAIL'} example invalid refused ({len(iv)} reasons)")
    ok &= (not v) and bool(iv)
    print(f"RS entries validated: {n_entries}; loop request records validated: {n_records}")
    if emit:
        e14 = Run("run:E-14", base_settings())
        e14.model_request("t1")
        case_ms23(e14)
        e14.request("call:12", {"category": "web access", "destination": "W-2"}, "read invented standard table",
                    "once", carried=("OP-W1", "web access", "W-2"), t="t4")
        e14.answer("call:12", "grant", "once", "t5")
        e14.start_server("M-1", "t6")
        e14.start_server("M-4", "t7")
        e14.request("call:14", {"category": "other APIs", "destination": "A-4"}, "read invented table", "once",
                    carried=("OP-A4", "other APIs", "A-4"), t="t8")
        e14.answer("call:14", "turn cancelled", t="t9")
        for e in e14.entries:
            assert not rs_validate(e, rs_schema, reg), e
        with open(emit, "w", encoding="utf-8") as fh:
            for e in e14.entries:
                fh.write(json.dumps(e, ensure_ascii=False) + "\n")
        print(f"wrote {len(e14.entries)} entries to {emit}")
    print("RESULT:", "all expectations held" if ok else "failures")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
