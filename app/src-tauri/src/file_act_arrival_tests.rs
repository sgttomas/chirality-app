// Owned local synthetic peer and native adapter; no supplier/person witness.
use tauri_plugin_dialog::MessageDialogResult;

fn fixture(kind: &str) -> (Peer, crate::AppState, String, String) {
    fixture_with(kind, "out/summary.md", true)
}
fn fixture_with(
    kind: &str,
    declared_path: &str,
    present: bool,
) -> (Peer, crate::AppState, String, String) {
    let peer = Peer::new();
    let path = peer.fixture.root.join("out/summary.md");
    std::fs::create_dir_all(path.parent().unwrap()).unwrap();
    std::fs::write(&path, b"v1").unwrap();
    let mut workflows = peer.registered_with(|draft| {
        let path = draft.join("WORKFLOW.md");
        let mut text = std::fs::read_to_string(&path).unwrap();
        let declaration = crate::checkpoint_recorder::tests::DECLARATION
            .replace(
                "\"required_act\":\"A7\"",
                &format!("\"required_act\":\"{kind}\""),
            )
            .replace("out/summary.md", declared_path);
        text.push_str(&format!("\n```workflow-declaration\n{declaration}\n```\n"));
        std::fs::write(path, text).unwrap();
    });
    let run = open_run(&peer, &mut workflows, "thread");
    if !present {
        std::fs::remove_file(&path).unwrap();
    }
    workflows.runs[&run]
        .lock()
        .unwrap()
        .observe_checkpoints(&recorder_view(&peer, &summary_items()[1..]));
    let arrival = rs_for(&peer, &run)
        .into_iter()
        .find(|e| e["kind"] == "checkpoint_arrival")
        .unwrap()["recordId"]
        .as_str()
        .unwrap()
        .to_owned();
    let (unused, mut state, _, _, _, _) = crate::workflow_root_context_tests::fixture();
    state.workspace = Some(peer.fixture.root.clone());
    state.act = Arc::new(Mutex::new(Some(crate::act_control::ActControl::new(
        &peer.fixture.root,
    ))));
    state.workflows = Mutex::new(workflows);
    state.homes = Mutex::new(HomeRouter::new(peer.home.clone()).unwrap());
    std::fs::remove_dir_all(unused).unwrap();
    (peer, state, run, arrival)
}
fn append_raw(log: &std::path::Path, mut entry: Value) {
    use std::io::Write;
    let bytes = std::fs::read(log).unwrap();
    let last = bytes
        .split(|b| *b == b'\n')
        .filter(|line| !line.is_empty())
        .last()
        .unwrap();
    entry["seq"] = json!(
        crate::records::read_log(log)
            .0
            .iter()
            .filter_map(|e| e["seq"].as_u64())
            .max()
            .unwrap()
            + 1
    );
    entry["prevLine"] = crate::record_lines::link(Some(&crate::record_lines::line_identity(last)));
    crate::schema_validation::bundled()
        .unwrap()
        .validate(&entry)
        .unwrap();
    let mut file = std::fs::OpenOptions::new().append(true).open(log).unwrap();
    writeln!(file, "{entry}").unwrap();
    file.sync_all().unwrap();
}
fn acts(peer: &Peer) -> Vec<Value> {
    peer.fixture
        .rs_entries()
        .into_iter()
        .filter(|e| matches!(e["kind"].as_str(), Some("human_act" | "act_declined")))
        .collect()
}
fn confirm(state: &crate::AppState, reference: &str, choice: &str) -> Value {
    crate::file_act_confirm_original(state, reference, |control, offer, observe| {
        control.synthetic_file_native(offer, observe, |text, kind| {
            assert!(
                text.contains("run run:") && text.contains("checkpoint CP-rely; arrival 1"),
                "{text}"
            );
            MessageDialogResult::Custom(
                if choice == "act" {
                    kind.wording()
                } else if choice == "decline" {
                    "Decline this act"
                } else {
                    "Cancel"
                }
                .into(),
            )
        })
    })
    .unwrap()
}

#[test]
fn file_act_arrival_production_connecting_path_and_dto() {
    let mut cases = vec![];
    for kind in ["A4", "A6", "A7"] {
        let (peer, state, run, arrival) = fixture(kind);
        let entry_run = state.workflows.lock().unwrap().runs[&run]
            .lock()
            .unwrap()
            .view(&run);
        assert_eq!(entry_run["fileActEntries"][&arrival]["state"], "candidate");
        let wire = peer.wire().len();
        let preview = crate::file_act_open_arrival_result(&state, &run, &arrival).unwrap();
        assert_eq!(preview["offer"]["actKind"], kind);
        assert_eq!(preview["offer"]["answers"]["runId"], run);
        assert_eq!(preview["utf8"], "v1");
        let result = confirm(&state, preview["reference"].as_str().unwrap(), "act");
        assert_eq!(result["state"], "AC-7 recorded", "{result}");
        let capture = &result["capture"];
        let entry = peer
            .fixture
            .rs_entries()
            .into_iter()
            .find(|e| {
                e["body"]["captureEvidence"]
                    .as_array()
                    .is_some_and(|refs| refs.iter().any(|r| r["ref"] == capture["captureId"]))
            })
            .unwrap();
        assert_eq!(entry["runId"], run);
        assert_eq!(
            entry["body"]["relations"]["arrivalAnswered"],
            capture["answers"]["arrival"]
        );
        assert!(crate::file_act_view::corresponds(capture, &entry));
        let log = crate::storage::project_log(
            &peer.fixture.root,
            Some(&run),
            crate::records::APP_INTERFACE.identity,
        )
        .unwrap();
        assert!(crate::records::read_log(&log).0.contains(&entry));
        assert!(
            crate::records::read_log(
                &crate::storage::project_file(&peer.fixture.root, crate::recorder::LOG).unwrap()
            )
            .0
            .iter()
            .all(|e| e["recordId"] != entry["recordId"]),
            "no duplicate standing entry"
        );
        state.workflows.lock().unwrap().runs[&run]
            .lock()
            .unwrap()
            .observe_checkpoints(&recorder_view(&peer, &summary_items()[1..]));
        assert!(rs_for(&peer, &run).iter().any(
            |e| e["kind"] == "act_counted" && e["body"]["act"]["recordId"] == entry["recordId"]
        ));
        assert_eq!(
            peer.wire().len(),
            wire,
            "preview/capture/counting sends nothing"
        );
        let read = crate::file_act_view::read(&peer.fixture.root);
        cases.push(json!({"kind":kind,"run":entry_run,"entryRun":entry_run,"preview":preview,"result":result,"record":entry,"read":read}));
    }
    println!("FILE_ACT_ARRIVAL_DTO:{}", json!({"cases":cases}));
}

