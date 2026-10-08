//! Protected, immutable publication of explicitly unqualified Host attempts.
//! This is not an S1 observation/lifecycle reader or a supplier trust issuer.
use crate::hosting::attachment_custody::NativeNamespaceBindings;
use crate::{distribution_preflight::digest, recovery, util};
use serde::Serialize;
use serde_json::{json, Value};
use std::{
    ffi::CString,
    fs::File,
    io::{Read, Write},
    os::unix::{
        fs::MetadataExt,
        io::{AsRawFd, FromRawFd},
    },
    path::{Component, Path, PathBuf},
    sync::Arc,
};

const MANIFEST: &str = "transport.json";
const ATTEMPT: &str = "attempt.json";
const LIMIT: usize = 16 * 1024 * 1024;
#[derive(Clone, Serialize)]
#[serde(rename_all = "camelCase")]
pub(crate) struct Reference {
    format: &'static str,
    publication: String,
    generation: Value,
    transport_sha256: String,
    attempt_sha256: String,
    #[serde(skip)]
    publication_id: (u64, u64),
}
pub(crate) struct Store {
    app_data: PathBuf,
    root: PathBuf,
    root_id: (u64, u64),
    vendor: PathBuf,
    namespaces: Arc<NativeNamespaceBindings>,
    #[cfg(test)]
    before_audit: std::sync::Mutex<Option<Box<dyn FnOnce() + Send>>>,
}
fn error(e: impl std::fmt::Display) -> String {
    e.to_string()
}
fn component(s: &str) -> Result<CString, String> {
    if s.is_empty() || s == "." || s == ".." || s.contains(['/', '\\', '\0', '\n', '\r']) {
        return Err("invalid publication component".into());
    }
    CString::new(s).map_err(error)
}
fn open_at(parent: &File, name: &str, directory: bool) -> Result<File, String> {
    let name = component(name)?;
    let flags = libc::O_RDONLY
        | libc::O_NOFOLLOW
        | libc::O_CLOEXEC
        | libc::O_NONBLOCK
        | if directory { libc::O_DIRECTORY } else { 0 };
    let fd = unsafe { libc::openat(parent.as_raw_fd(), name.as_ptr(), flags) };
    if fd < 0 {
        return Err(error(std::io::Error::last_os_error()));
    }
    Ok(unsafe { File::from_raw_fd(fd) })
}
fn physical_root(path: &Path) -> Result<File, String> {
    if !path.is_absolute() {
        return Err("absolute physical publication root required".into());
    }
    let mut fd = File::open("/").map_err(error)?;
    for c in path.components() {
        match c {
            Component::RootDir => (),
            Component::Normal(c) => {
                fd = open_at(&fd, c.to_str().ok_or("non UTF-8 publication root")?, true)?
            }
            _ => return Err("non-normal publication root".into()),
        }
    }
    Ok(fd)
}
fn id(file: &File) -> Result<(u64, u64), String> {
    let m = file.metadata().map_err(error)?;
    Ok((m.dev(), m.ino()))
}
fn private(file: &File, directory: bool) -> Result<(), String> {
    let m = file.metadata().map_err(error)?;
    if m.uid() != unsafe { libc::geteuid() }
        || m.mode() & 0o077 != 0
        || (directory && !m.is_dir())
        || (!directory && (!m.is_file() || m.nlink() != 1))
    {
        return Err("publication object is not private, owned, and expected type".into());
    }
    Ok(())
}
fn mkdir(parent: &File, name: &str, exclusive: bool) -> Result<File, String> {
    let c = component(name)?;
    if unsafe { libc::mkdirat(parent.as_raw_fd(), c.as_ptr(), 0o700) } != 0 {
        let e = std::io::Error::last_os_error();
        if exclusive || e.kind() != std::io::ErrorKind::AlreadyExists {
            return Err(error(e));
        }
    }
    let fd = open_at(parent, name, true)?;
    private(&fd, true)?;
    Ok(fd)
}
fn write_new(parent: &File, name: &str, bytes: &[u8]) -> Result<(), String> {
    if bytes.len() > LIMIT {
        return Err("publication exceeds bounded artifact size".into());
    }
    let c = component(name)?;
    let fd = unsafe {
        libc::openat(
            parent.as_raw_fd(),
            c.as_ptr(),
            libc::O_WRONLY | libc::O_CREAT | libc::O_EXCL | libc::O_NOFOLLOW | libc::O_CLOEXEC,
            0o600,
        )
    };
    if fd < 0 {
        return Err(error(std::io::Error::last_os_error()));
    }
    let mut file = unsafe { File::from_raw_fd(fd) };
    private(&file, false)?;
    file.write_all(bytes).map_err(error)?;
    file.sync_all().map_err(error)?;
    private(&file, false)
}
fn read_exact(parent: &File, name: &str, expected: &str) -> Result<Vec<u8>, String> {
    let mut file = open_at(parent, name, false)?;
    private(&file, false)?;
    let before = file.metadata().map_err(error)?;
    if before.len() > LIMIT as u64 {
        return Err("publication exceeds bounded artifact size".into());
    }
    let mut raw = Vec::new();
    (&mut file)
        .take(LIMIT as u64 + 1)
        .read_to_end(&mut raw)
        .map_err(error)?;
    let after = file.metadata().map_err(error)?;
    let named = open_at(parent, name, false)?;
    if raw.len() > LIMIT
        || id(&file)? != id(&named)?
        || before.len() != after.len()
        || before.mtime() != after.mtime()
        || before.mtime_nsec() != after.mtime_nsec()
        || before.ctime() != after.ctime()
        || before.ctime_nsec() != after.ctime_nsec()
        || digest(&raw) != expected
    {
        return Err("artifact changed or exact-byte digest differs".into());
    }
    private(&file, false)?;
    Ok(raw)
}
fn publish_rename(parent: &File, from: &str, to: &str) -> Result<(), String> {
    let from = component(from)?;
    let to = component(to)?;
    #[cfg(target_os = "macos")]
    let result = unsafe {
        libc::renameatx_np(
            parent.as_raw_fd(),
            from.as_ptr(),
            parent.as_raw_fd(),
            to.as_ptr(),
            libc::RENAME_EXCL,
        )
    };
    #[cfg(target_os = "linux")]
    let result = unsafe {
        libc::syscall(
            libc::SYS_renameat2,
            parent.as_raw_fd(),
            from.as_ptr(),
            parent.as_raw_fd(),
            to.as_ptr(),
            libc::RENAME_NOREPLACE,
        ) as i32
    };
    if result != 0 {
        return Err(error(std::io::Error::last_os_error()));
    }
    Ok(())
}
/// Observe every existing ancestor without following links. Missing suffixes are
/// allowed only for the prospective publication root, never the vendor root.
fn directory_chain(
    path: &Path,
    allow_missing: bool,
) -> Result<(Vec<(u64, u64)>, Option<(u64, u64)>), String> {
    if !path.is_absolute() {
        return Err("absolute physical domain required".into());
    }
    // Validate the entire path even when its first missing component is reached.
    for part in path.components() {
        match part {
            Component::RootDir => (),
            Component::Normal(name) => {
                component(name.to_str().ok_or("non UTF-8 domain")?)?;
            }
            _ => return Err("non-normal domain".into()),
        }
    }
    let mut fd = File::open("/").map_err(error)?;
    let mut chain = vec![id(&fd)?];
    for part in path.components() {
        if let Component::Normal(name) = part {
            let name = component(name.to_str().ok_or("non UTF-8 domain")?)?;
            let raw = unsafe {
                libc::openat(
                    fd.as_raw_fd(),
                    name.as_ptr(),
                    libc::O_RDONLY
                        | libc::O_DIRECTORY
                        | libc::O_NOFOLLOW
                        | libc::O_CLOEXEC
                        | libc::O_NONBLOCK,
                )
            };
            if raw < 0 {
                let e = std::io::Error::last_os_error();
                if allow_missing && e.kind() == std::io::ErrorKind::NotFound {
                    return Ok((chain, None));
                }
                return Err(error(e));
            }
            fd = unsafe { File::from_raw_fd(raw) };
            chain.push(id(&fd)?);
        }
    }
    Ok((chain, Some(id(&fd)?)))
}
fn guard_vendor_domain(root: &Path, vendor: &Path) -> Result<(), String> {
    let (vendor_chain, vendor_id) = directory_chain(vendor, false)?;
    let (root_chain, root_id) = directory_chain(root, true)?;
    if root_chain.contains(&vendor_id.ok_or("vendor absent")?)
        || root_id.is_some_and(|root_id| vendor_chain.contains(&root_id))
    {
        return Err("physical publication/vendor domains overlap".into());
    }
    Ok(())
}
impl Store {
    pub(crate) fn open(
        app_data: &Path,
        vendor: &Path,
        namespaces: Arc<NativeNamespaceBindings>,
    ) -> Result<Arc<Self>, String> {
        namespaces.guard_app_root(app_data)?;
        let root = app_data.join("runtime/distribution");
        namespaces.guard_domains(&[root.clone()])?;
        let app = physical_root(app_data)?;
        guard_vendor_domain(&root, vendor)?;
        if id(&app)? != id(&physical_root(app_data)?)? {
            return Err("App data root changed".into());
        }
        let runtime = mkdir(&app, "runtime", false)?;
        guard_vendor_domain(&root, vendor)?;
        if id(&runtime)? != id(&physical_root(&app_data.join("runtime"))?)? {
            return Err("runtime root changed".into());
        }
        let dir = mkdir(&runtime, "distribution", false)?;
        dir.sync_all().map_err(error)?;
        runtime.sync_all().map_err(error)?;
        app.sync_all().map_err(error)?;
        let store = Arc::new(Self {
            app_data: app_data.into(),
            root,
            root_id: id(&dir)?,
            vendor: vendor.into(),
            namespaces,
            #[cfg(test)]
            before_audit: std::sync::Mutex::new(None),
        });
        store.guard()?;
        Ok(store)
    }
    fn guard(&self) -> Result<File, String> {
        self.namespaces.guard_app_root(&self.app_data)?;
        self.namespaces.guard_domains(&[self.root.clone()])?;
        guard_vendor_domain(&self.root, &self.vendor)?;
        let root = physical_root(&self.root)?;
        private(&root, true)?;
        if id(&root)? != self.root_id {
            return Err("publication root relocated or replaced".into());
        }
        Ok(root)
    }
    fn generation(&self, g: &Value) -> Result<(), String> {
        recovery::generation_ref(g)?;
        self.namespaces
            .contains_home_id(g["home"].as_str().ok_or("missing home")?)
    }
    /// Development evidence only: no caller can turn it into a qualified closure.
    /// Selected-closure transport machinery is a separate implementation residual;
    /// production also lacks the compiled S3 selection and installed-custody issuer.
    pub(crate) fn publish_attempt(&self, g: &Value, attempt: &Value) -> Result<Reference, String> {
        self.generation(g)?;
        if attempt["format"] != "host-successor-attempt.s2"
            || attempt["standing"] != "unverified-development"
            || attempt["verificationGeneration"] != *g
        {
            return Err("unsupported attempt format/standing/generation".into());
        }
        let parent = self.guard()?;
        let name = util::opaque_id("attempt-")?;
        let staging = format!(".pending-{name}");
        let dir = mkdir(&parent, &staging, true)?;
        let raw = serde_json::to_vec(attempt).map_err(error)?;
        let attempt_hash = digest(&raw);
        let manifest = json!({"format":"distribution-evidence-transport.s2","mode":"development-unqualified","generation":g,
            "sourceSelection":null,"originalSource":null,"entries":[{"path":ATTEMPT,"sha256":attempt_hash}],
            "createdAt":util::now_rfc3339(),"limit":"Creation-time exact bytes only; no supplier trust, S1 validation, live custody, or future integrity guarantee"});
        let manifest_raw = serde_json::to_vec(&manifest).map_err(error)?;
        write_new(&dir, ATTEMPT, &raw)?;
        write_new(&dir, MANIFEST, &manifest_raw)?;
        dir.sync_all().map_err(error)?;
        self.guard()?;
        self.generation(g)?;
        if id(&dir)? != id(&open_at(&parent, &staging, true)?)? {
            return Err("staging root replaced".into());
        }
        publish_rename(&parent, &staging, &name)?;
        parent.sync_all().map_err(error)?;
        let reference = Reference {
            format: "host-attempt-reference.s2",
            publication: name,
            generation: g.clone(),
            transport_sha256: digest(&manifest_raw),
            attempt_sha256: attempt_hash,
            publication_id: id(&dir)?,
        };
        self.read(g, &reference)?;
        Ok(reference)
    }
    /// Native at-use read: references are held capabilities, not UI-supplied paths.
    pub(crate) fn read(&self, g: &Value, reference: &Reference) -> Result<Value, String> {
        self.generation(g)?;
        if &reference.generation != g {
            return Err("foreign generation reference".into());
        }
        let root = self.guard()?;
        let dir = open_at(&root, &reference.publication, true)?;
        private(&dir, true)?;
        if id(&dir)? != reference.publication_id {
            return Err("publication directory relocated or replaced".into());
        }
        let manifest_raw = read_exact(&dir, MANIFEST, &reference.transport_sha256)?;
        let manifest: Value = serde_json::from_slice(&manifest_raw).map_err(error)?;
        let schema: Value = serde_json::from_str(include_str!(
            "../resources/distribution-successor/distribution-evidence-transport.s2.schema.json"
        ))
        .map_err(error)?;
        jsonschema::validator_for(&schema)
            .map_err(error)?
            .validate(&manifest)
            .map_err(error)?;
        if manifest["generation"] != *g
            || manifest["entries"] != json!([{"path":ATTEMPT,"sha256":reference.attempt_sha256}])
        {
            return Err("transport binding differs".into());
        }
        let raw = read_exact(&dir, ATTEMPT, &reference.attempt_sha256)?;
        let attempt: Value = serde_json::from_slice(&raw).map_err(error)?;
        if attempt["format"] != "host-successor-attempt.s2"
            || attempt["standing"] != "unverified-development"
            || attempt["verificationGeneration"] != *g
        {
            return Err("attempt binding differs".into());
        }
        #[cfg(test)]
        if let Some(hook) = self.before_audit.lock().unwrap().take() {
            hook();
        }
        // Final full audit must join bytes, type and mode, not only names.
        let inventory =
            crate::distribution_preflight::scan(&self.root.join(&reference.publication))?;
        let names: Vec<_> = inventory
            .entries
            .iter()
            .filter(|e| e.path != ".")
            .map(|e| e.path.as_str())
            .collect();
        if names != vec![ATTEMPT, MANIFEST] || inventory.entries.len() != 3 {
            return Err("publication closure differs".into());
        }
        for entry in &inventory.entries {
            if entry.path == "." {
                if entry.kind != "dir" || entry.mode != 0o700 {
                    return Err("publication root identity differs".into());
                }
            } else {
                let (hash, len) = if entry.path == ATTEMPT {
                    (&reference.attempt_sha256, raw.len())
                } else {
                    (&reference.transport_sha256, manifest_raw.len())
                };
                if entry.kind != "file"
                    || entry.mode != 0o600
                    || entry.sha256.as_ref() != Some(hash)
                    || entry.size != Some(len as u64)
                {
                    return Err("publication final inventory differs".into());
                }
            }
        }
        if id(&dir)? != id(&open_at(&root, &reference.publication, true)?)? {
            return Err("publication directory replaced".into());
        }
        self.guard()?;
        self.generation(g)?;
        Ok(
            json!({"reference":reference,"artifact":attempt,"transport":manifest,"standing":"unverified-development","readStanding":"exact bytes checked at this read; no future integrity or live-custody assertion"}),
        )
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::home_resources::{ExistingHomeReference, HomeClass};
    use crate::hosting::attachment_custody::NativeHomeNamespace;
    struct Fixture {
        root: PathBuf,
        store: Arc<Store>,
        g: Value,
        attempt: Value,
    }
    impl Fixture {
        fn new() -> Self {
            let root = std::env::temp_dir()
                .canonicalize()
                .unwrap()
                .join(util::opaque_id("store-").unwrap());
            for name in ["app", "vendor", "home"] {
                std::fs::create_dir_all(root.join(name)).unwrap();
            }
            let home = ExistingHomeReference::new(root.join("home"), HomeClass::Account).unwrap();
            let bindings = NativeNamespaceBindings::from_root(vec![NativeHomeNamespace::received(
                &home, None,
            )])
            .unwrap();
            let store = Store::open(&root.join("app"), &root.join("vendor"), bindings).unwrap();
            let g = json!({"appSession":"fixture","home":home.opaque_home_id(),"spawnCounter":1});
            let attempt = json!({"format":"host-successor-attempt.s2","standing":"unverified-development","verificationGeneration":g,"rawVersionLabel":"codex-cli 0.160.0\n"});
            Self {
                root,
                store,
                g,
                attempt,
            }
        }
        fn publish(&self) -> Reference {
            self.store.publish_attempt(&self.g, &self.attempt).unwrap()
        }
        fn path(&self, r: &Reference) -> PathBuf {
            self.root
                .join("app/runtime/distribution")
                .join(&r.publication)
        }
    }
    impl Drop for Fixture {
        fn drop(&mut self) {
            let _ = std::fs::remove_dir_all(&self.root);
        }
    }
    #[test]
    fn repeated_prospective_tuple_never_overwrites_and_foreign_tuple_refuses() {
        let f = Fixture::new();
        let a = f.publish();
        let b = f.publish();
        assert_ne!(a.publication, b.publication);
        assert!(f.store.read(&f.g, &a).is_ok());
        assert!(f.store.read(&f.g, &b).is_ok());
        let mut g = f.g.clone();
        g["spawnCounter"] = json!(2);
        assert!(f.store.read(&g, &a).is_err());
        let parent = f.store.guard().unwrap();
        assert!(publish_rename(&parent, &a.publication, &b.publication).is_err());
        assert!(f.store.read(&f.g, &a).is_ok());
        assert!(f.store.read(&f.g, &b).is_ok());
    }
    #[test]
    fn hardlinks_symlinks_missing_bytes_and_relocated_roots_refuse() {
        for mode in ["hardlink", "symlink", "missing", "relocate"] {
            let f = Fixture::new();
            let r = f.publish();
            let file = f.path(&r).join(ATTEMPT);
            match mode {
                "hardlink" => std::fs::hard_link(&file, f.root.join("alias")).unwrap(),
                "symlink" => {
                    std::fs::remove_file(&file).unwrap();
                    std::os::unix::fs::symlink(f.root.join("external"), &file).unwrap();
                }
                "missing" => std::fs::remove_file(&file).unwrap(),
                _ => {
                    std::fs::rename(&f.store.root, f.root.join("moved")).unwrap();
                    std::fs::create_dir(&f.store.root).unwrap();
                }
            }
            assert!(f.store.read(&f.g, &r).is_err(), "{mode}");
        }
    }
    #[test]
    fn reobserves_native_protection_and_refuses_vendor_overlap() {
        let f = Fixture::new();
        let r = f.publish();
        std::os::unix::fs::symlink(f.path(&r).join(ATTEMPT), f.root.join("home/config.toml"))
            .unwrap();
        assert!(f.store.read(&f.g, &r).is_err());
        assert!(f.store.publish_attempt(&f.g, &f.attempt).is_err());
        let f = Fixture::new();
        assert!(Store::open(
            &f.root.join("vendor"),
            &f.root.join("vendor"),
            f.store.namespaces.clone()
        )
        .is_err());
        assert!(Store::open(
            &f.root.join("home"),
            &f.root.join("vendor"),
            f.store.namespaces.clone()
        )
        .is_err());
    }
    #[test]
    fn mutation_after_exact_read_is_caught_by_final_inventory() {
        let f = Fixture::new();
        let r = f.publish();
        let artifact = f.path(&r).join(ATTEMPT);
        *f.store.before_audit.lock().unwrap() =
            Some(Box::new(move || std::fs::write(artifact, b"{}").unwrap()));
        assert!(f
            .store
            .read(&f.g, &r)
            .unwrap_err()
            .contains("final inventory"));
    }
    #[cfg(target_os = "macos")]
    #[test]
    fn case_alias_vendor_containment_refuses_before_any_mkdir() {
        let f = Fixture::new();
        let alias = f.root.join("VENDOR");
        // Genuine filesystem alias, not lowercased strings or mocked identity.
        assert_eq!(
            id(&physical_root(&alias).unwrap()).unwrap(),
            id(&physical_root(&f.root.join("vendor")).unwrap()).unwrap()
        );
        assert!(Store::open(&f.root.join("vendor"), &alias, f.store.namespaces.clone()).is_err());
        assert!(!f.root.join("vendor/runtime").exists());
        std::fs::create_dir(f.root.join("vendor/nested")).unwrap();
        assert!(Store::open(
            &f.root.join("vendor/nested"),
            &alias,
            f.store.namespaces.clone()
        )
        .is_err());
        assert!(!f.root.join("vendor/nested/runtime").exists());
        // Reverse containment: vendor is already inside the publication root.
        std::fs::create_dir(f.store.root.join("vendor-child")).unwrap();
        assert!(guard_vendor_domain(
            &f.root.join("APP/runtime/DISTRIBUTION"),
            &f.store.root.join("vendor-child")
        )
        .is_err());
    }
    #[test]
    fn vendor_replaced_by_symlink_at_use_refuses_without_new_publication() {
        let f = Fixture::new();
        let reference = f.publish();
        let before = std::fs::read_dir(&f.store.root).unwrap().count();
        std::fs::rename(f.root.join("vendor"), f.root.join("vendor-old")).unwrap();
        std::os::unix::fs::symlink(&f.store.root, f.root.join("vendor")).unwrap();
        assert!(f.store.read(&f.g, &reference).is_err());
        assert!(f.store.publish_attempt(&f.g, &f.attempt).is_err());
        assert_eq!(std::fs::read_dir(&f.store.root).unwrap().count(), before);
    }
    #[test]
    fn unsupported_standing_or_generation_never_publishes() {
        let f = Fixture::new();
        let mut a = f.attempt.clone();
        a["standing"] = json!("verified");
        assert!(f.store.publish_attempt(&f.g, &a).is_err());
        a = f.attempt.clone();
        a["verificationGeneration"]["spawnCounter"] = json!(2);
        assert!(f.store.publish_attempt(&f.g, &a).is_err());
        assert_eq!(std::fs::read_dir(&f.store.root).unwrap().count(), 0);
    }
}
