//! DEL-01-01: the App's working folders, kept beside the App data folder in
//! "<App data folder's name> Working Files" and never in a temporary folder.
//! Each folder the App makes there is made by [`WorkingFiles::allocate`]:
//! - the label probe's home (`probe-homes/`);
//! - the connector's working folder (`connector/`);
//! - the temporary folder Codex is given as its TMPDIR (`codex-tmp/`).
//!
//! **The claim** (with its boundary in the pull request that made this): the
//! App allocates no working state at a location a sandboxed Codex can write.
//! These folders are outside the App data folder and outside every temporary
//! folder. Codex's TMPDIR is made writable to Codex on purpose; it is its own
//! subtree, never one of the others or above them.
//!
//! **What may be removed.** A folder here is removed only if all of these hold:
//! - its record, written before it was used, names it;
//! - it is a real folder of this user, not a link;
//! - its device, inode and creation time are the ones recorded;
//! - it is not, and does not contain, a folder the caller protects (checked by
//!   identity);
//! - no file under it, looked for by name and never opened, is named as Codex
//!   names its sign-in file. A probe home or temporary folder holding one is
//!   kept and reported: it is a finding, not rubbish.
//!
//! Anything else is kept and reported: a planted folder of a recorded name, a
//! link in its place, a folder whose identity has changed, and every entry when
//! the record cannot be read. The removal itself follows no link
//! (`std::fs::remove_dir_all` removes a link, not what it points to).
//!
//! **The record.** One file per subtree (`.made.json`), in the App's own
//! subtree, which is not a writable root of Codex. It is written whole to a new
//! file and renamed into place, so a reader sees the old or the new one. A record
//! that cannot be read or does not parse means nothing in that subtree is
//! removed, and the state is reported. It never means "remove everything that
//! looks like ours".
use std::os::unix::fs::{DirBuilderExt, MetadataExt};
use std::path::{Path, PathBuf};

/// What the Working Files folder's name adds to the App data folder's name.
pub const SUFFIX: &str = " Working Files";
/// The file under which Codex keeps a sign-in (HOSTING, DEL-01-05). It is
/// looked for by name only; it is never opened here.
const SIGN_IN_FILE: &str = "auth.json";
const RECORD: &str = ".made.json";
/// One writer of the records at a time in this process; the App's process lock
/// keeps other processes out of this App data folder's working files.
static RECORDS: std::sync::Mutex<()> = std::sync::Mutex::new(());
fn records_lock() -> std::sync::MutexGuard<'static, ()> {
    RECORDS.lock().unwrap_or_else(|e| e.into_inner())
}

/// The one place the Working Files folder's path is derived: the App data
/// folder's own name and [`SUFFIX`], beside it. A folder is never taken as the
/// App's by this name alone; [`establish`] checks what it is.
pub fn folder_for(app_data: &Path) -> Result<PathBuf, String> {
    let (Some(parent), Some(name)) = (app_data.parent(), app_data.file_name()) else {
        return Err(format!("Chirality's data folder {} has no parent folder to keep its working files beside", app_data.display()));
    };
    let mut leaf = name.to_os_string();
    leaf.push(SUFFIX);
    Ok(parent.join(leaf))
}

/// The kinds of folder the App makes here, each in its own subtree.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum Kind {
    ProbeHome,
    Connector,
    CodexTmp,
}
impl Kind {
    pub const ALL: [Kind; 3] = [Kind::ProbeHome, Kind::Connector, Kind::CodexTmp];
    fn subtree(self) -> &'static str {
        match self {
            Kind::ProbeHome => "probe-homes",
            Kind::Connector => "connector",
            Kind::CodexTmp => "codex-tmp",
        }
    }
    fn prefix(self) -> &'static str {
        match self {
            Kind::ProbeHome => "probe-",
            Kind::Connector => "connector-",
            Kind::CodexTmp => "tmp-",
        }
    }
}

/// A folder's identity as recorded: device, inode and creation time. An inode
/// can be reused after a folder is removed from outside; the creation time
/// makes a later folder with a reused number fail the check.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub struct Stamp {
    dev: u64,
    ino: u64,
    created_secs: i64,
    created_nanos: i64,
}
impl Stamp {
    fn of(meta: &std::fs::Metadata) -> Stamp {
        // The creation (birth) time where the system keeps one (macOS does); otherwise the
        // status-change time, which a later folder with a reused inode also fails to match.
        let (created_secs, created_nanos) = match meta.created().ok().and_then(|t| t.duration_since(std::time::UNIX_EPOCH).ok()) {
            Some(d) => (d.as_secs() as i64, d.subsec_nanos() as i64),
            None => (meta.ctime(), meta.ctime_nsec()),
        };
        Stamp { dev: meta.dev(), ino: meta.ino(), created_secs, created_nanos }
    }
    fn to_json(self, name: &str) -> serde_json::Value {
        serde_json::json!({"name": name, "dev": self.dev.to_string(), "ino": self.ino.to_string(),
            "createdSecs": self.created_secs.to_string(), "createdNanos": self.created_nanos.to_string()})
    }
    fn from_json(v: &serde_json::Value) -> Option<(String, Stamp)> {
        let text = |k: &str| v.get(k).and_then(serde_json::Value::as_str);
        Some((text("name")?.to_owned(), Stamp {
            dev: text("dev")?.parse().ok()?,
            ino: text("ino")?.parse().ok()?,
            created_secs: text("createdSecs")?.parse().ok()?,
            created_nanos: text("createdNanos")?.parse().ok()?,
        }))
    }
}

