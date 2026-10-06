//! Synthetic owning-event checks; none observes an actual native person/dialog.
use super::*;
struct Fixture {
    root: PathBuf,
    path: PathBuf,
    control: ActControl,
}
impl Fixture {
    fn new() -> Self {
        let parent = std::fs::canonicalize(std::env::temp_dir()).unwrap();
        let root = parent.join(crate::util::opaque_id("file-act-").unwrap());
        std::fs::create_dir(&root).unwrap();
        let path = root.join("output.txt");
        std::fs::write(&path, b"reviewed App output\n").unwrap();
        let control = ActControl::new(&root);
        Self {
            root,
            path,
            control,
        }
    }
    fn offer(&mut self, kind: FileActKind) -> FileActOfferRef {
        self.control
            .compose_file_act(
                &self.path,
                kind,
                "one identified output",
                "test the selected act",
            )
            .unwrap()
    }
    fn ready(
        &mut self,
        kind: FileActKind,
        decline: bool,
    ) -> (FileActOfferRef, native::ConfirmedFileEvent) {
        let offer = self.offer(kind);
        let actor = person(Some("Synthetic person"), Some("synthetic-os"));
        let context = json!({"fixture":"owning home 1"});
        let (_, digest, _) = self
            .control
            .freeze_file_native(&offer, &actor, &context)
            .unwrap();
        let event = native::ConfirmedFileEvent::synthetic(
            offer.id.clone(),
            digest,
            actor,
            context,
            decline,
        );
        (offer, event)
    }
    fn entries(&self) -> Vec<Value> {
        let (entries, limits) = storage::read_all(&self.root);
        assert!(limits.is_empty(), "{limits:?}");
        entries
    }
}
impl Drop for Fixture {
    fn drop(&mut self) {
        let _ = std::fs::remove_dir_all(&self.root);
    }
}
#[test]
fn file_act_all_kinds_preserve_kind_content_actor_and_decline_distinction() {
    for kind in [FileActKind::Check, FileActKind::Approve, FileActKind::Rely] {
        for decline in [false, true] {
            let mut f = Fixture::new();
            let (offer, event) = f.ready(kind, decline);
            let out = f.control.consume_file_event(&offer, event).unwrap();
            assert_eq!(out["state"], "AC-7 recorded", "{out}");
            let record = &out["record"];
            assert_eq!(
                record["kind"],
                if decline { "act_declined" } else { "human_act" }
            );
            assert_eq!(out["capture"]["actKind"], kind.code());
            assert_eq!(
                out["capture"]["boundContent"][0]["value"],
                crate::util::sha256_hex(b"reviewed App output\n")
            );
            assert_eq!(out["capture"]["actor"]["identityVerified"], false);
            if decline {
                assert_eq!(record["body"]["declinedKind"], kind.code());
                assert!(record["body"].get("actKind").is_none());
            } else {
                assert_eq!(record["body"]["actKind"], kind.code());
                assert_eq!(record["body"]["recordingMode"], "direct capture");
                assert_eq!(
                    record["body"]["actClass"]["value"],
                    "reserved to the person"
                );
            }
            assert_eq!(f.entries().len(), 1);
            assert_eq!(
                f.control.continue_file_act(&offer).unwrap()["record"]["recordId"],
                record["recordId"]
            );
            assert_eq!(f.entries().len(), 1);
        }
    }
}
#[test]
fn file_act_unpresented_dismissed_and_repeated_events_cannot_capture() {
    let mut f = Fixture::new();
    let offer = f.offer(FileActKind::Check);
    let digest = f.control.file_act_preview(&offer).unwrap().0["offerDigest"].clone();
    let actor = person(None, Some("synthetic-os"));
    let context = json!({});
    assert!(f
        .control
        .consume_file_event(
            &offer,
            native::ConfirmedFileEvent::synthetic(
                offer.id.clone(),
                digest.clone(),
                actor.clone(),
                context.clone(),
                false
            )
        )
        .is_err());
    f.control.dismiss_file_act(&offer);
    assert!(f
        .control
        .freeze_file_native(&offer, &actor, &context)
        .is_err());
    assert!(f.entries().is_empty());
    let (offer, event) = f.ready(FileActKind::Check, false);
    let duplicate = native::ConfirmedFileEvent::synthetic(
        event.id().into(),
        event.digest().clone(),
        event.actor().clone(),
        event.context().clone(),
        false,
    );
    f.control.consume_file_event(&offer, event).unwrap();
    assert!(f.control.consume_file_event(&offer, duplicate).is_err());
    assert_eq!(f.entries().len(), 1);
}
#[test]
fn file_act_changed_removed_and_symlinked_subjects_refuse() {
    for mode in [0, 1, 2] {
        let mut f = Fixture::new();
        let (offer, event) = f.ready(FileActKind::Approve, false);
        match mode {
            0 => std::fs::write(&f.path, b"changed").unwrap(),
            1 => std::fs::remove_file(&f.path).unwrap(),
            _ => {
                let other = f.root.join("other");
                std::fs::write(&other, b"reviewed App output\n").unwrap();
                std::fs::remove_file(&f.path).unwrap();
                std::os::unix::fs::symlink(other, &f.path).unwrap();
            }
        }
        assert!(f.control.consume_file_event(&offer, event).is_err());
        assert!(f.entries().is_empty());
        assert!(f.control.native_captures.is_empty());
    }
}
#[test]
fn file_act_wrong_digest_actor_or_context_never_mints_capture() {
    for fault in 0..3 {
        let mut f = Fixture::new();
        let (offer, event) = f.ready(FileActKind::Rely, false);
        let mut digest = event.digest().clone();
        let mut actor = event.actor().clone();
        let mut context = event.context().clone();
        match fault {
            0 => digest["value"] = json!("other"),
            1 => actor["osAccount"] = json!("other"),
            _ => context = json!({"fixture":"other home"}),
        }
        let bad =
            native::ConfirmedFileEvent::synthetic(offer.id.clone(), digest, actor, context, false);
        assert!(f.control.consume_file_event(&offer, bad).is_err());
        assert!(f.control.native_captures.is_empty());
        assert!(f.entries().is_empty());
    }
}
#[test]
fn file_act_definite_first_lock_or_publication_failure_never_retries_into_an_act() {
    for fail_write in [false, true] {
        let mut f = Fixture::new();
        let (offer, event) = f.ready(FileActKind::Check, true);
        let lock = f.root.join(CAPTURE_STORE).join(".capture.lock");
        if fail_write {
            storage::fail_capture_write_for_test(true);
        } else {
            std::fs::create_dir_all(&lock).unwrap();
        }
        let result = f.control.consume_file_event(&offer, event);
        storage::fail_capture_write_for_test(false);
        assert!(result.unwrap_err().contains("nothing captured"));
        assert!(f.control.native_captures.is_empty());
        if !fail_write {
            std::fs::remove_dir(lock).unwrap();
        }
        assert!(f.control.continue_file_act(&offer).is_err());
        f.control.recover_pending().unwrap();
        assert!(f.entries().is_empty());
        let (new_offer, new_event) = f.ready(FileActKind::Check, true);
        assert_eq!(
            f.control.consume_file_event(&new_offer, new_event).unwrap()["state"],
            "AC-7 recorded"
        );
        assert_eq!(f.entries().len(), 1);
    }
}
#[test]
fn file_act_uncertain_publication_requires_stored_matching_bytes_and_durability() {
    let mut f = Fixture::new();
    let (offer, event) = f.ready(FileActKind::Rely, false);
    storage::ensure_directory(&f.root.join(CAPTURE_STORE)).unwrap();
    storage::fail_directory_for_test(Some(f.root.clone()));
    let result = f.control.consume_file_event(&offer, event);
    storage::fail_directory_for_test(None);
    let result = result.unwrap();
    assert_eq!(result["state"], "capture publication uncertain");
    assert!(f.control.native_captures.is_empty());
    assert!(f.entries().is_empty());
    let path = storage::capture_path(&f.root, result["captureId"].as_str().unwrap());
    let bytes = std::fs::read(&path).unwrap();
    std::fs::remove_file(&path).unwrap();
    assert_eq!(
        f.control.continue_file_act(&offer).unwrap()["state"],
        "capture publication uncertain"
    );
    f.control.recover_pending().unwrap();
    assert!(!path.exists());
    assert!(f.entries().is_empty());
    std::fs::write(&path, b"{}").unwrap();
    assert_eq!(
        f.control.continue_file_act(&offer).unwrap()["state"],
        "capture publication uncertain"
    );
    assert_eq!(std::fs::read(&path).unwrap(), b"{}");
    std::fs::write(&path, &bytes).unwrap();
    let out = f.control.continue_file_act(&offer).unwrap();
    assert_eq!(out["state"], "AC-7 recorded");
    assert_eq!(out["capture"]["captureId"], result["captureId"]);
}
#[test]
fn file_act_decline_and_a16_retain_shared_admission_order_after_record_failure() {
    let mut f = Fixture::new();
    std::fs::create_dir_all(f.root.join("project/decisions")).unwrap();
    std::fs::copy(
        Path::new(env!("CARGO_MANIFEST_DIR"))
            .join("../tests/fixtures/FX-DP1/project/decisions/PKG-1.json"),
        f.root.join("project/decisions/PKG-1.json"),
    )
    .unwrap();
    let request = crate::recorder::identify_packages(&f.root)
        .unwrap()
        .remove(0);
    let a16 = f
        .control
        .compose_a16(request["recordId"].as_str().unwrap())
        .unwrap();
    let a16id = a16["offerId"].as_str().unwrap().to_owned();
    let actor = person(None, Some("synthetic-os"));
    f.control
        .confirmation_text(&a16id, "ALT-2", &actor)
        .unwrap();
    f.control.present(&a16id).unwrap();
    let (file, event) = f.ready(FileActKind::Check, true);
    storage::fail_directory_for_test(Some(f.root.join(LOG).parent().unwrap().to_path_buf()));
    let first = f.control.consume_file_event(&file, event);
    let second = f
        .control
        .confirm(&a16id, "ALT-2", InputSource::HostNativeConfirmation, actor);
    storage::fail_directory_for_test(None);
    assert_eq!(first.unwrap()["state"], "AC-8 record pending");
    assert_eq!(second.unwrap()["state"], "AC-8 record pending");
    f.control.recover_pending().unwrap();
    let entries = f.entries();
    let acts = entries
        .iter()
        .filter(|e| matches!(e["kind"].as_str(), Some("human_act" | "act_declined")))
        .collect::<Vec<_>>();
    assert_eq!(acts.len(), 2);
    assert_eq!(acts[0]["kind"], "act_declined");
    assert_eq!(acts[1]["body"]["actKind"], "A16");
}
#[test]
fn file_act_failed_log_retains_capture_and_cold_files_cannot_supply_authority() {
    let mut f = Fixture::new();
    let (offer, event) = f.ready(FileActKind::Rely, false);
    let log = f.root.join(LOG);
    std::fs::create_dir_all(&log).unwrap();
    let out = f.control.consume_file_event(&offer, event).unwrap();
    assert_eq!(out["state"], "AC-8 record pending", "{out}");
    let original = f
        .control
        .native_captures
        .values()
        .next()
        .unwrap()
        .capture
        .clone();
    std::fs::remove_dir(&log).unwrap();
    let mut cold = ActControl::new(&f.root);
    let observed = cold.recover_pending().unwrap();
    assert!(observed.iter().all(|v| v["state"] != "AC-7 recorded"));
    assert!(f.entries().is_empty());
    let recorded = f.control.continue_file_act(&offer).unwrap();
    assert_eq!(recorded["state"], "AC-7 recorded");
    assert_eq!(recorded["capture"]["capturedAt"], original["capturedAt"]);
}
#[test]
fn file_act_owner_change_and_restoration_keep_original_hot_capture() {
    let mut f = Fixture::new();
    let (offer, event) = f.ready(FileActKind::Check, false);
    let log = f.root.join(LOG);
    std::fs::create_dir_all(&log).unwrap();
    let result = f.control.consume_file_event(&offer, event).unwrap();
    assert_eq!(result["state"], "AC-8 record pending");
    let original = f
        .control
        .native_captures
        .values()
        .next()
        .unwrap()
        .capture
        .clone();
    let other = f.root.join("other-root");
    std::fs::create_dir(&other).unwrap();
    f.control.workspace = other.clone();
    assert!(f.control.continue_file_act(&offer).is_err());
    f.control.recover_pending().unwrap();
    assert!(!other.join(LOG).exists());
    f.control.workspace = f.root.clone();
    std::fs::remove_dir(log).unwrap();
    let recorded = f.control.continue_file_act(&offer).unwrap();
    assert_eq!(recorded["state"], "AC-7 recorded");
    assert_eq!(recorded["capture"]["captureId"], original["captureId"]);
    assert_eq!(recorded["capture"]["capturedAt"], original["capturedAt"]);
}
#[test]
fn file_act_compose_refuses_outside_scope_and_preserves_exact_preview() {
    let mut f = Fixture::new();
    let offer = f.offer(FileActKind::Check);
    let (view, bytes) = f.control.file_act_preview(&offer).unwrap();
    assert_eq!(bytes, b"reviewed App output\n");
    assert_eq!(view["answers"]["standing"], STANDING);
    assert!(f
        .control
        .compose_file_act(&f.path, FileActKind::Check, " ", "purpose")
        .is_err());
    let outside = Fixture::new();
    assert!(f
        .control
        .compose_file_act(&outside.path, FileActKind::Check, "scope", "purpose")
        .is_err());
}
#[test]
fn file_act_decline_body_cannot_be_relabelled_as_act_by_writer() {
    let mut f = Fixture::new();
    let (offer, event) = f.ready(FileActKind::Check, true);
    let out = f.control.consume_file_event(&offer, event).unwrap();
    let native = f.control.native_captures.values().next().unwrap();
    let pending = native.pending.as_ref().unwrap();
    let mut fake = body(&native.capture);
    fake["declinedKind"] = json!("A7");
    assert!(records::append_capture_submission(&f.root, pending, fake).is_err());
    assert_eq!(f.entries().len(), 1);
    assert_eq!(
        records::capture_record_kind(&native.capture).unwrap(),
        "act_declined"
    );
    assert_eq!(out["record"]["kind"], "act_declined");
}

