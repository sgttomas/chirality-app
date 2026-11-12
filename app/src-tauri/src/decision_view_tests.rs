//! Invented records only. No person performed any act recorded here: each act
//! record is a schema-checked claim standing for the record of a person's act,
//! written where the case needs it, and shows only how the reader reads it.
//! Expected states come from DEL-04-01 Person's acts, DEL-04-03 Record
//! authority, Correction and REQ-010, and DEL-06-02 Decision row and Several
//! decisions.
use super::*;
use crate::{records_store, schema_validation, util};
use std::path::PathBuf;

const LOG: &str = include_str!("../../tests/fixtures/FX-DP1/records/coordination.rs.jsonl");
const PACKAGE: &[u8] = include_bytes!("../../tests/fixtures/FX-DP1/project/decisions/PKG-1.json");
const PENDING: &str = "pending — awaiting the person's decision";

struct Fixture {
    root: PathBuf,
    project: PathBuf,
}
impl Fixture {
    fn new() -> Self {
        let root = std::env::temp_dir()
            .canonicalize()
            .unwrap()
            .join(util::opaque_id("decision-view-").unwrap());
        let project = root.join("project");
        std::fs::create_dir_all(project.join("decisions")).unwrap();
        std::fs::write(project.join("decisions/PKG-1.json"), PACKAGE).unwrap();
        std::fs::write(project.join("decisions/PKG-2.json"), b"{\"invented\":\"second package\"}").unwrap();
        records_store::use_store_for_test(Some(Ok(records_store::Store {
            root: root.join("store"),
            placement: records_store::Placement::Test,
            limits: vec![],
        })));
        Self { root, project }
    }
    /// The project's subtree in this installation's records store.
    fn store(&self) -> PathBuf {
        records_store::attach(&self.project, true).unwrap().dir.unwrap()
    }
    fn write(&self, dir: &Path, name: &str, entries: &[Value]) {
        let mut text = String::new();
        for (n, e) in entries.iter().enumerate() {
            let mut e = e.clone();
            e["seq"] = json!(n + 1);
            schema_validation::bundled().unwrap().validate(&e).unwrap();
            text += &(serde_json::to_string(&e).unwrap() + "\n");
        }
        std::fs::create_dir_all(dir).unwrap();
        std::fs::write(dir.join(format!("{name}.jsonl")), text).unwrap();
    }
    fn in_store(&self, name: &str, entries: &[Value]) {
        let dir = self.store().join("acts");
        self.write(&dir, name, entries);
    }
    fn view(&self) -> Value {
        derive(&self.project, &[])
    }
    fn row(&self, request: &str) -> Value {
        self.view()["rows"]
            .as_array()
            .unwrap()
            .iter()
            .find(|r| r["requests"].as_array().is_some_and(|v| v.iter().any(|id| id == request)) || r["package"] == request)
            .cloned()
            .unwrap_or(Value::Null)
    }
}
impl Drop for Fixture {
    fn drop(&mut self) {
        records_store::use_store_for_test(None);
        let _ = std::fs::remove_dir_all(&self.root);
    }
}
fn fixture_entries() -> Vec<Value> {
    LOG.lines().map(|l| serde_json::from_str(l).unwrap()).collect()
}
fn request(id: &str, file: &str, bytes: &[u8]) -> Value {
    let mut r = fixture_entries()[0].clone();
    r["recordId"] = json!(id);
    r["body"]["evidence"]["ref"] = json!(file);
    r["body"]["evidence"]["method"] = json!(util::FILE_IDENTITY_METHOD);
    r["body"]["evidence"]["claimedIdentity"] = json!(util::sha256_hex(bytes));
    r
}
fn act(id: &str, request: &str, alternative: &str, bytes: &[u8]) -> Value {
    let mut a = fixture_entries()[2].clone();
    a["recordId"] = json!(id);
    a["recorder"]["identity"] = json!(format!("writer:{id}"));
    a["body"]["decisionActor"] = json!({"displayName":"invented person; no person's act","osAccount":"invented","identityVerified":false});
    a["body"]["boundSubject"] = json!([format!("decision package {request}")]);
    a["body"]["boundContent"] = json!([{"method":util::FILE_IDENTITY_METHOD,"value":util::sha256_hex(bytes)}]);
    a["body"]["captureEvidence"][0]["ref"] = json!(format!("cap:{id}"));
    a["body"]["relations"]["requestRef"] = json!(request);
    a["body"]["relations"]["alternativeChosen"] = json!(alternative);
    a
}
fn correcting(mut entry: Value, id: &str, target: &str) -> Value {
    entry["recordId"] = json!(id);
    entry["corrects"] = json!(target);
    entry["correctionReason"] = json!("invented correction");
    entry
}

