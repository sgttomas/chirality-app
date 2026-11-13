//! Invented local persistence fixtures; these do not witness a human/native act.
use super::*;
use std::os::unix::fs::{symlink, PermissionsExt};
struct Fixture {
    root: PathBuf,
    scope: Scope,
}
impl Fixture {
    fn new() -> Self {
        let root = std::env::temp_dir()
            .canonicalize()
            .unwrap()
            .join(crate::util::opaque_id("native-link-records-").unwrap());
        let project = root.join("project");
        std::fs::create_dir_all(&project).unwrap();
        crate::records_store::use_store_for_test(Some(Ok(crate::records_store::Store {
            root: root.join("store"),
            placement: crate::records_store::Placement::Test,
            limits: vec![],
        })));
        crate::records_store::attach(&project, true).unwrap();
        let scope = Scope::capture(&project).unwrap();
        Self { root, scope }
    }
    fn record(&self) -> Value {
        let g = json!({"home":"invented-home","appSession":"invented-session","spawnCounter":1});
        json!({"format":"chirality.fleet.record","formatVersion":"0.2","observationId":crate::util::opaque_id("fl:app:").unwrap(),"kind":"related_conversation","recorder":{"kind":"App","identity":"app-writer:local"},"observedAt":"invented first observation","body":{"relation":"forked from","source":{"threadId":"invented-source","generation":g},"thread":{"threadId":"invented-fork","generation":g},"nativeHome":{"homeId":"invented-home","root":crate::attachments::native_path_identity(&self.scope.project.path),"physical":{"device":1,"inode":1}},"rpc":{"method":"thread/fork","requestId":1,"requestRef":"invented-rpc:1"},"typesPin":crate::hosting::DECLARED_PIN}})
    }
    fn pending(&self) -> Pending {
        let record = self.record();
        Pending {
            context: SourceContext {
                scope: Ok(self.scope.clone()),
                native_home: Ok(record["body"]["nativeHome"].clone()),
                generation: record["body"]["thread"]["generation"].clone(),
                custody_limit: None,
                activity: crate::records_retention::activity(&self.scope.project.path)
                    .unwrap()
                    .map(Arc::new),
            },
            bytes: line(&record).unwrap(),
            record,
            store_done: false,
            project_done: false,
            first_failure: [None, None],
            events: vec![],
            permanent: None,
        }
    }
    fn put(&self, path: &Path, bytes: &[u8]) {
        std::fs::create_dir_all(path.parent().unwrap()).unwrap();
        std::fs::write(path, bytes).unwrap();
    }
    fn logs(&self) -> (PathBuf, PathBuf) {
        (published_at(&self.scope, 0), published_at(&self.scope, 1))
    }
    fn act(&self, action: &str, bag: Option<&Path>) {
        let actor =
            crate::act_control::person(Some("invented fixture"), Some("invented OS fixture"));
        let observed = json!({"identityVerified":false,"source":"synthetic explicit native event"});
        let plan = crate::records_retention::prepare(
            &self.scope.project.path,
            action,
            bag,
            &actor,
            &observed,
        )
        .unwrap();
        crate::records_retention::apply(plan, &actor, &observed).unwrap();
    }
}
impl Drop for Fixture {
    fn drop(&mut self) {
        FAIL_AFTER_WRITE.with(|f| f.set(None));
        BEFORE_APPEND.with(|h| h.borrow_mut().take());
        crate::records_store::use_store_for_test(None);
        let _ = std::fs::remove_dir_all(&self.root);
    }
}
#[test]
fn native_links_real_publication_after_package_restore_keeps_imported_prefix_quoted() {
    for migrate in [false, true] {
        let mut f = Fixture::new();
        let mut initial = f.pending();
        settle(&mut initial);
        assert!(initial.store_done && initial.project_done);
        drop(initial);
        let (store, _) = f.logs();
        let bag = f.root.join("export-package");
        crate::records_export::export(&f.scope.project.path, &bag).unwrap();
        if migrate {
            crate::records_store::use_store_for_test(Some(Ok(crate::records_store::Store {
                root: f.root.join("destination-store"),
                placement: crate::records_store::Placement::Test,
                limits: vec![],
            })));
        } else {
            std::fs::remove_file(&store).unwrap();
        }
        let actor = crate::act_control::person(Some("invented fixture"), Some("fixture-account"));
        let observed = json!({"fixture":"native writer restoration test double"});
        let plan =
            crate::records_store::package::prepare(&f.scope.project.path, &bag, &actor, &observed)
                .unwrap();
        crate::records_store::package::apply(plan, &actor, &observed).unwrap();
        f.scope = Scope::capture(&f.scope.project.path).unwrap();
        let mut local = f.pending();
        local.record["body"]["rpc"]["requestId"] = json!(2);
        local.record["body"]["rpc"]["requestRef"] = json!("invented-rpc:2");
        local.bytes = line(&local.record).unwrap();
        settle(&mut local);
        assert!(
            local.store_done && local.project_done,
            "local writer remains usable after import: failures={:?}, permanent={:?}",
            local.first_failure,
            local.permanent
        );
        let view = crate::fleet_records::read_for_workspace(Some(&f.scope.project.path)).unwrap();
        let observations = view["coordination"]["appObservations"].as_array().unwrap();
        assert_eq!(
            observations.len(),
            1,
            "imported native-looking row stays quoted; actual later local publication is observed"
        );
        assert_eq!(
            observations[0]["record"]["observationId"],
            local.record["observationId"]
        );
        assert_eq!(
            view["coordination"]["governingStoreRecords"]
                .as_array()
                .unwrap()
                .len(),
            2
        );
    }
}
#[test]
fn native_links_store_first_exact_copy_and_idempotence() {
    let f = Fixture::new();
    let mut p = f.pending();
    let (store, project) = f.logs();
    assert!(publish(&f.scope, &p.record, &p.bytes, 1).is_err());
    assert!(!project.exists());
    settle(&mut p);
    assert!(p.store_done && p.project_done);
    assert_eq!(std::fs::read(&store).unwrap(), p.bytes);
    assert_eq!(std::fs::read(&project).unwrap(), p.bytes);
    settle(&mut p);
    assert_eq!(
        rows(&std::fs::read(&store).unwrap(), true).unwrap().len(),
        1
    );
    for path in [store, project] {
        assert_eq!(
            std::fs::metadata(path).unwrap().permissions().mode() & 0o777,
            0o600
        );
    }
}
#[test]
fn native_links_visible_uncertain_write_recovers_original_id_time_and_distinct_outcomes() {
    let f = Fixture::new();
    let mut p = f.pending();
    let original = p.bytes.clone();
    FAIL_AFTER_WRITE.with(|flag| flag.set(Some(0)));
    settle(&mut p);
    assert!(!p.store_done && !p.project_done);
    assert!(p.first_failure[0].is_some());
    assert_eq!(p.events.len(), 1);
    let event_id = p.events[0].record["observationId"].clone();
    settle(&mut p);
    assert_eq!(p.events.len(), 1);
    assert_eq!(p.events[0].record["observationId"], event_id);
    FAIL_AFTER_WRITE.with(|flag| flag.set(None));
    settle(&mut p);
    assert!(p.store_done && p.project_done);
    assert_eq!(p.bytes, original);
    assert_eq!(p.events.len(), 2);
    let (store, project) = f.logs();
    let rows = rows(&std::fs::read(store).unwrap(), true).unwrap();
    assert_eq!(
        rows.iter().filter(|(_, bytes)| bytes == &original).count(),
        1
    );
    assert_eq!(
        rows.iter()
            .filter(|(r, _)| r["kind"] == "recording_limit")
            .count(),
        1
    );
    assert_eq!(
        rows.iter()
            .filter(|(r, _)| r["kind"] == "recording_recovered")
            .count(),
        1
    );
    assert!(rows[2].0["body"]["statement"]
        .as_str()
        .unwrap()
        .contains("earlier failed/unconfirmed callback"));
    assert_eq!(
        std::fs::read(project).unwrap(),
        rows.iter().flat_map(|(_, b)| b.clone()).collect::<Vec<_>>()
    );
}
#[test]
fn native_links_torn_unknown_duplicate_and_conflicting_logs_refuse_without_repair() {
    for mode in ["torn", "unknown", "duplicate", "conflict"] {
        let f = Fixture::new();
        let mut p = f.pending();
        let mut conflicting = p.record.clone();
        conflicting["body"]["thread"]["threadId"] = json!("different-fork");
        let bytes = match mode {
            "torn" => b"{\"torn\":".to_vec(),
            "unknown" => b"{\"format\":\"unknown\"}\n".to_vec(),
            "duplicate" => [p.bytes.clone(), p.bytes.clone()].concat(),
            _ => line(&conflicting).unwrap(),
        };
        let (store, project) = f.logs();
        f.put(&store, &bytes);
        settle(&mut p);
        assert!(!p.store_done && !p.project_done, "{mode}");
        assert_eq!(std::fs::read(store).unwrap(), bytes);
        assert!(!project.exists());
    }
}
/// Review round 4 of the read-never-creates change: an import account that
/// exists and is empty is unknown here as it is to the store's own reader,
/// and a publication is withheld; only an account that is not there is no
/// import.
#[test]
fn native_links_an_import_account_that_exists_and_is_empty_withholds_publication() {
    let f = Fixture::new();
    let imports = f.scope.dir.path.join("imports.jsonl");
    assert!(!imports.exists());
    assert!(check_import_source(&f.scope.dir.path).is_ok(), "an account that is not there is no import");
    f.put(&imports, b"");
    let withheld = check_import_source(&f.scope.dir.path).unwrap_err();
    assert!(withheld.contains("exists and is empty") && withheld.contains("publication withheld"), "{withheld}");
    std::fs::remove_file(&imports).unwrap();
    assert!(check_import_source(&f.scope.dir.path).is_ok());
}

