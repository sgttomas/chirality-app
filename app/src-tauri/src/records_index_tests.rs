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
        let mut ids = Vec::new();
        ix.db.as_ref().unwrap().lines("", None, |_, l| { ids.extend(l.id); Ok(()) }).unwrap();
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
    let acts = crate::storage::project_log(&root, None, "index-writer").unwrap();
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
    let other = crate::storage::project_log(&root, None, "torn-writer").unwrap();
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
    let logs: Vec<PathBuf> = (0..4).map(|n| crate::storage::project_log(&root, if n % 2 == 0 { Some("run:random") } else { None }, &format!("w{n}")).unwrap()).collect();
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
    let other = crate::storage::project_log(&root, None, "holder").unwrap();
    let held = append(&other, "evidence_limit", &APP_WRITER, body(1)).unwrap()["recordId"].as_str().unwrap().to_owned();
    let own = |id: &str| crate::records::append_project_reserved(&root, "run:guard", "app-writer:local", "evidence_limit", &APP_WRITER, body(2), id, "2026-10-12T00:00:00.000Z");
    assert!(own(&held).is_err_and(|e| e.contains("record identity conflict")));
    push(&other, b"{\"torn");
    assert!(own("rec:app:index-guard-1").is_ok());
    push(&other, b"\n");
    assert!(own("rec:app:index-guard-2").is_err_and(|e| e.contains("record-set conflict/incomplete")));
    std::fs::remove_dir_all(root).unwrap();
}

// Review R11 G1 probe: a 40-entry log (~13.6 KB), edited in place before the
// kept 4 KiB. A same-size edit (line 1 damaged, or an early identity made a
// duplicate of another) is a change without the growth pattern, so the log is
// read in full and the index reports what the full reader reports. An edit
// made together with an append (the log only grew) is found by the verifier's
// pass, and an entry read again from its stored position that no longer holds
// it fails as incomplete and makes the next refresh read the log in full.
#[test]
fn probe_r11_in_place_edit_beyond_guard() {
    let root = scratch();
    let log = crate::storage::project_log(&root, None, "edited").unwrap();
    let padded = |n: usize| json!({"label":"unresolvable reference","subjectRef":format!("edit {n}"),"detail":"x".repeat(240)});
    for n in 0..40 { append(&log, "evidence_limit", &APP_WRITER, padded(n)).unwrap(); }
    let original = std::fs::read(&log).unwrap();
    assert!(original.len() > 13_000, "{}", original.len());
    agree(&root, "40 entries");
    let lines: Vec<&[u8]> = original.split(|b| *b == b'\n').collect();
    let id_of = |line: &[u8]| serde_json::from_slice::<Value>(line).unwrap()["recordId"].as_str().unwrap().to_owned();
    let (first_id, second_id) = (id_of(lines[0]), id_of(lines[1]));
    let pause = || std::thread::sleep(std::time::Duration::from_millis(5));
    // Line 1 damaged, same size.
    let mut damaged = original.clone();
    damaged[1] = b'#';
    pause();
    std::fs::write(&log, &damaged).unwrap();
    agree(&root, "line 1 damaged at the same size");
    assert!(with_index(&root, |ix| ix.limits()).iter().any(|l| l.contains("unreadable line 1")));
    // An early identity made a duplicate of another, same size.
    let duplicated = String::from_utf8(original.clone()).unwrap().replacen(&first_id, &second_id, 1);
    pause();
    std::fs::write(&log, duplicated.as_bytes()).unwrap();
    agree(&root, "early identity duplicated at the same size");
    assert!(with_index(&root, |ix| ix.limits()).iter().any(|l| l.contains("duplicate record identity")));
    pause();
    std::fs::write(&log, &original).unwrap();
    agree(&root, "restored");
    // An edit beyond the kept 4 KiB together with an append: the verifier finds it.
    let mut grown = damaged.clone();
    let extra = crate::records::envelope("evidence_limit", &APP_WRITER, padded(40), "rec:app:edit-41".into(), 41, None, None);
    grown.extend(serde_json::to_vec(&extra).unwrap());
    grown.push(b'\n');
    pause();
    std::fs::write(&log, &grown).unwrap();
    let _ = with_index(&root, |ix| ix.limits());
    assert!(verify(&root) >= 1, "the verifier replaces the log it finds changed");
    agree(&root, "after the verifier's pass");
    // A line read again that no longer holds its indexed entry: incomplete, then a full read.
    pause();
    std::fs::write(&log, &original).unwrap();
    agree(&root, "restored again");
    let mut moved = String::from_utf8(original.clone()).unwrap().replacen(&first_id, &"0".repeat(first_id.len()), 1).into_bytes();
    moved.extend(serde_json::to_vec(&crate::records::envelope("evidence_limit", &APP_WRITER, padded(41), "rec:app:edit-41".into(), 41, None, None)).unwrap());
    moved.push(b'\n');
    pause();
    std::fs::write(&log, &moved).unwrap();
    let read = with_index(&root, |ix| ix.entries_with(&first_id));
    assert!(read.as_ref().is_err_and(|e| e.contains("read again in full")) || read.as_ref().is_ok_and(|v| v.is_empty()), "{read:?}");
    agree(&root, "after a failed re-read");
    std::fs::remove_dir_all(root).unwrap();
}

