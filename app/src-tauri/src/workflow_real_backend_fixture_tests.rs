// Opt-in only (`#[ignore]` plus a distinct parent gate): the App's included
// LS-5 workflow run through the production WorkflowRootSession pipeline
// against the REAL pinned stock Codex 0.160 app-server, whose model side is
// the deterministic loopback Responses fixture. The fixture's replies are
// scripted, not inference: it asks for ONE fixed native tool action (an
// `exec_command` apply_patch adding an invented file in the owned project) and then
// reports the workflow finished. Nothing here is model, J1/J2, human or
// native qualification.
use crate::hosting::{Host, HostConfig};
use crate::native_history::{Direction, NativeHistory};
use std::time::Instant;
#[allow(dead_code)]
mod responses_fixture {
    include!("../tests/support/responses_fixture.rs");
}
use responses_fixture::ResponsesFixture;

const WORKFLOW_GATE: &str = "parent-authorized-0160-local-workflow-fixture";
const BINARY_SHA: &str = "112fae7a5a1223e673c8a1791d32338f37df8b527ff1159bb8adac6c4dbf1b4b";
const MODEL: &str = "chirality-fixture-model";
const PROVIDER: &str = "chirality-workflow-local";
const PERSON_TEXT: &str = "Synthetic fixture request (no model): run the included workflow.";
const BEGIN: &str = "<<<chirality-workflow coordinated-knowledge-work@3730d84debb5 begin>>>";
const TOOL_PATH: &str = "fixture-output/real-codex-tool-result.txt";
const TOOL_LINE: &str = "Invented fixture output, written by stock Codex's own apply_patch execution.";
const CALL_ID: &str = "call_fixture_exec_apply_patch_1";
const FINISHED_LINE: &str = "Workflow finished: bundled:coordinated-knowledge-work";
const NOTICE_START: &str = "[Chirality] Workflow run ended:";
const FOLLOW_TEXT: &str = "Synthetic fixture follow-up (no model): first ordinary message after the end.";
const LATER_TEXT: &str = "Synthetic fixture follow-up (no model): second ordinary message.";
const FOLLOW_REPLY: &str = "Synthetic fixture reply (scripted, not a model) to an ordinary message.";

/// The owned scratch: the host is stopped and the root removed on every path.
struct Owned {
    root: std::path::PathBuf,
    host: Arc<Host>,
    /// The later process's host (fresh-process read-back), when started.
    later: Mutex<Option<Arc<Host>>>,
}
impl Drop for Owned {
    fn drop(&mut self) {
        let _ = self.host.stop("workflow-backend-fixture", "fixture cleanup");
        if let Some(later) = self.later.lock().unwrap().take() {
            let _ = later.stop("workflow-backend-fixture", "fixture cleanup");
        }
        let _ = std::fs::remove_dir_all(&self.root);
    }
}

fn private_dir(path: &std::path::Path) {
    use std::os::unix::fs::PermissionsExt;
    std::fs::create_dir(path).unwrap();
    std::fs::set_permissions(path, std::fs::Permissions::from_mode(0o700)).unwrap();
}

/// Every file under `dir`, relative, sorted.
fn files_under(dir: &std::path::Path) -> Vec<(String, Vec<u8>)> {
    let mut out = Vec::new();
    let mut stack = vec![dir.to_path_buf()];
    while let Some(d) = stack.pop() {
        for entry in std::fs::read_dir(&d).unwrap() {
            let path = entry.unwrap().path();
            if path.is_dir() {
                stack.push(path);
            } else {
                out.push((path.strip_prefix(dir).unwrap().to_string_lossy().into_owned(), std::fs::read(&path).unwrap()));
            }
        }
    }
    out.sort();
    out
}

