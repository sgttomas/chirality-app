// WR TX-5 / SQ-END, (d), (j) restart residuals. Included in `workflow_root_tests`
// (runtime_session.rs), so the Peer fixture and its helpers are in scope.

/// The WR run-start `run_text` record of `run` in the fixture project.
fn run_start_record(peer:&Peer,run:&str)->crate::workflow_workspace::publication::ResolvedRecord{
    let project=crate::workflow_workspace::publication::ProjectRecords::open(&peer.fixture.root).unwrap();
    project.list_references().unwrap().into_iter().filter_map(|r|project.resolve(&r).ok())
        .find(|r|r.body()["record_kind"]=="run_text"&&r.body()["purpose"]=="run start"&&r.body()["run"]==run).expect("run-start record")
}
fn restart_fact(id:&str,thread:&str)->Value{
    json!({"kind":"app_restart_interruption","eventId":id,"appSession":"app-session:now","at":"2026-10-10T00:00:00Z","standing":"App-observed","threadId":thread,"home":"H-acct","priorSession":"app-session:before","priorSessionEnd":"ended-without-record","liveTurnsAtEnd":[{"threadId":thread,"turnId":"turn"}]})
}
fn index_row(thread:&str,tags:Value)->Value{
    json!({"kind":"conversation_index","session":"app-session:before","at":"2026-10-09T00:00:00Z","threadId":thread,"home":"H-acct","project":"fixture App project","tags":tags,"lastObservedExecution":{"state":"turn-live","at":"2026-10-09T00:00:00Z"}})
}
fn limits_named(peer:&Peer,run:&str,label:&str)->Vec<Value>{rs_for(peer,run).into_iter().filter(|e|e["kind"]=="evidence_limit"&&e["body"]["label"]==label).collect()}

