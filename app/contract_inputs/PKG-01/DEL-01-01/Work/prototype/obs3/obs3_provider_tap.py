#!/usr/bin/env python3
"""OBS-3 provider tap: the OBS-2 pass-through recorder with a per-request capture switch.

Prototype only (DEL-01-01, run APP-V4-DESIGN-PASS-3-20261001, node OBS-3). Not product code.
Python 3 standard library only. Loopback only.

It reuses obs2_provider_tap.py unchanged. Each request is handled in one of two ways, chosen
per request by the presence of a flag file:

- flag file absent: pass-through (OBS-2 default mode). The request is forwarded unchanged to
  LM Studio on 127.0.0.1:1234 and the response streamed back unchanged; the request body is
  recorded.
- flag file present: capture-only (OBS-2 --capture-only). The request is recorded and answered
  HTTP 400 with an invented error body; no model call is made.

The switch lets the harness see exactly what Codex would send to the model for a variant
without spending a model prediction, while the same Codex process and thread continue to be
used for real turns. Nothing is rewritten in either mode (the OBS-2 namespace adapter is not
used by OBS-3).

Usage: obs3_provider_tap.py --port 12350 --log FILE --flag FILE [--upstream-port 1234]
"""
import argparse
import os
import sys
from http.server import ThreadingHTTPServer

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "obs2"))
import obs2_provider_tap as T  # noqa: E402  (OBS-2 tap, unchanged)


def make_switch_handler(log_path, upstream_port, flag_path):
    Pass = T.make_handler(log_path, upstream_port, capture_only=False, flatten=False)
    Cap = T.make_handler(log_path, upstream_port, capture_only=True, flatten=False)

    class Switch(Pass):
        def _dispatch(self):
            if os.path.exists(flag_path):
                return Cap._forward(self)
            return Pass._forward(self)

        do_GET = _dispatch
        do_POST = _dispatch

    return Switch


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, default=12350)
    ap.add_argument("--upstream-port", type=int, default=1234)
    ap.add_argument("--log", required=True)
    ap.add_argument("--flag", required=True, help="capture-only while this file exists")
    a = ap.parse_args()
    srv = ThreadingHTTPServer(("127.0.0.1", a.port), make_switch_handler(a.log, a.upstream_port, a.flag))
    srv.daemon_threads = True
    sys.stderr.write("obs3 tap listening on 127.0.0.1:%d -> 127.0.0.1:%d (capture while %s exists)\n"
                     % (a.port, a.upstream_port, a.flag))
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
