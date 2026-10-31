#[path = "build_support/publisher_selection.rs"]
mod publisher_selection;
use publisher_selection::{BuildContext, Request};
use std::{env, path::PathBuf};

fn optional(name: &str) -> Result<Option<String>, String> {
    env::var(name).map(Some).or_else(|error| match error {
        env::VarError::NotPresent => Ok(None),
        _ => Err("publisher build control is not UTF-8".into()),
    })
}
fn unselected_context() -> BuildContext {
    BuildContext {
        target: String::new(),
        profile: String::new(),
        debug_assertions: true,
        development: true,
        successor: false,
        synthetic_anchor: false,
        package_name: String::new(),
        package_version: String::new(),
        features: vec![],
        application_identifier: String::new(),
        application_version: String::new(),
        tauri_config_sha256: String::new(),
    }
}
pub(crate) fn publisher_build() -> Result<(), String> {
    let out = PathBuf::from(env::var_os("OUT_DIR").ok_or("publisher output directory absent")?);
    // Clear compiler-facing Some and every companion before any fallible input
    // or configuration operation. Errors terminate this build, never reuse Some.
    publisher_selection::generate(&out, &Request::default(), &unselected_context())?;
    println!("cargo:rustc-check-cfg=cfg(chirality_publisher_selected)");
    for name in [
        "CHIRALITY_PUBLISHER_SELECTION",
        "CHIRALITY_PUBLISHER_INPUT_FILE",
        "CHIRALITY_PUBLISHER_INPUT_SHA256",
        "TAURI_CONFIG",
    ] {
        println!("cargo:rerun-if-env-changed={name}");
    }
    for file in [
        "build.rs",
        "build_support/publisher_selection.rs",
        "build_support/developer-id-application.s1.requirement-template.txt",
        "schemas/publisher-build-selection.s1.schema.json",
        "schemas/publisher-build-binding.s1.schema.json",
        "schemas/publisher-build-public-projection.s1.schema.json",
        "Cargo.toml",
        "Cargo.lock",
    ] {
        println!("cargo:rerun-if-changed={file}");
    }
    let request = Request {
        mode: optional("CHIRALITY_PUBLISHER_SELECTION")?,
        input_file: env::var_os("CHIRALITY_PUBLISHER_INPUT_FILE").map(PathBuf::from),
        input_sha256: optional("CHIRALITY_PUBLISHER_INPUT_SHA256")?,
    };
    if request.mode.is_none() {
        return publisher_selection::generate(&out, &request, &unselected_context());
    }
    // Cargo normally fingerprints input mtimes. Selected builds must re-read and
    // hash even a modified file whose mtime was restored. This never-created
    // output path keeps the selected build script dirty on each Cargo invocation.
    let recheck = out.join("publisher-selection-recheck-required");
    if recheck.exists() || recheck.is_symlink() {
        return Err(
            "unexpected publisher recheck sentinel; use a fresh build output directory".into(),
        );
    }
    println!("cargo:rerun-if-changed={}", recheck.display());
    let target = env::var("TARGET").map_err(|_| "publisher target absent")?;
    let root = PathBuf::from(
        env::var_os("CARGO_MANIFEST_DIR").ok_or("publisher manifest directory absent")?,
    );
    // Use the exact same locked parser, platform merge and overlay merge as
    // tauri-build 2.6.1. Configuration is a consistency check, not publisher input.
    let (mut config, paths) = tauri_utils::config::parse::read_from(
        tauri_utils::platform::Target::from_triple(&target),
        &root,
    )
    .map_err(|_| "publisher effective App configuration unavailable")?;
    for path in paths {
        println!("cargo:rerun-if-changed={}", path.display());
    }
    if let Some(overlay) = optional("TAURI_CONFIG")? {
        let overlay: serde_json::Value = serde_json::from_str(&overlay)
            .map_err(|_| "publisher effective App configuration overlay invalid")?;
        json_patch::merge(&mut config, &overlay);
    }
    let effective: tauri_utils::config::Config = serde_json::from_value(config.clone())
        .map_err(|_| "publisher effective App configuration invalid")?;
    // Read only this package's declared feature flags, never enumerate unrelated
    // environment values (which can contain credentials).
    let features = [
        ("custom-protocol", "CARGO_FEATURE_CUSTOM_PROTOCOL"),
        (
            "distribution-successor",
            "CARGO_FEATURE_DISTRIBUTION_SUCCESSOR",
        ),
        (
            "synthetic-distribution-anchor",
            "CARGO_FEATURE_SYNTHETIC_DISTRIBUTION_ANCHOR",
        ),
    ]
    .into_iter()
    .filter(|(_, key)| env::var_os(key).is_some())
    .map(|(feature, _)| feature.to_owned())
    .collect();
    let context = BuildContext {
        target,
        profile: env::var("PROFILE").map_err(|_| "publisher profile absent")?,
        debug_assertions: env::var_os("CARGO_CFG_DEBUG_ASSERTIONS").is_some(),
        development: tauri_build::is_dev(),
        successor: env::var_os("CARGO_FEATURE_DISTRIBUTION_SUCCESSOR").is_some(),
        synthetic_anchor: env::var_os("CARGO_FEATURE_SYNTHETIC_DISTRIBUTION_ANCHOR").is_some(),
        package_name: env::var("CARGO_PKG_NAME").map_err(|_| "publisher package name absent")?,
        package_version: env::var("CARGO_PKG_VERSION")
            .map_err(|_| "publisher package version absent")?,
        features,
        application_identifier: effective.identifier,
        application_version: effective.version.ok_or("publisher App version absent")?,
        tauri_config_sha256: publisher_selection::sha256(
            &serde_json::to_vec(&publisher_selection::ordered(config))
                .map_err(|_| "publisher effective configuration serialization failed")?,
        ),
    };
    publisher_selection::generate(&out, &request, &context)?;
    // A stale selected .rs output cannot compile into an unselected build even
    // if it was restored in OUT_DIR after Cargo last ran this script.
    println!("cargo:rustc-cfg=chirality_publisher_selected");
    Ok(())
}
fn main() {
    if let Err(reason) = publisher_build() {
        // Messages contain categories only; never emit selected values or input bytes.
        eprintln!("publisher build selection refused: {reason}");
        std::process::exit(1);
    }
    tauri_build::build()
}
