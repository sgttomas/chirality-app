//! "Continue as ‹role›", "Fork" and the guidance-changed flag through the real
//! Host against an owned app-server peer, plus the pure handoff/limit rules.
//! The peer is a fixture: it establishes no supplier behaviour.
use super::*;
use crate::hosting::{Host, HostConfig};
use crate::role_lifecycle::RoleInForce;
use crate::role_supply::Role;
use crate::runtime_session::HomeSession;
use std::path::PathBuf;
use std::sync::Arc;
use std::time::{Duration, Instant};

/// thread/start answers `thread`, `thread-2`…; thread/fork answers `fork-N`
/// forked from the source; turn/start answers `turn-N`, then reports the turn
/// started, one completed agent message (text from `summary.txt`) and the
/// turn ended with the status in `turn-status` (default `completed`).
const PEER: &str = r#"#!/usr/bin/python3
import sys,json,os,threading
if '--version' in sys.argv:
 print('codex-cli 0.160.0');sys.exit(0)
lock=threading.Lock()
def emit(v):
 with lock: print(json.dumps(v),flush=True)
def thread(i,extra=None):
 t={'id':i,'cliVersion':'0.160.0','createdAt':1,'updatedAt':2,'cwd':os.getcwd(),'ephemeral':False,'modelProvider':'fixture-provider','preview':'roles fixture','projectId':None,'sessionId':'fixture-session','source':'appServer','status':{'type':'idle'},'turns':[]}
 if extra: t.update(extra)
 return t
def settled(t):
 return {'thread':t,'model':'fixture-model','modelProvider':'fixture-provider','cwd':os.getcwd(),'approvalPolicy':'on-request','approvalsReviewer':'user','sandbox':{'type':'readOnly'},'instructionSources':[]}
n={'start':0,'fork':0,'turn':0}
for line in sys.stdin:
 f=json.loads(line)
 with open('wire.jsonl','a') as log: log.write(json.dumps(f)+'\n')
 m=f.get('method')
 if m=='initialize': emit({'id':f['id'],'result':{'userAgent':'unqualified-roles-fixture'}});continue
 if m=='thread/start':
  n['start']+=1;emit({'id':f['id'],'result':settled(thread('thread' if n['start']==1 else 'thread-%d'%n['start']))});continue
 if m=='thread/fork':
  n['fork']+=1;mode=open('fork-mode').read().strip() if os.path.exists('fork-mode') else 'new'
  src=f['params']['threadId']
  t=thread(src,{'forkedFromId':src}) if mode=='same' else thread('fork-%d'%n['fork'],{'forkedFromId':'elsewhere' if mode=='unrelated' else src})
  emit({'id':f['id'],'result':settled(t)});continue
 if m=='turn/start':
  n['turn']+=1;tid='turn-%d'%n['turn'];th=f['params']['threadId']
  emit({'id':f['id'],'result':{'turn':{'id':tid,'status':'inProgress','items':[],'error':None}}})
  emit({'method':'turn/started','params':{'threadId':th,'turn':{'id':tid,'status':'inProgress','items':[],'error':None,'itemsView':'summary'}}})
  status=open('turn-status').read().strip() if os.path.exists('turn-status') else 'completed'
  if status=='completed':
   text=open('summary.txt').read() if os.path.exists('summary.txt') else 'Summary from the source agent.'
   emit({'method':'item/completed','params':{'threadId':th,'turnId':tid,'completedAtMs':1,'item':{'id':'msg-'+tid,'type':'agentMessage','text':text}}})
  emit({'method':'turn/completed','params':{'threadId':th,'turn':{'id':tid,'status':status,'items':[],'error':None,'itemsView':'summary'}}})
  continue
"#;

