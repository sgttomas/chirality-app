//! SEAL-C storage transition only; not SEAL-2, entry sealing or person proof.
//! Compiled None prevents ALL real SecItem operations until reviewed signing activation.
use serde::{Deserialize, Serialize};
use sha2::{Digest, Sha256};
use std::{
    collections::BTreeMap,
    fs::{self, File, OpenOptions},
    io::{Read, Write},
    os::fd::AsRawFd,
    os::unix::fs::{DirBuilderExt, MetadataExt, OpenOptionsExt},
    path::{Path, PathBuf},
};
#[path = "capture_seal_keychain_macos.rs"]
mod macos;

/// Exact signing-stage choice. Never derive an access-group prefix from a team.
/// The signer must supply entitlement/profile compatibility separately.
struct Selection {
    bundle_identifier: &'static str,
    team_identifier: &'static str,
    service: &'static str,
    account: &'static str,
    access_group: &'static str,
    allow_first_enrollment: bool,
}
const KEYCHAIN_SELECTION: Option<Selection> = None;
#[derive(Clone, Debug, PartialEq, Eq)]
pub(super) struct ItemIdentity {
    pub service: String,
    pub account: String,
    pub access_group: String,
}
#[derive(Clone, Debug, PartialEq, Eq)]
pub(super) enum BackendError {
    Missing,
    Duplicate,
    Unavailable(i32),
    Invalid,
}
pub(super) trait Backend {
    fn read(&self, identity: &ItemIdentity) -> Result<Vec<u8>, BackendError>;
    fn add(&self, identity: &ItemIdentity, bytes: &[u8]) -> Result<(), BackendError>;
}
/// Constructed only after compiled selection, publisher and own installed checks.
/// A continuity marker cannot construct this or choose namespace/permissions.
pub(super) struct KeychainAuthority {
    identity: ItemIdentity,
    allow_first: bool,
    _installed: crate::installed_custody::InstalledCustody,
}
impl KeychainAuthority {
    fn admits(&self, item: &ItemIdentity) -> bool {
        item.service == self.identity.service
            && item.access_group == self.identity.access_group
            && (item.account == self.identity.account
                || item
                    .account
                    .strip_prefix(&format!("{}.rotation.", self.identity.account))
                    .is_some_and(|suffix| {
                        suffix.len() == 16
                            && suffix
                                .bytes()
                                .all(|b| b.is_ascii_digit() || (b'a'..=b'f').contains(&b))
                    }))
    }
    fn current() -> Result<Self, String> {
        let choice = KEYCHAIN_SELECTION
            .as_ref()
            .ok_or("SEAL-C keychain signing selection not admitted")?;
        let publisher =
            crate::publisher_selection::selected()?.ok_or("SEAL-C publisher not selected")?;
        if !publisher.matches_subject(choice.bundle_identifier, choice.team_identifier) {
            return Err("SEAL-C keychain publisher subject differs".into());
        }
        let executable = std::env::current_exe().map_err(|_| "SEAL-C own bundle unavailable")?;
        let resources = executable
            .parent()
            .and_then(Path::parent)
            .ok_or("SEAL-C own bundle unavailable")?
            .join("Resources");
        let installed = crate::installed_custody::observe(&resources)?;
        let identity = ItemIdentity {
            service: choice.service.into(),
            account: choice.account.into(),
            access_group: choice.access_group.into(),
        };
        validate_identity(&identity)?;
        Ok(Self {
            identity,
            allow_first: choice.allow_first_enrollment,
            _installed: installed,
        })
    }
}
pub(crate) struct Material {
    pub current: String,
    pub keys: BTreeMap<String, [u8; 32]>,
}
#[derive(Clone, Copy)]
pub(crate) enum Operation {
    Verify,
    Seal,
    Rotate,
    Enroll,
}
/// None means the unchanged unsigned/development file provider. A selected or
/// invalid publisher never falls back, even when keychain activation is absent.
#[cfg(test)]
thread_local! {static TEST_PROVIDER:std::cell::RefCell<Option<Box<dyn Fn(&Path,Operation)->Result<Material,String>>>>=const{std::cell::RefCell::new(None)};}
#[cfg(test)]
fn test_selected() -> bool {
    TEST_PROVIDER.with(|provider| provider.borrow().is_some())
}
pub(crate) fn dispatch(
    legacy_folder: &Path,
    operation: Operation,
) -> Option<Result<Material, String>> {
    #[cfg(test)]
    if let Some(result) = TEST_PROVIDER.with(|provider| {
        provider
            .borrow()
            .as_ref()
            .map(|p| p(legacy_folder, operation))
    }) {
        return Some(result);
    }
    match crate::publisher_selection::selected() {
        Ok(None) => None,
        Err(_) => Some(Err(
            "SEAL-C publisher validation unavailable; file fallback prohibited".into(),
        )),
        Ok(Some(_)) => Some((|| {
            let authority = KeychainAuthority::current()?;
            let backend = macos::NativeBackend::new(&authority);
            let directory = legacy_folder.with_file_name("capture-seal-keychain");
            let mut entropy = || {
                let mut key = [0u8; 32];
                getrandom::fill(&mut key)
                    .map_err(|_| "SEAL-C key entropy unavailable".to_owned())?;
                Ok(key)
            };
            operate(
                &directory,
                legacy_folder,
                &authority.identity,
                authority.allow_first,
                &backend,
                operation,
                &mut entropy,
            )
        })()),
    }
}
/// Host-only signing-stage enrollment entry. Not called by startup, seal, IPC or
/// any deserialized record. Actual activation/invocation needs the admitted stage.
pub(crate) fn enroll_initial(app_data: &Path) -> Result<(), String> {
    dispatch(
        &app_data.join(crate::capture_seal::KEY_FOLDER),
        Operation::Enroll,
    )
    .ok_or("SEAL-C keychain enrollment unavailable for unselected publisher")??;
    Ok(())
}
pub(crate) fn selected_route() -> bool {
    #[cfg(test)]
    if test_selected() {
        return true;
    }
    !matches!(crate::publisher_selection::selected(), Ok(None))
}
fn validate_identity(i: &ItemIdentity) -> Result<(), String> {
    if [&i.service, &i.account, &i.access_group].iter().any(|s| {
        s.is_empty()
            || s.len() > 255
            || !s
                .bytes()
                .all(|b| b.is_ascii_alphanumeric() || b".-_".contains(&b))
    }) {
        return Err("SEAL-C keychain namespace not an explicit supported identity".into());
    }
    Ok(())
}
fn digest(bytes: &[u8]) -> String {
    format!("{:x}", Sha256::digest(bytes))
}
fn scope(i: &ItemIdentity) -> String {
    digest(
        &serde_json::to_vec(&(
            &i.service,
            &i.account,
            &i.access_group,
            "data-protection/when-unlocked-device-only/non-sync/no-ui",
        ))
        .unwrap(),
    )
}
fn key_id(key: &[u8; 32]) -> String {
    crate::capture_seal::key_id(key)
}
#[derive(Clone, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
struct KeyRef {
    id: String,
    sha256: String,
}
#[derive(Clone, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
struct Marker {
    format: String,
    scope_sha256: String,
    keys: Vec<KeyRef>,
    pending: Option<KeyRef>,
}
const MARKER: &str = "continuity.s1.json";
fn keyref(key: &[u8; 32]) -> KeyRef {
    KeyRef {
        id: key_id(key),
        sha256: digest(key),
    }
}
fn item(i: &ItemIdentity, index: usize, key: &KeyRef) -> ItemIdentity {
    let mut item = i.clone();
    // The first item is a fixed namespace sentinel. Losing the marker can never
    // look like a fresh namespace while that first item remains present.
    if index > 0 {
        item.account = format!("{}.rotation.{}", i.account, key.id);
    }
    item
}
fn read_key(
    backend: &impl Backend,
    i: &ItemIdentity,
    index: usize,
    k: &KeyRef,
) -> Result<[u8; 32], String> {
    let raw = backend.read(&item(i, index, k)).map_err(|_| {
        "SEAL-C keychain item missing, locked, denied or unavailable; no replacement"
    })?;
    let key: [u8; 32] = raw
        .try_into()
        .map_err(|_| "SEAL-C keychain item malformed")?;
    if key_id(&key) != k.id || digest(&key) != k.sha256 {
        return Err("SEAL-C keychain item contradicts retained continuity".into());
    }
    Ok(key)
}
fn private_metadata(m: &fs::Metadata, directory: bool) -> bool {
    (if directory {
        m.is_dir()
    } else {
        m.is_file() && m.nlink() == 1
    }) && m.uid() == unsafe { libc::geteuid() }
        && m.mode() & 0o077 == 0
}
struct Guard(File, bool);
impl Drop for Guard {
    fn drop(&mut self) {
        unsafe {
            libc::flock(self.0.as_raw_fd(), libc::LOCK_UN);
        }
    }
}
fn guard(directory: &Path, create: bool) -> Result<Option<Guard>, String> {
    crate::storage::check_path(directory)?;
    let mut created = false;
    match fs::symlink_metadata(directory) {
        Err(e) if e.kind() == std::io::ErrorKind::NotFound => {
            if !create {
                return Ok(None);
            }
            fs::DirBuilder::new()
                .mode(0o700)
                .create(directory)
                .map_err(|_| "SEAL-C continuity directory creation unavailable")?;
            created = true;
            crate::storage::sync_dir(
                directory
                    .parent()
                    .ok_or("SEAL-C continuity parent absent")?,
            )?;
        }
        Err(_) => return Err("SEAL-C continuity directory unavailable".into()),
        Ok(_) => (),
    }
    if !private_metadata(
        &fs::symlink_metadata(directory).map_err(|_| "SEAL-C continuity directory unavailable")?,
        true,
    ) {
        return Err("SEAL-C continuity directory unsafe".into());
    }
    let lock = OpenOptions::new()
        .read(true)
        .write(true)
        .create(true)
        .truncate(false)
        .mode(0o600)
        .custom_flags(libc::O_NOFOLLOW | libc::O_NONBLOCK)
        .open(directory.join(".continuity.lock"))
        .map_err(|_| "SEAL-C continuity lock unavailable")?;
    if !private_metadata(
        &lock
            .metadata()
            .map_err(|_| "SEAL-C continuity lock unavailable")?,
        false,
    ) {
        return Err("SEAL-C continuity lock unsafe".into());
    }
    if unsafe { libc::flock(lock.as_raw_fd(), libc::LOCK_EX | libc::LOCK_NB) } != 0 {
        return Err("SEAL-C continuity busy; retry without key mutation".into());
    }
    Ok(Some(Guard(lock, created)))
}
fn load(directory: &Path, i: &ItemIdentity) -> Result<Option<Marker>, String> {
    let mut file = match OpenOptions::new()
        .read(true)
        .custom_flags(libc::O_NOFOLLOW | libc::O_NONBLOCK)
        .open(directory.join(MARKER))
    {
        Ok(f) => f,
        Err(e) if e.kind() == std::io::ErrorKind::NotFound => return Ok(None),
        Err(_) => return Err("SEAL-C continuity marker unavailable".into()),
    };
    if !private_metadata(
        &file
            .metadata()
            .map_err(|_| "SEAL-C continuity marker unavailable")?,
        false,
    ) {
        return Err("SEAL-C continuity marker unsafe".into());
    }
    let mut bytes = Vec::new();
    (&mut file)
        .take(65537)
        .read_to_end(&mut bytes)
        .map_err(|_| "SEAL-C continuity marker unreadable")?;
    if bytes.len() > 65536 {
        return Err("SEAL-C continuity marker oversized".into());
    }
    let m: Marker =
        serde_json::from_slice(&bytes).map_err(|_| "SEAL-C continuity marker malformed")?;
    if m.format != "capture-seal-keychain-continuity.s1"
        || m.scope_sha256 != scope(i)
        || m.keys.len() > 128
        || m.keys.is_empty() && m.pending.is_none()
    {
        return Err("SEAL-C continuity scope or state differs".into());
    }
    let mut ids = std::collections::BTreeSet::new();
    for k in m.keys.iter().chain(m.pending.iter()) {
        if k.id.len() != 16
            || k.sha256.len() != 64
            || !k
                .id
                .bytes()
                .chain(k.sha256.bytes())
                .all(|b| b.is_ascii_digit() || (b'a'..=b'f').contains(&b))
            || !ids.insert(&k.id)
        {
            return Err("SEAL-C continuity key identity invalid".into());
        }
    }
    Ok(Some(m))
}
fn publish(directory: &Path, m: &Marker) -> Result<(), String> {
    let raw = serde_json::to_vec(m).map_err(|_| "SEAL-C continuity encoding failed")?;
    let temp = directory.join(format!(".continuity-{}.tmp", crate::util::opaque_id("")?));
    let mut file = OpenOptions::new()
        .write(true)
        .create_new(true)
        .mode(0o600)
        .custom_flags(libc::O_NOFOLLOW)
        .open(&temp)
        .map_err(|_| "SEAL-C continuity publication unavailable")?;
    file.write_all(&raw)
        .and_then(|_| file.sync_all())
        .map_err(|_| "SEAL-C continuity write uncertain; no key operation")?;
    fs::rename(&temp, directory.join(MARKER))
        .map_err(|_| "SEAL-C continuity publication uncertain; no key operation")?;
    crate::storage::sync_dir(directory)
        .map_err(|_| "SEAL-C continuity durability uncertain; no key operation".into())
}
fn material(backend: &impl Backend, i: &ItemIdentity, m: &Marker) -> Result<Material, String> {
    let mut keys = BTreeMap::new();
    for (index, k) in m.keys.iter().enumerate() {
        keys.insert(k.id.clone(), read_key(backend, i, index, k)?);
    }
    Ok(Material {
        current: m.keys.last().ok_or("SEAL-C no committed key")?.id.clone(),
        keys,
    })
}
/// Marker is continuity evidence within a compiled namespace, never namespace
/// authority. No read failure causes creation. Pending+missing stays blocked.
fn operate(
    directory: &Path,
    legacy_folder: &Path,
    i: &ItemIdentity,
    allow_first: bool,
    backend: &impl Backend,
    operation: Operation,
    entropy: &mut impl FnMut() -> Result<[u8; 32], String>,
) -> Result<Material, String> {
    validate_identity(i)?;
    let _lock = guard(
        directory,
        matches!(operation, Operation::Enroll) && allow_first,
    )?
    .ok_or("SEAL-C keychain continuity not enrolled; not verified here")?;
    let mut m = match load(directory, i)? {
        Some(m) => m,
        None => {
            if !_lock.1 {
                return Err(
                    "SEAL-C continuity marker absent in existing namespace; no regeneration".into(),
                );
            }
            if !matches!(operation, Operation::Enroll) || !allow_first {
                return Err("SEAL-C explicit first enrollment not admitted".into());
            }
            match fs::symlink_metadata(legacy_folder) {
                Err(error) if error.kind() == std::io::ErrorKind::NotFound => (),
                Err(_) => {
                    return Err(
                        "SEAL-C legacy namespace presence unavailable; enrollment refused".into(),
                    )
                }
                Ok(_) => return Err(
                    "SEAL-C existing file-key namespace retained; implicit migration prohibited"
                        .into(),
                ),
            }
            // Fixed primary account survives marker loss and blocks regeneration.
            match backend.read(i) {
                Err(BackendError::Missing) => (),
                _ => return Err("SEAL-C namespace not demonstrably new; enrollment refused".into()),
            }
            Marker {
                format: "capture-seal-keychain-continuity.s1".into(),
                scope_sha256: scope(i),
                keys: vec![],
                pending: None,
            }
        }
    };
    if let Some(pending) = m.pending.clone() {
        // Preserve an incomplete rotation if any earlier retained item is lost;
        // do not advance the committed current-key marker on partial continuity.
        for (index, retained) in m.keys.iter().enumerate() {
            read_key(backend, i, index, retained)?;
        }
        // Readback proves actual bytes after a crash/unknown add outcome. A
        // missing item NEVER retries add or silently creates replacement bytes.
        read_key(backend, i, m.keys.len(), &pending)?;
        if matches!(operation, Operation::Verify) {
            return Err("SEAL-C enrollment/rotation pending explicit write-path recovery; not verified here".into());
        }
        m.keys.push(pending);
        m.pending = None;
        publish(directory, &m)?;
        return material(backend, i, &m);
    }
    if !m.keys.is_empty() {
        let existing = material(backend, i, &m)?;
        if !matches!(operation, Operation::Rotate) {
            return Ok(existing);
        }
    }
    if m.keys.len() >= 128 {
        return Err("SEAL-C retained key limit; explicit continuity disposition required".into());
    }
    let key = entropy()?;
    let reference = keyref(&key);
    if m.keys.iter().any(|k| k.id == reference.id) {
        return Err("SEAL-C key identity collision; no add".into());
    }
    m.pending = Some(reference.clone());
    publish(directory, &m)?;
    // Reservation is durable before add. No rollback/delete/retry after error.
    backend
        .add(&item(i, m.keys.len(), &reference), &key)
        .map_err(|_| "SEAL-C keychain add failed or outcome unknown; reservation retained")?;
    let observed = read_key(backend, i, m.keys.len(), &reference)?;
    if observed != key {
        return Err("SEAL-C keychain add readback differs; reservation retained".into());
    }
    m.keys.push(reference);
    m.pending = None;
    publish(directory, &m)?;
    material(backend, i, &m)
}

#[cfg(test)]
#[path = "capture_seal_keychain_tests.rs"]
mod tests;