#[test]
fn native_links_pipe_link_hardlink_and_parent_replacement_refuse() {
    for mode in ["pipe", "link", "hardlink", "parent"] {
        let f = Fixture::new();
        let mut p = f.pending();
        let (store, _) = f.logs();
        std::fs::create_dir_all(store.parent().unwrap()).unwrap();
        let other = f.root.join("invented-other");
        std::fs::write(&other, b"invented unrelated bytes\n").unwrap();
        match mode {
            "pipe" => {
                let name = std::ffi::CString::new(store.as_os_str().as_encoded_bytes()).unwrap();
                assert_eq!(unsafe { libc::mkfifo(name.as_ptr(), 0o600) }, 0);
            }
            "link" => symlink(&other, &store).unwrap(),
            "hardlink" => std::fs::hard_link(&other, &store).unwrap(),
            _ => {
                let parent = store.parent().unwrap().to_owned();
                let moved = parent.with_extension("held-original");
                let foreign = f.root.join("foreign-folder");
                std::fs::create_dir(&foreign).unwrap();
                std::fs::write(foreign.join(LOG), b"foreign bytes\n").unwrap();
                BEFORE_APPEND.with(|h| {
                    *h.borrow_mut() = Some(Box::new(move || {
                        std::fs::rename(&parent, &moved).unwrap();
                        symlink(&foreign, &parent).unwrap();
                    }))
                });
            }
        }
        let before = std::time::Instant::now();
        settle(&mut p);
        assert!(before.elapsed() < std::time::Duration::from_secs(2));
        assert!(!p.store_done && !p.project_done);
        assert_eq!(
            std::fs::read(&other).unwrap(),
            b"invented unrelated bytes\n"
        );
    }
}
#[test]
fn native_links_cold_exact_copy_recovery_is_quoted_and_warm_tick_reuses_basis() {
    let f = Fixture::new();
    let record = f.record();
    let bytes = line(&record).unwrap();
    let (store, project) = f.logs();
    f.put(&store, &bytes);
    let mut cold = Session::default();
    cold.retry(Some(&f.scope.project.path));
    assert_eq!(std::fs::read(&project).unwrap(), bytes);
    assert!(cold.facts.is_empty() && cold.attempts.is_empty());
    assert_eq!(
        cold.snapshot()["quotedCopyRecovery"]["completedCopies"]
            .as_array()
            .unwrap()
            .len(),
        1
    );
    let store_before = std::fs::metadata(&store).unwrap().modified().unwrap();
    let project_before = std::fs::metadata(&project).unwrap().modified().unwrap();
    for _ in 0..3 {
        cold.retry(Some(&f.scope.project.path));
    }
    assert_eq!(
        std::fs::metadata(store).unwrap().modified().unwrap(),
        store_before
    );
    assert_eq!(
        std::fs::metadata(project).unwrap().modified().unwrap(),
        project_before
    );
}
#[test]
fn native_links_observed_prefix_loss_and_changed_association_never_remint() {
    let f = Fixture::new();
    let mut p = f.pending();
    settle(&mut p);
    let (store, project) = f.logs();
    let original = std::fs::read(&store).unwrap();
    std::fs::write(&store, b"").unwrap();
    let mut new = f.record();
    new["body"]["rpc"]["requestId"] = json!(2);
    new["body"]["rpc"]["requestRef"] = json!("invented-rpc:2");
    assert!(publish(&f.scope, &new, &line(&new).unwrap(), 0)
        .unwrap_err()
        .contains("previously accepted"));
    assert_eq!(std::fs::read(&project).unwrap(), original);
    let old = f.scope.project.path.clone();
    let moved = old.with_extension("moved");
    std::fs::rename(&old, &moved).unwrap();
    std::fs::create_dir(&old).unwrap();
    assert!(publish(&f.scope, &new, &line(&new).unwrap(), 0)
        .unwrap_err()
        .contains("changed"));
    assert!(!old.join(crate::records_store::PROJECT_LINK).exists());
}
#[test]
fn native_links_fleet_payload_export_and_terminal_write_refusal() {
    let f = Fixture::new();
    let mut p = f.pending();
    settle(&mut p);
    f.act("close", None);
    let bag = f.root.join("verified-bag");
    crate::records_export::export(&f.scope.project.path, &bag).unwrap();
    assert_eq!(
        std::fs::read(bag.join("data/fleet").join(LOG)).unwrap(),
        std::fs::read(f.logs().0).unwrap()
    );
    f.act("dispose", Some(&bag));
    let before = std::fs::read(f.logs().1).unwrap();
    let mut next = f.record();
    next["body"]["rpc"]["requestId"] = json!(2);
    assert!(publish(&f.scope, &next, &line(&next).unwrap(), 0).is_err());
    let mut cold = Session::default();
    cold.retry(Some(&f.scope.project.path));
    assert!(!f.scope.dir.path.exists());
    assert_eq!(std::fs::read(f.logs().1).unwrap(), before);
    assert!(cold.snapshot()["quotedCopyRecovery"]["limit"].is_string());
}
#[test]
fn native_links_profile_does_not_accept_undertaking_or_unqualified_native_source() {
    let f = Fixture::new();
    let record = f.record();
    validate_record(&record).unwrap();
    for field in ["undertaking", "recordId"] {
        let mut bad = record.clone();
        bad[field] = json!("unqualified");
        assert!(validate_record(&bad).is_err());
    }
    let mut bad = record.clone();
    bad["body"]["nativeHome"]["homeId"] = json!("foreign");
    assert!(validate_record(&bad).is_err());
    let mut bad = record;
    bad["body"]["source"]["threadId"] = bad["body"]["thread"]["threadId"].clone();
    assert!(validate_record(&bad).is_err());
}

