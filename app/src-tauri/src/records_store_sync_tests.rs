// Publication durability regressions.
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

#[test]
fn records_store_sync_legacy_retry_reestablishes_durability_with_the_same_import_identity() {
    let _store = OwnStore::new();
    let project = Project::new();
    project.in_place();
    let dir = attach(&project.0, true).unwrap().dir.unwrap();
    storage::ensure_directory(&dir.join("acts")).unwrap();
    storage::fail_directory_for_test(Some(dir.join("acts")));
    let first = import(&project.0).unwrap_err();
    let account = read_lines(&dir.join("imports.jsonl")).unwrap();
    let id = account[0]["importId"].clone();
    let copy = dir.join(account[0]["census"][0]["copy"].as_str().unwrap());
    let bytes = std::fs::read(&copy).unwrap();
    let retry = import(&project.0).unwrap_err();
    storage::fail_directory_for_test(None);
    assert!(first.contains(id.as_str().unwrap()), "{first}");
    assert!(retry.contains(id.as_str().unwrap()), "{retry}");
    assert_eq!(read_lines(&dir.join("imports.jsonl")).unwrap(), account, "uncertain retry writes no completion or new identity");
    let resumed = import(&project.0).unwrap();
    assert_eq!(resumed["state"], "imported");
    assert_eq!(resumed["importId"], id);
    assert_eq!(resumed["alreadyPresent"], 1);
    assert_eq!(resumed["copied"], 0);
    assert_eq!(std::fs::read(copy).unwrap(), bytes);
    let account = read_lines(&dir.join("imports.jsonl")).unwrap();
    assert_eq!(account.len(), 2);
    assert_eq!(account[1]["event"], "completed");
    assert_eq!(account[1]["importId"], id);
    // Even the completed/no-new-input branch re-establishes copy durability.
    storage::fail_directory_for_test(Some(dir.join("acts")));
    let repeated = import(&project.0);
    storage::fail_directory_for_test(None);
    assert!(repeated.is_err(), "{repeated:?}");
    assert_eq!(import(&project.0).unwrap()["state"], "imported");
}
