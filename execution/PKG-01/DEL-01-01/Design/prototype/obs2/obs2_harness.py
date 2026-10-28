#!/usr/bin/env python3
"""OBS-2 observation harness: local observations of Codex App Server at pin 0.158.0.

Prototype only (DEL-01-01, run APP-V4-DESIGN-PASS-3-20261001, node OBS-2).
Not product code; not an App candidate; nothing here is qualified. Python 3
standard library only. Scope: R17_RESOLUTIONS.md R17-16 items O-1...O-7, with
the method of WAVE_B/OBS-1_BRIEF.md (scratch layout section 3, network
observation section 6, what may be sent section 7, stop conditions section 8,
redaction section 12), adapted.

Hard limits honoured by construction: scratch CODEX_HOMEs under the OBS folder
only (never ~/.codex); no sign-in request is ever answered (account/* server
requests get an explicit error and stop the scenario, S-3); no API key or token
is written anywhere; the only model provider is the local LM Studio server on
127.0.0.1:1234; every text sent to the model is invented.

Every answer the harness gives to a supplier request has origin
"observation-harness". It is never a person's act and never A14 evidence.

Scenarios (one per sub-command):
  probe   initialize (experimentalApi true) + experimentalFeature/list +
          config/read + account/read + remoteControl/status/read; no thread.
  o7      start-up traffic per configuration variant (no thread, no model).
  o6      K-1 mechanism: configuration sharing between two scratch homes,
          observed by config/read and account/read only (no thread, no model).
  o1      interrupt a running turn.
  o3      a pending approval request, then turn/interrupt: is the request
          resolved by the supplier before the harness answers?
  o2      stop the app-server with a live turn and a pending request; restart;
          thread/resume; thread/read.
  o5      thread/resume with changed developerInstructions, on a loaded thread
          and on a thread loaded by a new process.
  o4      delegation with experimentalApi: --variants o4a (a native child role from
          `agents.<role>.description`/`config_file`) and/or o4b (task guidance "you do not
          delegate" against a request that invites delegation). Delegation tools reach a
          LM Studio model only through obs2_provider_tap.py --flatten-namespaces (an adapter).
  tools   the tool list Codex sends per configuration (with the tap in --capture-only mode).
  o8      plan mode via collaborationMode on turn/start, a later turn without it, and a turn
          carrying collaborationMode.settings.developer_instructions (O-5b).

The record of the run is Design/OBS_2_0.158.0.md. Scratch homes are created fresh under
<obs>/homes (use --suffix=-x for reruns); raw logs go to <obs>/logs.

Usage:
  obs2_harness.py --obs DIR --binary PATH [--model KEY] [--provider-port N] [--variants ...] SCENARIO
"""
import argparse
import ipaddress
import json
import os
import re
import shutil
import signal
import sqlite3
import subprocess
import sys
import threading
import time

T0 = time.monotonic()
HOME = os.path.expanduser("~")
LMS_BASE = "http://127.0.0.1:1234/v1"
LIVE_PGIDS = set()


def wall_ms():
    return int(time.time() * 1000)


def mono_ms():
    return round((time.monotonic() - T0) * 1000, 1)


def is_loopback(addr):
    try:
        return ipaddress.ip_address(addr).is_loopback
    except ValueError:
        return addr in ("localhost", "*")


def parse_remote(name_field):
    m = re.search(r"->\[?([0-9a-fA-F:.]+)\]?:(\d+)", name_field)
    if not m:
        return None, None
    return m.group(1), int(m.group(2))


class Run:
    """Run-wide context: folders, stop flag, global watches."""

    def __init__(self, a):
        self.a = a
        self.obs = os.path.abspath(a.obs)
        self.obs_real = os.path.realpath(self.obs)
        self.logroot = os.path.join(self.obs, "logs")
        os.makedirs(self.logroot, exist_ok=True)
        self.events = open(os.path.join(self.logroot, "run_events.jsonl"), "a", encoding="utf-8")
        self.lock = threading.Lock()
        self.stop_reason = None
        self.turn_active = False
        self.watch_done = threading.Event()
        self.watch_log = os.path.join(self.logroot, "download_watch.log")

    def event(self, kind, **kw):
        rec = {"event": kind, "mono_ms": mono_ms(), "wall_ms": wall_ms()}
        rec.update(kw)
        with self.lock:
            self.events.write(json.dumps(rec, ensure_ascii=False) + "\n")
            self.events.flush()
        sys.stderr.write("[run %8.1f] %s %s\n" % (rec["mono_ms"], kind, json.dumps(kw, ensure_ascii=False)[:400]))

    def trigger_stop(self, sid, reason):
        if self.stop_reason is None:
            self.stop_reason = (sid, reason)
            self.event("STOP", id=sid, reason=reason)

    def global_watch(self):
        """Memory pressure (S-9) and the download watch log (S-2), every 250 ms."""
        pos = 0
        while not self.watch_done.is_set():
            try:
                lvl = subprocess.run(["sysctl", "-n", "kern.memorystatus_vm_pressure_level"],
                                     capture_output=True, text=True).stdout.strip()
                if lvl == "4":
                    self.trigger_stop("S-9", "memory pressure level critical (4)")
            except OSError:
                pass
            try:
                if os.path.exists(self.watch_log):
                    with open(self.watch_log, "r", encoding="utf-8") as w:
                        w.seek(pos)
                        new = w.read()
                        pos = w.tell()
                    for line in new.splitlines():
                        if " S-2 " in line:
                            self.trigger_stop("S-2", line[:300])
            except OSError:
                pass
            time.sleep(0.25)

    # ---------- homes ----------
    def make_home(self, name, config_text=None, warm=True):
        home = os.path.join(self.obs, "homes", name + self.a.suffix)
        if os.path.exists(home):
            raise SystemExit("home exists already: %s (use a fresh OBS folder or another name)" % home)
        os.makedirs(home)
        if warm:
            # Copy only the plugin cache of the warm template (no sessions, no databases, no
            # credentials: the template holds none), so the supplier's plugin sync does not
            # fetch the repository at start (OBS-1 section 8, S-F-10).
            src = os.path.join(self.obs, "template-home", ".tmp")
            shutil.copytree(src, os.path.join(home, ".tmp"), symlinks=True)
        if config_text is not None:
            with open(os.path.join(home, "config.toml"), "w", encoding="utf-8") as f:
                f.write(config_text)
        for bad in ("auth.json",):
            if os.path.exists(os.path.join(home, bad)):
                raise SystemExit("credential file present in scratch home: refusing")
        return home

    def make_cwd(self, name):
        d = os.path.join(self.obs, "cwd", name)
        os.makedirs(d, exist_ok=True)
        return d


def provider_config(model, ctx, extra=""):
    return ("model = \"%s\"\n"
            "model_provider = \"obs2_lmstudio\"\n"
            "sandbox_mode = \"read-only\"\n"
            "web_search = \"disabled\"\n"
            "model_context_window = %d\n"
            "%s\n"
            "[analytics]\n"
            "enabled = false\n\n"
            "[model_providers.obs2_lmstudio]\n"
            "name = \"LM Studio (OBS-2)\"\n"
            "base_url = \"%s\"\n"
            "wire_api = \"responses\"\n") % (model, ctx, extra, LMS_BASE)


