#!/usr/bin/env python3
"""Search files the App wrote for a credential, without showing the credential.

For the person who holds the credential to run themselves, at a terminal, on
their own machine (DEL-01-05 AC-001, AC-003). Read the whole file before
running it.

    python3 credential_search.py [--codex-auth FILE]... FOLDER [FOLDER]...

WHAT IT READS
  - The folders given, and every regular file under them, opened read-only
    without following symbolic links. A folder given as a symbolic link is
    refused.
  - With --codex-auth FILE: that one Codex sign-in file (auth.json in an
    App-owned Codex home, never your own ~/.codex). Its credential fields are
    taken by name: OPENAI_API_KEY, personal_access_token, agent_identity, the
    id, access and refresh tokens under "tokens", and any text under
    bedrock_api_key or bedrock_access_keys. Any other text value of 20
    characters or more in it is also looked for and reported separately as
    "may not be a credential". The sign-in file itself is not searched (it is
    Codex's custody); every other file in its folder is.
  - Values you type, read from your terminal with echo switched off. If echo
    cannot be switched off, nothing is read and the tool stops.
  It writes nothing, starts no process and opens no network connection.

WHAT IT PRINTS
  For each value, by number only: how many files contain it, and their names.
  Then counts of what was and was not read. It does not print a value, an
  encoded form of one, or its length. A file name that itself contains a value
  in a searched form is counted and not printed. An error prints a fixed
  sentence, never the error's own text.

WHAT MAKES THE RESULT INCOMPLETE (exit status 2)
  A folder that is missing, not a folder, or a symbolic link; a file or folder
  that could not be read or classified; a sign-in file that is missing, is a
  symbolic link, is not in the shape this tool recognises, or holds none of the
  credential fields named above; a value shorter than 8 bytes; no value given;
  no file read; echo that cannot be switched off; any unexpected error. An
  "incomplete" result says the search did not finish. It does not say that
  anything leaked.

  The field names above are from the supplier's published source and have not
  been checked against a real sign-in file. The first real run is also that
  check: if the file's shape differs, "incomplete" is the expected result.

WHAT IT LOOKS FOR, AND WHAT IT CANNOT ENSURE
  It finds a value stored as plain bytes, or as base64 of those bytes (standard
  or URL-safe alphabet, with or without padding). It does not find a value
  stored with JSON or percent escaping, in hex, split across lines, in another
  text encoding, compressed, encrypted, or inside a larger base64 block.
  Symbolic links are not followed, so what they point to is not searched.
  While it runs, values are held in this process's memory; it switches off
  core dumps where it can, but cannot keep memory out of swap or erase it, and
  cannot stop another program from changing files while it reads them.

Exit status: 0 when every regular file found was read and no value was found
in the forms above; 1 when a value was found; 2 when the result is incomplete.

Python 3 standard library only.
"""
import base64
import json
import os
import stat
import sys

CHUNK = 1 << 20
MIN_VALUE = 8          # bytes; anything shorter matches too much to mean anything
MIN_OTHER = 20         # characters; other text in a sign-in file shorter than this is a label
MAX_AUTH = 1 << 20     # a sign-in file larger than this is not one
CREDENTIAL_KEYS = ("OPENAI_API_KEY", "personal_access_token", "agent_identity")
TOKEN_KEYS = ("id_token", "access_token", "refresh_token")
CREDENTIAL_TREES = ("bedrock_api_key", "bedrock_access_keys")


class Stop(Exception):
    """Ends the run with one fixed sentence and exit status 2."""


def text_leaves(node):
    if isinstance(node, str):
        yield node
    elif isinstance(node, dict):
        for value in node.values():
            yield from text_leaves(value)
    elif isinstance(node, list):
        for value in node:
            yield from text_leaves(value)


def sign_in_values(parsed):
    """(credential values, other long values) of a parsed sign-in file, or None if its shape is not recognised."""
    if not isinstance(parsed, dict):
        return None
    tokens = parsed.get("tokens")
    if tokens is not None and not isinstance(tokens, dict):
        return None
    credentials = [parsed[key] for key in CREDENTIAL_KEYS if isinstance(parsed.get(key), str)]
    credentials += [tokens[key] for key in TOKEN_KEYS if isinstance((tokens or {}).get(key), str)]
    for key in CREDENTIAL_TREES:
        credentials += list(text_leaves(parsed.get(key)))
    credentials = [value for value in dict.fromkeys(credentials) if value]
    others = [value for value in dict.fromkeys(text_leaves(parsed)) if len(value) >= MIN_OTHER and value not in credentials]
    return credentials, others


