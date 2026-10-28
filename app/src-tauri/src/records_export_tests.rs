use super::*;
use crate::records_store::{self, Placement, Store};

struct Fixture { project: PathBuf, store: PathBuf, output: PathBuf }
impl Fixture {
    fn new() -> Self {
        let folder = |prefix| { let p = std::env::temp_dir().join(crate::util::opaque_id(prefix).unwrap()); std::fs::create_dir(&p).unwrap(); std::fs::canonicalize(p).unwrap() };
        let f = Self { project: folder("bag-project-"), store: folder("bag-store-"), output: folder("bag-output-") };
        records_store::use_store_for_test(Some(Ok(Store { root: f.store.clone(), placement: Placement::Override, limits: vec![] })));
        f
    }
    fn record(&self) -> PathBuf {
        crate::records::append_project(&self.project, Some("run:bag"), "app-writer:local", "evidence_limit", &crate::records::APP_WRITER,
            json!({"label":"unresolvable reference","subjectRef":"invented export fixture"})).unwrap();
        crate::storage::project_log(&self.project, Some("run:bag"), "app-writer:local").unwrap()
    }
    fn bag(&self) -> PathBuf { self.output.join("bag") }
}
impl Drop for Fixture {
    fn drop(&mut self) {
        records_store::use_store_for_test(None);
        for p in [&self.project, &self.store, &self.output] { let _ = std::fs::remove_dir_all(p); }
    }
}

#[test]
fn records_export_preserves_bytes_groups_heads_and_is_checkable_without_app() {
    let f = Fixture::new();
    let log = f.record();
    let specs = (0..2).map(|i| crate::records::Spec { kind: "evidence_limit", recorder: &crate::records::APP_WRITER,
        body: json!({"label":"unresolvable reference","subjectRef":format!("group member {i}")}),
        id: crate::util::opaque_id("rec:app:").unwrap(), observed_at: None }).collect();
    crate::records::append_group(&log, specs, Some("run:bag"), crate::records::RecordSet::Complete).unwrap();
    let dir = records_store::home(&f.project).unwrap().attachment.dir.unwrap();
    std::fs::create_dir_all(f.store.join("indexes")).unwrap();
    std::fs::write(f.store.join("indexes/query.sqlite"), b"discardable cache").unwrap();
    std::fs::create_dir_all(dir.join("connectors")).unwrap();
    std::fs::write(dir.join("connectors/account %\n.json"), b"invented account bytes").unwrap();
    std::fs::write(dir.join("connectors/account \u{2028}.json"), b"invented unicode filename").unwrap();
    std::fs::write(dir.join("connectors/.route-fixture.tmp"), b"interrupted publication evidence").unwrap();
    std::fs::write(dir.join("connectors/retained.lock"), b"retained imported bytes").unwrap();
    let result = export(&f.project, &f.bag()).unwrap();
    assert_eq!(result["state"], "verified export created");
    let rel = log.strip_prefix(&dir).unwrap();
    assert_eq!(std::fs::read(&log).unwrap(), std::fs::read(f.bag().join("data").join(rel)).unwrap());
    assert!(!f.bag().join("data/indexes").exists());
    assert!(!f.bag().join("data/.writer.lock").exists());
    assert_eq!(std::fs::read(f.bag().join("data/connectors/.route-fixture.tmp")).unwrap(), b"interrupted publication evidence");
    assert_eq!(std::fs::read(f.bag().join("data/connectors/retained.lock")).unwrap(), b"retained imported bytes");
    let output = std::process::Command::new("python3").arg(f.bag().join("verify.py")).arg(f.bag()).output().unwrap();
    assert!(output.status.success(), "{}", String::from_utf8_lossy(&output.stderr));
    assert!(export(&f.project, &f.bag()).is_err());
    // A later valid source append cannot change the earlier bag or its heads.
    f.record();
    assert!(verify(&f.bag()).is_ok());
}

#[test]
fn records_export_verifier_refuses_missing_extra_edited_or_linked_members() {
    let f = Fixture::new();
    f.record();
    export(&f.project, &f.bag()).unwrap();
    let payload = files(&f.bag().join("data"), false).unwrap().into_keys().next().unwrap();
    let path = f.bag().join("data").join(payload);
    let bytes = std::fs::read(&path).unwrap();
    std::fs::write(&path, b"edited").unwrap();
    assert!(verify(&f.bag()).is_err());
    std::fs::write(&path, &bytes).unwrap();
    std::fs::write(f.bag().join("data/extra"), b"extra").unwrap();
    assert!(verify(&f.bag()).is_err());
    std::fs::remove_file(f.bag().join("data/extra")).unwrap();
    std::fs::remove_file(&path).unwrap();
    assert!(verify(&f.bag()).is_err());
    std::os::unix::fs::symlink(f.project.join("anything"), &path).unwrap();
    assert!(verify(&f.bag()).is_err());
}