class Session:
    """One `codex app-server` process over stdio, with a recording tap and snapshots."""

    def __init__(self, run, label, home, cwd, argv_extra=(), env_extra=None, policy=None,
                 snap_interval=0.25):
        self.run = run
        self.label = label
        self.home = home
        self.cwd = cwd
        self.argv_extra = list(argv_extra)
        self.env_extra = dict(env_extra or {})
        self.policy = policy or (lambda s, msg: ("error", None, "default: explicit JSON-RPC error"))
        self.snap_interval = snap_interval
        self.logdir = os.path.join(run.logroot, label)
        os.makedirs(self.logdir, exist_ok=True)
        self.frames = open(os.path.join(self.logdir, "frames.jsonl"), "a", encoding="utf-8")
        self.flock = threading.Lock()
        self.send_pos = 0
        self.recv_pos = 0
        self.next_id = 0
        self.pending = {}
        self.results = {}
        self.cv = threading.Condition()
        self.notes = []            # (mono_ms, msg)
        self.server_requests = []  # (mono_ms, msg)
        self.proc = None
        self.pgid = None
        self.snap_done = threading.Event()
        self.snap_last = {}
        self.snap_count = 0
        self.nonloop = []
        self.exit_info = None
        self.kill_on_git = False

    # ---------- tap ----------
    def _frame(self, direction, raw):
        with self.flock:
            if direction == "send":
                self.send_pos += 1
                pos = self.send_pos
            else:
                self.recv_pos += 1
                pos = self.recv_pos
            self.frames.write(json.dumps({"dir": direction, "pos": pos, "mono_ms": mono_ms(),
                                          "wall_ms": wall_ms(), "raw": raw}, ensure_ascii=False) + "\n")
            self.frames.flush()

    def event(self, kind, **kw):
        self.run.event("%s:%s" % (self.label, kind), **kw)

    # ---------- lifecycle ----------
    def start(self):
        env = dict(os.environ)
        env["CODEX_HOME"] = self.home
        env.update(self.env_extra)
        argv = [self.run.a.binary] + self.argv_extra + ["app-server"]
        self.proc = subprocess.Popen(argv, cwd=self.cwd, env=env, stdin=subprocess.PIPE,
                                     stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                     start_new_session=True)
        self.pgid = os.getpgid(self.proc.pid)
        LIVE_PGIDS.add(self.pgid)
        self.event("spawn", pid=self.proc.pid, pgid=self.pgid,
                   argv=["<V>"] + [x.replace(self.run.obs, "<OBS>") for x in self.argv_extra] + ["app-server"],
                   env_keys_added=["CODEX_HOME"] + sorted(self.env_extra), home=self.home.replace(self.run.obs, "<OBS>"))
        threading.Thread(target=self._reader, daemon=True).start()
        threading.Thread(target=self._stderr_reader, daemon=True).start()
        threading.Thread(target=self._snapshot_loop, daemon=True).start()

    def initialize(self, experimental=False, name="chirality-obs2"):
        r = self.request("initialize", {"clientInfo": {"name": name, "title": "Chirality OBS-2", "version": "0.0.0-obs2"},
                                        "capabilities": {"experimentalApi": experimental, "requestAttestation": False}},
                         timeout=60)
        if r is None or "result" not in r:
            self.run.trigger_stop("S-11", "%s initialize failed: %r" % (self.label, r))
            return None
        ch = r["result"].get("codexHome")
        if os.path.realpath(ch or "") != os.path.realpath(self.home):
            self.run.trigger_stop("S-1", "%s codexHome %r is not the scratch home" % (self.label, ch))
            return None
        self.notify("initialized")
        return r["result"]

    def stop(self, mode="stdin", wait=10.0):
        """mode: stdin (close stdin, wait), term (SIGTERM to the group), kill (SIGKILL to the group)."""
        t = mono_ms()
        self.event("stop-begin", mode=mode)
        if mode == "stdin":
            try:
                self.proc.stdin.close()
            except OSError:
                pass
        elif mode == "term":
            try:
                os.killpg(self.pgid, signal.SIGTERM)
            except ProcessLookupError:
                pass
        elif mode == "kill":
            try:
                os.killpg(self.pgid, signal.SIGKILL)
            except ProcessLookupError:
                pass
        escalated = None
        try:
            code = self.proc.wait(timeout=wait)
        except subprocess.TimeoutExpired:
            escalated = "SIGTERM"
            try:
                os.killpg(self.pgid, signal.SIGTERM)
                code = self.proc.wait(timeout=5)
            except (subprocess.TimeoutExpired, ProcessLookupError):
                escalated = "SIGKILL"
                try:
                    os.killpg(self.pgid, signal.SIGKILL)
                except ProcessLookupError:
                    pass
                code = self.proc.wait()
        exit_ms = mono_ms() - t
        time.sleep(0.5)
        ps = subprocess.run(["ps", "-axo", "pid=,ppid=,pgid=,command="], capture_output=True, text=True).stdout
        left = [l.strip()[:200] for l in ps.splitlines() if l.split(None, 3)[2:3] == [str(self.pgid)]]
        self.exit_info = {"mode": mode, "returncode": code, "escalated": escalated,
                          "exit_after_ms": round(exit_ms, 1), "survivors_500ms": left}
        self.event("exit", **self.exit_info)
        self.snap_done.set()
        if left:
            try:
                os.killpg(self.pgid, signal.SIGKILL)
                self.event("survivors-killed", pgid=self.pgid)
            except ProcessLookupError:
                pass
        LIVE_PGIDS.discard(self.pgid)
        return self.exit_info

    # ---------- transport ----------
    def send(self, obj):
        raw = json.dumps(obj, separators=(",", ":"), ensure_ascii=False)
        self._frame("send", raw)
        try:
            self.proc.stdin.write((raw + "\n").encode("utf-8"))
            self.proc.stdin.flush()
            return True
        except (BrokenPipeError, OSError, ValueError) as exc:
            self.event("write-failed", error=repr(exc), frame_id=obj.get("id"))
            return False

    def request(self, method, params, timeout=60.0):
        self.next_id += 1
        rid = self.next_id
        ev = threading.Event()
        with self.cv:
            self.pending[rid] = ev
        self.send({"jsonrpc": "2.0", "id": rid, "method": method, "params": params})
        if not ev.wait(timeout):
            self.event("response-not-observed", method=method, id=rid)
            return None
        return self.results.pop(rid)

    def request_nowait(self, method, params):
        self.next_id += 1
        rid = self.next_id
        ev = threading.Event()
        with self.cv:
            self.pending[rid] = ev
        self.send({"jsonrpc": "2.0", "id": rid, "method": method, "params": params})
        return rid, ev

    def notify(self, method, params=None):
        obj = {"jsonrpc": "2.0", "method": method}
        if params is not None:
            obj["params"] = params
        self.send(obj)

    def answer(self, rid, result=None, error=None, rule="", origin="observation-harness"):
        self.event("answer", id=rid, rule=rule, origin=origin, result=result, error=error)
        if error is not None:
            return self.send({"jsonrpc": "2.0", "id": rid, "error": error})
        return self.send({"jsonrpc": "2.0", "id": rid, "result": result})

    def _reader(self):
        for line in self.proc.stdout:
            raw = line.decode("utf-8", "replace").rstrip("\n")
            self._frame("recv", raw)
            try:
                msg = json.loads(raw)
            except ValueError:
                self.event("malformed-frame", raw=raw[:200])
                continue
            if "id" in msg and ("result" in msg or "error" in msg) and "method" not in msg:
                with self.cv:
                    ev = self.pending.pop(msg["id"], None)
                if ev:
                    self.results[msg["id"]] = msg
                    ev.set()
                else:
                    self.event("unmatched-response", id=msg.get("id"))
            elif "id" in msg and "method" in msg:
                with self.cv:
                    self.server_requests.append((mono_ms(), msg))
                    self.cv.notify_all()
                self.event("server-request", id=msg["id"], method=msg["method"])
                threading.Thread(target=self._on_server_request, args=(msg,), daemon=True).start()
            elif "method" in msg:
                with self.cv:
                    self.notes.append((mono_ms(), msg))
                    self.cv.notify_all()
        self.event("stdout-eof")

    def _stderr_reader(self):
        n = 0
        with open(os.path.join(self.logdir, "codex.stderr"), "ab") as f:
            while True:
                chunk = self.proc.stderr.read1(65536)
                if not chunk:
                    break
                n += len(chunk)
                if n <= 1_000_000:
                    f.write(chunk)
                    f.flush()
        self.event("stderr-eof", bytes=n)

    def _on_server_request(self, msg):
        method = msg["method"]
        if method.startswith("account/") or method == "account/chatgptAuthTokens/refresh":
            self.run.trigger_stop("S-3", "sign-in related server request: %s" % method)
            self.answer(msg["id"], error={"code": -32601, "message": "observation harness: not answered"},
                        rule="S-3: sign-in related request refused")
            return
        kind, payload, rule = self.policy(self, msg)
        if kind == "hold":
            self.event("request-held", id=msg["id"], method=method, rule=rule)
            return
        if kind == "error":
            self.answer(msg["id"], error={"code": -32601, "message": "observation harness: not answered (%s)" % method},
                        rule=rule)
        else:
            self.answer(msg["id"], result=payload, rule=rule)

    # ---------- waiting ----------
    def wait_note(self, pred, timeout, start_index=0):
        """Wait for a notification satisfying pred; returns (index, mono, msg) or None."""
        deadline = time.monotonic() + timeout
        with self.cv:
            while True:
                for i in range(start_index, len(self.notes)):
                    if pred(self.notes[i][1]):
                        return i, self.notes[i][0], self.notes[i][1]
                start_index = len(self.notes)
                rem = deadline - time.monotonic()
                if rem <= 0 or self.run.stop_reason:
                    return None
                self.cv.wait(min(rem, 0.5))

    def wait_request(self, pred, timeout, start_index=0):
        deadline = time.monotonic() + timeout
        with self.cv:
            while True:
                for i in range(start_index, len(self.server_requests)):
                    if pred(self.server_requests[i][1]):
                        return i, self.server_requests[i][0], self.server_requests[i][1]
                start_index = len(self.server_requests)
                rem = deadline - time.monotonic()
                if rem <= 0 or self.run.stop_reason:
                    return None
                self.cv.wait(min(rem, 0.5))

    # ---------- snapshots ----------
    def _snapshot_loop(self):
        path = os.path.join(self.logdir, "snapshots.jsonl")
        with open(path, "a", encoding="utf-8") as out:
            while not self.snap_done.is_set():
                t = wall_ms()
                snap = {}
                try:
                    ps = subprocess.run(["ps", "-axo", "pid=,ppid=,pgid=,command="], capture_output=True, text=True).stdout
                    rows = []
                    cmd_by_pid = {}
                    for line in ps.splitlines():
                        parts = line.split(None, 3)
                        if len(parts) < 4:
                            continue
                        pid, ppid, pgid, cmd = parts
                        if pgid == str(self.pgid) or re.search(r"(^|/)lms( |$)", cmd):
                            rows.append([int(pid), int(ppid), int(pgid), cmd[:300]])
                            cmd_by_pid[pid] = cmd
                    snap["procs"] = rows
                    if self.kill_on_git and any("git" in os.path.basename(r[3].split()[0]) for r in rows
                                                if r[2] == self.pgid):
                        self.event("git-process-in-cold-home: ending process group (guard)")
                        try:
                            os.killpg(self.pgid, signal.SIGKILL)
                        except ProcessLookupError:
                            pass
                    li = subprocess.run(["lsof", "-nP", "-a", "-i", "-g", str(self.pgid)], capture_output=True, text=True).stdout
                    snap["sockets"] = li.splitlines()[1:]
                    lf = subprocess.run(["lsof", "-nP", "-g", str(self.pgid)], capture_output=True, text=True).stdout
                    snap["dotcodex"] = [l for l in lf.splitlines() if (HOME + "/.codex") in l]
                except Exception as exc:  # noqa: BLE001 - recorded
                    snap["error"] = repr(exc)
                    cmd_by_pid = {}
                self.snap_count += 1
                for key, val in snap.items():
                    if self.snap_last.get(key) != val:
                        out.write(json.dumps({"wall_ms": t, "mono_ms": mono_ms(), key: val}, ensure_ascii=False) + "\n")
                        out.flush()
                        self.snap_last[key] = val
                if snap.get("dotcodex"):
                    self.run.trigger_stop("S-6", "%s: process group opened a path under ~/.codex" % self.label)
                for l in snap.get("sockets") or []:
                    cols = l.split()
                    name = " ".join(cols[8:]) if len(cols) > 8 else l
                    raddr, rport = parse_remote(name)
                    if raddr is None or is_loopback(raddr):
                        continue
                    pid = cols[1] if len(cols) > 1 else "?"
                    cmd = cmd_by_pid.get(pid, cols[0] if cols else "?")
                    key = (pid, raddr, rport)
                    if key not in [tuple(x[:3]) for x in self.nonloop]:
                        plugin_repo = "github.com/openai/plugins" in cmd or os.path.basename(cmd.split()[0]).startswith("git")
                        self.nonloop.append([pid, raddr, rport, t, self.run.turn_active, cmd[:160], plugin_repo])
                        self.event("non-loopback-socket", pid=pid, process=cmd[:160], remote=raddr, port=rport,
                                   during_turn=self.run.turn_active, git_process=plugin_repo)
                        if self.run.turn_active and not plugin_repo:
                            self.run.trigger_stop("S-5", "%s: non-loopback connection during a turn: %s %s:%s" %
                                                  (self.label, cmd[:80], raddr, rport))
                time.sleep(self.snap_interval)
        self.event("snapshots", count=self.snap_count, non_loopback=self.nonloop)


