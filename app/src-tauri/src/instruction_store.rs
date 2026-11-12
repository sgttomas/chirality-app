//! Initial instruction copies through retained directory objects. No repair,
//! overwrite or release-default update of an existing user's store.
#[cfg(unix)]
pub(crate) fn seed(
    root: &std::path::Path,
    sources: &[(String, &[u8])],
    release: &str,
    after_directories: impl FnOnce(),
    validate: impl FnOnce() -> Result<(), String>,
) -> Result<(), String> {
    use std::{
        ffi::{CString, OsString},
        fs::{File, OpenOptions},
        io::Write,
        os::unix::{
            ffi::OsStrExt,
            fs::{MetadataExt, OpenOptionsExt},
            io::{AsRawFd, FromRawFd},
        },
        path::{Component, Path},
    };
    fn directory(path: &Path) -> Result<File, String> {
        OpenOptions::new()
            .read(true)
            .custom_flags(libc::O_DIRECTORY | libc::O_NOFOLLOW | libc::O_NONBLOCK | libc::O_CLOEXEC)
            .open(path)
            .map_err(|e| e.to_string())
    }
    fn name(value: &std::ffi::OsStr) -> Result<CString, String> {
        CString::new(value.as_bytes()).map_err(|_| "NUL in instruction directory name".into())
    }
    fn at(parent: &File, value: &std::ffi::OsStr) -> Result<File, String> {
        let value = name(value)?;
        let flags = libc::O_RDONLY
            | libc::O_DIRECTORY
            | libc::O_NOFOLLOW
            | libc::O_NONBLOCK
            | libc::O_CLOEXEC
            | libc::O_NOCTTY;
        let fd = unsafe { libc::openat(parent.as_raw_fd(), value.as_ptr(), flags, 0o666) };
        if fd < 0 {
            return Err(std::io::Error::last_os_error().to_string());
        }
        Ok(unsafe { File::from_raw_fd(fd) })
    }
    fn identity(file: &File) -> Result<(u64, u64), String> {
        let meta = file.metadata().map_err(|e| e.to_string())?;
        Ok((meta.dev(), meta.ino()))
    }
    fn child(parent: &File, value: &std::ffi::OsStr) -> Result<(File, bool), String> {
        let c = name(value)?;
        let created = unsafe { libc::mkdirat(parent.as_raw_fd(), c.as_ptr(), 0o777) } == 0;
        if !created {
            let error = std::io::Error::last_os_error();
            if error.kind() != std::io::ErrorKind::AlreadyExists {
                return Err(error.to_string());
            }
        }
        let opened = at(parent, value)?;
        opened.sync_all().map_err(|e| e.to_string())?;
        parent.sync_all().map_err(|e| e.to_string())?;
        Ok((opened, created))
    }
    // Validate every leaf before creating anything. Inputs are the compiled
    // common, four-role and delegation defaults, never a generic path
    // publication interface.
    let mut names = std::collections::BTreeSet::new();
    for (path, _) in sources {
        if !crate::role_supply::guidance_path(path) {
            return Err("instruction source name is not allowed".into());
        }
        if !names.insert(path) {
            return Err("duplicate instruction source name".into());
        }
    }
    if names.len() != crate::role_supply::Role::ALL.len() + 2 || release.is_empty() {
        return Err("complete instruction defaults and release are required".into());
    }
    let leaf = match root.components().next_back() {
        Some(Component::Normal(value)) => value.to_owned(),
        _ => return Err("initial instruction root needs a normal directory name".into()),
    };
    let parent = root.parent().ok_or("instruction root has no parent")?;
    let parent = if parent.as_os_str().is_empty() {
        Path::new(".")
    } else {
        parent
    };
    let mut ancestor = parent;
    let mut missing = Vec::<OsString>::new();
    let resolved = loop {
        match ancestor.canonicalize() {
            Ok(value) => break value,
            Err(error) if error.kind() == std::io::ErrorKind::NotFound => {
                let value = match ancestor.components().next_back() {
                    Some(Component::Normal(value)) => value.to_owned(),
                    _ => return Err("missing instruction ancestor has no normal name".into()),
                };
                missing.push(value);
                ancestor = ancestor
                    .parent()
                    .ok_or("instruction parent has no existing ancestor")?;
                if ancestor.as_os_str().is_empty() {
                    ancestor = Path::new(".");
                }
            }
            Err(error) => return Err(error.to_string()),
        }
    };
    let base = directory(&resolved)?;
    let mut opened = vec![base];
    let mut links = Vec::<OsString>::new();
    // Recheck the selected existing ancestor before any creates. Ancestor
    // aliases retain their meaning; managed entries are opened no-follow.
    let verify = |opened: &[File], links: &[OsString]| -> Result<(), String> {
        let current = ancestor.canonicalize().map_err(|e| e.to_string())?;
        if current != resolved || identity(&directory(&current)?)? != identity(&opened[0])? {
            return Err("instruction ancestor changed during seed".into());
        }
        for (index, link) in links.iter().enumerate() {
            if identity(&at(&opened[index], link)?)? != identity(&opened[index + 1])? {
                return Err("instruction directory changed during seed".into());
            }
        }
        Ok(())
    };
    verify(&opened, &links)?;
    for value in missing.into_iter().rev() {
        verify(&opened, &links)?;
        let (next, _) = child(opened.last().unwrap(), &value)?;
        links.push(value);
        opened.push(next);
    }
    verify(&opened, &links)?;
    let (store, created) = child(opened.last().unwrap(), &leaf)?;
    if !created {
        // Another actor established the store after initial absence admission.
        // The wrapper validates it without adding or repairing any copies.
        verify(&opened, &links)?;
        return validate();
    }
    links.push(leaf);
    opened.push(store);
    let root_index = opened.len() - 1;
    let agents_name = OsString::from("agents");
    verify(&opened, &links)?;
    let (agents, _) = child(&opened[root_index], &agents_name)?;
    links.push(agents_name);
    opened.push(agents);
    after_directories();
    let mut created_files = Vec::new();
    let mut preserved_files = Vec::new();
    for (path, bytes) in sources {
        verify(&opened, &links)?;
        let (parent, leaf) = match path.strip_prefix("agents/") {
            Some(value) => (opened.last().unwrap(), value),
            None => (&opened[root_index], path.as_str()),
        };
        let leaf = std::ffi::OsStr::new(leaf);
        let c = name(leaf)?;
        let flags = libc::O_WRONLY
            | libc::O_CREAT
            | libc::O_EXCL
            | libc::O_NOFOLLOW
            | libc::O_NONBLOCK
            | libc::O_CLOEXEC
            | libc::O_NOCTTY;
        let fd = unsafe { libc::openat(parent.as_raw_fd(), c.as_ptr(), flags, 0o666) };
        if fd < 0 {
            let error = std::io::Error::last_os_error();
            if error.kind() == std::io::ErrorKind::AlreadyExists {
                preserved_files.push(serde_json::json!({"path": path, "origin": "unknown"}));
                continue;
            }
            return Err(error.to_string());
        }
        let mut file = unsafe { File::from_raw_fd(fd) };
        if !file.metadata().map_err(|e| e.to_string())?.is_file() {
            return Err("created instruction source is not a regular file".into());
        }
        file.write_all(bytes)
            .and_then(|_| file.sync_all())
            .map_err(|e| e.to_string())?;
        parent.sync_all().map_err(|e| e.to_string())?;
        verify(&opened, &links)?;
        created_files.push(serde_json::json!({"path": path,
            "defaultContent": crate::role_supply::content(bytes)}));
    }
    validate()?;
    verify(&opened, &links)?;
    let record = serde_json::json!({"format": crate::role_supply::seed_history::SEED_FORMAT,
        "release": release, "created": created_files, "preserved": preserved_files});
    let mut raw = serde_json::to_vec(&record).map_err(|e| e.to_string())?;
    raw.push(b'\n');
    let leaf = name(std::ffi::OsStr::new(crate::role_supply::seed_history::SEED_RECORD))?;
    let fd = unsafe { libc::openat(opened[root_index].as_raw_fd(), leaf.as_ptr(),
        libc::O_WRONLY | libc::O_CREAT | libc::O_EXCL | libc::O_NOFOLLOW
            | libc::O_NONBLOCK | libc::O_CLOEXEC | libc::O_NOCTTY, 0o666) };
    if fd < 0 {
        return Err(format!("instruction seed record was not created: {}",
            std::io::Error::last_os_error()));
    }
    // Publication is exclusive, not transactional: a failed write/sync may
    // leave partial record bytes. No later call silently repairs that artifact.
    let mut record_file = unsafe { File::from_raw_fd(fd) };
    record_file.write_all(&raw).and_then(|_| record_file.sync_all())
        .map_err(|e| format!("instruction seed record publication failed: {e}"))?;
    opened[root_index].sync_all().map_err(|e| e.to_string())?;
    verify(&opened, &links)
}

