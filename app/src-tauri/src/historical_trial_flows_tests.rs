// Invented native Host peer; no live supplier or actual human act is witnessed.
fn historical_trial_peer() -> Peer {
    let mut peer = Peer::with_recovery();
    peer.home
        .host
        .stop(
            "historical fixture setup",
            "install durable invented history",
        )
        .unwrap();
    let path = peer.fixture.root.join("owned-peer.py");
    let mut source = std::fs::read_to_string(&path).unwrap();
    let save="  text=f['params']['input'][0]['text'];client=f['params'].get('clientUserMessageId','');inputs=[e.get('text','') for e in f['params']['input']];result={'turn':turn()}";
    let extra = r#"
  hp='learning-history.json'
  h=json.load(open(hp)) if os.path.exists(hp) else {}
  tid=f['params']['threadId'];u=turn()['id'];entry=h.setdefault(tid,{'turns':[],'items':{}})
  if not any(t['id']==u for t in entry['turns']):entry['turns'].append(turn())
  entry['items'][u]=[{'turnId':u,'item':{'id':u+'-user','type':'userMessage','clientId':client,'content':f['params']['input']}},
   {'turnId':u,'item':{'id':u+'-reply','type':'agentMessage','text':'Invented historical native result for '+u}}]
  json.dump(h,open(hp,'w'))
"#;
    assert!(source.contains(save));
    source = source.replace(save, &format!("{save}{extra}"));
    let marker =
        " elif method=='thread/turns/list' and f['params'].get('threadId','').startswith('child'):";
    let history = r#" elif method in ('thread/turns/list','thread/items/list') and os.path.exists('learning-history.json'):
  h=json.load(open('learning-history.json'));e=h.get(f['params']['threadId'],{'turns':[],'items':{}})
  if mode('learning-read-mode')=='slow':
   import time;time.sleep(0.2)
  if method=='thread/turns/list':
   if mode('learning-turns-mode')=='malformed-later':
    result={'data':'malformed invented later page','nextCursor':None} if f['params'].get('cursor') else {'data':e['turns'][:1],'nextCursor':'later'}
   elif mode('learning-turns-mode')=='repeat':result={'data':e['turns'][:1],'nextCursor':'same'}
   else:result={'data':e['turns'],'nextCursor':None}
  else:result={'data':e['items'].get(f['params']['turnId'],[]),'nextCursor':None}
"#;
    assert!(source.contains(marker));
    source = source.replace(marker, &format!("{history}{marker}"));
    std::fs::write(path, source).unwrap();
    peer.generation = peer.relaunch();
    let context = crate::recovery::ExplicitAppProjectContext::known(
        "fixture App project",
        crate::recovery::AppProjectSource::ConfiguredDirectory,
    )
    .unwrap();
    peer.home
        .host
        .observe_conversation_project(&peer.generation, "thread", Some("H-acct"), &context)
        .unwrap();
    peer
}
fn historical_trial_new_process(peer: &mut Peer) {
    peer.home
        .host
        .stop("invented App restart", "old native Host owner ends")
        .unwrap();
    let cfg = peer.home.host_config.as_ref().unwrap().clone();
    let host = Arc::new(crate::hosting::Host::new());
    host.configure_recovery(
        peer.fixture
            .root
            .join("app-data/runtime/recovery.ledger.jsonl"),
    )
    .unwrap();
    host.start(&cfg, "new invented App Host").unwrap();
    host.thread_start_with_guidance(
        &cfg.cwd.to_string_lossy(),
        "fixture-model",
        "fixture-provider",
        "existing role unchanged",
    )
    .unwrap();
    peer.generation = host.snapshot()["generation"].clone();
    peer.home = Arc::new(
        HomeSession::new(crate::home_resources::HomeClass::Account, host, Ok(cfg)).unwrap(),
    );
    let context = crate::recovery::ExplicitAppProjectContext::known(
        "fixture App project",
        crate::recovery::AppProjectSource::ConfiguredDirectory,
    )
    .unwrap();
    peer.home
        .host
        .observe_conversation_project(&peer.generation, "thread", Some("H-acct"), &context)
        .unwrap();
}
fn historical_trial_read_history(peer: &Peer) -> Value {
    serde_json::from_slice(&std::fs::read(peer.fixture.root.join("learning-history.json")).unwrap())
        .unwrap()
}
fn historical_trial_write_history(peer: &Peer, value: &Value) {
    std::fs::write(
        peer.fixture.root.join("learning-history.json"),
        serde_json::to_vec(value).unwrap(),
    )
    .unwrap();
}
fn historical_trial_snapshot(root: &Mutex<WorkflowRootSession>) -> Value {
    let root = root.lock().unwrap();
    let mut view = root.snapshot();
    root.decorate_status(&mut view, &json!({}));
    view
}
#[test]
fn historical_trial_run_after_restart_brings_back_unsent_without_restoring_owners() {
    let mut peer = historical_trial_peer();
    let mut live = peer.registered();
    let run = open_run(&peer, &mut live, "thread");
    // The ordinary positive start ack is durable REC location evidence; no
    // artificial human Check action is needed for subsequent learning.
    let before = peer.turn_starts();
    drop(live);
    let old_generation = peer.generation.clone();
    historical_trial_new_process(&mut peer);
    assert_ne!(peer.generation, old_generation);
    let mut fresh = WorkflowRootSession::default();
    fresh.set_app_user_data(peer.fixture.root.join("app-data"));
    let root = Mutex::new(fresh);
    let pending = trial_flows::bring_back_with_homes(
        &root,
        &[peer.home.clone()],
        peer.project(),
        &peer.home,
        None,
        Some(&run),
        &peer.generation,
        "thread",
        false,
    )
    .unwrap();
    assert_eq!(peer.turn_starts(), before, "reading and prefill never send");
    assert!(root.lock().unwrap().runs.is_empty());
    let view = historical_trial_snapshot(&root);
    assert_eq!(
        view["pendingBringBacks"][0]["target"]["generation"],
        peer.generation
    );
    assert_eq!(
        view["pendingBringBacks"][0]["source"]["generation"],
        peer.generation
    );
    let text = view["pendingBringBacks"][0]["transcript"].as_str().unwrap();
    assert!(
        text.contains("Invented historical native result for turn"),
        "{text}"
    );
    assert!(pending["card"]
        .as_str()
        .unwrap()
        .contains("historical quoted"));
    trial_flows::cancel_bring_back(&root, pending["id"].as_str().unwrap()).unwrap();
    assert_eq!(peer.turn_starts(), before);
}
#[test]
fn historical_trial_source_is_separate_from_target_and_duplicate_home_ids_refuse() {
    let source = historical_trial_peer();
    let mut target = Peer::with_class(crate::home_resources::HomeClass::ApiKey);
    let mut live = source.registered();
    let run = open_run(&source, &mut live, "thread");
    drop(live);
    let root = Mutex::new(WorkflowRootSession::default());
    // Key is another native source even when its supplier repeats "thread".
    Arc::get_mut(&mut target.home).unwrap().workflow_source_ref =
        "invented explicit target home".into();
    let target_home = target.home.clone();
    let homes = vec![target_home.clone(), source.home.clone()];
    let sent = (source.turn_starts(), target.turn_starts());
    let pending = trial_flows::bring_back_with_homes(
        &root,
        &homes,
        source.project(),
        &target_home,
        None,
        Some(&run),
        &target.generation,
        "thread",
        false,
    )
    .unwrap();
    assert_eq!(pending["source"]["generation"], source.generation);
    let view = historical_trial_snapshot(&root);
    assert_eq!(
        view["pendingBringBacks"][0]["target"]["generation"],
        target.generation
    );
    assert!(view["pendingBringBacks"][0]["transcript"]
        .as_str()
        .unwrap()
        .contains("Invented historical native result"));
    assert_eq!((source.turn_starts(), target.turn_starts()), sent);
    let duplicated = vec![
        source.home.clone(),
        source.home.clone(),
        target_home.clone(),
    ];
    let error = trial_flows::bring_back_with_homes(
        &root,
        &duplicated,
        source.project(),
        &target_home,
        None,
        Some(&run),
        &target.generation,
        "thread",
        false,
    )
    .unwrap_err();
    assert!(error.contains("ambiguous"), "{error}");
}
#[test]
fn historical_trial_malformed_later_page_is_named_and_does_not_become_empty_history() {
    let peer = historical_trial_peer();
    let mut root = peer.registered();
    let _ = open_run(&peer, &mut root, "thread");
    peer.set_mode("learning-turns-mode", "malformed-later");
    let (turns, limit) = trial_flows::read_turns(
        &peer.home,
        &peer.generation,
        "thread",
        &trial_flows::person_read(),
    );
    assert_eq!(
        turns.len(),
        1,
        "valid earlier page remains available to its reader"
    );
    assert!(limit.unwrap().contains("schema refused"));
}

