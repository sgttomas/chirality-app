use super::*;
use std::os::unix::fs::PermissionsExt;

// Each name denotes a row/family in the second review's table. Subcases cover
// the distinct readable evidence and precedence outcomes within those rows.
const CASES: &[&str] = &[
    "import needed",
    "empty final",
    "unclosed final",
    "uncertain in place",
    "corrupt final",
    "incomplete in place",
    "incomplete empty",
    "incomplete held",
    "incomplete late",
    "incomplete package",
    "torn registry",
    "closed",
    "retention unreadable",
    "disposed",
    "disposal incomplete",
    "disposal uncertain",
    "roots unreadable",
    "import unreadable",
    "import empty",
    "import unclosed",
    "census fails",
    "routing uncertain",
    "link missing",
    "link unreadable",
    "link changed",
    "link other store",
    "several identities",
    "torn unassociated",
    "unknown link unreadable",
    "moved",
    "duplicated",
    "another store",
    "released",
    "package incomplete",
    "store absent",
    "store identity changed",
    "root absent",
    "root alias",
    "admit empty",
    "admit uncertain empty",
    "admit runs",
    "admit acts",
    "admit legacy",
    "admit capture",
    "admit pending",
    "admit imported",
    "admit imported refused",
    "admit package",
    "admit census fails",
    "admit hardlink",
    "admit hold",
    "witness reproof fails",
    "account reproof fails",
    "first mint empty",
    "first mint legacy",
];

