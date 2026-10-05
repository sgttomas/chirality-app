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

mod common;
use common::{evidence_output, ScratchDirectory};

use chirality_app_v4_lib::act_control::{person, ActControl, InputSource, CAPTURE_STORE};
use chirality_app_v4_lib::canonical::offer_digest;
use chirality_app_v4_lib::decision_view::derive;
use chirality_app_v4_lib::recorder::{identify_packages, LOG};
use chirality_app_v4_lib::records::read_log;
use chirality_app_v4_lib::util::{sha256_hex, LEGACY_FILE_IDENTITY_METHOD};

const SELECTED_FILE_METHOD: &str = "chirality.app.exact-bytes.sha256/v1";
use serde_json::{json, Value};
use std::path::{Path, PathBuf};

fn fixture() -> PathBuf {
    PathBuf::from(env!("CARGO_MANIFEST_DIR")).join("../tests/fixtures/FX-DP1")
}

fn scratch_workspace() -> ScratchDirectory {
    let ws = ScratchDirectory::new("cxws");
    std::fs::create_dir_all(ws.join("project/decisions")).unwrap();
    for f in ["PKG-1.json", "PKG-2.json"] {
        std::fs::copy(
            fixture().join("project/decisions").join(f),
            ws.join("project/decisions").join(f),
        )
        .unwrap();
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
    fn census(root: &Path, path: &Path, out: &mut Vec<(String, String)>) {
        if path.is_dir() {
            let mut children = std::fs::read_dir(path)
                .unwrap()
                .map(|e| e.unwrap().path())
                .collect::<Vec<_>>();
            children.sort();
            for child in children {
                census(root, &child, out);
            }
        } else if path.is_file() {
            out.push((
                path.strip_prefix(root).unwrap().display().to_string(),
                sha256_hex(&std::fs::read(path).unwrap()),
            ));
        }
    }
    let mut out = vec![];
    for dir in ["project/decisions", "records", ".chirality"] {
        let path = root.join(dir);
        if path.exists() {
            census(root, &path, &mut out);
        }
    }
    out.sort();
    out
}

#[test]
fn view_model_reads_the_pass4_fixture() {
    // Preserve Pass 4 recorded claims; selected current methods do not relabel old identities.
    let before = hashes(&fixture());
    let v = derive(&fixture(), &["records/coordination.rs.jsonl"]);
    assert_eq!(hashes(&fixture()), before, "DV-9: deriving writes nothing");
    let rows = v["rows"].as_array().unwrap();
    assert_eq!(rows.len(), 2);
    assert_eq!(rows[0]["state"], "decided");
    assert_eq!(rows[0]["decision"]["alternativeChosen"], "ALT-2");
    assert_eq!(rows[0]["decision"]["lapse"], "unknown (incomparable)");
    assert_eq!(
        rows[0]["decision"]["standingComparison"]["bound"],
        fixture_log()[2]["body"]["boundContent"][0]
    );
    assert_eq!(
        rows[0]["decision"]["standingComparison"]["bound"]["method"],
        LEGACY_FILE_IDENTITY_METHOD
    );
    assert_eq!(
        rows[0]["decision"]["standingComparison"]["current"],
        json!({"method":SELECTED_FILE_METHOD,"value":sha256_hex(&std::fs::read(fixture().join("project/decisions/PKG-1.json")).unwrap())})
    );
    assert_eq!(
        rows[0]["decision"]["decidedBy"],
        "Engineer A / enga (identity not verified)"
    );
    assert_eq!(
        rows[0]["decision"]["recordedBy"],
        "App interface (capturing surface) app-interface:local"
    );
    // PKG-2 stays pending although the agent's message claims a decision (CAP-7, DV inputs).
    assert_eq!(rows[1]["state"], "pending — awaiting the person's decision");
    assert_eq!(rows[0]["limits"],json!([
        "package request identity method is incomparable with current observed method; historical identities are not relabelled",
        "recorded act and current file identity are incomparable; no lapse or current human-act standing established"
    ]));
    assert_eq!(rows[1]["limits"],json!([
        "package request identity method is incomparable with current observed method; historical identities are not relabelled"
    ]));
}

#[test]
fn offer_digest_matches_pass4_fixture() {
    // AAC §5.1 aac-offer-digest/0.1 over ü, ≈ and U+2028 (E1-R4 parity).
    let offer: Value =
        serde_json::from_slice(&std::fs::read(fixture().join("aac/offer-PKG-1.json")).unwrap())
            .unwrap();
    assert_eq!(
        offer_digest(&offer).unwrap(),
        offer["offerDigest"]["value"].as_str().unwrap()
    );
}

#[test]
fn person_decides_a_package_and_the_view_shows_it() {
    let ws = scratch_workspace();
    let fx = fixture_log();

    // The recorder identifies the two package files (RS §13.6 mapping).
    let reqs = identify_packages(&ws).unwrap();
    assert_eq!(reqs.len(), 2);
    for (mine, theirs) in reqs.iter().zip(fx.iter().take(2)) {
        assert!(mine["recordId"].as_str().unwrap().starts_with("rec:app:"));
        let bytes =
            std::fs::read(ws.join(mine["body"]["evidence"]["ref"].as_str().unwrap())).unwrap();
        let exact_digest = sha256_hex(&bytes);
        assert_eq!(mine["body"]["evidence"]["method"], SELECTED_FILE_METHOD);
        assert_eq!(mine["body"]["evidence"]["claimedIdentity"], exact_digest);
        assert_eq!(
            theirs["body"]["evidence"]["method"],
            LEGACY_FILE_IDENTITY_METHOD
        );
        assert_eq!(
            theirs["body"]["evidence"]["claimedIdentity"],
            format!("sha256:{exact_digest}")
        );
        assert_eq!(
            without(&mine["body"]["evidence"], &["method", "claimedIdentity"]),
            without(&theirs["body"]["evidence"], &["method", "claimedIdentity"]),
            "evidence reference/shape is preserved while methods remain distinct"
        );
        assert_eq!(
            without(&mine["body"], &["time", "requester", "evidence"]),
            without(&theirs["body"], &["time", "requester", "evidence"]),
            "remaining act_request body equals Pass 4's, apart from time and requester identity"
        );
    }
    assert!(
        identify_packages(&ws).unwrap().is_empty(),
        "the same bytes are not requested twice"
    );

    let v = derive(&ws, &[LOG]);
    assert!(v["rows"]
        .as_array()
        .unwrap()
        .iter()
        .all(|r| r["state"] == "pending — awaiting the person's decision"));

    // AI-9 / AX-01: the person opens the control on PKG-1's pending row.
    let mut ac = ActControl::new(&ws);
    let offer = ac
        .compose_a16(reqs[0]["recordId"].as_str().unwrap())
        .unwrap();
    let fx_offer: Value =
        serde_json::from_slice(&std::fs::read(fixture().join("aac/offer-PKG-1.json")).unwrap())
            .unwrap();
    let exact_digest = sha256_hex(&std::fs::read(ws.join("project/decisions/PKG-1.json")).unwrap());
    assert_eq!(
        offer["subject"]["contentIdentity"],
        json!({"method":SELECTED_FILE_METHOD,"value":exact_digest})
    );
    assert_eq!(
        fx_offer["subject"]["contentIdentity"],
        json!({"method":LEGACY_FILE_IDENTITY_METHOD,"value":format!("sha256:{exact_digest}")})
    );
    assert_eq!(
        without(&offer["subject"], &["contentIdentity"]),
        without(&fx_offer["subject"], &["contentIdentity"]),
        "same package subject; historical identity is not relabelled"
    );
    let skip = [
        "offerId",
        "composedAt",
        "offerDigest",
        "requestRef",
        "subject",
    ];
    assert_eq!(
        without(&offer, &skip),
        without(&fx_offer, &skip),
        "remaining offer shape equals Pass 4's, apart from id, time, digest and request reference"
    );
    assert_eq!(
        offer_digest(&offer).unwrap(),
        offer["offerDigest"]["value"].as_str().unwrap()
    );
    let oid = offer["offerId"].as_str().unwrap().to_string();

    let actor = person(Some("Engineer A"), Some("enga"));
    // Refusals: AX-04 automation sources; capture from AC-1; an alternative the package does not name.
    for src in [
        InputSource::WebviewScript,
        InputSource::AgentTool,
        InputSource::AppRule,
    ] {
        let e = ac.confirm(&oid, "ALT-2", src, actor.clone()).unwrap_err();
        assert!(e.starts_with("not operable from"), "{e}");
    }
    assert!(ac
        .confirm(
            &oid,
            "ALT-2",
            InputSource::HostNativeConfirmation,
            actor.clone()
        )
        .unwrap_err()
        .contains("not presented"));
    ac.confirmation_text(&oid, "ALT-2", &actor).unwrap();
    ac.present(&oid).unwrap();
    assert!(ac
        .confirm(
            &oid,
            "ALT-9",
            InputSource::HostNativeConfirmation,
            actor.clone()
        )
        .is_err());
    assert!(
        !ws.join(CAPTURE_STORE).exists(),
        "nothing captured by a refused operation"
    );
    let text = ac.confirmation_text(&oid, "ALT-2", &actor).unwrap();
    assert!(
        text.contains("Hold stage 2 until the version check returns")
            && text.contains("identity not verified")
    );

    // The person confirms ALT-2 in the native confirmation (stand-in; see the file comment).
    let out = ac
        .confirm(
            &oid,
            "ALT-2",
            InputSource::HostNativeConfirmation,
            actor.clone(),
        )
        .unwrap();
    assert_eq!(out["state"], "AC-7 recorded");
    let rec = out["record"].clone();
    let cap = out["capture"].clone();
    assert_eq!(rec["kind"], "human_act");
    assert_eq!(rec["seq"], 5);
    assert_eq!(cap["recordId"], rec["recordId"]);
    let fx_act = &fx[2];
    assert_eq!(
        rec["body"]["boundContent"],
        json!([{"method":SELECTED_FILE_METHOD,"value":exact_digest}])
    );
    assert_eq!(cap["boundContent"], rec["body"]["boundContent"]);
    assert_eq!(
        fx_act["body"]["boundContent"],
        json!([{"method":LEGACY_FILE_IDENTITY_METHOD,"value":format!("sha256:{exact_digest}")}])
    );
    let bskip = [
        "boundContent",
        "captureEvidence",
        "captureTime",
        "relations",
        "boundSubject",
    ];
    assert_eq!(
        rec["body"]["boundSubject"],
        json!([format!(
            "decision package {}",
            reqs[0]["recordId"].as_str().unwrap()
        )])
    );
    assert_eq!(rec["body"]["relations"]["requestRef"], reqs[0]["recordId"]);
    assert_eq!(
        rec["body"]["relations"]["alternativeChosen"],
        fx[2]["body"]["relations"]["alternativeChosen"]
    );
    assert_eq!(
        without(&rec["body"], &bskip),
        without(&fx_act["body"], &bskip),
        "remaining human_act body equals Pass 4's; selected and historical boundContent were checked separately"
    );
    assert_eq!(rec["recorder"], fx_act["recorder"]);
    // A second capture from the same offer is refused.
    assert!(ac
        .confirm(
            &oid,
            "ALT-1",
            InputSource::HostNativeConfirmation,
            actor.clone()
        )
        .is_err());

    // Step 4: the decision view shows the recorded decision.
    let before = hashes(&ws);
    let v = derive(&ws, &[LOG]);
    assert_eq!(hashes(&ws), before, "DV-9");
    let row = &v["rows"][0];
    assert_eq!(row["state"], "decided");
    assert_eq!(row["decision"]["act"], rec["recordId"]);
    assert_eq!(row["decision"]["alternativeChosen"], "ALT-2");
    assert_eq!(
        row["decision"]["statement"],
        "Hold stage 2 until the version check returns, then start"
    );
    assert_eq!(
        row["decision"]["decidedBy"],
        "Engineer A / enga (identity not verified)"
    );
    assert_eq!(row["decision"]["recordingMode"], "direct capture");
    assert_eq!(row["decision"]["lapse"], "not lapsed");
    assert_eq!(
        v["rows"][1]["state"],
        "pending — awaiting the person's decision"
    );

    // AK-c / AX-06: PKG-2 changes after its offer is shown: nothing captured.
    let o2 = ac
        .compose_a16(reqs[1]["recordId"].as_str().unwrap())
        .unwrap();
    let o2id = o2["offerId"].as_str().unwrap().to_string();
    ac.confirmation_text(&o2id, "ALT-1", &actor).unwrap();
    ac.present(&o2id).unwrap();
    let p2 = ws.join("project/decisions/PKG-2.json");
    let mut b = std::fs::read(&p2).unwrap();
    b.extend_from_slice(b" ");
    std::fs::write(&p2, &b).unwrap();
    let e = ac
        .confirm(
            &o2id,
            "ALT-1",
            InputSource::HostNativeConfirmation,
            actor.clone(),
        )
        .unwrap_err();
    assert!(e.contains("content changed"), "{e}");
    let (entries, _) = read_log(&ws.join(LOG));
    assert_eq!(entries.len(), 5, "no record written for the stale offer");

    // Write outputs for the schema test before the lapse case changes PKG-1.
    let out_dir = evidence_output();
    std::fs::create_dir_all(&out_dir).unwrap();
    std::fs::write(
        out_dir.join("decide-records.jsonl"),
        std::fs::read(ws.join(LOG)).unwrap(),
    )
    .unwrap();
    std::fs::write(
        out_dir.join("decide-offer.json"),
        serde_json::to_vec_pretty(&offer).unwrap(),
    )
    .unwrap();
    std::fs::write(
        out_dir.join("decide-capture.json"),
        serde_json::to_vec_pretty(&cap).unwrap(),
    )
    .unwrap();
    std::fs::write(
        out_dir.join("decide-view.json"),
        serde_json::to_vec_pretty(&v).unwrap(),
    )
    .unwrap();
    std::fs::write(
        out_dir.join("decide-package-files.json"),
        serde_json::to_vec_pretty(&json!([serde_json::from_slice::<Value>(
            &std::fs::read(ws.join("project/decisions/PKG-1.json")).unwrap()
        )
        .unwrap()]))
        .unwrap(),
    )
    .unwrap();

    // DV-7: PKG-1 edited after the decision shows lapsed; the decision is not hidden.
    let p1 = ws.join("project/decisions/PKG-1.json");
    let mut b = std::fs::read(&p1).unwrap();
    b.extend_from_slice(b" ");
    std::fs::write(&p1, &b).unwrap();
    let v = derive(&ws, &[LOG]);
    assert_eq!(v["rows"][0]["state"], "decided");
    assert_eq!(
        v["rows"][0]["decision"]["lapse"],
        "lapsed — the package changed after the decision"
    );
}

#[test]
fn no_write_census_detects_changes_in_relocated_log_and_capture_tree() {
    let ws = scratch_workspace();
    let reqs = identify_packages(&ws).unwrap();
    let mut ac = ActControl::new(&ws);
    let offer = ac
        .compose_a16(reqs[0]["recordId"].as_str().unwrap())
        .unwrap();
    let id = offer["offerId"].as_str().unwrap();
    let actor = person(Some("Fixture person"), Some("fixture"));
    ac.confirmation_text(id, "ALT-2", &actor).unwrap();
    ac.present(id).unwrap();
    let result = ac
        .confirm(id, "ALT-2", InputSource::HostNativeConfirmation, actor)
        .unwrap();
    let before = hashes(&ws);
    assert!(before
        .iter()
        .any(|(p, _)| p.starts_with(".chirality/records/")));
    assert!(before
        .iter()
        .any(|(p, _)| p.starts_with(".chirality/captures/")));
    derive(&ws, &[LOG]);
    assert_eq!(hashes(&ws), before);
    let capture = PathBuf::from(result["captureFile"].as_str().unwrap());
    let mut bytes = std::fs::read(&capture).unwrap();
    bytes.push(b' ');
    std::fs::write(&capture, bytes).unwrap();
    assert_ne!(
        hashes(&ws),
        before,
        "census must detect a mutation to actual relocated capture bytes"
    );
}
