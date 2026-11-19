//! The navigator's read, with invented material only: placement, ordering,
//! titles, the not-read cases, runs joined to their conversations, waiting
//! requests, and a real records store (moved, gone, torn, a label clash)
//! read without writing anything.
use super::*;
use serde_json::json;

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
        homes: vec![],
        index: vec![],
        finished: vec![],
        catalog: CatalogInput::default(),
    }
}
fn listed(root: &str, id: &str, line: usize) -> crate::records_store::ListedFolder {
    crate::records_store::ListedFolder { root: root.into(), identities: vec![id.into()], first_line: line }
}
fn attached(root: &str, id: &str, runs: Vec<RunInput>) -> FolderInput {
    FolderInput {
        root: root.into(),
        examined: Examined::Attached { project: Some(id.into()), fault: None, refusal: None, resolutions: vec![] },
        runs: RunsInput::Read { runs, limits: vec![] },
    }
}
/// A ready account home whose list was read to its end.
fn home(threads: Vec<Value>, loaded: Vec<Value>) -> HomeInput {
    HomeInput {
        class: "account".into(),
        state: "ready".into(),
        generation: generation(),
        current: true,
        loaded,
        history: Some(HistoryInput { generation: generation(), selection_epoch: 3, threads, read_at_ready: Some(json!({"generation":generation(),"state":"read-to-end"})) }),
        waiting: vec![],
    }
}
fn thread(id: &str, cwd: &str, updated: i64) -> Value {
    json!({"id":id,"cwd":cwd,"name":null,"preview":format!("first message of {id}"),"createdAt":updated - 100,"updatedAt":updated,"status":{"type":"notLoaded"},"parentThreadId":null})
}
fn run(id: &str, conversation: &str, lifecycle: RecordedLifecycle, at: &str) -> RunInput {
    RunInput {
        run_id: id.into(),
        conversation: Some(conversation.into()),
        workflow: json!({"kind":"workflow","origin":"project","sourceRoot":"/p/library","name":"review-pack","revision":"rev-1"}),
        lifecycle,
        recorded_at: Some(at.into()),
    }
}
fn project<'a>(read: &'a NavigatorRead, root: &str) -> &'a NavigatorProject {
    read.projects.iter().find(|p| p.root == root).unwrap_or_else(|| panic!("no project {root} in {:#?}", read.projects))
}
fn entry<'a>(read: &'a NavigatorRead, id: &str) -> &'a NavigatorEntry {
    read.projects.iter().flat_map(|p| &p.entries).chain(&read.unassigned).find(|e| e.id == id).unwrap_or_else(|| panic!("no entry {id}"))
}

#[test]
fn placement_by_record_then_reported_folder_then_unassigned_then_a_folder_section() {
    let mut g = empty();
    g.current_root = Some("/work/alpha".into());
    g.registry = Ok(crate::records_store::ListedFolders { folders: vec![listed("/work/alpha", "P-alpha", 0), listed("/work/beta", "P-beta", 1)], ..Default::default() });
    g.folders = vec![attached("/work/alpha", "P-alpha", vec![]), attached("/work/beta", "P-beta", vec![])];
    let mut child = thread("child", "/work/alpha", 50);
    child["parentThreadId"] = json!("by-folder");
    g.homes = vec![home(vec![
        // Codex reports beta's folder, the App recorded alpha: the record governs.
        thread("recorded", "/work/beta", 10),
        thread("by-folder", "/work/beta", 20),
        thread("no-project", "/data/conversations-without-project", 30),
        thread("elsewhere", "/somewhere/else", 40),
        child,
    ], vec![])];
    g.index = vec![IndexRow { home: "account".into(), thread: "recorded".into(), project: "/work/alpha".into() }];
    let read = compose(g);

    let recorded = entry(&read, "recorded");
    assert_eq!((recorded.project_root.as_deref(), recorded.project_source), (Some("/work/alpha"), ProjectSource::Recorded));
    assert!(project(&read, "/work/alpha").entries.iter().any(|e| e.id == "recorded"));
    let by_folder = entry(&read, "by-folder");
    assert_eq!((by_folder.project_root.as_deref(), by_folder.project_source), (Some("/work/beta"), ProjectSource::ReportedFolder));
    assert_eq!(read.unassigned.iter().map(|e| e.id.as_str()).collect::<Vec<_>>(), ["no-project"]);
    assert_eq!(read.unassigned[0].project_source, ProjectSource::ReportedFolder);
    let section = project(&read, "/somewhere/else");
    assert_eq!((section.project_id.as_deref(), section.state, section.current), (None, ProjectState::Listed, false));
    assert_eq!(section.notice.as_ref().unwrap().kind, "no-identity");
    assert!(matches!(section.runs_read.outcome, ReadOutcome::NotRead { .. }));
    assert_eq!(section.entries[0].id, "elsewhere");
    assert!(read.projects.iter().flat_map(|p| &p.entries).chain(&read.unassigned).all(|e| e.id != "child"), "a delegated child is no entry");
    assert_eq!(read.conversations, vec![ConversationsRead { home: "account".into(), outcome: ReadOutcome::Read }]);
}

