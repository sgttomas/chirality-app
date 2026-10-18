// Bounded historical query checks over the real pointer ledger and register.
use super::*;
use crate::native_requests::RequestRegister;

fn generation(session: &str, home: &str, counter: u64) -> Value {
    json!({"appSession":session,"home":home,"spawnCounter":counter})
}
fn terminal(ledger: &mut RecoveryLedger, generation: &Value, id: Value, outcome: &str) -> Value {
    let mut register = RequestRegister::default();
    register.receive(generation, 1, &json!({"id":id,"method":"item/fileChange/requestApproval","params":{"threadId":"thread","turnId":"turn","itemId":"item"}}), &json!({})).unwrap();
    ledger.request_summary(&register.entries()[0]).unwrap();
    if outcome != "unanswered" {
        register
            .prepare(
                generation,
                &id,
                &json!({"decision":if outcome == "declined" {"decline"} else {"accept"}}),
                "person-via-interaction",
                Some("person:synthetic fixture (identity not verified)"),
            )
            .unwrap();
        if outcome == "write-unknown" {
            register.begin_reply_write(generation, &id).unwrap();
        } else {
            register.written(generation, &id, true);
            ledger.request_summary(&register.entries()[0]).unwrap();
            if outcome == "acknowledged" {
                register.resolved(generation, &json!({"threadId":"thread","requestId":id}));
                ledger.request_summary(&register.entries()[0]).unwrap();
            }
        }
    }
    register.close_for(generation, "supplier-stop");
    ledger.request_summary(&register.entries()[0]).unwrap();
    ledger
        .current_entries()
        .iter()
        .rev()
        .find(|row| {
            row["kind"] == "register_entry_summary"
                && row["generation"] == crate::recovery::generation_ref(generation).unwrap()
                && row["requestIdentity"] == id.to_string()
        })
        .unwrap()
        .clone()
}
fn raw_page(ledger: &RecoveryLedger, cursor: Option<&Value>) -> Value {
    ledger
        .store()
        .unwrap()
        .terminal_request_page(cursor, &RecoveryLedger::validate_pointer_entry)
        .unwrap()
}

#[test]
fn terminal_history_preserves_full_generation_typed_identity_and_exact_terminal_states() {
    let f = Scratch::new();
    let mut ledger = f.open();
    ledger.start_session("old", "synthetic").unwrap();
    let mut expected = Vec::new();
    for (home, counter, id, outcome) in [
        ("home-a", 1, json!(1), "unanswered"),
        ("home-a", 1, json!("1"), "answered"),
        ("home-b", 1, json!(1), "declined"),
        ("home-a", 2, json!(1), "write-unknown"),
        ("home-a", 1, json!(2), "acknowledged"),
        ("home-a", 1, json!(u64::MAX), "unanswered"),
        ("home-a", 1, json!(u64::MAX.to_string()), "unanswered"),
    ] {
        expected.push(terminal(
            &mut ledger,
            &generation("old", home, counter),
            id,
            outcome,
        ));
    }
    // Retry duplicates and a delayed old listed fact must not duplicate or
    // reopen the terminal identity in this separate historical query.
    ledger.append(expected[0].clone()).unwrap();
    let mut delayed = expected[0].clone();
    delayed["state"] = json!("listed");
    delayed["transition"] = json!("RQ-01");
    delayed.as_object_mut().unwrap().remove("endedAs");
    delayed.as_object_mut().unwrap().remove("context");
    ledger.append(delayed).unwrap();
    drop(ledger);
    let mut reopened = f.open();
    reopened.start_session("new", "synthetic").unwrap();
    let held = reopened.current_entries().to_vec();
    let count = reopened.recorded_count().unwrap();
    let page = reopened.read_terminal_request_page(None).unwrap();
    let entries = page["entries"].as_array().unwrap();
    assert_eq!(entries.len(), expected.len());
    for original in &expected {
        assert!(entries.iter().any(|entry| entry["summary"] == *original));
    }
    let ids: std::collections::BTreeSet<_> = entries
        .iter()
        .map(|entry| json!([entry["sourceGeneration"], entry["summary"]["requestIdentity"]]).to_string())
        .collect();
    assert_eq!(
        ids.len(),
        7,
        "numeric/string IDs, homes and spawn counters stay distinct"
    );
    assert!(entries
        .iter()
        .any(|entry| entry["summary"]["transition"] == "RQ-10"
            && entry["summary"]["replyWrite"] == "unknown"));
    assert!(entries
        .iter()
        .any(|entry| entry["summary"]["endedAs"] == "declined"));
    assert!(entries
        .iter()
        .any(|entry| entry["summary"]["acknowledgment"] == "observed"));
    assert!(entries.iter().any(|entry| entry["summary"]["requestIdentity"] == u64::MAX.to_string()
        && entry["requestIdentityType"] == "integer"));
    assert!(entries.iter().any(|entry| entry["summary"]["requestIdentity"] == format!("\"{}\"",u64::MAX)
        && entry["requestIdentityType"] == "string"));
    assert_eq!(page["oldRequestsAnswerable"], false);
    assert_eq!(reopened.current_entries(), held);
    assert_eq!(reopened.recorded_count().unwrap(), count);
}

