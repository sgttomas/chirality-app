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
