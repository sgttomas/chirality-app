// Intentionally red trace witnesses. The Records Type 1 chooses the repair.
use super::*;

struct Project(PathBuf);
impl Project {
    fn new() -> Self { Self(folder("records-routing-project-")) }
    fn in_place(&self) -> String {
        let entry = records::append(
            &self.0.join(".chirality/records/acts/in-place.jsonl"),
            "evidence_limit", &APP_WRITER, body("in-place record must remain visible"),
        ).unwrap();
        entry["recordId"].as_str().unwrap().to_owned()
    }
}
impl Drop for Project {
    fn drop(&mut self) { let _ = std::fs::remove_dir_all(&self.0); }
}

// Exact current create_control_in name/bytes at the interruption boundary
// after creating its random empty capture-lock temporary, before rename.
// There is no existing prepublication hook for UNSTAGED empty controls
// (FAIL_CONTROL_BEFORE_PUBLISH only runs when staging.is_some()).
fn capture_lock_temporary(dir: &Path) -> PathBuf {
    let captures = dir.join("captures");
    storage::ensure_directory(&captures).unwrap();
    let temp = captures.join(format!("..capture.lock.{}.tmp", crate::util::opaque_id("").unwrap()));
    std::fs::OpenOptions::new().create_new(true).write(true).open(&temp).unwrap().sync_all().unwrap();
    temp
}

#[test]
fn records_store_routing_capture_lock_temporary_keeps_in_place_record_visible() {
    let _store = OwnStore::new();
    let project = Project::new();
    let id = project.in_place();
    let dir = attach(&project.0, true).unwrap().dir.unwrap();
    assert!(storage::read_all(&project.0).0.iter().any(|r| r["recordId"] == id));
    let temp = capture_lock_temporary(&dir);
    let (read, limits) = storage::read_all(&project.0);
    assert!(read.iter().any(|r| r["recordId"] == id),
        "capture-lock temporary {} hid existing in-place record {id}; read={read:?}, limits={limits:?}", temp.display());
}

#[test]
fn records_store_routing_capture_lock_temporary_status_still_requires_import() {
    let _store = OwnStore::new();
    let project = Project::new();
    project.in_place();
    let dir = attach(&project.0, true).unwrap().dir.unwrap();
    assert_eq!(status(Some(&project.0))["project"]["importNeeded"], true);
    capture_lock_temporary(&dir);
    let observed = status(Some(&project.0));
    assert_eq!(observed["project"]["importNeeded"], true,
        "a temporary cannot settle the import or change the reading: {}", observed["project"]);
}

#[test]
fn records_store_routing_capture_lock_temporary_cannot_export_instead_of_in_place_history() {
    let _store = OwnStore::new();
    let project = Project::new();
    project.in_place();
    let dir = attach(&project.0, true).unwrap().dir.unwrap();
    let output = Project::new();
    let destination = output.0.join("bag");
    assert!(crate::records_export::export(&project.0, &destination).is_err());
    capture_lock_temporary(&dir);
    let result = crate::records_export::export(&project.0, &destination);
    assert!(result.is_err(), "temporary allowed an export omitting the in-place history: {result:?}");
}

#[test]
fn records_store_routing_failed_payload_preparation_folders_do_not_hide_in_place_records() {
    let _store = OwnStore::new();
    let mut wrong = vec![];
    // Both helpers can leave a newly made folder after ensure_directory's
    // sync fails. No temporary or final member has even been opened yet.
    for name in ["runs", "acts", "workflow", "legacy", "connectors", "captures/pending"] {
        let project = Project::new();
        let id = project.in_place();
        let dir = attach(&project.0, true).unwrap().dir.unwrap();
        let parent = dir.join(name);
        storage::fail_directory_for_test(Some(parent.clone()));
        let failed = if name == "legacy" {
            storage::create_bytes(&parent.join("record.jsonl"), b"invented copy\n")
        } else {
            storage::create_json(&parent.join("record.json"), &json!({"invented":"payload"}))
        };
        storage::fail_directory_for_test(None);
        assert!(failed.as_ref().is_err_and(|e| e.contains("injected failure")), "{failed:?}");
        assert_eq!(std::fs::read_dir(&parent).unwrap().count(), 0);
        let (read, limits) = storage::read_all(&project.0);
        if !read.iter().any(|r| r["recordId"] == id) {
            wrong.push(format!("{name}: {failed:?}; read={read:?}; limits={limits:?}; status={}", status(Some(&project.0))["project"]));
        }
    }
    assert!(wrong.is_empty(), "failed preparations hid in-place records:\n{}", wrong.join("\n"));
}

#[test]
fn records_store_routing_package_inventory_excludes_own_temporary_but_keeps_connector_evidence() {
    let _store = OwnStore::new();
    let project = Project::new();
    let dir = attach(&project.0, true).unwrap().dir.unwrap();
    let temp = capture_lock_temporary(&dir);
    storage::ensure_directory(&dir.join("connectors")).unwrap();
    let connector = format!("connectors/.route-{}.tmp", crate::util::opaque_id("").unwrap());
    std::fs::write(dir.join(&connector), b"retained connector attempt evidence").unwrap();
    let inventory = crate::records_package::payload_inventory(&dir).unwrap();
    assert!(inventory.contains_key(&connector), "connector leftovers must stay evidence");
    let rel = temp.strip_prefix(&dir).unwrap().to_str().unwrap();
    assert!(!inventory.contains_key(rel), "unpublished owning-control temporary inventoried as record: {rel}; members={inventory:?}");
}

