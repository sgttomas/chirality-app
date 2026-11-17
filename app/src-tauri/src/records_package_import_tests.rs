use super::*;

struct Fixture {
    base: PathBuf,
    root: PathBuf,
    source: PathBuf,
    destination: PathBuf,
    bag: PathBuf,
    project: String,
    original: BTreeMap<String, bag::Member>,
}
fn actor() -> Value {
    crate::act_control::person(Some("Invented fixture"), Some("fixture-account"))
}
fn observed() -> Value {
    json!({"fixture":"native context test double; no actual human act"})
}

// A development export can be consistent BagIt while carrying an operational
// control. Preparation must reject it before publishing an import intent.
fn package_with_active_control(name: &str, bytes: &[u8]) -> Fixture {
    let f = Fixture::new();
    let member = f.bag.join("data").join(name);
    std::fs::create_dir_all(member.parent().unwrap()).unwrap();
    std::fs::write(member, bytes).unwrap();
    let manifest = f.bag.join("manifest-sha256.txt");
    let mut lines = std::fs::read_to_string(&manifest).unwrap();
    lines.push_str(&format!("{}  data/{name}\n", sha256_hex(bytes)));
    std::fs::write(manifest, lines).unwrap();
    let tags = f.bag.join("tagmanifest-sha256.txt");
    let mut rehashed = String::new();
    for line in std::fs::read_to_string(&tags).unwrap().lines() {
        let (_, name) = line.split_once("  ").unwrap();
        rehashed.push_str(&format!("{}  {name}\n", sha256_hex(&std::fs::read(f.bag.join(name)).unwrap())));
    }
    std::fs::write(tags, rehashed).unwrap();
    crate::records_export::verify(&f.bag).unwrap();
    f
}

fn refuses_package_control_before_intent(name: &str, bytes: &[u8]) {
    let f = package_with_active_control(name, bytes);
    let link = std::fs::read(f.root.join(PROJECT_LINK)).unwrap();
    let roots = optional(&f.destination.join("roots.jsonl")).unwrap();
    let error = match prepare(&f.root, &f.bag, &actor(), &observed()) {
        Err(error) => error,
        Ok(_) => panic!("preparation admitted data/{name} ({} bytes)", bytes.len()),
    };
    assert!(error.contains("package payload contains an active owning control"), "{error}");
    assert!(error.contains(&format!("data/{name}")), "refusal must name the member: {error}");
    assert!(!journal(&f.dir()).unwrap().exists(), "no durable import intent");
    assert!(!f.destination.join("package-associations").exists(), "no association intent");
    assert!(!f.dir().join("package-imports").exists(), "no payload receipt");
    assert!(!f.dir().join(name).exists(), "no restored control");
    assert_eq!(optional(&f.destination.join("roots.jsonl")).unwrap(), roots);
    assert_eq!(std::fs::read(f.root.join(PROJECT_LINK)).unwrap(), link);
}

macro_rules! package_control_case {
    ($test:ident, $name:literal, $bytes:expr) => {
        #[test]
        fn $test() { refuses_package_control_before_intent($name, $bytes); }
    };
}
package_control_case!(package_import_control_writer_empty, ".writer.lock", b"");
package_control_case!(package_import_control_writer_bytes, ".writer.lock", b"historical payload bytes");
package_control_case!(package_import_control_observer_empty, ".after-run-end.lock", b"");
package_control_case!(package_import_control_observer_bytes, ".after-run-end.lock", b"historical payload bytes");
package_control_case!(package_import_control_capture_empty, "captures/.capture.lock", b"");
package_control_case!(package_import_control_capture_bytes, "captures/.capture.lock", b"historical payload bytes");
package_control_case!(package_import_control_role_empty, "role-supply/.writer.lock", b"");
package_control_case!(package_import_control_role_bytes, "role-supply/.writer.lock", b"historical payload bytes");

