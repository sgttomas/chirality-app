//! The Working Files folder on invented folders: where it is, what it refuses,
//! and that a folder handed out is the one the App made, or the start is refused.
use super::*;
use std::ffi::OsStr;

use std::os::unix::fs::PermissionsExt;

struct Fixture {
    root: PathBuf,
    data: PathBuf,
}
impl Fixture {
    fn new() -> Fixture {
        let root = std::fs::canonicalize(std::env::temp_dir()).unwrap().join(crate::util::opaque_id("working-files-test-").unwrap());
        let data = root.join("invented.app.data");
        std::fs::create_dir_all(&data).unwrap();
        Fixture { root, data }
    }
    fn working(&self) -> WorkingFiles {
        establish(&self.data).unwrap()
    }
}
impl Drop for Fixture {
    fn drop(&mut self) {
        let _ = std::fs::remove_dir_all(&self.root);
    }
}

#[test]
fn the_folder_is_beside_app_data_named_from_it_in_one_place() {
    let f = Fixture::new();
    assert_eq!(folder_for(&f.data).unwrap(), f.root.join("invented.app.data Working Files"));
    let w = f.working();
    assert_eq!(w.root(), f.root.join("invented.app.data Working Files"));
    for kind in Kind::ALL {
        let meta = std::fs::symlink_metadata(w.root().join(kind.subtree())).unwrap();
        assert!(meta.is_dir() && meta.mode() & 0o777 == 0o700, "{kind:?}");
    }
    assert!(!w.root().starts_with(&f.data) && !f.data.starts_with(w.root()), "beside App data, never in it");
}

#[test]
fn a_start_is_refused_with_words_the_person_can_act_on_when_the_folder_is_not_the_apps() {
    let cases: [(&str, fn(&Path)); 3] = [
        ("a file", |p| std::fs::write(p, b"invented").unwrap()),
        ("a link to", |p| std::os::unix::fs::symlink("/private/tmp", p).unwrap()),
        ("other accounts can use", |p| {
            std::fs::create_dir(p).unwrap();
            std::fs::set_permissions(p, std::fs::Permissions::from_mode(0o755)).unwrap();
        }),
    ];
    for (said, plant) in cases {
        let f = Fixture::new();
        let folder = folder_for(&f.data).unwrap();
        plant(&folder);
        let refused = establish(&f.data).unwrap_err();
        assert!(refused.contains(&folder.display().to_string()) && refused.contains(said) && refused.contains("start Chirality again"), "{refused}");
        // Nothing replaced it: what was planted is still there, as it was.
        assert!(std::fs::symlink_metadata(&folder).is_ok());
    }
}

fn record_of(w: &WorkingFiles, made: &Made) -> PathBuf {
    w.subtree(made.kind).join(format!("{RECORD_PREFIX}{}.json", made.name))
}

// The positive evidence that a folder handed out is the one the App made, each
// piece shown on a permitted allocation and then invalidated through the real
// path, with the start refused.

#[test]
fn a_folder_handed_out_is_new_empty_private_recorded_and_in_the_verified_subtree() {
    let f = Fixture::new();
    let w = f.working();
    for kind in Kind::ALL {
        let made = w.allocate(kind).unwrap();
        let meta = std::fs::symlink_metadata(&made.path).unwrap();
        assert!(meta.is_dir() && meta.mode() & 0o777 == 0o700, "{kind:?}");
        assert_eq!(made.path.parent(), Some(w.subtree(kind).as_path()));
        assert_eq!((meta.dev(), meta.ino()), (made.stamp.dev, made.stamp.ino));
        assert_eq!(std::fs::read_dir(&made.path).unwrap().count(), 0);
        let record = std::fs::symlink_metadata(record_of(&w, &made)).unwrap();
        assert!(record.is_file() && record.nlink() == 1 && record.mode() & 0o777 == 0o600);
        let body: serde_json::Value = serde_json::from_slice(&std::fs::read(record_of(&w, &made)).unwrap()).unwrap();
        assert_eq!(body["name"], made.name.as_str());
        assert_ne!(made.path, w.allocate(kind).unwrap().path, "each allocation is its own");
    }
}