#[test]
fn file_act_fifo_refusals_have_bounded_subprocess_lifetime() {
    for mode in ["compose", "present", "confirm", "open-race"] {
        let mut child = std::process::Command::new(std::env::current_exe().unwrap())
            .args([
                "--exact",
                "act_control::file_act::tests::file_act_fifo_worker",
                "--ignored",
                "--nocapture",
            ])
            .env("CHIRALITY_FILE_ACT_FIFO_CASE", mode)
            .spawn()
            .unwrap();
        let deadline = std::time::Instant::now() + std::time::Duration::from_secs(3);
        loop {
            if let Some(status) = child.try_wait().unwrap() {
                assert!(status.success(), "FIFO {mode} worker failed");
                break;
            }
            if std::time::Instant::now() >= deadline {
                let _ = child.kill();
                let _ = child.wait();
                panic!("FIFO {mode} blocked past bounded deadline");
            }
            std::thread::sleep(std::time::Duration::from_millis(10));
        }
    }
}
fn replace_with_fifo(path: &Path) {
    use std::os::unix::ffi::OsStrExt;
    std::fs::remove_file(path).unwrap();
    let path = std::ffi::CString::new(path.as_os_str().as_bytes()).unwrap();
    assert_eq!(unsafe { libc::mkfifo(path.as_ptr(), 0o600) }, 0);
}
#[test]
#[ignore = "subprocess only, bounded by file_act_fifo_refusals_have_bounded_subprocess_lifetime"]
fn file_act_fifo_worker() {
    let Ok(mode) = std::env::var("CHIRALITY_FILE_ACT_FIFO_CASE") else {
        return;
    };
    let mut f = Fixture::new();
    match mode.as_str() {
        "compose" => {
            replace_with_fifo(&f.path);
            assert!(f
                .control
                .compose_file_act(&f.path, FileActKind::Check, "scope", "purpose")
                .is_err());
        }
        "present" => {
            let offer = f.offer(FileActKind::Check);
            replace_with_fifo(&f.path);
            assert!(f
                .control
                .freeze_file_native(&offer, &person(None, Some("os")), &json!({}))
                .is_err());
        }
        "confirm" => {
            let (offer, event) = f.ready(FileActKind::Check, false);
            replace_with_fifo(&f.path);
            assert!(f.control.consume_file_event(&offer, event).is_err());
        }
        "open-race" => {
            BEFORE_FILE_OPEN.with(|hook| *hook.borrow_mut() = Some(Box::new(replace_with_fifo)));
            assert!(f
                .control
                .compose_file_act(&f.path, FileActKind::Check, "scope", "purpose")
                .is_err());
        }
        _ => panic!("unexpected FIFO mode"),
    }
    assert!(f.control.native_captures.is_empty());
    assert!(f.entries().is_empty());
}

#[test]
fn file_act_publication_stage_helper_does_not_change_legacy_create_json() {
    let f = Fixture::new();
    let legacy = f.root.join("legacy.json");
    let new = f.root.join("new.json");
    let value = json!({"fixture":"publication stage only"});
    storage::fail_capture_write_for_test(true);
    let old_result = storage::create_json(&legacy, &value);
    let new_result = storage::create_capture_json(&new, &value);
    storage::fail_capture_write_for_test(false);
    assert!(old_result.is_ok());
    assert!(matches!(
        new_result,
        Err(storage::CapturePublicationFailure::DefinitelyNotPublished(
            _
        ))
    ));
    assert!(!new.exists());
    assert!(storage::create_capture_json(&new, &value).is_ok());
    assert!(matches!(
        storage::create_capture_json(&new, &value),
        Err(storage::CapturePublicationFailure::PublicationUncertain(_))
    ));
    let old_error = storage::create_json(&legacy, &value).unwrap_err();
    assert!(old_error.starts_with("create-once evidence publication:"));
    assert_eq!(
        std::fs::read(&legacy).unwrap(),
        std::fs::read(&new).unwrap()
    );
}