#[test]
fn decision_view_control_case_store_act_decides() {
    let f = Fixture::new();
    f.in_store("00-request", &[request("rec:r1", "decisions/PKG-1.json", PACKAGE)]);
    f.in_store("10-act", &[act("rec:a1", "rec:r1", "ALT-2", PACKAGE)]);
    let row = f.row("rec:r1");
    assert_eq!(row["state"], "decided", "{row}");
    assert_eq!(row["decision"]["origin"], "this installation's records store");
    assert_eq!(row["decision"]["actRecord"]["recorder"]["identity"], "writer:rec:a1");
}

#[test]
fn decision_view_project_file_act_decides_nothing() {
    // The store does not hold this project's records, so they are read in
    // place: an agent could have written every line.
    let f = Fixture::new();
    f.store();
    let place = f.project.join(".chirality/records/acts");
    f.write(&place, "00-request", &[request("rec:r1", "decisions/PKG-1.json", PACKAGE)]);
    f.write(&place, "10-act", &[act("rec:a1", "rec:r1", "ALT-2", PACKAGE)]);
    let row = f.row("rec:r1");
    assert_eq!(row["state"], PENDING, "{row}");
    assert_eq!(row["claims"][0]["origin"], "project-file claim");
    // Once the store holds the project's records, the project folder's copy is
    // not read at all.
    f.in_store("00-request", &[request("rec:r1", "decisions/PKG-1.json", PACKAGE)]);
    let row = f.row("rec:r1");
    assert_eq!(row["state"], PENDING, "{row}");
    assert_eq!(row["claims"], json!([]));
}

#[test]
fn decision_view_package_imported_act_decides_nothing() {
    let f = Fixture::new();
    f.in_store("00-request", &[request("rec:r1", "decisions/PKG-1.json", PACKAGE)]);
    f.in_store("10-act", &[act("rec:a1", "rec:r1", "ALT-2", PACKAGE)]);
    assert_eq!(f.row("rec:r1")["state"], "decided");
    let log = f.store().join("acts/10-act.jsonl");
    let bag = f.root.join("invented-package");
    crate::records_export::export(&f.project, &bag).unwrap();
    std::fs::remove_file(&log).unwrap();
    let actor = crate::act_control::person(Some("Invented package fixture"), Some("fixture-os"));
    let observed = json!({"fixture":"source-only package import stand-in; no live person's act"});
    let plan = records_store::package::prepare(&f.project, &bag, &actor, &observed).unwrap();
    records_store::package::apply(plan, &actor, &observed).unwrap();
    assert!(log.exists(), "the package import restored the act log");
    let row = f.row("rec:r1");
    assert_eq!(row["state"], PENDING, "{row}");
    assert_eq!(row["claims"][0]["origin"], "imported package record (quoted evidence)");
}

#[test]
fn decision_view_legacy_imported_act_decides_nothing() {
    let f = Fixture::new();
    f.store();
    let place = f.project.join(".chirality/records/acts");
    f.write(&place, "00-request", &[request("rec:r1", "decisions/PKG-1.json", PACKAGE)]);
    f.write(&place, "10-act", &[act("rec:a1", "rec:r1", "ALT-2", PACKAGE)]);
    records_store::import(&f.project).unwrap();
    let row = f.row("rec:r1");
    assert_eq!(row["state"], PENDING, "{row}");
    assert_eq!(row["claims"][0]["origin"], "legacy-imported copy of a project file (quoted evidence)");
    // An act the App later records in the store decides, beside the copies.
    f.in_store("20-later", &[act("rec:a2", "rec:r1", "ALT-1", PACKAGE)]);
    let row = f.row("rec:r1");
    assert_eq!(row["state"], "decided", "{row}");
    assert_eq!(row["decision"]["act"], "rec:a2");
}

