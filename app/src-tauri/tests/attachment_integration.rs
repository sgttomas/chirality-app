//! Actual native-selection command helpers/private producer; no native picker,
//! supplier/model/act/project acceptance or complete submission witness.
#[allow(dead_code)]
mod common;
use chirality_app_v4_lib::{
    attachments,
    runtime_session::{
        reconfirm_attachment_source, select_attachment_source,
        select_attachment_source_starting_in, AttachmentSelectionSession,
    },
};
use common::ScratchDirectory;
use serde_json::{json, Value};
use std::{
    cell::Cell,
    path::{Path, PathBuf},
    sync::Mutex,
};
fn state(project: Option<PathBuf>) -> Mutex<Result<AttachmentSelectionSession, String>> {
    Mutex::new(AttachmentSelectionSession::new(project))
}
fn view(state: &Mutex<Result<AttachmentSelectionSession, String>>) -> Value {
    state.lock().unwrap().as_ref().unwrap().snapshot()
}
fn refs(view: &Value) -> Vec<String> {
    view["selections"]
        .as_array()
        .unwrap()
        .iter()
        .map(|row| {
            row["selection"]["selectionRef"]
                .as_str()
                .unwrap()
                .to_owned()
        })
        .collect()
}
fn file(ws: &Path, name: &str, text: &[u8]) -> PathBuf {
    let path = ws.join(name);
    std::fs::write(&path, text).unwrap();
    path
}
fn add(state: &Mutex<Result<AttachmentSelectionSession, String>>, path: PathBuf) -> Value {
    let current = view(state);
    select_attachment_source(
        state,
        current["ownerRef"].as_str().unwrap(),
        current["listRevision"].as_u64().unwrap(),
        || Ok(Some(path)),
    )
    .unwrap()
}
#[test]
fn native_pick_private_handles_order_exact_unchanged_inputs_and_distinct_app_root() {
    let ws = ScratchDirectory::new("attachment-selection");
    let project = ws.join("explicit-project");
    std::fs::create_dir(&project).unwrap();
    let session = state(Some(project.clone()));
    let path = file(
        &ws,
        "actual-source.txt",
        "  exact source\n包括\n".as_bytes(),
    );
    let before = view(&session);
    let picks = Cell::new(0);
    let selected =
        select_attachment_source(&session, before["ownerRef"].as_str().unwrap(), 0, || {
            picks.set(picks.get() + 1);
            Ok(Some(path.clone()))
        })
        .unwrap();
    assert_eq!(picks.get(), 1);
    assert_eq!(selected["listRevision"], 1);
    assert_eq!(
        selected["selections"][0]["selection"]["standing"],
        "selected; not sent"
    );
    assert_eq!(
        selected["launchAppProjectObservation"]["nativeRoot"],
        attachments::native_path_identity(&project)
    );
    let order = refs(&selected);
    let submission = attachments::new_submission_ref().unwrap();
    let prepared = session
        .lock()
        .unwrap()
        .as_ref()
        .unwrap()
        .prepare_selected(
            selected["ownerRef"].as_str().unwrap(),
            1,
            &order,
            &submission,
            "2026-10-05T00:00:00Z",
        )
        .unwrap();
    assert_eq!(prepared.native_inputs().len(), 1);
    assert!(prepared.native_inputs()[0]["text"]
        .as_str()
        .unwrap()
        .ends_with("  exact source\n包括\n"));
    assert_eq!(
        prepared.supply_records()[0]["identityAtSelection"],
        prepared.supply_records()[0]["identityAtSubmission"]
    );
    assert_eq!(prepared.supply_records()[0]["turnRef"], submission);
    assert_eq!(
        prepared.supply_records()[0]["providerAdoption"],
        "not observed"
    );
    assert_eq!(view(&session), selected);
    assert_eq!(picks.get(), 1);
}
#[test]
fn remove_reorder_stale_cross_owner_unknown_and_subset_handles_never_construct_sources() {
    let ws = ScratchDirectory::new("attachment-order");
    let session = state(None);
    add(&session, file(&ws, "one.txt", b"one"));
    let selected = add(&session, file(&ws, "two.txt", b"two"));
    let original = refs(&selected);
    let owner = selected["ownerRef"].as_str().unwrap();
    let rev = selected["listRevision"].as_u64().unwrap();
    let other = state(None);
    let foreign = view(&other);
    let mut guard = session.lock().unwrap();
    let current = guard.as_mut().unwrap();
    for order in [
        vec![original[0].clone()],
        vec![original[0].clone(), original[0].clone()],
        vec![original[0].clone(), "JS-authored-selected-body".into()],
    ] {
        assert!(current.reorder(owner, rev, &order).is_err());
    }
    assert!(current
        .remove(foreign["ownerRef"].as_str().unwrap(), rev, &original[0])
        .is_err());
    assert!(current.remove(owner, rev - 1, &original[0]).is_err());
    assert!(current.remove(owner, rev, "unknown").is_err());
    assert!(current
        .prepare_selected(
            owner,
            rev,
            &original[..1],
            &attachments::new_submission_ref().unwrap(),
            "now"
        )
        .is_err());
    assert_eq!(current.snapshot(), selected);
    let mut reversed = original.clone();
    reversed.reverse();
    let reordered = current.reorder(owner, rev, &reversed).unwrap();
    assert_eq!(refs(&reordered), reversed);
    let removed = current.remove(owner, rev + 1, &original[0]).unwrap();
    assert_eq!(refs(&removed), vec![original[1].clone()]);
}
#[test]
fn whole_list_drift_holds_original_until_explicit_private_path_confirmation() {
    let ws = ScratchDirectory::new("attachment-drift");
    let session = state(None);
    let path = file(&ws, "source.txt", b"old bytes");
    let original = add(&session, path.clone());
    let owner = original["ownerRef"].as_str().unwrap();
    let reference = refs(&original)[0].clone();
    std::fs::write(&path, b"current bytes").unwrap();
    assert!(session
        .lock()
        .unwrap()
        .as_ref()
        .unwrap()
        .prepare_selected(
            owner,
            1,
            &refs(&original),
            &attachments::new_submission_ref().unwrap(),
            "now"
        )
        .unwrap_err()
        .contains("changed"));
    assert_eq!(view(&session), original);
    let cancelled = reconfirm_attachment_source(&session, owner, 1, &reference, |comparison| {
        assert_eq!(
            comparison["oldSelection"],
            original["selections"][0]["selection"]
        );
        assert_ne!(
            comparison["oldSelection"]["identityAtSelection"],
            comparison["tentativeSelection"]["identityAtSelection"]
        );
        false
    })
    .unwrap();
    assert_eq!(refs(&cancelled), refs(&original));
    assert_eq!(cancelled["listRevision"], 1);
    let refreshed = reconfirm_attachment_source(&session, owner, 1, &reference, |_| true).unwrap();
    assert_eq!(refreshed["listRevision"], 2);
    assert_ne!(refs(&refreshed), refs(&original));
    let prepared = session
        .lock()
        .unwrap()
        .as_ref()
        .unwrap()
        .prepare_selected(
            owner,
            2,
            &refs(&refreshed),
            &attachments::new_submission_ref().unwrap(),
            "now",
        )
        .unwrap();
    assert!(prepared.native_inputs()[0]["text"]
        .as_str()
        .unwrap()
        .ends_with("current bytes"));
}
#[test]
fn invalid_carrier_cancel_failure_and_reentrant_native_pick_keep_existing_list() {
    let ws = ScratchDirectory::new("attachment-holds");
    let session = state(None);
    let original = add(&session, file(&ws, "good.txt", b"good"));
    let owner = original["ownerRef"].as_str().unwrap();
    for (name, bytes) in [
        ("image.png", b"image".as_slice()),
        ("nul.txt", b"a\0b".as_slice()),
        ("invalid.txt", &[255u8][..]),
    ] {
        let selected =
            select_attachment_source(&session, owner, 1, || Ok(Some(file(&ws, name, bytes))))
                .unwrap();
        assert_eq!(selected["operation"]["state"], "held");
        assert_eq!(selected["selections"], original["selections"]);
        assert_eq!(selected["listRevision"], 1);
    }
    let cancelled = select_attachment_source(&session, owner, 1, || Ok(None)).unwrap();
    assert_eq!(cancelled["selections"], original["selections"]);
    assert!(select_attachment_source(&session, owner, 1, || Err(
        "native picker unavailable".into()
    ))
    .is_err());
    assert_eq!(view(&session)["selections"], original["selections"]);
    let cancelled = select_attachment_source(&session, owner, 1, || {
        assert!(select_attachment_source(&session, owner, 1, || panic!(
            "reentrant picker must not run"
        ))
        .is_err());
        Ok(None)
    })
    .unwrap();
    assert_eq!(cancelled["selections"], original["selections"]);
}

