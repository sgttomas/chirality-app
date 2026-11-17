#!/usr/bin/env python3
"""Bounded st5/nv04 pipe recordings for a separately approved supplier launch.

This is a scripted client, not the App or a qualification check. It runs only
invented exchanges against a loopback provider. It reads no process arguments,
environment, open files or sockets. Network contacts are NOT observed here.
Required replies and scenario events are checked; retained frames still require
an independent reading. No absence beyond the recorded interval is inferred.
The historical recording files and their stated limitations are untouched.
"""
import argparse
import datetime
import json
import os
from pathlib import Path
import selectors
import signal
import socket
import subprocess
import time

import intake
import recording_provider as provider

CLIENT = {"name": "chirality-st5-harness", "title": "Chirality ST-5 capture harness", "version": "0.0.0-st5"}
CAPABILITIES = {"experimentalApi": True, "requestAttestation": False}
CHILD_PROMPT = "st5-child-brief-marker: count the invented files."
COMMAND = "mkdir st5-marker-pump-skid"
STEP_SECONDS = 60


class Refused(Exception):
    pass


def require(condition, reason):
    if not condition:
        raise Refused(reason)


def stop_group(process):
    """Signal only the session/group this recorder created, then reap its child."""
    try:
        os.killpg(process.pid, signal.SIGKILL)
    except ProcessLookupError:
        pass
    except PermissionError:
        # macOS can report EPERM for an exited, unreaped group leader. Reap our own
        # child, then require ESRCH from the group check; EPERM itself proves nothing.
        process.wait(timeout=10)
        try:
            os.killpg(process.pid, 0)
        except ProcessLookupError:
            return
        raise Refused("owned process group remains or its termination cannot be established") from None
    process.wait(timeout=10)


def names(body):
    result = []
    for tool in body.get("tools", []):
        if tool.get("type") == "namespace":
            result.extend((tool.get("name"), item.get("name")) for item in tool.get("tools", []))
        else:
            result.append((None, tool.get("name")))
    return result


def script(scenario):
    spawned = False

    def plan(index, body):
        nonlocal spawned
        require(isinstance(body, dict), "provider request is not an object")
        outputs = any(item.get("type", "").endswith("_output") for item in body.get("input", []) if isinstance(item, dict))
        if scenario == "nv04" and spawned and CHILD_PROMPT in json.dumps(body) and not outputs:
            return [provider.message("Child finished counting.", "msg_child")], 8, "child held"
        if outputs:
            return [provider.message("Parent turn done; child still working." if scenario == "nv04" else "Done.", "msg_done")], 0, "final message"
        available = names(body)
        if scenario == "nv04":
            selected = next(((space, name) for space, name in available if name == "spawn_agent"), None)
            require(selected is not None and not spawned, "one native spawn tool required")
            spawned = True
            space, name = selected
            item = {"type": "function_call", "name": name, "call_id": "call_spawn_1", "id": "fc_spawn_1",
                    "arguments": json.dumps({"message": CHILD_PROMPT, "task_name": "count_files"})}
            if space:
                item["namespace"] = space
            return [item], 0, "spawn call"
        selected = next(((space, name) for space, name in available if name == "exec_command"), None)
        require(selected is not None, "native exec_command tool required; no alternative command is invented")
        space, name = selected
        item = {"type": "function_call", "name": name, "call_id": "call_st5_1", "id": "fc_st5_1",
                "arguments": json.dumps({"cmd": COMMAND, "workdir": None, "sandbox_permissions": "require_escalated",
                                         "justification": "Create the invented marker folder."})}
        if space:
            item["namespace"] = space
        return [item], 0, "shell call"

    return plan