#[test]
fn records_store_routing_package_preparation_interrupts_outside_live_payload() {
    for name in ["captures/.capture.lock", ".writer.lock"] {
        let f = Fixture::new();
        let target = f.dir().join(name);
        bag::fail_control_before_publish_for_test(Some(target.clone()));
        let result = prepare(&f.root, &f.bag, &actor(), &observed());
        bag::fail_control_before_publish_for_test(None);
        assert!(result.as_ref().is_err_and(|e| e.contains("interrupted before publication")), "{name}: {:?}", result.as_ref().err());
        assert!(!target.exists(), "unpublished final control appeared");
        fn temporary_files(dir: &Path, out: &mut Vec<PathBuf>) {
            for entry in std::fs::read_dir(dir).unwrap() {
                let path = entry.unwrap().path();
                if path.is_dir() { temporary_files(&path, out); }
                else if path.extension().is_some_and(|e| e == "tmp") { out.push(path); }
            }
        }
        let mut live = vec![];
        temporary_files(&f.dir(), &mut live);
        assert!(live.is_empty(), "live payload has unpublished temporary: {live:?}");
        let mut staged = vec![];
        temporary_files(&f.destination.join("package-preparation").join(storage::key(&f.project)), &mut staged);
        assert_eq!(staged.len(), 1, "interruption must retain its actual temporary outside payload");
        assert_eq!(std::fs::metadata(&staged[0]).unwrap().dev(), std::fs::metadata(&f.dir()).unwrap().dev());
    }
}
impl Fixture {
    fn new() -> Self {
        Self::named("project")
    }
    fn named(name: &str) -> Self {
        let base = std::env::temp_dir()
            .canonicalize()
            .unwrap()
            .join(crate::util::opaque_id("package-import-test-").unwrap());
        let root = base.join(name);
        std::fs::create_dir_all(&root).unwrap();
        let source = base.join("source-store");
        let destination = base.join("destination-store");
        Self::choose(&source);
        crate::records::append_project(
            &root,
            Some("run:fixture"),
            "app-writer:local",
            "evidence_limit",
            &crate::records::APP_WRITER,
            json!({"label":"unresolvable reference","subjectRef":"invented fixture"}),
        )
        .unwrap();
        let attachment = attach(&root, false).unwrap();
        let project = attachment.project.unwrap();
        let dir = attachment.dir.unwrap();
        let log =
            crate::storage::project_log(&root, Some("run:fixture"), "app-writer:local").unwrap();
        let specs = (0..2)
            .map(|n| crate::records::Spec {
                kind: "evidence_limit",
                recorder: &crate::records::APP_WRITER,
                body: json!({"label":"unresolvable reference","subjectRef":format!("group {n}")}),
                id: format!("rec:app:group-{n}"),
                observed_at: None,
            })
            .collect();
        crate::records::append_group(
            &log,
            specs,
            Some("run:fixture"),
            crate::records::RecordSet::Complete,
        )
        .unwrap();
        std::fs::create_dir_all(dir.join("connectors")).unwrap();
        std::fs::write(
            dir.join("connectors/.route-interrupted.tmp"),
            b"original interrupted bytes",
        )
        .unwrap();
        std::fs::write(
            dir.join("connectors/retained.lock"),
            b"ordinary retained evidence",
        )
        .unwrap();
        let bag = base.join("export/bag");
        std::fs::create_dir_all(bag.parent().unwrap()).unwrap();
        crate::records_export::export(&root, &bag).unwrap();
        let original = bag::payload_inventory(&dir).unwrap();
        Self::choose(&destination);
        Self {
            base,
            root,
            source,
            destination,
            bag,
            project,
            original,
        }
    }
    fn choose(path: &Path) {
        use_store_for_test(Some(Ok(Store {
            root: path.into(),
            placement: Placement::Test,
            limits: vec![],
        })));
    }
    fn dir(&self) -> PathBuf {
        project_dir(&self.destination, &self.project)
    }
    fn plan(&self) -> Plan {
        prepare(&self.root, &self.bag, &actor(), &observed()).unwrap()
    }
    fn import(&self) -> Value {
        apply(self.plan(), &actor(), &observed()).unwrap()
    }
}
impl Drop for Fixture {
    fn drop(&mut self) {
        use_store_for_test(None);
        let _ = std::fs::remove_dir_all(&self.base);
    }
}

#[test]
fn package_import_preserves_original_identity_bytes_groups_and_source() {
    let f = Fixture::new();
    let source_before = bag::payload_inventory(&project_dir(&f.source, &f.project)).unwrap();
    let package_before = std::fs::read(f.bag.join("tagmanifest-sha256.txt")).unwrap();
    let result = f.import();
    assert_eq!(result["state"], "package imported");
    let current = bag::payload_inventory(&f.dir()).unwrap();
    for (name, m) in &f.original {
        assert_eq!(current.get(name), Some(m), "{name}");
    }
    assert_eq!(
        source_before,
        bag::payload_inventory(&project_dir(&f.source, &f.project)).unwrap()
    );
    assert_eq!(
        package_before,
        std::fs::read(f.bag.join("tagmanifest-sha256.txt")).unwrap()
    );
    assert!(crate::records_export::verify(&f.bag).is_ok());
    assert_eq!(
        attach(&f.root, false).unwrap().project.as_deref(),
        Some(f.project.as_str())
    );
    assert!(home(&f.root).unwrap().store_mode);
    assert_eq!(status(&f.root)["state"], "complete");
    let bag2 = f.base.join("export/reexport");
    crate::records_export::export(&f.root, &bag2).unwrap();
    assert!(bag2.join("data/package-imports").is_dir());
}

