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
        crate::storage::project_file(&f.0, "workflow").unwrap()
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
        basis: None,
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
    // BUNDLED-RUN-01: a ProductionBundle admission naming the selected manifest
    // and a bundle root, but not the closed subject's identity and bytes, is not
    // a bundled run, even when it reaches publication directly.
    let mut forged = selection.clone();
    forged.admission = SelectionAdmission::ProductionBundle {
        manifest_sha256:
            crate::workflow_workspace::production_catalog::SELECTED_BUNDLED_MANIFEST_SHA256.into(),
        release_subject: crate::workflow_workspace::production_catalog::RELEASE_SUBJECT.into(),
        holding_library: None,
        bundle_root: Some(f.0.clone()),
    };
    assert!(PreparedRunPublication::new(
        &p,
        &forged,
        prepared.clone(),
        "writer",
        "selected",
        "prepared"
    )
    .is_err());
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
        basis: None,
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
    let start_path = crate::storage::project_file(&f.0, "workflow").unwrap().join(format!(
        "{}.json",
        key(start.run_text_record().reference()).unwrap()
    ));
    std::fs::remove_file(start_path).unwrap();
    assert!(f.store().resolve(reopened.reference()).is_err());
}
// V9 F-5: listing enumerates the pinned project descriptor and reports a symlinked
// (including dangling) `.chirality`, `records` or `workflow` explicitly, never as "no records".
#[test]
fn listing_refuses_symlinks_and_follows_the_pinned_project() {
    let f = Fixture::new();
    let p = f.store();
    assert_eq!(p.list_references().unwrap(), Vec::<String>::new(), "absent store: no records");
    std::os::unix::fs::symlink(f.0.join("nowhere"), f.0.join(".chirality")).unwrap();
    assert!(p.list_references().is_err(), "dangling .chirality symlink is not 'no records'");
    std::fs::remove_file(f.0.join(".chirality")).unwrap();
    std::fs::create_dir_all(f.0.join(".chirality/records")).unwrap();
    std::os::unix::fs::symlink(f.0.join("nowhere"), f.0.join(".chirality/records/workflow")).unwrap();
    assert!(p.list_references().is_err(), "dangling workflow symlink is not 'no records'");
    std::fs::remove_file(f.0.join(".chirality/records/workflow")).unwrap();
    let outside = Fixture::new();
    std::fs::create_dir(outside.0.join("workflow")).unwrap();
    std::os::unix::fs::symlink(outside.0.join("workflow"), f.0.join(".chirality/records/workflow")).unwrap();
    assert!(p.list_references().is_err(), "symlinked workflow directory refused");
    std::fs::remove_file(f.0.join(".chirality/records/workflow")).unwrap();
    let a = pending(&p);
    p.publish(&a).unwrap();
    assert_eq!(p.list_references().unwrap(), vec![a.reference().to_owned()]);
    // The path is replaced after open (the project moved, another folder put
    // at its path). DEL-04-03 AC-008: a project found at another folder is not
    // attached until the person resolves it, so the kept handle lists nothing,
    // neither the replacement's names nor the moved project's records.
    let moved = f.0.with_extension("moved");
    std::fs::rename(&f.0, &moved).unwrap();
    std::fs::create_dir_all(f.0.join(".chirality/records/workflow")).unwrap();
    std::fs::write(
        f.0.join(".chirality/records/workflow/00000000-0000-4000-8000-000000000000.json"),
        b"{}",
    )
    .unwrap();
    let replaced = p.list_references().unwrap_err();
    assert!(replaced.contains("not attached"), "{replaced}");
    std::fs::remove_dir_all(&f.0).unwrap();
    std::fs::rename(&moved, &f.0).unwrap();
    // The project back at its folder: the same handle lists its records again.
    assert_eq!(p.list_references().unwrap(), vec![a.reference().to_owned()]);
}
// V9 J3 note: PublishedText is sealed. Outside this module no type can name
// sealed::Sealed, so only the impls in this file exist; this guard fails if the
// module grows another implementor or loses the seal.
#[test]
fn published_text_is_sealed_to_two_types() {
    let source = include_str!("workflow_record_store.rs");
    let count = |needle: &str| source.matches(needle).count();
    assert_eq!(count("pub trait PublishedText: sealed::Sealed {"), 1);
    assert_eq!(count("    impl Sealed for super::"), 2);
    assert_eq!(count("impl PublishedText for "), 2);
    assert_eq!(count("impl PublishedText for PublishedRunText {"), 1);
    assert_eq!(count("impl PublishedText for PublishedEndNotice {"), 1);
    assert_eq!(count("pub trait Sealed {}"), 1, "Sealed stays inside the private module");
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
// BUNDLED-RUN-01: publication itself requires this App's recorded installed
// root. An exact copy of the selected subject at another root is not a bundled
// run even when it reaches publication directly, and a manifest change after
// preparation refuses publication (first attempt and retry) before any record.
#[test]
fn bundled_publication_requires_this_apps_installed_root_and_rechecks_at_publish() {
    use crate::workflow_workspace::{production_catalog::ProductionCatalog, PreparedRunText, RunScope};
    let f = Fixture::new();
    let p = f.store();
    let catalog = ProductionCatalog::load().unwrap();
    let make = |name: &str| {
        let root = f.0.join(name).join("workflows");
        std::fs::create_dir_all(&root).unwrap();
        std::fs::write(root.join("MANIFEST.json"), catalog.manifest()).unwrap();
        catalog.select_embedded().snapshot().publish_new(&root.join("coordinated-knowledge-work")).unwrap();
        root
    };
    let installed = make("installed");
    let elsewhere = make("elsewhere");
    crate::workflow_workspace::development_catalog::record_installed_root(installed.clone()).unwrap();
    let start = |root: &std::path::Path| {
        let resolved = catalog.select_bundle_package(root, "coordinated-knowledge-work").unwrap();
        let selection = resolved.selection().clone();
        let scope = RunScope {
            run: "run-B".into(),
            conversation: "thread-B".into(),
            home: "home".into(),
            generation: json!({"home":"home","appSession":"session","spawnCounter":1}),
            source_root: selection.identity().source_root.clone(),
            holding_library: root.to_str().unwrap().into(),
            selection_ref: "selection-B".into(),
            revision_store: resolved.package_path().into(),
        };
        let prepared = PreparedRunText::start(&selection, scope, ".chirality/workflow-supply/x", None).unwrap();
        (selection, prepared)
    };
    let (copy, prepared) = start(&elsewhere);
    assert!(PreparedRunPublication::new(&p, &copy, prepared, "writer", "selected", "prepared").is_err());
    let (selection, prepared) = start(&installed);
    let publication = PreparedRunPublication::new(&p, &selection, prepared, "writer", "selected", "prepared").unwrap();
    std::fs::write(installed.join("MANIFEST.json"), b"{}").unwrap();
    assert!(publication.publish(&p).is_err());
    assert!(publication.publish(&p).is_err(), "a retry rechecks too");
    std::fs::write(installed.join("MANIFEST.json"), catalog.manifest()).unwrap();
    let published = publication.publish(&p).unwrap();
    assert_eq!(published.selection_record().body()["standing"], "bundled");
    assert_eq!(published.selection_record().body()["identity"]["origin"], "bundled");
}
/// DEL-04-03 AC-008 / REQ-007: a handle that read the project's records keeps
/// its binding but reads and writes nothing while the project's link is
/// changed, missing, names another store, or the folder is moved; once the
/// person restores the link the same handle reads what it read before.
#[test]
fn a_kept_handle_refuses_while_the_link_disagrees_and_reads_again_once_restored() {
    let f = Fixture::new();
    let p = f.store();
    let a = pending(&p);
    let reference = a.reference().to_owned();
    let first = p.publish(&a).unwrap();
    assert_eq!(p.resolve(&reference).unwrap().bytes(), first.bytes());
    assert_eq!(p.list_references().unwrap(), vec![reference.clone()]);
    let link_path = f.0.join(crate::records_store::PROJECT_LINK);
    let link: Value = serde_json::from_slice(&std::fs::read(&link_path).unwrap()).unwrap();
    let mut changed = link.clone();
    changed["projectId"] = json!("chirality-project:forged-fixture");
    let mut other_store = link.clone();
    other_store["storeId"] = json!("records-store:another-fixture");
    for (case, replacement, expected) in [
        ("changed", Some(changed), "link changed; not attached"),
        ("missing", None, "link missing; not attached"),
        ("another store", Some(other_store), "not attached"),
    ] {
        match &replacement {
            Some(v) => std::fs::write(&link_path, serde_json::to_vec(v).unwrap()).unwrap(),
            None => std::fs::remove_file(&link_path).unwrap(),
        }
        match p.resolve(&reference) {
            Err(ResolutionError::Unreadable(e)) => assert!(e.contains(expected), "{case}: {e}"),
            other => panic!("{case}: read through the kept handle: {other:?}"),
        }
        let listed = p.list_references().unwrap_err();
        assert!(listed.contains(expected), "{case}: {listed}");
        let write = p.publish(&pending(&p)).unwrap_err();
        assert!(write.contains(expected) || write.contains("association changed"), "{case}: {write}");
        crate::records_store::restore_link(&f.0).unwrap();
        assert_eq!(p.resolve(&reference).unwrap().bytes(), first.bytes(), "{case}: the same handle reads again");
        assert_eq!(p.list_references().unwrap(), vec![reference.clone()], "{case}: nothing was written while refused");
    }
    // Moved: the folder is no longer at the path the handle was bound to.
    let moved = f.0.with_file_name(format!("{}-moved", f.0.file_name().unwrap().to_string_lossy()));
    std::fs::rename(&f.0, &moved).unwrap();
    let read = p.resolve(&reference);
    let listed = p.list_references();
    let write = p.publish(&pending(&p));
    std::fs::rename(&moved, &f.0).unwrap();
    assert!(matches!(read, Err(ResolutionError::Unreadable(_))), "moved: {read:?}");
    assert!(listed.is_err(), "moved: {listed:?}");
    assert!(write.is_err(), "moved: {:?}", write.map(|r| r.reference().to_owned()));
    assert_eq!(p.list_references().unwrap(), vec![reference.clone()], "moved: nothing was written while refused");
}
