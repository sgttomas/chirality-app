//! V4-AUT-06: the Host's start checks, send-time rules, level ledger entries, launch read and status.
use super::*;
use crate::codex_level::{self as cl, Method};
use std::io::BufRead;

fn root(name: &str) -> PathBuf {
    let base = std::env::temp_dir().join(opaque_id(&format!("level-{name}-")).unwrap());
    std::fs::create_dir_all(&base).unwrap();
    base.canonicalize().unwrap()
}
fn g(host: &Host) -> Value {
    json!({"appSession": host.inner.0.lock().unwrap().app_session.clone(), "home": "level-home", "spawnCounter": 1})
}
/// A ready Host with the App ledger at `dir`, one conversation `thread` working in `cwd`.
fn ready_with_ledger(dir: &Path, cwd: &str) -> Arc<Host> {
    std::fs::create_dir_all(dir).unwrap();
    let host = Arc::new(Host::new());
    host.configure_recovery(dir.join("recovery.ledger.jsonl")).unwrap();
    let generation = g(&host);
    let mut i = host.inner.0.lock().unwrap();
    i.state = "ready".into();
    i.home = "level-home".into();
    i.spawn_counter = 1;
    i.generation = generation.clone();
    i.journal.begin_generation(generation.clone());
    i.threads.push(json!({"generation": generation, "threadId": "thread", "cwd": cwd}));
    if let Some(places) = i.level.places.as_mut() { places.home_identity = Some("app-home:invented".into()); }
    drop(i);
    host
}
fn send(host: &Host, method: &str, params: Value) -> Result<SourceRequest, String> {
    host.request_begin_scoped(method, params, json!({"kind":"person-directed"}), false, Some(&g(host)))
}
fn turn_params(thread: &str) -> Value {
    json!({"threadId": thread, "input": [{"type":"text","text":"invented","text_elements":[]}]})
}
fn reply(host: &Host, frame: Value) {
    host.on_line(&serde_json::to_vec(&frame).unwrap(), &g(host));
}
fn entries(host: &Host, kind: &str) -> Vec<Value> {
    host.flush_recovery_observations();
    host.recorded_recovery_entries().as_array().unwrap().iter().filter(|e| e["kind"] == kind).cloned().collect()
}
fn counts(host: &Host) -> (u64, usize, u64) {
    let i = host.inner.0.lock().unwrap();
    (i.next_id, i.source_requests.len(), i.send_position)
}
/// Every frame the Host writes, in order (a stand-in for Codex's input).
struct Wire {
    child: std::process::Child,
    frames: Receiver<Value>,
}
impl Wire {
    fn attach(host: &Host) -> Self {
        let mut child = Command::new("/bin/cat").env_clear().stdin(Stdio::piped()).stdout(Stdio::piped()).stderr(Stdio::null()).spawn().unwrap();
        *host.stdin.lock().unwrap() = child.stdin.take();
        let stdout = child.stdout.take().unwrap();
        let (tx, rx) = channel();
        std::thread::spawn(move || {
            let mut reader = BufReader::new(stdout);
            loop {
                let mut line = String::new();
                match reader.read_line(&mut line) {
                    Ok(0) | Err(_) => break,
                    Ok(_) => { let _ = tx.send(serde_json::from_str::<Value>(&line).unwrap()); }
                }
            }
        });
        Wire { child, frames: rx }
    }
    fn next(&self) -> Value { self.frames.recv_timeout(Duration::from_secs(5)).expect("a frame was written") }
    fn nothing(&self) -> bool { self.frames.recv_timeout(Duration::from_millis(200)).is_err() }
    fn close(mut self, host: &Host) {
        *host.stdin.lock().unwrap() = None;
        assert!(self.child.wait().unwrap().success());
    }
}

// ---- Item 3: start refusals ----

fn start_config(home: &Path, cwd: &Path) -> HostConfig {
    // No Codex binary exists here: a start that got past the checks would fail later, for another reason.
    HostConfig::new(PathBuf::from("/nonexistent/codex"), home.to_path_buf(), cwd.join("probe"), cwd.to_path_buf())
}

#[test]
fn environments_toml_is_refused_by_presence_without_being_opened() {
    let base = root("environments");
    let home = base.join("account");
    std::fs::create_dir_all(&home).unwrap();
    // A named pipe: opening it to read would wait for a writer, so a start that returns shows it was not opened.
    let fifo = home.join(cl::ENVIRONMENTS_FILE);
    let name = std::ffi::CString::new(fifo.as_os_str().as_encoded_bytes()).unwrap();
    assert_eq!(unsafe { libc::mkfifo(name.as_ptr(), 0o600) }, 0);
    let host = Arc::new(Host::new());
    let cfg = start_config(&home, &base);
    let (tx, rx) = channel();
    let starter = Arc::clone(&host);
    std::thread::spawn(move || { let _ = tx.send(starter.start(&cfg, "fixture")); });
    let refused = rx.recv_timeout(Duration::from_secs(5)).expect("the start returned without opening the file").unwrap_err();
    assert!(refused.contains("environments.toml") && refused.contains("Remove it"), "{refused}");
    let status = host.snapshot();
    assert_eq!(status["levelStartRefusal"], json!({"refused":"environments-file","path":fifo.to_string_lossy(),"presence":"present"}));
    assert_eq!(status["startRefusalCause"], "home");
    assert_eq!(status["lastStartRefusal"]["reason"], refused.as_str());
    assert_eq!(status["state"], "absent", "Codex was not started");
    // A link to nowhere is an entry all the same: refused by its presence.
    std::fs::remove_file(&fifo).unwrap();
    std::os::unix::fs::symlink(base.join("nowhere"), &fifo).unwrap();
    assert!(host.start(&start_config(&home, &base), "fixture").unwrap_err().contains("environments.toml"));
    // Removed: the level's checks pass, and the start fails later for its own reason.
    std::fs::remove_file(&fifo).unwrap();
    let later = host.start(&start_config(&home, &base), "fixture").unwrap_err();
    assert!(!later.contains("environments.toml"), "{later}");
    assert!(host.snapshot()["levelStartRefusal"].is_null(), "a later request clears it");
    std::fs::remove_dir_all(&base).unwrap();
}

#[test]
fn a_refused_home_path_is_refused_through_a_link() {
    let base = root("home-path");
    let real = base.join("has $x").join("App Data").join("account");
    std::fs::create_dir_all(&real).unwrap();
    let link = base.join("plain-link");
    std::os::unix::fs::symlink(&real, &link).unwrap();
    let host = Arc::new(Host::new());
    let refused = host.start(&start_config(&link, &base), "fixture").unwrap_err();
    assert!(refused.contains("refuses in that path") && refused.contains("Rename the folder"), "{refused}");
    let status = host.snapshot();
    assert_eq!(status["levelStartRefusal"]["refused"], "home-path");
    assert_eq!(status["levelStartRefusal"]["character"], "$");
    assert_eq!(status["levelStartRefusal"]["folder"], base.join("has $x").to_string_lossy().as_ref());
    assert_eq!(status["startRefusalCause"], "home");
    assert_eq!(status["state"], "absent");
    // Each refused character, in a component above the App's folders, as written.
    for (name, c) in [("a`b", "`"), ("a\"b", "\""), ("a\\b", "\\")] {
        let home = base.join(name).join("account");
        std::fs::create_dir_all(&home).unwrap();
        host.start(&start_config(&home, &base), "fixture").unwrap_err();
        assert_eq!(host.snapshot()["levelStartRefusal"]["character"], c, "{name}");
    }
    std::fs::remove_dir_all(&base).unwrap();
}

// ---- Item 4: send-time rules ----