#[test]
fn package_import_of_a_store_with_a_broken_chain_is_not_refused_and_reports_the_break_before_and_after() {
    let f = Fixture::new();
    // The source store's log is altered in place after it was written: line 1
    // changes, so the link line 2 carries no longer names it. The store keeps
    // the log as it is (a broken chain is reported, never repaired).
    Fixture::choose(&f.source);
    let log = crate::storage::project_log(&f.root, Some("run:fixture"), "app-writer:local").unwrap();
    let mut changed = std::fs::read(&log).unwrap();
    let at = changed.windows(8).position(|w| w == b"invented").unwrap();
    changed[at] = b'I';
    std::fs::write(&log, &changed).unwrap();
    let rel = log.strip_prefix(project_dir(&f.source, &f.project)).unwrap().to_str().unwrap().to_owned();
    // Export is not refused, and the package records the break.
    let bag = f.base.join("export/broken");
    crate::records_export::export(&f.root, &bag).unwrap();
    assert_eq!(std::fs::read(bag.join("data").join(&rel)).unwrap(), changed, "the payload is the store's file byte for byte");
    let verified = crate::records_export::verify(&bag).unwrap();
    // Two statements, never one pass.
    assert_eq!(verified["state"], "package bytes consistent; log integrity limited");
    assert_eq!(verified["packageBytes"], "consistent with the manifests and the recorded chain heads");
    assert_eq!(verified["logIntegrity"]["state"], "limited");
    let named = verified["logIntegrity"]["limits"].as_array().unwrap();
    assert_eq!(named.len(), 1);
    assert!(named[0].as_str().unwrap().starts_with(&format!("{rel}: chain broken at line 2")), "{verified}");
    // The standalone verifier says the same two things, with its own exit status.
    let standalone = std::process::Command::new("python3").arg(bag.join("verify.py")).arg(&bag).output().unwrap();
    assert_eq!(standalone.status.code(), Some(2), "{}", String::from_utf8_lossy(&standalone.stderr));
    let stdout = String::from_utf8_lossy(&standalone.stdout);
    assert!(stdout.starts_with("Manifests and inventory: agree.") && stdout.contains("\nLimits: 1.\n"), "{stdout}");
    assert!(stdout.contains(&format!("  FOUND by this verifier: {rel}: chain broken at line 2")), "{stdout}");
    // Import is not refused: the person is told before deciding, as its own
    // statement, and in the result.
    Fixture::choose(&f.destination);
    let plan = prepare(&f.root, &bag, &actor(), &observed()).unwrap();
    let asked = statement(&plan).unwrap();
    assert!(asked.text.contains("Log integrity: LIMITED."), "{}", asked.text);
    match &asked.in_app {
        // The whole statement names the log and the line.
        None => assert!(asked.text.contains(&format!("{rel}: chain broken at line 2")), "{}", asked.text),
        // Too long for a native alert on this host: the bounded summary
        // still names the line whole, and the App shows every limit.
        Some(shown) => {
            assert!(asked.text.contains("1 limit(s); each is named in full in the App under this confirmation."), "{}", asked.text);
            assert!(shown.content["logIntegrity"]["limits"][0].as_str().unwrap().starts_with(&format!("{rel}: chain broken at line 2")));
        }
    }
    // The summary is checked directly as well, whichever form this host shows.
    let summary = crate::records_export::integrity_summary(plan.snapshot.log_integrity()).unwrap();
    assert!(summary.contains("1 limit(s); each is named in full in the App under this confirmation."), "{summary}");
    let result = apply(plan, &actor(), &observed()).unwrap();
    assert_eq!(result["state"], "package imported; log integrity limited");
    assert!(result["standing"].as_str().unwrap().contains("Log integrity: LIMITED."), "the standing sentence read alone is not a clean pass: {result}");
    assert!(result["logIntegrity"]["limits"][0].as_str().unwrap().contains(&format!("{rel}: chain broken at line 2")), "{result}");
    // Afterwards the imported log is the same bytes, and this store's own
    // reader reports the chain broken at the same line.
    let imported = crate::storage::project_log(&f.root, Some("run:fixture"), "app-writer:local").unwrap();
    assert_eq!(std::fs::read(&imported).unwrap(), changed);
    let heads = crate::records_index::chain_heads(&f.root);
    assert!(heads["broken"].as_array().unwrap().iter().any(|l| l.as_str().unwrap().contains("chain broken at line 2")), "{heads}");
    // A package with no chain recorded broken says so, and nothing more.
    let whole = crate::records_export::verify(&f.bag).unwrap();
    assert_eq!(whole["state"], "package bytes consistent; no chain recorded broken");
    assert_eq!(whole["logIntegrity"], json!({"state":"no chain recorded broken"}));
    assert!(!standing(&whole["logIntegrity"]).contains("Log integrity"));
}

#[test]
fn package_import_interrupted_phases_fence_reads_and_resume_same_intent() {
    for at in [
        "payload",
        "administration",
        "roots-partial",
        "roots",
        "link",
        "completion",
        "completion-published",
    ] {
        let f = Fixture::new();
        let plan = f.plan();
        let id = plan.intent.id.clone();
        STOP.with(|s| *s.borrow_mut() = Some(at));
        assert!(apply(plan, &actor(), &observed())
            .unwrap_err()
            .contains("test interruption"));
        assert_eq!(status(&f.root)["state"], "incomplete");
        assert!(home(&f.root).is_err(), "{at}: read must remain fenced");
        assert!(
            write_dir(&f.root).is_err(),
            "{at}: writes must remain fenced"
        );
        // Model restart: durable evidence, not volatile uncertainty, must fence.
        // A visible completed control must be reconciled in this process. A
        // cold process may use it if it actually survived the interruption.
        if at != "completion-published" {
            UNCERTAIN.lock().unwrap().remove(&f.dir());
        }
        assert!(require_complete(&f.dir()).is_err());
        let retry = prepare_resume(&f.root, &actor(), &observed()).unwrap();
        assert_eq!(retry.intent.id, id);
        apply(retry, &actor(), &observed()).unwrap();
        assert!(require_complete(&f.dir()).is_ok());
        assert_eq!(entries(&f.dir()).unwrap().len(), 1);
        for (name, m) in &f.original {
            assert_eq!(bag::payload_inventory(&f.dir()).unwrap().get(name), Some(m));
        }
    }
}

#[test]
fn package_import_refuses_changed_context_and_conflicts_without_replacement() {
    let f = Fixture::new();
    let plan = f.plan();
    let original = std::fs::read(f.root.join(PROJECT_LINK)).unwrap();
    std::fs::write(f.root.join(PROJECT_LINK), b"different local association").unwrap();
    assert!(apply(plan, &actor(), &observed()).is_err());
    assert!(entries(&f.dir()).unwrap().is_empty());
    std::fs::write(f.root.join(PROJECT_LINK), original).unwrap();
    let conflict = f.dir().join("connectors/retained.lock");
    std::fs::create_dir_all(conflict.parent().unwrap()).unwrap();
    std::fs::write(&conflict, b"different target bytes").unwrap();
    assert!(prepare(&f.root, &f.bag, &actor(), &observed()).is_err());
    assert_eq!(std::fs::read(conflict).unwrap(), b"different target bytes");
}

