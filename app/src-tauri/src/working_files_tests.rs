//! The Working Files folder on invented folders: where it is, what it refuses,
//! and above all that the cleaning removes nothing the App did not make.
use super::*;

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

#[test]
fn a_folder_made_is_exclusive_private_and_recorded_before_use() {
    let f = Fixture::new();
    let w = f.working();
    let made = w.allocate(Kind::CodexTmp).unwrap();
    let meta = std::fs::symlink_metadata(&made.path).unwrap();
    assert!(meta.is_dir() && meta.mode() & 0o777 == 0o700);
    assert!(made.path.starts_with(w.root().join("codex-tmp")));
    assert_eq!(w.read_record(Kind::CodexTmp).unwrap(), vec![(made.name.clone(), Stamp::of(&meta))]);
    let other = w.allocate(Kind::CodexTmp).unwrap();
    assert_ne!(made.path, other.path);
}

// Disposal: only a verified allocation of this launch authorises the removal
// of its contents, through the descriptor held since it was made; the folder
// itself is kept. The first reading of PR 340 found the cases marked "found".

#[test]
fn what_codex_leaves_in_a_folder_this_launch_made_is_removed_and_the_folder_kept() {
    let f = Fixture::new();
    let w = f.working();
    for kind in Kind::ALL {
        let made = w.allocate(kind).unwrap();
        std::fs::create_dir_all(made.path.join("deeper/still")).unwrap();
        std::fs::write(made.path.join("deeper/still/invented"), b"x").unwrap();
        std::os::unix::fs::symlink("/private/tmp", made.path.join("a-link")).unwrap();
        let cleaning = w.empty(&made);
        assert_eq!(cleaning.removed, vec![made.path.clone()], "{kind:?}: {cleaning:?}");
        assert!(made.path.is_dir() && std::fs::read_dir(&made.path).unwrap().count() == 0, "{kind:?}: emptied, kept");
        assert!(w.empty(&made).removed.is_empty(), "emptied once; no longer held");
    }
}

#[test]
fn nothing_is_removed_from_a_folder_this_launch_did_not_make() {
    // A folder an earlier launch left, and a folder planted with a name the App gives.
    let f = Fixture::new();
    let earlier = f.working().allocate(Kind::CodexTmp).unwrap();
    std::fs::write(earlier.path.join("invented"), b"x").unwrap();
    let w = f.working();
    let planted = w.subtree(Kind::ProbeHome).join("probe-invented-planted");
    std::fs::create_dir(&planted).unwrap();
    std::fs::write(planted.join("invented"), b"x").unwrap();
    let cleaning = w.empty_all();
    assert!(cleaning.removed.is_empty() && cleaning.kept.is_empty(), "{cleaning:?}");
    assert!(earlier.path.join("invented").exists() && planted.join("invented").exists());
    let kept = w.kept_folders();
    assert!(kept.contains(&earlier.path) && kept.contains(&planted), "reported at the start: {kept:?}");
    // The earlier launch's own value would empty it; a later one never does.
    assert!(w.empty(&earlier).kept.iter().any(|(_, why)| why.contains("does not hold it")));
}

#[test]
fn a_made_folder_moved_away_and_replaced_is_emptied_where_it_is_and_the_replacement_untouched() {
    let f = Fixture::new();
    let w = f.working();
    let made = w.allocate(Kind::CodexTmp).unwrap();
    std::fs::write(made.path.join("codexs"), b"x").unwrap();
    // found: the name given to someone else's folder after the check.
    let parked = f.root.join("parked-made");
    std::fs::rename(&made.path, &parked).unwrap();
    std::fs::create_dir(&made.path).unwrap();
    std::fs::write(made.path.join("precious"), b"x").unwrap();
    w.empty(&made);
    assert!(made.path.join("precious").exists(), "the name is never looked up again");
    assert!(!parked.join("codexs").exists(), "the folder made is the one emptied");
}

#[test]
fn a_protected_folder_inside_is_kept_whatever_contains_it() {
    // found: App data, or the person's .codex, moved in with a link left in its place.
    for codex_home in [false, true] {
        let f = Fixture::new();
        let protected = if codex_home { f.root.join("invented-home").join(".codex") } else { f.data.clone() };
        std::fs::create_dir_all(&protected).unwrap();
        std::fs::write(protected.join("invented-work"), b"x").unwrap();
        let w = f.working().protecting(&[protected.clone()]);
        let made = w.allocate(Kind::ProbeHome).unwrap();
        let relocated = made.path.join("deeper").join("relocated");
        std::fs::create_dir(made.path.join("deeper")).unwrap();
        std::fs::rename(&protected, &relocated).unwrap();
        std::os::unix::fs::symlink(&relocated, &protected).unwrap();
        let cleaning = w.empty(&made);
        assert!(protected.join("invented-work").exists(), "codex_home={codex_home}: {cleaning:?}");
        assert!(cleaning.kept.iter().any(|(_, why)| why.contains("protects")), "{cleaning:?}");
    }
    // found: the connector's folder protects the App data folder too, with no caller naming it.
    let f = Fixture::new();
    let w = f.working();
    let made = w.allocate(Kind::Connector).unwrap();
    std::fs::write(f.data.join("invented-work"), b"x").unwrap();
    std::fs::rename(&f.data, made.path.join("relocated-app-data")).unwrap();
    w.empty(&made);
    assert!(made.path.join("relocated-app-data/invented-work").exists());
}

