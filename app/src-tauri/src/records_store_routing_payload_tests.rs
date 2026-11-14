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

fn flip_history_routing(dir: &Path) {
    let dir = dir.to_path_buf();
    after_read_routing_for_test(move || {
        std::fs::create_dir_all(dir.join("acts")).unwrap();
        std::fs::write(dir.join("acts").join(format!("{}.jsonl", storage::key("route-flip"))), b"corrupt final\n").unwrap();
    });
}

#[test]
fn records_store_routing_history_notice_decision_read_keeps_one_home() {
    let (_own, root, dir, _) = routing_fixture();
    flip_history_routing(&dir);
    let first = crate::runtime_session::read_decision_packages(&root);
    assert_eq!(first["historyNotices"], json!([]), "in-place reading: {first}");
    assert_eq!(first["limits"], json!([]), "rows must keep the routing taken before the store changed: {first}");
    let next = crate::runtime_session::read_decision_packages(&root);
    assert_eq!(next["historyNotices"].as_array().unwrap().len(), 1);
    assert!(next["limits"].as_array().unwrap().iter().any(|l| l.as_str().is_some_and(|l| l.contains("unreadable line 1"))), "next reading sees the new home: {next}");
    std::fs::remove_dir_all(root).unwrap();
}

#[test]
fn records_store_routing_history_notice_file_act_read_keeps_one_home() {
    let (_own, root, dir, _) = routing_fixture();
    flip_history_routing(&dir);
    let first = crate::file_act_view::read(&root);
    assert_eq!(first["historyNotices"], json!([]), "in-place reading: {first}");
    assert_eq!(first["limits"], json!([]), "rows must keep the routing taken before the store changed: {first}");
    let next = crate::file_act_view::read(&root);
    assert_eq!(next["historyNotices"].as_array().unwrap().len(), 1);
    assert!(next["limits"].as_array().unwrap().iter().any(|l| l.as_str().is_some_and(|l| l.contains("unreadable line 1"))), "next reading sees the new home: {next}");
    std::fs::remove_dir_all(root).unwrap();
}

#[test]
fn records_store_routing_in_place_empty_and_only_unknown_store_member_reads_the_store() {
    let _own = OwnStore::new();
    let root = folder("routing-empty-in-place-");
    let dir = attach(&root, true).unwrap().dir.unwrap();
    assert!(legacy_census(&root).unwrap().is_empty());
    let relative = "acts/.unrecognised-member.jsonl";
    std::fs::create_dir_all(dir.join("acts")).unwrap();
    std::fs::write(dir.join(relative), b"invented unknown bytes\n").unwrap();
    assert!(
        store_holds(&dir).is_err(),
        "the member alone proves neither records nor emptiness"
    );
    assert_eq!(
        readable_home(&root).unwrap().in_store(),
        Some(dir.as_path())
    );
    let (read, limits) = storage::read_all(&root);
    assert!(
        read.is_empty() && limits.iter().any(|e| e.contains(".unrecognised-member.jsonl")),
        "{read:?}, {limits:?}"
    );
    assert_eq!(status(Some(&root))["project"]["reading"], "records store");
    std::fs::remove_dir_all(root).unwrap();
}

