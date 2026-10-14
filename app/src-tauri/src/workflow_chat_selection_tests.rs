// Per-chat choices through the same context/selection/preparation controller
// used by lib.rs, with actual Host-issued home/generation/thread identities.
fn chat_context(root:&WorkflowRootSession,home:&Arc<HomeSession>,thread:Option<&str>)->crate::workflow_selection::Context {
    let chat=thread.map(|t|crate::workflow_selection::Chat::in_home(home,t));
    let mut status=home.host.snapshot();
    {let mut history=home.history.lock().unwrap();history.reconcile(&home.host);status["nativeHistory"]=history.snapshot(None);}
    status["workflowRoot"]=root.snapshot();
    crate::workflow_selection::publish_context(&mut status,home);
    let mut context=status["workflowRoot"]["context"].clone();
    context["threadId"]=json!(thread);
    context["selectionRef"]=json!(chat.as_ref().and_then(|c|root.selected.get(c)).map(|s|s.reference.clone()));
    context["inspectionRef"]=json!(root.inspected.as_ref().map(|s|s.reference.clone()));
    context["libraryRef"]=json!(root.active_library);
    serde_json::from_value(context).unwrap()
}
#[test]
fn chat_workflow_published_status_context_acts_and_refuses_after_native_history_changes() {
    let peer=Peer::new();let root=Mutex::new(peer.registered());
    let context=chat_context(&root.lock().unwrap(),&peer.home,Some("thread"));
    assert!(context.history_epoch.is_some(),"the live nativeHistory epoch is in the renderer packet");
    let (review,revision)=review_of(&root.lock().unwrap());
    choose_context(&root,&peer.home,&context,&review,&revision).unwrap();
    let fresh=chat_context(&root.lock().unwrap(),&peer.home,Some("thread"));
    peer.select_history();
    assert_ne!(fresh.history_epoch,peer.home.history.lock().unwrap().snapshot(None)["selectionEpoch"].as_u64());
    assert!(choose_context(&root,&peer.home,&fresh,&review,&revision).unwrap_err().contains("history selection changed"));
    let refreshed=chat_context(&root.lock().unwrap(),&peer.home,Some("thread"));
    choose_context(&root,&peer.home,&refreshed,&review,&revision).unwrap();
}

