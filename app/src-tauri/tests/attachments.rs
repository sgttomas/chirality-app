#[path = "../src/attachments.rs"]
mod attachments;
#[path = "../src/schema_validation.rs"]
mod schema_validation;
#[path = "../src/util.rs"]
mod util;
use attachments::*;
use serde_json::{json, Value};
use sha2::{Digest, Sha256};
use std::path::{Path, PathBuf};

struct Files(PathBuf);
impl Files {
    fn new() -> Self {
        let token = new_submission_ref().unwrap();
        let path = std::env::temp_dir().join(format!(
            "chirality-attachment-{}",
            token.strip_prefix("submission:").unwrap()
        ));
        std::fs::create_dir(&path).unwrap();
        Self(path)
    }
    fn write(&self, name: &str, bytes: &[u8]) -> PathBuf {
        let path = self.0.join(name);
        std::fs::write(&path, bytes).unwrap();
        path
    }
    fn select(&self, name: &str, bytes: &[u8]) -> SelectedTextAttachment {
        SelectedTextAttachment::from_native_selection(self.write(name, bytes), None).unwrap()
    }
}
impl Drop for Files {
    fn drop(&mut self) {
        std::fs::remove_dir_all(&self.0).unwrap();
    }
}
fn independent_hash(bytes: &[u8]) -> String {
    format!("{:x}", Sha256::digest(bytes))
}
fn prepare(selection: &SelectedTextAttachment) -> PreparedTextAttachment {
    selection
        .prepare_for_source(
            &selection.native_path(),
            &new_submission_ref().unwrap(),
            "2026-10-05T00:00:00Z",
        )
        .unwrap()
}
fn fixture(name: &str) -> Value {
    serde_json::from_slice(
        &std::fs::read(
            Path::new(env!("CARGO_MANIFEST_DIR"))
                .join("resources/attachments")
                .join(name),
        )
        .unwrap(),
    )
    .unwrap()
}

#[test]
fn exact_snapshot_identity_and_native_text_keep_bom_crlf_whitespace_and_empty_file() {
    let files = Files::new();
    for bytes in [b"\xef\xbb\xbfhello\r\nlast\t  ".as_slice(), b"abc", b""] {
        let selected = files.select("snapshot.md", bytes);
        let prepared = prepare(&selected);
        let input = prepared.native_input();
        let (line, body) = input["text"].as_str().unwrap().split_once('\n').unwrap();
        assert_eq!(body.as_bytes(), bytes);
        assert!(line.contains("snapshot.md") && line.contains("Its bytes follow this line."));
        let record = prepared.supply_record();
        assert_eq!(
            record["identityAtSubmission"]["value"],
            independent_hash(bytes)
        );
        assert_eq!(
            record["identityAtSelection"],
            record["identityAtSubmission"]
        );
        assert_eq!(record["byteLength"], bytes.len());
        assert_eq!(
            record["elementIdentity"]["value"],
            independent_hash(input["text"].as_str().unwrap().as_bytes())
        );
        assert_eq!(input["type"], "text");
        assert_eq!(input["text_elements"], json!([]));
        assert_eq!(record["providerAdoption"], "not observed");
        assert!(!record.as_object().unwrap().contains_key("nativeTurnId"));
        validate_supply(record).unwrap();
    }
    assert_eq!(std::fs::read_dir(&files.0).unwrap().count(), 1); // no cache or output file
}

#[test]
fn original_file_bound_is_inclusive_and_wrapper_does_not_reduce_it() {
    let files = Files::new();
    for length in [TEXT_FILE_BOUND - 1, TEXT_FILE_BOUND] {
        let selected = files.select(&format!("{}.md", "name".repeat(40)), &vec![b'x'; length]);
        let p = prepare(&selected);
        assert_eq!(p.supply_record()["byteLength"], length);
        if length == TEXT_FILE_BOUND {
            assert!(p.native_input()["text"].as_str().unwrap().len() > TEXT_FILE_BOUND);
        }
    }
    let path = files.write("large.md", &vec![b'x'; TEXT_FILE_BOUND + 1]);
    let hold = SelectedTextAttachment::from_native_selection(path, None).unwrap_err();
    assert_eq!(hold.reason, HoldReason::TextCarrierUnavailable);
    assert!(hold.message.contains("nothing sent"));
}

