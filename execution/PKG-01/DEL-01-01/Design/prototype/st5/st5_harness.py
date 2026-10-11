#!/usr/bin/env python3
"""ST-5 / U-SQ-6 capture harness: an answer written to a Codex server request, the Codex process ended
before any acknowledgment arrives (HOSTING §9.4 X-09 form), then the X-10 restart and recovery read.

Prototype only (DEL-01-01 HOSTING §9.1 capture method; DEL-01-02 RECOVERY RQ-05; DEL-09-02 U-SQ-6).
Not product code and not an App candidate: this script stands in for the App side of the stdio boundary
and records it. Python 3 standard library only. No download, no sign-in, no credential, never `~/.codex`:
every Codex home and workspace is made with `tempfile.mkdtemp`. The model provider is
`stub_provider.py` on 127.0.0.1 (invented content); plugins and analytics are off in the scratch
`config.toml`. Any non-loopback socket of the Codex process group stops the run.

Scenarios
  st5     generation 1: initialize, thread/start, turn/start; the stub asks for one shell command; Codex
          raises item/commandExecution/requestApproval; the harness freezes the Codex process group
          (SIGSTOP), writes the answer {"decision":"accept"} to Codex's stdin, then ends the group
          (SIGKILL) while it is still frozen, so Codex cannot have read the answer or sent an
          acknowledgment; a client request (thread/turns/list) is written in the same frozen window and
          is left un-responded (X-09). Generation 2 (X-10): same home, initialize, thread/read with turns,
          thread/turns/list, thread/resume, a short wait for any re-raised request, graceful stop.
  st5-race  as st5 but without the freeze: write the answer and SIGKILL immediately (a natural race;
          whether serverRequest/resolved precedes the kill is what it observes).
  nv04    a primary turn whose model output spawns one sub-agent through Codex's own collaboration tool,
          the child's model response is held open by the stub, and the parent's turn ends first.

Usage: st5_harness.py --binary PATH --codex-path DIR --out DIR SCENARIO
The output directory receives the raw (unredacted, local-only) frames and the redacted recording
`<scenario>.recording.json`; only the redacted recording is meant to be committed.
"""
import argparse
import datetime
import hashlib
import json
import os
import re
import shutil
import signal
import socket
import subprocess
import sys
import tempfile
import threading
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import stub_provider as SP  # noqa: E402

T0 = time.monotonic()
CLIENT = {"name": "chirality-st5-harness", "title": "Chirality ST-5 capture harness", "version": "0.0.0-st5"}
APPROVAL = "on-request"
SANDBOX = "read-only"
PROMPT = "Create the marker folder for the invented pump-skid example."
COMMAND = "mkdir st5-marker-pump-skid"


def rel_ms():
    return round((time.monotonic() - T0) * 1000, 1)


CONFIG = """# Scratch stand-in for the person's Codex configuration (ST-5 capture harness).
model_provider = "st5_stub"
model = "st5-stub-model"
approval_policy = "{approval}"
sandbox_mode = "{sandbox}"

[model_providers.st5_stub]
name = "ST-5 scripted loopback stub (invented content)"
base_url = "http://127.0.0.1:{port}/v1"
wire_api = "responses"

[features]
plugins = false
{extra_features}
[analytics]
enabled = false
"""


