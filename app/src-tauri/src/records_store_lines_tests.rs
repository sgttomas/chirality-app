// The store's own line files (the registry and a project's import account):
// an append interrupted at any point leaves every earlier line reading as it
// did; a fragment is closed with the mark, named once, and never read; a
// complete unreadable line without the mark refuses appends and is shown.
use super::*;
use super::super::lines as store_lines;

/// Which store line file a case runs on.
#[derive(Clone, Copy, Debug)]
enum Kind {
    Roots,
    Imports,
}
const KINDS: [Kind; 2] = [Kind::Roots, Kind::Imports];

/// A store with one minted project, and the file of `kind` holding one line.
struct Case {
    _store: OwnStore,
    store: PathBuf,
    root: PathBuf,
    path: PathBuf,
    kind: Kind,
}
impl Case {
    fn new(kind: Kind) -> Self {
        let own = OwnStore::new();
        let root = folder("safe-append-project-");
        let attachment = attach(&root, true).unwrap();
        let store = opened().unwrap().0;
        let path = match kind {
            Kind::Roots => store.join("roots.jsonl"),
            Kind::Imports => {
                let path = attachment.dir.unwrap().join("imports.jsonl");
                append_line(&path, &Self::value(kind, 0)).unwrap();
                path
            }
        };
        Case { _store: own, store, root, path, kind }
    }
    /// The `n`-th invented line of this kind.
    fn value(kind: Kind, n: usize) -> Value {
        match kind {
            Kind::Roots => json!({"format":ROOT_FORMAT,"formatVersion":VERSION,"projectId":format!("chirality-project:invented-{n}"),"root":format!("/invented/folder-{n}"),"at":"2026-11-12T00:00:00Z","how":"registered"}),
            Kind::Imports => json!({"format":IMPORT_FORMAT,"formatVersion":VERSION,"event":"started","importId":format!("import:invented-{n}"),"at":"2026-11-12T00:00:00Z","census":[],"storeHeld":false}),
        }
    }
    fn line(&self, n: usize) -> Value {
        Self::value(self.kind, n)
    }
    fn bytes(&self) -> Vec<u8> {
        std::fs::read(&self.path).unwrap()
    }
    fn read(&self) -> store_lines::Read {
        store_lines::read(&self.bytes(), &self.path)
    }
    fn append(&self, n: usize) -> Result<(), String> {
        append_line(&self.path, &self.line(n))
    }
    fn append_stopped(&self, n: usize, stop: AppendStop) -> String {
        interrupt_append_for_test(Some(stop));
        let result = self.append(n);
        interrupt_append_for_test(None);
        result.unwrap_err()
    }
    fn put(&self, bytes: &[u8]) {
        std::fs::write(&self.path, bytes).unwrap();
        *ROOTS.lock().unwrap() = None;
    }
}
fn serialized(v: &Value) -> Vec<u8> {
    serde_json::to_vec(v).unwrap()
}
/// The one write an append of `value` makes to `bytes` now (recovery, then the line).
fn append_bytes(bytes: &[u8], path: &Path, value: &Value) -> Vec<u8> {
    let mut out = store_lines::read(bytes, path).recovery().unwrap();
    out.extend(serialized(value));
    out.push(b'\n');
    out
}
/// The file is whole, has no fragment left to close or name, names no line
/// twice, and reads exactly `values`; every line it could not read is set
/// aside by exactly one naming line that names its exact length and digest.
fn settled(read: &store_lines::Read, values: &[Value], bytes: &[u8]) {
    assert!(read.whole, "{:?}", read.limits);
    assert!(read.tail.is_none() && read.unnamed_closures.is_empty(), "{:?}", read.limits);
    assert_eq!(read.values, values, "only the lines appended whole are read");
    assert!(read.limits.is_empty(), "no naming line names twice or names other bytes: {:?}", read.limits);
    let lines: Vec<&[u8]> = bytes[..bytes.len() - 1].split(|b| *b == b'\n').collect();
    for (i, line) in lines.iter().enumerate() {
        if serde_json::from_slice::<Value>(line).is_ok() {
            continue;
        }
        assert!(read.set_aside.contains(&(i + 1)), "line {} is set aside", i + 1);
        assert!(store_lines::is_closed(line), "a set-aside line here is a closed fragment");
        let namers: Vec<Value> = lines.iter().filter_map(|l| serde_json::from_slice::<Value>(l).ok())
            .filter(|v| v["format"] == store_lines::UNREAD_FORMAT && v["line"] == i + 1).collect();
        assert_eq!(namers.len(), 1, "line {} named once", i + 1);
        assert_eq!(namers[0]["length"], line.len());
        assert_eq!(namers[0]["sha256"], crate::util::sha256_hex(line));
        assert_eq!(namers[0]["by"], "writer");
    }
}

