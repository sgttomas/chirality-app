//! Invented local fixtures. The spawn frames are the supplier's own, recorded
//! at the pipe (supplier_checks/recordings/nv04.recording.json) and received
//! through the App's native view; they show what the recorder writes from
//! such frames, not that a supplier's child ran on a candidate.
use super::super::{published_at, Scope};
use super::*;
use std::path::PathBuf;
use std::sync::Arc;

const RECORDING: &str = include_str!("../../supplier_checks/recordings/nv04.recording.json");
const BRIEF: &str = include_str!("../../tests/fixtures/FX-FL1/briefs/W1.json");
/// `shasum -a 256` of the recorded spawn prompt's bytes.
const PROMPT_SHA256: &str = "08aa0f0fa681b447f6149da457dd11ed0543452bff50e01ce38f51dc0d78d3f7";

struct Fixture {
    root: PathBuf,
    project: PathBuf,
    scope: Scope,
}
impl Fixture {
    fn new() -> Self {
        let root = std::env::temp_dir().canonicalize().unwrap().join(crate::util::opaque_id("native-delegation-records-").unwrap());
        let project = root.join("project");
        std::fs::create_dir_all(&project).unwrap();
        crate::records_store::use_store_for_test(Some(Ok(crate::records_store::Store {
            root: root.join("store"),
            placement: crate::records_store::Placement::Test,
            limits: vec![],
        })));
        crate::records_store::attach(&project, true).unwrap();
        let scope = Scope::capture(&project).unwrap();
        Self { root, project, scope }
    }
    fn context(&self, generation: &Value) -> SourceContext {
        SourceContext {
            scope: Ok(self.scope.clone()),
            native_home: Ok(json!({"homeId":generation["home"],"root":crate::attachments::native_path_identity(&self.project),"physical":{"device":1,"inode":1}})),
            generation: generation.clone(),
            custody_limit: None,
            activity: crate::records_retention::activity(&self.scope.project.path).unwrap().map(Arc::new),
        }
    }
    fn observe(&self, session: &mut Session, views: &[Value], cause: Option<&'static str>) {
        session.observe_delegation_views(Some(&self.project), views, &mut |generation| self.context(generation), &|_| cause);
    }
    fn lines(&self, phase: usize) -> Vec<String> {
        std::fs::read_to_string(published_at(&self.scope, phase)).unwrap_or_default().lines().map(str::to_owned).collect()
    }
    /// The store's rows, having checked that the project's log holds the identical lines.
    fn rows(&self) -> Vec<Value> {
        assert_eq!(self.lines(0), self.lines(1), "the store and the project's log hold the identical lines");
        self.lines(0).iter().map(|line| serde_json::from_str(line).unwrap()).collect()
    }
    fn of(&self, kind: &str) -> Vec<Value> {
        self.rows().into_iter().filter(|row| row["kind"] == kind).collect()
    }
    fn brief(&self, name: &str) -> String {
        let path = self.project.join(FLEET).join("briefs").join(name);
        std::fs::create_dir_all(path.parent().unwrap()).unwrap();
        std::fs::write(&path, BRIEF).unwrap();
        crate::util::sha256_hex(BRIEF.as_bytes())
    }
}
impl Drop for Fixture {
    fn drop(&mut self) {
        crate::records_store::use_store_for_test(None);
        let _ = std::fs::remove_dir_all(&self.root);
    }
}
fn generation(session: &str) -> Value {
    json!({"appSession":session,"home":"invented-home","spawnCounter":1})
}
struct Spawn {
    view: crate::native_items::NativeView,
    parent: String,
    child: String,
    prompt: String,
}
/// The recorded supplier frames of one spawn, received live by the native
/// view of `generation`. `prompt` replaces the recorded prompt when given
/// (`Some(None)` removes it, as the supplier's type allows).
fn spawn(generation: &Value, prompt: Option<Option<&str>>) -> Spawn {
    let recording: Value = serde_json::from_str(RECORDING).unwrap();
    let mut view = crate::native_items::NativeView::new("invented-home".into()).unwrap();
    view.ready(generation.clone(), json!("invented version"), Value::Null).unwrap();
    let mut completed = Value::Null;
    let mut position = 0;
    for row in recording["frames"].as_array().unwrap() {
        let mut frame = row["frame"].clone();
        if !matches!(frame["method"].as_str(), Some("item/started" | "item/completed")) {
            continue;
        }
        if frame["params"]["item"]["type"] == "collabAgentToolCall" {
            if let Some(prompt) = prompt {
                frame["params"]["item"]["prompt"] = json!(prompt);
            }
            if frame["method"] == "item/completed" {
                completed = frame["params"]["item"].clone();
            }
        }
        position += 1;
        view.consume(&json!({"generation":generation,"position":position,"frame":frame})).unwrap();
    }
    Spawn {
        view,
        parent: completed["senderThreadId"].as_str().unwrap().into(),
        child: completed["receiverThreadIds"][0].as_str().unwrap().into(),
        prompt: completed["prompt"].as_str().unwrap_or_default().into(),
    }
}
/// The view as the record tick hands it over: with the conversations the
/// host started in that generation and the folder each runs in.
fn handed(spawn: &Spawn, generation: &Value, folder: &Path) -> Value {
    let mut view = spawn.view.snapshot();
    view["hostThreads"] = json!([{"generation":generation,"threadId":spawn.parent,"cwd":folder}]);
    view
}

