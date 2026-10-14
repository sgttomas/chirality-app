#!/usr/bin/env python3
"""Opt-in stock 0.160.0 local authorization-carrier check.

Only a generated invented canary enters fresh file-auth homes. A loopback
provider captures header correspondence and returns HTTP400 without prediction.
This is supplier evidence, not App access integration or real-key validation.
"""
import argparse
import hashlib
import hmac
import http.server
import json
from pathlib import Path
import secrets
import socket
import socketserver
import tempfile
import threading
import time

from child_roles import BINARY_SHA, Native, fixture_sandbox, save

MODEL = "gpt-6.1-sol"
PROVIDER = "fixture_auth"
REDACTED = "<synthetic redacted>"
CAPTURE_ERROR = "capture-only synthetic auth fixture; no prediction"
CASES = ("auth-required", "anonymous-control", "policy-refusal")
POLICY_ERROR = {"code": -32600, "message": "API key login is disabled. Use ChatGPT login instead."}


def sha_file(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(65536), b""):
            digest.update(block)
    return digest.hexdigest()


def redact(value, canary):
    if isinstance(value, dict):
        secret_fields = {"apikey", "accesstoken", "secretaccesskey", "sessiontoken", "authorization"}
        return {redact(key, canary): REDACTED if key.lower() in secret_fields else redact(item, canary)
                for key, item in value.items()}
    if isinstance(value, list):
        return [redact(item, canary) for item in value]
    if isinstance(value, str):
        return value.replace(canary, REDACTED)
    return value


def guarded_save(path, value, canary):
    clean = redact(value, canary)
    assert canary not in json.dumps(clean), "canary survived redaction"
    save(path, clean)


class RedactedFrames(list):
    def __init__(self, canary):
        super().__init__()
        self.canary = canary

    def append(self, value):
        super().append(redact(value, self.canary))


class NativeRpcError(RuntimeError):
    def __init__(self, method, rpc_id, error):
        super().__init__("correlated native RPC refusal")
        self.method, self.rpc_id, self.error = method, rpc_id, error


class AuthNative(Native):
    """Keep shared process/env/cleanup policy; retain only redacted frames."""
    def __init__(self, binary, root, canary):
        super().__init__(binary, root, discard_stderr=True)
        self.frames = RedactedFrames(canary)

    def send(self, method, params, notification=False):
        expected_id = self.counter + 1
        try:
            return super().send(method, params, notification)
        except RuntimeError:
            # Native's error text can quote a supplied credential. Never copy
            # it to diagnostics; inspect the already-redacted correlated frame.
            reply = self.frames[-1] if self.frames else {}
            frame = reply.get("frame", {})
            if (not notification and reply.get("direction") == "received"
                    and type(frame.get("id")) is int and frame["id"] == expected_id and "error" in frame):
                raise NativeRpcError(method, expected_id, frame["error"]) from None
            raise RuntimeError("native transport failed; no policy refusal established") from None


def assert_policy_refusal(error):
    assert isinstance(error, NativeRpcError), "policy refusal requires a native RPC error"
    assert error.method == "account/login/start" and type(error.rpc_id) is int, "wrong policy response identity"
    assert error.error == POLICY_ERROR, "native did not report the controlled ChatGPT-only policy refusal"


def header_facts(authorization, canary):
    return {"authorizationPresent": authorization is not None,
            "authorizationMatchesCanaryBearer": hmac.compare_digest(authorization or "", "Bearer " + canary)}


def assert_capture(capture, thread, turn, requires_auth):
    assert capture["threadId"] == thread and capture["turnId"] == turn, "provider/request identity differs"
    assert capture["model"] == MODEL and capture["path"] == "/v1/responses", "provider route differs"
    assert capture["authorizationPresent"] is requires_auth, "unexpected authorization header presence"
    assert capture["authorizationMatchesCanaryBearer"] is requires_auth, "bearer did not match the invented canary"


def remove_auth(root):
    # Remove only this fresh fixture's leaf, without reading its content;
    # unlink also removes a substituted symlink itself rather than its target.
    (root / "home/auth.json").unlink(missing_ok=True)


