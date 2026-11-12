//! RS §13.8 records store: placement and override, project identity (mint,
//! missing, changed, duplicated, moved, another store), the explicit import of
//! §13.7 records (byte-identical, verified, idempotent, counted once, drift a
//! limit, originals untouched), refusals, and readers reading the store.
use super::*;
use crate::records::{self, APP_WRITER};
use crate::storage;
use serde_json::json;

mod publication { include!("records_store_publication_tests.rs"); }

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

/// Review round 3, findings 1 and 2, repaired by form (App Agent 0): one
/// decision (`readable_home`, `ReadHome`) says where a project's records are
/// read, and it is the only product code that joins the project folder with
/// a records location. This holds the source to that: every product source
/// file that names such a location is listed here with how many of its lines
/// do and why they may. A new mention anywhere fails.
///
/// Its limit: a location built with none of these names, from a path a
/// caller passes in, is not seen here. The unrefusing home being private to
/// the store module is what the compiler holds on the store's side.
#[test]
fn the_places_that_name_a_records_location_in_the_project_folder_are_a_closed_list() {
    const NAMES: [&str; 9] = [
        "LEGACY_RECORDS", "LEGACY_LOG", "CAPTURES", "CAPTURE_STORE", "LEGACY_DIRECTORY",
        ".chirality/records", ".chirality/captures", "records/coordination.rs.jsonl", "\".chirality\"",
    ];
    const ALLOWED: [(&str, usize, &str); 11] = [
        ("records_store.rs", 14, "the one decision (ReadHome and the in-project accounts place), the import's census of what an earlier build left in the folder, and the folder the project link is written in"),
        ("storage.rs", 9, "the three names' definitions, the library's own act log and capture folder, and checks of the shape of a path already in hand"),
        ("connector_route_store.rs", 3, "the accounts folder's name and two comparisons of a path recorded in an account; the place itself comes from records_store::route_accounts_place"),
        ("act_control.rs", 2, "the A15 capture store's name and the library act log's recorded name: an A15 capture stays with its library"),
        ("act_control_a15.rs", 13, "the library's own capture store (A15 stays with its library) and that module's tests"),
        ("file_act_root.rs", 1, "a test's assertion that nothing was created"),
        ("fleet_records.rs", 1, "the census of the project's .chirality folder for the fleet view (DEL-06-01): project content, not a records location"),
        ("native_conversation_links.rs", 1, "the folder of the fleet copy published in the project: not a records location"),
        ("runtime_session.rs", 2, "test fixtures"),
        ("workflow_library.rs", 1, "the workflow supply folder"),
        ("workflow_package_copy.rs", 1, "the workflow package copy folder"),
    ];
    fn walk(dir: &std::path::Path, found: &mut BTreeMap<String, Vec<usize>>, base: &std::path::Path) {
        for entry in std::fs::read_dir(dir).unwrap() {
            let path = entry.unwrap().path();
            if path.is_dir() {
                walk(&path, found, base);
                continue;
            }
            let name = path.file_name().unwrap().to_string_lossy().into_owned();
            if !name.ends_with(".rs") || name.ends_with("_tests.rs") || name == "tests.rs" {
                continue;
            }
            let text = std::fs::read_to_string(&path).unwrap();
            let lines: Vec<usize> = text.lines().enumerate()
                .filter(|(_, line)| !line.trim_start().starts_with("//") && NAMES.iter().any(|n| line.contains(n)))
                .map(|(i, _)| i + 1).collect();
            if !lines.is_empty() {
                found.insert(path.strip_prefix(base).unwrap().to_string_lossy().into_owned(), lines);
            }
        }
    }
    let base = std::path::Path::new(env!("CARGO_MANIFEST_DIR")).join("src");
    let mut found = BTreeMap::new();
    walk(&base, &mut found, &base);
    let mut wrong = Vec::new();
    for (file, lines) in &found {
        match ALLOWED.iter().find(|(name, _, _)| name == file) {
            None => wrong.push(format!("{file} names a records location in the project folder (lines {lines:?}) and is not on the list")),
            Some((_, count, why)) if *count != lines.len() => wrong.push(format!("{file} has {} such lines (lines {lines:?}); the list allows {count}: {why}", lines.len())),
            Some(_) => {}
        }
    }
    for (file, _, _) in ALLOWED {
        if !found.contains_key(file) {
            wrong.push(format!("{file} is on the list and names no such location any more; take it off"));
        }
    }
    assert!(wrong.is_empty(), "a project's records are read where records_store::readable_home says, and nowhere else. Take the location from the ReadHome it returns (it refuses for a refused attachment). Only where the line is none of the project's record locations (a library's own store, a test, a shape check), change this list and say why:\n{}", wrong.join("\n"));
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
