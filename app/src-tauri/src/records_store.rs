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
//! and this store). The store's own records govern, and a folder is attached
//! only when its link and the store agree on its identity. A link that is
//! missing or unreadable, that names another identity or another store than
//! the store records for the folder (changed), or whose identity the store records at another
//! folder (moved, or copied) attaches nothing until the person resolves it:
//! restore the link, confirm the folder is the project its link names
//! (adopt), or give the folder a new identity. Nothing is minted over a
//! mismatch. `Attachment::resolutions` names the acts that apply.
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
#[path = "records_store_lines.rs"]
pub(crate) mod lines;
#[path = "records_store_witness.rs"]
pub(crate) mod witness;
// The witness reader, for other code to use (the Delegation lane's decision reader).
#[allow(unused_imports)]
pub(crate) use witness::{legacy_import_origin, LegacyOrigin};

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
/// The store this process opened, bound to the physical folder it found: the
/// configured path, the canonical root, the identity, and the device and
/// inode of the store's folder and of its `store.json`. A folder or identity
/// file put in their place afterwards is not this store.
#[derive(Clone, Debug)]
struct Bound {
    configured: PathBuf,
    root: PathBuf,
    id: String,
    folder: (u64, u64),
    identity: (u64, u64),
}
static OPENED: Mutex<Option<Bound>> = Mutex::new(None);
/// Existing process custody only; no store open, identity write or cache change.
/// Read-only consumers preserve an already opened store's identity/alias binding.
pub(crate) fn known_identity_for_read(configured: &Path, physical: &Path) -> Option<(PathBuf,String)> {
    OPENED.lock().unwrap_or_else(|p|p.into_inner()).as_ref()
        .filter(|b| b.configured == configured || b.root == physical)
        .map(|b|(b.root.clone(),b.id.clone()))
}
/// The device and inode of `path` itself (a link is not followed).
fn node(path: &Path) -> std::io::Result<(u64, u64)> {
    use std::os::unix::fs::MetadataExt;
    std::fs::symlink_metadata(path).map(|m| (m.dev(), m.ino()))
}
/// Store project folder -> the project root it was attached from in this process.
static DIRS: Mutex<Vec<(PathBuf, PathBuf)>> = Mutex::new(Vec::new());
/// The roots record, read: (length read, stamp of the file, the reading).
static ROOTS: Mutex<Option<(PathBuf, u64, Option<crate::records_index::Stamp>, lines::Read)>> = Mutex::new(None);
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
    let chosen = STORE.write().unwrap_or_else(|p| p.into_inner()).get_or_insert(store).clone();
    // A test build's own default store is created when it is first taken, as
    // the App creates its store when it starts: tests' readers create
    // nothing either.
    #[cfg(test)]
    if chosen.as_ref().is_ok_and(|s| s.placement == Placement::Test) {
        static CREATED: std::sync::atomic::AtomicBool = std::sync::atomic::AtomicBool::new(false);
        if !CREATED.swap(true, std::sync::atomic::Ordering::SeqCst) { let _ = created(); }
    }
    chosen
}

#[cfg(test)]
thread_local! { static TEST_STORE: std::cell::RefCell<Option<Result<Store, String>>> = const { std::cell::RefCell::new(None) }; }
/// A test's own store on this thread (placement, refusal and import tests),
/// without changing the store other tests use.
#[cfg(test)]
pub(crate) fn use_store_for_test(store: Option<Result<Store, String>>) {
    let given = store.as_ref().is_some_and(|s| s.is_ok());
    TEST_STORE.with(|s| *s.borrow_mut() = store);
    // As the App creates its store when it starts, before any reader asks
    // for it: a test's own store exists once it is given. Readers create
    // nothing, in tests as in the App.
    if given { let _ = created(); }
}
/// A test's own store on this thread without the App's start: the store is
/// not created (tests of what a reader does when no store exists yet).
#[cfg(test)]
pub(crate) fn use_store_not_started_for_test(store: Option<Result<Store, String>>) {
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
        let root = std::env::temp_dir().join(test_store_name());
        Ok(Store { root, placement: Placement::Test, limits: vec![] })
    }
    #[cfg(not(test))]
    Err(format!("no records store configured ({OVERRIDE_ENV} unset); nothing is recorded"))
}

/// A test build's default store, one per process. A process id alone is
/// reused by later processes, which then opened an earlier process's store
/// and met its records; a fresh nonce beside the id makes the store this
/// process's own. The process registers best-effort removal of its default
/// test store on normal exit. Kill or abort may leave it behind; the fresh
/// nonce prevents a later process from reusing it.
#[cfg(test)]
static TEST_STORE_NAME: std::sync::OnceLock<String> = std::sync::OnceLock::new();
#[cfg(test)]
fn test_store_name() -> &'static str {
    TEST_STORE_NAME.get_or_init(|| {
        extern "C" fn remove_test_store() {
            if let Some(name) = TEST_STORE_NAME.get() { let _ = std::fs::remove_dir_all(std::env::temp_dir().join(name)); }
        }
        // SAFETY: registers a plain function with no arguments, run once at exit.
        unsafe { libc::atexit(remove_test_store) };
        fresh_test_store_name(std::process::id())
    })
}
/// A new name for a test store of process `pid`: its id and a fresh nonce.
#[cfg(test)]
pub(crate) fn fresh_test_store_name(pid: u32) -> String {
    crate::util::opaque_id(&format!("chirality-test-records-{pid}-")).expect("a test store's nonce")
}

