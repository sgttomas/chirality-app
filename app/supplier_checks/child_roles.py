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
import re
import signal
import subprocess
import sys
import tempfile
import threading
import time

BINARY_SHA = "112fae7a5a1223e673c8a1791d32338f37df8b527ff1159bb8adac6c4dbf1b4b"
BASE_SHA = "e1bdd4f8f0df4b20f4a0ffc8a861ce819df45325d8cecdfb92e80379cf8d142e"
RESOURCES = Path(__file__).resolve().parents[1] / "src-tauri/resources/instructions"
DESCRIPTION = "Chirality TASK: bounded work; does not delegate (stated, not enforced)"
USER_DESCRIPTION = "Synthetic person-defined TASK; preserve this definition"
STANDALONE_DESCRIPTION = "Synthetic standalone person-defined TASK; preserve this definition"
RUST_HELPER = None
ORIGIN_CASES = ("declared-alias", "project-nearest", "project-untrusted", "role-file-currentness")


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


def fixture_role_overrides(case, roles, role_file):
    """Fixture policy, not the App's still-unbuilt effective-name discovery.

    The standalone collision is known from this case's synthetic construction;
    config/read's null agents value does not establish that TASK is free.
    Other fresh cases retain the original controlled carrier setup.
    """
    if roles is not None and not isinstance(roles, dict):
        raise RuntimeError("native effective role configuration is unknown; no role override sent")
    if case in ("baseline", "standalone-collision", *ORIGIN_CASES) or (isinstance(roles, dict) and "TASK" in roles):
        return {}
    return {"agents.TASK.description": DESCRIPTION, "agents.TASK.config_file": str(role_file)}


def fixture_sandbox(binary):
    # main resolves and identifies this acquired executable before any case.
    # Permit only its exact path, including when acquired under /Users; this
    # does not admit sibling files or the supplier tree as a trusted input.
    return ('(version 1)\n(allow default)\n(deny network*)\n'
            '(allow network-outbound (remote ip "localhost:*"))\n'
            '(allow network-inbound (local ip "localhost:*"))\n'
            '(deny file-read* (subpath "/Users"))\n'
            f'(allow file-read* (literal {json.dumps(str(binary), ensure_ascii=False)}))\n')


def write_origin_role(path, name, description, guidance="Synthetic person fixture guidance"):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text('name = ' + json.dumps(name) + '\ndescription = ' + json.dumps(description) +
                    '\ndeveloper_instructions = ' + json.dumps(guidance) + '\n')


def prepare_origin_case(root, case):
    """Known synthetic inputs only; this does not discover the person's roles."""
    cwd, config = root / "work", ""
    expected, absent, changing = [], [], None
    if case == "declared-alias":
        named = root / "person-role.toml"
        write_origin_role(named, "TASK", "FILE_NAMED_TASK_DESCRIPTION")
        config += ('[agents.ALIAS]\ndescription = "TABLE_ALIAS_DESCRIPTION"\nconfig_file = ' +
                   json.dumps(str(named)) + '\n')
        write_origin_role(root / "home/agents/task.toml", "OTHER_ROLE", "FILENAME_IS_NOT_ROLE_NAME")
        write_origin_role(root / "home/agents/nested/deep.toml", "DEEP_ROLE", "RECURSIVE_ROLE_DESCRIPTION")
        write_origin_role(root / "home/agents/nested/conflict.toml", "TASK", "STANDALONE_TASK_SHADOWED")
        expected = [("TASK", "FILE_NAMED_TASK_DESCRIPTION"), ("OTHER_ROLE", "FILENAME_IS_NOT_ROLE_NAME"),
                    ("DEEP_ROLE", "RECURSIVE_ROLE_DESCRIPTION")]
        absent = ["TABLE_ALIAS_DESCRIPTION", "STANDALONE_TASK_SHADOWED"]
    elif case in ("project-nearest", "project-untrusted"):
        subprocess.run(["/usr/bin/git", "-c", "init.defaultBranch=main", "-c", "init.templateDir=", "init", str(cwd)],
                       check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE,
                       env={"PATH": "/usr/bin:/bin", "HOME": str(root / "os-home"),
                            "GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": "/dev/null"})
        write_origin_role(root / "home/agents/home.toml", "TASK", "HOME_TASK_DESCRIPTION")
        write_origin_role(cwd / ".codex/agents/root.toml", "TASK", "ROOT_TASK_DESCRIPTION")
        write_origin_role(cwd / "near/.codex/agents/near.toml", "TASK", "NEAR_TASK_DESCRIPTION")
        (cwd / "near/leaf").mkdir()
        trust = "trusted" if case == "project-nearest" else "untrusted"
        config += '[projects.' + json.dumps(str(cwd)) + ']\ntrust_level = ' + json.dumps(trust) + '\n'
        cwd = cwd / "near/leaf"
        expected = [("TASK", "NEAR_TASK_DESCRIPTION" if trust == "trusted" else "HOME_TASK_DESCRIPTION")]
        absent = ["HOME_TASK_DESCRIPTION", "ROOT_TASK_DESCRIPTION"] if trust == "trusted" else ["NEAR_TASK_DESCRIPTION", "ROOT_TASK_DESCRIPTION"]
    elif case == "role-file-currentness":
        changing = root / "home/agents/unrelated-filename.toml"
        write_origin_role(changing, "BEFORE_ROLE", "BEFORE_ROLE_DESCRIPTION", "Synthetic before guidance")
        expected, absent = [("TASK", "AFTER_TASK_DESCRIPTION")], ["BEFORE_ROLE_DESCRIPTION"]
    return cwd, config, expected, absent, changing