/// Public history path, as the greeting fixture reads it back: each turn
/// (oldest first) with its items.
fn history_items(host: &Host, generation: &Value, home: &str, thread: &str) -> Vec<(Value, Vec<Value>)> {
    let mut view = NativeHistory::new(home, generation.clone()).unwrap();
    let fetch = |view: &mut NativeHistory, query: crate::native_history::HistoryQuery| {
        let dispatch = host.history_dispatch(&query).unwrap();
        let evidence = host.history_wait(&dispatch, Duration::from_secs(10)).unwrap();
        assert!(evidence["response"].get("error").is_none(), "history read answered with an error");
        let result = evidence["response"]["result"].clone();
        view.receive(&query, home, generation, &result).unwrap();
        result
    };
    let query = view.list_threads(None, Direction::Desc).unwrap();
    let list = fetch(&mut view, query);
    assert!(list["data"].as_array().into_iter().flatten().any(|t| t["id"] == thread), "history lists the conversation");
    view.select(thread).unwrap();
    let query = view.turns_page(None, Direction::Asc).unwrap();
    let turns: Vec<Value> = fetch(&mut view, query)["data"].as_array().cloned().unwrap_or_default();
    let mut out = Vec::new();
    for turn in turns {
        let query = view.items_page(turn["id"].as_str().unwrap(), None, Direction::Asc).unwrap();
        // `thread/items/list` entries wrap each item: {item, turnId, …}.
        let items = fetch(&mut view, query)["data"].as_array().into_iter().flatten().filter(|e| e["turnId"] == turn["id"]).map(|e| e["item"].clone()).collect();
        out.push((turn, items));
    }
    out
}
fn user_texts(items: &[Value]) -> Vec<String> {
    items.iter().filter(|i| i["type"] == "userMessage").flat_map(|i| i["content"].as_array().cloned().unwrap_or_default())
        .filter_map(|c| c["text"].as_str().map(str::to_owned)).collect()
}
/// The home's own receiving history owner selects the conversation, as the
/// App's history panel does, so a supply check can read its native pages.
fn select_in_home(home: &HomeSession, thread: &str) {
    let receive = |query: crate::native_history::HistoryQuery| {
        let dispatch = home.host.history_dispatch(&query).unwrap();
        home.history.lock().unwrap().dispatched(dispatch.clone());
        home.host.history_wait(&dispatch, Duration::from_secs(10)).unwrap();
        home.history.lock().unwrap().reconcile(&home.host);
    };
    let list = { let mut h = home.history.lock().unwrap(); h.reconcile(&home.host); h.history_mut().unwrap().list_threads(None, Direction::Asc).unwrap() };
    receive(list);
    home.history.lock().unwrap().history_mut().unwrap().select(thread).unwrap();
    let turns = home.history.lock().unwrap().history_mut().unwrap().turns_page(None, Direction::Asc).unwrap();
    receive(turns);
}