#[test]
fn a_recorded_reference_spelled_as_launched_names_the_physical_root() {
    let mut g = empty();
    g.current_root = Some("/private/work/alpha".into());
    g.aliases = vec![("/work/alpha".into(), "/private/work/alpha".into())];
    g.folders = vec![attached("/private/work/alpha", "P-alpha", vec![])];
    g.homes = vec![home(vec![thread("t", "/other", 1)], vec![])];
    g.index = vec![IndexRow { home: "account".into(), thread: "t".into(), project: "/work/alpha".into() }];
    let read = compose(g);
    assert_eq!(read.projects.len(), 1);
    assert_eq!(entry(&read, "t").project_root.as_deref(), Some("/private/work/alpha"));
}

#[test]
fn ordering_current_first_then_newest_entry_then_registry_order() {
    let mut g = empty();
    g.current_root = Some("/w/current".into());
    g.registry = Ok(crate::records_store::ListedFolders {
        folders: vec![listed("/w/current", "P0", 0), listed("/w/quiet-early", "P1", 1), listed("/w/busy", "P2", 2), listed("/w/quiet-late", "P3", 3)],
        ..Default::default()
    });
    g.folders = ["/w/current", "/w/quiet-early", "/w/busy", "/w/quiet-late"].iter().enumerate().map(|(i, r)| attached(r, &format!("P{i}"), vec![])).collect();
    let mut loaded_only = json!({"generation":generation(),"threadId":"loaded-only","name":"No list row","status":{"type":"idle"},"cwd":"/w/busy"});
    loaded_only["preview"] = json!(null);
    g.homes = vec![home(vec![thread("old", "/w/busy", 100), thread("new", "/w/busy", 300), thread("mid", "/w/current", 200)], vec![loaded_only])];
    let read = compose(g);
    let roots: Vec<&str> = read.projects.iter().map(|p| p.root.as_str()).collect();
    assert_eq!(roots, ["/w/current", "/w/busy", "/w/quiet-early", "/w/quiet-late"]);
    assert!(read.projects[0].current && read.projects[1..].iter().all(|p| !p.current));
    assert_eq!(read.projects[0].state, ProjectState::Open);
    assert_eq!(read.projects[2].state, ProjectState::Listed);
    let busy: Vec<&str> = project(&read, "/w/busy").entries.iter().map(|e| e.id.as_str()).collect();
    assert_eq!(busy, ["new", "old", "loaded-only"], "newest first; no updatedAt last");
    let new = entry(&read, "new");
    assert_eq!(new.updated_at.as_deref(), Some("1970-01-01T00:05:00.000Z"));
    assert_eq!(new.created_at.as_deref(), Some("1970-01-01T00:03:20.000Z"));
    assert_eq!(entry(&read, "loaded-only").updated_at, None);
}

