#!/usr/bin/env python3
"""OBS-2 provider tap: a pass-through recorder between Codex and the local LM Studio server.

Prototype only (DEL-01-01, run APP-V4-DESIGN-PASS-3-20261001, node OBS-2). Not product
code. Python 3 standard library only. Loopback only: it listens on 127.0.0.1 and forwards
every request unchanged to the LM Studio server on 127.0.0.1:1234, streaming the response
back unchanged. It records each request (method, path, headers, body) and the size and
timing of each response, so the observation can see exactly what Codex sends to a
Responses provider (the tool list in particular). LM Studio's own log truncates request
bodies (OBS-1 section 5). Nothing is modified, nothing leaves the machine.

With --capture-only it forwards nothing: it records the request and answers HTTP 400 with an
invented error body, so a turn's request can be inspected without any model call.

With --flatten-namespaces it is an ADAPTER, not a pass-through: LM Studio 0.4.16 drops
Responses tools of type `namespace` ("Ignoring unsupported tool type(s): namespace", OBS-1),
and Codex 0.158.0 sends its delegation tools only inside a namespace (`multi_agent_v1`).
In this mode the tap replaces each namespace tool by its inner function tools before
forwarding, strips `namespace` from input items, and, in the streamed response, adds the
`namespace` back to any `function_call` item whose name belongs to a flattened namespace.
Everything else is forwarded unchanged and every rewrite is recorded. Codex is not modified.
Observations made through this mode are labelled "via the OBS-2 namespace adapter".

Usage: obs2_provider_tap.py --port 12340 --log FILE [--upstream-port 1234]
                            [--capture-only | --flatten-namespaces]
"""
import argparse
import http.client
import json
import sys
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

LOCK = threading.Lock()


def flatten_request(body, rewrites):
    """Return (new_body, name->namespace map). Records each rewrite in `rewrites`."""
    mapping = {}
    if not isinstance(body, dict):
        return body, mapping
    tools = body.get("tools")
    if isinstance(tools, list):
        flat = []
        for t in tools:
            if isinstance(t, dict) and t.get("type") == "namespace":
                for inner in t.get("tools") or []:
                    mapping[inner.get("name")] = t.get("name")
                    flat.append(inner)
                rewrites.append({"flattened_namespace": t.get("name"),
                                 "tools": [x.get("name") for x in t.get("tools") or []]})
            else:
                flat.append(t)
        body["tools"] = flat
    for it in body.get("input") or []:
        if isinstance(it, dict) and "namespace" in it:
            rewrites.append({"stripped_input_namespace": it.get("namespace"), "item_type": it.get("type"),
                             "name": it.get("name")})
            it.pop("namespace", None)
    return body, mapping


def restore_namespace(obj, mapping, rewrites):
    if isinstance(obj, dict):
        if obj.get("type") == "function_call" and obj.get("name") in mapping and not obj.get("namespace"):
            obj["namespace"] = mapping[obj["name"]]
            rewrites.append({"restored_namespace": obj["namespace"], "name": obj["name"],
                             "call_id": obj.get("call_id")})
        for v in obj.values():
            restore_namespace(v, mapping, rewrites)
    elif isinstance(obj, list):
        for v in obj:
            restore_namespace(v, mapping, rewrites)


