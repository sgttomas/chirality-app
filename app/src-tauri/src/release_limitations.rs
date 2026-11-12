//! The release's limitations list as shipped in the bundle (DEL-01-06 REQ-007, AC-008).
//!
//! `tauri.conf.json` maps `docs/RELEASE_LIMITATIONS_4.0.0.md` byte for byte to the bundle
//! resource [`RESOURCE_RELEASE_LIMITATIONS`]. This reads that resource and states its identity;
//! how a person reaches it inside the App is decided separately and nothing here presents it.

use crate::util::sha256_hex;
use serde_json::{json, Value};
use std::path::Path;

/// Bundle-relative path of the shipped limitations list.
pub const RESOURCE_RELEASE_LIMITATIONS: &str = "release/LIMITATIONS.md";

/// The shipped limitations list: its exact bytes and their SHA-256.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ReleaseLimitations {
    pub bytes: Vec<u8>,
    pub sha256: String,
}

/// Read the limitations list from a resource directory. A missing, unreadable or
/// non-file resource is an error, never an empty list.
pub fn read(resource_root: &Path) -> Result<ReleaseLimitations, String> {
    read_file(&resource_root.join(RESOURCE_RELEASE_LIMITATIONS))
}

/// Read the limitations list at its resolved resource path.
pub fn read_file(path: &Path) -> Result<ReleaseLimitations, String> {
    let meta = std::fs::symlink_metadata(path)
        .map_err(|e| format!("release limitations resource unavailable: {e}"))?;
    if !meta.file_type().is_file() {
        return Err("release limitations resource is not a regular file".into());
    }
    let bytes = std::fs::read(path).map_err(|e| format!("release limitations resource unreadable: {e}"))?;
    let sha256 = sha256_hex(&bytes);
    Ok(ReleaseLimitations { bytes, sha256 })
}

/// The reply a host caller receives for the resolved resource path: UTF-8 text when the bytes
/// are UTF-8, and the identity of the exact bytes read either way.
pub fn reply(path: &Path) -> Result<Value, String> {
    let limitations = read_file(path)?;
    let text = std::str::from_utf8(&limitations.bytes).ok();
    Ok(json!({"resource": RESOURCE_RELEASE_LIMITATIONS, "sha256": limitations.sha256,
              "size": limitations.bytes.len(), "text": text}))
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::path::PathBuf;

    fn temp(name: &str) -> PathBuf {
        let dir = std::env::temp_dir().join(format!("release-limitations-{name}-{}", std::process::id()));
        let _ = std::fs::remove_dir_all(&dir);
        std::fs::create_dir_all(dir.join("release")).unwrap();
        dir
    }

    #[test]
    fn reads_exact_bytes_and_their_sha256() {
        let root = temp("read");
        let raw = b"# Invented limitations\n\n- invented entry\n";
        std::fs::write(root.join(RESOURCE_RELEASE_LIMITATIONS), raw).unwrap();
        let read = read(&root).unwrap();
        assert_eq!(read.bytes, raw);
        assert_eq!(read.sha256, sha256_hex(raw));
        let reply = reply(&root.join(RESOURCE_RELEASE_LIMITATIONS)).unwrap();
        assert_eq!(reply["sha256"], sha256_hex(raw));
        assert_eq!(reply["text"], std::str::from_utf8(raw).unwrap());
        assert_eq!(reply["size"], raw.len());
        std::fs::remove_dir_all(&root).unwrap();
    }

    #[test]
    fn missing_or_non_file_resource_is_an_error() {
        let root = temp("missing");
        assert!(read(&root).is_err());
        std::fs::create_dir(root.join(RESOURCE_RELEASE_LIMITATIONS)).unwrap();
        assert!(read(&root).is_err());
        std::fs::remove_dir_all(&root).unwrap();
    }

    #[cfg(unix)]
    #[test]
    fn symbolic_link_resource_is_refused() {
        let root = temp("link");
        std::fs::write(root.join("elsewhere.md"), b"x").unwrap();
        std::os::unix::fs::symlink(root.join("elsewhere.md"), root.join(RESOURCE_RELEASE_LIMITATIONS)).unwrap();
        assert!(read(&root).is_err());
        std::fs::remove_dir_all(&root).unwrap();
    }

    /// The source tree's mapped file is what the host would read once bundled.
    #[test]
    fn source_document_is_readable_as_the_resource() {
        let docs = Path::new(env!("CARGO_MANIFEST_DIR")).join("../../docs/RELEASE_LIMITATIONS_4.0.0.md");
        let root = temp("source");
        std::fs::copy(&docs, root.join(RESOURCE_RELEASE_LIMITATIONS)).unwrap();
        assert_eq!(read(&root).unwrap().sha256, sha256_hex(&std::fs::read(&docs).unwrap()));
        std::fs::remove_dir_all(&root).unwrap();
    }
}
