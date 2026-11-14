//! Admission of a new signed-route seal. Absence is a fresh observation of
//! the selected namespace, not a statement about its history. Local evidence
//! can veto the file provider but can never authorize it.
use super::*;
use std::collections::BTreeSet;

// This process remembers having OBSERVED protection. It can only veto; it
// never proves absence or authorizes a provider. Quit loses this memory by
// design, and the next process must observe protected and local evidence anew.
static PROTECTED: std::sync::Mutex<BTreeSet<PathBuf>> = std::sync::Mutex::new(BTreeSet::new());
pub(super) fn remember(root: &Path) {
    PROTECTED.lock().unwrap_or_else(|p| p.into_inner()).insert(root.to_owned());
}
fn remembered(root: &Path) -> bool {
    PROTECTED.lock().unwrap_or_else(|p| p.into_inner()).contains(root)
}
#[cfg(test)]
pub(super) fn forget(root: &Path) { PROTECTED.lock().unwrap_or_else(|p| p.into_inner()).remove(root); }

const LIBRARIES_FILE: &str = "capture-seal-libraries.json";
const LIBRARIES_FORMAT: &str = "chirality.app.capture-seal-library-inventory/v1";
#[derive(Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
struct LibraryInventory {
    format: String,
    roots: BTreeSet<PathBuf>,
    complete: bool,
}
fn inventory_failure(detail: impl std::fmt::Display) -> EvidenceFailure {
    failure(Cause::ProtectionInconsistent, format!("Library protection inventory is incomplete: {detail}. Restore the original complete library list and listed libraries, then open Recover capture verification and check again."))
}
fn library_roots(installation: &Path) -> Result<BTreeSet<PathBuf>, EvidenceFailure> {
    let path = installation.join(LIBRARIES_FILE);
    // Only a missing file means no library known. A present empty, partial or
    // malformed document is an incomplete census, never an empty one. This
    // removable local trace may veto only; losing it is the LIM-026 loss class.
    if !exists(&path)? { return Ok(BTreeSet::new()); }
    let inventory: LibraryInventory = serde_json::from_slice(&snapshot_bytes(&path)?)
        .map_err(|_| inventory_failure("the list is malformed or truncated"))?;
    if inventory.format != LIBRARIES_FORMAT || !inventory.complete
        || inventory.roots.iter().any(|root| !root.is_absolute() || root.components().any(|c| !matches!(c, std::path::Component::RootDir | std::path::Component::Normal(_)))) {
        return Err(inventory_failure("the list has an unknown or incomplete format"));
    }
    Ok(inventory.roots)
}
pub(super) fn register_library(root: &Path) -> Result<(), EvidenceFailure> {
    let installation = crate::capture_seal::installed_root_for_enrollment()
        .map_err(inventory_failure)?;
    crate::storage::check_path(root).map_err(inventory_failure)?;
    if !root.is_absolute() { return Err(inventory_failure("the library root is not absolute")); }
    let root = root.canonicalize().map_err(inventory_failure)?;
    // Append the root logically, publishing the entire closed JSON document
    // atomically under the existing product enrolment join. No root is pruned;
    // this unit has no removal act, including for moved or unavailable roots.
    let join = EnrollmentJoin::acquire(&installation)?;
    let mut roots = library_roots(&installation)?;
    if !roots.insert(root) { return Ok(()); }
    let bytes = serde_json::to_vec(&LibraryInventory { format: LIBRARIES_FORMAT.into(), roots, complete: true })
        .map_err(inventory_failure)?;
    let temp = installation.join(format!(".{LIBRARIES_FILE}.{}.tmp", crate::util::opaque_id("").map_err(inventory_failure)?));
    let result = (|| {
        let mut file = OpenOptions::new().create_new(true).write(true).mode(0o600).open(&temp).map_err(inventory_failure)?;
        file.write_all(&bytes).map_err(inventory_failure)?;
        file.sync_all().map_err(inventory_failure)?;
        join.recheck()?;
        fs::rename(&temp, installation.join(LIBRARIES_FILE)).map_err(inventory_failure)?;
        crate::storage::sync_dir(&installation).map_err(inventory_failure)
    })();
    let _ = fs::remove_file(temp);
    result
}
fn library_trace(root: &Path) -> Result<bool, EvidenceFailure> {
    crate::storage::check_path(root).map_err(inventory_failure)?;
    let held = HeldDirectory::open(root).map_err(inventory_failure)?;
    let before = held.file.metadata().map_err(inventory_failure)?;
    // The listed root must itself be readable. Its disappearance must not be
    // mistaken for an absent capture subfolder in an otherwise readable root.
    for entry in fs::read_dir(root).map_err(inventory_failure)? { entry.map_err(inventory_failure)?; }
    let found = capture_trace(&root.join(crate::storage::CAPTURES), 0)?;
    held.recheck().map_err(inventory_failure)?;
    let after = held.file.metadata().map_err(inventory_failure)?;
    if FileStamp::of(&before) != FileStamp::of(&after) { return Err(inventory_failure("a listed root changed during its census")); }
    Ok(found)
}
/// Participating App operations share the existing enrolment join. Holding a
/// named file is advisory coordination, not a tamper-proof continuity anchor.
pub(super) struct EnrollmentJoin {
    _guard: Guard,
    path: PathBuf,
    stamp: (u64, u64, u32, u32),
}
impl EnrollmentJoin {
    pub(super) fn acquire(parent: &Path) -> Result<Self, EvidenceFailure> {
        crate::storage::check_path(parent).map_err(|e| failure(Cause::KeyStorageUnsafe, e))?;
        let path = parent.join(".seal-c-enrollment.lock");
        let file = OpenOptions::new().read(true).write(true).create(true).truncate(false)
            .mode(0o600).custom_flags(libc::O_NOFOLLOW | libc::O_NONBLOCK).open(&path)
            .map_err(|_| failure(Cause::SealOperationBusy, "SEAL-C enrollment lock unavailable"))?;
        let m = file.metadata().map_err(|_| failure(Cause::SealOperationBusy, "SEAL-C enrollment lock unavailable"))?;
        if !private_metadata(&m, false) {
            return Err(failure(Cause::KeyStorageUnsafe, "SEAL-C enrollment lock unsafe"));
        }
        if unsafe { libc::flock(file.as_raw_fd(), libc::LOCK_EX) } != 0 {
            return Err(failure(Cause::SealOperationBusy, "SEAL-C enrollment lock unavailable"));
        }
        let join = Self { _guard: Guard { file, directory: None }, path, stamp: (m.dev(), m.ino(), m.uid(), m.mode()) };
        join.recheck()?;
        Ok(join)
    }
    pub(super) fn recheck(&self) -> Result<(), EvidenceFailure> {
        let named = fs::symlink_metadata(&self.path).map_err(|_| failure(Cause::SealSourceChanged, "SEAL-C enrollment lock disappeared"))?;
        let held = self._guard.file.metadata().map_err(|_| failure(Cause::SealSourceChanged, "SEAL-C enrollment lock changed"))?;
        let stamp = |m: &fs::Metadata| (m.dev(), m.ino(), m.uid(), m.mode());
        if !private_metadata(&named, false) || stamp(&named) != self.stamp || stamp(&held) != self.stamp {
            return Err(failure(Cause::SealSourceChanged, "SEAL-C enrollment lock identity changed"));
        }
        Ok(())
    }
}
fn exists(path: &Path) -> Result<bool, EvidenceFailure> {
    match fs::symlink_metadata(path) {
        Ok(_) => Ok(true),
        Err(e) if e.kind() == std::io::ErrorKind::NotFound => Ok(false),
        Err(e) => Err(failure(Cause::ProtectionInconsistent, format!("Protection inventory is incomplete at {}: {e}. Recover capture verification and check again.", path.display()))),
    }
}
fn snapshot_bytes(path: &Path) -> Result<Vec<u8>, EvidenceFailure> {
    let mut file = OpenOptions::new().read(true).custom_flags(libc::O_NOFOLLOW | libc::O_NONBLOCK).open(path)
        .map_err(|e| failure(Cause::ProtectionInconsistent, format!("Protection inventory is unreadable at {}: {e}. Recover capture verification and check again.", path.display())))?;
    let before = file.metadata().map_err(|e| failure(Cause::ProtectionInconsistent, e.to_string()))?;
    if !before.is_file() { return Err(failure(Cause::ProtectionInconsistent, "Protection inventory contains a nonregular file. Recover capture verification.")); }
    let mut bytes = Vec::new();
    (&mut file).take(16 * 1024 * 1024 + 1).read_to_end(&mut bytes).map_err(|e| failure(Cause::ProtectionInconsistent, e.to_string()))?;
    if bytes.len() > 16 * 1024 * 1024 { return Err(failure(Cause::ProtectionInconsistent, "Protection inventory is too large to read completely. Recover capture verification.")); }
    let after = file.metadata().map_err(|e| failure(Cause::SealSourceChanged, e.to_string()))?;
    let named = fs::symlink_metadata(path).map_err(|e| failure(Cause::SealSourceChanged, e.to_string()))?;
    if FileStamp::of(&before) != FileStamp::of(&after) || FileStamp::of(&after) != FileStamp::of(&named) {
        return Err(failure(Cause::SealSourceChanged, "Protection inventory changed while it was read. Check again."));
    }
    Ok(bytes)
}
fn keychain_claim(value: &serde_json::Value) -> bool {
    match value {
        serde_json::Value::Object(o) => o.get("sealProvider").is_some_and(|p| p == "keychain") || o.values().any(keychain_claim),
        serde_json::Value::Array(a) => a.iter().any(keychain_claim),
        _ => false,
    }
}
fn capture_trace(directory: &Path, depth: usize) -> Result<bool, EvidenceFailure> {
    crate::storage::check_path(directory).map_err(|e| failure(Cause::ProtectionInconsistent, format!("Protection inventory is incomplete: {e}. Recover capture verification.")))?;
    if !exists(directory)? { return Ok(false) }
    if depth > 3 { return Err(failure(Cause::ProtectionInconsistent, "Protection inventory has an unknown directory shape. Recover capture verification.")); }
    let held = HeldDirectory::open(directory).map_err(|e| failure(Cause::ProtectionInconsistent, e))?;
    let before = held.file.metadata().map_err(|e| failure(Cause::ProtectionInconsistent, e.to_string()))?;
    for entry in fs::read_dir(directory).map_err(|e| failure(Cause::ProtectionInconsistent, e.to_string()))? {
        let path = entry.map_err(|e| failure(Cause::ProtectionInconsistent, e.to_string()))?.path();
        let m = fs::symlink_metadata(&path).map_err(|e| failure(Cause::ProtectionInconsistent, e.to_string()))?;
        if m.is_dir() {
            if capture_trace(&path, depth + 1)? { return Ok(true) }
        } else if m.is_file() && matches!(path.file_name().and_then(|v| v.to_str()), Some(".capture.lock" | ".pending.lock")) {
            continue;
        } else {
            let bytes = snapshot_bytes(&path)?;
            let value = serde_json::from_slice(&bytes).map_err(|_| failure(Cause::ProtectionInconsistent,
                "A capture in the protection inventory cannot be read completely. Recover capture verification and check again."))?;
            if keychain_claim(&value) { return Ok(true) }
            // A syntactically readable JSON value is not a complete inventory
            // observation. Only recognised captures and their pending writer
            // envelopes can establish that no provider claim was omitted.
            let recognised = if path.parent().and_then(Path::file_name).is_some_and(|name| name == "pending") {
                crate::records::recognise_capture_submission(&value, &crate::act_control::ActControl::capture_submission_log(&value["capture"]))
                    .map(|_| ())
            } else {
                crate::schema_validation::validate_capture(&value)
            };
            recognised.map_err(|e| failure(Cause::ProtectionInconsistent, format!(
                "A capture in the protection inventory has an unknown or incomplete shape: {e}. Recover capture verification and check again.")))?;
        }
    }
    held.recheck().map_err(|e| failure(Cause::SealSourceChanged, e))?;
    let after = held.file.metadata().map_err(|e| failure(Cause::SealSourceChanged, e.to_string()))?;
    if FileStamp::of(&before) != FileStamp::of(&after) { return Err(failure(Cause::SealSourceChanged, "Protection inventory changed while it was read. Check again.")); }
    Ok(false)
}
fn known_captures(installation: &Path, current: &Path) -> Result<Vec<PathBuf>, EvidenceFailure> {
    let (store, _) = crate::records_store::opened_existing().map_err(|e| failure(Cause::ProtectionInconsistent, format!("Records-store protection inventory is unknown: {e}. Restore the configured store and check again.")))?;
    crate::storage::check_path(&store).map_err(|e| failure(Cause::ProtectionInconsistent, e))?;
    let mut result = vec![current.join(crate::storage::CAPTURES)];
    let projects = store.join("projects");
    if exists(&projects)? {
        crate::storage::check_path(&projects).map_err(|e| failure(Cause::ProtectionInconsistent, e))?;
        for entry in fs::read_dir(projects).map_err(|e| failure(Cause::ProtectionInconsistent, e.to_string()))? {
            let path = entry.map_err(|e| failure(Cause::ProtectionInconsistent, e.to_string()))?.path();
            if !fs::symlink_metadata(&path).is_ok_and(|m| m.is_dir()) {
                return Err(failure(Cause::ProtectionInconsistent, "The records-store project inventory is incomplete. Restore access and check again."));
            }
            result.push(path.join("captures"));
        }
    }
    for library in library_roots(installation)? {
        if library_trace(&library)? {
            return Err(failure(Cause::ProtectionInconsistent, "A keychain-labelled capture survives in a known library. No file key is substituted. Open Recover capture verification."));
        }
    }
    result.sort(); result.dedup();
    Ok(result)
}
fn local_veto(root: &Path, captures: &[PathBuf], continuity: bool) -> Result<(), EvidenceFailure> {
    if remembered(root) || (continuity && exists(&root.join("capture-seal-keychain"))?) || exists(&root.join(POLICY_HEAD))? {
        return Err(failure(Cause::ProtectionInconsistent, "Earlier keychain protection is indicated here. No file key is substituted. Open Recover capture verification."));
    }
    for path in captures {
        if capture_trace(path, 0)? {
            return Err(failure(Cause::ProtectionInconsistent, "A keychain-labelled capture survives in the records or library store. No file key is substituted. Open Recover capture verification."));
        }
    }
    Ok(())
}
pub(super) fn selected_lookup(expected: &EnrollmentPolicy, authority: &KeychainAuthority) -> Result<(), EvidenceFailure> {
    validate_identity(&authority.identity).map_err(|e| failure(Cause::AuthorityUnavailable, e))?;
    if expected != &authority.enrollment_policy() {
        return Err(failure(Cause::AuthorityUnavailable, "SEAL-C installed lookup identity differs from the selected namespace; no absence is admitted"));
    }
    Ok(())
}
pub(super) fn with_material<R>(legacy: &Path, current: &Path, authority: &KeychainAuthority,
    backend: &(impl Backend + ?Sized), inventory: Option<&[PathBuf]>, attach_seal: impl FnOnce(Option<Material>) -> Result<R, EvidenceFailure>) -> Result<R, EvidenceFailure> {
    let root = legacy.parent().ok_or_else(|| failure(Cause::SealRootUnavailable, "SEAL-C installation root unavailable"))?;
    let join = EnrollmentJoin::acquire(root)?;
    let protection = protection_observation(backend, &authority.identity, Some(&root.join(POLICY_HEAD)))?;
    if protection.enrolled || protection.policy.is_some() { remember(root); }
    let enrolled = protection.enrolled;
    policy_from_observation(protection)?;
    if enrolled {
        let material = operate(&legacy.with_file_name("capture-seal-keychain"), legacy, &authority.identity, authority.allow_first,
            backend, Operation::Seal, &mut || Err("no new key during capture sealing".into()))?;
        join.recheck()?;
        return attach_seal(Some(material));
    }
    let mut captures = known_captures(root, current)?;
    if let Some(extra) = inventory { captures.extend_from_slice(extra); }
    local_veto(root, &captures, true)?;
    // A final fresh sentinel observation closes ordinary concurrent enrolment
    // under the intact join. Never cache a positive absence observation.
    match backend.read(&authority.identity) {
        Err(BackendError::Missing) => (),
        Ok(_) => { remember(root); return Err(failure(Cause::ProtectionInconsistent, "Protection appeared while admitting the file key. Recover capture verification.")); }
        Err(error) => return Err(backend_failure(error)),
    }
    join.recheck()?;
    // No further recheck around attachment: undetected join replacement in
    // that window is the expressly accepted release exclusion.
    attach_seal(None)
}
pub(super) fn fresh(legacy: &Path, identity: &ItemIdentity, backend: &(impl Backend + ?Sized)) -> Result<(), EvidenceFailure> {
    let root = legacy.parent().ok_or_else(|| failure(Cause::SealRootUnavailable, "SEAL-C installation root unavailable"))?;
    let p = protection_observation(backend, identity, Some(&root.join(POLICY_HEAD)))?;
    if p.enrolled || p.policy.is_some() { remember(root); return Err(failure(Cause::ProtectionInconsistent, "SEAL-C namespace not demonstrably new; enrollment refused")); }
    let inventory = known_captures(root, root)?;
    local_veto(root, &inventory, false)
}

