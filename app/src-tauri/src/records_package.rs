//! Private custody of an incoming records bag. Package bytes establish no
//! authenticated origin, human act, or current supplier/capability authority.
//! The import owner separately validates and reconciles administrative history.
use serde::de::{self, MapAccess, SeqAccess, Visitor};
use serde::{Deserialize, Deserializer, Serialize};
use serde_json::Value;
use sha2::{Digest, Sha256};
use std::collections::BTreeMap;
use std::ffi::{CStr, CString, OsStr};
use std::fs::{File, Metadata};
use std::io::{Read, Seek, SeekFrom, Write};
use std::os::fd::{AsRawFd, FromRawFd, IntoRawFd};
use std::os::unix::fs::MetadataExt;
use std::path::{Component, Path, PathBuf};

const ADMIN: &str = "records-administration.json";
const TAGS: &[&str] = &[
    "bagit.txt",
    "bag-info.txt",
    "manifest-sha256.txt",
    "records-chain-heads.json",
    "verify.py",
    ADMIN,
];
const SAFE_READ: i32 = libc::O_RDONLY | libc::O_NOFOLLOW | libc::O_NONBLOCK | libc::O_CLOEXEC;

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub(crate) struct Member {
    pub sha256: String,
    pub bytes: u64,
}

#[derive(Clone, Debug, PartialEq, Eq)]
struct Stamp {
    device: u64,
    inode: u64,
    mode: u32,
    links: u64,
    owner: u32,
    size: u64,
    modified: (i64, i64),
    changed: (i64, i64),
}
impl Stamp {
    fn of(m: &Metadata) -> Self {
        Self {
            device: m.dev(),
            inode: m.ino(),
            mode: m.mode(),
            links: m.nlink(),
            owner: m.uid(),
            size: m.len(),
            modified: (m.mtime(), m.mtime_nsec()),
            changed: (m.ctime(), m.ctime_nsec()),
        }
    }
    fn at(dir: &File, name: &str) -> Result<Self, String> {
        let name = name_c(name)?;
        let mut raw = std::mem::MaybeUninit::<libc::stat>::uninit();
        // SAFETY: name is NUL-terminated, dir is live, and the output is used
        // only after a successful fstatat. No link is followed.
        if unsafe {
            libc::fstatat(
                dir.as_raw_fd(),
                name.as_ptr(),
                raw.as_mut_ptr(),
                libc::AT_SYMLINK_NOFOLLOW,
            )
        } != 0
        {
            return Err(system("package member metadata"));
        }
        let m = unsafe { raw.assume_init() };
        Ok(Self {
            device: m.st_dev as u64,
            inode: m.st_ino as u64,
            mode: m.st_mode as u32,
            links: m.st_nlink as u64,
            owner: m.st_uid,
            size: m.st_size as u64,
            modified: (m.st_mtime as i64, m.st_mtime_nsec as i64),
            changed: (m.st_ctime as i64, m.st_ctime_nsec as i64),
        })
    }
    fn directory(&self) -> bool {
        self.mode & libc::S_IFMT as u32 == libc::S_IFDIR as u32
    }
    fn regular(&self) -> bool {
        self.mode & libc::S_IFMT as u32 == libc::S_IFREG as u32
    }
    fn plain(&self) -> Result<(), String> {
        if self.directory() || (self.regular() && self.links == 1) {
            Ok(())
        } else {
            Err("package has a symlink, hardlink or special member".into())
        }
    }
}

type Census = BTreeMap<String, Stamp>;

#[derive(Debug)]
struct Custody {
    path: PathBuf,
    directory: File,
    census: Census,
    members: BTreeMap<String, Member>,
}
impl Custody {
    fn bound(&self) -> Result<(), String> {
        let actual = open_root(&self.path)?;
        let expected = self.census.get("").ok_or("package root census absent")?;
        if Stamp::of(&actual.metadata().map_err(io)?) != *expected
            || Stamp::of(&self.directory.metadata().map_err(io)?) != *expected
        {
            return Err("package folder was replaced or changed".into());
        }
        Ok(())
    }
    fn unchanged(&self) -> Result<(), String> {
        self.bound()?;
        if scan(&self.directory)? != self.census {
            return Err("package inventory or first-observed metadata changed".into());
        }
        for (name, expected) in &self.members {
            if read_member(&self.directory, name, &self.census, None)? != *expected {
                return Err(format!("package bytes changed: {name}"));
            }
        }
        if scan(&self.directory)? != self.census {
            return Err("package inventory changed during verification".into());
        }
        self.bound()
    }
}

#[derive(Debug)]
pub(crate) struct Snapshot {
    stage: Custody,
    source: Option<Custody>,
    project: Value,
    administration: Value,
    project_id: String,
    identity: String,
    payload: BTreeMap<String, Member>,
}
impl Snapshot {
    pub(crate) fn root(&self) -> &Path {
        &self.stage.path
    }
    pub(crate) fn project_id(&self) -> &str {
        &self.project_id
    }
    pub(crate) fn administration(&self) -> &Value {
        &self.administration
    }
    pub(crate) fn project_record(&self) -> &Value {
        &self.project
    }
    /// SHA-256 of the exact tagmanifest bytes, not a reserialized object.
    pub(crate) fn identity(&self) -> &str {
        &self.identity
    }
    pub(crate) fn payload(&self) -> &BTreeMap<String, Member> {
        &self.payload
    }
    pub(crate) fn verify_unchanged(&self) -> Result<(), String> {
        self.stage.unchanged()
    }
    /// A recovered stage has no source claim: its durable intent belongs to
    /// the transaction owner. This never substitutes for verify_unchanged().
    pub(crate) fn source_unchanged(&self) -> Result<(), String> {
        self.source.as_ref().map_or(Ok(()), Custody::unchanged)
    }
}