class Pipe:
    def __init__(self, run, generation):
        self.run, self.number = run, generation
        binary, _ = intake.verified_vendor(str(run.vendor), run.record)
        intake.outside_configuration(str(run.work))
        self.process = subprocess.Popen([binary, "app-server"], cwd=run.work, env=run.environment,
                                        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
                                        start_new_session=True, bufsize=0)
        self.selector = selectors.DefaultSelector()
        os.set_blocking(self.process.stdout.fileno(), False)
        self.selector.register(self.process.stdout, selectors.EVENT_READ)
        self.buffer, self.eof, self.next_id, self.closed = b"", False, 0, False
        self.received, self.requests, self.answered = [], {}, set()
        run.pipes.append(self)

    def send(self, frame):
        raw = (json.dumps(frame, separators=(",", ":")) + "\n").encode()
        sent = 0
        while sent < len(raw):
            wrote = os.write(self.process.stdin.fileno(), raw[sent:])
            require(wrote > 0, "pipe write made no progress")
            sent += wrote
        self.run.frame(self.number, "app->codex", frame)

    def pump(self, wait):
        for key, _ in self.selector.select(wait):
            block = os.read(key.fd, 65536)
            if not block:
                self.eof = True
                self.selector.unregister(key.fileobj)
                require(not self.buffer, "supplier closed stdout with an incomplete frame")
                continue
            self.buffer += block
            require(len(self.buffer) <= 32 * 1024 * 1024, "supplier frame exceeds recorder bound")
            while b"\n" in self.buffer:
                raw, self.buffer = self.buffer.split(b"\n", 1)
                value = json.loads(raw)
                require(isinstance(value, dict), "supplier output is not a JSON object")
                if "id" in value and "method" not in value:
                    identity = json.dumps(value["id"], sort_keys=True)
                    require(identity in self.requests and identity not in self.answered, "unmatched or duplicate supplier reply")
                    self.answered.add(identity)
                self.received.append(value)
                self.run.frame(self.number, "codex->app", value)

    def until(self, predicate, seconds=STEP_SECONDS):
        end = time.monotonic() + seconds
        while True:
            value = predicate()
            if value is not None:
                return value
            require(not self.eof, "supplier stdout ended before the required observation")
            require(time.monotonic() < end, "required observation timed out")
            self.pump(min(0.1, max(0, end - time.monotonic())))

    def request(self, method, params, wait=True):
        self.next_id += 1
        identity = self.next_id
        self.requests[json.dumps(identity)] = method
        self.send({"jsonrpc": "2.0", "id": identity, "method": method, "params": params})
        if not wait:
            return None
        reply = self.until(lambda: next((f for f in self.received if f.get("id") == identity and "method" not in f), None))
        require("result" in reply and "error" not in reply, method + " did not return a result")
        return reply["result"]

    def initialize(self):
        result = self.request("initialize", {"clientInfo": CLIENT, "capabilities": CAPABILITIES})
        self.send({"jsonrpc": "2.0", "method": "initialized", "params": {}})
        return result

    def end(self, killed=False):
        if killed:
            stop_group(self.process)
        else:
            self.process.stdin.close()
        end = time.monotonic() + 10
        while not self.eof or self.process.poll() is None:
            if time.monotonic() >= end:
                stop_group(self.process)
                raise Refused("supplier did not close and drain within the end interval")
            self.pump(0.1)
        if not killed:
            require(self.process.returncode == 0, "supplier's graceful exit was nonzero")
        # No command-line/process inspection. Kill any remaining members of this owned group.
        if not killed:
            stop_group(self.process)
        self.closed = True
        self.selector.close()
        self.process.stdout.close()
        if not self.process.stdin.closed:
            self.process.stdin.close()


