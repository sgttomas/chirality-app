use super::*;

const UNKNOWN_FOLDER: &str = "not known which project this folder belongs to in this process; nothing written";

fn store_bytes(root: &Path) -> BTreeMap<PathBuf, Vec<u8>> {
    let mut files = BTreeMap::new();
    let mut todo = vec![root.to_path_buf()];
    while let Some(dir) = todo.pop() {
        for entry in std::fs::read_dir(dir).unwrap() {
            let entry = entry.unwrap();
            if entry.file_type().unwrap().is_dir() {
                todo.push(entry.path());
            } else {
                files.insert(entry.path(), std::fs::read(entry.path()).unwrap());
            }
        }
    }
    files
}

#[test]
fn records_store_writer_binding_f4_cached_act_log_preserves_confirmation_refusal() {
    let own = OwnStore::new();
    let root = folder("writer-f4-cached-log-");
    let log = storage::project_log(&root, None, "writer:cached").unwrap();
    records::append(&log, "evidence_limit", &APP_WRITER, body("before loss")).unwrap();
    std::fs::write(own.0.join("roots.jsonl"), b"").unwrap();
    let reason = status(Some(&root))["project"]["attachment"]["refusal"].as_str().unwrap().to_owned();
    let before = store_bytes(&own.0);
    assert_eq!(records::append(&log, "evidence_limit", &APP_WRITER, body("after loss")).unwrap_err(), reason);
    assert_eq!(store_bytes(&own.0), before);
    adopt(&root).unwrap();
    records::append(&log, "evidence_limit", &APP_WRITER, body("after loss")).unwrap();
    assert_eq!(records::read_log(&log).0.len(), 2);
    std::fs::remove_dir_all(root).unwrap();
}

#[test]
fn records_store_writer_binding_f4_retained_history_requires_confirmation_before_first_write() {
    let own = OwnStore::new();
    let root = folder("writer-f4-");
    records::append_project(&root, None, "writer:f4", "evidence_limit", &APP_WRITER, body("retained")).unwrap();
    let dir = attach(&root, false).unwrap().dir.unwrap();
    let registry = own.0.join("roots.jsonl");
    std::fs::write(&registry, b"").unwrap();
    let before = attach(&root, false).unwrap();
    assert_eq!(before.fault, Some("no folder recorded"));
    let reason = before.refusal.unwrap();
    let view = status(Some(&root));
    assert_eq!(view["project"]["attachment"]["refusal"], reason);
    assert_eq!(view["project"]["reading"], "nothing from the records store: this folder's project identity is kept there with no folder recorded; not attached to this folder");
    let (entries, limits) = storage::read_all(&root);
    assert!(entries.is_empty(), "ordinary reading cannot take the retained identity");
    assert!(limits.iter().any(|limit| limit.contains(&reason)), "{limits:?}");
    let files_before = store_bytes(&own.0);
    assert_eq!(attach(&root, true).unwrap().refusal.as_deref(), Some(reason.as_str()));
    let written = records::append_project(&root, None, "writer:f4-new", "evidence_limit", &APP_WRITER, body("must wait"));
    assert!(written.as_ref().is_err_and(|e| e.contains(&reason)), "{written:?}");
    assert_eq!(bind_writer(&root).err().as_deref(), Some(reason.as_str()));
    assert_eq!(std::fs::read(&registry).unwrap(), b"");
    assert!(!dir.join(storage::log_rel(None, "writer:f4-new")).exists());
    assert_eq!(files_before, store_bytes(&own.0));
    adopt(&root).unwrap(); // Existing confirmation act's implementation, synthetic examination only.
    records::append_project(&root, None, "writer:f4-new", "evidence_limit", &APP_WRITER, body("must wait")).unwrap();
    assert_eq!(storage::read_all(&root).0.len(), 2);
    std::fs::remove_dir_all(root).unwrap();
}

#[test]
fn records_store_writer_binding_f4_link_without_retained_history_still_registers() {
    let own = OwnStore::new();
    let root = folder("writer-f4-unheld-");
    let (_, store) = opened().unwrap();
    std::fs::create_dir_all(root.join(".chirality")).unwrap();
    std::fs::write(root.join(PROJECT_LINK), serde_json::to_vec(&link_value("chirality-project:unheld", &store)).unwrap()).unwrap();
    assert!(attach(&root, false).unwrap().refusal.is_none());
    let writer = bind_writer(&root).unwrap();
    assert_eq!(writer.project_id(), "chirality-project:unheld");
    assert!(writer.records_dir().starts_with(&own.0));
    assert_eq!(root_for_dir(writer.records_dir()).as_deref(), Some(root.as_path()));
    std::fs::remove_dir_all(root).unwrap();
}

#[test]
fn records_store_writer_binding_moved_identity_is_not_adopted_while_activity_is_held() {
    a_moved_project_is_not_adopted_while_its_activity_is_held();
}

