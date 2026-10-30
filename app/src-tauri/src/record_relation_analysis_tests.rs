//! The compact checkpoint facts retain the public reader's source meaning.
use super::*;

fn record(id: &str, seq: u64) -> Value {
    let fixtures: Value =
        serde_json::from_str(include_str!("../schemas/fixtures/valid-records.json")).unwrap();
    let mut record = fixtures[10].clone();
    record["recordId"] = json!(id);
    record["seq"] = json!(seq);
    record
}
fn correction(id: &str, seq: u64, target: &str) -> Value {
    let mut record = record(id, seq);
    record["corrects"] = json!(target);
    record["correctionReason"] = json!("Synthetic correction.");
    record
}
fn claims(rows: Vec<(Value, &str)>) -> Vec<Value> {
    rows.into_iter()
        .map(|(record, log)| json!({"source":{"log":log,"seq":record["seq"]},"record":record}))
        .collect()
}
fn check(claims: &[Value], complete: &[&str]) -> (Vec<ClaimState>, Value) {
    let complete = complete.iter().map(|s| s.to_string()).collect();
    let analysis = analyze(claims, &complete);
    let view = project_from_read_claims(claims, &complete);
    let states = claims
        .iter()
        .zip(view["claims"].as_array().unwrap())
        .map(|(original, projected)| {
            assert_eq!(
                original["record"], projected["record"],
                "every original record remains readable, even malformed claims"
            );
            assert_eq!(original["source"], projected["source"]);
            assert_eq!(
                projected["a15Semantics"],
                record_semantics::check_a15_correspondence(&original["record"]).snapshot()
            );
            let id = original["record"]["recordId"].as_str().unwrap_or("");
            let state = analysis.claim_state(id);
            assert_eq!(
                state.corrected,
                !projected["correctedBy"].as_array().unwrap().is_empty()
            );
            assert_eq!(state.relation_limit, projected["relationLimit"].as_str());
            assert_eq!(
                state.identity_resolution,
                projected["identityResolution"].as_str().unwrap()
            );
            assert_eq!(
                state.nonconformant,
                view["diagnostics"]
                    .as_array()
                    .unwrap()
                    .iter()
                    .any(|d| d["state"] == "nonconformant" && d["recordId"].as_str() == Some(id))
            );
            state
        })
        .collect();
    (states, view)
}
fn candidates(projected: &Value, id: &str) -> Value {
    projected["correctionGroups"]
        .as_array()
        .unwrap()
        .iter()
        .find(|g| {
            g["recordIds"]
                .as_array()
                .unwrap()
                .iter()
                .any(|member| member == id)
        })
        .unwrap()["currentCandidates"]
        .clone()
}

#[test]
fn checkpoint_identity_and_nonconformance_keep_all_original_claims() {
    let id = "rec:synthetic:identity";
    let original = record(id, 1);
    let (states, _) = check(
        &claims(vec![(original.clone(), "a"), (original.clone(), "b")]),
        &["a", "b"],
    );
    assert!(states.iter().all(|s| !s.nonconformant
        && !s.corrected
        && s.relation_limit.is_none()
        && s.identity_resolution == "one unchanged claim; identical sources retained"));
    let mut conflicting = original.clone();
    conflicting["body"]["detail"] = json!("Different claim under the same identity.");
    let (states, _) = check(
        &claims(vec![(original.clone(), "a"), (conflicting, "b")]),
        &["a", "b"],
    );
    assert!(states.iter().all(|s| !s.nonconformant
        && !s.corrected
        && s.relation_limit == Some("conflicting record identity")
        && s.identity_resolution == "conflicting identity"));
    let mut malformed = original.clone();
    malformed.as_object_mut().unwrap().remove("kind");
    let (states, _) = check(
        &claims(vec![(malformed, "a"), (original, "b")]),
        &["a", "b"],
    );
    assert!(
        states.iter().all(|s| s.nonconformant
            && !s.corrected
            && s.relation_limit.is_none()
            && s.identity_resolution == "unique readable identity"),
        "a malformed copy's diagnostic excludes that identity even beside a readable copy"
    );
}

