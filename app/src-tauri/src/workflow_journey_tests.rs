//! J4 (APP-V4-GROUP-A-20261004): one maintained offline end-to-end journey.
//!
//! J1 (publication and supply check), J2 (compatibility) and J3 (lifecycle and
//! reopen) keep their own component tests. This file is the evidence for the
//! complete journey only: select a workflow, register it, prepare and send a
//! run, inspect what was supplied, end it, and reopen the work after the loss
//! of every in-memory session object, in one scenario.
//!
//! Every step goes through the production Root API that the App commands in
//! `lib.rs` call (`WorkflowRootSession`, `WorkflowRun`, `start_workflow_run`,
//! `send_with_pending_notice`, `send_conversation_text`). The Tauri command
//! bodies themselves take `tauri::State`/`AppHandle` and are not callable here;
//! each step names the command whose body it follows. Two test doubles are
//! used, both already used by the existing Root tests: the owned Python
//! app-server peer (a verbatim copy of the script in `runtime_session.rs`
//! `workflow_root_tests::Peer`, which is private to that module) and the A15
//! act-control double (`ConfirmedA15Event::synthetic_for_test`).
//!
//! Not established here: native supplier behaviour (the peer is a fixture),
//! any real model, the UI, a person's native A15 confirmation, or a real App
//! relaunch (process loss is simulated by stopping the supplier child and
//! dropping every in-memory session object in this test process).
#![cfg(unix)]

use super::*;
use std::path::{Path, PathBuf};
use std::sync::{Arc, Mutex};
use std::time::Duration;

const NAME: &str = crate::workflow_workspace::development_catalog::NAME;
const THREAD: &str = "thread";

/// Copy of the owned native-shaped app-server peer used by `runtime_session.rs`
/// `workflow_root_tests::Peer` (that type is private to its module). One change:
/// `clientUserMessageId` is read with `.get(...)`, so an ordinary text turn
/// (which carries none) is answered instead of ending the peer. It logs every
/// received frame to `wire.jsonl` and, at each `turn/start`, the WR record
/// files it can see to `turn-start-wr.jsonl`.
const PEER: &str = r#"#!/usr/bin/python3
import sys,json,os
if '--version' in sys.argv:
 print('codex-cli 0.160.0');sys.exit(0)
def emit(v):print(json.dumps(v),flush=True)
starts=[0]
def thread(tid='thread'):return {'id':tid,'cliVersion':'0.160.0','createdAt':1,'updatedAt':2,'cwd':os.getcwd(),'ephemeral':False,'modelProvider':'fixture-provider','preview':'own native-shaped fixture','projectId':None,'sessionId':'fixture-session','source':'appServer','status':{'type':'idle'},'turns':[],'agentRole':'TASK'}
def turn():return {'id':'turn','status':'failed','items':[],'error':None,'itemsView':'summary'}
text='';client=''
def mode(name):
 return open(name).read().strip() if os.path.exists(name) else ''
def wr():
 d='.chirality/records/workflow'
 return sorted(n for n in os.listdir(d) if n.endswith('.json') and not n.startswith('.')) if os.path.isdir(d) else []
for line in sys.stdin:
 f=json.loads(line)
 with open('wire.jsonl','a') as log:log.write(json.dumps(f)+'\n')
 method=f.get('method')
 if method=='initialize':result={'userAgent':'unqualified-workflow-root-fixture'}
 elif method=='thread/start':
  starts[0]+=1
  result={'thread':thread('thread' if starts[0]==1 else 'thread-%d'%starts[0]),'model':'fixture-model','modelProvider':'fixture-provider','cwd':os.getcwd(),'approvalPolicy':'on-request','approvalsReviewer':'user','sandbox':{'type':'readOnly'},'instructionSources':[]}
 elif method=='turn/start':
  # Publish-before-send witness: the WR records the peer can see when the turn arrives.
  with open('turn-start-wr.jsonl','a') as log:log.write(json.dumps(wr())+'\n')
  if mode('turn-mode')=='error':
   emit({'id':f['id'],'error':{'code':-32000,'message':'fixture refused turn/start'}});continue
  if mode('turn-mode')=='exit':
   sys.exit(0)
  text=f['params']['input'][0]['text'];client=f['params'].get('clientUserMessageId','');result={'turn':turn()}
 elif method=='thread/list':result={'data':[thread()]+[thread('thread-%d'%n) for n in range(2,starts[0]+1)],'nextCursor':None,'backwardsCursor':None}
 elif method=='thread/turns/list':result={'data':[turn()],'nextCursor':None}
 elif method=='thread/items/list':
  m=mode('items-mode');seen=text;cid=client
  if m=='error':
   emit({'id':f['id'],'error':{'code':-32000,'message':'fixture unreadable items'}});continue
  if m=='framing':seen=text.replace('[Chirality] Workflow run start:','[Chirality] Workflow run started:',1)
  if m=='differ':seen=text.replace('\n','\r\n')
  if m=='noclient':cid='other-client'
  message={'type':'userMessage','id':'message','clientId':cid,'content':[{'type':'text','text':seen}]}
  data=[] if m=='absent' else [{'turnId':'turn','item':message}]
  if m=='finished':data.append({'turnId':'turn','item':{'type':'agentMessage','id':'reply','text':'Done.\nWorkflow finished: project:coordinated-knowledge-work\nNext workflow: project:coordinated-knowledge-work'}})
  if m=='paged' and f['params'].get('cursor') is None:result={'data':[],'nextCursor':'page-2'}
  else:result={'data':data,'nextCursor':None}
 else:continue
 emit({'id':f['id'],'result':result})
"#;