#[test]
fn package_import_refuses_group_member_identity_collision_in_another_target_log() {
    let f = Fixture::new();
    std::fs::create_dir_all(f.dir().join("acts")).unwrap();
    std::fs::write(
        f.dir().join("acts/other.jsonl"),
        b"{\"recordId\":\"rec:app:group-1\"}\n",
    )
    .unwrap();
    let error = prepare(&f.root, &f.bag, &actor(), &observed())
        .err()
        .unwrap();
    assert!(error.contains("group-1"), "{error}");
    assert!(entries(&f.dir()).unwrap().is_empty());
}

#[test]
fn package_import_revalidation_refuses_actor_source_or_target_mutation() {
    let f = Fixture::new();
    let plan = f.plan();
    assert!(apply(plan, &actor(), &json!({"changed":true})).is_err());
    let plan = f.plan();
    std::fs::write(f.dir().join("unreviewed"), b"new local bytes").unwrap();
    assert!(apply(plan, &actor(), &observed()).is_err());
    assert!(entries(&f.dir()).unwrap().is_empty());
    std::fs::remove_file(f.dir().join("unreviewed")).unwrap();
    let plan = f.plan();
    std::fs::write(f.bag.join("bag-info.txt"), b"source changed").unwrap();
    assert!(apply(plan, &actor(), &observed()).is_err());
    assert!(entries(&f.dir()).unwrap().is_empty());
}

#[test]
fn package_import_recovery_refuses_edited_original_or_staged_package() {
    for edit_stage in [false, true] {
        let f = Fixture::new();
        let plan = f.plan();
        let stage = plan.intent.stage.clone();
        STOP.with(|s| *s.borrow_mut() = Some("payload"));
        assert!(apply(plan, &actor(), &observed()).is_err());
        if edit_stage {
            std::fs::write(stage.join("bag-info.txt"), b"edited after intent").unwrap();
        } else {
            let name = f.original.keys().next().unwrap();
            let path = f.dir().join(name);
            std::fs::create_dir_all(path.parent().unwrap()).unwrap();
            std::fs::write(path, b"conflicting partial publication").unwrap();
        }
        assert!(prepare_resume(&f.root, &actor(), &observed()).is_err());
        assert!(require_complete(&f.dir()).is_err());
    }
}

#[test]
fn package_import_existing_newer_hold_and_closure_survive_recovery() {
    let f = Fixture::new();
    Fixture::choose(&f.source);
    for action in ["set-hold", "close"] {
        let plan = retention::prepare(&f.root, action, None, &actor(), &observed()).unwrap();
        retention::apply(plan, &actor(), &observed()).unwrap();
    }
    // Restore a missing payload member from an older package into the same store.
    let dir = project_dir(&f.source, &f.project);
    std::fs::remove_file(dir.join("connectors/retained.lock")).unwrap();
    let plan = prepare(&f.root, &f.bag, &actor(), &observed()).unwrap();
    apply(plan, &actor(), &observed()).unwrap();
    let state = retention::view(&dir);
    assert_eq!(state["closed"], true);
    assert_eq!(state["legalHold"], true);
    assert!(write_dir(&f.root).is_err());
    assert!(home(&f.root).unwrap().store_mode);
}

#[test]
fn package_import_never_mints_over_missing_or_different_project_identity() {
    let f = Fixture::new();
    std::fs::remove_file(f.root.join(PROJECT_LINK)).unwrap();
    assert!(prepare(&f.root, &f.bag, &actor(), &observed()).is_err());
    assert!(!f.root.join(PROJECT_LINK).exists());
    std::fs::write(
        f.root.join(PROJECT_LINK),
        json_bytes(&link_value("chirality-project:other", "other-store")).unwrap(),
    )
    .unwrap();
    assert!(prepare(&f.root, &f.bag, &actor(), &observed()).is_err());
    assert!(
        matches!(read_link(&f.root),Link::Present{project,..} if project=="chirality-project:other")
    );
}

#[test]
fn package_import_second_interruption_resumes_only_its_own_intent() {
    for at in ["payload", "completion-published"] {
        let f = Fixture::new();
        f.import();
        Fixture::choose(&f.source);
        if attach(&f.root, false).is_ok_and(|a| a.fault == Some("link names another store")) { restore_link(&f.root).unwrap(); }
        std::fs::write(
            project_dir(&f.source, &f.project).join("additional-evidence.json"),
            b"new exact source member",
        )
        .unwrap();
        let second = f.base.join("export/second");
        crate::records_export::export(&f.root, &second).unwrap();
        Fixture::choose(&f.destination);
        if attach(&f.root, false).is_ok_and(|a| a.fault == Some("link names another store")) { restore_link(&f.root).unwrap(); }
        let plan = prepare(&f.root, &second, &actor(), &observed()).unwrap();
        let id = plan.intent.id.clone();
        STOP.with(|s| *s.borrow_mut() = Some(at));
        assert!(apply(plan, &actor(), &observed()).is_err());
        assert_eq!(status(&f.root)["importId"], id);
        let retry = prepare_resume(&f.root, &actor(), &observed()).unwrap();
        assert_eq!(retry.intent.id, id);
        apply(retry, &actor(), &observed()).unwrap();
        assert_eq!(entries(&f.dir()).unwrap().len(), 2);
        assert!(require_complete(&f.dir()).is_ok());
    }
}