#[test]
fn decision_view_record_naming_its_recorder_as_actor_is_not_an_act() {
    let f = Fixture::new();
    f.in_store("00-request", &[request("rec:r1", "decisions/PKG-1.json", PACKAGE)]);
    let mut a = act("rec:a1", "rec:r1", "ALT-2", PACKAGE);
    a["recorder"]["identity"] = json!("agent:invented-manager");
    a["body"]["decisionActor"] = json!({"displayName":"agent:invented-manager","identityVerified":false});
    f.in_store("10-act", &[a]);
    let row = f.row("rec:r1");
    assert_eq!(row["state"], PENDING, "{row}");
    assert!(row["limits"].to_string().contains("names its recorder"), "{row}");
}

#[test]
fn decision_view_correction_stands_in_place_of_the_act_it_corrects() {
    let alternative = |c: &mut Value| c["body"]["relations"]["alternativeChosen"] = json!("ALT-9");
    let kind = |c: &mut Value| {
        c["body"]["actKind"] = json!("A13");
        c["body"]["relations"].as_object_mut().unwrap().remove("alternativeChosen");
    };
    let other_request = |c: &mut Value| {
        c["body"]["relations"]["requestRef"] = json!("rec:r2");
        c["body"]["boundSubject"] = json!(["decision package rec:r2"]);
        c["body"]["relations"]["alternativeChosen"] = json!("ALT-1");
    };
    let changes: [(&str, &dyn Fn(&mut Value)); 3] =
        [("alternative", &alternative), ("kind", &kind), ("request", &other_request)];
    for (case, change) in changes {
        let f = Fixture::new();
        f.in_store("00-request", &[
            request("rec:r1", "decisions/PKG-1.json", PACKAGE),
            request("rec:r2", "decisions/PKG-2.json", b"{\"invented\":\"second package\"}"),
        ]);
        let original = act("rec:a1", "rec:r1", "ALT-2", PACKAGE);
        let mut correction = correcting(original.clone(), "rec:a1-fix", "rec:a1");
        change(&mut correction);
        f.in_store("10-act", &[original, correction]);
        let row = f.row("rec:r1");
        assert_eq!(row["state"], PENDING, "{case}: the corrected-away act no longer decides: {row}");
        assert!(row["contenders"].to_string().contains("rec:a1"), "{case}: both stay listed");
    }
}

#[test]
fn decision_view_corrected_request_is_not_decided_on_its_own() {
    let f = Fixture::new();
    let r1 = request("rec:r1", "decisions/PKG-1.json", PACKAGE);
    let r1b = correcting(r1.clone(), "rec:r1b", "rec:r1");
    f.in_store("00-request", &[r1, r1b]);
    f.in_store("10-act", &[act("rec:a1", "rec:r1", "ALT-2", PACKAGE)]);
    let view = f.view();
    let rows = view["rows"].as_array().unwrap();
    assert_eq!(rows.len(), 1, "one row for the one package: {view}");
    assert_eq!(rows[0]["package"], "rec:r1b");
    assert_eq!(rows[0]["correctedRequests"], json!(["rec:r1"]));
    assert_eq!(rows[0]["state"], PENDING, "{}", rows[0]);
}

#[test]
fn decision_view_opposing_requests_for_one_package_are_one_unresolved_row() {
    let f = Fixture::new();
    f.in_store("00-request", &[
        request("rec:r1", "decisions/PKG-1.json", PACKAGE),
        request("rec:r2", "decisions/PKG-1.json", PACKAGE),
    ]);
    f.in_store("10-a", &[act("rec:a1", "rec:r1", "ALT-1", PACKAGE)]);
    f.in_store("20-b", &[act("rec:a2", "rec:r2", "ALT-2", PACKAGE)]);
    let view = f.view();
    let rows = view["rows"].as_array().unwrap();
    assert_eq!(rows.len(), 1, "{view}");
    assert_eq!(rows[0]["requests"], json!(["rec:r1", "rec:r2"]));
    assert_eq!(rows[0]["state"], "ambiguous current standing", "{}", rows[0]);
}

