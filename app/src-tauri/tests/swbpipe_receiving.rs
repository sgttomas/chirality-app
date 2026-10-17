//! SWBPIPE receiving: the App's catalog and proposal receivers applied to
//! (1) DEL-03-02's mapping of SWBPIPE's operation corpus and (2) the documents of
//! SH-1 profile `swbpipe` (DEL-03-01 C-v0.8 §10.8). Invented and test-double
//! material only: nothing here observes SWBPIPE, an App run or a person, and no
//! test may give a host Apply, a receipt or a refusal the standing of a human act.
#[path = "../src/schema_validation.rs"]
mod schema_validation;
#[path = "../src/catalog.rs"]
mod catalog;
#[path = "../src/proposal.rs"]
mod proposal;
use catalog::*;
use proposal::*;
use serde_json::{json, Value};

fn resource(name: &str) -> Vec<u8> {
    std::fs::read(std::path::Path::new(env!("CARGO_MANIFEST_DIR")).join("resources/swbpipe_receiving").join(name)).unwrap()
}
fn value(name: &str) -> Value { serde_json::from_slice(&resource(name)).unwrap() }
fn bytes(v: &Value) -> Vec<u8> { serde_json::to_vec(v).unwrap() }
fn profile() -> Value { value("swbpipe-profile-documents.json") }

/// One-item recorded state built around a supplied item. Elements SWBPIPE does not
/// supply (NR-04 change-item content identity; NR-08 record, count and time) are
/// marked as test placeholders; the App never mints them from host material.
fn one_item_state(item: Value) -> Value {
    let state = item["state"].as_str().unwrap().to_string();
    let open = matches!(state.as_str(), "drafted" | "validated" | "queued" | "accepted");
    let decided = item.get("item_left").is_some();
    let mut counts = serde_json::Map::new();
    counts.insert(state.clone(), json!(1));
    json!({"kind": "recorded_state", "proposal_identity": "test-placeholder:proposal", "dedup_scope": "not_stated",
           "submissions_recorded": 1, "items": [item],
           "derived_state": {"summary": state, "counts": counts, "open": open, "all_items_decided": decided},
           "observed_at": "test-placeholder:time"})
}

#[test]
fn swbpipe_resources_match_identified_source_bytes() {
    use sha2::{Digest, Sha256};
    let root = std::path::Path::new(env!("CARGO_MANIFEST_DIR")).ancestors().nth(4).unwrap();
    let manifest = value("manifest.json");
    assert_eq!(manifest.as_array().unwrap().len(), 2);
    for item in manifest.as_array().unwrap() {
        let copied = resource(item["file"].as_str().unwrap());
        let source = std::fs::read(root.join(item["source"].as_str().unwrap())).unwrap();
        assert_eq!(copied, source, "source drift: {}", item["source"]);
        assert_eq!(format!("{:x}", Sha256::digest(&copied)), item["sha256"].as_str().unwrap());
    }
}

#[test]
fn corpus_mapping_gives_no_case_a_human_act_or_an_applied_branch() {
    let m = value("swbpipe-corpus-mapping.json");
    let rows = m["cases"].as_array().unwrap();
    assert_eq!(rows.len(), 84);
    let count = |o: Option<&str>| rows.iter().filter(|r| r["app"]["contract_outcome"].as_str() == o).count();
    assert_eq!((count(None), count(Some("refused_invalid")), count(Some("refused_stale")), count(Some("success")), count(Some("error"))),
               (34, 45, 3, 1, 1));
    for row in rows {
        let text = serde_json::to_string(row).unwrap();
        for forbidden in ["\"decision\"", "\"A5\"", "\"A10\"", "\"A11\"", "\"accepted\"", "\"rejected\"", "\"withdrawn\"", "\"branch\""] {
            assert!(!text.contains(forbidden), "{}: {forbidden}", row["file"]);
        }
        assert_eq!(row["app"]["app_record_formable"], false);
        assert!(!row["app"]["blocked_by"].as_array().unwrap().is_empty());
        assert!(row["app"]["contract_terms"]["author_identity"].as_str().unwrap().starts_with("unverified")
            || row["host"]["author_type_asserted"].is_null());
    }
}

