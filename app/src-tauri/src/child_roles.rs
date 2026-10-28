//! Bounded 0.160.0 native-name observations and App-owned immutable child files.
//! Absence is scoped to one reading. It is never a lock on later native inputs.
use crate::role_supply::{content, Composition, Guidance, Role};
use serde_json::{json, Value};
use std::{
    collections::{BTreeMap, BTreeSet},
    ffi::{CStr, CString},
    fs::File,
    io::{Read, Write},
    os::{
        fd::{AsRawFd, FromRawFd},
        unix::fs::MetadataExt,
    },
    path::{Component, Path, PathBuf},
};
const LIMIT: &str =
    "Native child roles withheld: configuration origins or source currency unavailable";
const CONTROLS: &[&str] = &[
    "enabled",
    "max_concurrent_threads_per_session",
    "max_depth",
    "default_subagent_model",
    "default_subagent_reasoning_effort",
    "job_max_runtime_seconds",
    "interrupt_message_enabled",
];
const MAX_SOURCE: u64 = 8 * 1024 * 1024;
#[derive(Default)]
struct Observed {
    paths: BTreeMap<String, Value>,
    steps: usize,
    bytes: usize,
    started: Option<std::time::Instant>,
}
impl Observed {
    fn tick(&mut self, bytes: usize) -> Result<(), String> {
        let started = self.started.get_or_insert_with(std::time::Instant::now);
        self.steps += 1;
        self.bytes = self.bytes.checked_add(bytes).ok_or_else(unavailable)?;
        if self.steps > 8192
            || self.bytes > 16 * 1024 * 1024
            || started.elapsed() > std::time::Duration::from_millis(500)
        {
            return Err(unavailable());
        }
        Ok(())
    }
    fn insert(&mut self, key: String, value: Value) {
        self.paths.insert(key, value);
    }
}

