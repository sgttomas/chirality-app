"""app/tools/credential_search.py, with invented values only.

Holds what the tool states of itself: what it reads, what it prints, what
makes its result incomplete. Each way an earlier version failed an independent
review has a test here: an echoing terminal, a value in a file name, an
App-written file beside the sign-in file, a symbolic link as the folder given,
a harmless long label standing in for a short credential, and an error whose
text could quote a value.
"""
import base64
import importlib.util
import io
import os
import pathlib
import pty
import tempfile
import termios
import threading
import unittest
from contextlib import redirect_stderr, redirect_stdout
from unittest import mock

SPEC = importlib.util.spec_from_file_location(
    "credential_search", pathlib.Path(__file__).resolve().parents[1] / "tools" / "credential_search.py")
tool = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(tool)

VALUE = "INVENTED-KEY-0123456789-abcdef"
TOKEN = "INVENTED-TOKEN-" + "t" * 30


def run(args, typed=()):
    """Exit status and everything printed, with the terminal prompt replaced by `typed` (bytes) then an empty line."""
    answers = iter(list(typed) + [b""])
    out, err = io.StringIO(), io.StringIO()
    with mock.patch.object(tool, "read_secret", lambda prompt: next(answers)), redirect_stdout(out), redirect_stderr(err):
        code = tool.main(list(args))
    return code, out.getvalue() + err.getvalue()


def write(path, content):
    with open(path, "wb") as handle:
        handle.write(content if isinstance(content, bytes) else content.encode())


class Matching(unittest.TestCase):
    def test_plain_bytes_and_each_base64_form_are_found_and_nothing_shorter_is(self):
        raw = b"??>~~?" * 3  # its standard and URL-safe base64 differ, and need padding at other lengths
        self.assertNotEqual(base64.b64encode(raw), base64.urlsafe_b64encode(raw))
        padded = VALUE.encode() + b"x"
        self.assertTrue(base64.b64encode(padded).endswith(b"="))
        with tempfile.TemporaryDirectory() as folder:
            cases = {
                "plain": (raw, b"x" + raw + b"y", True),
                "standard": (raw, b"aa" + base64.b64encode(raw) + b"zz", True),
                "urlsafe": (raw, base64.urlsafe_b64encode(raw), True),
                "padded": (padded, base64.b64encode(padded), True),
                "unpadded": (padded, base64.b64encode(padded).rstrip(b"="), True),
                "split": (raw, b"p" * (tool.CHUNK - 7) + raw + b"q" * 50, True),
                "absent": (raw, b"nothing here " * 1000, False),
                "prefix-only": (raw, raw[:-1], False),
                # A value ending in "=" is not matched by its own text without the "=".
                "raw-padding-kept": (b"INVENTED-ENDS-IN=", b"INVENTED-ENDS-IN", False),
            }
            for name, (value, content, expected) in cases.items():
                path = os.path.join(folder, name)
                write(path, content)
                with open(path, "rb") as handle:
                    self.assertEqual(tool.stream_contains(handle, [tool.forms(value)]), {0} if expected else set(), name)

    def test_a_block_boundary_never_hides_a_value(self):
        with mock.patch.object(tool, "CHUNK", 8):
            for length in (1, 7, 8, 9, 17, 40):
                value = bytes(range(65, 65 + length))
                for offset in range(0, 20):
                    stream = io.BytesIO(b"." * offset + value + b"." * 11)
                    self.assertEqual(tool.stream_contains(stream, [[value]]), {0}, (length, offset))


