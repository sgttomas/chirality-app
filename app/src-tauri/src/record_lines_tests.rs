//! RS §13.8 "Units written together" and "Tamper-evidence": group lines
//! (whole, torn, refused by their rules), the chain (continuity, the head, a
//! broken chain never repaired, the unchained (legacy) boundary, an imported
//! pre-chain log), the run writer's W-2 retry of a unit, and the bounded index
//! and the readers on groups.
use super::*;
use crate::records::{self, RecordSet, Spec, APP_WRITER};
use crate::records_access::RecordsSource;
use crate::storage;
use std::path::{Path, PathBuf};

fn folder(prefix: &str) -> PathBuf {
    let p = std::env::temp_dir().join(crate::util::opaque_id(prefix).unwrap());
    std::fs::create_dir_all(&p).unwrap();
    std::fs::canonicalize(p).unwrap()
}
fn body(n: &str) -> Value {
    json!({"label":"unresolvable reference","subjectRef":n,"detail":"chain test"})
}
fn log_in(root: &Path) -> PathBuf {
    storage::project_log(root, None, "writer:chain").unwrap()
}
fn specs(n: usize, marker: &str) -> Vec<Spec<'static>> {
    (0..n).map(|i| Spec { kind: "evidence_limit", recorder: &APP_WRITER, body: body(&format!("{marker} {i}")), id: crate::util::opaque_id("rec:app:").unwrap(), observed_at: None }).collect()
}
fn group(log: &Path, n: usize, marker: &str) -> Vec<Value> {
    records::append_group(log, specs(n, marker), None, RecordSet::Complete).unwrap()
}
/// The complete lines on disk (without their LF).
fn raw_lines(log: &Path) -> Vec<Vec<u8>> {
    let bytes = std::fs::read(log).unwrap();
    let mut parts: Vec<Vec<u8>> = bytes.split(|b| *b == b'\n').map(<[u8]>::to_vec).collect();
    parts.pop();
    parts
}
fn value(raw: &[u8]) -> Value {
    serde_json::from_slice(raw).unwrap()
}
fn write_lines(log: &Path, lines: &[Vec<u8>]) {
    let mut out = Vec::new();
    for l in lines {
        out.extend(l);
        out.push(b'\n');
    }
    std::fs::write(log, out).unwrap();
}
fn without_link(raw: &[u8]) -> Vec<u8> {
    let mut v = value(raw);
    v.as_object_mut().unwrap().remove("prevLine");
    serde_json::to_vec(&v).unwrap()
}

// ---- Units written together ----