struct Fixture {
    root: PathBuf,
    instructions: PathBuf,
    home: Arc<HomeSession>,
    generation: Value,
}
impl Fixture {
    fn new() -> Self {
        use std::os::unix::fs::PermissionsExt;
        let root = std::fs::canonicalize(std::env::temp_dir()).unwrap().join(crate::util::opaque_id("conversation-roles-").unwrap());
        for name in ["account", "probe"] {
            std::fs::create_dir_all(root.join(name)).unwrap();
        }
        let instructions = root.join("instructions");
        crate::runtime_session::seed_instructions(&instructions).unwrap();
        let peer = root.join("peer.py");
        std::fs::write(&peer, PEER).unwrap();
        std::fs::set_permissions(&peer, std::fs::Permissions::from_mode(0o700)).unwrap();
        let mut cfg = HostConfig::new(peer, root.join("account"), root.join("probe"), root.clone());
        cfg.allow_unverified_dev = true;
        cfg.wait_limit = Duration::from_secs(2);
        let host = Arc::new(Host::new());
        host.start(&cfg, "roles fixture").unwrap();
        let generation = host.snapshot()["generation"].clone();
        let home = Arc::new(HomeSession::new(crate::home_resources::HomeClass::Account, host, Ok(cfg)).unwrap());
        Self { root, instructions, home, generation }
    }
    fn home_name(&self) -> String {
        self.generation["home"].as_str().unwrap().to_owned()
    }
    /// The App's own start path (lib.rs `thread_start`): compose, dispatch,
    /// bind from the actual request and correlated response.
    fn start(&self, role: Option<Role>, continued_from: Option<Value>) -> String {
        let composition = crate::runtime_session::compose_role(&self.instructions, role).unwrap();
        let receipt = self.home.host.thread_start_with_guidance_dispatch(&self.generation, &self.root.to_string_lossy(), "fixture-model", "fixture-provider", &composition.text).unwrap();
        self.home.history.lock().unwrap().start_dispatched_continuing(receipt.clone(), &composition, &crate::util::opaque_id("sup:").unwrap(), continued_from).unwrap();
        let evidence = self.home.host.source_request_wait(&receipt, Duration::from_secs(5)).unwrap();
        self.home.history.lock().unwrap().reconcile(&self.home.host);
        assert!(self.home.history.lock().unwrap().start_admitted(&receipt), "{evidence}");
        evidence["response"]["result"]["thread"]["id"].as_str().unwrap().to_owned()
    }
    fn role(&self, thread: &str) -> Value {
        self.home.history.lock().unwrap().role(&self.home_name(), thread)
    }
    fn evidence(&self, thread: &str) -> Value {
        self.home.history.lock().unwrap().binding(&self.home_name(), thread).map(|b| b.evidence()).unwrap_or(Value::Null)
    }
    fn details(&self, thread: &str) -> Value {
        self.home.history.lock().unwrap().role_details(&self.home_name(), thread, Some(&self.instructions))
    }
    fn role_in_force(&self, thread: &str) -> RoleInForce {
        let home = self.home_name();
        self.home.history.lock().unwrap().binding(&home, thread).map(|b| b.role_in_force(&home, thread))
            .unwrap_or(RoleInForce::Unknown { reason: "not bound".into() })
    }
    /// What host_status hands the view: the Host snapshot plus received native items.
    fn status(&self) -> Value {
        let mut runtime = self.home.runtime.lock().unwrap();
        let (generation, position) = runtime.cursor();
        let observation = self.home.host.observe(&generation.clone(), position);
        let received = runtime.receive(&observation);
        let mut s = observation["snapshot"].clone();
        for (k, v) in received.as_object().unwrap() {
            s[k] = v.clone();
        }
        s
    }
    fn wire(&self) -> Vec<Value> {
        std::fs::read_to_string(self.root.join("wire.jsonl")).unwrap_or_default().lines().map(|l| serde_json::from_str(l).unwrap()).collect()
    }
    fn until(&self, what: &str, done: impl Fn(&Value) -> bool) -> Value {
        let deadline = Instant::now() + Duration::from_secs(5);
        loop {
            let s = self.status();
            if done(&s) {
                return s;
            }
            assert!(Instant::now() < deadline, "{what} not observed");
            std::thread::sleep(Duration::from_millis(10));
        }
    }
}
impl Drop for Fixture {
    fn drop(&mut self) {
        let _ = self.home.host.stop("roles fixture cleanup", "test ended");
        let _ = std::fs::remove_dir_all(&self.root);
    }
}

