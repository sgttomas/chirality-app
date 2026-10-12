// Multi-year scale measurement of the record read paths (RS §14; DEL-01-02 §7).
// Included in `workflow_root_tests` (runtime_session.rs), so the Peer fixture
// is in scope for the record tick. `#[ignore]`: run on request with
//   cargo test --lib records_scale_report -- --ignored --nocapture --test-threads=1
// Sizes: CHIRALITY_SCALE_TIERS="runs:acts:ledgerLines,..." (default below).
// Each measurement runs in its own child process (this binary, re-run on
// `records_scale_child`) so its peak resident size is its own. Synthetic
// content: schema-valid entries written directly as lines (the writer's own
// per-append record-set read would make generating them quadratic); the act
// records cite sealed captures the App act control's way, so the act read
// verifies each one.

const SCALE_CHILD: &str = "runtime_session::workflow_root_tests::records_scale_child";
/// Entries per run log: what an App run writes today, roughly (run_opened and
/// its guidance and R3 references, ~3 checkpoint listings, an arrival or two
/// with labels and acts, one R5 model turn per turn, R13 per approval, run_ended).
const SCALE_ENTRIES_PER_RUN: usize = 30;
/// A realistic first year: 4 runs a working day for 250 days, 3 acts a run,
/// and ~340 ledger rows a run (10 turns x ~15 items: a conversation_index row
/// when an item opens and when it closes, plus register summaries).
const SCALE_FIRST_YEAR: (usize, usize, usize) = (1_000, 3_000, 340_000);

fn scale_tiers() -> Vec<(usize, usize, usize)> {
    let text = std::env::var("CHIRALITY_SCALE_TIERS").unwrap_or_else(|_| "100:300:34000,1000:3000:340000,10000:100000:1000000".into());
    text.split(',').map(|t| { let v: Vec<usize> = t.split(':').map(|n| n.trim().parse().unwrap()).collect(); (v[0], v[1], v[2]) }).collect()
}
fn scale_rss_bytes() -> u64 {
    let mut usage: libc::rusage = unsafe { std::mem::zeroed() };
    unsafe { libc::getrusage(libc::RUSAGE_SELF, &mut usage); }
    let max = usage.ru_maxrss as u64;
    if cfg!(target_os = "macos") { max } else { max * 1024 }
}
fn scale_ms(start: std::time::Instant) -> f64 { (start.elapsed().as_secs_f64() * 1000.0 * 10.0).round() / 10.0 }

