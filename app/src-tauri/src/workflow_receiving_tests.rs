//! Same-crate retained tests; original test bodies preserved from integration target.
use crate::workflow_workspace;
use crate::{role_supply, workflow_declaration, util};
use serde_json::{json, Value};
use std::collections::BTreeMap;
use workflow_workspace::*;
fn selection() -> Selection {
    let snapshot = Snapshot::from_files(BTreeMap::from([
        (
            "WORKFLOW.md".into(),
            b"---\r\nname: sample\r\n---\r\n# Method\r\nExact body bytes.\r\n".to_vec(),
        ),
        ("resources/binary.bin".into(), vec![0, 255]),
    ]))
    .unwrap();
    let id = snapshot
        .identity("bundled", "invented-test-release", "sample", None)
        .unwrap();
    // Deliberate test-double release admission through the existing typed seam;
    // source equality is not an actual shipping manifest or release qualification.
    Selection::synthetic_shipped(snapshot, id).unwrap()
}
struct HeldTestCopies(Vec<std::path::PathBuf>);
impl Drop for HeldTestCopies {
    fn drop(&mut self) {
        for root in &self.0 {
            let _ = std::fs::remove_dir_all(root);
        }
    }
}
thread_local! {static TEST_COPIES:std::cell::RefCell<HeldTestCopies>=std::cell::RefCell::new(HeldTestCopies(vec![]));}
// Each test-owned physical holding copy is compared through production capture.
fn store() -> std::path::PathBuf {
    let mut bytes = [0; 16];
    getrandom::fill(&mut bytes).unwrap();
    let base = std::env::temp_dir().join(format!("wr-receiving-{}", util::sha256_hex(&bytes)));
    std::fs::create_dir(&base).unwrap();
    TEST_COPIES.with(|copies| copies.borrow_mut().0.push(base.clone()));
    let path = base.join("revision");
    selection().snapshot().publish_new(&path).unwrap();
    path
}
fn scope(run: &str) -> RunScope {
    RunScope {
        run: run.into(),
        conversation: "thread-test".into(),
        home: "home-test".into(),
        generation: json!({"appSession":"session-test","home":"home-test","spawnCounter":1}),
        source_root: "invented-test-release".into(),
        holding_library: "invented-test-release".into(),
        selection_ref: "selection-test".into(),
        revision_store: store(),
    }
}
fn prepared() -> PreparedRunText {
    PreparedRunText::start(
        &selection(),
        scope("run-A"),
        "workflow-revisions/sample",
        None,
    )
    .unwrap()
}
fn exact(s: &str) -> Value {
    role_supply::content(s.as_bytes())
}
fn schema(target: &str, value: &Value) {
    let wd: Value = serde_json::from_str(workflow_declaration::SCHEMA).unwrap();
    let wr: Value = serde_json::from_str(include_str!(
        "../resources/workflow_role/workspace-registration.schema.json"
    ))
    .unwrap();
    let mut registry = jsonschema::Registry::new();
    for s in [wd, wr.clone()] {
        registry = registry.add(s["$id"].as_str().unwrap(), s.clone()).unwrap();
    }
    let registry = registry.prepare().unwrap();
    jsonschema::options()
        .with_registry(&registry)
        .offline()
        .build(&json!({"$ref":format!("{}#/$defs/{target}",wr["$id"].as_str().unwrap())}))
        .unwrap()
        .validate(value)
        .unwrap();
}
#[test]
fn complete_run_record_retains_source_and_composed_scopes_without_normalization() {
    let s = selection();
    let p = prepared();
    schema("run_text", p.record());
    assert_eq!(p.scope().generation["home"], "home-test");
    assert!(p.text().contains(s.snapshot().workflow_text()));
    assert_eq!(
        p.record()["workflow_file"]["content"],
        exact(s.snapshot().workflow_text())
    );
    assert_eq!(p.record()["text_identity"], exact(p.text()));
    assert_ne!(
        p.record()["workflow_file"]["content"],
        p.record()["text_identity"]
    );
    assert_eq!(
        p.record()["other_files"][0]["sha256"],
        util::sha256_hex(&[0, 255])
    );
    assert_eq!(p.record()["workflow"], json!(s.identity()));
    let params = p.turn_params("Person's own input", "client-test").unwrap();
    assert_eq!(params["input"][0]["text"], p.text());
    assert_eq!(params["input"][1]["text"], "Person's own input");
    assert_eq!(params["clientUserMessageId"], "client-test");
    assert!(!params
        .as_object()
        .unwrap()
        .contains_key("developerInstructions"));
}
#[test]
fn method_incomparability_precedes_values_and_body_fallback() {
    let p = prepared();
    let mut legacy = p.record()["text_identity"].clone();
    legacy["method"] = json!("sha256 over UTF-8 text");
    let body = p.record()["workflow_file"]["content"].clone();
    let c = p.compare_observed_text(&legacy, &body, p.text()).unwrap();
    assert_eq!(c.state, "incomparable");
    assert_eq!(c.observed_text, exact(p.text()));
    let changed = format!("changed wrapper\n{}", p.text());
    let c = p
        .compare_observed_text(&p.record()["text_identity"], &body, &changed)
        .unwrap();
    assert_eq!(c.state, "text differs, workflow bytes equal");
    let mut historical_body = body.clone();
    historical_body["method"] = json!("unknown-foreign-method");
    assert_eq!(
        p.compare_observed_text(&p.record()["text_identity"], &historical_body, &changed)
            .unwrap()
            .state,
        "incomparable"
    );
    assert_eq!(
        p.compare_observed_text(&p.record()["text_identity"], &historical_body, p.text())
            .unwrap()
            .state,
        "equal composed text"
    );
    assert!(p
        .compare_observed_text(&json!({"method":"","value":"x"}), &body, p.text())
        .is_err());
}
#[test]
fn chain_and_end_are_explicit_scope_bound_owner_facts_not_text_markers() {
    let a = prepared();
    let source = selection();
    let end = OwnerRunEnd {
        home: "home-test".into(),
        conversation: "thread-test".into(),
        run: "run-A".into(),
        workflow: source.identity().clone(),
        reason: RunEndReason::Completed,
    };
    let (notice, r) = a.end_notice(&end).unwrap();
    schema("run_text", &r);
    assert!(notice.ends_with("No workflow is in force."));
    assert_eq!(r["text_identity"], exact(&notice));
    let b = PreparedRunText::start(
        &source,
        scope("run-B"),
        "workflow-revisions/sample",
        Some(&end),
    )
    .unwrap();
    schema("run_text", b.record());
    assert!(b
        .text()
        .starts_with("[Chirality] Previous workflow run ended:"));
    assert_eq!(b.record()["chain"]["prior_run"], "run-A");
    assert!(b.text().contains(source.snapshot().workflow_text()));
    assert!(!b.record()["lines"]
        .as_object()
        .unwrap()
        .contains_key("end_line"));
    let mut wrong = end.clone();
    wrong.home = "foreign-home".into();
    assert!(a.end_notice(&wrong).is_err());
    assert!(PreparedRunText::start(
        &source,
        scope("run-B"),
        "workflow-revisions/sample",
        Some(&wrong)
    )
    .is_err());
    let mut wrong = end.clone();
    wrong.run = "turn-interrupted-not-run-A".into();
    assert!(a.end_notice(&wrong).is_err());
    let mut successor = end.clone();
    successor.reason = RunEndReason::ToStart("sample".into());
    assert!(a.end_notice(&successor).is_err());
    assert!(
        PreparedRunText::start(
            &source,
            scope("run-B"),
            "workflow-revisions/sample",
            Some(&successor)
        )
        .unwrap()
        .record()["chain"]["ended"]
            == "ended to start sample"
    );
    let unbound = scope("run-A");
    assert!(
        PreparedRunText::start(&source, unbound, "workflow-revisions/sample", Some(&end)).is_err()
    );
}
#[test]
fn home_generation_source_and_identity_omissions_cannot_prepare() {
    let s = selection();
    for key in ["home", "generation", "source", "selection"] {
        let mut sc = scope("run-A");
        match key {
            "home" => sc.home = "other-home".into(),
            "generation" => sc.generation = json!(1),
            "source" => sc.source_root = "another-root".into(),
            _ => sc.selection_ref.clear(),
        };
        assert!(PreparedRunText::start(&s, sc, "workflow-revisions/sample", None).is_err());
    }
    let mut sc = scope("run-A");
    sc.generation["appSession"] = json!("");
    assert!(PreparedRunText::start(&s, sc, "workflow-revisions/sample", None).is_err());
}