#[test]
fn an_edits_level_is_not_sent_into_the_app_folders_and_the_no_project_folder_is_exempt() {
    let base = root("send");
    let person = base.join("person");
    let app_data = person.join("Library").join("Application Support").join("Chirality");
    let codex_home = app_data.join("homes").join("account");
    let elsewhere = person.join("projects").join("bridge");
    let quoted = person.join("projects").join("my \"quoted\" one");
    let no_project = crate::working_folder::no_project_folder(&app_data);
    for d in [&codex_home, &elsewhere, &quoted, &no_project] { std::fs::create_dir_all(d).unwrap(); }
    let host = ready_with_ledger(&base, person.to_str().unwrap());
    {
        let mut i = host.inner.0.lock().unwrap();
        let places = i.level.places.as_mut().unwrap();
        places.app_data = Some(app_data.clone());
        places.own_homes = vec![codex_home.clone()];
        for (thread, cwd) in [("no-project", &no_project), ("elsewhere", &elsewhere), ("quoted", &quoted)] {
            let generation = i.generation.clone();
            i.threads.push(json!({"generation": generation, "threadId": thread, "cwd": cwd}));
        }
    }
    let wire = Wire::attach(&host);
    // The person's home folder contains the App data folder: an edits level is not sent, nothing written.
    let before = counts(&host);
    let refused = send(&host, "turn/start", turn_params("thread")).err().unwrap();
    assert!(refused.contains("edits-level-reaches-app-folders"), "{refused}");
    assert_eq!(counts(&host), before, "nothing reserved, recorded or pending");
    assert!(wire.nothing());
    let status = host.snapshot();
    let row = status["threads"].as_array().unwrap().iter().find(|t| t["threadId"] == "thread").unwrap().clone();
    assert_eq!(row["level"]["refused"]["refused"], "edits-level-reaches-app-folders");
    assert_eq!(row["level"]["refused"]["which"], "app-data");
    assert_eq!(status["levelSendRefusal"]["threadId"], "thread");
    // A start in the person's home folder is refused the same way, before it is reserved.
    assert!(send(&host, "thread/start", json!({"cwd": person})).err().unwrap().contains("edits-level-reaches-app-folders"));
    // Supervised and full access remain sendable there.
    for id in ["supervised", "full"] {
        host.set_thread_level("thread", id).unwrap();
        send(&host, "turn/start", turn_params("thread")).unwrap();
        assert_eq!(wire.next()["params"]["approvalPolicy"], json!(cl::level(id).unwrap().approval_policy));
    }
    assert!(host.snapshot()["threads"].as_array().unwrap().iter().find(|t| t["threadId"] == "thread").unwrap()["level"].get("refused").is_none(), "cleared by a later send");
    // The no-project folder, in the App data folder by construction, gets the edits level.
    send(&host, "turn/start", turn_params("no-project")).unwrap();
    assert_eq!(wire.next()["params"]["sandboxPolicy"]["type"], "workspaceWrite");
    // A project elsewhere gets it; a project whose path has a double quote gets no sandboxed level.
    send(&host, "turn/start", turn_params("elsewhere")).unwrap();
    wire.next();
    host.set_thread_level("quoted", "supervised").unwrap();
    assert!(send(&host, "turn/start", turn_params("quoted")).err().unwrap().contains("project-path-breaks-codex-sandbox"));
    host.set_thread_level("quoted", "full").unwrap();
    send(&host, "turn/start", turn_params("quoted")).unwrap();
    wire.next();
    // Without the App's folders established (a Host whose start never set them), a sandboxed level is not sent.
    host.inner.0.lock().unwrap().level.places = None;
    assert!(send(&host, "turn/start", turn_params("elsewhere")).err().unwrap().contains("app-folders-not-established"));
    wire.close(&host);
    std::fs::remove_dir_all(&base).unwrap();
}

// ---- Items 5 and 6: the person's choice and the ledger ----

#[test]
fn a_choice_is_written_first_and_a_resend_writes_nothing() {
    let base = root("ledger");
    let host = ready_with_ledger(&base, "/invented");
    host.inner.0.lock().unwrap().default_level = None;
    let wire = Wire::attach(&host);
    let edits = cl::level("edits").unwrap();
    let chosen = host.choose_level(&LevelScope::Default, edits, &[]).unwrap();
    let rows = entries(&host, "level_chosen");
    assert_eq!(rows.len(), 1);
    assert_eq!(rows[0]["entryId"], chosen["ledgerEntry"]);
    assert_eq!(rows[0]["scope"], json!({"kind":"default-for-new-conversations"}));
    assert_eq!(rows[0]["level"], cl::recorded_values(edits));
    assert_eq!(rows[0]["previous"], Value::Null);
    assert!(rows[0].get("confirmation").is_none(), "a plain setting: no confirmation");
    assert!(rows[0].get("actor").is_none(), "the person's own setting carries no actor");
    assert_eq!(host.snapshot()["levelDefault"]["ledgerEntry"], chosen["ledgerEntry"]);
    // The same level sent twice to one conversation: one level_sent.
    for _ in 0..2 {
        send(&host, "turn/start", turn_params("thread")).unwrap();
        let written = wire.next();
        reply(&host, json!({"id": written["id"], "result": {"turn": {"id": opaque_id("turn-").unwrap(), "status": "completed", "items": []}}}));
    }
    let sent = entries(&host, "level_sent");
    assert_eq!(sent.len(), 1, "{sent:?}");
    assert_eq!((sent[0]["threadId"].as_str(), sent[0]["method"].as_str(), sent[0]["writeResult"].as_str(), sent[0]["chosen"].clone()),
               (Some("thread"), Some("turn/start"), Some("written"), chosen["ledgerEntry"].clone()));
    // A second choice names the first as previous, and the next send writes one more level_sent.
    let second = host.choose_level(&LevelScope::Default, cl::level("supervised").unwrap(), &[]).unwrap();
    assert_eq!(entries(&host, "level_chosen")[1]["previous"], chosen["ledgerEntry"]);
    send(&host, "turn/start", turn_params("thread")).unwrap();
    wire.next();
    let sent = entries(&host, "level_sent");
    assert_eq!(sent.len(), 2);
    assert_eq!(sent[1]["chosen"], second["ledgerEntry"]);
    wire.close(&host);
    std::fs::remove_dir_all(&base).unwrap();
}

#[test]
fn a_choice_the_ledger_does_not_take_changes_nothing() {
    let base = root("ledger-fails");
    let host = ready_with_ledger(&base, "/invented");
    host.inner.0.lock().unwrap().default_level = None;
    let database = crate::recovery::database_path(&base.join("recovery.ledger.jsonl"));
    std::fs::rename(&database, base.join("displaced")).unwrap();
    std::fs::create_dir(&database).unwrap();
    let revision = host.inner.0.lock().unwrap().level_revision;
    let refused = host.choose_level(&LevelScope::Default, cl::level("full").unwrap(), &[]).unwrap_err();
    assert!(refused.contains("nothing was changed"), "{refused}");
    let i = host.inner.0.lock().unwrap();
    assert!(i.default_level.is_none() && i.level.default_chosen.is_none());
    assert_eq!(i.level_revision, revision);
    drop(i);
    // No ledger at all: refused the same way.
    let unledgered = Host::new();
    assert!(unledgered.choose_level(&LevelScope::Default, cl::level("full").unwrap(), &[]).unwrap_err().contains("unavailable"));
    assert_eq!(unledgered.default_level().map(|l| l.id.as_str()), Some("edits"), "the test Host's level is unchanged");
    std::fs::remove_dir_all(&base).unwrap();
}

#[test]
fn a_default_choice_reaches_every_home_and_a_conversation_choice_only_its_own() {
    let base = root("homes");
    let account = ready_with_ledger(&base, "/invented");
    let key = Arc::new(Host::new_with_app_custody(account.app_runtime_custody().unwrap()).unwrap());
    let hosts = [Arc::clone(&account), Arc::clone(&key)];
    account.choose_level(&LevelScope::Default, cl::level("supervised").unwrap(), &hosts).unwrap();
    assert_eq!(key.default_level().unwrap().id, "supervised");
    account.choose_level(&LevelScope::Conversation("thread".into()), cl::level("full").unwrap(), &hosts).unwrap();
    assert_eq!(account.thread_level("thread").unwrap().id, "full");
    assert!(key.thread_level("thread").is_none());
    let row = entries(&account, "level_chosen").pop().unwrap();
    assert_eq!(row["scope"], json!({"kind":"conversation","home":"app-home:invented","threadId":"thread"}));
    assert!(account.choose_level(&LevelScope::Conversation("unknown".into()), cl::level("full").unwrap(), &hosts).unwrap_err().contains("not one this Codex home has open"));
    std::fs::remove_dir_all(&base).unwrap();
}