#[test]
fn terminal_history_pages_are_bounded_cut_stable_and_validate_only_returned_rows() {
    let f = Scratch::new();
    let mut ledger = f.open();
    ledger.start_session("s", "synthetic").unwrap();
    let g = generation("s", "home", 1);
    for id in 0..TERMINAL_REQUEST_ROWS + 7 {
        terminal(&mut ledger, &g, json!(id), "unanswered");
    }
    let validated = std::cell::Cell::new(0);
    let first = ledger
        .store()
        .unwrap()
        .terminal_request_page(None, &|row| {
            validated.set(validated.get() + 1);
            RecoveryLedger::validate_pointer_entry(row)
        })
        .unwrap();
    assert_eq!(
        first["entries"].as_array().unwrap().len(),
        TERMINAL_REQUEST_ROWS
    );
    assert_eq!(
        validated.get(),
        TERMINAL_REQUEST_ROWS,
        "no whole-ledger Rust projection"
    );
    assert_eq!(first["hasMore"], true);
    terminal(&mut ledger, &g, json!("after-first-cut"), "unanswered");
    let second = raw_page(&ledger, Some(&first["nextCursor"]));
    assert_eq!(second["throughSequence"], first["throughSequence"]);
    assert_eq!(second["entries"].as_array().unwrap().len(), 7);
    assert_eq!(second["nextCursor"], Value::Null);
    assert!(!second.to_string().contains("after-first-cut"));
    assert!(raw_page(&ledger, None)
        .to_string()
        .contains("after-first-cut"));
    for invalid in [
        json!({}),
        json!({"source":"foreign","throughSequence":"1","beforeSequence":"1"}),
        json!({"source":first["nextCursor"]["source"],"throughSequence":1,"beforeSequence":"1"}),
        json!({"source":first["nextCursor"]["source"],"throughSequence":"999999999","beforeSequence":"1"}),
    ] {
        assert!(ledger.read_terminal_request_page(Some(&invalid)).is_err());
    }
}

#[test]
fn terminal_history_legacy_index_format_derives_closed_keys_from_json_in_sql() {
    let f = Scratch::new();
    let mut ledger = f.open();
    ledger.start_session("s", "synthetic").unwrap();
    let g = generation("s", "home", 1);
    terminal(&mut ledger, &g, json!(1), "unanswered");
    terminal(&mut ledger, &g, json!("1"), "answered");
    let expected = raw_page(&ledger, None)["entries"].clone();
    drop(ledger);
    let db = Connection::open(database_path(&f.ledger_path())).unwrap();
    db.execute_batch("DROP TRIGGER ledger_meta_never_deleted; DELETE FROM ledger_meta WHERE key='index_format'; INSERT INTO ledger_meta VALUES('index_format','0'); DROP TRIGGER ledger_entry_never_rewritten; UPDATE ledger_entry SET kind='old-index-kind', currency='old', subject=NULL;").unwrap();
    drop(db);
    let ledger = f.open();
    assert!(!ledger.store().unwrap().index_current);
    assert_eq!(raw_page(&ledger, None)["entries"], expected);
}