#[test]
fn a_host_apply_is_never_received_as_acceptance_or_as_applied() {
    let m = value("swbpipe-corpus-mapping.json");
    let applied: Vec<&Value> = m["cases"].as_array().unwrap().iter()
        .filter(|r| r["host"]["application_status"] == "applied_to_session_model").collect();
    assert_eq!(applied.len(), 34);
    for row in applied {
        assert!(row["app"]["contract_outcome"].is_null());
        let blocked = row["app"]["blocked_by"].as_array().unwrap();
        assert!(blocked.contains(&json!("NR-01")) && blocked.contains(&json!("NR-05")));
        assert_eq!(row["app"]["contract_terms"]["host_stated_acceptance_basis"], "user_initiated_apply_in_local_session");
        let terms = &row["app"]["contract_terms"];
        let basis = terms["evaluated_basis"].clone();
        let resulting = json!({"object_identity": row["host"]["target_ref"], "relation": "changed"});
        // The two readings P's applied state allows. Each would claim more than the host recorded.
        let after_acceptance = one_item_state(json!({"item_identity": "1", "state": "applied",
            "change_item_content_identity": "test-placeholder:NR-04",
            "applied": {"branch": "after_acceptance", "receipt_reference": "test-placeholder:NR-05", "relied_on_basis": basis,
                        "resulting_revision": terms["resulting_revision"]["canonical_content_identity"], "resulting_objects": [resulting]}}));
        let err = validate_host_state(&after_acceptance).unwrap_err();
        assert!(err.contains("after_acceptance requires supplied A5"), "{}: {err}", row["file"]);
        // The direct branch would claim a grant. SWBPIPE has none, and a state alone establishes none (P §4.4).
        let mut direct = after_acceptance.clone();
        direct["items"][0]["applied"]["branch"] = "direct_under_grant".into();
        let err = validate_host_state(&direct).unwrap_err();
        assert!(err.contains("direct_under_grant requires an established direct grant reference"), "{}: {err}", row["file"]);
        // Read as the person's acceptance, the Apply is refused for the A5 it lacks.
        let mut accepted = after_acceptance.clone();
        accepted["items"][0]["state"] = "accepted".into();
        accepted["items"][0].as_object_mut().unwrap().remove("applied");
        accepted["derived_state"] = json!({"summary": "accepted", "counts": {"accepted": 1}, "open": true, "all_items_decided": false});
        let err = validate_host_state(&accepted).unwrap_err();
        assert!(err.contains("domain-invalid state: accepted requires A5"), "{}: {err}", row["file"]);
    }
    // Received against a bound SWBPIPE-form request (propose mode, no grant), the direct reading is refused too.
    let p = profile();
    let w1 = bound(&p, "PR-W1", "read_before_apply");
    let mut direct = p["states"]["PR-W1 queued"].clone();
    for item in direct["items"].as_array_mut().unwrap() {
        item["state"] = "applied".into();
        item["applied"] = json!({"branch": "direct_under_grant", "receipt_reference": "test-placeholder:NR-05",
                                 "relied_on_basis": p["requests"]["PR-W1"]["relied_on_basis"][0], "resulting_revision": "test-placeholder:NR-06",
                                 "resulting_objects": "not_supplied"});
    }
    direct["derived_state"] = json!({"summary": "applied", "counts": {"applied": 2}, "open": false, "all_items_decided": false});
    let err = w1.receive_state(&bytes(&direct)).unwrap_err();
    assert!(err.contains("direct_under_grant requires an established direct grant reference"), "{err}");
}

