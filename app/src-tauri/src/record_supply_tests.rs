use super::*;

fn fixture() -> (Value, Value, Value) {
    let content = json!({"method":"fixture.text/v1", "value":"same-characters"});
    let run = json!({"record_kind":"run_text","run":"run:A","conversation":"thread:A","purpose":"run start","workflow":{"kind":"workflow","origin":"project","source_root":"project:A","name":"sample","revision":"rev:A","revision_method":"fixture.revision/v1"},"text_identity":content,"workflow_file":{"content":content}});
    let check = json!({"record_kind":"supply_check","check":"check:A","run":"run:A","conversation":"thread:A","purpose":"run start","turn":"opaque-native:A","expected_text":content,"observed_text":content,"state":"verified","item":"item:A","located_by":"client id","client_user_message_id":"client:A","read_at":"time:A","evidence_limits":["fixture only"]});
    let envelope = json!({"basis_records":["wr-record:v1:11111111-1111-4111-8111-111111111111"]});
    (run, check, envelope)
}
const RUN_REF: &str = "wr-record:v1:11111111-1111-4111-8111-111111111111";
const CHECK_REF: &str = "wr-record:v1:22222222-2222-4222-8222-222222222222";
fn build(
    run: &Value,
    check: &Value,
    envelope: &Value,
) -> Result<HistoricalSupply, CorrespondenceError> {
    correspond_bodies(RUN_REF, run, CHECK_REF, check, envelope, None)
}
#[test]
fn six_states_are_preserved_with_unknown_adoption_and_history_limit() {
    for state in [
        "verified",
        "text differs, workflow bytes equal",
        "text differs, workflow bytes differ",
        "incomparable",
        "not found",
        "unreadable",
    ] {
        let (run, mut check, envelope) = fixture();
        check["state"] = state.into();
        if state == "incomparable" {
            check["observed_text"]["method"] = "other.text/v1".into();
        }
        let supplied = build(&run, &check, &envelope).unwrap();
        assert_eq!(supplied.recorded_claim()["supplyCheck"], state);
        assert_eq!(supplied.recorded_claim()["adoption"], "unknown");
        assert_eq!(supplied.recorded_claim()["nativeTurn"], "opaque-native:A");
        assert!(supplied.recorded_claim().get("turn").is_none());
        assert_eq!(supplied.limits()[0], "fixture only");
        assert!(supplied
            .limits()
            .iter()
            .any(|s| s.contains("no live native witness")));
    }
}
#[test]
fn exact_start_identity_is_not_shortened_or_reinterpreted() {
    let (mut run, check, envelope) = fixture();
    run["workflow"]["source_root"] = "root:with:delimiters/and space".into();
    let supplied = build(&run, &check, &envelope).unwrap();
    let tuple: Value = serde_json::from_str(
        supplied.recorded_claim()["sourceIdentity"]
            .as_str()
            .unwrap(),
    )
    .unwrap();
    assert_eq!(tuple, run["workflow"]);
    assert_eq!(supplied.recorded_claim()["content"], run["text_identity"]);
}
#[test]
fn a_missing_turn_never_falls_back_to_client_id_or_number() {
    let (run, mut check, envelope) = fixture();
    check.as_object_mut().unwrap().remove("turn");
    for state in ["not found", "unreadable"] {
        check["state"] = state.into();
        assert_eq!(
            build(&run, &check, &envelope).unwrap_err(),
            CorrespondenceError::MissingNativeTurn
        );
    }
}
#[test]
fn resolved_claim_joins_reject_wrong_scope_basis_and_content() {
    for field in ["run", "conversation", "purpose"] {
        let (run, mut check, envelope) = fixture();
        check[field] = "different".into();
        assert!(build(&run, &check, &envelope).is_err(), "{field}");
    }
    let (run, check, mut envelope) = fixture();
    envelope["basis_records"] = json!([CHECK_REF]);
    assert!(build(&run, &check, &envelope).is_err());
    for field in ["method", "value"] {
        let (run, mut check, envelope) = fixture();
        check["expected_text"][field] = "different".into();
        assert!(build(&run, &check, &envelope).is_err(), "{field}");
    }
}
#[test]
fn equal_value_under_different_method_is_not_verified() {
    let (run, mut check, envelope) = fixture();
    check["observed_text"]["method"] = "other.text/v1".into();
    assert!(build(&run, &check, &envelope).is_err());
    check["state"] = "incomparable".into();
    assert_eq!(
        build(&run, &check, &envelope).unwrap().recorded_claim()["supplyCheck"],
        "incomparable"
    );
}
#[test]
fn full_reviewed_native_fixture_and_exclusive_coordinate_negatives_validate() {
    let valid: Value = serde_json::from_str(include_str!(
        "../schemas/fixtures/native-supply.example.jsonl"
    ))
    .unwrap();
    let validator = crate::schema_validation::bundled().unwrap();
    validator.validate(&valid).unwrap();
    let invalid: Value = serde_json::from_str(include_str!(
        "../schemas/fixtures/native-supply.invalid.json"
    ))
    .unwrap();
    for case in invalid.as_array().unwrap() {
        assert!(
            validator.validate(&case["record"]).is_err(),
            "{}",
            case["reason"]
        );
    }
    let mut ordinal = valid;
    ordinal["body"]
        .as_object_mut()
        .unwrap()
        .remove("nativeTurn");
    ordinal["body"]["turn"] = 6.into();
    validator.validate(&ordinal).unwrap();
}

