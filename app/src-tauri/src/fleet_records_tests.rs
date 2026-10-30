//! Invented local file records, never native/person act or supplier witnesses.
use super::*;

const PACKET: &str = include_str!("../../../execution/PKG-06/DEL-06-01/Work/prototype/fixtures/FX-FL1/coordination.fleet.jsonl");
struct Fixture { root: PathBuf, project: PathBuf, store: records_store::Store }
impl Fixture {
    fn new() -> Self {
        let root = std::env::temp_dir().canonicalize().unwrap().join(crate::util::opaque_id("fleet-reader-").unwrap());
        let project = root.join("project");
        std::fs::create_dir_all(&project).unwrap();
        let store = records_store::Store {root:root.join("store"),placement:records_store::Placement::Test,limits:vec![]};
        records_store::use_store_for_test(Some(Ok(store.clone())));
        Self {root,project,store}
    }
    fn attached(&self) -> PathBuf { records_store::attach(&self.project,true).unwrap().dir.unwrap() }
    fn project_log(&self) -> PathBuf { self.project.join(FOLDER).join(LOG) }
    fn put(&self, path: &Path, bytes: &[u8]) {
        std::fs::create_dir_all(path.parent().unwrap()).unwrap();
        std::fs::write(path,bytes).unwrap();
    }
    fn row(&self, id: &str, status: &str) -> Vec<u8> {
        let value = json!({"format":"chirality.fleet.record","formatVersion":"0.1","recordId":id,
            "kind":"child_observed","undertaking":"fixture-undertaking","recorder":{"kind":"App","identity":"app-writer:fixture"},
            "writtenAt":"invented fixture time","body":{"childThread":"fixture-child","status":status,
                "observation":{"source":"invented fixture source","at":"fixture","pin":"fixture","standing":"observed"}}});
        validator().unwrap().validate(&value).unwrap();
        let mut bytes = serde_json::to_vec(&value).unwrap(); bytes.push(b'\n'); bytes
    }
    fn pair(&self, rows: &[Vec<u8>]) -> PathBuf {
        let dir = self.attached();
        let bytes = rows.concat();
        self.put(&self.project_log(),&bytes);
        let log = dir.join("fleet").join(LOG); self.put(&log,&bytes);
        log
    }
    fn read(&self) -> Value { crate::read_fleet_records_for_workspace(Some(&self.project)).unwrap() }
}
impl Drop for Fixture {
    fn drop(&mut self) {
        records_store::use_store_for_test(None);
        let _ = std::fs::remove_dir_all(&self.root);
    }
}
pub(super) fn inventory(root: &Path) -> BTreeMap<PathBuf,Value> {
    fn walk(root: &Path, path: &Path, out: &mut BTreeMap<PathBuf,Value>) {
        let meta = match std::fs::symlink_metadata(path) {Ok(m)=>m,Err(_)=>return};
        let body = if meta.is_file() {json!(crate::util::sha256_hex(&std::fs::read(path).unwrap()))}
            else if meta.file_type().is_symlink(){json!(std::fs::read_link(path).unwrap().to_string_lossy())}else{Value::Null};
        out.insert(path.strip_prefix(root).unwrap().to_owned(),json!({"device":meta.dev(),"inode":meta.ino(),"mode":meta.mode(),"links":meta.nlink(),"size":meta.len(),"mtime":meta.mtime(),"mtime_ns":meta.mtime_nsec(),"body":body}));
        if meta.is_dir() {for entry in std::fs::read_dir(path).unwrap(){walk(root,&entry.unwrap().path(),out);}}
    }
    let mut out=BTreeMap::new();walk(root,root,&mut out);out
}
fn observations(value: &Value) -> &Vec<Value> {value["coordination"]["appObservations"].as_array().unwrap()}
fn has_limit(value: &Value, text: &str) -> bool {value["limits"].as_array().unwrap().iter().any(|l|l["reason"].as_str().unwrap().contains(text))}

#[test]
fn fleet_reader_native_adapter_full_response() {
    let f=Fixture::new();let dir=f.attached();
    f.put(&f.project_log(),PACKET.as_bytes());
    let protected:Vec<u8>=PACKET.split_inclusive('\n').filter(|line| {
        let v:Value=serde_json::from_str(line).unwrap(); OBSERVED.contains(&v["kind"].as_str().unwrap())
    }).flat_map(str::as_bytes).copied().collect();
    f.put(&dir.join("fleet").join(LOG),&protected);
    f.put(&f.project.join(FOLDER).join("briefs/W1.json"),include_bytes!("../../../execution/PKG-06/DEL-06-01/Work/prototype/fixtures/FX-FL1/briefs/W1.json"));
    f.put(&f.project.join(FOLDER).join("graphs/FX-U1/r1.json"),include_bytes!("../../../execution/PKG-06/DEL-06-01/Work/prototype/fixtures/FX-FL1/graphs/FX-U1/r1.json"));
    let before=inventory(&f.root);let view=f.read();
    assert_eq!(inventory(&f.root),before,"actual native adapter read creates/changes no file or lock");
    assert_eq!(view["briefs"].as_array().unwrap().len(),1);assert_eq!(view["graphs"].as_array().unwrap().len(),1);
    assert_eq!(view["coordination"]["projectRecords"].as_array().unwrap().len(),18);
    assert_eq!(observations(&view).len(),protected.split_inclusive(|b|*b==b'\n').count());
    assert!(has_limit(&view,"identity method is unselected/unsupported"));
    assert!(view.get("currentGraph").is_none() && view.get("workState").is_none());
    assert!(crate::read_fleet_records_for_workspace(None).is_err());
    println!("FLEET_DTO:{}",serde_json::to_string(&view).unwrap());
}