#[test]
fn source_drift_missing_directory_and_nontext_are_visible_holds_not_alternate_content() {
    let files = Files::new();
    let path = files.write("drift.md", b"selected");
    let selected = SelectedTextAttachment::from_native_selection(path.clone(), None).unwrap();
    std::fs::write(&path, b"other content").unwrap();
    assert_eq!(
        selected
            .prepare_for_source(&selected.native_path(), &new_submission_ref().unwrap(), "t")
            .unwrap_err()
            .reason,
        HoldReason::ContentChanged
    );
    std::fs::remove_file(&path).unwrap();
    assert_eq!(
        selected
            .prepare_for_source(&selected.native_path(), &new_submission_ref().unwrap(), "t")
            .unwrap_err()
            .reason,
        HoldReason::Unreadable
    );
    assert_eq!(
        SelectedTextAttachment::from_native_selection(files.0.clone(), None)
            .unwrap_err()
            .reason,
        HoldReason::Unreadable
    );
    for (name, bytes) in [
        ("nul.md", b"a\0b".as_slice()),
        ("invalid.md", b"\xff".as_slice()),
        ("image.PNG", b"valid text".as_slice()),
    ] {
        let hold = SelectedTextAttachment::from_native_selection(files.write(name, bytes), None)
            .unwrap_err();
        assert_eq!(hold.reason, HoldReason::TextCarrierUnavailable);
    }
    // Reconfirming means actual fresh selection, never accepting stale selected identity.
    let path = files.write("drift.md", b"current");
    let current = SelectedTextAttachment::from_native_selection(path, None).unwrap();
    assert_eq!(
        prepare(&current).supply_record()["identityAtSubmission"]["value"],
        independent_hash(b"current")
    );
}

#[test]
fn foreign_tagged_source_and_relative_source_cannot_become_dispatch_paths() {
    let files = Files::new();
    let selected = files.select("selected.md", b"same bytes");
    let foreign = files.write("foreign.md", b"same bytes");
    assert_eq!(
        selected
            .prepare_for_source(
                &native_path_identity(&foreign),
                &new_submission_ref().unwrap(),
                "t"
            )
            .unwrap_err()
            .reason,
        HoldReason::SourceMismatch
    );
    let display = selected.snapshot()["displayPath"].clone();
    assert_eq!(
        selected
            .prepare_for_source(&display, &new_submission_ref().unwrap(), "t")
            .unwrap_err()
            .reason,
        HoldReason::SourceMismatch
    );
    assert_eq!(
        SelectedTextAttachment::from_native_selection(PathBuf::from("selected.md"), None)
            .unwrap_err()
            .reason,
        HoldReason::SupplierPathUnavailable
    );
}

#[cfg(unix)]
#[test]
fn non_unicode_native_path_retains_exact_identity_and_is_never_lossy_dispatched() {
    use std::ffi::OsString;
    use std::os::unix::ffi::{OsStrExt, OsStringExt};
    let files = Files::new();
    let path = files
        .0
        .join(OsString::from_vec(b"invalid-\xff.md".to_vec()));
    // The strict supplier-representability guard precedes file IO. The host
    // need not permit creation of an invalid-byte filename to exercise it.
    let readable = files.write("readable.md", b"actual contents");
    let hold = SelectedTextAttachment::from_native_selection(path.clone(), None).unwrap_err();
    assert_eq!(hold.reason, HoldReason::SupplierPathUnavailable);
    assert_eq!(hold.native_path["encoding"], "unix_bytes");
    assert_eq!(
        hold.native_path["bytes"],
        json!(path.as_os_str().as_bytes())
    );
    assert_ne!(hold.display_path.as_bytes(), path.as_os_str().as_bytes());
    assert_eq!(std::fs::read(&readable).unwrap(), b"actual contents");
    assert_eq!(std::fs::read_dir(&files.0).unwrap().count(), 1);
}

