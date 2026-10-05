//! Actual native selector IPC helper with explicitly injected picker callbacks.
//! No real picker/window, examination, host, supplier/model or person witness.
#[allow(dead_code)]
mod common;
use chirality_app_v4_lib::{
    runtime_session::{select_trace_source, TraceSelectionSession},
    util,
};
use common::ScratchDirectory;
use serde_json::Value;
use std::{
    cell::Cell,
    path::{Path, PathBuf},
    sync::Mutex,
};
fn fixture(name: &str) -> Vec<u8> {
    std::fs::read(
        Path::new(env!("CARGO_MANIFEST_DIR"))
            .join("resources/external_trace")
            .join(name),
    )
    .unwrap()
}
fn source(ws: &Path, name: &str) -> PathBuf {
    let path = ws.join("selected.json");
    std::fs::write(&path, fixture(name)).unwrap();
    path
}
fn import(state: &Mutex<TraceSelectionSession>, path: PathBuf, record: &str, tier: &str) -> Value {
    select_trace_source(state, record, tier, || Ok(Some(path))).unwrap()
}
#[test]
fn actual_once_selected_source_keeps_full_declared_basis_bytes_path_hash_and_person_date() {
    let ws = ScratchDirectory::new("trace-join");
    let bytes = fixture("receiving/EXP-person-stated-basis.json");
    let path = source(&ws, "receiving/EXP-person-stated-basis.json");
    let state = Mutex::new(TraceSelectionSession::default());
    let picks = Cell::new(0);
    let selected = select_trace_source(&state, "exam_result", "native_supplier", || {
        picks.set(picks.get() + 1);
        Ok(Some(path.clone()))
    })
    .unwrap();
    assert_eq!(picks.get(), 1);
    assert_eq!(selected["selection"]["importIndex"], 0);
    let received = &selected["receiving"]["imports"][0];
    let original: Value = serde_json::from_slice(&bytes).unwrap();
    assert_eq!(received["assessment"], "received_supplied_record");
    assert_eq!(received["originalDocument"], original);
    assert_eq!(received["suppliedBasis"]["subject"], original["subject"]);
    assert_eq!(
        received["suppliedBasis"]["configuration"],
        original["configuration"]
    );
    assert_eq!(received["suppliedBasis"]["date"], original["date"]);
    assert_eq!(
        received["suppliedBasis"]["date"]["source"],
        "stated_by_person"
    );
    assert_eq!(
        received["source"]["originalBytes"],
        serde_json::json!(bytes)
    );
    assert_eq!(
        received["source"]["bufferIdentity"]["value"],
        util::sha256_hex(&bytes)
    );
    assert_eq!(
        received["source"]["readMechanism"],
        "regular_descriptor_read"
    );
    assert_eq!(
        received["source"]["selectedPath"],
        chirality_app_v4_lib::attachments::native_path_identity(&path)
    );
    assert_eq!(received["currentExecutableIdentity"], "not_established");
    assert_eq!(received["nativeExamination"], "not_established");
    assert_eq!(received["hostOrigin"], "unverified");
    assert_eq!(received["countsTowardV4Exm24"], false);
    assert_eq!(received["countsTowardV4Exm25"], false);
    assert_eq!(
        std::fs::read_dir(&*ws).unwrap().count(),
        1,
        "selector must not write durable imports or records"
    );
    std::fs::remove_file(path).unwrap();
    for _ in 0..2 {
        assert_eq!(state.lock().unwrap().snapshot(), selected);
    }
    assert_eq!(picks.get(), 1);
}
#[test]
fn same_filename_and_revision_other_build_are_independent_receipts_not_aliases() {
    let ws = ScratchDirectory::new("trace-independent");
    let state = Mutex::new(TraceSelectionSession::default());
    let first = import(
        &state,
        source(&ws, "receiving/EXP-person-stated-basis.json"),
        "exam_result",
        "native_supplier",
    );
    let original = first["receiving"]["imports"][0].clone();
    let next = import(
        &state,
        source(&ws, "receiving/EXP-same-revision-other-build.json"),
        "exam_result",
        "native_supplier",
    );
    let later = &next["receiving"]["imports"][1];
    assert_eq!(next["receiving"]["imports"].as_array().unwrap().len(), 2);
    assert_eq!(next["receiving"]["imports"][0], original);
    assert_eq!(
        original["suppliedBasis"]["subject"]["app_candidate"]["revision"],
        later["suppliedBasis"]["subject"]["app_candidate"]["revision"]
    );
    assert_ne!(
        original["suppliedBasis"]["subject"]["app_candidate"]["build_identity"],
        later["suppliedBasis"]["subject"]["app_candidate"]["build_identity"]
    );
    assert_ne!(
        original["source"]["bufferIdentity"],
        later["source"]["bufferIdentity"]
    );
    assert_eq!(later["account"]["entries"].as_array().unwrap().len(), 1);
    assert_eq!(std::fs::read_dir(&*ws).unwrap().count(), 1);
}
#[test]
fn cancellation_failure_invalid_kind_and_reentrant_pick_preserve_imports_without_extra_reads() {
    let ws = ScratchDirectory::new("trace-selection");
    let state = Mutex::new(TraceSelectionSession::default());
    let first = import(
        &state,
        source(&ws, "receiving/EXP-person-stated-basis.json"),
        "exam_result",
        "native_supplier",
    );
    for (kind, tier) in [
        ("renderer-path", "native_supplier"),
        ("exam_result", "trusted-origin"),
    ] {
        assert!(select_trace_source(&state, kind, tier, || panic!(
            "unsupported declarations must not open picker"
        ))
        .is_err());
        assert_eq!(state.lock().unwrap().snapshot(), first);
    }
    let cancelled =
        select_trace_source(&state, "xt_work", "definition_or_rehearsal", || Ok(None)).unwrap();
    assert_eq!(cancelled["selection"]["state"], "cancelled");
    assert_eq!(cancelled["receiving"], first["receiving"]);
    assert!(
        select_trace_source(&state, "exam_result", "native_supplier", || Err(
            "synthetic native picker failure".into()
        ))
        .is_err()
    );
    assert_eq!(
        state.lock().unwrap().snapshot()["selection"]["state"],
        "selection-failed"
    );
    assert_eq!(
        state.lock().unwrap().snapshot()["receiving"],
        first["receiving"]
    );
    let after = select_trace_source(&state, "exam_result", "native_supplier", || {
        assert!(
            select_trace_source(&state, "exam_result", "native_supplier", || panic!(
                "reentrant callback must not run"
            ))
            .unwrap_err()
            .contains("in progress")
        );
        Ok(None)
    })
    .unwrap();
    assert_eq!(after["receiving"], first["receiving"]);
}
#[test]
fn missing_basis_standalone_work_and_raw_semantic_refusals_never_borrow_previous_basis() {
    let ws = ScratchDirectory::new("trace-refusals");
    let state = Mutex::new(TraceSelectionSession::default());
    let first = import(
        &state,
        source(&ws, "receiving/EXP-person-stated-basis.json"),
        "exam_result",
        "native_supplier",
    );
    for (name, kind, tier, assessment) in [
        (
            "receiving/EXP-missing-build.json",
            "exam_result",
            "native_supplier",
            "refused_schema",
        ),
        (
            "xt-work-account.example.valid.json",
            "xt_work",
            "definition_or_rehearsal",
            "unbound",
        ),
        (
            "receiving/EXP-overlap-refused.json",
            "exam_result",
            "native_supplier",
            "refused_semantic",
        ),
        (
            "receiving/XT-false-joined-pass.json",
            "xt_result",
            "actual_host",
            "refused_semantic",
        ),
    ] {
        let bytes = fixture(name);
        let selected = import(&state, source(&ws, name), kind, tier);
        let received = selected["receiving"]["imports"]
            .as_array()
            .unwrap()
            .last()
            .unwrap();
        assert_eq!(
            selected["receiving"]["imports"][0],
            first["receiving"]["imports"][0]
        );
        assert_eq!(received["assessment"], assessment);
        assert_eq!(
            received["source"]["originalBytes"],
            serde_json::json!(bytes)
        );
        assert!(!received["reason"].as_str().unwrap().is_empty());
        if assessment != "refused_semantic" {
            assert!(received["suppliedBasis"].is_null());
            assert!(received["account"].is_null());
        }
        assert_eq!(received["countsTowardV4Exm24"], false);
        assert_eq!(received["countsTowardV4Exm25"], false);
        assert_eq!(received["hostJoin"], "deferred_DECISION-3");
    }
}
#[test]
fn malformed_and_unavailable_selection_retain_source_limits_without_fake_bytes_or_current_context()
{
    let ws = ScratchDirectory::new("trace-unavailable");
    let state = Mutex::new(TraceSelectionSession::default());
    let path = ws.join("selected.json");
    std::fs::write(&path, b"{bad source bytes").unwrap();
    let selected = import(&state, path.clone(), "exam_result", "native_supplier");
    let received = &selected["receiving"]["imports"][0];
    assert_eq!(received["assessment"], "refused_malformed");
    assert_eq!(
        received["source"]["originalBytes"],
        serde_json::json!(b"{bad source bytes")
    );
    assert!(received["suppliedBasis"].is_null());
    std::fs::remove_file(&path).unwrap();
    let selected = import(&state, path, "exam_result", "native_supplier");
    let received = &selected["receiving"]["imports"][1];
    assert_eq!(received["assessment"], "source_unavailable_or_partial");
    assert!(received["source"]["originalBytes"].is_null());
    assert!(received["source"]["bufferIdentity"].is_null());
    assert!(received["suppliedBasis"].is_null());
    assert!(received["account"].is_null());
    assert_eq!(received["currentExecutableIdentity"], "not_established");
}
