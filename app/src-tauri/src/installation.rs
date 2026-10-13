//! U-STORE-2 attribution: an opaque App-data identity, never authentication.
//! The reference travels with a new A15 as an unverified claim. Copying or
//! editing this file can repeat/change that claim; no selection trusts it.
use serde_json::{json, Value};
#[cfg(test)]
use std::collections::HashMap;
use std::io::Read;
use std::os::unix::fs::{MetadataExt, OpenOptionsExt};
use std::path::{Path, PathBuf};
use std::sync::Mutex;
#[cfg(test)]
use std::sync::OnceLock;

const FILE: &str = "installation.json";
const FORMAT: &str = "chirality.app.installation";
static FOLDER: Mutex<Option<PathBuf>> = Mutex::new(None);
#[cfg(not(test))]
static OBSERVED: Mutex<Option<(PathBuf, String)>> = Mutex::new(None);
#[cfg(test)]
thread_local! {
    static TEST_FOLDER: std::cell::RefCell<Option<Option<PathBuf>>> = const { std::cell::RefCell::new(None) };
    static TEST_OBSERVED: std::cell::RefCell<HashMap<PathBuf, String>> = std::cell::RefCell::new(HashMap::new());
}
pub(crate) fn install(app_data: &Path) {
    *FOLDER.lock().unwrap_or_else(|p| p.into_inner()) = Some(app_data.to_path_buf());
}
#[cfg(test)]
pub(crate) fn folder_for_test(folder: Option<Option<PathBuf>>) {
    TEST_FOLDER.with(|f| *f.borrow_mut() = folder);
}
#[cfg(test)]
pub(crate) fn restart_for_test() {
    TEST_OBSERVED.with(|f| f.borrow_mut().clear());
}
fn folder() -> Result<PathBuf, String> {
    #[cfg(test)]
    {
        if let Some(f) = TEST_FOLDER.with(|f| f.borrow().clone()) {
            return f.ok_or("local installation identity folder unavailable".into());
        }
        static DEFAULT: OnceLock<PathBuf> = OnceLock::new();
        return Ok(DEFAULT
            .get_or_init(|| {
                std::fs::canonicalize(std::env::temp_dir())
                    .unwrap()
                    .join(format!(
                        "chirality-test-installation-{}",
                        std::process::id()
                    ))
            })
            .clone());
    }
    #[cfg(not(test))]
    FOLDER
        .lock()
        .unwrap_or_else(|p| p.into_inner())
        .clone()
        .ok_or("local installation identity folder unavailable".into())
}
fn valid(id: &str) -> bool {
    let Some(uuid) = id.strip_prefix("chirality-installation:") else {
        return false;
    };
    let b = uuid.as_bytes();
    b.len() == 36
        && b.iter().enumerate().all(|(i, b)| {
            if [8, 13, 18, 23].contains(&i) {
                *b == b'-'
            } else {
                b.is_ascii_hexdigit() && !b.is_ascii_uppercase()
            }
        })
        && b[14] == b'4'
        && [b'8', b'9', b'a', b'b'].contains(&b[19])
}
fn read(path: &Path) -> Result<Option<String>, String> {
    crate::storage::check_path(path).map_err(|_| "local installation identity path is linked")?;
    let file = match std::fs::OpenOptions::new()
        .read(true)
        .custom_flags(libc::O_NOFOLLOW | libc::O_NONBLOCK)
        .open(path)
    {
        Ok(f) => f,
        Err(e) if e.kind() == std::io::ErrorKind::NotFound => return Ok(None),
        Err(_) => return Err("local installation identity unreadable".into()),
    };
    let meta = file
        .metadata()
        .map_err(|_| "local installation identity unreadable")?;
    if !meta.is_file() || meta.nlink() != 1 || meta.len() > 4096 {
        return Err("local installation identity is not one bounded regular file".into());
    }
    let mut bytes = Vec::new();
    file.take(4097)
        .read_to_end(&mut bytes)
        .map_err(|_| "local installation identity unreadable")?;
    if bytes.len() > 4096 {
        return Err("local installation identity exceeds its bound".into());
    }
    let v: Value =
        serde_json::from_slice(&bytes).map_err(|_| "local installation identity malformed")?;
    if v["format"] != FORMAT || v["formatVersion"] != "0.1" {
        return Err("local installation identity has an unsupported format".into());
    }
    v["installationRef"]
        .as_str()
        .filter(|s| valid(s))
        .map(|s| Some(s.to_owned()))
        .ok_or("local installation reference malformed".into())
}
fn claim_at(folder: &Path, root: &Path, observed: Option<&str>) -> Result<String, String> {
    if folder.components().any(|c| {
        matches!(
            c,
            std::path::Component::ParentDir | std::path::Component::CurDir
        )
    }) {
        return Err("local installation identity folder is not normalized".into());
    }
    if !folder.is_absolute() {
        return Err("local installation identity folder must be absolute".into());
    }
    crate::storage::check_path(folder)
        .map_err(|_| "local installation identity folder is linked")?;
    // No identity file is written into a portable library. App data may
    // contain a user library as a sibling of this identity file.
    let resolved = folder
        .canonicalize()
        .unwrap_or_else(|_| folder.to_path_buf());
    let root = root
        .canonicalize()
        .map_err(|_| "opened library root unavailable")?;
    let resolved_file = resolved.join(FILE);
    if resolved_file.starts_with(&root) || root.starts_with(&resolved_file) {
        return Err("local installation identity folder overlaps the library".into());
    }
    let path = folder.join(FILE);
    let found = read(&path)?;
    if let Some(before) = observed {
        if found.as_deref() != Some(before) {
            return Err(
                "local installation identity changed or disappeared; attribution unavailable"
                    .into(),
            );
        }
    }
    if found.is_none() {
        let id = crate::util::opaque_id("chirality-installation:")
            .map_err(|_| "local installation identity entropy unavailable")?;
        let value = json!({"format":FORMAT,"formatVersion":"0.1","installationRef":id});
        // Create once. A concurrent creator's valid identity is usable only
        // after our own durable reread; no overwrite/clock/path fallback.
        let _ = crate::storage::create_json(&path, &value);
    }
    let id = read(&path)?.ok_or("local installation identity was not persisted")?;
    crate::storage::sync_publication(&path)
        .map_err(|_| "local installation identity persistence not established")?;
    // Retrying after a failed directory publication must flush the same
    // parent links even though those folders now exist. Sync the configured
    // App-data ancestor chain; presence alone never establishes durability.
    for ancestor in folder.ancestors().skip(1) {
        crate::storage::sync_dir(ancestor)
            .map_err(|_| "local installation identity ancestor durability not established")?;
    }
    if read(&path)?.as_deref() != Some(&id) {
        return Err("local installation identity changed while read".into());
    }
    Ok(id)
}
pub(crate) fn reference(root: &Path) -> Result<String, String> {
    let folder = folder()?;
    #[cfg(test)]
    return TEST_OBSERVED.with(|seen| {
        let mut seen = seen.borrow_mut();
        let id = claim_at(&folder, root, seen.get(&folder).map(String::as_str))?;
        seen.insert(folder, id.clone());
        Ok(id)
    });
    #[cfg(not(test))]
    {
        let mut observed = OBSERVED.lock().unwrap_or_else(|p| p.into_inner());
        let before = observed
            .as_ref()
            .filter(|(p, _)| p == &folder)
            .map(|(_, s)| s.as_str());
        let id = claim_at(&folder, root, before)?;
        *observed = Some((folder, id.clone()));
        Ok(id)
    }
}
pub(crate) fn capture_claim(root: &Path) -> (Value, Option<String>) {
    match reference(root) {
        Ok(id) => (json!({"reference":id,"verification":"unverified"}), None),
        Err(cause) => (
            json!({"reference":null,"verification":"unverified"}),
            Some(format!(
                "installation attribution unavailable ({cause}); not verified"
            )),
        ),
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    fn scratch() -> PathBuf {
        let p = std::env::temp_dir().join(crate::util::opaque_id("installation-fixture-").unwrap());
        std::fs::create_dir_all(&p).unwrap();
        p.canonicalize().unwrap()
    }
    #[test]
    fn stable_after_restart_and_not_replaced_on_persistence_or_identity_failure() {
        let root = scratch();
        let data = scratch();
        folder_for_test(Some(Some(data.clone())));
        let id = reference(&root).unwrap();
        restart_for_test();
        assert_eq!(reference(&root).unwrap(), id);
        std::fs::write(data.join(FILE), b"malformed").unwrap();
        assert!(reference(&root).is_err());
        assert_eq!(std::fs::read(data.join(FILE)).unwrap(), b"malformed");
        std::fs::remove_file(data.join(FILE)).unwrap();
        assert!(
            reference(&root).is_err(),
            "known missing identity is not silently reminted"
        );
        let (claim, limit) = capture_claim(&root);
        assert!(claim["reference"].is_null());
        assert!(limit.is_some());
        folder_for_test(None);
        std::fs::remove_dir_all(root).unwrap();
        std::fs::remove_dir_all(data).unwrap();
    }
    #[test]
    fn retry_keeps_unknown_attribution_until_new_app_data_ancestors_are_durable() {
        let root = scratch();
        let parent = scratch();
        let data = parent.join("new/app-data");
        folder_for_test(Some(Some(data.clone())));
        crate::storage::fail_directory_for_test(Some(parent.clone()));
        assert!(
            reference(&root).is_err(),
            "first creation cannot establish the parent link"
        );
        assert!(data.is_dir());
        assert!(
            reference(&root).is_err(),
            "retry must not treat existing folders as durable"
        );
        assert!(capture_claim(&root).0["reference"].is_null());
        crate::storage::fail_directory_for_test(None);
        let id = reference(&root).unwrap();
        restart_for_test();
        assert_eq!(reference(&root).unwrap(), id);
        folder_for_test(None);
        std::fs::remove_dir_all(root).unwrap();
        std::fs::remove_dir_all(parent).unwrap();
    }
    #[test]
    fn a_user_library_inside_app_data_does_not_hide_the_sibling_identity() {
        let data = scratch();
        let root = data.join("user-library");
        std::fs::create_dir_all(&root).unwrap();
        folder_for_test(Some(Some(data.clone())));
        assert!(reference(&root).is_ok());
        assert!(!root.join(FILE).exists());
        folder_for_test(None);
        std::fs::remove_dir_all(data).unwrap();
    }
    #[test]
    fn unavailable_linked_overlapping_and_unsynced_identity_is_unknown() {
        let root = scratch();
        let data = scratch();
        folder_for_test(Some(None));
        assert!(capture_claim(&root).0["reference"].is_null());
        folder_for_test(Some(Some(root.join("app-data"))));
        assert!(reference(&root).is_err());
        assert!(!root.join("app-data").exists());
        folder_for_test(Some(Some(data.clone())));
        reference(&root).unwrap();
        crate::storage::fail_directory_for_test(Some(data.clone()));
        assert!(reference(&root).unwrap_err().contains("persistence"));
        crate::storage::fail_directory_for_test(None);
        let outside = scratch().join("unchanged");
        std::fs::write(&outside, b"outside").unwrap();
        std::fs::remove_file(data.join(FILE)).unwrap();
        std::os::unix::fs::symlink(&outside, data.join(FILE)).unwrap();
        assert!(reference(&root).is_err());
        assert_eq!(std::fs::read(&outside).unwrap(), b"outside");
        folder_for_test(None);
        std::fs::remove_dir_all(outside.parent().unwrap()).unwrap();
        std::fs::remove_dir_all(root).unwrap();
        std::fs::remove_dir_all(data).unwrap();
    }
}