#[test]
fn a_spawn_received_live_is_recorded_once_with_the_identities_codex_reported() {
    let f = Fixture::new();
    let g = generation("first");
    let s = spawn(&g, None);
    let view = handed(&s, &g, &f.project);
    let mut session = Session::default();
    f.observe(&mut session, &[view.clone()], None);
    let dispatches = f.of("dispatch_observed");
    assert_eq!(dispatches.len(), 1);
    let body = &dispatches[0]["body"];
    assert_eq!(body["parent"], json!({"threadId":s.parent,"generation":g}));
    assert_eq!(body["child"], json!({"threadId":s.child,"generation":g}));
    assert_eq!(body["spawnItem"]["itemId"], "call_spawn_1");
    assert_eq!(body["spawnItem"]["threadId"], s.parent.as_str());
    // The prompt's identity, against a SHA-256 of the recorded frame's prompt computed outside the product; its text is nowhere in the files.
    assert_eq!(s.prompt, "st5-child-brief-marker: count the invented files.");
    assert_eq!(body["spawnPrompt"], json!({"state":"supplied","bytes":49,
        "content":{"method":"chirality.app.exact-bytes.sha256/v1","value":PROMPT_SHA256}}));
    assert!(f.lines(0).iter().chain(f.lines(1).iter()).all(|line| !line.contains(&s.prompt)));
    assert_eq!(body["association"], json!({"state":"no brief reference"}));
    // The status is the supplier's value, unchanged, from the same item.
    let statuses = f.of("child_observed");
    assert_eq!(statuses.len(), 1);
    assert_eq!(statuses[0]["body"]["status"], "pendingInit");
    assert_eq!(statuses[0]["body"]["child"]["threadId"], s.child.as_str());
    assert!(f.of("observation_ended").is_empty(), "an observed child is not an ended one");
    // Later ticks hand over the same view; nothing is written twice.
    f.observe(&mut session, &[view.clone()], None);
    session.retry(Some(&f.project));
    assert_eq!(f.rows().len(), 2);
    assert!(!session.has_pending());
    // Read back by the fleet reader, they are the App's observations.
    let packet = crate::read_fleet_records_for_workspace(Some(&f.project)).unwrap();
    let read = packet["coordination"]["nativeDelegation"].as_array().unwrap();
    assert_eq!(read.len(), 2);
    assert_eq!(read[0]["record"], dispatches[0]);
    assert!(read.iter().all(|row| row["protectedOrder"].is_u64()));
    assert!(packet["coordination"]["recordingEvents"].as_array().unwrap().is_empty());
}

#[test]
fn a_spawn_outside_the_selected_project_or_read_from_history_is_not_recorded() {
    let f = Fixture::new();
    let g = generation("first");
    let s = spawn(&g, None);
    let elsewhere = f.root.join("elsewhere");
    std::fs::create_dir_all(&elsewhere).unwrap();
    let mut session = Session::default();
    f.observe(&mut session, &[handed(&s, &g, &elsewhere)], None);
    let mut unknown = s.view.snapshot();
    unknown["hostThreads"] = json!([]);
    f.observe(&mut Session::default(), &[unknown], None);
    assert!(f.lines(0).is_empty() && f.lines(1).is_empty());
    assert!(session.snapshot()["limits"][0].as_str().unwrap().contains("not the selected project"));
    // The same completed spawn item, read from Codex history, is not a live receipt.
    let mut view = crate::native_items::NativeView::new("invented-home".into()).unwrap();
    view.ready(g.clone(), json!("invented version"), Value::Null).unwrap();
    let item = json!({"type":"collabAgentToolCall","id":"call_spawn_1","tool":"spawnAgent","status":"completed","senderThreadId":s.parent,
        "receiverThreadIds":[s.child],"prompt":s.prompt,"agentsStates":{s.child.as_str():{"status":"running","message":null}}});
    view.history("invented-home", "thread/read", &json!({"threadId":s.parent}),
        &json!({"thread":{"id":s.parent,"turns":[{"id":"turn","status":"completed","items":[item]}]}})).unwrap();
    let mut recovered = view.snapshot();
    assert_eq!(recovered["items"][0]["standing"], "recovered-from-supplier");
    recovered["hostThreads"] = json!([{"generation":g,"threadId":s.parent,"cwd":f.project}]);
    f.observe(&mut Session::default(), &[recovered], None);
    assert!(f.lines(0).is_empty() && f.lines(1).is_empty());
}

