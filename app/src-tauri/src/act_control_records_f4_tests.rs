#[test]
fn records_store_writer_binding_f4_act_refuses_before_capture_and_reports_cause() {
    let root = scratch();
    let (mut control, id, actor) = prepared(&root);
    let dir = crate::records_store::attach(&root, false)
        .unwrap()
        .dir
        .unwrap();
    let log = storage::project_file(&root, LOG).unwrap();
    let before = std::fs::read(&log).unwrap();
    let registry = crate::records_store::store_root()
        .unwrap()
        .join("roots.jsonl");
    std::fs::write(&registry, b"").unwrap();
    let reason = crate::records_store::attach(&root, false)
        .unwrap()
        .refusal
        .unwrap();
    let error = control
        .confirm(&id, "ALT-2", InputSource::HostNativeConfirmation, actor)
        .unwrap_err();
    assert!(error.contains(&reason), "{error}");
    assert!(
        control.native_captures.is_empty(),
        "no capture or pending act admitted"
    );
    assert!(!dir.join("captures").exists());
    assert_eq!(std::fs::read(&log).unwrap(), before);
    assert_eq!(std::fs::read(&registry).unwrap(), b"");
    std::fs::remove_dir_all(root).unwrap();
}

#[test]
fn a16_records_that_cannot_be_read_are_reported_with_their_cause_and_the_offer_stays_presented() {
    // Permitted case: with the store attached, the decision records.
    let root = scratch();
    let (mut control, id, actor) = prepared(&root);
    crate::records_store::attach(&root, false).unwrap().dir.unwrap();
    let recorded = control
        .confirm(&id, "ALT-2", InputSource::HostNativeConfirmation, actor)
        .unwrap();
    assert_eq!(recorded["state"], "AC-7 recorded");
    std::fs::remove_dir_all(root).unwrap();
    // Spoiled through the real path: the store's registry emptied, so the records cannot
    // be read. The cause is the store's own, not a changed standing; nothing is captured;
    // the offer stays presented, and once the registry is back the same decision records.
    let root = scratch();
    let (mut control, id, actor) = prepared(&root);
    let dir = crate::records_store::attach(&root, false).unwrap().dir.unwrap();
    let registry = crate::records_store::store_root().unwrap().join("roots.jsonl");
    let kept = std::fs::read(&registry).unwrap();
    std::fs::write(&registry, b"").unwrap();
    let reason = crate::records_store::attach(&root, false).unwrap().refusal.unwrap();
    let error = control
        .confirm(&id, "ALT-2", InputSource::HostNativeConfirmation, actor.clone())
        .unwrap_err();
    assert!(error.contains(&reason), "{error}");
    assert!(!error.contains(package_standing::CHANGED), "{error}");
    assert!(control.native_captures.is_empty());
    assert!(!dir.join("captures").exists());
    assert!(matches!(control.offers[&id].state, OfferState::Presented));
    std::fs::write(&registry, kept).unwrap();
    let recorded = control
        .confirm(&id, "ALT-2", InputSource::HostNativeConfirmation, actor)
        .unwrap();
    assert_eq!(recorded["state"], "AC-7 recorded");
    std::fs::remove_dir_all(root).unwrap();
}
