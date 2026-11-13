use super::*;

fn routing_fixture() -> (OwnStore, PathBuf, PathBuf, String) {
    let own = OwnStore::new();
    let root = folder("payload-census-project-");
    let record = records::append(
        &root.join(".chirality/records/acts/in-place.jsonl"),
        "evidence_limit",
        &APP_WRITER,
        body("in place"),
    )
    .unwrap();
    let dir = attach(&root, true).unwrap().dir.unwrap();
    (own, root, dir, record["recordId"].as_str().unwrap().into())
}

fn unknown_case(kind: &str) {
    let (_own, root, dir, _) = routing_fixture();
    let acts = dir.join("acts");
    std::fs::create_dir_all(&acts).unwrap();
    let member = acts.join(format!("{}.jsonl", storage::key("invented")));
    let path = match kind {
        "unrecognised" => {
            let p = acts.join("unrecognised-member");
            std::fs::write(&p, b"unknown").unwrap();
            p
        }
        "symlink" => {
            std::os::unix::fs::symlink(root.join("absent"), &member).unwrap();
            member
        }
        "hard link" => {
            let outside = root.join("outside");
            std::fs::write(&outside, b"corrupt final").unwrap();
            std::fs::hard_link(outside, &member).unwrap();
            member
        }
        "unreadable" => acts.clone(),
        "publication" => {
            let p = acts.join(format!(
                ".{}.{}.tmp",
                member.file_name().unwrap().to_str().unwrap(),
                crate::util::opaque_id("").unwrap()
            ));
            std::fs::write(&p, b"partial bytes").unwrap();
            p
        }
        _ => unreachable!(),
    };
    let inspect = || {
        let read = readable_home(&root);
        let state = status(Some(&root));
        let export = crate::records_export::export(
            &root,
            &root
                .parent()
                .unwrap()
                .join(crate::util::opaque_id("refused-export-").unwrap()),
        );
        let cause = path.display().to_string();
        assert!(
            read.as_ref()
                .is_err_and(|e| e.contains("unknown") && e.contains(&cause)),
            "{kind}: {read:?}"
        );
        assert_eq!(state["project"]["state"], "unavailable", "{kind}: {state}");
        assert!(
            state["project"]["error"].as_str().unwrap().contains(&cause),
            "{kind}: {state}"
        );
        assert!(
            export.as_ref().is_err_and(|e| e.contains(&cause)),
            "{kind}: {export:?}"
        );
        let (entries, limits) = storage::read_all(&root);
        assert!(
            entries.is_empty() && limits.iter().any(|e| e.contains(&cause)),
            "{kind}: {entries:?}, {limits:?}"
        );
    };
    if kind == "unreadable" {
        unsearchable(&acts, inspect);
    } else {
        inspect();
    }
    std::fs::remove_dir_all(root).unwrap();
}

#[test]
fn records_store_routing_unknown_unrecognised_member() {
    unknown_case("unrecognised");
}
#[test]
fn records_store_routing_unknown_symlink() {
    unknown_case("symlink");
}
#[test]
fn records_store_routing_unknown_hard_linked_final() {
    unknown_case("hard link");
}
#[test]
fn records_store_routing_unknown_unreadable_folder() {
    unknown_case("unreadable");
}
#[test]
fn records_store_routing_unknown_generic_publication() {
    unknown_case("publication");
}

#[test]
fn records_store_routing_only_validated_controls_and_each_exact_preparation_keeps_in_place_history()
{
    for name in [
        ".writer.lock",
        "captures/.capture.lock",
        "..writer.lock.11111111-1111-4111-8111-111111111111.tmp",
        "captures/..capture.lock.11111111-1111-4111-8111-111111111111.tmp",
    ] {
        let (_own, root, dir, id) = routing_fixture();
        let path = dir.join(name);
        std::fs::create_dir_all(path.parent().unwrap()).unwrap();
        std::fs::write(&path, b"").unwrap();
        let (read, limits) = storage::read_all(&root);
        assert!(
            read.iter().any(|r| r["recordId"] == id),
            "{name}: {read:?}, {limits:?}"
        );
        assert_eq!(
            status(Some(&root))["project"]["importNeeded"],
            true,
            "{name}"
        );
        assert!(!store_holds(&dir).unwrap(), "{name}");
        std::fs::remove_dir_all(root).unwrap();
    }
}

#[test]
fn records_store_routing_nonempty_control_temporary_is_unknown() {
    let (_own, root, dir, _) = routing_fixture();
    std::fs::create_dir_all(dir.join("captures")).unwrap();
    let path = dir.join("captures/..capture.lock.11111111-1111-4111-8111-111111111111.tmp");
    std::fs::write(&path, b"not an empty owning control").unwrap();
    assert!(store_holds(&dir).is_err(), "nonempty control is ambiguous");
    assert!(crate::records_package::payload_inventory(&dir).is_err());
    std::fs::remove_dir_all(root).unwrap();
}

#[test]
fn records_store_routing_corrupt_final_is_still_record_evidence() {
    let (_own, root, dir, _) = routing_fixture();
    std::fs::create_dir_all(dir.join("acts")).unwrap();
    std::fs::write(
        dir.join("acts")
            .join(format!("{}.jsonl", storage::key("corrupt"))),
        b"corrupt final\n",
    )
    .unwrap();
    assert!(store_holds(&dir).unwrap());
    let (read, limits) = storage::read_all(&root);
    assert!(
        read.is_empty() && !limits.is_empty(),
        "{read:?}, {limits:?}"
    );
    std::fs::remove_dir_all(root).unwrap();
}

#[test]
fn records_store_routing_connector_attempt_is_retained_without_hiding_in_place_history() {
    let (_own, root, dir, id) = routing_fixture();
    std::fs::create_dir_all(dir.join("connectors/route-accounts")).unwrap();
    let relative = format!(
        "connectors/route-accounts/.route-{}.tmp",
        crate::util::opaque_id("").unwrap()
    );
    std::fs::write(
        dir.join(&relative),
        b"invented interrupted connector attempt\0\xff",
    )
    .unwrap();
    let (read, limits) = storage::read_all(&root);
    assert!(
        read.iter().any(|r| r["recordId"] == id),
        "{read:?}, {limits:?}"
    );
    assert_eq!(status(Some(&root))["project"]["importNeeded"], true);
    assert!(crate::records_export::export(&root, &root.join("not-exported")).is_err());
    // With no in-place history to omit, retained attempt evidence can travel.
    std::fs::remove_dir_all(root.join(".chirality/records")).unwrap();
    let output = folder("connector-attempt-export-");
    let target = output.join("bag");
    crate::records_export::export(&root, &target).unwrap();
    assert_eq!(
        std::fs::read(target.join("data").join(relative)).unwrap(),
        b"invented interrupted connector attempt\0\xff"
    );
    assert!(crate::records_export::verify(&target).is_ok());
    std::fs::remove_dir_all(output).unwrap();
    std::fs::remove_dir_all(root).unwrap();
}
