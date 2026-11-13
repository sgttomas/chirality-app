// The store's witness of legacy imports: written before any copy, outside the
// project's account, read apart from it; begun once with its backfill; a
// project that predates it with no account is "not established".
use super::*;
use super::super::lines as store_lines;
use super::super::witness::{self, LegacyOrigin, WitnessedFile};

/// A §13.7 project, attached in a fresh store of this thread's own.
struct Legacy {
    _store: OwnStore,
    store: PathBuf,
    root: PathBuf,
    project: String,
    dir: PathBuf,
}
impl Legacy {
    fn new() -> Self {
        let own = OwnStore::new();
        let root = legacy_project();
        let attachment = attach(&root, true).unwrap();
        let store = opened().unwrap().0;
        Legacy { _store: own, store, root, project: attachment.project.unwrap(), dir: attachment.dir.unwrap() }
    }
    fn origin(&self) -> Result<LegacyOrigin, String> {
        legacy_import_origin(&self.store, &self.project)
    }
    fn witness(&self) -> Vec<u8> {
        std::fs::read(self.store.join(witness::WITNESS_FILE)).unwrap_or_default()
    }
    /// The copies an import of this project places, by its census.
    fn copies(&self) -> Vec<String> {
        legacy_census(&self.root).unwrap().into_iter().filter(|f| f.refusal.is_none()).map(|f| f.copy).collect()
    }
    /// Each copy present in the subtree, with its length and digest.
    fn present(&self) -> Vec<WitnessedFile> {
        self.copies().into_iter().filter_map(|copy| {
            let bytes = std::fs::read(self.dir.join(&copy)).ok()?;
            Some(WitnessedFile { copy, length: bytes.len() as u64, sha256: crate::util::sha256_hex(&bytes) })
        }).collect()
    }
}
fn key_of(dir: &Path) -> String {
    dir.file_name().unwrap().to_str().unwrap().to_owned()
}
fn set_created(dir: &Path, at: &str) {
    let record = dir.join("project.json");
    let mut identity: Value = serde_json::from_slice(&std::fs::read(&record).unwrap()).unwrap();
    identity["createdAt"] = json!(at);
    std::fs::write(&record, serde_json::to_vec(&identity).unwrap()).unwrap();
}
fn imported_files(origin: &LegacyOrigin) -> Vec<WitnessedFile> {
    match origin {
        LegacyOrigin::Imported(imports) => imports.iter().flat_map(|i| i.files.clone()).collect(),
        _ => vec![],
    }
}
fn bases(origin: &LegacyOrigin) -> Vec<String> {
    match origin {
        LegacyOrigin::Imported(imports) => imports.iter().map(|i| i.basis.clone()).collect(),
        _ => vec![],
    }
}

#[test]
fn the_witness_exists_before_the_first_copied_byte_at_every_interruption_point_of_an_import() {
    // Store line writes of an import: 0 its witness line, 1 its "started"
    // line, 2 its "completed" line; and stops between copies.
    let stops: Vec<(String, Box<dyn Fn()>)> = vec![
        ("witness line not written".into(), Box::new(|| interrupt_append_after_for_test(0, Some(AppendStop::BeforeWrite)))),
        ("witness line cut short".into(), Box::new(|| interrupt_append_after_for_test(0, Some(AppendStop::AfterBytes(40))))),
        ("witness line not synced".into(), Box::new(|| interrupt_append_after_for_test(0, Some(AppendStop::BeforeSync)))),
        ("started line not written".into(), Box::new(|| interrupt_append_after_for_test(1, Some(AppendStop::BeforeWrite)))),
        ("started line cut short".into(), Box::new(|| interrupt_append_after_for_test(1, Some(AppendStop::AfterBytes(40))))),
        ("before the first copy".into(), Box::new(|| interrupt_import_for_test(Some(0), false))),
        ("after the first copy".into(), Box::new(|| interrupt_import_for_test(Some(1), false))),
        ("completed line not written".into(), Box::new(|| interrupt_append_after_for_test(2, Some(AppendStop::BeforeWrite)))),
        ("completed line cut short".into(), Box::new(|| interrupt_append_after_for_test(2, Some(AppendStop::AfterBytes(40))))),
    ];
    for (label, stop) in stops {
        let l = Legacy::new();
        assert_eq!(l.origin().unwrap(), LegacyOrigin::NoImport, "{label}: before any import");
        stop();
        let result = import(&l.root);
        interrupt_append_for_test(None);
        interrupt_import_for_test(None, false);
        assert!(result.is_err(), "{label}: interrupted");
        let present = l.present();
        let origin = l.origin().unwrap();
        let witnessed = imported_files(&origin);
        for file in &present {
            assert!(witnessed.contains(file), "{label}: imported bytes {} without their witness: {origin:?}", file.copy);
        }
        if present.is_empty() && label.starts_with("witness line") && !label.ends_with("synced") {
            assert_eq!(origin, LegacyOrigin::NoImport, "{label}: no copy and no witness: no import");
        }
        // The import, run again after the App's next start (whose recovery
        // closes and names a fragment the interruption left in the account,
        // which is unknown until then), completes; the witness still holds
        // every copy.
        recover_at_startup().unwrap();
        import(&l.root).unwrap();
        let witnessed = imported_files(&l.origin().unwrap());
        for file in l.present() {
            assert!(witnessed.contains(&file), "{label}: {} witnessed after the import completes", file.copy);
        }
    }
}