#[test]
fn native_links_cold_recovery_records_later_presence_without_rewriting_callback() {
    let f = Fixture::new();
    let mut p = f.pending();
    let original = p.bytes.clone();
    FAIL_AFTER_WRITE.with(|flag| flag.set(Some(1)));
    settle(&mut p);
    assert!(p.store_done && !p.project_done);
    assert_eq!(p.events.len(), 1);
    let original_id = p.record["observationId"].clone();
    FAIL_AFTER_WRITE.with(|flag| flag.set(None));
    let mut cold = Session::default();
    cold.retry(Some(&f.scope.project.path));
    assert!(!cold.has_pending());
    assert!(cold.facts.is_empty());
    let rows = rows(&std::fs::read(f.logs().0).unwrap(), true).unwrap();
    assert_eq!(rows.iter().filter(|(_, b)| b == &original).count(), 1);
    assert_eq!(
        rows.iter()
            .filter(|(r, _)| r["kind"] == "recording_limit"
                && r["body"]["originalObservationId"] == original_id)
            .count(),
        1
    );
    assert_eq!(
        rows.iter()
            .filter(|(r, _)| r["kind"] == "recording_recovered"
                && r["body"]["originalObservationId"] == original_id)
            .count(),
        1
    );
    assert_eq!(
        std::fs::read(f.logs().0).unwrap(),
        std::fs::read(f.logs().1).unwrap()
    );
}
#[test]
fn native_links_closed_cold_mutation_does_not_reserve_new_recording_work() {
    let f = Fixture::new();
    let mut p = f.pending();
    settle(&mut p);
    f.act("close", None);
    let before = std::fs::read(f.logs().0).unwrap();
    std::fs::remove_file(f.logs().1).unwrap();
    let mut cold = Session::default();
    cold.retry(Some(&f.scope.project.path));
    assert!(!cold.has_pending());
    assert!(cold.copies.is_empty());
    assert!(cold.snapshot()["quotedCopyRecovery"]["limit"]
        .as_str()
        .unwrap()
        .contains("closed"));
    assert_eq!(std::fs::read(f.logs().0).unwrap(), before);
    assert!(!f.logs().1.exists());
}

