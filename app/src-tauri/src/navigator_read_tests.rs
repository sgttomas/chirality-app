//! The navigator's read, with invented material only: placement, ordering,
//! titles, the not-read cases, the runs the App holds joined to their
//! conversations, waiting requests, and a real records store (the launched
//! project, another listed project, a gone one, a torn registry, a launched
//! path through a symlink) read as the command reads it, without writing or
//! remembering anything.
use super::*;
use serde_json::json;
use std::path::PathBuf;

const HOME: &str = "app-home:invented";

fn generation() -> Value {
    json!({"appSession":"session:invented","home":HOME,"spawnCounter":1})
}
fn empty() -> Gathered {
    Gathered {
        read_at: "2026-11-19T00:00:00.000Z".into(),
        current_root: None,
        aliases: vec![],
        no_project_folders: vec!["/data/conversations-without-project".into()],
        registry: Ok(crate::records_store::ListedFolders::default()),
        folders: vec![],
        held: HeldRuns::default(),
        homes: vec![],
        index: vec![],
        finished: vec![],
        catalog: CatalogInput::default(),
    }
}
fn listed(root: &str, id: &str, line: usize) -> crate::records_store::ListedFolder {
    crate::records_store::ListedFolder { root: root.into(), identities: vec![id.into()], first_line: line }
}
fn registry(folders: Vec<crate::records_store::ListedFolder>) -> Result<crate::records_store::ListedFolders, String> {
    Ok(crate::records_store::ListedFolders { folders, ..Default::default() })
}
fn attached(root: &str, id: &str) -> FolderInput {
    FolderInput { root: root.into(), examined: Examined::Attached { project: Some(id.into()), fault: None, refusal: None, resolutions: vec![], unavailable: None } }
}
fn other(root: &str) -> FolderInput {
    FolderInput { root: root.into(), examined: Examined::Listed }
}
/// A held reading of the launched project's recorded runs, with no limit.
fn held(runs: Vec<RunInput>) -> HeldRuns {
    HeldRuns { recorded: HeldReading::Read { read_at: Some("2026-11-18T09:00:00.000Z".into()), limits: vec![], notices: vec![], runs }, process: vec![] }
}
/// A ready home whose list was read to its end.
fn home(class: &str, threads: Vec<Value>, loaded: Vec<Value>) -> HomeInput {
    HomeInput {
        class: class.into(),
        state: "ready".into(),
        generation: generation(),
        current: true,
        loaded,
        history: Some(HistoryInput { generation: generation(), selection_epoch: 3, threads, read_at_ready: Some(json!({"generation":generation(),"state":"read-to-end"})) }),
        waiting: vec![],
        descendants: vec![],
    }
}
fn account(threads: Vec<Value>, loaded: Vec<Value>) -> HomeInput {
    home("account", threads, loaded)
}
fn thread(id: &str, cwd: &str, updated: i64) -> Value {
    json!({"id":id,"cwd":cwd,"name":null,"preview":format!("first message of {id}"),"createdAt":updated - 100,"updatedAt":updated,"status":{"type":"notLoaded"},"parentThreadId":null})
}
fn loaded_row(id: &str, cwd: &str) -> Value {
    json!({"generation":generation(),"threadId":id,"name":null,"preview":null,"status":{"type":"idle"},"cwd":cwd})
}
fn run(id: &str, conversation: &str, lifecycle: RecordedLifecycle, at: &str) -> RunInput {
    RunInput {
        run_id: id.into(),
        conversation: Some(conversation.into()),
        workflow: json!({"kind":"workflow","origin":"project","sourceRoot":"/p/library","name":"review-pack","revision":"rev-1"}),
        lifecycle,
        started_at: Some(at.into()),
        home: None,
    }
}
/// A recovery ledger `conversation_index` row as a Host holds it.
fn index(home: &str, thread: &str, project: &str, runs: &[&str]) -> Value {
    json!({"kind":"conversation_index","home":crate::stop_records::home_class(home).unwrap(),"threadId":thread,"project":project,
        "tags":runs.iter().map(|r| json!({"owner":crate::run_restart::RUN_TAG_OWNER,"value":r})).collect::<Vec<_>>()})
}
fn project<'a>(read: &'a NavigatorRead, root: &str) -> &'a NavigatorProject {
    read.projects.iter().find(|p| p.root == root).unwrap_or_else(|| panic!("no project {root} in {:#?}", read.projects))
}
fn entries<'a>(read: &'a NavigatorRead) -> impl Iterator<Item = &'a NavigatorEntry> {
    read.projects.iter().flat_map(|p| &p.entries).chain(&read.unassigned)
}
fn entry<'a>(read: &'a NavigatorRead, id: &str) -> &'a NavigatorEntry {
    entries(read).find(|e| e.id == id).unwrap_or_else(|| panic!("no entry {id}"))
}
fn entry_in<'a>(read: &'a NavigatorRead, home: &str, id: &str) -> &'a NavigatorEntry {
    entries(read).find(|e| e.id == id && e.home.as_deref() == Some(home)).unwrap_or_else(|| panic!("no entry {id} in {home}"))
}

#[test]
fn placement_by_record_then_reported_folder_then_unassigned_then_a_folder_section() {
    let mut g = empty();
    g.current_root = Some("/work/alpha".into());
    g.registry = registry(vec![listed("/work/alpha", "P-alpha", 0), listed("/work/beta", "P-beta", 1)]);
    g.folders = vec![attached("/work/alpha", "P-alpha"), other("/work/beta")];
    let mut child = thread("child", "/work/alpha", 50);
    child["parentThreadId"] = json!("by-folder");
    g.homes = vec![account(vec![
        // Codex reports beta's folder, the App recorded alpha: the record governs.
        thread("recorded", "/work/beta", 10),
        thread("by-folder", "/work/beta", 20),
        thread("no-project", "/data/conversations-without-project", 30),
        thread("elsewhere", "/somewhere/else", 40),
        child,
    ], vec![])];
    g.index = vec![index("account", "recorded", "/work/alpha", &[])];
    let read = compose(g);

    let recorded = entry(&read, "recorded");
    assert_eq!((recorded.project_root.as_deref(), recorded.project_source), (Some("/work/alpha"), ProjectSource::Recorded));
    let by_folder = entry(&read, "by-folder");
    assert_eq!((by_folder.project_root.as_deref(), by_folder.project_source, by_folder.archived), (Some("/work/beta"), ProjectSource::ReportedFolder, Some(false)));
    assert_eq!(read.unassigned.iter().map(|e| e.id.as_str()).collect::<Vec<_>>(), ["no-project"]);
    let section = project(&read, "/somewhere/else");
    assert_eq!((section.project_id.as_deref(), section.state, section.current), (None, ProjectState::Listed, false));
    assert_eq!(section.notice.as_ref().unwrap().kind, "no-identity");
    assert!(entries(&read).all(|e| e.id != "child"), "a delegated child is no entry");
    let beta = project(&read, "/work/beta");
    assert_eq!((beta.project_id.as_deref(), beta.state, beta.notice.clone()), (Some("P-beta"), ProjectState::Listed, None));
    assert_eq!(beta.runs_read.outcome, RunsOutcome::NotRead { reason: NOT_OPEN_RUNS.into() });
    assert_eq!(read.conversations, vec![ConversationsRead { home: "account".into(), list: LIST_WORDS.into(), read_at: None, outcome: ReadOutcome::Read }]);
}

