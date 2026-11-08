#!/usr/bin/env python3
"""OBS-1b observation harness: one live Codex App Server turn on the command-line path.

Prototype only (DEL-01-01, run APP-V4-DESIGN-PASS-2-20260930, node OBS-1b).
Not product code; not an App candidate; nothing here is qualified. Python 3
standard library only. Extends obs1_harness.py (same folder) for part B of
WAVE_B/OBS-1_BRIEF.md section 11, as BRIEFS.md "OBS-1b - the command-line turn"
sets it: a fresh app-server process and thread, one turn, approval policy
`untrusted`, sandbox `read-only`, no MCP server configured, route R-1 only.

Differences from obs1_harness.py:
  - the harness listens on a local Unix-domain socket (<obs>/probe.sock) and
    records every connection to it, with the connecting process id when the
    platform reports it (LOCAL_PEERPID on macOS) and that process's command;
  - approval requests are answered by one rule: accept (the per-request
    `accept` form, never a session form) only when the request's command is
    exactly the named command, compared token by token after unwrapping one
    `<shell> -c`/`-lc` wrapper; every other request gets the decline form.
    Each answer has origin "observation-harness";
  - S-8 for this part means: the turn completes with no commandExecution item.

Usage:
  obs1b_harness.py --obs DIR --binary PATH --model KEY --tool PATH
"""
import argparse
import json
import os
import shlex
import socket
import subprocess
import sys
import threading
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import obs1_harness as base  # noqa: E402

SHELLS = ("sh", "bash", "zsh")


def command_tokens(cmd):
    """Tokens of a command given as a string or an argv list, with one shell wrapper removed."""
    if cmd is None:
        return None
    try:
        toks = list(cmd) if isinstance(cmd, list) else shlex.split(cmd)
    except ValueError:
        return None
    if len(toks) == 3 and os.path.basename(toks[0]) in SHELLS and toks[1] in ("-c", "-lc", "-l -c"):
        try:
            return shlex.split(toks[2])
        except ValueError:
            return None
    return toks


