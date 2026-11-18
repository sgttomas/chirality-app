//! DEL-02-03 REQ-008: the point tool's definition, argument check, digest,
//! record body, pointer and receipt, read against independent expectations.
use super::*;

fn args(extra: Value) -> Value {
    let mut v = json!({"version":1,"operation":"place"});
    for (k, x) in extra.as_object().unwrap() { v[k] = x.clone(); }
    v
}
fn rs() -> Value {
    serde_json::from_str(include_str!("../schemas/RS_RECORD.schema.json")).unwrap()
}

#[test]
fn the_definition_is_closed_version_one_and_matches_the_record_schema() {
    let d = definition();
    assert_eq!(d["name"], "chirality_point_v1");
    assert_eq!(d["type"], "function");
    assert_eq!(d["inputSchema"]["additionalProperties"], false);
    assert_eq!(d["inputSchema"]["properties"]["operation"]["enum"], json!(["place"]));
    // The record body carries the tool's own schema, unchanged.
    let mut recorded = rs()["$defs"]["pointArguments"].clone();
    recorded.as_object_mut().unwrap().remove("description");
    assert_eq!(recorded, input_schema());
    // The rule the agent gets is in the description itself.
    let text = d["description"].as_str().unwrap();
    for needed in ["Give only the terms the person stated", "Leave out every field the person did not state", "does not pause you", "tell the person plainly that no point was recorded"] {
        assert!(text.contains(needed), "{needed}");
    }
}

#[test]
fn arguments_outside_version_one_are_refused_with_the_apps_reason() {
    assert!(validate(&args(json!({}))).is_ok());
    assert!(validate(&args(json!({"kind":"sign-off","reservedAct":"engineering approval","concerns":{"content":"drawing A","revision":"r2"}}))).is_ok());
    for (case, value) in [
        ("unknown property", args(json!({"assignee":"someone"}))),
        ("unknown property inside concerns", args(json!({"concerns":{"content":"x","owner":"y"}}))),
        ("empty concerns", args(json!({"concerns":{}}))),
        ("operation revise", args(json!({"operation":"revise"}))),
        ("version 2", args(json!({"version":2}))),
        ("kind outside the five", args(json!({"kind":"approval"}))),
        ("wrong type", args(json!({"whoMustRespond":7}))),
        ("empty text", args(json!({"label":""}))),
        ("not an object", json!("place")),
        ("a non-integer number", args(json!({"label":1.5}))),
    ] {
        let reason = validate(&value).unwrap_err();
        assert!(reason.starts_with("The arguments are not valid for chirality_point_v1 version 1"), "{case}: {reason}");
        assert!(reason.ends_with("no point was recorded."), "{case}: {reason}");
    }
    // Over the App's own byte limit, each field within its own maximum.
    let wide = "\u{10348}".repeat(1000);
    let big = args(json!({"whenItArises":wide,"responseRequested":wide,"resolvedWhen":wide,"agentStatement":wide,"whoMustRespond":"\u{10348}".repeat(500)}));
    let reason = validate(&big).unwrap_err();
    assert!(reason.contains("the App's own limit of 16384 bytes"), "{reason}");
}

#[test]
fn the_digest_is_of_the_canonical_arguments_whatever_the_key_order() {
    let a: Value = serde_json::from_str(r#"{"version":1,"operation":"place","label":"L","kind":"input"}"#).unwrap();
    let b: Value = serde_json::from_str(r#"{"kind":"input","label":"L","operation":"place","version":1}"#).unwrap();
    assert_eq!(digest(&a).unwrap(), digest(&b).unwrap());
    // Independently: SHA-256 of the canonical form written out by hand.
    assert_eq!(digest(&a).unwrap(), crate::util::sha256_hex(br#"{"kind":"input","label":"L","operation":"place","version":1}"#));
    assert_ne!(digest(&a).unwrap(), digest(&args(json!({"label":"L","kind":"review"}))).unwrap());
}

fn source() -> Source {
    Source { home: "app-home:fixture".into(), home_class: "H-acct".into(), generation: "gen:v1:s:73:h:68:n:1".into(), thread: "thread".into(), turn: "turn".into(), call: "call".into(), request: json!(7) }
}

#[test]
fn the_record_body_is_a_valid_point_placed_entry_and_its_pointer_holds_no_supplied_text() {
    let arguments = args(json!({"whoMustRespond":"MARKER-TERM the reviewer","kind":"review"}));
    let run = json!({"state":"no run","reason":"no run open in this conversation in this App session"});
    let placer = json!({"observed":{"caller":"this conversation's agent, through the App's point tool","turnStart":null,"turnStartLimit":"the App did not observe starting this turn"}});
    let point = crate::util::opaque_id("pt-").unwrap();
    let body = record_body(&point, &source(), "/project", &run, &placer, &arguments, &digest(&arguments).unwrap(), "2026-11-18T00:00:00Z");
    let entry = crate::records::envelope(KIND, &crate::records::APP_WRITER, body.clone(), "rec:app:fixture".into(), 1, None, None);
    let validator = crate::schema_validation::bundled().unwrap();
    validator.validate(&entry).unwrap();
    // The schema refuses a body carrying anything else, or arguments outside version 1.
    let mut extra = entry.clone();
    extra["body"]["note"] = json!("x");
    assert!(validator.validate(&extra).is_err());
    let mut wrong = entry.clone();
    wrong["body"]["arguments"]["assignee"] = json!("x");
    assert!(validator.validate(&wrong).is_err());
    let raw = pointer(&entry).unwrap();
    assert!(!raw.contains("MARKER-TERM"), "the pointer carries no supplied text");
    let decoded = decode(&raw).unwrap();
    assert_eq!(decoded["point"], json!(point));
    assert_eq!(decoded["record"], "rec:app:fixture");
    assert_eq!(decoded["source"], source().value());
    assert_eq!(decoded["digest"], json!({"method":DIGEST_METHOD,"value":digest(&arguments).unwrap()}));
    assert!(decode("{\"v\":2,\"kind\":\"placed\"}").is_none());
    assert!(decode("run:abc").is_none());
}

#[test]
fn a_receipt_is_recorded_or_not_recorded_and_carries_no_answer() {
    let run = json!({"state":"in run","run":"run:1"});
    let recorded = receipt(Some("pt-1"), None, Some(KEPT), &run);
    assert_eq!(recorded["success"], true);
    let text: Value = serde_json::from_str(recorded["contentItems"][0]["text"].as_str().unwrap()).unwrap();
    assert_eq!(text["state"], "recorded");
    assert_eq!(text["point"], "pt-1");
    assert_eq!(text["run"], run);
    let refused = receipt(None, Some("No App project is known for this conversation, so the point could not be kept; no point was placed."), None, &run);
    assert_eq!(refused["success"], false);
    let text: Value = serde_json::from_str(refused["contentItems"][0]["text"].as_str().unwrap()).unwrap();
    assert_eq!(text["state"], "not recorded");
    assert!(text["point"].is_null());
    assert!(pointer_pending("ledger refused").contains("the conversation's pointer to them could not be saved (ledger refused); the App completes it when it next can"));
}