#[test]
fn fleet_reader_never_initializes_an_absent_empty_or_unlinked_store() {
    for initialized in [false,true] {
        let f=Fixture::new();
        if initialized {std::fs::create_dir_all(&f.store.root).unwrap();}
        f.put(&f.project_log(),&f.row("fl:unlinked","fixture-status"));
        let before=inventory(&f.root);let view=f.read();
        assert_eq!(inventory(&f.root),before);
        assert!(observations(&view).is_empty());
        assert!(!f.project.join(records_store::PROJECT_LINK).exists());
        assert!(!f.store.root.join("store.json").exists());
        assert_eq!(view["coordination"]["protected"]["state"],"unavailable");
        assert!(view["coordination"]["projectRecords"][0]["protectedOrder"].is_null());
    }
}

#[test]
fn fleet_reader_protected_order_governs_replay_and_missing_project_rows() {
    let f=Fixture::new();let (old,new)=(f.row("fl:old","old-status"),f.row("fl:new","new-status"));
    f.pair(&[old.clone(),new.clone()]);
    f.put(&f.project_log(),&[new.clone(),old.clone(),old.clone()].concat());
    let before=inventory(&f.root);let view=f.read();
    assert_eq!(inventory(&f.root),before);
    assert_eq!(observations(&view).iter().map(|r|r["record"]["recordId"].as_str().unwrap()).collect::<Vec<_>>(),vec!["fl:old","fl:new"]);
    assert_eq!(observations(&view)[0]["projectCounterparts"].as_array().unwrap().len(),2);
    assert_eq!(view["coordination"]["projectRecords"][2]["protectedOrder"],1);
    assert!(has_limit(&view,"duplicate/conflicting recordId"));
    f.put(&f.project_log(),&new);
    let view=f.read();assert_eq!(observations(&view).len(),2);
    assert!(has_limit(&view,"no exact project counterpart"));
}

#[test]
fn fleet_reader_actual_adapter_retains_accepted_prefix_through_loss_rewrite_and_recovery() {
    // One live fixture/configuration: no Test store reset can clear the proof.
    let f=Fixture::new();let a=f.row("fl:accepted-a","original-a");let b=f.row("fl:accepted-b","original-b");
    let log=f.pair(&[a.clone(),b.clone()]);let original=[a.clone(),b.clone()].concat();
    assert_eq!(observations(&f.read()).len(),2);
    let assert_refused = || {
        let before=inventory(&f.root);let view=f.read();assert_eq!(inventory(&f.root),before);
        assert!(observations(&view).is_empty());
        assert!(view["coordination"]["governingStoreRecords"].as_array().unwrap().is_empty());
        assert_eq!(view["coordination"]["protectedLog"]["complete"],false);
        assert!(has_limit(&view,"previously accepted protected fleet history changed or disappeared"));
        assert!(view["coordination"]["projectRecords"].as_array().unwrap().iter().all(|row|row["protectedOrder"].is_null()));
    };
    f.put(&log,&a);f.put(&f.project_log(),&a);assert_refused();
    // Rewriting both copies under the old ID must not mint new App evidence.
    let rewrite=[a.clone(),f.row("fl:accepted-b","rewritten-b")].concat();
    f.put(&log,&rewrite);f.put(&f.project_log(),&rewrite);assert_refused();
    f.put(&log,b"");f.put(&f.project_log(),b"");assert_refused();
    std::fs::remove_file(&log).unwrap();assert_refused();
    let unknown=f.row("fl:recreated-unknown","not-the-accepted-history");
    f.put(&log,&unknown);f.put(&f.project_log(),&unknown);assert_refused();
    // A newly created descriptor at the same pathname cannot reset the prefix.
    let c=f.row("fl:accepted-c","legitimate-append");let restored=[original,c.clone()].concat();
    f.put(&log,&restored);f.put(&f.project_log(),&restored);
    let view=f.read();assert_eq!(observations(&view).len(),3);println!("NATIVE_LINK_MIXED_DTO:{}",serde_json::to_string(&view).unwrap());
    assert_eq!(view["coordination"]["protectedLog"]["complete"],true);
    assert!(!has_limit(&view,"previously accepted protected fleet history"));
    f.put(&log,&[a.clone(),b.clone()].concat());assert_refused();
    f.put(&log,&restored);
    let d=f.row("fl:accepted-d","next-append");let appended=[restored,d].concat();
    f.put(&log,&appended);f.put(&f.project_log(),&appended);
    let before=inventory(&f.root);assert_eq!(observations(&f.read()).len(),4);assert_eq!(inventory(&f.root),before);
}

#[test]
fn fleet_reader_accepts_prefix_only_after_a_complete_stable_native_snapshot() {
    let f=Fixture::new();let a=f.row("fl:stable-a","first");let b=f.row("fl:stable-b","second");
    let log=f.pair(&[a.clone(),b.clone()]);let changed=log.clone();
    AFTER_READ.with(|h|*h.borrow_mut()=Some(Box::new(move||std::fs::write(changed,b"missing-after-read").unwrap())));
    let view=f.read();assert!(observations(&view).is_empty());assert!(has_limit(&view,"changed while reading"));
    f.put(&log,&[a.clone(),b"{\n".to_vec()].concat());
    let view=f.read();assert!(observations(&view).is_empty());
    // Neither the unstable two-row snapshot nor the invalid append was accepted.
    f.put(&log,&a);f.put(&f.project_log(),&a);assert_eq!(observations(&f.read()).len(),1);
    f.put(&log,&[a,b].concat());assert_eq!(observations(&f.read()).len(),2);
}