struct ColdEndFixture {
    root: std::path::PathBuf,
    start: Value,
    end: Value,
    prepared: crate::workflow_workspace::PreparedRunText,
    owner_end: crate::workflow_workspace::OwnerRunEnd,
}
const SELECTION_REF: &str = "wr-record:v1:33333333-3333-4333-8333-333333333333";
const END_REF: &str = "wr-record:v1:44444444-4444-4444-8444-444444444444";
impl Drop for ColdEndFixture {
    fn drop(&mut self) {
        let _ = std::fs::remove_dir_all(&self.root);
    }
}
impl ColdEndFixture {
    fn file(&self, reference: &str) -> std::path::PathBuf {
        self.root.join(".chirality/records/workflow").join(format!(
            "{}.json",
            reference.strip_prefix("wr-record:v1:").unwrap()
        ))
    }
    // Explicitly historical fixture bytes. This does not create any live token.
    fn write(&self, reference: &str, body: Value, basis: Vec<&str>) {
        let path = self.file(reference);
        std::fs::create_dir_all(path.parent().unwrap()).unwrap();
        std::fs::write(path, serde_json::to_vec(&json!({"version":1,"record_id":reference,"writer":"fixture-only","observed_at":"fixture-time","body":body,"basis_records":basis,"source_references":[]})).unwrap()).unwrap();
    }
    fn new() -> Self {
        use crate::workflow_workspace::{
            OwnerRunEnd, PreparedRunText, RunEndReason, RunScope, Selection, Snapshot,
        };
        let root = std::env::temp_dir().join(crate::util::opaque_id("rs-real-end-").unwrap());
        std::fs::create_dir(&root).unwrap();
        let root = std::fs::canonicalize(root).unwrap();
        let snapshot = Snapshot::from_files(std::collections::BTreeMap::from([(
            "WORKFLOW.md".into(),
            b"---\nname: sample\n---\n# Real end producer fixture\n".to_vec(),
        )]))
        .unwrap();
        let identity = snapshot
            .identity("bundled", "fixture-release", "sample", None)
            .unwrap();
        let selection = Selection::synthetic_shipped(snapshot, identity.clone()).unwrap();
        let revision_store = root.join("revision");
        selection.snapshot().publish_new(&revision_store).unwrap();
        let prepared = PreparedRunText::start(
            &selection,
            RunScope {
                run: "run:A".into(),
                conversation: "thread:A".into(),
                home: "home:A".into(),
                generation: json!({"appSession":"fixture","home":"home:A","spawnCounter":1}),
                source_root: "fixture-release".into(),
                holding_library: "fixture-release".into(),
                selection_ref: "selection:A".into(),
                revision_store,
            },
            "revision",
            None,
        )
        .unwrap();
        let owner_end = OwnerRunEnd {
            home: "home:A".into(),
            conversation: "thread:A".into(),
            run: "run:A".into(),
            workflow: identity,
            reason: RunEndReason::Completed,
        };
        let (_, end) = prepared.end_notice(&owner_end).unwrap();
        let f = Self {
            root,
            start: prepared.record().clone(),
            end,
            prepared,
            owner_end,
        };
        let selection_body = json!({"record_kind":"selection_record","selection_id":"selection:A","identity":selection.identity(),"holding_library":"fixture-release","standing":"bundled","selected_by":"the person (App interface)","how":"explicit","conversation":"thread:A","selected_at":"fixture-time"});
        // 'bundled' is this cold fixture's historical claim, never actual release
        // admission; synthetic_shipped remains the actual producer.
        f.write(SELECTION_REF, selection_body, vec![]);
        f.write(RUN_REF, f.start.clone(), vec![SELECTION_REF]);
        f.write(END_REF, f.end.clone(), vec![RUN_REF]);
        let check = json!({"record_kind":"supply_check","check":"fixture-end-check","run":"run:A","conversation":"thread:A","turn":"opaque-native:end","purpose":"run end notice","expected_text":f.end["text_identity"],"observed_text":f.end["text_identity"],"state":"verified","read_at":"fixture-time","item":"fixture-item","located_by":"client id","client_user_message_id":"fixture-client","evidence_limits":["historical fixture only, no native observation"]});
        f.write(CHECK_REF, check, vec![END_REF]);
        f
    }
    fn entry(&self, body: &Value) -> Value {
        let mut entry: Value = serde_json::from_str(include_str!(
            "../schemas/fixtures/native-supply.example.jsonl"
        ))
        .unwrap();
        entry["runId"] = "run:A".into();
        entry["body"] = body.clone();
        entry
    }
}
#[test]
fn actual_end_notice_resolves_original_source_and_preserves_end_content() {
    let f = ColdEndFixture::new();
    assert!(f.end.get("workflow").is_none());
    assert!(f.end.get("workflow_file").is_none());
    let project = ProjectRecords::open(&f.root).unwrap();
    let end = project.resolve(END_REF).unwrap(); // full WR body/envelope/basis validation
    let check = project.resolve(CHECK_REF).unwrap();
    let supplied = correspond(&project, &end, &check).unwrap();
    assert_eq!(supplied.recorded_claim()["content"], f.end["text_identity"]);
    assert_ne!(
        supplied.recorded_claim()["content"],
        f.start["text_identity"]
    );
    let source: Value = serde_json::from_str(
        supplied.recorded_claim()["sourceIdentity"]
            .as_str()
            .unwrap(),
    )
    .unwrap();
    assert_eq!(source, f.start["workflow"]);
    let entry = f.entry(supplied.recorded_claim());
    crate::schema_validation::bundled()
        .unwrap()
        .validate(&entry)
        .unwrap();
    assert_eq!(
        read_correspondence(&project, &entry).standing,
        ReadStanding::HistoricalCorrespondence
    );
    let reopened = ProjectRecords::open(&f.root).unwrap();
    assert_eq!(
        read_correspondence(&reopened, &entry).standing,
        ReadStanding::HistoricalCorrespondence
    );
    std::fs::remove_file(f.file(RUN_REF)).unwrap();
    assert_eq!(
        read_correspondence(&reopened, &entry).standing,
        ReadStanding::Limited
    );
    // Cached resolved objects do not bypass a disappeared owning source.
    assert!(correspond(&reopened, &end, &check).is_err());
}
#[test]
fn end_notice_rejects_wrong_original_scope_missing_link_and_cross_project() {
    for field in ["run", "conversation"] {
        let f = ColdEndFixture::new();
        let mut wrong = f.start.clone();
        wrong[field] = "wrong".into();
        f.write(RUN_REF, wrong, vec![SELECTION_REF]);
        assert!(ProjectRecords::open(&f.root)
            .unwrap()
            .resolve(END_REF)
            .is_err());
    }
    let f = ColdEndFixture::new();
    f.write(END_REF, f.end.clone(), vec![]);
    assert!(ProjectRecords::open(&f.root)
        .unwrap()
        .resolve(END_REF)
        .is_err());
    let a = ColdEndFixture::new();
    let b = ColdEndFixture::new();
    let pa = ProjectRecords::open(&a.root).unwrap();
    let pb = ProjectRecords::open(&b.root).unwrap();
    assert!(correspond(
        &pa,
        &pa.resolve(END_REF).unwrap(),
        &pb.resolve(CHECK_REF).unwrap()
    )
    .is_err());
    let end = pa.resolve(END_REF).unwrap();
    let check = pa.resolve(CHECK_REF).unwrap();
    assert!(correspond(&pb, &end, &check).is_err());
}