#[test]
fn an_account_removed_emptied_or_stripped_is_told_apart_from_no_import_by_the_witness() {
    for change in ["removed", "emptied", "stripped"] {
        let l = Legacy::new();
        import(&l.root).unwrap();
        let files = l.present();
        assert!(!files.is_empty());
        let account = l.dir.join("imports.jsonl");
        match change {
            "removed" => std::fs::remove_file(&account).unwrap(),
            "emptied" => std::fs::write(&account, b"").unwrap(),
            _ => {
                // Every line of the import taken out; an invented other import's started line left.
                let other = json!({"format":IMPORT_FORMAT,"formatVersion":VERSION,"event":"started","importId":"import:invented-other","at":"2026-11-12T00:00:00.000Z","census":[],"storeHeld":false});
                let mut bytes = serde_json::to_vec(&other).unwrap();
                bytes.push(b'\n');
                std::fs::write(&account, bytes).unwrap();
            }
        }
        let origin = l.origin().unwrap();
        assert_eq!(bases(&origin)[0], witness::BEFORE_COPIES, "{change}: {origin:?}");
        let witnessed = imported_files(&origin);
        for file in &files {
            assert!(witnessed.contains(file), "{change}: {}", file.copy);
        }
    }
}

#[test]
fn a_store_from_before_the_witness_is_backfilled_once_and_only_once() {
    let l = Legacy::new();
    import(&l.root).unwrap();
    let files = l.present();
    // The store as it was before the witness existed.
    std::fs::remove_file(l.store.join(witness::WITNESS_FILE)).unwrap();
    assert!(matches!(l.origin().unwrap(), LegacyOrigin::Imported(_)), "the account alone, until the witness begins");
    recover_at_startup().unwrap();
    let first = l.witness();
    let read = store_lines::read(&first, &l.store.join(witness::WITNESS_FILE));
    assert_eq!(read.values.len(), 2, "the first line and one backfilled import");
    assert_eq!(read.values[0]["storeExisted"], true);
    assert_eq!(read.values[1]["basis"], witness::FROM_ACCOUNT);
    assert_eq!(read.values[1]["projectId"], l.project.as_str());
    // Again at the next startup, and at a registration: nothing more.
    recover_at_startup().unwrap();
    attach(&folder("witness-later-"), true).unwrap();
    assert_eq!(l.witness(), first, "backfilled once and only once");
    // The account then lost: the backfilled line still shows the import.
    std::fs::remove_file(l.dir.join("imports.jsonl")).unwrap();
    let origin = l.origin().unwrap();
    assert_eq!(bases(&origin), vec![witness::FROM_ACCOUNT.to_string()]);
    let witnessed = imported_files(&origin);
    for file in &files {
        assert!(witnessed.contains(file), "{}", file.copy);
    }
}