#[test]
fn a_recorded_reference_spelled_as_launched_names_the_physical_root() {
    let mut g = empty();
    g.current_root = Some("/private/work/alpha".into());
    g.aliases = vec![("/work/alpha".into(), "/private/work/alpha".into())];
    g.folders = vec![attached("/private/work/alpha", "P-alpha")];
    g.homes = vec![account(vec![thread("t", "/other", 1)], vec![])];
    g.index = vec![index("account", "t", "/work/alpha", &[])];
    let read = compose(g);
    assert_eq!(read.projects.len(), 1);
    assert_eq!(entry(&read, "t").project_root.as_deref(), Some("/private/work/alpha"));
}

// Point 17 with the project order: a loaded entry with no time first.
#[test]
fn ordering_current_first_then_newest_entry_then_registry_order_and_loaded_untimed_first() {
    let mut g = empty();
    g.current_root = Some("/w/current".into());
    g.registry = registry(vec![listed("/w/current", "P0", 0), listed("/w/quiet-early", "P1", 1), listed("/w/busy", "P2", 2), listed("/w/quiet-late", "P3", 3)]);
    g.folders = vec![attached("/w/current", "P0"), other("/w/quiet-early"), other("/w/busy"), other("/w/quiet-late")];
    g.homes = vec![account(vec![thread("old", "/w/busy", 100), thread("new", "/w/busy", 300), thread("mid", "/w/current", 200)], vec![loaded_row("loaded-only", "/w/busy")])];
    g.index = vec![index("account", "recorded-only", "/w/busy", &[])];
    let read = compose(g);
    let roots: Vec<&str> = read.projects.iter().map(|p| p.root.as_str()).collect();
    assert_eq!(roots, ["/w/current", "/w/busy", "/w/quiet-early", "/w/quiet-late"]);
    assert!(read.projects[0].current && read.projects[1..].iter().all(|p| !p.current));
    assert_eq!(read.projects[0].state, ProjectState::Open);
    let busy: Vec<&str> = project(&read, "/w/busy").entries.iter().map(|e| e.id.as_str()).collect();
    assert_eq!(busy, ["loaded-only", "new", "old", "recorded-only"], "loaded with no time, then newest first, then other untimed");
    let new = entry(&read, "new");
    assert_eq!(new.updated_at.as_deref(), Some("1970-01-01T00:05:00.000Z"));
    assert_eq!(new.created_at.as_deref(), Some("1970-01-01T00:03:20.000Z"));
    assert_eq!((entry(&read, "loaded-only").updated_at.clone(), entry(&read, "loaded-only").archived), (None, None));
}

#[test]
fn titles_from_name_then_preview_cut_on_a_word_then_none() {
    assert_eq!(title(Some("  Named  "), Some("preview")), (Some("Named".into()), TitleSource::Name));
    assert_eq!(title(Some(" "), Some("Short\n first   message")), (Some("Short first message".into()), TitleSource::Preview));
    // 58 characters, a space, then a word that crosses the 60th character.
    let long = format!("{} {}", "a".repeat(58), "overflowing words follow");
    let (cut, source) = title(None, Some(&long));
    assert_eq!((cut.as_deref(), source), (Some("a".repeat(58).as_str()), TitleSource::Preview));
    // A boundary exactly at 60 characters keeps all 60.
    let exact = format!("{} next", "b".repeat(60));
    assert_eq!(title(None, Some(&exact)).0.unwrap(), "b".repeat(60));
    // One word longer than the limit is cut at the limit; characters, not bytes.
    let word = "é".repeat(70);
    assert_eq!(title(None, Some(&word)).0.unwrap().chars().count(), TITLE_CHARS);
    assert_eq!(title(None, Some("   ")), (None, TitleSource::None));
    assert_eq!(title(None, None), (None, TitleSource::None));
}

#[test]
fn conversations_not_read_still_return_projects_and_run_record_entries() {
    let mut g = empty();
    g.current_root = Some("/w/alpha".into());
    g.folders = vec![attached("/w/alpha", "P-alpha")];
    g.held = held(vec![run("run:1", "thread:recorded-run", RecordedLifecycle::OpenInterrupted, "2026-11-01T00:00:00Z")]);
    let mut stopped = account(vec![], vec![]);
    stopped.state = "absent".into();
    stopped.current = false;
    stopped.history = None;
    let mut key = home("api-key", vec![], vec![]);
    key.history.as_mut().unwrap().read_at_ready = None;
    let mut cut = home("local-provider", vec![], vec![]);
    cut.history.as_mut().unwrap().read_at_ready = Some(json!({"generation":generation(),"state":"stopped","reason":"Codex did not answer the history list read in time"}));
    g.homes = vec![stopped, key, cut];
    let read = compose(g);
    let reasons: Vec<String> = read.conversations.iter().map(|c| match &c.outcome { ReadOutcome::NotRead { reason } => reason.clone(), ReadOutcome::Read => panic!("{} read", c.home) }).collect();
    assert!(reasons[0].contains("not running"), "{reasons:?}");
    assert!(reasons[1].contains("whole list"), "{reasons:?}");
    assert!(reasons[2].contains("not read to its end") && reasons[2].contains("did not answer"), "{reasons:?}");
    assert!(read.conversations.iter().all(|c| c.list == LIST_WORDS && c.read_at.is_none()));
    let alpha = project(&read, "/w/alpha");
    assert_eq!(alpha.runs_read.outcome, RunsOutcome::Read);
    let only = &alpha.entries[0];
    assert_eq!((only.id.as_str(), only.live, only.project_source, only.home.as_deref(), only.archived), ("thread:recorded-run", Live::Unknown, ProjectSource::RunRecord, None, None));
    assert!(matches!(&only.open, OpenWith::NotOpenable { reason } if reason.contains("run record")));
    assert_eq!((only.run.as_ref().unwrap().state, only.run_count), (RunState::Open, 1));
}

