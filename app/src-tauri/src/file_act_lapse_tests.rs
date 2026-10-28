//! Local synthetic native capture -> real standalone observer/writer/reader.
//! No supplier, real person, native authenticity or professional standing witness.
use super::*;
use std::{io::Write, os::unix::fs::symlink, path::Path};
use tauri_plugin_dialog::MessageDialogResult;
const C0: &[u8] = b"original reviewed bytes";
fn captured(kind: act_control::FileActKind, choice: &str) -> (PathBuf, AppState, Value) {
    let (root, state, home, _, _, _) = workflow_root_context_tests::fixture();
    std::fs::write(root.join("output.txt"), C0).unwrap();
    let (_, context) = file_act_observe(&state, &home).unwrap();
    let preview = state
        .file_acts
        .lock()
        .unwrap()
        .compose(
            state.act.lock().unwrap().as_mut().unwrap(),
            &root.join("output.txt"),
            kind,
            "one identified output",
            "synthetic explicit purpose",
            home,
            context,
        )
        .unwrap();
    let result = file_act_confirm_original(
        &state,
        preview["reference"].as_str().unwrap(),
        |control, offer, observe| {
            control.synthetic_file_native(offer, observe, |_, kind| {
                MessageDialogResult::Custom(
                    if choice == "act" {
                        kind.wording()
                    } else {
                        "Decline this act"
                    }
                    .into(),
                )
            })
        },
    )
    .unwrap();
    assert_eq!(result["state"], "AC-7 recorded", "{result}");
    let record = storage::read_all(&root)
        .0
        .into_iter()
        .find(|e| matches!(e["kind"].as_str(), Some("human_act" | "act_declined")))
        .unwrap();
    (root, state, record)
}
fn observe(state: &AppState) -> Value {
    file_act_lapse_result(state, false).unwrap()
}
fn retry(state: &AppState) -> Value {
    file_act_lapse_result(state, true).unwrap()
}
fn logs(root: &Path) -> Vec<Value> {
    let (e, l) = storage::read_all(root);
    assert!(l.is_empty(), "{l:?}");
    e
}
fn lapse_entries(root: &Path) -> Vec<Value> {
    logs(root)
        .into_iter()
        .filter(|e| e["kind"] == "act_lapsed")
        .collect()
}
fn fresh(state: &AppState, root: &Path) {
    *state.file_act_lapses.lock().unwrap() = Default::default();
    *state.file_acts.lock().unwrap() = Default::default();
    *state.act.lock().unwrap() = Some(ActControl::new(root));
}
fn append_raw(log: &Path, mut entry: Value) {
    let bytes = std::fs::read(log).unwrap();
    let last = bytes
        .split(|b| *b == b'\n')
        .filter(|b| !b.is_empty())
        .last()
        .unwrap();
    let sequence = records::read_log(log).0.last().unwrap()["seq"]
        .as_u64()
        .unwrap()
        + 1;
    entry["seq"] = json!(sequence);
    entry["prevLine"] = record_lines::link(Some(&record_lines::line_identity(last)));
    schema_validation::bundled()
        .unwrap()
        .validate(&entry)
        .unwrap();
    let mut file = std::fs::OpenOptions::new().append(true).open(log).unwrap();
    writeln!(file, "{entry}").unwrap();
    file.sync_all().unwrap();
}
#[test]
fn standalone_file_act_lapse_connected_and_cold_history_dto() {
    for kind in [
        act_control::FileActKind::Check,
        act_control::FileActKind::Approve,
        act_control::FileActKind::Rely,
    ] {
        let (root, state, act) = captured(kind, "act");
        assert!(observe(&state)["lapseObservation"]["recorded"]
            .as_array()
            .unwrap()
            .is_empty());
        let original = logs(&root);
        for (bytes, expected) in [
            (Some(b"changed".as_slice()), "lapsed"),
            (None, "lapsed (subject absent)"),
            (Some(C0), "matches c0 again after observed lapse"),
            (Some(b"changed again".as_slice()), "lapsed"),
            (Some(C0), "matches c0 again after observed lapse"),
        ] {
            match bytes {
                Some(bytes) => std::fs::write(root.join("output.txt"), bytes).unwrap(),
                None => std::fs::remove_file(root.join("output.txt")).unwrap(),
            }
            fresh(&state, &root);
            let view = observe(&state);
            let saved = &view["lapseObservation"]["recorded"];
            assert_eq!(saved.as_array().unwrap().len(), 1, "{view}");
            let entry = &saved[0];
            assert_eq!(entry["body"]["state"], expected);
            assert_eq!(entry["body"]["act"]["recordId"], act["recordId"]);
            assert_eq!(entry["body"]["c0"], act["body"]["boundContent"][0]);
            assert!(entry.get("runId").is_none());
            assert!(entry["body"].get("arrival").is_none());
            assert!(entry["body"].get("when").is_none());
            schema_validation::bundled()
                .unwrap()
                .validate(entry)
                .unwrap();
            let before =
                std::fs::read(storage::project_file(&root, recorder::LOG).unwrap()).unwrap();
            fresh(&state, &root);
            assert!(observe(&state)["lapseObservation"]["recorded"]
                .as_array()
                .unwrap()
                .is_empty());
            assert_eq!(
                std::fs::read(storage::project_file(&root, recorder::LOG).unwrap()).unwrap(),
                before,
                "fresh observer is idempotent"
            );
        }
        assert_eq!(lapse_entries(&root).len(), 5);
        assert_eq!(
            logs(&root)
                .into_iter()
                .filter(|e| e["kind"] == "human_act")
                .collect::<Vec<_>>(),
            original
                .into_iter()
                .filter(|e| e["kind"] == "human_act")
                .collect::<Vec<_>>()
        );
        let before = std::fs::read(storage::project_file(&root, recorder::LOG).unwrap()).unwrap();
        let cold = file_act_view::read(&root);
        assert_eq!(
            cold["rows"][0]["lapseHistoryClaims"]
                .as_array()
                .unwrap()
                .len(),
            5
        );
        assert!(cold["rows"][0]["comparison"]
            .as_str()
            .unwrap()
            .contains("matches c0 again"));
        assert_eq!(
            std::fs::read(storage::project_file(&root, recorder::LOG).unwrap()).unwrap(),
            before,
            "read-only view writes no observation"
        );
        if kind == act_control::FileActKind::Check {
            println!("FILE_ACT_LAPSE_DTO:{cold}");
        }
        drop(state);
        std::fs::remove_dir_all(root).unwrap();
    }
}
#[test]
fn standalone_file_act_lapse_pending_retry_keeps_original_metadata_dto() {
    let (root, state, act) = captured(act_control::FileActKind::Check, "act");
    let log = storage::project_file(&root, recorder::LOG).unwrap();
    std::fs::write(root.join("output.txt"), b"first observed change").unwrap();
    storage::fail_directory_for_test(Some(log.parent().unwrap().to_owned()));
    let pending = observe(&state);
    storage::fail_directory_for_test(None);
    assert!(pending["lapseObservation"]["recorded"]
        .as_array()
        .unwrap()
        .is_empty());
    let held = &pending["lapseObservation"]["pending"][0];
    assert_eq!(held["body"]["state"], "lapsed", "{pending}");
    println!("FILE_ACT_LAPSE_PENDING_DTO:{pending}");
    let id = held["recordId"].clone();
    let at = held["observedAt"].clone();
    let body = held["body"].clone();
    std::fs::write(root.join("output.txt"), C0).unwrap();
    let unobserved = observe(&state);
    assert_eq!(
        unobserved["lapseObservation"]["pending"][0]["body"], body,
        "new observe cannot replace held content"
    );
    let saved = retry(&state);
    assert!(
        saved["lapseObservation"]["pending"]
            .as_array()
            .unwrap()
            .is_empty(),
        "{saved}"
    );
    let written = &saved["lapseObservation"]["recorded"][0];
    assert_eq!(written["recordId"], id);
    assert_eq!(written["observedAt"], at);
    assert_eq!(written["body"], body);
    assert_eq!(written["body"]["act"]["recordId"], act["recordId"]);
    assert_eq!(
        lapse_entries(&root).len(),
        1,
        "uncertain landed write reconciles exactly once"
    );
    assert!(logs(&root).iter().any(|e| e["kind"] == "evidence_limit"
        && e["body"]["label"] == "record write failed"
        && e["body"]["subjectRef"] == id));
    assert_eq!(
        observe(&state)["lapseObservation"]["recorded"][0]["body"]["state"],
        "matches c0 again after observed lapse",
        "retry read no current content, separate observation records return"
    );
    assert!(retry(&state)["lapseObservation"]["recorded"]
        .as_array()
        .unwrap()
        .is_empty());
    drop(state);
    std::fs::remove_dir_all(root).unwrap();
}

