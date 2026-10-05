#[path = "../src/schema_validation.rs"]
mod schema_validation;
#[path = "../src/catalog.rs"]
mod catalog;
use catalog::*;
use serde_json::Value;
fn fixture(name: &str) -> Vec<u8> {
    std::fs::read(std::path::Path::new(env!("CARGO_MANIFEST_DIR")).join("resources/catalog_adapter").join(name)).unwrap()
}
fn value(name: &str) -> Value { serde_json::from_slice(&fixture(name)).unwrap() }
#[test]
fn declared_registry_and_all_design_examples() {
    let c = Contracts::from_resources(RESOURCES).unwrap();
    let manifest: Value = value("manifest.json");
    let mut tested = 0;
    for item in manifest.as_array().unwrap() {
        let name = item["file"].as_str().unwrap();
        if item["kind"] == "schema" { continue; }
        let stem = name.split(".example").next().unwrap();
        let schema: Value = serde_json::from_slice(&fixture(&format!("{stem}.schema.json"))).unwrap();
        let result = c.validate(schema["$id"].as_str().unwrap(), &value(name));
        assert_eq!(result.is_ok(), !name.contains("invalid"), "{name}: {result:?}");
        tested += 1;
    }
    assert_eq!(tested, 33);
}
#[test]
fn registry_setup_refuses_missing_resources_and_external_retrieval() {
    let mut resources = RESOURCES.to_vec(); resources.pop();
    assert!(Contracts::from_resources(&resources).is_err());
    let mut s: Value = serde_json::from_str(RESOURCES[0].1).unwrap();
    s["$defs"]["unavailable"] = serde_json::json!({"$ref":"https://example.invalid/no-fetch"});
    let text = serde_json::to_string(&s).unwrap(); resources = RESOURCES.to_vec(); resources[0].1 = &text;
    assert!(Contracts::from_resources(&resources).is_err());
}
#[test]
fn binding_and_unavailable_preserve_original_bytes() {
    let cat = Catalog::receive(&fixture("catalog.example-valid.json")).unwrap();
    let raw = fixture("read_result.example-valid.json");
    let ReadObservation::Success(read) = cat.receive_read(&raw).unwrap() else { panic!() };
    assert!(read.citable); assert_eq!(read.original_bytes(), raw);
    assert_eq!(read.host_identity(), "SH-1");
    let mut later = cat.document().clone(); later["edition"] = "e3".into();
    let _selection = Catalog::receive(&serde_json::to_vec(&later).unwrap()).unwrap();
    assert_eq!(read.document()["edition"], cat.document()["edition"]);
    let raw = fixture("read_result.example-valid-2.json");
    let ReadObservation::NonSuccess { document, bytes } = cat.receive_read(&raw).unwrap() else { panic!() };
    assert_eq!(document["outcome"], "unavailable"); assert_eq!(bytes, raw);
}
#[test]
fn schema_checks_precede_domain_and_basis_lineage_is_incomparable() {
    let mut doc = value("catalog.example-valid-2.json");
    doc["entries"][0]["effects"]["external_contact"]["argument_name"] = "undeclared".into();
    let bytes = serde_json::to_vec(&doc).unwrap();
    assert!(Catalog::receive(&bytes).unwrap_err().contains("CX-1"));
    doc["completeness"] = "bad".into();
    assert!(Catalog::receive(&serde_json::to_vec(&doc).unwrap()).unwrap_err().contains("schema-invalid"));
    let mut cat = value("catalog.example-valid.json");
    cat["basis_profile"]["workspace_identity"] = "not_supplied".into();
    cat["basis_profile"]["generation"] = "not_supplied".into();
    let cat = Catalog::receive(&serde_json::to_vec(&cat).unwrap()).unwrap();
    let ReadObservation::Success(read) = cat.receive_read(&fixture("read_result.example-valid-3.json")).unwrap() else { panic!() };
    assert!(read.citable); assert_eq!(read.limits, ["basis_lineage_not_supplied"]);
    assert_eq!(compare_basis(read.basis(), read.basis()), BasisComparison::Incomparable);
    let mut incomplete = read.document().clone(); incomplete["basis"]["model_revision"] = serde_json::json!({"not_supplied":"omitted"});
    let ReadObservation::Success(read) = cat.receive_read(&serde_json::to_vec(&incomplete).unwrap()).unwrap() else { panic!() };
    assert!(!read.citable);
}

