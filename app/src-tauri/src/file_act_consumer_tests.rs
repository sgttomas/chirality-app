//! Synthetic native adapter tests of actual Root ownership and production core.
use super::*;
use tauri_plugin_dialog::MessageDialogResult;
fn selected(
    state: &AppState,
    home: &Arc<runtime_session::HomeSession>,
    root: &std::path::Path,
    kind: act_control::FileActKind,
) -> String {
    std::fs::write(root.join("output.txt"), b"original reviewed bytes").unwrap();
    let (_, context) = file_act_observe(state, home).unwrap();
    let mut control = state.act.lock().unwrap();
    let preview = state
        .file_acts
        .lock()
        .unwrap()
        .compose(
            control.as_mut().unwrap(),
            &root.join("output.txt"),
            kind,
            "explicit scope",
            "explicit purpose",
            home.clone(),
            context,
        )
        .unwrap();
    preview["reference"].as_str().unwrap().into()
}
fn synthetic(state: &AppState, reference: &str, choice: &str, during: impl FnOnce()) -> Value {
    file_act_confirm_original(state, reference, |control, offer, observe| {
        control.synthetic_file_native(offer, observe, |text, kind| {
            assert!(text.contains("explicit scope"));
            assert!(text.contains("identity not verified"));
            during();
            MessageDialogResult::Custom(
                match choice {
                    "act" => kind.wording(),
                    "decline" => "Decline this act",
                    _ => "Cancel",
                }
                .into(),
            )
        })
    })
    .unwrap()
}
fn continued(state: &AppState, reference: &str) -> Result<Value, String> {
    let owner = state.file_acts.lock().unwrap().get(reference).unwrap();
    let owner = owner.lock().unwrap();
    state
        .act
        .lock()
        .unwrap()
        .as_mut()
        .unwrap()
        .continue_file_act(&owner.offer)
}
fn census(root: &std::path::Path) -> Vec<(String, String)> {
    fn walk(root: &std::path::Path, at: &std::path::Path, out: &mut Vec<(String, String)>) {
        for entry in std::fs::read_dir(at).unwrap() {
            let path = entry.unwrap().path();
            if path.is_dir() {
                walk(root, &path, out)
            } else {
                out.push((
                    path.strip_prefix(root).unwrap().display().to_string(),
                    util::sha256_hex(&std::fs::read(path).unwrap()),
                ));
            }
        }
    }
    let mut out = Vec::new();
    walk(root, root, &mut out);
    out.sort();
    out
}
#[test]
fn connected_file_act_all_kinds_and_declines_read_original_capture_without_writes() {
    for kind in [
        act_control::FileActKind::Check,
        act_control::FileActKind::Approve,
        act_control::FileActKind::Rely,
    ] {
        for choice in ["act", "decline"] {
            let (root, state, home, _, _, _) = workflow_root_context_tests::fixture();
            let reference = selected(&state, &home, &root, kind);
            let result = synthetic(&state, &reference, choice, || {});
            assert_eq!(result["state"], "AC-7 recorded");
            let before = census(&root);
            let view = file_act_view::read(&root);
            assert_eq!(census(&root), before);
            let rows = view["rows"].as_array().unwrap();
            assert_eq!(rows.len(), 1);
            let row = &rows[0];
            assert_eq!(row["kind"], kind.code());
            assert_eq!(row["captureCorrespondence"], true);
            assert_eq!(row["actor"]["identityVerified"], false);
            assert_eq!(
                row["recordedBy"]["identity"],
                records::APP_INTERFACE.identity
            );
            assert_eq!(
                row["event"],
                if choice == "decline" {
                    "declined this act"
                } else {
                    "recorded human-act claim"
                }
            );
            assert!(row["comparison"]
                .as_str()
                .unwrap()
                .contains("current bytes match"));
            assert!(
                file_act_confirm_original(&state, &reference, |_, _, _| panic!(
                    "second native presentation"
                ))
                .is_err()
            );
            assert_eq!(
                continued(&state, &reference).unwrap()["capture"]["captureId"],
                result["capture"]["captureId"]
            );
            std::fs::write(root.join("output.txt"), b"changed bytes").unwrap();
            assert!(file_act_view::read(&root)["rows"][0]["comparison"]
                .as_str()
                .unwrap()
                .contains("differs"));
            std::fs::remove_file(root.join("output.txt")).unwrap();
            assert!(file_act_view::read(&root)["rows"][0]["comparison"]
                .as_str()
                .unwrap()
                .contains("subject absent"));
            std::fs::remove_dir_all(root).unwrap();
        }
    }
}
#[test]
fn connected_file_act_dismiss_and_stale_actor_content_root_create_no_act() {
    for mode in ["dismiss", "actor", "content", "root"] {
        let (root, state, home, _, _, _) = workflow_root_context_tests::fixture();
        let reference = selected(&state, &home, &root, act_control::FileActKind::Check);
        let moved = root.with_extension("moved");
        let result = synthetic(
            &state,
            &reference,
            if mode == "dismiss" { "dismiss" } else { "act" },
            || match mode {
                "actor" => *state.person_name.lock().unwrap() = Some("changed person".into()),
                "content" => std::fs::write(root.join("output.txt"), b"changed").unwrap(),
                "root" => std::fs::rename(&root, &moved).unwrap(),
                _ => {}
            },
        );
        if mode == "root" {
            std::fs::rename(&moved, &root).unwrap();
        }
        assert_ne!(result["state"], "AC-7 recorded");
        assert!(continued(&state, &reference).is_err());
        assert!(file_act_view::read(&root)["rows"]
            .as_array()
            .unwrap()
            .is_empty());
        std::fs::remove_dir_all(root).unwrap();
    }
}
#[test]
fn connected_file_act_uncertain_and_record_pending_keep_original_continuation() {
    for uncertain in [true, false] {
        let (root, state, home, _, _, _) = workflow_root_context_tests::fixture();
        let reference = selected(&state, &home, &root, act_control::FileActKind::Rely);
        let log = root.join(recorder::LOG);
        if uncertain {
            storage::ensure_directory(&root.join(act_control::CAPTURE_STORE)).unwrap();
            storage::fail_directory_for_test(Some(root.clone()));
        } else {
            std::fs::create_dir_all(&log).unwrap();
        }
        let result = synthetic(&state, &reference, "act", || {});
        storage::fail_directory_for_test(None);
        assert_eq!(
            result["state"],
            if uncertain {
                "capture publication uncertain"
            } else {
                "AC-8 record pending"
            }
        );
        assert!(file_act_view::read(&root)["rows"]
            .as_array()
            .unwrap()
            .is_empty());
        if !uncertain {
            std::fs::remove_dir(&log).unwrap();
        }
        let recorded = continued(&state, &reference).unwrap();
        assert_eq!(recorded["state"], "AC-7 recorded");
        assert_eq!(
            file_act_view::read(&root)["rows"].as_array().unwrap().len(),
            1
        );
        std::fs::remove_dir_all(root).unwrap();
    }
}
#[test]
fn connected_file_act_reader_does_not_upgrade_missing_or_mismatched_capture() {
    let (root, state, home, _, _, _) = workflow_root_context_tests::fixture();
    let reference = selected(&state, &home, &root, act_control::FileActKind::Approve);
    let result = synthetic(&state, &reference, "act", || {});
    let path = storage::capture_path(&root, result["capture"]["captureId"].as_str().unwrap());
    let original = std::fs::read(&path).unwrap();
    std::fs::remove_file(&path).unwrap();
    let before = census(&root);
    let view = file_act_view::read(&root);
    assert_eq!(census(&root), before);
    assert_eq!(view["rows"][0]["captureCorrespondence"], false);
    assert!(view["rows"][0]["limits"]
        .as_array()
        .unwrap()
        .iter()
        .any(|v| v.as_str().unwrap().contains("native origin")));
    let mut altered: Value = serde_json::from_slice(&original).unwrap();
    altered["actor"]["displayName"] = json!("agent text claiming approval");
    std::fs::write(&path, serde_json::to_vec(&altered).unwrap()).unwrap();
    assert_eq!(
        file_act_view::read(&root)["rows"][0]["captureCorrespondence"],
        false
    );
    std::fs::write(&path, original).unwrap();
    assert_eq!(
        file_act_view::read(&root)["rows"][0]["captureCorrespondence"],
        true
    );
    std::fs::remove_dir_all(root).unwrap();
}