#[test]
fn the_association_is_recorded_only_as_the_prompt_and_the_brief_file_establish_it() {
    let f = Fixture::new();
    let digest = f.brief("W1.json");
    let line = |file: &str, digest: &str| format!("Count the invented files.\n{BRIEF_REFERENCE} {file} sha256:{digest}\nReturn a list.");
    let state = |prompt: Option<&str>| associate(&f.project, prompt);
    assert_eq!(state(None), json!({"state":"no brief reference"}));
    assert_eq!(state(Some("briefs/W1.json is mentioned, with no reference line")), json!({"state":"no brief reference"}));
    // The tie is recorded: what the brief record itself states, read from the bytes whose identity is recorded.
    assert_eq!(state(Some(&line("briefs/W1.json", &digest))), json!({"state":"brief referenced","brief":"brief:W1","briefRecord":"fl:brief:W1",
        "workItem":"W1","undertaking":"FX-U1","briefFile":"briefs/W1.json","briefContent":{"method":crate::util::FILE_IDENTITY_METHOD,"value":digest}}));
    // The file's bytes are not the referenced ones; which of the two is wrong is not known.
    let other = "0".repeat(64);
    let changed = state(Some(&line("briefs/W1.json", &other)));
    assert_eq!(changed["state"], "brief referenced; content does not match the reference");
    assert_eq!((&changed["referencedContent"]["value"], &changed["currentContent"]["value"]), (&json!(other), &json!(digest)));
    // Nothing is chosen or inferred where the reference does not resolve.
    for (prompt, reason) in [
        (line("briefs/absent.json", &digest), "not present"),
        (line("../briefs/W1.json", &digest), "not a brief file path"),
        (line("graphs/U/r1.json", &digest), "not a brief file path"),
        (format!("{}\n{BRIEF_REFERENCE} briefs/W2.json sha256:{other}", line("briefs/W1.json", &digest)), "more than one brief"),
        (format!("{BRIEF_REFERENCE} briefs/W1.json"), "malformed"),
        (format!("{BRIEF_REFERENCE} briefs/W1.json sha256:{}", digest.to_uppercase()), "malformed"),
    ] {
        let unresolved = state(Some(&prompt));
        assert_eq!(unresolved["state"], "brief reference not resolved", "{prompt}");
        assert!(unresolved["reason"].as_str().unwrap().contains(reason), "{unresolved}");
        assert!(unresolved.get("brief").is_none());
    }
    // A file that is not a brief record ties nothing, whether or not its bytes are the referenced ones.
    let stray = f.project.join(FLEET).join("briefs/stray.json");
    std::fs::write(&stray, b"{}").unwrap();
    for digest in [crate::util::sha256_hex(b"{}"), other.clone()] {
        let unresolved = state(Some(&line("briefs/stray.json", &digest)));
        assert_eq!(unresolved["state"], "brief reference not resolved");
        assert!(unresolved["reason"].as_str().unwrap().contains("not a readable brief record"));
    }
    assert_eq!((&changed["brief"], &changed["briefRecord"], &changed["workItem"], &changed["undertaking"]),
        (&json!("brief:W1"), &json!("fl:brief:W1"), &json!("W1"), &json!("FX-U1")), "a mismatch still records what the file held then");
    // A dispatch record without its tie cannot be read as tied: the format refuses a resolved association that lacks it.
    let mut untied = f.context(&generation("first"));
    untied.activity = None;
    let mut record = super::fact(untied, "dispatch_observed", json!({"mechanism":"Codex native subagent",
        "parent":{"threadId":"p","generation":generation("first")},"child":{"threadId":"c","generation":generation("first")},
        "parentSource":"collabAgentToolCall.senderThreadId","nativeHome":{"homeId":"invented-home","root":crate::attachments::native_path_identity(&f.project),"physical":{"device":1,"inode":1}},
        "spawnItem":{"threadId":"p","turnId":"t","itemId":"i"},"spawnPrompt":{"state":"not supplied"},"association":state(Some(&line("briefs/W1.json", &digest))),
        "observation":{"source":"item/completed notification, received live","position":1},"typesPin":crate::hosting::DECLARED_PIN})).unwrap().record;
    validate_record(&record).unwrap();
    for field in ["workItem", "undertaking", "briefRecord"] {
        let kept = record["body"]["association"].as_object_mut().unwrap().remove(field).unwrap();
        assert!(validate_record(&record).is_err(), "a resolved association without {field} is refused");
        record["body"]["association"][field] = kept;
    }
    // Every state is one the record format admits, on a recorded dispatch.
    let g = generation("first");
    let malformed = format!("{BRIEF_REFERENCE} briefs/W1.json");
    for (index, prompt) in [Some(line("briefs/W1.json", &digest)), Some(line("briefs/W1.json", &other)), Some(line("briefs/absent.json", &digest)), None, Some(malformed)].into_iter().enumerate() {
        let mut s = spawn(&g, Some(prompt.as_deref()));
        s.child = format!("child-{index}");
        let mut view = handed(&s, &g, &f.project);
        for row in view["items"].as_array_mut().unwrap().iter_mut().filter(|row| row["native"]["type"] == "collabAgentToolCall") {
            row["native"]["receiverThreadIds"] = json!([s.child]);
            row["native"]["agentsStates"] = json!({});
        }
        let mut session = Session::default();
        f.observe(&mut session, &[view], None);
        assert!(session.snapshot()["limits"].as_array().unwrap().is_empty(), "{}", session.snapshot()["limits"]);
    }
    let recorded: Vec<Value> = f.of("dispatch_observed").iter().map(|row| row["body"]["association"]["state"].clone()).collect();
    assert_eq!(recorded, json!(["brief referenced", "brief referenced; content does not match the reference", "brief reference not resolved", "no brief reference", "brief reference not resolved"]).as_array().unwrap().clone());
    assert_eq!(f.of("dispatch_observed")[3]["body"]["spawnPrompt"], json!({"state":"not supplied"}));
    // A malformed line gives no complete reference to quote, and the child is still recorded under its parent.
    let loose = &f.of("dispatch_observed")[4]["body"];
    assert_eq!((&loose["association"]["references"], &loose["child"]["threadId"]), (&json!([]), &json!("child-4")));
}