class Gen:
    """One Codex App Server process (one generation) and its stdio tap."""

    def __init__(self, h, number, home, cwd):
        self.h, self.number, self.home, self.cwd = h, number, home, cwd
        self.send_pos = self.recv_pos = 0
        self.next_id = 0
        self.pending, self.results = {}, {}
        self.cv = threading.Condition()
        self.server_requests, self.notes = [], []
        self.lock = threading.Lock()
        self.eof = threading.Event()

    def frame(self, direction, raw):
        with self.lock:
            if direction == "app->codex":
                self.send_pos += 1
                pos = self.send_pos
            else:
                self.recv_pos += 1
                pos = self.recv_pos
            self.h.frames.append({"generation": self.number, "direction": direction, "position": pos,
                                  "t_ms": rel_ms(), "raw": raw})

    def start(self):
        env = dict(os.environ)
        env["CODEX_HOME"] = self.home
        env["PATH"] = self.h.a.codex_path + os.pathsep + env.get("PATH", "")
        self.proc = subprocess.Popen([self.h.a.binary, "app-server"], cwd=self.cwd, env=env,
                                     stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                     start_new_session=True)
        self.pgid = os.getpgid(self.proc.pid)
        self.h.event("spawn", generation=self.number)
        threading.Thread(target=self._reader, daemon=True).start()
        threading.Thread(target=self._stderr, daemon=True).start()

    def _reader(self):
        for line in self.proc.stdout:
            raw = line.decode("utf-8", "replace").rstrip("\n")
            self.frame("codex->app", raw)
            try:
                msg = json.loads(raw)
            except ValueError:
                continue
            with self.cv:
                if "id" in msg and "method" not in msg:
                    self.results[msg["id"]] = msg
                elif "id" in msg:
                    self.server_requests.append(msg)
                else:
                    self.notes.append(msg)
                self.cv.notify_all()
        self.eof.set()
        with self.cv:
            self.cv.notify_all()

    def _stderr(self):
        data = self.proc.stderr.read() or b""
        self.h.stderr[self.number] = len(data)
        with open(os.path.join(self.h.out, "gen%d.stderr.local" % self.number), "wb") as f:
            f.write(data)

    def send(self, obj):
        raw = json.dumps(obj, separators=(",", ":"), ensure_ascii=False)
        self.frame("app->codex", raw)
        self.proc.stdin.write((raw + "\n").encode("utf-8"))
        self.proc.stdin.flush()

    def request(self, method, params, timeout=60):
        self.next_id += 1
        rid = self.next_id
        self.send({"jsonrpc": "2.0", "id": rid, "method": method, "params": params})
        return self.wait(lambda: self.results.get(rid), timeout)

    def notify(self, method, params=None):
        obj = {"jsonrpc": "2.0", "method": method}
        if params is not None:
            obj["params"] = params
        self.send(obj)

    def wait(self, pred, timeout):
        end = time.monotonic() + timeout
        with self.cv:
            while True:
                v = pred()
                if v or self.h.stop_reason:
                    return v
                left = end - time.monotonic()
                if left <= 0 or self.eof.is_set():
                    return pred()
                self.cv.wait(min(left, 0.2))

    def initialize(self):
        r = self.request("initialize", {"clientInfo": CLIENT,
                                        "capabilities": {"experimentalApi": True, "requestAttestation": False}})
        if not r or "result" not in r:
            time.sleep(1)
            raise SystemExit("initialize failed: %r rc=%r eof=%r" % (r, self.proc.poll(), self.eof.is_set()))
        if os.path.realpath(r["result"].get("codexHome") or "") != os.path.realpath(self.home):
            raise SystemExit("codexHome is not the scratch home")
        self.notify("initialized")
        return r["result"]


