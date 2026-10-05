//! Public decision-read and separate writer command helpers used by lib.rs.
//! Scratch files, synthetic native confirmation stand-ins and recorded claims;
//! no supplier, actual human act, native window or sealed-origin proof.
mod common;
use chirality_app_v4_lib::{
    act_control::{person, ActControl, InputSource},
    records,
    runtime_session::{continue_decision_writer, read_decision_packages},
    storage,
};
use common::ScratchDirectory;
use serde_json::Value;
use std::os::unix::fs::PermissionsExt;
use std::path::{Path, PathBuf};
fn workspace() -> ScratchDirectory {
    let ws = ScratchDirectory::new("public-reader");
    std::fs::create_dir_all(ws.join("project/decisions")).unwrap();
    copy_package(&ws, "PKG-1.json");
    ws
}
fn copy_package(ws: &Path, name: &str) {
    let fixture = PathBuf::from(env!("CARGO_MANIFEST_DIR"))
        .join("../tests/fixtures/FX-DP1/project/decisions")
        .join(name);
    std::fs::copy(fixture, ws.join("project/decisions").join(name)).unwrap();
}
// Includes directory/file names, full file bytes and modified times. Thus the
// public read must neither create writer lock/capture/log files nor alter them.
fn census(root: &Path) -> Vec<(PathBuf, Vec<u8>, std::time::SystemTime)> {
    fn visit(root: &Path, path: &Path, out: &mut Vec<(PathBuf, Vec<u8>, std::time::SystemTime)>) {
        let meta = std::fs::symlink_metadata(path).unwrap();
        out.push((
            path.strip_prefix(root).unwrap().into(),
            if meta.is_file() {
                std::fs::read(path).unwrap()
            } else {
                vec![]
            },
            meta.modified().unwrap(),
        ));
        if meta.is_dir() {
            let mut children = std::fs::read_dir(path)
                .unwrap()
                .map(|e| e.unwrap().path())
                .collect::<Vec<_>>();
            children.sort();
            for child in children {
                visit(root, &child, out);
            }
        }
    }
    let mut out = vec![];
    visit(root, root, &mut out);
    out
}
fn requests(ws: &Path) -> Vec<Value> {
    storage::read_all(ws)
        .0
        .into_iter()
        .filter(|e| e["kind"] == "act_request")
        .collect()
}
fn synthetic_decide(control: &mut ActControl, request: &str) -> Value {
    synthetic_decide_after(control, request, || {})
}
fn synthetic_decide_after(
    control: &mut ActControl,
    request: &str,
    before_capture: impl FnOnce(),
) -> Value {
    let offer = control.compose_a16(request).unwrap();
    let id = offer["offerId"].as_str().unwrap();
    let actor = person(Some("fixture person"), Some("fixture OS"));
    control.confirmation_text(id, "ALT-1", &actor).unwrap();
    control.present(id).unwrap();
    before_capture();
    control
        .confirm(id, "ALT-1", InputSource::HostNativeConfirmation, actor)
        .unwrap()
}
#[test]
fn public_read_never_discovers_or_records_unrecorded_packages_or_pending_files() {
    let ws = workspace();
    std::fs::create_dir_all(ws.join(".chirality/captures/pending")).unwrap();
    std::fs::write(
        ws.join(".chirality/captures/pending/untrusted.json"),
        b"untrusted original pending bytes",
    )
    .unwrap();
    let before = census(&ws);
    for _ in 0..2 {
        let view = read_decision_packages(&ws);
        assert_eq!(view["readOnly"], true);
        assert!(view["rows"].as_array().unwrap().is_empty());
        assert!(view.get("requestsRecordedNow").is_none());
        assert_eq!(
            census(&ws),
            before,
            "production public-read helper must write nothing"
        );
    }
    assert!(requests(&ws).is_empty());
}
#[test]
fn explicit_writer_preserves_hot_pending_flush_before_ordinary_requests_and_read_stays_pure() {
    let ws = workspace();
    let mut control = ActControl::new(&ws);
    let startup = continue_decision_writer(&ws, Some(&mut control), "app-startup-writer");
    assert_eq!(startup["requestsRecordedNow"], 1);
    let request = requests(&ws).remove(0);
    let blocker = ws.join(".chirality/captures");
    let pending =
        synthetic_decide_after(&mut control, request["recordId"].as_str().unwrap(), || {
            // Offer/attribution checks use healthy sources. Inject publication
            // failure only afterward, at the synthetic native capture boundary.
            assert!(blocker.join(".capture.lock").exists());
            std::fs::set_permissions(&blocker, std::fs::Permissions::from_mode(0o500)).unwrap();
        });
    assert_eq!(pending["state"], "AC-8 record pending");
    copy_package(&ws, "PKG-2.json");
    let before = census(&ws);
    let view = read_decision_packages(&ws);
    assert_eq!(view["rows"].as_array().unwrap().len(), 1);
    assert_eq!(census(&ws), before);
    let held = continue_decision_writer(&ws, Some(&mut control), "explicit-command");
    assert_eq!(held["requestsRecordedNow"], 0);
    assert!(held["limits"]
        .as_array()
        .unwrap()
        .iter()
        .any(|e| e.as_str().unwrap().contains("recorder continuation held")));
    assert_eq!(requests(&ws).len(), 1);
    std::fs::set_permissions(&blocker, std::fs::Permissions::from_mode(0o700)).unwrap();
    let before_retry = census(&ws);
    read_decision_packages(&ws);
    assert_eq!(census(&ws), before_retry);
    let continued = continue_decision_writer(&ws, Some(&mut control), "explicit-command");
    assert!(continued["captureRecovery"]
        .as_array()
        .unwrap()
        .iter()
        .any(|e| e["state"] == "AC-7 recorded"));
    assert_eq!(continued["requestsRecordedNow"], 1);
    let entries = storage::read_all(&ws).0;
    let act_position = entries
        .iter()
        .position(|e| e["kind"] == "human_act")
        .unwrap();
    let second_request = entries
        .iter()
        .position(|e| {
            e["kind"] == "act_request"
                && e["body"]["evidence"]["ref"]
                    .as_str()
                    .unwrap_or("")
                    .ends_with("PKG-2.json")
        })
        .unwrap();
    assert!(
        act_position < second_request,
        "writer continuation retains pending-before-recorder ordering"
    );
    let stable = census(&ws);
    let view = read_decision_packages(&ws);
    assert_eq!(view["rows"].as_array().unwrap().len(), 2);
    assert_eq!(census(&ws), stable);
}
#[test]
fn actual_public_reader_exposes_cross_log_ambiguity_each_source_and_distinct_times_without_writes()
{
    let ws = workspace();
    let mut control = ActControl::new(&ws);
    continue_decision_writer(&ws, Some(&mut control), "app-startup-writer");
    let request = requests(&ws).remove(0);
    let captured = synthetic_decide(&mut control, request["recordId"].as_str().unwrap());
    let original = storage::read_all(&ws)
        .0
        .into_iter()
        .find(|e| e["kind"] == "human_act")
        .unwrap();
    let external = storage::project_log(&ws, None, "synthetic-other-writer");
    let writer = records::Recorder {
        role: "App writer",
        identity: "synthetic-other-writer",
    };
    let mut distinct_capture_claim = original["body"].clone();
    distinct_capture_claim["captureEvidence"][0]["ref"] =
        serde_json::json!("cap:synthetic-distinct-unverified");
    let contender =
        records::append(&external, "human_act", &writer, distinct_capture_claim).unwrap();
    let before = census(&ws);
    let view = read_decision_packages(&ws);
    assert_eq!(census(&ws), before);
    let row = &view["rows"][0];
    assert_eq!(row["state"], "ambiguous current standing");
    assert!(row["decision"].is_null());
    let current = row["currentCandidates"].as_array().unwrap();
    assert_eq!(current.len(), 2);
    assert!(current.contains(&original["recordId"]));
    assert!(current.contains(&contender["recordId"]));
    let contenders = row["contenders"].as_array().unwrap();
    assert_eq!(contenders.len(), 2);
    for claim in contenders {
        assert_eq!(claim["capturedAt"], captured["capture"]["capturedAt"]);
        assert!(claim["recordedAt"].is_string());
        assert!(claim["recordSources"]
            .as_array()
            .unwrap()
            .iter()
            .all(|source| source["log"].is_string() && source["seq"].is_number()));
        assert!(claim["captureProvenance"]
            .as_str()
            .unwrap()
            .contains("not verified"));
    }
    let sources = contenders
        .iter()
        .flat_map(|c| c["recordSources"].as_array().unwrap())
        .map(|s| s["log"].clone())
        .collect::<Vec<_>>();
    assert_ne!(sources[0], sources[1]);
    // Prior ACT ambiguity is a recorded-standing limit, not a new blanket
    // prohibition on composing a fresh offer under existing package guards.
    let offer = control
        .compose_a16(request["recordId"].as_str().unwrap())
        .unwrap();
    assert_eq!(offer["requestRef"], request["recordId"]);
    assert_eq!(census(&ws), before);
}
#[test]
fn writer_unavailable_reports_hold_without_fallback_and_read_cannot_clear_it() {
    let ws = workspace();
    let before = census(&ws);
    let writer = continue_decision_writer(&ws, None, "explicit-command");
    assert_eq!(writer["state"], "unavailable");
    assert_eq!(writer["requestsRecordedNow"], 0);
    assert!(writer["limits"][0]
        .as_str()
        .unwrap()
        .contains("recorder continuation held"));
    read_decision_packages(&ws);
    assert_eq!(census(&ws), before);
}

