#[allow(dead_code)]
mod common;
use chirality_app_v4_lib::{records, schema_validation::{self, RecordValidator, RESOURCES}};
use serde_json::{json, Value};

fn fixtures() -> Vec<Value> {
    serde_json::from_str(include_str!("../schemas/fixtures/valid-records.json")).unwrap()
}
fn act() -> Value {
    fixtures().into_iter().find(|e| e["kind"] == "human_act" && e["body"]["actKind"] == "A16").unwrap()["body"].clone()
}

#[test]
fn declared_registry_validates_all_maintained_rs_fixtures() {
    let validator = schema_validation::bundled().unwrap();
    let entries = fixtures();
    assert_eq!(entries.len(), 66);
    for entry in entries { validator.validate(&entry).unwrap(); }
    let rs: Value = serde_json::from_str(RESOURCES[0].1).unwrap();
    fn refs(v: &Value, out: &mut Vec<String>) {
        match v {
            Value::Object(o) => {
                if let Some(Value::String(r)) = o.get("$ref") { out.push(r.clone()); }
                for v in o.values() { refs(v, out); }
            }
            Value::Array(a) => for v in a { refs(v, out); },
            _ => {}
        }
    }
    let mut found = Vec::new(); refs(&rs, &mut found);
    assert_eq!(found.iter().filter(|r| r.starts_with("chirality:del-02-03/")).count(), 19);
    let act: Value = serde_json::from_str(RESOURCES[2].1).unwrap();
    assert_eq!(act["$id"], "urn:chirality:app-v4:del-04-01:policy-class-record:0.1");
    // ACT is registered and compiled even though RS currently embeds act classes.
    let mut no_act = RESOURCES.to_vec(); no_act.remove(2);
    assert!(RecordValidator::from_resources(&no_act).is_err());
    assert!(found.iter().any(|r| r.starts_with("urn:chirality:app-v4:del-04-02:")));
}

#[test]
fn malformed_kind_nested_body_and_person_refuse_without_bytes_or_seq() {
    let dir = common::ScratchDirectory::new("chirality-w1");
    let log = dir.join("records.jsonl");
    assert!(records::append(&log, "unknown_kind", &records::APP_INTERFACE, act()).is_err());
    assert!(!log.exists());
    let first = records::append(&log, "human_act", &records::APP_INTERFACE, act()).unwrap();
    assert_eq!(first["seq"], 1);
    let before = std::fs::read(&log).unwrap();
    let invalid_recorder = records::Recorder { role: "", identity: "" };
    assert!(records::append(&log, "human_act", &invalid_recorder, act()).is_err());
    assert_eq!(std::fs::read(&log).unwrap(), before);
    let mut malformed = act(); malformed["relations"].as_object_mut().unwrap().remove("requestRef");
    let mut person = act(); person["decisionActor"]["identityVerified"] = json!("true");
    let mut wrong_class = act(); wrong_class["actKind"] = json!("A9");
    for body in [malformed, person, wrong_class, json!({})] {
        assert!(records::append(&log, "human_act", &records::APP_INTERFACE, body).is_err());
        assert_eq!(std::fs::read(&log).unwrap(), before);
    }
    let second = records::append(&log, "human_act", &records::APP_INTERFACE, act()).unwrap();
    assert_eq!(second["seq"], 2);
}

#[test]
fn missing_invalid_and_unregistered_resources_fail_schema_setup() {
    assert!(RecordValidator::from_resources(&RESOURCES[..3]).is_err());
    let mut resources = RESOURCES.to_vec(); resources[1].1 = "{";
    assert!(RecordValidator::from_resources(&resources).is_err());
    // An unknown HTTPS or file URI must refuse; neither can trigger retrieval.
    for uri in ["https://example.invalid/not-registered", "file:///tmp/not-registered"] {
        let mut root: Value = serde_json::from_str(RESOURCES[0].1).unwrap();
        root["$defs"]["unregistered"] = json!({"$ref": uri});
        let text = serde_json::to_string(&root).unwrap();
        let mut resources = RESOURCES.to_vec(); resources[0].1 = &text;
        assert!(RecordValidator::from_resources(&resources).is_err());
    }
}

#[test]
fn partial_last_line_preserves_w0_refusal() {
    let dir = common::ScratchDirectory::new("chirality-w1-partial");
    let log = dir.join("records.jsonl");
    std::fs::write(&log, b"{partial").unwrap();
    assert!(records::append(&log, "human_act", &records::APP_INTERFACE, act()).unwrap_err().contains("partial line"));
    assert_eq!(std::fs::read(log).unwrap(), b"{partial");
}

fn package_fixture() -> Value {
    serde_json::from_str(include_str!("../schemas/fixtures/decision-package-file.example.valid.json")).unwrap()
}
fn offer_fixtures() -> Value {
    serde_json::from_str(include_str!("../schemas/fixtures/aac.offer.example.valid.json")).unwrap()
}
fn capture_fixtures() -> Value {
    serde_json::from_str(include_str!("../schemas/fixtures/aac.capture-evidence.example.valid.json")).unwrap()
}

#[test]
fn package_offer_capture_apis_validate_full_maintained_objects() {
    schema_validation::validate_package(&package_fixture()).unwrap();
    for offer in offer_fixtures()["instances"].as_array().unwrap() {
        schema_validation::validate_offer(offer).unwrap();
    }
    for capture in capture_fixtures()["instances"].as_array().unwrap() {
        schema_validation::validate_capture(capture).unwrap();
    }
    // Package scope remains optional in EXEC; presentation mapping belongs to AAC.
    let mut absent_scope = package_fixture(); absent_scope.as_object_mut().unwrap().remove("scope");
    schema_validation::validate_package(&absent_scope).unwrap();
}

#[test]
fn full_package_and_authoritative_offer_capture_reject_malformed_objects() {
    let mut package = package_fixture(); package["alternatives"][0]["consequences"] = json!(7);
    assert!(schema_validation::validate_package(&package).is_err());
    let mut package = package_fixture(); package.as_object_mut().unwrap().remove("packageId");
    assert!(schema_validation::validate_package(&package).is_err());
    let mut package = package_fixture(); package["unexpected"] = json!(true);
    assert!(schema_validation::validate_package(&package).is_err());
    let mut offer = offer_fixtures()["instances"].as_array().unwrap().iter().find(|o| o["actKind"] == "A16").unwrap().clone();
    offer.as_object_mut().unwrap().remove("requestRef");
    assert!(schema_validation::validate_offer(&offer).is_err());
    let mut offer = offer_fixtures()["instances"][0].clone(); offer["offerDigest"]["value"] = json!(42);
    assert!(schema_validation::validate_offer(&offer).is_err());
    let capture = capture_fixtures()["instances"].as_array().unwrap().iter().find(|c| c["actKind"] == "A16").unwrap().clone();
    let mut malformed = capture.clone(); malformed["actor"]["identityVerified"] = json!(true);
    assert!(schema_validation::validate_capture(&malformed).is_err());
    let mut malformed = capture.clone(); malformed["inputSource"] = json!("agent automation");
    assert!(schema_validation::validate_capture(&malformed).is_err());
    let mut malformed = capture; malformed.as_object_mut().unwrap().remove("requestRef");
    assert!(schema_validation::validate_capture(&malformed).is_err());
}