#[test]
fn fleet_reader_counterparts_are_exact_bytes_including_whitespace_key_order_and_line_ending() {
    let f=Fixture::new();let original=f.row("fl:exact","original");f.pair(&[original.clone()]);
    let value:Value=serde_json::from_slice(&original).unwrap();
    let compact=serde_json::to_string(&value).unwrap();
    let reordered=format!("{{\"recordId\":\"fl:exact\",\"body\":{},\"format\":\"chirality.fleet.record\",\"formatVersion\":\"0.1\",\"kind\":\"child_observed\",\"recorder\":{},\"undertaking\":\"fixture-undertaking\",\"writtenAt\":\"invented fixture time\"}}\n",value["body"],value["recorder"]);
    for changed in [format!(" {compact}\n").into_bytes(),format!("{compact}\r\n").into_bytes(),reordered.into_bytes(),f.row("fl:exact","changed-status")] {
        assert_ne!(changed,original);f.put(&f.project_log(),&changed);let view=f.read();
        assert_eq!(observations(&view).len(),1,"healthy protected row is not erased by project changes");
        assert!(view["coordination"]["projectRecords"][0]["protectedOrder"].is_null());
        assert!(has_limit(&view,"lacks a healthy exact protected counterpart"));
    }
}

#[test]
fn fleet_reader_an_unread_or_duplicate_protected_line_withholds_the_entire_app_observation_projection() {
    for suffix in [b"{".to_vec(),b"not JSON\n".to_vec(),b"{}\n".to_vec()] {
        let f=Fixture::new();let original=f.row("fl:prefix","prefix");let log=f.pair(&[original.clone()]);
        f.put(&log,&[original,suffix].concat());let view=f.read();assert!(observations(&view).is_empty());
        assert!(has_limit(&view,"lacks a healthy exact protected counterpart"));
    }
    for conflicting in [false,true] {
        let f=Fixture::new();let first=f.row("fl:duplicate","first");let second=if conflicting {f.row("fl:duplicate","second")}else{first.clone()};
        f.pair(&[first,second]);let view=f.read();assert!(observations(&view).is_empty());assert!(has_limit(&view,"duplicate/conflicting"));
    }
}

#[test]
fn fleet_reader_unknown_and_torn_project_sources_are_limits_and_never_state() {
    let f=Fixture::new();f.attached();let mut unknown:Value=serde_json::from_slice(&f.row("fl:unknown","fixture")).unwrap();
    unknown["formatVersion"]=json!("9.9");
    f.put(&f.project_log(),format!("{unknown}\n{{").as_bytes());
    let mut invalid=unknown.clone();invalid["formatVersion"]=json!("0.1");invalid["kind"]=json!("brief");
    f.put(&f.project.join(FOLDER).join("briefs/bad.json"),serde_json::to_string(&invalid).unwrap().as_bytes());
    f.put(&f.project.join(FOLDER).join("graphs/not-a-folder.json"),b"{}");
    let view=f.read();assert!(has_limit(&view,"unknown fleet format/version"));assert!(has_limit(&view,"unclosed final line"));assert!(has_limit(&view,"schema invalid"));
    assert!(view["coordination"]["projectRecords"].as_array().unwrap().is_empty());
    assert!(view.get("ready").is_none() && view.get("currentGraph").is_none());
}

#[test]
fn fleet_reader_source_changes_and_alias_changes_withhold_protected_authority() {
    let f=Fixture::new();let log=f.pair(&[f.row("fl:race","old")]);
    let new=f.row("fl:race","new");
    AFTER_READ.with(|h|*h.borrow_mut()=Some(Box::new(move||std::fs::write(log,new).unwrap())));
    let view=f.read();assert!(observations(&view).is_empty());assert!(has_limit(&view,"changed while reading"));
    let project_alias=f.root.join("project-alias");let store_alias=f.root.join("store-alias");
    std::os::unix::fs::symlink(&f.project,&project_alias).unwrap();std::os::unix::fs::symlink(&f.store.root,&store_alias).unwrap();
    let mut aliased=f.store.clone();aliased.root=store_alias;records_store::use_store_for_test(Some(Ok(aliased)));
    let before=inventory(&f.root);let view=crate::read_fleet_records_for_workspace(Some(&project_alias)).unwrap();
    assert_eq!(inventory(&f.root),before);assert_eq!(view["project"]["canonicalRoot"],f.project.to_string_lossy().as_ref());
    assert_eq!(observations(&view).len(),1,"canonical configured aliases retain only protected sources");
}

#[test]
fn fleet_reader_identity_refusal_and_disposal_preserve_files_without_restoring_store_rows() {
    let f=Fixture::new();let log=f.pair(&[f.row("fl:retained","historical fixture")]);
    let link=f.project.join(records_store::PROJECT_LINK);
    let original_link=std::fs::read(&link).unwrap();std::fs::remove_file(&link).unwrap();
    let before=inventory(&f.root);let view=f.read();assert_eq!(inventory(&f.root),before);
    assert!(observations(&view).is_empty());assert_eq!(view["coordination"]["protected"]["state"],"unavailable");
    std::fs::write(&link,&original_link).unwrap();
    let actor=crate::act_control::person(Some("Invented fixture person"),Some("fixture-os"));
    let observed=json!({"fixture":"source test callback, no live person's act"});
    let close=crate::records_retention::prepare(&f.project,"close",None,&actor,&observed).unwrap();
    crate::records_retention::apply(close,&actor,&observed).unwrap();
    let before=inventory(&f.root);assert_eq!(observations(&f.read()).len(),1);assert_eq!(inventory(&f.root),before);
    let bag=f.root.join("closed-bag");crate::records_export::export(&f.project,&bag).unwrap();
    let dispose=crate::records_retention::prepare(&f.project,"dispose",Some(&bag),&actor,&observed).unwrap();
    crate::records_retention::apply(dispose,&actor,&observed).unwrap();
    let before=inventory(&f.root);let view=f.read();assert_eq!(inventory(&f.root),before);
    assert!(observations(&view).is_empty());assert!(view["coordination"]["protectedRecords"].as_array().unwrap().is_empty());
    assert!(has_limit(&view,"disposed"));assert_eq!(view["coordination"]["projectRecords"].as_array().unwrap().len(),1,"co-written source survives as a claim");
    f.put(&log,&f.row("fl:retained","copied back after disposal"));
    let before=inventory(&f.root);let view=f.read();assert_eq!(inventory(&f.root),before);assert!(observations(&view).is_empty());
    assert!(!view.to_string().contains("copied back after disposal"),"terminal payload is not read even if recreated");
}

