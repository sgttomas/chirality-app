//! Selected RS §13.7 App-local owning paths; keys do not encode governed IDs.
use crate::{records, util::sha256_hex};
use serde_json::Value;
use std::os::fd::AsRawFd;
use std::{
    fs::{File, OpenOptions},
    io::Write,
    path::{Path, PathBuf},
};
pub const LEGACY_LOG: &str = "records/coordination.rs.jsonl";
pub const CAPTURES: &str = ".chirality/captures";
pub fn key(identity: &str) -> String {
    sha256_hex(identity.as_bytes())
}
pub fn project_log(root: &Path, run: Option<&str>, writer: &str) -> PathBuf {
    match run {
        Some(run) => root
            .join(".chirality/records/runs")
            .join(key(run))
            .join(format!("{}.jsonl", key(writer))),
        None => root
            .join(".chirality/records/acts")
            .join(format!("{}.jsonl", key(writer))),
    }
}
pub fn library_log(library: &Path) -> PathBuf {
    library.join(".chirality/records/acts.jsonl")
}
pub fn capture_path(root: &Path, id: &str) -> PathBuf {
    root.join(CAPTURES).join(format!("{}.json", key(id)))
}
pub fn pending_path(root: &Path, id: &str) -> PathBuf {
    root.join(CAPTURES)
        .join("pending")
        .join(format!("{}.json", key(id)))
}
/// Reject symlinks rather than silently following an owning path outside its root.
pub fn check_path(path: &Path) -> Result<(), String> {
    for ancestor in path.ancestors() {
        if let Ok(meta) = std::fs::symlink_metadata(ancestor) {
            if meta.file_type().is_symlink() {
                return Err(format!(
                    "owning path contains symlink: {}",
                    ancestor.display()
                ));
            }
        }
    }
    Ok(())
}
pub struct Ownership(File);
impl Drop for Ownership {
    fn drop(&mut self) {
        unsafe {
            libc::flock(self.0.as_raw_fd(), libc::LOCK_UN);
        }
    }
}
pub fn lock(path: &Path) -> Result<Ownership, String> {
    check_path(path)?;
    ensure_directory(path.parent().ok_or("lock has no parent")?)?;
    let file = OpenOptions::new()
        .read(true)
        .write(true)
        .create(true)
        .truncate(false)
        .open(path)
        .map_err(|e| format!("owning lock: {e}"))?;
    if unsafe { libc::flock(file.as_raw_fd(), libc::LOCK_EX) } != 0 {
        return Err(format!("owning lock: {}", std::io::Error::last_os_error()));
    }
    Ok(Ownership(file))
}
#[cfg(test)]
thread_local! { static FAIL_DIRECTORY: std::cell::RefCell<Option<PathBuf>> = const { std::cell::RefCell::new(None) }; }
#[cfg(test)]
pub(crate) fn fail_directory_for_test(path: Option<PathBuf>) {
    FAIL_DIRECTORY.with(|p| *p.borrow_mut() = path);
}
pub fn sync_dir(path: &Path) -> Result<(), String> {
    #[cfg(test)]
    if FAIL_DIRECTORY.with(|p| p.borrow().as_deref() == Some(path)) {
        return Err("directory sync: injected failure".into());
    }
    File::open(path)
        .and_then(|f| f.sync_all())
        .map_err(|e| format!("directory sync: {}: {e}", path.display()))
}
/// Persist each newly created directory and its link in the pre-existing ancestor.
pub fn ensure_directory(path: &Path) -> Result<(), String> {
    check_path(path)?;
    let mut missing = vec![];
    let mut ancestor = path;
    while !ancestor.exists() {
        missing.push(ancestor.to_path_buf());
        ancestor = ancestor
            .parent()
            .ok_or("directory has no existing ancestor")?;
    }
    std::fs::create_dir_all(path).map_err(|e| format!("owning directory: {e}"))?;
    for created in &missing {
        sync_dir(created)?;
    }
    if !missing.is_empty() {
        sync_dir(ancestor)?;
    }
    Ok(())
}
/// Re-establish complete publication durability up through the owning project/library root.
pub fn sync_publication(path: &Path) -> Result<(), String> {
    check_path(path)?;
    File::open(path)
        .and_then(|f| f.sync_all())
        .map_err(|e| format!("file sync uncertain: {e}"))?;
    let boundary = path
        .ancestors()
        .find(|p| p.file_name().is_some_and(|n| n == ".chirality"))
        .and_then(Path::parent);
    let parent = path.parent().ok_or("publication has no parent")?;
    let boundary = boundary.or_else(|| {
        (path
            .file_name()
            .is_some_and(|n| n == "coordination.rs.jsonl")
            && parent.file_name().is_some_and(|n| n == "records"))
        .then(|| parent.parent())
        .flatten()
    });
    for dir in parent.ancestors() {
        sync_dir(dir)?;
        if Some(dir) == boundary || boundary.is_none() {
            break;
        }
    }
    Ok(())
}
fn publish_json(
    path: &Path,
    value: &Value,
    replace: bool,
    write: impl FnOnce(&mut File, &[u8]) -> Result<(), String>,
) -> Result<(), String> {
    check_path(path)?;
    let parent = path.parent().ok_or("evidence has no parent")?;
    ensure_directory(parent)?;
    let mut bytes = serde_json::to_vec_pretty(value).map_err(|e| e.to_string())?;
    bytes.push(b'\n');
    let temp = parent.join(format!(
        ".{}.{}.tmp",
        path.file_name().unwrap().to_string_lossy(),
        crate::util::opaque_id("")?
    ));
    let result = (|| {
        let mut file = OpenOptions::new()
            .create_new(true)
            .write(true)
            .open(&temp)
            .map_err(|e| format!("temporary evidence: {e}"))?;
        write(&mut file, &bytes)?;
        file.sync_all()
            .map_err(|e| format!("temporary evidence sync: {e}"))?;
        // hard_link publishes complete bytes atomically with create-new semantics.
        if replace {
            std::fs::rename(&temp, path).map_err(|e| format!("annotation publication: {e}"))?;
        } else {
            std::fs::hard_link(&temp, path)
                .map_err(|e| format!("create-once evidence publication: {e}"))?;
        }
        sync_publication(path)?;
        Ok(())
    })();
    if temp.exists() {
        let _ = std::fs::remove_file(&temp);
        let _ = sync_dir(parent);
    }
    result
}
pub fn create_json(path: &Path, value: &Value) -> Result<(), String> {
    publish_json(path, value, false, |file, bytes| {
        file.write_all(bytes)
            .map_err(|e| format!("temporary evidence write: {e}"))
    })
}
/// Atomic mutable writer metadata/sole backlink annotation; caller holds owning lock.
pub(crate) fn replace_json(path: &Path, value: &Value) -> Result<(), String> {
    publish_json(path, value, true, |file, bytes| {
        file.write_all(bytes)
            .map_err(|e| format!("temporary annotation write: {e}"))
    })
}
/// Add the sole mutable backlink by atomic replacement; all original act facts stay byte-value equivalent.
pub fn backlink(path: &Path, record_id: &str) -> Result<Value, String> {
    check_path(path)?;
    let mut capture: Value =
        serde_json::from_slice(&std::fs::read(path).map_err(|e| e.to_string())?)
            .map_err(|e| e.to_string())?;
    if let Some(existing) = capture.get("recordId") {
        if existing.as_str() == Some(record_id) {
            return Ok(capture);
        }
        return Err("capture backlink conflict; original evidence retained".into());
    }
    capture["recordId"] = Value::String(record_id.into());
    replace_json(path, &capture)?;
    Ok(capture)
}
pub fn discover(root: &Path) -> Result<Vec<PathBuf>, String> {
    fn walk(dir: &Path, out: &mut Vec<PathBuf>) -> Result<(), String> {
        check_path(dir)?;
        let rd = match std::fs::read_dir(dir) {
            Ok(rd) => rd,
            Err(e) if e.kind() == std::io::ErrorKind::NotFound => return Ok(()),
            Err(e) => {
                return Err(format!(
                    "incomplete record discovery: {}: {e}",
                    dir.display()
                ))
            }
        };
        for entry in rd {
            let entry = entry.map_err(|e| e.to_string())?;
            let path = entry.path();
            check_path(&path)?;
            if path.is_dir() {
                walk(&path, out)?;
            } else if path.extension().is_some_and(|e| e == "jsonl") {
                out.push(path);
            }
        }
        Ok(())
    }
    let mut paths = Vec::new();
    walk(&root.join(".chirality/records"), &mut paths)?;
    let legacy = root.join(LEGACY_LOG);
    check_path(&legacy)?;
    if legacy.exists() {
        paths.push(legacy);
    }
    paths.sort();
    paths.dedup();
    Ok(paths)
}
pub fn read_all(root: &Path) -> (Vec<Value>, Vec<String>) {
    let paths = match discover(root) {
        Ok(p) => p,
        Err(e) => return (vec![], vec![e]),
    };
    let mut entries = Vec::new();
    let mut limits = Vec::new();
    let mut ids = std::collections::HashSet::new();
    for path in paths {
        let (e, l) = records::read_log(&path);
        limits.extend(l);
        for entry in e {
            if let Some(id) = entry["recordId"].as_str() {
                if !ids.insert(id.to_owned()) {
                    limits.push(format!("duplicate record identity: {id}"));
                }
            }
            entries.push(entry);
        }
    }
    (entries, limits)
}
/// Both selected project paths and the portable library path have this common records root.
pub fn records_root(log: &Path) -> Option<PathBuf> {
    log.ancestors()
        .find(|p| {
            p.file_name().is_some_and(|n| n == "records")
                && p.parent()
                    .is_some_and(|p| p.file_name().is_some_and(|n| n == ".chirality"))
        })
        .map(Path::to_path_buf)
}