struct StatusCase {
    _own: OwnStore,
    root: PathBuf,
    dir: PathBuf,
    extra: Vec<PathBuf>,
}
impl Drop for StatusCase {
    fn drop(&mut self) {
        storage::fail_publication_sync_after_for_test(None);
        storage::fail_directory_for_test(None);
        let _ = std::fs::remove_dir_all(&self.root);
        for path in &self.extra {
            let _ = std::fs::remove_dir_all(path);
        }
    }
}
impl StatusCase {
    fn new(case: &str) -> Self {
        let (own, root, dir) = import_gate_project();
        let mut f = Self {
            _own: own,
            root,
            dir,
            extra: vec![],
        };
        match case {
            "uncertain in place" | "admit uncertain empty" => {
                std::fs::create_dir_all(f.dir.join("connectors")).unwrap();
                std::fs::write(f.dir.join("connectors/opaque-evidence"), b"opaque").unwrap();
            }
            "empty final" | "unclosed final" | "corrupt final" => {
                let path = f.dir.join(storage::log_rel(None, "writer:unpublished"));
                std::fs::create_dir_all(path.parent().unwrap()).unwrap();
                std::fs::write(
                    path,
                    match case {
                        "empty final" => b"".as_slice(),
                        "unclosed final" => b"unclosed",
                        _ => b"corrupt\n",
                    },
                )
                .unwrap();
            }
            "incomplete late"
            | "admit imported"
            | "admit imported refused"
            | "witness reproof fails"
            | "account reproof fails" => {
                if case == "admit imported refused" {
                    std::fs::create_dir_all(f.root.join(".chirality/captures")).unwrap();
                    std::fs::write(
                        f.root.join(".chirality/captures/refused.json"),
                        b"not a capture",
                    )
                    .unwrap();
                }
                import(&f.root).unwrap();
            }
            "unregistered kept" | "incomplete held" | "admit runs" | "admit acts"
            | "admit legacy" | "admit census fails" | "admit hardlink" | "admit hold" => {
                let rel = match case {
                    "admit runs" => storage::log_rel(Some("run:held"), "writer:held"),
                    "admit legacy" => REGISTERED_COPY.into(),
                    _ => storage::log_rel(None, "writer:held"),
                };
                let path = f.dir.join(rel);
                std::fs::create_dir_all(path.parent().unwrap()).unwrap();
                std::fs::copy(f.legacy(), &path).unwrap();
                if case == "admit hardlink" {
                    let other = folder("status-final-alias-");
                    std::fs::hard_link(path, other.join("alias")).unwrap();
                    f.extra.push(other);
                }
            }
            "admit capture" | "admit pending" => {
                let capture = import_gate_capture();
                let submission = import_gate_submission(&capture);
                place_gate_capture(
                    &f.dir,
                    &capture,
                    (case == "admit pending").then_some(&submission),
                );
            }
            "admit package" | "incomplete package" | "package incomplete" => {
                let native = f.dir.join(storage::log_rel(None, "writer:package"));
                std::fs::create_dir_all(native.parent().unwrap()).unwrap();
                std::fs::copy(f.legacy(), native).unwrap();
                let output = folder("status-package-");
                let bag = output.join("bag");
                crate::records_export::export(&f.root, &bag).unwrap();
                let destination = output.join("destination");
                use_store_for_test(Some(Ok(Store {
                    root: destination.clone(),
                    placement: Placement::Test,
                    limits: vec![],
                })));
                let plan = package::prepare(&f.root, &bag, &actor(), &observed()).unwrap();
                if case == "package incomplete" {
                    package::STOP.with(|s| *s.borrow_mut() = Some("payload"));
                }
                let result = package::apply(plan, &actor(), &observed());
                package::STOP.with(|s| *s.borrow_mut() = None);
                if case == "package incomplete" {
                    assert!(result.is_err(), "{result:?}");
                } else {
                    result.unwrap();
                }
                f.dir = attach(&f.root, false)
                    .ok()
                    .and_then(|a| a.dir)
                    .unwrap_or_else(|| project_dir(&destination, &read_link_id(&f.root)));
                f.extra.push(output);
            }
            _ => {}
        }
        if case.starts_with("incomplete ") {
            append_line(&f.dir.join("imports.jsonl"), &json!({"format":IMPORT_FORMAT,"formatVersion":VERSION,"event":"started","importId":"import:status","at":"now","storeHeld":matches!(case,"incomplete held"|"incomplete late"|"incomplete package"),"census":[]})).unwrap();
        }
        match case {
            "admit empty" | "admit uncertain empty" | "incomplete empty" => {
                std::fs::remove_dir_all(f.root.join(".chirality/records")).unwrap();
            }
            "closed" | "admit hold" | "disposed" | "disposal incomplete" | "disposal uncertain" => {
                if case != "closed" && case != "admit hold" {
                    import(&f.root).unwrap();
                }
                let action = if case == "admit hold" {
                    "set-hold"
                } else {
                    "close"
                };
                let plan =
                    crate::records_retention::prepare(&f.root, action, None, &actor(), &observed())
                        .unwrap();
                crate::records_retention::apply(plan, &actor(), &observed()).unwrap();
                if case.starts_with("dispos") {
                    let output = folder("status-disposal-");
                    let bag = output.join("bag");
                    crate::records_export::export(&f.root, &bag).unwrap();
                    let plan = crate::records_retention::prepare(
                        &f.root,
                        "dispose",
                        Some(&bag),
                        &actor(),
                        &observed(),
                    )
                    .unwrap();
                    crate::records_retention::fail_remove_for_test(case == "disposal incomplete");
                    if case == "disposal uncertain" {
                        crate::records_retention::FAIL_COMPLETION_PUBLICATION.with(|v| v.set(true));
                    }
                    let result = crate::records_retention::apply(plan, &actor(), &observed());
                    crate::records_retention::fail_remove_for_test(false);
                    crate::records_retention::FAIL_COMPLETION_PUBLICATION.with(|v| v.set(false));
                    storage::fail_directory_for_test(None);
                    if case == "disposed" {
                        result.unwrap();
                    } else {
                        assert!(result.is_err());
                    }
                    f.extra.push(output);
                }
            }
            "torn registry" | "torn unassociated" => {
                use std::io::Write;
                std::fs::OpenOptions::new()
                    .append(true)
                    .open(f.store().join("roots.jsonl"))
                    .unwrap()
                    .write_all(b"unclosed")
                    .unwrap();
                if case == "torn unassociated" {
                    let other = folder("status-unassociated-");
                    f.extra.push(std::mem::replace(&mut f.root, other));
                }
            }
            "roots unreadable" => {
                std::fs::remove_file(f.store().join("roots.jsonl")).unwrap();
                std::fs::create_dir(f.store().join("roots.jsonl")).unwrap();
            }
            "retention unreadable" => {
                let events = f
                    .store()
                    .join("administration")
                    .join(f.dir.file_name().unwrap())
                    .join("events");
                std::fs::create_dir_all(&events).unwrap();
                std::fs::write(events.join("unreadable.json"), b"bad administration").unwrap();
            }
            "import unreadable" | "import empty" | "import unclosed" => {
                std::fs::write(
                    f.dir.join("imports.jsonl"),
                    match case {
                        "import empty" => b"".as_slice(),
                        "import unclosed" => b"unclosed",
                        _ => b"unreadable\n",
                    },
                )
                .unwrap();
            }
            "census fails" | "admit census fails" => {
                std::fs::remove_dir_all(f.root.join(".chirality/records")).unwrap();
                std::fs::write(f.root.join(".chirality/records"), b"not a folder").unwrap();
            }
            "routing uncertain" => {
                std::fs::create_dir_all(f.dir.join("acts")).unwrap();
                std::fs::write(f.dir.join("acts/unknown"), b"ambiguous home").unwrap();
            }
            "link missing" => {
                std::fs::remove_file(f.root.join(PROJECT_LINK)).unwrap();
            }
            "link unreadable" => {
                std::fs::write(f.root.join(PROJECT_LINK), b"unreadable link").unwrap();
            }
            "link changed" | "link other store" => {
                let mut link = link_value(&read_link_id(&f.root), &opened().unwrap().1);
                if case == "link changed" {
                    link["projectId"] = json!("chirality-project:other");
                } else {
                    link["storeId"] = json!("records-store:other");
                }
                std::fs::write(
                    f.root.join(PROJECT_LINK),
                    serde_json::to_vec(&link).unwrap(),
                )
                .unwrap();
            }
            "several identities" => {
                append_line(&f.store().join("roots.jsonl"), &json!({"format":ROOT_FORMAT,"formatVersion":VERSION,"projectId":"chirality-project:other","root":f.root.to_str().unwrap(),"at":"now","how":"minted"})).unwrap();
            }
            "unknown link unreadable"
            | "another store"
            | "first mint empty"
            | "first mint legacy" => {
                let root = folder("status-new-project-");
                if case == "unknown link unreadable" {
                    std::fs::create_dir(root.join(".chirality")).unwrap();
                    std::fs::write(root.join(PROJECT_LINK), b"bad link").unwrap();
                } else if case == "another store" {
                    std::fs::create_dir(root.join(".chirality")).unwrap();
                    std::fs::write(
                        root.join(PROJECT_LINK),
                        serde_json::to_vec(&link_value(
                            "chirality-project:elsewhere",
                            "records-store:elsewhere",
                        ))
                        .unwrap(),
                    )
                    .unwrap();
                } else if case == "first mint legacy" {
                    records::append(
                        &root
                            .join(".chirality/records")
                            .join(storage::log_rel(None, "writer:legacy")),
                        "evidence_limit",
                        &APP_WRITER,
                        body("in place"),
                    )
                    .unwrap();
                }
                f.extra.push(std::mem::replace(&mut f.root, root));
            }
            "moved" | "duplicated" | "released" => {
                let root = folder("status-copied-project-");
                std::fs::create_dir(root.join(".chirality")).unwrap();
                std::fs::copy(f.root.join(PROJECT_LINK), root.join(PROJECT_LINK)).unwrap();
                if case == "moved" {
                    std::fs::remove_file(f.root.join(PROJECT_LINK)).unwrap();
                }
                if case == "released" {
                    append_line(&f.store().join("roots.jsonl"), &json!({"format":ROOT_FORMAT,"formatVersion":VERSION,"projectId":read_link_id(&root),"root":f.root.to_str().unwrap(),"at":"now","how":"released"})).unwrap();
                }
                f.extra.push(std::mem::replace(&mut f.root, root));
            }
            "unregistered kept" => {
                std::fs::write(f.store().join("roots.jsonl"), b"").unwrap();
                *ROOTS.lock().unwrap() = None;
            }
            "writer lock invalid" => {
                std::fs::create_dir(f.dir.join(".writer.lock")).unwrap();
            }
            "new installation" => {
                let store = f.store().join("new-installation");
                use_store_not_started_for_test(Some(Ok(Store {
                    root: store,
                    placement: Placement::Test,
                    limits: vec![],
                })));
            }
            "store absent" => {
                std::fs::remove_dir_all(f.store()).unwrap();
            }
            "store identity changed" => {
                std::fs::write(f.store().join("store.json"), b"changed identity").unwrap();
            }
            "root absent" => {
                std::fs::remove_dir_all(&f.root).unwrap();
            }
            "root alias" => {
                let output = folder("status-root-alias-");
                std::os::unix::fs::symlink(&f.root, output.join("alias")).unwrap();
                f.extra
                    .push(std::mem::replace(&mut f.root, output.join("alias")));
                f.extra.push(output);
            }
            "witness reproof fails" | "account reproof fails" => {
                let path = if case == "witness reproof fails" {
                    f.store().join(witness::WITNESS_FILE)
                } else {
                    f.dir.join("imports.jsonl")
                };
                storage::fail_publication_sync_after_for_test(Some((
                    path,
                    0,
                    storage::PublicationSyncStage::File,
                )));
            }
            _ => {}
        }
        f
    }
    fn store(&self) -> PathBuf {
        current().unwrap().root
    }
    fn legacy(&self) -> PathBuf {
        self.root
            .join(".chirality/records")
            .join(storage::log_rel(None, "writer:legacy"))
    }
}
fn read_link_id(root: &Path) -> String {
    match read_link(root) {
        Link::Present { project, .. } => project,
        _ => panic!("expected fixture link"),
    }
}
fn actor() -> Value {
    crate::act_control::person(Some("Invented status fixture"), Some("invented-os"))
}
fn observed() -> Value {
    json!({"fixture":"synthetic native callback; no person's act"})
}

