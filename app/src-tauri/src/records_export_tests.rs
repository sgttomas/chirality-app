use super::*;
use crate::records_store::{self, Placement, Store};

struct Fixture { project: PathBuf, store: PathBuf, output: PathBuf }
impl Fixture {
    fn new() -> Self {
        let folder = |prefix| { let p = std::env::temp_dir().join(crate::util::opaque_id(prefix).unwrap()); std::fs::create_dir(&p).unwrap(); std::fs::canonicalize(p).unwrap() };
        let f = Self { project: folder("bag-project-"), store: folder("bag-store-"), output: folder("bag-output-") };
        records_store::use_store_for_test(Some(Ok(Store { root: f.store.clone(), placement: Placement::Override, limits: vec![] })));
        f
    }
    fn record(&self) -> PathBuf {
        crate::records::append_project(&self.project, Some("run:bag"), "app-writer:local", "evidence_limit", &crate::records::APP_WRITER,
            json!({"label":"unresolvable reference","subjectRef":"invented export fixture"})).unwrap();
        crate::storage::project_log(&self.project, Some("run:bag"), "app-writer:local").unwrap()
    }
    fn bag(&self) -> PathBuf { self.output.join("bag") }
}
impl Drop for Fixture {
    fn drop(&mut self) {
        records_store::use_store_for_test(None);
        for p in [&self.project, &self.store, &self.output] { let _ = std::fs::remove_dir_all(p); }
    }
}

#[test]
fn records_export_preserves_bytes_groups_heads_and_is_checkable_without_app() {
    let f = Fixture::new();
    let log = f.record();
    let specs = (0..2).map(|i| crate::records::Spec { kind: "evidence_limit", recorder: &crate::records::APP_WRITER,
        body: json!({"label":"unresolvable reference","subjectRef":format!("group member {i}")}),
        id: crate::util::opaque_id("rec:app:").unwrap(), observed_at: None }).collect();
    crate::records::append_group(&log, specs, Some("run:bag"), crate::records::RecordSet::Complete).unwrap();
    let dir = records_store::home(&f.project).unwrap().attachment.dir.unwrap();
    std::fs::create_dir_all(f.store.join("indexes")).unwrap();
    std::fs::write(f.store.join("indexes/query.sqlite"), b"discardable cache").unwrap();
    std::fs::create_dir_all(dir.join("connectors")).unwrap();
    std::fs::write(dir.join("connectors/account %\n.json"), b"invented account bytes").unwrap();
    std::fs::write(dir.join("connectors/account \u{2028}.json"), b"invented unicode filename").unwrap();
    std::fs::write(dir.join("connectors/.route-fixture.tmp"), b"interrupted publication evidence").unwrap();
    std::fs::write(dir.join("connectors/retained.lock"), b"retained imported bytes").unwrap();
    let result = export(&f.project, &f.bag()).unwrap();
    assert_eq!(result["state"], "verified export created");
    let rel = log.strip_prefix(&dir).unwrap();
    assert_eq!(std::fs::read(&log).unwrap(), std::fs::read(f.bag().join("data").join(rel)).unwrap());
    assert!(!f.bag().join("data/indexes").exists());
    assert!(!f.bag().join("data/.writer.lock").exists());
    assert_eq!(std::fs::read(f.bag().join("data/connectors/.route-fixture.tmp")).unwrap(), b"interrupted publication evidence");
    assert_eq!(std::fs::read(f.bag().join("data/connectors/retained.lock")).unwrap(), b"retained imported bytes");
    let output = std::process::Command::new("python3").arg(f.bag().join("verify.py")).arg(f.bag()).output().unwrap();
    assert!(output.status.success(), "{}", String::from_utf8_lossy(&output.stderr));
    assert!(export(&f.project, &f.bag()).is_err());
    // A later valid source append cannot change the earlier bag or its heads.
    f.record();
    assert!(verify(&f.bag()).is_ok());
}

