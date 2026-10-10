//! Immutable workflow package snapshots and source-qualified selection (WR/WD).
//! Registration consumes verified A15 evidence from the act owner; files alone are not an act.
use crate::util::sha256_hex;
use crate::workflow_declaration::{self, Declaration};
use serde::{Deserialize, Serialize};
use std::{collections::BTreeMap, fs, path::Path};

/// Build-owned development package admission; separate from native A15.
#[path = "workflow_catalog.rs"]
pub mod development_catalog;
/// Release-candidate catalog; development admission remains separate.
pub mod production_catalog {
    pub use super::development_catalog::{
        ProductionBundlePackage, ProductionCatalog, ProductionHoldingCopy, PRODUCTION_STANDING,
        RELEASE_SUBJECT,
    };
}

/// Owner-held native A15 review and immutable library transaction.
#[path = "workflow_library.rs"]
pub(crate) mod registration;

/// Content-addressed package copies: TX-7 supply copies and TT-8 trial snapshots.
#[path = "workflow_package_copy.rs"]
pub(crate) mod package_copy;

/// Read only a regular file through the opened descriptor. Nonblocking/no-follow
/// open prevents a substituted FIFO or final-component link from hanging or
/// redirecting candidate manifest/registry checks before descriptor validation.
fn read_regular_file(path: &Path) -> std::io::Result<Vec<u8>> {
    use std::io::Read;
    #[cfg(not(unix))]
    {
        let _ = path;
        return Err(std::io::Error::new(
            std::io::ErrorKind::Unsupported,
            "regular no-follow workflow read unavailable on this platform",
        ));
    }
    #[cfg(unix)]
    {
        use std::os::unix::fs::OpenOptionsExt;
        // Avoid opening known special files at all; the descriptor check below
        // still governs if the final component changes after this preflight.
        if !fs::symlink_metadata(path)?.file_type().is_file() {
            return Err(std::io::Error::new(
                std::io::ErrorKind::InvalidData,
                "workflow input is not a regular file",
            ));
        }
        let mut file = fs::OpenOptions::new()
            .read(true)
            .custom_flags(libc::O_NOFOLLOW | libc::O_NONBLOCK)
            .open(path)?;
        if !file.metadata()?.file_type().is_file() {
            return Err(std::io::Error::new(
                std::io::ErrorKind::InvalidData,
                "workflow input is not a regular file",
            ));
        }
        let mut bytes = Vec::new();
        file.read_to_end(&mut bytes)?;
        Ok(bytes)
    }
}

/// Reviewed CC-CONTENT-IDENTITY App-only package method; no host/global adoption.
pub const SNAPSHOT_METHOD: &str = "chirality.app.workflow-package.sha256/v1";
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
#[serde(deny_unknown_fields)]
pub struct WorkflowIdentity {
    pub kind: String,
    pub origin: String,
    pub source_root: String,
    pub name: String,
    pub revision: String,
    pub revision_method: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub derived_from: Option<Box<WorkflowIdentity>>,
}
impl WorkflowIdentity {
    pub fn validate(&self) -> Result<(), String> {
        if self.kind != "workflow"
            || !["project", "user", "bundled", "host"].contains(&self.origin.as_str())
            || self.source_root.is_empty()
            || self.source_root.contains(['\n', '\r'])
            || !valid_name(&self.name)
            || self.revision.is_empty()
            || self.revision_method.is_empty()
        {
            return Err("workflow content identity not established".into());
        }
        if let Some(d) = &self.derived_from {
            d.validate()?
        }
        Ok(())
    }
    pub fn same_slot(&self, other: &Self) -> bool {
        self.origin == other.origin
            && self.source_root == other.source_root
            && self.name == other.name
    }
}
pub fn valid_name(n: &str) -> bool {
    !n.is_empty()
        && n.len() <= 64
        && n.split('-').all(|s| {
            !s.is_empty()
                && s.bytes()
                    .all(|b| b.is_ascii_lowercase() || b.is_ascii_digit())
        })
}
#[derive(Debug, Clone)]
pub struct Snapshot {
    files: BTreeMap<String, Vec<u8>>,
    revision: String,
}
/// WR §4.5 HY-5 as resolved under U-WR-7: at most 1 000 regular files and
/// 16 MiB of regular-file bytes per package.
pub const PACKAGE_MAX_FILES: usize = 1000;
pub const PACKAGE_MAX_BYTES: u64 = 16 * 1024 * 1024;
impl Snapshot {
    pub fn capture(root: &Path) -> Result<Self, String> {
        if fs::symlink_metadata(root)
            .map_err(|e| e.to_string())?
            .file_type()
            .is_symlink()
        {
            return Err("non-regular package root".into());
        }
        let mut files = BTreeMap::new();
        #[cfg(unix)]
        {
            use std::os::unix::fs::OpenOptionsExt;
            // The opened root descriptor, not the path, is the authority below.
            let dir = fs::OpenOptions::new()
                .read(true)
                .custom_flags(libc::O_DIRECTORY | libc::O_NOFOLLOW | libc::O_CLOEXEC)
                .open(root)
                .map_err(|e| format!("non-regular package root: {e}"))?;
            let mut budget = (0usize, 0u64);
            walk_fd(&dir, root, "", &mut files, &mut budget)?;
        }
        #[cfg(not(unix))]
        walk(root, root, &mut files)?;
        Self::from_files(files)
    }
    pub fn from_files(files: BTreeMap<String, Vec<u8>>) -> Result<Self, String> {
        for path in files.keys() {
            let p = Path::new(path);
            if p.is_absolute()
                || p.components()
                    .any(|c| !matches!(c, std::path::Component::Normal(_)))
                || path.is_empty()
            {
                return Err(format!("package relative path not established: {path}"));
            }
        }
        let wf = files.get("WORKFLOW.md").ok_or("HY-1: no WORKFLOW.md")?;
        std::str::from_utf8(wf).map_err(|_| "HY-7: WORKFLOW.md is not UTF-8")?;
        let mut preimage = Vec::new();
        preimage.extend_from_slice(SNAPSHOT_METHOD.as_bytes());
        preimage.push(0);
        preimage.extend_from_slice(&(files.len() as u64).to_be_bytes());
        for (path, bytes) in &files {
            preimage.extend_from_slice(&(path.len() as u64).to_be_bytes());
            preimage.extend_from_slice(path.as_bytes());
            preimage.extend_from_slice(&(bytes.len() as u64).to_be_bytes());
            preimage.extend_from_slice(bytes);
        }
        Ok(Self {
            files,
            revision: sha256_hex(&preimage),
        })
    }
    pub fn manifest(&self) -> Vec<serde_json::Value> {
        self.files.iter().map(|(path,bytes)|serde_json::json!({"path":path,"bytes":bytes.len(),"content":{"method":crate::role_supply::CONTENT_METHOD,"value":sha256_hex(bytes)}})).collect()
    }
    pub fn hygiene_findings(&self) -> Vec<String> {
        let mut findings = if self.files.len() > PACKAGE_MAX_FILES
            || self.files.values().map(Vec::len).sum::<usize>() as u64 > PACKAGE_MAX_BYTES
        {
            vec![HY5_EXCEEDED.into()]
        } else {
            vec![]
        };
        findings.extend(
            self.files
                .keys()
                .filter(|path| {
                    Path::new(path).components().any(|c| {
                        let s = c.as_os_str().to_string_lossy();
                        [
                            ".DS_Store",
                            "Thumbs.db",
                            "desktop.ini",
                            "Icon\r",
                            ".localized",
                            ".Spotlight-V100",
                            ".Trashes",
                            ".fseventsd",
                            "__MACOSX",
                        ]
                        .contains(&s.as_ref())
                            || s.starts_with("._")
                    })
                })
                .map(|path| format!("HY-4: operating-system entry {path}"))
                .collect::<Vec<String>>(),
        );
        findings
    }

