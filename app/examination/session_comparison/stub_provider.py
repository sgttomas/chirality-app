#!/usr/bin/env python3
"""A scripted loopback Responses provider for a conversation run through the App
with no model and no sign-in (the scripted driver's conversation scenario).

It is not a model and not product code. It uses the Python standard library
only, listens on 127.0.0.1 only, and forwards nothing. It is development
evidence; it establishes nothing about any model.

- `POST .../responses`: a server-sent-event stream. Every turn completes with
  REPLY, unless the last user message of the request's input contains HOLD.
  Then the stub sends `response.created` and holds the stream open until the
  client closes it (an interrupt), the bound passes, or the stub is stopped.
  It never sends a tool call, so nothing is asked and no approval arises.
- `GET .../responses` with an Upgrade header (Codex's WebSocket attempt):
  answered with the status given by --websocket-status, 404 by default.
- Anything else: 404, logged as unexpected.

Readiness: once listening it writes --ready atomically, holding pid, port and
base_url (`http://127.0.0.1:<port>/v1`). The App is given base_url exactly as
CHIRALITY_DEV_OPENAI_BASE_URL.

Log: one JSON line per request, appended to `<record>/stub-requests.jsonl` as
each request ends: seconds since start, method, path, disposition and header
names. Never a body, a prompt or a header value.

SIGTERM or SIGINT: stop listening, end any held stream, write the log's last
lines and exit 0.
"""
import argparse
import json
import os
import select
import signal
import socket
import socketserver
import sys
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

REPLY = 'Invented reply from the stub provider.'
HOLD = 'STUB-HOLD'
LOG_NAME = 'stub-requests.jsonl'
DISPOSITIONS = ('completed', 'held-ended-by-client', 'held-bound-reached', 'held-ended-by-stop',
                'websocket-refused', 'unexpected', 'unreadable-request')


def sse(event, data):
    return ('event: %s\ndata: %s\n\n' % (event, json.dumps(data, separators=(',', ':')))).encode('utf-8')


def created(response_id):
    return sse('response.created', {'type': 'response.created', 'response': {'id': response_id}})


def completion(response_id, message_id):
    """The rest of a completed turn, in the shape the 0.167.0 capture accepted."""
    item = {'type': 'message', 'role': 'assistant', 'id': message_id,
            'content': [{'type': 'output_text', 'text': REPLY, 'annotations': []}]}
    return [
        sse('response.output_item.added', {'type': 'response.output_item.added', 'output_index': 0, 'item': item}),
        sse('response.output_text.delta', {'type': 'response.output_text.delta', 'output_index': 0,
                                           'content_index': 0, 'delta': REPLY, 'item_id': message_id}),
        sse('response.output_item.done', {'type': 'response.output_item.done', 'output_index': 0, 'item': item}),
        sse('response.completed', {'type': 'response.completed', 'response': {
            'id': response_id, 'usage': {'input_tokens': 1, 'input_tokens_details': {'cached_tokens': 0},
                                         'output_tokens': 1, 'output_tokens_details': {'reasoning_tokens': 0},
                                         'total_tokens': 2}}}),
    ]


def last_user_text(body):
    """The text of the last user-role message in the request's input, or None."""
    entries = body.get('input') if isinstance(body, dict) else None
    if not isinstance(entries, list):
        return None
    for entry in reversed(entries):
        if isinstance(entry, dict) and entry.get('role') == 'user':
            content = entry.get('content')
            if isinstance(content, str):
                return content
            if isinstance(content, list):
                return ''.join(part.get('text', '') for part in content
                               if isinstance(part, dict) and isinstance(part.get('text'), str))
            return None
    return None