struct HistoricalTrialCleanup(PathBuf);
impl Drop for HistoricalTrialCleanup {
    fn drop(&mut self) {
        let _ = std::fs::remove_dir_all(&self.0);
    }
}
#[test]
fn historical_trial_imported_run_compares_with_persisted_trial_without_selecting_or_sending() {
    let _source_store = RoleR3Store::new();
    let peer = historical_trial_peer();
    let mut live = trial_root(&peer);
    let trial = live
        .prepare_trial(
            "clean",
            DRAFT,
            Some((&peer.generation, "thread")),
            Some(&peer.home),
            peer.project(),
        )
        .unwrap()["reference"]
        .as_str()
        .unwrap()
        .to_owned();
    live.begin_clean_start(&trial).unwrap();
    let thread = peer.second_thread();
    live.mark_clean_started(&trial, &peer.generation, &thread);
    let live = Mutex::new(live);
    trial_flows::send_trial(
        &live,
        &peer.home,
        &trial,
        &peer.generation,
        &thread,
        "Invented trial input",
    )
    .unwrap();
    let run = open_run(&peer, &mut live.lock().unwrap(), "thread");
    drop(live);
    let bag_path = peer
        .fixture
        .root
        .with_extension("historical-learning-export");
    let _bag_cleanup = HistoricalTrialCleanup(bag_path.clone());
    crate::records_export::export(&peer.fixture.root, &bag_path).unwrap();
    let _destination = RoleR3Store::new();
    let actor = crate::act_control::person(
        Some("invented learning import fixture"),
        Some("fixture account"),
    );
    let observed = json!({"fixture":"native import stand-in; no person witness"});
    let plan =
        crate::records_store::package::prepare(&peer.fixture.root, &bag_path, &actor, &observed)
            .unwrap();
    crate::records_store::package::apply(plan, &actor, &observed).unwrap();
    let mut fresh = WorkflowRootSession::default();
    fresh.set_app_user_data(peer.fixture.root.join("app-data"));
    fresh
        .open_library(
            peer.fixture.root.clone(),
            "project",
            Some(&peer.fixture.root),
            Arc::new(Mutex::new(None)),
        )
        .unwrap();
    let fresh = Mutex::new(fresh);
    let sent = peer.turn_starts();
    let compare = trial_flows::compare_with_homes(
        &fresh,
        &[peer.home.clone()],
        peer.project(),
        &json!({"trial":trial}),
        &json!({"run":run}),
    )
    .unwrap();
    assert_eq!(compare["right"]["kind"], "registered run");
    assert!(
        compare["right"]["summary"]["limits"]
            .as_array()
            .unwrap()
            .iter()
            .any(|limit| limit.as_str().unwrap_or_default().contains("historical")),
        "{compare}"
    );
    assert!(compare["difference"]["files"].is_array(), "{compare}");
    let unavailable = trial_flows::compare_with_homes(
        &fresh,
        &[],
        peer.project(),
        &json!({"trial":trial}),
        &json!({"run":run}),
    )
    .unwrap();
    assert!(
        unavailable["difference"]["files"].is_array(),
        "version bytes remain comparable without native home"
    );
    assert_eq!(unavailable["right"]["summary"]["turns"], 0);
    let pending = trial_flows::bring_back_with_homes(
        &fresh,
        &[peer.home.clone()],
        peer.project(),
        &peer.home,
        None,
        Some(&run),
        &peer.generation,
        "thread",
        false,
    )
    .unwrap();
    assert!(pending["card"].as_str().unwrap().contains("historical"));
    assert_eq!(peer.turn_starts(), sent);
    assert!(fresh.lock().unwrap().runs.is_empty());
    assert!(fresh.lock().unwrap().selected.is_empty());
    let homes = [peer.home.clone()];
    let (rows, events) = trial_flows::recovery_facts(&homes);
    let shared = trial_flows::learning_status_with_facts(
        &homes,
        peer.project(),
        &run,
        Some("thread"),
        &rows,
        &events,
    );
    assert_eq!(shared["bringBack"]["offered"], true, "{shared}");
    assert_eq!(
        shared,
        trial_flows::learning_status(&homes, peer.project(), &run, Some("thread"))
    );
    let missing_from_snapshot = trial_flows::learning_status_with_facts(
        &homes,
        peer.project(),
        &run,
        Some("thread"),
        &[],
        &[],
    );
    assert_eq!(missing_from_snapshot["bringBack"]["offered"], false);
    assert_eq!(missing_from_snapshot["compare"]["offered"], true);
    assert_eq!(
        trial_flows::learning_status(&[], peer.project(), &run, Some("thread"))["compare"]
            ["offered"],
        true
    );
    assert_eq!(
        trial_flows::learning_status(&[], peer.project(), &run, Some("thread"))["bringBack"]
            ["offered"],
        false
    );
}
#[test]
fn historical_trial_exact_end_and_chain_boundaries_ignore_pasted_prefix_and_exclude_later_activity()
{
    let peer = historical_trial_peer();
    let mut live = peer.registered();
    let run = open_run(&peer, &mut live, "thread");
    peer.set_mode("turn-id", "pasted-prefix");
    peer.home.host.turn_start_texts(&peer.generation,"thread",&[&format!("[Chirality] Workflow run ended: pasted prefix (run {run}-collision), not the original native end")],"invented-pasted-client").unwrap();
    live.runs[&run].lock().unwrap().end_run(None, None).unwrap();
    peer.set_mode("turn-id", "original-end");
    let result = live.runs[&run].lock().unwrap().send_end_notice_in_mode(
        &peer.generation,
        "ordinary after end",
        None,
    );
    result.result.unwrap();
    peer.set_mode("turn-id", "after-original-end");
    peer.home
        .host
        .turn_start_texts(
            &peer.generation,
            "thread",
            &["Activity after the original end must be excluded"],
            "later-ordinary-client",
        )
        .unwrap();
    peer.set_mode("turn-id", "following-run");
    let following = open_run(&peer, &mut live, "thread");
    assert_ne!(following, run);
    drop(live);
    let root = Mutex::new(WorkflowRootSession::default());
    let pending = trial_flows::bring_back_with_homes(
        &root,
        &[peer.home.clone()],
        peer.project(),
        &peer.home,
        None,
        Some(&run),
        &peer.generation,
        "thread",
        false,
    )
    .unwrap();
    let view = historical_trial_snapshot(&root);
    let text = view["pendingBringBacks"][0]["transcript"].as_str().unwrap();
    assert!(text.contains("pasted prefix"), "{text}");
    assert!(text.contains("Invented historical native result for pasted-prefix"));
    assert!(!text.contains("Activity after the original end"));
    assert!(!text.contains("Invented historical native result for following-run"));
    trial_flows::cancel_bring_back(&root, pending["id"].as_str().unwrap()).unwrap();
    let mut history = historical_trial_read_history(&peer);
    let original = history["thread"]["items"]["original-end"].clone();
    history["thread"]["turns"]
        .as_array_mut()
        .unwrap()
        .retain(|turn| turn["id"] != "original-end");
    history["thread"]["items"]
        .as_object_mut()
        .unwrap()
        .remove("original-end");
    let mut pasted = original;
    pasted[0]["turnId"] = json!("pasted-prefix");
    pasted[0]["item"]["clientId"] = json!("invented-pasted-client");
    history["thread"]["items"]["pasted-prefix"] = pasted;
    historical_trial_write_history(&peer, &history);
    let error = trial_flows::bring_back_with_homes(
        &root,
        &[peer.home.clone()],
        peer.project(),
        &peer.home,
        None,
        Some(&run),
        &peer.generation,
        "thread",
        false,
    )
    .unwrap_err();
    assert!(error.contains("boundary turn is missing"), "{error}");
    assert!(historical_trial_snapshot(&root)["pendingBringBacks"]
        .as_array()
        .unwrap()
        .is_empty());
}
#[test]
fn historical_trial_cold_source_live_turn_refuses_even_with_an_empty_native_view() {
    let peer = historical_trial_peer();
    let mut live = peer.registered();
    let run = open_run(&peer, &mut live, "thread");
    drop(live);
    let mut history = historical_trial_read_history(&peer);
    history["thread"]["turns"][0]["status"] = json!("inProgress");
    historical_trial_write_history(&peer, &history);
    let root = Mutex::new(WorkflowRootSession::default());
    let error = trial_flows::bring_back_with_homes(
        &root,
        &[peer.home.clone()],
        peer.project(),
        &peer.home,
        None,
        Some(&run),
        &peer.generation,
        "thread",
        false,
    )
    .unwrap_err();
    assert!(error.contains("live"), "{error}");
    assert!(historical_trial_snapshot(&root)["pendingBringBacks"]
        .as_array()
        .unwrap()
        .is_empty());
}
fn historical_trial_wait_for_query(peer: &Peer, before: usize) {
    let start = std::time::Instant::now();
    loop {
        let found = std::fs::read_to_string(peer.fixture.root.join("wire.jsonl"))
            .unwrap_or_default()
            .lines()
            .filter_map(|line| serde_json::from_str::<Value>(line).ok())
            .filter(|frame| frame["method"] == "thread/turns/list")
            .count();
        if found > before {
            return;
        }
        assert!(
            start.elapsed() < Duration::from_secs(3),
            "native read was not reached"
        );
        std::thread::sleep(Duration::from_millis(5));
    }
}
#[test]
fn historical_trial_generation_changed_during_blocking_history_read_prevents_prefill() {
    let peer = historical_trial_peer();
    let mut live = peer.registered();
    let run = open_run(&peer, &mut live, "thread");
    drop(live);
    peer.set_mode("learning-read-mode", "slow");
    let before = peer
        .wire()
        .iter()
        .filter(|frame| frame["method"] == "thread/turns/list")
        .count();
    let root = Mutex::new(WorkflowRootSession::default());
    let homes = vec![peer.home.clone()];
    std::thread::scope(|scope| {
        let read = scope.spawn(|| {
            trial_flows::bring_back_with_homes(
                &root,
                &homes,
                peer.project(),
                &peer.home,
                None,
                Some(&run),
                &peer.generation,
                "thread",
                false,
            )
        });
        historical_trial_wait_for_query(&peer, before);
        peer.home
            .host
            .stop(
                "invented concurrent generation change",
                "fixture mutation during read",
            )
            .unwrap();
        let next = peer.relaunch();
        assert_ne!(next, peer.generation);
        assert!(read.join().unwrap().is_err());
    });
    assert!(historical_trial_snapshot(&root)["pendingBringBacks"]
        .as_array()
        .unwrap()
        .is_empty());
}
#[test]
fn historical_trial_new_process_can_end_original_run_and_bound_at_new_typed_notice() {
    let mut peer = historical_trial_peer();
    let mut live = peer.registered();
    let run = open_run(&peer, &mut live, "thread");
    drop(live);
    historical_trial_new_process(&mut peer);
    let mut ended = WorkflowRootSession::default();
    ended
        .end_recorded_run(
            &peer.fixture.root,
            &run,
            "thread",
            false,
            Some(peer.home.clone()),
        )
        .unwrap();
    peer.set_mode("turn-id", "new-process-end");
    ended
        .reopened_end(&run)
        .unwrap()
        .lock()
        .unwrap()
        .send_end_notice_in_mode(
            &peer.generation,
            "ordinary carried notice after actual App restart",
            None,
        )
        .result
        .unwrap();
    peer.set_mode("turn-id", "new-process-after-end");
    peer.home
        .host
        .turn_start_texts(
            &peer.generation,
            "thread",
            &["must stay outside the earlier run"],
            "new-process-later-client",
        )
        .unwrap();
    drop(ended);
    let fresh = Mutex::new(WorkflowRootSession::default());
    trial_flows::bring_back_with_homes(
        &fresh,
        &[peer.home.clone()],
        peer.project(),
        &peer.home,
        None,
        Some(&run),
        &peer.generation,
        "thread",
        false,
    )
    .unwrap();
    let view = historical_trial_snapshot(&fresh);
    let text = view["pendingBringBacks"][0]["transcript"].as_str().unwrap();
    assert!(text.contains("Invented historical native result for turn"));
    assert!(!text.contains("must stay outside"));
    assert!(fresh.lock().unwrap().runs.is_empty());
}
#[test]
fn historical_trial_compare_refuses_same_origin_and_name_from_different_source_roots() {
    let a = historical_trial_peer();
    let b = historical_trial_peer();
    let mut authoring = trial_root(&a);
    let trial = authoring
        .prepare_trial("clean", DRAFT, None, Some(&a.home), a.project())
        .unwrap()["reference"]
        .as_str()
        .unwrap()
        .to_owned();
    authoring.begin_clean_start(&trial).unwrap();
    let thread = a.second_thread();
    authoring.mark_clean_started(&trial, &a.generation, &thread);
    let authoring = Mutex::new(authoring);
    trial_flows::send_trial(&authoring, &a.home, &trial, &a.generation, &thread, "").unwrap();
    drop(authoring);
    let mut other = b.registered();
    let run = open_run(&b, &mut other, "thread");
    drop(other);
    let mut fresh = WorkflowRootSession::default();
    fresh.set_app_user_data(a.fixture.root.join("app-data"));
    for library in [&a.fixture.root, &b.fixture.root] {
        fresh
            .open_library(library.clone(), "project", None, Arc::new(Mutex::new(None)))
            .unwrap();
    }
    let fresh = Mutex::new(fresh);
    let error = trial_flows::compare_with_homes(
        &fresh,
        &[],
        b.project(),
        &json!({"trial":trial}),
        &json!({"run":run}),
    )
    .unwrap_err();
    assert!(error.contains("full source-qualified slot"), "{error}");
}
#[test]
fn historical_trial_original_records_home_replaced_during_history_read_prevents_prefill() {
    let store = RoleR3Store::new();
    let peer = historical_trial_peer();
    let mut live = peer.registered();
    let run = open_run(&peer, &mut live, "thread");
    drop(live);
    peer.set_mode("learning-read-mode", "slow");
    let before = peer
        .wire()
        .iter()
        .filter(|frame| frame["method"] == "thread/turns/list")
        .count();
    let original = store.0.clone();
    let displaced = original.with_extension("learning-displaced-store");
    let _cleanup = HistoricalTrialCleanup(displaced.clone());
    let identity = std::fs::read(original.join("store.json")).unwrap();
    let root = Mutex::new(WorkflowRootSession::default());
    let homes = vec![peer.home.clone()];
    std::thread::scope(|scope| {
        let read = scope.spawn(|| {
            crate::records_store::use_store_for_test(Some(Ok(crate::records_store::Store {
                root: original.clone(),
                placement: crate::records_store::Placement::Test,
                limits: vec![],
            })));
            let result = trial_flows::bring_back_with_homes(
                &root,
                &homes,
                peer.project(),
                &peer.home,
                None,
                Some(&run),
                &peer.generation,
                "thread",
                false,
            );
            crate::records_store::use_store_for_test(None);
            result
        });
        historical_trial_wait_for_query(&peer, before);
        std::fs::rename(&original, &displaced).unwrap();
        std::fs::create_dir(&original).unwrap();
        std::fs::write(original.join("store.json"), identity).unwrap();
        assert!(read.join().unwrap().is_err());
    });
    assert!(historical_trial_snapshot(&root)["pendingBringBacks"]
        .as_array()
        .unwrap()
        .is_empty());
}
#[test]
fn historical_trial_positive_ack_metadata_retry_after_same_host_restart_sends_no_new_turn() {
    let mut peer = historical_trial_peer();
    let mut root = peer.registered();
    let ledger = peer
        .fixture
        .root
        .join("app-data/runtime/recovery.ledger.jsonl");
    let path = crate::recovery::database_path(&ledger);
    let saved = path.with_extension("learning-saved-db");
    std::fs::rename(&path, &saved).unwrap();
    std::fs::create_dir(&path).unwrap();
    let run = open_run(&peer, &mut root, "thread");
    assert_eq!(
        root.runs[&run].lock().unwrap().view(&run)["learningPointers"][0]["persistence"],
        "memory-only"
    );
    let starts = peer.turn_starts();
    peer.home
        .host
        .stop(
            "invented same-Host restart",
            "retain actual typed ACK pointer only",
        )
        .unwrap();
    peer.generation = peer.relaunch();
    std::fs::remove_dir(&path).unwrap();
    std::fs::rename(saved, &path).unwrap();
    root.runs[&run].lock().unwrap().retry_records().unwrap();
    assert_eq!(
        peer.turn_starts(),
        starts,
        "metadata retry never resends the original turn"
    );
    assert_eq!(
        root.runs[&run].lock().unwrap().view(&run)["learningPointers"][0]["persistence"],
        "durable App metadata"
    );
    drop(root);
    let fresh = Mutex::new(WorkflowRootSession::default());
    trial_flows::bring_back_with_homes(
        &fresh,
        &[peer.home.clone()],
        peer.project(),
        &peer.home,
        None,
        Some(&run),
        &peer.generation,
        "thread",
        false,
    )
    .unwrap();
    assert_eq!(peer.turn_starts(), starts);
}

