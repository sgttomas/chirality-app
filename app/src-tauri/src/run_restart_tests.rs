// CI-20 (c), (d), (j) restart residuals. Included in `workflow_root_tests`
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

// CI-20 (d), EXEC A-2, RECOVERY §4.1: when run_opened is recorded the run's conversation is
// tagged with the run reference in the REC ledger; tags are ordered, a later run's tag is
// appended and the earlier run's tag is kept; `look up` finds the conversation of a tag.
#[test]
fn ci20d_run_tag_written_at_run_opened_ordered_and_earlier_tag_kept(){
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
    let ledger=crate::recovery::RecoveryLedger::open(peer.fixture.root.join("app-data/runtime/recovery.ledger.jsonl")).unwrap().snapshot();
    let rows=ledger["entries"].as_array().unwrap().clone();
    assert_eq!(crate::recovery::tags_of(&rows,"H-acct","thread",owner),tags);
    // The conversation's latest index row itself still carries the earlier run's tag.
    let latest=rows.iter().rev().find(|r|r["kind"]=="conversation_index"&&r["threadId"]=="thread").unwrap();
    assert_eq!(crate::recovery::tags_of(std::slice::from_ref(latest),"H-acct","thread",owner),tags,"an earlier run's tag is never replaced");
    assert_eq!(crate::recovery::look_up(&rows,owner,&b),[("H-acct".to_string(),"thread".to_string())]);
    assert!(crate::recovery::tags_of(&rows,"H-acct","thread","DEL-01-04").is_empty(),"tags of one owner only");
}
// CI-20 (d), RECOVERY §4.1 failure column: a tag that cannot be stored lives in memory only
// and never blocks the run: no ledger, or a ledger that refuses the append.
#[test]
fn ci20d_run_tag_not_stored_keeps_the_run_going(){
    let peer=Peer::new();let mut root=peer.fixture.registered();
    let a=open_run(&peer,&mut root,"thread");
    let view=root.runs[&a].lock().unwrap().view(&a);
    assert_eq!(view["runTag"]["persistence"],"memory-only","{view}");
    assert!(rs_for(&peer,&a).iter().any(|e|e["kind"]=="run_opened"),"the run opened and was recorded");
    use std::os::unix::fs::PermissionsExt;
    let peer=Peer::with_recovery();let mut root=peer.fixture.registered();
    let ledger=peer.fixture.root.join("app-data/runtime/recovery.ledger.jsonl");
    std::fs::set_permissions(&ledger,std::fs::Permissions::from_mode(0o400)).unwrap();
    let a=open_run(&peer,&mut root,"thread");
    std::fs::set_permissions(&ledger,std::fs::Permissions::from_mode(0o600)).unwrap();
    let view=root.runs[&a].lock().unwrap().view(&a);
    assert_eq!(view["runTag"]["persistence"],"memory-only","{view}");assert!(view["runTag"]["limit"].as_str().unwrap().contains("append unavailable"));
    assert_eq!(root.runs[&a].lock().unwrap().lifecycle,RunLifecycle::Open);
    assert!(rs_for(&peer,&a).iter().any(|e|e["kind"]=="run_opened"));
    assert!(peer.home.host.tags_of("H-acct","thread",crate::run_restart::RUN_TAG_OWNER).is_empty());
}
// CI-20 (d), RS "Relaunch with a run interrupted", FC-9, EXEC RE-4: one "App-restart
// interruption" limit on the run current in the conversation at the end (picked from the
// ordered run tags and the RS records), never twice for the same run and fact; an earlier
// ended run is untouched; no run_ended is written; without a stored tag the run is found by
// run_opened.conversationRef and the limit says so; a conversation whose last run had
// ended gets no limit.
#[test]
fn ci20d_restart_limit_written_once_on_the_current_run(){
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
// CI-20 (c), WR TX-5 / SQ-END: an end the person makes after a relaunch gets its end notice,
// composed from the person's end plus the run's recorded run-start run_text (checked against
// its run_opened); the next ordinary turn carries it first, exactly once; until then a run
// start in that conversation is held back (CI-20 (f)).
#[test]
fn ci20c_end_after_relaunch_notice_from_recorded_run_text_carried_once(){
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
// CI-20 (c): with the recorded run text missing, or not matching the run's run_opened, no
// notice is sent and the reason is given; the person's end is still recorded.
#[test]
fn ci20c_end_after_relaunch_refuses_a_notice_without_a_matching_record(){
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
// CI-20 (c) with V10 G-5/R-4: an unwritable notice record sends nothing; the person may
// retry it or send without it, and that choice is recorded in the run's log first.
#[test]
fn ci20c_reopened_notice_record_failure_offers_retry_or_recorded_skip(){
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
// CI-20 (j), RS W-1/W-2: an R3 whose reserved identity is held by a different entry can
// never be written; it is not held: a "record write failed" limit names it as never
// written, and the later run_ended and R3 are written in order.
#[test]
fn ci20j_permanently_refused_r3_gets_its_limit_and_later_records_proceed(){
    let peer=Peer::new();let mut root=peer.fixture.registered();
    let reference=root.prepare_run(peer.home.clone(),&peer.generation,"thread","person".into(),peer.project()).unwrap();
    let run=root.runs[&reference].clone();let mut run=run.lock().unwrap();run.send().unwrap();peer.select_history();
    let runs=peer.fixture.root.join(".chirality/records/runs");let aside=peer.fixture.root.join("runs-aside");
    std::fs::rename(&runs,&aside).unwrap();std::fs::write(&runs,b"blocked").unwrap();
    let first=run.check_native_supply().unwrap()["check"].clone();let reserved=first["r3"]["recordId"].as_str().unwrap().to_owned();
    assert_eq!(first["r3"]["state"],"pending write; missing in record","an I/O failure is held, not refused");
    std::fs::remove_file(&runs).unwrap();std::fs::rename(&aside,&runs).unwrap();
    crate::records::append_with_id(&crate::storage::project_log(&peer.fixture.root,None,"conflict-fixture"),"evidence_limit",&crate::records::APP_WRITER,json!({"label":"unresolvable reference"}),&reserved).unwrap();
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
// CI-20 (j): a nonconformant lifecycle entry (W-1 (a)) is refused permanently too: its limit
// is written in its place and the run_ended behind it is written; a transient failure still
// holds every later entry in strict order.
#[test]
fn ci20j_nonconformant_entry_is_refused_but_transient_failure_keeps_strict_order(){
    let peer=Peer::new();let mut root=peer.fixture.registered();
    let runs=peer.fixture.root.join(".chirality/records/runs");std::fs::write(&runs,b"blocked").unwrap();
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
// CI-20 (d): the startup entry writes nothing without an explicit project or a configured
// REC projection, and says why (shown by workflow_reopen).
#[test]
fn ci20d_startup_writer_states_why_it_did_not_run(){
    let peer=Peer::new();
    assert_eq!(crate::run_restart::startup(&[peer.home.clone()],None)["state"],"not run");
    let out=crate::run_restart::startup(&[peer.home.clone()],peer.project());
    assert!(out["outcomes"].as_array().unwrap().is_empty());
    assert!(out["limits"][0]["limit"].as_str().unwrap().contains("not available"),"{out}");
    let mut root=WorkflowRootSession::default();root.set_restart_limits(out.clone());
    assert_eq!(root.reopen(&peer.fixture.root,&[]).unwrap()["restartLimits"],out);
}
// CI-20 (j): permanence is classified conservatively: an identity conflict found while
// part of the record set cannot be read is not a definite refusal, so the entry stays held.
#[test]
fn ci20j_identity_conflict_in_an_incomplete_record_set_is_not_a_permanent_refusal(){
    let root=std::fs::canonicalize(std::env::temp_dir()).unwrap().join(crate::util::opaque_id("ci20j-").unwrap());std::fs::create_dir_all(&root).unwrap();
    let id="rec:app:held-identity";let body=json!({"label":"record write failed","subjectRef":"x","detail":"d"});
    crate::records::append_with_id(&crate::storage::project_log(&root,None,"conflict-fixture"),"evidence_limit",&crate::records::APP_WRITER,json!({"label":"unresolvable reference"}),id).unwrap();
    let refusal=|| crate::records::supply::permanent_refusal(&root,"run:x","evidence_limit",id,&body,"2026-10-10T00:00:00Z");
    assert!(refusal().is_some_and(|r|r.contains("already held")),"complete set: definite conflict");
    let torn=crate::storage::project_log(&root,None,"other-writer");std::fs::write(&torn,b"{\"torn").unwrap();
    assert!(refusal().is_none(),"an unreadable log leaves the conflict indefinite: stays held");
    std::fs::remove_dir_all(root).unwrap();
}