#[test]
fn file_act_arrival_normalized_declared_path_and_saved_request_are_preserved() {
    let (peer, state, run, arrival) = fixture_with("A4", "./out//summary.md", true);
    let owned = state.workflows.lock().unwrap().runs[&run].clone();
    let mut view = recorder_view(&peer, &summary_items()[1..]);
    view["serverRequests"] = json!([{"requestIdentity":7,"generation":peer.generation,"method":"item/tool/requestUserInput","nativeParameters":{"threadId":"thread","turnId":"turn","itemId":"q"},"receiptPosition":30,"state":"outstanding"}]);
    owned.lock().unwrap().observe_checkpoints(&view);
    let request = rs_for(&peer, &run)
        .into_iter()
        .find(|e| e["kind"] == "act_request")
        .unwrap();
    let preview = crate::file_act_open_arrival_result(&state, &run, &arrival).unwrap();
    assert_eq!(
        preview["offer"]["subject"]["ref"],
        peer.fixture.root.join("out/summary.md").to_str().unwrap()
    );
    assert_eq!(preview["offer"]["requestRef"], request["recordId"]);
    assert_eq!(preview["offer"]["scope"], "The summary file.");
    let result = confirm(&state, preview["reference"].as_str().unwrap(), "act");
    assert_eq!(result["capture"]["requestRef"], request["recordId"]);
    assert_eq!(
        result["record"]["body"]["relations"]["requestRef"],
        request["recordId"]
    );
    assert!(crate::file_act_view::corresponds(
        &result["capture"],
        &result["record"]
    ));
}

#[test]
fn file_act_arrival_recheck_uses_recorded_effective_lapse_content_and_retains_history() {
    let (peer, state, run, arrival) = fixture("A4");
    let first = crate::file_act_open_arrival_result(&state, &run, &arrival).unwrap();
    let original = confirm(&state, first["reference"].as_str().unwrap(), "act");
    let owned = state.workflows.lock().unwrap().runs[&run].clone();
    let view = recorder_view(&peer, &summary_items()[1..]);
    owned.lock().unwrap().observe_checkpoints(&view);
    std::fs::write(peer.fixture.root.join("out/summary.md"), b"v2").unwrap();
    owned.lock().unwrap().observe_checkpoints(&view);
    let lapse = rs_for(&peer, &run)
        .into_iter()
        .find(|e| e["kind"] == "act_lapsed" && e["body"]["state"] == "lapsed")
        .unwrap();
    assert_eq!(
        lapse["body"]["act"]["recordId"],
        original["record"]["recordId"]
    );
    let next = crate::file_act_open_arrival_result(&state, &run, &arrival).unwrap();
    assert_eq!(next["utf8"], "v2");
    assert_eq!(
        next["offer"]["subject"]["contentIdentity"]["value"],
        lapse["body"]["c1"]["value"]
    );
    assert_ne!(
        next["offer"]["subject"]["contentIdentity"],
        first["offer"]["subject"]["contentIdentity"]
    );
    let second = confirm(&state, next["reference"].as_str().unwrap(), "act");
    owned.lock().unwrap().observe_checkpoints(&view);
    assert!(rs_for(&peer, &run)
        .iter()
        .any(|e| e["kind"] == "act_counted"
            && e["body"]["act"]["recordId"] == second["record"]["recordId"]));
    let read = crate::file_act_view::read(&peer.fixture.root);
    let old = read["rows"]
        .as_array()
        .unwrap()
        .iter()
        .find(|row| row["recordId"] == original["record"]["recordId"])
        .unwrap();
    assert!(old["lapseHistoryClaims"]
        .as_array()
        .unwrap()
        .iter()
        .any(|claim| claim["record"]["recordId"] == lapse["recordId"]));
    std::fs::remove_file(peer.fixture.root.join("out/summary.md")).unwrap();
    owned.lock().unwrap().observe_checkpoints(&view);
    assert!(rs_for(&peer, &run)
        .iter()
        .any(|e| e["kind"] == "act_lapsed" && e["body"]["state"] == "lapsed (subject absent)"));
    assert!(
        crate::file_act_open_arrival_result(&state, &run, &arrival).is_err(),
        "absent effective content does not acquire a new contextual act"
    );
}

#[test]
fn file_act_arrival_decline_and_cancel_remain_distinct() {
    for choice in ["decline", "cancel"] {
        let (peer, state, run, arrival) = fixture("A6");
        let preview = crate::file_act_open_arrival_result(&state, &run, &arrival).unwrap();
        let result = confirm(&state, preview["reference"].as_str().unwrap(), choice);
        if choice == "cancel" {
            assert!(acts(&peer).is_empty());
            assert_eq!(result["state"], "dismissed; nothing captured");
        } else {
            assert_eq!(result["record"]["kind"], "act_declined");
            assert_eq!(result["record"]["runId"], run);
            assert_eq!(
                result["record"]["body"]["arrival"],
                preview["offer"]["answers"]["arrival"]
            );
            assert!(crate::file_act_view::corresponds(
                &result["capture"],
                &result["record"]
            ));
            state.workflows.lock().unwrap().runs[&run]
                .lock()
                .unwrap()
                .observe_checkpoints(&recorder_view(&peer, &summary_items()[1..]));
            assert!(rs_for(&peer, &run)
                .iter()
                .any(|e| e["kind"] == "arrival_declined"));
            assert!(rs_for(&peer, &run)
                .iter()
                .all(|e| e["kind"] != "act_counted"));
        }
    }
}

