"""app/tools/credential_search.py, with invented values only.

The tool may call a search clean only when everything it was asked to search
was read and compared. Each way an earlier version failed an independent
review has a test here, named for the failure.
"""
import base64
import importlib.util
import io
import os
import pathlib
import pty
import subprocess
import sys
import tempfile
import termios
import threading
import unittest
from contextlib import redirect_stderr, redirect_stdout
from unittest import mock

TOOL = pathlib.Path(__file__).resolve().parents[1] / "tools" / "credential_search.py"
SPEC = importlib.util.spec_from_file_location("credential_search", TOOL)
tool = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(tool)

VALUE = "INVENTED-KEY-0123456789-abcdef"
TOKENS = {"id_token": "INVENTED-ID-" + "i" * 30, "access_token": "INVENTED-ACCESS-" + "a" * 30, "refresh_token": "INVENTED-REFRESH-" + "r" * 30}
CHATGPT = {"auth_mode": "chatgpt", "OPENAI_API_KEY": None, "tokens": dict(TOKENS, account_id="invented-account"), "last_refresh": "2026-01-01T00:00:00Z"}


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


def real_folder():
    """A temporary folder by its real path (the tool refuses a path through a link, such as /tmp on macOS)."""
    holder = tempfile.TemporaryDirectory()
    return holder, os.path.realpath(holder.name)


class Matching(unittest.TestCase):
    def test_plain_bytes_and_each_base64_form_are_found_and_nothing_shorter_is(self):
        raw = b"??>~~?" * 3  # standard and URL-safe base64 of this differ
        self.assertNotEqual(base64.b64encode(raw), base64.urlsafe_b64encode(raw))
        padded = VALUE.encode() + b"x"
        self.assertTrue(base64.b64encode(padded).endswith(b"="))
        cases = {
            "plain": (raw, b"x" + raw + b"y", True),
            "standard": (raw, b"aa" + base64.b64encode(raw) + b"zz", True),
            "urlsafe": (raw, base64.urlsafe_b64encode(raw), True),
            "padded": (padded, base64.b64encode(padded), True),
            "unpadded": (padded, base64.b64encode(padded).rstrip(b"="), True),
            "split": (raw, b"p" * (tool.CHUNK - 7) + raw + b"q" * 50, True),
            "absent": (raw, b"nothing here " * 1000, False),
            "prefix-only": (raw, raw[:-1], False),
            "raw-padding-kept": (b"INVENTED-ENDS-IN=", b"INVENTED-ENDS-IN", False),
        }
        for name, (value, content, expected) in cases.items():
            self.assertEqual(tool.stream_contains(io.BytesIO(content), [tool.forms(value)]), {0} if expected else set(), name)

    def test_a_block_boundary_never_hides_a_value(self):
        with mock.patch.object(tool, "CHUNK", 8):
            for length in (1, 7, 8, 9, 17, 40):
                value = bytes(range(65, 65 + length))
                for offset in range(0, 20):
                    self.assertEqual(tool.stream_contains(io.BytesIO(b"." * offset + value + b"." * 11), [[value]]), {0}, (length, offset))


