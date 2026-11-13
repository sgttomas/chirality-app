//! RS §13.8 records store: placement and override, project identity (mint,
//! missing, changed, duplicated, moved, another store), the explicit import of
//! §13.7 records (byte-identical, verified, idempotent, counted once, drift a
//! limit, originals untouched), refusals, and readers reading the store.
use super::*;
use crate::records::{self, APP_WRITER};
use crate::storage;
use serde_json::json;
use std::collections::BTreeMap;

mod publication { include!("records_store_publication_tests.rs"); }
mod safe_append { include!("records_store_lines_tests.rs"); }
mod legacy_witness { include!("records_store_witness_tests.rs"); }

fn folder(prefix: &str) -> PathBuf {
    let p = std::env::temp_dir().join(crate::util::opaque_id(prefix).unwrap());
    std::fs::create_dir_all(&p).unwrap();
    std::fs::canonicalize(p).unwrap()
}
/// A test's own store on this thread, removed with its folder at the end.
struct OwnStore(PathBuf);
impl OwnStore {
    fn new() -> Self {
        let root = folder("own-records-store-");
        use_store_for_test(Some(Ok(Store { root: root.clone(), placement: Placement::Override, limits: vec![] })));
        OwnStore(root)
    }
}
impl Drop for OwnStore {
    fn drop(&mut self) {
        use_store_for_test(None);
        let _ = std::fs::remove_dir_all(&self.0);
    }
}
fn body(n: &str) -> Value {
    json!({"label":"unresolvable reference","subjectRef":n,"detail":"store test"})
}
fn bytes_and_stamp(path: &Path) -> (Vec<u8>, Value) {
    (std::fs::read(path).unwrap(), stamp_value(&std::fs::metadata(path).unwrap()))
}
/// A §13.7 project as an earlier App left it: a run log, an outside-run act
/// log, a capture with its pending submission, a WR record, and an A15
/// capture and library act log that stay with the library.
fn legacy_project() -> PathBuf {
    let root = folder("legacy-project-");
    let run = root.join(".chirality/records").join(storage::log_rel(Some("run:legacy"), "writer:legacy"));
    records::append(&run, "evidence_limit", &APP_WRITER, body("legacy run entry")).unwrap();
    records::append(&run, "evidence_limit", &APP_WRITER, body("legacy run entry 2")).unwrap();
    let acts = root.join(".chirality/records").join(crate::recorder::LOG);
    records::append(&acts, "evidence_limit", &APP_WRITER, body("legacy act log entry")).unwrap();
    let captures = root.join(".chirality/captures");
    std::fs::create_dir_all(captures.join("pending")).unwrap();
    std::fs::write(captures.join("aaaa.json"), br#"{"captureId":"cap:legacy","actKind":"A16"}"#).unwrap();
    std::fs::write(captures.join("pending/aaaa.json"), br#"{"capture":{"captureId":"cap:legacy","actKind":"A16"},"log":".chirality/records/acts/x.jsonl"}"#).unwrap();
    std::fs::write(captures.join("bbbb.json"), br#"{"captureId":"cap:library","actKind":"A15"}"#).unwrap();
    let workflow = root.join(".chirality/records/workflow");
    std::fs::create_dir_all(&workflow).unwrap();
    std::fs::write(workflow.join("11111111-1111-4111-8111-111111111111.json"), b"{\"version\":1}").unwrap();
    records::append(&storage::library_log(&root), "evidence_limit", &APP_WRITER, body("library act")).unwrap();
    root
}

// ---- Placement ----

fn import_gate_project() -> (OwnStore, PathBuf, PathBuf) {
    let own = OwnStore::new();
    let root = folder("import-gate-project-");
    let dir = write_dir(&root).unwrap();
    let log = root.join(".chirality/records").join(storage::log_rel(None, "writer:legacy"));
    records::append(&log, "evidence_limit", &APP_WRITER, body("in place")).unwrap();
    assert!(write_dir(&root).unwrap_err().contains("import needed"));
    (own, root, dir)
}

#[test]
fn records_store_import_gate_non_directory_is_unknown_never_authority() {
    let mut results = Vec::new();
    for name in ["runs", "acts", "workflow", "legacy", "connectors", "captures"] {
        let (_own, root, dir) = import_gate_project();
        std::fs::write(dir.join(name), b"not a folder").unwrap();
        results.push((name, write_dir(&root)));
        std::fs::remove_dir_all(root).unwrap();
    }
    assert!(results.iter().all(|(_, r)| r.as_ref().is_err_and(|e| e.contains("unknown"))), "{results:?}");
}

#[test]
fn records_store_import_gate_unfamiliar_member_is_unknown_never_authority() {
    let mut results = Vec::new();
    for name in ["runs", "acts", "workflow", "legacy", "connectors", "captures", "captures/pending"] {
        let (_own, root, dir) = import_gate_project();
        std::fs::create_dir_all(dir.join(name)).unwrap();
        std::fs::write(dir.join(name).join("unfamiliar"), b"unrecognised bytes").unwrap();
        results.push((name, write_dir(&root)));
        std::fs::remove_dir_all(root).unwrap();
    }
    assert!(results.iter().all(|(_, r)| r.as_ref().is_err_and(|e| e.contains("unknown"))), "{results:?}");
}

#[test]
fn records_store_import_gate_empty_census_does_not_refuse_unrecognised_member() {
    let _own = OwnStore::new();
    let root = folder("import-gate-empty-census-");
    let dir = write_dir(&root).unwrap();
    std::fs::create_dir(dir.join("workflow")).unwrap();
    std::fs::write(dir.join("workflow/unfamiliar"), b"not a recognised record").unwrap();
    assert!(legacy_census(&root).unwrap().is_empty());
    let result = write_dir(&root);
    assert!(result.is_ok(), "nothing to import, so no authority is needed to waive a census: {result:?}");
    std::fs::remove_dir_all(root).unwrap();
}

#[test]
fn records_store_import_gate_unlistable_folder_is_unknown_never_authority() {
    use std::os::unix::fs::PermissionsExt;
    let mut results = Vec::new();
    for name in ["runs", "acts", "workflow", "legacy", "connectors", "captures"] {
        let (_own, root, dir) = import_gate_project();
        let path = dir.join(name);
        std::fs::create_dir(&path).unwrap();
        std::fs::set_permissions(&path, std::fs::Permissions::from_mode(0o000)).unwrap();
        let denied = std::fs::read_dir(&path).err().map(|e| e.kind());
        let result = write_dir(&root);
        std::fs::set_permissions(&path, std::fs::Permissions::from_mode(0o700)).unwrap();
        assert_eq!(denied, Some(std::io::ErrorKind::PermissionDenied));
        results.push((name, result));
        std::fs::remove_dir_all(root).unwrap();
    }
    assert!(results.iter().all(|(_, r)| r.as_ref().is_err_and(|e| e.contains("unknown"))), "{results:?}");
}

#[test]
fn records_store_import_gate_unexaminable_member_is_unknown_never_authority() {
    use std::os::unix::fs::PermissionsExt;
    let (_own, root, dir) = import_gate_project();
    let path = dir.join("acts");
    std::fs::create_dir(&path).unwrap();
    std::fs::write(path.join(format!("{}.jsonl", storage::key("writer"))), b"unreadable").unwrap();
    std::fs::set_permissions(&path, std::fs::Permissions::from_mode(0o400)).unwrap();
    let inventory = crate::records_inspect::listing(&path).unwrap().unwrap();
    let result = write_dir(&root);
    std::fs::set_permissions(&path, std::fs::Permissions::from_mode(0o700)).unwrap();
    assert!(inventory.iter().all(|e| e.metadata.is_err()));
    assert!(result.as_ref().is_err_and(|e| e.contains("unknown")), "{result:?}");
    std::fs::remove_dir_all(root).unwrap();
}

#[test]
fn records_store_import_gate_capture_name_without_capture_form_is_unknown() {
    let mut results = Vec::new();
    for name in ["captures", "captures/pending"] {
        let (_own, root, dir) = import_gate_project();
        std::fs::create_dir_all(dir.join(name)).unwrap();
        std::fs::write(dir.join(name).join(format!("{}.json", storage::key("cap:fixture"))), b"{}").unwrap();
        results.push((name, write_dir(&root)));
        std::fs::remove_dir_all(root).unwrap();
    }
    assert!(results.iter().all(|(_, r)| r.as_ref().is_err_and(|e| e.contains("unknown"))), "{results:?}");
}

#[test]
fn records_store_import_gate_recognised_rs_records_waive_census() {
    for name in [storage::log_rel(Some("run:held"), "writer:held"), storage::log_rel(None, "writer:held"), REGISTERED_COPY.into()] {
        let (_own, root, dir) = import_gate_project();
        let destination = dir.join(name);
        std::fs::create_dir_all(destination.parent().unwrap()).unwrap();
        std::fs::copy(root.join(".chirality/records").join(storage::log_rel(None, "writer:legacy")), destination).unwrap();
        assert!(write_dir(&root).is_ok());
        std::fs::remove_dir_all(root).unwrap();
    }
}

#[test]
fn records_store_import_gate_recognised_capture_and_pending_waive_census() {
    let capture: Value = serde_json::from_slice(include_bytes!("../../tests/fixtures/FX-DP1/aac/cap-decide-PKG-1.json")).unwrap();
    crate::schema_validation::validate_capture(&capture).unwrap();
    for pending in [false, true] {
        let (_own, root, dir) = import_gate_project();
        let folder = dir.join(if pending { "captures/pending" } else { "captures" });
        std::fs::create_dir_all(&folder).unwrap();
        let value = if pending { json!({"capture":capture,"recordId":"rec:app:pending","log":crate::recorder::LOG,"observedAt":capture["capturedAt"],"delayed":false}) } else { capture.clone() };
        std::fs::write(folder.join(format!("{}.json", storage::key(capture["captureId"].as_str().unwrap()))), serde_json::to_vec(&value).unwrap()).unwrap();
        assert!(write_dir(&root).is_ok());
        std::fs::remove_dir_all(root).unwrap();
    }
}

#[test]
fn records_store_import_gate_completed_import_waives_census_but_incomplete_still_refuses() {
    let (_own, root, dir) = import_gate_project();
    import(&root).unwrap();
    std::fs::write(root.join(".chirality/records/late.jsonl"), b"a late legacy file").unwrap();
    assert!(write_dir(&root).is_ok());
    append_line(&dir.join("imports.jsonl"), &json!({"format":IMPORT_FORMAT,"formatVersion":VERSION,"event":"started","importId":"import:late","at":"now","storeHeld":true,"census":[]})).unwrap();
    assert!(store_holds(&dir).unwrap());
    assert!(write_dir(&root).unwrap_err().contains("import incomplete"));
    std::fs::remove_dir_all(root).unwrap();
}

#[test]
fn records_store_import_gate_controls_and_exact_staging_names_never_waive_census() {
    let nonce = "12345678-1234-4234-8234-123456789abc";
    let hash = storage::key("cap:fixture");
    for relative in [".writer.lock".into(), "captures/.capture.lock".into(), "captures/pending".into(),
        format!("captures/.{hash}.json.{nonce}.tmp"),
        format!("captures/pending/.{hash}.json.{nonce}.tmp"),
        format!("workflow/.pending-{nonce}"),
        format!("workflow/.{nonce}.json.{nonce}.tmp"),
        format!("connectors/route-accounts/.route-{nonce}.tmp")] {
        let (_own, root, dir) = import_gate_project();
        let path = dir.join(&relative);
        if relative == "captures/pending" { std::fs::create_dir_all(&path).unwrap(); }
        else {
            std::fs::create_dir_all(path.parent().unwrap()).unwrap();
            std::fs::write(&path, b"").unwrap();
        }
        let result = write_dir(&root);
        assert!(result.as_ref().is_err_and(|e| e.contains("import needed")), "{relative}: {result:?}");
        // The same preparation in a new project must admit normal recording.
        std::fs::remove_dir_all(root.join(".chirality/records")).unwrap();
        assert!(write_dir(&root).is_ok(), "{relative}: normal first write refused");
        std::fs::remove_dir_all(root).unwrap();
    }
}

#[test]
fn records_store_import_gate_recognised_capture_during_create_link_waives_census() {
    let (_own, root, dir) = import_gate_project();
    let capture: Value = serde_json::from_slice(include_bytes!("../../tests/fixtures/FX-DP1/aac/cap-decide-PKG-1.json")).unwrap();
    let check_root = root.clone();
    storage::after_create_link_for_test(Some(Box::new(move |_| {
        assert!(write_dir(&check_root).is_ok(), "a published capture's temporary hard-link alias must not refuse ordinary recording");
    })));
    storage::create_json(&dir.join("captures").join(format!("{}.json", storage::key(capture["captureId"].as_str().unwrap()))), &capture).unwrap();
    std::fs::remove_dir_all(root).unwrap();
}

#[test]
fn placement_uses_the_override_or_app_data_and_never_falls_back() {
    // The App data folder as a release build sees it (never created here; outside every temporary folder).
    let data = PathBuf::from(format!("/nonexistent-app-data-for-test/{}", crate::util::opaque_id("").unwrap()));
    let project = folder("placement-project-");
    // A development build without the override has no store, and says why.
    let dev = for_app(None, Ok(&data), true, Some(&project), &[]).unwrap_err();
    assert!(dev.contains(OVERRIDE_ENV) && dev.contains("nothing is recorded"), "{dev}");
    // A release build: `<App data>/records/`, unless the person chose a location.
    let release = for_app(None, Ok(&data), false, Some(&project), &[]).unwrap();
    assert_eq!((release.root.clone(), release.placement), (data.join("records"), Placement::AppData));
    // The App data folder unavailable: no store, no other location.
    assert!(for_app(None, Err("no data".into()), false, None, &[]).unwrap_err().contains("App data folder unavailable"));
    // The development override is placed by the same rules: inside the
    // project or a Codex home it is refused, in every build.
    let inside = project.join("records");
    assert!(for_app(Some(inside), Ok(&data), true, Some(&project), &[]).unwrap_err().contains("project working tree"));
    let codex = PathBuf::from("/nonexistent-codex-home-for-test");
    assert!(for_app(Some(codex.join("records")), Ok(&data), true, None, &[codex.clone()]).unwrap_err().contains("Codex home"));
    // Only the override may name a temporary folder (a test store), shown as a limit.
    let temporary = std::env::temp_dir().join(crate::util::opaque_id("override-store-").unwrap());
    let overridden = for_app(Some(temporary.clone()), Ok(&data), true, Some(&project), &[]).unwrap();
    assert_eq!((overridden.root.clone(), overridden.placement), (temporary.clone(), Placement::Override));
    assert!(overridden.limits.iter().any(|l| l.contains("temporary folder")), "{:?}", overridden.limits);
    // A test build's own default store is never the App data folder. Read the
    // default itself: another test may have configured this process's store.
    let test_store = from_environment().unwrap();
    assert!(matches!(test_store.placement, Placement::Test | Placement::Override));
    assert!(test_store.root.starts_with(std::env::temp_dir()) || test_store.placement == Placement::Override);
    let _ = std::fs::remove_dir_all(&project);
}

#[test]
fn a_chosen_location_outside_the_project_and_codex_homes_takes_effect_next_start() {
    let data = folder("app-data-");
    let project = folder("chosen-project-");
    let codex = folder("codex-home-");
    // Inside the project, a Codex home or a temporary folder: refused.
    assert!(choose_location(&data, &project.join("store"), Some(&project), &[]).unwrap_err().contains("project working tree"));
    assert!(choose_location(&data, &codex.join("records"), None, &[codex.clone()]).unwrap_err().contains("Codex home"));
    assert!(choose_location(&data, &std::env::temp_dir().join("elsewhere"), None, &[]).unwrap_err().contains("temporary folder"));
    assert!(chosen_location(&data).unwrap().is_none(), "nothing recorded by a refusal");
    // A location the person may choose (lexically outside all three).
    let volume = PathBuf::from("/Volumes/Backup-for-test/Chirality records");
    let chosen = choose_location(&data, &volume, Some(&project), &[codex.clone()]).unwrap();
    assert_eq!(chosen["takesEffect"], "when the App next starts");
    assert_eq!(chosen_location(&data).unwrap(), Some(volume.clone()));
    let store = for_app(None, Ok(&data), false, Some(&project), &[codex.clone()]).unwrap();
    assert_eq!((store.root, store.placement), (volume, Placement::PersonChosen));
    for p in [data, project, codex] {
        let _ = std::fs::remove_dir_all(p);
    }
}

#[test]
fn the_app_reports_the_store_it_writes_and_an_unusable_store_refuses_recording() {
    let project = folder("status-project-");
    {
        let own = OwnStore::new();
        let status = status(Some(&project));
        assert_eq!(status["state"], "available");
        assert_eq!(status["root"], own.0.display().to_string());
        assert_eq!(status["placement"], Placement::Override.label());
        assert!(status["storeId"].as_str().unwrap().starts_with("records-store:"));
        // A store whose folder is a file: unavailable, and nothing is written anywhere.
        std::fs::remove_dir_all(&own.0).unwrap();
        std::fs::write(&own.0, b"not a folder").unwrap();
        *OPENED.lock().unwrap() = None;
        let status = super::status(Some(&project));
        assert_eq!(status["state"], "unavailable", "{status}");
        assert_eq!(status["recording"], "refused; no fallback");
        let refused = records::append_project(&project, None, "writer:x", "evidence_limit", &APP_WRITER, body("x")).unwrap_err();
        assert!(refused.contains("records store unavailable"), "{refused}");
        assert!(!project.join(".chirality/records").exists(), "no fallback to a project path");
        std::fs::remove_file(&own.0).unwrap();
        std::fs::create_dir(&own.0).unwrap();
    }
    {
        // No store configured at all: refused with the cause.
        use_store_for_test(Some(Err("no records store configured".into())));
        let refused = records::append_project(&project, None, "writer:x", "evidence_limit", &APP_WRITER, body("x")).unwrap_err();
        assert!(refused.contains("no records store configured"), "{refused}");
        assert_eq!(super::status(Some(&project))["state"], "unavailable");
        use_store_for_test(None);
    }
    assert!(!project.join(".chirality/records").exists());
    let _ = std::fs::remove_dir_all(&project);
}

// ---- Project identity ----

#[test]
fn a_new_project_is_given_an_identity_once_and_the_store_records_its_root() {
    let root = folder("mint-project-");
    // A read mints nothing.
    assert_eq!(attach(&root, false).unwrap().how, "none");
    assert!(!root.join(PROJECT_LINK).exists());
    let log = storage::project_log(&root, None, "writer:mint").unwrap();
    let first = attach(&root, false).unwrap();
    let project = first.project.clone().unwrap();
    assert!(project.starts_with("chirality-project:"));
    assert_eq!(first.how, "attached");
    assert!(first.limits.is_empty() && first.refusal.is_none());
    assert!(log.starts_with(first.dir.as_ref().unwrap()) && !log.starts_with(&root), "the log is in the store, outside the project");
    let link: Value = serde_json::from_slice(&std::fs::read(root.join(PROJECT_LINK)).unwrap()).unwrap();
    assert_eq!(link["projectId"], project.as_str());
    assert_eq!(link["format"], LINK_FORMAT);
    let (store, store_id) = opened().unwrap();
    assert_eq!(link["storeId"], store_id.as_str());
    assert!(first.dir.as_ref().unwrap().join("project.json").is_file());
    assert_eq!(roots_of(&roots(&store).unwrap(), &project), vec![root.display().to_string()]);
    // Attaching again keeps the identity.
    storage::project_log(&root, Some("run:1"), "writer:mint").unwrap();
    assert_eq!(attach(&root, true).unwrap().project.as_deref(), Some(project.as_str()));
    let _ = std::fs::remove_dir_all(&root);
}

#[test]
fn a_missing_changed_or_unreadable_project_file_attaches_nothing_until_the_person_restores_it() {
    let root = folder("link-project-");
    records::append_project(&root, None, "writer:link", "evidence_limit", &APP_WRITER, body("before")).unwrap();
    let governing = attach(&root, false).unwrap().project.unwrap();
    // Missing: never attached on the folder's path alone. Nothing is read or
    // written for it, and nothing is minted, until the person acts.
    std::fs::remove_file(root.join(PROJECT_LINK)).unwrap();
    let missing = attach(&root, true).unwrap();
    assert!(missing.dir.is_none() && missing.project.is_none(), "{missing:?}");
    assert_eq!(missing.recorded.as_deref(), Some(governing.as_str()));
    assert!(missing.refusal.as_deref().unwrap().starts_with("link missing; not attached"), "{missing:?}");
    assert!(!root.join(PROJECT_LINK).exists(), "nothing minted over the gap");
    let refused = records::append_project(&root, None, "writer:link", "evidence_limit", &APP_WRITER, body("while missing")).unwrap_err();
    assert!(refused.contains("link missing; not attached"), "{refused}");
    assert_eq!(storage::read_all(&root).0.len(), 0, "the store's history is not read for a folder with no link");
    // Nor are files kept in the project folder read in its place. An old log
    // still in the folder is not this project's history while the store
    // holds records for the folder that will not attach: every ordinary
    // reader and the status say the records are unavailable, and no import
    // is asked for.
    let kept = root.join(".chirality/records").join(storage::log_rel(Some("run:kept"), "writer:kept"));
    // (Written by hand, as an earlier App left it: the App's own writer refuses to write there now.)
    assert!(records::append(&kept, "evidence_limit", &APP_WRITER, body("refused")).unwrap_err().contains("project records unavailable"));
    std::fs::create_dir_all(kept.parent().unwrap()).unwrap();
    let mut line = serde_json::to_vec(&records::envelope("evidence_limit", &APP_WRITER, body("kept in the project folder"), crate::util::opaque_id("rec:app:").unwrap(), 1, Some("run:kept"), Some("2026-10-01T00:00:00.000Z"))).unwrap();
    line.push(b'\n');
    std::fs::write(&kept, line).unwrap();
    let (entries, limits) = storage::read_all(&root);
    assert!(entries.is_empty() && limits.iter().any(|l| l.contains("project records unavailable") && l.contains("link missing")), "{entries:?} {limits:?}");
    for unavailable in [storage::sources(&root).map(|_| ()), storage::discover(&root).map(|_| ()), storage::capture_dir(&root).map(|_| ()), storage::registered_legacy_log(&root).map(|_| ())] {
        assert!(unavailable.unwrap_err().contains("project records unavailable"));
    }
    let decisions = crate::decision_view::derive(&root, &[]);
    assert!(decisions["limits"].as_array().unwrap().iter().any(|l| l.as_str().is_some_and(|l| l.contains("project records unavailable"))), "{decisions}");
    let shown = status(Some(&root));
    assert_eq!(shown["project"]["reading"], "nothing from the records store (the project is not attached)", "{shown}");
    assert_eq!(shown["project"]["importNeeded"], false, "{shown}");
    // Review round 3, finding 2: nor do the notes say the kept files are
    // read in place or ask for an import; the refusal is the note.
    let said = shown["project"]["notes"].as_array().unwrap();
    assert!(said.iter().all(|n| n.as_str().is_some_and(|n| !n.contains("import needed") && !n.contains("read in place"))), "{shown}");
    assert!(said.iter().any(|n| n.as_str().is_some_and(|n| n.contains("link missing"))), "{shown}");
    std::fs::remove_dir_all(root.join(".chirality/records")).unwrap();
    assert!(notes(&root).iter().any(|n| n.contains("link missing")));
    assert_eq!(status(Some(&root))["project"]["attachment"]["recordedHere"], governing.as_str());
    assert_eq!(missing.fault, Some("link missing"));
    assert_eq!(missing.resolutions, ["restore-link", "new-identity"]);
    // The one-click restore attaches it again, with its history.
    assert_eq!(restore_link(&root).unwrap()["projectId"], governing.as_str());
    assert_eq!(storage::read_all(&root).0.len(), 1);
    records::append_project(&root, None, "writer:link", "evidence_limit", &APP_WRITER, body("restored")).unwrap();
    // Changed (an agent edits it to name another identity): the store does not
    // choose between the two. Not attached: nothing read, written or minted,
    // under either identity, and the file is left as it was found.
    let forged = serde_json::to_vec(&link_value("chirality-project:forged", "records-store:other")).unwrap();
    std::fs::write(root.join(PROJECT_LINK), &forged).unwrap();
    let store = opened().unwrap().0;
    let roots_before = std::fs::read(store.join("roots.jsonl")).unwrap();
    let log = project_dir(&store, &governing).join(storage::log_rel(None, "writer:link"));
    let log_before = std::fs::read(&log).unwrap();
    for mint in [true, false] {
        let changed = attach(&root, mint).unwrap();
        assert!(changed.dir.is_none() && changed.project.is_none(), "{changed:?}");
        assert_eq!(changed.how, "unattached");
        assert_eq!(changed.recorded.as_deref(), Some(governing.as_str()));
        assert_eq!(changed.linked.as_deref(), Some("chirality-project:forged"));
        assert_eq!(changed.fault, Some("link changed"));
        assert_eq!(changed.resolutions, ["restore-link", "adopt", "new-identity"]);
        let refusal = changed.refusal.as_deref().unwrap();
        assert!(refusal.starts_with("link changed; not attached") && refusal.contains("chirality-project:forged") && refusal.contains(governing.as_str()), "{refusal}");
    }
    let refused = records::append_project(&root, None, "writer:link", "evidence_limit", &APP_WRITER, body("while changed")).unwrap_err();
    assert!(refused.contains("link changed; not attached"), "{refused}");
    assert!(storage::write_capture_dir(&root).unwrap_err().contains("link changed; not attached"));
    assert_eq!(storage::read_all(&root).0.len(), 0, "the store's history is not read for a folder whose link names another identity");
    assert_eq!(std::fs::read(root.join(PROJECT_LINK)).unwrap(), forged, "the link is not rewritten until the person acts");
    assert_eq!(std::fs::read(store.join("roots.jsonl")).unwrap(), roots_before, "nothing registered for the named identity");
    assert_eq!(std::fs::read(&log).unwrap(), log_before, "nothing written under the recorded identity");
    assert!(!project_dir(&store, "chirality-project:forged").exists(), "nothing minted for the named identity");
    let view = status(Some(&root));
    assert_eq!(view["project"]["attachment"]["fault"], "link changed");
    assert_eq!(view["project"]["attachment"]["linkedIdentity"], "chirality-project:forged");
    assert_eq!(view["project"]["attachment"]["resolutions"], json!(["restore-link", "adopt", "new-identity"]));
    assert_eq!(view["project"]["reading"], "nothing from the records store (the project is not attached)");
    assert!(notes(&root).iter().any(|n| n.contains("link changed")));
    // Restoring the link attaches the folder to the recorded identity again.
    assert_eq!(restore_link(&root).unwrap()["projectId"], governing.as_str());
    let (entries, limits) = storage::read_all(&root);
    assert!(limits.is_empty(), "{limits:?}");
    assert_eq!(entries.len(), 2, "both entries, in the governing project");
    let restored = attach(&root, false).unwrap();
    assert!(restored.limits.is_empty() && restored.fault.is_none() && restored.resolutions.is_empty(), "{restored:?}");
    // Unreadable: like missing, not attached.
    std::fs::write(root.join(PROJECT_LINK), b"{").unwrap();
    let unreadable = attach(&root, true).unwrap();
    assert!(unreadable.dir.is_none() && unreadable.refusal.as_deref().unwrap().starts_with("link unreadable; not attached"), "{unreadable:?}");
    assert!(records::append_project(&root, None, "writer:link", "evidence_limit", &APP_WRITER, body("x")).is_err());

    // The person restores the link.
    assert_eq!(restore_link(&root).unwrap()["projectId"], governing.as_str());
    let restored = attach(&root, false).unwrap();
    assert!(restored.limits.is_empty(), "{:?}", restored.limits);
    let _ = std::fs::remove_dir_all(&root);
}

#[test]
fn a_changed_link_naming_a_project_moved_to_this_folder_is_adopted_and_the_earlier_identity_keeps_its_records() {
    // Project P is recorded at `here`; the person puts project Q's folder
    // (its link with it) where P stood.
    let here = folder("changed-here-");
    records::append_project(&here, None, "writer:p", "evidence_limit", &APP_WRITER, body("P's entry")).unwrap();
    let p = attach(&here, false).unwrap().project.unwrap();
    let elsewhere = folder("changed-elsewhere-");
    records::append_project(&elsewhere, None, "writer:q", "evidence_limit", &APP_WRITER, body("Q's entry")).unwrap();
    let q = attach(&elsewhere, false).unwrap().project.unwrap();
    std::fs::rename(elsewhere.join(PROJECT_LINK), here.join(PROJECT_LINK)).unwrap();
    let store = opened().unwrap().0;
    let p_log = project_dir(&store, &p).join(storage::log_rel(None, "writer:p"));
    let p_bytes = std::fs::read(&p_log).unwrap();
    let changed = attach(&here, true).unwrap();
    assert_eq!((changed.fault, changed.recorded.as_deref(), changed.linked.as_deref()), (Some("link changed"), Some(p.as_str()), Some(q.as_str())));
    assert_eq!(changed.resolutions, ["restore-link", "adopt", "new-identity"]);
    assert_eq!(storage::read_all(&here).0.len(), 0);
    // The person confirms this folder is the project its file names.
    let adopted = adopt(&here).unwrap();
    assert_eq!(adopted["projectId"], q.as_str());
    assert_eq!(adopted["releasedHere"], json!([p]));
    let now = attach(&here, false).unwrap();
    assert_eq!(now.project.as_deref(), Some(q.as_str()));
    assert!(now.refusal.is_none() && now.limits.is_empty() && now.resolutions.is_empty(), "{now:?}");
    let lines = roots(&store).unwrap();
    assert_eq!(listed(&lines, here.to_str().unwrap()), vec![q.clone()]);
    assert_eq!(roots_of(&lines, &q), vec![here.display().to_string()], "Q's earlier folder is released");
    assert!(roots_of(&lines, &p).is_empty(), "this folder is released from P");
    let (entries, limits) = storage::read_all(&here);
    assert!(limits.is_empty(), "{limits:?}");
    assert_eq!(entries.len(), 1, "Q's history, and none of P's");
    assert_eq!(entries[0]["body"]["subjectRef"], "Q's entry");
    assert_eq!(std::fs::read(&p_log).unwrap(), p_bytes, "P's records stay in the store, unchanged");
    records::append_project(&here, None, "writer:q", "evidence_limit", &APP_WRITER, body("Q after the move")).unwrap();
    assert_eq!(std::fs::read(&p_log).unwrap(), p_bytes);
    // A second adoption has nothing to do.
    assert!(adopt(&here).unwrap_err().contains("already attached to the project its file names"));
    let _ = (std::fs::remove_dir_all(&here), std::fs::remove_dir_all(&elsewhere));
}

#[test]
fn a_changed_link_copied_from_a_project_still_at_its_folder_is_not_adopted_and_a_new_identity_keeps_both_histories() {
    let here = folder("copied-here-");
    records::append_project(&here, None, "writer:p", "evidence_limit", &APP_WRITER, body("P's entry")).unwrap();
    let p = attach(&here, false).unwrap().project.unwrap();
    let original = folder("copied-original-");
    records::append_project(&original, None, "writer:q", "evidence_limit", &APP_WRITER, body("Q's entry")).unwrap();
    let q = attach(&original, false).unwrap().project.unwrap();
    std::fs::copy(original.join(PROJECT_LINK), here.join(PROJECT_LINK)).unwrap();
    let changed = attach(&here, true).unwrap();
    assert_eq!(changed.fault, Some("link changed"));
    assert_eq!(changed.resolutions, ["restore-link", "new-identity"], "Q is still at its own folder: adoption is not offered");
    assert!(!changed.refusal.as_deref().unwrap().contains("confirms this folder is the project its file names"));
    let store = opened().unwrap().0;
    let roots_before = std::fs::read(store.join("roots.jsonl")).unwrap();
    assert!(adopt(&here).unwrap_err().contains("another folder holds this project identity"));
    assert_eq!(std::fs::read(store.join("roots.jsonl")).unwrap(), roots_before, "a refused adoption releases nothing");
    assert_eq!(attach(&original, false).unwrap().project.as_deref(), Some(q.as_str()), "the original is unaffected");
    // A new identity: P's and Q's records both stay under their identities.
    let fresh = new_identity(&here).unwrap()["projectId"].as_str().unwrap().to_owned();
    assert!(fresh != p && fresh != q);
    assert_eq!(storage::read_all(&here).0.len(), 0);
    assert!(project_dir(&store, &p).join(storage::log_rel(None, "writer:p")).is_file());
    assert_eq!(storage::read_all(&original).0.len(), 1);
    let _ = (std::fs::remove_dir_all(&here), std::fs::remove_dir_all(&original));
}

#[test]
fn a_link_naming_another_store_with_the_recorded_identity_is_a_changed_link_and_attaches_nothing() {
    let root = folder("store-named-");
    records::append_project(&root, None, "writer:s", "evidence_limit", &APP_WRITER, body("entry")).unwrap();
    let id = attach(&root, false).unwrap().project.unwrap();
    std::fs::write(root.join(PROJECT_LINK), serde_json::to_vec(&link_value(&id, "records-store:another")).unwrap()).unwrap();
    for mint in [true, false] {
        let named = attach(&root, mint).unwrap();
        assert!(named.dir.is_none() && named.project.is_none(), "{named:?}");
        assert!(named.refusal.as_deref().unwrap().starts_with("link changed; not attached") && named.refusal.as_deref().unwrap().contains("names another records store (records-store:another)"), "{named:?}");
        assert_eq!((named.fault, named.resolutions.as_slice(), named.recorded.as_deref()), (Some("link names another store"), ["restore-link"].as_slice(), Some(id.as_str())));
    }
    assert!(records::append_project(&root, None, "writer:s", "evidence_limit", &APP_WRITER, body("x")).unwrap_err().contains("link changed; not attached"));
    assert_eq!(storage::read_all(&root).0.len(), 0);
    restore_link(&root).unwrap();
    let restored = attach(&root, false).unwrap();
    assert!(restored.refusal.is_none() && restored.limits.is_empty() && restored.fault.is_none(), "{restored:?}");
    assert_eq!(storage::read_all(&root).0.len(), 1);
    let _ = std::fs::remove_dir_all(&root);
}

#[test]
fn a_link_file_written_with_the_earlier_note_still_reads() {
    // The note in a link file is for a person reading the file; readers do
    // not take it. A file an earlier build wrote attaches as before.
    let root = folder("old-note-");
    records::append_project(&root, None, "writer:n", "evidence_limit", &APP_WRITER, body("entry")).unwrap();
    let mut link: Value = serde_json::from_slice(&std::fs::read(root.join(PROJECT_LINK)).unwrap()).unwrap();
    assert_eq!(link["note"], "A link to this project's records in the Chirality App's records store. The store's own record governs; a changed or missing file attaches nothing until you resolve it in the App.");
    link["note"] = json!("A link to this project's records in the Chirality App's records store. The store's own record governs; editing this file only produces a limit.");
    std::fs::write(root.join(PROJECT_LINK), serde_json::to_vec(&link).unwrap()).unwrap();
    let attached = attach(&root, false).unwrap();
    assert!(attached.dir.is_some() && attached.refusal.is_none() && attached.limits.is_empty(), "{attached:?}");
    assert_eq!(storage::read_all(&root).0.len(), 1);
    link.as_object_mut().unwrap().remove("note");
    std::fs::write(root.join(PROJECT_LINK), serde_json::to_vec(&link).unwrap()).unwrap();
    assert!(attach(&root, false).unwrap().dir.is_some(), "nor is the note required");
    let _ = std::fs::remove_dir_all(&root);
}

#[test]
fn a_folder_is_not_given_another_identity_while_its_recorded_project_is_still_in_use() {
    // P is recorded here and something still holds its activity (a running
    // Codex, an open run, a record waiting to be written). Q's link arrives.
    let here = folder("in-use-here-");
    records::append_project(&here, None, "writer:p", "evidence_limit", &APP_WRITER, body("P's entry")).unwrap();
    let p = attach(&here, false).unwrap().project.unwrap();
    let elsewhere = folder("in-use-elsewhere-");
    records::append_project(&elsewhere, None, "writer:q", "evidence_limit", &APP_WRITER, body("Q's entry")).unwrap();
    let in_use = crate::records_retention::activity(&here).unwrap().expect("P's activity lease");
    std::fs::rename(elsewhere.join(PROJECT_LINK), here.join(PROJECT_LINK)).unwrap();
    let store = opened().unwrap().0;
    let roots_before = std::fs::read(store.join("roots.jsonl")).unwrap();
    let link_before = std::fs::read(here.join(PROJECT_LINK)).unwrap();
    for refused in [adopt(&here).unwrap_err(), new_identity(&here).unwrap_err()] {
        assert!(refused.contains(&format!("project {p}, which the records store recorded at this folder, is still in use")), "{refused}");
        assert!(refused.contains("Stop Codex and end the run") && refused.contains("restore the project file so it can be written") && refused.ends_with("nothing changed"), "{refused}");
    }
    assert_eq!(std::fs::read(store.join("roots.jsonl")).unwrap(), roots_before, "a refused act releases and registers nothing");
    assert_eq!(std::fs::read(here.join(PROJECT_LINK)).unwrap(), link_before);
    // Restoring the link is never refused for this: it is what lets P's waiting records be written.
    restore_link(&here).unwrap();
    records::append_project(&here, None, "writer:p", "evidence_limit", &APP_WRITER, body("P's waiting entry")).unwrap();
    assert_eq!(storage::read_all(&here).0.len(), 2);
    // Once nothing holds P, the person may give the folder another identity.
    drop(in_use);
    std::fs::write(here.join(PROJECT_LINK), &link_before).unwrap();
    assert!(adopt(&here).is_ok());
    let _ = (std::fs::remove_dir_all(&here), std::fs::remove_dir_all(&elsewhere));
}

#[test]
fn an_adoption_stopped_after_its_release_lines_is_offered_to_the_person_to_complete() {
    // The state an interrupted adoption leaves: every earlier root of Q
    // released, this folder not yet registered, its link naming Q.
    let before = folder("stopped-before-");
    records::append_project(&before, None, "writer:q", "evidence_limit", &APP_WRITER, body("Q's entry")).unwrap();
    let q = attach(&before, false).unwrap().project.unwrap();
    let after = before.with_file_name(format!("{}-moved", before.file_name().unwrap().to_string_lossy()));
    std::fs::rename(&before, &after).unwrap();
    let store = opened().unwrap().0;
    append_line(&store.join("roots.jsonl"), &json!({"format":ROOT_FORMAT,"formatVersion":VERSION,"projectId":q,"root":before.display().to_string(),"at":now_rfc3339(),"how":"released","by":"adopt"})).unwrap();
    let stopped = attach(&after, false).unwrap();
    // Review round 2, finding 6: known history with no folder recorded is
    // "records kept, not attached", never a project with no records: it
    // refuses (the earlier expectation, no refusal, was that defect).
    assert!(stopped.dir.is_none(), "{stopped:?}");
    assert!(stopped.refusal.as_deref().is_some_and(|r| r.starts_with("records kept, not attached")), "{stopped:?}");
    assert_eq!((stopped.how, stopped.fault, stopped.resolutions.as_slice(), stopped.linked.as_deref()), ("unattached", Some("no folder recorded"), ["adopt"].as_slice(), Some(q.as_str())));
    let view = status(Some(&after));
    assert_eq!(view["project"]["attachment"]["resolutions"], json!(["adopt"]));
    assert_ne!(view["project"]["reading"], "no records yet", "{view}");
    assert!(view["project"]["reading"].as_str().unwrap().starts_with("records kept in the records store"), "{view}");
    // No supplier is admitted for it, and the App's opening attach does not
    // register the folder on its link alone: nothing is written.
    let roots_before = std::fs::read(store.join("roots.jsonl")).unwrap();
    let supplier = crate::records_retention::activity(&after).err().expect("no supplier admitted");
    assert!(supplier.starts_with("records kept, not attached"), "{supplier}");
    let opening = attach(&after, true).unwrap();
    assert!(opening.dir.is_none() && opening.fault == Some("no folder recorded"), "{opening:?}");
    assert!(records::append_project(&after, None, "writer:q", "evidence_limit", &APP_WRITER, body("not Q's until confirmed")).is_err());
    assert_eq!(std::fs::read(store.join("roots.jsonl")).unwrap(), roots_before, "nothing registered");
    assert_eq!(adopt(&after).unwrap()["projectId"], q.as_str());
    let done = attach(&after, false).unwrap();
    assert_eq!(done.project.as_deref(), Some(q.as_str()));
    assert!(done.resolutions.is_empty() && done.fault.is_none());
    assert_eq!(storage::read_all(&after).0.len(), 1, "Q's history");
    // A folder with a link to an identity the store does not hold at all is offered nothing of the kind.
    let unknown = folder("stopped-unknown-");
    std::fs::create_dir_all(unknown.join(".chirality")).unwrap();
    std::fs::write(unknown.join(PROJECT_LINK), serde_json::to_vec(&link_value("chirality-project:never-held", &opened().unwrap().1)).unwrap()).unwrap();
    let none = attach(&unknown, false).unwrap();
    assert!(none.resolutions.is_empty() && none.fault.is_none(), "{none:?}");
    let _ = (std::fs::remove_dir_all(&after), std::fs::remove_dir_all(&unknown));
}

/// Review round 2, finding 7, as App Agent 0 decided it: an incomplete last
/// line of the roots registry is said on every attachment and in status, its
/// bytes are kept exactly, records are read from what the complete lines
/// associate, and nothing is written, minted, adopted or restored.
#[test]
fn a_torn_roots_registry_reads_from_its_complete_lines_and_writes_nothing() {
    let _store = OwnStore::new();
    let known = folder("torn-known-");
    records::append_project(&known, None, "writer:p", "evidence_limit", &APP_WRITER, body("P's entry")).unwrap();
    let p = attach(&known, false).unwrap().project.unwrap();
    let store = opened().unwrap().0;
    let registry = store.join("roots.jsonl");
    // An incomplete line, as an interrupted append leaves it.
    let mut torn = std::fs::read(&registry).unwrap();
    torn.extend_from_slice(br#"{"format":"chirality.records-store.root","formatVersion":"0.1","projectId":"chirality-project:torn-fixture","root":"#);
    std::fs::write(&registry, &torn).unwrap();
    // The associated folder reads, with the limit, and is not writable.
    let a = attach(&known, false).unwrap();
    assert_eq!(a.project.as_deref(), Some(p.as_str()));
    assert!(a.view()["registry"].as_str().is_some_and(|r| r.contains("was not read whole")), "{a:?}");
    assert!(a.resolutions.is_empty());
    assert_eq!(storage::read_all(&known).0.len(), 1, "P's records are read");
    let view = status(Some(&known));
    assert!(view["registry"].as_str().is_some_and(|r| r.contains("was not read whole")), "{view}");
    assert!(view["project"]["attachment"]["registry"].as_str().is_some(), "{view}");
    assert!(view["project"]["notes"].as_array().unwrap().iter().any(|n| n.as_str().is_some_and(|n| n.contains("was not read whole"))), "{view}");
    let refused = records::append_project(&known, None, "writer:p", "evidence_limit", &APP_WRITER, body("not while torn")).unwrap_err();
    assert!(refused.contains("was not read whole"), "{refused}");
    let supplier = crate::records_retention::activity(&known).err().expect("no supplier admitted");
    assert!(supplier.contains("was not read whole"), "{supplier}");
    for act in [restore_link(&known), new_identity(&known), adopt(&known)] {
        let e = act.unwrap_err();
        assert!(e.contains("was not read whole"), "{e}");
    }
    // A folder its complete lines do not associate: association not known,
    // nothing minted, linked or registered.
    let unknown = folder("torn-unknown-");
    let b = attach(&unknown, true).unwrap();
    assert_eq!((b.how, b.fault), ("unattached", Some("association not known")), "{b:?}");
    assert!(b.refusal.as_deref().is_some_and(|r| r.contains("was not read whole")) && b.resolutions.is_empty() && b.dir.is_none());
    assert!(records::append_project(&unknown, None, "writer:b", "evidence_limit", &APP_WRITER, body("not minted")).is_err());
    assert!(!unknown.join(PROJECT_LINK).exists(), "no identity minted");
    assert_eq!(status(Some(&unknown))["project"]["reading"], "nothing from the records store (association not known)");
    for act in [new_identity(&unknown), adopt(&unknown)] { assert!(act.is_err()); }
    assert_eq!(storage::read_all(&known).0.len(), 1, "nothing written for P");
    assert_eq!(std::fs::read(&registry).unwrap(), torn, "the registry's bytes, torn tail included, are kept exactly");
    let _ = (std::fs::remove_dir_all(&known), std::fs::remove_dir_all(&unknown));
}

/// Review rounds 3 and 4, as App Agent 0 decided.
///
/// The form. Ordinary readers take the place a project's records are read
/// from one decision (`readable_home`, `ReadHome`), which gives none for a
/// refused attachment; writers take theirs from `write_dir`; the connector
/// accounts' place is built from the decision. ONE READER IS THE EXCEPTION:
/// the fleet reader (`fleet_records.rs`, DEL-06-01) must create nothing, so
/// it does not take its place from the decision; it keeps association checks
/// of its own before it builds the protected folder, and its own test holds
/// what it does with the link removed or changed.
///
/// What this test is: a limited check that fails when selected source lines
/// change. It reads physical lines of the product's Rust files and holds, by
/// full line content and with multiplicity, (1) the lines that contain one
/// of nine names of a records location in the project folder; (2) the lines
/// outside the store module that contain `records_store::` followed by the
/// name of one of nine functions of the store that return a store path or an
/// attachment without the decision; (3) the lines outside the store module
/// that begin with `use` and contain `records_store`; and it fails for
/// (4) a line outside the store module where one of those nine names is
/// followed at once by an opening bracket and is not part of a path, a
/// method call or a definition. "The store module" is `records_store.rs` and
/// the files named by a line `#[path = "..."]` in it or in them, test files
/// apart; that list of five files is held here too.
///
/// What it is not, and what it is known to miss (review round 5; App Agent 0
/// decided that the test stays as it is and claims no more than this). It
/// does not enforce the architecture, and it is not a complete list of who
/// can obtain a location. It does not see: a `use` item spread over several
/// lines; a call written with a space before its bracket; a path attribute
/// written without spaces or with a comment inside it; `include!`; an
/// out-of-line module declared beside a file that a path attribute brought
/// in; a re-export inside the store's own files; a new function of the
/// store that returns a location, a wrapper included; what a macro produces;
/// a location built with none of the nine names from a path a caller passes
/// in; an unchanged listed line whose argument now comes from somewhere
/// else; a comment line; a file that is not Rust; and test files, those
/// named `tests.rs` or ending `_tests.rs`. Review and the behavioural tests
/// establish the permitted use. What ends the need for it is making the
/// store's path functions private, which is the binding pull request's
/// first item. Reformatting a listed line fails it, by design: the digest is
/// then updated with its reason unchanged.
#[test]
fn selected_source_lines_about_where_a_projects_records_are_read_are_held_by_content() {
    type Held = BTreeMap<String, Vec<(usize, String)>>;
    fn walk(dir: &std::path::Path, base: &std::path::Path, files: &mut Vec<(String, String)>) {
        for entry in std::fs::read_dir(dir).unwrap() {
            let path = entry.unwrap().path();
            if path.is_dir() {
                walk(&path, base, files);
                continue;
            }
            let name = path.strip_prefix(base).unwrap().to_string_lossy().into_owned();
            if name.ends_with(".rs") && !name.ends_with("_tests.rs") && !name.ends_with("/tests.rs") && name != "tests.rs" {
                files.push((name, std::fs::read_to_string(&path).unwrap()));
            }
        }
    }
    fn scan(files: &[(String, String)], selected: &dyn Fn(&str) -> bool, leave_out: &[&str]) -> Held {
        let mut held = Held::new();
        for (file, text) in files.iter().filter(|(file, _)| !leave_out.contains(&file.as_str())) {
            let lines: Vec<(usize, String)> = text.lines().enumerate()
                .filter(|(_, line)| !line.trim_start().starts_with("//") && selected(line))
                .map(|(i, line)| (i + 1, line.to_owned())).collect();
            if !lines.is_empty() {
                held.insert(file.clone(), lines);
            }
        }
        held
    }
    fn digest(lines: &[(usize, String)]) -> String {
        crate::util::sha256_hex(lines.iter().map(|(_, line)| line.as_str()).collect::<Vec<_>>().join("\n").as_bytes())[..16].to_owned()
    }
    fn differences(what: &str, held: &Held, allowed: &[(&str, &str, &str)]) -> Vec<String> {
        let mut wrong = Vec::new();
        for (file, lines) in held {
            let shown = lines.iter().map(|(number, line)| format!("    {number}: {line}")).collect::<Vec<_>>().join("\n");
            match allowed.iter().find(|(name, _, _)| name == file) {
                None => wrong.push(format!("{file} {what} and is not on the list (digest {}):\n{shown}", digest(lines))),
                Some((_, expected, why)) if *expected != digest(lines) => wrong.push(format!("{file}: its lines that {what} are not the ones listed (digest now {}; the list holds {expected}: {why}):\n{shown}", digest(lines))),
                Some(_) => {}
            }
        }
        for (file, _, _) in allowed {
            if !held.contains_key(*file) {
                wrong.push(format!("{file} is on the list and no longer {what}; take it off"));
            }
        }
        wrong
    }
    let base = std::path::Path::new(env!("CARGO_MANIFEST_DIR")).join("src");
    let mut files = Vec::new();
    walk(&base, &base, &mut files);

    // "The store module" is these files: `records_store.rs` and every file a
    // line `#[path = "..."]` in it or in them names, test files apart. Other
    // ways a file can be brought in are not seen.
    const STORE_MODULE: [&str; 7] = ["records_package.rs", "records_package_controls.rs", "records_package_identity.rs", "records_package_import.rs", "records_store.rs", "records_store_lines.rs", "records_store_witness.rs"];
    let mut module = std::collections::BTreeSet::from(["records_store.rs".to_owned()]);
    let mut pending = vec!["records_store.rs".to_owned()];
    while let Some(file) = pending.pop() {
        let text = std::fs::read_to_string(base.join(&file)).unwrap();
        for line in text.lines() {
            if let Some(path) = line.trim().strip_prefix("#[path = \"").and_then(|rest| rest.strip_suffix("\"]")) {
                if !path.ends_with("_tests.rs") && module.insert(path.to_owned()) {
                    pending.push(path.to_owned());
                }
            }
        }
    }
    assert_eq!(module.iter().map(String::as_str).collect::<Vec<_>>(), STORE_MODULE, "the files that path attributes name in the store module changed: a file inside it may call the store's path functions freely, so the list is held");
    assert!(!base.join("records_store").exists(), "a records_store folder would add files to the store module without a path attribute");

    // 1. Who names a records location in the project folder.
    let names: Vec<String> = ["LEGACY_RECORDS", "LEGACY_LOG", "CAPTURES", "CAPTURE_STORE", "LEGACY_DIRECTORY",
        ".chirality/records", ".chirality/captures", "records/coordination.rs.jsonl", "\".chirality\""].iter().map(|n| n.to_string()).collect();
    const NAMED: [(&str, &str, &str); 11] = [
        ("records_store.rs", "71a9fb0ca2a91b13", "the one decision (ReadHome and the in-project accounts place), the import's census of what an earlier build left in the folder, and the folder the project link is written in"),
        ("storage.rs", "6ca4d68f984fcdfc", "the three names' definitions, the library's own act log and capture folder, and checks of the shape of a path already in hand"),
        ("connector_route_store.rs", "9e740a8128ab3c84", "the accounts folder's name and two comparisons of a path recorded in an account; the place itself comes from records_store::route_accounts_place"),
        ("act_control.rs", "9e08f8f561e55d16", "the A15 capture store's name and the library act log's recorded name: an A15 capture stays with its library"),
        ("act_control_a15.rs", "da4e32e280c2997c", "the library's own capture store (A15 stays with its library) and that module's tests"),
        ("file_act_root.rs", "b1d22e53205c6f8d", "a test's assertion that nothing was created"),
        ("fleet_records.rs", "13517bd392d9bced", "the census of the project's .chirality folder for the fleet view (DEL-06-01): project content, not a records location"),
        ("native_conversation_links.rs", "3f3917ac2f8c8a96", "the folder of the fleet copy published in the project: not a records location"),
        ("runtime_session.rs", "fd4d53d25c23d18a", "test fixtures"),
        ("workflow_library.rs", "56cb3f772daa84bf", "the workflow supply folder"),
        ("workflow_package_copy.rs", "2914ac79a2f7c182", "the workflow package copy folder"),
    ];
    let mut wrong = differences("names a records location in the project folder", &scan(&files, &|line: &str| names.iter().any(|n| line.contains(n.as_str())), &[]), &NAMED);

    // 2. Who, outside the store module, calls a function of the store that
    // returns a store path or an attachment without the decision.
    const FUNCTIONS: [&str; 9] = ["known_identity_for_read", "store_root", "configured_project_dir", "project_dir_of", "root_for_dir", "project_dir", "legacy_census", "read_log_path", "attach"];
    // `name` at `at` in `line` is that whole identifier (not part of a longer one).
    fn whole(line: &str, at: usize, name: &str) -> bool {
        !line[at + name.len()..].chars().next().is_some_and(|c| c.is_alphanumeric() || c == '_')
    }
    // By its `records_store::` path, called or passed.
    let qualified = |line: &str| FUNCTIONS.iter().any(|f| {
        let path = format!("records_store::{f}");
        line.match_indices(path.as_str()).any(|(at, _)| whole(line, at, &path))
    });
    // Called bare: the name, then `(`, not part of a path, a method or a longer name, and not its own definition.
    let bare = |line: &str| FUNCTIONS.iter().any(|f| {
        line.match_indices(*f).any(|(at, _)| whole(line, at, f) && line[at + f.len()..].starts_with('(')
            && !line[..at].chars().next_back().is_some_and(|c| c.is_alphanumeric() || c == '_' || c == ':' || c == '.')
            && !line[..at].trim_end().ends_with("fn"))
    });
    const CALLERS: [(&str, &str, &str); 14] = [
        ("fleet_records.rs", "7f59d78278e1388b", "the fleet reader (DEL-06-01), the one reader on this list: it must create nothing, so it does not attach; it compares the opened store's identity, then makes the association checks itself (the registry read strictly; exactly one project for the folder and no other folder for that project; the link present, of its format, naming that project and this store), and takes the store folder only after all of them pass. A missing, changed, duplicated or moved link, records kept with no folder, and a registry not read whole each refuse before the folder is taken"),
        ("file_act_arrival.rs", "2b3c14e9a624fea5", "the arrival preview pins the store's own root (its identity and an opened handle) beside the records folder its binding gave it; it takes no project's folder from the store's root"),
        ("file_act_lapse.rs", "bac1affed8c258c9", "the lapse observer pins the identity of the store's root it began with, beside the home it takes from the decision"),
        ("records_export.rs", "55d23a7524f88b16", "export refuses a destination inside the store's root; the project's folder it exports comes from the decision"),
        ("records_retention.rs", "61c7d3cfd6140ced", "administration and admission: for a path already in hand, the project store folder it lies in, to take that project's admission (no folder is read through it); and the activity lease and the retention acts take the attachment and themselves refuse a refused one, an identity limit and an unread registry"),
        ("storage.rs", "48623ca56512f990", "all of a path already in hand: its label for presentation, its sync boundary, its records root, and the project root its store folder was opened from for a writer; none gives a reader a place for a project"),
        ("file_act_view.rs", "e74763194a74bba7", "the folder a log path already in hand lies in, as the base for reading that log"),
        ("records.rs", "85c289c7b5d8b971", "the appender takes the writer lock of the store folder a log path already in hand lies in"),
        ("records_access.rs", "519c5024fe3afbe5", "the records capability's own read log, a writer: its path in the project's store folder, refused with the read when the attachment gives none"),
        ("role_observations.rs", "c024537e4e6f86bd", "the census of files kept in the project folder, read only to REFUSE role observation history while an import is needed; and a writer taking the project's identity from the attachment (none for a refused one)"),
        ("role_record_source.rs", "b7a86f4abea1daee", "the role source takes the project's identity from the attachment, to refuse a reference that belongs to another project; no place is taken"),
        ("workflow_record_store.rs", "b1cc7691732bfd74", "the workflow record store's read admission takes the attachment and returns its refusal for a refused one before anything is read"),
        ("native_conversation_links.rs", "58c2472c29734ec3", "the native relationship writer captures the attachment it will write under and refuses a refusal"),
        ("lib.rs", "49b753d2e7327969", "the App at startup gives the opened project its identity (a minting attachment), a writer"),
    ];
    let mut callers = scan(&files, &qualified, &STORE_MODULE);
    // Calls inside test modules of product files: fixtures, held with the rest.
    for (file, why) in [("act_control_a15.rs", "a test's assertion"), ("runtime_session.rs", "test fixtures")] {
        if let Some(lines) = callers.remove(file) {
            let expected = match file { "act_control_a15.rs" => "0e4d960a46572bf6", _ => "678c9810d8ef831b" };
            if digest(&lines) != expected {
                wrong.push(format!("{file} ({why}): its calls of the store's path functions changed (digest now {}):\n{}", digest(&lines), lines.iter().map(|(n, l)| format!("    {n}: {l}")).collect::<Vec<_>>().join("\n")));
            }
        }
    }
    wrong.extend(differences("calls a function of the store that returns a store path or an attachment without the decision", &callers, &CALLERS));

    // 3. The lines outside the store module that begin with `use` and name
    // the store. A `use` item spread over several lines is not seen.
    const IMPORTS: [(&str, &str, &str); 6] = [
        ("fleet_records.rs", "6e895d82e9a7f87f", "the module itself, with others; every use of it in this file is by its records_store:: path"),
        ("desktop_startup.rs", "0681da416c9617cc", "the module itself, in a test module"),
        ("lib.rs", "d771fd5d21ed7367", "an alias for the store's package custody submodule (records_package), which has none of the listed functions"),
        ("records_retention.rs", "3f8a677a36c99b49", "the module itself, with others; every use of it in this file is by its records_store:: path"),
        ("role_observations.rs", "2283fd61370d8a40", "the module itself, with others; every use of it in this file is by its records_store:: path"),
        ("storage.rs", "6ba69ddb5abdef78", "the module itself, with others; every use of it in this file is by its records_store:: path"),
    ];
    let imports = scan(&files, &|line: &str| { let line = line.trim_start(); (line.starts_with("use ") || line.starts_with("pub use ") || line.starts_with("pub(crate) use ")) && line.contains("records_store") }, &STORE_MODULE);
    wrong.extend(differences("imports from the records store by a use line", &imports, &IMPORTS));
    // 4. A listed function's name followed at once by an opening bracket,
    // outside the store module. A space before the bracket is not seen.
    for (file, lines) in scan(&files, &bare, &STORE_MODULE) {
        wrong.push(format!("{file} calls, by a bare name, something named as one of the store's path functions is; if it is that function, this file is not among the listed callers:\n{}", lines.iter().map(|(n, l)| format!("    {n}: {l}")).collect::<Vec<_>>().join("\n")));
    }
    assert!(wrong.is_empty(), "a project's records are read where records_store::readable_home says, and written where records_store::write_dir says. A new reader takes its place from the ReadHome that decision returns (it refuses for a refused attachment). Only where a line is none of that (a library's own store, a writer, administration, a test, a shape check) is this list changed, with the reason said:\n{}", wrong.join("\n"));
    // The decision itself: a refused attachment is an error, with nothing to read in place.
    let root = folder("decision-refused-");
    records::append_project(&root, None, "writer:d", "evidence_limit", &APP_WRITER, body("in the store")).unwrap();
    assert!(readable_home(&root).unwrap().in_store().is_some());
    std::fs::remove_file(root.join(PROJECT_LINK)).unwrap();
    let refused = readable_home(&root).unwrap_err();
    assert!(refused.starts_with("project records unavailable: link missing; not attached") && refused.ends_with("the files kept in the project folder are not read in their place"), "{refused}");
    assert!(route_accounts_place(&root, false).unwrap_err().contains("link missing; not attached"));
    // A folder that is simply new reads in place, as before.
    let fresh = folder("decision-new-");
    let read = readable_home(&fresh).unwrap();
    assert!(read.in_store().is_none() && read.records() == fresh.join(".chirality/records") && read.captures() == fresh.join(".chirality/captures"));
    assert_eq!(read.registered_log(), fresh.join("records/coordination.rs.jsonl"));
    assert_eq!(read.in_place_parts("workflow"), Some(vec![".chirality", "records", "workflow"]));
    let _ = (std::fs::remove_dir_all(&root), std::fs::remove_dir_all(&fresh));
}

/// Pull requests 240 and 246 together, for the merge of the two: a refused
/// attachment (240) and an import account that cannot be read (246) each
/// refuse on the merged path, and so do both at once. The attachment's
/// refusal is said first; nothing either made an error becomes a reading;
/// and no write, import or export is admitted in any of the three states.
#[test]
fn a_refused_attachment_and_an_unknown_import_account_each_refuse_and_so_do_both() {
    let _own = OwnStore::new();
    let unknown = |e: &str| e.contains("exists and is empty") && e.contains("whether an import was begun is not known");
    let refused = |e: &str| e.contains("link missing; not attached");
    let root = legacy_project();
    import(&root).unwrap();
    let dir = attach(&root, false).unwrap().dir.unwrap();
    let link = std::fs::read(root.join(PROJECT_LINK)).unwrap();
    let account = std::fs::read(dir.join("imports.jsonl")).unwrap();
    let run_log = |root: &Path| crate::records::supply::run_log_for_read(root, "run:legacy");
    let export_to = |root: &Path| {
        let destination = folder("both-refusals-export-").join("bag");
        let result = crate::records_export::export(root, &destination);
        (result, destination)
    };
    let store_before = |dir: &Path| (std::fs::read(dir.join("imports.jsonl")).unwrap(), std::fs::read_dir(dir).unwrap().count());
    // Neither: read from the store.
    assert!(readable_home(&root).unwrap().in_store().is_some());
    assert!(route_accounts_place(&root, false).unwrap().store_dir.is_some());
    assert!(run_log(&root).is_ok());
    assert_eq!(status(Some(&root))["project"]["reading"], "records store");
    assert_eq!(storage::read_all(&root).0.len(), 3);

    // 1. The account unknown, the attachment whole (246's refusal alone).
    std::fs::write(dir.join("imports.jsonl"), b"").unwrap();
    let before = store_before(&dir);
    for said in [
        readable_home(&root).map(|_| ()).unwrap_err(),
        route_accounts_place(&root, false).map(|_| ()).unwrap_err(),
        route_accounts_place(&root, true).map(|_| ()).unwrap_err(),
        run_log(&root).map(|_| ()).unwrap_err(),
        write_dir(&root).map(|_| ()).unwrap_err(),
        import(&root).map(|_| ()).unwrap_err(),
    ] {
        assert!(unknown(&said), "{said}");
    }
    let shown = status(Some(&root));
    assert_eq!(shown["project"]["state"], "unavailable", "{shown}");
    assert!(shown["project"]["reading"].as_str().is_none_or(|r| r != "records store" && r != "no records yet" && !r.contains("in place")), "{shown}");
    let (entries, limits) = storage::read_all(&root);
    assert!(entries.is_empty() && limits.iter().any(|l| unknown(l)), "{entries:?} {limits:?}");
    let (exported, destination) = export_to(&root);
    assert!(exported.is_err() && !destination.exists(), "{exported:?}");
    assert!(records::append_project(&root, None, "writer:both", "evidence_limit", &APP_WRITER, body("refused")).is_err());
    assert_eq!(store_before(&dir), before, "nothing written in the project's store folder");

    // 2. Both: the link removed as well. The attachment's refusal is the one
    // said, and nothing is read in place of the store's records.
    std::fs::remove_file(root.join(PROJECT_LINK)).unwrap();
    for said in [
        readable_home(&root).map(|_| ()).unwrap_err(),
        route_accounts_place(&root, false).map(|_| ()).unwrap_err(),
        route_accounts_place(&root, true).map(|_| ()).unwrap_err(),
        run_log(&root).map(|_| ()).unwrap_err(),
        write_dir(&root).map(|_| ()).unwrap_err(),
    ] {
        assert!(refused(&said), "{said}");
    }
    assert!(import(&root).is_err());
    let shown = status(Some(&root));
    assert_eq!(shown["project"]["reading"], "nothing from the records store (the project is not attached)", "{shown}");
    assert_eq!(shown["project"]["importNeeded"], false, "{shown}");
    let (entries, limits) = storage::read_all(&root);
    assert!(entries.is_empty() && limits.iter().any(|l| refused(l)), "{entries:?} {limits:?}");
    let (exported, destination) = export_to(&root);
    assert!(exported.is_err() && !destination.exists(), "{exported:?}");
    assert!(records::append_project(&root, None, "writer:both", "evidence_limit", &APP_WRITER, body("refused")).is_err());
    assert!(!root.join(PROJECT_LINK).exists(), "no identity minted for it");
    assert_eq!(store_before(&dir), before, "nothing written in the project's store folder");

    // 3. The attachment refused, the account whole (240's refusal alone).
    std::fs::write(dir.join("imports.jsonl"), &account).unwrap();
    for said in [
        readable_home(&root).map(|_| ()).unwrap_err(),
        route_accounts_place(&root, false).map(|_| ()).unwrap_err(),
        run_log(&root).map(|_| ()).unwrap_err(),
        write_dir(&root).map(|_| ()).unwrap_err(),
    ] {
        assert!(refused(&said), "{said}");
    }
    let (entries, _) = storage::read_all(&root);
    assert!(entries.is_empty(), "{entries:?}");
    let (exported, destination) = export_to(&root);
    assert!(exported.is_err() && !destination.exists(), "{exported:?}");

    // The link put back with the account whole: it reads as at the start.
    std::fs::write(root.join(PROJECT_LINK), &link).unwrap();
    assert!(readable_home(&root).unwrap().in_store().is_some());
    assert_eq!(storage::read_all(&root).0.len(), 3);
    assert_eq!(status(Some(&root))["project"]["reading"], "records store");
    let _ = std::fs::remove_dir_all(&root);
}

/// Review round 3, finding 3: with the registry's last line incomplete and
/// its complete lines recording the folder for several projects, no identity
/// act is offered, as none is on any other path while the tail is unread.
#[test]
fn several_identities_beside_an_incomplete_registry_tail_offer_no_identity_act() {
    let _store = OwnStore::new();
    let here = folder("torn-several-");
    records::append_project(&here, None, "writer:p", "evidence_limit", &APP_WRITER, body("P's entry")).unwrap();
    let store = opened().unwrap().0;
    let registry = store.join("roots.jsonl");
    let mut bytes = std::fs::read(&registry).unwrap();
    let second = json!({"format":"chirality.records-store.root","formatVersion":"0.1","projectId":"chirality-project:second-fixture","root":here.to_str().unwrap(),"at":"2026-11-12T00:00:00Z","how":"attached"});
    bytes.extend_from_slice(format!("{second}\n").as_bytes());
    std::fs::write(&registry, &bytes).unwrap();
    // Whole registry: the fault, with the acts that resolve it offered.
    let whole = attach(&here, false).unwrap();
    assert_eq!(whole.fault, Some("several identities"), "{whole:?}");
    assert!(whole.registry.is_none() && !whole.resolutions.is_empty(), "{whole:?}");
    // The reviewer's state: the same lines, then an incomplete one.
    bytes.extend_from_slice(b"{");
    std::fs::write(&registry, &bytes).unwrap();
    let torn = attach(&here, false).unwrap();
    assert_eq!(torn.fault, Some("several identities"), "{torn:?}");
    assert!(torn.registry.is_some(), "{torn:?}");
    assert!(torn.resolutions.is_empty(), "no act is offered that the host would refuse: {torn:?}");
    assert!(status(Some(&here))["project"]["attachment"]["resolutions"].as_array().is_some_and(|r| r.is_empty()));
    for act in [new_identity(&here), adopt(&here)] { assert!(act.unwrap_err().contains("was not read whole")); }
    assert_eq!(std::fs::read(&registry).unwrap(), bytes);
    let _ = std::fs::remove_dir_all(&here);
}

/// Review round 3, finding 5: something that is not a plain file where the
/// registry belongs is reported, by status and by an attachment, and is
/// never waited on.
#[test]
fn a_registry_that_is_not_a_plain_file_is_reported_without_waiting() {
    let own = OwnStore::new();
    let here = folder("fifo-registry-");
    records::append_project(&here, None, "writer:p", "evidence_limit", &APP_WRITER, body("P's entry")).unwrap();
    let store = opened().unwrap().0;
    let registry = store.join("roots.jsonl");
    std::fs::remove_file(&registry).unwrap();
    let name = std::ffi::CString::new(registry.as_os_str().as_encoded_bytes()).unwrap();
    assert_eq!(unsafe { libc::mkfifo(name.as_ptr(), 0o600) }, 0);
    let (done, wait) = std::sync::mpsc::channel();
    let (project, configured) = (here.clone(), own.0.clone());
    std::thread::spawn(move || {
        // The test's store is chosen per thread.
        use_store_for_test(Some(Ok(Store { root: configured, placement: Placement::Override, limits: vec![] })));
        let _ = done.send((status(None), status(Some(&project)), attach(&project, false).map(|_| ())));
    });
    let (store_view, project_view, attached) = wait.recv_timeout(std::time::Duration::from_secs(5)).expect("status and attachment return; nothing waits on the registry");
    assert!(store_view["registry"].as_str().is_some_and(|r| r.contains("records store unreadable: roots.jsonl")), "{store_view}");
    assert!(project_view["registry"].as_str().is_some_and(|r| r.contains("records store unreadable: roots.jsonl")), "{project_view}");
    assert!(attached.unwrap_err().contains("records store unreadable"));
    std::fs::remove_file(&registry).unwrap();
    let _ = std::fs::remove_dir_all(&here);
}

/// Review round 2, finding 1, case (b), as containment: with P's activity
/// held (a supplier or a record waiting to be written), P's moved folder is
/// not adopted elsewhere, so a write for the old path is refused there and
/// nothing is minted under another identity.
#[test]
fn a_moved_project_is_not_adopted_while_its_activity_is_held() {
    let before = folder("held-before-");
    records::append_project(&before, None, "writer:p", "evidence_limit", &APP_WRITER, body("P's entry")).unwrap();
    let p = attach(&before, false).unwrap().project.unwrap();
    let held = crate::records_retention::activity(&before).unwrap().expect("P's activity lease");
    let after = before.with_file_name(format!("{}-moved", before.file_name().unwrap().to_string_lossy()));
    std::fs::rename(&before, &after).unwrap();
    let store = opened().unwrap().0;
    let roots_before = std::fs::read(store.join("roots.jsonl")).unwrap();
    let refused = adopt(&after).unwrap_err();
    assert!(refused.contains(&format!("project {p}")) && refused.contains("is still in use") && refused.ends_with("nothing changed"), "{refused}");
    assert_eq!(std::fs::read(store.join("roots.jsonl")).unwrap(), roots_before, "nothing released or registered");
    // The old path made again: a write kept for it is refused, nothing minted.
    std::fs::create_dir_all(&before).unwrap();
    assert!(records::append_project(&before, None, "writer:p", "evidence_limit", &APP_WRITER, body("P's waiting entry")).is_err());
    assert!(!before.join(PROJECT_LINK).exists(), "no identity minted at the old path");
    assert_eq!(std::fs::read(store.join("roots.jsonl")).unwrap(), roots_before);
    drop(held);
    std::fs::remove_dir_all(&before).unwrap();
    assert_eq!(adopt(&after).unwrap()["projectId"], p.as_str());
    assert_eq!(storage::read_all(&after).0.len(), 1, "P's history");
    let _ = std::fs::remove_dir_all(&after);
}

#[test]
fn a_copied_project_is_duplicated_and_attaches_nothing_until_it_gets_its_own_identity() {
    let original = folder("dup-original-");
    records::append_project(&original, None, "writer:dup", "evidence_limit", &APP_WRITER, body("original")).unwrap();
    let id = attach(&original, false).unwrap().project.unwrap();
    let copy = folder("dup-copy-");
    std::fs::create_dir_all(copy.join(".chirality")).unwrap();
    std::fs::copy(original.join(PROJECT_LINK), copy.join(PROJECT_LINK)).unwrap();
    let dup = attach(&copy, true).unwrap();
    assert!(dup.dir.is_none() && dup.refusal.as_deref().unwrap().contains("duplicated project identity"), "{dup:?}");
    assert_eq!((dup.fault, dup.resolutions.as_slice()), (Some("duplicated"), ["new-identity"].as_slice()));
    let refused = records::append_project(&copy, None, "writer:dup", "evidence_limit", &APP_WRITER, body("copy")).unwrap_err();
    assert!(refused.contains("duplicated"), "{refused}");
    assert_eq!(storage::read_all(&copy).0.len(), 0, "the copy reads none of the original's records");
    assert!(adopt(&copy).unwrap_err().contains("another folder holds this project identity"));
    // The person gives the copy its own identity.
    let fresh = new_identity(&copy).unwrap()["projectId"].as_str().unwrap().to_owned();
    assert_ne!(fresh, id);
    records::append_project(&copy, None, "writer:dup", "evidence_limit", &APP_WRITER, body("copy")).unwrap();
    assert_eq!(storage::read_all(&copy).0.len(), 1);
    assert_eq!(storage::read_all(&original).0.len(), 1, "the original is unaffected");
    assert_eq!(attach(&original, false).unwrap().project.as_deref(), Some(id.as_str()));
    let _ = (std::fs::remove_dir_all(&original), std::fs::remove_dir_all(&copy));
}

#[test]
fn a_moved_project_is_attached_only_when_the_person_confirms_it() {
    let before = folder("moved-before-");
    records::append_project(&before, None, "writer:move", "evidence_limit", &APP_WRITER, body("before the move")).unwrap();
    let id = attach(&before, false).unwrap().project.unwrap();
    let after = before.with_file_name(format!("{}-moved", before.file_name().unwrap().to_string_lossy()));
    std::fs::rename(&before, &after).unwrap();
    let moved = attach(&after, true).unwrap();
    assert!(moved.dir.is_none() && moved.refusal.as_deref().unwrap().contains("adopt"), "{moved:?}");
    assert_eq!((moved.fault, moved.resolutions.as_slice()), (Some("moved"), ["adopt", "new-identity"].as_slice()));
    assert!(records::append_project(&after, None, "writer:move", "evidence_limit", &APP_WRITER, body("x")).is_err());
    assert_eq!(adopt(&after).unwrap()["projectId"], id.as_str());
    assert_eq!(storage::read_all(&after).0.len(), 1, "the project's history, in the store");
    records::append_project(&after, None, "writer:move", "evidence_limit", &APP_WRITER, body("after the move")).unwrap();
    assert_eq!(storage::read_all(&after).0.len(), 2);
    let _ = std::fs::remove_dir_all(&after);
}

#[test]
fn a_project_kept_in_another_store_and_an_unreadable_link_attach_nothing() {
    let root = folder("other-store-");
    std::fs::create_dir_all(root.join(".chirality")).unwrap();
    std::fs::write(root.join(PROJECT_LINK), serde_json::to_vec(&link_value("chirality-project:elsewhere", "records-store:another")).unwrap()).unwrap();
    let other = attach(&root, true).unwrap();
    assert!(other.refusal.as_deref().unwrap().contains("another records store"), "{other:?}");
    assert_eq!((other.fault, other.resolutions.as_slice()), (Some("another store"), ["adopt", "new-identity"].as_slice()));
    assert!(storage::project_log(&root, None, "w").is_err());
    assert_eq!(adopt(&root).unwrap()["projectId"], "chirality-project:elsewhere");
    let link: Value = serde_json::from_slice(&std::fs::read(root.join(PROJECT_LINK)).unwrap()).unwrap();
    assert_eq!(link["storeId"], opened().unwrap().1.as_str(), "the link now names this store");
    assert!(storage::project_log(&root, None, "w").is_ok());
    // An unreadable link on a folder the store does not know: nothing minted.
    let broken = folder("broken-link-");
    std::fs::create_dir_all(broken.join(".chirality")).unwrap();
    std::fs::write(broken.join(PROJECT_LINK), b"not json").unwrap();
    let refused = storage::project_log(&broken, None, "w").unwrap_err();
    assert!(refused.contains("unreadable") && refused.contains("nothing minted"), "{refused}");
    assert_eq!(std::fs::read(broken.join(PROJECT_LINK)).unwrap(), b"not json");
    assert!(listed(&roots(&opened().unwrap().0).unwrap(), broken.to_str().unwrap()).is_empty());
    let _ = (std::fs::remove_dir_all(&root), std::fs::remove_dir_all(&broken));
}

// ---- A read writes nothing ----

/// One call of the agents' records capability, as the App offers it.
fn capability_read(root: &Path) -> Result<(), String> {
    let cap = crate::records_access::RecordsCapability::new(root)?;
    let call = crate::records_access::Call { app_session: "app-session:fixture".into(), generation: "g:fixture".into(), request: json!(1), thread: "thread".into(), turn: "turn".into(),
        call: crate::util::opaque_id("call-")?, arguments: json!({"operation":"list_runs"}) };
    let answer = cap.answer(&call, Some(root.to_str().unwrap()));
    if answer["success"] != true { return Err(answer.to_string()); }
    // An answer that says the records are unavailable is a refusal here.
    let page: Value = serde_json::from_str(answer["contentItems"][0]["text"].as_str().unwrap_or("{}")).unwrap_or_default();
    match page["limits"].as_array() {
        Some(limits) if limits.iter().any(|l| l.as_str().is_some_and(|l| l.contains("unavailable"))) => Err(page["limits"].to_string()),
        _ => Ok(()),
    }
}
/// Readers outside the store's own module that a test only inventories (the
/// fleet view belongs to DEL-06-01): their answers are not judged here.
fn read_beside(root: &Path) {
    let _ = crate::fleet_records::read_for_workspace(Some(root));
    let _ = status(Some(root));
    let _ = storage::read_all(root);
}
/// The entries below `dir`, relative to it, with a derived query cache named by
/// its pattern (`indexes/query-<key of the project root>-*.sqlite`).
fn names(dir: &Path, project: &Path) -> std::collections::BTreeSet<String> {
    let key = format!("query-{}-", crate::util::sha256_hex(project.as_os_str().as_encoded_bytes()));
    tree(dir).keys().map(|p| {
        let rel = p.strip_prefix(dir).unwrap().to_string_lossy().into_owned();
        match rel.strip_prefix("indexes/") {
            Some(file) if file.starts_with(&key) && file.ends_with(".sqlite") => "indexes/query-<project>-*.sqlite".to_owned(),
            _ => rel,
        }
    }).collect()
}
/// Derived query caches for `project` left in the temporary folder.
fn temporary_caches(project: &Path) -> Vec<PathBuf> {
    let key = format!("query-{}-", crate::util::sha256_hex(project.as_os_str().as_encoded_bytes()));
    let mut out = Vec::new();
    for dir in [std::env::temp_dir(), PathBuf::from("/tmp"), PathBuf::from("/var/tmp")] {
        for entry in std::fs::read_dir(dir).into_iter().flatten().flatten() {
            if entry.file_name().to_string_lossy().starts_with(&key) { out.push(entry.path()); }
        }
    }
    out
}
/// As a new App process: nothing opened, no index held.
fn new_process() {
    crate::records_index::close_all();
    *OPENED.lock().unwrap() = None;
    *ROOTS.lock().unwrap() = None;
    DIRS.lock().unwrap().clear();
}

/// Every entry below `dir`, with each file's bytes (a folder: None).
fn tree(dir: &Path) -> BTreeMap<PathBuf, Option<Vec<u8>>> {
    let mut out = BTreeMap::new();
    let mut todo = vec![dir.to_path_buf()];
    while let Some(at) = todo.pop() {
        for entry in std::fs::read_dir(&at).unwrap() {
            let path = entry.unwrap().path();
            if std::fs::symlink_metadata(&path).unwrap().is_dir() { out.insert(path.clone(), None); todo.push(path); }
            else { out.insert(path.clone(), Some(std::fs::read(&path).unwrap())); }
        }
    }
    out
}
/// Every reader the App's views and commands reach: the store's own, the
/// records index and its chain report, the decision view, role and workflow
/// reads, and the agents' records capability. `Err` carries what the reader
/// said when it could not read; an answer that hides a failure is an `Err`
/// here too.
fn read_everything(root: &Path) -> Vec<Result<(), String>> {
    let failed = |limits: &Value| match limits.as_array() { Some(l) if !l.is_empty() => Err(Value::Array(l.clone()).to_string()), _ => Ok(()) };
    vec![
        crate::records_index::with_index(root, |ix| if ix.limits().is_empty() { Ok(()) } else { Err(ix.limits().join("; ")) }),
        { let heads = crate::records_index::chain_heads(root); if heads["discoveryLimit"].is_null() { Ok(()) } else { Err(heads["discoveryLimit"].to_string()) } },
        failed(&crate::decision_view::derive(root, &[])["limits"]),
        crate::role_observations::project_chain_head(root).map(|_| ()),
        crate::workflow_workspace::publication::ProjectRecords::open(root).and_then(|p| p.source_binding().map(|_| ())),
        capability_read(root),
        opened().map(|_| ()),
        opened_existing().map(|_| ()),
        attach(root, false).map(|_| ()),
        home(root).map(|_| ()),
        // Connector accounts of a folder with no link are read in place when
        // there is no store: that is an answer only if it says so and names
        // no store folder.
        route_accounts_place(root, false).and_then(|place| if place.store_dir.is_some() { Ok(()) } else { Err(format!("no store root: {}", place.location)) }),
        read_log_path(root).map(|_| ()),
        store_root().map(|_| ()).ok_or_else(|| "no store root".to_string()),
        (status(Some(root))["state"] == "available").then_some(()).ok_or_else(|| status(Some(root))["error"].to_string()),
        storage::discover(root).map(|_| ()),
    ]
}

#[test]
fn a_read_of_a_store_that_does_not_exist_creates_nothing_and_says_so() {
    let base = folder("unborn-base-");
    let root = folder("unborn-project-");
    let absent = base.join("store");
    use_store_not_started_for_test(Some(Ok(Store { root: absent.clone(), placement: Placement::Override, limits: vec![] })));
    for (index, outcome) in read_everything(&root).into_iter().enumerate() {
        let refused = outcome.err().unwrap_or_else(|| panic!("reader {index} answered for a store that does not exist"));
        assert!(refused.contains("not created yet") || refused.contains("no store root") || refused.contains("records store unavailable"), "{refused}");
    }
    assert!(!absent.exists(), "no reader created the store folder");
    assert_eq!(status(None)["state"], "unavailable", "a store that could not be opened is never shown as available");
    // An existing but empty folder: no identity and no bootstrap lock appear.
    std::fs::create_dir(&absent).unwrap();
    for outcome in read_everything(&root) { assert!(outcome.is_err()); }
    read_beside(&root);
    assert!(tree(&absent).is_empty(), "{:?}", tree(&absent).keys());
    assert!(tree(&root).is_empty(), "nothing written in the project either");
    // Not "empty": the read says the store is not there.
    let (entries, limits) = storage::read_all(&root);
    assert!(entries.is_empty() && limits.iter().any(|l| l.contains("not created yet")), "{limits:?}");
    read_beside(&root);
    assert!(tree(&absent).is_empty(), "{:?}", tree(&absent).keys());
    assert!(temporary_caches(&root).is_empty(), "no cache in the temporary folder: {:?}", temporary_caches(&root));
    // The App's start, or a writer, creates it; then the same readers read it.
    create_at_startup().unwrap();
    assert!(absent.join("store.json").is_file());
    assert!(opened().is_ok() && attach(&root, false).unwrap().how == "none");
    use_store_for_test(None);
    for p in [base, root] { let _ = std::fs::remove_dir_all(p); }
}

#[test]
fn a_read_through_a_store_alias_redirected_mid_way_writes_nothing_and_never_follows_it() {
    use std::os::unix::fs::symlink;
    let base = folder("alias-base-");
    let root = folder("alias-project-");
    let (real, empty, alias) = (base.join("real"), base.join("empty"), base.join("alias"));
    std::fs::create_dir(&real).unwrap();
    std::fs::create_dir(&empty).unwrap();
    symlink(&real, &alias).unwrap();
    use_store_for_test(Some(Ok(Store { root: alias.clone(), placement: Placement::Override, limits: vec![] })));
    records::append_project(&root, None, "writer:alias", "evidence_limit", &APP_WRITER, body("in the real store")).unwrap();
    let (opened_root, store_id) = opened().unwrap();
    assert_eq!(opened_root, real);
    assert_eq!(storage::read_all(&root).0.len(), 1);
    let project_folder = attach(&root, false).unwrap().dir.unwrap();
    let before = tree(&real);
    // Warm: this process opened the store. The alias now names an empty folder.
    std::fs::remove_file(&alias).unwrap();
    symlink(&empty, &alias).unwrap();
    for outcome in read_everything(&root) { outcome.unwrap(); }
    assert_eq!(opened().unwrap(), (real.clone(), store_id.clone()), "still bound to the physical store it opened");
    assert_eq!(storage::read_all(&root).0.len(), 1, "and reads its records there");
    assert!(tree(&empty).is_empty(), "nothing written through the redirected alias: {:?}", tree(&empty).keys());
    // Cold: another process (no opened store) reads through the redirected
    // alias. It finds no store there, refuses, and creates nothing.
    use_store_not_started_for_test(Some(Ok(Store { root: alias.clone(), placement: Placement::Override, limits: vec![] })));
    *OPENED.lock().unwrap() = None;
    *ROOTS.lock().unwrap() = None;
    for outcome in read_everything(&root) {
        let refused = outcome.unwrap_err();
        assert!(refused.contains("not created yet") || refused.contains("no store root"), "{refused}");
    }
    assert!(tree(&empty).is_empty(), "no identity, lock or folder created by a read: {:?}", tree(&empty).keys());
    assert_eq!(status(Some(&root))["state"], "unavailable", "never shown as an empty, healthy store");
    // The redirect is not healed by reading; nothing in the real store changed
    // apart from what its own readers keep (compared file by file).
    let after = tree(&real);
    // Only what a read is permitted to leave (the pinned list): the derived
    // query cache and the records read log of the capability's calls.
    let permitted = |p: &Path| p.starts_with(real.join("indexes")) || p.starts_with(project_folder.join("reads"));
    for (path, bytes) in before.iter().filter(|(p, _)| !permitted(p)) { assert_eq!(after.get(path), Some(bytes), "{}", path.display()); }
    let added: Vec<_> = after.keys().filter(|p| !before.contains_key(*p) && !permitted(p)).collect();
    assert!(added.is_empty(), "files created in the store by reads: {added:?}");
    use_store_for_test(None);
    *OPENED.lock().unwrap() = None;
    for p in [base, root] { let _ = std::fs::remove_dir_all(p); }
}

/// The readers a view or command reaches, by name.
const READERS: [&str; 8] = ["read_all", "index", "chain_heads", "decision_view", "role", "workflow", "status", "capability"];
/// One reader's answer, as a value to compare.
fn answer(root: &Path, name: &str) -> Value {
    let ok = |r: Result<Value, String>| r.unwrap_or_else(|e| json!({"refused": e}));
    match name {
        "read_all" => { let (entries, limits) = storage::read_all(root); json!({"entries": entries, "limits": limits}) }
        "index" => crate::records_index::with_index(root, |ix| json!({"paths": ix.paths(), "limits": ix.limits(), "partials": ix.partials(), "chains": ix.chains(),
            "acts": ix.act_claims().unwrap_or_else(|e| vec![json!({"refused": e})]), "entries": ix.entries_with("rec:app:store-0").unwrap_or_default(),
            "holds": ix.holds("rec:app:store-0"), "holdsNot": ix.holds("rec:app:nothing")})),
        "chain_heads" => crate::records_index::chain_heads(root),
        "decision_view" => crate::decision_view::derive(root, &[]),
        "role" => ok(crate::role_observations::project_chain_head(root).map(|h| json!(h))),
        "workflow" => ok(crate::workflow_workspace::publication::ProjectRecords::open(root).and_then(|p| p.source_binding().map(|_| Value::Null))),
        "status" => status(Some(root)),
        "capability" => ok(capability_read(root).map(|_| Value::Null)),
        _ => unreachable!(),
    }
}
fn answers(root: &Path) -> BTreeMap<&'static str, Value> {
    READERS.iter().map(|name| (*name, answer(root, name))).collect()
}
/// A project with a few records in two run logs, written by the App's writer.
fn written_project(prefix: &str) -> PathBuf {
    let root = folder(prefix);
    for n in 0..3 {
        records::append_project_reserved(&root, if n == 2 { "run:a" } else { "run:b" }, "writer:store", "evidence_limit", &APP_WRITER,
            body(&format!("entry {n}")), &format!("rec:app:store-{n}"), "2026-11-12T00:00:00.000Z").unwrap();
    }
    root
}

#[test]
fn a_read_whose_store_alias_is_redirected_between_two_of_its_steps_writes_nothing_there() {
    use std::os::unix::fs::symlink;
    use std::sync::{atomic::{AtomicBool, Ordering}, Arc};
    let base = folder("mid-read-alias-");
    let (real, replacement, alias) = (base.join("real"), base.join("replacement"), base.join("alias"));
    std::fs::create_dir(&real).unwrap();
    symlink(&real, &alias).unwrap();
    use_store_for_test(Some(Ok(Store { root: alias.clone(), placement: Placement::Override, limits: vec![] })));
    let root = written_project("mid-read-project-");
    // The worst replacement: a folder holding a copy of the store's identity.
    std::fs::create_dir(&replacement).unwrap();
    std::fs::copy(real.join("store.json"), replacement.join("store.json")).unwrap();
    let only_identity = tree(&replacement);
    let point = |to: &Path| { std::fs::remove_file(&alias).unwrap(); symlink(to, &alias).unwrap(); };
    // Each reader's answer in a new process with no redirect...
    new_process();
    let expected = answers(&root);
    for (name, answer) in &expected { assert!(answer.get("refused").is_none(), "{name} answered: {answer}"); }
    assert_eq!(expected["read_all"]["entries"].as_array().unwrap().len(), 3);
    // ...then again, the alias redirected to the replacement right after the
    // read's first step bound the store, before its next steps.
    for name in READERS {
        point(&real);
        new_process();
        let fired = Arc::new(AtomicBool::new(false));
        let (flag, to, at) = (fired.clone(), replacement.clone(), alias.clone());
        after_open_for_test(Some(Box::new(move || {
            std::fs::remove_file(&at).unwrap();
            symlink(&to, &at).unwrap();
            flag.store(true, Ordering::SeqCst);
        })));
        let got = answer(&root, name);
        after_open_for_test(None);
        assert!(fired.load(Ordering::SeqCst), "{name}: the redirect happened inside the read");
        assert_eq!(std::fs::read_link(&alias).unwrap(), replacement, "{name}");
        // The read stayed with the store it bound: the same answer, and
        // nothing created, locked or repaired in the folder now named.
        if name != "status" { assert_eq!(got, expected[name], "{name}"); }
        else { assert_eq!((got["state"].as_str(), &got["root"], &got["storeId"]), (Some("available"), &expected[name]["root"], &expected[name]["storeId"]), "{got}"); }
        assert_eq!(tree(&replacement), only_identity, "{name} wrote into the redirected alias: {:?}", tree(&replacement).keys());
        assert!(temporary_caches(&root).is_empty(), "{name} put a cache in the temporary folder: {:?}", temporary_caches(&root));
    }
    after_open_for_test(None);
    use_store_for_test(None);
    new_process();
    for p in [base, root] { let _ = std::fs::remove_dir_all(p); }
}

#[test]
fn a_cold_first_read_creates_only_the_pinned_files_below_an_existing_store_and_nothing_for_an_absent_one() {
    let own = OwnStore::new();
    let store = own.0.clone();
    // A store the App created at its start, with a project the App's writer
    // opened and wrote, and a folder the store has never seen.
    let written = written_project("cold-written-");
    let unseen = folder("cold-unseen-");
    for (root, expected) in [
        (&written, vec!["indexes", "indexes/query-<project>-*.sqlite", "projects/<project>/reads", "projects/<project>/reads/records-reads.jsonl"]),
        (&unseen, vec!["indexes", "indexes/query-<project>-*.sqlite"]),
    ] {
        new_process();
        if let Ok(dir) = std::fs::read_dir(store.join("indexes")) { for e in dir.flatten() { let _ = std::fs::remove_file(e.path()); } }
        let _ = std::fs::remove_dir(store.join("indexes"));
        let (store_before, project_before) = (names(&store, root), tree(root));
        let temporary_before = temporary_caches(root);
        for _ in read_everything(root) {}
        read_beside(root);
        let key = attach(root, false).unwrap().dir.map(|d| d.file_name().unwrap().to_string_lossy().into_owned());
        let created: Vec<String> = names(&store, root).difference(&store_before)
            .map(|n| key.as_ref().map_or(n.clone(), |k| n.replace(k.as_str(), "<project>"))).collect();
        // The pinned list: the derived query cache (and its folder), and for
        // a project with an identity, the records read log the capability's
        // read writes (DEL-04-03 REQ-011, AC-012). Nothing else.
        assert_eq!(created, expected, "{}", root.display());
        assert_eq!(tree(root), project_before, "nothing written in the project");
        assert_eq!(temporary_caches(root), temporary_before, "no cache in the temporary folder");
        // The cache is the process's own: it goes when the index is released.
        crate::records_index::close_all();
        assert!(!names(&store, root).iter().any(|n| n.ends_with(".sqlite")), "{:?}", names(&store, root));
    }
    // An absent store: nothing at all, here or in the temporary folder.
    let base = folder("cold-absent-base-");
    let absent = base.join("store");
    use_store_not_started_for_test(Some(Ok(Store { root: absent.clone(), placement: Placement::Override, limits: vec![] })));
    new_process();
    for root in [&written, &unseen] {
        for outcome in read_everything(root) { assert!(outcome.is_err()); }
        read_beside(root);
    }
    assert!(tree(&base).is_empty(), "{:?}", tree(&base).keys());
    assert!(temporary_caches(&written).is_empty() && temporary_caches(&unseen).is_empty());
    drop(own);
    new_process();
    for p in [base, written, unseen] { let _ = std::fs::remove_dir_all(p); }
}

#[test]
fn a_store_folder_replaced_at_its_path_is_refused_by_the_reading_and_the_creating_opening() {
    let own = OwnStore::new();
    let store = own.0.clone();
    let root = written_project("replaced-store-project-");
    let (_, id) = opened().unwrap();
    let moved = store.with_extension("moved");
    std::fs::rename(&store, &moved).unwrap();
    std::fs::create_dir(&store).unwrap();
    std::fs::copy(moved.join("store.json"), store.join("store.json")).unwrap();
    let only_identity = tree(&store);
    for refused in [opened().unwrap_err(), opened_existing().unwrap_err(), created().unwrap_err(), create_at_startup().unwrap_err()] {
        assert!(refused.contains("replaced by another folder"), "{refused}");
    }
    let writes = [
        records::append_project(&root, None, "writer:store", "evidence_limit", &APP_WRITER, body("after the replacement")).map(|_| ()),
        attach(&root, true).map(|_| ()),
        storage::project_log(&root, None, "w").map(|_| ()),
        import(&root).map(|_| ()),
    ];
    for write in writes { assert!(write.unwrap_err().contains("replaced by another folder")); }
    // Each reader says why (store_root's helper here has only "no store root").
    for read in read_everything(&root) { let e = read.unwrap_err(); assert!(e.contains("replaced") || e == "no store root", "{e}"); }
    assert_eq!(status(Some(&root))["state"], "unavailable");
    assert_eq!(tree(&store), only_identity, "nothing read into, written in or minted in the replacement: {:?}", tree(&store).keys());
    // The store itself, put back, is the store again.
    std::fs::remove_dir_all(&store).unwrap();
    std::fs::rename(&moved, &store).unwrap();
    assert_eq!(opened().unwrap().1, id);
    drop(own);
    let _ = std::fs::remove_dir_all(root);
}

#[test]
fn a_replaced_identity_file_is_refused_until_the_app_opens_the_store_afresh() {
    let own = OwnStore::new();
    let store = own.0.clone();
    let root = written_project("replaced-identity-project-");
    let (_, id) = opened().unwrap();
    // The same identity, put back as a new file (as a restore from a backup does).
    let bytes = std::fs::read(store.join("store.json")).unwrap();
    std::fs::remove_file(store.join("store.json")).unwrap();
    std::fs::write(store.join("store.json"), &bytes).unwrap();
    for refused in [opened().unwrap_err(), created().unwrap_err(), records::append_project(&root, None, "writer:store", "evidence_limit", &APP_WRITER, body("refused")).unwrap_err()] {
        assert!(refused.contains("identity file") && refused.contains("was replaced since this App opened the store")
            && refused.contains("nothing is read or written through it") && refused.contains("reopening the App opens the store afresh"), "{refused}");
    }
    // A new process opens the same folder with the same valid identity afresh.
    new_process();
    assert_eq!(opened().unwrap(), (store.clone(), id));
    assert_eq!(storage::read_all(&root).0.len(), 3);
    records::append_project(&root, None, "writer:store", "evidence_limit", &APP_WRITER, body("after reopening")).unwrap();
    drop(own);
    new_process();
    let _ = std::fs::remove_dir_all(root);
}

#[test]
fn an_index_read_writes_nothing_into_a_folder_put_in_place_of_its_store() {
    let own = OwnStore::new();
    let store = own.0.clone();
    let root = written_project("replaced-index-project-");
    assert!(crate::records_index::chain_heads(&root)["discoveryLimit"].is_null());
    let moved = store.with_extension("moved");
    std::fs::rename(&store, &moved).unwrap();
    std::fs::create_dir(&store).unwrap();
    std::fs::copy(moved.join("store.json"), store.join("store.json")).unwrap();
    let only_identity = tree(&store);
    // A new index for this process: its cache would be opened now.
    crate::records_index::close_all();
    let heads = crate::records_index::chain_heads(&root);
    assert!(heads["discoveryLimit"].as_str().is_some_and(|l| l.contains("replaced")), "{heads}");
    assert!(heads["notes"].as_array().unwrap().iter().any(|n| n.as_str().is_some_and(|n| n.contains("query cache not written"))), "{heads}");
    let limits = crate::records_index::with_index(&root, |ix| ix.limits());
    assert!(limits.iter().any(|l| l.contains("replaced")), "{limits:?}");
    assert_eq!(tree(&store), only_identity, "no indexes/ or cache in the replacement: {:?}", tree(&store).keys());
    assert!(temporary_caches(&root).is_empty());
    std::fs::remove_dir_all(&store).unwrap();
    std::fs::rename(&moved, &store).unwrap();
    drop(own);
    new_process();
    let _ = std::fs::remove_dir_all(root);
}

#[test]
fn deleting_the_index_cache_changes_no_answer_only_its_speed() {
    let own = OwnStore::new();
    let store = own.0.clone();
    let root = written_project("dispensable-cache-");
    let first = answers(&root);
    assert!(store.join("indexes").is_dir());
    // Removed while the process holds its index: the same answers.
    std::fs::remove_dir_all(store.join("indexes")).unwrap();
    assert_eq!(answers(&root), first);
    // Removed in a new process: the same answers.
    new_process();
    std::fs::remove_dir_all(store.join("indexes")).unwrap();
    assert_eq!(answers(&root), first);
    // A cache that cannot be written at all: the sources are read directly,
    // with the same answers, and the chain report says so in its notes.
    new_process();
    std::fs::remove_dir_all(store.join("indexes")).unwrap();
    std::fs::write(store.join("indexes"), b"not a folder").unwrap();
    let without = answers(&root);
    let notes = |a: &BTreeMap<&str, Value>| a["chain_heads"]["notes"].clone();
    assert!(notes(&without).as_array().unwrap().iter().any(|n| n.as_str().is_some_and(|n| n.contains("query cache not written") && n.contains("read directly"))), "{}", notes(&without));
    let strip = |mut a: BTreeMap<&'static str, Value>| { a.get_mut("chain_heads").unwrap()["notes"] = json!(null); a };
    assert_eq!(strip(without), strip(first.clone()));
    assert_eq!(std::fs::read(store.join("indexes")).unwrap(), b"not a folder");
    std::fs::remove_file(store.join("indexes")).unwrap();
    drop(own);
    new_process();
    let _ = std::fs::remove_dir_all(root);
}

#[test]
fn a_reader_creates_no_admission_control_and_records_without_one_are_unavailable() {
    let own = OwnStore::new();
    let store = own.0.clone();
    let root = written_project("admission-project-");
    let dir = attach(&root, false).unwrap().dir.unwrap();
    let control = store.join("administration").join(dir.file_name().unwrap()).join(".admission.lock");
    assert!(control.is_file(), "the writer made the project's admission control");
    std::fs::remove_file(&control).unwrap();
    let before = tree(&store);
    // The role and workflow reads take a reader's admission: with no control
    // beside the records they say so, and make none.
    for refused in [crate::role_observations::project_chain_head(&root).map(|_| ()), crate::workflow_workspace::publication::ProjectRecords::open(&root).unwrap().source_binding().map(|_| ())] {
        let refused = refused.unwrap_err();
        assert!(refused.contains("admission control") && refused.contains("missing"), "{refused}");
    }
    assert!(!control.exists());
    let after = tree(&store);
    let added: Vec<_> = after.keys().filter(|p| !before.contains_key(*p) && !p.starts_with(store.join("indexes"))).collect();
    assert!(added.is_empty(), "{added:?}");
    // A capability read must be recorded, and its read-log write is admitted
    // only through a control that exists: with the whole administration
    // folder gone it is refused, and nothing is made in its place.
    std::fs::remove_dir_all(store.join("administration")).unwrap();
    let before = tree(&store);
    let refused = capability_read(&root).unwrap_err();
    assert!(refused.contains("admission control"), "{refused}");
    assert!(!store.join("administration").exists(), "a read re-creates no control");
    let added: Vec<_> = tree(&store).keys().filter(|p| !before.contains_key(*p) && !p.starts_with(store.join("indexes"))).cloned().collect();
    assert!(added.is_empty(), "{added:?}");
    // A project with nothing in the store has nothing to read and nothing to hold.
    let nothing = project_dir(&store, "chirality-project:nothing-here");
    assert!(crate::records_retention::read_path(&nothing).unwrap().is_none());
    assert!(!store.join("administration").join(nothing.file_name().unwrap()).exists());
    // The writer, writing again, makes the control; the readers read.
    records::append_project(&root, None, "writer:store", "evidence_limit", &APP_WRITER, body("again")).unwrap();
    assert!(control.is_file());
    crate::role_observations::project_chain_head(&root).unwrap();
    crate::workflow_workspace::publication::ProjectRecords::open(&root).unwrap().source_binding().unwrap();
    drop(own);
    let _ = std::fs::remove_dir_all(root);
}

#[test]
fn an_unreadable_import_record_is_an_error_never_an_empty_history_or_the_kept_originals() {
    let own = OwnStore::new();
    // A project whose §13.7 originals were imported, and one with nothing in
    // place: each import record then becomes unreadable (a line that is not JSON).
    let imported = legacy_project();
    import(&imported).unwrap();
    let empty = folder("unknown-import-empty-");
    attach(&empty, true).unwrap();
    // "Cannot be read" is a rule, not a list: the account is read whole, and
    // nothing is concluded from one that is not. A line that is not JSON, a
    // value that is not an object, an empty object, an import line of
    // another version or event, a line without its identity or its files, a
    // file entry that is not one, a blank line, and a last line that is not
    // closed each make the account unknown.
    let listed: [&[u8]; 13] = [b"not json\n", b"{}\n", b"null\n", b"[]\n", b"null", b"{\"format\":", b"\n",
        b"{\"format\":\"chirality.records-store.import\",\"formatVersion\":\"0.1\",\"event\":\"completed\",\"importId\":\"import:review\",\"files\":[null]}\n",
        b"{\"format\":\"chirality.records-store.import\",\"formatVersion\":\"0.1\",\"importId\":\"import:review\",\"files\":[],\"conflicts\":[7]}\n",
        b"{\"format\":\"chirality.records-store.import\",\"formatVersion\":\"99.0\",\"event\":\"future\"}\n",
        b"{\"format\":\"chirality.records-store.import\",\"formatVersion\":\"0.1\",\"event\":\"future\",\"importId\":\"import:x\"}\n",
        b"{\"format\":\"chirality.records-store.import\",\"formatVersion\":\"0.1\",\"event\":\"completed\",\"importId\":\"import:x\"}\n",
        b"{\"format\":\"chirality.records-store.import\",\"formatVersion\":\"0.1\",\"event\":\"started\",\"census\":[]}\n"];
    // Review round 4, and the neighbouring contents asked of it: an account
    // that exists and is empty; contents in which nothing is parsed (a
    // byte-order mark, carriage returns, a NUL, spaces, with and without a
    // newline); and a line that IS a valid import line with something more
    // (a byte-order mark before it, a carriage return or a space after it, a
    // space before it, a key given twice, a byte that is not UTF-8).
    let valid = b"{\"format\":\"chirality.records-store.import\",\"formatVersion\":\"0.1\",\"event\":\"started\",\"importId\":\"import:edge\",\"census\":[]}".to_vec();
    assert_eq!(import_line(&serde_json::from_slice(&valid).unwrap()), Some("started"), "the line the edge contents are built on is a valid one");
    let around = |before: &[u8], after: &[u8]| [before, valid.as_slice(), after, b"\n"].concat();
    let twice = [&valid[..valid.len() - 1], b",\"event\":\"completed\",\"files\":[],\"conflicts\":[]}\n".as_slice()].concat();
    let not_utf8 = [&valid[..valid.len() - 2], b"\xff\"}\n".as_slice()].concat();
    let mut unknown: Vec<Vec<u8>> = listed.iter().map(|content| content.to_vec()).collect();
    unknown.extend([b"".to_vec(), b"\xef\xbb\xbf".to_vec(), b"\xef\xbb\xbf\n".to_vec(), b"\r".to_vec(), b"\r\n".to_vec(), b"\0".to_vec(), b"\0\n".to_vec(),
        b" ".to_vec(), b" \n".to_vec(), b"\n\n".to_vec(),
        around(b"\xef\xbb\xbf", b""), around(b"", b"\r"), around(b"", b" "), around(b" ", b""), around(b"\t", b"\t"), twice, not_utf8,
        [valid.as_slice(), b"\n\n"].concat(),
        // A valid line with a member no form of import line has.
        [&valid[..valid.len() - 1], b",\"added\":true}\n".as_slice()].concat()]);
    for (root, content) in [&imported, &empty].into_iter().flat_map(|root| unknown.iter().map(move |content| (root, content.as_slice()))) {
        let dir = attach(root, false).unwrap().dir.unwrap();
        std::fs::write(dir.join("imports.jsonl"), content).unwrap();
        let known = |e: &str| e.contains("unknown") && e.contains("import record is unreadable");
        let failed = home(root).unwrap_err();
        assert!(known(&failed), "{failed}");
        for (what, e) in [("discover", storage::discover(root).map(|_| ())), ("sources", storage::sources(root).map(|_| ())), ("capture_dir", storage::capture_dir(root).map(|_| ())),
            ("registered_legacy_log", storage::registered_legacy_log(root).map(|_| ())), ("route_accounts_place", route_accounts_place(root, false).map(|_| ())),
            ("write_dir", write_dir(root).map(|_| ())), ("export_permitted", export_permitted(&dir, root)),
            ("role", crate::role_observations::project_chain_head(root).map(|_| ())),
            ("workflow", crate::workflow_workspace::publication::ProjectRecords::open(root).and_then(|p| p.source_binding().map(|_| ())))] {
            let e = e.unwrap_err();
            // (The export's own refusal of an unclosed last line keeps its existing words.)
            assert!(known(&e) || e.contains("import state is unknown") || e.contains("import state has an unclosed final line"), "{what}: {e}");
        }
        // Never an empty or in-place history: the read and the views say why.
        let (entries, limits) = storage::read_all(root);
        assert!(entries.is_empty() && limits.iter().any(|l| known(l)), "{limits:?}");
        let decisions = crate::decision_view::derive(root, &[]);
        assert!(decisions["limits"].as_array().unwrap().iter().any(|l| l.as_str().is_some_and(known)), "{decisions}");
        let heads = crate::records_index::chain_heads(root);
        assert!(heads["discoveryLimit"].as_str().is_some_and(known), "{heads}");
        let shown = status(Some(root));
        assert_eq!(shown["project"]["state"], "unavailable", "{shown}");
        assert_ne!(shown["project"]["reading"], "no records yet");
        assert!(notes(root).iter().any(|n| known(n)), "{:?}", notes(root));
        assert!(capability_read(root).is_err(), "{:?}", capability_read(root));
    }
    // The valid line alone is read (an import begun and not completed), so
    // the refusals above are of what was added to it and of nothing else.
    for root in [&imported, &empty] {
        let dir = attach(root, false).unwrap().dir.unwrap();
        std::fs::write(dir.join("imports.jsonl"), around(b"", b"")).unwrap();
        assert!(home(root).is_ok(), "{:?}", home(root).err());
    }
    drop(own);
    for p in [imported, empty] { let _ = std::fs::remove_dir_all(p); }
}

/// Review round 5, as App Agent 0 decided it: the rule, held as a rule. Every
/// member the reader takes from an import line is checked for the form it is
/// taken as, and a wrong-typed value in any of them makes the account
/// unknown; the members it does not take are not checked, and a line lacking
/// them is accepted. The reviewer's state is the first: a `storeHeld` that is
/// neither true nor false was read as false, and a project whose records the
/// store held read its kept originals in place with no limit.
#[test]
fn every_member_the_reader_takes_from_an_import_line_is_checked_for_its_form_and_no_other_member_is() {
    let own = OwnStore::new();
    let root = folder("import-line-members-");
    let dir = attach(&root, true).unwrap().dir.unwrap();
    let account = dir.join("imports.jsonl");
    let put = |lines: &[&Value]| std::fs::write(&account, lines.iter().map(|l| format!("{l}\n")).collect::<String>()).unwrap();
    let entry = json!({"original":".chirality/records/acts.jsonl","copy":"acts/a.jsonl","sha256":"00","bytes":1,"stamp":{"size":1}});
    let started = json!({"format":"chirality.records-store.import","formatVersion":"0.1","event":"started","importId":"import:members","at":"2026-11-12T00:00:00.000Z",
        "root":"/invented","method":"sha-256 of the exact bytes","census":[entry.clone()],"storeHeld":true,"resumes":null});
    let completed = json!({"format":"chirality.records-store.import","formatVersion":"0.1","event":"completed","importId":"import:members","at":"2026-11-12T00:00:01.000Z",
        "files":[entry.clone()],"conflicts":[{"original":"records/coordination.rs.jsonl","reason":"invented"}],"censusChanged":[]});
    let mut earlier = completed.clone();
    for member in ["event", "censusChanged"] { earlier.as_object_mut().unwrap().remove(member); }
    earlier["root"] = json!("/invented");
    earlier["method"] = json!("sha-256 of the exact bytes");
    // The three forms as their writers give them are read.
    for (form, lines) in [("started", vec![&started]), ("started and completed", vec![&started, &completed]), ("no event", vec![&earlier])] {
        put(&lines);
        assert!(imports(&dir).is_ok(), "{form}: {:?}", imports(&dir).err());
    }
    // storeHeld is taken, and acted on: true means the store held the records.
    put(&[&started]);
    assert!(store_holds(&dir).unwrap(), "an unfinished import that began with the records in the store: read from the store");
    // Every taken member, in a form it is not taken as: the account is unknown.
    let with = |line: &Value, path: &[&str], value: Value| {
        let mut changed = line.clone();
        let mut at = &mut changed;
        for step in &path[..path.len() - 1] {
            at = match step.parse::<usize>() { Ok(index) => &mut at[index], Err(_) => &mut at[*step] };
        }
        at[path[path.len() - 1]] = value;
        changed
    };
    let wrong: Vec<(&str, Value)> = vec![
        ("the reviewer's state: storeHeld an object", with(&started, &["storeHeld"], json!({"not":"a boolean"}))),
        ("storeHeld a string", with(&started, &["storeHeld"], json!("true"))),
        ("storeHeld a number", with(&started, &["storeHeld"], json!(1))),
        ("storeHeld null", with(&started, &["storeHeld"], Value::Null)),
        ("a started line's at an object", with(&started, &["at"], json!({"unwritten":"object"}))),
        ("format a number", with(&started, &["format"], json!(1))),
        ("formatVersion a number", with(&started, &["formatVersion"], json!(0.1))),
        ("importId a number", with(&started, &["importId"], json!(7))),
        ("importId empty", with(&started, &["importId"], json!(""))),
        ("event a number", with(&started, &["event"], json!(7))),
        ("census an object", with(&started, &["census"], json!({}))),
        ("a census entry's original a number", with(&started, &["census", "0", "original"], json!(7))),
        ("a census entry's copy a number", with(&started, &["census", "0", "copy"], json!(7))),
        ("a census entry's sha256 a number", with(&started, &["census", "0", "sha256"], json!(7))),
        ("a census entry's bytes a string", with(&started, &["census", "0", "bytes"], json!("1"))),
        ("files an object", with(&completed, &["files"], json!({}))),
        ("a file entry's original a number", with(&completed, &["files", "0", "original"], json!(7))),
        ("a file entry's copy a number", with(&completed, &["files", "0", "copy"], json!(7))),
        ("a file entry's sha256 a number", with(&completed, &["files", "0", "sha256"], json!(7))),
        ("a file entry's bytes a fraction", with(&completed, &["files", "0", "bytes"], json!(1.5))),
        ("conflicts an object", with(&completed, &["conflicts"], json!({}))),
        ("a conflict's original a number", with(&completed, &["conflicts", "0", "original"], json!(7))),
        ("a conflict's reason a number", with(&completed, &["conflicts", "0", "reason"], json!(7))),
        ("the form with no event: a file entry's bytes a string", with(&earlier, &["files", "0", "bytes"], json!("1"))),
    ];
    for (what, line) in &wrong {
        put(&[line]);
        let refused = imports(&dir).err().unwrap_or_else(|| panic!("{what}: read as known"));
        assert!(refused.contains("is not an import line"), "{what}: {refused}");
        assert!(store_holds(&dir).is_err() && home(&root).is_err(), "{what}: never \"holds records\" and never \"no import\"");
    }
    // The members the reader does not take are not checked, and a line
    // lacking them is accepted: this is the boundary, stated, not a promise
    // that a line is one the App wrote.
    let mut bare = started.clone();
    for member in ["at", "root", "method", "storeHeld", "resumes"] { bare.as_object_mut().unwrap().remove(member); }
    let mut untaken = with(&with(&completed, &["at"], json!({"unwritten":"object"})), &["censusChanged"], json!(false));
    for (what, lines) in [("a started line lacking the members not taken, and storeHeld", vec![&bare]),
        ("root, method and resumes in other forms", vec![&with(&with(&with(&started, &["root"], json!(7)), &["method"], json!(7)), &["resumes"], json!(7))]),
        ("a completed line's at and censusChanged in other forms", vec![&started, &untaken]),
        ("a file entry's stamp in another form (compared as it stands)", vec![&started, &with(&completed, &["files", "0", "stamp"], json!("not a stamp"))])] {
        put(&lines);
        assert!(imports(&dir).is_ok(), "{what}: {:?}", imports(&dir).err());
    }
    untaken.as_object_mut().unwrap().remove("at");
    put(&[&started, &untaken]);
    assert!(imports(&dir).is_ok());
    drop(own);
    new_process();
    let _ = std::fs::remove_dir_all(root);
}

/// Review round 4: only an import account that is NOT THERE is "no import".
/// One that exists and is empty is unknown, as every other unreadable
/// account is: it cannot be told from an account emptied after an import.
/// The reviewer's three states: a newly attached project; an imported
/// project whose account is emptied; and an import begun, not completed,
/// whose account is then emptied, which must not give a verified export.
#[test]
fn an_import_account_that_exists_and_is_empty_is_unknown_and_only_a_missing_one_is_no_import() {
    let own = OwnStore::new();
    let known = |e: &str| e.contains("exists and is empty") && e.contains("whether an import was begun is not known");
    let export_to = |root: &Path| {
        let destination = folder("empty-account-export-").join("bag");
        let result = crate::records_export::export(root, &destination);
        (result, destination)
    };
    // A newly attached project with no account: no import, as before.
    let fresh = folder("empty-account-fresh-");
    let dir = attach(&fresh, true).unwrap().dir.unwrap();
    assert!(!dir.join("imports.jsonl").exists());
    assert_eq!(status(Some(&fresh))["project"]["reading"], "no records yet");
    std::fs::write(dir.join("imports.jsonl"), b"").unwrap();
    assert!(known(&home(&fresh).unwrap_err()));
    let shown = status(Some(&fresh));
    assert_eq!(shown["project"]["state"], "unavailable", "{shown}");
    assert_ne!(shown["project"]["reading"], "no records yet");
    let (entries, limits) = storage::read_all(&fresh);
    assert!(entries.is_empty() && limits.iter().any(|l| known(l)), "{limits:?}");
    assert!(write_dir(&fresh).is_err(), "nothing is written for it either");
    std::fs::remove_file(dir.join("imports.jsonl")).unwrap();
    assert_eq!(status(Some(&fresh))["project"]["reading"], "no records yet", "an account that is not there is no import");
    // An imported project: its account emptied.
    let imported = legacy_project();
    import(&imported).unwrap();
    let dir = attach(&imported, false).unwrap().dir.unwrap();
    assert_eq!(storage::read_all(&imported).0.len(), 3);
    let account = std::fs::read(dir.join("imports.jsonl")).unwrap();
    std::fs::write(dir.join("imports.jsonl"), b"").unwrap();
    let (entries, limits) = storage::read_all(&imported);
    assert!(entries.is_empty() && limits.iter().any(|l| known(l)), "the three entries are not read with no limit: {entries:?} {limits:?}");
    assert!(export_permitted(&dir, &imported).unwrap_err().contains("import state is unknown"));
    let (exported, destination) = export_to(&imported);
    assert!(exported.is_err() && !destination.exists(), "no export: {exported:?}");
    std::fs::write(dir.join("imports.jsonl"), &account).unwrap();
    assert_eq!(storage::read_all(&imported).0.len(), 3, "with its account back, it reads as before");
    // An import begun and not completed, then its account emptied: the
    // reviewer's "verified export created".
    let begun = legacy_project();
    interrupt_import_for_test(Some(1), false);
    let stopped = import(&begun);
    interrupt_import_for_test(None, false);
    assert!(stopped.unwrap_err().contains("interrupted"));
    let dir = attach(&begun, false).unwrap().dir.unwrap();
    assert!(std::fs::read(dir.join("imports.jsonl")).is_ok_and(|b| !b.is_empty()), "its started line is in the account");
    std::fs::write(dir.join("imports.jsonl"), b"").unwrap();
    assert!(known(&home(&begun).unwrap_err()));
    let (exported, destination) = export_to(&begun);
    assert!(exported.is_err() && !destination.exists(), "never a verified export: {exported:?}");
    drop(own);
    new_process();
    for p in [fresh, imported, begun] { let _ = std::fs::remove_dir_all(p); }
}

// ---- Existing records: explicit import ----

#[test]
fn records_in_the_project_are_read_in_place_and_recording_waits_for_import() {
    let root = legacy_project();
    let (entries, limits) = storage::read_all(&root);
    assert!(limits.is_empty(), "{limits:?}");
    assert_eq!(entries.len(), 3, "the §13.7 logs, read in place; the library's act log is not the project's set");
    let refused = records::append_project(&root, Some("run:new"), "writer:new", "evidence_limit", &APP_WRITER, body("new")).unwrap_err();
    assert!(refused.starts_with("import needed: 5 record file(s) in this project (1 WR workflow record(s), 2 capture file(s), 2 run/act log(s))"), "{refused}");
    assert!(storage::write_capture_dir(&root).unwrap_err().contains("import needed"));
    let status = status(Some(&root));
    assert_eq!(status["project"]["importNeeded"], true);
    assert_eq!(status["project"]["legacyFiles"], 5, "the A15 capture and the library log stay with the library");
    assert_eq!(status["project"]["notImported"], 5);
    // Nothing in the store yet: still read in place.
    assert_eq!(storage::read_all(&root).0.len(), 3);
    let _ = std::fs::remove_dir_all(&root);
}

#[test]
fn import_copies_byte_for_byte_verifies_counts_once_and_leaves_originals_alone() {
    let root = legacy_project();
    let census = legacy_census(&root).unwrap();
    let originals: Vec<(PathBuf, (Vec<u8>, Value))> = census.iter().map(|f| (f.original.clone(), bytes_and_stamp(&f.original))).collect();
    let library_capture = bytes_and_stamp(&root.join(".chirality/captures/bbbb.json"));
    let imported = import(&root).unwrap();
    assert_eq!((imported["state"].as_str(), imported["copied"].as_u64(), imported["alreadyPresent"].as_u64()), (Some("imported"), Some(5), Some(0)), "{imported}");
    let dir = attach(&root, false).unwrap().dir.unwrap();
    // Byte-identical copies, recorded with their SHA-256.
    // The started line names the whole census before any copy; the completed
    // line, last, is the commit point.
    let manifest = read_lines(&dir.join("imports.jsonl")).unwrap();
    assert_eq!((manifest.len(), manifest[0]["event"].as_str(), manifest[1]["event"].as_str()), (2, Some("started"), Some("completed")));
    assert_eq!(manifest[0]["importId"], manifest[1]["importId"]);
    assert_eq!(manifest[0]["census"].as_array().unwrap().len(), census.len());
    for file in &census {
        let copy = std::fs::read(dir.join(&file.copy)).unwrap();
        assert_eq!(copy, std::fs::read(&file.original).unwrap(), "{} copied byte for byte", file.rel);
        for line in &manifest {
            let list = if line["event"] == "started" { &line["census"] } else { &line["files"] };
            let recorded = list.as_array().unwrap().iter().find(|f| f["original"] == file.rel.as_str()).unwrap();
            assert_eq!(recorded["sha256"], sha256_hex(&copy));
        }
    }
    assert!(imported["standing"].as_str().unwrap().contains("only the trust of the project folder it came from"));
    // The originals are unchanged (bytes and file stamps), A15 evidence included.
    for (path, before) in &originals {
        assert_eq!(&bytes_and_stamp(path), before, "{}", path.display());
    }
    assert_eq!(bytes_and_stamp(&root.join(".chirality/captures/bbbb.json")), library_capture);
    assert!(!dir.join("captures/bbbb.json").exists(), "the A15 capture stays with its library");
    // Read from the store: each identity once, no duplicate, nothing pending.
    let (entries, limits) = storage::read_all(&root);
    assert!(limits.is_empty(), "{limits:?}");
    assert_eq!(entries.len(), 3);
    assert!(storage::discover(&root).unwrap().iter().all(|p| p.starts_with(&dir)), "only the store: the library's act log is not the project's set");
    assert!(notes(&root).is_empty(), "{:?}", notes(&root));
    let shown = status(Some(&root));
    assert_eq!((shown["project"]["reading"].as_str(), shown["project"]["importNeeded"].as_bool(), shown["project"]["notImported"].as_u64()), (Some("records store"), Some(false), Some(0)), "{shown}");
    // Recording resumes, in the store copy: the owning log continues its sequence.
    let next = records::append_project(&root, Some("run:legacy"), "writer:legacy", "evidence_limit", &APP_WRITER, body("after import")).unwrap();
    assert_eq!(next["seq"], 3);
    assert_eq!(bytes_and_stamp(&originals[0].0), originals[0].1, "the original run log is not written");
    // Idempotent: nothing more is copied or recorded.
    // The store copy of the run log has grown since; it is the owning log.
    let again = import(&root).unwrap();
    assert_eq!((again["copied"].as_u64(), again["alreadyPresent"].as_u64(), again["importId"].is_null()), (Some(0), Some(5), true), "{again}");
    assert_eq!(again["conflicts"], json!([]));
    assert_eq!(read_lines(&dir.join("imports.jsonl")).unwrap().len(), 2);

    let _ = std::fs::remove_dir_all(&root);
}

#[test]
fn an_original_that_differs_from_its_copy_is_a_limit_and_the_store_governs() {
    let root = legacy_project();
    import(&root).unwrap();
    let acts = root.join(".chirality/records").join(crate::recorder::LOG);
    // An agent (or an older App) writes to the original after import.
    let mut f = std::fs::OpenOptions::new().append(true).open(&acts).unwrap();
    std::io::Write::write_all(&mut f, b"{\"forged\":\"written to the original after import\"}\n").unwrap();
    let notes = notes(&root);
    assert!(notes.iter().any(|n| n.contains("differs from its imported copy") && n.contains("governs")), "{notes:?}");
    let (entries, limits) = storage::read_all(&root);
    assert!(limits.is_empty(), "drift is shown, never a reason to refuse recording: {limits:?}");
    assert!(entries.iter().all(|e| e.get("forged").is_none()), "the original is not read");
    let reimport = import(&root).unwrap();
    assert!(reimport["conflicts"][0]["reason"].as_str().unwrap().contains("differs from its imported copy"), "{reimport}");
    assert!(records::append_project(&root, None, "writer:x", "evidence_limit", &APP_WRITER, body("still recorded")).is_ok());
    // A §13.7 file that appears after import is not read, and does not refuse recording.
    let late = root.join(".chirality/records/acts/late.jsonl");
    std::fs::write(&late, b"{}\n").unwrap();
    assert!(super::notes(&root).iter().any(|n| n.contains("acts/late.jsonl") && n.contains("not imported")));
    assert!(records::append_project(&root, None, "writer:x", "evidence_limit", &APP_WRITER, body("still recorded")).is_ok());
    assert_eq!(std::fs::read(&late).unwrap(), b"{}\n");
    let _ = std::fs::remove_dir_all(&root);
}


#[test]
fn import_never_overwrites_a_different_copy_and_needs_an_identity() {
    let root = legacy_project();
    attach(&root, true).unwrap();
    let dir = attach(&root, false).unwrap().dir.unwrap();
    let copy = dir.join("workflow/11111111-1111-4111-8111-111111111111.json");
    std::fs::create_dir_all(copy.parent().unwrap()).unwrap();
    std::fs::write(&copy, b"{\"version\":1,\"other\":true}").unwrap();
    let imported = import(&root).unwrap();
    assert_eq!(imported["state"], "imported with conflicts");
    assert!(imported["conflicts"][0]["reason"].as_str().unwrap().contains("not overwritten"));
    assert_eq!(std::fs::read(&copy).unwrap(), b"{\"version\":1,\"other\":true}");
    // A folder whose identity cannot be attached imports nothing.
    let copy_project = folder("import-dup-");
    std::fs::create_dir_all(copy_project.join(".chirality")).unwrap();
    std::fs::copy(root.join(PROJECT_LINK), copy_project.join(PROJECT_LINK)).unwrap();
    assert!(import(&copy_project).unwrap_err().contains("nothing imported"));
    let _ = (std::fs::remove_dir_all(&root), std::fs::remove_dir_all(&copy_project));
}

#[test]
fn a_pending_capture_from_before_import_is_reconciled_from_the_store_copy() {
    // A capture, its pending submission (naming the §13.7 log) and its
    // record, written before the records store; the backlink was never added.
    let root = folder("pending-import-");
    let capture_id = "cap:pending-before-import";
    let capture = json!({"format":"chirality.aac.capture-evidence","formatVersion":"0.3","captureId":capture_id,"offerId":"offer:x",
        "offerDigest":{"method":"aac-offer-digest/0.1","value":"0".repeat(64)},"choice":"act","actKind":"A16","actor":{"osAccount":"fixture","identityVerified":false},
        "boundSubject":["decision package rec:app:req"],"boundContent":[{"method":crate::util::FILE_IDENTITY_METHOD,"value":"1".repeat(64)}],
        "scope":"s","purpose":"p","capturedAt":"2026-10-01T00:00:00.000Z","surface":"App interface","inputSource":"host-native-confirmation",
        "answers":{"standing":"no arrival: a standing act (RC-6)"},"requestRef":"rec:app:req","alternativeChosen":"ALT-1","evidenceLimits":["identity not verified"]});
    crate::schema_validation::validate_capture(&capture).unwrap();
    let legacy_log = format!(".chirality/records/{}", crate::recorder::LOG);
    let captures = root.join(".chirality/captures");
    std::fs::create_dir_all(captures.join("pending")).unwrap();
    let name = format!("{}.json", storage::key(capture_id));
    std::fs::write(captures.join(&name), serde_json::to_vec_pretty(&capture).unwrap()).unwrap();
    let record = records::append_with_id(&root.join(&legacy_log), "human_act", &records::APP_INTERFACE, crate::act_control::act_body(&capture), "rec:app:pending-before-import").unwrap();
    let pending = json!({"capture":capture,"recordId":record["recordId"],"log":legacy_log,"observedAt":capture["capturedAt"],"delayed":false});
    std::fs::write(captures.join("pending").join(&name), serde_json::to_vec_pretty(&pending).unwrap()).unwrap();
    let original_capture = std::fs::read(captures.join(&name)).unwrap();
    // Before import, recovery is held with its cause.
    let held = crate::act_control::ActControl::new(&root).recover_pending().unwrap_err();
    assert!(held.contains("import needed"), "{held}");

    import(&root).unwrap();
    let results = crate::act_control::ActControl::new(&root).recover_pending().unwrap();
    let recovered = results.iter().find(|r| r["capture"]["captureId"] == capture_id).unwrap_or_else(|| panic!("{results:?}"));
    assert_eq!(recovered["state"], "AC-7 recorded", "{recovered}");
    assert_eq!(recovered["record"]["recordId"], record["recordId"], "the one record, neither pending nor duplicated");
    let dir = attach(&root, false).unwrap().dir.unwrap();
    let linked: Value = serde_json::from_slice(&std::fs::read(dir.join("captures").join(&name)).unwrap()).unwrap();
    assert_eq!(linked["recordId"], record["recordId"], "the backlink is added to the store copy");
    assert_eq!(std::fs::read(captures.join(&name)).unwrap(), original_capture, "the original capture is not rewritten");
    assert_eq!(storage::read_all(&root).0.iter().filter(|e| e["kind"] == "human_act").count(), 1);
    let _ = std::fs::remove_dir_all(&root);
}

// ---- Readers read the store ----

#[test]
fn the_index_the_reader_and_the_records_capability_read_the_store() {
    use crate::records_access::RecordsSource;
    let root = folder("readers-project-");
    let written = records::append_project(&root, Some("run:r"), "writer:r", "evidence_limit", &APP_WRITER, body("in the store")).unwrap();
    let id = written["recordId"].as_str().unwrap();
    let dir = attach(&root, false).unwrap().dir.unwrap();
    assert!(!root.join(".chirality/records").exists(), "nothing written in the project but its link");
    assert!(crate::records_index::with_index(&root, |ix| ix.holds(id)));
    assert_eq!(storage::discover(&root).unwrap(), vec![dir.join(storage::log_rel(Some("run:r"), "writer:r"))]);
    let corpus = crate::records_access::ProjectPaths::new(&root).read();
    assert!(corpus.limits.is_empty(), "{:?}", corpus.limits);
    assert_eq!(corpus.entries.len(), 1);
    assert_eq!(corpus.entries[0].log, format!("records-store:{}", storage::log_rel(Some("run:r"), "writer:r")));
    assert_eq!(corpus.entries[0].entry["recordId"], id);
    assert_eq!(crate::decision_view::derive(&root, &[])["limits"], json!([]));
    let _ = std::fs::remove_dir_all(&root);
}

// ---- Review repairs (#1319): import commit point, attachment by link, library and legacy logs ----

#[test]
fn probe_r16_interrupted_import() {
    // The first of a five-file census is copied, then the import stops.
    let root = legacy_project();
    interrupt_import_for_test(Some(1), false);
    let stopped = import(&root);
    interrupt_import_for_test(None, false);
    assert!(stopped.unwrap_err().contains("interrupted"));
    let dir = attach(&root, false).unwrap().dir.unwrap();
    assert!(["runs", "acts", "captures", "workflow"].iter().any(|n| dir.join(n).exists()), "a copy was made");
    // No completion line: still read in place, and recording is refused.
    assert!(!home(&root).unwrap().store_mode);
    assert_eq!(storage::read_all(&root).0.len(), 3, "the whole history, read in place");
    let refused = write_dir(&root).unwrap_err();
    assert!(refused.starts_with("import incomplete"), "{refused}");
    assert!(records::append_project(&root, None, "writer:x", "evidence_limit", &APP_WRITER, body("x")).unwrap_err().contains("import incomplete"));
    assert_eq!(status(Some(&root))["project"]["reading"], "records in place in the project (import needed)");
    // The census changes before the rerun: reported, and the rerun resumes.
    let acts = root.join(".chirality/records").join(crate::recorder::LOG);
    records::append(&acts, "evidence_limit", &APP_WRITER, body("written before the rerun")).unwrap();
    let resumed = import(&root).unwrap();
    assert_eq!(resumed["state"], "imported", "{resumed}");
    assert!(resumed["censusChanged"].as_array().unwrap().iter().any(|c| c.as_str().unwrap().contains("changed since the interrupted import started")), "{resumed}");
    assert_eq!((resumed["copied"].as_u64(), resumed["alreadyPresent"].as_u64()), (Some(4), Some(1)), "the earlier copy is kept, not duplicated: {resumed}");
    let lines = read_lines(&dir.join("imports.jsonl")).unwrap();
    assert_eq!(lines.iter().map(|l| l["event"].as_str().unwrap()).collect::<Vec<_>>(), ["started", "started", "completed"]);
    assert_eq!(lines[1]["resumes"], lines[0]["importId"]);
    assert!(home(&root).unwrap().store_mode);
    let (entries, limits) = storage::read_all(&root);
    assert!(limits.is_empty(), "{limits:?}");
    assert_eq!(entries.len(), 4, "each identity once");
    assert!(write_dir(&root).is_ok());
    let _ = std::fs::remove_dir_all(&root);
}

#[test]
fn an_import_whose_copy_does_not_verify_does_not_complete() {
    let root = legacy_project();
    interrupt_import_for_test(None, true);
    let failed = import(&root);
    interrupt_import_for_test(None, false);
    assert!(failed.unwrap_err().contains("does not verify"));
    assert!(!home(&root).unwrap().store_mode);
    assert!(write_dir(&root).unwrap_err().starts_with("import incomplete"));
    let dir = attach(&root, false).unwrap().dir.unwrap();
    assert!(!read_lines(&dir.join("imports.jsonl")).unwrap().iter().any(|l| l["event"] == "completed"));
    // Run again: the copy is checked against the original, then completed.
    let again = import(&root).unwrap();
    assert_eq!((again["state"].as_str(), again["alreadyPresent"].as_u64()), (Some("imported"), Some(1)), "{again}");
    assert!(write_dir(&root).is_ok());
    let _ = std::fs::remove_dir_all(&root);
}

#[test]
fn probe_r16_new_project_at_a_moved_projects_path() {
    let old = folder("moved-from-");
    records::append_project(&old, None, "writer:m", "evidence_limit", &APP_WRITER, body("P's history")).unwrap();
    let p = attach(&old, false).unwrap().project.unwrap();
    let new_place = old.with_file_name(format!("{}-new-place", old.file_name().unwrap().to_string_lossy()));
    std::fs::rename(&old, &new_place).unwrap();
    adopt(&new_place).unwrap();
    // A new, unrelated folder made at the old path.
    std::fs::create_dir(&old).unwrap();
    let unrelated = attach(&old, true).unwrap();
    assert_eq!(unrelated.how, "minted", "{unrelated:?}");
    assert_ne!(unrelated.project.as_deref(), Some(p.as_str()), "never P's identity");
    assert_eq!(storage::read_all(&old).0.len(), 0, "none of P's history");
    assert_eq!(storage::read_all(&new_place).0.len(), 1);
    let _ = (std::fs::remove_dir_all(&old), std::fs::remove_dir_all(&new_place));
}

#[test]
fn probe_r16_adopt_keeps_the_old_root() {
    let old = folder("adopt-from-");
    records::append_project(&old, None, "writer:a", "evidence_limit", &APP_WRITER, body("x")).unwrap();
    let p = attach(&old, false).unwrap().project.unwrap();
    let new_place = old.with_file_name(format!("{}-adopted", old.file_name().unwrap().to_string_lossy()));
    std::fs::rename(&old, &new_place).unwrap();
    adopt(&new_place).unwrap();
    let (store, _) = opened().unwrap();
    let lines = roots(&store).unwrap();
    assert_eq!(roots_of(&lines, &p), vec![new_place.display().to_string()], "adopt releases every earlier root");
    assert!(lines.iter().any(|l| l["projectId"] == p.as_str() && l["root"] == old.display().to_string() && l["how"] == "released"), "an append-only release line");
    assert!(listed(&lines, old.to_str().unwrap()).is_empty());
    let _ = std::fs::remove_dir_all(&new_place);
}

#[test]
fn probe_r16_legacy_log_in_store_mode() {
    // A project recording in the store; a registered legacy log appears in
    // the agent-writable tree with a duplicated line.
    let root = folder("legacy-log-store-");
    records::append_project(&root, None, "writer:s", "evidence_limit", &APP_WRITER, body("in the store")).unwrap();
    let registered = root.join(storage::LEGACY_LOG);
    records::append(&registered, "evidence_limit", &APP_WRITER, body("legacy")).unwrap();
    let line = std::fs::read(&registered).unwrap();
    let mut doubled = line.clone();
    doubled.extend(&line);
    std::fs::write(&registered, &doubled).unwrap();
    let (entries, limits) = storage::read_all(&root);
    assert!(limits.is_empty(), "the project's set is not made incomplete: {limits:?}");
    assert_eq!(entries.len(), 1);
    assert!(records::append_project(&root, None, "writer:s", "evidence_limit", &APP_WRITER, body("still recorded")).is_ok());
    assert!(notes(&root).iter().any(|n| n.contains(storage::LEGACY_LOG) && n.contains("not imported")));
    let _ = std::fs::remove_dir_all(&root);
}

#[test]
fn the_registered_legacy_log_is_imported_and_its_original_never_read_again() {
    let root = folder("registered-import-");
    let registered = root.join(storage::LEGACY_LOG);
    let entry = records::append(&registered, "evidence_limit", &APP_WRITER, body("legacy history")).unwrap();
    assert!(write_dir(&root).unwrap_err().starts_with("import needed: 1"));
    import(&root).unwrap();
    let dir = attach(&root, false).unwrap().dir.unwrap();
    assert_eq!(std::fs::read(dir.join(REGISTERED_COPY)).unwrap(), std::fs::read(&registered).unwrap());
    assert_eq!(storage::registered_legacy_log(&root).unwrap(), dir.join(REGISTERED_COPY));
    assert_eq!(storage::read_all(&root).0, vec![entry.clone()], "read from the imported copy");
    // A forged line added to the original afterwards: not read, a note.
    let copy = std::fs::read(dir.join(REGISTERED_COPY)).unwrap();
    let mut f = std::fs::OpenOptions::new().append(true).open(&registered).unwrap();
    std::io::Write::write_all(&mut f, &copy).unwrap();
    let (entries, limits) = storage::read_all(&root);
    assert!(limits.is_empty(), "{limits:?}");
    assert_eq!(entries, vec![entry]);
    assert!(notes(&root).iter().any(|n| n.contains(storage::LEGACY_LOG) && n.contains("differs from its imported copy")));
    let _ = std::fs::remove_dir_all(&root);
}

#[test]
fn a_project_librarys_act_log_is_library_evidence_never_the_project_set() {
    // A project that is also a workflow library, recording in the store.
    let root = folder("project-library-");
    records::append_project(&root, None, "writer:p", "evidence_limit", &APP_WRITER, body("project")).unwrap();
    let library = storage::library_log(&root);
    let act = records::append(&library, "evidence_limit", &APP_WRITER, body("library act")).unwrap();
    // A forged, valid-looking entry and a duplicated line, written by an agent.
    let forged = records::append(&library, "evidence_limit", &APP_WRITER, body("forged")).unwrap();
    let first = std::fs::read(&library).unwrap();
    let one = first.split(|b| *b == b'\n').next().unwrap().to_vec();
    let mut f = std::fs::OpenOptions::new().append(true).open(&library).unwrap();
    std::io::Write::write_all(&mut f, &[one.as_slice(), b"\n"].concat()).unwrap();
    // The project's set: unaffected, and recording is not refused.
    let (entries, limits) = storage::read_all(&root);
    assert!(limits.is_empty(), "{limits:?}");
    assert!(entries.iter().all(|e| e["recordId"] != act["recordId"] && e["recordId"] != forged["recordId"]), "library entries never join the project's set");
    assert!(records::append_project(&root, Some("run:p"), "writer:p", "evidence_limit", &APP_WRITER, body("still recorded")).is_ok());
    assert!(crate::records_index::with_index(&root, |ix| ix.limits()).is_empty());
    // Library standing: the duplicate is a limit there.
    let (library_entries, library_limits) = records::library_record_set(&root);
    assert!(library_limits.iter().any(|l| l.contains("duplicate record identity") || l.contains("sequence")), "{library_limits:?}");
    assert!(library_entries.iter().any(|e| e["recordId"] == forged["recordId"]), "read as library evidence only");
    assert!(!records::read_log(&library).1.is_empty(), "library standing reads the act log with its limit");
    let _ = std::fs::remove_dir_all(&root);
}

// ---- Re-review repair (N2): a late import in a project the store already holds ----

/// A project recording in the store, with a §13.7 act log that appeared
/// later; returns the store entry and the late entry.
fn store_project_with_a_late_file() -> (PathBuf, Value, Value) {
    let root = folder("late-import-");
    let held = records::append_project(&root, Some("run:s"), "writer:s", "evidence_limit", &APP_WRITER, body("in the store")).unwrap();
    let late = root.join(".chirality/records/acts/late-writer.jsonl");
    let entry = records::append(&late, "evidence_limit", &APP_WRITER, body("late §13.7 entry")).unwrap();
    assert!(notes(&root).iter().any(|n| n.contains("late-writer.jsonl") && n.contains("not imported")));
    (root, held, entry)
}

#[test]
fn probe_r17_interrupted_late_import_in_a_store_project() {
    let (root, held, _) = store_project_with_a_late_file();
    interrupt_import_for_test(Some(0), false);
    let stopped = import(&root);
    interrupt_import_for_test(None, false);
    assert!(stopped.unwrap_err().contains("interrupted"));
    let dir = attach(&root, false).unwrap().dir.unwrap();
    let started = read_lines(&dir.join("imports.jsonl")).unwrap();
    assert_eq!((started.len(), started[0]["event"].as_str(), started[0]["storeHeld"].as_bool()), (1, Some("started"), Some(true)));
    // Readers keep reading the store, as before the import; writes wait.
    assert!(home(&root).unwrap().store_mode, "store_mode stays true");
    let (entries, limits) = storage::read_all(&root);
    assert!(limits.is_empty(), "{limits:?}");
    assert_eq!(entries, vec![held.clone()], "the store's own records, not the late file");
    assert!(write_dir(&root).unwrap_err().starts_with("import incomplete"));
    assert_eq!(status(Some(&root))["project"]["reading"], "records store");
    // Completed on a rerun: the late copy joins the store set.
    let done = import(&root).unwrap();
    assert_eq!((done["state"].as_str(), done["copied"].as_u64()), (Some("imported"), Some(1)), "{done}");
    assert!(write_dir(&root).is_ok());
    let _ = std::fs::remove_dir_all(&root);
}

#[test]
fn a_completed_late_import_counts_each_identity_once() {
    let (root, held, late) = store_project_with_a_late_file();
    // An agent also copies a store log (two entries) into a §13.7 path under another key.
    let second = records::append_project(&root, Some("run:s"), "writer:s", "evidence_limit", &APP_WRITER, body("second in the store")).unwrap();
    let store_log = storage::project_log(&root, Some("run:s"), "writer:s").unwrap();
    let copied_back = root.join(".chirality/records/acts/copy-of-store-log.jsonl");
    std::fs::copy(&store_log, &copied_back).unwrap();
    let done = import(&root).unwrap();
    assert_eq!(done["state"], "imported with conflicts", "{done}");
    assert!(done["conflicts"].as_array().unwrap().iter().any(|c| c["original"].as_str().unwrap().ends_with("copy-of-store-log.jsonl")
        && c["reason"].as_str().unwrap().contains("already holds")), "{done}");
    // Every held identity is named: in the result, the completed line and the note.
    let ids = [held["recordId"].as_str().unwrap(), second["recordId"].as_str().unwrap()];
    let conflict = done["conflicts"].as_array().unwrap().iter().find(|c| c["original"].as_str().unwrap().ends_with("copy-of-store-log.jsonl")).unwrap();
    assert_eq!(conflict["heldCount"], 2);
    assert!(ids.iter().all(|id| conflict["reason"].as_str().unwrap().contains(id) && conflict["heldIdentities"].as_array().unwrap().iter().any(|h| h == id)), "{conflict}");
    let dir = attach(&root, false).unwrap().dir.unwrap();
    let completed = read_lines(&dir.join("imports.jsonl")).unwrap().into_iter().rev().find(|l| l["event"] == "completed").unwrap();
    assert!(completed["conflicts"].as_array().unwrap().iter().any(|c| ids.iter().all(|id| c["reason"].as_str().unwrap().contains(id))));
    assert!(notes(&root).iter().any(|n| n.contains("copy-of-store-log.jsonl") && ids.iter().all(|id| n.contains(id))), "{:?}", notes(&root));
    assert!(!dir.join("acts/copy-of-store-log.jsonl").exists(), "not copied");
    assert!(dir.join("acts/late-writer.jsonl").exists());
    let (entries, limits) = storage::read_all(&root);
    assert!(limits.is_empty(), "no duplicate identity: {limits:?}");
    assert_eq!(entries.len(), 3);
    assert_eq!(entries.iter().filter(|e| e["recordId"] == second["recordId"]).count(), 1);
    assert_eq!(entries.iter().filter(|e| e["recordId"] == held["recordId"]).count(), 1);
    assert_eq!(entries.iter().filter(|e| e["recordId"] == late["recordId"]).count(), 1);
    assert!(records::append_project(&root, Some("run:s"), "writer:s", "evidence_limit", &APP_WRITER, body("after")).is_ok());
    let _ = std::fs::remove_dir_all(&root);
}

#[test]
fn held_identities_are_named_up_to_a_bound() {
    let ids: Vec<String> = (0..23).map(|n| format!("rec:app:held-{n}")).collect();
    let named = name_bounded(&ids);
    assert!(named.contains("rec:app:held-19") && !named.contains("rec:app:held-20"), "{named}");
    assert!(named.ends_with(", and 3 more"), "{named}");
    assert_eq!(name_bounded(&ids[..2]), "rec:app:held-0, rec:app:held-1");
}


/// An original swapped after the import's census, for a link, a hard link or
/// other bytes, is refused and never copied as a clean file: each read opens
/// one descriptor without following links and checks it against the census.
#[test]
fn an_original_swapped_after_the_census_is_never_copied() {
    for swap in ["symlink", "hard link", "other bytes", "fifo"] {
        let _store = OwnStore::new();
        let root = legacy_project();
        let run = root.join(".chirality/records").join(storage::log_rel(Some("run:legacy"), "writer:legacy"));
        let outside = root.parent().unwrap().join(crate::util::opaque_id("outside-").unwrap());
        std::fs::write(&outside, b"{\"not\":\"a record\"}\n").unwrap();
        let (run2, outside2) = (run.clone(), outside.clone());
        AFTER_CENSUS.with(|h| *h.borrow_mut() = Some(Box::new(move || {
            match swap {
                "symlink" => {
                    std::fs::remove_file(&run2).unwrap();
                    std::os::unix::fs::symlink(&outside2, &run2).unwrap();
                }
                "hard link" => std::fs::hard_link(&run2, outside2.with_extension("second")).unwrap(),
                "other bytes" => {
                    let mut bytes = std::fs::read(&run2).unwrap();
                    bytes.extend_from_slice(b"{\"appended\":\"after the census\"}\n");
                    std::fs::write(&run2, bytes).unwrap();
                }
                _ => {
                    std::fs::remove_file(&run2).unwrap();
                    let name = std::ffi::CString::new(run2.as_os_str().as_encoded_bytes()).unwrap();
                    assert_eq!(unsafe { libc::mkfifo(name.as_ptr(), 0o600) }, 0);
                }
            }
        })));
        let outcome = import(&root).unwrap();
        AFTER_CENSUS.with(|h| h.borrow_mut().take());
        let rel = run.strip_prefix(&root).unwrap().to_string_lossy().into_owned();
        let conflict = outcome["conflicts"].as_array().unwrap().iter().find(|c| c["original"] == rel.as_str()).unwrap_or_else(|| panic!("{swap}: {outcome}")).clone();
        let reason = conflict["reason"].as_str().unwrap();
        assert!(reason.contains("not copied"), "{swap}: {reason}");
        let dir = attach(&root, false).unwrap().dir.unwrap();
        assert!(!dir.join(storage::log_rel(Some("run:legacy"), "writer:legacy")).exists(), "{swap}: nothing copied for it");
        let _ = std::fs::remove_file(&outside);
        let _ = std::fs::remove_file(outside.with_extension("second"));
    }
}
/// A name that is not UTF-8 is never copied under a lossy name.
#[test]
fn an_original_whose_name_is_not_utf8_is_not_copied() {
    use std::os::unix::ffi::OsStrExt;
    let _store = OwnStore::new();
    let root = legacy_project();
    let dir = root.join(crate::connector_route_store::LEGACY_DIRECTORY);
    std::fs::create_dir_all(&dir).unwrap();
    // APFS (macOS) refuses such names itself (EILSEQ); other file systems
    // accept them, and the census must then refuse to copy them.
    if let Err(e) = std::fs::write(dir.join(std::ffi::OsStr::from_bytes(b"bad-\xff.json")), b"{}") {
        assert_eq!(e.raw_os_error(), Some(libc::EILSEQ), "{e}");
        return;
    }
    let outcome = import(&root).unwrap();
    assert!(outcome["conflicts"].to_string().contains("not UTF-8"), "{outcome}");
    let store_dir = attach(&root, false).unwrap().dir.unwrap();
    assert!(std::fs::read_dir(store_dir.join(CONNECTOR_COPY)).map_or(true, |mut d| d.next().is_none()), "nothing copied under a lossy name");
}

#[test]
fn records_store_lines_refuse_fifo_and_final_link_without_changing_torn_tail_parsing(){
 use std::os::unix::fs::symlink;
 let own=OwnStore::new();let path=own.0.join("invented-read-lines.jsonl");let regular=b"{\"invented\":\"complete\"}\n{\"torn\":";std::fs::write(&path,regular).unwrap();assert_eq!(read_lines(&path).unwrap(),vec![json!({"invented":"complete"})],"compatibility torn-tail parsing remains unchanged");std::fs::remove_file(&path).unwrap();let c=std::ffi::CString::new(path.as_os_str().as_encoded_bytes()).unwrap();assert_eq!(unsafe{libc::mkfifo(c.as_ptr(),0o600)},0);let before=std::time::Instant::now();assert!(read_lines(&path).is_err());assert!(before.elapsed()<std::time::Duration::from_secs(1));std::fs::remove_file(&path).unwrap();let other=own.0.join("other-owned.jsonl");std::fs::write(&other,b"{\"other\":\"not returned\"}\n").unwrap();symlink(&other,&path).unwrap();assert!(read_lines(&path).is_err());assert_eq!(std::fs::read(&other).unwrap(),b"{\"other\":\"not returned\"}\n");
}

#[test]
fn a_kept_index_cache_is_neither_changed_nor_cleaned_out_through_a_store_that_was_replaced() {
    for replace_folder in [false, true] {
        let own = OwnStore::new();
        let store = own.0.clone();
        let root = written_project("kept-cache-project-");
        // Warm: this process's index holds its cache file in the store.
        assert!(crate::records_index::chain_heads(&root)["discoveryLimit"].is_null());
        let cache_of = |at: &Path| tree(&at.join("indexes"));
        assert!(!cache_of(&store).is_empty());
        let moved = store.with_extension("moved");
        if replace_folder {
            // The store folder replaced, with the kept cache's folder moved into the replacement.
            std::fs::rename(&store, &moved).unwrap();
            std::fs::create_dir(&store).unwrap();
            std::fs::copy(moved.join("store.json"), store.join("store.json")).unwrap();
            std::fs::rename(moved.join("indexes"), store.join("indexes")).unwrap();
        } else {
            // The identity file replaced by another holding the same bytes.
            let bytes = std::fs::read(store.join("store.json")).unwrap();
            std::fs::remove_file(store.join("store.json")).unwrap();
            std::fs::write(store.join("store.json"), bytes).unwrap();
        }
        let before = cache_of(&store);
        // The same process reads again through its kept index. The opening refuses,
        let heads = crate::records_index::chain_heads(&root);
        assert!(heads["discoveryLimit"].as_str().is_some_and(|l| l.contains("replaced")), "{replace_folder}: {heads}");
        let _ = crate::records_index::with_index(&root, |ix| ix.limits());
        // and the kept cache is left exactly as it was: no row removed from it,
        assert_eq!(cache_of(&store), before, "{replace_folder}");
        // and it is not cleaned out through the refused binding when the index is released.
        crate::records_index::close_all();
        assert_eq!(cache_of(&store), before, "{replace_folder}");
        if replace_folder {
            std::fs::remove_dir_all(&store).unwrap();
            std::fs::rename(&moved, &store).unwrap();
        }
        drop(own);
        new_process();
        let _ = std::fs::remove_dir_all(root);
    }
}

#[test]
fn a_control_that_is_not_a_regular_singly_linked_file_is_refused_without_waiting() {
    let own = OwnStore::new();
    let store = own.0.clone();
    let root = written_project("special-control-");
    let dir = attach(&root, false).unwrap().dir.unwrap();
    let control = store.join("administration").join(dir.file_name().unwrap()).join(".admission.lock");
    // A FIFO where the control stood: opening it for reading would wait for a writer for ever.
    std::fs::remove_file(&control).unwrap();
    let name = std::ffi::CString::new(control.as_os_str().as_encoded_bytes()).unwrap();
    assert_eq!(unsafe { libc::mkfifo(name.as_ptr(), 0o600) }, 0);
    let (send, receive) = std::sync::mpsc::channel();
    let path = control.clone();
    std::thread::spawn(move || { let _ = send.send(storage::lock_shared_existing(&path).map(|guard| guard.is_some())); });
    let refused = receive.recv_timeout(std::time::Duration::from_secs(10)).expect("opening the control must not wait").unwrap_err();
    assert!(refused.contains("not a regular, singly linked file"), "{refused}");
    let refused = crate::role_observations::project_chain_head(&root).unwrap_err();
    assert!(refused.contains("not a regular, singly linked file"), "{refused}");
    // A regular control with a second link is refused too; alone, it is the control.
    std::fs::remove_file(&control).unwrap();
    std::fs::write(&control, b"").unwrap();
    std::fs::hard_link(&control, control.with_extension("other")).unwrap();
    assert!(storage::lock_shared_existing(&control).map(|guard| guard.is_some()).unwrap_err().contains("not a regular, singly linked file"));
    std::fs::remove_file(control.with_extension("other")).unwrap();
    assert!(storage::lock_shared_existing(&control).unwrap().is_some());
    drop(own);
    new_process();
    let _ = std::fs::remove_dir_all(root);
}

#[test]
fn the_single_line_form_the_first_store_builds_wrote_for_an_import_is_read_as_completed() {
    // Before imports had a "started" line, a completed import was one line
    // with no event (main at 0237b6b3). It is one of the three forms the
    // reader takes: read, not rewritten, and the store's copies govern as after any completed import.
    let own = OwnStore::new();
    let root = legacy_project();
    import(&root).unwrap();
    let dir = attach(&root, false).unwrap().dir.unwrap();
    let lines = read_lines(&dir.join("imports.jsonl")).unwrap();
    let started = lines.iter().find(|l| l["event"] == "started").unwrap();
    let mut earlier = lines.iter().find(|l| l["event"] == "completed").unwrap().clone();
    for member in ["event", "censusChanged"] { earlier.as_object_mut().unwrap().remove(member); }
    earlier["root"] = started["root"].clone();
    earlier["method"] = started["method"].clone();
    let mut bytes = serde_json::to_vec(&earlier).unwrap();
    bytes.push(b'\n');
    std::fs::write(dir.join("imports.jsonl"), &bytes).unwrap();
    assert!(home(&root).unwrap().store_mode);
    assert!(storage::read_all(&root).1.is_empty(), "{:?}", storage::read_all(&root).1);
    assert_eq!(std::fs::read(dir.join("imports.jsonl")).unwrap(), bytes, "not rewritten");
    drop(own);
    new_process();
    let _ = std::fs::remove_dir_all(root);
}

#[test]
fn a_capability_read_makes_only_its_read_logs_own_folder_and_nothing_above_it() {
    let own = OwnStore::new();
    let store = own.0.clone();
    let root = written_project("read-log-leaf-");
    let dir = attach(&root, false).unwrap().dir.unwrap();
    // The read's own folder is the one thing made, beneath a subtree that exists.
    capability_read(&root).unwrap();
    assert!(dir.join("reads/records-reads.jsonl").is_file());
    // The project's subtree gone while its admission control still stands:
    // the read is refused, and the subtree is not made again to hold its log.
    let moved = dir.with_extension("moved");
    std::fs::rename(&dir, &moved).unwrap();
    let before = tree(&store);
    assert!(capability_read(&root).is_err());
    let added: Vec<_> = tree(&store).keys().filter(|p| !before.contains_key(*p) && !p.starts_with(store.join("indexes"))).cloned().collect();
    assert!(added.is_empty(), "{added:?}");
    std::fs::rename(&moved, &dir).unwrap();
    drop(own);
    new_process();
    let _ = std::fs::remove_dir_all(root);
}

/// The census's premise (App Agent 0, from the INTERLOCUTOR's reading of
/// main): a census that could not inspect a project's records never says
/// there are none. Reproduced on main before the repair: in each state below
/// the census was empty, status read "no records yet" and write admission was
/// given. (1) The project's only record is its registered legacy log, and its
/// folder cannot be searched (a real permission failure). (2) Something other
/// than a folder where a census folder is expected, inside the App's own
/// `.chirality` folder. Genuine absence stays allowed: no records reads "no
/// records yet" and may be written, and so does a project with a file named
/// `records` at its root (the registered log cannot exist under it).
#[test]
fn a_census_that_cannot_inspect_the_records_never_says_there_are_none() {
    use std::os::unix::fs::PermissionsExt;
    let _own = OwnStore::new();
    let refused = |root: &Path, label: &str| {
        assert!(legacy_census(root).is_err(), "{label}: census");
        let shown = status(Some(root));
        assert_ne!(shown["project"]["reading"], "no records yet", "{label}: {shown}");
        assert_eq!(shown["project"]["state"], "unavailable", "{label}: {shown}");
        assert!(write_dir(root).is_err(), "{label}: write admission");
    };
    let allowed = |root: &Path, label: &str| {
        assert!(legacy_census(root).unwrap().is_empty(), "{label}: census");
        assert_eq!(status(Some(root))["project"]["reading"], "no records yet", "{label}");
        assert!(write_dir(root).is_ok(), "{label}: write admission");
    };
    // Genuine absence.
    let fresh = folder("census-fresh-");
    attach(&fresh, true).unwrap();
    allowed(&fresh, "no records");
    let named = folder("census-records-file-");
    std::fs::write(named.join("records"), b"a project file named records\n").unwrap();
    attach(&named, true).unwrap();
    allowed(&named, "a file named records at the project's root");
    // (1) The registered legacy log, its folder unsearchable.
    let root = folder("census-unsearchable-");
    records::append(&root.join(storage::LEGACY_LOG), "evidence_limit", &APP_WRITER, body("legacy history")).unwrap();
    attach(&root, true).unwrap();
    assert!(write_dir(&root).unwrap_err().starts_with("import needed: 1"), "readable: import needed");
    let parent = root.join(storage::LEGACY_LOG).parent().unwrap().to_path_buf();
    std::fs::set_permissions(&parent, std::fs::Permissions::from_mode(0o000)).unwrap();
    let denied = std::fs::symlink_metadata(root.join(storage::LEGACY_LOG)).map(|_| ()).map_err(|e| e.kind());
    let result = std::panic::catch_unwind(|| refused(&root, "the registered log's folder unsearchable"));
    std::fs::set_permissions(&parent, std::fs::Permissions::from_mode(0o700)).unwrap();
    assert_eq!(denied, Err(std::io::ErrorKind::PermissionDenied), "a real permission failure");
    assert!(result.is_ok(), "the registered log's folder unsearchable");
    // (2) Something other than a folder where a census folder is expected.
    for (label, rel) in [("records/runs a file", ".chirality/records/runs"), ("records a file", ".chirality/records"), ("captures a file", ".chirality/captures"),
        ("connector accounts a file", crate::connector_route_store::LEGACY_DIRECTORY), ("the registered log a folder", storage::LEGACY_LOG)] {
        let root = folder("census-wrong-type-");
        let path = root.join(rel);
        std::fs::create_dir_all(path.parent().unwrap()).unwrap();
        if label == "the registered log a folder" { std::fs::create_dir(&path).unwrap(); } else { std::fs::write(&path, b"{\"invented\":\"bytes where a folder is expected\"}\n").unwrap(); }
        attach(&root, true).unwrap();
        refused(&root, label);
    }
}

/// The same premise in the store's own identity record: a folder whose link
/// names a project the store holds, with that project's record unable to be
/// examined (its store folder unsearchable, a real permission failure), is
/// never taken for a project the store does not hold: attaching it, reading
/// it, writing for it and adopting it are each refused, never read in place.
#[test]
fn an_identity_record_that_cannot_be_examined_is_never_taken_for_one_the_store_does_not_hold() {
    use std::os::unix::fs::PermissionsExt;
    let _own = OwnStore::new();
    let root = folder("identity-unexaminable-");
    records::append_project(&root, None, "writer:i", "evidence_limit", &APP_WRITER, body("in the store")).unwrap();
    let attachment = attach(&root, false).unwrap();
    let dir = attachment.dir.clone().unwrap();
    // The registry names the identity nowhere (as when a minting stopped
    // before its first registry line), so whether the store holds it is
    // decided by its record alone.
    let store = opened().unwrap().0;
    std::fs::write(store.join("roots.jsonl"), b"").unwrap();
    *ROOTS.lock().unwrap() = None;
    let readable = attach(&root, false).unwrap();
    assert_eq!(readable.fault, Some("no folder recorded"), "readable: records kept, not attached: {readable:?}");
    std::fs::set_permissions(&dir, std::fs::Permissions::from_mode(0o000)).unwrap();
    let denied = std::fs::symlink_metadata(dir.join("project.json")).map(|_| ()).map_err(|e| e.kind());
    let attached = attach(&root, false);
    let reading = status(Some(&root))["project"]["reading"].clone();
    let written = write_dir(&root);
    let adopted = adopt(&root);
    std::fs::set_permissions(&dir, std::fs::Permissions::from_mode(0o700)).unwrap();
    assert_eq!(denied, Err(std::io::ErrorKind::PermissionDenied), "a real permission failure");
    assert!(attached.as_ref().is_err_and(|e| e.contains("whether the store holds this project is not known")), "{attached:?}");
    assert!(reading != "no records yet" && reading.as_str().is_none_or(|r| !r.contains("in place")), "{reading}");
    assert!(written.is_err(), "{written:?}");
    assert!(adopted.is_err(), "{adopted:?}");
}

/// Startup recovery shows what it left as it was. What it could not examine
/// (the store's own record, or a project's import account) is shown too,
/// never passed over as though there were nothing there to recover.
#[test]
fn startup_recovery_never_passes_over_what_it_could_not_examine() {
    use std::os::unix::fs::PermissionsExt;
    let _own = OwnStore::new();
    let root = folder("recovery-unexaminable-");
    let dir = attach(&root, true).unwrap().dir.unwrap();
    let store = opened().unwrap().0;
    let account = dir.join("imports.jsonl");
    // An append cut short: a fragment recovery would close and name.
    std::fs::write(&account, b"{\"cut short").unwrap();
    std::fs::set_permissions(&dir, std::fs::Permissions::from_mode(0o000)).unwrap();
    let denied = std::fs::symlink_metadata(&account).map(|_| ()).map_err(|e| e.kind());
    let left = recover_at_startup();
    std::fs::set_permissions(&dir, std::fs::Permissions::from_mode(0o700)).unwrap();
    assert_eq!(denied, Err(std::io::ErrorKind::PermissionDenied), "a real permission failure");
    let left = left.unwrap();
    assert!(left.iter().any(|l| l.contains(&account.display().to_string()) && l.contains("could not be examined")), "the account is shown as not examined: {left:?}");
    assert_eq!(std::fs::read(&account).unwrap(), b"{\"cut short", "left as it was");

    std::fs::set_permissions(&store, std::fs::Permissions::from_mode(0o000)).unwrap();
    let denied = std::fs::symlink_metadata(store.join("store.json")).map(|_| ()).map_err(|e| e.kind());
    let recovered = recover_at_startup();
    std::fs::set_permissions(&store, std::fs::Permissions::from_mode(0o700)).unwrap();
    assert_eq!(denied, Err(std::io::ErrorKind::PermissionDenied), "a real permission failure");
    assert!(recovered.as_ref().is_err_and(|e| e.contains("store.json")), "a store whose record cannot be examined is not a store not yet created: {recovered:?}");
}


/// A registered legacy log that cannot be examined is not absent from the
/// project's record set, in either read home: discovery shows a limit. And a
/// late import, which copies a log only when the store's set does not
/// already hold its record identities, is refused when that set could not
/// be read whole: it never copies a duplicate of a record it could not see.
#[test]
fn a_registered_log_that_cannot_be_examined_is_never_left_out_of_the_set_or_copied_again() {
    use std::os::unix::fs::PermissionsExt;
    let _own = OwnStore::new();
    // The late import.
    let root = folder("registered-late-import-");
    let original = root.join(storage::LEGACY_LOG);
    records::append(&original, "evidence_limit", &APP_WRITER, body("registered history")).unwrap();
    attach(&root, true).unwrap();
    import(&root).unwrap();
    let dir = attach(&root, false).unwrap().dir.unwrap();
    let copy = dir.join(REGISTERED_COPY);
    // A late log in the project folder holding the same record identity.
    let late = root.join(".chirality/records/runs/late-run/late.jsonl");
    std::fs::create_dir_all(late.parent().unwrap()).unwrap();
    std::fs::copy(&original, &late).unwrap();
    let parent = copy.parent().unwrap().to_path_buf();
    std::fs::set_permissions(&parent, std::fs::Permissions::from_mode(0o000)).unwrap();
    let denied = std::fs::symlink_metadata(&copy).map(|_| ()).map_err(|e| e.kind());
    let imported = import(&root);
    std::fs::set_permissions(&parent, std::fs::Permissions::from_mode(0o700)).unwrap();
    assert_eq!(denied, Err(std::io::ErrorKind::PermissionDenied), "a real permission failure");
    let after = storage::read_all_parts(&root);
    assert!(after.0.len() == 1 && after.1.is_empty(), "no duplicate record identity was copied: {imported:?}; the set reads {after:?}");
    assert!(imported.is_err(), "refused, never reported copied: {imported:?}");
    let _ = std::fs::remove_dir_all(&root);

    for stored in [false, true] {
        let root = folder("registered-unexaminable-");
        records::append(&root.join(storage::LEGACY_LOG), "evidence_limit", &APP_WRITER, body("registered history")).unwrap();
        attach(&root, true).unwrap();
        if stored { import(&root).unwrap(); }
        let log = readable_home(&root).unwrap().registered_log();
        let readable = storage::read_all_parts(&root);
        assert!(readable.0.len() == 1 && readable.1.is_empty(), "control (stored {stored}): {readable:?}");
        let parent = log.parent().unwrap().to_path_buf();
        std::fs::set_permissions(&parent, std::fs::Permissions::from_mode(0o000)).unwrap();
        let denied = std::fs::symlink_metadata(&log).map(|_| ()).map_err(|e| e.kind());
        let set = storage::read_all_parts(&root);
        let index = crate::records_index::with_index(&root, |ix| ix.limits());
        std::fs::set_permissions(&parent, std::fs::Permissions::from_mode(0o700)).unwrap();
        assert_eq!(denied, Err(std::io::ErrorKind::PermissionDenied), "a real permission failure");
        assert!(set.0.is_empty() && set.1.iter().any(|l| l.contains("could not be examined")), "stored {stored}: never a clean empty set: {set:?}");
        assert!(index.iter().any(|l| l.contains("could not be examined")), "stored {stored}: the index shows it too: {index:?}");
        let _ = std::fs::remove_dir_all(&root);
    }
}

/// A run folder whose entries can be listed but not examined is not an empty
/// record set. Through a caller that decides from the set: composing an A16
/// offer finds its act request in the set, and a set it could not walk whole
/// is refused as incomplete, never reported as one without the request.
/// (Writes are kept from this premise already: an append checks the set
/// through the index, whose own walk examines every entry; finishing a
/// delayed capture over such a set was refused before this repair.)
#[test]
fn a_record_set_that_cannot_be_walked_whole_never_decides_a_record_is_missing() {
    use std::os::unix::fs::PermissionsExt;
    let _own = OwnStore::new();
    let root = folder("set-unwalkable-");
    let rel = format!("{}/PKG-1.json", crate::recorder::DECISIONS_DIR);
    std::fs::create_dir_all(root.join(crate::recorder::DECISIONS_DIR)).unwrap();
    let bytes = std::fs::read(Path::new(env!("CARGO_MANIFEST_DIR")).join("../tests/fixtures/FX-DP1/project/decisions/PKG-1.json")).unwrap();
    std::fs::write(root.join(&rel), &bytes).unwrap();
    let (pkg, identity) = crate::util::package_snapshot(&bytes).unwrap();
    let body = crate::recorder::request_from_file(&pkg, &rel, &identity, json!({"kind":"agent"}), &crate::util::now_rfc3339());
    // The act request, recorded in a run's log.
    let request = records::append_project(&root, Some("run:invented-a16"), "writer:a16", "act_request", &APP_WRITER, body).unwrap();
    let rid = request["recordId"].as_str().unwrap().to_owned();
    let dir = attach(&root, false).unwrap().dir.unwrap();
    let readable = crate::act_control::ActControl::new(&root).compose_a16(&rid);
    assert!(readable.is_ok(), "control: the request is found and offered: {readable:?}");
    let runs = dir.join("runs");
    let child = std::fs::read_dir(&runs).unwrap().next().unwrap().unwrap().path();
    std::fs::set_permissions(&runs, std::fs::Permissions::from_mode(0o400)).unwrap();
    let denied = std::fs::symlink_metadata(&child).map(|_| ()).map_err(|e| e.kind());
    let set = storage::read_all_parts(&root);
    let offered = crate::act_control::ActControl::new(&root).compose_a16(&rid);
    std::fs::set_permissions(&runs, std::fs::Permissions::from_mode(0o700)).unwrap();
    assert_eq!(denied, Err(std::io::ErrorKind::PermissionDenied), "a real permission failure");
    assert!(offered.as_ref().is_err_and(|e| !e.contains("no act_request")), "never reported as a record without the request: {offered:?}; the set read {set:?}");
    assert!(offered.as_ref().is_err_and(|e| e.contains("incomplete")), "{offered:?}");
    assert!(!set.1.is_empty(), "never a clean set: {set:?}");
    let _ = std::fs::remove_dir_all(&root);
}

/// A test build's default store is this process's own: two stores made for
/// one process id differ, so a later process given a reused id never opens an
/// earlier process's store.
#[test]
fn two_test_stores_for_one_process_id_are_never_the_same() {
    let pid = std::process::id();
    let prefix = format!("chirality-test-records-{pid}-");
    let (first, second) = (fresh_test_store_name(pid), fresh_test_store_name(pid));
    assert!(first.starts_with(&prefix) && second.starts_with(&prefix), "{first} {second}");
    assert_ne!(first, second, "a reused process id never names the same store");
    // This process's own store carries its id and a nonce, and is stable.
    let own = test_store_name();
    assert!(own.starts_with(&prefix) && own.len() > prefix.len(), "{own}");
    assert_eq!(own, test_store_name());
}

/// S1. A store that cannot be examined when a read opens it is reported with
/// that cause, never as a store not created yet.
#[test]
fn a_store_that_cannot_be_examined_is_reported_with_its_cause() {
    use std::os::unix::fs::PermissionsExt;
    let parent = folder("store-unexaminable-");
    let root = parent.join("store");
    std::fs::create_dir_all(&root).unwrap();
    // Never opened in this process (the App's start did not reach it), so a
    // read opens it afresh rather than through the cached opening.
    use_store_not_started_for_test(Some(Ok(Store { root: root.clone(), placement: Placement::Override, limits: vec![] })));
    let project = folder("store-unexaminable-project-");
    std::fs::set_permissions(&parent, std::fs::Permissions::from_mode(0o000)).unwrap();
    let opened = opened();
    std::fs::set_permissions(&parent, std::fs::Permissions::from_mode(0o700)).unwrap();
    use_store_for_test(None);
    let e = opened.unwrap_err();
    assert!(e.contains("Permission denied") && !e.contains("does not exist") && !e.contains("not created yet"), "{e}");
    let _ = (std::fs::remove_dir_all(&parent), std::fs::remove_dir_all(&project));
}

/// S2. An imported original that cannot be read is described as not known,
/// never as differing from its imported copy.
#[test]
fn an_imported_original_that_cannot_be_read_is_never_said_to_differ() {
    use std::os::unix::fs::PermissionsExt;
    let _own = OwnStore::new();
    let root = legacy_project();
    attach(&root, true).unwrap();
    import(&root).unwrap();
    let original = root.join(".chirality/records").join(storage::log_rel(Some("run:legacy"), "writer:legacy"));
    assert!(notes(&root).iter().all(|n| !n.contains("differs")), "control: nothing differs");
    std::fs::set_permissions(&original, std::fs::Permissions::from_mode(0o000)).unwrap();
    let unreadable = std::fs::read(&original).is_err();
    let shown = notes(&root);
    std::fs::set_permissions(&original, std::fs::Permissions::from_mode(0o600)).unwrap();
    assert!(unreadable, "a real permission failure");
    let rel = storage::log_rel(Some("run:legacy"), "writer:legacy");
    // The positive claim of a difference names the copy's hash at import.
    assert!(shown.iter().all(|n| !(n.contains(&rel) && n.contains("differs from its imported copy") && n.contains("at import"))), "never said to differ: {shown:?}");
    assert!(shown.iter().any(|n| n.contains(&rel) && n.contains("not known")), "said to be not known: {shown:?}");
    let _ = std::fs::remove_dir_all(&root);
}

// ---- What could not be examined is never absent: the library's act set,
// identity creation and a pending capture (the lint census's traces) ----

/// Make `dir` unsearchable for the closure, and put its mode back after.
fn unsearchable<T>(dir: &Path, f: impl FnOnce() -> T) -> T {
    use std::os::unix::fs::PermissionsExt;
    std::fs::set_permissions(dir, std::fs::Permissions::from_mode(0o000)).unwrap();
    let out = f();
    std::fs::set_permissions(dir, std::fs::Permissions::from_mode(0o700)).unwrap();
    out
}

/// A library's act log that cannot be examined is a limit on its act set,
/// never an empty and complete set (only a log that is not there holds no
/// acts).
#[test]
fn records_store_an_unexaminable_library_act_log_is_a_limit_never_an_empty_set() {
    let library = folder("library-act-set-");
    let log = storage::library_log(&library);
    records::append(&log, "evidence_limit", &APP_WRITER, body("a library act")).unwrap();
    assert_eq!(records::library_record_set(&library).0.len(), 1);
    let folder_of_log = log.parent().unwrap().to_path_buf();
    let (entries, limits) = unsearchable(&folder_of_log, || records::library_record_set(&library));
    assert!(entries.is_empty(), "{entries:?}");
    assert!(limits.iter().any(|l| l.contains("incomplete record")), "the act set is not complete: {limits:?}");
    // A library with no act log at all still holds no acts, with no limit.
    let empty = folder("library-no-acts-");
    assert_eq!(records::library_record_set(&empty), (vec![], vec![]));
    let _ = (std::fs::remove_dir_all(&library), std::fs::remove_dir_all(&empty));
}

/// Identity creation with the store's record of the identity there but not
/// examinable (a link that leads nowhere, or a folder that cannot be
/// searched): adoption refuses, and nothing is minted, attached, released or
/// overwritten. The refusal comes from the strict reading of the record
/// before anything is released (`identity_held`).
#[test]
fn records_store_an_unexaminable_identity_record_is_never_taken_for_absent_by_adoption() {
    for case in ["dangling link", "unsearchable folder"] {
        let _store = OwnStore::new();
        let first = folder("adopt-first-");
        records::append_project(&first, None, "writer:p", "evidence_limit", &APP_WRITER, body("P's entry")).unwrap();
        let p = attach(&first, false).unwrap().project.unwrap();
        // The person moves the project's folder: its link goes with it.
        let moved = first.with_file_name(format!("{}-moved", first.file_name().unwrap().to_string_lossy()));
        std::fs::rename(&first, &moved).unwrap();
        let store = opened().unwrap().0;
        let dir = project_dir(&store, &p);
        let record = dir.join("project.json");
        let roots_before = std::fs::read(store.join("roots.jsonl")).unwrap();
        let link_before = std::fs::read(moved.join(PROJECT_LINK)).unwrap();
        let record_before = std::fs::read(&record).unwrap();
        let refused = match case {
            "dangling link" => {
                std::fs::rename(&record, dir.join("project.json.kept")).unwrap();
                std::os::unix::fs::symlink(dir.join("nothing-here"), &record).unwrap();
                let refused = adopt(&moved);
                std::fs::remove_file(&record).unwrap();
                std::fs::rename(dir.join("project.json.kept"), &record).unwrap();
                refused
            }
            _ => unsearchable(&dir, || adopt(&moved)),
        };
        assert!(refused.as_ref().is_err_and(|e| e.contains("not known")), "{case}: {refused:?}");
        assert_eq!(std::fs::read(store.join("roots.jsonl")).unwrap(), roots_before, "{case}: no roots line appended");
        assert_eq!(std::fs::read(&record).unwrap(), record_before, "{case}: the record's bytes unchanged");
        assert_eq!(std::fs::read(moved.join(PROJECT_LINK)).unwrap(), link_before, "{case}: the project's link unchanged");
        assert!(attach(&moved, false).unwrap().dir.is_none(), "{case}: not attached");
        let _ = std::fs::remove_dir_all(&moved);
    }
}

/// The guard behind it, reached directly: the store's registration of an
/// identity whose record is a link that leads nowhere. create_json refuses:
/// here at its path check, which refuses a link, before its create-new
/// publication (an occupied plain file is refused by that publication, "File
/// exists"). No record is written over the link and no roots line follows.
/// (witness::begin runs before that publication. Here the witness had begun
/// when the identity was minted, so it writes nothing; in a store whose
/// witness had not begun it would begin it, listing what the store holds,
/// which says nothing about this project.)
#[test]
fn records_store_registration_never_writes_over_an_identity_record_it_could_not_examine() {
    let _store = OwnStore::new();
    let project = folder("register-guard-");
    records::append_project(&project, None, "writer:p", "evidence_limit", &APP_WRITER, body("P's entry")).unwrap();
    let p = attach(&project, false).unwrap().project.unwrap();
    let store = opened().unwrap().0;
    let dir = project_dir(&store, &p);
    let record = dir.join("project.json");
    std::fs::rename(&record, dir.join("project.json.kept")).unwrap();
    std::os::unix::fs::symlink(dir.join("nothing-here"), &record).unwrap();
    let roots_before = std::fs::read(store.join("roots.jsonl")).unwrap();
    // The witness began when the identity was minted; beginning is done once.
    let witness_before = std::fs::read(store.join(witness::WITNESS_FILE)).unwrap();
    let registered = register(&store, &p, "/invented/elsewhere", "adopted");
    assert!(registered.is_err(), "{registered:?}");
    assert_eq!(std::fs::read(store.join(witness::WITNESS_FILE)).unwrap(), witness_before, "the witness, begun earlier, is unchanged");
    assert_eq!(std::fs::read_link(&record).unwrap(), dir.join("nothing-here"), "the link is left as it was, not written over");
    assert_eq!(std::fs::read(store.join("roots.jsonl")).unwrap(), roots_before, "no roots line appended");
    let _ = std::fs::remove_dir_all(&project);
}

/// A pending capture submission already there but not examinable is never
/// replaced without being compared: the submission is refused and the
/// existing bytes stay as they were.
#[test]
fn records_store_an_unexaminable_pending_capture_is_never_replaced() {
    let library = folder("pending-capture-");
    let capture = json!({"captureId":"capture:invented","actKind":"A15"});
    let pending = json!({"capture":capture,"recordId":"record:invented","observedAt":"2026-11-13T00:00:00Z"});
    let path = storage::pending_file_for(&library, &capture).unwrap();
    std::fs::create_dir_all(path.parent().unwrap()).unwrap();
    let existing = serde_json::to_vec(&json!({"capture":capture,"recordId":"record:another","observedAt":"2026-11-12T00:00:00Z"})).unwrap();
    std::fs::write(&path, &existing).unwrap();
    // Its folder cannot be searched.
    let refused = unsearchable(path.parent().unwrap(), || records::persist_capture_submission(&library, &pending));
    assert!(refused.is_err(), "{refused:?}");
    assert_eq!(std::fs::read(&path).unwrap(), existing, "the existing pending capture is unchanged");
    // It is a link that leads nowhere.
    std::fs::remove_file(&path).unwrap();
    std::os::unix::fs::symlink(library.join("nothing-here"), &path).unwrap();
    let mut failing = pending.clone();
    let refused = records::note_capture_submission_failure(&library, &mut failing, "invented failure");
    assert!(refused.is_err(), "{refused:?}");
    assert_eq!(std::fs::read_link(&path).unwrap(), library.join("nothing-here"), "the link is left as it was");
    assert!(std::fs::symlink_metadata(library.join("nothing-here")).is_err(), "nothing written through it");
    let _ = std::fs::remove_dir_all(&library);
}