#[test]
fn a_folder_holding_a_name_codex_gives_a_file_in_its_home_is_kept_unread() {
    for (name, nested) in [("auth.json", false), ("auth.json", true), ("config.toml", false), ("history.jsonl", true)] {
        let f = Fixture::new();
        let w = f.working();
        let made = w.allocate(Kind::ProbeHome).unwrap();
        let at = if nested { made.path.join("deeper") } else { made.path.clone() };
        std::fs::create_dir_all(&at).unwrap();
        std::fs::write(at.join(name), b"invented, never a real credential").unwrap();
        // Unreadable, to show it is looked for by name and never opened.
        std::fs::set_permissions(at.join(name), std::fs::Permissions::from_mode(0o000)).unwrap();
        let cleaning = w.empty(&made);
        assert!(at.join(name).exists(), "{name}: {cleaning:?}");
        assert!(cleaning.kept.iter().any(|(p, why)| *p == made.path && why.contains(&format!("named {name}"))), "{cleaning:?}");
        std::fs::set_permissions(at.join(name), std::fs::Permissions::from_mode(0o600)).unwrap();
    }
}

#[test]
fn a_folder_or_single_named_file_made_before_the_allocation_is_kept_as_moved_in() {
    // found: a Codex home with no sign-in file, moved in, was removed.
    for folder in [true, false] {
        let f = Fixture::new();
        let elsewhere = f.root.join("invented-elsewhere");
        if folder {
            std::fs::create_dir(&elsewhere).unwrap();
            std::fs::write(elsewhere.join("invented"), b"x").unwrap();
        } else {
            std::fs::write(&elsewhere, b"invented").unwrap();
        }
        std::thread::sleep(std::time::Duration::from_millis(20));
        let w = f.working();
        let made = w.allocate(Kind::Connector).unwrap();
        std::fs::rename(&elsewhere, made.path.join("moved")).unwrap();
        let cleaning = w.empty(&made);
        assert!(made.path.join("moved").exists(), "folder={folder}: {cleaning:?}");
        assert!(cleaning.kept.iter().any(|(_, why)| why.contains("moved in from elsewhere")), "{cleaning:?}");
    }
}

#[test]
fn a_hard_link_inside_loses_only_its_name_there() {
    let f = Fixture::new();
    let w = f.working();
    let source = f.root.join("invented-project-file");
    std::fs::write(&source, b"invented").unwrap();
    let made = w.allocate(Kind::CodexTmp).unwrap();
    std::fs::hard_link(&source, made.path.join("linked")).unwrap();
    assert_eq!(w.empty(&made).removed, vec![made.path.clone()]);
    assert_eq!(std::fs::read(&source).unwrap(), b"invented");
}

#[test]
fn a_link_inside_is_removed_and_not_followed() {
    let f = Fixture::new();
    let w = f.working();
    let outside = f.root.join("outside");
    std::fs::create_dir(&outside).unwrap();
    std::fs::write(outside.join("kept"), b"x").unwrap();
    let made = w.allocate(Kind::CodexTmp).unwrap();
    std::os::unix::fs::symlink(&outside, made.path.join("link")).unwrap();
    assert_eq!(w.empty(&made).removed, vec![made.path.clone()]);
    assert!(outside.join("kept").exists(), "what the link pointed to is untouched");
}

#[test]
fn the_record_is_read_only_as_a_regular_file_with_one_name_and_never_through_a_link() {
    // found: the record replaced by a link to a probe home's sign-in file was opened.
    for hard in [false, true] {
        let f = Fixture::new();
        let w = f.working();
        let made = w.allocate(Kind::ProbeHome).unwrap();
        let sign_in = made.path.join("auth.json");
        std::fs::write(&sign_in, b"{\"made\":[]}").unwrap();
        let record = w.subtree(Kind::ProbeHome).join(RECORD);
        std::fs::remove_file(&record).unwrap();
        if hard {
            std::fs::hard_link(&sign_in, &record).unwrap();
        } else {
            std::fs::set_permissions(&sign_in, std::fs::Permissions::from_mode(0o000)).unwrap();
            std::os::unix::fs::symlink(&sign_in, &record).unwrap();
        }
        let refused = w.allocate(Kind::ProbeHome).unwrap_err();
        assert!(refused.contains("nothing was made"), "hard={hard}: {refused}");
        assert!(w.read_record(Kind::ProbeHome).is_err(), "hard={hard}");
        std::fs::set_permissions(&sign_in, std::fs::Permissions::from_mode(0o600)).unwrap();
    }
}

