#!/usr/bin/env python3
"""Supplier double for HOSTING-BOUNDARY-v0.8 (DEL-01-01), seeded from the W11
spike transcripts. Prototype only (Wave B node B6); NOT product code and NOT
the supplier. Python 3 standard library only.

It speaks newline-delimited JSON over its standard input and output, like the
stock Codex App Server 0.158.0 did in the spike (HOSTING §5), and replays the
supplier->App frames recorded in the redacted transcripts committed at
`../generated/0.158.0/_spike/transcripts/` (fixture standing `recorded`,
HOSTING §9.2):

  * the initialize response and the `remoteControl/status/changed`
    notification that followed it before the client's `initialized`;
  * the -32600 "unknown variant" error for an unknown client method (its
    message lists the 170 client methods the server accepted);
  * the -32600 "Already initialized" error for a second initialize;
  * no reply to an unknown client notification;
  * exit code 0 on end of input and on SIGTERM.

A recorded frame is written byte for byte when its request identity (and, for
the unknown-method error, the method name) matches the recording; otherwise
the identity or name is substituted and the frame is labelled `mutated`.
Everything a scenario adds (server requests, items, malformed lines, exits)
is labelled `constructed` and comes from double_scenarios.py.

Usage:
  supplier_double.py --seed-dir DIR [--seed A-bin-freshhome] \
                     [--scenario default] [--log PATH]
"""
import argparse
import json
import os
import re
import signal
import sys
import threading
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import double_scenarios  # noqa: E402

T0 = time.monotonic()
OUT_LOCK = threading.Lock()
LOG = None


def now_ms():
    return int((time.monotonic() - T0) * 1000)


def log(event):
    if LOG is None:
        return
    event["t_ms"] = now_ms()
    with OUT_LOCK:
        LOG.write(json.dumps(event, ensure_ascii=False) + "\n")
        LOG.flush()


def compact(obj):
    return json.dumps(obj, separators=(",", ":"), ensure_ascii=False)


def load_seed(seed_dir, name, fallback="A-bin-freshhome"):
    """Frames from transcript `name`; a frame kind that `name` did not record
    (runs B, C and D sent fewer requests) is taken from `fallback`."""
    seed = _frames(seed_dir, name)
    if name != fallback:
        for key, value in _frames(seed_dir, fallback).items():
            seed.setdefault(key, value)
    seed["transcript"] = name
    msg = json.loads(seed["unknown_method"][0])["error"]["message"]
    names = re.findall(r"`([^`]+)`", msg)
    seed["recorded_unknown_name"] = names[0]
    seed["accepted_methods"] = names[1:]
    return seed


def _frames(seed_dir, name):
    path = os.path.join(seed_dir, name + ".jsonl")
    seed = {}
    for line in open(path, encoding="utf-8"):
        ev = json.loads(line)
        if ev.get("kind") != "recv":
            continue
        raw = ev["raw"]
        frame = json.loads(raw)
        if "result" in frame and "userAgent" in frame["result"]:
            seed["init_result"] = (raw, frame["id"])
        elif frame.get("method") == "remoteControl/status/changed":
            seed["early_notification"] = raw
        elif "error" in frame and "unknown variant" in frame["error"]["message"]:
            seed["unknown_method"] = (raw, frame["id"])
        elif "error" in frame and frame["error"]["message"] == "Already initialized":
            seed["already_initialized"] = (raw, frame["id"])
    return seed


