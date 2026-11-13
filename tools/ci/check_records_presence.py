#!/usr/bin/env python3
"""Check that no new spelling in the records modules reads "could not tell" as "not there".

``Path::exists()``, ``is_dir()`` and ``is_file()`` answer false both when a
path is not there and when it could not be examined, and they follow a link.
The records store asks instead through ``records_inspect`` (``presence``,
``listing``), which keeps "not there" apart from "not known" and does not
follow a link at the final entry. This check reads the raw text of every line
of the records modules' files (``app/src-tauri/src/records*.rs``, leaving out
only files named ``*_tests.rs``) and finds every line spelling ``.exists()``,
``.is_dir()``, ``.is_file()`` or ``.is_symlink()``, with or without white
space around the dot and the parentheses. It does not interpret the language:
a spelling in code, in a comment or in a string is found alike. Each such line
must be on the reviewed list ``tools/ci/records_presence_list.yaml``, keyed
by its file and the line's own text (not its number, so that moving code does
not fail it), with its kind and its reason:

- ``metadata``: called on metadata already examined, whose error was handled
  where the examination was made; the reason names that examination.
- ``path``: called on a path. The entry also says, in ``cannot_tell``, what
  the caller concludes when it cannot tell, and why that admits nothing.
- ``test``: in test code inside a records module (under ``#[cfg(test)]``);
  the reason names the module or attribute it is under.
- ``comment`` and ``string``: inside a comment or a string, not a call; the
  reason says which.
- ``outside``: a known site in a file outside the records modules, recorded
  with what was traced. It is not scanned; the check only keeps it from going
  stale (its line must still be in its file).

The check fails, naming the file, line and text, on a spelling not on the
list, and on a listed line no longer found (so the list follows the code).
The same text twice in one file needs two entries. A kind only describes: every
listed line, whatever its kind, takes part in the same accounting of exact text
and number of copies, and no kind exempts a line or loosens the count (an
``outside`` entry names a file that is not scanned and covers no scanned line).

Limits. It reads spelling, not meaning: a call on metadata is the same
spelling as a call on a path, and is told apart only by its entry. It notices
a new spelling, or one more copy of a listed one. It does not notice a change
of meaning around a listed line whose text stays the same, such as a caller
concluding something new from the same call: that is why each ``path`` entry
carries ``cannot_tell``, and it is what a reviewer of a change near a listed
line still has to read. The kinds
``test``, ``comment`` and ``string`` are the reviewer's statement; the check
does not verify them. It does not see ``try_exists()`` (which keeps the error
but follows a link), a call reached through an alias, a wrapper or a macro, a
spelling split across lines, or any module outside ``records*.rs`` that reads
the store (only the ``outside`` entries name such sites, and only those
found). Files named ``*_tests.rs`` are left out by name. Its passing says only
that no new such spelling appeared in its scope.
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
SPELLING = re.compile(r"\.\s*(?:exists|is_dir|is_file|is_symlink)\s*\(\s*\)")
KINDS = {"metadata", "path", "test", "comment", "string", "outside"}


def scanned(root: Path) -> list[Path]:
    return [p for p in sorted((root / SOURCE).glob("records*.rs")) if not p.name.endswith("_tests.rs")]


def occurrences(root: Path) -> list[tuple[str, int, str]]:
    """Each line in scope that spells one of the calls: (file, number, text).

    Lines end at a line feed, a carriage return or both, as Python's
    ``splitlines`` reads them; nothing in a line is interpreted.
    """
    found = []
    for path in scanned(root):
        for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
            if SPELLING.search(line):
                found.append((path.name, number, line.strip()))
    return found


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
    found = occurrences(root)
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
    parser.add_argument("--scan", action="store_true", help="print every occurrence found, with its line number, and exit")
    args = parser.parse_args(argv)
    if args.scan:
        for name, number, text in occurrences(args.root):
            print(f"{name}:{number}: {text}")
        return 0
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