// E2: a run stays in the project whose records hold it.
#[test]
fn a_run_of_the_launched_project_is_not_shown_on_an_entry_placed_under_another() {
    let mut g = empty();
    g.current_root = Some("/w/alpha".into());
    g.registry = registry(vec![listed("/w/alpha", "PA", 0), listed("/w/beta", "PB", 1)]);
    g.folders = vec![attached("/w/alpha", "PA"), other("/w/beta")];
    g.held = held(vec![run("run:1", "thread:x", RecordedLifecycle::StartNotConfirmed, "2026-11-01T00:00:00Z")]);
    // This process holds a run on a conversation Codex reports under beta.
    let mut own = run("run:2", "thread:y", RecordedLifecycle::OpenInterrupted, "2026-11-02T00:00:00Z");
    own.home = Some("account".into());
    g.held.process = vec![own];
    g.homes = vec![account(vec![thread("thread:y", "/w/beta", 5)], vec![])];
    // The App recorded thread:x under beta.
    g.index = vec![index("account", "thread:x", "/w/beta", &[])];
    let read = compose(g);
    let x = entry(&read, "thread:x");
    assert_eq!((x.home.as_deref(), x.project_root.as_deref(), x.project_source, x.run.clone(), x.run_count), (Some("account"), Some("/w/beta"), ProjectSource::Recorded, None, 0));
    let y = entry(&read, "thread:y");
    assert_eq!((y.project_root.as_deref(), y.run.clone(), y.run_count), (Some("/w/beta"), None, 0));
    let alpha = project(&read, "/w/alpha");
    assert!(alpha.entries.is_empty(), "{:?}", alpha.entries);
    assert_eq!((alpha.unplaced_runs, alpha.runs_read.outcome.clone()), (2, RunsOutcome::Limited));
    assert!(alpha.runs_read.limits.iter().any(|l| l.starts_with("2 recorded runs of this project name a conversation placed under another project")), "{:?}", alpha.runs_read.limits);
    let beta = project(&read, "/w/beta");
    assert_eq!(beta.runs_read.outcome, RunsOutcome::NotRead { reason: NOT_OPEN_RUNS.into() });
    assert_eq!(entries(&read).count(), 2);
}

#[test]
fn runs_join_their_conversation_with_each_lifecycle_state() {
    let mut g = empty();
    g.current_root = Some("/w/alpha".into());
    g.folders = vec![attached("/w/alpha", "P")];
    g.held = held(vec![
        run("run:open", "t-open", RecordedLifecycle::OpenInterrupted, "2026-11-02T00:00:00Z"),
        run("run:older", "t-open", RecordedLifecycle::Ended { stopped_by: "the person".into(), cause: "ended to start review-pack".into() }, "2026-11-01T00:00:00Z"),
        run("run:ended", "t-ended", RecordedLifecycle::Ended { stopped_by: "the person".into(), cause: "completed".into() }, "2026-11-01T00:00:00Z"),
        run("run:unconfirmed", "t-unconfirmed", RecordedLifecycle::StartNotConfirmed, "2026-11-01T00:00:00Z"),
        run("run:unknown", "t-unknown", RecordedLifecycle::Unknown("conflicting run_opened/run_ended entries".into()), "2026-11-01T00:00:00Z"),
        run("run:held-busy", "t-busy", RecordedLifecycle::OpenInterrupted, "2026-11-01T00:00:00Z"),
        run("run:earlier-session", "t-earlier", RecordedLifecycle::OpenInterrupted, "2026-11-01T00:00:00Z"),
        run("run:no-report", "t-no-report", RecordedLifecycle::OpenInterrupted, "2026-11-01T00:00:00Z"),
    ]);
    let threads = ["t-open", "t-ended", "t-unconfirmed", "t-unknown", "t-busy", "t-earlier", "t-no-report", "t-none"];
    g.homes = vec![account(threads.iter().enumerate().map(|(i, t)| thread(t, "/w/alpha", i as i64 + 1)).collect(), vec![])];
    // The App's ledger names each conversation in the account home only.
    g.index = threads.iter().map(|t| index("account", t, "/w/alpha", &[])).collect();
    g.finished = vec![("run:open".into(), Some(true)), ("run:no-report".into(), Some(false)), ("run:held-busy".into(), None)];
    let read = compose(g);
    let open = entry(&read, "t-open");
    let latest = open.run.as_ref().unwrap();
    assert_eq!((latest.run_id.as_str(), latest.state, latest.finished_reported, open.run_count), ("run:open", RunState::Open, Some(true), 2));
    assert_eq!((latest.ended_by.clone(), latest.result_count, latest.state_reason.clone()), (None, None, None));
    assert_eq!(latest.workflow, RunWorkflow { name: Some("review-pack".into()), title: None, origin: Some("project library".into()), release: None });
    let ended = entry(&read, "t-ended").run.clone().unwrap();
    assert_eq!((ended.state, ended.ended_by, ended.finished_reported), (RunState::Ended, Some(EndedBy { stopped_by: "the person".into(), cause: "completed".into() }), None));
    assert_eq!(entry(&read, "t-unconfirmed").run.as_ref().unwrap().state, RunState::StartNotConfirmed);
    let unknown = entry(&read, "t-unknown").run.clone().unwrap();
    assert_eq!((unknown.state, unknown.state_reason.as_deref()), (RunState::Unknown, Some("conflicting run_opened/run_ended entries")), "point 13");
    assert_eq!(entry(&read, "t-busy").run.as_ref().unwrap().finished_reported, None, "operation pending");
    assert_eq!(entry(&read, "t-earlier").run.as_ref().unwrap().finished_reported, None, "not held live here");
    assert_eq!(entry(&read, "t-no-report").run.as_ref().unwrap().finished_reported, Some(false));
    let none = entry(&read, "t-none");
    assert_eq!((none.run.clone(), none.run_count, none.children_running), (None, 0, None));
}

// Point 4: a thread id shared by two homes keeps each home's runs apart.
#[test]
fn a_thread_id_in_two_homes_keeps_each_homes_runs_apart() {
    let mut g = empty();
    g.current_root = Some("/w/alpha".into());
    g.folders = vec![attached("/w/alpha", "P")];
    g.held = held(vec![
        run("run:key", "shared", RecordedLifecycle::OpenInterrupted, "2026-11-02T00:00:00Z"),
        run("run:account", "shared", RecordedLifecycle::Ended { stopped_by: "the person".into(), cause: "completed".into() }, "2026-11-01T00:00:00Z"),
    ]);
    g.homes = vec![account(vec![thread("shared", "/w/alpha", 1)], vec![]), home("api-key", vec![], vec![])];
    g.index = vec![index("api-key", "shared", "/w/alpha", &["run:key"]), index("account", "shared", "/w/alpha", &["run:account"])];
    let read = compose(g);
    let on_account = entry_in(&read, "account", "shared");
    assert_eq!((on_account.run.as_ref().unwrap().run_id.as_str(), on_account.run_count), ("run:account", 1));
    let on_key = entry_in(&read, "api-key", "shared");
    assert_eq!((on_key.run.as_ref().unwrap().run_id.as_str(), on_key.run_count, on_key.live), ("run:key", 1, Live::Unknown), "the other home's run is its own record-only entry");
    // Untagged, a run whose thread is known in two homes is joined to neither.
    let mut g = empty();
    g.current_root = Some("/w/alpha".into());
    g.folders = vec![attached("/w/alpha", "P")];
    g.held = held(vec![run("run:untagged", "shared", RecordedLifecycle::OpenInterrupted, "2026-11-02T00:00:00Z")]);
    g.homes = vec![account(vec![thread("shared", "/w/alpha", 1)], vec![]), home("api-key", vec![thread("shared", "/w/alpha", 2)], vec![])];
    let read = compose(g);
    assert!(entries(&read).filter(|e| e.home.is_some()).all(|e| e.run.is_none()));
    let homeless = entries(&read).find(|e| e.home.is_none()).unwrap();
    assert_eq!((homeless.id.as_str(), homeless.run.as_ref().unwrap().run_id.as_str()), ("shared", "run:untagged"));
}