/// The durable side of the journey: the explicit App project (the
/// `CHIRALITY_WORKSPACE` stand-in), the development holding copy, the peer
/// script, the Codex account/probe homes and the App user-data folder (which
/// keeps App-kept draft bases, WR §3). It outlives every simulated App process.
struct Disk {
    base: PathBuf,
    project: PathBuf,
    package: PathBuf,
    script: PathBuf,
    app_data: PathBuf,
}
impl Disk {
    fn new() -> Self {
        use std::os::unix::fs::PermissionsExt;
        let base = std::fs::canonicalize(std::env::temp_dir())
            .unwrap()
            .join(crate::util::opaque_id("workflow-journey-").unwrap());
        let project = base.join("project");
        let app_data = base.join("app-data");
        for dir in [&base, &project, &base.join("account"), &base.join("probe"), &app_data] {
            std::fs::create_dir(dir).unwrap();
        }
        let package = project.join(NAME);
        std::fs::create_dir(&package).unwrap();
        let catalog = crate::workflow_workspace::development_catalog::DevelopmentCatalog::load().unwrap();
        for (name, bytes) in catalog.select_embedded().snapshot().files() {
            std::fs::write(package.join(name), bytes).unwrap();
        }
        let script = base.join("owned-peer.py");
        std::fs::write(&script, PEER).unwrap();
        std::fs::set_permissions(&script, std::fs::Permissions::from_mode(0o700)).unwrap();
        Self { base, project, package, script, app_data }
    }
    /// Every frame the peer received, across all simulated processes, in order.
    fn wire(&self) -> Vec<Value> {
        std::fs::read_to_string(self.project.join("wire.jsonl"))
            .unwrap_or_default()
            .lines()
            .map(|l| serde_json::from_str(l).unwrap())
            .collect()
    }
    fn frames(&self, method: &str) -> Vec<Value> {
        self.wire().into_iter().filter(|f| f["method"] == method).collect()
    }
    /// WR record files the peer saw at each `turn/start`, in arrival order.
    fn wr_at_turn_start(&self) -> Vec<Vec<String>> {
        std::fs::read_to_string(self.project.join("turn-start-wr.jsonl"))
            .unwrap_or_default()
            .lines()
            .map(|l| serde_json::from_str(l).unwrap())
            .collect()
    }
    fn wr_dir(&self) -> PathBuf {
        self.project.join(".chirality/records/workflow")
    }
    fn wr_files(&self) -> Vec<String> {
        let mut v: Vec<String> = std::fs::read_dir(self.wr_dir())
            .map(|d| {
                d.filter_map(|e| e.ok())
                    .map(|e| e.file_name().to_string_lossy().into_owned())
                    .filter(|n| n.ends_with(".json") && !n.starts_with('.'))
                    .collect()
            })
            .unwrap_or_default();
        v.sort();
        v
    }
    /// The file name a WR reference is published under.
    fn wr_file(&self, reference: &str) -> String {
        format!("{}.json", reference.strip_prefix("wr-record:v1:").expect("WR reference form"))
    }
    /// Every RS entry in the project, complete (no read limits).
    fn rs(&self) -> Vec<Value> {
        let (entries, limits) = crate::storage::read_all(&self.project);
        assert!(limits.is_empty(), "RS record set incomplete: {limits:?}");
        entries
    }
    fn rs_for(&self, run: &str) -> Vec<Value> {
        self.rs().into_iter().filter(|e| e["runId"] == run).collect()
    }
}
/// `AppState.workflows` with lib.rs setup's wiring: the App user-data root.
fn root_session(disk: &Disk) -> Mutex<WorkflowRootSession> {
    let mut root = WorkflowRootSession::default();
    root.set_app_user_data(disk.app_data.clone());
    Mutex::new(root)
}
impl Drop for Disk {
    fn drop(&mut self) {
        let _ = std::fs::remove_dir_all(&self.base);
    }
}

/// One simulated App process: its own Host (and supplier child), its own home
/// session, its current generation and the conversation loaded in it.
struct Process {
    host: Arc<crate::hosting::Host>,
    home: Arc<HomeSession>,
    generation: Value,
}
impl Process {
    fn start(disk: &Disk, actor: &str) -> Self {
        let mut cfg = crate::hosting::HostConfig::new(
            disk.script.clone(),
            disk.base.join("account"),
            disk.base.join("probe"),
            disk.project.clone(),
        );
        cfg.allow_unverified_dev = true;
        cfg.wait_limit = Duration::from_secs(2);
        let host = Arc::new(crate::hosting::Host::new());
        host.start(&cfg, actor).unwrap();
        assert_eq!(host.snapshot()["supplierStanding"], "unverified-development");
        let generation = host.snapshot()["generation"].clone();
        host.thread_start_with_guidance(&cfg.cwd.to_string_lossy(), "fixture-model", "fixture-provider", "existing role unchanged")
            .unwrap();
        let home = Arc::new(HomeSession::new(crate::home_resources::HomeClass::Account, host.clone(), Ok(cfg)).unwrap());
        Self { host, home, generation }
    }
    /// The person selects the conversation in native History and loads its turns
    /// (required before a supply check reads native item pages).
    fn select_history(&self) {
        let list = {
            let mut receiver = self.home.history.lock().unwrap();
            receiver.reconcile(&self.host);
            receiver.history_mut().unwrap().list_threads(None, crate::native_history::Direction::Asc).unwrap()
        };
        self.receive(list);
        self.home.history.lock().unwrap().history_mut().unwrap().select(THREAD).unwrap();
        let turns = self
            .home
            .history
            .lock()
            .unwrap()
            .history_mut()
            .unwrap()
            .turns_page(None, crate::native_history::Direction::Asc)
            .unwrap();
        self.receive(turns);
    }
    fn receive(&self, query: crate::native_history::HistoryQuery) {
        let dispatch = self.host.history_dispatch(&query).unwrap();
        self.home.history.lock().unwrap().dispatched(dispatch.clone());
        self.host.history_wait(&dispatch, Duration::from_secs(2)).unwrap();
        self.home.history.lock().unwrap().reconcile(&self.host);
    }
    /// Process loss: the supplier child stops and this process's Host and home
    /// session are dropped. The caller has already dropped its Root session.
    fn lose(self) {
        let home = Arc::downgrade(&self.home);
        let host = Arc::downgrade(&self.host);
        self.host.stop_scoped(&self.generation, "journey fixture", "App process lost").unwrap();
        drop(self);
        assert!(home.upgrade().is_none(), "a dropped session object still holds the lost process's home");
        // The Host's own reader threads release their handles as the stopped child's
        // streams close; give them a bounded moment.
        let deadline = std::time::Instant::now() + Duration::from_secs(5);
        while host.upgrade().is_some() && std::time::Instant::now() < deadline {
            std::thread::sleep(Duration::from_millis(10));
        }
        assert!(host.upgrade().is_none(), "something still holds the lost process's Host");
    }
}
impl Drop for Process {
    fn drop(&mut self) {
        let _ = self.host.stop("journey fixture cleanup", "test ended");
    }
}

