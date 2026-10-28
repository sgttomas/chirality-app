//! End-to-end package custody at the native act recovery boundary. Every actor,
//! package and confirmation below is an invented maintained test fixture.
use crate::act_control::{person, ActControl, InputSource};
use crate::{records, records_package as bag, records_store, storage};
use serde_json::{json, Value};
use std::collections::BTreeSet;
use std::path::{Path, PathBuf};

struct CaptureFixture {
    base: PathBuf,
    workspace: PathBuf,
    destination: PathBuf,
}
impl CaptureFixture {
    fn new() -> Self {
        let base = std::env::temp_dir()
            .canonicalize()
            .unwrap()
            .join(crate::util::opaque_id("package-cold-capture-").unwrap());
        let workspace = base.join("workspace");
        std::fs::create_dir_all(workspace.join("project/decisions")).unwrap();
        std::fs::copy(
            Path::new(env!("CARGO_MANIFEST_DIR"))
                .join("../tests/fixtures/FX-DP1/project/decisions/PKG-1.json"),
            workspace.join("project/decisions/PKG-1.json"),
        )
        .unwrap();
        let source = base.join("source-store");
        let destination = base.join("destination-store");
        Self::choose(&source);
        Self {
            base,
            workspace,
            destination,
        }
    }
    fn choose(path: &Path) {
        records_store::use_store_for_test(Some(Ok(records_store::Store {
            root: path.into(),
            placement: records_store::Placement::Test,
            limits: vec![],
        })));
    }
}
impl Drop for CaptureFixture {
    fn drop(&mut self) {
        storage::fail_directory_for_test(None);
        records_store::use_store_for_test(None);
        let _ = std::fs::remove_dir_all(&self.base);
    }
}
fn record_ids(entries: &[Value]) -> BTreeSet<String> {
    entries
        .iter()
        .map(|entry| entry["recordId"].as_str().unwrap().to_owned())
        .collect()
}
fn count_kind(entries: &[Value], kind: &str) -> usize {
    entries.iter().filter(|entry| entry["kind"] == kind).count()
}