    pub fn revision(&self) -> &str {
        &self.revision
    }
    pub fn files(&self) -> &BTreeMap<String, Vec<u8>> {
        &self.files
    }
    pub fn workflow_text(&self) -> &str {
        std::str::from_utf8(&self.files["WORKFLOW.md"]).expect("validated UTF-8")
    }
    pub fn declaration(&self) -> Result<Declaration, String> {
        workflow_declaration::read(self.workflow_text())
    }
    pub fn identity(
        &self,
        origin: &str,
        source_root: &str,
        name: &str,
        derived_from: Option<WorkflowIdentity>,
    ) -> Result<WorkflowIdentity, String> {
        let id = WorkflowIdentity {
            kind: "workflow".into(),
            origin: origin.into(),
            source_root: source_root.into(),
            name: name.into(),
            revision: self.revision.clone(),
            revision_method: SNAPSHOT_METHOD.into(),
            derived_from: derived_from.map(Box::new),
        };
        id.validate()?;
        Ok(id)
    }
    pub fn publish_new(&self, destination: &Path) -> Result<(), String> {
        // Exclusive new directory; callers own library lock, ledger, fsync and interruption recovery.
        fs::create_dir(destination).map_err(|e| e.to_string())?;
        for (p, b) in &self.files {
            let target = destination.join(p);
            if let Some(parent) = target.parent() {
                fs::create_dir_all(parent).map_err(|e| e.to_string())?;
            }
            let mut f = fs::OpenOptions::new()
                .write(true)
                .create_new(true)
                .open(target)
                .map_err(|e| e.to_string())?;
            use std::io::Write;
            f.write_all(b).map_err(|e| e.to_string())?;
            f.sync_all().map_err(|e| e.to_string())?;
        }
        Ok(())
    }
}
const HY5_EXCEEDED: &str = "HY-5: package exceeds review bound (1000 files / 16 MiB)";
#[cfg(unix)]
fn same_inode(a: &fs::Metadata, b: &fs::Metadata) -> bool {
    use std::os::unix::fs::MetadataExt;
    a.dev() == b.dev() && a.ino() == b.ino()
}
/// `openat` relative to an opened directory: the descriptor, not a path that
/// may have been swapped since, decides which entry is opened.
#[cfg(unix)]
fn open_at(dir: &fs::File, name: &std::ffi::OsStr, flags: i32) -> std::io::Result<fs::File> {
    use std::os::fd::{AsRawFd, FromRawFd};
    use std::os::unix::ffi::OsStrExt;
    let name = std::ffi::CString::new(name.as_bytes())
        .map_err(|_| std::io::Error::new(std::io::ErrorKind::InvalidInput, "NUL in entry name"))?;
    // SAFETY: `dir` is an open descriptor and `name` a NUL-terminated string.
    let fd = unsafe { libc::openat(dir.as_raw_fd(), name.as_ptr(), flags | libc::O_CLOEXEC) };
    if fd < 0 {
        return Err(std::io::Error::last_os_error());
    }
    // SAFETY: `fd` is a fresh descriptor owned by nothing else.
    Ok(unsafe { fs::File::from_raw_fd(fd) })
}
/// Package walk over opened descriptors (WR RV-2, HY-3, HY-5). Every entry is
/// opened no-follow and non-blocking relative to its opened parent and checked
/// with fstat: a link is refused (HY-3) and never followed, a FIFO or device is
/// refused without blocking, and bytes are read against a running budget, so a
/// growing file cannot exceed the bound. Names come from listing the parent's
/// path, accepted only while that path still names the opened directory.
#[cfg(unix)]
fn walk_fd(
    dir: &fs::File,
    path: &Path,
    prefix: &str,
    out: &mut BTreeMap<String, Vec<u8>>,
    budget: &mut (usize, u64),
) -> Result<(), String> {
    use std::io::Read;
    let opened = dir.metadata().map_err(|e| format!("{}: {e}", path.display()))?;
    if !opened.is_dir() {
        return Err(format!("HY-3: non-regular entry {}", path.display()));
    }
    let still_here = || {
        fs::symlink_metadata(path)
            .is_ok_and(|m| m.file_type().is_dir() && same_inode(&m, &opened))
    };
    if !still_here() {
        return Err(format!("package folder changed while read: {}", path.display()));
    }
    let mut names = fs::read_dir(path)
        .map_err(|e| format!("{}: {e}", path.display()))?
        .map(|e| e.map(|e| e.file_name()))
        .collect::<Result<Vec<_>, _>>()
        .map_err(|e| format!("{}: {e}", path.display()))?;
    if !still_here() {
        return Err(format!("package folder changed while read: {}", path.display()));
    }
    names.sort();
    for name in names {
        let shown = path.join(&name);
        let Some(text) = name.to_str() else {
            return Err("package path not UTF-8".into());
        };
        let relative = if prefix.is_empty() { text.to_owned() } else { format!("{prefix}/{text}") };
        let flags = libc::O_RDONLY | libc::O_NOFOLLOW | libc::O_NONBLOCK | libc::O_NOCTTY;
        let entry = match open_at(dir, &name, flags) {
            Ok(entry) => entry,
            Err(e) => {
                let non_regular = e.raw_os_error() == Some(libc::ELOOP)
                    || fs::symlink_metadata(&shown)
                        .is_ok_and(|m| !m.file_type().is_dir() && !m.file_type().is_file());
                return Err(if non_regular {
                    format!("HY-3: non-regular entry {}", shown.display())
                } else {
                    format!("{}: {e}", shown.display())
                });
            }
        };
        let meta = entry.metadata().map_err(|e| format!("{}: {e}", shown.display()))?;
        if meta.is_dir() {
            walk_fd(&entry, &shown, &relative, out, budget)?;
        } else if meta.is_file() {
            budget.0 += 1;
            if budget.0 > PACKAGE_MAX_FILES {
                return Err(HY5_EXCEEDED.into());
            }
            let remaining = PACKAGE_MAX_BYTES - budget.1;
            let mut bytes = Vec::new();
            (&entry)
                .take(remaining + 1)
                .read_to_end(&mut bytes)
                .map_err(|e| format!("{}: {e}", shown.display()))?;
            budget.1 += bytes.len() as u64;
            if budget.1 > PACKAGE_MAX_BYTES {
                return Err(HY5_EXCEEDED.into());
            }
            out.insert(relative, bytes);
        } else {
            return Err(format!("HY-3: non-regular entry {}", shown.display()));
        }
    }
    Ok(())
}
#[cfg(not(unix))]
fn walk(base: &Path, dir: &Path, out: &mut BTreeMap<String, Vec<u8>>) -> Result<(), String> {
    for entry in fs::read_dir(dir).map_err(|e| e.to_string())? {
        let entry = entry.map_err(|e| e.to_string())?;
        let path = entry.path();
        let ty = fs::symlink_metadata(&path)
            .map_err(|e| e.to_string())?
            .file_type();
        if ty.is_dir() {
            walk(base, &path, out)?;
        } else if ty.is_file() {
            let rel = path
                .strip_prefix(base)
                .map_err(|e| e.to_string())?
                .to_str()
                .ok_or("package path not UTF-8")?
                .replace(std::path::MAIN_SEPARATOR, "/");
            out.insert(rel, fs::read(&path).map_err(|e| e.to_string())?);
        } else {
            return Err(format!("HY-3: non-regular entry {}", path.display()));
        }
    }
    Ok(())
}
#[derive(Debug, Clone, serde::Serialize)]
pub struct DraftKey {
    pub draft_location: String,
    pub draft_root: String,
    pub name: String,
}
#[derive(Debug, Clone)]
pub struct Review {
    snapshot: Snapshot,
    pub identity: WorkflowIdentity,
    pub prior: Option<WorkflowIdentity>,
    pub draft_key: String,
    pub draft: DraftKey,
    pub review_ref: String,
}
impl Review {
    pub fn open(
        snapshot: Snapshot,
        live: &Snapshot,
        list_revision: &str,
        identity: WorkflowIdentity,
        prior: Option<WorkflowIdentity>,
        draft: DraftKey,
        review_ref: String,
    ) -> Result<Self, String> {
        identity.validate()?;
        let hygiene = snapshot.hygiene_findings();
        if !hygiene.is_empty() {
            return Err(hygiene.join("; "));
        }
        if !["project", "user"].contains(&identity.origin.as_str()) {
            return Err("registration target must be project or user".into());
        }
        if snapshot.revision != live.revision
            || snapshot.revision != list_revision
            || identity.revision != snapshot.revision
            || identity.revision_method != SNAPSHOT_METHOD
        {
            return Err("DS-6: draft changed while read; review again".into());
        }
        let normalized = snapshot
            .workflow_text()
            .replace("\r\n", "\n")
            .replace('\r', "\n");
        let name = normalized
            .as_str()
            .strip_prefix("---\n")
            .and_then(|s| s.split_once("\n---"))
            .and_then(|(fm, _)| {
                fm.lines()
                    .find_map(|l| l.strip_prefix("name:").map(str::trim))
            });
        if name != Some(identity.name.as_str()) {
            return Err("HY-2: front-matter name differs from target".into());
        }
        if let Some(existing) = &prior {
            if !identity.same_slot(existing) {
                return Err("prior revision belongs to another slot".into());
            }
            if identity
                .derived_from
                .as_deref()
                .is_none_or(|base| !base.same_slot(existing))
            {
                return Err(
                    "DS-3: same-name draft without registered origin; choose a new name".into(),
                );
            }
            if identity.revision == existing.revision {
                return Err("DS-4: identical revision already registered".into());
            }
        }
        if !["project", "user"].contains(&draft.draft_location.as_str())
            || draft.draft_root.is_empty()
            || draft.name != identity.name
            || review_ref.is_empty()
        {
            return Err("review references required".into());
        }
        let draft_key = format!(
            "draft:{}:{}@{}",
            draft.draft_location, draft.name, snapshot.revision
        );
        Ok(Self {
            snapshot,
            identity,
            prior,
            draft_key,
            draft,
            review_ref,
        })
    }
    pub fn snapshot(&self) -> &Snapshot {
        &self.snapshot
    }
    pub fn is_current(&self, live: &Snapshot, latest: Option<&WorkflowIdentity>) -> bool {
        live.revision == self.snapshot.revision && latest == self.prior.as_ref()
    }
    pub fn descriptor(&self) -> serde_json::Value {
        let bound = serde_json::json!({"method":SNAPSHOT_METHOD,"value":self.snapshot.revision});
        serde_json::json!({"record_kind":"a15_descriptor","descriptor_id":format!("descriptor:{}",self.review_ref),"act_kind":"A15","wording":"register workflow revision","subject":self.identity,"bound_content":bound,"relations":{"reviewed_draft":{"draft":self.draft,"content":bound},"prior_revision":self.prior,"derived_from":self.identity.derived_from},"disposition":if self.prior.is_some(){"new revision"}else{"new workflow"},"scope":self.identity.source_root,"purpose":format!("make it available in the {} library",self.identity.origin),"review_ref":self.review_ref,"freshness":{"draft_content":bound,"slot_latest":self.prior.as_ref().map(|p|serde_json::json!({"method":p.revision_method,"value":p.revision}))}})
    }
}
/// Unverified adapter DTO. Field consistency is not an actual capture-owner
/// capability or evidence that A15 occurred; it can never grant selection.
pub struct RegistrationAdapterClaim {
    pub act_ref: String,
    pub subject: WorkflowIdentity,
    pub reviewed_draft: String,
    pub review_ref: String,
    pub prior: Option<WorkflowIdentity>,
}
#[derive(Debug, Clone)]
pub struct RegistrationClaimMatch {
    identity: WorkflowIdentity,
    snapshot: Snapshot,
    claimed_act_ref: String,
}
impl RegistrationClaimMatch {
    pub fn compare(
        review: &Review,
        live: &Snapshot,
        latest: Option<&WorkflowIdentity>,
        claim: RegistrationAdapterClaim,
    ) -> Result<Self, String> {
        if review.identity.revision != review.snapshot.revision
            || review.identity.revision_method != SNAPSHOT_METHOD
        {
            return Err("review identity no longer binds snapshot".into());
        }
        if !review.is_current(live, latest) {
            return Err("changed since review — review again".into());
        }
        if claim.act_ref.is_empty()
            || claim.subject != review.identity
            || claim.reviewed_draft != review.draft_key
            || claim.review_ref != review.review_ref
            || claim.prior != review.prior
        {
            return Err("adapter claim does not match reviewed content and prior slot".into());
        }
        Ok(Self {
            identity: review.identity.clone(),
            snapshot: review.snapshot.clone(),
            claimed_act_ref: claim.act_ref,
        })
    }
    pub fn identity(&self) -> &WorkflowIdentity {
        &self.identity
    }
    pub fn snapshot(&self) -> &Snapshot {
        &self.snapshot
    }
    pub fn claimed_act_ref(&self) -> &str {
        &self.claimed_act_ref
    }
    pub fn selection_eligible(&self) -> bool {
        false
    }
    pub fn evidence(&self) -> serde_json::Value {
        serde_json::json!({"identity":self.identity,"claimedActRef":self.claimed_act_ref,"registrationAuthority":"unverified adapter claim","selectionEligible":false})
    }
}
/// Authority-bearing revision has no DTO constructor. Actual capture-owner
/// capability construction is unavailable until that owner supplies its seam.
#[derive(Debug, Clone)]
pub struct RegisteredRevision {
    identity: WorkflowIdentity,
    snapshot: Snapshot,
    act_ref: String,
}
impl RegisteredRevision {
    pub fn identity(&self) -> &WorkflowIdentity {
        &self.identity
    }
    pub fn act_ref(&self) -> &str {
        &self.act_ref
    }
    pub fn select(&self) -> Selection {
        Selection {
            identity: self.identity.clone(),
            snapshot: self.snapshot.clone(),
            admission: SelectionAdmission::RegisteredRevision,
        }
    }
}
#[derive(Debug, Clone)]
pub struct Selection {
    identity: WorkflowIdentity,
    snapshot: Snapshot,
    admission: SelectionAdmission,
}
/// Read-only provenance carried with selected content, never an admission input.
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum SelectionAdmission {
    RegisteredRevision,
    ProductionBundle {
        manifest_sha256: String,
        release_subject: String,
        holding_library: Option<std::path::PathBuf>,
        bundle_root: Option<std::path::PathBuf>,
    },
    DevelopmentCatalog {
        source_map_sha256: String,
        tranche: String,
    },
    #[cfg(test)]
    SyntheticFixture,
}
impl SelectionAdmission {
    pub fn standing(&self) -> &'static str {
        match self {
            Self::RegisteredRevision => "registered revision",
            Self::ProductionBundle { .. } => production_catalog::PRODUCTION_STANDING,
            Self::DevelopmentCatalog { .. } => development_catalog::STANDING,
            #[cfg(test)]
            Self::SyntheticFixture => "synthetic test fixture; no native or release admission",
        }
    }
}
impl Selection {
    /// Synthetic fixture admission only. Production shipping requires its owning
    /// closed release capability; caller fields/hashes do not establish it.
    #[cfg(test)]
    pub fn synthetic_shipped(
        snapshot: Snapshot,
        identity: WorkflowIdentity,
    ) -> Result<Self, String> {
        identity.validate()?;
        if identity.origin != "bundled"
            || identity.revision != snapshot.revision
            || identity.revision_method != SNAPSHOT_METHOD
        {
            return Err("shipped identity does not bind bytes".into());
        }
        Ok(Self {
            identity,
            snapshot,
            admission: SelectionAdmission::SyntheticFixture,
        })
    }
    /// Synthetic fixture only: a project or user library revision selected as a
    /// registered run would select it, for composition tests (WR-VC-21). It
    /// carries no native A15 and no registration standing.
    #[cfg(test)]
    pub fn synthetic_registered(snapshot: Snapshot, identity: WorkflowIdentity) -> Result<Self, String> {
        identity.validate()?;
        if !["project", "user"].contains(&identity.origin.as_str())
            || identity.revision != snapshot.revision
            || identity.revision_method != SNAPSHOT_METHOD
        {
            return Err("registered identity does not bind bytes".into());
        }
        Ok(Self { identity, snapshot, admission: SelectionAdmission::SyntheticFixture })
    }
    pub fn identity(&self) -> &WorkflowIdentity {
        &self.identity
    }
    pub fn snapshot(&self) -> &Snapshot {
        &self.snapshot
    }
    pub fn admission(&self) -> &SelectionAdmission {
        &self.admission
    }
    pub fn verify_store(&self, path: &Path) -> Result<(), String> {
        if let SelectionAdmission::ProductionBundle {
            holding_library: Some(root),
            ..
        } = &self.admission
        {
            if path != root.join(".chirality/workflows").join(&self.identity.name) {
                return Err("holding library changed; no rebinding".into());
            }
            development_catalog::verify_unregistered_slot(root, &self.identity.name)?;
        }
        if let SelectionAdmission::ProductionBundle {
            bundle_root: Some(root),
            ..
        } = &self.admission
        {
            if path != root.join(&self.identity.name) {
                return Err("bundle location changed; no rebinding".into());
            }
            development_catalog::verify_bundle_manifest(root)?;
        }
        let read = Snapshot::capture(path)
            .map_err(|e| format!("selected revision not resolvable: {e}"))?;
        if read.revision != self.identity.revision {
            return Err("revision not verified".into());
        }
        Ok(())
    }
    /// WR-FRAME-1. The person's brief travels in a second text element. The
    /// text is `compose_run_text`'s, the one composer a trial text also uses.
    pub fn run_start_text(&self, run: &str, folder_label: &str) -> Result<String, String> {
        compose_run_text(&self.identity, &self.snapshot, run, folder_label)
    }
    pub fn run_turn_params(
        &self,
        thread: &str,
        run: &str,
        folder_label: &str,
        person_text: &str,
        client_id: &str,
    ) -> Result<serde_json::Value, String> {
        if thread.is_empty() || client_id.is_empty() {
            return Err("thread and clientUserMessageId required".into());
        }
        let text = self.run_start_text(run, folder_label)?;
        let mut input = vec![serde_json::json!({"type":"text","text":text,"text_elements":[]})];
        if !person_text.is_empty() {
            input.push(serde_json::json!({"type":"text","text":person_text,"text_elements":[]}));
        }
        Ok(serde_json::json!({"threadId":thread,"clientUserMessageId":client_id,"input":input}))
    }
}
/// Collision inventory includes every origin; a selected tuple never follows discovery changes.
pub fn collisions<'a>(name: &str, entries: &'a [WorkflowIdentity]) -> Vec<&'a WorkflowIdentity> {
    entries.iter().filter(|e| e.name == name).collect()
}