/// `conversation_send_text` command body (lib.rs): a pending end notice goes
/// first, exactly once; otherwise ordinary text is sent unchanged.
fn conversation_send_text(root: &Mutex<WorkflowRootSession>, process: &Process, text: &str) -> Result<Value, String> {
    if let Some(result) = send_with_pending_notice(root, &process.generation, THREAD, text) {
        return result;
    }
    send_conversation_text(&process.host.snapshot(), &process.generation, THREAD, text, |generation, thread, text| {
        process.home.host.turn_start_text(generation, thread, text)
    })
}

/// `workflow_reopen` command body (lib.rs), with the REC restart facts this
/// process holds.
fn workflow_reopen(root: &Mutex<WorkflowRootSession>, process: &Process, project: &Path) -> Value {
    let recovery = process.home.recovery_startup.lock().unwrap().snapshot();
    let events = crate::restart_events(&recovery);
    root.lock().unwrap().reopen(project, &events).unwrap()
}

/// Step 2: draft, review, hot A15 and the registration transaction, with
/// the act-control double used by
/// `workflow_root_closed_selection_real_review_hot_receipt_and_transaction`,
/// then selection of the hot registered revision. Requires the development
/// copy to be selected. Returns (review reference, registered revision).
fn register_and_select(
    root: &Mutex<WorkflowRootSession>,
    home: &Arc<HomeSession>,
    library: &Path,
    origin: &str,
    project: &Path,
    workspace_control: Arc<Mutex<Option<crate::act_control::ActControl>>>,
) -> (String, String) {
    let mut r = root.lock().unwrap();
    // workflow_open_library, workflow_create_draft, workflow_review.
    r.open_library(library.to_path_buf(), origin, Some(project), workspace_control).unwrap();
    let draft = r.create_selected_draft(NAME).unwrap();
    assert_eq!(draft["name"], NAME);
    r.begin_review(home.clone(), json!({"hostState":"fixture","identityVerified":false}), vec![NAME.into()], false)
        .unwrap();
    let (reference, revision) = capture_and_register(&mut r, library, origin);
    drop(r);
    (reference, revision)
}

/// `workflow_register_native` (through the act-control double), the ledger
/// checks and `workflow_select_registered` for the review `begin_review` just
/// opened. Returns (review reference, registered revision).
fn capture_and_register(r: &mut WorkflowRootSession, library: &Path, origin: &str) -> (String, String) {
    let reference = r.active_review.clone().unwrap();
    // workflow_register_native, through the act-control double.
    let revision = {
        let review = r.reviews[&reference].clone();
        let mut review = review.lock().unwrap();
        let library_ctx = review.library.clone();
        let offer = review.offer.as_ref().unwrap();
        let current = review.review.as_ref().unwrap().current().unwrap();
        let actor = crate::act_control::person(Some("synthetic native fixture"), Some("fixture OS"));
        let context = json!({"library":library_ctx.reference,"home":"explicit absent/unknown fixture source","identityVerified":false});
        let mut owner_guard = library_ctx.control.lock().unwrap();
        let owner = owner_guard.as_mut().unwrap();
        owner.a15_confirmation_text(offer, &current, &actor, &context).unwrap();
        owner.present_a15(offer).unwrap();
        let event = crate::a15_native::ConfirmedA15Event::synthetic_for_test(
            offer.id().into(),
            owner.frozen_a15_offer_digest(offer).unwrap().clone(),
            actor,
            context,
        );
        let result = owner.confirm_a15_after_native_event(offer, event, &current).unwrap();
        drop(current);
        drop(owner_guard);
        review.attempted_native = true;
        review.accept_result(result).unwrap();
        assert_eq!(review.status["entries"][0]["state"], "registered", "{}", review.status);
        // J5: only this act's own revision becomes a registered value; a disclosed prior is never promoted.
        assert_eq!(review.registered.len(), 1, "{:?}", review.registered.keys().collect::<Vec<_>>());
        review.registered.values().next().unwrap().identity().revision.clone()
    };
    // The library's registration ledger holds the registered line, bound to the A15 act.
    let ledger: Vec<Value> = std::fs::read_to_string(library.join(".chirality/workflow-registry.jsonl"))
        .unwrap()
        .lines()
        .map(|l| serde_json::from_str(l).unwrap())
        .collect();
    let line = ledger.last().unwrap();
    assert_eq!(line["outcome"], "registered");
    assert_eq!(line["identity"]["revision"], revision.as_str());
    assert_eq!(line["identity"]["origin"], origin);
    let (acts, limits) = crate::records::read_log(&crate::storage::library_log(library));
    assert!(limits.is_empty(), "{limits:?}");
    assert!(acts.iter().any(|e| e["recordId"] == line["act"]["record_id"]), "the ledger cites the recorded A15 act");
    // workflow_select_registered: the hot registered revision's published copy.
    let copy = library.join(".chirality/workflows").join(NAME);
    let snapshot = r.select_hot_registered_copy(&reference, &revision, copy).unwrap();
    assert_eq!(snapshot["selection"]["standing"], "registered revision");
    assert_eq!(snapshot["selection"]["runnable"], true);
    assert_eq!(snapshot["selection"]["identity"]["revision"], revision.as_str());
    assert_eq!(snapshot["selection"]["identity"]["origin"], origin);
    (reference, revision)
}