def forms(raw):
    """The byte patterns that stand for one value: itself and its base64 forms."""
    encoded = {base64.b64encode(raw), base64.urlsafe_b64encode(raw)}
    encoded |= {form.rstrip(b"=") for form in encoded}
    return sorted({raw} | encoded)


def stream_contains(handle, patterns):
    """Indexes of the pattern groups that occur in the open file."""
    longest = max(len(p) for group in patterns for p in group)
    found, tail = set(), b""
    while True:
        block = handle.read(CHUNK)
        if not block:
            return found
        window = tail + block
        for index, group in enumerate(patterns):
            if index not in found and any(p in window for p in group):
                found.add(index)
        tail = window[-(longest - 1):] if longest > 1 else b""


def shown(path, patterns):
    """The path as it may be printed, or None when the name itself contains a value."""
    raw = os.fsencode(path)
    if any(p in raw for group in patterns for p in group):
        return None
    return "".join(c if c.isprintable() else "\\x%02x" % ord(c) if ord(c) < 256 else "\\u%04x" % ord(c) for c in path)


def read_secret(prompt):
    """One line from the terminal with echo off. Stops the run if echo cannot be switched off."""
    import termios
    try:
        fd = os.open("/dev/tty", os.O_RDWR | os.O_NOCTTY)
    except OSError:
        raise Stop("No terminal to read from; run this at a terminal. Nothing was read.")
    try:
        try:
            before = termios.tcgetattr(fd)
            quiet = list(before)
            quiet[3] &= ~termios.ECHO
            termios.tcsetattr(fd, termios.TCSAFLUSH, quiet)
            if termios.tcgetattr(fd)[3] & termios.ECHO:
                raise termios.error
        except termios.error:
            raise Stop("This terminal cannot switch echo off, so nothing was read. Use another terminal.")
        try:
            os.write(fd, prompt.encode())
            line = b""
            while not line.endswith(b"\n"):
                byte = os.read(fd, 1)
                if not byte:
                    break
                line += byte
            os.write(fd, b"\n")
        finally:
            termios.tcsetattr(fd, termios.TCSAFLUSH, before)
    finally:
        os.close(fd)
    return line.rstrip(b"\r\n")


def read_sign_in(path):
    """((dev, ino), credential values, other values) of a named sign-in file."""
    try:
        fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
    except OSError:
        raise Stop("A sign-in file given with --codex-auth is missing, is a symbolic link or cannot be opened. Nothing was searched.")
    try:
        info = os.fstat(fd)
        if not stat.S_ISREG(info.st_mode) or info.st_size > MAX_AUTH:
            raise Stop("A file given with --codex-auth is not a sign-in file. Nothing was searched.")
        with os.fdopen(os.dup(fd), "rb") as handle:
            data = handle.read(MAX_AUTH + 1)
    except OSError:
        raise Stop("A sign-in file given with --codex-auth could not be read. Nothing was searched.")
    finally:
        os.close(fd)
    try:
        values = sign_in_values(json.loads(data.decode("utf-8")))
    except ValueError:
        values = None
    if values is None or not values[0]:
        raise Stop("A sign-in file given with --codex-auth is not in the shape this tool recognises, or holds none of the "
                   "credential fields it knows. Nothing was searched. This does not mean anything leaked.")
    return (info.st_dev, info.st_ino), values[0], values[1]


def arguments(argv):
    folders, auths, index = [], [], 0
    while index < len(argv):
        if argv[index] == "--codex-auth" and index + 1 < len(argv):
            auths.append(argv[index + 1])
            index += 2
        elif argv[index].startswith("-"):
            raise Stop("Usage: credential_search.py [--codex-auth FILE]... FOLDER [FOLDER]...  (a value is never an argument)")
        else:
            folders.append(argv[index])
            index += 1
    if not folders:
        raise Stop("Usage: credential_search.py [--codex-auth FILE]... FOLDER [FOLDER]...  (a value is never an argument)")
    return folders, auths