#[test]
fn historical_attachment_notice_without_manual_checks_survives_all_owners_and_bounds_learning() {
    let mut peer = historical_trial_peer();
    let mut live = trial_root(&peer);
    let trial = live.prepare_trial("clean", DRAFT, Some((&peer.generation, "thread")), Some(&peer.home), peer.project()).unwrap()["reference"].as_str().unwrap().to_owned();
    live.begin_clean_start(&trial).unwrap();
    let trial_thread = peer.second_thread();
    live.mark_clean_started(&trial, &peer.generation, &trial_thread);
    let live = Mutex::new(live);
    peer.set_mode("turn-id", "attachment-comparison-trial");
    trial_flows::send_trial(&live, &peer.home, &trial, &peer.generation, &trial_thread, "trial input").unwrap();
    peer.set_mode("turn-id", "attachment-run-start");
    let run = open_run(&peer, &mut live.lock().unwrap(), "thread");
    let workflow = live.lock().unwrap().runs[&run].lock().unwrap().prepared().record()["workflow"].clone();
    peer.set_mode("turn-id", "attachment-run-activity");
    peer.home.host.turn_start_texts(&peer.generation, "thread", &["Exact activity inside the registered run"], "in-run-client").unwrap();
    live.lock().unwrap().runs[&run].lock().unwrap().end_run(None, None).unwrap();
    peer.set_mode("turn-id", "attachment-end-carrier");
    let (list, owner, revision, refs, custody, _) = attachment(&peer, "learning-carrier.txt", "carrier-only file bytes must stay outside the run\n");
    let sent = submit_attachments_with_pending_notice(&list, &live, &peer.home.host, Ok(custody.clone()), &owner, revision, &refs, &peer.generation, "thread", None, "carrier-only person text must stay outside the run", crate::recovery::ExplicitAppProjectContext::unknown(), None).unwrap();
    assert_eq!(sent["endNotice"]["turn"], "attachment-end-carrier");
    assert_eq!(sent["endNotice"]["outcome"]["learningBoundary"]["persistence"], "durable App metadata");
    peer.set_mode("turn-id", "attachment-later-turn");
    peer.home.host.turn_start_texts(&peer.generation, "thread", &["later-only activity must stay outside the run"], "later-client").unwrap();
    let before_records = peer.fixture.rs_entries();
    assert_eq!(kinds_of(&rs_for(&peer, &run)), ["run_opened", "run_ended"]);
    let wr_folder = crate::storage::project_file(&peer.fixture.root, "workflow").unwrap();
    let wr = peer.fixture.wr_files();
    assert!(wr.iter().all(|name| {
        let row: Value = serde_json::from_slice(&std::fs::read(wr_folder.join(name)).unwrap()).unwrap();
        row["body"]["record_kind"] != "supply_check"
    }), "neither start nor end requires a manual Check");
    let old_host = Arc::downgrade(&peer.home.host);
    drop((live, list, custody));
    let original_generation = peer.generation.clone();
    historical_trial_new_process(&mut peer);
    assert!(old_host.upgrade().is_none(), "all original Host/run/selection owners ended");
    assert_ne!(original_generation, peer.generation);
    let mut target = Peer::with_class(crate::home_resources::HomeClass::ApiKey);
    Arc::get_mut(&mut target.home).unwrap().workflow_source_ref = "separate learning target".into();
    let mut fresh = WorkflowRootSession::default();
    fresh.set_app_user_data(peer.fixture.root.join("app-data"));
    fresh.open_library(peer.fixture.root.clone(), "project", peer.project(), Arc::new(Mutex::new(None))).unwrap();
    let fresh = Mutex::new(fresh);
    let homes = [target.home.clone(), peer.home.clone()];
    let starts = (peer.turn_starts(), target.turn_starts());
    let pending = trial_flows::bring_back_with_homes(&fresh, &homes, peer.project(), &target.home, None, Some(&run), &target.generation, "thread", false).unwrap();
    let view = historical_trial_snapshot(&fresh);
    assert_eq!(view["pendingBringBacks"][0]["source"]["generation"], peer.generation);
    assert_eq!(view["pendingBringBacks"][0]["target"]["generation"], target.generation);
    let text = view["pendingBringBacks"][0]["transcript"].as_str().unwrap();
    for exact in ["Exact activity inside the registered run", "Invented historical native result for attachment-run-start", "Invented historical native result for attachment-run-activity"] {
        assert!(text.contains(exact), "{text}");
    }
    for excluded in ["carrier-only", "attachment-end-carrier", "later-only", "attachment-later-turn", "attachment-comparison-trial"] {
        assert!(!text.contains(excluded), "{text}");
    }
    assert!(pending["card"].as_str().unwrap().contains("historical quoted"));
    let compare = trial_flows::compare_with_homes(&fresh, &homes, peer.project(), &json!({"trial":trial}), &json!({"run":run})).unwrap();
    assert_eq!(compare["right"]["version"], json!({"method":workflow["revision_method"],"value":workflow["revision"]}));
    assert_eq!(compare["right"]["summary"]["turns"], 2, "{compare}");
    assert_eq!(compare["right"]["summary"]["endings"], json!([{"turn":"attachment-run-start","status":"failed"},{"turn":"attachment-run-activity","status":"failed"}]));
    assert_eq!(compare["right"]["summary"]["finalAgentMessage"], "Invented historical native result for attachment-run-activity");
    assert_eq!(compare["difference"]["files"], json!([]));
    assert!(compare["difference"]["unchanged"].as_u64().unwrap() > 0);
    assert_eq!((peer.turn_starts(), target.turn_starts()), starts, "Bring back/Compare only prefill/read");
    assert_eq!(peer.fixture.rs_entries(), before_records);
    assert_eq!(peer.fixture.wr_files(), wr);
    let root = fresh.lock().unwrap();
    assert!(root.runs.is_empty() && root.selected.is_empty() && root.reviews.is_empty(), "no run, selection or registration act owner restored");
}