/// J4 finding 1 (J5): after process loss the person registers the same workflow
/// again in the SAME library, through a new genuine A15 on the hot draft route
/// (WR RB-6, DS-2). The draft from the earlier process is kept (D-1: the App
/// never overwrites it) and refined, because identical content is DS-4. The
/// prior ledger line and the App-kept base are disclosed observations, frozen at
/// review and checked under the ledger lock; they never select the old revision.
fn refine_register_and_select(
    root: &Mutex<WorkflowRootSession>,
    home: &Arc<HomeSession>,
    library: &Path,
    origin: &str,
    project: &Path,
    workspace_control: Arc<Mutex<Option<crate::act_control::ActControl>>>,
    previous: &str,
    refinement: &str,
) -> (String, String) {
    let mut r = root.lock().unwrap();
    r.open_library(library.to_path_buf(), origin, Some(project), workspace_control).unwrap();
    let context = json!({"hostState":"fixture","identityVerified":false});
    // The published copy has registration history: in place is not offered (WR ME-1 / LS-2 only).
    let in_place = r.begin_review(home.clone(), context.clone(), vec![NAME.into()], true);
    assert!(in_place.as_ref().is_err_and(|e| e.contains("registration history")), "{in_place:?}");
    // D-1: the kept draft is never overwritten by an App action.
    assert!(r.create_selected_draft(NAME).is_err_and(|e| e.contains("no overwrite")));
    // The person refines the kept draft (J-8), then reviews it.
    let workflow = library.join(".chirality/workflow-drafts").join(NAME).join("WORKFLOW.md");
    let mut text = std::fs::read_to_string(&workflow).unwrap();
    text.push_str(refinement);
    std::fs::write(&workflow, text).unwrap();
    r.begin_review(home.clone(), context, vec![NAME.into()], false)
        .expect("same-library review after relaunch: DS-2 from the App-kept base");
    let reference = r.active_review.clone().unwrap();
    let presentation = r.reviews[&reference].lock().unwrap().status["presentation"].clone();
    let entry = &presentation["entries"][0];
    assert_eq!(entry["disposition"], "new revision", "{entry}");
    assert_eq!(entry["prior_revision"]["revision"], previous, "the prior is the slot's latest ledger line");
    assert_eq!(entry["base"]["revision"], previous, "the App-kept base survived the process loss");
    assert!(entry.to_string().contains("no earlier native-act authentication"), "{entry}");
    let (reference, revision) = capture_and_register(&mut r, library, origin);
    assert_ne!(revision, previous);
    let ledger: Vec<Value> = std::fs::read_to_string(library.join(".chirality/workflow-registry.jsonl"))
        .unwrap()
        .lines()
        .map(|l| serde_json::from_str(l).unwrap())
        .collect();
    let line = ledger.last().unwrap();
    assert_eq!(line["disposition"], "new revision");
    assert_eq!(line["prior_revision"]["revision"], previous, "the new act names the disclosed prior");
    assert_eq!(line["identity"]["derived_from"]["revision"], previous, "derived from the App-kept base");
    // The disclosed prior is not promoted: the old revision is not selectable, even through the new review.
    let copy = library.join(".chirality/workflows").join(NAME);
    assert!(r.select_hot_registered_copy(&reference, previous, copy.clone()).is_err(), "old revision stays cold");
    r.select_hot_registered_copy(&reference, &revision, copy).unwrap();
    (reference, revision)
}

fn text_identity(text: &str) -> Value {
    crate::role_supply::content(text.as_bytes())
}
fn kinds(entries: &[Value]) -> Vec<&str> {
    entries.iter().map(|e| e["kind"].as_str().unwrap()).collect()
}
/// RS run-log order: strictly increasing `seq`, non-decreasing `observedAt`.
fn assert_log_order(entries: &[Value]) {
    for pair in entries.windows(2) {
        assert!(pair[0]["seq"].as_u64().unwrap() < pair[1]["seq"].as_u64().unwrap(), "seq order: {pair:?}");
        assert!(
            pair[0]["observedAt"].as_str().unwrap() <= pair[1]["observedAt"].as_str().unwrap(),
            "observation order: {pair:?}"
        );
    }
}

