//! Content-addressed package copies written by the App (WR §16.2 TX-7 supply
//! copies under `.chirality/workflow-supply/`, WR §4.2 TT-8 trial snapshots
//! under `.chirality/workflow-trials/`).
//!
//! One writer for both. The folder is named by its content, so a folder that
//! already holds exactly these regular files is reused, and one holding other
//! bytes (or a link, a FIFO or any non-regular entry) is refused, never
//! replaced. The App never rewrites or removes a published folder; if the
//! person deletes it, the next writer call recreates it. Destination handling:
//! every step after the ancestor check works relative to the opened parent
//! directory; nothing is opened through a link planted at the destination; the
//! new folder is filled under a hidden staging name and published by an
//! exclusive rename that refuses an existing destination; the published folder
//! is recomputed before it is named.
use super::Snapshot;
use crate::storage;
use std::{fs, path::{Path, PathBuf}};

/// Where the copy is and whether this call wrote it.
#[derive(Debug, Clone, PartialEq, Eq)]
pub(crate) struct ContentCopy {
    pub path: PathBuf,
    /// True when the folder already held exactly these files.
    pub reused: bool,
    /// Hidden `.staging-…` folders beside the copy, left by a write that was
    /// interrupted (a lost process): reported, left as they are.
    pub leftovers: Vec<String>,
}

/// `<root>/.chirality/<area>/<name>/<content key>/<name>`, the WR §3 layout of
/// supply copies and trial snapshots. The content key is `storage::key` of the
/// package content identity, as for the revision store.
pub(crate) fn content_folder(root: &Path, area: &str, name: &str, revision: &str) -> PathBuf {
    root.join(".chirality")
        .join(area)
        .join(name)
        .join(storage::key(revision))
        .join(name)
}

#[cfg(test)]
thread_local! {
    /// Test hook: called once after the staging folder is filled and before
    /// the exclusive rename, with the destination path (a race injection).
    pub(crate) static BEFORE_PUBLISH: std::cell::RefCell<Option<Box<dyn FnOnce(&Path)>>> =
        std::cell::RefCell::new(None);
}

/// Writes `snapshot`'s files at `dest` once, or reuses an identical folder.
/// Refuses (with the cause, writing nothing at `dest`): a link in `dest` or an
/// ancestor, an existing non-folder, an existing folder with other bytes or a
/// non-regular entry, a failed write, and a published folder that does not
/// recompute to `snapshot`'s content identity.
pub(crate) fn write_content_copy(snapshot: &Snapshot, dest: &Path) -> Result<ContentCopy, String> {
    #[cfg(not(unix))]
    {
        let _ = (snapshot, dest);
        return Err("content-addressed package copies are unavailable on this platform".into());
    }
    #[cfg(unix)]
    unix::write(snapshot, dest)
}

/// Reads a content-addressed folder back and says whether it still holds the
/// content it is named for (TT-8 "trial snapshot changed after the trial";
/// "version bytes not available" when it is gone).
#[derive(Debug, Clone, PartialEq, Eq)]
pub(crate) enum CopyStanding {
    Current,
    Changed(String),
    NotAvailable(String),
}
pub(crate) fn copy_standing(dest: &Path, revision: &str) -> CopyStanding {
    match fs::symlink_metadata(dest) {
        Err(e) if e.kind() == std::io::ErrorKind::NotFound => {
            return CopyStanding::NotAvailable("version bytes not available: the folder was removed".into())
        }
        Err(e) => return CopyStanding::NotAvailable(format!("version bytes not available: {e}")),
        Ok(m) if !m.file_type().is_dir() => {
            return CopyStanding::Changed("the folder was replaced by something that is not a folder".into())
        }
        Ok(_) => {}
    }
    if let Err(cause) = storage::check_path(dest) {
        return CopyStanding::Changed(cause);
    }
    match Snapshot::capture(dest) {
        Ok(read) if read.revision() == revision => CopyStanding::Current,
        Ok(read) => CopyStanding::Changed(format!(
            "its bytes now have content identity {}, not {revision}",
            read.revision()
        )),
        Err(cause) => CopyStanding::Changed(cause),
    }
}

#[cfg(unix)]
mod unix {
    use super::*;
    use std::ffi::{CString, OsStr};
    use std::io::Write;
    use std::os::fd::AsRawFd;
    use std::os::unix::ffi::OsStrExt;

