#!/usr/bin/env python3
"""Check that no new spelling in the records modules reads "could not tell" as "not there".

``Path::exists()``, ``is_dir()`` and ``is_file()`` answer false both when a
path is not there and when it could not be examined, and they follow a link.
The records store asks instead through ``records_inspect`` (``presence``,
``listing``), which keeps "not there" apart from "not known" and does not
follow a link at the final entry. This check reads every line of the records
modules' files (``app/src-tauri/src/records*.rs``, leaving out only files
named ``*_tests.rs``) and finds every line spelling ``.exists()``,
``.is_dir()``, ``.is_file()`` or ``.is_symlink()`` outside comments and
strings. Each such line must be on the reviewed list
``tools/ci/records_presence_list.yaml``, keyed by its file and the line's own
text (not its number, so that moving code does not fail it), with its kind and
its reason:

- ``metadata``: called on metadata already examined, whose error was handled
  where the examination was made; the reason names that examination.
- ``path``: called on a path. The entry also says, in ``cannot_tell``, what
  the caller concludes when it cannot tell, and why that admits nothing.
- ``test``: in test code inside a records module (under ``#[cfg(test)]``);
  the reason names the module or attribute it is under.
- ``outside``: a known site in a file outside the records modules, recorded
  with what was traced. It is not scanned; the check only keeps it from going
  stale (its line must still be in its file).

The check fails, naming the file, line and text, on a spelling not on the
list, and on a listed line no longer found (so the list follows the code).
The same text twice in one file needs two entries. It also fails, naming the
line, on text it cannot read with certainty: a string or comment that does
not close, or a string prefix it does not know. Its masking knows ordinary,
byte and C strings, raw strings with any number of ``#`` (``r``, ``br``,
``cr``), character and byte literals, line comments and nested block
comments; any other form fails the check until someone changes the code or
this scanner. That cost is intended: what it cannot read is never taken for
"nothing there".

Limits. It reads spelling, not meaning: a call on metadata is the same
spelling as a call on a path, and is told apart only by its entry, and a
``test`` entry's kind is the reviewer's statement: the scanner does not check
that the line is test-only. It does not see ``try_exists()`` (which keeps the
error but follows a link), a call reached through an alias, a wrapper or a
macro, a spelling split across lines, or any module outside ``records*.rs``
that reads the store (only the ``outside`` entries name such sites, and only
those found). Files named ``*_tests.rs`` are left out by name. Its passing
says only that no new such spelling appeared in its scope.
"""
from __future__ import annotations

import argparse
import re
import sys
from collections import Counter
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
SOURCE = Path("app/src-tauri/src")
LIST = Path("tools/ci/records_presence_list.yaml")
SPELLING = re.compile(r"\.(?:exists|is_dir|is_file|is_symlink)\(\)")
KINDS = {"metadata", "path", "test", "outside"}
RAW = re.compile(r'(?:br|cr|r)(#*)"')
STRING_PREFIXES = {"", "b", "c"}
CHARACTER = re.compile(r"b?'(?:\\(?:x[0-9a-fA-F]{2}|u\{[0-9a-fA-F]{1,6}\}|[nrt0\\'\"])|[^\\'\n])'")


def _identifier(c: str) -> bool:
    return c.isalnum() or c == "_"


def masked(text: str) -> tuple[str, list[tuple[int, str]]]:
    """The text with comments, strings and character literals blanked, and
    what could not be read: (line, what) for each.

    Newlines are kept, so line numbers agree with the original. A string or
    comment that does not close, or a string prefix not known here, is
    returned as a problem; masking stops there, since nothing after it can
    be read with certainty.
    """
    out = list(text)
    problems: list[tuple[int, str]] = []
    n = len(text)

    def line(at: int) -> int:
        return text.count("\n", 0, at) + 1

    def blank(start: int, end: int) -> None:
        for k in range(start, min(end, n)):
            if out[k] != "\n":
                out[k] = " "

    i = 0
    while i < n:
        c = text[i]
        if text.startswith("//", i):
            end = text.find("\n", i)
            end = n if end < 0 else end
            blank(i, end)
            i = end
        elif text.startswith("/*", i):
            depth, k = 1, i + 2
            while k < n and depth:
                if text.startswith("/*", k):
                    depth, k = depth + 1, k + 2
                elif text.startswith("*/", k):
                    depth, k = depth - 1, k + 2
                else:
                    k += 1
            if depth:
                problems.append((line(i), "a block comment that does not close"))
                blank(i, n)
                break
            blank(i, k)
            i = k
        elif (m := RAW.match(text, i)) and (i == 0 or not _identifier(text[i - 1])):
            close = '"' + m.group(1)
            end = text.find(close, m.end())
            if end < 0:
                problems.append((line(i), "a raw string that does not close"))
                blank(i, n)
                break
            blank(i, end + len(close))
            i = end + len(close)
        elif c == '"':
            start = i
            while start > 0 and _identifier(text[start - 1]):
                start -= 1
            prefix = text[start:i]
            if prefix not in STRING_PREFIXES:
                problems.append((line(i), f"a string with a prefix this check does not know ({prefix!r})"))
                blank(start, n)
                break
            k = i + 1
            while k < n and text[k] != '"':
                k += 2 if text[k] == "\\" else 1
            if k >= n:
                problems.append((line(i), "a string that does not close"))
                blank(start, n)
                break
            blank(start, k + 1)
            i = k + 1
        elif c in "'b" and (m := CHARACTER.match(text, i)) and (i == 0 or not _identifier(text[i - 1])):
            blank(i, m.end())
            i = m.end()
        else:
            i += 1
    return "".join(out), problems