#[test]
fn public_request_conflict_preserves_sources_and_existing_control_refusal() {
    let ws = workspace();
    let mut control = ActControl::new(&ws);
    continue_decision_writer(&ws, Some(&mut control), "app-startup-writer");
    let request = requests(&ws).remove(0);
    let mut conflicting = request.clone();
    conflicting["seq"] = serde_json::json!(1); // standalone owning log starts at one
    conflicting["body"]["purpose"] =
        serde_json::json!("different synthetic request facts under the same recorded identity");
    chirality_app_v4_lib::schema_validation::bundled()
        .unwrap()
        .validate(&conflicting)
        .unwrap();
    let path = storage::project_log(&ws, None, "request-copy-fixture");
    std::fs::create_dir_all(path.parent().unwrap()).unwrap();
    std::fs::write(&path, serde_json::to_string(&conflicting).unwrap() + "\n").unwrap();
    assert!(records::read_log(&path).1.is_empty());
    assert!(
        records::read_log(&ws.join(chirality_app_v4_lib::recorder::LOG))
            .1
            .is_empty()
    );
    assert_eq!(
        storage::read_all(&ws).1,
        vec![format!(
            "duplicate record identity: {}",
            request["recordId"].as_str().unwrap()
        )]
    );
    let before = census(&ws);
    let view = read_decision_packages(&ws);
    assert_eq!(census(&ws), before);
    let row = &view["rows"][0];
    assert_eq!(row["requestResolution"], "conflicting identity");
    assert_eq!(row["state"], "unresolvable request identity");
    assert!(row["decision"].is_null());
    assert_eq!(row["requestSources"].as_array().unwrap().len(), 2);
    assert!(control
        .compose_a16(request["recordId"].as_str().unwrap())
        .unwrap_err()
        .contains("incomplete record set"));
    assert_eq!(census(&ws), before);
}