#[test]
fn a_group_is_one_line_that_every_reader_takes_whole() {
    let root = folder("group-whole-");
    let log = log_in(&root);
    let first = records::append(&log, "evidence_limit", &APP_WRITER, body("alone")).unwrap();
    let members = group(&log, 3, "member");
    let last = records::append(&log, "evidence_limit", &APP_WRITER, body("after")).unwrap();
    let lines = raw_lines(&log);
    assert_eq!(lines.len(), 3, "one line for the group");
    let line = value(&lines[1]);
    assert_eq!(line["format"], GROUP_FORMAT);
    assert!(line["groupId"].as_str().unwrap().starts_with("grp:app:"));
    assert_eq!(line["entries"].as_array().unwrap().iter().map(|e| e["seq"].as_u64().unwrap()).collect::<Vec<_>>(), [2, 3, 4]);
    assert!(line["entries"].as_array().unwrap().iter().all(|e| e.get("prevLine").is_none()), "the group line carries the link");
    assert_eq!(line["prevLine"]["value"], line_identity(&lines[0]));
    assert_eq!(last["seq"], 5);
    // R-2 as §13.8 reads it, through each reader.
    let (read, limits) = records::read_log(&log);
    assert!(limits.is_empty(), "{limits:?}");
    assert_eq!(read.iter().map(|e| e["seq"].as_u64().unwrap()).collect::<Vec<_>>(), [1, 2, 3, 4, 5]);
    assert_eq!(read[0]["recordId"], first["recordId"]);
    assert_eq!(&read[1..4], &members[..], "the members as written, in order");
    let (all, limits) = storage::read_all(&root);
    assert!(limits.is_empty(), "{limits:?}");
    assert_eq!(all.len(), 5);
    let corpus = crate::records_access::ProjectPaths::new(&root).read();
    assert!(corpus.limits.is_empty(), "{:?}", corpus.limits);
    assert_eq!(corpus.entries.iter().map(|e| e.line).collect::<Vec<_>>(), [1, 2, 2, 2, 3], "a member's line is its group's");
    // The bounded index: R-1 identity counting and each member re-read from its line.
    for m in &members {
        let id = m["recordId"].as_str().unwrap();
        let (holds, found) = crate::records_index::with_index(&root, |ix| (ix.holds(id), ix.entries_with(id)));
        assert!(holds);
        assert_eq!(found.unwrap(), vec![m.clone()]);
    }
    assert!(crate::records_index::with_index(&root, |ix| ix.limits()).is_empty());
    // Growth by a further group is read incrementally, as a full pass reads it.
    let more = group(&log, 2, "more");
    assert!(crate::records_index::with_index(&root, |ix| ix.holds(more[1]["recordId"].as_str().unwrap())));
    assert_eq!(crate::records_index::verify(&root), 0, "the incremental read equals the full read");
    // A unit repeats no identity, and none another entry holds.
    let mut twice = specs(2, "twice");
    twice[1].id = twice[0].id.clone();
    assert!(records::append_group(&log, twice, None, RecordSet::Complete).unwrap_err().contains("twice"));
    let mut held = specs(2, "held");
    held[1].id = members[0]["recordId"].as_str().unwrap().to_owned();
    assert!(records::append_group(&log, held, None, RecordSet::Complete).unwrap_err().contains("record identity conflict"));
    assert!(records::append_group(&log, specs(1, "one"), None, RecordSet::Complete).is_err(), "a group holds two or more");
    assert_eq!(raw_lines(&log).len(), 4, "nothing written by a refused unit");
    let _ = std::fs::remove_dir_all(&root);
}

#[test]
fn a_torn_group_is_only_a_partial_and_w0_terminates_it_outside_the_chain() {
    let root = folder("group-torn-");
    let log = log_in(&root);
    records::append(&log, "evidence_limit", &APP_WRITER, body("before")).unwrap();
    // A group line's write cut short: none of its members is read.
    let other = log.with_file_name("scratch-group.jsonl");
    group(&other, 2, "torn");
    let whole = std::fs::read(&other).unwrap();
    std::fs::remove_file(&other).unwrap();
    let mut bytes = std::fs::read(&log).unwrap();
    bytes.extend(&whole[..whole.len() / 2]);
    std::fs::write(&log, &bytes).unwrap();
    let (read, limits) = records::read_log(&log);
    assert_eq!(read.len(), 1, "no half group");
    assert_eq!(limits.len(), 1);
    assert!(limits[0].ends_with("partial entry at end (not read)"), "{limits:?}");
    // The reopened writer terminates it and names it; the torn line is not a link.
    let after = records::append(&log, "evidence_limit", &APP_WRITER, body("after")).unwrap();
    let lines = raw_lines(&log);
    assert_eq!(lines.len(), 4);
    let limit = value(&lines[2]);
    assert_eq!(limit["body"]["label"], records::PARTIAL_NOT_RECOVERED);
    assert_eq!(limit["prevLine"]["value"], line_identity(&lines[0]), "the limit links past the torn line");
    assert_eq!(value(&lines[3])["prevLine"]["value"], line_identity(&lines[2]));
    let (read, limits) = records::read_log(&log);
    assert!(limits.is_empty(), "{limits:?}");
    assert_eq!(read.last().unwrap()["recordId"], after["recordId"]);
    let parsed = parse(&std::fs::read(&log).unwrap(), "log", 0, 0, 1, Chain::default());
    assert!(parsed.lines[1].notes[0].contains("not a chain link"), "the reader notes the gap");
    let head = chain_head(&log);
    assert_eq!((head["head"].as_str(), head["lines"].as_u64(), head["broken"].as_array().unwrap().len()), (Some(line_identity(&lines[3]).as_str()), Some(3), 0), "{head}");
    // The records capability names the terminated line and reads the rest.
    let corpus = crate::records_access::ProjectPaths::new(&root).read();
    assert_eq!(corpus.entries.len(), 3);
    assert!(corpus.limits.iter().any(|l| l.contains("line 2 is a torn line")), "{:?}", corpus.limits);
    let _ = std::fs::remove_dir_all(&root);
}