#[test]
fn package_import_cold_a16_capture_preserves_claim_without_native_custody_or_replay() {
    // Both paths start at an actual native-confirmation test double. One has
    // its completed source record; the other was captured before an uncertain
    // capture-directory flush prevented writer identity reservation.
    for captured_before_record in [false, true] {
        let f = CaptureFixture::new();
        let decision = f.workspace.join("project/decisions/PKG-1.json");
        let decision_bytes = std::fs::read(&decision).unwrap();
        let actor = person(
            Some("Invented capture fixture person"),
            Some("invented-fixture-account"),
        );
        let observed =
            json!({"fixture":"native confirmation test double; no live person or supplier"});
        let request = crate::recorder::identify_packages(&f.workspace)
            .unwrap()
            .remove(0);
        let mut native = ActControl::new(&f.workspace);
        let offer = native
            .compose_a16(request["recordId"].as_str().unwrap())
            .unwrap();
        let offer_id = offer["offerId"].as_str().unwrap();
        native.confirmation_text(offer_id, "ALT-2", &actor).unwrap();
        native.present(offer_id).unwrap();
        if captured_before_record {
            let captures = storage::write_capture_dir(&f.workspace).unwrap();
            storage::ensure_directory(&captures).unwrap();
            storage::fail_directory_for_test(Some(captures));
        }
        let confirmed = native.confirm(
            offer_id,
            "ALT-2",
            InputSource::HostNativeConfirmation,
            actor.clone(),
        );
        storage::fail_directory_for_test(None);
        let confirmed = confirmed.unwrap();
        assert_eq!(
            confirmed["state"],
            if captured_before_record {
                "AC-8 record pending"
            } else {
                "AC-7 recorded"
            }
        );
        let capture_id = if captured_before_record {
            &confirmed["captureId"]
        } else {
            &confirmed["capture"]["captureId"]
        };
        let capture_id = capture_id.as_str().unwrap().to_owned();
        let source_capture = storage::capture_path(&f.workspace, &capture_id).unwrap();
        let capture_bytes = std::fs::read(&source_capture).unwrap();
        let capture: Value = serde_json::from_slice(&capture_bytes).unwrap();
        assert_eq!(capture["actKind"], "A16");
        assert_eq!(capture["alternativeChosen"], "ALT-2");
        assert_eq!(capture["actor"], actor);
        let (source_records, source_limits) = records::writer_record_set(&f.workspace);
        assert!(source_limits.is_empty(), "{source_limits:?}");
        assert_eq!(
            count_kind(&source_records, "human_act"),
            usize::from(!captured_before_record)
        );
        if !captured_before_record {
            assert_eq!(capture["recordId"], confirmed["record"]["recordId"]);
        } else {
            assert!(capture.get("recordId").is_none());
            assert!(!storage::write_pending_path(&f.workspace, &capture_id)
                .unwrap()
                .exists());
        }
        // Private native custody must end here, before export or store switching.
        drop(native);
        let attachment = records_store::attach(&f.workspace, false).unwrap();
        let project = attachment.project.unwrap();
        let source_dir = attachment.dir.unwrap();
        let source_payload = bag::payload_inventory(&source_dir).unwrap();
        let export = f.base.join("export");
        crate::records_export::export(&f.workspace, &export).unwrap();
        let export_manifest = std::fs::read(export.join("tagmanifest-sha256.txt")).unwrap();
        let source_link = std::fs::read(f.workspace.join(records_store::PROJECT_LINK)).unwrap();

        CaptureFixture::choose(&f.destination);
        assert_eq!(
            std::fs::read(f.workspace.join(records_store::PROJECT_LINK)).unwrap(),
            source_link
        );
        let plan =
            records_store::package::prepare(&f.workspace, &export, &actor, &observed).unwrap();
        let imported = records_store::package::apply(plan, &actor, &observed).unwrap();
        assert_eq!(imported["projectId"], project);
        let imported_capture = storage::capture_path(&f.workspace, &capture_id).unwrap();
        assert_eq!(std::fs::read(&imported_capture).unwrap(), capture_bytes);
        let mut cold = ActControl::new(&f.workspace);
        let recovered = cold.recover_pending().unwrap();
        assert_eq!(recovered.len(), 1, "{recovered:?}");
        let result = &recovered[0];
        assert_eq!(result["capture"]["captureId"], capture_id);
        if captured_before_record {
            assert_eq!(result["state"], "AC-8 record pending");
            assert!(result["originLimit"]
                .as_str()
                .unwrap()
                .contains("automatic act replay held"));
            assert!(result.get("record").is_none());
        } else {
            assert_eq!(result["state"], "AC-7 recorded");
            assert_eq!(result["record"], confirmed["record"]);
            assert!(result["provenance"]
                .as_str()
                .unwrap()
                .contains("does not verify native capture origin"));
        }
        let (after_recovery, limits) = records::writer_record_set(&f.workspace);
        assert!(limits.is_empty(), "{limits:?}");
        assert_eq!(record_ids(&after_recovery), record_ids(&source_records));
        assert_eq!(
            count_kind(&after_recovery, "human_act"),
            count_kind(&source_records, "human_act")
        );
        assert_eq!(
            count_kind(&after_recovery, "act_counted"),
            count_kind(&source_records, "act_counted")
        );
        assert_eq!(std::fs::read(&imported_capture).unwrap(), capture_bytes);

        // Public-API custody probe: without any cold files to rediscover, a
        // second call has no native queue to flush and recreates no capture.
        // Only destination test files move; source evidence stays untouched.
        let aside = f.base.join("retained-imported-capture.json");
        std::fs::rename(&imported_capture, &aside).unwrap();
        let pending = storage::pending_file_for(&f.workspace, &capture).unwrap();
        let pending_aside = f.base.join("retained-imported-pending.json");
        let pending_bytes = if pending.exists() {
            let bytes = std::fs::read(&pending).unwrap();
            std::fs::rename(&pending, &pending_aside).unwrap();
            Some(bytes)
        } else {
            None
        };
        assert!(cold.recover_pending().unwrap().is_empty());
        assert!(
            !imported_capture.exists(),
            "cold JSON must never become native capture custody"
        );
        assert!(!pending.exists());
        assert!(cold.writer_ready());
        std::fs::rename(&aside, &imported_capture).unwrap();
        if let Some(bytes) = pending_bytes {
            assert_eq!(std::fs::read(&pending_aside).unwrap(), bytes);
            std::fs::rename(&pending_aside, &pending).unwrap();
        }
        let (final_records, limits) = records::writer_record_set(&f.workspace);
        assert!(limits.is_empty(), "{limits:?}");
        assert_eq!(final_records, after_recovery);
        assert_eq!(std::fs::read(&imported_capture).unwrap(), capture_bytes);
        assert_eq!(std::fs::read(source_capture).unwrap(), capture_bytes);
        assert_eq!(bag::payload_inventory(&source_dir).unwrap(), source_payload);
        assert_eq!(
            std::fs::read(export.join("tagmanifest-sha256.txt")).unwrap(),
            export_manifest
        );
        assert_eq!(std::fs::read(&decision).unwrap(), decision_bytes);
        assert!(crate::records_export::verify(&export).is_ok());
    }
}
