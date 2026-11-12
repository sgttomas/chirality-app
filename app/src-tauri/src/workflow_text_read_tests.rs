// A workflow's own text, read for the person (crate::workflow_text_read):
// what is returned for an included entry and for a selection of each origin
// constructed here, what is refused, and that a read changes nothing.
// Constructed packages and the maintained fixtures only; no supplier, model,
// credential or native App.

use crate::workflow_text_read::Target;

fn included_target(name: &str, revision: &str) -> Target {
    Target { kind: "included".into(), name: Some(name.into()), revision: revision.into() }
}
fn chosen_target(revision: &str) -> Target {
    Target { kind: "selection".into(), name: None, revision: revision.into() }
}
fn bundled_identity() -> crate::workflow_workspace::WorkflowIdentity {
    crate::workflow_workspace::production_catalog::ProductionCatalog::load().unwrap().identity(BUNDLED).unwrap().clone()
}
/// Every path beneath `root` with its kind and size: a read leaves this unchanged.
fn tree(root: &std::path::Path) -> Vec<(String, bool, u64)> {
    fn walk(base: &std::path::Path, at: &std::path::Path, out: &mut Vec<(String, bool, u64)>) {
        let Ok(entries) = std::fs::read_dir(at) else { return };
        for entry in entries {
            let path = entry.unwrap().path();
            let meta = std::fs::symlink_metadata(&path).unwrap();
            out.push((path.strip_prefix(base).unwrap().to_string_lossy().into_owned(), meta.is_dir(), meta.len()));
            if meta.is_dir() { walk(base, &path, out); }
        }
    }
    let mut out = vec![];
    walk(root, root, &mut out);
    out.sort();
    out
}
/// A refusal carries its reason and no text, and never says the bytes matched.
fn assert_refused(read: &Value, reason: &str) {
    assert_eq!(read["state"], "refused", "{read}");
    assert!(read.get("text").is_none() && read.get("matched").is_none() && read.get("files").is_none(), "no text with a refusal: {read}");
    assert!(read["reason"].as_str().unwrap().contains(reason), "{read}");
}
/// A read: the text, its identity, its size, the other files as paths and sizes only.
fn assert_read(read: &Value, identity: &crate::workflow_workspace::WorkflowIdentity, on_disk: &std::path::Path) {
    assert_eq!(read["state"], "read", "{read}");
    assert_eq!(read["matched"], true);
    assert_eq!(read["identity"], json!(identity), "the source-qualified identity, as the snapshot gives it");
    let disk = std::fs::read_to_string(on_disk.join("WORKFLOW.md")).unwrap();
    assert_eq!(read["text"], disk.as_str(), "the bytes of WORKFLOW.md, unchanged");
    assert_eq!(read["bytes"], disk.len());
    let snapshot = crate::workflow_workspace::Snapshot::capture(on_disk).unwrap();
    let others = snapshot.files().iter().filter(|(p, _)| p.as_str() != "WORKFLOW.md")
        .map(|(p, b)| json!({"path":p,"bytes":b.len()})).collect::<Vec<_>>();
    assert_eq!(read["files"], json!(others), "other files as relative paths and sizes, never contents");
    assert_eq!(read["standing"], crate::workflow_text_read::STANDING);
}

#[test]
fn included_entry_text_is_the_installed_revision_and_the_read_changes_nothing() {
    let installed = InstalledBundle::new();
    let mut root = WorkflowRootSession::default();
    root.configure_installed_bundle(installed.0.clone()).unwrap();
    let identity = bundled_identity();
    let (before, files) = (root.snapshot(), tree(installed.0.parent().unwrap()));
    let read = root.read_included_text(&included_target(BUNDLED, &identity.revision));
    assert_read(&read, &identity, &installed.0.join(BUNDLED));
    assert!(!read["files"].as_array().unwrap().is_empty(), "this package has other files");
    assert_eq!(root.snapshot(), before, "no selection, library, run or record changed");
    assert!(root.selected.is_empty() && root.inspected.is_none(), "nothing selected");
    assert_eq!(tree(installed.0.parent().unwrap()), files, "no file or folder appears or changes");
    // The read is the same bytes a selection of the same entry would hold and compose a run's text from.
    let chat = crate::workflow_selection::Chat { source: "fixture source".into(), thread: "thread".into() };
    root.select_production_bundle(Some(&chat), installed.0.clone(), BUNDLED).unwrap();
    assert_eq!(read["text"], root.selected[&chat].selection.snapshot().workflow_text());
}

