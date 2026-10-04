#!/usr/bin/env python3
"""H-1 follow-up probe P-H1b (R23-37 item 1): after an App-origin
`mcpServer/tool/call`, does the next turn's model input carry any trace of
the call?

Bounded observation (owner O-D). Not product code; not qualification.
Same limits as P-H1 (`probe_mcp_call.py`): the scratch Codex 0.158.0 binary,
never the `codex` on PATH or ~/.codex; CODEX_HOME and HOME under /tmp with no
user name; DEL-01-01's MCP double; no network, no sign-in, no download; the
same socket guard and the same user-name and host-name redaction.

The model's input is observed with DEL-01-01's OBS-2 provider tap in
`--capture-only` mode: the tap, on loopback, records the exact request Codex
sends to the provider and answers HTTP 400 without forwarding it. So the
model input is observed without any model being called; LM Studio is not
started (R23-37 permits a local model; this probe needs none).

Detection: the double's result for key EX-1 carries the markers `P-EX-1` and
`toolReceivedAtMs`, which appear nowhere else (the tool's description says
only "e.g. EX-1"). The turn prompt is invented and names neither. The probe
also looks for any input item of a tool-call or tool-output type.

Usage: probe_model_input.py --binary PATH --double PATH --tap PATH --out DIR [--root /tmp/cvx-eud1b] [--cleanup]
"""
import argparse
import json
import os
import shutil
import socket
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import probe_mcp_call as P1  # noqa: E402

TAP_PORT = 12341
MARKERS = ["P-EX-1", "toolReceivedAtMs", "invented example material"]
PROMPT = "This is an observation test with invented data. Reply with the single word: ready."


class Probe2(P1.Probe):
    def setup(self):
        super().setup()
        cfg_p = os.path.join(self.home, "config.toml")
        cfg = open(cfg_p).read().replace('base_url = "http://127.0.0.1:9/v1"', f'base_url = "http://127.0.0.1:{TAP_PORT}/v1"')
        with open(cfg_p, "w") as f:
            f.write(cfg)
        self.ev("config-provider", base_url=f"http://127.0.0.1:{TAP_PORT}/v1 (capture-only tap)")

    def run(self):
        env = {"PATH": "/usr/bin:/bin:/usr/sbin:/sbin", "CODEX_HOME": self.home, "HOME": os.path.join(self.root, "h"),
               "TMPDIR": os.path.join(self.root, "h")}
        self.proc = subprocess.Popen([self.a.binary, "app-server"], cwd=self.cwd, env=env, stdin=subprocess.PIPE,
                                     stdout=subprocess.PIPE, stderr=subprocess.PIPE, start_new_session=True)
        import os as _os
        import threading
        self.pgid = _os.getpgid(self.proc.pid)
        self.ev("spawn", argv=["<scratch codex 0.158.0>", "app-server"], env_keys=sorted(env))
        for t in (self.reader, self.stderr_reader, self.guard):
            threading.Thread(target=t, daemon=True).start()
        obs = {}
        try:
            r = self.request("initialize", {"clientInfo": {"name": "chirality-eud1-probe-b", "title": "EU-D1 probe b", "version": "0.0.0"},
                                            "capabilities": {"experimentalApi": False, "requestAttestation": False}})
            obs["codexHome_is_scratch"] = os.path.realpath((r or {}).get("result", {}).get("codexHome") or "") == os.path.realpath(self.home)
            if not obs["codexHome_is_scratch"]:
                self.halt("codexHome is not the scratch home")
                return obs
            self.notify("initialized")
            time.sleep(3.0)
            r = self.request("thread/start", {"cwd": self.cwd, "approvalPolicy": "never", "sandbox": "read-only"}, timeout=60)
            tid = (((r or {}).get("result") or {}).get("thread") or {}).get("id")
            obs["thread_id"] = tid
            if not tid or self.stop.is_set():
                obs["thread_start_error"] = (r or {}).get("error")
                return obs
            time.sleep(3.0)
            r = self.request("mcpServer/tool/call", {"server": "double", "threadId": tid, "tool": "example_lookup",
                                                    "arguments": {"key": "EX-1"}}, timeout=60)
            obs["tool_call_returned"] = bool(r and "result" in r)
            obs["tool_call_markers_in_result"] = [m for m in MARKERS if m in json.dumps(r)]
            time.sleep(2.0)
            n_before = len(self.frames)
            r = self.request("turn/start", {"threadId": tid, "input": [{"type": "text", "text": PROMPT, "text_elements": []}]}, timeout=60)
            obs["turn_start"] = "ok" if r and "result" in r else (r or {}).get("error")
            deadline = time.time() + 60
            done = False
            while time.time() < deadline and not done and not self.stop.is_set():
                time.sleep(0.5)
                done = any(f["dir"] == "in" and f.get("raw", {}).get("method") == "turn/completed" for f in self.frames[n_before:])
            obs["turn_completed_seen"] = done
            obs["turn_notifications"] = [f["raw"].get("method") for f in self.frames[n_before:]
                                         if f["dir"] == "in" and "method" in f.get("raw", {})]
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