#[test]
fn fleet_reader_missing_or_busy_existing_admission_is_not_created_or_waited_on() {
    use std::os::fd::AsRawFd;
    let f=Fixture::new();let log=f.pair(&[f.row("fl:guard","fixture")]);
    let dir=log.parent().unwrap().parent().unwrap();
    let gate=f.store.root.join("administration").join(dir.file_name().unwrap()).join(".admission.lock");
    let guard=crate::records_index::open_log(&gate).unwrap();
    assert_eq!(unsafe{libc::flock(guard.as_raw_fd(),libc::LOCK_EX | libc::LOCK_NB)},0);
    let before=inventory(&f.root);let view=f.read();assert_eq!(inventory(&f.root),before);
    assert!(observations(&view).is_empty());assert!(has_limit(&view,"admission busy"));
    drop(guard);
    std::fs::remove_file(&gate).unwrap();let before=inventory(&f.root);let view=f.read();
    assert_eq!(inventory(&f.root),before);assert!(observations(&view).is_empty());assert!(has_limit(&view,"admission file absent"));
    assert!(!gate.exists());
}

#[test]
fn fleet_reader_actual_temporary_override_keeps_store_order_without_protected_app_provenance() {
    let f=Fixture::new();let old=f.row("fl:temporary-old","old");let new=f.row("fl:temporary-new","new");
    f.pair(&[old.clone(),new.clone()]);f.put(&f.project_log(),&[new,old].concat());
    let actual=records_store::for_app(Some(f.store.root.clone()),Err("unused with explicit override".into()),true,Some(&f.project),&[]).unwrap();
    assert_eq!(actual.placement,records_store::Placement::Override);
    records_store::use_store_for_test(Some(Ok(actual)));
    let before=inventory(&f.root);let view=f.read();assert_eq!(inventory(&f.root),before);
    assert!(observations(&view).is_empty());assert_eq!(view["coordination"]["protected"]["provenanceProtected"],false);
    let stored=view["coordination"]["governingStoreRecords"].as_array().unwrap();
    assert_eq!(stored.len(),2);assert_eq!(stored[0]["record"]["recordId"],"fl:temporary-old");assert_eq!(stored[1]["record"]["recordId"],"fl:temporary-new");
    assert_eq!(view["coordination"]["projectRecords"][0]["storeOrder"],2);
    assert!(view["coordination"]["projectRecords"][0]["protectedOrder"].is_null());
    assert!(has_limit(&view,"placement cannot establish protected App provenance"));
    assert!(crate::records_store::write_dir(&f.project).is_ok(),"existing allowed development recording is unchanged");
}

#[test]
fn fleet_reader_directory_parent_swap_does_not_read_or_name_the_second_fixture() {
    let f=Fixture::new();f.pair(&[f.row("fl:original","original")]);
    let folder=f.project.join(FOLDER);
    let second=f.root.join("second-fleet");f.put(&second.join("briefs/foreign-private-name.json"),b"{}");
    let held=f.root.join("original-fleet");let (changed,moved)=(folder.clone(),held.clone());
    let _hook=crate::records_index::log_open_hook_for_test(&folder,None,0,move||{
        std::fs::rename(&changed,&moved).unwrap();std::os::unix::fs::symlink(&second,&changed).unwrap();
    });
    let value=f.read();assert!(held.is_dir());assert!(!value.to_string().contains("foreign-private-name"));
    assert!(has_limit(&value,"symlink") || has_limit(&value,"Not a directory"));
    assert!(observations(&value).is_empty());
}

#[test]
fn fleet_reader_preserves_an_already_opened_store_identity_without_repairing_it() {
    let f=Fixture::new();f.pair(&[f.row("fl:store-identity","fixture")]);
    let path=f.store.root.join("store.json");let mut identity:Value=serde_json::from_slice(&std::fs::read(&path).unwrap()).unwrap();
    identity["storeId"]=json!("invented-replacement-store");
    std::fs::write(&path,serde_json::to_vec(&identity).unwrap()).unwrap();
    let before=inventory(&f.root);let value=f.read();assert_eq!(inventory(&f.root),before);
    assert!(observations(&value).is_empty());assert!(has_limit(&value,"no silent reassociation"));
}

