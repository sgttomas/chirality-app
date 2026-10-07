use super::*;
struct Fixture(PathBuf);
impl Fixture {
    fn new() -> Self {
        let p = std::fs::canonicalize(std::env::temp_dir())
            .unwrap()
            .join(crate::util::opaque_id("wr-store-").unwrap());
        std::fs::create_dir(&p).unwrap();
        Self(p)
    }
    fn store(&self) -> ProjectRecords {
        ProjectRecords::open(&self.0).unwrap()
    }
}
impl Drop for Fixture {
    fn drop(&mut self) {
        let _ = std::fs::remove_dir_all(&self.0);
    }
}
fn selection() -> Value {
    json!({"record_kind":"selection_record","selection_id":"selection-A","identity":{"kind":"workflow","origin":"project","source_root":"fixture","name":"sample","revision":"a".repeat(64),"revision_method":"fixture"},"holding_library":"fixture","standing":"registered","selected_by":"the person (App interface)","how":"explicit","conversation":"thread-A","selected_at":"original"})
}
fn pending(p: &ProjectRecords) -> PendingRecord {
    PendingRecord::new(p, selection(), vec![], vec![], "writer", "original").unwrap()
}
#[test]
fn immutable_reopen_retry_collision_and_wrong_project() {
    let f = Fixture::new();
    let p = f.store();
    let a = pending(&p);
    let reference = a.reference().to_owned();
    let first = p.publish(&a).unwrap();
    let second = p.publish(&a).unwrap();
    assert_eq!(first.bytes(), second.bytes());
    let reopened = f.store().resolve(&reference).unwrap();
    assert_eq!(first.bytes(), reopened.bytes());
    let other = Fixture::new();
    assert!(other.store().publish(&a).is_err());
    let mut collision = pending(&p);
    collision.envelope["record_id"] = reference.clone().into();
    collision.envelope["writer"] = "different".into();
    collision.bytes = serde_json::to_vec(&collision.envelope).unwrap();
    assert!(p.publish(&collision).is_err());
    assert_eq!(p.resolve(&reference).unwrap().bytes(), first.bytes());
}
#[test]
fn unknown_project_and_symlink_escape_refused() {
    assert!(ProjectRecords::open(Path::new("relative")).is_err());
    let f = Fixture::new();
    let outside = Fixture::new();
    std::os::unix::fs::symlink(&outside.0, f.0.join(".chirality")).unwrap();
    let p = f.store();
    assert!(p.publish(&pending(&p)).is_err());
    assert!(!outside.0.join("records").exists());
}
#[test]
fn invalid_partial_unsupported_and_escaping_reference_refused() {
    let f = Fixture::new();
    let p = f.store();
    let a = pending(&p);
    p.publish(&a).unwrap();
    assert!(matches!(
        p.resolve("wr-record:v1:../../escape"),
        Err(ResolutionError::Invalid(_))
    ));
    let path =
        f.0.join(".chirality/records/workflow")
            .join(format!("{}.json", key(a.reference()).unwrap()));
    std::fs::write(&path, b"{").unwrap();
    assert!(matches!(
        p.resolve(a.reference()),
        Err(ResolutionError::Invalid(_))
    ));
    let mut future = a.envelope.clone();
    future["version"] = 2.into();
    std::fs::write(&path, serde_json::to_vec(&future).unwrap()).unwrap();
    assert!(matches!(
        p.resolve(a.reference()),
        Err(ResolutionError::Unsupported)
    ));
}
#[test]
fn forbidden_native_payload_rejected_and_original_time_retained() {
    let f = Fixture::new();
    let p = f.store();
    let a = pending(&p);
    let mut e = a.envelope.clone();
    e["native_transcript"] = "not permitted".into();
    assert!(validate(&e).is_err());
    assert_eq!(p.publish(&a).unwrap().envelope()["observed_at"], "original");
}
#[test]
fn uncertain_link_is_same_original_retry_not_a_new_observation() {
    let f = Fixture::new();
    let p = f.store();
    let a = pending(&p);
    FAIL_AFTER_LINK.with(|v| v.set(true));
    assert!(p.publish(&a).is_err());
    let resumed = p.publish(&a).unwrap();
    assert_eq!(resumed.reference(), a.reference());
    assert_eq!(resumed.bytes(), a.bytes);
}
fn end_text() -> Value {
    let text="[Chirality] Workflow run ended: sample revision aaaaaaaaaaaa (run run-A, ended by the person). No workflow is in force.";
    json!({"record_kind":"run_text","purpose":"run end notice","framing":"WR-FRAME-1","run":"run-A","conversation":"thread-A","lines":{"end_line":text},"text_identity":crate::role_supply::content(text.as_bytes()),"text_bytes":text.len()})
}
#[test]
fn check_rereads_new_identity_retry_retains_identity_and_wrong_correspondence_refused() {
    let f = Fixture::new();
    let p = f.store();
    let rt = PendingRecord::new(&p, end_text(), vec![], vec![], "writer", "prepared-time").unwrap();
    assert!(p.publish(&rt).is_err()); // Original zero-basis end notice is no longer resolvable.
    let (prepared, start) = original_start(&f, &p);
    let end = crate::workflow_workspace::OwnerRunEnd {
        home: "home".into(),
        conversation: "thread-A".into(),
        run: "run-A".into(),
        workflow: prepared.workflow.clone(),
        reason: crate::workflow_workspace::RunEndReason::ByPerson,
    };
    let notice = PreparedEndPublication::new(
        &p,
        &prepared,
        &end,
        start.run_text_record(),
        "writer",
        "ended",
    )
    .unwrap()
    .publish(&p)
    .unwrap();
    let rt = p.resolve(notice.run_text_record().reference()).unwrap();
    assert!(rt.body().get("workflow").is_none());
    assert!(rt.body().get("workflow_file").is_none());
    let body = json!({"record_kind":"supply_check","check":"check-A","run":"run-A","conversation":"thread-A","purpose":"run end notice","turn":"opaque-native-turn","expected_text":rt.body()["text_identity"],"state":"not found","read_at":"read-time","evidence_limits":[]});
    // Test-only construction; no production constructor or JSON deserializer.
    let a = PendingRecord::supply_check(
        &p,
        CompletedSupplyCheck {
            body: body.clone(),
            sources: vec!["actual-receipt-reference".into()],
        },
        &rt,
        "writer",
    )
    .unwrap();
    let one = p.publish(&a).unwrap();
    assert_eq!(p.publish(&a).unwrap().reference(), one.reference());
    let mut next = body.clone();
    next["check"] = "check-B".into();
    let b = PendingRecord::supply_check(
        &p,
        CompletedSupplyCheck {
            body: next,
            sources: vec![],
        },
        &rt,
        "writer",
    )
    .unwrap();
    assert_ne!(p.publish(&b).unwrap().reference(), one.reference());
    let mut wrong = body;
    wrong["conversation"] = "other-thread".into();
    let c = PendingRecord::supply_check(
        &p,
        CompletedSupplyCheck {
            body: wrong,
            sources: vec![],
        },
        &rt,
        "writer",
    )
    .unwrap();
    assert!(p.publish(&c).is_err());
}
#[test]
fn typed_publication_retains_prepared_text_and_refuses_lost_source_or_development() {
    use crate::workflow_workspace::{
        OwnerRunEnd, PreparedRunText, RegisteredRevision, RunEndReason, RunScope, Snapshot,
    };
    let f = Fixture::new();
    let p = f.store();
    let snapshot = Snapshot::from_files(std::collections::BTreeMap::from([(
        "WORKFLOW.md".into(),
        b"---\nname: sample\n---\n# Exact\n".to_vec(),
    )]))
    .unwrap();
    let identity = snapshot
        .identity("project", "fixture", "sample", None)
        .unwrap();
    let store = f.0.join("revision");
    snapshot.publish_new(&store).unwrap();
    // Test fixture only: production RegisteredRevision still comes from its owner.
    let registered = RegisteredRevision {
        identity: identity.clone(),
        snapshot,
        act_ref: "test-native-owner".into(),
    };
    let selection = registered.select();
    let scope = RunScope {
        run: "run-A".into(),
        conversation: "thread-A".into(),
        home: "home".into(),
        generation: json!({"home":"home","appSession":"session","spawnCounter":1}),
        source_root: "fixture".into(),
        holding_library: "fixture".into(),
        selection_ref: "selection-A".into(),
        revision_store: store.clone(),
    };
    let prepared = PreparedRunText::start(&selection, scope, "revision", None).unwrap();
    let expected = prepared.text().to_owned();
    let publication = PreparedRunPublication::new(
        &p,
        &selection,
        prepared.clone(),
        "writer",
        "selected",
        "prepared",
    )
    .unwrap();
    let published = publication.publish(&p).unwrap();
    assert_eq!(published.prepared().text(), expected);
    assert_eq!(
        published.run_text_record().body()["text_identity"],
        crate::role_supply::content(expected.as_bytes())
    );
    let end = OwnerRunEnd {
        home: "home".into(),
        conversation: "thread-A".into(),
        run: "run-A".into(),
        workflow: identity,
        reason: RunEndReason::ByPerson,
    };
    let notice = PreparedEndPublication::new(
        &p,
        &prepared,
        &end,
        published.run_text_record(),
        "writer",
        "ended",
    )
    .unwrap()
    .publish(&p)
    .unwrap();
    assert_eq!(notice.run_text_record().body()["purpose"], "run end notice");
    assert!(notice.text().contains("No workflow is in force."));
    std::fs::remove_dir_all(store).unwrap();
    assert!(publication.publish(&p).is_err());
    let mut development = selection.clone();
    development.admission = SelectionAdmission::DevelopmentCatalog {
        source_map_sha256: "test".into(),
        tranche: "test".into(),
    };
    assert!(PreparedRunPublication::new(
        &p,
        &development,
        prepared,
        "writer",
        "selected",
        "prepared"
    )
    .is_err());
}
fn original_start(f: &Fixture, p: &ProjectRecords) -> (PreparedRunText, PublishedRunText) {
    use crate::workflow_workspace::{RegisteredRevision, RunScope, Snapshot};
    let snapshot = Snapshot::from_files(std::collections::BTreeMap::from([(
        "WORKFLOW.md".into(),
        b"---\nname: sample\n---\n# Exact\n".to_vec(),
    )]))
    .unwrap();
    let identity = snapshot
        .identity("project", "fixture", "sample", None)
        .unwrap();
    let store = f.0.join(crate::util::opaque_id("revision-").unwrap());
    snapshot.publish_new(&store).unwrap();
    let selection = RegisteredRevision {
        identity,
        snapshot,
        act_ref: "test-owner".into(),
    }
    .select();
    let scope = RunScope {
        run: "run-A".into(),
        conversation: "thread-A".into(),
        home: "home".into(),
        generation: json!({"home":"home","appSession":"session","spawnCounter":1}),
        source_root: "fixture".into(),
        holding_library: "fixture".into(),
        selection_ref: crate::util::opaque_id("selection-").unwrap(),
        revision_store: store,
    };
    let prepared = PreparedRunText::start(&selection, scope, "revision", None).unwrap();
    let published = PreparedRunPublication::new(
        p,
        &selection,
        prepared.clone(),
        "writer",
        "selected",
        "prepared",
    )
    .unwrap()
    .publish(p)
    .unwrap();
    (prepared, published)
}
#[test]
fn actual_end_notice_requires_original_start_and_preserves_optional_workflow_comparison() {
    let f = Fixture::new();
    let p = f.store();
    let (prepared, start) = original_start(&f, &p);
    let end = crate::workflow_workspace::OwnerRunEnd {
        home: "home".into(),
        conversation: "thread-A".into(),
        run: "run-A".into(),
        workflow: prepared.workflow.clone(),
        reason: crate::workflow_workspace::RunEndReason::ByPerson,
    };
    let (_, actual) = prepared.end_notice(&end).unwrap();
    assert!(actual.get("workflow").is_none());
    assert!(actual.get("workflow_file").is_none());
    super::super::wr_validate("run_text", &actual).unwrap();
    let notice = PreparedEndPublication::new(
        &p,
        &prepared,
        &end,
        start.run_text_record(),
        "writer",
        "ended",
    )
    .unwrap()
    .publish(&p)
    .unwrap();
    assert_eq!(notice.run_text_record().body(), &actual);
    let reopened = f
        .store()
        .resolve(notice.run_text_record().reference())
        .unwrap();
    assert_eq!(
        reopened.envelope()["basis_records"],
        json!([start.run_text_record().reference()])
    );
    let missing =
        PendingRecord::new(&p, actual.clone(), vec![], vec![], "writer", "ended").unwrap();
    assert!(p.publish(&missing).is_err());
    let mut wrong = actual.clone();
    wrong["run"] = "wrong-run".into();
    let wrong = PendingRecord::new(
        &p,
        wrong,
        vec![start.run_text_record().reference().into()],
        vec![],
        "writer",
        "ended",
    )
    .unwrap();
    assert!(p.publish(&wrong).is_err());
    let mut wrong = actual.clone();
    wrong["conversation"] = "wrong-thread".into();
    let wrong = PendingRecord::new(
        &p,
        wrong,
        vec![start.run_text_record().reference().into()],
        vec![],
        "writer",
        "ended",
    )
    .unwrap();
    assert!(p.publish(&wrong).is_err());
    let other = Fixture::new();
    assert!(PreparedEndPublication::new(
        &other.store(),
        &prepared,
        &end,
        start.run_text_record(),
        "writer",
        "ended"
    )
    .is_err());
    let body = json!({"record_kind":"supply_check","check":"check-start","run":"run-A","conversation":"thread-A","purpose":"run start","turn":"opaque-turn","expected_text":start.run_text_record().body()["text_identity"],"expected_workflow":{"method":"wrong-method","value":start.run_text_record().body()["workflow_file"]["content"]["value"]},"state":"not found","read_at":"read-time","evidence_limits":[]});
    let bad = PendingRecord::supply_check(
        &p,
        CompletedSupplyCheck {
            body,
            sources: vec![],
        },
        start.run_text_record(),
        "writer",
    )
    .unwrap();
    assert!(p.publish(&bad).is_err());
    let start_path = f.0.join(".chirality/records/workflow").join(format!(
        "{}.json",
        key(start.run_text_record().reference()).unwrap()
    ));
    std::fs::remove_file(start_path).unwrap();
    assert!(f.store().resolve(reopened.reference()).is_err());
}
fn located(item: Option<&str>, by_client: bool, text: &str) -> Observation<'static> {
    Observation::Located(crate::workflow_workspace::LocatedTurnText::Text {
        item: item.map(String::from),
        by_client,
        text: text.into(),
    })
}
fn map(run_text: &Value, prepared: &PreparedRunText, o: Observation<'_>) -> Value {
    supply_check_body(run_text, prepared, o, "turn-A", "client-A", "check-A", "read-A").unwrap()
}
// WR §16.4: every state from one pure mapping; all bodies validate as WR supply_check.
#[test]
fn live_mapping_covers_every_wr_state_including_incomparable() {
    let f = Fixture::new();
    let p = f.store();
    let (prepared, published) = original_start(&f, &p);
    let rt = published.run_text_record().body().clone();
    let text = prepared.text().to_owned();
    let v = map(&rt, &prepared, located(Some("item-A"), true, &text));
    assert_eq!(v["state"], "verified");
    assert_eq!(v["located_by"], "client id");
    assert_eq!(v["observed_text"], rt["text_identity"]);
    assert_eq!(v["expected_workflow"], rt["workflow_file"]["content"]);
    assert_eq!(v["turn"], "turn-A");
    assert_eq!(v["client_user_message_id"], "client-A");
    let framing = text.replacen("Workflow run start:", "Workflow run started:", 1);
    let v = map(&rt, &prepared, located(Some("item-A"), false, &framing));
    assert_eq!(v["state"], "text differs, workflow bytes equal");
    assert_eq!(v["located_by"], "first user message of the turn");
    assert!(v["evidence_limits"].to_string().contains("U-WR-15"));
    let v = map(
        &rt,
        &prepared,
        located(Some("item-A"), true, &text.replace('\n', "\r\n")),
    );
    assert_eq!(v["state"], "text differs, workflow bytes differ");
    // A preserved historical expected method is incomparable: no equality inference.
    let mut historical = rt.clone();
    historical["text_identity"]["method"] = "historical.text/v0".into();
    let v = map(&historical, &prepared, located(Some("item-A"), true, &text));
    assert_eq!(v["state"], "incomparable");
    assert_eq!(v["expected_text"]["method"], "historical.text/v0");
    assert_ne!(v["observed_text"]["method"], v["expected_text"]["method"]);
    let v = map(
        &rt,
        &prepared,
        Observation::Located(crate::workflow_workspace::LocatedTurnText::NotFound {
            item: Some("item-A".into()),
            by_client: Some(true),
        }),
    );
    assert_eq!(v["state"], "not found");
    assert!(v.get("observed_text").is_none());
    let v = map(
        &rt,
        &prepared,
        Observation::Located(crate::workflow_workspace::LocatedTurnText::NotFound {
            item: None,
            by_client: None,
        }),
    );
    assert_eq!(v["state"], "not found");
    assert!(v.get("item").is_none());
    let v = map(&rt, &prepared, located(None, true, &text));
    assert_eq!(v["state"], "unreadable", "unattributable text is never verified");
    assert!(v.get("observed_text").is_none());
    let v = map(
        &rt,
        &prepared,
        Observation::Located(crate::workflow_workspace::LocatedTurnText::Unreadable),
    );
    assert_eq!(v["state"], "unreadable");
    let v = map(&rt, &prepared, Observation::ReadFailed("fixture read failure"));
    assert_eq!(v["state"], "unreadable");
    assert!(v["evidence_limits"]
        .to_string()
        .contains("fixture read failure"));
    // An end notice or an absent identity is not a live run-start check.
    let mut end = rt.clone();
    end["purpose"] = "run end notice".into();
    assert!(supply_check_body(
        &end,
        &prepared,
        located(Some("i"), true, &text),
        "t",
        "c",
        "k",
        "r"
    )
    .is_err());
    assert!(supply_check_body(
        &rt,
        &prepared,
        located(Some("i"), true, &text),
        "",
        "c",
        "k",
        "r"
    )
    .is_err());
}
// Minting needs a Host-issued dispatch; none means nothing was checked.
#[test]
fn unreadable_check_requires_issued_native_dispatch() {
    let f = Fixture::new();
    let p = f.store();
    let (_, published) = original_start(&f, &p);
    let refused = CompletedSupplyCheck::unreadable_after_dispatch(
        &[], &published, "turn-A", "client-A", "check-A", "read-A", "lost",
    );
    assert!(refused
        .unwrap_err()
        .contains("no native item read was issued"));
}
// A pending live check publishes its original bytes once; the token re-resolves its run_text.
#[test]
fn pending_live_check_publishes_original_bytes_and_yields_typed_token() {
    let f = Fixture::new();
    let p = f.store();
    let (prepared, published) = original_start(&f, &p);
    let body = map(
        published.run_text_record().body(),
        &prepared,
        located(Some("item-A"), true, prepared.text()),
    );
    let pending = PendingSupplyCheck::new(
        &p,
        CompletedSupplyCheck {
            body,
            sources: vec!["receipt-A".into()],
        },
        &published,
        "writer",
    )
    .unwrap();
    let original = pending.bytes().to_vec();
    FAIL_AFTER_LINK.with(|v| v.set(true));
    assert!(pending.publish(&p).is_err());
    let token = pending.publish(&p).unwrap();
    assert_eq!(token.check().reference(), pending.reference());
    assert_eq!(token.check().bytes(), &original[..]);
    assert_eq!(token.check().envelope()["observed_at"], "read-A");
    assert_eq!(
        token.run_text().reference(),
        published.run_text_record().reference()
    );
    assert_eq!(p.list_references().unwrap().len(), 3);
}