// Point 5: a run with no conversation is counted, with a limit.
#[test]
fn a_run_naming_no_conversation_is_counted_and_said() {
    let mut g = empty();
    g.current_root = Some("/w/alpha".into());
    let mut lost = run("run:lost", "x", RecordedLifecycle::StartNotConfirmed, "2026-11-01T00:00:00Z");
    lost.conversation = None;
    g.folders = vec![attached("/w/alpha", "P")];
    g.held = held(vec![lost]);
    let read = compose(g);
    let alpha = project(&read, "/w/alpha");
    assert_eq!((alpha.unplaced_runs, alpha.runs_read.outcome.clone()), (1, RunsOutcome::Limited));
    assert!(alpha.runs_read.limits[0].contains("1 recorded run of this project names no conversation"), "{:?}", alpha.runs_read.limits);
    assert!(alpha.entries.is_empty());
}

// Point 6 and E4: the latest run is the latest start, compared as instants,
// including a start known only from its run-start record; a run with no
// readable time counts as older, and is said.
#[test]
fn the_latest_run_is_the_latest_start_by_instant() {
    let mut g = empty();
    g.current_root = Some("/w/alpha".into());
    g.folders = vec![attached("/w/alpha", "P")];
    let mut undated = run("run:undated", "t", RecordedLifecycle::OpenInterrupted, "not a time");
    undated.started_at = None;
    g.held = held(vec![
        run("run:later-start-only", "t", RecordedLifecycle::StartNotConfirmed, "2026-11-03T00:00:00Z"),
        run("run:opened", "t", RecordedLifecycle::OpenInterrupted, "2026-11-02T00:00:00Z"),
        // 10:00 at +02:00 is 08:00Z: earlier than 09:00Z, though it sorts after as text.
        run("run:offset", "u", RecordedLifecycle::Ended { stopped_by: "the person".into(), cause: "completed".into() }, "2026-11-01T10:00:00+02:00"),
        run("run:utc", "u", RecordedLifecycle::OpenInterrupted, "2026-11-01T09:00:00Z"),
        run("run:unparsed", "u", RecordedLifecycle::OpenInterrupted, "2026-11-01 11:00"),
        undated,
    ]);
    g.homes = vec![account(vec![thread("t", "/w/alpha", 1), thread("u", "/w/alpha", 2)], vec![])];
    g.index = vec![index("account", "t", "/w/alpha", &[]), index("account", "u", "/w/alpha", &[])];
    let read = compose(g);
    assert_eq!(entry(&read, "t").run.as_ref().unwrap().run_id, "run:later-start-only");
    assert_eq!((entry(&read, "u").run.as_ref().unwrap().run_id.as_str(), entry(&read, "u").run_count), ("run:utc", 3));
    let alpha = project(&read, "/w/alpha");
    assert_eq!(alpha.runs_read.outcome, RunsOutcome::Limited);
    assert!(alpha.runs_read.limits.iter().any(|l| l.starts_with("2 runs of this project have no start time that can be read")), "{:?}", alpha.runs_read.limits);
    assert_eq!(instant("2026-11-01T10:00:00+02:00"), instant("2026-11-01T08:00:00Z"));
    assert_eq!(instant("2026-11-01T08:00:00.5Z").unwrap() - instant("2026-11-01T08:00:00Z").unwrap(), 500_000_000);
    assert_eq!(instant("1970-01-01T00:00:00Z"), Some(0));
    assert!(instant("2026-13-01T00:00:00Z").is_none() && instant("2026-11-01T00:00:00").is_none());
}

// E1: a run's home comes only from the App's records.
#[test]
fn a_run_whose_home_the_app_does_not_record_joins_no_listed_conversation() {
    let mut g = empty();
    g.current_root = Some("/w/alpha".into());
    g.folders = vec![attached("/w/alpha", "P")];
    g.held = held(vec![run("run:untagged", "only-here", RecordedLifecycle::OpenInterrupted, "2026-11-02T00:00:00Z")]);
    g.homes = vec![account(vec![thread("only-here", "/w/alpha", 1)], vec![])];
    let read = compose(g);
    let listed = entry_in(&read, "account", "only-here");
    assert_eq!((listed.run.clone(), listed.run_count), (None, 0), "the only home that lists the thread is not taken as the run's");
    let homeless = entries(&read).find(|e| e.home.is_none()).unwrap();
    assert_eq!((homeless.id.as_str(), homeless.project_source, homeless.run.as_ref().unwrap().run_id.as_str()), ("only-here", ProjectSource::RunRecord, "run:untagged"));
}

// Point 7: a conversation the App recorded, in neither list nor run record.
#[test]
fn a_recorded_conversation_alone_is_an_entry() {
    let mut g = empty();
    g.current_root = Some("/w/alpha".into());
    g.folders = vec![attached("/w/alpha", "P")];
    g.homes = vec![account(vec![], vec![])];
    g.index = vec![index("account", "remembered", "/w/alpha", &[])];
    let read = compose(g);
    let e = entry(&read, "remembered");
    assert_eq!((e.project_source, e.live, e.home.as_deref(), e.archived, e.run.clone()), (ProjectSource::Recorded, Live::Unknown, Some("account"), None, None));
    assert!(matches!(&e.open, OpenWith::NotOpenable { reason } if reason.contains("App's own record")), "{:?}", e.open);
}