#[test]
fn records_export_refuses_unsafe_destination_and_linked_source_and_never_mints() {
    let f = Fixture::new();
    assert!(export(&f.project, &f.bag()).is_err());
    assert!(!f.project.join(".chirality/project.json").exists());
    f.record();
    assert!(export(&f.project, &f.store.join("bag")).is_err());
    assert!(export(&f.project, &f.project.join("bag")).is_err());
    let dir = records_store::home(&f.project).unwrap().attachment.dir.unwrap();
    std::os::unix::fs::symlink(f.project.join("anything"), dir.join("linked")).unwrap();
    assert!(export(&f.project, &f.bag()).is_err());
    assert!(!f.bag().exists());
}

#[test]
fn records_export_heads_cannot_be_substituted_even_with_rehashed_tags() {
    let f = Fixture::new(); f.record();
    export(&f.project, &f.bag()).unwrap();
    let mut h: Value = serde_json::from_slice(&std::fs::read(f.bag().join(HEADS)).unwrap()).unwrap();
    h["logs"][0]["chain"]["head"] = json!("0".repeat(64));
    std::fs::write(f.bag().join(HEADS), serde_json::to_vec(&h).unwrap()).unwrap();
    std::fs::write(f.bag().join("tagmanifest-sha256.txt"), manifest(&f.bag(), TAGS.iter().map(|s| s.to_string())).unwrap()).unwrap();
    assert!(verify(&f.bag()).is_err_and(|e| e.contains("chain heads differ")));
}

#[test]
fn records_export_preserves_imported_interrupted_connector_evidence() {
    let f = Fixture::new();
    let legacy = f.project.join(".chirality/records/connectors/route-accounts");
    std::fs::create_dir_all(&legacy).unwrap();
    for name in [".route-interrupted.tmp", "retained.lock"] { std::fs::write(legacy.join(name), name.as_bytes()).unwrap(); }
    records_store::import(&f.project).unwrap();
    export(&f.project, &f.bag()).unwrap();
    for name in [".route-interrupted.tmp", "retained.lock"] {
        assert_eq!(std::fs::read(f.bag().join("data/connectors/route-accounts").join(name)).unwrap(), name.as_bytes());
    }
}

#[test]
fn records_export_standalone_refuses_a_bag_without_its_payload_directory() {
    let f = Fixture::new(); f.record(); export(&f.project, &f.bag()).unwrap();
    std::fs::remove_dir_all(f.bag().join("data")).unwrap();
    std::fs::write(f.bag().join("manifest-sha256.txt"), b"").unwrap();
    std::fs::write(f.bag().join("tagmanifest-sha256.txt"), manifest(&f.bag(), TAGS.iter().map(|s| s.to_string())).unwrap()).unwrap();
    let output = std::process::Command::new("python3").arg(f.bag().join("verify.py")).arg(f.bag()).output().unwrap();
    assert!(!output.status.success());
    assert!(verify(&f.bag()).is_err());
}

#[test]
fn records_export_reports_published_location_when_folder_sync_fails() {
    let f = Fixture::new(); f.record();
    crate::storage::fail_directory_for_test(Some(f.output.clone()));
    let result = export(&f.project, &f.bag());
    crate::storage::fail_directory_for_test(None);
    let error = result.unwrap_err();
    assert!(error.contains("export published at") && error.contains("durability not established"));
    assert!(error.contains(f.bag().to_str().unwrap()));
    assert!(verify(&f.bag()).is_ok());
}

#[test]
fn records_export_verifier_refuses_fifo_tags_without_waiting_for_a_writer() {
    use std::os::unix::ffi::OsStrExt;
    let f = Fixture::new(); f.record(); export(&f.project, &f.bag()).unwrap();
    for name in ["bagit.txt", "manifest-sha256.txt", HEADS] {
        let path = f.bag().join(name);
        let original = std::fs::read(&path).unwrap();
        std::fs::remove_file(&path).unwrap();
        let c = std::ffi::CString::new(path.as_os_str().as_bytes()).unwrap();
        assert_eq!(unsafe { libc::mkfifo(c.as_ptr(), 0o600) }, 0);
        assert!(files(&f.bag(), false).is_err());
        assert!(read_tag(&path).is_err());
        assert!(verify(&f.bag()).is_err());
        std::fs::remove_file(&path).unwrap();
        std::fs::write(path, original).unwrap();
    }
}
