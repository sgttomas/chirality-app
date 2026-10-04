#!/usr/bin/env python3
"""H-1 probe P-H1c (R23-48 item 3): App-origin `mcpServer/tool/call` (a)
during an active turn and (b) between turns on a thread that already has
history. Does any later model request carry a trace of either call?

Bounded observation (owner O-D). Not product code; not qualification.
Limits (R23-34.3, R23-37 item 1, R23-48 item 3):
- the scratch Codex 0.158.0 binary, never the `codex` on PATH or ~/.codex;
- CODEX_HOME and HOME under /tmp with no user name, removed afterwards;
- DEL-01-01's MCP double; no network beyond loopback, no sign-in, no
  download;
- a model already present in LM Studio, served on loopback (the operator
  starts the server and loads the model before, and unloads and stops it
  after; this script checks the server listens on loopback only);
- the socket guard of P-H1, plus a memory-pressure stop (level 4), as
  OBS-2's S-9;
- user-name, host-name and HOSTING §9.1 redaction (`redact.py`).
DEL-01-01's OBS-2 provider tap runs in pass-through mode on loopback and
records every request Codex sends to the model.

Sequence:
  T1  turn/start "alpha" prompt; while T1 is active, App-origin call A
      (key EX-1; markers P-EX-1, toolReceivedAtMs, "invented example material");
      wait for T1 to complete (the thread now has history)
  T2  turn/start "beta" prompt; capture its requests
  B   App-origin call B between turns (key EX-ERR; marker "Invented example error")
  T3  turn/start "gamma" prompt; capture its requests
Every request is searched for every marker. The prompts are invented and
contain none of them.

Revision for RV2 EUD1-R15 (R23-52 item 1): `--call-b-key EX-1` makes call B
succeed (P-H1d). Each successful call's result carries its own
`toolReceivedAtMs` value, recorded as that call's own marker, so a trace in
a later request can be attributed to call A or call B; the shared result
texts are searched as well. The default (`EX-ERR`) reproduces P-H1c.

Usage: probe_history_active.py --binary PATH --double PATH --tap PATH --model KEY --out DIR
                               [--root /tmp/cvx-eud1c] [--ctx 24576] [--call-b-key EX-ERR|EX-1] [--cleanup]
"""
import argparse
import json
import os
import shutil
import socket
import subprocess
import sys
import threading
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import probe_mcp_call as P1  # noqa: E402
import redact  # noqa: E402

TAP_PORT = 12342
MARKERS_A = ["P-EX-1", "toolReceivedAtMs", "invented example material"]
MARKERS_B = ["Invented example error", "EX-ERR not found"]
PROMPTS = {"T1": "This is an observation test with invented data. Reply with the single word: alpha.",
           "T2": "Reply with the single word: beta.",
           "T3": "Reply with the single word: gamma."}


def loopback_only(port):
    out = subprocess.run(["lsof", "-nP", f"-iTCP:{port}", "-sTCP:LISTEN"], capture_output=True, text=True).stdout
    lines = out.splitlines()[1:]
    return bool(lines) and all(("127.0.0.1:" in l or "[::1]:" in l or "localhost:" in l) for l in lines), lines