#[test]
fn explicit_project_absence_and_access_choice_never_inherit_cwd_home_or_canonical_sentinel() {
    use chirality_app_v4_lib::{
        access::ConversationSelection, runtime_session::freeze_configured_project,
    };
    let ws = ScratchDirectory::new("attachment-context");
    let project = ws.join("App P / 家");
    let native_cwd = ws.join("native-Q");
    let context = freeze_configured_project(Some(&project)).unwrap();
    assert_eq!(context.reference(), project.to_str());
    assert_ne!(context.reference(), native_cwd.to_str());
    let none = freeze_configured_project(None).unwrap();
    assert!(none.reference().is_none());
    let mut choice =
        ConversationSelection::new_explicit("explicit-unknown", none.reference()).unwrap();
    assert!(choice.canonical_record().is_none());
    assert!(choice
        .offer_last("chatgpt-account", "provider", "model")
        .is_err());
    let generation =
        json!({"home":"opaque-supplier-root","appSession":"test-session","spawnCounter":1});
    assert!(choice.start_params(&generation, "account", false).is_err());
    choice
        .choose("chatgpt-account", "chosen-provider", "chosen-model", false)
        .unwrap();
    choice.start_params(&generation, "account", false).unwrap();
    assert_eq!(choice.recovery_home(), Some("H-acct"));
    assert!(choice.project().is_none());
    assert!(choice.canonical_record().is_none());
    assert_eq!(choice.snapshot()["state"], "starting");
    let known = ConversationSelection::new_explicit("known", context.reference()).unwrap();
    assert_eq!(
        known.canonical_record().unwrap()["project"],
        project.to_str().unwrap()
    );
}