#[test]
fn records_export_verifier_refuses_missing_extra_edited_or_linked_members() {
    let f = Fixture::new();
    f.record();
    export(&f.project, &f.bag()).unwrap();
    let payload = files(&f.bag().join("data"), false).unwrap().into_keys().next().unwrap();
    let path = f.bag().join("data").join(payload);
    let bytes = std::fs::read(&path).unwrap();
    std::fs::write(&path, b"edited").unwrap();
    assert!(verify(&f.bag()).is_err());
    std::fs::write(&path, &bytes).unwrap();
    std::fs::write(f.bag().join("data/extra"), b"extra").unwrap();
    assert!(verify(&f.bag()).is_err());
    std::fs::remove_file(f.bag().join("data/extra")).unwrap();
    std::fs::remove_file(&path).unwrap();
    assert!(verify(&f.bag()).is_err());
    std::os::unix::fs::symlink(f.project.join("anything"), &path).unwrap();
    assert!(verify(&f.bag()).is_err());
}

#[test]
fn records_export_refuses_unsafe_destination_and_linked_source_and_never_mints() {
    let f = Fixture::new();
    assert!(export(&f.project, &f.bag()).is_err());
    assert!(!f.project.join(".chirality/project.json").exists());
    f.record();
    assert!(export(&f.project, &f.store.join("bag")).is_err());
    assert!(export(&f.project, &f.project.join("bag")).is_err());
    let dir = records_store::home(&f.project).unwrap().attachment.dir.unwrap();
    std::os::unix::fs::symlink(f.project.join("anything"), dir.join("linked")).unwrap();
    assert!(export(&f.project, &f.bag()).is_err());
    assert!(!f.bag().exists());
}

#[test]
fn records_export_heads_cannot_be_substituted_even_with_rehashed_tags() {
    let f = Fixture::new(); f.record();
    export(&f.project, &f.bag()).unwrap();
    let mut h: Value = serde_json::from_slice(&std::fs::read(f.bag().join(HEADS)).unwrap()).unwrap();
    h["logs"][0]["chain"]["head"] = json!("0".repeat(64));
    std::fs::write(f.bag().join(HEADS), serde_json::to_vec(&h).unwrap()).unwrap();
    std::fs::write(f.bag().join("tagmanifest-sha256.txt"), manifest(&f.bag(), TAGS.iter().map(|s| s.to_string())).unwrap()).unwrap();
    assert!(verify(&f.bag()).is_err_and(|e| e.contains("chain heads differ")));
}

fn standalone(bag: &Path) -> std::process::Output {
    std::process::Command::new("python3").arg(bag.join("verify.py")).arg(bag).output().unwrap()
}