// EXEC §2.7 / RECOVERY §4.1, EXEC A-2, RECOVERY §4.1: when run_opened is recorded the run's conversation is
// tagged with the run reference in the REC ledger; tags are ordered, a later run's tag is
// appended and the earlier run's tag is kept; `look up` finds the conversation of a tag.
#[test]
fn run_tag_written_at_run_opened_ordered_and_earlier_tag_kept(){
    let owner=crate::run_restart::RUN_TAG_OWNER;
    let peer=Peer::with_recovery();let mut root=peer.fixture.registered();
    let a=open_run(&peer,&mut root,"thread");
    let tag=root.runs[&a].lock().unwrap().view(&a)["runTag"].clone();
    assert_eq!(tag["persistence"],"durable App metadata","{tag}");assert_eq!(tag["tag"]["value"],a.as_str());
    root.runs[&a].lock().unwrap().end_run(None,None).unwrap();
    let b=open_run(&peer,&mut root,"thread");
    let tags=peer.home.host.tags_of("H-acct","thread",owner);
    assert_eq!(tags.iter().map(|t|t["value"].as_str().unwrap()).collect::<Vec<_>>(),[a.as_str(),b.as_str()],"ordered; the earlier run's tag is kept");
    assert!(tags[0]["seq"].as_u64()<tags[1]["seq"].as_u64());
    // Durable: the ledger file itself carries both tags, readable by a later process.
    let ledger=crate::recovery::RecoveryLedger::open(peer.fixture.root.join("app-data/runtime/recovery.ledger.jsonl")).unwrap().recorded_entries();
    let rows=ledger.as_array().unwrap().clone();
    assert_eq!(crate::recovery::tags_of(&rows,"H-acct","thread",owner),tags);
    // The conversation's latest index row itself still carries the earlier run's tag.
    let latest=rows.iter().rev().find(|r|r["kind"]=="conversation_index"&&r["threadId"]=="thread").unwrap();
    assert_eq!(crate::recovery::tags_of(std::slice::from_ref(latest),"H-acct","thread",owner),tags,"an earlier run's tag is never replaced");
    assert_eq!(crate::recovery::look_up(&rows,owner,&b),[("H-acct".to_string(),"thread".to_string())]);
    assert!(crate::recovery::tags_of(&rows,"H-acct","thread","DEL-01-04").is_empty(),"tags of one owner only");
}
// EXEC §2.7 / RECOVERY §4.1, RECOVERY §4.1 failure column: a tag that cannot be stored lives in memory only
// and never blocks the run: no ledger, or a ledger that refuses the append.
#[test]
fn run_tag_not_stored_keeps_the_run_going(){
    let peer=Peer::new();let mut root=peer.fixture.registered();
    let a=open_run(&peer,&mut root,"thread");
    let view=root.runs[&a].lock().unwrap().view(&a);
    assert_eq!(view["runTag"]["persistence"],"memory-only","{view}");
    assert!(rs_for(&peer,&a).iter().any(|e|e["kind"]=="run_opened"),"the run opened and was recorded");
    let peer=Peer::with_recovery();let mut root=peer.fixture.registered();
    // The ledger refuses the append: its database leaf is displaced by a directory.
    let ledger=crate::recovery::database_path(&peer.fixture.root.join("app-data/runtime/recovery.ledger.jsonl"));let aside=peer.fixture.root.join("ledger-aside");
    std::fs::rename(&ledger,&aside).unwrap();std::fs::create_dir(&ledger).unwrap();
    let a=open_run(&peer,&mut root,"thread");
    std::fs::remove_dir(&ledger).unwrap();std::fs::rename(&aside,&ledger).unwrap();
    let view=root.runs[&a].lock().unwrap().view(&a);
    assert_eq!(view["runTag"]["persistence"],"memory-only","{view}");assert!(view["runTag"]["limit"].as_str().unwrap().contains("append unavailable"));
    assert_eq!(root.runs[&a].lock().unwrap().lifecycle,RunLifecycle::Open);
    assert!(rs_for(&peer,&a).iter().any(|e|e["kind"]=="run_opened"));
    assert!(peer.home.host.tags_of("H-acct","thread",crate::run_restart::RUN_TAG_OWNER).is_empty());
}
// EXEC §2.7 / RECOVERY §4.1, RS "Relaunch with a run interrupted", FC-9, EXEC RE-4: one "App-restart
// interruption" limit on the run current in the conversation at the end (picked from the
// ordered run tags and the RS records), never twice for the same run and fact; an earlier
// ended run is untouched; no run_ended is written; without a stored tag the run is found by
// run_opened.conversationRef and the limit says so; a conversation whose last run had
// ended gets no limit.
#[test]
fn restart_limit_written_once_on_the_current_run(){
    let label=crate::run_restart::RESTART_LABEL;
    let peer=Peer::new();let mut root=peer.fixture.registered();
    let a=open_run(&peer,&mut root,"thread");root.runs[&a].lock().unwrap().end_run(None,None).unwrap();
    let b=open_run(&peer,&mut root,"thread");
    let t2=peer.second_thread();let c=open_run(&peer,&mut root,&t2);root.runs[&c].lock().unwrap().end_run(None,None).unwrap();
    drop(root);
    let owner=crate::run_restart::RUN_TAG_OWNER;
    let rows=vec![index_row("thread",json!([{"owner":"DEL-01-04","value":"[\"sub\",null]","seq":1},{"owner":owner,"value":a,"seq":2}])),
        index_row("thread",json!([{"owner":"DEL-01-04","value":"[\"sub\",null]","seq":1},{"owner":owner,"value":a,"seq":2},{"owner":owner,"value":b,"seq":3}]))];
    let fact=restart_fact("cev:restart:one","thread");
    let out=crate::run_restart::write_restart_limits(&peer.fixture.root,std::slice::from_ref(&fact),&rows);
    assert_eq!(out[0]["outcome"],"written","{out:?}");assert_eq!(out[0]["run"],b.as_str());assert_eq!(out[0]["detail"]["foundBy"],"REC run tag");
    let limits=limits_named(&peer,&b,label);assert_eq!(limits.len(),1);
    assert_eq!(limits[0]["body"]["subjectRef"],"cev:restart:one");
    let detail=limits[0]["body"]["detail"].as_str().unwrap();assert!(detail.contains("app-session:before")&&detail.contains("ended-without-record")&&detail.contains("REC run tag"),"{detail}");
    assert!(limits_named(&peer,&a,label).is_empty(),"the earlier ended run is untouched");
    assert!(!rs_for(&peer,&b).iter().any(|e|e["kind"]=="run_ended"),"no run_ended is written automatically");
    // Idempotent on rerun (the next startup with the same fact).
    let again=crate::run_restart::write_restart_limits(&peer.fixture.root,std::slice::from_ref(&fact),&rows);
    assert_eq!(again[0]["outcome"],"already written");assert_eq!(limits_named(&peer,&b,label).len(),1);
    // No stored tag: found by run_opened.conversationRef, and the limit says so.
    let other=restart_fact("cev:restart:two","thread");
    let out=crate::run_restart::write_restart_limits(&peer.fixture.root,&[other],&[]);
    assert_eq!(out[0]["outcome"],"written");assert_eq!(out[0]["run"],b.as_str());
    let found=limits_named(&peer,&b,label).into_iter().find(|e|e["body"]["subjectRef"]=="cev:restart:two").unwrap();
    assert!(found["body"]["detail"].as_str().unwrap().contains("conversationRef")&&found["body"]["detail"].as_str().unwrap().contains("no REC run tag is stored"),"{found}");
    // The conversation's last run had ended: no run was current, nothing written.
    let ended=crate::run_restart::write_restart_limits(&peer.fixture.root,&[restart_fact("cev:restart:three",&t2)],&[]);
    assert_eq!(ended[0]["outcome"],"not written");assert!(ended[0]["detail"].as_str().unwrap().contains("had ended"));
    assert!(limits_named(&peer,&c,label).is_empty());
    assert!(!rs_for(&peer,&c).iter().any(|e|e["kind"]=="run_ended"&&e["body"]["stoppedBy"]!="the person"));
}
// WR TX-5 / SQ-END, WR TX-5 / SQ-END: an end the person makes after a relaunch gets its end notice,
// composed from the person's end plus the run's recorded run-start run_text (checked against
// its run_opened); the next ordinary turn carries it first, exactly once; until then a run
// start in that conversation is held back (EXEC CH-2 / RE-7).
#[test]
fn end_after_relaunch_notice_from_recorded_run_text_carried_once(){
    let peer=Peer::new();let mut root=peer.fixture.registered();let a=open_run(&peer,&mut root,"thread");
    let mut fresh=WorkflowRootSession::default();fresh.selected=root.selected.take();drop(root);
    let ended=fresh.end_recorded_run(&peer.fixture.root,&a,"thread",false,Some(peer.home.clone())).unwrap();
    assert!(ended["endNotice"]["state"].as_str().unwrap().starts_with("pending"),"{ended}");
    let blocked=fresh.prepare_run(peer.home.clone(),&peer.generation,"thread","next".into(),peer.project());
    assert!(blocked.as_ref().is_err_and(|e|e.contains("end notice pending")),"{blocked:?}");
    let workflow=rs_for(&peer,&a).into_iter().find(|e|e["kind"]=="run_opened").unwrap()["body"]["workflow"].clone();
    let expected=format!("[Chirality] Workflow run ended: {} revision {} (run {a}, ended by the person). No workflow is in force.",workflow["name"].as_str().unwrap(),&workflow["revision"].as_str().unwrap()[..12]);
    let root=Mutex::new(fresh);let starts=peer.turn_starts();
    assert!(send_with_pending_notice(&root,&peer.generation,"thread","hello").expect("pending").is_ok());
    assert_eq!(peer.turn_starts(),starts+1);
    let input=last_turn_start(&peer)["params"]["input"].clone();
    assert_eq!(input[0]["text"],expected.as_str());assert_eq!(input[1]["text"],"hello");
    assert!(send_with_pending_notice(&root,&peer.generation,"thread","again").is_none(),"carried once");
    // Its WR record cites the run's recorded start.
    let project=crate::workflow_workspace::publication::ProjectRecords::open(&peer.fixture.root).unwrap();
    let notice=project.list_references().unwrap().into_iter().filter_map(|r|project.resolve(&r).ok()).find(|r|r.body()["purpose"]=="run end notice"&&r.body()["run"]==a.as_str()).expect("notice record");
    assert_eq!(notice.envelope()["basis_records"][0],run_start_record(&peer,&a).reference());
    let view=root.lock().unwrap().reopened_end(&a).unwrap().lock().unwrap().view();assert!(view["endNotice"]["state"].as_str().unwrap().starts_with("sent once"),"{view}");
    assert!(root.lock().unwrap().prepare_run(peer.home.clone(),&peer.generation,"thread","next".into(),peer.project()).is_ok(),"after the notice went, a new start is allowed");
}
// WR TX-5 / SQ-END: with the recorded run text missing, or not matching the run's run_opened, no
// notice is sent and the reason is given; the person's end is still recorded.
#[test]
fn end_after_relaunch_refuses_a_notice_without_a_matching_record(){
    let peer=Peer::new();let mut root=peer.fixture.registered();let a=open_run(&peer,&mut root,"thread");
    let t2=peer.second_thread();let b=open_run(&peer,&mut root,&t2);
    let mut fresh=WorkflowRootSession::default();fresh.selected=root.selected.take();drop(root);
    // Mismatch: the recorded start of `b` checked against another revision or conversation.
    let records=crate::workflow_workspace::publication::ProjectRecords::open(&peer.fixture.root).unwrap();
    let mut workflow=rs_for(&peer,&b).into_iter().find(|e|e["kind"]=="run_opened").unwrap()["body"]["workflow"].clone();
    let compose=|w:&Value,thread:&str|crate::workflow_workspace::publication::PreparedEndPublication::after_relaunch(&records,&b,thread,w,&crate::workflow_workspace::RunEndReason::ByPerson,WR_WRITER,"2026-10-10T00:00:00Z",&peer.generation).map(|_|());
    assert!(compose(&workflow,&t2).is_ok());
    assert!(compose(&workflow,"thread").is_err_and(|e|e.contains("another conversation")));
    workflow["revision"]=json!("0".repeat(64));
    assert!(compose(&workflow,&t2).is_err_and(|e|e.contains("does not match")));
    // Missing: the run-start record of `a` is gone.
    let start=run_start_record(&peer,&a);let name=start.reference().trim_start_matches("wr-record:v1:").to_owned();
    std::fs::remove_file(wr_dir(&peer).join(format!("{name}.json"))).unwrap();
    let ended=fresh.end_recorded_run(&peer.fixture.root,&a,"thread",false,Some(peer.home.clone())).unwrap();
    let state=ended["endNotice"]["state"].as_str().unwrap();assert!(state.starts_with("not composed")&&state.contains("no recorded run-start text"),"{state}");
    assert!(rs_for(&peer,&a).iter().any(|e|e["kind"]=="run_ended"),"the person's end is recorded");
    let root=Mutex::new(fresh);
    assert!(send_with_pending_notice(&root,&peer.generation,"thread","hello").is_none(),"no notice is sent");
}
// WR TX-5 / SQ-END with V10 G-5/R-4: an unwritable notice record sends nothing; the person may
// retry it or send without it, and that choice is recorded in the run's log first.
#[test]
fn reopened_notice_record_failure_offers_retry_or_recorded_skip(){
    use std::os::unix::fs::PermissionsExt;
    let peer=Peer::new();let mut root=peer.fixture.registered();let a=open_run(&peer,&mut root,"thread");
    let mut fresh=WorkflowRootSession::default();fresh.selected=root.selected.take();drop(root);
    fresh.end_recorded_run(&peer.fixture.root,&a,"thread",false,Some(peer.home.clone())).unwrap();
    let root=Mutex::new(fresh);let starts=peer.turn_starts();
    std::fs::set_permissions(wr_dir(&peer),std::fs::Permissions::from_mode(0o500)).unwrap();
    let refused=send_with_pending_notice(&root,&peer.generation,"thread","hello").expect("pending").unwrap_err();
    assert!(refused.contains("Send without the end notice"),"{refused}");assert_eq!(peer.turn_starts(),starts,"nothing sent");
    let end=root.lock().unwrap().reopened_end(&a).unwrap();
    assert_eq!(end.lock().unwrap().retry_notice_record().unwrap()["state"],"still not recorded");
    std::fs::set_permissions(wr_dir(&peer),std::fs::Permissions::from_mode(0o700)).unwrap();
    let skipped=end.lock().unwrap().skip_end_notice().unwrap();assert!(skipped["endNotice"]["state"].as_str().unwrap().starts_with("not supplied"));
    let limit=rs_for(&peer,&a).into_iter().find(|e|e["kind"]=="evidence_limit"&&e["body"]["label"]=="record write failed").expect("the choice is recorded");
    assert!(limit["body"]["detail"].as_str().unwrap().contains("not supplied"));
    assert!(send_with_pending_notice(&root,&peer.generation,"thread","hello").is_none());assert_eq!(peer.turn_starts(),starts);
}
// RS §14.1 Permanent refusals, RS W-1/W-2: an R3 whose reserved identity is held by a different entry can
// never be written; it is not held: a "record write failed" limit names it as never
// written, and the later run_ended and R3 are written in order.
#[test]
fn permanently_refused_r3_gets_its_limit_and_later_records_proceed(){
    let peer=Peer::new();let mut root=peer.fixture.registered();
    let reference=root.prepare_run(peer.home.clone(),&peer.generation,"thread","person".into(),peer.project()).unwrap();
    let run=root.runs[&reference].clone();let mut run=run.lock().unwrap();run.send().unwrap();peer.select_history();
    let runs=crate::storage::project_file(&peer.fixture.root, "runs").unwrap();let aside=crate::storage::project_file(&peer.fixture.root, "runs-aside").unwrap();
    std::fs::rename(&runs,&aside).unwrap();std::fs::write(&runs,b"blocked").unwrap();
    let first=run.check_native_supply().unwrap()["check"].clone();let reserved=first["r3"]["recordId"].as_str().unwrap().to_owned();
    assert_eq!(first["r3"]["state"],"pending write; missing in record","an I/O failure is held, not refused");
    std::fs::remove_file(&runs).unwrap();std::fs::rename(&aside,&runs).unwrap();
    crate::records::append_with_id(&crate::storage::project_log(&peer.fixture.root,None,"conflict-fixture").unwrap(),"evidence_limit",&crate::records::APP_WRITER,json!({"label":"unresolvable reference"}),&reserved).unwrap();
    run.end_run(None,None).unwrap();
    let second=run.check_native_supply().unwrap()["check"].clone();assert_eq!(second["r3"]["state"],"recorded","later R3 proceeds");
    let log=rs_for(&peer,&reference);
    assert!(log.iter().all(|e|e["recordId"]!=reserved.as_str()),"the refused R3 is not in the run log");
    let limit=log.iter().find(|e|e["kind"]=="evidence_limit"&&e["body"]["subjectRef"]==reserved.as_str()).expect("never-written limit");
    assert_eq!(limit["body"]["label"],"record write failed");let detail=limit["body"]["detail"].as_str().unwrap();
    assert!(detail.contains("can never be written")&&detail.contains("not in the record")&&detail.contains("already held"),"{detail}");
    assert!(run.entry_written("run_ended"),"the person's run_ended is written");
    let order=log_order(&peer,&reference);
    let at=|k:&str|order.iter().position(|o|o==k).unwrap_or_else(||panic!("{k} in {order:?}"));
    assert!(at("run_opened")<at(&format!("limit:{reserved}"))&&at(&format!("limit:{reserved}"))<at("run_ended"),"{order:?}");
    assert_eq!(run.view(&reference)["checks"][0]["r3"]["state"],"unavailable");
    assert!(!run.has_pending_records());
}
// RS §14.1 Permanent refusals: a nonconformant lifecycle entry (W-1 (a)) is refused permanently too: its limit
// is written in its place and the run_ended behind it is written; a transient failure still
// holds every later entry in strict order.
#[test]
fn nonconformant_entry_is_refused_but_transient_failure_keeps_strict_order(){
    let peer=Peer::new();let mut root=peer.fixture.registered();
    let runs=crate::storage::project_file(&peer.fixture.root, "runs").unwrap();std::fs::write(&runs,b"blocked").unwrap();
    let a=root.prepare_run(peer.home.clone(),&peer.generation,"thread","person".into(),peer.project()).unwrap();
    let run=root.runs[&a].clone();let mut run=run.lock().unwrap();run.send().unwrap();
    let bad=crate::records::supply::PendingRunEntry::new("evidence_limit",json!({"label":"not an RS label"}),crate::util::now_rfc3339()).unwrap();let bad_id=bad.record_id.clone();
    run.entries.push(bad);
    run.end_run(None,None).unwrap();
    // Transient: nothing is refused; everything waits behind run_opened, in order.
    assert!(run.entries.iter().all(|e|e.refused.is_none()&&e.written.is_none()),"an I/O failure refuses nothing");
    assert!(!run.entry_written("run_ended"));
    std::fs::remove_file(&runs).unwrap();run.retry_records().unwrap();
    assert!(run.entry_written("run_ended"),"the end behind the refused entry is written");
    let order=log_order(&peer,&a);
    assert_eq!(order.iter().filter(|o|o.as_str()!="checkpoint_listed"&&o.as_str()!="declaration_finding"&&!o.starts_with("limit:checkpoint")&&!o.starts_with("limit:declaration")).cloned().collect::<Vec<_>>(),["run_opened","limit:run_opened",format!("limit:{bad_id}").as_str(),"run_ended","limit:run_ended"],"{order:?}");
    let limit=rs_for(&peer,&a).into_iter().find(|e|e["body"]["subjectRef"]==bad_id.as_str()).unwrap();
    assert!(limit["body"]["detail"].as_str().unwrap().contains("nonconformant"));
    assert!(run.entries.iter().any(|e|e.record_id==bad_id&&e.refused.is_some()));
}
// EXEC §2.7 / RECOVERY §4.1: the startup entry writes nothing without an explicit project or a configured
// REC projection, and says why (shown by workflow_reopen).
#[test]
fn startup_writer_states_why_it_did_not_run(){
    let peer=Peer::new();
    assert_eq!(crate::run_restart::startup(&[peer.home.clone()],None)["state"],"not run");
    let out=crate::run_restart::startup(&[peer.home.clone()],peer.project());
    assert!(out["outcomes"].as_array().unwrap().is_empty());
    assert!(out["limits"][0]["limit"].as_str().unwrap().contains("not available"),"{out}");
    let mut root=WorkflowRootSession::default();root.set_restart_limits(out.clone());
    assert_eq!(root.reopen(&peer.fixture.root,&[]).unwrap()["restartLimits"],out);
}
// RS §14.1 Permanent refusals: permanence is classified conservatively: an identity conflict found while
// part of the record set cannot be read is not a definite refusal, so the entry stays held.
#[test]
fn identity_conflict_in_an_incomplete_record_set_is_not_a_permanent_refusal(){
    let root=std::fs::canonicalize(std::env::temp_dir()).unwrap().join(crate::util::opaque_id("permanent-refusal-").unwrap());std::fs::create_dir_all(&root).unwrap();
    let id="rec:app:held-identity";let body=json!({"label":"record write failed","subjectRef":"x","detail":"d"});
    crate::records::append_with_id(&crate::storage::project_log(&root,None,"conflict-fixture").unwrap(),"evidence_limit",&crate::records::APP_WRITER,json!({"label":"unresolvable reference"}),id).unwrap();
    let refusal=|| crate::records::supply::permanent_refusal(&root,"run:x","evidence_limit",id,&body,"2026-10-10T00:00:00Z");
    assert!(refusal().is_some_and(|r|r.contains("already held")),"complete set: definite conflict");
    let torn=crate::storage::project_log(&root,None,"other-writer").unwrap();std::fs::write(&torn,b"{\"torn").unwrap();
    assert!(refusal().is_some_and(|r|r.contains("already held")),"a torn final line is a partial, never an entry (R-2): still definite");
    std::fs::write(&torn,b"{\"torn\n").unwrap();
    assert!(refusal().is_none(),"an unreadable log leaves the conflict indefinite: stays held");
    std::fs::remove_dir_all(root).unwrap();
}
// RS W-1 / §13.7 and CC-ID: every append but the relaunch end needs the whole record set
// complete. The relaunch end's mode accepts other incomplete logs, still refuses an
// incomplete owning log, and still refuses an identity held by a readable entry. A torn
// final line is a partial (R-2): it leaves another writer's set complete, and its own
// writer recovers it on its next open (W-0).
#[test]
fn writer_record_set_modes_beside_an_incomplete_log(){
    use crate::records::RecordSet::{Complete,ReadableBesideIncomplete};
    let root=std::fs::canonicalize(std::env::temp_dir()).unwrap().join(crate::util::opaque_id("rs-set-").unwrap());std::fs::create_dir_all(&root).unwrap();
    let held="rec:app:held-elsewhere";
    crate::records::append_with_id(&crate::storage::project_log(&root,None,"other-writer").unwrap(),"evidence_limit",&crate::records::APP_WRITER,json!({"label":"unresolvable reference"}),held).unwrap();
    let torn=crate::storage::project_log(&root,None,"torn-writer").unwrap();std::fs::write(&torn,b"{\"torn").unwrap();
    let body=json!({"label":"unresolvable reference","subjectRef":"x","detail":"d"});
    let append=|id:&str,set|crate::records::append_project_reserved_in(&root,"run:x","w","evidence_limit",&crate::records::APP_WRITER,body.clone(),id,"2026-10-11T00:00:00Z",set);
    assert!(append("rec:app:p",Complete).is_ok(),"another writer's torn tail leaves the set complete");
    assert_eq!(std::fs::read(&torn).unwrap(),b"{\"torn","another writer's log is never repaired here");
    std::fs::write(&torn,b"{\"torn\n").unwrap();
    assert!(append("rec:app:a",Complete).is_err_and(|e|e.contains("record-set conflict/incomplete")),"the default still needs the whole set");
    assert!(append("rec:app:a",ReadableBesideIncomplete).is_ok(),"the relaunch end's mode writes beside it");
    assert!(append(held,ReadableBesideIncomplete).is_err_and(|e|e.contains("identity conflict")),"a readable identity is still checked");
    let own=crate::storage::project_log(&root,Some("run:x"),"w").unwrap();
    let mut f=std::fs::OpenOptions::new().append(true).open(&own).unwrap();std::io::Write::write_all(&mut f,b"{\"torn").unwrap();drop(f);
    let torn_own=std::fs::read(&own).unwrap();
    assert!(append("rec:app:b",ReadableBesideIncomplete).is_ok(),"the owning writer recovers its torn tail (W-0)");
    assert!(std::fs::read(&own).unwrap().starts_with(&torn_own),"the torn bytes are kept");
    let (entries,limits)=crate::records::read_log(&own);assert!(limits.is_empty(),"{limits:?}");
    assert_eq!(entries.iter().map(|e|e["body"]["label"].as_str().unwrap()).collect::<Vec<_>>(),["unresolvable reference","unresolvable reference",crate::records::PARTIAL_NOT_RECOVERED,"unresolvable reference"]);
    let mut f=std::fs::OpenOptions::new().append(true).open(&own).unwrap();std::io::Write::write_all(&mut f,b"{\"unreadable\n").unwrap();drop(f);
    assert!(append("rec:app:c",ReadableBesideIncomplete).is_err_and(|e|e.contains("incomplete owning log")),"an unreadable owning line refuses");
    std::fs::remove_dir_all(root).unwrap();
}
// PR #1269 review: in `Complete` mode the supply writer refuses beside an incomplete set
// before it reads anything, so even an already-written entry is not recognised there; the
// relaunch end's mode recognises it from the readable entries (idempotent, W-2).
#[test]
fn supply_complete_mode_refuses_before_recognising_a_written_entry_beside_a_torn_log(){
    use crate::records::RecordSet::{Complete,ReadableBesideIncomplete};
    let root=std::fs::canonicalize(std::env::temp_dir()).unwrap().join(crate::util::opaque_id("rs-supply-").unwrap());std::fs::create_dir_all(&root).unwrap();
    let mut entry=crate::records::supply::PendingRunEntry::new("evidence_limit",json!({"label":"unresolvable reference","subjectRef":"x","detail":"d"}),"2026-10-11T00:00:00Z".into()).unwrap();
    let mut again=entry.clone();let mut third=entry.clone();
    crate::records::supply::append_run_entry(&root,"run:x",&mut entry).unwrap();
    let torn=crate::storage::project_log(&root,None,"torn-writer").unwrap();std::fs::create_dir_all(torn.parent().unwrap()).unwrap();std::fs::write(&torn,b"{\"torn\n").unwrap();
    assert!(crate::records::supply::append_run_entry_in(&root,"run:x",&mut again,Complete).is_err_and(|e|e.contains("RS record set incomplete")));
    assert_eq!(crate::records::supply::append_run_entry_in(&root,"run:x",&mut third,ReadableBesideIncomplete).unwrap()["recordId"],entry.record_id.as_str());
    std::fs::remove_dir_all(root).unwrap();
}