fn joined_fixture_choices(a:&Peer,b:&Peer)->(WorkflowRootSession,(String,String),(String,String)) {
    let mut root=a.registered();let other=b.registered_with(|p|{
        let file=p.join("WORKFLOW.md");let mut bytes=std::fs::read(&file).unwrap();bytes.extend_from_slice(b"\nSecond fixture revision.\n");std::fs::write(file,bytes).unwrap();
    });
    let first=review_of(&root);let second=review_of(&other);
    root.libraries.extend(other.libraries);root.reviews.extend(other.reviews);
    (root,first,second)
}
fn choose_context(root:&Mutex<WorkflowRootSession>,home:&Arc<HomeSession>,context:&crate::workflow_selection::Context,review:&str,revision:&str)->Result<Value,String> {
    crate::workflow_selection::choose(root,context,||home.clone(),|root,chat|root.select_hot_registered_copy(chat.ok_or("No chat chosen")?,review,revision))
}
#[test]
fn chat_workflow_two_chats_keep_their_pinned_choices_and_started_runs() {
    let a=Peer::new();let b=Peer::new();let (root,first,second)=joined_fixture_choices(&a,&b);
    let second_thread=a.second_thread();let root=Mutex::new(root);
    let chat1=crate::workflow_selection::Chat::in_home(&a.home,"thread");
    let chat2=crate::workflow_selection::Chat::in_home(&a.home,&second_thread);
    let original=root.lock().unwrap().selected[&chat1].reference.clone();
    let no_choice=chat_context(&root.lock().unwrap(),&a.home,Some(&second_thread));
    assert!(crate::workflow_selection::prepare(&root,&no_choice,||a.home.clone(),"new chat".into(),a.project()).unwrap_err().contains("No actual closed workflow selection"));
    let before=a.fixture.rs_entries();
    choose_context(&root,&a.home,&no_choice,&second.0,&second.1).unwrap();
    assert_eq!(a.fixture.rs_entries(),before,"selection keeps the existing record-timing behavior");
    assert_eq!(root.lock().unwrap().selected[&chat1].reference,original);
    assert!(root.lock().unwrap().selected[&chat2].replaces.is_none(),"chat 1's choice is not chat 2's replaced choice");
    let c1=chat_context(&root.lock().unwrap(),&a.home,Some("thread"));
    let c2=chat_context(&root.lock().unwrap(),&a.home,Some(&second_thread));
    let r1=crate::workflow_selection::prepare(&root,&c1,||a.home.clone(),"A".into(),a.project()).unwrap();
    let r2=crate::workflow_selection::prepare(&root,&c2,||a.home.clone(),"B".into(),a.project()).unwrap();
    start_workflow_run(&root,&r1).unwrap();start_workflow_run(&root,&r2).unwrap();
    let bytes=root.lock().unwrap().runs[&r1].lock().unwrap().prepared().text().to_owned();
    let r1_identity=root.lock().unwrap().runs[&r1].lock().unwrap().prepared().workflow().clone();
    let r2_identity=root.lock().unwrap().runs[&r2].lock().unwrap().prepared().workflow().clone();
    assert_eq!(r1_identity.revision,first.1);assert_eq!(r2_identity.revision,second.1);
    choose_context(&root,&a.home,&c1,&second.0,&second.1).unwrap();
    assert_eq!(root.lock().unwrap().runs[&r1].lock().unwrap().prepared().text(),bytes);
    assert_eq!(*root.lock().unwrap().runs[&r1].lock().unwrap().prepared().workflow(),r1_identity);
    let log=a.fixture.rs_entries();
    for (reference,identity,thread) in [(&r1,&r1_identity,"thread"),(&r2,&r2_identity,second_thread.as_str())] {
        let run=root.lock().unwrap().runs[reference].clone();let run=run.lock().unwrap();
        assert_eq!(run.prepared().scope().conversation,thread);
        assert_eq!(run.prepared().scope().home,a.generation["home"].as_str().unwrap());
        assert!(log.iter().any(|e|e["runId"]==reference.as_str()&&e["kind"]=="run_opened"));
        let records=crate::workflow_workspace::publication::ProjectRecords::open(a.project().unwrap()).unwrap();
        let selection=records.resolve(run.view(reference)["publication"]["selection"].as_str().unwrap()).unwrap();
        assert_eq!(selection.body()["conversation"],thread);assert_eq!(selection.body()["identity"],json!(identity));
    }
}
#[test]
fn chat_workflow_identical_thread_ids_in_two_homes_have_distinct_choices() {
    let a=Peer::new();let b=Peer::new();let(root,first,second)=joined_fixture_choices(&a,&b);let root=Mutex::new(root);
    let context=chat_context(&root.lock().unwrap(),&b.home,Some("thread"));
    choose_context(&root,&b.home,&context,&second.0,&second.1).unwrap();
    let ca=chat_context(&root.lock().unwrap(),&a.home,Some("thread"));let cb=chat_context(&root.lock().unwrap(),&b.home,Some("thread"));
    assert_ne!(ca.source_ref,cb.source_ref);
    let ar=crate::workflow_selection::prepare(&root,&ca,||a.home.clone(),"A home".into(),a.project()).unwrap();
    let br=crate::workflow_selection::prepare(&root,&cb,||b.home.clone(),"B home".into(),b.project()).unwrap();
    assert_eq!(root.lock().unwrap().runs[&ar].lock().unwrap().prepared().workflow().revision,first.1);
    assert_eq!(root.lock().unwrap().runs[&br].lock().unwrap().prepared().workflow().revision,second.1);
    assert_eq!(root.lock().unwrap().runs[&ar].lock().unwrap().prepared().scope().home,a.generation["home"].as_str().unwrap());
    assert_eq!(root.lock().unwrap().runs[&br].lock().unwrap().prepared().scope().home,b.generation["home"].as_str().unwrap());
}
#[test]
fn chat_workflow_stale_source_generation_history_and_choice_refuse_without_side_effects() {
    let a=Peer::new();let b=Peer::new();let(root,first,second)=joined_fixture_choices(&a,&b);let root=Mutex::new(root);
    let stale=chat_context(&root.lock().unwrap(),&a.home,Some("thread"));
    let before=a.fixture.rs_entries();
    assert!(choose_context(&root,&b.home,&stale,&second.0,&second.1).is_err());
    let mut old_generation=stale.clone();old_generation.generation["spawnCounter"]=json!(999);
    assert!(choose_context(&root,&a.home,&old_generation,&second.0,&second.1).is_err());
    let mut old_history=stale.clone();old_history.history_epoch=Some(999);
    assert!(choose_context(&root,&a.home,&old_history,&second.0,&second.1).is_err());
    choose_context(&root,&a.home,&stale,&second.0,&second.1).unwrap();
    assert!(choose_context(&root,&a.home,&stale,&first.0,&first.1).unwrap_err().contains("choice changed"));
    assert!(crate::workflow_selection::prepare(&root,&stale,||a.home.clone(),"stale".into(),a.project()).unwrap_err().contains("choice changed"));
    assert_eq!(a.fixture.rs_entries(),before);assert_eq!(a.turn_starts(),0);assert!(root.lock().unwrap().runs.is_empty());
}
#[test]
fn chat_workflow_queued_press_rechecks_the_original_app_source_at_mutation() {
    let a=Peer::new();let b=Peer::new();let(root,_,second)=joined_fixture_choices(&a,&b);let root=Arc::new(Mutex::new(root));
    let context=chat_context(&root.lock().unwrap(),&a.home,Some("thread"));
    let active=Arc::new(Mutex::new(a.home.clone()));let held=root.lock().unwrap();
    let (seen_tx,seen_rx)=std::sync::mpsc::channel();
    let shared=root.clone();let active_source=active.clone();let (review,revision)=second;
    let worker=std::thread::spawn(move||{
        // The closure's immutable call trait uses interior mutability for the witness.
        let seen=std::cell::Cell::new(false);
        let result=crate::workflow_selection::choose(&shared,&context,||{
            let home=active_source.lock().unwrap().clone();if !seen.replace(true){seen_tx.send(()).unwrap();}home
        },|root,chat|root.select_hot_registered_copy(chat.unwrap(),&review,&revision));
        result
    });
    seen_rx.recv_timeout(Duration::from_secs(2)).unwrap();*active.lock().unwrap()=b.home.clone();drop(held);
    assert!(worker.join().unwrap().unwrap_err().contains("source changed"));
    assert_eq!(root.lock().unwrap().selected.len(),1);assert_eq!(a.turn_starts()+b.turn_starts(),0);
}
#[test]
fn chat_workflow_no_chat_inspection_never_fills_a_new_chat_choice() {
    let peer=Peer::new();let root=Mutex::new(peer.registered());let original=chat_context(&root.lock().unwrap(),&peer.home,Some("thread"));
    let no_chat=chat_context(&root.lock().unwrap(),&peer.home,None);
    crate::workflow_selection::choose(&root,&no_chat,||peer.home.clone(),|root,chat|root.select_development_copy(chat,peer.fixture.package.clone())).unwrap();
    assert_eq!(chat_context(&root.lock().unwrap(),&peer.home,Some("thread")).selection_ref,original.selection_ref);
    let new=peer.second_thread();let context=chat_context(&root.lock().unwrap(),&peer.home,Some(&new));
    assert!(context.selection_ref.is_none());
    assert!(crate::workflow_selection::prepare(&root,&context,||peer.home.clone(),"no default".into(),peer.project()).unwrap_err().contains("No actual closed workflow selection"));
    assert!(root.lock().unwrap().snapshot().get("selection").is_none());
    // Inspection can make a draft while Codex has not started, without a chat.
    let cold=Arc::new(HomeSession::new(crate::home_resources::HomeClass::Account,Arc::new(crate::hosting::Host::new()),Err("invented no supplier".into())).unwrap());
    let fixture=Fixture::new();let empty=Mutex::new(WorkflowRootSession::default());let context=chat_context(&empty.lock().unwrap(),&cold,None);
    crate::workflow_selection::choose(&empty,&context,||cold.clone(),|root,chat|root.select_development_copy(chat,fixture.package.clone())).unwrap();
    let context=chat_context(&empty.lock().unwrap(),&cold,None);
    crate::workflow_selection::with_choice(&empty,&context,||cold.clone(),|root,_,chat| {
        root.open_library(fixture.root.clone(),"project",Some(&fixture.root),Arc::new(Mutex::new(Some(crate::act_control::ActControl::new(&fixture.root)))))?;
        root.create_selected_draft(chat,"from-inspection")
    }).unwrap();
    assert!(empty.lock().unwrap().selected.is_empty());assert!(fixture.root.join(".chirality/workflow-drafts/from-inspection/WORKFLOW.md").is_file());
}
#[test]
fn chat_workflow_selection_supersedes_only_its_own_chat_proposals() {
    let peer=Peer::new();let mut root=peer.registered();let second=peer.second_thread();
    let mut view=offer_view(&peer,&[("turn","p",1,PROPOSED,"live-observed")]);
    let mut other=view["items"][1].clone();other["threadId"]=json!(second);other["native"]["id"]=json!("p2");other["observedOrder"]=json!(2);
    view["items"].as_array_mut().unwrap().push(other);
    assert_eq!(root.offers(&view).as_array().unwrap().len(),2);
    root.note_selection(&view,&second);
    let offers=root.offers(&view);assert_eq!(offers.as_array().unwrap().len(),1);assert_eq!(offers[0]["message"]["threadId"],"thread");
}