#[test]
fn fork_is_a_same_role_copy_and_leaves_the_source_unchanged() {
    let f = Fixture::new();
    let source = f.start(Some(Role::WORKING_ITEMS), None);
    let (role_before, evidence_before) = (f.role(&source), f.evidence(&source));
    assert_eq!(role_before["role"], "WORKING_ITEMS");
    let out = fork_conversation(&f.home, &f.generation, &source, Duration::from_secs(5)).unwrap();
    let sent = f.wire().into_iter().find(|frame| frame["method"] == "thread/fork").expect("thread/fork written");
    assert_eq!(sent["params"], json!({"threadId":source,"deferGoalContinuation":true}),
        "the thread id and no instructions, model or settings; no automatic goal continuation turn");
    // The exact params are valid 0.160.0 ThreadForkParams.
    let mut schema: Value = serde_json::from_str(include_str!("../resources/supplier/0.160.0/codex_app_server_protocol.schemas.json")).unwrap();
    schema["$ref"] = json!("#/definitions/v2/ThreadForkParams");
    jsonschema::options().with_draft(jsonschema::Draft::Draft7).offline().build(&schema).unwrap().validate(&sent["params"]).unwrap();
    assert!(crate::role_supply::check_role_inputs("thread/fork", &sent["params"]).is_ok(), "carries no role input");
    let fork = out["thread"]["threadId"].as_str().unwrap().to_owned();
    assert_eq!(fork, "fork-1");
    assert_eq!(out["thread"]["forkedFrom"]["threadId"], source);
    assert!(f.home.host.snapshot()["threads"].as_array().unwrap().iter().any(|t| t["threadId"] == "fork-1"), "fork admitted operationally");
    // The fork inherits the source's role and original guidance bytes.
    assert_eq!(f.role(&fork)["role"], "WORKING_ITEMS");
    assert_ne!(f.role(&fork)["supply_ref"], role_before["supply_ref"], "the fork has its own record");
    assert_eq!(f.evidence(&fork)["binding"]["original"], evidence_before["binding"]["original"]);
    let relation = &f.details(&fork)["roleRelation"];
    assert_eq!(relation["kind"], "inherited-fork");
    assert_eq!(relation["sourceThread"], source);
    assert_eq!(relation["forkedFromId"], source);
    // The source conversation's role and record are exactly as they were.
    assert_eq!(f.role(&source), role_before);
    assert_eq!(f.evidence(&source), evidence_before);
    assert_eq!(f.details(&source)["roleRelation"]["kind"], "start");
}

#[test]
fn fork_refuses_an_unknown_conversation_and_keeps_an_unbound_role_unknown() {
    let f = Fixture::new();
    assert!(fork_conversation(&f.home, &f.generation, "no-such-thread", Duration::from_secs(1)).unwrap_err().contains("refused-not-sent"));
    assert!(f.wire().iter().all(|frame| frame["method"] != "thread/fork"), "nothing written for a refused fork");
    // A conversation started outside the App's binding (no original supply) forks with its role unknown.
    f.home.host.thread_start_selected(&f.root.to_string_lossy(), "fixture-model", "fixture-provider").unwrap();
    let out = fork_conversation(&f.home, &f.generation, "thread", Duration::from_secs(5)).unwrap();
    assert_eq!(out["role"]["role"]["standing"], "unknown");
    assert_eq!(f.role("fork-1")["standing"], "unknown", "no role is invented for the fork");
    // A result that is not a new thread forked from the source admits nothing.
    for mode in ["same", "unrelated"] {
        std::fs::write(f.root.join("fork-mode"), mode).unwrap();
        let threads = f.home.host.snapshot()["threads"].as_array().unwrap().len();
        assert!(fork_conversation(&f.home, &f.generation, "thread", Duration::from_secs(5)).unwrap_err().contains("nothing admitted"), "{mode}");
        assert_eq!(f.home.host.snapshot()["threads"].as_array().unwrap().len(), threads, "{mode}: no thread admitted");
    }
}