// A tree snapshot includes every directory entry, exact regular-file bytes,
// link target, file kind and permissions. It never follows a link.
fn tree(path: &Path) -> BTreeMap<PathBuf, (u32, Vec<u8>)> {
    fn walk(base: &Path, path: &Path, out: &mut BTreeMap<PathBuf, (u32, Vec<u8>)>) {
        let meta = match std::fs::symlink_metadata(path) {
            Ok(meta) => meta,
            Err(e) if e.kind() == std::io::ErrorKind::NotFound => return,
            Err(e) => panic!("snapshot {}: {e}", path.display()),
        };
        let bytes = if meta.file_type().is_symlink() {
            std::fs::read_link(path)
                .unwrap()
                .as_os_str()
                .as_encoded_bytes()
                .to_vec()
        } else if meta.is_file() {
            std::fs::read(path).unwrap()
        } else {
            vec![]
        };
        out.insert(
            path.strip_prefix(base).unwrap().to_path_buf(),
            (meta.permissions().mode(), bytes),
        );
        if meta.is_dir() {
            for entry in std::fs::read_dir(path).unwrap() {
                walk(base, &entry.unwrap().path(), out);
            }
        }
    }
    let mut out = BTreeMap::new();
    walk(path, path, &mut out);
    out
}

#[test]
fn records_store_import_gate_status_is_read_only_for_the_refusal_and_admission_table() {
    for case in CASES.iter().copied().chain([
        "unregistered kept",
        "writer lock invalid",
        "new installation",
    ]) {
        eprintln!("read-only row: {case}");
        let f = StatusCase::new(case);
        let before = (tree(&f.root), tree(&f.store()));
        storage::observe_publication_for_test(Some(Box::new(|step, path| {
            panic!("status reached {step:?}: {}", path.display())
        })));
        let shown = storage::without_mutations_for_test(|| status(Some(&f.root)));
        storage::observe_publication_for_test(None);
        assert!(shown.is_object(), "{case}: {shown}");
        assert_eq!(
            (tree(&f.root), tree(&f.store())),
            before,
            "{case}: status changed bytes or directory entries"
        );
    }
}

