use super::{read_guidance, read_guidance_snapshot, Guidance, Role, content};
use serde_json::{json, Value};
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

fn history(default: &[u8]) -> Value {
    let paths = std::iter::once("AGENTS.md".to_owned())
        .chain(Role::ALL.iter().map(|r| format!("agents/AGENT_{}.md", r.name())));
    json!({"format":"chirality.instruction-seed-record/1","release":"declared-old-release",
        "created":paths.map(|path|json!({"path":path,"defaultContent":content(default)})).collect::<Vec<_>>(),
        "preserved":[]})
}
fn put_history(f: &Fixture, record: &Value) -> Vec<u8> {
    let raw = serde_json::to_vec(record).unwrap(); fs::write(f.root().join(".seed-record.json"), &raw).unwrap(); raw
}

#[test]
fn declared_history_and_reviewed_default_are_separate_inspectable_facts() {
    let f = Fixture::new(); let raw = put_history(&f, &history(b"older default"));
    let guidance = Guidance::read_seeded(&f.root(), "AGENTS.md", "reviewed-current-release", BYTES).unwrap();
    assert_eq!(guidance.bytes(), BYTES); assert!(!guidance.modified());
    assert_eq!(guidance.source["store"], "editable-copy");
    assert_eq!(guidance.source["reviewedDefault"]["release"], "reviewed-current-release");
    assert_eq!(guidance.source["reviewedDefault"]["content"], content(BYTES));
    let h = &guidance.source["seedHistory"];
    assert_eq!(h["status"], "declared"); assert_eq!(h["record"]["content"], content(&raw));
    assert_eq!(h["release"], "declared-old-release");
    assert_eq!(h["matchesSuppliedContent"], false);
    let composed = super::Composition::new(&guidance, None, false).unwrap();
    let record = composed.start_record("sup:history-test", "thread", "request", 1, None).unwrap();
    let schema: Value = serde_json::from_str(include_str!("../resources/workflow_role/role-supply-record.schema.json")).unwrap();
    jsonschema::options().offline().build(&schema).unwrap().validate(&record).unwrap();
    assert_eq!(record["adoption"], "unknown");
}

#[test]
fn forged_seed_baseline_cannot_make_modified_guidance_a_reviewed_default() {
    let f = Fixture::new(); put_history(&f, &history(BYTES));
    let guidance = Guidance::read_seeded(&f.root(), "agents/AGENT_TASK.md", "reviewed", b"reviewed task default").unwrap();
    assert_eq!(guidance.source["seedHistory"]["matchesSuppliedContent"], true);
    assert!(guidance.modified());
    assert_eq!(super::limit(Role::TASK, &guidance)["standing"], "unknown");
}

#[test]
fn absent_and_preserved_history_do_not_invent_seed_origin_or_replace_bytes() {
    let f = Fixture::new();
    let before = fs::read(f.root().join("AGENTS.md")).unwrap();
    let missing = Guidance::read_seeded(&f.root(), "AGENTS.md", "reviewed", BYTES).unwrap();
    assert_eq!(missing.source["seedHistory"], json!({"status":"unestablished","reason":"missing"}));
    let mut record = history(BYTES);
    record["created"].as_array_mut().unwrap().remove(0);
    record["preserved"] = json!([{"path":"AGENTS.md","origin":"unknown"}]); put_history(&f, &record);
    let preserved = Guidance::read_seeded(&f.root(), "AGENTS.md", "reviewed", BYTES).unwrap();
    assert_eq!(preserved.source["seedHistory"], json!({"status":"unestablished","reason":"preserved-path"}));
    assert_eq!(preserved.bytes(), BYTES); assert!(!preserved.modified());
    assert_eq!(fs::read(f.root().join("AGENTS.md")).unwrap(), before);
}