#[test]
fn a_start_reply_reports_agreement_and_a_differing_reply_refuses_the_next_turn_with_its_reason() {
    let base = root("reported");
    let host = ready_with_ledger(&base, "/invented");
    let wire = Wire::attach(&host);
    let chosen = host.choose_level(&LevelScope::Default, cl::level("edits").unwrap(), &[]).unwrap();
    let edits_sandbox = cl::level("edits").unwrap().sandbox_policy.clone();
    send(&host, "thread/start", json!({"cwd": "/invented"})).unwrap();
    let written = wire.next();
    reply(&host, json!({"id": written["id"], "result": {"thread": {"id": "created", "status": "idle"},
        "approvalPolicy": "on-request", "approvalsReviewer": "user", "sandbox": edits_sandbox}}));
    let sent = entries(&host, "level_sent");
    assert_eq!((sent[0]["method"].as_str(), sent[0]["threadId"].clone()), (Some("thread/start"), Value::Null));
    let reported = entries(&host, "level_reported");
    assert_eq!(reported.len(), 1);
    assert_eq!((reported[0]["threadId"].as_str(), reported[0]["agreement"].as_str(), reported[0]["sent"].clone(), reported[0]["chosen"].clone()),
               (Some("created"), Some("agrees"), sent[0]["entryId"].clone(), chosen["ledgerEntry"].clone()));
    // Its status, beside the raw fields the conversation row keeps.
    {
        let generation = g(&host);
        host.inner.0.lock().unwrap().threads.push(json!({"generation": generation, "threadId": "created", "cwd": "/invented",
            "approvalPolicy": "on-request", "sandbox": edits_sandbox, "activePermissionProfile": null}));
    }
    let row = host.snapshot()["threads"].as_array().unwrap().iter().find(|t| t["threadId"] == "created").unwrap().clone();
    assert_eq!(row["level"]["agreement"], "agrees");
    assert_eq!(row["level"]["chosen"]["id"], "edits");
    assert_eq!(row["level"]["chosen"]["ledgerEntry"], chosen["ledgerEntry"]);
    assert_eq!(row["level"]["sent"]["method"], "thread/start");
    assert_eq!(row["level"]["reported"]["from"], "thread/start");
    assert_eq!(row["level"]["takesEffect"], "now");
    assert_eq!(row["approvalPolicy"], "on-request", "the raw reported field is kept");
    // A resume whose reply reports another sandbox: differs, in the ledger and the status.
    send(&host, "thread/resume", json!({"threadId": "created", "excludeTurns": true})).unwrap();
    let written = wire.next();
    reply(&host, json!({"id": written["id"], "result": {"thread": {"id": "created", "status": "idle"},
        "approvalPolicy": "on-request", "approvalsReviewer": "user", "sandbox": {"type": "dangerFullAccess"}}}));
    assert_eq!(entries(&host, "level_reported")[1]["agreement"], "differs");
    let row = host.snapshot()["threads"].as_array().unwrap().iter().find(|t| t["threadId"] == "created").unwrap().clone();
    assert_eq!(row["level"]["agreement"], "differs");
    assert_eq!(row["level"]["reported"]["differs"][0], "sandbox={\"type\":\"dangerFullAccess\"}");
    // The next turn is refused, with its reason, and nothing is written.
    let before = counts(&host);
    let refused = send(&host, "turn/start", turn_params("created")).err().unwrap();
    assert!(refused.contains("codex-reported-another-level"), "{refused}");
    assert_eq!(counts(&host), before);
    assert!(wire.nothing());
    let row = host.snapshot()["threads"].as_array().unwrap().iter().find(|t| t["threadId"] == "created").unwrap().clone();
    assert_eq!(row["level"]["refused"]["refused"], "codex-reported-another-level");
    assert_eq!(row["level"]["refused"]["reported"]["sandbox"], json!({"type": "dangerFullAccess"}));
    // A resume whose reply agrees lifts it.
    send(&host, "thread/resume", json!({"threadId": "created", "excludeTurns": true})).unwrap();
    let written = wire.next();
    reply(&host, json!({"id": written["id"], "result": {"thread": {"id": "created", "status": "idle"},
        "approvalPolicy": "on-request", "approvalsReviewer": "user", "sandbox": edits_sandbox}}));
    send(&host, "turn/start", turn_params("created")).unwrap();
    assert_eq!(wire.next()["method"], "turn/start");
    wire.close(&host);
    std::fs::remove_dir_all(&base).unwrap();
}

#[test]
fn a_new_conversation_choice_is_recorded_as_that_conversations_when_the_reply_names_it() {
    let base = root("new-conversation");
    let host = ready_with_ledger(&base, "/invented");
    let wire = Wire::attach(&host);
    let chosen = host.choose_level(&LevelScope::NewConversation, cl::level("supervised").unwrap(), &[]).unwrap();
    assert!(entries(&host, "level_chosen").is_empty(), "no ledger scope names a conversation not yet created");
    send(&host, "thread/start", json!({"cwd": "/invented"})).unwrap();
    let written = wire.next();
    assert!(entries(&host, "level_sent").is_empty(), "held with its choice until the conversation is named");
    reply(&host, json!({"id": written["id"], "result": {"thread": {"id": "fresh"}}}));
    let row = entries(&host, "level_chosen").pop().unwrap();
    assert_eq!(row["entryId"], chosen["ledgerEntry"]);
    assert_eq!(row["scope"], json!({"kind":"conversation","home":"app-home:invented","threadId":"fresh"}));
    let sent = entries(&host, "level_sent").pop().unwrap();
    assert_eq!((sent["threadId"].as_str(), sent["chosen"].clone()), (Some("fresh"), chosen["ledgerEntry"].clone()));
    assert_eq!(host.thread_level("fresh").unwrap().id, "supervised");
    wire.close(&host);
    std::fs::remove_dir_all(&base).unwrap();
}

#[test]
fn at_launch_only_the_latest_exact_choice_in_a_scope_is_in_force() {
    let base = root("launch");
    let path = base.join("recovery.ledger.jsonl");
    let row = |id: &str, scope: Value, values: Value| json!({"kind":"level_chosen","session":"app-session:earlier","entryId":id,"at":"2026-11-14T12:00:00Z",
        "scope":scope,"level":values,"previous":null});
    let default = json!({"kind":"default-for-new-conversations"});
    let mut tampered = cl::recorded_values(cl::level("supervised").unwrap());
    tampered["approvalPolicy"] = json!("never");
    let mut old_table = cl::recorded_values(cl::level("edits").unwrap());
    old_table["tableDigest"] = json!("a".repeat(64));
    {
        let mut ledger = RecoveryLedger::open(path.clone()).unwrap();
        ledger.append(row("level-chosen:a", default.clone(), cl::recorded_values(cl::level("full").unwrap()))).unwrap();
        ledger.append(row("level-chosen:b", json!({"kind":"conversation","home":"app-home:mine","threadId":"t1"}), cl::recorded_values(cl::level("supervised").unwrap()))).unwrap();
        ledger.append(row("level-chosen:c", json!({"kind":"conversation","home":"app-home:other","threadId":"t2"}), cl::recorded_values(cl::level("full").unwrap()))).unwrap();
        ledger.append(row("level-chosen:d", json!({"kind":"conversation","home":"app-home:mine","threadId":"t3"}), old_table)).unwrap();
    }
    let host = Host::new_without_level();
    host.set_app_default_for_test(None);
    host.configure_recovery(path.clone()).unwrap();
    let read = host.read_levels_at_launch(Some("app-home:mine"));
    assert_eq!(read["state"], "read");
    assert_eq!(host.default_level().unwrap().id, "full");
    assert_eq!(host.thread_level("t1").unwrap().id, "supervised");
    assert!(host.thread_level("t2").is_none(), "another home's conversation");
    assert!(host.thread_level("t3").is_none(), "another table's digest is no level");
    assert_eq!(read["refused"][0]["entryId"], "level-chosen:d");
    assert_eq!(host.snapshot()["levelDefault"]["ledgerEntry"], "level-chosen:a");
    host.app_runtime_custody().unwrap().record_app_session_end(&[]).unwrap();
    drop(host);
    // A later default whose values differ from the table: no default at all, never the earlier one.
    {
        let mut ledger = RecoveryLedger::open(path.clone()).unwrap();
        ledger.append(row("level-chosen:e", default, tampered)).unwrap();
    }
    let host = Host::new_without_level();
    host.set_app_default_for_test(None);
    host.configure_recovery(path).unwrap();
    host.read_levels_at_launch(Some("app-home:mine"));
    assert!(host.default_level().is_none());
    assert!(host.snapshot()["levelDefault"].is_null());
    // A ledger that cannot be read: no level, and the reason is shown.
    let unread = Host::new_without_level();
    unread.set_app_default_for_test(None);
    let view = unread.read_levels_at_launch(None);
    assert_eq!(view["state"], "not-read");
    assert!(unread.default_level().is_none());
    assert_eq!(unread.snapshot()["levelLaunchRead"]["state"], "not-read");
    std::fs::remove_dir_all(&base).unwrap();
}