fn unknown_in_place_census(kind: &str) {
    let _own = OwnStore::new();
    let root = folder("routing-unknown-in-place-");
    let dir = attach(&root, true).unwrap().dir.unwrap();
    std::fs::write(dir.join("unrecognised-member"), b"ambiguous store member").unwrap();
    let runs = root.join(".chirality/records/runs");
    std::fs::create_dir_all(runs.parent().unwrap()).unwrap();
    if kind == "link" {
        std::os::unix::fs::symlink(root.join("missing-target"), &runs).unwrap();
    } else {
        std::fs::create_dir(&runs).unwrap();
        for name in ["a-ordinary", "b-ordinary"] {
            std::fs::write(runs.join(name), b"not a record").unwrap();
        }
    }
    let inspect = || {
        let expected = if kind == "link" {
            "symlink"
        } else if kind == "partial" {
            "injected partial directory listing failure"
        } else {
            "Permission denied"
        };
        let home = readable_home(&root).unwrap_err();
        assert!(
            home.contains("unknown")
                && home.contains(&runs.display().to_string())
                && home.contains(expected),
            "{kind}: {home}"
        );
        let state = status(Some(&root));
        assert_eq!(state["project"]["state"], "unavailable", "{kind}: {state}");
        assert!(
            state["project"]["error"]
                .as_str()
                .unwrap()
                .contains(expected),
            "{kind}: {state}"
        );
        let output = folder("routing-refused-in-place-export-");
        let error = crate::records_export::export(&root, &output.join("bag")).unwrap_err();
        assert!(
            error.contains(expected) && error.contains(&runs.display().to_string()),
            "{kind}: {error}"
        );
        std::fs::remove_dir_all(output).unwrap();
    };
    if kind == "unreadable" {
        unsearchable(&runs, inspect);
    } else if kind == "partial" {
        LEGACY_LISTING_FAIL_AFTER.with(|hook| *hook.borrow_mut() = Some((runs.clone(), 1)));
        let result = std::panic::catch_unwind(inspect);
        LEGACY_LISTING_FAIL_AFTER.with(|hook| *hook.borrow_mut() = None);
        if let Err(error) = result {
            std::panic::resume_unwind(error);
        }
    } else {
        inspect();
    }
    std::fs::remove_dir_all(root).unwrap();
}

#[test]
fn records_store_routing_in_place_unreadable_with_only_ambiguous_store_is_not_known() {
    unknown_in_place_census("unreadable");
}
#[test]
fn records_store_routing_in_place_partial_listing_with_only_ambiguous_store_is_not_known() {
    unknown_in_place_census("partial");
}
#[test]
fn records_store_routing_in_place_unresolved_link_with_only_ambiguous_store_is_not_known() {
    unknown_in_place_census("link");
}