#[cfg(test)]
mod tests {
    use super::*;
    fn scratch() -> PathBuf {
        let p = std::env::temp_dir().join(crate::util::opaque_id("atomic-publication-").unwrap());
        std::fs::create_dir(&p).unwrap();
        std::fs::canonicalize(p).unwrap()
    }
    #[test]
    fn interrupted_temporary_write_never_exposes_partial_final_evidence() {
        let root = scratch();
        let path = root.join("nested/capture.json");
        let result = publish_json(
            &path,
            &serde_json::json!({"original":"complete"}),
            false,
            |f, b| {
                f.write_all(&b[..4]).unwrap();
                assert!(!path.exists());
                Err("injected partial temporary write".into())
            },
        );
        assert!(result.is_err());
        assert!(!path.exists());
        create_json(&path, &serde_json::json!({"original":"complete"})).unwrap();
        let old = std::fs::read(&path).unwrap();
        assert!(create_json(&path, &serde_json::json!({"overwrite":true})).is_err());
        assert_eq!(std::fs::read(&path).unwrap(), old);
        std::fs::remove_dir_all(root).unwrap();
    }
    #[test]
    fn directory_sync_failure_never_reports_publication_durable() {
        let root = scratch();
        let path = root.join("capture.json");
        fail_directory_for_test(Some(root.clone()));
        let result = create_json(&path, &serde_json::json!({"complete":true}));
        fail_directory_for_test(None);
        assert!(result.unwrap_err().contains("directory sync"));
        assert_eq!(
            serde_json::from_slice::<Value>(&std::fs::read(&path).unwrap()).unwrap(),
            serde_json::json!({"complete":true})
        );
        sync_publication(&path).unwrap();
        std::fs::remove_dir_all(root).unwrap();
    }
}