#[test]
fn file_act_arrival_refuses_unowned_unwritten_ambiguous_and_unsupported_sources() {
    for mode in [
        "forged identity",
        "unwritten",
        "duplicate coordinate",
        "duplicate opening",
        "corrected",
        "copied log",
        "foreign home",
        "foreign project",
        "cold run",
        "message output",
        "not obtainable",
        "stale content",
        "extra lapse",
    ] {
        let (peer, mut state, run, mut arrival) =
            fixture_with("A4", "out/summary.md", mode != "not obtainable");
        let source = crate::records::supply::run_log(&peer.fixture.root, &run).unwrap();
        let owned = state.workflows.lock().unwrap().runs[&run].clone();
        let mut extra_root = None;
        match mode {
            "forged identity" => arrival = "rec:invented:not-an-arrival".into(),
            "unwritten" => {
                owned
                    .lock()
                    .unwrap()
                    .entries
                    .iter_mut()
                    .find(|e| e.record_id == arrival)
                    .unwrap()
                    .written = None
            }
            "duplicate coordinate" | "corrected" => {
                let mut extra = rs_for(&peer, &run)
                    .into_iter()
                    .find(|e| e["recordId"] == arrival)
                    .unwrap();
                extra["recordId"] = json!(crate::util::opaque_id("rec:synthetic:").unwrap());
                if mode == "corrected" {
                    extra["corrects"] = json!(arrival);
                    extra["correctionReason"] = json!("Synthetic correction");
                }
                append_raw(&source, extra);
            }
            "duplicate opening" => {
                let mut extra = rs_for(&peer, &run)
                    .into_iter()
                    .find(|e| e["kind"] == "run_opened")
                    .unwrap();
                extra["recordId"] = json!(crate::util::opaque_id("rec:synthetic:").unwrap());
                append_raw(&source, extra);
            }
            "copied log" => {
                let copy =
                    crate::storage::project_log(&peer.fixture.root, Some(&run), "synthetic-copy")
                        .unwrap();
                std::fs::copy(&source, copy).unwrap();
            }
            "foreign home" => {
                *state.homes.lock().unwrap() = HomeRouter::new(Arc::new(
                    HomeSession::new(
                        crate::home_resources::HomeClass::Account,
                        Arc::new(crate::hosting::Host::new()),
                        Err("synthetic absent home".into()),
                    )
                    .unwrap(),
                ))
                .unwrap()
            }
            "foreign project" => {
                let path = peer.fixture.root.join("other-project");
                std::fs::create_dir(&path).unwrap();
                state.workspace = Some(path.clone());
                extra_root = Some(path);
            }
            "cold run" => {
                state.workflows.lock().unwrap().runs.remove(&run);
            }
            "message output" => {
                owned
                    .lock()
                    .unwrap()
                    .observe_checkpoints(&recorder_view(&peer, &summary_items()));
                arrival = rs_for(&peer, &run)
                    .into_iter()
                    .find(|e| {
                        e["kind"] == "checkpoint_arrival" && e["body"]["checkpoint"] == "CP-check"
                    })
                    .unwrap()["recordId"]
                    .as_str()
                    .unwrap()
                    .into();
            }
            "stale content" => std::fs::write(
                peer.fixture.root.join("out/summary.md"),
                b"changed after arrival",
            )
            .unwrap(),
            "extra lapse" => {
                let act = json!({"recordId":"rec:synthetic:missing-act","actKind":"A4","capturedAt":"2026-10-18T00:00:00.000Z","capturingSurface":"app_act_control"});
                crate::records::append_project(&peer.fixture.root,Some(&run),crate::records::supply::LIVE_WRITER,"act_lapsed",&crate::records::APP_WRITER,json!({"act":act,"state":"lapsed","referents":["invented"],"c0":{"method":crate::util::FILE_IDENTITY_METHOD,"value":"old"},"c1":{"method":crate::util::FILE_IDENTITY_METHOD,"value":"new"},"time":"2026-10-18T00:00:00.000Z","arrival":{"checkpoint":"CP-rely","arrivalOrdinal":1},"when":"after resume"})).unwrap();
            }
            _ => {}
        }
        let before = crate::storage::read_all(&peer.fixture.root);
        assert!(
            crate::file_act_open_arrival_result(&state, &run, &arrival).is_err(),
            "{mode}"
        );
        assert_eq!(
            crate::storage::read_all(&peer.fixture.root),
            before,
            "{mode}: opening performs no capture or recording"
        );
        assert!(
            state.file_acts.lock().unwrap().offers.is_empty(),
            "{mode}: no standing fallback offer"
        );
        drop(extra_root);
    }
}

#[test]
fn file_act_arrival_rechecks_actor_content_and_source_on_native_return() {
    for mode in ["actor", "content", "corrected source", "run ended"] {
        let (peer, state, run, arrival) = fixture("A7");
        let preview = crate::file_act_open_arrival_result(&state, &run, &arrival).unwrap();
        let result = crate::file_act_confirm_original(
            &state,
            preview["reference"].as_str().unwrap(),
            |control, offer, observe| {
                control.synthetic_file_native(offer, observe, |_, kind| {
                    match mode {
                        "actor" => {
                            *state.person_name.lock().unwrap() =
                                Some("different synthetic actor".into())
                        }
                        "content" => std::fs::write(
                            peer.fixture.root.join("out/summary.md"),
                            b"changed during native confirmation",
                        )
                        .unwrap(),
                        "corrected source" => {
                            let mut extra = rs_for(&peer, &run)
                                .into_iter()
                                .find(|e| e["recordId"] == arrival)
                                .unwrap();
                            extra["recordId"] =
                                json!(crate::util::opaque_id("rec:synthetic:").unwrap());
                            extra["corrects"] = json!(arrival);
                            extra["correctionReason"] =
                                json!("Synthetic correction during confirmation");
                            append_raw(
                                &crate::records::supply::run_log(&peer.fixture.root, &run).unwrap(),
                                extra,
                            );
                        }
                        _ => {
                            state.workflows.lock().unwrap().runs[&run]
                                .lock()
                                .unwrap()
                                .end_run(None, None)
                                .unwrap();
                        }
                    }
                    MessageDialogResult::Custom(kind.wording().into())
                })
            },
        )
        .unwrap();
        assert_eq!(result["state"],"native attempt returned an error; capture/record standing not established by this result","{mode}: {result}");
        assert!(acts(&peer).is_empty(), "{mode}");
    }
}

#[test]
fn file_act_arrival_changed_between_source_read_and_frozen_preview_creates_no_offer() {
    let (peer, state, run, arrival) = fixture("A4");
    crate::act_control::before_file_open_for_test(|path| {
        std::fs::write(path, b"changed exactly at compose read").unwrap()
    });
    let result = crate::file_act_open_arrival_result(&state, &run, &arrival);
    assert!(result.is_err(), "{result:?}");
    assert!(state.file_acts.lock().unwrap().offers.is_empty());
    assert!(acts(&peer).is_empty());
}

#[test]
fn file_act_arrival_record_correspondence_rejects_injected_links() {
    let (peer, state, run, arrival) = fixture("A4");
    let preview = crate::file_act_open_arrival_result(&state, &run, &arrival).unwrap();
    let result = confirm(&state, preview["reference"].as_str().unwrap(), "act");
    for change in ["run", "arrival", "request"] {
        let mut record = result["record"].clone();
        match change {
            "run" => record["runId"] = json!("run:synthetic:foreign"),
            "arrival" => {
                record["body"]["relations"]["arrivalAnswered"]["arrivalOrdinal"] = json!(2)
            }
            _ => record["body"]["relations"]["requestRef"] = json!("rec:synthetic:invented"),
        }
        assert!(
            !crate::file_act_view::corresponds(&result["capture"], &record),
            "{change}"
        );
    }
    let mut standing = result["capture"].clone();
    standing["answers"] = json!({"standing":"no arrival: a standing act (RC-6)"});
    assert!(!crate::file_act_view::corresponds(
        &standing,
        &result["record"]
    ));
    assert_eq!(acts(&peer).len(), 1);
}

