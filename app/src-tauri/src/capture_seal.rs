//! Host-held capture seal (DEL-01-04 AAC §6.3 SEAL-C, selected 2026-10-11 for
//! AAC §6.3 / EXEC §2.4–2.5 review finding R-1).
//!
//! The Rust act control seals each App-file act or decline capture it writes
//! with HMAC-SHA-256 under a per-installation key kept in the App data folder,
//! outside every project. The checkpoint counter and the file-act view count a
//! capture only when its seal verifies under a key this installation holds.
//! A capture without a seal, with an unknown method, sealed under a key this
//! installation does not hold, or whose seal does not verify is refused with a
//! stated limit; it is never called forged, only "not verified here".
//!
//! The seal covers the capture's original act facts: every member except
//! `seal` itself and the add-once `recordId` backlink (AAC §5.2a), so adding
//! the backlink needs no reseal and recovery's comparisons are unchanged.
//!
//! The separately gated signing-stage keychain provider preserves this seal
//! format. It never imports or falls back to file keys for a selected publisher.
//! Default unsigned/development installations retain the file provider below.
//!
//! What the file provider does not do (stated, not hidden): anything that can read the key
//! file can seal. That includes any process running as the same OS user, and a
//! Codex agent whose sandbox lets it read the App data folder (Codex's default
//! read policy does). It shows that a capture was sealed by a holder of this
//! installation's key, not that a person acted or who the person is (K1-4).
use serde_json::{json, Value};
use crate::act_evidence_cause::{ActEvidenceCause as Cause, EvidenceFailure};
fn failure(cause: Cause, detail: impl Into<String>) -> EvidenceFailure { EvidenceFailure::new(cause, detail) }
use sha2::{Digest, Sha256};
use std::{
    collections::BTreeMap,
    io::Write,
    os::unix::fs::{MetadataExt, OpenOptionsExt, PermissionsExt},
    path::{Path, PathBuf},
    sync::Mutex,
};

/// The seal's method designation (capture schema `seal.method`).
pub const SEAL_METHOD: &str = "chirality.app.capture-seal.hmac-sha256/v1";
const DOMAIN: &[u8] = b"chirality.app.capture-seal/v1\0";
const KEY_ID_DOMAIN: &[u8] = b"chirality.app.capture-seal.key-id/v1\0";
const KEYRING_FORMAT: &str = "chirality.app.capture-seal-keys";
const KEY_FILE: &str = "keys.json";
/// The key folder under the App data folder.
pub const KEY_FOLDER: &str = "capture-seal";

/// Authenticated storage-provider claim; key IDs identify bytes, not custody.
#[derive(Clone, Copy, Debug, PartialEq, Eq, serde::Serialize, serde::Deserialize)]
pub enum SealProvider {
    #[serde(rename = "file-key")]
    FileKey,
    #[serde(rename = "keychain")]
    Keychain,
}
impl SealProvider {
    pub fn name(self) -> &'static str { match self { Self::FileKey => "file-key", Self::Keychain => "keychain" } }
    pub fn sentence(self) -> &'static str { match self {
        Self::FileKey => "Sealed with the key file, which a process on this account could forge.",
        Self::Keychain => "Sealed with the keychain key.",
    } }
}
#[derive(Clone, Debug, PartialEq, Eq)]
pub struct SealVerification {
    pub recorded_provider: Option<SealProvider>,
    pub verified_with: SealProvider,
    pub key_id: String,
}
impl SealVerification {
    pub fn sentence(&self) -> String {
        match self.recorded_provider {
            Some(provider) => provider.sentence().into(),
            None => format!("Seal verified; provider not recorded. Verified here using {}. {}", self.verified_with.name(), self.verified_with.sentence()),
        }
    }
    pub fn view(&self) -> Value {
        json!({"status":"verified","recordedProvider":self.recorded_provider,"verifiedWith":self.verified_with,"standing":self.sentence()})
    }
}
fn file_material(ring: Keyring) -> crate::capture_seal_keychain::Material {
    crate::capture_seal_keychain::Material { current: ring.current, keys: ring.keys, provider: SealProvider::FileKey }
}