fn io(error: std::io::Error) -> String {
    error.to_string()
}
fn system(action: &str) -> String {
    format!("{action}: {}", std::io::Error::last_os_error())
}
fn name_c(name: &str) -> Result<CString, String> {
    CString::new(name).map_err(|_| "package path contains NUL".into())
}
fn open_at(dir: &File, name: &str, flags: i32) -> Result<File, String> {
    let name = name_c(name)?;
    // SAFETY: the borrowed descriptor and NUL-terminated name remain live.
    let fd = unsafe { libc::openat(dir.as_raw_fd(), name.as_ptr(), flags) };
    if fd < 0 {
        Err(system("open package component without following links"))
    } else {
        Ok(unsafe { File::from_raw_fd(fd) })
    }
}
fn absolute(path: &Path) -> Result<PathBuf, String> {
    let path = if path.is_absolute() {
        path.to_path_buf()
    } else {
        std::env::current_dir().map_err(io)?.join(path)
    };
    if path
        .components()
        .any(|c| !matches!(c, Component::RootDir | Component::Normal(_)))
    {
        return Err("package path must use physical normal components".into());
    }
    Ok(path)
}
/// Open every ancestor through the preceding held descriptor. O_NOFOLLOW on
/// just the final pathname would leave an ancestor-swap escape.
fn open_root(path: &Path) -> Result<File, String> {
    let path = absolute(path)?;
    let mut directory = File::open("/").map_err(io)?;
    for part in path.components() {
        if let Component::Normal(name) = part {
            directory = open_at(
                &directory,
                name.to_str().ok_or("package path is not UTF-8")?,
                SAFE_READ | libc::O_DIRECTORY,
            )?;
        }
    }
    Ok(directory)
}

struct Listing(*mut libc::DIR);
impl Drop for Listing {
    fn drop(&mut self) {
        unsafe {
            libc::closedir(self.0);
        }
    }
}
#[cfg(target_os = "macos")]
fn errno() -> *mut libc::c_int {
    unsafe { libc::__error() }
}
#[cfg(not(target_os = "macos"))]
fn errno() -> *mut libc::c_int {
    unsafe { libc::__errno_location() }
}
fn names(directory: &File) -> Result<Vec<String>, String> {
    // A fresh open description avoids sharing/reusing readdir's offset.
    let fresh = open_at(directory, ".", SAFE_READ | libc::O_DIRECTORY)?;
    let fd = fresh.into_raw_fd();
    let raw = unsafe { libc::fdopendir(fd) };
    if raw.is_null() {
        let error = system("list package directory");
        unsafe {
            libc::close(fd);
        }
        return Err(error);
    }
    let listing = Listing(raw);
    let mut out = Vec::new();
    loop {
        unsafe {
            *errno() = 0;
        }
        let entry = unsafe { libc::readdir(listing.0) };
        if entry.is_null() {
            if unsafe { *errno() } != 0 {
                return Err(system("list package directory"));
            }
            break;
        }
        let name = unsafe { CStr::from_ptr((*entry).d_name.as_ptr()) }
            .to_str()
            .map_err(|_| "package member name is not UTF-8")?;
        if name != "." && name != ".." {
            out.push(name.to_owned());
        }
    }
    out.sort();
    Ok(out)
}
fn scan(root: &File) -> Result<Census, String> {
    fn walk(directory: &File, prefix: &str, out: &mut Census, depth: usize) -> Result<(), String> {
        if depth > 256 {
            return Err("package directory nesting exceeds safe traversal depth".into());
        }
        let first = Stamp::of(&directory.metadata().map_err(io)?);
        if !first.directory() {
            return Err("package directory is not plain".into());
        }
        out.insert(prefix.to_owned(), first.clone());
        for name in names(directory)? {
            let path = if prefix.is_empty() {
                name.clone()
            } else {
                format!("{prefix}/{name}")
            };
            let stamp = Stamp::at(directory, &name)?;
            stamp.plain()?;
            if stamp.directory() {
                let child = open_at(directory, &name, SAFE_READ | libc::O_DIRECTORY)?;
                if Stamp::of(&child.metadata().map_err(io)?) != stamp {
                    return Err("package directory changed while opening".into());
                }
                walk(&child, &path, out, depth + 1)?;
                if Stamp::at(directory, &name)? != stamp {
                    return Err("package directory changed while scanning".into());
                }
            } else {
                out.insert(path, stamp);
            }
        }
        if Stamp::of(&directory.metadata().map_err(io)?) != first {
            return Err("package directory changed while listing".into());
        }
        Ok(())
    }
    let mut out = BTreeMap::new();
    walk(root, "", &mut out, 0)?;
    Ok(out)
}
fn parts(path: &str) -> Result<Vec<&str>, String> {
    let parts: Vec<_> = path.split('/').collect();
    if parts
        .iter()
        .any(|p| p.is_empty() || *p == "." || *p == ".." || p.contains('\0'))
    {
        return Err("unsafe package relative path".into());
    }
    Ok(parts)
}
fn parent_at(root: &File, path: &str, census: Option<&Census>) -> Result<(File, String), String> {
    let parts = parts(path)?;
    let mut directory = root.try_clone().map_err(io)?;
    let mut prefix = String::new();
    for part in &parts[..parts.len() - 1] {
        if !prefix.is_empty() {
            prefix.push('/');
        }
        prefix.push_str(part);
        let next = open_at(&directory, part, SAFE_READ | libc::O_DIRECTORY)?;
        if let Some(census) = census {
            if Some(&Stamp::of(&next.metadata().map_err(io)?)) != census.get(&prefix) {
                return Err("package directory changed since first observation".into());
            }
        }
        directory = next;
    }
    Ok((directory, parts.last().unwrap().to_string()))
}
fn read_member(
    root: &File,
    path: &str,
    census: &Census,
    mut output: Option<&mut File>,
) -> Result<Member, String> {
    let (directory, name) = parent_at(root, path, Some(census))?;
    let expected = census
        .get(path)
        .ok_or("package member absent from first census")?;
    if !expected.regular() || expected.links != 1 {
        return Err("package member is not a regular single-link file".into());
    }
    if Stamp::at(&directory, &name)? != *expected {
        return Err("package member changed since first observation".into());
    }
    let mut input = open_at(&directory, &name, SAFE_READ)?;
    if Stamp::of(&input.metadata().map_err(io)?) != *expected {
        return Err("package member changed while opening".into());
    }
    let mut hash = Sha256::new();
    let mut bytes = 0u64;
    let mut buffer = [0u8; 65536];
    loop {
        let count = input.read(&mut buffer).map_err(io)?;
        if count == 0 {
            break;
        }
        hash.update(&buffer[..count]);
        if let Some(file) = &mut output {
            file.write_all(&buffer[..count]).map_err(io)?;
        }
        bytes = bytes
            .checked_add(count as u64)
            .ok_or("package byte count overflow")?;
        #[cfg(test)]
        if let Some(hook) = DURING_READ.with(|h| h.borrow_mut().take()) {
            hook(path);
        }
    }
    if bytes != expected.size
        || Stamp::of(&input.metadata().map_err(io)?) != *expected
        || Stamp::at(&directory, &name)? != *expected
    {
        return Err(format!("package member changed while reading: {path}"));
    }
    Ok(Member {
        sha256: format!("{:x}", hash.finalize()),
        bytes,
    })
}
// Value's ordinary map parser keeps only the final value for a repeated key.
// At an import envelope boundary that could erase a conflicting identity claim.
// This recursive reader rejects duplicates before any field is interpreted.
struct UniqueValue(Value);
impl<'de> Deserialize<'de> for UniqueValue {
    fn deserialize<D: Deserializer<'de>>(deserializer: D) -> Result<Self, D::Error> {
        struct UniqueVisitor;
        impl<'de> Visitor<'de> for UniqueVisitor {
            type Value = UniqueValue;
            fn expecting(&self, f: &mut std::fmt::Formatter) -> std::fmt::Result {
                f.write_str("JSON without duplicate object keys")
            }
            fn visit_unit<E: de::Error>(self) -> Result<Self::Value, E> {
                Ok(UniqueValue(Value::Null))
            }
            fn visit_bool<E: de::Error>(self, value: bool) -> Result<Self::Value, E> {
                Ok(UniqueValue(Value::Bool(value)))
            }
            fn visit_i64<E: de::Error>(self, value: i64) -> Result<Self::Value, E> {
                Ok(UniqueValue(Value::Number(value.into())))
            }
            fn visit_u64<E: de::Error>(self, value: u64) -> Result<Self::Value, E> {
                Ok(UniqueValue(Value::Number(value.into())))
            }
            fn visit_f64<E: de::Error>(self, value: f64) -> Result<Self::Value, E> {
                serde_json::Number::from_f64(value)
                    .map(|n| UniqueValue(Value::Number(n)))
                    .ok_or_else(|| E::custom("non-finite JSON number"))
            }
            fn visit_str<E: de::Error>(self, value: &str) -> Result<Self::Value, E> {
                Ok(UniqueValue(Value::String(value.to_owned())))
            }
            fn visit_string<E: de::Error>(self, value: String) -> Result<Self::Value, E> {
                Ok(UniqueValue(Value::String(value)))
            }
            fn visit_seq<A: SeqAccess<'de>>(
                self,
                mut sequence: A,
            ) -> Result<Self::Value, A::Error> {
                let mut values = Vec::new();
                while let Some(UniqueValue(value)) = sequence.next_element()? {
                    values.push(value);
                }
                Ok(UniqueValue(Value::Array(values)))
            }
            fn visit_map<A: MapAccess<'de>>(self, mut object: A) -> Result<Self::Value, A::Error> {
                let mut values = serde_json::Map::new();
                while let Some(key) = object.next_key::<String>()? {
                    if values.contains_key(&key) {
                        return Err(de::Error::custom("duplicate JSON object key"));
                    }
                    let UniqueValue(value) = object.next_value()?;
                    values.insert(key, value);
                }
                Ok(UniqueValue(Value::Object(values)))
            }
        }
        deserializer.deserialize_any(UniqueVisitor)
    }
}