class SignInFile(unittest.TestCase):
    def test_credential_fields_are_taken_by_name_and_other_long_text_is_kept_apart(self):
        parsed = {"auth_mode": "chatgpt", "OPENAI_API_KEY": None, "last_refresh": "2026-01-01T00:00:00Z",
                  "tokens": {"id_token": "I" * 30, "access_token": "A" * 30, "refresh_token": "short-rt", "account_id": "account-" + "9" * 28},
                  "bedrock_access_keys": {"access_key_id": "K" * 20, "secret": "S" * 40}}
        credentials, others = tool.sign_in_values(parsed)
        self.assertEqual(sorted(credentials), sorted(["I" * 30, "A" * 30, "short-rt", "K" * 20, "S" * 40]))
        self.assertEqual(others, ["2026-01-01T00:00:00Z", "account-" + "9" * 28])
        self.assertEqual(tool.sign_in_values({"OPENAI_API_KEY": "sk-invented-" + "k" * 20})[0], ["sk-invented-" + "k" * 20])
        self.assertEqual(tool.sign_in_values({"note": "L" * 40})[0], [], "a long label is not a credential")
        for unknown in ([], "text", 3, None, {"tokens": ["not", "an", "object"]}):
            self.assertIsNone(tool.sign_in_values(unknown), repr(unknown))

    def test_only_the_sign_in_file_itself_is_left_unsearched(self):
        with tempfile.TemporaryDirectory() as folder:
            home = os.path.join(folder, "home")
            os.mkdir(home)
            auth = os.path.join(home, "auth.json")
            write(auth, '{"tokens": {"access_token": "%s", "id_token": "%s", "refresh_token": "%s"}}' % (TOKEN, "I" * 40, "R" * 40))
            write(os.path.join(home, "app-written.log"), "x" + TOKEN + "y")
            write(os.path.join(folder, "clean.txt"), "clean")
            code, text = run(["--codex-auth", auth, folder])
            self.assertEqual(code, 1)
            self.assertIn("app-written.log", text)
            self.assertNotIn("auth.json", text)
            self.assertIn("1 given, 1 met under the folders", text)
            self.assertNotIn(TOKEN, text)
            # With the leak gone, the same search is clean and says what it left out.
            os.remove(os.path.join(home, "app-written.log"))
            code, text = run(["--codex-auth", auth, folder])
            self.assertEqual(code, 0, text)
            self.assertIn("Regular files read: 1.", text)

    def test_a_sign_in_file_of_another_shape_or_without_a_credential_is_incomplete_not_clean(self):
        with tempfile.TemporaryDirectory() as folder:
            write(os.path.join(folder, "leak.log"), "short-secret")
            cases = {"label-only.json": '{"note": "%s", "tokens": {"access_token": ""}}' % ("L" * 40), "list.json": "[1, 2]", "not-json": "{",
                     "short-credential.json": '{"OPENAI_API_KEY": "short", "note": "%s"}' % ("L" * 40), "bad-text.json": '{"OPENAI_API_KEY": "\\ud800%s"}' % ("k" * 30)}
            for name, content in cases.items():
                auth = os.path.join(folder, name)
                write(auth, content)
                code, text = run(["--codex-auth", auth, folder])
                self.assertEqual(code, 2, name)
                self.assertIn("Nothing was searched.", text, name)
                self.assertIn("Result: incomplete.", text, name)
                self.assertNotIn("no value was found", text, name)
                self.assertNotIn("ud800", text.lower(), name)
            link = os.path.join(folder, "link.json")
            target = os.path.join(folder, "real.json")
            write(target, '{"OPENAI_API_KEY": "%s"}' % VALUE)
            os.symlink(target, link)
            code, text = run(["--codex-auth", link, folder])
            self.assertEqual(code, 2)
            self.assertIn("is a symbolic link", text)
            self.assertEqual(run(["--codex-auth", os.path.join(folder, "missing.json"), folder])[0], 2)


