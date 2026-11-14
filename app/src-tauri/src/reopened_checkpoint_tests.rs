// The reopened read through the actual run and RS writer: a run's checkpoint
// records as read, and its declared actor only where the recorded package
// digest verifies it. Included in workflow_root_tests, beside its fixtures.

/// A declared run with one arrival of CP-check waiting, then lost process state.
fn reopened_after_an_arrival() -> (Peer, String) {
    let peer = Peer::new();
    let mut root = declared(&peer);
    let a = open_run(&peer, &mut root, "thread");
    root.runs[&a].lock().unwrap().observe_checkpoints(&recorder_view(&peer, &[json!({"id":"m1","type":"agentMessage","text":"Spacing report"})]));
    drop(root);
    (peer, a)
}
fn reopened_entry(peer: &Peer, run: &str) -> Value {
    let reopened = WorkflowRootSession::default().reopen(&peer.fixture.root, &[]).unwrap();
    reopened["runs"].as_array().unwrap().iter().find(|r| r["run"] == run).unwrap().clone()
}
/// The package the run was started from, as its run-start record names it.
fn started_package(peer: &Peer, run: &str) -> std::path::PathBuf {
    let records = crate::workflow_workspace::publication::ProjectRecords::open(&peer.fixture.root).unwrap();
    let start = records.list_references().unwrap().into_iter()
        .map(|r| records.resolve(&r).unwrap().body().clone())
        .find(|b| b["record_kind"] == "run_text" && b["purpose"] == "run start" && b["run"] == run)
        .unwrap();
    std::path::Path::new(start["holding_library"].as_str().unwrap()).join(start["workflow"]["name"].as_str().unwrap())
}
fn not_established(entry: &Value) -> Option<String> {
    entry["limits"].as_array().unwrap().iter().filter_map(Value::as_str).find(|l| l.starts_with("the declared actor was not established")).map(str::to_owned)
}

#[test]
fn a_reopened_run_gives_its_records_as_read_and_makes_no_disposition() {
    let (peer, a) = reopened_after_an_arrival();
    let log = rs_for(&peer, &a);
    let entry = reopened_entry(&peer, &a);
    assert_eq!(entry["reference"], a.as_str());
    assert_eq!(entry["state"], "open; interrupted (no run_ended recorded)", "current fields kept");
    assert_eq!(entry["lifecycle"]["end"], Value::Null);
    let records = entry["lifecycle"]["records"].as_array().unwrap();
    // Exactly the run's log, in order: nothing filtered, nothing made.
    assert_eq!(records.len(), log.len(), "{records:?}");
    for (shown, read) in records.iter().zip(&log) {
        assert_eq!((&shown["kind"], &shown["recordId"], &shown["observedAt"], &shown["body"]), (&read["kind"], &read["recordId"], &read["observedAt"], &read["body"]));
        assert_eq!((shown["written"].as_bool(), shown["writtenLate"].as_bool(), shown["neverWritten"].as_bool()), (Some(true), Some(false), Some(false)));
    }
    let kinds: Vec<&str> = records.iter().filter_map(|r| r["kind"].as_str()).collect();
    assert!(kinds.contains(&"checkpoint_listed") && kinds.contains(&"checkpoint_arrival"), "{kinds:?}");
    let dispositions: Vec<&Value> = records.iter().filter(|r| r["kind"] == "disposition_change").map(|r| &r["body"]["disposition"]).collect();
    assert_eq!(dispositions, vec![&json!("waiting")], "the one recorded disposition, and no other");
}

#[test]
fn a_reopened_runs_declared_actor_is_given_only_as_verified_and_said_where_it_came_from() {
    let (peer, a) = reopened_after_an_arrival();
    let entry = reopened_entry(&peer, &a);
    assert_eq!(not_established(&entry), None, "{}", entry["limits"]);
    let compatibility = entry["compatibility"].as_array().unwrap();
    assert_eq!(compatibility.len(), 1);
    assert_eq!(compatibility[0]["source"], crate::records::supply::DECLARED_SOURCE);
    let checkpoints = compatibility[0]["preparation"]["declaration"]["elements"]["checkpoints"].as_array().unwrap();
    let check = checkpoints.iter().find(|c| c["value"]["name"] == "CP-check").unwrap();
    assert_eq!(check["value"]["actor"], "the_person");
    // The resolved declaration is apart from the run's records, never one of them.
    assert!(entry["lifecycle"]["records"].as_array().unwrap().iter().all(|r| r["body"].get("elements").is_none()));
}