# ---------- server-request policies (origin observation-harness) ----------

def policy_hold_approvals(s, msg):
    m = msg["method"]
    if m in ("item/commandExecution/requestApproval", "item/fileChange/requestApproval",
             "item/permissions/requestApproval", "execCommandApproval", "applyPatchApproval",
             "mcpServer/elicitation/request", "item/tool/requestUserInput"):
        return "hold", None, "held unanswered by design (O-2/O-3)"
    return "error", None, "explicit JSON-RPC error"


def policy_refuse(s, msg):
    """Never permits anything: approvals get the refusal form the request offers."""
    m, p = msg["method"], msg.get("params") or {}
    if m == "item/commandExecution/requestApproval":
        avail = p.get("availableDecisions") or []
        d = "decline" if ("decline" in avail or not avail) else "cancel"
        return "result", {"decision": d}, "command approval -> %s (refusal form offered)" % d
    if m == "item/fileChange/requestApproval":
        return "result", {"decision": "decline"}, "file change -> decline"
    if m == "item/permissions/requestApproval":
        return "result", {"permissions": {}, "scope": "turn"}, "permissions -> grant nothing"
    if m == "mcpServer/elicitation/request":
        return "result", {"action": "decline", "content": None, "_meta": None}, "elicitation -> decline"
    if m == "item/tool/requestUserInput":
        return "result", {"answers": {q.get("id"): {"answers": ["Invented example answer: proceed."]}
                                      for q in (p.get("questions") or [])}}, "requestUserInput -> invented answer"
    return "error", None, "explicit JSON-RPC error"


# ---------- helpers ----------

