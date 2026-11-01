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
/// Menu eligibility only: no namespace, signature, root or keychain observation.
/// Actual preparation/consumption independently validate authority and policy.
pub(crate) const fn enrollment_compiled_available() -> bool {
    cfg!(target_os = "macos") && !cfg!(debug_assertions) && KEYCHAIN_SELECTION.is_some()
}

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
    publisher_subject: serde_json::Value,
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
            publisher_subject: serde_json::json!({"publisher":crate::publisher_selection::identity(),
                "bundle_identifier":choice.bundle_identifier,"team_identifier":choice.team_identifier}),
            _installed: installed,
        })
    }
}
pub(crate) struct Material {
    pub current: String,
    pub keys: BTreeMap<String, [u8; 32]>,
}
#[derive(Clone)]
pub(crate) enum Operation {
    Verify,
    VerifyKey(String),
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
    if matches!(operation, Operation::Enroll) {
        return Some(Err(
            "SEAL-C enrollment requires the original prepared intent".into(),
        ));
    }
    #[cfg(test)]
    if let Some(result) = TEST_PROVIDER.with(|provider| {
        provider
            .borrow()
            .as_ref()
            .map(|p| p(legacy_folder, operation.clone()))
    }) {
        return Some(result);
    }
    match publisher_route() {
        Ok(false) => None,
        Err(_) => Some(Err(
            "SEAL-C publisher validation unavailable; file fallback prohibited".into(),
        )),
        Ok(true) => Some((|| {
            let authority =
                process_authority(matches!(operation, Operation::Enroll | Operation::Rotate))?;
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
/// Read-only provider preparation. No SecItem, marker write or advisory lock.
/// A future native caller still owns original-window/confirmation/key_setup/Quit.
pub(crate) fn prepare_enrollment() -> Result<PreparedSealEnrollment, String> {
    let authority = process_authority(false)?;
    prepare_installed_subject(&authority)
}
fn prepare_installed_subject(
    authority: &KeychainAuthority,
) -> Result<PreparedSealEnrollment, String> {
    let root = crate::capture_seal::installed_root_for_enrollment()?;
    prepare_subject(&root, authority)
}
/// Consumes the original intent once. No path-only production enrollment entry.
/// No menu/IPC/startup caller is registered by this source slice.
pub(crate) fn enroll_initial(prepared: PreparedSealEnrollment) -> Result<(), String> {
    let authority = process_authority(true)?;
    let backend = macos::NativeBackend::new(&authority);
    consume_prepared(prepared, &authority, &backend, &mut || {
        let mut key = [0u8; 32];
        getrandom::fill(&mut key).map_err(|_| "SEAL-C key entropy unavailable".to_owned())?;
        Ok(key)
    })?;
    Ok(())
}
pub(crate) fn selected_route() -> bool {
    #[cfg(test)]
    if test_selected() {
        return true;
    }
    !matches!(publisher_route(), Ok(false))
}
// The publisher selection is immutable compiler input. Cache its decision, not
// key availability. A denied/locked item is still observed on every verification.
fn publisher_route() -> Result<bool, ()> {
    static ROUTE: std::sync::OnceLock<Result<bool, ()>> = std::sync::OnceLock::new();
    *ROUTE.get_or_init(|| {
        crate::publisher_selection::selected()
            .map(|p| p.is_some())
            .map_err(|_| ())
    })
}
fn process_authority(recheck: bool) -> Result<std::sync::Arc<KeychainAuthority>, String> {
    static AUTHORITY: std::sync::Mutex<Option<std::sync::Arc<KeychainAuthority>>> =
        std::sync::Mutex::new(None);
    cached_authority(&AUTHORITY, recheck, KeychainAuthority::current)
}
fn cached_authority(
    state: &std::sync::Mutex<Option<std::sync::Arc<KeychainAuthority>>>,
    recheck: bool,
    create: impl FnOnce() -> Result<KeychainAuthority, String>,
) -> Result<std::sync::Arc<KeychainAuthority>, String> {
    let mut held = state
        .lock()
        .map_err(|_| "SEAL-C authority initialization unavailable")?;
    if recheck {
        *held = None;
    }
    if held.is_none() {
        // Refresh failure revokes the cached capability; it cannot resurrect on
        // the next normal capture. Item bytes/availability are never cached here.
        *held = Some(std::sync::Arc::new(create()?));
    }
    Ok(held.as_ref().unwrap().clone())
}

fn verifying(operation: &Operation) -> bool {
    matches!(operation, Operation::Verify | Operation::VerifyKey(_))
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
    #[serde(deserialize_with = "required_pending")]
    pending: Option<KeyRef>,
}
fn required_pending<'de, D: serde::Deserializer<'de>>(
    deserializer: D,
) -> Result<Option<KeyRef>, D::Error> {
    Option::<KeyRef>::deserialize(deserializer)
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
#[derive(Debug, PartialEq, Eq)]
struct DirectoryStamp(u64, u64, u32, u32);
impl DirectoryStamp {
    fn of(m: &fs::Metadata) -> Self {
        Self(m.dev(), m.ino(), m.uid(), m.mode())
    }
}
struct HeldDirectory {
    path: PathBuf,
    file: File,
    stamp: DirectoryStamp,
}
impl HeldDirectory {
    fn open(path: &Path) -> Result<Self, String> {
        let file = OpenOptions::new()
            .read(true)
            .custom_flags(libc::O_DIRECTORY | libc::O_NOFOLLOW)
            .open(path)
            .map_err(|_| "SEAL-C prepared directory unavailable or aliased")?;
        let metadata = file
            .metadata()
            .map_err(|_| "SEAL-C prepared directory metadata unavailable")?;
        if !metadata.is_dir() {
            return Err("SEAL-C prepared source is not a directory".into());
        }
        let held = Self {
            path: path.to_owned(),
            stamp: DirectoryStamp::of(&metadata),
            file,
        };
        held.recheck()?;
        Ok(held)
    }
    fn recheck(&self) -> Result<(), String> {
        let opened = self
            .file
            .metadata()
            .map_err(|_| "SEAL-C held directory unavailable")?;
        let named = fs::symlink_metadata(&self.path)
            .map_err(|_| "SEAL-C prepared directory disappeared")?;
        if !named.is_dir()
            || DirectoryStamp::of(&opened) != self.stamp
            || DirectoryStamp::of(&named) != self.stamp
        {
            return Err("SEAL-C prepared directory identity or permissions changed".into());
        }
        Ok(())
    }
}
#[derive(Debug, PartialEq, Eq)]
struct FileStamp(u64, u64, u64, u32, u32, i64, i64, i64, i64);
impl FileStamp {
    fn of(m: &fs::Metadata) -> Self {
        Self(
            m.dev(),
            m.ino(),
            m.len(),
            m.uid(),
            m.mode(),
            m.mtime(),
            m.mtime_nsec(),
            m.ctime(),
            m.ctime_nsec(),
        )
    }
}
struct MarkerSnapshot {
    stamp: FileStamp,
    sha256: String,
    _held: File,
}
impl PartialEq for MarkerSnapshot {
    fn eq(&self, other: &Self) -> bool {
        self.stamp == other.stamp && self.sha256 == other.sha256
    }
}
#[derive(Clone, PartialEq, Eq)]
struct EnrollmentPolicy {
    identity: ItemIdentity,
    allow_first: bool,
    publisher_subject: serde_json::Value,
}
impl KeychainAuthority {
    fn enrollment_policy(&self) -> EnrollmentPolicy {
        EnrollmentPolicy {
            identity: self.identity.clone(),
            allow_first: self.allow_first,
            publisher_subject: self.publisher_subject.clone(),
        }
    }
}

/// Provider-owned intent: no Clone, Deserialize, fields or public constructor.
/// Directory/file descriptors pin observed objects, but no advisory lock is kept
/// across confirmation. Dropping the intent cancels without backend or writes.
pub(crate) struct PreparedSealEnrollment {
    attempt: String,
    app_data: PathBuf,
    ancestors: Vec<HeldDirectory>,
    namespace: Option<HeldDirectory>,
    marker: Option<MarkerSnapshot>,
    marker_summary: serde_json::Value,
    policy: EnrollmentPolicy,
}
impl PreparedSealEnrollment {
    pub(crate) fn preview(&self) -> serde_json::Value {
        serde_json::json!({"attempt":self.attempt,"operation":"prepare-or-complete-capture-sealing",
            "app_data":self.app_data,"service":self.policy.identity.service,"account":self.policy.identity.account,
            "access_group":self.policy.identity.access_group,"allow_first_enrollment":self.policy.allow_first,
            "publisher_subject":self.policy.publisher_subject,"continuity_directory_present":self.namespace.is_some(),
            "marker_sha256":self.marker.as_ref().map(|m|&m.sha256),"marker":self.marker_summary,
            "legacy_directory_observed_absent":true,"limit":"Frozen read-only provider subject; not native confirmation or permission. Keychain presence remains unobserved."})
    }
    fn directory(&self) -> PathBuf {
        self.app_data.join("capture-seal-keychain")
    }
    fn legacy(&self) -> PathBuf {
        self.app_data.join(crate::capture_seal::KEY_FOLDER)
    }
    fn recheck_root_and_legacy(&self) -> Result<(), String> {
        for held in &self.ancestors {
            held.recheck()?;
        }
        legacy_absent(&self.legacy())
    }
    fn before_namespace(&self) -> Result<(), String> {
        self.recheck_root_and_legacy()?;
        match &self.namespace {
            Some(directory) => directory.recheck(),
            None => match fs::symlink_metadata(self.directory()) {
                Err(e) if e.kind() == std::io::ErrorKind::NotFound => Ok(()),
                _ => Err("SEAL-C prepared absent continuity directory changed".into()),
            },
        }
    }
    fn after_continuity(
        &self,
        guard: &Guard,
        marker: Option<&MarkerSnapshot>,
    ) -> Result<(), String> {
        self.recheck_root_and_legacy()?;
        let held = guard
            .directory
            .as_ref()
            .ok_or("SEAL-C continuity directory not held")?;
        held.recheck()?;
        if held.path != self.directory()
            || self
                .namespace
                .as_ref()
                .is_some_and(|old| old.stamp != held.stamp)
        {
            return Err("SEAL-C prepared continuity directory changed under lock".into());
        }
        if self.marker.as_ref() != marker {
            return Err("SEAL-C prepared marker bytes or identity changed".into());
        }
        Ok(())
    }
}
fn legacy_absent(path: &Path) -> Result<(), String> {
    match fs::symlink_metadata(path) {
        Err(e) if e.kind() == std::io::ErrorKind::NotFound => Ok(()),
        _ => Err("SEAL-C prepared enrollment requires observed legacy namespace absence".into()),
    }
}
fn prepare_subject(
    app_data: &Path,
    authority: &KeychainAuthority,
) -> Result<PreparedSealEnrollment, String> {
    if !app_data.is_absolute()
        || app_data
            .components()
            .any(|c| matches!(c, std::path::Component::ParentDir))
    {
        return Err("SEAL-C prepared AppData must be an absolute physical directory".into());
    }
    crate::storage::check_path(app_data)?;
    let ancestors = app_data
        .ancestors()
        .map(HeldDirectory::open)
        .collect::<Result<Vec<_>, _>>()?;
    let own = ancestors[0]
        .file
        .metadata()
        .map_err(|_| "SEAL-C AppData metadata unavailable")?;
    if own.uid() != unsafe { libc::geteuid() } || own.mode() & 0o022 != 0 {
        return Err("SEAL-C AppData ownership or writability unsafe".into());
    }
    let directory = app_data.join("capture-seal-keychain");
    let namespace = match fs::symlink_metadata(&directory) {
        Err(e) if e.kind() == std::io::ErrorKind::NotFound => None,
        Err(_) => return Err("SEAL-C continuity state unavailable".into()),
        Ok(m) => {
            if !private_metadata(&m, true) {
                return Err("SEAL-C continuity source unsafe".into());
            }
            Some(HeldDirectory::open(&directory)?)
        }
    };
    let observed = load_snapshot(&directory, &authority.identity)?;
    let summary=observed.as_ref().map(|(m,_)|serde_json::json!({"committed_key_ids":m.keys.iter().map(|k|&k.id).collect::<Vec<_>>(),"pending_key_id":m.pending.as_ref().map(|k|&k.id)})).unwrap_or(serde_json::Value::Null);
    let intent = PreparedSealEnrollment {
        attempt: crate::util::opaque_id("seal-enrollment-")?,
        app_data: app_data.to_owned(),
        ancestors,
        namespace,
        marker: observed.map(|(_, s)| s),
        marker_summary: summary,
        policy: authority.enrollment_policy(),
    };
    intent.before_namespace()?;
    Ok(intent)
}
fn consume_prepared(
    prepared: PreparedSealEnrollment,
    authority: &KeychainAuthority,
    backend: &impl Backend,
    entropy: &mut impl FnMut() -> Result<[u8; 32], String>,
) -> Result<Material, String> {
    // Refresh is performed by enroll_initial before this comparison and before
    // any provider locks. Never silently replace the original frozen policy.
    if crate::capture_seal::installed_root_for_enrollment()? != prepared.app_data {
        return Err("SEAL-C installed enrollment root changed after preparation".into());
    }
    if prepared.policy != authority.enrollment_policy() {
        return Err("SEAL-C refreshed authority differs from prepared policy".into());
    }
    // Precheck prevents stale path work even before lock-file creation. The
    // authoritative joins are repeated at the two in-lock effect boundaries.
    prepared.before_namespace()?;
    operate_bound(
        &prepared.directory(),
        &prepared.legacy(),
        &authority.identity,
        authority.allow_first,
        backend,
        Operation::Enroll,
        entropy,
        Some(&prepared),
    )
}

struct Guard {
    file: File,
    directory: Option<HeldDirectory>,
}
impl Drop for Guard {
    fn drop(&mut self) {
        unsafe {
            libc::flock(self.file.as_raw_fd(), libc::LOCK_UN);
        }
    }
}
#[cfg(test)]
fn guard(directory: &Path, create: bool) -> Result<Option<Guard>, String> {
    guard_mode(directory, create, false, false)
}
fn guard_mode(
    directory: &Path,
    create: bool,
    shared: bool,
    wait: bool,
) -> Result<Option<Guard>, String> {
    crate::storage::check_path(directory)?;
    match fs::symlink_metadata(directory) {
        Err(e) if e.kind() == std::io::ErrorKind::NotFound => {
            if !create {
                return Ok(None);
            }
            fs::DirBuilder::new()
                .mode(0o700)
                .create(directory)
                .map_err(|_| "SEAL-C continuity directory creation unavailable")?;
            crate::storage::sync_dir(
                directory
                    .parent()
                    .ok_or("SEAL-C continuity parent absent")?,
            )?;
        }
        Err(_) => return Err("SEAL-C continuity directory unavailable".into()),
        Ok(_) if create => {
            return Err("SEAL-C expected absent continuity directory appeared".into())
        }
        Ok(_) => (),
    }
    let held_directory = HeldDirectory::open(directory)?;
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
    let flags =
        (if shared { libc::LOCK_SH } else { libc::LOCK_EX }) | if wait { 0 } else { libc::LOCK_NB };
    if unsafe { libc::flock(lock.as_raw_fd(), flags) } != 0 {
        return Err("SEAL-C continuity busy; retry without key mutation".into());
    }
    held_directory.recheck()?;
    Ok(Some(Guard {
        file: lock,
        directory: Some(held_directory),
    }))
}
fn load(directory: &Path, i: &ItemIdentity) -> Result<Option<Marker>, String> {
    Ok(load_snapshot(directory, i)?.map(|(marker, _)| marker))
}
fn load_snapshot(
    directory: &Path,
    i: &ItemIdentity,
) -> Result<Option<(Marker, MarkerSnapshot)>, String> {
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
    let before = FileStamp::of(
        &file
            .metadata()
            .map_err(|_| "SEAL-C marker metadata unavailable")?,
    );
    let mut bytes = Vec::new();
    (&mut file)
        .take(65537)
        .read_to_end(&mut bytes)
        .map_err(|_| "SEAL-C continuity marker unreadable")?;
    if bytes.len() > 65536 {
        return Err("SEAL-C continuity marker oversized".into());
    }
    let after = FileStamp::of(
        &file
            .metadata()
            .map_err(|_| "SEAL-C marker metadata unavailable")?,
    );
    let named = FileStamp::of(
        &fs::symlink_metadata(directory.join(MARKER))
            .map_err(|_| "SEAL-C marker changed during read")?,
    );
    if before != after || after != named {
        return Err("SEAL-C marker changed during read".into());
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
    Ok(Some((
        m,
        MarkerSnapshot {
            stamp: after,
            sha256: digest(&bytes),
            _held: file,
        },
    )))
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
fn fresh_namespace(
    legacy_folder: &Path,
    i: &ItemIdentity,
    backend: &impl Backend,
) -> Result<(), String> {
    match fs::symlink_metadata(legacy_folder) {
        Err(e) if e.kind() == std::io::ErrorKind::NotFound => (),
        Err(_) => {
            return Err("SEAL-C legacy namespace presence unavailable; enrollment refused".into())
        }
        Ok(_) => {
            return Err(
                "SEAL-C existing file-key namespace retained; implicit migration prohibited".into(),
            )
        }
    }
    match backend.read(i) {
        Err(BackendError::Missing) => Ok(()),
        _ => Err("SEAL-C namespace not demonstrably new; enrollment refused".into()),
    }
}
fn verification_material(
    backend: &impl Backend,
    i: &ItemIdentity,
    m: &Marker,
    operation: &Operation,
) -> Result<Material, String> {
    let mut keys = BTreeMap::new();
    let current = m
        .keys
        .last()
        .ok_or("SEAL-C no committed key; enrollment pending")?
        .id
        .clone();
    for (index, k) in m.keys.iter().enumerate() {
        if let Operation::VerifyKey(wanted) = operation {
            if wanted != &k.id {
                continue;
            }
        }
        keys.insert(k.id.clone(), read_key(backend, i, index, k)?);
    }
    Ok(Material { current, keys })
}
#[cfg(test)]
thread_local! {static BEFORE_GUARD:std::cell::RefCell<Option<Box<dyn FnOnce()>>>=const{std::cell::RefCell::new(None)};}
#[cfg(test)]
thread_local! {static BEFORE_ENROLLMENT_JOIN:std::cell::RefCell<Option<Box<dyn FnOnce()>>>=const{std::cell::RefCell::new(None)};}
#[cfg(test)]
thread_local! {static AFTER_ENROLLMENT_JOIN:std::cell::RefCell<Option<Box<dyn FnOnce()>>>=const{std::cell::RefCell::new(None)};}
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
    operate_bound(
        directory,
        legacy_folder,
        i,
        allow_first,
        backend,
        operation,
        entropy,
        None,
    )
}
fn operate_bound(
    directory: &Path,
    legacy_folder: &Path,
    i: &ItemIdentity,
    allow_first: bool,
    backend: &impl Backend,
    operation: Operation,
    entropy: &mut impl FnMut() -> Result<[u8; 32], String>,
    prepared: Option<&PreparedSealEnrollment>,
) -> Result<Material, String> {
    #[cfg(not(test))]
    if matches!(operation, Operation::Enroll) && prepared.is_none() {
        return Err("SEAL-C prepared enrollment intent required".into());
    }
    validate_identity(i)?;
    // First-enrollment admission is serialized outside the not-yet-created
    // continuity directory. A transient keychain refusal leaves no empty
    // enrollment directory that could masquerade as a crashed reservation.
    let _enrollment = if matches!(operation, Operation::Enroll) {
        let parent = directory
            .parent()
            .ok_or("SEAL-C continuity parent absent")?;
        crate::storage::check_path(parent)?;
        let file = OpenOptions::new()
            .read(true)
            .write(true)
            .create(true)
            .truncate(false)
            .mode(0o600)
            .custom_flags(libc::O_NOFOLLOW | libc::O_NONBLOCK)
            .open(parent.join(".seal-c-enrollment.lock"))
            .map_err(|_| "SEAL-C enrollment lock unavailable")?;
        if !private_metadata(
            &file
                .metadata()
                .map_err(|_| "SEAL-C enrollment lock unavailable")?,
            false,
        ) {
            return Err("SEAL-C enrollment lock unsafe".into());
        }
        if unsafe { libc::flock(file.as_raw_fd(), libc::LOCK_EX) } != 0 {
            return Err("SEAL-C enrollment lock unavailable".into());
        }
        Some(Guard {
            file,
            directory: None,
        })
    } else {
        None
    };
    #[cfg(test)]
    BEFORE_ENROLLMENT_JOIN.with(|hook| {
        if let Some(hook) = hook.borrow_mut().take() {
            hook();
        }
    });
    if let Some(intent) = prepared {
        intent.before_namespace()?;
    }
    #[cfg(test)]
    AFTER_ENROLLMENT_JOIN.with(|hook| {
        if let Some(hook) = hook.borrow_mut().take() {
            hook();
        }
    });
    let observed_absent = !directory
        .try_exists()
        .map_err(|_| "SEAL-C continuity presence unavailable")?;
    if prepared.is_some_and(|intent| observed_absent != intent.namespace.is_none()) {
        return Err("SEAL-C prepared presence or absence changed after enrollment join".into());
    }
    let admitted_create = matches!(operation, Operation::Enroll) && allow_first && observed_absent;
    if matches!(operation, Operation::Enroll) && observed_absent {
        if !allow_first {
            return Err("SEAL-C explicit first enrollment not admitted".into());
        }
        fresh_namespace(legacy_folder, i, backend)?;
    }
    #[cfg(test)]
    BEFORE_GUARD.with(|hook| {
        if let Some(hook) = hook.borrow_mut().take() {
            hook();
        }
    });
    let _lock = guard_mode(
        directory,
        admitted_create,
        verifying(&operation),
        !verifying(&operation),
    )?
    .ok_or("SEAL-C keychain continuity not enrolled; not verified here")?;
    let snapshot = load_snapshot(directory, i)?;
    if let Some(intent) = prepared {
        intent.after_continuity(&_lock, snapshot.as_ref().map(|(_, stamp)| stamp))?;
    }
    let mut m = match snapshot {
        Some((m, _)) => m,
        None => {
            if !matches!(operation, Operation::Enroll) || !allow_first {
                return Err(
                    "SEAL-C explicit first enrollment not admitted; no regeneration".into(),
                );
            }
            // An explicit enrollment may resume an unreserved empty directory
            // after entropy/disk failure, but must re-establish absence while
            // holding BOTH locks. Normal seal/verify/rotate cannot take this path.
            fresh_namespace(legacy_folder, i, backend)?;
            Marker {
                format: "capture-seal-keychain-continuity.s1".into(),
                scope_sha256: scope(i),
                keys: vec![],
                pending: None,
            }
        }
    };
    if verifying(&operation) {
        // A pending item has never sealed a capture. Historical committed keys
        // remain verifiable without reading or committing that pending item.
        return verification_material(backend, i, &m, &operation);
    }
    if matches!(operation, Operation::Seal) {
        // Pending rotation never sealed a capture. New captures continue under
        // the committed current key, without reading/committing pending or old
        // rotated items. Initial pending-only enrollment remains unavailable.
        let current = m
            .keys
            .last()
            .ok_or("SEAL-C no committed key; explicit enrollment recovery required")?
            .id
            .clone();
        return verification_material(backend, i, &m, &Operation::VerifyKey(current));
    }
    if let Some(pending) = m.pending.clone() {
        // Preserve an incomplete rotation if any earlier retained item is lost;
        // do not advance the committed current-key marker on partial continuity.
        for (index, retained) in m.keys.iter().enumerate() {
            read_key(backend, i, index, retained)?;
        }
        // Readback proves actual bytes after a crash/unknown add outcome. A
        // missing item NEVER retries add or silently creates replacement bytes.
        read_key(backend, i, m.keys.len(), &pending)?;
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