#[test]
fn package_import_exact_repeat_is_idempotent_and_keeps_original_origin() {
    let f = Fixture::new();
    f.import();
    let before = bag::payload_inventory(&f.dir()).unwrap();
    let origin = provenance_context(&f.dir()).unwrap();
    let result = f.import();
    assert_eq!(result["state"], "package already present");
    assert_eq!(bag::payload_inventory(&f.dir()).unwrap(), before);
    assert_eq!(provenance_context(&f.dir()).unwrap(), origin);
    assert_eq!(entries(&f.dir()).unwrap().len(), 1);
}

#[test]
fn package_import_partial_control_publications_leave_recoverable_private_evidence() {
    for control in ["intent", "receipt", "completion"] {
        let f = Fixture::new();
        let plan = f.plan();
        let i = plan.intent.clone();
        let path = match control {
            "intent" => i.path().unwrap(),
            "receipt" => f.dir().join(i.receipt_relative()),
            _ => i.completion_path().unwrap(),
        };
        bag::fail_control_before_publish_for_test(Some(path));
        assert!(apply(plan, &actor(), &observed()).is_err());
        assert!(
            std::fs::read_dir(i.stage.parent().unwrap().join("control-staging"))
                .unwrap()
                .count()
                > 0
        );
        // No partial temporary enters either authoritative inventory.
        let controls = std::fs::read_dir(journal(&f.dir()).unwrap())
            .unwrap()
            .map(|e| e.unwrap().file_name().to_string_lossy().into_owned())
            .collect::<Vec<_>>();
        assert!(controls.iter().all(|n| !n.starts_with('.')));
        assert!(bag::payload_inventory(&f.dir())
            .unwrap()
            .keys()
            .all(|n| !n.contains(".tmp") || n == "connectors/.route-interrupted.tmp"));
        UNCERTAIN.lock().unwrap().remove(&f.dir());
        if control == "intent" {
            assert!(
                require_complete(&f.dir()).is_ok(),
                "no intent was published and no payload was admitted"
            );
            assert!(entries(&f.dir()).unwrap().is_empty());
            f.import();
        } else {
            assert!(require_complete(&f.dir()).is_err());
            let retry = prepare_resume(&f.root, &actor(), &observed()).unwrap();
            assert_eq!(retry.intent.id, i.id);
            apply(retry, &actor(), &observed()).unwrap();
        }
        assert!(require_complete(&f.dir()).is_ok());
    }
}

#[test]
fn package_import_resume_preserves_unrelated_newer_roots_tail() {
    let f = Fixture::new();
    let plan = f.plan();
    STOP.with(|s| *s.borrow_mut() = Some("roots"));
    assert!(apply(plan, &actor(), &observed()).is_err());
    append_line(&f.destination.join("roots.jsonl"),&json!({"format":ROOT_FORMAT,"formatVersion":VERSION,"projectId":"other-project","root":f.base.join("other-folder"),"how":"registered"})).unwrap();
    let before = std::fs::read(f.destination.join("roots.jsonl")).unwrap();
    let retry = prepare_resume(&f.root, &actor(), &observed()).unwrap();
    apply(retry, &actor(), &observed()).unwrap();
    assert_eq!(
        std::fs::read(f.destination.join("roots.jsonl")).unwrap(),
        before
    );
}

// ---- The registry's frozen write and the store's own appender ----

