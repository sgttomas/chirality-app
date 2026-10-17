use super::*;

const PROJECT: &str = "chirality-project:invented-administration-fixture";
struct History {
    root: PathBuf,
    dir: PathBuf,
    events: BTreeMap<String, Vec<u8>>,
}
impl History {
    fn new() -> Self {
        let root = std::env::temp_dir().join(util::opaque_id("package-administration-").unwrap());
        std::fs::create_dir(&root).unwrap();
        let root = std::fs::canonicalize(root).unwrap();
        let dir = root.join("projects").join(storage::key(PROJECT));
        Self {
            root,
            dir,
            events: BTreeMap::new(),
        }
    }
    fn push(&mut self, action: &str, closed: bool, hold: bool, disposition: &str) {
        let sequence = self.events.len() as u64 + 1;
        let previous = self
            .events
            .last_key_value()
            .map(|(_, bytes)| util::sha256_hex(bytes));
        let mut v = json!({"format":FORMAT,"formatVersion":"0.1","sequence":sequence,
            "previous":previous,"projectId":PROJECT,"projectKey":storage::key(PROJECT),
            "at":"2026-10-17T00:00:00Z","action":action,"purpose":"invented package fixture",
            "scope":{"projectId":PROJECT,"projectRoot":"/invented-fixture/project","storeId":"invented-fixture-store"},
            "context":{},"recorder":"App interface","actorKind":"person",
            "actor":{"identityVerified":false,"displayName":"Invented fixture person"},
            "stateAfter":{"closed":closed,"legalHold":hold,"disposition":disposition}});
        if action == "dispose" {
            let payload = json!({"files":1,"identity":"invented payload identity","identityMethod":"fixture only"});
            v["export"] = json!({"folder":"/invented-fixture/export","identity":"invented export identity","administrationIdentity":"invented administration identity","payload":payload});
            v["payload"] = payload;
        }
        if action == "disposal-completed" {
            v.as_object_mut().unwrap().remove("actor");
            v.as_object_mut().unwrap().remove("actorKind");
            v["recorder"] = json!("App");
            v["originalAct"] = json!(sequence - 1);
        }
        // Deliberate surrounding whitespace and CRLF must survive restoration.
        let bytes = format!(" \n{}\r\n", serde_json::to_string_pretty(&v).unwrap()).into_bytes();
        self.events.insert(format!("{sequence:020}.json"), bytes);
    }
    fn snapshot(&self) -> Value {
        json!({"format":"chirality.records-administration-snapshot","formatVersion":"0.1",
            "projectId":PROJECT,"projectKey":storage::key(PROJECT),"sequence":self.events.len(),
            "standing":"invented unsigned fixture evidence",
            "events":self.events.iter().map(|(n,b)|(n.clone(),String::from_utf8(b.clone()).unwrap())).collect::<BTreeMap<_,_>>()})
    }
    fn incoming(&self) -> PackageAdministration {
        validate_package_snapshot(PROJECT, &self.snapshot()).unwrap()
    }
    fn place(&self, names: &[u64]) {
        let folder = control(&self.dir).unwrap().join("events");
        std::fs::create_dir_all(&folder).unwrap();
        for sequence in names {
            let name = format!("{sequence:020}.json");
            std::fs::write(folder.join(&name), &self.events[&name]).unwrap();
        }
    }
    fn witness(&self) {
        let incoming = self.incoming();
        remember_prefix(&self.dir, incoming.sequence, incoming.head.as_deref()).unwrap();
    }
    fn marker(&self) {
        let control = control(&self.dir).unwrap();
        std::fs::create_dir_all(&control).unwrap();
        std::fs::write(control.join("history-started.json"),serde_json::to_vec(&json!({
            "format":"chirality.records-administration-started","formatVersion":"0.1",
            "projectKey":storage::key(PROJECT),"firstHead":util::sha256_hex(self.events.first_key_value().unwrap().1)
        })).unwrap()).unwrap();
    }
}
impl Drop for History {
    fn drop(&mut self) {
        let _ = std::fs::remove_dir_all(&self.root);
    }
}