#[test]
fn maintained_resources_match_identified_source_bytes() {
    use sha2::{Digest, Sha256};
    let manifest = value("manifest.json");
    let root = std::path::Path::new(env!("CARGO_MANIFEST_DIR")).ancestors().nth(4).unwrap();
    for item in manifest.as_array().unwrap() {
        let bytes = fixture(item["file"].as_str().unwrap());
        let source = std::fs::read(root.join(item["source"].as_str().unwrap())).unwrap();
        assert_eq!(bytes, source, "source drift: {}", item["source"]);
        assert_eq!(format!("{:x}", Sha256::digest(&bytes)), item["sha256"].as_str().unwrap());
    }
}
#[path = "../src/proposal.rs"]
mod proposal;
#[path = "../src/external_adapter.rs"]
mod external_adapter;
fn bound_proposal() -> proposal::BoundProposal {
    let cat = Catalog::receive(&fixture("catalog.example-valid.json")).unwrap();
    let ReadObservation::Success(read) = cat.receive_read(&fixture("read_result.example-valid.json")).unwrap() else { panic!() };
    // Invented App binding test. Use host-supplied identities from the maintained
    // original read; these are not new SH-1 or real host output observations.
    let mut p = value("proposal.example-valid.json"); p["relied_on_basis"] = serde_json::json!([read.basis()]);
    for item in p["items"].as_array_mut().unwrap() {
        for target in item["relied_on_targets"].as_array_mut().unwrap() {
            for view in read.document()["views"].as_array().unwrap() {
                for table in view["tables"].as_array().unwrap() {
                    for row in table["rows"].as_array().unwrap() {
                        if row["subject"]["subject_identity"] == target["subject_identity"] {
                            target["subject_content_identity"] = row["subject"]["subject_content_identity"].clone();
                        }
                    }
                }
            }
        }
    }
    proposal::BoundProposal::receive(&serde_json::to_vec(&p).unwrap(), &cat, &[read]).unwrap()
}
#[test]
fn receipt_unknown_retains_original_no_ack_or_retry_promotes_effect() {
    use proposal::*;
    let p = bound_proposal(); let original = p.original_bytes().to_vec();
    let mut custody = SubmissionCustody::default(); custody.begin(p.clone()).unwrap();
    custody.outcome_missing(p.identity(), "app", "transport ACK received; host receipt absent").unwrap();
    assert!(custody.begin(p.clone()).unwrap_err().contains("observe_before_resubmission"));
    assert_eq!(custody.bound(p.identity()).unwrap().original_bytes(),original);
    let mut state = value("proposal_state.example-valid.json");
    state["items"][0]["applied"]["relied_on_basis"] = p.document()["relied_on_basis"][0].clone();
    custody.observe(p.identity(), &serde_json::to_vec(&state).unwrap()).unwrap();
    assert!(matches!(custody.history(p.identity()).unwrap()[1], SubmissionObservation::OutcomeUnknown { .. }));
    assert!(matches!(custody.history(p.identity()).unwrap()[2], SubmissionObservation::Host(_)));
    state["items"][0]["applied"]["receipt_reference"] = Value::Null;
    assert!(p.receive_state(&serde_json::to_vec(&state).unwrap()).unwrap_err().contains("schema-invalid"));
}
#[test]
fn changed_basis_targets_and_derived_state_are_refused() {
    let p = bound_proposal();
    let mut state = value("proposal_state.example-valid.json");
    assert!(p.receive_state(&serde_json::to_vec(&state).unwrap()).unwrap_err().contains("retargeted"));
    state["items"][0]["applied"]["relied_on_basis"] = p.document()["relied_on_basis"][0].clone();
    state["derived_state"]["summary"] = "applied".into();
    assert!(p.receive_state(&serde_json::to_vec(&state).unwrap()).is_err());
}
#[test]
fn disabled_channel_executes_nothing_enabled_keeps_uncertainty() {
    use external_adapter::*;
    let p = bound_proposal(); let mut custody = proposal::SubmissionCustody::default();
    let mut status = value("channel_status.example-valid.json"); status["channel_state"] = "disabled".into(); status["disabled_sub_case"] = "host_reports_off".into();
    status["host_enablement"]["record"] = "not_in_force".into(); status["host_enablement"].as_object_mut().unwrap().remove("capture_evidence_reference");
    let channel = Channel::receive(&serde_json::to_vec(&status).unwrap()).unwrap();
    let count = std::cell::Cell::new(0);
    assert!(channel.submit(p.clone(), &mut custody, |_| { count.set(count.get()+1); Ok(vec![]) }).is_err());
    assert_eq!(count.get(),0); assert!(custody.bound(p.identity()).is_none());
    let channel = Channel::receive(&fixture("channel_status.example-valid.json")).unwrap();
    channel.submit(p.clone(), &mut custody, |bytes| { assert_eq!(bytes,p.original_bytes()); count.set(count.get()+1); Ok(b"{}".to_vec()) }).unwrap();
    assert_eq!(count.get(),1);
    assert!(matches!(custody.history(p.identity()).unwrap().last().unwrap(),proposal::SubmissionObservation::OutcomeUnknown { .. }));
    assert!(channel.submit(p.clone(), &mut custody, |_| {count.set(count.get()+1); Ok(vec![]) }).is_err()); assert_eq!(count.get(),1);
    let account = DispatchAccount::receive(&fixture("external_dispatch_record.example-valid-2.json")).unwrap();
    assert_eq!(account.document()["outcome"]["value"],"outcome_unknown"); assert!(account.missing.contains(&"grant_in_force"));
}
#[path = "../src/receiving.rs"]
mod receiving;
#[test]
fn loop_receiving_truncation_duplicates_and_siblings_do_not_execute() {
    use receiving::*;
    let cat = Catalog::receive(&fixture("catalog.example-valid.json")).unwrap();
    let valid = value("LOOP_TOOL_CALL.example.valid.json");
    let mut truncated = valid.clone(); truncated["response_termination"] = "length-truncated".into();
    let received = receive_calls(&[valid.clone(),truncated], &cat).unwrap();
    assert!(received.iter().all(|c| !c.ready_for_host_validation));
    let received = receive_calls(&[valid.clone(),valid.clone()], &cat).unwrap();
    assert!(received.iter().all(|c| c.refusal.as_ref().unwrap().contains("duplicate")));
    let mut bad = valid.clone(); bad["call_correlation_identity"] = "other".into(); bad["argument_text"] = "{".into();
    let received = receive_calls(&[valid,bad], &cat).unwrap();
    assert!(received[0].ready_for_host_validation); assert!(!received[1].ready_for_host_validation);
    assert!(supplied_model(None).is_err());
    let received = receive_destination(&fixture("LOOP_DESTINATION_REQUEST.example.valid.json")).unwrap();
    assert_eq!(received.document()["state"],"granted"); // supplied host report, no App A12
}
#[test]
fn panel_receiving_keeps_identity_content_and_missing_host_evidence() {
    use receiving::*;
    let received = receive_panel_input(&fixture("PANEL_RETURN_INPUT.example.valid.json")).unwrap();
    assert_eq!(received.original_bytes(), fixture("PANEL_RETURN_INPUT.example.valid.json"));
    let cat = Catalog::receive(&fixture("catalog.example-valid.json")).unwrap();
    let ReadObservation::Success(read) = cat.receive_read(&fixture("read_result.example-valid.json")).unwrap() else {panic!()};
    assert_eq!(compare_panel(&read,None),PanelComparison::HostTableNotSupplied);
    assert_eq!(compare_panel(&read,Some(&read)),PanelComparison::SameMeaningfulContent);
    let mut changed = read.document().clone(); changed["standing"]["known_limitations"] = serde_json::json!(["new host limitation"]);
    let ReadObservation::Success(host) = cat.receive_read(&serde_json::to_vec(&changed).unwrap()).unwrap() else {panic!()};
    assert_eq!(compare_panel(&read,Some(&host)),PanelComparison::DifferentMeaningfulContent);
}
