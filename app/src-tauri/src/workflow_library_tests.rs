//! Synthetic native-event tests use the real AAC capture/writer/receipt path.
use super::*;
use crate::act_control::{person, ActControl, HotA15Result};
struct Scratch(PathBuf);
impl Scratch {
    fn new() -> Self {
        let p = fs::canonicalize(std::env::temp_dir())
            .unwrap()
            .join(crate::util::opaque_id("chirality-library-").unwrap());
        fs::create_dir(&p).unwrap();
        Self(p)
    }
    fn owner(&self) -> LibraryOwner {
        LibraryOwner::open(self.0.clone(), "project", "fixture-project").unwrap()
    }
    /// A fresh owner (a new App process) with the App data folder attached.
    fn persistent_owner(&self) -> LibraryOwner {
        let mut owner = self.owner();
        owner.attach_app_kept_bases(&self.app_data()).unwrap();
        owner
    }
    fn app_data(&self) -> PathBuf {
        self.0.join("app-data")
    }
    fn base_files(&self) -> Vec<PathBuf> {
        fs::read_dir(self.app_data().join(BASE_STORE))
            .map(|d| {
                d.filter_map(|e| e.ok())
                    .filter(|e| !e.file_name().to_string_lossy().starts_with('.'))
                    .map(|e| e.path())
                    .collect()
            })
            .unwrap_or_default()
    }
    fn put(&self, name: &str, in_place: bool, body: &str) -> Snapshot {
        let p = self
            .0
            .join(".chirality")
            .join(if in_place {
                "workflows"
            } else {
                "workflow-drafts"
            })
            .join(name);
        fs::create_dir_all(&p).unwrap();
        fs::write(
            p.join("WORKFLOW.md"),
            format!("---\nname: {name}\n---\n# Method\n{body}\n"),
        )
        .unwrap();
        fs::write(p.join("notes.txt"), b"original notes\n").unwrap();
        Snapshot::capture(&p).unwrap()
    }
}
impl Drop for Scratch {
    fn drop(&mut self) {
        let _ = fs::remove_dir_all(&self.0);
    }
}
fn receipt(session: &ReviewSession) -> HotA15Receipt {
    let mut ac = ActControl::new(&session.root);
    let actor = person(
        Some("synthetic fixture; not native qualification"),
        Some("fixture"),
    );
    let context = json!({"home":"synthetic-test-home"});
    let offer = {
        let view = session.current().unwrap();
        ac.compose_a15(&view).unwrap()
    };
    let event = {
        let view = session.current().unwrap();
        ac.a15_confirmation_text(&offer, &view, &actor, &context)
            .unwrap();
        let digest = ac.frozen_a15_offer_digest(&offer).unwrap().clone();
        ac.present_a15(&offer).unwrap();
        crate::a15_native::ConfirmedA15Event::synthetic_for_test(
            offer.id().into(),
            digest,
            actor,
            context,
        )
    };
    let view = session.current().unwrap();
    match ac
        .confirm_a15_after_native_event(&offer, event, &view)
        .unwrap()
    {
        HotA15Result::Recorded(r) => r,
        _ => panic!("real synthetic capture/writer did not issue a receipt"),
    }
}
#[test]
fn actual_owner_snapshot_withdraws_after_resource_edit() {
    let s = Scratch::new();
    let snap = s.put("sample", false, "Work");
    let session = s.owner().review_draft("sample", snap.revision()).unwrap();
    assert_eq!(session.current().unwrap().ordered_bindings().count(), 1);
    fs::write(session.entries[0].live.join("notes.txt"), b"changed").unwrap();
    assert!(session.current().is_err());
    fs::write(
        session.entries[0].live.join("notes.txt"),
        b"original notes\n",
    )
    .unwrap();
    assert!(session.current().is_err());
}
#[test]
fn ordered_in_place_view_and_whole_offer_freshness() {
    let s = Scratch::new();
    s.put("one", true, "One");
    s.put("two", true, "Two");
    let session = s
        .owner()
        .review_in_place(&["two".into(), "one".into()])
        .unwrap();
    let view = session.current().unwrap();
    assert_eq!(view.descriptor_kind(), "a15_multi_descriptor");
    assert_eq!(
        view.ordered_bindings()
            .map(|e| e.subject().name.clone())
            .collect::<Vec<_>>(),
        ["two", "one"]
    );
    assert!(view
        .ordered_bindings()
        .all(|b| b.reviewed_id3().starts_with("entry:")));
    fs::write(session.entries[1].live.join("notes.txt"), b"new").unwrap();
    assert!(session.current().is_err());
}
#[test]
fn draft_after_capture_commits_original_bytes_and_canonical_ledger() {
    let s = Scratch::new();
    let snap = s.put("sample", false, "Original");
    let session = s.owner().review_draft("sample", snap.revision()).unwrap();
    let r = receipt(&session);
    fs::write(
        session.entries[0].live.join("notes.txt"),
        b"later draft edit",
    )
    .unwrap();
    let mut attempt = session.begin_hot_registration(r).unwrap();
    let outcomes = attempt.advance();
    let revision = match &outcomes[0] {
        EntryOutcome::Registered {
            revision,
            publication: PublicationOutcome::Current,
        } => revision,
        _ => panic!("expected original snapshot registration: {outcomes:?}"),
    };
    assert_eq!(revision.snapshot.files(), snap.files());
    let rows = read_ledger(&s.0).unwrap();
    assert_eq!(rows.len(), 1);
    super::super::wr_validate("library_entry", &rows[0]).unwrap();
    assert_eq!(rows[0]["identity"]["revision"], snap.revision());
    assert_eq!(attempt.advance().len(), 1);
    assert_eq!(read_ledger(&s.0).unwrap().len(), 1);
}
#[test]
fn in_place_changed_after_capture_is_terminal_while_sibling_commits() {
    let s = Scratch::new();
    s.put("one", true, "One");
    s.put("two", true, "Two");
    let session = s
        .owner()
        .review_in_place(&["one".into(), "two".into()])
        .unwrap();
    let r = receipt(&session);
    fs::write(
        session.entries[0].live.join("notes.txt"),
        b"changed after capture",
    )
    .unwrap();
    let mut attempt = session.begin_hot_registration(r).unwrap();
    let out = attempt.advance();
    assert!(matches!(&out[0], EntryOutcome::NotCompleted { .. }));
    assert!(matches!(&out[1], EntryOutcome::Registered { .. }));
    fs::write(
        attempt.session.entries[0].live.join("notes.txt"),
        b"original notes\n",
    )
    .unwrap();
    let out = attempt.advance();
    assert!(matches!(&out[0], EntryOutcome::NotCompleted { .. }));
    assert_eq!(read_ledger(&s.0).unwrap().len(), 2);
}
#[test]
fn store_conflict_records_no_effect_without_selection() {
    let s = Scratch::new();
    let snap = s.put("sample", false, "Original");
    let session = s.owner().review_draft("sample", snap.revision()).unwrap();
    let r = receipt(&session);
    let store = store_path(&s.0, &session.entries[0].review.identity);
    fs::create_dir_all(&store).unwrap();
    fs::write(store.join("WORKFLOW.md"), b"different").unwrap();
    let mut a = session.begin_hot_registration(r).unwrap();
    assert!(matches!(&a.advance()[0], EntryOutcome::NotCompleted { .. }));
    assert_eq!(read_ledger(&s.0).unwrap()[0]["outcome"], "not completed");
}
#[test]
fn postcommit_convenience_copy_failure_retains_registered_store() {
    let s = Scratch::new();
    let snap = s.put("sample", false, "Original");
    let session = s.owner().review_draft("sample", snap.revision()).unwrap();
    let r = receipt(&session);
    let parent = s.0.join(".chirality/workflows");
    fs::write(&parent, b"blocks convenience directory").unwrap();
    let mut a = session.begin_hot_registration(r).unwrap();
    let out = a.advance();
    assert!(matches!(
        &out[0],
        EntryOutcome::Registered {
            publication: PublicationOutcome::RepairPending(_),
            ..
        }
    ));
    assert_eq!(read_ledger(&s.0).unwrap()[0]["outcome"], "registered");
}
#[test]
fn wrong_review_receipt_is_consumed_without_library_effect() {
    let s = Scratch::new();
    let snap = s.put("sample", false, "Original");
    let owner = s.owner();
    let one = owner.review_draft("sample", snap.revision()).unwrap();
    let two = owner.review_draft("sample", snap.revision()).unwrap();
    let r = receipt(&one);
    assert!(two.begin_hot_registration(r).is_err());
    assert!(read_ledger(&s.0).unwrap().is_empty());
}
#[test]
fn malformed_cold_ledger_refuses_observation_without_origin_promotion() {
    let s = Scratch::new();
    let snap = s.put("sample", false, "Original");
    fs::write(
        s.0.join(".chirality/workflow-registry.jsonl"),
        b"{\"partial\":",
    )
    .unwrap();
    assert!(s.owner().review_draft("sample", snap.revision()).is_err());
}

#[test]
fn uncertain_ledger_append_retries_same_hot_line_without_duplicate() {
    let s = Scratch::new();
    let snap = s.put("sample", false, "Original");
    let session = s.owner().review_draft("sample", snap.revision()).unwrap();
    let r = receipt(&session);
    let mut a = session.begin_hot_registration(r).unwrap();
    FAIL_LEDGER_SYNC.with(|fail| fail.set(true));
    assert!(matches!(&a.advance()[0], EntryOutcome::Pending { .. }));
    assert_eq!(read_ledger(&s.0).unwrap().len(), 1);
    assert!(matches!(&a.advance()[0], EntryOutcome::Registered { .. }));
    assert_eq!(read_ledger(&s.0).unwrap().len(), 1);
}
#[test]
fn actual_latest_slot_change_after_capture_records_second_act_no_effect() {
    let s = Scratch::new();
    let snap = s.put("sample", false, "Original");
    let owner = s.owner();
    let one = owner.review_draft("sample", snap.revision()).unwrap();
    let two = owner.review_draft("sample", snap.revision()).unwrap();
    let r1 = receipt(&one);
    let r2 = receipt(&two);
    let mut a1 = one.begin_hot_registration(r1).unwrap();
    let mut a2 = two.begin_hot_registration(r2).unwrap();
    assert!(matches!(&a1.advance()[0], EntryOutcome::Registered { .. }));
    assert!(matches!(
        &a2.advance()[0],
        EntryOutcome::NotCompleted { .. }
    ));
    let rows = read_ledger(&s.0).unwrap();
    assert_eq!(rows.len(), 2);
    assert_ne!(rows[0]["act"], rows[1]["act"]);
}
#[test]
fn changed_unrecorded_copy_is_preserved_before_postcommit_publication() {
    let s = Scratch::new();
    let snap = s.put("sample", false, "Original");
    let session = s.owner().review_draft("sample", snap.revision()).unwrap();
    let r = receipt(&session);
    let changed = s.put("sample", true, "Outside registration");
    let mut a = session.begin_hot_registration(r).unwrap();
    assert!(matches!(
        &a.advance()[0],
        EntryOutcome::Registered {
            publication: PublicationOutcome::Current,
            ..
        }
    ));
    let kept =
        s.0.join(".chirality/workflow-unrecorded/sample")
            .join(changed.revision());
    assert_eq!(Snapshot::capture(&kept).unwrap().files(), changed.files());
    assert_eq!(
        Snapshot::capture(&s.0.join(".chirality/workflows/sample"))
            .unwrap()
            .files(),
        snap.files()
    );
}
#[test]
fn disclosed_prior_facts_do_not_block_new_hot_capture_or_authenticate_old_act() {
    let s = Scratch::new();
    let old = s.put("sample", false, "Old");
    let original = s.owner();
    let one = original.review_draft("sample", old.revision()).unwrap();
    let r = receipt(&one);
    let mut a = one.begin_hot_registration(r).unwrap();
    assert!(matches!(&a.advance()[0], EntryOutcome::Registered { .. }));
    // A new owner has only readable ledger facts; no original AAC custody is imported.
    let owner = s.owner();
    let old_identity = latest(&read_ledger(&s.0).unwrap()).unwrap().unwrap();
    // Explicit fixture for the preserved App-kept base pointer, not a native receipt.
    owner
        .bases
        .lock()
        .unwrap()
        .insert("sample".into(), old_identity);
    let new = s.put("sample", false, "New");
    let two = owner.review_draft("sample", new.revision()).unwrap();
    assert!(two
        .current()
        .unwrap()
        .review_presentation()
        .to_string()
        .contains("no earlier native-act authentication"));
    let r = receipt(&two);
    let mut a = two.begin_hot_registration(r).unwrap();
    assert!(matches!(&a.advance()[0], EntryOutcome::Registered { .. }));
    assert_eq!(read_ledger(&s.0).unwrap().len(), 2);
}

