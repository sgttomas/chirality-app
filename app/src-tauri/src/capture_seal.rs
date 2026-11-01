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
fn message(capture: &Value) -> Result<Vec<u8>, String> {
    let mut facts = capture.as_object().ok_or("capture is not an object")?.clone();
    facts.remove("seal");
    facts.remove("recordId");
    let mut text = String::new();
    crate::canonical::canonical(&Value::Object(facts), &mut text)?;
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
fn folder_for(root: &Path) -> Result<PathBuf, String> {
    let folder = folder()?;
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
            return Err("the capture-seal keychain continuity folder overlaps this project; provider not used there".into());
        }
    }
    if f.starts_with(&r) || r.starts_with(&f) {
        return Err("the capture-seal key folder is inside this project (or contains it); keys are not used there".into());
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
fn load(folder: &Path) -> Result<Option<Keyring>, String> {
    use std::io::Read;
    let path = folder.join(KEY_FILE);
    // Open without following a link and judge the opened file itself (fstat),
    // so nothing can be swapped in between the check and the read.
    let mut file = match std::fs::OpenOptions::new().read(true).custom_flags(libc::O_NOFOLLOW | libc::O_NONBLOCK).open(&path) {
        Ok(f) => f,
        Err(e) if e.kind() == std::io::ErrorKind::NotFound => return Ok(None),
        Err(e) if e.raw_os_error() == Some(libc::ELOOP) => return Err("capture-seal keys are a link, not a regular file in a folder; not used".into()),
        Err(e) => return Err(format!("capture-seal keys not readable: {e}")),
    };
    let meta = file.metadata().map_err(|e| format!("capture-seal keys not readable: {e}"))?;
    let dir = std::fs::symlink_metadata(folder).map_err(|e| format!("capture-seal key folder not readable: {e}"))?;
    if !meta.file_type().is_file() || !dir.file_type().is_dir() || crate::storage::check_path(folder).is_err() {
        return Err("capture-seal keys are a link, not a regular file in a folder; not used".into());
    }
    if meta.uid() != uid() || dir.uid() != uid() {
        return Err("capture-seal keys are owned by another user; not used".into());
    }
    if meta.mode() & 0o077 != 0 || dir.mode() & 0o077 != 0 {
        return Err("capture-seal keys are open to other users; not used".into());
    }
    let mut bytes = Vec::new();
    file.read_to_end(&mut bytes).map_err(|e| format!("capture-seal keys not readable: {e}"))?;
    let raw: Value = serde_json::from_slice(&bytes).map_err(|e| format!("capture-seal keys not readable: {e}"))?;
    let bad = || "capture-seal keys not in their format; not used".to_owned();
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
fn publish(folder: &Path, raw: &Value, replace: bool) -> Result<(), String> {
    crate::storage::ensure_directory(folder)?;
    std::fs::set_permissions(folder, std::fs::Permissions::from_mode(0o700)).map_err(|e| format!("capture-seal key folder: {e}"))?;
    let path = folder.join(KEY_FILE);
    let temp = folder.join(format!(".{KEY_FILE}.{}.tmp", crate::util::opaque_id("")?));
    let result = (|| {
        let mut file = std::fs::OpenOptions::new().create_new(true).write(true).mode(0o600).open(&temp)
            .map_err(|e| format!("capture-seal keys: {e}"))?;
        file.write_all(&serde_json::to_vec_pretty(raw).map_err(|e| e.to_string())?).map_err(|e| format!("capture-seal keys: {e}"))?;
        file.sync_all().map_err(|e| format!("capture-seal keys: {e}"))?;
        if replace {
            std::fs::rename(&temp, &path)
        } else {
            std::fs::hard_link(&temp, &path)
        }
        .map_err(|e| format!("capture-seal keys: {e}"))?;
        crate::storage::sync_dir(folder)
    })();
    let _ = std::fs::remove_file(&temp);
    result
}
fn new_key() -> Result<([u8; 32], Value), String> {
    let mut key = [0u8; 32];
    getrandom::fill(&mut key).map_err(|e| format!("capture-seal key entropy unavailable: {e}"))?;
    Ok((key, json!({"keyId":key_id(&key),"key":hex(&key),"createdAt":crate::util::now_rfc3339()})))
}
/// The current keyring, creating this installation's first key when none exists.
fn load_or_create(folder: &Path) -> Result<Keyring, String> {
    if let Some(ring) = load(folder)? {
        return Ok(ring);
    }
    let _lock = crate::storage::lock(&folder.join(".keys.lock"))?;
    if let Some(ring) = load(folder)? {
        return Ok(ring);
    }
    let (key, entry) = new_key()?;
    let raw = json!({"format":KEYRING_FORMAT,"formatVersion":"1","current":key_id(&key),"keys":[entry]});
    publish(folder, &raw, false)?;
    load(folder)?.ok_or_else(|| "capture-seal keys not readable after creation".into())
}
/// Rotate: add a new current key; earlier keys stay held so captures sealed
/// under them still verify here. Returns the new key identity.
pub fn rotate() -> Result<String, String> {
    let folder = folder()?;
    if let Some(result)=crate::capture_seal_keychain::dispatch(&folder,crate::capture_seal_keychain::Operation::Rotate){return result.map(|ring|ring.current);}
    load_or_create(&folder)?; // takes and releases the lock itself
    let _lock = crate::storage::lock(&folder.join(".keys.lock"))?;
    // Read the keyring under the lock, so a concurrent rotation is not lost.
    let ring = load(&folder)?.ok_or("capture-seal keys not readable for rotation")?;
    let (key, entry) = new_key()?;
    let mut raw = ring.raw.clone();
    raw["keys"].as_array_mut().ok_or("capture-seal keys not in their format")?.push(entry);
    raw["current"] = json!(key_id(&key));
    publish(&folder, &raw, true)?;
    Ok(key_id(&key))
}

/// Seal a capture for the project at `root` before its first publication.
pub fn seal(root: &Path, capture: &mut Value) -> Result<(), String> {
    let folder=folder_for(root)?;
    let ring=match crate::capture_seal_keychain::dispatch(&folder,crate::capture_seal_keychain::Operation::Seal){
        Some(result)=>{let material=result?;Keyring{current:material.current,keys:material.keys,raw:Value::Null}},
        None=>load_or_create(&folder)?,
    };
    let key = ring.keys[&ring.current];
    let mac = hmac(&key, &message(capture)?);
    capture["seal"] = json!({"method":SEAL_METHOD,"value":format!("{}:{}",ring.current,hex(&mac))});
    Ok(())
}
/// The evidence limit a capture of the App act control carries when it could
/// not be sealed; such a capture is recorded but never counted.
pub fn unsealed_limit(reason: &str) -> String {
    format!("capture not sealed ({reason}); not verifiable as this App's capture, so it is not counted as an act")
}
/// Whether this installation verifies the capture's seal. `Err` is the stated
/// limit for a capture that is not counted; it never claims a forgery.
pub fn verify(root: &Path, capture: &Value) -> Result<(), String> {
    let Some(seal) = capture.get("seal") else {
        return Err("capture has no App seal (written before capture sealing, or not by this App's act control); not verified here".into());
    };
    if seal["method"] != SEAL_METHOD {
        return Err(format!("capture seal method {} is not one this App verifies; not verified here", seal["method"]));
    }
    let value = seal["value"].as_str().unwrap_or("");
    let (id, mac) = value.split_once(':').unwrap_or(("", ""));
    let folder = folder_for(root).map_err(|e| format!("capture seal not checked: {e}; not verified here"))?;
    let ring=match crate::capture_seal_keychain::dispatch(&folder,crate::capture_seal_keychain::Operation::VerifyKey(id.to_owned())){
        Some(result)=>result.map(|material|Some(Keyring{current:material.current,keys:material.keys,raw:Value::Null})),
        None=>load(&folder),
    }.map_err(|e|format!("capture seal not checked: {e}; not verified here"))?;
    let Some(key) = ring.as_ref().and_then(|r| r.keys.get(id)) else {
        return Err(format!("capture sealed under key {id:?}, which this App installation does not hold (another installation, or a key lost here); not verified here"));
    };
    match unhex(mac) {
        Some(mac) if equal(&mac, &hmac(key, &message(capture)?)) => Ok(()),
        _ => Err(format!("capture seal does not verify under this installation's key {id:?}: the capture's act facts changed after sealing, or it was not sealed by this App; not verified")),
    }
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