#[test]
fn file_act_arrival_pending_record_continues_original_metadata_after_end_and_releases_retention() {
    for choice in ["act", "cancel"] {
        let (peer, state, run, arrival) = fixture("A6");
        let preview = crate::file_act_open_arrival_result(&state, &run, &arrival).unwrap();
        let reference = preview["reference"].as_str().unwrap();
        let log = crate::storage::project_log(
            &peer.fixture.root,
            Some(&run),
            crate::records::APP_INTERFACE.identity,
        )
        .unwrap();
        if choice == "act" {
            crate::storage::fail_directory_for_test(Some(log.parent().unwrap().to_path_buf()));
        }
        let result = confirm(&state, reference, choice);
        crate::storage::fail_directory_for_test(None);
        let original = result["capture"].clone();
        if choice == "act" {
            assert_eq!(result["state"], "AC-8 record pending", "{result}");
        }
        state.workflows.lock().unwrap().runs[&run]
            .lock()
            .unwrap()
            .end_run(None, None)
            .unwrap();
        let wire = peer.wire().len();
        if choice == "act" {
            let actor = crate::act_control::person(Some("Synthetic fixture"), Some("synthetic-os"));
            let context = json!({"fixture":"pending native metadata retention negative"});
            let refusal = crate::records_retention::prepare(
                &peer.fixture.root,
                "close",
                None,
                &actor,
                &context,
            )
            .and_then(|plan| crate::records_retention::apply(plan, &actor, &context));
            assert!(
                refusal.unwrap_err().contains("activity"),
                "pending capture retains the existing explicit activity refusal"
            );
            std::fs::write(
                peer.fixture.root.join("out/summary.md"),
                b"new content after the actual act",
            )
            .unwrap();
            *state.person_name.lock().unwrap() = Some("today's different actor".into());
            let done = crate::file_act_continue_result(&state, reference).unwrap();
            assert_eq!(done["state"], "AC-7 recorded", "{done}");
            assert_eq!(done["capture"]["captureId"], original["captureId"]);
            assert_eq!(done["capture"]["actor"], original["actor"]);
            assert_eq!(done["capture"]["boundContent"], original["boundContent"]);
            assert_eq!(done["record"]["observedAt"], original["capturedAt"]);
            let entries = crate::records::read_log(&log).0;
            assert_eq!(
                entries.iter().filter(|e| e["kind"] == "human_act").count(),
                1
            );
            assert!(entries.iter().any(|e| e["kind"] == "evidence_limit"
                && e["body"]["label"] == "record write failed"
                && e["runId"] == run));
        }
        assert_eq!(
            peer.wire().len(),
            wire,
            "metadata continuation sends no native request"
        );
        let dir = crate::records_store::home(&peer.fixture.root)
            .unwrap()
            .attachment
            .dir
            .unwrap();
        let store = crate::records_store::store_root().unwrap();
        let gate = store
            .join("administration")
            .join(dir.file_name().unwrap())
            .join(".admission.lock");
        let lease = crate::storage::try_lock_exclusive(&gate).unwrap();
        assert!(
            lease.is_some(),
            "settled/dismissed retained preview owns no admission lease"
        );
        drop(lease);
        peer.home
            .host
            .stop_scoped(
                &peer.generation,
                "synthetic fixture",
                "end local synthetic peer before close",
            )
            .unwrap();
        let actor = crate::act_control::person(Some("Synthetic fixture"), Some("synthetic-os"));
        let context = json!({"fixture":"synthetic retention callback"});
        let plan =
            crate::records_retention::prepare(&peer.fixture.root, "close", None, &actor, &context)
                .unwrap();
        crate::records_retention::apply(plan, &actor, &context).unwrap();
        assert!(
            state.file_acts.lock().unwrap().get(reference).is_ok(),
            "display offer retained without holding admission"
        );
    }
}

#[test]
fn file_act_arrival_metadata_retry_refuses_replacement_and_foreign_record_routes() {
    metadata_retry_refuses(&[
        "target log replaced",
        "source log replaced",
        "project replaced",
        "store replaced",
        "copied standing record",
        "moved standing record",
        "wrong run",
        "foreign late disclosure",
    ]);
}
#[test]
fn file_act_arrival_metadata_receipt_requires_original_recorder_and_time(){
    metadata_retry_refuses(&["wrong recorder","wrong observedAt"]);
}
fn metadata_retry_refuses(modes:&[&str]){
    for mode in modes.iter().copied() {
        let store = std::fs::canonicalize(std::env::temp_dir())
            .unwrap()
            .join(crate::util::opaque_id("arrival-store-").unwrap());
        crate::records_store::use_store_for_test(Some(Ok(crate::records_store::Store {
            root: store.clone(),
            placement: crate::records_store::Placement::Test,
            limits: vec![],
        })));
        let (peer, state, run, arrival) = fixture("A4");
        let preview = crate::file_act_open_arrival_result(&state, &run, &arrival).unwrap();
        let reference = preview["reference"].as_str().unwrap();
        let target = crate::storage::project_log(
            &peer.fixture.root,
            Some(&run),
            crate::records::APP_INTERFACE.identity,
        )
        .unwrap();
        crate::storage::fail_directory_for_test(Some(target.parent().unwrap().to_path_buf()));
        let held = confirm(&state, reference, "act");
        crate::storage::fail_directory_for_test(None);
        assert_eq!(held["state"], "AC-8 record pending", "{mode}: {held}");
        assert!(target.exists());
        let source = crate::records::supply::run_log(&peer.fixture.root, &run).unwrap();
        let mut moved = None;
        match mode {
            "target log replaced" | "source log replaced" => {
                let path = if mode == "target log replaced" {
                    &target
                } else {
                    &source
                };
                let aside = path.with_extension("original");
                std::fs::rename(path, &aside).unwrap();
                std::fs::copy(&aside, path).unwrap();
            }
            "project replaced" => {
                let aside = peer.fixture.root.with_extension("original");
                std::fs::rename(&peer.fixture.root, &aside).unwrap();
                std::fs::create_dir(&peer.fixture.root).unwrap();
                std::fs::create_dir_all(
                    peer.fixture
                        .root
                        .join(crate::records_store::PROJECT_LINK)
                        .parent()
                        .unwrap(),
                )
                .unwrap();
                std::fs::copy(
                    aside.join(crate::records_store::PROJECT_LINK),
                    peer.fixture.root.join(crate::records_store::PROJECT_LINK),
                )
                .unwrap();
                moved = Some(aside);
            }
            "store replaced" => {
                let aside = store.with_extension("original");
                std::fs::rename(&store, &aside).unwrap();
                std::fs::create_dir(&store).unwrap();
                for e in std::fs::read_dir(&aside).unwrap() {
                    let e = e.unwrap();
                    std::fs::rename(e.path(), store.join(e.file_name())).unwrap();
                }
                moved = Some(aside);
            }
            "copied standing record" | "moved standing record" => {
                let standing =
                    crate::storage::project_file(&peer.fixture.root, crate::recorder::LOG).unwrap();
                crate::storage::ensure_directory(standing.parent().unwrap()).unwrap();
                if mode == "moved standing record" {
                    std::fs::rename(&target, standing).unwrap();
                } else {
                    std::fs::copy(&target, standing).unwrap();
                }
            }
            "wrong run" | "wrong recorder" | "wrong observedAt" => {
                let bytes = std::fs::read_to_string(&target).unwrap();
                let mut record: Value = serde_json::from_str(bytes.trim()).unwrap();
                match mode{
                    "wrong run"=>record["runId"] = json!("run:synthetic:foreign"),
                    "wrong recorder"=>record["recorder"]=json!({"role":"App writer","identity":"app-writer:local"}),
                    _=>record["observedAt"]=json!("2000-01-01T00:00:00.000Z"),
                }
                std::fs::write(&target, format!("{record}\n")).unwrap();
            }
            _ => {
                let record = crate::records::read_log(&target)
                    .0
                    .into_iter()
                    .find(|e| e["kind"] == "human_act")
                    .unwrap();
                crate::records::append_project(&peer.fixture.root,Some("run:synthetic:foreign"),"synthetic-foreign-writer","evidence_limit",&crate::records::APP_WRITER,json!({"label":"record write failed","subjectRef":record["recordId"],"detail":"invented foreign disclosure is not the original writer's disclosure"})).unwrap();
            }
        }
        let before = crate::file_act_view::source_claims(&peer.fixture.root).claims;
        let requests = peer.home.host.client_requests().len();
        let result = crate::file_act_continue_result(&state, reference);
        assert!(
            match &result {
                Err(_) => true,
                Ok(value) =>
                    value["state"] != "AC-7 recorded" || value["delayEvidencePending"] == true,
            },
            "{mode}: {result:?}"
        );
        assert_eq!(
            crate::file_act_view::source_claims(&peer.fixture.root).claims,
            before,
            "{mode}: retry must not append into relocated or conflicting sources"
        );
        assert_eq!(
            peer.home.host.client_requests().len(),
            requests,
            "{mode}: metadata retry never repeats native send"
        );
        drop(state);
        drop(peer);
        crate::records_store::use_store_for_test(None);
        if let Some(moved) = moved {
            std::fs::remove_dir_all(moved).unwrap();
        }
        std::fs::remove_dir_all(store).unwrap();
    }
}

