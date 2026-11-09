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
        "158dd67072236253a694ca06d9bf7bfdebbe20d4a197bbf675433cbdddea7e7b"
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
    // The npm tree's main equals the canonical main, but package bytes differ.
    assert_eq!(
        expected
            .entries
            .iter()
            .find(|e| e.path == "bin/codex")
            .unwrap()
            .sha256
            .as_deref(),
        Some(ASSESSMENT_SUPPLIER_SHA256)
    );
    assert_eq!(
        basis()["package_metadata"]["execServer"],
        "bin/codex-exec-server"
    );
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
            "#!/bin/sh\ntouch '{}'\necho 'codex-cli 0.167.0'\n",
            marker.display()
        ),
    )
    .unwrap();
    std::fs::set_permissions(&main, std::fs::Permissions::from_mode(0o755)).unwrap();
    let mut cfg = HostConfig::new(main, root.clone(), root.clone(), root.clone());
    cfg.expected_sha256 = Some(ASSESSMENT_SUPPLIER_SHA256.into());
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
    cfg.expected_sha256 = Some(ASSESSMENT_SUPPLIER_SHA256.into());
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
        cfg.expected_sha256 = Some(ASSESSMENT_SUPPLIER_SHA256.into());
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
    cfg.expected_sha256 = Some(ASSESSMENT_SUPPLIER_SHA256.into());
    assert!(assessment_preflight(&cfg).unwrap().is_some());
}

#[test]
fn generated_0167_removed_provider_signal_and_new_human_checkpoint_are_explicit() {
    let schema: Value = serde_json::from_str(include_str!(
        "../resources/supplier/0.167.0/codex_app_server_protocol.schemas.json"
    ))
    .unwrap();
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