/// WR §16.2 lines 2–7 (WR-FRAME-1) for one identity and the exact package
/// bytes it names: the start line, the proposal line, the files line when the
/// package has files besides `WORKFLOW.md`, the begin marker, the body exactly,
/// and the end marker. This is the one composer: a registered run's text
/// (`Selection::run_start_text`, with TX-5's chain line placed before it by
/// `PreparedRunText::start`) and a trial's (`TrialText`, under its header) are
/// both this function's output, so they differ only in the identity's origin
/// fields, the run reference and the folder label (WR TT-3, AC-009).
pub(crate) fn compose_run_text(
    identity: &WorkflowIdentity,
    snapshot: &Snapshot,
    run: &str,
    folder_label: &str,
) -> Result<String, String> {
    if run.is_empty() || run.contains(['\n', '\r']) || folder_label.contains(['\n', '\r']) {
        return Err("run reference / folder label must be single line".into());
    }
    if identity.revision != snapshot.revision {
        return Err("workflow identity does not name these package bytes".into());
    }
    let id = identity;
    let rev = &id.revision[..id.revision.len().min(12)];
    let start=format!("[Chirality] Workflow run start: {} from the {} library \"{}\", revision {}, run {}. Follow the workflow between the two markers below for this run, until the person ends the run.",id.name,id.origin,id.source_root.replace('"',"'"),rev,run);
    let proposal=format!("[Chirality] When you judge this workflow finished, end the message with a line of its own \"Workflow finished: {}:{}\". To propose that another registered workflow runs next, end the message with a line of its own \"Next workflow: <origin>:<name>\", where <origin> is project, user, bundled or host; when you write both, the finished line comes just before it. The person decides; nothing ends or starts until they confirm.",id.origin,id.name);
    let mut lines = vec![start, proposal];
    let others = other_files(snapshot);
    if !others.is_empty() {
        if !valid_folder_label(folder_label) {
            return Err(
                "project-relative or home-relative holding-folder label required (WR TX-7: never an absolute path or a placeholder)".into(),
            );
        }
        lines.push(format!(
            "[Chirality] Other files of this revision, in the folder \"{}\": {}",
            folder_label,
            others.join("; ")
        ));
    }
    lines.push(format!("<<<chirality-workflow {}@{} begin>>>", id.name, rev));
    Ok(format!(
        "{}\n{}\n<<<chirality-workflow {}@{} end>>>",
        lines.join("\n"),
        snapshot.workflow_text(),
        id.name,
        rev
    ))
}
fn other_files(snapshot: &Snapshot) -> Vec<String> {
    snapshot
        .files
        .iter()
        .filter(|(p, _)| p.as_str() != "WORKFLOW.md")
        .map(|(p, b)| format!("{p} (sha256 {})", &sha256_hex(b)[..12]))
        .collect()
}