/// Every path below `dir` with its bytes (folders: None), leaving out the
/// derived query cache a read may keep under the store's `indexes/`.
fn inventory(dir: &std::path::Path) -> std::collections::BTreeMap<std::path::PathBuf, Option<Vec<u8>>> {
    let mut out = std::collections::BTreeMap::new();
    let mut todo = vec![dir.to_path_buf()];
    while let Some(at) = todo.pop() {
        for entry in std::fs::read_dir(&at).unwrap() {
            let path = entry.unwrap().path();
            if path.strip_prefix(dir).is_ok_and(|rel| rel.starts_with("indexes")) { continue; }
            // A temporary file gone between listing and reading was not kept.
            let Ok(meta) = std::fs::symlink_metadata(&path) else { continue };
            if meta.is_dir() { out.insert(path.clone(), None); todo.push(path); }
            else if let Ok(bytes) = std::fs::read(&path) { out.insert(path.clone(), Some(bytes)); }
        }
    }
    out
}

#[test]
fn file_act_arrival_preview_finds_its_log_through_the_read_home_and_writes_nothing() {
    // The test's own store, so no other test's writer shares it.
    let own = std::fs::canonicalize(std::env::temp_dir()).unwrap().join(crate::util::opaque_id("arrival-preview-store-").unwrap());
    crate::records_store::use_store_for_test(Some(Ok(crate::records_store::Store { root: own.clone(), placement: crate::records_store::Placement::Test, limits: vec![] })));
    let (peer, state, run, arrival) = fixture("A7");
    let store = crate::records_store::store_root().unwrap();
    assert_eq!(store, own);
    // The writer made the store-wide lock when it minted the project's
    // identity. A preview, before the person has done anything, is a read:
    // it takes no writer admission and makes no lock again.
    let lock = store.join(".store.lock");
    if lock.exists() { std::fs::remove_file(&lock).unwrap(); }
    let (store_before, project_before) = (inventory(&store), inventory(&peer.fixture.root));
    let preview = crate::file_act_open_arrival_result(&state, &run, &arrival).unwrap();
    assert_eq!(preview["offer"]["actKind"], "A7", "{preview}");
    assert!(!lock.exists(), "the preview made the store-wide writer lock");
    assert_eq!(inventory(&store), store_before, "the preview wrote in the records store");
    assert_eq!(inventory(&peer.fixture.root), project_before, "the preview wrote in the project");
    // The log it found is the run's own owning log.
    assert_eq!(crate::records::supply::run_log_for_read(&peer.fixture.root, &run).unwrap(), crate::records::supply::run_log(&peer.fixture.root, &run).unwrap());
    drop(state);
    drop(peer);
    crate::records_store::use_store_for_test(None);
    let _ = std::fs::remove_dir_all(own);
}

fn entry_of(state: &crate::AppState, run: &str, arrival: &str) -> Value {
    state.workflows.lock().unwrap().runs[run].lock().unwrap().view(run)["fileActEntries"][arrival].clone()
}
fn confirm_plain(state: &crate::AppState, reference: &str) -> Result<Value, String> {
    crate::file_act_confirm_original(state, reference, |control, offer, observe| {
        control.synthetic_file_native(offer, observe, |_, kind| MessageDialogResult::Custom(kind.wording().into()))
    })
}