/// A folder the App made here, with the identity it was recorded under.
#[derive(Clone, Debug)]
pub struct Made {
    pub path: PathBuf,
    pub kind: Kind,
    name: String,
    stamp: Stamp,
}

/// What a cleaning did: what it removed, and what it kept and why.
#[derive(Clone, Debug, Default, PartialEq, Eq)]
pub struct Cleaning {
    pub removed: Vec<PathBuf>,
    pub kept: Vec<(PathBuf, String)>,
}

/// The Working Files folder, established: a real private folder of this user
/// beside the App data folder, with its three subtrees.
#[derive(Clone, Debug)]
pub struct WorkingFiles {
    root: PathBuf,
}

fn euid() -> u32 {
    unsafe { libc::geteuid() }
}
/// Whether `meta` is a real private folder of this user; otherwise what it is,
/// in the person's words.
fn private_folder(path: &Path, meta: &std::fs::Metadata) -> Result<(), String> {
    let kind = meta.file_type();
    if kind.is_symlink() {
        return Err(format!("a link to {}", std::fs::read_link(path).unwrap_or_default().display()));
    }
    if !kind.is_dir() {
        return Err(if kind.is_file() { "a file".into() } else { "something that is not a folder".into() });
    }
    if meta.uid() != euid() {
        return Err("a folder that belongs to another account".into());
    }
    if meta.mode() & 0o077 != 0 {
        return Err("a folder that other accounts can use".into());
    }
    Ok(())
}
/// Makes `path` (0700) only where it is established to be absent, then checks
/// it is a real private folder of this user. Never removes or replaces what is
/// there. The error is what the person is told.
fn establish_folder(path: &Path, what: &str) -> Result<(), String> {
    let refused = |why: String| format!("Chirality keeps {what} at {}. {why} Move it aside (do not delete what a link points to) and start Chirality again.", path.display());
    match std::fs::symlink_metadata(path) {
        Ok(_) => {}
        Err(e) if e.kind() == std::io::ErrorKind::NotFound => {
            match std::fs::DirBuilder::new().mode(0o700).create(path) {
                Ok(()) => {
                    if let Some(parent) = path.parent() {
                        crate::storage::sync_dir(parent).map_err(|e| refused(format!("It could not be made: {e}.")))?;
                    }
                }
                Err(e) if e.kind() == std::io::ErrorKind::AlreadyExists => {}
                Err(e) => return Err(refused(format!("It could not be made: {e}."))),
            }
        }
        Err(e) => return Err(refused(format!("It could not be examined: {e}."))),
    }
    let meta = std::fs::symlink_metadata(path).map_err(|e| refused(format!("It could not be examined: {e}.")))?;
    private_folder(path, &meta).map_err(|what| refused(format!("Something else is there now: {what}.")))
}

/// The start's step that makes the Working Files folder and its subtrees. The
/// App data folder must already exist and be held. Refused, with words the
/// person can act on, when a folder cannot be made or is not the App's own;
/// there is no fall-back to a temporary folder.
pub fn establish(app_data: &Path) -> Result<WorkingFiles, String> {
    let root = folder_for(app_data)?;
    establish_folder(&root, "its working files")?;
    let data = std::fs::metadata(app_data).map_err(|e| format!("Chirality's data folder {} could not be examined: {e}", app_data.display()))?;
    let held = std::fs::metadata(&root).map_err(|e| format!("Chirality's working files {} could not be examined: {e}", root.display()))?;
    if (data.dev(), data.ino()) == (held.dev(), held.ino()) {
        return Err(format!("Chirality's working files {} are its data folder under another name; move one of them aside and start Chirality again.", root.display()));
    }
    for kind in Kind::ALL {
        establish_folder(&root.join(kind.subtree()), "a working folder")?;
    }
    Ok(WorkingFiles { root })
}