// RS §14.2 R-2, §14.1 W-0: another writer's torn final line is a partial, never an
// entry, so an open run (complete-set guard) keeps writing beside it, and the torn
// log is left for its own writer to recover.
#[test]
fn an_open_run_records_beside_another_writers_torn_tail(){
    let peer=Peer::new();let mut root=declared(&peer);let a=open_run(&peer,&mut root,"thread");
    std::fs::create_dir_all(peer.fixture.root.join("out")).unwrap();std::fs::write(peer.fixture.root.join("out/summary.md"),b"v1").unwrap();
    let other=crate::storage::project_log(&peer.fixture.root,None,"torn-writer").unwrap();std::fs::create_dir_all(other.parent().unwrap()).unwrap();std::fs::write(&other,b"{\"torn").unwrap();
    let before=own_log(&peer,&a).len();
    let shared=root.runs[&a].clone();let mut run=shared.lock().unwrap();
    run.observe_checkpoints(&recorder_view(&peer,&summary_items()[1..]));
    assert!(!run.has_pending_records(),"{}",run.view(&a));assert!(own_log(&peer,&a).len()>before);
    assert_eq!(std::fs::read(&other).unwrap(),b"{\"torn");
}

// The live end records without repairing unrelated logs, including when nothing
// waits and there is no reason to read acts or invent an unread-act limit.
#[test]
fn live_end_beside_a_torn_log_with_nothing_waiting_is_recorded_plainly(){
    let peer=Peer::new();let mut root=peer.fixture.registered();let a=open_run(&peer,&mut root,"thread");
    let (other,_)=break_act_log(&peer);let torn=std::fs::read(&other).unwrap();
    let ended=root.runs[&a].lock().unwrap().end_run(None,None).unwrap();
    assert_eq!(ended["recorded"],true,"{ended}");
    let log=own_log(&peer,&a);
    assert!(!log.iter().any(act_records_limit));
    assert_eq!(log.last().unwrap()["kind"],"run_ended");
    assert_eq!(log.last().unwrap()["body"]["waitingArrivals"],json!([]));
    assert_eq!(std::fs::read(&other).unwrap(),torn,"the unrelated log is untouched");
}

