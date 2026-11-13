"""Regressions for check_records_presence.py, and the check on this repository."""
from __future__ import annotations

import sys
from pathlib import Path

import pytest
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
import check_records_presence as presence  # noqa: E402


def write(root: Path, name: str, text: str) -> None:
    path = root / presence.SOURCE / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def listed(*entries: dict) -> str:
    return yaml.safe_dump(list(entries), sort_keys=False)


def entry(file: str, line: str, kind: str = "metadata", **extra) -> dict:
    out = {"file": file, "kind": kind, "line": line, "reason": "reviewed"}
    if kind == "path":
        out["cannot_tell"] = "it refuses"
    out.update(extra)
    return out


@pytest.fixture
def root(tmp_path):
    write(tmp_path, "records_a.rs", "fn a(meta: Metadata) {\n    if meta.is_dir() { go(); }\n}\n")
    return tmp_path


def test_every_spelling_listed_passes(root):
    assert presence.check(root, listed(entry("records_a.rs", "if meta.is_dir() { go(); }"))) == []


def test_a_new_spelling_fails_naming_its_file_line_and_text(root):
    # The shape pull request 290 repaired: a log that cannot be examined read as no log.
    write(root, "records.rs", "fn set(log: &Path) {\n    if !log.exists() {\n        return (vec![], vec![]);\n    }\n}\n")
    problems = presence.check(root, listed(entry("records_a.rs", "if meta.is_dir() { go(); }")))
    assert len(problems) == 1
    assert problems[0].startswith(f"{presence.SOURCE / 'records.rs'}:2: if !log.exists() {{")
    assert "records_inspect" in problems[0]


def test_a_listed_line_no_longer_found_fails(root):
    problems = presence.check(root, listed(entry("records_a.rs", "if meta.is_dir() { go(); }"), entry("records_a.rs", "if gone.exists() {", "path")))
    assert problems == [f"{presence.LIST}: records_a.rs: 'if gone.exists() {{' is listed 1 time(s) but found 0 time(s); remove the entry that no longer has a line"]


def test_the_same_text_twice_needs_two_entries(root):
    write(root, "records_a.rs", "fn a() {\n    if meta.is_dir() { go(); }\n    if meta.is_dir() { go(); }\n}\n")
    one = listed(entry("records_a.rs", "if meta.is_dir() { go(); }"))
    assert len(presence.check(root, one)) == 1
    two = listed(entry("records_a.rs", "if meta.is_dir() { go(); }"), entry("records_a.rs", "if meta.is_dir() { go(); }"))
    assert presence.check(root, two) == []


def test_moving_a_line_does_not_fail_it(root):
    write(root, "records_a.rs", "\n\n\nfn a(meta: Metadata) {\n    // moved down\n    if meta.is_dir() { go(); }\n}\n")
    assert presence.check(root, listed(entry("records_a.rs", "if meta.is_dir() { go(); }"))) == []


def test_test_code_comments_and_strings_are_left_out(root):
    write(root, "records_b.rs", "\n".join([
        "fn b() {",
        '    let s = "path.exists() in a string, with a { brace";',
        "    let r = r#\"raw path.is_file() } \"#;",
        "    // a comment: path.exists()",
        "    /* a block comment: path.is_dir() */",
        "    let c = '{';",
        "}",
        "#[cfg(test)]",
        "fn helper() { if path.exists() { let s = \"}\"; } }",
        "#[cfg(test)]",
        "#[allow(dead_code)]",
        "mod tests {",
        "    fn t() { assert!(path.exists()); }",
        "}",
        "fn after<'a>(meta: &'a Metadata) -> bool { meta.is_file() }",
    ]) + "\n")
    write(root, "records_b_tests.rs", "fn t() { assert!(path.exists()); }\n")
    found = [(name, number) for name, number, _ in presence.occurrences(root)]
    assert ("records_b.rs", 15) in found, found
    assert [f for f in found if f[0] == "records_b.rs"] == [("records_b.rs", 15)], found
    assert not any(name == "records_b_tests.rs" for name, _ in found)


def test_a_path_entry_must_say_what_its_caller_concludes(root):
    write(root, "records_a.rs", "fn a() {\n    if path.exists() { go(); }\n}\n")
    problems = presence.check(root, listed({"file": "records_a.rs", "kind": "path", "line": "if path.exists() { go(); }", "reason": "reviewed"}))
    assert any("cannot_tell" in p for p in problems), problems


def test_an_unknown_kind_or_a_missing_reason_fails(root):
    assert any("not one of" in p for p in presence.check(root, listed(entry("records_a.rs", "if meta.is_dir() { go(); }", kind="maybe"))))
    assert any("lacks reason" in p for p in presence.check(root, listed({"file": "records_a.rs", "kind": "metadata", "line": "if meta.is_dir() { go(); }"})))


def test_an_outside_site_is_kept_from_going_stale(root):
    (root / "app/src-tauri/src/storage.rs").write_text("fn check_path() {\n    if let Ok(meta) = x {\n    }\n}\n")
    here = entry("app/src-tauri/src/storage.rs", "if let Ok(meta) = x {", "outside")
    assert presence.check(root, listed(entry("records_a.rs", "if meta.is_dir() { go(); }"), here)) == []
    gone = entry("app/src-tauri/src/storage.rs", "if let Ok(meta) = y {", "outside")
    assert any("no longer found" in p for p in presence.check(root, listed(entry("records_a.rs", "if meta.is_dir() { go(); }"), gone)))


def test_this_repository_lists_every_such_spelling():
    root = presence.ROOT
    problems = presence.check(root, (root / presence.LIST).read_text(encoding="utf-8"))
    assert problems == [], "\n".join(problems)