/// HMAC-SHA-256 (RFC 2104) over `message` with a key of at most one block.
fn hmac(key: &[u8], message: &[u8]) -> [u8; 32] {
    assert!(key.len() <= 64, "capture-seal keys are one block or less");
    let mut inner = [0x36u8; 64];
    let mut outer = [0x5cu8; 64];
    for (i, k) in key.iter().enumerate() {
        inner[i] ^= k;
        outer[i] ^= k;
    }
    let digest = Sha256::new().chain_update(inner).chain_update(message).finalize();
    Sha256::new().chain_update(outer).chain_update(digest).finalize().into()
}
fn hex(bytes: &[u8]) -> String {
    bytes.iter().map(|b| format!("{b:02x}")).collect()
}
fn unhex(text: &str) -> Option<Vec<u8>> {
    if text.len() % 2 != 0 || !text.bytes().all(|b| b.is_ascii_hexdigit() && !b.is_ascii_uppercase()) {
        return None;
    }
    (0..text.len()).step_by(2).map(|i| u8::from_str_radix(&text[i..i + 2], 16).ok()).collect()
}
fn equal(a: &[u8], b: &[u8]) -> bool {
    a.len() == b.len() && a.iter().zip(b).fold(0u8, |acc, (x, y)| acc | (x ^ y)) == 0
}
pub(crate) fn key_id(key: &[u8; 32]) -> String {
    hex(&Sha256::new().chain_update(KEY_ID_DOMAIN).chain_update(key).finalize()[..8])
}
/// The sealed bytes: the domain, then the capture without `seal` and `recordId`
/// in the offer-digest canonical form (AAC §5.1).
fn message(capture: &Value) -> Result<Vec<u8>, EvidenceFailure> {
    let mut facts = capture.as_object().ok_or_else(|| failure(Cause::CaptureFactsUnencodable, "capture is not an object"))?.clone();
    facts.remove("seal");
    facts.remove("recordId");
    let mut text = String::new();
    crate::canonical::canonical(&Value::Object(facts), &mut text).map_err(|e| failure(Cause::CaptureFactsUnencodable, e))?;
    Ok([DOMAIN, text.as_bytes()].concat())
}

struct Keyring {
    current: String,
    keys: BTreeMap<String, [u8; 32]>,
    raw: Value,
}

/// Where this installation's keys live: set once at App startup from the App
/// data folder. In unit tests a per-process folder outside every test project
/// is used unless a test sets its own for its thread.
static FOLDER: Mutex<Option<PathBuf>> = Mutex::new(None);
#[cfg(test)]
thread_local! { static TEST_FOLDER: std::cell::RefCell<Option<Option<PathBuf>>> = const { std::cell::RefCell::new(None) }; }
#[cfg(test)]
static TEST_DEFAULT: std::sync::OnceLock<PathBuf> = std::sync::OnceLock::new();

