//! Explicit ACCESS/NIR/REC source semantics; no supplier/private context hydration.
use chirality_app_v4_lib::{
    access::ConversationSelection,
    recovery::{self, AppProjectSource, ExplicitAppProjectContext},
};
use serde_json::{json, Value};
#[test]
fn unknown_access_no_row_offer_or_defaults_and_actual_home_kind_only() {
    let mut selection = ConversationSelection::new_explicit("conversation", None).unwrap();
    assert!(selection.canonical_record().is_none());
    assert!(selection.recovery_home().is_none());
    assert!(selection
        .offer_last("chatgpt-account", "openai", "m")
        .is_err());
    assert!(selection
        .start_params(
            &json!({"appSession":"s","home":"opaque-native-home","spawnCounter":1}),
            "account",
            false
        )
        .is_err());
    selection
        .choose("chatgpt-account", "openai", "m", false)
        .unwrap();
    selection
        .start_params(
            &json!({"appSession":"s","home":"opaque-native-home","spawnCounter":1}),
            "account",
            false,
        )
        .unwrap();
    assert_eq!(selection.recovery_home(), Some("H-acct"));
    assert!(selection.canonical_record().is_none());
    assert!(selection.snapshot().get("project").is_none());
    assert_eq!(selection.snapshot()["selection"]["source"], "person");
}
#[test]
fn exact_opaque_context_codec_all_durable_hot_conflict_and_idempotence() {
    let token = "submission:actual-opaque";
    let q = ExplicitAppProjectContext::known("Root Q / 家", AppProjectSource::ConfiguredDirectory)
        .unwrap();
    let raw = recovery::encode_submission_context(token, q.reference()).unwrap();
    assert_eq!(raw, "[\"submission:actual-opaque\",\"Root Q / 家\"]");
    let index = json!({"project":"historical P","tags":[]});
    let hot = json!({"owner":"DEL-01-04","value":raw,"seq":1});
    assert!(
        recovery::submission_context_plan(Some(&index), &[], &[hot.clone()], token, Some("R"))
            .is_err()
    );
    let same =
        recovery::submission_context_plan(Some(&index), &[], &[hot.clone()], token, q.reference())
            .unwrap();
    assert_eq!(same["historicalProject"], "historical P");
    assert_eq!(same["relation"], "different; no transfer");
    assert_eq!(same["idempotent"], true);
    assert_eq!(same["durableBindingObserved"], false);
    assert!(same["limit"].as_str().unwrap().contains("memory-only"));
    let conflict = json!({"owner":"DEL-01-04","value":recovery::encode_submission_context(token,Some("R")).unwrap(),"seq":2});
    assert!(recovery::submission_context_plan(
        Some(&index),
        &[conflict],
        &[hot.clone()],
        token,
        q.reference()
    )
    .is_err());
    assert!(recovery::submission_context_plan(None, &[], &[hot], token, None).is_err());
    let absence =
        recovery::submission_context_plan(None, &[], &[], "submission:new", None).unwrap();
    assert_eq!(absence["tag"]["value"], "[\"submission:new\",null]");
    assert!(absence["limit"].as_str().unwrap().contains("no row"));
    let mut view = q.view();
    view["reference"] = json!("R");
    assert_eq!(q.reference(), Some("Root Q / 家"));
    assert_eq!(ExplicitAppProjectContext::unknown().reference(), None);
    assert!(ExplicitAppProjectContext::known("", AppProjectSource::OpenedDirectory).is_err());
}
#[test]
fn canonical_access_known_shape_stays_02_and_unknown_never_hydrates() {
    let known = ConversationSelection::new_explicit("c", Some("P")).unwrap();
    let schema: Value = serde_json::from_str(include_str!(
        "../resources/runtime_core/access.conversation-selection.schema.json"
    ))
    .unwrap();
    jsonschema::options()
        .offline()
        .build(&schema)
        .unwrap()
        .validate(&known.canonical_record().unwrap())
        .unwrap();
    let mut imported = known.view();
    imported["projectContext"]["reference"] = json!("Q");
    assert_eq!(known.project(), Some("P"));
    let unknown = ConversationSelection::new_explicit("u", None).unwrap();
    assert!(unknown.canonical_record().is_none());
    assert_eq!(unknown.snapshot()["projectSensitiveChoiceAvailable"], false);
}