#[test]
fn records_export_standalone_recomputes_chains_and_refuses_a_changed_line_with_rehashed_manifests() {
    let f = Fixture::new();
    f.record();
    let log = f.record();
    export(&f.project, &f.bag()).unwrap();
    let unaltered = standalone(&f.bag());
    assert_eq!(unaltered.status.code(), Some(0), "{}", String::from_utf8_lossy(&unaltered.stderr));
    let stdout = String::from_utf8_lossy(&unaltered.stdout);
    assert!(stdout.starts_with("Package bytes: consistent."), "{stdout}");
    assert!(stdout.contains("\nLog integrity: no chain is broken and no line was set aside. Every link this verifier examined names the line before it.\n"), "{stdout}");
    assert!(stdout.contains("A package whose records, manifests and chain heads were replaced together still verifies."), "{stdout}");
    // Change the first line (same length, still JSON), then recompute both
    // manifests as an alterer would. Only the chain shows the change.
    let dir = records_store::home(&f.project).unwrap().attachment.dir.unwrap();
    let rel = log.strip_prefix(&dir).unwrap().to_str().unwrap().to_owned();
    let path = f.bag().join("data").join(&rel);
    let bytes = std::fs::read(&path).unwrap();
    let at = bytes.windows(7).position(|w| w == b"invente").unwrap();
    let mut changed = bytes.clone();
    changed[at] = b'I';
    std::fs::write(&path, &changed).unwrap();
    let paths = files(&f.bag().join("data"), false).unwrap().into_keys().map(|p| format!("data/{p}")).collect::<Vec<_>>();
    std::fs::write(f.bag().join("manifest-sha256.txt"), manifest(&f.bag(), paths.into_iter()).unwrap()).unwrap();
    std::fs::write(f.bag().join("tagmanifest-sha256.txt"), manifest(&f.bag(), TAGS.iter().map(|s| s.to_string())).unwrap()).unwrap();
    let altered = standalone(&f.bag());
    assert_eq!(altered.status.code(), Some(1));
    let stderr = String::from_utf8_lossy(&altered.stderr);
    assert!(stderr.starts_with("Result: failed (exit status 1).") && stderr.contains(&format!("{rel}: chain broken at line 2: it links to")) && stderr.contains("the package records no break there"), "{stderr}");
    // The App's own verification recomputes the heads and refuses it too.
    assert!(verify(&f.bag()).is_err_and(|e| e.contains("chain heads differ")));
    // With the chain-head tag recomputed as well, the package is the one a
    // store whose log was already broken would export: it agrees with itself,
    // which is the unsigned package's stated limit. Neither verification
    // refuses it, and neither lets consistent bytes stand for a whole log:
    // each says, separately, that this log's integrity is limited at line 2.
    reprofile_for_test(&f.bag());
    let app = verify(&f.bag()).unwrap();
    assert_eq!(app["state"], "package bytes consistent; log integrity limited");
    assert!(app["logIntegrity"]["limits"][0].as_str().unwrap().starts_with(&format!("{rel}: chain broken at line 2")), "{app}");
    let rewritten = standalone(&f.bag());
    assert_eq!(rewritten.status.code(), Some(2), "{}", String::from_utf8_lossy(&rewritten.stderr));
    let stdout = String::from_utf8_lossy(&rewritten.stdout);
    assert!(stdout.starts_with("Package bytes: consistent.") && stdout.contains("\nLog integrity: LIMITED. 1 limit in 1 log."), "{stdout}");
    assert!(stdout.contains(&format!("Integrity limit: {rel}: chain broken at line 2: it links to")), "{stdout}");
    assert!(!stdout.contains("no chain is broken") && !stdout.contains("exit status 0"), "{stdout}");
}

#[test]
fn records_export_preserves_imported_interrupted_connector_evidence() {
    let f = Fixture::new();
    let legacy = f.project.join(".chirality/records/connectors/route-accounts");
    std::fs::create_dir_all(&legacy).unwrap();
    for name in [".route-interrupted.tmp", "retained.lock"] { std::fs::write(legacy.join(name), name.as_bytes()).unwrap(); }
    records_store::import(&f.project).unwrap();
    export(&f.project, &f.bag()).unwrap();
    for name in [".route-interrupted.tmp", "retained.lock"] {
        assert_eq!(std::fs::read(f.bag().join("data/connectors/route-accounts").join(name)).unwrap(), name.as_bytes());
    }
}

#[test]
fn records_export_standalone_refuses_a_bag_without_its_payload_directory() {
    let f = Fixture::new(); f.record(); export(&f.project, &f.bag()).unwrap();
    std::fs::remove_dir_all(f.bag().join("data")).unwrap();
    std::fs::write(f.bag().join("manifest-sha256.txt"), b"").unwrap();
    std::fs::write(f.bag().join("tagmanifest-sha256.txt"), manifest(&f.bag(), TAGS.iter().map(|s| s.to_string())).unwrap()).unwrap();
    let output = std::process::Command::new("python3").arg(f.bag().join("verify.py")).arg(f.bag()).output().unwrap();
    assert!(!output.status.success());
    assert!(verify(&f.bag()).is_err());
}

#[test]
fn records_export_reports_published_location_when_folder_sync_fails() {
    let f = Fixture::new(); f.record();
    crate::storage::fail_directory_for_test(Some(f.output.clone()));
    let result = export(&f.project, &f.bag());
    crate::storage::fail_directory_for_test(None);
    let error = result.unwrap_err();
    assert!(error.contains("export published at") && error.contains("durability not established"));
    assert!(error.contains(f.bag().to_str().unwrap()));
    assert!(verify(&f.bag()).is_ok());
}