#[test]
fn actual_end_publisher_resolves_source_and_cold_reads() {
    use crate::workflow_workspace::publication::PreparedEndPublication;
    let f = ColdEndFixture::new();
    let project = ProjectRecords::open(&f.root).unwrap();
    let start = project.resolve(RUN_REF).unwrap();
    let pending = PreparedEndPublication::new(
        &project,
        &f.prepared,
        &f.owner_end,
        &start,
        "fixture-only",
        "fixture-time",
    )
    .unwrap();
    let published = pending.publish(&project).unwrap();
    let published_ref = published.run_text_record().reference().to_owned();
    assert_eq!(published.run_text_record().body(), &f.end);
    let mut check = project.resolve(CHECK_REF).unwrap().body().clone();
    check["check"] = "fixture-published-end-check".into();
    f.write(CHECK_REF, check, vec![&published_ref]);
    let end = project.resolve(&published_ref).unwrap();
    let check = project.resolve(CHECK_REF).unwrap();
    let repaired = correspond(&project, &end, &check).unwrap();
    assert_eq!(repaired.recorded_claim()["content"], f.end["text_identity"]);
    let entry = f.entry(repaired.recorded_claim());
    crate::schema_validation::bundled()
        .unwrap()
        .validate(&entry)
        .unwrap();
    drop(project);
    let reopened = ProjectRecords::open(&f.root).unwrap();
    assert_eq!(
        read_correspondence(&reopened, &entry).standing,
        ReadStanding::HistoricalCorrespondence
    );
}