#[test]
fn included_entry_refusals_say_why_and_return_no_text() {
    let installed = InstalledBundle::new();
    let identity = bundled_identity();
    let mut root = WorkflowRootSession::default();
    // Before this App's installed resources are known, nothing is read.
    assert_refused(&root.read_included_text(&included_target(BUNDLED, &identity.revision)), "could not be verified");
    root.configure_installed_bundle(installed.0.clone()).unwrap();
    // A name is looked up in the compiled catalogue, never joined to a folder:
    // a package beside the bundle, reachable by a relative path, is not read.
    let outside = installed.0.parent().unwrap().join("outside");
    crate::workflow_workspace::Snapshot::from_files([("WORKFLOW.md".to_owned(), b"outside text".to_vec())].into()).unwrap().publish_new(&outside).unwrap();
    for name in ["no-such-workflow", "../outside", "coordinated-knowledge-work/../../outside", "/etc", "", "Coordinated-Knowledge-Work"] {
        let read = root.read_included_text(&included_target(name, &identity.revision));
        assert_refused(&read, "no workflow included with this App has that name");
        assert!(read["identity"].is_null(), "{read}");
    }
    assert_refused(&root.read_included_text(&Target { kind: "included".into(), name: None, revision: identity.revision.clone() }), "no included workflow was named");
    // The view showed another revision than the catalogue holds now.
    assert_refused(&root.read_included_text(&included_target(BUNDLED, "0".repeat(64).as_str())), "not the one the App holds now");
    // Listed by the catalogue but absent from the installed resources.
    let absent = crate::workflow_workspace::production_catalog::ProductionCatalog::load().unwrap().identity("create-workflow").unwrap().clone();
    assert_refused(&root.read_included_text(&included_target("create-workflow", &absent.revision)), "could not read this revision's files");
    // One byte changed in the stored WORKFLOW.md: the bytes no longer hash to the revision.
    let file = installed.0.join(BUNDLED).join("WORKFLOW.md");
    let original = std::fs::read(&file).unwrap();
    let mut changed = original.clone();
    changed[0] ^= 0x01;
    std::fs::write(&file, &changed).unwrap();
    let read = root.read_included_text(&included_target(BUNDLED, &identity.revision));
    assert_refused(&read, "could not read this revision's files and tie them to its identity");
    assert!(read["cause"].as_str().unwrap().contains("revision not verified"), "the host's own cause: {read}");
    assert_eq!(read["identity"], json!(identity), "the identity it was asked for, with no text");
    // Not UTF-8.
    let mut invalid = original.clone();
    invalid.extend_from_slice(&[0xff, 0xfe]);
    std::fs::write(&file, &invalid).unwrap();
    let read = root.read_included_text(&included_target(BUNDLED, &identity.revision));
    assert_refused(&read, "could not read this revision's files");
    assert!(read["cause"].as_str().unwrap().contains("UTF-8"), "{read}");
    // Restored, it reads again.
    std::fs::write(&file, &original).unwrap();
    assert_eq!(root.read_included_text(&included_target(BUNDLED, &identity.revision))["state"], "read");
    assert!(root.selected.is_empty() && root.inspected.is_none());
}

