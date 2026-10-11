use super::{
    role_default, seed_instructions, seed_instructions_with, seed_instructions_with_admission,
    COMMON_DEFAULT,
};
use std::{fs, path::PathBuf};

struct Fixture(PathBuf);
impl Fixture {
    fn new() -> Self {
        let mut id = [0; 16];
        getrandom::fill(&mut id).unwrap();
        let path =
            std::env::temp_dir().join(format!("instruction-seed-{}", crate::util::sha256_hex(&id)));
        fs::create_dir(&path).unwrap();
        Self(path)
    }
}
impl Drop for Fixture {
    fn drop(&mut self) {
        let _ = fs::remove_dir_all(&self.0);
    }
}

#[test]
fn replaced_root_cannot_redirect_initial_guidance_writes() {
    let f = Fixture::new();
    let root = f.0.join("instructions");
    let outside = f.0.join("unrelated");
    fs::create_dir(&outside).unwrap();
    fs::create_dir(outside.join("agents")).unwrap();
    let result = seed_instructions_with(&root, || {
        fs::rename(&root, f.0.join("original-instructions")).unwrap();
        std::os::unix::fs::symlink(&outside, &root).unwrap();
    });
    assert!(
        !outside.join("AGENTS.md").exists(),
        "initial seed wrote through the replaced instruction root"
    );
    assert!(
        fs::read_dir(outside.join("agents"))
            .unwrap()
            .next()
            .is_none(),
        "role copies escaped their opened store"
    );
    assert!(
        result.is_err(),
        "replaced instruction root was reported successfully seeded"
    );
}

#[test]
fn first_seed_creates_nested_parent_and_exact_defaults() {
    let f = Fixture::new();
    let root = f.0.join("new-parent/deeper/instructions");
    seed_instructions(&root).unwrap();
    assert_eq!(fs::read(root.join("AGENTS.md")).unwrap(), COMMON_DEFAULT);
    for role in crate::role_supply::Role::ALL {
        assert_eq!(
            fs::read(root.join(format!("agents/AGENT_{}.md", role.name()))).unwrap(),
            role_default(role)
        );
    }
    fs::write(root.join("AGENTS.md"), b"person's edited common guidance").unwrap();
    seed_instructions(&root).unwrap();
    assert_eq!(
        fs::read(root.join("AGENTS.md")).unwrap(),
        b"person's edited common guidance"
    );
}

#[test]
fn known_missing_copy_is_not_repaired() {
    let f = Fixture::new();
    let root = f.0.join("instructions");
    seed_instructions(&root).unwrap();
    fs::remove_file(root.join("agents/AGENT_TASK.md")).unwrap();
    assert!(seed_instructions(&root).is_err());
    assert!(!root.join("agents/AGENT_TASK.md").exists());
}

#[test]
fn replaced_role_folder_cannot_redirect_role_copies() {
    let f = Fixture::new();
    let root = f.0.join("instructions");
    let outside = f.0.join("unrelated");
    fs::create_dir(&outside).unwrap();
    let result = seed_instructions_with(&root, || {
        fs::rename(root.join("agents"), f.0.join("original-agents")).unwrap();
        std::os::unix::fs::symlink(&outside, root.join("agents")).unwrap();
    });
    assert!(result.is_err());
    assert!(fs::read_dir(&outside).unwrap().next().is_none());
    assert!(!root.join("AGENTS.md").exists());
}

#[test]
fn replaced_parent_cannot_redirect_the_initial_store() {
    let f = Fixture::new();
    let data = f.0.join("data");
    fs::create_dir(&data).unwrap();
    let root = data.join("instructions");
    let outside = f.0.join("unrelated");
    fs::create_dir(&outside).unwrap();
    fs::create_dir(outside.join("instructions")).unwrap();
    fs::create_dir(outside.join("instructions/agents")).unwrap();
    let result = seed_instructions_with(&root, || {
        fs::rename(&data, f.0.join("original-data")).unwrap();
        std::os::unix::fs::symlink(&outside, &data).unwrap();
    });
    assert!(result.is_err());
    assert!(!outside.join("instructions/AGENTS.md").exists());
    assert!(fs::read_dir(outside.join("instructions/agents"))
        .unwrap()
        .next()
        .is_none());
}

#[test]
fn racing_regular_user_copy_is_kept_and_checked() {
    let f = Fixture::new();
    let root = f.0.join("instructions");
    seed_instructions_with(&root, || {
        fs::write(root.join("AGENTS.md"), b"person's racing edit").unwrap();
    })
    .unwrap();
    assert_eq!(
        fs::read(root.join("AGENTS.md")).unwrap(),
        b"person's racing edit"
    );
}

#[test]
fn racing_leaf_link_is_never_followed_or_reported_usable() {
    let f = Fixture::new();
    let root = f.0.join("instructions");
    let outside = f.0.join("unrelated.md");
    fs::write(&outside, b"unrelated original bytes").unwrap();
    let result = seed_instructions_with(&root, || {
        std::os::unix::fs::symlink(&outside, root.join("AGENTS.md")).unwrap();
    });
    assert!(result.is_err());
    assert_eq!(fs::read(&outside).unwrap(), b"unrelated original bytes");
}

#[test]
fn a_store_appearing_after_absence_admission_is_not_repaired() {
    let f = Fixture::new();
    let root = f.0.join("instructions");
    let result = seed_instructions_with_admission(
        &root,
        || {
            fs::create_dir(&root).unwrap();
            fs::write(root.join("AGENTS.md"), b"person's partial store").unwrap();
        },
        || panic!("an existing store entered first-copy publication"),
    );
    assert!(result.is_err());
    assert_eq!(
        fs::read(root.join("AGENTS.md")).unwrap(),
        b"person's partial store"
    );
    assert!(!root.join("agents").exists());
}

#[test]
fn failed_first_copy_leaves_partial_store_and_later_calls_do_not_repair_it() {
    let f = Fixture::new();
    let root = f.0.join("instructions");
    let blocked = root.join("agents/AGENT_TASK.md");
    let result = seed_instructions_with(&root, || {
        fs::create_dir(&blocked).unwrap();
    });
    assert!(result.is_err());
    assert_eq!(fs::read(root.join("AGENTS.md")).unwrap(), COMMON_DEFAULT);
    assert!(blocked.is_dir());
    // The first attempt can leave copies behind. Removing another copy makes
    // any accidental later reseeding visible without relying on timestamps.
    let missing = root.join("agents/AGENT_HELP_HUMAN.md");
    fs::remove_file(&missing).unwrap();
    fs::write(root.join("AGENTS.md"), b"person's partial-store edit").unwrap();
    assert!(seed_instructions(&root).is_err());
    assert!(!missing.exists());
    assert!(blocked.is_dir());
    assert_eq!(
        fs::read(root.join("AGENTS.md")).unwrap(),
        b"person's partial-store edit"
    );
}
