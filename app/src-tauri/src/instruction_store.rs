//! Initial instruction copies through retained directory objects. No repair,
//! overwrite or release-default update of an existing user's store.
#[cfg(unix)]
pub(crate) fn seed(
    root: &std::path::Path,
    sources: &[(String, &[u8])],
    after_directories: impl FnOnce(),
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
    // common/four-role defaults, never a generic path publication interface.
    for (path, _) in sources {
        if path != "AGENTS.md"
            && !crate::role_supply::Role::ALL
                .iter()
                .any(|role| path == &format!("agents/AGENT_{}.md", role.name()))
        {
            return Err("instruction source name is not allowed".into());
        }
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
        return verify(&opened, &links);
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
    }
    verify(&opened, &links)
}

#[cfg(not(unix))]
pub(crate) fn seed(
    _: &std::path::Path,
    _: &[(String, &[u8])],
    _: impl FnOnce(),
) -> Result<(), String> {
    Err("directory-bound instruction seeding is unavailable on this target".into())
}
