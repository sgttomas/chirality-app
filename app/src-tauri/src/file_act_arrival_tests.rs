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

/// Confirms `reference` with its validations passing, then makes its record's append fail: an
/// invented folder occupies the writer log it would be appended to. The capture is then held.
fn confirm_holding(state: &crate::AppState, reference: &str, log: &std::path::Path) -> Value {
    assert!(!log.exists(), "the invented first-answer log is not yet present");
    std::fs::create_dir_all(log.parent().unwrap()).unwrap();
    let mut checks = 0;
    let held = crate::file_act_confirm_original(state, reference, |control, offer, check| {
        control.synthetic_file_native(offer, || {
            checks += 1;
            let result = check()?;
            if checks == 2 { std::fs::create_dir(log).unwrap(); }
            Ok(result)
        }, |_, kind| MessageDialogResult::Custom(kind.wording().into()))
    }).unwrap();
    held
}
fn captures(peer: &Peer) -> std::collections::BTreeMap<std::path::PathBuf, Option<Vec<u8>>> {
    crate::storage::capture_dir(&peer.fixture.root).ok().filter(|d| d.is_dir()).map(|d| inventory(&d)).unwrap_or_default()
}

// Third reading of 347, (a) and (e): an answer confirmed whose record is not yet written is no
// record the projection or the recorder can see, and the next recording writes it ahead of any
// new one. While the act owner holds one, contextual or standing, no contextual offer is opened,
// and an offer opened earlier is refused before its question, with nothing captured. Once its
// record is written, the arrival reads pending, then performed, and only one act answers it.
// The contextual case is also the new act's own failed append: no second offer follows it.
#[test]
fn an_answer_held_without_its_record_withholds_the_arrival_offer_until_its_record_is_written() {
    use crate::checkpoint_recorder::not_answering::{ANSWER_PENDING, EARLIER_CAPTURE_HELD, PERFORMED};
    for first_is_standing in [false, true] {
        let (peer, state, run, arrival) = fixture("A7");
        let earlier = crate::file_act_open_arrival_result(&state, &run, &arrival).unwrap();
        let (first, log) = if first_is_standing {
            (standing(&state, &peer, crate::act_control::FileActKind::Rely), crate::storage::project_file(&peer.fixture.root, crate::recorder::LOG).unwrap())
        } else {
            (crate::file_act_open_arrival_result(&state, &run, &arrival).unwrap()["reference"].as_str().unwrap().to_owned(),
             crate::storage::project_log(&peer.fixture.root, Some(&run), crate::records::APP_INTERFACE.identity).unwrap())
        };
        let held = confirm_holding(&state, &first, &log);
        assert_eq!(held["state"], "AC-8 record pending", "{held}");
        // While the cause stays, continuing does not clear the hold, and the standing act of the
        // same kind is still offered and captured, its record waiting behind the held one.
        assert_eq!(crate::file_act_continue_result(&state, &first).unwrap()["state"], "AC-8 record pending");
        let behind = standing(&state, &peer, crate::act_control::FileActKind::Rely);
        assert_eq!(confirm_plain(&state, &behind).unwrap()["state"], "AC-8 record pending");
        std::fs::remove_dir(&log).unwrap();
        assert!(acts(&peer).is_empty(), "the held answer has no record yet");
        assert_eq!(crate::file_act_open_arrival_result(&state, &run, &arrival).unwrap_err(), EARLIER_CAPTURE_HELD, "standing first: {first_is_standing}");
        let before = (acts(&peer).len(), captures(&peer));
        let mut asked = None;
        let refused = confirm_watching(&state, earlier["reference"].as_str().unwrap(), "act", &mut asked);
        assert!(asked.is_none() && refused["error"] == EARLIER_CAPTURE_HELD, "{refused}");
        assert_eq!((acts(&peer).len(), captures(&peer)), before, "nothing captured or recorded");
        // The cause gone, continuing the held record alone, with no new act, clears the hold; the
        // standing act behind it is written after it.
        assert_eq!(crate::file_act_continue_result(&state, &first).unwrap()["state"], "AC-7 recorded");
        assert!(!state.act.lock().unwrap().as_ref().unwrap().answer_held());
        assert_eq!(acts(&peer).len(), 2);
        assert_eq!(crate::file_act_open_arrival_result(&state, &run, &arrival).unwrap_err(), ANSWER_PENDING);
        observe(&state, &peer, &run);
        let counted: Vec<_> = rs_for(&peer, &run).into_iter().filter(|e| e["kind"] == "act_counted").collect();
        assert_eq!(counted.len(), 1);
        assert_eq!(crate::file_act_open_arrival_result(&state, &run, &arrival).unwrap_err(), PERFORMED);
    }
}

