#!/usr/bin/env python3
"""Scripted loopback Responses provider for supplier captures (capture.py).

Not a model and not product code. Python 3 standard library only. It listens on
127.0.0.1 only and forwards nothing. Each POST to `/v1/responses` is answered
with a short server-sent-event stream chosen by the capture's `plan(index, body)`
(invented content only). Every request is logged (path, header names, body) so a
capture can state what Codex sent to the provider; header values are not kept.
"""
import json
import socketserver
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

MODEL = "st5-stub-model"  # the name the 0.160.0 captures used, kept so pins compare


def sse(event, data):
    return ("event: %s\ndata: %s\n\n" % (event, json.dumps(data, separators=(",", ":")))).encode("utf-8")


def stream_for(items, response_id):
    """Encode output items as a Responses stream that Codex accepts."""
    out = [sse("response.created", {"type": "response.created", "response": {"id": response_id}})]
    for index, item in enumerate(items):
        out.append(sse("response.output_item.added",
                       {"type": "response.output_item.added", "output_index": index, "item": item}))
        if item.get("type") == "message":
            out.append(sse("response.output_text.delta",
                           {"type": "response.output_text.delta", "output_index": index, "content_index": 0,
                            "delta": item["content"][0]["text"], "item_id": item.get("id")}))
        out.append(sse("response.output_item.done",
                       {"type": "response.output_item.done", "output_index": index, "item": item}))
    out.append(sse("response.completed", {"type": "response.completed", "response": {
        "id": response_id, "usage": {"input_tokens": 1, "input_tokens_details": {"cached_tokens": 0},
                                     "output_tokens": 1, "output_tokens_details": {"reasoning_tokens": 0},
                                     "total_tokens": 2}}}))
    return out


def message(text, message_id):
    return {"type": "message", "role": "assistant", "id": message_id,
            "content": [{"type": "output_text", "text": text, "annotations": []}]}


class Provider:
    """plan(index, body) returns (items, delay_seconds, label), or None for HTTP 400."""

    def __init__(self, plan, log):
        self.plan, self.log = plan, log
        self.lock = threading.Lock()
        self.count = 0
        provider = self

        class Handler(BaseHTTPRequestHandler):
            protocol_version = "HTTP/1.1"

            def log_message(self, *unused):
                pass

            def reply(self, status, content_type, body):
                self.send_response(status)
                self.send_header("Content-Type", content_type)
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)

            def do_GET(self):
                with provider.lock:
                    provider.log.append({"index": None, "path": self.path, "body": None, "answered": "model list",
                                         "header_names": sorted(k.lower() for k in self.headers.keys())})
                self.reply(200, "application/json", json.dumps(
                    {"object": "list", "data": [{"id": MODEL, "object": "model"}]}).encode("utf-8"))

            def do_POST(self):
                raw = self.rfile.read(int(self.headers.get("Content-Length") or 0))
                try:
                    body = json.loads(raw)
                except ValueError:
                    body = None
                with provider.lock:
                    provider.count += 1
                    index = provider.count
                decision = provider.plan(index, body) if self.path.endswith("/responses") else None
                with provider.lock:
                    provider.log.append({"index": index, "path": self.path, "body": body,
                                         "header_names": sorted(k.lower() for k in self.headers.keys()),
                                         "answered": None if decision is None else decision[2]})
                if decision is None:
                    self.reply(400, "application/json", json.dumps({"error": {
                        "message": "capture stub: no scripted answer", "type": "invalid_request_error"}}).encode())
                    return
                items, delay, _label = decision
                self.send_response(200)
                self.send_header("Content-Type", "text/event-stream")
                self.send_header("Cache-Control", "no-cache")
                self.send_header("Connection", "close")
                self.end_headers()
                chunks = stream_for(items, "resp_capture_%d" % index)
                try:
                    self.wfile.write(chunks[0])
                    self.wfile.flush()
                    if delay:
                        time.sleep(delay)
                    for chunk in chunks[1:]:
                        self.wfile.write(chunk)
                        self.wfile.flush()
                except (BrokenPipeError, ConnectionResetError):
                    pass
                self.close_connection = True

        class Server(ThreadingHTTPServer):
            def server_bind(self):  # skip HTTPServer's reverse name lookup
                socketserver.TCPServer.server_bind(self)
                self.server_name, self.server_port = "127.0.0.1", self.server_address[1]

        self.server = Server(("127.0.0.1", 0), Handler)
        self.server.daemon_threads = True
        self.port = self.server.server_address[1]
        threading.Thread(target=self.server.serve_forever, daemon=True).start()

    def close(self):
        self.server.shutdown()
        self.server.server_close()