#[test]
fn chosen_text_of_an_included_selection_is_read_where_it_was_resolved() {
    let installed = InstalledBundle::new();
    let identity = bundled_identity();
    let mut root = WorkflowRootSession::default();
    root.configure_installed_bundle(installed.0.clone()).unwrap();
    let chat = crate::workflow_selection::Chat { source: "fixture source".into(), thread: "thread".into() };
    // No selection yet.
    assert_refused(&root.read_chosen_text(Some(&chat), &chosen_target(&identity.revision)), "no workflow is chosen");
    root.select_production_bundle(Some(&chat), installed.0.clone(), BUNDLED).unwrap();
    let (before, files) = (root.snapshot(), tree(installed.0.parent().unwrap()));
    let reference = root.selected[&chat].reference.clone();
    let read = root.read_chosen_text(Some(&chat), &chosen_target(&identity.revision));
    assert_read(&read, &identity, &installed.0.join(BUNDLED));
    assert_eq!(root.snapshot(), before, "the read changes nothing");
    assert_eq!(tree(installed.0.parent().unwrap()), files);
    assert_eq!(root.selected[&chat].reference, reference, "the selection is unchanged");
    // A selection is read without a name; another revision than the one shown is refused.
    assert_refused(&root.read_chosen_text(Some(&chat), &Target { kind: "selection".into(), name: Some(BUNDLED.into()), revision: identity.revision.clone() }), "without a name");
    assert_refused(&root.read_chosen_text(Some(&chat), &chosen_target("0".repeat(64).as_str())), "not the one the App holds now");
    // Another conversation has no selection.
    let other = crate::workflow_selection::Chat { source: "fixture source".into(), thread: "other".into() };
    assert_refused(&root.read_chosen_text(Some(&other), &chosen_target(&identity.revision)), "no workflow is chosen");
    // A byte changed where the selection was resolved from: no text, the selection stays.
    let file = installed.0.join(BUNDLED).join("WORKFLOW.md");
    let mut changed = std::fs::read(&file).unwrap();
    changed[0] ^= 0x01;
    std::fs::write(&file, &changed).unwrap();
    let read = root.read_chosen_text(Some(&chat), &chosen_target(&identity.revision));
    assert_refused(&read, "could not read this revision's files and tie them to its identity");
    assert!(read["cause"].as_str().unwrap().contains("revision not verified"), "{read}");
    assert_eq!(root.selected[&chat].reference, reference);
}

#[test]
fn chosen_text_of_a_development_holding_copy_and_a_registered_project_revision() {
    // A development holding copy, inspected with no conversation.
    let f = Fixture::new();
    let root = f.selected();
    let held = root.inspected.as_ref().unwrap().selection.identity().clone();
    let before = (root.snapshot(), tree(&f.root));
    let read = root.read_chosen_text(None, &chosen_target(&held.revision));
    assert_read(&read, &held, &f.package);
    assert_eq!((root.snapshot(), tree(&f.root)), before, "the read changes nothing");
    // A registered project revision, with a WORKFLOW.md of its own.
    let f = Fixture::new();
    let mut edited = String::new();
    let mut root = f.registered_with(|draft| {
        edited = std::fs::read_to_string(draft.join("WORKFLOW.md")).unwrap() + "\nAn invented closing line.\n";
        std::fs::write(draft.join("WORKFLOW.md"), &edited).unwrap();
    });
    let chat = root.fixture_chat();
    let chosen = root.selected[&chat].selection.identity().clone();
    assert_eq!(chosen.origin, "project");
    let store = root.selected[&chat].package.clone();
    let before = (root.snapshot(), tree(&f.root));
    let read = root.read_chosen_text(Some(&chat), &chosen_target(&chosen.revision));
    assert_read(&read, &chosen, &store);
    assert_eq!(read["text"], edited.as_str());
    assert_eq!((root.snapshot(), tree(&f.root)), before, "the read changes nothing");
    // One byte changed in the revision store: refused, no text.
    let mut changed = std::fs::read(store.join("WORKFLOW.md")).unwrap();
    changed[0] ^= 0x01;
    std::fs::write(store.join("WORKFLOW.md"), &changed).unwrap();
    assert_refused(&root.read_chosen_text(Some(&chat), &chosen_target(&chosen.revision)), "could not read this revision's files");
    // The published copy is never the authority: a matching store reads; the published copy's edits do not reach it.
    changed[0] ^= 0x01;
    std::fs::write(store.join("WORKFLOW.md"), &changed).unwrap();
    let published = f.root.join(".chirality/workflows/coordinated-knowledge-work");
    assert!(published.is_dir() && store != published, "registration keeps a published copy apart from the revision store");
    std::fs::write(published.join("WORKFLOW.md"), "edited published copy").unwrap();
    let read = root.read_chosen_text(Some(&chat), &chosen_target(&chosen.revision));
    assert_eq!(read["text"], edited.as_str(), "{read}");
    root.selected.clear();
    assert_refused(&root.read_chosen_text(Some(&chat), &chosen_target(&chosen.revision)), "no workflow is chosen");
}