#[test]
fn records_export_verifier_refuses_fifo_tags_without_waiting_for_a_writer() {
    use std::os::unix::ffi::OsStrExt;
    let f = Fixture::new(); f.record(); export(&f.project, &f.bag()).unwrap();
    for name in ["bagit.txt", "manifest-sha256.txt", HEADS] {
        let path = f.bag().join(name);
        let original = std::fs::read(&path).unwrap();
        std::fs::remove_file(&path).unwrap();
        let c = std::ffi::CString::new(path.as_os_str().as_bytes()).unwrap();
        assert_eq!(unsafe { libc::mkfifo(c.as_ptr(), 0o600) }, 0);
        assert!(files(&f.bag(), false).is_err());
        assert!(read_tag(&path).is_err());
        assert!(verify(&f.bag()).is_err());
        std::fs::remove_file(&path).unwrap();
        std::fs::write(path, original).unwrap();
    }
}

#[test]
fn records_export_log_integrity_never_reads_a_missing_or_unreadable_statement_as_no_chain_broken() {
    let whole = json!({"logs":[{"log":"runs/a/b.jsonl","chain":{"head":"x","lines":1,"broken":[]}}]});
    assert_eq!(log_integrity(&whole, false), json!({"state":"no chain recorded broken"}));
    assert_eq!(log_integrity(&json!({"logs":[]}), false), json!({"state":"no chain recorded broken"}), "a package with no chained log records no break");
    // Every other shape is a limit that names what is not stated.
    for (heads, says) in [
        (json!({}), "lists no logs"),
        (json!({"logs":"none"}), "lists no logs"),
        (json!({"logs":[{"log":"runs/a/b.jsonl","chain":{"head":"x","lines":1}}]}), "runs/a/b.jsonl: the package does not state whether this chain was broken"),
        (json!({"logs":[{"log":"runs/a/b.jsonl","chain":{"broken":"no"}}]}), "does not state whether this chain was broken"),
        (json!({"logs":[{"log":"runs/a/b.jsonl","chain":{"broken":[7]}}]}), "a recorded break that is not text"),
        (json!({"logs":[{"chain":{"broken":["chain broken at line 2: x"]}}]}), "a log the tag does not name: chain broken at line 2"),
        (json!({"logs":[{"log":"role-supply/observations.jsonl","chain":{"state":"unreadable or invalid role supply chain","error":"invented"}}]}), "chain not read at export (unreadable or invalid role supply chain: invented)"),
    ] {
        let integrity = log_integrity(&heads, false);
        assert_eq!(integrity["state"], "limited", "{heads}");
        assert!(integrity["limits"][0].as_str().unwrap().contains(says), "{integrity}");
    }
    // A log the legacy profile records no head for was not checked, which is a limit.
    let legacy = log_integrity(&whole, true);
    assert_eq!(legacy["state"], "limited");
    assert!(legacy["limits"][0].as_str().unwrap().contains("role-supply/observations.jsonl: this package's legacy chain-head profile (0.1) records no head"), "{legacy}");
    // A stored member is read only in its two written forms; anything else is not stated.
    for stored in [json!({}), json!({"logIntegrity":null}), json!({"logIntegrity":{"state":"limited"}}), json!({"logIntegrity":{"state":"fine"}}), json!({"logIntegrity":"no chain recorded broken"})] {
        assert_eq!(stored_log_integrity(&stored), json!({"state":"not stated"}), "{stored}");
    }
    assert!(integrity_statement(&json!({"state":"not stated"})).unwrap().starts_with("Log integrity: NOT STATED."));
    assert!(integrity_summary(&json!({"state":"not stated"})).unwrap().starts_with("Log integrity: NOT STATED."));
    assert!(integrity_statement(&json!({"state":"no chain recorded broken"})).is_none());
}