class Results(unittest.TestCase):
    def test_a_file_that_cannot_be_read_makes_a_search_with_no_hit_incomplete(self):
        with tempfile.TemporaryDirectory() as folder:
            write(os.path.join(folder, "clean.txt"), "clean")
            locked = os.path.join(folder, "locked.txt")
            write(locked, VALUE)
            os.chmod(locked, 0)
            try:
                code, text = run([folder], [VALUE.encode()])
            finally:
                os.chmod(locked, 0o600)
            self.assertEqual(code, 2)
            self.assertIn("INCOMPLETE: 1 file(s) or folder(s) could not be read or classified:", text)
            self.assertIn("locked.txt", text)
            self.assertIn("Result: incomplete.", text)
            self.assertNotIn("no value was found", text)

    def test_a_hit_is_reported_by_number_and_no_value_form_or_length_is_printed(self):
        with tempfile.TemporaryDirectory() as folder:
            write(os.path.join(folder, "leak.log"), "x" + VALUE + "y")
            write(os.path.join(folder, "encoded.bin"), base64.b64encode(VALUE.encode()))
            code, text = run([folder], [VALUE.encode()])
            self.assertEqual(code, 1)
            self.assertIn("Value 1 (typed at the keyboard): FOUND in 2 file(s):", text)
            self.assertIn("Result: a value was FOUND.", text)
            for form in tool.forms(VALUE.encode()):
                self.assertNotIn(form.decode(), text)
            self.assertNotIn(str(len(VALUE)), text.replace(folder, ""))

    def test_a_name_that_contains_the_value_is_counted_and_never_printed(self):
        with tempfile.TemporaryDirectory() as folder:
            os.mkdir(os.path.join(folder, VALUE))
            write(os.path.join(folder, VALUE, "inside.txt"), VALUE)
            write(os.path.join(folder, "named-" + VALUE + ".log"), VALUE)
            write(os.path.join(folder, "line\nbreak\x1b[31m.txt"), VALUE)
            code, text = run([folder], [VALUE.encode()])
            self.assertEqual(code, 1)
            self.assertNotIn(VALUE, text)
            self.assertIn("FOUND in 3 file(s):", text)
            self.assertIn("and 2 file(s) whose name itself contains a value; those names are not printed.", text)
            self.assertIn("line\\x0abreak\\x1b[31m.txt", text)
            self.assertNotIn("\x1b", text)

    def test_links_are_not_followed_a_linked_folder_is_refused_and_the_result_says_what_was_left_out(self):
        with tempfile.TemporaryDirectory() as folder:
            outside, inside = os.path.join(folder, "outside"), os.path.join(folder, "inside")
            os.mkdir(outside), os.mkdir(inside)
            write(os.path.join(outside, "secret.txt"), VALUE)
            write(os.path.join(inside, "clean.txt"), "clean")
            os.symlink(os.path.join(outside, "secret.txt"), os.path.join(inside, "file-link"))
            os.symlink(outside, os.path.join(inside, "folder-link"))
            os.mkfifo(os.path.join(inside, "pipe"))
            code, text = run([inside], [VALUE.encode()])
            self.assertEqual(code, 0, text)
            self.assertIn("Regular files read: 1.", text)
            self.assertIn("Symbolic links not followed: 2. Special files (not regular files) not read: 1.", text)
            self.assertIn("and whatever the symbolic links point to", text)
            root_link = os.path.join(folder, "root-link")
            os.symlink(outside, root_link)
            code, text = run([root_link], [VALUE.encode()])
            self.assertEqual(code, 2)
            self.assertIn("is a symbolic link. Nothing was searched.", text)
            self.assertEqual(run([os.path.join(folder, "missing")], [VALUE.encode()])[0], 2)
            self.assertEqual(run([os.path.join(inside, "clean.txt")], [VALUE.encode()])[0], 2)

    def test_nothing_is_called_clean_without_a_value_a_file_or_a_usable_argument(self):
        with tempfile.TemporaryDirectory() as folder:
            empty = os.path.join(folder, "empty")
            os.mkdir(empty)
            for args, typed, expect in (([folder], [], "No value was given."), ([folder], [b"short"], "too short to search for"),
                                        ([empty], [VALUE.encode()], "INCOMPLETE: no file was read."), ([], [], "Usage:"),
                                        (["--secret=" + VALUE, folder], [], "Usage:")):
                code, text = run(args, typed)
                self.assertEqual(code, 2, expect)
                self.assertIn(expect, text)
                self.assertNotIn(VALUE, text)
                self.assertNotIn("no value was found", text)

    def test_an_unexpected_error_prints_a_fixed_sentence_and_never_its_own_text(self):
        with tempfile.TemporaryDirectory() as folder:
            write(os.path.join(folder, "a.txt"), "a")
            with mock.patch.object(tool, "stream_contains", side_effect=ValueError("quoted " + VALUE)):
                code, text = run([folder], [VALUE.encode()])
            self.assertEqual(code, 2)
            self.assertIn("Stopped by an unexpected error. Result: incomplete.", text)
            self.assertNotIn(VALUE, text)
            self.assertNotIn("Traceback", text)
            with mock.patch.object(tool, "read_secret", side_effect=KeyboardInterrupt):
                out = io.StringIO()
                with redirect_stdout(out):
                    self.assertEqual(tool.main([folder]), 2)
            self.assertIn("Stopped at your request. Result: incomplete.", out.getvalue())


