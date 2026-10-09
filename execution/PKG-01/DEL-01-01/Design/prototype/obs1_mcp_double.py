#!/usr/bin/env python3
"""OBS-1 test tool, MCP path: a minimal stdio MCP server offering one tool.

Prototype only (DEL-01-01, Wave B node B6); a test double for the observation
OBS-1 (`_Coordination/AgentRuns/APP-V4-DESIGN-PASS-2-20260930/WAVE_B/OBS-1_BRIEF.md`).
Not product code. Python 3 standard library only. No network.

It answers `initialize` (echoing the client's protocol version), `ping`,
`tools/list` and `tools/call` over newline-delimited JSON-RPC 2.0 on stdio,
and replies -32601 to any other request. The one tool, `example_lookup`,
returns invented example material only:
  key "EX-1"   -> a normal result with text and structured content
                  {"outcome": "queued", "proposal": "P-EX-1", ...}
  key "EX-ERR" -> a tool-reported error (isError true)
Every message received and sent is logged with the wall-clock time in
milliseconds (comparable with the supplier's `startedAtMs`/`completedAtMs`)
to the file named by --log, so that OBS-1 can order the tool's receipt of a
call against the supplier's `item/started` (OBS-1 O-1). If the log cannot be
written (for example under a sandbox), that failure is itself reported on
stderr and in the tool result's `logWritable` element.

Usage: obs1_mcp_double.py --log PATH
"""
import argparse
import json
import sys
import time

TOOL = {
    "name": "example_lookup",
    "description": ("Look up an invented example record by key. Test tool for an "
                    "observation; returns invented example data only."),
    "inputSchema": {"type": "object",
                    "properties": {"key": {"type": "string",
                                           "description": "Example key, e.g. EX-1"}},
                    "required": ["key"]},
}
LOG_OK = True


def wall_ms():
    return int(time.time() * 1000)


def log(path, event):
    global LOG_OK
    event["wall_ms"] = wall_ms()
    try:
        with open(path, "a", encoding="utf-8") as f:
            f.write(json.dumps(event, ensure_ascii=False) + "\n")
    except OSError as exc:
        LOG_OK = False
        sys.stderr.write("obs1_mcp_double: log not writable: %r\n" % exc)


def send(path, obj):
    line = json.dumps(obj, separators=(",", ":"))
    sys.stdout.write(line + "\n")
    sys.stdout.flush()
    log(path, {"dir": "sent", "raw": line})


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--log", required=True)
    args = ap.parse_args()
    log(args.log, {"dir": "start"})
    for raw in sys.stdin:
        raw = raw.rstrip("\n")
        log(args.log, {"dir": "received", "raw": raw})
        try:
            msg = json.loads(raw)
        except ValueError:
            continue
        if not isinstance(msg, dict) or "id" not in msg or "method" not in msg:
            continue  # notifications (e.g. notifications/initialized) and responses
        rid, method, params = msg["id"], msg["method"], msg.get("params") or {}
        if method == "initialize":
            send(args.log, {"jsonrpc": "2.0", "id": rid, "result": {
                "protocolVersion": params.get("protocolVersion", "2025-06-18"),
                "capabilities": {"tools": {"listChanged": False}},
                "serverInfo": {"name": "obs1-example-host", "version": "0.0.0-test"}}})
        elif method == "ping":
            send(args.log, {"jsonrpc": "2.0", "id": rid, "result": {}})
        elif method == "tools/list":
            send(args.log, {"jsonrpc": "2.0", "id": rid, "result": {"tools": [TOOL]}})
        elif method == "tools/call":
            key = (params.get("arguments") or {}).get("key")
            received_ms = wall_ms()
            if params.get("name") != TOOL["name"]:
                send(args.log, {"jsonrpc": "2.0", "id": rid, "error": {
                    "code": -32602, "message": "unknown tool"}})
            elif key == "EX-ERR":
                send(args.log, {"jsonrpc": "2.0", "id": rid, "result": {
                    "content": [{"type": "text", "text": "Invented example error: EX-ERR not found."}],
                    "isError": True}})
            else:
                data = {"outcome": "queued", "proposal": "P-EX-1", "key": key,
                        "note": "invented example material", "toolReceivedAtMs": received_ms,
                        "logWritable": LOG_OK, "metaReceived": "_meta" in params}
                send(args.log, {"jsonrpc": "2.0", "id": rid, "result": {
                    "content": [{"type": "text", "text": json.dumps(data)}],
                    "structuredContent": data, "isError": False}})
        else:
            send(args.log, {"jsonrpc": "2.0", "id": rid, "error": {
                "code": -32601, "message": "method not found: " + str(method)}})


if __name__ == "__main__":
    main()
