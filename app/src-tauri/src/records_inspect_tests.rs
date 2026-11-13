//! Each function by its answer: a thing that is there, a thing that is not,
//! a dangling link, and a thing that cannot be examined (a real permission
//! failure). Invented material only.
use super::*;
use std::os::unix::fs::{symlink, PermissionsExt};

fn folder(prefix: &str) -> PathBuf {
    let p = std::env::temp_dir().join(crate::util::opaque_id(prefix).unwrap());
    std::fs::create_dir_all(&p).unwrap();
    p
}
fn mode(path: &Path, bits: u32) {
    std::fs::set_permissions(path, std::fs::Permissions::from_mode(bits)).unwrap();
}

#[test]
fn presence_answers_there_not_there_a_dangling_link_and_not_known() {
    let root = folder("inspect-presence-");
    let file = root.join("file");
    std::fs::write(&file, b"invented").unwrap();
    // There: its own metadata.
    assert!(presence(&file).unwrap().is_some_and(|m| m.is_file()));
    // Not there.
    assert!(presence(&root.join("absent")).unwrap().is_none());
    // A dangling link is there, as a link.
    let link = root.join("dangling");
    symlink(root.join("no-target"), &link).unwrap();
    assert!(presence(&link).unwrap().is_some_and(|m| m.file_type().is_symlink()));
    // Not known: the folder above cannot be searched.
    let closed = root.join("closed");
    std::fs::create_dir(&closed).unwrap();
    std::fs::write(closed.join("inside"), b"invented").unwrap();
    mode(&closed, 0o000);
    let answer = presence(&closed.join("inside")).map(|m| m.is_some()).map_err(|e| e.kind());
    mode(&closed, 0o700);
    assert_eq!(answer, Err(io::ErrorKind::PermissionDenied), "never absent when it could not be examined");
    let _ = std::fs::remove_dir_all(&root);
}

#[test]
fn listing_answers_there_not_there_a_dangling_link_and_not_known() {
    let root = folder("inspect-listing-");
    let dir = root.join("dir");
    std::fs::create_dir(&dir).unwrap();
    std::fs::write(dir.join("a-file"), b"invented").unwrap();
    std::fs::create_dir(dir.join("b-folder")).unwrap();
    symlink(dir.join("no-target"), dir.join("c-dangling")).unwrap();
    // There: every entry, each with its own metadata; the dangling link listed as a link.
    let entries = listing(&dir).unwrap().unwrap();
    let kinds: Vec<_> = entries.iter().map(|e| {
        let m = e.metadata.as_ref().unwrap();
        (e.path.file_name().unwrap().to_str().unwrap().to_owned(), m.is_file(), m.is_dir(), m.file_type().is_symlink())
    }).collect();
    assert_eq!(kinds, vec![("a-file".into(), true, false, false), ("b-folder".into(), false, true, false), ("c-dangling".into(), false, false, true)]);
    // Not there.
    assert!(listing(&root.join("absent")).unwrap().is_none());
    // A dangling link in place of the folder is there and never listed as absent.
    let link = root.join("dangling-folder");
    symlink(root.join("no-target"), &link).unwrap();
    assert_eq!(listing(&link).map(|l| l.is_some()).map_err(|e| e.kind()), Err(io::ErrorKind::NotADirectory));
    // Not known, the whole folder: it cannot be listed.
    mode(&dir, 0o000);
    let unlisted = listing(&dir).map(|l| l.map(|e| e.len())).map_err(|e| e.kind());
    mode(&dir, 0o700);
    assert_eq!(unlisted, Err(io::ErrorKind::PermissionDenied));
    // Not known, each entry: the folder can be listed but not searched. Every
    // entry is kept, each with its own error; none dropped.
    mode(&dir, 0o400);
    let unexamined = listing(&dir).map(|l| l.map(|e| e.iter().map(|x| x.metadata.as_ref().map(|_| ()).map_err(|e| e.kind())).collect::<Vec<_>>()));
    mode(&dir, 0o700);
    assert_eq!(unexamined.unwrap().unwrap(), vec![Err(io::ErrorKind::PermissionDenied); 3], "three entries, each not known");
    let _ = std::fs::remove_dir_all(&root);
}
