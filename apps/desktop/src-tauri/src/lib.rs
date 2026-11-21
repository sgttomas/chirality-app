//! The Chirality App's Rust side: the engine's adapter on the Tauri builder,
//! the desktop plugins the interface uses, and the engine's setup on this machine.

use std::path::{Path, PathBuf};

use chirality_engine_tauri::chirality_engine::EngineConfig;
use tauri::{AppHandle, Manager, Runtime};

/// The engine's setup. `CHIRALITY_CODEX_BIN` names the pinned Codex (by
/// default `codex` among the app's resources); `CHIRALITY_WORKFLOW_ROOTS`
/// (a `:`-separated list) replaces the bundled Library. Codex uses the
/// person's own home, or `CODEX_HOME`.
fn config<R: Runtime>(app: &AppHandle<R>) -> Result<EngineConfig, Box<dyn std::error::Error>> {
    let resources = app.path().resource_dir()?;
    let codex_bin = std::env::var_os("CHIRALITY_CODEX_BIN").map(PathBuf::from).unwrap_or_else(|| resources.join("codex"));
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

/// The bundled Library edition's workflows: `library/<edition>/workflows`.
fn library(dir: &Path) -> Vec<PathBuf> {
    let Ok(entries) = std::fs::read_dir(dir) else { return Vec::new() };
    let mut roots: Vec<PathBuf> = entries.filter_map(|e| Some(e.ok()?.path().join("workflows"))).filter(|p| p.is_dir()).collect();
    roots.sort();
    roots
}

pub fn run() {
    tauri::Builder::default()
        .plugin(chirality_engine_tauri::plugin(|app| config(app)))
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
    fn the_bundled_library_is_each_editions_workflows() {
        let dir = std::env::temp_dir().join(format!("chirality-app-library-{}", std::process::id()));
        std::fs::create_dir_all(dir.join("library-v3.4.0/workflows")).unwrap();
        std::fs::create_dir_all(dir.join("stray")).unwrap();
        assert_eq!(super::library(&dir), vec![dir.join("library-v3.4.0/workflows")]);
        assert!(super::library(&dir.join("absent")).is_empty());
        std::fs::remove_dir_all(dir).unwrap();
    }
}