#[test]
fn terminal_history_refuses_invalid_stored_rows_without_returning_partial_or_payload() {
    for invalid in ["schema", "index"] {
        let f = Scratch::new();
        let mut ledger = f.open();
        ledger.start_session("s", "synthetic").unwrap();
        let row = terminal(
            &mut ledger,
            &generation("s", "home", 1),
            json!(1),
            "unanswered",
        );
        let db = Connection::open(database_path(&f.ledger_path())).unwrap();
        db.execute_batch("DROP TRIGGER ledger_entry_never_rewritten")
            .unwrap();
        if invalid == "schema" {
            let mut bad = row;
            bad["unpermitted"] = json!("PRIVATE_PAYLOAD_CANARY");
            db.execute(
                "UPDATE ledger_entry SET entry=?1 WHERE json_extract(entry,'$.state')='closed'",
                [bad.to_string()],
            )
            .unwrap();
        } else {
            db.execute("UPDATE ledger_entry SET currency='wrong-index' WHERE json_extract(entry,'$.state')='closed'", []).unwrap();
        }
        drop(db);
        let error = ledger.read_terminal_request_page(None).unwrap_err();
        assert!(!error.contains("PRIVATE_PAYLOAD_CANARY"));
    }
}

#[test]
fn terminal_history_revalidates_original_database_before_and_after_actual_read() {
    for change in ["missing", "hard-link", "symlink", "replaced-after-read"] {
        let f = Scratch::new();
        let mut ledger = f.open();
        ledger.start_session("s", "synthetic").unwrap();
        terminal(
            &mut ledger,
            &generation("s", "home", 1),
            json!(1),
            "unanswered",
        );
        assert_eq!(
            raw_page(&ledger, None)["entries"].as_array().unwrap().len(),
            1
        );
        let database = database_path(&f.ledger_path());
        let retained = f.0.join("original.sqlite");
        match change {
            "missing" => std::fs::rename(&database, &retained).unwrap(),
            "hard-link" => std::fs::hard_link(&database, &retained).unwrap(),
            "symlink" => {
                std::fs::rename(&database, &retained).unwrap();
                std::os::unix::fs::symlink(&retained, &database).unwrap();
            }
            "replaced-after-read" => AFTER_TERMINAL_READ.with(|slot| {
                *slot.borrow_mut() = Some(Box::new(move || {
                    std::fs::rename(&database, &retained).unwrap();
                    std::fs::copy(&retained, &database).unwrap();
                }))
            }),
            _ => unreachable!(),
        }
        assert!(
            ledger.read_terminal_request_page(None).is_err(),
            "{change}: never return cached success or replacement-source rows"
        );
    }
}

#[test]
fn terminal_history_refuses_oversized_pointer_rows_without_unbounded_rust_read() {
    let f = Scratch::new();
    let mut ledger = f.open();
    ledger.start_session("s", "synthetic").unwrap();
    let mut row = terminal(
        &mut ledger,
        &generation("s", "home", 1),
        json!(1),
        "unanswered",
    );
    row["method"] = json!("x".repeat(TERMINAL_REQUEST_BYTES + 1));
    ledger.append(row).unwrap();
    assert!(ledger
        .read_terminal_request_page(None)
        .unwrap_err()
        .contains("bounded read budget"));
}

#[test]
fn terminal_history_rechecks_native_namespace_after_read() {
    let f = Scratch::new();
    let account = f.0.join("account");
    let probe = f.0.join("probe");
    std::fs::create_dir(&account).unwrap();
    std::fs::create_dir(&probe).unwrap();
    std::fs::create_dir(f.0.join("app")).unwrap();
    let config = crate::hosting::HostConfig::new(
        f.0.join("never-executed"),
        account.clone(),
        probe,
        f.0.clone(),
    );
    let binding = crate::runtime_session::freeze_root_home_descriptors(
        &f.0.join("app"),
        &config,
        None,
        [None, None, None],
    )
    .unwrap()
    .native_namespaces(false)
    .unwrap();
    let mut ledger = RecoveryLedger::open_with_namespaces(f.ledger_path(), binding).unwrap();
    ledger.start_session("s", "synthetic").unwrap();
    terminal(
        &mut ledger,
        &generation("s", "home", 1),
        json!(1),
        "unanswered",
    );
    let database = database_path(&f.ledger_path());
    AFTER_TERMINAL_READ.with(|slot| {
        *slot.borrow_mut() = Some(Box::new(move || {
            std::os::unix::fs::symlink(database, account.join("config.toml")).unwrap()
        }))
    });
    assert!(
        ledger.read_terminal_request_page(None).is_err(),
        "post-read protected source drift refuses the page"
    );
}
