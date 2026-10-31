// Actual build recipe, executed only inside an isolated synthetic test process.
use super::*;
use std::os::unix::fs::PermissionsExt;
use std::{fs, process::Command};
fn invoke(root: &std::path::Path, stage: &str, digest: &str) -> std::process::Output {
    let mut cmd = Command::new(std::env::current_exe().unwrap());
    cmd.env_clear().args(["--exact","publisher_selection::tests::recipe::publisher_actual_recipe_selected_none_changed_and_debug","--nocapture"])
        .env("SYNTHETIC_PUBLISHER_RECIPE_CHILD",stage)
        .env("OUT_DIR",root.join("out"))
        .env("CARGO_MANIFEST_DIR",env!("CARGO_MANIFEST_DIR"))
        .env("TARGET","aarch64-apple-darwin").env("PROFILE","release")
        .env("DEP_TAURI_DEV","false").env("CARGO_FEATURE_DISTRIBUTION_SUCCESSOR","1")
        .env("CARGO_FEATURE_CUSTOM_PROTOCOL","1")
        .env("CARGO_PKG_NAME","chirality-app-v4").env("CARGO_PKG_VERSION",env!("CARGO_PKG_VERSION"))
        .env("TAURI_CONFIG",r#"{"identifier":"invalid.example.synthetic","version":"0.0.0-synthetic"}"#);
    if stage != "none" {
        cmd.env("CHIRALITY_PUBLISHER_SELECTION", "production-v1")
            .env("CHIRALITY_PUBLISHER_INPUT_FILE", root.join("input.json"))
            .env("CHIRALITY_PUBLISHER_INPUT_SHA256", digest);
    }
    if stage == "debug" {
        cmd.env("PROFILE", "debug")
            .env("CARGO_CFG_DEBUG_ASSERTIONS", "");
    }
    if stage == "dev" {
        cmd.env("DEP_TAURI_DEV", "true");
    }
    if stage == "config-mismatch" {
        cmd.env_remove("TAURI_CONFIG");
    }
    cmd.output().unwrap()
}
#[test]
fn publisher_actual_recipe_selected_none_changed_and_debug() {
    if let Ok(stage) = std::env::var("SYNTHETIC_PUBLISHER_RECIPE_CHILD") {
        let result = crate::publisher_recipe::publisher_build();
        if matches!(stage.as_str(), "selected" | "none") {
            result.unwrap();
        } else {
            assert!(result.is_err());
        }
        return;
    }
    let root = std::env::temp_dir()
        .canonicalize()
        .unwrap()
        .join(crate::util::opaque_id("publisher-recipe-").unwrap());
    fs::create_dir_all(root.join("out")).unwrap();
    let input=br#"{"format":"publisher-build-selection.s1","production_bundle_identifier":"invalid.example.synthetic","developer_id_team_identifier":"SYNTHETIC0"}"#;
    fs::write(root.join("input.json"), input).unwrap();
    fs::set_permissions(root.join("input.json"), fs::Permissions::from_mode(0o600)).unwrap();
    let digest = hash(input);
    let output = invoke(&root, "selected", &digest);
    assert!(
        output.status.success(),
        "{}",
        String::from_utf8_lossy(&output.stderr)
    );
    assert!(
        String::from_utf8_lossy(&output.stdout).contains("publisher-selection-recheck-required")
    );
    assert!(String::from_utf8_lossy(&output.stdout)
        .lines()
        .any(|line| line == "cargo:rustc-cfg=chirality_publisher_selected"));
    let private = fs::read_to_string(root.join("out/publisher-build-binding.s1.json")).unwrap();
    let public =
        fs::read_to_string(root.join("out/publisher-build-public-projection.s1.json")).unwrap();
    let requirement = fs::read_to_string(root.join("out/publisher-requirement.txt")).unwrap();
    validate_artifacts(
        &requirement,
        &private,
        &hash(private.as_bytes()),
        &public,
        &hash(public.as_bytes()),
    )
    .unwrap();
    assert!(validate_artifacts(
        "always",
        &private,
        &hash(private.as_bytes()),
        &public,
        &hash(public.as_bytes())
    )
    .is_err());
    let pretty =
        serde_json::to_string_pretty(&serde_json::from_str::<Value>(&private).unwrap()).unwrap();
    assert!(validate_artifacts(
        &requirement,
        &pretty,
        &hash(private.as_bytes()),
        &public,
        &hash(public.as_bytes())
    )
    .is_err());
    let mut altered: Value = serde_json::from_str(&private).unwrap();
    altered["template_sha256"] = json!("0".repeat(64));
    let altered = serde_json::to_string(&altered).unwrap();
    assert!(validate_artifacts(
        &requirement,
        &altered,
        &hash(altered.as_bytes()),
        &public,
        &hash(public.as_bytes())
    )
    .is_err());
    let parsed: Value = serde_json::from_str(&private).unwrap();
    assert_eq!(
        parsed["build_context"]["application_version"],
        "0.0.0-synthetic"
    );
    assert!(!public.contains("SYNTHETIC0"));
    assert!(!public.contains("invalid.example.synthetic"));
    for stage in [
        "none",
        "debug",
        "dev",
        "changed",
        "missing",
        "config-mismatch",
    ] {
        fs::write(root.join("input.json"), input).unwrap();
        fs::set_permissions(root.join("input.json"), fs::Permissions::from_mode(0o600)).unwrap();
        let selected = invoke(&root, "selected", &digest);
        assert!(
            selected.status.success(),
            "{stage}: {}",
            String::from_utf8_lossy(&selected.stderr)
        );
        if stage == "changed" {
            fs::write(root.join("input.json"), b"changed").unwrap();
        }
        if stage == "missing" {
            fs::remove_file(root.join("input.json")).unwrap();
        }
        let output = invoke(&root, stage, &digest);
        assert!(
            output.status.success(),
            "{stage}: {}",
            String::from_utf8_lossy(&output.stderr)
        );
        assert!(
            !String::from_utf8_lossy(&output.stdout)
                .lines()
                .any(|line| line == "cargo:rustc-cfg=chirality_publisher_selected"),
            "{stage}"
        );
        let generated = fs::read_to_string(root.join("out/publisher_selection.rs")).unwrap();
        assert!(!generated.contains("= Some("), "{stage}");
        assert_eq!(
            fs::read_to_string(root.join("out/publisher-build-binding.s1.json")).unwrap(),
            "null\n"
        );
        assert_eq!(
            fs::read_to_string(root.join("out/publisher-build-public-projection.s1.json")).unwrap(),
            "null\n"
        );
    }
    // Changed bytes with a refreshed digest still cannot inject requirement logic.
    for bad in [
        r#"{"format":"publisher-build-selection.s1","production_bundle_identifier":"invalid.example.synthetic","developer_id_team_identifier":"SYNTHETIC0","requirement":"always"}"#,
        r#"{"format":"publisher-build-selection.s1","production_bundle_identifier":"invalid.example.synthetic\" or true","developer_id_team_identifier":"SYNTHETIC0"}"#,
    ] {
        fs::write(root.join("input.json"), bad).unwrap();
        fs::set_permissions(root.join("input.json"), fs::Permissions::from_mode(0o600)).unwrap();
        assert!(invoke(&root, "invalid", &hash(bad.as_bytes()))
            .status
            .success());
    }
    fs::remove_dir_all(root).unwrap();
}
#[cfg(target_os = "macos")]
#[test]
fn publisher_independent_requirement_template_parses_without_signing() {
    use std::{
        ffi::{c_void, CString},
        ptr,
    };
    type Ref = *const c_void;
    #[link(name = "CoreFoundation", kind = "framework")]
    extern "C" {
        fn CFStringCreateWithCString(a: Ref, s: *const std::ffi::c_char, encoding: u32) -> Ref;
        fn CFRelease(value: Ref);
    }
    #[link(name = "Security", kind = "framework")]
    extern "C" {
        fn SecRequirementCreateWithString(text: Ref, flags: u32, output: *mut Ref) -> i32;
    }
    let text =
        include_str!("../build_support/developer-id-application.s1.requirement-template.txt")
            .replace(
                "{{production_bundle_identifier}}",
                "\"invalid.example.synthetic\"",
            )
            .replace("{{developer_id_team_identifier}}", "\"SYNTHETIC0\"");
    let c = CString::new(text).unwrap();
    unsafe {
        let string = CFStringCreateWithCString(ptr::null(), c.as_ptr(), 0x08000100);
        assert!(!string.is_null());
        let mut requirement = ptr::null();
        let result = SecRequirementCreateWithString(string, 0, &mut requirement);
        CFRelease(string);
        assert_eq!(result, 0, "synthetic independent requirement syntax");
        assert!(!requirement.is_null());
        CFRelease(requirement);
    }
}

#[cfg(all(target_os = "macos", target_arch = "aarch64"))]
#[test]
fn publisher_generated_source_compiler_refuses_debug_dev_and_missing_features() {
    let root = std::env::temp_dir()
        .canonicalize()
        .unwrap()
        .join(crate::util::opaque_id("publisher-compiler-").unwrap());
    fs::create_dir_all(root.join("out")).unwrap();
    let input = br#"{"format":"publisher-build-selection.s1","production_bundle_identifier":"invalid.example.synthetic","developer_id_team_identifier":"SYNTHETIC0"}"#;
    fs::write(root.join("input.json"), input).unwrap();
    fs::set_permissions(root.join("input.json"), fs::Permissions::from_mode(0o600)).unwrap();
    assert!(invoke(&root, "selected", &hash(input)).status.success());
    let compile = |kind: &str| {
        let mut command = Command::new(std::env::var_os("RUSTC").unwrap_or_else(|| "rustc".into()));
        command
            .arg(root.join("out/publisher_selection.rs"))
            .args([
                "--crate-name",
                "synthetic_publisher",
                "--crate-type",
                "lib",
                "--emit",
                "metadata",
                "--edition",
                "2021",
                "-Adead_code",
            ])
            .arg("-o")
            .arg(root.join("synthetic.rmeta"))
            .arg("-C")
            .arg(if kind == "debug" {
                "debug-assertions=yes"
            } else {
                "debug-assertions=no"
            });
        if kind != "missing-feature" {
            command.args([
                "--cfg",
                "feature=\"distribution-successor\"",
                "--cfg",
                "feature=\"custom-protocol\"",
            ]);
        }
        if matches!(kind, "dev" | "test") {
            command.args(["--cfg", kind]);
        }
        if kind != "unselected-build" {
            command.args(["--cfg", "chirality_publisher_selected"]);
        }
        if kind == "synthetic-anchor" {
            command.args(["--cfg", "feature=\"synthetic-distribution-anchor\""]);
        }
        command.output().unwrap()
    };
    let production = compile("production");
    assert!(
        production.status.success(),
        "{}",
        String::from_utf8_lossy(&production.stderr)
    );
    for kind in [
        "debug",
        "dev",
        "test",
        "missing-feature",
        "unselected-build",
        "synthetic-anchor",
    ] {
        let result = compile(kind);
        assert!(!result.status.success(), "{kind}");
        assert!(String::from_utf8_lossy(&result.stderr)
            .contains("publisher selection requires a production"));
    }
    assert!(invoke(&root, "none", &hash(input)).status.success());
    assert!(compile("debug").status.success());
    assert!(compile("unselected-build").status.success());
    fs::remove_dir_all(root).unwrap();
}