#[test]
fn same_agreeing_capture_records_keep_each_source_without_arbitrary_current_alias_or_time() {
    let ws = workspace();
    let mut control = ActControl::new(&ws);
    continue_decision_writer(&ws, Some(&mut control), "app-startup-writer");
    let request = requests(&ws).remove(0);
    synthetic_decide(&mut control, request["recordId"].as_str().unwrap());
    let original = storage::read_all(&ws)
        .0
        .into_iter()
        .find(|e| e["kind"] == "human_act")
        .unwrap();
    let writer = records::Recorder {
        role: "App writer",
        identity: "copy-fixture",
    };
    let path = storage::project_log(&ws, None, writer.identity);
    let copy = records::append(&path, "human_act", &writer, original["body"].clone()).unwrap();
    let before = census(&ws);
    let view = read_decision_packages(&ws);
    assert_eq!(census(&ws), before);
    let row = &view["rows"][0];
    assert_eq!(row["state"], "decided");
    assert!(
        row["decision"]["act"].is_null(),
        "multiple agreeing direct-capture records do not choose a filename alias"
    );
    assert!(row["decision"]["recordedAt"].is_null());
    assert!(row["decision"]["observedAt"].is_null());
    let equivalent = row["decision"]["equivalentCaptureRecords"]
        .as_array()
        .unwrap();
    assert_eq!(equivalent.len(), 2);
    assert!(equivalent.contains(&original["recordId"]));
    assert!(equivalent.contains(&copy["recordId"]));
    let contenders = row["contenders"].as_array().unwrap();
    assert_eq!(contenders.len(), 2);
    assert!(contenders.iter().all(|c| c["act"].is_string()
        && c["recordedAt"].is_string()
        && !c["recordSources"].as_array().unwrap().is_empty()));
    assert_eq!(census(&ws), before);
}