// W-2: observations held while the run is open, including R3, drain at the
// explicit end with their original identities/times and late-write limits.
#[test]
fn live_end_drains_pending_checkpoint_and_r3_before_its_end_beside_a_torn_log(){
    let peer=Peer::new();let mut root=declared(&peer);let a=open_run(&peer,&mut root,"thread");
    std::fs::create_dir_all(peer.fixture.root.join("out")).unwrap();std::fs::write(peer.fixture.root.join("out/summary.md"),b"v1").unwrap();
    let (other,_)=break_act_log(&peer);let torn=std::fs::read(&other).unwrap();
    let shared=root.runs[&a].clone();let mut run=shared.lock().unwrap();
    run.observe_checkpoints(&recorder_view(&peer,&summary_items()[1..]));
    peer.select_history();let check=run.check_native_supply().unwrap()["check"].clone();
    assert_eq!(check["r3"]["state"],"pending write; missing in record","open runs retain Complete: {check}");
    let r3=check["r3"]["recordId"].as_str().unwrap().to_owned();
    let pending:Vec<_>=run.entries.iter().filter(|e|e.pending()).map(|e|(e.record_id.clone(),e.observed_at.clone())).collect();
    assert!(!pending.is_empty());
    let r3_at=match &run.checks.last().unwrap().r3 {WorkflowR3::Pending(p)=>p.observed_at().to_owned(),_=>panic!("R3 must be pending")};
    run.end_run(None,None).unwrap();
    assert!(!run.has_pending_records(),"{}",run.view(&a));
    let log=own_log(&peer,&a);let end=log.iter().position(|e|e["kind"]=="run_ended").unwrap();
    for (id,at) in pending.into_iter().chain(std::iter::once((r3,r3_at))) {
        let written:Vec<_>=log.iter().enumerate().filter(|(_,e)|e["recordId"]==id.as_str()).collect();
        assert_eq!(written.len(),1,"reserved identity written once");
        let (pos,e)=written[0];assert_eq!(e["observedAt"],at.as_str());
        let limit=log.iter().position(|e|e["kind"]=="evidence_limit"&&e["body"]["label"]=="record write failed"&&e["body"]["subjectRef"]==id.as_str()).unwrap();
        assert!(pos<limit&&limit<end,"late observation, its limit, then end");
    }
    assert!(log.iter().position(act_records_limit).unwrap()<end);
    let before=std::fs::read(crate::records::supply::run_log(&peer.fixture.root,&a).unwrap()).unwrap();
    run.retry_records().unwrap();
    assert_eq!(std::fs::read(crate::records::supply::run_log(&peer.fixture.root,&a).unwrap()).unwrap(),before,"retry duplicates nothing");
    assert_eq!(std::fs::read(&other).unwrap(),torn);
}

