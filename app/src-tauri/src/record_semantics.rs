//! RS HA-10/R-7 A15 correspondence only. Shapes and recorded claims are not
//! capture/native proof, full record conformance or registration authority.
use serde_json::{json,Value};
#[derive(Clone,Copy,Debug,PartialEq,Eq)]
pub enum Status { NotApplicable, CheckedSubset, Nonconformant, Incomparable }
impl Status {fn label(self)->&'static str{match self{Self::NotApplicable=>"not_applicable",Self::CheckedSubset=>"checked_a15_r7_subset",Self::Nonconformant=>"nonconformant_a15_correspondence",Self::Incomparable=>"incomparable_a15_content"}}}
#[derive(Clone,Debug)]
pub struct Assessment {pub status:Status,pub reasons:Vec<String>}
impl Assessment {
 pub fn eligible_for_derived_claim(&self)->bool{matches!(self.status,Status::NotApplicable|Status::CheckedSubset)}
 pub fn snapshot(&self)->Value{json!({"status":self.status.label(),"reasons":self.reasons,"derivedClaimEligible":self.eligible_for_derived_claim(),"scope":"A15 HA-10/R-7 correspondence subset only","nativeCustody":"unknown; semantic comparison is not capture proof","actAdmitted":false,"registrationEstablished":false})}
 fn new(status:Status)->Self{Self{status,reasons:vec![]}}
 fn add(&mut self,status:Status,reason:impl Into<String>){
  if status==Status::Nonconformant || (status==Status::Incomparable&&self.status!=Status::Nonconformant){self.status=status;}
  self.reasons.push(reason.into());
 }
}
fn content(a:&Value,b:&Value,out:&mut Assessment,where_:&str){
 if a.get("notObtainable").is_some()||b.get("notObtainable").is_some(){out.add(Status::Incomparable,format!("{where_}: content identity not obtainable"));return;}
 if a["method"].as_str().is_none()||b["method"].as_str().is_none()||a["method"]!=b["method"]{out.add(Status::Incomparable,format!("{where_}: methods differ/unavailable; no value-only fallback"));return;}
 if a.get("scope")!=b.get("scope"){out.add(Status::Incomparable,format!("{where_}: content scopes differ/unavailable"));return;}
 if a["value"]!=b["value"]{out.add(Status::Nonconformant,format!("{where_}: bound content differs from reviewed/expected content"));}
}
/// Subjects and WR ID-3 references remain opaque. No sourceRoot/full tuple is
/// inferred from a display string or historical shortened revision label.
pub fn check_a15_correspondence(record:&Value)->Assessment{
 if record["kind"]!="human_act"||record["body"]["actKind"]!="A15"{return Assessment::new(Status::NotApplicable);}
 let mut out=Assessment::new(Status::CheckedSubset);
 if let Err(reason)=crate::schema_validation::bundled().and_then(|v|v.validate(record)){out.add(Status::Nonconformant,format!("full schema prerequisite: {reason}"));return out;}
 let body=&record["body"];let subjects=body["boundSubject"].as_array().unwrap();let contents=body["boundContent"].as_array().unwrap();let relations=&body["relations"];
 if let Some(entries)=relations.get("registeredEntries").and_then(Value::as_array){
  if entries.len()!=subjects.len()||entries.len()!=contents.len(){out.add(Status::Nonconformant,"registered entries/bound subjects/bound contents must correspond one-to-one in order");return out;}
  for(i,entry)in entries.iter().enumerate(){
   if entry["subject"]!=subjects[i]{out.add(Status::Nonconformant,format!("entry {i}: registered subject differs from ordered bound subject"));}
   content(&contents[i],&entry["reviewedDraft"]["content"],&mut out,&format!("entry {i}"));
  }
 }else{
  if subjects.len()!=1||contents.len()!=1{out.add(Status::Nonconformant,"single reviewed-draft relation requires exactly one bound subject/content");return out;}
  content(&contents[0],&relations["reviewedDraft"]["content"],&mut out,"single registration");
 }
 out
}
/// Actual owning consumer supplies these frozen source facts. This struct is
/// comparison input, not a trusted-capture/capability/registration constructor.
pub struct RegistrationBinding {
 pub identity:Value,
 pub registered_identity:Value,
 pub library_origin:String,
 pub library_source_root:String,
 pub scope:String,
 pub persisted_subject:String,
 pub reviewed_reference:String,
 pub content:Value,
 pub prior_revision:Option<Value>,
 pub source_reference:String,
}
fn binding_shape(identity:&Value,contents:&Value)->Result<(),String>{
 use std::sync::OnceLock;
 static VALIDATORS:OnceLock<Result<Vec<jsonschema::Validator>,String>>=OnceLock::new();
 let validators=VALIDATORS.get_or_init(||crate::schema_validation::compile_targets(crate::schema_validation::RESOURCES,&[crate::schema_validation::RS_ID],&["urn:chirality:app-v4:del-04-03:rs-record:0.1#/$defs/workflowTuple","urn:chirality:app-v4:del-04-03:rs-record:0.1#/$defs/contentIdentity"])).as_ref().map_err(Clone::clone)?;
 validators[0].validate(identity).map_err(|e|e.to_string())?;validators[1].validate(contents).map_err(|e|e.to_string())
}
fn tuple(a:&Value,b:&Value,out:&mut Assessment,where_:&str){
 for field in ["kind","origin","sourceRoot","name"]{
  if a[field].as_str().is_none()||b[field].as_str().is_none(){out.add(Status::Incomparable,format!("{where_}: full tuple field {field} not supplied"));return;}
  if a[field]!=b[field]{out.add(Status::Nonconformant,format!("{where_}: tuple field {field} differs"));}
 }
 if a["revision"].as_str().is_none()||b["revision"].as_str().is_none()||a["revisionMethod"].as_str().is_none()||b["revisionMethod"].as_str().is_none(){out.add(Status::Incomparable,format!("{where_}: revision/method not supplied"));}
 else if a["revisionMethod"]!=b["revisionMethod"]{out.add(Status::Incomparable,format!("{where_}: revision methods differ; no value-only fallback"));}
 else if a["revision"]!=b["revision"]{out.add(Status::Nonconformant,format!("{where_}: revision differs"));}
 match(a.get("derivedFrom"),b.get("derivedFrom")){
  (None,None)=>{},(Some(a),Some(b))=>tuple(a,b,out,&format!("{where_} derived-from")),_=>out.add(Status::Nonconformant,format!("{where_}: derived-from tuple differs")),
 }
}
/// Additional candidate-specific comparison; cannot recover missing tuples or
/// bless an act. Caller owns the bridge between descriptor and opaque RS refs.
pub fn check_registration_candidate(record:&Value,expected:&[RegistrationBinding])->Assessment{
 let mut out=check_a15_correspondence(record);if out.status==Status::NotApplicable||out.status==Status::Nonconformant{return out;}
 let body=&record["body"];let subjects=body["boundSubject"].as_array().unwrap();let contents=body["boundContent"].as_array().unwrap();let relations=&body["relations"];
 if expected.len()!=subjects.len(){out.add(Status::Nonconformant,"candidate binding count differs from ordered registration subjects");return out;}
 for(i,binding)in expected.iter().enumerate(){
  if binding.source_reference.is_empty()||binding.library_origin.is_empty()||binding.library_source_root.is_empty()||binding.scope.is_empty(){out.add(Status::Incomparable,format!("entry {i}: actual full library/scope/source binding not supplied"));continue;}
  if let Err(reason)=binding_shape(&binding.identity,&binding.content){out.add(Status::Incomparable,format!("entry {i}: complete canonical binding not supplied: {reason}"));continue;}
  if let Err(reason)=binding_shape(&binding.registered_identity,&binding.content){out.add(Status::Incomparable,format!("entry {i}: actual descriptor tuple not supplied: {reason}"));continue;}
  tuple(&binding.registered_identity,&binding.identity,&mut out,&format!("entry {i} registered/current full tuple"));
  if binding.identity["kind"]!="workflow"||binding.identity["origin"]!=binding.library_origin||binding.identity["sourceRoot"]!=binding.library_source_root{out.add(Status::Nonconformant,format!("entry {i}: full tuple/library origin or source root differs"));}
  if body["scope"]!=binding.scope||subjects[i]!=binding.persisted_subject{out.add(Status::Nonconformant,format!("entry {i}: explicit scope/full subject bridge differs"));}
  let relation=relations.get("registeredEntries").and_then(Value::as_array).map(|es|&es[i]).unwrap_or(relations);
  if relation["reviewedDraft"]["draft"]!=binding.reviewed_reference{out.add(Status::Nonconformant,format!("entry {i}: reviewed source reference differs"));}
  content(&contents[i],&binding.content,&mut out,&format!("entry {i} candidate"));
  let revision=json!({"method":binding.registered_identity["revisionMethod"],"value":binding.registered_identity["revision"]});
  let no_scope=json!({"method":binding.content["method"],"value":binding.content["value"]});
  content(&revision,&no_scope,&mut out,&format!("entry {i} registered revision/content"));
  match(&binding.prior_revision,&relation["priorRevision"]){
   (None,Value::Null)=>{},(Some(expected),actual)if!actual.is_null()=>tuple(actual,expected,&mut out,&format!("entry {i} prior revision")),_=>out.add(Status::Nonconformant,format!("entry {i}: prior revision relation differs")),
  }
 }
 out
}