#[test]
fn records_export_integrity_summary_keeps_every_line_number_whole_for_ordinary_run_paths() {
    // An ordinary run log's path is 140 characters. The summary a native
    // confirmation falls back to must still name each log and its whole line.
    let log = |c: &str| format!("runs/{}/{}.jsonl", c.repeat(64), "f".repeat(64));
    let limit = |c: &str, line: u64| format!("{}: chain broken at line {line}: it links to \"{}\", but the preceding line's identity is {}; never repaired", log(c), "0".repeat(64), "1".repeat(64));
    let one = integrity_summary(&json!({"state":"limited","limits":[limit("a", 2)]})).unwrap();
    assert!(one.contains("1 log chain fault(s)") && one.contains(&format!("…{}.jsonl is broken at line 2.", "f".repeat(34))), "{one}");
    let limits: Vec<String> = vec![limit("a", 2), limit("b", 1048576), limit("c", 7), limit("d", 9),
        "role-supply/observations.jsonl: chain not read at export (unreadable or invalid role supply chain: invented)".into()];
    let several = integrity_summary(&json!({"state":"limited","limits":limits})).unwrap();
    assert!(several.contains("5 log chain fault(s)"), "{several}");
    for line in ["is broken at line 2;", "is broken at line 1048576;", "is broken at line 7; and 2 more."] { assert!(several.contains(line), "{line}: {several}"); }
    assert!(!several.contains("line 9"), "only the first three are named in the summary: {several}");
    // A fault that is not a broken link keeps its log and what it is.
    let unread = integrity_summary(&json!({"state":"limited","limits":["role-supply/observations.jsonl: chain not read at export (unreadable or invalid role supply chain: invented)"]})).unwrap();
    assert!(unread.contains("role-supply/observations.jsonl: chain not read at export"), "{unread}");
    // Bounded however many logs are named, and it fits a native confirmation.
    let many: Vec<String> = (0..5000).map(|n| limit("e", n)).collect();
    let bounded = integrity_summary(&json!({"state":"limited","limits":many})).unwrap();
    assert!(bounded.chars().count() < 700 && bounded.contains("5000 log chain fault(s)") && bounded.contains("and 4997 more"), "{bounded}");
    assert!(crate::act_control::native_statement::bounded("records", bounded).is_ok());
    assert!(integrity_summary(&json!({"state":"no chain recorded broken"})).is_none());
}