/// While an interrupted package import's frozen registry write is pending,
/// a registration, an adoption and a new identity each refuse and leave the
/// registry's bytes as they were, the startup recovery leaves them too, and
/// finishing the import then succeeds as before; afterwards the registry is
/// appended to again.
#[test]
fn package_import_pending_registry_write_holds_every_other_registry_append_until_finished() {
    for at in ["payload", "administration", "roots-partial"] {
        let f = Fixture::new();
        let plan = f.plan();
        assert!(plan.intent.roots_final.len() > plan.intent.roots_original.len(), "{at}: the import appends registry rows");
        STOP.with(|s| *s.borrow_mut() = Some(at));
        assert!(apply(plan, &actor(), &observed()).unwrap_err().contains("test interruption"));
        let path = f.destination.join("roots.jsonl");
        let before = std::fs::read(&path).ok();
        if at == "roots-partial" {
            assert!(!before.as_ref().unwrap().ends_with(b"\n"), "the frozen write left a fragment");
        }
        let pending = "package import's write to the registry of project folders is pending";
        let other = f.base.join("other-folder");
        std::fs::create_dir_all(&other).unwrap();
        // Refused either way, with nothing minted: by the pending write, or,
        // where the frozen write left the registry's last line incomplete, by
        // the registry not read whole, which pull request 240 checks first.
        match attach(&other, true) {
            Err(registration) => assert!(registration.contains(pending), "{at}: registration: {registration}"),
            Ok(refused) => assert!(at == "roots-partial" && refused.project.is_none() && refused.dir.is_none()
                && refused.refusal.as_deref().is_some_and(|r| r.contains("was not read whole")), "{at}: registration: {refused:?}"),
        }
        let renamed = f.base.join("renamed-folder");
        std::fs::create_dir_all(&renamed).unwrap();
        let identity = new_identity(&renamed).unwrap_err();
        let torn = at == "roots-partial" && identity.contains("was not read whole");
        assert!(identity.contains(pending) || torn, "{at}: new identity: {identity}");
        let adopted = f.base.join("adopted-folder");
        std::fs::create_dir_all(adopted.join(".chirality")).unwrap();
        let store_id: Value = serde_json::from_slice(&std::fs::read(f.destination.join("store.json")).unwrap()).unwrap();
        std::fs::write(adopted.join(PROJECT_LINK), serde_json::to_vec(&link_value("chirality-project:invented-adopted", store_id["storeId"].as_str().unwrap())).unwrap()).unwrap();
        let adoption = adopt(&adopted).unwrap_err();
        assert!(adoption.contains(pending) || (at == "roots-partial" && adoption.contains("was not read whole")), "{at}: adoption: {adoption}");
        let left = recover_at_startup().unwrap();
        if at == "roots-partial" {
            assert!(left.iter().any(|l| l.contains(pending)), "{at}: {left:?}");
        }
        assert_eq!(std::fs::read(&path).ok(), before, "{at}: the registry's bytes are unchanged");
        UNCERTAIN.lock().unwrap().remove(&f.dir());
        let retry = prepare_resume(&f.root, &actor(), &observed()).unwrap();
        apply(retry, &actor(), &observed()).unwrap();
        assert!(require_complete(&f.dir()).is_ok(), "{at}: the import finishes");
        assert_eq!(attach(&f.root, false).unwrap().project.as_deref(), Some(f.project.as_str()));
        if at == "roots-partial" {
            // The torn registry refused the first mint before even its link
            // or identity file was written: this is still a new identity.
            assert_eq!(attach(&other, true).unwrap().how, "minted");
        } else {
            // The interrupted first registration already published an
            // identity file. Status requires confirmation, so a write must
            // not complete that association silently, even without records.
            let stopped = attach(&other, false).unwrap();
            let reason = stopped.refusal.unwrap();
            assert_eq!(stopped.fault, Some("no folder recorded"));
            let identity_dir = project_dir(&f.destination, stopped.linked.as_deref().unwrap());
            assert_eq!(bag::payload_inventory(&identity_dir).unwrap().keys().map(String::as_str).collect::<Vec<_>>(), ["project.json"]);
            let view = crate::records_store::status(Some(&other));
            assert_eq!(view["project"]["attachment"]["refusal"], reason);
            assert_eq!(view["project"]["reading"], "nothing from the records store: this folder's project identity is kept there with no folder recorded; not attached to this folder");
            assert!(view["project"]["notes"].as_array().unwrap().iter().all(|note|
                !note.as_str().unwrap().contains("no project identity in the records store")));
            fn bytes(dir: &Path) -> BTreeMap<PathBuf, Vec<u8>> {
                let mut files = BTreeMap::new();
                for entry in std::fs::read_dir(dir).unwrap() {
                    let entry = entry.unwrap();
                    if entry.file_type().unwrap().is_dir() { files.extend(bytes(&entry.path())); }
                    else { files.insert(entry.path(), std::fs::read(entry.path()).unwrap()); }
                }
                files
            }
            let before = bytes(&f.destination);
            assert_eq!(attach(&other, true).unwrap().refusal.as_deref(), Some(reason.as_str()));
            assert_eq!(write_dir(&other).unwrap_err(), reason);
            assert_eq!(bytes(&f.destination), before, "no registration or record bytes changed");
            adopt(&other).unwrap(); // Existing person confirmation; synthetic fixture only.
            assert!(attach(&other, false).unwrap().dir.is_some());
            crate::records::append_project(&other, None, "writer:confirmed", "evidence_limit", &crate::records::APP_WRITER,
                json!({"label":"unresolvable reference","subjectRef":"invented confirmation"})).unwrap();
        }
    }
}

/// Review round 1, finding 1. A package import publishes its own registry
/// write and does not go through the store's appender, so the appender's
/// refusal did not reach it: a second import froze and published its write
/// while another's was pending, and the first could then never finish. Now a
/// new import is refused while another's registry write is pending, when it
/// is prepared and again, under the store lock, before its intent is made
/// durable; nothing of it is left, and both finish in turn.
#[test]
fn package_import_a_second_import_is_refused_while_anothers_registry_write_is_pending() {
    for at in ["payload", "roots-partial"] {
        let f = Fixture::new();
        // Another project with a package of its own, exported from the source store.
        Fixture::choose(&f.source);
        let second_root = f.base.join("second-project");
        std::fs::create_dir_all(&second_root).unwrap();
        crate::records::append_project(&second_root, Some("run:fixture"), "app-writer:local", "evidence_limit", &crate::records::APP_WRITER,
            json!({"label":"unresolvable reference","subjectRef":"invented second fixture"})).unwrap();
        let second_project = attach(&second_root, false).unwrap().project.unwrap();
        let second_bag = f.base.join("export/second-bag");
        crate::records_export::export(&second_root, &second_bag).unwrap();
        Fixture::choose(&f.destination);
        // Prepared before the first import freezes anything durable.
        let early = prepare(&second_root, &second_bag, &actor(), &observed()).unwrap();
        let plan = f.plan();
        STOP.with(|s| *s.borrow_mut() = Some(at));
        assert!(apply(plan, &actor(), &observed()).unwrap_err().contains("test interruption"));
        let path = f.destination.join("roots.jsonl");
        let before = std::fs::read(&path).ok();
        assert!(roots_write_pending(&f.destination, before.as_deref().unwrap_or_default()).unwrap(), "{at}: the first import's registry write is pending");
        let pending = "package import's write to the registry of project folders is pending";
        let prepared = prepare(&second_root, &second_bag, &actor(), &observed()).err().expect("a new import is not prepared");
        assert!(prepared.contains(pending), "{at}: {prepared}");
        let applied = apply(early, &actor(), &observed()).unwrap_err();
        if at == "payload" {
            assert!(applied.contains(pending), "{at}: {applied}");
        }
        let second_dir = project_dir(&f.destination, &second_project);
        assert!(std::fs::symlink_metadata(journal(&second_dir).unwrap()).is_err(), "{at}: the second import left no durable intent");
        assert_eq!(std::fs::read(&path).ok(), before, "{at}: the registry's bytes are unchanged");
        // The first finishes, as before; then the second imports.
        UNCERTAIN.lock().unwrap().remove(&f.dir());
        let retry = prepare_resume(&f.root, &actor(), &observed()).unwrap();
        apply(retry, &actor(), &observed()).unwrap();
        assert!(require_complete(&f.dir()).is_ok(), "{at}: the first import finishes");
        let second = prepare(&second_root, &second_bag, &actor(), &observed()).unwrap();
        apply(second, &actor(), &observed()).unwrap();
        assert!(require_complete(&second_dir).is_ok(), "{at}: then the second imports");
        assert_eq!(attach(&second_root, false).unwrap().project.as_deref(), Some(second_project.as_str()));
    }
}

