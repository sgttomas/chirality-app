#!/usr/bin/env python3
"""Opt-in stock 0.160.0 child carrier check; no credentials or model predictions.

Run on macOS with an already acquired supplier. Each case uses a new scratch
Codex home, and sandbox-exec denies every network destination except localhost.
The fixture emits one scripted spawn call, then returns HTTP400 to all requests.
This observes supplier carriage, not App integration, adoption or enforcement.
Decoded frames and requests remain private in the reported temporary directory.
"""
import argparse
import hashlib
import http.server
import json
import os
from pathlib import Path
import queue
import signal
import subprocess
import sys
import tempfile
import threading
import time

BINARY_SHA = "112fae7a5a1223e673c8a1791d32338f37df8b527ff1159bb8adac6c4dbf1b4b"
BASE_SHA = "e1bdd4f8f0df4b20f4a0ffc8a861ce819df45325d8cecdfb92e80379cf8d142e"
RESOURCES = Path(__file__).resolve().parents[1] / "src-tauri/resources/instructions"
DESCRIPTION = "Bounded TASK child with complete App guidance"
USER_DESCRIPTION = "Synthetic person-defined TASK; preserve this definition"


def sha(data):
    return hashlib.sha256(data).hexdigest()


def save(path, value):
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n")


def developer_texts(body):
    return [part["text"] for row in body["input"] if row["type"] == "message" and row["role"] == "developer"
            for part in row["content"] if isinstance(part.get("text"), str)]


def spawn_tool(body):
    tools = [tool for row in body["input"] if row["type"] == "additional_tools"
             for namespace in row["tools"] if namespace["name"] == "collaboration"
             for tool in namespace["tools"] if tool["name"] == "spawn_agent"]
    return tools[0] if tools else None


def role_description(body):
    tool = spawn_tool(body)
    return tool["parameters"]["properties"].get("agent_type", {}).get("description", "") if tool else ""


class Native:
    def __init__(self, binary, root, local_oss_port=None):
        self.frames, self.incoming, self.counter = [], queue.Queue(), 0
        env = {key: os.environ[key] for key in ("PATH", "HOME", "TMPDIR", "USER", "LOGNAME")
               if key in os.environ}
        env["CODEX_HOME"] = str(root / "home")
        if local_oss_port is not None:
            if not isinstance(local_oss_port, int) or not 1 <= local_oss_port <= 65535:
                raise ValueError("local OSS port must be an integer in 1..65535")
            env["CODEX_OSS_BASE_URL"] = f"http://127.0.0.1:{local_oss_port}/v1"
        self.stderr = (root / "stderr.log").open("w")
        self.process = subprocess.Popen(
            ["/usr/bin/sandbox-exec", "-f", str(root / "network.sb"), str(binary), "app-server"],
            cwd=root / "work", env=env, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
            stderr=self.stderr, text=True, start_new_session=True)

        def receive():
            for line in self.process.stdout:
                try:
                    self.incoming.put(json.loads(line))
                except ValueError:
                    self.incoming.put({"invalidOutput": line})
            self.incoming.put({"processEnded": True})
        self.reader = threading.Thread(target=receive, daemon=True)
        self.reader.start()

    def send(self, method, params, notification=False):
        self.counter += 1
        frame = {"method": method, "params": params}
        if not notification:
            frame["id"] = self.counter
        self.frames.append({"direction": "sent", "frame": frame})
        self.process.stdin.write(json.dumps(frame) + "\n")
        self.process.stdin.flush()
        if notification:
            return None
        deadline = time.monotonic() + 10
        while time.monotonic() < deadline:
            reply = self.incoming.get(timeout=max(.001, deadline - time.monotonic()))
            self.frames.append({"direction": "received", "frame": reply})
            if reply.get("processEnded"):
                raise RuntimeError("native process ended; inspect private stderr")
            if reply.get("id") == frame["id"]:
                if "error" in reply:
                    raise RuntimeError(f"{method} native error: {reply['error']}")
                return reply["result"]
        raise TimeoutError(method)

    def close(self):
        def stop_group(sig):
            try:
                os.killpg(self.process.pid, sig)
            except ProcessLookupError:
                pass
        try:
            self.process.stdin.close()
        except BrokenPipeError:
            pass
        # start_new_session makes this the fixture's own group. Stop that
        # group even if its leader exited while a descendant retained stdout.
        stop_group(signal.SIGTERM)
        self.reader.join(timeout=.5)
        # Keep the leader unreaped until the last group signal. Its allocated
        # PID prevents this PGID from being reused for an unrelated process.
        if self.reader.is_alive():
            stop_group(signal.SIGKILL)
        try:
            self.process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            # A timeout did not reap the leader; group ownership is retained.
            stop_group(signal.SIGKILL)
            self.process.wait(timeout=5)
        self.reader.join(timeout=1)
        self.stderr.close()
        if self.reader.is_alive():
            # Buffered stdout.close can wait for that reader's lock forever.
            raise RuntimeError("owned native output did not close within cleanup limit")
        self.process.stdout.close()