#[test]
fn historical_attachment_notice_save_failure_keeps_sent_and_retries_only_original_metadata() {
    let mut peer = historical_trial_peer();
    let (root, run) = ended_run(&peer);
    let (list, owner, revision, refs, custody, _) = attachment(&peer, "retry-notes.txt", "ordinary selected file\n");
    let ledger = peer.fixture.root.join("app-data/runtime/recovery.ledger.jsonl");
    let path = crate::recovery::database_path(&ledger);
    let saved = path.with_extension("attachment-saved-db");
    let original_index = peer.home.host.recovery_custody().snapshot()["historicalConversations"][0]["index"].clone();
    std::fs::rename(&path, &saved).unwrap();
    std::fs::create_dir(&path).unwrap();
    peer.set_mode("turn-id", "attachment-metadata-retry");
    let sent = submit_attachments_with_pending_notice(&list, &root, &peer.home.host, Ok(custody.clone()), &owner, revision, &refs, &peer.generation, "thread", None, "ordinary carrier", crate::recovery::ExplicitAppProjectContext::unknown(), None).unwrap();
    assert_eq!(sent["endNotice"]["state"], "sent once with the next ordinary turn");
    assert_eq!(sent["endNotice"]["turn"], "attachment-metadata-retry");
    assert_eq!(sent["endNotice"]["outcome"]["learningBoundary"]["persistence"], "memory-only");
    let old_generation = peer.generation.clone();
    let original_client = last_turn_start(&peer)["params"]["clientUserMessageId"].clone();
    let before = (peer.turn_starts(), peer.fixture.wr_files(), peer.fixture.rs_entries());
    peer.home.host.stop("invented child restart", "hold original attachment pointer").unwrap();
    peer.generation = peer.relaunch();
    std::fs::remove_dir(&path).unwrap();
    std::fs::rename(saved, &path).unwrap();
    root.lock().unwrap().runs[&run].lock().unwrap().retry_records().unwrap();
    assert_eq!((peer.turn_starts(), peer.fixture.wr_files(), peer.fixture.rs_entries()), before);
    assert!(send_with_pending_notice(&root, &peer.generation, "thread", "never resent").is_none());
    let row = peer.home.host.recovery_custody().snapshot()["historicalConversations"][0]["index"].clone();
    assert_eq!(row["lastLoadedGeneration"], original_index["lastLoadedGeneration"]);
    let pointers: Vec<Value> = row["tags"].as_array().unwrap().iter().filter(|tag| tag["owner"] == crate::workflow_learning_pointers::OWNER).map(|tag| crate::workflow_learning_pointers::decode(tag["value"].as_str().unwrap()).unwrap()).collect();
    let end = pointers.iter().find(|p| p["purpose"] == "run end notice").unwrap();
    assert_eq!(end["generation"], old_generation);
    assert_eq!(end["turn"], "attachment-metadata-retry");
    assert_eq!(end["run"], run);
    assert_eq!(end["client_user_message_id"], original_client);
    drop((root, list, custody));
    historical_trial_new_process(&mut peer);
    let fresh = Mutex::new(WorkflowRootSession::default());
    trial_flows::bring_back_with_homes(&fresh, &[peer.home.clone()], peer.project(), &peer.home, None, Some(&run), &peer.generation, "thread", false).unwrap();
    assert_eq!(peer.turn_starts(), before.0);
}
#[test]
fn historical_trial_explicit_target_generation_changed_while_source_is_read_refuses_prefill() {
    let source = historical_trial_peer();
    let target = Peer::with_class(crate::home_resources::HomeClass::ApiKey);
    let mut live = source.registered();
    let run = open_run(&source, &mut live, "thread");
    drop(live);
    source.set_mode("learning-read-mode", "slow");
    let before = source
        .wire()
        .iter()
        .filter(|frame| frame["method"] == "thread/turns/list")
        .count();
    let target_home = target.home.clone();
    let homes = vec![source.home.clone(), target_home.clone()];
    let root = Mutex::new(WorkflowRootSession::default());
    std::thread::scope(|scope| {
        let read = scope.spawn(|| {
            trial_flows::bring_back_with_homes(
                &root,
                &homes,
                source.project(),
                &target_home,
                None,
                Some(&run),
                &target.generation,
                "thread",
                false,
            )
        });
        historical_trial_wait_for_query(&source, before);
        target
            .home
            .host
            .stop(
                "invented explicit target changed",
                "source read continues independently",
            )
            .unwrap();
        let next = target.relaunch();
        assert_ne!(next, target.generation);
        let error = read.join().unwrap().unwrap_err();
        assert!(
            error.contains("target changed") || error.contains("stale"),
            "{error}"
        );
    });
    assert!(historical_trial_snapshot(&root)["pendingBringBacks"]
        .as_array()
        .unwrap()
        .is_empty());
}
#[test]
fn historical_trial_repeated_native_page_cursor_is_named_and_cannot_prefill() {
    let peer = historical_trial_peer();
    let mut live = peer.registered();
    let run = open_run(&peer, &mut live, "thread");
    drop(live);
    peer.set_mode("learning-turns-mode", "repeat");
    let root = Mutex::new(WorkflowRootSession::default());
    let error = trial_flows::bring_back_with_homes(
        &root,
        &[peer.home.clone()],
        peer.project(),
        &peer.home,
        None,
        Some(&run),
        &peer.generation,
        "thread",
        false,
    )
    .unwrap_err();
    assert!(error.contains("repeated a page cursor"), "{error}");
    assert!(historical_trial_snapshot(&root)["pendingBringBacks"]
        .as_array()
        .unwrap()
        .is_empty());
}
#[test]
fn historical_trial_delegated_child_uses_authoring_home_without_loading_child() {
    let peer = Peer::new();
    let mut root = trial_root(&peer);
    let trial = root
        .prepare_trial(
            "delegated",
            DRAFT,
            Some((&peer.generation, "thread")),
            Some(&peer.home),
            peer.project(),
        )
        .unwrap()["reference"]
        .as_str()
        .unwrap()
        .to_owned();
    let root = Mutex::new(root);
    trial_flows::send_trial(&root, &peer.home, &trial, &peer.generation, "thread", "").unwrap();
    root.lock()
        .unwrap()
        .link_trial_child(
            &trial,
            "child-1",
            true,
            &descendant_view(&peer, &["child-1"]),
        )
        .unwrap();
    assert!(!peer.home.host.snapshot()["threads"]
        .as_array()
        .unwrap()
        .iter()
        .any(|thread| thread["threadId"] == "child-1"));
    let sent = peer.turn_starts();
    let pending = trial_flows::bring_back_with_homes(
        &root,
        &[peer.home.clone()],
        peer.project(),
        &peer.home,
        Some(&trial),
        None,
        &peer.generation,
        "thread",
        false,
    )
    .unwrap();
    assert_eq!(pending["source"]["threadId"], "child-1");
    assert_eq!(peer.turn_starts(), sent);
    assert!(
        historical_trial_snapshot(&root)["pendingBringBacks"][0]["transcript"]
            .as_str()
            .unwrap()
            .contains("Done.")
    );
}
#[test]
fn historical_trial_recorded_source_history_can_be_read_without_loading_original_thread() {
    let mut source = historical_trial_peer();
    let target = Peer::with_class(crate::home_resources::HomeClass::ApiKey);
    let mut live = source.registered();
    let run = open_run(&source, &mut live, "thread");
    drop(live);
    source
        .home
        .host
        .stop(
            "invented App restart",
            "new source starts without loading conversations",
        )
        .unwrap();
    let cfg = source.home.host_config.as_ref().unwrap().clone();
    let host = Arc::new(crate::hosting::Host::new());
    host.configure_recovery(
        source
            .fixture
            .root
            .join("app-data/runtime/recovery.ledger.jsonl"),
    )
    .unwrap();
    host.start(&cfg, "source history only").unwrap();
    source.generation = host.snapshot()["generation"].clone();
    source.home = Arc::new(
        HomeSession::new(crate::home_resources::HomeClass::Account, host, Ok(cfg)).unwrap(),
    );
    assert!(source.home.host.snapshot()["threads"]
        .as_array()
        .unwrap()
        .is_empty());
    let target_home = target.home.clone();
    let root = Mutex::new(WorkflowRootSession::default());
    let homes = vec![source.home.clone(), target_home.clone()];
    let pending = trial_flows::bring_back_with_homes(
        &root,
        &homes,
        source.project(),
        &target_home,
        None,
        Some(&run),
        &target.generation,
        "thread",
        false,
    )
    .unwrap();
    assert_eq!(pending["source"]["generation"], source.generation);
    assert!(
        historical_trial_snapshot(&root)["pendingBringBacks"][0]["transcript"]
            .as_str()
            .unwrap()
            .contains("Invented historical native result")
    );
    assert!(
        source.home.host.snapshot()["threads"]
            .as_array()
            .unwrap()
            .is_empty(),
        "learning does not load or resume the source conversation"
    );
}
