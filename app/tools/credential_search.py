#!/usr/bin/env python3
"""Search files the App wrote for a credential, without showing the credential.

For the person who holds the credential to run themselves (DEL-01-05 AC-001,
AC-003). Read the whole file before running it; it is short on purpose.

What it does
  - Takes the folders to search as arguments: the App's data folder, the
    records store and the project folder.
  - Asks for each value at the keyboard with no echo (a key you typed into the
    App's secure field). Enter an empty line when there are no more.
  - Optionally, with --codex-auth FILE (may be repeated), also takes every long
    text value inside a Codex sign-in file (auth.json in an App-owned Codex
    home) as a value to look for. That file and the folder it is in are Codex's
    own custody and are not searched.
  - Looks for each value in every file under the folders, as plain bytes and as
    base64 of those bytes.

What it never does
  - It never prints, logs, writes or sends a value, or any part or length of
    one. Values exist only in this process's memory. It writes no file and
    opens no network connection.
  - It never reports a file it could not read as clean: unreadable files and
    folders are counted and listed, and the result is then "incomplete".

What it prints: for each value, by number, how many files contain it and their
names; then what could not be read. Exit status 0 only when every file was
read and no value was found; 1 when a value was found; 2 when the search was
incomplete or could not start.

Python 3 standard library only.
"""
import argparse
import base64
import getpass
import json
import os
import sys

CHUNK = 1 << 20
MIN_AUTH_VALUE = 20  # shorter text in a sign-in file is a label, not a credential


def long_strings(node):
    """Every text value of at least MIN_AUTH_VALUE characters in parsed JSON."""
    if isinstance(node, str):
        if len(node) >= MIN_AUTH_VALUE:
            yield node
    elif isinstance(node, dict):
        for value in node.values():
            yield from long_strings(value)
    elif isinstance(node, list):
        for value in node:
            yield from long_strings(value)


def forms(value):
    """The byte patterns that stand for one value."""
    raw = value.encode("utf-8")
    patterns = {raw, base64.b64encode(raw), base64.urlsafe_b64encode(raw)}
    patterns |= {p.rstrip(b"=") for p in list(patterns)}
    return [p for p in patterns if p]


def file_contains(path, patterns):
    """Which pattern groups occur in the file. Raises OSError if it cannot be read."""
    longest = max(len(p) for group in patterns for p in group)
    found = set()
    tail = b""
    with open(path, "rb") as handle:
        while True:
            block = handle.read(CHUNK)
            if not block:
                break
            window = tail + block
            for index, group in enumerate(patterns):
                if index not in found and any(p in window for p in group):
                    found.add(index)
            tail = window[-(longest - 1):] if longest > 1 else b""
    return found


def main():
    parser = argparse.ArgumentParser(description="Search App-written files for a credential without showing it.")
    parser.add_argument("folders", nargs="+", help="folders to search")
    parser.add_argument("--codex-auth", action="append", default=[], metavar="FILE",
                        help="a Codex sign-in file whose long text values are also looked for; its folder is not searched")
    args = parser.parse_args()

    values = []
    excluded = []
    for auth in args.codex_auth:
        try:
            with open(auth, "r", encoding="utf-8") as handle:
                found = sorted(set(long_strings(json.load(handle))))
        except (OSError, ValueError):
            print("Could not read the sign-in file given with --codex-auth; nothing was searched.")
            return 2
        if not found:
            print("The sign-in file given with --codex-auth holds no long text value; nothing was searched.")
            return 2
        values.extend(found)
        excluded.append(os.path.realpath(os.path.dirname(os.path.abspath(auth))))

    if not sys.stdin.isatty():
        print("Run this at a terminal: values are read from the keyboard only.")
        return 2
    while True:
        typed = getpass.getpass("Value to look for (not shown; empty line to finish): ")
        if not typed:
            break
        values.append(typed)
    values = list(dict.fromkeys(values))
    if not values:
        print("No value was given; nothing was searched.")
        return 2
    patterns = [forms(value) for value in values]

    hits = {index: [] for index in range(len(values))}
    unreadable = []
    skipped_links = 0
    searched = 0
    for folder in args.folders:
        if not os.path.isdir(folder):
            unreadable.append(folder)
            continue
        for root, dirs, files in os.walk(folder, onerror=lambda error: unreadable.append(error.filename)):
            real = os.path.realpath(root)
            if any(real == e or real.startswith(e + os.sep) for e in excluded):
                dirs[:] = []
                continue
            for name in dirs[:]:
                if os.path.islink(os.path.join(root, name)):
                    skipped_links += 1
            for name in files:
                path = os.path.join(root, name)
                if os.path.islink(path):
                    skipped_links += 1
                    continue
                if not os.path.isfile(path):
                    continue
                try:
                    for index in file_contains(path, patterns):
                        hits[index].append(path)
                    searched += 1
                except OSError:
                    unreadable.append(path)

    print("Files read: %d. Values looked for: %d." % (searched, len(values)))
    any_hit = False
    for index in range(len(values)):
        if hits[index]:
            any_hit = True
            print("Value %d: FOUND in %d file(s):" % (index + 1, len(hits[index])))
            for path in hits[index]:
                print("  " + path)
        else:
            print("Value %d: not found in the files read." % (index + 1))
    if skipped_links:
        print("Symbolic links not followed: %d (what they point to was not searched through them)." % skipped_links)
    if excluded:
        print("Not searched, as Codex's own custody: %d folder(s) holding the sign-in file(s) given." % len(excluded))
    if unreadable:
        print("INCOMPLETE: %d file(s) or folder(s) could not be read:" % len(unreadable))
        for path in unreadable:
            print("  " + str(path))
    if any_hit:
        return 1
    if unreadable or searched == 0:
        if searched == 0 and not unreadable:
            print("INCOMPLETE: no file was read.")
        return 2
    print("Result: every file was read and no value was found.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