#[test]
fn continue_as_drafts_from_a_visible_source_turn_and_starts_a_new_conversation() {
    let f = Fixture::new();
    std::fs::write(f.root.join("summary.txt"), "The person asked for X. No workflow run. No attachments.").unwrap();
    let source = f.start(Some(Role::HELP_HUMAN), None);
    let (role_before, evidence_before) = (f.role(&source), f.evidence(&source));
    let mut handoffs = Handoffs::default();
    let host = Arc::clone(&f.home.host);
    let generation = f.generation.clone();
    let begun = handoffs.begin(&f.generation, &source, f.role_in_force(&source), Some(Role::WORKING_ITEMS), |text| {
        crate::runtime_session::send_conversation_text(&host.snapshot(), &generation, "thread", text, |g, t, x| host.turn_start_text(g, t, x))
    }).unwrap();
    assert_eq!(begun["request"]["state"], "sent");
    // CA-2: a visible ordinary turn of the source conversation, nothing else.
    let turn = f.wire().into_iter().find(|frame| frame["method"] == "turn/start").unwrap();
    assert_eq!(turn["params"]["threadId"], source);
    assert_eq!(turn["params"]["input"][0]["text"], handoff_request_text(Some(Role::WORKING_ITEMS)));
    assert!(turn["params"].get("collaborationMode").is_none() && turn["params"].get("developerInstructions").is_none());
    let s = f.until("drafted summary", |s| handoffs.view(s)[0]["draft"]["state"] == "drafted");
    let view = &handoffs.view(&s)[0];
    assert_eq!(view["header"], format!("Handoff from conversation {source} (role HELP_HUMAN)."));
    assert_eq!(view["draftText"], format!("Handoff from conversation {source} (role HELP_HUMAN).\n\nThe person asked for X. No workflow run. No attachments."));
    assert!(view["started"].is_null(), "nothing is started or sent to a new conversation yet");
    assert_eq!(f.wire().iter().filter(|frame| frame["method"] == "thread/start").count(), 1);
    // The new conversation: the chosen role's own composition with the CA-3 relation.
    assert!(handoffs.continuation(view["id"].as_str().unwrap(), &f.generation, Some(Role::HELPS_HUMANS)).is_err(), "the role chosen at Continue as is the one started");
    let relation = handoffs.continuation(view["id"].as_str().unwrap(), &f.generation, Some(Role::WORKING_ITEMS)).unwrap();
    assert_eq!(relation["sourceThread"], source);
    assert_eq!(relation["sourceStartRecord"], role_before["supply_ref"]);
    let new = f.start(Some(Role::WORKING_ITEMS), Some(relation.clone()));
    handoffs.started(view["id"].as_str().unwrap(), &new, &f.generation);
    assert_ne!(new, source);
    assert_eq!(f.role(&new)["role"], "WORKING_ITEMS");
    let starts: Vec<Value> = f.wire().into_iter().filter(|frame| frame["method"] == "thread/start").collect();
    assert!(starts[1]["params"]["developerInstructions"].as_str().unwrap().contains("# Active role: WORKING_ITEMS"));
    assert!(!starts[1]["params"]["developerInstructions"].as_str().unwrap().contains("The person asked for X"), "the summary is not supplied guidance");
    assert_eq!(f.details(&new)["roleRelation"], json!({"kind":"continued-from","from":relation}));
    assert!(f.wire().iter().filter(|frame| frame["method"] == "turn/start").all(|frame| frame["params"]["threadId"] == source), "nothing sent to the new conversation");
    // The source conversation keeps its role and record (L-2).
    assert_eq!(f.role(&source), role_before);
    assert_eq!(f.evidence(&source), evidence_before);
    assert!(handoffs.continuation(view["id"].as_str().unwrap(), &f.generation, Some(Role::WORKING_ITEMS)).is_err(), "one start per handoff");
}

