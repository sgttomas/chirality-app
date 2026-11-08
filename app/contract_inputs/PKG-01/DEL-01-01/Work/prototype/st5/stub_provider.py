#!/usr/bin/env python3
"""Scripted loopback Responses provider for the ST-5 / NV-04 captures.

Prototype only (DEL-01-01 HOSTING §9.1 capture method; DEL-09-02 U-SQ-6). Not product code, not a
model, not an App candidate. Python 3 standard library only. It listens on 127.0.0.1 only and never
forwards anything. Each POST to `/v1/responses` is answered with a short server-sent-event stream chosen
by `plan(request_body)` in the harness (invented content only). Every request is recorded (path, header
names, body) so the capture can show what Codex sent to the provider; header values are not kept.
"""
import json
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer


def sse(event, data):
    return ("event: %s\ndata: %s\n\n" % (event, json.dumps(data, separators=(",", ":")))).encode("utf-8")


def stream_for(items, resp_id):
    """Encode a list of output items as a Responses stream that Codex accepts."""
    out = [sse("response.created", {"type": "response.created", "response": {"id": resp_id}})]
    for i, item in enumerate(items):
        out.append(sse("response.output_item.added",
                       {"type": "response.output_item.added", "output_index": i, "item": item}))
        if item.get("type") == "message":
            text = item["content"][0]["text"]
            out.append(sse("response.output_text.delta",
                           {"type": "response.output_text.delta", "output_index": i, "content_index": 0,
                            "delta": text, "item_id": item.get("id")}))
        out.append(sse("response.output_item.done",
                       {"type": "response.output_item.done", "output_index": i, "item": item}))
    out.append(sse("response.completed", {"type": "response.completed", "response": {
        "id": resp_id, "usage": {"input_tokens": 1, "input_tokens_details": {"cached_tokens": 0},
                                 "output_tokens": 1, "output_tokens_details": {"reasoning_tokens": 0},
                                 "total_tokens": 2}}}))
    return out


def message(text, mid):
    return {"type": "message", "role": "assistant", "id": mid,
            "content": [{"type": "output_text", "text": text, "annotations": []}]}


class Provider:
    def __init__(self, plan, log):
        self.plan = plan          # plan(index, body) -> (items, delay_s) or None for HTTP 400
        self.log = log            # list, appended under lock
        self.lock = threading.Lock()
        self.count = 0
        prov = self

        class H(BaseHTTPRequestHandler):
            protocol_version = "HTTP/1.1"

            def log_message(self, *a):
                pass

            def do_GET(self):
                body = b'{"object":"list","data":[{"id":"st5-stub-model","object":"model"}]}'
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)

            def do_POST(self):
                n = int(self.headers.get("Content-Length") or 0)
                raw = self.rfile.read(n)
                try:
                    body = json.loads(raw)
                except ValueError:
                    body = None
                with prov.lock:
                    prov.count += 1
                    idx = prov.count
                decision = prov.plan(idx, body) if self.path.endswith("/responses") else None
                with prov.lock:
                    prov.log.append({"index": idx, "t": time.monotonic(), "path": self.path,
                                     "header_names": sorted(k.lower() for k in self.headers.keys()),
                                     "body": body, "answered": None if decision is None else decision[2]})
                if decision is None:
                    err = b'{"error":{"message":"st5 stub: no scripted answer","type":"invalid_request_error"}}'
                    self.send_response(400)
                    self.send_header("Content-Type", "application/json")
                    self.send_header("Content-Length", str(len(err)))
                    self.end_headers()
                    self.wfile.write(err)
                    return
                items, delay, _label = decision
                self.send_response(200)
                self.send_header("Content-Type", "text/event-stream")
                self.send_header("Cache-Control", "no-cache")
                self.send_header("Connection", "close")
                self.end_headers()
                chunks = stream_for(items, "resp_st5_%d" % idx)
                try:
                    self.wfile.write(chunks[0])
                    self.wfile.flush()
                    if delay:
                        time.sleep(delay)
                    for c in chunks[1:]:
                        self.wfile.write(c)
                        self.wfile.flush()
                except (BrokenPipeError, ConnectionResetError):
                    pass
                self.close_connection = True

        class S(ThreadingHTTPServer):
            def server_bind(self):  # skip HTTPServer's reverse name lookup
                import socketserver
                socketserver.TCPServer.server_bind(self)
                self.server_name, self.server_port = "127.0.0.1", self.server_address[1]

        self.server = S(("127.0.0.1", 0), H)
        self.server.daemon_threads = True
        self.port = self.server.server_address[1]
        threading.Thread(target=self.server.serve_forever, daemon=True).start()

    def close(self):
        self.server.shutdown()
        self.server.server_close()