#[test]
fn standalone_file_act_lapse_retry_reconciles_own_torn_tail_before_readmission() {
    for mode in [
        "fragment",
        "whole entry",
        "correction",
        "shared capture",
        "other log incomplete",
        "other log partial",
    ] {
        let (root, state, act) = captured(act_control::FileActKind::Check, "act");
        let log = storage::project_file(&root, recorder::LOG).unwrap();
        std::fs::write(root.join("output.txt"), b"original observed change").unwrap();
        storage::fail_directory_for_test(Some(log.parent().unwrap().to_owned()));
        let held = observe(&state);
        storage::fail_directory_for_test(None);
        let pending = &held["lapseObservation"]["pending"][0];
        assert!(pending["recordId"].is_string(), "{held}");
        let bytes = std::fs::read(&log).unwrap();
        let last_start = bytes[..bytes.len() - 1]
            .iter()
            .rposition(|b| *b == b'\n')
            .unwrap()
            + 1;
        match mode {
            "fragment" => std::fs::write(
                &log,
                &bytes[..last_start + (bytes.len() - 1 - last_start) / 2],
            )
            .unwrap(),
            "whole entry" => std::fs::write(&log, &bytes[..bytes.len() - 1]).unwrap(),
            "correction" | "shared capture" => {
                std::fs::write(&log, &bytes[..last_start]).unwrap();
                let mut extra = act.clone();
                extra["recordId"] = json!("rec:synthetic:recovered-tail");
                if mode == "correction" {
                    extra["corrects"] = act["recordId"].clone();
                    extra["correctionReason"] = json!("Synthetic recovered correction");
                }
                append_raw(&log, extra);
                let changed = std::fs::read(&log).unwrap();
                std::fs::write(&log, &changed[..changed.len() - 1]).unwrap();
            }
            _ => {
                let other = storage::project_log(&root, None, "synthetic-incomplete").unwrap();
                storage::ensure_directory(other.parent().unwrap()).unwrap();
                std::fs::write(
                    other,
                    if mode == "other log incomplete" {
                        b"not a record\n".as_slice()
                    } else {
                        b"not a record".as_slice()
                    },
                )
                .unwrap();
            }
        }
        std::fs::write(root.join("output.txt"), C0).unwrap();
        let before_retry = std::fs::read(&log).unwrap();
        let result = retry(&state);
        if matches!(mode, "fragment" | "whole entry") {
            assert!(
                result["lapseObservation"]["pending"]
                    .as_array()
                    .unwrap()
                    .is_empty(),
                "{mode}: {result}"
            );
            let saved = &result["lapseObservation"]["recorded"][0];
            assert_eq!(saved["recordId"], pending["recordId"], "{mode}");
            assert_eq!(saved["observedAt"], pending["observedAt"], "{mode}");
            assert_eq!(saved["body"], pending["body"], "{mode}");
            assert_eq!(
                lapse_entries(&root).len(),
                1,
                "{mode}: original event is reconciled exactly once"
            );
            let all = logs(&root);
            assert_eq!(
                all.iter()
                    .filter(|entry| entry["kind"] == "evidence_limit"
                        && entry["body"]["label"] == records::PARTIAL_NOT_RECOVERED)
                    .count(),
                usize::from(mode == "fragment")
            );
            assert!(all.iter().any(|entry| entry["kind"] == "evidence_limit"
                && entry["body"]["label"] == "record write failed"
                && entry["body"]["subjectRef"] == pending["recordId"]));
        } else {
            assert_eq!(
                result["lapseObservation"]["pending"][0]["body"], pending["body"],
                "{mode}"
            );
            assert!(
                result["lapseObservation"]["recorded"]
                    .as_array()
                    .unwrap()
                    .is_empty(),
                "{mode}: {result}"
            );
            if matches!(mode, "correction" | "shared capture") {
                assert!(
                    records::read_log_parts(&log).partial_tail.is_none(),
                    "own tail was recovered before final readmission"
                );
                assert!(
                    lapse_entries(&root).is_empty(),
                    "recovered act correction/shared capture refuses the held observation"
                );
            } else {
                assert_eq!(
                    std::fs::read(&log).unwrap(),
                    before_retry,
                    "{mode}: unrelated incompleteness is not bypassed"
                );
            }
        }
        drop(state);
        std::fs::remove_dir_all(root).unwrap();
    }
}

