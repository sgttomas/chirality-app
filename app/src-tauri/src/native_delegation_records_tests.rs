//! Invented local fixtures. The spawn frames are the supplier's own, recorded
//! at the pipe (supplier_checks/recordings/nv04.recording.json) and received
//! through the App's native view; they show what the recorder writes from
//! such frames, not that a supplier's child ran on a candidate.
use super::*;
use std::path::PathBuf;

const RECORDING: &str = include_str!("../../supplier_checks/recordings/nv04.recording.json");
const BRIEF: &str = include_str!("../../tests/fixtures/FX-FL1/briefs/W1.json");

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
    // The prompt's identity is recomputed here from the recorded frame; its text is nowhere in the files.
    assert!(!s.prompt.is_empty());
    assert_eq!(body["spawnPrompt"], json!({"state":"supplied","bytes":s.prompt.len(),
        "content":{"method":crate::util::FILE_IDENTITY_METHOD,"value":crate::util::sha256_hex(s.prompt.as_bytes())}}));
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
    assert_eq!(state(Some(&line("briefs/W1.json", &digest))), json!({"state":"brief referenced","brief":"brief:W1","briefFile":"briefs/W1.json",
        "briefContent":{"method":crate::util::FILE_IDENTITY_METHOD,"value":digest}}));
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
    // A file with the referenced bytes that is not a brief record ties nothing.
    let stray = f.project.join(FLEET).join("briefs/stray.json");
    std::fs::write(&stray, b"{}").unwrap();
    assert_eq!(state(Some(&line("briefs/stray.json", &crate::util::sha256_hex(b"{}"))))["state"], "brief reference not resolved");
    // Every state is one the record format admits, on a recorded dispatch.
    let g = generation("first");
    for (index, prompt) in [Some(line("briefs/W1.json", &digest)), Some(line("briefs/W1.json", &other)), Some(line("briefs/absent.json", &digest)), None].into_iter().enumerate() {
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
    assert_eq!(recorded, json!(["brief referenced", "brief referenced; content does not match the reference", "brief reference not resolved", "no brief reference"]).as_array().unwrap().clone());
    assert_eq!(f.of("dispatch_observed")[3]["body"]["spawnPrompt"], json!({"state":"not supplied"}));
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
fn a_child_recorded_by_an_earlier_session_is_ended_at_relaunch_from_stored_lines_alone() {
    let f = Fixture::new();
    let first = generation("first");
    let s = spawn(&first, None);
    f.observe(&mut Session::default(), &[handed(&s, &first, &f.project)], None);
    assert_eq!(f.rows().len(), 2);
    // The App is relaunched: a new session holds the same home, with nothing received yet.
    let second = generation("second");
    let mut view = crate::native_items::NativeView::new("invented-home".into()).unwrap();
    view.ready(second.clone(), json!("invented version"), Value::Null).unwrap();
    let mut session = Session::default();
    for _ in 0..3 {
        f.observe(&mut session, &[view.snapshot()], None);
    }
    let ended = f.of("observation_ended");
    assert_eq!(ended.len(), 1);
    assert_eq!(ended[0]["body"], json!({"child":{"threadId":s.child,"generation":first},"cause":"App relaunch","lastObserved":"pendingInit",
        "nativeHome":f.of("dispatch_observed")[0]["body"]["nativeHome"]}));
    // A session that holds another home says nothing of this one's children.
    let g = Fixture::new();
    let s = spawn(&first, None);
    g.observe(&mut Session::default(), &[handed(&s, &first, &g.project)], None);
    let mut other = crate::native_items::NativeView::new("another-home".into()).unwrap();
    let other_generation = json!({"appSession":"second","home":"another-home","spawnCounter":1});
    other.ready(other_generation, json!("invented version"), Value::Null).unwrap();
    g.observe(&mut Session::default(), &[other.snapshot()], None);
    assert!(g.of("observation_ended").is_empty());
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
