//! DEL-01-01: the folder the App gives the Codex it hosts as its working
//! folder when no project is open, and the rules that place a folder against
//! the App data folder by what it is (device and inode), never by the text of
//! its path. Kept apart from desktop setup so that the Codex home plans
//! (`home_resources`) apply the same rule wherever they are built.
use crate::storage;
use std::os::unix::fs::{DirBuilderExt, MetadataExt};
use std::path::{Path, PathBuf};

/// DEL-01-01: the folder the App gives the Codex it hosts as its working
/// folder when no project is open. Under Codex's workspace-write sandbox the
/// working folder is an agent's writable root, so it is a folder of its own,
/// set aside for this and holding nothing else of the App's: never the App
/// data folder itself, whose other contents (the records store, the account
/// homes, the saved setup request, the recovery ledger) stay outside it. This
/// only calculates the path; [`ensure_no_project_folder`] creates it.
pub fn no_project_folder(app_data: &Path) -> PathBuf {
    app_data.join("conversations-without-project")
}
/// Where a working folder lies against the App data folder. Decided by what
/// each folder is (its device and inode, and those of its ancestors), never by
/// the text of a path, so that no spelling, link or alias turns the folder for
/// conversations without a project into a way to admit the App's other data.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum WorkingFolder {
    /// Not the App data folder and not inside it. A folder that contains it
    /// (a project such as the home folder) is here too, as before this change.
    Outside,
    /// The folder set aside for conversations without a project, or a folder
    /// inside it, while that folder is a real private directory of this user
    /// at its literal place (`no_project_folder` of the canonical App data).
    NoProject,
    /// The App data folder, or a folder inside it other than the one set aside.
    AppData,
    /// Its place cannot be established: it is relative, a link in its existing
    /// part cannot be resolved, a `..` follows a missing part, or its existing
    /// part lies in the App data folder while the rest is missing.
    Unresolved,
}
type Identity = (u64, u64);
fn identity(meta: &std::fs::Metadata) -> Identity {
    (meta.dev(), meta.ino())
}
/// The identities of `path` (which must exist) and each of its ancestors.
fn identity_chain(path: &Path) -> Vec<Identity> {
    path.ancestors().filter_map(|at| std::fs::metadata(at).ok()).map(|meta| identity(&meta)).collect()
}
/// The folder set aside, and its identity, only while it is a real private
/// directory of this user at its literal place, checked without following a
/// link. Nothing a link points to is ever that folder.
pub fn valid_no_project_folder(app_data: &Path) -> Option<(PathBuf, Identity)> {
    let leaf = no_project_folder(&std::fs::canonicalize(app_data).ok()?);
    let meta = std::fs::symlink_metadata(&leaf).ok()?;
    let private = meta.uid() == unsafe { libc::geteuid() } && meta.mode() & 0o077 == 0;
    (meta.file_type().is_dir() && private).then(|| (leaf, identity(&meta)))
}
/// The canonical form of the longest existing part of `path`, and the missing
/// rest. `None` when a link in the existing part cannot be resolved, or the
/// existing part cannot be examined: such a place is never established.
fn existing_part(path: &Path) -> Option<(PathBuf, Vec<std::ffi::OsString>)> {
    let mut at = PathBuf::new();
    let mut components = path.components();
    let mut missing = Vec::new();
    for component in components.by_ref() {
        let next = at.join(component.as_os_str());
        match std::fs::symlink_metadata(&next) {
            Ok(meta) => {
                if meta.file_type().is_symlink() && std::fs::canonicalize(&next).is_err() {
                    return None;
                }
                at = next;
            }
            Err(e) if e.kind() == std::io::ErrorKind::NotFound => {
                missing.push(component.as_os_str().to_owned());
                break;
            }
            Err(_) => return None,
        }
    }
    missing.extend(components.map(|c| c.as_os_str().to_owned()));
    Some((std::fs::canonicalize(&at).ok()?, missing))
}
pub fn working_folder_place(app_data: &Path, folder: &Path) -> WorkingFolder {
    let Ok(data) = std::fs::canonicalize(app_data) else { return WorkingFolder::Unresolved };
    let Ok(data_meta) = std::fs::metadata(&data) else { return WorkingFolder::Unresolved };
    let data_id = identity(&data_meta);
    if !folder.is_absolute() {
        return WorkingFolder::Unresolved;
    }
    let Some((existing, missing)) = existing_part(folder) else { return WorkingFolder::Unresolved };
    let chain = identity_chain(&existing);
    let in_leaf = valid_no_project_folder(&data).is_some_and(|(_, leaf)| chain.contains(&leaf));
    let in_data = chain.contains(&data_id);
    if !missing.is_empty() {
        // A missing folder is placed by its existing part. Inside the App data
        // folder (the folder set aside included) or after a `..`, its place is
        // not established; elsewhere it is not in the App data folder.
        let dotted = missing.iter().any(|name| name == ".." || name == ".");
        return if dotted || in_data { WorkingFolder::Unresolved } else { WorkingFolder::Outside };
    }
    if in_leaf {
        WorkingFolder::NoProject
    } else if in_data {
        WorkingFolder::AppData
    } else {
        WorkingFolder::Outside
    }
}
/// The plain reason a working folder is refused, or `None` when it may be
/// given to Codex. `subject` begins the sentence ("Codex was not started", for
/// example).
pub fn working_folder_refusal(app_data: &Path, folder: &Path, subject: &str) -> Option<String> {
    let data = std::fs::canonicalize(app_data).unwrap_or_else(|_| app_data.to_path_buf());
    let set_aside = no_project_folder(&data);
    if (folder == set_aside || folder == no_project_folder(app_data)) && valid_no_project_folder(&data).is_none() {
        return Some(format!("{subject}: the folder Chirality sets aside for conversations without a project ({}) is missing or is no longer a private folder of its own.", set_aside.display()));
    }
    match working_folder_place(app_data, folder) {
        WorkingFolder::Outside | WorkingFolder::NoProject => None,
        WorkingFolder::AppData => Some(format!("{subject}: its working folder {} is in Chirality's own data folder ({}), where a conversation could change Chirality's records and settings.", folder.display(), data.display())),
        WorkingFolder::Unresolved => Some(format!("{subject}: Chirality could not establish where the folder {} is, so it might be in Chirality's own data folder.", folder.display())),
    }
}
/// Whether `candidate` may be at, in or contain `reserved`, decided by the
/// identity of what exists: the resolved existing part of `candidate` lies in
/// `reserved`, or `candidate` exists and `reserved` lies in it; for what does
/// not exist, by the resolved text. A link that cannot be resolved, or a `..`
/// after a missing part, cannot be established and counts as overlapping.
pub fn may_overlap(candidate: &Path, reserved: &Path) -> bool {
    if !candidate.is_absolute() {
        return true;
    }
    let Some((existing, missing)) = existing_part(candidate) else { return true };
    if missing.iter().any(|name| name == ".." || name == ".") {
        return true;
    }
    let chain = identity_chain(&existing);
    if let Ok(meta) = std::fs::metadata(reserved) {
        let reserved_id = identity(&meta);
        if chain.contains(&reserved_id) {
            return true;
        }
        if missing.is_empty() && chain.first().is_some_and(|own| identity_chain(reserved).contains(own)) {
            return true;
        }
    }
    let lexical = resolve_lexically;
    let at = missing.iter().fold(existing, |at, name| at.join(name));
    let reserved = lexical(reserved);
    at.starts_with(&reserved) || reserved.starts_with(&at)
}
/// DEL-01-01: whether `candidate` (a records store or a Codex home, or a
/// source of its settings) may be at, in or contain the folder set aside for
/// conversations without a project. The folder is made to exist first (when
/// the App data folder exists), so that any other spelling of it resolves
/// through the real directory and is decided by identity. If it could not be
/// made or verified, nothing under the App data folder can be established
/// and every such candidate counts. Uncertainty counts.
pub fn may_be_in_no_project_folder(app_data: &Path, candidate: &Path) -> bool {
    // With no App data folder yet, nothing under it exists, so nothing can be another spelling
    // of an existing folder: decided by the resolved text, and decided again by identity once it
    // exists (a home plan checks again before it creates anything).
    if matches!(std::fs::symlink_metadata(app_data), Err(e) if e.kind() == std::io::ErrorKind::NotFound) {
        return may_overlap(candidate, &resolve_lexically(&no_project_folder(app_data)));
    }
    let verified = app_data.is_dir() && ensure_no_project_folder(app_data).is_ok();
    match valid_no_project_folder(app_data).filter(|_| verified) {
        Some((leaf, _)) => may_overlap(candidate, &leaf),
        None => may_overlap(candidate, &std::fs::canonicalize(app_data).unwrap_or_else(|_| app_data.to_path_buf())),
    }
}
/// DEL-01-01: a Codex home is never at, in or containing the folder set aside
/// for conversations without a project: refused when the home is planned, its
/// descriptors frozen or before it is prepared or started, before anything is
/// created in it. A home whose place cannot be established is refused.
pub fn refuse_in_no_project_folder(app_data: &Path, path: &Path, what: &str) -> Result<(), String> {
    if may_be_in_no_project_folder(app_data, path) {
        return Err(format!("{what} ({}) may not be in, or contain, the folder Chirality sets aside for conversations without a project, and its place relative to that folder must be established", path.display()));
    }
    Ok(())
}
/// DEL-01-01: a source of a Codex home's settings is never in, or over, the
/// folder set aside. A source may be absent, or behind a link whose target is
/// absent: that stays a visible source limit, as before. Such a source is
/// placed where its links lead, by their target text, and refused only when
/// that place is in, or over, the folder set aside (or cannot be followed).
pub fn refuse_source_in_no_project_folder(app_data: &Path, path: &Path, what: &str) -> Result<(), String> {
    let refused = match located(path, 0) {
        Some(at) => may_be_in_no_project_folder(app_data, &at),
        None => true,
    };
    if refused {
        return Err(format!("{what} ({}) may not be in the folder Chirality sets aside for conversations without a project, by itself or through a link", path.display()));
    }
    Ok(())
}
/// Where `path` leads when every link in it is followed by its target text,
/// absent targets included: the canonical existing part and the missing rest.
/// `None` for a link cycle or a part that cannot be examined.
fn located(path: &Path, depth: usize) -> Option<PathBuf> {
    if depth > 40 || !path.is_absolute() {
        return None;
    }
    let mut at = PathBuf::new();
    let mut components = path.components();
    while let Some(component) = components.next() {
        let next = at.join(component.as_os_str());
        match std::fs::symlink_metadata(&next) {
            Ok(meta) if meta.file_type().is_symlink() => {
                let target = std::fs::read_link(&next).ok()?;
                let target = if target.is_absolute() { target } else { at.join(target) };
                let rest: PathBuf = components.map(|c| c.as_os_str()).collect();
                return located(&target.join(rest), depth + 1);
            }
            Ok(_) => at = next,
            Err(e) if e.kind() == std::io::ErrorKind::NotFound => {
                let mut out = std::fs::canonicalize(&at).ok()?;
                out.push(component.as_os_str());
                out.extend(components.map(|c| c.as_os_str()));
                return Some(out);
            }
            Err(_) => return None,
        }
    }
    std::fs::canonicalize(&at).ok()
}
/// Creates the folder for conversations without a project when it is
/// missing (owner-only, 0700) and checks it: a link, a file or a folder that
/// is not private refuses, so nothing is started there. Called before every
/// Codex start whose working folder it is.
pub fn ensure_no_project_folder(app_data: &Path) -> Result<PathBuf, String> {
    let data = std::fs::canonicalize(app_data).map_err(|e| format!("Codex was not started: Chirality's data folder ({}) could not be found: {e}", app_data.display()))?;
    let folder = no_project_folder(&data);
    protected_directory(&folder).map_err(|e| {
        format!("Codex was not started: the folder Chirality sets aside for conversations without a project ({}) is not a private folder of its own: {e}", folder.display())
    })?;
    Ok(folder)
}