#[test]
fn a_declaration_whose_bytes_differ_or_are_gone_is_not_used_and_nothing_is_inferred() {
    for change in ["bytes differ", "revision gone"] {
        let (peer, a) = reopened_after_an_arrival();
        let package = started_package(&peer, &a);
        let workflow = package.join("WORKFLOW.md");
        if change == "bytes differ" {
            let mut perms = std::fs::metadata(&workflow).unwrap().permissions();
            #[allow(clippy::permissions_set_readonly_false)]
            perms.set_readonly(false);
            std::fs::set_permissions(&workflow, perms).unwrap();
            let text = std::fs::read_to_string(&workflow).unwrap().replace("\"actor\":\"the_person\"", "\"actor\":\"the_agent\"");
            std::fs::write(&workflow, text).unwrap();
        } else {
            let aside = package.with_extension("aside");
            std::fs::rename(&package, &aside).unwrap();
        }
        let entry = reopened_entry(&peer, &a);
        assert!(entry.get("compatibility").is_none(), "{change}: {entry}");
        let why = not_established(&entry).unwrap_or_else(|| panic!("{change}: {}", entry["limits"]));
        if change == "bytes differ" {
            assert!(why.contains("differ"), "{why}");
        } else {
            assert!(why.contains("no longer yields"), "{why}");
        }
        assert!(!entry.to_string().contains("the_agent"), "{change}: the changed bytes are never shown");
        // The run's own records are still given whole.
        assert_eq!(entry["lifecycle"]["records"].as_array().unwrap().len(), rs_for(&peer, &a).len());
    }
}

#[test]
fn a_run_whose_log_cannot_be_read_whole_carries_that_limit_so_its_dispositions_read_not_known() {
    // Permitted: the whole log read, no limit on the run.
    let (peer, a) = reopened_after_an_arrival();
    let whole = reopened_entry(&peer, &a);
    assert!(whole["limits"].as_array().unwrap().iter().all(|l| !l.as_str().unwrap().contains("torn")), "{}", whole["limits"]);
    assert_eq!(whole["state"], "open; interrupted (no run_ended recorded)");
    // The same run with its log's last line cut short, read through the real reader: the run
    // carries the read limit and its state is unknown, so nothing it shows reads as established.
    let mut logs = vec![crate::storage::project_file(&peer.fixture.root, "runs").unwrap()];
    let mut cut = 0;
    while let Some(dir) = logs.pop() {
        for entry in std::fs::read_dir(&dir).unwrap().flatten() {
            let path = entry.path();
            if path.is_dir() {
                logs.push(path);
            } else if path.extension().is_some_and(|e| e == "jsonl") && std::fs::read_to_string(&path).unwrap().contains(a.as_str()) {
                use std::io::Write;
                std::fs::OpenOptions::new().append(true).open(&path).unwrap().write_all(b"{\"kind\":\"disposition_change\"").unwrap();
                cut += 1;
            }
        }
    }
    assert!(cut > 0, "the run's own log was found");
    let torn = reopened_entry(&peer, &a);
    assert!(!torn["limits"].as_array().unwrap().is_empty(), "the read limit is on the run: {torn}");
    assert_eq!(torn["state"], "unknown", "{torn}");
    let shown = torn["lifecycle"]["records"].as_array().unwrap();
    assert_eq!(shown.len(), whole["lifecycle"]["records"].as_array().unwrap().len(), "the cut line is never shown as a record");
}