def run_case(binary, root, case, parent, task):
    root.mkdir()
    (root / "home").mkdir()
    (root / "work").mkdir()
    (root / "network.sb").write_text(
        '(version 1)\n(allow default)\n(deny network*)\n'
        '(allow network-outbound (remote ip "localhost:*"))\n'
        '(allow network-inbound (local ip "localhost:*"))\n')
    captures, lock = [], threading.Lock()
    spawning = case in ("none", "all")

    class Provider(http.server.BaseHTTPRequestHandler):
        def log_message(self, *args):
            pass

        def do_POST(self):
            self.connection.settimeout(5)
            size = int(self.headers["Content-Length"])
            if not 0 < size <= 2 * 1024 * 1024:
                self.send_error(413)
                return
            body = json.loads(self.rfile.read(size))
            with lock:
                captures.append({"path": self.path, "body": body})
                first = len(captures) == 1
            if spawning and first:
                item = {"id": "fc_fixture", "type": "function_call", "namespace": "collaboration",
                        "name": "spawn_agent", "call_id": "call_fixture_task", "status": "completed",
                        "arguments": json.dumps({"task_name": "fixture_child", "agent_type": "TASK",
                            "fork_turns": case, "message": "Synthetic bounded carrier check only."})}
                events = [
                    {"type": "response.created", "response": {"id": "resp_fixture", "status": "in_progress", "output": []}},
                    {"type": "response.output_item.added", "output_index": 0, "item": dict(item, status="in_progress")},
                    {"type": "response.output_item.done", "output_index": 0, "item": item},
                    {"type": "response.completed", "response": {"id": "resp_fixture", "status": "completed", "output": [item],
                        "usage": {"input_tokens": 0, "output_tokens": 0, "total_tokens": 0}}}]
                self.send_response(200)
                self.send_header("Content-Type", "text/event-stream")
                self.end_headers()
                for event in events:
                    self.wfile.write(("data: " + json.dumps(event) + "\n\n").encode())
            else:
                self.send_response(400)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(b'{"error":{"message":"capture-only fixture; no prediction"}}')

    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), Provider)
    server.daemon_threads = True
    worker = threading.Thread(target=server.serve_forever, daemon=True)
    worker.start()
    config = (f'model_provider = "fixture"\nmodel = "gpt-6.1-sol"\n'
              f'[model_providers.fixture]\nname = "Offline fixture"\n'
              f'base_url = "http://127.0.0.1:{server.server_port}/v1"\nwire_api = "responses"\n'
              '[features]\nplugins = false\n[analytics]\nenabled = false\n')
    role_file = root / "task.toml"
    if case != "missing":
        role_file.write_text("developer_instructions = [\n" if case == "invalid" else
                             "developer_instructions = " + json.dumps(task, ensure_ascii=False) + "\n")
    if case == "collision":
        (root / "user-task.toml").write_text('developer_instructions = "PERSON_DEFINED_TASK_MARKER"\n')
        config += (f'[agents.TASK]\ndescription = {json.dumps(USER_DESCRIPTION)}\n'
                   f'config_file = {json.dumps(str(root / "user-task.toml"))}\n')
    (root / "home/config.toml").write_text(config)
    native = None
    try:
        native = Native(binary, root)
        native.send("initialize", {"clientInfo": {"name": "child_carrier_fixture", "version": "0.0.0"},
                                   "capabilities": {"experimentalApi": True}})
        native.send("initialized", {}, notification=True)
        effective = native.send("config/read", {"includeLayers": True, "cwd": str(root / "work")})
        save(root / "effective-config.json", effective)
        roles = effective["config"]["agents"]
        if roles is not None and not isinstance(roles, dict):
            raise RuntimeError("native effective role configuration is unknown; no role override sent")
        overrides = {} if case == "baseline" or (isinstance(roles, dict) and "TASK" in roles) else {
            "agents.TASK.description": DESCRIPTION, "agents.TASK.config_file": str(role_file)}
        if case == "collision":
            assert isinstance(roles, dict) and "TASK" in roles, "native config did not expose person-defined TASK"
            assert not overrides, "fixture must withhold the colliding App name"
        started = native.send("thread/start", {"model": "gpt-6.1-sol", "modelProvider": "fixture",
            "cwd": str(root / "work"), "developerInstructions": parent, "config": overrides})
        thread = started["thread"]["id"]
        native.send("turn/start", {"threadId": thread, "input": [{"type": "text",
            "text": "Synthetic carrier check; only scripted fixture responses follow."}]})
        deadline, ended = time.monotonic() + 10, set()
        children = set()
        while time.monotonic() < deadline:
            frame = native.incoming.get(timeout=max(.001, deadline - time.monotonic()))
            native.frames.append({"direction": "received", "frame": frame})
            params, method = frame.get("params", {}), frame.get("method")
            item = params.get("item", {})
            if method == "item/completed" and item.get("type") == "subAgentActivity" and item.get("kind") == "started":
                children.add(item["agentThreadId"])
            if method == "turn/completed":
                ended.add(params["threadId"])
            if thread in ended and (not spawning or (len(children) == 1 and children <= ended)):
                break
        else:
            raise TimeoutError("fixture turns did not report completion")
        assert len(captures) == (3 if spawning else 1), "unexpected supplier request count"
        first = captures[0]["body"]
        assert parent in developer_texts(first), "complete parent composition not carried as developer guidance"
        assert sha(developer_texts(first)[0].encode()) == BASE_SHA, "native model template differs from selected reference"
        offered = role_description(first)
        if case in ("baseline", "missing", "invalid"):
            assert DESCRIPTION not in offered, "unavailable fixture role was advertised"
        elif case == "collision":
            assert USER_DESCRIPTION in offered and DESCRIPTION not in offered, "person-defined role was replaced"
        else:
            assert DESCRIPTION in offered, "per-thread custom role was not advertised"
        findings = {"case": case, "requests": len(captures), "nativeTemplate": BASE_SHA,
                    "customRoleOffered": DESCRIPTION in offered, "personRolePreserved": True if case == "collision" else None}
        if spawning:
            child = next(iter(children))
            received = native.send("thread/read", {"threadId": child, "includeTurns": True})
            save(root / "child-read.json", received)
            assert received["thread"]["agentRole"] == "TASK" and received["thread"]["parentThreadId"] == thread
            child_bodies = [c["body"] for c in captures if task in developer_texts(c["body"])]
            assert len(child_bodies) == 1, "exact child composition not observed once"
            child_body = child_bodies[0]
            assert parent not in developer_texts(child_body), "parent App composition replaced child role"
            assert sha(developer_texts(child_body)[0].encode()) == BASE_SHA, "child native template not preserved"
            assert spawn_tool(child_body) is not None, "child delegation tool unexpectedly absent"
            findings.update({"childMetadataMatched": True, "exactChildComposition": sha(task.encode()),
                             "childDelegationToolStillPresent": spawn_tool(child_body) is not None})
        return findings
    finally:
        try:
            if native is not None:
                native.close()
        finally:
            try:
                server.shutdown()
            finally:
                try:
                    server.server_close()
                finally:
                    worker.join(timeout=1)
                    try:
                        if native is not None:
                            save(root / "frames.json", native.frames)
                    finally:
                        save(root / "captures.json", captures)


