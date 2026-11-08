#!/usr/bin/env python3
"""OBS-1 observation harness: one live Codex App Server turn at pin 0.158.0.

Prototype only (DEL-01-01, run APP-V4-DESIGN-PASS-2-20260930, node OBS-1).
Not product code; not an App candidate; nothing here is qualified. Python 3
standard library only. Follows WAVE_B/OBS-1_BRIEF.md sections 5, 6 and 8 with
the integrator's decisions in BRIEFS.md ("OBS-1 - the live Codex turn"):
one turn only (part B is not run), route R-1 only, part D (a second
thread/start with per-thread MCP configuration and no turn) allowed.

What it does:
  D-1 spawn `<binary> app-server` with CODEX_HOME=<obs>/codex-home, cwd
      <obs>/cwd, in its own process group; one reader per stream.
  D-2..D-9 as the brief's table, with a recording tap writing every frame in
      both directions, unchanged, to <obs>/logs/frames.jsonl with direction,
      send/receipt position, monotonic offset and wall-clock ms.
  Answers to server requests use the brief's section 5 table, each recorded
  with origin "observation-harness" (never a person's act).
  Snapshots every 250 ms (process group, `lms` processes, IP sockets of the
  group, paths under ~/.codex opened by the group) into
  <obs>/logs/snapshots.jsonl (written when a value changes).
  Stop conditions S-1, S-2 (from the download watch), S-3, S-4, S-5, S-6,
  S-7 and S-8 are checked where the brief says.

Usage:
  obs1_harness.py --obs DIR --binary PATH --model KEY --mcp-double PATH [--part-d]
"""
import argparse
import ipaddress
import json
import os
import re
import signal
import subprocess
import sys
import threading
import time

T0 = time.monotonic()
HOME = os.path.expanduser("~")


def wall_ms():
    return int(time.time() * 1000)


def mono_ms():
    return round((time.monotonic() - T0) * 1000, 1)


class Recorder:
    def __init__(self, logdir):
        self.logdir = logdir
        self.lock = threading.Lock()
        self.frames = open(os.path.join(logdir, "frames.jsonl"), "a", encoding="utf-8")
        self.events = open(os.path.join(logdir, "harness_events.jsonl"), "a", encoding="utf-8")
        self.send_pos = 0
        self.recv_pos = 0

    def frame(self, direction, raw):
        with self.lock:
            if direction == "send":
                self.send_pos += 1
                pos = self.send_pos
            else:
                self.recv_pos += 1
                pos = self.recv_pos
            rec = {"dir": direction, "pos": pos, "mono_ms": mono_ms(), "wall_ms": wall_ms(), "raw": raw}
            self.frames.write(json.dumps(rec, ensure_ascii=False) + "\n")
            self.frames.flush()
            return rec

    def event(self, kind, **kw):
        rec = {"event": kind, "mono_ms": mono_ms(), "wall_ms": wall_ms()}
        rec.update(kw)
        with self.lock:
            self.events.write(json.dumps(rec, ensure_ascii=False) + "\n")
            self.events.flush()
        sys.stderr.write("[harness %8.1f] %s %s\n" % (rec["mono_ms"], kind, json.dumps(kw, ensure_ascii=False)[:300]))


# GitHub address ranges (for classifying the supplier's plugin-repository fetch; U-18).
GITHUB_NETS = [ipaddress.ip_network(n) for n in (
    "140.82.112.0/20", "143.55.64.0/20", "185.199.108.0/22", "192.30.252.0/22",
    "2606:50c0::/32", "2a0a:a440::/29")]


def is_loopback(addr):
    try:
        return ipaddress.ip_address(addr).is_loopback
    except ValueError:
        return addr in ("localhost", "*")


def is_github(addr):
    try:
        ip = ipaddress.ip_address(addr)
    except ValueError:
        return False
    return any(ip in n for n in GITHUB_NETS)


