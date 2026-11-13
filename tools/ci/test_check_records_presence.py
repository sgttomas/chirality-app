"""Regressions for check_records_presence.py, and the check on this repository."""
from __future__ import annotations

import re
import shutil
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


def test_comments_strings_and_test_code_are_read_like_code(root):
    # The scanner does not interpret the language: a spelling in a comment, a
    # string or test code is found like a call, and is listed with its kind.
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
    found = presence.occurrences(root)
    assert [(name, number) for name, number, _ in found if name != "records_a.rs"] == [("records_b.rs", n) for n in (2, 3, 4, 5, 10, 12)]


def test_the_comment_and_string_kinds_are_accepted(root):
    write(root, "records_a.rs", "fn a() {\n    // path.exists() is not asked here\n    let s = \"path.is_dir()\";\n}\n")
    assert presence.check(root, listed(
        entry("records_a.rs", "// path.exists() is not asked here", "comment", reason="a line comment"),
        entry("records_a.rs", 'let s = "path.is_dir()";', "string", reason="a string literal"),
    )) == []


def test_white_space_around_the_dot_and_parentheses_is_seen(tmp_path):
    write(tmp_path, "records_probe.rs", "fn a() {\n    path.exists ();\n    path . is_dir( );\n    path\t.is_file\t()\n}\n")
    assert [number for _, number, _ in presence.occurrences(tmp_path)] == [2, 3, 4]


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


@pytest.mark.parametrize("kind", ["metadata", "path", "test", "comment", "string"])
def test_a_kind_describes_and_never_exempts_or_loosens_the_count(root, kind):
    # The same text under any kind gives the same result: one entry covers one
    # line, a second copy of the line fails, and a stale entry fails.
    line = "if meta.is_dir() { go(); }"
    one = listed(entry("records_a.rs", line, kind))
    assert presence.check(root, one) == []
    write(root, "records_a.rs", f"fn a() {{\n    {line}\n    {line}\n}}\n")
    problems = presence.check(root, one)
    assert len(problems) == 1 and problems[0].startswith(f"{presence.SOURCE / 'records_a.rs'}:3: {line}"), problems
    stale = listed(entry("records_a.rs", line, kind), entry("records_a.rs", line, kind), entry("records_a.rs", line, kind))
    assert [p for p in presence.check(root, stale) if "listed 3 time(s) but found 2" in p], presence.check(root, stale)


def test_an_outside_entry_never_covers_a_scanned_line(root):
    problems = presence.check(root, listed(entry("records_a.rs", "if meta.is_dir() { go(); }", "outside")))
    assert any(p.startswith(f"{presence.SOURCE / 'records_a.rs'}:2:") for p in problems), problems


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
# read like the rest, and nothing is masked, so no spelling is hidden: each line
# that spells one, in code or in a string, is seen.
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
     "fn production(path: &Path) -> bool {\n    let _text = r#######\"a raw quote: \" .exists()\"#######;\n    path.is_file()\n}\n", [2, 3]),
    ("a byte raw string with six hashes",
     "fn production(path: &Path) -> bool {\n    let _text = br######\"a raw quote: \" .exists()\"######;\n    path.is_file()\n}\n", [2, 3]),
    ("a raw C string",
     "fn production(path: &Path) -> bool {\n    let _text = cr#\"a raw quote: \" .exists()\"#;\n    path.is_file()\n}\n", [2, 3]),
    ("a C string",
     "fn production(path: &Path) -> bool {\n    let _text = c\"a quote: \\\" .exists()\";\n    path.is_file()\n}\n", [2, 3]),
])
def test_no_production_spelling_is_hidden(tmp_path, name, source, expected):
    write(tmp_path, "records_probe.rs", source)
    assert [number for _, number, _ in presence.occurrences(tmp_path)] == expected, name


# The second reading's candidates (pull request 291, round 2), with the one it
# found (a raw identifier taken for a raw string's opener, which hid the call on
# the next line) and the combining-character one it named but did not run. Each
# is added beside this repository's scanned files and checked against the
# repository's unchanged list: each must fail, naming every line that spells a
# call on the path.
def function(body: str) -> str:
    return "fn probe(path: &std::path::Path) -> bool {\n" + body + "\n}\n"