class Harness:
    def __init__(self, a):
        self.a = a
        self.frames, self.events, self.provider_log = [], [], []
        self.stderr = {}
        self.stop_reason = None
        self.out = os.path.realpath(a.out)
        os.makedirs(self.out, exist_ok=True)
        self.scratch = os.path.realpath(tempfile.mkdtemp(prefix="st5-"))
        self.home = os.path.join(self.scratch, "home")
        self.work = os.path.join(self.scratch, "workspace")
        os.makedirs(self.home)
        os.makedirs(self.work)
        with open(os.path.join(self.work, "README.md"), "w") as f:
            f.write("Invented pump-skid example workspace (ST-5 capture).\n")
        self.gens = []

    def event(self, kind, **kw):
        rec = {"event": kind, "t_ms": rel_ms()}
        rec.update(kw)
        self.events.append(rec)
        sys.stderr.write("[%8.1f] %s %s\n" % (rec["t_ms"], kind, json.dumps(kw)[:300]))

    def watch_sockets(self, done):
        while not done.is_set():
            for g in self.gens:
                if g.proc.poll() is not None:
                    continue
                out = subprocess.run(["lsof", "-n", "-P", "-a", "-i", "-g", str(g.pgid)],
                                     capture_output=True, text=True).stdout
                for line in out.splitlines()[1:]:
                    m = re.search(r"->\[?([0-9a-fA-F:.]+)\]?:\d+", line)
                    if m and m.group(1) not in ("127.0.0.1", "::1"):
                        self.stop_reason = "non-loopback socket: " + m.group(1)
                        self.event("STOP", reason=self.stop_reason)
                        os.killpg(g.pgid, signal.SIGKILL)
            done.wait(0.25)

    def write_config(self, port, extra_features=""):
        with open(os.path.join(self.home, "config.toml"), "w") as f:
            f.write(CONFIG.format(approval=APPROVAL, sandbox=SANDBOX, port=port, extra_features=extra_features))

    def gen(self):
        g = Gen(self, len(self.gens) + 1, self.home, self.work)
        self.gens.append(g)
        g.start()
        return g

    def end(self, g, how):
        if how == "stdin":
            g.proc.stdin.close()
        else:
            os.killpg(g.pgid, getattr(signal, how))
        try:
            code = g.proc.wait(timeout=15)
        except subprocess.TimeoutExpired:
            os.killpg(g.pgid, signal.SIGKILL)
            code = g.proc.wait()
        g.eof.wait(5)
        time.sleep(0.3)
        left = [l for l in subprocess.run(["ps", "-axo", "pgid="], capture_output=True, text=True).stdout.split()
                if l == str(g.pgid)]
        if left:
            try:
                os.killpg(g.pgid, signal.SIGKILL)
            except ProcessLookupError:
                pass
        self.event("exit", generation=g.number, how=how, returncode=code, group_members_left=len(left))
        return code


# ---------- provider plans ----------
def tool_names(body):
    names = []
    for t in (body or {}).get("tools") or []:
        if t.get("type") == "namespace":
            names += ["%s.%s" % (t.get("name"), x.get("name")) for x in t.get("tools") or []]
        else:
            names.append(t.get("name") or t.get("type"))
    return names


def has_output(body):
    return any(isinstance(i, dict) and i.get("type", "").endswith("_output") for i in (body or {}).get("input") or [])


def shell_call(body, call_id):
    names = tool_names(body)
    if "exec_command" in names:
        return {"type": "function_call", "name": "exec_command", "call_id": call_id, "id": "fc_" + call_id,
                "arguments": json.dumps({"cmd": COMMAND, "workdir": None, "sandbox_permissions": "require_escalated",
                                         "justification": "Create the invented marker folder."})}
    if "shell_command" in names:
        return {"type": "function_call", "name": "shell_command", "call_id": call_id, "id": "fc_" + call_id,
                "arguments": json.dumps({"command": COMMAND})}
    return {"type": "function_call", "name": "shell", "call_id": call_id, "id": "fc_" + call_id,
            "arguments": json.dumps({"command": ["bash", "-lc", COMMAND]})}


def st5_plan(idx, body):
    if has_output(body):
        return ([SP.message("Done.", "msg_st5_done")], 0, "final message")
    return ([shell_call(body, "call_st5_1")], 0, "shell call")


