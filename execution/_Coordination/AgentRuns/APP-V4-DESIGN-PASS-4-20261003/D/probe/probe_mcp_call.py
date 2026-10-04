#!/usr/bin/env python3
"""H-1 side probe (R23-34 item 3): does an App-origin `mcpServer/tool/call`
result enter the thread's items, or its rollout history (which later turns
send to the model)? HOSTING-v0.9 §6.8 marks this "not observed".

Bounded observation (owner O-D). Not product code; not qualification. Limits,
as R23-34.3 sets them:
- an existing scratch Codex binary (0.158.0), passed with --binary; never the
  `codex` on PATH, never ~/.codex;
- a scratch home under a path without the user name (default /tmp/cvx-eud1),
  with HOME also pointed there, removed afterwards by --cleanup;
- DEL-01-01's MCP double (`obs1_mcp_double.py`, copied into the scratch
  path), no network, no sign-in, no model (the provider points at a loopback
  port nothing listens on, and no turn is started), no download.
Guard: every 250 ms the process group's IP sockets are listed (`lsof`); any
non-loopback socket, or any `git` process, stops the probe at once.

Usage: probe_mcp_call.py --binary PATH --double PATH --out DIR [--root /tmp/cvx-eud1] [--cleanup]
"""
import argparse
import json
import os
import re
import shutil
import signal
import subprocess
import sys
import threading
import time

T0 = time.monotonic()


def ms():
    return int((time.monotonic() - T0) * 1000)