#[test]
fn the_end_of_observation_is_recorded_with_its_cause_and_never_before_it_is_known() {
    let f = Fixture::new();
    let g = generation("first");
    let mut s = spawn(&g, None);
    let mut session = Session::default();
    f.observe(&mut session, &[handed(&s, &g, &f.project)], None);
    s.view.close(&g).unwrap();
    let closed = handed(&s, &g, &f.project);
    f.observe(&mut session, &[closed.clone()], None);
    assert!(f.of("observation_ended").is_empty(), "no cause is recorded before the host reports how the generation ended");
    f.observe(&mut session, &[closed.clone()], Some("Codex process stopped"));
    f.observe(&mut session, &[closed], Some("Codex process stopped"));
    let ended = f.of("observation_ended");
    assert_eq!(ended.len(), 1);
    assert_eq!(ended[0]["body"]["child"], json!({"threadId":s.child,"generation":g}));
    assert_eq!((&ended[0]["body"]["cause"], &ended[0]["body"]["lastObserved"]), (&json!("Codex process stopped"), &json!("pendingInit")));
    assert_eq!(f.rows().len(), 3);
}

#[test]
fn a_session_ends_only_its_own_observation_and_at_its_own_exit() {
    let f = Fixture::new();
    let g = generation("first");
    let s = spawn(&g, None);
    let mut session = Session::default();
    f.observe(&mut session, &[handed(&s, &g, &f.project)], None);
    assert_eq!(f.rows().len(), 2);
    // Another session, which recorded nothing of this child, holds the same home. Reading the same
    // files, and exiting, it records nothing about a child it did not itself observe.
    let second = generation("second");
    let mut other_view = crate::native_items::NativeView::new("invented-home".into()).unwrap();
    other_view.ready(second.clone(), json!("invented version"), Value::Null).unwrap();
    let mut other = Session::default();
    f.observe(&mut other, &[other_view.snapshot()], None);
    other.end_own_delegation(&|_| Some("App quit"));
    assert_eq!(f.rows().len(), 2, "one home under two sessions establishes nothing about the first session's child");
    // The session that recorded the child exits: its own observation ends, once.
    for _ in 0..2 {
        session.end_own_delegation(&|_| Some("App quit"));
    }
    let ended = f.of("observation_ended");
    assert_eq!(ended.len(), 1);
    assert_eq!(ended[0]["body"], json!({"child":{"threadId":s.child,"generation":g},"cause":"App quit","lastObserved":"pendingInit",
        "nativeHome":f.of("dispatch_observed")[0]["body"]["nativeHome"]}));
    // A generation whose home the exiting session no longer holds is given no end.
    let h = Fixture::new();
    let mut session = Session::default();
    h.observe(&mut session, &[handed(&s, &g, &h.project)], None);
    session.end_own_delegation(&|_| None);
    assert!(h.of("observation_ended").is_empty());
}

