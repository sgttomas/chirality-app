//! The App's records store (RS §13.8; PRD R-STORE; V4-REC-02, V4-REC-04,
//! V4-REC-06): placement, project identity and the explicit import of the
//! §13.7 project records.
//!
//! **Placement.** One store per installation, `<App data>/records/` by
//! default, or a folder the person chose (another volume, for example),
//! outside every project working tree and every Codex home. Tests and
//! development name it explicitly (`CHIRALITY_RECORDS_STORE`); a development
//! build without it has no store, and recording is refused visibly. There is
//! no fallback to another store, a project path or memory.
//!
//! ```text
//! <store>/store.json                      the store's identity (created once)
//! <store>/roots.jsonl                     every project root the store has seen
//! <store>/projects/<key>/project.json     the project's identity record
//! <store>/projects/<key>/imports.jsonl    each explicit import (copies and digests)
//! <store>/projects/<key>/runs/<run-key>/<writer-key>.jsonl
//! <store>/projects/<key>/acts/<writer-key>.jsonl
//! <store>/projects/<key>/captures/        capture evidence (and `pending/`)
//! <store>/projects/<key>/workflow/        WR WP-1 records
//! ```
//!
//! `<key>` is the SHA-256 of the project identity, as §13.7 keys runs and
//! writers. Every file is a plain file written once or only appended (a
//! capture's add-once backlink is its one replacement), so the subtree can be
//! exported byte for byte.
//!
//! **Project identity.** The App mints an opaque identity once and writes it
//! in the project at `.chirality/project.json` (a link naming the identity
//! and this store). The store's own records govern: a missing, changed or
//! unreadable link with the folder known to the store is a visible limit and
//! the store's identity is used; a link whose identity the store records at
//! another folder (moved, or copied) attaches nothing until the person says
//! which it is (adopt, or a new identity); nothing is minted over a mismatch.
//!
//! **Existing records.** Until the person imports them, the §13.7 records in
//! the project are read in place and new recording is refused ("import
//! needed"), so no history is split across two homes. Import copies each file
//! byte for byte, verifies the copy by its SHA-256 and records it; after that
//! the store copy is the owning file and the original is a legacy source, read
//! no more: an original that later differs from its copy is a limit, and the
//! store governs. Originals are never rewritten or deleted.
use crate::util::{now_rfc3339, sha256_hex};
use serde_json::{json, Value};
use std::collections::{BTreeMap, HashMap};
use std::io::{Read, Write};
use std::path::{Path, PathBuf};
use std::sync::{Mutex, RwLock};

#[path = "records_package_import.rs"]
pub(crate) mod package;
#[path = "records_package.rs"]
pub(crate) mod custody;

/// The explicit store location for tests and development.
pub const OVERRIDE_ENV: &str = "CHIRALITY_RECORDS_STORE";
/// The project's link to its identity, inside the project.
pub const PROJECT_LINK: &str = ".chirality/project.json";
/// The person's chosen store location, in the App data folder.
pub const CHOICE_FILE: &str = "records-store.json";
const STORE_FORMAT: &str = "chirality.records-store";
const PROJECT_FORMAT: &str = "chirality.records-store.project";
const LINK_FORMAT: &str = "chirality.project-link";
const ROOT_FORMAT: &str = "chirality.records-store.root";
const IMPORT_FORMAT: &str = "chirality.records-store.import";
const VERSION: &str = "0.1";

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum Placement {
    /// `CHIRALITY_RECORDS_STORE` (tests and development).
    Override,
    /// The location the person chose.
    PersonChosen,
    /// `<App data>/records/`.
    AppData,
    /// A test build's own temporary store (never the App data folder).
    Test,
}
impl Placement {
    pub fn label(self) -> &'static str {
        match self {
            Placement::Override => "explicit override (CHIRALITY_RECORDS_STORE)",
            Placement::PersonChosen => "the location the person chose",
            Placement::AppData => "the App data folder",
            Placement::Test => "test build temporary store",
        }
    }
}

#[derive(Clone, Debug)]
pub struct Store {
    pub root: PathBuf,
    pub placement: Placement,
    /// Placement facts shown with the store (for example, a location inside a
    /// folder an agent can write).
    pub limits: Vec<String>,
}

static STORE: RwLock<Option<Result<Store, String>>> = RwLock::new(None);
/// The opened store: its canonical root and identity.
static OPENED: Mutex<Option<(PathBuf, PathBuf, String)>> = Mutex::new(None);
/// Existing process custody only; no store open, identity write or cache change.
/// Read-only consumers preserve an already opened store's identity/alias binding.
pub(crate) fn known_identity_for_read(configured: &Path, physical: &Path) -> Option<(PathBuf,String)> {
    OPENED.lock().unwrap_or_else(|p|p.into_inner()).as_ref()
        .filter(|(at,root,_)| at == configured || root == physical)
        .map(|(_,root,id)|(root.clone(),id.clone()))
}
/// Store project folder -> the project root it was attached from in this process.
static DIRS: Mutex<Vec<(PathBuf, PathBuf)>> = Mutex::new(Vec::new());
/// The roots record, parsed: (length read, stamp of the file, lines).
static ROOTS: Mutex<Option<(PathBuf, u64, Option<crate::records_index::Stamp>, Vec<Value>)>> = Mutex::new(None);
/// Drift checks of imported originals, by path and stamp.
static DRIFT: Mutex<Vec<(PathBuf, crate::records_index::Stamp, bool)>> = Mutex::new(Vec::new());

/// Sets the store this process writes (the App at startup). Replaces any earlier one.
pub fn configure(store: Result<Store, String>) {
    *STORE.write().unwrap_or_else(|p| p.into_inner()) = Some(store);
    *OPENED.lock().unwrap_or_else(|p| p.into_inner()) = None;
    *ROOTS.lock().unwrap_or_else(|p| p.into_inner()) = None;
    DIRS.lock().unwrap_or_else(|p| p.into_inner()).clear();
}

/// The process store exactly as configured (possibly none), without this
/// thread's test store or the environment default; for tests that restore it.
#[cfg(test)]
pub(crate) fn configured_for_test() -> Option<Result<Store, String>> {
    STORE.read().unwrap_or_else(|p| p.into_inner()).clone()
}
/// Puts back a store read by `configured_for_test`, clearing what `configure` clears.
#[cfg(test)]
pub(crate) fn restore_configured_for_test(store: Option<Result<Store, String>>) {
    *STORE.write().unwrap_or_else(|p| p.into_inner()) = store;
    *OPENED.lock().unwrap_or_else(|p| p.into_inner()) = None;
    *ROOTS.lock().unwrap_or_else(|p| p.into_inner()) = None;
    DIRS.lock().unwrap_or_else(|p| p.into_inner()).clear();
}

/// The configured store; without configuration, the override variable (and in
/// a test build its own temporary store). Never the App data folder.
pub fn current() -> Result<Store, String> {
    #[cfg(test)]
    if let Some(store) = TEST_STORE.with(|s| s.borrow().clone()) {
        return store;
    }
    if let Some(store) = STORE.read().unwrap_or_else(|p| p.into_inner()).clone() {
        return store;
    }
    let store = from_environment();
    let mut slot = STORE.write().unwrap_or_else(|p| p.into_inner());
    slot.get_or_insert(store).clone()
}

#[cfg(test)]
thread_local! { static TEST_STORE: std::cell::RefCell<Option<Result<Store, String>>> = const { std::cell::RefCell::new(None) }; }
/// A test's own store on this thread (placement, refusal and import tests),
/// without changing the store other tests use.
#[cfg(test)]
pub(crate) fn use_store_for_test(store: Option<Result<Store, String>>) {
    TEST_STORE.with(|s| *s.borrow_mut() = store);
}
#[cfg(test)]
thread_local! { static BOOTSTRAP_BLOCKED: std::cell::RefCell<Option<Box<dyn FnOnce()>>> = const { std::cell::RefCell::new(None) }; }
#[cfg(test)]
pub(crate) fn bootstrap_blocked_for_test(hook: Option<Box<dyn FnOnce()>>) {
    BOOTSTRAP_BLOCKED.with(|slot| *slot.borrow_mut() = hook);
}

fn from_environment() -> Result<Store, String> {
    // The override is for tests and development: a release build never reads it.
    if let Some(path) = std::env::var_os(OVERRIDE_ENV).filter(|p| (cfg!(debug_assertions) || cfg!(test)) && !p.is_empty()) {
        let root = PathBuf::from(path);
        if !root.is_absolute() {
            return Err(format!("{OVERRIDE_ENV} must name an absolute folder; no records store"));
        }
        return Ok(Store { root, placement: Placement::Override, limits: vec![] });
    }
    #[cfg(test)]
    {
        let root = std::env::temp_dir().join(format!("chirality-test-records-{}", std::process::id()));
        Ok(Store { root, placement: Placement::Test, limits: vec![] })
    }
    #[cfg(not(test))]
    Err(format!("no records store configured ({OVERRIDE_ENV} unset); nothing is recorded"))
}

