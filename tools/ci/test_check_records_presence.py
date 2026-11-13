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


def test_comments_and_strings_are_left_out_and_test_code_is_read(root):
    write(root, "records_b.rs", "\n".join([
        "fn b() {",
        '    let s = "path.exists() in a string, with a { brace";',
        "    let r = r#\"raw path.is_file() } \"#;",
        "    // a comment: path.exists()",
        "    /* a block comment: path.is_dir() /* nested */ still */",
        "    let c = '{';",
        "}",
        "#[cfg(test)]",
        "mod tests {",
        "    fn t() { assert!(path.exists()); }",
        "}",
        "fn after<'a>(meta: &'a Metadata) -> bool { meta.is_file() }",
    ]) + "\n")
    write(root, "records_b_tests.rs", "fn t() { assert!(path.exists()); }\n")
    found, unreadable = presence.occurrences(root)
    assert unreadable == []
    assert [(name, number) for name, number, _ in found if name != "records_a.rs"] == [("records_b.rs", 10), ("records_b.rs", 12)]


def test_the_same_test_line_four_times_needs_four_entries_and_a_fifth_fails(root):
    line = "assert!(!path.exists());"
    def module(times: int) -> str:
        return "#[cfg(test)]\nmod tests {\n" + "".join(f"    fn t{i}() {{\n        {line}\n    }}\n" for i in range(times)) + "}\n"
    write(root, "records_a.rs", module(4))
    four = listed(*[entry("records_a.rs", line, "test", reason="in mod tests under #[cfg(test)]") for _ in range(4)])
    assert presence.check(root, four) == []
    write(root, "records_a.rs", module(5))
    problems = presence.check(root, four)
    assert len(problems) == 1 and "assert!(!path.exists());" in problems[0], problems


@pytest.mark.parametrize("name, source, line", [
    ("a string that does not close", 'fn a() {\n    let s = "open;\n    path.exists();\n}\n', 2),
    ("a raw string that does not close", 'fn a() {\n    let s = r##"open"#;\n    path.exists();\n}\n', 2),
    ("a block comment that does not close", "fn a() {\n    /* open\n    path.exists();\n}\n", 2),
    ("a string prefix it does not know", 'fn a() {\n    let s = f"{x}";\n    path.exists();\n}\n', 2),
])
def test_what_it_cannot_read_fails_naming_the_line(tmp_path, name, source, line):
    write(tmp_path, "records_probe.rs", source)
    problems = presence.check(tmp_path, listed())
    assert any(p.startswith(f"{presence.SOURCE / 'records_probe.rs'}:{line}:") and "cannot tell what follows" in p for p in problems), (name, problems)
    assert presence.main(["--root", str(tmp_path), "--list", str(tmp_path / "missing.yaml")]) == 1


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


# The first reading's counterexamples (pull request 291, round 1). Test code is
# read like the rest, and every raw or C string is masked to its true end, so
# no spelling is hidden: each one here is seen.
@pytest.mark.parametrize("name, source, expected", [
    ("a production call on the line of a test-only item",
     "#[cfg(test)] fn helper() {} fn production(path: &Path) -> bool { path.exists() }\n", [1]),
    ("an attributed if with an else",
     "fn production(path: &Path) -> bool {\n#[cfg(test)]\nif true {} else {\n    let _ = path.exists();\n}\npath.is_file()\n}\n", [4, 6]),
    ("an attributed else if chain",
     "fn production(path: &Path) -> bool {\n#[cfg(test)]\nif a {} else if b { path.exists(); } else { path.is_dir(); }\npath.is_file()\n}\n", [3, 4]),
    ("an array type in a test-only item's signature",
     "#[cfg(test)]\nfn helper(path: &Path, _: [u8; 1]) -> bool {\n    path.exists()\n}\nfn production(path: &Path) -> bool { path.is_file() }\n", [3, 5]),
    ("a test-only static with an array type",
     "#[cfg(test)]\nstatic HELD: [u8; 2] = [0, 1]; fn production(path: &Path) -> bool { path.exists() }\n", [2]),
    ("a raw string with seven hashes",
     "fn production(path: &Path) -> bool {\n    let _text = r#######\"a raw quote: \" .exists()\"#######;\n    path.is_file()\n}\n", [3]),
    ("a byte raw string with six hashes",
     "fn production(path: &Path) -> bool {\n    let _text = br######\"a raw quote: \" .exists()\"######;\n    path.is_file()\n}\n", [3]),
    ("a raw C string",
     "fn production(path: &Path) -> bool {\n    let _text = cr#\"a raw quote: \" .exists()\"#;\n    path.is_file()\n}\n", [3]),
    ("a C string",
     "fn production(path: &Path) -> bool {\n    let _text = c\"a quote: \\\" .exists()\";\n    path.is_file()\n}\n", [3]),
])
def test_no_production_spelling_is_hidden(tmp_path, name, source, expected):
    write(tmp_path, "records_probe.rs", source)
    found, unreadable = presence.occurrences(tmp_path)
    assert unreadable == [], (name, unreadable)
    assert [number for _, number, _ in found] == expected, name