DISCARD = "macro_rules! discard { ($($t:tt)*) => {}; }\n"
CANDIDATES = [(f"plain_{s}", function(f"    path.{s}()")) for s in ("exists", "is_dir", "is_file", "is_symlink")] + [
    ("lifetimes", "fn probe<'a, 'b>(path: &'a std::path::Path, _: &'b str, _: &'static str) -> bool { path.exists() }\n"),
    ("labels", function("    'a: loop { 'static_label: loop { break 'a path.exists(); } }")),
    ("ordinary_characters", function("    let _ = ('a', '\u00e9', '{', '\\'', '\\\\', b'x', b'\\'', b'\\\\', '\\u{301}');\n    path.exists()")),
    ("character_quote", function("    let _ = '\\'';\n    path.exists()")),
    ("character_backslash", function("    let _ = '\\\\';\n    path.exists()")),
    ("escaped_string_quote", function(r'    let _ = "escaped \" quote /* .is_dir() */";' + "\n    path.exists()")),
    ("even_backslashes_before_quote", function(r'    let _ = "ends in slash \\";' + "\n    path.exists()")),
    ("odd_backslashes_before_quote", function(r'    let _ = "slash and quote \\\" here";' + "\n    path.exists()")),
    ("byte_and_c_strings", function(r'    let _ = b"/* .is_file() */ \""; let _ = c"// .is_dir() \"";' + "\n    path.exists()")),
] + [(f"identifier_suffix_{i}", function(f'    discard!({i}"text");\n    path.exists()')) for i in ("for", "bar", "abc", "abr")] + [
    ("raw_identifier_plain", function("    let r#ident = 1; let r#r = 2; let r#c = 3;\n    path.exists()")),
    ("attributes_next_to_raw", '#[doc = r###"attribute quote: \" /* */"###]\n' + function('    let _ = r#"value"#;\n    path.exists()')),
    ("string_with_block_comment_opener", function('    let _ = "/*";\n    path.exists()')),
    ("block_comment_with_string_opener", function('    /* " r####" nested /* comment */ */\n    path.exists()')),
    ("doc_comments", '/// .is_dir() "\n//! .exists()\n/** .is_file() " /* nested */ */\n' + function("    path.exists()")),
    ("unicode_non_ascii", function('    let caf\u00e9 = "\u65e5\u672c\u8a9e"; /* \u03bb */\n    path.exists()')),
    ("crlf", function('    let _ = "\u00e9"; // comment\n    path.exists()').replace("\n", "\r\n")),
    ("carriage_return", function('    let _ = "text";\r    path.exists()')),
    ("raw_seven_hashes", function('    let _ = r#######"a raw quote: "nothing"#######;\n    path.exists()')),
    ("raw_byte_six_hashes", function('    let _ = br######"a raw quote: "nothing"######;\n    path.exists()')),
    ("raw_c_string", function('    let _ = cr#"a raw quote: "nothing"#;\n    path.exists()')),
    ("raw_no_hashes", function('    let _ = r"value"; let _ = br"byte"; let _ = cr"C";\n    path.exists()')),
    ("raw_255_hashes", function('    let _ = r' + "#" * 255 + '"quote: "middle"' + "#" * 255 + ";\n    path.exists()")),
    ("cfg_same_line", "#[cfg(test)] fn helper() {} fn probe(path: &std::path::Path) -> bool { path.exists() }\n"),
    ("cfg_array_parameter", "#[cfg(test)]\nfn helper(_: [u8; 1]) {} fn probe(path: &std::path::Path) -> bool { path.exists() }\n"),
    ("cfg_attributed_else", function("#[cfg(test)]\n    if false {} else { path.exists(); }\n    path.is_file()")),
    ("unclosed_string", function('    let _ = "open;\n    path.exists()')),
    ("unclosed_raw_string", function('    let _ = r##"open"#;\n    path.exists()')),
    ("unclosed_block_comment", function("    /* open\n    path.exists()")),
    ("unknown_prefix", function('    let _ = f"unknown";\n    path.exists()')),
    ("space_before_parenthesis", function("    path.exists ()")),
    ("raw_identifier_hash_boundary", DISCARD + function('    discard!(r#r#"first");\n    let present = path.exists();\n    discard!("last"#);\n    present')),
    ("unicode_combining_raw_boundary", DISCARD + function('    discard!(a\u0301r#"first");\n    let present = path.exists();\n    discard!("last"#);\n    present')),
]
CALL = re.compile(r"path\.\s*(?:exists|is_dir|is_file|is_symlink)\s*\(")


