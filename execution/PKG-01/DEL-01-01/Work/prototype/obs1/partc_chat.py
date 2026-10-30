#!/usr/bin/env python3
"""OBS-1 part C: three direct Chat Completions requests to the local LM Studio server.

Prototype only (DEL-01-01, run APP-V4-DESIGN-PASS-2-20260930, node OBS-1; LOOP
fixture basis, R12-8). Not a Codex turn. Python 3 standard library only;
loopback only (http://127.0.0.1:1234). Invented content only.

Requests (all streamed, so the raw server-sent events show how tool-call
fragments arrive):
  C1 one tool with one parameter      -> points 1 (fragments) and 2 (finish reason)
  C2 two calls asked for in one reply -> point 3 (several calls in one response)
  C3 a tool with no parameters        -> point 4 (the argument text sent)
Raw SSE lines are written unchanged to <out>/C<n>.sse; a summary to <out>/partc_summary.json.

Usage: partc_chat.py --model KEY --out DIR
"""
import argparse
import json
import os
import time
import urllib.request

URL = "http://127.0.0.1:1234/v1/chat/completions"

LOOKUP = {"type": "function", "function": {
    "name": "example_lookup",
    "description": "Look up an invented example record by key. Test tool; invented data only.",
    "parameters": {"type": "object", "properties": {"key": {"type": "string", "description": "Example key, e.g. EX-1"}},
                   "required": ["key"]}}}
PING = {"type": "function", "function": {
    "name": "example_ping",
    "description": "Invented test function with no parameters. Call it to check the example service.",
    "parameters": {"type": "object", "properties": {}}}}

CASES = {
    "C1": {"tools": [LOOKUP], "messages": [
        {"role": "system", "content": "You are running an observation test with invented data. Use the tools when asked."},
        {"role": "user", "content": "This is a test with invented data. Call example_lookup with key EX-1."}]},
    "C2": {"tools": [LOOKUP], "messages": [
        {"role": "system", "content": "You are running an observation test with invented data. Use the tools when asked. You may call several tools at once."},
        {"role": "user", "content": "This is a test with invented data. In a single reply, call example_lookup twice at the same time: once with key EX-1 and once with key EX-2."}]},
    "C3": {"tools": [PING], "messages": [
        {"role": "system", "content": "You are running an observation test with invented data. Use the tools when asked."},
        {"role": "user", "content": "This is a test with invented data. Call example_ping."}]},
}


def run(case, model, out):
    body = dict(CASES[case])
    body.update({"model": model, "stream": True, "max_tokens": 2048})
    data = json.dumps(body).encode()
    req = urllib.request.Request(URL, data=data, headers={"Content-Type": "application/json"})
    proxy = urllib.request.ProxyHandler({})  # loopback: never a proxy
    opener = urllib.request.build_opener(proxy)
    t0 = time.time()
    lines = []
    with opener.open(req, timeout=600) as resp:
        status = resp.status
        headers = dict(resp.headers)
        for raw in resp:
            lines.append(raw.decode("utf-8", "replace").rstrip("\n"))
    with open(os.path.join(out, case + ".sse"), "w", encoding="utf-8") as f:
        f.write(json.dumps({"request": body}) + "\n")
        f.write("\n".join(lines) + "\n")
    # summarise
    calls = {}
    frag = []
    finish = []
    content = ""
    reasoning_chars = 0
    for l in lines:
        if not l.startswith("data: ") or l == "data: [DONE]":
            continue
        ev = json.loads(l[6:])
        for ch in ev.get("choices", []):
            d = ch.get("delta") or {}
            if d.get("content"):
                content += d["content"]
            if d.get("reasoning_content") or d.get("reasoning"):
                reasoning_chars += len(d.get("reasoning_content") or d.get("reasoning") or "")
            for tc in d.get("tool_calls") or []:
                idx = tc.get("index")
                fn = tc.get("function") or {}
                frag.append({"index": idx, "id": tc.get("id"), "type": tc.get("type"),
                             "name": fn.get("name"), "arguments_fragment": fn.get("arguments")})
                c = calls.setdefault(idx, {"id": None, "name": "", "arguments": ""})
                if tc.get("id"):
                    c["id"] = tc["id"]
                if fn.get("name"):
                    c["name"] += fn["name"]
                if fn.get("arguments") is not None:
                    c["arguments"] += fn["arguments"]
            if ch.get("finish_reason") is not None:
                finish.append(ch["finish_reason"])
    return {"case": case, "http_status": status, "server_header": headers.get("Server") or headers.get("server"),
            "elapsed_s": round(time.time() - t0, 1), "sse_lines": len(lines),
            "tool_call_fragments": frag, "assembled_calls": calls, "finish_reasons": finish,
            "content": content, "reasoning_chars": reasoning_chars}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    res = [run(c, a.model, a.out) for c in ("C1", "C2", "C3")]
    with open(os.path.join(a.out, "partc_summary.json"), "w", encoding="utf-8") as f:
        json.dump(res, f, indent=1)
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    main()
