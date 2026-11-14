//! DEL-01-01: the folder the App gives the Codex it hosts as its working
//! folder when no project is open, and the rules that place a folder against
//! the App data folder by what it is (device and inode), never by the text of
//! its path. Kept apart from desktop setup so that the Codex home plans
//! (`home_resources`) apply the same rule wherever they are built.
//!
//! The order is fixed: the App data folder is established by its own custody
//! rules; then [`establish`] makes the folder set aside (the one step here
//! that creates anything); only then is any folder placed against them
//! ([`Established`]); only then is anything carried or created. Nothing is
//! placed against an App data folder that does not exist.
//!
//! Every lookup here has two outcomes besides success, kept apart: an
//! established absence (the lookup said "not found") and a failure to examine
//! (any other error). Neither is ever taken as "outside" or as the folder set
//! aside, and nothing falls back to comparing text after a failure.
use crate::storage;
use std::os::unix::fs::{DirBuilderExt, MetadataExt};
use std::path::{Path, PathBuf};

/// DEL-01-01: the folder the App gives the Codex it hosts as its working
/// folder when no project is open. Under Codex's workspace-write sandbox the
/// working folder is an agent's writable root, so it is a folder of its own,
/// set aside for this, and not the App data folder itself. The App's own fixed
/// locations (the records store, the account homes, the saved setup request,
/// the recovery ledger) are other children of the App data folder; a location
/// the App is given for them is checked against this folder by identity when
/// it is admitted (the checks below). A file that is already another name for
/// a file inside this folder, and a location replaced after its check, are
/// outside what those checks guarantee. This only calculates the path;
/// [`establish`] creates it.
pub fn no_project_folder(app_data: &Path) -> PathBuf {
    app_data.join("conversations-without-project")
}

pub type Identity = (u64, u64);
fn identity(meta: &std::fs::Metadata) -> Identity {
    (meta.dev(), meta.ino())
}

#[cfg(test)]
thread_local! {
    /// Test seam: a lookup of exactly this path fails as "permission denied".
    static FAIL_LOOKUP: std::cell::RefCell<Option<PathBuf>> = const { std::cell::RefCell::new(None) };
}
/// Makes every lookup of `path` on this thread fail (as permission denied)
/// until called again; tests only.
#[cfg(test)]
pub fn fail_lookup_for_test(path: Option<PathBuf>) {
    FAIL_LOOKUP.with(|f| *f.borrow_mut() = path);
}
fn seam(path: &Path) -> std::io::Result<()> {
    #[cfg(test)]
    if FAIL_LOOKUP.with(|f| f.borrow().as_deref() == Some(path)) {
        return Err(std::io::Error::from(std::io::ErrorKind::PermissionDenied));
    }
    let _ = path;
    Ok(())
}
fn lstat(path: &Path) -> std::io::Result<std::fs::Metadata> {
    seam(path)?;
    std::fs::symlink_metadata(path)
}
fn stat(path: &Path) -> std::io::Result<std::fs::Metadata> {
    seam(path)?;
    std::fs::metadata(path)
}
fn canonical(path: &Path) -> std::io::Result<PathBuf> {
    seam(path)?;
    std::fs::canonicalize(path)
}
/// The identities of `path` (which must exist) and each of its ancestors.
/// Any failed lookup fails the whole chain: an ancestor that cannot be
/// examined is never silently left out.
fn identity_chain(path: &Path) -> Result<Vec<Identity>, String> {
    path.ancestors()
        .map(|at| stat(at).map(|meta| identity(&meta)).map_err(|e| format!("{} could not be examined: {e}", at.display())))
        .collect()
}

