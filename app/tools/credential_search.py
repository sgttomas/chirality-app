#!/usr/bin/env python3
"""Search what the App wrote for a credential, without showing the credential.

For the person who holds the credential to run themselves, at a terminal, on
their own machine (DEL-01-05 AC-001, AC-003). Read the whole file first.

    python3 credential_search.py [--codex-auth FILE]... FOLDER [FOLDER]...

WHERE TO POINT IT
  It searches only the FOLDERs you give; it knows nothing of where the App
  writes. For the App these are: the App's data folder
  (~/Library/Application Support/<the build's identifier>); the system web
  view's data and caches for the same build (~/Library/WebKit/<name> and
  ~/Library/Caches/<name>, where <name> is the build's identifier, or the
  program's name for a development run that was not bundled); the records
  store; and the project folder. A folder you leave out is not searched and
  the result says nothing about it.

WHAT IT READS
  - Each FOLDER and everything under it: the name of every entry, the bytes of
    every regular file, and the target text of every symbolic link. No link is
    followed, at any level: what a link points to is not read. A FOLDER whose
    path is, or passes through, a symbolic link is refused; give its real path.
  - With --codex-auth FILE: that one Codex sign-in file (auth.json in an
    App-owned Codex home; never your own ~/.codex). Only two shapes are
    accepted, the two the App's homes produce: an API key in OPENAI_API_KEY, and
    a ChatGPT sign-in with id_token, access_token and refresh_token under
    "tokens". Those values are what is looked for. A file with any other
    credential field in use, any unknown field, or a field of the wrong kind is
    refused. The sign-in file itself, wherever it is met under a FOLDER
    (including by another name through a hard link), is not searched: it is
    Codex's custody. If it lies outside every FOLDER, nothing beside it is
    searched.
  - Values you type, read from your terminal with echo switched off. If echo
    cannot be switched off and checked, nothing is read.
  It writes no file, starts no process and opens no network connection. It
  changes two things and puts one back: it switches terminal echo off while you
  type and back on afterwards, and it switches off core dumps for itself.

WHAT IT PRINTS
  Counts, and the names of files in which a value was found. A value, an
  encoded form of one, or its length is not printed. A name is printed only if
  neither the name nor its printed form contains a value; otherwise it is
  counted. An error prints one fixed sentence, never the error's own text. If
  its output cannot be written (a closed pipe), it stops with status 2 and may
  print nothing.

WHEN THE RESULT IS "INCOMPLETE" (exit status 2)
  Anything it was asked to search that it did not read: a FOLDER that is
  missing, not a folder, or reached through a link; an entry that could not be
  read or classified, or that changed while being read; a special file (a
  pipe, socket or device). And anything it could not rely on: a sign-in file
  that is missing, is a link, or is not one of the two shapes; a value shorter
  than 8 bytes; no value; nothing read; echo that could not be switched off
  or back on; typing that ended without a line end; any unexpected error.
  "Incomplete" says the search did not finish. It does not say anything leaked.

  The two sign-in shapes are from the supplier's published source for this
  version. They have not been checked against a real sign-in file, which no one
  but you may open. Your first real run is also that check: if the real file
  differs, the result is "incomplete", as intended.

EXIT STATUS
  1  a value was found (stated even if the search was also incomplete)
  2  incomplete, and no value was found in what was read
  0  every entry under every FOLDER was read and compared and no value was found

WHAT IT LOOKS FOR, AND WHAT IT CANNOT ENSURE
  It finds a value written as plain bytes, or as base64 of those bytes
  (standard or URL-safe alphabet, with or without padding). It does not find a
  value written with JSON or percent escaping, in hex, split across lines, in
  another text encoding, compressed, encrypted, or inside a larger base64
  block. A result of 0 means "not found in those forms", not "absent".
  While it runs, values are in this process's memory; it cannot keep memory
  out of swap or erase it. It cannot stop another program changing files while
  it reads; a change it detects makes the result incomplete.

Python 3 standard library only; macOS or Linux.
"""
import base64
import json
import os
import stat
import sys

CHUNK = 1 << 20
MIN_VALUE = 8        # bytes; a shorter value matches too much to mean anything
MAX_AUTH = 1 << 20   # a sign-in file larger than this is not one
TOP_KEYS = {"auth_mode", "OPENAI_API_KEY", "tokens", "last_refresh", "agent_identity",
            "personal_access_token", "bedrock_api_key", "bedrock_access_keys"}
UNSUPPORTED = ("agent_identity", "personal_access_token", "bedrock_api_key", "bedrock_access_keys")
TOKEN_KEYS = ("id_token", "access_token", "refresh_token")
TOKEN_OTHER = {"account_id": str, "login_owner_id": str, "oauth_provenance": dict}
NOFOLLOW_DIR = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW
NOFOLLOW_FILE = os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK


class Stop(Exception):
    """Ends the run with one fixed sentence and exit status 2."""


def sign_in_credentials(parsed):
    """The credential values of a parsed sign-in file of an accepted shape, or None for any other shape."""
    if not isinstance(parsed, dict) or not set(parsed) <= TOP_KEYS:
        return None
    if any(parsed.get(key) is not None for key in UNSUPPORTED):
        return None
    for key in ("auth_mode", "last_refresh"):
        if not isinstance(parsed.get(key), (str, type(None))):
            return None
    values = []
    api_key = parsed.get("OPENAI_API_KEY")
    if isinstance(api_key, str):
        values.append(api_key)
    elif api_key is not None:
        return None
    tokens = parsed.get("tokens")
    if isinstance(tokens, dict):
        if not set(tokens) <= set(TOKEN_KEYS) | set(TOKEN_OTHER):
            return None
        if not all(isinstance(tokens.get(key), str) for key in TOKEN_KEYS):
            return None
        for key, kind in TOKEN_OTHER.items():
            if not isinstance(tokens.get(key), (kind, type(None))):
                return None
        provenance = tokens.get("oauth_provenance")
        if provenance is not None and (set(provenance) != {"issuer", "client_id"} or not all(isinstance(v, str) for v in provenance.values())):
            return None
        values += [tokens[key] for key in TOKEN_KEYS]
    elif tokens is not None:
        return None
    return values if values and all(values) else None


def forms(raw):
    """The byte patterns that stand for one value: itself and its base64 forms."""
    encoded = {base64.b64encode(raw), base64.urlsafe_b64encode(raw)}
    encoded |= {form.rstrip(b"=") for form in encoded}
    return sorted({raw} | encoded)


def within(data, patterns):
    """Indexes of the pattern groups that occur in these bytes."""
    return {index for index, group in enumerate(patterns) if any(p in data for p in group)}


def stream_contains(handle, patterns):
    """Indexes of the pattern groups that occur in the open file."""
    longest = max(len(p) for group in patterns for p in group)
    found, tail = set(), b""
    while True:
        block = handle.read(CHUNK)
        if not block:
            return found
        window = tail + block
        found |= within(window, patterns)
        tail = window[-(longest - 1):] if longest > 1 else b""


def printable(path, patterns):
    """The path as it may be printed, or None when the path or its printed form contains a value."""
    rendered = "".join(c if c.isprintable() and c != "\\" else "\\x%02x" % ord(c) if ord(c) < 256 else "\\u%04x" % ord(c)
                       for c in os.fsdecode(path))
    if within(os.fsencode(path), patterns) or within(rendered.encode("utf-8", "backslashreplace"), patterns):
        return None
    return rendered


def read_secret(prompt):
    """One line from the terminal with echo off. Stops the run unless echo was switched off, checked and put back."""
    import termios
    try:
        fd = os.open("/dev/tty", os.O_RDWR | os.O_NOCTTY)
    except OSError:
        raise Stop("No terminal to read from; run this at a terminal. Nothing was read.")
    line, complete, restored = b"", False, True
    try:
        try:
            before = termios.tcgetattr(fd)
        except termios.error:
            raise Stop("This terminal's settings cannot be read, so nothing was read. Use another terminal.")
        try:
            quiet = list(before)
            quiet[3] &= ~termios.ECHO
            termios.tcsetattr(fd, termios.TCSAFLUSH, quiet)
            if termios.tcgetattr(fd)[3] & termios.ECHO:
                raise termios.error
            os.write(fd, prompt.encode())
            while True:
                byte = os.read(fd, 1)
                if not byte:
                    break
                if byte == b"\n":
                    complete = True
                    break
                line += byte
            os.write(fd, b"\n")
        except termios.error:
            raise Stop("This terminal cannot switch echo off, so nothing was read. Use another terminal.")
        finally:
            try:
                termios.tcsetattr(fd, termios.TCSAFLUSH, before)
            except termios.error:
                restored = False
    finally:
        os.close(fd)
    if not restored:
        raise Stop("Terminal echo could not be switched back on; type: stty echo  and press Return. Nothing was searched.")
    if not complete:
        raise Stop("Typing ended without a line end, so the value was not used. Nothing was searched.")
    return line.rstrip(b"\r")