class Probe3(P1.Probe):
    def __init__(self, a):
        super().__init__(a)
        self.turn_done = {}

    def setup(self):
        super().setup()
        cfg_p = os.path.join(self.home, "config.toml")
        cfg = open(cfg_p).read()
        cfg = cfg.replace('model = "probe-none"', f'model = "{self.a.model}"\nmodel_context_window = {self.a.ctx}')
        cfg = cfg.replace('base_url = "http://127.0.0.1:9/v1"', f'base_url = "http://127.0.0.1:{TAP_PORT}/v1"')
        cfg = cfg.replace('name = "EU-D1 probe: no model"', 'name = "EU-D1 probe: LM Studio on loopback via tap"')
        with open(cfg_p, "w") as f:
            f.write(cfg)
        self.ev("config-provider", base_url=f"http://127.0.0.1:{TAP_PORT}/v1 (pass-through tap to LM Studio 127.0.0.1:1234)", model=self.a.model)

    def pressure(self):
        while not self.stop.is_set():
            lvl = subprocess.run(["sysctl", "-n", "kern.memorystatus_vm_pressure_level"], capture_output=True, text=True).stdout.strip()
            if lvl == "4":
                self.halt("memory pressure level critical (4)")
            time.sleep(0.25)

    def wait_method(self, method, start, timeout):
        deadline = time.time() + timeout
        while time.time() < deadline and not self.stop.is_set():
            for f in self.frames[start:]:
                if f["dir"] == "in" and f.get("raw", {}).get("method") == method:
                    return f["t_ms"]
            time.sleep(0.1)
        return None

    def turn(self, tid, name, timeout=300):
        n0 = len(self.frames)
        r = self.request("turn/start", {"threadId": tid, "input": [{"type": "text", "text": PROMPTS[name], "text_elements": []}]}, timeout=60)
        self.ev(f"{name} turn/start", ok=bool(r and "result" in r))
        return n0

    def run(self):
        env = {"PATH": "/usr/bin:/bin:/usr/sbin:/sbin", "CODEX_HOME": self.home, "HOME": os.path.join(self.root, "h"),
               "TMPDIR": os.path.join(self.root, "h")}
        self.proc = subprocess.Popen([self.a.binary, "app-server"], cwd=self.cwd, env=env, stdin=subprocess.PIPE,
                                     stdout=subprocess.PIPE, stderr=subprocess.PIPE, start_new_session=True)
        self.pgid = os.getpgid(self.proc.pid)
        self.ev("spawn", argv=["<scratch codex 0.158.0>", "app-server"], env_keys=sorted(env))
        for t in (self.reader, self.stderr_reader, self.guard, self.pressure):
            threading.Thread(target=t, daemon=True).start()
        obs = {}
        try:
            r = self.request("initialize", {"clientInfo": {"name": "chirality-eud1-probe-c", "title": "EU-D1 probe c", "version": "0.0.0"},
                                            "capabilities": {"experimentalApi": False, "requestAttestation": False}})
            if os.path.realpath((r or {}).get("result", {}).get("codexHome") or "") != os.path.realpath(self.home):
                self.halt("codexHome is not the scratch home")
                return obs
            self.notify("initialized")
            time.sleep(3.0)
            r = self.request("thread/start", {"cwd": self.cwd, "approvalPolicy": "never", "sandbox": "read-only"}, timeout=60)
            tid = (((r or {}).get("result") or {}).get("thread") or {}).get("id")
            if not tid:
                obs["thread_start_error"] = (r or {}).get("error")
                return obs
            time.sleep(3.0)
            # T1 with call A during it
            n0 = self.turn(tid, "T1")
            started = self.wait_method("turn/started", n0, 60)
            t_call = P1.ms()
            ra = self.request("mcpServer/tool/call", {"server": "double", "threadId": tid, "tool": "example_lookup",
                                                     "arguments": {"key": "EX-1"}}, timeout=60)
            t_ret = P1.ms()
            done1 = self.wait_method("turn/completed", n0, 600)
            obs["call_A_own_marker"] = str((((ra or {}).get("result") or {}).get("structuredContent") or {}).get("toolReceivedAtMs", ""))
            obs["call_A"] = {"returned": bool(ra and "result" in ra), "markers_in_result": [m for m in MARKERS_A if m in json.dumps(ra)],
                             "t1_turn_started_ms": started, "call_sent_ms": t_call, "call_returned_ms": t_ret, "t1_turn_completed_ms": done1,
                             "during_active_turn": bool(started is not None and done1 is not None and started <= t_call and t_ret <= done1)}
            if self.stop.is_set() or done1 is None:
                return obs
            # T2 on a thread with history
            n2 = self.turn(tid, "T2")
            obs["t2_completed_ms"] = self.wait_method("turn/completed", n2, 600)
            if self.stop.is_set():
                return obs
            # call B between turns, then T3
            rb = self.request("mcpServer/tool/call", {"server": "double", "threadId": tid, "tool": "example_lookup",
                                                     "arguments": {"key": self.a.call_b_key}}, timeout=60)
            res_b = (rb or {}).get("result") or {}
            obs["call_B_own_marker"] = str((res_b.get("structuredContent") or {}).get("toolReceivedAtMs", ""))
            obs["call_B"] = {"key": self.a.call_b_key, "returned": bool(rb and ("result" in rb)), "is_error": res_b.get("isError"),
                             "markers_in_result": [m for m in MARKERS_A + MARKERS_B if m in json.dumps(rb)],
                             "sent_after_t2_completed": obs["t2_completed_ms"] is not None}
            time.sleep(1.0)
            n3 = self.turn(tid, "T3")
            obs["t3_completed_ms"] = self.wait_method("turn/completed", n3, 600)
            obs["notifications"] = [f["raw"].get("method") for f in self.frames if f["dir"] == "in" and "method" in f.get("raw", {})
                                    and not f["raw"]["method"].startswith(("item/agentMessage/delta", "item/reasoning"))]
        finally:
            self.ev("end", stop_reason=self.stop_reason)
            try:
                self.proc.stdin.close()
            except OSError:
                pass
            try:
                self.proc.wait(timeout=10)
            except subprocess.TimeoutExpired:
                os.killpg(self.pgid, 9)
            self.stop.set()
        return obs