// ---- Interruption points of the appender ----

#[test]
fn a_new_file_stopped_before_it_is_put_in_place_leaves_no_file_and_is_made_whole_next() {
    for kind in KINDS {
        let own = OwnStore::new();
        let root = folder("safe-append-new-");
        let dir = attach(&root, true).unwrap().dir.unwrap();
        let store = opened().unwrap().0;
        let path = match kind { Kind::Roots => store.join("roots-new-test.jsonl"), Kind::Imports => dir.join("imports.jsonl") };
        interrupt_append_for_test(Some(AppendStop::BeforeWrite));
        assert!(append_line(&path, &Case::value(kind, 1)).unwrap_err().contains("interrupted"));
        interrupt_append_for_test(None);
        assert!(std::fs::symlink_metadata(&path).is_err(), "{kind:?}: no file, not even an empty one");
        let strays: Vec<_> = std::fs::read_dir(path.parent().unwrap()).unwrap().filter_map(|e| e.ok()).filter(|e| e.file_name().to_string_lossy().ends_with(".tmp")).collect();
        assert!(strays.is_empty(), "{kind:?}: the temporary file is removed");
        append_line(&path, &Case::value(kind, 1)).unwrap();
        let mut expected = serialized(&Case::value(kind, 1));
        expected.push(b'\n');
        assert_eq!(std::fs::read(&path).unwrap(), expected, "{kind:?}: the first line, whole");
        drop(own);
    }
}

#[test]
fn an_existing_file_stopped_before_the_write_is_unchanged() {
    for kind in KINDS {
        let c = Case::new(kind);
        let before = c.bytes();
        c.append_stopped(1, AppendStop::BeforeWrite);
        assert_eq!(c.bytes(), before, "{kind:?}");
    }
}

#[test]
fn a_write_stopped_midway_leaves_a_fragment_never_read_and_closed_and_named_once() {
    for kind in KINDS {
        for startup in [false, true] {
            let c = Case::new(kind);
            let first = c.read().values;
            let whole = c.bytes();
            let write = append_bytes(&whole, &c.path, &c.line(1));
            c.append_stopped(1, AppendStop::AfterBytes(write.len() / 2));
            let torn = c.read();
            assert_eq!(torn.values, first, "{kind:?}: the fragment is not read");
            assert!(torn.whole && torn.tail.is_some());
            if startup {
                recover_at_startup().unwrap();
            } else {
                c.append(2).unwrap();
            }
            let after = c.bytes();
            assert!(after.starts_with(&c.bytes()[..whole.len()]) && after.starts_with(&whole), "{kind:?}: earlier bytes kept");
            let mut values = first.clone();
            if !startup {
                values.push(c.line(2));
            }
            settled(&c.read(), &values, &after);
            // Again: nothing more is named.
            recover_at_startup().unwrap();
            assert_eq!(c.bytes(), after, "{kind:?}: not named twice");
        }
    }
}

#[test]
fn a_write_stopped_before_its_sync_is_a_complete_line_that_reads() {
    for kind in KINDS {
        let c = Case::new(kind);
        let mut values = c.read().values;
        c.append_stopped(1, AppendStop::BeforeSync);
        values.push(c.line(1));
        settled(&c.read(), &values, &c.bytes());
    }
}