// Review R11 G3: a log added to a directory whose stamp the index already
// holds is found by the verifier's pass, which lists every directory again.
#[test]
fn the_verifier_lists_every_directory_again() {
    let root = scratch();
    let first = crate::storage::project_log(&root, None, "first").unwrap();
    append(&first, "evidence_limit", &APP_WRITER, body(1)).unwrap();
    agree(&root, "one log");
    // Make the index's directory stamp stale-looking: forget the listing's content.
    {
        let mut all = INDEXES.lock().unwrap();
        let (_, ix) = all.iter_mut().find(|(r, _)| *r == root).unwrap();
        for (_, (_, children)) in ix.dirs.iter_mut() { children.clear(); }
    }
    let ids = with_index(&root, |ix| { let mut count = 0; ix.db.as_ref().unwrap().lines("", None, |_, _| { count += 1; Ok(()) }).unwrap(); count });
    assert_eq!(ids, 0, "a cached listing hides the log until listed again");
    verify(&root);
    agree(&root, "after the verifier's pass");
    std::fs::remove_dir_all(root).unwrap();
}

// Review R11 G1 (3): a writer's first use of its owning log in this process reads
// that log in full, so an edit the index missed (made with an append, beyond the
// kept 4 KiB) refuses the append instead of passing unseen.
#[test]
fn a_writers_first_open_reads_its_log_in_full() {
    let root = scratch();
    let log = crate::storage::project_log(&root, None, "first-open").unwrap();
    let padded = |n: usize| json!({"label":"unresolvable reference","subjectRef":format!("open {n}"),"detail":"x".repeat(240)});
    // Written outside this index's writer bookkeeping: lines built directly.
    let mut bytes = Vec::new();
    for n in 0..40u64 {
        bytes.extend(serde_json::to_vec(&crate::records::envelope("evidence_limit", &APP_WRITER, padded(n as usize), format!("rec:app:open-{n}"), n + 1, None, None)).unwrap());
        bytes.push(b'\n');
    }
    std::fs::create_dir_all(log.parent().unwrap()).unwrap();
    std::fs::write(&log, &bytes).unwrap();
    agree(&root, "read by a reader first");
    bytes[1] = b'#';
    bytes.extend(serde_json::to_vec(&crate::records::envelope("evidence_limit", &APP_WRITER, padded(40), "rec:app:open-40".into(), 41, None, None)).unwrap());
    bytes.push(b'\n');
    std::thread::sleep(std::time::Duration::from_millis(5));
    std::fs::write(&log, &bytes).unwrap();
    let refused = append(&log, "evidence_limit", &APP_WRITER, body(99)).unwrap_err();
    assert!(refused.contains("incomplete owning log") && refused.contains("unreadable line 1"), "{refused}");
    std::fs::remove_dir_all(root).unwrap();
}