class Probe:
    def __init__(self, a):
        self.a = a
        self.root = a.root
        self.home = os.path.join(self.root, "codex-home")
        self.cwd = os.path.join(self.root, "cwd")
        self.logs = os.path.join(self.root, "logs")
        self.frames = []
        self.events = []
        self.pending = {}
        self.next_id = 1
        self.lock = threading.Lock()
        self.stop = threading.Event()
        self.stop_reason = None

    def ev(self, kind, **kw):
        kw.update({"t_ms": ms(), "kind": kind})
        self.events.append(kw)

    def setup(self):
        if os.path.exists(self.root):
            raise SystemExit(f"{self.root} exists; refusing to reuse it")
        for d in (self.home, self.cwd, self.logs, os.path.join(self.root, "h")):
            os.makedirs(d)
        dbl = os.path.join(self.root, "obs1_mcp_double.py")
        shutil.copyfile(self.a.double, dbl)
        cfg = (
            'model = "probe-none"\n'
            'model_provider = "probe_none"\n'
            'sandbox_mode = "read-only"\n'
            'web_search = "disabled"\n\n'
            '[analytics]\nenabled = false\n\n'
            '[features]\nplugins = false\n\n'
            '[model_providers.probe_none]\n'
            'name = "EU-D1 probe: no model"\n'
            'base_url = "http://127.0.0.1:9/v1"\n'
            'wire_api = "responses"\n\n'
            '[mcp_servers.double]\n'
            'command = "/usr/bin/python3"\n'
            f'args = ["{dbl}", "--log", "{os.path.join(self.logs, "mcp_double.jsonl")}"]\n')
        with open(os.path.join(self.home, "config.toml"), "w") as f:
            f.write(cfg)
        self.ev("setup", root=self.root, config=cfg)

    # ------------------------------------------------ JSON-RPC
    def send(self, obj):
        line = json.dumps(obj)
        self.frames.append({"t_ms": ms(), "dir": "out", "raw": obj})
        self.proc.stdin.write((line + "\n").encode())
        self.proc.stdin.flush()

    def request(self, method, params, timeout=30):
        with self.lock:
            rid = self.next_id
            self.next_id += 1
            ev = threading.Event()
            self.pending[rid] = [ev, None]
        self.send({"jsonrpc": "2.0", "id": rid, "method": method, "params": params})
        ev.wait(timeout)
        return self.pending.pop(rid)[1]

    def notify(self, method, params=None):
        o = {"jsonrpc": "2.0", "method": method}
        if params is not None:
            o["params"] = params
        self.send(o)

    def reader(self):
        for line in self.proc.stdout:
            try:
                msg = json.loads(line)
            except ValueError:
                self.frames.append({"t_ms": ms(), "dir": "in", "unparsed": line.decode(errors="replace")})
                continue
            self.frames.append({"t_ms": ms(), "dir": "in", "raw": msg})
            if "id" in msg and ("result" in msg or "error" in msg) and msg["id"] in self.pending:
                self.pending[msg["id"]][1] = msg
                self.pending[msg["id"]][0].set()
            elif "id" in msg and "method" in msg:
                # a server request: decline; this probe performs no act and answers nothing affirmatively
                self.ev("server-request", method=msg["method"])
                self.send({"jsonrpc": "2.0", "id": msg["id"], "error": {"code": -32601, "message": "probe answers no server request"}})

    def stderr_reader(self):
        with open(os.path.join(self.logs, "stderr.txt"), "wb") as f:
            for line in self.proc.stderr:
                f.write(line)

    def guard(self):
        while not self.stop.is_set():
            try:
                out = subprocess.run(["lsof", "-nP", "-a", "-i", "-g", str(self.pgid)], capture_output=True, text=True).stdout
                for l in out.splitlines()[1:]:
                    name = l.split()[-1] if l.split() else ""
                    if l.endswith("(LISTEN)"):
                        continue
                    if "->" in l:
                        remote = l.split("->")[1].split()[0]
                        host = remote.rsplit(":", 1)[0].strip("[]")
                        if host not in ("127.0.0.1", "::1", "localhost"):
                            self.halt("non-loopback socket: " + remote)
                ps = subprocess.run(["ps", "-o", "comm=", "-g", str(self.pgid)], capture_output=True, text=True).stdout
                if any(os.path.basename(c.strip()) == "git" for c in ps.splitlines()):
                    self.halt("git process in the group")
            except Exception as exc:  # pragma: no cover
                self.ev("guard-error", error=repr(exc))
            time.sleep(0.25)

    def halt(self, why):
        if not self.stop.is_set():
            self.stop_reason = why
            self.ev("STOP", reason=why)
            self.stop.set()
            try:
                os.killpg(self.pgid, signal.SIGKILL)
            except OSError:
                pass

    # ------------------------------------------------ sequence
    def run(self):
        env = {"PATH": "/usr/bin:/bin:/usr/sbin:/sbin", "CODEX_HOME": self.home, "HOME": os.path.join(self.root, "h"),
               "TMPDIR": os.path.join(self.root, "h")}
        self.proc = subprocess.Popen([self.a.binary, "app-server"], cwd=self.cwd, env=env, stdin=subprocess.PIPE,
                                     stdout=subprocess.PIPE, stderr=subprocess.PIPE, start_new_session=True)
        self.pgid = os.getpgid(self.proc.pid)
        self.ev("spawn", argv=["<scratch codex 0.158.0>", "app-server"], env_keys=sorted(env))
        for t in (self.reader, self.stderr_reader, self.guard):
            threading.Thread(target=t, daemon=True).start()
        obs = {}
        try:
            r = self.request("initialize", {"clientInfo": {"name": "chirality-eud1-probe", "title": "EU-D1 probe", "version": "0.0.0"},
                                            "capabilities": {"experimentalApi": False, "requestAttestation": False}})
            obs["initialize_ok"] = bool(r and "result" in r)
            obs["codexHome"] = (r or {}).get("result", {}).get("codexHome")
            if os.path.realpath(obs["codexHome"] or "") != os.path.realpath(self.home):
                self.halt("codexHome is not the scratch home")
                return obs
            self.notify("initialized")
            time.sleep(3.0)
            r = self.request("mcpServerStatus/list", {})
            obs["mcp_status"] = (r or {}).get("result") or (r or {}).get("error")
            r = self.request("thread/start", {"cwd": self.cwd, "approvalPolicy": "never", "sandbox": "read-only"}, timeout=60)
            obs["thread_start"] = (r or {}).get("error") or "ok"
            tid = (((r or {}).get("result") or {}).get("thread") or {}).get("id")
            obs["thread_id"] = tid
            if not tid or self.stop.is_set():
                return obs
            time.sleep(3.0)
            r = self.request("thread/items/list", {"threadId": tid})
            obs["items_before"] = (r or {}).get("result") or (r or {}).get("error")
            n_before = len(self.frames)
            r = self.request("mcpServer/tool/call", {"server": "double", "threadId": tid, "tool": "example_lookup",
                                                    "arguments": {"key": "EX-1"}}, timeout=60)
            obs["tool_call_response"] = r
            time.sleep(3.0)
            obs["notifications_after_call"] = [f["raw"].get("method") for f in self.frames[n_before:]
                                               if f["dir"] == "in" and "method" in f.get("raw", {})]
            r = self.request("thread/items/list", {"threadId": tid})
            obs["items_after"] = (r or {}).get("result") or (r or {}).get("error")
            r = self.request("thread/read", {"threadId": tid, "includeTurns": True})
            obs["thread_read_after"] = (r or {}).get("result") or (r or {}).get("error")
        finally:
            self.ev("end", stop_reason=self.stop_reason)
            try:
                self.proc.stdin.close()
            except OSError:
                pass
            try:
                self.proc.wait(timeout=10)
            except subprocess.TimeoutExpired:
                os.killpg(self.pgid, signal.SIGKILL)
            self.stop.set()
        return obs

    def rollouts(self):
        hits = []
        for d, _, fs in os.walk(self.home):
            for f in fs:
                if f.endswith(".jsonl"):
                    p = os.path.join(d, f)
                    with open(p, encoding="utf-8", errors="replace") as h:
                        text = h.read()
                    hits.append({"file": os.path.relpath(p, self.home), "lines": text.count("\n"),
                                 "mentions_example_lookup": "example_lookup" in text, "mentions_P-EX-1": "P-EX-1" in text})
        return hits