/// Install this App installation's key folder (`<App data>/capture-seal`).
pub fn install(app_data: &Path) {
    *FOLDER.lock().unwrap() = Some(app_data.join(KEY_FOLDER));
}
/// Unit tests: use `folder` (or no key folder at all) on this thread.
#[cfg(test)]
pub(crate) fn set_folder_for_test(folder: Option<Option<PathBuf>>) {
    TEST_FOLDER.with(|f| *f.borrow_mut() = folder);
}
fn folder() -> Result<PathBuf, String> {
    #[cfg(test)]
    {
        if let Some(chosen) = TEST_FOLDER.with(|f| f.borrow().clone()) {
            return chosen.ok_or_else(|| "this App installation's capture-seal key folder is not known".into());
        }
        return Ok(TEST_DEFAULT
            .get_or_init(|| std::fs::canonicalize(std::env::temp_dir()).unwrap().join(crate::util::opaque_id("chirality-seal-test-").unwrap()))
            .clone());
    }
    #[allow(unreachable_code)]
    FOLDER.lock().unwrap().clone().ok_or_else(|| "this App installation's capture-seal key folder is not known".into())
}
/// Read-only enrollment root source: exactly the folder installed for ordinary
/// capture sealing, never a path supplied by a UI/caller enrollment request.
pub(crate) fn installed_root_for_enrollment() -> Result<PathBuf, String> {
    let installed = folder()?;
    if !installed.is_absolute() || installed.file_name().is_none_or(|name|name != KEY_FOLDER) {
        return Err("this App installation's capture-seal root is unavailable or invalid".into());
    }
    installed.parent().map(Path::to_path_buf).ok_or_else(||"this App installation's capture-seal root is unavailable".into())
}
/// The key folder must be outside the project whose captures it seals or reads.
fn folder_for(root: &Path) -> Result<PathBuf, EvidenceFailure> {
    let folder = folder().map_err(|e| failure(Cause::SealRootUnavailable, e))?;
    // Resolve through the nearest existing ancestor, so a folder not made yet
    // is compared as it will be.
    let real = |p: &Path| {
        p.ancestors()
            .find_map(|a| std::fs::canonicalize(a).ok().map(|c| c.join(p.strip_prefix(a).unwrap())))
            .unwrap_or_else(|| p.to_path_buf())
    };
    let (f, r) = (real(&folder), real(root));
    if crate::capture_seal_keychain::selected_route() {
        let continuity=real(&folder.with_file_name("capture-seal-keychain"));
        if continuity.starts_with(&r)||r.starts_with(&continuity){
            return Err(failure(Cause::SealRootUnavailable, "the capture-seal keychain continuity folder overlaps this project; provider not used there"));
        }
    }
    if f.starts_with(&r) || r.starts_with(&f) {
        return Err(failure(Cause::SealRootUnavailable, "the capture-seal key folder is inside this project (or contains it); keys are not used there"));
    }
    Ok(folder)
}
/// What verifying a capture of `root` depends on besides the capture itself:
/// the key folder in use and the identity, size, times (modified, changed), owner and mode of the
/// folder and its key file. An act read kept across calls is read again when
/// this changes (a key added, a folder moved, permissions changed).
pub(crate) fn verification_basis(root: &Path) -> String {
    if crate::capture_seal_keychain::selected_route() {
        // File metadata cannot establish keychain freshness. Force the consuming
        // cache to re-run verification; locked/missing/rotated items must revoke
        // prior positive observations. No SecItem call is made by this token.
        static NEXT: std::sync::atomic::AtomicU64 = std::sync::atomic::AtomicU64::new(0);
        return format!("SEAL-C keychain reobserve:{}", NEXT.fetch_add(1,std::sync::atomic::Ordering::Relaxed));
    }
    let describe = |p: &Path| match std::fs::symlink_metadata(p) {
        Ok(m) => format!("{}:{}:{}:{}:{}:{}:{}:{}:{:o}", m.dev(), m.ino(), m.len(), m.mtime(), m.mtime_nsec(), m.ctime(), m.ctime_nsec(), m.uid(), m.mode()),
        Err(e) => e.to_string(),
    };
    match folder_for(root) {
        Ok(folder) => format!("{}|{}|{}", folder.display(), describe(&folder), describe(&folder.join(KEY_FILE))),
        Err(e) => format!("no key folder: {e}"),
    }
}
fn uid() -> u32 {
    unsafe { libc::geteuid() }
}
/// Read the keyring; `Ok(None)` only when no key file exists yet.
fn load(folder: &Path) -> Result<Option<Keyring>, EvidenceFailure> {
    use std::io::Read;
    let path = folder.join(KEY_FILE);
    // Open without following a link and judge the opened file itself (fstat),
    // so nothing can be swapped in between the check and the read.
    let mut file = match std::fs::OpenOptions::new().read(true).custom_flags(libc::O_NOFOLLOW | libc::O_NONBLOCK).open(&path) {
        Ok(f) => f,
        Err(e) if e.kind() == std::io::ErrorKind::NotFound => return Ok(None),
        Err(e) if e.raw_os_error() == Some(libc::ELOOP) => return Err(failure(Cause::KeyStorageUnsafe, "capture-seal keys are a link, not a regular file in a folder; not used")),
        Err(e) => return Err(failure(Cause::SealRootUnavailable, format!("capture-seal keys not readable: {e}"))),
    };
    let meta = file.metadata().map_err(|e| failure(Cause::SealRootUnavailable, format!("capture-seal keys not readable: {e}")))?;
    let dir = std::fs::symlink_metadata(folder).map_err(|e| failure(Cause::SealRootUnavailable, format!("capture-seal key folder not readable: {e}")))?;
    if !meta.file_type().is_file() || !dir.file_type().is_dir() || crate::storage::check_path(folder).is_err() {
        return Err(failure(Cause::KeyStorageUnsafe, "capture-seal keys are a link, not a regular file in a folder; not used"));
    }
    if meta.uid() != uid() || dir.uid() != uid() {
        return Err(failure(Cause::KeyStorageUnsafe, "capture-seal keys are owned by another user; not used"));
    }
    if meta.mode() & 0o077 != 0 || dir.mode() & 0o077 != 0 {
        return Err(failure(Cause::KeyStorageUnsafe, "capture-seal keys are open to other users; not used"));
    }
    let mut bytes = Vec::new();
    file.read_to_end(&mut bytes).map_err(|e| failure(Cause::SealRootUnavailable, format!("capture-seal keys not readable: {e}")))?;
    let raw: Value = serde_json::from_slice(&bytes).map_err(|e| failure(Cause::KeyMaterialInvalid, format!("capture-seal keys not readable: {e}")))?;
    let bad = || failure(Cause::KeyMaterialInvalid, "capture-seal keys not in their format; not used");
    if raw["format"] != KEYRING_FORMAT || raw["formatVersion"] != "1" {
        return Err(bad());
    }
    let mut keys = BTreeMap::new();
    for entry in raw["keys"].as_array().ok_or_else(bad)? {
        let key: [u8; 32] = entry["key"].as_str().and_then(unhex).and_then(|k| k.try_into().ok()).ok_or_else(bad)?;
        if entry["keyId"] != key_id(&key).as_str() {
            return Err(bad());
        }
        keys.insert(key_id(&key), key);
    }
    let current = raw["current"].as_str().filter(|c| keys.contains_key(*c)).ok_or_else(bad)?.to_owned();
    Ok(Some(Keyring { current, keys, raw }))
}
/// Publish the keyring readable by its owner only: a 0600 file in a 0700 folder.
fn publish(folder: &Path, raw: &Value, replace: bool) -> Result<(), EvidenceFailure> {
    #[cfg(test)]
    crate::records_effect_guard::mutation_for_test("capture_seal::publish");
    crate::storage::ensure_directory(folder).map_err(|e| failure(Cause::SealWriteUnavailable, e))?;
    std::fs::set_permissions(folder, std::fs::Permissions::from_mode(0o700)).map_err(|e| failure(Cause::SealWriteUnavailable, format!("capture-seal key folder: {e}")))?;
    let path = folder.join(KEY_FILE);
    let temp = folder.join(format!(".{KEY_FILE}.{}.tmp", crate::util::opaque_id("").map_err(|e| failure(Cause::SealEntropyUnavailable, e))?));
    let result = (|| {
        let mut file = std::fs::OpenOptions::new().create_new(true).write(true).mode(0o600).open(&temp)
            .map_err(|e| failure(Cause::SealWriteUnavailable, format!("capture-seal keys: {e}")))?;
        file.write_all(&serde_json::to_vec_pretty(raw).map_err(|e| failure(Cause::SealWriteUnavailable, e.to_string()))?).map_err(|e| failure(Cause::SealWriteUnavailable, format!("capture-seal keys: {e}")))?;
        file.sync_all().map_err(|e| failure(Cause::SealWriteUnavailable, format!("capture-seal keys: {e}")))?;
        if replace {
            std::fs::rename(&temp, &path)
        } else {
            std::fs::hard_link(&temp, &path)
        }
        .map_err(|e| failure(Cause::SealWriteUnavailable, format!("capture-seal keys: {e}")))?;
        crate::storage::sync_dir(folder).map_err(|e| failure(Cause::SealWriteUnavailable, e))
    })();
    let _ = std::fs::remove_file(&temp);
    result
}
fn new_key() -> Result<([u8; 32], Value), EvidenceFailure> {
    let mut key = [0u8; 32];
    getrandom::fill(&mut key).map_err(|e| failure(Cause::SealEntropyUnavailable, format!("capture-seal key entropy unavailable: {e}")))?;
    Ok((key, json!({"keyId":key_id(&key),"key":hex(&key),"createdAt":crate::util::now_rfc3339()})))
}
/// The current keyring, creating this installation's first key when none exists.
fn load_or_create(folder: &Path) -> Result<Keyring, EvidenceFailure> {
    if let Some(ring) = load(folder)? {
        return Ok(ring);
    }
    let _lock = crate::storage::lock(&folder.join(".keys.lock")).map_err(|e| failure(Cause::SealOperationBusy, e))?;
    if let Some(ring) = load(folder)? {
        return Ok(ring);
    }
    let (key, entry) = new_key()?;
    let raw = json!({"format":KEYRING_FORMAT,"formatVersion":"1","current":key_id(&key),"keys":[entry]});
    publish(folder, &raw, false)?;
    load(folder)?.ok_or_else(|| failure(Cause::SealWriteUnavailable, "capture-seal keys not readable after creation"))
}
/// Rotate: add a new current key; earlier keys stay held so captures sealed
/// under them still verify here. Returns the new key identity.
pub fn rotate() -> Result<String, String> {
    let folder = folder()?;
    if let Some(result)=crate::capture_seal_keychain::dispatch(&folder,crate::capture_seal_keychain::Operation::Rotate){return result.map(|ring|ring.current).map_err(Into::into);}
    load_or_create(&folder)?; // takes and releases the lock itself
    let _lock = crate::storage::lock(&folder.join(".keys.lock")).map_err(|e| failure(Cause::SealOperationBusy, e))?;
    // Read the keyring under the lock, so a concurrent rotation is not lost.
    let ring = load(&folder)?.ok_or("capture-seal keys not readable for rotation")?;
    let (key, entry) = new_key()?;
    let mut raw = ring.raw.clone();
    raw["keys"].as_array_mut().ok_or("capture-seal keys not in their format")?.push(entry);
    raw["current"] = json!(key_id(&key));
    publish(&folder, &raw, true)?;
    Ok(key_id(&key))
}