def analyse(tap_log):
    reqs = [json.loads(l) for l in open(tap_log)] if os.path.exists(tap_log) else []
    out = {"requests": len(reqs), "per_request": []}
    for q in reqs:
        b = q.get("body") or {}
        text = json.dumps(b)
        inp = b.get("input") if isinstance(b, dict) else None
        types = sorted({i.get("type", "message") for i in inp}) if isinstance(inp, list) else None
        input_text = json.dumps(inp) if inp is not None else ""
        tools = [t.get("name") or t.get("type") for t in b.get("tools", [])] if isinstance(b, dict) else []
        out["per_request"].append({
            "method": q.get("method"), "path": q.get("path"),
            "input_item_types": types,
            "input_items": len(inp) if isinstance(inp, list) else None,
            "markers_anywhere_in_body": [m for m in MARKERS if m in text],
            "markers_in_input": [m for m in MARKERS if m in input_text],
            "tool_call_items_in_input": [i.get("type") for i in (inp or []) if isinstance(i, dict) and ("call" in str(i.get("type")) or "output" in str(i.get("type")))],
            "example_lookup_offered_as_tool": any("example_lookup" in json.dumps(t) for t in (b.get("tools") or [])) if isinstance(b, dict) else None,
            "prompt_present": PROMPT in input_text,
        })
    return out, reqs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--binary", required=True)
    ap.add_argument("--double", required=True)
    ap.add_argument("--tap", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--root", default="/tmp/cvx-eud1b")
    ap.add_argument("--cleanup", action="store_true")
    a = ap.parse_args()
    if shutil.which("codex") and os.path.realpath(shutil.which("codex")) == os.path.realpath(a.binary):
        raise SystemExit("refusing: binary must be a scratch binary, not the codex on PATH")
    if os.environ.get("USER") and os.environ["USER"] in a.root:
        raise SystemExit("refusing: root path contains the user name")
    p = Probe2(a)
    p.setup()
    tap_log = os.path.join(p.logs, "tap.jsonl")
    tap = subprocess.Popen([sys.executable, "-B", a.tap, "--port", str(TAP_PORT), "--log", tap_log, "--capture-only"],
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
    analysis, reqs = analyse(tap_log)
    obs["model_input"] = analysis
    host = socket.gethostname()
    user = os.environ.get("USER", "\0")
    needles = [os.path.expanduser("~"), host, host.split(".")[0], user, user.capitalize()]
    os.makedirs(a.out, exist_ok=True)
    for name, obj in (("observations.json", obs), ("frames.json", p.frames), ("events.json", p.events), ("model_requests.json", reqs)):
        with open(os.path.join(a.out, name), "w") as f:
            f.write(P1.scrub(obj, needles))
    import redact  # HOSTING §9.1 categories (RV2 EUD1-R11; R23-48 item 3), applied to every later run
    redact.redact_dir(a.out)
    leaked = [n for n in needles if n and n != "\0" and any(n in open(os.path.join(a.out, f)).read() for f in os.listdir(a.out))]
    print("redaction check:", "no user or host name left" if not leaked else "LEAK %d needle(s)" % len(leaked))
    if a.cleanup:
        shutil.rmtree(a.root)
        print("removed", a.root)
    print(json.dumps({"stop_reason": p.stop_reason, "requests": analysis["requests"],
                      "markers_in_input": [r["markers_in_input"] for r in analysis["per_request"]]}))


if __name__ == "__main__":
    main()