#[test]
fn validate_only_rows_are_received_as_non_mutating_check_outcomes() {
    let m = value("swbpipe-corpus-mapping.json");
    let p = profile();
    let cat = Catalog::receive(&bytes(&p["catalog"])).unwrap();
    let row = |n: &str| m["cases"].as_array().unwrap().iter().find(|r| r["file"].as_str().unwrap().starts_with(n)).unwrap().clone();
    // Case 38: the preview's error is a C §4.1 error of that check, reported by the host. Nothing is queued or applied.
    let blocked = row("case_38_");
    assert_eq!(blocked["app"]["contract_outcome"], "error");
    let terms = &blocked["app"]["contract_terms"];
    let error = json!({"outcome": "error", "reporter": "host",
                       "operation": {"operation_identity": "test-placeholder:NR-10", "operation_version": "test-placeholder:NR-10"},
                       "evaluated_basis": terms["evaluated_basis"],
                       "error": {"error_identity": terms["error_identities"][0], "meaning": terms["outcome_statement"], "effect": "none"}});
    let ReadObservation::NonSuccess { document, .. } = cat.receive_read(&bytes(&error)).unwrap() else { panic!("case 38") };
    assert_eq!(document["error"]["error_identity"], terms["error_identities"][0]);
    assert_eq!(document["error"]["effect"], "none");
    // Case 14: the preview's success, with the host's evaluated basis. SWBPIPE has no catalog (NR-10), so the
    // operation is undiscovered and the read is refused.
    let passed = row("case_14_");
    assert_eq!(passed["app"]["contract_outcome"], "success");
    let mut success = p["read_before_apply"].clone();
    success["basis"] = passed["app"]["contract_terms"]["evaluated_basis"].clone();
    let mut undiscovered = success.clone();
    undiscovered["operation"] = json!({"operation_identity": "test-placeholder:NR-10", "operation_version": "test-placeholder:NR-10"});
    assert!(cat.receive_read(&bytes(&undiscovered)).unwrap_err().contains("undiscovered operation/version"));
    // With the double's read operation standing in for a catalog entry, the success is received but cannot be
    // cited: the host's basis carries no model revision (NR-06).
    let ReadObservation::Success(read) = cat.receive_read(&bytes(&success)).unwrap() else { panic!("case 14") };
    assert!(!read.citable);
    assert_eq!(read.basis()["model_revision"], json!({"not_supplied": "omitted"}));
}

#[test]
fn corpus_refusals_land_on_refused_and_need_host_identities_to_be_recorded() {
    let m = value("swbpipe-corpus-mapping.json");
    for row in m["cases"].as_array().unwrap() {
        let outcome = row["app"]["contract_outcome"].as_str();
        if !matches!(outcome, Some("refused_stale") | Some("refused_invalid")) { continue; }
        let terms = &row["app"]["contract_terms"];
        let mut refusal = json!({"reason": format!("host: {}", terms["error_identities"].as_array().unwrap()
                                     .iter().map(|c| c.as_str().unwrap()).collect::<Vec<_>>().join(", ")),
                                 "evaluated_basis": terms["evaluated_basis"],
                                 "error_identity": terms["error_identities"][0]});
        if outcome == Some("refused_stale") {
            let scope = terms["staleness_scope"].as_str().unwrap();
            refusal["staleness_scope"] = if scope == "whole_model" { "whole_model" } else { "host_stated_other" }.into();
            match terms["failing_targets"].as_array() {
                Some(t) => refusal["failing_targets"] = Value::Array(t.clone()),
                None => refusal["failing_targets_not_supplied"] = true.into(),
            }
        }
        let item = json!({"item_identity": "1", "state": outcome.unwrap(), "refusal": refusal,
                          "item_left": {"cause": terms["item_left_cause"], "time": "test-placeholder:NR-08"}});
        // Without the host's change-item content identity (NR-04) no state can be recorded:
        let missing = one_item_state(item.clone());
        assert!(validate_host_state(&missing).unwrap_err().contains("schema-invalid"), "{}", row["file"]);
        // With it, the refusal is received as refused (never A10), with its item-left event and no act.
        let mut supplied = item.clone();
        supplied["change_item_content_identity"] = "test-placeholder:NR-04".into();
        validate_host_state(&one_item_state(supplied)).unwrap_or_else(|e| panic!("{}: {e}", row["file"]));
    }
}