/// Legacy bytes use only the currently admitted route. This observes absence
/// read-only; it never creates the enrolment join, a file key or a provider label.
pub(super) fn legacy_material(legacy: &Path, current: &Path, authority: &KeychainAuthority,
    backend: &(impl Backend + ?Sized), inventory: Option<&[PathBuf]>, id: &str) -> Result<Option<Material>, EvidenceFailure> {
    let root = legacy.parent().ok_or_else(|| failure(Cause::SealRootUnavailable, "SEAL-C installation root unavailable"))?;
    let observed = protection_observation(backend, &authority.identity, Some(&root.join(POLICY_HEAD)))?;
    let enrolled = observed.enrolled;
    policy_from_observation(observed)?;
    if enrolled {
        return operate(&legacy.with_file_name("capture-seal-keychain"), legacy, &authority.identity, authority.allow_first,
            backend, Operation::VerifyKey(id.into()), &mut || Err("verification never generates a key".into())).map(Some);
    }
    let mut paths = known_captures(root,current)?;
    if let Some(extra) = inventory { paths.extend_from_slice(extra); }
    local_veto(root, &paths, true)?;
    match backend.read(&authority.identity) {
        Err(BackendError::Missing) => Ok(None),
        Ok(_) => { remember(root); Err(failure(Cause::ProtectionInconsistent, "Protection appeared during legacy verification. Check again.")) },
        Err(error) => Err(backend_failure(error)),
    }
}