#[test]
fn checkpoint_correction_refusals_and_branches_preserve_warranted_order() {
    let base = "rec:synthetic:base";
    let first = "rec:synthetic:first";
    let last = "rec:synthetic:last";
    let rows = vec![
        (record(base, 1), "one"),
        (correction(first, 2, base), "one"),
        (correction(last, 3, base), "one"),
    ];
    let (states, projected) = check(&claims(rows.clone()), &["one"]);
    assert!(states[0].corrected && !states[1].corrected && !states[2].corrected);
    assert_eq!(candidates(&projected, base), json!([last]));
    let (_, incomplete) = check(&claims(rows), &[]);
    assert_eq!(candidates(&incomplete, base), json!([first, last]));
    let (_, cross) = check(
        &claims(vec![
            (record(base, 1), "z"),
            (correction(first, 1, base), "a"),
            (correction(last, 1, base), "m"),
        ]),
        &["z", "a", "m"],
    );
    assert_eq!(candidates(&cross, base), json!([first, last]));
    for (rows, reason, nonconformant) in [
        (
            vec![(correction(first, 1, "rec:synthetic:missing"), "one")],
            "unresolvable correction target",
            false,
        ),
        (
            vec![(correction(first, 1, first), "one")],
            "self correction relation",
            false,
        ),
        (
            vec![
                (record(base, 2), "one"),
                (correction(first, 1, base), "one"),
            ],
            "contradictory owning-log correction order",
            false,
        ),
        (
            vec![
                (correction(first, 1, last), "a"),
                (correction(last, 1, first), "b"),
            ],
            "cyclic correction dependency",
            false,
        ),
    ] {
        let (states, _) = check(&claims(rows), &["one", "a", "b"]);
        let state = states.last().unwrap();
        assert_eq!(state.relation_limit, Some(reason));
        assert_eq!(state.nonconformant, nonconformant);
        assert!(!state.corrected);
    }
    let fixtures: Value =
        serde_json::from_str(include_str!("../schemas/fixtures/valid-records.json")).unwrap();
    let mut wrong_kind = fixtures[29].clone();
    wrong_kind["recordId"] = json!(first);
    wrong_kind["corrects"] = json!(base);
    wrong_kind["correctionReason"] = json!("Synthetic correction.");
    let (states, _) = check(
        &claims(vec![(record(base, 1), "a"), (wrong_kind, "b")]),
        &["a", "b"],
    );
    assert!(!states[0].corrected);
    assert!(states[1].nonconformant);
    assert_eq!(
        states[1].relation_limit,
        Some("nonconformant correction: reason/same-kind rule")
    );
    let mut missing_reason = correction(first, 2, base);
    missing_reason
        .as_object_mut()
        .unwrap()
        .remove("correctionReason");
    let (states, _) = check(
        &claims(vec![(record(base, 1), "one"), (missing_reason, "one")]),
        &["one"],
    );
    assert!(!states[0].corrected && states[1].nonconformant && states[1].relation_limit.is_none());
}

#[test]
fn checkpoint_a15_semantic_correction_limits_do_not_become_capture_authority() {
    let first_line = include_str!(
        "../../../execution/PKG-04/DEL-04-03/Work/RS_RECORD.valid.act-log.example.jsonl"
    )
    .lines()
    .next()
    .unwrap();
    let mut original: Value = serde_json::from_str(first_line).unwrap();
    original["recordId"] = json!("rec:app:original");
    let mut invalid = original.clone();
    invalid["recordId"] = json!("rec:app:invalid");
    invalid["seq"] = json!(2);
    invalid["corrects"] = original["recordId"].clone();
    invalid["correctionReason"] = json!("Synthetic correction.");
    invalid["body"]["relations"]["reviewedDraft"]["content"]["value"] =
        json!("Different reviewed content.");
    let (states, projected) = check(
        &claims(vec![(original.clone(), "one"), (invalid.clone(), "one")]),
        &["one"],
    );
    assert!(!states[0].corrected && !states[1].nonconformant, "A15 semantic diagnostics retain their specific state, rather than the generic schema state");
    assert_eq!(
        candidates(&projected, "rec:app:original"),
        json!(["rec:app:original"])
    );
    invalid.as_object_mut().unwrap().remove("corrects");
    invalid.as_object_mut().unwrap().remove("correctionReason");
    let mut repair = original;
    repair["recordId"] = json!("rec:app:repair");
    repair["seq"] = json!(3);
    repair["corrects"] = json!("rec:app:invalid");
    repair["correctionReason"] = json!("Synthetic valid repair.");
    let (states, projected) = check(&claims(vec![(invalid, "one"), (repair, "one")]), &["one"]);
    assert!(states[0].corrected && !states[1].corrected);
    assert_eq!(
        candidates(&projected, "rec:app:invalid"),
        json!(["rec:app:repair"])
    );
    assert!(projected["claims"]
        .as_array()
        .unwrap()
        .iter()
        .all(|c| c["a15Semantics"]["actAdmitted"] == false));
}