/// Every prefix of the closure write: (a) nothing, (b) the mark alone, (c) the
/// mark and the newline, (d) part of the naming line, (e) the whole naming
/// line without its newline. After the next startup and after the next
/// append the file reads the same, no line is named twice, and no line comes
/// into force.
#[test]
fn every_prefix_of_a_cut_closure_recovers_at_startup_and_at_the_next_append() {
    for kind in KINDS {
        let mut ends: Vec<(String, Vec<Vec<u8>>)> = Vec::new();
        for (label, prefix) in ["a nothing", "b mark", "c mark and newline", "d part of naming line", "e naming line without newline"].iter().zip(0..5) {
            let mut set_aside_by_route = Vec::new();
            for startup in [true, false] {
                let c = Case::new(kind);
                let first = c.read().values;
                // A fragment: a cut-short line that is whole JSON but for its newline.
                let mut torn = c.bytes();
                torn.extend(serialized(&c.line(9)));
                c.put(&torn);
                let recovery = c.read().recovery().unwrap();
                assert_eq!(recovery[0], store_lines::MARK);
                assert_eq!(recovery[1], b'\n');
                let naming = recovery.len() - 2;
                let cut = match prefix { 0 => 0, 1 => 1, 2 => 2, 3 => 2 + naming / 2, _ => 2 + naming - 1 };
                c.append_stopped(1, AppendStop::AfterBytes(cut));
                assert_eq!(c.bytes().len(), torn.len() + cut, "{label}");
                let cut_read = c.read();
                assert_eq!(cut_read.values, first, "{kind:?} {label}: nothing cut short is read");
                assert!(cut_read.whole, "{kind:?} {label}: {:?}", cut_read.limits);
                let before = c.bytes();
                if startup {
                    recover_at_startup().unwrap();
                } else {
                    c.append(2).unwrap();
                }
                let after = c.bytes();
                assert!(after.starts_with(&before), "{kind:?} {label}: earlier bytes kept");
                let mut values = first.clone();
                if !startup {
                    values.push(c.line(2));
                }
                let read = c.read();
                settled(&read, &values, &after);
                assert!(!read.values.contains(&c.line(9)), "{kind:?} {label}: the whole-JSON fragment never comes into force");
                // The next startup and the next append name nothing more.
                recover_at_startup().unwrap();
                assert_eq!(c.bytes(), after, "{kind:?} {label}: not named twice");
                c.append(3).unwrap();
                let mut values = values.clone();
                values.push(c.line(3));
                settled(&c.read(), &values, &c.bytes());
                let lines: Vec<Vec<u8>> = after.split(|b| *b == b'\n').map(<[u8]>::to_vec).collect();
                set_aside_by_route.push(read.set_aside.iter().map(|n| lines[n - 1].clone()).collect::<Vec<_>>());
            }
            // The same lines set aside by both routes: the fragment byte for
            // byte; a cut naming line by its length (it holds its own time).
            let (s, a) = (&set_aside_by_route[0], &set_aside_by_route[1]);
            assert_eq!(s.len(), a.len(), "{kind:?} {label}");
            assert_eq!(s[0], a[0], "{kind:?} {label}: the same fragment set aside by startup and by the next append");
            assert!(s.iter().zip(a).all(|(x, y)| x.len() == y.len()), "{kind:?} {label}");
            ends.push((label.to_string(), set_aside_by_route.remove(0)));
        }
        // (a) and (b) leave one closed line; (c) one; (d) and (e) two (the cut naming line too).
        let counts: Vec<usize> = ends.iter().map(|(_, s)| s.len()).collect();
        assert_eq!(counts, vec![1, 1, 1, 2, 2], "{kind:?}: {ends:?}");
    }
}

#[test]
fn two_fragments_in_succession_are_each_named_once() {
    for kind in KINDS {
        let c = Case::new(kind);
        let first = c.read().values;
        let write = append_bytes(&c.bytes(), &c.path, &c.line(1));
        c.append_stopped(1, AppendStop::AfterBytes(write.len() - 3));
        // The second append closes the first fragment, then is itself cut inside its own line.
        let write = append_bytes(&c.bytes(), &c.path, &c.line(2));
        c.append_stopped(2, AppendStop::AfterBytes(write.len() - 3));
        let read = c.read();
        assert_eq!(read.values, first, "{kind:?}");
        c.append(3).unwrap();
        let mut values = first.clone();
        values.push(c.line(3));
        let read = c.read();
        settled(&read, &values, &c.bytes());
        assert_eq!(read.set_aside.len(), 2, "{kind:?}");
    }
}