#[test]
fn file_act_arrival_is_offered_only_while_an_act_would_answer_it() {
    let (peer, state, run, arrival) = fixture("A7");
    // Permitted: a waiting arrival is offered.
    assert_eq!(entry_of(&state, &run, &arrival)["state"], "candidate");
    let answering = crate::file_act_open_arrival_result(&state, &run, &arrival).unwrap();
    let later = crate::file_act_open_arrival_result(&state, &run, &arrival).unwrap();
    assert_eq!(confirm(&state, answering["reference"].as_str().unwrap(), "act")["state"], "AC-7 recorded");
    // Its disposition changed through the real recorder: the offer is withdrawn, with the reason.
    state.workflows.lock().unwrap().runs[&run].lock().unwrap().observe_checkpoints(&recorder_view(&peer, &summary_items()[1..]));
    assert!(rs_for(&peer, &run).iter().any(|e| e["kind"] == "disposition_change" && e["body"]["disposition"] == "performed"));
    let withdrawn = entry_of(&state, &run, &arrival);
    assert_eq!((withdrawn["state"].as_str(), withdrawn["reason"].as_str()), (Some("unavailable"), Some(crate::checkpoint_recorder::not_answering::PERFORMED)));
    assert_eq!(crate::file_act_open_arrival_result(&state, &run, &arrival).unwrap_err(), crate::checkpoint_recorder::not_answering::PERFORMED);
    // An offer taken before the arrival was answered is refused at confirmation, before the person
    // is asked anything, and records nothing.
    let before = acts(&peer).len();
    let mut asked = false;
    let refused = crate::file_act_confirm_original(&state, later["reference"].as_str().unwrap(), |control, offer, observe| {
        control.synthetic_file_native(offer, observe, |_, kind| { asked = true; MessageDialogResult::Custom(kind.wording().into()) })
    }).unwrap();
    assert!(!asked, "the native question is never put");
    assert_eq!(refused["error"], crate::checkpoint_recorder::not_answering::PERFORMED, "{refused}");
    assert_eq!(acts(&peer).len(), before, "nothing recorded");
    // DEL-04-01: the same act on the same file stays the person's, outside the arrival, recorded as before.
    let home = state.homes.lock().unwrap().active();
    let (_, context) = crate::file_act_observe(&state, &home).unwrap();
    let path = peer.fixture.root.join("out/summary.md");
    let offer = {
        let mut control = state.act.lock().unwrap();
        state.file_acts.lock().unwrap().compose(control.as_mut().unwrap(), &path, crate::act_control::FileActKind::Rely, "The summary file.", "You decide to rely on the summary.", home, context).unwrap()
    };
    let recorded = confirm_plain(&state, offer["reference"].as_str().unwrap()).unwrap();
    assert_eq!(recorded["state"], "AC-7 recorded", "{recorded}");
    let after = acts(&peer);
    assert_eq!(after.len(), before + 1);
    let standing = after.iter().find(|e| e["body"]["captureEvidence"].as_array().is_some_and(|refs| refs.iter().any(|r| r["ref"] == recorded["capture"]["captureId"]))).unwrap();
    assert_eq!(standing["kind"], "human_act");
    assert!(standing["body"]["relations"]["arrivalAnswered"].is_null(), "a standing act, answering no arrival: {standing}");
}


#[test]
fn a_second_offer_on_an_arrival_already_answered_but_not_yet_taken_up_is_refused() {
    // found (reading of 347): two offers confirmed before the recorder's next observation both
    // recorded, though only the first could count.
    let (peer, state, run, arrival) = fixture("A7");
    let first = crate::file_act_open_arrival_result(&state, &run, &arrival).unwrap();
    let second = crate::file_act_open_arrival_result(&state, &run, &arrival).unwrap();
    assert_eq!(confirm(&state, first["reference"].as_str().unwrap(), "act")["state"], "AC-7 recorded");
    // Before the recorder observes: the second is refused before the native question, and a new
    // offer is not made.
    let before = acts(&peer).len();
    let mut asked = false;
    let refused = crate::file_act_confirm_original(&state, second["reference"].as_str().unwrap(), |control, offer, observe| {
        control.synthetic_file_native(offer, observe, |_, kind| { asked = true; MessageDialogResult::Custom(kind.wording().into()) })
    }).unwrap();
    assert!(!asked && refused["error"] == crate::checkpoint_recorder::not_answering::ANSWER_PENDING, "{refused}");
    assert_eq!(acts(&peer).len(), before, "nothing recorded");
    assert_eq!(crate::file_act_open_arrival_result(&state, &run, &arrival).unwrap_err(), crate::checkpoint_recorder::not_answering::ANSWER_PENDING);
    // Once taken up, the arrival reads performed, and the reason says that.
    state.workflows.lock().unwrap().runs[&run].lock().unwrap().observe_checkpoints(&recorder_view(&peer, &summary_items()[1..]));
    assert_eq!(rs_for(&peer, &run).iter().filter(|e| e["kind"] == "act_counted").count(), 1);
    assert_eq!(crate::file_act_open_arrival_result(&state, &run, &arrival).unwrap_err(), crate::checkpoint_recorder::not_answering::PERFORMED);
}

fn observe(state: &crate::AppState, peer: &Peer, run: &str) {
    state.workflows.lock().unwrap().runs[run].lock().unwrap().observe_checkpoints(&recorder_view(peer, &summary_items()[1..]));
}
/// A standing offer on the arrival's file, of `kind`, composed outside any arrival.
fn standing(state: &crate::AppState, peer: &Peer, kind: crate::act_control::FileActKind) -> String {
    let home = state.homes.lock().unwrap().active();
    let (_, context) = crate::file_act_observe(state, &home).unwrap();
    let mut control = state.act.lock().unwrap();
    state.file_acts.lock().unwrap().compose(control.as_mut().unwrap(), &peer.fixture.root.join("out/summary.md"), kind, "The summary file.", "You decide on the summary.", home, context).unwrap()["reference"].as_str().unwrap().to_owned()
}
/// A confirmation that records whether the native question was put, and what it said.
fn confirm_watching(state: &crate::AppState, reference: &str, choice: &str, asked: &mut Option<String>) -> Value {
    crate::file_act_confirm_original(state, reference, |control, offer, observe| {
        control.synthetic_file_native(offer, observe, |text, kind| {
            *asked = Some(text);
            MessageDialogResult::Custom(if choice == "act" { kind.wording().into() } else { "Decline this act".into() })
        })
    }).unwrap()
}
/// Every log and capture the App could write: the project and the records store, as bytes.
fn everything(peer: &Peer) -> (std::collections::BTreeMap<std::path::PathBuf, Option<Vec<u8>>>, std::collections::BTreeMap<std::path::PathBuf, Option<Vec<u8>>>) {
    (inventory(&peer.fixture.root), inventory(&crate::records_store::store_root().unwrap()))
}

