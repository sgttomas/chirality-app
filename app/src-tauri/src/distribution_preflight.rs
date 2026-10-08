//! Staged S2 filesystem preflight. No production selection or supplier execution.
//! Descriptor observations cannot eliminate hostile same-user check-to-exec races.
use serde::{Deserialize, Serialize};
use sha2::{Digest, Sha256};
use std::{
    collections::BTreeMap,
    ffi::{CStr, CString},
    fs::File,
    io::Read,
    os::unix::{
        fs::MetadataExt,
        io::{AsRawFd, FromRawFd},
    },
    path::{Component, Path},
};

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct Entry {
    pub path: String,
    pub kind: String,
    pub mode: u32,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub size: Option<u64>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub sha256: Option<String>,
}
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct Inventory {
    pub method: String,
    pub algorithm: String,
    pub entries: Vec<Entry>,
    pub manifest_sha256: String,
}
pub fn digest(bytes: &[u8]) -> String {
    format!("{:x}", Sha256::digest(bytes))
}
fn name(s: &str) -> Result<(), String> {
    if s.is_empty() || s == "." || s == ".." || s.contains(['/', '\\', '\r', '\n', '\0']) {
        return Err("unsupported path component".into());
    }
    Ok(())
}
fn open_at(parent: &File, child: &str, directory: bool) -> Result<File, String> {
    let child = CString::new(child).map_err(|_| "NUL path")?;
    let flags = libc::O_RDONLY
        | libc::O_CLOEXEC
        | libc::O_NOFOLLOW
        | libc::O_NONBLOCK
        | if directory { libc::O_DIRECTORY } else { 0 };
    // SAFETY: valid borrowed directory fd, NUL-terminated name, owned result fd.
    let fd = unsafe { libc::openat(parent.as_raw_fd(), child.as_ptr(), flags) };
    if fd < 0 {
        return Err(format!(
            "no-follow open refused: {}",
            std::io::Error::last_os_error()
        ));
    }
    Ok(unsafe { File::from_raw_fd(fd) })
}
fn root(path: &Path) -> Result<File, String> {
    if !path.is_absolute() {
        return Err("absolute physical root required".into());
    }
    let mut fd = File::open("/").map_err(|e| e.to_string())?;
    for c in path.components() {
        match c {
            Component::RootDir => (),
            Component::Normal(s) => {
                let s = s.to_str().ok_or("non UTF-8 component")?;
                name(s)?;
                fd = open_at(&fd, s, true)?;
            }
            _ => return Err("non-normal root".into()),
        }
    }
    Ok(fd)
}
type Stamp = (u64, u64, u64, u32, u64, i64, i64, i64, i64);
fn stamp(m: &std::fs::Metadata) -> Stamp {
    (
        m.dev(),
        m.ino(),
        m.nlink(),
        m.mode(),
        m.size(),
        m.mtime(),
        m.mtime_nsec(),
        m.ctime(),
        m.ctime_nsec(),
    )
}
fn names(fd: &File) -> Result<Vec<String>, String> {
    // A fresh open file description avoids shared directory offsets with dup().
    let copy = open_at(fd, ".", true)?;
    let raw = std::os::fd::IntoRawFd::into_raw_fd(copy);
    let dir = unsafe { libc::fdopendir(raw) };
    if dir.is_null() {
        unsafe {
            libc::close(raw);
        }
        return Err("fdopendir refused".into());
    }
    let mut out = Vec::new();
    let result = (|| {
        loop {
            // errno is reset because readdir null means either EOF or error.
            #[cfg(target_os = "macos")]
            unsafe {
                *libc::__error() = 0;
            }
            #[cfg(target_os = "linux")]
            unsafe {
                *libc::__errno_location() = 0;
            }
            let entry = unsafe { libc::readdir(dir) };
            if entry.is_null() {
                if std::io::Error::last_os_error().raw_os_error().unwrap_or(0) != 0 {
                    return Err("directory enumeration failed".into());
                }
                break;
            }
            let bytes = unsafe { CStr::from_ptr((*entry).d_name.as_ptr()) }.to_bytes();
            if bytes == b"." || bytes == b".." {
                continue;
            }
            let s = std::str::from_utf8(bytes).map_err(|_| "non UTF-8 entry")?;
            name(s)?;
            out.push(s.to_owned());
        }
        out.sort();
        if out.windows(2).any(|p| p[0] == p[1]) {
            return Err("duplicate directory entry".into());
        }
        Ok(out)
    })();
    unsafe {
        libc::closedir(dir);
    }
    result
}
fn walk(
    fd: &File,
    path: &str,
    entries: &mut Vec<Entry>,
    stamps: &mut BTreeMap<String, Stamp>,
) -> Result<(), String> {
    let before = fd.metadata().map_err(|e| e.to_string())?;
    let children = names(fd)?;
    stamps.insert(path.to_owned(), stamp(&before));
    entries.push(Entry {
        path: path.into(),
        kind: "dir".into(),
        mode: before.mode() & 0o7777,
        size: None,
        sha256: None,
    });
    for child in &children {
        let mut opened = open_at(fd, child, false)?;
        let before = opened.metadata().map_err(|e| e.to_string())?;
        let relative = if path == "." {
            child.clone()
        } else {
            format!("{path}/{child}")
        };
        stamps.insert(relative.clone(), stamp(&before));
        if before.is_dir() {
            walk(&opened, &relative, entries, stamps)?;
        } else if before.is_file() {
            if before.nlink() != 1 {
                return Err("hard-linked file refused".into());
            }
            let mut hash = Sha256::new();
            let mut size = 0u64;
            let mut buffer = [0u8; 65536];
            loop {
                let n = opened.read(&mut buffer).map_err(|e| e.to_string())?;
                if n == 0 {
                    break;
                }
                size += n as u64;
                hash.update(&buffer[..n]);
            }
            if size != before.size() {
                return Err("file size changed during read".into());
            }
            entries.push(Entry {
                path: relative,
                kind: "file".into(),
                mode: before.mode() & 0o7777,
                size: Some(size),
                sha256: Some(format!("{:x}", hash.finalize())),
            });
        } else {
            return Err("unsupported filesystem entry".into());
        }
        let after = opened.metadata().map_err(|e| e.to_string())?;
        let rebound = open_at(fd, child, before.is_dir())?
            .metadata()
            .map_err(|e| e.to_string())?;
        if stamp(&before) != stamp(&after) || stamp(&before) != stamp(&rebound) {
            return Err("entry changed during scan".into());
        }
    }
    if children != names(fd)? || stamp(&before) != stamp(&fd.metadata().map_err(|e| e.to_string())?)
    {
        return Err("directory changed during scan".into());
    }
    Ok(())
}
// Revisit every path after all content reads. Parent-directory timestamps alone
// do not detect an in-place write to a previously hashed descendant. Identity,
// nlink, mode, size, mtime and ctime are compared, including nanoseconds.
fn final_audit(
    fd: &File,
    path: &str,
    expected: &BTreeMap<String, Stamp>,
    seen: &mut usize,
) -> Result<(), String> {
    let before = fd.metadata().map_err(|e| e.to_string())?;
    if expected.get(path) != Some(&stamp(&before)) {
        return Err("entry changed before final inventory audit".into());
    }
    *seen += 1;
    if before.is_dir() {
        let children = names(fd)?;
        for child in &children {
            let opened = open_at(fd, child, false)?;
            let relative = if path == "." {
                child.clone()
            } else {
                format!("{path}/{child}")
            };
            final_audit(&opened, &relative, expected, seen)?;
            let rebound = open_at(fd, child, false)?
                .metadata()
                .map_err(|e| e.to_string())?;
            if expected.get(&relative) != Some(&stamp(&rebound)) {
                return Err("path replaced during final inventory audit".into());
            }
        }
        if children != names(fd)? {
            return Err("directory entries changed during final inventory audit".into());
        }
    }
    if stamp(&before) != stamp(&fd.metadata().map_err(|e| e.to_string())?) {
        return Err("entry changed during final inventory audit".into());
    }
    Ok(())
}
pub fn scan(path: &Path) -> Result<Inventory, String> {
    let fd = root(path)?;
    let before = fd.metadata().map_err(|e| e.to_string())?;
    let mut entries = Vec::new();
    let mut stamps = BTreeMap::new();
    walk(&fd, ".", &mut entries, &mut stamps)?;
    let mut seen = 0;
    final_audit(&fd, ".", &stamps, &mut seen)?;
    if seen != stamps.len() {
        return Err("path set changed before final inventory audit".into());
    }
    if stamp(&before) != stamp(&root(path)?.metadata().map_err(|e| e.to_string())?) {
        return Err("root changed during scan".into());
    }
    entries.sort_by(|a, b| a.path.as_bytes().cmp(b.path.as_bytes()));
    let manifest: String = entries
        .iter()
        .filter(|e| e.kind == "file")
        .map(|e| format!("{}  {}\n", e.sha256.as_ref().unwrap(), e.path))
        .collect();
    Ok(Inventory {
        method: "codex-vendor-tree-v1".into(),
        algorithm: "sha-256".into(),
        entries,
        manifest_sha256: digest(manifest.as_bytes()),
    })
}
/// Complete inventory comparison is order independent, but rejects duplicate paths.
pub fn equal(expected: &Inventory, actual: &Inventory) -> bool {
    fn map(i: &Inventory) -> BTreeMap<&str, &Entry> {
        i.entries.iter().map(|e| (e.path.as_str(), e)).collect()
    }
    let e = map(expected);
    let a = map(actual);
    expected.method == actual.method
        && expected.algorithm == actual.algorithm
        && expected.manifest_sha256 == actual.manifest_sha256
        && e.len() == expected.entries.len()
        && a.len() == actual.entries.len()
        && e == a
}
/// Re-enumerates instead of caching an earlier match. This is preflight only.
pub fn revalidate(path: &Path, expected: &Inventory) -> Result<Inventory, String> {
    let actual = scan(path)?;
    if !equal(expected, &actual) {
        return Err("complete distribution inventory mismatch".into());
    }
    Ok(actual)
}
#[cfg(test)]
#[path = "distribution_preflight_tests.rs"]
mod tests;