def scanned(root: Path) -> list[Path]:
    return [p for p in sorted((root / SOURCE).glob("records*.rs")) if not p.name.endswith("_tests.rs")]


def occurrences(root: Path) -> tuple[list[tuple[str, int, str]], list[str]]:
    """Each line in scope that spells one of the calls, (file, number, text),
    and what could not be read."""
    found, unreadable = [], []
    for path in scanned(root):
        text = path.read_text(encoding="utf-8")
        code, problems = masked(text)
        for number, what in problems:
            unreadable.append(f"{SOURCE / path.name}:{number}: {what}; this check cannot tell what follows, so it fails until the code or the check changes")
        for number, (line, masked_line) in enumerate(zip(text.split("\n"), code.split("\n")), start=1):
            if SPELLING.search(masked_line):
                found.append((path.name, number, line.strip()))
    return found, unreadable


def parse_list(text: str) -> tuple[list[dict], list[str]]:
    problems: list[str] = []
    try:
        data = yaml.safe_load(text) or []
    except yaml.YAMLError as error:
        return [], [f"{LIST} is not readable YAML: {error}"]
    if not isinstance(data, list):
        return [], [f"{LIST} must be a list of entries"]
    entries = []
    for index, entry in enumerate(data, start=1):
        where = f"{LIST} entry {index}"
        if not isinstance(entry, dict):
            problems.append(f"{where} is not a mapping")
            continue
        missing = [key for key in ("file", "kind", "line", "reason") if not str(entry.get(key) or "").strip()]
        if missing:
            problems.append(f"{where} lacks {', '.join(missing)}")
            continue
        if entry["kind"] not in KINDS:
            problems.append(f"{where} has kind {entry['kind']!r}, not one of {sorted(KINDS)}")
            continue
        if entry["kind"] == "path" and not str(entry.get("cannot_tell") or "").strip():
            problems.append(f"{where} ({entry['file']}: {entry['line']}) is called on a path and does not say, in cannot_tell, what its caller concludes when it cannot tell")
            continue
        entries.append(entry)
    return entries, problems


def check(root: Path, list_text: str) -> list[str]:
    entries, problems = parse_list(list_text)
    if not scanned(root):
        return problems + [f"no records module found under {SOURCE}"]
    found, unreadable = occurrences(root)
    problems += unreadable
    listed = Counter((e["file"], str(e["line"]).strip()) for e in entries if e["kind"] != "outside")
    seen = Counter((name, text) for name, _, text in found)
    remaining = listed.copy()
    for name, number, text in found:
        if remaining[(name, text)] > 0:
            remaining[(name, text)] -= 1
        else:
            problems.append(f"{SOURCE / name}:{number}: {text}  -- a new spelling that reads 'could not tell' as 'not there' or follows a link; ask through records_inspect, or list it in {LIST} with its kind and reason")
    for (name, text), count in remaining.items():
        if count > 0:
            problems.append(f"{LIST}: {name}: {text!r} is listed {listed[(name, text)]} time(s) but found {seen[(name, text)]} time(s); remove the entry that no longer has a line")
    for entry in entries:
        if entry["kind"] == "outside":
            path = root / str(entry["file"])
            if not path.is_file() or str(entry["line"]).strip() not in (line.strip() for line in path.read_text(encoding="utf-8").split("\n")):
                problems.append(f"{LIST}: outside site {entry['file']}: {entry['line']!r} is no longer found there")
    return problems


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--list", type=Path, help="reviewed list to read (default: the root's list)")
    parser.add_argument("--scan", action="store_true", help="print every occurrence found, with its line number, and what could not be read, and exit")
    args = parser.parse_args(argv)
    if args.scan:
        found, unreadable = occurrences(args.root)
        for name, number, text in found:
            print(f"{name}:{number}: {text}")
        for problem in unreadable:
            print(problem, file=sys.stderr)
        return 1 if unreadable else 0
    list_path = args.list or args.root / LIST
    problems = check(args.root, list_path.read_text(encoding="utf-8") if list_path.exists() else "")
    for problem in problems:
        print(problem, file=sys.stderr)
    if problems:
        print(f"records presence spelling: {len(problems)} problem(s)", file=sys.stderr)
        return 1
    print("records presence spelling: every such spelling in the records modules is on the reviewed list with its reason")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