/// WR §16.2 line 4 and TX-7: a folder the files line may name. It is relative
/// to the conversation's project (`.chirality/…`) or to the home folder
/// (`~/…`), one line, with no `"`, backslash or control character and no empty,
/// `.` or `..` component. Never an absolute path.
pub(crate) fn valid_folder_label(label: &str) -> bool {
    let rest = label.strip_prefix("~/").unwrap_or(label);
    !rest.is_empty()
        && !rest.starts_with('~')
        && !rest.starts_with('/')
        && !label.chars().any(|c| c.is_control() || c == '"' || c == '\\')
        && rest.split('/').all(|c| !c.is_empty() && c != "." && c != "..")
}

/// WR §3 and TX-7(c): where the App writes content-addressed supply copies.
pub const SUPPLY_AREA: &str = "workflow-supply";
/// WR §3 and TT-8: where the App writes trial snapshots.
#[allow(dead_code)] // the trial flows (WR §17 steps 5–8) are its callers
pub const TRIAL_AREA: &str = "workflow-trials";

/// How the files line's folder was established (TX-7).
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum FilesFolderBasis {
    /// The package is `WORKFLOW.md` only: there is no files line.
    NoOtherFiles,
    /// (a) The holding folder is inside the explicitly opened project.
    ProjectRelative,
    /// (b) The holding folder is inside the home folder.
    HomeRelative,
    /// (c) A content-addressed supply copy in the project names the files;
    /// `reused` when an identical copy was already there.
    SupplyCopy { path: std::path::PathBuf, reused: bool },
}
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct FilesFolder {
    /// The folder the files line names; empty when there is no files line.
    pub label: String,
    pub basis: FilesFolderBasis,
}
impl FilesFolder {
    pub fn describe(&self) -> serde_json::Value {
        match &self.basis {
            FilesFolderBasis::NoOtherFiles => serde_json::json!({"basis":"no other files; no files line"}),
            FilesFolderBasis::ProjectRelative => serde_json::json!({"basis":"holding folder inside the project","folder":self.label}),
            FilesFolderBasis::HomeRelative => serde_json::json!({"basis":"holding folder inside the home folder","folder":self.label}),
            FilesFolderBasis::SupplyCopy { reused, .. } => serde_json::json!({"basis":if *reused {"supply copy in the project (already present, recomputed)"} else {"supply copy in the project (written, recomputed)"},"folder":self.label,"retention":"never rewritten or removed by the App; if deleted, the next run start recreates it"}),
        }
    }
}
/// The label for `folder` when it is inside `project` (project-relative) or
/// inside `home` (`~/`-relative), in that order; None otherwise. Lexical: both
/// roots are the App's absolute paths, and a folder reached through another
/// spelling of them is treated as outside (and gets a supply copy).
pub(crate) fn relative_folder_label(
    folder: &Path,
    project: Option<&Path>,
    home: Option<&Path>,
) -> Option<(String, FilesFolderBasis)> {
    let relative = |root: &Path| -> Option<String> {
        if !root.is_absolute() {
            return None;
        }
        let rest = folder.strip_prefix(root).ok()?;
        let parts = rest
            .components()
            .map(|c| match c {
                std::path::Component::Normal(s) => s.to_str().map(str::to_owned),
                _ => None,
            })
            .collect::<Option<Vec<_>>>()?;
        (!parts.is_empty()).then(|| parts.join("/"))
    };
    if let Some(label) = project.and_then(relative).filter(|l| valid_folder_label(l)) {
        return Some((label, FilesFolderBasis::ProjectRelative));
    }
    home.and_then(relative)
        .map(|r| format!("~/{r}"))
        .filter(|l| valid_folder_label(l))
        .map(|l| (l, FilesFolderBasis::HomeRelative))
}
/// WR §16.2 TX-7: the folder a run text's files line names for `snapshot`
/// held at `holding`: (a) project-relative, (b) `~/`-relative, or (c) a
/// content-addressed supply copy under
/// `<project>/.chirality/workflow-supply/<name>/<content key>/<name>/`, written
/// from the selected bytes (or reused when identical) and recomputed before it
/// is named. Refused, with the cause, when the copy cannot be written or does
/// not recompute: the run does not start. Never absolute, never a placeholder.
pub fn files_folder(
    snapshot: &Snapshot,
    identity: &WorkflowIdentity,
    holding: &Path,
    project: &Path,
    home: Option<&Path>,
) -> Result<FilesFolder, String> {
    if identity.revision != snapshot.revision {
        return Err("workflow identity does not name these package bytes".into());
    }
    if other_files(snapshot).is_empty() {
        return Ok(FilesFolder { label: String::new(), basis: FilesFolderBasis::NoOtherFiles });
    }
    if let Some((label, basis)) = relative_folder_label(holding, Some(project), home) {
        return Ok(FilesFolder { label, basis });
    }
    let refuse = |cause: String| format!("other files of this revision could not be supplied: {cause}");
    if !project.is_absolute() {
        return Err(refuse("no explicit absolute project folder to hold a supply copy".into()));
    }
    let dest = package_copy::content_folder(project, SUPPLY_AREA, &identity.name, &snapshot.revision);
    let (label, _) = relative_folder_label(&dest, Some(project), None)
        .ok_or_else(|| refuse(format!("{} cannot be named relative to the project", dest.display())))?;
    let copy = package_copy::write_content_copy(snapshot, &dest).map_err(refuse)?;
    Ok(FilesFolder {
        label,
        basis: FilesFolderBasis::SupplyCopy { path: copy.path, reused: copy.reused },
    })
}