#[test]
fn native_links_original_activity_blocks_another_controller_through_both_copy_phases() {
    let f = Fixture::new();
    let mut p = f.pending();
    let actor =
        crate::act_control::person(Some("invented independent controller"), Some("invented OS"));
    let observed = json!({"fixture":"second retention-controller instance, no live human act"});
    let close = || {
        crate::records_retention::prepare(&f.scope.project.path, "close", None, &actor, &observed)
    };
    assert!(close().err().unwrap().contains("activity"));
    FAIL_AFTER_WRITE.with(|flag| flag.set(Some(1)));
    settle(&mut p);
    assert!(p.store_done && !p.project_done);
    assert!(p.context.activity.is_some());
    assert!(close().err().unwrap().contains("activity"));
    FAIL_AFTER_WRITE.with(|flag| flag.set(None));
    settle(&mut p);
    assert!(p.store_done && p.project_done);
    assert!(p.events.iter().all(|e| e.store_done && e.project_done));
    assert!(p.context.activity.is_none());
    assert!(close().is_ok());
}

#[test]
fn native_links_unknown_torn_or_incomplete_import_cannot_bypass_writer_permission() {
    for kind in ["unknown", "torn", "started"] {
        let f = Fixture::new();
        let mut p = f.pending();
        let data=match kind {"unknown"=>b"{\"format\":\"chirality.records-store.import\",\"formatVersion\":\"0.1\",\"event\":\"unknown\",\"importId\":\"invented\"}\n".to_vec(),"torn"=>b"{\"format\":\"chirality.records-store.import\",\"event\":".to_vec(),_=>b"{\"format\":\"chirality.records-store.import\",\"formatVersion\":\"0.1\",\"event\":\"started\",\"importId\":\"invented\",\"storeHeld\":false}\n".to_vec()};
        f.put(&f.scope.dir.path.join("imports.jsonl"), &data);
        settle(&mut p);
        assert!(!p.store_done && !p.project_done);
        assert!(!f.logs().0.exists() && !f.logs().1.exists());
        assert!(p.first_failure[0].is_some());
        assert_eq!(
            std::fs::read(f.scope.dir.path.join("imports.jsonl")).unwrap(),
            data
        );
    }
}
#[test]
fn native_links_torn_or_unknown_original_registry_is_unavailable_without_reassociation() {
    let f = Fixture::new();
    let path = f.scope.store.path.join("roots.jsonl");
    let original = std::fs::read(&path).unwrap();
    let mut p = f.pending();
    let mut torn = original.clone();
    torn.extend_from_slice(b"{\"unclosed\":");
    std::fs::write(&path, &torn).unwrap();
    assert!(Scope::capture(&f.scope.project.path).is_err());
    settle(&mut p);
    assert!(!p.store_done && !p.project_done);
    assert_eq!(std::fs::read(&path).unwrap(), torn);
    std::fs::write(&path, original).unwrap();
    settle(&mut p);
    assert!(p.store_done && p.project_done);
}