#[test]
fn fleet_reader_refuses_a_controlled_pipe_and_links_without_waiting_or_following() {
    use std::os::unix::{ffi::OsStrExt,fs::OpenOptionsExt};
    let f=Fixture::new();f.attached();let pipe=f.project_log();std::fs::create_dir_all(pipe.parent().unwrap()).unwrap();
    let name=std::ffi::CString::new(pipe.as_os_str().as_bytes()).unwrap();assert_eq!(unsafe{libc::mkfifo(name.as_ptr(),0o600)},0);
    let writer=std::fs::OpenOptions::new().read(true).write(true).custom_flags(libc::O_NONBLOCK).open(&pipe).unwrap();
    let project=f.project.clone();let store=f.store.clone();let (send,recv)=std::sync::mpsc::channel();
    let worker=std::thread::spawn(move||{records_store::use_store_for_test(Some(Ok(store)));send.send(crate::read_fleet_records_for_workspace(Some(&project))).unwrap();records_store::use_store_for_test(None);});
    let early=recv.recv_timeout(std::time::Duration::from_secs(2));let prompt=early.is_ok();drop(writer);
    let value=early.unwrap_or_else(|_|recv.recv_timeout(std::time::Duration::from_secs(2)).expect("owned writer closed"));
    worker.join().unwrap();assert!(prompt);let value=value.unwrap();assert!(has_limit(&value,"not a regular single-link file"));
    std::fs::remove_file(&pipe).unwrap();
    let second=f.root.join("second-fixture.jsonl");f.put(&second,&f.row("fl:second","NEVER-RETURNED"));
    std::os::unix::fs::symlink(second,&pipe).unwrap();let value=f.read();assert!(has_limit(&value,"symlink"));assert!(!value.to_string().contains("NEVER-RETURNED"));
}

fn ordinary_legacy(f: &Fixture) -> (PathBuf,String,Vec<u8>) {
    let log=f.project.join(".chirality/records").join(storage::log_rel(Some("run:fleet-legacy"),"writer:legacy-fixture"));
    let id=crate::util::opaque_id("rec:app:legacy-fixture-").unwrap();
    let entry=crate::records::envelope("evidence_limit",&crate::records::APP_WRITER,
        json!({"label":"unresolvable reference","subjectRef":"invented ordinary legacy evidence"}),
        id.clone(),1,Some("run:fleet-legacy"),Some("2026-10-13T00:00:00Z"));
    let bytes=crate::record_lines::fixture::rechain(format!("{entry}\n").as_bytes());
    f.put(&log,&bytes);
    let (read,limits)=crate::records::read_log(&log);assert!(limits.is_empty());assert_eq!(read.len(),1);
    (log,id,bytes)
}
fn ordinary_consumers(f: &Fixture, original: &Path, id: &str, capability: &crate::records_access::RecordsCapability, n: u64) {
    use crate::records_access::{Call,ProjectPaths,RecordsSource};
    assert!(storage::discover(&f.project).unwrap().iter().any(|path|path==original));
    let full=ProjectPaths::new(&f.project).read();assert_eq!(full.entries.len(),1);assert_eq!(full.entries[0].entry["recordId"],id);
    crate::records_index::with_index(&f.project,|ix|{
        assert!(ix.holds(id));assert_eq!(ix.entries_with(id).unwrap().len(),1);
        assert!(!ix.holds("fl:manual-fleet"));assert!(ix.limits().is_empty());
    });
    let call=Call {app_session:"app-session:invented".into(),generation:"generation:invented".into(),request:json!(n),
        thread:"thread:invented".into(),turn:"turn:invented".into(),call:format!("call:{n}"),
        arguments:json!({"operation":"read_run","run":"run:fleet-legacy"})};
    let answer=capability.answer(&call,Some(f.project.to_str().unwrap()));assert_eq!(answer["success"],true);
    let packet:Value=serde_json::from_str(answer["contentItems"][0]["text"].as_str().unwrap()).unwrap();
    assert_eq!(packet["items"].as_array().unwrap().len(),1);assert!(packet.to_string().contains(id));
    assert!(!packet.to_string().contains("fl:manual-fleet"),"fleet never enters the RS capability");
    assert!(!records_store::home(&f.project).unwrap().store_mode,"ordinary readers/read log/index do not change the RS home before import");
}

#[test]
fn fleet_payload_preserves_unimported_legacy_readers_and_explicit_import() {
    for with_fleet in [false,true] {
        let f=Fixture::new();let dir=f.attached();let (original,id,bytes)=ordinary_legacy(&f);
        let capability=crate::records_access::RecordsCapability::new(&f.project).unwrap();
        ordinary_consumers(&f,&original,&id,&capability,1);
        let fleet=with_fleet.then(||{
            let log=f.pair(&[f.row("fl:manual-fleet","invented supported payload")]);
            assert_eq!(observations(&f.read()).len(),1);log
        });
        ordinary_consumers(&f,&original,&id,&capability,2);
        let census=records_store::legacy_census(&f.project).unwrap();assert_eq!(census.len(),1);
        assert!(records_store::write_dir(&f.project).unwrap_err().contains("import needed"));
        let bag=f.root.join("refused-before-import");
        assert!(crate::records_export::export(&f.project,&bag).unwrap_err().contains("need import"));assert!(!bag.exists());
        records_store::interrupt_import_for_test(Some(0),false);
        assert!(records_store::import(&f.project).unwrap_err().contains("interrupted"));
        records_store::interrupt_import_for_test(None,false);
        ordinary_consumers(&f,&original,&id,&capability,3);
        assert!(records_store::write_dir(&f.project).unwrap_err().contains("import incomplete"));
        assert!(crate::records_export::export(&f.project,&bag).unwrap_err().contains("import incomplete"));
        records_store::import(&f.project).unwrap();
        assert!(records_store::home(&f.project).unwrap().store_mode);
        assert!(!storage::discover(&f.project).unwrap().contains(&original));
        assert_eq!(std::fs::read(&original).unwrap(),bytes,"explicit import preserves original bytes");
        assert_eq!(std::fs::read(dir.join(&census[0].copy)).unwrap(),bytes);
        assert!(records_store::write_dir(&f.project).is_ok());
        crate::records_index::with_index(&f.project,|ix|assert_eq!(ix.entries_with(&id).unwrap().len(),1));
        let bag=f.root.join("after-import");crate::records_export::export(&f.project,&bag).unwrap();
        assert_eq!(std::fs::read(bag.join("data").join(&census[0].copy)).unwrap(),bytes);
        if let Some(fleet)=fleet {assert_eq!(std::fs::read(bag.join("data/fleet").join(LOG)).unwrap(),std::fs::read(fleet).unwrap());}
    }
}