#[test]
fn a_reading_that_cannot_read_stores_nothing_and_says_it_was_not_read_and_why() {
    // As the launch reads, through the same function as the person's Reopen.
    let (peer, a) = reopened_after_an_arrival();
    let workflows = std::sync::Mutex::new(WorkflowRootSession::default());
    // A folder name a person or a file could choose: it must never reach the App's own words.
    let missing = peer.fixture.root.join("invented project; chosen 'name' \u{202e}not-there");
    for (project, words) in [(Err("No explicit App project (CHIRALITY_WORKSPACE); nothing to reopen and no fallback"), 0), (Ok(missing.as_path()), 1)] {
        let refused = crate::runtime_session::reopen_recorded(&workflows, project, &[], &[]);
        assert!(refused.is_err());
        let root = workflows.lock().unwrap();
        assert!(root.reopened.is_none(), "nothing stored");
        let not_read = root.reopened_not_read.clone().unwrap();
        assert_eq!(not_read["state"], "not read");
        assert_eq!(not_read["words"], crate::runtime_session::REOPEN_NOT_READ_WORDS[words], "one of the closed set, exactly");
        assert_eq!(not_read["detail"].as_str(), refused.as_ref().err().map(String::as_str), "the reading's own reason, apart");
        assert_eq!(not_read["project"].as_str(), project.ok().map(|p| p.display().to_string()).as_deref());
        let detail = not_read["detail"].as_str().unwrap();
        assert!(!not_read["words"].as_str().unwrap().contains(detail) && !not_read["words"].as_str().unwrap().contains("chosen"), "nothing variable in the words");
    }
    assert!(!missing.exists(), "nothing was made");
    // A reading that reads replaces the reason and stores the view.
    let read = crate::runtime_session::reopen_recorded(&workflows, Ok(peer.fixture.root.as_path()), &[], &[]).unwrap();
    let root = workflows.lock().unwrap();
    assert!(root.reopened_not_read.is_none());
    assert!(root.reopened.as_ref().unwrap()["runs"].as_array().unwrap().iter().any(|r| r["run"] == a.as_str()));
    assert_eq!(root.reopened.as_ref(), Some(&read));
}

/// The run's own logs, by path.
fn run_logs(peer: &Peer, run: &str) -> Vec<std::path::PathBuf> {
    let mut pending = vec![crate::storage::project_file(&peer.fixture.root, "runs").unwrap()];
    let mut logs = Vec::new();
    while let Some(dir) = pending.pop() {
        for entry in std::fs::read_dir(&dir).unwrap().flatten() {
            let path = entry.path();
            if path.is_dir() {
                pending.push(path);
            } else if path.extension().is_some_and(|e| e == "jsonl") && std::fs::read_to_string(&path).unwrap().contains(run) {
                logs.push(path);
            }
        }
    }
    logs
}

#[test]
fn a_project_record_that_cannot_be_read_withholds_every_declared_actor() {
    // found (reading of 344): an unreadable second start restored the actor that two readable
    // starts withhold. Any unreadable record could be another start of this run.
    let (peer, a) = reopened_after_an_arrival();
    assert!(reopened_entry(&peer, &a).get("compatibility").is_some(), "permitted: every record reads");
    let unreadable = crate::storage::project_file(&peer.fixture.root, "workflow").unwrap().join("55555555-5555-4555-8555-555555555555.json");
    std::fs::write(&unreadable, b"{ not a record").unwrap();
    let entry = reopened_entry(&peer, &a);
    assert!(entry.get("compatibility").is_none(), "{entry}");
    assert!(not_established(&entry).is_some_and(|why| why.contains("could not be read")), "{}", entry["limits"]);
}

#[test]
fn the_declared_actor_is_withheld_when_the_runs_opening_names_another_revision() {
    // found (reading of 344): the actor came from the start while the workflow shown came from
    // run_opened; they must agree.
    let (peer, a) = reopened_after_an_arrival();
    assert!(reopened_entry(&peer, &a).get("compatibility").is_some(), "permitted: they agree");
    let mut rewritten = 0;
    for log in run_logs(&peer, &a) {
        let text = std::fs::read_to_string(&log).unwrap();
        let mut out: Vec<String> = Vec::new();
        for line in text.lines().filter(|l| !l.is_empty()) {
            let mut entry: Value = serde_json::from_str(line).unwrap();
            if entry["kind"] == "run_opened" && entry["runId"] == a.as_str() {
                entry["body"]["workflow"]["revision"] = json!("0".repeat(64));
                rewritten += 1;
            }
            if let Some(previous) = out.last() {
                entry["prevLine"] = crate::record_lines::link(Some(&crate::record_lines::line_identity(previous.as_bytes())));
            }
            out.push(entry.to_string());
        }
        std::fs::write(&log, out.join("\n") + "\n").unwrap();
    }
    assert_eq!(rewritten, 1);
    let entry = reopened_entry(&peer, &a);
    assert_eq!(entry["workflow"]["revision"], "0".repeat(64), "the opening is read as rewritten");
    assert!(entry.get("compatibility").is_none(), "{entry}");
    assert!(not_established(&entry).is_some_and(|why| why.contains("another workflow revision")), "{}", entry["limits"]);
}