#[test]
fn records_store_writer_binding_first_attachment_still_registers() {
    let own = OwnStore::new();
    let root = folder("writer-first-");
    let attachment = attach(&root, true).unwrap();
    let dir = attachment.dir.unwrap();
    assert!(dir.starts_with(&own.0));
    assert!(dir.join("project.json").is_file());
    assert_eq!(root_for_dir(&dir).as_deref(), Some(root.as_path()));
    assert!(crate::records_retention::write_path(&dir).is_ok());
    std::fs::remove_dir_all(root).unwrap();
}

#[test]
fn records_store_writer_binding_new_identity_still_registers() {
    let own = OwnStore::new();
    let root = folder("writer-new-");
    let prior = attach(&root, true).unwrap().project.unwrap();
    let fresh = new_identity(&root).unwrap();
    let id = fresh["projectId"].as_str().unwrap();
    assert_ne!(id, prior);
    assert!(project_dir(&own.0, id).join("project.json").is_file());
    assert_eq!(attach(&root, false).unwrap().project.as_deref(), Some(id));
    std::fs::remove_dir_all(root).unwrap();
}

#[test]
fn records_store_writer_binding_unknown_folder_is_refused() {
    let own = OwnStore::new();
    let dir = project_dir(&own.0, "invented:never-opened");
    std::fs::create_dir_all(&dir).unwrap();
    assert!(root_for_dir(&dir).is_none());
    let ordinary = crate::records_retention::write_path(&dir).err();
    let existing = crate::records_retention::write_path_existing(&dir).err();
    assert_eq!(ordinary.as_deref(), Some(UNKNOWN_FOLDER));
    assert_eq!(existing.as_deref(), Some(UNKNOWN_FOLDER));
}

#[test]
fn records_store_writer_binding_registration_mark_ends_after_success() {
    let own = OwnStore::new();
    let root = folder("writer-registration-");
    let project = "invented:registration-only";
    let dir = project_dir(&own.0, project);
    let _lock = store_lock(&own.0).unwrap();
    register(&own.0, project, root.to_str().unwrap(), "minted").unwrap();
    assert!(root_for_dir(&dir).is_none());
    let error = storage::create_bytes(&dir.join("later"), b"not registration").err();
    assert_eq!(error.as_deref(), Some(UNKNOWN_FOLDER));
    assert!(!dir.join("later").exists());
    std::fs::remove_dir_all(root).unwrap();
}

#[test]
fn records_store_writer_binding_registration_mark_ends_after_error() {
    let own = OwnStore::new();
    let root = folder("writer-registration-failed-");
    let project = "invented:failed-registration";
    let dir = project_dir(&own.0, project);
    let _lock = store_lock(&own.0).unwrap();
    storage::fail_directory_for_test(Some(dir.clone()));
    let failed = register(&own.0, project, root.to_str().unwrap(), "minted");
    storage::fail_directory_for_test(None);
    assert!(failed.is_err(), "fault did not interrupt registration");
    assert!(root_for_dir(&dir).is_none());
    let error = storage::create_bytes(&dir.join("later"), b"not registration").err();
    assert_eq!(error.as_deref(), Some(UNKNOWN_FOLDER));
    assert!(!dir.join("later").exists());
    std::fs::remove_dir_all(root).unwrap();
}

#[test]
fn records_store_writer_binding_registration_does_not_admit_another_thread() {
    let own = OwnStore::new();
    let root = folder("writer-registration-thread-");
    REGISTER_BEFORE_PUBLICATION.with(|slot| *slot.borrow_mut() = Some(Box::new(|dir| {
        let dir = dir.to_path_buf();
        let error = std::thread::spawn(move || {
            crate::records_retention::write_path(&dir).err()
        }).join().unwrap();
        assert_eq!(error.as_deref(), Some(UNKNOWN_FOLDER));
    })));
    attach(&root, true).unwrap();
    std::fs::remove_dir_all(root).unwrap();
}

#[test]
fn records_store_writer_binding_registration_does_not_admit_another_or_replaced_folder() {
    let _own = OwnStore::new();
    let root = folder("writer-registration-physical-");
    REGISTER_BEFORE_PUBLICATION.with(|slot| *slot.borrow_mut() = Some(Box::new(|dir| {
        let other = dir.parent().unwrap().join(storage::key("invented:other-registration"));
        std::fs::create_dir(&other).unwrap();
        let other_error = crate::records_retention::write_path(&other).err();
        let aside = dir.with_extension("held");
        std::fs::rename(dir, &aside).unwrap();
        std::fs::create_dir(dir).unwrap();
        let replaced_error = crate::records_retention::write_path(dir).err();
        std::fs::remove_dir(dir).unwrap();
        std::fs::rename(aside, dir).unwrap();
        assert_eq!(other_error.as_deref(), Some(UNKNOWN_FOLDER));
        assert_eq!(replaced_error.as_deref(), Some(UNKNOWN_FOLDER));
    })));
    attach(&root, true).unwrap();
    std::fs::remove_dir_all(root).unwrap();
}
