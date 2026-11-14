//! V4-AUT-06: the Host's start checks, send-time rules, level ledger entries, launch read and status.
use super::*;
use crate::codex_level as cl;
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
/// `read_levels_at_launch`: no production source calls the setters the tests use, and `apply_chosen` is called
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
                let allowed = name == "hosting_level.rs" && setter == "Self::apply_chosen(" && ["choose_level", "read_levels_at_launch"].contains(&function.as_str());
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