#[test]
fn native_links_payload_and_store_identity_refusal_matches_reader_and_retains_original_fact() {
    for mode in [
        "missing",
        "foreign-project",
        "unknown-project-version",
        "project-pipe",
        "project-link",
        "store-version",
        "link-format",
        "link-version",
        "link-empty-project",
        "link-mistyped-store",
    ] {
        let f = Fixture::new();
        let mut p = f.pending();
        let original_bytes = p.bytes.clone();
        let original_record = p.record.clone();
        let project_identity = f.scope.dir.path.join("project.json");
        let path = if mode == "store-version" {
            f.scope.store.path.join("store.json")
        } else if mode.starts_with("link-") {
            f.scope
                .project
                .path
                .join(crate::records_store::PROJECT_LINK)
        } else {
            project_identity.clone()
        };
        let original_identity = std::fs::read(&path).unwrap();
        match mode {
            "missing" => std::fs::remove_file(&path).unwrap(),
            "project-pipe" => {
                std::fs::remove_file(&path).unwrap();
                let name = std::ffi::CString::new(path.as_os_str().as_encoded_bytes()).unwrap();
                assert_eq!(unsafe { libc::mkfifo(name.as_ptr(), 0o600) }, 0);
            }
            "project-link" => {
                std::fs::remove_file(&path).unwrap();
                let other = f.root.join("other-identity.json");
                std::fs::write(&other, &original_identity).unwrap();
                symlink(&other, &path).unwrap();
            }
            _ => {
                let mut identity: Value = serde_json::from_slice(&original_identity).unwrap();
                if mode == "foreign-project" {
                    identity["projectId"] = json!("chirality-project:unrelated-invented");
                } else if mode == "link-format" {
                    identity["format"] = json!("unknown");
                } else if mode == "link-empty-project" {
                    identity["projectId"] = json!("");
                } else if mode == "link-mistyped-store" {
                    identity["storeId"] = json!(9);
                } else {
                    identity["formatVersion"] = json!("99");
                }
                std::fs::write(&path, serde_json::to_vec(&identity).unwrap()).unwrap();
            }
        }
        let before = std::time::Instant::now();
        assert!(Scope::capture(&f.scope.project.path).is_err(), "{mode}");
        settle(&mut p);
        assert!(before.elapsed() < std::time::Duration::from_secs(2));
        assert!(!p.store_done && !p.project_done);
        assert!(!f.logs().0.exists() && !f.logs().1.exists(), "{mode}");
        let dto = crate::read_fleet_records_for_workspace(Some(&f.scope.project.path)).unwrap();
        assert!(dto["coordination"]["nativeRelationships"]
            .as_array()
            .unwrap()
            .is_empty());
        assert_eq!(dto["coordination"]["protected"]["state"], "unavailable");
        assert_eq!(p.record, original_record);
        assert_eq!(p.bytes, original_bytes);
        assert!(p.context.activity.is_some());
        // The store's identity file is put back in place (the same file, as
        // the open store is bound to it); every other member is made again.
        if mode != "store-version" { std::fs::remove_file(&path).ok(); }
        std::fs::write(&path, &original_identity).unwrap();
        settle(&mut p);
        assert!(p.store_done && p.project_done, "{mode}");
        assert_eq!(p.record, original_record);
        assert_eq!(p.bytes, original_bytes);
        let dto = crate::read_fleet_records_for_workspace(Some(&f.scope.project.path)).unwrap();
        assert_eq!(
            dto["coordination"]["nativeRelationships"]
                .as_array()
                .unwrap()
                .len(),
            1
        );
        assert_eq!(
            dto["coordination"]["nativeRelationships"][0]["record"],
            original_record
        );
        assert_eq!(
            std::fs::read(f.logs().0).unwrap(),
            std::fs::read(f.logs().1).unwrap()
        );
    }
}
#[test]
fn native_links_identity_change_at_append_boundary_refuses_original_line_then_recovers() {
    let f = Fixture::new();
    let mut p = f.pending();
    let identity_path = f.scope.dir.path.join("project.json");
    let saved = std::fs::read(&identity_path).unwrap();
    let original = p.bytes.clone();
    BEFORE_APPEND.with(|h| {
        *h.borrow_mut() = Some(Box::new(move || {
            let mut bad: Value =
                serde_json::from_slice(&std::fs::read(&identity_path).unwrap()).unwrap();
            bad["projectId"] = json!("chirality-project:substituted-at-boundary");
            std::fs::write(identity_path, serde_json::to_vec(&bad).unwrap()).unwrap();
        }))
    });
    settle(&mut p);
    assert!(!p.store_done && !p.project_done);
    assert_eq!(std::fs::read(f.logs().0).unwrap(), b"");
    assert!(
        crate::read_fleet_records_for_workspace(Some(&f.scope.project.path)).unwrap()
            ["coordination"]["nativeRelationships"]
            .as_array()
            .unwrap()
            .is_empty()
    );
    std::fs::write(f.scope.dir.path.join("project.json"), saved).unwrap();
    settle(&mut p);
    assert!(p.store_done && p.project_done);
    assert_eq!(p.bytes, original);
    assert_eq!(
        rows(&std::fs::read(f.logs().0).unwrap(), true)
            .unwrap()
            .iter()
            .filter(|(_, b)| b == &original)
            .count(),
        1
    );
}

