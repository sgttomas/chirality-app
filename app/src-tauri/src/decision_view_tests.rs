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
    // The row says first that the reading is incomplete, and its state is
    // neither of the two plain ones.
    let state = row["state"].as_str().unwrap();
    assert!(state.starts_with("act records incomplete"), "{row}");
    assert!(state != "decided" && state != PENDING, "{row}");
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
    // The row says first that the reading is incomplete, and its state is
    // neither of the two plain ones.
    let state = row["state"].as_str().unwrap();
    assert!(state.starts_with("act records incomplete"), "{row}");
    assert!(state != "decided" && state != PENDING, "{row}");
    assert!(row["limits"].to_string().contains("10-torn.jsonl"), "{row}");
}

// Review of #247. Expected states come from the rule App Agent 0 decided:
// only an act record held in this installation's records store, outside every
// imported part, can decide; a record naming its recorder as the decision
// actor decides nothing; a record that cannot decide changes no standing in
// either direction; while any act log is not fully read, no row is decided or
// pending. States are written here as the reader's words, not its constants.

/// A record brought into the store by the explicit legacy import.
fn legacy(f: &Fixture, name: &str, entries: &[Value]) {
    let place = f.project.join(".chirality/records/acts");
    f.write(&place, name, entries);
    records_store::import(&f.project).unwrap();
    assert!(f.store().join(format!("acts/{name}.jsonl")).exists());
}
fn self_recorded(mut record: Value, recorder: &str, actor: &str) -> Value {
    record["recorder"]["identity"] = json!(recorder);
    record["body"]["decisionActor"] = json!({"displayName":actor,"identityVerified":false});
    record
}
fn lapse_record(id: &str, act: &Value, state: &str, c1: Value) -> Value {
    json!({"format":"chirality.rs.record","formatVersion":"0.1","recordId":id,"kind":"act_lapsed",
        "recorder":{"role":"App writer","identity":"writer:lapse"},"context":{"surface":"App"},"seq":1,"writtenAt":"invented",
        "body":{"act":{"recordId":act["recordId"],"actKind":"A16","capturedAt":act["body"]["captureTime"],"capturingSurface":"app_act_control"},
            "state":state,"referents":act["body"]["boundSubject"],"c0":act["body"]["boundContent"][0],"c1":c1,"time":"invented"}})
}
fn not_decided(row: &Value) -> bool {
    row["state"] != "decided" && row["decision"].is_null()
}

#[test]
fn decision_view_a_correction_that_may_not_decide_changes_no_standing() {
    // Two unordered store acts leave the row unresolved. A correction of one
    // of them that is a legacy-imported copy, or that names its recorder as
    // the decision actor, must not remove it and leave the other deciding.
    for case in ["legacy-imported", "recorder-as-actor"] {
        let f = Fixture::new();
        f.in_store("00-request", &[request("rec:r1", "decisions/PKG-1.json", PACKAGE)]);
        f.in_store("10-a", &[act("rec:a1", "rec:r1", "ALT-1", PACKAGE)]);
        f.in_store("11-b", &[act("rec:a2", "rec:r1", "ALT-2", PACKAGE)]);
        assert_eq!(f.row("rec:r1")["state"], "ambiguous current standing");
        let mut fix = correcting(act("rec:a2", "rec:r1", "ALT-9", PACKAGE), "rec:a2-fix", "rec:a2");
        fix["body"]["captureEvidence"][0]["ref"] = json!("cap:a2-fix");
        if case == "legacy-imported" {
            legacy(&f, "20-fix", &[fix]);
        } else {
            f.in_store("20-fix", &[self_recorded(fix, "agent:invented-manager", "agent:invented-manager")]);
        }
        let row = f.row("rec:r1");
        assert_eq!(row["state"], "ambiguous current standing", "{case}: {row}");
        let claim = row["claims"].as_array().unwrap().iter().find(|c| c["recordId"] == "rec:a2-fix");
        assert!(claim.is_some(), "{case}: the correction is listed as a claim: {row}");
    }
}

#[test]
fn decision_view_a_correction_of_a_correction_obeys_the_same_rule() {
    // A store act; a legacy-imported correction of it, which changes nothing;
    // a store correction of that imported correction. Two store acts remain,
    // unordered: never decided by either.
    let f = Fixture::new();
    f.in_store("00-request", &[request("rec:r1", "decisions/PKG-1.json", PACKAGE)]);
    f.in_store("10-a", &[act("rec:a1", "rec:r1", "ALT-2", PACKAGE)]);
    let mut imported = correcting(act("rec:a1", "rec:r1", "ALT-9", PACKAGE), "rec:a1-fix", "rec:a1");
    imported["body"]["captureEvidence"][0]["ref"] = json!("cap:a1-fix");
    legacy(&f, "20-imported-fix", &[imported]);
    let mut local = correcting(act("rec:a1-fix", "rec:r1", "ALT-1", PACKAGE), "rec:a1-fix2", "rec:a1-fix");
    local["body"]["captureEvidence"][0]["ref"] = json!("cap:a1-fix2");
    f.in_store("30-local-fix", &[local]);
    let row = f.row("rec:r1");
    assert!(not_decided(&row), "{row}");
}

