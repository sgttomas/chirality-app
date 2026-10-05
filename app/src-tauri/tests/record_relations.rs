//! General RS corrections from actual once-read schema-valid log files.
mod common;
use chirality_app_v4_lib::{
    decision_view::{derive, record_relations::read_logs},
    records, schema_validation,
};
use common::ScratchDirectory;
use serde_json::{json, Value};
use std::path::{Path, PathBuf};
fn claim(id: &str, seq: u64, detail: &str) -> Value {
    let fixtures: Value = serde_json::from_slice(
        &std::fs::read(
            Path::new(env!("CARGO_MANIFEST_DIR")).join("schemas/fixtures/valid-records.json"),
        )
        .unwrap(),
    )
    .unwrap();
    let mut r = fixtures[10].clone();
    r["recordId"] = json!(id);
    r["seq"] = json!(seq);
    r["writtenAt"] = json!("equal-clock");
    r["body"]["detail"] = json!(detail);
    r
}
fn correction(id: &str, seq: u64, target: &str, detail: &str) -> Value {
    let mut r = claim(id, seq, detail);
    r["corrects"] = json!(target);
    r["correctionReason"] = json!("synthetic correction reason");
    r
}
fn write(root: &ScratchDirectory, name: &str, rows: &[Value]) -> PathBuf {
    let path = root.join(name);
    let mut bytes = Vec::new();
    for r in rows {
        schema_validation::bundled().unwrap().validate(r).unwrap();
        bytes.extend(serde_json::to_vec(r).unwrap());
        bytes.push(b'\n');
    }
    std::fs::write(&path, bytes).unwrap();
    path
}
fn group<'a>(v: &'a Value, id: &str) -> &'a Value {
    v["correctionGroups"]
        .as_array()
        .unwrap()
        .iter()
        .find(|g| g["recordIds"].as_array().unwrap().contains(&json!(id)))
        .unwrap()
}
#[test]
fn actual_general_log_chain_preserves_all_immutable_claims_and_connects_decision_view_once_read_projection(
) {
    let root = ScratchDirectory::new("rs-correction-chain");
    let rows = vec![
        claim("rec:synthetic:original", 1, "original"),
        correction("rec:synthetic:fix", 2, "rec:synthetic:original", "fixed"),
        correction("rec:synthetic:fix2", 3, "rec:synthetic:fix", "fixed again"),
    ];
    let path = write(&root, "general.jsonl", &rows);
    let before = std::fs::read(&path).unwrap();
    assert_eq!(records::read_log(&path).0, rows);
    let v = read_logs(&[path.clone()]);
    assert_eq!(v["claims"].as_array().unwrap().len(), 3);
    assert_eq!(
        group(&v, "rec:synthetic:original")["currentCandidates"],
        json!(["rec:synthetic:fix2"])
    );
    assert_eq!(v["claims"][0]["correctedBy"], json!(["rec:synthetic:fix"]));
    let connected = derive(&root, &["general.jsonl".into()]);
    assert_eq!(
        connected["recordCorrections"]["claims"][0]["record"],
        rows[0]
    );
    assert_eq!(
        group(&connected["recordCorrections"], "rec:synthetic:original")["currentCandidates"],
        json!(["rec:synthetic:fix2"])
    );
    assert_eq!(std::fs::read(path).unwrap(), before);
}
#[test]
fn cross_log_branches_are_ambiguous_and_filename_permutations_never_choose_a_winner() {
    let root = ScratchDirectory::new("rs-correction-branches");
    let a = write(
        &root,
        "z-original.jsonl",
        &[claim("rec:synthetic:original", 1, "original")],
    );
    let b = write(
        &root,
        "a-first.jsonl",
        &[correction(
            "rec:synthetic:a",
            1,
            "rec:synthetic:original",
            "a",
        )],
    );
    let c = write(
        &root,
        "m-last.jsonl",
        &[correction(
            "rec:synthetic:z",
            1,
            "rec:synthetic:original",
            "z",
        )],
    );
    for paths in [vec![a.clone(), b.clone(), c.clone()], vec![c, b, a]] {
        let v = read_logs(&paths);
        assert_eq!(
            group(&v, "rec:synthetic:original")["currentCandidates"],
            json!(["rec:synthetic:a", "rec:synthetic:z"])
        );
        assert!(group(&v, "rec:synthetic:original")["resolution"]
            .as_str()
            .unwrap()
            .contains("ambiguous"));
    }
}
#[test]
fn complete_single_writer_branches_use_local_sequence_but_partial_stream_keeps_ambiguity() {
    let root = ScratchDirectory::new("rs-correction-local");
    let path = write(
        &root,
        "one.jsonl",
        &[
            claim("rec:synthetic:base", 1, "base"),
            correction("rec:synthetic:a", 2, "rec:synthetic:base", "a"),
            correction("rec:synthetic:b", 3, "rec:synthetic:base", "b"),
        ],
    );
    assert_eq!(
        group(&read_logs(&[path.clone()]), "rec:synthetic:base")["currentCandidates"],
        json!(["rec:synthetic:b"])
    );
    let mut bytes = std::fs::read(&path).unwrap();
    bytes.extend_from_slice(b"{torn");
    std::fs::write(&path, bytes).unwrap();
    let v = read_logs(&[path]);
    assert_eq!(
        group(&v, "rec:synthetic:base")["currentCandidates"],
        json!(["rec:synthetic:a", "rec:synthetic:b"])
    );
    assert_eq!(group(&v, "rec:synthetic:base")["sourceIncomplete"], true);
    assert!(!v["readLimits"].as_array().unwrap().is_empty());
}
#[test]
fn wrong_kind_missing_and_conflicting_targets_cycles_remain_readable_with_no_replacement() {
    let root = ScratchDirectory::new("rs-correction-refusal");
    let fixtures: Value = serde_json::from_slice(
        &std::fs::read(
            Path::new(env!("CARGO_MANIFEST_DIR")).join("schemas/fixtures/valid-records.json"),
        )
        .unwrap(),
    )
    .unwrap();
    let mut wrong = fixtures[29].clone();
    wrong["recordId"] = json!("rec:synthetic:wrong-kind");
    wrong["seq"] = json!(1);
    wrong["corrects"] = json!("rec:synthetic:base");
    wrong["correctionReason"] = json!("synthetic reason");
    let paths = vec![
        write(
            &root,
            "base.jsonl",
            &[claim("rec:synthetic:base", 1, "base")],
        ),
        write(&root, "wrong.jsonl", &[wrong]),
        write(
            &root,
            "missing.jsonl",
            &[correction(
                "rec:synthetic:missing",
                1,
                "rec:synthetic:absent",
                "missing",
            )],
        ),
        write(
            &root,
            "cycle-a.jsonl",
            &[correction(
                "rec:synthetic:cycle-a",
                1,
                "rec:synthetic:cycle-b",
                "a",
            )],
        ),
        write(
            &root,
            "cycle-b.jsonl",
            &[correction(
                "rec:synthetic:cycle-b",
                1,
                "rec:synthetic:cycle-a",
                "b",
            )],
        ),
    ];
    let v = read_logs(&paths);
    assert_eq!(v["claims"].as_array().unwrap().len(), 5);
    assert_eq!(
        group(&v, "rec:synthetic:base")["currentCandidates"],
        json!(["rec:synthetic:base"])
    );
    for id in [
        "rec:synthetic:wrong-kind",
        "rec:synthetic:missing",
        "rec:synthetic:cycle-a",
    ] {
        assert!(group(&v, id)["currentCandidates"]
            .as_array()
            .unwrap()
            .is_empty());
    }
    let x = write(
        &root,
        "conflict-a.jsonl",
        &[claim("rec:synthetic:dup", 1, "one")],
    );
    let y = write(
        &root,
        "conflict-b.jsonl",
        &[claim("rec:synthetic:dup", 1, "two")],
    );
    let z = write(
        &root,
        "fix-dup.jsonl",
        &[correction(
            "rec:synthetic:fix-dup",
            1,
            "rec:synthetic:dup",
            "fix",
        )],
    );
    let v = read_logs(&[x, y, z]);
    assert!(group(&v, "rec:synthetic:dup")["currentCandidates"]
        .as_array()
        .unwrap()
        .is_empty());
    assert!(group(&v, "rec:synthetic:fix-dup")["currentCandidates"]
        .as_array()
        .unwrap()
        .is_empty());
    assert_eq!(v["claims"].as_array().unwrap().len(), 3);
}
#[test]
fn schema_missing_reason_unreadable_line_and_identical_copies_preserve_specific_limits() {
    let root = ScratchDirectory::new("rs-correction-schema");
    let base = claim("rec:synthetic:base", 1, "base");
    let a = write(&root, "copy-a.jsonl", &[base.clone()]);
    let b = write(&root, "copy-b.jsonl", &[base]);
    let mut missing = correction("rec:synthetic:invalid", 2, "rec:synthetic:base", "invalid");
    missing.as_object_mut().unwrap().remove("correctionReason");
    let mut bytes = serde_json::to_vec(&missing).unwrap();
    bytes.extend_from_slice(b"\nnot-json\n");
    let invalid = root.join("invalid.jsonl");
    std::fs::write(&invalid, bytes).unwrap();
    let v = read_logs(&[a, b, invalid]);
    assert_eq!(v["claims"].as_array().unwrap().len(), 2);
    assert_eq!(
        v["claims"][0]["identityResolution"],
        "one unchanged claim; identical sources retained"
    );
    assert!(v["readLimits"].as_array().unwrap().len() >= 2);
    assert_eq!(
        group(&v, "rec:synthetic:base")["currentCandidates"],
        json!(["rec:synthetic:base"])
    );
}