#[test]
fn native_links_link_naming_another_identity_attaches_nothing_until_the_person_restores_it() {
    let f = Fixture::new();
    let mut p = f.pending();
    let link = f
        .scope
        .project
        .path
        .join(crate::records_store::PROJECT_LINK);
    let mut claim: Value = serde_json::from_slice(&std::fs::read(&link).unwrap()).unwrap();
    claim["projectId"] = json!("chirality-project:invented-file-claim");
    claim["storeId"] = json!("chirality-store:invented-file-claim");
    std::fs::write(&link, serde_json::to_vec(&claim).unwrap()).unwrap();
    // The store does not choose between the registry's identity and the
    // file's: no recording context, nothing published, nothing read.
    let refused = Scope::capture(&f.scope.project.path).err().unwrap();
    assert!(refused.contains("link changed; not attached"), "{refused}");
    let before = [0, 1].map(|phase| std::fs::read(published_at(&f.scope, phase)).ok());
    settle(&mut p);
    assert!(!p.store_done && !p.project_done, "the pending line waits; it is not written under either identity");
    assert_eq!([0, 1].map(|phase| std::fs::read(published_at(&f.scope, phase)).ok()), before);
    // The fleet read stays available for the project's own files and takes
    // nothing from the store: no protected counterpart, with the reason.
    let unread = crate::read_fleet_records_for_workspace(Some(&f.scope.project.path)).unwrap();
    assert_ne!(unread["coordination"]["protected"]["state"], "attached", "{}", unread["coordination"]["protected"]);
    assert!(unread["coordination"]["protected"].get("projectId").is_none());
    assert!(unread["coordination"]["nativeRelationships"].as_array().unwrap().is_empty());
    assert!(unread["coordination"]["governingStoreRecords"].as_array().unwrap().is_empty());
    assert!(unread["limits"].as_array().unwrap().iter().any(|v| v["reason"]
        .as_str()
        .unwrap_or("")
        .contains("project link names another identity than the protected root association; nothing attached until the person resolves it")));
    // The person restores the link: the waiting line is recorded once.
    crate::records_store::restore_link(&f.scope.project.path).unwrap();
    let scope = Scope::capture(&f.scope.project.path).unwrap();
    assert_eq!(scope.project_id, f.scope.project_id);
    assert_eq!(scope.store_id, f.scope.store_id);
    settle(&mut p);
    assert!(p.store_done && p.project_done);
    let dto = crate::read_fleet_records_for_workspace(Some(&f.scope.project.path)).unwrap();
    assert_eq!(
        dto["coordination"]["nativeRelationships"]
            .as_array()
            .unwrap()
            .len(),
        1
    );
    assert_eq!(
        dto["coordination"]["protected"]["projectId"],
        f.scope.project_id
    );
}