#[test]
fn decision_view_a_request_correction_that_may_not_decide_leaves_the_request_standing() {
    let f = Fixture::new();
    let r1 = request("rec:r1", "decisions/PKG-1.json", PACKAGE);
    f.in_store("00-request", &[r1.clone()]);
    f.in_store("10-a", &[act("rec:a1", "rec:r1", "ALT-2", PACKAGE)]);
    legacy(&f, "20-imported-request-fix", &[correcting(r1, "rec:r1-fix", "rec:r1")]);
    let row = f.row("rec:r1");
    assert_eq!(row["correctedRequests"], json!([]), "{row}");
    assert_eq!(row["state"], "decided", "{row}");
    assert_eq!(row["decision"]["act"], "rec:a1");
}

#[test]
fn decision_view_a_corrected_lapse_observation_is_no_lapse_history() {
    // A store lapse observation, then a store correction of it to "unknown
    // (unavailable)": the corrected observation decides the lapse state no more.
    let f = Fixture::new();
    f.in_store("00-request", &[request("rec:r1", "decisions/PKG-1.json", PACKAGE)]);
    let a = act("rec:a1", "rec:r1", "ALT-2", PACKAGE);
    f.in_store("10-a", &[a.clone()]);
    let observed = lapse_record("rec:lapse", &a, "lapsed", json!({"method":util::FILE_IDENTITY_METHOD,"value":"changed-invented"}));
    f.in_store("20-lapse", &[observed.clone()]);
    assert_eq!(f.row("rec:r1")["decision"]["lapse"], "matches c0 again after observed lapse");
    let mut fix = correcting(observed.clone(), "rec:lapse-fix", "rec:lapse");
    fix["body"]["state"] = json!("unknown (unavailable)");
    fix["body"]["c1"] = a["body"]["boundContent"][0].clone();
    f.in_store("30-lapse-fix", &[fix.clone()]);
    assert_eq!(f.row("rec:r1")["decision"]["lapse"], "not lapsed");
    // A lapse observation, or a correction of one, that may not change
    // standing changes nothing.
    let g = Fixture::new();
    g.in_store("00-request", &[request("rec:r1", "decisions/PKG-1.json", PACKAGE)]);
    g.in_store("10-a", &[a.clone()]);
    g.in_store("20-lapse", &[observed]);
    legacy(&g, "30-imported-lapse-fix", &[fix]);
    assert_eq!(g.row("rec:r1")["decision"]["lapse"], "matches c0 again after observed lapse");
    let h = Fixture::new();
    h.in_store("00-request", &[request("rec:r1", "decisions/PKG-1.json", PACKAGE)]);
    h.in_store("10-a", &[a.clone()]);
    legacy(&h, "20-imported-lapse", &[lapse_record("rec:lapse", &a, "lapsed", json!({"method":util::FILE_IDENTITY_METHOD,"value":"changed-invented"}))]);
    let row = h.row("rec:r1");
    assert_eq!(row["decision"]["lapse"], "not lapsed", "{row}");
    assert!(row["claims"].to_string().contains("rec:lapse"), "{row}");
}

#[test]
fn decision_view_an_act_decides_only_the_package_identity_its_request_claims() {
    // The request claims other content than the act was bound to, by value
    // and by method: the row is unresolved, never decided.
    for case in ["value", "method"] {
        let f = Fixture::new();
        let mut r1 = request("rec:r1", "decisions/PKG-1.json", PACKAGE);
        if case == "value" {
            r1["body"]["evidence"]["claimedIdentity"] = json!("invented-other-content");
        } else {
            r1["body"]["evidence"]["method"] = json!("invented method");
        }
        f.in_store("00-request", &[r1]);
        f.in_store("10-a", &[act("rec:a1", "rec:r1", "ALT-2", PACKAGE)]);
        let row = f.row("rec:r1");
        assert!(not_decided(&row), "{case}: {row}");
        assert!(row["state"].as_str().unwrap().starts_with("unresolved"), "{case}: {row}");
        assert!(row["limits"].to_string().contains("package identity"), "{case}: {row}");
    }
    // Two requests for one file differing only in content identity: one act
    // cannot make both read decided.
    let f = Fixture::new();
    let mut r2 = request("rec:r2", "decisions/PKG-1.json", PACKAGE);
    r2["body"]["evidence"]["claimedIdentity"] = json!("invented-other-content");
    f.in_store("00-request", &[request("rec:r1", "decisions/PKG-1.json", PACKAGE), r2]);
    f.in_store("10-a", &[act("rec:a1", "rec:r1", "ALT-2", PACKAGE)]);
    f.in_store("11-b", &[act("rec:a2", "rec:r2", "ALT-2", PACKAGE)]);
    let view = f.view();
    let decided = view["rows"].as_array().unwrap().iter().filter(|r| r["state"] == "decided").count();
    assert!(decided <= 1, "{view}");
    assert!(not_decided(&f.row("rec:r2")));
}