/// In production the level in force changes only through `choose_level` (the `set_level` command) and
/// `read_levels_at_launch_in`: no production source calls the setters the tests use, and `apply_chosen` is called
/// only from those two.
#[test]
fn production_code_changes_the_level_only_from_set_level_and_the_launch_read() {
    let dir = Path::new(env!("CARGO_MANIFEST_DIR")).join("src");
    let mut offending = Vec::new();
    for entry in std::fs::read_dir(&dir).unwrap() {
        let path = entry.unwrap().path();
        let name = path.file_name().unwrap().to_string_lossy().into_owned();
        if !name.ends_with(".rs") || name.ends_with("_tests.rs") || name == "pinned_codex_observations.rs" { continue; }
        let text = without_test_modules(&std::fs::read_to_string(&path).unwrap());
        for setter in [".set_default_level(", ".set_thread_level(", ".choose_new_conversation_level(", "set_default_level(\"", "Self::apply_chosen("] {
            for (at, _) in text.match_indices(setter) {
                let function = text[..at].rfind("fn ").map(|f| text[f + 3..].split('(').next().unwrap_or_default().trim().to_owned()).unwrap_or_default();
                let allowed = name == "hosting_level.rs" && setter == "Self::apply_chosen(" && ["choose_level", "read_levels_at_launch_in"].contains(&function.as_str());
                if !allowed { offending.push(format!("{name}: {setter} in fn {function}")); }
            }
        }
    }
    assert!(offending.is_empty(), "{offending:#?}");
    let level_state = without_test_modules(&std::fs::read_to_string(dir.join("hosting_level.rs")).unwrap());
    assert_eq!(level_state.matches("Self::apply_chosen(").count(), 7,
        "choose_level (a session-only choice here and in the other homes; a new conversation; a recorded choice here and in the other homes) and the launch read (a recorded choice; the App's default)");
}

/// The source with each `#[cfg(test)]` item (a module, function or block) removed.
fn without_test_modules(text: &str) -> String {
    let mut out = String::new();
    let mut rest = text;
    while let Some(at) = rest.find("#[cfg(test)]") {
        out.push_str(&rest[..at]);
        let after = &rest[at + "#[cfg(test)]".len()..];
        // Skip to the end of the item: a `;` before any `{`, or the matching `}`.
        let open = after.find('{');
        let semi = after.find(';');
        match (open, semi) {
            (Some(o), Some(s)) if s < o => rest = &after[s + 1..],
            (Some(o), _) => {
                let mut depth = 0usize;
                let mut end = after.len();
                for (i, ch) in after[o..].char_indices() {
                    match ch { '{' => depth += 1, '}' => { depth -= 1; if depth == 0 { end = o + i + 1; break; } } _ => {} }
                }
                rest = &after[end..];
            }
            (None, Some(s)) => rest = &after[s + 1..],
            (None, None) => rest = "",
        }
    }
    out.push_str(rest);
    out
}

// ---- Item 8: lasting rules ----

#[test]
fn lasting_rules_are_read_for_the_home_and_after_an_answer_that_adds_one() {
    let base = root("rules");
    let host = Host::new();
    host.read_lasting_rules(Some(&base));
    assert_eq!(host.lasting_rules().unwrap()["lastingRules"]["state"], "none");
    assert_eq!(host.lasting_rules().unwrap()["home"], base.to_string_lossy().as_ref());
    assert!(level_state::adds_lasting_rule(&json!({"decision": {"acceptWithExecpolicyAmendment": {"execpolicy_amendment": ["ls"]}}})));
    assert!(level_state::adds_lasting_rule(&json!({"decision": {"applyNetworkPolicyAmendment": {"host": "x"}}})));
    assert!(!level_state::adds_lasting_rule(&json!({"decision": "accept"})));
    std::fs::remove_dir_all(&base).unwrap();
}

#[test]
fn a_relative_project_is_checked_where_codex_resolves_it() {
    let base = root("relative");
    let home = base.join("account");
    let work = base.join("work");
    for d in [&home, &work] { std::fs::create_dir_all(d).unwrap(); }
    let host = ready_with_ledger(&base, work.to_str().unwrap());
    {
        let mut i = host.inner.0.lock().unwrap();
        let places = i.level.places.as_mut().unwrap();
        places.own_homes = vec![home.clone()];
        places.process_cwd = Some(base.clone());
    }
    let wire = Wire::attach(&host);
    // "." is the folder Codex was started in, which contains the home: refused, whatever this process's folder is.
    assert!(send(&host, "thread/start", json!({"cwd": "."})).err().unwrap().contains("edits-level-reaches-app-folders"));
    assert!(send(&host, "thread/start", json!({"cwd": "work"})).is_ok());
    wire.next();
    wire.close(&host);
    std::fs::remove_dir_all(&base).unwrap();
}

// ---- B1: the App's default level ----

/// A ready Host as production makes it (no level in force), with the App's own folders established, and no ledger.
fn ready_unledgered(cwd: &str) -> Arc<Host> {
    let host = Arc::new(Host::new_without_level());
    host.inner.0.lock().unwrap().app_session = "app-session:invented".into();
    let generation = g(&host);
    let mut i = host.inner.0.lock().unwrap();
    i.state = "ready".into();
    i.home = "level-home".into();
    i.spawn_counter = 1;
    i.generation = generation.clone();
    i.journal.begin_generation(generation.clone());
    i.threads.push(json!({"generation": generation, "threadId": "thread", "cwd": cwd}));
    i.level.places = Some(level_state::Places { home_identity: Some("app-home:invented".into()), ..level_state::Places::for_test() });
    drop(i);
    host
}
fn thread_row(host: &Host, thread: &str) -> Value {
    host.snapshot()["threads"].as_array().unwrap().iter().find(|t| t["threadId"] == thread).unwrap().clone()
}