def read_sign_in(path):
    """((dev, ino), credential values as bytes) of a named sign-in file."""
    try:
        fd = os.open(path, NOFOLLOW_FILE)
    except OSError:
        raise Stop("A sign-in file given with --codex-auth is missing, is a symbolic link or cannot be opened. Nothing was searched.")
    try:
        info = os.fstat(fd)
        if not stat.S_ISREG(info.st_mode) or info.st_size > MAX_AUTH:
            raise Stop("A file given with --codex-auth is not a sign-in file. Nothing was searched.")
        data = b""
        while len(data) <= MAX_AUTH:
            block = os.read(fd, CHUNK)
            if not block:
                break
            data += block
    except OSError:
        raise Stop("A sign-in file given with --codex-auth could not be read. Nothing was searched.")
    finally:
        os.close(fd)
    try:
        values = sign_in_credentials(json.loads(data.decode("utf-8")))
        raws = None if values is None else [value.encode("utf-8") for value in values]
    except (ValueError, RecursionError):
        raws = None
    if raws is None:
        raise Stop("A sign-in file given with --codex-auth is not one of the two shapes this tool accepts. Nothing was searched. "
                   "This does not mean anything leaked.")
    if any(len(raw) < MIN_VALUE for raw in raws):
        raise Stop("A credential in a sign-in file is too short to search for. Nothing was searched.")
    return (info.st_dev, info.st_ino), raws


def arguments(argv):
    usage = "Usage: credential_search.py [--codex-auth FILE]... FOLDER [FOLDER]...  (a value is never an argument)"
    folders, auths, index = [], [], 0
    while index < len(argv):
        if argv[index] == "--codex-auth" and index + 1 < len(argv):
            auths.append(argv[index + 1])
            index += 2
        elif argv[index].startswith("-"):
            raise Stop(usage)
        else:
            folders.append(argv[index])
            index += 1
    if not folders:
        raise Stop(usage)
    return folders, auths


class Search:
    def __init__(self, patterns, excluded):
        self.patterns, self.excluded = patterns, excluded
        self.hits = [[] for _ in patterns]         # printable names of files containing each value
        self.hits_withheld = [0 for _ in patterns]  # the same, where the name may not be printed
        self.name_hits = [0 for _ in patterns]      # entries whose own name contains each value
        self.link_hits = [0 for _ in patterns]      # links whose target text contains each value
        self.unread, self.unread_withheld = [], 0
        self.files = self.links = self.folders = self.special = self.sign_in_met = 0

    def not_read(self, path):
        name = printable(path, self.patterns)
        if name is None:
            self.unread_withheld += 1
        else:
            self.unread.append(name)

    def folder(self, fd, path):
        """Everything in the open folder `fd`, shown as `path`. Closes nothing it did not open."""
        self.folders += 1
        try:
            with os.scandir(fd) as entries:
                names = sorted(entry.name for entry in entries)
        except OSError:
            self.not_read(path)
            return
        for name in names:
            shown = os.path.join(path, name)
            for index in within(os.fsencode(name), self.patterns):
                self.name_hits[index] += 1
            try:
                info = os.stat(name, dir_fd=fd, follow_symlinks=False)
                if stat.S_ISLNK(info.st_mode):
                    for index in within(os.fsencode(os.readlink(name, dir_fd=fd)), self.patterns):
                        self.link_hits[index] += 1
                    self.links += 1
                elif stat.S_ISDIR(info.st_mode):
                    child = os.open(name, NOFOLLOW_DIR, dir_fd=fd)
                    try:
                        now = os.fstat(child)
                        if (now.st_dev, now.st_ino) != (info.st_dev, info.st_ino):
                            raise OSError
                        self.folder(child, shown)
                    finally:
                        os.close(child)
                elif stat.S_ISREG(info.st_mode):
                    child = os.open(name, NOFOLLOW_FILE, dir_fd=fd)
                    with os.fdopen(child, "rb") as handle:
                        now = os.fstat(handle.fileno())
                        if not stat.S_ISREG(now.st_mode) or (now.st_dev, now.st_ino) != (info.st_dev, info.st_ino):
                            raise OSError
                        if (now.st_dev, now.st_ino) in self.excluded:
                            self.sign_in_met += 1
                            continue
                        found = stream_contains(handle, self.patterns)
                    self.files += 1
                    for index in found:
                        name_shown = printable(shown, self.patterns)
                        if name_shown is None:
                            self.hits_withheld[index] += 1
                        else:
                            self.hits[index].append(name_shown)
                else:
                    self.special += 1
            except OSError:
                self.not_read(shown)