def assert_canary_absent(root, canary):
    needle = canary.encode()
    for path in root.rglob("*"):
        if path.is_file() and not path.is_symlink():
            with path.open("rb") as stream:
                tail = b""
                for block in iter(lambda: stream.read(65536), b""):
                    joined = tail + block
                    assert needle not in joined, "canary found in retained fixture output"
                    tail = joined[-len(needle):]


def run_case(binary, root, case):
    assert case in CASES, "unknown local-auth case"
    requires, policy = case != "anonymous-control", "chatgpt" if case == "policy-refusal" else None
    canary = "synthetic-not-a-provider-key-" + secrets.token_urlsafe(32)
    root.mkdir()
    (root / "home").mkdir()
    (root / "work").mkdir()
    native, server, worker = None, None, None
    frames, captures, server_errors = [], [], []
    lock = threading.Lock()
    summary = {"case": case, "requiresOpenaiAuthConfigured": requires, "forcedLoginMethod": policy,
               "fileAuthSelected": True, "configChecks": [], "turns": [], "captures": captures}

    class Provider(http.server.BaseHTTPRequestHandler):
        def log_message(self, *args):
            pass

        def do_POST(self):
            try:
                self.connection.settimeout(5)
                size = int(self.headers.get("Content-Length", "0"))
                assert 0 < size <= 2 * 1024 * 1024, "capture body outside bound"
                raw = self.rfile.read(size)
                assert len(raw) == size, "incomplete capture body"
                body = json.loads(raw)
                metadata = body.get("client_metadata", {})
                observed = {"path": self.path, **header_facts(self.headers.get("Authorization"), canary),
                            "model": body.get("model"), "threadId": metadata.get("thread_id"),
                            "turnId": metadata.get("turn_id")}
                with lock:
                    assert len(captures) < 24, "capture count outside bound"
                    captures.append(redact(observed, canary))
                self.send_response(400)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"error": {"message": CAPTURE_ERROR}}).encode())
            except Exception:
                # Do not print parser/transport errors or retain raw headers/body.
                with lock:
                    server_errors.append("loopback capture failed")
                self.close_connection = True

    # One owned server thread handles these sequential requests. Bound reads
    # before HTTP header parsing and close every accepted socket at teardown,
    # so a partial/dripping header cannot hold listener shutdown indefinitely.
    class Server(http.server.HTTPServer):
        def __init__(self, *args, **kwargs):
            self.active, self.stopping = set(), False
            super().__init__(*args, **kwargs)

        def server_bind(self):
            # This fixture binds only the literal loopback address. HTTPServer's
            # reverse-name lookup is unnecessary and could stall before the
            # listener worker/cleanup ownership is established.
            socketserver.TCPServer.server_bind(self)
            self.server_name, self.server_port = "localhost", self.server_address[1]

        def get_request(self):
            connection, address = super().get_request()
            connection.settimeout(5)
            with lock:
                if self.stopping:
                    connection.close()
                    raise OSError("owned listener is stopping")
                self.active.add(connection)
            return connection, address

        def shutdown_request(self, connection):
            try:
                super().shutdown_request(connection)
            finally:
                with lock:
                    self.active.discard(connection)

        def close_active(self):
            with lock:
                self.stopping = True
                active = tuple(self.active)
            for connection in active:
                try:
                    connection.shutdown(socket.SHUT_RDWR)
                except OSError:
                    pass
                connection.close()

        def handle_error(self, request, client_address):
            with lock:
                server_errors.append("loopback handler failed")

    def open_native():
        n = AuthNative(binary, root, canary)
        try:
            summary.setdefault("initializes", []).append(n.send("initialize", {
                "clientInfo": {"name": "local_auth_synthetic_fixture", "version": "0.0.0"},
                "capabilities": {"experimentalApi": True}}))
            n.send("initialized", {}, notification=True)
            return n
        except BaseException:
            try:
                n.close()
            finally:
                frames.extend(n.frames)
            raise

    def close_native():
        nonlocal native
        if native is not None:
            ended, native = native, None
            try:
                ended.close()
            finally:
                frames.extend(ended.frames)

    def config_checks(stage):
        for layers in (False, True):
            read = native.send("config/read", {"includeLayers": layers, "cwd": str(root / "work")})
            assert canary not in json.dumps(read), "config/read included credential value"
            effective = read["config"]
            assert effective["model_provider"] == PROVIDER and effective["model"] == MODEL, "wrong configured route"
            definition = effective["model_providers"][PROVIDER]
            assert definition["requires_openai_auth"] is requires and definition["wire_api"] == "responses", "wrong provider configuration"
            assert definition["base_url"] == f"http://127.0.0.1:{server.server_port}/v1", "wrong capture endpoint"
            guarded_save(root / f"config-{stage}-layers-{layers}.json", read, canary)
            summary["configChecks"].append({"stage": stage, "includeLayers": layers, "canaryAbsent": True})

    def account(stage, expected):
        result = native.send("account/read", {"refreshToken": False})
        assert canary not in json.dumps(result), "account/read included credential value"
        assert result["account"] == expected and result["requiresOpenaiAuth"] is requires, "unexpected native account projection"
        summary.setdefault("accountReads", {})[stage] = result
        exists = (root / "home/auth.json").is_file()
        summary.setdefault("authFileExists", {})[stage] = exists
        return exists

    def turn(stage, authorized):
        before, first_frame = len(captures), len(native.frames)
        started = native.send("thread/start", {"model": MODEL, "modelProvider": PROVIDER, "cwd": str(root / "work")})
        assert started["model"] == MODEL and started["modelProvider"] == PROVIDER, "wrong native thread route"
        thread = started["thread"]["id"]
        response = native.send("turn/start", {"threadId": thread, "input": [{"type": "text",
            "text": "Invented synthetic authorization-carrier fixture; no model prediction."}]})
        turn_id = response["turn"]["id"]
        backlog = [row["frame"] for row in native.frames[first_frame:] if row["direction"] == "received"]
        deadline, completed = time.monotonic() + 15, None
        while time.monotonic() < deadline:
            if backlog:
                frame = backlog.pop(0)
            else:
                frame = native.incoming.get(timeout=max(.001, deadline - time.monotonic()))
                native.frames.append({"direction": "received", "frame": frame})
            assert not frame.get("processEnded"), "native process ended before correlated completion"
            params = frame.get("params", {})
            if (frame.get("method") == "turn/completed" and params.get("threadId") == thread
                    and params.get("turn", {}).get("id") == turn_id):
                completed = params["turn"]
                break
        assert completed is not None, "no correlated turn completion"
        assert completed["status"] == "failed" and CAPTURE_ERROR in completed["error"]["message"], "not the capture-only fixture failure"
        assert len(captures) - before == 1 and not server_errors, "unexpected capture requests/failure"
        assert_capture(captures[-1], thread, turn_id, authorized)
        summary["turns"].append({"stage": stage, "threadId": thread, "turnId": turn_id,
                                 "completion": redact(completed, canary), "requests": 1})

    try:
        (root / "network.sb").write_text(fixture_sandbox(binary))
        # All setup after listener acquisition belongs to this cleanup block.
        server = Server(("127.0.0.1", 0), Provider)
        worker = threading.Thread(target=server.serve_forever, kwargs={"poll_interval": .1}, daemon=True)
        worker.start()
        config = (f'model_provider = "{PROVIDER}"\nmodel = "{MODEL}"\ncli_auth_credentials_store = "file"\n'
                  + ('forced_login_method = "chatgpt"\n' if policy else '')
                  + f'[model_providers.{PROVIDER}]\nname = "Invented auth capture provider"\n'
                  f'base_url = "http://127.0.0.1:{server.server_port}/v1"\nwire_api = "responses"\n'
                  f'requires_openai_auth = {str(requires).lower()}\n'
                  '[features]\nplugins = false\n[analytics]\nenabled = false\n')
        (root / "home/config.toml").write_text(config)
        native = open_native()
        summary["requirements"] = native.send("configRequirements/read", None)
        config_checks("before-login")
        assert not account("before-login", None), "fresh fixture unexpectedly holds auth"
        if not policy:
            # A declared requirement does not prevent an unauthenticated request.
            turn("before-login", False)
        try:
            login = native.send("account/login/start", {"type": "apiKey", "apiKey": canary})
        except NativeRpcError as error:
            assert policy, "unexpected login refusal"
            assert_policy_refusal(error)
            summary["loginRefusal"] = {"method": error.method, "id": error.rpc_id, "error": error.error}
        else:
            assert not policy and login == {"type": "apiKey"}, "unexpected native login success"
            summary["loginResponse"] = login
        if policy:
            assert "loginRefusal" in summary, "no correlated policy refusal"
            assert not account("after-refused-login", None) and not captures, "refused login changed auth or contacted provider"
        else:
            expected_account = {"type": "apiKey"} if requires else None
            assert account("after-login", expected_account), "native did not retain file-auth leaf"
            config_checks("after-login")
            turn("after-login", requires)
            close_native()
            native = open_native()
            assert account("after-native-restart", expected_account), "cold auth leaf disappeared"
            config_checks("after-native-restart")
            turn("after-native-restart", requires)
            summary["logoutResponse"] = native.send("account/logout", None)
            assert not account("after-logout", None), "native logout did not remove auth leaf"
            turn("after-logout", False)
            close_native()
            native = open_native()
            assert not account("after-logout-restart", None), "logout did not persist across native restart"
            turn("after-logout-restart", False)
        summary["pass"] = True
        return summary
    finally:
        try:
            try:
                close_native()
            finally:
                if server is not None:
                    try:
                        server.close_active()
                        if worker is not None and worker.is_alive():
                            server.shutdown()
                    finally:
                        server.server_close()
                        if worker is not None:
                            worker.join(timeout=2)
                            assert not worker.is_alive(), "owned listener did not stop"
                guarded_save(root / "frames-redacted.json", frames, canary)
                guarded_save(root / "observations.json", summary, canary)
        finally:
            # Even failed shutdown/redaction/evidence writes cannot skip removal.
            remove_auth(root)
            assert_canary_absent(root, canary)