/// Review round 1, finding 2. Whether a registry write is pending is read
/// from each project's package import journal. A journal that is not there
/// is passed over; one that cannot be examined is a refusal, never "nothing
/// pending": with the project's administration folder unsearchable, a
/// registration is refused, the startup recovery writes nothing, the
/// registry's bytes are unchanged, and the import still finishes once the
/// folder can be read again.
#[test]
fn package_import_a_journal_that_cannot_be_examined_refuses_the_registry_write() {
    use std::os::unix::fs::PermissionsExt;
    let f = Fixture::new();
    let plan = f.plan();
    STOP.with(|s| *s.borrow_mut() = Some("roots-partial"));
    assert!(apply(plan, &actor(), &observed()).unwrap_err().contains("test interruption"));
    let path = f.destination.join("roots.jsonl");
    let before = std::fs::read(&path).unwrap();
    assert!(!before.ends_with(b"\n"), "the frozen write left a fragment");
    let controls = journal(&f.dir()).unwrap().parent().unwrap().to_path_buf();
    let mode = std::fs::metadata(&controls).unwrap().permissions();
    std::fs::set_permissions(&controls, std::fs::Permissions::from_mode(0o000)).unwrap();
    let pending = roots_write_pending(&f.destination, &before);
    let other = f.base.join("other-folder");
    std::fs::create_dir_all(&other).unwrap();
    let registration = attach(&other, true);
    let left = recover_at_startup();
    let after = std::fs::read(&path).unwrap();
    std::fs::set_permissions(&controls, mode).unwrap();
    let unknown = "so whether a registry write is pending is unknown";
    assert!(pending.unwrap_err().contains(unknown));
    // Refused either way, with nothing minted: whether a write is pending is
    // unknown, or, with the registry's last line incomplete, the registry is
    // not read whole, which pull request 240 checks first.
    match registration {
        Err(e) => assert!(e.contains(unknown), "{e}"),
        Ok(refused) => assert!(refused.project.is_none() && refused.dir.is_none()
            && refused.refusal.as_deref().is_some_and(|r| r.contains("was not read whole")), "{refused:?}"),
    }
    assert!(match left { Ok(left) => left.iter().any(|l| l.contains(unknown)), Err(e) => e.contains(unknown) });
    assert_eq!(after, before, "the registry's bytes are unchanged");
    UNCERTAIN.lock().unwrap().remove(&f.dir());
    let retry = prepare_resume(&f.root, &actor(), &observed()).unwrap();
    apply(retry, &actor(), &observed()).unwrap();
    assert!(require_complete(&f.dir()).is_ok(), "the import finishes once its journal can be examined");
}

/// Without a pending import, a fragment in the registry is closed and named,
/// and the package import's readers (its frozen-prefix comparison and its
/// registry reading) ignore the naming line and the set-aside line.
#[test]
fn package_import_readers_ignore_a_closed_and_named_fragment_in_a_later_tail() {
    let f = Fixture::new();
    let plan = f.plan();
    STOP.with(|s| *s.borrow_mut() = Some("roots"));
    assert!(apply(plan, &actor(), &observed()).is_err());
    let path = f.destination.join("roots.jsonl");
    let mut bytes = std::fs::read(&path).unwrap();
    bytes.extend(b"{\"format\":\"chirality.records-store.root\",\"how\":\"rele");
    std::fs::write(&path, &bytes).unwrap();
    *ROOTS.lock().unwrap() = None;
    assert!(recover_at_startup().unwrap().is_empty());
    let after = std::fs::read(&path).unwrap();
    assert!(after.starts_with(&bytes) && after.len() > bytes.len(), "closed and named");
    let read = lines::read(&after, &path);
    assert_eq!(read.set_aside.len(), 1);
    let retry = prepare_resume(&f.root, &actor(), &observed()).unwrap();
    apply(retry, &actor(), &observed()).unwrap();
    assert!(require_complete(&f.dir()).is_ok());
    assert_eq!(std::fs::read(&path).unwrap(), after, "the import's recovery wrote nothing more");
    assert_eq!(attach(&f.root, false).unwrap().project.as_deref(), Some(f.project.as_str()));
}