// SQLite contains only hints. Its deletion/corruption/tampering must never
// invent a record or erase an identity from a writer's conflict check.
#[test]
fn deleted_corrupt_and_tampered_sqlite_caches_rebuild_from_logs() {
    let root = scratch();
    let log = crate::storage::project_log(&root, None, "sqlite-authority").unwrap();
    let first = append(&log, "evidence_limit", &APP_WRITER, body(1)).unwrap();
    let id = first["recordId"].as_str().unwrap();
    let cache = || with_index(&root, |ix| ix.db.as_ref().unwrap().path.clone());
    let at = cache();
    let external = rusqlite::Connection::open(&at).unwrap();
    external.execute("DELETE FROM entries", []).unwrap();
    drop(external);
    assert!(with_index(&root, |ix| ix.holds(id)), "omitted SQL row cannot establish absence");
    agree(&root, "SQL row omission");
    let at = cache();
    std::fs::remove_file(&at).unwrap();
    assert_eq!(with_index(&root, |ix| ix.entries_with(id)).unwrap(), vec![first.clone()]);
    agree(&root, "deleted database");
    let at = cache();
    std::fs::write(&at, b"not SQLite").unwrap();
    assert_eq!(with_index(&root, |ix| ix.entries_with(id)).unwrap(), vec![first.clone()]);
    agree(&root, "corrupt database");
    // A cache changed after refresh, inside the same query request, takes the
    // source-scan fallback immediately rather than trusting stale metadata.
    with_index(&root, |ix| {
        let external = rusqlite::Connection::open(&ix.db.as_ref().unwrap().path).unwrap();
        external.execute("DELETE FROM entries", []).unwrap();
        assert!(ix.holds(id));
        assert_eq!(ix.entries_with(id).unwrap(), vec![first.clone()]);
        assert_eq!(ix.limits(), Vec::<String>::new());
        assert!(ix.cache_fault.get());
    });
    agree(&root, "cache changed within request");
    // Replacement by a symlink must neither read nor remove the target.
    let at = cache();
    let outside = root.join("outside.sqlite");
    std::fs::write(&outside, b"outside unchanged").unwrap();
    std::fs::remove_file(&at).unwrap();
    std::os::unix::fs::symlink(&outside, &at).unwrap();
    assert!(with_index(&root, |ix| ix.holds(id)));
    assert_eq!(std::fs::read(&outside).unwrap(), b"outside unchanged");
    assert!(std::fs::symlink_metadata(&at).unwrap().file_type().is_symlink());
    std::fs::remove_file(at).unwrap();
    std::fs::remove_dir_all(root).unwrap();
}

#[test]
fn source_scan_fallback_and_sqlite_keep_group_members_and_duplicate_limits() {
    let root = scratch();
    let log = crate::storage::project_log(&root, Some("run:sqlite-group"), "sqlite-group").unwrap();
    let specs = (0..2).map(|n| crate::records::Spec { kind:"evidence_limit", recorder:&APP_WRITER, body:body(n), id:format!("rec:sqlite-group-{n}"), observed_at:None }).collect();
    let entries = crate::records::append_group(&log, specs, Some("run:sqlite-group"), crate::records::RecordSet::Complete).unwrap();
    agree(&root, "group positions in SQL");
    for entry in &entries {
        assert_eq!(with_index(&root, |ix| ix.entries_with(entry["recordId"].as_str().unwrap())).unwrap(), vec![entry.clone()]);
    }
    // The exceptional no-database path rereads sources and preserves guards.
    with_index(&root, |ix| {
        // Break SQLite after refresh; source scanning is this request's fallback.
        std::fs::remove_file(&ix.db.as_ref().unwrap().path).unwrap();
        for entry in &entries {
            let id = entry["recordId"].as_str().unwrap();
            assert!(ix.holds(id));
            assert_eq!(ix.entries_with(id).unwrap(), vec![entry.clone()]);
        }
        assert!(!ix.holds("rec:absent"));
    });
    let duplicate = crate::storage::project_log(&root, Some("run:sqlite-group"), "duplicate-group").unwrap();
    std::fs::create_dir_all(duplicate.parent().unwrap()).unwrap();
    std::fs::copy(&log, &duplicate).unwrap();
    agree(&root, "duplicates of grouped entries");
    assert_eq!(with_index(&root, |ix| ix.entries_with("rec:sqlite-group-0")).unwrap().len(), 2);
    std::fs::remove_dir_all(root).unwrap();
}