#[cfg(test)]
thread_local! {
    /// Run once, just after a later-added file is made visible and before its
    /// addition record is written, so a test can interrupt the placement there.
    pub(crate) static AFTER_VISIBLE: std::cell::RefCell<Option<Box<dyn FnOnce()>>> = const { std::cell::RefCell::new(None) };
}

/// Place, once, a file this release adds to a store first seeded without it.
/// Nothing already in the store is opened for writing. The file is created
/// only on affirmative evidence: the first seed record is read, valid and
/// names the files of a store seeded without it, and no addition record for
/// it exists. Otherwise nothing is placed and its absence is a missing file.
///
/// Evidence comes before effect. A marker that the placement was begun is
/// written first; then the file, written whole under a scratch name and linked
/// into place without replacing anything; then the addition record, naming it
/// as created or, when a file was already there, as preserved; then the marker
/// is removed. A marker found with no addition record means an earlier
/// placement was begun and not recorded as finished: whether the file was
/// never made or was made and then removed by the person cannot be told, so
/// nothing is placed. An absent file stays missing, and a present one is left
/// as it is and recorded as preserved. The addition record governs: once it
/// exists, a marker left beside it means nothing.
#[cfg(unix)]
pub(crate) fn add_later(
    root: &std::path::Path,
    path: &str,
    bytes: &[u8],
    release: &str,
) -> Result<(), String> {
    use crate::role_supply::seed_history;
    use std::{
        ffi::CString,
        fs::{File, OpenOptions},
        io::{Read, Write},
        os::unix::{
            fs::OpenOptionsExt,
            io::{AsRawFd, FromRawFd},
        },
    };
    let record_name = seed_history::addition_record(path)
        .ok_or("instruction source is not one a later release adds")?;
    if path.contains('/') || release.is_empty() || bytes.is_empty() {
        return Err("instruction addition is not a store-root default".into());
    }
    let dir = OpenOptions::new()
        .read(true)
        .custom_flags(libc::O_DIRECTORY | libc::O_NOFOLLOW | libc::O_NONBLOCK | libc::O_CLOEXEC)
        .open(root)
        .map_err(|e| e.to_string())?;
    let open = |leaf: &str, flags: i32| -> Result<Option<File>, String> {
        let c = CString::new(leaf).map_err(|_| "NUL in instruction name")?;
        let fd = unsafe {
            libc::openat(dir.as_raw_fd(), c.as_ptr(),
                flags | libc::O_NOFOLLOW | libc::O_NONBLOCK | libc::O_CLOEXEC | libc::O_NOCTTY, 0o666)
        };
        if fd < 0 {
            let error = std::io::Error::last_os_error();
            return match error.kind() {
                std::io::ErrorKind::NotFound | std::io::ErrorKind::AlreadyExists => Ok(None),
                _ => Err(error.to_string()),
            };
        }
        Ok(Some(unsafe { File::from_raw_fd(fd) }))
    };
    let exists = |leaf: &str| -> Result<bool, String> {
        let c = CString::new(leaf).map_err(|_| "NUL in instruction name")?;
        let mut m = std::mem::MaybeUninit::<libc::stat>::uninit();
        if unsafe { libc::fstatat(dir.as_raw_fd(), c.as_ptr(), m.as_mut_ptr(), libc::AT_SYMLINK_NOFOLLOW) } == 0 {
            return Ok(true);
        }
        let error = std::io::Error::last_os_error();
        if error.kind() == std::io::ErrorKind::NotFound { Ok(false) } else { Err(error.to_string()) }
    };
    let begun = seed_history::addition_begun(path)
        .ok_or("instruction source is not one a later release adds")?;
    let scratch = format!(".{path}.placing");
    // Best effort: these remove only the App's own marker and scratch file.
    let remove = |leaf: &str| {
        if let Ok(c) = CString::new(leaf) {
            unsafe { libc::unlinkat(dir.as_raw_fd(), c.as_ptr(), 0) };
        }
    };
    if exists(record_name)? {
        // The placement was recorded as finished; a marker left behind is spent.
        remove(begun);
        return Ok(());
    }
    // Only affirmative evidence that the store predates this file permits it:
    // a first seed record that is read, valid and names the files of a store
    // seeded without it. A missing, unreadable, oversized or malformed record
    // is no such evidence: nothing is placed, and the file reads as missing.
    let predates = match open(seed_history::SEED_RECORD, libc::O_RDONLY) {
        Ok(Some(mut file)) => {
            let mut raw = Vec::new();
            file.metadata().is_ok_and(|m| m.is_file())
                && (&mut file).take(16 * 1024 + 1).read_to_end(&mut raw).is_ok()
                && raw.len() <= 16 * 1024
                && seed_history::seeded_paths(&raw).is_some_and(|paths| !paths.contains(path))
        }
        _ => false,
    };
    if !predates {
        return Ok(());
    }
    let preserved = || serde_json::json!({"created":[],"preserved":[{"path":path,"origin":"unknown"}]});
    let entry = if exists(begun)? {
        // Begun earlier and not recorded as finished. Nothing is placed again.
        remove(&scratch);
        if !exists(path)? {
            return Ok(());
        }
        preserved()
    } else {
        let marker = serde_json::json!({"format":seed_history::ADDITION_BEGUN_FORMAT,"release":release,"path":path});
        let mut raw = serde_json::to_vec(&marker).map_err(|e| e.to_string())?;
        raw.push(b'\n');
        match open(begun, libc::O_WRONLY | libc::O_CREAT | libc::O_EXCL)? {
            Some(mut file) => {
                if let Err(e) = file.write_all(&raw).and_then(|_| file.sync_all()).and_then(|_| dir.sync_all()) {
                    // Nothing has been made visible, so the marker claims nothing worth keeping.
                    remove(begun);
                    return Err(format!("instruction addition could not be begun: {e}"));
                }
            }
            // Another start began it between the check and this one; that start places it.
            None => return Ok(()),
        }
        // Until the link below, nothing is visible at the guidance path: a
        // failure here withdraws the marker, and where that fails too the
        // marker stands and nothing is placed later.
        let written = (|| -> Result<Option<()>, String> {
            // The scratch name is the App's own. One found without a marker is
            // not known to be the App's and is left alone: nothing is placed.
            let Some(mut file) = open(&scratch, libc::O_WRONLY | libc::O_CREAT | libc::O_EXCL)? else {
                return Ok(None);
            };
            if !file.metadata().map_err(|e| e.to_string())?.is_file() {
                return Err("created instruction source is not a regular file".into());
            }
            file.write_all(bytes).and_then(|_| file.sync_all()).map_err(|e| e.to_string())?;
            Ok(Some(()))
        })();
        match written {
            Ok(Some(())) => {}
            Ok(None) => {
                remove(begun);
                return Ok(());
            }
            Err(e) => {
                remove(&scratch);
                remove(begun);
                return Err(e);
            }
        }
        // The guidance path receives the whole default or nothing, and nothing there is replaced.
        let (from, to) = (CString::new(scratch.as_str()).map_err(|_| "NUL in instruction name")?,
            CString::new(path).map_err(|_| "NUL in instruction name")?);
        let linked = unsafe { libc::linkat(dir.as_raw_fd(), from.as_ptr(), dir.as_raw_fd(), to.as_ptr(), 0) };
        let error = std::io::Error::last_os_error();
        remove(&scratch);
        if linked == 0 {
            dir.sync_all().map_err(|e| e.to_string())?;
            #[cfg(test)]
            AFTER_VISIBLE.with(|hook| {
                if let Some(run) = hook.borrow_mut().take() {
                    run()
                }
            });
            serde_json::json!({"created":[{"path":path,"defaultContent":crate::role_supply::content(bytes)}],"preserved":[]})
        } else if error.kind() == std::io::ErrorKind::AlreadyExists {
            preserved()
        } else {
            remove(begun);
            return Err(error.to_string());
        }
    };
    let record = serde_json::json!({"format":seed_history::ADDITION_FORMAT,"release":release,
        "created":entry["created"],"preserved":entry["preserved"]});
    let mut raw = serde_json::to_vec(&record).map_err(|e| e.to_string())?;
    raw.push(b'\n');
    // Exclusive, like the first seed record: a concurrent addition keeps its own.
    if let Some(mut file) = open(record_name, libc::O_WRONLY | libc::O_CREAT | libc::O_EXCL)? {
        file.write_all(&raw).and_then(|_| file.sync_all())
            .map_err(|e| format!("instruction addition record publication failed: {e}"))?;
        dir.sync_all().map_err(|e| e.to_string())?;
    }
    remove(begun);
    Ok(())
}

#[cfg(not(unix))]
pub(crate) fn add_later(_: &std::path::Path, _: &str, _: &[u8], _: &str) -> Result<(), String> {
    Err("directory-bound instruction addition is unavailable on this target".into())
}

#[cfg(not(unix))]
pub(crate) fn seed(
    _: &std::path::Path,
    _: &[(String, &[u8])],
    _: &str,
    _: impl FnOnce(),
    _: impl FnOnce() -> Result<(), String>,
) -> Result<(), String> {
    Err("directory-bound instruction seeding is unavailable on this target".into())
}