// The ground the held-answer check rests on (App Agent 0, round 3): a capture with no native
// custody and no matching record is never appended, not by a contextual act's flush and not by
// recovery (act_control.rs recover_capture_recording: without native custody it returns "record
// pending" with the origin hold, and only reconciles a record that already exists). So the check
// need not count such a capture. Were recovery ever to replay it, this test fails.
#[test]
fn a_capture_without_native_custody_or_record_is_never_appended_by_a_flush_or_by_recovery() {
    let (peer, state, run, arrival) = fixture("A7");
    let capture = invented_capture(&peer);
    crate::checkpoint_recorder::tests::store(&peer.fixture.root, &capture);
    let id = capture["captureId"].clone();
    let cited = || acts(&peer).iter().any(|e| e["body"]["captureEvidence"].as_array().is_some_and(|refs| refs.iter().any(|r| r["ref"] == id)));
    assert!(!state.act.lock().unwrap().as_ref().unwrap().answer_held(), "not held: no native custody");
    let offered = crate::file_act_open_arrival_result(&state, &run, &arrival).unwrap();
    let recorded = confirm(&state, offered["reference"].as_str().unwrap(), "act");
    assert_eq!(recorded["state"], "AC-7 recorded");
    assert!(!cited(), "a contextual act's flush appended a capture it had no custody of");
    // Recovery, as at start-up and by the explicit continuation.
    let status = crate::runtime_session::continue_decision_writer(&peer.fixture.root, state.act.lock().unwrap().as_mut(), "test");
    assert!(!cited(), "recovery appended a capture it had no custody of: {status}");
    assert!(status["captureRecovery"].as_array().unwrap().iter().any(|r| r["capture"]["captureId"] == id && r["state"] == "AC-8 record pending"), "{status}");
    observe(&state, &peer, &run);
    let counted: Vec<_> = rs_for(&peer, &run).into_iter().filter(|e| e["kind"] == "act_counted").collect();
    assert_eq!(counted.len(), 1);
    assert_eq!(counted[0]["body"]["act"]["recordId"], recorded["record"]["recordId"]);
}

/// Seals made on this thread find no key folder (as a signed build before keychain enrolment
/// finds none it may use): the act is captured and recorded unsealed, and is not counted.
struct NoSealKeys;
impl NoSealKeys {
    fn on() -> NoSealKeys {
        crate::capture_seal::set_folder_for_test(Some(None));
        NoSealKeys
    }
}
impl Drop for NoSealKeys {
    fn drop(&mut self) {
        crate::capture_seal::set_folder_for_test(None);
    }
}

