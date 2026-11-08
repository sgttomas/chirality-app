"""Scenarios for supplier_double.py. Prototype only (DEL-01-01, Wave B node B6).

Every frame here is `constructed` (HOSTING §9.2): it was not recorded from the
supplier. Shapes follow the committed 0.158.0 JSON Schema bundle, and
run_cases.py validates every constructed frame against that bundle (except
the frames that are unfamiliar or malformed by design, which are marked).
All content is invented example material (V4-CST-06): thread, turn, item and
server names are "example" identities, not observations.
"""

THREAD, TURN = "thr-ex-1", "turn-ex-1"


def _req(rid, method, params, note=None):
    return {"emit": {"id": rid, "method": method, "params": params},
            "standing": "constructed", "note": note}


def _note(method, params, note=None, delay=None):
    a = {"emit": {"method": method, "params": params}, "standing": "constructed",
         "note": note}
    if delay is not None:
        a["delay"] = delay
    return a


def _resp(frame, result):
    return [{"emit": {"id": frame["id"], "result": result}, "standing": "constructed",
             "responds_to": frame["method"]}]


def cmd_approval(rid, item):
    return _req(rid, "item/commandExecution/requestApproval", {
        "threadId": THREAD, "turnId": TURN, "itemId": item, "startedAtMs": 1790000000000,
        "command": "./example-tool --sample", "cwd": "/example/cwd",
        "reason": "invented example"})


def file_approval(rid, item):
    return _req(rid, "item/fileChange/requestApproval", {
        "threadId": THREAD, "turnId": TURN, "itemId": item, "startedAtMs": 1790000000000,
        "reason": "invented example"})


def user_input(rid, item):
    return _req(rid, "item/tool/requestUserInput", {
        "threadId": THREAD, "turnId": TURN, "itemId": item, "isBlocking": True,
        "questions": [{"id": "q-ex-1", "header": "Example",
                       "question": "Invented example question?"}]})


def elicitation(rid, message):
    return _req(rid, "mcpServer/elicitation/request", {
        "threadId": THREAD, "turnId": TURN, "serverName": "example-host",
        "mode": "form", "message": message,
        "requestedSchema": {"type": "object", "properties": {
            "answer": {"type": "string"}}}})


def current_time(rid):
    return _req(rid, "currentTime/read", {"threadId": THREAD})


def mcp_item(status, item_id="item-ex-3"):
    item = {"type": "mcpToolCall", "id": item_id, "server": "example-host",
            "tool": "example_lookup", "arguments": {"key": "EX-1"}, "status": status}
    if status == "completed":
        item["result"] = {"content": [{"type": "text", "text": "invented example result"}]}
    return item


class Scenario:
    """Default: the recorded handshake only; nothing after `initialized`."""

    def on_initialize(self, ctx, frame):
        return None  # None = use the recorded initialize response

    def after_initialize_response(self, ctx):
        return []  # frames sent before the client's `initialized`

    def after_initialized(self, ctx):
        return []

    def on_request(self, ctx, frame):
        return None  # None = constructed "no scripted response" error

    def on_client_response(self, ctx, frame):
        return []


class EarlyRequest(Scenario):  # VC-16 (b): server requests while handshaking
    def after_initialize_response(self, ctx):
        return [cmd_approval("srv-p1", "item-ex-1"),
                _req("srv-p2", "chirality/b6UnfamiliarKind", {},
                     note="unfamiliar by design; exempt from bundle validation")]


class Unfamiliar(Scenario):  # VC-03 (X-07)
    def after_initialized(self, ctx):
        a = _req("srv-u1", "chirality/b6UnfamiliarKind", {},
                 note="unfamiliar by design; exempt from bundle validation")
        return [a]


class Capabilities(Scenario):  # VC-20
    def after_initialized(self, ctx):
        return [current_time("srv-c1"), _req("srv-c2", "attestation/generate", {})]