#[test]
fn native_links_link_naming_another_store_attaches_nothing_until_the_person_restores_it() {
    let f = Fixture::new();
    let mut p = f.pending();
    let link = f
        .scope
        .project
        .path
        .join(crate::records_store::PROJECT_LINK);
    let mut claim: Value = serde_json::from_slice(&std::fs::read(&link).unwrap()).unwrap();
    claim["storeId"] = json!("chirality-store:invented-file-claim");
    std::fs::write(&link, serde_json::to_vec(&claim).unwrap()).unwrap();
    let refused = Scope::capture(&f.scope.project.path).err().unwrap();
    assert!(refused.contains("link changed; not attached") && refused.contains("names another records store"), "{refused}");
    let before = [0, 1].map(|phase| std::fs::read(published_at(&f.scope, phase)).ok());
    settle(&mut p);
    assert!(!p.store_done && !p.project_done, "the pending line waits");
    assert_eq!([0, 1].map(|phase| std::fs::read(published_at(&f.scope, phase)).ok()), before);
    let unread = crate::read_fleet_records_for_workspace(Some(&f.scope.project.path)).unwrap();
    assert_ne!(unread["coordination"]["protected"]["state"], "attached");
    assert!(unread["limits"].as_array().unwrap().iter().any(|v| v["reason"]
        .as_str()
        .unwrap_or("")
        .contains("project link names another records store than the protected root association")));
    crate::records_store::restore_link(&f.scope.project.path).unwrap();
    settle(&mut p);
    assert!(p.store_done && p.project_done);
    let dto = crate::read_fleet_records_for_workspace(Some(&f.scope.project.path)).unwrap();
    assert_eq!(
        dto["coordination"]["nativeRelationships"]
            .as_array()
            .unwrap()
            .len(),
        1
    );
    assert_eq!(
        dto["coordination"]["protected"]["projectId"],
        f.scope.project_id
    );
}