#[test]
fn package_administration_validates_empty_held_closed_and_preserves_exact_bytes() {
    let mut h = History::new();
    let empty = h.incoming();
    assert_eq!(empty.sequence, 0);
    assert!(!empty.closed && !empty.legal_hold && empty.head.is_none());
    restore_package_history(&h.dir, &plan_package_restore(&h.dir, &empty).unwrap()).unwrap();
    assert!(
        !control(&h.dir).unwrap().exists(),
        "empty history creates no control evidence"
    );
    h.push("set-hold", false, true, "kept");
    h.push("close", true, true, "kept");
    let incoming = h.incoming();
    assert!(incoming.closed && incoming.legal_hold);
    assert_eq!(incoming.events, h.events);
    let plan = plan_package_restore(&h.dir, &incoming).unwrap();
    assert_eq!(plan.missing_events.len(), 2);
    assert!(plan.marker_needed);
    restore_package_history(&h.dir, &plan).unwrap();
    restore_package_history(&h.dir, &plan).unwrap();
    assert_eq!(local_history(&h.dir).unwrap().events, h.events);
    for name in h.events.keys() {
        assert_eq!(
            std::fs::metadata(control(&h.dir).unwrap().join("events").join(name))
                .unwrap()
                .mode()
                & 0o777,
            0o600
        );
    }
    assert_eq!(
        std::fs::metadata(history_marker(&h.dir).unwrap())
            .unwrap()
            .mode()
            & 0o777,
        0o600
    );
    assert_eq!(
        std::fs::metadata(control(&h.dir).unwrap().join("events"))
            .unwrap()
            .mode()
            & 0o777,
        0o700
    );
    assert_eq!(state(&h.dir).unwrap().view()["legalHold"], true);
}

#[test]
fn package_administration_retains_newer_local_hold_and_closure_for_older_export() {
    let mut h = History::new();
    h.push("close", true, false, "kept");
    let older = h.incoming();
    h.push("reopen", false, false, "kept");
    h.push("set-hold", false, true, "kept");
    h.push("close", true, true, "kept");
    h.place(&[1, 2, 3, 4]);
    h.marker();
    h.witness();
    let plan = plan_package_restore(&h.dir, &older).unwrap();
    assert!(plan.missing_events.is_empty());
    assert!(plan.summary()["resultingRetention"]["closed"]
        .as_bool()
        .unwrap());
    assert!(plan.summary()["resultingRetention"]["legalHold"]
        .as_bool()
        .unwrap());
    assert_eq!(plan.summary()["sourceHistory"]["sequence"], 1);
    assert_eq!(plan.summary()["resultingRetention"]["sequence"], 4);
    restore_package_history(&h.dir, &plan).unwrap();
    assert_eq!(local_history(&h.dir).unwrap().events, h.events);
}

#[test]
fn package_administration_restores_missing_prefix_from_surviving_marker_and_witness() {
    let mut h = History::new();
    h.push("set-hold", false, true, "kept");
    h.push("close", true, true, "kept");
    h.place(&[2]);
    h.marker();
    h.witness();
    assert!(state(&h.dir).is_err());
    let plan = plan_package_restore(&h.dir, &h.incoming()).unwrap();
    assert_eq!(
        plan.missing_events.keys().collect::<Vec<_>>(),
        vec!["00000000000000000001.json"]
    );
    restore_package_history(&h.dir, &plan).unwrap();
    assert_eq!(state(&h.dir).unwrap().view()["closed"], true);
    assert_eq!(state(&h.dir).unwrap().view()["legalHold"], true);
}

#[test]
fn package_administration_restores_whole_witnessed_history_and_missing_marker() {
    let mut h = History::new();
    h.push("set-hold", false, true, "kept");
    h.push("close", true, true, "kept");
    h.witness();
    let plan = plan_package_restore(&h.dir, &h.incoming()).unwrap();
    restore_package_history(&h.dir, &plan).unwrap();
    assert_eq!(
        marker_head(&h.dir).unwrap(),
        h.events.first_key_value().map(|(_, b)| util::sha256_hex(b))
    );
    assert_eq!(state(&h.dir).unwrap().sequence, 2);
}