// Point 10 and E3: `current` stays; `open` only where the status gives the
// project as usable.
#[test]
fn the_launched_project_is_open_only_where_its_status_says_so() {
    let launched = |examined: Examined| {
        let mut g = empty();
        g.current_root = Some("/w/alpha".into());
        g.registry = registry(vec![listed("/w/alpha", "P-registry", 0)]);
        g.folders = vec![FolderInput { root: "/w/alpha".into(), examined }];
        compose(g).projects.remove(0)
    };
    let moved = launched(Examined::Attached { project: None, fault: Some("moved".into()), refusal: Some("not attached".into()), resolutions: vec!["adopt".into(), "new-identity".into()], unavailable: None });
    assert_eq!((moved.current, moved.state), (true, ProjectState::Unavailable));
    assert_eq!(moved.notice, Some(ProjectNotice { kind: "moved".into(), message: fault_message("moved"), resolutions: vec!["adopt".into(), "new-identity".into()] }));
    let refused = launched(Examined::Attached { project: Some("P".into()), fault: None, refusal: Some("retention state unavailable".into()), resolutions: vec![], unavailable: None });
    assert_eq!((refused.state, refused.notice.unwrap().kind.as_str()), (ProjectState::Unavailable, "unavailable"));
    let no_store = launched(Examined::Refused("records store not created yet".into()));
    assert_eq!((no_store.current, no_store.state, no_store.project_id.clone()), (true, ProjectState::Unavailable, None), "the launched project takes no identity from the registry");
    assert!(no_store.notice.unwrap().message.contains("records store not created yet"));
    // A disposed identity: an attachment with an identity and no refusal,
    // under `project.state: unavailable`.
    let disposed = examined_from_status(&json!({"state":"available","project":{"state":"unavailable","error":"this project's records were disposed of",
        "reading":"ordinary project records unavailable","attachment":{"projectId":"P","refusal":null,"fault":null,"resolutions":[]}}}));
    assert_eq!(disposed, Examined::Attached { project: Some("P".into()), fault: None, refusal: None, resolutions: vec![], unavailable: Some("this project's records were disposed of".into()) });
    let disposed = launched(disposed);
    assert_eq!((disposed.state, disposed.project_id.as_deref()), (ProjectState::Unavailable, Some("P")));
    assert!(disposed.notice.unwrap().message.contains("disposed of"));
    assert_eq!(examined_from_status(&json!({"state":"unavailable","error":"no store"})), Examined::Refused("no store".into()));
    let open = launched(examined_from_status(&json!({"project":{"attachment":{"projectId":"P","refusal":null,"fault":null}}})));
    assert_eq!((open.state, open.project_id.as_deref(), open.notice), (ProjectState::Open, Some("P"), None));
}

// Point 4: the runs the App holds: the reading as last held, and this
// process's own view of the runs it holds.
#[test]
fn the_launched_projects_runs_are_as_the_app_holds_them() {
    let compose_with = |held: HeldRuns| {
        let mut g = empty();
        g.current_root = Some("/w/alpha".into());
        g.folders = vec![attached("/w/alpha", "P")];
        g.held = held;
        g.homes = vec![account(vec![thread("t", "/w/alpha", 1)], vec![])];
        g.index = vec![index("account", "t", "/w/alpha", &[])];
        compose(g)
    };
    let not_yet = compose_with(HeldRuns::default());
    assert_eq!(project(&not_yet, "/w/alpha").runs_read, RunsRead { outcome: RunsOutcome::NotRead { reason: RUNS_NOT_YET.into() }, read_at: None, limits: vec![] });
    let words = crate::runtime_session::REOPEN_NOT_READ_WORDS[1];
    let not_read = compose_with(HeldRuns { recorded: HeldReading::NotRead(words.into()), process: vec![] });
    assert_eq!(project(&not_read, "/w/alpha").runs_read.outcome, RunsOutcome::NotRead { reason: words.into() });

    // The routing changed while the reading read: none of its runs, but this
    // process's own still.
    let mut own = run("run:own", "t", RecordedLifecycle::OpenInterrupted, "2026-11-03T00:00:00Z");
    own.home = Some("account".into());
    let changed = compose_with(HeldRuns {
        recorded: HeldReading::Read { read_at: Some("2026-11-18T09:00:00.000Z".into()), limits: vec![], notices: vec![crate::records_store::HISTORY_CHANGED_VIEW.into()],
            runs: vec![run("run:recorded", "t", RecordedLifecycle::OpenInterrupted, "2026-11-02T00:00:00Z")] },
        process: vec![own.clone()],
    });
    let alpha = project(&changed, "/w/alpha");
    assert_eq!(alpha.runs_read.outcome, RunsOutcome::NotRead { reason: crate::records_store::HISTORY_CHANGED_VIEW.into() });
    assert_eq!((entry(&changed, "t").run.as_ref().unwrap().run_id.as_str(), entry(&changed, "t").run_count), ("run:own", 1));

    // A reading with limits is limited, with when it began; a run the process
    // holds is one run, its state as the process holds it (here ended in this
    // session, which stays held as ended).
    let mut ended = run("run:recorded", "t", RecordedLifecycle::Ended { stopped_by: "the person".into(), cause: "completed".into() }, "2026-11-04T00:00:00Z");
    ended.home = Some("account".into());
    let mut busy = run("run:busy", "t", RecordedLifecycle::Unknown(RUN_PENDING.into()), "x");
    (busy.started_at, busy.workflow, busy.home) = (None, Value::Null, Some("account".into()));
    let limited = compose_with(HeldRuns {
        recorded: HeldReading::Read { read_at: Some("2026-11-18T09:00:00.000Z".into()), limits: vec!["WR records unreadable: invented".into()], notices: vec![crate::records_store::HISTORY_UNIMPORTED_VIEW.into()],
            runs: vec![run("run:recorded", "t", RecordedLifecycle::OpenInterrupted, "2026-11-02T00:00:00Z"), run("run:busy", "t", RecordedLifecycle::OpenInterrupted, "2026-11-01T00:00:00Z")] },
        process: vec![ended, busy],
    });
    let alpha = project(&limited, "/w/alpha");
    assert_eq!((alpha.runs_read.outcome.clone(), alpha.runs_read.read_at.as_deref()), (RunsOutcome::Limited, Some("2026-11-18T09:00:00.000Z")));
    assert_eq!(alpha.runs_read.limits, vec!["WR records unreadable: invented".to_owned(), crate::records_store::HISTORY_UNIMPORTED_VIEW.into()]);
    let t = entry(&limited, "t");
    let latest = t.run.as_ref().unwrap();
    assert_eq!((latest.run_id.as_str(), latest.state, t.run_count), ("run:recorded", RunState::Ended, 2));
    assert_eq!(latest.ended_by, Some(EndedBy { stopped_by: "the person".into(), cause: "completed".into() }));
}

#[test]
fn workflow_origin_and_release_as_the_run_guide_words_them() {
    let catalog = CatalogInput {
        identities: vec![json!({"kind":"workflow","origin":"bundled","source_root":"chirality-library@library-v3.4.0","name":"review-pack","revision":"r1","revision_method":"m"})],
        release: release_words(&json!({"tag":"library-v3.4.0"})),
    };
    let included = json!({"kind":"workflow","origin":"bundled","sourceRoot":"chirality-library@library-v3.4.0","name":"review-pack","revision":"r1"});
    assert_eq!(workflow_words(&included, &catalog), RunWorkflow { name: Some("review-pack".into()), title: None, origin: Some("included with the App".into()), release: Some("Chirality Library 3.4.0".into()) });
    let mut copy = included.clone();
    copy["revision"] = json!("r0");
    assert_eq!(workflow_words(&copy, &catalog).origin.as_deref(), Some("a bundled copy (source chirality-library@library-v3.4.0)"));
    assert_eq!(workflow_words(&copy, &catalog).release, None);
    assert_eq!(workflow_words(&json!({"origin":"user","name":"x"}), &catalog).origin.as_deref(), Some("user library"));
    assert_eq!(release_words(&json!({"tag":"main"})).as_deref(), Some("Chirality Library (main)"));
    assert_eq!(release_words(&json!({})), None);
}