#[test]
fn records_export_standalone_agrees_with_the_reader_on_every_line_the_reader_sets_aside() {
    use crate::record_lines::{fixture::next_link, is_valid_line, line_identity, link};
    let f = Fixture::new();
    let log = f.record();
    let template: Value = serde_json::from_slice(std::fs::read(&log).unwrap().split(|b| *b == b'\n').next().unwrap()).unwrap();
    // A link that names no line: only a line the reader examines breaks on it.
    let nothing = link(Some(&"0".repeat(64)));
    let entry = |n: usize, change: &dyn Fn(&mut Value)| -> Vec<u8> {
        let mut v = template.clone();
        v["recordId"] = json!(format!("rec:app:invented-{n}"));
        v["prevLine"] = nothing.clone();
        change(&mut v);
        serde_json::to_vec(&v).unwrap()
    };
    let replaced = |raw: Vec<u8>, from: &str, to: &str| String::from_utf8(raw).unwrap().replace(from, to).into_bytes();
    let push = |raw: &[u8]| { let mut bytes = std::fs::read(&log).unwrap(); bytes.extend(raw); bytes.push(b'\n'); std::fs::write(&log, bytes).unwrap(); };
    let lines = || std::fs::read(&log).unwrap().iter().filter(|b| **b == b'\n').count();
    // The App's JSON reader takes 127 levels of nesting and refuses 128; the
    // standalone verifier carries that bound (MAX_DEPTH).
    let brackets = |levels: usize| format!("{}{}", "[".repeat(levels), "]".repeat(levels));
    assert!(serde_json::from_str::<Value>(&brackets(127)).is_ok() && serde_json::from_str::<Value>(&brackets(128)).is_err());
    let mut group = template.clone();
    group.as_object_mut().unwrap().remove("prevLine");
    let member = |n: u64, id: &str| { let mut m = group.clone(); m["seq"] = json!(n); m["recordId"] = json!(id); m };
    let set_aside: Vec<Vec<u8>> = vec![
        b"{}".to_vec(),
        b"not json at all".to_vec(),
        entry(1, &|v| v["kind"] = json!("not a kind")),
        entry(2, &|v| { v.as_object_mut().unwrap().remove("body"); }),
        entry(3, &|v| v["extra"] = json!(true)),
        replaced(entry(5, &|v| v["seq"] = json!(987654321)), "987654321", "1e400"),
        replaced(entry(6, &|v| v["writtenAt"] = json!("SURROGATE")), "SURROGATE", "\\ud800"),
        serde_json::to_vec(&json!({"format":"chirality.rs.group","formatVersion":"0.1","groupId":"grp:app:invented-a","prevLine":nothing,"entries":[member(5, "rec:app:g1"), member(7, "rec:app:g2")]})).unwrap(),
        serde_json::to_vec(&json!({"format":"chirality.rs.group","formatVersion":"0.1","groupId":"grp:app:invented-b","prevLine":nothing,"entries":[member(5, "rec:app:same"), member(6, "rec:app:same")]})).unwrap(),
        // The record, its body and "detail" are three levels; 125 more make
        // 128, one past what the App's JSON reader takes.
        replaced(entry(7, &|v| v["body"]["detail"] = json!("DEEP")), "\"DEEP\"", &format!("{{\"a\":{}}}", brackets(125))),
    ];
    for raw in &set_aside {
        assert!(!is_valid_line(raw), "the reader must set this aside: {}", String::from_utf8_lossy(raw));
        push(raw);
    }
    // A whole record the reader takes, carrying that same link: its link is
    // examined, and the chain is broken there, in the store, before any export.
    let within = entry(8, &|_| {});
    assert!(is_valid_line(&within));
    push(&within);
    let broken_at = lines();
    // The App appends nothing more to a log it reads as incomplete, so the
    // lines after these are written by hand, linked as the App links them.
    let good = |n: usize| entry(n, &|v| v["prevLine"] = next_link(&log));
    push(&good(20));
    // A torn line the App closed: the next line names it exactly, and links
    // to the line before it.
    let before = next_link(&log);
    push(b"{}");
    let torn_at = lines();
    let mut limit = template.clone();
    limit["recordId"] = json!("rec:app:invented-limit");
    limit["body"] = json!({"label":crate::records::PARTIAL_NOT_RECOVERED,"subjectRef":format!("line {torn_at}; 2 bytes; sha256 {}", line_identity(b"{}"))});
    limit["prevLine"] = before;
    let limit = serde_json::to_vec(&limit).unwrap();
    assert!(is_valid_line(&limit));
    push(&limit);
    let last = good(21);
    assert!(is_valid_line(&last));
    push(&last);
    // The App exports the store as it stands and records what its reader found.
    export(&f.project, &f.bag()).unwrap();
    let dir = records_store::home(&f.project).unwrap().attachment.dir.unwrap();
    let rel = log.strip_prefix(&dir).unwrap().to_str().unwrap().to_owned();
    let app = verify(&f.bag()).unwrap();
    let limits: Vec<&str> = app["logIntegrity"]["limits"].as_array().unwrap().iter().map(|l| l.as_str().unwrap()).collect();
    assert_eq!(limits.len(), 1 + set_aside.len(), "{app}");
    assert!(limits[0].starts_with(&format!("{rel}: chain broken at line {broken_at}: it links to")), "{app}");
    for (index, line) in (2..2 + set_aside.len()).enumerate() {
        assert_eq!(limits[1 + index], format!("{rel}: line {line} was set aside by the App as invalid: it is not read as a record, and its own link is not examined"));
    }
    // The package records the reader's account of this log.
    let tag: Value = serde_json::from_slice(&std::fs::read(f.bag().join(HEADS)).unwrap()).unwrap();
    assert_eq!(tag["formatVersion"], "0.3");
    assert_eq!(tag["logs"][0]["chain"]["setAside"], json!((2..2 + set_aside.len()).collect::<Vec<_>>()));
    assert_eq!(tag["logs"][0]["chain"]["torn"], json!([torn_at]));
    // The standalone verifier reads the same lines the same way: the same one
    // break, nothing else, and the lines set aside named as not examined.
    let alone = standalone(&f.bag());
    let (stdout, stderr) = (String::from_utf8_lossy(&alone.stdout), String::from_utf8_lossy(&alone.stderr));
    assert_eq!(alone.status.code(), Some(2), "{stdout}{stderr}");
    assert!(stdout.contains(&format!("\nLog integrity: LIMITED. {} limits in 1 log.", 1 + set_aside.len())), "{stdout}");
    assert!(stdout.contains(&format!("Integrity limit: {rel}: chain broken at line {broken_at}: it links to")), "{stdout}");
    for line in 2..2 + set_aside.len() {
        assert!(stdout.contains(&format!("Integrity limit: {rel}: line {line} was set aside by the App as invalid: it is not read as a record, and its own link is not examined")), "{line}: {stdout}");
    }
    assert!(stdout.contains(&format!("Note: {rel}: line {torn_at} is a torn line the App closed and set aside after an interrupted write. It is not a limit")), "{stdout}");
    // The same store exported by a build of the earlier profile, which
    // recorded no account: the App still reports each line it sets aside,
    // and the standalone verifier, working the lines out for itself, agrees.
    reprofile_as_for_test(&f.bag(), "0.2");
    let earlier = verify(&f.bag()).unwrap();
    assert_eq!(earlier["logIntegrity"], app["logIntegrity"]);
    let alone = standalone(&f.bag());
    assert_eq!(alone.status.code(), Some(2), "{}", String::from_utf8_lossy(&alone.stderr));
    assert!(String::from_utf8_lossy(&alone.stdout).contains(&format!("\nLog integrity: LIMITED. {} limits in 1 log.", 1 + set_aside.len())));
}