#[test]
fn continue_as_falls_back_to_the_header_when_the_source_turn_fails() {
    let f = Fixture::new();
    std::fs::write(f.root.join("turn-status"), "failed").unwrap();
    let source = f.start(None, None);
    let mut handoffs = Handoffs::default();
    let host = Arc::clone(&f.home.host);
    let generation = f.generation.clone();
    handoffs.begin(&f.generation, &source, f.role_in_force(&source), None, |text| {
        crate::runtime_session::send_conversation_text(&host.snapshot(), &generation, "thread", text, |g, t, x| host.turn_start_text(g, t, x))
    }).unwrap();
    let s = f.until("failed turn", |s| handoffs.view(s)[0]["draft"]["state"] == "header-only");
    let view = &handoffs.view(&s)[0];
    assert_eq!(view["draftText"], format!("Handoff from conversation {source} (no role)."));
    assert!(view["draft"]["reading"].as_str().unwrap().contains("ended failed"));
    // A request written whose outcome failed is also header only, never retried.
    let mut written = Handoffs::default();
    let calls = std::cell::Cell::new(0);
    let out = written.begin(&f.generation, "other", RoleInForce::Unknown { reason: "r".into() }, None, |_| { calls.set(calls.get() + 1); Err("no response to turn/start within the wait limit (outcome stays pending/unknown)".into()) }).unwrap();
    assert_eq!((out["request"]["state"].as_str(), calls.get()), (Some("failed"), 1));
    assert_eq!(written.view(&json!({}))[0]["draftText"], "Handoff from conversation other (role not established in this App process).");
    // A request refused before any write asked nothing: no handoff stays open, and trying again is possible.
    let mut refused = Handoffs::default();
    for reason in ["refused-not-sent(not-ready): state stopping", "refused-not-sent: Stop Codex was confirmed for this Codex process; no turn/start is sent", "conversation is not loaded in this home generation"] {
        let error = refused.begin(&f.generation, "other", RoleInForce::Unknown { reason: "r".into() }, None, |_| Err(reason.into())).unwrap_err();
        assert!(error.contains("No summary was requested") && error.contains(reason), "{error}");
        assert_eq!(refused.view(&json!({})), json!([]), "{reason}: no handoff left open");
    }
    // A written request's later error that only mentions those words keeps the header-only fallback.
    let out = refused.begin(&f.generation, "other", RoleInForce::Unknown { reason: "r".into() }, None, |_| Err("turn/start native error: {\"message\":\"upstream said refused-not-sent\"}".into())).unwrap();
    assert_eq!(out["request"]["state"], "failed");
    assert_eq!(refused.view(&json!({})).as_array().unwrap().len(), 1, "the handoff stays open with the header only");
}

/// WR TX-5 / NIR TC-2: when the summary request carried a pending run-end
/// notice, its outcome reaches `Handoffs::sent` in the same shape: the turn
/// Codex named, or, when no frame was written, a `refused-not-sent` refusal
/// that closes the handoff (the notice stays pending for the next turn). A
/// written request that failed keeps the header-only fallback.
#[test]
fn continue_as_request_carrying_the_end_notice_keeps_the_handoff_rules() {
    use crate::runtime_session::NoticeSend;
    let sent = notice_turn_outcome(NoticeSend { result: Ok(json!({"state":"end notice and the person's text sent once","turnId":"turn-9","endNotice":{"state":"sent once with the next ordinary turn"}})), written: true });
    let mut handoffs = Handoffs::default();
    let generation = json!({"appSession":"s","home":"h","spawnCounter":1});
    let out = handoffs.begin(&generation, "src", RoleInForce::Unknown { reason: "r".into() }, None, |_| sent.clone()).unwrap();
    assert_eq!((out["request"]["state"].as_str(), out["request"]["turnId"].as_str()), (Some("sent"), Some("turn-9")));
    let unwritten = notice_turn_outcome(NoticeSend { result: Err("End notice not durably recorded; nothing sent: disk full".into()), written: false });
    let mut closed = Handoffs::default();
    let error = closed.begin(&generation, "src", RoleInForce::Unknown { reason: "r".into() }, None, |_| unwritten.clone()).unwrap_err();
    assert!(error.contains("No summary was requested") && error.contains("disk full"), "{error}");
    assert_eq!(closed.view(&json!({})), json!([]), "nothing written: no handoff left open");
    let failed = notice_turn_outcome(NoticeSend { result: Err("End notice turn outcome unavailable; not resent".into()), written: true });
    let mut kept = Handoffs::default();
    let out = kept.begin(&generation, "src", RoleInForce::Unknown { reason: "r".into() }, None, |_| failed.clone()).unwrap();
    assert_eq!(out["request"]["state"], "failed", "a written request is never treated as unsent");
}