def run(argv, lines):
    try:
        import resource
        resource.setrlimit(resource.RLIMIT_CORE, (0, 0))
        core = True
    except (ImportError, ValueError, OSError):
        core = False
    folders, auths = arguments(argv)
    roots = []
    try:
        for folder in folders:
            real = os.path.abspath(folder)
            if os.path.realpath(real) != real:
                raise Stop("A folder to search is, or is reached through, a symbolic link. Give its real path. Nothing was searched.")
            try:
                roots.append((os.open(real, NOFOLLOW_DIR), real))
            except OSError:
                raise Stop("A folder to search is missing, is not a folder or cannot be opened. Nothing was searched.")

        excluded, raws, kinds = set(), [], []
        for auth in auths:
            identity, values = read_sign_in(auth)
            excluded.add(identity)
            for raw in values:
                if raw not in raws:
                    raws.append(raw)
                    kinds.append("credential of a sign-in file")
        while True:
            typed = read_secret("Value to look for (not shown; empty line to finish): ")
            if not typed:
                break
            if len(typed) < MIN_VALUE:
                raise Stop("A typed value is too short to search for (fewer than 8 bytes). Nothing was searched.")
            if typed not in raws:
                raws.append(typed)
                kinds.append("typed at the keyboard")
        if not raws:
            raise Stop("No value was given. Nothing was searched.")

        search = Search([forms(raw) for raw in raws], excluded)
        for fd, real in roots:
            for index in within(os.fsencode(real), search.patterns):
                search.name_hits[index] += 1
            search.folder(fd, real)
    finally:
        for fd, _ in roots:
            try:
                os.close(fd)
            except OSError:
                pass

    s = search
    lines.append("Read and compared: %d regular file(s), %d symbolic link(s) (their target text only), the names of all entries in %d folder(s). "
                 "Values looked for: %d." % (s.files, s.links, s.folders, len(raws)))
    any_hit = False
    for index, kind in enumerate(kinds):
        in_files = len(s.hits[index]) + s.hits_withheld[index]
        if in_files or s.name_hits[index] or s.link_hits[index]:
            any_hit = True
            lines.append("Value %d (%s): FOUND." % (index + 1, kind))
            if in_files:
                lines.append("  in the contents of %d file(s):" % in_files)
                lines.extend("    " + name for name in s.hits[index])
                if s.hits_withheld[index]:
                    lines.append("    and %d whose name cannot be printed without showing a value." % s.hits_withheld[index])
            if s.name_hits[index]:
                lines.append("  in the name of %d file(s) or folder(s); those names are not printed." % s.name_hits[index])
            if s.link_hits[index]:
                lines.append("  in the target text of %d symbolic link(s)." % s.link_hits[index])
        else:
            lines.append("Value %d (%s): not found in what was read." % (index + 1, kind))
    if auths:
        lines.append("Sign-in file(s) given: %d; met under the folders and not searched, as Codex's custody: %d time(s)." % (len(auths), s.sign_in_met))
    if not core:
        lines.append("Note: core dumps could not be switched off for this run.")
    not_read = len(s.unread) + s.unread_withheld
    incomplete = bool(not_read or s.special or s.files + s.links == 0)
    if not_read:
        lines.append("INCOMPLETE: %d file(s) or folder(s) could not be read, or changed while being read%s" % (not_read, ":" if s.unread else "."))
        lines.extend("  " + name for name in s.unread)
        if s.unread_withheld:
            lines.append("  and %d whose name cannot be printed without showing a value." % s.unread_withheld)
    if s.special:
        lines.append("INCOMPLETE: %d special file(s) (pipes, sockets or devices) were not read." % s.special)
    if s.files + s.links == 0:
        lines.append("INCOMPLETE: nothing was read.")
    if any_hit:
        lines.append("Result: a value was FOUND." + (" The search was also incomplete." if incomplete else ""))
        return 1
    if incomplete:
        lines.append("Result: incomplete. The search did not finish; this does not say that anything leaked.")
        return 2
    lines.append("Result: every entry under the folder(s) given was read and compared, and no value was found as plain bytes or as base64 "
                 "(standard or URL-safe).")
    lines.append("Not covered: a value written escaped, percent-encoded, in hex, split across lines, in another text encoding, compressed, "
                 "encrypted or inside a larger base64 block; and what the symbolic links point to.")
    return 0


def main(argv=None):
    lines = []
    try:
        code = run(sys.argv[1:] if argv is None else argv, lines)
    except Stop as stop:
        lines, code = [stop.args[0], "Result: incomplete. This does not say that anything leaked."], 2
    except KeyboardInterrupt:
        lines, code = ["", "Stopped at your request. Result: incomplete."], 2
    except BaseException:  # never print an error's own text: it could quote a value
        lines, code = ["Stopped by an unexpected error. Result: incomplete. Nothing of a value was printed."], 2
    try:
        sys.stdout.write("\n".join(lines) + "\n")
        sys.stdout.flush()
    except BaseException:  # output cannot be written: say nothing more, and do not let Python report it
        try:
            os.dup2(os.open(os.devnull, os.O_WRONLY), sys.stdout.fileno())
        except BaseException:
            pass
        return 2
    return code


if __name__ == "__main__":
    sys.exit(main())