#[test]
fn actual_start_cold_reader_rejects_rs_turn_purpose_method_and_state_drift() {
    let f = ColdEndFixture::new();
    let project = ProjectRecords::open(&f.root).unwrap();
    let mut check = project.resolve(CHECK_REF).unwrap().body().clone();
    check["purpose"] = "run start".into();
    check["expected_text"] = f.start["text_identity"].clone();
    check["observed_text"] = f.start["text_identity"].clone();
    check["expected_workflow"] = f.start["workflow_file"]["content"].clone();
    f.write(CHECK_REF, check, vec![RUN_REF]);
    let start = project.resolve(RUN_REF).unwrap();
    let check = project.resolve(CHECK_REF).unwrap();
    let supplied = correspond(&project, &start, &check).unwrap();
    let entry = f.entry(supplied.recorded_claim());
    let reopened = ProjectRecords::open(&f.root).unwrap();
    assert_eq!(
        read_correspondence(&reopened, &entry).standing,
        ReadStanding::HistoricalCorrespondence
    );
    for (field, wrong) in [
        ("nativeTurn", "other-native"),
        ("thread", "other-thread"),
        ("supplyForm", "workflow run end notice (turn text)"),
        ("supplyCheck", "incomparable"),
        ("sourceIdentity", "other-source"),
    ] {
        let mut changed = entry.clone();
        changed["body"][field] = wrong.into();
        assert_eq!(
            read_correspondence(&reopened, &changed).standing,
            ReadStanding::Limited,
            "{field}"
        );
    }
    let mut changed = entry.clone();
    changed["body"]["content"]["method"] = "other-method".into();
    assert_eq!(
        read_correspondence(&reopened, &changed).standing,
        ReadStanding::Limited
    );
    let mut changed = entry.clone();
    changed["runId"] = "other-run".into();
    assert_eq!(
        read_correspondence(&reopened, &changed).standing,
        ReadStanding::Limited
    );
    std::fs::write(f.file(CHECK_REF), b"corrupt").unwrap();
    assert_eq!(
        read_correspondence(&reopened, &entry).standing,
        ReadStanding::Limited
    );
}