#[test]
fn facts_reach_the_store_in_the_order_observed_after_failed_writes() {
    let f = Fixture::new();
    let g = generation("first");
    let mut s = spawn(&g, None);
    // The store's log cannot be written: a folder stands where the file belongs.
    let log = published_at(&f.scope, 0);
    std::fs::create_dir_all(&log).unwrap();
    let mut session = Session::default();
    f.observe(&mut session, &[handed(&s, &g, &f.project)], None);
    s.view.close(&g).unwrap();
    f.observe(&mut session, &[handed(&s, &g, &f.project)], Some("Codex process stopped"));
    assert!(session.has_pending() && f.lines(1).is_empty(), "nothing reaches the project's log before the store holds it");
    std::fs::remove_dir(&log).unwrap();
    for _ in 0..3 {
        session.retry(Some(&f.project));
    }
    let kinds: Vec<Value> = f.rows().iter().map(|row| row["kind"].clone()).filter(|kind| KINDS.contains(&kind.as_str().unwrap())).collect();
    assert_eq!(kinds, json!(["dispatch_observed", "child_observed", "observation_ended"]).as_array().unwrap().clone(),
        "a delayed status is never written after the end of its own observation");
    assert!(!session.has_pending());
}

#[test]
fn an_observation_whose_recording_context_is_unavailable_waits_and_is_then_recorded_once() {
    let f = Fixture::new();
    let g = generation("first");
    let s = spawn(&g, None);
    let view = handed(&s, &g, &f.project);
    let mut session = Session::default();
    // As when the project is not attached, or its link was changed: no recording context.
    session.observe_delegation_views(Some(&f.project), &[view.clone()], &mut |generation| {
        let mut context = f.context(generation);
        context.scope = Err("link changed; not attached".into());
        context.activity = None;
        context
    }, &|_| None);
    assert!(f.lines(0).is_empty() && f.lines(1).is_empty());
    assert!(session.snapshot()["limits"].to_string().contains("waits to be recorded: link changed; not attached"));
    assert!(!session.has_pending(), "nothing is owed to a context that does not exist");
    f.observe(&mut session, &[view.clone()], None);
    f.observe(&mut session, &[view], None);
    assert_eq!((f.of("dispatch_observed").len(), f.of("child_observed").len()), (1, 1));
}

// Every later fact of a child goes through the context frozen when the child
// was first recorded, and the writer's own physical check applies to it. Here
// another folder stands at the project's path with a copy of its link: same
// identities, same spelling, another place. Nothing is written of the child
// there; when the original is back, its end is recorded once.
#[test]
fn a_later_fact_of_a_child_is_published_only_through_its_first_frozen_context() {
    let f = Fixture::new();
    let g = generation("first");
    let mut s = spawn(&g, None);
    let mut session = Session::default();
    f.observe(&mut session, &[handed(&s, &g, &f.project)], None);
    assert_eq!(f.rows().len(), 2);
    let store_log = || std::fs::read_to_string(published_at(&f.scope, 0)).unwrap();
    let before = store_log();
    let away = f.root.join("project-moved-away");
    std::fs::rename(&f.project, &away).unwrap();
    std::fs::create_dir_all(f.project.join(".chirality")).unwrap();
    std::fs::copy(away.join(crate::records_store::PROJECT_LINK), f.project.join(crate::records_store::PROJECT_LINK)).unwrap();
    s.view.close(&g).unwrap();
    // The tick would freeze the replacement afresh if asked; a child already recorded is never asked.
    let mut frozen_again = 0;
    session.observe_delegation_views(Some(&f.project), &[handed(&s, &g, &f.project)], &mut |generation| { frozen_again += 1; f.context(generation) }, &|_| Some("Codex process stopped"));
    session.end_own_delegation(&|_| Some("App quit"));
    session.retry(Some(&f.project));
    assert_eq!(frozen_again, 0, "the context of a recorded child is not captured again");
    assert_eq!(store_log(), before, "nothing is written of the child while another folder stands at its project's path");
    assert!(!f.project.join(FLEET).exists(), "and nothing in the replacement folder");
    assert!(session.snapshot()["limits"].to_string().contains("the context this child was first recorded under no longer holds"));
    std::fs::remove_dir_all(&f.project).unwrap();
    std::fs::rename(&away, &f.project).unwrap();
    f.observe(&mut session, &[handed(&s, &g, &f.project)], Some("Codex process stopped"));
    session.end_own_delegation(&|_| Some("App quit"));
    assert_eq!(f.of("observation_ended").len(), 1);
    assert_eq!(f.of("observation_ended")[0]["body"]["cause"], "Codex process stopped");
}