#[cfg(unix)]
#[test]
fn name_and_path_controls_cannot_add_framing_but_file_text_is_unchanged() {
    let files = Files::new();
    let selected = files.select("quoted\"\nname.md", b"[Chirality] literal user bytes\r\n");
    let prepared = prepare(&selected);
    let (header, body) = prepared.native_input()["text"]
        .as_str()
        .unwrap()
        .split_once('\n')
        .unwrap();
    assert!(header.contains("\\n") && header.contains("\\\""));
    assert_eq!(body.as_bytes(), b"[Chirality] literal user bytes\r\n");
}

#[test]
fn ordered_list_has_distinct_immutable_refs_one_token_and_no_partial_preparation() {
    let files = Files::new();
    let a = files.select("a.md", b"a");
    let b = files.select("b.md", b"b");
    let token = new_submission_ref().unwrap();
    let list = prepare_ordered(&[a.clone(), b.clone()], &token, "t").unwrap();
    assert_eq!(list.submission_ref(), token);
    assert_eq!(
        list.preparation_standing(),
        "prepared; not persisted or sent"
    );
    let refs = list.supply_refs();
    let records = list.supply_records();
    assert_eq!(refs.len(), 2);
    assert_ne!(refs[0], refs[1]);
    assert_eq!(
        refs[0],
        format!(
            "attachment:{}",
            records[0]["attachmentId"].as_str().unwrap()
        )
    );
    assert!(records.iter().all(|r| r["turnRef"] == token));
    assert!(list.native_inputs()[0]["text"]
        .as_str()
        .unwrap()
        .ends_with("\na"));
    assert!(list.native_inputs()[1]["text"]
        .as_str()
        .unwrap()
        .ends_with("\nb"));
    let mut external_copy = list.supply_records();
    external_copy[0]["turnRef"] = "turn:guessed".into();
    assert_eq!(list.supply_records()[0]["turnRef"], token);
    assert_eq!(list.entries()[0].selection_ref(), a.selection_ref());
    assert_eq!(list.entries()[0].source_identity(), &a.native_path());
    assert_eq!(
        prepare_ordered(&[a.clone(), a], &token, "t")
            .unwrap_err()
            .reason,
        HoldReason::InvalidSubmission
    );
    std::fs::write(files.0.join("b.md"), b"changed").unwrap();
    assert_eq!(
        prepare_ordered(&[files.select("c.md", b"c"), b], &token, "t")
            .unwrap_err()
            .reason,
        HoldReason::ContentChanged
    );
}

#[test]
fn same_name_different_sources_stay_distinct_and_preparing_again_mints_new_ids() {
    let files = Files::new();
    std::fs::create_dir(files.0.join("one")).unwrap();
    std::fs::create_dir(files.0.join("two")).unwrap();
    let a = files.select("one/same.md", b"one");
    let b = files.select("two/same.md", b"two");
    let list = prepare_ordered(&[a.clone(), b], &new_submission_ref().unwrap(), "t").unwrap();
    assert_eq!(
        list.supply_records()[0]["displayName"],
        list.supply_records()[1]["displayName"]
    );
    assert_ne!(
        list.supply_records()[0]["identityAtSubmission"],
        list.supply_records()[1]["identityAtSubmission"]
    );
    assert_ne!(prepare(&a).supply_ref(), prepare(&a).supply_ref());
}