/// Shared strict parser for operational package/journal/admin envelopes. The
/// caller retains the raw bytes as evidence; duplicate fields confer no state.
pub(crate) fn parse_json_unique(bytes: &[u8]) -> Result<Value, String> {
    serde_json::from_slice::<UniqueValue>(bytes)
        .map(|v| v.0)
        .map_err(|e| e.to_string())
}

fn json_member(custody: &Custody, path: &str) -> Result<Value, String> {
    let (directory, name) = parent_at(&custody.directory, path, Some(&custody.census))?;
    let mut input = open_at(&directory, &name, SAFE_READ)?;
    let expected = custody
        .census
        .get(path)
        .ok_or("package JSON member absent")?;
    if !expected.regular()
        || expected.links != 1
        || Stamp::of(&input.metadata().map_err(io)?) != *expected
    {
        return Err("package JSON member changed while opening".into());
    }
    let UniqueValue(value) = serde_json::from_reader::<_, UniqueValue>(&mut input)
        .map_err(|e| format!("invalid {path}: {e}"))?;
    if Stamp::of(&input.metadata().map_err(io)?) != *expected
        || Stamp::at(&directory, &name)? != *expected
    {
        return Err("package JSON member changed while reading".into());
    }
    Ok(value)
}
fn text_member(custody: &Custody, path: &str) -> Result<String, String> {
    let (directory, name) = parent_at(&custody.directory, path, Some(&custody.census))?;
    let mut input = open_at(&directory, &name, SAFE_READ)?;
    let expected = custody.census.get(path).ok_or("package tag absent")?;
    if !expected.regular()
        || expected.links != 1
        || Stamp::of(&input.metadata().map_err(io)?) != *expected
    {
        return Err("package tag changed while opening".into());
    }
    let mut text = String::new();
    input.read_to_string(&mut text).map_err(io)?;
    if Stamp::of(&input.metadata().map_err(io)?) != *expected
        || Stamp::at(&directory, &name)? != *expected
    {
        return Err("package tag changed while reading".into());
    }
    Ok(text)
}
fn manifest(
    custody: &Custody,
    name: &str,
    payload: bool,
) -> Result<BTreeMap<String, String>, String> {
    let text = text_member(custody, name)?;
    let mut out = BTreeMap::new();
    for line in text.split_terminator('\n') {
        let (hash, encoded) = line.split_once("  ").ok_or("malformed package manifest")?;
        if hash.len() != 64 || !hash.bytes().all(|b| b.is_ascii_hexdigit()) {
            return Err("invalid package checksum".into());
        }
        if encoded.contains('\r') {
            return Err("raw carriage return in package manifest path".into());
        }
        let mut decoded = String::new();
        let mut chars = encoded.chars();
        while let Some(c) = chars.next() {
            if c != '%' {
                decoded.push(c);
                continue;
            }
            let code = [
                chars.next().ok_or("bad manifest escape")?,
                chars.next().ok_or("bad manifest escape")?,
            ]
            .iter()
            .collect::<String>();
            decoded.push(match code.as_str() {
                "25" => '%',
                "0A" => '\n',
                "0D" => '\r',
                _ => return Err("unsafe manifest escape".into()),
            });
        }
        parts(&decoded)?;
        if decoded.starts_with("data/") != payload
            || (!payload && decoded.starts_with("tagmanifest-"))
        {
            return Err("invalid manifest member class".into());
        }
        if out
            .insert(decoded.clone(), hash.to_ascii_lowercase())
            .is_some()
        {
            return Err("duplicate package manifest path".into());
        }
        if custody.members.get(&decoded).map(|m| m.sha256.as_str())
            != Some(hash.to_ascii_lowercase().as_str())
        {
            return Err(format!("package checksum mismatch: {decoded}"));
        }
    }
    Ok(out)
}
fn validate(stage: Custody) -> Result<Snapshot, String> {
    for stamp in stage.census.values() {
        if stamp.mode & 0o077 != 0 || stamp.owner != unsafe { libc::geteuid() } {
            return Err("staged package is not private to its owner".into());
        }
    }
    let payload_manifest = manifest(&stage, "manifest-sha256.txt", true)?;
    let tag_manifest = manifest(&stage, "tagmanifest-sha256.txt", false)?;
    if tag_manifest
        .keys()
        .map(String::as_str)
        .collect::<std::collections::BTreeSet<_>>()
        != TAGS.iter().copied().collect()
    {
        return Err(
            "operational import requires the current administrative snapshot profile".into(),
        );
    }
    let mut expected: std::collections::BTreeSet<_> = payload_manifest.keys().cloned().collect();
    expected.extend(tag_manifest.into_keys());
    expected.insert("tagmanifest-sha256.txt".to_owned());
    if stage
        .members
        .keys()
        .cloned()
        .collect::<std::collections::BTreeSet<_>>()
        != expected
    {
        return Err("package inventory differs from manifests".into());
    }
    if ["data/.writer.lock", "data/captures/.capture.lock"]
        .iter()
        .any(|path| stage.census.contains_key(*path))
    {
        return Err("package payload contains an active owning control".into());
    }
    let mut payload = BTreeMap::new();
    for path in payload_manifest.keys() {
        let relative = path
            .strip_prefix("data/")
            .ok_or("payload member outside data")?;
        if matches!(relative, ".writer.lock" | "captures/.capture.lock") {
            return Err("package payload contains an active owning control".into());
        }
        payload.insert(relative.to_owned(), stage.members[path].clone());
    }
    let project = json_member(&stage, "data/project.json")?;
    let project_id = project["projectId"]
        .as_str()
        .filter(|id| !id.is_empty() && !id.chars().any(char::is_control))
        .ok_or("package project identity absent or invalid")?
        .to_owned();
    if project["format"] != "chirality.records-store.project" || project["formatVersion"] != "0.1" {
        return Err("package project record format/version unsupported".into());
    }
    let info = text_member(&stage, "bag-info.txt")?;
    let identifiers: Vec<_> = info
        .split_terminator('\n')
        .filter_map(|line| line.strip_prefix("External-Identifier: "))
        .collect();
    if identifiers != [project_id.as_str()] {
        return Err("bag-info project identity differs from payload".into());
    }
    let administration = json_member(&stage, ADMIN)?;
    if administration["format"] != "chirality.records-administration-snapshot"
        || administration["formatVersion"] != "0.1"
        || administration["projectId"] != project_id
        || administration["projectKey"] != crate::storage::key(&project_id)
        || !administration["events"].is_object()
        || administration["sequence"].as_u64().is_none()
    {
        return Err("administrative snapshot envelope identity/profile invalid".into());
    }
    let _ = json_member(&stage, "records-chain-heads.json")?;
    // The existing verifier supplies supported BagIt declaration and exact RS
    // chain-head-profile checks. No executable from the package is run.
    stage.unchanged()?;
    crate::records_export::verify(&stage.path)?;
    stage.unchanged()?;
    let identity = stage.members["tagmanifest-sha256.txt"].sha256.clone();
    Ok(Snapshot {
        stage,
        source: None,
        project,
        administration,
        project_id,
        identity,
        payload,
    })
}