#[test]
fn a_project_from_before_the_witness_with_no_account_reads_not_established_and_a_later_one_no_import() {
    let l = Legacy::new();
    // The store as it was before the witness existed: this project predates it.
    std::fs::remove_file(l.store.join(witness::WITNESS_FILE)).unwrap();
    assert!(matches!(l.origin().unwrap(), LegacyOrigin::NotEstablished(_)), "the witness has not begun");
    recover_at_startup().unwrap();
    match l.origin().unwrap() {
        LegacyOrigin::NotEstablished(reason) => {
            assert!(reason.contains("was present in the store when the store's witness of legacy imports began") && reason.contains("absent"), "{reason}");
            assert!(reason.contains("whether it holds imported records cannot be known") && reason.contains("This does not change."), "{reason}");
            for instruction in ["repair", "restore", "import them", "run ", "fix"] {
                assert!(!reason.to_lowercase().contains(instruction), "no instruction to repair: {reason}");
            }
        }
        other => panic!("never \"no import\" for a project that predates the witness: {other:?}"),
    }
    // A project created after the witness began, with no import: no import.
    let later = attach(&folder("witness-later-project-"), true).unwrap();
    assert_eq!(legacy_import_origin(&l.store, later.project.as_deref().unwrap()).unwrap(), LegacyOrigin::NoImport);
}

#[test]
fn a_witness_not_read_whole_is_an_error_and_refuses_an_import_before_any_copy() {
    let l = Legacy::new();
    let path = l.store.join(witness::WITNESS_FILE);
    let mut bytes = l.witness();
    bytes.extend(b"{\"damaged from outside\n");
    std::fs::write(&path, &bytes).unwrap();
    assert!(l.origin().unwrap_err().contains("not read whole"), "never \"no import\"");
    assert!(import(&l.root).unwrap_err().contains("not read whole"));
    assert!(l.present().is_empty(), "nothing copied");
    assert_eq!(std::fs::read(&path).unwrap(), bytes);
}

#[test]
fn the_witness_writer_emits_no_raw_record_separator() {
    let l = Legacy::new();
    // A run log whose folder name holds 0x1E.
    let from = l.root.join(".chirality/records").join(storage::log_rel(Some("run:legacy"), "writer:legacy"));
    let to = l.root.join(".chirality/records/runs/name\u{1e}held/w.jsonl");
    std::fs::create_dir_all(to.parent().unwrap()).unwrap();
    std::fs::copy(&from, &to).unwrap();
    import(&l.root).unwrap();
    let witness = l.witness();
    assert!(!witness.contains(&store_lines::MARK));
    assert!(imported_files(&l.origin().unwrap()).iter().any(|f| f.copy.contains('\u{1e}')));
    let account = std::fs::read(l.dir.join("imports.jsonl")).unwrap();
    assert!(!account.contains(&store_lines::MARK), "nor the account's lines");
}

#[test]
fn a_project_registered_in_the_same_startup_that_begins_the_witness_is_known_to_be_created_after_it() {
    let l = Legacy::new();
    // A store from before the witness: its registry exists, its witness does not.
    std::fs::remove_file(l.store.join(witness::WITNESS_FILE)).unwrap();
    // As the App's startup does: the project folder is attached (minted)
    // first, then the startup recovery runs.
    let fresh = attach(&folder("witness-startup-project-"), true).unwrap();
    recover_at_startup().unwrap();
    let path = l.store.join(witness::WITNESS_FILE);
    let read = store_lines::read(&std::fs::read(&path).unwrap(), &path);
    let first = &read.values[0];
    assert_eq!(first["format"], "chirality.records-store.legacy-imports-began");
    assert_eq!(first["formatVersion"], "0.1");
    assert_eq!(first["storeExisted"], true);
    assert_eq!(first["by"], "writer");
    // The witness began before the new project's folder and registry line
    // existed: the list names the earlier project and not the new one.
    assert_eq!(first["projectsPresent"], json!([key_of(&l.dir)]));
    assert_ne!(key_of(fresh.dir.as_ref().unwrap()), key_of(&l.dir));
    assert_eq!(legacy_import_origin(&l.store, fresh.project.as_deref().unwrap()).unwrap(), LegacyOrigin::NoImport);
}