class Origin(Scenario):  # VC-22
    def after_initialized(self, ctx):
        return [user_input("srv-o1", "item-ex-1"), file_approval("srv-o2", "item-ex-2"),
                elicitation("srv-o3", "Invented example: confirm the example lookup?"),
                current_time("srv-o4")]


class Elicit(Scenario):  # VC-23
    def after_initialized(self, ctx):
        return [elicitation("srv-e1",
                            "Invented example: accept change item CI-EX-1 on the example host?")]


class Settlement(Scenario):  # VC-14 (X-12)
    def after_initialized(self, ctx):
        return [cmd_approval("srv-s1", "item-ex-1"), file_approval("srv-s2", "item-ex-2"),
                cmd_approval("srv-s3", "item-ex-3"),
                _note("serverRequest/resolved", {"threadId": THREAD, "requestId": "srv-s3"},
                      note="supplier-reported resolution before any answer", delay=0.3)]

    def on_client_response(self, ctx, frame):
        if frame.get("id") in ("srv-s1", "srv-s2"):
            return [_note("serverRequest/resolved", {"threadId": THREAD, "requestId": frame["id"]},
                          note="after the App's written reply")]
        return []


class WriteFail(Scenario):  # VC-14 settle-write-failed; generation closed
    def after_initialized(self, ctx):
        return [cmd_approval("srv-w1", "item-ex-1"), cmd_approval("srv-w2", "item-ex-2"),
                {"close_stdin": True}, {"exit": 0, "delay": 1.2}]


class Malformed(Scenario):  # VC-04 (X-08)
    def after_initialized(self, ctx):
        big = '{"method":"warning","params":{"message":"' + "x" * 300000 + '"}}'
        return [
            {"emit_raw": "this is not json", "note": "malformed by design"},
            {"emit_raw": "[1,2,3]", "note": "malformed by design (not an object)"},
            {"emit_raw": '{"neither":true}', "note": "malformed by design (unclassifiable)"},
            {"emit_raw": big, "note": "oversize by design (300,041 bytes)"},
            _note("warning", {"message": "invented example warning", "threadId": THREAD},
                  note="valid, no version member (as every recorded supplier frame)"),
            _note("thread/status/changed", {"threadId": THREAD, "status": {"type": "idle"}}),
        ]


class ExitOnInitialize(Scenario):  # VC-06: handshake failure
    def on_initialize(self, ctx, frame):
        return [{"exit": 0}]


class ExitAfterReady(Scenario):  # VC-06 (b): unexpected exit with outstanding work
    def after_initialized(self, ctx):
        return [cmd_approval("srv-x1", "item-ex-1"), {"exit": 0, "delay": 0.6}]

    def on_request(self, ctx, frame):
        if frame["method"] == "thread/list":
            return [{"ignore": True, "note": "left without response by design"}]
        return None


def _mcp_status_response(frame):
    return _resp(frame, {"data": [{
        "name": "example-host", "authStatus": "unsupported", "runtimeStatus": "disabled",
        "httpOrigin": None, "resources": [], "resourceTemplates": [],
        "tools": {"example_lookup": {"name": "example_lookup",
                                     "description": "Invented example tool",
                                     "inputSchema": {"type": "object"}}}}],
        "nextCursor": None})


def _mcp_call_response(frame):
    return _resp(frame, {"content": [{"type": "text", "text": "invented example result"}],
                         "isError": False, "structuredContent": {"outcome": "example"}})


class Mcp(Scenario):  # VC-24
    def after_initialized(self, ctx):
        return [
            _note("mcpServer/startupStatus/updated", {"name": "example-host", "status": "ready"}),
            _note("item/started", {"threadId": THREAD, "turnId": TURN, "startedAtMs": 1790000000100,
                                   "item": mcp_item("inProgress")}),
            _note("item/completed", {"threadId": THREAD, "turnId": TURN,
                                     "completedAtMs": 1790000000200,
                                     "item": mcp_item("completed")}),
        ]

    def on_request(self, ctx, frame):
        if frame["method"] == "mcpServerStatus/list":
            return _mcp_status_response(frame)
        if frame["method"] == "mcpServer/tool/call":
            return _mcp_call_response(frame)
        return None