#[test]
#[ignore = "Parent only: explicit local workflow fixture opt-in; stock Codex, loopback fixture, no model, credential or owner home"]
fn parent_authorized_stock_native_bundled_workflow_fixture() -> Result<(), String> {
    // The gate precedes path lookup, scratch setup or supplier execution.
    if std::env::var("CHIRALITY_RUN_NATIVE_BACKEND_SMOKE").ok().as_deref() != Some(WORKFLOW_GATE) {
        return Err("Parent local workflow fixture opt-in absent; nothing executed".into());
    }
    let binary = PathBuf::from(std::env::var("CHIRALITY_NATIVE_SMOKE_BIN").map_err(|_| "stock binary path absent")?);
    if !binary.is_absolute() {
        return Err("stock binary path must be absolute".into());
    }
    let base = std::fs::canonicalize(std::env::temp_dir()).unwrap();
    let owned = Owned { root: base.join(crate::util::opaque_id("workflow-backend-fixture-")?), host: Arc::new(Host::new()), later: Mutex::new(None) };
    private_dir(&owned.root);
    let project = owned.root.join("project");
    let codex_home = owned.root.join("codex-home");
    let instructions = owned.root.join("app-data/instructions");
    std::fs::create_dir(&project).unwrap();
    private_dir(&codex_home);
    std::fs::create_dir(instructions.parent().unwrap()).unwrap(); // first seed: the instruction folder is absent
    let mktemp = std::process::Command::new("/usr/bin/mktemp").arg("-d").arg(owned.root.join("version-probe-XXXXXX")).output().unwrap();
    assert!(mktemp.status.success());
    let probe_home = PathBuf::from(String::from_utf8(mktemp.stdout).unwrap().trim_end_matches('\n'));
    assert!(probe_home.starts_with(&owned.root));
    // This App's installed resources, explicitly bound (as lib.rs setup records
    // `resource_dir()/workflows`): the exact pinned LS-5 package bytes.
    let installed = InstalledBundle::under(&owned.root.join("installed-resources"));

    // Synthetic model side. Step 0 asks for one fixed apply_patch adding an
    // invented file through `exec_command` (the only command tool Codex 0.160
    // offers an unknown model; it has no `apply_patch` tool), whose heredoc
    // form Codex applies as a patch itself; step 1 is the scripted report.
    let patch = format!("*** Begin Patch\n*** Add File: {TOOL_PATH}\n+{TOOL_LINE}\n*** End Patch\n");
    let finished = format!("Synthetic fixture reply (scripted, not a model): the fixed tool action was requested.\n{FINISHED_LINE}");
    let fixture = ResponsesFixture::start(
        vec![
            vec![json!({"type":"function_call","id":"fc_fixture_1","call_id":CALL_ID,"name":"exec_command",
                "arguments":json!({"cmd":format!("apply_patch <<'PATCH'\n{patch}PATCH\n"),"workdir":project.to_str().unwrap(),"login":false}).to_string()})],
            vec![responses_fixture::message("msg_fixture_finished", &finished)],
            // Steps 2+: the scripted reply to each later ordinary message.
            vec![responses_fixture::message("msg_fixture_ordinary", FOLLOW_REPLY)],
        ],
        vec![("begin", BEGIN.to_string()), ("person", PERSON_TEXT.to_string()), ("supply", ".chirality/workflow-supply/coordinated-knowledge-work/".to_string()), ("callId", CALL_ID.to_string()),
            ("notice", NOTICE_START.to_string()), ("follow", FOLLOW_TEXT.to_string()), ("later", LATER_TEXT.to_string())],
    )?;
    // A fresh private Codex home: the App's local-provider literal plus the
    // home's own approval/sandbox choice (the App sends neither). Codex's own
    // seatbelt cannot nest inside the parent's localhost-only sandbox
    // (`sandbox_apply: Operation not permitted`), so the parent's outer profile
    // is the boundary here: loopback-only network, no owner `~/.codex`, and
    // writes denied under `$HOME` except the owned scratch. It does not restrict
    // writes outside `$HOME`. No production guard is changed.
    std::fs::write(codex_home.join("config.toml"), format!(
        "model = \"{MODEL}\"\nmodel_provider = \"{PROVIDER}\"\napproval_policy = \"never\"\nsandbox_mode = \"danger-full-access\"\n\n[model_providers.{PROVIDER}]\nname = \"Chirality workflow fixture\"\nbase_url = \"{}\"\nwire_api = \"responses\"\nrequires_openai_auth = false\n",
        fixture.base_url())).unwrap();

    let mut cfg = HostConfig::new(binary, codex_home, probe_home, project.clone());
    cfg.expected_sha256 = Some(BINARY_SHA.into());
    cfg.allow_unverified_dev = true; // the pinned binary; not supplier qualification
    cfg.wait_limit = Duration::from_secs(15);
    let ready = owned.host.start(&cfg, "workflow-backend-fixture")?;
    assert_eq!(ready["versionIdentity"]["observedVersionLabel"], "codex-cli 0.160.0");
    let generation = owned.host.snapshot()["generation"].clone();
    super::seed_instructions(&instructions)?;
    let composition = super::compose_role(&instructions, Some(crate::role_supply::Role::HELP_HUMAN))?;
    let started = owned.host.thread_start_with_guidance(project.to_str().unwrap(), MODEL, PROVIDER, &composition.text)?;
    assert_eq!((started["result"]["model"].as_str(), started["result"]["modelProvider"].as_str()), (Some(MODEL), Some(PROVIDER)));
    let thread = started["result"]["thread"]["id"].as_str().ok_or("native thread identity absent")?.to_owned();
    let later_cfg = cfg.clone();
    let home = Arc::new(HomeSession::new(crate::home_resources::HomeClass::Account, owned.host.clone(), Ok(cfg))?);
    let home_id = generation["home"].as_str().unwrap().to_owned();

    // select → prepare (records pending) → start (production dispatch).
    let workflows = Mutex::new(WorkflowRootSession::default());
    let chat = crate::workflow_selection::Chat::in_home(&home, &thread);
    let reference = {
        let mut root = workflows.lock().unwrap();
        root.configure_installed_bundle(installed.0.clone())?;
        let choice = root.select_production_bundle(Some(&chat), installed.0.clone(), BUNDLED)?["choice"].clone();
        assert_eq!(choice["runnable"], true, "{choice}");
        assert_eq!(choice["identity"]["origin"], "bundled");
        assert_eq!(choice["identity"]["revision"], crate::workflow_workspace::production_catalog::SELECTED_BUNDLED_REVISION);
        root.prepare_run(home.clone(), &generation, &thread, PERSON_TEXT.into(), Some(&project))?
    };
    assert!(!project.join(TOOL_PATH).exists(), "the tool result is not pre-created");
    let send = super::start_workflow_run(&workflows, &reference)?;
    assert_eq!(workflows.lock().unwrap().runs[&reference].lock().unwrap().lifecycle, RunLifecycle::Open, "{send}");

    // Observe through the production record tick until the conversation has
    // exactly `n` turns and the newest reached its native terminal.
    let wait_turns = |n: usize| -> Result<Value, String> {
        let deadline = Instant::now() + Duration::from_secs(60);
        loop {
            crate::host_tick::tick_home(&home, &workflows);
            let snapshot = owned.host.snapshot();
            let turns: Vec<Value> = snapshot["conversationTurns"].as_array().into_iter().flatten()
                .filter(|t| t["generation"] == generation && t["threadId"] == thread.as_str()).cloned().collect();
            assert!(turns.len() <= n, "no duplicate send: {} turns, {n} expected", turns.len());
            if turns.len() == n && turns.iter().all(|t| t["terminalEventObserved"] == true) {
                return Ok(turns[n - 1].clone());
            }
            if Instant::now() >= deadline {
                return Err(format!("native terminal wait deadline exceeded at turn {n}"));
            }
            std::thread::sleep(Duration::from_millis(100));
        }
    };
    let terminal = wait_turns(1)?;
    assert_eq!(terminal["nativeTurn"]["status"], "completed", "{}", terminal["nativeTurn"]["status"]);
    let turn = terminal["turnId"].as_str().unwrap().to_owned();
    crate::host_tick::tick_home(&home, &workflows);

    // Real Codex executed the fixed tool action; the file is its result.
    let written = std::fs::read_to_string(project.join(TOOL_PATH)).map_err(|_| {
        // Facts only: offered tool names, returned tool results and item kinds.
        let facts: Vec<Value> = fixture.requests().iter().map(|r| json!({"step":r["scriptStep"],"tools":r["tools"],"outputs":r["toolOutputs"]})).collect();
        let kinds: Vec<Value> = terminal["nativeTurn"]["items"].as_array().into_iter().flatten().map(|i| json!({"type":i["type"],"status":i["status"]})).collect();
        format!("tool result file absent; fixture {}; terminal items {}", json!(facts), json!(kinds))
    })?;
    assert_eq!(written, format!("{TOOL_LINE}\n"));

    // The run-text supply check against the real native pages (WR records it).
    select_in_home(&home, &thread);
    let run_check = workflows.lock().unwrap().runs[&reference].lock().unwrap().check_native_supply()?["check"].clone();
    assert_eq!(run_check["state"], "verified", "{run_check}");

    // The finished offer, as `host_status` shows it, then the person's end on it
    // (`workflow_end_run` with the offered message; the host re-reads it).
    let view = crate::host_tick::receive_view(&home);
    let status = crate::host_tick::workflow_status(&workflows, &home, &view, false);
    let offers: Vec<Value> = status["offers"].as_array().cloned().unwrap_or_default();
    let offer = offers.iter().find(|o| o["finished"]["run"] == reference.as_str()).ok_or_else(|| format!("no finished offer for the run: {}", json!(offers)))?.clone();
    assert_eq!(offer["finished"]["statement"], FINISHED_LINE);
    let ended = workflows.lock().unwrap().end_requested(&reference, &view, Some(&offer["message"]))?;
    let run_view = workflows.lock().unwrap().runs[&reference].lock().unwrap().view(&reference);
    assert_eq!(run_view["finishedReport"]["statement"], FINISHED_LINE);
    assert_eq!(run_view["endedAfterTurn"], turn.as_str());
    assert_eq!(ended["endNotice"]["state"], "pending: the next ordinary turn in this conversation carries it");

    // The end notice: the next ordinary message (`conversation_send_text`)
    // carries it exactly once, and the run stays ended.
    let follow = crate::ordinary_send_text(&home, &workflows, &generation, &thread, FOLLOW_TEXT, None, None)?;
    assert_eq!(follow["state"], "end notice and the person's text sent once", "{follow}");
    wait_turns(2)?;
    assert!(super::send_with_pending_notice(&workflows, &generation, &thread, "nothing pending").is_none(), "no notice is pending after it was carried");
    crate::ordinary_send_text(&home, &workflows, &generation, &thread, LATER_TEXT, None, None)?;
    wait_turns(3)?;
    assert_eq!(workflows.lock().unwrap().runs[&reference].lock().unwrap().lifecycle, RunLifecycle::Ended, "the run is not reopened");
    let view = crate::host_tick::receive_view(&home);
    let status = crate::host_tick::workflow_status(&workflows, &home, &view, false);
    assert!(!status["offers"].as_array().into_iter().flatten().any(|o| o["finished"]["run"] == reference.as_str()), "no finished offer for an ended run");
    select_in_home(&home, &thread);
    let notice_check = workflows.lock().unwrap().runs[&reference].lock().unwrap().check_end_notice_supply()?["check"].clone();
    assert_eq!((notice_check["state"].as_str(), notice_check["r3"]["state"].as_str()), (Some("verified"), Some("recorded")), "{notice_check}");

    // Records read back from the project (`workflow_read_records`, R3/RS).
    let records = crate::workflow_workspace::publication::ProjectRecords::open(&project)?;
    let selection = records.resolve(run_view["publication"]["selection"].as_str().unwrap()).map_err(|e| format!("{e:?}"))?;
    let body = selection.body();
    assert_eq!(body["standing"], "bundled");
    assert_eq!(body["identity"]["origin"], "bundled");
    assert_eq!(body["identity"]["revision"], crate::workflow_workspace::production_catalog::SELECTED_BUNDLED_REVISION);
    assert_eq!(body["holding_library"], installed.0.to_str().unwrap());
    let supply = crate::records::supply::read_project_supply(&records);
    let wr_kinds: Vec<Value> = supply["records"].as_array().into_iter().flatten().map(|r| r["kind"].clone()).collect();
    let (rs, limits) = crate::storage::read_all(&project);
    assert!(limits.is_empty(), "{limits:?}");
    let rs: Vec<Value> = rs.into_iter().filter(|e| e["runId"] == reference.as_str()).collect();
    let rs_kinds: Vec<Value> = rs.iter().map(|e| e["kind"].clone()).collect();
    assert_eq!(rs.iter().filter(|e| e["kind"] == "run_opened").count(), 1);
    assert_eq!(rs_kinds.first(), Some(&json!("run_opened")));
    let ended_at = rs_kinds.iter().position(|k| k == "run_ended").ok_or("no run_ended")?;
    // After the end, the run's log gains only the notice's R3 (and its check).
    let after: Vec<&Value> = rs[ended_at + 1..].iter().collect();
    assert!(after.iter().all(|e| e["kind"] == "supplied_guidance"), "{rs_kinds:?}");
    assert!(after.iter().any(|e| e["body"]["supplyForm"] == "workflow run end notice (turn text)"), "{rs_kinds:?}");
    // The included package declares no checkpoints, so the tool's file change
    // is no checkpoint arrival (EXEC §2.4 records declared checkpoints only).
    assert!(!rs_kinds.contains(&json!("checkpoint_arrival")), "{rs_kinds:?}");
    let mut wr_set: Vec<String> = wr_kinds.iter().map(|k| k.as_str().unwrap_or("").to_owned()).collect();
    wr_set.sort(); // references are opaque, listed by name
    for kind in ["run_text", "selection_record", "supply_check"] {
        assert!(wr_set.iter().any(|k| k == kind), "{wr_set:?}");
    }
    assert_eq!(wr_set.len(), wr_kinds.len());
    let end = rs.iter().filter(|e| e["kind"] == "run_ended").collect::<Vec<_>>();
    assert_eq!(end.len(), 1);
    assert_eq!(end[0]["body"]["cause"], "completed");

    // Supplied files: the TX-7 (c) supply copy holds exactly the package bytes.
    let package = files_under(&installed.0.join(BUNDLED));
    let supply_root = project.join(".chirality/workflow-supply").join(BUNDLED);
    let copies: Vec<PathBuf> = std::fs::read_dir(&supply_root).unwrap().map(|e| e.unwrap().path().join(BUNDLED)).collect();
    assert_eq!(copies.len(), 1);
    assert_eq!(files_under(&copies[0]), package, "the supply copy is the pinned package");

    // History read-back: three turns. The run turn has the exact run text, the
    // tool's file change and the scripted report; the next turn carries the end
    // notice once, then the person's text; the last has the person's text only.
    let history = history_items(&owned.host, &generation, &home_id, &thread);
    assert_eq!(history.len(), 3, "three native turns (no duplicate send)");
    let items = &history[0].1;
    let texts = user_texts(items);
    assert_eq!(texts.len(), 2, "run text and the person's text");
    assert!(texts[0].contains(BEGIN) && texts[0].contains(".chirality/workflow-supply/coordinated-knowledge-work/"));
    assert!(!texts[0].contains(installed.0.to_str().unwrap()), "no App-bundle path reaches the agent");
    assert_eq!(texts[1], PERSON_TEXT);
    let change = items.iter().find(|i| i["type"] == "fileChange").ok_or_else(|| format!("no fileChange item: {}", json!(items.iter().map(|i| &i["type"]).collect::<Vec<_>>())))?;
    assert_eq!(change["status"], "completed", "{change}");
    assert!(items.iter().any(|i| i["type"] == "agentMessage" && i["text"] == finished.as_str()));
    let follow_texts = user_texts(&history[1].1);
    assert_eq!(follow_texts.len(), 2, "{follow_texts:?}");
    assert!(follow_texts[0].starts_with(NOTICE_START) && follow_texts[0].contains(&reference) && follow_texts[0].ends_with("No workflow is in force."), "{}", follow_texts[0]);
    assert_eq!(follow_texts[1], FOLLOW_TEXT);
    assert_eq!(user_texts(&history[2].1), [LATER_TEXT], "the notice is carried once only");
    let turn_texts: Vec<Vec<String>> = history.iter().map(|(_, items)| user_texts(items)).collect();

    // The fixture saw: the run text, then the tool result for the one call.
    let requests = fixture.requests();
    let responses: Vec<&Value> = requests.iter().filter(|r| r["answered"] == "sse").collect();
    assert!(requests.iter().all(|r| r["loopbackPeer"] == true && r["parsed"] == true));
    assert_eq!(responses.len(), 4, "tool step, report and two ordinary replies: {}", json!(responses.iter().map(|r| json!({"step":r["scriptStep"],"outputs":r["toolOutputs"]})).collect::<Vec<_>>()));
    assert!(responses.iter().all(|r| r["model"] == MODEL && r["stream"] == true && r["markers"]["begin"] == true && r["markers"]["person"] == true));
    assert_eq!(responses.iter().map(|r| r["markers"]["notice"] == true).collect::<Vec<_>>(), [false, false, true, true], "the notice first reaches the model with the follow-up");
    let outputs = responses[1]["toolOutputs"].as_array().cloned().unwrap_or_default();
    assert!(outputs.iter().any(|o| o["callId"] == CALL_ID), "the tool result returned for the scripted call: {}", json!(outputs));
    let offered: Vec<Value> = responses[0]["tools"].as_array().cloned().unwrap_or_default();

    // Normal stop with no surviving descendants.
    owned.host.stop("workflow-backend-fixture", "workflow fixture finished")?;
    assert_eq!(owned.host.snapshot()["lifecycle"].as_array().and_then(|v| v.last()).map(|e| e["descendants"]["surviving"].clone()), Some(json!(0)));

    // A fresh process: a new Host and generation over the same Codex home and
    // project, and a new Root holding no run. It reads the ended run's records
    // and the real backend's history back; a repeat end is refused and writes
    // nothing.
    let later = Arc::new(Host::new());
    *owned.later.lock().unwrap() = Some(later.clone());
    later.start(&later_cfg, "workflow-backend-fixture-later")?;
    let later_generation = later.snapshot()["generation"].clone();
    assert_ne!(later_generation, generation, "a new generation");
    let rs_before = crate::storage::read_all(&project).0;
    let wr_before = crate::records::supply::read_project_supply(&crate::workflow_workspace::publication::ProjectRecords::open(&project)?);
    let mut fresh = WorkflowRootSession::default();
    let repeat = fresh.end_recorded_run(&project, &reference, &thread, false, None);
    assert!(repeat.is_err(), "an ended run is not ended again: {repeat:?}");
    fresh.observe_ended_runs(&project);
    assert_eq!(crate::storage::read_all(&project).0, rs_before, "no RS record from the fresh process");
    let wr_after = crate::records::supply::read_project_supply(&crate::workflow_workspace::publication::ProjectRecords::open(&project)?);
    assert_eq!(wr_after["records"], wr_before["records"], "no WR record from the fresh process");
    let later_history = history_items(&later, &later_generation, later_generation["home"].as_str().unwrap(), &thread);
    let later_texts: Vec<Vec<String>> = later_history.iter().map(|(_, items)| user_texts(items)).collect();
    assert_eq!(later_texts, turn_texts, "the later generation reads the same three turns");
    later.stop("workflow-backend-fixture", "fresh-process read finished")?;
    assert_eq!(later.snapshot()["lifecycle"].as_array().and_then(|v| v.last()).map(|e| e["descendants"]["surviving"].clone()), Some(json!(0)));
    drop(fixture);
    println!("{}", json!({
        "probe":"real-backend-bundled-workflow-fixture",
        "standing":"stock Codex 0.160 with a deterministic loopback Responses fixture; the model replies and the finished report are SCRIPTED SYNTHETIC facts; the person's end is the test's call; not inference, model, human, J1/J2 or native qualification",
        "supplier":ready["versionIdentity"]["observedVersionLabel"],"reported":{"model":started["result"]["model"],"provider":started["result"]["modelProvider"]},
        "workflow":{"name":BUNDLED,"revision":body["identity"]["revision"],"standing":body["standing"],"holdingLibrary":"the explicitly bound test resources root"},
        "send":{"lifecycleAfterSend":"Open","terminal":terminal["nativeTurn"]["status"],"runTextCheck":run_check["state"]},
        "tool":{"offered":offered,"scripted":"exec_command carrying a fixed apply_patch heredoc (function_call)","fileWrittenByCodex":TOOL_PATH,"historyItem":change["type"],"resultReturned":true},
        "end":{"cause":end[0]["body"]["cause"],"statement":run_view["finishedReport"]["statement"],"result":ended},
        "endNotice":{"carriedBy":"the first ordinary message after the end","state":follow["state"],"check":notice_check["state"],"r3":notice_check["r3"]["state"],"laterTurnsWithNotice":0,"lifecycleAfter":"Ended"},
        "freshProcess":{"newGeneration":true,"repeatEnd":"refused","newRecords":0,"historyTurns":later_history.len()},
        "records":{"wr":wr_kinds,"rs":rs_kinds},
        "historyItems":history.iter().map(|(_, items)| items.iter().map(|i| i["type"].clone()).collect::<Vec<_>>()).collect::<Vec<_>>(),
        "fixture":{"responsesRequests":responses.len(),"otherRequests":requests.iter().filter(|r| r["answered"] != "sse").map(|r| json!({"method":r["method"],"path":r["path"]})).collect::<Vec<_>>()},
        "cleanup":{"descendantsSurviving":0}
    }));
    Ok(())
}