// The settled no-seal verdict (347, before the landing): an act recorded on the arrival's file
// whose capture carries no seal can never count, so it holds nothing. The offer opens with no
// not-read sentence and a new act is offered. In this state that act is again captured unsealed
// and not counted, until the sealing and the telling units land; once seals can be made, the
// next act counts.
#[test]
fn an_act_recorded_unsealed_holds_nothing_and_the_offer_stays_open() {
    use crate::checkpoint_recorder::not_answering::PERFORMED;
    let (peer, state, run, arrival) = fixture("A7");
    {
        let _unsealed = NoSealKeys::on();
        let first = crate::file_act_open_arrival_result(&state, &run, &arrival).unwrap();
        let recorded = confirm(&state, first["reference"].as_str().unwrap(), "act");
        assert_eq!(recorded["state"], "AC-7 recorded", "{recorded}");
        assert!(recorded["capture"]["seal"].is_null() && recorded["capture"]["evidenceLimits"].to_string().contains("capture not sealed"), "{recorded}");
        observe(&state, &peer, &run);
        assert_eq!(rs_for(&peer, &run).iter().filter(|e| e["kind"] == "act_counted").count(), 0, "not counted");
        let read = crate::checkpoint_recorder::project_act_records(&peer.fixture.root).unwrap();
        assert!(read.unresolved.iter().any(|u| u["settled"] == true && u["record"]["recordId"] == recorded["record"]["recordId"]), "{:?}", read.unresolved);
        // The offer opens, with no not-read sentence, and a new act is offered.
        let again = crate::file_act_open_arrival_result(&state, &run, &arrival).unwrap();
        assert!(again["reference"].is_string(), "{again}");
        assert_eq!(confirm(&state, again["reference"].as_str().unwrap(), "act")["state"], "AC-7 recorded");
        observe(&state, &peer, &run);
        assert_eq!(rs_for(&peer, &run).iter().filter(|e| e["kind"] == "act_counted").count(), 0, "again not counted in this state");
    }
    // Seals can be made again: the next act through the offer counts.
    let sealed = crate::file_act_open_arrival_result(&state, &run, &arrival).unwrap();
    let counted = confirm(&state, sealed["reference"].as_str().unwrap(), "act");
    observe(&state, &peer, &run);
    let counts: Vec<_> = rs_for(&peer, &run).into_iter().filter(|e| e["kind"] == "act_counted").collect();
    assert_eq!(counts.len(), 1);
    assert_eq!(counts[0]["body"]["act"]["recordId"], counted["record"]["recordId"]);
    assert_eq!(crate::file_act_open_arrival_result(&state, &run, &arrival).unwrap_err(), PERFORMED);
}

// A true limit of the read still refuses: a sealed act on the arrival's file whose seal cannot be
// checked now (no key folder at reading) may be an answer, so the offer is withheld with the
// not-read reason, and opens once the seal can be checked (then as pending, since it answers).
#[test]
fn a_seal_that_cannot_be_checked_now_still_withholds_the_offer_with_its_reason() {
    use crate::checkpoint_recorder::not_answering::{ACTS_NOT_READ, ANSWER_PENDING};
    let (peer, state, run, arrival) = fixture("A7");
    let rely = standing(&state, &peer, crate::act_control::FileActKind::Rely);
    let recorded = confirm_plain(&state, &rely).unwrap();
    assert!(recorded["capture"]["seal"].is_object(), "sealed: {recorded}");
    {
        let _unchecked = NoSealKeys::on();
        let read = crate::checkpoint_recorder::project_act_records(&peer.fixture.root).unwrap();
        assert!(read.unresolved.iter().any(|u| u["settled"].is_null() && u["record"]["recordId"] == recorded["record"]["recordId"]), "{:?}", read.unresolved);
        assert_eq!(crate::file_act_open_arrival_result(&state, &run, &arrival).unwrap_err(), ACTS_NOT_READ);
    }
    assert_eq!(crate::file_act_open_arrival_result(&state, &run, &arrival).unwrap_err(), ANSWER_PENDING);
}

// ---- H2 (App Agent 0, criterion 4): after a relaunch, the reopened reading projects what an act
// already in the act records does to each arrival, by this file's own act-offer rule. ----

/// The reopened reading of `run` through the real reader and projection, counting its reads of the
/// project's act records: the run's row and its projections.
fn reopened_projection(peer: &Peer, run: &str, reads: &mut usize) -> (Value, Vec<Value>) {
    let records = crate::workflow_workspace::publication::ProjectRecords::open(&peer.fixture.root).unwrap();
    let root = records.root().to_path_buf();
    let view = crate::records::supply::read_project_runs(&records, &[])
        .view_reopened_with(crate::records::supply::REOPENED_RECORDS_BOUND, &root, &mut || { *reads += 1; crate::checkpoint_recorder::project_act_records(&root) });
    let row = view["runs"].as_array().unwrap().iter().find(|r| r["run"] == run).unwrap().clone();
    let projection = row["answerability"].as_array().cloned().unwrap_or_default();
    (row, projection)
}
/// The latest disposition the run's own records hold for arrival 1 of CP-rely.
fn latest_recorded(row: &Value) -> String {
    row["lifecycle"]["records"].as_array().unwrap().iter()
        .filter(|e| e["kind"] == "disposition_change" && e["body"]["arrival"] == json!({"checkpoint":"CP-rely","arrivalOrdinal":1}))
        .last().unwrap()["body"]["disposition"].as_str().unwrap().to_owned()
}
fn projected(projection: &[Value], run: &str, arrival: &str) -> Vec<(String, Option<String>)> {
    projection.iter()
        .filter(|p| p["run"] == run && p["arrival"] == json!({"checkpoint":"CP-rely","arrivalOrdinal":1}) && p["arrivalRecordId"] == arrival)
        .map(|p| (p["state"].as_str().unwrap().to_owned(), p["reason"].as_str().map(str::to_owned)))
        .collect()
}