fn unavailable() -> String {
    LIMIT.into()
}
fn at(parent: &File, name: &str, flags: i32) -> Result<File, String> {
    let name = CString::new(name).map_err(|_| unavailable())?;
    let fd = unsafe {
        libc::openat(
            parent.as_raw_fd(),
            name.as_ptr(),
            flags | libc::O_NOFOLLOW | libc::O_NONBLOCK | libc::O_CLOEXEC,
            0o600,
        )
    };
    if fd < 0 {
        Err(unavailable())
    } else {
        Ok(unsafe { File::from_raw_fd(fd) })
    }
}
fn id(file: &File) -> Result<(u64, u64), String> {
    let m = file.metadata().map_err(|_| unavailable())?;
    Ok((m.dev(), m.ino()))
}
fn stamp(file: &File) -> Result<Value, String> {
    let m = file.metadata().map_err(|_| unavailable())?;
    Ok(json!([
        m.dev(),
        m.ino(),
        m.len(),
        m.mtime(),
        m.mtime_nsec(),
        m.ctime(),
        m.ctime_nsec(),
        m.mode(),
        m.nlink()
    ]))
}
fn names(dir: &File) -> Result<Vec<String>, String> {
    let dot = CString::new(".").unwrap();
    let fd = unsafe {
        libc::openat(
            dir.as_raw_fd(),
            dot.as_ptr(),
            libc::O_RDONLY | libc::O_DIRECTORY | libc::O_NOFOLLOW | libc::O_CLOEXEC,
        )
    };
    if fd < 0 {
        return Err(unavailable());
    }
    let stream = unsafe { libc::fdopendir(fd) };
    if stream.is_null() {
        unsafe { libc::close(fd) };
        return Err(unavailable());
    }
    let result = (|| {
        let mut names = vec![];
        loop {
            #[cfg(target_os = "macos")]
            unsafe {
                *libc::__error() = 0;
            }
            #[cfg(target_os = "linux")]
            unsafe {
                *libc::__errno_location() = 0;
            }
            let entry = unsafe { libc::readdir(stream) };
            if entry.is_null() {
                if std::io::Error::last_os_error().raw_os_error() != Some(0) {
                    return Err(unavailable());
                }
                break;
            }
            let name = unsafe { CStr::from_ptr((*entry).d_name.as_ptr()) }
                .to_str()
                .map_err(|_| unavailable())?
                .to_owned();
            if name != "." && name != ".." {
                names.push(name);
                if names.len() > 4096 {
                    return Err(unavailable());
                }
            }
        }
        names.sort();
        Ok(names)
    })();
    unsafe { libc::closedir(stream) };
    result
}
fn metadata_at(dir: &File, name: &str) -> Result<Option<libc::stat>, String> {
    let name = CString::new(name).map_err(|_| unavailable())?;
    let mut m = std::mem::MaybeUninit::uninit();
    if unsafe {
        libc::fstatat(
            dir.as_raw_fd(),
            name.as_ptr(),
            m.as_mut_ptr(),
            libc::AT_SYMLINK_NOFOLLOW,
        )
    } < 0
    {
        if std::io::Error::last_os_error().kind() == std::io::ErrorKind::NotFound {
            Ok(None)
        } else {
            Err(unavailable())
        }
    } else {
        Ok(Some(unsafe { m.assume_init() }))
    }
}
fn directory(path: &Path, observed: &mut Observed) -> Result<Option<File>, String> {
    if !path.is_absolute() || path.components().count() > 128 {
        return Err(unavailable());
    }
    let mut file = File::open("/").map_err(|_| unavailable())?;
    let mut prefix = PathBuf::from("/");
    let mut absent = false;
    for component in path.components() {
        match component {
            Component::RootDir => {}
            Component::Normal(name) => {
                observed.tick(0)?;
                let name = name.to_str().ok_or_else(unavailable)?;
                prefix.push(name);
                if absent {
                    continue;
                }
                let parent = id(&file)?;
                match metadata_at(&file, name)? {
                    None => {
                        observed.insert(
                            prefix.to_string_lossy().into(),
                            json!({"absentUnder":parent}),
                        );
                        absent = true;
                    }
                    Some(m) if m.st_mode & libc::S_IFMT == libc::S_IFDIR => {
                        let next = at(&file, name, libc::O_RDONLY | libc::O_DIRECTORY)?;
                        if id(&next)? != (m.st_dev as u64, m.st_ino as u64) {
                            return Err(unavailable());
                        }
                        observed.insert(
                            prefix.to_string_lossy().into(),
                            json!({"directory":id(&next)?}),
                        );
                        file = next;
                    }
                    _ => return Err(unavailable()),
                }
            }
            _ => return Err(unavailable()),
        }
    }
    Ok((!absent).then_some(file))
}
fn bytes_at(dir: &File, name: &str) -> Result<(Vec<u8>, Value), String> {
    let mut file = at(dir, name, libc::O_RDONLY)?;
    let m = file.metadata().map_err(|_| unavailable())?;
    if !m.is_file() || m.nlink() != 1 || m.len() > MAX_SOURCE {
        return Err(unavailable());
    }
    let before = stamp(&file)?;
    let mut bytes = vec![];
    (&mut file)
        .take(MAX_SOURCE + 1)
        .read_to_end(&mut bytes)
        .map_err(|_| unavailable())?;
    if bytes.len() as u64 > MAX_SOURCE || stamp(&file)? != before {
        return Err(unavailable());
    }
    let named = at(dir, name, libc::O_RDONLY)?;
    if stamp(&named)? != before {
        return Err(unavailable());
    }
    let identity = json!({"metadata":before,"content":content(&bytes)});
    Ok((bytes, identity))
}
fn source_file(path: &Path, observed: &mut Observed) -> Result<Vec<u8>, String> {
    let parent = path.parent().ok_or_else(unavailable)?;
    let file = path
        .file_name()
        .and_then(|n| n.to_str())
        .ok_or_else(unavailable)?;
    let dir = directory(parent, observed)?.ok_or_else(unavailable)?;
    let (bytes, identity) = bytes_at(&dir, file)?;
    observed.tick(bytes.len())?;
    observed.insert(path.to_string_lossy().into(), identity);
    Ok(bytes)
}
fn parse_name(bytes: &[u8], hint: Option<&str>, out: &mut BTreeSet<String>) -> Result<(), String> {
    let text = std::str::from_utf8(bytes).map_err(|_| unavailable())?;
    let value: toml::Value = toml::from_str(text).map_err(|_| unavailable())?;
    let table = value.as_table().ok_or_else(unavailable)?;
    // Initial supported file shape is deliberately narrow. Unknown native
    // settings or malformed metadata withhold rather than approximating the
    // supplier's entire ConfigToml deserializer.
    if table.keys().any(|key| {
        !matches!(
            key.as_str(),
            "name" | "description" | "developer_instructions" | "nickname_candidates"
        )
    }) {
        return Err(unavailable());
    }
    for key in ["name", "description", "developer_instructions"] {
        if let Some(value) = table.get(key) {
            if value.as_str().is_none_or(|s| s.trim().is_empty()) {
                return Err(unavailable());
            }
        }
    }
    if hint.is_none()
        && (!table.contains_key("description") || !table.contains_key("developer_instructions"))
    {
        return Err(unavailable());
    }
    if let Some(value) = table.get("nickname_candidates") {
        let values = value.as_array().ok_or_else(unavailable)?;
        if values.is_empty()
            || values
                .iter()
                .any(|v| v.as_str().is_none_or(|s| s.trim().is_empty()))
        {
            return Err(unavailable());
        }
    }

    let name = match table.get("name") {
        Some(v) => Some(v.as_str().ok_or_else(unavailable)?.trim()).filter(|n| !n.is_empty()),
        None => None,
    }
    .or(hint)
    .ok_or_else(unavailable)?;
    out.insert(name.to_owned());
    Ok(())
}
fn walk(
    dir: &File,
    path: &Path,
    observed: &mut Observed,
    out: &mut BTreeSet<String>,
    depth: usize,
) -> Result<(), String> {
    observed.tick(0)?;
    if depth > 32 {
        return Err(unavailable());
    }
    let before = stamp(dir)?;
    let entries = names(dir)?;
    observed.insert(
        format!("{}/", path.display()),
        json!({"metadata":before,"entries":entries}),
    );
    for name in &entries {
        observed.tick(0)?;
        let child = path.join(name);
        let m = metadata_at(dir, name)?.ok_or_else(unavailable)?;
        match m.st_mode & libc::S_IFMT {
            libc::S_IFDIR => {
                let next = at(dir, name, libc::O_RDONLY | libc::O_DIRECTORY)?;
                if id(&next)? != (m.st_dev as u64, m.st_ino as u64) {
                    return Err(unavailable());
                }
                walk(&next, &child, observed, out, depth + 1)?;
            }
            libc::S_IFREG => {
                if child.extension().is_some_and(|e| e == "toml") {
                    let (bytes, identity) = bytes_at(dir, name)?;
                    observed.tick(bytes.len())?;
                    parse_name(&bytes, None, out)?;
                    observed.insert(child.to_string_lossy().into(), identity);
                }
            }
            _ => return Err(unavailable()),
        }
    }
    if stamp(dir)? != before || names(dir)? != entries {
        return Err(unavailable());
    }
    Ok(())
}
fn declarations(
    agents: &Value,
    base: Option<&Path>,
    observed: &mut Observed,
    names: &mut BTreeSet<String>,
) -> Result<(), String> {
    if agents.is_null() {
        return Ok(());
    }
    for (hint, role) in agents.as_object().ok_or_else(unavailable)? {
        observed.tick(0)?;
        if CONTROLS.contains(&hint.as_str()) {
            if !role.is_null() && !role.is_boolean() && !role.is_number() && !role.is_string() {
                return Err(unavailable());
            }
            continue;
        }
        let role = role.as_object().ok_or_else(unavailable)?;
        if role.keys().any(|key| {
            !matches!(
                key.as_str(),
                "description" | "config_file" | "nickname_candidates"
            )
        }) {
            return Err(unavailable());
        }
        if role
            .get("description")
            .is_some_and(|v| !v.is_null() && v.as_str().is_none_or(|s| s.trim().is_empty()))
        {
            return Err(unavailable());
        }
        if let Some(value) = role.get("nickname_candidates").filter(|v| !v.is_null()) {
            if value.as_array().is_none_or(|values| {
                values.is_empty()
                    || values
                        .iter()
                        .any(|v| v.as_str().is_none_or(|s| s.trim().is_empty()))
            }) {
                return Err(unavailable());
            }
        }

        names.insert(hint.clone());
        if let Some(file) = role.get("config_file").filter(|v| !v.is_null()) {
            let path = Path::new(file.as_str().ok_or_else(unavailable)?);
            let path = if path.is_absolute() {
                path.to_owned()
            } else if let Some(base) = base {
                if path
                    .components()
                    .any(|p| !matches!(p, Component::Normal(_) | Component::CurDir))
                {
                    return Err(unavailable());
                }
                base.join(path)
                    .components()
                    .filter(|c| !matches!(c, Component::CurDir))
                    .collect()
            } else {
                return Err(unavailable());
            };
            let bytes = source_file(&path, observed)?;
            parse_name(&bytes, Some(hint), names)?;
        }
    }
    Ok(())
}
/// Only a Root-owned home-resource descriptor may authorize this one leaf.
#[derive(Clone, Debug, PartialEq)]
pub(crate) struct ConfigLink {
    source: PathBuf,
    target: PathBuf,
}
impl ConfigLink {
    pub(crate) fn observed(source: PathBuf, target: PathBuf) -> Result<Self, String> {
        let link = Self { source, target };
        let mut observed = Observed::default();
        link.read(&mut observed)?;
        Ok(link)
    }
    fn read(&self, observed: &mut Observed) -> Result<Vec<u8>, String> {
        let parent = directory(self.source.parent().ok_or_else(unavailable)?, observed)?
            .ok_or_else(unavailable)?;
        let name = self
            .source
            .file_name()
            .and_then(|s| s.to_str())
            .ok_or_else(unavailable)?;
        let before = metadata_at(&parent, name)?.ok_or_else(unavailable)?;
        if before.st_mode & libc::S_IFMT != libc::S_IFLNK {
            return Err(unavailable());
        }
        let c = CString::new(name).map_err(|_| unavailable())?;
        let mut bytes = vec![0u8; 4097];
        let len = unsafe {
            libc::readlinkat(
                parent.as_raw_fd(),
                c.as_ptr(),
                bytes.as_mut_ptr().cast(),
                bytes.len(),
            )
        };
        if len < 0 || len as usize >= bytes.len() {
            return Err(unavailable());
        }
        bytes.truncate(len as usize);
        use std::os::unix::ffi::OsStrExt;
        if std::ffi::OsStr::from_bytes(&bytes) != self.target.as_os_str()
            || !self.target.is_absolute()
        {
            return Err(unavailable());
        }
        let result = source_file(&self.target, observed)?;
        let after = metadata_at(&parent, name)?.ok_or_else(unavailable)?;
        if (
            before.st_dev,
            before.st_ino,
            before.st_mtime,
            before.st_ctime,
        ) != (after.st_dev, after.st_ino, after.st_mtime, after.st_ctime)
        {
            return Err(unavailable());
        }
        observed.insert(
            format!("configLink:{}", self.source.display()),
            json!({"device":before.st_dev,"inode":before.st_ino,"target":self.target}),
        );
        Ok(result)
    }
}
/// Private construction is performed only from the genuine Host config receipt.
#[derive(Clone, Debug, PartialEq)]
pub(crate) struct Namespace {
    config: Value,
    paths: BTreeMap<String, Value>,
    names: BTreeSet<String>,
    link: Option<ConfigLink>,
}
impl Namespace {
    pub(crate) fn observe(config: &Value) -> Result<Self, String> {
        Self::observe_linked(config, None)
    }
    pub(crate) fn observe_linked(config: &Value, link: Option<ConfigLink>) -> Result<Self, String> {
        let layers = config["layers"]
            .as_array()
            .filter(|v| !v.is_empty())
            .ok_or_else(unavailable)?;
        if layers.len() > 128
            || serde_json::to_vec(config).map_err(|_| unavailable())?.len() > 8 * 1024 * 1024
        {
            return Err(unavailable());
        }
        let mut paths = Observed::default();
        let mut names = BTreeSet::new();
        let mut sources = BTreeSet::new();
        let mut roots = BTreeSet::new();
        let mut user = false;
        let mut system = false;
        for layer in layers {
            let source = layer["name"].as_object().ok_or_else(unavailable)?;
            let kind = source
                .get("type")
                .and_then(Value::as_str)
                .ok_or_else(unavailable)?;
            if layer["version"].as_str().is_none_or(str::is_empty) || !layer["config"].is_object() {
                return Err(unavailable());
            }
            if !sources.insert(serde_json::to_string(source).map_err(|_| unavailable())?) {
                return Err(unavailable());
            }
            let folder = match kind {
                "system" => {
                    system = true;
                    if !layer["config"].as_object().unwrap().is_empty() {
                        return Err(unavailable());
                    }
                    PathBuf::from(
                        source
                            .get("file")
                            .and_then(Value::as_str)
                            .ok_or_else(unavailable)?,
                    )
                    .parent()
                    .ok_or_else(unavailable)?
                    .to_owned()
                }
                "user" => {
                    user = true;
                    if source.get("profile") != Some(&Value::Null) {
                        return Err(unavailable());
                    }
                    PathBuf::from(
                        source
                            .get("file")
                            .and_then(Value::as_str)
                            .ok_or_else(unavailable)?,
                    )
                    .parent()
                    .ok_or_else(unavailable)?
                    .to_owned()
                }
                "project" => PathBuf::from(
                    source
                        .get("dotCodexFolder")
                        .and_then(Value::as_str)
                        .ok_or_else(unavailable)?,
                ),
                "sessionFlags" => {
                    if source.len() != 1 {
                        return Err(unavailable());
                    }
                    PathBuf::new()
                }
                _ => return Err(unavailable()),
            };
            #[cfg(target_os = "macos")]
            let folder = if kind == "system" && folder == Path::new("/etc/codex") {
                let metadata = std::fs::symlink_metadata("/etc").map_err(|_| unavailable())?;
                let target = std::fs::read_link("/etc").map_err(|_| unavailable())?;
                if !metadata.file_type().is_symlink() || target != Path::new("private/etc") {
                    return Err(unavailable());
                }
                paths.insert(
                    "systemAlias:/etc".into(),
                    json!({"device":metadata.dev(),"inode":metadata.ino(),"target":"/private/etc"}),
                );
                PathBuf::from("/private/etc/codex")
            } else {
                folder
            };
            let known = if kind == "project" {
                vec!["type", "dotCodexFolder"]
            } else if kind == "user" {
                vec!["type", "file", "profile"]
            } else if kind == "system" {
                vec!["type", "file"]
            } else {
                vec!["type"]
            };
            if source.keys().any(|k| !known.contains(&k.as_str())) {
                return Err(unavailable());
            }
            if let Some(reason) = layer.get("disabledReason").filter(|r| !r.is_null()) {
                if !reason.is_string() || kind != "project" {
                    return Err(unavailable());
                }
                continue;
            }
            if !folder.as_os_str().is_empty() {
                let config_file = if kind == "project" || kind == "system" {
                    folder.join("config.toml")
                } else {
                    PathBuf::from(
                        source
                            .get("file")
                            .and_then(Value::as_str)
                            .ok_or_else(unavailable)?,
                    )
                };
                if let Some(dir) = directory(&folder, &mut paths)? {
                    let leaf = config_file
                        .file_name()
                        .and_then(|s| s.to_str())
                        .ok_or_else(unavailable)?;
                    if metadata_at(&dir, leaf)?.is_some() {
                        let bytes = if kind == "user"
                            && link.as_ref().is_some_and(|l| l.source == config_file)
                        {
                            link.as_ref().unwrap().read(&mut paths)?
                        } else {
                            source_file(&config_file, &mut paths)?
                        };
                        let source: toml::Value =
                            toml::from_str(std::str::from_utf8(&bytes).map_err(|_| unavailable())?)
                                .map_err(|_| unavailable())?;
                        let source = serde_json::to_value(source).map_err(|_| unavailable())?;
                        if let Some(agents) = source.get("agents") {
                            declarations(agents, Some(&folder), &mut paths, &mut names)?;
                        }
                    } else {
                        paths.insert(
                            config_file.to_string_lossy().into(),
                            json!({"absentUnder":id(&dir)?}),
                        );
                    }
                }
                let root = folder.join("agents");
                let dir = directory(&root, &mut paths)?;
                if kind == "system" && dir.is_some() {
                    return Err(unavailable());
                }
                if roots.insert(root.clone()) {
                    if let Some(dir) = dir {
                        walk(&dir, &root, &mut paths, &mut names, 0)?
                    }
                }
            }
            if let Some(agents) = layer["config"].get("agents") {
                declarations(agents, None, &mut paths, &mut names)?;
            }
        }
        if !user || !system {
            return Err(unavailable());
        }
        paths.tick(0)?;
        Ok(Self {
            config: config.clone(),
            paths: paths.paths,
            names,
            link,
        })
    }
    pub(crate) fn recheck(&self) -> Result<(), String> {
        #[cfg(test)]
        BEFORE_RECHECK.with(|hook| {
            let hook = hook.borrow_mut().take();
            if let Some(hook) = hook {
                hook();
            }
        });
        if &Self::observe_linked(&self.config, self.link.clone())? != self {
            return Err(unavailable());
        }
        Ok(())
    }
    pub(crate) fn contains(&self, role: Role) -> bool {
        self.names.contains(role.name())
    }
    pub(crate) fn summary(&self) -> Value {
        json!({"standing":"observed configuration and source bytes; not a lock on later changes","candidateNames":self.names,"sourceCount":self.paths.len(),"config":content(&serde_json::to_vec(&self.config).unwrap())})
    }
}
#[derive(Clone, Debug)]
pub struct ChildSupply {
    pub(crate) role: Role,
    pub(crate) composition: Box<Composition>,
    pub(crate) path: PathBuf,
    pub(crate) envelope: Vec<u8>,
}
impl ChildSupply {
    pub fn description(&self) -> String {
        format!(
            "Chirality {}: {}",
            self.role.name(),
            if self.role == Role::TASK {
                "bounded work; does not delegate (stated, not enforced)"
            } else {
                "App working relationship guidance"
            }
        )
    }
    pub fn config(&self) -> Value {
        json!({format!("agents.{}.description",self.role.name()):self.description(),format!("agents.{}.config_file",self.role.name()):self.path})
    }
    pub fn record(&self) -> Value {
        json!({"role":self.role,"status":"supplied","configKeys":[format!("agents.{}.description",self.role.name()),format!("agents.{}.config_file",self.role.name())],"composed":content(self.composition.text.as_bytes()),"file":content(&self.envelope)})
    }
    pub(crate) fn recheck(&self) -> Result<(), String> {
        let mut observed = Observed::default();
        if source_file(&self.path, &mut observed)? != self.envelope {
            return Err("Native child roles withheld: App child file changed".into());
        }
        Ok(())
    }
}
fn publish(root: &Path, role: Role, composition: Composition) -> Result<ChildSupply, String> {
    let envelope = format!(
        "developer_instructions = {}\n",
        serde_json::to_string(&composition.text).map_err(|_| unavailable())?
    )
    .into_bytes();
    // JSON strings are valid TOML basic strings; parse the complete saved envelope.
    let parsed: toml::Value =
        toml::from_str(std::str::from_utf8(&envelope).unwrap()).map_err(|_| unavailable())?;
    if parsed["developer_instructions"].as_str() != Some(&composition.text) {
        return Err(unavailable());
    }
    let mut observed = Observed::default();
    let parent = directory(root, &mut observed)?.ok_or_else(unavailable)?;
    let name = CString::new("native-child-roles").unwrap();
    if unsafe { libc::mkdirat(parent.as_raw_fd(), name.as_ptr(), 0o700) } < 0
        && std::io::Error::last_os_error().kind() != std::io::ErrorKind::AlreadyExists
    {
        return Err(unavailable());
    }
    let dir = at(
        &parent,
        "native-child-roles",
        libc::O_RDONLY | libc::O_DIRECTORY,
    )?;
    let filename = format!("{}.toml", crate::util::sha256_hex(&envelope));
    match at(
        &dir,
        &filename,
        libc::O_WRONLY | libc::O_CREAT | libc::O_EXCL,
    ) {
        Ok(mut file) => {
            file.write_all(&envelope).map_err(|_| unavailable())?;
            file.sync_all().map_err(|_| unavailable())?;
            if unsafe { libc::fchmod(file.as_raw_fd(), 0o400) } < 0 {
                return Err(unavailable());
            }
            file.sync_all().map_err(|_| unavailable())?;
        }
        Err(_) => {
            let (bytes, _) = bytes_at(&dir, &filename)?;
            if bytes != envelope {
                return Err("Native child roles withheld: App child content path collision".into());
            }
        }
    }
    dir.sync_all().map_err(|_| unavailable())?;
    parent.sync_all().map_err(|_| unavailable())?;
    let path = root.join("native-child-roles").join(filename);
    let supply = ChildSupply {
        role,
        composition: Box::new(composition),
        path,
        envelope,
    };
    supply.recheck()?;
    Ok(supply)
}
/// Called by Rust's private admitted start path; uncertainty withholds children.
pub(crate) fn prepare(
    parent: &mut Composition,
    reading: Result<Namespace, String>,
    instructions: &Path,
    data: &Path,
) -> Option<Namespace> {
    let mut statuses = vec![];
    let mut children = vec![];
    let unsupported = reading
        .as_ref()
        .err()
        .is_some_and(|e| e == "unsupported-native-child-supplier");
    let namespace = reading.ok();
    for role in Role::ALL {
        let offered = parent.role.is_some_and(|r| r.child_roles().contains(&role));
        let result = if !offered {
            Err("not-offered-by-role")
        } else if unsupported {
            Err("mechanism-not-supported-at-pin")
        } else if namespace.is_none() {
            Err("user-configuration-not-read")
        } else if namespace.as_ref().unwrap().contains(role) {
            Err("user-configuration-defines-role")
        } else {
            Ok(())
        };
        let child = result
            .and_then(|_| {
                Guidance::read_seeded(
                    instructions,
                    &format!("agents/AGENT_{}.md", role.name()),
                    crate::runtime_session::INSTRUCTION_RELEASE,
                    crate::runtime_session::role_default(role),
                )
                .map_err(|_| "child-guidance-unavailable")
            })
            .and_then(|g| {
                parent
                    .compose_child(role, &g)
                    .map_err(|_| "child-guidance-unavailable")
            })
            .and_then(|c| publish(data, role, c).map_err(|_| "child-file-unavailable"));
        match child {
            Ok(child) => {
                statuses.push(child.record());
                children.push(child)
            }
            Err(reason) => {
                statuses.push(json!({"role":role,"status":"not-supplied","reason":reason}))
            }
        }
    }
    parent.carried["nativeChildRoles"] = json!(statuses);
    parent.children = children;
    parent.child_reading = namespace
        .as_ref()
        .map(Namespace::summary)
        .unwrap_or_else(|| json!({"standing":LIMIT}));
    parent.carried["nativeChildObservation"] = parent.child_reading.clone();
    namespace
}
#[cfg(test)]
thread_local! {pub(crate) static BEFORE_RECHECK:std::cell::RefCell<Option<Box<dyn FnOnce()>>>=const{std::cell::RefCell::new(None)};}
#[cfg(test)]
#[path = "child_roles_tests.rs"]
mod tests;
/// Explicit supplier-check plumbing. This pure output grants no Host admission;
/// production dispatch still requires its private correlated native receipt.
#[cfg(feature = "synthetic-distribution-anchor")]
pub fn supplier_fixture(
    reading: &Value,
    instructions: &Path,
    data: &Path,
    role: Option<Role>,
    link: Option<(PathBuf, PathBuf)>,
) -> Result<Value, String> {
    crate::runtime_session::seed_instructions(instructions)?;
    let mut composition = crate::runtime_session::compose_role(instructions, role)?;
    let link = link
        .map(|(source, target)| ConfigLink::observed(source, target))
        .transpose()?;
    prepare(
        &mut composition,
        Namespace::observe_linked(reading, link),
        instructions,
        data,
    );
    composition.verify()?;
    Ok(
        json!({"config":composition.native_config(),"parent":composition.text,"carried":composition.carried,"namespace":composition.child_reading,"children":composition.children.iter().map(|c|json!({"role":c.role,"text":c.composition.text,"path":c.path,"file":content(&c.envelope)})).collect::<Vec<_>>() }),
    )
}