/// The front-matter `name` of `WORKFLOW.md`, read as the review reads it (HY-2).
#[allow(dead_code)] // the trial flows (WR §17 steps 5–8) are its callers
pub(crate) fn declared_name(snapshot: &Snapshot) -> Option<String> {
    let normalized = snapshot.workflow_text().replace("\r\n", "\n").replace('\r', "\n");
    normalized
        .strip_prefix("---\n")
        .and_then(|s| s.split_once("\n---"))
        .and_then(|(fm, _)| fm.lines().find_map(|l| l.strip_prefix("name:").map(|n| n.trim().to_owned())))
}

/// WR §4.2 TT-3 (framing WR-TRIAL-1): the text a trial's agent receives. One
/// trial header line, then the run text `compose_run_text` gives for a
/// registered run of the draft's exact content in its target slot (SP-2: the
/// draft's library, under its folder name; revision = the draft content
/// identity, ID-2), with the trial reference as the run reference, no chain
/// line, and the trial snapshot folder (TT-8) in the files line. It opens no
/// run and is never a run text (TT-2, TX-1): there is no `run_text` or
/// `supply_check` record for it, and nothing here writes anything.
#[derive(Debug, Clone)]
#[allow(dead_code)] // the trial flows (WR §17 steps 5–8) are its callers
pub struct TrialText {
    reference: String,
    sequence: u64,
    location: String,
    name: String,
    content: String,
    snapshot_folder: String,
    header_len: usize,
    text: String,
}
#[allow(dead_code)] // the trial flows (WR §17 steps 5–8) are its callers
pub(crate) fn valid_trial_reference(reference: &str) -> bool {
    reference
        .strip_prefix("trial:")
        .is_some_and(|u| u.len() == 36 && uuid::Uuid::parse_str(u).is_ok_and(|p| p.hyphenated().to_string() == u))
}
#[allow(dead_code)] // the trial flows (WR §17 steps 5–8) are its callers
impl TrialText {
    pub fn compose(
        location: &str,
        source_root: &str,
        name: &str,
        snapshot: &Snapshot,
        sequence: u64,
        reference: &str,
        snapshot_folder: &str,
    ) -> Result<Self, String> {
        if !["project", "user"].contains(&location) {
            return Err("a draft's location is project or user".into());
        }
        if sequence == 0 || !valid_trial_reference(reference) {
            return Err("trial sequence and `trial:<uuid>` reference required".into());
        }
        let mut findings = snapshot.hygiene_findings();
        if !valid_name(name) {
            findings.push(format!("HY-2: folder name {name:?} does not follow the workflow name rule"));
        } else if declared_name(snapshot).as_deref() != Some(name) {
            findings.push(format!("HY-2: front-matter name differs from the folder name {name:?}"));
        }
        if !findings.is_empty() {
            return Err(format!("cannot be tried: {}", findings.join("; ")));
        }
        let target = snapshot.identity(location, source_root, name, None)?;
        let run_text = compose_run_text(&target, snapshot, reference, snapshot_folder)?;
        let rev = &snapshot.revision[..snapshot.revision.len().min(12)];
        let header = format!("[Chirality] Workflow trial {sequence} of draft {location}:{name}, content {rev} (trial {reference}). Not registered; not a workflow run. The lines below are the run text a registered run of this exact content would receive, except its run reference and the folder named for other files.");
        Ok(Self {
            reference: reference.into(),
            sequence,
            location: location.into(),
            name: name.into(),
            content: snapshot.revision.clone(),
            snapshot_folder: snapshot_folder.into(),
            header_len: header.len(),
            text: format!("{header}\n{run_text}"),
        })
    }
    /// The whole trial text: header line, line feed, run text.
    pub fn text(&self) -> &str {
        &self.text
    }
    pub fn header(&self) -> &str {
        &self.text[..self.header_len]
    }
    /// The trial text less its header: the §16.2 run text of this content.
    pub fn run_text(&self) -> &str {
        &self.text[self.header_len + 1..]
    }
    /// TX-4 exact-bytes identity of the whole trial text.
    pub fn identity(&self) -> serde_json::Value {
        exact_text_identity(&self.text)
    }
    pub fn bytes(&self) -> usize {
        self.text.len()
    }
    pub fn reference(&self) -> &str {
        &self.reference
    }
    pub fn sequence(&self) -> u64 {
        self.sequence
    }
    pub fn location(&self) -> &str {
        &self.location
    }
    pub fn name(&self) -> &str {
        &self.name
    }
    /// The draft content identity value (SNAPSHOT_METHOD) this text tries.
    pub fn content(&self) -> &str {
        &self.content
    }
    pub fn snapshot_folder(&self) -> &str {
        &self.snapshot_folder
    }
    /// The begin-marker line TT-9 links a sub-agent by.
    pub fn begin_marker(&self) -> String {
        format!("<<<chirality-workflow {}@{} begin>>>", self.name, &self.content[..self.content.len().min(12)])
    }
    /// TT-9's fidelity reading of one first user message's text elements, as
    /// read. Pure: it reads nothing and records nothing.
    pub fn fidelity(&self, texts: &[&str]) -> FidelityReading {
        let run = self.run_text();
        if let Some(found) = texts.iter().find(|t| t.contains(run)) {
            return FidelityReading::Verbatim {
                header_present: found.contains(self.text.as_str()),
                observed: exact_text_identity(found),
            };
        }
        let marker = self.begin_marker();
        let Some(chosen) = texts.iter().find(|t| t.contains(&marker)).or(texts.first()) else {
            return FidelityReading::NotChecked {
                limits: vec!["the first user message carries no text element".into()],
            };
        };
        let expected = expected_marker_body(run, run);
        let observed = expected_marker_body(run, chosen);
        let difference = match observed {
            None => FidelityDifference::WorkflowNotFound,
            Some(body) if Some(body) == expected => FidelityDifference::FramingDiffers,
            Some(_) => FidelityDifference::BodyDiffers,
        };
        FidelityReading::Differs { difference, observed: exact_text_identity(chosen) }
    }
}
/// TT-9 readings (schema `trial_fidelity`).
#[derive(Debug, Clone, PartialEq)]
#[allow(dead_code)] // the trial flows (WR §17 steps 5–8) are its callers
pub enum FidelityReading {
    Verbatim { header_present: bool, observed: serde_json::Value },
    Differs { difference: FidelityDifference, observed: serde_json::Value },
    NotChecked { limits: Vec<String> },
}
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
#[allow(dead_code)] // the trial flows (WR §17 steps 5–8) are its callers
pub enum FidelityDifference {
    FramingDiffers,
    BodyDiffers,
    WorkflowNotFound,
}
#[allow(dead_code)]
impl FidelityDifference {
    pub fn text(self) -> &'static str {
        match self {
            Self::FramingDiffers => "framing differs, workflow body equal",
            Self::BodyDiffers => "workflow body differs",
            Self::WorkflowNotFound => "workflow not found",
        }
    }
}
#[allow(dead_code)]
impl FidelityReading {
    /// The schema `trial_fidelity` object for this reading of `read_thread`.
    pub fn record(&self, read_thread: Option<&str>, mut limits: Vec<String>) -> serde_json::Value {
        match self {
            Self::Verbatim { header_present, observed } => serde_json::json!({"state":"verbatim","header_present":header_present,"read_thread":read_thread,"observed_text":observed,"limits":limits}),
            Self::Differs { difference, observed } => serde_json::json!({"state":"differs","difference":difference.text(),"read_thread":read_thread,"observed_text":observed,"limits":limits}),
            Self::NotChecked { limits: own } => {
                limits.extend(own.iter().cloned());
                serde_json::json!({"state":"not checked","read_thread":read_thread,"limits":limits})
            }
        }
    }
}