fn custody(path: &Path) -> Result<Custody, String> {
    let path = absolute(path)?;
    let directory = open_root(&path)?;
    let census = scan(&directory)?;
    let mut members = BTreeMap::new();
    for (name, stamp) in &census {
        if stamp.regular() {
            members.insert(name.clone(), read_member(&directory, name, &census, None)?);
        }
    }
    let custody = Custody {
        path,
        directory,
        census,
        members,
    };
    custody.unchanged()?;
    Ok(custody)
}

/// Reopen an already private staged package. Original-source association and
/// publication intent must be checked by the transaction owner on recovery.
pub(crate) fn inspect(snapshot_path: &Path) -> Result<Snapshot, String> {
    validate(custody(snapshot_path)?)
}

/// Stream an unchanged package into a new absent private folder. On a failure
/// after creation, retain the private partial stage for the transaction owner;
/// never clean up through a possibly replaced pathname or change the source.
pub(crate) fn snapshot(source: &Path, destination: &Path) -> Result<Snapshot, String> {
    let source = custody(source)?;
    let destination = absolute(destination)?;
    if destination.starts_with(&source.path) {
        return Err("snapshot destination must be outside the source package".into());
    }
    let parent_path = destination
        .parent()
        .ok_or("snapshot destination has no parent")?;
    let parent = open_root(parent_path)?;
    let name = destination
        .file_name()
        .and_then(OsStr::to_str)
        .ok_or("snapshot name is not UTF-8")?;
    let destination_name = name_c(name)?;
    if unsafe { libc::mkdirat(parent.as_raw_fd(), destination_name.as_ptr(), 0o700) } != 0 {
        return Err(system(
            "create new private package stage; nothing overwritten",
        ));
    }
    let result = (|| {
        let stage_root = open_at(&parent, name, SAFE_READ | libc::O_DIRECTORY)?;
        #[cfg(test)]
        if let Some(hook) = AFTER_CENSUS.with(|h| h.borrow_mut().take()) {
            hook();
        }
        let mut copied = BTreeMap::new();
        for (path, stamp) in &source.census {
            if path.is_empty() {
                continue;
            }
            let (directory, name) = parent_at(&stage_root, path, None)?;
            let c_name = name_c(&name)?;
            if stamp.directory() {
                if unsafe { libc::mkdirat(directory.as_raw_fd(), c_name.as_ptr(), 0o700) } != 0 {
                    return Err(system(
                        "create package directory; conflicting or aliased name",
                    ));
                }
            } else {
                let fd = unsafe {
                    libc::openat(
                        directory.as_raw_fd(),
                        c_name.as_ptr(),
                        libc::O_WRONLY
                            | libc::O_CREAT
                            | libc::O_EXCL
                            | libc::O_NOFOLLOW
                            | libc::O_NONBLOCK
                            | libc::O_CLOEXEC,
                        0o600,
                    )
                };
                if fd < 0 {
                    return Err(system("create package file; conflicting or aliased name"));
                }
                let mut output = unsafe { File::from_raw_fd(fd) };
                let member =
                    read_member(&source.directory, path, &source.census, Some(&mut output))?;
                output.sync_all().map_err(io)?;
                if source.members.get(path) != Some(&member) {
                    return Err("source bytes changed since first observation".into());
                }
                copied.insert(path.clone(), member);
            }
        }
        source.unchanged()?;
        let stage = custody(&destination)?;
        if stage.census.get("") != Some(&Stamp::of(&stage_root.metadata().map_err(io)?)) {
            return Err("private stage folder was replaced during copy".into());
        }
        if copied != stage.members
            || source
                .census
                .iter()
                .map(|(p, s)| (p, s.directory()))
                .collect::<Vec<_>>()
                != stage
                    .census
                    .iter()
                    .map(|(p, s)| (p, s.directory()))
                    .collect::<Vec<_>>()
        {
            return Err("staged bytes or names differ from the source package".into());
        }
        // Deepest directories first; the parent link is synced last.
        for (path, stamp) in stage.census.iter().rev() {
            if stamp.directory() {
                if path.is_empty() {
                    stage.directory.sync_all().map_err(io)?;
                } else {
                    let (dir, name) = parent_at(&stage.directory, path, Some(&stage.census))?;
                    open_at(&dir, &name, SAFE_READ | libc::O_DIRECTORY)?
                        .sync_all()
                        .map_err(io)?;
                }
            }
        }
        parent.sync_all().map_err(io)?;
        let mut snapshot = validate(stage)?;
        source.unchanged()?;
        snapshot.source = Some(source);
        Ok(snapshot)
    })();
    result.map_err(|error| {
        format!(
            "package snapshot incomplete at {}; private stage retained: {error}",
            destination.display()
        )
    })
}