/// What stands where the folder set aside should be, as the person is told.
#[derive(Clone, Debug, PartialEq, Eq)]
pub enum Occupant {
    File,
    Link(PathBuf),
    SharedFolder,
    OtherOwner,
    NotAFolder,
}
/// Why the App data folder and the folder set aside are not established.
#[derive(Clone, Debug, PartialEq, Eq)]
pub enum Blocked {
    /// The App data folder does not exist (an established absence).
    AppDataAbsent(PathBuf),
    /// The App data folder exists and the folder set aside does not.
    LeafAbsent(PathBuf),
    /// Something other than a private folder of this user is in its place.
    Occupied(PathBuf, Occupant),
    /// A lookup failed: nothing can be established.
    CannotExamine(String),
}
impl Blocked {
    /// What the person is told, in plain words with the path.
    pub fn sentence(&self) -> String {
        match self {
            Blocked::Occupied(path, what) => {
                let what = match what {
                    Occupant::File => "a file".to_string(),
                    Occupant::Link(target) => format!("a link to {}", target.display()),
                    Occupant::SharedFolder => "a folder that other accounts can use".to_string(),
                    Occupant::OtherOwner => "a folder that belongs to another account".to_string(),
                    Occupant::NotAFolder => "something that is not a folder".to_string(),
                };
                format!("Chirality keeps a folder for conversations without a project at {}. Something else is there now: {what}. Move it aside (do not delete what a link points to) and start Chirality again.", path.display())
            }
            Blocked::LeafAbsent(path) => format!("Chirality keeps a folder for conversations without a project at {}, and it is not there now. Start Chirality again to make it.", path.display()),
            Blocked::AppDataAbsent(path) => format!("Chirality's data folder ({}) does not exist yet, so where other folders lie relative to it cannot be decided.", path.display()),
            Blocked::CannotExamine(why) => format!("Chirality could not examine its data folder or the folder it keeps for conversations without a project, so nothing was decided: {why}."),
        }
    }
}
/// The App data folder and the folder set aside, both established, with the
/// identities everything else is placed against.
#[derive(Clone, Debug)]
pub struct Established {
    data: PathBuf,
    data_id: Identity,
    leaf: PathBuf,
    leaf_id: Identity,
    leaf_chain: Vec<Identity>,
}
impl Established {
    pub fn data(&self) -> &Path {
        &self.data
    }
    /// The folder set aside, at its literal place in the canonical App data folder.
    pub fn leaf(&self) -> &Path {
        &self.leaf
    }
    pub fn leaf_identity(&self) -> Identity {
        self.leaf_id
    }
}
/// Reads, creating nothing: the App data folder must exist and the folder
/// set aside must be a real private folder of this user at its literal
/// place, checked without following a link.
pub fn established(app_data: &Path) -> Result<Established, Blocked> {
    let data = match canonical(app_data) {
        Ok(data) => data,
        Err(e) if e.kind() == std::io::ErrorKind::NotFound => return Err(Blocked::AppDataAbsent(app_data.to_path_buf())),
        Err(e) => return Err(Blocked::CannotExamine(format!("{} could not be examined: {e}", app_data.display()))),
    };
    let data_id = stat(&data).map(|m| identity(&m)).map_err(|e| Blocked::CannotExamine(format!("{} could not be examined: {e}", data.display())))?;
    let leaf = no_project_folder(&data);
    let meta = match lstat(&leaf) {
        Ok(meta) => meta,
        Err(e) if e.kind() == std::io::ErrorKind::NotFound => return Err(Blocked::LeafAbsent(leaf)),
        Err(e) => return Err(Blocked::CannotExamine(format!("{} could not be examined: {e}", leaf.display()))),
    };
    let kind = meta.file_type();
    let occupant = if kind.is_symlink() {
        // The target is only shown to the person; an unreadable one shows empty and the folder
        // is refused as occupied either way.
        Some(Occupant::Link(std::fs::read_link(&leaf).unwrap_or_default()))
    } else if kind.is_file() {
        Some(Occupant::File)
    } else if !kind.is_dir() {
        Some(Occupant::NotAFolder)
    } else if meta.uid() != unsafe { libc::geteuid() } {
        Some(Occupant::OtherOwner)
    } else if meta.mode() & 0o077 != 0 {
        Some(Occupant::SharedFolder)
    } else {
        None
    };
    if let Some(occupant) = occupant {
        return Err(Blocked::Occupied(leaf, occupant));
    }
    let leaf_chain = identity_chain(&leaf).map_err(Blocked::CannotExamine)?;
    Ok(Established { data, data_id, leaf_id: identity(&meta), leaf, leaf_chain })
}
/// The start's step that makes the folder set aside: the App data folder
/// must already exist (its creation belongs to its own custody rules); the
/// folder is made (0700, empty) only where it is established to be absent.
/// Never removes or replaces what is there.
pub fn establish(app_data: &Path) -> Result<Established, Blocked> {
    match established(app_data) {
        Err(Blocked::LeafAbsent(leaf)) => {
            storage::check_path(&leaf).map_err(Blocked::CannotExamine)?;
            match std::fs::DirBuilder::new().mode(0o700).create(&leaf) {
                // The leaf always has a parent (the App data folder); the fallback only names a path to sync.
                Ok(()) => storage::sync_dir(leaf.parent().unwrap_or(&leaf)).map_err(Blocked::CannotExamine)?,
                // Made by another start in between: examined below like any other.
                Err(e) if e.kind() == std::io::ErrorKind::AlreadyExists => {}
                Err(e) => return Err(Blocked::CannotExamine(format!("{} could not be made: {e}", leaf.display()))),
            }
            established(app_data)
        }
        other => other,
    }
}