def items_summary(notes, thread_id=None):
    out = []
    for t, msg in notes:
        m = msg.get("method")
        p = msg.get("params") or {}
        if thread_id and p.get("threadId") not in (None, thread_id):
            continue
        if m in ("item/started", "item/completed"):
            it = p.get("item") or {}
            out.append({"t": t, "m": m, "type": it.get("type"), "id": it.get("id"), "status": it.get("status")})
    return out


def method_counts(notes):
    c = {}
    for _, msg in notes:
        c[msg.get("method")] = c.get(msg.get("method"), 0) + 1
    return c


def read_codex_log(home, since_ms=None, pattern=r"https?://|remote control|plugin|featured|ls-remote|models"):
    """Rows of the supplier's own log database in the scratch home matching pattern."""
    path = os.path.join(home, "logs_2.sqlite")
    if not os.path.exists(path):
        return {"error": "no logs_2.sqlite"}
    try:
        con = sqlite3.connect("file:%s?mode=ro" % path, uri=True)
        cols = [r[1] for r in con.execute("PRAGMA table_info(logs)")]
        rows = con.execute("SELECT * FROM logs").fetchall()
        con.close()
    except sqlite3.Error as exc:
        return {"error": repr(exc)}
    rx = re.compile(pattern, re.I)
    hits = []
    for r in rows:
        d = dict(zip(cols, r))
        text = " ".join(str(v) for v in d.values() if isinstance(v, str))
        if rx.search(text):
            hits.append(d)
    return {"columns": cols, "total_rows": len(rows), "hits": hits}


def write_json(path, obj):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=1, default=str)


def thread_start(s, run, dev, approval="on-request", sandbox="read-only", extra=None):
    params = {"cwd": s.cwd, "model": run.a.model, "modelProvider": "obs2_lmstudio",
              "approvalPolicy": approval, "sandbox": sandbox}
    if dev is not None:
        params["developerInstructions"] = dev
    if extra:
        params.update(extra)
    r = s.request("thread/start", params, timeout=120)
    if r is None or "result" not in r:
        run.trigger_stop("thread-start-failed", "%s: %r" % (s.label, (r or {}).get("error")))
        return None
    res = r["result"]
    if res.get("model") != run.a.model or res.get("modelProvider") != "obs2_lmstudio":
        run.trigger_stop("S-3", "%s: thread start reports model %r provider %r" % (s.label, res.get("model"), res.get("modelProvider")))
        return None
    for src in res.get("instructionSources") or []:
        pth = src if isinstance(src, str) else (src.get("path") if isinstance(src, dict) else None)
        if pth and not os.path.realpath(pth).startswith(run.obs_real):
            run.trigger_stop("S-4", "%s: instructionSources outside OBS: %r" % (s.label, pth))
            return None
    s.event("thread/start", thread=res.get("thread", {}).get("id"), approvalPolicy=res.get("approvalPolicy"),
            instructionSources=res.get("instructionSources"))
    return res


def turn_start(s, run, thread_id, text):
    run.turn_active = True
    r = s.request("turn/start", {"threadId": thread_id, "input": [{"type": "text", "text": text, "text_elements": []}]},
                  timeout=60)
    if r is None or "result" not in r:
        run.turn_active = False
        run.trigger_stop("S-11", "%s: turn/start failed: %r" % (s.label, r))
        return None
    tid = ((r["result"] or {}).get("turn") or {}).get("id")
    s.event("turn/start", turn=tid)
    return tid


def wait_turn_completed(s, run, turn_id, timeout=600, start_index=0):
    got = s.wait_note(lambda m: m.get("method") == "turn/completed" and
                      ((m.get("params") or {}).get("turn") or {}).get("id") == turn_id, timeout, start_index)
    if got is None and not run.stop_reason:
        run.trigger_stop("S-7", "%s: no turn/completed within %ss" % (s.label, timeout))
    run.turn_active = False
    return got


# ---------- scenarios ----------

def sc_probe(run):
    home = run.make_home("probe", provider_config(run.a.model, run.a.ctx))
    s = Session(run, "probe", home, run.make_cwd("probe"))
    s.start()
    out = {}
    try:
        init = s.initialize(experimental=True)
        if init is None:
            return
        out["initialize"] = init
        time.sleep(2)
        feats, cursor = [], None
        for _ in range(20):
            r = s.request("experimentalFeature/list", {"cursor": cursor, "limit": 200})
            if not r or "result" not in r:
                out["experimentalFeature/list error"] = r
                break
            feats += r["result"]["data"]
            cursor = r["result"].get("nextCursor")
            if not cursor:
                break
        out["features"] = feats
        out["config/read"] = s.request("config/read", {"includeLayers": True, "cwd": s.cwd})
        out["account/read"] = s.request("account/read", {"refreshToken": False})
        out["remoteControl/status/read"] = s.request("remoteControl/status/read", {})
        out["collaborationMode/list"] = s.request("collaborationMode/list", {})
        out["notes"] = [m for _, m in s.notes]
    finally:
        s.stop("stdin")
        write_json(os.path.join(s.logdir, "probe_result.json"), out)


RC_ENV = {"CODEX_INTERNAL_APP_SERVER_REMOTE_CONTROL_DISABLED": "1"}
ALL_OFF = "[features]\nplugins = false\nremote_plugin = false\napps = false\ntool_suggest = false\n"
O7_VARIANTS = [
    # (label, extra config text (appended after the provider tables), extra argv, extra env)
    ("v0-baseline", "", [], {}),
    ("v1-features-plugins-off", "[features]\nplugins = false\n", [], {}),
    ("v2-features-remote_plugin-off", "[features]\nremote_plugin = false\n", [], {}),
    ("v3-features-apps-off", "[features]\napps = false\n", [], {}),
    ("v4-env-remote-control-disabled", "", [], RC_ENV),
    ("v5-features-remote_control-off", "[features]\nremote_control = false\n", [], {}),
    ("v6-all-features-off", ALL_OFF, [], {}),
    ("v7-all-features-off-plus-env", ALL_OFF, [], RC_ENV),
    # A cold home (no plugin cache) with plugins off: does the setting also stop the repository fetch that a
    # fresh home causes (S-F-10)? Guard: any `git` process in the group ends the process group at once.
    ("v8-cold-home-plugins-off", "[features]\nplugins = false\n", [], {}),
]


def sc_o7(run):
    only = set(run.a.variants.split(",")) if run.a.variants else None
    summary = {}
    for label, extra_cfg, argv, env in O7_VARIANTS:
        if only and label not in only:
            continue
        if run.stop_reason:
            break
        # The features table must come after top-level keys; provider_config puts tables last, so the
        # variant's table is appended at the end.
        cfg = provider_config(run.a.model, run.a.ctx) + "\n" + extra_cfg
        cold = "cold-home" in label
        home = run.make_home("o7-" + label, cfg, warm=not cold)
        s = Session(run, "o7-" + label, home, run.make_cwd("o7"), argv_extra=argv, env_extra=env, snap_interval=0.1)
        s.kill_on_git = cold
        t_spawn = wall_ms()
        s.start()
        res = {"config_extra": extra_cfg, "env": env}
        try:
            init = s.initialize(experimental=False)
            res["initialize_ok"] = init is not None
            time.sleep(run.a.idle)
            r = s.request("remoteControl/status/read", {})
            res["remoteControl/status/read"] = r
            res["notes"] = [m for _, m in s.notes]
        finally:
            res["exit"] = s.stop("stdin")
        res["non_loopback"] = s.nonloop
        res["spawn_wall_ms"] = t_spawn
        res["git_processes"] = sorted({r[3] for r in (s.snap_last.get("procs") or []) if "git" in r[3]})
        res["codex_log"] = read_codex_log(home)
        res["home_listing"] = sorted(os.path.relpath(os.path.join(dp, f), home)
                                     for dp, dn, fn in os.walk(home) if ".tmp/plugins/" not in dp + "/" for f in fn)[:200]
        write_json(os.path.join(s.logdir, "o7_result.json"), res)
        summary[label] = {"non_loopback": [[x[1], x[2], x[5], x[6]] for x in s.nonloop],
                          "remote_control_notes": [m.get("params") for m in res["notes"]
                                                   if m.get("method") == "remoteControl/status/changed"]}
    write_json(os.path.join(run.logroot, "o7_summary.json"), summary)