def analyse(tap_log, frames, own=()):
    reqs = [json.loads(l) for l in open(tap_log)] if os.path.exists(tap_log) else []
    out = []
    for q in reqs:
        b = q.get("body") or {}
        inp = b.get("input") if isinstance(b, dict) else None
        text = json.dumps(b)
        input_text = json.dumps(inp) if inp is not None else ""
        which = [k for k, p in PROMPTS.items() if p in input_text]
        out.append({"path": q.get("path"), "status": q.get("status"),
                    "prompts_in_input": which,
                    "input_items": len(inp) if isinstance(inp, list) else None,
                    "input_item_types": [i.get("type", "message") + (":" + i.get("role") if i.get("role") else "") for i in (inp or []) if isinstance(i, dict)],
                    "markers_A_in_body": [m for m in MARKERS_A if m in text],
                    "markers_B_in_body": [m for m in MARKERS_B if m in text],
                    "own_markers_in_body": [m for m in own if m and m in text],
                    "tool_call_items_in_input": [i.get("type") for i in (inp or []) if isinstance(i, dict) and ("call" in str(i.get("type")) or "output" in str(i.get("type")))]})
    return out, reqs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--binary", required=True)
    ap.add_argument("--double", required=True)
    ap.add_argument("--tap", required=True)
    ap.add_argument("--model", required=True)
    ap.add_argument("--ctx", type=int, default=24576)
    ap.add_argument("--out", required=True)
    ap.add_argument("--root", default="/tmp/cvx-eud1c")
    ap.add_argument("--call-b-key", default="EX-ERR", choices=["EX-ERR", "EX-1"])
    ap.add_argument("--cleanup", action="store_true")
    a = ap.parse_args()
    if shutil.which("codex") and os.path.realpath(shutil.which("codex")) == os.path.realpath(a.binary):
        raise SystemExit("refusing: binary must be a scratch binary, not the codex on PATH")
    if os.environ.get("USER") and os.environ["USER"] in a.root:
        raise SystemExit("refusing: root path contains the user name")
    ok, lines = loopback_only(1234)
    if not ok:
        raise SystemExit(f"refusing: LM Studio server is not listening on loopback only: {lines}")
    p = Probe3(a)
    p.setup()
    tap_log = os.path.join(p.logs, "tap.jsonl")
    tap = subprocess.Popen([sys.executable, "-B", a.tap, "--port", str(TAP_PORT), "--log", tap_log, "--upstream-port", "1234"],
                           stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, start_new_session=True)
    time.sleep(1.0)
    try:
        obs = p.run()
    finally:
        tap.terminate()
        try:
            tap.wait(timeout=5)
        except subprocess.TimeoutExpired:
            tap.kill()
    obs["stop_reason"] = p.stop_reason
    per, reqs = analyse(tap_log, p.frames, (obs.get("call_A_own_marker"), obs.get("call_B_own_marker")))
    obs["model_requests"] = per
    obs["any_marker_in_any_request"] = any(r["markers_A_in_body"] or r["markers_B_in_body"] or r["own_markers_in_body"] for r in per)
    host = socket.gethostname()
    user = os.environ.get("USER", "\0")
    needles = [os.path.expanduser("~"), host, host.split(".")[0], user, user.capitalize()]
    os.makedirs(a.out, exist_ok=True)
    for name, obj in (("observations.json", obs), ("frames.json", p.frames), ("events.json", p.events), ("model_requests.json", reqs)):
        with open(os.path.join(a.out, name), "w") as f:
            f.write(P1.scrub(obj, needles))
    redact.redact_dir(a.out)
    if a.cleanup:
        shutil.rmtree(a.root)
        print("removed", a.root)
    print(json.dumps({"stop_reason": p.stop_reason, "requests": len(per), "any_marker": obs["any_marker_in_any_request"],
                      "call_A_during_active_turn": obs.get("call_A", {}).get("during_active_turn")}))


if __name__ == "__main__":
    main()
