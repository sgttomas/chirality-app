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

#[test]
fn a_leftover_from_a_launch_that_ended_badly_is_removed() {
    let f = Fixture::new();
    for kind in Kind::ALL {
        let made = f.working().allocate(kind).unwrap();
        std::fs::write(made.path.join("invented"), b"x").unwrap();
        // A later launch, after one that ended without cleaning up.
        let cleaning = f.working().clean(&[]);
        assert_eq!(cleaning.removed, vec![made.path.clone()], "{kind:?}: {cleaning:?}");
        assert!(!made.path.exists());
        assert!(f.working().read_record(kind).unwrap().is_empty());
    }
}

#[test]
fn a_planted_folder_of_a_name_the_app_gives_is_kept_and_reported() {
    let f = Fixture::new();
    let w = f.working();
    let planted = w.root().join("probe-homes").join("probe-invented-planted");
    std::fs::create_dir(&planted).unwrap();
    let cleaning = w.clean(&[]);
    assert!(cleaning.removed.is_empty(), "{cleaning:?}");
    assert!(planted.exists());
    assert!(cleaning.kept.iter().any(|(p, why)| *p == planted && why.contains("did not record")), "{cleaning:?}");
}

#[test]
fn a_link_in_a_recorded_folders_place_is_kept_and_its_target_untouched() {
    let f = Fixture::new();
    let w = f.working();
    let made = w.allocate(Kind::Connector).unwrap();
    let target = f.root.join("not-the-apps");
    std::fs::create_dir(&target).unwrap();
    std::fs::write(target.join("precious"), b"x").unwrap();
    std::fs::remove_dir(&made.path).unwrap();
    std::os::unix::fs::symlink(&target, &made.path).unwrap();
    let cleaning = w.clean(&[]);
    assert!(cleaning.removed.is_empty(), "{cleaning:?}");
    assert!(target.join("precious").exists() && std::fs::symlink_metadata(&made.path).unwrap().file_type().is_symlink());
    assert!(cleaning.kept.iter().any(|(p, why)| *p == made.path && why.contains("not a folder")), "{cleaning:?}");
}

#[test]
fn a_recorded_folder_replaced_by_another_of_the_same_name_is_kept() {
    let f = Fixture::new();
    let w = f.working();
    let made = w.allocate(Kind::ProbeHome).unwrap();
    std::fs::remove_dir(&made.path).unwrap();
    // A different folder with the same name; its identity is not the recorded one.
    std::fs::create_dir(&made.path).unwrap();
    std::fs::set_permissions(&made.path, std::fs::Permissions::from_mode(0o700)).unwrap();
    std::fs::write(made.path.join("someone-elses"), b"x").unwrap();
    let cleaning = w.clean(&[]);
    assert!(cleaning.removed.is_empty(), "{cleaning:?}");
    assert!(made.path.join("someone-elses").exists());
    assert!(cleaning.kept.iter().any(|(p, why)| *p == made.path && why.contains("different folder")), "{cleaning:?}");
    assert!(w.remove(&made, &[]).removed.is_empty(), "removing the one made also refuses");
}

#[test]
fn an_unreadable_record_removes_nothing_and_says_so() {
    for bytes in [&b"{not json"[..], &b"{\"made\":[{\"name\":\"tmp-x\"}]}"[..]] {
        let f = Fixture::new();
        let w = f.working();
        let made = w.allocate(Kind::CodexTmp).unwrap();
        std::fs::write(w.root().join("codex-tmp").join(RECORD), bytes).unwrap();
        let cleaning = w.clean(&[]);
        assert!(cleaning.removed.is_empty(), "{cleaning:?}");
        assert!(made.path.exists());
        assert!(cleaning.kept.iter().any(|(_, why)| why.contains("nothing in it was removed")), "{cleaning:?}");
        assert!(w.allocate(Kind::CodexTmp).is_err(), "nothing new is made on a record that cannot be read");
    }
}

#[test]
fn a_folder_holding_a_sign_in_file_is_kept_unread() {
    for nested in [false, true] {
        let f = Fixture::new();
        let w = f.working();
        let made = w.allocate(Kind::ProbeHome).unwrap();
        let at = if nested { made.path.join("deeper") } else { made.path.clone() };
        std::fs::create_dir_all(&at).unwrap();
        std::fs::write(at.join("auth.json"), b"invented, never a real credential").unwrap();
        // Unreadable to show it is looked for by name, never opened.
        std::fs::set_permissions(at.join("auth.json"), std::fs::Permissions::from_mode(0o000)).unwrap();
        let cleaning = w.clean(&[]);
        assert!(cleaning.removed.is_empty(), "{cleaning:?}");
        assert!(cleaning.kept.iter().any(|(p, why)| *p == made.path && why.contains("sign-in")), "{cleaning:?}");
        std::fs::set_permissions(at.join("auth.json"), std::fs::Permissions::from_mode(0o600)).unwrap();
    }
}

#[test]
fn a_folder_that_is_or_contains_a_protected_folder_is_kept() {
    let f = Fixture::new();
    let w = f.working();
    let made = w.allocate(Kind::CodexTmp).unwrap();
    let inside = made.path.join("a-project-moved-in");
    std::fs::create_dir(&inside).unwrap();
    for protected in [made.path.clone(), inside.clone()] {
        let cleaning = w.clean(&[protected.clone()]);
        assert!(cleaning.removed.is_empty(), "{cleaning:?}");
        assert!(cleaning.kept.iter().any(|(_, why)| why.contains("is, or contains")), "{cleaning:?}");
    }
    assert_eq!(w.clean(&[f.data.clone()]).removed, vec![made.path.clone()], "an unrelated protected folder keeps nothing");
}

#[test]
fn a_link_inside_a_removed_folder_is_removed_and_not_followed() {
    let f = Fixture::new();
    let w = f.working();
    let made = w.allocate(Kind::CodexTmp).unwrap();
    let outside = f.root.join("outside");
    std::fs::create_dir(&outside).unwrap();
    std::fs::write(outside.join("kept"), b"x").unwrap();
    std::os::unix::fs::symlink(&outside, made.path.join("link")).unwrap();
    assert_eq!(w.remove(&made, &[]).removed, vec![made.path.clone()]);
    assert!(outside.join("kept").exists(), "what the link pointed to is untouched");
}
