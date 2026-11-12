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
        // The import, run again, completes; the witness still holds every copy.
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
    // An identity record from before the witness, as an earlier App wrote it.
    let record = l.dir.join("project.json");
    let mut identity: Value = serde_json::from_slice(&std::fs::read(&record).unwrap()).unwrap();
    identity["createdAt"] = json!("2026-01-01T00:00:00.000Z");
    std::fs::write(&record, serde_json::to_vec(&identity).unwrap()).unwrap();
    recover_at_startup().unwrap();
    match l.origin().unwrap() {
        LegacyOrigin::NotEstablished(reason) => {
            assert!(reason.contains("existed before") && reason.contains("absent"), "{reason}");
            assert!(reason.contains("nothing in this project reads as the person's decision") && reason.contains("This does not change."), "{reason}");
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
    let record: Value = serde_json::from_slice(&std::fs::read(fresh.dir.as_ref().unwrap().join("project.json")).unwrap()).unwrap();
    assert!(record["createdAt"].as_str().unwrap() >= first["at"].as_str().unwrap(), "created at or after the witness began");
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
    let record: Value = serde_json::from_slice(&std::fs::read(attachment.dir.as_ref().unwrap().join("project.json")).unwrap()).unwrap();
    assert!(record["createdAt"].as_str().unwrap() >= read.values[0]["at"].as_str().unwrap());
    assert_eq!(legacy_import_origin(&store, attachment.project.as_deref().unwrap()).unwrap(), LegacyOrigin::NoImport);
    drop(own);
}