// Condition 1 of App Agent 0 (347, round 2): the projection writes nothing, at an opening or at a
// refused confirmation.
#[test]
fn the_offers_projection_writes_nothing_at_an_opening_or_a_refused_confirmation() {
    let own = std::fs::canonicalize(std::env::temp_dir()).unwrap().join(crate::util::opaque_id("arrival-projection-store-").unwrap());
    crate::records_store::use_store_for_test(Some(Ok(crate::records_store::Store { root: own.clone(), placement: crate::records_store::Placement::Test, limits: vec![] })));
    let (peer, state, run, arrival) = fixture("A7");
    // The run's own memory: its entries as held, and its recorder's working state.
    let memory = || {
        let owned = state.workflows.lock().unwrap().runs[&run].clone();
        let run = owned.lock().unwrap();
        (run.entries.iter().map(|e| json!({"kind":e.kind,"body":e.body,"written":e.written,"refused":e.refused.is_some()})).collect::<Vec<_>>(), format!("{:?}", run.checkpoints))
    };
    let before = (everything(&peer), memory());
    let first = crate::file_act_open_arrival_result(&state, &run, &arrival).unwrap();
    let second = crate::file_act_open_arrival_result(&state, &run, &arrival).unwrap();
    assert_eq!((everything(&peer), memory()), before, "a permitted opening wrote or changed the run's memory");
    assert_eq!(confirm(&state, first["reference"].as_str().unwrap(), "act")["state"], "AC-7 recorded");
    let answered = (everything(&peer), memory());
    assert_eq!(crate::file_act_open_arrival_result(&state, &run, &arrival).unwrap_err(), crate::checkpoint_recorder::not_answering::ANSWER_PENDING);
    let mut asked = None;
    let refused = confirm_watching(&state, second["reference"].as_str().unwrap(), "act", &mut asked);
    assert!(asked.is_none() && refused["error"] == crate::checkpoint_recorder::not_answering::ANSWER_PENDING, "{refused}");
    assert_eq!((everything(&peer), memory()), answered, "a refused opening or confirmation wrote or changed the run's memory");
    drop(state);
    drop(peer);
    crate::records_store::use_store_for_test(None);
    let _ = std::fs::remove_dir_all(own);
}

// (e), reading of 347 round 2: a standing act on the same file revision, recorded before a
// contextual confirmation, holds the arrival until the recorder takes it up, and then the
// arrival reads performed: unavailable throughout, and only one act answers.
#[test]
fn a_standing_act_recorded_first_holds_the_arrival_until_taken_up_and_it_then_reads_performed() {
    use crate::checkpoint_recorder::not_answering::{ANSWER_PENDING, PERFORMED};
    let (peer, state, run, arrival) = fixture("A7");
    let contextual = crate::file_act_open_arrival_result(&state, &run, &arrival).unwrap();
    let rely = standing(&state, &peer, crate::act_control::FileActKind::Rely);
    assert_eq!(confirm_plain(&state, &rely).unwrap()["state"], "AC-7 recorded");
    assert_eq!(crate::file_act_open_arrival_result(&state, &run, &arrival).unwrap_err(), ANSWER_PENDING);
    let before = acts(&peer).len();
    let mut asked = None;
    let refused = confirm_watching(&state, contextual["reference"].as_str().unwrap(), "act", &mut asked);
    assert!(asked.is_none() && refused["error"] == ANSWER_PENDING, "{refused}");
    assert_eq!(acts(&peer).len(), before, "nothing recorded");
    observe(&state, &peer, &run);
    assert_eq!(rs_for(&peer, &run).iter().filter(|e| e["kind"] == "act_counted").count(), 1);
    assert_eq!(crate::file_act_open_arrival_result(&state, &run, &arrival).unwrap_err(), PERFORMED);
}

// (e), the hand-over inside a confirmation: while the contextual question is put, no other act
// can be recorded (the act owner is held from the first check to the write), and the recorder's
// observation then has nothing to take up; the contextual act records and is the one counted.
#[test]
fn no_act_is_recorded_between_a_contextual_confirmations_check_and_its_write() {
    let (peer, state, run, arrival) = fixture("A7");
    let contextual = crate::file_act_open_arrival_result(&state, &run, &arrival).unwrap();
    let rely = standing(&state, &peer, crate::act_control::FileActKind::Rely);
    let mut during = None;
    let recorded = crate::file_act_confirm_original(&state, contextual["reference"].as_str().unwrap(), |control, offer, check| {
        control.synthetic_file_native(offer, check, |_, kind| {
            during = Some(confirm_plain(&state, &rely));
            observe(&state, &peer, &run);
            MessageDialogResult::Custom(kind.wording().into())
        })
    }).unwrap();
    let during = during.unwrap();
    assert!(during.as_ref().is_err_and(|e| e.contains("Act owner busy")), "{during:?}");
    assert_eq!(recorded["state"], "AC-7 recorded", "{recorded}");
    observe(&state, &peer, &run);
    let counted: Vec<_> = rs_for(&peer, &run).into_iter().filter(|e| e["kind"] == "act_counted").collect();
    assert_eq!(counted.len(), 1);
    assert_eq!(counted[0]["body"]["act"]["recordId"], recorded["record"]["recordId"]);
}

/// A claim, in another run's log, to answer `run`'s arrival with an A7 on the file, citing
/// `capture` (its record body is the App's own for that capture, plus the arrival it claims).
fn claim_in_another_runs_log(peer: &Peer, state: &crate::AppState, run: &str, capture: &Value) {
    let second = peer.second_thread();
    let other = open_run(peer, &mut state.workflows.lock().unwrap(), &second);
    let log = crate::records::supply::run_log(&peer.fixture.root, &other).unwrap();
    let mut claim = rs_for(peer, &other).into_iter().last().unwrap();
    claim["kind"] = json!("human_act");
    claim["runId"] = json!(run);
    claim["recordId"] = json!(crate::util::opaque_id("rec:app:").unwrap());
    claim["recorder"] = json!({"role":crate::records::APP_INTERFACE.role,"identity":crate::records::APP_INTERFACE.identity});
    let mut body = crate::act_control::act_body(capture);
    body["relations"] = json!({"arrivalAnswered":{"checkpoint":"CP-rely","arrivalOrdinal":1}});
    claim["body"] = body;
    append_raw(&log, claim);
}
fn invented_capture(peer: &Peer) -> Value {
    let file = peer.fixture.root.join("out/summary.md");
    let content = json!({"method":crate::util::FILE_IDENTITY_METHOD,"value":crate::util::sha256_hex(b"v1")});
    crate::checkpoint_recorder::tests::capture_of("act", "A7", &file, &content, &crate::util::now_rfc3339())
}

// (b), reading of 347 round 2: a claim to answer the arrival, placed in another run's log, that
// differs from the capture it cites, is settled by the reader as no act, and holds nothing.
#[test]
fn an_invented_claim_in_another_runs_log_that_differs_from_its_capture_holds_nothing() {
    let (peer, state, run, arrival) = fixture("A7");
    let capture = invented_capture(&peer);
    crate::checkpoint_recorder::tests::store(&peer.fixture.root, &capture);
    claim_in_another_runs_log(&peer, &state, &run, &capture);
    let read = crate::checkpoint_recorder::project_act_records(&peer.fixture.root).unwrap();
    assert!(read.unresolved.iter().any(|u| u["reason"] == "the record differs from the capture it cites"), "{:?}", read.unresolved);
    let offered = crate::file_act_open_arrival_result(&state, &run, &arrival).unwrap();
    assert_eq!(confirm(&state, offered["reference"].as_str().unwrap(), "act")["state"], "AC-7 recorded");
}