impl WorkingFiles {
    pub fn root(&self) -> &Path {
        &self.root
    }
    fn subtree(&self, kind: Kind) -> PathBuf {
        self.root.join(kind.subtree())
    }
    /// The record of `kind`'s subtree: `Ok(empty)` when there is none yet,
    /// `Err` when it cannot be read or does not parse.
    fn read_record(&self, kind: Kind) -> Result<Vec<(String, Stamp)>, String> {
        let path = self.subtree(kind).join(RECORD);
        let bytes = match std::fs::read(&path) {
            Ok(bytes) => bytes,
            Err(e) if e.kind() == std::io::ErrorKind::NotFound => return Ok(Vec::new()),
            Err(e) => return Err(format!("the record {} could not be read ({e})", path.display())),
        };
        let value: serde_json::Value = serde_json::from_slice(&bytes).map_err(|_| format!("the record {} does not parse", path.display()))?;
        value.get("made").and_then(serde_json::Value::as_array)
            .ok_or_else(|| format!("the record {} does not parse", path.display()))?
            .iter()
            .map(|entry| Stamp::from_json(entry).ok_or_else(|| format!("the record {} does not parse", path.display())))
            .collect()
    }
    /// Writes `kind`'s record whole to a new file and renames it into place.
    fn write_record(&self, kind: Kind, made: &[(String, Stamp)]) -> Result<(), String> {
        let subtree = self.subtree(kind);
        let bytes = serde_json::to_vec(&serde_json::json!({"made": made.iter().map(|(name, stamp)| stamp.to_json(name)).collect::<Vec<_>>()}))
            .map_err(|e| e.to_string())?;
        let temporary = subtree.join(format!("{RECORD}.{}", crate::util::opaque_id("new-")?));
        {
            use std::io::Write;
            let mut file = std::fs::OpenOptions::new().write(true).create_new(true).open(&temporary)
                .map_err(|e| format!("the record in {} could not be written: {e}", subtree.display()))?;
            file.write_all(&bytes).and_then(|()| file.sync_all())
                .map_err(|e| format!("the record in {} could not be written: {e}", subtree.display()))?;
        }
        std::fs::rename(&temporary, subtree.join(RECORD)).map_err(|e| {
            let _ = std::fs::remove_file(&temporary);
            format!("the record in {} could not be written: {e}", subtree.display())
        })?;
        crate::storage::sync_dir(&subtree)
    }
    /// Makes a new folder of `kind`, exclusively and private (0700), and
    /// records its identity before it is returned for use.
    pub fn allocate(&self, kind: Kind) -> Result<Made, String> {
        let _records = records_lock();
        let subtree = self.subtree(kind);
        let meta = std::fs::symlink_metadata(&subtree).map_err(|e| format!("Chirality's working folder {} could not be examined: {e}", subtree.display()))?;
        private_folder(&subtree, &meta).map_err(|what| format!("Chirality's working folder {} is now {what}; move it aside and start Chirality again.", subtree.display()))?;
        let mut record = self.read_record(kind).map_err(|why| format!("Chirality could not make a working folder: {why}; nothing was made."))?;
        let name = crate::util::opaque_id(kind.prefix())?;
        let path = subtree.join(&name);
        std::fs::DirBuilder::new().mode(0o700).create(&path).map_err(|e| format!("Chirality could not make the working folder {}: {e}", path.display()))?;
        let stamp = match std::fs::symlink_metadata(&path) {
            Ok(meta) if meta.is_dir() => Stamp::of(&meta),
            _ => return Err(format!("Chirality could not examine the working folder it made at {}", path.display())),
        };
        record.push((name.clone(), stamp));
        if let Err(why) = self.write_record(kind, &record) {
            // Not recorded, so never used: the folder just made (still empty) is taken back.
            let _ = std::fs::remove_dir(&path);
            return Err(format!("Chirality could not make a working folder: {why}; nothing was made."));
        }
        Ok(Made { path, kind, name, stamp })
    }
    /// Why `path` (recorded as `stamp`) may not be removed, or `None` when it may.
    fn keep_reason(path: &Path, stamp: Stamp, protected: &[PathBuf]) -> Option<String> {
        let meta = match std::fs::symlink_metadata(path) {
            Ok(meta) => meta,
            Err(e) => return Some(format!("it could not be examined ({e})")),
        };
        if meta.file_type().is_symlink() || !meta.is_dir() {
            return Some("it is not a folder (a link or a file is in its place)".into());
        }
        if meta.uid() != euid() {
            return Some("it belongs to another account".into());
        }
        if Stamp::of(&meta) != stamp {
            return Some("a different folder now has its name".into());
        }
        let id = (meta.dev(), meta.ino());
        for keep in protected {
            match std::fs::metadata(keep) {
                Ok(_) => match keep.ancestors().map(std::fs::metadata).collect::<Result<Vec<_>, _>>() {
                    Ok(chain) if chain.iter().any(|m| (m.dev(), m.ino()) == id) => {
                        return Some(format!("it is, or contains, {}", keep.display()));
                    }
                    Ok(_) => {}
                    Err(e) => return Some(format!("where {} lies could not be established ({e})", keep.display())),
                },
                Err(e) if e.kind() == std::io::ErrorKind::NotFound => {}
                Err(e) => return Some(format!("{} could not be examined ({e})", keep.display())),
            }
        }
        match holds_sign_in(path) {
            Ok(false) => None,
            Ok(true) => Some(format!("it holds a file named {SIGN_IN_FILE}, as Codex names its sign-in; nothing in it was read")),
            Err(e) => Some(format!("what it holds could not be examined ({e})")),
        }
    }
    fn take(&self, kind: Kind, name: &str, stamp: Stamp, protected: &[PathBuf], cleaning: &mut Cleaning) -> bool {
        let path = self.subtree(kind).join(name);
        if name.contains('/') || !name.starts_with(kind.prefix()) {
            cleaning.kept.push((path, "its recorded name is not one the App gives".into()));
            return false;
        }
        match std::fs::symlink_metadata(&path) {
            Err(e) if e.kind() == std::io::ErrorKind::NotFound => return true,
            _ => {}
        }
        if let Some(why) = Self::keep_reason(&path, stamp, protected) {
            cleaning.kept.push((path, why));
            return false;
        }
        match std::fs::remove_dir_all(&path) {
            Ok(()) => {
                cleaning.removed.push(path);
                true
            }
            Err(e) => {
                cleaning.kept.push((path, format!("it could not be removed ({e})")));
                false
            }
        }
    }
    /// Removes one folder the App made, if it is still exactly that folder.
    pub fn remove(&self, made: &Made, protected: &[PathBuf]) -> Cleaning {
        let _records = records_lock();
        let mut cleaning = Cleaning::default();
        let Ok(mut record) = self.read_record(made.kind) else {
            cleaning.kept.push((made.path.clone(), "the record could not be read, so nothing was removed".into()));
            return cleaning;
        };
        if !record.iter().any(|(name, stamp)| *name == made.name && *stamp == made.stamp) {
            cleaning.kept.push((made.path.clone(), "it is not in the record".into()));
            return cleaning;
        }
        if self.take(made.kind, &made.name, made.stamp, protected, &mut cleaning) {
            record.retain(|(name, _)| *name != made.name);
            if let Err(why) = self.write_record(made.kind, &record) {
                cleaning.kept.push((self.subtree(made.kind), why));
            }
        }
        cleaning
    }
    /// Removes what the record names and still is what it was, in every
    /// subtree; to be called only under the App's process lock (one App per App
    /// data folder). Entries the record does not name are reported, never removed.
    pub fn clean(&self, protected: &[PathBuf]) -> Cleaning {
        let _records = records_lock();
        let mut cleaning = Cleaning::default();
        for kind in Kind::ALL {
            let subtree = self.subtree(kind);
            let record = match self.read_record(kind) {
                Ok(record) => record,
                Err(why) => {
                    cleaning.kept.push((subtree, format!("{why}, so nothing in it was removed")));
                    continue;
                }
            };
            let mut left = Vec::new();
            for (name, stamp) in record {
                if !self.take(kind, &name, stamp, protected, &mut cleaning) {
                    left.push((name, stamp));
                }
            }
            if let Err(why) = self.write_record(kind, &left) {
                cleaning.kept.push((subtree.clone(), why));
            }
            let named: std::collections::HashSet<String> = left.iter().map(|(name, _)| name.clone()).collect();
            if let Ok(entries) = std::fs::read_dir(&subtree) {
                for entry in entries.flatten() {
                    let name = entry.file_name().to_string_lossy().into_owned();
                    if name == RECORD || name.starts_with(&format!("{RECORD}.")) || named.contains(&name) {
                        continue;
                    }
                    cleaning.kept.push((entry.path(), "the App did not record making it, so it was not removed".into()));
                }
            }
        }
        cleaning
    }
}

/// Whether any entry under `path` is named [`SIGN_IN_FILE`], looked for by
/// name and never opened, and never through a link.
fn holds_sign_in(path: &Path) -> std::io::Result<bool> {
    let mut pending = vec![path.to_path_buf()];
    while let Some(folder) = pending.pop() {
        for entry in std::fs::read_dir(&folder)? {
            let entry = entry?;
            if entry.file_name() == SIGN_IN_FILE {
                return Ok(true);
            }
            if entry.file_type()?.is_dir() {
                pending.push(entry.path());
            }
        }
    }
    Ok(false)
}

#[cfg(test)]
#[path = "working_files_tests.rs"]
mod tests;