/// The App's store at startup: the override (`CHIRALITY_RECORDS_STORE`) when
/// given; otherwise, in a release build, the person's chosen location or
/// `<App data>/records/`. A development build uses only the override, never
/// the real App data folder. `project` and `codex_homes` are the folders the
/// store must stay out of.
pub fn for_app(override_root: Option<PathBuf>, app_data: Result<&Path, String>, development: bool, project: Option<&Path>, codex_homes: &[PathBuf]) -> Result<Store, String> {
    // The override is honoured only in a development (or debug) build.
    let mut limits = Vec::new();
    let override_root = match override_root {
        Some(_) if !(development || cfg!(debug_assertions)) => {
            limits.push(format!("{OVERRIDE_ENV} is set but ignored: a release build keeps its records only in the App data folder or the location the person chose"));
            None
        }
        other => other,
    };
    let (root, placement) = if let Some(path) = override_root {
        (path, Placement::Override)
    } else if development {
        return Err(format!("development build: set {OVERRIDE_ENV} to a records store folder outside the project; the App data folder is not used in development, and nothing is recorded without a store"));
    } else {
        let data = app_data.map_err(|e| format!("App data folder unavailable, so no records store: {e}"))?;
        match chosen_location(data)? {
            Some(chosen) => (chosen, Placement::PersonChosen),
            None => (data.join("records"), Placement::AppData),
        }
    };
    if !root.is_absolute() {
        return Err("the records store must be an absolute folder; no records store".into());
    }
    // Refused in every build; only the development override may name a
    // temporary folder (a test store).
    let problems = placement_problems(&root, project, codex_homes, placement == Placement::Override);
    if !problems.is_empty() {
        return Err(format!("records store refused: {}", problems.join("; ")));
    }
    if placement == Placement::Override && is_temporary(&root) {
        limits.push(format!("{} is a temporary folder, which an agent under Codex's workspace-write sandbox can write (development override only)", root.display()));
    }
    Ok(Store { root, placement, limits })
}

/// The person's chosen store location, if one is recorded.
pub fn chosen_location(app_data: &Path) -> Result<Option<PathBuf>, String> {
    let path = app_data.join(CHOICE_FILE);
    match std::fs::read(&path) {
        Ok(bytes) => {
            let v: Value = serde_json::from_slice(&bytes).map_err(|e| format!("records store choice unreadable: {e}; no records store"))?;
            let location = v["location"].as_str().ok_or("records store choice names no location; no records store")?;
            Ok(Some(PathBuf::from(location)))
        }
        Err(e) if e.kind() == std::io::ErrorKind::NotFound => Ok(None),
        Err(e) => Err(format!("records store choice unreadable: {e}; no records store")),
    }
}

/// Records the person's chosen location for the next start. Records already
/// in the current store are not moved or copied.
pub fn choose_location(app_data: &Path, location: &Path, project: Option<&Path>, codex_homes: &[PathBuf]) -> Result<Value, String> {
    if !location.is_absolute() {
        return Err("choose an absolute folder for the records store".into());
    }
    let problems = placement_problems(location, project, codex_homes, false);
    if !problems.is_empty() {
        return Err(format!("records store location refused: {}", problems.join("; ")));
    }
    crate::storage::ensure_directory(app_data)?;
    crate::storage::replace_json(&app_data.join(CHOICE_FILE), &json!({"location": location.display().to_string(), "chosenAt": now_rfc3339()}))?;
    Ok(json!({"state":"chosen","location":location.display().to_string(),
        "takesEffect":"when the App next starts",
        "limit":"records already in the current store are not moved or copied; to keep one history, move the store folder to the new location before the App next starts"}))
}