#[test]
fn rebuilding_or_evicting_an_index_changes_its_act_epoch() {
    let root = scratch();
    let first = with_index(&root, |ix| ix.act_epoch());
    INDEXES.lock().unwrap().retain(|(r, _)| r != &root);
    let second = with_index(&root, |ix| ix.act_epoch());
    assert_ne!(first, second, "an act projection must not survive a rebuilt index under a reused epoch");
    let cache = with_index(&root, |ix| ix.db.as_ref().unwrap().path.clone());
    std::fs::remove_file(cache).unwrap();
    assert_ne!(second, with_index(&root, |ix| ix.act_epoch()));
    std::fs::remove_dir_all(root).unwrap();
}

#[test]
fn unreadable_source_is_a_limit_and_cache_fallback_never_establishes_absence() {
    use std::os::unix::fs::PermissionsExt;
    let root = scratch();
    let log = crate::storage::project_log(&root, None, "unreadable-source").unwrap();
    let entry = append(&log, "evidence_limit", &APP_WRITER, body(1)).unwrap();
    std::fs::set_permissions(&log, std::fs::Permissions::from_mode(0)).unwrap();
    if std::fs::File::open(&log).is_ok() {
        // Elevated test runners can bypass mode bits; they cannot witness this case.
        std::fs::set_permissions(&log, std::fs::Permissions::from_mode(0o600)).unwrap();
        std::fs::remove_dir_all(root).unwrap();
        return;
    }
    agree(&root, "unreadable owning file");
    with_index(&root, |ix| {
        assert!(ix.limits().iter().any(|l| l.contains("incomplete record:")));
        std::fs::remove_file(&ix.db.as_ref().unwrap().path).unwrap();
        assert!(ix.holds("rec:absent"), "a failed source scan cannot prove absence");
        assert!(ix.entries_with(entry["recordId"].as_str().unwrap()).is_err());
    });
    std::fs::set_permissions(&log, std::fs::Permissions::from_mode(0o600)).unwrap();
    agree(&root, "read permission restored");
    std::fs::remove_dir_all(root).unwrap();
}

