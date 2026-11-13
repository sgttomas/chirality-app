use super::*;
use crate::records_store::{Placement, Store};
struct Fixture {
    project: PathBuf,
    store: PathBuf,
    output: PathBuf,
    actor: Value,
    observed: Value,
}
impl Fixture {
    fn new() -> Self {
        let folder = |prefix| {
            let p = std::env::temp_dir().join(util::opaque_id(prefix).unwrap());
            std::fs::create_dir(&p).unwrap();
            std::fs::canonicalize(p).unwrap()
        };
        let f = Self {
            project: folder("retention-project-"),
            store: folder("retention-store-"),
            output: folder("retention-output-"),
            actor: crate::act_control::person(
                Some("Invented fixture person"),
                Some("invented-fixture-os"),
            ),
            observed: json!({"observedHome":{"codexAccount":"invented-fixture@example.invalid"},"fixture":"native callback test seam; no live person's act"}),
        };
        records_store::use_store_for_test(Some(Ok(Store {
            root: f.store.clone(),
            placement: Placement::Test,
            limits: vec![],
        })));
        f.record();
        f
    }
    fn record(&self) {
        crate::records::append_project(
            &self.project,
            None,
            "app-writer:fixture",
            "evidence_limit",
            &crate::records::APP_WRITER,
            json!({"label":"unresolvable reference","subjectRef":"invented retention fixture"}),
        )
        .unwrap();
    }
    fn dir(&self) -> PathBuf {
        records_store::attach(&self.project, false)
            .unwrap()
            .dir
            .unwrap()
    }
    fn act(&self, action: &str, bag: Option<&Path>) -> Result<Value, String> {
        let p = prepare(&self.project, action, bag, &self.actor, &self.observed)?;
        apply(p, &self.actor, &self.observed)
    }
    fn export(&self, name: &str) -> PathBuf {
        let bag = self.output.join(name);
        crate::records_export::export(&self.project, &bag).unwrap();
        bag
    }
}
impl Drop for Fixture {
    fn drop(&mut self) {
        records_store::use_store_for_test(None);
        for p in [&self.project, &self.store, &self.output] {
            let _ = std::fs::remove_dir_all(p);
        }
    }
}
#[test]
fn records_retention_imported_package_can_be_exported_disposed_and_remains_terminal() {
    let f = Fixture::new();
    let source = f.export("source-package");
    records_store::use_store_for_test(Some(Ok(Store {
        root: f.output.join("destination-store"),
        placement: Placement::Test,
        limits: vec![],
    })));
    let imported =
        records_store::package::prepare(&f.project, &source, &f.actor, &f.observed).unwrap();
    records_store::package::apply(imported, &f.actor, &f.observed).unwrap();
    let dir = f.dir();
    assert!(dir.join("package-imports").is_dir());
    let stale_plan =
        records_store::package::prepare(&f.project, &source, &f.actor, &f.observed).unwrap();
    f.act("close", None).unwrap();
    let bag = f.export("closed-imported-package");
    let result = f.act("dispose", Some(&bag)).unwrap();
    assert_eq!(result["state"], "disposed");
    assert!(!dir.exists());
    assert_eq!(view(&dir)["disposition"], "disposed");
    assert!(records_store::write_dir(&f.project).is_err());
    assert!(records_store::home(&f.project).is_err());
    for action in ["import", "restore", "resume"] {
        let refused = match action {
            "import" => records_store::package::prepare(&f.project, &source, &f.actor, &f.observed),
            "restore" => {
                records_store::package::prepare_restore(&f.project, &source, &f.actor, &f.observed)
            }
            _ => records_store::package::prepare_resume(&f.project, &f.actor, &f.observed),
        };
        assert!(refused.is_err(), "{action} must refuse disposed records");
        assert!(
            !dir.exists(),
            "{action} must not recreate disposed payload for locks"
        );
    }
    assert!(records_store::package::apply(stale_plan, &f.actor, &f.observed).is_err());
    assert!(
        !dir.exists(),
        "a stale native plan cannot recreate disposed payload"
    );
    assert!(crate::records_export::verify(&source).is_ok());
    assert!(crate::records_export::verify(&bag).is_ok());
}
#[test]
fn records_store_completed_package_history_moves_with_the_store_without_rewriting_native_intent() {
    let f = Fixture::new();
    let source = f.export("source-before-store-move");
    let destination = f.output.join("destination-store");
    records_store::use_store_for_test(Some(Ok(Store {
        root: destination.clone(),
        placement: Placement::Test,
        limits: vec![],
    })));
    let plan = records_store::package::prepare(&f.project, &source, &f.actor, &f.observed).unwrap();
    records_store::package::apply(plan, &f.actor, &f.observed).unwrap();
    let dir = f.dir();
    let key = dir.file_name().unwrap().to_owned();
    let journal = destination
        .join("administration")
        .join(&key)
        .join("package-imports");
    let controls = std::fs::read_dir(&journal)
        .unwrap()
        .map(|entry| {
            let path = entry.unwrap().path();
            (
                path.file_name().unwrap().to_owned(),
                std::fs::read(path).unwrap(),
            )
        })
        .collect::<Vec<_>>();
    let moved = f.output.join("moved-store");
    std::fs::rename(&destination, &moved).unwrap();
    records_store::use_store_for_test(Some(Ok(Store {
        root: moved.clone(),
        placement: Placement::Test,
        limits: vec![],
    })));
    let home = records_store::home(&f.project).unwrap();
    assert!(home.store_mode);
    assert!(crate::storage::sources(&f.project).is_ok());
    f.record();
    let exported = f.export("export-after-store-move");
    assert!(crate::records_export::verify(&exported).is_ok());
    for (name, bytes) in controls {
        assert_eq!(
            std::fs::read(
                moved
                    .join("administration")
                    .join(&key)
                    .join("package-imports")
                    .join(name)
            )
            .unwrap(),
            bytes,
            "historical native intent and completion bytes remain unchanged"
        );
    }
}
#[test]
fn records_retention_hold_close_export_dispose_and_tombstone_preserve_other_evidence() {
    let f = Fixture::new();
    let dir = f.dir();
    let id = records_store::attach(&f.project, false)
        .unwrap()
        .project
        .unwrap();
    std::fs::create_dir_all(f.project.join(".chirality/fleet")).unwrap();
    std::fs::write(
        f.project.join(".chirality/fleet/coordination.fleet.jsonl"),
        b"co-written project evidence",
    )
    .unwrap();
    std::fs::create_dir_all(f.project.join(".chirality/records")).unwrap();
    std::fs::write(
        f.project.join(".chirality/records/acts.jsonl"),
        b"library evidence",
    )
    .unwrap();
    f.act("set-hold", None).unwrap();
    f.act("close", None).unwrap();
    let bag = f.export("held-bag");
    assert!(f
        .act("dispose", Some(&bag))
        .unwrap_err()
        .contains("legal hold"));
    f.act("release-hold", None).unwrap();
    assert!(f
        .act("dispose", Some(&bag))
        .unwrap_err()
        .contains("administrative history is stale"));
    let bag = f.export("current-bag");
    let result = f.act("dispose", Some(&bag)).unwrap();
    assert_eq!(result["state"], "disposed");
    assert!(!dir.exists());
    assert_eq!(state(&dir).unwrap().sequence, 5);
    assert!(state(&dir).unwrap().completed);
    assert!(crate::records_export::verify(&bag).is_ok());
    assert_eq!(
        std::fs::read(f.project.join(".chirality/fleet/coordination.fleet.jsonl")).unwrap(),
        b"co-written project evidence"
    );
    assert_eq!(
        std::fs::read(f.project.join(".chirality/records/acts.jsonl")).unwrap(),
        b"library evidence"
    );
    assert_eq!(
        records_store::attach(&f.project, true)
            .unwrap()
            .project
            .as_deref(),
        Some(id.as_str())
    );
    assert!(records_store::write_dir(&f.project).is_err());
    assert!(records_store::import(&f.project).is_err());
    assert!(records_store::new_identity(&f.project).is_err());
    // Putting the project file back reads no record and reopens nothing: it
    // stays possible, and the disposed payload stays gone and unwritable.
    assert!(records_store::restore_link(&f.project).is_ok());
    assert!(records_store::write_dir(&f.project).is_err());
    assert!(storage::create_json(&dir.join("captures/resurrection.json"), &json!({})).is_err());
    assert!(!dir.exists());
    assert!(storage::sources(&f.project).is_err());
    std::fs::remove_file(f.project.join(records_store::PROJECT_LINK)).unwrap();
    assert!(storage::sources(&f.project).is_err());
    assert!(records_store::new_identity(&f.project).is_err());
}
#[test]
fn records_retention_freezes_actor_legal_hold_payload_and_export_after_native_question() {
    let f = Fixture::new();
    f.act("close", None).unwrap();
    let bag = f.export("bag");
    let p = prepare(&f.project, "dispose", Some(&bag), &f.actor, &f.observed).unwrap();
    let mut actor = f.actor.clone();
    actor["displayName"] = json!("another person");
    assert!(apply(p, &actor, &f.observed).is_err());
    assert!(f.dir().exists());
    let p = prepare(&f.project, "dispose", Some(&bag), &f.actor, &f.observed).unwrap();
    f.act("set-hold", None).unwrap();
    assert!(apply(p, &f.actor, &f.observed).is_err());
    f.act("release-hold", None).unwrap();
    let bag = f.export("fresh-bag");
    let p = prepare(&f.project, "dispose", Some(&bag), &f.actor, &f.observed).unwrap();
    std::fs::write(f.dir().join("late-evidence.json"), b"a late external write").unwrap();
    assert!(apply(p, &f.actor, &f.observed).is_err());
    assert!(f.dir().exists());
    std::fs::remove_file(f.dir().join("late-evidence.json")).unwrap();
    let p = prepare(&f.project, "dispose", Some(&bag), &f.actor, &f.observed).unwrap();
    std::fs::write(bag.join("data/project.json"), b"edited export").unwrap();
    assert!(apply(p, &f.actor, &f.observed).is_err());
}
#[test]
fn records_retention_no_automatic_disposal_closed_write_denial_reopen_and_active_lease() {
    let f = Fixture::new();
    let lease = activity(&f.project).unwrap();
    assert!(f
        .act("close", None)
        .unwrap_err()
        .contains("Project activity"));
    drop(lease);
    f.act("close", None).unwrap();
    assert!(f.dir().exists());
    assert!(records_store::write_dir(&f.project).is_err());
    assert!(activity(&f.project).is_err());
    f.act("reopen", None).unwrap();
    f.record();
    assert!(activity(&f.project).is_ok());
}
#[test]
fn records_retention_partial_disposal_recovery_requires_original_unchanged_bag_and_remaining_subset(
) {
    let f = Fixture::new();
    f.act("close", None).unwrap();
    let bag = f.export("bag");
    let dir = f.dir();
    fail_remove_for_test(true);
    let error = f.act("dispose", Some(&bag)).unwrap_err();
    fail_remove_for_test(false);
    assert!(error.contains("disposal incomplete"));
    assert!(state(&dir).unwrap().disposition.is_some());
    assert!(records_store::write_dir(&f.project).is_err());
    let one = crate::records_export::payload_paths_for_test(&dir)
        .into_iter()
        .find(|p| p.file_name().unwrap() != "project.json")
        .unwrap();
    std::fs::remove_file(one).unwrap();
    std::fs::write(dir.join("unexported.json"), b"new unexported file").unwrap();
    assert!(f.act("resume-disposal", None).is_err());
    std::fs::remove_file(dir.join("unexported.json")).unwrap();
    assert_eq!(f.act("resume-disposal", None).unwrap()["state"], "disposed");
    assert!(!dir.exists());
}
#[test]
fn records_retention_a_link_changed_during_an_unfinished_disposal_can_be_restored_and_the_disposal_finished() {
    let f = Fixture::new();
    f.act("close", None).unwrap();
    let bag = f.export("bag");
    let dir = f.dir();
    let project = records_store::attach(&f.project, false).unwrap().project.unwrap();
    fail_remove_for_test(true);
    assert!(f.act("dispose", Some(&bag)).unwrap_err().contains("disposal incomplete"));
    fail_remove_for_test(false);
    // The project file is edited while the disposal stands unfinished.
    let link = f.project.join(records_store::PROJECT_LINK);
    let mut changed: Value = serde_json::from_slice(&std::fs::read(&link).unwrap()).unwrap();
    changed["projectId"] = json!("chirality-project:invented-other");
    std::fs::write(&link, serde_json::to_vec(&changed).unwrap()).unwrap();
    let attachment = records_store::attach(&f.project, false).unwrap();
    assert_eq!((attachment.fault, attachment.recorded.as_deref()), (Some("link changed"), Some(project.as_str())));
    assert!(attachment.resolutions.contains(&"restore-link"));
    assert!(f.act("resume-disposal", None).is_err(), "the disposal cannot be finished for a folder that is not attached");
    // Restoring the link reads no record, so the standing disposal does not
    // refuse it; then the same disposal is finished.
    assert_eq!(records_store::restore_link(&f.project).unwrap()["projectId"], project.as_str());
    assert_eq!(f.act("resume-disposal", None).unwrap()["state"], "disposed");
    assert!(!dir.exists());
    // And after the disposal is complete the link can still be put back.
    std::fs::remove_file(&link).unwrap();
    assert_eq!(records_store::restore_link(&f.project).unwrap()["projectId"], project.as_str());
}
#[test]
fn records_retention_strict_history_and_uncertain_publication_never_enable_disposal() {
    let f = Fixture::new();
    f.act("close", None).unwrap();
    let dir = f.dir();
    let events = control(&dir).unwrap().join("events");
    std::fs::write(
        events.join("00000000000000000002.json"),
        b"{\"action\":\"set-hold\"",
    )
    .unwrap();
    assert!(state(&dir).is_err());
    assert!(records_store::write_dir(&f.project).is_err());
    assert!(f.act("dispose", None).is_err());
    std::fs::remove_file(events.join("00000000000000000002.json")).unwrap();
    FAIL_ADMIN_PUBLICATION.with(|flag| flag.set(true));
    assert!(f.act("set-hold", None).unwrap_err().contains("durable"));
    FAIL_ADMIN_PUBLICATION.with(|flag| flag.set(false));
    storage::fail_directory_for_test(None);
    assert!(state(&dir).unwrap().hold);
    assert!(f.act("dispose", None).is_err());
    assert!(f.dir().exists());
}
/// Alters the first line of the fixture's log in the store after a second
/// line was written, so that line's link no longer names it. Returns the
/// log's path within the project's store folder.
fn break_chain(f: &Fixture) -> String {
    f.record();
    let log = crate::storage::project_log(&f.project, None, "app-writer:fixture").unwrap();
    let mut bytes = std::fs::read(&log).unwrap();
    let at = bytes.windows(8).position(|w| w == b"invented").unwrap();
    bytes[at] = b'I';
    std::fs::write(&log, bytes).unwrap();
    log.strip_prefix(f.dir()).unwrap().to_str().unwrap().to_owned()
}
fn dispose_entry(dir: &Path) -> Value {
    let events = control(dir).unwrap().join("events");
    let mut found = None;
    for entry in std::fs::read_dir(events).unwrap() {
        let v: Value = serde_json::from_slice(&std::fs::read(entry.unwrap().path()).unwrap()).unwrap();
        if v["action"] == "dispose" { found = Some(v); }
    }
    found.unwrap()
}
#[test]
fn records_retention_disposal_relying_on_an_export_with_a_broken_chain_is_not_refused_and_states_and_records_the_limit() {
    let f = Fixture::new();
    let rel = break_chain(&f);
    let dir = f.dir();
    f.act("close", None).unwrap();
    let bag = f.export("bag");
    let p = prepare(&f.project, "dispose", Some(&bag), &f.actor, &f.observed).unwrap();
    assert_eq!(p.context["export"]["logIntegrity"]["state"], "limited");
    // Its own statement in the native question, with the log and the line.
    let asked = statement(&p).unwrap();
    assert!(asked.text.contains("Log integrity: LIMITED."), "{}", asked.text);
    assert!(asked.text.contains("This is the export you are relying on, and this is recorded with the disposal."), "{}", asked.text);
    match &asked.in_app {
        None => assert!(asked.text.contains(&format!("{rel}: chain broken at line 2")), "{}", asked.text),
        // The bounded summary names the line whole; the App shows every limit.
        Some(shown) => {
            assert!(asked.text.contains("1 limit(s); each is named in full in the App under this confirmation."), "{}", asked.text);
            assert!(shown.content["export"]["logIntegrity"]["limits"][0].as_str().unwrap().contains(&format!("{rel}: chain broken at line 2")));
        }
    }
    let summary = crate::records_export::integrity_summary(&p.context["export"]["logIntegrity"]).unwrap();
    assert!(summary.contains("1 limit(s); each is named in full in the App under this confirmation."), "{summary}");
    assert!(p.context["export"]["verification"].as_str().unwrap().contains("separately, log integrity: limited (1,"), "the verification sentence read alone is not a clean pass");
    // Not refused, and recorded with the act.
    let result = apply(p, &f.actor, &f.observed).unwrap();
    assert_eq!(result["state"], "disposed");
    assert_eq!(result["exportLogIntegrity"]["state"], "limited");
    assert!(result["standing"].as_str().unwrap().contains("Log integrity: LIMITED."), "{result}");
    let entry = dispose_entry(&dir);
    assert_eq!(entry["export"]["logIntegrity"]["state"], "limited");
    assert!(entry["export"]["logIntegrity"]["limits"][0].as_str().unwrap().contains(&format!("{rel}: chain broken at line 2")), "{entry}");
    assert_eq!(view(&dir)["disposalExportLogIntegrity"], entry["export"]["logIntegrity"]);
}
#[test]
fn records_retention_disposal_always_records_whether_the_export_states_a_broken_chain_and_an_older_entry_reads_as_not_stated() {
    // An export with no chain recorded broken: stated as such, and the
    // question makes no integrity statement.
    let f = Fixture::new();
    let dir = f.dir();
    f.act("close", None).unwrap();
    let bag = f.export("bag");
    let p = prepare(&f.project, "dispose", Some(&bag), &f.actor, &f.observed).unwrap();
    assert_eq!(p.context["export"]["logIntegrity"], json!({"state":"no chain recorded broken"}));
    assert!(!statement(&p).unwrap().text.contains("Log integrity"));
    apply(p, &f.actor, &f.observed).unwrap();
    assert_eq!(dispose_entry(&dir)["export"]["logIntegrity"], json!({"state":"no chain recorded broken"}));
    assert_eq!(view(&dir)["disposalExportLogIntegrity"]["state"], "no chain recorded broken");
    drop(f);
    // A disposal act recorded before the member existed (its export object
    // as that build wrote it), left incomplete. It still reads; its absent
    // member is "not stated", never "no chain recorded broken"; and the
    // resumed disposal carries the member from its own check of the export.
    let f = Fixture::new();
    let rel = break_chain(&f);
    let dir = f.dir();
    f.act("close", None).unwrap();
    let bag = f.export("bag");
    crate::records_export::BEFORE_LOG_INTEGRITY.with(|b| b.set(true));
    fail_remove_for_test(true);
    let error = f.act("dispose", Some(&bag)).unwrap_err();
    fail_remove_for_test(false);
    crate::records_export::BEFORE_LOG_INTEGRITY.with(|b| b.set(false));
    assert!(error.contains("disposal incomplete"), "{error}");
    let entry = dispose_entry(&dir);
    assert!(entry["export"].get("logIntegrity").is_none(), "{entry}");
    let older = view(&dir);
    assert_eq!(older["disposition"], "disposal incomplete", "the older entry still reads");
    assert_eq!(older["disposalExportLogIntegrity"], json!({"state":"not stated"}));
    let resume = prepare(&f.project, "resume-disposal", None, &f.actor, &f.observed).unwrap();
    assert_eq!(resume.context["export"]["logIntegrity"]["state"], "limited");
    assert!(resume.context["export"]["logIntegrity"]["limits"][0].as_str().unwrap().contains(&format!("{rel}: chain broken at line 2")));
    assert!(statement(&resume).unwrap().text.contains("Log integrity: LIMITED."));
    let result = apply(resume, &f.actor, &f.observed).unwrap();
    assert_eq!(result["state"], "disposed");
    assert_eq!(result["exportLogIntegrity"]["state"], "limited");
    assert_eq!(view(&dir)["disposalExportLogIntegrity"], json!({"state":"not stated"}), "the original act is not rewritten");
}
#[test]
fn records_retention_stale_member_bytes_and_legacy_bag_do_not_satisfy_disposal() {
    let f = Fixture::new();
    let old = f.export("old");
    f.record();
    f.act("close", None).unwrap();
    assert!(f.act("dispose", Some(&old)).is_err());
    let bag = f.export("current");
    crate::records_export::legacy_for_test(&bag);
    assert!(
        crate::records_export::verify(&bag).unwrap()["administration"]
            .as_str()
            .unwrap()
            .contains("unknown")
    );
    assert!(f
        .act("dispose", Some(&bag))
        .unwrap_err()
        .contains("legacy export"));
}
#[test]
fn records_retention_a_writer_waiting_at_admission_rechecks_closure_before_creating_anything() {
    let f = Fixture::new();
    let dir = f.dir();
    let target = dir.join("captures/queued.json");
    let gate = storage::lock(&gate(&dir).unwrap()).unwrap();
    let store = f.store.clone();
    let next = target.clone();
    let (ready, arrived) = std::sync::mpsc::channel();
    let writer = std::thread::spawn(move || {
        records_store::use_store_for_test(Some(Ok(Store {
            root: store,
            placement: Placement::Test,
            limits: vec![],
        })));
        ready.send(()).unwrap();
        let r = storage::create_json(&next, &json!({"queued":"before closure"}));
        records_store::use_store_for_test(None);
        r
    });
    arrived.recv().unwrap();
    let s = state(&dir).unwrap();
    let captured = json!({"projectId":records_store::attach(&f.project,false).unwrap().project,"projectRoot":f.project,"storeId":records_store::status(None)["storeId"],"fixture":"original confirmed native close"});
    event(&dir, &s, "close", Some(&f.actor), &captured).unwrap();
    drop(gate);
    assert!(writer.join().unwrap().unwrap_err().contains("closed"));
    assert!(!target.exists());
}