/// Build the complete pair on a private copy. Failure never leaves a
/// provisional provider claim on the capture that the writer will publish.
fn attach(capture: &mut Value, material: crate::capture_seal_keychain::Material) -> Result<SealVerification, EvidenceFailure> {
    let mut facts = capture.clone();
    let object = facts.as_object_mut().ok_or_else(|| failure(Cause::CaptureFactsUnencodable, "capture is not an object"))?;
    object.insert("sealProvider".into(), json!(material.provider));
    let key = material.keys.get(&material.current).ok_or_else(|| failure(Cause::KeyNotHeld, "SEAL-C current key unavailable"))?;
    let mac = hmac(key, &message(&facts)?);
    facts["seal"] = json!({"method":SEAL_METHOD,"value":format!("{}:{}",material.current,hex(&mac))});
    *capture = facts;
    Ok(SealVerification { recorded_provider: Some(material.provider), verified_with: material.provider, key_id: material.current })
}
/// Seal a capture before its first publication, using only admitted material.
pub fn seal(root: &Path, capture: &mut Value) -> Result<SealVerification, EvidenceFailure> {
    let folder = folder_for(root)?;
    let material = match crate::capture_seal_keychain::dispatch(&folder, crate::capture_seal_keychain::Operation::Seal) {
        Some(result) => result?,
        None => file_material(load_or_create(&folder)?),
    };
    attach(capture, material)
}
/// Kept until the A15 writer moves to generic sealing; admission stays keychain-only.
pub(crate) fn seal_a15_if_keychain_available(root: &Path, capture: &mut Value) -> Result<SealVerification, EvidenceFailure> {
    let folder = folder_for(root)?;
    let material = crate::capture_seal_keychain::dispatch(&folder, crate::capture_seal_keychain::Operation::Seal)
        .ok_or_else(|| failure(Cause::KeychainProviderUnavailableOnThisBuild, "SEAL-C keychain provider is not selected/enrolled"))??;
    attach(capture, material)
}
/// The original wording remains the wording lane's; append provider/cause
/// presentation separately after the record's publication is known.
pub fn unsealed_limit(reason: impl std::fmt::Display) -> String {
    format!("capture not sealed ({reason}); not verifiable as this App's capture, so it is not counted as an act")
}
pub fn verify(root: &Path, capture: &Value) -> Result<SealVerification, EvidenceFailure> {
    verify_with(root, capture, false)
}
pub(crate) fn verify_keychain(root: &Path, capture: &Value) -> Result<SealVerification, EvidenceFailure> {
    verify_with(root, capture, true)
}
fn provider(capture: &Value) -> Result<Option<SealProvider>, EvidenceFailure> {
    match capture.get("sealProvider") {
        None => Ok(None),
        Some(value) => serde_json::from_value(value.clone()).map(Some)
            .map_err(|_| failure(Cause::ProviderInvalid, "capture seal provider is invalid; not verified here")),
    }
}
fn verify_with(root: &Path, capture: &Value, keychain_only: bool) -> Result<SealVerification, EvidenceFailure> {
    let recorded_provider = provider(capture)?;
    let Some(seal) = capture.get("seal") else {
        return Err(failure(if recorded_provider.is_some() { Cause::ProviderInvalid } else { Cause::NoSeal }, "capture has no App seal (written before capture sealing, or not by this App's act control); not verified here"));
    };
    if !seal.is_object() || !seal["method"].is_string() || !seal["value"].is_string() {
        return Err(failure(Cause::SealMalformed, "capture seal is malformed; not verified here"));
    }
    if seal["method"] != SEAL_METHOD {
        return Err(failure(Cause::SealMethodUnsupported, format!("capture seal method {} is not one this App verifies; not verified here", seal["method"])));
    }
    let value = seal["value"].as_str().unwrap_or("");
    let (id, mac) = value.split_once(':').unwrap_or(("", ""));
    if id.len() != 16 || mac.len() != 64 || unhex(id).is_none() || unhex(mac).is_none() {
        return Err(failure(Cause::SealMalformed, "capture seal value is malformed; not verified here"));
    }
    let folder = folder_for(root).map_err(|e| { let detail = format!("capture seal not checked: {e}; not verified here"); e.with_detail(detail) })?;
    let file_read = || -> Result<crate::capture_seal_keychain::Material, EvidenceFailure> {
        crate::capture_seal_keychain::file_read_authority()?;
        load(&folder)?.map(file_material).ok_or_else(|| failure(Cause::KeyNotHeld,
            format!("capture sealed under key {id:?}, which this App installation does not hold (another installation, or a key lost here); not verified here")))
    };
    // Labelled captures request exactly one provider. Legacy captures retain
    // the current-route rule; no error triggers a second verifier.
    let material = match recorded_provider {
        Some(SealProvider::FileKey) => file_read(),
        Some(SealProvider::Keychain) => crate::capture_seal_keychain::dispatch(&folder, crate::capture_seal_keychain::Operation::VerifyKey(id.into()))
            .unwrap_or_else(|| Err(failure(Cause::KeychainProviderUnavailableOnThisBuild, "keychain protection is not available on this build; not verified here"))),
        None => match crate::capture_seal_keychain::dispatch(&folder, crate::capture_seal_keychain::Operation::VerifyKey(id.into())) {
            Some(result) => result,
            None if keychain_only => Err(failure(Cause::KeychainProviderUnavailableOnThisBuild, "keychain protection is not available on this build; not verified here")),
            None => file_read(),
        },
    }.map_err(|e| { let detail = format!("capture seal not checked: {e}; not verified here"); e.with_detail(detail) })?;
    if let Some(recorded) = recorded_provider {
        if recorded != material.provider {
            let detail = match recorded {
                SealProvider::Keychain => "This capture claims the keychain provider but the verifying key comes from the key file; the claim is not verifiable as labelled.",
                SealProvider::FileKey => "This capture claims the file-key provider but the verifying key comes from the keychain; the claim is not verifiable as labelled.",
            };
            return Err(failure(Cause::ProviderMismatch, detail));
        }
    }
    let key = material.keys.get(id).ok_or_else(|| failure(Cause::KeyNotHeld,
        format!("capture sealed under key {id:?}, which this App installation does not hold (another installation, or a key lost here); not verified here")))?;
    if !equal(&unhex(mac).unwrap(), &hmac(key, &message(capture)?)) {
        return Err(failure(Cause::SealInvalid, format!("capture seal does not verify under this installation's key {id:?}: the capture's act facts changed after sealing, or it was not sealed by this App; not verified")));
    }
    if keychain_only && material.provider != SealProvider::Keychain {
        return Err(failure(Cause::ProviderNotEligible, "The file-key seal cannot supply keychain-verified workflow approval. Confirm A15 in this session, or enrol and make a new approval for future sessions."));
    }
    Ok(SealVerification { recorded_provider, verified_with: material.provider, key_id: id.into() })
}