/// The registry and an import account holding a closed fragment and its
/// naming line: refused while the fragment is unclosed, then read with only
/// the rows written whole, the fragment left out and nothing in its place.
#[test]
fn native_links_registry_and_import_account_with_a_closed_and_named_fragment_read_only_their_rows() {
    let f = Fixture::new();
    let roots = f.scope.store.path.join("roots.jsonl");
    let imports = f.scope.dir.path.join("imports.jsonl");
    let account = b"{\"format\":\"chirality.records-store.import\",\"formatVersion\":\"0.1\",\"event\":\"started\",\"importId\":\"import:invented\",\"census\":[],\"storeHeld\":false}\n";
    f.put(&imports, account);
    for (path, format) in [(&roots, "chirality.records-store.root"), (&imports, "chirality.records-store.import")] {
        let rows = administrative_lines(path, format).unwrap();
        assert!(!rows.is_empty());
        let mut torn = std::fs::read(path).unwrap();
        torn.extend_from_slice(b"{\"format\":\"chirality.records-store.root\",\"how\":\"rel");
        f.put(path, &torn);
        assert!(administrative_lines(path, format).unwrap_err().contains("unclosed final line"));
        crate::records_store::recover_at_startup().unwrap();
        let closed = std::fs::read(path).unwrap();
        assert!(closed.starts_with(&torn) && closed.len() > torn.len(), "closed and named, bytes kept");
        assert_eq!(administrative_lines(path, format).unwrap(), rows, "{format}: the fragment left out, nothing invented");
    }
    assert!(check_import_source(&f.scope.dir.path).is_ok());
    std::fs::remove_file(&imports).unwrap();
    assert!(Scope::capture(&f.scope.project.path).is_ok());
    let mut p = f.pending();
    settle(&mut p);
    assert!(p.store_done && p.project_done);
}

/// Review round 1, finding 3, on this reader directly: it returns no row it
/// refused before for any reason but a closed fragment named exactly once.
/// The reviewer's two inputs (an exact naming line for a complete unreadable
/// line without the mark; a naming line of another version for a closed
/// fragment) each still refuse, in the registry and in an import account.
#[test]
fn native_links_a_naming_line_for_an_unmarked_line_or_of_another_version_still_refuses() {
    for which in 0..2 {
        let f = Fixture::new();
        let roots = f.scope.store.path.join("roots.jsonl");
        let imports = f.scope.dir.path.join("imports.jsonl");
        f.put(&imports, b"{\"format\":\"chirality.records-store.import\",\"formatVersion\":\"0.1\",\"event\":\"started\",\"importId\":\"import:invented\",\"census\":[],\"storeHeld\":false}\n");
        for (path, format) in [(&roots, "chirality.records-store.root"), (&imports, "chirality.records-store.import")] {
            let whole = std::fs::read(path).unwrap();
            assert!(!administrative_lines(path, format).unwrap().is_empty(), "{format}: read while whole");
            let mut bytes = whole.clone();
            bytes.extend(&crate::records_store::lines::naming_inputs_that_set_nothing_aside(&whole)[which]);
            f.put(path, &bytes);
            assert!(administrative_lines(path, format).is_err(), "{format}, input {which}: no row is returned");
            f.put(path, &whole);
        }
        let whole = std::fs::read(&roots).unwrap();
        let mut bytes = whole.clone();
        bytes.extend(&crate::records_store::lines::naming_inputs_that_set_nothing_aside(&whole)[which]);
        f.put(&roots, &bytes);
        assert!(Scope::capture(&f.scope.project.path).is_err(), "input {which}: no association is taken from such a registry");
    }
}

/// The shared reading has not widened what these readers accept: a line of an
/// unknown format, a naming line that names nothing, an unnamed closed line
/// and an empty line each still refuse.
#[test]
fn native_links_unknown_line_stray_naming_unnamed_closure_or_empty_line_still_refuses() {
    let stray = crate::records_store::lines::naming_line(1, b"invented other bytes").unwrap();
    for extra in [b"{\"format\":\"unknown\",\"formatVersion\":\"0.1\"}\n".to_vec(), stray, b"{\"cut\x1e\n".to_vec(), b"\n".to_vec()] {
        let f = Fixture::new();
        let roots = f.scope.store.path.join("roots.jsonl");
        let mut bytes = std::fs::read(&roots).unwrap();
        bytes.extend(&extra);
        f.put(&roots, &bytes);
        assert!(administrative_lines(&roots, "chirality.records-store.root").is_err(), "{}", String::from_utf8_lossy(&extra));
        assert!(Scope::capture(&f.scope.project.path).is_err());
        let imports = f.scope.dir.path.join("imports.jsonl");
        f.put(&imports, &extra);
        assert!(administrative_lines(&imports, "chirality.records-store.import").is_err());
    }
}
