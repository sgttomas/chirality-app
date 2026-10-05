//! Actual decision-view consumer with synthetic native events and recorded claims.
//! No real person presses native confirmation in this suite.
mod common;
use chirality_app_v4_lib::{
    act_control::{person, ActControl, InputSource},
    decision_view::derive,
    recorder::identify_packages,
    records, util,
};
use common::ScratchDirectory;
use serde_json::{json, Value};
fn workspace() -> ScratchDirectory {
    let ws = ScratchDirectory::new("decision-standing");
    std::fs::create_dir_all(ws.join("project/decisions")).unwrap();
    let src = std::path::Path::new(env!("CARGO_MANIFEST_DIR"))
        .join("../tests/fixtures/FX-DP1/project/decisions/PKG-1.json");
    std::fs::copy(src, ws.join("project/decisions/PKG-1.json")).unwrap();
    ws
}
fn decide(ws: &std::path::Path) -> (ActControl, Value) {
    let mut requests = identify_packages(ws).unwrap();
    if requests.is_empty() {
        requests = chirality_app_v4_lib::storage::read_all(ws)
            .0
            .into_iter()
            .filter(|e| e["kind"] == "act_request")
            .collect();
    }
    let req = requests.remove(0);
    let mut c = ActControl::new(ws);
    let offer = c.compose_a16(req["recordId"].as_str().unwrap()).unwrap();
    let id = offer["offerId"].as_str().unwrap();
    let actor = person(Some("fixture person"), Some("fixture account"));
    c.confirmation_text(id, "ALT-1", &actor).unwrap();
    c.present(id).unwrap();
    let result = c
        .confirm(id, "ALT-1", InputSource::HostNativeConfirmation, actor)
        .unwrap();
    (c, result)
}
fn row(ws: &std::path::Path) -> Value {
    derive(ws, &[])["rows"][0].clone()
}
fn rewrite_claim(ws: &std::path::Path, mutate: impl Fn(&mut Value)) {
    let paths = chirality_app_v4_lib::storage::discover(ws).unwrap();
    for path in paths {
        let (mut entries, limits) = records::read_log(&path);
        assert!(limits.is_empty());
        for e in &mut entries {
            if e["kind"] == "human_act" {
                mutate(e);
                chirality_app_v4_lib::schema_validation::bundled()
                    .unwrap()
                    .validate(e)
                    .unwrap();
            }
        }
        let text = entries
            .iter()
            .map(|e| serde_json::to_string(e).unwrap() + "\n")
            .collect::<String>();
        std::fs::write(path, text).unwrap();
    }
}
#[test]
fn new_writes_use_selected_exact_buffer_method_and_no_normalization() {
    let ws = workspace();
    let bytes = std::fs::read(ws.join("project/decisions/PKG-1.json")).unwrap();
    let req = identify_packages(&ws).unwrap().remove(0);
    assert_eq!(
        req["body"]["evidence"]["method"],
        "chirality.app.exact-bytes.sha256/v1"
    );
    assert_eq!(
        req["body"]["evidence"]["claimedIdentity"],
        util::sha256_hex(&bytes)
    );
    let (_, captured) = decide(&ws);
    assert_eq!(
        captured["capture"]["boundContent"][0]["method"],
        util::FILE_IDENTITY_METHOD
    );
    assert_eq!(row(&ws)["decision"]["lapse"], "not lapsed");
    let mut extra = bytes.clone();
    extra.push(b'\n');
    assert_ne!(
        util::package_snapshot(&bytes).unwrap().1,
        util::package_snapshot(&extra).unwrap().1
    );
}
#[test]
fn same_value_different_method_is_incomparable_and_claim_remains_unverified() {
    let ws = workspace();
    let (_, original) = decide(&ws);
    rewrite_claim(&ws, |e| {
        e["body"]["boundContent"][0]["method"] = "fixture.other-method".into();
        e["body"]["captureEvidence"][0]["ref"] = "cap:altered-valid-claim".into();
    });
    let r = row(&ws);
    assert_eq!(r["decision"]["lapse"], "unknown (incomparable)");
    assert_eq!(
        r["decision"]["standingComparison"]["bound"]["value"],
        original["capture"]["boundContent"][0]["value"]
    );
    assert!(r["decision"]["captureProvenance"]
        .as_str()
        .unwrap()
        .contains("native capture origin not verified"));
    assert_eq!(
        r["decision"]["decidedBy"],
        "fixture person / fixture account (identity not verified)"
    );
    assert!(!r["limits"].as_array().unwrap().is_empty());
}
#[test]
fn different_subject_or_scope_never_becomes_current_standing() {
    for scope in [false, true] {
        let ws = workspace();
        decide(&ws);
        rewrite_claim(&ws, |e| {
            if scope {
                e["body"]["scope"] = "other scope".into();
            } else {
                e["body"]["boundSubject"][0] = "decision package rec:other".into();
            }
        });
        assert_eq!(row(&ws)["decision"]["lapse"], "unknown (incomparable)");
    }
}
#[test]
fn absent_and_unreadable_are_distinct_and_derivation_writes_nothing() {
    let ws = workspace();
    decide(&ws);
    let p = ws.join("project/decisions/PKG-1.json");
    std::fs::remove_file(&p).unwrap();
    assert_eq!(row(&ws)["decision"]["lapse"], "lapsed (subject absent)");
    std::fs::create_dir(&p).unwrap();
    assert_eq!(row(&ws)["decision"]["lapse"], "unknown (unavailable)");
    let logs = chirality_app_v4_lib::storage::discover(&ws).unwrap();
    let before: Vec<_> = logs.iter().map(|p| std::fs::read(p).unwrap()).collect();
    derive(&ws, &[]);
    assert_eq!(
        before,
        logs.iter()
            .map(|p| std::fs::read(p).unwrap())
            .collect::<Vec<_>>()
    );
}
fn lapse_record(ws: &std::path::Path, act: &Value, reference: &str) -> Value {
    let subject = act["body"]["boundSubject"][0].as_str().unwrap();
    records::append_project(ws,None,"fixture-observer","act_lapsed",&records::APP_WRITER,json!({
        "act":{"recordId":reference,"actKind":"A16","capturedAt":act["body"]["captureTime"],"capturingSurface":"app_act_control"},
        "state":"lapsed","referents":[subject],"c0":act["body"]["boundContent"][0],
        "c1":{"method":util::FILE_IDENTITY_METHOD,"value":util::file_identity(&ws.join("project/decisions/PKG-1.json")).unwrap()},"time":"fixture-observation-time"
    })).unwrap()
}
#[test]
fn restoration_uses_only_existing_referent_bound_act_lapsed_history() {
    let ws = workspace();
    let (_, result) = decide(&ws);
    let act = &result["record"];
    let package = ws.join("project/decisions/PKG-1.json");
    let original = std::fs::read(&package).unwrap();
    let mut changed = original.clone();
    changed.push(b'\n');
    std::fs::write(&package, &changed).unwrap();
    assert_eq!(
        row(&ws)["decision"]["lapse"],
        "lapsed — the package changed after the decision"
    );
    lapse_record(&ws, act, "rec:unrelated");
    std::fs::write(&package, &original).unwrap();
    assert_eq!(row(&ws)["decision"]["lapse"], "not lapsed");
    std::fs::write(&package, &changed).unwrap();
    let event = lapse_record(&ws, act, act["recordId"].as_str().unwrap());
    std::fs::write(&package, &original).unwrap();
    let r = row(&ws);
    assert_eq!(
        r["decision"]["lapse"],
        "matches c0 again after observed lapse"
    );
    assert_eq!(r["decision"]["lapseHistory"], json!([event["recordId"]]));
    assert!(r["decision"]["captureProvenance"]
        .as_str()
        .unwrap()
        .contains("recorded claim"));
}
#[test]
fn historical_test_value_bytes_and_method_remain_unchanged() {
    let src = std::path::Path::new(env!("CARGO_MANIFEST_DIR")).join("../tests/fixtures/FX-DP1");
    let log = src.join("records/coordination.rs.jsonl");
    let before = std::fs::read(&log).unwrap();
    let view = derive(&src, &["records/coordination.rs.jsonl"]);
    assert_eq!(
        view["rows"][0]["decision"]["lapse"],
        "unknown (incomparable)"
    );
    assert_eq!(
        view["rows"][0]["decision"]["standingComparison"]["bound"]["method"],
        util::LEGACY_FILE_IDENTITY_METHOD
    );
    assert_eq!(std::fs::read(log).unwrap(), before);
}
#[test]
fn synthetic_control_failures_and_cold_replay_boundary_are_unchanged() {
    let ws = workspace();
    let req = identify_packages(&ws).unwrap().remove(0);
    let mut c = ActControl::new(&ws);
    let o = c.compose_a16(req["recordId"].as_str().unwrap()).unwrap();
    let id = o["offerId"].as_str().unwrap();
    let a = person(Some("fixture"), Some("account"));
    c.confirmation_text(id, "ALT-1", &a).unwrap();
    c.present(id).unwrap();
    assert!(c
        .confirm(id, "ALT-1", InputSource::WebviewScript, a.clone())
        .is_err());
    let p = ws.join("project/decisions/PKG-1.json");
    let mut bytes = std::fs::read(&p).unwrap();
    bytes.push(b'\n');
    std::fs::write(&p, bytes).unwrap();
    assert!(c
        .confirm(id, "ALT-1", InputSource::HostNativeConfirmation, a)
        .is_err());
    let (entries, _) = chirality_app_v4_lib::storage::read_all(&ws);
    assert!(!entries.iter().any(|e| e["kind"] == "human_act"));
    // No file-derived claim is imported into the native capture map or admission types.
    let fresh = ActControl::new(&ws);
    assert!(fresh.offers.is_empty());
}
#[test]
fn schema_valid_cold_capture_cannot_mint_a_human_act() {
    let ws = workspace();
    let (_, result) = decide(&ws);
    let mut capture = result["capture"].clone();
    capture.as_object_mut().unwrap().remove("recordId");
    let paths = chirality_app_v4_lib::storage::discover(&ws).unwrap();
    for path in paths {
        let entries = records::read_log(&path).0;
        let text = entries
            .into_iter()
            .filter(|e| e["kind"] != "human_act")
            .map(|e| serde_json::to_string(&e).unwrap() + "\n")
            .collect::<String>();
        std::fs::write(path, text).unwrap();
    }
    let capture_path =
        chirality_app_v4_lib::storage::capture_path(&ws, capture["captureId"].as_str().unwrap());
    std::fs::write(capture_path, serde_json::to_vec(&capture).unwrap()).unwrap();
    let mut cold = ActControl::new(&ws);
    let recovered = cold.recover_pending().unwrap();
    assert!(recovered.iter().any(|r| r["state"] == "AC-8 record pending"
        && r["originLimit"]
            .as_str()
            .is_some_and(|s| s == "capture origin not verified; automatic act replay held")));
    let (entries, _) = chirality_app_v4_lib::storage::read_all(&ws);
    assert!(!entries.iter().any(|e| e["kind"] == "human_act"));
}
#[test]
fn contradictory_schema_valid_lapse_claim_is_visible_and_not_restoration_proof() {
    let ws = workspace();
    let (_, result) = decide(&ws);
    let act = &result["record"];
    // Valid shape but c1 equals c0: the recorded state word alone proves no lapse.
    lapse_record(&ws, act, act["recordId"].as_str().unwrap());
    let r = row(&ws);
    assert_eq!(r["decision"]["lapse"], "not lapsed");
    assert_eq!(r["decision"]["lapseHistory"], json!([]));
    assert!(r["limits"]
        .as_array()
        .unwrap()
        .iter()
        .any(|l| l.as_str().unwrap().contains("not used as lapse history")));
}