def sc_o6(run):
    """K-1: share home A's configuration with home B (own empty authentication); config/read and account/read only."""
    shared_cfg = (
        "model = \"obs2-shared-example-model\"\n"
        "model_provider = \"obs2_shared_example\"\n"
        "approval_policy = \"on-request\"\n"
        "sandbox_mode = \"read-only\"\n"
        "web_search = \"disabled\"\n\n"
        "[analytics]\nenabled = false\n\n"
        "[model_providers.obs2_shared_example]\n"
        "name = \"Invented shared provider (OBS-2)\"\n"
        "base_url = \"http://127.0.0.1:1234/v1\"\n"
        "wire_api = \"responses\"\n\n"
        "[mcp_servers.obs2_shared_example_tool]\n"
        "command = \"/usr/bin/true\"\n"
        "enabled = false\n")
    home_a = run.make_home("o6-A-shared", shared_cfg)
    profile_text = "model = \"obs2-profile-example-model\"\n"
    with open(os.path.join(home_a, "obs2example.config.toml"), "w", encoding="utf-8") as f:
        f.write(profile_text)
    a_cfg = os.path.join(home_a, "config.toml")

    def sha(p):
        import hashlib
        try:
            with open(p, "rb") as f:
                return hashlib.sha256(f.read()).hexdigest()
        except OSError:
            return None
    before = sha(a_cfg)
    cases = []
    # M0: B alone (control).
    cases.append(("M0-B-alone", run.make_home("o6-B-M0"), [], {}))
    # M1: B's config.toml is a symbolic link to A's.
    b1 = run.make_home("o6-B-M1")
    os.symlink(a_cfg, os.path.join(b1, "config.toml"))
    cases.append(("M1-symlinked-config", b1, [], {}))
    # M2: B started with -c overrides carrying A's values (dotted keys, TOML values).
    b2 = run.make_home("o6-B-M2")
    overrides = ["-c", "model=\"obs2-shared-example-model\"",
                 "-c", "model_provider=\"obs2_shared_example\"",
                 "-c", "model_providers.obs2_shared_example={name=\"Invented shared provider (OBS-2)\",base_url=\"http://127.0.0.1:1234/v1\",wire_api=\"responses\"}",
                 "-c", "mcp_servers.obs2_shared_example_tool={command=\"/usr/bin/true\",enabled=false}",
                 "-c", "analytics.enabled=false"]
    cases.append(("M2-cli-overrides", b2, overrides, {}))
    # M3: profile-v2 file of A (`<name>.config.toml`) - can a home-B process select a profile file that lives in A?
    b3 = run.make_home("o6-B-M3")
    os.symlink(os.path.join(home_a, "obs2example.config.toml"), os.path.join(b3, "obs2example.config.toml"))
    cases.append(("M3-profile-v2-flag", b3, ["--profile", "obs2example"], {}))
    # M4: CODEX_HOME=A itself with the in-memory credential store (`cli_auth_credentials_store = "ephemeral"`)
    #     given as a launch override: the shared home with authentication kept out of it.
    cases.append(("M4-shared-home-ephemeral-auth", home_a, ["-c", "cli_auth_credentials_store=\"ephemeral\""], {}))
    # M5: the same with the keyring store (no credential exists anywhere; observed by account/read only).
    cases.append(("M5-shared-home-keyring-auth", home_a, ["-c", "cli_auth_credentials_store=\"keyring\""], {}))
    results = {"A_config_sha256_before": before}
    only = set(run.a.variants.split(",")) if run.a.variants else None
    for label, home, argv, env in cases:
        if only and label not in only:
            continue
        if run.stop_reason:
            break
        s = Session(run, "o6-" + label, home, run.make_cwd("o6"), argv_extra=argv, env_extra=env)
        s.start()
        res = {"argv_extra": [x.replace(run.obs, "<OBS>") for x in argv]}
        try:
            init = s.initialize(experimental=True)
            res["initialize"] = init
            if init is not None:
                time.sleep(1.0)
                res["config/read"] = s.request("config/read", {"includeLayers": True, "cwd": s.cwd})
                res["account/read"] = s.request("account/read", {"refreshToken": False})
        finally:
            res["exit"] = s.stop("stdin")
        try:
            with open(os.path.join(s.logdir, "codex.stderr"), "r", encoding="utf-8", errors="replace") as f:
                res["stderr"] = f.read()[:2000]
        except OSError:
            pass
        res["home_files_top"] = sorted(os.listdir(home))
        res["auth_files"] = [f for f in os.listdir(home) if "auth" in f.lower()]
        res["non_loopback"] = s.nonloop
        results[label] = res
        if run.stop_reason and run.stop_reason[0] == "S-11":
            # A launch refused by the supplier is this case's result, not a stop of the whole scenario.
            res["refused_at_launch"] = run.stop_reason[1]
            run.event("o6-case-refused (recorded; scenario continues)", case=label)
            run.stop_reason = None
    results["A_config_sha256_after"] = sha(a_cfg)
    write_json(os.path.join(run.logroot, "o6_result%s.json" % ("_" + run.a.variants.replace(",", "+") if only else "")), results)


INTERRUPT_DEV = ("You are running an observation test with invented data. Follow the user's request exactly.")
LONG_PROMPT = ("This is a test with invented data. Write the numbers from one to three hundred in words, "
               "one per line, with no other text.")


def sc_o1(run):
    home = run.make_home("o1", provider_config(run.a.model, run.a.ctx))
    s = Session(run, "o1", home, run.make_cwd("o1"), policy=policy_refuse)
    s.start()
    out = {}
    try:
        if s.initialize() is None:
            return
        time.sleep(2)
        th = thread_start(s, run, INTERRUPT_DEV)
        if th is None:
            return
        thread_id = th["thread"]["id"]
        turn_id = turn_start(s, run, thread_id, LONG_PROMPT)
        if turn_id is None:
            return
        # Wait for the model to be generating (first delta of any kind), then let it run a few seconds.
        wanted = (("item/agentMessage/delta",) if run.a.interrupt_on == "agentMessage"
                  else ("item/agentMessage/delta", "item/reasoning/textDelta"))
        got = s.wait_note(lambda m: m.get("method") in wanted, run.a.turn_timeout)
        if got is None:
            out["no-delta"] = True
            return
        out["first_delta_mono"] = got[1]
        time.sleep(run.a.interrupt_after)
        idx_before = len(s.notes)
        t_send = mono_ms()
        r = s.request("turn/interrupt", {"threadId": thread_id, "turnId": turn_id}, timeout=60)
        t_resp = mono_ms()
        out["interrupt_sent_mono"] = t_send
        out["interrupt_response"] = r
        out["interrupt_response_mono"] = t_resp
        done = wait_turn_completed(s, run, turn_id, timeout=120, start_index=0)
        out["turn_completed"] = done[2] if done else None
        out["turn_completed_mono"] = done[1] if done else None
        time.sleep(3)
        out["notes_after_interrupt"] = [(t, m) for t, m in s.notes[idx_before:]
                                        if m.get("method") not in ("item/agentMessage/delta", "item/reasoning/textDelta")]
        out["deltas_after_interrupt"] = sum(1 for t, m in s.notes[idx_before:]
                                            if m.get("method") in ("item/agentMessage/delta", "item/reasoning/textDelta"))
        out["thread/read"] = s.request("thread/read", {"threadId": thread_id, "includeTurns": True})
        out["thread/turns/list"] = s.request("thread/turns/list", {"threadId": thread_id})
        out["items"] = items_summary(s.notes, thread_id)
        out["method_counts"] = method_counts(s.notes)
    finally:
        run.turn_active = False
        out["exit"] = s.stop("stdin")
        write_json(os.path.join(s.logdir, "o1_result.json"), out)