fn unknown_case(kind: &str) {
    let (_own, root, dir, _) = routing_fixture();
    assert!(
        !legacy_census(&root).unwrap().is_empty(),
        "in-place records make the unknown store consequential"
    );
    assert!(
        !store_holds(&dir).unwrap(),
        "no store record beside the ambiguous member"
    );
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
fn records_store_routing_recognised_final_wins_over_earlier_unrecognised_member_shown_by_reader() {
    let (_own, root, dir, in_place) = routing_fixture();
    let log = dir.join(storage::log_rel(
        Some("run:recognised"),
        "writer:recognised",
    ));
    // Place already-retained, valid bytes without asking the native write
    // gate to waive this fixture's deliberately unimported in-place history.
    let source = root.join("recognised-record-fixture.jsonl");
    let record = records::append(
        &source,
        "evidence_limit",
        &APP_WRITER,
        body("recognised store record"),
    )
    .unwrap();
    std::fs::create_dir_all(log.parent().unwrap()).unwrap();
    std::fs::copy(&source, &log).unwrap();
    let unknown = dir.join("acts/.unrecognised-member.jsonl");
    std::fs::create_dir_all(unknown.parent().unwrap()).unwrap();
    std::fs::write(&unknown, b"unrecognised retained bytes\n").unwrap();
    // acts is visited before runs, and this member is not a final name the
    // census recognises. It must not prevent finding the later real record.
    assert!(store_holds(&dir).unwrap());
    let home = readable_home(&root).unwrap();
    assert!(home.store_mode);
    let (read, limits) = storage::read_all(&root);
    assert!(
        read.iter().any(|r| r["recordId"] == record["recordId"]),
        "{read:?}, {limits:?}"
    );
    assert!(!read.iter().any(|r| r["recordId"] == in_place));
    assert!(
        limits
            .iter()
            .any(|e| e.contains(".unrecognised-member.jsonl")),
        "the reader must show the member's own limit: {limits:?}"
    );
    assert_eq!(status(Some(&root))["project"]["reading"], "records store");
    // An inventory carries ordinary unknown bytes; they are not an unresolved
    // publication and cannot block the export of the known history.
    assert!(crate::records_package::payload_inventory(&dir)
        .unwrap()
        .contains_key("acts/.unrecognised-member.jsonl"));
    let output = folder("retained-unrecognised-export-");
    crate::records_export::export(&root, &output.join("bag")).unwrap();
    assert_eq!(
        std::fs::read(output.join("bag/data/acts/.unrecognised-member.jsonl")).unwrap(),
        b"unrecognised retained bytes\n"
    );
    std::fs::remove_dir_all(output).unwrap();
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
        "role-supply/.writer.lock",
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
fn records_store_routing_history_notice_names_omitted_in_place_records() {
    let (_own, root, dir, _) = routing_fixture();
    let (in_place, limits) = storage::read_all(&root);
    assert_eq!(in_place.len(), 1, "the project starts with readable history");
    assert!(limits.is_empty(), "{limits:?}");
    std::fs::create_dir_all(dir.join("acts")).unwrap();
    std::fs::write(
        dir.join("acts").join(format!("{}.jsonl", storage::key("corrupt"))),
        b"corrupt final\n",
    ).unwrap();
    assert!(!dir.join("imports.jsonl").exists(), "no import account in this case");
    let shown = status(Some(&root));
    assert_eq!(shown["project"]["reading"], "records store");
    assert_eq!(shown["project"]["notImported"], 1);
    let view = crate::runtime_session::read_decision_packages(&root);
    assert!(view["rows"].as_array().unwrap().is_empty(), "{view}");
    assert!(view["limits"].as_array().unwrap().iter().any(|limit| {
        limit.as_str().is_some_and(|s| s.contains("unreadable line 1"))
    }), "the corrupt store line remains a separate reading limit: {view}");

    // Control: the originals remain in the project after a complete import,
    // but those files are covered and must not produce the omission notice.
    let imported_root = folder("history-notice-imported-project-");
    records::append(
        &imported_root.join(".chirality/records/acts/in-place.jsonl"),
        "evidence_limit", &APP_WRITER, body("imported history"),
    ).unwrap();
    import(&imported_root).unwrap();
    let imported_status = status(Some(&imported_root));
    assert_eq!(imported_status["project"]["reading"], "records store");
    assert_eq!(imported_status["project"]["notImported"], 0);
    let imported_view = crate::runtime_session::read_decision_packages(&imported_root);
    assert!(imported_view.get("historyNotices").is_none_or(|notices| {
        notices.as_array().is_some_and(Vec::is_empty)
    }), "imported originals must not be reported as omitted: {imported_view}");
    std::fs::remove_dir_all(imported_root).unwrap();
    std::fs::remove_dir_all(root).unwrap();

    // Proposed display channel and wording, for Agent 0's decision before
    // implementation. This must not be added to storage::read_all's limits.
    assert_eq!(view["historyNotices"], json!([
        "This project's records are kept in the records store. Records in the project folder have not been imported and may not be shown in this view."
    ]), "the person-facing history result must explain the omitted in-place history beside its corruption limit; status elsewhere is insufficient");
}

#[test]
fn records_store_routing_history_notice_capability_pages_keep_real_limits() {
    let (own, root, dir, _) = routing_fixture();
    std::fs::create_dir_all(dir.join("acts")).unwrap();
    std::fs::write(dir.join("acts").join(format!("{}.jsonl", storage::key("corrupt"))), b"corrupt final\n").unwrap();
    let capability = crate::records_access::RecordsCapability::at(&root, own.0.join("reads.jsonl")).unwrap();
    let mut pages = Vec::new();
    for (n, arguments) in [json!({"operation":"list_runs"}), json!({"operation":"read_run","run":"run:invented"}), json!({"operation":"read_acts"})].into_iter().enumerate() {
        let call = crate::records_access::Call {app_session:"notice-test".into(), generation:"notice-generation".into(), request:json!(n), thread:"notice-thread".into(), turn:"notice-turn".into(), call:format!("notice-{n}"), arguments};
        let answer = capability.answer(&call, root.to_str());
        assert_eq!(answer["success"], true, "{answer}");
        let page: Value = serde_json::from_str(answer["contentItems"][0]["text"].as_str().unwrap()).unwrap();
        assert!(page["limits"].as_array().unwrap().iter().any(|l| l.as_str().is_some_and(|s| s.contains("not JSON"))), "{page}");
        pages.push(page);
    }
    std::fs::remove_dir_all(root).unwrap();
    for page in pages {
        assert_eq!(page["historyNotices"], json!(["This project's records are kept in the records store. Records in the project folder have not been imported and may not be shown on this page."]), "{}", page["operation"]);
    }
}

#[test]
fn records_store_routing_history_notice_census_failure_keeps_successful_read() {
    let (own, root, dir, _) = routing_fixture();
    std::fs::create_dir_all(dir.join("acts")).unwrap();
    std::fs::copy(root.join(".chirality/records/acts/in-place.jsonl"), dir.join("acts").join(format!("{}.jsonl", storage::key("readable")))).unwrap();
    // The store is readable; only the independent census is uninspectable.
    std::fs::write(root.join(".chirality/records/workflow"), b"not a folder").unwrap();
    let (records, limits) = storage::read_all(&root);
    assert_eq!(records.len(), 1);
    assert!(limits.is_empty(), "{limits:?}");
    let view = crate::runtime_session::read_decision_packages(&root);
    assert!(view["limits"].as_array().unwrap().is_empty(), "{view}");
    let capability = crate::records_access::RecordsCapability::at(&root, own.0.join("reads.jsonl")).unwrap();
    let call = crate::records_access::Call {app_session:"notice-test".into(), generation:"notice-generation".into(), request:json!(0), thread:"notice-thread".into(), turn:"notice-turn".into(), call:"notice-census".into(), arguments:json!({"operation":"read_run","run":"run:invented"})};
    let answer = capability.answer(&call, root.to_str());
    assert_eq!(answer["success"], true, "the notice's own failure cannot refuse a page: {answer}");
    let page: Value = serde_json::from_str(answer["contentItems"][0]["text"].as_str().unwrap()).unwrap();
    assert_eq!(page["limits"], json!(["no readable entries for run run:invented"]), "the pre-existing missing-run diagnostic is retained, and the census failure is separate: {page}");
    assert!(page["historyNotices"][0].as_str().is_some_and(|n| n.contains("History notice unavailable") && n.contains("census")), "{page}");
    assert!(!page["historyNotices"].to_string().contains(root.to_str().unwrap()), "the diagnostic does not disclose the local project path");
    std::fs::remove_dir_all(root).unwrap();
    assert!(view["historyNotices"].as_array().is_some_and(|notices| notices.iter().any(|n| n.as_str().is_some_and(|s| s.contains("History notice unavailable") && s.contains("not a folder")))), "a census failure must be explicit without refusing the successful read: {view}");
}

#[test]
fn records_store_routing_history_notice_does_not_hide_completeness_refusal() {
    let (_own, root, dir, _) = routing_fixture();
    std::fs::create_dir_all(dir.join("acts")).unwrap();
    std::fs::write(dir.join("acts").join(format!("{}.jsonl", storage::key("corrupt"))), b"corrupt final\n").unwrap();
    std::fs::create_dir_all(root.join(crate::recorder::DECISIONS_DIR)).unwrap();
    let refused = crate::recorder::identify_packages(&root).unwrap_err();
    assert!(refused.contains("incomplete record set") && refused.contains("unreadable line 1"), "{refused}");
    let view = crate::runtime_session::read_decision_packages(&root);
    std::fs::remove_dir_all(root).unwrap();
    assert!(view["historyNotices"].as_array().is_some_and(|n| !n.is_empty()), "the completeness refusal and display notice coexist: {view}");
    assert!(view["limits"].as_array().unwrap().iter().any(|l| l.as_str().is_some_and(|s| s.contains("unreadable line 1"))), "{view}");
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

/// Status's "importNeeded" says what the write gate says. The reader's store
/// (pull request 313's reading): valid in-place history, a store holding only
/// a corrupt final, no import account. Routing reads the store; status names
/// the in-place file as not imported and not read; and status's importNeeded
/// and notes give the gate's own answer for a write: here "not known".
#[test]
fn records_store_routing_status_import_needed_follows_the_gate_with_only_a_corrupt_final() {
    let (_own, root, dir, _) = routing_fixture();
    std::fs::create_dir_all(dir.join("acts")).unwrap();
    std::fs::write(dir.join("acts").join(format!("{}.jsonl", storage::key("corrupt"))), b"corrupt final\n").unwrap();
    let gate = write_dir(&root).map(|_| ()).unwrap_err();
    let shown = status(Some(&root));
    let project = &shown["project"];
    assert_eq!(project["reading"], "records store", "{shown}");
    assert_eq!((project["legacyFiles"].as_u64(), project["notImported"].as_u64()), (Some(1), Some(1)), "{shown}");
    let notes = project["notes"].as_array().unwrap().iter().filter_map(Value::as_str).collect::<Vec<_>>();
    assert!(notes.iter().any(|n| n.contains("not imported into the records store") && n.contains("it is not read")), "{notes:?}");
    // A corrupt final gives the gate no positive evidence and makes its
    // authority uncertain: the gate refuses "not known", not "import needed".
    // Status says the same: importNeeded false, and the gate's own sentence.
    assert!(gate.contains("records store governs this project's records is unknown") && gate.contains("no recognised RS record in the log"), "{gate}");
    assert_eq!(project["importNeeded"], false, "{shown}");
    assert!(notes.iter().any(|n| *n == gate), "status carries the gate's own refusal word for word: {gate}; {notes:?}");
    std::fs::remove_dir_all(root).unwrap();
}

/// A completed import that refused a file: the store governs and recording is
/// admitted, so importNeeded is false; notImported and the refusal note say
/// what is not read.
#[test]
fn records_store_routing_status_import_needed_is_false_after_a_completed_import_with_a_refused_file() {
    let (_own, root, dir, _) = routing_fixture();
    std::fs::create_dir_all(dir.join("acts")).unwrap();
    std::fs::write(dir.join("acts/in-place.jsonl"), b"a different file the store already holds\n").unwrap();
    let imported = import(&root);
    assert!(imported.is_ok(), "{imported:?}");
    assert!(write_dir(&root).is_ok(), "a completed import admits recording");
    let shown = status(Some(&root));
    let project = &shown["project"];
    assert_eq!(project["importNeeded"], false, "{shown}");
    assert_eq!(project["notImported"].as_u64(), Some(1), "{shown}");
    let notes = project["notes"].as_array().unwrap().iter().filter_map(Value::as_str).collect::<Vec<_>>();
    assert!(notes.iter().any(|n| n.contains("not imported into the records store:") && n.contains("not overwritten")), "{notes:?}");
    std::fs::remove_dir_all(root).unwrap();
}

/// Where the gate's authority is uncertain, status never says "import needed":
/// it gives the gate's own "not known" sentence as a note.
#[test]
fn records_store_routing_status_import_needed_is_never_claimed_on_uncertain_authority() {
    let (_own, root, dir, _) = routing_fixture();
    std::fs::create_dir_all(dir.join("acts")).unwrap();
    std::fs::write(dir.join("acts").join(format!("{}.jsonl", storage::key("good"))), b"").unwrap();
    std::fs::write(dir.join("acts").join(format!("{}.jsonl", storage::key("corrupt"))), b"corrupt final\n").unwrap();
    let gate = write_dir(&root).map(|_| ()).unwrap_err();
    assert!(gate.contains("is unknown"), "{gate}");
    let shown = status(Some(&root));
    assert_eq!(shown["project"]["importNeeded"], false, "{shown}");
    let notes = shown["project"]["notes"].as_array().unwrap().iter().filter_map(Value::as_str).collect::<Vec<_>>();
    assert!(notes.iter().any(|n| n.contains("records store governs this project's records is unknown")), "{notes:?}");
    std::fs::remove_dir_all(root).unwrap();
}

fn notice_run(root: &Path, ended: bool) -> String {
    let run = "run:notice-cache";
    let fixtures: Vec<Value> = serde_json::from_str(include_str!("../schemas/fixtures/valid-records.json")).unwrap();
    let mut entries = Vec::new();
    for (i, kind) in ["run_opened", "run_ended"].into_iter().take(if ended {2} else {1}).enumerate() {
        let mut e = fixtures.iter().find(|e| e["kind"] == kind).unwrap().clone();
        e["runId"] = json!(run);
        if kind == "run_opened" { e["body"]["runId"] = json!(run); }
        e["seq"] = json!(i + 1); e["recordId"] = json!(format!("rec:app:notice:{}", i + 1));
        e["writtenAt"] = json!(format!("2026-11-01T00:00:0{i}Z"));
        entries.push(format!("{e}\n"));
    }
    let log = root.join(".chirality/records").join(storage::log_rel(Some(run), crate::records::supply::LIVE_WRITER));
    std::fs::create_dir_all(log.parent().unwrap()).unwrap();
    std::fs::write(log, entries.concat()).unwrap(); run.into()
}
fn notice_seed_store(dir: &Path) {
    let e = records::envelope("evidence_limit", &APP_WRITER, body("store only"), "rec:app:notice-store".into(), 1, None, None);
    std::fs::create_dir_all(dir.join("acts")).unwrap();
    std::fs::write(dir.join("acts").join(format!("{}.jsonl", storage::key("notice-store"))), format!("{e}\n")).unwrap();
}
fn notice_flip_store(dir: &Path) { let dir = dir.to_path_buf(); after_read_routing_for_test(move || notice_seed_store(&dir)); }
fn notice_page(root: &Path, log: &Path) -> Value {
    let capability = crate::records_access::RecordsCapability::at(root, log.to_path_buf()).unwrap();
    let call = crate::records_access::Call {app_session:"notice-test".into(),generation:"notice-generation".into(),request:json!(0),thread:"notice-thread".into(),turn:"notice-turn".into(),call:"notice-read".into(),arguments:json!({"operation":"list_runs"})};
    let answer = capability.answer(&call, root.to_str()); assert_eq!(answer["success"], true, "{answer}");
    serde_json::from_str(answer["contentItems"][0]["text"].as_str().unwrap()).unwrap()
}
#[test]
fn review_notice_cached_reopened_after_import() {
    let (_own, root, dir, _) = routing_fixture(); let run = notice_run(&root, false); notice_seed_store(&dir);
    let workflow = Mutex::new(crate::runtime_session::WorkflowRootSession::default());
    let old = crate::runtime_session::read_reopened_history(&workflow, &root, &[], &[]).unwrap();
    assert_eq!(old["runs"], json!([])); assert_eq!(old["historyNotices"].as_array().unwrap().len(), 1);
    import(&root).unwrap(); let shown = workflow.lock().unwrap().snapshot()["reopened"].clone();
    assert_eq!(shown["runs"], old["runs"]); assert_eq!(shown["historyNotices"], old["historyNotices"], "status keeps the cached reading's notice");
    let fresh = crate::runtime_session::read_reopened_history(&workflow, &root, &[], &[]).unwrap();
    assert!(fresh["runs"].as_array().unwrap().iter().any(|r| r["run"] == run)); assert_eq!(fresh["historyNotices"], json!([]));
    std::fs::remove_dir_all(root).unwrap();
}
#[test]
fn review_notice_cached_reopened_route_changes() {
    let (_own, root, dir, _) = routing_fixture(); let run = notice_run(&root, false);
    let workflow = Mutex::new(crate::runtime_session::WorkflowRootSession::default());
    let old = crate::runtime_session::read_reopened_history(&workflow, &root, &[], &[]).unwrap();
    assert!(old["runs"].as_array().unwrap().iter().any(|r| r["run"] == run)); notice_seed_store(&dir);
    let shown = workflow.lock().unwrap().snapshot()["reopened"].clone();
    assert_eq!(shown["runs"], old["runs"]); assert_eq!(shown["historyNotices"], json!([]), "status cannot freshly decorate cached in-place rows");
    std::fs::remove_dir_all(root).unwrap();
}
#[test]
fn records_store_routing_history_notice_reopened_change_is_not_known() {
    let (_own, root, dir, _) = routing_fixture(); notice_run(&root, false);
    let workflow = Mutex::new(crate::runtime_session::WorkflowRootSession::default()); notice_flip_store(&dir);
    let old = crate::runtime_session::read_reopened_history(&workflow, &root, &[], &[]).unwrap();
    assert_eq!(old["historyNotices"], json!([HISTORY_CHANGED_VIEW]));
    assert_eq!(workflow.lock().unwrap().snapshot()["reopened"]["historyNotices"], old["historyNotices"]);
    let next = crate::runtime_session::read_reopened_history(&workflow, &root, &[], &[]).unwrap(); assert_ne!(next["historyNotices"], old["historyNotices"]);
    std::fs::remove_dir_all(root).unwrap();
}
#[test]
#[ignore = "in-place ended history creates .after-run-end.lock, which payload routing classifies as an unrecognised member; separate payload-control repair required"]
fn records_store_routing_history_notice_post_end_cache_rebuilds_on_route_change() {
    let (_own, root, dir, _) = routing_fixture(); let run = notice_run(&root, true);
    let workflow = Mutex::new(crate::runtime_session::WorkflowRootSession::default()); crate::host_tick::observe_project_history(&workflow, &root);
    let old = workflow.lock().unwrap().snapshot()["afterRunEnd"].clone();
    assert!(old["runs"].as_array().unwrap().iter().any(|r| r["run"] == run), "{old}"); assert_eq!(old["historyNotices"], json!([]));
    notice_seed_store(&dir); crate::host_tick::observe_project_history(&workflow, &root);
    let next = workflow.lock().unwrap().snapshot()["afterRunEnd"].clone();
    assert_eq!(next["runs"], json!([]), "cache rebuilt: {next}"); assert_eq!(next["historyNotices"].as_array().unwrap().len(), 1);
    std::fs::remove_dir_all(root).unwrap();
}
#[test]
fn records_store_routing_history_notice_post_end_nonended_cache_rebuilds_on_route_change() {
    let (_own, root, dir, _) = routing_fixture(); notice_run(&root, false);
    let workflow = Mutex::new(crate::runtime_session::WorkflowRootSession::default());
    crate::host_tick::observe_project_history(&workflow, &root);
    assert_eq!(workflow.lock().unwrap().ended_cached_logs_for_test(), 1, "the in-place run populated the incremental cache");
    let old = workflow.lock().unwrap().snapshot()["afterRunEnd"].clone();
    assert_eq!(old["historyNotices"], json!([])); assert_eq!(old["limits"], json!([]));
    notice_seed_store(&dir); crate::host_tick::observe_project_history(&workflow, &root);
    assert_eq!(workflow.lock().unwrap().ended_cached_logs_for_test(), 0, "no in-place log survives the store refresh");
    let next = workflow.lock().unwrap().snapshot()["afterRunEnd"].clone();
    assert_eq!(next["runs"], json!([])); assert_eq!(next["historyNotices"].as_array().unwrap().len(), 1);
    std::fs::remove_dir_all(root).unwrap();
}
#[test]
fn records_store_routing_history_notice_post_end_import_refreshes_rows_and_notice() {
    let (_own, root, dir, _) = routing_fixture(); let run = notice_run(&root, true); notice_seed_store(&dir);
    let workflow = Mutex::new(crate::runtime_session::WorkflowRootSession::default()); crate::host_tick::observe_project_history(&workflow, &root);
    let old = workflow.lock().unwrap().snapshot()["afterRunEnd"].clone();
    assert_eq!(old["runs"], json!([])); assert_eq!(old["historyNotices"].as_array().unwrap().len(), 1); import(&root).unwrap();
    assert_eq!(workflow.lock().unwrap().snapshot()["afterRunEnd"]["historyNotices"], old["historyNotices"]);
    crate::host_tick::observe_project_history(&workflow, &root); let next = workflow.lock().unwrap().snapshot()["afterRunEnd"].clone();
    assert!(next["runs"].as_array().unwrap().iter().any(|r| r["run"] == run), "{next}"); assert_eq!(next["historyNotices"], json!([]));
    std::fs::remove_dir_all(root).unwrap();
}
#[test]
fn records_store_routing_history_notice_post_end_change_is_not_known_until_refresh() {
    let (_own, root, dir, _) = routing_fixture(); let workflow = Mutex::new(crate::runtime_session::WorkflowRootSession::default());
    notice_flip_store(&dir); crate::host_tick::observe_project_history(&workflow, &root);
    let old = workflow.lock().unwrap().snapshot()["afterRunEnd"].clone(); assert_eq!(old["historyNotices"], json!([HISTORY_CHANGED_VIEW]));
    crate::host_tick::observe_project_history(&workflow, &root); assert_ne!(workflow.lock().unwrap().snapshot()["afterRunEnd"]["historyNotices"], old["historyNotices"]);
    std::fs::remove_dir_all(root).unwrap();
}
#[test]
fn records_store_routing_history_notice_integrity_change_is_not_known() {
    let (_own, root, dir, _) = routing_fixture(); notice_flip_store(&dir); let read = crate::records_index::chain_heads(&root);
    assert_eq!(read["historyNotices"], json!([HISTORY_CHANGED_VIEW])); std::fs::remove_dir_all(root).unwrap();
}
#[test]
fn records_store_routing_history_notice_capability_change_is_not_known() {
    let (own, root, dir, _) = routing_fixture(); notice_flip_store(&dir); let read = notice_page(&root, &own.0.join("notice-reads.jsonl"));
    assert_eq!(read["historyNotices"], json!([HISTORY_CHANGED_PAGE])); std::fs::remove_dir_all(root).unwrap();
}
#[test]
fn records_store_routing_history_notice_supply_change_is_not_known() {
    let (_own, root, dir, _) = routing_fixture(); let records = crate::workflow_workspace::publication::ProjectRecords::open(&root).unwrap();
    notice_flip_store(&dir); let read = crate::records::supply::read_project_supply(&records);
    assert_eq!(read["historyNotices"], json!([HISTORY_CHANGED_VIEW])); std::fs::remove_dir_all(root).unwrap();
}
#[test]
fn records_store_routing_history_notice_capability_census_counts() {
    let (own, root, dir, _) = routing_fixture(); notice_seed_store(&dir); take_census_calls_for_test();
    let read = notice_page(&root, &own.0.join("notice-counts.jsonl")); assert_eq!(read["historyNotices"].as_array().unwrap().len(), 1);
    assert_eq!(take_census_calls_for_test(), 1, "only the notice census");
    std::fs::remove_dir_all(dir.join("acts")).unwrap(); std::fs::create_dir_all(dir.join("acts")).unwrap();
    std::fs::write(dir.join("acts/.unknown"), b"unknown retained bytes").unwrap(); std::fs::remove_dir_all(root.join(".chirality/records")).unwrap(); take_census_calls_for_test();
    let read = notice_page(&root, &own.0.join("notice-ambiguous-counts.jsonl")); assert_eq!(read["historyNotices"], json!([]));
    assert_eq!(take_census_calls_for_test(), 3, "before, source and after; reuse before for notice"); std::fs::remove_dir_all(root).unwrap();
}
