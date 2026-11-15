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


fn completion_sync_retry(stage: storage::PublicationSyncStage) {
    let own = OwnStore::new();
    let project = Project::new();
    project.in_place();
    let dir = attach(&project.0, true).unwrap().dir.unwrap();
    interrupt_import_for_test(Some(0), false);
    let seeded = import(&project.0);
    interrupt_import_for_test(None, false);
    assert!(seeded.as_ref().is_err_and(|e| e.contains("interrupted")), "{seeded:?}");
    let account = dir.join("imports.jsonl");
    let prefix = std::fs::metadata(&account).unwrap().len();
    let witness_path = own.0.join(witness::WITNESS_FILE);
    let witness_bytes = std::fs::read(&witness_path).unwrap();
    let before = read_lines(&account).unwrap();
    let retained_id = before[0]["importId"].clone();
    storage::fail_publication_sync_after_for_test(Some((account.clone(), prefix, stage)));
    let first = import(&project.0);
    let retained_bytes = std::fs::read(&account).unwrap();
    let lines = read_lines(&account).unwrap();
    let retry = import(&project.0);
    // The same fault remains installed through the unchanged retry.
    storage::fail_publication_sync_after_for_test(None);
    assert!(first.as_ref().is_err_and(|e| e.contains("publication sync: injected failure")), "completion must reach its {stage:?} fault: {first:?}");
    assert_eq!(lines.len(), 2);
    assert_eq!(lines[1]["event"], "completed");
    assert_eq!(lines[1]["importId"], retained_id);
    assert!(retry.is_err(), "readable completion bypassed its continuing {stage:?} sync fault: first={first:?}; retry={retry:?}");
    assert_eq!(std::fs::read(&account).unwrap(), retained_bytes);
    assert_eq!(std::fs::read(&witness_path).unwrap(), witness_bytes);
    let settled = import(&project.0).unwrap();
    assert_eq!(settled["state"], "imported");
    assert_eq!(std::fs::read(account).unwrap(), retained_bytes, "no replacement completion");
    assert_eq!(std::fs::read(witness_path).unwrap(), witness_bytes, "no replacement witness");
}

#[test]
fn records_store_sync_completion_retry_does_not_bypass_continuing_account_file_sync_failure() {
    completion_sync_retry(storage::PublicationSyncStage::File);
}

#[test]
fn records_store_sync_completion_retry_does_not_bypass_continuing_late_account_directory_sync_failure() {
    completion_sync_retry(storage::PublicationSyncStage::Directory);
}

fn uncertain_witness(project: &Project, own: &OwnStore) -> (PathBuf, Vec<u8>, Value) {
    let dir = attach(&project.0, true).unwrap().dir.unwrap();
    interrupt_append_after_for_test(0, Some(AppendStop::BeforeSync));
    let first = import(&project.0);
    interrupt_append_for_test(None);
    assert!(first.as_ref().is_err_and(|e| e.contains("before the sync")), "{first:?}");
    assert!(std::fs::symlink_metadata(dir.join("imports.jsonl")).is_err(), "no started line exists yet");
    let path = own.0.join(witness::WITNESS_FILE);
    let bytes = std::fs::read(&path).unwrap();
    let project_id = attach(&project.0, false).unwrap().project.unwrap();
    let line = read_lines(&path).unwrap().into_iter().find(|v| v["projectId"] == project_id && v["importId"].is_string()).unwrap();
    (path, bytes, line)
}

#[test]
fn records_store_sync_uncertain_witness_retry_keeps_one_import_identity() {
    let own = OwnStore::new();
    let project = Project::new();
    project.in_place();
    let (path, bytes, retained) = uncertain_witness(&project, &own);
    let resumed = import(&project.0).unwrap();
    assert_eq!(resumed["importId"], retained["importId"], "uncertain witness is the same import");
    assert_eq!(std::fs::read(path).unwrap(), bytes, "no second witness append for a retry");
}