#[test]
fn journey_select_register_run_check_end_and_reopen_after_process_loss() {
    let disk = Disk::new();
    let project = disk.project.clone();

    // ---- Step 1. Open a project and a library; select the development copy; it cannot be run.
    let one = Process::start(&disk, "journey process 1");
    let generation_one = one.generation.clone();
    let act = Arc::new(Mutex::new(Some(crate::act_control::ActControl::new(&project)))); // AppState.act
    let root = root_session(&disk); // AppState.workflows
    {
        let mut r = root.lock().unwrap();
        r.open_library(project.clone(), "project", Some(&project), act.clone()).unwrap();
        let selected = r.select_development_copy(disk.package.clone()).unwrap();
        assert_eq!(selected["selection"]["standing"], crate::workflow_workspace::development_catalog::STANDING);
        assert_eq!(selected["selection"]["runnable"], false);
        // workflow_prepare_run on a development selection (TT-1/TX-1, CI-18).
        let refused = r.prepare_run(one.home.clone(), &one.generation, THREAD, "person".into(), Some(&project));
        assert!(refused.as_ref().is_err_and(|e| e.contains("TT-1") && e.contains("TX-1")), "{refused:?}");
        assert!(r.runs.is_empty());
    }
    assert!(disk.frames("turn/start").is_empty(), "nothing sent");
    assert!(disk.wr_files().is_empty(), "nothing recorded");
    assert!(disk.rs().iter().all(|e| e.get("runId").is_none()), "no run log");

    // ---- Step 2. Draft, review, hot A15 and transaction; select the hot registered revision.
    let (review_one, revision_one) = register_and_select(&root, &one.home, &project, "project", &project, act.clone());

    // ---- Step 3. Prepare a run: CK-1 is advisory, no R14, nothing published or sent yet.
    let person = "person exact\r\ntext";
    let a = root.lock().unwrap().prepare_run(one.home.clone(), &one.generation, THREAD, person.into(), Some(&project)).unwrap();
    let run_a = root.lock().unwrap().runs[&a].clone();
    let (selection_ref, text_ref) = {
        let run = run_a.lock().unwrap();
        assert_eq!(run.lifecycle, RunLifecycle::Prepared);
        assert!(!run.attempted);
        let view = run.view(&a);
        let compatibility = view["compatibility"].as_array().unwrap();
        assert_eq!(compatibility.len(), 1, "{}", view["compatibility"]);
        assert_eq!(compatibility[0]["occasionLabel"], "CK-1 selection");
        assert_eq!(compatibility[0]["advisory"], true);
        assert_eq!(compatibility[0]["publication"]["state"], "not published");
        assert!(compatibility[0]["r14"].as_str().unwrap().contains("no R14 written"));
        (
            view["publication"]["selection"].as_str().unwrap().to_owned(),
            view["publication"]["runText"].as_str().unwrap().to_owned(),
        )
    };
    {
        let records = crate::workflow_workspace::publication::ProjectRecords::open(&project).unwrap();
        // Reserved identities only: neither resolves before send (the WR store does not exist yet).
        assert!(records.resolve(&selection_ref).is_err() && records.resolve(&text_ref).is_err());
        assert!(!disk.wr_dir().exists());
    }
    assert!(disk.wr_files().is_empty() && disk.frames("turn/start").is_empty(), "preparing records and sends nothing");
    assert!(disk.rs().iter().all(|e| e["kind"] != "compatibility_report_ref"), "no R14");

    // ---- Step 4. Send through the owned peer (workflow_send_run): records durable at turn/start; CK-2; run_opened.
    let sent = start_workflow_run(&root, &a).unwrap();
    assert_eq!(sent["observedStatus"], "failed", "the peer reports a failed native turn");
    let starts = disk.frames("turn/start");
    assert_eq!(starts.len(), 1);
    let records = crate::workflow_workspace::publication::ProjectRecords::open(&project).unwrap();
    let selection = records.resolve(&selection_ref).unwrap();
    let run_text = records.resolve(&text_ref).unwrap();
    let client_id = {
        let run = run_a.lock().unwrap();
        assert_eq!(starts[0]["params"], run.prepared().turn_params(person, &run.client_id).unwrap(), "exact wire frame");
        assert_eq!(run.lifecycle, RunLifecycle::Open, "a failed native turn does not end the run");
        assert_eq!(run.turn_id.as_deref(), Some("turn"));
        let occasions: Vec<Value> = run.view(&a)["compatibility"].as_array().unwrap().iter().map(|c| c["occasionLabel"].clone()).collect();
        assert_eq!(occasions, [json!("CK-1 selection"), json!("CK-2 run start")]);
        for c in run.view(&a)["compatibility"].as_array().unwrap() {
            assert_eq!(c["advisory"], true);
            assert_eq!(c["publication"]["state"], "not published");
        }
        run.client_id.clone()
    };
    let wire_text = starts[0]["params"]["input"][0]["text"].as_str().unwrap();
    assert_eq!(text_identity(wire_text), run_text.body()["text_identity"], "sent bytes are the published run_text");
    assert_eq!(starts[0]["params"]["input"][1]["text"], person);
    assert_eq!(starts[0]["params"]["threadId"], THREAD);
    let mut published_pair = vec![disk.wr_file(&selection_ref), disk.wr_file(&text_ref)];
    published_pair.sort();
    assert_eq!(disk.wr_at_turn_start(), vec![published_pair.clone()], "selection and run_text durable at turn/start, nothing else");
    assert_eq!(run_text.envelope()["basis_records"], json!([selection_ref]));
    assert_eq!(selection.body()["standing"], "registered");
    assert_eq!(selection.body()["identity"]["revision"], revision_one.as_str());
    assert_eq!(selection.body()["conversation"], THREAD);
    assert_eq!(run_text.body()["run"], a.as_str());
    let log = disk.rs_for(&a);
    assert_eq!(kinds(&log), ["run_opened"]);
    let opened = &log[0];
    assert_eq!(opened["body"]["runId"], a.as_str());
    assert_eq!(opened["body"]["conversationRef"], THREAD);
    assert_eq!(opened["body"]["startedBy"], json!({"kind":"person"}));
    assert_eq!(opened["body"]["workflow"]["name"], NAME);
    assert_eq!(opened["body"]["workflow"]["revision"], revision_one.as_str());
    assert_eq!(opened["body"]["workflow"]["origin"], "project");
    assert!(opened["body"].get("follows").is_none(), "first run in the conversation follows nothing");
    assert!(opened["observedAt"].as_str().unwrap() >= run_text.envelope()["observed_at"].as_str().unwrap());
    assert!(disk.rs().iter().all(|e| e["kind"] != "compatibility_report_ref"), "no R14 after CK-2");

    // ---- Step 5. Check supply against native pages (workflow_check_supply); reread once.
    // The peer's native history also holds an agent reply reporting the workflow
    // finished; that report has no lifecycle effect (FN-3).
    std::fs::write(project.join("items-mode"), "finished").unwrap();
    one.select_history();
    let first = run_a.lock().unwrap().check_native_supply().unwrap()["check"].clone();
    assert_eq!(first["state"], "verified");
    assert_eq!(first["published"], true);
    assert_eq!(first["r3"]["state"], "recorded");
    let first_ref = first["reference"].as_str().unwrap().to_owned();
    let first_record = records.resolve(&first_ref).unwrap();
    let first_bytes = first_record.bytes().to_vec();
    assert_eq!(first_record.body()["record_kind"], "supply_check");
    assert_eq!(first_record.body()["state"], "verified");
    assert_eq!(first_record.body()["turn"], "turn");
    assert_eq!(first_record.body()["client_user_message_id"], client_id.as_str());
    assert_eq!(first_record.envelope()["basis_records"], json!([text_ref]), "the check cites the run text");
    assert_eq!(first_record.envelope()["observed_at"], first_record.body()["read_at"]);
    assert!(!first_record.envelope()["source_references"].as_array().unwrap().is_empty(), "native source receipts");
    let r3_first = disk.rs().into_iter().find(|e| e["recordId"] == first["r3"]["recordId"]).unwrap();
    assert_eq!(r3_first["kind"], "supplied_guidance");
    assert_eq!(r3_first["runId"], a.as_str());
    assert_eq!(r3_first["body"]["supplyRecord"]["ref"], text_ref.as_str(), "R3 cites the run text");
    assert_eq!(r3_first["body"]["supplyCheckRecord"]["ref"], first_ref.as_str(), "R3 cites the check");
    assert_eq!(r3_first["body"]["supplyCheck"], "verified");
    assert_eq!(r3_first["body"]["adoption"], "unknown");
    assert_eq!(r3_first["body"]["nativeTurn"], "turn");
    assert_eq!(r3_first["body"]["thread"], THREAD);
    assert_eq!(r3_first["observedAt"], first_record.body()["read_at"]);
    let second = run_a.lock().unwrap().check_native_supply().unwrap()["check"].clone();
    let second_ref = second["reference"].as_str().unwrap().to_owned();
    assert_ne!(second_ref, first_ref, "a reread is a new check record");
    let second_record = records.resolve(&second_ref).unwrap();
    assert_ne!(second_record.body()["check"], first_record.body()["check"], "a reread is a new check identity");
    assert_eq!(second_record.envelope()["basis_records"], json!([text_ref]));
    assert_eq!(records.resolve(&first_ref).unwrap().bytes(), first_bytes.as_slice(), "the first check is unchanged");
    assert_eq!(disk.wr_files().len(), 4);
    assert_eq!(disk.frames("thread/items/list").len(), 2, "one native read per check");
    assert_eq!(disk.frames("turn/start").len(), 1, "checks never send");
    assert_eq!(run_a.lock().unwrap().lifecycle, RunLifecycle::Open, "a reported finish ends nothing");
    let log = disk.rs_for(&a);
    assert_eq!(kinds(&log), ["run_opened", "supplied_guidance", "supplied_guidance"]);
    assert_eq!(log[1]["body"]["supplyCheckRecord"]["ref"], first_ref.as_str());
    assert_eq!(log[2]["body"]["supplyCheckRecord"]["ref"], second_ref.as_str());
    assert_log_order(&log);

    // ---- Step 6. End explicitly (workflow_end_run); the next ordinary turn carries the notice once.
    run_a.lock().unwrap().end_run(false, None).unwrap();
    assert_eq!(run_a.lock().unwrap().lifecycle, RunLifecycle::Ended);
    let log = disk.rs_for(&a);
    assert_eq!(kinds(&log), ["run_opened", "supplied_guidance", "supplied_guidance", "run_ended"]);
    assert_eq!(log[3]["body"], json!({"stoppedBy":"the person","cause":"ended by the person","waitingArrivals":[]}));
    assert_log_order(&log);
    conversation_send_text(&root, &one, "hello").unwrap();
    let starts = disk.frames("turn/start");
    assert_eq!(starts.len(), 2);
    let notice_file = {
        let mut now = disk.wr_files();
        now.retain(|f| ![disk.wr_file(&selection_ref), disk.wr_file(&text_ref), disk.wr_file(&first_ref), disk.wr_file(&second_ref)].contains(f));
        assert_eq!(now.len(), 1, "exactly one new WR record: the end notice");
        now.remove(0)
    };
    let notice_ref = format!("wr-record:v1:{}", notice_file.strip_suffix(".json").unwrap());
    let notice = records.resolve(&notice_ref).unwrap();
    assert_eq!(notice.body()["purpose"], "run end notice");
    assert_eq!(notice.body()["run"], a.as_str());
    assert_eq!(notice.envelope()["basis_records"], json!([text_ref]));
    assert_eq!(disk.wr_at_turn_start()[1].contains(&notice_file), true, "notice record durable at its turn/start");
    let notice_text = starts[1]["params"]["input"][0]["text"].as_str().unwrap().to_owned();
    assert_eq!(notice_text, notice.body()["lines"]["end_line"].as_str().unwrap(), "the turn carries the published notice text");
    assert_eq!(text_identity(&notice_text), notice.body()["text_identity"]);
    assert!(notice_text.contains(&a));
    assert_eq!(starts[1]["params"]["input"][1]["text"], "hello");
    assert_eq!(starts[1]["params"]["input"].as_array().unwrap().len(), 2);
    conversation_send_text(&root, &one, "later").unwrap();
    let starts = disk.frames("turn/start");
    assert_eq!(starts.len(), 3);
    assert_eq!(starts[2]["params"]["threadId"], THREAD);
    let later = starts[2]["params"]["input"].as_array().unwrap();
    assert_eq!(later.len(), 1, "a later ordinary turn carries no notice: {later:?}");
    assert_eq!(later[0]["text"], "later");
    let carrying = disk
        .wire()
        .iter()
        .filter(|f| f["params"]["input"].as_array().is_some_and(|input| input.iter().any(|i| i["text"] == notice_text.as_str())))
        .count();
    assert_eq!(carrying, 1, "exactly one frame carries the end notice");
    assert_eq!(disk.wr_files().len(), 5);
    assert_eq!(disk.rs_for(&a).len(), 4, "ordinary turns write nothing to the run log");

    // ---- Step 7. Reopen after loss of every in-memory session object.
    let log_before = disk.rs_for(&a);
    let wr_before: Vec<(String, Vec<u8>)> =
        disk.wr_files().into_iter().map(|f| (f.clone(), std::fs::read(disk.wr_dir().join(&f)).unwrap())).collect();
    drop((selection, run_text, first_record, second_record, notice, records));
    drop(run_a);
    drop(root);
    drop(act);
    one.lose();
    // The App-kept draft base survives in the App data folder (WR §3): one
    // draft_reference, recorded by the App, naming the registered revision (G-6).
    let base_records: Vec<PathBuf> = std::fs::read_dir(disk.app_data.join(crate::workflow_workspace::registration::BASE_STORE))
        .unwrap()
        .filter_map(|e| e.ok())
        .filter(|e| !e.file_name().to_string_lossy().starts_with('.'))
        .map(|e| e.path())
        .collect();
    assert_eq!(base_records.len(), 1, "{base_records:?}");
    let base_record: Value = serde_json::from_slice(&std::fs::read(&base_records[0]).unwrap()).unwrap();
    assert_eq!(base_record["record_kind"], "draft_reference");
    assert_eq!(base_record["base_recorded_by"], "app");
    assert_eq!(base_record["base"]["revision"], revision_one.as_str());
    assert_eq!(base_record["state"], "registered, unchanged since");

    let two = Process::start(&disk, "journey process 2 (after loss)");
    assert_ne!(two.generation, generation_one, "a new process generation");
    assert_eq!(two.generation["home"], generation_one["home"], "the same Codex home");
    let root = root_session(&disk);
    let records = crate::workflow_workspace::publication::ProjectRecords::open(&project).unwrap();
    let reopened = workflow_reopen(&root, &two, &project);
    assert_eq!(reopened["limits"], json!([]), "{reopened}");
    let reading = crate::records::supply::read_project_runs(&records, &[]);
    assert!(reading.limits.is_empty(), "{:?}", reading.limits);
    assert_eq!(reading.runs.len(), 1);
    let ra = &reading.runs[0];
    assert_eq!(ra.run, a);
    assert_eq!(
        ra.lifecycle,
        crate::records::supply::RecordedLifecycle::Ended { stopped_by: "the person".into(), cause: "ended by the person".into() },
        "the run reads ended, with its cause"
    );
    assert_eq!(ra.conversation.as_deref(), Some(THREAD));
    assert_eq!(ra.workflow["revision"], revision_one.as_str());
    assert_eq!(reopened["runs"][0]["run"], a.as_str());
    assert_eq!(reopened["runs"][0]["detail"], json!({"stoppedBy":"the person","cause":"ended by the person"}));
    // Every published record resolves, byte for byte, in its recorded order.
    let mut references = records.list_references().unwrap();
    references.sort();
    let mut expected = vec![selection_ref.clone(), text_ref.clone(), first_ref.clone(), second_ref.clone(), notice_ref.clone()];
    expected.sort();
    assert_eq!(references, expected);
    for (file, bytes) in &wr_before {
        let reference = format!("wr-record:v1:{}", file.strip_suffix(".json").unwrap());
        assert_eq!(records.resolve(&reference).unwrap().bytes(), bytes.as_slice(), "{reference} resolves unchanged");
    }
    let chain = [&selection_ref, &text_ref, &first_ref, &second_ref, &notice_ref];
    let at: Vec<String> =
        chain.iter().map(|r| records.resolve(r).unwrap().envelope()["observed_at"].as_str().unwrap().to_owned()).collect();
    assert!(at.windows(2).all(|w| w[0] <= w[1]), "selection, run text, checks, notice in observation order: {at:?}");
    assert_eq!(records.resolve(&text_ref).unwrap().envelope()["basis_records"], json!([selection_ref]));
    for r in [&first_ref, &second_ref, &notice_ref] {
        assert_eq!(records.resolve(r).unwrap().envelope()["basis_records"], json!([text_ref]));
    }
    let supply = crate::records::supply::read_project_supply(&records);
    let supply_records = supply["records"].as_array().unwrap();
    assert_eq!(supply_records.len(), 5);
    assert!(supply_records.iter().all(|r| r["resolution"] == "resolved"), "{supply}");
    for check in [&first_ref, &second_ref] {
        let view = supply_records.iter().find(|r| r["reference"] == check.as_str()).unwrap();
        assert_eq!(view["r3"][0]["standing"], "HistoricalCorrespondence", "{view}");
    }
    let log_after = disk.rs_for(&a);
    assert_eq!(log_after, log_before, "the run log is read back unchanged");
    assert_log_order(&log_after);
    // Nothing is inferred as completed from the native turn status ("failed" at send).
    assert!(disk.rs().iter().all(|e| !(e["kind"] == "run_ended" && e["body"]["cause"] == "completed")));
    // No live run exists: none in the record, none in the fresh process, no hot authority recreated.
    assert!(reading.possibly_live_in(THREAD).is_empty());
    assert!(root.lock().unwrap().snapshot()["runs"].as_array().unwrap().is_empty());
    assert!(
        root.lock().unwrap().select_hot_registered_copy(&review_one, &revision_one, project.join(".chirality/workflows").join(NAME)).is_err(),
        "the lost process's hot registration is not recreated from files"
    );
    // A new start in that conversation is allowed because the run ended. The fresh
    // process has no hot registration, so the person registers again in the SAME
    // library (a refinement of the kept draft, new genuine A15) and selects that
    // registered revision (J4 finding 1).
    let act = Arc::new(Mutex::new(Some(crate::act_control::ActControl::new(&project))));
    root.lock().unwrap().select_development_copy(disk.package.clone()).unwrap();
    let (review_two, revision_two) = refine_register_and_select(
        &root,
        &two.home,
        &project,
        "project",
        &project,
        act.clone(),
        &revision_one,
        "\nRefined after relaunch (journey step 7).\n",
    );
    assert!(
        root.lock().unwrap().select_hot_registered_copy(&review_one, &revision_one, project.join(".chirality/workflows").join(NAME)).is_err(),
        "re-registration does not recreate the lost process's registration"
    );
    // The selection is the new revision; re-select it after the negative check.
    root.lock().unwrap().select_hot_registered_copy(&review_two, &revision_two, project.join(".chirality/workflows").join(NAME)).unwrap();
    let b = root
        .lock()
        .unwrap()
        .prepare_run(two.home.clone(), &two.generation, THREAD, "second run".into(), Some(&project))
        .expect("a new start is allowed: the recorded run ended");

    // ---- Step 8. A second run left open; reopen reads it open and interrupted; it blocks a new start.
    start_workflow_run(&root, &b).unwrap();
    let starts = disk.frames("turn/start");
    assert_eq!(starts.len(), 4);
    let (b_selection, b_text) = {
        let run = root.lock().unwrap().runs[&b].clone();
        let run = run.lock().unwrap();
        assert_eq!(run.lifecycle, RunLifecycle::Open);
        assert_eq!(starts[3]["params"], run.prepared().turn_params("second run", &run.client_id).unwrap());
        let view = run.view(&b);
        (view["publication"]["selection"].as_str().unwrap().to_owned(), view["publication"]["runText"].as_str().unwrap().to_owned())
    };
    let seen = disk.wr_at_turn_start();
    assert_eq!(seen.len(), 4);
    assert!(seen[3].contains(&disk.wr_file(&b_selection)) && seen[3].contains(&disk.wr_file(&b_text)), "B's records durable at its turn/start");
    let b_log = disk.rs_for(&b);
    assert_eq!(kinds(&b_log), ["run_opened"]);
    assert_eq!(b_log[0]["body"]["workflow"]["revision"], revision_two.as_str());
    // Was "user" (library-2); the re-registration is now in the same project library.
    assert_eq!(b_log[0]["body"]["workflow"]["origin"], "project");
    assert_eq!(b_log[0]["body"]["conversationRef"], THREAD);
    let b_follows = b_log[0]["body"].get("follows").cloned();
    let wr_count = disk.wr_files().len();
    drop(records);
    drop(root);
    drop(act);
    two.lose();

    let three = Process::start(&disk, "journey process 3 (after loss)");
    let root = root_session(&disk);
    let records = crate::workflow_workspace::publication::ProjectRecords::open(&project).unwrap();
    let reopened = workflow_reopen(&root, &three, &project);
    let reading = crate::records::supply::read_project_runs(&records, &[]);
    assert!(reading.limits.is_empty(), "{:?}", reading.limits);
    let state = |run: &str| reading.runs.iter().find(|r| r.run == run).unwrap().clone();
    assert_eq!(state(&b).lifecycle, crate::records::supply::RecordedLifecycle::OpenInterrupted, "open; interrupted");
    assert_eq!(state(&b).conversation.as_deref(), Some(THREAD));
    assert!(matches!(state(&a).lifecycle, crate::records::supply::RecordedLifecycle::Ended { .. }), "A stays ended");
    let b_view = reopened["runs"].as_array().unwrap().iter().find(|r| r["run"] == b.as_str()).unwrap().clone();
    assert_eq!(b_view["state"], "open; interrupted (no run_ended recorded)");
    assert_eq!(disk.rs_for(&b).len(), 1, "the native turn status ('failed') ended nothing");
    assert_eq!(reading.possibly_live_in(THREAD).iter().map(|r| r.run.as_str()).collect::<Vec<_>>(), [b.as_str()]);
    assert!(root.lock().unwrap().snapshot()["runs"].as_array().unwrap().is_empty(), "no live process run is recreated");
    let act = Arc::new(Mutex::new(Some(crate::act_control::ActControl::new(&project))));
    root.lock().unwrap().select_development_copy(disk.package.clone()).unwrap();
    // Step 8 re-registration also stays in the same library: a second refinement.
    refine_register_and_select(
        &root,
        &three.home,
        &project,
        "project",
        &project,
        act.clone(),
        &revision_two,
        "\nRefined again after the second relaunch (journey step 8).\n",
    );
    let (turns, wr) = (disk.frames("turn/start").len(), disk.wr_files().len());
    assert_eq!(wr, wr_count);
    let blocked = root.lock().unwrap().prepare_run(three.home.clone(), &three.generation, THREAD, "third".into(), Some(&project));
    assert!(blocked.as_ref().is_err_and(|e| e.contains(&b)), "the interrupted run blocks a new start: {blocked:?}");
    assert!(root.lock().unwrap().runs.is_empty());
    assert_eq!((disk.frames("turn/start").len(), disk.wr_files().len()), (turns, wr), "nothing prepared, recorded or sent");
    // workflow_end_recorded: the person's plain end of the interrupted run.
    let ended = root.lock().unwrap().end_recorded_run(&project, &b, THREAD, false).unwrap();
    assert_eq!(ended["cause"], "ended by the person");
    let b_log = disk.rs_for(&b);
    assert_eq!(kinds(&b_log), ["run_opened", "run_ended"]);
    assert_eq!(b_log[1]["body"], json!({"stoppedBy":"the person","cause":"ended by the person","waitingArrivals":[]}));
    assert_log_order(&b_log);
    let reading = crate::records::supply::read_project_runs(&records, &[]);
    assert!(reading.possibly_live_in(THREAD).is_empty());
    root.lock()
        .unwrap()
        .prepare_run(three.home.clone(), &three.generation, THREAD, "third".into(), Some(&project))
        .expect("after the person's end a new start is allowed");
    assert_eq!(disk.frames("turn/start").len(), turns, "preparing sends nothing");
    // Recorded observation (not a contract assertion): a successor prepared in a fresh
    // process after the predecessor ended carries no `follows` (the chain is hot-only).
    assert_eq!(b_follows, None);
    drop(records);
    drop(root);
    drop(three);
}