fn mutate_first(snapshot: &mut Value, change: impl FnOnce(&mut Value)) {
    let text = snapshot["events"]["00000000000000000001.json"]
        .as_str()
        .unwrap();
    let mut event: Value = serde_json::from_str(text).unwrap();
    change(&mut event);
    snapshot["events"]["00000000000000000001.json"] = json!(serde_json::to_string(&event).unwrap());
}
#[test]
fn package_administration_refuses_wrong_profile_identity_count_names_schema_order_and_state() {
    let mut h = History::new();
    h.push("close", true, false, "kept");
    let original = h.snapshot();
    let mut cases = Vec::new();
    for (field, value) in [
        ("format", json!("unknown")),
        ("formatVersion", json!("0.2")),
        ("projectId", json!("other")),
        ("projectKey", json!("0".repeat(64))),
        ("sequence", json!(0)),
        ("standing", Value::Null),
    ] {
        let mut v = original.clone();
        v[field] = value;
        cases.push(v);
    }
    let mut v = original.clone();
    v.as_object_mut().unwrap().remove("events");
    cases.push(v);
    let mut v = original.clone();
    v["unknown"] = json!(true);
    cases.push(v);
    for name in ["../escape.json", "1.json", "00000000000000000002.json"] {
        let mut v = original.clone();
        let entry = v["events"]
            .as_object_mut()
            .unwrap()
            .remove("00000000000000000001.json")
            .unwrap();
        v["events"][name] = entry;
        cases.push(v);
    }
    let mut v = original.clone();
    v["events"]["00000000000000000001.json"] = json!({});
    cases.push(v);
    let mut v = original.clone();
    mutate_first(&mut v, |e| e["actor"]["identityVerified"] = json!(true));
    cases.push(v);
    let mut v = original.clone();
    mutate_first(&mut v, |e| e["previous"] = json!("0".repeat(64)));
    cases.push(v);
    let mut v = original.clone();
    mutate_first(&mut v, |e| e["sequence"] = json!(2));
    cases.push(v);
    let mut v = original.clone();
    mutate_first(&mut v, |e| e["action"] = json!("reopen"));
    cases.push(v);
    let mut v = original.clone();
    mutate_first(&mut v, |e| e["stateAfter"]["legalHold"] = json!(true));
    cases.push(v);
    let mut v = original.clone();
    mutate_first(&mut v, |e| e["scope"]["projectId"] = json!("other"));
    cases.push(v);
    for (index, v) in cases.iter().enumerate() {
        assert!(
            validate_package_snapshot(PROJECT, v).is_err(),
            "invalid snapshot case {index} admitted"
        );
    }
    assert!(validate_package_snapshot("other", &original).is_err());
}

#[test]
fn package_administration_refuses_divergence_marker_conflict_and_missing_witnessed_tail() {
    let mut h = History::new();
    h.push("close", true, false, "kept");
    h.place(&[1]);
    let path = control(&h.dir)
        .unwrap()
        .join("events/00000000000000000001.json");
    let mut different = h.events.first_key_value().unwrap().1.clone();
    different.push(b' ');
    std::fs::write(&path, different).unwrap();
    assert!(plan_package_restore(&h.dir, &h.incoming())
        .unwrap_err()
        .contains("conflicting"));
    std::fs::write(&path, h.events.first_key_value().unwrap().1).unwrap();
    h.marker();
    let marker = history_marker(&h.dir).unwrap();
    let mut value: Value = serde_json::from_slice(&std::fs::read(&marker).unwrap()).unwrap();
    value["firstHead"] = json!("0".repeat(64));
    std::fs::write(&marker, serde_json::to_vec(&value).unwrap()).unwrap();
    assert!(plan_package_restore(&h.dir, &h.incoming())
        .unwrap_err()
        .contains("marker"));
    std::fs::remove_file(marker).unwrap();
    let older = h.incoming();
    h.push("set-hold", true, true, "kept");
    h.witness();
    assert!(plan_package_restore(&h.dir, &older)
        .unwrap_err()
        .contains("previously observed"));
}