#[test]
fn a_complete_read_with_no_choice_puts_the_apps_default_in_force_and_writes_nothing() {
    let base = root("default");
    let host = ready_with_ledger(&base, "/invented");
    {
        let mut i = host.inner.0.lock().unwrap();
        i.default_level = None;
    }
    host.set_app_default_for_test(Some("full"));
    let view = host.read_levels_at_launch(Some("app-home:invented"));
    assert_eq!(view, json!({"state": "read", "accepted": [], "refused": [], "appDefault": "full"}));
    assert_eq!(host.default_level().unwrap().id, "full");
    let status = host.snapshot();
    assert_eq!(status["levelDefault"]["origin"], "app-default");
    assert_eq!(status["levelDefault"]["originSentence"], cl::APP_DEFAULT_SENTENCE);
    assert_eq!(status["levelDefault"]["explanation"], cl::APP_DEFAULT_EXPLAINED);
    assert_eq!(status["levelDefault"]["ledgerEntry"], Value::Null);
    assert_eq!(status["levelAppDefault"], "full");
    assert!(status["levelSessionOnlyOffered"].is_null(), "an empty ledger is the default's case, not the session-only one");
    // Conversations without their own choice take it, and the status says where it comes from.
    assert_eq!(thread_row(&host, "thread")["level"]["chosen"]["origin"], "app-default");
    // Sending it writes nothing: the default is never a choice in the ledger.
    let wire = Wire::attach(&host);
    send(&host, "turn/start", turn_params("thread")).unwrap();
    assert_eq!(wire.next()["params"]["sandboxPolicy"]["type"], "dangerFullAccess");
    for kind in ["level_chosen", "level_sent", "level_reported"] {
        assert!(entries(&host, kind).is_empty(), "{kind}");
    }
    // The person choosing the same level is a recorded choice, and the origin changes.
    let chosen = host.choose_level(&LevelScope::Default, cl::level("full").unwrap(), &[]).unwrap();
    assert_eq!(entries(&host, "level_chosen").len(), 1);
    let status = host.snapshot();
    assert_eq!(status["levelDefault"]["origin"], "chosen");
    assert_eq!(status["levelDefault"]["ledgerEntry"], chosen["ledgerEntry"]);
    assert!(status["levelDefault"].get("originSentence").is_none());
    wire.close(&host);
    std::fs::remove_dir_all(&base).unwrap();
}

#[test]
fn a_recorded_choice_wins_over_the_default_and_an_invalid_one_leaves_the_default() {
    let base = root("default-recorded");
    let path = base.join("recovery.ledger.jsonl");
    let row = |id: &str, values: Value| json!({"kind":"level_chosen","session":"app-session:earlier","entryId":id,"at":"2026-11-14T12:00:00Z",
        "scope":{"kind":"default-for-new-conversations"},"level":values,"previous":null});
    {
        let mut ledger = RecoveryLedger::open(path.clone()).unwrap();
        ledger.append(row("level-chosen:a", cl::recorded_values(cl::level("supervised").unwrap()))).unwrap();
    }
    let host = Host::new_without_level();
    host.configure_recovery(path.clone()).unwrap();
    let view = host.read_levels_at_launch(Some("app-home:mine"));
    assert!(view.get("appDefault").is_none());
    assert_eq!(host.default_level().unwrap().id, "supervised");
    assert_eq!(host.snapshot()["levelDefault"]["origin"], "chosen");
    host.app_runtime_custody().unwrap().record_app_session_end(&[]).unwrap();
    drop(host);
    // The latest entry does not match the table: no valid choice, so the App's default, never the earlier entry.
    let mut tampered = cl::recorded_values(cl::level("supervised").unwrap());
    tampered["approvalPolicy"] = json!("never");
    { RecoveryLedger::open(path.clone()).unwrap().append(row("level-chosen:b", tampered)).unwrap(); }
    let host = Host::new_without_level();
    host.configure_recovery(path).unwrap();
    let view = host.read_levels_at_launch(Some("app-home:mine"));
    assert_eq!(view["refused"][0]["entryId"], "level-chosen:b");
    assert_eq!(view["appDefault"], "full");
    assert_eq!(host.default_level().unwrap().id, "full");
    assert_eq!(host.snapshot()["levelDefault"]["origin"], "app-default");
    std::fs::remove_dir_all(&base).unwrap();
}