#[test]
fn hr1_new_store_parent_sync_failure_cannot_reach_g4_then_same_hot_retry_commits() {
    struct ResetSync;
    impl Drop for ResetSync {
        fn drop(&mut self) {
            storage::fail_directory_for_test(None);
        }
    }
    let s = Scratch::new();
    let snapshot = s.put("sample", false, "Original");
    let session = s
        .owner()
        .review_draft("sample", snapshot.revision())
        .unwrap();
    let native_receipt = receipt(&session);
    let store = store_path(&s.0, &session.entries[0].review.identity);
    let parent = store.parent().unwrap();
    // Establish parent first: injection targets only publication of its NEW child.
    storage::ensure_directory(parent).unwrap();
    assert!(!store.exists());
    storage::fail_directory_for_test(Some(parent.to_path_buf()));
    let _reset = ResetSync;
    let mut attempt = session.begin_hot_registration(native_receipt).unwrap();
    let first = attempt.advance();
    assert!(
        matches!(&first[0], EntryOutcome::Pending { .. }),
        "parent durability failure must withhold Registered: {first:?}"
    );
    assert!(
        read_ledger(&s.0).unwrap().is_empty(),
        "G4 cannot precede store directory publication durability"
    );
    assert_eq!(Snapshot::capture(&store).unwrap().files(), snapshot.files());
    storage::fail_directory_for_test(None);
    assert!(matches!(
        &attempt.advance()[0],
        EntryOutcome::Registered { .. }
    ));
    assert_eq!(read_ledger(&s.0).unwrap().len(), 1);
    assert!(matches!(
        &attempt.advance()[0],
        EntryOutcome::Registered { .. }
    ));
    assert_eq!(read_ledger(&s.0).unwrap().len(), 1);
}

#[test]
fn listed_revision_reads_actual_bytes_and_stale_listing_still_refuses_review() {
    let s = Scratch::new();
    let snapshot = s.put("sample", false, "Original");
    let owner = s.owner();
    let listed = owner.listed_draft_revision("sample").unwrap();
    assert_eq!(listed, snapshot.revision());
    assert!(owner.review_draft("sample", &listed).is_ok());
    fs::write(
        s.0.join(".chirality/workflow-drafts/sample/notes.txt"),
        b"changed after listing",
    )
    .unwrap();
    assert!(owner.review_draft("sample", &listed).is_err());
    let refreshed = owner.listed_draft_revision("sample").unwrap();
    assert_ne!(refreshed, listed);
    assert!(owner.review_draft("sample", &refreshed).is_ok());
    assert!(owner.listed_draft_revision("../other").is_err());
}

// ---- J5: App-kept base persistence and re-registration after process loss.

/// Registers the draft `sample` through one review, receipt and attempt.
fn register(owner: &LibraryOwner, revision: &str) -> RegisteredRevision {
    let session = owner.review_draft("sample", revision).unwrap();
    let r = receipt(&session);
    let mut attempt = session.begin_hot_registration(r).unwrap();
    let outcomes = attempt.advance();
    assert_eq!(outcomes.len(), 1, "one entry, one outcome: {outcomes:?}");
    match &outcomes[0] {
        EntryOutcome::Registered { revision, .. } => revision.clone(),
        other => panic!("expected registration: {other:?}"),
    }
}

#[test]
fn j5_relaunch_reregisters_same_slot_from_persisted_app_kept_base() {
    let s = Scratch::new();
    let one = s.put("sample", false, "One");
    let first = register(&s.persistent_owner(), one.revision());
    assert_eq!(
        s.base_files().len(),
        1,
        "G-6 base persisted in the App data folder"
    );
    // Process loss: every owner and session is gone. A process without the App
    // data folder has no base, so K-6 refuses the same name (the J4 finding).
    let two = s.put("sample", false, "Two (refined after relaunch)");
    let refused = s.owner().review_draft("sample", two.revision());
    assert!(
        refused.as_ref().is_err_and(|e| e.starts_with("DS-3")),
        "{:?}",
        refused.err()
    );
    // The relaunched App reads its own App-kept base: DS-2 on a new genuine A15.
    let owner = s.persistent_owner();
    let session = owner.review_draft("sample", two.revision()).unwrap();
    let view = session.current().unwrap();
    let entry = &view.review_presentation()["entries"][0];
    assert_eq!(entry["disposition"], "new revision");
    assert_eq!(
        entry["prior_revision"]["revision"],
        first.identity().revision.as_str()
    );
    assert_eq!(
        entry["base"]["revision"],
        first.identity().revision.as_str()
    );
    assert_eq!(
        entry["base_observation"]["observed"]["source"],
        "App data folder"
    );
    assert_eq!(
        entry["base_observation"]["observed"]["record"]["base_recorded_by"],
        "app"
    );
    assert!(entry["ledger_observation"]["standing"]
        .as_str()
        .unwrap()
        .contains("not replay proof"));
    assert_eq!(
        view.ordered_bindings().next().unwrap().prior(),
        Some(first.identity())
    );
    drop(view);
    let r = receipt(&session);
    let mut attempt = session.begin_hot_registration(r).unwrap();
    let outcomes = attempt.advance();
    // Only the new revision is a registered value; the disclosed prior is not promoted.
    assert_eq!(outcomes.len(), 1);
    let second = match &outcomes[0] {
        EntryOutcome::Registered { revision, .. } => revision.clone(),
        other => panic!("expected the new revision: {other:?}"),
    };
    assert_eq!(second.identity().revision, two.revision());
    assert_ne!(second.identity().revision, first.identity().revision);
    let rows = read_ledger(&s.0).unwrap();
    assert_eq!(rows.len(), 2);
    assert_eq!(rows[1]["disposition"], "new revision");
    assert_eq!(rows[1]["sequence"], 2);
    assert_eq!(
        rows[1]["prior_revision"], rows[0]["identity"],
        "the new act names the disclosed prior"
    );
    assert_eq!(
        rows[1]["identity"]["derived_from"]["revision"],
        first.identity().revision.as_str()
    );
    assert_ne!(
        rows[1]["act"], rows[0]["act"],
        "a new act, not the old one reused"
    );
    // G-6 again: the next relaunch sees revision 2 as the base.
    let record: Value = serde_json::from_slice(&fs::read(&s.base_files()[0]).unwrap()).unwrap();
    assert_eq!(record["base"]["revision"], two.revision());
    assert_eq!(record["state"], "registered, unchanged since");
    // Identical content in the same process stays DS-4: this process holds revision 2.
    let identical = owner.review_draft("sample", two.revision());
    assert!(
        identical.as_ref().is_err_and(|e| e.starts_with("DS-4")),
        "{:?}",
        identical.err()
    );
    // After a relaunch it is DS-8 re-confirmation, by the owner's CC-WR-RECONFIRM
    // decision (was DS-4 here before J8; CI-21 (b) closed by adoption).
    let relaunched = s
        .persistent_owner()
        .review_draft("sample", two.revision())
        .unwrap();
    assert_eq!(
        relaunched.current().unwrap().descriptor()["disposition"],
        "re-confirmation"
    );
}

#[test]
fn j5_app_kept_base_is_frozen_and_rechecked_at_current_and_under_the_ledger_lock() {
    let s = Scratch::new();
    let one = s.put("sample", false, "One");
    register(&s.persistent_owner(), one.revision());
    let two = s.put("sample", false, "Two");
    let owner = s.persistent_owner();
    // Before capture: a changed base withdraws the review.
    let session = owner.review_draft("sample", two.revision()).unwrap();
    let file = s.base_files()[0].clone();
    let original = fs::read(&file).unwrap();
    let mut changed: Value = serde_json::from_slice(&original).unwrap();
    changed["observed_at"] = json!("2026-10-07T00:00:00Z");
    fs::write(&file, serde_json::to_vec(&changed).unwrap()).unwrap();
    let stale = session.current().err().unwrap();
    assert!(
        stale.contains("App-kept base changed since review"),
        "{stale}"
    );
    // After capture: G1 under the lock ends the attempt, citing the act, with no effect.
    fs::write(&file, &original).unwrap();
    let session = owner.review_draft("sample", two.revision()).unwrap();
    let r = receipt(&session);
    fs::write(&file, serde_json::to_vec(&changed).unwrap()).unwrap();
    let mut attempt = session.begin_hot_registration(r).unwrap();
    match &attempt.advance()[0] {
        EntryOutcome::NotCompleted { reason, .. } => {
            assert!(
                reason.contains("App-kept base changed since review"),
                "{reason}"
            )
        }
        other => panic!("expected no effect: {other:?}"),
    }
    let rows = read_ledger(&s.0).unwrap();
    assert_eq!(rows.len(), 2);
    assert_eq!(rows[1]["outcome"], "not completed");
    // An unreadable base under the lock keeps a fresh attempt pending with its cause.
    fs::write(&file, &original).unwrap();
    let session = owner.review_draft("sample", two.revision()).unwrap();
    let r = receipt(&session);
    fs::write(&file, b"{not json").unwrap();
    let mut attempt = session.begin_hot_registration(r).unwrap();
    match &attempt.advance()[0] {
        EntryOutcome::Pending { reason, .. } => {
            assert!(
                reason.contains("App-kept base record malformed"),
                "{reason}"
            )
        }
        other => panic!("expected pending: {other:?}"),
    }
    assert_eq!(
        read_ledger(&s.0).unwrap().len(),
        2,
        "nothing appended while pending"
    );
}