/// Writes `runs` run logs of SCALE_ENTRIES_PER_RUN schema-valid entries each.
fn scale_runs(root: &std::path::Path, runs: usize) {
    use std::io::Write;
    let validator = crate::schema_validation::bundled().unwrap();
    let rec = &crate::records::APP_WRITER;
    for r in 0..runs {
        let run = format!("run:scale:{r}");
        let log = crate::storage::project_log(root, Some(&run), "app-writer:local");
        std::fs::create_dir_all(log.parent().unwrap()).unwrap();
        let mut out = std::io::BufWriter::new(std::fs::File::create(&log).unwrap());
        for seq in 1..=SCALE_ENTRIES_PER_RUN as u64 {
            let (kind, body) = match seq {
                n if n == SCALE_ENTRIES_PER_RUN as u64 => ("run_ended", json!({"stoppedBy":"the person","cause":"ended by the person","waitingArrivals":[]})),
                n if n % 3 == 0 => ("tool_permission_settlement", json!({"request":format!("server-request:1/{n}"),"settledBy":"the person via interaction","settlement":"answered"})),
                n if n % 7 == 0 => ("evidence_limit", json!({"label":"lost acknowledgement","subjectRef":format!("server-request:1/{n}"),"detail":"synthetic scale entry"})),
                n => ("model_turn", json!({"turn":n,"scope":"turn","requested":"fixture-provider/fixture-model","effective":"fixture-provider/fixture-model","destinationClass":"local model server"})),
            };
            let entry = crate::records::envelope(kind, rec, body, format!("rec:app:scale-{r}-{seq}"), seq, Some(&run), Some("2026-10-12T00:00:00.000Z"));
            if r == 0 { validator.validate(&entry).unwrap_or_else(|e| panic!("{kind}: {e}")); }
            writeln!(out, "{}", serde_json::to_string(&entry).unwrap()).unwrap();
        }
    }
}
/// Writes `acts` A7 act records (by the App's capturing surface) to one acts
/// log, each citing its own capture sealed under the key folder in use.
fn scale_acts(root: &std::path::Path, acts: usize) {
    use std::io::Write;
    let validator = crate::schema_validation::bundled().unwrap();
    let log = crate::storage::project_log(root, None, "scale-act-writer");
    std::fs::create_dir_all(log.parent().unwrap()).unwrap();
    let mut out = std::io::BufWriter::new(std::fs::File::create(&log).unwrap());
    let file = root.join("out/summary.md");
    for a in 0..acts {
        let id = format!("cap:scale-{a}");
        let mut capture = json!({"format":"chirality.aac.capture-evidence","formatVersion":"0.3","captureId":id,"offerId":format!("offer:{id}"),
            "offerDigest":{"method":"aac-offer-digest/0.1","value":"0".repeat(64)},"choice":"act","actKind":"A7",
            "actor":{"osAccount":"fixture","identityVerified":false},"boundSubject":[file.to_str().unwrap()],"boundContent":[{"method":"chirality.app.exact-bytes.sha256/v1","value":crate::util::sha256_hex(format!("v{a}").as_bytes())}],
            "scope":"The summary file.","purpose":"You decide.","capturedAt":"2026-10-12T00:00:00.000Z","surface":"App interface","inputSource":"host-native-confirmation",
            "answers":{"standing":"no arrival: a standing act (RC-6)"},"evidenceLimits":["identity not verified"]});
        if a == 0 { crate::schema_validation::validate_capture(&capture).unwrap(); }
        crate::capture_seal::seal(root, &mut capture).unwrap();
        let path = crate::storage::capture_path(root, &id);
        if a == 0 { std::fs::create_dir_all(path.parent().unwrap()).unwrap(); }
        std::fs::write(path, serde_json::to_vec(&capture).unwrap()).unwrap();
        let kind = crate::records::capture_record_kind(&capture).unwrap();
        let entry = crate::records::envelope(kind, &crate::records::APP_INTERFACE, crate::act_control::act_body(&capture), format!("rec:app:scale-act-{a}"), a as u64 + 1, None, None);
        if a == 0 { validator.validate(&entry).unwrap(); }
        writeln!(out, "{}", serde_json::to_string(&entry).unwrap()).unwrap();
    }
}
/// A ledger of `lines` schema-valid rows: one session start, then per
/// conversation item an index row as it opens and as it closes, and a register
/// summary pair every eighth item.
fn scale_ledger(path: &std::path::Path, lines: usize) {
    use std::io::Write;
    let mut out = std::io::BufWriter::new(std::fs::File::create(path).unwrap());
    let session = "app-session:scale";
    let start = json!({"kind":"session_started","session":session,"at":"2026-01-01T00:00:00.000Z","candidate":"chirality-app-v4-unqualified","previousSessionEnd":"none"});
    let first = crate::recovery::RecoveryLedger::validate_pointer_entry(&start);
    let mut written = 0;
    if first.is_ok() { writeln!(out, "{start}").unwrap(); written += 1; }
    let generation = json!({"appSession":session,"home":"H-acct","spawnCounter":1});
    let mut item = 0u64;
    let mut checked = std::collections::BTreeSet::new();
    while written < lines {
        item += 1;
        let thread = format!("thread-{}", item / 150);
        let turn = format!("turn-{}", item / 15);
        let index = |open: bool| json!({"kind":"conversation_index","session":session,"at":"2026-10-12T00:00:00.000Z","threadId":thread,"home":"H-acct","project":"scale App project","tags":[],
            "lastLoadedGeneration":crate::recovery::generation_ref(&generation).unwrap(),
            "lastObservedExecution":{"state":"turn-live","at":"2026-10-12T00:00:00.000Z","liveTurn":turn,"openItems":if open {json!([{"turnId":turn,"itemId":format!("item-{item}"),"itemType":"commandExecution"}])} else {json!([])}}});
        let mut rows = vec![index(true), index(false)];
        if item % 8 == 0 {
            let request = json!({"requestId":item,"generation":generation,"method":"item/commandExecution/requestApproval","nativeParameters":{"threadId":thread,"turnId":turn,"itemId":format!("item-{item}")},
                "state":"outstanding","replyWriteResult":"not-attempted","classification":"known-answerable"});
            rows.push(crate::recovery::RecoveryLedger::request_summary_entry(&request, &[]).unwrap().unwrap());
            let mut closed = request.clone();
            closed["state"] = json!("answered");closed["replyWriteResult"] = json!("written");
            closed["settlement"] = json!({"origin":"person-via-interaction","actor":"person:p (identity not verified)","content":{"decision":"accept"}});
            rows.push(crate::recovery::RecoveryLedger::request_summary_entry(&closed, &[]).unwrap().unwrap());
        }
        for row in rows {
            if written >= lines { break; }
            let kind = row["kind"].as_str().unwrap().to_owned() + row["state"].as_str().unwrap_or("");
            if checked.insert(kind.clone()) { crate::recovery::RecoveryLedger::validate_pointer_entry(&row).unwrap_or_else(|e| panic!("{kind}: {e}: {row}")); }
            writeln!(out, "{row}").unwrap();
            written += 1;
        }
    }
    if let Err(e) = first { println!("SCALE-NOTE session_started row not written: {e}"); }
}