// Index-only memory/latency measurement: no capture or act projection, one
// owning log with 30k/300k records. Each measurement runs in a fresh child so
// peak RSS belongs to this cache build, rather than earlier tests/generation.
// cargo test --offline --lib records_index_disk_scale_report -- --ignored --nocapture --test-threads=1
const INDEX_SCALE_CHILD: &str = "records_index::tests::records_index_disk_scale_child";
fn index_scale_rss() -> u64 {
    let mut usage: libc::rusage = unsafe { std::mem::zeroed() };
    unsafe { libc::getrusage(libc::RUSAGE_SELF, &mut usage); }
    if cfg!(target_os = "macos") { usage.ru_maxrss as u64 } else { usage.ru_maxrss as u64 * 1024 }
}
fn index_scale_ms(at: std::time::Instant) -> f64 { (at.elapsed().as_secs_f64() * 10_000.0).round() / 10.0 }
#[test]
#[ignore = "child process of records_index_disk_scale_report"]
fn records_index_disk_scale_child() {
    let Ok(spec) = std::env::var("CHIRALITY_INDEX_SCALE_CHILD") else { return };
    let spec: Value = serde_json::from_str(&spec).unwrap();
    let root = PathBuf::from(spec["root"].as_str().unwrap());
    let log = PathBuf::from(spec["log"].as_str().unwrap());
    let start = std::time::Instant::now();
    let rss_before = index_scale_rss();
    let (limits, held, db_bytes) = with_index_writing(&root, &log, |ix| {
        (ix.limits().len(), ix.holds("rec:index-scale-0"), std::fs::metadata(&ix.db.as_ref().unwrap().path).unwrap().len())
    });
    let build = index_scale_ms(start);
    let rss_built = index_scale_rss();
    let start = std::time::Instant::now();
    for n in 0..10 { append(&log, "evidence_limit", &APP_WRITER, body(n)).unwrap(); }
    let append = index_scale_ms(start) / 10.0;
    let start = std::time::Instant::now();
    let replaced = verify(&root);
    println!("INDEX-SCALE-RESULT {}", json!({"buildMs":build,"rssBeforeBytes":rss_before,"peakRssAfterBuildBytes":rss_built,"databaseBytes":db_bytes,
        "nextAppendMs":append,"limits":limits,"held":held,"verifyMs":index_scale_ms(start),"verifyReplaced":replaced,"peakRssBytes":index_scale_rss()}));
    close_all();
}
#[test]
#[ignore = "bounded disk query index measurement; run on request"]
fn records_index_disk_scale_report() {
    use std::io::Write;
    for count in [30_000usize, 300_000] {
        let root = scratch();
        let log = crate::storage::project_log(&root, None, "index-scale").unwrap();
        std::fs::create_dir_all(log.parent().unwrap()).unwrap();
        let mut out = std::io::BufWriter::new(std::fs::File::create(&log).unwrap());
        let mut previous = None;
        for n in 0..count {
            let mut entry = crate::records::envelope("evidence_limit", &APP_WRITER, body(n), format!("rec:index-scale-{n}"), n as u64 + 1, None, None);
            entry["prevLine"] = crate::record_lines::link(previous.as_deref());
            let bytes = serde_json::to_vec(&entry).unwrap();
            previous = Some(crate::record_lines::line_identity(&bytes));
            out.write_all(&bytes).unwrap(); out.write_all(b"\n").unwrap();
        }
        out.flush().unwrap(); drop(out);
        let spec = json!({"root":root,"log":log});
        let output = std::process::Command::new(std::env::current_exe().unwrap())
            .args([INDEX_SCALE_CHILD, "--exact", "--ignored", "--nocapture", "--test-threads=1"])
            .env("CHIRALITY_INDEX_SCALE_CHILD", spec.to_string())
            .env(crate::records_store::OVERRIDE_ENV, crate::records_store::current().unwrap().root)
            .output().unwrap();
        assert!(output.status.success(), "{} {}", String::from_utf8_lossy(&output.stdout), String::from_utf8_lossy(&output.stderr));
        let text = String::from_utf8_lossy(&output.stdout);
        let result = text.lines().find_map(|l| l.split_once("INDEX-SCALE-RESULT ").map(|(_, r)| r)).expect("child result");
        println!("INDEX-SCALE {}", json!({"entries":count,"recordLogBytes":std::fs::metadata(&log).unwrap().len(),"index":serde_json::from_str::<Value>(result).unwrap()}));
        // An optional already-built baseline binary can run its existing
        // index-only child on these same logs without copying source/builds.
        if let Ok(binary) = std::env::var("CHIRALITY_INDEX_BASELINE_BINARY") {
            let output = std::process::Command::new(binary)
                .args(["runtime_session::workflow_root_tests::records_scale_child", "--exact", "--ignored", "--nocapture", "--test-threads=1"])
                .env("CHIRALITY_SCALE_CHILD", json!({"what":"index","root":root,"keys":root.join("unused-keys")}).to_string())
                .env(crate::records_store::OVERRIDE_ENV, crate::records_store::current().unwrap().root)
                .output().unwrap();
            assert!(output.status.success(), "{} {}", String::from_utf8_lossy(&output.stdout), String::from_utf8_lossy(&output.stderr));
            let text = String::from_utf8_lossy(&output.stdout);
            let result = text.lines().find_map(|l| l.split_once("SCALE-RESULT ").map(|(_, r)| r)).expect("baseline child result");
            println!("INDEX-SCALE-BASELINE {}", json!({"entries":count,"index":serde_json::from_str::<Value>(result).unwrap()}));
        }
        let _ = std::fs::remove_dir_all(log.parent().unwrap().parent().unwrap());
        std::fs::remove_dir_all(root).unwrap();
    }
}

#[test]
fn replacing_cache_during_a_transaction_never_adopts_or_deletes_the_substitute() {
    let root = scratch();
    let mut db = query::QueryDb::open(&root).unwrap();
    let at = db.path.clone();
    db.begin_log(1, 0).unwrap();
    db.insert(1, &Line { id:Some("rec:cache-replaced".into()), offset:0, len:1, seq:1, act:false, corrects:None, late_subject:None, member:None, digest:"0".repeat(64) }).unwrap();
    std::fs::remove_file(&at).unwrap();
    std::fs::write(&at, b"replacement must survive").unwrap();
    assert!(db.finish_log(true).is_err(), "commit through an unlinked descriptor cannot adopt another file");
    assert!(!db.unchanged());
    drop(db);
    assert_eq!(std::fs::read(&at).unwrap(), b"replacement must survive");
    std::fs::remove_file(at).unwrap();
    std::fs::remove_dir_all(root).unwrap();
}

