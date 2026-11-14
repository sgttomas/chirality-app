//! Admission of a new signed-route seal. Absence is a fresh observation of
//! the selected namespace, not a statement about its history. Local evidence
//! can veto the file provider but can never authorize it.
use super::*;
use std::collections::BTreeSet;

static PROTECTED: std::sync::Mutex<BTreeSet<PathBuf>> = std::sync::Mutex::new(BTreeSet::new());
static LIBRARIES: std::sync::Mutex<std::collections::BTreeMap<PathBuf, BTreeSet<PathBuf>>> = std::sync::Mutex::new(std::collections::BTreeMap::new());
#[cfg(test)]
thread_local! {
    static TEST_PROTECTED: std::cell::RefCell<BTreeSet<PathBuf>> = const { std::cell::RefCell::new(BTreeSet::new()) };
}
pub(super) fn remember(root: &Path) {
    #[cfg(test)]
    { TEST_PROTECTED.with(|s| { s.borrow_mut().insert(root.to_owned()); }); return; }
    #[allow(unreachable_code)]
    PROTECTED.lock().unwrap_or_else(|p| p.into_inner()).insert(root.to_owned());
}
fn remembered(root: &Path) -> bool {
    #[cfg(test)]
    { return TEST_PROTECTED.with(|s| s.borrow().contains(root)); }
    #[allow(unreachable_code)]
    PROTECTED.lock().unwrap_or_else(|p| p.into_inner()).contains(root)
}
#[cfg(test)]
pub(super) fn forget(root: &Path) { TEST_PROTECTED.with(|s| { s.borrow_mut().remove(root); }); }

pub(super) fn register_library(root: &Path) {
    if let Ok(installation) = crate::capture_seal::installed_root_for_enrollment() {
        LIBRARIES.lock().unwrap_or_else(|p| p.into_inner()).entry(installation).or_default().insert(root.to_owned());
    }
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
    if let Some(libraries) = LIBRARIES.lock().unwrap_or_else(|p| p.into_inner()).get(installation) {
        result.extend(libraries.iter().map(|p| p.join(crate::storage::CAPTURES)));
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
    backend: &(impl Backend + ?Sized), inventory: Option<&[PathBuf]>, attach: impl FnOnce(Option<Material>) -> Result<R, EvidenceFailure>) -> Result<R, EvidenceFailure> {
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
        return attach(Some(material));
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
    attach(None)
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