#[test]
fn actual_holding_revision_tamper_refuses_preparation_without_silent_rebind() {
    let s = selection();
    let sc = scope("run-A");
    let path = sc.revision_store.clone();
    std::fs::write(
        path.join("resources/binary.bin"),
        b"changed outside registration",
    )
    .unwrap();
    assert!(PreparedRunText::start(&s, sc, "workflow-revisions/sample", None).is_err());
}

#[test]
fn tx3_body_fallback_requires_original_selected_marker_tuple() {
    let p = prepared();
    let expected = &p.record()["text_identity"];
    let body = &p.record()["workflow_file"]["content"];
    let changed = format!("prefix-only wrapper change\n{}", p.text());
    assert_eq!(
        p.compare_observed_text(expected, body, &changed)
            .unwrap()
            .state,
        "text differs, workflow bytes equal"
    );
    let revision = p.record()["workflow"]["revision"].as_str().unwrap();
    let short = &revision[..12];
    for altered in [
        p.text().replace(
            "<<<chirality-workflow sample@",
            "<<<chirality-workflow foreign@",
        ),
        p.text()
            .replace(&format!("sample@{short}"), "sample@FOREIGNREV12"),
        p.text().replace(" begin>>>", " begin>>> extra-field"),
        p.text().replace(" end>>>", " end>>> extra-field"),
    ] {
        assert_ne!(
            p.compare_observed_text(expected, body, &altered)
                .unwrap()
                .state,
            "text differs, workflow bytes equal"
        );
    }
    let mut unknown = expected.clone();
    unknown["method"] = json!("unknown-other-method");
    assert_eq!(
        p.compare_observed_text(&unknown, body, &changed)
            .unwrap()
            .state,
        "incomparable"
    );
    let (begin, end) = (
        p.record()["lines"]["begin_marker"].as_str().unwrap(),
        p.record()["lines"]["end_marker"].as_str().unwrap(),
    );
    let raw_body = selection().snapshot().workflow_text().to_owned();
    let doubled = format!("changed prefix\n{begin}\n{raw_body}\n{end}\n{end}");
    assert_eq!(
        p.compare_observed_text(expected, body, &doubled)
            .unwrap()
            .state,
        "text differs, workflow bytes differ"
    );
}