/// Why `root` is not a fit place for the store: inside the project, a Codex
/// home or a temporary folder (each writable by an agent under Codex's
/// workspace-write sandbox, or the person's own Codex data).
pub fn placement_problems(root: &Path, project: Option<&Path>, codex_homes: &[PathBuf], allow_temporary: bool) -> Vec<String> {
    let resolved = resolve_lexically(root);
    let mut problems = Vec::new();
    let mut inside = |outer: &Path, what: &str| {
        let outer = resolve_lexically(outer);
        if resolved.starts_with(&outer) || outer.starts_with(&resolved) {
            problems.push(format!("{} overlaps {what} {}", root.display(), outer.display()));
        }
    };
    if let Some(project) = project {
        inside(project, "the project working tree");
    }
    for home in codex_homes {
        inside(home, "the Codex home");
    }
    if let Some(home) = std::env::var_os("HOME") {
        inside(&PathBuf::from(home).join(".codex"), "the Codex home");
    }
    if !allow_temporary && is_temporary(root) {
        problems.push(format!("{} is in a temporary folder (an agent under Codex's workspace-write sandbox can write there)", root.display()));
    }
    problems
}
fn is_temporary(root: &Path) -> bool {
    let resolved = resolve_lexically(root);
    [std::env::temp_dir(), PathBuf::from("/tmp")].iter().any(|t| resolved.starts_with(resolve_lexically(t)))
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

/// Cross-process ownership of cold identity bootstrap only.
fn bootstrap_lock(root: &Path) -> Result<crate::storage::Ownership, String> {
    let path = root.join(".store-bootstrap.lock");
    #[cfg(test)]
    if let Some(hook) = BOOTSTRAP_BLOCKED.with(|slot| slot.borrow_mut().take()) {
        // Expose an actual refused OS-lock attempt, not a pre-call marker.
        // Only the coordinating regression installs this scheduling hook.
        if let Some(guard) = crate::storage::try_lock_exclusive(&path)? { return Ok(guard); }
        hook();
    }
    crate::storage::lock(&path)
}

/// Opens the store: creates its folder and identity once, and returns its
/// canonical root and identity. An unreadable store is an error.
fn opened() -> Result<(PathBuf, String), String> {
    let store = current()?;
    {
        let cached = OPENED.lock().unwrap_or_else(|p| p.into_inner());
        if let Some((configured, root, id)) = cached.as_ref() {
            if *configured == store.root {
                if !root.is_dir(){return Err("the opened records store folder disappeared; no replacement store or project identity minted".into());}
                let bytes=crate::records_retention::read_plain(&root.join("store.json")).map_err(|e|format!("opened store identity unavailable; no replacement identity minted: {e}"))?;
                let identity:Value=serde_json::from_slice(&bytes).map_err(|e|format!("opened store identity unreadable: {e}"))?;
                if identity["format"]!=STORE_FORMAT || identity["storeId"]!=*id{return Err("opened records store identity changed; no silent reassociation".into());}
                return Ok((root.clone(), id.clone()));
            }
        }
    }
    if !store.root.exists() {
        // Each created folder and its link in the existing parent are synced
        // (ensure_directory), on the folder's physical path.
        crate::storage::ensure_directory(&resolve_lexically(&store.root)).map_err(|e| format!("records store unavailable: {}: {e}", store.root.display()))?;
    }

    let root = std::fs::canonicalize(&store.root).map_err(|e| format!("records store unavailable: {}: {e}", store.root.display()))?;
    if !root.is_dir() {
        return Err(format!("records store unavailable: {} is not a folder", root.display()));
    }
    let identity = root.join("store.json");
    let read = |path: &Path| -> Result<Option<String>, String> {
        match std::fs::symlink_metadata(path) {
            Ok(_) => {
                let bytes=crate::records_retention::read_plain(path)?;
                let v: Value = serde_json::from_slice(&bytes).map_err(|e| format!("records store unreadable: store.json: {e}"))?;
                if v["format"] != STORE_FORMAT {
                    return Err("records store unreadable: store.json is not a records store identity".into());
                }
                v["storeId"].as_str().map(|s| Some(s.to_owned())).ok_or_else(|| "records store unreadable: store.json names no identity".into())
            }
            Err(e) if e.kind() == std::io::ErrorKind::NotFound => Ok(None),
            Err(e) => Err(format!("records store unreadable: store.json: {e}")),
        }
    };
    let (id, _bootstrap) = match read(&identity) {
        // Preserve the existing strict read-only cold path. A valid single-link
        // identity needs no writable bootstrap control and may be read before
        // the publisher's final cleanup-directory sync or return, as before.
        Ok(Some(id)) => (id, None),
        _ => {
            // Missing/unreadable identity may be another opener's in-flight
            // create-once publication. Wait, then repeat the SAME strict read;
            // lock ownership never authorizes accepting or cleaning bad links.
            // This distinct guard is released before any returned source or
            // subsequent store/writer locking; cache misses under an already
            // held .store.lock must not re-acquire that non-reentrant lock.
            let bootstrap = bootstrap_lock(&root)?;
            let id = match read(&identity)? {
                Some(id) => id,
                None => {
                    let id = crate::util::opaque_id("records-store:")?;
                    let created = crate::storage::create_json(&identity, &json!({"format":STORE_FORMAT,"formatVersion":VERSION,"storeId":id,"createdAt":now_rfc3339()}));
                    match read(&identity)? {
                        Some(id) => id,
                        None => return Err(format!("records store unwritable: {}", created.err().unwrap_or_default())),
                    }
                }
            };
            (id, Some(bootstrap))
        }
    };
    *OPENED.lock().unwrap_or_else(|p| p.into_inner()) = Some((store.root.clone(), root.clone(), id.clone()));
    Ok((root, id))
}

/// The store's canonical root, when it is open and readable.
pub(crate) fn store_root() -> Option<PathBuf> {
    opened().ok().map(|(root, _)| root)
}

/// Identify an owning subtree without opening/creating store identity. Used by
/// low-level write admission; calling opened() here would recurse at bootstrap.
pub(crate) fn configured_project_dir(path: &Path) -> Option<PathBuf> {
    // A queued writer may already hold a source path when store configuration
    // becomes unavailable. Its known admission boundary must not disappear.
    if let Some(dir)=DIRS.lock().unwrap_or_else(|p|p.into_inner()).iter().rev().find(|(d,_)|path.starts_with(d)).map(|(d,_)|d.clone()){return Some(dir);}
    let configured = current().ok()?.root;
    let store = std::fs::canonicalize(&configured).unwrap_or(configured);
    let projects = store.join("projects");
    let rest = path.strip_prefix(&projects).ok()?;
    let key = rest.components().next()?;
    let key_text = key.as_os_str().to_str()?;
    if key_text.len()!=64 || !key_text.bytes().all(|b|b.is_ascii_hexdigit()) {return None;}
    Some(projects.join(key))
}

/// The store project folder holding `path` (`<store>/projects/<key>`), if any.
pub(crate) fn project_dir_of(path: &Path) -> Option<PathBuf> {
    let root = store_root()?;
    let rest = path.strip_prefix(root.join("projects")).ok()?;
    let key = rest.components().next()?;
    Some(root.join("projects").join(key))
}

/// The project root a store project folder was attached from in this process.
pub(crate) fn root_for_dir(dir: &Path) -> Option<PathBuf> {
    DIRS.lock().unwrap_or_else(|p| p.into_inner()).iter().rev().find(|(d, _)| d == dir).map(|(_, r)| r.clone())
}
pub(crate) fn known_project_root(root:&Path)->bool{DIRS.lock().unwrap_or_else(|p|p.into_inner()).iter().any(|(_,r)|r==root)}
fn remember(dir: &Path, root: &Path) {
    let mut dirs = DIRS.lock().unwrap_or_else(|p| p.into_inner());
    if !dirs.iter().any(|(d, r)| d == dir && r == root) {
        dirs.push((dir.to_path_buf(), root.to_path_buf()));
    }
}

fn store_lock(store: &Path) -> Result<crate::storage::Ownership, String> {
    crate::storage::lock(&store.join(".store.lock"))
}

/// Appends one JSON line, terminating a torn last line first, and syncs.
fn append_line(path: &Path, value: &Value) -> Result<(), String> {
    crate::storage::ensure_directory(path.parent().ok_or("record has no folder")?)?;
    let existing = std::fs::metadata(path).map(|m| m.len()).unwrap_or(0);
    let mut line = Vec::new();
    if existing > 0 {
        let mut f = std::fs::File::open(path).map_err(|e| format!("{}: {e}", path.display()))?;
        use std::io::{Seek, SeekFrom};
        f.seek(SeekFrom::Start(existing - 1)).map_err(|e| e.to_string())?;
        let mut last = [0u8; 1];
        f.read_exact(&mut last).map_err(|e| e.to_string())?;
        if last[0] != b'\n' {
            line.push(b'\n');
        }
    }
    line.extend(serde_json::to_vec(value).map_err(|e| e.to_string())?);
    line.push(b'\n');
    let mut f = std::fs::OpenOptions::new().create(true).append(true).open(path).map_err(|e| format!("{}: {e}", path.display()))?;
    f.write_all(&line).map_err(|e| format!("{}: write: {e}", path.display()))?;
    f.sync_all().map_err(|e| format!("{}: sync uncertain: {e}", path.display()))?;
    crate::storage::sync_dir(path.parent().unwrap())
}
/// The complete lines of an append-only store file (a torn last line is not read).
fn read_lines(path: &Path) -> Result<Vec<Value>, String> {
    let bytes = match std::fs::symlink_metadata(path) {
        Err(e) if e.kind() == std::io::ErrorKind::NotFound => return Ok(vec![]),
        Err(e) => return Err(format!("records store unreadable: {}: {e}",path.display())),
        Ok(_)=>crate::records_retention::read_plain(path).map_err(|e|format!("records store unreadable: {}: {e}",path.display()))?,
    };
    parse_lines(&bytes, path)
}
fn parse_lines(bytes: &[u8], path: &Path) -> Result<Vec<Value>, String> {
    let end = bytes.iter().rposition(|b| *b == b'\n').map_or(0, |i| i + 1);
    bytes[..end].split(|b| *b == b'\n').filter(|l| !l.is_empty()).map(|l| {
        serde_json::from_slice(l).map_err(|e| format!("records store unreadable: {}: {e}", path.display()))
    }).collect()
}

/// Every line of `<store>/roots.jsonl`, read again only as far as it grew.
fn roots(store: &Path) -> Result<Vec<Value>, String> {
    let path = store.join("roots.jsonl");
    let meta = match std::fs::metadata(&path) {
        Ok(m) => Some(m),
        Err(e) if e.kind() == std::io::ErrorKind::NotFound => None,
        Err(e) => return Err(format!("records store unreadable: roots.jsonl: {e}")),
    };
    let stamp = meta.as_ref().map(crate::records_index::Stamp::of);
    let mut cache = ROOTS.lock().unwrap_or_else(|p| p.into_inner());
    if let Some((p, _, s, lines)) = cache.as_ref() {
        if *p == path && *s == stamp {
            return Ok(lines.clone());
        }
    }
    let lines = read_lines(&path)?;
    *cache = Some((path, 0, stamp, lines.clone()));
    Ok(lines)
}
/// The project identities `root` is a current root of, by the roots record.
fn listed(lines: &[Value], root: &str) -> Vec<String> {
    let mut current: BTreeMap<String, bool> = BTreeMap::new();
    for line in lines.iter().filter(|l| l["root"] == root) {
        if let Some(project) = line["projectId"].as_str() {
            current.insert(project.to_owned(), line["how"] != "released");
        }
    }
    current.into_iter().filter(|(_, on)| *on).map(|(p, _)| p).collect()
}
/// The current roots of `project`.
fn roots_of(lines: &[Value], project: &str) -> Vec<String> {
    let mut current: BTreeMap<String, bool> = BTreeMap::new();
    for line in lines.iter().filter(|l| l["projectId"] == project) {
        if let Some(root) = line["root"].as_str() {
            current.insert(root.to_owned(), line["how"] != "released");
        }
    }
    current.into_iter().filter(|(_, on)| *on).map(|(r, _)| r).collect()
}

/// What the project's link file says.
#[derive(Clone, Debug, PartialEq)]
enum Link {
    Absent,
    Present { project: String, store: String },
    Unreadable(String),
}
fn read_link(root: &Path) -> Link {
    let path = root.join(PROJECT_LINK);
    if let Err(e) = crate::storage::check_path(&path) {
        return Link::Unreadable(e);
    }
    if let Err(e)=std::fs::symlink_metadata(&path){return if e.kind()==std::io::ErrorKind::NotFound{Link::Absent}else{Link::Unreadable(e.to_string())};}
    match crate::records_retention::read_plain(&path) {
        Ok(bytes) => match serde_json::from_slice::<Value>(&bytes) {
            Ok(v) if v["format"] == LINK_FORMAT => match (v["projectId"].as_str(), v["storeId"].as_str()) {
                (Some(p), Some(s)) if !p.is_empty() => Link::Present { project: p.to_owned(), store: s.to_owned() },
                _ => Link::Unreadable("the project file names no project identity".into()),
            },
            Ok(_) => Link::Unreadable("the project file is not a Chirality project link".into()),
            Err(e) => Link::Unreadable(format!("the project file is not JSON: {e}")),
        },
        Err(e) => Link::Unreadable(e),
    }
}
fn link_value(project: &str, store: &str) -> Value {
    json!({"format":LINK_FORMAT,"formatVersion":VERSION,"projectId":project,"storeId":store,
        "note":"A link to this project's records in the Chirality App's records store. The store's own record governs; editing this file only produces a limit."})
}

/// The project folder in the store for `project`.
pub(crate) fn project_dir(store: &Path, project: &str) -> PathBuf {
    store.join("projects").join(crate::storage::key(project))
}

/// How a project root stands with the store.
#[derive(Clone, Debug)]
pub struct Attachment {
    /// The canonical project root.
    pub root: PathBuf,
    /// The governing project identity (the store's), when attached.
    pub project: Option<String>,
    /// The project's store folder, when attached.
    pub dir: Option<PathBuf>,
    /// Visible identity limits; they do not refuse recording.
    pub limits: Vec<String>,
    /// Why nothing is attached (recording into the store is refused).
    pub refusal: Option<String>,
    /// "attached", "minted", "registered", "unattached", or "none" (no
    /// identity yet).
    pub how: &'static str,
    /// The identity the store recorded at this folder, when the folder is not
    /// attached to it (its link is missing or unreadable).
    pub recorded: Option<String>,
}
impl Attachment {
    pub fn view(&self) -> Value {
        json!({"root":self.root.display().to_string(),"projectId":self.project,"how":self.how,"limits":self.limits,"refusal":self.refusal,"recordedHere":self.recorded})
    }
}

/// Resolves `root` against the store. With `mint`, a project new to the store
/// gets an identity (link written first, then the store's records), and a
/// link whose identity the store does not know yet is registered; without it
/// nothing is written. `Err` only when the store or the root is unavailable.
pub fn attach(root: &Path, mint: bool) -> Result<Attachment, String> {
    let (store, store_id) = opened()?;
    // The physical project folder only: an alias (symlink) is refused, never
    // resolved into another folder's identity.
    crate::storage::check_path(root)?;
    let canonical = std::fs::canonicalize(root).map_err(|e| format!("project folder unavailable: {}: {e}", root.display()))?;
    if canonical != root {
        return Err(format!("project folder must be named by its physical path: {}", root.display()));
    }
    let _lock = if mint { Some(store_lock(&store)?) } else { None };
    package::require_root(&canonical)?;
    let lines = roots(&store)?;
    let at = canonical.to_str().ok_or("project folder is not Unicode; no project identity")?.to_owned();
    let listed = listed(&lines, &at);
    let link = read_link(&canonical);
    let mut out = Attachment { root: canonical.clone(), project: None, dir: None, limits: vec![], refusal: None, how: "attached", recorded: None };
    let attach_to = |out: &mut Attachment, project: &str| {
        let dir = project_dir(&store, project);
        remember(&dir, root);
        out.project = Some(project.to_owned());
        out.dir = Some(dir);
    };
    if listed.len() > 1 {
        out.refusal = Some(format!("the records store records this folder for several projects ({}); nothing attached until the person resolves it", listed.join(", ")));
        out.how = "unattached";
        return Ok(out);
    }
    match (&link, listed.first()) {
        (Link::Present { project, .. }, Some(y)) if project == y => attach_to(&mut out, y),
        (Link::Present { project, .. }, Some(y)) => {
            out.limits.push(format!("project file {PROJECT_LINK} names {project}, but the records store records this folder as {y}, which governs"));
            attach_to(&mut out, y);
        }
        // No usable link: never attached on its path alone (a new folder can
        // stand where a moved project was). The person restores the link or
        // gives the folder a new identity.
        (Link::Absent, Some(y)) => {
            out.refusal = Some(format!("link missing; not attached: project file {PROJECT_LINK} is missing, and the records store recorded project {y} at this folder; nothing is read or written for it until the person restores the link or gives this folder a new identity"));
            out.recorded = Some(y.clone());
            out.how = "unattached";
        }
        (Link::Unreadable(e), Some(y)) => {
            out.refusal = Some(format!("link unreadable; not attached: project file {PROJECT_LINK} is unreadable ({e}), and the records store recorded project {y} at this folder; nothing is read or written for it until the person restores the link or gives this folder a new identity"));
            out.recorded = Some(y.clone());
            out.how = "unattached";
        }
        (Link::Unreadable(e), None) => {
            out.refusal = Some(format!("project file {PROJECT_LINK} is unreadable ({e}) and the records store does not know this folder; nothing minted or attached"));
            out.how = "unattached";
        }
        (Link::Present { project, store: linked }, None) => {
            let elsewhere = roots_of(&lines, project);
            if !elsewhere.is_empty() {
                let holding: Vec<&String> = elsewhere.iter().filter(|r| matches!(read_link(Path::new(r)), Link::Present { project: ref p, .. } if p == project)).collect();
                out.how = "unattached";
                out.refusal = Some(if holding.is_empty() {
                    format!("this folder's project identity {project} is recorded at {} and not here; nothing attached until the person confirms this folder is that project (adopt) or gives it a new identity", elsewhere.join(", "))
                } else {
                    format!("duplicated project identity: {project} is also the identity of {}; nothing attached until the person gives this folder a new identity", holding.iter().map(|s| s.as_str()).collect::<Vec<_>>().join(", "))
                });
            } else if *linked != store_id {
                out.how = "unattached";
                out.refusal = Some(format!("this project's records were kept in another records store ({linked}); nothing attached here until the person adopts this project into this store"));
            } else if mint {
                register(&store, project, &at, "registered")?;
                out.limits.push(format!("the records store held no record of project {project}; registered from its project file"));
                out.how = "registered";
                attach_to(&mut out, project);
            } else {
                out.how = "none";
            }
        }
        (Link::Absent, None) => {
            if mint {
                let project = crate::util::opaque_id("chirality-project:")?;
                // The link first: an interruption leaves a link the store
                // registers on the next attach, never a store record whose
                // folder has lost its link.
                crate::storage::create_json(&canonical.join(PROJECT_LINK), &link_value(&project, &store_id))?;
                register(&store, &project, &at, "minted")?;
                out.how = "minted";
                attach_to(&mut out, &project);
            } else {
                out.how = "none";
            }
        }
    }
    if let Some(dir) = out.dir.as_deref() {
        let retention = crate::records_retention::view(dir);
        match retention["disposition"].as_str() {
            Some("disposed" | "disposal incomplete") => {},
            Some("unavailable") => out.refusal=Some(format!("retention state unavailable: {}",retention["limit"])),
            _ => {},
        }
    }
    Ok(out)
}

/// The store's identity record for `project` (once) and a roots line.
fn register(store: &Path, project: &str, root: &str, how: &str) -> Result<(), String> {
    let dir = project_dir(store, project);
    let record = dir.join("project.json");
    if !record.exists() {
        crate::records_retention::check_write(&dir)?;
        crate::storage::create_json(&record, &json!({"format":PROJECT_FORMAT,"formatVersion":VERSION,"projectId":project,"createdAt":now_rfc3339(),"how":how}))?;
    }
    append_line(&store.join("roots.jsonl"), &json!({"format":ROOT_FORMAT,"formatVersion":VERSION,"projectId":project,"root":root,"at":now_rfc3339(),"how":how}))
}

/// The project's imports as recorded: each import writes a "started" line
/// with its whole census before it copies anything, and a "completed" line
/// last. Only a completed import's files count as imported.
#[derive(Default)]
struct Imports {
    /// Lines in the file at all.
    any: bool,
    /// At least one import completed.
    completed: bool,
    /// The latest started import with no completion line.
    incomplete: Option<Value>,
    /// Imported originals (completed imports only): relative path ->
    /// (copy, sha256, stamp at import).
    covered: HashMap<String, (String, String, Value)>,
    /// Originals the latest completed import refused, with its reason.
    refused: HashMap<String, String>,
}
fn imports(dir: &Path) -> Result<Imports, String> {
    let lines = read_lines(&dir.join("imports.jsonl"))?;
    let mut out = Imports { any: !lines.is_empty(), ..Imports::default() };
    let done: std::collections::HashSet<&str> = lines.iter().filter(|l| l["event"] == "completed").filter_map(|l| l["importId"].as_str()).collect();
    for line in &lines {
        match line["event"].as_str() {
            Some("started") if !done.contains(line["importId"].as_str().unwrap_or_default()) => out.incomplete = Some(line.clone()),
            Some("completed") => {
                out.completed = true;
                out.incomplete = None;
                for file in line["files"].as_array().into_iter().flatten() {
                    if let (Some(original), Some(copy), Some(sha)) = (file["original"].as_str(), file["copy"].as_str(), file["sha256"].as_str()) {
                        out.covered.insert(original.to_owned(), (copy.to_owned(), sha.to_owned(), file["stamp"].clone()));
                    }
                }
                out.refused = line["conflicts"].as_array().into_iter().flatten()
                    .filter_map(|c| Some((c["original"].as_str()?.to_owned(), c["reason"].as_str()?.to_owned()))).collect();

            }
            _ => {}
        }
    }
    Ok(out)
}

/// Whether the store holds the project's records, so they are read from the
/// store: an import has completed, or (with no import ever started) the App
/// has written records there. Folders an interrupted import created do not
/// count: until its "completed" line, the history is read in place — unless
/// the store already held the project's records when that import started
/// (a late import): then the store is read, as before it started.
fn store_holds(dir: &Path) -> bool {
    if package::complete_exists(dir) { return true; }
    match imports(dir) {
        Ok(i) if i.completed => true,
        Ok(i) if i.incomplete.as_ref().is_some_and(|s| s["storeHeld"] == true) => true,
        Ok(i) if i.any => false,
        Ok(_) => ["runs", "acts", "workflow", "legacy", "connectors"].iter().any(|n| dir.join(n).exists()) || captures_hold_records(dir),
        // An unreadable import record: the store's state is unknown, so
        // writes are refused (`write_dir`) and the history is read in place.
        Err(_) => false,
    }
}

/// Export may acquire capture ownership before any capture was recorded.
/// That exact control file (or an empty folder) establishes no RS home. Any
/// unknown/non-control member or unreadable inventory remains conservative.
fn captures_hold_records(dir: &Path) -> bool {
    use std::os::unix::fs::MetadataExt;
    let folder = dir.join("captures");
    match std::fs::symlink_metadata(&folder) {
        Ok(meta) if meta.is_dir() => {},
        Ok(_) => return true,
        Err(error) => return error.kind() != std::io::ErrorKind::NotFound,
    }
    match std::fs::read_dir(folder) {
        Ok(mut entries) => entries.any(|entry|match entry {
            Ok(entry) if entry.file_name() == ".capture.lock" => !std::fs::symlink_metadata(entry.path()).is_ok_and(|m|m.is_file() && m.nlink()==1),
            _ => true,
        }),
        Err(_) => true,
    }
}
/// Whole retained payload export is distinct from ordinary RS source routing.
/// A fleet-only or role-observation-only store can be exported without importing nonexistent RS history;
/// it never hides real in-place history or bypasses an unfinished/unknown import.
pub(crate) fn export_permitted(dir: &Path, root: &Path) -> Result<(), String> {
    // The legacy import reader skips a torn last line for replay/recovery. An
    // export cannot interpret that uncertain state as no import ever started.
    let path=dir.join("imports.jsonl");
    match std::fs::symlink_metadata(&path) {
        Ok(_) => {
            let bytes=crate::records_retention::read_plain(&path).map_err(|error|format!("project import state is unknown; nothing exported: {error}"))?;
            if !bytes.is_empty() && !bytes.ends_with(b"\n") {
                return Err("project import state has an unclosed final line; nothing exported".into());
            }
        },
        Err(error) if error.kind()==std::io::ErrorKind::NotFound => {},
        Err(error) => return Err(format!("project import state is unknown; nothing exported: {error}")),
    }
    let state = imports(dir).map_err(|error|format!("project import state is unknown; nothing exported: {error}"))?;
    if state.incomplete.is_some() {
        return Err("project import incomplete; finish the explicit import before export".into());
    }
    if store_holds(dir) { return Ok(()); }
    if !state.any && ["fleet","role-supply"].iter().any(|name|std::fs::symlink_metadata(dir.join(name)).is_ok()) && legacy_census(root)?.is_empty() {
        return Ok(());
    }
    Err("project records need import before export".into())
}

/// Where a project's records are read and written now.
#[derive(Clone, Debug)]
pub(crate) struct Home {
    pub attachment: Attachment,
    /// The store holds this project's records: they are read from the store.
    /// Otherwise the project's §13.7 records (if any) are read in place.
    pub store_mode: bool,
}
/// The project's home for reading. An unavailable configured store never
/// falls back to retained originals, even with a missing project link. Explicit
/// library readers use their library's own log/capture paths independently.
pub(crate) fn home(root: &Path) -> Result<Home, String> {
    match attach(root, false) {
        Ok(attachment) => {
            if attachment.dir.is_none() {
                let identity=attachment.recorded.clone().or_else(||match read_link(root){Link::Present{project,..}=>Some(project),_=>None});
                if let Some(identity)=identity {
                    let store=opened()?.0;
                    if crate::records_retention::terminal(&project_dir(&store,&identity))? {return Err("project records disposed or disposal incomplete; its identity/link is unresolved, and retained project originals are not read".into());}
                }
            }
            if let Some(dir)=attachment.dir.as_deref(){if crate::records_retention::terminal(dir)?{return Err("project records disposed or disposal incomplete; ordinary project record reads are unavailable; administrative recovery and export verification remain separate".into());}}
            let store_mode = attachment.dir.as_deref().is_some_and(store_holds);
            Ok(Home { attachment, store_mode })
        }

        Err(e) => Err(e),
    }
}

/// The project's store folder for a write: attached (minted if new), and with
/// no §13.7 records waiting for import. Every refusal names its cause.
pub(crate) fn write_dir(root: &Path) -> Result<PathBuf, String> {
    let attachment = attach(root, true).map_err(|e| format!("nothing written: {e}"))?;
    let dir = attachment.dir.clone().ok_or_else(|| format!("no project identity in the records store; nothing written: {}", attachment.refusal.clone().unwrap_or_default()))?;
    write_permitted(&dir, &attachment.root)?;
    Ok(dir)
}
/// Whether the project's store folder may be written now: no import is
/// incomplete, and no project records wait for one.
fn write_permitted(dir: &Path, root: &Path) -> Result<(), String> {
    crate::records_retention::check_write(dir)?;
    let current=attach(root,false)?;
    if current.dir.as_deref()!=Some(dir) || current.refusal.is_some(){return Err("project root association changed; stale queued writer refused".into());}
    let state = imports(dir).map_err(|e| format!("the project's import record is unreadable, so whether its history is in the store is unknown; nothing written: {e}"))?;
    if let Some(started) = state.incomplete {
        return Err(format!("import incomplete: the import started at {} did not complete; run the import again before recording (nothing written; no history is split across two homes)", started["at"].as_str().unwrap_or("an unknown time")));
    }
    if !store_holds(dir) {
        let legacy = legacy_census(root)?;
        if !legacy.is_empty() {
            return Err(format!("import needed: {} record file(s) in this project ({}) are not in the records store; import them before recording. Until then nothing is recorded for the project, runs, acts, captures and connector accounts alike, so no history is split across two homes", legacy.len(), describe(&legacy)));
        }
    }
    Ok(())
}
/// The project's writer lock (shared for writers that do not wait on each
/// other), with the write permission checked again once it is held: an
/// import may have started, or stopped after only its "started" line, while
/// the writer waited. `dir` is a store project folder attached in this process.
pub(crate) fn writer_lock(dir: &Path, shared: bool) -> Result<crate::storage::Ownership, String> {
    let path = dir.join(".writer.lock");
    let lock = if shared { crate::storage::lock_shared(&path)? } else { crate::storage::lock(&path)? };
    let root = root_for_dir(dir).ok_or_else(|| format!("records store folder {} belongs to no project opened in this process; nothing written", dir.display()))?;
    write_permitted(dir, &root).map_err(|e| format!("nothing written: {e}"))?;
    Ok(lock)
}
/// The files waiting for import, by kind, for a person to read.
fn describe(files: &[LegacyFile]) -> String {
    let mut counts: BTreeMap<&str, usize> = BTreeMap::new();
    for f in files {
        let kind = match f.copy.split('/').next().unwrap_or_default() {
            "runs" | "acts" => "run/act log(s)",
            "workflow" => "WR workflow record(s)",
            "captures" => "capture file(s)",
            "legacy" => "registered legacy log",
            "connectors" => "connector route account file(s)",
            _ => "other record file(s)",
        };
        *counts.entry(kind).or_default() += 1;
    }
    counts.iter().map(|(k, n)| format!("{n} {k}")).collect::<Vec<_>>().join(", ")
}

/// A §13.7 project record file in place, and where its copy goes.
#[derive(Clone, Debug)]
pub(crate) struct LegacyFile {
    pub original: PathBuf,
    /// Relative to the project root.
    pub rel: String,
    /// Relative to the project's store folder.
    pub copy: String,
    /// Why the import does not copy it (a connector account entry that is a
    /// symbolic link, hard-linked or not a regular file): it is reported as
    /// a conflict and is not read from the store.
    pub refusal: Option<String>,
    /// The entry's stamp (device, inode, size, times) at the census, not
    /// following links; the import copies it only if the file it opens is
    /// still this one.
    pub stamp: Value,
}
/// The §13.7 project records in the project: run and act logs, WR WP-1
/// records, and capture evidence (with pending submissions) other than A15
/// captures, which stay with their library (U-STORE-2). The library's own act
/// log and the registered legacy log are not among them.
pub(crate) fn legacy_census(root: &Path) -> Result<Vec<LegacyFile>, String> {
    let mut out = Vec::new();
    let records = root.join(".chirality/records");
    let captures = root.join(".chirality/captures");
    fn list(dir: &Path) -> Result<Vec<(PathBuf, bool)>, String> {
        crate::storage::check_path(dir)?;
        let rd = match std::fs::read_dir(dir) {
            Ok(rd) => rd,
            Err(e) if e.kind() == std::io::ErrorKind::NotFound || e.kind() == std::io::ErrorKind::NotADirectory => return Ok(vec![]),
            Err(e) => return Err(format!("§13.7 records could not all be listed: {}: {e}", dir.display())),
        };
        let mut v = Vec::new();
        for entry in rd {
            let entry = entry.map_err(|e| e.to_string())?;
            let path = entry.path();
            if path.file_name().is_some_and(|n| n.to_string_lossy().starts_with('.')) {
                continue;
            }
            let meta = std::fs::symlink_metadata(&path).map_err(|e| e.to_string())?;
            if meta.file_type().is_symlink() {
                return Err(format!("owning path contains symlink: {}", path.display()));
            }
            v.push((path, meta.is_dir()));
        }
        v.sort();
        Ok(v)
    }
    let rel = |p: &Path| p.strip_prefix(root).map(|r| r.to_string_lossy().into_owned()).unwrap_or_default();
    let name = |p: &Path| p.file_name().map(|n| n.to_string_lossy().into_owned()).unwrap_or_default();
    let mut todo = vec![records.join("runs")];
    while let Some(dir) = todo.pop() {
        for (path, is_dir) in list(&dir)? {
            if is_dir {
                todo.push(path);
            } else if path.extension().is_some_and(|e| e == "jsonl") {
                let inner = path.strip_prefix(&records).unwrap().to_string_lossy().into_owned();
                out.push(LegacyFile { rel: rel(&path), copy: inner, original: path, refusal: None, stamp: Value::Null });
            }
        }
    }
    for (path, is_dir) in list(&records.join("acts"))? {
        if !is_dir && path.extension().is_some_and(|e| e == "jsonl") {
            out.push(LegacyFile { rel: rel(&path), copy: format!("acts/{}", name(&path)), original: path, refusal: None, stamp: Value::Null });
        }
    }
    for (path, is_dir) in list(&records.join("workflow"))? {
        if !is_dir && path.extension().is_some_and(|e| e == "json") {
            out.push(LegacyFile { rel: rel(&path), copy: format!("workflow/{}", name(&path)), original: path, refusal: None, stamp: Value::Null });
        }
    }
    for (dir, prefix, pending) in [(captures.clone(), "captures", false), (captures.join("pending"), "captures/pending", true)] {
        for (path, is_dir) in list(&dir)? {
            if is_dir || path.extension().is_none_or(|e| e != "json") {
                continue;
            }
            if !is_a15(&path, pending) {
                out.push(LegacyFile { rel: rel(&path), copy: format!("{prefix}/{}", name(&path)), original: path, refusal: None, stamp: Value::Null });
            }
        }
    }
    // The explicitly registered legacy log (§13.7) is project history too.
    let registered = root.join(crate::storage::LEGACY_LOG);
    crate::storage::check_path(&registered)?;
    if registered.is_file() {
        out.push(LegacyFile { rel: crate::storage::LEGACY_LOG.into(), copy: REGISTERED_COPY.into(), original: registered, refusal: None, stamp: Value::Null });
    }
    out.extend(connector_census(root)?);
    for file in &mut out {
        // A name that is not UTF-8 would be copied under a lossy name that
        // could collide with another: it is not copied.
        if file.refusal.is_none() && file.original.strip_prefix(root).map_or(true, |r| r.to_str().is_none()) {
            file.refusal = Some("its name is not UTF-8, so its copy could not keep it exactly; not copied".into());
        }
        if let Ok(meta) = std::fs::symlink_metadata(&file.original) {
            file.stamp = stamp_value(&meta);
        }
    }
    Ok(out)
}
/// The DEL-07-02 connector route accounts in the project (§13.8 "Split by who
/// writes"): every entry of the account folder, interrupted temporary files
/// (`.route-….tmp`) and other names included, so discovery in the store shows
/// what it showed in place. An entry the account reader would refuse in place
/// (a symbolic link, a hard-linked file, anything not a regular file) is
/// named with its refusal and never copied: a copy would be a clean file.
fn connector_census(root: &Path) -> Result<Vec<LegacyFile>, String> {
    use std::os::unix::fs::MetadataExt;
    let dir = root.join(crate::connector_route_store::LEGACY_DIRECTORY);
    crate::storage::check_path(&dir)?;
    let rd = match std::fs::read_dir(&dir) {
        Ok(rd) => rd,
        Err(e) if e.kind() == std::io::ErrorKind::NotFound || e.kind() == std::io::ErrorKind::NotADirectory => return Ok(vec![]),
        Err(e) => return Err(format!("connector route accounts could not all be listed: {}: {e}", dir.display())),
    };
    let mut out = Vec::new();
    for entry in rd {
        let entry = entry.map_err(|e| format!("connector route accounts could not all be listed: {e}"))?;
        let path = entry.path();
        let name = entry.file_name().to_string_lossy().into_owned();
        let meta = std::fs::symlink_metadata(&path).map_err(|e| format!("connector route accounts could not all be listed: {}: {e}", path.display()))?;
        let refusal = if meta.file_type().is_symlink() {
            Some("a symbolic link, which the account reader refuses; not copied".to_string())
        } else if !meta.is_file() {
            Some("not a regular file, which the account reader refuses; not copied".to_string())
        } else if meta.nlink() != 1 {
            Some("a hard-linked file, which the account reader refuses; not copied (a copy would be a clean file)".to_string())
        } else {
            None
        };
        out.push(LegacyFile { rel: format!("{}/{name}", crate::connector_route_store::LEGACY_DIRECTORY), copy: format!("{CONNECTOR_COPY}/{name}"), original: path, refusal, stamp: Value::Null });
    }
    out.sort_by(|a, b| a.rel.cmp(&b.rel));
    Ok(out)
}
/// Where imported (and new) connector route accounts are kept in a project's
/// store folder.
pub(crate) const CONNECTOR_COPY: &str = "connectors/route-accounts";
/// The project's records read log (§13.9) in its store folder.
pub(crate) const READ_LOG: &str = "reads/records-reads.jsonl";

/// §13.9: the project's records read log, in its store folder. The read log
/// is the App's own log, not §13.7 history, so it is written before an import
/// too. An agent's call never mints the project's identity (the App mints it
/// when it opens the project) and takes no store-wide lock: a project with no
/// identity yet, or one that cannot be attached, refuses, and nothing is
/// written elsewhere.
pub(crate) fn read_log_path(root: &Path) -> Result<PathBuf, String> {
    let attachment = attach(root, false).map_err(|e| format!("records store unavailable: {e}"))?;
    let dir = attachment.dir.ok_or_else(|| match attachment.refusal {
        Some(refusal) => format!("no project identity in the records store: {refusal}"),
        None => "the project has no records store identity yet (the App mints it when it opens the project; an agent's read does not); nothing recorded".into(),
    })?;
    Ok(dir.join(READ_LOG))
}

/// Where a project's connector route accounts are read now (DEL-07-02;
/// §13.8 "Split by who writes"): an anchor folder and the folder names below
/// it, opened one by one without following links.
#[derive(Clone, Debug)]
pub(crate) struct AccountsPlace {
    pub anchor: PathBuf,
    pub parts: Vec<String>,
    /// The project's store folder (writes go only there), when the place is the store.
    pub store_dir: Option<PathBuf>,
    /// Shown with the accounts: where they are read and why.
    pub location: String,
}
/// The project's accounts place. With `mint` (a writer opening them) the
/// project is attached and minted an identity if it has none; reading mints
/// nothing. Once the store holds the
/// project's records the accounts are in its store folder; before that,
/// accounts in the project are read in place (writes refused, "import
/// needed"); a project with none is placed in the store. A folder the store
/// cannot attach, or one with no identity yet, is read in place and written
/// nowhere.
pub(crate) fn route_accounts_place(root: &Path, mint: bool) -> Result<AccountsPlace, String> {
    // As `home`: with no store, a folder with no link is read in place and
    // written nowhere; a linked project with the store unavailable is an error.
    let store = match opened() {
        Ok((store, _)) => store,
        Err(e) if !mint && read_link(root) == Link::Absent && root.is_dir() => {
            return Ok(AccountsPlace {
                anchor: root.to_path_buf(),
                parts: crate::connector_route_store::LEGACY_DIRECTORY.split('/').map(str::to_owned).collect(),
                store_dir: None,
                location: format!("the project, read in place; nothing written: records store unavailable: {e}"),
            });
        }
        Err(e) => return Err(e),
    };
    let attachment = attach(root, mint)?;
    let in_place = || AccountsPlace {
        anchor: attachment.root.clone(),
        parts: crate::connector_route_store::LEGACY_DIRECTORY.split('/').map(str::to_owned).collect(),
        store_dir: None,
        location: String::new(),
    };
    let in_project = !connector_census(&attachment.root)?.is_empty();
    let Some(dir) = attachment.dir.clone() else {
        let mut place = in_place();
        place.location = match (&attachment.refusal, in_project) {
            (Some(refusal), _) => format!("the project, read in place; nothing written: {refusal}"),
            (None, true) => "the project, read in place: import needed before accounts are written in the records store".into(),
            (None, false) => "the project, read in place: no project identity in the records store yet (a writer opening the accounts mints it)".into(),
        };
        return Ok(place);
    };
    let store_mode = store_holds(&dir);
    if !store_mode && in_project {
        let mut place = in_place();
        place.location = "the project, read in place: import needed before accounts are written in the records store".into();
        return Ok(place);
    }
    let key = dir.file_name().ok_or("project store folder has no name")?.to_string_lossy().into_owned();
    let mut parts = vec!["projects".to_owned(), key.clone()];
    parts.extend(CONNECTOR_COPY.split('/').map(str::to_owned));
    Ok(AccountsPlace { anchor: store, parts, store_dir: Some(dir), location: format!("the records store (projects/{key}/{CONNECTOR_COPY})") })
}
/// Where the registered legacy log's imported copy is kept.
pub(crate) const REGISTERED_COPY: &str = "legacy/coordination.rs.jsonl";

/// Whether a capture file (or pending submission) in a §13.7 capture folder is
/// an A15 capture, which stays with its library. Read again only when the
/// file's stamp changes (the census runs on every host status).
fn is_a15(path: &Path, pending: bool) -> bool {
    static SEEN: std::sync::OnceLock<Mutex<HashMap<PathBuf, (crate::records_index::Stamp, bool)>>> = std::sync::OnceLock::new();
    let seen = SEEN.get_or_init(Default::default);
    let stamp = std::fs::metadata(path).ok().map(|m| crate::records_index::Stamp::of(&m));
    if let Some(stamp) = stamp {
        if let Some((s, a15)) = seen.lock().unwrap_or_else(|p| p.into_inner()).get(path) {
            if *s == stamp {
                return *a15;
            }
        }
    }
    let a15 = std::fs::read(path).ok().and_then(|b| serde_json::from_slice::<Value>(&b).ok()).is_some_and(|v| {
        (if pending { &v["capture"]["actKind"] } else { &v["actKind"] }) == "A15"
    });
    if let Some(stamp) = stamp {
        seen.lock().unwrap_or_else(|p| p.into_inner()).insert(path.to_path_buf(), (stamp, a15));
    }
    a15
}

/// Imported originals (completed imports only): relative path -> (copy,
/// sha256, stamp at import).
fn coverage(dir: &Path) -> Result<HashMap<String, (String, String, Value)>, String> {
    Ok(imports(dir)?.covered)
}
#[cfg(test)]
thread_local! {
    /// Stops an import after this many copies (an interruption).
    static IMPORT_STOP_AFTER: std::cell::Cell<Option<usize>> = const { std::cell::Cell::new(None) };
    /// Makes an import's read-back of its next copy disagree.
    static IMPORT_BAD_READBACK: std::cell::Cell<bool> = const { std::cell::Cell::new(false) };
}
#[cfg(test)]
thread_local! {
    /// Runs once between the import's census and its first read (a swap).
    pub(crate) static AFTER_CENSUS: std::cell::RefCell<Option<Box<dyn FnOnce()>>> = std::cell::RefCell::new(None);
}
#[cfg(test)]
pub(crate) fn interrupt_import_for_test(after: Option<usize>, bad_readback: bool) {
    IMPORT_STOP_AFTER.with(|c| c.set(after));
    IMPORT_BAD_READBACK.with(|c| c.set(bad_readback));
}
fn stamp_value(m: &std::fs::Metadata) -> Value {
    use std::os::unix::fs::MetadataExt;
    json!({"dev":m.dev(),"ino":m.ino(),"size":m.len(),"mtime":m.mtime(),"mtimeNs":m.mtime_nsec(),"ctime":m.ctime(),"ctimeNs":m.ctime_nsec()})
}
/// Reads an import original through one descriptor opened without following
/// links: it must be a regular, single-link file with the stamp the census
/// recorded, unchanged while it is read. Anything else is refused, never
/// copied: an entry swapped for a link, a hard link or other bytes after the
/// census would otherwise be copied as a clean file.
fn read_stable(path: &Path, census: &Value) -> Result<(Vec<u8>, std::fs::Metadata), String> {
    use std::os::unix::fs::{MetadataExt, OpenOptionsExt};
    let mut file = std::fs::OpenOptions::new()
        .read(true)
        .custom_flags(libc::O_NOFOLLOW | libc::O_NONBLOCK | libc::O_CLOEXEC)
        .open(path)
        .map_err(|e| format!("{} could not be opened without following links ({e}); not copied", path.display()))?;
    let before = file.metadata().map_err(|e| format!("{}: {e}", path.display()))?;
    if !before.is_file() {
        return Err(format!("{} is not a regular file; not copied", path.display()));
    }
    if before.nlink() != 1 {
        return Err(format!("{} is a hard-linked file; not copied (a copy would be a clean file)", path.display()));
    }
    if stamp_value(&before) != *census {
        return Err(format!("{} changed since the import's census (another file or other bytes); not copied", path.display()));
    }
    let mut bytes = Vec::new();
    file.read_to_end(&mut bytes).map_err(|e| format!("{}: {e}", path.display()))?;
    let after = file.metadata().map_err(|e| format!("{}: {e}", path.display()))?;
    if stamp_value(&before) != stamp_value(&after) || after.len() != bytes.len() as u64 {
        return Err(format!("{} changed while it was read; not copied", path.display()));
    }
    Ok((bytes, after))
}

/// RS §13.8 "Existing records": the person's explicit import of this
/// project's §13.7 records into the store. The import record is the commit
/// point: a "started" line names the whole census (each file's path, size and
/// SHA-256) before anything is copied, and a "completed" line is written last;
/// until it is, recording stays refused and the history is read in place.
/// Each file is copied byte for byte (created once, synced, then read back and
/// verified by SHA-256); a copy already present with the same bytes is kept,
/// so an interrupted import is resumed by running it again, never duplicated;
/// a copy present with other bytes is a conflict, never overwritten. A census
/// that changed since an interrupted import started is reported. Originals
/// are not changed.
pub fn import(root: &Path) -> Result<Value, String> {
    let (store, _) = opened()?;
    let attachment = attach(root, true)?;
    let dir = attachment.dir.clone().ok_or_else(|| format!("nothing imported: {}", attachment.refusal.clone().unwrap_or_default()))?;
    let _store = store_lock(&store)?;
    let _admission=crate::records_retention::write_path(&dir)?;
    // Writers wait while the copies are made (the logs' writer lock).
    let _writers = crate::storage::lock(&dir.join(".writer.lock"))?;
    let census = legacy_census(&attachment.root)?;
    let state = imports(&dir)?;
    // Read every original once, stably, before the started line names it.
    let mut read = Vec::new();
    let mut conflicts = Vec::new();
    for file in &census {
        if let Some(reason) = &file.refusal {
            conflicts.push(json!({"original":file.rel,"copy":file.copy,"reason":reason}));
            continue;
        }
        #[cfg(test)]
        if let Some(hook) = AFTER_CENSUS.with(|h| h.borrow_mut().take()) {
            hook();
        }
        match read_stable(&file.original, &file.stamp) {
            Ok((bytes, meta)) => read.push((file, sha256_hex(&bytes), bytes, meta)),
            Err(e) => conflicts.push(json!({"original":file.rel,"copy":file.copy,"reason":e})),
        }
    }
    // What changed since an interrupted import named its census.
    let mut census_changed = Vec::new();
    if let Some(started) = &state.incomplete {
        let before: HashMap<&str, &str> = started["census"].as_array().into_iter().flatten()
            .filter_map(|f| Some((f["original"].as_str()?, f["sha256"].as_str()?))).collect();
        for (file, sha, _, _) in &read {
            match before.get(file.rel.as_str()) {
                Some(old) if *old == sha => {}
                Some(_) => census_changed.push(format!("{} changed since the interrupted import started", file.rel)),
                None => census_changed.push(format!("{} appeared since the interrupted import started", file.rel)),
            }
        }
        for rel in before.keys().filter(|r| !read.iter().any(|(f, ..)| f.rel == **r)) {
            census_changed.push(format!("{rel} is no longer there since the interrupted import started"));
        }
    }
    let pending: Vec<_> = read.iter().filter(|(file, sha, ..)| state.covered.get(&file.rel).is_none_or(|(_, s, _)| s != sha)).collect();
    // A conflict is new unless the latest completed import already recorded
    // it with the same reason (a refused entry is reported, not re-imported).
    let fresh_conflict = conflicts.iter().any(|c| {
        let original = c["original"].as_str().unwrap_or_default();
        !state.covered.contains_key(original) && state.refused.get(original).map(String::as_str) != c["reason"].as_str()
    });
    if pending.is_empty() && !fresh_conflict && state.incomplete.is_none() {
        // Nothing new: an import repeated after it completed records nothing.
        let drifted: Vec<Value> = read.iter().filter_map(|(file, sha, ..)| {
            let (copy, imported, _) = state.covered.get(&file.rel)?;
            (imported != sha).then(|| json!({"original":file.rel,"copy":copy,"reason":format!("the original differs from its imported copy (sha256 {imported} at import); the records store copy governs and is not replaced")}))
        }).collect();
        conflicts.extend(drifted);
        return Ok(outcome(&attachment, None, census.len(), 0, read.len(), conflicts, census_changed));
    }
    let id = crate::util::opaque_id("import:")?;
    // Whether the store already held the project's records: a late import,
    // during which (and if it is interrupted) readers keep reading the store.
    let store_held = store_holds(&dir);
    let named: Vec<Value> = read.iter().map(|(file, sha, bytes, _)| json!({"original":file.rel,"copy":file.copy,"sha256":sha,"bytes":bytes.len()})).collect();
    append_line(&dir.join("imports.jsonl"), &json!({"format":IMPORT_FORMAT,"formatVersion":VERSION,"event":"started","importId":id,"at":now_rfc3339(),
        "root":attachment.root.display().to_string(),"method":"sha-256 of the exact bytes","census":named,"storeHeld":store_held,
        "resumes":state.incomplete.as_ref().map(|s| s["importId"].clone())}))?;
    let mut files = Vec::new();
    let (mut copied, mut present) = (0, 0);
    for (file, sha, bytes, meta) in &read {
        // Imported before: the store copy governs (it may have grown since);
        // an original that no longer matches is reported, never imported again.
        if let Some((copy, imported, _)) = state.covered.get(&file.rel) {
            if imported == sha {
                present += 1;
            } else {
                conflicts.push(json!({"original":file.rel,"copy":copy,"reason":format!("the original differs from its imported copy (sha256 {imported} at import); the records store copy governs and is not replaced")}));
            }
            continue;
        }
        let target = dir.join(&file.copy);
        crate::storage::check_path(&target)?;
        let outcome = match std::fs::read(&target) {
            Ok(existing) if existing == *bytes => {
                present += 1;
                "present"
            }
            Ok(existing) => {
                conflicts.push(json!({"original":file.rel,"copy":file.copy,"reason":format!("the store already holds a different file there (sha256 {}); not overwritten", sha256_hex(&existing))}));
                continue;
            }
            // A late log that would bring a record identity the store's set
            // already holds is not copied: R-1 counts each identity once.
            Err(e) if e.kind() == std::io::ErrorKind::NotFound && store_held && file.copy.ends_with(".jsonl")
                && !held_identities(&attachment.root, bytes).is_empty() => {
                let held = held_identities(&attachment.root, bytes);
                conflicts.push(json!({"original":file.rel,"copy":file.copy,"heldIdentities":held.iter().take(HELD_SHOWN).collect::<Vec<_>>(),"heldCount":held.len(),
                    "reason":format!("it holds record identities the records store already holds ({}); not copied, so each identity is counted once (R-1)", name_bounded(&held))}));
                continue;
            }
            Err(e) if e.kind() == std::io::ErrorKind::NotFound => {
                #[cfg(test)]
                if IMPORT_STOP_AFTER.with(|c| c.get()) == Some(copied) {
                    return Err("import interrupted (injected); it did not complete".into());
                }
                crate::storage::create_bytes(&target, bytes)?;
                #[allow(unused_mut)]
                let mut back = std::fs::read(&target).map_err(|e| format!("imported copy unreadable: {e}; the import did not complete"))?;
                #[cfg(test)]
                if IMPORT_BAD_READBACK.with(|c| c.get()) {
                    back.push(b'!');
                }
                if sha256_hex(&back) != *sha {
                    return Err(format!("imported copy of {} does not verify; the import stopped and did not complete", file.rel));
                }
                copied += 1;
                "copied"
            }
            Err(e) => return Err(format!("records store unreadable: {}: {e}; the import did not complete", target.display())),
        };
        files.push(json!({"original":file.rel,"copy":file.copy,"outcome":outcome,"sha256":sha,"bytes":bytes.len(),"stamp":stamp_value(meta)}));
    }
    append_line(&dir.join("imports.jsonl"), &json!({"format":IMPORT_FORMAT,"formatVersion":VERSION,"event":"completed","importId":id,"at":now_rfc3339(),
        "files":files,"conflicts":conflicts,"censusChanged":census_changed}))?;
    Ok(outcome(&attachment, Some(id), census.len(), copied, present, conflicts, census_changed))
}
/// Every record identity in a log's `bytes` that the project's record set
/// (the store, read through the index) already holds, in log order.
fn held_identities(root: &Path, bytes: &[u8]) -> Vec<String> {
    let ids: Vec<String> = bytes.split(|b| *b == b'\n').filter_map(|l| serde_json::from_slice::<Value>(l).ok())
        .filter_map(|v| v["recordId"].as_str().map(str::to_owned)).collect();
    let mut held = crate::records_index::with_index(root, |ix| ids.into_iter().filter(|id| ix.holds(id)).collect::<Vec<_>>());
    let mut seen = std::collections::HashSet::new();
    held.retain(|id| seen.insert(id.clone()));
    held
}
/// How many held identities a conflict names before "and N more".
const HELD_SHOWN: usize = 20;
fn name_bounded(ids: &[String]) -> String {
    let shown = ids.iter().take(HELD_SHOWN).cloned().collect::<Vec<_>>().join(", ");
    if ids.len() > HELD_SHOWN { format!("{shown}, and {} more", ids.len() - HELD_SHOWN) } else { shown }
}
/// What `import` reports, with the trust its copies carry.
fn outcome(attachment: &Attachment, id: Option<String>, census: usize, copied: usize, present: usize, conflicts: Vec<Value>, census_changed: Vec<String>) -> Value {
    json!({"state":if conflicts.is_empty(){"imported"}else{"imported with conflicts"},"importId":id,"projectId":attachment.project,
        "files":census,"copied":copied,"alreadyPresent":present,"conflicts":conflicts,"censusChanged":census_changed,
        "standing":IMPORT_STANDING})
}
/// The standing of imported copies (shown with every import, and in the host view).
pub const IMPORT_STANDING: &str = "Byte-identical copies verified by SHA-256; the store copies now govern, and the originals are kept unchanged and no longer read. An imported copy carries only the trust of the project folder it came from, which an agent could write: the import proves the copy equals the file, not who wrote it.";

/// The person confirms this folder is the project its link names (moved, or
/// kept in another store): the store records this folder as one of its roots.
pub fn adopt(root: &Path) -> Result<Value, String> {
    let (store, store_id) = opened()?;
    let canonical = std::fs::canonicalize(root).map_err(|e| e.to_string())?;
    let _lock = store_lock(&store)?;
    package::require_root(&canonical)?;
    let at = canonical.to_str().ok_or("project folder is not Unicode")?.to_owned();
    let lines = roots(&store)?;
    if !listed(&lines, &at).is_empty() {
        return Err("this folder is already attached; nothing adopted".into());
    }
    let Link::Present { project, store: linked } = read_link(&canonical) else {
        return Err("the project file names no identity to adopt; nothing adopted".into());
    };
    let _admission=crate::records_retention::read_path(&project_dir(&store,&project))?;
    if roots_of(&lines, &project).iter().any(|r| matches!(read_link(Path::new(r)), Link::Present { project: ref p, .. } if *p == project)) {
        return Err("another folder holds this project identity; give this folder a new identity instead; nothing adopted".into());
    }
    // Every earlier root of this identity is released (append-only lines), so
    // a new folder later made at an old path is not taken for this project.
    for earlier in roots_of(&lines, &project) {
        append_line(&store.join("roots.jsonl"), &json!({"format":ROOT_FORMAT,"formatVersion":VERSION,"projectId":project,"root":earlier,"at":now_rfc3339(),"how":"released","by":"adopt"}))?;
    }
    register(&store, &project, &at, "adopted")?;
    if linked != store_id {

        crate::storage::replace_json(&canonical.join(PROJECT_LINK), &link_value(&project, &store_id))?;
    }
    Ok(json!({"state":"adopted","projectId":project,"root":at}))
}

/// The person gives this folder a new identity (a copy, or another project
/// whose link was copied in): the folder is released from any identity the
/// store records for it, and a new one is minted and linked.
pub fn new_identity(root: &Path) -> Result<Value, String> {
    let (store, store_id) = opened()?;
    let canonical = std::fs::canonicalize(root).map_err(|e| e.to_string())?;
    let _lock = store_lock(&store)?;
    package::require_root(&canonical)?;
    let at = canonical.to_str().ok_or("project folder is not Unicode")?.to_owned();
    let prior = listed(&roots(&store)?, &at);
    let mut _admissions=Vec::new();
    for project in &prior {_admissions.push(crate::records_retention::read_path(&project_dir(&store,project))?);}
    if let Link::Present{project,..}=read_link(&canonical) {_admissions.push(crate::records_retention::read_path(&project_dir(&store,&project))?);}
    for project in prior {
        append_line(&store.join("roots.jsonl"), &json!({"format":ROOT_FORMAT,"formatVersion":VERSION,"projectId":project,"root":at,"at":now_rfc3339(),"how":"released"}))?;
    }
    let project = crate::util::opaque_id("chirality-project:")?;
    crate::storage::ensure_directory(&canonical.join(".chirality"))?;
    crate::storage::replace_json(&canonical.join(PROJECT_LINK), &link_value(&project, &store_id))?;
    register(&store, &project, &at, "minted")?;
    Ok(json!({"state":"new identity","projectId":project,"root":at,"limit":"records of the identity this folder had stay with that identity"}))
}

/// The person restores a missing, changed or unreadable project file to the
/// identity the store records for this folder.
pub fn restore_link(root: &Path) -> Result<Value, String> {
    let (store, store_id) = opened()?;
    let canonical = std::fs::canonicalize(root).map_err(|e| e.to_string())?;
    let _lock = store_lock(&store)?;
    package::require_root(&canonical)?;
    let at = canonical.to_str().ok_or("project folder is not Unicode")?.to_owned();
    let listed = listed(&roots(&store)?, &at);
    let [project] = listed.as_slice() else {
        return Err("the records store records no single identity for this folder; nothing restored".into());
    };
    let _admission=crate::records_retention::read_path(&project_dir(&store,project))?;
    crate::storage::ensure_directory(&canonical.join(".chirality"))?;
    crate::storage::replace_json(&canonical.join(PROJECT_LINK), &link_value(project, &store_id))?;
    Ok(json!({"state":"link restored","projectId":project,"root":at}))
}

/// Limits about the project's records that do not make its record set
/// incomplete (the store governs): identity limits, §13.7 records not
/// imported (not read), and imported originals that differ from their copies.
pub(crate) fn notes(root: &Path) -> Vec<String> {
    let home = match home(root) {
        Ok(h) => h,
        Err(e) => return vec![e],
    };
    let mut notes = home.attachment.limits.clone();
    if home.attachment.dir.as_deref().is_some_and(|d|crate::records_retention::terminal(d).unwrap_or(false)){notes.push("Records disposed or disposal incomplete; only surviving administration and export evidence remain. Retained project originals are not read or re-imported.".into());}
    if let Some(refusal) = &home.attachment.refusal {
        notes.push(refusal.clone());
    }
    let census = match legacy_census(&home.attachment.root) {
        Ok(c) => c,
        Err(e) => {
            notes.push(e);
            return notes;
        }
    };
    if !home.store_mode {
        if !census.is_empty() {
            notes.push(format!("import needed: {} record file(s) ({}) are read in place; all new recording for the project is refused until they are imported into the records store", census.len(), describe(&census)));
        }
        return notes;
    }
    let dir = home.attachment.dir.clone().unwrap();
    let covered = match coverage(&dir) {
        Ok(c) => c,
        Err(e) => {
            notes.push(e);
            return notes;
        }
    };
    let refused = imports(&dir).map(|i| i.refused).unwrap_or_default();
    for file in census {
        match covered.get(&file.rel) {
            None => match refused.get(&file.rel) {
                // Refused by the last completed import (each identity is counted once).
                Some(reason) => notes.push(format!("{} is a §13.7 record not imported into the records store: {reason}; it is not read", file.rel)),
                None => notes.push(format!("{} is a §13.7 record not imported into the records store; it is not read (import to include it)", file.rel)),
            },
            Some((copy, sha, stamp)) => {
                if drifted(&file.original, sha, stamp) {
                    notes.push(format!("{} differs from its imported copy {copy} (sha256 {sha} at import); the records store copy governs", file.rel));
                }
            }
        }
    }
    notes
}
fn drifted(path: &Path, sha: &str, stamp: &Value) -> bool {
    let Ok(meta) = std::fs::metadata(path) else { return true };
    if stamp_value(&meta) == *stamp {
        return false;
    }
    let now = crate::records_index::Stamp::of(&meta);
    let mut cache = DRIFT.lock().unwrap_or_else(|p| p.into_inner());
    if let Some((_, _, d)) = cache.iter().find(|(p, s, _)| p == path && *s == now) {
        return *d;
    }
    let d = std::fs::read(path).map_or(true, |b| sha256_hex(&b) != sha);
    cache.retain(|(p, _, _)| p != path);
    cache.push((path.to_path_buf(), now, d));
    d
}

/// Host status: which store the App writes, and the project's standing in it.
pub fn status(project: Option<&Path>) -> Value {
    let store = current();
    let mut out = match (&store, opened()) {
        (Ok(s), Ok((root, id))) => json!({"state":"available","root":root.display().to_string(),"configured":s.root.display().to_string(),"placement":s.placement.label(),"storeId":id,"limits":s.limits}),
        (Ok(s), Err(e)) => json!({"state":"unavailable","configured":s.root.display().to_string(),"placement":s.placement.label(),"error":e,"recording":"refused; no fallback"}),
        (Err(e), _) => json!({"state":"unavailable","error":e,"recording":"refused; no fallback"}),
    };
    if let Some(root) = project {
        out["packageImport"] = package::status(root);
        out["project"] = match home(root) {
            Ok(home) => {
                let census = legacy_census(&home.attachment.root).unwrap_or_default();
                let imports = home.attachment.dir.as_ref().and_then(|d| read_lines(&d.join("imports.jsonl")).ok()).map_or(0, |l| l.len());
                let covered = home.attachment.dir.as_ref().and_then(|d| coverage(d).ok()).unwrap_or_default();
                // §13.7 files no import has copied (all of them before the first).
                let to_import = census.iter().filter(|f| !covered.contains_key(&f.rel)).count();
                json!({"attachment":home.attachment.view(),
                    "retention":home.attachment.dir.as_deref().map(crate::records_retention::view),
                    "reading":if home.store_mode {"records store"} else if !census.is_empty() {"records in place in the project (import needed)"} else {"no records yet"},
                    "importNeeded":!home.store_mode && !census.is_empty(),
                    "legacyFiles":census.len(),"notImported":to_import,
                    "notImportedKinds":describe(&census.iter().filter(|f| !covered.contains_key(&f.rel)).cloned().collect::<Vec<_>>()),"imports":imports,"importStanding":IMPORT_STANDING,"notes":notes(root)})
            }
            Err(e) => {
                // Ordinary source refusal must not hide the surviving native
                // hold/recovery controls. Unattached terminal identities are
                // explicit too; absent retention never means disposed.
                match attach(root,false){
                    Ok(attachment)=>{
                        let dir=attachment.dir.clone().or_else(||attachment.recorded.as_ref().and_then(|id|opened().ok().map(|(store,_)|project_dir(&store,id))));
                        json!({"state":"unavailable","error":e,"reading":"ordinary project records unavailable","attachment":attachment.view(),"retention":dir.as_deref().map(crate::records_retention::view),"notes":[e]})
                    },
                    Err(_)=>json!({"state":"unavailable","error":e}),
                }
            },
        };
    }
    out
}

/// Test reads: `rel` in the project's store subtree if the folder already has
/// one, without minting; otherwise a path that does not exist.
#[cfg(test)]
pub(crate) fn existing(root: &Path, rel: &str) -> PathBuf {
    match attach(root, false).ok().and_then(|a| a.dir) {
        Some(dir) => dir.join(rel),
        None => root.join(".chirality/no-records-store-subtree").join(rel),
    }
}

#[cfg(test)]
#[path = "records_store_tests.rs"]
mod tests;