#[test]
fn a_group_that_breaks_its_rules_is_not_read_at_all() {
    let root = folder("group-rules-");
    let log = log_in(&root);
    records::append(&log, "evidence_limit", &APP_WRITER, body("before")).unwrap();
    group(&log, 2, "good");
    let lines = raw_lines(&log);
    let good = value(&lines[1]);
    let bad = |edit: &dyn Fn(&mut Value)| {
        let mut g = good.clone();
        edit(&mut g);
        write_lines(&log, &[lines[0].clone(), serde_json::to_vec(&g).unwrap()]);
        let (read, limits) = records::read_log(&log);
        assert_eq!(read.len(), 1, "no member of a refused group is read: {g}");
        assert!(limits.iter().any(|l| l.contains("invalid line 2")), "{limits:?}");
        assert!(records::append(&log, "evidence_limit", &APP_WRITER, body("refused")).unwrap_err().contains("incomplete owning log"));
    };
    bad(&|g| g["entries"][1]["seq"] = json!(4));
    bad(&|g| g["entries"][1]["recordId"] = g["entries"][0]["recordId"].clone());
    bad(&|g| g["entries"][1]["runId"] = json!("run:other"));
    bad(&|g| g["entries"][1]["prevLine"] = g["prevLine"].clone());
    bad(&|g| g["entries"][1]["kind"] = json!("not a kind"));
    bad(&|g| { g["entries"].as_array_mut().unwrap().pop(); });
    let _ = std::fs::remove_dir_all(&root);
}

// ---- Tamper-evidence ----

#[test]
fn each_line_links_to_the_one_before_and_the_head_is_the_last() {
    let root = folder("chain-continuity-");
    let log = log_in(&root);
    for n in 0..3 {
        records::append(&log, "evidence_limit", &APP_WRITER, body(&format!("entry {n}"))).unwrap();
    }
    group(&log, 2, "unit");
    let lines = raw_lines(&log);
    assert_eq!(value(&lines[0])["prevLine"], json!({"method":LINE_METHOD,"value":null}), "the first line of a log");
    for pair in lines.windows(2) {
        assert_eq!(value(&pair[1])["prevLine"]["value"], line_identity(&pair[0]));
    }
    assert_eq!(line_identity(&lines[0]), crate::util::sha256_hex(&lines[0]));
    let head = chain_head(&log);
    assert_eq!(head["head"], line_identity(&lines[3]));
    assert_eq!((head["lines"].as_u64(), head["linked"].as_bool(), head["unchained"].as_u64()), (Some(4), Some(true), Some(0)));
    assert!(head["broken"].as_array().unwrap().is_empty() && head["unchainedLimit"].is_null(), "{head}");
    assert!(head["signedCheckpoints"].as_str().unwrap().contains("OI-011"));
    // The index holds the same head, for the host's status (the cache of
    // indexed projects is shared with tests running beside this one).
    let chains = crate::records_index::with_index(&root, |ix| ix.chains());
    let logged = chains.iter().find(|l| l["log"] == log.display().to_string()).cloned().unwrap_or_else(|| panic!("{chains:?}"));
    assert_eq!((&logged["head"], logged["lines"].as_u64(), logged["unchained"].as_u64()), (&head["head"], Some(4), Some(0)));
    let status = crate::records_index::chain_status(Some(&root));
    assert!(status["signedCheckpoints"].as_str().unwrap().contains("OI-011"), "{status}");
    if status["logs"].is_array() {
        assert!(status["broken"].as_array().unwrap().is_empty(), "{status}");
    }
    let unopened = folder("chain-unopened-");
    assert_eq!(crate::records_index::chain_status(Some(&unopened))["state"], "not read yet in this process", "status never reads a project first");
    let _ = std::fs::remove_dir_all(&unopened);
    let _ = std::fs::remove_dir_all(&root);
}