#[test]
fn an_external_sql_omission_cannot_be_adopted_by_an_unrelated_log_update() {
    let root = scratch();
    let mut db = query::QueryDb::open(&root).unwrap();
    let at = db.path.clone();
    let line = Line { id:Some("rec:cache-held".into()), offset:0, len:1, seq:1, act:false, corrects:None, late_subject:None, member:None, digest:"0".repeat(64) };
    db.begin_log(1, 0).unwrap(); db.insert(1, &line).unwrap(); db.finish_log(true).unwrap();
    assert!(db.holds("rec:cache-held").unwrap());
    assert!(db.unchanged()); // outer refresh check, before discovery
    let external = rusqlite::Connection::open(&at).unwrap();
    external.execute("DELETE FROM entries WHERE id='rec:cache-held'", []).unwrap();
    assert!(db.begin_log(2, 0).is_err(), "an unrelated update must refuse the changed cache basis");
    assert!(db.insert(2, &line).is_err());
    assert!(db.finish_log(true).is_err(), "failed begin cannot restamp an external omission");
    assert!(!db.unchanged());
    assert!(db.holds("rec:cache-held").is_err());
    drop(external); drop(db);
    std::fs::remove_file(at).unwrap();
    std::fs::remove_dir_all(root).unwrap();
}

#[test]
fn normal_exit_clears_owned_caches_and_preserves_substituted_leaves() {
    let first = scratch();
    let second = scratch();
    let owned = with_index(&first, |ix| ix.db.as_ref().unwrap().path.clone());
    let replaced = with_index(&second, |ix| ix.db.as_ref().unwrap().path.clone());
    std::fs::remove_file(&replaced).unwrap();
    std::fs::write(&replaced, b"exit must preserve replacement").unwrap();
    close_all();
    assert!(!owned.exists());
    assert_eq!(std::fs::read(&replaced).unwrap(), b"exit must preserve replacement");
    assert!(INDEXES.lock().unwrap().is_empty());
    std::fs::remove_file(replaced).unwrap();
    std::fs::remove_dir_all(first).unwrap();
    std::fs::remove_dir_all(second).unwrap();
}

#[test]
fn new_changed_and_removed_correction_targets_invalidate_act_claims() {
    let root = scratch();
    let correction_log = crate::storage::project_log(&root, None, "correction-sql").unwrap();
    std::fs::create_dir_all(correction_log.parent().unwrap()).unwrap();
    let mut correction = crate::records::envelope("evidence_limit", &APP_WRITER, body(2), "rec:correction-sql".into(), 1, None, None);
    correction["corrects"] = json!("rec:correction-target-sql");
    correction["correctionReason"] = json!("subject corrected");
    correction["prevLine"] = crate::record_lines::link(None);
    crate::schema_validation::bundled().unwrap().validate(&correction).unwrap();
    push(&correction_log, format!("{correction}\n").as_bytes());
    let before = with_index(&root, |ix| { assert_eq!(ix.act_claims().unwrap().len(), 1); ix.act_epoch() });
    let target = crate::records::append_project_reserved(&root, "run:correction-target", "correction-target-sql", "evidence_limit", &APP_WRITER, body(1), "rec:correction-target-sql", "2026-10-13T00:00:00.000Z").unwrap();
    let target_log = crate::storage::project_log(&root, Some("run:correction-target"), "correction-target-sql").unwrap();
    let added = with_index(&root, |ix| { assert_eq!(ix.act_claims().unwrap().len(), 2); ix.act_epoch() });
    assert_ne!(before, added, "a formerly missing target changes the claims");
    let mut changed = target;
    changed["body"] = body(3);
    std::fs::write(&target_log, format!("{changed}\n")).unwrap();
    let replaced = with_index(&root, |ix| { let claims = ix.act_claims().unwrap(); assert!(claims.iter().any(|c| c["record"] == changed)); ix.act_epoch() });
    assert_ne!(added, replaced);
    std::fs::remove_file(target_log).unwrap();
    let removed = with_index(&root, |ix| { assert_eq!(ix.act_claims().unwrap().len(), 1); ix.act_epoch() });
    assert_ne!(replaced, removed);
    // An unrelated non-act entry has no effect on the correction relation.
    append_project(&root, Some("run:unrelated-sql"), "unrelated-sql", "evidence_limit", &APP_WRITER, body(4)).unwrap();
    assert_eq!(removed, with_index(&root, |ix| ix.act_epoch()));
    std::fs::remove_dir_all(root).unwrap();
}

