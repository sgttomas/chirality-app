"""Executable model of the HOSTING-BOUNDARY-v0.8 rules (DEL-01-01), used to run
the designed cases against supplier_double.py.

Prototype only (Wave B node B6). NOT product code, NOT an App candidate, and
NOT the O-1 proposal realized: it is a small Python model of the boundary's
stated rules (§3 H1-H11, §4 lifecycle, §5 frames and client requests, §6
register R1-R9, §8.3 destination facts) so that the rules can be run end to
end. A case that passes here shows the rules are consistent and executable
against the double; it passes no VER criterion (no candidate exists).

Numbers marked TEST VALUE are implementation choices the file leaves open
(U-05 restart bound and delays, grace period, wait limits, frame size limit,
the App's error code for unfamiliar requests).
"""
import datetime
import hashlib
import uuid
import json
import os
import queue
import signal
import subprocess
import sys
import threading
import time

import jsonschema_subset as V

HERE = os.path.dirname(os.path.abspath(__file__))
DESIGN = os.path.dirname(HERE)
BUNDLE = os.path.join(DESIGN, "generated", "0.158.0", "json-schema", "experimental",
                      "codex_app_server_protocol.schemas.json")
SEED_DIR = os.path.join(DESIGN, "generated", "0.158.0", "_spike", "transcripts")

# ---- TEST VALUES (open implementation choices) ---------------------------
MAX_FAILURES, FAILURE_WINDOW_S = 3, 60.0          # U-05
RESTART_DELAYS_S = [0.05, 0.1, 0.2]                # U-05 (growing)
HANDSHAKE_WAIT_S = 2.0                             # wait limit
GRACE_S = 1.0                                      # §4.5 grace period
FRAME_LIMIT = 262144                               # oversize threshold (bytes)
UNFAMILIAR_ERROR_CODE = -32601                     # R2: App's code is a choice (S-F-16)
DECLARED_PIN = "0.158.0"

# ---- §4.7 lifecycle transition table (LT-nn); checked against HOSTING ----
TRANSITIONS = {
    "LT-01": ("absent", "start-requested", "verifying"),
    "LT-02": ("stopped", "start-requested", "verifying"),
    "LT-03": ("refused", "start-requested", "verifying"),
    "LT-04": ("verifying", "verification-passed", "spawning"),
    "LT-05": ("verifying", "verification-failed", "refused"),
    "LT-06": ("spawning", "spawned", "handshaking"),
    "LT-07": ("spawning", "spawn-failed", "restart-waiting"),
    "LT-08": ("spawning", "spawn-failed", "halted-after-repeated-failure"),
    "LT-09": ("handshaking", "handshake-completed", "ready"),
    "LT-10": ("handshaking", "handshake-failed", "restart-waiting"),
    "LT-11": ("handshaking", "handshake-failed", "halted-after-repeated-failure"),
    "LT-12": ("ready", "child-ended-without-stop-record", "exited-unexpectedly"),
    "LT-13": ("exited-unexpectedly", "exit-recorded", "restart-waiting"),
    "LT-14": ("exited-unexpectedly", "exit-recorded", "halted-after-repeated-failure"),
    "LT-15": ("restart-waiting", "restart-delay-elapsed", "verifying"),
    "LT-16": ("halted-after-repeated-failure", "explicit-restart-requested", "verifying"),
    "LT-17": ("ready", "stop-requested", "stopping"),
    "LT-18": ("handshaking", "stop-requested", "stopping"),
    "LT-19": ("spawning", "stop-requested", "stopping"),
    "LT-20": ("verifying", "stop-requested", "stopped"),
    "LT-21": ("restart-waiting", "stop-requested", "stopped"),
    "LT-22": ("halted-after-repeated-failure", "stop-requested", "stopped"),
    "LT-23": ("stopping", "tree-ended", "stopped"),
    "LT-24": ("verifying", "development-start-authorized", "spawning"),
}

