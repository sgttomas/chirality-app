#!/usr/bin/env python3
"""Check that no new spelling in the records modules reads "could not tell" as "not there".

``Path::exists()``, ``is_dir()`` and ``is_file()`` answer false both when a
path is not there and when it could not be examined, and they follow a link.
The records store asks instead through ``records_inspect`` (``presence``,
``listing``), which keeps "not there" apart from "not known" and leaves a link
as itself. This check finds, in the non-test code of the records modules
(``app/src-tauri/src/records*.rs``, files named ``*_tests.rs`` and items
under ``#[cfg(test)]`` left out), every line spelling ``.exists()``,
``.is_dir()``, ``.is_file()`` or ``.is_symlink()``. Each such line must be on
the reviewed list ``tools/ci/records_presence_list.yaml``, keyed by its file
and the line's own text (not its number, so that moving code does not fail
it), with its kind and its reason:

- ``metadata``: called on metadata already examined, whose error was handled
  where the examination was made; the reason names that examination.
- ``path``: called on a path. The entry also says, in ``cannot_tell``, what
  the caller concludes when it cannot tell, and why that admits nothing.
- ``outside``: a known site in a file outside the records modules, recorded
  with what was traced. It is not scanned; the check only keeps it from going
  stale (its line must still be in its file).

The check fails, naming the file, line and text, on a spelling not on the
list, and on a listed line no longer found (so the list follows the code).
The same text twice in one file needs two entries.

Limits. It reads spelling, not meaning: a call on metadata is the same
spelling as a call on a path, and is told apart only by its entry. It does not
see ``try_exists()`` (which keeps the error but follows a link), a call
reached through an alias, a wrapper or a macro, a spelling split across
lines, or any module outside ``records*.rs`` that reads the store (only the
``outside`` entries name such sites, and only those found). It does not
recognise test-only code by any attribute but ``#[cfg(test)]`` itself. Its
passing says only that no new such spelling appeared in its scope.
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
CFG_TEST = re.compile(r"#\[\s*cfg\s*\(\s*test\s*\)\s*\]")
KINDS = {"metadata", "path", "outside"}


def masked(text: str) -> str:
    """The text with comments, string and character literals blanked.

    Newlines are kept, so line numbers and columns agree with the original.
    Raw strings (``r"..."``, ``r#"..."#``), byte strings and escapes are
    handled; a lifetime (``'a``) is left as code.
    """
    out = list(text)
    i, n = 0, len(text)

    def blank(start: int, end: int) -> None:
        for k in range(start, min(end, n)):
            if out[k] != "\n":
                out[k] = " "

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
            blank(i, k)
            i = k
        elif re.match(r'b?r#*"', text[i:i + 8]) and (i == 0 or not (text[i - 1].isalnum() or text[i - 1] == "_")):
            m = re.match(r'b?r(#*)"', text[i:])
            close = '"' + m.group(1)
            end = text.find(close, i + len(m.group(0)))
            end = n if end < 0 else end + len(close)
            blank(i, end)
            i = end
        elif c == '"' or (c == "b" and text.startswith('b"', i) and (i == 0 or not (text[i - 1].isalnum() or text[i - 1] == "_"))):
            k = i + (2 if c == "b" else 1)
            while k < n and text[k] != '"':
                k += 2 if text[k] == "\\" else 1
            blank(i, k + 1)
            i = k + 1
        elif c == "'":
            m = re.match(r"'(?:\\(?:x[0-9a-fA-F]{2}|u\{[0-9a-fA-F]{1,6}\}|.)|[^\\'\n])'", text[i:])
            if m:
                blank(i, i + len(m.group(0)))
                i += len(m.group(0))
            else:
                i += 1  # a lifetime or label
        else:
            i += 1
    return "".join(out)


def test_only_lines(code: str) -> set[int]:
    """Line numbers (1-based) inside items or statements under ``#[cfg(test)]``.

    ``code`` is masked text. An attributed item ends at its first ``;`` when
    that comes before any ``{``, and otherwise at the brace that closes its
    first ``{``.
    """
    lines: set[int] = set()
    for m in CFG_TEST.finditer(code):
        k = m.end()
        # Further attributes on the same item.
        while True:
            while k < len(code) and code[k].isspace():
                k += 1
            if code.startswith("#[", k):
                depth = 0
                while k < len(code):
                    depth += code[k] == "["
                    depth -= code[k] == "]"
                    k += 1
                    if depth == 0:
                        break
                continue
            break
        semi, brace = code.find(";", k), code.find("{", k)
        if brace < 0 or (0 <= semi < brace):
            end = len(code) if semi < 0 else semi + 1
        else:
            depth, end = 0, brace
            while end < len(code):
                depth += code[end] == "{"
                depth -= code[end] == "}"
                end += 1
                if depth == 0:
                    break
        first = code.count("\n", 0, m.start()) + 1
        last = code.count("\n", 0, end) + 1
        lines.update(range(first, last + 1))
    return lines


def occurrences(root: Path) -> list[tuple[str, int, str]]:
    """Each production line in scope that spells one of the calls: (file, number, text)."""
    found = []
    for path in sorted((root / SOURCE).glob("records*.rs")):
        if path.name.endswith("_tests.rs"):
            continue
        text = path.read_text(encoding="utf-8")
        code = masked(text)
        skipped = test_only_lines(code)
        for number, (line, masked_line) in enumerate(zip(text.split("\n"), code.split("\n")), start=1):
            if number not in skipped and SPELLING.search(masked_line):
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
    found = occurrences(root)
    if not found and not entries:
        problems.append(f"no records module found under {SOURCE}")
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