#[test]
fn records_export_reads_packages_of_the_earlier_chain_head_profiles_unchanged() {
    // The tag this build writes is profile 0.3: each head carries the
    // reader's account of its log's lines.
    let f = Fixture::new();
    f.record();
    f.record();
    export(&f.project, &f.bag()).unwrap();
    let tag = |bag: &Path| -> Value { serde_json::from_slice(&std::fs::read(bag.join(HEADS)).unwrap()).unwrap() };
    let written = tag(&f.bag());
    assert_eq!(written["formatVersion"], "0.3");
    assert_eq!(written["logs"][0]["chain"]["setAside"], json!([]));
    assert_eq!(written["logs"][0]["chain"]["torn"], json!([]));
    let now = verify(&f.bag()).unwrap();
    assert!(now["chainHeadProfile"].as_str().unwrap().starts_with("0.3:"), "{now}");
    assert_eq!(now["logIntegrity"], json!({"state":"no chain recorded broken"}));
    assert_eq!(standalone(&f.bag()).status.code(), Some(0));
    // The same package as a build of each earlier profile wrote its tag: no
    // account in a head, and for 0.1 no head for a role supply log. Both
    // verifications read them, with the same result for the same records.
    for version in ["0.2", "0.1"] {
        reprofile_as_for_test(&f.bag(), version);
        let earlier = tag(&f.bag());
        assert_eq!(earlier["formatVersion"], version);
        assert!(earlier["logs"][0]["chain"].get("setAside").is_none() && earlier["logs"][0]["chain"].get("torn").is_none(), "{earlier}");
        let read = verify(&f.bag()).unwrap();
        assert!(read["chainHeadProfile"].as_str().unwrap().starts_with(&format!("{version}:")), "{read}");
        assert_eq!(read["state"], "package bytes consistent; no chain recorded broken");
        assert_eq!(read["logIntegrity"], json!({"state":"no chain recorded broken"}));
        let alone = standalone(&f.bag());
        assert_eq!(alone.status.code(), Some(0), "{version}: {}", String::from_utf8_lossy(&alone.stderr));
        // A tag of one profile presented as another is a disagreement.
        let mut forged = earlier.clone();
        forged["formatVersion"] = json!("0.3");
        std::fs::write(f.bag().join(HEADS), serde_json::to_vec_pretty(&forged).unwrap()).unwrap();
        std::fs::write(f.bag().join("tagmanifest-sha256.txt"), manifest(&f.bag(), TAGS.iter().map(|s| s.to_string())).unwrap()).unwrap();
        assert!(verify(&f.bag()).is_err_and(|e| e.contains("chain heads differ")));
        assert_eq!(standalone(&f.bag()).status.code(), Some(1), "an account that is missing fails");
    }
    assert!(Profile::of(Some("0.4")).is_err() && Profile::of(None).is_err());
}