// W-0 at the person's hot end: the run's own torn log is recovered (the torn
// bytes kept, "partial entry not recovered" naming the line) and the end is
// recorded after it, beside another incomplete log.
#[test]
fn live_end_recovers_its_own_torn_log_beside_another_incomplete_log(){
    let peer=Peer::new();let mut root=peer.fixture.registered();let a=open_run(&peer,&mut root,"thread");
    let own=crate::records::supply::run_log(&peer.fixture.root,&a).unwrap();
    let mut f=std::fs::OpenOptions::new().append(true).open(&own).unwrap();std::io::Write::write_all(&mut f,b"{\"torn").unwrap();drop(f);
    let torn=std::fs::read(&own).unwrap();let (other,_)=break_act_log(&peer);let other_bytes=std::fs::read(&other).unwrap();
    let shared=root.runs[&a].clone();let mut run=shared.lock().unwrap();let ended=run.end_run(None,None).unwrap();
    assert_eq!(ended["recorded"],true,"{ended}");assert!(!run.has_pending_records());
    assert!(std::fs::read(&own).unwrap().starts_with(&torn),"the torn bytes are kept in place");
    let log=own_log(&peer,&a);
    let w0=log.iter().position(|e|e["body"]["label"]==crate::records::PARTIAL_NOT_RECOVERED).expect("W-0's limit");
    assert!(w0<log.iter().position(|e|e["kind"]=="run_ended").unwrap());
    assert_eq!(std::fs::read(&other).unwrap(),other_bytes,"another writer's log is untouched");
}

// The person's hot end still ends the run when its owning target cannot be
// written (an unreadable line, not a torn tail); the record stays pending and
// retries preserve the original end.
#[test]
fn live_end_own_unreadable_log_holds_writes_until_repair_even_beside_another_incomplete_log(){
    let peer=Peer::new();let mut root=peer.fixture.registered();let a=open_run(&peer,&mut root,"thread");
    let own=crate::records::supply::run_log(&peer.fixture.root,&a).unwrap();let before=std::fs::read(&own).unwrap();
    let mut f=std::fs::OpenOptions::new().append(true).open(&own).unwrap();std::io::Write::write_all(&mut f,b"{\"torn\n").unwrap();drop(f);
    let torn=std::fs::read(&own).unwrap();let (other,_)=break_act_log(&peer);let other_bytes=std::fs::read(&other).unwrap();
    let shared=root.runs[&a].clone();let mut run=shared.lock().unwrap();let ended=run.end_run(None,None).unwrap();
    assert_eq!(ended["recorded"],false);assert_eq!(run.lifecycle,RunLifecycle::Ended);assert!(run.has_pending_records());
    let end=run.entries.iter().find(|e|e.kind=="run_ended").unwrap().clone();
    run.retry_records().unwrap();assert_eq!(std::fs::read(&own).unwrap(),torn,"no append to the owning torn log");
    std::fs::write(&own,before).unwrap();run.retry_records().unwrap();
    assert!(!run.has_pending_records());let log=own_log(&peer,&a);
    let written=log.iter().find(|e|e["kind"]=="run_ended").unwrap();assert_eq!(written["recordId"],end.record_id);assert_eq!(written["observedAt"],end.observed_at);
    assert_eq!(log.last().unwrap()["body"]["subjectRef"],end.record_id);
    assert_eq!(std::fs::read(&other).unwrap(),other_bytes);
}

// An uncertain landed entry is not reconciled from a matching prefix of an
// incomplete own log, nor through a symlink. Failed discovery can still recover
// a complete owning entry and its late limit without writing either twice.
#[test]
fn live_end_reconciles_uncertain_own_writes_when_discovery_fails_but_refuses_own_tails_and_aliases(){
    use crate::records::RecordSet::ReadableBesideIncomplete;
    let peer=Peer::new();let run="run:uncertain";
    let mut original=crate::records::supply::PendingRunEntry::new("evidence_limit",json!({"label":"unresolvable reference","subjectRef":"x","detail":"d"}),"2026-10-11T00:00:00Z".into()).unwrap();
    let mut pending=original.clone();pending.failure=Some("injected uncertain sync".into());
    crate::records::supply::append_run_entry(&peer.fixture.root,run,&mut original).unwrap();
    crate::records::append_project(&peer.fixture.root,Some(run),"other-writer","evidence_limit",&crate::records::APP_WRITER,
        json!({"label":"record write failed","subjectRef":original.record_id,"detail":"another writer's claim cannot settle this writer's late limit"})).unwrap();
    let own=crate::records::supply::run_log(&peer.fixture.root,run).unwrap();let complete=std::fs::read(&own).unwrap();
    // An unreadable own line (a torn tail alone is recovered by W-0 first).
    let mut f=std::fs::OpenOptions::new().append(true).open(&own).unwrap();std::io::Write::write_all(&mut f,b"{\"torn\n").unwrap();drop(f);
    let torn=std::fs::read(&own).unwrap();
    assert!(crate::records::supply::append_run_entry_in(&peer.fixture.root,run,&mut pending,ReadableBesideIncomplete).is_err_and(|e|e.contains("owning log incomplete")));
    assert!(pending.written.is_none());assert_eq!(std::fs::read(&own).unwrap(),torn);
    std::fs::write(&own,complete).unwrap();
    let alias=crate::storage::project_file(&peer.fixture.root, "acts/discovery-alias.jsonl").unwrap();std::fs::create_dir_all(alias.parent().unwrap()).unwrap();std::os::unix::fs::symlink(&own,&alias).unwrap();
    assert!(!crate::storage::read_all(&peer.fixture.root).1.is_empty(),"discovery fails on alias");
    let mut again=pending.clone();
    crate::records::supply::append_run_entry_in(&peer.fixture.root,run,&mut pending,ReadableBesideIncomplete).unwrap();
    let settled=std::fs::read(&own).unwrap();
    crate::records::supply::append_run_entry_in(&peer.fixture.root,run,&mut again,ReadableBesideIncomplete).unwrap();
    assert_eq!(std::fs::read(&own).unwrap(),settled,"landed entry and late limit each appear once");
    let log=crate::records::read_log(&own).0;assert_eq!(log.len(),2);assert_eq!(log[1]["body"]["subjectRef"],original.record_id);
    std::fs::remove_file(&alias).unwrap();
    let relocated=peer.fixture.root.join("saved-own-log");std::fs::rename(&own,&relocated).unwrap();std::os::unix::fs::symlink(&relocated,&own).unwrap();
    again.written=None;
    assert!(crate::records::supply::append_run_entry_in(&peer.fixture.root,run,&mut again,ReadableBesideIncomplete).is_err());
    assert_eq!(std::fs::read(&relocated).unwrap(),settled);
}