#[test]
fn a_working_files_folder_replaced_by_a_link_after_it_was_established_is_refused() {
    // found: a new folder was made through the link, in App data.
    let f = Fixture::new();
    let w = f.working();
    std::fs::rename(w.root(), f.root.join("parked")).unwrap();
    std::os::unix::fs::symlink(&f.data, w.root()).unwrap();
    std::fs::DirBuilder::new().mode(0o700).create(f.data.join("probe-homes")).unwrap();
    let refused = w.allocate(Kind::ProbeHome).unwrap_err();
    assert!(refused.contains("could not be opened as a folder") || refused.contains("no longer the folder"), "{refused}");
    assert_eq!(std::fs::read_dir(f.data.join("probe-homes")).unwrap().count(), 0, "nothing made in App data");
}

#[test]
fn a_forged_record_authorises_nothing() {
    // found: a record edited to carry another folder's stamp had that folder removed. No record
    // authorises a removal now; what it names, inside the subtree or outside it, is untouched.
    let f = Fixture::new();
    let w = f.working();
    let outside = f.root.join("outside");
    let inside = w.subtree(Kind::ProbeHome).join("probe-not-made-by-app");
    for at in [&outside, &inside] {
        std::fs::create_dir(at).unwrap();
        std::fs::write(at.join("precious"), b"x").unwrap();
    }
    let forged: Vec<(String, Stamp)> = [("../../outside", &outside), ("probe-not-made-by-app", &inside)]
        .iter().map(|(name, at)| (name.to_string(), Stamp::of(&std::fs::metadata(at).unwrap()))).collect();
    w.write_record(Kind::ProbeHome, &forged).unwrap();
    let later = f.working();
    let cleaning = later.empty_all();
    assert!(cleaning.removed.is_empty(), "{cleaning:?}");
    assert!(outside.join("precious").exists() && inside.join("precious").exists());
}

#[test]
fn no_record_or_subtree_is_inside_a_folder_the_app_hands_out() {
    // Every record, its subtree and the Working Files folder lie outside every made folder,
    // the one given to Codex as its TMPDIR and the probe's home included.
    let f = Fixture::new();
    let w = f.working();
    for kind in Kind::ALL {
        let made = w.allocate(kind).unwrap();
        assert_eq!(made.path.parent(), Some(w.subtree(kind).as_path()), "{kind:?}");
        for other in Kind::ALL {
            for control in [w.subtree(other).join(RECORD), w.subtree(other), w.root().to_path_buf()] {
                assert!(!control.starts_with(&made.path), "{kind:?} holds {}", control.display());
            }
        }
    }
}

#[test]
fn a_layout_imitated_inside_codexs_temporary_folder_is_removed_as_files_and_read_as_nothing() {
    let f = Fixture::new();
    let w = f.working();
    let made = w.allocate(Kind::CodexTmp).unwrap();
    let outside = f.root.join("outside");
    std::fs::create_dir(&outside).unwrap();
    std::fs::write(outside.join("precious"), b"x").unwrap();
    let sibling = w.subtree(Kind::CodexTmp).join("tmp-not-made");
    std::fs::create_dir(&sibling).unwrap();
    let forged = serde_json::json!({"made": [
        Stamp::of(&std::fs::metadata(&outside).unwrap()).to_json("../../../outside"),
        Stamp::of(&std::fs::metadata(&sibling).unwrap()).to_json("tmp-not-made"),
    ]});
    for at in [made.path.clone(), made.path.join("codex-tmp"), made.path.join("probe-homes")] {
        std::fs::create_dir_all(&at).unwrap();
        std::fs::write(at.join(RECORD), serde_json::to_vec(&forged).unwrap()).unwrap();
    }
    let cleaning = w.empty(&made);
    assert_eq!(cleaning.removed, vec![made.path.clone()], "{cleaning:?}");
    assert!(outside.join("precious").exists() && sibling.exists());
    assert_eq!(std::fs::read_dir(&made.path).unwrap().count(), 0);
}

#[test]
fn an_entry_made_after_the_allocation_and_moved_in_is_removed() {
    // Its creation time is later than the folder's, so it is taken as made there. Moving it in
    // took the right to remove it where it was (write on the folder it came from).
    let f = Fixture::new();
    let w = f.working();
    let made = w.allocate(Kind::CodexTmp).unwrap();
    std::thread::sleep(std::time::Duration::from_millis(20));
    let elsewhere = f.root.join("invented-newer");
    std::fs::create_dir(&elsewhere).unwrap();
    std::fs::write(elsewhere.join("invented"), b"x").unwrap();
    std::fs::rename(&elsewhere, made.path.join("moved")).unwrap();
    assert_eq!(w.empty(&made).removed, vec![made.path.clone()]);
    assert!(!made.path.join("moved").exists());
}
