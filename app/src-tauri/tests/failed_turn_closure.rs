//! Failed-turn closure as the App receives it: shape only. The App takes a
//! destination request, its RS closure entry and its settings row as supplied
//! claims; it runs no destination flow, admits no host and grants nothing.
//! These cases cover what the receiving code refuses for a closure caused by
//! "turn failed" beyond the cases in catalog_adapter.rs, schema_validation.rs
//! and policy_standing.rs: an incomplete turn binding, an invented cause, and
//! a grant, result or waiting notice on the closed request.
use chirality_app_v4_lib::{act_policy::SchemaClaim, receiving, schema_validation};
use serde_json::{json, Value};

const BINDING: [&str; 4] = ["hostIdentity", "conversationId", "runId", "turnId"];

fn resource(dir: &str, name: &str) -> Value {
    let path = std::path::Path::new(env!("CARGO_MANIFEST_DIR")).join(dir).join(name);
    serde_json::from_slice(&std::fs::read(path).unwrap()).unwrap()
}
fn turn(run: &Value) -> Value {
    json!({"hostIdentity":"FX-PIPE-01","conversationId":"conversation:fixture","runId":run,"turnId":"turn:fixture"})
}
fn loop_closure() -> Value {
    let mut request = resource("resources/catalog_adapter", "LOOP_DESTINATION_REQUEST.example.valid.json");
    for field in ["result", "grantScope", "interimNotice"] { request.as_object_mut().unwrap().remove(field); }
    request["state"] = "unanswered at end".into();
    request["endCause"] = "turn failed".into();
    request["turnRef"] = turn(&json!("run:fixture"));
    request
}
fn receive_loop(request: &Value) -> Result<receiving::ReceivedDocument, String> {
    receiving::receive_destination(&serde_json::to_vec(request).unwrap())
}
fn rs_closure() -> Value {
    let mut record = resource("schemas/fixtures", "valid-records.json").as_array().unwrap().iter()
        .find(|e| e["kind"] == "destination_request_closed").unwrap().clone();
    record["body"]["state"] = "unanswered at end".into();
    record["body"].as_object_mut().unwrap().remove("reason");
    record["body"]["cause"] = "turn failed".into();
    record["body"]["turnRef"] = turn(&record["runId"].clone());
    record
}
fn settings_closure() -> Value {
    let mut body = resource("resources/policy_standing", "AS_SETTINGS_IN.valid.examples.json").as_array().unwrap().iter()
        .find(|e| e["instance"]["destinationSettings"].is_object()).unwrap()["instance"].clone();
    body["destinationSettings"]["agentRequests"] = json!([{
        "requestRef":"rec:fixture:pending","target":{"destination":"A-1","category":"other APIs"},
        "scopeSought":"once","state":"unanswered at end","stateReason":"turn failed",
        "turnRef":turn(&body["runId"].clone())}]);
    body
}

#[test]
fn loop_destination_closure_refuses_incomplete_binding_invented_cause_and_any_grant() {
    let closed = loop_closure();
    receive_loop(&closed).unwrap();
    for field in BINDING {
        let mut incomplete = closed.clone();
        incomplete["turnRef"].as_object_mut().unwrap().remove(field);
        assert!(receive_loop(&incomplete).is_err(), "{field}");
    }
    let mut invented = closed.clone();
    invented["endCause"] = "timed out; granted".into();
    assert!(receive_loop(&invented).is_err());
    for (field, value) in [
        ("grantScope", json!("once")),
        ("result", json!({"class":3,"label":"granted","reporter":"host control"})),
        ("interimNotice", json!("waiting for the person's answer")),
    ] {
        let mut granted = closed.clone();
        granted[field] = value;
        assert!(receive_loop(&granted).is_err(), "{field}");
    }
    let mut pending = closed;
    pending["state"] = "pending".into();
    assert!(receive_loop(&pending).is_err(), "a failed turn leaves no request pending");
}

#[test]
fn rs_destination_closure_refuses_invented_cause_and_any_state_but_unanswered() {
    let validator = schema_validation::bundled().unwrap();
    let closed = rs_closure();
    validator.validate(&closed).unwrap();
    let mut invented = closed.clone();
    invented["body"]["cause"] = "timed out; granted".into();
    assert!(validator.validate(&invented).is_err());
    let mut not_granted = closed;
    not_granted["body"]["state"] = "not granted".into();
    not_granted["body"]["reason"] = "prompt not shown".into();
    assert!(validator.validate(&not_granted).is_err());
}

#[test]
fn settings_request_closure_refuses_incomplete_binding_invented_cause_and_granted_state() {
    let closed = settings_closure();
    SchemaClaim::receive(closed.clone(), true).unwrap();
    for field in BINDING {
        let mut incomplete = closed.clone();
        incomplete["destinationSettings"]["agentRequests"][0]["turnRef"].as_object_mut().unwrap().remove(field);
        assert!(SchemaClaim::receive(incomplete, true).is_err(), "{field}");
    }
    let mut invented = closed.clone();
    invented["destinationSettings"]["agentRequests"][0]["stateReason"] = "timed out; granted".into();
    assert!(SchemaClaim::receive(invented, true).is_err());
    for state in ["granted", "pending"] {
        let mut changed = closed.clone();
        changed["destinationSettings"]["agentRequests"][0]["state"] = state.into();
        assert!(SchemaClaim::receive(changed, true).is_err(), "{state}");
    }
}