// Readable duplicates cannot be hidden by an earlier exact matching entry.
#[test]
fn live_end_matching_own_entry_does_not_hide_readable_conflicting_content(){
    for detail in ["different content","d"] {
        let peer=Peer::new();let mut root=peer.fixture.registered();let a=open_run(&peer,&mut root,"thread");
        let mut entry=crate::records::supply::PendingRunEntry::new("evidence_limit",json!({"label":"unresolvable reference","subjectRef":"x","detail":"d"}),crate::util::now_rfc3339()).unwrap();
        let pending=entry.clone();crate::records::supply::append_run_entry(&peer.fixture.root,&a,&mut entry).unwrap();
        let own=crate::records::supply::run_log(&peer.fixture.root,&a).unwrap();let before=std::fs::read(&own).unwrap();
        let mut conflict=entry.written.clone().unwrap();conflict["body"]["detail"]=json!(detail);
        let other=crate::storage::project_log(&peer.fixture.root,None,"duplicate-fixture").unwrap();std::fs::create_dir_all(other.parent().unwrap()).unwrap();std::fs::write(&other,format!("{conflict}\n")).unwrap();
        break_act_log(&peer);let shared=root.runs[&a].clone();let mut run=shared.lock().unwrap();run.entries.push(pending);
        assert_eq!(run.end_run(None,None).unwrap()["recorded"],false);
        let held=run.entries.iter().find(|e|e.record_id==entry.record_id).unwrap();assert!(held.pending()&&held.refused.is_none());
        assert_eq!(std::fs::read(&own).unwrap(),before,"already-landed observation cannot be called never written");
        std::fs::remove_file(&other).unwrap();run.retry_records().unwrap();assert!(!run.has_pending_records());
        assert_eq!(own_log(&peer,&a).iter().filter(|e|e["recordId"]==entry.record_id).count(),1);
    }
}

#[test]
fn live_end_exact_foreign_copy_cannot_supply_an_owning_write_receipt(){
    let peer=Peer::new();let mut root=peer.fixture.registered();let a=open_run(&peer,&mut root,"thread");
    let pending=crate::records::supply::PendingRunEntry::new("evidence_limit",json!({"label":"unresolvable reference","subjectRef":"x","detail":"d"}),crate::util::now_rfc3339()).unwrap();let id=pending.record_id.clone();
    crate::records::append_project_reserved(&peer.fixture.root,&a,"foreign-copy",pending.kind,&crate::records::APP_WRITER,pending.body.clone(),&id,&pending.observed_at).unwrap();
    break_act_log(&peer);let own=crate::records::supply::run_log(&peer.fixture.root,&a).unwrap();let before=std::fs::read(&own).unwrap();
    let shared=root.runs[&a].clone();let mut run=shared.lock().unwrap();run.entries.push(pending);
    assert_eq!(run.end_run(None,None).unwrap()["recorded"],false);assert!(run.has_pending_records());
    let held=run.entries.iter().find(|e|e.record_id==id).unwrap();assert!(held.pending()&&held.refused.is_none());
    assert_eq!(std::fs::read(&own).unwrap(),before,"a foreign copy cannot settle the owning observation or let the end skip it");
}

#[test]
fn live_end_conflicting_late_limit_keeps_its_already_landed_parent_pending(){
    use crate::records::RecordSet::ReadableBesideIncomplete;
    let peer=Peer::new();let run="run:late-limit";
    let mut entry=crate::records::supply::PendingRunEntry::new("evidence_limit",json!({"label":"unresolvable reference","subjectRef":"x","detail":"d"}),"2026-10-11T00:00:00Z".into()).unwrap();entry.failure=Some("injected uncertain write".into());
    let mut pending=entry.clone();crate::records::supply::append_run_entry_in(&peer.fixture.root,run,&mut entry,ReadableBesideIncomplete).unwrap();
    let own=crate::records::supply::run_log(&peer.fixture.root,run).unwrap();let before=std::fs::read(&own).unwrap();let limit=crate::records::read_log(&own).0.last().unwrap().clone();
    let other=crate::storage::project_log(&peer.fixture.root,None,"conflicting-limit").unwrap();std::fs::create_dir_all(other.parent().unwrap()).unwrap();std::fs::write(&other,format!("{limit}\n")).unwrap();break_act_log(&peer);
    assert!(crate::records::supply::append_run_entry_in(&peer.fixture.root,run,&mut pending,ReadableBesideIncomplete).is_err_and(|e|e.contains("owning limit cannot be reconciled")));
    assert!(pending.written.is_none());assert_eq!(std::fs::read(&own).unwrap(),before);
    assert!(crate::records::supply::permanent_refusal_in(&peer.fixture.root,run,pending.kind,&pending.record_id,&pending.body,&pending.observed_at,ReadableBesideIncomplete).is_none());
    std::fs::remove_file(&other).unwrap();crate::records::supply::append_run_entry_in(&peer.fixture.root,run,&mut pending,ReadableBesideIncomplete).unwrap();
    assert_eq!(std::fs::read(&own).unwrap(),before,"reconciliation adds no duplicate late limit");
}