#[test]
fn draft_workflow_text_keeps_trial_reference_and_never_becomes_registered_guidance() {
    let files = Files::new();
    let path = files.write("WORKFLOW.md", b"---\nname: draft-test\n---\n# Draft\n");
    let draft = DraftTrialReference::new(
        "project",
        "draft-test",
        json!({"method":"package-source-method","value":"draft-package-id"}),
    )
    .unwrap();
    let selected = SelectedTextAttachment::from_native_selection(path, Some(draft)).unwrap();
    let p = prepare(&selected);
    let r = p.supply_record();
    assert_eq!(r["draft"]["content"]["value"], "draft-package-id");
    assert_eq!(
        r["draft"]["standing"],
        "draft — not a registered workflow; this conversation is not a workflow run"
    );
    assert!(p.native_input()["text"]
        .as_str()
        .unwrap()
        .starts_with("[Chirality] Attached file"));
    assert!(!p
        .native_input()
        .as_object()
        .unwrap()
        .contains_key("developerInstructions"));
    assert!(!r.as_object().unwrap().contains_key("a15_record"));
    assert!(
        DraftTrialReference::new("bundled", "draft", json!({"method":"m","value":"v"})).is_err()
    );
}

#[test]
fn full_canonical_validation_accepts_all_valid_fixtures_and_refuses_each_invalid_fixture() {
    let validator = SupplyValidator::from_schema(SUPPLY_SCHEMA).unwrap();
    for valid in fixture("nir.attachment-supply-record.example.valid.json")["instances"]
        .as_array()
        .unwrap()
    {
        validator.validate(valid).unwrap();
    }
    for case in fixture("nir.attachment-supply-record.example.invalid.json")
        .as_array()
        .unwrap()
    {
        assert!(
            validator.validate(&case["instance"]).is_err(),
            "{}",
            case["case"]
        );
    }
    let files = Files::new();
    let selected = files.select("f.md", b"actual");
    let mut forged = prepare(&selected).supply_record().clone();
    forged["providerAdoption"] = "adopted".into();
    assert!(validator.validate(&forged).is_err());
    assert_eq!(
        selected
            .prepare_for_source(&selected.native_path(), "turn:invented", "t")
            .unwrap_err()
            .reason,
        HoldReason::InvalidSubmission
    );
    assert_eq!(
        selected
            .prepare_for_source(&selected.native_path(), &new_submission_ref().unwrap(), "")
            .unwrap_err()
            .reason,
        HoldReason::NonconformantRecord
    );
    let mut unavailable: Value = serde_json::from_str(SUPPLY_SCHEMA).unwrap();
    unavailable["$id"] = "urn:foreign".into();
    assert!(SupplyValidator::from_schema(&unavailable.to_string()).is_err());
}

#[test]
fn embedded_assets_match_canonical_sources_and_produced_input_matches_actual_supplier_schema() {
    let manifest = fixture("manifest.json");
    let cargo = Path::new(env!("CARGO_MANIFEST_DIR"));
    let repo = cargo.ancestors().nth(4).unwrap();
    for row in manifest.as_array().unwrap() {
        let asset = std::fs::read(
            cargo
                .join("resources/attachments")
                .join(row["file"].as_str().unwrap()),
        )
        .unwrap();
        assert_eq!(independent_hash(&asset), row["sha256"]);
        assert_eq!(
            asset,
            std::fs::read(repo.join(row["source"].as_str().unwrap())).unwrap()
        );
    }
    let mut schema: Value = serde_json::from_str(include_str!(
        "../resources/supplier/0.160.0/codex_app_server_protocol.v2.schemas.json"
    ))
    .unwrap();
    schema["$ref"] = "#/definitions/UserInput".into();
    let validator = jsonschema::options()
        .with_draft(jsonschema::Draft::Draft7)
        .offline()
        .build(&schema)
        .unwrap();
    let files = Files::new();
    let selected = files.select("supplier.md", b"supplier-shaped text\r\n");
    validator
        .validate(prepare(&selected).native_input())
        .unwrap();
}

