#!/usr/bin/env python3
"""Opt-in stock 0.160.0 records-tool carriage check, with invented providers.

The provider captures declarations and returns HTTP400; it makes no prediction.
Homes are fresh, the environment excludes credentials, and the native process
is restricted to localhost by the maintained Native helper's OS sandbox.
"""
import argparse
import copy
import hashlib
import http.server
import json
from pathlib import Path
import tempfile
import threading
import time

from child_roles import BINARY_SHA, Native, save

DEFAULT_MODEL = "gpt-6.1-sol"
FLAT_MODEL = "gpt-5.5"


def sha_file(path):
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(65536), b""):
            h.update(block)
    return h.hexdigest()


def named_tools(body, definition):
    name = definition["name"]
    schema = definition["inputSchema"]
    fields = []
    for key, prop in sorted(schema["properties"].items()):
        kind = prop["type"]
        if kind == "string":
            rendered = " | ".join(json.dumps(v) for v in prop["enum"]) if "enum" in prop else "string"
        elif kind == "integer":
            rendered = "number"
        else:
            raise ValueError("records check needs an updated declaration renderer for this schema")
        optional = "" if key in schema["required"] else "?"
        fields.append(f"{key}{optional}: {rendered};")
    declaration = f"declare const tools: {{ {name}(args: {{ {' '.join(fields)} }}): Promise<unknown>; }};"
    section = f"### `{name}`\n{definition['description']}\n\nexec tool declaration:\n```ts\n{declaration}\n```"
    # The observed stock flat renderer omits these scalar bounds. Match that
    # specific projection, retaining all other schema fields; this establishes
    # declaration carriage, not transmission or enforcement of omitted bounds.
    flat_schema = copy.deepcopy(schema)
    for prop in flat_schema["properties"].values():
        omitted = {"string": ("minLength", "maxLength"), "integer": ("minimum", "maximum")}.get(prop["type"], ())
        for key in omitted:
            prop.pop(key, None)
    found = []
    def walk(value, path, namespace=None):
        if isinstance(value, dict):
            if (value.get("type") == "function" and value.get("name") == name
                    and value.get("description") == definition["description"]):
                parameters = value.get("parameters", value.get("inputSchema"))
                if parameters == schema or parameters == flat_schema:
                    found.append({"representation": "function", "path": path, "tool": value,
                        "schemaRendering": "exact" if parameters == schema else "stock-scalar-projection"})
            if (namespace == "functions" and value.get("type") == "custom" and value.get("name") == "exec"
                    and isinstance(value.get("description"), str)):
                text = value["description"]
                if text.count(section) == 1:
                    found.append({"representation": "code-exec", "path": path + ["description"], "declaration": declaration})
            if value.get("type") == "namespace":
                walk(value.get("tools", []), path + ["tools"], value.get("name"))
        elif isinstance(value, list):
            for index, child in enumerate(value):
                walk(child, path + [index], namespace)
    walk(body.get("tools", []), ["tools"])
    for i, row in enumerate(body.get("input", [])):
        if isinstance(row, dict) and row.get("type") == "additional_tools":
            walk(row.get("tools", []), ["input", i, "tools"])
    return found


def reported_route(config, capabilities, model, provider):
    effective = config.get("config", {})
    if effective.get("model") != model or effective.get("model_provider") != provider:
        raise RuntimeError("effective model/provider did not match the scripted route")
    namespace_tools = capabilities.get("namespaceTools")
    if not isinstance(namespace_tools, bool):
        raise RuntimeError("supplier did not report boolean namespaceTools capability")
    return {"model": model, "providerId": provider, "namespaceTools": namespace_tools}