# ---------- scenarios ----------
def scenario_st5(h, freeze=True):
    prov = SP.Provider(st5_plan, h.provider_log)
    h.write_config(prov.port)
    g1 = h.gen()
    init1 = g1.initialize()
    ts = g1.request("thread/start", {"cwd": h.work, "approvalPolicy": APPROVAL, "sandbox": SANDBOX})
    thread_id = ts["result"]["thread"]["id"]
    g1.request("turn/start", {"threadId": thread_id, "input": [{"type": "text", "text": PROMPT}]})
    req = g1.wait(lambda: next((r for r in g1.server_requests
                                if r["method"] == "item/commandExecution/requestApproval"), None), 60)
    if not req:
        raise SystemExit("no command approval request raised; stop reason %r" % (h.stop_reason,))
    h.event("server-request-received", generation=1, method=req["method"])
    time.sleep(0.2)  # let any frames Codex emits right after the request arrive first
    if freeze:
        os.killpg(g1.pgid, signal.SIGSTOP)
        h.event("process-group-frozen", generation=1, signal="SIGSTOP")
    g1.send({"jsonrpc": "2.0", "id": req["id"], "result": {"decision": "accept"}})
    h.event("answer-written", generation=1, request_position=req["id"], decision="accept",
            origin="capture-harness (stands in for the person's answer)")
    g1.next_id += 1
    g1.send({"jsonrpc": "2.0", "id": g1.next_id, "method": "thread/turns/list",
             "params": {"threadId": thread_id, "limit": 1}})
    h.event("client-request-written", generation=1, method="thread/turns/list",
            note="left un-responded by the process end (X-09's un-responded client request)")
    if freeze:
        os.killpg(g1.pgid, signal.SIGKILL)
        h.event("process-group-killed-while-frozen", generation=1, signal="SIGKILL")
    else:
        os.killpg(g1.pgid, signal.SIGKILL)
        h.event("process-group-killed", generation=1, signal="SIGKILL")
    h.end(g1, "SIGKILL")
    resolved = [n for n in g1.notes if n.get("method") == "serverRequest/resolved"]
    h.event("acknowledgment-reading", generation=1,
            serverRequest_resolved_observed=bool(resolved), turn_completed_observed=any(
                n.get("method") == "turn/completed" for n in g1.notes))
    marker = os.path.exists(os.path.join(h.work, "st5-marker-pump-skid"))
    h.event("workspace-reading", marker_folder_exists=marker)

    # X-10: restart on the same home, recovery read of actual state
    g2 = h.gen()
    g2.initialize()
    read = g2.request("thread/read", {"threadId": thread_id, "includeTurns": True})
    turns = g2.request("thread/turns/list", {"threadId": thread_id, "itemsView": "full"})
    loaded = g2.request("thread/loaded/list", {})
    resume = g2.request("thread/resume", {"threadId": thread_id})
    g2.wait(lambda: g2.server_requests, 3)
    h.event("re-raised-request-reading", generation=2, server_requests_after_resume=len(g2.server_requests))
    h.end(g2, "stdin")
    prov.close()
    h.event("workspace-reading-end", marker_folder_exists=os.path.exists(
        os.path.join(h.work, "st5-marker-pump-skid")))
    return {"init": init1, "thread_id": thread_id,
            "recovery": {"thread/read": bool(read and "result" in read),
                         "thread/turns/list": bool(turns and "result" in turns),
                         "thread/loaded/list": bool(loaded and "result" in loaded),
                         "thread/resume": bool(resume and "result" in resume)}}


def nv04_plan_factory(h):
    state = {"spawned": False}

    def plan(idx, body):
        names = tool_names(body)
        text = json.dumps(body or {})
        child = "st5-child-brief-marker" in text and not has_output(body) and state["spawned"]
        if child:
            return ([SP.message("Child finished counting.", "msg_child")], h.a.child_hold, "child held")
        if has_output(body):
            return ([SP.message("Parent turn done; child still working.", "msg_parent_done")], 0, "parent final")
        spawn = next((n for n in names if n.split(".")[-1] == "spawn_agent"), None)
        if spawn is None:
            return ([SP.message("No spawn tool offered.", "msg_nospawn")], 0, "no spawn tool")
        state["spawned"] = True
        for t in body.get("tools") or []:
            for x in t.get("tools") or []:
                if x.get("name") == "spawn_agent":
                    h.event("spawn-tool-parameters", parameters=sorted((x.get("parameters") or {}).get("properties", {})),
                            required=(x.get("parameters") or {}).get("required"))
        ns, _, nm = spawn.rpartition(".")
        item = {"type": "function_call", "name": nm, "call_id": "call_spawn_1", "id": "fc_spawn_1",
                "arguments": json.dumps({"message": "st5-child-brief-marker: count the invented files.",
                                         "task_name": "count_files"})}
        if ns:
            item["namespace"] = ns
        return ([item], 0, "spawn call")
    return plan