#[test]
fn j5_unusable_app_kept_base_record_refuses_review_with_its_exact_cause() {
    let s = Scratch::new();
    let one = s.put("sample", false, "One");
    register(&s.persistent_owner(), one.revision());
    let two = s.put("sample", false, "Two");
    let file = s.base_files()[0].clone();
    let original: Value = serde_json::from_slice(&fs::read(&file).unwrap()).unwrap();
    let mut other = original.clone();
    other["draft"]["name"] = json!("other");
    let cases: Vec<(Vec<u8>, &str)> = vec![
        (b"{not json".to_vec(), "App-kept base record malformed"),
        (
            serde_json::to_vec(&json!({"record_kind":"draft_reference"})).unwrap(),
            "App-kept base record malformed",
        ),
        (
            serde_json::to_vec(&other).unwrap(),
            "App-kept base record ambiguous",
        ),
    ];
    for (bytes, cause) in cases {
        fs::write(&file, &bytes).unwrap();
        let error = s
            .persistent_owner()
            .review_draft("sample", two.revision())
            .err()
            .unwrap();
        assert!(
            error.contains(cause) && error.contains(&file.display().to_string()),
            "{error}"
        );
        assert!(
            !error.starts_with("DS-3"),
            "an exact cause, not a blanket name refusal: {error}"
        );
    }
    // An unreadable record (here a directory in its place) names that cause too.
    fs::remove_file(&file).unwrap();
    fs::create_dir(&file).unwrap();
    let error = s
        .persistent_owner()
        .review_draft("sample", two.revision())
        .err()
        .unwrap();
    assert!(error.contains("App-kept base record unreadable"), "{error}");
}

#[test]
fn j5_removed_draft_drops_its_app_kept_base_and_a_recreated_draft_is_ds3() {
    let s = Scratch::new();
    let one = s.put("sample", false, "One");
    register(&s.persistent_owner(), one.revision());
    assert_eq!(s.base_files().len(), 1);
    fs::remove_dir_all(s.0.join(".chirality/workflow-drafts/sample")).unwrap();
    assert!(s
        .persistent_owner()
        .listed_draft_revision("sample")
        .is_err());
    assert!(
        s.base_files().is_empty(),
        "WR §5.1: the App's base pointer is dropped"
    );
    let fresh = s.put("sample", false, "Written from scratch");
    let refused = s
        .persistent_owner()
        .review_draft("sample", fresh.revision());
    assert!(
        refused.as_ref().is_err_and(|e| e.starts_with("DS-3")),
        "{:?}",
        refused.err()
    );
}

#[test]
fn j5_ledger_refusals_name_their_exact_cause() {
    let s = Scratch::new();
    let one = s.put("sample", false, "One");
    register(&s.owner(), one.revision());
    let ledger = s.0.join(".chirality/workflow-registry.jsonl");
    let good = fs::read_to_string(&ledger).unwrap();
    let line: Value = serde_json::from_str(good.trim_end()).unwrap();
    let with = |edit: &dyn Fn(&mut Value)| {
        let mut v = line.clone();
        edit(&mut v);
        format!("{good}{}\n", serde_json::to_string(&v).unwrap())
    };
    let two = s.put("sample", false, "Two");
    let cases: Vec<(String, &str)> = vec![
        (good.trim_end().to_string(), "malformed: "),
        (format!("{good}{{\"partial\":\n"), "line 2 is not JSON"),
        (with(&|v| v["outcome"] = json!("auto-registered")), "line 2: WR library_entry refused"),
        (with(&|v| v["ledger_seq"] = json!(7)), "line 2 has ledger_seq 7, expected 2"),
        (
            with(&|v| v["ledger_seq"] = json!(2)),
            "registration ledger ambiguous for slot project:sample: ledger_seq 2 has sequence 1, expected 2",
        ),
        (
            with(&|v| {
                v["ledger_seq"] = json!(2);
                v["sequence"] = json!(2);
            }),
            "names prior revision null, but the slot's latest before it is",
        ),
        (
            with(&|v| {
                v["ledger_seq"] = json!(2);
                v["sequence"] = json!(2);
                v["prior_revision"] = line["identity"].clone();
            }),
            "a second time",
        ),
    ];
    for (bytes, cause) in cases {
        fs::write(&ledger, &bytes).unwrap();
        let error = s
            .owner()
            .review_draft("sample", two.revision())
            .err()
            .unwrap();
        assert!(error.contains(cause), "expected {cause:?} in {error:?}");
    }
    fs::remove_file(&ledger).unwrap();
    fs::create_dir(&ledger).unwrap();
    let error = s
        .owner()
        .review_draft("sample", two.revision())
        .err()
        .unwrap();
    assert!(
        error.starts_with("registration ledger unreadable: "),
        "{error}"
    );
}

/// V11 J5-1: SP-3 "made from" needs the App-kept base to be a revision OF the
/// slot, i.e. registered there per the ledger; a same-slot base the ledger never
/// registered is "lineage not established" (DS-3), shown as ID-4's "lineage
/// incomplete at ‹tuple›". The lineage limb (a base elsewhere whose derived-from
/// reaches the slot) is held to the same rule.
#[test]
fn v11_j5_1_app_kept_base_must_name_a_revision_registered_in_the_slot() {
    let s = Scratch::new();
    let one = s.put("sample", false, "One");
    let first = register(&s.persistent_owner(), one.revision());
    let two = s.put("sample", false, "Two");
    let file = s.base_files()[0].clone();
    let original: Value = serde_json::from_slice(&fs::read(&file).unwrap()).unwrap();
    let fabricated = "0".repeat(64);
    let write_base = |base: Value| {
        let mut record = original.clone();
        record["base"] = base;
        fs::write(&file, serde_json::to_vec(&record).unwrap()).unwrap();
    };
    let mut unregistered = original["base"].clone();
    unregistered["revision"] = json!(fabricated);
    let host = |derived: Value| {
        json!({"kind":"workflow","origin":"host","source_root":"fixture-host","name":"sample",
            "revision":"1".repeat(64),"revision_method":SNAPSHOT_METHOD,"derived_from":derived})
    };
    for (base, label) in [
        (unregistered.clone(), "same-slot base never registered"),
        (
            host(unregistered.clone()),
            "lineage limb reaching an unregistered revision",
        ),
    ] {
        write_base(base);
        let refused = s
            .persistent_owner()
            .review_draft("sample", two.revision())
            .err()
            .unwrap_or_else(|| panic!("{label}: accepted"));
        assert!(refused.starts_with("DS-3"), "{label}: {refused}");
        assert!(
            refused.contains("lineage incomplete at project:sample@")
                && refused.contains(&fabricated),
            "{label}: {refused}"
        );
        assert_eq!(
            read_ledger(&s.0).unwrap().len(),
            1,
            "{label}: nothing registered"
        );
    }
    // The round trip (SP-3 second limb) still holds when the reached revision is registered.
    write_base(host(serde_json::to_value(first.identity()).unwrap()));
    let session = s
        .persistent_owner()
        .review_draft("sample", two.revision())
        .unwrap();
    assert_eq!(
        session.current().unwrap().review_presentation()["entries"][0]["disposition"],
        "new revision"
    );
    // And the ordinary same-slot base naming the registered latest stays DS-2.
    fs::write(&file, serde_json::to_vec(&original).unwrap()).unwrap();
    assert!(s
        .persistent_owner()
        .review_draft("sample", two.revision())
        .is_ok());
}

/// V11 J5-3 (reviewer probe P2): the base key is the whole draft key {draft
/// location, draft root, name}. Two libraries with the same draft name, sharing
/// one App data folder, keep separate bases; the same root under another origin
/// sees none of them.
#[test]
fn v11_j5_3_same_draft_name_in_two_libraries_keeps_separate_app_kept_bases() {
    let a = Scratch::new();
    let b = Scratch::new();
    let app_data = a.app_data();
    let owner = |s: &Scratch, origin: &str| {
        let mut owner = LibraryOwner::open(s.0.clone(), origin, "fixture-project").unwrap();
        owner.attach_app_kept_bases(&app_data).unwrap();
        owner
    };
    let a1 = a.put("sample", false, "A one");
    let first_a = register(&owner(&a, "project"), a1.revision());
    let b1 = b.put("sample", false, "B one");
    let first_b = register(&owner(&b, "project"), b1.revision());
    assert_eq!(a.base_files().len(), 2, "one record per draft key");
    // Library A, relaunched after B registered: still DS-2 from A's own base.
    let a2 = a.put("sample", false, "A two");
    let session = owner(&a, "project")
        .review_draft("sample", a2.revision())
        .unwrap();
    let entry = session.current().unwrap().review_presentation()["entries"][0].clone();
    assert_eq!(entry["disposition"], "new revision");
    assert_eq!(
        entry["base"]["revision"],
        first_a.identity().revision.as_str()
    );
    // Library B likewise.
    let b2 = b.put("sample", false, "B two");
    let session = owner(&b, "project")
        .review_draft("sample", b2.revision())
        .unwrap();
    let entry = session.current().unwrap().review_presentation()["entries"][0].clone();
    assert_eq!(
        entry["base"]["revision"],
        first_b.identity().revision.as_str()
    );
    // The same root as a user library: another draft location, so no base.
    let user = owner(&a, "user").base_custody().get("sample").unwrap();
    assert_eq!(user.base, None);
    assert_eq!(user.source["record"], "none for this draft key");
}

/// J8 control (WR-VC-16 first half): after a relaunch, the registered draft left
/// unchanged reviews as DS-8 re-confirmation, not DS-4.
#[test]
fn j8_control_relaunch_unchanged_registered_draft_reviews_as_ds8() {
    let s = Scratch::new();
    let one = s.put("sample", false, "One");
    register(&s.persistent_owner(), one.revision());
    let session = s
        .persistent_owner()
        .review_draft("sample", one.revision())
        .expect("DS-8 offered after relaunch");
    let descriptor = session.current().unwrap().descriptor().clone();
    assert_eq!(descriptor["disposition"], "re-confirmation");
    assert_eq!(
        descriptor["wording"],
        "re-confirm workflow revision for use"
    );
}

// ---- J8: CC-WR-RECONFIRM (WR §4.8 RC-1…RC-10, RF-1; WR-VC-16…WR-VC-20).
// Per V13 R2-N2, LS-1 "as read" only gates the DS-8 offer: none of these tests
// treats it as a trust signal, and nothing is selectable without a new act.

