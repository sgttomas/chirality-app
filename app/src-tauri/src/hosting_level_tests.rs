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
    assert_eq!(refused,cl::SAVE_UNCONFIRMED_NOT_APPLIED);
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
                let allowed = name == "hosting_level.rs" && setter == "Self::apply_chosen(" && ["choose_level", "read_levels_with_account_state"].contains(&function.as_str());
                if !allowed { offending.push(format!("{name}: {setter} in fn {function}")); }
            }
        }
    }
    assert!(offending.is_empty(), "{offending:#?}");

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
fn a_recorded_choice_wins_over_the_default_and_an_unusable_one_is_asked_about_not_defaulted() {
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
    // The latest entry does not match the table: neither the earlier entry nor the App's default, but the ask, with
    // the default preselected. A spoiled record must not raise a level as a removed one would.
    let mut tampered = cl::recorded_values(cl::level("supervised").unwrap());
    tampered["approvalPolicy"] = json!("never");
    { RecoveryLedger::open(path.clone()).unwrap().append(row("level-chosen:b", tampered)).unwrap(); }
    let host = Host::new_without_level();
    host.configure_recovery(path).unwrap();
    let view = host.read_levels_at_launch(Some("app-home:mine"));
    assert_eq!(view["refused"][0]["entryId"], "level-chosen:b");
    assert!(view.get("appDefault").is_none());
    assert_eq!(view["recordMissing"], cl::RECORD_MISSING_SENTENCE);
    assert!(host.default_level().is_none());
    let status = host.snapshot();
    assert!(status["levelDefault"].is_null());
    assert_eq!((status["levelRecordMissing"].as_str(), status["levelAskPreselected"].as_str()), (Some(cl::RECORD_MISSING_SENTENCE), Some("full")));
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
        r#"{"reason":"The App's records are not available in this session.","state":"not-read"}"#);
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
    assert_eq!(level["takesEffectSentence"], cl::NEXT_TURN_SENTENCE);
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
    assert!(host.choose_level(&LevelScope::Default, cl::level("supervised").unwrap(), &[]).unwrap_err().contains("session's level was not changed"));
    assert_eq!(host.default_level().unwrap().id, "full", "the App's default, unchanged");
    std::fs::remove_dir_all(&database).unwrap();
    std::fs::rename(base.join("displaced"), &database).unwrap();
    // A session-only choice, then the ledger is read whole: the read governs, and the choice is dropped.
    let unread = ready_unledgered("/invented");
    unread.read_levels_at_launch(Some("app-home:invented"));
    unread.choose_level(&LevelScope::Default, cl::level("supervised").unwrap(), &[]).unwrap();
    unread.choose_level(&LevelScope::Conversation("thread".into()), cl::level("edits").unwrap(), &[]).unwrap();
    let other = root("session-later");
    let recovered = ready_with_ledger(&other, "/invented");
    unread.inner.0.lock().unwrap().recovery = recovered.inner.0.lock().unwrap().recovery.clone();
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
    recovered.app_runtime_custody().unwrap().record_app_session_end(&[]).unwrap();
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
    assert_eq!(row["level"]["projectTrust"]["case"], "unmarked");
    assert_eq!(row["level"]["projectTrust"]["lines"], json!([cl::TRUST_UNTRUSTED_SENT]));
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
            "marked-untrusted" => assert_eq!(trust["lines"], json!([cl::TRUST_MARKED_UNTRUSTED, cl::TRUST_UNTRUSTED_SENT])),
            _ => {
                assert_eq!(trust["lines"], json!([cl::TRUST_NOT_READ, cl::TRUST_UNTRUSTED_SENT]), "{what}");
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
    assert_eq!(cl::home_has_codex_state(&home), Ok(false));
    // State elsewhere (beside the home, or in its parent) is not this home's.
    std::fs::write(base.join("homes").join(cl::CODEX_STATE_NAME), b"invented").unwrap();
    assert_eq!(cl::home_has_codex_state(&home), Ok(false));
    // A dangling link is present and is not followed.
    std::os::unix::fs::symlink(base.join("absent"), home.join(cl::CODEX_STATE_NAME)).unwrap();
    assert_eq!(cl::home_has_codex_state(&home), Ok(true));
    std::fs::remove_file(home.join(cl::CODEX_STATE_NAME)).unwrap();
    // A named pipe is present, and opening it would block: the probe does not open it.
    let pipe = home.join(cl::CODEX_STATE_NAME);
    let c = std::ffi::CString::new(pipe.as_os_str().as_encoded_bytes()).unwrap();
    assert_eq!(unsafe { libc::mkfifo(c.as_ptr(), 0o600) }, 0);
    assert_eq!(cl::home_has_codex_state(&home), Ok(true));
    std::fs::remove_dir_all(base).unwrap();
}


/// The trust reading is on the start path, so it is held to one deadline even when its write is blocked: with
/// Codex's input full and not being read, the reading returns at the deadline as not read in time, and the entry
/// would go untrusted. (The start's own frame then waits for the writer, as any frame does while Codex is not reading.)
#[test]
fn a_blocked_trust_reading_write_ends_at_the_one_deadline_as_not_read() {
    use std::os::fd::{FromRawFd, OwnedFd};
    let (base, project, _, _) = git_project("trust-blocked");
    let host = trusting_host(&base, &project, "full");
    *host.this.lock().unwrap() = Arc::downgrade(&host);
    host.inner.0.lock().unwrap().level.trust_budget = Some(Duration::from_millis(300));
    let mut fds = [0; 2];
    assert_eq!(unsafe { libc::pipe(fds.as_mut_ptr()) }, 0);
    let read = unsafe { std::fs::File::from_raw_fd(fds[0]) };
    let write = unsafe { OwnedFd::from_raw_fd(fds[1]) };
    let flags = unsafe { libc::fcntl(fds[1], libc::F_GETFL) };
    assert_eq!(unsafe { libc::fcntl(fds[1], libc::F_SETFL, flags | libc::O_NONBLOCK) }, 0);
    let filler = [b'\n'; 4096];
    while unsafe { libc::write(fds[1], filler.as_ptr().cast(), filler.len()) } >= 0 {}
    assert_eq!(unsafe { libc::fcntl(fds[1], libc::F_SETFL, flags) }, 0);
    *host.stdin.lock().unwrap() = Some(ChildStdin::from(write));
    let began = std::time::Instant::now();
    let reading = host.trust_reading("thread/start", &json!({"cwd": key(&project)}), None).unwrap();
    let elapsed = began.elapsed();
    assert!(elapsed < Duration::from_millis(1500), "returned at the deadline, not when the pipe drains: {elapsed:?}");
    assert!(matches!(&reading.case, cl::TrustCase::NotRead { reason, .. } if reason == cl::TRUST_READ_TIMED_OUT), "{:?}", reading.case);
    // Release the blocked write so the worker ends.
    drop(read);
    *host.stdin.lock().unwrap() = None;
    std::fs::remove_dir_all(&base).unwrap();
}


/// Supervised says what allowing a command means at the pinned Codex.
#[test]
fn supervised_says_an_allowed_command_can_run_outside_the_sandbox() {
    let base = root("supervised-words");
    let host = ready_with_ledger(&base.join("data"), "/invented");
    host.choose_level(&LevelScope::Default, cl::level("supervised").unwrap(), &[]).unwrap();
    assert_eq!(host.snapshot()["levelDefault"]["allowing"], cl::SUPERVISED_ALLOWING);
    host.choose_level(&LevelScope::Default, cl::level("edits").unwrap(), &[]).unwrap();
    assert_eq!(host.snapshot()["levelDefault"]["allowing"], cl::SUPERVISED_ALLOWING);
    std::fs::remove_dir_all(base).unwrap();
}

/// Review B1, the owner's default with its one exception: a narrower choice whose record was altered never runs at
/// full access without the person's press. The ask names why, with full access preselected; one press continues at
/// full access, recorded as the person's choice.
#[test]
fn a_narrower_choice_whose_record_was_altered_does_not_run_at_full_access_without_the_ask() {
    for prior_state in [false, true] {
    let base = root("altered");
    let home = account_home(&base, prior_state);
    let path = base.join("data").join("recovery.ledger.jsonl");
    {
        let before = ready_with_ledger(&base.join("data"), "/invented");
        before.choose_level(&LevelScope::Default, cl::level("supervised").unwrap(), &[]).unwrap();
        before.app_runtime_custody().unwrap().record_app_session_end(&[]).unwrap();
    }
    // A command changed the recorded choice so that it no longer matches the table.
    let mut altered = cl::recorded_values(cl::level("supervised").unwrap());
    altered["approvalPolicy"] = json!("never");
    { RecoveryLedger::open(path).unwrap().append(json!({"kind":"level_chosen","session":"app-session:earlier","entryId":"level-chosen:altered",
        "at":"2026-11-14T12:00:00Z","scope":{"kind":"default-for-new-conversations"},"level":altered,"previous":null})).unwrap(); }
    let host = ready_with_ledger(&base.join("data"), "/invented");
    host.inner.0.lock().unwrap().default_level = None;
    host.set_app_default_for_test(Some("full"));
    let view = host.read_levels_at_launch_in(Some("app-home:invented"), Some(&home));
    assert!(view.get("appDefault").is_none(), "the App's default does not answer an altered record");
    let status = host.snapshot();
    assert_eq!((status["levelRecordMissing"].as_str(), status["levelAskPreselected"].as_str()), (Some(cl::RECORD_MISSING_SENTENCE), Some("full")));
    let wire = Wire::attach(&host);
    assert!(send(&host, "turn/start", turn_params("thread")).err().unwrap().contains("no level chosen"), "nothing runs before the press");
    assert!(wire.nothing(), "no frame, at full access or any other");
    // One press, on the preselected level.
    host.choose_level(&LevelScope::Default, cl::level("full").unwrap(), &[]).unwrap();
    let status = host.snapshot();
    assert_eq!(status["levelDefault"]["origin"], "chosen");
    assert!(status["levelRecordMissing"].is_null() && status["levelAskPreselected"].is_null());
    send(&host, "turn/start", turn_params("thread")).unwrap();
    assert_eq!(wire.next()["params"]["approvalPolicy"], "never");
    wire.close(&host);
    std::fs::remove_dir_all(base).unwrap();
    }
}

/// A conversation's own recorded level that no longer matches the table: that conversation is asked about, with the
/// default preselected; it does not fall to the default scope. Other conversations go on at the default.
#[test]
fn a_conversations_unusable_record_is_asked_about_and_never_falls_to_the_default() {
    let base = root("altered-conversation");
    let home = account_home(&base, true);
    let path = base.join("data").join("recovery.ledger.jsonl");
    {
        let before = ready_with_ledger(&base.join("data"), "/invented");
        before.choose_level(&LevelScope::Conversation("thread".into()), cl::level("supervised").unwrap(), &[]).unwrap();
        before.app_runtime_custody().unwrap().record_app_session_end(&[]).unwrap();
    }
    let mut altered = cl::recorded_values(cl::level("supervised").unwrap());
    altered["sandbox"] = json!("danger-full-access");
    { RecoveryLedger::open(path).unwrap().append(json!({"kind":"level_chosen","session":"app-session:earlier","entryId":"level-chosen:altered",
        "at":"2026-11-14T12:00:00Z","scope":{"kind":"conversation","home":"app-home:invented","threadId":"thread"},"level":altered,"previous":null})).unwrap(); }
    let host = ready_with_ledger(&base.join("data"), "/invented");
    let generation = g(&host);
    host.inner.0.lock().unwrap().threads.push(json!({"generation": generation, "threadId": "other", "cwd": "/invented"}));
    host.inner.0.lock().unwrap().default_level = None;
    host.set_app_default_for_test(Some("full"));
    let view = host.read_levels_at_launch_in(Some("app-home:invented"), Some(&home));
    assert_eq!(view["appDefault"], "full", "the default scope has no unusable record");
    let status = host.snapshot();
    let row = |id: &str| status["threads"].as_array().unwrap().iter().find(|t| t["threadId"] == id).unwrap()["level"].clone();
    assert_eq!(row("thread")["ask"], json!({"sentence": cl::RECORD_MISSING_SENTENCE, "preselected": "full"}));
    assert!(row("thread")["chosen"].is_null(), "nothing is in force for that conversation");
    assert!(row("thread").get("scopeSentence").is_none(), "an unusable choice never says it follows the default");
    assert!(row("other").get("ask").is_none());
    assert_eq!(row("other")["scopeSentence"], cl::FOLLOWS_DEFAULT_SENTENCE);
    assert_eq!(status["levelAskPreselected"], "full");
    let wire = Wire::attach(&host);
    assert!(send(&host, "turn/start", turn_params("thread")).err().unwrap().contains("no level chosen"));
    assert!(host.level_for("thread/fork", &json!({"threadId": "thread"})).is_none(), "a fork of it carries no level either");
    assert!(host.level_for("thread/resume", &json!({"threadId": "thread"})).is_none());
    assert!(wire.nothing());
    send(&host, "turn/start", turn_params("other")).unwrap();
    assert_eq!(wire.next()["params"]["approvalPolicy"], "never", "another conversation goes on at the default");
    host.choose_level(&LevelScope::Conversation("thread".into()), cl::level("supervised").unwrap(), &[]).unwrap();
    assert!(host.snapshot()["levelAskPreselected"].is_null());
    send(&host, "turn/start", turn_params("thread")).unwrap();
    assert_eq!(wire.next()["params"]["approvalPolicy"], "untrusted");
    wire.close(&host);
    std::fs::remove_dir_all(base).unwrap();
}

/// Records that cannot be read, on a first run by this home's evidence (no earlier Codex start in it): the App's
/// default applies, with the line that a choice made now is kept for this session only.
#[test]
fn unreadable_records_on_a_first_run_take_the_default_with_its_words() {
    let base = root("unread-first");
    let home = account_home(&base, false);
    let host = ready_unledgered("/invented");
    host.set_app_default_for_test(Some("full"));
    host.inner.0.lock().unwrap().recovery_initialization_error = Some("invented raw ledger failure".into());
    let view = host.read_levels_at_launch_in(Some("app-home:invented"), Some(&home));
    assert_eq!((view["state"].as_str(), view["appDefault"].as_str()), (Some("not-read"), Some("full")));
    let status = host.snapshot();
    assert_eq!(status["levelDefault"]["origin"], "app-default");
    assert_eq!(status["levelRecordsUnread"], cl::RECORDS_UNREAD_SENTENCE);
    assert!(status["levelRecordMissing"].is_null() && status["levelAskPreselected"].is_null());
    assert_eq!(status["levelSessionOnlyOffered"]["reason"], cl::RECORDS_NOT_READ);
    let wire = Wire::attach(&host);
    send(&host, "turn/start", turn_params("thread")).unwrap();
    assert_eq!(wire.next()["params"]["approvalPolicy"], "never", "the first conversation runs at the default, with no step");
    let out = host.choose_level(&LevelScope::Default, cl::level("supervised").unwrap(), &[]).unwrap();
    assert_eq!(out["origin"], "session-only");
    assert!(host.snapshot()["levelRecordsUnread"].is_null());
    wire.close(&host);
    std::fs::remove_dir_all(base).unwrap();
}

/// Records that cannot be read where this home has been used: the ask, with the default preselected and the choice
/// kept for this session only.
#[test]
fn unreadable_records_where_this_home_has_been_used_are_asked_about() {
    let base = root("unread-used");
    let home = account_home(&base, true);
    let host = ready_unledgered("/invented");
    host.set_app_default_for_test(Some("full"));
    host.inner.0.lock().unwrap().recovery_initialization_error = Some("invented raw ledger failure".into());
    let view = host.read_levels_at_launch_in(Some("app-home:invented"), Some(&home));
    assert!(view.get("appDefault").is_none());
    let status = host.snapshot();
    assert_eq!((status["levelRecordMissing"].as_str(), status["levelAskPreselected"].as_str()), (Some(cl::RECORD_MISSING_SENTENCE), Some("full")));
    assert_eq!(status["levelSessionOnlyOffered"]["reason"], cl::RECORDS_NOT_READ);
    assert!(status["levelRecordsUnread"].is_null());
    let wire = Wire::attach(&host);
    assert!(send(&host, "turn/start", turn_params("thread")).is_err());
    assert!(wire.nothing());
    let out = host.choose_level(&LevelScope::Default, cl::level("full").unwrap(), &[]).unwrap();
    assert_eq!(out["origin"], "session-only");
    assert!(host.snapshot()["levelRecordMissing"].is_null());
    send(&host, "turn/start", turn_params("thread")).unwrap();
    assert_eq!(wire.next()["params"]["approvalPolicy"], "never");
    wire.close(&host);
    std::fs::remove_dir_all(base).unwrap();
}

// Review regressions: decide from observed records/home state, not a failed probe or stale cache.
#[test]
fn review_repairs_unknown_home_state_asks_and_does_not_leave_a_default_after_access_returns() {
    use std::os::unix::fs::PermissionsExt;
    let base = root("unknown-state");
    let home = account_home(&base, true);
    for readable_ledger in [false, true] {
        let host = if readable_ledger { ready_with_ledger(&base.join("data"), "/invented") } else { ready_unledgered("/invented") };
        host.inner.0.lock().unwrap().default_level = None;
        std::fs::set_permissions(&home, std::fs::Permissions::from_mode(0o000)).unwrap();
        let observation = std::fs::symlink_metadata(home.join(cl::CODEX_STATE_NAME));
        let view = host.read_levels_at_launch_in(Some("app-home:invented"), Some(&home));
        std::fs::set_permissions(&home, std::fs::Permissions::from_mode(0o700)).unwrap();
        assert_eq!(observation.unwrap_err().kind(), std::io::ErrorKind::PermissionDenied);
        assert!(host.default_level().is_none(), "unknown home must ask: {view}");
        assert_eq!(view["homeState"]["state"], "unknown");
        assert_eq!(view["homeState"]["detail"]["standing"], cl::NOT_THE_APPS_TEXT);
        assert_eq!(host.snapshot()["levelAskPreselected"], "full");
        if readable_ledger { host.app_runtime_custody().unwrap().record_app_session_end(&[]).unwrap(); }
    }
    std::fs::remove_dir_all(base).unwrap();
}

#[test]
fn review_repairs_unreadable_first_run_reason_does_not_demand_a_choice() {
    let base = root("first-read-words");
    let home = account_home(&base, false);
    let host = ready_unledgered("/invented");
    host.inner.0.lock().unwrap().recovery_initialization_error = Some("invented raw failure".into());
    let view = host.read_levels_at_launch_in(Some("app-home:invented"), Some(&home));
    assert_eq!(view["appDefault"], "full");
    assert_eq!(view["reason"], cl::RECORDS_NOT_READ);
    assert!(!view["reason"].as_str().unwrap().contains("invented raw failure"));
    assert_eq!(host.snapshot()["levelSessionOnlyOffered"]["detail"]["text"], "invented raw failure");
    std::fs::remove_dir_all(base).unwrap();
}

#[test]
fn review_repairs_additional_home_reads_a_choice_committed_before_a_flush_failure() {
    let base = root("committed-choice");
    let host = ready_with_ledger(&base.join("data"), "/invented");
    host.choose_level(&LevelScope::Default, cl::level("full").unwrap(), &[]).unwrap();
    host.flush_recovery_observations();
    crate::recovery::store::FAIL_FLUSH_AFTER_COMMIT.with(|f| f.set(true));
    let failed = host.choose_level(&LevelScope::Default, cl::level("supervised").unwrap(), &[]).unwrap_err();
    assert_eq!(failed,cl::SAVE_UNCONFIRMED_NOT_APPLIED);
    assert!(host.snapshot()["levelChoiceSave"]["writeFailure"]["text"].as_str().unwrap().contains("commit returned"));
    let other = Host::new_with_app_custody(host.app_runtime_custody().unwrap()).unwrap();
    other.read_levels_at_launch(Some("app-home:additional"));
    assert_eq!(other.default_level().map(|l| l.id.as_str()), Some("supervised"));
    host.app_runtime_custody().unwrap().record_app_session_end(&[]).unwrap();
    std::fs::remove_dir_all(base).unwrap();
}

#[test]
fn review_repairs_failed_fresh_read_preserves_a_known_narrower_level_and_reports_failure() {
    let base = root("fresh-read-failure");
    let host = ready_with_ledger(&base.join("data"), "/invented");
    host.choose_level(&LevelScope::Default, cl::level("supervised").unwrap(), &[]).unwrap();
    let db = base.join("data/recovery.ledger.sqlite");
    let moved = base.join("data/moved.sqlite");
    std::fs::rename(&db, &moved).unwrap();
    let view = host.read_levels_at_launch_in(Some("app-home:invented"), Some(&account_home(&base, false)));
    std::fs::rename(&moved, &db).unwrap();
    assert_eq!(view["state"], "not-read");
    assert_eq!(host.default_level().map(|l| l.id.as_str()), Some("supervised"));
    assert_eq!(host.snapshot()["levelDefault"]["origin"], "chosen");
    assert!(!host.snapshot()["levelSessionOnlyOffered"].is_null());
    host.app_runtime_custody().unwrap().record_app_session_end(&[]).unwrap();
    std::fs::remove_dir_all(base).unwrap();
}

#[test]
fn review_repairs_unknown_resume_or_fork_folder_is_not_the_server_folder() {
    let base = root("unknown-saved-folder");
    let host = ready_with_ledger(&base.join("data"), "/invented");
    host.choose_level(&LevelScope::Default, cl::level("full").unwrap(), &[]).unwrap();
    let wire = Wire::attach(&host);
    for method in ["thread/resume", "thread/fork"] {
        let sent = send(&host, method, json!({"threadId":"unknown-saved"}));
        let failed = sent.is_err();
        if sent.is_ok() { wire.next(); }
        assert!(failed, "{method} substituted the server folder");
    }
    assert!(wire.nothing());
    wire.close(&host);
    host.app_runtime_custody().unwrap().record_app_session_end(&[]).unwrap();
    std::fs::remove_dir_all(base).unwrap();
}

#[test]
fn review_repairs_report_names_the_requested_id_beside_the_actual_reply() {
    let base = root("requested-id");
    let host = ready_with_ledger(&base.join("data"), "/invented");
    host.choose_level(&LevelScope::Default, cl::level("full").unwrap(), &[]).unwrap();
    let wire = Wire::attach(&host);
    send(&host, "thread/resume", json!({"threadId":"thread"})).unwrap();
    let sent = wire.next();
    reply(&host, json!({"id":sent["id"],"result":{"thread":{"id":"thread"},"approvalPolicy":"on-request","approvalsReviewer":"user","sandbox":{"type":"readOnly"}}}));
    let report = thread_row(&host,"thread")["level"]["reported"].clone();
    wire.close(&host);
    assert_eq!(report["requestedLevelId"], "full");
    assert!(report.get("levelId").is_none());
    assert_eq!(report["sandbox"]["type"], "readOnly");
    assert_eq!(report["agreement"], "differs");
    host.app_runtime_custody().unwrap().record_app_session_end(&[]).unwrap();
    std::fs::remove_dir_all(base).unwrap();
}

#[test]
fn review_repairs_level_disclosures_come_from_the_host_for_each_asking_policy() {
    let base = root("closed-disclosures");
    let host = ready_with_ledger(&base.join("data"), "/invented");
    for id in ["supervised","edits","edits-network","edits-no-asking","full"] {
        host.choose_level(&LevelScope::Default, cl::level(id).unwrap(), &[]).unwrap();
        let chosen = host.snapshot()["levelDefault"].clone();
        assert_eq!(chosen["readingSentence"], "Reading is not limited at any permission level.");
        assert_eq!(chosen["allowing"].is_string(), matches!(id,"supervised"|"edits"|"edits-network"));
    }
    host.app_runtime_custody().unwrap().record_app_session_end(&[]).unwrap();
    std::fs::remove_dir_all(base).unwrap();
}

#[test]
fn review_inheritance_created_and_forked_levels_survive_a_new_default_and_relaunch() {
    for inherited in ["chosen", "app-default"] {
        let base = root("inherited-relaunch");
        let home = account_home(&base, false);
        let expected = if inherited == "chosen" { "supervised" } else { "full" };
        let chosen_at;
        {
            let host = ready_with_ledger(&base.join("data"), "/invented");
            host.inner.0.lock().unwrap().default_level = None;
            host.read_levels_at_launch_in(Some("app-home:invented"), Some(&home));
            if inherited == "chosen" { host.choose_level(&LevelScope::Default, cl::level(expected).unwrap(), &[]).unwrap(); }
            chosen_at = host.snapshot()["levelDefault"]["chosenAt"].clone();
            let wire = Wire::attach(&host);
            for (method,params,target) in [("thread/start",json!({"cwd":"/invented"}),"created"),
                                           ("thread/fork",json!({"threadId":"created"}),"copied")] {
                send(&host,method,params).unwrap();
                let sent=wire.next();
                reply(&host,json!({"id":sent["id"],"result":{"thread":{"id":target}}}));
                let generation=g(&host);
                host.inner.0.lock().unwrap().threads.push(json!({"generation":generation,"threadId":target,"cwd":"/invented"}));
            }
            let associations=entries(&host,"level_inherited");
            wire.close(&host);
            assert_eq!(associations.len(),2);
            assert!(associations.iter().all(|r|r["origin"]==inherited));
            let another=if expected=="full" {"supervised"} else {"full"};
            host.choose_level(&LevelScope::Default,cl::level(another).unwrap(),&[]).unwrap();
            for thread in ["created","copied"] {
                assert_eq!(host.thread_level(thread).unwrap().id,expected);
                assert_eq!(thread_row(&host,thread)["level"]["chosen"]["origin"],inherited);
            }
            assert_eq!(entries(&host,"level_chosen").len(),if inherited=="chosen" {2} else {1},"association is not a new choice");
            host.app_runtime_custody().unwrap().record_app_session_end(&[]).unwrap();
        }
        let host=ready_with_ledger(&base.join("data"),"/invented");
        host.read_levels_at_launch_in(Some("app-home:invented"),Some(&home));
        for thread in ["created","copied"] {
            assert_eq!(host.level_for("thread/resume",&json!({"threadId":thread})).unwrap().id,expected);
            let chosen=host.inner.0.lock().unwrap().level.thread_chosen[thread].clone();
            assert_eq!(chosen.origin.as_str(),inherited);
            assert_eq!(if inherited=="app-default" {Value::Null} else {json!(chosen.at)},chosen_at);
        }
        host.app_runtime_custody().unwrap().record_app_session_end(&[]).unwrap();
        std::fs::remove_dir_all(base).unwrap();
    }
}

#[test]
fn review_inheritance_session_only_origin_survives_start_and_fork_but_is_never_saved() {
    let base=root("session-inheritance");
    let host=ready_unledgered("/invented");
    host.read_levels_at_launch(Some("app-home:invented"));
    host.choose_level(&LevelScope::Default,cl::level("supervised").unwrap(),&[]).unwrap();
    let expected=host.snapshot()["levelDefault"].clone();
    let wire=Wire::attach(&host);
    for (method,params,target) in [("thread/start",json!({"cwd":"/invented"}),"created"),
                                   ("thread/fork",json!({"threadId":"created"}),"copied")] {
        send(&host,method,params).unwrap();
        let sent=wire.next();
        reply(&host,json!({"id":sent["id"],"result":{"thread":{"id":target}}}));
        let generation=g(&host);
        host.inner.0.lock().unwrap().threads.push(json!({"generation":generation,"threadId":target,"cwd":"/invented"}));
    }
    wire.close(&host);
    for thread in ["created","copied"] {
        let chosen=thread_row(&host,thread)["level"]["chosen"].clone();
        assert_eq!(chosen["origin"],"session-only");
        assert_eq!(chosen["chosenAt"],expected["chosenAt"]);
        assert_eq!(chosen["originSentence"],cl::SESSION_ONLY_SENTENCE);
        assert!(chosen["ledgerEntry"].is_null());
    }
    std::fs::create_dir_all(base.join("data")).unwrap();
    let recovered=ready_with_ledger(&base.join("data"),"/invented");
    host.inner.0.lock().unwrap().recovery=recovered.inner.0.lock().unwrap().recovery.clone();
    host.read_levels_at_launch(Some("app-home:invented"));
    assert!(entries(&host,"level_inherited").is_empty());
    assert!(entries(&host,"level_chosen").is_empty());
    for thread in ["created","copied"] { assert!(host.thread_level(thread).is_none()); }
    recovered.app_runtime_custody().unwrap().record_app_session_end(&[]).unwrap();
    std::fs::remove_dir_all(base).unwrap();
}

#[test]
fn review_inheritance_failed_association_is_disclosed_and_relaunch_uses_the_current_default() {
    let base=root("association-failure");
    let home=account_home(&base,false);
    {
        let host=ready_with_ledger(&base.join("data"),"/invented");
        host.choose_level(&LevelScope::Default,cl::level("supervised").unwrap(),&[]).unwrap();
        let wire=Wire::attach(&host);
        send(&host,"thread/start",json!({"cwd":"/invented"})).unwrap();
        let sent=wire.next();
        host.choose_level(&LevelScope::Default,cl::level("full").unwrap(),&[]).unwrap();
        crate::recovery::store::FAIL_BATCH_AFTER.with(|f|f.set(Some(0)));
        reply(&host,json!({"id":sent["id"],"result":{"thread":{"id":"created"}}}));
        let generation=g(&host);
        host.inner.0.lock().unwrap().threads.push(json!({"generation":generation,"threadId":"created","cwd":"/invented"}));
        let status=thread_row(&host,"created")["level"].clone();
        wire.close(&host);
        assert_eq!(status["chosen"]["id"],"supervised");
        assert_eq!(status["inheritancePersistence"]["state"],"not-confirmed");
        assert_eq!(status["inheritancePersistence"]["sentence"],cl::INHERITANCE_NOT_RECORDED);
        assert!(!host.snapshot()["recoveryPersistenceError"].is_null());
        // Quit retries queued facts; keep the same append failure through that attempt.
        crate::recovery::store::FAIL_BATCH_AFTER.with(|f|f.set(Some(0)));
        let end=host.app_runtime_custody().unwrap().record_app_session_end(&[]).unwrap();
        assert!(end["pendingPointerFacts"].as_u64().unwrap()>0);
    }
    let host=ready_with_ledger(&base.join("data"),"/invented");
    host.read_levels_at_launch_in(Some("app-home:invented"),Some(&home));
    let generation=g(&host);
    host.inner.0.lock().unwrap().threads.push(json!({"generation":generation,"threadId":"created","cwd":"/invented"}));
    let status=thread_row(&host,"created")["level"].clone();
    assert_eq!(status["chosen"]["id"],"full");
    assert_eq!(status["chosen"]["origin"],"chosen");
    assert_eq!(status["chosen"]["scope"],"default");
    host.app_runtime_custody().unwrap().record_app_session_end(&[]).unwrap();
    std::fs::remove_dir_all(base).unwrap();
}

#[test]
fn review_repairs_unknown_home_on_complete_refresh_withdraws_an_earlier_app_default() {
    use std::os::unix::fs::PermissionsExt;
    let base=root("unknown-refresh");let home=account_home(&base,false);
    let host=ready_with_ledger(&base.join("data"),"/invented");
    host.inner.0.lock().unwrap().default_level=None;
    host.read_levels_at_launch_in(Some("app-home:invented"),Some(&home));
    assert_eq!(host.default_level().unwrap().id,"full");
    std::fs::set_permissions(&home,std::fs::Permissions::from_mode(0o000)).unwrap();
    let view=host.read_levels_at_launch_in(Some("app-home:invented"),Some(&home));
    std::fs::set_permissions(&home,std::fs::Permissions::from_mode(0o700)).unwrap();
    let level=host.default_level().map(|l|l.id.clone());
    host.app_runtime_custody().unwrap().record_app_session_end(&[]).unwrap();
    std::fs::remove_dir_all(base).unwrap();
    assert!(level.is_none(),"an earlier App default must not bypass the new ask: {view}");
}

/// LIM-022's explicit boundary, on invented data: valid remaining rows cannot establish that an outside
/// writer removed a choice. This observes the limit, not a successful missing-record safeguard.
#[test]
fn outside_entry_removal_can_expose_an_older_choice_or_the_app_default() {
    for remove_all in [false,true] {
        let base=root("outside-choice-removal");let home=account_home(&base,true);
        {
            let host=ready_with_ledger(&base.join("data"),"/invented");
            host.choose_level(&LevelScope::Default,cl::level("full").unwrap(),&[]).unwrap();
            host.choose_level(&LevelScope::Default,cl::level("supervised").unwrap(),&[]).unwrap();
            host.app_runtime_custody().unwrap().record_app_session_end(&[]).unwrap();
        }
        let db=rusqlite::Connection::open(base.join("data/recovery.ledger.sqlite")).unwrap();
        db.execute("DROP TRIGGER ledger_entry_never_deleted",[]).unwrap();
        let sql=if remove_all {"DELETE FROM ledger_entry WHERE kind='level_chosen'"}
            else {"DELETE FROM ledger_entry WHERE seq=(SELECT MAX(seq) FROM ledger_entry WHERE kind='level_chosen')"};
        assert_eq!(db.execute(sql,[]).unwrap(),if remove_all {2} else {1});drop(db);
        let host=ready_with_ledger(&base.join("data"),"/invented");
        host.read_levels_at_launch_in(Some("app-home:invented"),Some(&home));
        let status=host.snapshot();
        assert_eq!(status["levelDefault"]["id"],"full");
        assert_eq!(status["levelDefault"]["origin"],if remove_all {"app-default"} else {"chosen"});
        assert!(status["levelRecordMissing"].is_null());
        host.app_runtime_custody().unwrap().record_app_session_end(&[]).unwrap();
        std::fs::remove_dir_all(base).unwrap();
    }
}

#[test]
fn round_two_choice_flush_failure_distinguishes_applied_level_and_unconfirmed_save() {
    for fallback in [false, true] {
        let base = root("choice-flush-outcome");
        let home = account_home(&base, false);
        let data = base.join("data");
        let host = ready_with_ledger(&data, "/invented");
        host.choose_level(&LevelScope::Default, cl::level("full").unwrap(), &[]).unwrap();
        if fallback {
            let db = data.join("recovery.ledger.sqlite"); let moved = data.join("moved.sqlite");
            std::fs::rename(&db, &moved).unwrap();
            host.read_levels_at_launch_in(Some("app-home:invented"), Some(&home));
            std::fs::rename(&moved, &db).unwrap();
        }
        crate::recovery::store::FAIL_FLUSH_AFTER_COMMIT.with(|f| f.set(true));
        let result = host.choose_level(&LevelScope::Default, cl::level("supervised").unwrap(), &[]);
        assert_eq!(result.is_ok(), fallback);
        let status = host.snapshot();
        let expected = if fallback { "supervised" } else { "full" };
        assert_eq!(status["levelDefault"]["id"], expected);
        let save = status["levelChoiceSave"].clone();
        let current = status["levelDefault"].clone();
        host.app_runtime_custody().unwrap().record_app_session_end(&[]).unwrap();
        drop(host);
        let reopened = ready_with_ledger(&data, "/invented");
        reopened.read_levels_at_launch_in(Some("app-home:invented"), Some(&home));
        assert_eq!(reopened.default_level().unwrap().id, "supervised", "the append committed despite its flush failure");
        reopened.app_runtime_custody().unwrap().record_app_session_end(&[]).unwrap();
        std::fs::remove_dir_all(base).unwrap();
        assert_eq!(save["recorded"], "not-confirmed");
        assert_eq!(save["applied"], fallback);
        assert!(!save.to_string().contains("not recorded"));
        if fallback {
            assert_eq!(current["recorded"], "not-confirmed");
            assert_ne!(current["origin"], "session-only");
            assert!(!current.to_string().contains("not kept after"));
        } else {
            assert!(save["sentence"].as_str().unwrap().contains("reopening"));
        }
    }
}

#[test]
fn round_two_inherited_flush_failure_is_conditional_and_distinct_from_a_choice_failure() {
    let base = root("inheritance-flush-outcome"); let data=base.join("data");
    let home=account_home(&base,false);
    let host=ready_with_ledger(&data,"/invented");
    host.choose_level(&LevelScope::Default,cl::level("supervised").unwrap(),&[]).unwrap();
    let wire=Wire::attach(&host);
    send(&host,"thread/start",json!({"cwd":"/invented"})).unwrap(); let sent=wire.next();
    host.choose_level(&LevelScope::Default,cl::level("full").unwrap(),&[]).unwrap();
    crate::recovery::store::FAIL_FLUSH_AFTER_COMMIT.with(|f|f.set(true));
    reply(&host,json!({"id":sent["id"],"result":{"thread":{"id":"created"}}}));
    let generation=g(&host);
    host.inner.0.lock().unwrap().threads.push(json!({"generation":generation,"threadId":"created","cwd":"/invented"}));
    let inherited=thread_row(&host,"created")["level"]["inheritancePersistence"].clone();
    wire.close(&host);
    host.app_runtime_custody().unwrap().record_app_session_end(&[]).unwrap(); drop(host);
    let reopened=ready_with_ledger(&data,"/invented");
    reopened.read_levels_at_launch_in(Some("app-home:invented"),Some(&home));
    assert_eq!(reopened.thread_level("created").unwrap().id,"supervised");
    let generation=g(&reopened);
    reopened.inner.0.lock().unwrap().threads.push(json!({"generation":generation,"threadId":"created","cwd":"/invented"}));
    crate::recovery::store::FAIL_FLUSH_AFTER_COMMIT.with(|f|f.set(true));
    assert!(reopened.choose_level(&LevelScope::Conversation("created".into()),cl::level("edits").unwrap(),&[]).is_err());
    let explicit=reopened.snapshot()["levelChoiceSave"].clone();
    reopened.app_runtime_custody().unwrap().record_app_session_end(&[]).unwrap();
    std::fs::remove_dir_all(base).unwrap();
    assert_eq!(inherited["sentence"],"The App could not confirm that this conversation's level was saved. If it is not saved before the App closes, reopening follows the default for new conversations then in force, which could allow more than this level, unless you set its level.");
    assert_eq!(explicit["recorded"],"not-confirmed");
    assert_ne!(explicit["sentence"],inherited["sentence"]);
}

#[test]
fn round_two_additional_home_uses_account_state_at_its_production_launch_read() {
    use crate::{home_resources::HomeClass, runtime_session::HomeSession};
    use std::os::unix::fs::PermissionsExt;
    for unknown in [false,true] {
        let base=root("shared-account-evidence");let account_path=account_home(&base,true);
        let host=ready_with_ledger(&base.join("data"),"/invented");
        let mut cfg=start_config(&account_path,&base);cfg.codex_home=account_path.clone();
        let account=HomeSession::new(HomeClass::Account,host.clone(),Ok(cfg.clone())).unwrap();
        let other=Arc::new(Host::new_with_app_custody(host.app_runtime_custody().unwrap()).unwrap());
        cfg.codex_home=base.join("other-home");
        let additional=HomeSession::new(HomeClass::ApiKey,other.clone(),Ok(cfg)).unwrap();
        if unknown { std::fs::set_permissions(&account_path,std::fs::Permissions::from_mode(0o000)).unwrap(); }
        account.level_launch_reads(&account); additional.level_launch_reads(&account);
        let account_status=host.snapshot(); let additional_status=other.snapshot();
        if unknown { std::fs::set_permissions(&account_path,std::fs::Permissions::from_mode(0o700)).unwrap(); }
        host.app_runtime_custody().unwrap().record_app_session_end(&[]).unwrap();
        std::fs::remove_dir_all(base).unwrap();
        assert!(account_status["levelRecordMissing"].is_string());
        assert!(additional_status["levelRecordMissing"].is_string(),"{additional_status}");
        assert!(additional_status["levelDefault"].is_null());
        if unknown { assert_eq!(additional_status["levelLaunchRead"]["homeState"]["state"],"unknown"); }
    }
}

#[test]
fn round_two_failed_trust_write_reports_an_attempt_not_a_completed_send() {
    let base=root("trust-write-outcome");let host=ready_with_ledger(&base,"/invented");
    let mut wire=Wire::attach(&host);wire.child.kill().unwrap();wire.child.wait().unwrap();
    let receipt=send(&host,"thread/resume",json!({"threadId":"thread"})).unwrap();
    assert!(receipt.evidence()["writeError"].is_string());
    let sent=thread_row(&host,"thread")["level"]["sent"].clone();
    *host.stdin.lock().unwrap()=None;
    host.app_runtime_custody().unwrap().record_app_session_end(&[]).unwrap();
    std::fs::remove_dir_all(base).unwrap();
    assert_eq!(sent["writeResult"],"not-established");
    assert!(!sent["projectTrust"]["lines"].to_string().contains("sent"));
    assert!(sent["projectTrust"]["lines"].to_string().contains("tried to send"));
}

#[test]
fn round_two_refused_start_retry_keeps_its_recorded_default() {
    let base=root("refused-start-choice");let host=ready_with_ledger(&base,"/invented");
    let chosen=host.choose_level(&LevelScope::Default,cl::level("supervised").unwrap(),&[]).unwrap();
    assert_eq!(entries(&host,"level_chosen")[0]["entryId"],chosen["ledgerEntry"]);
    let wire=Wire::attach(&host);let serial=host.frame_write.lock().unwrap();
    let sender=host.clone();let pending=std::thread::spawn(move||send(&sender,"thread/start",json!({"cwd":"/invented"})).unwrap());
    let deadline=std::time::Instant::now()+Duration::from_secs(5);
    while host.inner.0.lock().unwrap().source_requests.is_empty(){assert!(std::time::Instant::now()<deadline);std::thread::yield_now();}
    host.choose_level(&LevelScope::Conversation("thread".into()),cl::level("edits").unwrap(),&[]).unwrap();
    drop(serial);let refused=pending.join().unwrap();
    assert_eq!(refused.write_attempt_observed(),Some(false));assert!(wire.nothing());
    send(&host,"thread/start",json!({"cwd":"/invented"})).unwrap();
    assert_eq!(wire.next()["params"]["sandbox"],"read-only");
    assert_eq!(host.default_level().unwrap().id,"supervised");
    wire.close(&host);host.app_runtime_custody().unwrap().record_app_session_end(&[]).unwrap();std::fs::remove_dir_all(base).unwrap();
}

// ---- DEL-01-01: the App's own trust choice in the frames ----

const SET_UP: &str = crate::desktop_startup::SAVED_REQUEST_SOURCE;
const ENVIRONMENT: &str = "explicit Root native environment path inputs";

/// A trusting Host whose launched project is `project`, known as `source` says.
fn app_project_host(base: &Path, project: &Path, source: &str) -> (Arc<Host>, Arc<crate::project_trust::ProjectTrust>) {
    let host = trusting_host(base, project, "edits");
    let trust = Arc::new(crate::project_trust::ProjectTrust::for_launch(Some(project), source));
    host.configure_project_trust(Arc::clone(&trust));
    (host, trust)
}
/// The person's switch off, or a switch file damaged past its last complete line.
fn switched_off(project: &Path, trust: &crate::project_trust::ProjectTrust) {
    crate::records_store::attach(project, true).unwrap();
    trust.switch_off_launched().unwrap();
}
fn damaged_choice(project: &Path, trust: &crate::project_trust::ProjectTrust) {
    switched_off(project, trust);
    let file = crate::records_store::attach(project, false).unwrap().dir.unwrap().join(crate::records_store::TRUST_SWITCHES);
    use std::io::Write;
    std::fs::OpenOptions::new().append(true).open(file).unwrap().write_all(b"{\"damaged\n").unwrap();
}
const START_RESUME_FORK: [(&str, &str); 3] = [("thread/start", "start"), ("thread/resume", "resume"), ("thread/fork", "fork")];
fn frame_params(method: &str, cwd: &Path) -> Value {
    match method {
        "thread/start" => json!({"cwd": cwd}),
        "thread/resume" => json!({"threadId": "thread", "excludeTurns": true}),
        _ => json!({"threadId": "thread", "deferGoalContinuation": true}),
    }
}

#[test]
fn every_row_of_the_case_table_through_start_resume_and_fork_with_exactly_one_entry() {
    type Prepare = fn(&Path, &crate::project_trust::ProjectTrust);
    let none: Prepare = |_, _| {};
    let unmarked = || json!({});
    let cases: Vec<(&str, &str, Prepare, Box<dyn Fn(&str) -> Value + Send>, &str, &str)> = vec![
        ("5: unmarked, set up through the App", SET_UP, none, Box::new(move |_| layers_with(unmarked())), "trusted", "app-on-by-setup"),
        ("2: the person's untrusted mark over the App's on", SET_UP, none, Box::new(|k| layers_with(json!({k: {"trust_level": "untrusted"}}))), "untrusted", "marked-untrusted"),
        ("3: the App's off over the settings' trusted mark", SET_UP, switched_off, Box::new(|k| layers_with(json!({k: {"trust_level": "trusted"}}))), "untrusted", "switched-off"),
        ("1: an unreadable reading over the App's on", SET_UP, none, Box::new(|_| json!({"error": {"code": -32603, "message": "invented"}})), "untrusted", "not-read"),
        ("7: an unreadable choice over the trusted mark", SET_UP, damaged_choice, Box::new(|k| layers_with(json!({k: {"trust_level": "trusted"}}))), "untrusted", "choice-not-read"),
        ("4: the trusted mark", SET_UP, none, Box::new(|k| layers_with(json!({k: {"trust_level": "trusted"}}))), "trusted", "trusted"),
        ("6: environment route, unmarked", ENVIRONMENT, none, Box::new(move |_| layers_with(unmarked())), "untrusted", "unmarked"),
        ("4: environment route, the trusted mark", ENVIRONMENT, none, Box::new(|k| layers_with(json!({k: {"trust_level": "trusted"}}))), "trusted", "trusted"),
    ];
    for (n, (what, source, prepare, answer, level, case)) in cases.into_iter().enumerate() {
        let (base, project, _, _) = git_project(&format!("app-trust-{n}"));
        let (host, trust) = app_project_host(&base, &project, source);
        prepare(&project, &trust);
        let k = key(&project);
        let wire = Responder::attach(&host, move |_| answer(&k));
        for (method, _) in START_RESUME_FORK {
            send(&host, method, frame_params(method, &project)).unwrap();
            let (reads, frame) = wire.next_sent();
            assert_eq!(reads.len(), 1, "{what} {method}: one settings reading, just before");
            assert_eq!(frame["params"]["config"]["projects"], json!({key(&project): {"trust_level": level}}), "{what} {method}: exactly one entry, under the canonical spelling");
        }
        let trust_status = thread_row(&host, "thread")["level"]["projectTrust"].clone();
        assert_eq!((trust_status["case"].as_str(), trust_status["sent"].as_str()), (Some(case), Some(level)), "{what}");
        assert_eq!(trust_status["appChoice"], json!(if source == SET_UP { if case == "switched-off" { "off" } else if case == "choice-not-read" { "not-read" } else { "on" } } else { "none" }), "{what}");
        assert_eq!(trust.view()["lastSent"]["case"], json!(case), "{what}: the view shows what the last frame sent");
        wire.close(&host);
        std::fs::remove_dir_all(&base).unwrap();
    }
}

#[test]
fn a_folder_that_is_not_the_apps_project_gets_todays_rule_exactly() {
    let (base, project, _, _) = git_project("app-trust-elsewhere");
    let (host, trust) = app_project_host(&base, &project, SET_UP);
    let wire = Responder::attach(&host, |_| layers_with(json!({})));
    // A subfolder of the project, and a folder outside it: the App's on is not inferred.
    for cwd in [project.join("sub"), base.clone()] {
        send(&host, "thread/start", json!({"cwd": cwd})).unwrap();
        let (_, frame) = wire.next_sent();
        let entry = frame["params"]["config"]["projects"].as_object().unwrap().clone();
        assert_eq!(entry.len(), 1);
        assert_eq!(entry.values().next().unwrap(), &json!({"trust_level": "untrusted"}), "{}", cwd.display());
    }
    assert!(trust.view()["lastSent"].is_null(), "no frame of the App's project was sent");
    wire.close(&host);
    std::fs::remove_dir_all(&base).unwrap();
}

#[test]
fn a_switch_takes_effect_at_the_next_start_resume_or_fork_and_not_on_a_running_conversation() {
    let (base, project, _, _) = git_project("app-trust-next");
    let (host, trust) = app_project_host(&base, &project, SET_UP);
    crate::records_store::attach(&project, true).unwrap();
    let wire = Responder::attach(&host, |_| layers_with(json!({})));
    send(&host, "thread/resume", frame_params("thread/resume", &project)).unwrap();
    assert_eq!(wire.next_sent().1["params"]["config"]["projects"], json!({key(&project): {"trust_level": "trusted"}}));
    trust.switch_off_launched().unwrap();
    // The running conversation's next turn carries no trust entry: nothing changes for it.
    send(&host, "turn/start", turn_params("thread")).unwrap();
    let (reads, turn) = wire.next_sent();
    assert!(reads.is_empty() && turn["params"].get("config").and_then(|c| c.get("projects")).is_none());
    // The view says the choice is off while the last frame sent was trusted: they can differ.
    let view = trust.view();
    assert_eq!((view["choice"].as_str(), view["lastSent"]["sent"].as_str()), (Some("off"), Some("trusted")));
    for (method, _) in START_RESUME_FORK {
        send(&host, method, frame_params(method, &project)).unwrap();
        assert_eq!(wire.next_sent().1["params"]["config"]["projects"], json!({key(&project): {"trust_level": "untrusted"}}), "{method}");
    }
    // On again, by the confirmed act: the next frame is trusted.
    let token = trust.preview_on_launched().unwrap()["token"].as_str().unwrap().to_owned();
    trust.confirm_on(&token, |_, _, _| Ok(true)).unwrap();
    send(&host, "thread/resume", frame_params("thread/resume", &project)).unwrap();
    assert_eq!(wire.next_sent().1["params"]["config"]["projects"], json!({key(&project): {"trust_level": "trusted"}}));
    assert_eq!(thread_row(&host, "thread")["level"]["projectTrust"]["case"], "app-on-by-switch");
    wire.close(&host);
    std::fs::remove_dir_all(&base).unwrap();
}

/// A Host of another home, made from `account`'s App custody as the App makes its key and local homes, ready with
/// the one conversation in `cwd`.
fn other_home(account: &Arc<Host>, cwd: &Path) -> Arc<Host> {
    let host = Arc::new(Host::new_with_app_custody(account.app_runtime_custody().unwrap()).unwrap());
    let generation = g(&host);
    let mut i = host.inner.0.lock().unwrap();
    i.state = "ready".into();
    i.home = "level-home".into();
    i.spawn_counter = 1;
    i.generation = generation.clone();
    i.journal.begin_generation(generation.clone());
    i.threads.push(json!({"generation": generation, "threadId": "thread", "cwd": cwd}));
    i.level.trust_reads = true;
    drop(i);
    host.set_default_level("edits").unwrap();
    host
}

#[test]
fn a_key_home_and_a_local_home_apply_the_same_rule() {
    let (base, project, _, _) = git_project("app-trust-homes");
    let account = trusting_host(&base, &project, "edits");
    // A home made before the App's projects are configured gets them too: one for every home.
    let key_home = other_home(&account, &project);
    let trust = Arc::new(crate::project_trust::ProjectTrust::for_launch(Some(&project), SET_UP));
    account.configure_project_trust(Arc::clone(&trust));
    let local_home = other_home(&account, &project);
    for (name, home) in [("key", &key_home), ("local", &local_home)] {
        assert!(Arc::ptr_eq(&home.project_trust().unwrap(), &trust), "{name}");
        let wire = Responder::attach(home, |_| layers_with(json!({})));
        send(home, "thread/resume", frame_params("thread/resume", &project)).unwrap();
        assert_eq!(wire.next_sent().1["params"]["config"]["projects"], json!({key(&project): {"trust_level": "trusted"}}), "{name}");
        assert_eq!(thread_row(home, "thread")["level"]["projectTrust"]["case"], "app-on-by-setup", "{name}");
        wire.close(home);
    }
    std::fs::remove_dir_all(&base).unwrap();
}

#[test]
fn a_trusted_projects_settings_file_that_stops_a_start_reaches_the_status_and_other_refusals_do_not() {
    let (base, project, _, _) = git_project("app-trust-refusal");
    let file = project.join(".codex").join("config.toml");
    std::fs::create_dir_all(file.parent().unwrap()).unwrap();
    let refused = |host: &Arc<Host>, wire: &Responder, method: &str, error: Value| {
        let request = send(host, method, frame_params(method, &project)).unwrap();
        wire.next_sent();
        reply(host, json!({"jsonrpc": "2.0", "id": request.request_id(), "error": error}));
    };
    let parse = json!({"code": -32600, "message": format!("failed to load configuration: {}: TOML parse error", file.display())});
    // Trusted (set up through the App): said plainly, for a start and for a resume.
    let (host, _) = app_project_host(&base, &project, SET_UP);
    let wire = Responder::attach(&host, |_| layers_with(json!({})));
    refused(&host, &wire, "thread/start", parse.clone());
    let said = host.snapshot()["projectSettingsRefusal"].clone();
    assert_eq!(said["lines"], json!([cl::PROJECT_SETTINGS_NOT_LOADED]));
    assert_eq!((said["method"].as_str(), said["files"].clone()), (Some("thread/start"), json!([file.to_string_lossy()])));
    assert_eq!(said["codexReason"]["standing"], cl::NOT_THE_APPS_TEXT);
    refused(&host, &wire, "thread/resume", json!({"code": -32600, "message": "failed to load configuration: `invented` is no longer supported; remove it from config.toml"}));
    let row = thread_row(&host, "thread");
    assert_eq!(row["level"]["projectSettingsRefusal"]["fileSentence"], cl::PROJECT_SETTINGS_FILE_CANDIDATES);
    assert_eq!(row["level"]["projectSettingsRefusal"]["remedy"], cl::PROJECT_SETTINGS_REMEDY);
    // Another refusal of a trusted entry is left as it is.
    refused(&host, &wire, "thread/fork", json!({"code": -32603, "message": "invented internal error"}));
    assert_eq!(host.snapshot()["projectSettingsRefusal"]["method"], "thread/resume", "the fork's refusal adds nothing");
    wire.close(&host);
    // Untrusted (environment route, unmarked): the same error adds nothing.
    let (host, _) = app_project_host(&base, &project, ENVIRONMENT);
    let wire = Responder::attach(&host, |_| layers_with(json!({})));
    refused(&host, &wire, "thread/start", parse);
    assert!(host.snapshot()["projectSettingsRefusal"].is_null());
    wire.close(&host);
    std::fs::remove_dir_all(&base).unwrap();
}

#[test]
fn with_no_records_store_the_environment_route_is_unchanged_and_the_setup_route_is_fail_closed() {
    let (base, project, _, _) = git_project("app-trust-no-store");
    crate::records_store::use_store_for_test(Some(Err("no records store configured (invented)".into())));
    for (source, mark, level, case) in [(ENVIRONMENT, "trusted", "trusted", "trusted"), (ENVIRONMENT, "none", "untrusted", "unmarked"),
                                        (SET_UP, "none", "untrusted", "choice-not-read"), (SET_UP, "trusted", "untrusted", "choice-not-read")] {
        let (host, _) = app_project_host(&base, &project, source);
        let k = key(&project);
        let wire = Responder::attach(&host, move |_| layers_with(if mark == "trusted" { json!({k.clone(): {"trust_level": "trusted"}}) } else { json!({}) }));
        send(&host, "thread/resume", frame_params("thread/resume", &project)).unwrap();
        assert_eq!(wire.next_sent().1["params"]["config"]["projects"], json!({key(&project): {"trust_level": level}}), "{source} {mark}");
        let status = thread_row(&host, "thread")["level"]["projectTrust"].clone();
        assert_eq!(status["case"], case, "{source} {mark}");
        if case == "choice-not-read" { assert_eq!(status["lines"], json!([cl::TRUST_CHOICE_NOT_READ])); }
        wire.close(&host);
    }
    crate::records_store::use_store_for_test(None);
    std::fs::remove_dir_all(&base).unwrap();
}

#[test]
fn the_settings_file_message_does_not_outlive_its_cause() {
    let (base, project, _, _) = git_project("app-trust-refusal-cleared");
    crate::records_store::attach(&project, true).unwrap();
    let elsewhere = base.join("elsewhere");
    std::fs::create_dir_all(&elsewhere).unwrap();
    let (host, trust) = app_project_host(&base, &project, SET_UP);
    let wire = Responder::attach(&host, |_| layers_with(json!({})));
    let error = json!({"code": -32600, "message": "failed to load configuration: `invented` is no longer supported; remove it from config.toml"});
    let answer = |method: &str, cwd: &Path, outcome: Value| {
        let params = if method == "thread/start" { json!({"cwd": cwd}) } else { frame_params(method, cwd) };
        let request = send(&host, method, params).unwrap();
        wire.next_sent();
        let mut frame = json!({"jsonrpc": "2.0", "id": request.request_id()});
        let member = if outcome.get("code").is_some() { "error" } else { "result" };
        frame[member] = outcome;
        reply(&host, frame);
    };
    let shown = || (host.snapshot()["projectSettingsRefusal"].is_object(), thread_row(&host, "thread")["level"]["projectSettingsRefusal"].is_object());
    // A refused resume of the conversation: said in both places.
    answer("thread/resume", &project, error.clone());
    assert_eq!(shown(), (true, true));
    // A start that succeeds in another folder leaves it: its cause is this project's file.
    answer("thread/start", &elsewhere, json!({"thread": {"id": "elsewhere-thread"}}));
    assert_eq!(shown(), (true, true));
    // A later start in the same project that succeeds clears both.
    answer("thread/start", &project, json!({"thread": {"id": "new-thread"}}));
    assert_eq!(shown(), (false, false));
    // Refused again; a later resume of the conversation that succeeds clears both.
    answer("thread/resume", &project, error.clone());
    assert_eq!(shown(), (true, true));
    answer("thread/resume", &project, json!({"thread": {"id": "thread"}}));
    assert_eq!(shown(), (false, false));
    // Refused again; the person switches trust off: neither is shown from then on.
    answer("thread/resume", &project, error);
    assert_eq!(shown(), (true, true));
    trust.switch_off_launched().unwrap();
    assert_eq!(shown(), (false, false));
    wire.close(&host);
    std::fs::remove_dir_all(&base).unwrap();
}

// ---- Repair after the independent review: the rule (A) ----

/// A start in a project set up through the App, its frame built trusted and then held at the frame writer while
/// `between` runs. Returns whether the start's frame was written, and its trust entry when it was.
fn held_at_the_writer(name: &str, between: impl FnOnce(&Arc<Host>, &crate::project_trust::ProjectTrust)) -> Option<Value> {
    let (base, project, _, _) = git_project(name);
    crate::records_store::attach(&project, true).unwrap();
    let written = held_frame(&base, &project, true, between);
    std::fs::remove_dir_all(&base).unwrap();
    written
}
/// A start in `cwd`, its trust entry built trusted (by the App's on where `known`, the folder then being the App's
/// project; else by the settings' mark for it, the App's project being another folder), then held at the frame
/// writer while `between` runs. The trust entry written, or None when nothing was written.
fn held_frame(base: &Path, cwd: &Path, known: bool, between: impl FnOnce(&Arc<Host>, &crate::project_trust::ProjectTrust)) -> Option<Value> {
    let elsewhere = base.join("the-apps-project");
    std::fs::create_dir_all(&elsewhere).unwrap();
    let (host, trust) = app_project_host(base, if known { cwd } else { &elsewhere }, SET_UP);
    let mark = if known { json!({}) } else { json!({cl::folder_binding(cwd).key: {"trust_level": "trusted"}}) };
    let (asked_tx, asked_rx) = channel::<()>();
    let (go_tx, go_rx) = channel::<()>();
    let (asked_tx, go_rx) = (Mutex::new(asked_tx), Mutex::new(go_rx));
    let wire = Responder::attach(&host, move |_| {
        asked_tx.lock().unwrap().send(()).unwrap();
        go_rx.lock().unwrap().recv().unwrap();
        layers_with(mark.clone())
    });
    let (sender, folder) = (Arc::clone(&host), cwd.to_path_buf());
    let pending = std::thread::spawn(move || send(&sender, "thread/start", json!({"cwd": folder})).unwrap());
    asked_rx.recv_timeout(Duration::from_secs(5)).unwrap();
    // The reading's own frame is written; the writer is taken before its reply, so the start waits for it.
    let serial = host.frame_write.lock().unwrap();
    go_tx.send(()).unwrap();
    let deadline = std::time::Instant::now() + Duration::from_secs(5);
    while !host.inner.0.lock().unwrap().source_requests.values().any(|e| e.request.frame["method"] == "thread/start") {
        assert!(std::time::Instant::now() < deadline, "the start's frame was built");
        std::thread::yield_now();
    }
    between(&host, &trust);
    drop(serial);
    let request = pending.join().unwrap();
    let mut written = None;
    while let Ok(frame) = wire.frames.recv_timeout(Duration::from_millis(300)) {
        if frame["method"] == "thread/start" { written = Some(frame["params"]["config"]["projects"].clone()); }
    }
    if written.is_none() { assert_eq!(request.write_attempt_observed(), Some(false), "{}: nothing written", cwd.display()); }
    wire.close(&host);
    written
}

#[test]
fn a_trusted_frame_waiting_at_the_writer_is_not_written_after_a_switch_off_or_a_settings_write() {
    // The fixture itself: nothing between, the trusted frame is written.
    let written = held_at_the_writer("app-trust-held-nothing", |_, _| {}).expect("written");
    assert_eq!(written.as_object().unwrap().values().next().unwrap(), &json!({"trust_level": "trusted"}));
    // A switch-off completes while the frame waits: not written.
    assert_eq!(held_at_the_writer("app-trust-held-off", |_, trust| { trust.switch_off_launched().unwrap(); }), None);
    // A settings write is admitted while the frame waits: not written.
    assert_eq!(held_at_the_writer("app-trust-held-settings", |host, _| { host.inner.0.lock().unwrap().level.config_writes += 1; }), None);
}

#[test]
fn a_frame_in_a_project_folder_that_now_names_another_folder_is_untrusted_and_says_why() {
    let base = root("app-trust-repointed");
    let (first, second) = (base.join("first"), base.join("second"));
    for p in [&first, &second] { std::fs::create_dir_all(p).unwrap(); }
    crate::records_store::attach(&first, true).unwrap();
    let alias = base.join("alias");
    std::os::unix::fs::symlink(&first, &alias).unwrap();
    let (host, _trust) = app_project_host(&base, &alias, SET_UP);
    let wire = Responder::attach(&host, |_| layers_with(json!({})));
    let entry = |frame: Value| frame["params"]["config"]["projects"].as_object().unwrap().values().next().unwrap().clone();
    send(&host, "thread/start", json!({"cwd": alias})).unwrap();
    assert_eq!(entry(wire.next_sent().1), json!({"trust_level": "trusted"}));
    std::fs::remove_file(&alias).unwrap();
    std::os::unix::fs::symlink(&second, &alias).unwrap();
    let second = send(&host, "thread/start", json!({"cwd": alias})).unwrap();
    assert_eq!(entry(wire.next_sent().1), json!({"trust_level": "untrusted"}));
    let status = host.inner.0.lock().unwrap().level.request_sent[&second.request_id().to_string()]["projectTrust"].clone();
    assert_eq!((status["case"].as_str(), status["lines"].clone()), (Some("folder-changed"), json!([cl::TRUST_FOLDER_CHANGED])));
    wire.close(&host);
    std::fs::remove_dir_all(&base).unwrap();
}

// ---- Second repair: the revision and the new identity on every route (B) ----

#[test]
fn a_frame_waiting_at_the_writer_is_not_written_after_an_earlier_decisive_switch_line_was_replaced() {
    let line = |trust: &str, store: &str, id: &str| format!("{}\n", json!({"format": crate::project_trust::SWITCH_FORMAT, "at": "2026-11-19T05:00:00.000Z", "trust": trust, "storeId": store, "projectId": id}));
    for replace in [false, true] {
        let (base, project, _, _) = git_project(&format!("app-trust-revision-held-{replace}"));
        let attached = crate::records_store::attach(&project, true).unwrap();
        let (store, id) = (crate::records_store::opened_existing().unwrap().1, attached.project.unwrap());
        let file = attached.dir.unwrap().join(crate::records_store::TRUST_SWITCHES);
        std::fs::create_dir_all(file.parent().unwrap()).unwrap();
        // On here, then an on made in another store (passed over): the frame is built trusted.
        let passed_over = line("on", "another-store", &id);
        std::fs::write(&file, format!("{}{passed_over}", line("on", &store, &id))).unwrap();
        let written = held_frame(&base, &project, true, |_, _| {
            // The decisive line becomes an off; the count and the last line stay.
            if replace { std::fs::write(&file, format!("{}{passed_over}", line("off", &store, &id))).unwrap(); }
        });
        if replace { assert_eq!(written, None, "a frame built before the replacement is not written"); }
        else { assert_eq!(written.unwrap().as_object().unwrap().values().next().unwrap(), &json!({"trust_level": "trusted"}), "the control"); }
        std::fs::remove_dir_all(&base).unwrap();
    }
}

#[test]
fn an_environment_project_switched_on_then_given_a_new_identity_is_sent_untrusted_over_a_trusted_mark() {
    let (base, project, _, _) = git_project("app-trust-environment-new-identity");
    crate::records_store::attach(&project, true).unwrap();
    let (host, trust) = app_project_host(&base, &project, ENVIRONMENT);
    let token = trust.preview_on_launched().unwrap()["token"].as_str().unwrap().to_owned();
    trust.confirm_on(&token, |_, _, _| Ok(true)).unwrap();
    let line = trust.new_identity_off_line(&project).expect("every held project");
    crate::records_store::new_identity_with_trust_off(&project, Some(&line)).unwrap();
    let k = key(&project);
    let wire = Responder::attach(&host, move |_| layers_with(json!({k.clone(): {"trust_level": "trusted"}})));
    send(&host, "thread/start", json!({"cwd": project})).unwrap();
    let (_, frame) = wire.next_sent();
    assert_eq!(frame["params"]["config"]["projects"], json!({key(&project): {"trust_level": "untrusted"}}), "the off wins over the mark");
    assert_eq!(trust.view()["why"], "new-identity");
    wire.close(&host);
    std::fs::remove_dir_all(&base).unwrap();
}

// ---- Repair after the independent review: the settings-file message (E) ----

const UNSUPPORTED: &str = "failed to load configuration: `invented_key` is no longer supported; remove it from config.toml";
fn refuse(host: &Host, request: &SourceRequest, message: &str) {
    reply(host, json!({"jsonrpc": "2.0", "id": request.request_id(), "error": {"code": -32600, "message": message}}));
}

#[test]
fn the_settings_file_message_is_recorded_only_once_its_frame_settled_as_written() {
    let (base, project, _, _) = git_project("app-trust-notice-settled");
    let (host, _) = app_project_host(&base, &project, SET_UP);
    let me = Arc::clone(&host);
    let wire = Responder::attach(&host, move |_| {
        // After the reading's own write: the start's reply arrives before its write has settled.
        *me.before_request_write.lock().unwrap() = Some(Box::new(|h: &Host| {
            let id = h.inner.0.lock().unwrap().next_id;
            h.on_line(&serde_json::to_vec(&json!({"jsonrpc": "2.0", "id": id, "error": {"code": -32600, "message": UNSUPPORTED}})).unwrap(), &g(h));
            assert!(h.snapshot()["projectSettingsRefusal"].is_null(), "not before the write settles");
        }));
        layers_with(json!({}))
    });
    send(&host, "thread/start", json!({"cwd": project})).unwrap();
    wire.next_sent();
    assert_eq!(host.snapshot()["projectSettingsRefusal"]["lines"], json!([cl::PROJECT_SETTINGS_NOT_ATTRIBUTED]), "recorded once written");
    wire.close(&host);
    std::fs::remove_dir_all(&base).unwrap();
}

#[test]
fn the_settings_file_message_stands_exactly_as_long_as_its_cause() {
    let (base, project, _, _) = git_project("app-trust-notice-cause");
    let other = base.join("other");
    std::fs::create_dir_all(&other).unwrap();
    crate::records_store::attach(&project, true).unwrap();
    let (host, trust) = app_project_host(&base, &project, SET_UP);
    // The settings mark the other folder trusted, and the project as the test says.
    let project_mark = Arc::new(Mutex::new(json!({})));
    let (mark, other_key) = (Arc::clone(&project_mark), key(&other));
    let k = key(&project);
    let wire = Responder::attach(&host, move |_| {
        let mut projects = json!({other_key.clone(): {"trust_level": "trusted"}});
        if let Some(m) = mark.lock().unwrap().as_object() { for (_, v) in m { projects[k.clone()] = v.clone(); } }
        layers_with(projects)
    });
    let start = |cwd: &Path| { let r = send(&host, "thread/start", json!({"cwd": cwd})).unwrap(); wire.next_sent(); r };
    let shown = || host.snapshot()["projectSettingsRefusal"]["projectRoot"].as_str().map(str::to_owned);
    // A reply that arrives after a switch-off, for a frame sent before it: not shown.
    let request = start(&project);
    trust.switch_off_launched().unwrap();
    refuse(&host, &request, UNSUPPORTED);
    assert_eq!(shown(), None);
    confirmed_on(&trust);
    // Shown; then a later start whose settings now mark the project untrusted hides it.
    let request = start(&project);
    refuse(&host, &request, UNSUPPORTED);
    assert_eq!(shown(), Some(key(&project)));
    *project_mark.lock().unwrap() = json!({"mark": {"trust_level": "untrusted"}});
    let later = start(&project);
    assert_eq!(later.frame["params"]["config"]["projects"].as_object().unwrap().values().next().unwrap(), &json!({"trust_level": "untrusted"}));
    assert_eq!(shown(), None, "settings that now make the entry untrusted hide it");
    *project_mark.lock().unwrap() = json!({});
    // Another root's notice is not hidden by this project's switch-off.
    let request = start(&other);
    refuse(&host, &request, UNSUPPORTED);
    assert_eq!(shown(), Some(key(&other)));
    trust.switch_off_launched().unwrap();
    assert_eq!(shown(), Some(key(&other)), "an unrelated root's notice stands");
    wire.close(&host);
    std::fs::remove_dir_all(&base).unwrap();
}
fn confirmed_on(trust: &crate::project_trust::ProjectTrust) {
    let token = trust.preview_on_launched().unwrap()["token"].as_str().unwrap().to_owned();
    trust.confirm_on(&token, |_, _, _| Ok(true)).unwrap();
}

#[test]
fn the_commands_own_error_is_the_notices_first_sentence_and_every_other_refusal_is_unchanged() {
    let (base, project, _, _) = git_project("app-trust-notice-error");
    let (host, _) = app_project_host(&base, &project, SET_UP);
    let wire = Responder::attach(&host, |_| layers_with(json!({})));
    let fork = || { let r = send(&host, "thread/fork", frame_params("thread/fork", &project)).unwrap(); wire.next_sent(); r };
    let request = fork();
    refuse(&host, &request, UNSUPPORTED);
    let expected = format!("{} {}", cl::PROJECT_SETTINGS_NOT_ATTRIBUTED, cl::PROJECT_SETTINGS_SEE_TRUST);
    assert_eq!(host.settings_notice_error(request.request_ref()), Some(expected.clone()));
    let refused = host.thread_fork_finish(&request).unwrap_err();
    assert_eq!(refused, expected);
    assert!(!refused.contains(UNSUPPORTED) && !refused.contains("-32600"), "not Codex's error object");
    // Another refusal: its text as before.
    let request = fork();
    reply(&host, json!({"jsonrpc": "2.0", "id": request.request_id(), "error": {"code": -32603, "message": "invented internal error"}}));
    assert_eq!(host.settings_notice_error(request.request_ref()), None);
    assert!(host.thread_fork_finish(&request).unwrap_err().starts_with("thread/fork has no successful write and correlated result"));
    wire.close(&host);
    std::fs::remove_dir_all(&base).unwrap();
}

// ---- Second repair: what a frame is bound to (A) ----

#[test]
fn a_frame_waiting_at_the_writer_is_not_written_after_its_folder_or_root_changed_known_or_settings_only() {
    type Change = fn(&Path);
    // Each: a fresh folder layout, the conversation's folder in it, and the change made while the writer is held.
    let layouts: [(&str, fn(&Path) -> PathBuf, Change); 3] = [
        ("re-pointed", |base| {
            for f in ["first", "second"] { std::fs::create_dir_all(base.join(f)).unwrap(); }
            std::os::unix::fs::symlink(base.join("first"), base.join("alias")).unwrap();
            base.join("alias")
        }, |base| { std::fs::remove_file(base.join("alias")).unwrap(); std::os::unix::fs::symlink(base.join("second"), base.join("alias")).unwrap(); }),
        ("replaced at the same path", |base| { std::fs::create_dir_all(base.join("folder")).unwrap(); base.join("folder") },
            |base| { std::fs::rename(base.join("folder"), base.join("folder-old")).unwrap(); std::fs::create_dir_all(base.join("folder")).unwrap(); }),
        ("its Git root changed", |base| { std::fs::create_dir_all(base.join("repo").join("inner")).unwrap(); base.join("repo").join("inner") },
            |base| { std::fs::create_dir_all(base.join("repo").join(".git")).unwrap(); std::fs::write(base.join("repo").join(".git").join("HEAD"), b"ref: refs/heads/main\n").unwrap(); }),
    ];
    for (what, layout, change) in layouts {
        for known in [true, false] {
            let label = format!("{what}, {}", if known { "the App's project" } else { "settings only" });
            // The control: nothing changes, and the trusted frame is written.
            let base = root("app-trust-bound-control");
            let cwd = layout(&base);
            let written = held_frame(&base, &cwd, known, |_, _| {}).unwrap_or_else(|| panic!("{label}: the control is written"));
            assert_eq!(written.as_object().unwrap().values().next().unwrap(), &json!({"trust_level": "trusted"}), "{label}");
            std::fs::remove_dir_all(&base).unwrap();
            // The change while the frame waits: nothing written.
            let base = root("app-trust-bound");
            let cwd = layout(&base);
            assert_eq!(held_frame(&base, &cwd, known, |_, _| change(&base)), None, "{label}");
            std::fs::remove_dir_all(&base).unwrap();
        }
    }
}