#[test]
fn capture_control_only_does_not_establish_rs_home_and_unknown_import_refuses_fleet_export() {
    let f=Fixture::new();let log=f.pair(&[f.row("fl:manual-fleet","invented")]);let dir=log.parent().unwrap().parent().unwrap();
    let captures=dir.join("captures");std::fs::create_dir(&captures).unwrap();
    assert!(!records_store::home(&f.project).unwrap().store_mode);
    f.put(&captures.join(".capture.lock"),b"");assert!(!records_store::home(&f.project).unwrap().store_mode);
    f.put(&captures.join("unknown-non-control"),b"invented payload");assert!(records_store::home(&f.project).unwrap().store_mode);
    std::fs::remove_file(captures.join("unknown-non-control")).unwrap();
    let control=captures.join(".capture.lock");std::fs::remove_file(&control).unwrap();
    let other=f.root.join("invented-control-link-target");f.put(&other,b"");std::os::unix::fs::symlink(&other,&control).unwrap();
    assert!(records_store::home(&f.project).unwrap().store_mode,"unsafe control is conservative unknown payload");
    std::fs::remove_file(control).unwrap();
    for bytes in [b"not JSON\n".as_slice(),b"{}\n".as_slice(),b"{".as_slice()] {
        f.put(&dir.join("imports.jsonl"),bytes);
        assert!(crate::records_export::export(&f.project,&f.root.join("refused-unknown-import")).is_err());
    }
}

#[test]
fn fleet_only_protected_payload_exports_without_joining_rs_readers_or_import_census() {
    let f=Fixture::new();let bytes=f.row("fl:fleet-payload","fixture");let log=f.pair(&[bytes.clone()]);
    assert!(records_store::legacy_census(&f.project).unwrap().is_empty());
    assert!(storage::discover(&f.project).unwrap().iter().all(|p|p!=&log && p!=&f.project_log()));
    let bag=f.root.join("bag");
    crate::records_export::export(&f.project,&bag).unwrap();
    assert_eq!(std::fs::read(bag.join("data/fleet").join(LOG)).unwrap(),bytes);
    let heads:Value=serde_json::from_slice(&std::fs::read(bag.join("records-chain-heads.json")).unwrap()).unwrap();
    assert_eq!(heads["logs"],json!([]),"fleet is not an RS log or chain-head source");
    assert!(!records_store::home(&f.project).unwrap().store_mode,"fleet export and its capture-control file do not establish an ordinary RS home");
    let capability=crate::records_access::RecordsCapability::new(&f.project).unwrap();
    crate::records_index::with_index(&f.project,|ix|assert!(ix.paths().is_empty()));
    let (original,id,_)=ordinary_legacy(&f);ordinary_consumers(&f,&original,&id,&capability,1);
    assert!(records_store::write_dir(&f.project).unwrap_err().contains("import needed"));
    assert!(crate::records_export::export(&f.project,&f.root.join("refused-later-legacy")).unwrap_err().contains("need import"));
}

#[test]
fn fleet_reader_native_links_mixed_profile_keeps_legacy_quoted_and_mechanical_separate(){
 let f=Fixture::new();let g=json!({"appSession":"invented-session","home":"invented-native-home","spawnCounter":1});let native=json!({"format":"chirality.fleet.record","formatVersion":"0.2","observationId":"fl:app:invented-native-link","kind":"related_conversation","recorder":{"kind":"App","identity":"app-writer:local"},"observedAt":"invented observation","body":{"relation":"forked from","source":{"threadId":"same-source","generation":g},"thread":{"threadId":"same-fork","generation":g},"nativeHome":{"homeId":"invented-native-home","root":crate::attachments::native_path_identity(&f.project),"physical":{"device":1,"inode":1}},"rpc":{"method":"thread/fork","requestId":1,"requestRef":"invented:rpc-1"},"typesPin":crate::hosting::DECLARED_PIN}});let limit=json!({"format":"chirality.fleet.record","formatVersion":"0.2","observationId":"fl:app:invented-copy-limit","kind":"recording_limit","recorder":{"kind":"App","identity":"app-writer:local"},"observedAt":"invented later observation","body":{"originalObservationId":native["observationId"],"phase":"project","statement":"Invented copy failure; native success unchanged"}});let line=|r:&Value|{let mut bytes=serde_json::to_vec(r).unwrap();bytes.push(b'\n');validate_line(&bytes).unwrap();bytes};f.pair(&[f.row("fl:quoted-old","old undertaking label"),line(&native),line(&limit)]);let before=inventory(&f.root);let view=f.read();assert_eq!(inventory(&f.root),before);assert_eq!(view["coordination"]["nativeRelationships"].as_array().unwrap().len(),1);assert_eq!(view["coordination"]["recordingEvents"].as_array().unwrap().len(),1);assert_eq!(view["coordination"]["nativeRelationships"][0]["record"],native);assert!(view["coordination"]["governingStoreRecords"][0]["standing"].as_str().unwrap().contains("undertaking/thread fields establish no native"));assert_eq!(observations(&view).len(),3);println!("NATIVE_LINK_MIXED_DTO:{}",serde_json::to_string(&view).unwrap());
 let conflict_fixture=Fixture::new();let mut other=native.clone();other["observationId"]=json!("fl:app:duplicate-native-receipt");other["body"]["thread"]["threadId"]=json!("conflicting-fork");conflict_fixture.pair(&[line(&native),line(&other)]);let view=conflict_fixture.read();assert!(view["coordination"]["nativeRelationships"].as_array().unwrap().is_empty());assert!(has_limit(&view,"duplicate/conflicting original native request identity"));assert_eq!(view["coordination"]["protectedLog"]["complete"],false);
}

