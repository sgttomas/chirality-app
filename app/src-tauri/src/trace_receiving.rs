//! Native-selected, memory-only receiving of untrusted XT/EXP source records.
//! The integrating picker owns selection. No current executable identity,
//! native/host witness, examination run, act or durable copy is established.
use crate::external_trace::{EvidenceKind, RecordKind, SuppliedRecord, TraceAccount, RESOURCES, XT_RESULT, XT_WORK, EXP_RESULT};
use crate::attachments::native_path_identity;
use crate::util::{sha256_hex, FILE_IDENTITY_METHOD};
use serde_json::{json, Value};
use jsonschema::Validator;
use std::collections::HashMap;
use std::io::Read;
use std::path::{Path, PathBuf};
use std::sync::OnceLock;

#[derive(Clone, Debug)]
pub struct ActualSelectedSource {
    path: PathBuf,
    bytes: Option<Vec<u8>>,
    identity: Option<Value>,
    read_state: &'static str,
    read_mechanism: &'static str,
    reason: Option<String>,
}
impl ActualSelectedSource {
    /// Caller must supply the actual native picker's path. Read one opened
    /// regular descriptor, not pathname metadata followed by a possibly FIFO open.
    pub fn read(path: PathBuf) -> Self {
        let mut options = std::fs::OpenOptions::new(); options.read(true);
        #[cfg(unix)] {
            use std::os::unix::fs::OpenOptionsExt;
            options.custom_flags(libc::O_NONBLOCK | libc::O_NOCTTY);
        }
        let mut file = match options.open(&path) {
            Ok(file) => file,
            Err(e) => return Self::failed(path, format!("selected file unavailable: {e}")),
        };
        match file.metadata() {
            Ok(metadata) if metadata.file_type().is_file() => {},
            Ok(_) => return Self::failed(path, "opened source is not a regular file; no content read".into()),
            Err(e) => return Self::failed(path, format!("opened source metadata unavailable: {e}")),
        }
        let mut bytes = Vec::new();
        let result = file.read_to_end(&mut bytes);
        let mut source = Self::from_complete_selected_buffer(path, bytes);
        source.read_mechanism = "regular_descriptor_read";
        if let Err(e) = result {
            source.read_state = "partial";
            source.reason = Some(format!("selected descriptor read failed; partial buffer retained: {e}"));
        }
        source
    }
    /// Already-read selected bytes can be handed in by the sole main-process
    /// reader. The supplied buffer is immutable custody, not proof of selection.
    pub fn from_complete_selected_buffer(path: PathBuf, bytes: Vec<u8>) -> Self {
        let identity = json!({"method": FILE_IDENTITY_METHOD,"value":sha256_hex(&bytes),"subject":"observed input buffer"});
        Self { path, bytes: Some(bytes), identity: Some(identity), read_state:"complete", read_mechanism:"supplied_selected_buffer", reason:None }
    }
    fn failed(path:PathBuf, reason:String)->Self { Self{path,bytes:None,identity:None,read_state:"unavailable",read_mechanism:"selected_path_open_refused",reason:Some(reason)} }
    pub fn original_bytes(&self)->Option<&[u8]> {self.bytes.as_deref()}
    pub fn selected_path(&self)->&Path {&self.path}
    pub fn snapshot(&self)->Value {
        json!({"selectedPath":native_path_identity(&self.path),"displayPath":self.path.to_string_lossy(),
            "pathDisplayLimit":if self.path.to_str().is_some(){None}else{Some("native path is not Unicode; display is lossy; selectedPath retains identity")},
            "readState":self.read_state,"readMechanism":self.read_mechanism,"reason":self.reason,"originalBytes":self.bytes,"bufferIdentity":self.identity,
            "identityScope":if self.bytes.is_none(){"not supplied; no input buffer read"}else if self.read_state=="partial"{"partial observed buffer; not full file identity"}else{"observed input buffer; not executable or host content identity"},
            "sourceStanding":"person-supplied; host/executable/native origin unverified"})
    }
    fn reference(&self)->String {json!({"selectedPath":native_path_identity(&self.path),"bufferIdentity":self.identity}).to_string()}
}
fn schema_id(kind:RecordKind)-> &'static str {match kind {RecordKind::XtResult=>XT_RESULT,RecordKind::XtWork=>XT_WORK,RecordKind::ExaminationResult=>EXP_RESULT}}
fn kind_label(kind:RecordKind)-> &'static str {match kind {RecordKind::XtResult=>"xt_result",RecordKind::XtWork=>"xt_work",RecordKind::ExaminationResult=>"exam_result"}}
fn tier_label(tier:EvidenceKind)-> &'static str {match tier {EvidenceKind::OwnCode=>"own_code",EvidenceKind::NativeSupplier=>"native_supplier",EvidenceKind::ActualHost=>"actual_host",EvidenceKind::Extension=>"extension",EvidenceKind::DefinitionOrRehearsal=>"definition_or_rehearsal"}}
fn validate_shape(kind:RecordKind,document:&Value)->Result<(),String> {
    static VALIDATORS:OnceLock<Result<HashMap<String,Validator>,String>>=OnceLock::new();
    let validators=VALIDATORS.get_or_init(|| {
        let ids=[XT_RESULT,XT_WORK,EXP_RESULT];
        let compiled=crate::schema_validation::compile_targets(RESOURCES,&ids,&ids)?;
        Ok(ids.into_iter().map(str::to_string).zip(compiled).collect())
    }).as_ref().map_err(Clone::clone)?;
    validators[schema_id(kind)].validate(document).map_err(|e|format!("canonical schema-invalid: {e}"))
}
#[derive(Clone,Debug)]
pub struct DeclaredBasis { subject:Value, configuration:Value, date:Value, case:Value, candidate_key:String, source_reference:String }
impl DeclaredBasis {
    pub fn snapshot(&self)->Value {json!({"subject":self.subject,"configuration":self.configuration,"date":self.date,"case":self.case,
        "candidateRoutingKey":self.candidate_key,"routingKeyScope":"source-declared routing key; full subject tuple retained; not executable identity",
        "sourceReference":self.source_reference,"basisStanding":"person-supplied examination record; executable/host/native observation not verified"})}
}
fn basis(kind:RecordKind,document:&Value,source:&ActualSelectedSource)->Result<DeclaredBasis,String> {
    let (subject,candidate_key)=match kind {
        RecordKind::ExaminationResult=>{
            if document["run_basis"]!="candidate" {return Err("non-candidate EXP subject; no candidate account basis supplied".into());}
            (document["subject"].clone(),document["subject"]["app_candidate"]["revision"].as_str().unwrap().to_owned())
        },
        RecordKind::XtResult=>{
            if document["run_kind"]!="joined_witness" {return Err("non-candidate XT subject; no candidate account basis supplied".into());}
            (document["subject_of_run"].clone(),document["subject_of_run"]["app_candidate"].as_str().unwrap().to_owned())
        },
        RecordKind::XtWork=>return Err("XT work account has only a source-subject reference/date; complete candidate/configuration basis is not supplied by this document".into()),
    };
    // Full immutable tuple/config/date come from this one shape-valid buffer.
    // No App/supplier status or import clock is used to fill missing fields.
    Ok(DeclaredBasis{subject,configuration:document["configuration"].clone(),date:document["date"].clone(),case:document["case"].clone(),candidate_key,source_reference:source.reference()})
}
#[derive(Debug)]
pub struct ReceivedTrace {
    source:ActualSelectedSource, record_kind:RecordKind, evidence_kind:EvidenceKind,
    document:Option<Value>, basis:Option<DeclaredBasis>, account:Option<TraceAccount>,
    assessment:&'static str, reason:Option<String>,
}
impl ReceivedTrace {
    pub fn receive(source:ActualSelectedSource,record_kind:RecordKind,evidence_kind:EvidenceKind)->Self {
        let mut received=Self{source,record_kind,evidence_kind,document:None,basis:None,account:None,assessment:"unbound",reason:None};
        if received.source.read_state!="complete" {
            received.assessment="source_unavailable_or_partial";received.reason=received.source.reason.clone();return received;
        }
        let document=match serde_json::from_slice::<Value>(received.source.original_bytes().unwrap()) {
            Ok(document)=>document,
            Err(e)=>{received.assessment="refused_malformed";received.reason=Some(format!("malformed JSON: {e}"));return received;}
        };
        received.document=Some(document.clone());
        if let Err(reason)=validate_shape(record_kind,&document){received.assessment="refused_schema";received.reason=Some(reason);return received;}
        let bound=match basis(record_kind,&document,&received.source){Ok(bound)=>bound,Err(reason)=>{received.reason=Some(reason);return received;}};
        let mut account=TraceAccount::new(&bound.candidate_key,&bound.source_reference).expect("complete shape-valid source basis has nonempty routing identity");
        let entry=account.receive(SuppliedRecord{candidate:bound.candidate_key.clone(),origin:bound.source_reference.clone(),source_reference:bound.source_reference.clone(),evidence_kind,record_kind,bytes:received.source.original_bytes().unwrap().to_vec()});
        if let Some(reason)=entry.refusal(){received.assessment="refused_semantic";received.reason=Some(reason.into());}
        else {received.assessment="received_supplied_record";}
        received.basis=Some(bound);received.account=Some(account);received
    }
    pub fn source(&self)->&ActualSelectedSource {&self.source}
    pub fn snapshot(&self)->Value {
        json!({"source":self.source.snapshot(),"recordKind":kind_label(self.record_kind),"declaredEvidenceCategory":tier_label(self.evidence_kind),
            "assessment":self.assessment,"reason":self.reason,"originalDocument":self.document,
            "suppliedBasis":self.basis.as_ref().map(DeclaredBasis::snapshot),"account":self.account.as_ref().map(TraceAccount::snapshot),
            "semanticAssessment":if self.account.is_some(){"TraceAccount checked; see refusal/account"}else{"not admitted to candidate account"},
            "currentExecutableIdentity":"not_established","nativeExamination":"not_established","hostOrigin":"unverified",
            "countsTowardV4Exm24":false,"countsTowardV4Exm25":false,"oi003":"UNRESOLVED{OI-003}","hostJoin":"deferred_DECISION-3"})
    }
}
/// Each selected import owns an independent source/basis/account. No filename,
/// revision-only key or prior successful basis can merge or retarget another.
#[derive(Default,Debug)]
pub struct TraceReceivingSession { imports:Vec<ReceivedTrace> }
impl TraceReceivingSession {
    pub fn read_selected(&mut self,path:PathBuf,kind:RecordKind,tier:EvidenceKind)->usize {self.receive_selected_source(ActualSelectedSource::read(path),kind,tier)}
    pub fn receive_selected_source(&mut self,source:ActualSelectedSource,kind:RecordKind,tier:EvidenceKind)->usize {
        self.imports.push(ReceivedTrace::receive(source,kind,tier));self.imports.len()-1
    }
    pub fn import(&self,index:usize)->Option<&ReceivedTrace>{self.imports.get(index)}
    pub fn snapshot(&self)->Value {json!({"imports":self.imports.iter().map(ReceivedTrace::snapshot).collect::<Vec<_>>(),
        "custody":"App memory only; independent imports, no merge or executable verification"})}
}
