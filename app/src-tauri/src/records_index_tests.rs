//! The bounded index against the full reader: after every kind of change a
//! project's logs can see (appends by the writer, lines appended from outside,
//! a torn tail and its W-0 recovery, an unreadable line, a sequence gap, a
//! duplicate identity, a shrink, a replaced file, a removed log, a new run
//! directory, a symlink), the index reports exactly what `storage::read_all`
//! reports: the same identities, the same limits and the same partials.
use super::*;
use crate::records::{append, append_project, APP_WRITER};

fn scratch() -> PathBuf {
    let p = std::env::temp_dir().join(crate::util::opaque_id("records-index-").unwrap());
    std::fs::create_dir_all(&p).unwrap();
    std::fs::canonicalize(p).unwrap()
}
fn body(n: usize) -> Value {
    json!({"label":"unresolvable reference","subjectRef":format!("index {n}")})
}
/// The index and the full reader agree (identities as a multiset, limits and partials as sorted lists).
fn agree(root: &Path, step: &str) {
    let (entries, limits, partials) = crate::storage::read_all_parts(root);
    let mut ids: Vec<String> = entries.iter().filter_map(|e| e["recordId"].as_str().map(str::to_owned)).collect();
    ids.sort();
    let (mut ix_ids, mut ix_limits, mut ix_partials) = with_index(root, |ix| {
        let ids: Vec<String> = ix.ids.iter().flat_map(|(id, n)| std::iter::repeat_n(id.clone(), n.len())).collect();
        (ids, ix.limits(), ix.partials())
    });
    ix_ids.sort();
    let (mut limits, mut partials) = (limits, partials);
    limits.sort();
    ix_limits.sort();
    partials.sort();
    ix_partials.sort();
    assert_eq!(ix_ids, ids, "{step}: identities");
    if ix_limits != limits {
        let logs: Vec<String> = crate::storage::discover(root).unwrap_or_default().iter().map(|p| format!("{}: {:?}", p.display(), String::from_utf8_lossy(&std::fs::read(p).unwrap_or_default()).chars().map(|c| if c == '\n' { '|' } else { c }).filter(|c| !c.is_alphanumeric() || *c == '|').collect::<String>())).collect();
        panic!("{step}: limits\n index {ix_limits:?}\n full {limits:?}\n{}", logs.join("\n"));
    }
    assert_eq!(ix_partials, partials, "{step}: partials");
}
fn push(path: &Path, bytes: &[u8]) {
    use std::io::Write;
    std::fs::OpenOptions::new().append(true).create(true).open(path).unwrap().write_all(bytes).unwrap();
}

#[test]
fn the_index_reports_what_the_full_reader_reports_through_every_change() {
    let root = scratch();
    agree(&root, "empty project");
    let acts = crate::storage::project_log(&root, None, "index-writer");
    for n in 0..5 { append(&acts, "evidence_limit", &APP_WRITER, body(n)).unwrap(); }
    agree(&root, "writer appends");
    let run = |n: usize| append_project(&root, Some(&format!("run:index-{n}")), "app-writer:local", "evidence_limit", &APP_WRITER, body(n)).unwrap();
    for n in 0..3 { run(n); }
    agree(&root, "new run directories");
    // A line appended from outside the writer, copied from an existing entry: a duplicate identity and a sequence gap.
    let first = std::fs::read_to_string(&acts).unwrap().lines().next().unwrap().to_owned();
    push(&acts, format!("{first}\n").as_bytes());
    agree(&root, "external duplicate line");
    let restored = std::fs::read(&acts).unwrap();
    std::fs::write(&acts, &restored[..restored.len() - first.len() - 1]).unwrap();
    agree(&root, "duplicate removed (shrunk in place)");
    // A torn tail in another log, then its writer's W-0 recovery.
    let other = crate::storage::project_log(&root, None, "torn-writer");
    append(&other, "evidence_limit", &APP_WRITER, body(9)).unwrap();
    push(&other, b"{\"torn");
    agree(&root, "torn tail");
    append(&other, "evidence_limit", &APP_WRITER, body(10)).unwrap();
    agree(&root, "after W-0");
    // An unreadable line, then the file replaced by its readable prefix (another inode).
    push(&other, b"{\"unreadable\n");
    agree(&root, "unreadable line");
    let text = std::fs::read_to_string(&other).unwrap();
    let keep: String = text.lines().take(3).map(|l| format!("{l}\n")).collect();
    let replaced = other.with_extension("tmp");
    std::fs::write(&replaced, keep.as_bytes()).unwrap();
    std::fs::rename(&replaced, &other).unwrap();
    agree(&root, "replaced file");
    // A shrink in place (same inode).
    let shorter: String = keep.lines().take(1).map(|l| format!("{l}\n")).collect();
    std::fs::write(&other, shorter.as_bytes()).unwrap();
    agree(&root, "shrunk in place");
    // An edit of the last line in place, same size.
    let mut bytes = std::fs::read(&other).unwrap();
    let at = bytes.len() - 3;
    bytes[at] = b'#';
    std::thread::sleep(std::time::Duration::from_millis(5));
    std::fs::write(&other, &bytes).unwrap();
    agree(&root, "same-size edit of the last line");
    // A removed log, and a symlink where a log was.
    std::fs::remove_file(&other).unwrap();
    agree(&root, "removed log");
    std::os::unix::fs::symlink(&acts, &other).unwrap();
    agree(&root, "symlinked log");
    std::fs::remove_file(&other).unwrap();
    agree(&root, "symlink removed");
    // The legacy log.
    let legacy = root.join(crate::storage::LEGACY_LOG);
    std::fs::create_dir_all(legacy.parent().unwrap()).unwrap();
    append(&legacy, "evidence_limit", &APP_WRITER, body(20)).unwrap();
    agree(&root, "legacy log");
    std::fs::remove_dir_all(root).unwrap();
}

