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
fn a_missing_or_changed_project_file_is_a_limit_and_the_store_governs() {
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
    assert!(notes(&root).iter().any(|n| n.contains("link missing")));
    assert_eq!(status(Some(&root))["project"]["attachment"]["recordedHere"], governing.as_str());
    // The one-click restore attaches it again, with its history.
    assert_eq!(restore_link(&root).unwrap()["projectId"], governing.as_str());
    assert_eq!(storage::read_all(&root).0.len(), 1);
    records::append_project(&root, None, "writer:link", "evidence_limit", &APP_WRITER, body("restored")).unwrap();
    // Changed (an agent edits it): a limit; records never attach elsewhere.
    std::fs::write(root.join(PROJECT_LINK), serde_json::to_vec(&link_value("chirality-project:forged", "records-store:other")).unwrap()).unwrap();
    let changed = attach(&root, true).unwrap();
    assert_eq!(changed.project.as_deref(), Some(governing.as_str()));
    assert!(changed.limits[0].contains("chirality-project:forged") && changed.limits[0].contains("governs"));
    let (entries, limits) = storage::read_all(&root);
    assert!(limits.is_empty(), "{limits:?}");
    assert_eq!(entries.len(), 2, "both entries, in the governing project");
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
fn a_copied_project_is_duplicated_and_attaches_nothing_until_it_gets_its_own_identity() {
    let original = folder("dup-original-");
    records::append_project(&original, None, "writer:dup", "evidence_limit", &APP_WRITER, body("original")).unwrap();
    let id = attach(&original, false).unwrap().project.unwrap();
    let copy = folder("dup-copy-");
    std::fs::create_dir_all(copy.join(".chirality")).unwrap();
    std::fs::copy(original.join(PROJECT_LINK), copy.join(PROJECT_LINK)).unwrap();
    let dup = attach(&copy, true).unwrap();
    assert!(dup.dir.is_none() && dup.refusal.as_deref().unwrap().contains("duplicated project identity"), "{dup:?}");
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
    // "Cannot be read" is a rule, not a list: the account is read only as
    // its two written line forms of the supported version. A line that is
    // not JSON, a value that is not an object, an empty object, an import
    // line of another version or event, and a line without its identity or
    // its files each make the account unknown.
    let unknown: [&[u8]; 8] = [b"not json\n", b"{}\n", b"null\n", b"[]\n",
        b"{\"format\":\"chirality.records-store.import\",\"formatVersion\":\"99.0\",\"event\":\"future\"}\n",
        b"{\"format\":\"chirality.records-store.import\",\"formatVersion\":\"0.1\",\"event\":\"future\",\"importId\":\"import:x\"}\n",
        b"{\"format\":\"chirality.records-store.import\",\"formatVersion\":\"0.1\",\"event\":\"completed\",\"importId\":\"import:x\"}\n",
        b"{\"format\":\"chirality.records-store.import\",\"formatVersion\":\"0.1\",\"event\":\"started\",\"census\":[]}\n"];
    for (root, content) in [&imported, &empty].into_iter().flat_map(|root| unknown.iter().map(move |content| (root, *content))) {
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
            assert!(known(&e) || e.contains("import state is unknown"), "{what}: {e}");
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
    drop(own);
    for p in [imported, empty] { let _ = std::fs::remove_dir_all(p); }
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
