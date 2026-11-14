use super::*;
use std::path::PathBuf;

fn ready_with_ledger() -> (PathBuf, Arc<Host>) {
    let root = std::env::temp_dir().join(crate::util::opaque_id("level-choice-").unwrap());
    std::fs::create_dir_all(&root).unwrap();
    let host = Arc::new(Host::new());
    host.configure_recovery(root.join("recovery.ledger.jsonl")).unwrap();
    (root, host)
}
fn chosen_rows(host: &Host) -> usize {
    host.flush_recovery_observations();
    host.recorded_recovery_entries().as_array().unwrap().iter().filter(|e| e["kind"] == "level_chosen").count()
}

#[test]
fn declining_or_closing_the_statement_changes_nothing_and_writes_nothing() {
    let (root, host) = ready_with_ledger();
    let before = host.default_level().map(|l| l.id.clone());
    for result in [MessageDialogResult::Custom(DONT_SET.into()), MessageDialogResult::Cancel, MessageDialogResult::No, MessageDialogResult::Yes] {
        let mut shown = None;
        let out = set_level(&host, &[Arc::clone(&host)], &json!("default"), "full", |s| { shown = Some(s.text.clone()); Ok(result.clone()) }).unwrap();
        assert_eq!(out, json!({"state":"dismissed","changed":false}), "{result:?}");
        assert!(shown.unwrap().contains(cl::FULL_ACCESS_STATEMENT));
    }
    assert_eq!(host.default_level().map(|l| l.id.clone()), before);
    assert_eq!(chosen_rows(&host), 0, "nothing written");
    // A refusal to present is an error, not the person's choice.
    assert!(set_level(&host, &[Arc::clone(&host)], &json!("default"), "full", |_| Err("no window".into())).is_err());
    assert_eq!(chosen_rows(&host), 0);
    std::fs::remove_dir_all(root).unwrap();
}

#[test]
fn confirming_writes_the_choice_with_the_statements_digest_then_sets_the_level() {
    let (root, host) = ready_with_ledger();
    let mut text = String::new();
    let out = set_level(&host, &[Arc::clone(&host)], &json!("default"), "supervised", |s| { text = s.text.clone(); Ok(MessageDialogResult::Custom(SET_LEVEL.into())) }).unwrap();
    assert_eq!(out["state"], "chosen");
    assert_eq!(host.default_level().unwrap().id, "supervised");
    host.flush_recovery_observations();
    let rows = host.recorded_recovery_entries();
    let row = rows.as_array().unwrap().iter().find(|e| e["kind"] == "level_chosen").unwrap();
    assert_eq!(row["confirmation"]["statementDigest"], crate::util::sha256_hex(text.as_bytes()));
    assert_eq!(row["entryId"], out["ledgerEntry"]);
    std::fs::remove_dir_all(root).unwrap();
}

#[test]
fn the_statement_names_scope_dimensions_reading_and_when_it_takes_effect() {
    let edits = cl::level("edits").unwrap();
    let text = statement(&LevelScope::Conversation("thread-1".into()), edits, false).unwrap().text;
    for part in ["this conversation (thread-1)", "edits", "Where commands may write: in the project only.", "Network for the commands the agent runs: off.",
                 "When the agent asks you: when a command needs more than this level gives.", "Reading is not limited", "It takes effect now"] {
        assert!(text.contains(part), "{part}\n{text}");
    }
    assert!(!text.contains(cl::FULL_ACCESS_STATEMENT));
    let running = statement(&LevelScope::Conversation("thread-1".into()), edits, true).unwrap().text;
    assert!(running.contains("from its next turn"), "{running}");
    for scope in [LevelScope::Default, LevelScope::NewConversation] {
        for level in cl::levels() {
            let text = statement(&scope, level, false).unwrap().text;
            assert_eq!(text.contains(cl::FULL_ACCESS_STATEMENT), level.id == "full", "{}", level.id);
            assert!(text.contains("Reading is not limited"));
        }
    }
}

#[test]
fn the_scope_and_level_are_checked_before_anything_is_shown() {
    let host = Arc::new(Host::new());
    for scope in [json!("everywhere"), json!({"conversation": ""}), json!({"conversation": "t", "extra": 1}), json!(3)] {
        assert!(set_level(&host, &[], &scope, "edits", |_| panic!("not shown")).is_err(), "{scope}");
    }
    assert!(set_level(&host, &[], &json!("default"), "invented", |_| panic!("not shown")).is_err());
    assert_eq!(parse_scope(&json!({"conversation": "t"})).unwrap(), LevelScope::Conversation("t".into()));
    assert_eq!(parse_scope(&json!("new-conversation")).unwrap(), LevelScope::NewConversation);
}

/// No test-build stand-in answers the level's confirmation: the command presents only the window's own sheet.
#[test]
fn the_command_uses_only_the_native_sheet() {
    let lib = include_str!("lib.rs");
    let start = lib.find("fn set_level(").unwrap();
    let body = &lib[start..start + lib[start..].find("\n}\n").unwrap()];
    assert!(body.contains("level_choice::confirm(&window, statement)"), "{body}");
    assert!(!body.contains("scripted_driver") && !body.contains("cfg("), "{body}");
    assert!(!include_str!("level_choice.rs").contains("scripted_driver"));
}