class SignInFile(unittest.TestCase):
    def test_exactly_two_shapes_are_accepted_and_their_credentials_taken(self):
        self.assertEqual(tool.sign_in_credentials(CHATGPT), list(TOKENS.values()))
        self.assertEqual(tool.sign_in_credentials({"OPENAI_API_KEY": "sk-invented-" + "k" * 20}), ["sk-invented-" + "k" * 20])
        both = dict(CHATGPT, OPENAI_API_KEY="sk-invented-" + "k" * 20)
        self.assertEqual(tool.sign_in_credentials(both), ["sk-invented-" + "k" * 20] + list(TOKENS.values()))
        with_provenance = dict(CHATGPT, tokens=dict(CHATGPT["tokens"], oauth_provenance={"issuer": "https://invented.invalid", "client_id": "invented"}, login_owner_id="invented"))
        self.assertEqual(tool.sign_in_credentials(with_provenance), list(TOKENS.values()))

    def test_a_recognised_fragment_never_makes_another_shape_acceptable(self):
        """Round 2: one recognised field beside an unexpected one passed, so the unexpected credential was never compared."""
        refused = {
            "labels only": {"auth_mode": "chatgpt", "last_refresh": "2026-01-01T00:00:00Z"},
            "bedrock label": {"bedrock_access_keys": {"region": "us-east-1"}},
            "bedrock beside a key": {"OPENAI_API_KEY": "sk-invented-" + "k" * 20, "bedrock_api_key": {"api_key": "x" * 30}},
            "refresh token as an object": {"tokens": dict(TOKENS, refresh_token={"new": "NEWSECRET"})},
            "refresh token as a list": {"tokens": dict(TOKENS, refresh_token=["NEWSECRET"])},
            "a token missing": {"tokens": {"id_token": TOKENS["id_token"], "access_token": TOKENS["access_token"]}},
            "an empty token": {"tokens": dict(TOKENS, access_token="")},
            "empty tokens": {"tokens": {}},
            "agent identity as text": dict(CHATGPT, agent_identity="x" * 40),
            "agent identity as a record": dict(CHATGPT, agent_identity={"agent_private_key": "shortkey9"}),
            "personal access token": dict(CHATGPT, personal_access_token="x" * 40),
            "unknown top-level field": dict(CHATGPT, new_secret="x" * 40),
            "unknown token field": {"tokens": dict(TOKENS, session_key="x" * 40)},
            "key of the wrong kind": {"OPENAI_API_KEY": ["sk-invented"]},
            "tokens of the wrong kind": {"OPENAI_API_KEY": "sk-invented-" + "k" * 20, "tokens": ["a"]},
            "provenance with an extra field": {"tokens": dict(TOKENS, oauth_provenance={"issuer": "i", "client_id": "c", "secret": "s"})},
            "mode of the wrong kind": dict(CHATGPT, auth_mode={"x": 1}),
            "empty key only": {"OPENAI_API_KEY": ""},
            "a list": [1, 2], "text": "text", "nothing": None,
        }
        for name, parsed in refused.items():
            self.assertIsNone(tool.sign_in_credentials(parsed), name)

    def test_a_refused_sign_in_file_ends_incomplete_even_with_a_clean_folder_beside_it(self):
        holder, folder = real_folder()
        with holder:
            write(os.path.join(folder, "clean.txt"), "clean")
            cases = {"region.json": '{"bedrock_access_keys": {"region": "us-east-1"}}', "not-json": "{", "list.json": "[1]",
                     "short.json": '{"OPENAI_API_KEY": "short"}', "bad-text.json": '{"OPENAI_API_KEY": "\\ud800%s"}' % ("k" * 30),
                     "deep.json": "[" * 100000}
            for name, content in cases.items():
                auth = os.path.join(folder, name)
                write(auth, content)
                code, text = run(["--codex-auth", auth, folder])
                self.assertEqual(code, 2, name)
                self.assertIn("Nothing was searched.", text, name)
                self.assertNotIn("no value was found", text, name)
                self.assertNotIn("ud800", text.lower(), name)
                os.remove(auth)
            target, link = os.path.join(folder, "real.json"), os.path.join(folder, "link.json")
            write(target, '{"OPENAI_API_KEY": "%s"}' % VALUE)
            os.symlink(target, link)
            self.assertEqual(run(["--codex-auth", link, folder])[0], 2)
            self.assertEqual(run(["--codex-auth", os.path.join(folder, "missing.json"), folder])[0], 2)

    def test_only_the_sign_in_file_itself_is_left_unsearched(self):
        """Round 1: excluding its whole folder hid an App-written file beside it."""
        import json
        holder, folder = real_folder()
        with holder:
            home = os.path.join(folder, "home")
            os.mkdir(home)
            auth = os.path.join(home, "auth.json")
            write(auth, json.dumps(CHATGPT))
            os.link(auth, os.path.join(folder, "hard-link-to-it"))
            write(os.path.join(home, "app-written.log"), "x" + TOKENS["refresh_token"] + "y")
            code, text = run(["--codex-auth", auth, folder])
            self.assertEqual(code, 1)
            self.assertIn("app-written.log", text)
            self.assertNotIn("auth.json", text)
            self.assertIn("not searched, as Codex's custody: 2 time(s)", text)
            for token in TOKENS.values():
                self.assertNotIn(token, text)
            os.remove(os.path.join(home, "app-written.log"))
            write(os.path.join(home, "clean.txt"), "clean")
            code, text = run(["--codex-auth", auth, folder])
            self.assertEqual(code, 0, text)
            self.assertIn("1 regular file(s)", text)