#[test]
fn a_line_that_was_whole_json_and_lost_only_its_newline_never_comes_into_force() {
    // The registry: a release cut before its newline does not release; a
    // registration cut before its newline does not register.
    let c = Case::new(Kind::Roots);
    let at = c.root.to_str().unwrap().to_owned();
    let project = attach(&c.root, false).unwrap().project.unwrap();
    let release = json!({"format":ROOT_FORMAT,"formatVersion":VERSION,"projectId":project,"root":at,"at":"2026-11-12T00:00:00Z","how":"released"});
    let other = folder("safe-append-other-");
    let registration = json!({"format":ROOT_FORMAT,"formatVersion":VERSION,"projectId":"chirality-project:invented","root":other.to_str().unwrap(),"at":"2026-11-12T00:00:00Z","how":"registered"});
    for torn in [release, registration] {
        let whole = c.bytes();
        let mut bytes = whole.clone();
        bytes.extend(serialized(&torn));
        c.put(&bytes);
        assert_eq!(listed(&roots(&c.store).unwrap(), &at), vec![project.clone()], "before closing");
        assert!(listed(&roots(&c.store).unwrap(), other.to_str().unwrap()).is_empty());
        recover_at_startup().unwrap();
        *ROOTS.lock().unwrap() = None;
        let rows = roots(&c.store).unwrap();
        assert_eq!(listed(&rows, &at), vec![project.clone()], "the release does not come into force when closed");
        assert!(listed(&rows, other.to_str().unwrap()).is_empty(), "the registration does not come into force when closed");
        assert_eq!(attach(&c.root, false).unwrap().project.as_deref(), Some(project.as_str()));
    }
    // The import account: a completed line cut before its newline completes nothing.
    let c = Case::new(Kind::Imports);
    let mut bytes = c.bytes();
    bytes.extend(serialized(&json!({"format":IMPORT_FORMAT,"formatVersion":VERSION,"event":"completed","importId":"import:invented-0","at":"2026-11-12T00:00:00Z","files":[],"conflicts":[],"censusChanged":[]})));
    c.put(&bytes);
    let dir = c.path.parent().unwrap();
    assert!(!imports(dir).unwrap().completed && imports(dir).unwrap().incomplete.is_some());
    recover_at_startup().unwrap();
    assert!(!imports(dir).unwrap().completed, "the completion does not come into force when closed");
    assert!(imports(dir).unwrap().incomplete.is_some());
}

// ---- The shared reading ----

#[test]
fn a_hand_written_line_ending_in_the_mark_is_named_by_the_writer_and_never_read() {
    // The one thing the mark lets someone outside the App cause.
    for kind in KINDS {
        let c = Case::new(kind);
        let first = c.read().values;
        let mut hand = serialized(&c.line(7));
        hand.push(store_lines::MARK);
        let mut bytes = c.bytes();
        let number = bytes.iter().filter(|b| **b == b'\n').count() + 1;
        bytes.extend(&hand);
        bytes.push(b'\n');
        bytes.extend(serialized(&c.line(8)));
        bytes.push(b'\n');
        c.put(&bytes);
        let read = c.read();
        let mut values = first.clone();
        values.push(c.line(8));
        assert!(read.whole, "{kind:?}");
        assert_eq!(read.values, values, "{kind:?}: never read");
        assert_eq!(read.unnamed_closures, vec![(number, hand.clone())]);
        recover_at_startup().unwrap();
        let after = c.bytes();
        assert!(after.starts_with(&bytes), "{kind:?}: its bytes kept");
        let read = c.read();
        settled(&read, &values, &after);
        assert_eq!(read.set_aside, vec![number]);
    }
}

#[test]
fn a_complete_unreadable_line_without_the_mark_refuses_appends_changes_nothing_and_is_shown() {
    for kind in KINDS {
        let c = Case::new(kind);
        let first = c.read().values;
        let mut bytes = c.bytes();
        bytes.extend(b"{\"damaged from outside\n");
        bytes.extend(serialized(&c.line(3)));
        bytes.push(b'\n');
        c.put(&bytes);
        let read = c.read();
        assert!(!read.whole, "{kind:?}");
        let mut values = first.clone();
        values.push(c.line(3));
        assert_eq!(read.values, values, "{kind:?}: reading continues from the other lines");
        assert!(read.limits.iter().any(|l| l.contains("cannot be read and is not named")), "{:?}", read.limits);
        let refused = c.append(4).unwrap_err();
        assert!(refused.contains("not read whole") && refused.contains("bytes are kept") && refused.contains("nothing in it changed"), "{refused}");
        assert_eq!(c.bytes(), bytes, "{kind:?}: nothing written");
        let left = recover_at_startup().unwrap();
        assert!(left.iter().any(|l| l.contains("not read whole")), "{left:?}");
        assert_eq!(c.bytes(), bytes, "{kind:?}: no repair at startup");
        match kind {
            Kind::Roots => {
                assert!(roots(&c.store).unwrap_err().contains("not read whole"));
                let attachment = attach(&c.root, false).unwrap();
                assert!(attachment.project.is_some(), "the folder's own line still reads");
                assert!(attachment.limits.iter().any(|l| l.contains("cannot be read")), "shown: {:?}", attachment.limits);
                let other = folder("safe-append-refused-");
                assert!(attach(&other, true).unwrap_err().contains("not read whole"), "a registration is refused");
                assert_eq!(c.bytes(), bytes);
            }
            Kind::Imports => {
                let dir = c.path.parent().unwrap();
                assert!(imports(dir).err().unwrap().contains("not read whole"));
                assert!(write_dir(&c.root).unwrap_err().contains("not read whole"), "writes for the project are refused, never routed on a partial account");
            }
        }
    }
}