#[test]
fn an_edited_or_removed_line_breaks_the_chain_and_nothing_repairs_it() {
    let root = folder("chain-broken-");
    let log = log_in(&root);
    for n in 0..3 {
        records::append(&log, "evidence_limit", &APP_WRITER, body(&format!("entry {n}"))).unwrap();
    }
    let lines = raw_lines(&log);
    let broken = |edited: Vec<Vec<u8>>, at: usize| {
        write_lines(&log, &edited);
        let before = std::fs::read(&log).unwrap();
        let (_, limits) = records::read_log(&log);
        assert!(limits.iter().any(|l| l.contains(&format!("chain broken at line {at}")) && l.ends_with("never repaired")), "{limits:?}");
        assert!(!storage::read_all(&root).1.is_empty(), "a broken chain leaves the set incomplete");
        assert!(records::append(&log, "evidence_limit", &APP_WRITER, body("refused")).unwrap_err().contains("incomplete owning log"));
        assert!(records::append_project(&root, None, "writer:other", "evidence_limit", &APP_WRITER, body("other log")).unwrap_err().contains("incomplete"));
        assert_eq!(std::fs::read(&log).unwrap(), before, "never repaired");
        assert!(!chain_head(&log)["broken"].as_array().unwrap().is_empty());
        let corpus = crate::records_access::ProjectPaths::new(&root).read();
        assert!(corpus.limits.iter().any(|l| l.contains(&format!("the chain is broken at line {at}"))), "{:?}", corpus.limits);
    };
    // An entry edited in place (still valid, same seq).
    let mut edited = value(&lines[0]);
    edited["body"]["detail"] = json!("rewritten");
    broken(vec![serde_json::to_vec(&edited).unwrap(), lines[1].clone(), lines[2].clone()], 2);
    // A line removed (its seq gap aside, the next link names the removed line).
    broken(vec![lines[0].clone(), lines[2].clone()], 2);
    // A line without a link after linked lines.
    broken(vec![lines[0].clone(), lines[1].clone(), without_link(&lines[2])], 3);
    // A second chain started after earlier lines.
    let mut restarted = value(&lines[2]);
    restarted["prevLine"] = link(None);
    broken(vec![lines[0].clone(), lines[1].clone(), serde_json::to_vec(&restarted).unwrap()], 3);
    // Restored, the log reads and records again.
    write_lines(&log, &lines);
    assert!(records::read_log(&log).1.is_empty());
    records::append(&log, "evidence_limit", &APP_WRITER, body("restored")).unwrap();
    let _ = std::fs::remove_dir_all(&root);
}

#[test]
fn pre_chain_lines_read_as_unchained_legacy_and_the_chain_starts_after_them() {
    let root = folder("chain-legacy-");
    let log = log_in(&root);
    for n in 0..2 {
        records::append(&log, "evidence_limit", &APP_WRITER, body(&format!("legacy {n}"))).unwrap();
    }
    let legacy: Vec<Vec<u8>> = raw_lines(&log).iter().map(|l| without_link(l)).collect();
    write_lines(&log, &legacy);
    let read = records::read_log_parts(&log);
    assert!(read.limits.is_empty(), "unchained is not incomplete: {:?}", read.limits);
    assert_eq!(read.entries.len(), 2);
    let head = chain_head(&log);
    assert_eq!((head["linked"].as_bool(), head["unchained"].as_u64()), (Some(false), Some(2)));
    assert!(head["unchainedLimit"].as_str().unwrap().contains("unchained (legacy): no line carries a chain link (2 lines)"), "{head}");
    assert!(crate::records_index::with_index(&root, |ix| ix.notes()).iter().any(|n| n.contains(UNCHAINED)));
    let corpus = crate::records_access::ProjectPaths::new(&root).read();
    assert!(corpus.limits.iter().any(|l| l.contains("2 line(s) carry no chain link (unchained (legacy))")), "{:?}", corpus.limits);
    // The App's next line links to the last legacy line: the chain starts there.
    let next = records::append(&log, "evidence_limit", &APP_WRITER, body("chained")).unwrap();
    assert_eq!(next["prevLine"]["value"], line_identity(&legacy[1]));
    assert_eq!(&raw_lines(&log)[..2], &legacy[..], "legacy lines are never rewritten");
    let head = chain_head(&log);
    assert_eq!((head["linked"].as_bool(), head["unchained"].as_u64(), head["lines"].as_u64()), (Some(true), Some(2), Some(3)));
    assert!(head["unchainedLimit"].as_str().unwrap().contains("the chain starts after them"), "{head}");
    assert!(records::read_log(&log).1.is_empty());
    // An unchained line after the chain started is a break, not legacy.
    let mut lines = raw_lines(&log);
    lines.push(without_link(&lines[1]));
    write_lines(&log, &lines);
    assert!(records::read_log(&log).1.iter().any(|l| l.contains("chain broken at line 4")));
    let _ = std::fs::remove_dir_all(&root);
}

