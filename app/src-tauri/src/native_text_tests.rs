use super::*;
use serde_json::json;

const WITHHELD: Unfit = Unfit::Withhold(VALUE_NOT_SHOWN);
/// Values a supplier or a file could send: a line break, a direction override, an invisible
/// character, and a sentence imitating the App's.
fn poisoned() -> Vec<Value> {
    vec![
        json!("thr-1\nQuit proceeds; nothing is stopped."),
        json!("thr-1\u{202e}"),
        json!("thr-\u{200b}1"),
        json!("Quit proceeds; nothing is stopped."),
        json!(""),
        json!(null),
        json!({"id": "thr-1"}),
        json!(-1),
    ]
}
fn inline(p: Placed) -> String {
    match p {
        Placed::Inline(c) => c.to_string(),
        Placed::Lines(_) => panic!("Withhold never gives lines"),
    }
}
/// What a sheet may carry inside an App sentence.
fn closed_text(s: &str) -> bool {
    s.chars().all(|c| !c.is_control() && !matches!(c, '\u{200b}'..='\u{200f}' | '\u{202a}'..='\u{202e}' | '\u{2060}'..='\u{2069}' | '\u{feff}'))
}

#[test]
fn every_closed_function_withholds_a_poisoned_value() {
    let functions: [(&str, fn(&Value, Unfit) -> Placed); 4] = [("identifier", identifier), ("time", time), ("number", number), ("workflow_name", workflow_name)];
    for (name, f) in functions {
        for value in poisoned() {
            assert_eq!(inline(f(&value, WITHHELD)), VALUE_NOT_SHOWN, "{name}: {value}");
        }
    }
    for value in poisoned() {
        assert_eq!(inline(vocabulary(&value, supplier::TURN_STATUSES, WITHHELD)), VALUE_NOT_SHOWN, "vocabulary: {value}");
    }
}

#[test]
fn a_value_in_its_closed_form_is_given_back_as_written() {
    for (value, shown) in [(json!("019a-thread_1.2:x/y"), "019a-thread_1.2:x/y"), (json!(42), "42")] {
        assert_eq!(inline(identifier(&value, WITHHELD)), shown);
    }
    assert_eq!(inline(identifier(&json!("x".repeat(128)), WITHHELD)), "x".repeat(128));
    assert_eq!(inline(identifier(&json!("x".repeat(129)), WITHHELD)), VALUE_NOT_SHOWN);
    assert_eq!(inline(time(&json!("2026-11-14T12:00:00.5+01:00"), WITHHELD)), "2026-11-14T12:00:00.5+01:00");
    assert_eq!(inline(time(&json!("today"), WITHHELD)), VALUE_NOT_SHOWN);
    assert_eq!(inline(number(&json!(10), WITHHELD)), "10");
    assert_eq!(inline(number(&json!("10"), WITHHELD)), VALUE_NOT_SHOWN);
    assert_eq!(inline(workflow_name(&json!("invented-flow-2"), WITHHELD)), "invented-flow-2");
    assert_eq!(inline(workflow_name(&json!("Invented Flow"), WITHHELD)), VALUE_NOT_SHOWN);
}

#[test]
fn a_known_value_becomes_the_apps_word_and_an_unknown_one_is_withheld() {
    const TABLE: &[(&str, &str)] = &[("inProgress", "in progress")];
    assert_eq!(inline(vocabulary(&json!("inProgress"), TABLE, WITHHELD)), "in progress");
    assert_eq!(inline(vocabulary(&json!("InProgress"), TABLE, Unfit::Withhold(CODEX_VALUE_NOT_SHOWN))), CODEX_VALUE_NOT_SHOWN);
}

#[test]
fn every_word_this_module_can_give_is_closed() {
    for table in [supplier::TURN_STATUSES, supplier::AGENT_STATUSES, supplier::SERVER_REQUEST_METHODS, app::HOST_STATES, app::HOME_CLASSES] {
        for (value, word) in table {
            assert!(closed_text(value) && closed_text(word), "{value} / {word}");
        }
    }
    assert!(closed_text(CODEX_VALUE_NOT_SHOWN) && closed_text(VALUE_NOT_SHOWN));
}

#[test]
fn the_supplier_tables_are_the_pinned_schemas_own_and_the_home_classes_the_apps() {
    let read = |file: &str| -> Value {
        let path = std::path::Path::new(env!("CARGO_MANIFEST_DIR")).join("resources/supplier/0.167.0").join(file);
        serde_json::from_slice(&std::fs::read(path).unwrap()).unwrap()
    };
    let values = |table: &[(&str, &str)]| -> std::collections::BTreeSet<String> { table.iter().map(|(v, _)| v.to_string()).collect() };
    let names = |v: &Value| -> std::collections::BTreeSet<String> { v.as_array().unwrap().iter().map(|s| s.as_str().unwrap().to_owned()).collect() };
    let v2 = read("codex_app_server_protocol.v2.schemas.json");
    assert_eq!(names(&v2["definitions"]["TurnStatus"]["enum"]), values(supplier::TURN_STATUSES));
    assert_eq!(names(&v2["definitions"]["CollabAgentStatus"]["enum"]), values(supplier::AGENT_STATUSES));
    let all = read("codex_app_server_protocol.schemas.json");
    let methods: std::collections::BTreeSet<String> = all["definitions"]["ServerRequest"]["oneOf"].as_array().unwrap().iter()
        .flat_map(|v| v["properties"]["method"]["enum"].as_array().cloned().unwrap_or_default())
        .map(|m| m.as_str().unwrap().to_owned())
        .collect();
    assert_eq!(methods, values(supplier::SERVER_REQUEST_METHODS));
    use crate::home_resources::HomeClass;
    let classes: std::collections::BTreeSet<String> = [HomeClass::Account, HomeClass::ApiKey, HomeClass::LocalProvider, HomeClass::Probe].iter().map(|c| c.as_str().to_owned()).collect();
    assert_eq!(classes, values(app::HOME_CLASSES));
}