def make_handler(log_path, upstream_port, capture_only=False, flatten=False):
    class Tap(BaseHTTPRequestHandler):
        protocol_version = "HTTP/1.0"  # close-delimited responses: stream through without re-framing

        def log_message(self, fmt, *args):  # keep stderr quiet
            pass

        def _record(self, rec):
            with LOCK:
                with open(log_path, "a", encoding="utf-8") as f:
                    f.write(json.dumps(rec, ensure_ascii=False) + "\n")

        def _forward(self):
            t0 = int(time.time() * 1000)
            n = int(self.headers.get("Content-Length") or 0)
            body = self.rfile.read(n) if n else b""
            hdrs = {k: v for k, v in self.headers.items()
                    if k.lower() not in ("host", "connection", "content-length", "accept-encoding")}
            rec = {"wall_ms": t0, "method": self.command, "path": self.path,
                   "headers": {k: ("<redacted>" if k.lower() in ("authorization", "cookie") else v)
                               for k, v in hdrs.items()}}
            try:
                rec["body"] = json.loads(body.decode("utf-8")) if body else None
            except ValueError:
                rec["body_text"] = body.decode("utf-8", "replace")[:200000]
            if capture_only:
                payload = json.dumps({"error": {"message": "OBS-2 capture-only tap: request recorded, not forwarded",
                                                "type": "invalid_request_error"}}).encode("utf-8")
                self.send_response(400)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(payload)))
                self.end_headers()
                self.wfile.write(payload)
                rec.update({"status": 400, "capture_only": True, "done_wall_ms": int(time.time() * 1000)})
                self._record(rec)
                return
            mapping = {}
            rewrites = []
            if flatten and isinstance(rec.get("body"), dict):
                newbody, mapping = flatten_request(json.loads(body.decode("utf-8")), rewrites)
                body = json.dumps(newbody).encode("utf-8")
                hdrs["Content-Type"] = "application/json"
            up = http.client.HTTPConnection("127.0.0.1", upstream_port, timeout=900)
            sent = 0
            pending = b""
            status = None
            client_gone = False
            try:
                up.request(self.command, self.path, body=body or None, headers=hdrs)
                resp = up.getresponse()
                status = resp.status
                self.send_response(resp.status, resp.reason)
                for k, v in resp.getheaders():
                    if k.lower() in ("transfer-encoding", "content-length", "connection"):
                        continue
                    self.send_header(k, v)
                self.send_header("Connection", "close")
                self.end_headers()
                eof = False
                while not eof:
                    chunk = resp.read1(65536) if hasattr(resp, "read1") else resp.read(4096)
                    if not chunk:
                        eof = True
                    if mapping:
                        # Rewrite complete SSE lines only; keep a partial line until more arrives (or EOF).
                        data = pending + chunk
                        if eof:
                            lines, pending = data, b""
                        else:
                            cut = data.rfind(b"\n") + 1
                            lines, pending = data[:cut], data[cut:]
                        out_lines = []
                        for line in lines.split(b"\n"):
                            if line.startswith(b"data: ") and b"function_call" in line:
                                try:
                                    ev = json.loads(line[6:].decode("utf-8"))
                                    n0 = len(rewrites)
                                    restore_namespace(ev, mapping, rewrites)
                                    if len(rewrites) > n0:
                                        line = b"data: " + json.dumps(ev).encode("utf-8")
                                except ValueError:
                                    pass
                            out_lines.append(line)
                        chunk = b"\n".join(out_lines)
                    if not chunk:
                        continue
                    try:
                        self.wfile.write(chunk)
                        self.wfile.flush()
                        sent += len(chunk)
                    except (BrokenPipeError, ConnectionResetError):
                        client_gone = True
                        break
            except Exception as exc:  # noqa: BLE001 - recorded
                rec["error"] = repr(exc)
            finally:
                up.close()
            rec.update({"status": status, "response_bytes": sent, "client_disconnected": client_gone,
                        "done_wall_ms": int(time.time() * 1000)})
            if flatten:
                rec["adapter_rewrites"] = rewrites
            self._record(rec)

        do_GET = _forward
        do_POST = _forward

    return Tap


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, default=12340)
    ap.add_argument("--upstream-port", type=int, default=1234)
    ap.add_argument("--log", required=True)
    ap.add_argument("--capture-only", action="store_true")
    ap.add_argument("--flatten-namespaces", action="store_true")
    a = ap.parse_args()
    srv = ThreadingHTTPServer(("127.0.0.1", a.port), make_handler(a.log, a.upstream_port, a.capture_only, a.flatten_namespaces))
    srv.daemon_threads = True
    sys.stderr.write("tap listening on 127.0.0.1:%d -> 127.0.0.1:%d\n" % (a.port, a.upstream_port))
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
