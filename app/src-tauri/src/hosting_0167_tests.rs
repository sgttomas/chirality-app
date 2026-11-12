//! Static distribution and protocol regressions; never execute the real supplier.
use super::*;
use crate::distribution_preflight::{Entry, Inventory};
use std::os::unix::fs::PermissionsExt;

fn basis() -> Value {
    serde_json::from_slice(ASSESSMENT_DISTRIBUTION).unwrap()
}
fn expected() -> Inventory {
    serde_json::from_value(basis()["inventory"].clone()).unwrap()
}
fn with_container(mut inventory: Inventory) -> Inventory {
    inventory.entries.push(Entry {
        path: ".".into(),
        kind: "dir".into(),
        mode: 0o700,
        size: None,
        sha256: None,
    });
    inventory
}

#[test]
fn canonical_member_comparison_rejects_npm_missing_changed_helper_metadata_and_modes() {
    let expected = expected();
    assert_eq!(
        expected.entries.iter().filter(|e| e.kind == "file").count(),
        42
    );
    assert_eq!(
        expected.manifest_sha256,
        "7de507bfbf3fa77efc50c9bbe24778b2c0e0a4a8a244fd90220df3cfecf0a905"
    );
    assert!(assessment_members_match(
        &expected,
        &with_container(expected.clone())
    ));
    for case in [
        "npm41",
        "missing-helper",
        "changed-helper",
        "metadata",
        "mode",
        "extra",
        "duplicate",
    ] {
        let mut actual = with_container(expected.clone());
        match case {
            "npm41" | "missing-helper" => {
                actual.entries.retain(|e| e.path != "bin/codex-exec-server")
            }
            "changed-helper" => {
                actual
                    .entries
                    .iter_mut()
                    .find(|e| e.path == "bin/codex-exec-server")
                    .unwrap()
                    .sha256 = Some("0".repeat(64))
            }
            "metadata" => {
                actual
                    .entries
                    .iter_mut()
                    .find(|e| e.path == "codex-package.json")
                    .unwrap()
                    .sha256 = Some("0".repeat(64))
            }
            "mode" => {
                actual
                    .entries
                    .iter_mut()
                    .find(|e| e.path == "bin/codex-exec-server")
                    .unwrap()
                    .mode = 0o644
            }
            "extra" => {
                let mut entry = actual.entries[0].clone();
                entry.path = "extra".into();
                actual.entries.push(entry);
            }
            "duplicate" => actual.entries.push(actual.entries[0].clone()),
            _ => unreachable!(),
        }
        assert!(!assessment_members_match(&expected, &actual), "{case}");
    }
    // The development assertion is the record's main binary.
    assert_eq!(
        expected
            .entries
            .iter()
            .find(|e| e.path == "bin/codex")
            .unwrap()
            .sha256
            .as_deref(),
        Some(assessment_supplier_sha256())
    );
    assert_eq!(
        basis()["package_metadata"]["execServer"],
        "bin/codex-exec-server"
    );
}

/// The prior pin's committed records; read only to show they no longer pass.
const PRIOR_DISTRIBUTION: &[u8] =
    include_bytes!("../resources/supplier/0.167.0/CANONICAL_DISTRIBUTION.json");
const PRIOR_GENERATION: &[u8] = include_bytes!("../resources/supplier/0.167.0/GENERATION.json");