/// Complete coherent hashes for a retained payload. Only actual plain owning
/// lock files are excluded; similarly named connector evidence stays present.
pub(crate) fn payload_inventory(root: &Path) -> Result<BTreeMap<String, Member>, String> {
    let root = absolute(root)?;
    if optional_root(&root)?.is_none() {
        return Ok(BTreeMap::new());
    }
    let mut held = custody(&root)?;
    for control in [".writer.lock", "captures/.capture.lock"] {
        if held
            .census
            .get(control)
            .is_some_and(|stamp| !stamp.regular() || stamp.links != 1)
        {
            return Err("owning control is not a regular single-link file".into());
        }
    }
    held.members.remove(".writer.lock");
    held.members.remove("captures/.capture.lock");
    Ok(held.members)
}

fn optional_root(path: &Path) -> Result<Option<File>, String> {
    let path = absolute(path)?;
    let mut directory = File::open("/").map_err(io)?;
    for part in path.components() {
        if let Component::Normal(name) = part {
            let name = name_c(name.to_str().ok_or("owning path is not UTF-8")?)?;
            let fd = unsafe {
                libc::openat(
                    directory.as_raw_fd(),
                    name.as_ptr(),
                    SAFE_READ | libc::O_DIRECTORY,
                )
            };
            if fd < 0 {
                let error = std::io::Error::last_os_error();
                if error.kind() == std::io::ErrorKind::NotFound {
                    return Ok(None);
                }
                return Err(format!("open owning directory without links: {error}"));
            }
            directory = unsafe { File::from_raw_fd(fd) };
        }
    }
    Ok(Some(directory))
}

/// Create missing owning directories privately through held ancestors. Existing
/// directories are never chmodded. Reflush every ancestor link on retries too:
/// an existing folder may survive an earlier uncertain directory publication.
fn ensure_root(path: &Path) -> Result<File, String> {
    let path = absolute(path)?;
    let mut directory = File::open("/").map_err(io)?;
    for part in path.components() {
        if let Component::Normal(name) = part {
            let name = name.to_str().ok_or("owning path is not UTF-8")?;
            let c_name = name_c(name)?;
            let mut fd = unsafe {
                libc::openat(
                    directory.as_raw_fd(),
                    c_name.as_ptr(),
                    SAFE_READ | libc::O_DIRECTORY,
                )
            };
            if fd < 0 {
                let error = std::io::Error::last_os_error();
                if error.kind() != std::io::ErrorKind::NotFound {
                    return Err(format!("open owning directory: {error}"));
                }
                if unsafe { libc::mkdirat(directory.as_raw_fd(), c_name.as_ptr(), 0o700) } != 0 {
                    let error = std::io::Error::last_os_error();
                    if error.kind() != std::io::ErrorKind::AlreadyExists {
                        return Err(format!("create private owning directory: {error}"));
                    }
                }
                fd = unsafe {
                    libc::openat(
                        directory.as_raw_fd(),
                        c_name.as_ptr(),
                        SAFE_READ | libc::O_DIRECTORY,
                    )
                };
                if fd < 0 {
                    return Err(system("open newly created owning directory"));
                }
            }
            let child = unsafe { File::from_raw_fd(fd) };
            if !names(&directory)?.iter().any(|actual| actual == name) {
                return Err(
                    "owning directory name aliases another spelling on this filesystem".into(),
                );
            }
            child.sync_all().map_err(io)?;
            directory.sync_all().map_err(io)?;
            directory = child;
        }
    }
    Ok(directory)
}