/// The App's store at startup: the override (`CHIRALITY_RECORDS_STORE`) when
/// given; otherwise, in a release build, the person's chosen location or
/// `<App data>/records/`. A development build uses only the override, never
/// the real App data folder. `project` and `codex_homes` are the folders the
/// store must stay out of.
///
/// Precondition: its production caller (`initialize_startup_consumers`)
/// calls it only after admission has admitted operational inputs, which a
/// start whose App data cannot be resolved and held never has
/// (`admitted_startup`). It answers truly only with complete protected-home
/// inputs: every Codex home in `codex_homes`, and the App data folder this
/// start uses, from which the folder reserved for the App's account homes is
/// computed. Given no App data, it cannot compute that reservation and, as a
/// function, still admits an explicit override; the App's start never gives
/// it that input.
pub fn for_app(override_root: Option<PathBuf>, app_data: Result<&Path, String>, development: bool, project: Option<&Path>, codex_homes: &[PathBuf]) -> Result<Store, String> {
    // The App data folder as placement needs it (its reserved folders),
    // taken before the branches below consume it.
    let data_for_placement: Option<&Path> = app_data.as_ref().ok().copied();
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
    let problems = placement_problems_in(&root, project, codex_homes, placement == Placement::Override, data_for_placement);
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
    let problems = placement_problems_in(location, project, codex_homes, false, Some(app_data));
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
    placement_problems_in(root, project, codex_homes, allow_temporary, None)
}
/// As `placement_problems`, with the App data folder known: the folder where
/// the App allocates its account homes (`desktop_startup::desktop_account_homes`)
/// is reserved, whether or not any home has been planned or created in it,
/// so a store equal to it, inside it or containing it is refused.
fn placement_problems_in(root: &Path, project: Option<&Path>, codex_homes: &[PathBuf], allow_temporary: bool, app_data: Option<&Path>) -> Vec<String> {
    let resolved = resolve_lexically(root);
    let mut problems = Vec::new();
    let mut inside = |outer: &Path, what: &str| {
        // An empty folder name is an invalid input, refused by name: never
        // compared, so it neither overlaps everything nor nothing.
        if outer.as_os_str().is_empty() {
            problems.push(format!("{what} is given as an empty path, an invalid input, so whether {} overlaps it cannot be established", root.display()));
            return;
        }
        // Never compared while still relative: a relative folder would never
        // overlap an absolute store and so would pass silently. Made absolute
        // against the App's own working folder (the caller has already added
        // the resolution its child uses); a folder that cannot be made
        // absolute is a refusal, never "no overlap".
        let outer = match resolve_lexically(outer) {
            relative if relative.is_relative() => match std::path::absolute(&relative) {
                Ok(absolute) => resolve_lexically(&absolute),
                Err(e) => {
                    problems.push(format!("{what} {} could not be made absolute ({e}), so whether {} overlaps it is not known", relative.display(), root.display()));
                    return;
                }
            },
            resolved_outer => resolved_outer,
        };
        if resolved.starts_with(&outer) || outer.starts_with(&resolved) {
            problems.push(format!("{} overlaps {what} {}", root.display(), outer.display()));
        }
    };
    if let Some(project) = project {
        inside(project, "the project working tree");
    }
    if let Some(data) = app_data {
        inside(&crate::desktop_startup::desktop_account_homes(data), "the folder reserved for the App's account homes");
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
pub(crate) fn resolve_lexically(path: &Path) -> PathBuf {
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

/// The store as it exists: its canonical root and identity. Never creates,
/// locks or repairs anything, so every reader can call it: where the store's
/// folder or identity is absent or unreadable it is an error that says so. A
/// process that has opened the store stays bound to that physical folder and
/// identity; a configured alias redirected afterwards is not followed.
fn opened() -> Result<(PathBuf, String), String> {
    open(false)
}
/// `opened`, for a caller outside this module that compares the store it is
/// about to read with one it inspected.
pub(crate) fn opened_existing() -> Result<(PathBuf, String), String> {
    open(false)
}
/// Opens the store for writing, creating its folder and identity once. Only
/// the App's start and the entry points that write for the person call it
/// (`attach` with `mint`, the imports and the identity acts).
fn created() -> Result<(PathBuf, String), String> {
    open(true)
}
/// The App creates its store when it starts, before any reader asks for it.
pub fn create_at_startup() -> Result<(), String> {
    created().map(|_| ())
}
fn open(create: bool) -> Result<(PathBuf, String), String> {
    let store = current()?;
    {
        let cached = OPENED.lock().unwrap_or_else(|p| p.into_inner());
        if let Some(bound) = cached.as_ref().filter(|b| b.configured == store.root) {
            return still_bound(bound);
        }
    }
    // Only a store that is not there is "not created yet"; one that cannot
    // be examined is reported with that cause (S1).
    let there = crate::records_inspect::presence(&store.root).map_err(|e| format!("records store unavailable: {}: {e}", store.root.display()))?.is_some();
    if !there {
        if !create {
            return Err(format!("records store not created yet: {} does not exist; a read creates nothing", store.root.display()));
        }
        // Each created folder and its link in the existing parent are synced
        // (ensure_directory), on the folder's physical path.
        crate::storage::ensure_directory(&resolve_lexically(&store.root)).map_err(|e| format!("records store unavailable: {}: {e}", store.root.display()))?;
    }

    let root = std::fs::canonicalize(&store.root).map_err(|e| format!("records store unavailable: {}: {e}", store.root.display()))?;
    match crate::records_inspect::presence(&root) {
        Ok(Some(meta)) if meta.is_dir() => {}
        Ok(Some(_)) | Ok(None) => return Err(format!("records store unavailable: {} is not a folder", root.display())),
        Err(e) => return Err(format!("records store unavailable: {}: {e}", root.display())),
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
    let folder = node(&root).map_err(|e| format!("records store unavailable: {}: {e}", root.display()))?;
    let (id, _bootstrap) = match read(&identity) {
        // Preserve the existing strict read-only cold path. A valid single-link
        // identity needs no writable bootstrap control and may be read before
        // the publisher's final cleanup-directory sync or return, as before.
        Ok(Some(id)) => (id, None),
        // A read never takes the bootstrap lock (it would create it) and
        // never publishes an identity: the store is not there to read.
        Ok(None) if !create => return Err(format!("records store not created yet: {} holds no store identity; a read creates nothing", root.display())),
        Err(e) if !create => return Err(e),
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
    // Bound to the folder and identity file as found: the folder's node read
    // before the identity, and again after it, must agree.
    let identity_node = node(&identity).map_err(|e| format!("records store unreadable: store.json: {e}"))?;
    if node(&root).ok() != Some(folder) {
        return Err(format!("records store folder {} changed while it was opened; nothing read or written there", root.display()));
    }
    *OPENED.lock().unwrap_or_else(|p| p.into_inner()) = Some(Bound { configured: store.root.clone(), root: root.clone(), id: id.clone(), folder, identity: identity_node });
    #[cfg(test)]
    after_bind();
    Ok((root, id))
}
/// The opened store, checked again: the same physical folder (device and
/// inode) holding the same `store.json` file with the same identity. A folder
/// put at the store's path in its place, even holding a copy of its identity
/// file, is refused; nothing is read, written, created or minted there.
fn still_bound(bound: &Bound) -> Result<(PathBuf, String), String> {
    match node(&bound.root) {
        Err(e) if e.kind() == std::io::ErrorKind::NotFound => return Err("the opened records store folder disappeared; no replacement store or project identity minted".into()),
        Err(e) => return Err(format!("the opened records store folder is unavailable: {}: {e}", bound.root.display())),
        Ok(at) if at != bound.folder || !bound.root.is_dir() => return Err(format!("the opened records store folder {} was replaced by another folder; it is not the store this App opened, so nothing is read or written there and no replacement store or project identity is minted", bound.root.display())),
        Ok(_) => {}
    }
    let file = bound.root.join("store.json");
    match node(&file) {
        Ok(at) if at == bound.identity => {}
        Ok(_) => return Err(format!("the records store's identity file {} was replaced since this App opened the store (for example, restored from a backup), so nothing is read or written through it; reopening the App opens the store afresh", file.display())),
        Err(e) => return Err(format!("opened store identity unavailable; no replacement identity minted: {e}")),
    }
    let bytes = crate::records_retention::read_plain(&file).map_err(|e| format!("opened store identity unavailable; no replacement identity minted: {e}"))?;
    let identity: Value = serde_json::from_slice(&bytes).map_err(|e| format!("opened store identity unreadable: {e}"))?;
    if identity["format"] != STORE_FORMAT || identity["storeId"] != bound.id.as_str() {
        return Err("opened records store identity changed; no silent reassociation".into());
    }
    #[cfg(test)]
    after_bind();
    Ok((bound.root.clone(), bound.id.clone()))
}
// A test seam inside one read: runs once, right after the next opening binds
// or checks the store (so between that step of a read and the next).
#[cfg(test)]
thread_local! { static AFTER_OPEN: std::cell::RefCell<Option<Box<dyn FnOnce()>>> = const { std::cell::RefCell::new(None) }; }
#[cfg(test)]
fn after_bind() {
    if let Some(hook) = AFTER_OPEN.with(|h| h.borrow_mut().take()) { hook(); }
}
#[cfg(test)]
pub(crate) fn after_open_for_test(hook: Option<Box<dyn FnOnce()>>) {
    AFTER_OPEN.with(|h| *h.borrow_mut() = hook);
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
    // The store this process bound (its physical folder, whatever the
    // configured path names now), then the configured store.
    let bound = OPENED.lock().unwrap_or_else(|p|p.into_inner()).as_ref().map(|b| b.root.clone());
    let configured = current().ok().map(|s| std::fs::canonicalize(&s.root).unwrap_or(s.root));
    bound.into_iter().chain(configured).find_map(|store| {
        let projects = store.join("projects");
        let rest = path.strip_prefix(&projects).ok()?;
        let key = rest.components().next()?;
        let key_text = key.as_os_str().to_str()?;
        if key_text.len()!=64 || !key_text.bytes().all(|b|b.is_ascii_hexdigit()) {return None;}
        Some(projects.join(key))
    })
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

/// Appends one JSON line to a store line file (`roots.jsonl`, an
/// `imports.jsonl`, `legacy-imports.jsonl`), under the store lock, so that the
/// append never changes the meaning of bytes already in the file (`lines`).
/// A new file is made whole or not at all (its first line written to a
/// temporary file beside it, synced, and put in place by an exclusive rename).
/// An existing file has every fragment closed and named first, then the line,
/// all in one write, then a sync. A file not read whole is refused, as is the
/// registry while an interrupted package import is still writing it; either
/// way its bytes are left exactly as they were.
fn append_line(path: &Path, value: &Value) -> Result<(), String> {
    let parent = path.parent().ok_or("record has no folder")?;
    crate::storage::ensure_directory(parent)?;
    let mut line = serde_json::to_vec(value).map_err(|e| e.to_string())?;
    line.push(b'\n');
    let existing = match std::fs::symlink_metadata(path) {
        Err(e) if e.kind() == std::io::ErrorKind::NotFound => {
            refuse_pending_registry(path, b"")?;
            return create_whole(path, &line);
        }
        Err(e) => return Err(format!("records store unreadable: {}: {e}; nothing in it changed", path.display())),
        Ok(_) => crate::records_retention::read_plain(path).map_err(|e| format!("records store unreadable: {}: {e}; nothing in it changed", path.display()))?,
    };
    refuse_pending_registry(path, &existing)?;
    let read = lines::read(&existing, path);
    if !read.whole {
        return Err(lines::not_read_whole(path, &read.limits));
    }
    let mut bytes = read.recovery()?;
    bytes.extend(line);
    write_appending(path, &bytes)
}
/// The registry's bytes are left untouched while an interrupted package
/// import's frozen registry write is pending over them (its own recovery
/// appends the rest of that write; `publish_roots`).
fn refuse_pending_registry(path: &Path, existing: &[u8]) -> Result<(), String> {
    if path.file_name().is_some_and(|n| n == "roots.jsonl") && package::roots_write_pending(path.parent().ok_or("record has no folder")?, existing)? {
        return Err("an interrupted package import's write to the registry of project folders is pending; finish that import first; nothing in the registry changed".into());
    }
    Ok(())
}
#[cfg(test)]
#[derive(Clone, Copy, Debug, PartialEq)]
pub(crate) enum AppendStop {
    /// Stop before anything is written (an existing file), or before the
    /// temporary file is put in place (a new file).
    BeforeWrite,
    /// Write only this many bytes of the append's one write, then stop.
    AfterBytes(usize),
    /// Write everything, then stop before the sync.
    BeforeSync,
}
#[cfg(test)]
thread_local! {
    static APPEND_STOP: std::cell::Cell<Option<AppendStop>> = const { std::cell::Cell::new(None) };
    static APPEND_SKIP: std::cell::Cell<usize> = const { std::cell::Cell::new(0) };
}
/// Stops this thread's next store line write at `stop` (an interruption).
#[cfg(test)]
pub(crate) fn interrupt_append_for_test(stop: Option<AppendStop>) {
    interrupt_append_after_for_test(0, stop);
}
/// Lets `skip` store line writes on this thread complete, then stops the next at `stop`.
#[cfg(test)]
pub(crate) fn interrupt_append_after_for_test(skip: usize, stop: Option<AppendStop>) {
    APPEND_SKIP.with(|c| c.set(skip));
    APPEND_STOP.with(|c| c.set(stop));
}
#[cfg(test)]
fn append_stop() -> Option<AppendStop> {
    APPEND_STOP.with(|c| c.get())?;
    if APPEND_SKIP.with(|c| c.get()) > 0 {
        APPEND_SKIP.with(|c| c.set(c.get() - 1));
        return None;
    }
    APPEND_STOP.with(|c| c.take())
}
/// A new store line file, whole or not at all.
fn create_whole(path: &Path, bytes: &[u8]) -> Result<(), String> {
    let parent = path.parent().ok_or("record has no folder")?;
    let temp = parent.join(format!(".{}.{}.tmp", path.file_name().unwrap_or_default().to_string_lossy(), crate::util::opaque_id("")?));
    let result = (|| {
        let mut f = std::fs::OpenOptions::new().create_new(true).write(true).open(&temp).map_err(|e| format!("{}: {e}; nothing changed", temp.display()))?;
        f.write_all(bytes).map_err(|e| format!("{}: write: {e}; nothing changed", temp.display()))?;
        f.sync_all().map_err(|e| format!("{}: sync: {e}; nothing changed", temp.display()))?;
        #[cfg(test)]
        if append_stop().is_some() {
            return Err("store line write interrupted (injected) before the new file was put in place".to_string());
        }
        crate::records_export::publish(&temp, path).map_err(|e| format!("{}: {e}; nothing changed", path.display()))?;
        crate::storage::sync_dir(parent).map_err(|e| format!("{}: sync uncertain: {e}", path.display()))
    })();
    if temp.exists() {
        let _ = std::fs::remove_file(&temp);
    }
    result
}
/// One write appended to an existing store line file, then synced. The file
/// is never created here.
fn write_appending(path: &Path, bytes: &[u8]) -> Result<(), String> {
    use std::os::unix::fs::OpenOptionsExt;
    let mut f = std::fs::OpenOptions::new().append(true).custom_flags(libc::O_NOFOLLOW).open(path).map_err(|e| format!("{}: {e}; nothing changed", path.display()))?;
    #[cfg(test)]
    match append_stop() {
        Some(AppendStop::BeforeWrite) => return Err("store line write interrupted (injected) before the write".into()),
        Some(AppendStop::AfterBytes(n)) => {
            f.write_all(&bytes[..n.min(bytes.len())]).map_err(|e| e.to_string())?;
            f.sync_all().map_err(|e| e.to_string())?;
            return Err("store line write interrupted (injected) during the write".into());
        }
        Some(AppendStop::BeforeSync) => {
            f.write_all(bytes).map_err(|e| e.to_string())?;
            return Err("store line write interrupted (injected) before the sync".into());
        }
        None => {}
    }
    f.write_all(bytes).map_err(|e| format!("{}: write: {e}", path.display()))?;
    #[cfg(test)]
    crate::storage::publication_sync_for_test(path, crate::storage::PublicationSyncStage::File)?;
    f.sync_all().map_err(|e| format!("{}: sync uncertain: {e}", path.display()))?;
    #[cfg(test)]
    crate::storage::publication_sync_for_test(path, crate::storage::PublicationSyncStage::Directory)?;
    crate::storage::sync_dir(path.parent().unwrap())
}
/// Closes and names the fragments of one store line file, writing nothing
/// else (startup). Returns what was left as it was, and why.
fn recover_file(path: &Path) -> Result<Option<String>, String> {
    let existing = match std::fs::symlink_metadata(path) {
        Err(e) if e.kind() == std::io::ErrorKind::NotFound => return Ok(None),
        Err(e) => return Err(format!("{}: {e}", path.display())),
        Ok(_) => crate::records_retention::read_plain(path).map_err(|e| format!("{}: {e}", path.display()))?,
    };
    let read = lines::read(&existing, path);
    if !read.whole {
        return Ok(Some(lines::not_read_whole(path, &read.limits)));
    }
    let bytes = read.recovery()?;
    if bytes.is_empty() {
        return Ok(None);
    }
    if let Err(refusal) = refuse_pending_registry(path, &existing) {
        return Ok(Some(refusal));
    }
    write_appending(path, &bytes).map(|_| None)
}
/// Once at startup, under the store lock: every fragment in the store's line
/// files (the registry, each project's import account and the legacy import
/// witness) is closed and named, and the witness of legacy imports is begun
/// if it has not been (`witness`). A store not yet created is left alone. Returns what was left as it was.
pub fn recover_at_startup() -> Result<Vec<String>, String> {
    let configured = current()?;
    // Only a store that is not there is left alone; one whose record cannot
    // be examined is not a store not yet created. What recovery could not
    // examine is shown, never passed over as though nothing were there.
    let record = configured.root.join("store.json");
    match std::fs::symlink_metadata(&record) {
        Ok(_) => {}
        Err(e) if e.kind() == std::io::ErrorKind::NotFound => return Ok(vec![]),
        Err(e) => return Err(format!("records store unreadable: {}: {e}", record.display())),
    }
    let (store, _) = opened()?;
    let _lock = store_lock(&store)?;
    let mut left = Vec::new();
    left.extend(recover_file(&store.join("roots.jsonl"))?);
    left.extend(recover_file(&store.join(witness::WITNESS_FILE))?);
    let projects = store.join("projects");
    let mut dirs: Vec<PathBuf> = Vec::new();
    match std::fs::read_dir(&projects) {
        Ok(rd) => for entry in rd {
            match entry {
                Ok(entry) => dirs.push(entry.path()),
                Err(e) => left.push(format!("{}: a project folder could not be listed ({e}), so its import account could not be examined; left as it is", projects.display())),
            }
        },
        Err(e) if e.kind() == std::io::ErrorKind::NotFound => {}
        Err(e) => return Err(format!("records store unreadable: {}: {e}", projects.display())),
    }
    dirs.sort();
    for dir in dirs {
        let path = dir.join("imports.jsonl");
        match std::fs::symlink_metadata(&path) {
            Ok(_) => {}
            Err(e) if e.kind() == std::io::ErrorKind::NotFound => continue,
            Err(e) => {
                left.push(format!("{}: could not be examined ({e}); left as it is", path.display()));
                continue;
            }
        }
        if let Err(e) = crate::records_retention::check_write(&dir) {
            left.push(format!("{}: left as it is: {e}", path.display()));
            continue;
        }
        left.extend(recover_file(&path)?);
    }
    // A witness that cannot begin now (the projects present could not be
    // listed whole) is a limit shown, not a failed recovery: it begins at a
    // later start, or the act that needs it is refused.
    match witness::begin(&store) {
        Ok(not_established) => left.extend(not_established),
        Err(e) => left.push(e),
    }
    Ok(left)
}
/// The readable lines of a store line file (the shared reading), or the
/// refusal when it was not read whole; a missing file reads as empty.
fn read_lines(path: &Path) -> Result<Vec<Value>, String> {
    read_store_file(path)?.require_whole(path)
}
/// A store line file as read by the one shared reading (`lines`); a missing
/// file reads as empty.
fn read_store_file(path: &Path) -> Result<lines::Read, String> {
    let bytes = match std::fs::symlink_metadata(path) {
        Err(e) if e.kind() == std::io::ErrorKind::NotFound => return Ok(lines::read(b"", path)),
        Err(e) => return Err(format!("records store unreadable: {}: {e}",path.display())),
        Ok(_)=>crate::records_retention::read_plain(path).map_err(|e|format!("records store unreadable: {}: {e}",path.display()))?,
    };
    Ok(lines::read(&bytes, path))
}
/// The readable lines of a store line file's `bytes` (the shared reading), or
/// the refusal when they were not read whole.
fn parse_lines(bytes: &[u8], path: &Path) -> Result<Vec<Value>, String> {
    lines::read(bytes, path).require_whole(path)
}

/// Every readable line of `<store>/roots.jsonl`, or the refusal when the
/// registry was not read whole.
fn roots(store: &Path) -> Result<Vec<Value>, String> {
    let (values, whole, limits) = roots_read(store)?;
    if whole { Ok(values) } else { Err(lines::not_read_whole(&store.join("roots.jsonl"), &limits)) }
}
/// The registry as read (its readable lines, whether it was read whole, and
/// its limits), read again only when its stamp changes.
fn roots_read(store: &Path) -> Result<(Vec<Value>, bool, Vec<String>), String> {
    let path = store.join("roots.jsonl");
    let meta = match std::fs::metadata(&path) {
        Ok(m) => Some(m),
        Err(e) if e.kind() == std::io::ErrorKind::NotFound => None,
        Err(e) => return Err(format!("records store unreadable: roots.jsonl: {e}")),
    };
    let stamp = meta.as_ref().map(crate::records_index::Stamp::of);
    let mut cache = ROOTS.lock().unwrap_or_else(|p| p.into_inner());
    if let Some((p, _, s, read)) = cache.as_ref() {
        if *p == path && *s == stamp {
            return Ok((read.values.clone(), read.whole, read.limits.clone()));
        }
    }
    let read = read_store_file(&path)?;
    let out = (read.values.clone(), read.whole, read.limits.clone());
    *cache = Some((path, 0, stamp, read));
    Ok(out)
}
/// What every attachment says while the roots registry's last line is unread.
const REGISTRY_TORN: &str = "the records store's registry of project folders (roots.jsonl) was not read whole: its last line is incomplete and was not read, and its bytes are kept as found. That line may change which folder a project belongs to, so records are only read, from what its complete lines record; nothing is written, minted, adopted or restored for any project until it is resolved";
/// Whether `<store>/roots.jsonl` ends in an incomplete line, which `roots`
/// does not read. Read only, and the bytes are never changed here.
fn roots_torn(store: &Path) -> Result<bool, String> {
    let path = store.join("roots.jsonl");
    // Read as every other line file of the store is: a plain, singly linked
    // file, opened without following a link and without waiting, so that
    // something else at this path is reported and never waited on.
    match std::fs::symlink_metadata(&path) {
        Err(e) if e.kind() == std::io::ErrorKind::NotFound => return Ok(false),
        Err(e) => return Err(format!("records store unreadable: roots.jsonl: {e}")),
        Ok(_) => {}
    }
    let bytes = crate::records_retention::read_plain(&path).map_err(|e| format!("records store unreadable: roots.jsonl: {e}"))?;
    Ok(bytes.last().is_some_and(|last| *last != b'\n'))
}
/// Refuses an act that would append to the roots registry while its last
/// line is incomplete: appending would close that line and change what it
/// reads as. The tail's bytes are kept exactly.
fn require_roots_whole(store: &Path) -> Result<(), String> {
    if roots_torn(store)? { return Err(format!("{REGISTRY_TORN}; nothing changed")); }
    Ok(())
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
        "note":"A link to this project's records in the Chirality App's records store. The store's own record governs; a changed or missing file attaches nothing until you resolve it in the App."})
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
    /// attached to it (its link is missing, unreadable or names another).
    pub recorded: Option<String>,
    /// What stands between the folder and its records, as one word for the
    /// view: "link missing", "link unreadable", "link changed", "several
    /// identities", "moved", "duplicated", "another store", "link names
    /// another store", or (no identity yet, and one the store holds with no
    /// folder recorded) "no folder recorded".
    pub fault: Option<&'static str>,
    /// The identity the project's link file names, when it is not the one
    /// attached.
    pub linked: Option<String>,
    /// The person's acts that resolve the fault, of "restore-link", "adopt"
    /// and "new-identity" (`records_store_identity`). Only these are offered.
    pub resolutions: Vec<&'static str>,
    /// Set when the store's registry of project folders was not read whole
    /// (its last line is incomplete): this attachment rests on its complete
    /// lines only. Shown on every attachment while it stands.
    pub registry: Option<String>,
}
impl Attachment {
    pub fn view(&self) -> Value {
        json!({"root":self.root.display().to_string(),"projectId":self.project,"how":self.how,"limits":self.limits,"refusal":self.refusal,"recordedHere":self.recorded,
            "fault":self.fault,"linkedIdentity":self.linked,"resolutions":self.resolutions,"registry":self.registry})
    }
}

/// Resolves `root` against the store. With `mint`, a project new to the store
/// gets an identity (link written first, then the store's records), and a
/// link whose identity the store does not know yet is registered; without it
/// nothing is written. `Err` only when the store or the root is unavailable.
pub fn attach(root: &Path, mint: bool) -> Result<Attachment, String> {
    let (store, store_id) = if mint { created()? } else { opened()? };
    // The physical project folder only: an alias (symlink) is refused, never
    // resolved into another folder's identity.
    crate::storage::check_path(root)?;
    let canonical = std::fs::canonicalize(root).map_err(|e| format!("project folder unavailable: {}: {e}", root.display()))?;
    if canonical != root {
        return Err(format!("project folder must be named by its physical path: {}", root.display()));
    }
    let _lock = if mint { Some(store_lock(&store)?) } else { None };
    package::require_root(&canonical)?;
    // Reading continues past what the registry could not read; that is shown.
    let (lines, _, registry_limits) = roots_read(&store)?;
    let at = canonical.to_str().ok_or("project folder is not Unicode; no project identity")?.to_owned();
    let listed = listed(&lines, &at);
    let link = read_link(&canonical);
    let torn = roots_torn(&store)?;
    let mut out = Attachment { root: canonical.clone(), project: None, dir: None, limits: registry_limits, refusal: None, how: "attached", recorded: None, fault: None, linked: None, resolutions: vec![],
        registry: torn.then(|| REGISTRY_TORN.to_owned()) };
    // Other folders the store records for `project` whose own link still names it.
    let held_elsewhere = |project: &str| -> Vec<String> {
        roots_of(&lines, project).into_iter().filter(|r| *r != at && matches!(read_link(Path::new(r)), Link::Present { project: ref p, .. } if p == project)).collect()
    };
    let attach_to = |out: &mut Attachment, project: &str| {
        let dir = project_dir(&store, project);
        remember(&dir, root);
        out.project = Some(project.to_owned());
        out.dir = Some(dir);
    };
    if listed.len() > 1 {
        out.refusal = Some(format!("the records store records this folder for several projects ({}); nothing attached until the person resolves it", listed.join(", ")));
        out.how = "unattached";
        out.fault = Some("several identities");
        if let Link::Present { project, .. } = &link {
            out.linked = Some(project.clone());
            if held_elsewhere(project).is_empty() { out.resolutions.push("adopt"); }
        }
        out.resolutions.push("new-identity");
        // No identity act can succeed while the registry's last line is
        // unread, so none is offered on this path either.
        if torn { out.resolutions.clear(); }
        return Ok(out);
    }
    // The incomplete last line may be exactly this folder's registration (or
    // its release): a folder the complete lines do not associate is not
    // known, and nothing is minted, registered or adopted beside it.
    if torn && listed.is_empty() {
        out.refusal = Some(format!("association not known; not attached: {REGISTRY_TORN}, and its complete lines record no project for this folder; nothing is read, written, minted or adopted for it"));
        out.how = "unattached";
        out.fault = Some("association not known");
        if let Link::Present { project, .. } = &link { out.linked = Some(project.clone()); }
        return Ok(out);
    }
    match (&link, listed.first()) {
        (Link::Present { project, store: linked }, Some(y)) if project == y && *linked == store_id => attach_to(&mut out, y),
        // The identity agrees and the link names another store: the link is
        // changed all the same, and a changed link attaches nothing.
        (Link::Present { project, store: linked }, Some(y)) if project == y => {
            out.refusal = Some(format!("link changed; not attached: project file {PROJECT_LINK} names another records store ({linked}), and this store recorded project {y} at this folder; nothing is read or written for it until the person restores the link"));
            out.recorded = Some(y.clone());
            out.linked = Some(project.clone());
            out.how = "unattached";
            out.fault = Some("link names another store");
            out.resolutions.push("restore-link");
        }
        // The link names another identity than the store records here (an
        // edit, or another project's folder put at this path): the store does
        // not choose between them. Nothing is attached until the person does.
        (Link::Present { project, .. }, Some(y)) => {
            let holding = held_elsewhere(project);
            out.refusal = Some(format!("link changed; not attached: project file {PROJECT_LINK} names project {project}, and the records store recorded project {y} at this folder; nothing is read or written for it until the person restores the link, {}gives this folder a new identity",
                if holding.is_empty() { "confirms this folder is the project its file names or " } else { "" }));
            out.recorded = Some(y.clone());
            out.linked = Some(project.clone());
            out.how = "unattached";
            out.fault = Some("link changed");
            out.resolutions.push("restore-link");
            if holding.is_empty() { out.resolutions.push("adopt"); }
            out.resolutions.push("new-identity");
        }
        // No usable link: never attached on its path alone (a new folder can
        // stand where a moved project was). The person restores the link or
        // gives the folder a new identity.
        (Link::Absent, Some(y)) => {
            out.refusal = Some(format!("link missing; not attached: project file {PROJECT_LINK} is missing, and the records store recorded project {y} at this folder; nothing is read or written for it until the person restores the link or gives this folder a new identity"));
            out.recorded = Some(y.clone());
            out.how = "unattached";
            out.fault = Some("link missing");
            out.resolutions.extend(["restore-link", "new-identity"]);
        }
        (Link::Unreadable(e), Some(y)) => {
            out.refusal = Some(format!("link unreadable; not attached: project file {PROJECT_LINK} is unreadable ({e}), and the records store recorded project {y} at this folder; nothing is read or written for it until the person restores the link or gives this folder a new identity"));
            out.recorded = Some(y.clone());
            out.how = "unattached";
            out.fault = Some("link unreadable");
            out.resolutions.extend(["restore-link", "new-identity"]);
        }
        (Link::Unreadable(e), None) => {
            out.refusal = Some(format!("project file {PROJECT_LINK} is unreadable ({e}) and the records store does not know this folder; nothing minted or attached"));
            out.how = "unattached";
            out.fault = Some("link unreadable");
            out.resolutions.push("new-identity");
        }
        (Link::Present { project, store: linked }, None) => {
            let elsewhere = roots_of(&lines, project);
            if !elsewhere.is_empty() {
                let holding: Vec<&String> = elsewhere.iter().filter(|r| matches!(read_link(Path::new(r)), Link::Present { project: ref p, .. } if p == project)).collect();
                out.how = "unattached";
                out.linked = Some(project.clone());
                out.refusal = Some(if holding.is_empty() {
                    out.fault = Some("moved");
                    out.resolutions.extend(["adopt", "new-identity"]);
                    format!("this folder's project identity {project} is recorded at {} and not here; nothing attached until the person confirms this folder is that project (adopt) or gives it a new identity", elsewhere.join(", "))
                } else {
                    out.fault = Some("duplicated");
                    out.resolutions.push("new-identity");
                    format!("duplicated project identity: {project} is also the identity of {}; nothing attached until the person gives this folder a new identity", holding.iter().map(|s| s.as_str()).collect::<Vec<_>>().join(", "))
                });
            } else if *linked != store_id {
                out.how = "unattached";
                out.linked = Some(project.clone());
                out.fault = Some("another store");
                out.resolutions.extend(["adopt", "new-identity"]);
                out.refusal = Some(format!("this project's records were kept in another records store ({linked}); nothing attached here until the person adopts this project into this store"));
            } else {
                // Known history: the store holds this identity's record, or
                // has recorded folders for it that are all released (an
                // adoption stopped after its release lines, or a link copied
                // from a folder that was later given a new identity). Its
                // records are kept and are not this folder's until the person
                // confirms it; never read as a project with no records, and
                // never registered here on the link alone.
                let released = lines.iter().any(|l| l["projectId"] == project.as_str());
                let known = released || identity_held(&project_dir(&store, project))?;
                if mint && !released {
                    // A link the store does not know yet, or an identity whose
                    // minting stopped before its first roots line.
                    register(&store, project, &at, "registered")?;
                    out.limits.push(format!("the records store held no record of project {project}; registered from its project file"));
                    out.how = "registered";
                    attach_to(&mut out, project);
                } else if known {
                    out.refusal = Some(format!("records kept, not attached: the records store holds project {project}, which this folder's project file names, and records no folder for it; nothing is read or written for it until the person confirms this folder is that project"));
                    out.how = "unattached";
                    out.linked = Some(project.clone());
                    out.fault = Some("no folder recorded");
                    out.resolutions.push("adopt");
                } else {
                    out.how = "none";
                }
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
    // While the registry's last line is unread no identity act can succeed
    // (`adopt`, `new_identity` and `restore_link` refuse): none is offered.
    if torn { out.resolutions.clear(); }
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

/// For a handle bound earlier to the store folder `bound`: `root` must be
/// attached now, cleanly, to that same folder. Whatever stands between the
/// folder and its records refuses with the attachment's own text; a check
/// that cannot be made refuses. Nothing is minted, written or re-associated.
pub(crate) fn require_attached(root: &Path, bound: &Path) -> Result<(), String> {
    let now = attach(root, false)?;
    if let Some(refusal) = now.refusal {
        return Err(refusal);
    }
    if let Some(fault) = now.fault {
        return Err(format!("{fault}; not attached: {}", now.limits.join("; ")));
    }
    match now.dir {
        Some(dir) if dir == bound => Ok(()),
        Some(_) => Err(format!("the project's records association changed: {} is now attached to project {}, not to the records this handle was opened for; nothing read or written", now.root.display(), now.project.unwrap_or_default())),
        None => Err(format!("the project's records association changed: the records store no longer attaches {} to the records this handle was opened for; nothing read or written", now.root.display())),
    }
}

/// The store's identity record for `project` (once) and a roots line.
fn register(store: &Path, project: &str, root: &str, how: &str) -> Result<(), String> {
    // Whatever the caller checked: no line is ever appended after an
    // incomplete one, which the append would close and change.
    require_roots_whole(store)?;
    let dir = project_dir(store, project);
    let record = dir.join("project.json");
    if !record.exists() {
        crate::records_retention::check_write(&dir)?;
        // The witness of legacy imports begins before any project is created
        // after it, so such a project is known to have been created after it.
        witness::begin(store)?;
        crate::storage::create_json(&record, &json!({"format":PROJECT_FORMAT,"formatVersion":VERSION,"projectId":project,"createdAt":now_rfc3339(),"how":how}))?;
    }
    append_line(&store.join("roots.jsonl"), &json!({"format":ROOT_FORMAT,"formatVersion":VERSION,"projectId":project,"root":root,"at":now_rfc3339(),"how":how}))
}

/// The project's imports as recorded: each import writes a "started" line
/// with its whole census before it copies anything, and a "completed" line
/// last. Only a completed import's files count as imported.
#[derive(Default)]
struct Imports {
    /// Every attempt named by a readable account line, started or completed.
    ids: std::collections::BTreeSet<String>,
    /// Lines in the file at all.
    any: bool,
    /// How many lines the account holds.
    lines: usize,
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
/// One line of a project's import account: a "started" line (its census), a
/// "completed" line (its files and conflicts), or the single line with no
/// event that the first store builds wrote for a completed import. `None`
/// for anything else.
///
/// **The boundary of what is checked** (decided by App Agent 0). The reader
/// checks every member of a line that it takes, for the form it takes it as,
/// and checks no member of a line that it does not take. Taken: the format,
/// the version, the import identity (a string that is not empty), the event,
/// `storeHeld` (true or false, where present), a started line's `at` (a
/// string, where present; it is shown in one refusal), and the census, files
/// and conflicts lists. Not taken, not checked, and accepted when absent:
/// `root`, `method`, `resumes`, `censusChanged`, and `at` on a completed
/// line. An entry of a census, files or conflicts list is held to its entry
/// form whole (`original`, `copy` and `sha256` strings that are not empty,
/// `bytes` a whole number; a conflict's `original` and its `reason`),
/// although nothing after the reader reads a census entry's `copy` or
/// `bytes` or a file entry's `bytes`. A file entry's `stamp` is compared for
/// equality as it stands and needs no form. And no line carries a member
/// that no form of import line has.
///
/// This establishes that an account whose bytes, as they stand, are not
/// whole lines in a form the reader accepts is never read as whole. It does
/// not establish that a line is one the App wrote: the store's files are
/// unsigned, and a well-formed line added from outside reads as the App's
/// own. Nor does it establish that lines once there are still there: an
/// account cut back at the end of a line reads as the shorter account, so a
/// later interrupted import whose started line is cut away reads as no
/// unfinished import, and an export verifies. Like an added line, that is a
/// change made to an unsigned file from outside the App; the App's own
/// interrupted append leaves a partial line or none and never removes one.
/// Signing does not by itself close it: a signed export of a cut account
/// authenticates the cut, and signed lines still allow a suffix to be
/// removed. Closing it needs trusted, retained evidence of the expected
/// history, covering the started line and checked before export.
fn import_line(line: &Value) -> Option<&'static str> {
    let text = |v: &Value| v.as_str().is_some_and(|s| !s.is_empty());
    let file = |f: &Value| f.is_object() && text(&f["original"]) && text(&f["copy"]) && text(&f["sha256"]) && f["bytes"].as_u64().is_some();
    let conflict = |c: &Value| c.is_object() && text(&c["original"]) && c["reason"].is_string();
    let all = |list: &Value, each: &dyn Fn(&Value) -> bool| list.as_array().is_some_and(|items| items.iter().all(each));
    if !line.is_object() || line["format"] != IMPORT_FORMAT || line["formatVersion"] != VERSION || !text(&line["importId"]) {
        return None;
    }
    let completed = || all(&line["files"], &file) && all(&line["conflicts"], &conflict);
    // `storeHeld` decides where the project's records are read from while an
    // import is unfinished, so a value that is neither true nor false is not
    // read as false: the line is unknown.
    let started = || all(&line["census"], &file)
        && line.get("storeHeld").is_none_or(Value::is_boolean)
        && line.get("at").is_none_or(Value::is_string);
    // No line carries a member that none of the three forms has (the forms
    // of the two writers of this file, and of the one at 0237b6b3).
    let only = |members: &[&str]| line.as_object().is_some_and(|object| object.keys().all(|key| members.contains(&key.as_str())));
    match line.get("event").map(Value::as_str) {
        Some(Some("started")) if started()
            && only(&["format", "formatVersion", "event", "importId", "at", "root", "method", "census", "storeHeld", "resumes"]) => Some("started"),
        Some(Some("completed")) if completed()
            && only(&["format", "formatVersion", "event", "importId", "at", "files", "conflicts", "censusChanged"]) => Some("completed"),
        // Written before imports had a "started" line: one line per completed import.
        None if completed() && only(&["format", "formatVersion", "importId", "at", "root", "method", "files", "conflicts"]) => Some("completed"),
        _ => None,
    }
}
fn imports(dir: &Path) -> Result<Imports, String> {
    // The account is read whole, and nothing is concluded from one that is
    // not: an unclosed last line, a blank line, a line that is not JSON, a
    // value that is not an object, another format, version or event, a line
    // without its import identity, a member the reader takes in another
    // form, or a census, file or conflict entry that is not one, each make
    // it unknown, and unknown is an error. Never "no import", never "nothing
    // completed". (What a line's form does not establish: `import_line`.)
    //
    // Only an account that is not there is "no import". One that exists and
    // yields no import line is unknown too (below). And a line is one JSON
    // object and nothing else: no
    // byte before or after it (no padding, no carriage return, no byte-order
    // mark), valid UTF-8, and no key given twice at any depth, since a
    // repeated key reads as its last value and the App writes none.
    //
    // The store's appender closes a fragment an interrupted append left with
    // the mark and names it (`lines`); such a line and the one naming line
    // that names it are left out, as the store's shared reading leaves them
    // out, and every other line is held to the rule above. The account must
    // be settled for that: a partial last line, or a closed line not yet
    // named, makes it unknown until the appender's recovery has named it.
    let path = dir.join("imports.jsonl");
    let unknown = |why: String| format!("records store unreadable: {}: {why}", path.display());
    let account = match std::fs::symlink_metadata(&path) {
        Err(e) if e.kind() == std::io::ErrorKind::NotFound => None,
        Err(e) => return Err(unknown(e.to_string())),
        Ok(_) => Some(crate::records_retention::read_plain(&path).map_err(unknown)?),
    };
    let mut lines: Vec<(Value, &'static str)> = Vec::new();
    if let Some(bytes) = account.as_ref().filter(|bytes| !bytes.is_empty()) {
        let Some(body) = bytes.strip_suffix(b"\n") else { return Err(unknown("its last line is not closed".into())) };
        let shared = lines::read(bytes, &path);
        let set_aside = shared.set_aside.clone();
        shared.require_settled(bytes, &path).map_err(unknown)?;
        for (index, raw) in body.split(|b| *b == b'\n').enumerate() {
            let number = index + 1;
            // A closed fragment that a naming line set aside, and that naming
            // line (the shared reading has checked both): never read.
            if set_aside.contains(&number) || serde_json::from_slice::<Value>(raw).is_ok_and(|v| v["format"] == lines::UNREAD_FORMAT) {
                continue;
            }
            if raw.first() != Some(&b'{') || raw.last() != Some(&b'}') {
                return Err(unknown(format!("its line {number} is not one JSON object and nothing else")));
            }
            let text = std::str::from_utf8(raw).map_err(|_| unknown(format!("its line {number} is not UTF-8")))?;
            let line = crate::workflow_declaration::parse_unique(text).map_err(|e| unknown(format!("its line {number} is not JSON, or gives a key twice ({e})")))?;
            let Some(event) = import_line(&line) else { return Err(unknown(format!("its line {number} is not an import line in a form this App reads"))) };
            lines.push((line, event));
        }
    }
    // An account that exists and yields no import line (an empty file, or
    // one holding only closed fragments and the lines that name them) cannot
    // be told from an account emptied after an import: it is unknown, always,
    // decided on what was read and not on the bytes (App Agent 0, after
    // review round 4: no evidence beside it, the witness included, is taken
    // to show that nothing was begun). The App leaves no such account of its
    // own: the store's appender makes a new file whole or not at all, and an
    // interrupted later append leaves its fragment after lines that remain.
    if let Some(bytes) = &account {
        if lines.is_empty() {
            return Err(unknown(if bytes.is_empty() {
                "it exists and is empty; whether an import was begun is not known"
            } else {
                "it exists and holds no import line, only closed fragments and the lines that name them; whether an import was begun is not known"
            }.into()));
        }
    }
    let mut out = Imports {
        ids: lines.iter().filter_map(|(line, _)| line["importId"].as_str().map(str::to_owned)).collect(),
        any: !lines.is_empty(), lines: lines.len(), ..Imports::default()
    };
    let done: std::collections::HashSet<&str> = lines.iter().filter(|(_, event)| *event == "completed").filter_map(|(l, _)| l["importId"].as_str()).collect();
    for (line, event) in &lines {
        match *event {
            "started" if !done.contains(line["importId"].as_str().unwrap_or_default()) => out.incomplete = Some(line.clone()),
            "completed" => {
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
///
/// `Err` when that cannot be known (an unreadable import record, package
/// import state or store folder): never "the store holds nothing", which
/// would read the kept originals or an empty history in its place.
fn store_holds(dir: &Path) -> Result<bool, String> {
    let unknown = |e: String| format!("whether the records store holds this project's records is unknown, so nothing is read in its place: {e}");
    // The account is read, and found whole, before anything is concluded:
    // a completed package import does not excuse an account that cannot be read.
    let state = imports(dir).map_err(|e| unknown(format!("the project's import record is unreadable: {e}")))?;
    if package::completed(dir).map_err(unknown)? { return Ok(true); }
    Ok(match state {
        i if i.completed => true,
        i if i.incomplete.as_ref().is_some_and(|s| s["storeHeld"] == true) => true,
        i if i.any => false,
        _ => {
            for name in ["runs", "acts", "workflow", "legacy", "connectors"] {
                match std::fs::symlink_metadata(dir.join(name)) {
                    Ok(_) => return Ok(true),
                    Err(e) if e.kind() == std::io::ErrorKind::NotFound => {}
                    Err(e) => return Err(unknown(format!("{}: {e}", dir.join(name).display()))),
                }
            }
            captures_hold_records(dir).map_err(unknown)?
        }
    })
}

/// Export may acquire capture ownership before any capture was recorded.
/// That exact control file (or an empty folder) establishes no RS home. Any
/// unknown/non-control member or unreadable inventory remains conservative.
fn captures_hold_records(dir: &Path) -> Result<bool, String> {
    use std::os::unix::fs::MetadataExt;
    let folder = dir.join("captures");
    match std::fs::symlink_metadata(&folder) {
        Ok(meta) if meta.is_dir() => {},
        Ok(_) => return Ok(true),
        Err(error) if error.kind() == std::io::ErrorKind::NotFound => return Ok(false),
        Err(error) => return Err(format!("{}: {error}", folder.display())),
    }
    let entries = std::fs::read_dir(&folder).map_err(|e| format!("{}: {e}", folder.display()))?;
    for entry in entries {
        let entry = entry.map_err(|e| format!("{}: {e}", folder.display()))?;
        if entry.file_name() != ".capture.lock" || !std::fs::symlink_metadata(entry.path()).is_ok_and(|m|m.is_file() && m.nlink()==1) {
            return Ok(true);
        }
    }
    Ok(false)
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
    if store_holds(dir).map_err(|e|format!("{e}; nothing exported"))? { return Ok(()); }
    if !state.any && ["fleet","role-supply"].iter().any(|name|std::fs::symlink_metadata(dir.join(name)).is_ok()) && legacy_census(root)?.is_empty() {
        return Ok(());
    }
    Err("project records need import before export".into())
}

/// Where a project's records are read and written now, whether or not the
/// attachment is refused. Product code outside this module cannot obtain one:
/// an ordinary reader takes `readable_home`, the one decision.
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
fn unrefusing_home(root: &Path) -> Result<Home, String> {
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
            let store_mode = match attachment.dir.as_deref() { Some(dir) => store_holds(dir)?, None => false };
            Ok(Home { attachment, store_mode })
        }

        Err(e) => Err(e),
    }
}

/// The unrefusing home, for tests only: they read the attachment and the
/// store's standing directly. No product code outside this module has it.
#[cfg(test)]
pub(crate) fn home(root: &Path) -> Result<Home, String> {
    unrefusing_home(root)
}

/// Where an ordinary reader reads a project's records now. Made only by the
/// one decision (`decide`), so having one means the attachment is not
/// refused. Its methods are where ordinary readers join the project folder
/// with a records location; a limited test (`selected_source_lines_about_
/// where_a_projects_records_are_read_are_held_by_content`) fails when the
/// source lines that name such a location change.
#[derive(Clone, Debug)]
pub(crate) struct ReadHome {
    pub attachment: Attachment,
    /// The store holds this project's records: they are read from the store.
    /// Otherwise the project's §13.7 records (if any) are read in place.
    pub store_mode: bool,
    place: ReadPlace,
}
#[derive(Clone, Debug)]
enum ReadPlace {
    /// The project's folder in the records store.
    Store(PathBuf),
    /// The project folder: the store holds nothing of the project's, and
    /// records an earlier build wrote there (if any) are read in place.
    InPlace(PathBuf),
}
/// The one decision of where a project's records are read from. A refused
/// attachment (a link missing, changed, moved or duplicated; records kept
/// and not attached; an association not known) is an error: the files kept
/// in the project folder are never read in the place of records the store
/// holds and will not attach. A folder that is simply new and unlinked has
/// no refusal and reads in place as before.
fn decide(attachment: Attachment, store_mode: bool) -> Result<ReadHome, String> {
    if let Some(refusal) = &attachment.refusal {
        return Err(format!("project records unavailable: {refusal}; the files kept in the project folder are not read in their place"));
    }
    let place = match (store_mode, attachment.dir.clone()) {
        (true, Some(dir)) => ReadPlace::Store(dir),
        _ => ReadPlace::InPlace(attachment.root.clone()),
    };
    Ok(ReadHome { attachment, store_mode, place })
}
/// The project's records home for an ordinary reader: the one decision, after
/// the unrefusing home's own refusals (an unavailable store, a disposal).
pub(crate) fn readable_home(root: &Path) -> Result<ReadHome, String> {
    let home = unrefusing_home(root)?;
    decide(home.attachment, home.store_mode)
}
impl ReadHome {
    /// The project's store folder, when its records are read from the store.
    pub(crate) fn in_store(&self) -> Option<&Path> {
        match &self.place {
            ReadPlace::Store(dir) => Some(dir),
            ReadPlace::InPlace(_) => None,
        }
    }
    /// The folder the project's run, act and workflow logs are read under.
    pub(crate) fn records(&self) -> PathBuf {
        match &self.place {
            ReadPlace::Store(dir) => dir.clone(),
            ReadPlace::InPlace(root) => root.join(crate::storage::LEGACY_RECORDS),
        }
    }
    /// The project's capture evidence folder.
    pub(crate) fn captures(&self) -> PathBuf {
        match &self.place {
            ReadPlace::Store(dir) => dir.join("captures"),
            ReadPlace::InPlace(root) => root.join(crate::storage::CAPTURES),
        }
    }
    /// The registered legacy log: its imported copy, or the file in place.
    pub(crate) fn registered_log(&self) -> PathBuf {
        match &self.place {
            ReadPlace::Store(dir) => dir.join(REGISTERED_COPY),
            ReadPlace::InPlace(root) => root.join(crate::storage::LEGACY_LOG),
        }
    }
    /// A log named by its path in the project, where it is read now.
    pub(crate) fn named(&self, rel: &str) -> PathBuf {
        match &self.place {
            ReadPlace::Store(_) if rel == crate::storage::LEGACY_LOG => self.registered_log(),
            ReadPlace::Store(dir) => dir.join(crate::storage::home_rel(rel)),
            ReadPlace::InPlace(root) => root.join(rel),
        }
    }
    /// The folder names, below the project folder, of the in-place records
    /// folder `leaf`, for a reader that opens them one by one from a handle
    /// it holds on the project folder. `None` when read from the store.
    pub(crate) fn in_place_parts(&self, leaf: &'static str) -> Option<Vec<&'static str>> {
        match &self.place {
            ReadPlace::Store(_) => None,
            ReadPlace::InPlace(_) => Some(crate::storage::LEGACY_RECORDS.split('/').chain([leaf]).collect()),
        }
    }
    /// What status says is being read. "In place" and "import needed" are
    /// said only here and in `import_needed_note`, of the in-place variant.
    fn reading(&self, kept_in_project: bool) -> &'static str {
        match (&self.place, kept_in_project) {
            (ReadPlace::Store(_), _) => "records store",
            (ReadPlace::InPlace(_), true) => "records in place in the project (import needed)",
            (ReadPlace::InPlace(_), false) => "no records yet",
        }
    }
    fn import_needed(&self, kept_in_project: bool) -> bool {
        matches!(self.place, ReadPlace::InPlace(_)) && kept_in_project
    }
    fn import_needed_note(&self, census: &[LegacyFile]) -> Option<String> {
        if !self.import_needed(!census.is_empty()) {
            return None;
        }
        Some(format!("import needed: {} record file(s) ({}) are read in place; all new recording for the project is refused until they are imported into the records store", census.len(), describe(census)))
    }
    /// The connector route accounts kept in the project folder, read in place
    /// and written nowhere.
    fn accounts_in_place(&self, location: &str) -> Result<AccountsPlace, String> {
        match &self.place {
            ReadPlace::InPlace(root) => Ok(accounts_in_project(root, location.to_owned())),
            ReadPlace::Store(_) => Err("the project's records are in the records store; its connector accounts are not read in the project".into()),
        }
    }
}
/// The in-project connector accounts place. Built only by the one decision
/// (`ReadHome::accounts_in_place`) and by the one named case in
/// `route_accounts_place` where no records store is available at all.
fn accounts_in_project(root: &Path, location: String) -> AccountsPlace {
    AccountsPlace {
        anchor: root.to_path_buf(),
        parts: crate::connector_route_store::LEGACY_DIRECTORY.split('/').map(str::to_owned).collect(),
        store_dir: None,
        location,
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
    require_roots_whole(dir.parent().and_then(Path::parent).ok_or("project store absent")?)?;
    crate::records_retention::check_write(dir)?;
    let current=attach(root,false)?;
    if current.dir.as_deref()!=Some(dir) || current.refusal.is_some(){return Err("project root association changed; stale queued writer refused".into());}
    let state = imports(dir).map_err(|e| format!("the project's import record is unreadable, so whether its history is in the store is unknown; nothing written: {e}"))?;
    if let Some(started) = state.incomplete {
        return Err(format!("import incomplete: the import started at {} did not complete; run the import again before recording (nothing written; no history is split across two homes)", started["at"].as_str().unwrap_or("an unknown time")));
    }
    if !store_holds(dir).map_err(|e| format!("{e}; nothing written"))? {
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
/// Whether the store holds `dir`'s identity record (`project.json`): a
/// regular file there, yes; nothing there, no; anything else, or a record
/// that cannot be examined, is an error, never "not held" (the census's
/// premise: what could not be inspected is not absent).
fn identity_held(dir: &Path) -> Result<bool, String> {
    let record = dir.join("project.json");
    match std::fs::symlink_metadata(&record) {
        Ok(meta) if meta.is_file() => Ok(true),
        Ok(_) => Err(format!("records store unreadable: {} is not a regular file, so whether the store holds this project is not known", record.display())),
        Err(e) if e.kind() == std::io::ErrorKind::NotFound => Ok(false),
        Err(e) => Err(format!("records store unreadable: {}: {e}; whether the store holds this project is not known", record.display())),
    }
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
        // Only a folder that is not there holds nothing. One that cannot be
        // listed, or something else in its place (inside the App's own
        // `.chirality` folder, where earlier builds wrote only folders), is
        // an error: a census that could not inspect the records never says
        // there are none.
        let rd = match std::fs::read_dir(dir) {
            Ok(rd) => rd,
            Err(e) if e.kind() == std::io::ErrorKind::NotFound => return Ok(vec![]),
            Err(e) if e.kind() == std::io::ErrorKind::NotADirectory => return Err(format!("§13.7 records could not all be listed: {} (or a folder above it) is not a folder, so what it holds is not known", dir.display())),
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
    // Present, absent, or not known: a log that cannot be examined (its
    // folder unsearchable, for one) is an error, never absent.
    // One case of "not a folder" is absence and is kept as absence, on
    // purpose: the log's folder is `records` at the project's ROOT, which is
    // the project's own space and not the App's `.chirality` folder. A
    // project may well have an ordinary file named `records` there, and a
    // path beneath a regular file cannot exist (the system answers
    // NotADirectory), so the log is observed to be absent, not left
    // uninspected. Inside `.chirality`, where earlier builds wrote only
    // folders, something other than a folder is an error instead (`list`).
    let registered = root.join(crate::storage::LEGACY_LOG);
    crate::storage::check_path(&registered)?;
    match std::fs::symlink_metadata(&registered) {
        Ok(meta) if meta.is_file() => out.push(LegacyFile { rel: crate::storage::LEGACY_LOG.into(), copy: REGISTERED_COPY.into(), original: registered, refusal: None, stamp: Value::Null }),
        Ok(_) => return Err(format!("§13.7 records could not all be listed: {} is not a regular file, so what it holds is not known", registered.display())),
        Err(e) if e.kind() == std::io::ErrorKind::NotFound || e.kind() == std::io::ErrorKind::NotADirectory => {}
        Err(e) => return Err(format!("§13.7 records could not all be listed: {}: {e}", registered.display())),
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
    // As the census: only a folder that is not there holds nothing.
    let rd = match std::fs::read_dir(&dir) {
        Ok(rd) => rd,
        Err(e) if e.kind() == std::io::ErrorKind::NotFound => return Ok(vec![]),
        Err(e) if e.kind() == std::io::ErrorKind::NotADirectory => return Err(format!("connector route accounts could not all be listed: {} (or a folder above it) is not a folder, so what it holds is not known", dir.display())),
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
/// needed"); a project with none is placed in the store. A folder with no
/// identity yet is read in place and written nowhere. A folder whose
/// attachment is refused has no accounts place at all: an error.
pub(crate) fn route_accounts_place(root: &Path, mint: bool) -> Result<AccountsPlace, String> {
    // The one named case outside the decision, unchanged: with no records
    // store available and no link in the folder, connector accounts are read
    // in place and nothing is written (ordinary records in that state are
    // unavailable); a linked project with the store unavailable is an error.
    let store = match if mint { created() } else { opened() } {
        Ok((store, _)) => store,
        Err(e) if !mint && read_link(root) == Link::Absent && root.is_dir() => {
            return Ok(accounts_in_project(root, format!("the project, read in place; nothing written: records store unavailable: {e}")));
        }
        Err(e) => return Err(e),
    };
    let attachment = attach(root, mint)?;
    // Whether the store holds the project's records can be unknown (an import
    // account that cannot be read): that is an error here as everywhere the
    // account is read through the store, never "does not hold".
    let store_mode = match attachment.dir.as_deref() { Some(dir) => store_holds(dir)?, None => false };
    // The one decision, entered from the attachment: a refused attachment has
    // no accounts place, in the store or in the project.
    let read = decide(attachment, store_mode)?;
    let in_project = !connector_census(&read.attachment.root)?.is_empty();
    let Some(dir) = read.attachment.dir.clone() else {
        return read.accounts_in_place(if in_project {
            "the project, read in place: import needed before accounts are written in the records store"
        } else {
            "the project, read in place: no project identity in the records store yet (a writer opening the accounts mints it)"
        });
    };
    if !read.store_mode && in_project {
        return read.accounts_in_place("the project, read in place: import needed before accounts are written in the records store");
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
    let (store, _) = created()?;
    let attachment = attach(root, true)?;
    let dir = attachment.dir.clone().ok_or_else(|| format!("nothing imported: {}", attachment.refusal.clone().unwrap_or_default()))?;
    let _store = store_lock(&store)?;
    let _admission=crate::records_retention::write_path(&dir)?;
    // Writers wait while the copies are made (the logs' writer lock).
    let _writers = crate::storage::lock(&dir.join(".writer.lock"))?;
    let census = legacy_census(&attachment.root)?;
    let state = imports(&dir)?;
    let project = attachment.project.clone().ok_or("nothing imported: no project identity")?;
    // The witness can have been appended whole before a failed sync prevented
    // even the started account line. Recover that attempt before minting an ID.
    let orphan = witness::unaccounted_import(&store, &project, &state.ids)?;
    if state.any || orphan.is_some() {
        let attempts = orphan.as_ref().map(|w| w.import_id.clone())
            .unwrap_or_else(|| state.ids.iter().cloned().collect::<Vec<_>>().join(", "));
        crate::storage::sync_publication(&store.join(witness::WITNESS_FILE))
            .map_err(|e| format!("import {attempts}: witness durability not established: {e}; nothing imported"))?;
        if state.any {
            // A readable completion is not proof that its own appended bytes
            // synced. This covers completed/no-new-input retries too.
            crate::storage::sync_publication(&dir.join("imports.jsonl"))
                .map_err(|e| format!("import {attempts}: account durability not established: {e}; nothing imported"))?;
        }
    }
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
    if pending.is_empty() && !fresh_conflict && state.incomplete.is_none() && orphan.is_none() {
        // Nothing new: an import repeated after it completed records nothing.
        let drifted: Vec<Value> = read.iter().filter_map(|(file, sha, ..)| {
            let (copy, imported, _) = state.covered.get(&file.rel)?;
            (imported != sha).then(|| json!({"original":file.rel,"copy":copy,"reason":format!("the original differs from its imported copy (sha256 {imported} at import); the records store copy governs and is not replaced")}))
        }).collect();
        conflicts.extend(drifted);
        for (file, sha, ..) in &read {
            if let Some((copy, imported, _)) = state.covered.get(&file.rel) {
                if imported == sha {
                    crate::storage::sync_publication(&dir.join(copy))
                        .map_err(|e| format!("imported copy durability not established: {copy}: {e}"))?;
                }
            }
        }
        return Ok(outcome(&attachment, None, census.len(), 0, read.len(), conflicts, census_changed));
    }
    let named: Vec<Value> = read.iter().map(|(file, sha, bytes, _)| json!({"original":file.rel,"copy":file.copy,"sha256":sha,"bytes":bytes.len()})).collect();
    // An unchanged interrupted census is the same import, including when its
    // copies are readable but their publication could not be synced. Changed
    // input still uses the existing explicit resumption account below.
    let same_import = state.incomplete.as_ref().filter(|started| started["census"] == json!(named));
    let id = match (&orphan, same_import) {
        (Some(witnessed), _) => witnessed.import_id.clone(),
        (None, Some(started)) => started["importId"].as_str().ok_or("incomplete import has no identity")?.to_owned(),
        (None, None) => crate::util::opaque_id("import:")?,
    };
    // Whether the store already held the project's records: a late import,
    // during which (and if it is interrupted) readers keep reading the store.
    let store_held = store_holds(&dir).map_err(|e| format!("{e}; nothing imported"))?;
    // The store's witness of this import, outside the project's subtree,
    // before the account's "started" line and before any copy.
    let witnessed: Vec<witness::WitnessedFile> = pending.iter().map(|(file, sha, bytes, _)| witness::WitnessedFile { copy: file.copy.clone(), length: bytes.len() as u64, sha256: sha.clone() }).collect();
    if let Some(retained) = &orphan {
        if retained.files != witnessed {
            return Err(format!("import {id}: continuation is not known: the pending files differ from the retained witness; no new identity or copy written"));
        }
    }
    if same_import.is_none() || orphan.is_some() {
        if orphan.is_none() {
            witness::record(&store, &project, &id, &witnessed)
                .map_err(|e| format!("import {id}: witness publication not confirmed: {e}; the import did not complete"))?;
        }
        append_line(&dir.join("imports.jsonl"), &json!({"format":IMPORT_FORMAT,"formatVersion":VERSION,"event":"started","importId":id,"at":now_rfc3339(),
            "root":attachment.root.display().to_string(),"method":"sha-256 of the exact bytes","census":named,"storeHeld":store_held,
            "resumes":state.incomplete.as_ref().map(|s| s["importId"].clone())}))?;
    }
    let mut files = Vec::new();
    let (mut copied, mut present) = (0, 0);
    for (file, sha, bytes, meta) in &read {
        // Imported before: the store copy governs (it may have grown since);
        // an original that no longer matches is reported, never imported again.
        if let Some((copy, imported, _)) = state.covered.get(&file.rel) {
            if imported == sha {
                crate::storage::sync_publication(&dir.join(copy))
                    .map_err(|e| format!("import {id}: copy {copy} durability not established: {e}; the import did not complete"))?;
                present += 1;
            } else {
                conflicts.push(json!({"original":file.rel,"copy":copy,"reason":format!("the original differs from its imported copy (sha256 {imported} at import); the records store copy governs and is not replaced")}));
            }
            continue;
        }
        let target = dir.join(&file.copy);
        crate::storage::check_path(&target)?;
        let outcome = match std::fs::read(&target) {
            Ok(existing) if existing == *bytes => "present",
            Ok(existing) => {
                conflicts.push(json!({"original":file.rel,"copy":file.copy,"reason":format!("the store already holds a different file there (sha256 {}); not overwritten", sha256_hex(&existing))}));
                continue;
            }
            Err(e) if e.kind() == std::io::ErrorKind::NotFound => {
                // A late log that would bring a record identity the store's
                // set already holds is not copied: R-1 counts each identity
                // once. Whether the set holds one is known only from a set
                // read whole (`held_identities`).
                if store_held && file.copy.ends_with(".jsonl") {
                    let held = held_identities(&attachment.root, bytes)?;
                    if !held.is_empty() {
                        conflicts.push(json!({"original":file.rel,"copy":file.copy,"heldIdentities":held.iter().take(HELD_SHOWN).collect::<Vec<_>>(),"heldCount":held.len(),
                            "reason":format!("it holds record identities the records store already holds ({}); not copied, so each identity is counted once (R-1)", name_bounded(&held))}));
                        continue;
                    }
                }
                #[cfg(test)]
                if IMPORT_STOP_AFTER.with(|c| c.get()) == Some(copied) {
                    return Err("import interrupted (injected); it did not complete".into());
                }
                crate::storage::create_bytes(&target, bytes)
                    .map_err(|e| format!("import {id}: copy {} publication not confirmed: {e}; the import did not complete", file.copy))?;
                #[allow(unused_mut)]
                let mut back = std::fs::read(&target).map_err(|e| format!("imported copy unreadable: {e}; the import did not complete"))?;
                #[cfg(test)]
                if IMPORT_BAD_READBACK.with(|c| c.get()) {
                    back.push(b'!');
                }
                if sha256_hex(&back) != *sha {
                    return Err(format!("imported copy of {} does not verify; the import stopped and did not complete", file.rel));
                }
                "copied"
            }
            Err(e) => return Err(format!("records store unreadable: {}: {e}; the import did not complete", target.display())),
        };
        // Equality identifies the copy; only fresh file and ancestor syncs
        // establish its durability (also after temporary alias cleanup).
        crate::storage::sync_publication(&target)
            .map_err(|e| format!("import {id}: copy {} durability not established: {e}; the import did not complete", file.copy))?;
        if outcome == "present" { present += 1; } else { copied += 1; }
        files.push(json!({"original":file.rel,"copy":file.copy,"outcome":outcome,"sha256":sha,"bytes":bytes.len(),"stamp":stamp_value(meta)}));
    }
    append_line(&dir.join("imports.jsonl"), &json!({"format":IMPORT_FORMAT,"formatVersion":VERSION,"event":"completed","importId":id,"at":now_rfc3339(),
        "files":files,"conflicts":conflicts,"censusChanged":census_changed}))?;
    Ok(outcome(&attachment, Some(id), census.len(), copied, present, conflicts, census_changed))
}
/// Every record identity in a log's `bytes` that the project's record set
/// (the store, read through the index) already holds, in log order. A set
/// not read whole cannot say that it holds none of them, so the import is
/// refused rather than copying what may be a duplicate.
fn held_identities(root: &Path, bytes: &[u8]) -> Result<Vec<String>, String> {
    let ids: Vec<String> = bytes.split(|b| *b == b'\n').filter_map(|l| serde_json::from_slice::<Value>(l).ok())
        .filter_map(|v| v["recordId"].as_str().map(str::to_owned)).collect();
    let mut held = crate::records_index::with_index(root, |ix| {
        let limits = ix.limits();
        if !limits.is_empty() {
            return Err(format!("the project's record set is not read whole ({limits:?}), so whether it already holds this log's record identities is not known; the import did not complete"));
        }
        Ok(ids.into_iter().filter(|id| ix.holds(id)).collect::<Vec<_>>())
    })?;
    let mut seen = std::collections::HashSet::new();
    held.retain(|id| seen.insert(id.clone()));
    Ok(held)
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
    let (store, store_id) = created()?;
    let canonical = std::fs::canonicalize(root).map_err(|e| e.to_string())?;
    let _lock = store_lock(&store)?;
    require_roots_whole(&store)?;
    package::require_root(&canonical)?;
    let at = canonical.to_str().ok_or("project folder is not Unicode")?.to_owned();
    let lines = roots(&store)?;
    let Link::Present { project, store: linked } = read_link(&canonical) else {
        return Err("the project file names no identity to adopt; nothing adopted".into());
    };
    let here = listed(&lines, &at);
    if here.len() == 1 && here[0] == project {
        return Err("this folder is already attached to the project its file names; nothing adopted".into());
    }
    // Containment (a later design replaces it): refused while anything is
    // admitted to read or write the records of an identity concerned, the
    // adopted one and each this folder is released from, and while anything
    // still holds its activity (a running Codex, an open run, a capture or a
    // record waiting to be written). Held until the association has changed,
    // so nothing pending is written into another identity or follows a path
    // into a new one. The adopted identity's own record is only checked when
    // the store holds it: one adopted from another store has none yet, and
    // registering it publishes under that admission.
    let adopted = project_dir(&store, &project);
    let held = identity_held(&adopted)?;
    let mut _admissions = Vec::new();
    if held {
        _admissions.push(crate::records_retention::quiet_for_reassociation(&adopted, &project)?);
    } else {
        _admissions.push(crate::records_retention::read_path(&adopted)?);
    }
    for other in here.iter().filter(|p| **p != project) { _admissions.push(crate::records_retention::quiet_for_reassociation(&project_dir(&store,other), other)?); }
    let mut _idle = Vec::new();
    for other in here.iter() { _idle.push(crate::records_retention::idle_for_reassociation(&project_dir(&store,other), other)?); }
    if !here.contains(&project) && held {
        _idle.push(crate::records_retention::idle_for_reassociation(&adopted, &project)?);
    }
    if roots_of(&lines, &project).iter().any(|r| *r != at && matches!(read_link(Path::new(r)), Link::Present { project: ref p, .. } if *p == project)) {
        return Err("another folder holds this project identity; give this folder a new identity instead; nothing adopted".into());
    }
    // Every earlier root of this identity is released (append-only lines), so
    // a new folder later made at an old path is not taken for this project.
    for earlier in roots_of(&lines, &project).into_iter().filter(|r| *r != at) {
        append_line(&store.join("roots.jsonl"), &json!({"format":ROOT_FORMAT,"formatVersion":VERSION,"projectId":project,"root":earlier,"at":now_rfc3339(),"how":"released","by":"adopt"}))?;
    }
    // A link that names another identity than the store recorded here (the
    // project's folder was put where another project's stood): this folder is
    // released from that identity, whose records stay in the store under it.
    let released: Vec<String> = here.iter().filter(|p| **p != project).cloned().collect();
    for other in &released {
        append_line(&store.join("roots.jsonl"), &json!({"format":ROOT_FORMAT,"formatVersion":VERSION,"projectId":other,"root":at,"at":now_rfc3339(),"how":"released","by":"adopt"}))?;
    }
    if !here.contains(&project) {
        register(&store, &project, &at, "adopted")?;
    }
    if linked != store_id {

        crate::storage::replace_json(&canonical.join(PROJECT_LINK), &link_value(&project, &store_id))?;
    }
    let mut out = json!({"state":"adopted","projectId":project,"root":at});
    if !released.is_empty() {
        out["releasedHere"] = json!(released);
        out["limit"] = json!("records of the identity this folder had stay in the store under that identity and are no longer attached to this folder");
    }
    Ok(out)
}

/// The person gives this folder a new identity (a copy, or another project
/// whose link was copied in): the folder is released from any identity the
/// store records for it, and a new one is minted and linked.
pub fn new_identity(root: &Path) -> Result<Value, String> {
    let (store, store_id) = created()?;
    let canonical = std::fs::canonicalize(root).map_err(|e| e.to_string())?;
    let _lock = store_lock(&store)?;
    require_roots_whole(&store)?;
    package::require_root(&canonical)?;
    let at = canonical.to_str().ok_or("project folder is not Unicode")?.to_owned();
    let prior = listed(&roots(&store)?, &at);
    // Containment, as `adopt`: refused while anything is admitted to read or
    // write the records of an identity this folder is released from, or still
    // holds its activity.
    let mut _admissions=Vec::new();
    for project in &prior {_admissions.push(crate::records_retention::quiet_for_reassociation(&project_dir(&store,project), project)?);}
    let mut _idle = Vec::new();
    for project in &prior { _idle.push(crate::records_retention::idle_for_reassociation(&project_dir(&store,project), project)?); }
    // The identity the link names, when it is not one already held above
    // (a second admission on a held one would wait on this act itself).
    if let Link::Present{project,..}=read_link(&canonical) { if !prior.contains(&project) {_admissions.push(crate::records_retention::read_path(&project_dir(&store,&project))?);} }
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
    let (store, store_id) = created()?;
    let canonical = std::fs::canonicalize(root).map_err(|e| e.to_string())?;
    let _lock = store_lock(&store)?;
    require_roots_whole(&store)?;
    package::require_root(&canonical)?;
    let at = canonical.to_str().ok_or("project folder is not Unicode")?.to_owned();
    let listed = listed(&roots(&store)?, &at);
    let [project] = listed.as_slice() else {
        return Err("the records store records no single identity for this folder; nothing restored".into());
    };
    // The link is a file in the project folder: restoring it reads no record,
    // so it is possible whatever the state of the project's records (a
    // disposal left unfinished can then be finished). The admission only
    // keeps a disposal from running at the same moment.
    let _admission=crate::records_retention::link_path(&project_dir(&store,project))?;
    crate::storage::ensure_directory(&canonical.join(".chirality"))?;
    crate::storage::replace_json(&canonical.join(PROJECT_LINK), &link_value(project, &store_id))?;
    Ok(json!({"state":"link restored","projectId":project,"root":at}))
}

/// Limits about the project's records that do not make its record set
/// incomplete (the store governs): identity limits, §13.7 records not
/// imported (not read), and imported originals that differ from their copies.
pub(crate) fn notes(root: &Path) -> Vec<String> {
    let home = match unrefusing_home(root) {
        Ok(h) => h,
        Err(e) => return vec![e],
    };
    let mut notes = home.attachment.limits.clone();
    notes.extend(home.attachment.registry.clone());
    if home.attachment.dir.as_deref().is_some_and(|d|crate::records_retention::terminal(d).unwrap_or(false)){notes.push("Records disposed or disposal incomplete; only surviving administration and export evidence remain. Retained project originals are not read or re-imported.".into());}
    // The one decision: of a refused attachment nothing is said to be read
    // in place and no import is asked for; its refusal is the note.
    let read = match decide(home.attachment.clone(), home.store_mode) {
        Ok(read) => read,
        Err(_) => {
            notes.extend(home.attachment.refusal.clone());
            return notes;
        }
    };
    let census = match legacy_census(&read.attachment.root) {
        Ok(c) => c,
        Err(e) => {
            notes.push(e);
            return notes;
        }
    };
    let Some(dir) = read.in_store().map(Path::to_path_buf) else {
        notes.extend(read.import_needed_note(&census));
        return notes;
    };
    let covered = match coverage(&dir) {
        Ok(c) => c,
        Err(e) => {
            notes.push(e);
            return notes;
        }
    };
    let refused = match imports(&dir) {
        Ok(i) => i.refused,
        Err(e) => {
            notes.push(e);
            return notes;
        }
    };
    for file in census {
        match covered.get(&file.rel) {
            None => match refused.get(&file.rel) {
                // Refused by the last completed import (each identity is counted once).
                Some(reason) => notes.push(format!("{} is a §13.7 record not imported into the records store: {reason}; it is not read", file.rel)),
                None => notes.push(format!("{} is a §13.7 record not imported into the records store; it is not read (import to include it)", file.rel)),
            },
            Some((copy, sha, stamp)) => match drifted(&file.original, sha, stamp) {
                Ok(false) => {}
                Ok(true) => notes.push(format!("{} differs from its imported copy {copy} (sha256 {sha} at import); the records store copy governs", file.rel)),
                // S2: an original that cannot be examined or read is not
                // known to differ; it is said to be not known.
                Err(e) => notes.push(format!("{} could not be examined or read ({e}), so whether it differs from its imported copy {copy} is not known; the records store copy governs", file.rel)),
            },
        }
    }
    notes
}
/// Whether an imported original now differs from its copy: `Ok(true)` or
/// `Ok(false)` from what was examined and read; an error when it could not
/// be examined or read, which is never taken for a difference (S2).
fn drifted(path: &Path, sha: &str, stamp: &Value) -> Result<bool, String> {
    let meta = std::fs::metadata(path).map_err(|e| e.to_string())?;
    if stamp_value(&meta) == *stamp {
        return Ok(false);
    }
    let now = crate::records_index::Stamp::of(&meta);
    let mut cache = DRIFT.lock().unwrap_or_else(|p| p.into_inner());
    if let Some((_, _, d)) = cache.iter().find(|(p, s, _)| p == path && *s == now) {
        return Ok(*d);
    }
    let d = sha256_hex(&std::fs::read(path).map_err(|e| e.to_string())?) != sha;
    cache.retain(|(p, _, _)| p != path);
    cache.push((path.to_path_buf(), now, d));
    Ok(d)
}

/// Host status: which store the App writes, and the project's standing in it.
pub fn status(project: Option<&Path>) -> Value {
    let store = current();
    let mut out = match (&store, opened()) {
        (Ok(s), Ok((root, id))) => json!({"state":"available","root":root.display().to_string(),"configured":s.root.display().to_string(),"placement":s.placement.label(),"storeId":id,"limits":s.limits}),
        (Ok(s), Err(e)) => json!({"state":"unavailable","configured":s.root.display().to_string(),"placement":s.placement.label(),"error":e,"recording":"refused; no fallback"}),
        (Err(e), _) => json!({"state":"unavailable","error":e,"recording":"refused; no fallback"}),
    };
    // The registry of project folders not read whole is said at the store
    // level too, whether or not a project is open.
    if let Ok((root, _)) = opened() {
        match roots_torn(&root) {
            Ok(false) => {}
            Ok(true) => out["registry"] = json!(REGISTRY_TORN),
            Err(e) => out["registry"] = json!(e),
        }
    }
    if let Some(root) = project {
        out["packageImport"] = package::status(root);
        // What the project holds is read whole or reported unavailable: an
        // unreadable census or import record is never "no records yet" and
        // never a count of nothing.
        out["project"] = match unrefusing_home(root).and_then(|home| {
            let census = legacy_census(&home.attachment.root)?;
            // What is read comes from the one decision.
            let read = decide(home.attachment.clone(), home.store_mode);
            let imports = match home.attachment.dir.as_ref() { Some(d) => imports(d)?.lines, None => 0 };
            let covered = match home.attachment.dir.as_ref() { Some(d) => coverage(d)?, None => HashMap::new() };
            // §13.7 files no import has copied (all of them before the first).
            let to_import = census.iter().filter(|f| !covered.contains_key(&f.rel)).count();
            Ok(json!({"attachment":home.attachment.view(),
                "retention":home.attachment.dir.as_deref().map(crate::records_retention::view),
                // A refused attachment is said first: files kept in the
                // project folder are not read in the place of records the
                // store holds, and no import is asked for while it stands.
                "reading":if home.attachment.fault == Some("no folder recorded") {"records kept in the records store under the identity this folder's file names, not attached to this folder"}
                    else if home.attachment.fault == Some("association not known") {"nothing from the records store (association not known)"}
                    else {match &read {Err(_) => "nothing from the records store (the project is not attached)", Ok(read) => read.reading(!census.is_empty())}},
                "importNeeded":read.as_ref().is_ok_and(|read| read.import_needed(!census.is_empty())),
                "legacyFiles":census.len(),"notImported":to_import,
                "notImportedKinds":describe(&census.iter().filter(|f| !covered.contains_key(&f.rel)).cloned().collect::<Vec<_>>()),"imports":imports,"importStanding":IMPORT_STANDING,"notes":notes(root)}))
        }) {
            Ok(view) => view,
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