class Run:
    def __init__(self, vendor, record, root, scenario, port):
        self.vendor, self.record, self.root = Path(vendor), record, Path(root)
        require(self.root.is_absolute() and os.path.realpath(self.root) == str(self.root), "run root must be a plain absolute path")
        self.root.mkdir(mode=0o700)  # new; never reuse a run home
        self.work = self.root / "workspace"
        for name in ("workspace", "user-home", "home", "tmp"):
            (self.root / name).mkdir(mode=0o700)
        binary, path = intake.verified_vendor(str(self.vendor), record)
        self.binary = binary
        self.outside = intake.outside_configuration(str(self.work))
        self.environment = intake.supplier_environment(path, str(self.vendor), *(str(self.root / n) for n in ("user-home", "home", "tmp")))
        # Proxy controls are not isolation and are not a contact observation.
        for name in ("HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "http_proxy", "https_proxy", "all_proxy"):
            self.environment[name] = "http://127.0.0.1:9"
        self.environment.update(NO_PROXY="127.0.0.1,localhost,::1", no_proxy="127.0.0.1,localhost,::1")
        approval = "on-request" if scenario == "st5" else "never"
        (self.root / "home/config.toml").write_text(
            f'model_provider = "st5_stub"\nmodel = "{provider.MODEL}"\napproval_policy = "{approval}"\n'
            'sandbox_mode = "read-only"\nallow_login_shell = false\n'
            f'[model_providers.st5_stub]\nname = "Invented loopback provider"\nbase_url = "http://127.0.0.1:{port}/v1"\nwire_api = "responses"\n'
            '[features]\nplugins = false\nshell_snapshot = false\n[analytics]\nenabled = false\n')
        self.started, self.frames, self.events, self.pipes = time.monotonic(), [], [], []
        self.positions, self.provider_log = {}, []
        self.provider = provider.Provider(script(scenario), self.provider_log, port=port)
        self.event("begin", pin=record["pin"], scenario=scenario)

    def version(self):
        binary, _ = intake.verified_vendor(str(self.vendor), self.record)
        intake.outside_configuration(str(self.work))
        process = subprocess.Popen([binary, "--version"], cwd=self.work, env=self.environment,
                                   stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                   start_new_session=True)
        try:
            output, error = process.communicate(timeout=15)
            require(process.returncode == 0 and not error and output.decode().strip() == "codex-cli " + self.record["pin"],
                    "version probe did not return the pinned label without a diagnostic")
            self.version_output = output.decode().strip()
        finally:
            stop_group(process)

    def event(self, event, **fields):
        self.events.append({"event": event, "t_ms": int((time.monotonic() - self.started) * 1000), **fields})

    def frame(self, generation, direction, frame):
        require(len(self.frames) < 20000, "frame count exceeds recorder bound")
        key = generation, direction
        self.positions[key] = self.positions.get(key, 0) + 1
        self.frames.append({"generation": generation, "direction": direction, "position": self.positions[key],
                            "t_ms": int((time.monotonic() - self.started) * 1000), "frame": frame})

    def close(self):
        failures = []
        for pipe in self.pipes:
            if pipe.closed:
                continue
            try:
                stop_group(pipe.process)
            except Exception as error:
                failures.append(type(error).__name__)
        if not self.provider.close(timeout=15):
            failures.append("provider did not drain")
        require(not failures, "cleanup incomplete: " + ", ".join(failures))


def histories(pipe, parent, turn, child):
    pipe.request("thread/read", {"threadId": parent, "includeTurns": True})
    pipe.request("thread/turns/list", {"threadId": parent, "itemsView": "full"})
    pipe.request("thread/items/list", {"threadId": parent, "turnId": turn})
    pipe.request("thread/read", {"threadId": child, "includeTurns": True})


def scenario(run, kind):
    first = Pipe(run, 1)
    first.initialize()
    parent = first.request("thread/start", {"cwd": str(run.work), "approvalPolicy": "on-request" if kind == "st5" else "never", "sandbox": "read-only"})["thread"]["id"]
    turn = first.request("turn/start", {"threadId": parent, "input": [{"type": "text", "text": "Create the marker folder for the invented pump-skid example." if kind == "st5" else "Delegate the count."}]})["turn"]["id"]
    if kind == "st5":
        request = first.until(lambda: next((f for f in first.received if f.get("method") == "item/commandExecution/requestApproval" and "id" in f), None))
        run.event("server-request-received", generation=1, method=request["method"])
        os.killpg(first.process.pid, signal.SIGSTOP)
        end = time.monotonic() + 5
        while True:
            pid, status = os.waitpid(first.process.pid, os.WUNTRACED | os.WNOHANG)
            if pid:
                require(os.WIFSTOPPED(status), "supplier did not stop before the answer")
                break
            require(time.monotonic() < end, "supplier stop was not observed")
            time.sleep(0.01)
        run.event("process-group-frozen", generation=1, signal="SIGSTOP")
        first.send({"jsonrpc": "2.0", "id": request["id"], "result": {"decision": "accept"}})
        run.event("answer-written", generation=1, decision="accept", origin="scripted capture; not a person's act")
        first.request("thread/turns/list", {"threadId": parent, "limit": 1}, wait=False)
        first.end(killed=True)
        run.event("process-group-killed-while-frozen", generation=1, signal="SIGKILL")
        second = Pipe(run, 2)
        second.initialize()
        second.request("thread/read", {"threadId": parent, "includeTurns": True})
        second.request("thread/turns/list", {"threadId": parent, "itemsView": "full"})
        second.request("thread/loaded/list", {})
        second.request("thread/resume", {"threadId": parent})
        second.end()
    else:
        completed = lambda thread: next((f for f in first.received if f.get("method") == "turn/completed" and f["params"].get("threadId") == thread), None)
        parent_done = first.until(lambda: completed(parent))
        spawned = [f["params"]["item"] for f in first.received if f.get("method") == "item/completed" and f["params"]["item"].get("type") == "collabAgentToolCall"]
        require(len(spawned) == 1 and len(spawned[0].get("receiverThreadIds", [])) == 1, "one completed spawn required")
        child = spawned[0]["receiverThreadIds"][0]
        require(child != parent, "spawned child equals parent")
        child_done = first.until(lambda: completed(child))
        require(first.received.index(parent_done) < first.received.index(child_done), "parent did not finish before child")
        first.request("thread/loaded/list", {})
        histories(first, parent, turn, child)
        first.end()
        second = Pipe(run, 2)
        second.initialize()
        histories(second, parent, turn, child)
        second.end()


def redacted_record(run, kind):
    replacements = [(str(run.root / "home"), "<HOME>"), (str(run.work), "<WORKSPACE>"), (str(run.root), "<SCRATCH>"),
                    (str(run.vendor), "<VENDOR>"), (socket.gethostname(), "<HOST>")]
    keys = {"userAgent", "installationId", "serverName", "userId", "accountId", "apiKey", "accessToken", "loginId", "userCode", "authUrl", "verificationUrl"}
    def redact(value, key=None):
        if key in keys:
            return "<REDACTED-IDENTITY>"
        if isinstance(value, dict):
            return {k: redact(v, k) for k, v in value.items()}
        if isinstance(value, list):
            return [redact(v) for v in value]
        if isinstance(value, str):
            for old, new in replacements:
                value = value.replace(old, new)
        return value
    frames = []
    for row in run.frames:
        frame = redact(row["frame"])
        frames.append({**row, "frame": frame, "redacted": frame != row["frame"]})
    value = {"format": "chirality.app-v4.supplier-capture.v2", "pin": run.record["pin"], "scenario": kind,
             "date": datetime.datetime.now(datetime.timezone.utc).date().isoformat(), "app_candidate": None,
             "version_identity": {"version_output": run.version_output, "binary_sha256": intake.sha256_file(run.binary),
                                  "distribution": {"archive_sha256": run.record["archive"]["sha256"], "inventory_manifest_sha256": run.record["inventory"]["manifest_sha256"]}},
             "frames": frames, "events": redact(run.events), "provider": {"requests": run.provider_log},
             "settings_supplied": {"environment": sorted(run.environment), "features.shell_snapshot": False, "allow_login_shell": False,
                                   "features.plugins": False, "analytics.enabled": False, "outside_configuration": run.outside},
             "socket_watch": {"observed": False, "reason": "this route reads no process sockets; proxy controls are not isolation"},
             "limits": ["Scripted capture, not App behavior or qualification.", "Settings supplied are not settings read back.",
                        "No contact observation or sign-in; no absence beyond the recorded interval is inferred.",
                        "Redacted frames do not claim original byte identity; independent content reading remains required."]}
    text = json.dumps(value, indent=1, ensure_ascii=False) + "\n"
    require(not any(s in text for s in ("/Users/", "/private/", "/var/folders/", "/home/")), "local path remains; no recording written")
    return text


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--vendor", required=True)
    parser.add_argument("--record", required=True)
    parser.add_argument("--run-root", required=True)
    parser.add_argument("--port", required=True, type=int)
    parser.add_argument("scenario", choices=("st5", "nv04"))
    args = parser.parse_args()
    record = json.loads(Path(args.record).read_bytes())
    facts = intake.PINS[record["pin"]]
    require(record["archive"] == {k: facts[k] for k in ("url", "size", "sha256")} and record["source_commit"] == facts["source_commit"], "record does not name the admitted archive")
    run = Run(args.vendor, record, args.run_root, args.scenario, args.port)
    try:
        run.version()
        scenario(run, args.scenario)
    finally:
        run.close()
    text = redacted_record(run, args.scenario)
    output = run.root / (args.scenario + ".recording.json")
    with output.open("x") as handle:
        handle.write(text)
    print(json.dumps({"recording": str(output), "sha256": intake.sha256_file(output), "frames": len(run.frames)}))


if __name__ == "__main__":
    try:
        main()
    except (Refused, intake.Refused, OSError, ValueError, KeyError, subprocess.TimeoutExpired) as error:
        raise SystemExit("recording refused: " + str(error)) from None