#[test]
fn an_imported_pre_chain_log_reads_unchained_and_recording_links_to_it() {
    let store = folder("chain-import-store-");
    crate::records_store::use_store_for_test(Some(Ok(crate::records_store::Store { root: store.clone(), placement: crate::records_store::Placement::Override, limits: vec![] })));
    let root = folder("chain-import-project-");
    // A §13.7 run log written before the chain (no line carries a link).
    let original = root.join(".chirality/records").join(storage::log_rel(Some("run:legacy"), "writer:legacy"));
    records::append(&original, "evidence_limit", &APP_WRITER, body("legacy 1")).unwrap();
    records::append(&original, "evidence_limit", &APP_WRITER, body("legacy 2")).unwrap();
    let legacy: Vec<Vec<u8>> = raw_lines(&original).iter().map(|l| without_link(l)).collect();
    write_lines(&original, &legacy);
    let imported = crate::records_store::import(&root).unwrap();
    assert_eq!(imported["state"], "imported", "{imported}");
    let (entries, limits) = storage::read_all(&root);
    assert!(limits.is_empty(), "{limits:?}");
    assert_eq!(entries.len(), 2);
    let copy = storage::project_log(&root, Some("run:legacy"), "writer:legacy").unwrap();
    assert!(copy.starts_with(&store));
    assert_eq!(chain_head(&copy)["unchained"], 2);
    let next = records::append_project(&root, Some("run:legacy"), "writer:legacy", "evidence_limit", &APP_WRITER, body("after import")).unwrap();
    assert_eq!((next["seq"].as_u64(), next["prevLine"]["value"].as_str()), (Some(3), Some(line_identity(&legacy[1]).as_str())));
    assert_eq!(&raw_lines(&copy)[..2], &legacy[..], "the imported copy's bytes are kept");
    assert_eq!(raw_lines(&original), legacy, "the original is not written");
    let head = chain_head(&copy);
    assert_eq!((head["linked"].as_bool(), head["lines"].as_u64()), (Some(true), Some(3)));
    crate::records_store::use_store_for_test(None);
    let _ = std::fs::remove_dir_all(&root);
    let _ = std::fs::remove_dir_all(&store);
}

// ---- The run writer's units (W-2) ----

fn pending(kind: &'static str, marker: &str) -> crate::records::supply::PendingRunEntry {
    crate::records::supply::PendingRunEntry::new(kind, body(marker), "2026-10-12T00:00:00.000Z".into()).unwrap()
}

