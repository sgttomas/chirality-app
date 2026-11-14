use super::*;

const UNKNOWN_FOLDER: &str = "not known which project this folder belongs to in this process; nothing written";

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