/// Review round 1, finding 3. Only a line that ends in the mark is ever set
/// aside, and only by a naming line in the one form the App writes. A naming
/// line written for a complete unreadable line WITHOUT the mark sets nothing
/// aside: the file is not read whole, as if the naming line were not there.
/// A naming line of another version, or with other members, names nothing.
#[test]
fn a_naming_line_for_a_line_without_the_mark_or_in_another_form_sets_nothing_aside() {
    for kind in KINDS {
        let c = Case::new(kind);
        let original = c.bytes();
        let first = c.read().values;
        let [unmarked, other_version] = store_lines::naming_inputs_that_set_nothing_aside(&original);
        // A naming line with a member the App does not write, for a closed fragment.
        let line = original.iter().filter(|b| **b == b'\n').count() + 1;
        let mut closed = b"{\"cut".to_vec();
        closed.push(store_lines::MARK);
        let named = store_lines::naming_line(line, &closed).unwrap();
        let mut naming: Value = serde_json::from_slice(&named[..named.len() - 1]).unwrap();
        naming["extra"] = json!(true);
        let mut extra_member = closed.clone();
        extra_member.push(b'\n');
        extra_member.extend(serialized(&naming));
        extra_member.push(b'\n');
        for (case, input, limit, awaiting) in [
            ("unmarked", unmarked, "does not end in the closure mark", 0),
            ("another version", other_version, "in a form this App does not write", 1),
            ("another member", extra_member, "in a form this App does not write", 1),
        ] {
            let mut bytes = original.clone();
            bytes.extend(&input);
            c.put(&bytes);
            let read = c.read();
            assert!(!read.whole, "{kind:?} {case}: not read whole");
            assert!(read.set_aside.is_empty(), "{kind:?} {case}: nothing is set aside");
            assert_eq!(read.values, first, "{kind:?} {case}: reading continues from the other lines");
            assert!(read.limits.iter().any(|l| l.contains(limit)), "{kind:?} {case}: {:?}", read.limits);
            assert_eq!(read.unnamed_closures.len(), awaiting, "{kind:?} {case}");
            if case == "unmarked" {
                assert!(read.limits.iter().any(|l| l.contains("cannot be read and is not named")), "{:?}", read.limits);
            }
            assert!(read.require_settled(&bytes, &c.path).is_err(), "{kind:?} {case}: a strict reader refuses");
            let refused = c.append(9).unwrap_err();
            assert!(refused.contains("not read whole") && refused.contains("nothing in it changed"), "{kind:?} {case}: {refused}");
            let left = recover_at_startup().unwrap();
            assert!(left.iter().any(|l| l.contains("not read whole")), "{kind:?} {case}: {left:?}");
            assert_eq!(c.bytes(), bytes, "{kind:?} {case}: nothing written, at an append or at startup");
        }
    }
}

#[test]
fn a_naming_line_that_names_a_readable_line_or_other_bytes_sets_nothing_aside() {
    for kind in KINDS {
        let c = Case::new(kind);
        let mut bytes = c.bytes();
        let first_line = bytes[..bytes.len() - 1].to_vec();
        // Names line 1, which can be read.
        bytes.extend(store_lines::naming_line(1, &first_line).unwrap());
        // A closed fragment, then a naming line with the wrong digest.
        let mut closed = b"{\"cut".to_vec();
        closed.push(store_lines::MARK);
        bytes.extend(&closed);
        bytes.push(b'\n');
        let mut wrong = store_lines::naming_line(3, b"other bytes").unwrap();
        let mut v: Value = serde_json::from_slice(&wrong[..wrong.len() - 1]).unwrap();
        v["length"] = json!(closed.len());
        wrong = serialized(&v);
        wrong.push(b'\n');
        bytes.extend(&wrong);
        c.put(&bytes);
        let read = c.read();
        assert_eq!(read.values.len(), c.read().values.len());
        assert_eq!(read.values[0], serde_json::from_slice::<Value>(&first_line).unwrap(), "{kind:?}: the readable line is still read");
        assert!(read.set_aside.is_empty(), "{kind:?}");
        assert!(read.limits.iter().any(|l| l.contains("names line 1, which can be read")), "{:?}", read.limits);
        assert!(read.limits.iter().any(|l| l.contains("names bytes that are not")), "{:?}", read.limits);
        assert_eq!(read.unnamed_closures.len(), 1, "the closed fragment still awaits its name");
        // The writer names the closed fragment; the two naming lines stay limits.
        recover_at_startup().unwrap();
        let read = c.read();
        assert_eq!(read.set_aside, vec![3], "{kind:?}");
        assert!(read.unnamed_closures.is_empty());
    }
}