class Hold(Scenario):  # VC-25
    def after_initialized(self, ctx):
        review = {"status": "approved"}
        action = {"type": "command", "command": "./example-tool --list", "cwd": "/example/cwd",
                  "source": "shell"}
        return [
            cmd_approval("srv-h1", "item-ex-7"),
            _note("item/autoApprovalReview/started", {
                "threadId": THREAD, "turnId": TURN, "reviewId": "rev-ex-1",
                "startedAtMs": 1790000000300, "targetItemId": "item-ex-8",
                "review": review, "action": action}),
            _note("item/autoApprovalReview/completed", {
                "threadId": THREAD, "turnId": TURN, "reviewId": "rev-ex-1",
                "startedAtMs": 1790000000300, "completedAtMs": 1790000000400,
                "targetItemId": "item-ex-8", "decisionSource": "agent",
                "review": review, "action": action}),
            _note("item/completed", {"threadId": THREAD, "turnId": TURN,
                                     "completedAtMs": 1790000000500, "item": {
                                         "type": "commandExecution", "id": "item-ex-8",
                                         "command": "./example-tool --list",
                                         "cwd": "/example/cwd", "commandActions": [],
                                         "status": "completed", "exitCode": 0,
                                         "aggregatedOutput": "invented example output"}}),
        ]

    def on_request(self, ctx, frame):
        m = frame["method"]
        if m == "mcpServer/tool/call":
            return _mcp_call_response(frame)
        if m == "turn/start":
            return _resp(frame, {"turn": {"id": "turn-ex-2", "items": [], "status": "inProgress"}})
        if m == "turn/interrupt":
            return _resp(frame, {})
        return None


class Destination(Scenario):  # VC-26
    def on_request(self, ctx, frame):
        m = frame["method"]
        if m == "thread/start":
            p = frame.get("params", {})
            return _resp(frame, {
                "model": p.get("model", "example-model-a"),
                "modelProvider": p.get("modelProvider", "example-local"),
                "approvalPolicy": "on-request", "approvalsReviewer": "user",
                "cwd": "/example/cwd", "sandbox": {"type": "readOnly"},
                "thread": {"id": THREAD, "cliVersion": "0.158.0", "createdAt": 1790000000,
                           "updatedAt": 1790000000, "cwd": "/example/cwd", "ephemeral": True,
                           "modelProvider": p.get("modelProvider", "example-local"),
                           "preview": "", "projectId": None, "sessionId": "ses-ex-1",
                           "source": "appServer", "status": {"type": "idle"}, "turns": []}})
        if m == "turn/start":
            ctx["counter"] += 1
            turn_id = "turn-ex-%d" % ctx["counter"]
            acts = _resp(frame, {"turn": {"id": turn_id, "items": [], "status": "inProgress"}})
            if ctx["counter"] == 1:
                acts.append(_note("model/rerouted", {
                    "threadId": THREAD, "turnId": turn_id, "fromModel": "example-model-a",
                    "toModel": "example-model-b", "reason": "highRiskCyberActivity"},
                    note="constructed re-route (the only reason value in the bundle)"))
            return acts
        return None


SCENARIOS = {
    "default": Scenario, "early-request": EarlyRequest, "unfamiliar": Unfamiliar, "capabilities": Capabilities,
    "origin": Origin, "elicitation": Elicit, "settlement": Settlement,
    "writefail": WriteFail, "malformed": Malformed,
    "exit-on-initialize": ExitOnInitialize, "exit-after-ready": ExitAfterReady,
    "mcp": Mcp, "hold": Hold, "destination": Destination,
}


def get(name):
    return SCENARIOS[name]()