#[test]
fn a_line_established_when_the_witness_began_keeps_its_mark_apart_from_a_line_written_before_the_copies() {
    let l = Legacy::new();
    import(&l.root).unwrap();
    std::fs::remove_file(l.store.join(witness::WITNESS_FILE)).unwrap();
    recover_at_startup().unwrap();
    // A later record file, then a second import: its line is written before its copies.
    let later = l.root.join(".chirality/records").join(crate::storage::log_rel(Some("run:later"), "writer:later"));
    records::append(&later, "evidence_limit", &APP_WRITER, body("later legacy entry")).unwrap();
    import(&l.root).unwrap();
    assert_ne!(witness::FROM_ACCOUNT, witness::BEFORE_COPIES);
    // Through the shared reading, the stored member is unchanged.
    let path = l.store.join(witness::WITNESS_FILE);
    let read = store_lines::read(&std::fs::read(&path).unwrap(), &path);
    let stored: Vec<&Value> = read.values.iter().map(|v| &v["basis"]).collect();
    assert_eq!(stored, vec![&Value::Null, &json!(witness::FROM_ACCOUNT), &json!(witness::BEFORE_COPIES)]);
    // And the reader returns each with its own basis, never merged.
    assert_eq!(bases(&l.origin().unwrap()), vec![witness::FROM_ACCOUNT.to_string(), witness::BEFORE_COPIES.to_string()]);
}

#[test]
fn a_store_created_by_this_build_has_the_witness_from_its_first_line() {
    let own = OwnStore::new();
    let root = folder("witness-fresh-project-");
    let attachment = attach(&root, true).unwrap();
    let store = opened().unwrap().0;
    let path = store.join(witness::WITNESS_FILE);
    let read = store_lines::read(&std::fs::read(&path).unwrap(), &path);
    assert_eq!(read.values.len(), 1, "only its first line");
    assert_eq!(read.values[0]["storeExisted"], false, "the witness began with the store");
    assert_eq!(read.values[0]["projectsPresent"], json!([]), "no project was present when it began");
    assert_eq!(legacy_import_origin(&store, attachment.project.as_deref().unwrap()).unwrap(), LegacyOrigin::NoImport);
    drop(own);
}