#[derive(Debug, Clone, serde::Serialize, PartialEq, Eq)]
#[serde(rename_all = "snake_case")]
pub enum UntrustedPageComparisonState {
    EqualClaimedText,
    TextDiffersWorkflowBytesEqual,
    TextDiffersWorkflowBytesDiffer,
    NotFound,
    Unreadable,
}
#[derive(Debug, Clone, serde::Serialize)]
pub struct UntrustedPageComparison {
    pub state: UntrustedPageComparisonState,
    pub expected_text: serde_json::Value,
    pub observed_text: Option<serde_json::Value>,
    pub turn: String,
    pub item: Option<String>,
    pub located_by: Option<String>,
    pub adoption: String,
    pub evidence_limits: Vec<String>,
}
/// SC-3 location over one turn's item pages, read in order. Data only: the
/// caller owns whether these pages are genuine native observations.
#[derive(Debug, Clone, PartialEq, Eq)]
pub(crate) enum LocatedTurnText {
    /// A page could not be read or its shape/cursor progression was not usable.
    Unreadable,
    /// No user message, or the selected message has no text element.
    NotFound {
        item: Option<String>,
        by_client: Option<bool>,
    },
    /// The first text element of the selected user message.
    Text {
        item: Option<String>,
        by_client: bool,
        text: String,
    },
}
pub(crate) fn locate_turn_text(
    turn: &str,
    client_id: &str,
    mut read: impl FnMut(Option<&str>) -> Result<serde_json::Value, String>,
) -> LocatedTurnText {
    let mut cursor: Option<String> = None;
    let mut seen = std::collections::BTreeSet::new();
    let mut messages = vec![];
    loop {
        let Ok(page) = read(cursor.as_deref()) else {
            return LocatedTurnText::Unreadable;
        };
        let Some(data) = page["data"].as_array() else {
            return LocatedTurnText::Unreadable;
        };
        for entry in data {
            if entry["turnId"].as_str() != Some(turn) {
                continue;
            }
            let Some(item) = entry.get("item") else {
                return LocatedTurnText::Unreadable;
            };
            if item["type"] == "userMessage" {
                messages.push(item.clone());
            }
        }
        match page.get("nextCursor") {
            None | Some(serde_json::Value::Null) => break,
            Some(serde_json::Value::String(c)) if !c.is_empty() && seen.insert(c.clone()) => {
                cursor = Some(c.clone())
            }
            _ => return LocatedTurnText::Unreadable,
        }
    }
    let matched = messages.iter().find(|item| item["clientId"] == client_id);
    let selected = matched.or_else(|| messages.first());
    let Some(item) = selected else {
        return LocatedTurnText::NotFound {
            item: None,
            by_client: None,
        };
    };
    let id = item["id"].as_str().map(String::from);
    let text = item["content"]
        .as_array()
        .and_then(|a| a.iter().find(|v| v["type"] == "text"))
        .and_then(|v| v["text"].as_str());
    match text {
        Some(text) => LocatedTurnText::Text {
            item: id,
            by_client: matched.is_some(),
            text: text.into(),
        },
        None => LocatedTurnText::NotFound {
            item: id,
            by_client: Some(matched.is_some()),
        },
    }
}
/// Compare untrusted purported pages as data only. This route cannot report
/// native verification/supply; actual supply requires the Core-owned capability.
pub fn compare_untrusted_pages(
    expected: &str,
    turn: &str,
    client_id: &str,
    read: impl FnMut(Option<&str>) -> Result<serde_json::Value, String>,
) -> UntrustedPageComparison {
    let cid = |text: &str| serde_json::json!({"method":crate::role_supply::CONTENT_METHOD,"value":sha256_hex(text.as_bytes())});
    let mut result = UntrustedPageComparison {
        state: UntrustedPageComparisonState::Unreadable,
        expected_text: cid(expected),
        observed_text: None,
        turn: turn.into(),
        item: None,
        located_by: None,
        adoption: "unknown".into(),
        evidence_limits:vec!["untrusted purported pages; byte comparison is not native verification, supplied guidance, active run, A15 or adoption".into()],
    };
    let by = |client: bool| {
        if client {
            "client_user_message_id"
        } else {
            "first_user_message"
        }
        .to_owned()
    };
    let text = match locate_turn_text(turn, client_id, read) {
        LocatedTurnText::Unreadable => return result,
        LocatedTurnText::NotFound { item, by_client } => {
            result.item = item;
            result.located_by = by_client.map(by);
            result.state = UntrustedPageComparisonState::NotFound;
            return result;
        }
        LocatedTurnText::Text {
            item,
            by_client,
            text,
        } => {
            result.item = item;
            result.located_by = Some(by(by_client));
            text
        }
    };
    {
        let text = text.as_str();
        result.observed_text = Some(cid(text));
        result.state = if text == expected {
            UntrustedPageComparisonState::EqualClaimedText
        } else {
            if expected_marker_body(expected, expected).is_some()
                && expected_marker_body(expected, expected) == expected_marker_body(expected, text)
            {
                UntrustedPageComparisonState::TextDiffersWorkflowBytesEqual
            } else {
                UntrustedPageComparisonState::TextDiffersWorkflowBytesDiffer
            }
        };
    }
    result
}