#[test]
fn decision_view_a_record_naming_its_recorder_as_actor_is_listed_as_a_claim() {
    let f = Fixture::new();
    f.in_store("00-request", &[request("rec:r1", "decisions/PKG-1.json", PACKAGE)]);
    f.in_store("10-a", &[self_recorded(act("rec:a1", "rec:r1", "ALT-2", PACKAGE), "agent:invented-manager", "agent:invented-manager")]);
    let view = f.view();
    println!("DECISION_VIEW_CLAIM_DTO:{view}");
    let row = f.row("rec:r1");
    let claim = row["claims"].as_array().unwrap().iter().find(|c| c["recordId"] == "rec:a1").cloned();
    let claim = claim.unwrap_or_else(|| panic!("listed as a claim: {row}"));
    assert!(claim["reason"].as_str().unwrap().contains("names its recorder"), "{claim}");
    assert_eq!(claim["alternativeChosen"], "ALT-2");
    assert_eq!(claim["recordedBy"]["identity"], "agent:invented-manager");
    assert!(claim["actor"].as_str().unwrap().contains("agent:invented-manager"));
}

#[test]
fn decision_view_incomplete_act_records_lead_every_row_and_establish_no_lapse() {
    let f = Fixture::new();
    f.in_store("00-request", &[request("rec:r1", "decisions/PKG-1.json", PACKAGE)]);
    f.in_store("10-a", &[act("rec:a1", "rec:r1", "ALT-2", PACKAGE)]);
    std::fs::write(f.store().join("acts/90-unreadable.jsonl"), b"garbage\n").unwrap();
    let row = f.row("rec:r1");
    assert!(row["state"].as_str().unwrap().starts_with("act records incomplete; "), "{row}");
    assert_ne!(row["decision"]["lapse"], "not lapsed", "no lapse state while incomplete: {row}");
    assert!(row["decision"]["lapse"].as_str().unwrap().contains("not established"), "{row}");
    assert!(row["decision"]["currentBytesObservation"].as_str().unwrap().contains("observation"), "{row}");
    // Unordered acts with an unread line: the heading leads with the incompleteness.
    f.in_store("11-b", &[act("rec:a2", "rec:r1", "ALT-1", PACKAGE)]);
    let row = f.row("rec:r1");
    let state = row["state"].as_str().unwrap();
    assert!(state.starts_with("act records incomplete; ") && state.contains("ambiguous"), "{row}");
}

#[test]
fn decision_view_recorder_as_actor_is_compared_with_unicode_case_folding() {
    let f = Fixture::new();
    f.in_store("00-request", &[request("rec:r1", "decisions/PKG-1.json", PACKAGE)]);
    f.in_store("10-a", &[self_recorded(act("rec:a1", "rec:r1", "ALT-2", PACKAGE), "AGENT:ÉQUIPE", "agent:équipe")]);
    let row = f.row("rec:r1");
    assert!(not_decided(&row), "{row}");
}

#[test]
fn decision_view_never_shows_an_identity_as_verified() {
    let f = Fixture::new();
    f.in_store("00-request", &[request("rec:r1", "decisions/PKG-1.json", PACKAGE)]);
    let mut a = act("rec:a1", "rec:r1", "ALT-2", PACKAGE);
    a["body"]["decisionActor"]["identityVerified"] = json!(true);
    f.in_store("10-a", &[a]);
    let by = f.row("rec:r1")["decision"]["decidedBy"].as_str().unwrap().to_owned();
    assert!(by.contains("identity not verified"), "{by}");
    assert!(by.contains("claims"), "the record's own claim is reported as a claim: {by}");
}

#[test]
fn decision_view_an_import_record_that_is_present_but_not_readable_whole_establishes_no_origin() {
    for case in ["empty", "torn", "not-an-event"] {
        let f = Fixture::new();
        f.in_store("00-request", &[request("rec:r1", "decisions/PKG-1.json", PACKAGE)]);
        legacy(&f, "10-act", &[act("rec:a1", "rec:r1", "ALT-2", PACKAGE)]);
        let imports = f.store().join("imports.jsonl");
        let original = std::fs::read(&imports).unwrap();
        match case {
            "empty" => std::fs::write(&imports, b"").unwrap(),
            "torn" => std::fs::write(&imports, &original[..original.len() - 1]).unwrap(),
            _ => std::fs::write(&imports, [&original[..], b"{}\n"].concat()).unwrap(),
        }
        let row = f.row("rec:r1");
        assert!(not_decided(&row), "{case}: {row}");
    }
}
