//! Explicit, synthetic startup observation. Never a current trust or supplier gate.
#[cfg(all(feature = "synthetic-distribution-anchor", not(debug_assertions)))]
compile_error!(
    "synthetic-distribution-anchor is debug-only and must not be enabled in release builds"
);

use serde_json::{json, Value};
use std::path::PathBuf;

pub(crate) fn observe_startup(resource_dir: impl FnOnce() -> Result<PathBuf, String>) -> Value {
    #[cfg(all(feature = "synthetic-distribution-anchor", debug_assertions))]
    {
        let result = resource_dir()
            .and_then(|root| enabled::check(&root.join("distribution-development-reference")));
        match result {
            Ok(inventory) => {
                json!({"standing":"development-unverifiable","observedAt":"app-startup","outcome":"compiled-bytes-matched","currentTrust":false,"productionAvailable":crate::distribution_preflight::production_available(),"inventory":inventory,"modePolicy":"modes observed only; no mode acceptance or integrity claim"})
            }
            Err(reason) => {
                json!({"standing":"development-unverifiable","observedAt":"app-startup","outcome":"refused","currentTrust":false,"reason":reason})
            }
        }
    }
    #[cfg(not(all(feature = "synthetic-distribution-anchor", debug_assertions)))]
    {
        let _ = resource_dir;
        json!({"standing":"disabled","observedAt":"app-startup","currentTrust":false})
    }
}

#[cfg(all(feature = "synthetic-distribution-anchor", debug_assertions))]
mod enabled {
    use crate::distribution_preflight::{digest, scan, Inventory};
    use std::path::Path;
    pub(super) const FILES: [(&str, &[u8]); 4] = [
        (
            "build-selection.s2.json",
            include_bytes!(
                "../resources/distribution-development-reference/build-selection.s2.json"
            ),
        ),
        (
            "expected.json",
            include_bytes!("../resources/distribution-successor/synthetic-expected.json"),
        ),
        (
            "attestation.json",
            include_bytes!("../resources/distribution-successor/synthetic-attestation.json"),
        ),
        (
            "synthetic-evidence.json",
            include_bytes!("../resources/distribution-successor/synthetic-evidence.json"),
        ),
    ];
    pub(super) fn check(root: &Path) -> Result<Inventory, String> {
        let inventory = scan(root)?;
        if inventory.entries.len() != FILES.len() + 1
            || !inventory
                .entries
                .iter()
                .any(|e| e.path == "." && e.kind == "dir")
        {
            return Err("synthetic startup resource set is not the closed four-file set".into());
        }
        for (path, bytes) in FILES {
            let entry = inventory
                .entries
                .iter()
                .find(|e| e.path == path)
                .ok_or("synthetic startup resource missing")?;
            if entry.kind != "file"
                || entry.size != Some(bytes.len() as u64)
                || entry.sha256.as_deref() != Some(digest(bytes).as_str())
            {
                return Err("synthetic startup resource differs from compiled bytes".into());
            }
        }
        Ok(inventory)
    }
}

#[cfg(test)]
#[path = "compiled_development_selection_tests.rs"]
mod tests;
