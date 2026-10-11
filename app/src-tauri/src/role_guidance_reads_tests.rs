use super::{read_guidance, Guidance};
use std::os::unix::fs::symlink;
use std::{fs, path::PathBuf};

const BYTES: &[u8] = "Common ü / role 字\r\n".as_bytes();

struct Fixture(PathBuf);
impl Fixture {
    fn new() -> Self {
        let mut id = [0; 16];
        getrandom::fill(&mut id).unwrap();
        let parent =
            std::env::temp_dir().join(format!("role-guidance-{}", crate::util::sha256_hex(&id)));
        fs::create_dir(&parent).unwrap();
        fs::create_dir(parent.join("store")).unwrap();
        fs::create_dir(parent.join("store/agents")).unwrap();
        fs::write(parent.join("store/AGENTS.md"), BYTES).unwrap();
        fs::write(parent.join("store/agents/AGENT_TASK.md"), BYTES).unwrap();
        Self(parent)
    }
    fn root(&self) -> PathBuf {
        self.0.join("store")
    }
}
impl Drop for Fixture {
    fn drop(&mut self) {
        let _ = fs::remove_dir_all(&self.0);
    }
}

#[test]
fn guidance_keeps_exact_regular_bytes_default_modified_and_hardlinks() {
    let f = Fixture::new();
    let common = Guidance::read_seeded(&f.root(), "AGENTS.md", "fixture", BYTES).unwrap();
    assert_eq!(common.bytes(), BYTES);
    assert!(!common.modified());
    fs::remove_file(f.root().join("agents/AGENT_TASK.md")).unwrap();
    fs::hard_link(
        f.root().join("AGENTS.md"),
        f.root().join("agents/AGENT_TASK.md"),
    )
    .unwrap();
    let role = Guidance::read_seeded(&f.root(), "agents/AGENT_TASK.md", "fixture", b"old default")
        .unwrap();
    assert_eq!(role.bytes(), BYTES);
    assert!(role.modified());
}

#[test]
fn relative_roots_and_existing_ancestor_aliases_keep_their_meaning() {
    let f = Fixture::new();
    let cwd = std::env::current_dir().unwrap();
    let mut relative = PathBuf::new();
    for component in cwd.components() {
        if matches!(component, std::path::Component::Normal(_)) {
            relative.push("..");
        }
    }
    for component in f.root().components() {
        if let std::path::Component::Normal(name) = component {
            relative.push(name);
        }
    }
    assert_eq!(
        Guidance::read_seeded(&relative, "AGENTS.md", "fixture", BYTES)
            .unwrap()
            .bytes(),
        BYTES
    );
    let alias = f.0.join("ancestor-alias");
    symlink(&f.0, &alias).unwrap();
    assert_eq!(
        Guidance::read_seeded(&alias.join("store"), "AGENTS.md", "fixture", BYTES)
            .unwrap()
            .bytes(),
        BYTES
    );
}

#[test]
fn static_root_role_directory_and_leaf_links_refuse() {
    let f = Fixture::new();
    let alias = f.0.join("root-alias");
    symlink(f.root(), &alias).unwrap();
    assert!(Guidance::read_seeded(&alias, "AGENTS.md", "fixture", BYTES).is_err());
    fs::rename(f.root().join("agents"), f.0.join("real-agents")).unwrap();
    symlink(f.0.join("real-agents"), f.root().join("agents")).unwrap();
    assert!(Guidance::read_seeded(&f.root(), "agents/AGENT_TASK.md", "fixture", BYTES).is_err());
    fs::remove_file(f.root().join("AGENTS.md")).unwrap();
    symlink(
        f.0.join("real-agents/AGENT_TASK.md"),
        f.root().join("AGENTS.md"),
    )
    .unwrap();
    assert!(Guidance::read_seeded(&f.root(), "AGENTS.md", "fixture", BYTES).is_err());
}

#[test]
fn directory_and_invalid_utf8_guidance_refuse() {
    let f = Fixture::new();
    fs::remove_file(f.root().join("AGENTS.md")).unwrap();
    fs::create_dir(f.root().join("AGENTS.md")).unwrap();
    assert!(Guidance::read_seeded(&f.root(), "AGENTS.md", "fixture", BYTES).is_err());
    fs::remove_dir(f.root().join("AGENTS.md")).unwrap();
    fs::write(f.root().join("AGENTS.md"), [0xff]).unwrap();
    assert!(Guidance::read_seeded(&f.root(), "AGENTS.md", "fixture", BYTES).is_err());
}

#[test]
fn opened_leaf_replacement_refuses_even_with_equal_bytes() {
    let f = Fixture::new();
    assert!(read_guidance(&f.root(), "AGENTS.md", || {
        fs::rename(f.root().join("AGENTS.md"), f.0.join("original.md")).unwrap();
        fs::write(f.root().join("AGENTS.md"), BYTES).unwrap();
    })
    .is_err());
}

#[test]
fn opened_leaf_replaced_by_link_refuses() {
    let f = Fixture::new();
    assert!(read_guidance(&f.root(), "AGENTS.md", || {
        fs::rename(f.root().join("AGENTS.md"), f.0.join("original.md")).unwrap();
        symlink(f.0.join("original.md"), f.root().join("AGENTS.md")).unwrap();
    })
    .is_err());
}

#[test]
fn opened_role_directory_replacement_refuses() {
    let f = Fixture::new();
    assert!(read_guidance(&f.root(), "agents/AGENT_TASK.md", || {
        fs::rename(f.root().join("agents"), f.0.join("original-agents")).unwrap();
        fs::create_dir(f.root().join("agents")).unwrap();
        fs::write(f.root().join("agents/AGENT_TASK.md"), BYTES).unwrap();
    })
    .is_err());
}

#[test]
fn opened_root_replacement_refuses() {
    let f = Fixture::new();
    assert!(read_guidance(&f.root(), "AGENTS.md", || {
        fs::rename(f.root(), f.0.join("original-store")).unwrap();
        fs::create_dir(f.root()).unwrap();
        fs::write(f.root().join("AGENTS.md"), BYTES).unwrap();
    })
    .is_err());
}

#[test]
fn growth_and_shrink_after_open_refuse_instead_of_accepting_partial_bytes() {
    use std::io::Write;
    let f = Fixture::new();
    assert!(read_guidance(&f.root(), "AGENTS.md", || {
        fs::OpenOptions::new()
            .append(true)
            .open(f.root().join("AGENTS.md"))
            .unwrap()
            .write_all(b"appended bytes")
            .unwrap();
    })
    .is_err());
    assert!(read_guidance(&f.root(), "AGENTS.md", || {
        fs::write(f.root().join("AGENTS.md"), b"short").unwrap();
    })
    .is_err());
    assert_eq!(
        Guidance::read_seeded(&f.root(), "AGENTS.md", "fixture", BYTES)
            .unwrap()
            .bytes(),
        b"short"
    );
}