#[test]
fn the_verifiers_expensive_read_leaves_index_consumers_running() {
    use std::sync::mpsc;
    use std::time::Duration;
    let root = scratch();
    let log = crate::storage::project_log(&root, None, "verifier-outside-lock").unwrap();
    let first = append(&log, "evidence_limit", &APP_WRITER, body(1)).unwrap();
    with_index(&root, |_| {});
    append(&log, "evidence_limit", &APP_WRITER, body(2)).unwrap();
    // The final append has not yet been read into the index. This exercises
    // the changed-source install branch, not only an unchanged full pass.
    let (paused_tx, paused_rx) = mpsc::channel();
    let (release_tx, release_rx) = mpsc::channel();
    let verifying = root.clone();
    let worker = std::thread::spawn(move || {
        VERIFY_READ_HOOK.with(|h| *h.borrow_mut() = Some(Box::new(move || {
            paused_tx.send(()).unwrap();
            release_rx.recv_timeout(Duration::from_secs(5)).unwrap();
        })));
        verify(&verifying)
    });
    paused_rx.recv_timeout(Duration::from_secs(5)).unwrap();
    let free = INDEXES.try_lock().is_ok();
    let consumed = free && with_index(&root, |ix| ix.holds(first["recordId"].as_str().unwrap()));
    // Release before asserting so a failing test cannot strand the verifier.
    release_tx.send(()).unwrap();
    assert!(free, "full parsing/staging must not hold the shared index lock");
    assert!(consumed, "an ordinary consumer can finish while the verifier is paused");
    worker.join().unwrap();
    assert!(with_index(&root, |ix| ix.holds(first["recordId"].as_str().unwrap())));
    agree(&root, "verified outside the shared lock");
    std::fs::remove_dir_all(root).unwrap();
}

#[test]
fn the_verifier_updates_idle_status_for_new_removed_and_undiscoverable_logs() {
    let root = scratch();
    let first = crate::storage::project_log(&root, None, "idle-first").unwrap();
    append(&first, "evidence_limit", &APP_WRITER, body(1)).unwrap();
    with_index(&root, |_| {});
    let second = crate::storage::project_log(&root, None, "idle-second").unwrap();
    let mut entry = crate::records::envelope("evidence_limit", &APP_WRITER, body(2), "rec:idle-second".into(), 1, None, None);
    entry["prevLine"] = crate::record_lines::link(None);
    std::fs::write(&second, format!("{entry}\n")).unwrap();
    assert!(verify(&root) >= 1);
    assert_eq!(chain_status(Some(&root))["logs"], 2);
    std::fs::remove_file(&first).unwrap();
    assert!(verify(&root) >= 1);
    assert_eq!(chain_status(Some(&root))["logs"], 1);
    // Failed discovery is unknown membership, never evidence that every log
    // vanished; the idle status explicitly carries its limit.
    let linked = second.with_file_name("refused-link.jsonl");
    std::os::unix::fs::symlink(&second, &linked).unwrap();
    verify(&root);
    let status = chain_status(Some(&root));
    assert!(status["discoveryLimit"].as_str().unwrap().contains("symlink"));
    assert_eq!(status["logs"], 1);
    std::fs::remove_file(linked).unwrap();
    verify(&root);
    assert!(chain_status(Some(&root))["discoveryLimit"].is_null());
    agree(&root, "idle verifier discovers/removes/refuses links");
    std::fs::remove_dir_all(root).unwrap();
}