#[test]
fn records_retention_retry_reflushes_administration_ancestors_before_any_disposal() {
    let f = Fixture::new();
    let dir = f.dir();
    std::fs::remove_dir_all(f.store.join("administration")).unwrap();
    storage::fail_directory_for_test(Some(f.store.clone()));
    assert!(prepare(&f.project, "close", None, &f.actor, &f.observed).is_err());
    storage::fail_directory_for_test(None);
    // The failed first attempt left visible directories. Existence alone cannot
    // establish the durability of their link in the store root.
    assert!(control(&dir).unwrap().exists());
    storage::fail_directory_for_test(Some(f.store.clone()));
    assert!(f.act("close", None).is_err());
    storage::fail_directory_for_test(None);
    assert_eq!(state(&dir).unwrap().sequence, 0);
    assert!(dir.exists());
    f.act("close", None).unwrap();
    let bag = f.export("bag");
    storage::fail_directory_for_test(Some(f.store.clone()));
    assert!(f.act("dispose", Some(&bag)).is_err());
    storage::fail_directory_for_test(None);
    assert!(dir.exists());
    assert!(state(&dir).unwrap().disposition.is_none());
    assert_eq!(f.act("dispose", Some(&bag)).unwrap()["state"], "disposed");
}

#[test]
fn records_retention_recovery_refuses_a_replacement_payload_folder_even_with_identical_files() {
    let f = Fixture::new();
    f.act("close", None).unwrap();
    let bag = f.export("bag");
    let dir = f.dir();
    fail_remove_for_test(true);
    assert!(f.act("dispose", Some(&bag)).is_err());
    fail_remove_for_test(false);
    let old = dir.with_extension("original");
    std::fs::rename(&dir, &old).unwrap();
    std::fs::create_dir(&dir).unwrap();
    for source in crate::records_export::payload_paths_for_test(&old) {
        let relative = source.strip_prefix(&old).unwrap();
        let to = dir.join(relative);
        std::fs::create_dir_all(to.parent().unwrap()).unwrap();
        std::fs::copy(source, to).unwrap();
    }
    assert!(f
        .act("resume-disposal", None)
        .unwrap_err()
        .contains("folder was replaced"));
    assert!(dir.exists());
    std::fs::remove_dir_all(&dir).unwrap();
    std::fs::rename(old, &dir).unwrap();
    assert_eq!(f.act("resume-disposal", None).unwrap()["state"], "disposed");
}