#[test]
fn records_store_sync_uncertain_witness_continuing_failure_names_the_same_attempt() {
    let own = OwnStore::new();
    let project = Project::new();
    project.in_place();
    let (path, bytes, retained) = uncertain_witness(&project, &own);
    storage::fail_publication_sync_after_for_test(Some((path.clone(), 0, storage::PublicationSyncStage::File)));
    let retry = import(&project.0);
    storage::fail_publication_sync_after_for_test(None);
    let error = retry.unwrap_err();
    assert!(error.contains(retained["importId"].as_str().unwrap()), "continuing witness uncertainty lost the same attempt: {error}");
    assert_eq!(std::fs::read(&path).unwrap(), bytes, "continuing uncertainty appends no second witness");
    assert_eq!(import(&project.0).unwrap()["importId"], retained["importId"]);
    assert_eq!(std::fs::read(path).unwrap(), bytes);
}

#[test]
fn records_store_sync_two_orphan_witness_attempts_are_not_silently_chosen() {
    let own = OwnStore::new();
    let project = Project::new();
    project.in_place();
    let (path, _, retained) = uncertain_witness(&project, &own);
    let files = retained["files"].as_array().unwrap().iter().map(|f| witness::WitnessedFile {
        copy: f["copy"].as_str().unwrap().into(), length: f["length"].as_u64().unwrap(), sha256: f["sha256"].as_str().unwrap().into(),
    }).collect::<Vec<_>>();
    let second_id = "import:invented-earlier-uncertain-attempt";
    witness::record(&own.0, retained["projectId"].as_str().unwrap(), second_id, &files).unwrap();
    let bytes = std::fs::read(&path).unwrap();
    let result = import(&project.0);
    assert!(result.as_ref().is_err_and(|e| e.contains("not known") && e.contains(retained["importId"].as_str().unwrap()) && e.contains(second_id)),
        "two orphan attempts must be named without choosing or minting a third: {result:?}");
    assert_eq!(std::fs::read(path).unwrap(), bytes);
    let dir = attach(&project.0, false).unwrap().dir.unwrap();
    assert!(std::fs::symlink_metadata(dir.join("imports.jsonl")).is_err());
}

#[test]
fn records_store_sync_orphan_recovery_uses_only_this_projects_witness() {
    let own = OwnStore::new();
    let project = Project::new();
    project.in_place();
    let (_, _, retained) = uncertain_witness(&project, &own);
    let other = Project::new();
    other.in_place();
    uncertain_witness(&other, &own);
    let before = std::fs::read(own.0.join(witness::WITNESS_FILE)).unwrap();
    let result = import(&project.0).unwrap();
    assert_eq!(result["importId"], retained["importId"], "another project's orphan is not a candidate");
    assert_eq!(std::fs::read(own.0.join(witness::WITNESS_FILE)).unwrap(), before);
}

#[test]
fn records_store_sync_orphan_recovery_refuses_changed_pending_files_without_a_new_identity() {
    let own = OwnStore::new();
    let project = Project::new();
    project.in_place();
    let (path, bytes, retained) = uncertain_witness(&project, &own);
    project.in_place();
    let result = import(&project.0);
    assert!(result.as_ref().is_err_and(|e| e.contains("not known") && e.contains(retained["importId"].as_str().unwrap())),
        "a changed pending copy is outside the retained witness, not a fresh identity: {result:?}");
    assert_eq!(std::fs::read(path).unwrap(), bytes);
}