#[test]
fn titles_from_name_then_first_message_cut_on_a_word_then_none() {
    assert_eq!(title(Some("  Named  "), Some("preview")), (Some("Named".into()), TitleSource::Name));
    assert_eq!(title(Some(" "), Some("Short\n first   message")), (Some("Short first message".into()), TitleSource::FirstMessage));
    // 58 characters, a space, then a word that crosses the 60th character.
    let long = format!("{} {}", "a".repeat(58), "overflowing words follow");
    let (cut, source) = title(None, Some(&long));
    assert_eq!((cut.as_deref(), source), (Some("a".repeat(58).as_str()), TitleSource::FirstMessage));
    // A boundary exactly at 60 characters keeps all 60.
    let exact = format!("{} next", "b".repeat(60));
    assert_eq!(title(None, Some(&exact)).0.unwrap(), "b".repeat(60));
    // One word longer than the limit is cut at the limit; characters, not bytes.
    let word = "é".repeat(70);
    assert_eq!(title(None, Some(&word)).0.unwrap().chars().count(), TITLE_CHARS);
    assert_eq!(title(None, Some("   ")), (None, TitleSource::None));
    assert_eq!(title(None, None), (None, TitleSource::None));

    let mut g = empty();
    let mut unnamed = thread("unnamed", "/data/conversations-without-project", 1);
    unnamed["preview"] = json!(null);
    g.homes = vec![home(vec![unnamed], vec![])];
    let read = compose(g);
    assert_eq!((read.unassigned[0].title.clone(), read.unassigned[0].title_source), (None, TitleSource::None));
}

#[test]
fn conversations_not_read_still_return_projects_and_run_record_entries() {
    let mut g = empty();
    g.current_root = Some("/w/alpha".into());
    g.folders = vec![attached("/w/alpha", "P-alpha", vec![run("run:1", "thread:recorded-run", RecordedLifecycle::OpenInterrupted, "2026-11-01T00:00:00Z")])];
    let mut stopped = home(vec![], vec![]);
    stopped.state = "absent".into();
    stopped.current = false;
    stopped.history = None;
    let mut key = home(vec![], vec![]);
    key.class = "api-key".into();
    key.history.as_mut().unwrap().read_at_ready = None;
    let mut cut = home(vec![], vec![]);
    cut.class = "local-provider".into();
    cut.history.as_mut().unwrap().read_at_ready = Some(json!({"generation":generation(),"state":"stopped","reason":"Codex did not answer the history list read in time"}));
    g.homes = vec![stopped, key, cut];
    let read = compose(g);
    let reasons: Vec<String> = read.conversations.iter().map(|c| match &c.outcome { ReadOutcome::NotRead { reason } => reason.clone(), ReadOutcome::Read => panic!("{} read", c.home) }).collect();
    assert!(reasons[0].contains("not running"), "{reasons:?}");
    assert!(reasons[1].contains("whole list"), "{reasons:?}");
    assert!(reasons[2].contains("not read to its end") && reasons[2].contains("did not answer"), "{reasons:?}");
    let alpha = project(&read, "/w/alpha");
    assert_eq!(alpha.runs_read.outcome, ReadOutcome::Read);
    let only = &alpha.entries[0];
    assert_eq!((only.id.as_str(), only.live, only.project_source, only.home.as_deref()), ("thread:recorded-run", Live::Unknown, ProjectSource::RunRecord, None));
    assert!(matches!(&only.open, OpenWith::NotOpenable { reason } if reason.contains("run record")));
    assert_eq!(only.run.as_ref().unwrap().state, RunState::Open);
    assert_eq!(only.run_count, 1);
}

#[test]
fn a_run_record_entry_takes_the_home_and_project_the_app_recorded() {
    let mut g = empty();
    g.current_root = Some("/w/alpha".into());
    g.registry = Ok(crate::records_store::ListedFolders { folders: vec![listed("/w/alpha", "PA", 0), listed("/w/beta", "PB", 1)], ..Default::default() });
    g.folders = vec![attached("/w/alpha", "PA", vec![run("run:1", "thread:x", RecordedLifecycle::StartNotConfirmed, "2026-11-01T00:00:00Z")]), attached("/w/beta", "PB", vec![])];
    g.homes = vec![home(vec![], vec![])];
    g.index = vec![IndexRow { home: "account".into(), thread: "thread:x".into(), project: "/w/beta".into() }];
    let read = compose(g);
    let x = entry(&read, "thread:x");
    assert_eq!((x.home.as_deref(), x.project_root.as_deref(), x.project_source), (Some("account"), Some("/w/beta"), ProjectSource::Recorded));
    assert!(matches!(&x.open, OpenWith::NotOpenable { reason } if reason.contains("not in the list")), "{:?}", x.open);
}