/// One measurement in its own process. Does nothing unless run by the report.
#[test]
#[ignore = "child process of records_scale_report"]
fn records_scale_child() {
    let Ok(spec) = std::env::var("CHIRALITY_SCALE_CHILD") else { return };
    let spec: Value = serde_json::from_str(&spec).unwrap();
    let root = std::path::PathBuf::from(spec["root"].as_str().unwrap());
    crate::capture_seal::set_folder_for_test(Some(Some(std::path::PathBuf::from(spec["keys"].as_str().unwrap()))));
    let t = std::time::Instant::now;
    let result = match spec["what"].as_str().unwrap() {
        "read_all" => {
            let start = t();
            let (entries, limits) = crate::storage::read_all(&root);
            let read = scale_ms(start);
            let rss = scale_rss_bytes();
            let count = entries.len();
            drop(entries);
            // The RS writer's own per-append record-set check (append_reserved):
            // the first append in a process reads the set once (the index is
            // built); the next ones read only what changed.
            let probe = |n: u32| crate::records::append_project_reserved(&root, "run:scale-probe", "app-writer:local", "evidence_limit", &crate::records::APP_WRITER,
                json!({"label":"unresolvable reference","subjectRef":"scale probe"}), &format!("rec:app:scale-probe-{n}"), "2026-10-12T00:00:00.000Z");
            let start = t();
            let appended = probe(0);
            let first = scale_ms(start);
            let start = t();
            for n in 1..=10 { probe(n).unwrap(); }
            let next = scale_ms(start) / 10.0;
            json!({"readAllMs":read,"entries":count,"limits":limits.len(),"peakRssBytes":rss,"oneAppendMs":first,"nextAppendMs":next,"appendOk":appended.is_ok(),"peakRssAfterAppendsBytes":scale_rss_bytes()})
        }
        "acts" => {
            let start = t();
            let fingerprint = crate::checkpoint_recorder::act_records_fingerprint(&root).map(|f| f.len());
            let fingerprint_ms = scale_ms(start);
            let start = t();
            let read = crate::checkpoint_recorder::project_act_records(&root).unwrap();
            let act_read = scale_ms(start);
            // After a run entry is written, the act read again (no act record changed).
            crate::records::append_project(&root, Some("run:scale-acts"), "app-writer:local", "evidence_limit", &crate::records::APP_WRITER,
                json!({"label":"unresolvable reference","subjectRef":"scale act probe"})).unwrap();
            let start = t();
            let again = crate::checkpoint_recorder::project_act_records(&root).unwrap();
            let act_again = scale_ms(start);
            json!({"fingerprintMs":fingerprint_ms,"fingerprintPaths":fingerprint,"actReadMs":act_read,"actReadAfterRunEntryMs":act_again,"acts":read.acts.len(),"actsAgain":again.acts.len(),"unresolved":read.unresolved.len(),"peakRssBytes":scale_rss_bytes()})
        }
        "ledger" => {
            let path = std::path::PathBuf::from(spec["ledger"].as_str().unwrap());
            let start = t();
            let mut ledger = crate::recovery::RecoveryLedger::open(path.clone()).unwrap();
            let open = scale_ms(start);
            let open_rss = scale_rss_bytes();
            let start = t();
            let snapshot = ledger.snapshot();
            let snapshot_ms = scale_ms(start);
            let start = t();
            let bytes = serde_json::to_vec(&snapshot).unwrap().len();
            let serialize_ms = scale_ms(start);
            drop(snapshot);
            // One fact as the Host persists it: append, then a fresh snapshot.
            let start = t();
            ledger.append(crate::recovery::RecoveryLedger::session_end_entry("app-session:scale", "quit", &[]).unwrap()).unwrap();
            let _ = ledger.snapshot();
            let append_ms = scale_ms(start);
            let rows = ledger.snapshot()["entries"].as_array().unwrap().len();
            drop(ledger);
            // App startup: the Host opens the ledger, starts its session and builds custody.
            let host = crate::hosting::Host::new();
            let start = t();
            host.configure_recovery(path).unwrap();
            let configure = scale_ms(start);
            let start = t();
            let snap = host.snapshot();
            let host_snapshot_ms = scale_ms(start);
            drop(snap);
            json!({"rows":rows,"openMs":open,"rssAfterOpenBytes":open_rss,"snapshotCloneMs":snapshot_ms,"snapshotJsonBytes":bytes,"snapshotSerializeMs":serialize_ms,
                "appendAndSnapshotMs":append_ms,"hostConfigureMs":configure,"hostSnapshotMs":host_snapshot_ms,"peakRssBytes":scale_rss_bytes()})
        }
        "tick" => {
            let peer = Peer::new();
            let mut wr = declared(&peer);
            let a = open_run(&peer, &mut wr, "thread");
            let project = peer.fixture.root.clone();
            std::fs::create_dir_all(project.join("out")).unwrap();
            std::fs::write(project.join("out/summary.md"), b"v1").unwrap();
            scale_runs(&project, spec["runs"].as_u64().unwrap() as usize);
            scale_acts(&project, spec["acts"].as_u64().unwrap() as usize);
            let shared = wr.runs[&a].clone();
            let mut run = shared.lock().unwrap();
            let before = own_log(&peer, &a).len();
            let start = t();
            run.observe_checkpoints(&recorder_view(&peer, &[]));
            let first = scale_ms(start);
            let start = t();
            run.observe_checkpoints(&recorder_view(&peer, &[]));
            let quiet = scale_ms(start);
            let start = t();
            run.observe_checkpoints(&recorder_view(&peer, &summary_items()));
            let writing = scale_ms(start);
            let written = own_log(&peer, &a).len() - before;
            // A later tick writing again (another report arrives).
            let mut more = summary_items().to_vec();
            more.push(json!({"id":"m2","type":"agentMessage","text":"Spacing report"}));
            let before_next = own_log(&peer, &a).len();
            let start = t();
            run.observe_checkpoints(&recorder_view(&peer, &more));
            let next_writing = scale_ms(start);
            let next_written = own_log(&peer, &a).len() - before_next;
            json!({"firstTickMs":first,"quietTickMs":quiet,"writingTickMs":writing,"entriesWritten":written,"nextWritingTickMs":next_writing,"nextEntriesWritten":next_written,"pending":run.has_pending_records(),"peakRssBytes":scale_rss_bytes()})
        }
        other => panic!("unknown scale child {other}"),
    };
    println!("SCALE-RESULT {result}");
}

