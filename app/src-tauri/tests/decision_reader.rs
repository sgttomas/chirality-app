//! CI12 actual derive/discovery consumer. All human-act bodies are synthetic claims.
//! No person performed a native act; schema validity supplies no custody authority.
mod common;
use chirality_app_v4_lib::{decision_view::derive, records, schema_validation, util};
use common::ScratchDirectory;
use serde_json::{json, Value};
use std::path::Path;

fn setup() -> (ScratchDirectory, Value, Value) {
    let ws = ScratchDirectory::new("decision-reader");
    let fixture = Path::new(env!("CARGO_MANIFEST_DIR")).join("../tests/fixtures/FX-DP1");
    std::fs::create_dir_all(ws.join("project/decisions")).unwrap();
    let bytes = std::fs::read(fixture.join("project/decisions/PKG-1.json")).unwrap();
    std::fs::write(ws.join("project/decisions/PKG-1.json"), &bytes).unwrap();
    let entries = records::read_log(&fixture.join("records/coordination.rs.jsonl")).0;
    let mut request = entries[0].clone();
    request["recordId"] = json!("rec:synthetic:request");
    request["seq"] = json!(1);
    request["recorder"]["identity"] = json!("writer:request");
    request["body"]["evidence"]["method"] = json!(util::FILE_IDENTITY_METHOD);
    request["body"]["evidence"]["claimedIdentity"] = json!(util::sha256_hex(&bytes));
    let mut act = entries[2].clone();
    act["body"]["decisionActor"] = json!({"displayName":"synthetic fixture; no person's act","osAccount":"synthetic","identityVerified":false});
    act["body"]["boundSubject"] = json!(["decision package rec:synthetic:request"]);
    act["body"]["boundContent"] =
        json!([{"method":util::FILE_IDENTITY_METHOD,"value":util::sha256_hex(&bytes)}]);
    act["body"]["relations"]["requestRef"] = request["recordId"].clone();
    write(&ws, "00-request", &[request.clone()]);
    (ws, request, act)
}
fn claim(base: &Value, id: &str, alternative: &str) -> Value {
    let mut a = base.clone();
    a["recordId"] = json!(format!("rec:synthetic:{id}"));
    a["seq"] = json!(1);
    a["recorder"]["identity"] = json!(format!("writer:{id}"));
    a["body"]["captureEvidence"][0]["ref"] = json!(format!("cap:synthetic:{id}"));
    a["body"]["relations"]["alternativeChosen"] = json!(alternative);
    a
}
fn write(root: &Path, name: &str, entries: &[Value]) {
    let dir = root.join(".chirality/records/acts");
    std::fs::create_dir_all(&dir).unwrap();
    for e in entries {
        schema_validation::bundled().unwrap().validate(e).unwrap();
    }
    std::fs::write(
        dir.join(format!("{name}.jsonl")),
        entries
            .iter()
            .map(|v| serde_json::to_string(v).unwrap() + "\n")
            .collect::<String>(),
    )
    .unwrap();
}
fn row(root: &Path) -> Value {
    derive(root, &[])["rows"][0].clone()
}
fn projection<'a>(r: &'a Value, id: &str) -> &'a Value {
    r["contenders"]
        .as_array()
        .unwrap()
        .iter()
        .find(|p| p["act"] == format!("rec:synthetic:{id}"))
        .unwrap()
}
fn lapse(a: &Value) -> Value {
    json!({"format":"chirality.rs.record","formatVersion":"0.1","recordId":"rec:synthetic:lapse","kind":"act_lapsed","recorder":{"role":"App writer","identity":"writer:lapse"},"context":{"surface":"App"},"seq":1,"writtenAt":"synthetic-recorded", "body":{"act":{"recordId":a["recordId"],"actKind":"A16","capturedAt":a["body"]["captureTime"],"capturingSurface":"app_act_control"},"state":"lapsed","referents":a["body"]["boundSubject"],"c0":a["body"]["boundContent"][0],"c1":{"method":util::FILE_IDENTITY_METHOD,"value":"changed-synthetic"},"time":"synthetic-observed"}})
}
#[test]
fn actual_ab_ba_unordered_claims_and_lapse_attribution_are_invariant() {
    for swap in [false, true] {
        let (ws, _, base) = setup();
        let a = claim(&base, "a", "ALT-1");
        let b = claim(&base, "b", "ALT-2");
        write(&ws, "10-first", &[if swap { b.clone() } else { a.clone() }]);
        write(
            &ws,
            "20-second",
            &[if swap { a.clone() } else { b.clone() }],
        );
        write(&ws, "30-lapse", &[lapse(&a)]);
        let before = std::fs::read(ws.join(".chirality/records/acts/10-first.jsonl")).unwrap();
        let r = row(&ws);
        assert_eq!(r["state"], "ambiguous current standing");
        assert!(r["decision"].is_null());
        assert_eq!(r["currentCandidates"].as_array().unwrap().len(), 2);
        assert_eq!(
            projection(&r, "a")["lapse"],
            "matches c0 again after observed lapse"
        );
        assert_eq!(
            projection(&r, "a")["lapseHistory"],
            json!(["rec:synthetic:lapse"])
        );
        assert_eq!(projection(&r, "b")["lapse"], "not lapsed");
        assert_eq!(projection(&r, "b")["lapseHistory"], json!([]));
        assert!(projection(&r, "a")["captureProvenance"]
            .as_str()
            .unwrap()
            .contains("not verified"));
        assert_eq!(
            before,
            std::fs::read(ws.join(".chirality/records/acts/10-first.jsonl")).unwrap()
        );
    }
}
#[test]
fn actual_ab_ba_competing_corrections_keep_every_branch() {
    for swap in [false, true] {
        let (ws, _, base) = setup();
        let original = claim(&base, "original", "ALT-1");
        let mut a = claim(&base, "a", "ALT-1");
        let mut b = claim(&base, "b", "ALT-2");
        for c in [&mut a, &mut b] {
            c["corrects"] = original["recordId"].clone();
            c["correctionReason"] = json!("synthetic correction");
            c["body"]["captureEvidence"] = original["body"]["captureEvidence"].clone();
        }
        write(&ws, "01-original", &[original]);
        write(&ws, "10-first", &[if swap { b.clone() } else { a.clone() }]);
        write(
            &ws,
            "20-second",
            &[if swap { a.clone() } else { b.clone() }],
        );
        write(&ws, "30-lapse", &[lapse(&a)]);
        let r = row(&ws);
        assert_eq!(r["state"], "ambiguous current standing");
        assert!(r["decision"].is_null());
        assert_eq!(r["contenders"].as_array().unwrap().len(), 3);
        assert_eq!(
            projection(&r, "a")["lapseHistory"],
            json!(["rec:synthetic:lapse"])
        );
        assert_eq!(projection(&r, "b")["lapseHistory"], json!([]));
        assert_eq!(
            projection(&r, "original")["correctedBy"]
                .as_array()
                .unwrap()
                .len(),
            2
        );
    }
}
#[test]
fn valid_correction_links_and_stream_order_do_not_create_new_performances() {
    let (ws, _, base) = setup();
    let mut original = claim(&base, "original", "ALT-1");
    let mut corrected = claim(&base, "corrected", "ALT-2");
    corrected["corrects"] = original["recordId"].clone();
    corrected["correctionReason"] = json!("recorded choice corrected");
    corrected["body"]["captureEvidence"] = original["body"]["captureEvidence"].clone();
    original["seq"] = json!(1);
    corrected["seq"] = json!(2);
    corrected["recorder"] = original["recorder"].clone();
    write(&ws, "10-one-stream", &[original, corrected]);
    let r = row(&ws);
    assert_eq!(r["state"], "decided");
    assert_eq!(r["decision"]["alternativeChosen"], "ALT-2");
    assert!(r["decision"]["earlierActs"][0]["relation"]
        .as_str()
        .unwrap()
        .contains("corrected by"));
}
#[test]
fn distinct_capture_with_explicit_supersession_is_ordered_not_by_filename_or_time() {
    for swap in [false, true] {
        let (ws, _, base) = setup();
        let mut a = claim(&base, "a", "ALT-1");
        let mut b = claim(&base, "b", "ALT-2");
        // The explicit source relation warrants later established capture, not these clock strings.
        a["body"]["captureTime"] = json!("later-looking arbitrary text");
        b["body"]["captureTime"] = json!("earlier-looking arbitrary text");
        a["body"]["relations"]["supersededBy"] = b["recordId"].clone();
        write(&ws, "10-first", &[if swap { b.clone() } else { a.clone() }]);
        write(
            &ws,
            "20-second",
            &[if swap { a.clone() } else { b.clone() }],
        );
        let r = row(&ws);
        assert_eq!(r["state"], "decided");
        assert_eq!(r["decision"]["act"], b["recordId"]);
        assert_eq!(r["decision"]["alternativeChosen"], "ALT-2");
        assert!(r["decision"]["earlierActs"][0]["relation"]
            .as_str()
            .unwrap()
            .contains("explicit recorded relation"));
    }
}
#[test]
fn same_capture_disagreement_is_not_a_later_performance_even_in_one_log() {
    let (ws, _, base) = setup();
    let a = claim(&base, "a", "ALT-1");
    let mut b = claim(&base, "b", "ALT-2");
    b["body"]["captureEvidence"] = a["body"]["captureEvidence"].clone();
    b["seq"] = json!(2);
    b["recorder"] = a["recorder"].clone();
    write(&ws, "10-one-stream", &[a, b]);
    let r = row(&ws);
    assert_eq!(r["state"], "ambiguous current standing");
    assert!(r["limits"]
        .as_array()
        .unwrap()
        .iter()
        .any(|v| v.as_str().unwrap().contains("recorders disagree")));
}
#[test]
fn late_record_sequence_and_clock_do_not_order_distinct_captures() {
    let (ws, _, base) = setup();
    let a = claim(&base, "a", "ALT-1");
    let mut b = claim(&base, "b", "ALT-2");
    b["seq"] = json!(2);
    b["recorder"] = a["recorder"].clone();
    b["observedAt"] = json!("earlier capture observation");
    write(&ws, "10-one-stream", &[a, b]);
    let r = row(&ws);
    assert_eq!(r["state"], "ambiguous current standing");
    assert!(r["decision"].is_null());
}
#[test]
fn unknown_wrong_kind_self_and_cyclic_correction_targets_never_replace() {
    for mode in ["missing", "wrong-kind", "self", "cycle"] {
        let (ws, req, base) = setup();
        let original = claim(&base, "original", "ALT-1");
        let mut a = claim(&base, "a", "ALT-2");
        a["correctionReason"] = json!("synthetic");
        a["corrects"] = match mode {
            "missing" => json!("rec:missing"),
            "wrong-kind" => req["recordId"].clone(),
            "self" => a["recordId"].clone(),
            _ => json!("rec:synthetic:b"),
        };
        write(&ws, "01-original", &[original.clone()]);
        write(&ws, "10-a", &[a.clone()]);
        if mode == "cycle" {
            let mut b = claim(&base, "b", "ALT-1");
            b["corrects"] = a["recordId"].clone();
            b["correctionReason"] = json!("synthetic");
            write(&ws, "20-b", &[b]);
        }
        let v = derive(&ws, &[]);
        assert!(v["limits"]
            .as_array()
            .unwrap()
            .iter()
            .any(|v| v.as_str().unwrap().contains("correction")));
        assert!(v["rows"][0]["contenders"]
            .as_array()
            .unwrap()
            .iter()
            .any(|v| v["act"] == a["recordId"]));
        assert_ne!(v["rows"][0]["decision"]["act"], a["recordId"]);
    }
}
#[test]
fn duplicate_identity_resolution_distinguishes_identical_copies_from_conflicting_requests() {
    for conflict in [false, true] {
        let (ws, req, base) = setup();
        let mut copy = req.clone();
        if conflict {
            copy["body"]["purpose"] = json!("conflicting synthetic request");
        }
        write(&ws, "01-copy", &[copy]);
        write(&ws, "10-act", &[claim(&base, "a", "ALT-1")]);
        let v = derive(&ws, &[]);
        if conflict {
            assert!(v["rows"]
                .as_array()
                .unwrap()
                .iter()
                .all(|r| r["state"] == "unresolvable request identity" && r["decision"].is_null()));
        } else {
            assert_eq!(v["rows"].as_array().unwrap().len(), 1);
            assert_eq!(
                v["rows"][0]["requestResolution"],
                "unique claim (identical copies)"
            );
            assert_eq!(v["rows"][0]["requestSources"].as_array().unwrap().len(), 2);
        }
    }
}
#[test]
fn conflicting_act_ids_on_explicit_read_paths_do_not_pick_one_claim() {
    let (ws, _, base) = setup();
    let a = claim(&base, "duplicate", "ALT-1");
    let b = claim(&base, "duplicate", "ALT-2");
    write(&ws, "10-a", &[a]);
    write(&ws, "20-b", &[b]);
    let v = derive(
        &ws,
        &[
            ".chirality/records/acts/00-request.jsonl",
            ".chirality/records/acts/20-b.jsonl",
            ".chirality/records/acts/10-a.jsonl",
        ],
    );
    assert_eq!(v["rows"][0]["state"], "ambiguous current standing");
    assert!(v["rows"][0]["decision"].is_null());
    assert_eq!(v["unresolvedRecords"].as_array().unwrap().len(), 2);
}
#[test]
fn correction_without_reason_is_nonconformant_and_keeps_original() {
    let (ws, _, base) = setup();
    let original = claim(&base, "original", "ALT-1");
    let mut correction = claim(&base, "bad", "ALT-2");
    correction["corrects"] = original["recordId"].clone();
    write(&ws, "10-original", &[original.clone()]);
    std::fs::write(
        ws.join(".chirality/records/acts/20-invalid.jsonl"),
        serde_json::to_string(&correction).unwrap() + "\n",
    )
    .unwrap();
    let v = derive(&ws, &[]);
    assert_eq!(v["rows"][0]["decision"]["act"], original["recordId"]);
    assert!(!v["limits"].as_array().unwrap().is_empty());
}
#[test]
fn repeated_identical_capture_is_one_claim_with_all_attributed_histories() {
    for swap in [false, true] {
        let (ws, _, base) = setup();
        let a = claim(&base, "a", "ALT-1");
        let mut b = claim(&base, "b", "ALT-1");
        b["body"] = a["body"].clone();
        write(&ws, "10-first", &[if swap { b.clone() } else { a.clone() }]);
        write(
            &ws,
            "20-second",
            &[if swap { a.clone() } else { b.clone() }],
        );
        write(&ws, "30-lapse", &[lapse(&a)]);
        let r = row(&ws);
        assert_eq!(r["state"], "decided");
        assert!(r["decision"]["act"].is_null());
        assert_eq!(
            r["decision"]["equivalentCaptureRecords"],
            json!(["rec:synthetic:a", "rec:synthetic:b"])
        );
        assert_eq!(
            r["decision"]["lapseHistory"],
            json!(["rec:synthetic:lapse"])
        );
        assert_eq!(
            r["decision"]["lapse"],
            "matches c0 again after observed lapse"
        );
    }
}
#[test]
fn original_native_admission_observation_stream_preserves_order_without_clock_ordering() {
    for marker in ["matching", "missing", "mismatch"] {
        let (ws, _, base) = setup();
        let mut a = claim(&base, "a", "ALT-1");
        let mut b = claim(&base, "b", "ALT-2");
        for item in [&mut a, &mut b] {
            item["recorder"] = json!({"role":records::APP_INTERFACE.role,"identity":records::APP_INTERFACE.identity});
            item["observedAt"] = json!("same original event clock text");
            item["body"]["captureTime"] = json!("same original event clock text");
        }
        b["seq"] = json!(2);
        if marker == "missing" {
            b.as_object_mut().unwrap().remove("observedAt");
        } else if marker == "mismatch" {
            b["observedAt"] = json!("different original observation");
        }
        write(&ws, "10-native-observations", &[a, b]);
        let r = row(&ws);
        if marker != "matching" {
            assert_eq!(r["state"], "ambiguous current standing");
        } else {
            assert_eq!(r["decision"]["alternativeChosen"], "ALT-2");
            assert!(r["decision"]["orderingEvidence"][0]["source"]
                .as_str()
                .unwrap()
                .contains("not native-origin verification"));
            assert!(r["decision"]["captureProvenance"]
                .as_str()
                .unwrap()
                .contains("not verified"));
        }
    }
}
#[test]
fn matching_forgeable_markers_in_different_logs_never_create_global_or_native_authority() {
    let (ws, _, base) = setup();
    let mut a = claim(&base, "a", "ALT-1");
    let mut b = claim(&base, "b", "ALT-2");
    for e in [&mut a, &mut b] {
        e["recorder"] =
            json!({"role":records::APP_INTERFACE.role,"identity":records::APP_INTERFACE.identity});
        e["observedAt"] = json!("same forgeable text");
        e["body"]["captureTime"] = json!("same forgeable text");
    }
    write(&ws, "10-a", &[a]);
    write(&ws, "20-b", &[b]);
    let before = std::fs::read(ws.join(".chirality/records/acts/10-a.jsonl")).unwrap();
    let r = row(&ws);
    assert_eq!(r["state"], "ambiguous current standing");
    assert!(r["decision"].is_null());
    assert!(r["contenders"]
        .as_array()
        .unwrap()
        .iter()
        .all(|p| p["captureProvenance"]
            .as_str()
            .unwrap()
            .contains("not verified")));
    assert!(!ws.join(".chirality/captures").exists());
    assert_eq!(
        before,
        std::fs::read(ws.join(".chirality/records/acts/10-a.jsonl")).unwrap()
    );
}
#[test]
fn globally_conflicting_lapse_id_keeps_past_unknown_and_current_bytes_separate() {
    for conflict in [false, true] {
        let (ws, _, base) = setup();
        let a = claim(&base, "a", "ALT-1");
        write(&ws, "10-act", &[a.clone()]);
        let observed = lapse(&a);
        write(&ws, "20-lapse", &[observed.clone()]);
        if conflict {
            let mut disputed = observed.clone();
            disputed["body"]["c1"] = disputed["body"]["c0"].clone();
            write(&ws, "30-conflict", &[disputed]);
        }
        let r = row(&ws);
        let p = projection(&r, "a");
        assert_eq!(p["currentContentComparison"], "matches bound content");
        if conflict {
            assert_eq!(p["lapse"], "unknown (lapse history unresolved)");
            assert_eq!(
                p["historyResolution"],
                "unknown/unresolvable past observation"
            );
            assert_eq!(p["lapseHistory"], json!([]));
            assert_eq!(p["lapseObservationClaims"].as_array().unwrap().len(), 2);
            assert_ne!(
                p["lapseObservationClaims"][0]["source"]["log"],
                p["lapseObservationClaims"][1]["source"]["log"]
            );
            assert_eq!(r["decision"]["lapse"], "unknown (lapse history unresolved)");
        } else {
            assert_eq!(p["lapse"], "matches c0 again after observed lapse");
            assert_eq!(p["lapseHistory"], json!(["rec:synthetic:lapse"]));
        }
    }
}
#[test]
fn identical_lapse_copies_remain_one_resolved_observation_with_all_sources() {
    let (ws, _, base) = setup();
    let a = claim(&base, "a", "ALT-1");
    write(&ws, "10-act", &[a.clone()]);
    let observed = lapse(&a);
    write(&ws, "20-observation", &[observed.clone()]);
    write(&ws, "30-copy", &[observed]);
    let r = row(&ws);
    assert_eq!(
        projection(&r, "a")["lapse"],
        "matches c0 again after observed lapse"
    );
    assert_eq!(
        projection(&r, "a")["historyResolution"],
        "resolved recorded history"
    );
    assert_eq!(
        projection(&r, "a")["lapseObservationClaims"]
            .as_array()
            .unwrap()
            .len(),
        2
    );
}
#[test]
fn equivalent_capture_aggregate_and_each_contender_propagate_unresolved_lapse_dependency() {
    let (ws, _, base) = setup();
    let a = claim(&base, "a", "ALT-1");
    let mut b = claim(&base, "b", "ALT-1");
    b["body"] = a["body"].clone();
    write(&ws, "10-a", &[a.clone()]);
    write(&ws, "11-b", &[b]);
    let observed = lapse(&a);
    let mut dispute = observed.clone();
    dispute["body"]["c1"] = dispute["body"]["c0"].clone();
    write(&ws, "20-lapse", &[observed]);
    write(&ws, "30-dispute", &[dispute]);
    let r = row(&ws);
    assert_eq!(r["decision"]["lapse"], "unknown (lapse history unresolved)");
    assert_eq!(
        r["decision"]["historyResolution"],
        "unknown/unresolvable past observation"
    );
    assert_eq!(
        r["decision"]["currentContentComparison"],
        "matches bound content"
    );
    assert_eq!(
        projection(&r, "a")["historyResolution"],
        "unknown/unresolvable past observation"
    );
    assert_eq!(projection(&r, "b")["lapseHistory"], json!([]));
    assert_eq!(
        projection(&r, "b")["historyResolution"],
        "unknown/unresolvable past observation"
    );
    assert_eq!(
        projection(&r, "b")["lapse"],
        "unknown (lapse history unresolved)"
    );
}
#[test]
fn independent_good_lapse_witness_survives_other_conflicting_id_without_claiming_complete_history()
{
    for aliases in [false, true] {
        let (ws, _, base) = setup();
        let a = claim(&base, "a", "ALT-1");
        write(&ws, "10-a", &[a.clone()]);
        if aliases {
            let mut b = claim(&base, "b", "ALT-1");
            b["body"] = a["body"].clone();
            write(&ws, "11-b", &[b]);
        }
        let conflicting = lapse(&a);
        let mut changed = conflicting.clone();
        changed["body"]["c1"] = changed["body"]["c0"].clone();
        write(&ws, "20-first", &[conflicting.clone()]);
        write(&ws, "30-conflict", &[changed]);
        let mut good = conflicting;
        good["recordId"] = json!("rec:synthetic:independent-good-lapse");
        write(&ws, "40-independent-witness", &[good]);
        let r = row(&ws);
        assert_eq!(
            r["decision"]["lapse"],
            "matches c0 again after observed lapse"
        );
        assert_eq!(
            r["decision"]["historyResolution"],
            "established prior lapse; history incomplete"
        );
        assert_eq!(r["decision"]["historyIncomplete"], true);
        assert_eq!(
            r["decision"]["currentContentComparison"],
            "matches bound content"
        );
        assert_eq!(
            r["decision"]["lapseHistory"],
            json!(["rec:synthetic:independent-good-lapse"])
        );
        for contender in r["contenders"].as_array().unwrap() {
            assert_eq!(contender["lapse"], "matches c0 again after observed lapse");
            assert_eq!(
                contender["historyResolution"],
                "established prior lapse; history incomplete"
            );
            assert_eq!(
                contender["lapseHistory"],
                json!(["rec:synthetic:independent-good-lapse"])
            );
            assert_eq!(
                contender["lapseObservationClaims"]
                    .as_array()
                    .unwrap()
                    .len(),
                3
            );
        }
        assert!(r["limits"]
            .as_array()
            .unwrap()
            .iter()
            .any(|v| v.as_str().unwrap().contains("history remains incomplete")));
    }
}