#[test]
fn runs_join_their_conversation_with_each_lifecycle_state() {
    let mut g = empty();
    g.current_root = Some("/w/alpha".into());
    g.folders = vec![attached("/w/alpha", "P", vec![
        run("run:open", "t-open", RecordedLifecycle::OpenInterrupted, "2026-11-02T00:00:00Z"),
        run("run:older", "t-open", RecordedLifecycle::Ended { stopped_by: "the person".into(), cause: "ended to start review-pack".into() }, "2026-11-01T00:00:00Z"),
        run("run:ended", "t-ended", RecordedLifecycle::Ended { stopped_by: "the person".into(), cause: "completed".into() }, "2026-11-01T00:00:00Z"),
        run("run:unconfirmed", "t-unconfirmed", RecordedLifecycle::StartNotConfirmed, "2026-11-01T00:00:00Z"),
        run("run:unknown", "t-unknown", RecordedLifecycle::Unknown("conflicting run_opened/run_ended entries".into()), "2026-11-01T00:00:00Z"),
        run("run:held-busy", "t-busy", RecordedLifecycle::OpenInterrupted, "2026-11-01T00:00:00Z"),
        run("run:earlier-session", "t-earlier", RecordedLifecycle::OpenInterrupted, "2026-11-01T00:00:00Z"),
        run("run:no-report", "t-no-report", RecordedLifecycle::OpenInterrupted, "2026-11-01T00:00:00Z"),
    ])];
    g.homes = vec![home(["t-open", "t-ended", "t-unconfirmed", "t-unknown", "t-busy", "t-earlier", "t-no-report", "t-none"].iter().enumerate().map(|(i, t)| thread(t, "/w/alpha", i as i64 + 1)).collect(), vec![])];
    g.finished = vec![("run:open".into(), Some(true)), ("run:no-report".into(), Some(false)), ("run:held-busy".into(), None)];
    let read = compose(g);
    let open = entry(&read, "t-open");
    let latest = open.run.as_ref().unwrap();
    assert_eq!((latest.run_id.as_str(), latest.state, latest.finished_reported, open.run_count), ("run:open", RunState::Open, Some(true), 2));
    assert_eq!((latest.ended_by.clone(), latest.result_count), (None, None));
    assert_eq!(latest.workflow, RunWorkflow { name: Some("review-pack".into()), title: None, origin: Some("project library".into()), release: None });
    let ended = entry(&read, "t-ended").run.clone().unwrap();
    assert_eq!((ended.state, ended.ended_by, ended.finished_reported), (RunState::Ended, Some(EndedBy { stopped_by: "the person".into(), cause: "completed".into() }), None));
    assert_eq!(entry(&read, "t-unconfirmed").run.as_ref().unwrap().state, RunState::StartNotConfirmed);
    assert_eq!(entry(&read, "t-unknown").run.as_ref().unwrap().state, RunState::Unknown);
    assert_eq!(entry(&read, "t-busy").run.as_ref().unwrap().finished_reported, None, "operation pending");
    assert_eq!(entry(&read, "t-earlier").run.as_ref().unwrap().finished_reported, None, "not held live here");
    assert_eq!(entry(&read, "t-no-report").run.as_ref().unwrap().finished_reported, Some(false));
    let none = entry(&read, "t-none");
    assert_eq!((none.run.clone(), none.run_count, none.children_running, none.archived), (None, 0, None, false));
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
fn needs_answer_live_and_open_come_from_what_the_host_holds() {
    let mut g = empty();
    g.current_root = Some("/w/alpha".into());
    g.folders = vec![attached("/w/alpha", "P", vec![])];
    let mut h = home(vec![thread("loaded", "/w/alpha", 2), thread("listed", "/w/alpha", 1)], vec![
        json!({"generation":generation(),"threadId":"loaded","name":"Working","status":{"type":"active","activeFlags":["waitingOnApproval"]},"cwd":"/w/alpha"}),
        json!({"generation":{"appSession":"session:invented","home":HOME,"spawnCounter":0},"threadId":"listed","status":{"type":"active"}}),
    ]);
    h.waiting = vec![("loaded".into(), 2)];
    g.homes = vec![h];
    let read = compose(g);
    let loaded = entry(&read, "loaded");
    assert_eq!((loaded.needs_answer, loaded.live, loaded.title.as_deref()), (2, Live::Running, Some("Working")));
    assert_eq!(loaded.open, OpenWith::Loaded { generation: generation(), thread_id: "loaded".into() });
    let listed = entry(&read, "listed");
    assert_eq!((listed.needs_answer, listed.live), (0, Live::NotLoaded), "an earlier generation's row is not this generation's report");
    assert_eq!(listed.open, OpenWith::History { home: "account".into(), generation: generation(), selection_epoch: 3, thread_id: "listed".into() });
    assert_eq!(live(&json!({"type":"idle"})), Live::Idle);
    assert_eq!(live(&json!({"type":"systemError"})), Live::Unknown);
    assert_eq!(live(&Value::Null), Live::Unknown);

    // A home whose Codex ended: what it last held opens nothing and reports nothing live.
    let mut g = empty();
    let mut ended = home(vec![thread("gone-codex", "/data/conversations-without-project", 1)], vec![]);
    ended.current = false;
    let read = compose({ g.homes = vec![ended]; g });
    assert!(read.unassigned.is_empty(), "no list of a Codex not running is shown as current");
}

#[test]
fn the_shape_serializes_as_agreed() {
    let mut g = empty();
    g.current_root = Some("/w/alpha".into());
    g.folders = vec![FolderInput { root: "/w/alpha".into(), examined: Examined::Gone, runs: RunsInput::NotAttempted }];
    g.homes = vec![home(vec![thread("t", "/w/alpha", 1)], vec![])];
    let value = serde_json::to_value(compose(g)).unwrap();
    assert_eq!(value["readAt"], "2026-11-19T00:00:00.000Z");
    assert_eq!(value["conversations"][0], json!({"home":"account","state":"read"}));
    let p = &value["projects"][0];
    assert_eq!((p["state"].clone(), p["notice"]["kind"].clone(), p["runsRead"]["state"].clone()), (json!("unavailable"), json!("gone"), json!("not-read")));
    assert!(p["runsRead"]["reason"].as_str().unwrap().contains("located"));
    let e = &p["entries"][0];
    for key in ["id", "home", "projectRoot", "projectSource", "title", "titleSource", "createdAt", "updatedAt", "live", "needsAnswer", "archived", "open", "run", "runCount", "childrenRunning"] {
        assert!(e.get(key).is_some(), "entry lacks {key}: {e}");
    }
    assert_eq!((e["projectSource"].clone(), e["titleSource"].clone(), e["live"].clone()), (json!("reported-folder"), json!("first-message"), json!("not-loaded")));
    assert_eq!(e["open"], json!({"kind":"history","home":"account","generation":generation(),"selectionEpoch":3,"threadId":"t"}));
    let not_openable = serde_json::to_value(OpenWith::NotOpenable { reason: "why".into() }).unwrap();
    assert_eq!(not_openable, json!({"kind":"not-openable","reason":"why"}));
    let run = serde_json::to_value(entry_run(&run("r", "t", RecordedLifecycle::StartNotConfirmed, "x"), &BTreeMap::new(), &CatalogInput::default())).unwrap();
    assert_eq!(run["state"], "start-not-confirmed");
    for key in ["runId", "workflow", "endedBy", "finishedReported", "resultCount"] { assert!(run.get(key).is_some(), "run lacks {key}"); }
}

// ---- A real records store, read without writing ----

fn folder(base: &Path, rel: &str) -> PathBuf {
    let p = base.join(rel);
    std::fs::create_dir_all(&p).unwrap();
    p
}
/// Every entry below `root`: its bytes (None for a folder), length and
/// modification time, so a rewrite with the same bytes shows too.
fn tree(root: &Path) -> BTreeMap<PathBuf, (Option<Vec<u8>>, u64, Option<std::time::SystemTime>)> {
    let mut out = BTreeMap::new();
    let mut stack = vec![root.to_path_buf()];
    while let Some(dir) = stack.pop() {
        for item in std::fs::read_dir(&dir).unwrap() {
            let path = item.unwrap().path();
            let meta = std::fs::symlink_metadata(&path).unwrap();
            let bytes = if meta.is_dir() { stack.push(path.clone()); None } else { Some(std::fs::read(&path).unwrap()) };
            out.insert(path.strip_prefix(root).unwrap().to_path_buf(), (bytes, meta.len(), meta.modified().ok()));
        }
    }
    out
}
use std::path::PathBuf;

struct Fixture { store: PathBuf, base: PathBuf }
impl Drop for Fixture {
    fn drop(&mut self) {
        crate::records_store::use_store_for_test(None);
        let _ = std::fs::remove_dir_all(&self.store);
        let _ = std::fs::remove_dir_all(&self.base);
    }
}

#[test]
fn a_real_registry_with_a_moved_and_a_gone_folder_a_torn_line_and_a_name_clash_is_read_without_writing() {
    let temp = std::fs::canonicalize(std::env::temp_dir()).unwrap();
    let store = temp.join(crate::util::opaque_id("navigator-store-").unwrap());
    let base = temp.join(crate::util::opaque_id("navigator-projects-").unwrap());
    std::fs::create_dir_all(&base).unwrap();
    crate::records_store::use_store_for_test(Some(Ok(crate::records_store::Store { root: store.clone(), placement: crate::records_store::Placement::Override, limits: vec![] })));
    let f = Fixture { store, base };
    let one = folder(&f.base, "one/proj");
    let two = folder(&f.base, "two/proj");
    let gone = folder(&f.base, "gone");
    let before = folder(&f.base, "before-move");
    for root in [&one, &two, &gone, &before] {
        assert_eq!(crate::records_store::attach(root, true).unwrap().how, "minted");
    }
    // A recorded run in `one/proj`, opened in an invented conversation.
    let body = json!({"runId":"run:invented","startedBy":{"kind":"person"},"surface":"App run",
        "workflow":{"kind":"workflow","origin":"project","sourceRoot":"/invented/library","name":"review-pack","revision":"rev-invented","revisionVerification":"verified"},
        "conversationRef":"thread:invented"});
    let mut opened = crate::records::supply::PendingRunEntry::new("run_opened", body, crate::util::now_rfc3339()).unwrap();
    crate::records::supply::append_run_entry(&one, "run:invented", &mut opened).unwrap();
    let after = f.base.join("after-move");
    std::fs::rename(&before, &after).unwrap();
    std::fs::remove_dir_all(&gone).unwrap();
    let s = |p: &Path| p.to_str().unwrap().to_owned();

    // Read while the registry is whole.
    let trees = || (tree(&f.store), tree(&f.base));
    let was = trees();
    let listed = crate::storage::without_mutations_for_test(crate::records_store::listed_folders).unwrap();
    assert_eq!(listed.folders.iter().map(|l| l.root.clone()).collect::<Vec<_>>(), [s(&one), s(&two), s(&gone), s(&before)]);
    assert_eq!(listed.torn, None);
    let (registry, folders) = gather_projects(Some(&s(&after)));
    assert_eq!(trees(), was, "the read wrote, created or touched nothing in the store or the projects");
    let mut g = empty();
    g.current_root = Some(s(&after));
    g.registry = registry;
    g.folders = folders;
    let read = compose(g);
    let current = &read.projects[0];
    assert_eq!((current.root.clone(), current.current, current.state), (s(&after), true, ProjectState::Open));
    let notice = current.notice.as_ref().unwrap();
    assert_eq!((notice.kind.as_str(), notice.resolutions.clone()), ("moved", vec!["adopt".to_owned(), "new-identity".to_owned()]));
    assert!(matches!(current.runs_read.outcome, ReadOutcome::NotRead { .. }));
    let gone_project = project(&read, &s(&gone));
    assert_eq!((gone_project.state, gone_project.notice.as_ref().unwrap().kind.as_str()), (ProjectState::Unavailable, "gone"));
    assert!(gone_project.project_id.is_some(), "the store's identity of a folder that is gone is still given");
    let before_project = project(&read, &s(&before));
    assert_eq!(before_project.state, ProjectState::Unavailable);
    let first = project(&read, &s(&one));
    assert_eq!((first.label.as_str(), first.state, first.notice.clone()), ("one/proj", ProjectState::Listed, None));
    assert_eq!(project(&read, &s(&two)).label, "two/proj");
    assert_eq!(project(&read, &s(&gone)).label, "gone");
    assert_eq!(first.runs_read, RunsRead { outcome: ReadOutcome::Read, limits: vec![] });
    let invented = &first.entries[0];
    assert_eq!((invented.id.as_str(), invented.project_source, invented.live), ("thread:invented", ProjectSource::RunRecord, Live::Unknown));
    assert_eq!(invented.run.as_ref().unwrap().state, RunState::Open);
    assert!(read.registry_limits.is_empty());

    // The registry's last line torn: read to its last complete line, and said.
    let roots = f.store.join("roots.jsonl");
    let mut bytes = std::fs::read(&roots).unwrap();
    bytes.extend_from_slice(b"{\"format\":\"chirality.records-store.root\",\"projectId\":");
    std::fs::write(&roots, &bytes).unwrap();
    let was = trees();
    let (registry, folders) = gather_projects(Some(&s(&after)));
    assert_eq!(trees(), was, "nothing written beside a torn registry either");
    let mut g = empty();
    g.current_root = Some(s(&after));
    g.registry = registry;
    g.folders = folders;
    let read = compose(g);
    assert_eq!(read.projects.len(), 5, "the complete lines still list every folder");
    assert!(read.registry_limits.iter().any(|l| l.contains("roots.jsonl")), "{:?}", read.registry_limits);
    let notice = read.projects[0].notice.as_ref().unwrap();
    assert_eq!((notice.kind.as_str(), notice.resolutions.len()), ("association not known", 0), "no act is offered while the registry is torn");
    assert_eq!(project(&read, &s(&one)).runs_read.outcome, ReadOutcome::Read);
}

#[test]
fn without_a_store_the_launched_project_is_still_shown() {
    let temp = std::fs::canonicalize(std::env::temp_dir()).unwrap();
    let missing = temp.join(crate::util::opaque_id("navigator-no-store-").unwrap()).join("absent");
    let base = temp.join(crate::util::opaque_id("navigator-launched-").unwrap());
    std::fs::create_dir_all(&base).unwrap();
    crate::records_store::use_store_not_started_for_test(Some(Ok(crate::records_store::Store { root: missing.clone(), placement: crate::records_store::Placement::Override, limits: vec![] })));
    let f = Fixture { store: missing.parent().unwrap().to_path_buf(), base: base.clone() };
    let was = tree(&f.base);
    let (registry, folders) = gather_projects(base.to_str());
    assert_eq!(tree(&f.base), was);
    assert!(!missing.exists(), "no store was created");
    let mut g = empty();
    g.current_root = Some(base.to_str().unwrap().into());
    g.registry = registry;
    g.folders = folders;
    let read = compose(g);
    assert_eq!(read.projects.len(), 1);
    assert_eq!(read.projects[0].state, ProjectState::Open);
    assert!(read.registry_limits[0].contains("not read"), "{:?}", read.registry_limits);
    assert!(matches!(&read.projects[0].runs_read.outcome, ReadOutcome::NotRead { reason } if reason.contains("records store")));
}