fn inject_complete_request_conflict(ws: &Path, request: &Value) {
    let mut conflicting = request.clone();
    conflicting["seq"] = serde_json::json!(1);
    conflicting["body"]["purpose"] =
        serde_json::json!("new conflicting request purpose after offer composition");
    chirality_app_v4_lib::schema_validation::bundled()
        .unwrap()
        .validate(&conflicting)
        .unwrap();
    let path = storage::project_log(ws, None, "late-conflict-fixture");
    std::fs::create_dir_all(path.parent().unwrap()).unwrap();
    std::fs::write(&path, serde_json::to_string(&conflicting).unwrap() + "\n").unwrap();
    assert!(records::read_log(&path).1.is_empty());
    assert!(
        records::read_log(&ws.join(chirality_app_v4_lib::recorder::LOG))
            .1
            .is_empty()
    );
    assert_eq!(
        storage::read_all(ws).1,
        vec![format!(
            "duplicate record identity: {}",
            request["recordId"].as_str().unwrap()
        )]
    );
}
fn assert_late_request_conflict_refused(after_confirmation: bool) {
    let ws = workspace();
    let mut control = ActControl::new(&ws);
    continue_decision_writer(&ws, Some(&mut control), "app-startup-writer");
    let request = requests(&ws).remove(0);
    let offer = control
        .compose_a16(request["recordId"].as_str().unwrap())
        .unwrap();
    let id = offer["offerId"].as_str().unwrap();
    let actor = person(Some("fixture person"), Some("fixture OS"));
    if after_confirmation {
        control.confirmation_text(id, "ALT-1", &actor).unwrap();
        control.present(id).unwrap();
    }
    inject_complete_request_conflict(&ws, &request);
    let before = census(&ws);
    let refused = if after_confirmation {
        control
            .confirm(id, "ALT-1", InputSource::HostNativeConfirmation, actor)
            .map(|_| ())
    } else {
        control.confirmation_text(id, "ALT-1", &actor).map(|_| ())
    };
    assert!(refused.is_err(),"a previously composed offer must refuse conflicting request identity; after_confirmation={after_confirmation}");
    assert!(refused.unwrap_err().contains("request binding"));
    assert_eq!(
        census(&ws),
        before,
        "request-binding refusal occurs before capture/record writes"
    );
    assert!(storage::read_all(&ws)
        .0
        .iter()
        .all(|e| e["kind"] != "human_act"));
}