#[test]
fn declared_pin_records_are_the_official_0167_2_archive_and_its_generation() {
    assert_eq!(DECLARED_PIN, "0.167.2");
    let basis = basis();
    assert_eq!(basis["pin"], DECLARED_PIN);
    assert_eq!(basis["package_metadata"]["version"], DECLARED_PIN);
    assert_eq!(basis["source_commit"], "ce21072c90d32c40af7a55b60b2fb35c84a43a6a");
    assert_eq!(basis["archive"]["size"], 166599161);
    assert_eq!(
        basis["archive"]["sha256"],
        "e791290651bce41938fb160b5de2bd9ff8bcf3401ca3e236c73f485fca4be1bb"
    );
    assert_eq!(
        assessment_supplier_sha256(),
        "97bc82fd46f117cf10efb95e6ff0c81dc4784f5797bcdc2cb75093ba09e4def0"
    );
    assert_eq!(assessment_identity_rows().len(), 42);
    let generation = generation_record();
    assert_eq!(generation["pin"], DECLARED_PIN);
    assert_eq!(generation["supplier"]["main_sha256"], assessment_supplier_sha256());
    assert_eq!(generation["supplier"]["archive_sha256"], basis["archive"]["sha256"]);
    assert_eq!(
        generation["supplier"]["tree_manifest_sha256"],
        assessment_manifest_sha256()
    );
    let identity = generated_output_identity();
    assert!(identity.starts_with("codex 0.167.2 generated from official release archive https://github.com/openai/codex/releases/download/rust-v0.167.2/"), "{identity}");
    for part in [
        "e791290651bce41938fb160b5de2bd9ff8bcf3401ca3e236c73f485fca4be1bb",
        "97bc82fd46f117cf10efb95e6ff0c81dc4784f5797bcdc2cb75093ba09e4def0",
        "the generation record states: complete vendor tree equal to the expected inventory before execution",
        GENERATED_MANIFEST_SHA256,
    ] {
        assert!(identity.contains(part), "{part}");
    }
    assert!(!identity.contains("npm"));
}

#[test]
fn prior_pin_tree_and_generated_output_are_refused_as_not_the_pin() {
    let prior: Value = serde_json::from_slice(PRIOR_DISTRIBUTION).unwrap();
    assert_eq!(prior["pin"], "0.167.0");
    let prior_inventory: Inventory = serde_json::from_value(prior["inventory"].clone()).unwrap();
    // The complete 0.167.0 tree differs from the declared pin's inventory.
    assert!(!assessment_members_match(&expected(), &with_container(prior_inventory.clone())));
    // Its per-file identities are not the declared pin's.
    let prior_rows: Vec<Value> = prior_inventory
        .entries
        .iter()
        .filter(|e| e.kind == "file")
        .map(|e| json!({"path":e.path,"identity":{"algorithm":"sha-256","value":e.sha256}}))
        .collect();
    assert_ne!(prior_rows, assessment_identity_rows());
    // Its main binary is not the development assertion, so the canonical route is not taken.
    let prior_main = prior_rows
        .iter()
        .find(|r| r["path"] == "bin/codex")
        .unwrap()["identity"]["value"]
        .as_str()
        .unwrap()
        .to_owned();
    assert_ne!(prior_main, assessment_supplier_sha256());
    let root = std::env::temp_dir().join(crate::util::opaque_id("prior-pin-").unwrap());
    std::fs::create_dir_all(root.join("bin")).unwrap();
    let mut cfg = HostConfig::new(root.join("bin/codex"), root.clone(), root.clone(), root.clone());
    cfg.expected_sha256 = Some(prior_main);
    assert!(assessment_preflight(&cfg).unwrap().is_none());
    std::fs::remove_dir_all(root).unwrap();
    // Another pin's generated output refuses, even with byte-identical bundles.
    assert!(generated_outputs_match_record(
        GENERATION_RECORD,
        GENERATED_MANIFEST,
        GENERATED_SCHEMA.as_bytes(),
        GENERATED_V2_SCHEMA
    ));
    assert!(!generated_outputs_match_record(
        PRIOR_GENERATION,
        GENERATED_MANIFEST,
        GENERATED_SCHEMA.as_bytes(),
        GENERATED_V2_SCHEMA
    ));
    let mut wrong_pin: Value = serde_json::from_slice(GENERATION_RECORD).unwrap();
    wrong_pin["pin"] = json!("0.167.0");
    assert!(!generated_outputs_match_record(
        &serde_json::to_vec(&wrong_pin).unwrap(),
        GENERATED_MANIFEST,
        GENERATED_SCHEMA.as_bytes(),
        GENERATED_V2_SCHEMA
    ));
    let mut changed = GENERATED_V2_SCHEMA.to_vec();
    changed.push(b' ');
    assert!(!generated_outputs_match_record(
        GENERATION_RECORD,
        GENERATED_MANIFEST,
        GENERATED_SCHEMA.as_bytes(),
        &changed
    ));
}