#[test]
fn live_and_open_come_from_what_the_host_holds() {
    let mut g = empty();
    g.current_root = Some("/w/alpha".into());
    g.folders = vec![attached("/w/alpha", "P")];
    g.homes = vec![account(vec![thread("loaded", "/w/alpha", 2), thread("listed", "/w/alpha", 1)], vec![
        json!({"generation":generation(),"threadId":"loaded","name":"Working","status":{"type":"active","activeFlags":["waitingOnApproval"]},"cwd":"/w/alpha"}),
        json!({"generation":{"appSession":"session:invented","home":HOME,"spawnCounter":0},"threadId":"listed","status":{"type":"active"}}),
    ])];
    let read = compose(g);
    let loaded = entry(&read, "loaded");
    assert_eq!((loaded.live, loaded.title.as_deref(), loaded.archived), (Live::Running, Some("Working"), Some(false)));
    assert_eq!(loaded.open, OpenWith::Loaded { generation: generation(), thread_id: "loaded".into() });
    let listed = entry(&read, "listed");
    assert_eq!(listed.live, Live::NotLoaded, "an earlier generation's row is not this generation's report");
    assert_eq!(listed.open, OpenWith::History { home: "account".into(), generation: generation(), selection_epoch: 3, thread_id: "listed".into() });
    assert_eq!(live(&json!({"type":"idle"})), Live::Idle);
    assert_eq!(live(&json!({"type":"systemError"})), Live::Unknown);
    assert_eq!(live(&Value::Null), Live::Unknown);

    // A home whose Codex ended: what it last held is not shown as current.
    let mut g = empty();
    let mut ended = account(vec![thread("gone-codex", "/data/conversations-without-project", 1)], vec![]);
    ended.current = false;
    g.homes = vec![ended];
    assert!(compose(g).unassigned.is_empty());
}

// Point 16: own and descendants' requests on the root entry, and those that
// reach no entry.
#[test]
fn requests_count_on_their_root_conversation_and_children_are_no_entries() {
    let mut g = empty();
    g.current_root = Some("/w/alpha".into());
    g.folders = vec![attached("/w/alpha", "P")];
    let mut h = account(vec![thread("root", "/w/alpha", 3), thread("listed-child", "/w/alpha", 2)], vec![loaded_row("root", "/w/alpha")]);
    // `listed-child` has no parentThreadId in the list; the native view names its parent.
    h.descendants = vec![("child".into(), "root".into()), ("grandchild".into(), "child".into()), ("listed-child".into(), "root".into()), ("orphan".into(), "nowhere".into())];
    h.waiting = vec![(Some("root".into()), 1), (Some("grandchild".into()), 2), (Some("orphan".into()), 1), (None, 1)];
    g.homes = vec![h];
    let read = compose(g);
    let root = entry(&read, "root");
    assert_eq!(root.needs_answer, 3);
    assert_eq!(root.needs_answer_on, vec![RequestsOn { thread_id: "root".into(), count: 1 }, RequestsOn { thread_id: "grandchild".into(), count: 2 }]);
    assert!(entries(&read).all(|e| e.id != "listed-child"), "a child named by the native view is no entry");
    assert_eq!(read.unplaced_requests, vec![
        UnplacedRequests { home: "account".into(), thread_id: Some("orphan".into()), count: 1 },
        UnplacedRequests { home: "account".into(), thread_id: None, count: 1 },
    ]);
}

#[test]
fn the_shape_serializes_as_agreed() {
    let mut g = empty();
    g.current_root = Some("/w/alpha".into());
    g.folders = vec![FolderInput { root: "/w/alpha".into(), examined: Examined::Gone }];
    g.homes = vec![account(vec![thread("t", "/w/alpha", 1)], vec![])];
    let value = serde_json::to_value(compose(g)).unwrap();
    assert_eq!(value["readAt"], "2026-11-19T00:00:00.000Z");
    assert_eq!(value["conversations"][0], json!({"home":"account","list":LIST_WORDS,"readAt":null,"state":"read"}));
    assert_eq!(value["unplacedRequests"], json!([]));
    let p = &value["projects"][0];
    assert_eq!((p["state"].clone(), p["notice"]["kind"].clone(), p["runsRead"]["state"].clone(), p["unplacedRuns"].clone()), (json!("unavailable"), json!("gone"), json!("not-read"), json!(0)));
    let e = &p["entries"][0];
    for key in ["id", "home", "projectRoot", "projectSource", "title", "titleSource", "createdAt", "updatedAt", "live", "needsAnswer", "needsAnswerOn", "archived", "open", "run", "runCount", "childrenRunning"] {
        assert!(e.get(key).is_some(), "entry lacks {key}: {e}");
    }
    assert_eq!((e["projectSource"].clone(), e["titleSource"].clone(), e["live"].clone(), e["archived"].clone()), (json!("reported-folder"), json!("preview"), json!("not-loaded"), json!(false)));
    assert_eq!(e["open"], json!({"kind":"history","home":"account","generation":generation(),"selectionEpoch":3,"threadId":"t"}));
    assert_eq!(serde_json::to_value(OpenWith::NotOpenable { reason: "why".into() }).unwrap(), json!({"kind":"not-openable","reason":"why"}));
    assert_eq!(serde_json::to_value(RunsRead { outcome: RunsOutcome::Limited, read_at: Some("t".into()), limits: vec!["x".into()] }).unwrap(), json!({"state":"limited","readAt":"t","limits":["x"]}));
    assert_eq!(p["runsRead"]["readAt"], Value::Null);
    let run = serde_json::to_value(entry_run(&run("r", "t", RecordedLifecycle::Unknown("why".into()), "x"), &BTreeMap::new(), &CatalogInput::default())).unwrap();
    assert_eq!((run["state"].clone(), run["stateReason"].clone()), (json!("unknown"), json!("why")));
    for key in ["runId", "workflow", "endedBy", "finishedReported", "resultCount"] { assert!(run.get(key).is_some(), "run lacks {key}"); }
}

// ---- A real records store, read as the command reads it ----