fn directory_binding(path: &Path, held: &File) -> Result<(), String> {
    let current = open_root(path)?.metadata().map_err(io)?;
    let held = held.metadata().map_err(io)?;
    if current.dev() != held.dev() || current.ino() != held.ino() {
        return Err("owning directory pathname was replaced".into());
    }
    Ok(())
}
fn exists_at(directory: &File, name: &str) -> Result<bool, String> {
    let name = name_c(name)?;
    let mut raw = std::mem::MaybeUninit::<libc::stat>::uninit();
    if unsafe {
        libc::fstatat(
            directory.as_raw_fd(),
            name.as_ptr(),
            raw.as_mut_ptr(),
            libc::AT_SYMLINK_NOFOLLOW,
        )
    } == 0
    {
        Ok(true)
    } else {
        let error = std::io::Error::last_os_error();
        if error.kind() == std::io::ErrorKind::NotFound {
            Ok(false)
        } else {
            Err(error.to_string())
        }
    }
}
fn one_member(directory: &File, name: &str) -> Result<(File, Stamp, Member), String> {
    if !names(directory)?.iter().any(|actual| actual == name) {
        return Err("owning member name aliases another spelling on this filesystem".into());
    }
    let stamp = Stamp::at(directory, name)?;
    if !stamp.regular() || stamp.links != 1 {
        return Err("owning member is not regular and single-link".into());
    }
    let mut file = open_at(directory, name, SAFE_READ)?;
    if Stamp::of(&file.metadata().map_err(io)?) != stamp {
        return Err("owning member changed while opening".into());
    }
    let mut hash = Sha256::new();
    let mut bytes = 0u64;
    let mut buffer = [0; 65536];
    loop {
        let count = file.read(&mut buffer).map_err(io)?;
        if count == 0 {
            break;
        }
        hash.update(&buffer[..count]);
        bytes = bytes
            .checked_add(count as u64)
            .ok_or("owning member byte count overflow")?;
    }
    if bytes != stamp.size
        || Stamp::of(&file.metadata().map_err(io)?) != stamp
        || Stamp::at(directory, name)? != stamp
    {
        return Err("owning member changed while reading".into());
    }
    file.seek(SeekFrom::Start(0)).map_err(io)?;
    Ok((
        file,
        stamp,
        Member {
            sha256: format!("{:x}", hash.finalize()),
            bytes,
        },
    ))
}
fn exclusive_rename(from_dir: &File, from: &str, to_dir: &File, to: &str) -> Result<(), String> {
    let from = name_c(from)?;
    let to = name_c(to)?;
    #[cfg(target_os = "macos")]
    let result = unsafe {
        libc::renameatx_np(
            from_dir.as_raw_fd(),
            from.as_ptr(),
            to_dir.as_raw_fd(),
            to.as_ptr(),
            libc::RENAME_EXCL,
        )
    };
    #[cfg(target_os = "linux")]
    let result = unsafe {
        libc::renameat2(
            from_dir.as_raw_fd(),
            from.as_ptr(),
            to_dir.as_raw_fd(),
            to.as_ptr(),
            libc::RENAME_NOREPLACE,
        )
    };
    #[cfg(not(any(target_os = "macos", target_os = "linux")))]
    return Err("exclusive package member publication unavailable".into());
    #[cfg(any(target_os = "macos", target_os = "linux"))]
    if result != 0 {
        return Err(system(
            "exclusive package member publication; target may be present",
        ));
    }
    Ok(())
}
fn exact_existing(directory: &File, name: &str, expected: &Member) -> Result<bool, String> {
    if !exists_at(directory, name)? {
        return Ok(false);
    }
    let (file, _, observed) = one_member(directory, name)?;
    if observed != *expected {
        return Err("existing member differs; nothing overwritten".into());
    }
    file.sync_all().map_err(io)?;
    directory.sync_all().map_err(io)?;
    Ok(true)
}

/// Restore one exact staged file. A partial scratch is resumed only after its
/// complete existing prefix matches the held source. Conflicting scratch and
/// destination bytes are preserved. The caller owns journal/admission locks.
pub(crate) fn restore_member(
    source: &Path,
    target_root: &Path,
    relative: &str,
    scratch: &Path,
    expected: &Member,
) -> Result<bool, String> {
    parts(relative)?;
    let source = absolute(source)?;
    let target_root = absolute(target_root)?;
    let scratch = absolute(scratch)?;
    if scratch.starts_with(&target_root) || scratch == source {
        return Err("unpublished scratch must be outside the live payload and source".into());
    }
    let source_parent = source.parent().ok_or("source file has no parent")?;
    let source_name = source
        .file_name()
        .and_then(OsStr::to_str)
        .ok_or("source name is not UTF-8")?;
    let source_dir = open_root(source_parent)?;
    let (mut input, source_stamp, observed) = one_member(&source_dir, source_name)?;
    if observed != *expected {
        return Err("staged source differs from expected exact bytes".into());
    }
    let target = target_root.join(relative);
    if target == source {
        return Err("restoration target is the staged source".into());
    }
    let target_parent = target.parent().ok_or("target file has no parent")?;
    let target_name = target
        .file_name()
        .and_then(OsStr::to_str)
        .ok_or("target name is not UTF-8")?;
    let target_dir = ensure_root(target_parent)?;
    if exact_existing(&target_dir, target_name, expected)? {
        directory_binding(target_parent, &target_dir)?;
        return Ok(false);
    }
    let scratch_parent = scratch.parent().ok_or("scratch has no parent")?;
    let scratch_name = scratch
        .file_name()
        .and_then(OsStr::to_str)
        .ok_or("scratch name is not UTF-8")?;
    let scratch_dir = ensure_root(scratch_parent)?;
    let existed = exists_at(&scratch_dir, scratch_name)?;
    let scratch_c = name_c(scratch_name)?;
    let flags = libc::O_RDWR
        | libc::O_NOFOLLOW
        | libc::O_NONBLOCK
        | libc::O_CLOEXEC
        | if existed {
            0
        } else {
            libc::O_CREAT | libc::O_EXCL
        };
    let fd = unsafe { libc::openat(scratch_dir.as_raw_fd(), scratch_c.as_ptr(), flags, 0o600) };
    if fd < 0 {
        return Err(system("open unpublished member scratch"));
    }
    let mut output = unsafe { File::from_raw_fd(fd) };
    let first = Stamp::of(&output.metadata().map_err(io)?);
    if !first.regular()
        || first.links != 1
        || first.owner != unsafe { libc::geteuid() }
        || first.mode & 0o077 != 0
        || first.size > expected.bytes
        || Stamp::at(&scratch_dir, scratch_name)? != first
    {
        return Err(
            "unpublished scratch is not an unchanged private regular prefix; retained".into(),
        );
    }
    let mut source_bytes = [0u8; 65536];
    let mut scratch_bytes = [0u8; 65536];
    let mut left = first.size;
    while left != 0 {
        let count = left.min(source_bytes.len() as u64) as usize;
        input.read_exact(&mut source_bytes[..count]).map_err(io)?;
        output.read_exact(&mut scratch_bytes[..count]).map_err(io)?;
        if source_bytes[..count] != scratch_bytes[..count] {
            return Err(
                "unpublished scratch differs from source prefix; retained unchanged".into(),
            );
        }
        left -= count as u64;
    }
    if Stamp::of(&output.metadata().map_err(io)?) != first
        || Stamp::at(&scratch_dir, scratch_name)? != first
    {
        return Err("unpublished scratch changed during prefix verification; retained".into());
    }
    loop {
        let count = input.read(&mut source_bytes).map_err(io)?;
        if count == 0 {
            break;
        }
        output.write_all(&source_bytes[..count]).map_err(io)?;
        #[cfg(test)]
        if STOP_RESTORE.with(|flag| flag.replace(false)) {
            output.sync_all().map_err(io)?;
            scratch_dir.sync_all().map_err(io)?;
            return Err("member restoration interrupted after scratch write (injected)".into());
        }
    }
    output.sync_all().map_err(io)?;
    scratch_dir.sync_all().map_err(io)?;
    if Stamp::of(&input.metadata().map_err(io)?) != source_stamp
        || Stamp::at(&source_dir, source_name)? != source_stamp
    {
        return Err("staged source changed while restoring; unpublished scratch retained".into());
    }
    directory_binding(source_parent, &source_dir)?;
    let (_, completed_stamp, completed) = one_member(&scratch_dir, scratch_name)?;
    if completed != *expected || Stamp::of(&output.metadata().map_err(io)?) != completed_stamp {
        return Err("unpublished restored copy does not verify; retained".into());
    }
    directory_binding(target_parent, &target_dir)?;
    directory_binding(scratch_parent, &scratch_dir)?;
    if let Err(error) = exclusive_rename(&scratch_dir, scratch_name, &target_dir, target_name) {
        if exact_existing(&target_dir, target_name, expected)? {
            directory_binding(target_parent, &target_dir)?;
            directory_binding(scratch_parent, &scratch_dir)?;
            return Ok(false);
        }
        return Err(error);
    }
    // Once rename was attempted, errors are never treated as proof of rollback.
    let published = (|| {
        #[cfg(test)]
        if FAIL_PUBLICATION_SYNC.with(|flag| flag.replace(false)) {
            return Err("directory sync failed after member publication (injected)".into());
        }
        target_dir.sync_all().map_err(io)?;
        scratch_dir.sync_all().map_err(io)?;
        if !exact_existing(&target_dir, target_name, expected)? {
            return Err("published member absent on readback".into());
        }
        directory_binding(target_parent, &target_dir)?;
        directory_binding(scratch_parent, &scratch_dir)?;
        Ok(true)
    })();
    published.map_err(|error: String| format!("member publication durability uncertain at {}; reconcile existing bytes before retry: {error}", target.display()))
}

