use super::*;
use serde_json::json;
use std::path::PathBuf;

fn ready_with_ledger() -> (PathBuf, Arc<Host>) {
    let root = std::env::temp_dir().join(crate::util::opaque_id("level-choice-").unwrap());
    std::fs::create_dir_all(&root).unwrap();
    let host = Arc::new(Host::new());
    host.configure_recovery(root.join("recovery.ledger.jsonl")).unwrap();
    (root, host)
}

/// A plain setting: the person's choice is the act. The entry carries the scope, the values, when, its id and the
/// previous choice, and no confirmation or digest.
#[test]
fn choosing_writes_the_choice_and_sets_the_level_with_no_confirmation() {
    let (root, host) = ready_with_ledger();
    let out = set_level(&host, &[Arc::clone(&host)], &json!("default"), "supervised").unwrap();
    assert_eq!(out["state"], "chosen");
    assert_eq!(out["origin"], "chosen");
    assert_eq!(host.default_level().unwrap().id, "supervised");
    host.flush_recovery_observations();
    let rows = host.recorded_recovery_entries();
    let row = rows.as_array().unwrap().iter().find(|e| e["kind"] == "level_chosen").unwrap().clone();
    let mut keys: Vec<&str> = row.as_object().unwrap().keys().map(String::as_str).collect();
    keys.sort();
    assert_eq!(keys, ["at", "entryId", "kind", "level", "previous", "scope", "session"]);
    assert_eq!(row["entryId"], out["ledgerEntry"]);
    assert_eq!(row["level"], cl::recorded_values(cl::level("supervised").unwrap()));
    std::fs::remove_dir_all(root).unwrap();
}

#[test]
fn the_scope_and_level_are_checked_before_anything_changes() {
    let host = Arc::new(Host::new());
    for scope in [json!("new-conversation"), json!("everywhere"), json!({"conversation": ""}), json!({"conversation": "t", "extra": 1}), json!(3)] {
        assert!(set_level(&host, &[], &scope, "edits").is_err(), "{scope}");
    }
    assert!(set_level(&host, &[], &json!("default"), "invented").is_err());
    assert_eq!(host.default_level().unwrap().id, "edits", "the test Host's level is unchanged");
    assert_eq!(parse_scope(&json!({"conversation": "t"})).unwrap(), LevelScope::Conversation("t".into()));
    assert!(parse_scope(&json!("new-conversation")).unwrap_err().contains("default was not changed"));
}

/// No native sheet, no statement and no stand-in: the command passes the person's choice straight to the Host.
#[test]
fn the_command_shows_no_native_statement() {
    let lib = include_str!("lib.rs");
    let start = lib.find("fn set_level(").unwrap();
    let body = &lib[start..start + lib[start..].find("\n}\n").unwrap()];
    assert!(body.contains("level_choice::set_level(&target, &hosts, &scope, &level_id)"), "{body}");
    assert!(!body.contains("window") && !body.contains("scripted_driver") && !body.contains("cfg("), "{body}");
    let source = include_str!("level_choice.rs");
    let production = &source[..source.find("#[cfg(test)]").unwrap()];
    for absent in ["native_statement", "dialog", "statementDigest", "sha256"] {
        assert!(!production.contains(absent), "{absent}");
    }
}

#[test]
fn removed_one_shot_scope_is_refused_never_reinterpreted_as_default() {
    assert!(parse_scope(&json!("new-conversation")).is_err());
}