#[test]
fn a_working_files_folder_or_subtree_that_is_no_longer_the_one_established_refuses_the_start() {
    // found (first reading): the Working Files folder replaced by a link let a folder be made in App data.
    let f = Fixture::new();
    let w = f.working();
    assert!(w.allocate(Kind::ProbeHome).is_ok(), "permitted");
    std::fs::rename(w.root(), f.root.join("parked")).unwrap();
    std::os::unix::fs::symlink(&f.data, w.root()).unwrap();
    std::fs::DirBuilder::new().mode(0o700).create(f.data.join("probe-homes")).unwrap();
    let refused = w.allocate(Kind::ProbeHome).unwrap_err();
    assert!(refused.contains("could not be opened as a folder") && refused.contains("start Chirality again"), "{refused}");
    assert_eq!(std::fs::read_dir(f.data.join("probe-homes")).unwrap().count(), 0, "nothing made in App data");
    // A subtree replaced by another folder of the same name, or opened to other accounts.
    let f = Fixture::new();
    let w = f.working();
    let subtree = w.subtree(Kind::CodexTmp);
    std::fs::rename(&subtree, f.root.join("parked-subtree")).unwrap();
    std::fs::DirBuilder::new().mode(0o700).create(&subtree).unwrap();
    assert!(w.allocate(Kind::CodexTmp).unwrap_err().contains("no longer the folder Chirality made"));
    assert_eq!(std::fs::read_dir(&subtree).unwrap().count(), 0, "nothing made in the replacement");
    let f = Fixture::new();
    let w = f.working();
    std::fs::set_permissions(w.subtree(Kind::Connector), std::fs::Permissions::from_mode(0o755)).unwrap();
    let refused = w.allocate(Kind::Connector).unwrap_err();
    assert!(refused.contains("is not private now") && refused.contains("Other accounts can use it"), "{refused}");
}

#[test]
fn a_folder_that_is_not_new_empty_and_private_is_not_used() {
    let f = Fixture::new();
    let w = f.working();
    let subtree = w.open_subtree(Kind::CodexTmp).unwrap();
    let before = std::time::SystemTime::now();
    let fresh = w.subtree(Kind::CodexTmp).join("tmp-invented-fresh");
    std::fs::DirBuilder::new().mode(0o700).create(&fresh).unwrap();
    assert!(WorkingFiles::made_folder(&subtree, OsStr::new("tmp-invented-fresh"), before).is_ok(), "permitted");
    std::fs::write(fresh.join("invented"), b"x").unwrap();
    assert_eq!(WorkingFiles::made_folder(&subtree, OsStr::new("tmp-invented-fresh"), before).unwrap_err(), "it is not empty");
    std::fs::remove_file(fresh.join("invented")).unwrap();
    std::fs::set_permissions(&fresh, std::fs::Permissions::from_mode(0o755)).unwrap();
    assert!(WorkingFiles::made_folder(&subtree, OsStr::new("tmp-invented-fresh"), before).unwrap_err().contains("not a private folder"));
    std::fs::set_permissions(&fresh, std::fs::Permissions::from_mode(0o700)).unwrap();
    let later = std::time::SystemTime::now() + std::time::Duration::from_secs(5);
    assert_eq!(WorkingFiles::made_folder(&subtree, OsStr::new("tmp-invented-fresh"), later).unwrap_err(), "it was created before Chirality made it");
    std::os::unix::fs::symlink(&fresh, w.subtree(Kind::CodexTmp).join("tmp-invented-link")).unwrap();
    assert!(WorkingFiles::made_folder(&subtree, OsStr::new("tmp-invented-link"), before).unwrap_err().contains("could not be opened as a folder"));
}

#[test]
fn a_name_that_no_longer_leads_to_the_folder_made_refuses_the_start() {
    // found (second reading, 3): the path returned could lead to another folder than the one made.
    let f = Fixture::new();
    let w = f.working();
    let subtree = w.open_subtree(Kind::CodexTmp).unwrap();
    let path = w.subtree(Kind::CodexTmp).join("tmp-invented");
    std::fs::DirBuilder::new().mode(0o700).create(&path).unwrap();
    let (folder, _) = WorkingFiles::made_folder(&subtree, OsStr::new("tmp-invented"), std::time::SystemTime::now() - std::time::Duration::from_secs(1)).unwrap();
    assert!(WorkingFiles::still_named(&subtree, OsStr::new("tmp-invented"), &folder).is_ok(), "permitted");
    let foreign = f.root.join("invented-foreign");
    std::fs::create_dir(&foreign).unwrap();
    std::fs::rename(&path, f.root.join("parked")).unwrap();
    std::os::unix::fs::symlink(&foreign, &path).unwrap();
    assert_eq!(WorkingFiles::still_named(&subtree, OsStr::new("tmp-invented"), &folder).unwrap_err(), "its name now leads somewhere else");
    std::fs::remove_file(&path).unwrap();
    std::fs::DirBuilder::new().mode(0o700).create(&path).unwrap();
    assert_eq!(WorkingFiles::still_named(&subtree, OsStr::new("tmp-invented"), &folder).unwrap_err(), "its name now leads somewhere else", "another folder of the same name");
}