// Regression 1: an act captured before the recorder's next observation, then a relaunch.
#[test]
fn reopened_an_act_captured_before_the_next_observation_is_awaiting_count_with_one_read_and_no_record_written() {
    let own = std::fs::canonicalize(std::env::temp_dir()).unwrap().join(crate::util::opaque_id("reopened-projection-store-").unwrap());
    crate::records_store::use_store_for_test(Some(Ok(crate::records_store::Store { root: own.clone(), placement: crate::records_store::Placement::Test, limits: vec![] })));
    let (peer, state, run, arrival) = fixture("A7");
    let mut reads = 0;
    let (row, before) = reopened_projection(&peer, &run, &mut reads);
    assert_eq!((reads, projected(&before, &run, &arrival)), (1, vec![("waiting".into(), None)]), "permitted: nothing on record answers it");
    assert_eq!(latest_recorded(&row), "waiting");
    let offer = crate::file_act_open_arrival_result(&state, &run, &arrival).unwrap();
    assert_eq!(confirm(&state, offer["reference"].as_str().unwrap(), "act")["state"], "AC-7 recorded");
    // No observation follows: the App quits here. A later process reads the project's records.
    let written = everything(&peer);
    let mut reads = 0;
    let (row, after) = reopened_projection(&peer, &run, &mut reads);
    assert_eq!(reads, 1, "one read of the project's act records");
    assert_eq!(projected(&after, &run, &arrival), vec![("awaiting count".into(), None)], "{after:?}");
    assert_eq!(latest_recorded(&row), "waiting", "the recorded disposition is carried unchanged beside the projection");
    assert!(!row["lifecycle"]["records"].as_array().unwrap().iter().any(|e| e["kind"] == "act_counted"), "nothing is made to look recorded");
    // Through the real reopen the App calls.
    let reopened = WorkflowRootSession::default().reopen(&peer.fixture.root, &[]).unwrap();
    let real = reopened["runs"].as_array().unwrap().iter().find(|r| r["run"] == run.as_str()).unwrap();
    assert_eq!(projected(real["answerability"].as_array().unwrap(), &run, &arrival), vec![("awaiting count".into(), None)]);
    assert_eq!(reopened["answerabilityStanding"], crate::records::supply::ANSWERABILITY_STANDING);
    assert_eq!(everything(&peer), written, "reading and projecting wrote no record: the project folder and the store are unchanged outside the store's derived query cache (indexes/)");
    drop(state);
    drop(peer);
    crate::records_store::use_store_for_test(None);
    let _ = std::fs::remove_dir_all(own);
}

// Regression 2: the recorder took the act up, but its "performed" entry could not be written
// before the App quit (CE-19: held in memory only).
#[test]
fn reopened_an_act_whose_performed_entry_was_never_written_is_awaiting_count() {
    use std::os::unix::fs::PermissionsExt;
    let (peer, state, run, arrival) = fixture("A7");
    let offer = crate::file_act_open_arrival_result(&state, &run, &arrival).unwrap();
    assert_eq!(confirm(&state, offer["reference"].as_str().unwrap(), "act")["state"], "AC-7 recorded");
    let log = crate::records::supply::run_log(&peer.fixture.root, &run).unwrap();
    let mode = std::fs::metadata(&log).unwrap().permissions().mode();
    std::fs::set_permissions(&log, std::fs::Permissions::from_mode(0o444)).unwrap();
    observe(&state, &peer, &run);
    let held = state.workflows.lock().unwrap().runs[&run].lock().unwrap().view(&run);
    assert!(held["lifecycle"]["records"].as_array().unwrap().iter().any(|e| e["kind"] == "disposition_change" && e["body"]["disposition"] == "performed" && e["written"] == false), "the performed entry is held, not written: {held}");
    let mut reads = 0;
    let (row, projection) = reopened_projection(&peer, &run, &mut reads);
    std::fs::set_permissions(&log, std::fs::Permissions::from_mode(mode)).unwrap();
    assert_eq!(latest_recorded(&row), "waiting", "the run's record still says waiting");
    assert_eq!((reads, projected(&projection, &run, &arrival)), (1, vec![("awaiting count".into(), None)]));
}

