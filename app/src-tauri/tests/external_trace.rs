#[path="../src/schema_validation.rs"] mod schema_validation;
#[path="../src/external_trace.rs"] mod external_trace;
use external_trace::*;
use serde_json::{json,Value};
fn fixture(name:&str)->Vec<u8>{std::fs::read(std::path::Path::new(env!("CARGO_MANIFEST_DIR")).join("resources/external_trace").join(name)).unwrap()}
fn value(name:&str)->Value{serde_json::from_slice(&fixture(name)).unwrap()}
fn account()->TraceAccount{TraceAccount::new("candidate:local-1","origin:local-1").unwrap()}
fn input(bytes:Vec<u8>,kind:RecordKind,evidence:EvidenceKind)->SuppliedRecord{SuppliedRecord{candidate:"candidate:local-1".into(),origin:"origin:local-1".into(),source_reference:"source:fixture".into(),evidence_kind:evidence,record_kind:kind,bytes}}
#[test]
fn canonical_xt_rehearsal_and_work_are_preserved_without_join_counts(){
 let mut a=account();
 for (file,kind) in [("xt-result-record.example.valid.json",RecordKind::XtResult),("xt-work-account.example.valid.json",RecordKind::XtWork)]{
  let bytes=fixture(file);let r=a.receive(input(bytes.clone(),kind,EvidenceKind::DefinitionOrRehearsal));assert!(r.refusal().is_none(),"{:?}",r.refusal());assert_eq!(r.original_bytes(),bytes);assert_eq!(r.original_document(),Some(&value(file)));
 }
 let s=a.snapshot();assert_eq!(s["countsTowardV4Exm24"],false);assert_eq!(s["countsTowardV4Exm25"],false);assert_eq!(s["joinedWitnessState"],"not_supplied");assert_eq!(s["oi003"],"UNRESOLVED{OI-003}");
}
#[test]
fn malformed_schema_invalid_and_candidate_mismatch_are_retained_refusals(){
 let mut a=account();
 for bytes in [b"{".to_vec(),fixture("xt-result-record.example.invalid.json"),fixture("xt-work-account.example.invalid.json")]{
  let r=a.receive(input(bytes.clone(),RecordKind::XtResult,EvidenceKind::OwnCode));assert!(r.refusal().is_some());assert_eq!(r.original_bytes(),bytes);
 }
 let mut supplied=input(fixture("xt-result-record.example.valid.json"),RecordKind::XtResult,EvidenceKind::OwnCode);supplied.candidate="foreign-candidate".into();
 let r=a.receive(supplied);assert!(r.refusal().unwrap().contains("identity mismatch"));assert_eq!(a.snapshot()["entries"].as_array().unwrap().last().unwrap()["candidate"],"foreign-candidate");
}
#[test]
fn parts_cannot_hide_failure_or_missing_attempt_and_joined_pass_is_refused(){
 let original=value("xt-result-record.example.valid.json");let mut a=account();
 let mut wrong=original.clone();wrong["outcome"]="passed".into();assert!(a.receive(input(serde_json::to_vec(&wrong).unwrap(),RecordKind::XtResult,EvidenceKind::DefinitionOrRehearsal)).refusal().unwrap().contains("X-R5"));
 let mut blocked=original.clone();blocked["parts"][0]["outcome"]="blocked".into();blocked["outcome"]="blocked".into();assert!(a.receive(input(serde_json::to_vec(&blocked).unwrap(),RecordKind::XtResult,EvidenceKind::DefinitionOrRehearsal)).refusal().unwrap().contains("blocking cause"));
 blocked["blocked_by"]="attempt stopped by identified unavailable prerequisite".into();assert!(a.receive(input(serde_json::to_vec(&blocked).unwrap(),RecordKind::XtResult,EvidenceKind::DefinitionOrRehearsal)).refusal().is_none());
 let mut joined=original;joined["run_kind"]="joined_witness".into();joined["evidence_label"]="actual_host".into();joined["subject_of_run"]=json!({"app_candidate":"candidate:local-1","host_candidate":"claimed-host","identification_record":"claimed-XC00"});
 for p in joined["parts"].as_array_mut().unwrap(){p["outcome"]="passed".into();p.as_object_mut().unwrap().remove("not_run_because");}
 joined["outcome"]="passed".into();joined["completion"]["counts_toward_witness"]=true.into();
 let r=a.receive(input(serde_json::to_vec(&joined).unwrap(),RecordKind::XtResult,EvidenceKind::ActualHost));assert!(r.refusal().unwrap().contains("DECISION-3"));assert_eq!(r.original_document().unwrap()["outcome"],"passed");
}
#[test]
fn supplier_or_own_code_is_never_actual_host_and_oi003_remains_unruled(){
 let mut a=account();let mut doc=value("xt-result-record.example.valid.json");doc["run_kind"]="joined_witness".into();doc["evidence_label"]="actual_host".into();doc["subject_of_run"]=json!({"app_candidate":"candidate:local-1","host_candidate":"claimed-host","identification_record":"claimed-XC00"});
 for tier in [EvidenceKind::OwnCode,EvidenceKind::NativeSupplier]{assert!(a.receive(input(serde_json::to_vec(&doc).unwrap(),RecordKind::XtResult,tier)).refusal().unwrap().contains("misclassified"));}
 let mut work=value("xt-work-account.example.valid.json");work["disposition"]["status"]="ruled".into();work["disposition"]["ruling"]=json!({"option":"defer","decision_actor":"claimed-person","date":"2026-10-05","source_record":"claimed-source","custody":"claimed-custody","supersession":"claimed","consequences":"claimed"});work["disposition"]["criterion_examined"]="claimed-criterion".into();
 assert!(a.receive(input(serde_json::to_vec(&work).unwrap(),RecordKind::XtWork,EvidenceKind::Extension)).refusal().unwrap().contains("ruling not supplied"));
}
#[test]
fn examination_protocol_binding_native_need_and_act_owner_are_checked(){
 let docs=value("exam.result-record.valid.examples.json");let mut a=account();let doc=docs[0].clone();assert!(a.receive(input(serde_json::to_vec(&doc).unwrap(),RecordKind::ExaminationResult,EvidenceKind::DefinitionOrRehearsal)).refusal().is_none());
 let mut wrong=doc.clone();wrong["parts"]=json!([{"part":"applicable failed part","expectation":"kept criterion","outcome":"fail"}]);assert!(a.receive(input(serde_json::to_vec(&wrong).unwrap(),RecordKind::ExaminationResult,EvidenceKind::OwnCode)).refusal().unwrap().contains("EXP-R1"));
 let mut native=doc.clone();native["parts"]=json!([{"part":"native needed","expectation":"native route","outcome":"pass","needs_native":true}]);assert!(a.receive(input(serde_json::to_vec(&native).unwrap(),RecordKind::ExaminationResult,EvidenceKind::OwnCode)).refusal().unwrap().contains("EXP-R4"));
 let mut actor=doc;actor["acts_cited"]=json!([{"record_ref":"claimed-record","kind":"A5","actor":"app","recorder":"app"}]);assert!(a.receive(input(serde_json::to_vec(&actor).unwrap(),RecordKind::ExaminationResult,EvidenceKind::OwnCode)).refusal().unwrap().contains("EXP-R5"));
}
#[test]
fn own_code_inputs_and_missing_unknown_refused_claims_keep_separate_origin(){
 let raw=fixture("own-code-inputs.json");let manifest:Value=serde_json::from_slice(&raw).unwrap();let mut a=TraceAccount::new(manifest["candidate"].as_str().unwrap(),manifest["origin"].as_str().unwrap()).unwrap();
 a.attach_evidence(EvidenceInput{case:"I4-own-code".into(),source_reference:"own-code-inputs.json (actual receipt/review source hashes)".into(),kind:EvidenceKind::OwnCode,state:ClaimState::Observed,bytes:Some(raw.clone()),reason:"supplied offline result/review references; no supplier or host qualification".into()}).unwrap();
 for (kind,state) in [(EvidenceKind::NativeSupplier,ClaimState::Unknown),(EvidenceKind::ActualHost,ClaimState::NotSupplied),(EvidenceKind::Extension,ClaimState::Refused)]{
  a.attach_evidence(EvidenceInput{case:"TR-01".into(),source_reference:"missing-witness-account".into(),kind,state,bytes:None,reason:"actual join not supplied; DECISION-3/OI-003 unchanged".into()}).unwrap();
 }
 let s=a.snapshot();assert_eq!(s["inputEvidence"][0]["originalBytes"],json!(raw));assert_eq!(s["inputEvidence"][1]["state"],"unknown");assert_eq!(s["inputEvidence"][2]["state"],"not_supplied");assert_eq!(s["inputEvidence"][3]["state"],"refused");
 assert!(a.attach_evidence(EvidenceInput{case:"XC-02".into(),source_reference:"claimed-host".into(),kind:EvidenceKind::ActualHost,state:ClaimState::Observed,bytes:Some(b"claim".to_vec()),reason:"claimed observed".into()}).is_err());
}
#[test]
fn maintained_canonical_resources_and_examples_match_recorded_source_bytes(){
 use sha2::{Digest,Sha256};let root=std::path::Path::new(env!("CARGO_MANIFEST_DIR")).ancestors().nth(4).unwrap();
 for item in value("manifest.json").as_array().unwrap(){let bytes=fixture(item["file"].as_str().unwrap());assert_eq!(std::fs::read(root.join(item["source"].as_str().unwrap())).unwrap(),bytes);assert_eq!(format!("{:x}",Sha256::digest(&bytes)),item["sha256"].as_str().unwrap());}
}
#[test]
fn work_account_missing_duplicate_or_misbound_surface_row_is_not_complete(){
 let original=value("xt-work-account.example.valid.json");let mut a=account();
 let mut missing=original.clone();missing["rows"].as_array_mut().unwrap().remove(0);
 assert!(a.receive(input(serde_json::to_vec(&missing).unwrap(),RecordKind::XtWork,EvidenceKind::DefinitionOrRehearsal)).refusal().unwrap().contains("missing"));
 let mut duplicate=original.clone();let row=duplicate["rows"][0].clone();duplicate["rows"].as_array_mut().unwrap().push(row);
 assert!(a.receive(input(serde_json::to_vec(&duplicate).unwrap(),RecordKind::XtWork,EvidenceKind::DefinitionOrRehearsal)).refusal().unwrap().contains("duplicate"));
 let mut misbound=original;misbound["rows"][0]["c8_row"]="Errors".into();
 assert!(a.receive(input(serde_json::to_vec(&misbound).unwrap(),RecordKind::XtWork,EvidenceKind::DefinitionOrRehearsal)).refusal().unwrap().contains("mismatch"));
}
#[test]
fn exp_r1_exact_independent_overlap_repro_refused_unchanged_control_retained(){
 let controls=value("exam.result-record.valid.examples.json");let valid=controls.as_array().unwrap().iter().find(|d|d["record_id"]=="EXP-EX-08").unwrap().clone();
 let raw=fixture("regressions/EXP-EX-08-overlap.invalid.json");let invalid:Value=serde_json::from_slice(&raw).unwrap();
 let mut exact=valid.clone();exact["parts_not_applicable"][0]["part"]=exact["parts"][0]["part"].clone();assert_eq!(invalid,exact);
 // Both inputs remain valid against the unchanged complete canonical shape.
 let validators=schema_validation::compile_targets(RESOURCES,&[XT_RESULT,XT_WORK,EXP_RESULT],&[EXP_RESULT]).unwrap();validators[0].validate(&valid).unwrap();validators[0].validate(&invalid).unwrap();
 // EXP-EX-08 is explicitly illustrative, not an actual supplier/host witness.
 // This evidence tier only preserves the independent receiver repro's control;
 // the account's joined counts stay false throughout.
 let mut a=account();let control=a.receive(input(serde_json::to_vec(&valid).unwrap(),RecordKind::ExaminationResult,EvidenceKind::NativeSupplier));assert!(control.refusal().is_none());assert_eq!(control.original_document(),Some(&valid));
 let refused=a.receive(input(raw.clone(),RecordKind::ExaminationResult,EvidenceKind::NativeSupplier));assert!(refused.refusal().unwrap().contains("both applicable and not-applicable"));assert_eq!(refused.original_bytes(),raw);assert_eq!(refused.original_document(),Some(&invalid));
 let snapshot=a.snapshot();assert_eq!(snapshot["entries"][1]["claimState"],"refused");assert_eq!(snapshot["entries"][1]["originalDocument"]["outcome"],"pass");assert_eq!(snapshot["countsTowardV4Exm24"],false);assert_eq!(snapshot["countsTowardV4Exm25"],false);
}
#[test]
fn exp_r1_applicability_sets_reject_duplicates_without_relabeling_results(){
 let controls=value("exam.result-record.valid.examples.json");let valid=controls.as_array().unwrap().iter().find(|d|d["record_id"]=="EXP-EX-08").unwrap();
 for field in ["parts","parts_not_applicable"]{
  let mut duplicate=valid.clone();let row=duplicate[field][0].clone();duplicate[field].as_array_mut().unwrap().push(row);
  let mut a=account();let refused=a.receive(input(serde_json::to_vec(&duplicate).unwrap(),RecordKind::ExaminationResult,EvidenceKind::NativeSupplier));assert!(refused.refusal().unwrap().contains("duplicate"));assert_eq!(refused.original_document(),Some(&duplicate));
 }
}