/// One DS-8 review, a synthetic native A15 and one advance.
fn reconfirm(owner: &LibraryOwner, revision: &str) -> (Vec<EntryOutcome>, String) {
    let session = owner.review_draft("sample", revision).unwrap();
    let r = receipt(&session);
    let record = r.record_id().to_string();
    let mut attempt = session.begin_hot_registration(r).unwrap();
    (attempt.advance(), record)
}
fn ledger(s: &Scratch) -> Vec<Value> {
    read_ledger(&s.0).unwrap()
}
fn store_folders(s: &Scratch) -> usize {
    fs::read_dir(s.0.join(".chirality/workflow-revisions/sample"))
        .map(|d| d.count())
        .unwrap_or(0)
}
/// SQ-X X-1's view: A15 entries of the library that no ledger line cites. An
/// attempt is closed exactly when its A15 has its ledger line (no journal).
fn uncited_count(s: &Scratch) -> usize {
    uncited(&s.0, "project", "fixture-project", &ledger(s))
        .unwrap()
        .len()
}
fn reconfirmed(outcome: &EntryOutcome) -> RegisteredRevision {
    match outcome {
        EntryOutcome::ReConfirmed { revision, .. } => revision.clone(),
        other => panic!("expected re-confirmed: {other:?}"),
    }
}

/// WR-VC-16: register ‹k›; relaunch; the registered draft, unchanged, reviews as
/// DS-8; a new A15 re-confirms ‹k› with no new revision, sequence, store or copy;
/// ‹k› is then selectable in that process only.
#[test]
fn wr_vc_16_reconfirm_after_relaunch_keeps_the_revision_and_needs_a_new_act() {
    let s = Scratch::new();
    let one = s.put("sample", false, "One");
    let first = register(&s.persistent_owner(), one.revision());
    let before = ledger(&s);
    let copy = Snapshot::capture(&s.0.join(".chirality/workflows/sample")).unwrap();
    // Relaunch: a new owner holds nothing; LS-1 as read gates the offer only.
    let owner = s.persistent_owner();
    assert!(
        !owner.is_held(first.identity()),
        "nothing selectable from disk"
    );
    let session = owner.review_draft("sample", one.revision()).unwrap();
    {
        let view = session.current().unwrap();
        let d = view.descriptor();
        assert_eq!(d["disposition"], "re-confirmation");
        assert_eq!(d["wording"], "re-confirm workflow revision for use");
        assert_eq!(
            d["purpose"],
            "make it available again in this App session from the project library"
        );
        assert_eq!(
            d["subject"], before[0]["identity"],
            "RC-3: ‹k›'s tuple as its line records it"
        );
        assert_eq!(
            d["relations"]["prior_revision"],
            Value::Null,
            "‹k›'s own prior"
        );
        assert_eq!(
            d["reconfirms"],
            json!({"identity":before[0]["identity"],"ledger_seq":1,"sequence":1})
        );
        assert_eq!(
            d["freshness"]["slot_latest"],
            json!({"method":SNAPSHOT_METHOD,"value":one.revision()}),
            "RC-5: the slot's latest at review"
        );
        let entry = &view.review_presentation()["entries"][0];
        assert!(entry["message"]
            .as_str()
            .unwrap()
            .contains("not verified in this session"));
        let rc = &entry["reconfirmation"];
        assert_eq!(rc["sequence"], 1);
        assert!(rc["standing"].as_str().unwrap().starts_with("LS-1"));
        assert_eq!(rc["registered_earlier"]["act"], before[0]["act"]);
        assert_eq!(
            rc["statement"],
            "Re-confirm revision 1 of project:sample for use in this App session. This registers no new revision."
        );
        let binding = view.ordered_bindings().next().unwrap();
        assert_eq!(binding.subject(), first.identity());
        assert_eq!(binding.prior(), None);
    }
    let r = receipt(&session);
    let record = r.record_id().to_string();
    let mut attempt = session.begin_hot_registration(r).unwrap();
    let outcomes = attempt.advance();
    assert_eq!(outcomes.len(), 1);
    let again = reconfirmed(&outcomes[0]);
    assert_eq!(
        again.identity(),
        first.identity(),
        "no new revision identity"
    );
    assert_eq!(again.act_ref(), record, "the value cites the new act");
    assert_ne!(again.act_ref(), first.act_ref());
    let rows = ledger(&s);
    assert_eq!(rows.len(), 2);
    let line = &rows[1];
    assert_eq!(line["outcome"], "re-confirmed");
    assert_eq!(line["disposition"], "re-confirmation");
    assert_eq!(line["act"]["record_id"], record.as_str());
    assert_eq!(line["reconfirms"]["ledger_seq"], 1);
    for field in ["identity", "sequence", "prior_revision", "store_path"] {
        assert_eq!(line[field], rows[0][field], "{field}");
    }
    assert_eq!(store_folders(&s), 1, "no new store folder");
    assert_eq!(
        Snapshot::capture(&s.0.join(".chirality/workflows/sample"))
            .unwrap()
            .files(),
        copy.files(),
        "no published copy written"
    );
    assert_eq!(uncited_count(&s), 0, "the attempt closed");
    let (acts, _) = crate::records::read_log(&storage::library_log(&s.0));
    let act = acts
        .iter()
        .find(|a| a["recordId"] == record.as_str())
        .unwrap();
    assert_eq!(
        act["body"]["purpose"],
        "make it available again in this App session from the project library"
    );
    // RC-2: selectable here (DS-4 for identical bytes), not after another relaunch.
    assert!(owner.is_held(first.identity()));
    let here = owner.review_draft("sample", one.revision()).err().unwrap();
    assert!(
        here.starts_with("DS-4: identical to revision 1; select it instead"),
        "{here}"
    );
    let later = s
        .persistent_owner()
        .review_draft("sample", one.revision())
        .unwrap();
    assert_eq!(
        later.current().unwrap().descriptor()["disposition"],
        "re-confirmation"
    );
    // G-6R: ‹k› is the draft's App-kept base.
    let record: Value = serde_json::from_slice(&fs::read(&s.base_files()[0]).unwrap()).unwrap();
    assert_eq!(record["base"]["revision"], one.revision());
    assert_eq!(record["state"], "registered, unchanged since");
}

/// WR-VC-17: DS-4 while ‹k› is selectable in this process, or when ‹k› is not
/// LS-1 (with its exact cause); after the record or bytes are restored, DS-8.
#[test]
fn wr_vc_17_ds4_while_selectable_or_not_ls1_with_exact_cause() {
    let s = Scratch::new();
    let one = s.put("sample", false, "One");
    let owner = s.persistent_owner();
    register(&owner, one.revision());
    let same = owner.review_draft("sample", one.revision()).err().unwrap();
    assert!(
        same.starts_with("DS-4: identical to revision 1; select it instead"),
        "{same}"
    );
    // LS-4: the A15 record missing.
    let log = storage::library_log(&s.0);
    let aside = s.0.join("acts-aside.jsonl");
    fs::rename(&log, &aside).unwrap();
    let missing = s
        .persistent_owner()
        .review_draft("sample", one.revision())
        .err()
        .unwrap();
    assert!(
        missing.starts_with("DS-4") && missing.contains("LS-4") && missing.contains("not found"),
        "{missing}"
    );
    fs::rename(&aside, &log).unwrap();
    // LS-4: store bytes that no longer recompute.
    let store =
        s.0.join(".chirality/workflow-revisions/sample")
            .join(storage::key(one.revision()))
            .join("sample");
    fs::write(store.join("extra.txt"), b"x").unwrap();
    let bytes = s
        .persistent_owner()
        .review_draft("sample", one.revision())
        .err()
        .unwrap();
    assert!(
        bytes.starts_with("DS-4") && bytes.contains("does not recompute"),
        "{bytes}"
    );
    // RF-1 gives no draft from such a store either.
    fs::remove_dir_all(s.0.join(".chirality/workflow-drafts/sample")).unwrap();
    let refine = s
        .persistent_owner()
        .refine_from_store("sample", one.revision())
        .err()
        .unwrap();
    assert!(refine.contains("LS-4"), "{refine}");
    assert!(!s.0.join(".chirality/workflow-drafts/sample").exists());
    // Restored (§5.3): DS-8 applies.
    fs::remove_file(store.join("extra.txt")).unwrap();
    s.persistent_owner()
        .refine_from_store("sample", one.revision())
        .unwrap();
    let restored = s
        .persistent_owner()
        .review_draft("sample", one.revision())
        .unwrap();
    assert_eq!(
        restored.current().unwrap().descriptor()["disposition"],
        "re-confirmation"
    );
}

/// WR-VC-18: after a relaunch, a draft one byte away from ‹k› takes the ordinary
/// route: DS-2 with a base reaching the slot, DS-3 without one.
#[test]
fn wr_vc_18_changed_bytes_take_the_ordinary_route() {
    let s = Scratch::new();
    let one = s.put("sample", false, "One");
    register(&s.persistent_owner(), one.revision());
    let changed = s.put("sample", false, "One!");
    let ds2 = s
        .persistent_owner()
        .review_draft("sample", changed.revision())
        .unwrap();
    assert_eq!(
        ds2.current().unwrap().descriptor()["disposition"],
        "new revision"
    );
    let ds3 = s
        .owner()
        .review_draft("sample", changed.revision())
        .err()
        .unwrap();
    assert!(ds3.starts_with("DS-3"), "{ds3}");
    // Identical bytes without a base reaching the slot: K-6 first (SP-4a), DS-3.
    s.put("sample", false, "One");
    let k6 = s
        .owner()
        .review_draft("sample", one.revision())
        .err()
        .unwrap();
    assert!(k6.starts_with("DS-3"), "{k6}");
}