// Regression 3: a later recorded settlement decides; nothing is projected for it.
#[test]
fn reopened_a_later_recorded_settlement_is_not_projected_and_a_decline_on_record_is_awaiting_count_until_taken_up() {
    let (peer, state, run, arrival) = fixture("A7");
    let offer = crate::file_act_open_arrival_result(&state, &run, &arrival).unwrap();
    assert_eq!(confirm(&state, offer["reference"].as_str().unwrap(), "act")["state"], "AC-7 recorded");
    observe(&state, &peer, &run);
    let mut reads = 0;
    let (row, projection) = reopened_projection(&peer, &run, &mut reads);
    assert_eq!(latest_recorded(&row), "performed");
    assert_eq!(projected(&projection, &run, &arrival), vec![], "performed: the recorded disposition decides");
    // A decline answering the arrival: awaiting count before it is taken up, then resolved negatively.
    let (peer, state, run, arrival) = fixture("A7");
    let offer = crate::file_act_open_arrival_result(&state, &run, &arrival).unwrap();
    assert_eq!(confirm(&state, offer["reference"].as_str().unwrap(), "decline")["state"], "AC-7 recorded");
    let (_, pending) = reopened_projection(&peer, &run, &mut reads);
    assert_eq!(projected(&pending, &run, &arrival), vec![("awaiting count".into(), None)]);
    observe(&state, &peer, &run);
    let (row, settled) = reopened_projection(&peer, &run, &mut reads);
    assert_eq!(latest_recorded(&row), "resolved negatively");
    assert_eq!(projected(&settled, &run, &arrival), vec![]);
}

// Regression 4: act evidence on the arrival's file that the reader cannot settle.
#[test]
fn reopened_an_unsettled_record_on_the_arrivals_file_makes_it_unknown_never_waiting() {
    let (peer, state, run, arrival) = fixture("A7");
    claim_in_another_runs_log(&peer, &state, &run, &invented_capture(&peer));
    let mut reads = 0;
    let (row, projection) = reopened_projection(&peer, &run, &mut reads);
    assert_eq!(latest_recorded(&row), "waiting");
    assert_eq!((reads, projected(&projection, &run, &arrival)), (1, vec![("unknown".into(), Some(crate::records::supply::answerability_unknown::ACTS_NOT_SETTLED.into()))]));
}

// Regression 5: act records that cannot be read at all (an unreadable line in the act log, which
// also leaves the project's record set incomplete): every arrival is unknown, never waiting.
#[test]
fn reopened_unreadable_act_records_make_every_arrival_unknown_never_waiting() {
    let (peer, _state, run, arrival) = fixture("A7");
    let log = crate::storage::project_file(&peer.fixture.root, crate::recorder::LOG).unwrap();
    std::fs::create_dir_all(log.parent().unwrap()).unwrap();
    let bytes = std::fs::read(&log).unwrap_or_default();
    { let mut f = std::fs::OpenOptions::new().create(true).append(true).open(&log).unwrap(); std::io::Write::write_all(&mut f, b"{\"partial\":\n").unwrap(); }
    assert!(crate::checkpoint_recorder::project_act_records(&peer.fixture.root).is_err(), "the act records cannot be read");
    let mut reads = 0;
    let (row, projection) = reopened_projection(&peer, &run, &mut reads);
    std::fs::write(&log, bytes).unwrap();
    assert_eq!(reads, 1);
    assert_eq!(row["state"], "unknown", "the incomplete record set leaves the run's lifecycle unknown");
    let arrivals = row["lifecycle"]["records"].as_array().unwrap().iter().filter(|e| e["kind"] == "checkpoint_arrival").count();
    assert_eq!(projection.len(), arrivals, "every arrival of the run");
    assert!(projection.iter().all(|p| p["state"] == "unknown" && p["reason"].is_string()), "{projection:?}");
    assert_eq!(projected(&projection, &run, &arrival).len(), 1);
}