#[test]
fn package_administration_old_exports_cannot_revive_disposed_or_incomplete_identities() {
    for completed in [false, true] {
        let mut h = History::new();
        h.push("close", true, false, "kept");
        let older = h.incoming();
        h.push("dispose", true, false, "disposal incomplete");
        if completed {
            h.push("disposal-completed", true, false, "disposed");
        }
        let names = (1..=h.events.len() as u64).collect::<Vec<_>>();
        h.place(&names);
        h.marker();
        h.witness();
        assert!(plan_package_restore(&h.dir, &older)
            .unwrap_err()
            .contains("disposed"));
        assert!(plan_package_restore(&h.dir, &h.incoming())
            .unwrap_err()
            .contains("disposed"));
        // A missing disposal tail remains pinned in this process.
        for sequence in 2..=h.events.len() as u64 {
            std::fs::remove_file(
                control(&h.dir)
                    .unwrap()
                    .join("events")
                    .join(format!("{sequence:020}.json")),
            )
            .unwrap();
        }
        assert!(plan_package_restore(&h.dir, &older).is_err());
    }
}

#[test]
fn package_administration_restore_retries_visible_unsynced_bytes_without_rewriting() {
    let mut h = History::new();
    h.push("set-hold", false, true, "kept");
    let plan = plan_package_restore(&h.dir, &h.incoming()).unwrap();
    let folder = control(&h.dir).unwrap().join("events");
    // Precreate directories so injected failure occurs after event publication.
    std::fs::create_dir_all(&folder).unwrap();
    storage::fail_directory_for_test(Some(folder.clone()));
    assert!(restore_package_history(&h.dir, &plan).is_err());
    storage::fail_directory_for_test(None);
    let path = folder.join("00000000000000000001.json");
    assert_eq!(
        read_plain(&path).unwrap(),
        h.events.first_key_value().unwrap().1.as_slice()
    );
    let inode = std::fs::metadata(&path).unwrap().ino();
    restore_package_history(&h.dir, &plan).unwrap();
    restore_package_history(&h.dir, &plan).unwrap();
    assert_eq!(std::fs::metadata(&path).unwrap().ino(), inode);
    assert_eq!(state(&h.dir).unwrap().view()["legalHold"], true);
}

#[test]
fn package_administration_frozen_local_evidence_and_unknown_members_cannot_change() {
    let mut h = History::new();
    h.push("close", true, false, "kept");
    h.place(&[1]);
    h.marker();
    let plan = plan_package_restore(&h.dir, &h.incoming()).unwrap();
    let event = control(&h.dir)
        .unwrap()
        .join("events/00000000000000000001.json");
    let replacement = h.root.join("replacement");
    std::fs::write(&replacement, h.events.first_key_value().unwrap().1).unwrap();
    std::fs::rename(&replacement, &event).unwrap();
    assert!(restore_package_history(&h.dir, &plan)
        .unwrap_err()
        .contains("evidence changed"));
    let unknown = control(&h.dir).unwrap().join("events/unknown");
    std::fs::write(&unknown, b"retained").unwrap();
    assert!(plan_package_restore(&h.dir, &h.incoming()).is_err());
    std::fs::remove_file(unknown).unwrap();
    std::fs::create_dir(control(&h.dir).unwrap().join("removal")).unwrap();
    assert!(plan_package_restore(&h.dir, &h.incoming())
        .unwrap_err()
        .contains("disposal staging"));
}

#[test]
fn package_administration_source_extension_cannot_clear_local_hold_or_closure() {
    for hold in [false, true] {
        let mut h = History::new();
        if hold {
            h.push("set-hold", false, true, "kept");
        } else {
            h.push("close", true, false, "kept");
        }
        h.place(&[1]);
        h.marker();
        h.witness();
        if hold {
            h.push("release-hold", false, false, "kept");
        } else {
            h.push("reopen", false, false, "kept");
        }
        assert!(plan_package_restore(&h.dir, &h.incoming())
            .unwrap_err()
            .contains("cannot reopen"));
        // The same restriction survives loss of all event files while the
        // process still remembers its accepted prefix.
        std::fs::remove_file(
            control(&h.dir)
                .unwrap()
                .join("events/00000000000000000001.json"),
        )
        .unwrap();
        assert!(plan_package_restore(&h.dir, &h.incoming())
            .unwrap_err()
            .contains("cannot reopen"));
    }
}

