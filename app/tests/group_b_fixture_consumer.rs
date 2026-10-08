//! Offline fixture preflight through production consumers; no act or registration double.
use crate::workflow_declaration::{self, Reading};
use crate::workflow_workspace::{collisions, DraftKey, Review, Snapshot};
use std::path::PathBuf;

const NAME: &str = "invented-pipe-inventory";
fn fixture(variant: &str) -> Snapshot {
    Snapshot::capture(&PathBuf::from(env!("CARGO_MANIFEST_DIR"))
        .join("../examination/standalone/fixtures").join(variant).join(NAME)).unwrap()
}
fn review(snapshot: &Snapshot, live: &Snapshot, name: &str) -> Result<Review, String> {
    Review::open(snapshot.clone(), live, snapshot.revision(),
        snapshot.identity("project", "invented-project", name, None).unwrap(), None,
        DraftKey { draft_location: "project".into(), draft_root: "invented-draft-root".into(), name: name.into() },
        "offline-review-only".into())
}
#[test]
fn group_b_fixture_all_declarations_reach_maintained_reader_and_review() {
    for variant in ["revision-1", "revision-2", "revision-3", "user-collision"] {
        let snapshot = fixture(variant);
        assert!(snapshot.hygiene_findings().is_empty());
        let declaration = workflow_declaration::read(snapshot.workflow_text()).unwrap();
        assert_eq!(declaration.reading, Reading::Recognized, "{variant}");
        assert!(declaration.findings.is_empty(), "{variant}: {:?}", declaration.findings);
        for category in ["expected_inputs", "required_tools", "returned_outputs", "returned_evidence"] {
            assert_eq!(declaration.categories[category], Reading::Recognized);
        }
        assert!(declaration.elements.values().flatten().all(|e| e.reading == Reading::Recognized), "{variant}: {:?}", declaration.elements);
        let opened = review(&snapshot, &snapshot, NAME).unwrap();
        assert!(opened.is_current(&snapshot, None));
        assert_eq!(opened.snapshot().revision(), snapshot.revision());
    }
}
#[test]
fn group_b_fixture_collisions_keep_origin_and_revision_without_registration() {
    let first = fixture("revision-1");
    let old_bytes = first.files().clone();
    let first_identity = first.identity("project", "invented-project", NAME, None).unwrap();
    let other = fixture("user-collision").identity("user", "invented-user", NAME, None).unwrap();
    let entries = vec![first_identity.clone(), other.clone()];
    let matches = collisions(NAME, &entries);
    assert_eq!(matches.len(), 2);
    assert_eq!(matches[0].origin, "project");
    assert_eq!(matches[1].origin, "user");
    assert!(!first_identity.same_slot(&other));
    let second = fixture("revision-2");
    let third = fixture("revision-3");
    assert_ne!(first.revision(), second.revision());
    assert_ne!(second.revision(), third.revision());
    assert_eq!(first.files(), &old_bytes);
    assert_eq!(first_identity.revision, fixture("revision-1").revision());
    // These are content identities only, not registered or runnable selections.
}
#[test]
fn group_b_fixture_stale_and_misnamed_reviews_refuse() {
    let first = fixture("revision-1");
    assert!(review(&first, &fixture("revision-2"), NAME).unwrap_err().contains("DS-6"));
    assert!(review(&first, &first, "wrong-name").unwrap_err().contains("HY-2"));
    let opened = review(&first, &first, NAME).unwrap();
    assert!(!opened.is_current(&fixture("revision-3"), None));
}
#[test]
fn group_b_fixture_duplicate_declaration_is_not_established() {
    let snapshot = fixture("revision-1");
    let block = workflow_declaration::extract(snapshot.workflow_text()).unwrap().unwrap();
    let doubled = format!("{}\n```workflow-declaration\n{}\n```\n", snapshot.workflow_text(), block);
    let read = workflow_declaration::read(&doubled).unwrap();
    assert_eq!(read.reading, Reading::NotEstablished);
    assert!(!read.findings.is_empty());
}

#[test]
fn group_b_fixture_compatibility_never_infers_tools_from_valid_draft() {
    use crate::execution_compatibility::{Check, Compatibility, Environment};
    let declaration = workflow_declaration::read(fixture("revision-1").workflow_text()).unwrap();
    let result = Compatibility::check(&declaration, &Environment::default());
    assert_eq!(result.result, Check::NotEstablished);
    assert_eq!(result.tools.len(), 1);
    assert!(result.checkpoints_are_guidance);
}