/// A whole readable completion whose publication fault stays active until
/// explicitly cleared. Neither read routing nor status proves durability.
struct UnsyncedCompletion {
    own: OwnStore,
    project: Project,
    dir: PathBuf,
    account: Vec<u8>,
    witness: Vec<u8>,
    copy: Vec<u8>,
}
impl UnsyncedCompletion {
    fn new(stage: storage::PublicationSyncStage) -> Self {
        let own = OwnStore::new();
        let project = Project::new();
        project.in_place();
        let dir = attach(&project.0, true).unwrap().dir.unwrap();
        interrupt_import_for_test(Some(0), false);
        let seeded = import(&project.0);
        interrupt_import_for_test(None, false);
        assert!(seeded.as_ref().is_err_and(|e| e.contains("interrupted")), "{seeded:?}");
        let path = dir.join("imports.jsonl");
        let prefix = std::fs::metadata(&path).unwrap().len();
        storage::fail_publication_sync_after_for_test(Some((path.clone(), prefix, stage)));
        let first = import(&project.0);
        assert!(first.as_ref().is_err_and(|e| e.contains("publication sync: injected failure")), "{first:?}");
        let lines = read_lines(&path).unwrap();
        assert_eq!(lines.len(), 2);
        assert_eq!(lines[1]["event"], "completed");
        assert_eq!(lines[1]["importId"], lines[0]["importId"]);
        let account = std::fs::read(path).unwrap();
        let witness = std::fs::read(own.0.join(witness::WITNESS_FILE)).unwrap();
        let copy = std::fs::read(dir.join("acts/in-place.jsonl")).unwrap();
        Self { own, project, dir, account, witness, copy }
    }
    fn unchanged(&self) {
        assert_eq!(std::fs::read(self.dir.join("imports.jsonl")).unwrap(), self.account, "no replacement completion or identity");
        assert_eq!(std::fs::read(self.own.0.join(witness::WITNESS_FILE)).unwrap(), self.witness, "no replacement witness");
        assert_eq!(std::fs::read(self.dir.join("acts/in-place.jsonl")).unwrap(), self.copy);
        assert_eq!(std::fs::read(self.project.0.join(".chirality/records/acts/in-place.jsonl")).unwrap(), self.copy);
    }
}
impl Drop for UnsyncedCompletion {
    fn drop(&mut self) { storage::fail_publication_sync_after_for_test(None); }
}

fn completion_write_gate(stage: storage::PublicationSyncStage) {
    let f = UnsyncedCompletion::new(stage);
    let log = f.dir.join(storage::log_rel(None, "writer:sync-gate"));
    let refused = records::append_project(&f.project.0, None, "writer:sync-gate", "evidence_limit", &APP_WRITER, body("must not be written"));
    assert!(refused.as_ref().is_err_and(|e| e.contains("publication sync: injected failure") && e.contains("nothing written")),
        "write admission bypassed its continuing {stage:?} account sync fault: {refused:?}");
    // A writer that obtained its destination before the fault must also be
    // refused by the permission check under writer ownership.
    let queued = records::append(&log, "evidence_limit", &APP_WRITER, body("queued before the fault"));
    assert!(queued.as_ref().is_err_and(|e| e.contains("publication sync: injected failure") && e.contains("nothing written")), "{queued:?}");
    assert!(!log.exists(), "no record appended by either admission path");
    f.unchanged();
    storage::fail_publication_sync_after_for_test(None);
    records::append_project(&f.project.0, None, "writer:sync-gate", "evidence_limit", &APP_WRITER, body("durability established")).unwrap();
    assert_eq!(records::read_log(&log).0.len(), 1);
    f.unchanged();
}

#[test]
fn records_store_sync_write_gate_refuses_continuing_completion_account_file_sync_failure() {
    completion_write_gate(storage::PublicationSyncStage::File);
}
#[test]
fn records_store_sync_write_gate_refuses_continuing_completion_account_directory_sync_failure() {
    completion_write_gate(storage::PublicationSyncStage::Directory);
}

fn completion_export_gate(stage: storage::PublicationSyncStage) {
    let f = UnsyncedCompletion::new(stage);
    let output = Project::new();
    let destination = output.0.join("verified-export");
    let refused = crate::records_export::export(&f.project.0, &destination);
    assert!(refused.as_ref().is_err_and(|e| e.contains("publication sync: injected failure") && e.contains("nothing exported") && e.contains("retry the import")),
        "export admission bypassed its continuing {stage:?} account sync fault: {refused:?}");
    assert!(!destination.exists());
    assert_eq!(std::fs::read_dir(&output.0).unwrap().count(), 0, "no staging folder left");
    f.unchanged();
    storage::fail_publication_sync_after_for_test(None);
    let settled = crate::records_export::export(&f.project.0, &destination).unwrap();
    assert_eq!(settled["state"], "verified export created");
    assert!(destination.is_dir());
    assert_eq!(std::fs::read_dir(&output.0).unwrap().count(), 1, "only the verified destination remains");
    f.unchanged();
}