/// Where a working folder lies against the App data folder, decided by what
/// each folder is (its device and inode, and those of its ancestors).
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum WorkingFolder {
    /// Not the App data folder and not in it. A folder that contains it (a
    /// project such as the home folder) is here too, as before this change;
    /// so is a missing folder whose existing part is established outside it.
    Outside,
    /// The folder set aside, or a folder in it.
    NoProject,
    /// The App data folder, or a folder in it other than the folder set
    /// aside (a missing folder whose existing part is in it included).
    AppData,
    /// Its place cannot be established: a lookup failed, a link in its
    /// existing part cannot be resolved, it is relative, or a `..` follows a
    /// missing part.
    CannotEstablish,
}
/// The canonical form of the longest existing part of `path`, and the
/// missing rest (an established absence). `Err` when any lookup fails for a
/// reason other than "not found", or a link in the existing part cannot be
/// resolved.
fn existing_part(path: &Path) -> Result<(PathBuf, Vec<std::ffi::OsString>), ()> {
    if !path.is_absolute() {
        return Err(());
    }
    let mut at = PathBuf::new();
    let mut components = path.components();
    let mut missing = Vec::new();
    for component in components.by_ref() {
        let next = at.join(component.as_os_str());
        match lstat(&next) {
            Ok(meta) => {
                // A link whose target cannot be resolved (absent included) establishes nothing.
                // Any failure to resolve the link (absent target or a failed lookup) is `Err`.
                if meta.file_type().is_symlink() && canonical(&next).is_err() {
                    return Err(());
                }
                at = next;
            }
            Err(e) if e.kind() == std::io::ErrorKind::NotFound => {
                missing.push(component.as_os_str().to_owned());
                break;
            }
            Err(_) => return Err(()),
        }
    }
    missing.extend(components.map(|c| c.as_os_str().to_owned()));
    if missing.iter().any(|name| name == ".." || name == ".") {
        return Err(());
    }
    Ok((canonical(&at).map_err(|_| ())?, missing))
}
impl Established {
    pub fn place(&self, folder: &Path) -> WorkingFolder {
        // Each failure is "cannot be established", never a default place.
        let Ok((existing, missing)) = existing_part(folder) else { return WorkingFolder::CannotEstablish };
        let Ok(chain) = identity_chain(&existing) else { return WorkingFolder::CannotEstablish };
        if chain.contains(&self.data_id) {
            if missing.is_empty() && chain.contains(&self.leaf_id) { WorkingFolder::NoProject } else { WorkingFolder::AppData }
        } else {
            WorkingFolder::Outside
        }
    }
    /// Whether `candidate` (a records store, a Codex home) may be at, in or
    /// contain the folder set aside. `Err` when that cannot be established.
    /// A missing part beyond an existing ancestor cannot be another spelling
    /// of the folder set aside, which exists: the existing ancestor decides.
    pub fn overlaps_leaf(&self, candidate: &Path) -> Result<bool, ()> {
        overlaps(candidate, self.leaf_id, &self.leaf_chain)
    }
    /// The plain reason a working folder is refused, or `None` when it may
    /// be given to Codex. `subject` begins the sentence.
    pub fn refusal(&self, folder: &Path, subject: &str) -> Option<String> {
        match self.place(folder) {
            WorkingFolder::Outside | WorkingFolder::NoProject => None,
            WorkingFolder::AppData => Some(format!("{subject}: its working folder {} is in Chirality's own data folder ({}), where a conversation could change Chirality's records and settings.", folder.display(), self.data.display())),
            WorkingFolder::CannotEstablish => Some(format!("{subject}: Chirality could not establish where the folder {} is, so it might be in Chirality's own data folder.", folder.display())),
        }
    }
    /// A project admitted against the established App data folder: the only
    /// way start-up carries a project forward.
    pub fn admit_project(&self, project: &Path) -> Result<AdmittedProject, String> {
        match self.place(project) {
            WorkingFolder::Outside => Ok(AdmittedProject(project.to_path_buf())),
            _ => Err(format!("the project folder {} is in Chirality's own data folder ({}), or its place cannot be established; choose a project folder outside it", project.display(), self.data.display())),
        }
    }
}
fn overlaps(candidate: &Path, reserved_id: Identity, reserved_chain: &[Identity]) -> Result<bool, ()> {
    let (existing, missing) = existing_part(candidate)?;
    let chain = identity_chain(&existing).map_err(|_| ())?;
    Ok(chain.contains(&reserved_id) || (missing.is_empty() && reserved_chain.contains(&chain[0])))
}
/// Whether `candidate` may be at, in or contain `reserved` (which must
/// exist), by identity. `Err` when that cannot be established.
pub fn may_overlap(candidate: &Path, reserved: &Path) -> Result<bool, ()> {
    let reserved = canonical(reserved).map_err(|_| ())?;
    let chain = identity_chain(&reserved).map_err(|_| ())?;
    overlaps(candidate, chain[0], &chain)
}
/// While the folder set aside is not established: whether `candidate` may be
/// at, in or contain the App data folder, by identity. With the App data
/// folder established to be absent, its nearest existing ancestor A decides:
/// a candidate whose existing part runs below A through an existing child is
/// not in it (that child is not the App data folder's missing name, which
/// would then exist under any spelling the file system accepts); a candidate
/// whose existing part is A itself, or contains A, may be. No names are
/// compared. `Err` when that cannot be established.
pub fn may_be_in_app_data(app_data: &Path, candidate: &Path) -> Result<bool, ()> {
    match canonical(app_data) {
        Ok(data) => may_overlap(candidate, &data),
        Err(e) if e.kind() == std::io::ErrorKind::NotFound => {
            let mut nearest = app_data;
            let nearest = loop {
                nearest = nearest.parent().ok_or(())?;
                match lstat(nearest) {
                    Ok(_) => break canonical(nearest).map_err(|_| ())?,
                    Err(e) if e.kind() == std::io::ErrorKind::NotFound => continue,
                    Err(_) => return Err(()),
                }
            };
            let nearest_chain = identity_chain(&nearest).map_err(|_| ())?;
            let (existing, _) = existing_part(candidate)?;
            let own = identity_chain(&existing).map_err(|_| ())?[0];
            Ok(nearest_chain.contains(&own))
        }
        Err(_) => Err(()),
    }
}
/// DEL-01-01: the temporary root the App is given (`TMPDIR`) is checked by identity before the
/// App allocates anything in it: a root that is an App data folder this process holds, or a
/// folder inside one (the folder set aside included), refuses with a plain reason naming it, and
/// so does a root whose place cannot be established. Returns the canonical root to allocate in.
/// The check is made when this is called; the caller's allocation resolves the path again, so a
/// root replaced between the two is outside what it guarantees.
pub fn check_temporary_root(root: &Path, held: &[Identity], what: &str) -> Result<PathBuf, String> {
    let refused = |why: String| format!("{what} was not made: {why}. Set TMPDIR to a folder outside Chirality's data folder.");
    let canonical_root = canonical(root).map_err(|e| refused(format!("the temporary folder {} could not be examined ({e})", root.display())))?;
    let chain = identity_chain(&canonical_root).map_err(refused)?;
    if held.iter().any(|data| chain.contains(data)) {
        return Err(refused(format!("the temporary folder {} is inside Chirality's own data folder (its folder for conversations without a project included)", root.display())));
    }
    Ok(canonical_root)
}
/// A project folder that has passed admission ([`Established::admit_project`]).
#[derive(Clone, Debug, PartialEq, Eq)]
pub struct AdmittedProject(PathBuf);
impl AdmittedProject {
    pub fn into_path(self) -> PathBuf {
        self.0
    }
}
impl std::ops::Deref for AdmittedProject {
    type Target = Path;
    fn deref(&self) -> &Path {
        &self.0
    }
}