    fn cstr(name: &OsStr) -> Result<CString, String> {
        CString::new(name.as_bytes()).map_err(|_| "NUL in a folder or file name".to_string())
    }
    fn open_dir(path: &Path) -> Result<fs::File, String> {
        use std::os::unix::fs::OpenOptionsExt;
        fs::OpenOptions::new()
            .read(true)
            .custom_flags(libc::O_DIRECTORY | libc::O_NOFOLLOW | libc::O_CLOEXEC)
            .open(path)
            .map_err(|e| format!("{}: {e}", path.display()))
    }
    fn open_dir_at(dir: &fs::File, name: &OsStr) -> Result<fs::File, String> {
        crate::workflow_workspace::open_at(dir, name, libc::O_RDONLY | libc::O_DIRECTORY | libc::O_NOFOLLOW)
            .map_err(|e| format!("{}: {e}", name.to_string_lossy()))
    }
    /// A new regular file `name` in `dir`: exclusive, never through a link.
    fn create_at(dir: &fs::File, name: &OsStr) -> std::io::Result<fs::File> {
        use std::os::fd::FromRawFd;
        let c = cstr(name).map_err(std::io::Error::other)?;
        let flags = libc::O_WRONLY | libc::O_CREAT | libc::O_EXCL | libc::O_NOFOLLOW | libc::O_CLOEXEC;
        // SAFETY: an open directory descriptor, a NUL-terminated name and the
        // mode argument O_CREAT requires.
        let fd = unsafe { libc::openat(dir.as_raw_fd(), c.as_ptr(), flags, 0o644 as libc::c_uint) };
        if fd < 0 {
            return Err(std::io::Error::last_os_error());
        }
        // SAFETY: a fresh descriptor owned by nothing else.
        Ok(unsafe { fs::File::from_raw_fd(fd) })
    }
    fn mkdir_at(dir: &fs::File, name: &OsStr) -> Result<(), String> {
        let c = cstr(name)?;
        // SAFETY: an open directory descriptor and a NUL-terminated name.
        if unsafe { libc::mkdirat(dir.as_raw_fd(), c.as_ptr(), 0o755) } != 0 {
            return Err(format!("{}: {}", name.to_string_lossy(), std::io::Error::last_os_error()));
        }
        Ok(())
    }
    /// The entry `name` in `dir`, not following a link: None when absent.
    fn stat_at(dir: &fs::File, name: &OsStr) -> Result<Option<libc::stat>, String> {
        let c = cstr(name)?;
        let mut st = std::mem::MaybeUninit::<libc::stat>::uninit();
        // SAFETY: an open directory descriptor, a NUL-terminated name and a
        // buffer of the right type; the result is read only on success.
        let rc = unsafe {
            libc::fstatat(dir.as_raw_fd(), c.as_ptr(), st.as_mut_ptr(), libc::AT_SYMLINK_NOFOLLOW)
        };
        if rc != 0 {
            let e = std::io::Error::last_os_error();
            if e.kind() == std::io::ErrorKind::NotFound {
                return Ok(None);
            }
            return Err(format!("{}: {e}", name.to_string_lossy()));
        }
        // SAFETY: fstatat succeeded and filled the buffer.
        Ok(Some(unsafe { st.assume_init() }))
    }
    fn kind(st: &libc::stat) -> libc::mode_t {
        st.st_mode & libc::S_IFMT
    }
    /// Exclusive publish: refuses an existing destination of any kind.
    fn rename_no_replace(dir: &fs::File, from: &OsStr, to: &OsStr) -> std::io::Result<()> {
        let (f, t) = (
            cstr(from).map_err(std::io::Error::other)?,
            cstr(to).map_err(std::io::Error::other)?,
        );
        #[cfg(target_os = "macos")]
        // SAFETY: open directory descriptors and NUL-terminated names.
        let rc = unsafe {
            libc::renameatx_np(dir.as_raw_fd(), f.as_ptr(), dir.as_raw_fd(), t.as_ptr(), libc::RENAME_EXCL)
        };
        #[cfg(not(target_os = "macos"))]
        let rc = {
            // Without an exclusive rename the check and the rename are separate
            // steps; rename(2) still never writes through a link at the target.
            if stat_at(dir, to).map_err(std::io::Error::other)?.is_some() {
                return Err(std::io::Error::from(std::io::ErrorKind::AlreadyExists));
            }
            // SAFETY: open directory descriptors and NUL-terminated names.
            unsafe { libc::renameat(dir.as_raw_fd(), f.as_ptr(), dir.as_raw_fd(), t.as_ptr()) }
        };
        if rc != 0 {
            return Err(std::io::Error::last_os_error());
        }
        Ok(())
    }
    /// Fills `staging` (an empty folder this call created) with the files.
    fn fill(staging: &fs::File, snapshot: &Snapshot) -> Result<(), String> {
        let mut dirs: Vec<fs::File> = vec![];
        for (relative, bytes) in snapshot.files() {
            let path = Path::new(relative);
            let mut parts: Vec<&OsStr> = path.iter().collect();
            let file_name = parts.pop().ok_or("empty package path")?;
            let mut here = staging.try_clone().map_err(|e| e.to_string())?;
            for part in parts {
                if stat_at(&here, part)?.is_none() {
                    mkdir_at(&here, part)?;
                }
                let next = open_dir_at(&here, part)?;
                dirs.push(next.try_clone().map_err(|e| e.to_string())?);
                here = next;
            }
            let mut file = create_at(&here, file_name).map_err(|e| format!("{relative}: {e}"))?;
            file.write_all(bytes).map_err(|e| format!("{relative}: {e}"))?;
            file.sync_all().map_err(|e| format!("{relative}: {e}"))?;
        }
        for dir in dirs.iter().chain(std::iter::once(staging)) {
            dir.sync_all().map_err(|e| format!("folder sync: {e}"))?;
        }
        Ok(())
    }
    fn existing(dest: &Path, st: &libc::stat, snapshot: &Snapshot) -> Result<ContentCopy, String> {
        match kind(st) {
            libc::S_IFLNK => Err(format!(
                "{} is a symbolic link; it is not followed and nothing was written",
                dest.display()
            )),
            libc::S_IFDIR => {
                let read = Snapshot::capture(dest).map_err(|cause| {
                    format!("{} exists and cannot be read as a package ({cause}); not replaced", dest.display())
                })?;
                if read.files() != snapshot.files() {
                    return Err(format!(
                        "{} exists and holds other bytes (content identity {}); not replaced",
                        dest.display(),
                        read.revision()
                    ));
                }
                Ok(ContentCopy { path: dest.to_path_buf(), reused: true, leftovers: vec![] })
            }
            _ => Err(format!("{} exists and is not a folder; not replaced", dest.display())),
        }
    }
    pub(super) fn write(snapshot: &Snapshot, dest: &Path) -> Result<ContentCopy, String> {
        let parent = dest.parent().ok_or("copy destination has no parent")?;
        let name = dest.file_name().ok_or("copy destination has no name")?;
        storage::check_path(dest)?;
        storage::ensure_directory(parent)?;
        let dir = open_dir(parent)?;
        let mut copy = match stat_at(&dir, name)? {
            Some(st) => existing(dest, &st, snapshot)?,
            None => {
                let staging_name = std::ffi::OsString::from(format!(
                    ".staging-{}",
                    crate::util::opaque_id("")?
                ));
                mkdir_at(&dir, &staging_name)?;
                let staging_path = parent.join(&staging_name);
                let filled = open_dir_at(&dir, &staging_name).and_then(|staging| fill(&staging, snapshot));
                #[cfg(test)]
                if filled.is_ok() {
                    if let Some(hook) = BEFORE_PUBLISH.with(|h| h.borrow_mut().take()) {
                        hook(dest);
                    }
                }
                let published = filled.and_then(|()| {
                    rename_no_replace(&dir, &staging_name, name).map_err(|e| e.to_string())
                });
                match published {
                    Ok(()) => {
                        dir.sync_all().map_err(|e| format!("folder sync: {e}"))?;
                        ContentCopy { path: dest.to_path_buf(), reused: false, leftovers: vec![] }
                    }
                    Err(cause) => {
                        // The staging folder is this call's own; remove_dir_all
                        // does not follow links inside it.
                        let _ = fs::remove_dir_all(&staging_path);
                        let _ = dir.sync_all();
                        // Another writer may have published the same content.
                        match stat_at(&dir, name)? {
                            Some(st) => existing(dest, &st, snapshot)?,
                            None => return Err(format!("copy not written: {cause}")),
                        }
                    }
                }
            }
        };
        // Staging folders this call did not remove: an interrupted earlier write.
        copy.leftovers = fs::read_dir(parent)
            .map(|d| {
                d.filter_map(Result::ok)
                    .map(|e| e.file_name().to_string_lossy().into_owned())
                    .filter(|n| n.starts_with(".staging-"))
                    .map(|n| format!("staging folder left by an interrupted write (left as it is): {}", parent.join(n).display()))
                    .collect()
            })
            .unwrap_or_default();
        // Recomputed before it is named (TX-7, TT-8).
        match Snapshot::capture(dest) {
            Ok(read) if read.revision() == snapshot.revision() => Ok(copy),
            Ok(read) => Err(format!(
                "{} does not recompute (content identity {}, expected {})",
                dest.display(),
                read.revision(),
                snapshot.revision()
            )),
            Err(cause) => Err(format!("{} does not recompute: {cause}", dest.display())),
        }
    }
}