/// Publish a complete small control once, or durably reconcile exact existing
/// bytes. Partial temporary bytes never become a JSON control at the final name.
pub(crate) fn create_or_match(path: &Path, bytes: &[u8]) -> Result<(), String> {
    create_control_in(path, bytes, None)
}

/// Publish an import control with unpublished bytes kept in an explicit private
/// staging directory. The caller places staging outside the whole journal and
/// payload, on the same filesystem. Failed/partial temporaries are retained
/// there, so they cannot poison either strict final inventory on recovery.
pub(crate) fn create_or_match_staged(
    path: &Path,
    bytes: &[u8],
    staging: &Path,
) -> Result<(), String> {
    create_control_in(path, bytes, Some(staging))
}

fn create_control_in(path: &Path, bytes: &[u8], staging: Option<&Path>) -> Result<(), String> {
    let path = absolute(path)?;
    let parent = path.parent().ok_or("control has no parent")?;
    let name = path
        .file_name()
        .and_then(OsStr::to_str)
        .ok_or("control name is not UTF-8")?;
    let staging_path = match staging {
        Some(staging) => {
            let staging = absolute(staging)?;
            if staging.starts_with(parent) || parent.starts_with(&staging) {
                return Err(
                    "control staging must be separate from the final journal/payload directory"
                        .into(),
                );
            }
            staging
        }
        None => parent.to_path_buf(),
    };
    let directory = ensure_root(parent)?;
    let expected = Member {
        sha256: crate::util::sha256_hex(bytes),
        bytes: bytes.len() as u64,
    };
    let temporary_directory = ensure_root(&staging_path)?;
    if staging.is_some() {
        let metadata = temporary_directory.metadata().map_err(io)?;
        if metadata.uid() != unsafe { libc::geteuid() } || metadata.mode() & 0o077 != 0 {
            return Err("control staging is not private to its owner".into());
        }
    }
    if exact_existing(&directory, name, &expected)? {
        // Reconcile both sides of a previously uncertain cross-directory
        // rename, including the unpublished staging link's removal.
        temporary_directory.sync_all().map_err(io)?;
        directory_binding(parent, &directory)?;
        directory_binding(&staging_path, &temporary_directory)?;
        return Ok(());
    }
    let temporary = format!(".{}.{}.tmp", name, crate::util::opaque_id("")?);
    let c_name = name_c(&temporary)?;
    let fd = unsafe {
        libc::openat(
            temporary_directory.as_raw_fd(),
            c_name.as_ptr(),
            libc::O_WRONLY | libc::O_CREAT | libc::O_EXCL | libc::O_NOFOLLOW | libc::O_CLOEXEC,
            0o600,
        )
    };
    if fd < 0 {
        return Err(system("create private control temporary"));
    }
    let mut file = unsafe { File::from_raw_fd(fd) };
    #[cfg(test)]
    if staging.is_some()
        && FAIL_CONTROL_BEFORE_PUBLISH.with(|target| {
            let mut target = target.borrow_mut();
            if target.as_ref() == Some(&path) {
                target.take();
                true
            } else {
                false
            }
        })
    {
        let prefix = bytes.len().div_ceil(2);
        file.write_all(&bytes[..prefix]).map_err(io)?;
        file.sync_all().map_err(io)?;
        temporary_directory.sync_all().map_err(io)?;
        return Err(format!("control interrupted before publication at {}; partial temporary retained in {} (injected)", path.display(), staging_path.display()));
    }
    file.write_all(bytes).map_err(io)?;
    file.sync_all().map_err(io)?;
    let (_, stamp, observed) = one_member(&temporary_directory, &temporary)?;
    if observed != expected || Stamp::of(&file.metadata().map_err(io)?) != stamp {
        return Err("private control temporary differs before publication; retained".into());
    }
    temporary_directory.sync_all().map_err(io)?;
    directory_binding(parent, &directory)?;
    directory_binding(&staging_path, &temporary_directory)?;
    if let Err(error) = exclusive_rename(&temporary_directory, &temporary, &directory, name) {
        if exact_existing(&directory, name, &expected)? {
            temporary_directory.sync_all().map_err(io)?;
            directory_binding(parent, &directory)?;
            directory_binding(&staging_path, &temporary_directory)?;
            return Ok(());
        }
        return Err(error);
    }
    let result = (|| {
        #[cfg(test)]
        if FAIL_PUBLICATION_SYNC.with(|flag| flag.replace(false)) {
            return Err("directory sync failed after control publication (injected)".into());
        }
        directory.sync_all().map_err(io)?;
        temporary_directory.sync_all().map_err(io)?;
        if !exact_existing(&directory, name, &expected)? {
            return Err("published control absent".into());
        }
        directory_binding(parent, &directory)?;
        directory_binding(&staging_path, &temporary_directory)
    })();
    result.map_err(|error| {
        format!(
            "control publication durability uncertain at {}; re-read before retry: {error}",
            path.display()
        )
    })
}