def assert_origin_catalog(catalog, pairs, absent):
    # Exact controlled 0.160.0 formatting, not a generic namespace parser.
    for name, description in pairs:
        pattern = rf"(?m)^{re.escape(name)}: \{{\n{re.escape(description)}\n\}}(?:\n|$)"
        assert re.search(pattern, catalog), "constructed native name/description association missing"
    assert all(marker not in catalog for marker in absent), "shadowed or disabled role definition retained"


def wait_origin_turn(native, thread):
    deadline = time.monotonic() + 10
    while time.monotonic() < deadline:
        frame = native.incoming.get(timeout=max(.001, deadline - time.monotonic()))
        native.frames.append({"direction": "received", "frame": frame})
        if frame.get("method") == "turn/completed" and frame.get("params", {}).get("threadId") == thread:
            return
    raise TimeoutError("origin fixture turn did not report completion")


def unchanged_config_reading(before, after):
    # Native object-key order is not stable. Compare every parsed field and
    # canonical JSON byte, retaining original snapshots/frames separately.
    canonical = lambda value: json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode()
    before_bytes, after_bytes = canonical(before), canonical(after)
    assert before == after and before_bytes == after_bytes, "config response unexpectedly reports standalone-file currency"
    return before_bytes


class Native:
    def __init__(self, binary, root, local_oss_port=None, discard_stderr=False):
        self.frames, self.incoming, self.counter = [], queue.Queue(), 0
        env = {key: os.environ[key] for key in ("PATH", "HOME", "TMPDIR", "USER", "LOGNAME")
               if key in os.environ}
        env["CODEX_HOME"] = str(root / "home")
        # Local child environment only; cold records-delivery reopen retains
        # its Codex home while using the same separate synthetic OS home.
        (root / "os-home").mkdir(exist_ok=True)
        env["HOME"] = str(root / "os-home")
        if local_oss_port is not None:
            if not isinstance(local_oss_port, int) or not 1 <= local_oss_port <= 65535:
                raise ValueError("local OSS port must be an integer in 1..65535")
            env["CODEX_OSS_BASE_URL"] = f"http://127.0.0.1:{local_oss_port}/v1"
        # Credential-carrier fixtures can discard diagnostics before transfer;
        # existing noncredential checks retain their private stderr unchanged.
        self.stderr = open(os.devnull, "w") if discard_stderr else (root / "stderr.log").open("w")
        self.process = subprocess.Popen(
            ["/usr/bin/sandbox-exec", "-f", str(root / "network.sb"), str(binary),
             "-c", 'cli_auth_credentials_store="file"', "app-server"],
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


def run_case(binary, root, case, parent, task, parent_role="WORKING_ITEMS", child_role="TASK"):
    root.mkdir()
    (root / "home").mkdir()
    (root / "os-home").mkdir()
    (root / "work").mkdir()
    (root / "network.sb").write_text(fixture_sandbox(binary))
    # Git/setup failures in new origin inputs occur before any provider starts.
    selected_cwd, origin_config, origin_expected, origin_absent, changing = prepare_origin_case(root, case)
    captures, lock = [], threading.Lock()
    spawning = case in ("none", "all", "linked-home") or case.startswith("matrix-")

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
                        "arguments": json.dumps({"task_name": "fixture_child", "agent_type": child_role,
                            "fork_turns": case if case in ("none", "all") else "none", "message": "Synthetic bounded carrier check only."})}
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
    standalone = None
    if case == "standalone-collision":
        (root / "home/agents").mkdir()
        standalone = root / "home/agents/task.toml"
        standalone.write_text('name = "TASK"\ndescription = ' + json.dumps(STANDALONE_DESCRIPTION) +
                              '\ndeveloper_instructions = "STANDALONE_PERSON_DEFINED_TASK_MARKER"\n')
    config += origin_config
    original_config = config.encode()
    original_standalone = standalone.read_bytes() if standalone is not None else None
    linked_target = None
    if case == "linked-home":
        linked_target = root / "shared/config.toml"
        linked_target.parent.mkdir()
        linked_target.write_text(config)
        (root / "home/config.toml").symlink_to(linked_target)
        # The config link grants no sibling agents/ sharing. The native role
        # roots remain relative to the reported CODEX_HOME user-layer file.
        write_origin_role(root / "shared/agents/task.toml", "TASK", "LINK_TARGET_SIBLING_MUST_NOT_BE_IMPORTED")
    else:
        (root / "home/config.toml").write_text(config)
    origin_sources = {path: path.read_bytes() for path in root.rglob("*.toml")} if case in ORIGIN_CASES else {}
    origin_reading = {}
    native = None
    try:
        native = Native(binary, root)
        native.send("initialize", {"clientInfo": {"name": "child_carrier_fixture", "version": "0.0.0"},
                                   "capabilities": {"experimentalApi": True}})
        native.send("initialized", {}, notification=True)
        effective = native.send("config/read", {"includeLayers": True, "cwd": str(selected_cwd)})
        save(root / "effective-config.json", effective)
        if changing is not None:
            before = native.send("thread/start", {"model": "gpt-6.1-sol", "modelProvider": "fixture",
                "cwd": str(selected_cwd), "developerInstructions": parent, "config": {}})["thread"]["id"]
            native.send("turn/start", {"threadId": before, "input": [{"type": "text", "text": "Synthetic before-change capture only."}]})
            wait_origin_turn(native, before)
            assert len(captures) == 1, "before-change catalog not captured exactly once"
            before_catalog = role_description(captures[0]["body"])
            assert_origin_catalog(before_catalog, [("BEFORE_ROLE", "BEFORE_ROLE_DESCRIPTION")], ["AFTER_TASK_DESCRIPTION"])
            assert all(path.read_bytes() == data for path, data in origin_sources.items()), "person fixture bytes changed before the intentional mutation"
            before_bytes = changing.read_bytes()
            write_origin_role(changing, "TASK", "AFTER_TASK_DESCRIPTION", "Synthetic after guidance")
            after_bytes = changing.read_bytes()
            assert before_bytes != after_bytes, "fixture did not change the role name/content"
            repeated = native.send("config/read", {"includeLayers": True, "cwd": str(selected_cwd)})
            save(root / "effective-config-after.json", repeated)
            canonical_reading = unchanged_config_reading(effective, repeated)
            (root / "effective-config-canonical.json").write_bytes(canonical_reading + b"\n")
            save(root / "role-file-change.json", {"actor": "synthetic fixture", "path": str(changing.relative_to(root)),
                "before": before_bytes.decode(), "after": after_bytes.decode(),
                "beforeSha256": sha(before_bytes), "afterSha256": sha(after_bytes)})
            origin_sources[changing] = after_bytes  # Only the fixture's intentional mutation.
            origin_reading.update({"sameConfigResponseAfterRoleChange": True, "nativeCatalogBeforeObserved": True,
                "beforeThreadId": before, "beforeRoleFileSha256": sha(before_bytes), "afterRoleFileSha256": sha(after_bytes),
                "fixtureRoleMutation": True, "beforeAndAfterSourceSnapshotsRetained": True,
                "canonicalConfigResponseSha256": sha(canonical_reading),
                "configReading": "complete parsed responses and canonical JSON equal; native key order is not wire-byte identity"})
        roles = effective["config"]["agents"]
        production = None
        if RUST_HELPER is not None and case not in ("baseline", "missing", "invalid"):
            save(root / "effective-current.json", effective)
            (root / "app-data").mkdir()
            command = [str(RUST_HELPER), str(root / "effective-current.json"), str(root / "instructions"), str(root / "app-data"), parent_role or "none"]
            if linked_target is not None:
                command += [str(root / "home/config.toml"), str(linked_target)]
            run = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            production = json.loads(run.stdout)
            save(root / "rust-preparation.json", production)
            assert production["parent"] == parent, "production Rust parent composition differs"
            for child in production["children"]:
                expected = (RESOURCES / "AGENTS.md").read_bytes() + ("\n\n# Active role: " + child["role"] + "\n\n").encode() + (RESOURCES / ("agents/AGENT_" + child["role"] + ".md")).read_bytes()
                assert child["text"].encode() == expected, "production Rust child composition differs"
            overrides = production["config"]
        else:
            overrides = fixture_role_overrides(case, roles, role_file)
        app_description = overrides.get("agents." + child_role + ".description", DESCRIPTION)
        if case == "collision":
            assert isinstance(roles, dict) and "TASK" in roles, "native config did not expose person-defined TASK"
            assert not overrides, "fixture must withhold the colliding App name"
        if case == "standalone-collision":
            assert roles is None, "counterexample requires agents:null, not an exposed config table"
            assert not overrides, "known standalone fixture collision must withhold every App child key"
        if case in ORIGIN_CASES:
            assert not overrides, "known origin collision must withhold every App child key"
            if case == "declared-alias":
                assert isinstance(roles, dict) and "ALIAS" in roles and "TASK" not in roles
            else:
                assert roles is None, "standalone origin control requires agents:null"
            if case in ("project-nearest", "project-untrusted"):
                project_layers = [row for row in effective["layers"] if row["name"]["type"] == "project"]
                assert len(project_layers) == 2, "selected cwd did not expose both constructed project layers"
                assert all(bool(row.get("disabledReason")) == (case == "project-untrusted") for row in project_layers)
        started = native.send("thread/start", {"model": "gpt-6.1-sol", "modelProvider": "fixture",
            "cwd": str(selected_cwd), "developerInstructions": parent, "config": overrides})
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
        assert len(captures) == (3 if spawning else 2 if changing is not None else 1), "unexpected supplier request count"
        first = captures[-1 if changing is not None else 0]["body"]
        assert parent in developer_texts(first), "complete parent composition not carried as developer guidance"
        assert sha(developer_texts(first)[0].encode()) == BASE_SHA, "native model template differs from selected reference"
        offered = role_description(first)
        if case in ("baseline", "missing", "invalid", "no-role"):
            assert app_description not in offered, "unavailable fixture role was advertised"
        elif case == "collision":
            assert USER_DESCRIPTION in offered and DESCRIPTION not in offered, "person-defined role was replaced"
        elif case == "standalone-collision":
            assert STANDALONE_DESCRIPTION in offered and DESCRIPTION not in offered, "standalone person-defined role was replaced or lost"
            assert (root / "home/config.toml").read_bytes() == original_config, "person configuration bytes changed"
            assert standalone.read_bytes() == original_standalone, "standalone person definition bytes changed"
            start_frames = [row["frame"] for row in native.frames if row["direction"] == "sent" and row["frame"].get("method") == "thread/start"]
            assert len(start_frames) == 1 and start_frames[0]["params"]["config"] == {}, "standalone negative sent App child keys"
        elif case in ORIGIN_CASES:
            assert_origin_catalog(offered, origin_expected, origin_absent)
            assert DESCRIPTION not in offered, "known origin fixture supplied an App child role"
            assert all(path.read_bytes() == data for path, data in origin_sources.items()), "person fixture bytes changed during native run"
            start_frames = [row["frame"] for row in native.frames if row["direction"] == "sent" and row["frame"].get("method") == "thread/start"]
            assert len(start_frames) == (2 if changing is not None else 1)
            assert all(row["params"]["config"] == {} and row["params"]["cwd"] == str(selected_cwd) for row in start_frames)
            for capture in captures:
                assert parent in developer_texts(capture["body"]), "origin control lost complete parent guidance"
                assert sha(developer_texts(capture["body"])[0].encode()) == BASE_SHA, "origin control changed native model template"
            origin_reading.update({"nativeCatalogAfterObserved": True, "selectedCwd": str(selected_cwd),
                "threadId": thread, "appChildKeysWithheldByFixture": True,
                "expectedNameDescriptions": dict(origin_expected), "absentDescriptions": origin_absent,
                "sourceFileSha256": {str(path.relative_to(root)): sha(data) for path, data in origin_sources.items()},
                "discoveryStanding": "known synthetic origins; not namespace completeness or App discovery"})
            if changing is None:
                origin_reading["originalDefinitionBytesRetained"] = True
            else:
                assert before != thread, "currency catalogs were not observed in separate starts of the same native source"
                origin_reading.update({"postMutationDefinitionBytesRetained": True, "otherDefinitionBytesUnchanged": True})
        else:
            assert app_description in offered, "per-thread custom role was not advertised"
        findings = {"case": case, "requests": len(captures), "nativeTemplate": BASE_SHA,
                    "customRoleOffered": app_description in offered, "personRolePreserved": True if changing is None and case in ("collision", "standalone-collision", *ORIGIN_CASES) else None}
        findings.update(origin_reading)
        findings["parentRole"] = parent_role
        findings["selectedChildRole"] = child_role if spawning else None
        if production is not None:
            assert_origin_catalog(offered, [(child["role"], production["config"]["agents." + child["role"] + ".description"]) for child in production["children"]], [])
        findings["preparationBasis"] = "production Rust namespace/composition/publication" if production is not None else "direct native negative/control fixture"
        if case == "linked-home":
            assert linked_target.read_bytes() == original_config
            assert (root / "home/config.toml").readlink() == linked_target
            assert "LINK_TARGET_SIBLING_MUST_NOT_BE_IMPORTED" not in offered
            findings["ownedConfigLinkRetained"] = True
            findings["linkTargetAgentsSiblingNotImported"] = True
        if case == "standalone-collision":
            findings.update({"effectiveAgentsNull": True, "standaloneDescriptionRetained": True,
                             "appChildKeysWithheldByFixture": True, "originalDefinitionBytesRetained": True,
                             "discoveryStanding": "known synthetic standalone collision; not generic App discovery"})
        if spawning:
            child = next(iter(children))
            received = native.send("thread/read", {"threadId": child, "includeTurns": True})
            save(root / "child-read.json", received)
            assert received["thread"]["agentRole"] == child_role and received["thread"]["parentThreadId"] == thread
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
    parser.add_argument("--rust-helper", type=Path, required=True, help="offline-built production child_role_boundary example")
    parser.add_argument("--matrix-only", action="store_true", help="only the additional standing-role and no-role consuming paths")
    args = parser.parse_args()
    global RUST_HELPER
    RUST_HELPER = args.rust_helper.resolve(strict=True)
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
              "checkerSha256": sha(Path(__file__).read_bytes()), "rustHelperSha256": sha(RUST_HELPER.read_bytes()), "invocation": [sys.executable, *sys.argv],
              "sourceComponents": {"AGENTS.md": sha(common), "agents/AGENT_WORKING_ITEMS.md": sha(manager),
                                   "agents/AGENT_TASK.md": sha(executor)},
              "parentComposition": sha(parent.encode()), "childComposition": sha(task.encode()),
              "network": "OS sandbox allows localhost only", "modelPredictions": 0,
              "standing": "production Rust preparation and scripted stock-supplier carriage; private App Host custody tested separately; no adoption, enforcement or qualification"}
    print(f"Private evidence: {root}", flush=True)
    report["cases"] = [] if args.matrix_only else [run_case(binary, root / case, case, parent, task)
                       for case in ("baseline", "missing", "invalid", "collision", "standalone-collision", "none", "all", "linked-home", *ORIGIN_CASES)]
    for parent_role, child_role in (("HELP_HUMAN", "HELPS_HUMANS"), ("HELP_HUMAN", "WORKING_ITEMS"), ("HELP_HUMAN", "TASK"), ("HELPS_HUMANS", "TASK")):
        case = "matrix-" + parent_role + "-" + child_role
        parent_bytes = (common + ("\n\n# Active role: " + parent_role + "\n\n").encode() + (RESOURCES / ("agents/AGENT_" + parent_role + ".md")).read_bytes()).decode()
        child_bytes = (common + ("\n\n# Active role: " + child_role + "\n\n").encode() + (RESOURCES / ("agents/AGENT_" + child_role + ".md")).read_bytes()).decode()
        report["cases"].append(run_case(binary, root / case, case, parent_bytes, child_bytes, parent_role, child_role))
    report["cases"].append(run_case(binary, root / "no-role", "no-role", common.decode(), task, None))
    report["rustProductionSources"] = {name: sha((RESOURCES.parents[1] / "src" / name).read_bytes()) for name in ("child_roles.rs", "role_supply.rs", "role_lifecycle.rs", "runtime_session.rs", "access_provider.rs")}
    report["evidenceFiles"] = {str(path.relative_to(root)): sha(path.read_bytes())
                             for path in sorted(root.rglob("*.json"))}
    save(root / "report.json", report)
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