#[test]
fn standalone_file_act_lapse_cold_explicit_observe_recovers_own_tail_then_rechecks_sources() {
    for mode in ["fragment", "whole entry", "correction", "shared capture"] {
        let (root, state, act) = captured(act_control::FileActKind::Check, "act");
        let log = storage::project_file(&root, recorder::LOG).unwrap();
        std::fs::write(root.join("output.txt"), b"first observed change").unwrap();
        storage::fail_directory_for_test(Some(log.parent().unwrap().to_owned()));
        let held = observe(&state);
        storage::fail_directory_for_test(None);
        let original_id = held["lapseObservation"]["pending"][0]["recordId"].clone();
        let bytes = std::fs::read(&log).unwrap();
        let last_start = bytes[..bytes.len() - 1]
            .iter()
            .rposition(|b| *b == b'\n')
            .unwrap()
            + 1;
        match mode {
            "fragment" => std::fs::write(
                &log,
                &bytes[..last_start + (bytes.len() - 1 - last_start) / 2],
            )
            .unwrap(),
            "whole entry" => std::fs::write(&log, &bytes[..bytes.len() - 1]).unwrap(),
            _ => {
                std::fs::write(&log, &bytes[..last_start]).unwrap();
                let mut extra = act.clone();
                extra["recordId"] = json!("rec:synthetic:cold-recovered-tail");
                if mode == "correction" {
                    extra["corrects"] = act["recordId"].clone();
                    extra["correctionReason"] = json!("Synthetic cold recovered correction");
                }
                append_raw(&log, extra);
                let changed = std::fs::read(&log).unwrap();
                std::fs::write(&log, &changed[..changed.len() - 1]).unwrap();
            }
        }
        fresh(&state, &root);
        std::fs::write(
            root.join("output.txt"),
            if mode == "whole entry" {
                C0
            } else {
                b"later changed bytes"
            },
        )
        .unwrap();
        let before_read = std::fs::read(&log).unwrap();
        let read = file_act_view::read(&root);
        assert!(
            !read["limits"].as_array().unwrap().is_empty(),
            "{mode}: read exposes the tail limit"
        );
        assert_eq!(
            std::fs::read(&log).unwrap(),
            before_read,
            "read-only file acts never perform W-0 recovery"
        );
        let result = observe(&state);
        assert!(
            records::read_log_parts(&log).partial_tail.is_none(),
            "{mode}: explicit observation opens its own writer"
        );
        assert!(
            result["lapseObservation"]["pending"]
                .as_array()
                .unwrap()
                .is_empty(),
            "{mode}: {result}"
        );
        if matches!(mode, "fragment" | "whole entry") {
            let saved = &result["lapseObservation"]["recorded"][0];
            assert!(saved["recordId"].is_string(), "{mode}: {result}");
            assert_ne!(saved["recordId"], original_id, "cold explicit observation creates a new current observation, never replays lost memory");
            assert_eq!(
                saved["body"]["state"],
                if mode == "whole entry" {
                    "matches c0 again after observed lapse"
                } else {
                    "lapsed"
                }
            );
            assert_eq!(
                lapse_entries(&root).len(),
                if mode == "whole entry" { 2 } else { 1 }
            );
            let all = logs(&root);
            assert_eq!(
                all.iter()
                    .filter(|entry| entry["kind"] == "human_act")
                    .count(),
                1
            );
            assert_eq!(
                all.iter()
                    .filter(|entry| entry["kind"] == "evidence_limit"
                        && entry["body"]["label"] == records::PARTIAL_NOT_RECOVERED)
                    .count(),
                usize::from(mode == "fragment")
            );
        } else {
            assert!(
                result["lapseObservation"]["recorded"]
                    .as_array()
                    .unwrap()
                    .is_empty(),
                "{mode}: recovered sources are readmitted before observation"
            );
            assert!(lapse_entries(&root).is_empty());
        }
        drop(state);
        std::fs::remove_dir_all(root).unwrap();
    }
}
#[test]
fn standalone_file_act_lapse_unknown_alias_and_absence_are_distinct() {
    let (root, state, _) = captured(act_control::FileActKind::Check, "act");
    std::fs::write(root.join("other.txt"), b"other").unwrap();
    std::fs::remove_file(root.join("output.txt")).unwrap();
    symlink(root.join("other.txt"), root.join("output.txt")).unwrap();
    let unknown = observe(&state);
    assert_eq!(
        unknown["lapseObservation"]["recorded"][0]["body"]["state"], "unknown (unavailable)",
        "{unknown}"
    );
    fresh(&state, &root);
    assert!(observe(&state)["lapseObservation"]["recorded"]
        .as_array()
        .unwrap()
        .is_empty());
    assert!(file_act_view::read(&root)["rows"][0]["comparison"]
        .as_str()
        .unwrap()
        .contains("unknown"));
    std::fs::remove_file(root.join("output.txt")).unwrap();
    assert_eq!(
        observe(&state)["lapseObservation"]["recorded"][0]["body"]["state"],
        "lapsed (subject absent)"
    );
    std::fs::write(root.join("output.txt"), C0).unwrap();
    assert_eq!(
        observe(&state)["lapseObservation"]["recorded"][0]["body"]["state"],
        "matches c0 again after observed lapse"
    );
    assert_eq!(
        file_act_view::read(&root)["rows"][0]["lapseHistoryClaims"]
            .as_array()
            .unwrap()
            .len(),
        3
    );
    drop(state);
    std::fs::remove_dir_all(root).unwrap();
}
#[test]
fn standalone_file_act_lapse_rejects_cold_decline_duplicates_and_incomplete_sources() {
    for mode in [
        "decline",
        "capture missing",
        "unsealed",
        "duplicate source",
        "shared capture",
        "corrected",
        "incomplete",
        "run scoped",
    ] {
        let (root, state, act) = captured(
            act_control::FileActKind::Check,
            if mode == "decline" { "decline" } else { "act" },
        );
        let log = storage::project_file(&root, recorder::LOG).unwrap();
        let capture = storage::write_capture_path(
            &root,
            act["body"]["captureEvidence"][0]["ref"].as_str().unwrap(),
        )
        .unwrap();
        match mode {
            "capture missing" => std::fs::remove_file(&capture).unwrap(),
            "unsealed" => {
                let mut c: Value =
                    serde_json::from_slice(&std::fs::read(&capture).unwrap()).unwrap();
                c.as_object_mut().unwrap().remove("seal");
                std::fs::write(&capture, serde_json::to_vec(&c).unwrap()).unwrap();
            }
            "duplicate source" => {
                let other = storage::project_log(&root, None, "synthetic-copy").unwrap();
                storage::ensure_directory(other.parent().unwrap()).unwrap();
                std::fs::copy(&log, other).unwrap();
            }
            "shared capture" => {
                records::append_with_id(
                    &log,
                    "human_act",
                    &records::APP_INTERFACE,
                    act["body"].clone(),
                    "rec:synthetic:shared-capture",
                )
                .unwrap();
            }
            "corrected" => {
                let mut c = act.clone();
                c["recordId"] = json!("rec:synthetic:correction");
                c["corrects"] = act["recordId"].clone();
                c["correctionReason"] = json!("Synthetic correction");
                append_raw(&log, c);
            }
            "incomplete" => {
                let other = storage::project_log(&root, None, "synthetic-bad").unwrap();
                storage::ensure_directory(other.parent().unwrap()).unwrap();
                std::fs::write(other, b"not a record\n").unwrap();
            }
            "run scoped" => {
                let mut c = act.clone();
                c["runId"] = json!("run:synthetic:separate-owner");
                std::fs::write(&log, format!("{c}\n")).unwrap();
            }
            _ => {}
        }
        std::fs::write(root.join("output.txt"), b"changed").unwrap();
        let view = observe(&state);
        assert!(
            view["lapseObservation"]["recorded"]
                .as_array()
                .unwrap()
                .is_empty(),
            "{mode}: {view}"
        );
        assert!(
            view["lapseObservation"]["pending"]
                .as_array()
                .unwrap()
                .is_empty(),
            "{mode}: {view}"
        );
        assert!(
            records::read_log(&log)
                .0
                .iter()
                .all(|e| e["kind"] != "act_lapsed"),
            "{mode}"
        );
        drop(state);
        std::fs::remove_dir_all(root).unwrap();
    }
}
#[test]
fn standalone_file_act_lapse_retry_refuses_changed_original_sources() {
    for mode in [
        "log replaced",
        "capture replaced",
        "corrected",
        "shared capture",
        "link changed",
        "root replaced",
    ] {
        let (root, state, act) = captured(act_control::FileActKind::Check, "act");
        let log = storage::project_file(&root, recorder::LOG).unwrap();
        std::fs::write(root.join("output.txt"), b"observed change").unwrap();
        storage::fail_directory_for_test(Some(log.parent().unwrap().to_owned()));
        let pending = observe(&state);
        storage::fail_directory_for_test(None);
        assert_eq!(
            pending["lapseObservation"]["pending"]
                .as_array()
                .unwrap()
                .len(),
            1
        );
        let before = records::read_log(&log).0.len();
        let moved = root.with_extension("held-original");
        match mode {
            "log replaced" => {
                let old = log.with_extension("old");
                std::fs::rename(&log, &old).unwrap();
                std::fs::copy(&old, &log).unwrap();
            }
            "capture replaced" => {
                let capture = storage::write_capture_path(
                    &root,
                    act["body"]["captureEvidence"][0]["ref"].as_str().unwrap(),
                )
                .unwrap();
                let bytes = std::fs::read(&capture).unwrap();
                std::fs::remove_file(&capture).unwrap();
                std::fs::write(&capture, bytes).unwrap();
            }
            "corrected" => {
                let mut c = act.clone();
                c["recordId"] = json!("rec:synthetic:correction");
                c["corrects"] = act["recordId"].clone();
                c["correctionReason"] = json!("Synthetic correction");
                append_raw(&log, c);
            }
            "shared capture" => {
                records::append_with_id(
                    &log,
                    "human_act",
                    &records::APP_INTERFACE,
                    act["body"].clone(),
                    "rec:synthetic:shared-capture",
                )
                .unwrap();
            }
            "link changed" => {
                let link = root.join(records_store::PROJECT_LINK);
                let mut value: Value =
                    serde_json::from_slice(&std::fs::read(&link).unwrap()).unwrap();
                value["synthetic-change"] = json!(true);
                std::fs::write(link, serde_json::to_vec(&value).unwrap()).unwrap();
            }
            "root replaced" => {
                std::fs::rename(&root, &moved).unwrap();
                std::fs::create_dir(&root).unwrap();
            }
            _ => unreachable!(),
        }
        let result = retry(&state);
        assert_eq!(
            result["lapseObservation"]["pending"][0]["body"],
            pending["lapseObservation"]["pending"][0]["body"],
            "{mode}: {result}"
        );
        assert!(
            result["lapseObservation"]["recorded"]
                .as_array()
                .unwrap()
                .is_empty(),
            "{mode}: {result}"
        );
        assert_eq!(
            records::read_log(&log).0.len(),
            before + usize::from(matches!(mode, "corrected" | "shared capture")),
            "retry appended no rebinding or late-write limit: {mode}"
        );
        drop(state);
        std::fs::remove_dir_all(&root).unwrap();
        if moved.exists() {
            std::fs::remove_dir_all(moved).unwrap();
        }
    }
}
#[test]
fn standalone_file_act_lapse_limited_history_stays_visible_and_does_not_establish_interval() {
    let (root, state, act) = captured(act_control::FileActKind::Check, "act");
    std::fs::write(root.join("output.txt"), b"changed").unwrap();
    let view = observe(&state);
    let lapse = view["lapseObservation"]["recorded"][0].clone();
    let log = storage::project_file(&root, recorder::LOG).unwrap();
    let mut corrected = lapse.clone();
    corrected["recordId"] = json!("rec:synthetic:history-correction");
    corrected["corrects"] = lapse["recordId"].clone();
    corrected["correctionReason"] = json!("Synthetic correction");
    corrected["body"]["c0"]["value"] = json!("different original");
    append_raw(&log, corrected);
    std::fs::write(root.join("output.txt"), C0).unwrap();
    fresh(&state, &root);
    let result = observe(&state);
    assert!(result["lapseObservation"]["recorded"]
        .as_array()
        .unwrap()
        .is_empty());
    let row = &result["rows"][0];
    assert_eq!(row["recordId"], act["recordId"]);
    assert!(row["lapseHistoryClaims"].as_array().unwrap().is_empty());
    assert_eq!(
        row["lapseHistoryLimitedClaims"].as_array().unwrap().len(),
        2
    );
    assert!(!row["lapseHistoryLimits"].as_array().unwrap().is_empty());
    assert!(!row["comparison"].as_str().unwrap().contains("again"));
    drop(state);
    std::fs::remove_dir_all(root).unwrap();
}
#[test]
fn standalone_file_act_lapse_saved_observation_disclosure_failure_has_distinct_phase() {
    let (root, state, _) = captured(act_control::FileActKind::Check, "act");
    let log = storage::project_file(&root, recorder::LOG).unwrap();
    std::fs::write(root.join("output.txt"), b"first observed").unwrap();
    storage::fail_directory_for_test(Some(log.parent().unwrap().to_owned()));
    let held = observe(&state);
    storage::fail_directory_for_test(None);
    assert_eq!(
        held["lapseObservation"]["pending"][0]["observationDurable"],
        false
    );
    let parent = log.parent().unwrap().to_owned();
    file_act_lapse::before_late_limit_for_test(move || {
        storage::fail_directory_for_test(Some(parent))
    });
    let disclosure = retry(&state);
    storage::fail_directory_for_test(None);
    println!("FILE_ACT_LAPSE_DISCLOSURE_PENDING_DTO:{disclosure}");
    let pending = &disclosure["lapseObservation"]["pending"][0];
    assert_eq!(pending["observationDurable"], true, "{disclosure}");
    assert_eq!(pending["lateWriteDisclosurePending"], true);
    assert_eq!(
        pending["recordedEntry"]["recordId"],
        held["lapseObservation"]["pending"][0]["recordId"]
    );
    assert!(disclosure["lapseObservation"]["state"]
        .as_str()
        .unwrap()
        .contains("observation saved"));
    std::fs::write(root.join("output.txt"), C0).unwrap();
    let done = retry(&state);
    assert!(done["lapseObservation"]["pending"]
        .as_array()
        .unwrap()
        .is_empty());
    assert_eq!(lapse_entries(&root).len(), 1);
    assert_eq!(logs(&root).iter().filter(|e|e["kind"]=="evidence_limit"&&e["body"]["label"]=="record write failed").count(),1,"disclosure retry reconciles landed line");
    drop(state);
    std::fs::remove_dir_all(root).unwrap();
}
#[test]
fn standalone_file_act_lapse_preserves_checkpoint_history_without_duplicate_standalone_observation()
{
    let (root, state, act) = captured(act_control::FileActKind::Check, "act");
    let run = "run:synthetic:history";
    let arrival = json!({"checkpoint":"synthetic-output","arrivalOrdinal":1});
    let act_ref = json!({"recordId":act["recordId"],"actKind":"A4","capturedAt":act["body"]["captureTime"],"capturingSurface":"app_act_control"});
    records::append_project(&root,Some(run),"synthetic-checkpoint-writer","act_counted",&records::APP_WRITER,json!({"arrival":arrival,"act":act_ref,"relation":"earlier act","referents":act["body"]["boundSubject"]})).unwrap();
    let body = json!({"act":act_ref,"state":"lapsed","referents":act["body"]["boundSubject"],"c0":act["body"]["boundContent"][0],"c1":{"method":util::FILE_IDENTITY_METHOD,"value":util::sha256_hex(b"changed")},"time":"2026-10-18T00:00:00Z","arrival":arrival,"when":"after resume"});
    records::append_project(
        &root,
        Some(run),
        "synthetic-checkpoint-writer",
        "act_lapsed",
        &records::APP_WRITER,
        body,
    )
    .unwrap();
    let before = logs(&root);
    let view = observe(&state);
    assert!(view["lapseObservation"]["recorded"]
        .as_array()
        .unwrap()
        .is_empty());
    assert_eq!(logs(&root), before);
    assert_eq!(
        view["rows"][0]["lapseHistoryClaims"]
            .as_array()
            .unwrap()
            .len(),
        1
    );
    assert!(view["rows"][0]["comparison"]
        .as_str()
        .unwrap()
        .contains("matches c0 again"));
    drop(state);
    std::fs::remove_dir_all(root).unwrap();
}