class Terminal(unittest.TestCase):
    """A pseudo-terminal stands in for the person's terminal; a helper types only after the prompt appears."""

    def with_terminal(self, typed, check):
        master, slave = pty.openpty()
        real_open = os.open
        seen = []

        def person():
            shown = b""
            try:
                while b"Prompt: " not in shown:
                    block = os.read(master, 4096)
                    if not block:
                        break
                    shown += block
                if typed is not None:
                    os.write(master, typed + b"\n")
                shown += os.read(master, 4096)
            except OSError:
                pass
            seen.append(shown)

        helper = threading.Thread(target=person, daemon=True)
        helper.start()
        try:
            with mock.patch.object(tool.os, "open", lambda path, flags, *rest, **named: os.dup(slave) if path == "/dev/tty" else real_open(path, flags, *rest, **named)):
                check()
        finally:
            os.close(slave)
            helper.join(5)
            os.close(master)
        return seen[0] if seen else b""

    def test_a_typed_value_is_read_with_echo_off(self):
        result = []
        shown = self.with_terminal(VALUE.encode(), lambda: result.append(tool.read_secret("Prompt: ")))
        self.assertEqual(result, [VALUE.encode()])
        self.assertIn(b"Prompt: ", shown)
        self.assertNotIn(VALUE.encode(), shown, "the terminal did not echo the value")

    def test_a_terminal_that_cannot_switch_echo_off_stops_the_run_before_anything_is_read(self):
        def check():
            with mock.patch.object(termios, "tcsetattr", side_effect=termios.error(25, "refused")):
                with self.assertRaises(tool.Stop) as stopped:
                    tool.read_secret("Prompt: ")
                self.assertIn("cannot switch echo off, so nothing was read", stopped.exception.args[0])
                # The same terminal, through the whole tool: incomplete, no prompt, the value never printed.
                with tempfile.TemporaryDirectory() as folder:
                    write(os.path.join(folder, "a.txt"), VALUE)
                    out = io.StringIO()
                    with redirect_stdout(out):
                        self.assertEqual(tool.main([folder]), 2)
                    self.assertIn("Result: incomplete.", out.getvalue())
                    self.assertNotIn(VALUE, out.getvalue())
        shown = self.with_terminal(None, check)
        self.assertNotIn(b"Prompt: ", shown, "nothing was asked for once echo could not be switched off")

    def test_without_a_terminal_nothing_is_read(self):
        with mock.patch.object(tool.os, "open", side_effect=OSError):
            with self.assertRaises(tool.Stop):
                tool.read_secret("Prompt: ")


if __name__ == "__main__":
    unittest.main()