def run_case(binary, root, definition, provider, model=DEFAULT_MODEL, representation="code-exec"):
    root.mkdir()
    (root / "home").mkdir()
    (root / "work").mkdir()
    (root / "network.sb").write_text('(version 1)\n(allow default)\n(deny network*)\n'
        '(allow network-outbound (remote ip "localhost:*"))\n'
        '(allow network-inbound (local ip "localhost:*"))\n')
    captures, lock = [], threading.Lock()

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
                captures.append(body)
            self.send_response(400)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(b'{"error":{"message":"capture-only fixture; no prediction"}}')

    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), Provider)
    server.daemon_threads = True
    worker = threading.Thread(target=server.serve_forever, daemon=True)
    worker.start()
    provider_config = (f'[model_providers.{provider}]\nname = "Invented records provider"\n'
        f'base_url = "http://127.0.0.1:{server.server_port}/v1"\nwire_api = "responses"\n') if provider == "fixture" else ""
    config_text = (
        f'model_provider = "{provider}"\nmodel = "{model}"\n'
        + provider_config +
        '[features]\nplugins = false\n[analytics]\nenabled = false\n')
    native, all_frames = None, []
    def open_native():
        n = Native(binary, root, local_oss_port=server.server_port if provider == "lmstudio" else None)
        try:
            n.send("initialize", {"clientInfo": {"name":"records_delivery_fixture", "version":"0.0.0"}, "capabilities":{"experimentalApi": True}})
            n.send("initialized", {}, notification=True)
        except BaseException:
            try:
                n.close()
            finally:
                all_frames.extend(n.frames)
            raise
        return n
    def turn(label, thread, expected=True):
        before = len(captures)
        frame_start = len(native.frames)
        started_turn = native.send("turn/start", {"threadId":thread, "input":[{"type":"text", "text":"Invented records-tool delivery check; no model prediction."}]})
        turn_id = started_turn["turn"]["id"]
        backlog = [row["frame"] for row in native.frames[frame_start:] if row["direction"] == "received"]
        deadline = time.monotonic() + 15
        while time.monotonic() < deadline:
            if backlog:
                frame = backlog.pop(0)
            else:
                frame = native.incoming.get(timeout=max(.001, deadline - time.monotonic()))
                native.frames.append({"direction":"received", "frame":frame})
            if frame.get("processEnded"):
                raise RuntimeError(f"{label}: native process ended; inspect private stderr")
            params = frame.get("params", {})
            if (frame.get("method") == "turn/completed" and params.get("threadId") == thread
                    and params.get("turn", {}).get("id") == turn_id):
                if (params["turn"].get("status") != "failed"
                        or "capture-only fixture; no prediction" not in params["turn"].get("error", {}).get("message", "")):
                    raise RuntimeError(f"{label}: turn did not end with the fixture refusal")
                break
        else:
            raise TimeoutError(label)
        if len(captures) != before + 1:
            raise RuntimeError(f"{label}: unexpected provider request count")
        metadata = captures[-1].get("client_metadata", {})
        if metadata.get("thread_id") != thread or metadata.get("turn_id") != turn_id:
            raise RuntimeError(f"{label}: captured request identity did not match the turn")
        if captures[-1].get("model") != model:
            raise RuntimeError(f"{label}: captured request did not use the selected model")
        found = named_tools(captures[-1], definition)
        if len(found) != (1 if expected else 0):
            raise RuntimeError(f"{label}: expected {int(expected)} capability declaration, found {len(found)}")
        if expected and found[0]["representation"] != representation:
            raise RuntimeError(f"{label}: expected {representation} declaration, found {found[0]['representation']}")
        return {"step":label, "threadId":thread, "turnId":turn_id, "requestOrdinal":before + 1,
            "offered":bool(found), "definitions":found}
    def fork(thread):
        result = native.send("thread/fork", {"threadId":thread, "deferGoalContinuation":True})["thread"]
        if result["id"] == thread or result.get("forkedFromId") != thread:
            raise RuntimeError("fork reply did not identify a new copy of the source thread")
        return result["id"]
    def check_start(result):
        if result.get("model") != model or result.get("modelProvider") != provider:
            raise RuntimeError("thread/start reply did not identify the scripted model/provider")
        return result
    try:
        (root / "home/config.toml").write_text(config_text)
        native = open_native()
        config = native.send("config/read", {"includeLayers":True, "cwd":str(root / "work")})
        save(root / "effective-config.json", config)
        capabilities = native.send("modelProvider/capabilities/read", {})
        save(root / "capabilities.json", capabilities)
        route = reported_route(config, capabilities, model, provider)
        catalog = native.send("model/list", {"includeHidden":True})
        save(root / "catalog.json", catalog)
        if not any(row.get("model") == model for row in catalog.get("data", [])):
            raise RuntimeError("scripted model was not reported by the supplier catalogue")
        control = check_start(native.send("thread/start", {"model":model, "modelProvider":provider, "cwd":str(root / "work")}))
        results = [turn("unoffered-before", control["thread"]["id"], False)]
        started = check_start(native.send("thread/start", {"model":model, "modelProvider":provider, "cwd":str(root / "work"), "dynamicTools":[definition]}))
        thread = started["thread"]["id"]
        results.append(turn("start", thread))
        native.send("thread/resume", {"threadId":thread})
        results.append(turn("resume-hot", thread))
        results.append(turn("fork-hot", fork(thread)))
        ended, native = native, None
        try:
            ended.close()
        finally:
            all_frames.extend(ended.frames)
        (root / "stderr.log").rename(root / "stderr-hot.log")
        native = open_native()
        cold_config = native.send("config/read", {"includeLayers":True, "cwd":str(root / "work")})
        save(root / "effective-config-cold.json", cold_config)
        cold_capabilities = native.send("modelProvider/capabilities/read", {})
        save(root / "capabilities-cold.json", cold_capabilities)
        cold_route = reported_route(cold_config, cold_capabilities, model, provider)
        if cold_route != route:
            raise RuntimeError("reported route changed across supplier restart")
        native.send("thread/resume", {"threadId":thread})
        results.append(turn("resume-cold", thread))
        results.append(turn("fork-cold", fork(thread)))
        native.send("thread/resume", {"threadId":control["thread"]["id"]})
        results.append(turn("unoffered-after-cold", control["thread"]["id"], False))
        return {**route, "capabilities":capabilities, "coldCapabilities":cold_capabilities,
            "expectedRepresentation":representation, "steps":results}
    finally:
        try:
            if native is not None:
                ended, native = native, None
                try:
                    ended.close()
                finally:
                    all_frames.extend(ended.frames)
        finally:
            server.shutdown()
            server.server_close()
            worker.join(timeout=1)
            save(root / "frames.json", all_frames)
            save(root / "captures.json", captures)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--codex", required=True, type=Path)
    parser.add_argument("--definition", required=True, type=Path, help="JSON emitted by records_tool_definition")
    parser.add_argument("--include-flat-model", action="store_true",
        help="also check supported gpt-5.5 flat function rendering; reported namespaceTools remains separate")
    args = parser.parse_args()
    binary = args.codex.resolve(strict=True)
    if sha_file(binary) != BINARY_SHA:
        parser.error("not the identified stock 0.160.0 macOS arm64 binary")
    definition = json.loads(args.definition.read_text())
    if definition.get("type") != "function" or definition.get("name") != "chirality_records_read_v1":
        parser.error("not the App records capability definition")
    root = Path(tempfile.mkdtemp(prefix="chirality-records-delivery-", dir="/private/tmp"))
    print(f"Private evidence: {root}", flush=True)
    results = [run_case(binary, root / provider, definition, provider) for provider in ("fixture", "lmstudio")]
    if args.include_flat_model:
        results.append(run_case(binary, root / "fixture-flat", definition, "fixture", FLAT_MODEL, "function"))
    summary = {"format":"chirality.records-tool-carriage/1", "binarySha256":BINARY_SHA,
        "definitionSha256":sha_file(args.definition), "checkSha256":sha_file(Path(__file__)),
        "nativeHelperSha256":sha_file(Path(__file__).with_name("child_roles.py")), "cases":results,
        "standing":"stock supplier declarations to an invented capture-only provider; no model prediction, App handler or qualification witness"}
    save(root / "result.json", summary)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
