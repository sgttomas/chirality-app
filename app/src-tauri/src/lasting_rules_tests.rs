use super::*;
use std::os::unix::fs::PermissionsExt;
use std::path::PathBuf;

fn home(name: &str) -> PathBuf {
    let base = std::env::temp_dir().join(format!("lasting-rules-{}-{}", std::process::id(), name));
    let _ = std::fs::remove_dir_all(&base);
    std::fs::create_dir_all(&base).unwrap();
    base
}

#[test]
fn a_missing_folder_and_a_folder_without_rules_files_are_none() {
    let h = home("none");
    let missing = read(&h);
    assert_eq!(missing["state"], "none");
    assert!(missing["readAt"].is_string());
    std::fs::create_dir(h.join("rules")).unwrap();
    std::fs::write(h.join("rules").join("notes.txt"), "prefix_rule(pattern=[\"ls\"], decision=\"allow\")\n").unwrap();
    std::fs::create_dir(h.join("rules").join("nested.rules")).unwrap();
    let empty = read(&h);
    assert_eq!(empty["state"], "none");
    assert_eq!(empty["skippedEntries"], 2, "a file of another name and a folder are counted, not read");
    assert_eq!(empty["files"], json!([]));
    std::fs::remove_dir_all(&h).unwrap();
}

#[test]
fn prefix_and_network_rules_are_read_and_every_other_line_is_only_counted() {
    let h = home("read");
    std::fs::create_dir(h.join("rules")).unwrap();
    let text = concat!(
        "# written by Codex\n",
        "\n",
        "prefix_rule(pattern=[\"git\", \"status\"], decision=\"allow\")\n",
        "prefix_rule(pattern=[\"rm\", \"-rf\", \"/tmp/x y\"], decision=\"allow\")\n",
        "network_rule(host=\"example.com\", protocol=\"https\", decision=\"allow\")\n",
        "network_rule(host=\"api.example.com\", protocol=\"https\", decision=\"deny\", justification=\"the person said \\\"no\\\"\")\n",
        // Not exactly the form: other spacing, another decision, an evaluated expression, a trailing comment.
        "prefix_rule(pattern=[\"git\",\"push\"], decision=\"allow\")\n",
        "prefix_rule(pattern=[\"curl\"], decision=\"forbidden\")\n",
        "prefix_rule(pattern=[\"a\"] + [\"b\"], decision=\"allow\")\n",
        "prefix_rule(pattern=[\"ls\"], decision=\"allow\") # trailing\n",
        "  prefix_rule(pattern=[\"ls\"], decision=\"allow\")\n",
        "network_rule(host=\"x\", protocol=\"https\")\n",
        "load(\"other.rules\", \"x\")\n",
    );
    std::fs::write(h.join("rules").join("default.rules"), text).unwrap();
    let reading = read(&h);
    assert_eq!(reading["state"], "read");
    assert_eq!(reading["skippedEntries"], 0);
    let file = &reading["files"][0];
    assert_eq!(file["path"], h.join("rules").join("default.rules").to_string_lossy().as_ref());
    assert_eq!(file["prefixRules"], json!([
        {"words":["git","status"],"line":"prefix_rule(pattern=[\"git\", \"status\"], decision=\"allow\")"},
        {"words":["rm","-rf","/tmp/x y"],"line":"prefix_rule(pattern=[\"rm\", \"-rf\", \"/tmp/x y\"], decision=\"allow\")"},
    ]));
    assert_eq!(file["networkRules"][0], json!({"host":"example.com","protocol":"https","decision":"allow",
        "line":"network_rule(host=\"example.com\", protocol=\"https\", decision=\"allow\")"}));
    assert_eq!(file["networkRules"][1]["justification"], "the person said \"no\"");
    assert_eq!(file["networkRules"][1]["decision"], "deny");
    assert_eq!(file["unreadLines"], 7, "every line not exactly of a known form is counted, with nothing kept");
    let shown = serde_json::to_string(&reading).unwrap();
    assert!(!shown.contains("load(") && !shown.contains("forbidden") && !shown.contains("trailing"), "no content of an unread line is kept");
    std::fs::remove_dir_all(&h).unwrap();
}

#[test]
fn a_link_in_the_rules_folder_is_skipped_and_not_followed() {
    let h = home("link");
    std::fs::create_dir(h.join("rules")).unwrap();
    let outside = h.join("outside.rules");
    std::fs::write(&outside, "prefix_rule(pattern=[\"ls\"], decision=\"allow\")\n").unwrap();
    std::os::unix::fs::symlink(&outside, h.join("rules").join("linked.rules")).unwrap();
    let reading = read(&h);
    assert_eq!(reading["state"], "none", "a link is never read as a rules file");
    assert_eq!(reading["skippedEntries"], 1);
    // The rules folder itself as a link: not followed, and not shown as none.
    let other = h.join("elsewhere");
    std::fs::create_dir(&other).unwrap();
    std::fs::remove_dir_all(h.join("rules")).unwrap();
    std::os::unix::fs::symlink(&other, h.join("rules")).unwrap();
    let linked = read(&h);
    assert_eq!(linked["state"], "not-known");
    assert!(linked["reason"].as_str().unwrap().contains("link"));
    std::fs::remove_dir_all(&h).unwrap();
}

#[test]
fn a_folder_or_file_that_cannot_be_read_is_not_known_never_none() {
    let h = home("unreadable");
    let rules = h.join("rules");
    std::fs::create_dir(&rules).unwrap();
    std::fs::write(rules.join("a.rules"), "prefix_rule(pattern=[\"ls\"], decision=\"allow\")\n").unwrap();
    std::fs::write(rules.join("b.rules"), "prefix_rule(pattern=[\"pwd\"], decision=\"allow\")\n").unwrap();
    std::fs::set_permissions(rules.join("b.rules"), std::fs::Permissions::from_mode(0o000)).unwrap();
    let file = read(&h);
    // Running as root would read it regardless; the file case is asserted only where the mode holds.
    if std::fs::File::open(rules.join("b.rules")).is_err() {
        assert_eq!(file["state"], "not-known");
        assert_eq!(file["unreadFiles"][0]["path"], rules.join("b.rules").to_string_lossy().as_ref());
        assert_eq!(file["files"][0]["prefixRules"][0]["words"], json!(["ls"]), "the files that were read are still shown");
    }
    std::fs::set_permissions(rules.join("b.rules"), std::fs::Permissions::from_mode(0o600)).unwrap();
    std::fs::set_permissions(&rules, std::fs::Permissions::from_mode(0o000)).unwrap();
    let folder = read(&h);
    if std::fs::read_dir(&rules).is_err() {
        assert_eq!(folder["state"], "not-known");
        assert!(folder["reason"].as_str().unwrap().contains("could not be read"));
    }
    std::fs::set_permissions(&rules, std::fs::Permissions::from_mode(0o700)).unwrap();
    // A rules entry that is a file, not a folder.
    std::fs::remove_dir_all(&rules).unwrap();
    std::fs::write(&rules, "x").unwrap();
    assert_eq!(read(&h)["state"], "not-known");
    std::fs::remove_dir_all(&h).unwrap();
}

#[test]
fn a_line_that_is_not_utf8_is_counted_and_crlf_lines_are_read() {
    let mut bytes = b"prefix_rule(pattern=[\"ls\"], decision=\"allow\")\r\n".to_vec();
    bytes.extend_from_slice(b"\xff\xfe\n");
    let file = parse(Path::new("/invented/default.rules"), &bytes);
    assert_eq!(file["prefixRules"][0]["words"], json!(["ls"]));
    assert_eq!(file["unreadLines"], 1);
}