fn folder(base: &Path, rel: &str) -> PathBuf {
    let p = base.join(rel);
    std::fs::create_dir_all(&p).unwrap();
    p
}
/// Every entry below `root`: its bytes (None for a folder; a symlink's
/// target), length and modification time, so a rewrite with the same bytes
/// shows too.
type Tree = BTreeMap<PathBuf, (Option<Vec<u8>>, u64, Option<std::time::SystemTime>)>;
fn tree(root: &Path) -> Tree {
    let mut out = BTreeMap::new();
    let mut stack = vec![root.to_path_buf()];
    while let Some(dir) = stack.pop() {
        for item in std::fs::read_dir(&dir).unwrap() {
            let path = item.unwrap().path();
            let meta = std::fs::symlink_metadata(&path).unwrap();
            let bytes = if meta.file_type().is_symlink() {
                Some(std::fs::read_link(&path).unwrap().into_os_string().into_encoded_bytes())
            } else if meta.is_dir() { stack.push(path.clone()); None } else { Some(std::fs::read(&path).unwrap()) };
            out.insert(path.strip_prefix(root).unwrap().to_path_buf(), (bytes, meta.len(), meta.modified().ok()));
        }
    }
    out
}
struct Fixture { store: PathBuf, base: PathBuf }
impl Fixture {
    fn new(prefix: &str) -> Self {
        let temp = std::fs::canonicalize(std::env::temp_dir()).unwrap();
        let store = temp.join(crate::util::opaque_id(&format!("{prefix}-store-")).unwrap());
        let base = temp.join(crate::util::opaque_id(&format!("{prefix}-projects-")).unwrap());
        std::fs::create_dir_all(&base).unwrap();
        crate::records_store::use_store_for_test(Some(Ok(crate::records_store::Store { root: store.clone(), placement: crate::records_store::Placement::Override, limits: vec![] })));
        Fixture { store, base }
    }
    fn trees(&self) -> (Tree, Tree) {
        (tree(&self.store), tree(&self.base))
    }
}
impl Drop for Fixture {
    fn drop(&mut self) {
        crate::records_store::use_store_for_test(None);
        let _ = std::fs::remove_dir_all(&self.store);
        let _ = std::fs::remove_dir_all(&self.base);
    }
}
fn open_run(root: &Path, run: &str, conversation: &str) {
    let body = json!({"runId":run,"startedBy":{"kind":"person"},"surface":"App run",
        "workflow":{"kind":"workflow","origin":"project","sourceRoot":"/invented/library","name":"review-pack","revision":"rev-invented","revisionVerification":"verified"},
        "conversationRef":conversation});
    let mut opened = crate::records::supply::PendingRunEntry::new("run_opened", body, crate::util::now_rfc3339()).unwrap();
    crate::records::supply::append_run_entry(root, run, &mut opened).unwrap();
}
/// The App's start as the store sees it: what earlier attachments remembered
/// is forgotten and the store is opened again, as at launch.
fn as_at_launch() {
    crate::records_store::restore_configured_for_test(crate::records_store::configured_for_test());
    crate::records_store::opened_existing().unwrap();
}
fn read_as_command(launched: &Path, homes: Vec<std::sync::Arc<crate::runtime_session::HomeSession>>, workflows: &std::sync::Mutex<crate::runtime_session::WorkflowRootSession>, status: &StatusSlot) -> NavigatorRead {
    read_from(Sources { homes, workflows, workspace: Some(launched), app_data: None, status })
}
fn fresh_home() -> std::sync::Arc<crate::runtime_session::HomeSession> {
    let host = std::sync::Arc::new(crate::hosting::Host::new());
    std::sync::Arc::new(crate::runtime_session::HomeSession::new(crate::home_resources::HomeClass::Account, host, Err("invented: no configuration".into())).unwrap())
}
/// The files below `dir`.
fn files(dir: &Path) -> Vec<PathBuf> {
    tree(dir).into_iter().filter(|(_, (bytes, _, _))| bytes.is_some()).map(|(p, _)| dir.join(p)).collect()
}

#[test]
fn the_whole_read_writes_nothing_and_remembers_no_other_folder() {
    let f = Fixture::new("navigator");
    let launched = folder(&f.base, "one/proj");
    let two = folder(&f.base, "two/proj");
    let gone = folder(&f.base, "gone");
    for root in [&launched, &gone] {
        assert_eq!(crate::records_store::attach(root, true).unwrap().how, "minted");
    }
    let two_dir = crate::records_store::attach(&two, true).unwrap().dir.unwrap();
    open_run(&launched, "run:launched", "thread:launched");
    open_run(&two, "run:other", "thread:other");
    std::fs::remove_dir_all(&gone).unwrap();
    as_at_launch();
    // The launch's one reading of the recorded runs, as the App makes it.
    let workflows = std::sync::Mutex::new(crate::runtime_session::WorkflowRootSession::default());
    crate::runtime_session::read_reopened_history(&workflows, &launched, &[], &[]).unwrap();
    let s = |p: &Path| p.to_str().unwrap().to_owned();
    // The second project's actual store log, and the writer-side lookup of its folder.
    let other_log = files(&two_dir).into_iter().find(|p| std::fs::read_to_string(p).is_ok_and(|t| t.contains("run:other"))).expect("the second project's run log");
    assert_eq!(crate::records_store::configured_project_dir(&other_log).as_deref(), Some(two_dir.as_path()));
    assert_eq!(crate::records_store::root_for_dir(&two_dir), None, "the other project is not remembered at launch");

    let status = StatusSlot::default();
    let was = f.trees();
    let read = read_as_command(&launched, vec![fresh_home()], &workflows, &status);
    assert_eq!(f.trees(), was, "the read wrote, created or touched nothing in the store or the projects");
    assert_eq!(crate::records_store::root_for_dir(&two_dir), None, "the read remembered the other project's folder for its writers");
    assert!(!crate::records_store::known_project_root(&two));

    let current = &read.projects[0];
    assert_eq!((current.root.clone(), current.current, current.state, current.notice.clone()), (s(&launched), true, ProjectState::Open, None));
    assert_eq!(current.runs_read.outcome, RunsOutcome::Read);
    assert!(current.runs_read.read_at.is_some());
    let run_entry = &current.entries[0];
    assert_eq!((run_entry.id.as_str(), run_entry.project_source, run_entry.run.as_ref().unwrap().state), ("thread:launched", ProjectSource::RunRecord, RunState::Open));
    let second = project(&read, &s(&two));
    assert_eq!((second.label.as_str(), second.state, second.notice.clone()), ("two/proj", ProjectState::Listed, None));
    assert!(second.project_id.is_some(), "the registry's identity");
    assert_eq!(second.runs_read.outcome, RunsOutcome::NotRead { reason: NOT_OPEN_RUNS.into() });
    assert!(second.entries.is_empty(), "the other project's runs are not read");
    assert_eq!(current.label, "one/proj");
    let gone_project = project(&read, &s(&gone));
    assert_eq!((gone_project.state, gone_project.notice.as_ref().unwrap().kind.as_str()), (ProjectState::Unavailable, "gone"));
    assert_eq!(read.conversations[0].outcome, ReadOutcome::NotRead { reason: "Codex is not running for this home, so its conversations were not read.".into() });

    // The registry's last line torn: read to its last complete line, and said.
    let roots = f.store.join("roots.jsonl");
    let mut bytes = std::fs::read(&roots).unwrap();
    bytes.extend_from_slice(b"{\"format\":\"chirality.records-store.root\",\"projectId\":");
    std::fs::write(&roots, &bytes).unwrap();
    let was = f.trees();
    let listing = crate::storage::without_mutations_for_test(|| crate::records_store::listed_folders()).unwrap();
    assert!(listing.torn.is_some());
    let read = read_as_command(&launched, vec![], &workflows, &status);
    assert_eq!(f.trees(), was, "nothing written beside a torn registry either");
    assert_eq!(read.projects.len(), 3, "the complete lines still list every folder");
    assert!(read.registry_limits.iter().any(|l| l.contains("roots.jsonl")), "{:?}", read.registry_limits);
    assert_eq!(crate::records_store::root_for_dir(&two_dir), None);
}