#[test]
fn fleet_log_offsets_include_every_source_byte_and_crossing_imported_lines_stay_quoted() {
    let f = Fixture::new();
    let mut first = f.row("fl:offset-first", "first");
    first.pop();
    first.extend_from_slice(b"\r\n");
    let second = f.row("fl:offset-second", "second");
    let invalid = b"not JSON\n";
    let bytes = [first.as_slice(), invalid, second.as_slice()].concat();
    f.put(&f.project_log(), &bytes);
    let mut census = Census::default();
    let mut limits = Vec::new();
    let log = read_log(&mut census, &f.project_log(), &f.project, false, validator().unwrap(), &mut limits);
    assert!(!log.complete);
    assert_eq!(log.rows.len(), 2);
    assert_eq!(log.rows[0].log_end, Some(first.len() as u64));
    assert_eq!(log.rows[1].log_end, Some(bytes.len() as u64));
    let second_start = (first.len() + invalid.len()) as u64;
    assert!(!log.rows[0].follows_quoted_prefix(first.len() as u64));
    assert!(log.rows[1].follows_quoted_prefix(second_start));
    assert!(!log.rows[1].follows_quoted_prefix(second_start + 1));
    assert!(!log.rows[1].follows_quoted_prefix(bytes.len() as u64 - 1),
        "adding the newline to an imported unterminated row cannot make it a local observation");
    assert!(log.rows[0].follows_quoted_prefix(0));
}

fn native_package_row(f: &Fixture, id: &str, request: u64) -> Vec<u8> {
    let generation = json!({"appSession":"invented-package-session","home":"invented-package-home","spawnCounter":1});
    let record = json!({"format":"chirality.fleet.record","formatVersion":"0.2","observationId":id,
        "kind":"related_conversation","recorder":{"kind":"App","identity":"app-writer:local"},
        "observedAt":"invented package observation","body":{"relation":"forked from",
            "source":{"threadId":"invented-source","generation":generation},
            "thread":{"threadId":format!("invented-child-{request}"),"generation":generation},
            "nativeHome":{"homeId":"invented-package-home","root":crate::attachments::native_path_identity(&f.project),"physical":{"device":1,"inode":1}},
            "rpc":{"method":"thread/fork","requestId":request,"requestRef":format!("invented:package-rpc-{request}")},
            "typesPin":crate::hosting::DECLARED_PIN}});
    let mut bytes = serde_json::to_vec(&record).unwrap();
    bytes.push(b'\n');
    validate_line(&bytes).unwrap();
    bytes
}

fn restore_fleet_package(f: &Fixture, log: &Path, remove: bool) -> Value {
    let bag = f.root.join("invented-package");
    crate::records_export::export(&f.project, &bag).unwrap();
    if remove { std::fs::remove_file(log).unwrap(); }
    let actor = crate::act_control::person(Some("Invented package fixture"), Some("fixture-os"));
    let observed = json!({"fixture":"source-only package import stand-in; no live person's act"});
    let plan = records_store::package::prepare(&f.project, &bag, &actor, &observed).unwrap();
    records_store::package::apply(plan, &actor, &observed).unwrap()
}

#[test]
fn imported_native_relationship_claims_stay_quoted_and_later_local_append_has_its_own_provenance() {
    let f = Fixture::new();
    let imported = native_package_row(&f, "fl:app:invented-imported-native", 1);
    let legacy = f.row("fl:invented-imported-legacy", "imported claim");
    let log = f.pair(&[imported.clone(), legacy.clone()]);
    restore_fleet_package(&f, &log, true);
    let before = inventory(&f.root);
    let view = f.read();
    assert_eq!(inventory(&f.root), before, "package-origin inspection is read-only");
    assert!(observations(&view).is_empty());
    assert!(view["coordination"]["nativeRelationships"].as_array().unwrap().is_empty());
    let governing = view["coordination"]["governingStoreRecords"].as_array().unwrap();
    assert_eq!(governing.len(), 2);
    for (n, row) in governing.iter().enumerate() {
        assert_eq!(row["storeOrder"], n + 1);
        assert!(row["protectedOrder"].is_null());
        assert!(row["standing"].as_str().unwrap().contains("imported package row"));
        assert_eq!(row["projectCounterparts"].as_array().unwrap().len(), 1);
        let counterpart = &view["coordination"]["projectRecords"][n];
        assert_eq!(counterpart["storeOrder"], n + 1);
        assert!(counterpart["protectedOrder"].is_null());
        assert!(counterpart["reconciliation"].as_str().unwrap().contains("imported package counterpart"));
    }
    assert!(has_limit(&view, "imported package prefix is quoted evidence"));

    // This direct fixture append stands for a later App-produced observation;
    // the imported bytes remain an exact prefix and acquire no new authority.
    let local = native_package_row(&f, "fl:app:invented-local-after-import", 2);
    let bytes = [imported, legacy, local].concat();
    f.put(&log, &bytes);
    f.put(&f.project_log(), &bytes);
    let view = f.read();
    assert_eq!(observations(&view).len(), 1);
    assert_eq!(observations(&view)[0]["record"]["observationId"], "fl:app:invented-local-after-import");
    assert_eq!(observations(&view)[0]["protectedOrder"], 3);
    assert_eq!(view["coordination"]["nativeRelationships"].as_array().unwrap().len(), 1);
    assert!(view["coordination"]["projectRecords"][0]["protectedOrder"].is_null());
    assert_eq!(view["coordination"]["projectRecords"][2]["protectedOrder"], 3);
}