/// Review round 1, finding 4, as App Agent 0 decided it: the boundary is the
/// list of projects present that the witness's first line records, and no
/// time is compared. The reviewer's two states: a project that predates the
/// witness, with imported payload and a lost account, whose creation time is
/// not before the witness's, still reads "origin not established"; a project
/// made after the witness began, with a creation time before it (a clock set
/// back), reads "no import". Then the three conditions of the decision.
#[test]
fn the_witness_boundary_is_the_recorded_list_of_projects_present_and_no_clock() {
    let l = Legacy::new();
    import(&l.root).unwrap();
    assert!(!l.present().is_empty(), "the project holds imported payload");
    // The store as it was before the witness existed, with the account lost.
    std::fs::remove_file(l.store.join(witness::WITNESS_FILE)).unwrap();
    std::fs::remove_file(l.dir.join("imports.jsonl")).unwrap();
    set_created(&l.dir, "2099-01-01T00:00:00.000Z");
    recover_at_startup().unwrap();
    let path = l.store.join(witness::WITNESS_FILE);
    let first_line = |bytes: &[u8]| store_lines::read(bytes, &path).values[0].clone();
    let began = l.witness();
    assert_eq!(first_line(&began)["projectsPresent"], json!([key_of(&l.dir)]));
    assert!(matches!(l.origin().unwrap(), LegacyOrigin::NotEstablished(_)), "never \"no import\", whatever its creation time says");
    let later = attach(&folder("witness-clock-set-back-"), true).unwrap();
    set_created(later.dir.as_ref().unwrap(), "2000-01-01T00:00:00.000Z");
    assert_eq!(legacy_import_origin(&l.store, later.project.as_deref().unwrap()).unwrap(), LegacyOrigin::NoImport, "made after the witness began, whatever its creation time says");
    // Condition 2. What the list records is the project's store folder key,
    // which comes from its identity and which no act changes. The folder is
    // given a new identity: that is a new project with its own folder and
    // none of the imported payload; the earlier project, its payload and its
    // standing are as they were.
    std::fs::remove_file(l.root.join(PROJECT_LINK)).unwrap();
    new_identity(&l.root).unwrap();
    let renamed = attach(&l.root, false).unwrap();
    let new_project = renamed.project.clone().expect("the folder has its new identity");
    assert_ne!(new_project, l.project);
    assert!(matches!(l.origin().unwrap(), LegacyOrigin::NotEstablished(_)), "the earlier project still reads not established");
    assert!(!l.present().is_empty(), "its imported payload is where it was");
    let new_dir = project_dir(&l.store, &new_project);
    for copy in l.copies() {
        assert!(!new_dir.join(&copy).exists(), "{copy}: nothing imported is under the new identity");
    }
    assert_eq!(legacy_import_origin(&l.store, &new_project).unwrap(), LegacyOrigin::NoImport);
    // Condition 3. The list is never changed, and the witness begins once.
    recover_at_startup().unwrap();
    assert_eq!(first_line(&l.witness()), first_line(&began), "the first line is as it was written");
    // If the witness is lost and a new one begins, every project then present
    // is in the new list: it errs toward "not established", never "no import".
    std::fs::remove_file(&path).unwrap();
    recover_at_startup().unwrap();
    let again = first_line(&l.witness());
    let listed: Vec<String> = again["projectsPresent"].as_array().unwrap().iter().map(|v| v.as_str().unwrap().to_owned()).collect();
    for dir in [&l.dir, later.dir.as_ref().unwrap(), &new_dir] {
        assert!(listed.contains(&key_of(dir)), "{}", dir.display());
    }
    assert!(matches!(legacy_import_origin(&l.store, later.project.as_deref().unwrap()).unwrap(), LegacyOrigin::NotEstablished(_)));
    // A first line that does not carry the list concludes nothing.
    let mut stripped = again.clone();
    stripped.as_object_mut().unwrap().remove("projectsPresent");
    std::fs::write(&path, format!("{stripped}\n")).unwrap();
    assert!(l.origin().unwrap_err().contains("does not list the projects present"));
}

/// Condition 1 of that decision: the listing is whole or the witness does not
/// begin. With the registry not read whole, the projects present cannot be
/// listed whole: the startup recovery shows that as a limit and writes no
/// witness, and an import, which would have begun it, is refused before any
/// copy. No partial list is ever written.
#[test]
fn a_witness_whose_listing_cannot_be_taken_whole_does_not_begin_and_refuses_the_act() {
    let l = Legacy::new();
    let path = l.store.join(witness::WITNESS_FILE);
    std::fs::remove_file(&path).unwrap();
    let registry = l.store.join("roots.jsonl");
    let mut bytes = std::fs::read(&registry).unwrap();
    bytes.extend(b"{\"damaged from outside\n");
    std::fs::write(&registry, &bytes).unwrap();
    *ROOTS.lock().unwrap() = None;
    let left = recover_at_startup().unwrap();
    assert!(left.iter().any(|l| l.contains("the projects present cannot be listed whole") && l.contains("was not begun")), "{left:?}");
    assert!(!path.exists(), "no witness, and so no partial list");
    let refused = import(&l.root).unwrap_err();
    assert!(refused.contains("not read whole"), "{refused}");
    assert!(!path.exists());
    assert!(l.present().is_empty(), "nothing was copied");
    assert!(matches!(l.origin().unwrap(), LegacyOrigin::NotEstablished(_)), "with no witness, never \"no import\"");
}