#[test]
fn a_unit_retried_after_a_failure_is_written_once_whole_with_its_late_limits() {
    use crate::records::supply::{append_run_group_in, permanent_group_refusal_in, run_log};
    let root = folder("group-retry-");
    let run = "run:group-retry";
    // Another log of the project is unreadable: the unit waits (W-2), nothing written.
    let other = storage::project_log(&root, None, "writer:other").unwrap();
    std::fs::create_dir_all(other.parent().unwrap()).unwrap();
    std::fs::write(&other, b"not json\n").unwrap();
    let mut unit = vec![pending("evidence_limit", "first"), pending("evidence_limit", "second")];
    assert!(append_run_group_in(&root, run, &mut unit, RecordSet::Complete).is_err());
    assert!(unit.iter().all(|e| e.failure.is_some() && e.written.is_none()));
    assert!(permanent_group_refusal_in(&root, run, &unit, RecordSet::Complete).is_none(), "not permanent");
    assert!(!run_log(&root, run).unwrap().exists());
    std::fs::remove_file(&other).unwrap();
    let written = append_run_group_in(&root, run, &mut unit, RecordSet::Complete).unwrap();
    let log = run_log(&root, run).unwrap();
    let lines = raw_lines(&log);
    assert_eq!(lines.len(), 3, "the group, then one late-write limit per entry");
    assert_eq!(value(&lines[0])["entries"].as_array().unwrap(), &written);
    for (k, e) in unit.iter().enumerate() {
        let limit = value(&lines[k + 1]);
        assert_eq!((limit["body"]["label"].as_str(), limit["body"]["subjectRef"].as_str()), (Some("record write failed"), Some(e.record_id.as_str())));
    }
    // Retried again: the receipt, nothing more.
    assert_eq!(append_run_group_in(&root, run, &mut unit, RecordSet::Complete).unwrap(), written);
    assert_eq!(raw_lines(&log).len(), 3);
    // An uncertain earlier write that landed whole is its receipt.
    let mut landed = vec![pending("evidence_limit", "landed 1"), pending("evidence_limit", "landed 2")];
    let members = landed.iter().map(|p| (p.kind, p.body.clone(), p.record_id.as_str(), p.observed_at.as_str())).collect();
    records::append_project_group_in(&root, run, crate::records::supply::LIVE_WRITER, members, RecordSet::Complete).unwrap();
    let receipt = append_run_group_in(&root, run, &mut landed, RecordSet::Complete).unwrap();
    assert_eq!(receipt.len(), 2);
    assert_eq!(raw_lines(&log).len(), 4, "not written twice");
    // A unit only partly in its log cannot be reconciled: nothing is written.
    let mut partly = vec![pending("evidence_limit", "partly 1"), pending("evidence_limit", "partly 2")];
    records::append_project_reserved_in(&root, run, crate::records::supply::LIVE_WRITER, partly[0].kind, &APP_WRITER, partly[0].body.clone(), &partly[0].record_id, &partly[0].observed_at, RecordSet::Complete).unwrap();
    assert!(append_run_group_in(&root, run, &mut partly, RecordSet::Complete).unwrap_err().contains("only partly in its log"));
    assert_eq!(raw_lines(&log).len(), 5);
    // A permanent refusal of one entry refuses its unit.
    let mut refused = vec![pending("evidence_limit", "fine"), crate::records::supply::PendingRunEntry::new("act_counted", json!({}), "2026-10-12T00:00:00.000Z".into()).unwrap()];
    assert!(append_run_group_in(&root, run, &mut refused, RecordSet::Complete).is_err());
    let reason = permanent_group_refusal_in(&root, run, &refused, RecordSet::Complete).unwrap();
    assert!(reason.contains("nonconformant") && reason.contains("its unit of 2 entries stands whole"), "{reason}");
    assert_eq!(raw_lines(&log).len(), 5);
    let _ = std::fs::remove_dir_all(&root);
}

#[test]
fn recorder_units_pair_an_event_with_the_disposition_change_it_makes() {
    use crate::checkpoint_recorder::units;
    let change = |arrival: &str| ("disposition_change", json!({"arrival":arrival}));
    let outputs = vec![
        ("checkpoint_arrival", json!({"arrival":"a"})),
        change("a"),
        ("act_counted", json!({"arrival":"a"})),
        change("a"),
        ("act_not_counted", json!({"arrival":"a"})),
        change("b"),
        ("arrival_declined", json!({"arrival":"b"})),
        change("b"),
        ("act_lapsed", json!({"arrival":"b"})),
        change("b"),
        ("tool_permission_settlement", json!({})),
        ("tool_permission_settlement", json!({})),
        change("c"),
    ];
    assert_eq!(units(&outputs), vec![0..1, 1..2, 2..4, 4..5, 5..6, 6..8, 8..10, 10..11, 11..12, 12..13]);
    assert!(units(&[]).is_empty());
}