# ---- §6.2.1 register transition table (RT-nn) -------------------------
REGISTER_TRANSITIONS = {
    "RT-01": (None, "server-request-received", "received"),
    "RT-02": ("received", "classified-unfamiliar", "errored"),
    "RT-03": ("received", "classified-known-app-unsupported", "errored"),
    "RT-04": ("received", "classified-known-answerable", "outstanding"),
    "RT-05": ("outstanding", "answer-refused", "outstanding"),
    "RT-06": ("outstanding", "answer-accepted-for-write", "settling"),
    "RT-07": ("settling", "reply-written-affirmative-or-content", "answered"),
    "RT-08": ("settling", "reply-written-negative", "declined"),
    "RT-09": ("settling", "reply-write-failed", "settle-write-failed"),
    "RT-10": ("outstanding", "supplier-reported-resolution", "resolved-by-supplier"),
    "RT-11": ("outstanding", "generation-closed", "ended-unanswered"),
    "RT-12": ("answered", "supplier-reported-resolution", "answered"),
    "RT-13": ("declined", "supplier-reported-resolution", "declined"),
}

STABLE_KINDS = [
    "item/commandExecution/requestApproval", "item/fileChange/requestApproval",
    "item/tool/requestUserInput", "mcpServer/elicitation/request",
    "item/permissions/requestApproval", "item/tool/call",
    "account/chatgptAuthTokens/refresh", "attestation/generate",
    "applyPatchApproval", "execCommandApproval"]
# §6.1 proposed partition (U-20) and R9 origin classes
PARTITION = {
    "item/commandExecution/requestApproval": ("known-answerable", "a14"),
    "item/fileChange/requestApproval": ("known-answerable", "a14"),
    "item/permissions/requestApproval": ("known-answerable", "a14"),
    "execCommandApproval": ("known-answerable", "a14"),
    "applyPatchApproval": ("known-answerable", "a14"),
    "item/tool/requestUserInput": ("known-answerable", "person-input"),
    "mcpServer/elicitation/request": ("known-answerable", "person-input"),
    "item/tool/call": ("known-app-unsupported", "none"),
    "account/chatgptAuthTokens/refresh": ("known-app-unsupported", "none"),
    "attestation/generate": ("known-app-unsupported", "none"),
    "currentTime/read": ("known-answerable", "named-service"),
}
RESPONSE_DEF = {
    "item/commandExecution/requestApproval": "#/definitions/CommandExecutionRequestApprovalResponse",
    "item/fileChange/requestApproval": "#/definitions/FileChangeRequestApprovalResponse",
    "item/permissions/requestApproval": "#/definitions/PermissionsRequestApprovalResponse",
    "execCommandApproval": "#/definitions/ExecCommandApprovalResponse",
    "applyPatchApproval": "#/definitions/ApplyPatchApprovalResponse",
    "item/tool/requestUserInput": "#/definitions/ToolRequestUserInputResponse",
    "mcpServer/elicitation/request": "#/definitions/McpServerElicitationRequestResponse",
    "item/tool/call": "#/definitions/DynamicToolCallResponse",
    "account/chatgptAuthTokens/refresh": "#/definitions/ChatgptAuthTokensRefreshResponse",
    "attestation/generate": "#/definitions/AttestationGenerateResponse",
    "currentTime/read": "#/definitions/CurrentTimeReadResponse",
}
NEGATIVE = {"decline", "cancel", "abort", "denied"}
HOLD_REFUSABLE = {"turn/start", "mcpServer/tool/call", "mcpServer/resource/read"}


def now_text():
    return datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="milliseconds")


def is_negative(method, native):
    if not isinstance(native, dict):
        return False
    d = native.get("decision", native.get("action"))
    if isinstance(d, str):
        return d in NEGATIVE
    if isinstance(d, dict):
        return any(k in NEGATIVE for k in d)
    return False


class Child:
    """One spawned process tree (the double) with a stdout reader thread."""

    def __init__(self, argv):
        self.proc = subprocess.Popen(argv, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE, start_new_session=True)
        self.q = queue.Queue()
        self.stderr_bytes = 0
        threading.Thread(target=self._read, daemon=True).start()
        threading.Thread(target=self._err, daemon=True).start()

    def _read(self):
        for line in iter(self.proc.stdout.readline, b""):
            self.q.put(("line", line.rstrip(b"\n")))
        self.q.put(("eof", None))

    def _err(self):
        for chunk in iter(lambda: self.proc.stderr.read(4096), b""):
            self.stderr_bytes += len(chunk)  # captured, bounded, never parsed

    def write(self, obj):
        try:
            self.proc.stdin.write((json.dumps(obj, separators=(",", ":")) + "\n").encode())
            self.proc.stdin.flush()
            return "written"
        except (BrokenPipeError, OSError, ValueError):
            return "write-failed"

    def quiet_close(self):
        try:
            self.proc.stdin.close()
        except OSError:
            pass

    def descendants_alive(self):
        try:
            os.killpg(self.proc.pid, 0)
            return 1
        except (ProcessLookupError, PermissionError):
            return 0


