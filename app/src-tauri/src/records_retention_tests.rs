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
    assert!(records_store::restore_link(&f.project).is_err());
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
 print('codex-cli 0.160.0');sys.exit(0)
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