// Many random changes, each followed by a comparison with the full reader.
#[test]
fn random_changes_keep_the_index_equal_to_the_full_reader() {
    let root = scratch();
    let mut state = 0x9e3779b97f4a7c15u64 ^ std::process::id() as u64;
    let mut next = |n: u64| { state ^= state << 13; state ^= state >> 7; state ^= state << 17; state % n };
    let logs: Vec<PathBuf> = (0..4).map(|n| crate::storage::project_log(&root, if n % 2 == 0 { Some("run:random") } else { None }, &format!("w{n}"))).collect();
    for log in &logs { std::fs::create_dir_all(log.parent().unwrap()).unwrap(); }
    for step in 0..400 {
        let log = &logs[next(logs.len() as u64) as usize];
        match next(9) {
            0..=3 => { let _ = append(log, "evidence_limit", &APP_WRITER, body(step)); }
            4 => push(log, b"{\"torn"),
            5 => push(log, b"\n"),
            6 => {
                // A line copied from another log: a duplicate identity.
                let from = &logs[next(logs.len() as u64) as usize];
                if let Some(line) = std::fs::read_to_string(from).ok().and_then(|t| t.lines().find(|l| l.starts_with('{') && l.ends_with('}')).map(str::to_owned)) {
                    push(log, format!("{line}\n").as_bytes());
                }
            }
            7 => if log.exists() { std::fs::remove_file(log).unwrap(); },
            _ => if log.exists() {
                let bytes = std::fs::read(log).unwrap();
                let cut = next(bytes.len() as u64 + 1) as usize;
                std::fs::write(log, &bytes[..cut]).unwrap();
            },
        }
        agree(&root, &format!("random step {step}"));
    }
    std::fs::remove_dir_all(root).unwrap();
}

// The writer's guards answer from the index as they did from the full read:
// a readable identity anywhere is refused, an unreadable line elsewhere
// refuses an open run's append, and another writer's torn tail does not.
#[test]
fn the_writer_refuses_held_identities_and_incomplete_sets_from_the_index() {
    let root = scratch();
    let other = crate::storage::project_log(&root, None, "holder");
    let held = append(&other, "evidence_limit", &APP_WRITER, body(1)).unwrap()["recordId"].as_str().unwrap().to_owned();
    let own = |id: &str| crate::records::append_project_reserved(&root, "run:guard", "app-writer:local", "evidence_limit", &APP_WRITER, body(2), id, "2026-10-12T00:00:00.000Z");
    assert!(own(&held).is_err_and(|e| e.contains("record identity conflict")));
    push(&other, b"{\"torn");
    assert!(own("rec:app:index-guard-1").is_ok());
    push(&other, b"\n");
    assert!(own("rec:app:index-guard-2").is_err_and(|e| e.contains("record-set conflict/incomplete")));
    std::fs::remove_dir_all(root).unwrap();
}