#[test]
#[ignore = "multi-year scale measurement; run on request"]
fn records_scale_report() {
    let keys = std::fs::canonicalize(std::env::temp_dir()).unwrap().join(crate::util::opaque_id("scale-seal-keys-").unwrap());
    crate::capture_seal::set_folder_for_test(Some(Some(keys.clone())));
    println!("SCALE first year estimate: runs {} (x{SCALE_ENTRIES_PER_RUN} entries), acts {}, ledger rows {}", SCALE_FIRST_YEAR.0, SCALE_FIRST_YEAR.1, SCALE_FIRST_YEAR.2);
    for (runs, acts, ledger_lines) in scale_tiers() {
        let root = std::fs::canonicalize(std::env::temp_dir()).unwrap().join(crate::util::opaque_id("records-scale-").unwrap());
        std::fs::create_dir_all(root.join("out")).unwrap();
        let start = std::time::Instant::now();
        scale_runs(&root, runs);
        scale_acts(&root, acts);
        let ledger = root.with_extension("ledger.jsonl");
        scale_ledger(&ledger, ledger_lines);
        let generated = scale_ms(start);
        let size = |p: &std::path::Path| std::fs::metadata(p).map(|m| m.len()).unwrap_or(0);
        let records_bytes: u64 = crate::storage::discover(&root).unwrap().iter().map(|p| size(p)).sum();
        let mut tier = json!({"runs":runs,"acts":acts,"ledgerLines":ledger_lines,"recordLogBytes":records_bytes,"ledgerBytes":size(&ledger),"generateMs":generated});
        for what in ["read_all", "acts", "ledger", "tick"] {
            let spec = json!({"what":what,"root":root,"keys":keys,"ledger":ledger,"runs":runs,"acts":acts});
            let output = std::process::Command::new(std::env::current_exe().unwrap())
                .args([SCALE_CHILD, "--exact", "--ignored", "--nocapture", "--test-threads=1"])
                .env("CHIRALITY_SCALE_CHILD", spec.to_string()).output().unwrap();
            let text = String::from_utf8_lossy(&output.stdout);
            let result = text.lines().find_map(|l| l.split_once("SCALE-RESULT ").map(|(_, r)| r.to_owned()))
                .unwrap_or_else(|| panic!("{what}: no result: {text} {}", String::from_utf8_lossy(&output.stderr)));
            for note in text.lines().filter(|l| l.contains("SCALE-NOTE")) { println!("{note}"); }
            tier[what] = serde_json::from_str(&result).unwrap();
        }
        println!("SCALE {tier}");
        let _ = std::fs::remove_dir_all(&root);
        let _ = std::fs::remove_file(&ledger);
    }
    let _ = std::fs::remove_dir_all(&keys);
}
