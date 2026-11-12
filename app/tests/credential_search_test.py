"""app/tools/credential_search.py: the parts that decide what counts as found.

Invented values only. The prompt itself (keyboard only, no echo) is exercised
by hand through a terminal; these tests hold the matching and the rule that a
value never appears in what the tool can print.
"""
import base64
import importlib.util
import io
import os
import pathlib
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from unittest import mock

SPEC = importlib.util.spec_from_file_location(
    "credential_search", pathlib.Path(__file__).resolve().parents[1] / "tools" / "credential_search.py")
tool = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(tool)

VALUE = "INVENTED-KEY-0123456789-abcdef"


class CredentialSearch(unittest.TestCase):
    def test_long_text_values_of_a_sign_in_file_are_taken_and_labels_are_not(self):
        parsed = {"mode": "chatgpt", "tokens": {"access": "A" * 40, "list": ["B" * 20, "short"]}, "n": 3}
        self.assertEqual(sorted(tool.long_strings(parsed)), ["A" * 40, "B" * 20])

    def test_a_value_is_found_plain_and_as_base64_and_across_a_block_boundary(self):
        patterns = [tool.forms(VALUE)]
        with tempfile.TemporaryDirectory() as folder:
            cases = {
                "plain": b"x" + VALUE.encode() + b"y",
                "base64": b"aa" + base64.b64encode(VALUE.encode()) + b"zz",
                "urlsafe-unpadded": base64.urlsafe_b64encode(VALUE.encode()).rstrip(b"="),
                "split": b"p" * (tool.CHUNK - 7) + VALUE.encode() + b"q" * 50,
                "absent": b"nothing here " * 1000,
                "prefix-only": VALUE[:-1].encode(),
            }
            for name, content in cases.items():
                path = os.path.join(folder, name)
                with open(path, "wb") as handle:
                    handle.write(content)
                found = tool.file_contains(path, patterns)
                self.assertEqual(found, set() if name in ("absent", "prefix-only") else {0}, name)

    def test_an_unreadable_file_is_incomplete_and_no_value_or_length_is_printed(self):
        with tempfile.TemporaryDirectory() as folder:
            with open(os.path.join(folder, "leak.log"), "w") as handle:
                handle.write("x" + VALUE + "y")
            locked = os.path.join(folder, "locked.txt")
            with open(locked, "w") as handle:
                handle.write("unread")
            os.chmod(locked, 0)
            typed = iter([VALUE, ""])
            out = io.StringIO()
            try:
                with mock.patch.object(sys, "argv", ["credential_search.py", folder]), \
                        mock.patch.object(sys.stdin, "isatty", lambda: True), \
                        mock.patch.object(tool.getpass, "getpass", lambda prompt: next(typed)), redirect_stdout(out):
                    code = tool.main()
            finally:
                os.chmod(locked, 0o600)
            text = out.getvalue()
            self.assertEqual(code, 1)
            self.assertIn("Value 1: FOUND in 1 file(s):", text)
            self.assertIn("INCOMPLETE: 1 file(s) or folder(s) could not be read:", text)
            self.assertNotIn(VALUE, text)
            self.assertNotIn(str(len(VALUE)), text.replace(folder, ""))
            self.assertNotIn("every file was read", text)

    def test_nothing_is_searched_without_a_terminal_or_without_a_value(self):
        with tempfile.TemporaryDirectory() as folder:
            for tty, typed, expect in ((False, [], "Run this at a terminal"), (True, [""], "No value was given")):
                answers = iter(typed)
                out = io.StringIO()
                with mock.patch.object(sys, "argv", ["credential_search.py", folder]), \
                        mock.patch.object(sys.stdin, "isatty", lambda: tty), \
                        mock.patch.object(tool.getpass, "getpass", lambda prompt: next(answers)), redirect_stdout(out):
                    self.assertEqual(tool.main(), 2)
                self.assertIn(expect, out.getvalue())

    def test_the_folder_of_a_given_sign_in_file_is_not_searched_and_its_values_are_looked_for(self):
        with tempfile.TemporaryDirectory() as folder:
            home, data = os.path.join(folder, "home"), os.path.join(folder, "data")
            os.mkdir(home), os.mkdir(data)
            token = "INVENTED-TOKEN-" + "t" * 30
            with open(os.path.join(home, "auth.json"), "w") as handle:
                handle.write('{"tokens": {"access_token": "%s"}, "kind": "x"}' % token)
            with open(os.path.join(data, "record.json"), "w") as handle:
                handle.write('{"note": "%s"}' % token)
            answers = iter([""])
            out = io.StringIO()
            with mock.patch.object(sys, "argv", ["credential_search.py", "--codex-auth", os.path.join(home, "auth.json"), folder]), \
                    mock.patch.object(sys.stdin, "isatty", lambda: True), \
                    mock.patch.object(tool.getpass, "getpass", lambda prompt: next(answers)), redirect_stdout(out):
                code = tool.main()
            text = out.getvalue()
            self.assertEqual(code, 1)
            self.assertIn("record.json", text)
            self.assertNotIn("auth.json", text)
            self.assertNotIn(token, text)


if __name__ == "__main__":
    unittest.main()