/// Pull requests 246 and 261 together (the merge of the two): a fragment an
/// interrupted append left in a project's import account makes the account
/// unknown until the store's recovery has closed and named it; then it is
/// left out with its naming line and every line before it reads as before.
#[test]
fn an_import_account_reads_as_before_once_its_fragment_is_closed_and_named_and_is_unknown_until_then() {
    let l = Legacy::new();
    import(&l.root).unwrap();
    let account = l.dir.join("imports.jsonl");
    let before = std::fs::read(&account).unwrap();
    assert_eq!(status(Some(&l.root))["project"]["reading"], "records store");
    let imports_before = status(Some(&l.root))["project"]["imports"].clone();
    assert_eq!(storage::read_all(&l.root).0.len(), 3);
    // An append cut short: a partial last line.
    let mut cut = before.clone();
    cut.extend_from_slice(br#"{"format":"chirality.records-import","formatVersion":"#);
    std::fs::write(&account, &cut).unwrap();
    let refused = home(&l.root).map(|_| ()).unwrap_err();
    assert!(refused.contains("records store unreadable") && refused.contains("its last line is not closed"), "{refused}");
    assert!(storage::read_all(&l.root).0.is_empty(), "nothing is read from a project whose account is unknown");
    assert!(write_dir(&l.root).is_err());
    // The store's recovery closes and names it; the account then reads as it did.
    recover_at_startup().unwrap();
    let recovered = std::fs::read(&account).unwrap();
    assert!(recovered.starts_with(&before) && recovered.len() > cut.len(), "the fragment's bytes are kept, closed and named");
    assert!(home(&l.root).unwrap().store_mode);
    assert_eq!(status(Some(&l.root))["project"]["reading"], "records store");
    assert_eq!(status(Some(&l.root))["project"]["imports"], imports_before, "the fragment and its naming line are not counted");
    assert_eq!(storage::read_all(&l.root).0.len(), 3);
    assert!(matches!(l.origin().unwrap(), LegacyOrigin::Imported(_)));
    // A line the rule refuses, written after the closed fragment, is still refused.
    let mut padded = recovered.clone();
    padded.extend_from_slice(b" {}\n");
    std::fs::write(&account, &padded).unwrap();
    assert!(home(&l.root).map(|_| ()).unwrap_err().contains("is not one JSON object and nothing else"));
}

/// Pull requests 246 and 261 together: an import account that exists and is
/// empty, decided by the witness. Nothing begun (the witness began, does not
/// list the project, and has no line for it): no import. Anything else:
/// unknown, an error everywhere the account is read through the store.
#[test]
fn an_empty_import_account_is_no_import_only_where_the_witness_shows_nothing_begun() {
    let unknown = |e: &str| e.contains("exists and is empty") && e.contains("whether an import was begun is not known");
    // A project created after the witness began, with no import: nothing begun.
    let l = Legacy::new();
    let later_root = folder("empty-account-later-");
    let later = attach(&later_root, true).unwrap();
    let later_dir = later.dir.unwrap();
    std::fs::write(later_dir.join("imports.jsonl"), b"").unwrap();
    assert!(witness::empty_account_is_nothing_begun(&later_dir));
    assert!(home(&later_root).is_ok(), "nothing begun: the empty account is no import");
    assert_eq!(legacy_import_origin(&l.store, later.project.as_deref().unwrap()).unwrap(), LegacyOrigin::NoImport);
    // The same project with a witness line: an import was begun.
    witness::record(&l.store, later.project.as_deref().unwrap(), "import:invented", &[]).unwrap();
    assert!(!witness::empty_account_is_nothing_begun(&later_dir));
    assert!(unknown(&home(&later_root).map(|_| ()).unwrap_err()));
    // A project present when the witness began (listed), its account empty:
    // not known. (In a store this build creates the witness begins before any
    // project, so the witness is begun again here with this project present.)
    std::fs::remove_file(l.store.join(witness::WITNESS_FILE)).unwrap();
    recover_at_startup().unwrap();
    std::fs::write(l.dir.join("imports.jsonl"), b"").unwrap();
    assert!(!witness::empty_account_is_nothing_begun(&l.dir));
    assert!(unknown(&home(&l.root).map(|_| ()).unwrap_err()));
    // No witness at all: not known.
    let other_root = folder("empty-account-other-");
    let other = attach(&other_root, true).unwrap().dir.unwrap();
    std::fs::write(other.join("imports.jsonl"), b"").unwrap();
    assert!(witness::empty_account_is_nothing_begun(&other));
    std::fs::rename(l.store.join(witness::WITNESS_FILE), l.store.join("witness-aside")).unwrap();
    assert!(!witness::empty_account_is_nothing_begun(&other));
    assert!(unknown(&home(&other_root).map(|_| ()).unwrap_err()));
    std::fs::rename(l.store.join("witness-aside"), l.store.join(witness::WITNESS_FILE)).unwrap();
}

/// Pull requests 246 and 261 together: the witness reads a project's account
/// through the store's strict reading, so an account that exists and cannot
/// be read is an error, never "no account evidence" from which a project the
/// witness does not list would read "no import".
#[test]
fn an_unreadable_import_account_never_reads_no_import_through_the_witness() {
    let l = Legacy::new();
    let later = attach(&folder("unreadable-account-later-"), true).unwrap();
    let (project, dir) = (later.project.unwrap(), later.dir.unwrap());
    assert_eq!(legacy_import_origin(&l.store, &project).unwrap(), LegacyOrigin::NoImport, "an account that is not there: no import");
    for (label, content) in [
        ("a line that is not an import line", &b"{}\n"[..]),
        ("a padded line", &b" {}\n"[..]),
        ("a partial line", &br#"{"format":"#[..]),
        ("a key given twice", &br#"{"format":"chirality.records-import","format":"chirality.records-import"}"#[..]),
    ] {
        std::fs::write(dir.join("imports.jsonl"), content).unwrap();
        let origin = legacy_import_origin(&l.store, &project);
        assert!(origin.as_ref().is_err_and(|e| e.contains("records store unreadable")), "{label}: {origin:?}");
    }
}

/// Review round 3, finding R3-B1: an account that exists and yields no import
/// line because it holds only closed fragments and the lines that name them
/// is decided as an empty one is, on what was read and not on the bytes:
/// unknown, unless nothing was begun for the project.
#[test]
fn an_import_account_holding_only_named_fragments_is_decided_as_an_empty_one() {
    let unknown = |e: &str| e.contains("holds no import line, only closed fragments") && e.contains("whether an import was begun is not known");
    let fragments_only = || {
        let tail = br#"{"format":"chirality.records-import","formatVersion":"#;
        let (closing, line) = store_lines::closure(tail);
        [tail.as_slice(), &closing, &store_lines::naming_line(1, &line).unwrap()].concat()
    };
    // The reviewer's state: a project holding imported records, listed when
    // the witness began, its account replaced by a fragment that the recovery
    // then closed and named.
    let l = Legacy::new();
    import(&l.root).unwrap();
    std::fs::remove_file(l.store.join(witness::WITNESS_FILE)).unwrap();
    recover_at_startup().unwrap();
    let account = l.dir.join("imports.jsonl");
    std::fs::write(&account, br#"{"format":"chirality.records-import","formatVersion":"#).unwrap();
    recover_at_startup().unwrap();
    let recovered = std::fs::read(&account).unwrap();
    assert_eq!(store_lines::read(&recovered, &account).set_aside, vec![1], "closed and named by the recovery");
    assert!(unknown(&home(&l.root).map(|_| ()).unwrap_err()));
    assert!(write_dir(&l.root).is_err());
    assert!(storage::read_all(&l.root).0.is_empty());
    let destination = folder("fragments-only-export-").join("bag");
    let exported = crate::records_export::export(&l.root, &destination);
    assert!(exported.is_err() && !destination.exists(), "no verified export: {exported:?}");
    // The same, built directly, for a project created after the witness began
    // that has a witness line: an import was begun, so unknown.
    let later_root = folder("fragments-only-later-");
    let later = attach(&later_root, true).unwrap();
    let later_dir = later.dir.unwrap();
    std::fs::write(later_dir.join("imports.jsonl"), fragments_only()).unwrap();
    // A project that genuinely never imported still works, through reading,
    // writing and export.
    assert!(home(&later_root).is_ok(), "nothing begun: no import, as for an empty file");
    records::append_project(&later_root, None, "writer:later", "evidence_limit", &APP_WRITER, body("never imported")).unwrap();
    assert_eq!(storage::read_all(&later_root).0.len(), 1);
    let destination = folder("fragments-only-never-imported-").join("bag");
    assert!(crate::records_export::export(&later_root, &destination).is_ok(), "a project that never imported exports");
    witness::record(&l.store, later.project.as_deref().unwrap(), "import:invented", &[]).unwrap();
    assert!(unknown(&home(&later_root).map(|_| ()).unwrap_err()));
}

