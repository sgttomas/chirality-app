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