// Review round 4. A child is a thread in a home, whatever generation of Codex
// reports it: its recording context is the one frozen when this session first
// recorded it, and no later fact of it, in any generation, captures another.
#[test]
fn a_child_keeps_its_first_context_across_a_restart_of_codex() {
    let f = Fixture::new();
    let first = generation("first");
    let mut s = spawn(&first, None);
    let mut session = Session::default();
    let captures = std::cell::Cell::new(0);
    // A capture that would succeed under whatever identity is in force when it is asked.
    let mut capture = |generation: &Value| {
        captures.set(captures.get() + 1);
        let mut context = f.context(generation);
        context.scope = Scope::capture(&f.project);
        context
    };
    session.observe_delegation_views(Some(&f.project), &[handed(&s, &first, &f.project)], &mut capture, &|_| None);
    assert_eq!((captures.get(), f.rows().len()), (1, 2), "the first record of the child captures its context once");
    s.view.close(&first).unwrap();
    session.observe_delegation_views(Some(&f.project), &[handed(&s, &first, &f.project)], &mut capture, &|_| Some("Codex process stopped"));
    assert_eq!(f.of("observation_ended").len(), 1);
    // Codex is started again in the same App session: a later generation, the same home, and a live item naming the same child.
    let second = json!({"appSession":"first","home":"invented-home","spawnCounter":2});
    let later = |status: &str, item: &str, position: u64| {
        let mut view = crate::native_items::NativeView::new("invented-home".into()).unwrap();
        view.ready(second.clone(), json!("invented version"), Value::Null).unwrap();
        for (n, (id, reported)) in [("wait-1", "running"), (item, status)].iter().enumerate().take(if item == "wait-1" { 1 } else { 2 }) {
            view.consume(&json!({"generation":second,"position":position + n as u64,"frame":{"method":"item/completed","params":{"threadId":s.parent,"turnId":"later-turn",
                "item":{"type":"collabAgentToolCall","id":id,"tool":"wait","status":"completed","senderThreadId":s.parent,"receiverThreadIds":[s.child],
                    "agentsStates":{s.child.as_str():{"status":reported,"message":null}}}}}})).unwrap();
        }
        let mut handed = view.snapshot();
        handed["hostThreads"] = json!([{"generation":second,"threadId":s.parent,"cwd":f.project}]);
        handed
    };
    session.observe_delegation_views(Some(&f.project), &[later("running", "wait-1", 1)], &mut capture, &|_| None);
    let statuses = f.of("child_observed");
    assert_eq!(statuses.len(), 2);
    assert_eq!((&statuses[1]["body"]["status"], &statuses[1]["body"]["child"]["generation"]), (&json!("running"), &second));
    // Where each record of the child landed, read from the files themselves: the store subtree and the
    // project log of the context it was first recorded under, and nowhere else.
    let landed = |path: PathBuf| -> Vec<Value> {
        std::fs::read_to_string(path).unwrap_or_default().lines().map(|line| serde_json::from_str::<Value>(line).unwrap())
            .filter(|row| row["body"]["child"]["threadId"] == s.child.as_str()).map(|row| row["kind"].clone()).collect()
    };
    let of_child = json!(["dispatch_observed", "child_observed", "observation_ended", "child_observed"]).as_array().unwrap().clone();
    assert_eq!(landed(published_at(&f.scope, 0)), of_child, "every record of the child is in the original store subtree");
    assert_eq!(landed(published_at(&f.scope, 1)), of_child, "and, as the identical lines, in the original project's log");
    assert_eq!(captures.get(), 1, "the later generation's status goes through the child's first context, captured zero more times");
    // The project is given a new records identity. A capture now would succeed under it; none is made for this child.
    let before = std::fs::read_to_string(published_at(&f.scope, 0)).unwrap();
    crate::records_store::new_identity(&f.project).unwrap();
    let replacement = crate::records_store::attach(&f.project, false).unwrap().dir.unwrap();
    assert_ne!(replacement, f.scope.dir.path);
    session.observe_delegation_views(Some(&f.project), &[later("completed", "wait-2", 1)], &mut capture, &|_| None);
    session.end_own_delegation(&|_| Some("App quit"));
    session.retry(Some(&f.project));
    // Where the later status and the exit's end landed: nowhere. The writes were refused, and the files show it.
    assert!(landed(replacement.join("fleet").join("coordination.fleet.jsonl")).is_empty(), "nothing of that child under the replacement identity");
    assert!(!replacement.join("fleet").exists(), "the replacement subtree gained no fleet log at all");
    assert_eq!(std::fs::read_to_string(published_at(&f.scope, 0)).unwrap(), before, "and nothing more under the original, which no longer holds");
    assert_eq!(landed(published_at(&f.scope, 1)), of_child, "nor in the project's log");
    assert!(session.has_pending() || session.snapshot()["limits"].to_string().contains("waits to be recorded"), "the refused facts are stated as unwritten");
    // A second assertion only: a count of zero would prove nothing if a writer did not ask.
    assert_eq!(captures.get(), 1, "across a generation change, a later status and the exit, the context is never captured again");
    assert!(session.snapshot()["limits"].to_string().contains("the context this child was first recorded under no longer holds"));
}

// ---- At the next start: the end, cause "App relaunch", of an observation an
// earlier session of this App left open.

