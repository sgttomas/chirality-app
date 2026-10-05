mod common;
use common::ScratchDirectory;
use chirality_app_v4_lib::{records,schema_validation,decision_view::record_relations::{read_logs,record_semantics::{self,Status,RegistrationBinding}}};
use serde_json::{json,Value};
use std::path::{Path,PathBuf};
fn examples()->Vec<Value>{
 let root=Path::new(env!("CARGO_MANIFEST_DIR")).ancestors().nth(2).unwrap();
 let execution=root.join("execution/PKG-04_Human acts, autonomy and run evidence/1_Working/DEL-04-03_Content-bound decisions and compact run records/Design/RS_RECORD.valid.act-log.example.jsonl");
 std::fs::read_to_string(execution).unwrap().lines().map(|l|serde_json::from_str(l).unwrap()).collect()
}
fn single()->Value{examples()[0].clone()}
fn multi()->Value{examples()[3].clone()}
fn write(root:&ScratchDirectory,name:&str,rows:&[Value])->PathBuf{
 let path=root.join(name);let mut bytes=Vec::new();for(i,r)in rows.iter().enumerate(){let mut r=r.clone();r["seq"]=json!(i+1);schema_validation::bundled().unwrap().validate(&r).unwrap();bytes.extend(serde_json::to_vec(&r).unwrap());bytes.push(b'\n');}std::fs::write(&path,bytes).unwrap();path
}
fn read_claim(path:&Path)->Value{let(entries,limits)=records::read_log(path);assert!(limits.is_empty());assert_eq!(entries.len(),1);entries[0].clone()}
fn binding(record:&Value,index:usize)->RegistrationBinding{
 let body=&record["body"];let r=body["relations"].get("registeredEntries").and_then(Value::as_array).map(|v|&v[index]).unwrap_or(&body["relations"]);let content=body["boundContent"][index].clone();
 let name=if body["boundSubject"].as_array().unwrap().len()==1{"supports-adjust"}else if index==0{"row-review"}else{"span-check"};
 let identity=json!({"kind":"workflow","origin":"project","sourceRoot":"explicit-library-root","name":name,"revision":content["value"],"revisionMethod":content["method"]});
 RegistrationBinding{registered_identity:identity.clone(),identity,library_origin:"project".into(),library_source_root:"explicit-library-root".into(),scope:body["scope"].as_str().unwrap().into(),persisted_subject:body["boundSubject"][index].as_str().unwrap().into(),reviewed_reference:r["reviewedDraft"]["draft"].as_str().unwrap().into(),content,prior_revision:None,source_reference:"synthetic explicit WR descriptor/library input; no capture proof".into()}
}
#[test]
fn actual_log_valid_single_multi_historical_and_other_kind_are_only_subset_checked(){
 let root=ScratchDirectory::new("a15-r7-valid");for record in [single(),multi()]{let path=write(&root,"claims.jsonl",&[record.clone()]);let claim=read_claim(&path);assert_eq!(claim["body"],record["body"]);let a=record_semantics::check_a15_correspondence(&claim);assert_eq!(a.status,Status::CheckedSubset);assert!(a.eligible_for_derived_claim());let projection=read_logs(&[path]);assert_eq!(projection["claims"][0]["record"]["body"],record["body"]);assert_eq!(projection["claims"][0]["a15Semantics"]["actAdmitted"],false);assert_eq!(projection["correctionGroups"][0]["currentCandidates"],json!([record["recordId"]]));}
 let other=examples()[1].clone();assert_eq!(record_semantics::check_a15_correspondence(&other).status,Status::NotApplicable);
}
#[test]
fn schema_valid_different_reviewed_content_and_wrong_order_remain_readable_but_ineligible(){
 let root=ScratchDirectory::new("a15-r7-invalid");let mut wrong=single();wrong["body"]["relations"]["reviewedDraft"]["content"]["value"]="other-reviewed-content".into();
 let mut order=multi();order["body"]["relations"]["registeredEntries"].as_array_mut().unwrap().swap(0,1);
 let mut count=multi();count["body"]["boundContent"].as_array_mut().unwrap().pop();
 for record in [wrong,order,count]{let path=write(&root,"invalid.jsonl",&[record.clone()]);let claim=read_claim(&path);assert_eq!(record_semantics::check_a15_correspondence(&claim).status,Status::Nonconformant);let p=read_logs(&[path]);assert_eq!(p["claims"][0]["record"]["body"],record["body"]);assert_eq!(p["claims"][0]["a15Semantics"]["derivedClaimEligible"],false);assert!(p["correctionGroups"][0]["currentCandidates"].as_array().unwrap().is_empty());assert_eq!(p["claims"][0]["provenance"],"recorded claim; not verified native evidence");}
}
#[test]
fn equal_value_under_other_method_or_scope_and_unobtainable_are_incomparable_not_invalid_native(){
 let root=ScratchDirectory::new("a15-r7-methods");for field in ["method","scope","notObtainable"]{
  let mut r=single();if field=="notObtainable"{r["body"]["relations"]["reviewedDraft"]["content"]=json!({"notObtainable":true,"reason":"identity not observed"});}else{r["body"]["relations"]["reviewedDraft"]["content"][field]="other opaque designation/scope".into();}
  let path=write(&root,"incomparable.jsonl",&[r.clone()]);let a=record_semantics::check_a15_correspondence(&read_claim(&path));assert_eq!(a.status,Status::Incomparable);let p=read_logs(&[path]);assert_eq!(p["claims"][0]["record"]["body"],r["body"]);assert_eq!(p["claims"][0]["a15Semantics"]["nativeCustody"],"unknown; semantic comparison is not capture proof");assert!(p["correctionGroups"][0]["currentCandidates"].as_array().unwrap().is_empty());
 }
}
#[test]
fn full_explicit_registration_tuple_library_revision_and_order_no_display_parser_fallback(){
 let root=ScratchDirectory::new("a15-r7-full-tuple");let r=read_claim(&write(&root,"tuple.jsonl",&[single()]));assert_eq!(record_semantics::check_registration_candidate(&r,&[binding(&r,0)]).status,Status::CheckedSubset);
 for field in ["origin","sourceRoot","name","revision"]{let mut b=binding(&r,0);b.identity[field]=if field=="origin"{"user".into()}else{"foreign actual candidate component".into()};assert_eq!(record_semantics::check_registration_candidate(&r,&[b]).status,Status::Nonconformant,"{field}");}
 let mut b=binding(&r,0);b.identity["revisionMethod"]="other opaque method".into();assert_eq!(record_semantics::check_registration_candidate(&r,&[b]).status,Status::Incomparable);
 let mut b=binding(&r,0);b.library_source_root="different library root".into();assert_eq!(record_semantics::check_registration_candidate(&r,&[b]).status,Status::Nonconformant);
 let mut b=binding(&r,0);b.source_reference.clear();assert_eq!(record_semantics::check_registration_candidate(&r,&[b]).status,Status::Incomparable);
 let m=read_claim(&write(&root,"multi-tuple.jsonl",&[multi()]));assert_eq!(record_semantics::check_registration_candidate(&m,&[binding(&m,0),binding(&m,1)]).status,Status::CheckedSubset);let bindings=vec![binding(&m,1),binding(&m,0)];assert_eq!(record_semantics::check_registration_candidate(&m,&bindings).status,Status::Nonconformant);
 // Opaque shortened revision labels are never parsed as full revision/content.
 assert!(r["body"]["boundSubject"][0].as_str().unwrap().ends_with("@rev-4"));assert_eq!(r["body"]["boundContent"][0]["value"],"wfrev:rev-4");
}
#[test]
fn prior_tuple_and_derived_from_are_full_method_aware_without_historical_relabel(){
 let mut r=single();let prior=json!({"kind":"workflow","origin":"project","sourceRoot":"explicit-library-root","name":"supports-adjust","revision":"prior opaque revision","revisionMethod":"prior opaque method","derivedFrom":{"kind":"workflow","origin":"user","sourceRoot":"source-user-library","name":"base","revision":"base revision","revisionMethod":"base method"}});r["body"]["relations"]["priorRevision"]=prior.clone();schema_validation::bundled().unwrap().validate(&r).unwrap();let mut b=binding(&r,0);b.prior_revision=Some(prior.clone());assert_eq!(record_semantics::check_registration_candidate(&r,&[b]).status,Status::CheckedSubset);
 let mut b=binding(&r,0);let mut wrong=prior.clone();wrong["derivedFrom"]["sourceRoot"]="different source root".into();b.prior_revision=Some(wrong);assert_eq!(record_semantics::check_registration_candidate(&r,&[b]).status,Status::Nonconformant);
 let mut b=binding(&r,0);let mut wrong=prior;wrong["revisionMethod"]="other method".into();b.prior_revision=Some(wrong);assert_eq!(record_semantics::check_registration_candidate(&r,&[b]).status,Status::Incomparable);
}
#[test]
fn nonconformant_or_incomparable_correction_cannot_suppress_valid_predecessor_but_valid_repair_can(){
 let root=ScratchDirectory::new("a15-r7-corrections");let mut original=single();original["recordId"]="rec:app:original".into();let mut invalid=original.clone();invalid["recordId"]="rec:app:invalid-correction".into();invalid["corrects"]="rec:app:original".into();invalid["correctionReason"]="synthetic correction claim".into();invalid["body"]["relations"]["reviewedDraft"]["content"]["value"]="unreviewed".into();
 let path=write(&root,"invalid-correction.jsonl",&[original.clone(),invalid.clone()]);let p=read_logs(&[path]);assert_eq!(p["claims"].as_array().unwrap().len(),2);assert_eq!(p["claims"][1]["record"]["body"],invalid["body"]);assert_eq!(p["correctionGroups"][0]["currentCandidates"],json!(["rec:app:original"]));assert!(p["claims"][0]["correctedBy"].as_array().unwrap().is_empty());
 let mut unknown=invalid.clone();unknown["body"]["relations"]["reviewedDraft"]["content"]=original["body"]["boundContent"][0].clone();unknown["body"]["relations"]["reviewedDraft"]["content"]["method"]="other method".into();let p=read_logs(&[write(&root,"unknown-correction.jsonl",&[original.clone(),unknown])]);assert_eq!(p["correctionGroups"][0]["currentCandidates"],json!(["rec:app:original"]));
 let mut bad_original=invalid.clone();bad_original.as_object_mut().unwrap().remove("corrects");bad_original.as_object_mut().unwrap().remove("correctionReason");let mut repaired=original;repaired["recordId"]="rec:app:repaired".into();repaired["corrects"]="rec:app:invalid-correction".into();repaired["correctionReason"]="explicit valid content repair".into();let p=read_logs(&[write(&root,"valid-repair.jsonl",&[bad_original,repaired])]);assert_eq!(p["correctionGroups"][0]["currentCandidates"],json!(["rec:app:repaired"]));assert_eq!(p["claims"].as_array().unwrap().len(),2);
}