/// WR-VC-19: dismissal, staleness and loss have no effect.
#[test]
fn wr_vc_19_dismissal_staleness_and_loss_have_no_effect() {
    let s = Scratch::new();
    let one = s.put("sample", false, "One");
    let first = register(&s.persistent_owner(), one.revision());
    let owner = s.persistent_owner();
    // Control closed: nothing captured, ledger unchanged, ‹k› not selectable.
    let session = owner.review_draft("sample", one.revision()).unwrap();
    {
        let mut ac = ActControl::new(&s.0);
        let offer = ac.compose_a15(&session.current().unwrap()).unwrap();
        ac.dismiss_a15(&offer);
    }
    assert_eq!(ledger(&s).len(), 1);
    assert!(!owner.is_held(first.identity()));
    // Bytes changed between review and act: withdrawn, nothing captured.
    fs::write(
        s.0.join(".chirality/workflow-drafts/sample/notes.txt"),
        b"edit",
    )
    .unwrap();
    assert!(session.current().is_err());
    s.put("sample", false, "One");
    assert_eq!(ledger(&s).len(), 1);
    // ‹k› became selectable after capture: the second act has no effect.
    let a = owner.review_draft("sample", one.revision()).unwrap();
    let b = owner.review_draft("sample", one.revision()).unwrap();
    let (ra, rb) = (receipt(&a), receipt(&b));
    let mut first_attempt = a.begin_hot_registration(ra).unwrap();
    let mut second_attempt = b.begin_hot_registration(rb).unwrap();
    reconfirmed(&first_attempt.advance()[0]);
    match &second_attempt.advance()[0] {
        EntryOutcome::NotCompleted { reason, .. } => {
            assert!(
                reason.contains("already selectable in this App session"),
                "{reason}"
            )
        }
        other => panic!("expected no effect: {other:?}"),
    }
    let rows = ledger(&s);
    assert_eq!(rows.last().unwrap()["outcome"], "not completed");
    assert_eq!(rows.last().unwrap()["disposition"], "re-confirmation");
    assert_eq!(rows.last().unwrap()["reconfirms"]["ledger_seq"], 1);
    // Act record no longer found after capture (relaunched owner): no effect.
    let owner = s.persistent_owner();
    let session = owner.review_draft("sample", one.revision()).unwrap();
    let r = receipt(&session);
    let log = storage::library_log(&s.0);
    let kept = fs::read(&log).unwrap();
    // The record is renamed in place: the log still reads completely (V15 F4
    // keeps an unreadable log pending instead; tested separately).
    let renamed = String::from_utf8(kept.clone())
        .unwrap()
        .replace(first.act_ref(), "rec:app:renamed-elsewhere");
    fs::write(&log, renamed).unwrap();
    let mut attempt = session.begin_hot_registration(r).unwrap();
    let outcome = attempt.advance();
    fs::write(&log, kept).unwrap();
    match &outcome[0] {
        EntryOutcome::NotCompleted { reason, .. } => {
            assert!(
                reason.contains("registration record incomplete"),
                "{reason}"
            )
        }
        other => panic!("expected no effect: {other:?}"),
    }
    assert!(!owner.is_held(first.identity()));
    // Store no longer recomputes after capture: no effect, and nothing written to it.
    let owner = s.persistent_owner();
    let session = owner.review_draft("sample", one.revision()).unwrap();
    let r = receipt(&session);
    let store =
        s.0.join(".chirality/workflow-revisions/sample")
            .join(storage::key(one.revision()))
            .join("sample");
    fs::write(store.join("notes.txt"), b"tampered").unwrap();
    let mut attempt = session.begin_hot_registration(r).unwrap();
    match &attempt.advance()[0] {
        EntryOutcome::NotCompleted { reason, .. } => {
            assert!(reason.contains("store no longer recomputes"), "{reason}")
        }
        other => panic!("expected no effect: {other:?}"),
    }
    assert_eq!(
        fs::read(store.join("notes.txt")).unwrap(),
        b"tampered",
        "never repaired"
    );
    fs::write(store.join("notes.txt"), b"original notes\n").unwrap();
    assert_eq!(uncited_count(&s), 0, "every act has its line");
}

/// WR-VC-19 / RC-5 (F1): freshness is read against `freshness.slot_latest`. A
/// re-confirmation of an earlier ‹k› while the slot's latest is another revision
/// stays current until the latest changes, then has no effect.
#[test]
fn wr_vc_19_freshness_is_against_slot_latest_not_the_prior() {
    let s = Scratch::new();
    let one = s.put("sample", false, "One");
    register(&s.persistent_owner(), one.revision());
    let two = s.put("sample", false, "Two");
    let second = register(&s.persistent_owner(), two.revision());
    // Relaunch with revision 2's bytes: k = 2, its prior 1, the slot's latest 2.
    let owner = s.persistent_owner();
    let session = owner.review_draft("sample", two.revision()).unwrap();
    let d = session.current().unwrap().descriptor().clone();
    assert_eq!(d["relations"]["prior_revision"]["revision"], one.revision());
    assert_eq!(d["freshness"]["slot_latest"]["value"], two.revision());
    let r = receipt(&session);
    let mut attempt = session.begin_hot_registration(r).unwrap();
    assert_eq!(
        reconfirmed(&attempt.advance()[0]).identity(),
        second.identity()
    );
    // Back to revision 1's bytes (base 2 reaches the slot): k = 1, latest 2.
    s.put("sample", false, "One");
    let owner = s.persistent_owner();
    let session = owner.review_draft("sample", one.revision()).unwrap();
    let entry = session.current().unwrap().review_presentation()["entries"][0].clone();
    assert_eq!(
        entry["reconfirmation"]["slot_latest"]["revision"],
        two.revision()
    );
    let r = receipt(&session);
    // The slot moves on after capture: a third revision registered elsewhere.
    let mover = s.owner();
    mover
        .bases
        .lock()
        .unwrap()
        .insert("sample".into(), second.identity().clone());
    s.put("sample", false, "Three");
    let three = Snapshot::capture(&s.0.join(".chirality/workflow-drafts/sample")).unwrap();
    register(&mover, three.revision());
    s.put("sample", false, "One");
    assert!(session.current().is_err(), "RB-3 (b): the latest changed");
    let mut attempt = session.begin_hot_registration(r).unwrap();
    match &attempt.advance()[0] {
        EntryOutcome::NotCompleted { reason, .. } => {
            assert!(reason.contains("slot moved on"), "{reason}")
        }
        other => panic!("expected slot moved on: {other:?}"),
    }
}

/// WR-VC-19 / RC-7, X-2: process loss of a re-confirmation (owner ruling
/// 2026-10-10: no attempt journal; X-2 reads the A15 record). Lost after
/// capture, or after *stored* before G-4R: X-2 writes *not completed*, never
/// *re-confirmed*. Lost after G-4R became durable: X-2 finds the line citing the
/// act and writes nothing.
#[test]
fn wr_vc_19_process_loss_and_x2() {
    let s = Scratch::new();
    let one = s.put("sample", false, "One");
    let first = register(&s.persistent_owner(), one.revision());
    let lost_and_relaunched = |s: &Scratch, record: &str, at: usize| {
        let relaunched = s.persistent_owner();
        assert_eq!(relaunched.reconciliation().len(), 1, "{:?}", relaunched.reconciliation());
        assert!(relaunched.reconciliation()[0].contains("not completed"), "{:?}", relaunched.reconciliation());
        let rows = ledger(s);
        assert_eq!(rows.len(), at + 1);
        assert_eq!(rows[at]["outcome"], "not completed");
        assert_eq!(rows[at]["reason"], "process lost before re-confirmation committed");
        assert_eq!(rows[at]["disposition"], "re-confirmation");
        assert_eq!(rows[at]["reconfirms"]["ledger_seq"], 1);
        assert_eq!(rows[at]["act"]["record_id"], record);
        assert_eq!(uncited_count(s), 0);
        relaunched
    };
    // Lost after capture, before the attempt began: the A15 alone.
    {
        let owner = s.persistent_owner();
        let session = owner.review_draft("sample", one.revision()).unwrap();
        let record = receipt(&session).record_id().to_string();
        assert_eq!(uncited_count(&s), 1);
        drop(session);
        drop(owner);
        let relaunched = lost_and_relaunched(&s, &record, 1);
        assert!(!relaunched.is_held(first.identity()));
    }
    // Lost after *stored*, before G-4R.
    {
        let owner = s.persistent_owner();
        let session = owner.review_draft("sample", one.revision()).unwrap();
        let r = receipt(&session);
        let record = r.record_id().to_string();
        let mut attempt = session.begin_hot_registration(r).unwrap();
        LOSE_AT.with(|at| at.set(LOSE_BEFORE_COMMIT));
        assert!(matches!(&attempt.advance()[0], EntryOutcome::Pending { .. }));
        assert_eq!(ledger(&s).len(), 2);
        drop(attempt);
        drop(owner);
        let relaunched = lost_and_relaunched(&s, &record, 2);
        assert!(!relaunched.is_held(first.identity()), "X-2 never completes a re-confirmation");
        // A later open finds nothing to do.
        assert!(s.persistent_owner().reconciliation().is_empty());
    }
    // Lost after G-4R durable (uncertain sync): nothing written by X-2.
    {
        let owner = s.persistent_owner();
        let session = owner.review_draft("sample", one.revision()).unwrap();
        let r = receipt(&session);
        let record = r.record_id().to_string();
        let mut attempt = session.begin_hot_registration(r).unwrap();
        FAIL_LEDGER_SYNC.with(|fail| fail.set(true));
        assert!(matches!(&attempt.advance()[0], EntryOutcome::Pending { .. }));
        drop(attempt);
        drop(owner);
        let relaunched = s.persistent_owner();
        assert!(relaunched.reconciliation().is_empty(), "{:?}", relaunched.reconciliation());
        let rows = ledger(&s);
        assert_eq!(rows.len(), 4);
        assert_eq!(rows[3]["outcome"], "re-confirmed");
        assert_eq!(
            rows.iter().filter(|v| v["act"]["record_id"] == record.as_str()).count(),
            1,
            "one act, one ledger line"
        );
        assert!(!relaunched.is_held(first.identity()), "X-2 never completes a re-confirmation");
    }
}

// ---- SQ-X for registrations without an attempt journal (owner ruling
// 2026-10-10): X-2 decides from the A15 record and the store folder.

/// One draft review, capture and begin, lost at `at` (or after capture when
/// `at` is 0); returns the A15 record identity. The attempt is dropped, as a
/// lost process's memory is, which also ends its liveness lock.
fn lose_registration(owner: &LibraryOwner, revision: &str, at: u8) -> String {
    let session = owner.review_draft("sample", revision).unwrap();
    let r = receipt(&session);
    let record = r.record_id().to_string();
    if at == 0 {
        return record;
    }
    let mut attempt = session.begin_hot_registration(r).unwrap();
    LOSE_AT.with(|cell| cell.set(at));
    match &attempt.advance()[0] {
        EntryOutcome::Pending { reason, .. } => assert!(reason.contains("injected process loss"), "{reason}"),
        other => panic!("expected the injected loss: {other:?}"),
    }
    record
}
fn store_of(s: &Scratch, revision: &str) -> PathBuf {
    s.0.join(".chirality/workflow-revisions/sample")
        .join(storage::key(revision))
        .join("sample")
}