/// The folder the panel is asked to start in for one selection, and the view
/// that selection returns. The panel itself is the injected callback.
fn starting_folder_asked(
    state: &Mutex<Result<AttachmentSelectionSession, String>>,
    chosen: PathBuf,
) -> (Option<PathBuf>, Value) {
    let current = view(state);
    let mut asked = None;
    let mut calls = 0;
    let selected = select_attachment_source_starting_in(
        state,
        current["ownerRef"].as_str().unwrap(),
        current["listRevision"].as_u64().unwrap(),
        |start| {
            calls += 1;
            asked = start.map(Path::to_path_buf);
            Ok(Some(chosen))
        },
    )
    .unwrap();
    assert_eq!(calls, 1, "the panel opens exactly once, whatever the start");
    (asked, selected)
}

#[test]
fn attachment_panel_starts_in_the_known_project_folder_and_otherwise_opens_as_before() {
    let ws = ScratchDirectory::new("attachment-panel-start");
    let project = ws.join("invented project P");
    let elsewhere = ws.join("invented folder outside P");
    std::fs::create_dir(&project).unwrap();
    std::fs::create_dir(&elsewhere).unwrap();

    // Known project folder: the panel is asked to start there, and the person
    // may still select a file anywhere (here outside the project).
    let session = state(Some(project.clone()));
    let outside = file(&elsewhere, "outside.txt", b"outside");
    let (asked, selected) = starting_folder_asked(&session, outside.clone());
    assert_eq!(asked.as_deref(), Some(project.as_path()));
    assert_eq!(selected["operation"]["state"], "selected-not-sent");
    assert_eq!(selected["listRevision"], 1);
    // The last selected source lies elsewhere; the next panel still starts in
    // the project the attachments are for, not where the last file came from.
    let (asked, selected) = starting_folder_asked(&session, file(&project, "inside.txt", b"in"));
    assert_eq!(asked.as_deref(), Some(project.as_path()));
    assert_eq!(selected["selections"].as_array().unwrap().len(), 2);

    // Unknown project: no starting folder, the selection proceeds as before.
    let session = state(None);
    let (asked, selected) = starting_folder_asked(&session, outside.clone());
    assert_eq!(asked, None);
    assert_eq!(selected["operation"]["state"], "selected-not-sent");

    // Project folder no longer exists: no starting folder, no refusal.
    let vanished = ws.join("invented project removed");
    std::fs::create_dir(&vanished).unwrap();
    let session = state(Some(vanished.clone()));
    std::fs::remove_dir(&vanished).unwrap();
    let (asked, selected) = starting_folder_asked(&session, outside.clone());
    assert_eq!(asked, None);
    assert_eq!(selected["operation"]["state"], "selected-not-sent");

    // Project path is now a file, not a folder: no starting folder, no refusal.
    let not_folder = file(&ws, "invented project now a file", b"not a folder");
    let session = state(Some(not_folder));
    let (asked, selected) = starting_folder_asked(&session, outside);
    assert_eq!(asked, None);
    assert_eq!(selected["operation"]["state"], "selected-not-sent");
}

#[test]
fn attachment_panel_starting_folder_leaves_owner_revision_admission_and_holds_unchanged() {
    let ws = ScratchDirectory::new("attachment-panel-start-custody");
    let project = ws.join("invented project P");
    std::fs::create_dir(&project).unwrap();
    let session = state(Some(project.clone()));
    let original = add(&session, file(&project, "good.txt", b"good"));
    let owner = original["ownerRef"].as_str().unwrap();
    // A stale revision or a foreign owner is refused before any panel opens.
    for (who, revision) in [(owner, 0), ("attachment-owner:foreign", 1)] {
        assert!(select_attachment_source_starting_in(&session, who, revision, |_| panic!(
            "refused selection must not open the panel"
        ))
        .is_err());
    }
    // A selection already in progress refuses a second panel.
    let cancelled = select_attachment_source_starting_in(&session, owner, 1, |start| {
        assert_eq!(start, Some(project.as_path()));
        assert!(select_attachment_source_starting_in(&session, owner, 1, |_| panic!(
            "reentrant panel must not open"
        ))
        .is_err());
        Ok(None)
    })
    .unwrap();
    assert_eq!(cancelled["operation"]["state"], "cancelled");
    assert_eq!(cancelled["selections"], original["selections"]);
    // A file the checks after the panel hold is still held.
    let held = select_attachment_source_starting_in(&session, owner, 1, |start| {
        assert_eq!(start, Some(project.as_path()));
        Ok(Some(file(&project, "nul.txt", b"a\0b")))
    })
    .unwrap();
    assert_eq!(held["operation"]["state"], "held");
    assert_eq!(held["selections"], original["selections"]);
    assert_eq!(held["listRevision"], 1);
}
