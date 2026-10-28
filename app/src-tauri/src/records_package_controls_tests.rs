//! Invented local recovery fixtures; no live native/person act is witnessed.
use super::*;

fn actor() -> Value {
    crate::act_control::person(
        Some("Invented control-recovery fixture"),
        Some("fixture-account"),
    )
}
fn observed() -> Value {
    json!({"fixture":"explicit native recovery stand-in; no live person act"})
}
struct Fixture {
    base: PathBuf,
    root: PathBuf,
    source: PathBuf,
    destination: PathBuf,
    bag: PathBuf,
    project: String,
    restore_identity: bool,
}
impl Fixture {
    fn new(restore_identity: bool) -> Self {
        let base = std::env::temp_dir()
            .canonicalize()
            .unwrap()
            .join(crate::util::opaque_id("package-control-recovery-").unwrap());
        let root = base.join("project");
        std::fs::create_dir_all(&root).unwrap();
        let source = base.join("source-store");
        let destination = base.join("destination-store");
        Self::choose(&source);
        crate::records::append_project(&root,Some("run:control-fixture"),"app-writer:local",
            "evidence_limit",&crate::records::APP_WRITER,
            json!({"label":"unresolvable reference","subjectRef":"invented original control fixture"})).unwrap();
        let project = attach(&root, false).unwrap().project.unwrap();
        let bag = base.join("original-package");
        crate::records_export::export(&root, &bag).unwrap();
        Self::choose(&destination);
        if restore_identity {
            std::fs::remove_file(root.join(PROJECT_LINK)).unwrap();
        }
        Self {
            base,
            root,
            source,
            destination,
            bag,
            project,
            restore_identity,
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
    fn original_plan(&self) -> Plan {
        if self.restore_identity {
            super::super::prepare_restore(&self.root, &self.bag, &actor(), &observed()).unwrap()
        } else {
            super::super::prepare(&self.root, &self.bag, &actor(), &observed()).unwrap()
        }
    }
    fn import(&self) {
        super::super::apply(self.original_plan(), &actor(), &observed()).unwrap();
    }
    fn row(&self) -> Entry {
        entries(&self.dir()).unwrap().remove(0)
    }
    fn recover(&self, source: Option<&Path>) -> Value {
        let plan = prepare(&self.root, source, &actor(), &observed()).unwrap();
        statement(&plan).unwrap();
        apply(plan, &actor(), &observed()).unwrap()
    }
    fn cold(&self) {
        SEEN.lock().unwrap().remove(&self.dir());
        ORIGINALS.lock().unwrap().remove(&self.dir());
        UNCERTAIN.lock().unwrap().remove(&self.dir());
    }
}
impl Drop for Fixture {
    fn drop(&mut self) {
        STOP.with(|flag| *flag.borrow_mut() = None);
        bag::fail_control_before_publish_for_test(None);
        bag::after_census_for_test(None);
        storage::fail_directory_for_test(None);
        use_store_for_test(None);
        let _ = std::fs::remove_dir_all(&self.base);
    }
}

#[test]
fn missing_derived_receipt_or_completion_recovers_without_another_import_act_warm_and_cold() {
    for cold in [false, true] {
        for receipt in [false, true] {
            let f = Fixture::new(false);
            f.import();
            let row = f.row();
            let original = row.bytes.clone();
            let missing = if receipt {
                f.dir().join(row.intent.receipt_relative())
            } else {
                row.intent.completion_path().unwrap()
            };
            std::fs::remove_file(&missing).unwrap();
            // Pure derivative recovery does not depend on the old private bag.
            std::fs::remove_dir_all(&row.intent.stage).unwrap();
            if cold {
                f.cold();
            }
            assert!(require_complete(&f.dir()).is_err());
            assert_eq!(status(&f.root)["canRepair"], true);
            assert!(!needs_package(&f.root).unwrap());
            assert_eq!(f.recover(None)["state"], "package controls recovered");
            assert_eq!(f.row().bytes, original);
            assert_eq!(entries(&f.dir()).unwrap().len(), 1);
            assert!(require_complete(&f.dir()).is_ok());
            assert!(missing.is_file());
        }
    }
}

#[test]
fn control_repair_preserves_later_local_appends_and_newer_legal_hold() {
    let f = Fixture::new(false);
    f.import();
    crate::records::append_project(
        &f.root,
        Some("run:control-fixture"),
        "app-writer:local",
        "evidence_limit",
        &crate::records::APP_WRITER,
        json!({"label":"unresolvable reference","subjectRef":"invented later local append"}),
    )
    .unwrap();
    let hold = retention::prepare(&f.root, "set-hold", None, &actor(), &observed()).unwrap();
    retention::apply(hold, &actor(), &observed()).unwrap();
    let row = f.row();
    let actual = bag::payload_inventory(&f.dir()).unwrap();
    let admin = retention::export_snapshot(&f.dir(), &f.project, None).unwrap();
    std::fs::remove_file(f.dir().join(row.intent.receipt_relative())).unwrap();
    std::fs::remove_file(row.intent.completion_path().unwrap()).unwrap();
    f.recover(None);
    assert_eq!(bag::payload_inventory(&f.dir()).unwrap(), actual);
    assert_eq!(
        retention::export_snapshot(&f.dir(), &f.project, None).unwrap(),
        admin
    );
    assert_eq!(retention::view(&f.dir())["legalHold"], true);
    assert_eq!(f.row().bytes, row.bytes);
}

#[test]
fn incomplete_original_import_finishes_from_retained_or_reselected_exact_package() {
    for reselect in [false, true] {
        let f = Fixture::new(false);
        let plan = f.original_plan();
        let stage = plan.intent.stage.clone();
        STOP.with(|flag| *flag.borrow_mut() = Some("payload"));
        assert!(super::super::apply(plan, &actor(), &observed()).is_err());
        let original = f.row().bytes;
        if reselect {
            std::fs::remove_dir_all(stage).unwrap();
        }
        f.cold();
        assert_eq!(needs_package(&f.root).unwrap(), reselect);
        if reselect {
            assert!(prepare(&f.root, None, &actor(), &observed()).is_err());
        }
        f.recover(reselect.then_some(f.bag.as_path()));
        assert_eq!(f.row().bytes, original);
        assert_eq!(status(&f.root)["canRepair"], false);
        assert!(require_complete(&f.dir()).is_ok());
    }
}

#[test]
fn missing_association_journal_reference_repairs_only_from_surviving_original_native_intent() {
    for interrupted in [false, true] {
        let f = Fixture::new(true);
        let plan = f.original_plan();
        let path = plan.intent.path().unwrap();
        if interrupted {
            bag::fail_control_before_publish_for_test(Some(path.clone()));
        }
        let result = super::super::apply(plan, &actor(), &observed());
        bag::fail_control_before_publish_for_test(None);
        if interrupted {
            assert!(result.is_err());
        } else {
            result.unwrap();
            std::fs::remove_file(&path).unwrap();
        }
        f.cold();
        let row = f.row();
        assert!(row.missing_entry);
        let original = row.bytes;
        assert!(require_complete(&f.dir()).is_err());
        f.recover(None);
        assert_eq!(f.row().bytes, original);
        assert!(path.is_file());
        assert!(require_complete(&f.dir()).is_ok());
    }
}

#[test]
fn conflicting_controls_original_prefix_or_missing_actual_intent_remain_held() {
    for problem in ["receipt", "completion", "prefix", "intent", "unknown"] {
        let f = Fixture::new(false);
        f.import();
        let row = f.row();
        match problem {
            "receipt" => std::fs::write(
                f.dir().join(row.intent.receipt_relative()),
                b"unequal original receipt",
            )
            .unwrap(),
            "completion" => std::fs::write(row.intent.completion_path().unwrap(), b"{}").unwrap(),
            "prefix" => {
                let member = row
                    .intent
                    .payload
                    .keys()
                    .find(|name| name.ends_with(".jsonl"))
                    .unwrap();
                std::fs::write(f.dir().join(member), b"changed original prefix\n").unwrap();
                std::fs::remove_file(f.dir().join(row.intent.receipt_relative())).unwrap();
            }
            "intent" => {
                std::fs::remove_file(row.intent.path().unwrap()).unwrap();
                f.cold();
            }
            "unknown" => std::fs::write(
                journal(&f.dir()).unwrap().join("unknown.tmp"),
                b"unowned bytes",
            )
            .unwrap(),
            _ => unreachable!(),
        }
        assert!(require_complete(&f.dir()).is_err(), "{problem}");
        assert!(
            prepare(&f.root, None, &actor(), &observed()).is_err(),
            "{problem}"
        );
    }
}

#[test]
fn failed_derived_control_publication_stays_fenced_and_retries_the_same_original_bytes() {
    let f = Fixture::new(false);
    f.import();
    let row = f.row();
    let receipt = f.dir().join(row.intent.receipt_relative());
    std::fs::remove_file(&receipt).unwrap();
    let plan = prepare(&f.root, None, &actor(), &observed()).unwrap();
    bag::fail_control_before_publish_for_test(Some(receipt));
    assert!(apply(plan, &actor(), &observed()).is_err());
    bag::fail_control_before_publish_for_test(None);
    assert!(require_complete(&f.dir()).is_err());
    f.recover(None);
    assert_eq!(f.row().bytes, row.bytes);
    assert_eq!(entries(&f.dir()).unwrap().len(), 1);
    assert!(require_complete(&f.dir()).is_ok());
}

fn package_facts(root: &Path) -> BTreeMap<PathBuf, (u32, Option<String>)> {
    fn visit(root: &Path, path: &Path, out: &mut BTreeMap<PathBuf, (u32, Option<String>)>) {
        let meta = std::fs::symlink_metadata(path).unwrap();
        out.insert(
            path.strip_prefix(root).unwrap().into(),
            (
                meta.mode(),
                meta.is_file()
                    .then(|| sha256_hex(&std::fs::read(path).unwrap())),
            ),
        );
        if meta.is_dir() {
            for entry in std::fs::read_dir(path).unwrap() {
                visit(root, &entry.unwrap().path(), out);
            }
        }
    }
    let mut out = BTreeMap::new();
    visit(root, root, &mut out);
    out
}
fn public_modes(root: &Path) {
    use std::os::unix::fs::PermissionsExt;
    let meta = std::fs::symlink_metadata(root).unwrap();
    std::fs::set_permissions(
        root,
        std::fs::Permissions::from_mode(if meta.is_dir() { 0o755 } else { 0o644 }),
    )
    .unwrap();
    if meta.is_dir() {
        for entry in std::fs::read_dir(root).unwrap() {
            public_modes(&entry.unwrap().path());
        }
    }
}

#[test]
fn exact_reselected_public_mode_backup_is_private_custody_without_source_changes() {
    let f = Fixture::new(false);
    let plan = f.original_plan();
    let stage = plan.intent.stage_path();
    STOP.with(|flag| *flag.borrow_mut() = Some("payload"));
    assert!(super::super::apply(plan, &actor(), &observed()).is_err());
    let original = f.row().bytes;
    std::fs::remove_dir_all(&stage).unwrap();
    public_modes(&f.bag);
    let before = package_facts(&f.bag);
    f.recover(Some(&f.bag));
    assert_eq!(
        package_facts(&f.bag),
        before,
        "recovery never chmods or edits the selected backup"
    );
    assert_eq!(f.row().bytes, original);
    assert!(
        bag::inspect(&stage).is_ok(),
        "restored private stage retains its own custody rules"
    );
}

#[test]
fn unequal_reselected_package_does_not_reserve_the_original_stage_slot() {
    let f = Fixture::new(false);
    let plan = f.original_plan();
    let stage = plan.intent.stage_path();
    STOP.with(|flag| *flag.borrow_mut() = Some("payload"));
    assert!(super::super::apply(plan, &actor(), &observed()).is_err());
    std::fs::remove_dir_all(&stage).unwrap();
    Fixture::choose(&f.source);
    crate::records::append_project(
        &f.root,
        Some("run:different-backup"),
        "app-writer:local",
        "evidence_limit",
        &crate::records::APP_WRITER,
        json!({"label":"unresolvable reference","subjectRef":"different backup evidence"}),
    )
    .unwrap();
    let unequal = f.base.join("different-package");
    crate::records_export::export(&f.root, &unequal).unwrap();
    Fixture::choose(&f.destination);
    assert!(prepare(&f.root, Some(&unequal), &actor(), &observed()).is_err());
    assert!(
        !stage.exists(),
        "a different package cannot occupy the original missing bag slot"
    );
    assert!(require_complete(&f.dir()).is_err());
    f.recover(Some(&f.bag));
    assert!(require_complete(&f.dir()).is_ok());
}

#[test]
fn failed_reselected_private_copy_keeps_fixed_original_stage_absent_and_retryable() {
    let f = Fixture::new(false);
    let plan = f.original_plan();
    let stage = plan.intent.stage_path();
    STOP.with(|flag| *flag.borrow_mut() = Some("payload"));
    assert!(super::super::apply(plan, &actor(), &observed()).is_err());
    let original = f.row().bytes;
    std::fs::remove_dir_all(&stage).unwrap();
    let external = package_facts(&f.bag);
    let parent = stage.parent().unwrap().to_path_buf();
    // The first snapshot takes external custody; interrupt the second private
    // copy after its destination exists, reproducing a retained partial stage.
    bag::after_census_for_test(Some(Box::new(move || {
        bag::after_census_for_test(Some(Box::new(move || {
            let review = std::fs::read_dir(parent)
                .unwrap()
                .map(Result::unwrap)
                .find(|row| {
                    row.file_name()
                        .to_str()
                        .unwrap()
                        .starts_with("reselected-review-")
                })
                .unwrap()
                .path();
            std::fs::write(
                review.join("bag/bag-info.txt"),
                b"injected changed private copy source",
            )
            .unwrap();
        })));
    })));
    let error = prepare(&f.root, Some(&f.bag), &actor(), &observed())
        .err()
        .unwrap();
    assert!(
        error.contains("snapshot") || error.contains("changed"),
        "{error}"
    );
    assert!(
        !stage.exists(),
        "a failed private rebuild cannot occupy the fixed original stage name"
    );
    assert!(needs_package(&f.root).unwrap());
    assert_eq!(package_facts(&f.bag), external);
    assert_eq!(f.row().bytes, original);
    assert!(require_complete(&f.dir()).is_err());
    f.recover(Some(&f.bag));
    assert!(bag::inspect(&stage).is_ok());
    assert!(require_complete(&f.dir()).is_ok());
    assert_eq!(package_facts(&f.bag), external);
    assert_eq!(f.row().bytes, original);
}

#[test]
fn unknown_fixed_original_stage_arriving_during_private_rebuild_is_never_replaced() {
    let f = Fixture::new(false);
    let plan = f.original_plan();
    let stage = plan.intent.stage_path();
    STOP.with(|flag| *flag.borrow_mut() = Some("payload"));
    assert!(super::super::apply(plan, &actor(), &observed()).is_err());
    std::fs::remove_dir_all(&stage).unwrap();
    let unknown = stage.clone();
    bag::after_census_for_test(Some(Box::new(move || {
        bag::after_census_for_test(Some(Box::new(move || {
            bag::create_or_match(
                &unknown.join("unknown-existing-member"),
                b"invented unknown stage; retain unchanged",
            )
            .unwrap();
        })));
    })));
    assert!(prepare(&f.root, Some(&f.bag), &actor(), &observed()).is_err());
    let before = package_facts(&stage);
    assert_eq!(
        before.keys().cloned().collect::<Vec<_>>(),
        vec![PathBuf::new(), PathBuf::from("unknown-existing-member")],
        "no copied package member may be added to the unknown fixed stage"
    );
    assert_eq!(
        std::fs::read(stage.join("unknown-existing-member")).unwrap(),
        b"invented unknown stage; retain unchanged"
    );
    assert!(prepare(&f.root, Some(&f.bag), &actor(), &observed()).is_err());
    assert_eq!(package_facts(&stage), before);
    assert!(require_complete(&f.dir()).is_err());
}

#[test]
fn safe_prior_derivative_repair_unblocks_but_does_not_complete_a_later_original_import() {
    let f = Fixture::new(false);
    f.import();
    let first = f.row();
    Fixture::choose(&f.source);
    for run in ["run:later-one", "run:later-two"] {
        crate::records::append_project(
            &f.root,
            Some(run),
            "app-writer:local",
            "evidence_limit",
            &crate::records::APP_WRITER,
            json!({"label":"unresolvable reference","subjectRef":run}),
        )
        .unwrap();
    }
    let later = f.base.join("later-package");
    crate::records_export::export(&f.root, &later).unwrap();
    Fixture::choose(&f.destination);
    let later_plan = super::super::prepare(&f.root, &later, &actor(), &observed()).unwrap();
    let later_id = later_plan.intent.id.clone();
    assert!(later_plan.intent.copied.len() >= 2);
    STOP.with(|flag| *flag.borrow_mut() = Some("payload"));
    assert!(super::super::apply(later_plan, &actor(), &observed()).is_err());
    std::fs::remove_file(f.dir().join(first.intent.receipt_relative())).unwrap();
    let plan = prepare(&f.root, None, &actor(), &observed()).unwrap();
    assert_eq!(plan.work.len(), 1);
    assert_eq!(plan.work[0].entry.intent.id, first.intent.id);
    assert_eq!(plan.deferred, vec![later_id.clone()]);
    statement(&plan).unwrap();
    let result = apply(plan, &actor(), &observed()).unwrap();
    assert_eq!(result["state"], "package controls partly recovered");
    assert_eq!(result["deferredImports"], json!([later_id]));
    assert!(f.dir().join(first.intent.receipt_relative()).is_file());
    assert!(
        require_complete(&f.dir()).is_err(),
        "the later incomplete operation stays fenced"
    );
    f.recover(None);
    assert!(require_complete(&f.dir()).is_ok());
    assert_eq!(entries(&f.dir()).unwrap().len(), 2);
    assert_eq!(
        entries(&f.dir())
            .unwrap()
            .into_iter()
            .find(|e| e.intent.id == first.intent.id)
            .unwrap()
            .bytes,
        first.bytes
    );
}

#[test]
fn visible_repaired_completion_with_uncertain_final_sync_keeps_the_same_intent_fenced() {
    let f = Fixture::new(false);
    f.import();
    let row = f.row();
    std::fs::remove_file(row.intent.completion_path().unwrap()).unwrap();
    let plan = prepare(&f.root, None, &actor(), &observed()).unwrap();
    storage::fail_directory_for_test(Some(journal(&f.dir()).unwrap()));
    assert!(apply(plan, &actor(), &observed()).is_err());
    storage::fail_directory_for_test(None);
    assert!(
        f.row().done.is_some(),
        "completed bytes may be visible after an uncertain extra flush"
    );
    assert!(require_complete(&f.dir()).is_err());
    f.recover(None);
    assert_eq!(f.row().bytes, row.bytes);
    assert_eq!(entries(&f.dir()).unwrap().len(), 1);
    assert!(require_complete(&f.dir()).is_ok());
}

#[test]
fn changed_reselected_source_after_native_question_refuses_recovery_without_another_act() {
    let f = Fixture::new(false);
    let plan = f.original_plan();
    let stage = plan.intent.stage_path();
    STOP.with(|flag| *flag.borrow_mut() = Some("payload"));
    assert!(super::super::apply(plan, &actor(), &observed()).is_err());
    let original = f.row().bytes;
    std::fs::remove_dir_all(stage).unwrap();
    let recovery = prepare(&f.root, Some(&f.bag), &actor(), &observed()).unwrap();
    std::fs::write(
        f.bag.join("bag-info.txt"),
        b"source changed during native question",
    )
    .unwrap();
    assert!(apply(recovery, &actor(), &observed()).is_err());
    assert_eq!(f.row().bytes, original);
    assert!(require_complete(&f.dir()).is_err());
    // The already verified original private copy remains independently usable.
    f.recover(None);
    assert_eq!(f.row().bytes, original);
}

#[test]
fn cold_missing_prior_association_reference_keeps_imported_prefix_after_later_import() {
    let mut f = Fixture::new(false);
    Fixture::choose(&f.source);
    let fleet = json!({"format":"chirality.fleet.record","formatVersion":"0.1","recordId":"fl:historical-imported-fixture",
        "kind":"child_observed","undertaking":"invented historical fixture","recorder":{"kind":"App","identity":"app-writer:local"},
        "writtenAt":"invented fixture time","body":{"childThread":"invented-child","status":"invented observation",
            "observation":{"source":"invented historical package","at":"fixture","pin":"fixture","standing":"observed"}}});
    let fleet_bytes = format!("{fleet}\n").into_bytes();
    crate::fleet_records::validate_line(&fleet_bytes).unwrap();
    let fleet_relative = "fleet/coordination.fleet.jsonl";
    let fleet_path = project_dir(&f.source, &f.project).join(fleet_relative);
    std::fs::create_dir_all(fleet_path.parent().unwrap()).unwrap();
    std::fs::write(fleet_path, &fleet_bytes).unwrap();
    f.bag = f.base.join("original-package-with-fleet");
    crate::records_export::export(&f.root, &f.bag).unwrap();
    Fixture::choose(&f.destination);
    std::fs::remove_file(f.root.join(PROJECT_LINK)).unwrap();
    f.restore_identity = true;
    f.import();
    let first = f.row();
    Fixture::choose(&f.source);
    crate::records::append_project(
        &f.root,
        Some("run:later-association"),
        "app-writer:local",
        "evidence_limit",
        &crate::records::APP_WRITER,
        json!({"label":"unresolvable reference","subjectRef":"later association fixture"}),
    )
    .unwrap();
    let later = f.base.join("later-association-package");
    crate::records_export::export(&f.root, &later).unwrap();
    Fixture::choose(&f.destination);
    let plan = super::super::prepare_restore(&f.root, &later, &actor(), &observed()).unwrap();
    assert!(!plan.intent.copied.contains_key(fleet_relative));
    let later_id = plan.intent.id.clone();
    super::super::apply(plan, &actor(), &observed()).unwrap();
    let later_raw = entries(&f.dir())
        .unwrap()
        .into_iter()
        .find(|row| row.intent.id == later_id)
        .unwrap()
        .bytes;
    std::fs::remove_file(first.intent.path().unwrap()).unwrap();
    f.cold();
    assert!(
        quoted_prefix(&f.dir(), fleet_relative, &fleet_bytes).is_err(),
        "lost A reference keeps provenance fenced, even though B retains these bytes"
    );
    let rows = entries(&f.dir()).unwrap();
    assert_eq!(rows.len(), 2);
    assert!(
        rows.iter()
            .find(|row| row.intent.id == first.intent.id)
            .unwrap()
            .missing_entry
    );
    f.recover(None);
    let rows = entries(&f.dir()).unwrap();
    assert_eq!(rows.len(), 2);
    assert_eq!(
        rows.iter()
            .find(|row| row.intent.id == first.intent.id)
            .unwrap()
            .bytes,
        first.bytes
    );
    assert_eq!(
        rows.iter()
            .find(|row| row.intent.id == later_id)
            .unwrap()
            .bytes,
        later_raw
    );
    assert_eq!(
        quoted_prefix(&f.dir(), fleet_relative, &fleet_bytes).unwrap(),
        fleet_bytes.len() as u64,
        "repair retains A's imported prefix, rather than treating B's exact existing copy as local"
    );
    let original = identity::original_context(&first.intent, &first.bytes).unwrap();
    let original = PathBuf::from(original["path"].as_str().unwrap());
    std::fs::remove_file(original).unwrap();
    f.cold();
    assert!(require_complete(&f.dir()).is_err());
    assert!(
        quoted_prefix(&f.dir(), fleet_relative, &fleet_bytes).is_err(),
        "lost actual native A intent cannot be replaced by a receipt or B's existing-copy claim"
    );
}

#[test]
fn identical_original_native_intent_replacement_during_question_refuses_control_recovery() {
    let f = Fixture::new(true);
    f.import();
    let row = f.row();
    std::fs::remove_file(f.dir().join(row.intent.receipt_relative())).unwrap();
    let plan = prepare(&f.root, None, &actor(), &observed()).unwrap();
    let original = f
        .destination
        .join("package-associations/active/intent.json");
    let bytes = std::fs::read(&original).unwrap();
    std::fs::rename(
        &original,
        f.base.join("original-native-intent-before-replacement"),
    )
    .unwrap();
    std::fs::write(&original, &bytes).unwrap();
    let error = apply(plan, &actor(), &observed()).unwrap_err();
    assert!(error.contains("changed"), "{error}");
    assert_eq!(std::fs::read(original).unwrap(), bytes);
    assert!(require_complete(&f.dir()).is_err());
    f.recover(None);
    assert_eq!(f.row().bytes, row.bytes);
}

fn completed_identity_roundtrip(f: &Fixture) -> (Entry, Entry) {
    f.import();
    let first = f.row();
    new_identity(&f.root).unwrap();
    let startup = attach(&f.root, false).unwrap().project.unwrap();
    assert_ne!(startup, f.project);
    let plan = super::super::prepare_restore(&f.root, &f.bag, &actor(), &observed()).unwrap();
    assert!(plan.intent.association.is_some());
    let later = plan.intent.id.clone();
    super::super::apply(plan, &actor(), &observed()).unwrap();
    let later = entries(&f.dir())
        .unwrap()
        .into_iter()
        .find(|row| row.intent.id == later)
        .unwrap();
    assert!(later.done.is_some());
    (first, later)
}

fn lose_prior_derivatives(f: &Fixture, first: &Entry) {
    std::fs::remove_file(first.intent.path().unwrap()).unwrap();
    std::fs::remove_file(f.dir().join(first.intent.receipt_relative())).unwrap();
    f.cold();
}

#[test]
fn prior_controls_recover_after_a_completed_native_identity_roundtrip_without_rewriting_roots() {
    let f = Fixture::new(true);
    let (first, later) = completed_identity_roundtrip(&f);
    // The existing unrelated-tail rule remains usable after the witnessed
    // round trip; neither native operation may authorize another related tail.
    let other = f.base.join("unrelated-project");
    std::fs::create_dir(&other).unwrap();
    assert_ne!(attach(&other, true).unwrap().project.unwrap(), f.project);
    let roots = std::fs::read(f.destination.join("roots.jsonl")).unwrap();
    let payload = bag::payload_inventory(&f.dir()).unwrap();
    lose_prior_derivatives(&f, &first);
    assert!(!needs_package(&f.root).unwrap());
    let plan = prepare(&f.root, None, &actor(), &observed()).unwrap();
    assert_eq!(plan.work.len(), 1);
    assert!(matches!(plan.work[0].kind, WorkKind::Controls));
    assert_eq!(
        plan.work[0].context["rootsWitness"]["importId"],
        later.intent.id
    );
    statement(&plan).unwrap();
    apply(plan, &actor(), &observed()).unwrap();
    assert_eq!(
        std::fs::read(f.destination.join("roots.jsonl")).unwrap(),
        roots
    );
    assert_eq!(bag::payload_inventory(&f.dir()).unwrap(), payload);
    assert_eq!(
        entries(&f.dir())
            .unwrap()
            .into_iter()
            .find(|row| row.intent.id == first.intent.id)
            .unwrap()
            .bytes,
        first.bytes
    );
    assert!(require_complete(&f.dir()).is_ok());
}

#[test]
fn cold_loss_of_prior_reference_completion_and_root_locator_retains_required_native_import() {
    let mut f = Fixture::new(false);
    Fixture::choose(&f.source);
    let fleet = json!({"format":"chirality.fleet.record","formatVersion":"0.1","recordId":"fl:triple-loss-imported-fixture",
        "kind":"child_observed","undertaking":"invented historical fixture","recorder":{"kind":"App","identity":"app-writer:local"},
        "writtenAt":"invented fixture time","body":{"childThread":"invented-child","status":"invented observation",
            "observation":{"source":"invented historical package","at":"fixture","pin":"fixture","standing":"observed"}}});
    let fleet_bytes = format!("{fleet}\n").into_bytes();
    crate::fleet_records::validate_line(&fleet_bytes).unwrap();
    let relative = "fleet/coordination.fleet.jsonl";
    let source = project_dir(&f.source, &f.project).join(relative);
    std::fs::create_dir_all(source.parent().unwrap()).unwrap();
    std::fs::write(source, &fleet_bytes).unwrap();
    f.bag = f.base.join("triple-loss-original-package");
    crate::records_export::export(&f.root, &f.bag).unwrap();
    Fixture::choose(&f.destination);
    std::fs::remove_file(f.root.join(PROJECT_LINK)).unwrap();
    f.restore_identity = true;
    let (first, later) = completed_identity_roundtrip(&f);
    assert!(first.intent.copied.contains_key(relative));
    assert!(!later.intent.copied.contains_key(relative));
    let original = identity::original_context(&first.intent, &first.bytes).unwrap();
    let original = PathBuf::from(original["path"].as_str().unwrap());
    assert_eq!(
        original,
        f.destination
            .join("package-associations/history")
            .join(&first.intent.id)
            .join("intent.json")
    );
    assert!(original.is_file());
    std::fs::remove_file(first.intent.path().unwrap()).unwrap();
    std::fs::remove_file(first.intent.completion_path().unwrap()).unwrap();
    let root_locator = f
        .destination
        .join("package-associations/roots")
        .join(storage::key(f.root.to_str().unwrap()))
        .join(format!("{}.json", first.intent.id));
    std::fs::remove_file(&root_locator).unwrap();
    f.cold();
    let quoted = quoted_prefix(&f.dir(), relative, &fleet_bytes);
    assert!(
        quoted.is_err(),
        "lost prior derivatives must fence its prefix instead of forgetting original A: {quoted:?}"
    );
    let rows = entries(&f.dir()).unwrap();
    let prior = rows
        .iter()
        .find(|row| row.intent.id == first.intent.id)
        .unwrap();
    assert!(prior.missing_entry && prior.done.is_none());
    assert!(!prior.missing_receipt);
    assert_eq!(prior.bytes, first.bytes);
    assert!(!needs_package(&f.root).unwrap());
    let roots = std::fs::read(f.destination.join("roots.jsonl")).unwrap();
    let payload = bag::payload_inventory(&f.dir()).unwrap();
    let plan = prepare(&f.root, None, &actor(), &observed()).unwrap();
    assert_eq!(plan.work.len(), 1);
    assert!(matches!(plan.work[0].kind, WorkKind::Controls));
    assert_eq!(plan.work[0].entry.intent.id, first.intent.id);
    assert_eq!(
        plan.work[0].context["rootsWitness"]["importId"],
        later.intent.id
    );
    statement(&plan).unwrap();
    apply(plan, &actor(), &observed()).unwrap();
    assert_eq!(
        quoted_prefix(&f.dir(), relative, &fleet_bytes).unwrap(),
        fleet_bytes.len() as u64
    );
    assert_eq!(
        std::fs::read(f.destination.join("roots.jsonl")).unwrap(),
        roots
    );
    assert_eq!(bag::payload_inventory(&f.dir()).unwrap(), payload);
    assert_eq!(std::fs::read(&original).unwrap(), first.bytes);
    std::fs::remove_file(original).unwrap();
    f.cold();
    assert!(require_complete(&f.dir()).is_err());
    assert!(quoted_prefix(&f.dir(), relative, &fleet_bytes).is_err());
    assert!(
        prepare(&f.root, None, &actor(), &observed()).is_err(),
        "foreign receipt or later existing-copy claim cannot replace the lost actual A"
    );
}

#[test]
fn cold_loss_of_an_ordinary_native_import_without_roots_rows_keeps_its_receipt_held() {
    let f = Fixture::new(false);
    f.import();
    Fixture::choose(&f.source);
    let fleet = json!({"format":"chirality.fleet.record","formatVersion":"0.1","recordId":"fl:ordinary-lost-import-fixture",
        "kind":"child_observed","undertaking":"invented historical fixture","recorder":{"kind":"App","identity":"app-writer:local"},
        "writtenAt":"invented fixture time","body":{"childThread":"invented-child","status":"invented observation",
            "observation":{"source":"invented historical package","at":"fixture","pin":"fixture","standing":"observed"}}});
    let fleet_bytes = format!("{fleet}\n").into_bytes();
    crate::fleet_records::validate_line(&fleet_bytes).unwrap();
    let relative = "fleet/coordination.fleet.jsonl";
    let source = project_dir(&f.source, &f.project).join(relative);
    std::fs::create_dir_all(source.parent().unwrap()).unwrap();
    std::fs::write(source, &fleet_bytes).unwrap();
    let ordinary_bag = f.base.join("ordinary-native-fleet-package");
    crate::records_export::export(&f.root, &ordinary_bag).unwrap();
    Fixture::choose(&f.destination);
    let ordinary = super::super::prepare(&f.root, &ordinary_bag, &actor(), &observed()).unwrap();
    assert!(ordinary.intent.association.is_none());
    assert!(ordinary.intent.copied.contains_key(relative));
    assert_eq!(ordinary.intent.roots_original, ordinary.intent.roots_final);
    let lost_id = ordinary.intent.id.clone();
    super::super::apply(ordinary, &actor(), &observed()).unwrap();
    let lost = entries(&f.dir())
        .unwrap()
        .into_iter()
        .find(|row| row.intent.id == lost_id)
        .unwrap();
    Fixture::choose(&f.source);
    crate::records::append_project(
        &f.root,
        Some("run:after-ordinary-native-import"),
        "app-writer:local",
        "evidence_limit",
        &crate::records::APP_WRITER,
        json!({"label":"unresolvable reference","subjectRef":"invented later native import"}),
    )
    .unwrap();
    let later_bag = f.base.join("later-ordinary-native-package");
    crate::records_export::export(&f.root, &later_bag).unwrap();
    Fixture::choose(&f.destination);
    let later = super::super::prepare(&f.root, &later_bag, &actor(), &observed()).unwrap();
    assert!(!later.intent.copied.contains_key(relative));
    assert!(!later
        .intent
        .copied
        .contains_key(&lost.intent.receipt_relative()));
    super::super::apply(later, &actor(), &observed()).unwrap();
    let original = identity::original_context(&lost.intent, &lost.bytes).unwrap();
    std::fs::remove_file(PathBuf::from(original["path"].as_str().unwrap())).unwrap();
    std::fs::remove_file(lost.intent.completion_path().unwrap()).unwrap();
    assert!(f.dir().join(lost.intent.receipt_relative()).is_file());
    f.cold();
    let quoted = quoted_prefix(&f.dir(), relative, &fleet_bytes);
    assert!(quoted.is_err(), "a retained local receipt cannot be mistaken for copied foreign evidence after its actual native intent disappears: {quoted:?}");
    assert!(require_complete(&f.dir()).is_err());
    assert!(prepare(&f.root, None, &actor(), &observed()).is_err());
}

#[test]
fn copied_foreign_origin_receipt_reads_only_under_exact_surviving_local_copy_proof() {
    let f = Fixture::new(false);
    f.import();
    let foreign = f.row();
    let exported = f.base.join("package-with-foreign-origin-receipt");
    crate::records_export::export(&f.root, &exported).unwrap();
    let third = f.base.join("third-store");
    Fixture::choose(&third);
    let local = super::super::prepare(&f.root, &exported, &actor(), &observed()).unwrap();
    let relative = foreign.intent.receipt_relative();
    assert!(local.intent.copied.contains_key(&relative));
    super::super::apply(local, &actor(), &observed()).unwrap();
    let dir = project_dir(&third, &f.project);
    SEEN.lock().unwrap().remove(&dir);
    ORIGINALS.lock().unwrap().remove(&dir);
    UNCERTAIN.lock().unwrap().remove(&dir);
    assert_eq!(
        entries(&dir).unwrap().len(),
        1,
        "foreign receipt grants no local intent authority"
    );
    assert!(require_complete(&dir).is_ok());
    assert!(home(&f.root).is_ok());
    let path = dir.join(relative);
    let original = std::fs::read(&path).unwrap();
    std::fs::write(&path, b"unequal copied foreign receipt fixture").unwrap();
    assert!(
        require_complete(&dir).is_err(),
        "copy proof must bind exact receipt bytes"
    );
    std::fs::write(path, original).unwrap();
    assert!(require_complete(&dir).is_ok());
}

#[test]
fn later_roots_witness_requires_its_actual_native_intent_and_exact_completion() {
    for damage in ["missing original", "unequal original", "unequal completion"] {
        let f = Fixture::new(true);
        let (first, later) = completed_identity_roundtrip(&f);
        lose_prior_derivatives(&f, &first);
        let original = identity::original_context(&later.intent, &later.bytes).unwrap();
        let original = PathBuf::from(original["path"].as_str().unwrap());
        match damage {
            "missing original" => std::fs::remove_file(&original).unwrap(),
            "unequal original" => {
                let mut changed = bag::parse_json_unique(&later.bytes).unwrap();
                changed["at"] = json!("unequal surviving native intent fixture");
                std::fs::write(&original, json_bytes(&changed).unwrap()).unwrap();
            }
            "unequal completion" => {
                let path = later.intent.completion_path().unwrap();
                let mut changed = completion(&later.intent, &later.bytes);
                changed["intentSha256"] = json!("0".repeat(64));
                std::fs::write(path, json_bytes(&changed).unwrap()).unwrap();
            }
            _ => unreachable!(),
        }
        f.cold();
        assert!(entries(&f.dir()).is_err(), "{damage}");
        assert!(
            prepare(&f.root, None, &actor(), &observed()).is_err(),
            "{damage}"
        );
        assert!(!first.intent.path().unwrap().exists(), "{damage}");
        assert!(
            !f.dir().join(first.intent.receipt_relative()).exists(),
            "{damage}"
        );
    }
}

#[test]
fn missing_later_completion_cannot_witness_prior_repair_before_its_own_native_recovery() {
    let f = Fixture::new(true);
    let (first, later) = completed_identity_roundtrip(&f);
    lose_prior_derivatives(&f, &first);
    std::fs::remove_file(later.intent.completion_path().unwrap()).unwrap();
    f.cold();
    let rows = entries(&f.dir()).unwrap();
    let derived = derivative_members(&rows).unwrap();
    assert!(complete_context(&first.intent, &derived, &rows).is_err());
    let plan = prepare(&f.root, None, &actor(), &observed()).unwrap();
    assert_eq!(plan.work.len(), 1);
    assert_eq!(plan.work[0].entry.intent.id, later.intent.id);
    assert!(matches!(plan.work[0].kind, WorkKind::Controls));
    assert_eq!(plan.deferred, vec![first.intent.id.clone()]);
    apply(plan, &actor(), &observed()).unwrap();
    assert!(!first.intent.path().unwrap().exists());
    assert!(!f.dir().join(first.intent.receipt_relative()).exists());
    assert!(require_complete(&f.dir()).is_err());
    f.recover(None);
    assert!(require_complete(&f.dir()).is_ok());
}

#[test]
fn completed_later_witness_refuses_a_current_unrelated_link_or_unanchored_related_roots_tail() {
    for damage in ["unrelated link", "related tail"] {
        let f = Fixture::new(true);
        let (first, _) = completed_identity_roundtrip(&f);
        lose_prior_derivatives(&f, &first);
        match damage {
            "unrelated link" => {
                let path = f.root.join(PROJECT_LINK);
                let mut link = bag::parse_json_unique(&plain(&path).unwrap()).unwrap();
                link["projectId"] = json!("invented-unrelated-project");
                std::fs::write(path, json_bytes(&link).unwrap()).unwrap();
            }
            "related tail" => {
                use std::io::Write;
                let row = json!({"format":ROOT_FORMAT,"formatVersion":VERSION,
                    "projectId":f.project,"root":f.root,"how":"registered"});
                let mut file = std::fs::OpenOptions::new()
                    .append(true)
                    .open(f.destination.join("roots.jsonl"))
                    .unwrap();
                writeln!(file, "{row}").unwrap();
            }
            _ => unreachable!(),
        }
        let roots = std::fs::read(f.destination.join("roots.jsonl")).unwrap();
        let link = std::fs::read(f.root.join(PROJECT_LINK)).unwrap();
        let payload = bag::payload_inventory(&f.dir()).unwrap();
        let rows = entries(&f.dir()).unwrap();
        assert!(
            complete_context(&first.intent, &derivative_members(&rows).unwrap(), &rows).is_err(),
            "{damage}"
        );
        assert!(
            prepare(&f.root, None, &actor(), &observed()).is_err(),
            "{damage}"
        );
        assert_eq!(
            std::fs::read(f.destination.join("roots.jsonl")).unwrap(),
            roots
        );
        assert_eq!(std::fs::read(f.root.join(PROJECT_LINK)).unwrap(), link);
        assert_eq!(bag::payload_inventory(&f.dir()).unwrap(), payload);
    }
}

#[test]
fn changed_completed_later_witness_custody_during_native_question_refuses_prior_repair() {
    for replace in ["original", "completion"] {
        let f = Fixture::new(true);
        let (first, later) = completed_identity_roundtrip(&f);
        lose_prior_derivatives(&f, &first);
        let plan = prepare(&f.root, None, &actor(), &observed()).unwrap();
        assert_eq!(
            plan.work[0].context["rootsWitness"]["importId"],
            later.intent.id
        );
        let path = match replace {
            "original" => {
                let original = identity::original_context(&later.intent, &later.bytes).unwrap();
                PathBuf::from(original["path"].as_str().unwrap())
            }
            "completion" => later.intent.completion_path().unwrap(),
            _ => unreachable!(),
        };
        let bytes = std::fs::read(&path).unwrap();
        std::fs::rename(&path, f.base.join("witness-before-identical-replacement")).unwrap();
        std::fs::write(&path, &bytes).unwrap();
        let error = apply(plan, &actor(), &observed()).unwrap_err();
        assert!(error.contains("changed"), "{replace}: {error}");
        assert!(!first.intent.path().unwrap().exists(), "{replace}");
        assert!(
            !f.dir().join(first.intent.receipt_relative()).exists(),
            "{replace}"
        );
        assert!(require_complete(&f.dir()).is_err());
    }
}
