//! Filesystem/state-machine witnesses; native confirmation is a test stand-in, never a human-act qualification.
mod common;
use chirality_app_v4_lib::{
    act_control::{person, ActControl, InputSource},
    recorder::{identify_packages, LOG},
    records::{self, APP_WRITER},
    storage, util,
};
use common::ScratchDirectory;
use serde_json::{json, Value};
use std::{io::Write, path::Path};
fn workspace() -> ScratchDirectory {
    let ws = ScratchDirectory::new("act-storage");
    std::fs::create_dir_all(ws.join("project/decisions")).unwrap();
    std::fs::copy(
        Path::new(env!("CARGO_MANIFEST_DIR"))
            .join("../tests/fixtures/FX-DP1/project/decisions/PKG-1.json"),
        ws.join("project/decisions/PKG-1.json"),
    )
    .unwrap();
    ws
}
fn prepared(ws: &Path) -> (ActControl, String, Value) {
    identify_packages(ws).unwrap();
    let req = storage::read_all(ws)
        .0
        .into_iter()
        .find(|e| e["kind"] == "act_request")
        .unwrap();
    let mut ac = ActControl::new(ws);
    let offer = ac.compose_a16(req["recordId"].as_str().unwrap()).unwrap();
    let id = offer["offerId"].as_str().unwrap().to_owned();
    let actor = person(Some("Fixture person"), Some("fixture"));
    let text = ac.confirmation_text(&id, "ALT-2", &actor).unwrap();
    assert!(text.contains("Hold stage 2 until the version check returns, then start"));
    assert!(text.contains("Consequences:"));
    ac.present(&id).unwrap();
    (ac, id, actor)
}
#[test]
fn scope_absence_and_requester_limit_are_source_faithful() {
    for empty in [false, true] {
        let ws = workspace();
        let path = ws.join("project/decisions/PKG-1.json");
        let mut package: Value = serde_json::from_slice(&std::fs::read(&path).unwrap()).unwrap();
        if empty {
            package["scope"] = json!("")
        } else {
            package.as_object_mut().unwrap().remove("scope");
        }
        std::fs::write(&path, serde_json::to_vec(&package).unwrap()).unwrap();
        let reqs = identify_packages(&ws).unwrap();
        let req = &reqs[0];
        assert_eq!(req["body"].get("scope"), package.get("scope"));
        assert!(req["body"]["requester"].get("identity").is_none());
        let (entries, limits) = storage::read_all(&ws);
        assert!(limits.is_empty());
        assert!(entries.iter().any(|e| e["kind"] == "evidence_limit"
            && e["body"]["label"] == "requester identity not established"
            && e["body"]["subjectRef"] == req["recordId"]));
        let (mut ac, id, actor) = prepared(&ws);
        let out = ac
            .confirm(&id, "ALT-2", InputSource::HostNativeConfirmation, actor)
            .unwrap();
        assert_eq!(out["capture"]["scope"], "not named by the package");
        assert_eq!(out["record"]["body"]["scope"], "not named by the package");
    }
}
#[test]
fn frozen_native_choice_cancel_and_script_refuse_without_capture() {
    let ws = workspace();
    let (mut ac, id, actor) = prepared(&ws);
    assert!(ac
        .confirm(
            &id,
            "ALT-1",
            InputSource::HostNativeConfirmation,
            actor.clone()
        )
        .unwrap_err()
        .contains("frozen"));
    assert!(ac
        .confirm(&id, "ALT-2", InputSource::WebviewScript, actor.clone())
        .is_err());
    ac.dismiss(&id);
    assert!(ac
        .confirm(&id, "ALT-2", InputSource::HostNativeConfirmation, actor)
        .is_err());
    assert!(!ws.join(storage::CAPTURES).exists());
}
#[test]
fn rejected_append_cold_hold_and_hot_late_retry_preserve_facts_and_id() {
    let ws = workspace();
    let (mut ac, id, actor) = prepared(&ws);
    let before = std::fs::read(ws.join(LOG)).unwrap();
    let mut f = std::fs::OpenOptions::new()
        .append(true)
        .open(ws.join(LOG))
        .unwrap();
    f.write_all(b"{torn").unwrap();
    f.sync_all().unwrap();
    let out = ac
        .confirm(&id, "ALT-2", InputSource::HostNativeConfirmation, actor)
        .unwrap();
    assert_eq!(out["state"], "AC-8 record pending");
    let capture = &out["capture"];
    assert!(capture.get("recordId").is_none());
    let capid = capture["captureId"].as_str().unwrap();
    let pending: Value =
        serde_json::from_slice(&std::fs::read(storage::pending_path(&ws, capid)).unwrap()).unwrap();
    let reserved = pending["recordId"].clone();
    let mut relaunched = ActControl::new(&ws);
    assert_eq!(
        relaunched.recover_pending().unwrap()[0]["state"],
        "AC-8 record pending"
    );
    assert!(relaunched
        .compose_a16(capture["requestRef"].as_str().unwrap())
        .unwrap_err()
        .contains("incomplete record set"));
    assert_eq!(
        std::fs::read(ws.join(LOG)).unwrap().len(),
        before.len() + 5,
        "partial log is never repaired or replayed implicitly"
    );
    // Explicit fixture repair restores the pre-fault bytes; no product W-0 repair is claimed.
    std::fs::write(ws.join(LOG), before).unwrap();
    let cold = relaunched.recover_pending().unwrap().remove(0);
    assert_eq!(cold["state"], "AC-8 record pending");
    assert_eq!(
        cold["originLimit"],
        "capture origin not verified; automatic act replay held"
    );
    assert_eq!(
        records::read_log(&ws.join(LOG)).0.len(),
        2,
        "cold files never append an act"
    );
    let package_path = ws.join("project/decisions/PKG-1.json");
    let mut later: Value = serde_json::from_slice(&std::fs::read(&package_path).unwrap()).unwrap();
    later["scope"] = json!("changed after original capture");
    std::fs::write(package_path, serde_json::to_vec(&later).unwrap()).unwrap();
    let recovered = ac.recover_pending().unwrap().remove(0);
    assert_eq!(recovered["state"], "AC-7 recorded");
    assert_eq!(recovered["record"]["recordId"], reserved);
    assert_eq!(recovered["record"]["observedAt"], capture["capturedAt"]);
    assert_eq!(recovered["record"]["body"]["scope"], capture["scope"]);
    let view = chirality_app_v4_lib::decision_view::derive(&ws, &[LOG]);
    assert_eq!(
        view["rows"][0]["decision"]["lapse"],
        "lapsed — the package changed after the decision"
    );

    let late = records::read_log(&ws.join(LOG)).0;
    assert_eq!(late.len(), 4);
    assert_eq!(late[2]["kind"], "human_act");
    assert_eq!(late[3]["kind"], "evidence_limit");
    assert_eq!(late[3]["body"]["label"], "record write failed");
    assert_eq!(late[3]["body"]["subjectRef"], reserved);

    let mut facts = recovered["capture"].clone();
    facts.as_object_mut().unwrap().remove("recordId");
    assert_eq!(&facts, capture);
    let log = std::fs::read(ws.join(LOG)).unwrap();
    assert_eq!(
        relaunched.recover_pending().unwrap()[0]["state"],
        "AC-7 recorded"
    );
    assert_eq!(std::fs::read(ws.join(LOG)).unwrap(), log);
}
#[test]
fn crash_after_append_reconciles_backlink_once_without_duplicate() {
    let ws = workspace();
    let (mut ac, id, actor) = prepared(&ws);
    let out = ac
        .confirm(&id, "ALT-2", InputSource::HostNativeConfirmation, actor)
        .unwrap();
    let mut original = out["capture"].clone();
    original.as_object_mut().unwrap().remove("recordId");
    let capid = original["captureId"].as_str().unwrap();
    let path = storage::capture_path(&ws, capid);
    // Frozen fixture of crash after RS append, before backlink publication.
    std::fs::write(&path, serde_json::to_vec(&original).unwrap()).unwrap();
    let log = std::fs::read(ws.join(LOG)).unwrap();
    let recovered = ActControl::new(&ws).recover_pending().unwrap().remove(0);
    assert_eq!(recovered["capture"]["recordId"], out["record"]["recordId"]);
    assert_eq!(std::fs::read(ws.join(LOG)).unwrap(), log);
    assert!(storage::backlink(&path, "rec:conflicting").is_err());
    assert_eq!(
        serde_json::from_slice::<Value>(&std::fs::read(path).unwrap()).unwrap(),
        recovered["capture"]
    );
}
#[test]
fn capture_store_failure_is_visible_without_record_or_relocation() {
    let ws = workspace();
    let (mut ac, id, actor) = prepared(&ws);
    let before = std::fs::read(ws.join(LOG)).unwrap();
    std::fs::write(ws.join(".chirality/captures"), b"owning target blocked").unwrap();
    assert!(ac
        .confirm(&id, "ALT-2", InputSource::HostNativeConfirmation, actor)
        .is_err());
    assert_eq!(std::fs::read(ws.join(LOG)).unwrap(), before);
}
#[test]
fn legacy_and_library_history_remain_in_place_and_opaque() {
    let ws = workspace();
    let old = ws.join(storage::LEGACY_LOG);
    std::fs::create_dir_all(old.parent().unwrap()).unwrap();
    let fixture = Path::new(env!("CARGO_MANIFEST_DIR"))
        .join("../tests/fixtures/FX-DP1/records/coordination.rs.jsonl");
    std::fs::copy(fixture, &old).unwrap();
    // Only PKG-1 exists in this scratch project; history itself is not recopied to new logs.
    let bytes = std::fs::read(&old).unwrap();
    assert!(identify_packages(&ws).unwrap().is_empty());
    assert_eq!(std::fs::read(&old).unwrap(), bytes);
    assert!(!ws.join(LOG).exists());
    let entries = storage::read_all(&ws).0;
    assert_eq!(entries[0]["recordId"], "rec:app:coord:0001");
    assert_eq!(
        entries[0]["body"]["evidence"]["method"],
        util::LEGACY_FILE_IDENTITY_METHOD
    );
    let package = ws.join("project/decisions/PKG-1.json");
    let mut changed = std::fs::read(&package).unwrap();
    changed.push(b' ');
    std::fs::write(&package, &changed).unwrap();
    let fresh = identify_packages(&ws).unwrap();
    assert_eq!(
        fresh.len(),
        1,
        "changed exact bytes still create a selected-method request"
    );
    assert_eq!(
        fresh[0]["body"]["evidence"]["method"],
        "chirality.app.exact-bytes.sha256/v1"
    );
    assert_eq!(
        fresh[0]["body"]["evidence"]["claimedIdentity"],
        util::sha256_hex(&changed)
    );
    assert_ne!(fresh[0]["recordId"], entries[0]["recordId"]);
    assert!(identify_packages(&ws).unwrap().is_empty());
    assert_eq!(
        std::fs::read(&old).unwrap(),
        bytes,
        "new observation never copies, relabels or rewrites the original log"
    );
    let all = storage::read_all(&ws).0;
    assert_eq!(
        all.iter().filter(|e| e["kind"] == "human_act").count(),
        1,
        "no historical act is copied or reissued"
    );
    let view = chirality_app_v4_lib::decision_view::derive(&ws, &[]);
    let historical = view["rows"]
        .as_array()
        .unwrap()
        .iter()
        .find(|r| r["package"] == "rec:app:coord:0001")
        .unwrap();
    assert_eq!(historical["decision"]["lapse"], "unknown (incomparable)");

    let library = ScratchDirectory::new("library-acts");
    let log = storage::library_log(&library);
    let rec = records::append(
        &log,
        "evidence_limit",
        &APP_WRITER,
        json!({"label":"unresolvable reference"}),
    )
    .unwrap();
    assert_eq!(storage::read_all(&library).0[0], rec);
    assert!(storage::capture_path(&library, "cap:fixture").starts_with(&*library));
}
#[test]
fn concurrent_append_sequences_and_cross_log_ids_are_unique() {
    let ws = ScratchDirectory::new("record-race");
    let root = ws.to_path_buf();
    let log = storage::project_log(&root, None, APP_WRITER.identity);
    let mut threads = vec![];
    for _ in 0..8 {
        let log = log.clone();
        threads.push(std::thread::spawn(move || {
            for _ in 0..8 {
                records::append(
                    &log,
                    "evidence_limit",
                    &APP_WRITER,
                    json!({"label":"unresolvable reference"}),
                )
                .unwrap();
            }
        }));
    }
    for t in threads {
        t.join().unwrap();
    }
    let (entries, limits) = storage::read_all(&root);
    assert!(limits.is_empty());
    assert_eq!(entries.len(), 64);
    for (n, e) in entries.iter().enumerate() {
        assert_eq!(e["seq"], json!(n + 1));
    }
    let other = storage::project_log(&root, None, "writer:other");
    let second = records::append(
        &other,
        "evidence_limit",
        &APP_WRITER,
        json!({"label":"unresolvable reference"}),
    )
    .unwrap();
    assert_eq!(second["seq"], 1);
    assert_ne!(entries[0]["recordId"], second["recordId"]);
    let before = std::fs::read(&other).unwrap();
    assert!(records::append_with_id(
        &other,
        "evidence_limit",
        &APP_WRITER,
        json!({"label":"unresolvable reference"}),
        entries[0]["recordId"].as_str().unwrap()
    )
    .is_err());
    assert_eq!(std::fs::read(&other).unwrap(), before);
    assert!(util::opaque_id_with("rec:app:", |_| Err("fixture entropy failure".into())).is_err());
    assert!(!storage::key("../../escape").contains('/'));
    assert!(
        storage::project_log(&root, Some("run:../../escape"), "writer:../escape")
            .starts_with(&root)
    );
}
#[test]
fn backlink_failure_stays_recorded_link_pending_then_recovers_without_append() {
    use std::os::unix::fs::PermissionsExt;
    let ws = workspace();
    let (mut ac, id, actor) = prepared(&ws);
    let out = ac
        .confirm(&id, "ALT-2", InputSource::HostNativeConfirmation, actor)
        .unwrap();
    let mut capture = out["capture"].clone();
    capture.as_object_mut().unwrap().remove("recordId");
    let path = storage::capture_path(&ws, capture["captureId"].as_str().unwrap());
    std::fs::write(&path, serde_json::to_vec(&capture).unwrap()).unwrap();
    let directory = path.parent().unwrap();
    let prior = std::fs::metadata(directory).unwrap().permissions();
    std::fs::set_permissions(directory, std::fs::Permissions::from_mode(0o500)).unwrap();
    let pending = ActControl::new(&ws).recover_pending();
    std::fs::set_permissions(directory, prior).unwrap();
    let pending = pending.unwrap().remove(0);
    assert_eq!(pending["state"], "AC-7 recorded");
    assert_eq!(pending["backlinkPending"], true);
    assert_eq!(
        pending["statusDetail"],
        "act recorded; capture record link pending"
    );
    assert_eq!(pending["recordDurable"], true);
    assert!(pending["backlinkFailure"].is_string());
    assert!(pending["capture"].get("recordId").is_none());
    assert!(
        ActControl::new(&ws)
            .compose_a16(capture["requestRef"].as_str().unwrap())
            .is_ok(),
        "a durable recorded claim is not turned into a missing act by backlink failure"
    );

    let log = std::fs::read(ws.join(LOG)).unwrap();
    let recovered = ActControl::new(&ws).recover_pending().unwrap().remove(0);
    assert_eq!(recovered["state"], "AC-7 recorded");
    assert_eq!(std::fs::read(ws.join(LOG)).unwrap(), log);
}
#[test]
fn malformed_packages_duplicate_alternatives_and_digest_changes_refuse() {
    for mutation in [0, 1, 2] {
        let ws = workspace();
        let path = ws.join("project/decisions/PKG-1.json");
        let mut package: Value = serde_json::from_slice(&std::fs::read(&path).unwrap()).unwrap();
        match mutation {
            0 => {
                package["alternatives"][0]["consequences"] = json!("bad");
            }
            1 => {
                package.as_object_mut().unwrap().remove("packageId");
            }
            _ => {
                package["unexpected"] = json!(true);
            }
        }
        std::fs::write(path, serde_json::to_vec(&package).unwrap()).unwrap();
        assert!(identify_packages(&ws).unwrap().is_empty());
        assert!(!ws.join(LOG).exists());
    }
    let ws = workspace();
    let path = ws.join("project/decisions/PKG-1.json");
    let mut package: Value = serde_json::from_slice(&std::fs::read(&path).unwrap()).unwrap();
    package["alternatives"][1]["id"] = package["alternatives"][0]["id"].clone();
    std::fs::write(&path, serde_json::to_vec(&package).unwrap()).unwrap();
    let req = identify_packages(&ws).unwrap().remove(0);
    assert!(ActControl::new(&ws)
        .compose_a16(req["recordId"].as_str().unwrap())
        .unwrap_err()
        .contains("duplicate"));
    let ws = workspace();
    let (mut ac, id, actor) = prepared(&ws);
    ac.offers.get_mut(&id).unwrap().offer["purpose"] = json!("tampered");
    assert!(ac
        .confirm(&id, "ALT-2", InputSource::HostNativeConfirmation, actor)
        .is_err());
    assert!(!ws.join(storage::CAPTURES).exists());
}
#[test]
fn incomplete_foreign_log_blocks_recovery_and_backlink_even_after_local_append() {
    let ws = workspace();
    let (mut ac, id, actor) = prepared(&ws);
    let out = ac
        .confirm(&id, "ALT-2", InputSource::HostNativeConfirmation, actor)
        .unwrap();
    let mut capture = out["capture"].clone();
    capture.as_object_mut().unwrap().remove("recordId");
    let path = storage::capture_path(&ws, capture["captureId"].as_str().unwrap());
    std::fs::write(&path, serde_json::to_vec(&capture).unwrap()).unwrap();
    let foreign = storage::project_log(&ws, Some("run:foreign"), "writer:foreign");
    std::fs::create_dir_all(foreign.parent().unwrap()).unwrap();
    std::fs::write(&foreign, b"{partial").unwrap();
    let log = std::fs::read(ws.join(LOG)).unwrap();
    let result = ActControl::new(&ws).recover_pending().unwrap().remove(0);
    assert_eq!(result["state"], "AC-8 record pending");
    assert_eq!(std::fs::read(ws.join(LOG)).unwrap(), log);
    assert!(
        serde_json::from_slice::<Value>(&std::fs::read(path).unwrap())
            .unwrap()
            .get("recordId")
            .is_none()
    );
}
#[test]
fn run_and_outside_run_logs_keep_identity_and_do_not_duplicate() {
    let ws = ScratchDirectory::new("run-log");
    let run = "run:fixture/../../opaque";
    let entry = records::append_project(
        &ws,
        Some(run),
        "writer:fixture",
        "evidence_limit",
        &APP_WRITER,
        json!({"label":"unresolvable reference"}),
    )
    .unwrap();
    assert_eq!(entry["runId"], run);
    assert!(!storage::project_log(&ws, None, "writer:fixture").exists());
    assert_eq!(storage::read_all(&ws).0, vec![entry]);
}
#[test]
fn duplicate_and_disagreeing_discovered_capture_records_never_replay() {
    for disagree in [false, true] {
        let ws = workspace();
        let (mut ac, id, actor) = prepared(&ws);
        let out = ac
            .confirm(&id, "ALT-2", InputSource::HostNativeConfirmation, actor)
            .unwrap();
        let mut capture = out["capture"].clone();
        capture.as_object_mut().unwrap().remove("recordId");
        let path = storage::capture_path(&ws, capture["captureId"].as_str().unwrap());
        std::fs::write(&path, serde_json::to_vec(&capture).unwrap()).unwrap();
        let foreign = storage::project_log(&ws, None, "writer:conflict-fixture");
        std::fs::create_dir_all(foreign.parent().unwrap()).unwrap();
        let mut record = out["record"].clone();
        record["seq"] = json!(1);
        if disagree {
            record["recordId"] = json!("rec:fixture:disagreement");
            record["body"]["scope"] = json!("different original act scope");
        }
        let mut line = serde_json::to_vec(&record).unwrap();
        line.push(b'\n');
        // Synthetic conflicting input history; no qualification of another real writer.
        std::fs::write(&foreign, line).unwrap();
        let before = std::fs::read(ws.join(LOG)).unwrap();
        let result = ActControl::new(&ws).recover_pending();
        if disagree {
            assert!(result.unwrap()[0]["writeFailure"]
                .as_str()
                .unwrap()
                .contains("disagreement"));
        } else {
            assert_eq!(result.unwrap()[0]["state"], "AC-8 record pending");
        }
        assert_eq!(std::fs::read(ws.join(LOG)).unwrap(), before);
        assert!(
            serde_json::from_slice::<Value>(&std::fs::read(path).unwrap())
                .unwrap()
                .get("recordId")
                .is_none()
        );
    }
}
#[test]
fn fabricated_cold_capture_and_pending_files_never_create_native_act() {
    let ws = workspace();
    let capture: Value = serde_json::from_slice(
        &std::fs::read(
            Path::new(env!("CARGO_MANIFEST_DIR"))
                .join("../tests/fixtures/FX-DP1/aac/cap-decide-PKG-1.json"),
        )
        .unwrap(),
    )
    .unwrap();
    let mut original = capture.clone();
    original.as_object_mut().unwrap().remove("recordId");
    chirality_app_v4_lib::schema_validation::validate_capture(&original).unwrap();
    let id = original["captureId"].as_str().unwrap();
    let cap = storage::capture_path(&ws, id);
    let pending_path = storage::pending_path(&ws, id);
    storage::create_json(&cap, &original).unwrap();
    storage::create_json(&pending_path,&json!({"capture":original,"recordId":"rec:fixture:fabricated","log":LOG,"observedAt":original["capturedAt"],"delayed":false})).unwrap();
    let cap_bytes = std::fs::read(&cap).unwrap();
    let pending_bytes = std::fs::read(&pending_path).unwrap();
    let result = ActControl::new(&ws).recover_pending().unwrap().remove(0);
    assert_eq!(result["state"], "AC-8 record pending");
    assert_eq!(
        result["originLimit"],
        "capture origin not verified; automatic act replay held"
    );
    assert!(storage::read_all(&ws).0.is_empty());
    assert!(!ws.join(LOG).exists());
    assert_eq!(std::fs::read(cap).unwrap(), cap_bytes);
    assert_eq!(std::fs::read(pending_path).unwrap(), pending_bytes);
}
#[test]
fn writer_sequence_gaps_duplicates_and_reordering_hold_append_and_backlink() {
    for seqs in [[1, 3], [1, 1], [2, 1]] {
        let ws = workspace();
        let (mut ac, id, actor) = prepared(&ws);
        let out = ac
            .confirm(&id, "ALT-2", InputSource::HostNativeConfirmation, actor)
            .unwrap();
        let mut capture = out["capture"].clone();
        capture.as_object_mut().unwrap().remove("recordId");
        let path = storage::capture_path(&ws, capture["captureId"].as_str().unwrap());
        std::fs::write(&path, serde_json::to_vec(&capture).unwrap()).unwrap();
        let foreign = storage::project_log(&ws, None, "writer:sequence-fixture");
        let mut lines = vec![];
        for seq in seqs {
            let mut entry = records::append(
                &foreign,
                "evidence_limit",
                &APP_WRITER,
                json!({"label":"unresolvable reference"}),
            )
            .unwrap();
            entry["seq"] = json!(seq);
            lines.push(entry);
        }
        // Introduce individually schema-valid but incomplete/contradictory input history.
        let bytes = lines
            .iter()
            .map(|e| serde_json::to_string(e).unwrap() + "\n")
            .collect::<String>();
        std::fs::write(&foreign, bytes).unwrap();
        assert!(storage::read_all(&ws)
            .1
            .iter()
            .any(|l| l.contains("sequence")));
        let before = std::fs::read(ws.join(LOG)).unwrap();
        let result = ActControl::new(&ws).recover_pending().unwrap().remove(0);
        assert_eq!(result["state"], "AC-8 record pending");
        assert!(records::append(
            &ws.join(LOG),
            "evidence_limit",
            &APP_WRITER,
            json!({"label":"unresolvable reference"})
        )
        .is_err());
        assert_eq!(std::fs::read(ws.join(LOG)).unwrap(), before);
        assert!(
            serde_json::from_slice::<Value>(&std::fs::read(path).unwrap())
                .unwrap()
                .get("recordId")
                .is_none()
        );
    }
}
#[test]
fn observed_buffer_hash_and_fields_agree_after_controlled_file_replacement() {
    let ws = workspace();
    let path = ws.join("project/decisions/PKG-1.json");
    let first = std::fs::read(&path).unwrap();
    let mut replacement: Value = serde_json::from_slice(&first).unwrap();
    replacement["scope"] = json!("replacement scope");
    replacement["purpose"] = json!("replacement purpose");
    let second = serde_json::to_vec(&replacement).unwrap();
    for observed in [&first, &second, &first] {
        std::fs::write(&path, observed).unwrap();
        let buffer = std::fs::read(&path).unwrap();
        std::fs::write(&path, if observed == &first { &second } else { &first }).unwrap();
        let (package, identity) = util::package_snapshot(&buffer).unwrap();
        let body = chirality_app_v4_lib::recorder::request_from_file(
            &package,
            "project/decisions/PKG-1.json",
            &identity,
            json!({"kind":"agent"}),
            "2026-10-04T00:00:00Z",
        );
        assert_eq!(
            body["evidence"]["claimedIdentity"],
            util::sha256_hex(&buffer)
        );
        assert_eq!(
            body["evidence"]["method"],
            "chirality.app.exact-bytes.sha256/v1"
        );
        assert_eq!(identity, util::sha256_hex(&buffer));
        assert_eq!(body["scope"], package["scope"]);
        assert_eq!(body["purpose"], package["purpose"]);
        // Recorder/compose observe the replacement in their own single new snapshot.
        let requests = identify_packages(&ws).unwrap();
        let actual = std::fs::read(&path).unwrap();
        let current: Value = serde_json::from_slice(&actual).unwrap();
        let request = requests
            .into_iter()
            .last()
            .or_else(|| {
                storage::read_all(&ws).0.into_iter().rev().find(|e| {
                    e["kind"] == "act_request"
                        && e["body"]["evidence"]["claimedIdentity"] == util::sha256_hex(&actual)
                })
            })
            .unwrap();
        assert_eq!(
            request["body"]["evidence"]["method"],
            "chirality.app.exact-bytes.sha256/v1"
        );
        assert_eq!(request["body"]["purpose"], current["purpose"]);
        assert_eq!(
            request["body"]["evidence"]["claimedIdentity"],
            util::sha256_hex(&actual)
        );
        let mut control = ActControl::new(&ws);
        let offer = control
            .compose_a16(request["recordId"].as_str().unwrap())
            .unwrap();
        assert_eq!(offer["purpose"], current["purpose"]);
        assert_eq!(offer["scope"], current["scope"]);
        assert_eq!(
            offer["subject"]["contentIdentity"]["value"],
            request["body"]["evidence"]["claimedIdentity"]
        );
    }
}
#[test]
fn hot_pending_batch_keeps_native_event_order_before_delay_limits() {
    let ws = workspace();
    std::fs::copy(
        Path::new(env!("CARGO_MANIFEST_DIR"))
            .join("../tests/fixtures/FX-DP1/project/decisions/PKG-2.json"),
        ws.join("project/decisions/PKG-2.json"),
    )
    .unwrap();
    let requests = identify_packages(&ws).unwrap();
    let mut control = ActControl::new(&ws);
    let actor = person(Some("Fixture person"), Some("fixture"));
    let mut offers = vec![];
    for request in &requests {
        let offer = control
            .compose_a16(request["recordId"].as_str().unwrap())
            .unwrap();
        let id = offer["offerId"].as_str().unwrap().to_owned();
        control.confirmation_text(&id, "ALT-1", &actor).unwrap();
        control.present(&id).unwrap();
        offers.push(id);
    }
    let before = std::fs::read(ws.join(LOG)).unwrap();
    let mut torn = before.clone();
    torn.extend(b"{torn");
    std::fs::write(ws.join(LOG), torn).unwrap();
    let mut ids = vec![];
    for offer in &offers {
        let result = control
            .confirm(
                offer,
                "ALT-1",
                InputSource::HostNativeConfirmation,
                actor.clone(),
            )
            .unwrap();
        assert_eq!(result["state"], "AC-8 record pending");
        let pending: Value = serde_json::from_slice(
            &std::fs::read(storage::pending_path(
                &ws,
                result["capture"]["captureId"].as_str().unwrap(),
            ))
            .unwrap(),
        )
        .unwrap();
        ids.push(pending["recordId"].clone());
    }
    std::fs::write(ws.join(LOG), before).unwrap();
    let results = control.recover_pending().unwrap();
    assert!(results.iter().all(|r| r["state"] == "AC-7 recorded"));
    let entries = records::read_log(&ws.join(LOG)).0;
    assert_eq!(entries.len(), 8);
    for n in 0..2 {
        assert_eq!(entries[4 + n]["kind"], "human_act");
        assert_eq!(entries[4 + n]["recordId"], ids[n]);
        assert_eq!(
            entries[4 + n]["body"]["relations"]["requestRef"],
            requests[n]["recordId"]
        );
        assert_eq!(entries[6 + n]["body"]["label"], "record write failed");
        assert_eq!(entries[6 + n]["body"]["subjectRef"], ids[n]);
    }
    let after = std::fs::read(ws.join(LOG)).unwrap();
    control.recover_pending().unwrap();
    assert_eq!(std::fs::read(ws.join(LOG)).unwrap(), after);
}
#[test]
fn cold_capture_without_writer_submission_is_held_without_mint_or_reissue() {
    let ws = workspace();
    let request = identify_packages(&ws).unwrap().remove(0);
    let before = std::fs::read(ws.join(LOG)).unwrap();
    let mut original: Value = serde_json::from_slice(
        &std::fs::read(
            Path::new(env!("CARGO_MANIFEST_DIR"))
                .join("../tests/fixtures/FX-DP1/aac/cap-decide-PKG-1.json"),
        )
        .unwrap(),
    )
    .unwrap();
    original.as_object_mut().unwrap().remove("recordId");
    original["captureId"] = json!("cap:fixture:orphan");
    original["requestRef"] = request["recordId"].clone();
    original["boundSubject"] = json!([format!(
        "decision package {}",
        request["recordId"].as_str().unwrap()
    )]);
    chirality_app_v4_lib::schema_validation::validate_capture(&original).unwrap();
    let id = original["captureId"].as_str().unwrap();
    storage::create_json(&storage::capture_path(&ws, id), &original).unwrap();
    let mut cold = ActControl::new(&ws);
    let out = cold.recover_pending().unwrap().remove(0);
    assert_eq!(
        out["originLimit"],
        "capture origin not verified; automatic act replay held"
    );
    assert!(
        !storage::pending_path(&ws, id).exists(),
        "cold files cannot reserve an RS identity"
    );
    assert_eq!(std::fs::read(ws.join(LOG)).unwrap(), before);
    assert!(cold
        .compose_a16(request["recordId"].as_str().unwrap())
        .unwrap_err()
        .contains("record pending"));
}
fn twice_prepared(ws: &Path) -> (ActControl, [String; 2], Value, Value) {
    let request = identify_packages(ws).unwrap().remove(0);
    let mut control = ActControl::new(ws);
    let actor = person(Some("Fixture person"), Some("fixture"));
    let mut ids = vec![];
    for alternative in ["ALT-1", "ALT-2"] {
        let offer = control
            .compose_a16(request["recordId"].as_str().unwrap())
            .unwrap();
        let id = offer["offerId"].as_str().unwrap().to_owned();
        control.confirmation_text(&id, alternative, &actor).unwrap();
        control.present(&id).unwrap();
        ids.push(id);
    }
    (control, [ids.remove(0), ids.remove(0)], actor, request)
}
#[test]
fn older_pending_act_precedes_fresh_confirmation_and_latest_decision_stays_latest() {
    let ws = workspace();
    let (mut control, ids, actor, request) = twice_prepared(&ws);
    let before = std::fs::read(ws.join(LOG)).unwrap();
    let mut torn = before.clone();
    torn.extend(b"{torn");
    std::fs::write(ws.join(LOG), torn).unwrap();
    let first = control
        .confirm(
            &ids[0],
            "ALT-1",
            InputSource::HostNativeConfirmation,
            actor.clone(),
        )
        .unwrap();
    assert_eq!(first["state"], "AC-8 record pending");
    let reserved: Value = serde_json::from_slice(
        &std::fs::read(storage::pending_path(
            &ws,
            first["capture"]["captureId"].as_str().unwrap(),
        ))
        .unwrap(),
    )
    .unwrap();
    std::fs::write(ws.join(LOG), before).unwrap();
    let fresh = control
        .confirm(&ids[1], "ALT-2", InputSource::HostNativeConfirmation, actor)
        .unwrap();
    assert_eq!(fresh["state"], "AC-7 recorded");
    assert_eq!(
        control.offers[&ids[0]].state,
        chirality_app_v4_lib::act_control::OfferState::Recorded
    );

    let entries = records::read_log(&ws.join(LOG)).0;
    let acts = entries
        .iter()
        .filter(|e| e["kind"] == "human_act")
        .collect::<Vec<_>>();
    assert_eq!(acts.len(), 2);
    assert_eq!(acts[0]["recordId"], reserved["recordId"]);
    assert_eq!(acts[1]["recordId"], fresh["record"]["recordId"]);
    assert_eq!(acts[0]["body"]["relations"]["alternativeChosen"], "ALT-1");
    assert_eq!(acts[1]["body"]["relations"]["alternativeChosen"], "ALT-2");
    assert_eq!(
        entries[3]["body"]["label"], "record write failed",
        "pending act delay account precedes fresh writer continuation"
    );
    assert_eq!(entries[4]["recordId"], fresh["record"]["recordId"]);
    let view = chirality_app_v4_lib::decision_view::derive(&ws, &[LOG]);
    assert_eq!(view["rows"][0]["package"], request["recordId"]);
    assert_eq!(view["rows"][0]["decision"]["alternativeChosen"], "ALT-2");
    let bytes = std::fs::read(ws.join(LOG)).unwrap();
    control.recover_pending().unwrap();
    assert_eq!(std::fs::read(ws.join(LOG)).unwrap(), bytes);
}
#[test]
fn fresh_confirmed_facts_remain_pending_when_older_admission_cannot_flush() {
    let ws = workspace();
    let (mut control, ids, actor, _) = twice_prepared(&ws);
    let before = std::fs::read(ws.join(LOG)).unwrap();
    let mut torn = before.clone();
    torn.extend(b"{torn");
    std::fs::write(ws.join(LOG), torn).unwrap();
    let a = control
        .confirm(
            &ids[0],
            "ALT-1",
            InputSource::HostNativeConfirmation,
            actor.clone(),
        )
        .unwrap();
    let b = control
        .confirm(&ids[1], "ALT-2", InputSource::HostNativeConfirmation, actor)
        .unwrap();
    assert_eq!(a["state"], "AC-8 record pending");
    assert_eq!(b["state"], "AC-8 record pending");
    assert_eq!(b["capture"]["alternativeChosen"], "ALT-2");
    assert!(records::read_log(&ws.join(LOG))
        .0
        .iter()
        .all(|e| e["kind"] != "human_act"));
    let id = b["capture"]["captureId"].as_str().unwrap();
    let reserved: Value =
        serde_json::from_slice(&std::fs::read(storage::pending_path(&ws, id)).unwrap()).unwrap();
    std::fs::write(ws.join(LOG), before).unwrap();
    let results = control.recover_pending().unwrap();
    assert_eq!(results[1]["record"]["recordId"], reserved["recordId"]);
    let mut original = results[1]["capture"].clone();
    original.as_object_mut().unwrap().remove("recordId");
    assert_eq!(original, b["capture"]);
    let entries = records::read_log(&ws.join(LOG)).0;
    assert_eq!(
        entries[2]["body"]["relations"]["alternativeChosen"],
        "ALT-1"
    );
    assert_eq!(
        entries[3]["body"]["relations"]["alternativeChosen"],
        "ALT-2"
    );
    assert_eq!(entries[4]["body"]["label"], "record write failed");
    assert_eq!(entries[5]["body"]["label"], "record write failed");
}
#[test]
fn refresh_flushes_pending_native_admission_before_new_recorder_input() {
    let ws = workspace();
    let (mut control, id, actor) = prepared(&ws);
    let before = std::fs::read(ws.join(LOG)).unwrap();
    let mut torn = before.clone();
    torn.extend(b"{torn");
    std::fs::write(ws.join(LOG), torn).unwrap();
    let first = control
        .confirm(&id, "ALT-2", InputSource::HostNativeConfirmation, actor)
        .unwrap();
    assert_eq!(first["state"], "AC-8 record pending");
    std::fs::copy(
        Path::new(env!("CARGO_MANIFEST_DIR"))
            .join("../tests/fixtures/FX-DP1/project/decisions/PKG-2.json"),
        ws.join("project/decisions/PKG-2.json"),
    )
    .unwrap();
    let (_, blocked) = control.refresh_recording();
    assert!(blocked.unwrap_err().contains("older trusted native"));
    assert_eq!(records::read_log(&ws.join(LOG)).0.len(), 2);
    std::fs::write(ws.join(LOG), before).unwrap();
    let (recovery, written) = control.refresh_recording();
    assert_eq!(recovery.unwrap()[0]["state"], "AC-7 recorded");
    let written = written.unwrap();
    assert_eq!(written.len(), 1);
    let entries = records::read_log(&ws.join(LOG)).0;
    assert_eq!(entries[2]["kind"], "human_act");
    assert_eq!(entries[3]["body"]["label"], "record write failed");
    assert_eq!(entries[4]["recordId"], written[0]["recordId"]);
    assert_eq!(
        entries[5]["body"]["label"],
        "requester identity not established"
    );
}
#[test]
fn unverified_cold_files_neither_grant_append_authority_nor_hold_unrelated_refresh() {
    let ws = workspace();
    let mut control = ActControl::new(&ws);
    storage::ensure_directory(&ws.join(storage::CAPTURES)).unwrap();
    std::fs::write(
        ws.join(storage::CAPTURES).join("untrusted.json"),
        b"not capture JSON",
    )
    .unwrap();
    let (recovery, written) = control.refresh_recording();
    assert!(recovery
        .unwrap()
        .iter()
        .any(|r| r["originLimit"] == "capture origin not verified; automatic act replay held"));
    assert_eq!(written.unwrap().len(), 1);
    assert!(records::read_log(&ws.join(LOG))
        .0
        .iter()
        .all(|e| e["kind"] != "human_act"));
}
#[test]
fn legacy_request_discovery_never_coerces_unknown_methods_or_malformed_legacy_values() {
    for unknown_method in [true, false] {
        let ws = workspace();
        let path = ws.join("project/decisions/PKG-1.json");
        let package_bytes = std::fs::read(&path).unwrap();
        let digest = util::sha256_hex(&package_bytes);
        let fixture = Path::new(env!("CARGO_MANIFEST_DIR"))
            .join("../tests/fixtures/FX-DP1/records/coordination.rs.jsonl");
        let mut entries = records::read_log(&fixture).0;
        // A schema-valid opaque claim does not establish a method bridge merely by equal text.
        if unknown_method {
            entries[0]["body"]["evidence"]["method"] = json!("host:opaque-method");
        }
        entries[0]["body"]["evidence"]["claimedIdentity"] = json!(digest);
        let old = ws.join(storage::LEGACY_LOG);
        std::fs::create_dir_all(old.parent().unwrap()).unwrap();
        let original = entries
            .iter()
            .map(|e| serde_json::to_string(e).unwrap() + "\n")
            .collect::<String>()
            .into_bytes();
        std::fs::write(&old, &original).unwrap();
        let observed = identify_packages(&ws).unwrap();
        assert_eq!(observed.len(),1,"unknown designation or invalid historical representation is never coerced into equality");
        assert_eq!(
            observed[0]["body"]["evidence"]["method"],
            "chirality.app.exact-bytes.sha256/v1"
        );
        assert_eq!(observed[0]["body"]["evidence"]["claimedIdentity"], digest);
        assert_eq!(std::fs::read(&old).unwrap(), original);
        assert_eq!(std::fs::read(&path).unwrap(), package_bytes);
        assert!(identify_packages(&ws).unwrap().is_empty());
    }
}
#[test]
fn historical_request_observer_requires_registered_origin_and_exact_file_reference() {
    for wrong_origin in [true, false] {
        let ws = workspace();
        let fixture = Path::new(env!("CARGO_MANIFEST_DIR"))
            .join("../tests/fixtures/FX-DP1/records/coordination.rs.jsonl");
        let mut entries = records::read_log(&fixture).0;
        let old = if wrong_origin {
            storage::project_log(&ws, None, "unregistered-legacy-import")
        } else {
            ws.join(storage::LEGACY_LOG)
        };
        if !wrong_origin {
            entries[0]["body"]["evidence"]["ref"] = json!("project/decisions/other.json");
        }
        std::fs::create_dir_all(old.parent().unwrap()).unwrap();
        let bytes = entries
            .iter()
            .map(|e| serde_json::to_string(e).unwrap() + "\n")
            .collect::<String>()
            .into_bytes();
        std::fs::write(&old, &bytes).unwrap();
        let current = identify_packages(&ws).unwrap();
        assert_eq!(current.len(),1,"legacy-method tokens from another origin or file do not suppress a current observation");
        assert_eq!(
            current[0]["body"]["evidence"]["method"],
            "chirality.app.exact-bytes.sha256/v1"
        );
        assert_eq!(std::fs::read(&old).unwrap(), bytes);
        assert!(identify_packages(&ws).unwrap().is_empty());
    }
}
#[test]
fn incomplete_registered_legacy_history_refuses_discovery_without_rewriting_or_reissuing() {
    let ws = workspace();
    let old = ws.join(storage::LEGACY_LOG);
    std::fs::create_dir_all(old.parent().unwrap()).unwrap();
    let mut bytes = std::fs::read(
        Path::new(env!("CARGO_MANIFEST_DIR"))
            .join("../tests/fixtures/FX-DP1/records/coordination.rs.jsonl"),
    )
    .unwrap();
    bytes.extend(b"{incomplete");
    std::fs::write(&old, &bytes).unwrap();
    let package = ws.join("project/decisions/PKG-1.json");
    let original = std::fs::read(&package).unwrap();
    assert!(identify_packages(&ws)
        .unwrap_err()
        .contains("incomplete record set"));
    assert_eq!(std::fs::read(&old).unwrap(), bytes);
    assert_eq!(std::fs::read(package).unwrap(), original);
    assert!(!ws.join(LOG).exists());
}