/// Session "first" records a dispatch and a status, and ends without recording
/// the end of its observation (a crash, or an exit whose end was not written).
fn left_open(f: &Fixture) -> (Spawn, Value) {
    let first = generation("first");
    let s = spawn(&first, None);
    f.observe(&mut Session::default(), &[handed(&s, &first, &f.project)], None);
    assert_eq!(f.rows().len(), 2);
    (s, first)
}
fn established(current: &str, ended: &[&str]) -> impl Fn() -> Result<(String, BTreeSet<String>), String> {
    let (current, ended): (String, BTreeSet<String>) = (current.into(), ended.iter().map(|s| s.to_string()).collect());
    move || Ok((current.clone(), ended.clone()))
}

#[test]
fn an_observation_an_earlier_session_left_open_is_ended_at_the_next_start_as_app_relaunch() {
    let f = Fixture::new();
    let (s, first) = left_open(&f);
    let mut second = Session::default();
    assert_eq!(second.reconciliation_status()["state"], "pending", "before it has run, a read is told it is pending");
    for _ in 0..3 {
        second.end_earlier_observations(Some(&f.project), &established("second", &["first"]));
    }
    let ended = f.of("observation_ended");
    assert_eq!(ended.len(), 1, "one end, however many record ticks");
    assert_eq!(ended[0]["body"], json!({"child":{"threadId":s.child,"generation":first},"cause":"App relaunch","lastObserved":"pendingInit",
        "nativeHome":f.of("dispatch_observed")[0]["body"]["nativeHome"]}));
    let status = second.reconciliation_status();
    assert_eq!((status["state"].as_str(), status["endsRecorded"].as_u64()), (Some("recorded"), Some(1)), "{status}");
    assert!(status.get("limit").is_none(), "{status}");
    // A later session finds that end in the store and records no second one.
    let mut third = Session::default();
    third.end_earlier_observations(Some(&f.project), &established("third", &["first", "second"]));
    assert_eq!(f.of("observation_ended").len(), 1);
}

#[test]
fn a_session_the_ledger_did_not_establish_as_ended_is_never_ended_and_not_looked_at_again() {
    let f = Fixture::new();
    left_open(&f);
    let mut second = Session::default();
    second.end_earlier_observations(Some(&f.project), &established("second", &[]));
    assert!(f.of("observation_ended").is_empty());
    let status = second.reconciliation_status();
    assert_eq!(status["sessionsNotEstablished"], json!(["first"]), "{status}");
    assert!(status["limit"].as_str().unwrap().contains("could not be established"), "{status}");
    // Not looked at again in this session.
    second.end_earlier_observations(Some(&f.project), &established("second", &["first"]));
    assert!(f.of("observation_ended").is_empty());
    // The App ledger itself unavailable: nothing is ended, and that is stated.
    let mut third = Session::default();
    third.end_earlier_observations(Some(&f.project), &|| Err("App ledger unavailable".into()));
    assert!(f.of("observation_ended").is_empty());
    assert!(third.reconciliation_status()["limit"].as_str().unwrap().contains("App ledger unavailable"));
}

/// Two Apps, each with its own App data, on one project and store: the second
/// App's ledger establishes only its own sessions, so the first App's open
/// observation is never ended by the second, whatever home or project they share.
#[test]
fn another_apps_session_is_never_ended_by_this_one() {
    let f = Fixture::new();
    left_open(&f);
    let app_two = f.root.join("app-two");
    std::fs::create_dir_all(&app_two).unwrap();
    let _custody = crate::hold_app_data_for_test(&app_two).unwrap();
    let mut ledger = crate::recovery::RecoveryLedger::open(app_two.join("recovery.ledger.jsonl")).unwrap();
    ledger.start_session("app-two", "candidate").unwrap();
    let rows = ledger.recorded_entries().as_array().unwrap().clone();
    let set = crate::recovery::established_ended_sessions(&rows, "app-two").unwrap();
    assert!(!set.contains("first"), "{set:?}");
    assert!(crate::recovery::established_ended_sessions(&rows, "never-started").is_err(), "a session whose start is not in the ledger establishes nothing");
    let mut two = Session::default();
    let sessions = move || Ok(("app-two".to_owned(), set.clone()));
    two.end_earlier_observations(Some(&f.project), &sessions);
    assert!(f.of("observation_ended").is_empty());
    assert_eq!(two.reconciliation_status()["sessionsNotEstablished"], json!(["first"]));
}

#[test]
fn an_end_whose_write_failed_is_retried_at_the_record_tick_and_written_once() {
    let f = Fixture::new();
    left_open(&f);
    let mut second = Session::default();
    super::super::FAIL_AFTER_WRITE.with(|flag| flag.set(Some(0)));
    second.end_earlier_observations(Some(&f.project), &established("second", &["first"]));
    super::super::FAIL_AFTER_WRITE.with(|flag| flag.set(None));
    let status = second.reconciliation_status();
    assert_eq!(status["state"], "unavailable", "{status}");
    assert!(status["limit"].as_str().unwrap().contains("retried at the next record tick"), "{status}");
    second.retry(Some(&f.project));
    assert_eq!(f.of("observation_ended").len(), 1, "the retry writes that one end, once");
    assert_eq!(second.reconciliation_status()["state"], "recorded");
}