#[test]
fn decision_view_matches_again_after_lapse_is_shown_as_such() {
    let f = Fixture::new();
    f.in_store("00-request", &[request("rec:r1", "decisions/PKG-1.json", PACKAGE)]);
    let a = act("rec:a1", "rec:r1", "ALT-2", PACKAGE);
    let lapse = json!({"format":"chirality.rs.record","formatVersion":"0.1","recordId":"rec:lapse","kind":"act_lapsed",
        "recorder":{"role":"App writer","identity":"writer:lapse"},"context":{"surface":"App"},"seq":1,"writtenAt":"invented",
        "body":{"act":{"recordId":"rec:a1","actKind":"A16","capturedAt":a["body"]["captureTime"],"capturingSurface":"app_act_control"},
            "state":"lapsed","referents":a["body"]["boundSubject"],"c0":a["body"]["boundContent"][0],
            "c1":{"method":util::FILE_IDENTITY_METHOD,"value":"changed-invented"},"time":"invented"}});
    f.in_store("10-act", &[a]);
    f.in_store("20-lapse", &[lapse]);
    assert_eq!(f.row("rec:r1")["decision"]["lapse"], "matches c0 again after observed lapse");
}

#[test]
fn decision_view_work_does_not_grow_with_unrelated_history() {
    let pairs = |unrelated: usize| {
        let f = Fixture::new();
        f.in_store("00-request", &[request("rec:r1", "decisions/PKG-1.json", PACKAGE)]);
        f.in_store("10-act", &[act("rec:a1", "rec:r1", "ALT-2", PACKAGE)]);
        let history: Vec<Value> = (0..unrelated)
            .map(|n| {
                // Other captured acts of the person, citing no decision package.
                let mut other = act(&format!("rec:other-{n}"), "rec:none", "ALT-1", PACKAGE);
                other["body"]["actKind"] = json!("A13");
                other["body"].as_object_mut().unwrap().remove("relations");
                other
            })
            .collect();
        f.in_store("30-history", &history);
        PAIRS.with(|p| p.set(0));
        let view = f.view();
        assert_eq!(view["rows"][0]["state"], "decided");
        (PAIRS.with(|p| p.get()), view["readScope"].clone())
    };
    let (small, _) = pairs(0);
    let (large, scope) = pairs(400);
    assert_eq!(small, large, "pairwise work is bounded by decision records");
    assert_eq!(scope["entriesRead"], 402);
    assert_eq!(scope["decisionRecords"], 2);
}

#[test]
fn decision_view_row_with_an_unread_act_line_is_not_plainly_decided() {
    let f = Fixture::new();
    f.in_store("00-request", &[request("rec:r1", "decisions/PKG-1.json", PACKAGE)]);
    f.in_store("10-act", &[act("rec:a1", "rec:r1", "ALT-2", PACKAGE)]);
    // Another log holds a line that cannot be read: it may be a correction of
    // the act or a later opposing decision.
    std::fs::write(f.store().join("acts/20-unreadable.jsonl"), b"{\"kind\":\"human_act\",\n").unwrap();
    let row = f.row("rec:r1");
    assert_eq!(row["state"], DECIDED_INCOMPLETE, "{row}");
    assert_eq!(row["decision"]["act"], "rec:a1", "the act is still shown");
    assert!(row["limits"].to_string().contains("act records not fully read: records-store:acts/20-unreadable.jsonl"), "{row}");
}

#[test]
fn decision_view_row_with_a_torn_act_log_is_not_plainly_pending() {
    let f = Fixture::new();
    f.in_store("00-request", &[request("rec:r1", "decisions/PKG-1.json", PACKAGE)]);
    // A torn final line, which may be the decision being written.
    std::fs::write(f.store().join("acts/10-torn.jsonl"), b"{\"format\":\"chirality.rs.record\"").unwrap();
    let row = f.row("rec:r1");
    assert_eq!(row["state"], PENDING_INCOMPLETE, "{row}");
    assert!(row["limits"].to_string().contains("10-torn.jsonl"), "{row}");
}