/// Lost after the store copy (G-3) and before G-4, the slot unchanged: X-2
/// completes G-4 and G-5 citing the same A15. Nothing is selectable from it in
/// the new process (RC-2); its standing reads LS-1 (a DS-8 review follows).
#[test]
fn sqx_registration_lost_after_store_completes_citing_the_same_a15() {
    let s = Scratch::new();
    let one = s.put("sample", false, "One");
    let record = lose_registration(&s.persistent_owner(), one.revision(), LOSE_BEFORE_COMMIT);
    assert!(store_of(&s, one.revision()).is_dir(), "stored before the loss");
    assert!(ledger(&s).is_empty());
    assert!(!s.0.join(".chirality/workflows/sample").exists());
    let relaunched = s.persistent_owner();
    assert_eq!(relaunched.reconciliation().len(), 1, "{:?}", relaunched.reconciliation());
    assert!(relaunched.reconciliation()[0].contains("completed at relaunch"), "{:?}", relaunched.reconciliation());
    let rows = ledger(&s);
    assert_eq!(rows.len(), 1);
    let line = &rows[0];
    assert_eq!(line["outcome"], "registered");
    assert_eq!(line["act"]["record_id"], record.as_str(), "the same A15");
    assert_eq!(line["sequence"], 1);
    assert_eq!(line["disposition"], "new workflow");
    assert_eq!(line["prior_revision"], Value::Null);
    assert_eq!(line["identity"]["revision"], one.revision());
    assert_eq!(line["reviewed_draft"]["draft"]["name"], "sample");
    assert!(line["store_path"].as_str().unwrap().starts_with(".chirality/workflow-revisions/sample/"));
    super::super::wr_validate("library_entry", line).unwrap();
    // G-5: the published copy is the registered bytes.
    assert_eq!(
        Snapshot::capture(&s.0.join(".chirality/workflows/sample")).unwrap().files(),
        one.files()
    );
    let k: WorkflowIdentity = serde_json::from_value(line["identity"].clone()).unwrap();
    assert!(!relaunched.is_held(&k), "RC-2: nothing selectable from X-2");
    // X-2 records no App-kept base (G-6 is the live process's): the old draft is
    // DS-3 (K-6), and Refine (RF-1), which needs LS-1 as read, gives a DS-8 draft.
    assert!(relaunched.review_draft("sample", one.revision()).err().unwrap().starts_with("DS-3"));
    fs::remove_dir_all(s.0.join(".chirality/workflow-drafts/sample")).unwrap();
    relaunched.refine_from_store("sample", one.revision()).unwrap();
    assert_eq!(
        relaunched.review_draft("sample", one.revision()).unwrap().current().unwrap().descriptor()["disposition"],
        "re-confirmation",
        "LS-1 as read: the A15 record and the store"
    );
    assert!(s.persistent_owner().reconciliation().is_empty(), "nothing left");
}

/// Lost after the store copy, but the slot moved on before relaunch: *not
/// completed*; the store folder is left as it is.
#[test]
fn sqx_registration_slot_moved_on_is_not_completed() {
    let s = Scratch::new();
    let one = s.put("sample", false, "One");
    let first = register(&s.persistent_owner(), one.revision());
    // A second process, opened before the loss, registers later.
    let mover = s.owner();
    let two = s.put("sample", false, "Two");
    let record = lose_registration(&s.persistent_owner(), two.revision(), LOSE_BEFORE_COMMIT);
    mover.bases.lock().unwrap().insert("sample".into(), first.identity().clone());
    let three = s.put("sample", false, "Three");
    register(&mover, three.revision());
    let relaunched = s.persistent_owner();
    assert!(relaunched.reconciliation()[0].contains("not completed: slot moved on"), "{:?}", relaunched.reconciliation());
    let rows = ledger(&s);
    assert_eq!(rows.len(), 3);
    assert_eq!(rows[2]["outcome"], "not completed");
    assert_eq!(rows[2]["act"]["record_id"], record.as_str());
    assert_eq!(rows[2]["identity"]["revision"], two.revision());
    assert!(rows[2]["reason"].as_str().unwrap().starts_with("slot moved on"));
    assert_eq!(
        Snapshot::capture(&store_of(&s, two.revision())).unwrap().files(),
        two.files(),
        "the store folder is left, standing not registered"
    );
}

/// No store folder (lost right after capture, or before the store copy), or a
/// store folder that no longer recomputes: *not completed*, citing the A15. A
/// store folder is never deleted or repaired.
#[test]
fn sqx_registration_without_a_recomputing_store_is_not_completed() {
    // The A15 alone: lost after capture, before the attempt began.
    let s = Scratch::new();
    let one = s.put("sample", false, "One");
    let record = lose_registration(&s.persistent_owner(), one.revision(), 0);
    let relaunched = s.persistent_owner();
    assert!(relaunched.reconciliation()[0].contains("process lost before the registration was stored"), "{:?}", relaunched.reconciliation());
    let rows = ledger(&s);
    assert_eq!((rows.len(), &rows[0]["outcome"], &rows[0]["act"]["record_id"]), (1, &json!("not completed"), &json!(record)));
    // Lost before the store copy (G-2): no store folder either.
    let two = s.put("sample", false, "Two");
    let record = lose_registration(&s.persistent_owner(), two.revision(), LOSE_BEFORE_STORE);
    assert!(!store_of(&s, two.revision()).exists());
    s.persistent_owner();
    let rows = ledger(&s);
    assert_eq!(rows[1]["outcome"], "not completed");
    assert_eq!(rows[1]["act"]["record_id"], record.as_str());
    assert!(rows[1]["reason"].as_str().unwrap().starts_with("process lost before the registration was stored"));
    // Stored, then the store bytes changed before relaunch.
    let three = s.put("sample", false, "Three");
    let record = lose_registration(&s.persistent_owner(), three.revision(), LOSE_BEFORE_COMMIT);
    let store = store_of(&s, three.revision());
    fs::write(store.join("notes.txt"), b"tampered").unwrap();
    let relaunched = s.persistent_owner();
    assert!(relaunched.reconciliation()[0].contains("does not recompute"), "{:?}", relaunched.reconciliation());
    let rows = ledger(&s);
    assert_eq!(rows.len(), 3);
    assert_eq!(rows[2]["outcome"], "not completed");
    assert_eq!(rows[2]["act"]["record_id"], record.as_str());
    assert_eq!(fs::read(store.join("notes.txt")).unwrap(), b"tampered", "left as it is");
    assert!(read_ledger(&s.0).is_ok());
}

/// A line already citing the act: X-2 writes nothing (a durable G-4 whose sync
/// was uncertain, or an ordinary completed registration).
#[test]
fn sqx_line_already_present_writes_nothing() {
    let s = Scratch::new();
    let one = s.put("sample", false, "One");
    register(&s.persistent_owner(), one.revision());
    assert!(s.persistent_owner().reconciliation().is_empty());
    let two = s.put("sample", false, "Two");
    let owner = s.persistent_owner();
    let session = owner.review_draft("sample", two.revision()).unwrap();
    let r = receipt(&session);
    let record = r.record_id().to_string();
    let mut attempt = session.begin_hot_registration(r).unwrap();
    FAIL_LEDGER_SYNC.with(|fail| fail.set(true));
    assert!(matches!(&attempt.advance()[0], EntryOutcome::Pending { .. }));
    drop(attempt);
    drop(owner);
    let before = fs::read(s.0.join(".chirality/workflow-registry.jsonl")).unwrap();
    let relaunched = s.persistent_owner();
    assert!(relaunched.reconciliation().is_empty(), "{:?}", relaunched.reconciliation());
    assert_eq!(fs::read(s.0.join(".chirality/workflow-registry.jsonl")).unwrap(), before);
    let rows = ledger(&s);
    assert_eq!(rows.iter().filter(|v| v["act"]["record_id"] == record.as_str()).count(), 1);
}

/// WR-VC-20: re-confirmed lines add nothing to the slot's series and never change
/// its latest; a concurrent registration is not "slot moved on" (F14); RC-9's
/// reader checks name the breaking line.
#[test]
fn wr_vc_20_ledger_series_with_reconfirmation_lines() {
    let s = Scratch::new();
    let one = s.put("sample", false, "One");
    register(&s.persistent_owner(), one.revision());
    let two = s.put("sample", false, "Two");
    let second = register(&s.persistent_owner(), two.revision());
    // Re-confirm 2, then 1 twice (each in a fresh process).
    reconfirmed(&reconfirm(&s.persistent_owner(), two.revision()).0[0]);
    s.put("sample", false, "One");
    reconfirmed(&reconfirm(&s.persistent_owner(), one.revision()).0[0]);
    reconfirmed(&reconfirm(&s.persistent_owner(), one.revision()).0[0]);
    let rows = ledger(&s);
    assert_eq!(rows.len(), 5);
    let slot = slot_lines(&rows, "project", "fixture-project", "sample");
    assert_eq!(
        latest(&slot).unwrap().as_ref(),
        Some(second.identity()),
        "latest unchanged"
    );
    // F14: a DS-2 attempt captured before a re-confirmation commits still registers.
    let mover = s.owner();
    mover
        .bases
        .lock()
        .unwrap()
        .insert("sample".into(), second.identity().clone());
    let three = s.put("sample", false, "Three");
    let ds2 = mover.review_draft("sample", three.revision()).unwrap();
    let r3 = receipt(&ds2);
    s.put("sample", false, "One");
    reconfirmed(&reconfirm(&s.persistent_owner(), one.revision()).0[0]);
    // (The live draft changed after capture, which RB-6 allows; G-1 compares the
    // slot's latest registered revision only.)
    let mut a3 = ds2.begin_hot_registration(r3).unwrap();
    assert!(matches!(&a3.advance()[0], EntryOutcome::Registered { .. }));
    let rows = ledger(&s);
    assert_eq!(rows.last().unwrap()["sequence"], 3);
    // RC-9 reader checks.
    let path = s.0.join(".chirality/workflow-registry.jsonl");
    let good = fs::read_to_string(&path).unwrap();
    let lines: Vec<Value> = good
        .lines()
        .map(|l| serde_json::from_str(l).unwrap())
        .collect();
    let reline = lines
        .iter()
        .find(|v| v["outcome"] == "re-confirmed")
        .unwrap()
        .clone();
    let append = |edit: &dyn Fn(&mut Value)| {
        let mut v = reline.clone();
        v["ledger_seq"] = json!(lines.len() + 1);
        edit(&mut v);
        format!("{good}{}\n", serde_json::to_string(&v).unwrap())
    };
    let cases: Vec<(String, &str)> = vec![
        (append(&|_| {}), "is cited by another ledger line"),
        (
            append(&|v| {
                v["act"]["record_id"] = json!("rec:fresh");
                v["reconfirms"]["ledger_seq"] = json!(3);
            }),
            "which is not an earlier registered line",
        ),
        (
            append(&|v| {
                v["act"]["record_id"] = json!("rec:fresh");
                v["store_path"] = json!("elsewhere");
            }),
            "store_path differs from line",
        ),
    ];
    for (bytes, cause) in cases {
        fs::write(&path, &bytes).unwrap();
        let error = read_ledger(&s.0).err().unwrap();
        assert!(
            error.contains("registration ledger ambiguous") && error.contains(cause),
            "{cause}: {error}"
        );
    }
    fs::write(&path, &good).unwrap();
    assert!(read_ledger(&s.0).is_ok());
}