// ---- The act-record reader's derived query cache (App Agent 0's cache conditions for H2). The
// reopened projection uses the arrival act control's own reader unchanged: that reader may create or
// refresh its derived query cache under the bound records store's indexes/ folder, and reads the
// record sources directly where it cannot. No act, run or capture record is created or changed. ----

/// A test's own records store, created as the App creates its store at start.
fn own_store(prefix: &str) -> std::path::PathBuf {
    let own = std::fs::canonicalize(std::env::temp_dir()).unwrap().join(crate::util::opaque_id(prefix).unwrap());
    crate::records_store::use_store_for_test(Some(Ok(crate::records_store::Store { root: own.clone(), placement: crate::records_store::Placement::Test, limits: vec![] })));
    own
}
/// The query cache files in a store's indexes/ folder (none when it is not a folder).
fn cache_files(store: &std::path::Path) -> Vec<String> {
    std::fs::read_dir(store.join("indexes")).map(|d| d.map(|e| e.unwrap().file_name().to_string_lossy().into_owned()).collect()).unwrap_or_default()
}
/// Make the store's query cache unwritable: its indexes/ folder replaced by a plain file.
fn break_cache(store: &std::path::Path) {
    let _ = std::fs::remove_dir_all(store.join("indexes"));
    std::fs::write(store.join("indexes"), b"not a folder").unwrap();
}
fn mend_cache(store: &std::path::Path) {
    std::fs::remove_file(store.join("indexes")).unwrap();
}
fn cache_note(root: &std::path::Path) -> bool {
    crate::records_index::with_index(root, |ix| ix.notes()).iter().any(|n| n.starts_with("query cache not written"))
}

#[test]
fn reopened_with_the_query_cache_unwritable_the_record_sources_give_the_same_projection_as_a_healthy_cache() {
    let store = own_store("reopened-cache-unwritable-");
    let (peer, state, run, arrival) = fixture("A7");
    // The index the act-record reader uses is the one for the project's records root.
    let root = crate::workflow_workspace::publication::ProjectRecords::open(&peer.fixture.root).unwrap().root().to_path_buf();
    let mut reads = 0;
    // Waiting: no act on record answers it.
    let (healthy_row, healthy) = reopened_projection(&peer, &run, &mut reads);
    assert!(!cache_note(&root), "the cache is healthy");
    break_cache(&store);
    let records = everything(&peer);
    let (broken_row, broken) = reopened_projection(&peer, &run, &mut reads);
    assert!(cache_note(&root), "the existing note says the cache was not written");
    assert_eq!(cache_files(&store), Vec::<String>::new(), "no cache could be written");
    assert_eq!(projected(&broken, &run, &arrival), vec![("waiting".into(), None)]);
    assert_eq!((broken, broken_row["lifecycle"].clone()), (healthy, healthy_row["lifecycle"].clone()), "the same result as with a healthy cache");
    assert_eq!(everything(&peer), records, "no record created or changed");
    // An answering act on record, not yet counted: the same result either way.
    mend_cache(&store);
    let offer = crate::file_act_open_arrival_result(&state, &run, &arrival).unwrap();
    assert_eq!(confirm(&state, offer["reference"].as_str().unwrap(), "act")["state"], "AC-7 recorded");
    let (healthy_row, healthy) = reopened_projection(&peer, &run, &mut reads);
    assert!(!cache_note(&root));
    assert_eq!(projected(&healthy, &run, &arrival), vec![("awaiting count".into(), None)]);
    break_cache(&store);
    let records = everything(&peer);
    let (broken_row, broken) = reopened_projection(&peer, &run, &mut reads);
    assert!(cache_note(&root));
    assert_eq!((broken, broken_row["lifecycle"].clone()), (healthy, healthy_row["lifecycle"].clone()));
    assert_eq!(everything(&peer), records, "no record created or changed");
    // The reopen the App calls does not fail on it, and the view says nothing new about the cache.
    let reopened = WorkflowRootSession::default().reopen(&peer.fixture.root, &[]).unwrap();
    assert!(!reopened.to_string().contains("query cache"), "no new cache status in the reopened view");
    drop(state);
    drop(peer);
    crate::records_store::use_store_for_test(None);
    let _ = std::fs::remove_file(store.join("indexes"));
    let _ = std::fs::remove_dir_all(store);
}

