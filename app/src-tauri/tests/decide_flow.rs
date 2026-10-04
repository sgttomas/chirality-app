//! Steps 2-4: the person decides a decision package through the App act control
//! (A16 "decide"), the RS record is written to a file, and the decision view shows it.
//!
//! Content is the Pass 4 fixture FX-DP1 (run APP-V4-DESIGN-PASS-4-20261003, E/),
//! copied into a scratch workspace; the fixture itself is only read.
//! Schema validation of what this test writes is in ../tests/validate-records.test.mjs
//! (Ajv, JSON Schema 2020-12), which runs this test first.
//!
//! The person's native confirmation cannot be pressed by a test. Here the test calls
//! the control's `confirm` with `InputSource::HostNativeConfirmation`, standing in
//! for the person pressing "Decide" in the host's native dialog (lib.rs `decide`).
//! That stand-in exists only in test code; the App exposes no such path (NA-1).

use chirality_app_v4_lib::act_control::{person, ActControl, InputSource, CAPTURE_STORE};
use chirality_app_v4_lib::canonical::offer_digest;
use chirality_app_v4_lib::decision_view::derive;
use chirality_app_v4_lib::recorder::{identify_packages, LOG};
use chirality_app_v4_lib::records::read_log;
use chirality_app_v4_lib::util::sha256_hex;
use serde_json::{json, Value};
use std::path::{Path, PathBuf};

fn fixture() -> PathBuf {
    PathBuf::from(env!("CARGO_MANIFEST_DIR"))
        .join("../../execution/_Coordination/AgentRuns/APP-V4-DESIGN-PASS-4-20261003/E/fixtures/FX-DP1")
}

fn scratch_workspace() -> PathBuf {
    let out = std::process::Command::new("mktemp").args(["-d", "/private/tmp/cxws.XXXXXX"]).output().unwrap();
    let ws = PathBuf::from(String::from_utf8(out.stdout).unwrap().trim());
    std::fs::create_dir_all(ws.join("project/decisions")).unwrap();
    for f in ["PKG-1.json", "PKG-2.json"] {
        std::fs::copy(fixture().join("project/decisions").join(f), ws.join("project/decisions").join(f)).unwrap();
    }
    ws
}

fn fixture_log() -> Vec<Value> {
    read_log(&fixture().join("records/coordination.rs.jsonl")).0
}

fn without(v: &Value, keys: &[&str]) -> Value {
    let mut v = v.clone();
    for k in keys {
        v.as_object_mut().unwrap().remove(*k);
    }
    v
}

fn hashes(root: &Path) -> Vec<(String, String)> {
    let mut v = Vec::new();
    for d in ["project/decisions", "records"] {
        if let Ok(rd) = std::fs::read_dir(root.join(d)) {
            for e in rd.flatten() {
                v.push((e.path().display().to_string(), sha256_hex(&std::fs::read(e.path()).unwrap())));
            }
        }
    }
    v.sort();
    v
}

#[test]
fn view_model_reads_the_pass4_fixture() {
    // The Pass 4 decision view's result on FX-DP1, reproduced by this view model.
    let before = hashes(&fixture());
    let v = derive(&fixture(), &["records/coordination.rs.jsonl"]);
    assert_eq!(hashes(&fixture()), before, "DV-9: deriving writes nothing");
    let rows = v["rows"].as_array().unwrap();
    assert_eq!(rows.len(), 2);
    assert_eq!(rows[0]["state"], "decided");
    assert_eq!(rows[0]["decision"]["alternativeChosen"], "ALT-2");
    assert_eq!(rows[0]["decision"]["lapse"], "not lapsed");
    assert_eq!(rows[0]["decision"]["decidedBy"], "Engineer A / enga (identity not verified)");
    assert_eq!(rows[0]["decision"]["recordedBy"], "App interface (capturing surface) app-interface:local");
    // PKG-2 stays pending although the agent's message claims a decision (CAP-7, DV inputs).
    assert_eq!(rows[1]["state"], "pending — awaiting the person's decision");
    assert!(rows.iter().all(|r| r["limits"].as_array().unwrap().is_empty()));
}

#[test]
fn offer_digest_matches_pass4_fixture() {
    // AAC §5.1 aac-offer-digest/0.1 over ü, ≈ and U+2028 (E1-R4 parity).
    let offer: Value = serde_json::from_slice(&std::fs::read(fixture().join("aac/offer-PKG-1.json")).unwrap()).unwrap();
    assert_eq!(offer_digest(&offer).unwrap(), offer["offerDigest"]["value"].as_str().unwrap());
}