def scenario_nv04(h):
    prov = SP.Provider(nv04_plan_factory(h), h.provider_log)
    h.write_config(prov.port)
    g = h.gen()
    init = g.initialize()
    ts = g.request("thread/start", {"cwd": h.work, "approvalPolicy": "never", "sandbox": SANDBOX})
    thread_id = ts["result"]["thread"]["id"]
    g.request("turn/start", {"threadId": thread_id, "input": [{"type": "text", "text": "Delegate the count."}]})
    done = g.wait(lambda: next((n for n in g.notes if n.get("method") == "turn/completed"
                                and n["params"].get("threadId") == thread_id), None), 60)
    h.event("parent-turn-completed", observed=bool(done))
    g.wait(lambda: next((n for n in g.notes if n.get("method") == "turn/completed"
                         and n["params"].get("threadId") != thread_id), None), h.a.child_hold + 20)
    loaded = g.request("thread/loaded/list", {})
    h.end(g, "stdin")
    prov.close()
    return {"init": init, "thread_id": thread_id, "loaded": loaded}


# ---------- redaction and recording ----------
def build_redactor(h):
    pairs = []
    for p in sorted({h.home, h.work, h.scratch, os.path.realpath(tempfile.gettempdir()),
                     tempfile.gettempdir(), os.path.dirname(h.a.binary), h.a.codex_path,
                     os.path.expanduser("~")}, key=len, reverse=True):
        if p and len(p) > 1:
            name = ("<HOME>" if p == h.home else "<WORKSPACE>" if p == h.work else "<SCRATCH>" if p == h.scratch
                    else "<CODEX-BIN-DIR>" if p == os.path.dirname(h.a.binary) else "<CODEX-PATH-DIR>"
                    if p == h.a.codex_path else "<TMP>" if "tmp" in p.lower() or "var/folders" in p
                    else "<USER-HOME>")
            pairs.append((p, name, "personal path"))
    user = os.path.basename(os.path.expanduser("~"))
    host = socket.gethostname()
    counts = {}

    def red(s):
        for p, name, cat in pairs:
            if p in s:
                counts[cat] = counts.get(cat, 0) + s.count(p)
                s = s.replace(p, name)
        for val, name, cat in ((host, "<HOST>", "host name"), (host.split(".")[0], "<HOST>", "host name")):
            if val and len(val) > 2 and val in s:
                counts[cat] = counts.get(cat, 0) + s.count(val)
                s = s.replace(val, name)
        if user and len(user) > 2 and re.search(r"\b%s\b" % re.escape(user), s):
            counts["user name"] = counts.get("user name", 0) + len(re.findall(r"\b%s\b" % re.escape(user), s))
            s = re.sub(r"\b%s\b" % re.escape(user), "<USER>", s)
        s2 = re.sub(r'("userAgent":")[^"]*(")', r"\1<REDACTED-USER-AGENT>\2", s)
        if s2 != s:
            counts["userAgent client identity"] = counts.get("userAgent client identity", 0) + 1
        s3 = re.sub(r'("serverName":")[^"]*(")', r"\1<REDACTED-HOST>\2", s2)
        if s3 != s2:
            counts["serverName"] = counts.get("serverName", 0) + 1
        s4 = re.sub(r'("installationId":")[^"]*(")', r"\1<REDACTED-INSTALLATION-ID>\2", s3)
        if s4 != s3:
            counts["installation identifier"] = counts.get("installation identifier", 0) + 1
        return s4
    return red, counts


def sha256(path):
    d = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            d.update(chunk)
    return d.hexdigest()