def main():
    if not __debug__:
        raise RuntimeError("run this check without Python optimization; its evidence assertions are required")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--codex", type=Path, required=True, help="already acquired stock 0.160.0 macOS arm64 binary")
    args = parser.parse_args()
    binary = args.codex.resolve(strict=True)
    if sha(binary.read_bytes()) != BINARY_SHA:
        parser.error("binary is not the identified stock 0.160.0 arm64 input; nothing executed")
    common = (RESOURCES / "AGENTS.md").read_bytes()
    manager = (RESOURCES / "agents/AGENT_WORKING_ITEMS.md").read_bytes()
    executor = (RESOURCES / "agents/AGENT_TASK.md").read_bytes()
    parent = (common + b"\n\n# Active role: WORKING_ITEMS\n\n" + manager).decode()
    task = (common + b"\n\n# Active role: TASK\n\n" + executor).decode()
    root = Path(tempfile.mkdtemp(prefix="chirality-child-roles-", dir="/private/tmp"))
    report = {"format": "chirality.child-carrier-check/1", "binarySha256": BINARY_SHA,
              "checkerSha256": sha(Path(__file__).read_bytes()), "invocation": [sys.executable, *sys.argv],
              "sourceComponents": {"AGENTS.md": sha(common), "agents/AGENT_WORKING_ITEMS.md": sha(manager),
                                   "agents/AGENT_TASK.md": sha(executor)},
              "parentComposition": sha(parent.encode()), "childComposition": sha(task.encode()),
              "network": "OS sandbox allows localhost only", "modelPredictions": 0,
              "standing": "scripted stock-supplier carriage; not App integration, adoption, enforcement or qualification"}
    print(f"Private evidence: {root}", flush=True)
    report["cases"] = [run_case(binary, root / case, case, parent, task)
                       for case in ("baseline", "missing", "invalid", "collision", "none", "all")]
    report["evidenceFiles"] = {str(path.relative_to(root)): sha(path.read_bytes())
                             for path in sorted(root.rglob("*.json"))}
    save(root / "report.json", report)
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
