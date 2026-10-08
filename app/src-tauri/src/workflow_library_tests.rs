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
    // Identical content after relaunch stays DS-4 (WR SP-4); its remedy needs SEAL-2 (CI-21).
    let identical = s.persistent_owner().review_draft("sample", two.revision());
    assert!(
        identical.as_ref().is_err_and(|e| e.starts_with("DS-4")),
        "{:?}",
        identical.err()
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
