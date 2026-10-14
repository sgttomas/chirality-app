"""Local auth oracles distinguish exact custody facts from transport failures."""
import copy
import http.server
import io
import json
import os
from pathlib import Path
import tempfile
import threading
import socket
import re
import unittest
from unittest.mock import patch

from child_roles import Native
from local_auth import (AuthNative, MODEL, NativeRpcError, POLICY_ERROR, REDACTED, RedactedFrames,
                        assert_capture, assert_policy_refusal, guarded_save, header_facts, redact,
                        remove_auth, run_case)


class LocalAuthDetection(unittest.TestCase):
    def test_exact_bearer_and_original_request_route_required(self):
        canary = "invented unit canary"
        expected = {"path": "/v1/responses", "model": MODEL, "threadId": "thread", "turnId": "turn",
                    **header_facts("Bearer " + canary, canary)}
        assert_capture(expected, "thread", "turn", True)
        for auth in (None, "Bearer unrelated", "bearer " + canary, "Bearer " + canary + " "):
            wrong = {**expected, **header_facts(auth, canary)}
            with self.assertRaises(AssertionError):
                assert_capture(wrong, "thread", "turn", True)
        for key in ("path", "model", "threadId", "turnId"):
            wrong = dict(expected, **{key: "unrelated"})
            with self.assertRaises(AssertionError):
                assert_capture(wrong, "thread", "turn", True)
        anonymous = {**expected, **header_facts(None, canary)}
        assert_capture(anonymous, "thread", "turn", False)
        with self.assertRaises(AssertionError):
            assert_capture({**anonymous, **header_facts("Bearer unrelated", canary)}, "thread", "turn", False)

    def test_policy_requires_correlated_native_error_not_transport_failure(self):
        assert_policy_refusal(NativeRpcError("account/login/start", 7, POLICY_ERROR))
        for error in (TimeoutError("policy"), RuntimeError("native ended"),
                      NativeRpcError("thread/start", 7, POLICY_ERROR),
                      NativeRpcError("account/login/start", True, POLICY_ERROR),
                      NativeRpcError("account/login/start", 7, {"code": -32600, "message": "unrelated refusal"})):
            with self.assertRaises(AssertionError):
                assert_policy_refusal(error)

    def test_retained_frames_and_nested_errors_redact_without_mutating_wire_input(self):
        canary = "invented unit canary"
        value = {"apiKey": canary, "nested": [{"Authorization": "Bearer unrelated",
                  "accessToken": "another synthetic secret", canary: "echo " + canary}],
                 "error": {"message": "quoted " + canary}}
        original = copy.deepcopy(value)
        frames = RedactedFrames(canary)
        frames.append(value)
        self.assertEqual(value, original)
        self.assertNotIn(canary, json.dumps(frames))
        self.assertNotIn("another synthetic secret", json.dumps(frames))
        self.assertEqual(frames[0]["apiKey"], REDACTED)
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "evidence.json"
            guarded_save(target, value, canary)
            self.assertEqual(json.loads(target.read_text()), redact(value, canary))

    def test_native_error_diagnostics_require_actual_response_identity(self):
        native = AuthNative.__new__(AuthNative)
        native.counter, native.frames = 6, RedactedFrames("invented unit canary")
        def fail(self, method, params, notification):
            self.frames.append({"direction": "received", "frame": {"id": 7, "error": POLICY_ERROR}})
            raise RuntimeError("raw diagnostic invented unit canary")
        with patch.object(Native, "send", fail):
            with self.assertRaises(NativeRpcError) as caught:
                native.send("account/login/start", {})
            assert_policy_refusal(caught.exception)
        for frame in ({"processEnded": True}, {"id": 8, "error": POLICY_ERROR}, {"id": True, "error": POLICY_ERROR}):
            native.frames.clear()
            def unrelated(self, method, params, notification):
                self.frames.append({"direction": "received", "frame": frame})
                raise RuntimeError("raw diagnostic invented unit canary")
            with patch.object(Native, "send", unrelated):
                with self.assertRaises(RuntimeError) as caught:
                    native.send("account/login/start", {})
                self.assertNotIsInstance(caught.exception, NativeRpcError)
                self.assertNotIn("invented unit canary", str(caught.exception))

    def test_optional_stderr_sink_preserves_shared_env_argv_and_default_output(self):
        parent = dict(os.environ)
        class Process:
            pid = 12345
            def __init__(self):
                self.stdout, self.stdin = io.StringIO(""), io.StringIO()
            def wait(self, timeout):
                return 0
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "work").mkdir()
            with patch("child_roles.subprocess.Popen", side_effect=lambda *args, **kwargs: Process()) as popen, \
                    patch("child_roles.os.killpg"):
                normal = Native(Path("/owned/identified/codex"), root)
                normal_args = popen.call_args
                self.assertEqual(Path(normal.stderr.name), root / "stderr.log")
                normal.close()
                (root / "stderr.log").unlink()
                private = Native(Path("/owned/identified/codex"), root, discard_stderr=True)
                private_args = popen.call_args
                self.assertEqual(private.stderr.name, os.devnull)
                self.assertFalse((root / "stderr.log").exists())
                self.assertEqual(normal_args.args, private_args.args)
                self.assertEqual(normal_args.kwargs["env"], private_args.kwargs["env"])
                self.assertEqual(private_args.kwargs["env"]["HOME"], str(root / "os-home"))
                self.assertEqual(private_args.kwargs["env"]["CODEX_HOME"], str(root / "home"))
                self.assertIn('cli_auth_credentials_store="file"', private_args.args[0])
                private.close()
        self.assertEqual(dict(os.environ), parent)

    def test_cleanup_removes_auth_even_when_evidence_save_or_setup_fails(self):
        made = []
        class Server:
            def __init__(self, address, handler):
                self.server_port, self.stopped, self.closed = 12345, threading.Event(), False
                made.append(self)
            def serve_forever(self, poll_interval):
                self.stopped.wait(3)
            def shutdown(self):
                self.stopped.set()
            def server_close(self):
                self.closed = True
        class FailingNative:
            def __init__(self, binary, root, canary):
                (root / "home/auth.json").write_text(canary)
                self.frames = RedactedFrames(canary)
            def send(self, *args, **kwargs):
                raise RuntimeError("controlled transport failure")
            def close(self):
                pass
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "case"
            with patch("local_auth.http.server.HTTPServer", Server), \
                    patch("local_auth.AuthNative", FailingNative), \
                    patch("local_auth.guarded_save", side_effect=OSError("controlled evidence failure")):
                with self.assertRaises(OSError):
                    run_case(Path("/owned/identified/codex"), root, "auth-required")
            self.assertFalse((root / "home/auth.json").exists())
            self.assertTrue(made[-1].stopped.is_set() and made[-1].closed)
            original_write = Path.write_text
            def refuse_config(path, text, *args, **kwargs):
                if path.name == "config.toml":
                    raise OSError("controlled setup failure")
                return original_write(path, text, *args, **kwargs)
            with patch("local_auth.http.server.HTTPServer", Server), \
                    patch.object(Path, "write_text", refuse_config):
                with self.assertRaises(OSError):
                    run_case(Path("/owned/identified/codex"), Path(directory) / "setup", "auth-required")
            self.assertTrue(made[-1].stopped.is_set() and made[-1].closed)

    def test_auth_cleanup_unlinks_only_owned_leaf_not_symlink_target(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "home").mkdir()
            target = root / "unrelated"
            target.write_text("unrelated fixture data")
            (root / "home/auth.json").symlink_to(target)
            remove_auth(root)
            self.assertTrue(target.exists())
            self.assertFalse((root / "home/auth.json").exists())

    def test_partial_http_headers_cannot_hold_failed_native_cleanup(self):
        began, errors, clients, timeouts = threading.Event(), [], [], []
        original_handle = http.server.BaseHTTPRequestHandler.handle_one_request
        def observe_handler(handler):
            timeouts.append(handler.connection.gettimeout())
            began.set()
            return original_handle(handler)
        class FailingNative:
            def __init__(self, binary, root, canary):
                self.root, self.frames = root, RedactedFrames(canary)
                (root / "home/auth.json").write_text(canary)
            def send(self, *args, **kwargs):
                config = (self.root / "home/config.toml").read_text()
                port = int(re.search(r"127\.0\.0\.1:(\d+)/v1", config)[1])
                client = socket.create_connection(("127.0.0.1", port), timeout=2)
                clients.append(client)
                client.sendall(b"POST /v1/responses HTTP/1.1\r\nHost:")
                assert began.wait(2), "controlled handler did not start"
                raise RuntimeError("controlled initialization failure")
            def close(self):
                pass
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "case"
            def attempt():
                try:
                    run_case(Path("/owned/identified/codex"), root, "auth-required")
                except BaseException as error:
                    errors.append(type(error))
            with patch("local_auth.AuthNative", FailingNative), \
                    patch.object(http.server.BaseHTTPRequestHandler, "handle_one_request", observe_handler):
                worker = threading.Thread(target=attempt, daemon=True)
                worker.start()
                try:
                    worker.join(timeout=3)
                    self.assertFalse(worker.is_alive(), "partial headers held fixture teardown")
                    self.assertEqual(errors, [RuntimeError])
                    self.assertEqual(timeouts, [5])
                    self.assertFalse((root / "home/auth.json").exists())
                    self.assertTrue((root / "frames-redacted.json").exists())
                    self.assertEqual(clients[0].recv(1), b"")
                finally:
                    for client in clients:
                        client.close()
                    worker.join(timeout=6)
                    self.assertFalse(worker.is_alive(), "owned failing test worker did not stop")


if __name__ == "__main__":
    unittest.main()