#[test]
fn prior_pin_label_refuses_without_server_child() {
    let root = std::env::temp_dir()
        .canonicalize()
        .unwrap()
        .join(crate::util::opaque_id("prior-pin-label-").unwrap());
    for dir in ["bin", "home", "probe"] {
        std::fs::create_dir_all(root.join(dir)).unwrap();
    }
    let main = root.join("bin/codex");
    std::fs::write(&main, "#!/bin/sh\necho 'codex-cli 0.167.0'\n").unwrap();
    std::fs::set_permissions(&main, std::fs::Permissions::from_mode(0o755)).unwrap();
    let mut cfg = HostConfig::new(main, root.join("home"), root.join("probe"), root.clone());
    cfg.allow_unverified_dev = true;
    let host = Arc::new(Host::new());
    let error = host.start(&cfg, "fixture").unwrap_err();
    assert!(error.contains("observed version label"), "{error}");
    assert_eq!(host.snapshot()["verification"]["result"], "mismatch");
    assert_eq!(host.snapshot()["verification"]["element"], "observed version label");
    assert_eq!(host.state(), "refused");
    assert!(host.child.lock().unwrap().is_none());
    std::fs::remove_dir_all(root).unwrap();
}

#[test]
fn selected_0167_mismatch_refuses_before_any_version_probe() {
    let root = std::env::temp_dir().join(crate::util::opaque_id("canonical-0167-").unwrap());
    std::fs::create_dir_all(root.join("bin")).unwrap();
    let marker = root.join("executed");
    let main = root.join("bin/codex");
    std::fs::write(
        &main,
        format!(
            "#!/bin/sh\ntouch '{}'\necho 'codex-cli {DECLARED_PIN}'\n",
            marker.display()
        ),
    )
    .unwrap();
    std::fs::set_permissions(&main, std::fs::Permissions::from_mode(0o755)).unwrap();
    let mut cfg = HostConfig::new(main, root.clone(), root.clone(), root.clone());
    cfg.expected_sha256 = Some(assessment_supplier_sha256().into());
    cfg.allow_unverified_dev = true;
    let (result, label, distribution) = Host::new().verify(0, &cfg);
    assert_eq!(result["result"], "mismatch");
    assert_eq!(result["element"], "canonical .167 distribution preflight");
    assert!(label.is_none());
    assert!(distribution.is_empty());
    assert!(!marker.exists());
    // An unrelated caller's development assertion retains its existing route.
    cfg.expected_sha256 = Some("f".repeat(64));
    assert!(assessment_preflight(&cfg).unwrap().is_none());
    std::fs::remove_dir_all(root).unwrap();
}

#[test]
#[ignore = "requires explicit retained canonical vendor; static read only, never supplier execution"]
fn retained_canonical_0167_passes_actual_static_preflight() {
    let root = PathBuf::from(
        std::env::var_os("CHIRALITY_0167_CANONICAL_VENDOR")
            .expect("explicit canonical vendor input"),
    );
    let mut cfg = HostConfig::new(root.join("bin/codex"), root.clone(), root.clone(), root);
    cfg.expected_sha256 = Some(assessment_supplier_sha256().into());
    let actual = assessment_preflight(&cfg).unwrap().unwrap();
    assert_eq!(actual.manifest_sha256, expected().manifest_sha256);
    assert_eq!(
        actual.entries.iter().filter(|e| e.kind == "file").count(),
        42
    );
}

