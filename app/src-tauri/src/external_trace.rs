//! Local XT work/result accounting: XT X-R1…5, §5; EXP-R1…5 through
//! DEP-09-09-012. No suite execution or host qualification occurs here.
use serde_json::{json, Value};
use jsonschema::Validator;
use std::collections::HashMap;
use std::sync::OnceLock;
pub const XT_RESULT: &str = "urn:chirality:app-v4:proposed:xt-result-record";
pub const XT_WORK: &str = "urn:chirality:app-v4:proposed:xt-work-account";
pub const EXP_RESULT: &str = "urn:chirality:app-v4:del-09-01:exam-result-record:0.2";
pub const RESOURCES: &[(&str,&str)] = &[
 ("xt-result-record.schema.json",include_str!("../resources/external_trace/xt-result-record.schema.json")),
 ("xt-work-account.schema.json",include_str!("../resources/external_trace/xt-work-account.schema.json")),
 ("exam.result-record.schema.json",include_str!("../resources/external_trace/exam.result-record.schema.json")),
];
fn validate(id: &str, document: &Value) -> Result<(),String> {
 static REGISTRY: OnceLock<Result<HashMap<String,Validator>,String>>=OnceLock::new();
 let registry=REGISTRY.get_or_init(|| {
  let ids=[XT_RESULT,XT_WORK,EXP_RESULT];
  let validators=crate::schema_validation::compile_targets(RESOURCES,&ids,&ids)?;
  Ok(ids.into_iter().map(str::to_string).zip(validators).collect())
 }).as_ref().map_err(Clone::clone)?;
 registry.get(id).ok_or("trace record contract not selected")?.validate(document).map_err(|e|format!("schema-invalid: {e}"))
}
#[derive(Clone,Copy,Debug,PartialEq,Eq)]
pub enum EvidenceKind { OwnCode, NativeSupplier, ActualHost, Extension, DefinitionOrRehearsal }
impl EvidenceKind {
 fn label(self)-> &'static str {match self {Self::OwnCode=>"own_code",Self::NativeSupplier=>"native_supplier",Self::ActualHost=>"actual_host",Self::Extension=>"extension",Self::DefinitionOrRehearsal=>"definition_or_rehearsal"}}
}
#[derive(Clone,Copy,Debug)]
pub enum RecordKind { XtResult, XtWork, ExaminationResult }
impl RecordKind {fn id(self)-> &'static str {match self {Self::XtResult=>XT_RESULT,Self::XtWork=>XT_WORK,Self::ExaminationResult=>EXP_RESULT}}}
#[derive(Clone,Copy,Debug,PartialEq,Eq)]
pub enum ClaimState { Observed, Refused, Unknown, NotSupplied }
impl ClaimState {fn label(self)-> &'static str {match self {Self::Observed=>"observed",Self::Refused=>"refused",Self::Unknown=>"unknown",Self::NotSupplied=>"not_supplied"}}}
#[derive(Clone,Debug)]
pub struct EvidenceInput {pub case:String,pub source_reference:String,pub kind:EvidenceKind,pub state:ClaimState,pub bytes:Option<Vec<u8>>,pub reason:String}
impl EvidenceInput {fn snapshot(&self)->Value {json!({"case":self.case,"sourceReference":self.source_reference,"evidenceKind":self.kind.label(),"state":self.state.label(),"originalBytes":self.bytes,"reason":self.reason,"countsTowardJoinedWitness":false})}}
#[derive(Clone,Debug)]
pub struct SuppliedRecord {
 pub candidate: String, pub origin: String, pub source_reference: String,
 pub evidence_kind: EvidenceKind, pub record_kind: RecordKind, pub bytes: Vec<u8>,
}
#[derive(Clone,Debug)]
pub struct AccountEntry { supplied:SuppliedRecord, document:Option<Value>, refusal:Option<String> }
impl AccountEntry {
 pub fn original_bytes(&self)-> &[u8] {&self.supplied.bytes}
 pub fn original_document(&self)-> Option<&Value> {self.document.as_ref()}
 pub fn refusal(&self)-> Option<&str> {self.refusal.as_deref()}
 fn snapshot(&self)->Value {json!({"candidate":self.supplied.candidate,"origin":self.supplied.origin,
  "sourceReference":self.supplied.source_reference,"evidenceKind":self.supplied.evidence_kind.label(),
  "claimState":if self.refusal.is_some(){"refused"}else{"observed_supplied_record"},
  "reason":self.refusal,"originalBytes":self.supplied.bytes,"originalDocument":self.document,
  "countsTowardJoinedWitness":false})}
}
#[derive(Debug)]
pub struct TraceAccount {candidate:String,origin:String,entries:Vec<AccountEntry>,evidence:Vec<EvidenceInput>}
impl TraceAccount {
 pub fn new(candidate:&str,origin:&str)->Result<Self,String> {
  if candidate.is_empty()||origin.is_empty(){return Err("candidate/origin identity not supplied".into());}
  Ok(Self{candidate:candidate.into(),origin:origin.into(),entries:Vec::new(),evidence:Vec::new()})
 }
 /// Retains malformed or refused claims as raw evidence, never a validated pass.
 /// Source references are supplied provenance, not authenticated act evidence.
 pub fn receive(&mut self,supplied:SuppliedRecord)-> &AccountEntry {
  let parsed=serde_json::from_slice::<Value>(&supplied.bytes);
  let (document,refusal)=match parsed {
   Err(e)=>(None,Some(format!("malformed JSON: {e}"))),
   Ok(document)=>{
    let result=if supplied.candidate!=self.candidate||supplied.origin!=self.origin||supplied.source_reference.is_empty(){Err("candidate/origin/source identity mismatch or missing".into())}
     else {validate(supplied.record_kind.id(),&document).and_then(|_|semantic(&document,supplied.record_kind,supplied.evidence_kind,&self.candidate))};
    (Some(document),result.err())
   }
  };
  self.entries.push(AccountEntry{supplied,document,refusal});self.entries.last().unwrap()
 }
 /// Own-code receipts/review references are retained as supplied input claims;
 /// they neither stand for native evidence nor count toward an XT witness.
 pub fn attach_evidence(&mut self,input:EvidenceInput)->Result<(),String> {
  if input.case.is_empty()||input.source_reference.is_empty()||input.reason.is_empty(){return Err("evidence case/source/reason missing".into());}
  if input.state==ClaimState::Observed && input.bytes.is_none(){return Err("observed evidence has no supplied bytes".into());}
  if matches!(input.kind,EvidenceKind::ActualHost|EvidenceKind::Extension)&&input.state==ClaimState::Observed{return Err("actual joined/extension witness not supplied; retain as unknown or not-supplied".into());}
  self.evidence.push(input);Ok(())
 }
 pub fn entries(&self)-> &[AccountEntry] {&self.entries}
 pub fn snapshot(&self)->Value {json!({"candidate":self.candidate,"origin":self.origin,
  "entries":self.entries.iter().map(AccountEntry::snapshot).collect::<Vec<_>>(),
  "inputEvidence":self.evidence.iter().map(EvidenceInput::snapshot).collect::<Vec<_>>(),
  "joinedWitnessState":"not_supplied","extensionCriterion":"not_established",
  "oi003":"UNRESOLVED{OI-003}","hostJoin":"deferred_DECISION-3",
  "countsTowardV4Exm24":false,"countsTowardV4Exm25":false})}
}
/// EXP §3.1 / XT X-R5; label mapping is explicit, never outcome conflation.
fn aggregate(parts:&[Value],exp:bool)-> &'static str {
 let pass=if exp{"pass"}else{"passed"};let fail=if exp{"fail"}else{"failed"};let notrun=if exp{"not-run"}else{"not_run"};
 if parts.iter().any(|p|p["outcome"]==fail){fail}
 else if parts.iter().any(|p|p["outcome"]=="blocked"){"blocked"}
 else if parts.iter().all(|p|p["outcome"]==pass){pass}
 else if parts.iter().all(|p|p["outcome"]==notrun){notrun}
 else {"inconclusive"}
}
fn semantic(doc:&Value,kind:RecordKind,evidence:EvidenceKind,candidate:&str)->Result<(),String> {
 match kind {
  RecordKind::XtResult=>{
   if doc["completion"]["counts_toward_witness"]==true || (doc["run_kind"]=="joined_witness" && doc["outcome"]=="passed") {
    return Err("joined pass/count refused: actual joined input not supplied; DECISION-3 deferred; OI-003 unresolved".into());
   }
   if doc["evidence_label"]=="actual_host" && !matches!(evidence,EvidenceKind::ActualHost|EvidenceKind::Extension){return Err("evidence misclassified: own-code/native supplier/rehearsal is not actual-host witness".into());}
   if let Some(app)=doc["subject_of_run"].get("app_candidate") {if app!=candidate{return Err("record's App candidate differs from supplied account candidate".into());}}
   if doc["outcome"]!=aggregate(doc["parts"].as_array().unwrap(),false){return Err("XT X-R5: outcome conceals applicable part result".into());}
   if doc["outcome"]=="blocked" && doc.get("blocked_by").is_none(){return Err("EXP blocked: attempted case needs recorded blocking cause".into());}
   for act in doc.get("act_records_cited").and_then(Value::as_array).into_iter().flatten(){if act["actor"]==act["recorder"]{return Err("EXP-R5: actor must differ from recorder".into());}}
  }
  RecordKind::XtWork=>{
   if doc["disposition"]["status"]=="ruled"{return Err("OI-003 ruling not supplied to this local account; input ruling claim retained, not performed".into());}
   if doc["evidence_label"]=="actual_host"&&!matches!(evidence,EvidenceKind::ActualHost|EvidenceKind::Extension){return Err("work evidence misclassified as actual host".into());}
   let expected = [
    ("entry_discovery","Entry discovery"),("catalog_level_interface","Catalog-level interface"),
    ("exposure","Exposure per surface"),("input_schema","Input schema / argument checking"),
    ("availability_and_reason","Availability + reason"),("effects_and_resulting_objects","Effects / affected objects / resulting objects"),
    ("result_and_standing","Result content + standing"),("errors","Errors"),("class_element","Class element"),
    ("constraint_receipt","Governing checkpoint constraint"),("read_basis","Read basis, subject content identities, method designation"),
    ("proposal_views","Proposal views")];
   let mut seen=std::collections::HashSet::new();
   for row in doc["rows"].as_array().unwrap(){
    let surface=row["surface"].as_str().unwrap();let element=row["element"].as_str().unwrap();
    if !seen.insert((surface,element)){return Err("duplicate surface/element work row".into());}
    let receiving=match element {"native_mapping"=>Some("X"),"loop_tool_offering"=>Some("E"),"app_receiving_configuration"=>Some("App-X"),_=>None};
    if let Some(required)=receiving {if surface!=required{return Err("receiving work element on wrong surface".into());}}
    else {
     let c8=expected.iter().find(|(e,_)|*e==element).unwrap().1;
     if !matches!(surface,"H"|"E"|"X") || (row["c8_row"]!=c8 && !(surface=="E"&&element=="input_schema"&&row["c8_row"]=="Loop-side catalog-schema argument checking")){return Err("work element/C8 row or surface mismatch".into());}
    }
    if row["evidence"].get("not_observed").is_some() && (row["change_made"]!="not_observed"||row["other_changes_required"]!="unknown") {return Err("unobserved work cannot establish a change or no further work".into());}
   }
   for surface in ["H","E","X"] {for (element,_) in expected {if !seen.contains(&(surface,element)){return Err("work account missing required surface/element row; unknown is not no".into());}}}
   for key in [("X","native_mapping"),("E","loop_tool_offering"),("App-X","app_receiving_configuration")] {if !seen.contains(&key){return Err("work account missing receiving row".into());}}
  }
  RecordKind::ExaminationResult=>{
   // EXP-R1 / §3.1: applicable and pre-declared not-applicable parts
   // are disjoint sets, not repeated rows. Compare exact supplied IDs;
   // never remove a failed/applicable row or rewrite the source declaration.
   let mut applicable=std::collections::HashSet::new();
   for part in doc.get("parts").and_then(Value::as_array).into_iter().flatten(){
    if !applicable.insert(part["part"].as_str().unwrap()){return Err("EXP-R1: duplicate applicable part identity".into());}
   }
   let mut excluded=std::collections::HashSet::new();
   for part in doc.get("parts_not_applicable").and_then(Value::as_array).into_iter().flatten(){
    let id=part["part"].as_str().unwrap();
    if applicable.contains(id){return Err("EXP-R1: part listed both applicable and not-applicable".into());}
    if !excluded.insert(id){return Err("EXP-R1: duplicate not-applicable part identity".into());}
   }
   if let Some(parts)=doc.get("parts").and_then(Value::as_array){if !parts.is_empty()&&doc["outcome"]!=aggregate(parts,true){return Err("EXP-R1: outcome conceals applicable part result".into());}}
   if matches!(doc["case"]["scenario"].as_str(),Some("V4-EXM-24"|"V4-EXM-25")) && doc["outcome"]=="pass" {return Err("joined scenario pass refused: DECISION-3 deferred and actual input not supplied".into());}
   if matches!(evidence,EvidenceKind::OwnCode|EvidenceKind::DefinitionOrRehearsal) && doc["case"].get("scenario").is_some(){return Err("own-code/rehearsal record cannot establish joined scenario".into());}
   for act in doc.get("acts_cited").and_then(Value::as_array).into_iter().flatten(){if act["actor"]==act["recorder"]{return Err("EXP-R5: actor must differ from recorder".into());}}
   for part in doc.get("parts").and_then(Value::as_array).into_iter().flatten(){
    if part["needs_native"]==true&&part["outcome"]=="pass" {
     let native=part.get("evidence").and_then(Value::as_array).into_iter().flatten().chain(doc["evidence"].as_array().unwrap().iter()).any(|e|matches!(e["route"].as_str().or(doc["configuration"]["route"]["kind"].as_str()),Some("native_development"|"native_packaged")));
     if !native || matches!(evidence,EvidenceKind::OwnCode|EvidenceKind::DefinitionOrRehearsal){return Err("EXP-R4: native-needed part lacks native-route evidence".into());}
    }
   }
  }
 }
 Ok(())
}
