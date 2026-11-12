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
    read_beneath(resource_root, RESOURCE_RELEASE_LIMITATIONS)
}

/// Read `relative` beneath `resource_root` without following a link in any component beneath
/// the resource directory: each directory is opened relative to its parent's descriptor with
/// `O_NOFOLLOW`, the leaf likewise, and the bytes come from that one descriptor after its own
/// metadata shows a regular file.
#[cfg(unix)]
pub fn read_beneath(resource_root: &Path, relative: &str) -> Result<ReleaseLimitations, String> {
    use std::ffi::CString;
    use std::fs::File;
    use std::io::Read;
    use std::os::unix::fs::OpenOptionsExt;
    use std::os::unix::io::{AsRawFd, FromRawFd};
    let parts = relative_parts(relative)?;
    let mut dir = std::fs::OpenOptions::new()
        .read(true)
        .custom_flags(libc::O_DIRECTORY | libc::O_CLOEXEC)
        .open(resource_root)
        .map_err(|e| format!("release limitations resource directory unavailable: {e}"))?;
    for (at, part) in parts.iter().enumerate() {
        let last = at + 1 == parts.len();
        let name = CString::new(part.as_bytes()).map_err(|_| "resource name contains NUL")?;
        let flags = libc::O_RDONLY | libc::O_NOFOLLOW | libc::O_CLOEXEC | libc::O_NONBLOCK
            | if last { 0 } else { libc::O_DIRECTORY };
        // SAFETY: `dir` is an open descriptor and `name` a NUL-terminated component.
        let fd = unsafe { libc::openat(dir.as_raw_fd(), name.as_ptr(), flags) };
        if fd < 0 {
            let error = std::io::Error::last_os_error();
            return Err(if error.raw_os_error() == Some(libc::ELOOP) || error.raw_os_error() == Some(libc::ENOTDIR) {
                "release limitations resource path holds a link or a non-directory; refused".into()
            } else {
                format!("release limitations resource unavailable: {error}")
            });
        }
        // SAFETY: `fd` was just returned by openat and is owned here.
        dir = unsafe { File::from_raw_fd(fd) };
    }
    let meta = dir.metadata().map_err(|e| format!("release limitations resource unreadable: {e}"))?;
    if !meta.file_type().is_file() {
        return Err("release limitations resource is not a regular file".into());
    }
    let mut bytes = Vec::with_capacity(meta.len() as usize);
    dir.read_to_end(&mut bytes).map_err(|e| format!("release limitations resource unreadable: {e}"))?;
    let sha256 = sha256_hex(&bytes);
    Ok(ReleaseLimitations { bytes, sha256 })
}

/// Without descriptor-relative opens, refuse a link in any component before reading. This check
/// is not free of a race between check and open; macOS is the release target.
#[cfg(not(unix))]
pub fn read_beneath(resource_root: &Path, relative: &str) -> Result<ReleaseLimitations, String> {
    let mut path = resource_root.to_path_buf();
    for part in relative_parts(relative)? {
        path.push(part);
        let meta = std::fs::symlink_metadata(&path)
            .map_err(|e| format!("release limitations resource unavailable: {e}"))?;
        if meta.file_type().is_symlink() {
            return Err("release limitations resource path holds a link; refused".into());
        }
    }
    if !std::fs::symlink_metadata(&path).map_err(|e| e.to_string())?.file_type().is_file() {
        return Err("release limitations resource is not a regular file".into());
    }
    let bytes = std::fs::read(&path).map_err(|e| format!("release limitations resource unreadable: {e}"))?;
    let sha256 = sha256_hex(&bytes);
    Ok(ReleaseLimitations { bytes, sha256 })
}

fn relative_parts(relative: &str) -> Result<Vec<&str>, String> {
    let parts: Vec<&str> = relative.split('/').collect();
    if parts.iter().any(|p| p.is_empty() || *p == "." || *p == "..") {
        return Err("resource path must be plain and relative".into());
    }
    Ok(parts)
}

/// The reply a host caller receives: UTF-8 text when the bytes are UTF-8, and the identity of
/// the exact bytes read either way.
pub fn reply(resource_root: &Path, relative: &str) -> Result<Value, String> {
    let limitations = read_beneath(resource_root, relative)?;
    let text = std::str::from_utf8(&limitations.bytes).ok();
    Ok(json!({"resource": relative, "sha256": limitations.sha256,
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
        let reply = reply(&root, RESOURCE_RELEASE_LIMITATIONS).unwrap();
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

    #[cfg(unix)]
    #[test]
    fn linked_directory_component_is_refused() {
        let root = temp("dirlink");
        let outside = temp("dirlink-outside");
        std::fs::write(outside.join("release/LIMITATIONS.md"), b"invented outside text\n").unwrap();
        std::fs::remove_dir(root.join("release")).unwrap();
        std::os::unix::fs::symlink(outside.join("release"), root.join("release")).unwrap();
        assert!(read(&root).unwrap_err().contains("link"));
        std::fs::remove_dir_all(&root).unwrap();
        std::fs::remove_dir_all(&outside).unwrap();
    }

    #[cfg(unix)]
    #[test]
    fn linked_leaf_to_outside_file_is_refused() {
        let root = temp("leaflink");
        let outside = temp("leaflink-outside");
        std::fs::write(outside.join("text.md"), b"invented outside text\n").unwrap();
        std::os::unix::fs::symlink(outside.join("text.md"), root.join(RESOURCE_RELEASE_LIMITATIONS)).unwrap();
        assert!(read(&root).unwrap_err().contains("link"));
        std::fs::remove_dir_all(&root).unwrap();
        std::fs::remove_dir_all(&outside).unwrap();
    }

    #[test]
    fn non_plain_relative_path_is_refused() {
        let root = temp("plain");
        for bad in ["../release/LIMITATIONS.md", "release//LIMITATIONS.md", "/release/LIMITATIONS.md", "release/./LIMITATIONS.md"] {
            assert!(read_beneath(&root, bad).is_err(), "{bad}");
        }
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