/// A write the earlier App left part way (its last line unclosed, as a crash
/// mid-append leaves it): no end is recorded over it, and that is stated as
/// unavailable with the reason, tried again at each record tick; nothing reads
/// as reconciled.
#[test]
fn a_log_left_with_an_unclosed_line_is_reported_unavailable_and_nothing_is_ended() {
    use std::io::Write;
    let f = Fixture::new();
    left_open(&f);
    let store = published_at(&f.scope, 0);
    std::fs::OpenOptions::new().append(true).open(&store).unwrap().write_all(b"{\"format\":\"chirality.fleet.rec").unwrap();
    let mut second = Session::default();
    for _ in 0..2 {
        second.end_earlier_observations(Some(&f.project), &established("second", &["first"]));
    }
    assert!(!std::fs::read_to_string(&store).unwrap().contains("App relaunch"), "nothing is written over the unclosed line");
    let status = second.reconciliation_status();
    assert_eq!(status["state"], "unavailable", "{status}");
    assert!(status["limit"].as_str().unwrap().contains("unclosed final line"), "{status}");
}

/// An end another writer records after this session's read and before its
/// apply is found under the store's writer lock: no second end is written,
/// and the reconciliation says the end was found already recorded (round 2 of
/// the review, within the older-build exception of session liveness).
#[test]
fn an_end_recorded_after_the_read_is_found_and_not_written_twice() {
    let f = Fixture::new();
    let first = generation("first");
    let s = spawn(&first, None);
    let mut earlier = Session::default();
    f.observe(&mut earlier, &[handed(&s, &first, &f.project)], None);
    let read = read_earlier(Some(&f.project), &established("second", &["first"]));
    earlier.end_own_delegation(&|_| Some("App quit"));
    assert_eq!(f.of("observation_ended").len(), 1);
    let mut second = Session::default();
    second.apply_earlier(read);
    let ended = f.of("observation_ended");
    assert_eq!(ended.len(), 1, "the governing log already holds this generation's end: {ended:?}");
    assert_eq!(ended[0]["body"]["cause"], "App quit");
    let status = second.reconciliation_status();
    assert_eq!((status["state"].as_str(), status["endsRecorded"].as_u64(), status["endsFoundAlreadyRecorded"].as_u64()), (Some("recorded"), Some(0), Some(1)), "{status}");
    second.retry(Some(&f.project));
    assert_eq!(f.of("observation_ended").len(), 1);
}

/// Two reads applied in turn, a failed write retried, a later session, a
/// duplicated line and a torn line: one end at most, and nothing written over
/// a log that is not whole.
#[test]
fn overlapping_reads_retries_and_damaged_logs_take_one_end_at_most() {
    {
        let f = Fixture::new();
        left_open(&f);
        let a = read_earlier(Some(&f.project), &established("second", &["first"]));
        let b = read_earlier(Some(&f.project), &established("second", &["first"]));
        let mut second = Session::default();
        super::super::FAIL_AFTER_WRITE.with(|flag| flag.set(Some(0)));
        second.apply_earlier(a);
        super::super::FAIL_AFTER_WRITE.with(|flag| flag.set(None));
        assert_eq!(second.reconciliation_status()["state"], "unavailable");
        second.apply_earlier(b);
        second.retry(Some(&f.project));
        assert_eq!(second.reconciliation_status()["state"], "recorded");
        assert_eq!(f.of("observation_ended").len(), 1);
        let mut third = Session::default();
        third.end_earlier_observations(Some(&f.project), &established("third", &["first", "second"]));
        assert_eq!(f.of("observation_ended").len(), 1);
    }
    for torn in [false, true] {
        use std::io::Write;
        let f = Fixture::new();
        left_open(&f);
        let path = published_at(&f.scope, 0);
        let extra = if torn { b"{\"format\":\"chirality.fleet.rec".to_vec() } else {
            let bytes = std::fs::read(&path).unwrap();
            bytes.split_inclusive(|b| *b == b'\n').next().unwrap().to_vec()
        };
        std::fs::OpenOptions::new().append(true).open(&path).unwrap().write_all(&extra).unwrap();
        let before = std::fs::read(&path).unwrap();
        let mut second = Session::default();
        for _ in 0..2 {
            second.end_earlier_observations(Some(&f.project), &established("second", &["first"]));
        }
        assert_eq!(std::fs::read(&path).unwrap(), before);
        assert_eq!(second.reconciliation_status()["state"], "unavailable");
        let words = second.reconciliation_status()["limit"].as_str().unwrap().to_owned();
        assert!(words.contains(if torn { "unclosed final line" } else { "duplicate/conflicting" }), "{words}");
    }
}