#[test]
fn a_record_is_made_new_and_nothing_at_a_record_name_is_read_or_replaced() {
    // found (second reading, 4): a foreign file renamed to the record's name was read and replaced.
    let f = Fixture::new();
    let w = f.working();
    let subtree_path = w.subtree(Kind::ProbeHome);
    let foreign = subtree_path.join(".made.json");
    std::fs::write(&foreign, b"{\"made\":[],\"invented\":\"keep this\"}").unwrap();
    // Unreadable, so any reading of it would fail the allocation rather than pass unseen.
    std::fs::set_permissions(&foreign, std::fs::Permissions::from_mode(0o000)).unwrap();
    let before = std::fs::symlink_metadata(&foreign).unwrap();
    assert!(w.allocate(Kind::ProbeHome).is_ok());
    let after = std::fs::symlink_metadata(&foreign).unwrap();
    assert_eq!((before.ino(), before.len()), (after.ino(), after.len()), "never read or replaced");
    std::fs::set_permissions(&foreign, std::fs::Permissions::from_mode(0o600)).unwrap();
    // A file already at the very name a record would take: the record is not made over it.
    let subtree = w.open_subtree(Kind::ProbeHome).unwrap();
    let taken = subtree_path.join(format!("{RECORD_PREFIX}probe-invented.json"));
    std::fs::write(&taken, b"invented").unwrap();
    let stamp = Stamp { dev: 0, ino: 0, created_secs: 0, created_nanos: 0 };
    assert!(WorkingFiles::write_record(&subtree, "probe-invented", stamp).is_err());
    assert_eq!(std::fs::read(&taken).unwrap(), b"invented");
    // A link at that name is not followed.
    let target = f.root.join("invented-target");
    std::fs::write(&target, b"untouched").unwrap();
    std::os::unix::fs::symlink(&target, subtree_path.join(format!("{RECORD_PREFIX}probe-linked.json"))).unwrap();
    assert!(WorkingFiles::write_record(&subtree, "probe-linked", stamp).is_err());
    assert_eq!(std::fs::read(&target).unwrap(), b"untouched");
}

#[test]
fn nothing_is_removed_and_every_folder_is_counted() {
    let f = Fixture::new();
    let w = f.working();
    let made: Vec<Made> = Kind::ALL.iter().map(|kind| w.allocate(*kind).unwrap()).collect();
    for m in &made {
        std::fs::write(m.path.join("invented"), b"x").unwrap();
    }
    // A later launch establishes the same folder again and removes nothing.
    let later = f.working();
    let _ = later.allocate(Kind::CodexTmp).unwrap();
    for m in &made {
        assert!(m.path.join("invented").exists());
    }
    assert_eq!(kept_count(&f.data), Some(4), "the records are not counted as folders");
}

#[test]
fn no_record_or_subtree_is_inside_a_folder_the_app_hands_out() {
    // Every record, its subtree and the Working Files folder lie outside every made folder,
    // the one given to Codex as its TMPDIR and the probe's home included.
    let f = Fixture::new();
    let w = f.working();
    for kind in Kind::ALL {
        let made = w.allocate(kind).unwrap();
        for other in Kind::ALL {
            for control in [record_of(&w, &made), w.subtree(other), w.root().to_path_buf()] {
                assert!(!control.starts_with(&made.path), "{kind:?} holds {}", control.display());
            }
        }
    }
}

/// An access-list entry on an invented folder, through the system's own tool.
fn add_entry(path: &Path, entry: &str) {
    let done = std::process::Command::new("/bin/chmod").arg("+a").arg(entry).arg(path).status().unwrap();
    assert!(done.success(), "chmod +a {entry}");
}