// Point 2: the attachment shown is host status's own observation while it is
// fresh; only a stale or missing one makes the navigator take the status.
#[test]
fn the_attachment_shown_is_host_statuss_last_observation() {
    let f = Fixture::new("navigator-status");
    let launched = folder(&f.base, "proj");
    crate::records_store::attach(&launched, true).unwrap();
    as_at_launch();
    let workflows = std::sync::Mutex::new(crate::runtime_session::WorkflowRootSession::default());
    let kept = json!({"state":"available","project":{"attachment":{"projectId":"P-kept","refusal":null,"fault":null}}});
    let status = StatusSlot::default();
    status.keep(Some(&launched), &kept);
    assert_eq!(read_as_command(&launched, vec![], &workflows, &status).projects[0].project_id.as_deref(), Some("P-kept"));
    let stale = std::time::Instant::now().checked_sub(STATUS_FRESH + std::time::Duration::from_secs(1)).unwrap();
    status.keep_at(Some(&launched), &kept, stale);
    let read = read_as_command(&launched, vec![], &workflows, &status);
    let taken = crate::records_store::status(Some(&launched));
    assert_eq!(read.projects[0].project_id.as_deref(), taken["project"]["attachment"]["projectId"].as_str(), "a stale observation is taken again, exactly as host status takes it");
    assert_ne!(read.projects[0].project_id.as_deref(), Some("P-kept"));
    // Kept for another workspace: not this one's.
    status.keep(Some(&f.base), &kept);
    assert_ne!(read_as_command(&launched, vec![], &workflows, &status).projects[0].project_id.as_deref(), Some("P-kept"));
    drop(f);
}

// Point 1 and B1: the workspace goes to the store exactly as given. Given
// through a symlink to another registered folder, the launched project
// carries host status's refusal for that path and the other folder is not
// remembered.
#[test]
fn a_launched_path_through_a_symlink_carries_host_statuss_answer_for_that_path() {
    let f = Fixture::new("navigator-symlink");
    let other = folder(&f.base, "other");
    let other_dir = crate::records_store::attach(&other, true).unwrap().dir.unwrap();
    let link = f.base.join("launched");
    std::os::unix::fs::symlink(&other, &link).unwrap();
    as_at_launch();
    let workflows = std::sync::Mutex::new(crate::runtime_session::WorkflowRootSession::default());
    let host_status = crate::records_store::status(Some(&link));
    let expected = examined_from_status(&host_status);
    assert!(!matches!(expected, Examined::Attached { refusal: None, fault: None, unavailable: None, project: Some(_), .. }), "the store refuses a symlinked folder: {host_status}");
    let was = f.trees();
    let read = read_as_command(&link, vec![], &workflows, &StatusSlot::default());
    assert_eq!(f.trees(), was);
    let current = read.projects.iter().find(|p| p.current).unwrap();
    let section_alone = {
        let mut g = empty();
        g.current_root = Some(current.root.clone());
        g.folders = vec![FolderInput { root: current.root.clone(), examined: expected }];
        compose(g).projects.remove(0)
    };
    assert_eq!((current.state, current.notice.clone(), current.project_id.clone()), (ProjectState::Unavailable, section_alone.notice, None));
    assert_eq!(crate::records_store::root_for_dir(&other_dir), None, "the other folder was not remembered");
    assert!(!crate::records_store::known_project_root(&other));
    drop(f);
}

#[test]
fn without_a_store_the_launched_project_is_still_shown() {
    let temp = std::fs::canonicalize(std::env::temp_dir()).unwrap();
    let missing = temp.join(crate::util::opaque_id("navigator-no-store-").unwrap()).join("absent");
    let base = temp.join(crate::util::opaque_id("navigator-launched-").unwrap());
    std::fs::create_dir_all(&base).unwrap();
    crate::records_store::use_store_not_started_for_test(Some(Ok(crate::records_store::Store { root: missing.clone(), placement: crate::records_store::Placement::Override, limits: vec![] })));
    let workflows = std::sync::Mutex::new(crate::runtime_session::WorkflowRootSession::default());
    let was = tree(&base);
    let read = read_as_command(&base, vec![], &workflows, &StatusSlot::default());
    assert_eq!(tree(&base), was);
    assert!(!missing.exists(), "no store was created");
    assert_eq!(read.projects.len(), 1);
    assert_eq!((read.projects[0].current, read.projects[0].state), (true, ProjectState::Unavailable));
    assert!(read.registry_limits[0].contains("not read") && read.registry_limits[0].contains("supplied no project folders"), "{:?}", read.registry_limits);
    assert_eq!(read.projects[0].runs_read.outcome, RunsOutcome::NotRead { reason: RUNS_NOT_YET.into() });
    crate::records_store::use_store_for_test(None);
    let _ = std::fs::remove_dir_all(&base);
}

/// The navigator makes no reading of the store's records: it names none of
/// their readers, and its only calls into the store are the registry listing
/// and the one status fallback.
#[test]
fn the_navigator_names_no_reader_of_the_stores_records() {
    let source = include_str!("navigator_read.rs");
    for reader in ["ProjectRecords::open", "read_project_runs", "HistoryRead", "storage::read_all", "attach("] {
        assert!(!source.contains(reader), "navigator_read.rs names {reader}");
    }
    let mut calls = Vec::new();
    for (at, _) in source.match_indices("records_store::") {
        let rest = &source[at + "records_store::".len()..];
        let name: String = rest.chars().take_while(|c| c.is_alphanumeric() || *c == '_').collect();
        if rest[name.len()..].starts_with('(') { calls.push(name); }
    }
    calls.sort();
    assert_eq!(calls, ["listed_folders", "status"], "{calls:?}");
}