/// WR §4.6 RF-1: Refine an LS-1 revision from the revision store with no
/// selection, including one registered in place; the base is App-recorded,
/// shown and frozen at review; left unchanged the draft is DS-8.
#[test]
fn rf_1_refine_from_the_store_without_a_selection_including_in_place() {
    let s = Scratch::new();
    // Two entries: a single in-place a15_descriptor is refused by the adopted
    // AAC offer schema (pre-existing; CONTRACT_ISSUES CI-24 (e)).
    let entry = s.put("sample", true, "In place");
    s.put("other", true, "Other in place");
    let session = s
        .persistent_owner()
        .review_in_place(&["sample".into(), "other".into()])
        .unwrap();
    let r = receipt(&session);
    let mut attempt = session.begin_hot_registration(r).unwrap();
    assert!(matches!(
        &attempt.advance()[0],
        EntryOutcome::Registered { .. }
    ));
    // Relaunch: no selection exists in this process.
    let owner = s.persistent_owner();
    assert!(owner
        .refine_from_store("sample", "0".repeat(64).as_str())
        .is_err());
    let made = owner.refine_from_store("sample", entry.revision()).unwrap();
    assert_eq!(made["base"]["revision"], entry.revision());
    assert!(made["standing"]
        .as_str()
        .unwrap()
        .contains("not verified in this session"));
    let draft = s.0.join(".chirality/workflow-drafts/sample");
    assert_eq!(Snapshot::capture(&draft).unwrap().files(), entry.files());
    // D-1: never overwrites.
    let again = owner
        .refine_from_store("sample", entry.revision())
        .err()
        .unwrap();
    assert!(again.contains("already exists"), "{again}");
    // Shown and frozen at review: DS-8 with the App-recorded base.
    let review = owner.review_draft("sample", entry.revision()).unwrap();
    let view = review.current().unwrap();
    assert_eq!(view.descriptor()["disposition"], "re-confirmation");
    let shown = &view.review_presentation()["entries"][0];
    assert_eq!(shown["base"]["revision"], entry.revision());
    assert_eq!(
        shown["base_observation"]["observed"]["source"],
        "App data folder"
    );
    drop(view);
    let r = receipt(&review);
    let mut attempt = review.begin_hot_registration(r).unwrap();
    reconfirmed(&attempt.advance()[0]);
}

// ---- V15 F1 (MAJOR): the App never appends a line its own reader refuses, and
// one act never has two ledger lines (RC-7, RB-8). Based on the reviewer's
// probes P1, P2, P5 and P6 (`v15-probe-tests.rs.txt`), restated for SQ-X without
// a journal (owner ruling 2026-10-10).

/// P1 (restated): an uncited A15 that X-2 cannot close as a registration of
/// this library is reported with its cause and nothing is written; an act log
/// that cannot be read completely leaves X-1 not established.
#[test]
fn v15_p1_x2_writes_nothing_it_cannot_establish() {
    let s = Scratch::new();
    let one = s.put("sample", false, "One");
    register(&s.persistent_owner(), one.revision());
    let record = {
        let owner = s.persistent_owner();
        let session = owner.review_draft("sample", one.revision()).unwrap();
        let r = receipt(&session);
        let record = r.record_id().to_string();
        let mut attempt = session.begin_hot_registration(r).unwrap();
        LOSE_AT.with(|at| at.set(LOSE_BEFORE_COMMIT));
        let _ = attempt.advance();
        record
    };
    // The re-confirmation's ‹k› no longer matches any registered line.
    let log = storage::library_log(&s.0);
    let kept = fs::read_to_string(&log).unwrap();
    let mut lines: Vec<String> = kept.lines().map(str::to_owned).collect();
    let at = lines.iter().position(|l| l.contains(&record)).unwrap();
    lines[at] = lines[at].replace(one.revision(), &"a".repeat(64));
    fs::write(&log, lines.join("\n") + "\n").unwrap();
    let outcome = s.persistent_owner().reconciliation().join("; ");
    assert!(outcome.contains("X-2 pending") && outcome.contains("no registered line records"), "{outcome}");
    assert_eq!(ledger(&s).len(), 1, "nothing appended; the ledger still reads");
    // An act log that cannot be read completely: nothing is decided.
    fs::write(&log, kept.clone() + "{not json\n").unwrap();
    let outcome = s.persistent_owner().reconciliation().join("; ");
    assert!(outcome.contains("X-1 not established") && outcome.contains("act log"), "{outcome}");
    assert_eq!(ledger(&s).len(), 1);
    fs::write(&log, kept).unwrap();
    assert!(s.persistent_owner().reconciliation()[0].contains("not completed"));
}

/// P2 (restated): a live attempt in another App process is not closed as lost.
/// Process B's append fails before writing (its attempt is *Intended* and still
/// held); process C opens the library: X-2 is deferred and writes nothing. B's
/// Continue then commits its own line. The same holds for a live review whose
/// A15 is recorded but whose attempt has not begun.
#[test]
fn sqx_live_attempt_in_another_process_is_not_closed_as_lost() {
    let s = Scratch::new();
    let one = s.put("sample", false, "One");
    let owner_b = s.persistent_owner();
    // A review with its A15 recorded, the attempt not yet begun.
    let session = owner_b.review_draft("sample", one.revision()).unwrap();
    let r = receipt(&session);
    let record = r.record_id().to_string();
    let deferred = s.persistent_owner();
    assert!(deferred.reconciliation()[0].starts_with("X-2 deferred"), "{:?}", deferred.reconciliation());
    assert!(ledger(&s).is_empty());
    // The attempt begins and its append fails before writing anything.
    let mut attempt = session.begin_hot_registration(r).unwrap();
    FAIL_LEDGER_APPEND.with(|fail| fail.set(true));
    assert!(matches!(&attempt.advance()[0], EntryOutcome::Pending { .. }));
    let owner_c = s.persistent_owner();
    assert!(owner_c.reconciliation()[0].starts_with("X-2 deferred"), "{:?}", owner_c.reconciliation());
    assert!(ledger(&s).is_empty(), "the live attempt was not closed as lost");
    match &attempt.advance()[0] {
        EntryOutcome::Registered { .. } => {}
        other => panic!("expected B to commit its own line: {other:?}"),
    }
    let rows = ledger(&s);
    assert_eq!(rows.len(), 1);
    assert_eq!(rows[0]["act"]["record_id"], record.as_str());
    // Closed: the liveness lock is released and a later open has nothing to do.
    assert!(s.persistent_owner().reconciliation().is_empty());
    assert!(storage::try_lock_exclusive(&liveness_path(&s.0)).unwrap().is_some());
}

/// P6 (V15-R1 R1-1), kept as the defence behind the liveness lock: if B's
/// liveness were lost while its attempt is *Intended* (its append wrote
/// nothing), C's X-2 closes the attempt with a *not completed* line citing B's
/// A15, and B's Continue ends with that line, a definite outcome. One act, one
/// ledger line. The same for a registration C completed: B finishes with it.
#[test]
fn v15_r1_p6_intended_attempt_ends_with_the_other_process_x2_line() {
    let s = Scratch::new();
    let one = s.put("sample", false, "One");
    let first = register(&s.persistent_owner(), one.revision());
    let owner_b = s.persistent_owner();
    let session = owner_b.review_draft("sample", one.revision()).unwrap();
    let r = receipt(&session);
    let record = r.record_id().to_string();
    let mut attempt = session.begin_hot_registration(r).unwrap();
    FAIL_LEDGER_APPEND.with(|fail| fail.set(true));
    match &attempt.advance()[0] {
        EntryOutcome::Pending { reason, .. } => {
            assert!(reason.contains("durability uncertain"), "{reason}")
        }
        other => panic!("expected pending: {other:?}"),
    }
    assert_eq!(ledger(&s).len(), 1, "the failed append wrote nothing");
    attempt.session.live = None; // liveness lost (defence test only)
    let owner_c = s.persistent_owner();
    assert!(
        owner_c.reconciliation()[0].contains("not completed"),
        "{:?}",
        owner_c.reconciliation()
    );
    assert_eq!(ledger(&s).len(), 2, "X-2 wrote its not completed line");
    for _ in 0..2 {
        match &attempt.advance()[0] {
            EntryOutcome::NotCompleted { reason, .. } => assert!(
                reason.contains(&format!("A15 {record} already has ledger line 2 (not completed)")),
                "{reason}"
            ),
            other => panic!("expected the definite line, not uncertainty: {other:?}"),
        }
    }
    let raw = fs::read_to_string(s.0.join(".chirality/workflow-registry.jsonl")).unwrap();
    assert_eq!(
        raw.lines().filter(|l| l.contains(&record)).count(),
        1,
        "one act, one line"
    );
    assert!(read_ledger(&s.0).is_ok());
    assert!(!owner_b.is_held(first.identity()));
    // A registration whose liveness is lost after its store copy: C completes
    // it citing B's A15; B's Continue finishes with that line, appending none.
    let two = s.put("sample", false, "Two");
    let owner_b = s.persistent_owner();
    let session = owner_b.review_draft("sample", two.revision()).unwrap();
    let r = receipt(&session);
    let record = r.record_id().to_string();
    let mut attempt = session.begin_hot_registration(r).unwrap();
    LOSE_AT.with(|at| at.set(LOSE_BEFORE_COMMIT));
    assert!(matches!(&attempt.advance()[0], EntryOutcome::Pending { .. }));
    attempt.session.live = None;
    assert!(s.persistent_owner().reconciliation()[0].contains("completed at relaunch"));
    assert!(matches!(&attempt.advance()[0], EntryOutcome::Registered { .. }));
    let raw = fs::read_to_string(s.0.join(".chirality/workflow-registry.jsonl")).unwrap();
    assert_eq!(raw.lines().filter(|l| l.contains(&record)).count(), 1, "one act, one line");
}

/// P5: after capture, registered line 1 is edited outside the App so it no
/// longer reads as registered. WR G-1R says *not completed*, but no such line
/// can satisfy RC-9 here (CI-25): the App appends nothing and the attempt stays
/// pending with the exact cause; the ledger stays readable.
#[test]
fn v15_p5_g1r_line_no_longer_registered_appends_nothing() {
    let s = Scratch::new();
    let one = s.put("sample", false, "One");
    register(&s.persistent_owner(), one.revision());
    let owner = s.persistent_owner();
    let session = owner.review_draft("sample", one.revision()).unwrap();
    let r = receipt(&session);
    let path = s.0.join(".chirality/workflow-registry.jsonl");
    let mut line: Value =
        serde_json::from_str(fs::read_to_string(&path).unwrap().lines().next().unwrap()).unwrap();
    line["outcome"] = json!("not completed");
    line["reason"] = json!("edited outside the App");
    fs::write(
        &path,
        format!("{}\n", serde_json::to_string(&line).unwrap()),
    )
    .unwrap();
    let mut attempt = session.begin_hot_registration(r).unwrap();
    match &attempt.advance()[0] {
        EntryOutcome::Pending { reason, .. } => {
            assert!(
                reason.contains("RC-9") && reason.contains("not appended"),
                "{reason}"
            )
        }
        other => panic!("expected pending: {other:?}"),
    }
    assert_eq!(
        read_ledger(&s.0).unwrap().len(),
        1,
        "nothing appended; readable"
    );
}

// ---- V15 F2–F5: branches the reviewer's mutations MA–ME showed untested.

