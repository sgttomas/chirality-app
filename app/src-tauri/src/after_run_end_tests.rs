//! Invented records/captures only; no native person/supplier witness.
use super::*;
#[test]
fn after_run_end_orders_valid_rfc3339_instants_without_rewriting_text() {
    let utc = instant("2026-10-13T12:00:00.123Z").unwrap();
    assert_eq!(instant("2026-10-13T14:30:00.123+02:30"), Some(utc));
    assert!(instant("2026-10-13T12:00:00.123000001Z").unwrap() > utc);
    for bad in [
        "bad",
        "2026-02-30T12:00:00Z",
        "2026-10-13T-1:00:00Z",
        "2026-10-13T12:00:60Z",
        "2026-10-13T12:00:00-00:00",
        "2026-10-13T12:00:00.1234567890Z",
        "2026-10-13T12:00:00+-1:00",
    ] {
        assert_eq!(instant(bad), None, "{bad}");
    }
}
#[test]
fn after_run_end_subject_is_historical_and_never_follows_a_path() {
    let root = Path::new("/invented/project");
    let arrival = json!({"body":{"referents":[{"subject":"output summary: file out/summary.md"}]}});
    assert_eq!(subjects(root, &arrival), vec![root.join("out/summary.md")]);
    for bad in [
        "output summary: file ../outside",
        "output summary: file /outside",
        "output a: file ambiguous: file out/a",
    ] {
        assert!(subjects(root, &json!({"body":{"referents":[{"subject":bad}]}})).is_empty());
    }
}

fn file_fixture() -> (PathBuf, (u64, u64)) {
    let root = std::fs::canonicalize(std::env::temp_dir())
        .unwrap()
        .join(crate::util::opaque_id("ended-file-source-").unwrap());
    std::fs::create_dir(&root).unwrap();
    let m = std::fs::symlink_metadata(&root).unwrap();
    (root, (m.dev(), m.ino()))
}
#[test]
fn ended_file_lapse_reads_owned_bytes_and_proves_absence_without_following_aliases() {
    use crate::checkpoint_recorder::Current;
    use std::os::unix::fs::symlink;
    let (root, owner) = file_fixture();
    let folder = root.join("sub");
    std::fs::create_dir(&folder).unwrap();
    let path = folder.join("leaf");
    std::fs::write(&path, b"v1").unwrap();
    let mut cache = BTreeMap::new();
    assert_eq!(
        current_file(&root, owner, &path, &mut cache),
        Current::Present(crate::util::sha256_hex(b"v1"))
    );
    cache.get_mut(&path).unwrap().read_at = std::fs::metadata(&path).unwrap().ctime() + 2;
    std::fs::rename(&folder, root.join("physical")).unwrap();
    symlink("physical", &folder).unwrap();
    assert!(
        matches!(
            current_file(&root, owner, &path, &mut cache),
            Current::Unavailable(_)
        ),
        "same leaf inode cannot preserve currency through a parent alias"
    );
    std::fs::remove_file(&folder).unwrap();
    std::fs::rename(root.join("physical"), &folder).unwrap();
    std::fs::remove_file(&path).unwrap();
    assert_eq!(
        current_file(&root, owner, &path, &mut cache),
        Current::Absent
    );
    std::fs::remove_dir(&folder).unwrap();
    std::fs::create_dir(root.join("empty")).unwrap();
    symlink("empty", &folder).unwrap();
    assert!(
        matches!(
            current_file(&root, owner, &path, &mut cache),
            Current::Unavailable(_)
        ),
        "a missing leaf behind an alias is not proved absence"
    );
    std::fs::remove_dir_all(root).unwrap();
}
#[test]
fn ended_file_lapse_refuses_nonplain_and_raced_sources_without_blocking() {
    use crate::checkpoint_recorder::Current;
    use std::os::unix::ffi::OsStrExt;
    let (root, owner) = file_fixture();
    let path = root.join("leaf");
    let mut cache = BTreeMap::new();
    let name = std::ffi::CString::new(path.as_os_str().as_bytes()).unwrap();
    assert_eq!(unsafe { libc::mkfifo(name.as_ptr(), 0o600) }, 0);
    assert!(matches!(
        current_file(&root, owner, &path, &mut cache),
        Current::Unavailable(_)
    ));
    std::fs::remove_file(&path).unwrap();
    std::fs::create_dir(&path).unwrap();
    assert!(matches!(
        current_file(&root, owner, &path, &mut cache),
        Current::Unavailable(_)
    ));
    std::fs::remove_dir(&path).unwrap();
    std::fs::write(&path, b"before").unwrap();
    DURING_FILE_READ.with(|hook| {
        *hook.borrow_mut() = Some(Box::new(|path| {
            let replaced = path.with_extension("new");
            std::fs::write(&replaced, b"after").unwrap();
            std::fs::rename(replaced, path).unwrap();
        }))
    });
    assert!(
        matches!(
            current_file(&root, owner, &path, &mut cache),
            Current::Unavailable(_)
        ),
        "opened bytes are not the final named file"
    );
    assert_eq!(
        current_file(&root, owner, &path, &mut cache),
        Current::Present(crate::util::sha256_hex(b"after"))
    );
    assert!(
        matches!(
            current_file(&root, (owner.0, owner.1 + 1), &path, &mut cache),
            Current::Unavailable(_)
        ),
        "no observation transfers to another physical project"
    );
    std::fs::remove_dir_all(root).unwrap();
}