#[test]
fn package_administration_retry_uses_frozen_local_baseline_for_its_partial_source_rows() {
    let mut h = History::new();
    h.push("set-hold", false, true, "kept");
    h.push("release-hold", false, false, "kept");
    h.push("close", true, false, "kept");
    h.push("reopen", false, false, "kept");
    let incoming = h.incoming();
    let plan = plan_package_restore(&h.dir, &incoming).unwrap();
    let original_context = plan.source_context.clone();
    // A crashed import published only its source's old hold, not a new local act.
    h.place(&[1]);
    h.marker();
    assert!(plan_package_restore(&h.dir, &incoming).is_err());
    let resumed = resume_package_restore(&h.dir, &incoming, &original_context).unwrap();
    restore_package_history(&h.dir, &resumed).unwrap();
    restore_package_history(&h.dir, &plan).unwrap();
    assert_eq!(state(&h.dir).unwrap().view()["legalHold"], false);
    assert_eq!(state(&h.dir).unwrap().view()["closed"], false);
    assert_eq!(local_history(&h.dir).unwrap().events, h.events);
}

#[test]
fn package_administration_refuses_partial_event_bytes_without_overwriting_them() {
    let mut h = History::new();
    h.push("close", true, false, "kept");
    let plan = plan_package_restore(&h.dir, &h.incoming()).unwrap();
    h.place(&[1]);
    let path = control(&h.dir)
        .unwrap()
        .join("events/00000000000000000001.json");
    std::fs::write(&path, b"{partial original").unwrap();
    assert!(restore_package_history(&h.dir, &plan).is_err());
    assert_eq!(std::fs::read(&path).unwrap(), b"{partial original");
}

#[test]
fn package_administration_newer_local_release_supersedes_an_older_remembered_restriction() {
    let mut h = History::new();
    h.push("close", true, false, "kept");
    h.witness();
    let older = h.incoming();
    h.push("reopen", false, false, "kept");
    h.place(&[1, 2]);
    h.marker();
    let plan = plan_package_restore(&h.dir, &older).unwrap();
    restore_package_history(&h.dir, &plan).unwrap();
    assert_eq!(state(&h.dir).unwrap().view()["closed"], false);
}

#[test]
fn package_administration_resume_validates_frozen_prefix_even_after_process_memory_loss() {
    let mut h = History::new();
    h.push("close", true, false, "kept");
    h.witness();
    let incoming = h.incoming();
    let plan = plan_package_restore(&h.dir, &incoming).unwrap();
    ACCEPTED_HEADS.lock().unwrap().remove(&h.dir);
    let mut context = plan.source_context.clone();
    context["rememberedPrefix"][1] = json!("0".repeat(64));
    assert!(resume_package_restore(&h.dir, &incoming, &context)
        .unwrap_err()
        .contains("frozen original"));
    let mut context = plan.source_context.clone();
    context.as_object_mut().unwrap().remove("retention");
    assert!(resume_package_restore(&h.dir, &incoming, &context).is_err());
    let resumed = resume_package_restore(&h.dir, &incoming, &plan.source_context).unwrap();
    restore_package_history(&h.dir, &resumed).unwrap();
}

#[test]
fn package_administration_resume_refuses_valid_events_outside_original_intent() {
    let mut h = History::new();
    h.push("close", true, false, "kept");
    let incoming = h.incoming();
    let plan = plan_package_restore(&h.dir, &incoming).unwrap();
    h.push("reopen", false, false, "kept");
    h.place(&[1, 2]);
    h.marker();
    assert!(
        resume_package_restore(&h.dir, &incoming, &plan.source_context)
            .unwrap_err()
            .contains("outside the frozen")
    );
}

#[test]
fn package_administration_interrupted_private_staging_is_never_an_event_or_swept() {
    let mut h = History::new();
    h.push("close", true, false, "kept");
    let plan = plan_package_restore(&h.dir, &h.incoming()).unwrap();
    std::fs::create_dir_all(control(&h.dir).unwrap()).unwrap();
    let partial = control(&h.dir)
        .unwrap()
        .join(".package-restore-invented-crash-stage");
    std::fs::write(&partial, b"{partial unpublished stage").unwrap();
    let resumed = resume_package_restore(&h.dir, &h.incoming(), &plan.source_context).unwrap();
    restore_package_history(&h.dir, &resumed).unwrap();
    assert_eq!(
        std::fs::read(partial).unwrap(),
        b"{partial unpublished stage"
    );
    assert_eq!(local_history(&h.dir).unwrap().events, h.events);
}