#[test]
fn malformed_duplicate_or_incomplete_history_stays_unknown() {
    let f = Fixture::new(); let good = history(BYTES);
    let mut bad = Vec::new();
    bad.push(b"not JSON".to_vec());
    let raw = serde_json::to_string(&good).unwrap();
    bad.push(raw.replacen("\"release\":", "\"release\":\"duplicate\",\"release\":", 1).into_bytes());
    bad.push(raw.replacen("\"path\":", "\"path\":\"duplicate\",\"path\":", 1).into_bytes());
    for change in 0..7 {
        let mut record = good.clone();
        match change {
            0 => { record["format"] = json!("unsupported"); }
            1 => { record["release"] = json!(""); }
            2 => { record["created"].as_array_mut().unwrap().pop(); }
            3 => { record["created"][1]["path"] = json!("AGENTS.md"); }
            4 => { record["created"][0]["defaultContent"]["method"] = json!("unsupported"); }
            5 => { record["created"][0]["defaultContent"]["value"] = json!("invalid digest"); }
            _ => { record["unexpected"] = json!(true); }
        }
        bad.push(serde_json::to_vec(&record).unwrap());
    }
    for raw in bad {
        fs::write(f.root().join(".seed-record.json"), raw).unwrap();
        let g = Guidance::read_seeded(&f.root(), "AGENTS.md", "reviewed", BYTES).unwrap();
        assert_eq!(g.source["seedHistory"], json!({"status":"unestablished","reason":"invalid"}));
        assert_eq!(g.bytes(), BYTES);
    }
}

#[test]
fn linked_special_oversized_or_changed_history_never_redirects_guidance() {
    let f = Fixture::new(); let record_path = f.root().join(".seed-record.json");
    symlink(f.root().join("AGENTS.md"), &record_path).unwrap();
    let g = Guidance::read_seeded(&f.root(), "AGENTS.md", "reviewed", BYTES).unwrap();
    assert_eq!(g.source["seedHistory"]["reason"], "unreadable"); fs::remove_file(&record_path).unwrap();
    fs::create_dir(&record_path).unwrap();
    assert_eq!(Guidance::read_seeded(&f.root(), "AGENTS.md", "reviewed", BYTES).unwrap().source["seedHistory"]["reason"], "unreadable");
    fs::remove_dir(&record_path).unwrap();
    let fifo = std::ffi::CString::new(record_path.as_os_str().as_encoded_bytes()).unwrap();
    assert_eq!(unsafe { libc::mkfifo(fifo.as_ptr(), 0o600) }, 0);
    let root = f.root(); let (tx, rx) = std::sync::mpsc::channel();
    std::thread::spawn(move || { let _ = tx.send(Guidance::read_seeded(&root, "AGENTS.md", "reviewed", BYTES)); });
    let fifo_result = rx.recv_timeout(std::time::Duration::from_secs(1)).expect("history FIFO blocked the guidance read").unwrap();
    assert_eq!(fifo_result.source["seedHistory"]["reason"], "unreadable");
    fs::remove_file(&record_path).unwrap();
    fs::write(&record_path, vec![b'x'; super::seed_history::MAX_BYTES as usize + 1]).unwrap();
    assert_eq!(Guidance::read_seeded(&f.root(), "AGENTS.md", "reviewed", BYTES).unwrap().source["seedHistory"]["reason"], "unreadable");
    put_history(&f, &history(BYTES));
    let (bytes, h) = read_guidance_snapshot(&f.root(), "AGENTS.md", || {
        fs::rename(&record_path, f.root().join("replaced-record")).unwrap();
        put_history(&f, &history(BYTES));
    }).unwrap();
    assert_eq!(bytes, BYTES); assert_eq!(h, json!({"status":"unestablished","reason":"changed"}));
    let (bytes, h) = read_guidance_snapshot(&f.root(), "AGENTS.md", || {
        fs::write(&record_path, b"changed").unwrap();
    }).unwrap();
    assert_eq!(bytes, BYTES); assert_eq!(h["reason"], "changed");
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