// Compare actual writer refusals, typed inspection and the visible status.
// Write-dependent outcomes are compared as outstanding, never predicted from
// readable bytes. Unavailable ordinary reads retain their separate wrapper.
#[test]
fn records_store_import_gate_status_matches_the_ordered_gate() {
    let mut failures = Vec::new();
    for case in CASES {
        eprintln!("property row: {case}");
        let f = StatusCase::new(case);
        let inspection = storage::without_mutations_for_test(|| inspect_write(&f.root));
        let shown = status(Some(&f.root));
        let gate = write_dir(&f.root);
        let expected = match *case {
            "torn registry" => Some(WriteRefusalKind::Registry),
            "closed" => Some(WriteRefusalKind::Closed),
            "retention unreadable" => Some(WriteRefusalKind::Retention),
            "disposed" | "disposal incomplete" | "disposal uncertain" => {
                Some(WriteRefusalKind::Disposed)
            }
            "import unreadable" | "import empty" | "import unclosed" => {
                Some(WriteRefusalKind::ImportAccount)
            }
            "census fails" => Some(WriteRefusalKind::Census),
            "uncertain in place" | "corrupt final" | "routing uncertain" => {
                Some(WriteRefusalKind::NotKnown)
            }
            "import needed" | "empty final" | "unclosed final" => {
                Some(WriteRefusalKind::ImportNeeded)
            }
            name if name.starts_with("incomplete ") => Some(WriteRefusalKind::ImportIncomplete),
            name if name.starts_with("admit ")
                || name.contains("reproof fails")
                || name.starts_with("first mint ") =>
            {
                None
            }
            _ => Some(WriteRefusalKind::Association),
        };
        match (&inspection, expected) {
            (WriteInspection::Refused(refusal), Some(kind)) => {
                if refusal.kind != kind || gate.as_ref().err() != Some(&refusal.message) {
                    failures.push(format!(
                        "{case}: expected {kind:?}; inspection={inspection:?}; gate={gate:?}"
                    ));
                }
            }
            (WriteInspection::Outstanding(OutstandingWriteProof::FirstWriteMint), None)
                if case.starts_with("first mint ") => {}
            (WriteInspection::Outstanding(OutstandingWriteProof::CompletionReproof), None)
                if case.contains("reproof fails")
                    || matches!(*case, "admit imported" | "admit imported refused") =>
            {
                if case.contains("reproof fails") {
                    let error = gate.as_ref().unwrap_err();
                    if !error.contains("durability not established")
                        || !error.contains("injected failure")
                    {
                        failures.push(format!("{case}: {gate:?}"));
                    }
                } else if gate.is_err() {
                    failures.push(format!("{case}: {gate:?}"));
                }
            }
            (WriteInspection::None, None) if case.starts_with("admit ") && gate.is_ok() => {}
            _ => failures.push(format!(
                "{case}: wrong inspection: {inspection:?}; gate={gate:?}"
            )),
        }
        let project = &shown["project"];
        if project["state"] != "unavailable" {
            let needed = expected == Some(WriteRefusalKind::ImportNeeded);
            if project["importNeeded"] != needed {
                failures.push(format!("{case}: importNeeded disagrees: {project}"));
            }
            let notes = project["notes"].as_array().unwrap();
            if let WriteInspection::Refused(refusal) = &inspection {
                if !notes.iter().any(|n| n.as_str() == Some(&refusal.message)) {
                    failures.push(format!(
                        "{case}: exact gate sentence absent: {refusal:?}; status={project}"
                    ));
                }
                if !refusal.imports_assessed()
                    && !notes.iter().any(|n| {
                        n.as_str()
                            .is_some_and(|s| s.contains("Imports were not assessed"))
                    })
                {
                    failures.push(format!("{case}: imports not assessed omitted: {project}"));
                }
            }
            if let WriteInspection::Outstanding(proof) = &inspection {
                if !notes.iter().any(|n| n.as_str() == Some(proof.note())) {
                    failures.push(format!("{case}: proof not outstanding: {project}"));
                }
            }
            let reading_needed = project["reading"]
                .as_str()
                .unwrap()
                .contains("import needed");
            let note_needed = notes.iter().any(|n| {
                n.as_str()
                    .is_some_and(|n| n.contains("recording for the project is refused until"))
            });
            let in_place = project["reading"]
                .as_str()
                .unwrap()
                .starts_with("records in place");
            if reading_needed != (in_place && needed) || note_needed != (in_place && needed) {
                failures.push(format!("{case}: contradictory import wording: {project}"));
            }
            if matches!(
                *case,
                "torn registry" | "closed" | "uncertain in place" | "incomplete in place"
            ) {
                if project["notImported"] != 1
                    || project["reading"] != "records in place in the project"
                    || !notes.iter().any(|n| {
                        n.as_str()
                            .is_some_and(|n| n.contains("are read in place and are not imported"))
                    })
                {
                    failures.push(format!(
                        "{case}: reading/count/import history lost: {project}"
                    ));
                }
            }
        } else if project["error"].as_str().is_none_or(str::is_empty) {
            failures.push(format!(
                "{case}: unavailable read lost its cause: {project}"
            ));
        }
    }
    // A queued writer carries its old dir; ordinary status describes the
    // current attachment. Both entry-point effects still share this refusal.
    let f = StatusCase::new("admit empty");
    let other = folder("status-current-project-");
    let queued = ordered_write_check(&f.dir, &other, |_, _| {
        Ok(Some(OutstandingWriteProof::CompletionReproof))
    })
    .unwrap_err();
    assert_eq!(queued.kind, WriteRefusalKind::Association);
    assert_eq!(write_permitted(&f.dir, &other).unwrap_err(), queued.message);
    std::fs::remove_dir_all(other).unwrap();
    let absent = Path::new("no-store-parent");
    let direct =
        ordered_write_check(absent, &f.root, |_, _| panic!("no proof before roots")).unwrap_err();
    assert_eq!(direct.kind, WriteRefusalKind::Registry);
    assert_eq!(
        write_permitted(absent, &f.root).unwrap_err(),
        direct.message
    );
    assert!(failures.is_empty(), "{}", failures.join("\n"));
}