#[test]
fn actual_offer_request_binding_refuses_complete_conflict_before_native_confirmation() {
    assert_late_request_conflict_refused(false);
}
#[test]
fn actual_offer_request_binding_refuses_complete_conflict_after_native_confirmation() {
    assert_late_request_conflict_refused(true);
}

#[test]
fn actual_offer_request_binding_refuses_changed_sole_request_before_native_capture() {
    let ws = workspace();
    let mut control = ActControl::new(&ws);
    continue_decision_writer(&ws, Some(&mut control), "app-startup-writer");
    let request = requests(&ws).remove(0);
    let offer = control
        .compose_a16(request["recordId"].as_str().unwrap())
        .unwrap();
    let id = offer["offerId"].as_str().unwrap();
    let actor = person(Some("fixture person"), Some("fixture OS"));
    control.confirmation_text(id, "ALT-1", &actor).unwrap();
    control.present(id).unwrap();
    // Synthetic corrupt-store scenario: preserve valid shapes/sequence and ID,
    // but change the originally composed request facts. No production history edit.
    let path = ws.join(chirality_app_v4_lib::recorder::LOG);
    let (mut entries, limits) = records::read_log(&path);
    assert!(limits.is_empty());
    for entry in &mut entries {
        if entry["recordId"] == request["recordId"] {
            entry["body"]["purpose"] =
                serde_json::json!("changed sole request facts after native presentation");
        }
        chirality_app_v4_lib::schema_validation::bundled()
            .unwrap()
            .validate(entry)
            .unwrap();
    }
    std::fs::write(
        &path,
        entries
            .iter()
            .map(|e| serde_json::to_string(e).unwrap() + "\n")
            .collect::<String>(),
    )
    .unwrap();
    assert!(records::read_log(&path).1.is_empty());
    assert!(storage::read_all(&ws).1.is_empty());
    let before = census(&ws);
    let error = control
        .confirm(id, "ALT-1", InputSource::HostNativeConfirmation, actor)
        .unwrap_err();
    assert!(error.contains("request binding changed"));
    assert_eq!(
        census(&ws),
        before,
        "changed sole request refused before capture/record writes"
    );
    assert!(storage::read_all(&ws)
        .0
        .iter()
        .all(|e| e["kind"] != "human_act"));
}

#[test]
fn identical_request_copies_keep_reader_resolution_distinct_from_unchanged_control_guard() {
    let ws = workspace();
    let mut control = ActControl::new(&ws);
    continue_decision_writer(&ws, Some(&mut control), "app-startup-writer");
    let request = requests(&ws).remove(0);
    assert_eq!(request["seq"], serde_json::json!(1));
    let path = storage::project_log(&ws, None, "identical-request-copy");
    std::fs::create_dir_all(path.parent().unwrap()).unwrap();
    std::fs::write(&path, serde_json::to_string(&request).unwrap() + "\n").unwrap();
    assert!(records::read_log(&path).1.is_empty());
    assert_eq!(
        storage::read_all(&ws).1,
        vec![format!(
            "duplicate record identity: {}",
            request["recordId"].as_str().unwrap()
        )]
    );
    let before = census(&ws);
    let view = read_decision_packages(&ws);
    let row = &view["rows"][0];
    assert_eq!(row["requestResolution"], "unique claim (identical copies)");
    assert_eq!(row["requestSources"].as_array().unwrap().len(), 2);
    assert!(control
        .compose_a16(request["recordId"].as_str().unwrap())
        .unwrap_err()
        .contains("incomplete record set"));
    assert_eq!(census(&ws), before);
}
