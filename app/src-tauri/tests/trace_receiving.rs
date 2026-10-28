#[path="../src/schema_validation.rs"] mod schema_validation;
#[path="../src/external_trace.rs"] mod external_trace;
#[path="../src/trace_receiving.rs"] mod trace_receiving;
pub use chirality_app_v4_lib::{attachments,util};
use external_trace::{RecordKind,EvidenceKind};
use trace_receiving::{ActualSelectedSource,ReceivedTrace,TraceReceivingSession};
use serde_json::{json,Value};
use std::path::{Path,PathBuf};
struct Files(PathBuf);
impl Files {
 fn new()->Self {
  static NEXT:std::sync::atomic::AtomicUsize=std::sync::atomic::AtomicUsize::new(0);
  let path=std::env::temp_dir().join(format!("chirality-trace-receiving-{}-{}-{}",std::process::id(),std::time::SystemTime::now().duration_since(std::time::UNIX_EPOCH).unwrap().as_nanos(),NEXT.fetch_add(1,std::sync::atomic::Ordering::Relaxed)));
  std::fs::create_dir(&path).unwrap();Self(path)
 }
 fn write(&self,name:&str,bytes:&[u8])->PathBuf{let path=self.0.join(name);std::fs::write(&path,bytes).unwrap();path}
}
impl Drop for Files {fn drop(&mut self){std::fs::remove_dir_all(&self.0).unwrap();}}
fn fixture(name:&str)->Vec<u8>{std::fs::read(Path::new(env!("CARGO_MANIFEST_DIR")).join("resources/external_trace").join(name)).unwrap()}
fn value(name:&str)->Value{serde_json::from_slice(&fixture(name)).unwrap()}
#[test]
fn selected_regular_file_once_to_full_unverified_person_stated_basis_and_later_snapshot(){
 let files=Files::new();let bytes=fixture("receiving/EXP-person-stated-basis.json");let path=files.write("résultat-Δ.json",&bytes);let mut session=TraceReceivingSession::default();
 let id=session.read_selected(path.clone(),RecordKind::ExaminationResult,EvidenceKind::NativeSupplier);let snapshot=session.snapshot();let received=&snapshot["imports"][id];let original=value("receiving/EXP-person-stated-basis.json");
 assert_eq!(received["assessment"],"received_supplied_record");assert_eq!(received["originalDocument"],original);assert_eq!(received["suppliedBasis"]["subject"],original["subject"]);assert_eq!(received["suppliedBasis"]["configuration"],original["configuration"]);assert_eq!(received["suppliedBasis"]["date"],original["date"]);assert_eq!(received["suppliedBasis"]["date"]["source"],"stated_by_person");
 assert_eq!(session.import(id).unwrap().source().original_bytes().unwrap(),bytes);assert_eq!(received["source"]["bufferIdentity"]["value"],util::sha256_hex(&bytes));assert_eq!(received["source"]["bufferIdentity"]["method"],util::FILE_IDENTITY_METHOD);assert_eq!(received["source"]["readMechanism"],"regular_descriptor_read");assert_eq!(received["source"]["selectedPath"],attachments::native_path_identity(&path));assert!(received["source"]["pathDisplayLimit"].is_null());
 assert_eq!(received["currentExecutableIdentity"],"not_established");assert_eq!(received["nativeExamination"],"not_established");assert_eq!(received["countsTowardV4Exm24"],false);assert_eq!(received["countsTowardV4Exm25"],false);assert_eq!(std::fs::read_dir(&files.0).unwrap().count(),1);
 std::fs::write(&path,b"{}").unwrap();assert_eq!(session.snapshot(),snapshot); // snapshot never reopens latest filename
}
#[test]
fn same_filename_revision_different_build_imports_have_separate_exact_basis_and_custody(){
 let files=Files::new();let first=fixture("receiving/EXP-person-stated-basis.json");let second=fixture("receiving/EXP-same-revision-other-build.json");let path=files.write("report.json",&first);let mut session=TraceReceivingSession::default();
 let a=session.read_selected(path.clone(),RecordKind::ExaminationResult,EvidenceKind::NativeSupplier);let first_snapshot=session.import(a).unwrap().snapshot();std::fs::write(&path,&second).unwrap();let b=session.read_selected(path,RecordKind::ExaminationResult,EvidenceKind::NativeSupplier);let second_snapshot=session.import(b).unwrap().snapshot();
 assert_eq!(first_snapshot["suppliedBasis"]["subject"]["app_candidate"]["revision"],second_snapshot["suppliedBasis"]["subject"]["app_candidate"]["revision"]);assert_ne!(first_snapshot["suppliedBasis"]["subject"]["app_candidate"]["build_identity"],second_snapshot["suppliedBasis"]["subject"]["app_candidate"]["build_identity"]);assert_ne!(first_snapshot["source"]["bufferIdentity"],second_snapshot["source"]["bufferIdentity"]);assert_eq!(session.import(a).unwrap().snapshot(),first_snapshot);assert_eq!(session.snapshot()["imports"].as_array().unwrap().len(),2);assert_eq!(first_snapshot["account"]["entries"].as_array().unwrap().len(),1);assert_eq!(second_snapshot["account"]["entries"].as_array().unwrap().len(),1);
}
#[test]
fn missing_or_noncandidate_basis_keeps_raw_record_hash_and_source_limits(){
 let files=Files::new();let bytes=fixture("receiving/EXP-missing-build.json");let source=ActualSelectedSource::read(files.write("missing-build.json",&bytes));let received=ReceivedTrace::receive(source,RecordKind::ExaminationResult,EvidenceKind::NativeSupplier);let snapshot=received.snapshot();
 assert_eq!(snapshot["assessment"],"refused_schema");assert!(snapshot["suppliedBasis"].is_null());assert_eq!(received.source().original_bytes().unwrap(),bytes);assert_eq!(snapshot["source"]["bufferIdentity"]["value"],util::sha256_hex(&bytes));assert!(!snapshot["reason"].as_str().unwrap().is_empty());
 let definition=value("exam.result-record.valid.examples.json")[0].clone();let bytes=serde_json::to_vec(&definition).unwrap();let received=ReceivedTrace::receive(ActualSelectedSource::read(files.write("definition.json",&bytes)),RecordKind::ExaminationResult,EvidenceKind::DefinitionOrRehearsal);let snapshot=received.snapshot();assert_eq!(snapshot["assessment"],"unbound");assert!(snapshot["suppliedBasis"].is_null());assert!(snapshot["account"].is_null());assert_eq!(snapshot["originalDocument"],definition);assert_eq!(received.source().original_bytes().unwrap(),bytes);
 let bytes=fixture("xt-result-record.example.valid.json");let received=ReceivedTrace::receive(ActualSelectedSource::read(files.write("rehearsal.json",&bytes)),RecordKind::XtResult,EvidenceKind::DefinitionOrRehearsal);assert_eq!(received.snapshot()["assessment"],"unbound");assert_eq!(received.source().original_bytes().unwrap(),bytes);
}
#[test]
fn xt_work_intake_does_not_borrow_previous_candidate_or_invent_configuration(){
 let files=Files::new();let mut session=TraceReceivingSession::default();session.read_selected(files.write("basis.json",&fixture("receiving/EXP-person-stated-basis.json")),RecordKind::ExaminationResult,EvidenceKind::NativeSupplier);
 let bytes=fixture("xt-work-account.example.valid.json");let id=session.read_selected(files.write("work.json",&bytes),RecordKind::XtWork,EvidenceKind::DefinitionOrRehearsal);let snapshot=session.import(id).unwrap().snapshot();assert_eq!(snapshot["assessment"],"unbound");assert!(snapshot["suppliedBasis"].is_null());assert!(snapshot["account"].is_null());assert_eq!(snapshot["originalDocument"],value("xt-work-account.example.valid.json"));assert_eq!(session.import(id).unwrap().source().original_bytes().unwrap(),bytes);assert!(snapshot["reason"].as_str().unwrap().contains("configuration"));assert_eq!(snapshot["countsTowardV4Exm24"],false);
}
#[test]
fn actual_byte_intake_retains_malformed_or_missing_date_without_default_or_upgrade(){
 let files=Files::new();let mut missing=value("receiving/EXP-person-stated-basis.json");missing.as_object_mut().unwrap().remove("date");
 for (bytes,expected) in [(vec![0xff,0x00],"refused_malformed"),(b"{".to_vec(),"refused_malformed"),(serde_json::to_vec(&missing).unwrap(),"refused_schema")]{
  let received=ReceivedTrace::receive(ActualSelectedSource::read(files.write("invalid.json",&bytes)),RecordKind::ExaminationResult,EvidenceKind::NativeSupplier);let snapshot=received.snapshot();assert_eq!(snapshot["assessment"],expected);assert_eq!(received.source().original_bytes().unwrap(),bytes);assert_eq!(snapshot["source"]["bufferIdentity"]["value"],util::sha256_hex(&bytes));assert!(snapshot["suppliedBasis"].is_null());assert_eq!(snapshot["nativeExamination"],"not_established");
 }
}
#[test]
fn bound_selected_sources_refuse_overlap_false_join_and_misclassified_evidence_raw(){
 let files=Files::new();for (name,kind,tier,reason) in [("EXP-overlap-refused.json",RecordKind::ExaminationResult,EvidenceKind::NativeSupplier,"both applicable"),("XT-false-joined-pass.json",RecordKind::XtResult,EvidenceKind::ActualHost,"DECISION-3"),("XT-unverified-joined-claim.json",RecordKind::XtResult,EvidenceKind::NativeSupplier,"misclassified")]{
  let bytes=fixture(&format!("receiving/{name}"));let original:Value=serde_json::from_slice(&bytes).unwrap();let received=ReceivedTrace::receive(ActualSelectedSource::read(files.write(name,&bytes)),kind,tier);let snapshot=received.snapshot();assert_eq!(snapshot["assessment"],"refused_semantic");assert!(snapshot["reason"].as_str().unwrap().contains(reason));assert_eq!(snapshot["originalDocument"],original);assert_eq!(received.source().original_bytes().unwrap(),bytes);assert_eq!(snapshot["source"]["bufferIdentity"]["value"],util::sha256_hex(&bytes));assert_eq!(snapshot["account"]["entries"][0]["claimState"],"refused");assert_eq!(snapshot["countsTowardV4Exm24"],false);assert_eq!(snapshot["countsTowardV4Exm25"],false);
 }
}
#[cfg(unix)]
#[test]
fn descriptor_guard_refuses_fifo_directory_device_and_missing_nonunicode_path_without_reading(){
 use std::os::unix::ffi::{OsStrExt,OsStringExt};let files=Files::new();let fifo=files.0.join("special.fifo");let name=std::ffi::CString::new(fifo.as_os_str().as_bytes()).unwrap();assert_eq!(unsafe{libc::mkfifo(name.as_ptr(),0o600)},0); // no writer, nonblocking open is required
 for path in [fifo,files.0.clone(),PathBuf::from("/dev/null")]{let source=ActualSelectedSource::read(path);let snapshot=source.snapshot();assert_eq!(snapshot["readState"],"unavailable");assert!(source.original_bytes().is_none());assert!(snapshot["bufferIdentity"].is_null());assert!(snapshot["reason"].as_str().unwrap().contains("regular"));}
 let path=files.0.join(std::ffi::OsString::from_vec(b"missing-\xff.json".to_vec()));let source=ActualSelectedSource::read(path.clone());let received=ReceivedTrace::receive(source,RecordKind::ExaminationResult,EvidenceKind::NativeSupplier);let snapshot=received.snapshot();assert_eq!(snapshot["source"]["selectedPath"],attachments::native_path_identity(&path));assert!(snapshot["source"]["pathDisplayLimit"].as_str().unwrap().contains("lossy"));assert!(snapshot["source"]["originalBytes"].is_null());assert!(snapshot["suppliedBasis"].is_null());serde_json::to_vec(&snapshot).unwrap();
}
#[test]
fn already_read_selected_buffer_is_consumed_without_opening_or_repairing_it(){
 let files=Files::new();let absent=files.0.join("no-longer-present.json");let bytes=fixture("receiving/EXP-person-stated-basis.json");let received=ReceivedTrace::receive(ActualSelectedSource::from_complete_selected_buffer(absent.clone(),bytes.clone()),RecordKind::ExaminationResult,EvidenceKind::NativeSupplier);assert!(!absent.exists());let snapshot=received.snapshot();assert_eq!(snapshot["assessment"],"received_supplied_record");assert_eq!(snapshot["source"]["readMechanism"],"supplied_selected_buffer");assert_eq!(received.source().original_bytes().unwrap(),bytes);assert_eq!(std::fs::read_dir(&files.0).unwrap().count(),0);
}
#[test]
fn metadata_reader_has_no_attachment_text_bound_or_implicit_truncation(){
 let files=Files::new();let mut doc=value("receiving/EXP-person-stated-basis.json");doc["blocked_by"]=Value::String("ILLUSTRATIVE supplied metadata; not an attempted run. ".repeat(6000));let bytes=serde_json::to_vec(&doc).unwrap();assert!(bytes.len()>262144);let received=ReceivedTrace::receive(ActualSelectedSource::read(files.write("metadata.json",&bytes)),RecordKind::ExaminationResult,EvidenceKind::NativeSupplier);assert_eq!(received.source().original_bytes().unwrap(),bytes);assert_eq!(received.snapshot()["assessment"],"received_supplied_record");assert_eq!(received.snapshot()["originalDocument"],doc);
}
#[test]
fn constructed_receiving_fixtures_keep_exact_declared_provenance(){
 for row in value("receiving/manifest.json").as_array().unwrap(){let bytes=fixture(&format!("receiving/{}",row["file"].as_str().unwrap()));assert_eq!(util::sha256_hex(&bytes),row["sha256"].as_str().unwrap());assert!(row["standing"].as_str().unwrap().contains("no actual"));}
 let source=value("exam.result-record.valid.examples.json");let mut original=source.as_array().unwrap().iter().find(|v|v["record_id"]=="EXP-EX-08").unwrap().clone();original["date"]["source"]="stated_by_person".into();assert_eq!(original,value("receiving/EXP-person-stated-basis.json"));
}