fn expected_marker_body<'a>(expected: &str, observed: &'a str) -> Option<&'a str> {
    let begin = expected
        .lines()
        .find(|line| line.starts_with("<<<chirality-workflow ") && line.ends_with(" begin>>>"))?;
    let end = begin.strip_suffix(" begin>>>")?.to_owned() + " end>>>";
    let start = observed
        .match_indices(&(begin.to_owned() + "\n"))
        .find(|(i, _)| *i == 0 || observed.as_bytes().get(i - 1) == Some(&b'\n'))?
        .0
        + begin.len()
        + 1;
    let marker = "\n".to_owned() + &end;
    let finish = observed
        .match_indices(&marker)
        .filter(|(i, _)| {
            let after = i + marker.len();
            after == observed.len() || observed.as_bytes().get(after) == Some(&b'\n')
        })
        .last()?
        .0;
    observed.get(start..finish)
}

/// App-owned preparing scope. It does not establish an active native run or a
/// registration act; selection admission and actual callbacks belong to owners.
#[derive(Clone, Debug)]
pub struct RunScope {
    pub run: String,
    pub conversation: String,
    pub home: String,
    pub generation: serde_json::Value,
    pub source_root: String,
    pub holding_library: String,
    pub selection_ref: String,
    pub revision_store: std::path::PathBuf,
}
impl RunScope {
    fn validate(&self, selection: &Selection) -> Result<(), String> {
        if [
            &self.run,
            &self.conversation,
            &self.home,
            &self.source_root,
            &self.holding_library,
            &self.selection_ref,
        ]
        .iter()
        .any(|s| s.is_empty() || s.contains(['\n', '\r']))
            || self.generation.as_object().is_none_or(|o| o.len() != 3)
            || self.generation["home"] != self.home
            || self.generation["appSession"]
                .as_str()
                .is_none_or(str::is_empty)
            || self.generation["spawnCounter"].as_u64().unwrap_or(0) == 0
            || self.source_root != selection.identity.source_root
        {
            return Err("run/source/home/full-generation scope not established".into());
        }
        Ok(())
    }
}
#[derive(Clone, Debug)]
pub enum RunEndReason {
    ByPerson,
    Completed,
    ToStart(String),
}
impl RunEndReason {
    fn text(&self) -> Result<String, String> {
        match self {
            Self::ByPerson => Ok("ended by the person".into()),
            Self::Completed => Ok("completed".into()),
            Self::ToStart(name) if valid_name(name) => Ok(format!("ended to start {name}")),
            _ => Err("end successor name invalid".into()),
        }
    }
}
/// This is an owning EXEC/RECOVERY callback contract, not proof minted by a
/// serialized marker or the agent's completion sentence. No Deserialize path.
#[derive(Clone, Debug)]
pub struct OwnerRunEnd {
    pub home: String,
    pub conversation: String,
    pub run: String,
    pub workflow: WorkflowIdentity,
    pub reason: RunEndReason,
}
#[derive(Clone, Debug)]
pub struct PreparedRunText {
    admission: SelectionAdmission,
    scope: RunScope,
    workflow: WorkflowIdentity,
    text: String,
    record: serde_json::Value,
    /// WR PR-4: the agent message whose proposal the person confirmed, if any.
    proposal: Option<serde_json::Value>,
}
fn exact_text_identity(text: &str) -> serde_json::Value {
    crate::role_supply::content(text.as_bytes())
}
fn wr_validate(target: &str, value: &serde_json::Value) -> Result<(), String> {
    let wd: serde_json::Value =
        serde_json::from_str(crate::workflow_declaration::SCHEMA).map_err(|e| e.to_string())?;
    let wr: serde_json::Value = serde_json::from_str(include_str!(
        "../resources/workflow_role/workspace-registration.schema.json"
    ))
    .map_err(|e| e.to_string())?;
    let mut registry = jsonschema::Registry::new();
    for schema in [wd, wr.clone()] {
        registry = registry
            .add(
                schema["$id"].as_str().ok_or("WR/WD ID absent")?,
                schema.clone(),
            )
            .map_err(|e| e.to_string())?;
    }
    let registry = registry.prepare().map_err(|e| e.to_string())?;
    let validator=jsonschema::options().with_registry(&registry).offline().build(&serde_json::json!({"$ref":format!("{}#/$defs/{target}",wr["$id"].as_str().ok_or("WR ID absent")?)})).map_err(|e|e.to_string())?;
    validator
        .validate(value)
        .map_err(|e| format!("WR {target} refused: {e}"))
}
impl PreparedRunText {
    pub fn start(
        selection: &Selection,
        scope: RunScope,
        folder_label: &str,
        prior: Option<&OwnerRunEnd>,
    ) -> Result<Self, String> {
        scope.validate(selection)?;
        selection.verify_store(&scope.revision_store)?;
        let mut text = selection.run_start_text(&scope.run, folder_label)?;
        let mut chain = serde_json::Value::Null;
        if let Some(prior) = prior {
            prior.workflow.validate()?;
            if prior.home != scope.home
                || prior.conversation != scope.conversation
                || prior.run.is_empty()
                || prior.run == scope.run
            {
                return Err("prior run end belongs to another scope".into());
            }
            let reason = prior.reason.text()?;
            let line=format!("[Chirality] Previous workflow run ended: {} revision {} (run {}, {}). Its instructions no longer apply.",prior.workflow.name,&prior.workflow.revision.chars().take(12).collect::<String>(),prior.run,reason);
            text = format!("{line}\n{text}");
            chain = serde_json::json!({"prior_run":prior.run,"prior_workflow":prior.workflow,"ended":reason});
        }
        let mut lines = serde_json::Map::new();
        for line in text
            .lines()
            .take_while(|s| !s.starts_with("<<<chirality-workflow "))
        {
            let key = if line.starts_with("[Chirality] Previous") {
                "chain_line"
            } else if line.starts_with("[Chirality] Workflow run start") {
                "start_line"
            } else if line.starts_with("[Chirality] When") {
                "proposal_line"
            } else {
                "files_line"
            };
            lines.insert(key.into(), line.into());
        }
        let revision = &selection.identity.revision[..selection.identity.revision.len().min(12)];
        lines.insert(
            "begin_marker".into(),
            format!(
                "<<<chirality-workflow {}@{} begin>>>",
                selection.identity.name, revision
            )
            .into(),
        );
        lines.insert(
            "end_marker".into(),
            format!(
                "<<<chirality-workflow {}@{} end>>>",
                selection.identity.name, revision
            )
            .into(),
        );
        let body = selection.snapshot.workflow_text();
        let mut record = serde_json::json!({"record_kind":"run_text","purpose":"run start","framing":"WR-FRAME-1","run":scope.run,"conversation":scope.conversation,"workflow":selection.identity,"holding_library":scope.holding_library,
            "workflow_file":{"path":"WORKFLOW.md","content":exact_text_identity(body),"bytes":body.len()},"chain":chain,"origin_of_start":"selected by the person","selection":scope.selection_ref,"lines":lines,"text_identity":exact_text_identity(&text),"text_bytes":text.len()});
        let other: Vec<_> = selection
            .snapshot
            .files
            .iter()
            .filter(|(p, _)| p.as_str() != "WORKFLOW.md")
            .map(|(path, b)| serde_json::json!({"path":path,"sha256":sha256_hex(b)}))
            .collect();
        if !other.is_empty() {
            record["other_files"] = serde_json::json!(other);
        }
        wr_validate("run_text", &record)?;
        Ok(Self {
            scope,
            workflow: selection.identity.clone(),
            admission: selection.admission.clone(),
            text,
            record,
            proposal: None,
        })
    }
    /// WR PR-4: a start the person confirmed from an agent's proposal line. The
    /// run text is unchanged; its record says how the start came about, and the
    /// selection record cites the proposal. The proposal itself selects nothing.
    pub fn confirmed_from_proposal(mut self, proposal: serde_json::Value) -> Result<Self, String> {
        self.record["origin_of_start"] = serde_json::json!("agent proposal confirmed by the person");
        wr_validate("run_text", &self.record)?;
        self.proposal = Some(proposal);
        Ok(self)
    }
    pub fn proposal(&self) -> Option<&serde_json::Value> {
        self.proposal.as_ref()
    }
    pub fn text(&self) -> &str {
        &self.text
    }
    pub fn record(&self) -> &serde_json::Value {
        &self.record
    }
    pub fn admission(&self) -> &SelectionAdmission {
        &self.admission
    }
    pub fn scope(&self) -> &RunScope {
        &self.scope
    }
    pub fn turn_params(
        &self,
        person_text: &str,
        client_id: &str,
    ) -> Result<serde_json::Value, String> {
        if client_id.is_empty() {
            return Err("client message identity absent".into());
        }
        let mut input =
            vec![serde_json::json!({"type":"text","text":self.text,"text_elements":[]})];
        if !person_text.is_empty() {
            input.push(serde_json::json!({"type":"text","text":person_text,"text_elements":[]}));
        }
        Ok(
            serde_json::json!({"threadId":self.scope.conversation,"clientUserMessageId":client_id,"input":input}),
        )
    }
    pub fn workflow(&self) -> &WorkflowIdentity {
        &self.workflow
    }
    /// TX-5: the end notice as a sendable text element for the person's next
    /// ordinary turn in the same conversation, scoped to the current generation of
    /// the same home. Composition only; no lifecycle event is created here.
    pub fn notice_turn(
        &self,
        end: &OwnerRunEnd,
        current_generation: &serde_json::Value,
    ) -> Result<Self, String> {
        let (text, record) = self.end_notice(end)?;
        if current_generation["home"] != self.scope.home {
            return Err("end notice belongs to another home".into());
        }
        let mut scope = self.scope.clone();
        scope.generation = current_generation.clone();
        Ok(Self {
            admission: self.admission.clone(),
            scope,
            workflow: self.workflow.clone(),
            text,
            record,
            proposal: None,
        })
    }
    /// The same composed text and record, scoped to a later generation of the
    /// same home (V10 G-1). Text, record and identities are unchanged.
    pub fn with_generation(&self, current_generation: &serde_json::Value) -> Result<Self, String> {
        if current_generation["home"] != self.scope.home {
            return Err("text belongs to another home".into());
        }
        let mut copy = self.clone();
        copy.scope.generation = current_generation.clone();
        Ok(copy)
    }
    pub fn end_notice(&self, end: &OwnerRunEnd) -> Result<(String, serde_json::Value), String> {
        if end.home != self.scope.home
            || end.conversation != self.scope.conversation
            || end.run != self.scope.run
            || end.workflow != self.workflow
        {
            return Err("end event does not identify this run".into());
        }
        let reason = end.reason.text()?;
        if matches!(&end.reason, RunEndReason::ToStart(_)) {
            return Err("successor start uses chain line, not end notice".into());
        }
        let text = format!(
            "[Chirality] Workflow run ended: {} revision {} (run {}, {}). No workflow is in force.",
            self.workflow.name,
            &self.workflow.revision[..self.workflow.revision.len().min(12)],
            self.scope.run,
            reason
        );
        let record = serde_json::json!({"record_kind":"run_text","purpose":"run end notice","framing":"WR-FRAME-1","run":self.scope.run,"conversation":self.scope.conversation,"lines":{"end_line":text},"text_identity":exact_text_identity(&text),"text_bytes":text.len()});
        wr_validate("run_text", &record)?;
        Ok((text, record))
    }
    /// TX3 locates this selected tuple's exact marker lines, not an arbitrary
    /// workflow-shaped pair from observed text. No source-byte normalization.
    fn selected_body<'a>(&self, observed: &'a str) -> Option<&'a str> {
        let revision = self.workflow.revision.chars().take(12).collect::<String>();
        let begin = format!(
            "<<<chirality-workflow {}@{} begin>>>\n",
            self.workflow.name, revision
        );
        let end = format!(
            "\n<<<chirality-workflow {}@{} end>>>",
            self.workflow.name, revision
        );
        let start = observed
            .match_indices(&begin)
            .find(|(i, _)| *i == 0 || observed.as_bytes().get(i - 1) == Some(&b'\n'))?
            .0
            + begin.len();
        let finish = observed
            .match_indices(&end)
            .filter(|(i, _)| {
                let after = i + end.len();
                after == observed.len() || observed.as_bytes().get(after) == Some(&b'\n')
            })
            .last()?
            .0;
        if finish < start {
            return None;
        }
        observed.get(start..finish)
    }
    /// Pure content comparison only. A supply_check record may be emitted only
    /// after the owning native accepted-page capability is available; arbitrary
    /// JSON/pages cannot mint that observation here.
    pub fn compare_observed_text(
        &self,
        expected_text: &serde_json::Value,
        expected_body: &serde_json::Value,
        observed: &str,
    ) -> Result<TextComparison, String> {
        wr_validate("text_identity", expected_text)?;
        wr_validate("text_identity", expected_body)?;
        let actual = exact_text_identity(observed);
        let mut limits=vec!["content comparison alone establishes no native supply, A15, active run or model adoption".into()];
        let state = if expected_text["method"] != actual["method"] {
            limits.push("text identity methods incomparable".into());
            "incomparable"
        } else if expected_text == &actual {
            "equal composed text"
        } else if let Some(body) = self.selected_body(observed) {
            if expected_body["method"] != crate::role_supply::CONTENT_METHOD {
                limits.push("body identity methods incomparable; no value-only fallback".into());
                "incomparable"
            } else if expected_body == &exact_text_identity(body) {
                "text differs, workflow bytes equal"
            } else {
                "text differs, workflow bytes differ"
            }
        } else {
            "text differs, workflow bytes differ"
        };
        Ok(TextComparison {
            state: state.into(),
            observed_text: actual,
            evidence_limits: limits,
        })
    }
}
#[derive(Clone, Debug, serde::Serialize)]
pub struct TextComparison {
    pub state: String,
    pub observed_text: serde_json::Value,
    pub evidence_limits: Vec<String>,
}

#[cfg(test)]
#[path = "workflow_role_tests.rs"]
mod workflow_role_tests;

#[cfg(test)]
#[path = "workflow_receiving_tests.rs"]
mod workflow_receiving_tests;

#[cfg(test)]
#[path = "workflow_catalog_tests.rs"]
mod workflow_catalog_tests;

/// Immutable WR evidence publication; resolved JSON confers no live authority.
#[path = "workflow_record_store.rs"]
pub mod publication;

#[cfg(test)]
#[path = "p2_production_catalog_tests.rs"]
mod p2_production_catalog_tests;