/// F2 (MC; P4): RC-5 (d) in current(): once ‹k› becomes selectable in this
/// process, a second DS-8 review of it is withdrawn.
#[test]
fn v15_f2_rc5d_second_review_withdrawn_once_k_selectable() {
    let s = Scratch::new();
    let one = s.put("sample", false, "One");
    register(&s.persistent_owner(), one.revision());
    let owner = s.persistent_owner();
    let a = owner.review_draft("sample", one.revision()).unwrap();
    let b = owner.review_draft("sample", one.revision()).unwrap();
    let ra = receipt(&a);
    let mut attempt = a.begin_hot_registration(ra).unwrap();
    reconfirmed(&attempt.advance()[0]);
    let stale = b.current().err().unwrap();
    assert!(
        stale.contains("already selectable in this App session"),
        "{stale}"
    );
}

/// F2 (MD): LS-4 "bound to other content": the line's A15 record is found but
/// binds another content identity, so DS-4 with that cause, never DS-8.
#[test]
fn v15_f2_ls4_record_bound_to_other_content_is_ds4() {
    let s = Scratch::new();
    let one = s.put("sample", false, "One");
    let first = register(&s.persistent_owner(), one.revision());
    let log = storage::library_log(&s.0);
    let text = fs::read_to_string(&log).unwrap();
    let edited: String = text
        .lines()
        .map(|l| {
            let mut v: Value = serde_json::from_str(l).unwrap();
            if v["recordId"] == first.act_ref() {
                v["body"]["boundContent"][0]["value"] = json!("f".repeat(64));
            }
            format!("{}\n", serde_json::to_string(&v).unwrap())
        })
        .collect();
    fs::write(&log, edited).unwrap();
    assert!(
        crate::records::read_log(&log).1.is_empty(),
        "the log still reads"
    );
    let error = s
        .persistent_owner()
        .review_draft("sample", one.revision())
        .err()
        .unwrap();
    assert!(
        error.starts_with("DS-4") && error.contains("bound to other content"),
        "{error}"
    );
}

/// F2 (MB, ME): RC-9 reader negatives not covered by WR-VC-20: same slot, tuple
/// and sequence of `reconfirms`; the *re-confirmed* line's identity and prior;
/// reviewed content; and a `reconfirms` naming a *not completed* or later line.
#[test]
fn v15_f2_rc9_reader_names_each_breach() {
    let s = Scratch::new();
    let one = s.put("sample", false, "One");
    register(&s.persistent_owner(), one.revision());
    reconfirmed(&reconfirm(&s.persistent_owner(), one.revision()).0[0]);
    let path = s.0.join(".chirality/workflow-registry.jsonl");
    let good = fs::read_to_string(&path).unwrap();
    let rows: Vec<Value> = good
        .lines()
        .map(|l| serde_json::from_str(l).unwrap())
        .collect();
    assert_eq!(rows.len(), 2);
    let reline = rows[1].clone();
    // A valid *not completed* re-confirmation line, as line 3.
    let mut not_completed = reline.clone();
    {
        let f = not_completed.as_object_mut().unwrap();
        f.remove("sequence");
        f.remove("store_path");
    }
    not_completed["outcome"] = json!("not completed");
    not_completed["reason"] = json!("fixture");
    not_completed["ledger_seq"] = json!(3);
    not_completed["act"]["record_id"] = json!("rec:fixture:nc");
    let base = format!("{good}{}\n", serde_json::to_string(&not_completed).unwrap());
    assert!(
        {
            fs::write(&path, &base).unwrap();
            read_ledger(&s.0).is_ok()
        },
        "the valid fixture line reads"
    );
    let with = |edit: &dyn Fn(&mut Value)| {
        let mut v = reline.clone();
        v["ledger_seq"] = json!(4);
        v["act"]["record_id"] = json!("rec:fixture:new");
        edit(&mut v);
        format!("{base}{}\n", serde_json::to_string(&v).unwrap())
    };
    let other = |v: &mut Value, field: &str, value: Value| {
        v["reconfirms"][field] = value;
    };
    let cases: Vec<(String, &str)> = vec![
        (
            with(&|v| other(v, "sequence", json!(2))),
            "with another slot, tuple or sequence",
        ),
        (
            with(&|v| {
                let mut id = v["reconfirms"]["identity"].clone();
                id["revision"] = json!("e".repeat(64));
                other(v, "identity", id);
            }),
            "with another slot, tuple or sequence",
        ),
        (
            with(&|v| v["identity"]["name"] = json!("elsewhere")),
            "with another slot, tuple or sequence",
        ),
        (
            with(&|v| v["identity"]["derived_from"] = v["identity"].clone()),
            "identity differs from line 1",
        ),
        (
            with(&|v| v["prior_revision"] = v["identity"].clone()),
            "prior_revision differs from line 1",
        ),
        (
            with(&|v| v["reviewed_draft"]["content"]["value"] = json!("d".repeat(64))),
            "reviewed content is not the re-confirmed revision",
        ),
        (
            with(&|v| other(v, "ledger_seq", json!(3))),
            "re-confirms line 3, which is not an earlier registered line",
        ),
        (
            with(&|v| other(v, "ledger_seq", json!(4))),
            "re-confirms line 4, which is not an earlier registered line",
        ),
    ];
    for (bytes, cause) in cases {
        fs::write(&path, &bytes).unwrap();
        let error = read_ledger(&s.0).err().unwrap_or_default();
        assert!(
            error.contains("registration ledger ambiguous") && error.contains(cause),
            "{cause}: {error}"
        );
    }
}

/// F2 (WR G-1R "line changed"): the registered line still reads as registered
/// for ‹k› but no longer as reviewed. The *not completed* line satisfies RC-9,
/// so it is written; the ledger stays readable.
#[test]
fn v15_f2_g1r_registered_line_changed_is_not_completed() {
    let s = Scratch::new();
    let one = s.put("sample", false, "One");
    register(&s.persistent_owner(), one.revision());
    let owner = s.persistent_owner();
    let session = owner.review_draft("sample", one.revision()).unwrap();
    let r = receipt(&session);
    let path = s.0.join(".chirality/workflow-registry.jsonl");
    let mut line: Value =
        serde_json::from_str(fs::read_to_string(&path).unwrap().lines().next().unwrap()).unwrap();
    line["written_at"] = json!("2026-10-08T00:00:00Z");
    fs::write(
        &path,
        format!("{}\n", serde_json::to_string(&line).unwrap()),
    )
    .unwrap();
    let mut attempt = session.begin_hot_registration(r).unwrap();
    match &attempt.advance()[0] {
        EntryOutcome::NotCompleted { reason, .. } => {
            assert!(
                reason.contains("registered line 1 no longer reads as reviewed"),
                "{reason}"
            )
        }
        other => panic!("expected no effect: {other:?}"),
    }
    let rows = read_ledger(&s.0).unwrap();
    assert_eq!(rows.len(), 2);
    assert_eq!(rows[1]["disposition"], "re-confirmation");
}

/// F3 (MA): RF-1 leaves no draft without its App-kept base: on a failure to
/// record the base, and on a sync failure after the copy, the copy is removed.
#[test]
fn v15_f3_rf1_removes_its_copy_on_every_failure() {
    struct ResetSync;
    impl Drop for ResetSync {
        fn drop(&mut self) {
            storage::fail_directory_for_test(None);
        }
    }
    let s = Scratch::new();
    let one = s.put("sample", false, "One");
    register(&s.persistent_owner(), one.revision());
    let draft = s.0.join(".chirality/workflow-drafts/sample");
    fs::remove_dir_all(&draft).unwrap();
    // (a) The App-kept base cannot be written.
    let base_files = s.base_files();
    for f in &base_files {
        fs::remove_file(f).unwrap();
    }
    let blocker = s.app_data().join("runtime/wr");
    fs::remove_dir_all(&blocker).unwrap();
    fs::write(&blocker, b"not a directory").unwrap();
    let error = s
        .persistent_owner()
        .refine_from_store("sample", one.revision())
        .err()
        .unwrap();
    assert!(
        error.contains("App-kept base not recorded") && error.contains("copy was removed"),
        "{error}"
    );
    assert!(!draft.exists());
    fs::remove_file(&blocker).unwrap();
    // (b) The copy's directory sync fails after the copy was written.
    storage::fail_directory_for_test(Some(draft.clone()));
    let _reset = ResetSync;
    let error = s
        .persistent_owner()
        .refine_from_store("sample", one.revision())
        .err()
        .unwrap();
    storage::fail_directory_for_test(None);
    assert!(
        error.contains("injected failure") && error.contains("copy was removed"),
        "{error}"
    );
    assert!(!draft.exists());
    assert!(s.base_files().is_empty(), "no base recorded");
    // Then Refine works.
    s.persistent_owner()
        .refine_from_store("sample", one.revision())
        .unwrap();
    assert!(draft.join("WORKFLOW.md").is_file());
    assert_eq!(s.base_files().len(), 1);
}

/// F4: an act log that cannot be read completely keeps a captured
/// re-confirmation pending at G-1R (the act is not spent); once readable, the
/// same attempt completes.
#[test]
fn v15_f4_unreadable_act_log_keeps_g1r_pending() {
    let s = Scratch::new();
    let one = s.put("sample", false, "One");
    let first = register(&s.persistent_owner(), one.revision());
    let owner = s.persistent_owner();
    let session = owner.review_draft("sample", one.revision()).unwrap();
    let r = receipt(&session);
    let log = storage::library_log(&s.0);
    let kept = fs::read(&log).unwrap();
    let mut broken = kept.clone();
    broken.extend_from_slice(b"{\"not\":\"an act record\"}\n");
    fs::write(&log, &broken).unwrap();
    let mut attempt = session.begin_hot_registration(r).unwrap();
    match &attempt.advance()[0] {
        EntryOutcome::Pending { reason, .. } => {
            assert!(
                reason.contains("act log not completely readable"),
                "{reason}"
            )
        }
        other => panic!("expected pending: {other:?}"),
    }
    assert_eq!(ledger(&s).len(), 1, "nothing appended");
    fs::write(&log, &kept).unwrap();
    assert_eq!(
        reconfirmed(&attempt.advance()[0]).identity(),
        first.identity()
    );
}

/// F5: the library lists its registered revisions with WR's label; a row is
/// "selectable in this App session" only after this process's own commit.
#[test]
fn v15_f5_registered_listing_labels_rows() {
    let s = Scratch::new();
    let one = s.put("sample", false, "One");
    register(&s.persistent_owner(), one.revision());
    let owner = s.persistent_owner();
    let rows = owner.registered_listing();
    assert_eq!(rows.as_array().unwrap().len(), 1, "{rows}");
    assert_eq!(rows[0]["revision"], one.revision());
    assert_eq!(rows[0]["sequence"], 1);
    assert_eq!(
        rows[0]["label"],
        "registered — re-confirm to use in this App session"
    );
    reconfirmed(&reconfirm(&owner, one.revision()).0[0]);
    let rows = owner.registered_listing();
    assert_eq!(
        rows.as_array().unwrap().len(),
        1,
        "a re-confirmed line is not a revision"
    );
    assert_eq!(
        rows[0]["label"],
        "registered — selectable in this App session"
    );
}