#[test]
fn continue_as_glue_checks_the_source_before_opening_anything() {
    let f = Fixture::new();
    let source = f.start(Some(Role::HELP_HUMAN), None);
    let handoffs = std::sync::Mutex::new(Handoffs::default());
    let workflows = std::sync::Mutex::new(crate::runtime_session::WorkflowRootSession::default());
    let starts = || f.wire().iter().filter(|frame| frame["method"] == "turn/start").count();
    // A stale or foreign conversation is refused before any handoff is opened or frame written.
    for thread in ["no-such-thread", ""] {
        let error = continue_as_begin(&handoffs, &workflows, &f.home, &f.generation, thread, None).unwrap_err();
        assert!(error.contains("nothing sent"), "{error}");
    }
    let mut stale = f.generation.clone();
    stale["spawnCounter"] = json!(99);
    assert!(continue_as_begin(&handoffs, &workflows, &f.home, &stale, &source, None).unwrap_err().contains("stale"));
    assert_eq!((handoffs.lock().unwrap().view(&json!({})), starts()), (json!([]), 0));
    // The real path: one visible turn in the source conversation.
    let out = continue_as_begin(&handoffs, &workflows, &f.home, &f.generation, &source, Some(Role::WORKING_ITEMS)).unwrap();
    assert_eq!((out["request"]["state"].as_str(), starts()), (Some("sent"), 1));
    let id = out["id"].as_str().unwrap().to_owned();
    // thread_start(continue_as): a role or home differing from the handoff refuses before anything is sent.
    assert!(continuation_for_start(&handoffs, &f.home, Some(&id), Some(Role::HELPS_HUMANS)).unwrap_err().contains("differs"));
    assert_eq!(continuation_for_start(&handoffs, &f.home, None, Some(Role::HELPS_HUMANS)).unwrap(), None);
    let other = Fixture::new();
    assert!(continuation_for_start(&handoffs, &other.home, Some(&id), Some(Role::WORKING_ITEMS)).unwrap_err().contains("home"));
    let relation = continuation_for_start(&handoffs, &f.home, Some(&id), Some(Role::WORKING_ITEMS)).unwrap().unwrap();
    // Only an admitted start marks the handoff started.
    mark_started(&handoffs, Some(&id), &Err("start-failed-or-unknown".into()), &f.generation);
    assert!(handoffs.lock().unwrap().view(&json!({}))[0]["started"].is_null());
    let new = f.start(Some(Role::WORKING_ITEMS), Some(relation));
    mark_started(&handoffs, Some(&id), &Ok(json!({"result":{"thread":{"id":new}}})), &f.generation);
    assert_eq!(handoffs.lock().unwrap().view(&json!({}))[0]["started"]["threadId"], new);
    assert!(continuation_for_start(&handoffs, &f.home, Some(&id), Some(Role::WORKING_ITEMS)).unwrap_err().contains("already started"));
}

#[test]
fn fork_command_routes_to_the_owning_home_only() {
    let f = Fixture::new();
    let source = f.start(None, None);
    let homes = std::sync::Mutex::new(crate::runtime_session::HomeRouter::new(Arc::clone(&f.home)).unwrap());
    let mut foreign = f.generation.clone();
    foreign["home"] = json!("another-home");
    assert!(fork_command(&homes, &foreign, &source, Duration::from_secs(1)).is_err());
    assert!(f.wire().iter().all(|frame| frame["method"] != "thread/fork"), "no fork written for a foreign generation");
    let out = fork_command(&homes, &f.generation, &source, Duration::from_secs(5)).unwrap();
    assert_eq!(out["thread"]["forkedFrom"]["threadId"], source);
    assert_eq!(f.role(out["thread"]["threadId"].as_str().unwrap())["role"], Value::Null, "the fork keeps the source's no-role binding");
    assert_eq!(f.role(out["thread"]["threadId"].as_str().unwrap())["standing"], "app-observed");
}

#[test]
fn continue_as_choices_are_checked_before_anything_is_sent() {
    let g = json!({"appSession":"s","home":"h","spawnCounter":1});
    let mut handoffs = Handoffs::default();
    let never = |_: &str| -> Result<Value, String> { panic!("nothing may be sent") };
    assert!(handoffs.begin(&g, "t", RoleInForce::Unknown { reason: "r".into() }, Some(Role::TASK), never).unwrap_err().contains("not a conversation role"));
    assert!(handoffs.begin(&json!("h"), "t", RoleInForce::Unknown { reason: "r".into() }, None, never).is_err());
    handoffs.begin(&g, "t", RoleInForce::Unknown { reason: "r".into() }, None, |_| Ok(json!({"result":{"turn":{"id":"u"}}}))).unwrap();
    assert!(handoffs.begin(&g, "t", RoleInForce::Unknown { reason: "r".into() }, None, never).unwrap_err().contains("already open"));
    let id = handoffs.view(&json!({}))[0]["id"].as_str().unwrap().to_owned();
    let other_home = json!({"appSession":"s","home":"k","spawnCounter":1});
    assert!(handoffs.continuation(&id, &other_home, None).is_err());
    let relation = handoffs.continuation(&id, &g, None).unwrap();
    assert_eq!(relation["sourceStartRecord"]["standing"], "unknown", "an unknown source record is said, never invented");
    handoffs.dismiss(&id).unwrap();
    assert!(handoffs.continuation(&id, &g, None).is_err() && handoffs.dismiss(&id).is_err());
}