class Double:
    def __init__(self, seed, scenario):
        self.seed = seed
        self.scenario = scenario
        self.initialize_answered = False
        self.stdin_closed = False
        self.ctx = {"requests": {}, "counter": 0}

    # ---- output -------------------------------------------------------
    def write_line(self, line, standing, note=None, responds_to=None):
        with OUT_LOCK:
            try:
                sys.stdout.write(line + "\n")
                sys.stdout.flush()
            except BrokenPipeError:
                return
        ev = {"dir": "emit", "standing": standing, "raw": line}
        if note:
            ev["note"] = note
        if responds_to:
            ev["responds_to"] = responds_to
        log(ev)

    def emit_recorded(self, key, req_id=None, name=None, responds_to=None):
        raw, rec_id = self.seed[key] if isinstance(self.seed[key], tuple) else (self.seed[key], None)
        frame = json.loads(raw)
        standing = "recorded"
        if req_id is not None and req_id != rec_id:
            frame["id"] = req_id
            standing = "mutated"
        if name is not None and name != self.seed["recorded_unknown_name"]:
            frame["error"]["message"] = frame["error"]["message"].replace(
                "`%s`" % self.seed["recorded_unknown_name"], "`%s`" % name, 1)
            standing = "mutated"
        line = raw if standing == "recorded" else compact(frame)
        self.write_line(line, standing, note="seed:" + key, responds_to=responds_to)

    def run_actions(self, actions):
        for act in actions or []:
            if "delay" in act:
                a = dict(act)
                d = a.pop("delay")
                threading.Timer(d, self.run_actions, args=([a],)).start()
                continue
            if "emit" in act:
                self.write_line(compact(act["emit"]), act.get("standing", "constructed"),
                                note=act.get("note"), responds_to=act.get("responds_to"))
            elif "emit_raw" in act:
                self.write_line(act["emit_raw"], act.get("standing", "constructed"),
                                note=act.get("note"))
            elif act.get("close_stdin"):
                log({"dir": "action", "action": "close-stdin"})
                self.stdin_closed = True
                try:
                    os.close(0)
                except OSError:
                    pass
            elif "exit" in act:
                log({"dir": "action", "action": "exit", "code": act["exit"]})
                LOG and LOG.flush()
                os._exit(act["exit"])
            elif act.get("ignore"):
                log({"dir": "action", "action": "no-response", "note": act.get("note")})

    # ---- input --------------------------------------------------------
    def handle(self, raw):
        log({"dir": "recv-from-app", "raw": raw})
        try:
            frame = json.loads(raw)
        except ValueError:
            return
        if not isinstance(frame, dict):
            return
        method, has_id = frame.get("method"), "id" in frame
        if method and has_id:
            self.on_request(frame)
        elif method:
            if method == "initialized":
                self.run_actions(self.scenario.after_initialized(self.ctx))
            # unknown client notifications get no reply (recorded, run A)
        elif has_id:
            self.run_actions(self.scenario.on_client_response(self.ctx, frame))

    def on_request(self, frame):
        method, rid = frame["method"], frame["id"]
        self.ctx["requests"][json.dumps(rid)] = method
        if method == "initialize":
            if self.initialize_answered:
                self.emit_recorded("already_initialized", req_id=rid, responds_to=method)
                return
            override = self.scenario.on_initialize(self.ctx, frame)
            if override is not None:
                self.run_actions(override)
                return
            self.emit_recorded("init_result", req_id=rid, responds_to=method)
            self.emit_recorded("early_notification")
            self.initialize_answered = True
            self.run_actions(self.scenario.after_initialize_response(self.ctx))
            return
        if method not in self.seed["accepted_methods"]:
            self.emit_recorded("unknown_method", req_id=rid, name=method, responds_to=method)
            return
        actions = self.scenario.on_request(self.ctx, frame)
        if actions is None:
            actions = [{"emit": {"id": rid, "error": {
                "code": -32603,
                "message": "supplier double: no scripted response for " + method}},
                "standing": "constructed", "responds_to": method}]
        self.run_actions(actions)


def main():
    global LOG
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed-dir", required=True)
    ap.add_argument("--seed", default="A-bin-freshhome")
    ap.add_argument("--scenario", default="default")
    ap.add_argument("--log")
    args = ap.parse_args()
    if args.log:
        LOG = open(args.log, "a", encoding="utf-8")

    def on_term(signum, _frame):
        log({"dir": "signal", "signal": "SIGTERM", "exit": 0})
        LOG and LOG.flush()
        os._exit(0)  # recorded: SIGTERM -> exit code 0, no signal (runs D)

    signal.signal(signal.SIGTERM, on_term)
    seed = load_seed(args.seed_dir, args.seed)
    dbl = Double(seed, double_scenarios.get(args.scenario))
    log({"dir": "start", "seed": args.seed, "scenario": args.scenario,
         "accepted_methods": len(seed["accepted_methods"])})
    stdin = sys.stdin.buffer
    while not dbl.stdin_closed:
        try:
            line = stdin.readline()
        except (OSError, ValueError):
            break
        if not line:
            log({"dir": "eof", "exit": 0})
            LOG and LOG.flush()
            os._exit(0)  # recorded: end of input -> exit code 0 (runs A, B, C)
        dbl.handle(line.decode("utf-8", "replace").rstrip("\n"))
    while True:  # stdin closed by a scenario: wait for a scripted exit or SIGTERM
        time.sleep(0.05)


if __name__ == "__main__":
    main()