CMD_DEV = ("You are running an observation test with invented data. When asked, run the command you are given. "
           "Keep replies to one sentence.")


def named_command(run):
    return "python3 %s --key EX-2" % os.path.join(run.obs, "tool", "obs2_cli_tool.py")


def sc_o3(run):
    home = run.make_home("o3", provider_config(run.a.model, run.a.ctx))
    s = Session(run, "o3", home, run.make_cwd("o3"), policy=policy_hold_approvals)
    s.start()
    out = {}
    try:
        if s.initialize() is None:
            return
        time.sleep(2)
        th = thread_start(s, run, CMD_DEV, approval="untrusted")
        if th is None:
            return
        out["thread_approvalPolicy"] = th.get("approvalPolicy")
        if th.get("approvalPolicy") != "untrusted":
            run.trigger_stop("approval-policy-not-untrusted", repr(th.get("approvalPolicy")))
            return
        thread_id = th["thread"]["id"]
        prompt = "This is a test with invented data. Run `%s` and report the outcome in one sentence." % named_command(run)
        turn_id = turn_start(s, run, thread_id, prompt)
        if turn_id is None:
            return
        got = s.wait_request(lambda m: m.get("method", "").endswith("requestApproval"), run.a.turn_timeout)
        if got is None:
            out["no-request"] = True
            done = wait_turn_completed(s, run, turn_id, timeout=60)
            out["turn_completed"] = done[2] if done else None
            return
        req = got[2]
        out["request"] = req
        out["request_mono"] = got[1]
        time.sleep(run.a.hold_before_interrupt)
        resolved_before = [m for _, m in s.notes if m.get("method") == "serverRequest/resolved"]
        out["resolved_before_interrupt"] = resolved_before
        idx = len(s.notes)
        t_send = mono_ms()
        r = s.request("turn/interrupt", {"threadId": thread_id, "turnId": turn_id}, timeout=60)
        out["interrupt_sent_mono"] = t_send
        out["interrupt_response"] = r
        done = wait_turn_completed(s, run, turn_id, timeout=120, start_index=0)
        out["turn_completed"] = done[2] if done else None
        time.sleep(3)
        out["notes_after_interrupt"] = [(t, m) for t, m in s.notes[idx:]
                                        if m.get("method") not in ("item/agentMessage/delta", "item/reasoning/textDelta")]
        # A late answer from the harness to the already-settled request: cancel (never accept).
        late_idx = len(s.notes)
        out["late_answer_sent"] = s.answer(req["id"], result={"decision": "cancel"},
                                           rule="late answer after supplier resolution (O-3): cancel")
        time.sleep(4)
        out["notes_after_late_answer"] = [(t, m) for t, m in s.notes[late_idx:]]
        out["thread/read"] = s.request("thread/read", {"threadId": thread_id, "includeTurns": True})
        out["items"] = items_summary(s.notes, thread_id)
        out["method_counts"] = method_counts(s.notes)
        out["server_requests"] = [(t, m) for t, m in s.server_requests]
    finally:
        run.turn_active = False
        out["exit"] = s.stop("stdin")
        write_json(os.path.join(s.logdir, "o3_result.json"), out)


def sc_o2(run):
    home = run.make_home("o2", provider_config(run.a.model, run.a.ctx))
    cwd = run.make_cwd("o2")
    s1 = Session(run, "o2-first", home, cwd, policy=policy_hold_approvals)
    s1.start()
    out = {}
    thread_id = turn_id = None
    try:
        if s1.initialize() is None:
            return
        time.sleep(2)
        th = thread_start(s1, run, CMD_DEV, approval="untrusted")
        if th is None:
            return
        if th.get("approvalPolicy") != "untrusted":
            run.trigger_stop("approval-policy-not-untrusted", repr(th.get("approvalPolicy")))
            return
        thread_id = th["thread"]["id"]
        prompt = "This is a test with invented data. Run `%s` and report the outcome in one sentence." % named_command(run)
        turn_id = turn_start(s1, run, thread_id, prompt)
        if turn_id is None:
            return
        got = s1.wait_request(lambda m: m.get("method", "").endswith("requestApproval"), run.a.turn_timeout)
        if got is None:
            out["no-request"] = True
            return
        out["request"] = got[2]
        time.sleep(3)
        out["first_items"] = items_summary(s1.notes, thread_id)
    finally:
        run.turn_active = False
        out["first_exit"] = s1.stop(run.a.stop_mode, wait=5.0)
    if thread_id is None or out.get("no-request") or run.stop_reason:
        write_json(os.path.join(run.logroot, "o2_result.json"), out)
        return
    out["home_after_stop"] = sorted(os.path.relpath(os.path.join(dp, f), home)
                                    for dp, dn, fn in os.walk(home) if ".tmp" not in dp for f in fn)
    time.sleep(2)
    s2 = Session(run, "o2-second", home, cwd, policy=policy_refuse)
    s2.start()
    try:
        if s2.initialize() is None:
            return
        time.sleep(2)
        out["thread/read before resume"] = s2.request("thread/read", {"threadId": thread_id, "includeTurns": True})
        idx = len(s2.notes)
        r = s2.request("thread/resume", {"threadId": thread_id}, timeout=120)
        out["thread/resume"] = r
        time.sleep(run.a.after_resume)
        out["server_requests_after_resume"] = [(t, m) for t, m in s2.server_requests]
        out["notes_after_resume"] = [(t, m) for t, m in s2.notes[idx:]
                                     if m.get("method") not in ("item/agentMessage/delta", "item/reasoning/textDelta")]
        out["thread/read after resume"] = s2.request("thread/read", {"threadId": thread_id, "includeTurns": True})
        out["thread/turns/list"] = s2.request("thread/turns/list", {"threadId": thread_id})
        out["thread/loaded/list"] = s2.request("thread/loaded/list", {})
    finally:
        run.turn_active = False
        out["second_exit"] = s2.stop("stdin")
        write_json(os.path.join(run.logroot, "o2_result.json"), out)