#[test]
fn records_retention_canonical_supplier_stop_releases_activity_while_host_stays_alive() {
    use std::os::unix::fs::PermissionsExt;
    use std::time::{Duration, Instant};
    let f = Fixture::new();
    let peer = f.output.join("peer.py");
    std::fs::write(&peer,r#"#!/usr/bin/python3
import json,sys
if '--version' in sys.argv:
 print('codex-cli 0.167.0');sys.exit(0)
for line in sys.stdin:
 frame=json.loads(line)
 if frame.get('method')=='initialize':
  print(json.dumps({'id':frame['id'],'result':{'userAgent':'invented canonical retention fixture'}}),flush=True)
"#).unwrap();
    std::fs::set_permissions(&peer, std::fs::Permissions::from_mode(0o700)).unwrap();
    for home in ["home", "probe"] {
        std::fs::create_dir(f.output.join(home)).unwrap();
    }
    let mut cfg = crate::hosting::HostConfig::new(
        peer,
        f.output.join("home"),
        f.output.join("probe"),
        f.project.clone(),
    );
    cfg.allow_unverified_dev = true;
    cfg.wait_limit = Duration::from_secs(2);
    assert!(cfg.distribution.is_none());
    let host = std::sync::Arc::new(crate::hosting::Host::new());
    host.start(&cfg, "invented fixture person").unwrap();
    assert!(f.act("close", None).is_err());
    host.stop("invented fixture person", "fixture end").unwrap();
    let deadline = Instant::now() + Duration::from_secs(3);
    let plan = loop {
        match prepare(&f.project, "close", None, &f.actor, &f.observed) {
            Ok(plan) => break plan,
            Err(e) => {
                assert!(
                    Instant::now() < deadline,
                    "stopped canonical Host retained activity: {e}"
                );
                std::thread::sleep(Duration::from_millis(10));
            }
        }
    };
    assert_eq!(
        apply(plan, &f.actor, &f.observed).unwrap()["action"],
        "close"
    );
    assert_eq!(host.state(), "stopped");
    // The no-project host path still starts independently and never mints a
    // project identity in a temporary cwd merely for an activity lease.
    cfg.cwd = f.output.clone();
    cfg.records_project = false;
    host.start(&cfg, "invented no-project fixture person")
        .unwrap();
    host.stop("invented no-project fixture person", "fixture end")
        .unwrap();
    assert!(!f.output.join(records_store::PROJECT_LINK).exists());
}

#[test]
fn records_retention_cached_index_source_and_live_capability_cannot_resurrect_imported_originals() {
    use crate::records_access::RecordsSource;
    let f = Fixture::new();
    let hot = crate::records::append_project(
        &f.project,
        Some("run:retention-hot"),
        "app-writer:fixture",
        "evidence_limit",
        &crate::records::APP_WRITER,
        json!({"label":"unresolvable reference","subjectRef":"hot retention marker"}),
    )
    .unwrap();
    let legacy = f.project.join(".chirality/records").join(storage::log_rel(
        Some("run:retention-legacy"),
        "writer:legacy",
    ));
    std::fs::create_dir_all(legacy.parent().unwrap()).unwrap();
    let historical = crate::records::envelope(
        "evidence_limit",
        &crate::records::APP_WRITER,
        json!({"label":"unresolvable reference","subjectRef":"retained original marker"}),
        "rec:app:retention-legacy".into(),
        1,
        Some("run:retention-legacy"),
        None,
    );
    let original = format!("{historical}\n");
    std::fs::write(&legacy, &original).unwrap();
    records_store::import(&f.project).unwrap();
    let ids = [
        hot["recordId"].as_str().unwrap(),
        "rec:app:retention-legacy",
    ];
    for id in ids {
        assert!(crate::records_index::with_index(&f.project, |ix| ix.holds(id)));
        assert_eq!(
            crate::records_index::with_index(&f.project, |ix| ix.entries_with(id).unwrap()).len(),
            1
        );
    }
    let warm_wr = crate::workflow_workspace::publication::ProjectRecords::open(&f.project).unwrap();
    warm_wr.list_references().unwrap();
    let source = crate::records_access::ProjectPaths::new(&f.project);
    assert!(source
        .read()
        .entries
        .iter()
        .any(|e| e.entry["recordId"] == ids[1]));
    let capability = crate::records_access::RecordsCapability::new(&f.project).unwrap();
    let call = |n| crate::records_access::Call {
        app_session: "fixture".into(),
        generation: "g:fixture".into(),
        request: json!(n),
        thread: "thread".into(),
        turn: "turn".into(),
        call: format!("call-{n}"),
        arguments: json!({"operation":"read_run","run":"run:retention-legacy"}),
    };
    assert_eq!(
        capability.answer(&call(1), Some(f.project.to_str().unwrap()))["success"],
        true
    );
    let id = records_store::attach(&f.project, false)
        .unwrap()
        .project
        .unwrap();
    f.act("close", None).unwrap();
    let bag = f.export("bag");
    f.act("dispose", Some(&bag)).unwrap();
    for key in ids {
        assert!(!crate::records_index::with_index(&f.project, |ix| ix.holds(key)));
        assert!(
            crate::records_index::with_index(&f.project, |ix| ix.entries_with(key).unwrap())
                .is_empty()
        );
    }
    assert!(source.read().entries.is_empty());
    let answer = capability.answer(&call(2), Some(f.project.to_str().unwrap()));
    assert_eq!(answer["success"], false);
    assert!(!answer.to_string().contains("retained original marker"));
    assert!(!f.dir().exists());
    let restored = f.dir();
    for source in crate::records_export::payload_paths_for_test(&bag.join("data")) {
        let relative = source.strip_prefix(bag.join("data")).unwrap();
        let to = restored.join(relative);
        std::fs::create_dir_all(to.parent().unwrap()).unwrap();
        std::fs::copy(source, to).unwrap();
    }
    assert!(
        source.read().entries.is_empty(),
        "restoring disposed payload does not restore authority or ordinary source discovery"
    );
    for key in ids {
        assert!(!crate::records_index::with_index(&f.project, |ix| ix.holds(key)));
        assert!(
            crate::records_index::with_index(&f.project, |ix| ix.entries_with(key).unwrap())
                .is_empty()
        );
    }
    for n in 0..5 {
        let other = f.output.join(format!("other-index-{n}"));
        std::fs::create_dir(&other).unwrap();
        crate::records_index::with_index(&other, |_| ());
    }
    for key in ids {
        assert!(
            !crate::records_index::with_index(&f.project, |ix| ix.holds(key)),
            "fresh index also rejects recreated disposed records"
        );
    }
    assert!(
        warm_wr.list_references().is_err(),
        "cached WR reader rejects recreated disposed payload"
    );
    let wr = crate::workflow_workspace::publication::ProjectRecords::open(&f.project).unwrap();
    assert!(wr.list_references().is_err());
    assert_eq!(std::fs::read_to_string(&legacy).unwrap(), original);
    assert_eq!(
        records_store::attach(&f.project, true)
            .unwrap()
            .project
            .as_deref(),
        Some(id.as_str())
    );
    std::fs::remove_file(f.project.join(records_store::PROJECT_LINK)).unwrap();
    assert!(source.read().entries.is_empty());
    assert!(capability.answer(&call(3), Some(f.project.to_str().unwrap()))["success"] == false);
    assert!(!f.project.join(records_store::PROJECT_LINK).exists());
    assert!(records_store::write_dir(&f.project).is_err());
    assert!(!f.project.join(records_store::PROJECT_LINK).exists());
}
#[test]
fn records_retention_visible_but_uncertain_completion_has_a_resync_path_without_a_new_act() {
    let f = Fixture::new();
    f.act("close", None).unwrap();
    let bag = f.export("bag");
    let dir = f.dir();
    FAIL_COMPLETION_PUBLICATION.with(|flag| flag.set(true));
    let e = f.act("dispose", Some(&bag)).unwrap_err();
    FAIL_COMPLETION_PUBLICATION.with(|flag| flag.set(false));
    storage::fail_directory_for_test(None);
    assert!(e.contains("records removed; completion publication durability uncertain"));
    assert!(!dir.exists());
    assert_eq!(view(&dir)["disposition"], "completion durability uncertain");
    let sequence = state(&dir).unwrap().sequence;
    assert_eq!(f.act("resume-disposal", None).unwrap()["state"], "disposed");
    assert_eq!(
        state(&dir).unwrap().sequence,
        sequence,
        "reconciliation records no second person's disposal or second completion event"
    );
    assert_eq!(view(&dir)["disposition"], "disposed");
}
#[test]
fn records_retention_completion_resync_returns_the_resumed_checks_finding_about_the_export() {
    // An older disposal act (no logIntegrity member) whose completion was
    // visible but not confirmed durable, relying on an export with a broken
    // chain. The resync performs no new act, and still says what the resumed
    // check found about the export.
    let f = Fixture::new();
    let rel = break_chain(&f);
    f.act("close", None).unwrap();
    let bag = f.export("bag");
    let dir = f.dir();
    crate::records_export::BEFORE_LOG_INTEGRITY.with(|b| b.set(true));
    FAIL_COMPLETION_PUBLICATION.with(|flag| flag.set(true));
    let e = f.act("dispose", Some(&bag)).unwrap_err();
    FAIL_COMPLETION_PUBLICATION.with(|flag| flag.set(false));
    crate::records_export::BEFORE_LOG_INTEGRITY.with(|b| b.set(false));
    storage::fail_directory_for_test(None);
    assert!(e.contains("completion publication durability uncertain"), "{e}");
    assert_eq!(view(&dir)["disposition"], "completion durability uncertain");
    let sequence = state(&dir).unwrap().sequence;
    let result = f.act("resume-disposal", None).unwrap();
    assert_eq!(result["state"], "disposed");
    assert_eq!(result["exportLogIntegrity"]["state"], "limited");
    assert!(result["exportLogIntegrity"]["limits"][0].as_str().unwrap().contains(&format!("{rel}: chain broken at line 2")), "{result}");
    assert!(result["standing"].as_str().unwrap().contains("Log integrity: LIMITED."), "{result}");
    assert_eq!(state(&dir).unwrap().sequence, sequence, "no second act");
    assert_eq!(view(&dir)["disposalExportLogIntegrity"], json!({"state":"not stated"}), "the original act is not rewritten");
}
#[test]
fn records_retention_disposed_unlinked_project_never_falls_back_when_store_becomes_unavailable() {
    let f = Fixture::new();
    let legacy = f.project.join(".chirality/records/runs/legacy.jsonl");
    std::fs::create_dir_all(legacy.parent().unwrap()).unwrap();
    let line = crate::records::envelope(
        "evidence_limit",
        &crate::records::APP_WRITER,
        json!({"label":"unresolvable reference","subjectRef":"retained original"}),
        "rec:app:retained-original".into(),
        1,
        Some("run:retained"),
        None,
    );
    std::fs::write(&legacy, format!("{line}\n")).unwrap();
    records_store::import(&f.project).unwrap();
    f.act("close", None).unwrap();
    let bag = f.export("bag");
    f.act("dispose", Some(&bag)).unwrap();
    std::fs::remove_file(f.project.join(records_store::PROJECT_LINK)).unwrap();
    let moved = f.output.join("store-temporarily-unavailable");
    std::fs::rename(&f.store, &moved).unwrap();
    assert!(storage::sources(&f.project).is_err());
    assert!(storage::read_all(&f.project).0.is_empty());
    assert!(
        !f.store.exists(),
        "a missing opened store is never silently recreated"
    );
    std::fs::rename(moved, &f.store).unwrap();
    std::fs::rename(
        f.store.join("store.json"),
        f.store.join("store.json.unavailable"),
    )
    .unwrap();
    assert!(storage::sources(&f.project).is_err());
    assert!(storage::read_all(&f.project).0.is_empty());
    // The explicit library evidence reader remains usable independently.
    let library = f.output.join("library");
    std::fs::create_dir(&library).unwrap();
    crate::records::append(
        &storage::library_log(&library),
        "evidence_limit",
        &crate::records::APP_WRITER,
        json!({"label":"unresolvable reference","subjectRef":"library-only evidence"}),
    )
    .unwrap();
    assert_eq!(crate::records::library_record_set(&library).0.len(), 1);
    assert!(records_store::write_dir(&f.project).is_err());
    assert!(!f.project.join(records_store::PROJECT_LINK).exists());
}
#[test]
fn records_retention_closed_project_can_be_explicitly_adopted_after_move_without_reopening() {
    let f = Fixture::new();
    let original = records_store::attach(&f.project, false)
        .unwrap()
        .project
        .unwrap();
    f.act("set-hold", None).unwrap();
    f.act("close", None).unwrap();
    let before = std::fs::read(f.dir().join("project.json")).unwrap();
    let moved = f.output.join("moved-project");
    std::fs::rename(&f.project, &moved).unwrap();
    assert!(records_store::attach(&moved, false)
        .unwrap()
        .refusal
        .is_some());
    records_store::adopt(&moved).unwrap();
    let attachment = records_store::attach(&moved, false).unwrap();
    assert_eq!(attachment.project.as_deref(), Some(original.as_str()));
    let dir = attachment.dir.unwrap();
    assert_eq!(std::fs::read(dir.join("project.json")).unwrap(), before);
    assert!(state(&dir).unwrap().closed);
    assert!(state(&dir).unwrap().hold);
    assert!(!storage::read_all(&moved).0.is_empty());
    assert!(records_store::write_dir(&moved).is_err());
    let plan = prepare(&moved, "reopen", None, &f.actor, &f.observed).unwrap();
    apply(plan, &f.actor, &f.observed).unwrap();
    assert!(!state(&dir).unwrap().closed);
    assert!(state(&dir).unwrap().hold);
    assert!(records_store::write_dir(&moved).is_ok());
}
#[test]
fn records_retention_rechecks_source_and_original_bag_after_durable_disposal_act() {
    for mode in ["new file", "both source and bag changed"] {
        let f = Fixture::new();
        f.act("close", None).unwrap();
        let bag = f.export("bag");
        let dir = f.dir();
        let source = dir.clone();
        let package = bag.clone();
        AFTER_DISPOSAL_ACT.with(|h| {
            *h.borrow_mut() = Some(Box::new(move || {
                if mode == "new file" {
                    std::fs::write(
                        source.join("unexported.json"),
                        b"unexported after native act",
                    )
                    .unwrap();
                } else {
                    let member = crate::records_export::payload_paths_for_test(&source)
                        .into_iter()
                        .find(|p| p.extension().is_some_and(|e| e == "jsonl"))
                        .unwrap();
                    let mut entry: Value =
                        serde_json::from_slice(&std::fs::read(&member).unwrap()).unwrap();
                    entry["body"]["subjectRef"] = json!("changed after native act");
                    let bytes = format!("{entry}\n");
                    std::fs::write(&member, &bytes).unwrap();
                    std::fs::write(
                        package
                            .join("data")
                            .join(member.strip_prefix(&source).unwrap()),
                        &bytes,
                    )
                    .unwrap();
                    crate::records_export::reprofile_for_test(&package);
                }
            }))
        });
        assert!(f.act("dispose", Some(&bag)).is_err());
        assert!(dir.exists());
        assert!(state(&dir).unwrap().disposition.is_some());
        assert!(!state(&dir).unwrap().completed);
        if mode == "new file" {
            assert_eq!(
                std::fs::read(dir.join("unexported.json")).unwrap(),
                b"unexported after native act"
            );
        }
    }
}
#[test]
fn records_retention_checked_member_deletion_preserves_late_files_and_changed_staged_bytes() {
    for mode in ["late source file", "changed staged bytes"] {
        let f = Fixture::new();
        f.act("close", None).unwrap();
        let bag = f.export("bag");
        let dir = f.dir();
        let source = dir.clone();
        let stage = control(&dir).unwrap().join("removal");
        let staging = stage.clone();
        crate::records_export::AFTER_MEMBER_STAGE.with(|h| {
            *h.borrow_mut() = Some(Box::new(move || {
                if mode == "late source file" {
                    std::fs::write(source.join("late.json"), b"never exported").unwrap();
                } else {
                    let member = crate::records_export::payload_paths_for_test(&staging)
                        .into_iter()
                        .next()
                        .unwrap();
                    std::fs::write(member, b"changed after staging").unwrap();
                }
            }))
        });
        assert!(f.act("dispose", Some(&bag)).is_err());
        assert!(!state(&dir).unwrap().completed);
        if mode == "late source file" {
            assert_eq!(
                std::fs::read(dir.join("late.json")).unwrap(),
                b"never exported"
            );
        } else {
            assert!(crate::records_export::payload_paths_for_test(&stage)
                .iter()
                .any(|p| std::fs::read(p).unwrap() == b"changed after staging"));
        }
        assert!(f.act("resume-disposal", None).is_err());
    }
}
#[test]
fn records_retention_admin_reader_refuses_fifo_or_symlink_replacement_without_following_or_waiting()
{
    use std::time::{Duration, Instant};
    let f = Fixture::new();
    f.act("close", None).unwrap();
    let dir = f.dir();
    let path = control(&dir)
        .unwrap()
        .join("events/00000000000000000001.json");
    let bytes = std::fs::read(&path).unwrap();
    for mode in ["fifo", "symlink"] {
        let outside = f.output.join("outside.json");
        std::fs::write(&outside, &bytes).unwrap();
        AFTER_ADMIN_METADATA.with(|h| {
            *h.borrow_mut() = Some(Box::new(move |path| {
                std::fs::remove_file(path).unwrap();
                if mode == "fifo" {
                    use std::os::unix::ffi::OsStrExt;
                    let name = std::ffi::CString::new(path.as_os_str().as_bytes()).unwrap();
                    assert_eq!(unsafe { libc::mkfifo(name.as_ptr(), 0o600) }, 0);
                } else {
                    std::os::unix::fs::symlink(&outside, path).unwrap();
                }
            }))
        });
        let at = Instant::now();
        assert!(state(&dir).is_err());
        assert!(at.elapsed() < Duration::from_secs(2));
        std::fs::remove_file(&path).unwrap();
        std::fs::write(&path, &bytes).unwrap();
    }
}
#[test]
fn records_retention_linked_or_known_project_cannot_bypass_retention_when_store_configuration_is_refused(
) {
    let f = Fixture::new();
    f.act("close", None).unwrap();
    let dir = f.dir();
    records_store::use_store_for_test(Some(Err("invented refused configuration".into())));
    let queued = dir.join("captures/queued-after-configuration-refusal.json");
    assert!(storage::create_json(&queued, &json!({"queued":"before refusal"})).is_err());
    assert!(!queued.exists());
    assert!(activity(&f.project).is_err());
    std::fs::remove_file(f.project.join(records_store::PROJECT_LINK)).unwrap();
    assert!(activity(&f.project).is_err());
    assert!(dir.exists());
    let fresh = f.output.join("fresh-unlinked");
    std::fs::create_dir(&fresh).unwrap();
    assert!(activity(&fresh).unwrap().is_none());
    assert!(!fresh.join(records_store::PROJECT_LINK).exists());
}
#[test]
fn records_retention_legal_hold_blocks_remaining_disposal_and_release_keeps_original_bag_cutoff() {
    let f = Fixture::new();
    f.act("close", None).unwrap();
    let bag = f.export("bag");
    let dir = f.dir();
    fail_remove_for_test(true);
    assert!(f.act("dispose", Some(&bag)).is_err());
    fail_remove_for_test(false);
    let before = crate::records_export::payload_paths_for_test(&dir)
        .into_iter()
        .map(|p| (p.clone(), std::fs::read(p).unwrap()))
        .collect::<Vec<_>>();
    let original = state(&dir).unwrap().disposition.unwrap();
    f.act("set-hold", None).unwrap();
    assert!(state(&dir).unwrap().hold);
    assert!(f
        .act("resume-disposal", None)
        .unwrap_err()
        .contains("legal hold"));
    for (p, bytes) in before {
        assert_eq!(std::fs::read(p).unwrap(), bytes);
    }
    f.act("release-hold", None).unwrap();
    assert_eq!(f.act("resume-disposal", None).unwrap()["state"], "disposed");
    assert_eq!(
        state(&dir).unwrap().disposition.unwrap(),
        original,
        "hold/release changes no original disposal actor, export, payload or history cutoff"
    );
}

#[test]
fn records_retention_remembered_hold_and_disposal_heads_refuse_tail_or_whole_history_removal() {
    let f = Fixture::new();
    f.act("close", None).unwrap();
    f.act("set-hold", None).unwrap();
    let dir = f.dir();
    let events = control(&dir).unwrap().join("events");
    let hold = events.join("00000000000000000002.json");
    let hold_bytes = std::fs::read(&hold).unwrap();
    std::fs::remove_file(&hold).unwrap();
    assert!(state(&dir).unwrap_err().contains("links removed"));
    assert!(storage::sources(&f.project).is_err());
    assert!(records_store::write_dir(&f.project).is_err());
    assert!(f.act("dispose", None).is_err());
    std::fs::write(&hold, &hold_bytes).unwrap();
    assert!(state(&dir).unwrap().hold);
    f.act("release-hold", None).unwrap();
    let bag = f.export("bag");
    fail_remove_for_test(true);
    assert!(f.act("dispose", Some(&bag)).is_err());
    fail_remove_for_test(false);
    let dispose = events.join("00000000000000000004.json");
    let dispose_bytes = std::fs::read(&dispose).unwrap();
    std::fs::remove_file(&dispose).unwrap();
    assert!(state(&dir).unwrap_err().contains("links removed"));
    assert!(storage::sources(&f.project).is_err());
    assert!(records_store::write_dir(&f.project).is_err());
    assert!(activity(&f.project).is_err());
    std::fs::write(&dispose, &dispose_bytes).unwrap();
    let saved = events.with_extension("saved");
    std::fs::rename(&events, &saved).unwrap();
    assert!(state(&dir).is_err());
    assert!(records_store::write_dir(&f.project).is_err());
    // Simulate a cold App process: the surviving marker refuses an absent
    // whole history, rather than inferring that no hold/disposal ever happened.
    ACCEPTED_HEADS.lock().unwrap().remove(&dir);
    assert!(state(&dir).unwrap_err().contains("events are absent"));
    std::fs::create_dir(&events).unwrap();
    assert!(state(&dir).unwrap_err().contains("events are absent"));
    std::fs::remove_dir(&events).unwrap();
    std::fs::rename(&saved, &events).unwrap();
    assert!(state(&dir).unwrap().disposition.is_some());
}

#[test]
fn records_retention_uncertain_native_publication_is_remembered_even_before_a_later_read() {
    let f = Fixture::new();
    // Establish events/ first so this injection fails publication sync after
    // the hold bytes are visible, rather than directory creation before them.
    f.act("close", None).unwrap();
    let dir = f.dir();
    FAIL_ADMIN_PUBLICATION.with(|flag| flag.set(true));
    assert!(f.act("set-hold", None).is_err());
    FAIL_ADMIN_PUBLICATION.with(|flag| flag.set(false));
    storage::fail_directory_for_test(None);
    std::fs::remove_file(
        control(&dir)
            .unwrap()
            .join("events/00000000000000000002.json"),
    )
    .unwrap();
    assert!(state(&dir).is_err());
    assert!(records_store::write_dir(&f.project).is_err());
    assert!(activity(&f.project).is_err());
}

#[test]
fn records_retention_identity_reads_refuse_special_files_at_attach_and_after_metadata() {
    use std::time::{Duration, Instant};
    let f = Fixture::new();
    let paths = [
        f.store.join("store.json"),
        f.project.join(records_store::PROJECT_LINK),
    ];
    for path in paths {
        let bytes = std::fs::read(&path).unwrap();
        for mode in ["fifo", "symlink"] {
            let outside = f.output.join("outside-identity.json");
            std::fs::write(&outside, &bytes).unwrap();
            let replace = move |path: &Path| {
                std::fs::remove_file(path).unwrap();
                if mode == "fifo" {
                    use std::os::unix::ffi::OsStrExt;
                    let name = std::ffi::CString::new(path.as_os_str().as_bytes()).unwrap();
                    assert_eq!(unsafe { libc::mkfifo(name.as_ptr(), 0o600) }, 0);
                } else {
                    std::os::unix::fs::symlink(outside, path).unwrap();
                }
            };
            AFTER_ADMIN_METADATA.with(|h| *h.borrow_mut() = Some(Box::new(replace)));
            let at = Instant::now();
            assert!(read_plain(&path).is_err());
            assert!(at.elapsed() < Duration::from_secs(2));
            let at = Instant::now();
            let attached = records_store::attach(&f.project, false);
            assert!(attached.as_ref().map_or(true, |a| a.refusal.is_some()));
            assert!(at.elapsed() < Duration::from_secs(2));
            assert!(prepare(&f.project, "close", None, &f.actor, &f.observed).is_err());
            std::fs::remove_file(&path).unwrap();
            std::fs::write(&path, &bytes).unwrap();
        }
    }
}

#[test]
fn records_retention_export_defaults_are_owner_only_under_a_permissive_umask() {
    use std::os::unix::fs::PermissionsExt;
    struct Umask(libc::mode_t);
    impl Drop for Umask {
        fn drop(&mut self) {
            unsafe { libc::umask(self.0) };
        }
    }
    let f = Fixture::new();
    let _mask = Umask(unsafe { libc::umask(0o022) });
    let bag = f.export("private-bag");
    fn modes(path: &Path) {
        let metadata = std::fs::symlink_metadata(path).unwrap();
        assert_eq!(
            metadata.permissions().mode() & 0o777,
            if metadata.is_dir() { 0o700 } else { 0o600 },
            "{}",
            path.display()
        );
        if metadata.is_dir() {
            for entry in std::fs::read_dir(path).unwrap() {
                modes(&entry.unwrap().path());
            }
        }
    }
    modes(&bag);
    crate::records_export::verify(&bag).unwrap();
    modes(&bag); // Imported/existing-package verification changes no modes.
}
/// DEL-04-03 AC-008 / REQ-007: a capture destination and a read-log path
/// resolved while the project was attached are not written once its link
/// names another identity, names another store or is missing: nothing appears
/// under the old subtree until the person restores the link.
#[test]
fn records_retention_a_write_resolved_before_the_link_changed_is_refused_until_the_link_is_restored() {
    fn listing(dir: &Path) -> Vec<(PathBuf, u64)> {
        let mut out = Vec::new();
        let mut stack = vec![dir.to_path_buf()];
        while let Some(at) = stack.pop() {
            for entry in std::fs::read_dir(&at).unwrap() {
                let entry = entry.unwrap();
                let meta = std::fs::symlink_metadata(entry.path()).unwrap();
                if meta.is_dir() {
                    stack.push(entry.path());
                }
                out.push((entry.path(), if meta.is_dir() { 0 } else { meta.len() }));
            }
        }
        out.sort();
        out
    }
    fn refusal(result: Result<(), storage::CapturePublicationFailure>) -> String {
        match result {
            Ok(()) => panic!("the capture was published"),
            Err(storage::CapturePublicationFailure::DefinitelyNotPublished(e)) => e,
            Err(storage::CapturePublicationFailure::PublicationUncertain(e)) => panic!("publication attempted: {e}"),
        }
    }
    const STALE: &str = "project root association changed; stale queued write refused";
    let f = Fixture::new();
    let project = f.project.clone();
    let dir = records_store::attach(&project, false).unwrap().dir.unwrap();
    // Resolved while attached.
    let captures = storage::write_capture_dir(&project).unwrap();
    let capture = captures.join(format!("{}.json", storage::key("cap:link-fixture")));
    let pending = captures.join("pending").join(format!("{}.json", storage::key("cap:link-fixture")));
    let read_log = records_store::read_log_path(&project).unwrap();
    storage::ensure_directory(read_log.parent().unwrap()).unwrap();
    let capability = crate::records_access::RecordsCapability::at(&project, read_log.clone()).unwrap();
    let call = |n: u64| crate::records_access::Call {
        app_session: "app-session:fixture".into(), generation: "g:fixture".into(), request: json!(n),
        thread: "thread".into(), turn: "turn".into(), call: format!("call-{n}"), arguments: json!({"operation":"list_runs"}),
    };
    let cwd = project.to_str().unwrap().to_owned();
    assert_eq!(capability.answer(&call(1), Some(&cwd))["success"], true);
    let logged = std::fs::read(&read_log).unwrap();
    assert!(!logged.is_empty());
    let value = json!({"captureId":"cap:link-fixture","actKind":"A16","fixture":"invented"});
    let link_path = project.join(records_store::PROJECT_LINK);
    let link: Value = serde_json::from_slice(&std::fs::read(&link_path).unwrap()).unwrap();
    let mut changed = link.clone();
    changed["projectId"] = json!("chirality-project:forged-fixture");
    let mut other_store = link.clone();
    other_store["storeId"] = json!("records-store:another-fixture");
    let before = listing(&dir);
    for (n, (case, replacement, expected)) in [
        ("changed", Some(changed), "names project chirality-project:forged-fixture"),
        ("another store", Some(other_store), "names another records store (records-store:another-fixture)"),
        ("missing", None, "is missing"),
    ].into_iter().enumerate() {
        match &replacement {
            Some(v) => std::fs::write(&link_path, serde_json::to_vec(v).unwrap()).unwrap(),
            None => std::fs::remove_file(&link_path).unwrap(),
        }
        let e = refusal(storage::create_capture_json(&capture, &value));
        assert!(e.contains(STALE) && e.contains(expected), "{case}: {e}");
        let e = storage::create_json(&pending, &json!({"capture":value})).unwrap_err();
        assert!(e.contains(STALE) && e.contains(expected), "{case}: {e}");
        let answer = capability.answer(&call(10 + n as u64), Some(&cwd));
        assert_eq!(answer["success"], false, "{case}: {answer}");
        assert_eq!(std::fs::read(&read_log).unwrap(), logged, "{case}: the read is not recorded under the old subtree");
        assert_eq!(listing(&dir), before, "{case}: nothing appears under the old subtree");
        records_store::restore_link(&project).unwrap();
    }
    // Restored: the same resolved paths are written.
    storage::create_capture_json(&capture, &value).map_err(|_| "capture refused after restore").unwrap();
    storage::create_json(&pending, &json!({"capture":value})).unwrap();
    assert!(capture.is_file() && pending.is_file());
    assert_eq!(capability.answer(&call(20), Some(&cwd))["success"], true);
    assert!(std::fs::read(&read_log).unwrap().len() > logged.len());
}

#[test]
fn a_queued_write_is_refused_when_the_store_identity_attach_would_refuse() {
    // Review round 2, finding 5: the low-level write admission took storeId
    // from store.json without checking it is a records store identity or the
    // one this process opened. Attach refuses both; so must a queued write.
    const STALE: &str = "project root association changed; stale queued write refused";
    let f = Fixture::new();
    let project = f.project.clone();
    let captures = storage::write_capture_dir(&project).unwrap();
    let pending = captures.join("pending").join(format!("{}.json", storage::key("cap:store-identity-fixture")));
    let identity_path = f.store.join("store.json");
    let identity_bytes = std::fs::read(&identity_path).unwrap();
    let identity: Value = serde_json::from_slice(&identity_bytes).unwrap();
    let link_path = project.join(records_store::PROJECT_LINK);
    let link_bytes = std::fs::read(&link_path).unwrap();
    // The same id with a format that is not a records store identity.
    let mut wrong_format = identity.clone();
    wrong_format["format"] = json!("invented.not-a-records-store");
    std::fs::write(&identity_path, serde_json::to_vec(&wrong_format).unwrap()).unwrap();
    assert!(records_store::attach(&project, false).is_err(), "attach refuses this store identity");
    let e = storage::create_json(&pending, &json!({"fixture":"invented"})).unwrap_err();
    assert!(e.contains(STALE) && e.contains("not a records store identity"), "{e}");
    assert!(!pending.exists());
    // Another id, with the project link changed to name it.
    let mut replaced = identity.clone();
    replaced["storeId"] = json!("records-store:replaced-fixture");
    std::fs::write(&identity_path, serde_json::to_vec(&replaced).unwrap()).unwrap();
    let mut link: Value = serde_json::from_slice(&link_bytes).unwrap();
    link["storeId"] = json!("records-store:replaced-fixture");
    std::fs::write(&link_path, serde_json::to_vec(&link).unwrap()).unwrap();
    assert!(records_store::attach(&project, false).is_err(), "attach refuses a changed store identity");
    let e = storage::create_json(&pending, &json!({"fixture":"invented"})).unwrap_err();
    assert!(e.contains(STALE) && e.contains("identity changed"), "{e}");
    assert!(!pending.exists());
    // Put back, the same resolved path is written.
    std::fs::write(&identity_path, &identity_bytes).unwrap();
    std::fs::write(&link_path, &link_bytes).unwrap();
    storage::create_json(&pending, &json!({"fixture":"invented"})).unwrap();
    assert!(pending.is_file());
}

/// Every file beneath `root`, by its relative path, with its bytes.
fn files_with_bytes(root: &Path) -> std::collections::BTreeMap<String, Vec<u8>> {
    fn walk(root: &Path, at: &Path, out: &mut std::collections::BTreeMap<String, Vec<u8>>) {
        let Ok(rd) = std::fs::read_dir(at) else { return };
        for entry in rd {
            let path = entry.unwrap().path();
            if std::fs::symlink_metadata(&path).unwrap().is_dir() { walk(root, &path, out); }
            else { out.insert(path.strip_prefix(root).unwrap().to_string_lossy().into_owned(), std::fs::read(&path).unwrap()); }
        }
    }
    let mut out = std::collections::BTreeMap::new();
    walk(root, root, &mut out);
    out
}

/// Removal not established: a disposal that cannot examine what remains of
/// the payload (the projects folder made unsearchable after its first member
/// is staged) records no completion. The original act survives, every
/// remaining byte is kept (in the payload or the private removal stage),
/// and a reopened store still reports the disposal as incomplete, to be
/// finished once the payload can be examined. The other side, removal
/// established but completion's publication uncertain, is
/// records_retention_visible_but_uncertain_completion_has_a_resync_path_without_a_new_act.
#[test]
fn a_disposal_that_cannot_examine_what_remains_records_no_completion() {
    use std::os::unix::fs::PermissionsExt;
    let f = Fixture::new();
    f.act("close", None).unwrap();
    let bag = f.export("bag");
    let dir = f.dir();
    let stage = control(&dir).unwrap().join("removal");
    let before = files_with_bytes(&dir);
    assert!(!before.is_empty());
    let projects = dir.parent().unwrap().to_path_buf();
    let (blocked, seen) = (projects.clone(), std::rc::Rc::new(std::cell::Cell::new(None)));
    let observed = seen.clone();
    let probe = dir.clone();
    crate::records_export::AFTER_MEMBER_STAGE.with(|h| *h.borrow_mut() = Some(Box::new(move || {
        std::fs::set_permissions(&blocked, std::fs::Permissions::from_mode(0o400)).unwrap();
        observed.set(Some(std::fs::symlink_metadata(&probe).map(|_| ()).map_err(|e| e.kind())));
    })));
    let disposed = f.act("dispose", Some(&bag));
    std::fs::set_permissions(&projects, std::fs::Permissions::from_mode(0o700)).unwrap();
    assert_eq!(seen.get(), Some(Err(std::io::ErrorKind::PermissionDenied)), "a real permission failure, after the first member was staged");
    // The durable record, read again from disk.
    let s = state(&dir).unwrap();
    assert!(!s.completed, "no completion is recorded: {disposed:?}");
    assert!(s.disposition.is_some(), "the original disposal act survives");
    assert!(disposed.as_ref().is_err_and(|e| e.contains("disposal incomplete")), "{disposed:?}");
    // Every byte is kept, in the payload or the private removal stage, unless
    // the member was removed after its exact bytes were verified in the
    // export (an empty owning control lock apart): removal stopped, and what
    // it had not yet verified and removed is all still there.
    let mut kept = files_with_bytes(&dir);
    kept.extend(files_with_bytes(&stage));
    let exported = files_with_bytes(&bag.join("data"));
    let mut removed = 0;
    for (rel, bytes) in &before {
        if kept.get(rel) == Some(bytes) { continue; }
        assert!(!kept.contains_key(rel), "kept bytes are unchanged: {rel}");
        let control = rel == ".writer.lock" || rel == "captures/.capture.lock";
        assert!(exported.get(rel) == Some(bytes) || (control && bytes.is_empty()), "removed only after its bytes were verified in the export: {rel}");
        removed += 1;
    }
    assert!(removed < before.len() && !files_with_bytes(&dir).is_empty(), "the remaining payload is still there: {removed} of {} removed", before.len());
    // Reopened: the store configured afresh, as at the App's next start.
    records_store::use_store_for_test(Some(Ok(Store { root: f.store.clone(), placement: Placement::Test, limits: vec![] })));
    assert_eq!(view(&dir)["disposition"], "disposal incomplete");
    // Once the payload can be examined, the original act is finished.
    assert_eq!(f.act("resume-disposal", None).unwrap()["state"], "disposed");
    assert!(!dir.exists());
}

/// A project link that cannot be examined is not an unlinked project. With
/// the records store unavailable, the start of a supplier for that project
/// (an invented peer here, never the supplier's Codex) is refused, never
/// admitted without the activity lease that keeps an open project from
/// disposal.
#[test]
fn a_start_for_a_project_whose_link_cannot_be_examined_is_refused() {
    use std::os::unix::fs::PermissionsExt;
    struct Restore;
    impl Drop for Restore { fn drop(&mut self) { records_store::use_store_for_test(None); } }
    let _restore = Restore;
    records_store::use_store_not_started_for_test(Some(Err("invented unavailable store".into())));
    let output = std::env::temp_dir().join(util::opaque_id("activity-output-").unwrap());
    let project = std::env::temp_dir().join(util::opaque_id("activity-project-").unwrap());
    let folder = project.join(".chirality");
    std::fs::create_dir_all(&folder).unwrap();
    std::fs::write(folder.join(records_store::PROJECT_LINK.rsplit('/').next().unwrap()),
        br#"{"format":"chirality.project-link","projectId":"invented project","storeId":"invented store"}"#).unwrap();
    for home in ["home", "probe"] { std::fs::create_dir_all(output.join(home)).unwrap(); }
    let peer = output.join("peer.py");
    std::fs::write(&peer, r#"#!/usr/bin/python3
import json,sys
if '--version' in sys.argv:
 print('codex-cli 0.167.0');sys.exit(0)
for line in sys.stdin:
 frame=json.loads(line)
 if frame.get('method')=='initialize':
  print(json.dumps({'id':frame['id'],'result':{'userAgent':'invented activity fixture'}}),flush=True)
"#).unwrap();
    std::fs::set_permissions(&peer, std::fs::Permissions::from_mode(0o700)).unwrap();
    let mut cfg = crate::hosting::HostConfig::new(peer, output.join("home"), output.join("probe"), project.clone());
    cfg.allow_unverified_dev = true;
    cfg.wait_limit = std::time::Duration::from_secs(2);
    assert!(cfg.records_project);
    let host = std::sync::Arc::new(crate::hosting::Host::new());
    // Control: a readable link refuses the start while the store is unavailable.
    assert!(host.start(&cfg, "invented fixture person").is_err_and(|e| e.contains("no Codex start")));
    std::fs::set_permissions(&folder, std::fs::Permissions::from_mode(0o000)).unwrap();
    let denied = std::fs::symlink_metadata(folder.join("project.json")).map(|_| ()).map_err(|e| e.kind());
    let started = host.start(&cfg, "invented fixture person");
    std::fs::set_permissions(&folder, std::fs::Permissions::from_mode(0o700)).unwrap();
    if started.is_ok() { let _ = host.stop("invented fixture person", "fixture end"); }
    assert_eq!(denied, Err(std::io::ErrorKind::PermissionDenied), "a real permission failure");
    assert!(started.as_ref().is_err_and(|e| e.contains("no Codex start")), "{started:?}");
    let _ = (std::fs::remove_dir_all(&project), std::fs::remove_dir_all(&output));
}

/// The folder comparison stage. After the disposal act is published and
/// before anything is removed, apply compares the payload folder with the
/// one the act names. A payload folder that cannot be examined then (the
/// projects folder made unsearchable at that point) is not taken as gone:
/// nothing is removed and no completion is recorded.
#[test]
fn a_disposal_whose_payload_folder_cannot_be_examined_at_removal_removes_and_records_nothing() {
    use std::os::unix::fs::PermissionsExt;
    let f = Fixture::new();
    f.act("close", None).unwrap();
    let bag = f.export("bag");
    let dir = f.dir();
    let before = files_with_bytes(&dir);
    let projects = dir.parent().unwrap().to_path_buf();
    let blocked = projects.clone();
    AFTER_DISPOSAL_ACT.with(|h| *h.borrow_mut() = Some(Box::new(move || {
        std::fs::set_permissions(&blocked, std::fs::Permissions::from_mode(0o400)).unwrap();
    })));
    let probe = dir.clone();
    let disposed = f.act("dispose", Some(&bag));
    let denied = std::fs::symlink_metadata(&probe).map(|_| ()).map_err(|e| e.kind());
    std::fs::set_permissions(&projects, std::fs::Permissions::from_mode(0o700)).unwrap();
    assert_eq!(denied, Err(std::io::ErrorKind::PermissionDenied), "a real permission failure");
    let s = state(&dir).unwrap();
    assert!(!s.completed, "no completion is recorded: {disposed:?}");
    assert!(s.disposition.is_some(), "the original disposal act survives");
    assert_eq!(files_with_bytes(&dir), before, "nothing was removed");
    // The state could not be read again for the report, and no completion
    // was attempted, so the report knows there is none: "disposal
    // incomplete", never "not known".
    assert!(disposed.as_ref().is_err_and(|e| e.contains("disposal incomplete") && e.contains("could not be read again") && !e.contains("whether its completion was recorded is not known")), "{disposed:?}");
    assert_eq!(view(&dir)["disposition"], "disposal incomplete");
    assert_eq!(f.act("resume-disposal", None).unwrap()["state"], "disposed");
}

/// The completion's choice of path. Finish disposal after a completion whose
/// publication was uncertain reconciles only when the payload is gone; a
/// payload folder that has reappeared and cannot be examined is never
/// reported as disposed.
#[test]
fn finishing_a_completed_disposal_never_reports_disposed_over_a_payload_it_cannot_examine() {
    use std::os::unix::fs::PermissionsExt;
    let f = Fixture::new();
    f.act("close", None).unwrap();
    let bag = f.export("bag");
    let dir = f.dir();
    FAIL_COMPLETION_PUBLICATION.with(|flag| flag.set(true));
    let uncertain = f.act("dispose", Some(&bag)).unwrap_err();
    FAIL_COMPLETION_PUBLICATION.with(|flag| flag.set(false));
    storage::fail_directory_for_test(None);
    assert!(uncertain.contains("completion publication durability uncertain"), "{uncertain}");
    assert!(!dir.exists());
    // The subtree reappears, and then cannot be examined.
    std::fs::create_dir_all(&dir).unwrap();
    std::fs::write(dir.join("reappeared.json"), b"invented reappeared bytes").unwrap();
    let projects = dir.parent().unwrap().to_path_buf();
    std::fs::set_permissions(&projects, std::fs::Permissions::from_mode(0o400)).unwrap();
    let denied = std::fs::symlink_metadata(&dir).map(|_| ()).map_err(|e| e.kind());
    let finished = f.act("resume-disposal", None);
    std::fs::set_permissions(&projects, std::fs::Permissions::from_mode(0o700)).unwrap();
    assert_eq!(denied, Err(std::io::ErrorKind::PermissionDenied), "a real permission failure");
    assert!(finished.as_ref().map_or(true, |v| v["state"] != "disposed"), "never reported disposed: {finished:?}");
    assert!(finished.is_err(), "{finished:?}");
    assert_eq!(std::fs::read(dir.join("reappeared.json")).unwrap(), b"invented reappeared bytes", "nothing removed");
}

/// The removal's inventory. When the private removal stage cannot be
/// examined after the last member is staged, nothing staged is passed over:
/// no completion is recorded and the staged bytes are kept. (This one holds
/// on main too: the completion's own record lives in the same administration
/// folder as the stage, so a stage that cannot be examined there leaves the
/// completion unwritable as well. It guards the stage's checks themselves.)
#[test]
fn a_disposal_whose_removal_stage_cannot_be_examined_records_no_completion() {
    use std::os::unix::fs::PermissionsExt;
    fn block_after(n: usize, folder: PathBuf) {
        crate::records_export::AFTER_MEMBER_STAGE.with(|h| *h.borrow_mut() = Some(Box::new(move || {
            if n <= 1 { std::fs::set_permissions(&folder, std::fs::Permissions::from_mode(0o400)).unwrap(); }
            else { block_after(n - 1, folder); }
        })));
    }
    let f = Fixture::new();
    f.act("close", None).unwrap();
    let bag = f.export("bag");
    let dir = f.dir();
    let stage = control(&dir).unwrap().join("removal");
    let administration = control(&dir).unwrap();
    let before = files_with_bytes(&dir);
    block_after(before.len(), administration.clone());
    let disposed = f.act("dispose", Some(&bag));
    let denied = std::fs::symlink_metadata(&stage).map(|_| ()).map_err(|e| e.kind());
    std::fs::set_permissions(&administration, std::fs::Permissions::from_mode(0o700)).unwrap();
    crate::records_export::AFTER_MEMBER_STAGE.with(|h| *h.borrow_mut() = None);
    assert_eq!(denied, Err(std::io::ErrorKind::PermissionDenied), "a real permission failure");
    let s = state(&dir).unwrap();
    assert!(!s.completed, "no completion is recorded: {disposed:?}");
    let mut kept = files_with_bytes(&dir);
    kept.extend(files_with_bytes(&stage));
    let exported = files_with_bytes(&bag.join("data"));
    for (rel, bytes) in &before {
        let control = rel == ".writer.lock" || rel == "captures/.capture.lock";
        assert!(kept.get(rel) == Some(bytes) || exported.get(rel) == Some(bytes) || (control && bytes.is_empty()), "kept, or removed only after its bytes were verified in the export: {rel}");
    }
    assert!(disposed.is_err(), "{disposed:?}");
}

/// Removal established: a true completion is reported as one. The state is
/// made unreadable at the moment the completion's own event is read back
/// (the payload's parent made unsearchable then), so the act's report cannot
/// re-read the state. A published, durable completion still reads
/// "disposed"; a published completion whose sync failed is reported as not
/// known, never "incomplete", and keeps Finish disposal's resync path.
#[test]
fn a_true_completion_is_reported_as_one_when_the_state_cannot_be_read_again() {
    use std::os::unix::fs::PermissionsExt;
    fn on_completion_read(projects: PathBuf) {
        AFTER_ADMIN_METADATA.with(|h| *h.borrow_mut() = Some(Box::new(move |path: &Path| {
            if path.file_name().and_then(|n| n.to_str()) == Some("00000000000000000003.json") {
                std::fs::set_permissions(&projects, std::fs::Permissions::from_mode(0o400)).unwrap();
            } else {
                on_completion_read(projects);
            }
        })));
    }
    for uncertain in [false, true] {
        let f = Fixture::new();
        f.act("close", None).unwrap();
        let bag = f.export("bag");
        let dir = f.dir();
        let projects = dir.parent().unwrap().to_path_buf();
        FAIL_COMPLETION_PUBLICATION.with(|flag| flag.set(uncertain));
        on_completion_read(projects.clone());
        let reply = f.act("dispose", Some(&bag));
        let denied = std::fs::symlink_metadata(&dir).map(|_| ()).map_err(|e| e.kind());
        std::fs::set_permissions(&projects, std::fs::Permissions::from_mode(0o700)).unwrap();
        AFTER_ADMIN_METADATA.with(|h| *h.borrow_mut() = None);
        FAIL_COMPLETION_PUBLICATION.with(|flag| flag.set(false));
        storage::fail_directory_for_test(None);
        assert_eq!(denied, Err(std::io::ErrorKind::PermissionDenied), "uncertain {uncertain}: a real permission failure");
        let actual = state(&dir).unwrap();
        assert!(actual.completed && !dir.exists(), "uncertain {uncertain}: the completion is true");
        if uncertain {
            let e = reply.unwrap_err();
            assert!(!e.contains("disposal incomplete") && e.contains("not known"), "never reported incomplete: {e}");
            assert_eq!(view(&dir)["disposition"], "completion durability uncertain");
            assert_eq!(f.act("resume-disposal", None).unwrap()["state"], "disposed", "the resync path is kept");
        } else {
            let reply = reply.unwrap();
            assert_eq!(reply["state"], "disposed", "{reply}");
            assert_eq!(reply["administration"]["disposition"], "unavailable", "{reply}");
            assert_eq!(view(&dir)["disposition"], "disposed");
        }
    }
}

/// Finish disposal never offers a verification of a remaining payload it
/// could not examine. After an incomplete disposal, the payload is made
/// unexaminable while export verification reads the administrative history
/// (the payload's parent made unsearchable then): the offer is refused,
/// never a verified empty remainder.
#[test]
fn finishing_a_disposal_never_offers_a_verification_of_a_payload_it_could_not_examine() {
    use std::os::unix::fs::PermissionsExt;
    use std::cell::Cell;
    use std::rc::Rc;
    fn count_reads(name: &'static str, n: Rc<Cell<usize>>) {
        AFTER_ADMIN_METADATA.with(|h| *h.borrow_mut() = Some(Box::new(move |path: &Path| {
            if path.file_name().and_then(|f| f.to_str()) == Some(name) { n.set(n.get() + 1); }
            count_reads(name, n);
        })));
    }
    fn block_at(name: &'static str, left: usize, blocked: PathBuf) {
        AFTER_ADMIN_METADATA.with(|h| *h.borrow_mut() = Some(Box::new(move |path: &Path| {
            let named = path.file_name().and_then(|f| f.to_str()) == Some(name);
            if named && left == 1 { std::fs::set_permissions(&blocked, std::fs::Permissions::from_mode(0o400)).unwrap(); }
            else { block_at(name, if named { left - 1 } else { left }, blocked); }
        })));
    }
    let f = Fixture::new();
    f.act("close", None).unwrap();
    let bag = f.export("bag");
    let dir = f.dir();
    fail_remove_for_test(true);
    assert!(f.act("dispose", Some(&bag)).is_err());
    fail_remove_for_test(false);
    let before = files_with_bytes(&dir);
    assert!(!before.is_empty());
    // The last read of the disposal act's event during a readable offer.
    let reads = Rc::new(Cell::new(0));
    count_reads("00000000000000000002.json", reads.clone());
    let readable = prepare(&f.project, "resume-disposal", None, &f.actor, &f.observed);
    AFTER_ADMIN_METADATA.with(|h| *h.borrow_mut() = None);
    assert!(readable.is_ok(), "control: {:?}", readable.err());
    let projects = dir.parent().unwrap().to_path_buf();
    block_at("00000000000000000002.json", reads.get(), projects.clone());
    let offered = prepare(&f.project, "resume-disposal", None, &f.actor, &f.observed);
    let denied = std::fs::symlink_metadata(&dir).map(|_| ()).map_err(|e| e.kind());
    std::fs::set_permissions(&projects, std::fs::Permissions::from_mode(0o700)).unwrap();
    AFTER_ADMIN_METADATA.with(|h| *h.borrow_mut() = None);
    assert_eq!(denied, Err(std::io::ErrorKind::PermissionDenied), "a real permission failure");
    let offered = offered.map(|p| p.context["export"].clone());
    assert!(offered.is_err(), "never a verified remainder of a payload not examined: {offered:?}");
    assert_eq!(files_with_bytes(&dir), before, "nothing removed");
    assert_eq!(f.act("resume-disposal", None).unwrap()["state"], "disposed");
}

/// The completion's choice of path, reached (a construction the second
/// reading found). Finish disposal after a completion whose publication was
/// uncertain reconciles only over a payload known to be gone: when the
/// payload's parent becomes unsearchable at the last read of the completion
/// before that check, the check is reached and refuses, and the resync path
/// is kept. (Were the payload to reappear instead, apply's recheck of the
/// prepared context refuses before this check.)
#[test]
fn reconciling_a_completed_disposal_refuses_when_the_payload_cannot_be_examined() {
    use std::os::unix::fs::PermissionsExt;
    use std::cell::Cell;
    use std::rc::Rc;
    const COMPLETION: &str = "00000000000000000003.json";
    fn count_reads(n: Rc<Cell<usize>>) {
        AFTER_ADMIN_METADATA.with(|h| *h.borrow_mut() = Some(Box::new(move |path: &Path| {
            if path.file_name().and_then(|f| f.to_str()) == Some(COMPLETION) { n.set(n.get() + 1); }
            count_reads(n);
        })));
    }
    fn block_at(left: usize, blocked: PathBuf) {
        AFTER_ADMIN_METADATA.with(|h| *h.borrow_mut() = Some(Box::new(move |path: &Path| {
            let named = path.file_name().and_then(|f| f.to_str()) == Some(COMPLETION);
            if named && left == 1 { std::fs::set_permissions(&blocked, std::fs::Permissions::from_mode(0o400)).unwrap(); }
            else { block_at(if named { left - 1 } else { left }, blocked); }
        })));
    }
    let uncertain = || {
        let f = Fixture::new();
        f.act("close", None).unwrap();
        let bag = f.export("bag");
        let dir = f.dir();
        FAIL_COMPLETION_PUBLICATION.with(|flag| flag.set(true));
        assert!(f.act("dispose", Some(&bag)).unwrap_err().contains("completion publication durability uncertain"));
        FAIL_COMPLETION_PUBLICATION.with(|flag| flag.set(false));
        storage::fail_directory_for_test(None);
        let plan = prepare(&f.project, "resume-disposal", None, &f.actor, &f.observed).unwrap();
        (f, dir, plan)
    };
    // Control: how many times a readable reconciliation reads the completion.
    let total = {
        let (f, _dir, plan) = uncertain();
        let reads = Rc::new(Cell::new(0));
        count_reads(reads.clone());
        let result = apply(plan, &f.actor, &f.observed);
        AFTER_ADMIN_METADATA.with(|h| *h.borrow_mut() = None);
        assert!(result.is_ok(), "readable reconciliation: {result:?}");
        reads.get()
    };
    assert!(total >= 2, "the last state read, then the reply's");
    let (f, dir, plan) = uncertain();
    let projects = dir.parent().unwrap().to_path_buf();
    block_at(total - 1, projects.clone());
    let result = apply(plan, &f.actor, &f.observed);
    let denied = std::fs::symlink_metadata(&dir).map(|_| ()).map_err(|e| e.kind());
    std::fs::set_permissions(&projects, std::fs::Permissions::from_mode(0o700)).unwrap();
    AFTER_ADMIN_METADATA.with(|h| *h.borrow_mut() = None);
    assert_eq!(denied, Err(std::io::ErrorKind::PermissionDenied), "a real permission failure");
    assert!(result.as_ref().is_err_and(|e| e.contains("could not be examined")), "the check is reached and refuses: {result:?}");
    assert_eq!(view(&dir)["disposition"], "completion durability uncertain", "the resync path is kept");
    assert_eq!(f.act("resume-disposal", None).unwrap()["state"], "disposed");
}

/// Finish disposal never says a completion's evidence was synced over
/// history it could not examine, and never clears the uncertainty then.
/// After a completion whose publication sync failed, the administration
/// folder is made unsearchable while Finish disposal syncs the history, and
/// readable again before it reads the state: the sync is refused, the
/// marker kept, and a later Finish disposal syncs and reconciles.
#[test]
fn finishing_a_disposal_never_claims_a_sync_over_history_it_could_not_examine() {
    use std::os::unix::fs::PermissionsExt;
    let f = Fixture::new();
    f.act("close", None).unwrap();
    let bag = f.export("bag");
    let dir = f.dir();
    FAIL_COMPLETION_PUBLICATION.with(|flag| flag.set(true));
    assert!(f.act("dispose", Some(&bag)).unwrap_err().contains("completion publication durability uncertain"));
    FAIL_COMPLETION_PUBLICATION.with(|flag| flag.set(false));
    storage::fail_directory_for_test(None);
    assert_eq!(view(&dir)["disposition"], "completion durability uncertain");
    let administration = control(&dir).unwrap();
    let (block, restore) = (administration.clone(), administration.clone());
    let denied = std::rc::Rc::new(std::cell::Cell::new(None));
    let seen = denied.clone();
    let marker = history_marker(&dir).unwrap();
    AROUND_APPLY_HISTORY.with(|h| *h.borrow_mut() = Some((
        Box::new(move || {
            std::fs::set_permissions(&block, std::fs::Permissions::from_mode(0o400)).unwrap();
            seen.set(Some(std::fs::symlink_metadata(&marker).map(|_| ()).map_err(|e| e.kind())));
        }),
        Box::new(move || std::fs::set_permissions(&restore, std::fs::Permissions::from_mode(0o700)).unwrap()),
    )));
    let finished = f.act("resume-disposal", None);
    std::fs::set_permissions(&administration, std::fs::Permissions::from_mode(0o700)).unwrap();
    AROUND_APPLY_HISTORY.with(|h| *h.borrow_mut() = None);
    assert_eq!(denied.get(), Some(Err(std::io::ErrorKind::PermissionDenied)), "a real permission failure while the history was synced");
    assert!(finished.as_ref().map_or(true, |v| v["completion"] != "existing completion evidence synced; no new disposal act"), "no sync claimed: {finished:?}");
    assert!(finished.is_err(), "{finished:?}");
    assert_eq!(view(&dir)["disposition"], "completion durability uncertain", "the marker is kept");
    let synced = f.act("resume-disposal", None).unwrap();
    assert_eq!(synced["completion"], "existing completion evidence synced; no new disposal act");
    assert_eq!(view(&dir)["disposition"], "disposed");
}

/// An uncertainty marker never outlives a later successful completion. An
/// attempt removes the payload and attempts its completion, which is not
/// published (the events folder made unsearchable after the last member is
/// staged), and the state cannot be read for the report: completion is not
/// known, and the marker set. Once readable, no completion is recorded, and
/// Finish disposal publishes one: the view is then "disposed", with no
/// further Finish disposal needed or admitted.
#[test]
fn a_retry_that_completes_a_disposal_clears_an_earlier_uncertainty() {
    use std::os::unix::fs::PermissionsExt;
    fn block_after(n: usize, folder: PathBuf) {
        crate::records_export::AFTER_MEMBER_STAGE.with(|h| *h.borrow_mut() = Some(Box::new(move || {
            if n <= 1 { std::fs::set_permissions(&folder, std::fs::Permissions::from_mode(0o400)).unwrap(); }
            else { block_after(n - 1, folder); }
        })));
    }
    let f = Fixture::new();
    f.act("close", None).unwrap();
    let bag = f.export("bag");
    let dir = f.dir();
    let events = control(&dir).unwrap().join("events");
    block_after(files_with_bytes(&dir).len(), events.clone());
    let attempt = f.act("dispose", Some(&bag));
    std::fs::set_permissions(&events, std::fs::Permissions::from_mode(0o700)).unwrap();
    crate::records_export::AFTER_MEMBER_STAGE.with(|h| *h.borrow_mut() = None);
    assert!(attempt.as_ref().is_err_and(|e| e.contains("is not known")), "{attempt:?}");
    let s = state(&dir).unwrap();
    assert!(!s.completed && s.disposition.is_some() && !dir.exists(), "removal done, no completion published");
    assert_eq!(view(&dir)["disposition"], "disposal incomplete");
    assert_eq!(f.act("resume-disposal", None).unwrap()["state"], "disposed");
    assert_eq!(view(&dir)["disposition"], "disposed", "no stale uncertainty");
    assert!(f.act("resume-disposal", None).is_err(), "no further Finish disposal is admitted");
}

/// Export's interior syncs never pass over a folder they could not examine.
/// After the staged export is verified, one of its interior folders is made
/// listable but not searchable, so its entries cannot be examined: the
/// export is refused and nothing is published, never reported "verified
/// export created" with folders left unsynced.
#[test]
fn an_export_never_publishes_over_folders_it_could_not_sync() {
    use std::os::unix::fs::PermissionsExt;
    let f = Fixture::new();
    let bag = f.output.join("bag");
    let blocked = std::rc::Rc::new(std::cell::RefCell::new(None::<PathBuf>));
    let seen = blocked.clone();
    crate::records_export::BEFORE_EXPORT_SYNC.with(|h| *h.borrow_mut() = Some(Box::new(move |stage: &Path| {
        let data = stage.join("data");
        assert!(std::fs::read_dir(&data).unwrap().any(|e| e.unwrap().path().is_dir()), "an interior folder with folders beneath it");
        std::fs::set_permissions(&data, std::fs::Permissions::from_mode(0o400)).unwrap();
        *seen.borrow_mut() = Some(data);
    })));
    let exported = crate::records_export::export(&f.project, &bag);
    crate::records_export::BEFORE_EXPORT_SYNC.with(|h| *h.borrow_mut() = None);
    let data = blocked.borrow().clone().expect("the seam ran");
    for folder in [data.clone(), bag.join("data")] {
        if folder.exists() { std::fs::set_permissions(&folder, std::fs::Permissions::from_mode(0o700)).unwrap(); }
    }
    assert!(exported.is_err(), "never published over unsynced folders: {exported:?}");
    assert!(!bag.exists(), "nothing published");
    let _ = std::fs::remove_dir_all(data.parent().unwrap());
}

/// The export's administrative snapshot never omits history while keeping
/// its sequence. The events folder is made unexaminable between the strict
/// state read and its examination, in both of export's snapshot reads: the
/// export is refused, never published as verified with its administrative
/// history missing.
#[test]
fn an_export_never_carries_a_snapshot_without_the_history_its_sequence_counts() {
    use std::os::unix::fs::PermissionsExt;
    let f = Fixture::new();
    f.act("close", None).unwrap();
    let dir = f.dir();
    let administration = control(&dir).unwrap();
    let bag = f.output.join("bag");
    let blocked = administration.clone();
    AROUND_SNAPSHOT_EVENTS.with(|h| *h.borrow_mut() = Some(Box::new(move |before: bool| {
        std::fs::set_permissions(&blocked, std::fs::Permissions::from_mode(if before { 0o400 } else { 0o700 })).unwrap();
    })));
    let exported = crate::records_export::export(&f.project, &bag);
    AROUND_SNAPSHOT_EVENTS.with(|h| *h.borrow_mut() = None);
    std::fs::set_permissions(&administration, std::fs::Permissions::from_mode(0o700)).unwrap();
    assert!(exported.is_err(), "never a snapshot without its history: {exported:?}");
    assert!(!bag.exists(), "nothing published");
}

/// A dangling active-association link is there, not "no active
/// association": recording is refused as it is for an active folder whose
/// original intent is lost.
#[test]
fn a_dangling_active_association_never_admits_recording() {
    let f = Fixture::new();
    let base = f.store.join("package-associations");
    std::fs::create_dir_all(&base).unwrap();
    let active = base.join("active");
    let record = || crate::records::append_project(&f.project, None, "app-writer:fixture", "evidence_limit", &crate::records::APP_WRITER, json!({"label":"unresolvable reference","subjectRef":"invented active association"}));
    std::fs::create_dir(&active).unwrap();
    assert!(record().is_err(), "control: an empty active folder refuses");
    std::fs::remove_dir(&active).unwrap();
    std::os::unix::fs::symlink(base.join("no-target"), &active).unwrap();
    let recorded = record();
    assert!(recorded.is_err(), "a dangling active link is never taken for no active association: {recorded:?}");
}

/// An export never publishes a staged member that is a link. After the
/// staged export is verified, its data folder is replaced by a link to that
/// folder (moved aside), once with the target readable and once unreadable
/// (the second reading's construction): the export is refused both times
/// and nothing is published.
#[test]
fn an_export_never_publishes_a_linked_member() {
    use std::os::unix::fs::{symlink, PermissionsExt};
    for readable in [true, false] {
        let f = Fixture::new();
        let moved = f.output.join("moved-data");
        let target = moved.clone();
        let before = std::rc::Rc::new(std::cell::RefCell::new(std::collections::BTreeMap::new()));
        let taken = before.clone();
        crate::records_export::BEFORE_EXPORT_SYNC.with(|h| *h.borrow_mut() = Some(Box::new(move |stage: &Path| {
            std::fs::rename(stage.join("data"), &target).unwrap();
            *taken.borrow_mut() = files_with_bytes(&target);
            symlink(&target, stage.join("data")).unwrap();
            if !readable { std::fs::set_permissions(&target, std::fs::Permissions::from_mode(0o000)).unwrap(); }
        })));
        let bag = f.output.join("bag");
        let exported = crate::records_export::export(&f.project, &bag);
        crate::records_export::BEFORE_EXPORT_SYNC.with(|h| *h.borrow_mut() = None);
        if moved.exists() { std::fs::set_permissions(&moved, std::fs::Permissions::from_mode(0o700)).unwrap(); }
        assert!(exported.is_err(), "readable target {readable}: never published with a link inside: {exported:?}");
        assert!(!bag.exists(), "readable target {readable}: no published destination exists");
        // The refused export's cleanup removes its own staging, never what a
        // link in it pointed to: the target keeps every byte it had.
        let before = before.borrow().clone();
        assert!(before.keys().any(|rel| rel.ends_with(".jsonl")), "readable target {readable}: the target held records to protect: {:?}", before.keys().collect::<Vec<_>>());
        let kept = files_with_bytes(&moved);
        assert_eq!(kept.keys().collect::<Vec<_>>(), before.keys().collect::<Vec<_>>(), "readable target {readable}: every file of the link's target is preserved through cleanup");
        assert!(kept == before, "readable target {readable}: every byte of the link's target is preserved through cleanup");
    }
}

fn publication_interruption(marker: bool) {
    use storage::{PublicationPoint, PublicationStep};
    for subsequent in [false, true] {
        for point in if marker {
            [PublicationPoint::Published, PublicationPoint::Staged]
        } else {
            [PublicationPoint::Staged, PublicationPoint::Published]
        } {
            let f = Fixture::new();
            let dir = f.dir();
            if subsequent {
                f.act("set-hold", None).unwrap();
                if marker {
                    // Exercise marker creation for a surviving first event.
                    std::fs::remove_file(history_marker(&dir).unwrap()).unwrap();
                }
            }
            let before = history_state(&dir).unwrap();
            let events = control(&dir).unwrap().join("events");
            let path = if marker {
                history_marker(&dir).unwrap()
            } else {
                events.join(format!("{:020}.json", before.sequence + 1))
            };
            let staged = std::rc::Rc::new(std::cell::RefCell::new(None));
            let observed = staged.clone();
            storage::publication_hook_for_test(path.clone(), point, move |temporary| {
                *observed.borrow_mut() = Some(temporary.to_path_buf());
                panic!("injected administrative publication interruption at {point:?}");
            });
            let stopped = std::panic::catch_unwind(std::panic::AssertUnwindSafe(|| {
                if marker && subsequent {
                    ensure_history_marker(&dir)
                } else {
                    f.act(
                        if subsequent {
                            "release-hold"
                        } else {
                            "set-hold"
                        },
                        None,
                    )
                    .map(|_| ())
                }
            }));
            assert!(stopped.is_err());
            let temporary = staged.borrow().clone().expect("interruption hook ran");
            assert_ne!(
                temporary.parent(),
                Some(events.as_path()),
                "a temporary must never appear inside events"
            );
            assert_eq!(temporary.parent(), Some(control(&dir).unwrap().as_path()));
            match point {
                PublicationPoint::Staged => assert!(!path.exists()),
                PublicationPoint::Published => {
                    assert_eq!(std::fs::metadata(&path).unwrap().nlink(), 1);
                    read_plain(&path).unwrap();
                    assert!(!temporary.exists());
                }
            }
            let state = history_state(&dir)
                .expect("interrupted publication leaves strict history readable");
            let expected = if marker {
                before.sequence.max(1)
            } else {
                before.sequence + u64::from(point == PublicationPoint::Published)
            };
            assert_eq!(state.sequence, expected);
            let entries = match std::fs::read_dir(&events) {
                Ok(entries) => entries.map(|e| e.unwrap().file_name()).collect::<Vec<_>>(),
                Err(e) if e.kind() == std::io::ErrorKind::NotFound => vec![],
                Err(e) => panic!("events inventory: {e}"),
            };
            assert_eq!(entries.len() as u64, expected);
            for seq in 1..=expected {
                assert!(entries.contains(&format!("{seq:020}.json").into()));
            }
            // Neither ordinary recording nor the next administrative act is
            // stranded by an interrupted stage left outside events.
            f.record();
            let steps = std::rc::Rc::new(std::cell::RefCell::new(Vec::new()));
            let observed = steps.clone();
            storage::observe_publication_for_test(Some(Box::new(move |step, at| {
                observed.borrow_mut().push((step, at.to_path_buf()))
            })));
            f.act(
                if state.hold {
                    "release-hold"
                } else {
                    "set-hold"
                },
                None,
            )
            .unwrap();
            storage::observe_publication_for_test(None);
            let steps = steps.borrow();
            let final_path = events.join(format!("{:020}.json", expected + 1));
            let published = steps
                .iter()
                .position(|(step, at)| *step == PublicationStep::Published && at == &final_path)
                .unwrap();
            let data = steps[..published]
                .iter()
                .rfind(|(step, _)| *step == PublicationStep::DataSynced)
                .unwrap();
            assert_eq!(data.1.parent(), Some(control(&dir).unwrap().as_path()));
            assert!(data
                .1
                .file_name()
                .unwrap()
                .to_string_lossy()
                .starts_with(&format!(
                    ".{}.",
                    final_path.file_name().unwrap().to_string_lossy()
                )));
            assert!(steps[published + 1..]
                .iter()
                .any(|(step, at)| *step == PublicationStep::FileSynced && at == &final_path));
            for folder in [&events, &control(&dir).unwrap()] {
                assert!(steps[published + 1..].iter().any(|(step, at)| *step == PublicationStep::DirectorySynced && at == folder), "both event and staging folders are synced after publication");
            }
            let original = read_plain(&final_path).unwrap();
            let links = std::fs::metadata(&final_path).unwrap().nlink();
            let names = || {
                std::fs::read_dir(control(&dir).unwrap())
                    .unwrap()
                    .map(|entry| entry.unwrap().file_name())
                    .collect::<std::collections::BTreeSet<_>>()
            };
            let before_names = names();
            let error = storage::create_json_staged(
                &final_path,
                &json!({"different":"bytes"}),
                &control(&dir).unwrap(),
            )
            .unwrap_err();
            assert!(
                error.contains("create-once evidence publication") && error.contains("File exists"),
                "{error}"
            );
            assert_eq!(read_plain(&final_path).unwrap(), original);
            assert_eq!(std::fs::metadata(&final_path).unwrap().nlink(), links);
            assert_eq!(
                names(),
                before_names,
                "failed staged publication cleans only its own temporary"
            );
        }
    }
}
#[test]
fn records_store_publication_events_stage_outside_strict_history_at_both_windows() {
    publication_interruption(false);
}
#[test]
fn records_store_publication_history_marker_is_single_link_at_both_windows() {
    publication_interruption(true);
}