class Boundary:
    def __init__(self, scenario="default", seed="A-bin-freshhome", declared=None,
                 phase="phase-1", distribution=None, expected=None, log_dir=None,
                 spawn_argv=None):
        self.scenario, self.seed = scenario, seed
        self.declared = declared or {"experimentalApi": False, "requestAttestation": False}
        self.phase = phase
        self.distribution = distribution or {"label": "codex-cli 0.158.0", "content": "double-tree-1",
                                             "outputPin": "0.158.0"}
        self.expected = expected or {"label": "codex-cli 0.158.0", "content": "double-tree-1",
                                     "outputPin": "0.158.0"}
        self.log_dir = log_dir
        self.spawn_argv = spawn_argv
        self.root = json.load(open(BUNDLE, encoding="utf-8"))
        self.app_session, self.home = str(uuid.uuid4()), "prototype-account"
        self.allow_unverified_dev = False
        self.supplier_standing = "verified-pin"
        self.state, self.generation, self.child = "absent", 0, None
        self.seq, self.events, self.failures, self.fail_times = 0, [], 0, []
        self.transitions_used = set()
        self.register_transitions_used = set()
        self.delivered, self.held, self.pos = [], [], 0
        self.client, self.register, self.malformed = {}, {}, 0
        self.stop_record, self.next_id, self.holding_threads = None, 100, set()
        self.out_pos = 0
        self.inject_stop_in = None  # test hook: a stop request arriving in this state
        self.destination = {"thread": {}, "turns": {}}
        self.pending_turn_request = {}
        self.version_identity = None
        self.restart_at = None

    def generation_identity(self, counter):
        return None if not counter else {"appSession": self.app_session, "home": self.home, "spawnCounter": counter}

    # ---- lifecycle -----------------------------------------------------
    def _transition(self, tid, event, **extra):
        frm, ev, to = TRANSITIONS[tid]
        assert frm == self.state and ev == event, "illegal %s: %s --%s-->" % (tid, self.state, event)
        self.seq += 1
        pre_spawn = ev in ("start-requested", "verification-passed", "verification-failed", "development-start-authorized",
                           "restart-delay-elapsed", "explicit-restart-requested") or \
            (ev == "stop-requested" and to == "stopped")
        rec = {"recordKind": "lifecycle-event", "sequence": self.seq, "transitionId": tid,
               "generation": None if pre_spawn else (self.generation or None),
               "fromState": frm, "event": ev,
               "toState": to, "at": now_text()}
        if self.supplier_standing == "unverified-development":
            rec["supplierStanding"] = self.supplier_standing
        rec.update(extra)
        self.events.append(rec)
        self.transitions_used.add(tid)
        self.state = to
        return rec

    def _count_failure(self):
        t = time.monotonic()
        self.fail_times = [x for x in self.fail_times if t - x < FAILURE_WINDOW_S] + [t]
        return len(self.fail_times)

    def start(self, actor="app-startup", explicit=False):
        if self.state == "halted-after-repeated-failure":
            assert explicit, "halted: only an explicit person-initiated restart"
            self._transition("LT-16", "explicit-restart-requested", actor=actor)
            self.fail_times = []
        elif self.state == "restart-waiting":
            self._transition("LT-15", "restart-delay-elapsed")
        else:
            tid = {"absent": "LT-01", "stopped": "LT-02", "refused": "LT-03"}[self.state]
            self._transition(tid, "start-requested", actor=actor)
        return self._verify_and_spawn()

    def _injected_stop(self):
        if self.inject_stop_in == self.state:
            self.inject_stop_in = None
            self.stop(actor="person:ex-1", reason="stop requested during start (injected)")
            return True
        return False

    def _verify_and_spawn(self):
        if self._injected_stop():
            return False
        d, e = self.distribution, self.expected
        if not e.get("content") and d.get("label") == e.get("label") and d.get("outputPin") == DECLARED_PIN:
            vr = {"result": "unverifiable", "reason": "no expected distribution identity"}
        elif d["label"] != e["label"]:
            vr = {"result": "mismatch", "element": "observed version label"}
        elif d["content"] != e["content"]:
            vr = {"result": "mismatch", "element": "distribution content identity"}
        elif d["outputPin"] != DECLARED_PIN:
            vr = {"result": "mismatch", "element": "generated-output identity"}
        else:
            vr = {"result": "verified"}
        dev = self.allow_unverified_dev and vr["result"] == "unverifiable" and bool(d.get("label"))
        if vr["result"] != "verified" and not dev:
            self._transition("LT-05", "verification-failed", verificationResult=vr)
            return False
        self.supplier_standing = "unverified-development" if dev else "verified-pin"
        if dev:
            self._transition("LT-24", "development-start-authorized", verificationResult=vr,
                             supplierStanding=self.supplier_standing,
                             reason="U-06 development run: unverified distribution, not the pinned supplier")
        else:
            self._transition("LT-04", "verification-passed", verificationResult=vr)
        if self._injected_stop():
            return False
        self.generation += 1
        g = self.generation
        argv = self.spawn_argv or [sys.executable, os.path.join(HERE, "supplier_double.py"),
                                   "--seed-dir", SEED_DIR, "--seed", self.seed,
                                   "--scenario", self.scenario]
        if self.log_dir and not self.spawn_argv:
            argv += ["--log", os.path.join(self.log_dir, "double-g%d.jsonl" % g)]
        try:
            self.child = Child(argv)
        except OSError as exc:
            n = self._count_failure()
            tid = "LT-08" if n >= MAX_FAILURES else "LT-07"
            self._transition(tid, "spawn-failed", failure="spawn-error: %s" % exc.__class__.__name__,
                             failureCount=n)
            self._schedule_restart()
            return False
        self.pos = 0
        self._transition("LT-06", "spawned")
        return self._handshake()

    def _handshake(self):
        g = self.generation
        init_id = self._new_id()
        params = {"clientInfo": {"name": "chirality-b6-model", "title": "B6 boundary model",
                                 "version": "0.0.0-prototype"},
                  "capabilities": dict(self.declared)}
        self.child.write({"jsonrpc": "2.0", "id": init_id, "method": "initialize", "params": params})
        if self._injected_stop():
            return False
        deadline, response = time.monotonic() + HANDSHAKE_WAIT_S, None
        failure = None
        while response is None:
            try:
                kind, raw = self.child.q.get(timeout=max(0.0, deadline - time.monotonic()))
            except queue.Empty:
                failure = "no-response-within-wait-limit"
                break
            if kind == "eof":
                failure = "child-ended"
                break
            frame = self._classify(raw)
            if frame["class"] == "response" and frame["obj"].get("id") == init_id:
                if "error" in frame["obj"]:
                    failure = "error-response"
                    break
                response = frame
            else:
                if frame["class"] == "server-request":
                    self._register(frame)  # R1: entry at receipt, even while handshaking
                    frame["registered"] = True
                self.held.append(frame)  # H4: kept in order under g, delivered at ready
        if response is None:
            self._end_tree(close_first=True)
            n = self._count_failure()
            tid = "LT-11" if n >= MAX_FAILURES else "LT-10"
            closed = self._close_generation()
            self._transition(tid, "handshake-failed", failure=failure, failureCount=n,
                             closedGeneration=closed)
            for f in self.held:  # never dropped (H4): surfaced as from a generation never ready
                f["neverReady"] = True
                self._deliver(f)
            self.held = []
            self._schedule_restart()
            return False
        res = response["obj"]["result"]
        ua = res.get("userAgent", "")
        ver = ua.split(" ")[0].split("/")[-1] if "/" in ua else None
        consistency = ("no-version-found" if not ver else
                       "consistent" if ver == DECLARED_PIN else "contradicts-declared-pin")
        self.version_identity = {
            "declaredPin": DECLARED_PIN, "observedVersionLabel": self.distribution["label"],
            "handshakeReportedIdentity": res, "handshakeConsistency": consistency,
            "launcherRecord": {"launcher": "supplier-double", "addedEnvironment": []},
            "generatedOutputIdentity": "0.158.0 json-schema experimental (committed bundle)",
            "supplementIdentity": "empty"}
        self.child.write({"jsonrpc": "2.0", "method": "initialized"})
        self._transition("LT-09", "handshake-completed", versionIdentity=self.version_identity,
                         declaredCapabilities=dict(self.declared))
        self.delivered.append({"generation": self.generation_identity(g), "position": None, "class": "announcement",
                               "announcement": "ready", "supplierStanding": self.supplier_standing, "versionIdentity": self.version_identity})
        for f in self.held:
            self._deliver(f)
        self.held = []
        return True

    def _schedule_restart(self):
        if self.state == "restart-waiting":
            i = min(len(self.fail_times) - 1, len(RESTART_DELAYS_S) - 1)
            self.restart_at = time.monotonic() + RESTART_DELAYS_S[max(i, 0)]

    def _end_tree(self, close_first=True, means="close-input"):
        c = self.child
        if c is None:
            return {"exitCode": None, "signal": None}, {"checked": False, "surviving": 0}
        try:
            if means == "termination-signal":
                c.proc.send_signal(signal.SIGTERM)
            else:
                c.proc.stdin.close()
        except OSError:
            pass
        forced = False
        try:
            c.proc.wait(timeout=GRACE_S)
        except subprocess.TimeoutExpired:
            forced = True
            try:
                os.killpg(c.proc.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
            c.proc.wait()
        c.quiet_close()
        rc = c.proc.returncode
        facts = {"exitCode": rc if rc is not None and rc >= 0 else None,
                 "signal": ("SIG%d" % -rc) if rc is not None and rc < 0 else None,
                 "lastReceiptPosition": self.pos, "malformedFrameCount": self.malformed,
                 "diagnosticOutputBytes": c.stderr_bytes, "forcedAfterGrace": forced}
        surviving = c.descendants_alive()
        return facts, {"checked": True, "surviving": surviving,
                       "handling": "recorded; none to handle" if not surviving else "recorded (U-16)"}

    def _close_generation(self):
        g, unk, ended = self.generation, 0, 0
        for rec in self.client.values():
            if rec["generation"] == g and rec["outcome"] == "pending":
                rec["outcome"] = "unknown-no-response"
                unk += 1
        for e in self.register.values():
            if e["generation"] == g and e["state"] in ("outstanding", "received"):
                self._reg(e, "RT-11", "generation-closed", "ended-unanswered")
                e["endCause"] = "process-exit"
                ended += 1
        return {"unknownNoResponse": unk, "endedUnanswered": ended}

    def stop(self, actor="person:ex-1", reason="person chose stop", means="close-input",
             outstanding="left-to-end-with-process"):
        record = {"actor": actor, "reason": reason, "outstandingEntryHandling": outstanding,
                  "endingMeans": means}
        self.stop_record = record  # written first: the only evidence the end was deliberate
        if self.state in ("verifying", "restart-waiting", "halted-after-repeated-failure"):
            tid = {"verifying": "LT-20", "restart-waiting": "LT-21",
                   "halted-after-repeated-failure": "LT-22"}[self.state]
            self._transition(tid, "stop-requested", actor=actor, stopRecord=record)
            return
        tid = {"ready": "LT-17", "handshaking": "LT-18", "spawning": "LT-19"}[self.state]
        self._transition(tid, "stop-requested", actor=actor, stopRecord=record)
        if self.state == "stopping" and tid == "LT-19":
            self.generation += 1  # the generation that would have been spawned is closed unused
            self._transition("LT-23", "tree-ended", exitFacts={"exitCode": None, "signal": None},
                             descendants={"checked": True, "surviving": 0,
                                          "handling": "no process tree was created"},
                             closedGeneration={"unknownNoResponse": 0, "endedUnanswered": 0})
            return
        if outstanding == "declined-by-app-rule-on-stop":
            for e in list(self.register.values()):
                if e["generation"] == self.generation and e["state"] == "outstanding":
                    self.answer(e["requestIdentity"], self._decline_form(e["method"]),
                                {"class": "app-rule", "ruleName": "on-stop"})
        facts, desc = self._end_tree(means=means)
        self.pump(0.05)
        closed = self._close_generation()
        self._transition("LT-23", "tree-ended", exitFacts=facts, descendants=desc,
                         closedGeneration=closed)

    def _decline_form(self, method):
        if method == "mcpServer/elicitation/request":
            return {"action": "decline"}
        return {"decision": "decline"}

    # ---- frames ---------------------------------------------------------
    def _classify(self, raw):
        self.pos += 1
        f = {"generation": self.generation, "position": self.pos, "raw": raw}
        if len(raw) > FRAME_LIMIT:
            f.update({"class": "malformed", "reason": "oversize", "bytes": len(raw)})
            self.malformed += 1
            return f
        try:
            obj = json.loads(raw)
        except ValueError:
            f.update({"class": "malformed", "reason": "not-json"})
            self.malformed += 1
            return f
        f["obj"] = obj
        if not isinstance(obj, dict):
            f.update({"class": "malformed", "reason": "not-an-object"})
            self.malformed += 1
        elif "method" in obj and "id" in obj:
            f["class"] = "server-request"
        elif "method" in obj:
            f["class"] = "notification"
        elif "id" in obj and ("result" in obj or "error" in obj):
            f["class"] = "response"
        else:
            f.update({"class": "malformed", "reason": "unclassifiable"})
            self.malformed += 1
        return f

    def _deliver(self, f):
        """H6: native frame unchanged; metadata beside it, never merged."""
        meta = {k: f[k] for k in ("generation", "position", "class", "reason", "neverReady") if k in f}
        meta["generation"] = self.generation_identity(f["generation"])
        if f["class"] == "notification":
            meta["familiar"] = f["obj"]["method"] in self._familiar_notifications()
            self._observe_notification(f)
        if f["class"] == "server-request" and not f.get("registered"):
            self._register(f)
        if f["class"] == "response":
            if not self._correlate(f):
                meta["class"] = "uncorrelated-response"
        self.delivered.append({"meta": meta, "native": f["raw"]})

    def _familiar_notifications(self):
        if not hasattr(self, "_notes"):
            u = self.root["definitions"]["ServerNotification"]["oneOf"]
            self._notes = {b["properties"]["method"]["enum"][0] for b in u}
        return self._notes

    def pump(self, seconds):
        """Process inbound frames for `seconds`; handle exits and restarts."""
        end = time.monotonic() + seconds
        while True:
            if self.state == "restart-waiting" and self.restart_at and time.monotonic() >= self.restart_at:
                self.restart_at = None
                self.start()
                continue
            left = end - time.monotonic()
            if left <= 0:
                return
            if self.child is None or self.state not in ("ready", "stopping"):
                time.sleep(min(left, 0.02))
                continue
            try:
                kind, raw = self.child.q.get(timeout=min(left, 0.05))
            except queue.Empty:
                continue
            if kind == "eof":
                self._on_eof()
                continue
            self._deliver(self._classify(raw.decode("utf-8", "replace")))

    def _on_eof(self):
        if self.state == "stopping":
            return  # stop() finishes the transition
        c = self.child
        c.quiet_close()
        try:
            c.proc.wait(timeout=GRACE_S)
        except subprocess.TimeoutExpired:
            pass
        rc = c.proc.returncode
        facts = {"exitCode": rc if rc is not None and rc >= 0 else None,
                 "signal": ("SIG%d" % -rc) if rc is not None and rc < 0 else None,
                 "lastReceiptPosition": self.pos, "malformedFrameCount": self.malformed,
                 "diagnosticOutputBytes": c.stderr_bytes}
        closed = self._close_generation()
        # S-F-07: no stop record for g, so the end is unexpected whatever the exit code
        self._transition("LT-12", "child-ended-without-stop-record", exitFacts=facts,
                         closedGeneration=closed)
        n = self._count_failure()
        tid = "LT-14" if n >= MAX_FAILURES else "LT-13"
        self._transition(tid, "exit-recorded", failureCount=n)
        self.child = None
        self._schedule_restart()

    # ---- client-request path (§5, §5.1) ---------------------------------
    def _new_id(self):
        self.next_id += 1
        return self.next_id

    def send(self, method, params, initiator):
        rec = {"recordKind": "client-request", "generation": self.generation or None,
               "requestIdentity": None, "method": method, "initiator": initiator,
               "sendPosition": None, "writeResult": "not-attempted", "outcome": "refused-not-sent"}
        if self.state != "ready":
            rec["refusalReason"] = "not-ready"
            self.client[("refused", len(self.client))] = rec
            return rec
        if (self.phase == "governance" and method in HOLD_REFUSABLE
                and initiator["kind"] != "person-directed"
                and params.get("threadId") in self.holding_threads):
            rec["refusalReason"] = "run-holding"  # HP-4, governance phase only
            self.client[("refused", len(self.client))] = rec
            return rec
        rid = self._new_id()
        self.out_pos += 1
        rec.update({"requestIdentity": rid, "sendPosition": self.out_pos, "outcome": "pending"})
        guidance = []
        for el in ("baseInstructions", "developerInstructions"):
            if isinstance(params.get(el), str):
                guidance.append({"element": el, "contentIdentity": {
                    "algorithm": "sha256 (prototype choice; U-08 open)",
                    "value": hashlib.sha256(params[el].encode()).hexdigest()},
                    "sourceIdentity": None})
        if guidance:
            rec["carriedGuidance"] = guidance
        self._observe_request(method, params, rid)
        rec["writeResult"] = self.child.write({"jsonrpc": "2.0", "id": rid, "method": method,
                                               "params": params})
        if rec["writeResult"] == "write-failed":
            rec["outcome"] = "unknown-no-response"
        self.client[(self.generation, rid)] = rec
        return rec

    def wait_for(self, rec, seconds):
        end = time.monotonic() + seconds
        while rec["outcome"] == "pending" and time.monotonic() < end:
            self.pump(0.05)
        if rec["outcome"] == "pending":
            rec["waitingEnded"] = True  # ends waiting, not the outcome (H10)
        return rec

    def _correlate(self, f):
        rec = self.client.get((f["generation"], f["obj"].get("id")))
        if rec is None or rec["outcome"] != "pending":
            return False
        rec["responseReceiptPosition"] = f["position"]
        if "error" in f["obj"]:
            rec["outcome"] = "response-observed-error"
            rec["error"] = {k: f["obj"]["error"][k] for k in ("code", "message")}
        else:
            rec["outcome"] = "response-observed-result"
            rec["_result"] = f["obj"]["result"]
            self._observe_response(rec)
        return True

    # ---- register (§6) --------------------------------------------------
    def _familiar(self, method):
        kinds = set(STABLE_KINDS)
        if self.declared.get("experimentalApi"):
            kinds.add("currentTime/read")
        if not self.declared.get("requestAttestation"):
            kinds.discard("attestation/generate")
        return method in kinds

    def _reg(self, e, tid, event, to):
        frm = REGISTER_TRANSITIONS[tid]
        assert frm[0] == e.get("state") and frm[1] == event and frm[2] == to, (tid, e.get("state"), event)
        e["state"] = to
        self.register_transitions_used.add(tid)

    def _register(self, f):
        obj = f["obj"]
        p = obj.get("params") if isinstance(obj.get("params"), dict) else {}
        subj = {k2: p[k1] for k1, k2 in (("threadId", "thread"), ("turnId", "turn"),
                                         ("itemId", "item"), ("callId", "call")) if k1 in p}
        e = {"recordKind": "server-request-entry", "requestIdentity": obj["id"],
             "generation": f["generation"], "method": obj["method"], "subjectReferences": subj,
             "nativeParameters": obj.get("params"), "receiptPosition": f["position"],
             "replyWriteResult": "not-attempted",
             "acknowledgmentObservation": {"status": "not-observed"}}
        e["state"] = None
        self._reg(e, "RT-01", "server-request-received", "received")  # R1: before other handling
        self.register[(f["generation"], json.dumps(obj["id"]))] = e
        if not self._familiar(obj["method"]):
            e.update({"classification": "unfamiliar", "originClass": "none"})
            self._write_error(e, UNFAMILIAR_ERROR_CODE, "unfamiliar server request", "RT-02",
                              "classified-unfamiliar", {"class": "app-explicit-error"})
            return
        cls, origin = PARTITION[obj["method"]]
        e.update({"classification": cls, "originClass": origin})
        if cls == "known-app-unsupported":
            self._write_error(e, -32000, "not supported by this App (named rule)", "RT-03",
                              "classified-known-app-unsupported",
                              {"class": "app-rule", "ruleName": "unsupported-kind"})
            return
        self._reg(e, "RT-04", "classified-known-answerable", "outstanding")  # R3, R6

    def _write_error(self, e, code, message, tid, event, origin):
        content = {"code": code, "message": message}
        e["replyWriteResult"] = self.child.write({"jsonrpc": "2.0", "id": e["requestIdentity"],
                                                  "error": content})
        e["settlement"] = {"kind": "error", "nativeContent": content, "origin": origin}
        self._reg(e, tid, event, "errored")

    def answer(self, request_identity, native, origin, generation=None):
        """§6.4 answer operation. Returns 'accepted-for-write' or 'refused(<reason>)'."""
        if generation is not None and generation != self.generation_identity(self.generation):
            return "refused(generation-closed)"
        g = self.generation  # internal cache is scoped to this session/home only
        e = self.register.get((g, json.dumps(request_identity)))
        if e is None:
            return "refused(no-such-request)"
        refusal = None
        if e["generation"] != self.generation or self.state != "ready":
            refusal = "generation-closed"
        elif e["state"] == "resolved-by-supplier":
            refusal = "already-resolved"
        elif e["state"] != "outstanding":
            refusal = "already-settled"
        elif origin["class"] == "app-rule" and e["originClass"] in ("a14", "person-input") \
                and not is_negative(e["method"], native):
            refusal = "origin-not-permitted"  # R7, R9
        elif V.validate_against(native, self.root, RESPONSE_DEF[e["method"]]):
            refusal = "invalid-answer"  # R5: entry stays outstanding
        if refusal:
            if e["state"] == "outstanding":
                self._reg(e, "RT-05", "answer-refused", "outstanding")
            return "refused(%s)" % refusal
        self._reg(e, "RT-06", "answer-accepted-for-write", "settling")
        negative = is_negative(e["method"], native)
        e["settlement"] = {"kind": "decline" if negative else "answer", "nativeContent": native,
                           "origin": origin}
        e["replyWriteResult"] = self.child.write({"jsonrpc": "2.0", "id": request_identity,
                                                  "result": native})
        if e["replyWriteResult"] == "write-failed":
            self._reg(e, "RT-09", "reply-write-failed", "settle-write-failed")
        elif negative:
            self._reg(e, "RT-08", "reply-written-negative", "declined")
        else:
            self._reg(e, "RT-07", "reply-written-affirmative-or-content", "answered")
        return "accepted-for-write"

    # ---- notifications and §8.3 destination facts -------------------------
    def _observe_notification(self, f):
        obj = f["obj"]
        m, p = obj.get("method"), obj.get("params") or {}
        if m == "serverRequest/resolved":
            e = self.register.get((f["generation"], json.dumps(p.get("requestId"))))
            if e is None:
                return
            if e["state"] == "outstanding":
                e["supplierResolution"] = {"source": "serverRequest/resolved", "cause": None}
                self._reg(e, "RT-10", "supplier-reported-resolution", "resolved-by-supplier")
            elif e["state"] in ("answered", "declined"):
                tid = "RT-12" if e["state"] == "answered" else "RT-13"
                self._reg(e, tid, "supplier-reported-resolution", e["state"])
                e["acknowledgmentObservation"] = {"status": "observed",
                                                  "what": "serverRequest/resolved after the written reply"}
        elif m == "model/rerouted":
            t = self.destination["turns"].setdefault(p["turnId"], {"requested": None})
            t["effective"] = {"model": p["toModel"], "source": "model/rerouted",
                              "from": p["fromModel"], "position": f["position"]}

    def _observe_request(self, method, params, rid):
        if method == "thread/start":
            self.destination["thread"]["requested"] = {
                "provider": params.get("modelProvider"), "model": params.get("model")}
        if method == "turn/start":
            self.pending_turn_request[rid] = {"model": params.get("model"),
                                              "threadId": params.get("threadId")}

    def _observe_response(self, rec):
        res = rec.get("_result") or {}
        if rec["method"] == "thread/start":
            self.destination["thread"]["effective"] = {
                "provider": res.get("modelProvider"), "model": res.get("model"),
                "source": "thread/start response"}
        if rec["method"] == "turn/start":
            tid = res.get("turn", {}).get("id")
            t = self.destination["turns"].setdefault(tid, {})
            t["requested"] = self.pending_turn_request.pop(rec["requestIdentity"], None)

    def destination_facts(self):
        """Per turn: requested and effective kept apart; no report -> unknown."""
        out = {"thread": self.destination["thread"], "turns": {}}
        for tid, t in self.destination["turns"].items():
            out["turns"][tid] = {"requested": t.get("requested"),
                                 "effective": t.get("effective", "unknown")}
        return out

    # ---- records for S-7 --------------------------------------------------
    def records(self):
        out = [dict(event) for event in self.events]
        for rec in self.client.values():
            out.append({k: v for k, v in rec.items() if not k.startswith("_")})
        for e in self.register.values():
            out.append(dict(e))
        for rec in out:
            counter = rec.get("generation")
            rec["generation"] = None if counter is None else {"appSession": self.app_session,
                "home": self.home, "spawnCounter": counter}
        return out