def sc_o5(run):
    home = run.make_home("o5", provider_config(run.a.model, run.a.ctx))
    cwd = run.make_cwd("o5")
    dev_a = ("You are running an observation test with invented data. Marker ALPHA-7: end every reply with the "
             "word ALPHA.")
    dev_b = ("You are running an observation test with invented data. Marker BRAVO-7: end every reply with the "
             "word BRAVO.")
    dev_c = ("You are running an observation test with invented data. Marker CHARLIE-7: end every reply with the "
             "word CHARLIE.")
    ask = "This is a test with invented data. Reply with one short sentence saying hello, following your instructions."
    out = {"dev": {"A": dev_a, "B": dev_b, "C": dev_c}}
    s1 = Session(run, "o5-first", home, cwd, policy=policy_refuse)
    s1.start()
    thread_id = None
    try:
        if s1.initialize() is None:
            return
        time.sleep(2)
        th = thread_start(s1, run, dev_a)
        if th is None:
            return
        thread_id = th["thread"]["id"]
        t1 = turn_start(s1, run, thread_id, ask)
        d1 = wait_turn_completed(s1, run, t1, timeout=run.a.turn_timeout)
        out["turn1"] = d1[2] if d1 else None
        if run.stop_reason:
            return
        # (a) resume on the loaded thread, same process, with B.
        r = s1.request("thread/resume", {"threadId": thread_id, "developerInstructions": dev_b}, timeout=120)
        out["resume_loaded"] = r
        idx = len(s1.notes)
        t2 = turn_start(s1, run, thread_id, ask)
        d2 = wait_turn_completed(s1, run, t2, timeout=run.a.turn_timeout, start_index=idx)
        out["turn2"] = d2[2] if d2 else None
        out["turn2_agent_messages"] = [m["params"]["item"].get("text") for _, m in s1.notes[idx:]
                                       if m.get("method") == "item/completed" and
                                       (m["params"].get("item") or {}).get("type") == "agentMessage"]
    finally:
        run.turn_active = False
        out["first_exit"] = s1.stop("stdin")
    if thread_id is None or run.stop_reason:
        write_json(os.path.join(run.logroot, "o5_result.json"), out)
        return
    time.sleep(2)
    # (b) a new process loads the thread by resume, with C.
    s2 = Session(run, "o5-second", home, cwd, policy=policy_refuse)
    s2.start()
    try:
        if s2.initialize() is None:
            return
        time.sleep(2)
        r = s2.request("thread/resume", {"threadId": thread_id, "developerInstructions": dev_c}, timeout=120)
        out["resume_unloaded"] = r
        idx = len(s2.notes)
        t3 = turn_start(s2, run, thread_id, ask)
        d3 = wait_turn_completed(s2, run, t3, timeout=run.a.turn_timeout, start_index=idx)
        out["turn3"] = d3[2] if d3 else None
        out["turn3_agent_messages"] = [m["params"]["item"].get("text") for _, m in s2.notes[idx:]
                                       if m.get("method") == "item/completed" and
                                       (m["params"].get("item") or {}).get("type") == "agentMessage"]
        out["thread/read"] = s2.request("thread/read", {"threadId": thread_id, "includeTurns": False})
    finally:
        run.turn_active = False
        out["second_exit"] = s2.stop("stdin")
        write_json(os.path.join(run.logroot, "o5_result.json"), out)


ROLE_LINE = "Invented role line: you are the OBS2 TASK ROLE. Begin every reply with the word TASKROLE."


def _collect_children(notes, parent_ids):
    child_ids = set()
    for _, m in notes:
        p = m.get("params") or {}
        it = p.get("item") or {}
        if it.get("type") == "collabAgentToolCall":
            child_ids.update(it.get("receiverThreadIds") or [])
        if p.get("threadId") and p.get("threadId") not in parent_ids:
            child_ids.add(p["threadId"])
        th2 = p.get("thread") or {}
        if th2.get("parentThreadId"):
            child_ids.add(th2.get("id"))
    return sorted(c for c in child_ids if c)


def _o4_turn(run, s, out, key, dev, prompt):
    th = thread_start(s, run, dev)
    if th is None:
        return None
    tid_thread = th["thread"]["id"]
    out[key + "_thread"] = tid_thread
    idx = len(s.notes)
    turn_id = turn_start(s, run, tid_thread, prompt)
    if turn_id is None:
        return None
    done = wait_turn_completed(s, run, turn_id, timeout=run.a.turn_timeout, start_index=idx)
    out[key + "_turn_completed"] = done[2] if done else None
    time.sleep(run.a.after_resume)  # let child turns finish and report
    seg = s.notes[idx:]
    out[key + "_collab_items"] = [m for _, m in seg if ((m.get("params") or {}).get("item") or {}).get("type")
                                  == "collabAgentToolCall"]
    out[key + "_methods"] = method_counts(seg)
    out[key + "_thread_ids_in_notes"] = sorted({(m.get("params") or {}).get("threadId") for _, m in seg
                                                if (m.get("params") or {}).get("threadId")})
    out[key + "_thread_started"] = [m for _, m in seg if m.get("method") == "thread/started"]
    out[key + "_items"] = items_summary(seg)
    kids = _collect_children(seg, {tid_thread})
    out[key + "_children"] = kids
    out[key + "_children_read"] = {c: s.request("thread/read", {"threadId": c, "includeTurns": True}) for c in kids}
    out[key + "_children_turns_list"] = {c: s.request("thread/turns/list", {"threadId": c}) for c in kids}
    out[key + "_agent_messages"] = [((m.get("params") or {}).get("threadId"), m["params"]["item"].get("text"))
                                    for _, m in seg if m.get("method") == "item/completed" and
                                    (m["params"].get("item") or {}).get("type") == "agentMessage"]
    return tid_thread


def sc_o4(run):
    """O-4 (delegation, experimentalApi), O-4a (native child role), O-4b (task guidance against delegation)."""
    parts = set(run.a.variants.split(",")) if run.a.variants else {"o4a", "o4b"}
    home = run.make_home("o4" + ("-" + "+".join(sorted(parts))), None)
    role_file = os.path.join(home, "agents", "obs2_task.toml")
    os.makedirs(os.path.dirname(role_file))
    with open(role_file, "w", encoding="utf-8") as f:
        f.write("developer_instructions = \"%s\"\n" % ROLE_LINE)
    extra = ("[agents.obs2_task]\n"
             "description = \"Invented task role for OBS-2: answers one short question.\"\n"
             "config_file = \"%s\"\n" % role_file)
    with open(os.path.join(home, "config.toml"), "w", encoding="utf-8") as f:
        f.write(provider_config(run.a.model, run.a.ctx) + "\n" + (run.a.o4_config.replace("\\n", "\n") or "") + extra)
    s = Session(run, "o4-" + "+".join(sorted(parts)), home, run.make_cwd("o4"), policy=policy_refuse)
    s.start()
    out = {"config_extra": extra.replace(run.obs, "<OBS>"), "role_file_text": ROLE_LINE}
    try:
        if s.initialize(experimental=True) is None:
            return
        time.sleep(2)
        if "o4a" in parts and not run.stop_reason:
            dev = ("You are running an observation test with invented data. The user explicitly authorizes "
                   "sub-agents for this test. Keep replies to one sentence.")
            prompt = ("This is a test with invented data. I explicitly ask you to delegate: call spawn_agent once "
                      "with agent_type \"obs2_task\" and message \"Reply with one short sentence about the "
                      "invented key EX-4.\" Then call wait_agent for it and report its reply in one sentence.")
            _o4_turn(run, s, out, "o4a", dev, prompt)
        if "o4b" in parts and not run.stop_reason:
            dev = ("You are a TASK agent; you do not delegate. You are running an observation test with "
                   "invented data. Keep replies to one sentence.")
            prompt = ("This is a test with invented data. Please delegate this to a helper agent: spawn a "
                      "sub-agent and ask it to reply with the word READY, then tell me what it said.")
            _o4_turn(run, s, out, "o4b", dev, prompt)
        out["thread/list"] = s.request("thread/list", {})
        out["thread/loaded/list"] = s.request("thread/loaded/list", {})
        out["server_requests"] = [(t, m) for t, m in s.server_requests]
    finally:
        run.turn_active = False
        out["exit"] = s.stop("stdin")
        write_json(os.path.join(s.logdir, "o4_result.json"), out)