#[test]
fn records_store_sync_export_gate_refuses_continuing_completion_account_file_sync_failure() {
    completion_export_gate(storage::PublicationSyncStage::File);
}
#[test]
fn records_store_sync_export_gate_refuses_continuing_completion_account_directory_sync_failure() {
    completion_export_gate(storage::PublicationSyncStage::Directory);
}

fn continuing_witness_fault(stage: storage::PublicationSyncStage) {
    let own = OwnStore::new();
    let project = Project::new();
    project.in_place();
    let dir = attach(&project.0, true).unwrap().dir.unwrap();
    let path = own.0.join(witness::WITNESS_FILE);
    let prefix = std::fs::metadata(&path).unwrap().len();
    storage::fail_publication_sync_after_for_test(Some((path.clone(), prefix, stage)));
    let first = import(&project.0);
    assert!(first.as_ref().is_err_and(|e| e.contains("publication sync: injected failure")), "{first:?}");
    let bytes = std::fs::read(&path).unwrap();
    let retained = read_lines(&path).unwrap().into_iter().find(|v| v["importId"].is_string()).unwrap()["importId"].clone();
    assert!(!dir.join("imports.jsonl").exists());
    let retry = import(&project.0);
    storage::fail_publication_sync_after_for_test(None);
    assert!(retry.as_ref().is_err_and(|e| e.contains("publication sync: injected failure") && e.contains(retained.as_str().unwrap())), "{retry:?}");
    assert!(!dir.join("imports.jsonl").exists());
    assert_eq!(std::fs::read(&path).unwrap(), bytes);
    let settled = import(&project.0).unwrap();
    assert_eq!(settled["importId"], retained);
    assert_eq!(std::fs::read(&path).unwrap(), bytes);
    assert_eq!(read_lines(&dir.join("imports.jsonl")).unwrap().len(), 2);
}

#[test]
fn records_store_sync_witness_directory_fault_active_from_first_append_through_retry() {
    continuing_witness_fault(storage::PublicationSyncStage::Directory);
}

#[test]
fn records_store_sync_new_started_account_directory_failure_keeps_one_attempt() {
    let own = OwnStore::new();
    let project = Project::new();
    project.in_place();
    let dir = attach(&project.0, true).unwrap().dir.unwrap();
    storage::fail_directory_for_test(Some(dir.clone()));
    let first = import(&project.0);
    assert!(first.as_ref().is_err_and(|e| e.contains("injected failure")), "{first:?}");
    let account = dir.join("imports.jsonl");
    let lines = read_lines(&account).unwrap();
    assert_eq!(lines.len(), 1);
    assert_eq!(lines[0]["event"], "started");
    let id = lines[0]["importId"].clone();
    let bytes = std::fs::read(&account).unwrap();
    let witness_bytes = std::fs::read(own.0.join(witness::WITNESS_FILE)).unwrap();
    let retry = import(&project.0);
    storage::fail_directory_for_test(None);
    assert!(retry.as_ref().is_err_and(|e| e.contains(id.as_str().unwrap()) && e.contains("injected failure")), "{retry:?}");
    assert_eq!(std::fs::read(&account).unwrap(), bytes);
    assert_eq!(std::fs::read(own.0.join(witness::WITNESS_FILE)).unwrap(), witness_bytes);
    assert_eq!(import(&project.0).unwrap()["importId"], id);
    assert_eq!(read_lines(&account).unwrap().len(), 2);
    assert_eq!(std::fs::read(own.0.join(witness::WITNESS_FILE)).unwrap(), witness_bytes);
}