#[test]
fn guidance_changed_flag_fires_only_on_an_actual_change() {
    let f = Fixture::new();
    let thread = f.start(Some(Role::HELPS_HUMANS), None);
    let role_file = f.instructions.join("agents/AGENT_HELPS_HUMANS.md");
    let original = std::fs::read(&role_file).unwrap();
    let flagged = |f: &Fixture| -> Vec<Value> { f.details(&thread)["futureGuidanceNotices"].as_array().unwrap().clone() };
    assert!(flagged(&f).is_empty(), "no change, no flag");
    // An unrelated role's file changing is not this conversation's guidance.
    std::fs::write(f.instructions.join("agents/AGENT_TASK.md"), b"edited TASK").unwrap();
    assert!(flagged(&f).is_empty());
    // Rewriting the same bytes is not a change.
    std::fs::write(&role_file, &original).unwrap();
    assert!(flagged(&f).is_empty());
    std::fs::write(&role_file, b"edited role guidance").unwrap();
    let notices = flagged(&f);
    assert_eq!(notices.len(), 1);
    assert_eq!((notices[0]["path"].as_str(), notices[0]["kind"].as_str()), (Some("agents/AGENT_HELPS_HUMANS.md"), Some("changed")));
    assert_eq!(notices[0]["currentConversationRoleChanged"], false);
    assert_eq!(f.role(&thread)["role"], "HELPS_HUMANS", "the flag changes nothing in the conversation");
    // Restored to the original bytes: no flag.
    std::fs::write(&role_file, &original).unwrap();
    assert!(flagged(&f).is_empty());
    std::fs::remove_file(f.instructions.join("AGENTS.md")).unwrap();
    let notices = flagged(&f);
    assert_eq!((notices.len(), notices[0]["kind"].as_str()), (1, Some("missing")));
    // A store that cannot be read is no change: the comparison is reported as not made.
    let unread = f.home.history.lock().unwrap().role_details(&f.home_name(), &thread, None)["futureGuidanceNotices"].clone();
    assert!(unread.as_array().unwrap().iter().all(|n| n["kind"] == "not-read"), "{unread}");
}

#[test]
fn limit_account_is_handed_in_its_schema_and_task_is_stated_not_enforced() {
    let root = std::fs::canonicalize(std::env::temp_dir()).unwrap().join(crate::util::opaque_id("limits-").unwrap());
    crate::runtime_session::seed_instructions(&root).unwrap();
    let schema: Value = serde_json::from_str(include_str!("../resources/workflow_role/role-limit-account.schema.json")).unwrap();
    let validator = jsonschema::options().with_draft(jsonschema::Draft::Draft202012).offline().build(&schema).unwrap();
    let out = limit_account(Some(&root));
    validator.validate(&out["account"]).unwrap();
    let task = out["account"]["roles"].as_array().unwrap().iter().find(|r| r["role"] == "TASK").unwrap().clone();
    assert_eq!(task["delegation"], "does-not-delegate");
    assert_eq!(task["limits"][0]["limitId"], "L-TASK-1");
    assert_eq!(task["limits"][0]["presentedAs"], "Stated, not enforced");
    assert!(task["limits"][0]["notEnforcement"].as_array().unwrap().contains(&json!("depth-limit")));
    std::fs::write(root.join("agents/AGENT_TASK.md"), b"modified TASK guidance").unwrap();
    let out = limit_account(Some(&root));
    validator.validate(&out["account"]).unwrap();
    let task = out["account"]["roles"].as_array().unwrap().iter().find(|r| r["role"] == "TASK").unwrap().clone();
    assert_eq!((task["guidanceState"].as_str(), task["limits"][0]["standing"].as_str()), (Some("modified"), Some("unknown")));
    std::fs::remove_file(root.join("agents/AGENT_HELP_HUMAN.md")).unwrap();
    let out = limit_account(Some(&root));
    assert_eq!(out["notRead"][0]["role"], "HELP_HUMAN", "a role not read is reported, never guessed");
    assert_eq!(limit_account(None)["notRead"].as_array().unwrap().len(), 4);
    std::fs::remove_dir_all(root).unwrap();
}