#[test]
fn exact_existing_local_fleet_log_keeps_provenance_during_idempotent_package_import() {
    let f = Fixture::new();
    let log = f.pair(&[native_package_row(&f, "fl:app:unchanged-local-package", 1)]);
    assert_eq!(observations(&f.read()).len(), 1);
    restore_fleet_package(&f, &log, false);
    let view = f.read();
    assert_eq!(observations(&view).len(), 1);
    assert_eq!(view["coordination"]["nativeRelationships"].as_array().unwrap().len(), 1);
    assert!(!has_limit(&view, "imported package prefix is quoted evidence"));
}

#[test]
fn changed_imported_prefix_withholds_provenance_for_later_local_rows() {
    let f = Fixture::new();
    let original = native_package_row(&f, "fl:app:imported-prefix-before-change", 1);
    let log = f.pair(&[original]);
    restore_fleet_package(&f, &log, true);
    let changed = native_package_row(&f, "fl:app:imported-prefix-was-changed", 8);
    let local = native_package_row(&f, "fl:app:local-after-prefix-change", 2);
    let bytes = [changed, local].concat();
    f.put(&log, &bytes);
    f.put(&f.project_log(), &bytes);
    let view = f.read();
    assert!(observations(&view).is_empty());
    assert!(view["coordination"]["nativeRelationships"].as_array().unwrap().is_empty());
    assert!(has_limit(&view, "imported observation prefix changed"));
    assert_eq!(view["coordination"]["governingStoreRecords"].as_array().unwrap().len(), 2,
        "current stable bytes remain quoted evidence even though origin proof fails");
    assert!(view["coordination"]["projectRecords"].as_array().unwrap().iter().all(|row|row["protectedOrder"].is_null()));
}

#[test]
fn changed_package_origin_receipt_during_fleet_read_withholds_all_app_provenance() {
    let f = Fixture::new();
    let imported = native_package_row(&f, "fl:app:receipt-race-imported", 1);
    let log = f.pair(&[imported.clone()]);
    restore_fleet_package(&f, &log, true);
    let local = native_package_row(&f, "fl:app:receipt-race-local", 2);
    let bytes = [imported, local].concat();
    f.put(&log, &bytes);
    f.put(&f.project_log(), &bytes);
    let dir = log.parent().unwrap().parent().unwrap();
    let receipt = std::fs::read_dir(dir.join("package-imports")).unwrap().next().unwrap().unwrap().path();
    AFTER_READ.with(|h| *h.borrow_mut() = Some(Box::new(move || {
        let mut bytes = std::fs::read(&receipt).unwrap();
        bytes.push(b' ');
        std::fs::write(&receipt, bytes).unwrap();
    })));
    let view = f.read();
    assert!(observations(&view).is_empty());
    assert!(view["coordination"]["nativeRelationships"].as_array().unwrap().is_empty());
    assert!(has_limit(&view, "package provenance unavailable after reading"));
    assert!(view["coordination"]["projectRecords"].as_array().unwrap().iter().all(|row|row["protectedOrder"].is_null()));
}

#[test]
fn finishing_an_imported_unterminated_native_row_does_not_turn_it_into_a_local_observation() {
    let f = Fixture::new();
    let mut imported = native_package_row(&f, "fl:app:imported-without-line-ending", 1);
    imported.pop();
    let log = f.pair(&[imported.clone()]);
    restore_fleet_package(&f, &log, true);
    imported.push(b'\n');
    let local = native_package_row(&f, "fl:app:local-after-finished-imported-line", 2);
    let bytes = [imported, local].concat();
    f.put(&log, &bytes);
    f.put(&f.project_log(), &bytes);
    let view = f.read();
    assert_eq!(observations(&view).len(), 1);
    assert_eq!(observations(&view)[0]["record"]["observationId"], "fl:app:local-after-finished-imported-line");
    assert_eq!(view["coordination"]["nativeRelationships"].as_array().unwrap().len(), 1);
    assert!(view["coordination"]["governingStoreRecords"][0]["protectedOrder"].is_null());
    assert_eq!(view["coordination"]["governingStoreRecords"][1]["protectedOrder"], 2);
}

#[test]
fn replacing_a_package_origin_receipt_with_identical_bytes_during_read_withholds_provenance() {
    let f = Fixture::new();
    let imported = native_package_row(&f, "fl:app:receipt-replacement-imported", 1);
    let log = f.pair(&[imported.clone()]);
    restore_fleet_package(&f, &log, true);
    let local = native_package_row(&f, "fl:app:receipt-replacement-local", 2);
    let bytes = [imported, local].concat();
    f.put(&log, &bytes);
    f.put(&f.project_log(), &bytes);
    let dir = log.parent().unwrap().parent().unwrap();
    let receipt = std::fs::read_dir(dir.join("package-imports")).unwrap().next().unwrap().unwrap().path();
    let original = f.root.join("original-receipt-moved-during-read");
    AFTER_READ.with(|h| *h.borrow_mut() = Some(Box::new(move || {
        let bytes = std::fs::read(&receipt).unwrap();
        std::fs::rename(&receipt, original).unwrap();
        std::fs::write(&receipt, bytes).unwrap();
    })));
    let view = f.read();
    assert!(observations(&view).is_empty());
    assert!(view["coordination"]["nativeRelationships"].as_array().unwrap().is_empty());
    assert!(has_limit(&view, "package provenance changed while reading"));
    assert_eq!(view["coordination"]["governingStoreRecords"].as_array().unwrap().len(), 2,
        "stable Fleet bytes keep their quoted store order when only provenance sources change");
}