#[test]
fn reopened_a_cold_query_cache_is_created_only_in_the_bound_stores_indexes_and_no_record_changes() {
    let store = own_store("reopened-cache-cold-");
    let (peer, _state, run, arrival) = fixture("A7");
    let root = peer.fixture.root.clone();
    // Cold: no cache file exists for this reading to use.
    std::fs::remove_dir_all(store.join("indexes")).unwrap();
    let project = inventory(&root);
    let store_records = inventory(&store);
    let mut reads = 0;
    let (_, projection) = reopened_projection(&peer, &run, &mut reads);
    assert_eq!((reads, projected(&projection, &run, &arrival)), (1, vec![("waiting".into(), None)]));
    let made = cache_files(&store);
    assert!(!made.is_empty() && made.iter().all(|n| n.starts_with("query-") && n.ends_with(".sqlite")), "{made:?}");
    assert_eq!(inventory(&root), project, "nothing created or changed in the project folder");
    assert!(!walk(&root).iter().any(|p| p.extension().is_some_and(|e| e == "sqlite")), "no cache in the project folder");
    assert_eq!(inventory(&store), store_records, "outside indexes/, the store is unchanged");
    drop(peer);
    crate::records_store::use_store_for_test(None);
    let _ = std::fs::remove_dir_all(store);
}
fn walk(dir: &std::path::Path) -> Vec<std::path::PathBuf> {
    let mut out = Vec::new();
    let mut todo = vec![dir.to_path_buf()];
    while let Some(at) = todo.pop() {
        for entry in std::fs::read_dir(&at).unwrap() {
            let path = entry.unwrap().path();
            if std::fs::symlink_metadata(&path).unwrap().is_dir() { todo.push(path.clone()); }
            out.push(path);
        }
    }
    out
}

#[test]
fn reopened_with_no_admitted_store_no_cache_is_written_anywhere_and_the_arrival_is_unknown_never_waiting() {
    let store = own_store("reopened-cache-admitted-");
    let (peer, _state, run, arrival) = fixture("A7");
    let project = peer.fixture.root.clone();
    // The reading as the reopen takes it while the store is admitted: the project's records live in it.
    let records = crate::workflow_workspace::publication::ProjectRecords::open(&project).unwrap();
    let root = records.root().to_path_buf();
    let reading = crate::records::supply::read_project_runs(&records, &[]);
    let project_ = |reads: &mut usize| reading.view_reopened_with(crate::records::supply::REOPENED_RECORDS_BOUND, &root, &mut || { *reads += 1; crate::checkpoint_recorder::project_act_records(&root) });
    let mut reads = 0;
    let admitted = project_(&mut reads)["runs"].clone();
    let row = admitted.as_array().unwrap().iter().find(|r| r["run"] == run.as_str()).unwrap();
    assert_eq!(projected(row["answerability"].as_array().unwrap(), &run, &arrival), vec![("waiting".into(), None)]);
    // The configured store is now a folder that is not a records store (it holds no store identity),
    // and the cache the index held is gone, so the act-record reader must open one again.
    let plain = std::fs::canonicalize(std::env::temp_dir()).unwrap().join(crate::util::opaque_id("reopened-not-a-store-").unwrap());
    std::fs::create_dir(&plain).unwrap();
    crate::records_store::use_store_not_started_for_test(Some(Ok(crate::records_store::Store { root: plain.clone(), placement: crate::records_store::Placement::Test, limits: vec![] })));
    std::fs::remove_dir_all(store.join("indexes")).unwrap();
    let in_project = inventory(&project);
    let in_store = inventory(&store);
    // Without an admitted store the record sources it keeps cannot be discovered either: the act
    // records are not read, so the arrival is unknown with that reason, never waiting.
    let unknown = |runs: &Value| { let row = runs.as_array().unwrap().iter().find(|r| r["run"] == run.as_str()).unwrap();
        let mine = projected(row["answerability"].as_array().unwrap(), &run, &arrival);
        assert_eq!(mine.len(), 1, "{mine:?}");
        assert_eq!(mine[0].0, "unknown", "{mine:?}");
        assert!(mine[0].1.as_deref().is_some_and(|r| r.starts_with("the project's act records could not be read: ")), "{mine:?}"); };
    unknown(&project_(&mut reads)["runs"]);
    assert_eq!(std::fs::read_dir(&plain).unwrap().count(), 0, "nothing is written in a folder that is not an admitted store");
    assert!(!store.join("indexes").exists(), "nor in the store this process no longer has admitted");
    assert_eq!(inventory(&store), in_store, "whose records are unchanged");
    assert_eq!(inventory(&project), in_project, "nor in the project folder");
    assert!(!walk(&project).iter().any(|p| p.extension().is_some_and(|e| e == "sqlite")));
    // A configured store that does not exist is not created by the reading.
    let absent = plain.join("absent-store");
    crate::records_store::use_store_not_started_for_test(Some(Ok(crate::records_store::Store { root: absent.clone(), placement: crate::records_store::Placement::Test, limits: vec![] })));
    unknown(&project_(&mut reads)["runs"]);
    assert!(!absent.exists(), "a read creates no store");
    assert!(!store.join("indexes").exists());
    assert_eq!(reads, 3, "one read of the act records for each reading");
    drop(peer);
    crate::records_store::use_store_for_test(None);
    let _ = std::fs::remove_dir_all(plain);
    let _ = std::fs::remove_dir_all(store);
}