#[cfg(test)]
pub(crate) fn fail_control_before_publish_for_test(path: Option<PathBuf>) {
    FAIL_CONTROL_BEFORE_PUBLISH.with(|target| *target.borrow_mut() = path);
}

/// Replace only a caller-authorized mutable association control, never a
/// package/payload member. The transaction owner binds both exact versions
/// and holds its association lock. POSIX rename has no inode compare-and-swap: a
/// noncooperating writer in the final compare/rename interval cannot be excluded.
/// Held-parent rebinding and pre/post descriptor checks expose observed races.
pub(crate) fn replace_control(
    path: &Path,
    expected: &[u8],
    replacement: &[u8],
) -> Result<(), String> {
    let path = absolute(path)?;
    if !path.ends_with(Path::new(crate::records_store::PROJECT_LINK)) {
        return Err("mutable association replacement is limited to .chirality/project.json".into());
    }
    let parent = path.parent().ok_or("association control has no parent")?;
    let name = path
        .file_name()
        .and_then(OsStr::to_str)
        .ok_or("association control name is not UTF-8")?;
    let directory = open_root(parent)?;
    let old_identity = Member {
        sha256: crate::util::sha256_hex(expected),
        bytes: expected.len() as u64,
    };
    let new_identity = Member {
        sha256: crate::util::sha256_hex(replacement),
        bytes: replacement.len() as u64,
    };
    let (mut original, first, observed) = one_member(&directory, name)?;
    if observed == new_identity {
        original.sync_all().map_err(io)?;
        directory.sync_all().map_err(io)?;
        return directory_binding(parent, &directory);
    }
    if observed != old_identity {
        return Err(
            "association control differs from the confirmed original; nothing replaced".into(),
        );
    }
    let temporary = format!(".{}.{}.tmp", name, crate::util::opaque_id("")?);
    let from = name_c(&temporary)?;
    let to = name_c(name)?;
    let fd = unsafe {
        libc::openat(
            directory.as_raw_fd(),
            from.as_ptr(),
            libc::O_WRONLY | libc::O_CREAT | libc::O_EXCL | libc::O_NOFOLLOW | libc::O_CLOEXEC,
            0o600,
        )
    };
    if fd < 0 {
        return Err(system("create private association temporary"));
    }
    let mut file = unsafe { File::from_raw_fd(fd) };
    file.write_all(replacement).map_err(io)?;
    file.sync_all().map_err(io)?;
    #[cfg(test)]
    if let Some(hook) = BEFORE_CONTROL_REPLACE.with(|h| h.borrow_mut().take()) {
        hook();
    }
    let (_, current, current_bytes) = one_member(&directory, name)?;
    if current != first
        || current_bytes != old_identity
        || Stamp::of(&original.metadata().map_err(io)?) != first
    {
        return Err("association control changed before publication; original and private temporary retained".into());
    }
    directory_binding(parent, &directory)?;
    if unsafe {
        libc::renameat(
            directory.as_raw_fd(),
            from.as_ptr(),
            directory.as_raw_fd(),
            to.as_ptr(),
        )
    } != 0
    {
        return Err(system(
            "association control publication uncertain; re-read before retry",
        ));
    }
    let result = (|| {
        #[cfg(test)]
        if FAIL_PUBLICATION_SYNC.with(|flag| flag.replace(false)) {
            return Err("directory sync failed after association publication (injected)".into());
        }
        directory.sync_all().map_err(io)?;
        if !exact_existing(&directory, name, &new_identity)? {
            return Err("replacement association absent on readback".into());
        }
        // The original descriptor survives unlink; ordinary replacement changes
        // its link count/ctime. Its exact contents and modification time must
        // still be those observed before publication.
        let after = Stamp::of(&original.metadata().map_err(io)?);
        if after.device != first.device
            || after.inode != first.inode
            || after.modified != first.modified
            || after.size != first.size
        {
            return Err("original association changed during replacement".into());
        }
        let mut buffer = [0u8; 65536];
        let mut offset = 0usize;
        original.seek(SeekFrom::Start(0)).map_err(io)?;
        loop {
            let count = original.read(&mut buffer).map_err(io)?;
            if count == 0 {
                break;
            }
            if expected.get(offset..offset + count) != Some(&buffer[..count]) {
                return Err("original association bytes changed during replacement".into());
            }
            offset += count;
        }
        if offset != expected.len() {
            return Err("original association length changed during replacement".into());
        }
        directory_binding(parent, &directory)
    })();
    result.map_err(|error| {
        format!(
            "association publication durability uncertain at {}; re-read before retry: {error}",
            path.display()
        )
    })
}

#[cfg(test)]
thread_local! {
    static FAIL_CONTROL_BEFORE_PUBLISH: std::cell::RefCell<Option<PathBuf>> = const { std::cell::RefCell::new(None) };
    static BEFORE_CONTROL_REPLACE: std::cell::RefCell<Option<Box<dyn FnOnce()>>> = const { std::cell::RefCell::new(None) };
    static FAIL_PUBLICATION_SYNC: std::cell::Cell<bool> = const { std::cell::Cell::new(false) };
    static STOP_RESTORE: std::cell::Cell<bool> = const { std::cell::Cell::new(false) };
    static AFTER_CENSUS: std::cell::RefCell<Option<Box<dyn FnOnce()>>> = const { std::cell::RefCell::new(None) };
    static DURING_READ: std::cell::RefCell<Option<Box<dyn FnOnce(&str)>>> = const { std::cell::RefCell::new(None) };
}
#[cfg(test)]
#[path = "records_package_tests.rs"]
mod tests;