class HarnessB(base.Harness):
    def __init__(self, a):
        super().__init__(a)
        self.probe_path = os.path.join(self.obs, "probe.sock")
        self.named = "python3 %s --key EX-1 --probe-socket %s" % (a.tool, self.probe_path)
        self.named_tokens = shlex.split(self.named)
        self.probe_sock = None
        self.probe_conns = []
        self.cmd_items = []
        # S-5 classification (repairs OBS-1 deviation D-3): besides the fixed GitHub ranges, an address
        # counts as the plugin repository when the socket to it belongs to a process whose command line
        # fetches https://github.com/openai/plugins.git (the supplier's plugin sync, U-18).
        orig = base.is_github

        def is_plugin_repo(addr):
            if orig(addr):
                return True
            pids = {str(r[0]) for r in (self.snap_last.get("procs") or []) if "github.com/openai/plugins" in r[3]}
            for line in self.snap_last.get("sockets") or []:
                cols = line.split()
                if len(cols) > 8 and cols[1] in pids and base.parse_remote(" ".join(cols[8:]))[0] == addr:
                    return True
            return False
        base.is_github = is_plugin_repo

    # ---------- local probe socket (A-7, ADAPTER OC-5) ----------
    def probe_listen(self):
        if os.path.exists(self.probe_path):
            os.unlink(self.probe_path)
        s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        s.bind(self.probe_path)
        s.listen(4)
        self.probe_sock = s
        self.rec.event("probe-socket listening", path="<OBS>/probe.sock", path_len=len(self.probe_path))

        def loop():
            while True:
                try:
                    c, _ = s.accept()
                except OSError:
                    return
                rec = {"wall_ms": base.wall_ms()}
                try:
                    pid = c.getsockopt(0, 0x002, 4)  # SOL_LOCAL, LOCAL_PEERPID (macOS)
                    pid = int.from_bytes(pid, sys.byteorder)
                    rec["peer_pid"] = pid
                    ps = subprocess.run(["ps", "-o", "pid=,ppid=,pgid=,command=", "-p", str(pid)],
                                        capture_output=True, text=True).stdout.strip()
                    rec["peer"] = ps[:300]
                except OSError as exc:
                    rec["peer_error"] = repr(exc)
                c.close()
                self.probe_conns.append(rec)
                self.rec.event("probe-socket connection", **rec)
        threading.Thread(target=loop, daemon=True).start()

    # ---------- approvals: the one rule ----------
    def answer_server_request(self, msg):
        rid, method, p = msg["id"], msg["method"], msg.get("params") or {}
        answer, error, rule, exact = None, None, None, False
        if method == "item/commandExecution/requestApproval":
            toks = command_tokens(p.get("command"))
            exact = toks == self.named_tokens and (p.get("kind") in (None, "command"))
            answer = {"decision": "accept" if exact else "decline"}
            rule = "command approval: %s" % ("subject is exactly the named command -> accept (this request only)"
                                              if exact else "subject is not exactly the named command -> decline")
        elif method == "execCommandApproval":
            toks = command_tokens(p.get("command"))
            exact = toks == self.named_tokens
            answer = {"decision": "approved" if exact else "denied"}
            rule = "legacy command approval -> %s" % answer["decision"]
        elif method == "item/permissions/requestApproval":
            answer = {"permissions": {}, "scope": "turn"}
            rule = "permissions approval -> decline form (grant nothing)"
        elif method in ("item/fileChange/requestApproval",):
            answer = {"decision": "decline"}
            rule = "file change approval -> decline"
        elif method == "applyPatchApproval":
            answer = {"decision": "denied"}
            rule = "legacy patch approval -> denied"
        elif method == "mcpServer/elicitation/request":
            answer = {"action": "decline", "content": None, "_meta": None}
            rule = "elicitation -> decline"
        elif method == "item/tool/requestUserInput":
            answer = {"answers": {q.get("id"): {"answers": ["Invented example answer: proceed."]}
                                  for q in (p.get("questions") or [])}}
            rule = "requestUserInput -> invented answer"
        else:
            if method == "account/chatgptAuthTokens/refresh" or method.startswith("account/"):
                self.trigger_stop("S-3", "sign-in related server request: %s" % method)
            error = {"code": -32601, "message": "observation harness: not answered (%s)" % method}
            rule = "explicit JSON-RPC error"
        self.rec.event("server-request", id=rid, method=method, exact_named_command=exact, rule=rule,
                       answer=answer, origin="observation-harness")
        if error is not None:
            self.send({"jsonrpc": "2.0", "id": rid, "error": error})
        else:
            self.send({"jsonrpc": "2.0", "id": rid, "result": answer})

    def on_notification(self, msg):
        super().on_notification(msg)
        p = msg.get("params") or {}
        item = p.get("item") or {}
        if msg.get("method") in ("item/started", "item/completed") and item.get("type") == "commandExecution":
            self.cmd_items.append((msg["method"], item.get("id"), item.get("status")))
            self.rec.event("commandExecution " + msg["method"], id=item.get("id"), status=item.get("status"),
                           source=item.get("source"), exitCode=item.get("exitCode"))

    # ---------- sequence (D-2..D-8; one turn only) ----------
    def sequence(self, obs_real):
        a = self.a
        self.rec.event("capture-metadata-b", scenario="OBS-1b one live turn, command-line path", pin="0.158.0",
                       approval_policy="untrusted", sandbox="read-only", mcp_servers="none",
                       named_command=self.named.replace(self.obs, "<OBS>"))
        self.probe_listen()
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
        self.notify("initialized")
        time.sleep(3.0)
        r = self.request("mcpServerStatus/list", {}, timeout=60)
        self.rec.event("D-4 mcpServerStatus/list", ok=bool(r and "result" in r))
        if self.stop_evt.is_set():
            return
        dev = ("You are running an observation test with invented data. When asked, run the command you "
               "are given. Keep replies to one sentence.")
        r = self.request("thread/start", {"cwd": self.cwd, "model": a.model, "modelProvider": "obs1_lmstudio",
                                          "approvalPolicy": "untrusted", "sandbox": "read-only",
                                          "developerInstructions": dev}, timeout=120)
        if r is None or "result" not in r:
            self.trigger_stop("R-1-thread-start-failed", "thread/start failed: %r (route R-1 only; R-2 not tried)"
                              % ((r or {}).get("error"),))
            return
        res = r["result"]
        self.thread_id = (res.get("thread") or {}).get("id")
        rep_model, rep_prov = res.get("model"), res.get("modelProvider")
        self.rec.event("D-5 thread/start", thread=self.thread_id, reported_model=rep_model,
                       reported_provider=rep_prov, approvalPolicy=res.get("approvalPolicy"),
                       sandbox=res.get("sandbox"), instructionSources=res.get("instructionSources"))
        if rep_model != a.model or rep_prov != "obs1_lmstudio":
            self.trigger_stop("S-3", "thread start reports model %r provider %r" % (rep_model, rep_prov))
            return
        # The owner's limit is approval policy `untrusted`. Pin 0.158.0 refuses it in config.toml
        # ("no longer supported"), so it is requested on thread/start only; if the thread reports
        # another policy, no turn is started.
        if res.get("approvalPolicy") != "untrusted":
            self.trigger_stop("approval-policy-not-untrusted",
                              "thread start reports approvalPolicy %r; no turn started" % (res.get("approvalPolicy"),))
            return
        for src in res.get("instructionSources") or []:
            pth = src if isinstance(src, str) else (src.get("path") if isinstance(src, dict) else None)
            if pth and not self._under_obs(pth, obs_real):
                self.trigger_stop("S-4", "instructionSources lists a path outside OBS: %r" % pth)
                return
        if self.stop_evt.is_set():
            return
        prompt = "This is a test with invented data. Run `%s` and report the outcome in one sentence." % self.named
        self.turn_active = True
        r = self.request("turn/start", {"threadId": self.thread_id,
                                        "input": [{"type": "text", "text": prompt, "text_elements": []}]}, timeout=60)
        if r is None or "result" not in r:
            self.turn_active = False
            self.trigger_stop("S-11", "turn/start failed: %r" % (r,))
            return
        self.turn_id = ((r["result"] or {}).get("turn") or {}).get("id")
        self.rec.event("D-6 turn/start", turn=self.turn_id)
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
        self.rec.event("turn/completed received", commandExecution_items=self.cmd_items,
                       probe_connections=len(self.probe_conns))
        if not self.cmd_items:
            self.rec.event("S-8 (part B): no commandExecution item in the turn")
        time.sleep(2.0)

    def finish(self):
        super().finish()
        if self.probe_sock:
            self.probe_sock.close()
            try:
                os.unlink(self.probe_path)
            except OSError:
                pass


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--obs", required=True)
    ap.add_argument("--binary", required=True)
    ap.add_argument("--model", required=True)
    ap.add_argument("--tool", required=True)
    a = ap.parse_args()
    a.part_d = False
    a.mcp_double = None
    h = HarnessB(a)
    h.run()
    print(json.dumps({"stop": h.stop_reason, "thread": h.thread_id, "turn": h.turn_id,
                      "commandExecution": h.cmd_items, "probe_connections": h.probe_conns}))


if __name__ == "__main__":
    main()