def run(argv):
    try:
        import resource
        resource.setrlimit(resource.RLIMIT_CORE, (0, 0))
        core = True
    except (ImportError, ValueError, OSError):
        core = False
    folders, auths = arguments(argv)
    for folder in folders:
        try:
            if not stat.S_ISDIR(os.lstat(folder).st_mode):
                raise OSError
        except OSError:
            raise Stop("A folder to search is missing, is not a folder or is a symbolic link. Nothing was searched.")

    excluded, raws, kinds = set(), [], []
    for auth in auths:
        identity, credentials, others = read_sign_in(auth)
        excluded.add(identity)
        for kind, values in (("credential field of a sign-in file", credentials), ("other long value of a sign-in file; may not be a credential", others)):
            for value in values:
                try:
                    raw = value.encode("utf-8")
                except UnicodeError:
                    raise Stop("A value in a sign-in file is not valid text. Nothing was searched.")
                if kind.startswith("credential") and len(raw) < MIN_VALUE:
                    raise Stop("A credential field in a sign-in file is too short to search for. Nothing was searched.")
                if raw not in raws:
                    raws.append(raw)
                    kinds.append(kind)
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
    patterns = [forms(raw) for raw in raws]

    hits = [[] for _ in raws]
    withheld = [0 for _ in raws]
    unreadable, unreadable_withheld = [], 0
    read = links = special = skipped_sign_in = 0

    def could_not_read(path):
        nonlocal unreadable_withheld
        name = shown(str(path), patterns)
        if name is None:
            unreadable_withheld += 1
        else:
            unreadable.append(name)

    for folder in folders:
        for root, dirs, files in os.walk(folder, onerror=lambda error: could_not_read(error.filename)):
            for name in dirs + files:
                path = os.path.join(root, name)
                try:
                    mode = os.lstat(path).st_mode
                except OSError:
                    could_not_read(path)
                    continue
                if stat.S_ISLNK(mode):
                    links += 1
                elif stat.S_ISDIR(mode):
                    pass
                elif not stat.S_ISREG(mode):
                    special += 1
                else:
                    try:
                        fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
                    except OSError:
                        could_not_read(path)
                        continue
                    try:
                        with os.fdopen(fd, "rb") as handle:
                            info = os.fstat(handle.fileno())
                            if not stat.S_ISREG(info.st_mode):
                                could_not_read(path)
                                continue
                            if (info.st_dev, info.st_ino) in excluded:
                                skipped_sign_in += 1
                                continue
                            found = stream_contains(handle, patterns)
                    except OSError:
                        could_not_read(path)
                        continue
                    read += 1
                    for index in found:
                        name_shown = shown(path, patterns)
                        if name_shown is None:
                            withheld[index] += 1
                        else:
                            hits[index].append(name_shown)

    print("Regular files read: %d. Values looked for: %d." % (read, len(raws)))
    any_hit = False
    for index, kind in enumerate(kinds):
        count = len(hits[index]) + withheld[index]
        if count:
            any_hit = True
            print("Value %d (%s): FOUND in %d file(s):" % (index + 1, kind, count))
            for name in hits[index]:
                print("  " + name)
            if withheld[index]:
                print("  and %d file(s) whose name itself contains a value; those names are not printed." % withheld[index])
        else:
            print("Value %d (%s): not found in the files read." % (index + 1, kind))
    print("Symbolic links not followed: %d. Special files (not regular files) not read: %d." % (links, special))
    if auths:
        print("Sign-in file(s) given, not searched as Codex's custody: %d given, %d met under the folders." % (len(auths), skipped_sign_in))
    if not core:
        print("Note: core dumps could not be switched off for this run.")
    incomplete = bool(unreadable or unreadable_withheld or read == 0)
    if incomplete:
        print("INCOMPLETE: %d file(s) or folder(s) could not be read or classified%s" % (
            len(unreadable) + unreadable_withheld, ":" if unreadable else "."))
        for name in unreadable:
            print("  " + name)
        if unreadable_withheld:
            print("  and %d whose name itself contains a value; not printed." % unreadable_withheld)
        if read == 0:
            print("INCOMPLETE: no file was read.")
    if any_hit:
        print("Result: a value was FOUND." + (" The search was also incomplete." if incomplete else ""))
        return 1
    if incomplete:
        print("Result: incomplete. The search did not finish; this does not say that anything leaked.")
        return 2
    print("Result: no value was found in the %d regular files read, as plain bytes or as base64 (standard or URL-safe)." % read)
    print("Not covered: a value stored escaped, percent-encoded, in hex, split across lines, in another text encoding, "
          "compressed, encrypted or inside a larger base64 block; and whatever the symbolic links point to.")
    return 0


def main(argv=None):
    try:
        return run(sys.argv[1:] if argv is None else argv)
    except Stop as stop:
        print(stop.args[0])
        print("Result: incomplete. This does not say that anything leaked.")
        return 2
    except KeyboardInterrupt:
        print("\nStopped at your request. Result: incomplete.")
        return 2
    except BaseException:  # never print an error's own text: it could quote a value
        print("Stopped by an unexpected error. Result: incomplete. Nothing of a value was printed.")
        return 2


if __name__ == "__main__":
    sys.exit(main())