def write_outputs(h, scenario, info):
    with open(os.path.join(h.out, scenario + ".raw-frames.jsonl"), "w") as f:
        for fr in h.frames:
            f.write(json.dumps(fr, ensure_ascii=False) + "\n")
    red, counts = build_redactor(h)
    frames = []
    for fr in h.frames:
        r = red(fr["raw"])
        try:
            parsed = json.loads(r)
        except ValueError:
            parsed = None
        frames.append({"generation": fr["generation"], "direction": fr["direction"], "position": fr["position"],
                       "t_ms": fr["t_ms"], "redacted": r != fr["raw"], "frame": parsed if parsed is not None else r})
    prov = []
    for p in h.provider_log:
        b = p["body"] or {}
        prov.append({"index": p["index"], "path": p["path"], "header_names": p["header_names"],
                     "answered_with": p["answered"], "tools": tool_names(b),
                     "input_item_types": [i.get("type") for i in b.get("input") or [] if isinstance(i, dict)],
                     "body": "not kept (carries instructions, environment context, installation and turn "
                             "identifiers; HOSTING §9.1)"})
    version = subprocess.run([h.a.binary, "--version"], capture_output=True, text=True).stdout.strip()
    init = info.get("init") or {}
    rec = {
        "format": "chirality.app-v4.hosting-capture.st5.v1",
        "scenario": scenario,
        "fixture_standing": "recorded-truncated" if scenario.startswith("st5") else "recorded",
        "standing_note": ("Development evidence at Codex 0.160.0 captured by a prototype harness that stands in "
                          "for the App side; no App candidate, not a qualification pin (OI-012 open), no "
                          "acceptance or VER result. Redacted frames never claim byte identity."),
        "date": datetime.date.today().isoformat(),
        "version_identity": {"version_output": red(version), "binary_sha256": sha256(h.a.binary),
                             "distribution": "npm platform package vendor/aarch64-apple-darwin, complete layout, "
                                             "codex-path on PATH (development assertion only)",
                             "initialize_userAgent": "redacted (client identity)",
                             "platform": {k: init.get(k) for k in ("platformFamily", "platformOs") if k in init}},
        "app_candidate": None,
        "app_side": "st5_harness.py (prototype observation harness)",
        "declared_capabilities": {"experimentalApi": True, "requestAttestation": False},
        "provider": {"kind": "local loopback stub (stub_provider.py), Responses wire API, scripted invented "
                             "output", "requests": prov},
        "settings_in_effect": {"approval_policy": APPROVAL if scenario.startswith("st5") else "never",
                               "sandbox_mode": SANDBOX, "features.plugins": False, "analytics.enabled": False,
                               "note": "scratch stand-ins, not a person's settings"},
        "redaction_record": {"categories_replaced": counts,
                             "markers": ["<HOME>", "<WORKSPACE>", "<SCRATCH>", "<TMP>", "<USER-HOME>", "<USER>",
                                         "<HOST>", "<CODEX-BIN-DIR>", "<CODEX-PATH-DIR>",
                                         "<REDACTED-USER-AGENT>", "<REDACTED-HOST>",
                                         "<REDACTED-INSTALLATION-ID>"],
                             "not_present": "no credential, token, account identifier or secret answer was used"},
        "material": "invented (V4-CST-06): pump-skid marker folder and README",
        "events": h.events,
        "stderr_bytes_by_generation": h.stderr,
        "frames": frames,
    }
    path = os.path.join(h.out, scenario + ".recording.json")
    with open(path, "w") as f:
        json.dump(rec, f, indent=1, ensure_ascii=False)
        f.write("\n")
    leaks = [s for s in (os.path.expanduser("~"), socket.gethostname(), h.scratch) if s and s in open(path).read()]
    if leaks:
        raise SystemExit("redaction incomplete: %d local strings remain" % len(leaks))
    return path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--binary", required=True)
    ap.add_argument("--codex-path", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--child-hold", type=float, default=8.0)
    ap.add_argument("scenario", choices=["st5", "st5-race", "nv04"])
    a = ap.parse_args()
    a.binary = os.path.realpath(a.binary)
    a.codex_path = os.path.realpath(a.codex_path)
    h = Harness(a)
    done = threading.Event()
    threading.Thread(target=h.watch_sockets, args=(done,), daemon=True).start()
    h.event("begin", scenario=a.scenario, pin="0.160.0")
    try:
        if a.scenario == "nv04":
            info = scenario_nv04(h)
        else:
            info = scenario_st5(h, freeze=(a.scenario == "st5"))
    finally:
        done.set()
        with open(os.path.join(h.out, a.scenario + ".raw-frames.jsonl"), "w") as f:
            for fr in h.frames:
                f.write(json.dumps(fr, ensure_ascii=False) + "\n")
        for g in h.gens:
            if g.proc.poll() is None:
                os.killpg(g.pgid, signal.SIGKILL)
    if h.stop_reason:
        raise SystemExit("stopped: " + h.stop_reason)
    print(write_outputs(h, a.scenario, info))
    shutil.rmtree(h.scratch, ignore_errors=True)


if __name__ == "__main__":
    main()