#[test]
fn records_store_routing_export_excludes_own_temporary_but_keeps_connector_evidence() {
    let _store = OwnStore::new();
    let project = Project::new();
    records::append_project(&project.0, Some("run:routing"), "app-writer:local", "evidence_limit", &APP_WRITER, body("real store record")).unwrap();
    let dir = attach(&project.0, false).unwrap().dir.unwrap();
    let temp = capture_lock_temporary(&dir);
    storage::ensure_directory(&dir.join("connectors")).unwrap();
    let connector = format!("connectors/.route-{}.tmp", crate::util::opaque_id("").unwrap());
    std::fs::write(dir.join(&connector), b"retained connector attempt evidence").unwrap();
    let output = Project::new();
    let destination = output.0.join("bag");
    let result = crate::records_export::export(&project.0, &destination).unwrap();
    assert!(crate::records_export::verify(&destination).is_ok());
    assert_eq!(std::fs::read(destination.join("data").join(&connector)).unwrap(), b"retained connector attempt evidence");
    let rel = temp.strip_prefix(&dir).unwrap();
    assert!(!destination.join("data").join(rel).exists(), "App lock temporary travelled in a successful export: {}; result={result}", rel.display());
}

#[test]
fn records_store_routing_export_does_not_carry_json_temporary_left_by_interrupted_publisher() {
    let _store = OwnStore::new();
    let project = Project::new();
    records::append_project(&project.0, Some("run:routing"), "app-writer:local", "evidence_limit", &APP_WRITER, body("real store record")).unwrap();
    let dir = attach(&project.0, false).unwrap().dir.unwrap();
    let capture = dir.join("captures").join(format!("{}.json", storage::key("invented capture")));
    storage::after_create_link_for_test(Some(Box::new(|_| panic!("interrupted after create-once link, before sync/cleanup"))));
    let interrupted = std::panic::catch_unwind(|| storage::create_json(&capture, &json!({"captureId":"invented capture"})));
    storage::after_create_link_for_test(None);
    assert!(interrupted.is_err(), "existing hook must interrupt the real publisher");
    let temp = std::fs::read_dir(capture.parent().unwrap()).unwrap().map(|e| e.unwrap().path()).find(|p| p.extension().is_some_and(|e| e == "tmp")).unwrap();
    let output = Project::new();
    let destination = output.0.join("bag");
    let result = crate::records_export::export(&project.0, &destination);
    assert!(result.is_err() || !destination.join("data").join(temp.strip_prefix(&dir).unwrap()).exists(),
        "real publisher's interrupted JSON temporary travelled in export: {result:?}");
}

#[test]
fn records_store_routing_package_inventory_does_not_promote_unpublished_payload_temporaries() {
    let _store = OwnStore::new();
    let project = Project::new();
    let dir = attach(&project.0, true).unwrap().dir.unwrap();
    // Pre-link write interruption fixtures; existing hooks cannot stop these
    // helpers between temporary open and hard-link publication.
    let mut names = vec![];
    for final_name in [".writer.lock", "workflow/11111111-1111-4111-8111-111111111111.json", "legacy/coordination.rs.jsonl", "captures/pending/aaaaaaaa.json"] {
        let final_path = dir.join(final_name);
        let parent = final_path.parent().unwrap();
        storage::ensure_directory(parent).unwrap();
        let temp = parent.join(format!(".{}.{}.tmp", final_path.file_name().unwrap().to_str().unwrap(), crate::util::opaque_id("").unwrap()));
        std::fs::write(&temp, if final_name == ".writer.lock" { &b""[..] } else { &b"{\"partial"[..] }).unwrap();
        names.push(temp.strip_prefix(&dir).unwrap().to_str().unwrap().to_owned());
    }
    let inventory = crate::records_package::payload_inventory(&dir);
    if let Ok(members) = &inventory {
        let carried: Vec<_> = names.iter().filter(|name| members.contains_key(*name)).collect();
        assert!(carried.is_empty(), "unpublished control/JSON/copy temporaries became package members: {carried:?}");
    }
}

#[test]
fn records_store_sync_failed_identity_publication_is_not_successful_startup_creation() {
    let project = Project::new();
    let root = folder("records-sync-store-");
    let _cleanup = Project(root.clone());
    use_store_not_started_for_test(Some(Ok(Store { root: root.clone(), placement: Placement::Override, limits: vec![] })));
    // The root already exists, so this fault hits publication, not mkdir.
    storage::fail_directory_for_test(Some(root.clone()));
    let result = create_at_startup();
    storage::fail_directory_for_test(None);
    let observed = status(None);
    let readable = crate::records_retention::read_plain(&root.join("store.json"));
    use_store_for_test(None);
    drop(project);
    assert!(readable.is_ok(), "published identity must be retained");
    assert!(result.is_err(), "store.json publication sync failed, but startup reported success: {result:?}; subsequent status={observed}");
}

#[test]
fn records_store_sync_failed_legacy_copy_is_not_imported_on_unsynced_readback() {
    let _store = OwnStore::new();
    let project = Project::new();
    project.in_place();
    let dir = attach(&project.0, true).unwrap().dir.unwrap();
    let target_parent = dir.join("acts");
    storage::ensure_directory(&target_parent).unwrap();
    storage::fail_directory_for_test(Some(target_parent));
    let first = import(&project.0);
    let retry = import(&project.0);
    storage::fail_directory_for_test(None);
    assert!(first.as_ref().is_err_and(|e| e.contains("injected failure")), "first publication must hit the sync fault: {first:?}");
    assert!(retry.is_err(), "same directory still cannot sync, but equal readable bytes were reported imported: first={first:?}; retry={retry:?}");
}