#[test]
fn an_access_list_that_allows_refuses_the_start_and_a_deny_only_list_does_not() {
    // Through establish: an allowing entry on the Working Files folder refuses, words and all.
    let f = Fixture::new();
    let root = folder_for(&f.data).unwrap();
    std::fs::DirBuilder::new().mode(0o700).create(&root).unwrap();
    add_entry(&root, "everyone allow list,search");
    let refused = establish(&f.data).unwrap_err();
    assert!(refused.contains("access list that gives access beyond your account") && refused.contains(&root.display().to_string()) && refused.contains("start Chirality again"), "{refused}");
    // A deny-only list passes: a deny gives no one access.
    let f = Fixture::new();
    let root = folder_for(&f.data).unwrap();
    std::fs::DirBuilder::new().mode(0o700).create(&root).unwrap();
    add_entry(&root, "everyone deny delete");
    let w = establish(&f.data).unwrap();
    assert!(w.allocate(Kind::CodexTmp).is_ok());
    // Through allocate: an allowing entry added to a subtree after it was established refuses.
    add_entry(&w.subtree(Kind::CodexTmp), "everyone allow list,search,add_file");
    let refused = w.allocate(Kind::CodexTmp).unwrap_err();
    assert!(refused.contains("access list that gives access beyond your account"), "{refused}");
    // An allowing entry meant only to be inherited is refused where it is, before any folder is
    // made under it.
    let f = Fixture::new();
    let w = f.working();
    add_entry(&w.subtree(Kind::Connector), "everyone allow list,search,file_inherit,directory_inherit,only_inherit");
    let refused = w.allocate(Kind::Connector).unwrap_err();
    assert!(refused.contains("access list that gives access beyond your account"), "{refused}");
    assert_eq!(kept_count(&f.data), Some(0), "nothing made under it");
}

#[test]
fn the_folder_holding_the_working_files_entry_must_not_be_writable_by_another_account() {
    for (what, plant) in [("its mode", "mode"), ("access list", "acl")] {
        let f = Fixture::new();
        if plant == "mode" {
            std::fs::set_permissions(&f.root, std::fs::Permissions::from_mode(0o777)).unwrap();
        } else {
            add_entry(&f.root, "everyone allow add_subdirectory,delete_child");
        }
        let refused = establish(&f.data).unwrap_err();
        assert!(refused.contains(&f.root.display().to_string()) && refused.contains(what) && refused.contains("changes no folder's access"), "{plant}: {refused}");
        assert!(!folder_for(&f.data).unwrap().exists(), "{plant}: nothing made");
    }
    // A deny-only list on it passes.
    let f = Fixture::new();
    add_entry(&f.root, "everyone deny delete");
    assert!(establish(&f.data).is_ok());
}

#[test]
fn a_path_that_no_longer_leads_to_the_folder_made_is_not_handed_out() {
    // At the helper: the full path is compared once, before it is handed out; a parent replaced
    // during allocation (the reading's case) cannot be made without a race through allocate.
    let f = Fixture::new();
    let w = f.working();
    let subtree = w.open_subtree(Kind::CodexTmp).unwrap();
    let path = w.subtree(Kind::CodexTmp).join("tmp-invented");
    std::fs::DirBuilder::new().mode(0o700).create(&path).unwrap();
    let folder = open_dir_at(&subtree, OsStr::new("tmp-invented")).unwrap();
    assert!(WorkingFiles::path_leads_to(&path, &folder).is_ok(), "permitted");
    let elsewhere = f.root.join("invented-elsewhere");
    std::fs::create_dir_all(elsewhere.join("tmp-invented")).unwrap();
    std::fs::rename(w.subtree(Kind::CodexTmp), f.root.join("parked-subtree")).unwrap();
    std::os::unix::fs::symlink(&elsewhere, w.subtree(Kind::CodexTmp)).unwrap();
    assert_eq!(WorkingFiles::path_leads_to(&path, &folder).unwrap_err(), "its path now leads somewhere else");
}

#[test]
fn only_folders_are_counted() {
    let f = Fixture::new();
    let w = f.working();
    let _ = w.allocate(Kind::ProbeHome).unwrap();
    std::fs::write(w.subtree(Kind::ProbeHome).join("invented-file"), b"x").unwrap();
    std::os::unix::fs::symlink(&f.data, w.subtree(Kind::ProbeHome).join("invented-link")).unwrap();
    assert_eq!(kept_count(&f.data), Some(1));
}