#[test]
fn standalone_file_act_lapse_history_keeps_each_log_sequence_without_timestamp_arbitration() {
    let (root, state, act) = captured(act_control::FileActKind::Check, "act");
    let act_ref = json!({"recordId":act["recordId"],"actKind":"A4","capturedAt":act["body"]["captureTime"],"capturingSurface":"app_act_control"});
    for (run, states) in [
        (
            "run:synthetic:one",
            vec![
                ("lapsed", "2099-01-01T00:00:00Z"),
                (
                    "matches c0 again after observed lapse",
                    "2000-01-01T00:00:00Z",
                ),
            ],
        ),
        (
            "run:synthetic:two",
            vec![
                (
                    "matches c0 again after observed lapse",
                    "2100-01-01T00:00:00Z",
                ),
                ("lapsed", "1999-01-01T00:00:00Z"),
            ],
        ),
    ] {
        for (state, time) in states {
            let c1 = if state == "lapsed" {
                json!({"method":util::FILE_IDENTITY_METHOD,"value":util::sha256_hex(b"changed")})
            } else {
                act["body"]["boundContent"][0].clone()
            };
            records::append_project(&root, Some(run), "synthetic-checkpoint-writer", "act_lapsed", &records::APP_WRITER,
                json!({"act":act_ref,"state":state,"referents":act["body"]["boundSubject"],"c0":act["body"]["boundContent"][0],"c1":c1,"time":time,"arrival":{"checkpoint":"synthetic-output","arrivalOrdinal":1},"when":"after resume"})).unwrap();
        }
    }
    let before = logs(&root);
    let view = observe(&state);
    let row = &view["rows"][0];
    let claims = row["lapseHistoryClaims"].as_array().unwrap();
    assert_eq!(claims.len(), 3, "{view}");
    let sources: std::collections::BTreeSet<_> = claims
        .iter()
        .map(|claim| claim["source"]["log"].as_str().unwrap())
        .collect();
    assert_eq!(sources.len(), 2);
    for source in sources {
        let chain: Vec<_> = claims
            .iter()
            .filter(|claim| claim["source"]["log"] == source)
            .collect();
        assert!(chain
            .windows(2)
            .all(|pair| pair[0]["record"]["seq"].as_u64() < pair[1]["record"]["seq"].as_u64()));
    }
    assert_eq!(row["lapseHistoryLimitedClaims"].as_array().unwrap().len(), 1, "a return without an earlier lapse in its own log stays limited even when another log has one");
    assert!(row["lapseHistoryLimits"]
        .as_array()
        .unwrap()
        .iter()
        .any(|limit| limit
            .as_str()
            .unwrap()
            .contains("order between those logs is not established")));
    assert!(row["comparison"]
        .as_str()
        .unwrap()
        .contains("matches c0 again"));
    assert!(view["lapseObservation"]["recorded"]
        .as_array()
        .unwrap()
        .is_empty());
    assert_eq!(logs(&root), before);
    drop(state);
    std::fs::remove_dir_all(root).unwrap();
}
#[test]
fn standalone_file_act_lapse_incomparable_method_is_unknown_with_present_or_absent_subject() {
    for absent in [false, true] {
        let (root, state, mut act) = captured(act_control::FileActKind::Check, "act");
        let log = storage::project_file(&root, recorder::LOG).unwrap();
        let capture_path = storage::write_capture_path(
            &root,
            act["body"]["captureEvidence"][0]["ref"].as_str().unwrap(),
        )
        .unwrap();
        let mut capture: Value =
            serde_json::from_slice(&std::fs::read(&capture_path).unwrap()).unwrap();
        // An explicitly synthetic sealed source with a foreign identity method:
        // still no claim that this method can be compared with App file bytes.
        act["body"]["boundContent"][0]["method"] = json!("synthetic.foreign/v1");
        capture["boundContent"] = act["body"]["boundContent"].clone();
        capture_seal::seal(&root, &mut capture).unwrap();
        std::fs::write(&capture_path, serde_json::to_vec(&capture).unwrap()).unwrap();
        std::fs::write(&log, format!("{act}\n")).unwrap();
        if absent {
            std::fs::remove_file(root.join("output.txt")).unwrap();
        } else {
            std::fs::write(root.join("output.txt"), b"changed").unwrap();
        }
        let result = observe(&state);
        assert_eq!(
            result["lapseObservation"]["recorded"][0]["body"]["state"], "unknown (incomparable)",
            "{result}"
        );
        assert!(result["rows"][0]["comparison"]
            .as_str()
            .unwrap()
            .contains("incomparable"));
        fresh(&state, &root);
        assert!(observe(&state)["lapseObservation"]["recorded"]
            .as_array()
            .unwrap()
            .is_empty());
        drop(state);
        std::fs::remove_dir_all(root).unwrap();
    }
}