/// The package import's own registry write emits no raw 0x1E, even for a
/// project folder whose name holds one: serde_json escapes it.
#[test]
fn package_import_registry_write_emits_no_raw_record_separator() {
    let f = Fixture::named("project\u{1e}folder");
    f.import();
    let registry = std::fs::read(f.destination.join("roots.jsonl")).unwrap();
    assert!(!registry.contains(&lines::MARK));
    assert_eq!(attach(&f.root, false).unwrap().project.as_deref(), Some(f.project.as_str()));
}

/// A registry that already holds a closed and named fragment when an import
/// begins: the import freezes those bytes as its original prefix, and every
/// reading of them (the frozen-prefix comparison, the discovery of its own
/// intents from the frozen bytes, the root association) sets the fragment
/// aside and ignores its naming line.
#[test]
fn package_import_reads_a_registry_holding_a_named_fragment_before_it_began() {
    let f = Fixture::new();
    let store = opened().unwrap().0;
    let path = store.join("roots.jsonl");
    let other = json!({"format":ROOT_FORMAT,"formatVersion":VERSION,"projectId":"chirality-project:invented-other","root":f.base.join("elsewhere"),"at":"2026-11-12T00:00:00.000Z","how":"registered"});
    let mut bytes = std::fs::read(&path).unwrap_or_default();
    bytes.extend(serde_json::to_vec(&other).unwrap());
    bytes.extend(b"\n{\"format\":\"chirality.records-store.root\",\"projectId\":\"");
    std::fs::write(&path, &bytes).unwrap();
    *ROOTS.lock().unwrap() = None;
    recover_at_startup().unwrap();
    let closed = std::fs::read(&path).unwrap();
    assert_eq!(lines::read(&closed, &path).set_aside.len(), 1);
    let plan = f.plan();
    assert_eq!(plan.intent.roots_original, closed, "the frozen prefix holds the named fragment");
    STOP.with(|s| *s.borrow_mut() = Some("roots"));
    assert!(apply(plan, &actor(), &observed()).is_err());
    UNCERTAIN.lock().unwrap().remove(&f.dir());
    let retry = prepare_resume(&f.root, &actor(), &observed()).unwrap();
    apply(retry, &actor(), &observed()).unwrap();
    assert!(require_complete(&f.dir()).is_ok());
    assert_eq!(status(&f.root)["state"], "complete");
    assert_eq!(attach(&f.root, false).unwrap().project.as_deref(), Some(f.project.as_str()));
    assert!(roots(&store).unwrap().iter().all(|r| r["format"] == ROOT_FORMAT));
}

/// Review round 3's package-import consequence, as App Agent 0 decided after
/// round 4: an account that exists and yields no import line is unknown,
/// always. A project whose
/// records arrived by package import into this store, with its account then
/// emptied or left holding only closed fragments, reads unknown and is
/// refused, never "no import", through reading and export alike; so does one
/// whose package import is unfinished. The destination's witness is begun
/// before the import, so the project is not listed and no witness line names
/// it: the state in which an exception for "nothing begun" would have read
/// "no import".
#[test]
fn package_import_an_emptied_or_fragments_only_account_is_unknown_never_no_import() {
    let tail = br#"{"format":"chirality.records-import","formatVersion":"#;
    let (closing, line) = crate::records_store::lines::closure(tail);
    let fragments_only = [tail.as_slice(), &closing, &crate::records_store::lines::naming_line(1, &line).unwrap()].concat();
    // `said`: the account's own refusal is the one given; an unfinished
    // import's publication refuses first, with its own words.
    let check = |f: &Fixture, label: &str, account_said: bool| {
        let dir = f.dir();
        for (form, content, said) in [("emptied", Vec::new(), "exists and is empty"), ("fragments only", fragments_only.clone(), "holds no import line, only closed fragments")] {
            std::fs::write(dir.join("imports.jsonl"), &content).unwrap();
            let refused = crate::records_store::home(&f.root).map(|_| ()).unwrap_err();
            assert!(!account_said || (refused.contains(said) && refused.contains("whether an import was begun is not known")), "{label}, {form}: {refused}");
            let (entries, limits) = crate::storage::read_all(&f.root);
            assert!(entries.is_empty() && !limits.is_empty() && (!account_said || limits.iter().any(|l| l.contains(said))), "{label}, {form}: {entries:?} {limits:?}");
            let destination = f.base.join(format!("export-{}-{}", label.replace(' ', "-"), form.replace(' ', "-")));
            let exported = crate::records_export::export(&f.root, &destination);
            assert!(exported.is_err() && !destination.exists(), "{label}, {form}: no verified export: {exported:?}");
        }
        std::fs::remove_file(dir.join("imports.jsonl")).unwrap();
    };
    // A finished package import.
    let f = Fixture::new();
    crate::records_store::witness::begin(&f.destination).unwrap();
    f.import();
    let began = std::fs::read(f.destination.join(crate::records_store::witness::WITNESS_FILE)).unwrap();
    assert!(!String::from_utf8_lossy(&began).contains(&f.project), "the project is neither listed nor named by a witness line");
    check(&f, "finished", true);
    // An unfinished package import (stopped after its payload began).
    let f = Fixture::new();
    crate::records_store::witness::begin(&f.destination).unwrap();
    STOP.with(|flag| *flag.borrow_mut() = Some("payload"));
    assert!(apply(f.plan(), &actor(), &observed()).is_err());
    STOP.with(|flag| *flag.borrow_mut() = None);
    check(&f, "unfinished", false);
}