class Results(unittest.TestCase):
    def test_a_file_that_cannot_be_read_makes_a_search_with_no_hit_incomplete(self):
        holder, folder = real_folder()
        with holder:
            write(os.path.join(folder, "clean.txt"), "clean")
            locked = os.path.join(folder, "locked.txt")
            write(locked, VALUE)
            os.chmod(locked, 0)
            sub = os.path.join(folder, "closed")
            os.mkdir(sub)
            os.chmod(sub, 0)
            try:
                code, text = run([folder], [VALUE.encode()])
            finally:
                os.chmod(locked, 0o600), os.chmod(sub, 0o700)
            self.assertEqual(code, 2)
            self.assertIn("INCOMPLETE: 2 file(s) or folder(s) could not be read", text)
            self.assertIn("locked.txt", text)
            self.assertIn("Result: incomplete.", text)
            self.assertNotIn("no value was found", text)

    def test_a_hit_is_reported_by_number_and_no_value_form_or_length_is_printed(self):
        holder, folder = real_folder()
        with holder:
            write(os.path.join(folder, "leak.log"), "x" + VALUE + "y")
            write(os.path.join(folder, "encoded.bin"), base64.b64encode(VALUE.encode()))
            code, text = run([folder], [VALUE.encode()])
            self.assertEqual(code, 1)
            self.assertIn("Value 1 (typed at the keyboard): FOUND.", text)
            self.assertIn("in the contents of 2 file(s):", text)
            for form in tool.forms(VALUE.encode()):
                self.assertNotIn(form.decode(), text)
            self.assertNotIn(str(len(VALUE)), text.replace(folder, ""))

    def test_a_hit_takes_precedence_and_says_when_the_search_was_also_incomplete(self):
        holder, folder = real_folder()
        with holder:
            write(os.path.join(folder, "leak.log"), VALUE)
            os.mkfifo(os.path.join(folder, "pipe"))
            code, text = run([folder], [VALUE.encode()])
            self.assertEqual(code, 1)
            self.assertIn("Result: a value was FOUND. The search was also incomplete.", text)

    def test_a_name_that_contains_the_value_is_a_hit_and_is_never_printed(self):
        """Round 1: such a name was printed. Round 2: a name whose escaped form spells the value was printed."""
        holder, folder = real_folder()
        with holder:
            os.mkdir(os.path.join(folder, VALUE))
            write(os.path.join(folder, VALUE, "inside.txt"), VALUE)
            write(os.path.join(folder, "named-" + base64.b64encode(VALUE.encode()).decode() + ".log"), "clean")
            write(os.path.join(folder, "line\nbreak\x1b[31m.txt"), VALUE)
            code, text = run([folder], [VALUE.encode()])
            self.assertEqual(code, 1)
            self.assertNotIn(VALUE, text)
            self.assertNotIn(base64.b64encode(VALUE.encode()).decode(), text)
            self.assertIn("in the name of 2 file(s) or folder(s); those names are not printed.", text)
            self.assertIn("and 1 whose name cannot be printed without showing a value.", text)
            self.assertIn("line\\x0abreak\\x1b[31m.txt", text)
            self.assertNotIn("\x1b", text)
        # The escaped form of a name spells the value: the name's raw bytes do not contain it.
        escaped = "ABCDEF\\x0aUVWXYZ"
        holder, folder = real_folder()
        with holder:
            write(os.path.join(folder, "ABCDEF\nUVWXYZ"), escaped)
            locked = os.path.join(folder, "ABCDEF\nUVWXYZ-locked")
            write(locked, "x")
            os.chmod(locked, 0)
            try:
                code, text = run([folder], [escaped.encode()])
            finally:
                os.chmod(locked, 0o600)
            self.assertEqual(code, 1)
            self.assertNotIn(escaped, text)
            self.assertIn("and 1 whose name cannot be printed without showing a value.", text)
            self.assertEqual(text.count("whose name cannot be printed"), 2, "the hit and the unreadable entry are both withheld")
        self.assertIsNone(tool.printable("a\\b", [[b"a\\x5cb"]]), "a backslash is escaped, so the printed form is checked too")
        # A value with a control byte: the name's raw bytes contain it and its printed form does not.
        self.assertIsNone(tool.printable("pre-ABCDEF\x01UVWXYZ-post", [[b"ABCDEF\x01UVWXYZ"]]))
        self.assertEqual(tool.printable(os.fsdecode(b"bad\xff"), [[b"zzzzzzzz"]]), "bad\\udcff")

    def test_no_link_is_followed_at_any_level_and_a_linked_folder_is_refused_however_it_is_spelled(self):
        """Round 1: a linked folder was followed. Round 2: "link/", "link/." and a folder beneath a link still were."""
        holder, folder = real_folder()
        with holder:
            outside, inside = os.path.join(folder, "outside"), os.path.join(folder, "inside")
            os.mkdir(outside), os.mkdir(inside), os.mkdir(os.path.join(outside, "deeper"))
            write(os.path.join(outside, "secret.txt"), VALUE)
            write(os.path.join(inside, "clean.txt"), "clean")
            os.symlink(os.path.join(outside, "secret.txt"), os.path.join(inside, "file-link"))
            os.symlink(outside, os.path.join(inside, "folder-link"))
            code, text = run([inside], [VALUE.encode()])
            self.assertEqual(code, 0, text)
            self.assertIn("1 regular file(s), 2 symbolic link(s) (their target text only)", text)
            self.assertIn("and what the symbolic links point to", text)
            root_link = os.path.join(folder, "root-link")
            os.symlink(outside, root_link)
            for spelling in (root_link, root_link + "/", root_link + "/.", os.path.join(root_link, "deeper"), os.path.join(inside, "folder-link", "deeper")):
                code, text = run([spelling], [VALUE.encode()])
                self.assertEqual(code, 2, spelling)
                self.assertIn("reached through, a symbolic link", text, spelling)
            self.assertEqual(run([os.path.join(folder, "missing")], [VALUE.encode()])[0], 2)
            self.assertEqual(run([os.path.join(inside, "clean.txt")], [VALUE.encode()])[0], 2)
            # A link whose own target text holds the value is a hit: that text is something the App wrote.
            os.symlink("/invented/" + VALUE, os.path.join(inside, "telling-link"))
            code, text = run([inside], [VALUE.encode()])
            self.assertEqual(code, 1)
            self.assertIn("in the target text of 1 symbolic link(s).", text)
            self.assertNotIn(VALUE, text)

    def test_a_folder_swapped_for_a_link_while_it_is_searched_is_not_followed_and_is_incomplete(self):
        holder, folder = real_folder()
        with holder:
            outside, inside = os.path.join(folder, "outside"), os.path.join(folder, "inside")
            os.mkdir(outside), os.mkdir(inside), os.mkdir(os.path.join(inside, "sub"))
            write(os.path.join(outside, "secret.txt"), VALUE)
            write(os.path.join(inside, "clean.txt"), "clean")
            real_stat = os.stat

            def swapping(name, *rest, **named):
                info = real_stat(name, *rest, **named)
                if name == "sub" and named.get("dir_fd") is not None:
                    os.rmdir(os.path.join(inside, "sub"))
                    os.symlink(outside, os.path.join(inside, "sub"))
                return info
            with mock.patch.object(tool.os, "stat", swapping):
                code, text = run([inside], [VALUE.encode()])
            self.assertEqual(code, 2, text)
            self.assertIn("could not be read, or changed while being read", text)
            self.assertNotIn("FOUND", text)

    def test_a_folder_swapped_for_another_folder_while_it_is_searched_is_incomplete(self):
        holder, folder = real_folder()
        with holder:
            inside, other = os.path.join(folder, "inside"), os.path.join(folder, "other")
            os.mkdir(inside), os.mkdir(other), os.mkdir(os.path.join(inside, "sub"))
            write(os.path.join(inside, "clean.txt"), "clean")
            write(os.path.join(other, "clean2.txt"), "clean")
            real_stat = os.stat

            def swapping(name, *rest, **named):
                info = real_stat(name, *rest, **named)
                if name == "sub" and named.get("dir_fd") is not None:
                    os.rmdir(os.path.join(inside, "sub"))
                    os.rename(other, os.path.join(inside, "sub"))
                return info
            with mock.patch.object(tool.os, "stat", swapping):
                code, text = run([inside], [VALUE.encode()])
            self.assertEqual(code, 2, text)
            self.assertIn("changed while being read", text)

    def test_a_special_file_makes_the_result_incomplete(self):
        holder, folder = real_folder()
        with holder:
            write(os.path.join(folder, "clean.txt"), "clean")
            os.mkfifo(os.path.join(folder, "pipe"))
            code, text = run([folder], [VALUE.encode()])
            self.assertEqual(code, 2)
            self.assertIn("INCOMPLETE: 1 special file(s)", text)
            self.assertNotIn("no value was found", text)

    def test_nothing_is_called_clean_without_a_value_something_read_or_a_usable_argument(self):
        holder, folder = real_folder()
        with holder:
            empty = os.path.join(folder, "empty")
            os.mkdir(empty)
            write(os.path.join(folder, "a.txt"), "a")
            for args, typed, expect in (([folder], [], "No value was given."), ([folder], [b"short"], "too short to search for"),
                                        ([empty], [VALUE.encode()], "INCOMPLETE: nothing was read."), ([], [], "Usage:"),
                                        (["--secret=" + VALUE, folder], [], "Usage:")):
                code, text = run(args, typed)
                self.assertEqual(code, 2, expect)
                self.assertIn(expect, text)
                self.assertNotIn(VALUE, text)
                self.assertNotIn("no value was found", text)

    def test_an_unexpected_error_prints_a_fixed_sentence_and_never_its_own_text(self):
        holder, folder = real_folder()
        with holder:
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

    def test_output_that_cannot_be_written_ends_with_status_2_and_no_traceback(self):
        """Round 2: a closed pipe produced a traceback."""
        holder, folder = real_folder()
        with holder:
            reader, writer = os.pipe()
            os.close(reader)
            try:
                done = subprocess.run([sys.executable, "-I", str(TOOL), os.path.join(folder, "missing")], stdin=subprocess.DEVNULL,
                                      stdout=writer, stderr=subprocess.PIPE, timeout=30)
            finally:
                os.close(writer)
            self.assertEqual(done.returncode, 2)
            self.assertEqual(done.stderr, b"")


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
                # A prompt that should never have appeared is answered with a line, so a broken tool fails its test instead of waiting.
                os.write(master, typed if typed is not None else b"UNEXPECTED-PROMPT-ANSWER\n")
                while True:  # keep reading so nothing the tool writes to the terminal can block it
                    block = os.read(master, 4096)
                    if not block:
                        break
                    shown += block
            except OSError:
                pass
            seen.append(shown)

        helper = threading.Thread(target=person, daemon=True)
        helper.start()
        try:
            with mock.patch.object(tool.os, "open", lambda path, flags, *rest, **named: os.dup(slave) if path == "/dev/tty" else real_open(path, flags, *rest, **named)):
                check(slave)
        finally:
            echo_on = bool(termios.tcgetattr(slave)[3] & termios.ECHO)
            os.close(slave)
            helper.join(5)
            os.close(master)
            helper.join(5)
        return (seen[0] if seen else b""), echo_on

    def test_a_typed_value_is_read_with_echo_off_and_echo_is_put_back(self):
        result = []
        shown, echo_on = self.with_terminal(VALUE.encode() + b"\n", lambda slave: result.append(tool.read_secret("Prompt: ")))
        self.assertEqual(result, [VALUE.encode()])
        self.assertIn(b"Prompt: ", shown)
        self.assertNotIn(VALUE.encode(), shown, "the terminal did not echo the value")
        self.assertTrue(echo_on)

    def test_a_terminal_that_cannot_switch_echo_off_stops_before_anything_is_asked(self):
        """Round 1: the standard prompt fell back and echoed the value."""
        real_set = termios.tcsetattr
        for failure in ("refused", "ignored"):
            def setter(fd, when, attributes, failure=failure):
                if failure == "refused" and not attributes[3] & termios.ECHO:
                    raise termios.error(25, "refused")
                if failure == "ignored" and not attributes[3] & termios.ECHO:
                    return None
                return real_set(fd, when, attributes)

            def check(slave):
                with mock.patch.object(termios, "tcsetattr", setter):
                    with self.assertRaises(tool.Stop) as stopped:
                        tool.read_secret("Prompt: ")
                self.assertIn("cannot switch echo off, so nothing was read", stopped.exception.args[0])
            shown, echo_on = self.with_terminal(None, check)
            self.assertNotIn(b"Prompt: ", shown, failure)
            self.assertTrue(echo_on, failure)

    def test_echo_is_put_back_when_the_check_after_switching_it_off_fails(self):
        """Round 2: a failure between switching echo off and checking it left echo off."""
        real_get = termios.tcgetattr
        calls = []

        def getter(fd):
            calls.append(fd)
            if len(calls) == 2:
                raise termios.error(5, "failed after the change")
            return real_get(fd)

        def check(slave):
            with mock.patch.object(termios, "tcgetattr", getter):
                with self.assertRaises(tool.Stop):
                    tool.read_secret("Prompt: ")
        shown, echo_on = self.with_terminal(None, check)
        self.assertTrue(echo_on, "echo was restored")
        self.assertNotIn(b"Prompt: ", shown)

    def test_echo_that_cannot_be_put_back_is_said_and_the_value_is_not_used(self):
        real_set = termios.tcsetattr

        def setter(fd, when, attributes):
            if attributes[3] & termios.ECHO:
                raise termios.error(5, "cannot restore")
            return real_set(fd, when, attributes)

        def check(slave):
            with mock.patch.object(termios, "tcsetattr", setter):
                with self.assertRaises(tool.Stop) as stopped:
                    tool.read_secret("Prompt: ")
            self.assertIn("stty echo", stopped.exception.args[0])
            real_set(slave, termios.TCSANOW, [a | termios.ECHO if i == 3 else a for i, a in enumerate(termios.tcgetattr(slave))])
        self.with_terminal(VALUE.encode() + b"\n", check)

    def test_typing_that_ends_without_a_line_end_is_not_used(self):
        def check(slave):
            real_read = os.read  # the tool reads one byte at a time; the test's own reads are left alone
            with mock.patch.object(tool.os, "read", lambda fd, count: b"" if count == 1 else real_read(fd, count)):
                with self.assertRaises(tool.Stop) as stopped:
                    tool.read_secret("Prompt: ")
            self.assertIn("ended without a line end", stopped.exception.args[0])
        self.with_terminal(None, check)

    def test_without_a_terminal_nothing_is_read(self):
        with mock.patch.object(tool.os, "open", side_effect=OSError):
            with self.assertRaises(tool.Stop):
                tool.read_secret("Prompt: ")


if __name__ == "__main__":
    unittest.main()