#[test]
fn profile_reads_bind_whole_model_identities_and_never_compare_across_lineage() {
    let p = profile();
    let cat = Catalog::receive(&bytes(&p["catalog"])).unwrap();
    assert_eq!(cat.document()["basis_profile"]["subject_content_identity"], "whole_model_only");
    assert_eq!(cat.document()["basis_profile"]["staleness_scope"], "whole_model");
    let mut bases = Vec::new();
    for key in ["read_before_apply", "read_after_apply"] {
        let ReadObservation::Success(read) = cat.receive_read(&bytes(&p[key])).unwrap() else { panic!("{key}") };
        assert!(read.citable, "{key}");
        assert_eq!(read.limits, vec!["basis_lineage_not_supplied".to_string()]);
        let whole = &read.basis()["canonical_content_identity"];
        for table in read.document()["views"][0]["tables"].as_array().unwrap() {
            for row in table["rows"].as_array().unwrap() {
                assert_eq!(&row["subject"]["subject_content_identity"], whole);
                assert_eq!(row["subject"]["identity_scope"], "whole_model");
            }
        }
        bases.push(read.basis().clone());
    }
    assert_ne!(bases[0]["canonical_content_identity"], bases[1]["canonical_content_identity"]);
    // No workspace identity or generation: the App reports neither same nor changed (C §5.2 rules 1, 6).
    assert_eq!(compare_basis(&bases[0], &bases[1]), BasisComparison::Incomparable);
}

fn bound(p: &Value, request: &str, read: &str) -> BoundProposal {
    let cat = Catalog::receive(&bytes(&p["catalog"])).unwrap();
    let ReadObservation::Success(r) = cat.receive_read(&bytes(&p[read])).unwrap() else { panic!() };
    BoundProposal::receive(&bytes(&p["requests"][request]), &cat, &[r]).unwrap()
}

#[test]
fn profile_states_are_received_as_queued_or_refused_without_any_act() {
    let p = profile();
    let w1 = bound(&p, "PR-W1", "read_before_apply");
    let queued = w1.receive_state(&bytes(&p["states"]["PR-W1 queued"])).unwrap();
    assert_eq!(queued.document()["derived_state"], json!({"summary": "queued", "counts": {"queued": 2}, "open": true, "all_items_decided": false}));
    assert_eq!(queued.document()["dedup_scope"], "not_stated");
    let w4 = bound(&p, "PR-W4", "read_before_apply");
    let stale = w4.receive_state(&bytes(&p["states"]["PR-W4 refused stale"])).unwrap();
    for item in stale.document()["items"].as_array().unwrap() {
        assert_eq!(item["state"], "refused_stale");
        assert_eq!(item["refusal"]["staleness_scope"], "whole_model");
        assert_eq!(item["refusal"]["failing_targets_not_supplied"], true);
        assert_eq!(item["item_left"]["cause"], "refused_stale");
        assert!(item.get("decision").is_none());
    }
    // PR-W1 was applied by the person inside the host, which no agent path observes. A resubmission is not
    // de-duplicated (SWBPIPE NR-08) and comes back refused stale by its own effect. The App receives that as a
    // refusal of this submission; it carries no act and says nothing about whether the earlier one was applied.
    let again = w1.receive_state(&bytes(&p["states"]["PR-W1 resubmitted after Apply"])).unwrap();
    assert_eq!(again.document()["answered_from_recorded_state"], false);
    assert!(again.document()["items"].as_array().unwrap().iter()
        .all(|i| i["state"] == "refused_stale" && i.get("decision").is_none()));
    for doc in [&p["states"]["PR-W1 queued"], &p["states"]["PR-W4 refused stale"], &p["states"]["PR-W5 refused invalid"],
                &p["states"]["PR-W1 resubmitted after Apply"]] {
        validate_host_state(doc).unwrap();
        assert!(!serde_json::to_string(doc).unwrap().contains("\"decision\""));
    }
}

#[test]
fn an_unobservable_submission_stays_unknown_and_is_never_resubmitted_blind() {
    let p = profile();
    let mut custody = SubmissionCustody::default();
    custody.begin(bound(&p, "PR-W6", "read_after_apply")).unwrap();
    custody.outcome_missing("PR-W6", "app", "lost acknowledgement").unwrap();
    // SWBPIPE offers no observation by identity: the host's 'not exposed' answer is not a proposal state.
    assert!(custody.observe("PR-W6", &bytes(&p["observation_not_exposed"])).is_err());
    let history = custody.history("PR-W6").unwrap();
    assert!(history.iter().any(|h| matches!(h, SubmissionObservation::OutcomeUnknown { .. })));
    assert!(!history.iter().any(|h| matches!(h, SubmissionObservation::Host(_))));
    let again = custody.begin(bound(&p, "PR-W6", "read_after_apply")).unwrap_err();
    assert!(again.contains("observe_before_resubmission"));
}