/// With no default (`None`), the launch read gives exactly what it gave before the default existed (f32b96b67):
/// the same bytes, for an empty ledger, a ledger with choices and an unread ledger.
#[test]
fn with_no_default_the_launch_read_is_byte_for_byte_as_before() {
    let base = root("default-none");
    let path = base.join("recovery.ledger.jsonl");
    let empty = Host::new_without_level();
    empty.set_app_default_for_test(None);
    empty.configure_recovery(path.clone()).unwrap();
    assert_eq!(serde_json::to_string(&empty.read_levels_at_launch(Some("app-home:mine"))).unwrap(), r#"{"accepted":[],"refused":[],"state":"read"}"#);
    assert!(empty.default_level().is_none());
    assert!(empty.snapshot()["levelDefault"].is_null());
    empty.app_runtime_custody().unwrap().record_app_session_end(&[]).unwrap();
    drop(empty);
    let mut tampered = cl::recorded_values(cl::level("edits").unwrap());
    tampered["sandbox"] = json!("read-only");
    {
        let mut ledger = RecoveryLedger::open(path.clone()).unwrap();
        let row = |id: &str, scope: Value, values: Value| json!({"kind":"level_chosen","session":"app-session:earlier","entryId":id,"at":"2026-11-14T12:00:00Z","scope":scope,"level":values,"previous":null});
        ledger.append(row("level-chosen:x", json!({"kind":"conversation","home":"app-home:mine","threadId":"t1"}), cl::recorded_values(cl::level("full").unwrap()))).unwrap();
        ledger.append(row("level-chosen:y", json!({"kind":"default-for-new-conversations"}), tampered)).unwrap();
    }
    let host = Host::new_without_level();
    host.set_app_default_for_test(None);
    host.configure_recovery(path).unwrap();
    assert_eq!(serde_json::to_string(&host.read_levels_at_launch(Some("app-home:mine"))).unwrap(),
        r#"{"accepted":[{"entryId":"level-chosen:x","levelId":"full"}],"refused":[{"entryId":"level-chosen:y","reason":"The recorded level does not match the App's level table exactly; choose a level again."}],"state":"read"}"#);
    assert!(host.default_level().is_none());
    assert_eq!(host.thread_level("t1").unwrap().id, "full");
    let unread = Host::new_without_level();
    unread.set_app_default_for_test(None);
    assert_eq!(serde_json::to_string(&unread.read_levels_at_launch(None)).unwrap(),
        r#"{"reason":"The App ledger is unavailable, so no level is in force; choose a level before any conversation.","state":"not-read"}"#);
    assert!(unread.default_level().is_none());
    std::fs::remove_dir_all(&base).unwrap();
}

#[test]
fn an_unreadable_ledger_never_takes_the_default() {
    let host = ready_unledgered("/invented");
    host.set_app_default_for_test(Some("full"));
    host.inner.0.lock().unwrap().recovery_initialization_error = Some("invented raw ledger failure".into());
    let view = host.read_levels_at_launch(Some("app-home:invented"));
    assert_eq!(view["state"], "not-read");
    assert!(view.get("appDefault").is_none());
    assert!(host.default_level().is_none());
}

// ---- B1: a level for this session only ----

/// The failed read only makes the choice available: no level is in force until the person chooses.
#[test]
fn a_failed_read_alone_puts_no_level_in_force_and_only_offers_the_choice() {
    let host = ready_unledgered("/invented");
    host.inner.0.lock().unwrap().recovery_initialization_error = Some("invented raw ledger failure".into());
    host.read_levels_at_launch(Some("app-home:invented"));
    assert!(host.default_level().is_none());
    let status = host.snapshot();
    assert_eq!(status["levelSessionOnlyOffered"]["reason"], cl::RECORDS_NOT_READ);
    assert_eq!(status["levelSessionOnlyOffered"]["detail"], json!({"text": "invented raw ledger failure", "standing": cl::NOT_THE_APPS_TEXT}));
    assert!(status["levelDefault"].is_null());
    let wire = Wire::attach(&host);
    assert!(send(&host, "turn/start", turn_params("thread")).err().unwrap().contains("no level chosen"));
    assert!(wire.nothing());
    // The person's explicit choice puts it in force, held in memory only.
    let out = host.choose_level(&LevelScope::Default, cl::level("supervised").unwrap(), &[]).unwrap();
    assert_eq!((out["origin"].as_str(), out["ledgerEntry"].clone()), (Some("session-only"), Value::Null));
    let status = host.snapshot();
    assert_eq!(status["levelDefault"]["origin"], "session-only");
    assert_eq!(status["levelDefault"]["originSentence"], cl::SESSION_ONLY_SENTENCE);
    assert_eq!(status["levelDefault"]["sessionOnly"]["reason"], cl::RECORDS_NOT_READ);
    send(&host, "turn/start", turn_params("thread")).unwrap();
    assert_eq!(wire.next()["params"]["approvalPolicy"], "untrusted");
    wire.close(&host);
}

#[test]
fn a_session_only_choice_takes_effect_from_the_next_turn_while_a_turn_runs() {
    let host = ready_unledgered("/invented");
    host.read_levels_at_launch(Some("app-home:invented"));
    assert_eq!(host.snapshot()["levelSessionOnlyOffered"]["reason"], cl::RECORDS_UNAVAILABLE);
    host.choose_level(&LevelScope::Default, cl::level("supervised").unwrap(), &[]).unwrap();
    let wire = Wire::attach(&host);
    send(&host, "turn/start", turn_params("thread")).unwrap();
    let written = wire.next();
    reply(&host, json!({"id": written["id"], "result": {"turn": {"id": "turn-running", "status": "inProgress", "items": []}}}));
    assert_eq!(thread_row(&host, "thread")["level"]["takesEffect"], "now");
    host.choose_level(&LevelScope::Conversation("thread".into()), cl::level("full").unwrap(), &[]).unwrap();
    let level = thread_row(&host, "thread")["level"].clone();
    assert_eq!(level["chosen"]["origin"], "session-only");
    assert_eq!(level["takesEffect"], "from-next-turn", "{level}");
    wire.close(&host);
}

#[test]
fn a_session_only_choice_is_never_offered_on_an_empty_ledger_and_a_complete_read_drops_it() {
    // An empty ledger whose write then fails: an error, never a session-only choice.
    let base = root("session-empty");
    let host = ready_with_ledger(&base, "/invented");
    host.inner.0.lock().unwrap().default_level = None;
    host.read_levels_at_launch(Some("app-home:invented"));
    let database = crate::recovery::database_path(&base.join("recovery.ledger.jsonl"));
    std::fs::rename(&database, base.join("displaced")).unwrap();
    std::fs::create_dir(&database).unwrap();
    assert!(host.choose_level(&LevelScope::Default, cl::level("supervised").unwrap(), &[]).unwrap_err().contains("nothing was changed"));
    assert_eq!(host.default_level().unwrap().id, "full", "the App's default, unchanged");
    std::fs::remove_dir_all(&database).unwrap();
    std::fs::rename(base.join("displaced"), &database).unwrap();
    // A session-only choice, then the ledger is read whole: the read governs, and the choice is dropped.
    let unread = ready_unledgered("/invented");
    unread.read_levels_at_launch(Some("app-home:invented"));
    unread.choose_level(&LevelScope::Default, cl::level("supervised").unwrap(), &[]).unwrap();
    unread.choose_level(&LevelScope::Conversation("thread".into()), cl::level("edits").unwrap(), &[]).unwrap();
    let other = root("session-later");
    let ledger = RecoveryLedger::open(other.join("recovery.ledger.jsonl")).unwrap();
    unread.inner.0.lock().unwrap().recovery = Some(Arc::new(Mutex::new(ledger)));
    unread.set_app_default_for_test(None);
    unread.read_levels_at_launch(Some("app-home:invented"));
    assert!(unread.default_level().is_none(), "dropped");
    assert!(unread.thread_level("thread").is_none(), "dropped");
    assert!(unread.snapshot()["levelSessionOnlyOffered"].is_null());
    // A later successful save is a real recorded choice.
    let out = unread.choose_level(&LevelScope::Default, cl::level("edits").unwrap(), &[]).unwrap();
    assert_eq!(out["origin"], "chosen");
    assert_eq!(unread.snapshot()["levelDefault"]["origin"], "chosen");
    std::fs::remove_dir_all(&base).unwrap();
    std::fs::remove_dir_all(&other).unwrap();
}

// ---- B1: the project trust entry ----

/// A stand-in for Codex that answers each `config/read` with `answer` and passes every frame on, in order.
struct Responder {
    child: std::process::Child,
    frames: Receiver<Value>,
}
impl Responder {
    fn attach(host: &Arc<Host>, answer: impl Fn(&Value) -> Value + Send + 'static) -> Self {
        let mut child = Command::new("/bin/cat").env_clear().stdin(Stdio::piped()).stdout(Stdio::piped()).stderr(Stdio::null()).spawn().unwrap();
        *host.stdin.lock().unwrap() = child.stdin.take();
        let stdout = child.stdout.take().unwrap();
        let (tx, rx) = channel();
        let me = Arc::clone(host);
        std::thread::spawn(move || {
            let mut reader = BufReader::new(stdout);
            loop {
                let mut line = String::new();
                match reader.read_line(&mut line) {
                    Ok(0) | Err(_) => break,
                    Ok(_) => {
                        let frame: Value = serde_json::from_str(&line).unwrap();
                        if frame["method"] == "config/read" {
                            let mut reply = answer(&frame);
                            reply["id"] = frame["id"].clone();
                            me.on_line(&serde_json::to_vec(&reply).unwrap(), &g(&me));
                        }
                        let _ = tx.send(frame);
                    }
                }
            }
        });
        Responder { child, frames: rx }
    }
    /// The next frame that is not a `config/read`, and the `config/read` frames before it.
    fn next_sent(&self) -> (Vec<Value>, Value) {
        let mut reads = Vec::new();
        loop {
            let frame = self.frames.recv_timeout(Duration::from_secs(5)).expect("a frame was written");
            if frame["method"] == "config/read" { reads.push(frame); } else { return (reads, frame); }
        }
    }
    fn close(mut self, host: &Host) {
        *host.stdin.lock().unwrap() = None;
        assert!(self.child.wait().unwrap().success());
    }
}
/// A whole `config/read` result whose user layer holds `projects`.
fn layers_with(projects: Value) -> Value {
    json!({"result": {"config": {}, "origins": {}, "layers": [
        {"name": {"type": "user", "file": "/invented/home/config.toml", "profile": null}, "version": "1", "config": {"projects": projects}},
        {"name": {"type": "sessionFlags"}, "version": "1", "config": {}}]}})
}
/// A project folder holding `.git` (with HEAD), a subfolder to work in, and a second spelling of the project
/// through a link.
fn git_project(name: &str) -> (PathBuf, PathBuf, PathBuf, PathBuf) {
    let base = root(name);
    let project = base.join("project");
    std::fs::create_dir_all(project.join(".git")).unwrap();
    std::fs::write(project.join(".git").join("HEAD"), b"ref: refs/heads/main\n").unwrap();
    std::fs::create_dir_all(project.join("sub")).unwrap();
    let alias = base.join("alias");
    std::os::unix::fs::symlink(&project, &alias).unwrap();
    (base, project, alias, PathBuf::new())
}
fn trusting_host(base: &Path, cwd: &Path, level: &str) -> Arc<Host> {
    // Each Host its own ledger: a Host left without an ended session holds its ledger's history.
    let ledger = base.join(opaque_id("ledger-").unwrap());
    std::fs::create_dir_all(&ledger).unwrap();
    let host = ready_with_ledger(&ledger, cwd.to_str().unwrap());
    host.set_default_level(level).unwrap();
    host.inner.0.lock().unwrap().level.trust_reads = true;
    host
}
fn key(path: &Path) -> String { path.to_string_lossy().into_owned() }

#[test]
fn each_start_resume_and_fork_carries_exactly_one_trust_entry_for_the_project_root_read_just_before() {
    let (base, project, _, _) = git_project("trust-unmarked");
    let cwd = project.join("sub");
    // Full access, where Codex would otherwise write `trusted` into the person's settings: the explicit entry is
    // sent every time, so Codex's "no trust entry" condition never holds (thread_processor.rs:1478-1482).
    let host = trusting_host(&base, &cwd, "full");
    let wire = Responder::attach(&host, |_| layers_with(json!({"/somewhere/else": {"trust_level": "trusted"}})));
    for (method, params) in [("thread/start", json!({"cwd": cwd})), ("thread/resume", json!({"threadId": "thread", "excludeTurns": true})),
                             ("thread/fork", json!({"threadId": "thread", "deferGoalContinuation": true}))] {
        send(&host, method, params).unwrap();
        let (reads, frame) = wire.next_sent();
        assert_eq!(reads.len(), 1, "{method}: one settings reading, just before");
        assert_eq!(reads[0]["params"], json!({"cwd": key(&cwd), "includeLayers": true}), "{method}");
        assert_eq!(frame["method"], method);
        assert_eq!(frame["params"]["config"]["projects"], json!({key(&project): {"trust_level": "untrusted"}}), "{method}: the root, nearest .git");
    }
    let row = thread_row(&host, "thread");
    assert_eq!(row["level"]["projectTrust"]["case"], "not-used");
    assert_eq!(row["level"]["projectTrust"]["lines"], json!([cl::TRUST_NOT_USED]));
    wire.close(&host);
    std::fs::remove_dir_all(&base).unwrap();
}

#[test]
fn a_trusted_mark_is_honoured_under_either_spelling_and_sent_under_the_one_codex_looks_up_first() {
    let (base, project, alias, _) = git_project("trust-marked");
    // Working through the link: Codex looks up the canonical spelling first, then the one as given.
    let cwd = alias.join("sub");
    for marked in [key(&project), key(&alias)] {
        let host = trusting_host(&base, &cwd, "edits");
        let projects = json!({marked.clone(): {"trust_level": "trusted"}});
        let wire = Responder::attach(&host, move |_| layers_with(projects.clone()));
        send(&host, "thread/resume", json!({"threadId": "thread", "excludeTurns": true})).unwrap();
        let (_, frame) = wire.next_sent();
        assert_eq!(frame["params"]["config"]["projects"], json!({key(&project): {"trust_level": "trusted"}}), "marked under {marked}");
        let trust = thread_row(&host, "thread")["level"]["projectTrust"].clone();
        assert_eq!(trust["case"], "trusted");
        assert_eq!(trust["matchedKey"], json!(marked));
        let line = trust["lines"][0].as_str().unwrap();
        assert!(line.starts_with(cl::TRUST_TRUSTED_PREFIX) && line.ends_with(cl::TRUST_TRUSTED_SUFFIX) && line.contains(trust["readAt"].as_str().unwrap()), "{line}");
        wire.close(&host);
    }
    std::fs::remove_dir_all(&base).unwrap();
}

#[test]
fn an_untrusted_mark_is_preserved_and_a_failed_or_limited_reading_sends_untrusted() {
    let (base, project, _, _) = git_project("trust-other");
    let cwd = project.clone();
    let cases: [(&str, Value, &str); 4] = [
        ("marked untrusted", layers_with(json!({key(&project): {"trust_level": "untrusted"}})), "marked-untrusted"),
        ("an error reply", json!({"error": {"code": -32603, "message": "invented, may quote configuration"}}), "not-read"),
        ("no layers", json!({"result": {"config": {}, "origins": {}, "layers": null}}), "not-read"),
        ("a reply of another shape", json!({"result": {"invented": true}}), "not-read"),
    ];
    for (what, answer, case) in cases {
        let host = trusting_host(&base, &cwd, "edits");
        let wire = Responder::attach(&host, move |_| answer.clone());
        send(&host, "thread/resume", json!({"threadId": "thread", "excludeTurns": true})).unwrap();
        let (_, frame) = wire.next_sent();
        assert_eq!(frame["params"]["config"]["projects"], json!({key(&project): {"trust_level": "untrusted"}}), "{what}");
        let trust = thread_row(&host, "thread")["level"]["projectTrust"].clone();
        assert_eq!(trust["case"], case, "{what}");
        match case {
            "marked-untrusted" => assert_eq!(trust["lines"], json!([cl::TRUST_MARKED_UNTRUSTED, cl::TRUST_NOT_USED])),
            _ => {
                assert_eq!(trust["lines"], json!([cl::TRUST_NOT_READ, cl::TRUST_NOT_USED]), "{what}");
                assert!(!trust.to_string().contains("may quote configuration"), "{what}: a native message is not passed on");
            }
        }
        wire.close(&host);
    }
    std::fs::remove_dir_all(&base).unwrap();
}

#[test]
fn a_reading_that_is_no_longer_current_is_never_trusted() {
    let host = ready_with_ledger(&root("trust-stale"), "/invented");
    let mut reading = cl::TrustReading::not_read(PathBuf::from("/invented"), cl::TRUST_READ_FAILED, None);
    reading.case = cl::TrustCase::Trusted { key: "/invented".into() };
    let i = host.inner.0.lock().unwrap();
    reading.generation = Some(json!({"generation": i.generation, "configWrites": i.level.config_writes}));
    assert_eq!(Host::trust_current(&i, reading.clone()).trust_level(), "trusted");
    let mut written = reading.clone();
    written.generation = Some(json!({"generation": i.generation, "configWrites": i.level.config_writes + 1}));
    assert_eq!(Host::trust_current(&i, written).trust_level(), "untrusted", "a configuration write since");
    let mut other = reading;
    other.generation = Some(json!({"generation": {"invented": 1}, "configWrites": i.level.config_writes}));
    assert_eq!(Host::trust_current(&i, other).trust_level(), "untrusted", "another generation");
}

/// The trust reading leaves the newest configuration proof as it was: a provider reading admitted before it is
/// still current after it.
#[test]
fn the_trust_reading_does_not_supersede_an_earlier_configuration_proof() {
    let base = root("trust-proof");
    let host = trusting_host(&base, Path::new("/invented"), "full");
    let wire = Responder::attach(&host, |_| layers_with(json!({})));
    let proof = host.request_reading("config/read", json!({"cwd": "/invented", "includeLayers": false}), json!({"kind":"person-directed"}), &g(&host), true,
        std::time::Instant::now() + Duration::from_secs(5)).unwrap();
    host.wait_source_response(&proof, Duration::from_secs(5)).unwrap();
    assert_eq!(host.reading_current_for_test().as_deref(), Some(proof.request_ref()));
    send(&host, "thread/resume", json!({"threadId": "thread", "excludeTurns": true})).unwrap();
    let (reads, _) = wire.next_sent();
    assert_eq!(reads.len(), 2, "the proof's reading, then the trust reading");
    assert_eq!(host.reading_current_for_test().as_deref(), Some(proof.request_ref()), "still the newest proof");
    wire.close(&host);
    std::fs::remove_dir_all(&base).unwrap();
}

// ---- B1: frame post-conditions ----

/// Start, resume and fork carry exactly these configuration keys: the level's workspace options (edits levels
/// only), and `projects` with one entry; never `bypass_hook_trust` or `hooks.state`; and no frame is a remote
/// control request.
#[test]
fn start_resume_and_fork_carry_exactly_the_expected_configuration_keys() {
    for id in ["supervised", "edits", "edits-network", "edits-no-asking", "full"] {
        let base = root("post");
        let host = trusting_host(&base, Path::new("/invented"), id);
        let wire = Responder::attach(&host, |_| layers_with(json!({})));
        for (method, params) in [("thread/start", json!({"cwd": "/invented"})), ("thread/resume", json!({"threadId": "thread", "excludeTurns": true})),
                                 ("thread/fork", json!({"threadId": "thread", "deferGoalContinuation": true}))] {
            send(&host, method, params).unwrap();
            let (reads, frame) = wire.next_sent();
            let config = frame["params"]["config"].as_object().unwrap();
            let mut keys: Vec<&str> = config.keys().map(String::as_str).collect();
            keys.sort();
            let want: Vec<&str> = if cl::level(id).unwrap().workspace_write.is_some() { vec!["projects", "sandbox_workspace_write"] } else { vec!["projects"] };
            assert_eq!(keys, want, "{id} {method}");
            assert_eq!(config["projects"].as_object().unwrap().len(), 1, "{id} {method}");
            for never in cl::NEVER_SENT_CONFIG { assert!(!config.contains_key(never), "{id} {method}: {never}"); }
            assert!(config.get("hooks").is_none(), "{id} {method}");
            for f in reads.iter().chain([&frame]) { assert!(!f["method"].as_str().unwrap().starts_with("remoteControl/"), "{f}"); }
        }
        assert!(host.client_requests().iter().all(|r| !r["method"].as_str().unwrap_or_default().starts_with("remoteControl/")));
        wire.close(&host);
        std::fs::remove_dir_all(&base).unwrap();
    }
    // The post-condition itself refuses a second entry, a forbidden key, and an entry on a turn.
    let ok = json!({"config": {"projects": {"/p": {"trust_level": "untrusted"}}}});
    assert!(cl::config_post_condition(&ok, Method::ThreadStart).is_ok());
    for (bad, method) in [
        (json!({"config": {"projects": {"/p": {"trust_level": "untrusted"}, "/q": {"trust_level": "untrusted"}}}}), Method::ThreadStart),
        (json!({"config": {"projects": {}}}), Method::ThreadResume),
        (json!({}), Method::ThreadFork),
        (json!({"config": {"projects": {"/p": {"trust_level": "trusted", "extra": 1}}}}), Method::ThreadStart),
        (json!({"config": {"projects": {"/p": {"trust_level": "untrusted"}}, "bypass_hook_trust": true}}), Method::ThreadStart),
        (json!({"config": {"projects": {"/p": {"trust_level": "untrusted"}}, "hooks.state": {}}}), Method::ThreadStart),
        (json!({"config": {"projects": {"/p": {"trust_level": "untrusted"}}, "hooks": {"state": {}}}}), Method::ThreadStart),
        (json!({"config": {"projects": {"/p": {"trust_level": "untrusted"}}}}), Method::TurnStart),
    ] {
        assert!(cl::config_post_condition(&bad, method).is_err(), "{bad}");
    }
    // A frame changed after the merge to carry a second entry is refused before anything is written.
    let base = root("post-tamper");
    let host = trusting_host(&base, Path::new("/invented"), "full");
    let wire = Responder::attach(&host, |_| layers_with(json!({})));
    *host.after_level_merge.lock().unwrap() = Some(Box::new(|p: &mut Value| { p["config"]["projects"]["/second"] = json!({"trust_level": "untrusted"}); }));
    assert!(send(&host, "thread/start", json!({"cwd": "/invented"})).is_err());
    *host.after_level_merge.lock().unwrap() = Some(Box::new(|p: &mut Value| { p["config"]["bypass_hook_trust"] = json!(true); }));
    assert!(send(&host, "thread/start", json!({"cwd": "/invented"})).is_err());
    wire.close(&host);
    std::fs::remove_dir_all(&base).unwrap();
}


// ---- The App's default needs positive evidence that the person has never chosen ----

/// The account home as the App made it, with or without state from an earlier Codex start in it.
fn account_home(base: &Path, started_before: bool) -> PathBuf {
    let home = base.join("homes").join("account");
    std::fs::create_dir_all(&home).unwrap();
    if started_before { std::fs::write(home.join(cl::CODEX_STATE_NAME), b"invented").unwrap(); }
    home
}
/// An entry of an earlier App session, as each launch writes one.
fn earlier_session(host: &Host) {
    let ledger = host.inner.0.lock().unwrap().recovery.clone().unwrap();
    ledger.lock().unwrap().append(json!({"kind":"session_started","session":"invented-earlier-session","at":"2026-11-01T00:00:00Z",
        "previousSessionEnd":"none","candidate":"invented"})).unwrap();
}

/// Used before and never chose: a complete record holding an earlier session and no choice takes the default,
/// whatever this home holds.
#[test]
fn a_record_of_earlier_use_with_no_choice_takes_the_apps_default() {
    let base = root("used-before");
    let host = ready_with_ledger(&base.join("data"), "/invented");
    earlier_session(&host);
    host.inner.0.lock().unwrap().default_level = None;
    host.set_app_default_for_test(Some("full"));
    let view = host.read_levels_at_launch_in(Some("app-home:invented"), Some(&account_home(&base, true)));
    assert_eq!(view["appDefault"], "full");
    assert!(view.get("recordMissing").is_none());
    assert_eq!(host.snapshot()["levelDefault"]["origin"], "app-default");
    assert!(host.snapshot()["levelRecordMissing"].is_null());
    std::fs::remove_dir_all(base).unwrap();
}

/// Chose, then the record was removed, where this home has been used: the record is missing, no default applies,
/// the person is told so, and their choice is recorded normally.
#[test]
fn a_removed_record_where_this_home_has_been_used_is_missing_and_takes_no_default() {
    let base = root("removed");
    let home = account_home(&base, true);
    {
        let before = ready_with_ledger(&base.join("data"), "/invented");
        before.choose_level(&LevelScope::Default, cl::level("supervised").unwrap(), &[]).unwrap();
        assert_eq!(entries(&before, "level_chosen").len(), 1);
    }
    // A command removed the record, and nothing else.
    std::fs::remove_dir_all(base.join("data")).unwrap();
    let host = ready_with_ledger(&base.join("data"), "/invented");
    host.inner.0.lock().unwrap().default_level = None;
    host.set_app_default_for_test(Some("full"));
    let view = host.read_levels_at_launch_in(Some("app-home:invented"), Some(&home));
    assert_eq!(view["recordMissing"], cl::RECORD_MISSING_SENTENCE);
    assert!(view.get("appDefault").is_none(), "no default is named");
    assert!(host.default_level().is_none(), "nothing is in force");
    let status = host.snapshot();
    assert_eq!(status["levelRecordMissing"], cl::RECORD_MISSING_SENTENCE);
    assert!(status["levelDefault"]["origin"] != "app-default");
    assert!(send(&host, "turn/start", turn_params("thread")).is_err(), "no conversation runs until the person chooses");
    // The ledger can be written: the person's choice is recorded normally, and the missing record is answered.
    host.choose_level(&LevelScope::Default, cl::level("supervised").unwrap(), &[]).unwrap();
    assert_eq!(entries(&host, "level_chosen").len(), 1);
    let status = host.snapshot();
    assert_eq!(status["levelDefault"]["origin"], "chosen");
    assert!(status["levelRecordMissing"].is_null());
    std::fs::remove_dir_all(base).unwrap();
}

/// A genuine first run, the path every new person takes: no record and no earlier Codex start in this home. The
/// default is in force, with no question.
#[test]
fn a_first_run_reaches_the_apps_default_with_no_question() {
    let base = root("first-run");
    let host = ready_with_ledger(&base.join("data"), "/invented");
    host.inner.0.lock().unwrap().default_level = None;
    host.set_app_default_for_test(Some("full"));
    let view = host.read_levels_at_launch_in(Some("app-home:invented"), Some(&account_home(&base, false)));
    assert_eq!(view, json!({"state": "read", "accepted": [], "refused": [], "appDefault": "full"}));
    assert_eq!(host.default_level().unwrap().id, "full");
    let status = host.snapshot();
    assert_eq!(status["levelDefault"]["origin"], "app-default");
    assert!(status["levelRecordMissing"].is_null());
    assert!(status["levelSessionOnlyOffered"].is_null());
    // The same when everything was removed: a complete reset reads as a first run.
    std::fs::remove_dir_all(base).unwrap();
}

/// The probe looks at one name in this home by presence only: it follows no link, opens nothing, and looks at no
/// other folder.
#[test]
fn the_home_probe_is_presence_only_in_this_home() {
    let base = root("probe");
    let home = account_home(&base, false);
    assert!(!cl::home_has_codex_state(&home));
    // State elsewhere (beside the home, or in its parent) is not this home's.
    std::fs::write(base.join("homes").join(cl::CODEX_STATE_NAME), b"invented").unwrap();
    assert!(!cl::home_has_codex_state(&home));
    // A dangling link is present and is not followed.
    std::os::unix::fs::symlink(base.join("absent"), home.join(cl::CODEX_STATE_NAME)).unwrap();
    assert!(cl::home_has_codex_state(&home));
    std::fs::remove_file(home.join(cl::CODEX_STATE_NAME)).unwrap();
    // A named pipe is present, and opening it would block: the probe does not open it.
    let pipe = home.join(cl::CODEX_STATE_NAME);
    let c = std::ffi::CString::new(pipe.as_os_str().as_encoded_bytes()).unwrap();
    assert_eq!(unsafe { libc::mkfifo(c.as_ptr(), 0o600) }, 0);
    assert!(cl::home_has_codex_state(&home));
    std::fs::remove_dir_all(base).unwrap();
}