/// The canonical form of the longest existing ancestor, with the rest appended.
fn resolve_lexically(path: &Path) -> PathBuf {
    let mut tail = Vec::new();
    let mut at = path.to_path_buf();
    loop {
        if let Ok(c) = std::fs::canonicalize(&at) {
            let mut out = c;
            for part in tail.iter().rev() {
                out.push(part);
            }
            return out;
        }
        match (at.file_name().map(|n| n.to_owned()), at.parent()) {
            (Some(name), Some(parent)) => {
                tail.push(name);
                at = parent.to_path_buf();
            }
            _ => return path.to_path_buf(),
        }
    }
}
/// A private directory of this user (0700), created with its missing
/// ancestors when absent; a link, a file or a directory that is not private
/// refuses.
pub fn protected_directory(path: &Path) -> Result<(), String> {
    storage::check_path(path)?;
    if !path.exists() {
        let mut missing = Vec::new();
        let mut ancestor = path;
        while !ancestor.exists() {
            missing.push(ancestor.to_owned());
            ancestor = ancestor
                .parent()
                .ok_or("private directory ancestor absent")?;
        }
        std::fs::DirBuilder::new()
            .recursive(true)
            .mode(0o700)
            .create(path)
            .map_err(|e| e.to_string())?;
        for directory in missing {
            storage::sync_dir(&directory)?;
        }
        storage::sync_dir(ancestor)?;
    }
    let meta = std::fs::symlink_metadata(path).map_err(|e| e.to_string())?;
    if !meta.is_dir() || meta.uid() != unsafe { libc::geteuid() } || meta.mode() & 0o077 != 0 {
        return Err(
            "desktop profile directory must be private (0700) and owned by this user".into(),
        );
    }
    Ok(())
}