def scrub(obj, needles):
    s = json.dumps(obj, indent=2, ensure_ascii=False)
    for n in needles:
        s = s.replace(n, "<REDACTED>")
    return s + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--binary", required=True)
    ap.add_argument("--double", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--root", default="/tmp/cvx-eud1")
    ap.add_argument("--cleanup", action="store_true")
    a = ap.parse_args()
    if "/.codex" in a.binary or shutil.which("codex") and os.path.realpath(shutil.which("codex")) == os.path.realpath(a.binary):
        raise SystemExit("refusing: binary must be a scratch binary, not the codex on PATH")
    if os.environ.get("USER", "") and os.environ["USER"] in a.root:
        raise SystemExit("refusing: root path contains the user name")
    p = Probe(a)
    p.setup()
    obs = p.run()
    obs["rollouts"] = p.rollouts()
    dbl_log = os.path.join(p.logs, "mcp_double.jsonl")
    obs["double_received"] = [json.loads(l).get("raw", "")[:200] for l in open(dbl_log)] if os.path.exists(dbl_log) else None
    obs["stop_reason"] = p.stop_reason
    import socket
    host = socket.gethostname()
    needles = [os.path.expanduser("~"), host, host.split(".")[0], os.environ.get("USER", "\0"),
               os.environ.get("USER", "\0").capitalize()]
    os.makedirs(a.out, exist_ok=True)
    with open(os.path.join(a.out, "observations.json"), "w") as f:
        f.write(scrub(obs, needles))
    with open(os.path.join(a.out, "frames.json"), "w") as f:
        f.write(scrub(p.frames, needles))
    with open(os.path.join(a.out, "events.json"), "w") as f:
        f.write(scrub(p.events, needles))
    err = open(os.path.join(p.logs, "stderr.txt"), "rb").read().decode(errors="replace")
    with open(os.path.join(a.out, "stderr.txt"), "w") as f:
        f.write(scrub(err, needles))
    import redact  # HOSTING §9.1 categories (RV2 EUD1-R11; R23-48 item 3), applied to every later run
    redact.redact_dir(a.out)
    leaked = [n for n in needles if n and n != "\0" and any(n in open(os.path.join(a.out, f)).read() for f in os.listdir(a.out))]
    print("redaction check:", "no user or host name left" if not leaked else "LEAK %d needle(s)" % len(leaked))
    if a.cleanup:
        shutil.rmtree(a.root)
        print("removed", a.root)
    print(json.dumps({"stop_reason": p.stop_reason, "thread": obs.get("thread_id")}))


if __name__ == "__main__":
    main()