#[test]
fn every_reader_ignores_naming_lines_and_sets_named_lines_aside() {
    // records_store: roots / roots_read / attach / listed, parse_lines and
    // imports / status; the package import's frozen-prefix readers go through
    // parse_lines and roots (records_package_import_tests).
    let c = Case::new(Kind::Roots);
    let project = attach(&c.root, false).unwrap().project.unwrap();
    let at = c.root.to_str().unwrap().to_owned();
    let mut bytes = c.bytes();
    bytes.extend(b"{\"format\":\"chirality.records-store.root\",\"how\":\"rel");
    c.put(&bytes);
    recover_at_startup().unwrap();
    *ROOTS.lock().unwrap() = None;
    let rows = roots(&c.store).unwrap();
    assert!(rows.iter().all(|r| r["format"] == ROOT_FORMAT), "no naming line is read as a registry row");
    assert_eq!(listed(&rows, &at), vec![project.clone()]);
    assert_eq!(parse_lines(&c.bytes(), &c.path).unwrap(), rows);
    let attachment = attach(&c.root, false).unwrap();
    assert_eq!(attachment.project.as_deref(), Some(project.as_str()));
    assert!(attachment.limits.is_empty(), "{:?}", attachment.limits);
    // A further registration, adoption and new identity append after it.
    let other = folder("safe-append-after-");
    assert_eq!(attach(&other, true).unwrap().how, "minted");
    // The import account through imports() and status.
    let c = Case::new(Kind::Imports);
    let dir = c.path.parent().unwrap().to_path_buf();
    let mut bytes = c.bytes();
    bytes.extend(b"{\"format\":\"chirality.records-store.import\",\"event\":\"comp");
    c.put(&bytes);
    recover_at_startup().unwrap();
    let state = imports(&dir).unwrap();
    assert!(state.any && !state.completed && state.incomplete.is_some());
    assert_eq!(status(Some(&c.root))["project"]["imports"], 1, "the naming line and the closed fragment are not counted as import lines");
}

// ---- The ground of the mark ----

#[test]
fn no_writer_of_these_files_emits_a_raw_record_separator() {
    // serde_json escapes every control character it writes in a string.
    let all: String = (0u8..0x20).map(char::from).collect();
    let bytes = serialized(&json!({"root":all,"copy":"a\u{1e}b"}));
    assert!(!bytes.contains(&store_lines::MARK), "{}", String::from_utf8_lossy(&bytes));
    // The appender, through the registry: a folder whose name holds 0x1E.
    let own = OwnStore::new();
    let parent = folder("safe-append-mark-");
    let root = parent.join("folder\u{1e}name");
    std::fs::create_dir_all(&root).unwrap();
    let attachment = attach(&root, true).unwrap();
    let store = opened().unwrap().0;
    let registry = std::fs::read(store.join("roots.jsonl")).unwrap();
    assert!(!registry.contains(&store_lines::MARK));
    assert_eq!(listed(&roots(&store).unwrap(), root.to_str().unwrap()), vec![attachment.project.clone().unwrap()]);
    // The closure: one mark, first, and none in its naming line.
    let recovery = store_lines::read(b"{\"cut", Path::new("x.jsonl")).recovery().unwrap();
    assert_eq!(recovery.iter().filter(|b| **b == store_lines::MARK).count(), 1);
    assert_eq!(recovery[0], store_lines::MARK);
    assert!(!store_lines::naming_line(1, &[store_lines::MARK; 4]).unwrap().contains(&store_lines::MARK));
    drop(own);
}