// R3 uses the same guarded uncertain-write reconciliation as lifecycle entries.
// W-0 first: a torn tail after the landed R3 is terminated and named, so the
// owning log is complete, and the landed R3 is settled once with its late limit.
#[test]
fn live_end_r3_landed_before_a_torn_own_tail_is_settled_once_after_w0(){
    let peer=Peer::new();let mut root=peer.fixture.registered();let a=open_run(&peer,&mut root,"thread");
    let shared=root.runs[&a].clone();let mut run=shared.lock().unwrap();peer.select_history();run.check_native_supply().unwrap();
    let project=crate::workflow_workspace::publication::ProjectRecords::open(&peer.fixture.root).unwrap();
    let slot=run.checks.last_mut().unwrap();
    slot.r3=WorkflowR3::Pending(crate::records::supply::prepare_live(&project,slot.published.as_ref().unwrap()).unwrap());
    let pending=match &mut slot.r3 {WorkflowR3::Pending(p)=>p,_=>unreachable!()};
    crate::records::supply::append_live(&project,slot.published.as_ref().unwrap(),pending,crate::records::RecordSet::Complete).unwrap();
    let id=pending.record_id().to_owned();pending.hold("injected uncertain write");
    let own=crate::records::supply::run_log(&peer.fixture.root,&a).unwrap();
    let mut f=std::fs::OpenOptions::new().append(true).open(&own).unwrap();std::io::Write::write_all(&mut f,b"{\"torn").unwrap();drop(f);
    let torn=std::fs::read(&own).unwrap();break_act_log(&peer);
    run.end_run(None,None).unwrap();assert!(!run.has_pending_records(),"{}",run.view(&a));
    assert!(std::fs::read(&own).unwrap().starts_with(&torn),"the torn bytes are kept");
    let log=own_log(&peer,&a);
    assert_eq!(log.iter().filter(|e|e["recordId"]==id.as_str()).count(),1,"the landed R3 is not written again");
    let w0=log.iter().position(|e|e["body"]["label"]==crate::records::PARTIAL_NOT_RECOVERED).unwrap();
    let late=log.iter().position(|e|e["kind"]=="evidence_limit"&&e["body"]["subjectRef"]==id.as_str()).unwrap();let end=log.iter().position(|e|e["kind"]=="run_ended").unwrap();
    assert!(w0<late&&late<end);
}
// An unreadable own line holds the R3 pending until repaired.
#[test]
fn live_end_r3_matching_prefix_in_an_unreadable_own_log_stays_pending(){
    let peer=Peer::new();let mut root=peer.fixture.registered();let a=open_run(&peer,&mut root,"thread");
    let shared=root.runs[&a].clone();let mut run=shared.lock().unwrap();peer.select_history();run.check_native_supply().unwrap();
    let project=crate::workflow_workspace::publication::ProjectRecords::open(&peer.fixture.root).unwrap();
    let slot=run.checks.last_mut().unwrap();
    slot.r3=WorkflowR3::Pending(crate::records::supply::prepare_live(&project,slot.published.as_ref().unwrap()).unwrap());
    let pending=match &mut slot.r3 {WorkflowR3::Pending(p)=>p,_=>unreachable!()};
    crate::records::supply::append_live(&project,slot.published.as_ref().unwrap(),pending,crate::records::RecordSet::Complete).unwrap();
    let id=pending.record_id().to_owned();pending.hold("injected uncertain write");
    let own=crate::records::supply::run_log(&peer.fixture.root,&a).unwrap();let before=std::fs::read(&own).unwrap();
    let mut f=std::fs::OpenOptions::new().append(true).open(&own).unwrap();std::io::Write::write_all(&mut f,b"{\"torn\n").unwrap();drop(f);
    let torn=std::fs::read(&own).unwrap();break_act_log(&peer);
    run.end_run(None,None).unwrap();assert!(run.has_pending_records());
    assert!(matches!(&run.checks.last().unwrap().r3,WorkflowR3::Pending(_)));assert_eq!(std::fs::read(&own).unwrap(),torn);
    std::fs::write(&own,before).unwrap();run.retry_records().unwrap();
    assert!(!run.has_pending_records());let log=own_log(&peer,&a);
    assert_eq!(log.iter().filter(|e|e["recordId"]==id.as_str()).count(),1);
    let late=log.iter().position(|e|e["kind"]=="evidence_limit"&&e["body"]["subjectRef"]==id.as_str()).unwrap();let end=log.iter().position(|e|e["kind"]=="run_ended").unwrap();
    assert!(late<end);
}

// A readable collision remains definite at an end even beside unreadable
// unrelated lines. Its never-written limit precedes the end, rather than
// dropping the conflict or holding the run forever.
#[test]
fn live_end_readable_collision_is_refused_with_a_limit_before_end(){
    let peer=Peer::new();let mut root=peer.fixture.registered();let a=open_run(&peer,&mut root,"thread");
    let shared=root.runs[&a].clone();let mut run=shared.lock().unwrap();
    let entry=crate::records::supply::PendingRunEntry::new("evidence_limit",json!({"label":"unresolvable reference","subjectRef":"x","detail":"d"}),crate::util::now_rfc3339()).unwrap();let id=entry.record_id.clone();
    crate::records::append_with_id(&crate::storage::project_log(&peer.fixture.root,None,"conflict-fixture").unwrap(),"evidence_limit",&crate::records::APP_WRITER,json!({"label":"unresolvable reference"}),&id).unwrap();
    run.entries.push(entry);let (other,_)=break_act_log(&peer);let torn=std::fs::read(&other).unwrap();
    run.flush_records();assert!(run.entries.last().unwrap().pending(),"open-run policy keeps the incomplete set pending");
    run.end_run(None,None).unwrap();assert!(!run.has_pending_records());
    let log=own_log(&peer,&a);assert!(!log.iter().any(|e|e["recordId"]==id.as_str()));
    let limit=log.iter().position(|e|e["kind"]=="evidence_limit"&&e["body"]["subjectRef"]==id.as_str()).unwrap();let end=log.iter().position(|e|e["kind"]=="run_ended").unwrap();
    assert!(limit<end);assert!(log[limit]["body"]["detail"].as_str().unwrap().contains("already held"));
    assert_eq!(std::fs::read(&other).unwrap(),torn);
}