#[test]
fn records_export_stored_log_integrity_is_read_only_in_its_two_written_forms() {
    let limited = json!({"state":"limited","limits":["runs/a.jsonl: chain broken at line 2: x"]});
    assert_eq!(stored_log_integrity(&json!({"logIntegrity":limited})), limited);
    assert_eq!(stored_log_integrity(&json!({"logIntegrity":{"state":"no chain recorded broken"}})), json!({"state":"no chain recorded broken"}));
    // Malformed or self-contradictory: not stated, never clean and never a count of nothing.
    for stored in [
        json!({"state":"no chain recorded broken","limits":["runs/a.jsonl: chain broken at line 2: x"]}),
        json!({"state":"no chain recorded broken","limits":[]}),
        json!({"state":"limited","limits":[7]}),
        json!({"state":"limited","limits":[]}),
        json!({"state":"limited","limits":[""]}),
        json!({"state":"limited","limits":["x"],"extra":true}),
        json!({"state":"limited"}),
        json!({"limits":["x"]}),
        json!("no chain recorded broken"),
        json!(null),
    ] {
        let read = stored_log_integrity(&json!({"logIntegrity":stored}));
        assert_eq!(read, json!({"state":"not stated"}), "{stored}");
        assert!(integrity_statement(&read).unwrap().starts_with("Log integrity: NOT STATED."));
    }
}

#[test]
fn records_export_integrity_summary_takes_the_line_from_the_break_and_not_from_the_logs_path() {
    // A package path may itself hold the words that introduce a break.
    let path = "runs/attacker: chain broken at line 987: /app-writer.jsonl";
    let limit = format!("{path}: chain broken at line 2: it links to \"{}\", but the preceding line's identity is {}; never repaired", "0".repeat(64), "1".repeat(64));
    let summary = integrity_summary(&json!({"state":"limited","limits":[limit]})).unwrap();
    assert!(summary.contains("/app-writer.jsonl is broken at line 2."), "{summary}");
    assert!(!summary.contains("is broken at line 987"), "{summary}");
    // A line set aside keeps its log and its line in the summary too.
    let aside = integrity_summary(&json!({"state":"limited","limits":[format!("runs/{}/{}.jsonl: line 12 was set aside by the App as invalid: it is not read as a record, and its own link is not examined", "a".repeat(64), "f".repeat(64))]})).unwrap();
    assert!(aside.contains(".jsonl: line 12 was set aside by the App as invalid"), "{aside}");
    // And there too the line is the limit's own, not one a path spells.
    let spelled = integrity_summary(&json!({"state":"limited","limits":["runs/a: line 987 was set aside/app-writer.jsonl: line 12 was set aside by the App as invalid: it is not read as a record, and its own link is not examined"]})).unwrap();
    assert!(spelled.contains("/app-writer.jsonl: line 12 was set aside by the App as invalid;") || spelled.contains("/app-writer.jsonl: line 12 was set aside by the App as invalid."), "{spelled}");
}