#[test]
fn records_store_import_gate_status_mutation_control_detects_even_unchanged_byte_effects() {
    let f = StatusCase::new("admit imported");
    let operations: Vec<Box<dyn Fn()>> = vec![
        Box::new(|| {
            let _ = storage::sync_dir(&f.store());
        }),
        Box::new(|| {
            let _ = storage::sync_publication(&f.dir.join("imports.jsonl"));
        }),
        Box::new(|| {
            let _ = storage::ensure_directory(&f.dir);
        }),
        Box::new(|| {
            let _ = storage::create_json(&f.dir.join("new.json"), &json!({}));
        }),
        Box::new(|| {
            let _ = storage::create_bytes(&f.dir.join("new"), b"new");
        }),
        Box::new(|| {
            let _ = storage::lock(&f.dir.join(".writer.lock"));
        }),
        Box::new(|| {
            let _ = append_line(&f.dir.join("imports.jsonl"), &json!({}));
        }),
        Box::new(|| {
            let _ = register(
                &f.store(),
                "chirality-project:probe",
                f.root.to_str().unwrap(),
                "registered",
            );
        }),
        Box::new(|| {
            let _ = attach(&f.root, true);
        }),
    ];
    for operation in operations {
        assert!(std::panic::catch_unwind(std::panic::AssertUnwindSafe(|| {
            storage::without_mutations_for_test(operation)
        }))
        .is_err());
    }
    // The guard is reset even after panic; a real writer still re-proves.
    assert!(write_dir(&f.root).is_ok());
}