#[test]
fn live_end_unconfirmed_start_is_refused_beside_an_incomplete_log(){
    for failure in ["error","exit"] {
        let peer=Peer::new();let mut root=peer.fixture.registered();
        let a=root.prepare_run(peer.home.clone(),&peer.generation,"thread","person".into(),peer.project()).unwrap();
        peer.set_mode("turn-mode",failure);let shared=root.runs[&a].clone();let mut run=shared.lock().unwrap();assert!(run.send().is_err());
        break_act_log(&peer);
        assert!(run.end_run(None,None).is_err_and(|e|e.contains("Only an open run")));
        assert!(!own_log(&peer,&a).iter().any(|e|e["kind"]=="run_opened"||e["kind"]=="run_ended"));
    }
}
// RS §14.1 Permanent refusals review B1, RS W-2: the never-written limit takes the refused record's own
// observation time, so a check observed after the next lifecycle entry is not written
// before the limit or before that entry.
#[test]
fn never_written_limit_keeps_observation_order_with_a_later_check(){
    let peer=Peer::new();let mut root=peer.fixture.registered();
    let reference=root.prepare_run(peer.home.clone(),&peer.generation,"thread","person".into(),peer.project()).unwrap();
    let run=root.runs[&reference].clone();let mut run=run.lock().unwrap();run.send().unwrap();peer.select_history();
    let runs=crate::storage::project_file(&peer.fixture.root, "runs").unwrap();let aside=crate::storage::project_file(&peer.fixture.root, "runs-aside").unwrap();
    std::fs::rename(&runs,&aside).unwrap();std::fs::write(&runs,b"blocked").unwrap();
    let first=run.check_native_supply().unwrap()["check"].clone();let reserved=first["r3"]["recordId"].as_str().unwrap().to_owned();
    run.end_run(None,None).unwrap();assert!(!run.entry_written("run_ended"),"run_ended held");
    std::thread::sleep(std::time::Duration::from_millis(5));
    let second=run.check_native_supply().unwrap()["check"].clone();let later=second["r3"]["recordId"].as_str().unwrap().to_owned();
    assert_ne!(reserved,later);
    std::fs::remove_file(&runs).unwrap();std::fs::rename(&aside,&runs).unwrap();
    crate::records::append_with_id(&crate::storage::project_log(&peer.fixture.root,None,"conflict-fixture").unwrap(),"evidence_limit",&crate::records::APP_WRITER,json!({"label":"unresolvable reference"}),&reserved).unwrap();
    run.retry_records().unwrap();
    let log=rs_for(&peer,&reference);
    let at=|pred:&dyn Fn(&Value)->bool,what:&str|log.iter().position(|e|pred(e)).unwrap_or_else(||panic!("{what} missing: {log:?}"));
    let limit=at(&|e|e["kind"]=="evidence_limit"&&e["body"]["subjectRef"]==reserved.as_str(),"never-written limit");
    let ended=at(&|e|e["kind"]=="run_ended","run_ended");
    let check2=at(&|e|e["recordId"]==later.as_str(),"check 2's R3");
    assert!(limit<ended&&ended<check2,"W-2 observation order: limit {limit}, run_ended {ended}, check 2 {check2}: {:?}",log_order(&peer,&reference));
    assert!(log[limit]["observedAt"].as_str().unwrap()<=log[ended]["observedAt"].as_str().unwrap(),"the limit keeps the refused record's observation time, before run_ended's");
}
// WR TX-5 / SQ-END review M1: the home of a recorded conversation comes from the App's recovery
// ledger (restart fact, the run's own tag, or a single home in the index), never a guess.
#[test]
fn conversation_home_comes_from_the_ledger_or_is_refused(){
    let home=|rows:&[Value],events:&[Value]|crate::run_restart::conversation_home_class(rows,events,"thread","run:a");
    let mut key_fact=restart_fact("cev:x","thread");key_fact["home"]=json!("H-key");
    assert_eq!(home(&[],&[key_fact]).unwrap(),"H-key");
    let mut tagged=index_row("thread",json!([{"owner":crate::run_restart::RUN_TAG_OWNER,"value":"run:a","seq":1}]));tagged["home"]=json!("H-key");
    let mut other=index_row("thread",json!([]));other["home"]=json!("H-acct");
    assert_eq!(home(&[other.clone(),tagged],&[]).unwrap(),"H-key","the run's own tag wins over other rows");
    assert_eq!(home(std::slice::from_ref(&other),&[]).unwrap(),"H-acct");
    let mut key_row=index_row("thread",json!([]));key_row["home"]=json!("H-key");
    assert!(home(&[other,key_row],&[]).unwrap_err().contains("more than one"));
    assert!(home(&[],&[]).unwrap_err().contains("does not say"),"no active-home fallback");
}
// EXEC §2.7 / RECOVERY §4.1 review M3: a conversation whose last REC run tag names a run with no run_opened
// (tagged when run_opened was queued, never written) gets no limit: the current run is not
// established.
#[test]
fn last_tag_naming_an_unrecorded_run_writes_no_limit(){
    let peer=Peer::new();let mut root=peer.fixture.registered();
    let b=open_run(&peer,&mut root,"thread");drop(root);
    let owner=crate::run_restart::RUN_TAG_OWNER;
    let rows=vec![index_row("thread",json!([{"owner":owner,"value":b,"seq":1},{"owner":owner,"value":"run:workflow:never-recorded","seq":2}]))];
    let out=crate::run_restart::write_restart_limits(&peer.fixture.root,&[restart_fact("cev:ghost","thread")],&rows);
    assert_eq!(out[0]["outcome"],"not written","{out:?}");assert!(out[0]["detail"].as_str().unwrap().contains("has no run_opened"),"{out:?}");
    assert!(limits_named(&peer,&b,crate::run_restart::RESTART_LABEL).is_empty());
}
// WR TX-5 / SQ-END review M3: a choice to send without the end notice that cannot be recorded is
// refused; the notice stays pending and nothing is sent.
#[test]
fn unrecordable_skip_is_refused_and_the_notice_stays_pending(){
    use std::os::unix::fs::PermissionsExt;
    let peer=Peer::new();let mut root=peer.fixture.registered();let a=open_run(&peer,&mut root,"thread");
    let mut fresh=WorkflowRootSession::default();fresh.selected=root.selected.take();drop(root);
    fresh.end_recorded_run(&peer.fixture.root,&a,"thread",false,Some(peer.home.clone())).unwrap();
    let root=Mutex::new(fresh);let starts=peer.turn_starts();
    std::fs::set_permissions(wr_dir(&peer),std::fs::Permissions::from_mode(0o500)).unwrap();
    assert!(send_with_pending_notice(&root,&peer.generation,"thread","hello").expect("pending").is_err());
    let runs=crate::storage::project_file(&peer.fixture.root, "runs").unwrap();let aside=crate::storage::project_file(&peer.fixture.root, "runs-aside").unwrap();
    std::fs::rename(&runs,&aside).unwrap();std::fs::write(&runs,b"blocked").unwrap();
    let end=root.lock().unwrap().reopened_end(&a).unwrap();
    let refused=end.lock().unwrap().skip_end_notice().unwrap_err();assert!(refused.contains("stays pending"),"{refused}");
    std::fs::remove_file(&runs).unwrap();std::fs::rename(&aside,&runs).unwrap();
    assert!(send_with_pending_notice(&root,&peer.generation,"thread","hello").expect("still pending").is_err(),"the notice is still pending");
    assert_eq!(peer.turn_starts(),starts,"nothing sent");
    assert!(end.lock().unwrap().skip_end_notice().is_ok(),"the refused choice left the notice pending, so it can be made once recordable");
    std::fs::set_permissions(wr_dir(&peer),std::fs::Permissions::from_mode(0o700)).unwrap();
}

// RS §13.8 with §14.1 Permanent refusals, through the run's flush: a unit only
// partly in its log is settled. Its entry already in the log is shown as
// written (its receipt), the other is never written and named by its "record
// write failed" limit, and the run's later entries proceed.
#[test]
fn a_unit_only_partly_in_its_log_is_settled_and_the_flush_continues(){
    let peer=Peer::new();let mut root=peer.fixture.registered();
    let a=root.prepare_run(peer.home.clone(),&peer.generation,"thread","person".into(),peer.project()).unwrap();
    let run=root.runs[&a].clone();let mut run=run.lock().unwrap();run.send().unwrap();
    let run_id=run.prepared().scope().run.clone();
    let at=crate::util::now_rfc3339();
    let mut first=crate::records::supply::PendingRunEntry::new("evidence_limit",json!({"label":"unresolvable reference","subjectRef":"unit 1"}),at.clone()).unwrap();
    let mut second=crate::records::supply::PendingRunEntry::new("evidence_limit",json!({"label":"unresolvable reference","subjectRef":"unit 2"}),at.clone()).unwrap();
    first.group=Some(first.record_id.clone());second.group=first.group.clone();
    let (first_id,second_id)=(first.record_id.clone(),second.record_id.clone());
    // An earlier write left the first entry alone in the log.
    crate::records::append_project_reserved_in(&peer.fixture.root,&run_id,crate::records::supply::LIVE_WRITER,first.kind,&crate::records::APP_WRITER,first.body.clone(),&first.record_id,&first.observed_at,crate::records::RecordSet::Complete).unwrap();
    run.entries.push(first);run.entries.push(second);
    run.retry_records().unwrap();
    run.end_run(None,None).unwrap();
    assert!(run.entry_written("run_ended"),"the flush continued past the unit");
    let one=run.entries.iter().find(|e|e.record_id==first_id).unwrap();
    assert!(one.written.is_some()&&one.refused.is_none()&&one.failure.is_none(),"in the record: its receipt");
    let two=run.entries.iter().find(|e|e.record_id==second_id).unwrap();
    assert!(two.written.is_none()&&two.refused.as_deref().is_some_and(|r|r.contains("only partly in its log")));
    let records=run.lifecycle_view()["records"].clone();
    let shown=|id:&str|records.as_array().unwrap().iter().find(|r|r["recordId"]==id).cloned().unwrap();
    assert_eq!((shown(&first_id)["written"].as_bool(),shown(&first_id)["neverWritten"].is_null()),(Some(true),true));
    assert_eq!((shown(&second_id)["written"].as_bool(),shown(&second_id)["neverWritten"].is_string()),(Some(false),true));
    let limits=limits_named(&peer,&a,"record write failed");
    assert!(limits.iter().any(|l|l["body"]["subjectRef"]==second_id.as_str()));
    assert!(!limits.iter().any(|l|l["body"]["subjectRef"]==first_id.as_str()),"no limit says the entry in the record was never written");
    assert_eq!(rs_for(&peer,&a).iter().filter(|e|e["recordId"]==first_id.as_str()).count(),1,"not written twice");
}
