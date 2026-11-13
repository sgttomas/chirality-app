//! What is there, as the file system answers it, and nothing else.
//!
//! These functions RETURN THE ANSWER ONLY. None of them decides, refuses,
//! logs or words a message for a person: the caller keeps the consequence
//! (a refusal, a limit, a record counted as held), because callers differ in
//! what "not known" means for them, though not in the answer itself.
//!
//! The answer has three parts, and they are never folded together:
//! - there: the thing's own metadata, so a caller can tell the expected
//!   file or folder from another kind or from a link;
//! - not there: only when the system answers NotFound for that lookup, which
//!   establishes absence at that lookup and nothing more (whether absence
//!   is legitimate is the caller's to decide);
//! - not known: any other answer, as the error itself.
//!
//! Links are not followed. A dangling link is there. A caller that needs a
//! link's target examines the target itself, and says so.

use std::fs::Metadata;
use std::io;
use std::path::{Path, PathBuf};

/// Whether `path` is there: its own metadata (a link not followed), `None`
/// only when the system answers NotFound, or the error.
pub(crate) fn presence(path: &Path) -> io::Result<Option<Metadata>> {
    match std::fs::symlink_metadata(path) {
        Ok(metadata) => Ok(Some(metadata)),
        Err(e) if e.kind() == io::ErrorKind::NotFound => Ok(None),
        Err(e) => Err(e),
    }
}

/// One entry of a folder's listing: its path, and its own metadata (a link
/// not followed) or that entry's own error. An entry that cannot be examined
/// is kept, never dropped, so a listing never reads as shorter than it is.
pub(crate) struct Entry {
    pub path: PathBuf,
    pub metadata: io::Result<Metadata>,
}

/// The entries of the folder `dir`, sorted by path: `None` only when the
/// system answers NotFound for `dir`; an error when `dir` is a link (not
/// followed, so never listed as if it were its target), when it cannot be
/// listed, or when the listing cannot be read whole (a failed entry read
/// leaves the names unknown). Each entry carries its own metadata or error.
pub(crate) fn listing(dir: &Path) -> io::Result<Option<Vec<Entry>>> {
    match presence(dir)? {
        None => return Ok(None),
        Some(metadata) if metadata.file_type().is_symlink() => {
            return Err(io::Error::new(io::ErrorKind::NotADirectory, format!("{} is a link, which is not followed", dir.display())));
        }
        Some(_) => {}
    }
    let read = match std::fs::read_dir(dir) {
        Ok(read) => read,
        Err(e) if e.kind() == io::ErrorKind::NotFound => return Ok(None),
        Err(e) => return Err(e),
    };
    let mut entries = Vec::new();
    for entry in read {
        let path = entry?.path();
        let metadata = std::fs::symlink_metadata(&path);
        entries.push(Entry { path, metadata });
    }
    entries.sort_by(|a, b| a.path.cmp(&b.path));
    Ok(Some(entries))
}

#[cfg(test)]
#[path = "records_inspect_tests.rs"]
mod tests;
