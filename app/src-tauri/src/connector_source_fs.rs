//! CSP-v0.1 local descriptor capabilities. No writes or pathname fallback.
use std::path::{Path, PathBuf};
pub const LIMIT: usize = 262_144;
#[derive(Debug)]
pub struct ReadBuffer {
    pub bytes: Vec<u8>,
    pub identity: serde_json::Value,
}
#[cfg(unix)]
mod unix {
    use super::*;
    use std::{
        ffi::{CString, OsString},
        fs::{File, Metadata, OpenOptions},
        io::Read,
        os::unix::{
            ffi::OsStrExt,
            fs::{MetadataExt, OpenOptionsExt},
            io::{AsRawFd, FromRawFd},
        },
    };
    pub struct Root {
        original: PathBuf,
        resolved: PathBuf,
        handle: File,
    }
    fn identity(m: &Metadata) -> (u64, u64) {
        (m.dev(), m.ino())
    }
    fn stamp(m: &Metadata) -> (u64, u64, u64, i64, i64, i64, i64) {
        (
            m.dev(),
            m.ino(),
            m.len(),
            m.mtime(),
            m.mtime_nsec(),
            m.ctime(),
            m.ctime_nsec(),
        )
    }
    fn directory(path: &Path) -> Result<File, String> {
        OpenOptions::new()
            .read(true)
            .custom_flags(libc::O_DIRECTORY | libc::O_NOFOLLOW | libc::O_CLOEXEC)
            .open(path)
            .map_err(|e| format!("Project directory unavailable: {e}"))
    }
    fn at(parent: &File, name: &std::ffi::OsStr, is_dir: bool) -> Result<File, String> {
        let name = CString::new(name.as_bytes()).map_err(|_| "NUL in selected path")?;
        let flags = libc::O_RDONLY
            | libc::O_NOFOLLOW
            | libc::O_CLOEXEC
            | libc::O_NONBLOCK
            | libc::O_NOCTTY
            | if is_dir { libc::O_DIRECTORY } else { 0 };
        let fd = unsafe { libc::openat(parent.as_raw_fd(), name.as_ptr(), flags) };
        if fd < 0 {
            return Err(format!(
                "Selected entry refused or unavailable: {}",
                std::io::Error::last_os_error()
            ));
        }
        Ok(unsafe { File::from_raw_fd(fd) })
    }
    impl Root {
        pub fn open(path: &Path) -> Result<Self, String> {
            if !path.is_absolute()
                || path
                    .components()
                    .any(|p| matches!(p, std::path::Component::ParentDir))
            {
                return Err("Explicit absolute project required".into());
            }
            let resolved = path
                .canonicalize()
                .map_err(|e| format!("Project unavailable: {e}"))?;
            let handle = directory(&resolved)?;
            let root = Self {
                original: path.into(),
                resolved,
                handle,
            };
            root.verify()?;
            Ok(root)
        }
        pub(crate) fn project_identity(
            &self,
        ) -> Result<crate::connector_route_store::FileIdentity, String> {
            let m = self.handle.metadata().map_err(|e| e.to_string())?;
            Ok(crate::connector_route_store::FileIdentity {
                device: m.dev(),
                inode: m.ino(),
            })
        }
        pub fn verify(&self) -> Result<(), String> {
            let current = self
                .original
                .canonicalize()
                .map_err(|e| format!("Project association path changed/unavailable: {e}"))?;
            if current != self.resolved
                || identity(&directory(&current)?.metadata().map_err(|e| e.to_string())?)
                    != identity(&self.handle.metadata().map_err(|e| e.to_string())?)
            {
                return Err("Project association directory changed; prepare again".into());
            }
            Ok(())
        }
        pub fn git_location(&self, path: &Path) -> Result<(PathBuf, PathBuf), String> {
            self.verify()?;
            let relative = path
                .strip_prefix(&self.original)
                .or_else(|_| path.strip_prefix(&self.resolved))
                .map_err(|_| "Selection is outside retained project")?;
            if relative.as_os_str().is_empty()
                || relative
                    .components()
                    .any(|c| !matches!(c, std::path::Component::Normal(_)))
            {
                return Err("Invalid private relative selection".into());
            }
            Ok((self.resolved.clone(), relative.to_path_buf()))
        }
        pub fn read(&self, path: &Path) -> Result<ReadBuffer, String> {
            self.read_with(path, |_| {})
        }
        pub(crate) fn read_with(
            &self,
            path: &Path,
            mut hook: impl FnMut(&str),
        ) -> Result<ReadBuffer, String> {
            self.verify()?;
            if !path.is_absolute()
                || path
                    .components()
                    .any(|p| matches!(p, std::path::Component::ParentDir))
            {
                return Err("Selected path is not an absolute project descendant".into());
            }
            let relative = path
                .strip_prefix(&self.original)
                .or_else(|_| path.strip_prefix(&self.resolved))
                .map_err(|_| "Selected source is outside the explicit project")?;
            let names: Vec<OsString> = relative
                .components()
                .map(|p| match p {
                    std::path::Component::Normal(n) => Ok(n.to_owned()),
                    _ => Err("Non-normal selected path component"),
                })
                .collect::<Result<_, _>>()?;
            if names.is_empty() {
                return Err("Select a regular file, not the project directory".into());
            }
            let mut dirs = vec![self.handle.try_clone().map_err(|e| e.to_string())?];
            for name in &names[..names.len() - 1] {
                let next = at(dirs.last().unwrap(), name, true)?;
                dirs.push(next);
            }
            let mut file = at(dirs.last().unwrap(), names.last().unwrap(), false)?;
            let before = file.metadata().map_err(|e| e.to_string())?;
            if !before.is_file() {
                return Err("Selected descriptor is not a regular file".into());
            }
            hook("opened");
            let mut bytes = Vec::new();
            (&mut file)
                .take((LIMIT + 1) as u64)
                .read_to_end(&mut bytes)
                .map_err(|e| format!("Read failed; no partial preview: {e}"))?;
            hook("read");
            let after = file.metadata().map_err(|e| e.to_string())?;
            if stamp(&before) != stamp(&after) {
                return Err("Mutation detected during read; no stable preview".into());
            }
            if bytes.len() > LIMIT {
                return Err("Source exceeds 262144-byte slice limit; no truncated preview".into());
            }
            if bytes.contains(&0) {
                return Err("NUL-bearing source is outside this text slice".into());
            }
            std::str::from_utf8(&bytes)
                .map_err(|_| "Source is not UTF-8; no replacement decoding")?;
            self.verify()?;
            // Rewalk from the retained root and compare every directory/file.
            // This detects ordinary substitutions, not all transient rename races.
            let mut check = self.handle.try_clone().map_err(|e| e.to_string())?;
            for (i, name) in names[..names.len() - 1].iter().enumerate() {
                let next = at(&check, name, true)?;
                if identity(&next.metadata().map_err(|e| e.to_string())?)
                    != identity(&dirs[i + 1].metadata().map_err(|e| e.to_string())?)
                {
                    return Err("Selected directory path changed during read".into());
                }
                check = next;
            }
            let current = at(&check, names.last().unwrap(), false)?;
            if stamp(&current.metadata().map_err(|e| e.to_string())?) != stamp(&after) {
                return Err("Selected file path changed during read".into());
            }
            Ok(ReadBuffer {
                bytes,
                identity: serde_json::json!({"device":after.dev().to_string(),"inode":after.ino().to_string(),"length":after.len(),"modifiedSeconds":after.mtime().to_string(),"modifiedNanoseconds":after.mtime_nsec().to_string()}),
            })
        }
    }
}
#[cfg(unix)]
pub use unix::Root;
#[cfg(not(unix))]
pub struct Root;
#[cfg(not(unix))]
impl Root {
    pub fn open(_: &Path) -> Result<Self, String> {
        Err("CSP descriptor capability unsupported on this platform".into())
    }
    pub fn verify(&self) -> Result<(), String> {
        Err("Unsupported platform".into())
    }
    pub fn read(&self, _: &Path) -> Result<ReadBuffer, String> {
        Err("Unsupported platform".into())
    }
}