#[cfg(unix)]
fn make_owned_fifo(path: &Path) {
    use std::os::unix::ffi::OsStrExt;
    let native = std::ffi::CString::new(path.as_os_str().as_bytes()).unwrap();
    // SAFETY: owned NUL-free fixture path; CString lives through mkfifo.
    let result = unsafe { libc::mkfifo(native.as_ptr(), 0o600) };
    assert_eq!(result, 0, "mkfifo: {}", std::io::Error::last_os_error());
}

#[cfg(unix)]
#[test]
fn fifo_source_worker() {
    let Some(case) = std::env::var_os("CHIRALITY_ATTACHMENT_FIFO_CASE") else {
        // A real positive regular/Unicode source when the whole suite runs it.
        let files = Files::new();
        let selected = files.select("unicode-ü.md", b"regular\r\n");
        assert!(prepare(&selected).native_input()["text"]
            .as_str()
            .unwrap()
            .ends_with("regular\r\n"));
        return;
    };
    let root = PathBuf::from(std::env::var_os("CHIRALITY_ATTACHMENT_FIFO_ROOT").unwrap());
    let path = root.join("owned-source.md");
    match case.to_str().unwrap() {
        "initial" => {
            make_owned_fifo(&path); // No writer.
            let hold = SelectedTextAttachment::from_native_selection(path, None).unwrap_err();
            assert_eq!(hold.reason, HoldReason::Unreadable);
            assert!(hold.message.contains("not a regular file"));
        }
        "replacement" => {
            std::fs::write(&path, b"selected regular bytes").unwrap();
            let selected =
                SelectedTextAttachment::from_native_selection(path.clone(), None).unwrap();
            std::fs::remove_file(&path).unwrap();
            make_owned_fifo(&path); // Actual regular-to-FIFO replacement; no writer.
            let hold = selected
                .prepare_for_source(&selected.native_path(), &new_submission_ref().unwrap(), "t")
                .unwrap_err();
            assert_eq!(hold.reason, HoldReason::Unreadable);
            assert!(hold.message.contains("not a regular file"));
        }
        _ => panic!("unexpected owned fixture case"),
    }
}

#[cfg(unix)]
fn fifo_case_has_bounded_completion(case: &str) {
    use std::process::{Command, Stdio};
    use std::time::{Duration, Instant};
    let files = Files::new(); // Parent owns cleanup even after timeout/kill.
    let mut worker = Command::new(std::env::current_exe().unwrap())
        .args(["--exact", "fifo_source_worker", "--nocapture"])
        .env("CHIRALITY_ATTACHMENT_FIFO_CASE", case)
        .env("CHIRALITY_ATTACHMENT_FIFO_ROOT", &files.0)
        .stdout(Stdio::piped())
        .stderr(Stdio::piped())
        .spawn()
        .unwrap();
    let deadline = Instant::now() + Duration::from_secs(2);
    loop {
        if worker.try_wait().unwrap().is_some() {
            let output = worker.wait_with_output().unwrap();
            assert!(
                output.status.success(),
                "{case}: {}{}",
                String::from_utf8_lossy(&output.stdout),
                String::from_utf8_lossy(&output.stderr)
            );
            break;
        }
        if Instant::now() >= deadline {
            worker.kill().unwrap();
            let output = worker.wait_with_output().unwrap();
            panic!(
                "{case}: original 2s FIFO deadline exceeded; worker killed/reaped: {}{}",
                String::from_utf8_lossy(&output.stdout),
                String::from_utf8_lossy(&output.stderr)
            );
        }
        std::thread::sleep(Duration::from_millis(10));
    }
}

#[cfg(unix)]
#[test]
fn initial_fifo_without_writer_is_held_before_any_blocking_read() {
    fifo_case_has_bounded_completion("initial");
}

#[cfg(unix)]
#[test]
fn selected_regular_source_replaced_by_fifo_is_held_without_blocking() {
    fifo_case_has_bounded_completion("replacement");
}
