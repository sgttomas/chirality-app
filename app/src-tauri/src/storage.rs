//! RS §13.8 records store paths (the project's subtree of the App's records
//! store, `records_store`), the §13.7 paths still read in place before an
//! import, and the workflow library's own paths (U-STORE-2). Keys do not
//! encode governed IDs.
use crate::{records, records_store, util::sha256_hex};
use serde_json::Value;
use std::os::fd::AsRawFd;
use std::{
    fs::{File, OpenOptions},
    io::Write,
    path::{Path, PathBuf},
};
pub const LEGACY_LOG: &str = "records/coordination.rs.jsonl";
/// A workflow library's capture evidence, beside its act log (U-STORE-2), and
/// where a project's captures were kept before the records store (§13.7).
pub const CAPTURES: &str = ".chirality/captures";
/// Where a project's logs were kept before the records store (§13.7).
pub const LEGACY_RECORDS: &str = ".chirality/records";
pub fn key(identity: &str) -> String {
    sha256_hex(identity.as_bytes())
}
/// A project log's path in its records home: `runs/<run-key>/<writer-key>.jsonl`
/// or `acts/<writer-key>.jsonl`.
pub fn log_rel(run: Option<&str>, writer: &str) -> String {
    match run {
        Some(run) => format!("runs/{}/{}.jsonl", key(run), key(writer)),
        None => format!("acts/{}.jsonl", key(writer)),
    }
}
/// The owning log for a project write, in the project's store subtree. A
/// refusal (store unavailable, no identity, import needed) is returned, never
/// a fallback path.
pub fn project_log(root: &Path, run: Option<&str>, writer: &str) -> Result<PathBuf, String> {
    Ok(records_store::write_dir(root)?.join(log_rel(run, writer)))
}
/// A path named relative to a project's records home, accepting the §13.7
/// spelling (`.chirality/records/…`, `.chirality/captures/…`) of the same file.
pub fn home_rel(rel: &str) -> String {
    if let Some(rest) = rel.strip_prefix(".chirality/records/") {
        rest.to_owned()
    } else if let Some(rest) = rel.strip_prefix(".chirality/") {
        rest.to_owned()
    } else {
        rel.to_owned()
    }
}
/// A project file for a write: `rel` in the project's store subtree.
pub fn project_file(root: &Path, rel: &str) -> Result<PathBuf, String> {
    Ok(records_store::write_dir(root)?.join(home_rel(rel)))
}
pub fn library_log(library: &Path) -> PathBuf {
    library.join(".chirality/records/acts.jsonl")
}
/// A workflow library's capture evidence folder (U-STORE-2).
pub fn library_capture_dir(library: &Path) -> PathBuf {
    library.join(CAPTURES)
}
pub fn library_capture_path(library: &Path, id: &str) -> PathBuf {
    library_capture_dir(library).join(format!("{}.json", key(id)))
}
pub fn library_pending_path(library: &Path, id: &str) -> PathBuf {
    library_capture_dir(library).join("pending").join(format!("{}.json", key(id)))
}
/// The project's capture evidence folder as it is read now: the store's, or
/// before an import the §13.7 folder in place.
pub fn capture_dir(root: &Path) -> Result<PathBuf, String> {
    let home = records_store::home(root)?;
    Ok(match (home.store_mode, home.attachment.dir) {
        (true, Some(dir)) => dir.join("captures"),
        _ => root.join(CAPTURES),
    })
}
/// The project's capture evidence folder for a write (store only).
pub fn write_capture_dir(root: &Path) -> Result<PathBuf, String> {
    Ok(records_store::write_dir(root)?.join("captures"))
}
pub fn capture_path(root: &Path, id: &str) -> Result<PathBuf, String> {
    Ok(capture_dir(root)?.join(format!("{}.json", key(id))))
}
pub fn write_capture_path(root: &Path, id: &str) -> Result<PathBuf, String> {
    Ok(write_capture_dir(root)?.join(format!("{}.json", key(id))))
}
pub fn write_pending_path(root: &Path, id: &str) -> Result<PathBuf, String> {
    Ok(write_capture_dir(root)?.join("pending").join(format!("{}.json", key(id))))
}
/// The capture file of `capture` for a write or a recovery: an A15 capture
/// stays with its library (`root` is the library), every other with the
/// project's store subtree.
pub fn capture_file_for(root: &Path, capture: &Value) -> Result<PathBuf, String> {
    let id = capture["captureId"].as_str().ok_or("capture identity absent")?;
    if capture["actKind"] == "A15" { Ok(library_capture_path(root, id)) } else { write_capture_path(root, id) }
}
pub fn pending_file_for(root: &Path, capture: &Value) -> Result<PathBuf, String> {
    let id = capture["captureId"].as_str().ok_or("capture identity absent")?;
    if capture["actKind"] == "A15" { Ok(library_pending_path(root, id)) } else { write_pending_path(root, id) }
}
/// The capture lock for `capture`'s home.
pub fn capture_lock_for(root: &Path, capture: &Value) -> Result<PathBuf, String> {
    Ok(capture_file_for(root, capture)?.parent().ok_or("capture has no folder")?.join(".capture.lock"))
}
/// The owning log a pending capture submission names: an A15 log relative to
/// the library, every other relative to the project's records home.
pub fn submission_log(root: &Path, capture: &Value, log: &str) -> Result<PathBuf, String> {
    if capture["actKind"] == "A15" { Ok(root.join(log)) } else { project_file(root, log) }
}
/// A log's name for presentation: `records-store:<path>` in the project's
/// store subtree, otherwise relative to the project (or the full path).
pub fn log_label(root: &Path, path: &Path) -> String {
    if let Some(dir) = records_store::project_dir_of(path) {
        if let Ok(rest) = path.strip_prefix(&dir) {
            return format!("records-store:{}", rest.to_string_lossy());
        }
    }
    path.strip_prefix(root).map(|p| p.to_string_lossy().into_owned()).unwrap_or_else(|_| path.to_string_lossy().into_owned())
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
pub struct Ownership(File, #[allow(dead_code)] Option<Box<Ownership>>);
impl Drop for Ownership {
    fn drop(&mut self) {
        unsafe {
            libc::flock(self.0.as_raw_fd(), libc::LOCK_UN);
        }
    }
}
pub fn lock(path: &Path) -> Result<Ownership, String> {
    flock(path, libc::LOCK_EX, false).map(|o| o.expect("a blocking lock is always taken"))
}
/// A shared lock, held by each holder for as long as it lives; the OS releases
/// it when the holding process ends.
pub fn lock_shared(path: &Path) -> Result<Ownership, String> {
    flock(path, libc::LOCK_SH, false).map(|o| o.expect("a blocking lock is always taken"))
}
/// An exclusive lock taken only if no other holder (shared or exclusive, in this
/// or another process) has the file locked now; `None` otherwise. Never waits.
pub fn try_lock_exclusive(path: &Path) -> Result<Option<Ownership>, String> {
    flock(path, libc::LOCK_EX | libc::LOCK_NB, false)
}
/// Read ownership allows a closed retained payload (for export), while the
/// stable admission lease still prevents removal during the read.
pub(crate) fn read_lock(path:&Path)->Result<Ownership,String>{flock(path,libc::LOCK_EX,true).map(|o|o.unwrap())}
/// Nonblocking read ownership, including closed retained payloads.
pub(crate) fn try_read_lock(path:&Path)->Result<Option<Ownership>,String>{flock(path,libc::LOCK_EX|libc::LOCK_NB,true)}
fn flock(path: &Path, operation: libc::c_int, read: bool) -> Result<Option<Ownership>, String> {
    let admission=if read {crate::records_retention::read_path(path)?}else{crate::records_retention::write_path(path)?};
    check_path(path)?;
    ensure_directory_impl(path.parent().ok_or("lock has no parent")?)?;
    let file = OpenOptions::new()
        .read(true)
        .write(true)
        .create(true)
        .truncate(false)
        .open(path)
        .map_err(|e| format!("owning lock: {e}"))?;
    if unsafe { libc::flock(file.as_raw_fd(), operation) } != 0 {
        let error = std::io::Error::last_os_error();
        if operation & libc::LOCK_NB != 0 && error.kind() == std::io::ErrorKind::WouldBlock {
            return Ok(None);
        }
        return Err(format!("owning lock: {error}"));
    }
    Ok(Some(Ownership(file,admission.map(Box::new))))
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
    let _admission=crate::records_retention::write_path(path)?;
    ensure_directory_impl(path)
}
fn ensure_directory_impl(path:&Path)->Result<(),String>{
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
    let store = records_store::project_dir_of(path).and_then(|d| d.parent().and_then(Path::parent).map(Path::to_path_buf));
    let boundary = store.as_deref().or_else(|| path
        .ancestors()
        .find(|p| p.file_name().is_some_and(|n| n == ".chirality"))
        .and_then(Path::parent));
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
fn publish_json_observed(
    path: &Path,
    value: &Value,
    replace: bool,
    attempted_publication: &mut bool,
    write: impl FnOnce(&mut File, &[u8]) -> Result<(), String>,
) -> Result<(), String> {
    let _admission=crate::records_retention::write_path(path)?;
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
        // A syscall attempted publication: its failure is conservatively uncertain.
        *attempted_publication = true;
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
fn publish_json(
    path: &Path,
    value: &Value,
    replace: bool,
    write: impl FnOnce(&mut File, &[u8]) -> Result<(), String>,
) -> Result<(), String> {
    publish_json_observed(path, value, replace, &mut false, write)
}
/// Capture-specific stage evidence; not an origin/admission proof.
pub(crate) enum CapturePublicationFailure {
    DefinitelyNotPublished(String),
    PublicationUncertain(String),
}
#[cfg(test)]
thread_local! { static FAIL_CAPTURE_WRITE: std::cell::Cell<bool> = const { std::cell::Cell::new(false) }; }
#[cfg(test)]
pub(crate) fn fail_capture_write_for_test(fail: bool) { FAIL_CAPTURE_WRITE.with(|v|v.set(fail)); }
pub(crate) fn create_capture_json(path: &Path, value: &Value) -> Result<(), CapturePublicationFailure> {
    let mut attempted = false;
    let result = publish_json_observed(path, value, false, &mut attempted, |file, bytes| {
        #[cfg(test)]
        if FAIL_CAPTURE_WRITE.with(|v|v.get()) { return Err("temporary evidence write: injected prepublication failure".into()); }
        file.write_all(bytes).map_err(|e|format!("temporary evidence write: {e}"))
    });
    result.map_err(|error| if attempted { CapturePublicationFailure::PublicationUncertain(error) } else { CapturePublicationFailure::DefinitelyNotPublished(error) })
}
/// Publishes exact `bytes` once (an import's byte-identical copy): temporary
/// file in the same folder, written and synced, linked without replacing.
pub(crate) fn create_bytes(path: &Path, bytes: &[u8]) -> Result<(), String> {
    let _admission=crate::records_retention::write_path(path)?;
    check_path(path)?;
    let parent = path.parent().ok_or("copy has no parent")?;
    ensure_directory(parent)?;
    let temp = parent.join(format!(".{}.{}.tmp", path.file_name().unwrap().to_string_lossy(), crate::util::opaque_id("")?));
    let result = (|| {
        let mut file = OpenOptions::new().create_new(true).write(true).open(&temp).map_err(|e| format!("temporary copy: {e}"))?;
        file.write_all(bytes).map_err(|e| format!("temporary copy write: {e}"))?;
        file.sync_all().map_err(|e| format!("temporary copy sync: {e}"))?;
        std::fs::hard_link(&temp, path).map_err(|e| format!("create-once copy publication: {e}"))?;
        sync_publication(path)
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
    let _admission=crate::records_retention::write_path(path)?;
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
    let found = sources(root)?;
    let mut paths = Vec::new();
    for dir in &found.walk {
        walk(dir, &mut paths)?;
    }
    paths.extend(found.files);
    paths.retain(|p| !found.exclude.contains(p));
    paths.sort();
    paths.dedup();
    Ok(paths)
}
/// Where a project's logs are discovered (R-1): folders walked for `*.jsonl`
/// and single files.
pub(crate) struct Sources {
    pub walk: Vec<PathBuf>,
    pub files: Vec<PathBuf>,
    /// Logs found by the walk that are not part of this set.
    pub exclude: Vec<PathBuf>,
}
/// R-1 for `root`: the project's run/act record set. Once the records store
/// holds the project's records: its store `runs/` and `acts/`, and the
/// imported copy of the registered legacy log. Before that (nothing imported
/// or written yet, or a folder that is only a library): the §13.7 folder and
/// the registered legacy log in place. §13.7 files left in place after an
/// import are not read (`records_store::notes`). The act log of a workflow
/// library that is also the project is never part of a project's set: it is
/// library evidence, in the agent-writable tree, read on its own
/// (`records::library_record_set`) so its lines never make the project's
/// set incomplete (U-STORE-2).
pub(crate) fn sources(root: &Path) -> Result<Sources, String> {
    let home = records_store::home(root)?;
    let library = library_log(root);
    check_path(&library)?;
    match (home.store_mode, home.attachment.dir) {
        (true, Some(dir)) => {
            let registered = dir.join(records_store::REGISTERED_COPY);
            let files = if registered.exists() { vec![registered] } else { vec![] };
            Ok(Sources { walk: vec![dir.join("runs"), dir.join("acts")], files, exclude: vec![] })
        }
        _ => {
            let legacy = root.join(LEGACY_LOG);
            check_path(&legacy)?;
            let files = if legacy.exists() { vec![legacy] } else { vec![] };
            Ok(Sources { walk: vec![root.join(LEGACY_RECORDS)], files, exclude: vec![library] })
        }
    }
}
/// The registered legacy log as it is read now: the imported copy in the
/// project's store subtree, or before an import the file in place.
pub fn registered_legacy_log(root: &Path) -> Result<PathBuf,String> {
    let home=records_store::home(root)?;
    if home.store_mode {Ok(home.attachment.dir.ok_or("records store source identity unavailable")?.join(records_store::REGISTERED_COPY))}
    else{Ok(root.join(LEGACY_LOG))}
}

pub fn read_all(root: &Path) -> (Vec<Value>, Vec<String>) {
    let (entries, mut limits, partial) = read_all_parts(root);
    limits.extend(partial);
    (entries, limits)
}
/// As [`read_all`], with each log's torn final line (a partial, never an
/// entry; RS §14.2 R-2) apart from the limits that leave the set incomplete.
pub(crate) fn read_all_parts(root: &Path) -> (Vec<Value>, Vec<String>, Vec<String>) {
    let paths = match discover(root) {
        Ok(p) => p,
        Err(e) => return (vec![], vec![e], vec![]),
    };
    let mut entries = Vec::new();
    let mut limits = Vec::new();
    let mut partial = Vec::new();
    let mut ids = std::collections::HashSet::new();
    for path in paths {
        let read = records::read_log_parts(&path);
        limits.extend(read.limits);
        partial.extend(read.partial_tail);
        for entry in read.entries {
            if let Some(id) = entry["recordId"].as_str() {
                if !ids.insert(id.to_owned()) {
                    limits.push(format!("duplicate record identity: {id}"));
                }
            }
            entries.push(entry);
        }
    }
    (entries, limits, partial)
}
/// Both selected project paths and the portable library path have this common records root.
/// A log in the records store has its project's store folder as this root.
pub fn records_root(log: &Path) -> Option<PathBuf> {
    if let Some(dir) = records_store::project_dir_of(log) {
        return Some(dir);
    }
    log.ancestors()
        .find(|p| {
            p.file_name().is_some_and(|n| n == "records")
                && p.parent()
                    .is_some_and(|p| p.file_name().is_some_and(|n| n == ".chirality"))
        })
        .map(Path::to_path_buf)
}
/// The project root a log belongs to (the records set its writer checks):
/// for a store log, the root its project folder was attached from in this
/// process (`Err` if none was); for a §13.7 or library log, the folder above
/// `.chirality`; `Ok(None)` outside any records tree.
pub(crate) fn project_of_log(log: &Path) -> Result<Option<PathBuf>, String> {
    // A workflow library's act log is its own record set (U-STORE-2).
    if log.file_name().is_some_and(|n| n == "acts.jsonl") && log.parent().is_some_and(|p| p.ends_with(LEGACY_RECORDS)) {
        return Ok(None);
    }

    if let Some(dir) = records_store::project_dir_of(log) {
        return records_store::root_for_dir(&dir).map(Some).ok_or_else(|| format!("records store log {} belongs to no project opened in this process; nothing written", log.display()));
    }
    Ok(records_root(log).as_ref().and_then(|r| r.parent()).and_then(|r| r.parent()).map(Path::to_path_buf))
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