#[cfg(test)]
mod tests {
    use super::*;
    fn temp(prefix: &str) -> PathBuf {
        let dir = std::env::temp_dir().join(crate::util::opaque_id(prefix).unwrap());
        std::fs::create_dir_all(&dir).unwrap();
        std::fs::canonicalize(dir).unwrap()
    }
    fn capture() -> Value {
        json!({"captureId":"cap:x","choice":"act","actKind":"A6","boundSubject":["/p/a"],"capturedAt":"2026-10-11T00:00:00.000Z","answers":{"n":1},
            "boundContent":[{"method":"m","value":"v"}],"scope":"the file","purpose":"rely","actor":{"osAccount":"fixture","identityVerified":false},
            "offerDigest":{"method":"aac-offer-digest/0.1","value":"0".repeat(64)}})
    }
    #[test]
    fn verify_returns_closed_causes_at_the_failing_primitive() {
        let (project, keys) = (temp("typed-seal-project-"), temp("typed-seal-keys-"));
        set_folder_for_test(Some(Some(keys.join(KEY_FOLDER))));
        let mut original = capture();
        seal(&project, &mut original).unwrap();
        verify(&project, &original).unwrap();
        let mut changed = original.clone();
        changed["choice"] = json!("decline");
        assert_eq!(verify(&project, &changed).unwrap_err().cause, Cause::SealInvalid);
        changed = original.clone();
        changed["seal"]["value"] = json!("bad encoding");
        assert_eq!(verify(&project, &changed).unwrap_err().cause, Cause::SealMalformed);
        changed = original.clone();
        changed["seal"]["method"] = json!("unknown");
        assert_eq!(verify(&project, &changed).unwrap_err().cause, Cause::SealMethodUnsupported);
        changed = original.clone();
        changed.as_object_mut().unwrap().remove("seal");
        changed.as_object_mut().unwrap().remove("sealProvider");
        assert_eq!(verify(&project, &changed).unwrap_err().cause, Cause::NoSeal);
        std::fs::remove_dir_all(keys.join(KEY_FOLDER)).unwrap();
        assert_eq!(verify(&project, &original).unwrap_err().cause, Cause::KeyNotHeld);
        set_folder_for_test(None);
        std::fs::remove_dir_all(project).unwrap();
        std::fs::remove_dir_all(keys).unwrap();
    }
    #[test]
    fn named_provider_is_covered_and_never_rescued_by_another_source() {
        use crate::capture_seal_keychain::{Material, set_material_provider_for_test};
        let (project, keys) = (temp("provider-project-"), temp("provider-keys-"));
        let folder = keys.join(KEY_FOLDER);
        set_folder_for_test(Some(Some(folder.clone())));
        let mut file = capture();
        assert_eq!(seal(&project, &mut file).unwrap().verified_with, SealProvider::FileKey);
        assert_eq!(file["sealProvider"], "file-key");
        assert_eq!(verify(&project, &file).unwrap().recorded_provider, Some(SealProvider::FileKey));
        assert_eq!(verify_keychain(&project, &file).unwrap_err().cause, Cause::ProviderNotEligible);
        let mut removed = file.clone();
        removed.as_object_mut().unwrap().remove("sealProvider");
        assert_eq!(verify(&project, &removed).unwrap_err().cause, Cause::SealInvalid);
        let ring = load(&folder).unwrap().unwrap();
        let material = Material { current: ring.current, keys: ring.keys, provider: SealProvider::Keychain };
        let mut keychain = capture();
        attach(&mut keychain, material.clone()).unwrap();
        let supplied = material.clone();
        set_material_provider_for_test(Some(Box::new(move |_, _| Ok(supplied.clone()))));
        verify(&project, &keychain).unwrap();
        // An explicitly named file source remains read-only and weaker on the
        // selected route, even with an enrolled keychain provider available.
        assert_eq!(verify(&project, &file).unwrap().verified_with, SealProvider::FileKey);
        set_material_provider_for_test(None);
        assert_eq!(verify(&project, &keychain).unwrap_err().cause, Cause::KeychainProviderUnavailableOnThisBuild);
        // Equal key bytes are insufficient: the trusted source must agree.
        let mut wrong_source = material.clone();
        wrong_source.provider = SealProvider::FileKey;
        set_material_provider_for_test(Some(Box::new(move |_, _| Ok(wrong_source.clone()))));
        assert_eq!(verify(&project, &keychain).unwrap_err().cause, Cause::ProviderMismatch);
        set_material_provider_for_test(Some(Box::new(move |_, _| Ok(material.clone()))));
        verify(&project, &keychain).unwrap();
        set_material_provider_for_test(None);
        set_folder_for_test(None);
        std::fs::remove_dir_all(project).unwrap();
        std::fs::remove_dir_all(keys).unwrap();
    }
    #[test]
    fn genuinely_legacy_facts_verify_without_a_recorded_provider() {
        let (project, keys) = (temp("legacy-seal-project-"), temp("legacy-seal-keys-"));
        let folder = keys.join(KEY_FOLDER);
        set_folder_for_test(Some(Some(folder.clone())));
        let ring = load_or_create(&folder).unwrap();
        let mut legacy = capture();
        let mac = hmac(&ring.keys[&ring.current], &message(&legacy).unwrap());
        legacy["seal"] = json!({"method":SEAL_METHOD,"value":format!("{}:{}",ring.current,hex(&mac))});
        let result = verify(&project, &legacy).unwrap();
        assert_eq!(result.recorded_provider, None);
        assert!(result.sentence().contains("provider not recorded"));
        assert_eq!(result.verified_with, SealProvider::FileKey);
        let bytes = legacy.clone();
        std::fs::remove_dir_all(&folder).unwrap();
        assert_eq!(verify(&project, &legacy).unwrap_err().cause, Cause::KeyNotHeld);
        publish(&folder, &ring.raw, false).unwrap();
        verify(&project, &legacy).unwrap();
        assert_eq!(legacy, bytes);
        set_folder_for_test(None);
        std::fs::remove_dir_all(project).unwrap();
        std::fs::remove_dir_all(keys).unwrap();
    }
    #[test]
    fn hmac_matches_rfc_4231_case_2() {
        assert_eq!(hex(&hmac(b"Jefe", b"what do ya want for nothing?")), "5bdcc146bf60754e6a042426089575c75a003f089d2739839dec58b964ec3843");
    }
    #[test]
    fn seal_covers_act_facts_not_the_backlink() {
        let (project, keys) = (temp("seal-project-"), temp("seal-keys-"));
        set_folder_for_test(Some(Some(keys.join(KEY_FOLDER))));
        let mut c = capture();
        seal(&project, &mut c).unwrap();
        verify(&project, &c).unwrap();
        let mut linked = c.clone();
        linked["recordId"] = json!("rec:app:1");
        verify(&project, &linked).unwrap();
        for (member, other) in [("actKind", json!("A7")), ("capturedAt", json!("2026-10-12T00:00:00.000Z")), ("boundSubject", json!(["/p/b"])), ("choice", json!("decline")),
            ("boundContent", json!([{"method":"m","value":"other"}])), ("scope", json!("other scope")), ("purpose", json!("other purpose")),
            ("actor", json!({"osAccount":"someone-else","identityVerified":false})), ("captureId", json!("cap:y")),
            ("offerDigest", json!({"method":"aac-offer-digest/0.1","value":"1".repeat(64)}))] {
            let mut changed = c.clone();
            changed[member] = other;
            assert!(verify(&project, &changed).unwrap_err().contains("does not verify"), "{member}");
        }
        let mut unsealed = c.clone();
        unsealed.as_object_mut().unwrap().remove("seal");
        unsealed.as_object_mut().unwrap().remove("sealProvider");
        assert!(verify(&project, &unsealed).unwrap_err().contains("no App seal"));
        let mut method = c.clone();
        method["seal"]["method"] = json!("other");
        assert!(verify(&project, &method).unwrap_err().contains("not one this App verifies"));
        set_folder_for_test(None);
    }
    #[test]
    fn keys_are_owner_only_and_outside_the_project() {
        let (project, keys) = (temp("seal-project-"), temp("seal-keys-"));
        let folder = keys.join(KEY_FOLDER);
        set_folder_for_test(Some(Some(folder.clone())));
        let mut c = capture();
        seal(&project, &mut c).unwrap();
        assert_eq!(std::fs::metadata(&folder).unwrap().mode() & 0o777, 0o700);
        assert_eq!(std::fs::metadata(folder.join(KEY_FILE)).unwrap().mode() & 0o777, 0o600);
        // Keys open to other users are not used, for reading or sealing.
        std::fs::set_permissions(folder.join(KEY_FILE), std::fs::Permissions::from_mode(0o644)).unwrap();
        assert!(verify(&project, &c).unwrap_err().contains("open to other users"));
        assert!(seal(&project, &mut capture()).is_err());
        std::fs::set_permissions(folder.join(KEY_FILE), std::fs::Permissions::from_mode(0o600)).unwrap();
        verify(&project, &c).unwrap();
        // A folder open to other users is not used either.
        std::fs::set_permissions(&folder, std::fs::Permissions::from_mode(0o750)).unwrap();
        assert!(verify(&project, &c).unwrap_err().contains("open to other users"));
        std::fs::set_permissions(&folder, std::fs::Permissions::from_mode(0o700)).unwrap();
        verify(&project, &c).unwrap();
        // A linked key file, or a linked key folder, is not used.
        let moved = keys.join("real-keys.json");
        std::fs::rename(folder.join(KEY_FILE), &moved).unwrap();
        std::os::unix::fs::symlink(&moved, folder.join(KEY_FILE)).unwrap();
        assert!(verify(&project, &c).unwrap_err().contains("a link"));
        std::fs::remove_file(folder.join(KEY_FILE)).unwrap();
        std::fs::rename(&moved, folder.join(KEY_FILE)).unwrap();
        verify(&project, &c).unwrap();
        let linked_folder = keys.join("linked-folder");
        std::os::unix::fs::symlink(&folder, &linked_folder).unwrap();
        set_folder_for_test(Some(Some(linked_folder)));
        assert!(verify(&project, &c).unwrap_err().contains("a link"));
        set_folder_for_test(Some(Some(folder.clone())));
        // A key folder containing the project is never used.
        set_folder_for_test(Some(Some(project.parent().unwrap().to_path_buf())));
        assert!(verify(&project, &c).unwrap_err().contains("inside this project (or contains it)"));
        set_folder_for_test(Some(Some(folder.clone())));
        verify(&project, &c).unwrap();
        // A key folder inside the project is never used, also when it is not
        // made yet and named through a link (/var is a link on macOS).
        set_folder_for_test(Some(Some(project.join(".chirality/capture-seal"))));
        assert!(seal(&project, &mut capture()).unwrap_err().contains("inside this project"));
        let linked = std::env::temp_dir().join(project.file_name().unwrap()).join("not-yet/capture-seal");
        set_folder_for_test(Some(Some(linked)));
        assert!(seal(&project, &mut capture()).unwrap_err().contains("inside this project"));
        assert!(verify(&project, &c).unwrap_err().contains("inside this project"));
        // No key folder known: nothing sealed, nothing verified.
        set_folder_for_test(Some(None));
        assert!(seal(&project, &mut capture()).is_err());
        assert!(verify(&project, &c).unwrap_err().contains("not known"));
        set_folder_for_test(None);
    }
    #[test]
    fn rotation_keeps_earlier_keys_and_loss_reads_not_verified_here() {
        let (project, keys) = (temp("seal-project-"), temp("seal-keys-"));
        let folder = keys.join(KEY_FOLDER);
        set_folder_for_test(Some(Some(folder.clone())));
        let mut before = capture();
        seal(&project, &mut before).unwrap();
        let first = before["seal"]["value"].as_str().unwrap().split(':').next().unwrap().to_owned();
        let second = rotate().unwrap();
        assert_ne!(first, second);
        let mut after = capture();
        seal(&project, &mut after).unwrap();
        assert!(after["seal"]["value"].as_str().unwrap().starts_with(&format!("{second}:")));
        verify(&project, &before).unwrap();
        verify(&project, &after).unwrap();
        // Loss: the keys are gone; a new key is made at the next capture and
        // earlier captures read "not verified here", never forged.
        std::fs::remove_dir_all(&folder).unwrap();
        assert!(verify(&project, &before).unwrap_err().contains("does not hold"));
        seal(&project, &mut capture()).unwrap();
        assert!(verify(&project, &before).unwrap_err().contains("does not hold"));
        set_folder_for_test(None);
    }
}