#[test]
#[cfg(target_os = "macos")]
#[ignore = "requires explicit retained canonical vendor; private CoW mutations only, no supplier execution"]
fn retained_canonical_0167_mutations_refuse_before_probe() {
    let source = PathBuf::from(
        std::env::var_os("CHIRALITY_0167_CANONICAL_VENDOR")
            .expect("explicit canonical vendor input"),
    );
    let root =
        std::env::temp_dir().join(crate::util::opaque_id("canonical-0167-mutations-").unwrap());
    std::fs::create_dir(&root).unwrap();
    std::fs::set_permissions(&root, std::fs::Permissions::from_mode(0o700)).unwrap();
    struct Cleanup(PathBuf);
    impl Drop for Cleanup {
        fn drop(&mut self) {
            let _ = std::fs::remove_dir_all(&self.0);
        }
    }
    let _cleanup = Cleanup(root.clone());
    for case in [
        "npm41",
        "missing-helper",
        "changed-helper",
        "metadata",
        "mismatch",
    ] {
        let vendor = root.join(case);
        assert!(Command::new("/bin/cp")
            .arg("-cR")
            .arg(&source)
            .arg(&vendor)
            .status()
            .unwrap()
            .success());
        match case {
            "npm41" | "missing-helper" => {
                std::fs::remove_file(vendor.join("bin/codex-exec-server")).unwrap();
                if case == "npm41" {
                    let mut metadata = basis()["package_metadata"].clone();
                    metadata.as_object_mut().unwrap().remove("execServer");
                    std::fs::write(
                        vendor.join("codex-package.json"),
                        serde_json::to_vec_pretty(&metadata).unwrap(),
                    )
                    .unwrap();
                }
            }
            "changed-helper" => {
                let mut file = std::fs::OpenOptions::new()
                    .write(true)
                    .open(vendor.join("bin/codex-exec-server"))
                    .unwrap();
                file.write_all(b"changed").unwrap();
            }
            "metadata" => {
                let mut metadata = basis()["package_metadata"].clone();
                metadata["execServer"] = json!("bin/other");
                std::fs::write(
                    vendor.join("codex-package.json"),
                    serde_json::to_vec(&metadata).unwrap(),
                )
                .unwrap();
            }
            "mismatch" => std::fs::write(vendor.join("unexpected"), b"extra").unwrap(),
            _ => unreachable!(),
        }
        let mut cfg = HostConfig::new(
            vendor.join("bin/codex"),
            root.clone(),
            root.clone(),
            root.clone(),
        );
        cfg.expected_sha256 = Some(assessment_supplier_sha256().into());
        cfg.allow_unverified_dev = true;
        let (result, label, distribution) = Host::new().verify(0, &cfg);
        assert_eq!(result["result"], "mismatch", "{case}");
        assert_eq!(
            result["element"], "canonical .167 distribution preflight",
            "{case}"
        );
        assert!(label.is_none());
        assert!(distribution.is_empty());
    }
    // The retained source still passes after all private mutations.
    let mut cfg = HostConfig::new(source.join("bin/codex"), root.clone(), root.clone(), root);
    cfg.expected_sha256 = Some(assessment_supplier_sha256().into());
    assert!(assessment_preflight(&cfg).unwrap().is_some());
}

#[test]
fn generated_0167_removed_provider_signal_and_new_human_checkpoint_are_explicit() {
    let schema: Value = serde_json::from_str(GENERATED_SCHEMA).unwrap();
    let caps = &schema["definitions"]["v2"]["ModelProviderCapabilitiesReadResponse"];
    assert!(caps["properties"].get("namespaceTools").is_none());
    assert!(
        schema["definitions"]["InitializeCapabilities"]["properties"]
            .get("requiredHumanApproval")
            .is_some()
    );
    let mut kind_schema = schema.clone();
    kind_schema["$ref"] = json!("#/definitions/CommandExecutionApprovalKind");
    let kind = jsonschema::options().offline().build(&kind_schema).unwrap();
    for spelling in ["command", "writeStdin", "humanCommand"] {
        kind.validate(&json!(spelling)).unwrap();
    }
    assert!(kind.validate(&json!("futureKind")).is_err());
}