#[test]
fn chosen_text_of_a_user_library_revision() {
    let base = std::fs::canonicalize(std::env::temp_dir()).unwrap().join(crate::util::opaque_id("user-library-").unwrap());
    std::fs::create_dir(&base).unwrap();
    struct Gone(std::path::PathBuf);
    impl Drop for Gone { fn drop(&mut self) { let _ = std::fs::remove_dir_all(&self.0); } }
    let _gone = Gone(base.clone());
    let files: std::collections::BTreeMap<String, Vec<u8>> = [
        ("WORKFLOW.md".to_owned(), "# A user workflow\n\nRead the brief.\n".as_bytes().to_vec()),
        ("notes/extra.txt".to_owned(), b"twelve bytes".to_vec()),
    ].into();
    let snapshot = crate::workflow_workspace::Snapshot::from_files(files).unwrap();
    let store = base.join("revision");
    snapshot.publish_new(&store).unwrap();
    let identity = snapshot.identity("user", base.to_str().unwrap(), "user-flow", None).unwrap();
    let selection = crate::workflow_workspace::Selection::synthetic_registered(snapshot, identity.clone()).unwrap();
    let mut root = WorkflowRootSession::default();
    let chat = crate::workflow_selection::Chat { source: "fixture source".into(), thread: "thread".into() };
    root.selected.insert(chat.clone(), WorkflowSelectionState { reference: "workflow-selection:fixture".into(), selection, package: store.clone(), selected_at: "fixture".into(), replaces: None });
    let before = (root.snapshot(), tree(&base));
    let read = root.read_chosen_text(Some(&chat), &chosen_target(&identity.revision));
    assert_read(&read, &identity, &store);
    assert_eq!(read["identity"]["origin"], "user");
    assert_eq!(read["files"], json!([{"path":"notes/extra.txt","bytes":12}]));
    assert_eq!((root.snapshot(), tree(&base)), before, "the read changes nothing");
    // Another file of the revision changed: its identity covers every file, so no text.
    std::fs::write(store.join("notes/extra.txt"), b"twelve byteS").unwrap();
    assert_refused(&root.read_chosen_text(Some(&chat), &chosen_target(&identity.revision)), "could not read this revision's files");
}

#[test]
fn unknown_targets_are_refused_before_anything_is_read() {
    assert!(crate::workflow_text_read::kind_known(&Target { kind: "path".into(), name: Some("/etc".into()), revision: "r".into() }).is_err());
    assert!(crate::workflow_text_read::kind_known(&included_target(BUNDLED, "r")).is_ok());
    assert!(crate::workflow_text_read::kind_known(&chosen_target("r")).is_ok());
    // The target takes exactly its three fields; a caller cannot add a path.
    assert!(serde_json::from_value::<Target>(json!({"kind":"included","name":BUNDLED,"revision":"r","path":"/etc"})).is_err());
    assert!(serde_json::from_value::<Target>(json!({"kind":"selection","revision":"r"})).is_ok());
}