#[test]
fn standalone_file_act_lapse_closed_store_refuses_without_new_observation() {
    let (root, state, _) = captured(act_control::FileActKind::Check, "act");
    let actor = act_control::person(Some("Synthetic fixture"), Some("invented-fixture-os"));
    let context = json!({"fixture":"local synthetic retention callback; no person's act"});
    let before = logs(&root);
    let plan = records_retention::prepare(&root, "close", None, &actor, &context).unwrap();
    records_retention::apply(plan, &actor, &context).unwrap();
    std::fs::write(root.join("output.txt"), b"changed after close").unwrap();
    let result = observe(&state);
    assert!(result["lapseObservation"]["recorded"]
        .as_array()
        .unwrap()
        .is_empty());
    assert!(result["lapseObservation"]["pending"]
        .as_array()
        .unwrap()
        .is_empty());
    assert!(!result["lapseObservation"]["limits"]
        .as_array()
        .unwrap()
        .is_empty());
    assert_eq!(logs(&root), before);
    drop(state);
    std::fs::remove_dir_all(root).unwrap();
}

#[test]
fn standalone_file_act_lapse_retry_refuses_replaced_store_root_with_same_project_subtree() {
    for scope in ["store root", "project store directory"] {
        let store = std::fs::canonicalize(std::env::temp_dir())
            .unwrap()
            .join(util::opaque_id("lapse-store-").unwrap());
        records_store::use_store_for_test(Some(Ok(records_store::Store {
            root: store.clone(),
            placement: records_store::Placement::Test,
            limits: vec![],
        })));
        let (root, state, _) = captured(act_control::FileActKind::Check, "act");
        let log = storage::project_file(&root, recorder::LOG).unwrap();
        std::fs::write(root.join("output.txt"), b"held observed change").unwrap();
        storage::fail_directory_for_test(Some(log.parent().unwrap().to_owned()));
        let held = observe(&state);
        storage::fail_directory_for_test(None);
        assert_eq!(
            held["lapseObservation"]["pending"]
                .as_array()
                .unwrap()
                .len(),
            1
        );
        let original_log = std::fs::read(&log).unwrap();
        let original_project =
            file_act_view::FileSource::directory_at(log.parent().unwrap()).unwrap();
        let replaced = if scope == "store root" {
            store.clone()
        } else {
            records_store::home(&root).unwrap().attachment.dir.unwrap()
        };
        let original_directory = file_act_view::FileSource::directory_at(&replaced).unwrap();
        let moved = replaced.with_extension("original");
        std::fs::rename(&replaced, &moved).unwrap();
        std::fs::create_dir(&replaced).unwrap();
        for entry in std::fs::read_dir(&moved).unwrap() {
            let entry = entry.unwrap();
            std::fs::rename(entry.path(), replaced.join(entry.file_name())).unwrap();
        }
        assert_ne!(
            file_act_view::FileSource::directory_at(&replaced).unwrap(),
            original_directory
        );
        assert_eq!(
            file_act_view::FileSource::directory_at(log.parent().unwrap()).unwrap(),
            original_project
        );
        let refused = retry(&state);
        assert_eq!(
            refused["lapseObservation"]["pending"][0]["body"],
            held["lapseObservation"]["pending"][0]["body"]
        );
        assert!(refused["lapseObservation"]["recorded"]
            .as_array()
            .unwrap()
            .is_empty());
        assert!(
            refused["lapseObservation"]["limits"]
                .as_array()
                .unwrap()
                .iter()
                .any(|limit| limit
                    .as_str()
                    .unwrap_or("")
                    .contains("source binding changed")),
            "{refused}"
        );
        assert_eq!(
            std::fs::read(&log).unwrap(),
            original_log,
            "retry writes no observation or late disclosure into replacement store"
        );
        drop(state);
        records_store::use_store_for_test(None);
        std::fs::remove_dir_all(root).unwrap();
        std::fs::remove_dir_all(moved).unwrap();
        std::fs::remove_dir_all(store).unwrap();
    }
}