def parse_remote(name_field):
    # lsof NAME like "127.0.0.1:55012->127.0.0.1:1234 (ESTABLISHED)" or "[::1]:x->[::1]:y"
    m = re.search(r"->\[?([0-9a-fA-F:.]+)\]?:(\d+)", name_field)
    if not m:
        return None, None
    return m.group(1), int(m.group(2))


class Harness:
    def __init__(self, a):
        self.a = a
        self.obs = a.obs
        self.logdir = os.path.join(self.obs, "logs")
        self.home = os.path.join(self.obs, "codex-home")
        self.cwd = os.path.join(self.obs, "cwd")
        self.rec = Recorder(self.logdir)
        self.next_id = 0
        self.pending = {}          # id -> threading.Event, result slot
        self.results = {}
        self.cv = threading.Condition()
        self.notifications = []    # (mono, frame)
        self.proc = None
        self.pgid = None
        self.stop_reason = None
        self.stop_evt = threading.Event()
        self.turn_active = False
        self.turn_completed = threading.Event()
        self.thread_id = None
        self.turn_id = None
        self.snap_last = {}
        self.snap_count = 0
        self.snap_done = threading.Event()
        self.nonloop = []

    # ---------- transport ----------
    def send(self, obj):
        raw = json.dumps(obj, separators=(",", ":"), ensure_ascii=False)
        self.rec.frame("send", raw)
        try:
            self.proc.stdin.write((raw + "\n").encode("utf-8"))
            self.proc.stdin.flush()
        except (BrokenPipeError, OSError) as exc:
            self.rec.event("write-failed", error=repr(exc), frame_id=obj.get("id"))

    def request(self, method, params, timeout=60.0):
        self.next_id += 1
        rid = self.next_id
        ev = threading.Event()
        with self.cv:
            self.pending[rid] = ev
        self.send({"jsonrpc": "2.0", "id": rid, "method": method, "params": params})
        if not ev.wait(timeout):
            self.rec.event("response-not-observed", method=method, id=rid, outcome="unknown")
            return None
        return self.results.pop(rid)

    def notify(self, method, params=None):
        obj = {"jsonrpc": "2.0", "method": method}
        if params is not None:
            obj["params"] = params
        self.send(obj)

    def reader(self):
        for line in self.proc.stdout:
            raw = line.decode("utf-8", "replace").rstrip("\n")
            self.rec.frame("recv", raw)
            try:
                msg = json.loads(raw)
            except ValueError:
                self.rec.event("malformed-frame", raw=raw[:200])
                continue
            if "id" in msg and ("result" in msg or "error" in msg) and "method" not in msg:
                with self.cv:
                    ev = self.pending.pop(msg["id"], None)
                if ev:
                    self.results[msg["id"]] = msg
                    ev.set()
                else:
                    self.rec.event("unmatched-response", id=msg.get("id"))
            elif "id" in msg and "method" in msg:
                threading.Thread(target=self.answer_server_request, args=(msg,), daemon=True).start()
            elif "method" in msg:
                self.on_notification(msg)
        self.rec.event("stdout-eof")

    def stderr_reader(self):
        cap = 1_000_000
        n = 0
        with open(os.path.join(self.logdir, "codex.stderr"), "ab") as f:
            for chunk in iter(lambda: self.proc.stderr.read1(65536) if hasattr(self.proc.stderr, "read1") else self.proc.stderr.read(4096), b""):
                n += len(chunk)
                if n <= cap:
                    f.write(chunk)
                    f.flush()
        self.rec.event("stderr-eof", bytes=n, kept=min(n, cap))

    # ---------- notifications ----------
    def on_notification(self, msg):
        m = msg.get("method")
        p = msg.get("params") or {}
        if m == "turn/completed":
            self.turn_completed.set()
        if m in ("account/login/completed", "account/updated") :
            self.rec.event("account-notification", method=m)
        if m == "error":
            self.rec.event("supplier-error-notification", params=p)
            text = json.dumps(p).lower()
            if any(k in text for k in ("unauthorized", "401", "login", "sign in", "auth")):
                self.rec.event("possible-auth-error", note="checked against S-3 after the run")

    # ---------- server requests (brief section 5 answers; origin observation-harness) ----------
    def _is_obs1_subject(self, method, p):
        blob = json.dumps(p)
        return ("obs1" in blob) or ("example_lookup" in blob)

    def answer_server_request(self, msg):
        rid, method, p = msg["id"], msg["method"], msg.get("params") or {}
        subject_obs1 = self._is_obs1_subject(method, p)
        answer = None
        error = None
        rule = None
        if method == "item/permissions/requestApproval":
            if subject_obs1:
                answer = {"permissions": {k: v for k, v in (p.get("permissions") or {}).items() if v is not None},
                          "scope": "turn"}
                rule = "approval, subject obs1 -> grant requested permissions, scope turn"
            else:
                answer = {"permissions": {}, "scope": "turn"}
                rule = "approval, other subject -> decline form (grant nothing)"
        elif method in ("item/commandExecution/requestApproval", "item/fileChange/requestApproval"):
            answer = {"decision": "accept" if subject_obs1 else "decline"}
            rule = "approval -> %s" % answer["decision"]
        elif method in ("execCommandApproval", "applyPatchApproval"):
            answer = {"decision": "approved" if subject_obs1 else {"denied": {"rejection": "observation harness declines"}}}
            rule = "legacy approval"
        elif method == "mcpServer/elicitation/request":
            meta = p.get("_meta") or {}
            kind = meta.get("codex_approval_kind") if isinstance(meta, dict) else None
            if p.get("serverName") == "obs1" and kind == "mcp_tool_call":
                answer = {"action": "accept", "content": {}, "_meta": None}
                rule = "elicitation carrying an MCP tool-call approval (codex_approval_kind mcp_tool_call) for obs1 -> accept (row 1 of the brief's answer table)"
            else:
                answer = {"action": "decline", "content": None, "_meta": None}
                rule = "elicitation -> decline"
        elif method == "item/tool/requestUserInput":
            answers = {}
            for q in p.get("questions") or []:
                opts = q.get("options") or []
                qblob = json.dumps(q).lower()
                chosen = "Invented example answer: proceed."
                if opts and subject_obs1 and ("approv" in qblob or "allow" in qblob or "mcp" in qblob):
                    for o in opts:
                        lab = (o.get("label") or "")
                        if re.search(r"allow|approve|accept|yes|run", lab, re.I) and not re.search(r"always|session|deny|decline|cancel|don", lab, re.I):
                            chosen = lab
                            break
                answers[q.get("id")] = {"answers": [chosen]}
            answer = {"answers": answers}
            rule = "requestUserInput -> invented answer (or the accept option for an obs1 tool approval)"
        else:
            if method == "account/chatgptAuthTokens/refresh" or method.startswith("account/"):
                self.trigger_stop("S-3", "sign-in related server request: %s" % method)
            error = {"code": -32601, "message": "observation harness: not answered (%s)" % method}
            rule = "explicit JSON-RPC error"
        self.rec.event("server-request", id=rid, method=method, subject_obs1=subject_obs1, rule=rule,
                       origin="observation-harness")
        if error is not None:
            self.send({"jsonrpc": "2.0", "id": rid, "error": error})
        else:
            self.send({"jsonrpc": "2.0", "id": rid, "result": answer})

    # ---------- snapshots ----------
    def snapshot_loop(self):
        path = os.path.join(self.logdir, "snapshots.jsonl")
        watch = os.path.join(self.logdir, "download_watch.log")
        watch_pos = os.path.getsize(watch) if os.path.exists(watch) else 0
        with open(path, "a", encoding="utf-8") as out:
            while not self.snap_done.is_set():
                t = wall_ms()
                snap = {}
                try:
                    ps = subprocess.run(["ps", "-axo", "pid=,ppid=,pgid=,command="], capture_output=True, text=True).stdout
                    rows = []
                    for line in ps.splitlines():
                        parts = line.split(None, 3)
                        if len(parts) < 4:
                            continue
                        pid, ppid, pgid, cmd = parts
                        if (self.pgid and pgid == str(self.pgid)) or re.search(r"(^|/)lms( |$)", cmd):
                            rows.append([int(pid), int(ppid), int(pgid), cmd[:300]])
                    snap["procs"] = rows
                    if self.pgid:
                        li = subprocess.run(["lsof", "-nP", "-a", "-i", "-g", str(self.pgid)], capture_output=True, text=True).stdout
                        socks = [l for l in li.splitlines()[1:]]
                        snap["sockets"] = socks
                        lf = subprocess.run(["lsof", "-nP", "-g", str(self.pgid)], capture_output=True, text=True).stdout
                        snap["dotcodex"] = [l for l in lf.splitlines() if (HOME + "/.codex") in l]
                except Exception as exc:  # noqa: BLE001 - recorded
                    snap["error"] = repr(exc)
                try:
                    snap["mem_pressure_level"] = subprocess.run(
                        ["sysctl", "-n", "kern.memorystatus_vm_pressure_level"],
                        capture_output=True, text=True).stdout.strip()
                except OSError:
                    pass
                if snap.get("mem_pressure_level") == "4":
                    self.trigger_stop("S-9", "memory pressure level critical (4)")
                self.snap_count += 1
                for key, val in snap.items():
                    if self.snap_last.get(key) != val:
                        out.write(json.dumps({"wall_ms": t, "mono_ms": mono_ms(), key: val}, ensure_ascii=False) + "\n")
                        out.flush()
                        self.snap_last[key] = val
                # S-6
                if snap.get("dotcodex"):
                    self.trigger_stop("S-6", "process group opened a path under ~/.codex")
                # S-5 and L-4 classification
                for l in snap.get("sockets") or []:
                    cols = l.split()
                    name = " ".join(cols[8:]) if len(cols) > 8 else l
                    raddr, rport = parse_remote(name)
                    if raddr is None or is_loopback(raddr):
                        continue
                    proc = cols[0] if cols else "?"
                    key = (proc, raddr, rport)
                    if key not in [tuple(x[:3]) for x in self.nonloop]:
                        gh = is_github(raddr)
                        self.nonloop.append([proc, raddr, rport, t, self.turn_active, gh])
                        self.rec.event("non-loopback-socket", process=proc, remote=raddr, port=rport,
                                       during_turn=self.turn_active, github_range=gh)
                        if self.turn_active and not gh:
                            self.trigger_stop("S-5", "non-loopback connection from the Codex process group during the turn: %s %s:%s" % (proc, raddr, rport))
                # S-2 from the download watch
                try:
                    if os.path.exists(watch):
                        with open(watch, "r", encoding="utf-8") as w:
                            w.seek(watch_pos)
                            new = w.read()
                            watch_pos = w.tell()
                        for line in new.splitlines():
                            if " S-2 " in line:
                                self.trigger_stop("S-2", line[:300])
                    for r in snap.get("procs") or []:
                        if re.search(r"\blms\b.*\bget\b", r[3]):
                            self.trigger_stop("S-2", "lms get process: %s" % r[3])
                except OSError:
                    pass
                time.sleep(0.25)

    # ---------- stops ----------
    def trigger_stop(self, sid, reason):
        if self.stop_reason is None:
            self.stop_reason = (sid, reason)
            self.rec.event("STOP", id=sid, reason=reason)
            if sid in ("S-5", "S-7") and self.turn_active and self.thread_id and self.turn_id:
                self.request_async("turn/interrupt", {"threadId": self.thread_id, "turnId": self.turn_id})
            self.stop_evt.set()

    def request_async(self, method, params):
        self.next_id += 1
        self.send({"jsonrpc": "2.0", "id": self.next_id, "method": method, "params": params})

    # ---------- sequence ----------
    def run(self):
        a = self.a
        obs_real = os.path.realpath(self.obs)
        env = dict(os.environ)
        env["CODEX_HOME"] = self.home
        self.rec.event("capture-metadata", scenario="OBS-1 one live turn", pin="0.158.0",
                       launcher="vendor", provider_route="R-1 obs1_lmstudio", model=a.model,
                       approval_policy="on-request", sandbox="read-only", env_keys_added=["CODEX_HOME"])
        # D-1
        self.proc = subprocess.Popen([a.binary, "app-server"], cwd=self.cwd, env=env,
                                     stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                     start_new_session=True)
        self.pgid = os.getpgid(self.proc.pid)
        self.rec.event("D-1 spawn", pid=self.proc.pid, pgid=self.pgid, argv=["<V>", "app-server"],
                       env_keys_added=["CODEX_HOME"], cwd="<OBS>/cwd")
        threading.Thread(target=self.reader, daemon=True).start()
        threading.Thread(target=self.stderr_reader, daemon=True).start()
        snap_t = threading.Thread(target=self.snapshot_loop, daemon=True)
        snap_t.start()
        try:
            self.sequence(obs_real)
        finally:
            self.finish()

    def _under_obs(self, path, obs_real):
        if not isinstance(path, str):
            return True
        rp = os.path.realpath(path)
        return rp.startswith(obs_real) or path.startswith(self.obs)

    def sequence(self, obs_real):
        a = self.a
        # D-2
        r = self.request("initialize", {"clientInfo": {"name": "chirality-obs1", "title": "Chirality OBS-1",
                                                       "version": "0.0.0-obs1"},
                                        "capabilities": {"experimentalApi": False, "requestAttestation": False}})
        if r is None or "result" not in r:
            self.trigger_stop("S-11", "initialize failed: %r" % (r,))
            return
        ch = r["result"].get("codexHome")
        if os.path.realpath(ch or "") != os.path.realpath(self.home):
            self.trigger_stop("S-1", "codexHome %r is not <OBS>/codex-home" % ch)
            return
        # D-3
        self.notify("initialized")
        time.sleep(3.0)  # let early notifications (MCP startup) arrive
        # D-4
        r = self.request("mcpServerStatus/list", {}, timeout=60)
        self.rec.event("D-4 mcpServerStatus/list", ok=bool(r and "result" in r))
        if self.stop_evt.is_set():
            return
        # D-5
        dev = ("You are running an observation test with invented data. When asked, use the "
               "example_lookup tool. Keep replies to one sentence.")
        r = self.request("thread/start", {"cwd": self.cwd, "model": a.model, "modelProvider": "obs1_lmstudio",
                                          "approvalPolicy": "on-request", "sandbox": "read-only",
                                          "developerInstructions": dev}, timeout=120)
        if r is None or "result" not in r:
            err = (r or {}).get("error")
            self.trigger_stop("R-1-thread-start-failed", "thread/start failed: %r (route R-1 only; R-2 not tried)" % (err,))
            return
        res = r["result"]
        self.thread_id = (res.get("thread") or {}).get("id")
        rep_model, rep_prov = res.get("model"), res.get("modelProvider")
        self.rec.event("D-5 thread/start", thread=self.thread_id, requested_model=a.model, reported_model=rep_model,
                       requested_provider="obs1_lmstudio", reported_provider=rep_prov,
                       instructionSources=res.get("instructionSources"))
        if rep_model != a.model or rep_prov != "obs1_lmstudio":
            self.trigger_stop("S-3", "thread start reports model %r provider %r" % (rep_model, rep_prov))
            return
        for src in res.get("instructionSources") or []:
            p = src if isinstance(src, str) else (src.get("path") if isinstance(src, dict) else None)
            if p and not self._under_obs(p, obs_real):
                self.trigger_stop("S-4", "instructionSources lists a path outside OBS: %r" % p)
                return
        if self.stop_evt.is_set():
            return
        # D-6
        prompt = ("This is a test with invented data. Call the tool example_lookup with key EX-1. Then call it "
                  "again with key EX-ERR. Then reply in one sentence naming the proposal from the first call and "
                  "saying whether the second key was found.")
        self.turn_active = True
        r = self.request("turn/start", {"threadId": self.thread_id,
                                        "input": [{"type": "text", "text": prompt, "text_elements": []}]}, timeout=60)
        if r is None or "result" not in r:
            self.turn_active = False
            self.trigger_stop("S-11", "turn/start failed: %r" % (r,))
            return
        self.turn_id = ((r["result"] or {}).get("turn") or {}).get("id")
        self.rec.event("D-6 turn/start", turn=self.turn_id)
        # D-8: wait for turn/completed or the time limit (S-7), or another stop
        deadline = time.monotonic() + 600
        while time.monotonic() < deadline:
            if self.turn_completed.wait(0.5):
                break
            if self.stop_evt.is_set():
                self.turn_completed.wait(60)
                self.turn_active = False
                return
        else:
            self.trigger_stop("S-7", "no turn/completed within 10 minutes")
            self.turn_completed.wait(60)
            self.turn_active = False
            return
        self.turn_active = False
        self.rec.event("turn/completed received")
        time.sleep(2.0)
        # Part D: per-thread MCP configuration, no turn
        if a.part_d and not self.stop_evt.is_set():
            cfg = {"mcp_servers.obs1d": {"command": "/usr/bin/python3",
                                         "args": [a.mcp_double, "--log", os.path.join(self.logdir, "mcp_partd.jsonl")]}}
            r = self.request("thread/start", {"cwd": self.cwd, "model": a.model, "modelProvider": "obs1_lmstudio",
                                              "approvalPolicy": "on-request", "sandbox": "read-only",
                                              "config": cfg}, timeout=120)
            tid2 = ((r or {}).get("result") or {}).get("thread", {}).get("id") if r and "result" in r else None
            self.rec.event("part-D thread/start", ok=bool(r and "result" in r), thread=tid2,
                           error=(r or {}).get("error"))
            time.sleep(4.0)
            if tid2:
                self.request("mcpServerStatus/list", {"threadId": tid2}, timeout=60)
            self.request("mcpServerStatus/list", {}, timeout=60)

    def finish(self):
        # D-9: stop record first, then close stdin
        reason = "OBS-1 end" if self.stop_reason is None else "stop %s: %s" % self.stop_reason
        self.rec.event("D-9 stop-record", actor="HELP_HUMAN (delegated OBS-1 executor)", reason=reason)
        try:
            self.proc.stdin.close()
        except OSError:
            pass
        try:
            code = self.proc.wait(timeout=10 if self.stop_reason is None else 2)
        except subprocess.TimeoutExpired:
            self.rec.event("exit-wait-expired; SIGTERM to process group")
            try:
                os.killpg(self.pgid, signal.SIGTERM)
                code = self.proc.wait(timeout=5)
            except (subprocess.TimeoutExpired, ProcessLookupError):
                try:
                    os.killpg(self.pgid, signal.SIGKILL)
                except ProcessLookupError:
                    pass
                code = self.proc.wait()
        self.rec.event("exit", returncode=code, signal=(-code if code is not None and code < 0 else None))
        time.sleep(0.5)
        ps = subprocess.run(["ps", "-axo", "pid=,ppid=,pgid=,command="], capture_output=True, text=True).stdout
        left = [l for l in ps.splitlines() if l.split(None, 3)[2:3] == [str(self.pgid)]]
        self.rec.event("process-tree-500ms-after-exit", survivors=left)
        self.snap_done.set()
        self.rec.event("snapshots", count=self.snap_count, non_loopback=self.nonloop)
        if left:
            try:
                os.killpg(self.pgid, signal.SIGTERM)
                self.rec.event("survivors-terminated", pgid=self.pgid)
            except ProcessLookupError:
                pass


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--obs", required=True)
    ap.add_argument("--binary", required=True)
    ap.add_argument("--model", required=True)
    ap.add_argument("--mcp-double", required=True)
    ap.add_argument("--part-d", action="store_true")
    a = ap.parse_args()
    h = Harness(a)
    h.run()
    print(json.dumps({"stop": h.stop_reason, "thread": h.thread_id, "turn": h.turn_id}))


if __name__ == "__main__":
    main()