@pytest.fixture(scope="module")
def repository_copy(tmp_path_factory):
    base = tmp_path_factory.mktemp("repository")
    for path in presence.scanned(presence.ROOT):
        write(base, path.name, path.read_text(encoding="utf-8"))
    write(base, "storage.rs", (presence.ROOT / presence.SOURCE / "storage.rs").read_text(encoding="utf-8"))
    return base


def test_every_candidate_of_the_second_reading_is_here():
    # Its forty run, the split one below among them, and the combining one it did not run.
    assert len({name for name, _ in CANDIDATES}) + 1 == 41


@pytest.mark.parametrize("name, source", CANDIDATES, ids=[name for name, _ in CANDIDATES])
def test_each_candidate_fails_on_the_unchanged_list(repository_copy, tmp_path, capsys, name, source):
    root = tmp_path / "root"
    shutil.copytree(repository_copy, root)
    (root / presence.SOURCE / "records_unreviewed.rs").write_bytes(source.encode("utf-8"))
    calls = [n for n, line in enumerate(source.splitlines(), start=1) if CALL.search(line)]
    assert calls, name
    assert presence.main(["--root", str(root), "--list", str(presence.ROOT / presence.LIST)]) == 1, name
    reported = capsys.readouterr().err
    for number in calls:
        assert f"{presence.SOURCE / 'records_unreviewed.rs'}:{number}:" in reported, (name, number, reported)


def test_a_split_after_the_name_is_seen_and_a_split_before_it_is_a_stated_limit(repository_copy, tmp_path, capsys):
    # The second reading's split_across_lines candidate breaks the line after the
    # name, which the check now sees. A line boundary between the dot and the
    # name is the limit its docstring states.
    root = tmp_path / "root"
    shutil.copytree(repository_copy, root)
    probe = root / presence.SOURCE / "records_unreviewed.rs"
    probe.write_text(function("    path.exists\n    ()"), encoding="utf-8")
    assert presence.main(["--root", str(root), "--list", str(presence.ROOT / presence.LIST)]) == 1
    assert f"{presence.SOURCE / 'records_unreviewed.rs'}:2: path.exists" in capsys.readouterr().err
    for boundary in ("\n", "\u2028", "\x0c"):
        probe.write_text(function(f"    path.{boundary}exists()"), encoding="utf-8")
        assert presence.main(["--root", str(root), "--list", str(presence.ROOT / presence.LIST)]) == 0, repr(boundary)
    assert "divided by a line boundary" in presence.__doc__


# App Agent 0's third look (pull request 291): forms that spell one of the names
# without the dot-and-empty-parentheses shape, each passing the check at
# b0985f1a. The first is in the records code today.
@pytest.mark.parametrize("name, body, line", [
    ("a function reference", "    path.parent().is_some_and(Path::is_dir)", 2),
    ("a comment between the parentheses", "    path.exists(/**/)", 2),
    ("a break between the name and the parentheses", "    path.exists\n    ()", 2),
    ("a path-qualified call", "    std::path::Path::exists(path)", 2),
    ("a line separator after the name", "    path.exists\u2028()", 2),
    ("a form feed after the name", "    path.exists\x0c()", 2),
])
def test_the_third_looks_forms_are_seen(tmp_path, name, body, line):
    write(tmp_path, "records_probe.rs", function(body))
    problems = presence.check(tmp_path, listed())
    assert [p for p in problems if p.startswith(f"{presence.SOURCE / 'records_probe.rs'}:{line}:")], (name, problems)


def test_the_read_log_folder_check_in_records_access_is_found_and_listed():
    # records_access.rs, RecordsCapability::with_source: a presence check on a
    # path through a function reference, missed until the third look.
    text = "if !read_log.parent().is_some_and(Path::is_dir) {"
    source = (presence.ROOT / presence.SOURCE / "records_access.rs").read_text(encoding="utf-8")
    assert text in (line.strip() for line in source.splitlines())
    assert ("records_access.rs", text) in {(name, found) for name, _, found in presence.occurrences(presence.ROOT)}
    entries, _ = presence.parse_list((presence.ROOT / presence.LIST).read_text(encoding="utf-8"))
    assert [e["kind"] for e in entries if e["file"] == "records_access.rs" and e["line"] == text] == ["path"]