#[test]
fn reopened_a_failed_source_scan_with_the_cache_unwritable_is_unknown_never_waiting() {
    use std::os::unix::fs::PermissionsExt;
    let store = own_store("reopened-cache-scan-failed-");
    let (peer, state, run, arrival) = fixture("A7");
    let offer = crate::file_act_open_arrival_result(&state, &run, &arrival).unwrap();
    assert_eq!(confirm(&state, offer["reference"].as_str().unwrap(), "act")["state"], "AC-7 recorded");
    break_cache(&store);
    // The record source that holds the act, among the sources the act-record reader discovers.
    let records = crate::workflow_workspace::publication::ProjectRecords::open(&peer.fixture.root).unwrap();
    let root = records.root().to_path_buf();
    let held: Vec<_> = crate::records_index::with_index(&root, |ix| ix.paths()).into_iter().filter(|p| std::fs::read(p).is_ok_and(|b| b.windows(11).any(|w| w == b"\"human_act\""))).collect();
    assert_eq!(held.len(), 1, "{held:?}");
    let log = held[0].clone();
    let mode = std::fs::metadata(&log).unwrap().permissions().mode();
    std::fs::set_permissions(&log, std::fs::Permissions::from_mode(0o000)).unwrap();
    let read = crate::checkpoint_recorder::project_act_records(&root);
    let mut reads = 0;
    let (_, projection) = reopened_projection(&peer, &run, &mut reads);
    assert!(read.as_ref().is_err_and(|e| e.contains("incomplete record")), "the act records' source cannot be scanned: {:?}", read.as_ref().err());
    std::fs::set_permissions(&log, std::fs::Permissions::from_mode(mode)).unwrap();
    assert!(cache_note(&root), "the cache could not be written, so the sources were scanned");
    assert_eq!(reads, 1);
    let mine = projected(&projection, &run, &arrival);
    assert_eq!(mine.len(), 1, "{projection:?}");
    assert_eq!(mine[0].0, "unknown", "never waiting and never answered: {projection:?}");
    assert!(mine[0].1.as_deref().is_some_and(|r| !r.is_empty()), "with its reason");
    assert!(projection.iter().all(|p| p["state"] == "unknown"));
    drop(state);
    drop(peer);
    crate::records_store::use_store_for_test(None);
    let _ = std::fs::remove_file(store.join("indexes"));
    let _ = std::fs::remove_dir_all(store);
}
