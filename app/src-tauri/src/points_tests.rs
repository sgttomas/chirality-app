//! DEL-02-03 REQ-008: the point tool's definition, argument check, digest,
//! record body, pointer, receipt, framing and the reader's soundness and
//! version rules, read against independent expectations.
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
    for needed in ["Give only the terms the person stated", "Leave out every field the person did not state", "does not pause you",
        "tell the person plainly that no point was recorded", "A sign-off point names its act in reservedAct, engineering approval or professional reliance",
        "could not establish whether the point was recorded"] {
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

/// PRD V4-AUT-07: a sign-off point always names its act, engineering approval
/// or professional reliance; version 1 refuses one that does not, with the
/// App's sentence, and the schema the record is checked against refuses it too.
#[test]
fn a_sign_off_point_that_names_neither_of_its_acts_is_refused() {
    for act in SIGN_OFF_ACTS { assert!(validate(&args(json!({"kind":"sign-off","reservedAct":act}))).is_ok(), "{act}"); }
    for value in [args(json!({"kind":"sign-off"})), args(json!({"kind":"sign-off","reservedAct":"accepting a proposal"})), args(json!({"kind":"sign-off","reservedAct":"marking work checked"}))] {
        assert_eq!(validate(&value).unwrap_err(), SIGN_OFF_UNNAMED, "{value}");
        // The schema alone (the record schema's copy) refuses it as well.
        assert!(validator().unwrap().iter_errors(&value).next().is_some(), "{value}");
    }
    // Another kind may name a reserved act, or none.
    assert!(validate(&args(json!({"kind":"review","reservedAct":"accepting a proposal"}))).is_ok());
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
    Source { home: "app-home:fixture".into(), home_class: "H-acct".into(), generation: crate::recovery::generation_ref(&json!({"appSession":"s","home":"app-home:fixture","spawnCounter":1})).unwrap(), thread: "thread".into(), turn: "turn".into(), call: "call".into(), request: json!(7) }
}
fn entry(arguments: &Value, point: &str, record: &str, seq: u64, previous: Option<&str>) -> Value {
    let body = record_body(point, &source(), "/project", "records-project:fixture", &run_none(), &observed(None, false), arguments, &digest(arguments).unwrap(), "2026-11-18T00:00:00Z");
    let mut e = crate::records::envelope(KIND, &crate::records::APP_WRITER, body, record.into(), seq, None, None);
    e["prevLine"] = crate::record_lines::link(previous);
    e
}

#[test]
fn the_record_body_is_closed_and_its_pointer_holds_identities_and_the_digest_only() {
    let arguments = args(json!({"whoMustRespond":"MARKER-TERM the reviewer","kind":"review"}));
    let point = crate::util::opaque_id("pt-").unwrap();
    let e = crate::records::envelope(KIND, &crate::records::APP_WRITER,
        record_body(&point, &source(), "/project", "records-project:fixture", &run_in("run:workflow:x"), &observed(Some("req:1"), true), &arguments, &digest(&arguments).unwrap(), "2026-11-18T00:00:00Z"),
        RECORD.into(), 1, None, None);
    let validator = crate::schema_validation::bundled().unwrap();
    validator.validate(&e).unwrap();
    // The schema refuses a body carrying anything else, prose in the run or
    // observation, or arguments outside version 1.
    for (case, change) in [
        ("extra field", Box::new(|b: &mut Value| b["note"] = json!("x")) as Box<dyn Fn(&mut Value)>),
        ("run prose", Box::new(|b: &mut Value| b["run"] = json!({"state":"no run","reason":"free prose"}))),
        ("run reason outside the codes", Box::new(|b: &mut Value| b["run"] = json!({"state":"not established","reason":"free prose"}))),
        ("observation prose", Box::new(|b: &mut Value| b["observed"]["turnStartLimit"] = json!("free prose"))),
        ("person press without its request", Box::new(|b: &mut Value| { b["observed"]["turnStart"] = json!("person-press"); b["observed"].as_object_mut().unwrap().remove("requestRef"); })),
        ("request named without a person press", Box::new(|b: &mut Value| { b["observed"]["turnStart"] = json!("not-observed"); b["observed"]["requestRef"] = json!("req:1"); })),
        ("no store project", Box::new(|b: &mut Value| { b.as_object_mut().unwrap().remove("storeProject"); })),
        ("arguments outside version 1", Box::new(|b: &mut Value| b["arguments"]["assignee"] = json!("x"))),
        ("unnamed sign-off", Box::new(|b: &mut Value| b["arguments"] = json!({"version":1,"operation":"place","kind":"sign-off"}))),
    ] {
        let mut changed = e.clone();
        change(&mut changed["body"]);
        assert!(validator.validate(&changed).is_err(), "{case}");
    }
    let raw = pointer(&e).unwrap();
    assert!(!raw.contains("MARKER-TERM"), "the pointer carries no supplied text");
    let decoded = decode(&raw).unwrap();
    let keys: Vec<&str> = decoded.as_object().unwrap().keys().map(String::as_str).collect();
    assert_eq!(keys, ["digest", "kind", "point", "project", "record", "source", "storeProject", "v"]);
    assert_eq!(decoded["point"], json!(point));
    assert_eq!(decoded["record"], RECORD);
    assert_eq!(decoded["source"], source().value());
    assert_eq!(decoded["storeProject"], "records-project:fixture");
    assert_eq!(decoded["digest"], json!({"method":DIGEST_METHOD,"value":digest(&arguments).unwrap()}));
    // Anything else of this owner is not a pointer: a run or observation carried, an older shape, another version.
    for raw in ["{\"v\":2,\"kind\":\"placed\"}", "run:abc"] { assert!(decode(raw).is_none(), "{raw}"); }
    let mut with_run = decoded.clone();
    with_run["run"] = json!({"state":"no run"});
    assert!(decode(&with_run.to_string()).is_none());
    // Finding 6: every part of the tag is checked.
    let changed = |change: &dyn Fn(&mut Value)| { let mut v = decoded.clone(); change(&mut v); decode(&v.to_string()) };
    assert!(changed(&|v| v["digest"]["extra"] = json!(1)).is_none(), "an extra digest key");
    assert!(changed(&|v| v["digest"]["value"] = json!(digest(&arguments).unwrap().to_uppercase())).is_none(), "an uppercase digest");
    assert!(changed(&|v| v["digest"]["value"] = json!("z".repeat(64))).is_none(), "a digest that is not hexadecimal");
    assert!(changed(&|v| v["point"] = json!("pt-not-a-uuid")).is_none());
    assert!(changed(&|v| v["record"] = json!("rec:app:fixture")).is_none());
    assert!(changed(&|v| v["source"]["generation"] = Value::Null).is_none());
    assert!(changed(&|v| v["source"]["generation"] = json!(crate::recovery::generation_ref(&json!({"appSession":"s","home":"another-home","spawnCounter":1})).unwrap())).is_none(), "a generation of another home");
    assert!(changed(&|v| v["source"]["homeClass"] = json!("H-other")).is_none());
    let generation = source().generation;
    let offer = offer_pointer("app-home:fixture", &generation, "thread");
    assert!(decode(&offer).is_some());
    let bound = bound_offer_pointer("app-home:fixture", &generation, "thread", "/project", "records-project:fixture");
    assert_eq!(decode(&bound).unwrap()["storeProject"], "records-project:fixture");
    let offer: Value = serde_json::from_str(&offer).unwrap();
    for (case, change) in [
        ("generation null", Box::new(|v: &mut Value| v["generation"] = Value::Null) as Box<dyn Fn(&mut Value)>),
        ("generation of another home", Box::new(|v: &mut Value| v["generation"] = json!(crate::recovery::generation_ref(&json!({"appSession":"s","home":"other","spawnCounter":1})).unwrap()))),
        ("generation not canonical", Box::new(|v: &mut Value| v["generation"] = json!("gen:v1:s:73:h:68:n:01"))),
        ("definition not a digest", Box::new(|v: &mut Value| v["definition"] = json!("x"))),
        ("store project without its project", Box::new(|v: &mut Value| v["storeProject"] = json!("records-project:fixture"))),
    ] {
        let mut v = offer.clone();
        change(&mut v);
        assert!(decode(&v.to_string()).is_none(), "{case}");
    }
}
const RECORD: &str = "rec:app:00000000-0000-4000-8000-000000000001";

#[test]
fn a_receipt_is_recorded_not_recorded_or_not_established_and_carries_no_answer() {
    let run = run_in("run:1");
    let text = |r: &Value| -> Value { serde_json::from_str(r["contentItems"][0]["text"].as_str().unwrap()).unwrap() };
    let recorded = receipt(&Outcome::Recorded { point: "pt-1".into(), persistence: KEPT.into(), run: run.clone() }, &run_none());
    assert_eq!(recorded["success"], true);
    assert_eq!(text(&recorded)["state"], "recorded");
    assert_eq!(text(&recorded)["point"], "pt-1");
    assert_eq!(text(&recorded)["run"], run, "the run of the record");
    let refused = receipt(&Outcome::NotRecorded { reason: "No App project is known for this conversation, so the point could not be kept; no point was placed.".into() }, &run);
    assert_eq!(refused["success"], false);
    assert_eq!(text(&refused)["state"], "not recorded");
    assert!(text(&refused)["point"].is_null());
    let unknown = receipt(&Outcome::NotEstablished { point: Some("pt-2".into()), reason: not_established("the write reported x") }, &run);
    assert_eq!(unknown["success"], false);
    assert_eq!(text(&unknown)["state"], "not established");
    assert_eq!(text(&unknown)["point"], "pt-2");
    assert!(text(&unknown)["reason"].as_str().unwrap().starts_with("The App could not establish whether the point was recorded (the write reported x)."));
    assert!(pointer_pending("ledger refused").contains("the conversation's pointer to them could not be saved (ledger refused); the App completes it before a later placement in this conversation or when the conversation is resumed"));
}

#[test]
fn only_a_request_framed_as_a_point_call_is_one() {
    let call = json!({"id":"1","method":"item/tool/call","params":{"threadId":"t","turnId":"u","callId":"c","tool":TOOL,"namespace":null,"arguments":{}}});
    assert!(frame_ok(&call));
    let mut with_jsonrpc = call.clone();
    with_jsonrpc["jsonrpc"] = json!("2.0");
    assert!(frame_ok(&with_jsonrpc));
    for (case, change) in [
        ("a result beside the method", Box::new(|f: &mut Value| f["result"] = json!({})) as Box<dyn Fn(&mut Value)>),
        ("an error beside the method", Box::new(|f: &mut Value| f["error"] = json!({}))),
        ("no call identity", Box::new(|f: &mut Value| { f["params"].as_object_mut().unwrap().remove("callId"); })),
        ("an empty turn", Box::new(|f: &mut Value| f["params"]["turnId"] = json!(""))),
        ("no arguments", Box::new(|f: &mut Value| { f["params"].as_object_mut().unwrap().remove("arguments"); })),
        ("an object as the id", Box::new(|f: &mut Value| f["id"] = json!({}))),
        ("another tool", Box::new(|f: &mut Value| f["params"]["tool"] = json!("other"))),
        ("a protocol version of false", Box::new(|f: &mut Value| f["jsonrpc"] = json!(false))),
        ("a protocol version other than 2.0", Box::new(|f: &mut Value| f["jsonrpc"] = json!("1.0"))),
    ] {
        let mut f = call.clone();
        change(&mut f);
        assert!(!frame_ok(&f), "{case}");
    }
}

/// The reader: a W-0 fragment set aside is a note, not a limit, so a later
/// sound record still reads; a broken line is a limit for what follows it.
#[test]
fn a_fragment_the_writer_set_aside_does_not_block_later_records_but_a_broken_line_does() {
    let root = std::env::temp_dir().canonicalize().unwrap().join(crate::util::opaque_id("point-reader-").unwrap());
    std::fs::create_dir_all(&root).unwrap();
    let log = root.join("points.jsonl");
    let a = args(json!({"label":"A"}));
    crate::records::append_reserved(&log, KIND, &crate::records::APP_WRITER, record_body("pt-00000000-0000-0000-0000-000000000001", &source(), "/project", "records-project:fixture", &run_none(), &observed(None, false), &a, &digest(&a).unwrap(), "t"),
        "rec:app:a".into(), None, None, crate::records::RecordSet::Complete, crate::schema_validation::bundled()).unwrap();
    let mut bytes = std::fs::read(&log).unwrap();
    bytes.extend_from_slice(b"{\"torn\":");
    std::fs::write(&log, &bytes).unwrap();
    let torn = LogReading::read(&log).unwrap();
    assert_eq!(torn.tail, Tail::Fragment);
    assert!(!torn.whole());
    let mut later = source();
    later.call = "call-2".into();
    let b = args(json!({"label":"B"}));
    crate::records::append_reserved(&log, KIND, &crate::records::APP_WRITER, record_body("pt-00000000-0000-0000-0000-000000000002", &later, "/project", "records-project:fixture", &run_none(), &observed(None, false), &b, &digest(&b).unwrap(), "t"),
        "rec:app:b".into(), None, None, crate::records::RecordSet::Complete, crate::schema_validation::bundled()).unwrap();
    let read = LogReading::read(&log).unwrap();
    assert_eq!(read.set_aside, 1, "the writer set the fragment aside (W-0)");
    assert!(read.limits.is_empty(), "{:?}", read.limits);
    assert!(read.whole());
    assert_eq!(read.lines.len(), 2);
    assert!(read.lines.iter().enumerate().all(|(i, _)| read.soundness(i).is_ok()));
    // A broken line in the middle limits the records after it, not before.
    let text = std::fs::read_to_string(&log).unwrap();
    let mut lines: Vec<String> = text.lines().map(str::to_owned).collect();
    lines.insert(1, "not a record".into());
    std::fs::write(&log, lines.join("\n") + "\n").unwrap();
    let read = LogReading::read(&log).unwrap();
    assert!(!read.limits.is_empty());
    assert!(read.soundness(0).is_ok());
    assert!(read.soundness(1).as_ref().unwrap_err().contains("not whole at or before"), "{:?}", read.soundness(1));
    std::fs::remove_dir_all(root).unwrap();
}

/// DEL-04-03 REQ-012 for the point reader, as far as these entries show it:
/// with only the version string changed, an entry of an unknown major version
/// is refused and nothing is inferred from it, and one of a newer minor
/// version is read as far as known and marked so. A newer entry that also
/// carries a field today's schema does not know is refused before this rule
/// is reached, by the store's line reader (shown through the host in
/// hosting_points_tests); corrections of points are not built, so a
/// `corrects` relation is not applied.
#[test]
fn the_point_reader_applies_the_records_version_rule() {
    let root = std::env::temp_dir().canonicalize().unwrap().join(crate::util::opaque_id("point-versions-").unwrap());
    std::fs::create_dir_all(&root).unwrap();
    let log = root.join("points.jsonl");
    let a = args(json!({"label":"A"}));
    let write = |version: &str| {
        let mut e = entry(&a, "pt-00000000-0000-0000-0000-000000000001", "rec:app:a", 1, None);
        e["formatVersion"] = json!(version);
        std::fs::write(&log, serde_json::to_string(&e).unwrap() + "\n").unwrap();
        LogReading::read(&log).unwrap()
    };
    let known = write("0.1");
    assert_eq!(known.lines.len(), 1);
    assert!(known.lines[0].newer.is_none());
    let newer = write("0.2");
    assert_eq!(newer.lines.len(), 1, "a newer minor version is read as far as known");
    assert_eq!(newer.lines[0].newer.as_deref(), Some("0.2"));
    assert!(newer.soundness(0).is_ok());
    for version in ["9.0", "1.1"] {
        let refused = write(version);
        assert!(refused.lines.is_empty(), "{version}: nothing is inferred from it");
        assert_eq!(refused.refused.len(), 1, "{version}");
        assert!(refused.refused[0].1.contains(&format!("format version {version}")), "{:?}", refused.refused);
        assert!(!refused.whole());
    }
    std::fs::remove_dir_all(root).unwrap();
}

/// One soundness check: unique by point reference, by record identity and by
/// call source, and the digest recomputed.
#[test]
fn a_record_is_sound_only_when_unique_by_every_identity_and_its_digest_holds() {
    let a = args(json!({"label":"A"}));
    let b = args(json!({"label":"B"}));
    let read = |entries: Vec<Value>| {
        let mut bytes = Vec::new();
        let mut previous: Option<String> = None;
        for mut e in entries {
            e["prevLine"] = crate::record_lines::link(previous.as_deref());
            let line = serde_json::to_vec(&e).unwrap();
            previous = Some(crate::record_lines::line_identity(&line));
            bytes.extend(line);
            bytes.push(b'\n');
        }
        LogReading::of_bytes(std::path::Path::new("points.jsonl"), &bytes)
    };
    let mut second = source();
    second.call = "call-2".into();
    let other = |point: &str, record: &str, src: &Source, arguments: &Value, seq: u64| {
        let body = record_body(point, src, "/project", "records-project:fixture", &run_none(), &observed(None, false), arguments, &digest(arguments).unwrap(), "t");
        crate::records::envelope(KIND, &crate::records::APP_WRITER, body, record.into(), seq, None, None)
    };
    let p1 = "pt-00000000-0000-0000-0000-000000000001";
    let p2 = "pt-00000000-0000-0000-0000-000000000002";
    let fine = read(vec![other(p1, "rec:app:a", &source(), &a, 1), other(p2, "rec:app:b", &second, &b, 2)]);
    assert!(fine.soundness(0).is_ok() && fine.soundness(1).is_ok(), "{:?} {:?}", fine.soundness(0), fine.soundness(1));
    let same_record = read(vec![other(p1, "rec:app:a", &source(), &a, 1), other(p2, "rec:app:a", &second, &b, 2)]);
    assert!(same_record.soundness(0).as_ref().unwrap_err().contains("record identity more than once"));
    let same_point = read(vec![other(p1, "rec:app:a", &source(), &a, 1), other(p1, "rec:app:b", &second, &b, 2)]);
    assert!(same_point.soundness(0).as_ref().unwrap_err().contains("point's reference more than once"));
    let same_call = read(vec![other(p1, "rec:app:a", &source(), &a, 1), other(p2, "rec:app:b", &source(), &b, 2)]);
    assert!(same_call.soundness(1).as_ref().unwrap_err().contains("more than one record for this call"));
    let mut altered = other(p1, "rec:app:a", &source(), &a, 1);
    altered["body"]["arguments"]["label"] = json!("changed");
    let bad_digest = read(vec![altered]);
    assert!(bad_digest.soundness(0).as_ref().unwrap_err().contains("do not match their recorded digest"));
}
