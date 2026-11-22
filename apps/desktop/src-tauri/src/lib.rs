//! The Chirality App's Rust side: the engine's adapter on the Tauri builder,
//! the desktop plugins the interface uses, and the engine's setup on this machine.

use std::path::{Path, PathBuf};

use chirality_engine_tauri::chirality_engine::EngineConfig;
use tauri::{AppHandle, Manager, Runtime};

/// The engine's setup. `CHIRALITY_CODEX_BIN` names the pinned Codex (by
/// default the bundled package's entrypoint); `CHIRALITY_WORKFLOW_ROOTS`
/// (a `:`-separated list) replaces the bundled Library edition. Codex uses the
/// person's own home, or `CODEX_HOME`.
fn config<R: Runtime>(app: &AppHandle<R>) -> Result<EngineConfig, Box<dyn std::error::Error>> {
    let resources = app.path().resource_dir()?;
    let codex_bin = std::env::var_os("CHIRALITY_CODEX_BIN").map(PathBuf::from).unwrap_or_else(|| codex(&resources.join("codex")));
    let workflow_roots = match std::env::var_os("CHIRALITY_WORKFLOW_ROOTS") {
        Some(roots) => std::env::split_paths(&roots).collect(),
        None => library(&resources.join("library")),
    };
    Ok(EngineConfig {
        codex_bin,
        codex_home: None,
        state_dir: app.path().app_data_dir()?,
        workflow_roots,
        codex_settings: Vec::new(),
        tools: None,
    })
}

/// The pinned Library edition (`library.json`).
const EDITION: &str = env!("CHIRALITY_LIBRARY_TAG");

/// The pinned Codex (`codex.json`): its package's folder and entrypoint.
const CODEX: &str = env!("CHIRALITY_CODEX_TAG");
const CODEX_ENTRYPOINT: &str = env!("CHIRALITY_CODEX_ENTRYPOINT");

/// The bundled Codex package's entrypoint, `codex/<the pinned package>/bin/codex`.
fn codex(dir: &Path) -> PathBuf {
    dir.join(CODEX).join(CODEX_ENTRYPOINT)
}

/// The bundled Library edition's workflows, `library/<the pinned edition>/workflows`, and no other edition's.
fn library(dir: &Path) -> Vec<PathBuf> {
    let workflows = dir.join(EDITION).join("workflows");
    if workflows.is_dir() { vec![workflows] } else { Vec::new() }
}

pub fn run() {
    tauri::Builder::default()
        .plugin(chirality_engine_tauri::plugin(config))
        .invoke_handler(chirality_engine_tauri::commands(|_| false))
        .plugin(tauri_plugin_dialog::init())
        .plugin(tauri_plugin_notification::init())
        .plugin(tauri_plugin_opener::init())
        .run(tauri::generate_context!())
        .expect("the app starts");
}

#[cfg(test)]
mod tests {
    #[test]
    fn the_bundled_library_is_the_pinned_editions_workflows_only() {
        let edition = std::fs::read_to_string(concat!(env!("CARGO_MANIFEST_DIR"), "/../library.json")).unwrap();
        assert!(edition.contains(&format!("\"tag\": \"{}\"", super::EDITION)), "the pinned edition is library.json's");
        let dir = std::env::temp_dir().join(format!("chirality-app-library-{}", std::process::id()));
        std::fs::create_dir_all(dir.join(super::EDITION).join("workflows")).unwrap();
        std::fs::create_dir_all(dir.join("library-v9.9.9/workflows")).unwrap();
        std::fs::create_dir_all(dir.join("stray")).unwrap();
        assert_eq!(super::library(&dir), vec![dir.join(super::EDITION).join("workflows")]);
        assert!(super::library(&dir.join("absent")).is_empty());
        std::fs::remove_dir_all(dir).unwrap();
    }

    #[test]
    fn the_bundled_codex_is_the_pinned_packages_entrypoint() {
        let pin = std::fs::read_to_string(concat!(env!("CARGO_MANIFEST_DIR"), "/../codex.json")).unwrap();
        assert!(pin.contains(&format!("\"tag\": \"{}\"", super::CODEX)), "the pinned package is codex.json's");
        assert!(pin.contains("\"entrypoint\": \"bin/codex\""), "its entrypoint is codex.json's");
        let dir = std::path::Path::new("/resources/codex");
        assert_eq!(super::codex(dir), dir.join(super::CODEX).join("bin").join("codex"));
    }
}