class Stub:
    def __init__(self, record, hold_bound, websocket_status):
        self.log_path = Path(record) / LOG_NAME
        self.hold_bound, self.websocket_status = hold_bound, websocket_status
        self.started = time.monotonic()
        self.stopping = threading.Event()
        self.lock = threading.Lock()
        self.idle = threading.Condition(self.lock)
        self.count = self.active = 0
        stub = self

        class Handler(BaseHTTPRequestHandler):
            protocol_version = 'HTTP/1.1'

            def log_message(self, *unused):
                pass

            def note(self, disposition):
                stub.note(self.command, self.path, disposition, self.headers.keys())

            def refuse(self, status, disposition):
                body = json.dumps({'error': {'message': 'stub provider: not served', 'type': 'not_found'}}).encode()
                self.send_response(status)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Content-Length', str(len(body)))
                self.send_header('Connection', 'close')
                self.end_headers()
                self.wfile.write(body)
                self.close_connection = True
                self.note(disposition)

            def do_GET(self):
                with stub.answering():
                    if self.path.split('?')[0].endswith('/responses') and self.headers.get('Upgrade'):
                        self.refuse(stub.websocket_status, 'websocket-refused')
                    else:
                        self.refuse(404, 'unexpected')

            def do_POST(self):
                with stub.answering():
                    if not self.path.split('?')[0].endswith('/responses'):
                        self.refuse(404, 'unexpected')
                        return
                    try:
                        body = json.loads(self.rfile.read(int(self.headers.get('Content-Length') or 0)))
                    except (ValueError, OSError):
                        self.refuse(400, 'unreadable-request')
                        return
                    text = last_user_text(body)
                    with stub.lock:
                        stub.count += 1
                        index = stub.count
                    response_id, message_id = 'resp_stub_%d' % index, 'msg_stub_%d' % index
                    self.send_response(200)
                    self.send_header('Content-Type', 'text/event-stream')
                    self.send_header('Cache-Control', 'no-cache')
                    self.send_header('Connection', 'close')
                    self.end_headers()
                    self.close_connection = True
                    try:
                        self.wfile.write(created(response_id))
                        self.wfile.flush()
                        if text is not None and HOLD in text:
                            self.note(self.hold())
                            return
                        for chunk in completion(response_id, message_id):
                            self.wfile.write(chunk)
                        self.wfile.flush()
                        self.note('completed')
                    except (BrokenPipeError, ConnectionResetError):
                        self.note('held-ended-by-client' if text is not None and HOLD in text else 'unexpected')

            def hold(self):
                """Hold until the client closes, the bound passes, or the stub stops."""
                deadline = time.monotonic() + stub.hold_bound
                conn = self.connection
                while True:
                    if stub.stopping.is_set():
                        return 'held-ended-by-stop'
                    left = deadline - time.monotonic()
                    if left <= 0:
                        return 'held-bound-reached'
                    readable, _, _ = select.select([conn], [], [], min(left, 0.2))
                    if readable:
                        try:
                            data = conn.recv(1, socket.MSG_PEEK)
                        except OSError:
                            return 'held-ended-by-client'
                        if not data:
                            return 'held-ended-by-client'
                        conn.recv(65536)  # anything the client sends while held is read and dropped

        class Server(ThreadingHTTPServer):
            daemon_threads = True

            def server_bind(self):  # skip HTTPServer's reverse name lookup
                socketserver.TCPServer.server_bind(self)
                self.server_name, self.server_port = '127.0.0.1', self.server_address[1]

        self.server = Server(('127.0.0.1', 0), Handler)
        self.port = self.server.server_address[1]

    def note(self, method, path, disposition, header_names):
        assert disposition in DISPOSITIONS
        line = {'t': round(time.monotonic() - self.started, 3), 'method': method,
                'path': path.split('?')[0], 'disposition': disposition,
                'header_names': sorted({k.lower() for k in header_names})}
        with self.lock:
            with open(self.log_path, 'a') as f:
                f.write(json.dumps(line, sort_keys=True) + '\n')

    def answering(self):
        stub = self

        class Answering:
            def __enter__(self):
                with stub.lock:
                    stub.active += 1

            def __exit__(self, *unused):
                with stub.idle:
                    stub.active -= 1
                    stub.idle.notify_all()

        return Answering()

    def serve(self):
        threading.Thread(target=self.server.serve_forever, daemon=True).start()

    def stop(self, timeout=5.0):
        """Stop listening, end held streams, and wait for answers in progress."""
        self.stopping.set()
        self.server.shutdown()
        self.server.server_close()
        with self.idle:
            return self.idle.wait_for(lambda: self.active == 0, timeout)


def write_ready(path, stub):
    path = Path(path)
    tmp = path.with_name(path.name + '.tmp')
    tmp.write_text(json.dumps({'pid': os.getpid(), 'port': stub.port,
                               'base_url': 'http://127.0.0.1:%d/v1' % stub.port}))
    os.replace(tmp, path)


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.split('\n\n')[0])
    p.add_argument('--record', required=True, help='the examination root\'s record/ folder, for the request log')
    p.add_argument('--ready', required=True, help='the ready file, written atomically once listening')
    p.add_argument('--hold-bound', type=float, default=60.0, help='seconds a held turn is held at most (default 60)')
    p.add_argument('--websocket-status', type=int, default=404,
                   help='the HTTP status answering a WebSocket upgrade on /responses (default 404)')
    args = p.parse_args(argv)
    if not Path(args.record).is_dir():
        print('refused: --record is not a folder', file=sys.stderr)
        return 2
    stub = Stub(args.record, args.hold_bound, args.websocket_status)
    stop = threading.Event()
    for sig in (signal.SIGTERM, signal.SIGINT):
        signal.signal(sig, lambda *unused: stop.set())
    stub.serve()
    write_ready(args.ready, stub)
    while not stop.wait(0.5):
        pass
    finished = stub.stop()
    if not finished:
        print('note: an answer did not finish before exit; the log may lack its line', file=sys.stderr)
    return 0


if __name__ == '__main__':
    sys.exit(main())