#[test]
fn a_reader_refresh_during_verification_wins_over_older_staged_positions() {
    let root = scratch();
    let log = crate::storage::project_log(&root, None, "verifier-reader-race").unwrap();
    append(&log, "evidence_limit", &APP_WRITER, body(1)).unwrap();
    let reading = root.clone();
    let log_edit = log.clone();
    VERIFY_READ_HOOK.with(|h| *h.borrow_mut() = Some(Box::new(move || {
        // A replacement seen by an ordinary reader while the verifier is
        // parsing its old descriptor gets a new revision and must win.
        let mut entry = crate::records::envelope("evidence_limit", &APP_WRITER, body(3), "rec:verifier-race-new".into(), 1, None, None);
        entry["prevLine"] = crate::record_lines::link(None);
        let other = log_edit.with_extension("replacement");
        std::fs::write(&other, format!("{entry}\n")).unwrap();
        std::fs::rename(other, &log_edit).unwrap();
        assert!(with_index(&reading, |ix| ix.holds("rec:verifier-race-new")));
    })));
    verify(&root);
    assert!(with_index(&root, |ix| ix.holds("rec:verifier-race-new")));
    agree(&root, "reader wins while verifier parses old file");
    std::fs::remove_dir_all(root).unwrap();
}

#[test]
fn staged_positions_copy_only_while_cache_and_source_proofs_remain_valid() {
    let root = scratch();
    let mut stage = query::QueryDb::open(&root).unwrap();
    let stage_path = stage.path.clone();
    let mut main = query::QueryDb::open(&root).unwrap();
    let main_path = main.path.clone();
    let line = Line { id:Some("rec:staged-position".into()), offset:0, len:1, seq:1, act:false, corrects:None, late_subject:None, member:None, digest:"0".repeat(64) };
    stage.begin_log(1, 0).unwrap(); stage.insert(1, &line).unwrap(); stage.finish_log(true).unwrap();
    main.copy_log(&stage, 1, 0, || true).unwrap();
    assert!(main.holds("rec:staged-position").unwrap());
    assert!(stage.unchanged());
    // A source change during the copy invalidates the derivative destination,
    // even if SQLite itself could commit the staged positions successfully.
    assert!(main.copy_log(&stage, 1, 0, || false).is_err());
    assert!(!main.unchanged());
    assert!(main.holds("rec:staged-position").is_err());
    drop(main);
    std::fs::remove_file(main_path).unwrap();
    let mut main = query::QueryDb::open(&root).unwrap();
    let main_path = main.path.clone();
    assert!(main.copy_log(&stage, 1, 0, || {
        std::fs::remove_file(&stage_path).unwrap();
        std::fs::write(&stage_path, b"foreign staging substitute").unwrap();
        true
    }).is_err());
    assert!(!main.unchanged());
    drop(main); drop(stage);
    assert_eq!(std::fs::read(&stage_path).unwrap(), b"foreign staging substitute");
    std::fs::remove_file(stage_path).unwrap();
    std::fs::remove_file(main_path).unwrap();
    std::fs::remove_dir_all(root).unwrap();
}

#[test]
fn an_older_verifier_listing_cannot_clear_a_newer_discovery_failure() {
    let root = scratch();
    let log = crate::storage::project_log(&root, None, "discovery-race").unwrap();
    append(&log, "evidence_limit", &APP_WRITER, body(1)).unwrap();
    with_index(&root, |_| {});
    let newer = root.clone();
    let linked = log.with_file_name("newer-symlink.jsonl");
    let target = log.clone();
    let hook_link = linked.clone();
    VERIFY_READ_HOOK.with(|h| *h.borrow_mut() = Some(Box::new(move || {
        std::os::unix::fs::symlink(target, hook_link).unwrap();
        with_index(&newer, |ix| assert!(ix.discovery_failed()));
    })));
    verify(&root);
    assert!(chain_status(Some(&root))["discoveryLimit"].as_str().unwrap().contains("symlink"));
    std::fs::remove_file(linked).unwrap();
    with_index(&root, |ix| assert!(!ix.discovery_failed()));
    agree(&root, "newer discovery failure survives older verifier listing");
    std::fs::remove_dir_all(root).unwrap();
}
