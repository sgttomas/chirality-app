"""Recording transport and redaction on invented peers; no supplier or model."""
import json
import os
from pathlib import Path
import sys
import tempfile
import types
import unittest
from unittest.mock import patch

import record_at_pin as capture


class Transport(unittest.TestCase):
    def peer(self, mode):
        temporary = tempfile.TemporaryDirectory(prefix="invented-recorder-")
        self.addCleanup(temporary.cleanup)
        root = Path(os.path.realpath(temporary.name))
        binary = root / "invented-peer"
        binary.write_text(f'''#!{sys.executable}
import json,sys
for line in sys.stdin:
 frame=json.loads(line)
 if "id" not in frame: continue
 if {mode!r} == "truncated":
  sys.stdout.write('{{"id":');sys.stdout.flush();break
 response=json.dumps({{"id":frame["id"],"result":{{"observed":frame["method"]}}}})+"\\n"
 sys.stdout.write(response);sys.stdout.flush()
 if {mode!r} == "duplicate": sys.stdout.write(response);sys.stdout.flush()
''')
        binary.chmod(0o755)
        run = types.SimpleNamespace(vendor=root, record={}, work=root, pipes=[], frames=[], environment={
            "PATH":"/usr/bin:/bin", "HOME":str(root), "CODEX_HOME":str(root), "TMPDIR":str(root), "LANG":"C", "TZ":"UTC"})
        run.frame = lambda generation, direction, frame: run.frames.append((generation, direction, frame))
        with patch.object(capture.intake, "verified_vendor", return_value=(str(binary), str(root))), \
             patch.object(capture.intake, "outside_configuration", return_value={}):
            pipe = capture.Pipe(run, 1)
        def close():
            if not pipe.closed:
                capture.stop_group(pipe.process)
                pipe.selector.close()
                pipe.process.stdin.close()
                pipe.process.stdout.close()
        self.addCleanup(close)
        return run, pipe

    def test_correlated_frames_drain_through_eof(self):
        run, pipe = self.peer("ordinary")
        self.assertEqual(pipe.initialize(), {"observed":"initialize"})
        self.assertEqual(pipe.request("thread/read", {"threadId":"invented"}), {"observed":"thread/read"})
        pipe.end()
        self.assertTrue(pipe.eof and pipe.closed)
        self.assertEqual([f[2].get("method") for f in run.frames if f[1] == "app->codex"],
                         ["initialize", "initialized", "thread/read"])

    def test_duplicate_reply_refuses(self):
        _, pipe = self.peer("duplicate")
        with self.assertRaisesRegex(capture.Refused, "duplicate"):
            pipe.initialize()
            pipe.end()

    def test_truncated_frame_refuses(self):
        _, pipe = self.peer("truncated")
        with self.assertRaisesRegex(capture.Refused, "incomplete frame"):
            pipe.initialize()


class Scripts(unittest.TestCase):
    def test_only_the_declared_command_is_scripted(self):
        plan = capture.script("st5")
        body = {"tools":[{"name":"exec_command"}],"input":[]}
        items, _, _ = plan(1, body)
        args = json.loads(items[0]["arguments"])
        self.assertEqual(args["cmd"], "mkdir st5-marker-pump-skid")
        self.assertEqual(args["sandbox_permissions"], "require_escalated")
        with self.assertRaises(capture.Refused):
            plan(1, {"tools":[{"name":"unknown"}],"input":[]})

    def test_spawn_script_names_only_the_invented_prompt(self):
        plan = capture.script("nv04")
        items, _, _ = plan(1, {"tools":[{"type":"namespace","name":"collab","tools":[{"name":"spawn_agent"}]}]})
        self.assertEqual(items[0]["namespace"], "collab")
        self.assertEqual(json.loads(items[0]["arguments"]), {"message":capture.CHILD_PROMPT,"task_name":"count_files"})
        with self.assertRaises(capture.Refused):
            plan(2, {"tools":[{"name":"spawn_agent"}]})


if __name__ == "__main__":
    unittest.main()