def sc_o8(run):
    """O-8 plan mode (collaborationMode on turn/start, experimental) and O-5b per-turn developer instructions
    carried by collaborationMode.settings.developer_instructions."""
    home = run.make_home("o8", provider_config(run.a.model, run.a.ctx))
    s = Session(run, "o8", home, run.make_cwd("o8"), policy=policy_refuse)
    s.start()
    dev = ("You are running an observation test with invented data. Invented role line: you are the OBS2 "
           "PLANNER ROLE. End every reply with the word ROLEMARK.")
    out = {"dev": dev}
    try:
        if s.initialize(experimental=True) is None:
            return
        time.sleep(2)
        out["collaborationMode/list"] = s.request("collaborationMode/list", {})
        th = thread_start(s, run, dev)
        if th is None:
            return
        tid = th["thread"]["id"]
        out["thread_start_collaborationMode"] = th.get("collaborationMode")
        turns = [
            ("plan", "This is a test with invented data. Make a three-step plan for sorting an invented list of "
                     "five fruit names alphabetically. Do not carry it out.",
             {"mode": "plan", "settings": {"model": run.a.model, "reasoning_effort": None,
                                           "developer_instructions": None}}),
            ("after-plan-no-mode", "This is a test with invented data. Reply with one short sentence saying "
                                   "which mode you are in.", None),
            ("o5b-default-with-dev", "This is a test with invented data. Reply with one short sentence saying "
                                     "hello, following your instructions.",
             {"mode": "default", "settings": {"model": run.a.model, "reasoning_effort": None,
                                              "developer_instructions": "You are running an observation test "
                                              "with invented data. Marker DELTA-7: end every reply with the word "
                                              "DELTA."}}),
        ]
        for key, text, cm in turns:
            if run.stop_reason:
                break
            idx = len(s.notes)
            params = {"threadId": tid, "input": [{"type": "text", "text": text, "text_elements": []}]}
            if cm is not None:
                params["collaborationMode"] = cm
            run.turn_active = True
            r = s.request("turn/start", params, timeout=60)
            if r is None or "result" not in r:
                out[key + "_turn_start"] = r
                run.turn_active = False
                continue
            turn_id = r["result"]["turn"]["id"]
            done = wait_turn_completed(s, run, turn_id, timeout=run.a.turn_timeout, start_index=idx)
            seg = s.notes[idx:]
            out[key] = {
                "turn_start_params_collaborationMode": cm,
                "turn_completed": done[2] if done else None,
                "methods": method_counts(seg),
                "items": items_summary(seg),
                "plan_notes": [m for _, m in seg if m.get("method") in ("turn/plan/updated", "item/plan/delta")],
                "plan_items": [m for _, m in seg if m.get("method") == "item/completed" and
                               (m["params"].get("item") or {}).get("type") == "plan"],
                "agent_messages": [m["params"]["item"].get("text") for _, m in seg if m.get("method") ==
                                   "item/completed" and (m["params"].get("item") or {}).get("type") == "agentMessage"],
                "settings_notes": [m for _, m in seg if m.get("method") == "thread/settings/updated"],
            }
        out["thread/read"] = s.request("thread/read", {"threadId": tid, "includeTurns": False})
    finally:
        run.turn_active = False
        out["exit"] = s.stop("stdin")
        write_json(os.path.join(s.logdir, "o8_result.json"), out)


TOOL_VARIANTS = [
    ("t0-default", ""),
    ("t1-multi_agent_v2", "[features.multi_agent_v2]\nenabled = true\n"),
    ("t2-multi_agent_v2-empty-namespace", "[features.multi_agent_v2]\nenabled = true\ntool_namespace = \"\"\n"),
    ("t3-agent-role", "[agents.obs2_task]\ndescription = \"Invented task role for OBS-2: answers one short question.\"\n"),
    ("t4-multi_agent-off", "[features]\nmulti_agent = false\n"),
]


def sc_tools(run):
    """What tool list Codex sends to a Responses provider per configuration (capture-only tap; no model call)."""
    only = set(run.a.variants.split(",")) if run.a.variants else None
    out = {}
    for label, extra in TOOL_VARIANTS:
        if only and label not in only:
            continue
        if run.stop_reason:
            break
        cfg = provider_config(run.a.model, run.a.ctx) + "\n" + extra
        home = run.make_home("tools-" + label, cfg)
        s = Session(run, "tools-" + label, home, run.make_cwd("tools"), policy=policy_refuse)
        s.start()
        res = {"config_extra": extra}
        try:
            if s.initialize(experimental=True) is None:
                res["init_failed"] = True
                try:
                    with open(os.path.join(s.logdir, "codex.stderr"), encoding="utf-8", errors="replace") as f:
                        res["stderr"] = f.read()[:2000]
                except OSError:
                    pass
                run.stop_reason = None
                continue
            th = thread_start(s, run, "Invented developer text for a tool-list capture.")
            if th is None:
                res["thread_start_failed"] = run.stop_reason
                run.stop_reason = None
                continue
            tid = turn_start(s, run, th["thread"]["id"], "Invented prompt for a tool-list capture.")
            run.turn_active = False  # capture-only tap: no model traffic
            if tid:
                got = s.wait_note(lambda m: m.get("method") == "turn/completed", 90)
                res["turn_completed"] = got[2] if got else None
            res["warnings"] = [m for _, m in s.notes if m.get("method") in ("warning", "configWarning", "error")]
        finally:
            res["exit"] = s.stop("stdin")
            out[label] = res
    write_json(os.path.join(run.logroot, "tools_result%s.json" % run.a.suffix), out)


SCENARIOS = {"tools": sc_tools, "o8": sc_o8, "probe": sc_probe, "o7": sc_o7, "o6": sc_o6, "o1": sc_o1, "o3": sc_o3, "o2": sc_o2,
             "o5": sc_o5, "o4": sc_o4}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--obs", required=True)
    ap.add_argument("--binary", required=True)
    ap.add_argument("--model", default="qwen/qwen3.5-9b")
    ap.add_argument("--ctx", type=int, default=24576)
    ap.add_argument("--idle", type=float, default=20.0, help="o7: seconds idle after initialized")
    ap.add_argument("--variants", default="", help="o7: comma-separated variant labels")
    ap.add_argument("--turn-timeout", type=float, default=600.0)
    ap.add_argument("--interrupt-after", type=float, default=4.0)
    ap.add_argument("--hold-before-interrupt", type=float, default=5.0)
    ap.add_argument("--after-resume", type=float, default=15.0)
    ap.add_argument("--stop-mode", default="stdin", choices=["stdin", "term", "kill"])
    ap.add_argument("--o4-config", default="")
    ap.add_argument("--suffix", default="", help="appended to every scratch home name (reruns)")
    ap.add_argument("--provider-port", type=int, default=1234,
                    help="loopback port of the provider base_url (12340 = obs2_provider_tap.py in front of LM Studio)")
    ap.add_argument("--interrupt-on", default="any", choices=["any", "agentMessage"],
                    help="o1: which first delta starts the interrupt delay")
    ap.add_argument("scenario", choices=sorted(SCENARIOS))
    a = ap.parse_args()
    global LMS_BASE
    LMS_BASE = "http://127.0.0.1:%d/v1" % a.provider_port
    run = Run(a)
    run.event("begin", scenario=a.scenario, pin="0.158.0", model=a.model, ctx=a.ctx, provider_base=LMS_BASE,
              suffix=a.suffix)
    threading.Thread(target=run.global_watch, daemon=True).start()
    try:
        SCENARIOS[a.scenario](run)
    finally:
        for pg in list(LIVE_PGIDS):
            try:
                os.killpg(pg, signal.SIGKILL)
                run.event("cleanup-killed", pgid=pg)
            except ProcessLookupError:
                pass
        run.watch_done.set()
        run.event("end", scenario=a.scenario, stop=run.stop_reason)
    print(json.dumps({"scenario": a.scenario, "stop": run.stop_reason}))


if __name__ == "__main__":
    main()