def protocol_check(schemas):
    outer = json.loads((schemas / "codex_app_server_protocol.schemas.json").read_text())["definitions"]
    v2 = json.loads((schemas / "codex_app_server_protocol.v2.schemas.json").read_text())["definitions"]
    api = next(value for value in v2["LoginAccountParams"]["oneOf"] if value["properties"]["type"]["enum"] == ["apiKey"])
    assert api["required"] == ["apiKey", "type"] and api["properties"]["apiKey"]["type"] == "string", "login carrier schema differs"
    refs = {value["properties"]["method"]["enum"][0]: value["properties"]["params"] for value in outer["ClientRequest"]["oneOf"]}
    assert refs["account/login/start"]["$ref"] == "#/definitions/v2/LoginAccountParams", "login method schema differs"
    assert refs["account/logout"] == {"type": "null"} and refs["configRequirements/read"] == {"type": "null"}, "account method schema differs"
    return {path.name: sha_file(path) for path in sorted(schemas.glob("*.schemas.json"))}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--codex", required=True, type=Path, help="already acquired identified stock executable")
    parser.add_argument("--case", choices=CASES, action="append", help="repeat to select controls; default runs all three")
    args = parser.parse_args()
    binary = args.codex.resolve(strict=True)
    if sha_file(binary) != BINARY_SHA:
        parser.error("not the identified stock 0.160.0 macOS arm64 binary")
    schemas = Path(__file__).resolve().parents[1] / "src-tauri/resources/supplier/0.160.0"
    report = {"format": "chirality.local-auth-carriage/1", "binarySha256": BINARY_SHA,
              "checkSha256": sha_file(Path(__file__)), "nativeHelperSha256": sha_file(Path(__file__).with_name("child_roles.py")),
              "protocolSha256": protocol_check(schemas), "cases": [],
              "standing": "stock Native with invented loopback canary; no real key, prediction, App access or qualification witness"}
    root = Path(tempfile.mkdtemp(prefix="chirality-local-auth-", dir="/private/tmp"))
    print(f"Private redacted evidence: {root}", flush=True)
    try:
        for case in args.case or CASES:
            report["cases"].append(run_case(binary, root / case, case))
            print(f"Completed {case}", flush=True)
    except BaseException:
        # Transport/native/parser errors must not escape as raw diagnostics.
        report["failure"] = "local-auth control failed; inspect redacted case evidence"
        save(root / "result.json", report)
        raise SystemExit("local-auth check failed; inspect redacted evidence") from None
    report["scriptedRequests"] = sum(len(case["captures"]) for case in report["cases"])
    report["predictionCount"] = 0
    save(root / "result.json", report)
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