/// DEL-01-01: a Codex home at, in or containing the folder set aside is
/// refused when it is checked. While nothing is to be created (`creating` false: a plan or an
/// inspection) and the App data folder or the folder set aside is
/// established to be absent, nothing is decided and nothing exists to
/// decide against: the plan is checked again before it creates anything,
/// and then both must be established. Something else in its place, or a
/// failure to examine, refuses at once.
pub fn refuse_in_no_project_folder(app_data: &Path, path: &Path, what: &str, creating: bool) -> Result<(), String> {
    match established(app_data) {
        Ok(e) => match e.overlaps_leaf(path) {
            Ok(false) => Ok(()),
            Ok(true) => Err(format!("{what} ({}) may not be in, or contain, the folder Chirality sets aside for conversations without a project ({})", path.display(), e.leaf.display())),
            Err(()) => Err(format!("{what} ({}): its place relative to the folder Chirality sets aside for conversations without a project ({}) could not be established", path.display(), e.leaf.display())),
        },
        Err(Blocked::AppDataAbsent(_) | Blocked::LeafAbsent(_)) if !creating => Ok(()),
        Err(blocked) => Err(blocked.sentence()),
    }
}
/// DEL-01-01: a source of a Codex home's settings in, or over, the folder set
/// aside is refused when it is checked. A source may be absent, or behind a link whose target is
/// absent: that stays a visible source limit, as before. Such a source is
/// placed where its links lead, by their target text, and refused when that
/// place is in, or over, the folder set aside or cannot be followed.
pub fn refuse_source_in_no_project_folder(app_data: &Path, path: &Path, what: &str, creating: bool) -> Result<(), String> {
    match located(path, 0) {
        Some(at) => refuse_in_no_project_folder(app_data, &at, what, creating),
        None => Err(format!("{what} ({}): where it leads could not be followed, so whether it is in the folder Chirality sets aside for conversations without a project cannot be established", path.display())),
    }
}
/// Where `path` leads when every link in it is followed by its target text,
/// absent targets included: the canonical existing part and the missing rest.
/// `None` for a link cycle, a part that cannot be examined, or a `..` after a
/// missing part.
fn located(path: &Path, depth: usize) -> Option<PathBuf> {
    if depth > 40 || !path.is_absolute() {
        return None;
    }
    let mut at = PathBuf::new();
    let mut components = path.components();
    while let Some(component) = components.next() {
        let next = at.join(component.as_os_str());
        match lstat(&next) {
            Ok(meta) if meta.file_type().is_symlink() => {
                // Every failure here is `None`, which its caller refuses.
                let target = std::fs::read_link(&next).ok()?;
                let target = if target.is_absolute() { target } else { at.join(target) };
                let rest: PathBuf = components.map(|c| c.as_os_str()).collect();
                return located(&target.join(rest), depth + 1);
            }
            Ok(_) => at = next,
            Err(e) if e.kind() == std::io::ErrorKind::NotFound => {
                let rest: Vec<_> = std::iter::once(component.as_os_str()).chain(components.map(|c| c.as_os_str())).collect();
                if rest.iter().any(|name| *name == ".." || *name == ".") {
                    return None;
                }
                let mut out = canonical(&at).ok()?;
                out.extend(rest);
                return Some(out);
            }
            Err(_) => return None,
        }
    }
    canonical(&at).ok()
}
/// A private directory of this user (0700), created with its missing
/// ancestors when absent; a link, a file or a directory that is not private
/// refuses.
pub fn protected_directory(path: &Path) -> Result<(), String> {
    #[cfg(test)]
    crate::records_effect_guard::mutation_for_test("desktop_startup::protected_directory");
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