#[test]
fn person_decides_a_package_and_the_view_shows_it() {
    let ws = scratch_workspace();
    let fx = fixture_log();

    // The recorder identifies the two package files (RS §13.6 mapping).
    let reqs = identify_packages(&ws).unwrap();
    assert_eq!(reqs.len(), 2);
    for (mine, theirs) in reqs.iter().zip(fx.iter().take(2)) {
        assert_eq!(mine["recordId"], theirs["recordId"]);
        assert_eq!(without(&mine["body"], &["time", "requester"]), without(&theirs["body"], &["time", "requester"]),
                   "act_request body equals Pass 4's, apart from time and requester identity");
    }
    assert!(identify_packages(&ws).unwrap().is_empty(), "the same bytes are not requested twice");

    let v = derive(&ws, &[LOG]);
    assert!(v["rows"].as_array().unwrap().iter().all(|r| r["state"] == "pending — awaiting the person's decision"));

    // AI-9 / AX-01: the person opens the control on PKG-1's pending row.
    let mut ac = ActControl::new(&ws);
    let offer = ac.compose_a16("rec:app:coord:0001").unwrap();
    let fx_offer: Value = serde_json::from_slice(&std::fs::read(fixture().join("aac/offer-PKG-1.json")).unwrap()).unwrap();
    let skip = ["offerId", "composedAt", "offerDigest"];
    assert_eq!(without(&offer, &skip), without(&fx_offer, &skip), "offer equals Pass 4's, apart from id, time, digest");
    assert_eq!(offer_digest(&offer).unwrap(), offer["offerDigest"]["value"].as_str().unwrap());
    let oid = offer["offerId"].as_str().unwrap().to_string();

    let actor = person(Some("Engineer A"), Some("enga"));
    // Refusals: AX-04 automation sources; capture from AC-1; an alternative the package does not name.
    for src in [InputSource::WebviewScript, InputSource::AgentTool, InputSource::AppRule] {
        let e = ac.confirm(&oid, "ALT-2", src, actor.clone()).unwrap_err();
        assert!(e.starts_with("not operable from"), "{e}");
    }
    assert!(ac.confirm(&oid, "ALT-2", InputSource::HostNativeConfirmation, actor.clone()).unwrap_err().contains("not presented"));
    ac.present(&oid).unwrap();
    assert!(ac.confirm(&oid, "ALT-9", InputSource::HostNativeConfirmation, actor.clone()).is_err());
    assert!(!ws.join(CAPTURE_STORE).exists(), "nothing captured by a refused operation");
    let text = ac.confirmation_text(&oid, "ALT-2", &actor).unwrap();
    assert!(text.contains("Hold stage 2 until the version check returns") && text.contains("identity not verified"));

    // The person confirms ALT-2 in the native confirmation (stand-in; see the file comment).
    let out = ac.confirm(&oid, "ALT-2", InputSource::HostNativeConfirmation, actor.clone()).unwrap();
    assert_eq!(out["state"], "AC-7 recorded");
    let rec = out["record"].clone();
    let cap = out["capture"].clone();
    assert_eq!(rec["kind"], "human_act");
    assert_eq!(rec["seq"], 3);
    assert_eq!(cap["recordId"], rec["recordId"]);
    let fx_act = &fx[2];
    let bskip = ["captureEvidence", "captureTime"];
    assert_eq!(without(&rec["body"], &bskip), without(&fx_act["body"], &bskip), "human_act body equals Pass 4's, apart from capture ref and time");
    assert_eq!(rec["recorder"], fx_act["recorder"]);
    // A second capture from the same offer is refused.
    assert!(ac.confirm(&oid, "ALT-1", InputSource::HostNativeConfirmation, actor.clone()).is_err());

    // Step 4: the decision view shows the recorded decision.
    let before = hashes(&ws);
    let v = derive(&ws, &[LOG]);
    assert_eq!(hashes(&ws), before, "DV-9");
    let row = &v["rows"][0];
    assert_eq!(row["state"], "decided");
    assert_eq!(row["decision"]["act"], rec["recordId"]);
    assert_eq!(row["decision"]["alternativeChosen"], "ALT-2");
    assert_eq!(row["decision"]["statement"], "Hold stage 2 until the version check returns, then start");
    assert_eq!(row["decision"]["decidedBy"], "Engineer A / enga (identity not verified)");
    assert_eq!(row["decision"]["recordingMode"], "direct capture");
    assert_eq!(row["decision"]["lapse"], "not lapsed");
    assert_eq!(v["rows"][1]["state"], "pending — awaiting the person's decision");

    // AK-c / AX-06: PKG-2 changes after its offer is shown: nothing captured.
    let o2 = ac.compose_a16("rec:app:coord:0002").unwrap();
    let o2id = o2["offerId"].as_str().unwrap().to_string();
    ac.present(&o2id).unwrap();
    let p2 = ws.join("project/decisions/PKG-2.json");
    let mut b = std::fs::read(&p2).unwrap();
    b.extend_from_slice(b" ");
    std::fs::write(&p2, &b).unwrap();
    let e = ac.confirm(&o2id, "ALT-1", InputSource::HostNativeConfirmation, actor.clone()).unwrap_err();
    assert!(e.contains("content changed"), "{e}");
    let (entries, _) = read_log(&ws.join(LOG));
    assert_eq!(entries.len(), 3, "no record written for the stale offer");

    // Write outputs for the schema test before the lapse case changes PKG-1.
    let out_dir = PathBuf::from(env!("CARGO_TARGET_TMPDIR")).join("skeleton-output");
    std::fs::create_dir_all(&out_dir).unwrap();
    std::fs::write(out_dir.join("decide-records.jsonl"), std::fs::read(ws.join(LOG)).unwrap()).unwrap();
    std::fs::write(out_dir.join("decide-offer.json"), serde_json::to_vec_pretty(&offer).unwrap()).unwrap();
    std::fs::write(out_dir.join("decide-capture.json"), serde_json::to_vec_pretty(&cap).unwrap()).unwrap();
    std::fs::write(out_dir.join("decide-view.json"), serde_json::to_vec_pretty(&v).unwrap()).unwrap();
    std::fs::write(out_dir.join("decide-package-files.json"), serde_json::to_vec_pretty(&json!([
        serde_json::from_slice::<Value>(&std::fs::read(ws.join("project/decisions/PKG-1.json")).unwrap()).unwrap()
    ])).unwrap()).unwrap();

    // DV-7: PKG-1 edited after the decision shows lapsed; the decision is not hidden.
    let p1 = ws.join("project/decisions/PKG-1.json");
    let mut b = std::fs::read(&p1).unwrap();
    b.extend_from_slice(b" ");
    std::fs::write(&p1, &b).unwrap();
    let v = derive(&ws, &[LOG]);
    assert_eq!(v["rows"][0]["state"], "decided");
    assert_eq!(v["rows"][0]["decision"]["lapse"], "lapsed — the package changed after the decision");
}