// INTERLOCUTOR's condition 7 (347, round 2): a read that succeeded but could not settle a record
// on the arrival's file (here, its capture is not in the store) is not positively complete: the
// offer is refused with the not-read reason, at opening, and at the confirmation of an offer
// opened before the record was written, before the native question.
#[test]
fn a_record_on_the_file_that_the_reader_cannot_settle_withholds_the_offer_at_opening_and_confirmation() {
    use crate::checkpoint_recorder::not_answering::ACTS_NOT_READ;
    let (peer, state, run, arrival) = fixture("A7");
    let earlier = crate::file_act_open_arrival_result(&state, &run, &arrival).unwrap();
    claim_in_another_runs_log(&peer, &state, &run, &invented_capture(&peer));
    let read = crate::checkpoint_recorder::project_act_records(&peer.fixture.root).unwrap();
    assert!(read.unresolved.iter().any(|u| u["reason"].as_str().is_some_and(|r| r.starts_with("capture evidence not resolved"))), "{:?}", read.unresolved);
    assert_eq!(crate::file_act_open_arrival_result(&state, &run, &arrival).unwrap_err(), ACTS_NOT_READ);
    let before = acts(&peer).len();
    let mut asked = None;
    let refused = confirm_watching(&state, earlier["reference"].as_str().unwrap(), "act", &mut asked);
    assert!(asked.is_none() && refused["error"] == ACTS_NOT_READ, "{refused}");
    assert_eq!(acts(&peer).len(), before);
}

// (d), reading of 347 round 2, and App Agent 0's option 1: on a performed arrival answered again
// only by an act on its current content, the contextual sheet and preview say a decline would not
// answer; a decline pressed there is refused before any capture, and nothing is written anywhere;
// the act is offered and counted; the standing decline of the same kind stays the person's.
#[test]
fn a_decline_that_would_not_answer_is_said_and_refused_and_the_act_and_the_standing_decline_stay() {
    use crate::checkpoint_recorder::not_answering::DECLINE_DOES_NOT_ANSWER;
    let own = std::fs::canonicalize(std::env::temp_dir()).unwrap().join(crate::util::opaque_id("arrival-decline-store-").unwrap());
    crate::records_store::use_store_for_test(Some(Ok(crate::records_store::Store { root: own.clone(), placement: crate::records_store::Placement::Test, limits: vec![] })));
    let (peer, state, run, arrival) = fixture("A7");
    let waiting = crate::file_act_open_arrival_result(&state, &run, &arrival).unwrap();
    assert!(waiting["declineNotice"].is_null(), "while it waits, a decline answers");
    let stale = crate::file_act_open_arrival_result(&state, &run, &arrival).unwrap();
    assert_eq!(confirm(&state, waiting["reference"].as_str().unwrap(), "act")["state"], "AC-7 recorded");
    observe(&state, &peer, &run);
    // The run's next action, started after the act, is its resume point; the file then changes,
    // so the lapse is after resume (RC-8) and the arrival stays performed.
    let mut resumed = recorder_view(&peer, &[summary_items()[1].clone(), json!({"id":"c1","type":"commandExecution","source":"agent","command":"ls","status":"inProgress"})]);
    let later = std::time::SystemTime::now().duration_since(std::time::UNIX_EPOCH).unwrap().as_millis() as i64 + 60_000;
    resumed["items"][2]["sourceFrame"] = json!({"method":"item/started","params":{"startedAtMs":later}});
    let owned = state.workflows.lock().unwrap().runs[&run].clone();
    owned.lock().unwrap().observe_checkpoints(&resumed);
    std::fs::write(peer.fixture.root.join("out/summary.md"), b"v2").unwrap();
    owned.lock().unwrap().observe_checkpoints(&resumed);
    assert!(rs_for(&peer, &run).iter().any(|e| e["kind"] == "act_lapsed" && e["body"]["when"] == "after resume"), "{:#?}", rs_for(&peer, &run));
    let relapsed = crate::file_act_open_arrival_result(&state, &run, &arrival).unwrap();
    assert_eq!(relapsed["declineNotice"], DECLINE_DOES_NOT_ANSWER);
    let held = state.file_acts.lock().unwrap().snapshot();
    assert!(held.as_array().unwrap().iter().any(|o| o["reference"] == relapsed["reference"] && o["declineNotice"] == DECLINE_DOES_NOT_ANSWER), "{held}");
    let before = everything(&peer);
    let mut asked = None;
    let refused = confirm_watching(&state, relapsed["reference"].as_str().unwrap(), "decline", &mut asked);
    assert!(asked.as_deref().is_some_and(|text| text.contains(DECLINE_DOES_NOT_ANSWER) && !text.contains("Decline records only")), "{asked:?}");
    assert_eq!(refused["error"], DECLINE_DOES_NOT_ANSWER, "{refused}");
    assert_eq!(everything(&peer), before, "nothing captured or recorded, in any log");
    // The restriction holds at confirmation too: an offer opened while the arrival waited, whose
    // decline would then have answered, is refused before its question once that has changed.
    let mut asked = None;
    let refused = confirm_watching(&state, stale["reference"].as_str().unwrap(), "decline", &mut asked);
    assert!(asked.is_none() && refused["error"].is_string(), "{refused}");
    assert_eq!(everything(&peer), before, "nothing captured or recorded, in any log");
    let again = crate::file_act_open_arrival_result(&state, &run, &arrival).unwrap();
    let act = confirm(&state, again["reference"].as_str().unwrap(), "act");
    assert_eq!(act["state"], "AC-7 recorded");
    owned.lock().unwrap().observe_checkpoints(&resumed);
    assert!(rs_for(&peer, &run).iter().any(|e| e["kind"] == "act_counted" && e["body"]["act"]["recordId"] == act["record"]["recordId"]));
    // DEL-04-01: the standing decline of the same kind on the same file, from the standing file
    // selection, records as before.
    let rely = standing(&state, &peer, crate::act_control::FileActKind::Rely);
    let mut asked = None;
    let declined = confirm_watching(&state, &rely, "decline", &mut asked);
    assert!(asked.as_deref().is_some_and(|text| text.contains("Decline records only a decline of this kind")), "{asked:?}");
    assert_eq!(declined["record"]["kind"], "act_declined", "{declined}");
    assert!(declined["record"]["body"]["arrival"].is_null());
    drop(state);
    drop(peer);
    crate::records_store::use_store_for_test(None);
    let _ = std::fs::remove_dir_all(own);
}