#[derive(Clone, Debug, Serialize, Deserialize, PartialEq, Eq)]
#[serde(deny_unknown_fields)]
pub struct Artifact {
    pub path: String,
    pub sha256: String,
}
#[derive(Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
struct Selection {
    format: String,
    method: String,
    schema_ids: [String; 2],
    expected: Artifact,
    attestation: Artifact,
}
// No S3-qualified selection exists. Only source-reviewed compilation can change this.
const PRODUCTION_SELECTION: Option<(&str, &str)> = None;
pub fn production_available() -> bool {
    PRODUCTION_SELECTION.is_some()
}
fn artifact(base: &Path, reference: &Artifact) -> Result<Vec<u8>, String> {
    let mut fd = root(base)?;
    let parts: Vec<_> = reference.path.split('/').collect();
    if parts.is_empty() {
        return Err("empty artifact path".into());
    }
    for (index, p) in parts.iter().enumerate() {
        name(p)?;
        fd = open_at(&fd, p, index + 1 < parts.len())?;
    }
    let before = fd.metadata().map_err(|e| e.to_string())?;
    if !before.is_file() || before.nlink() != 1 {
        return Err("artifact is not unique regular file".into());
    }
    let mut raw = Vec::new();
    fd.read_to_end(&mut raw).map_err(|e| e.to_string())?;
    if stamp(&before) != stamp(&fd.metadata().map_err(|e| e.to_string())?)
        || digest(&raw) != reference.sha256
    {
        return Err("artifact exact-byte mismatch or unstable read".into());
    }
    Ok(raw)
}
fn resolve(base: &Path, anchor: &Artifact) -> Result<serde_json::Value, String> {
    fn parsed(raw: Vec<u8>, schema: &str) -> Result<serde_json::Value, String> {
        let value = serde_json::from_slice(&raw).map_err(|e| e.to_string())?;
        let schema = serde_json::from_str(schema).map_err(|e| e.to_string())?;
        let validator = jsonschema::validator_for(&schema).map_err(|e| e.to_string())?;
        validator.validate(&value).map_err(|e| e.to_string())?;
        Ok(value)
    }
    let selection: Selection =
        serde_json::from_slice(&artifact(base, anchor)?).map_err(|e| e.to_string())?;
    if selection.format != "build-selection.s2"
        || selection.method != "codex-vendor-tree-v1"
        || selection.schema_ids != ["expected-reference.s1", "adoption-attestation.s1"]
    {
        return Err("unknown build selection method/schema identity".into());
    }
    let e = parsed(
        artifact(base, &selection.expected)?,
        include_str!("../resources/distribution-successor/expected-reference.s1.schema.json"),
    )?;
    let a = parsed(
        artifact(base, &selection.attestation)?,
        include_str!("../resources/distribution-successor/adoption-attestation.s1.schema.json"),
    )?;
    if a["expected_reference"] != serde_json::to_value(&selection.expected).unwrap()
        || a["author"] != e["author"]
        || a["author"].as_str().unwrap().trim().to_lowercase()
            == a["independent_reviewer"]
                .as_str()
                .unwrap()
                .trim()
                .to_lowercase()
        || e["pin"] != e["generated"]["pin"]
    {
        return Err("reference/attestation binding mismatch".into());
    }
    for pointer in [
        "/label_evidence",
        "/generation_correspondence",
        "/generated/provenance",
        "/generated/version_advance",
        "/archive/acquisition_authorization",
        "/archive/custody",
        "/archive/extraction_procedure",
    ] {
        artifact(
            base,
            &serde_json::from_value(e.pointer(pointer).unwrap().clone())
                .map_err(|e| e.to_string())?,
        )?;
    }
    for pointer in [
        "/review_evidence",
        "/adoption/through_help_human",
        "/adoption/evidence",
    ] {
        artifact(
            base,
            &serde_json::from_value(a.pointer(pointer).unwrap().clone())
                .map_err(|e| e.to_string())?,
        )?;
    }
    Ok(serde_json::json!({"expected":e,"selection":selection}))
}
#[derive(Debug)]
struct LaunchPlan {
    executable: std::path::PathBuf,
    path: String,
    removed: [&'static str; 2],
}
fn plan(root: &Path, inherited: Option<&str>) -> Result<LaunchPlan, String> {
    let prefix = root
        .join("codex-path")
        .to_str()
        .ok_or("non UTF-8 PATH")?
        .to_owned();
    if prefix.contains([':', '\0']) {
        return Err("unrepresentable PATH prefix".into());
    }
    Ok(LaunchPlan {
        executable: root.join("bin/codex"),
        path: match inherited {
            Some(p) => format!("{prefix}:{p}"),
            None => prefix,
        },
        removed: ["CODEX_MANAGED_PACKAGE_ROOT", "CODEX_MANAGED_BY_NPM"],
    })
}
// Private orchestration seam: no caller can inject a trust selection into production.
// Callbacks stand for future isolated label/native launch adapters, exercised only synthetically.
fn staged_start(
    base: &Path,
    tree: &Path,
    anchor: &Artifact,
    generated: &serde_json::Value,
    inherited: Option<&str>,
    verification_generation: serde_json::Value,
    label: impl FnOnce(&LaunchPlan) -> Result<String, String>,
    launch: impl FnOnce(&LaunchPlan) -> Result<serde_json::Value, String>,
) -> Result<serde_json::Value, String> {
    if verification_generation["appSession"]
        .as_str()
        .is_none_or(str::is_empty)
        || verification_generation["home"]
            .as_str()
            .is_none_or(str::is_empty)
        || verification_generation["spawnCounter"]
            .as_u64()
            .unwrap_or(0)
            == 0
        || verification_generation
            .as_object()
            .is_none_or(|g| g.len() != 3)
    {
        return Err("invalid allocated H5 generation".into());
    }
    let resolved = resolve(base, anchor)?;
    let expected = &resolved["expected"];
    let selection: Selection =
        serde_json::from_value(resolved["selection"].clone()).map_err(|e| e.to_string())?;
    let inventory: Inventory =
        serde_json::from_value(expected["inventory"].clone()).map_err(|e| e.to_string())?;
    revalidate(tree, &inventory)?;
    if &expected["generated"] != generated {
        return Err("generated identity mismatch".into());
    }
    let plan = plan(tree, inherited)?;
    let raw = label(&plan)?;
    if raw.strip_suffix('\n').unwrap_or(&raw)
        != format!("codex-cli {}", expected["pin"].as_str().unwrap())
    {
        return Err("observed label mismatch".into());
    }
    let observed = revalidate(tree, &inventory)?;
    let generation = launch(&plan)?;
    if generation != verification_generation
        || generation["appSession"].as_str().is_none_or(str::is_empty)
        || generation["home"].as_str().is_none_or(str::is_empty)
        || generation["spawnCounter"].as_u64().unwrap_or(0) == 0
    {
        return Err("launch returned invalid generation".into());
    }
    Ok(
        serde_json::json!({"format":"staged-preflight.s2","outcome":"unverifiable","inventory":observed,"generation":generation,"verification_generation":verification_generation,"build_selection":anchor,"raw_version_label":raw,"expected_reference":selection.expected,"adoption_attestation":selection.attestation,"resolved_executable":plan.executable,"removed_environment_names":plan.removed,"limits":["Synthetic adapter only; S3 qualification, native custody, installed integrity and lifecycle successor publication absent","Residual check-to-exec race; no production verification claim"]}),
    )
}
