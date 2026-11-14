use super::*;

fn tmp(name: &str) -> PathBuf {
    let base = std::env::temp_dir().join(format!("codex-level-{}-{}", std::process::id(), name));
    let _ = std::fs::remove_dir_all(&base);
    std::fs::create_dir_all(&base).unwrap();
    base
}

#[test]
fn the_table_holds_the_five_levels_with_the_person_answering() {
    let ids: Vec<_> = levels().iter().map(|l| l.id.as_str()).collect();
    assert_eq!(ids, ["supervised", "edits", "edits-network", "edits-no-asking", "full"]);
    for level in levels() {
        assert_eq!(params(level, Method::TurnStart)["approvalsReviewer"], "user");
        assert_eq!(params(level, Method::ThreadStart)["approvalsReviewer"], "user");
    }
    assert!(RECOMMENDED_LEVEL.map_or(true, |id| level(id).is_some()));
}

#[test]
fn start_resume_and_fork_carry_the_mode_and_the_workspace_options_with_writable_roots_always_sent() {
    let edits = level("edits").unwrap();
    for method in [Method::ThreadStart, Method::ThreadResume, Method::ThreadFork] {
        let p = params(edits, method);
        assert_eq!(p["approvalPolicy"], "on-request");
        assert_eq!(p["sandbox"], "workspace-write");
        assert_eq!(p["config"]["sandbox_workspace_write"]["writable_roots"], json!([]));
        assert_eq!(p["config"]["sandbox_workspace_write"]["exclude_slash_tmp"], true);
        assert_eq!(p["config"]["sandbox_workspace_write"]["exclude_tmpdir_env_var"], true);
        assert_eq!(p["config"]["sandbox_workspace_write"]["network_access"], false);
        assert!(!p.contains_key("sandboxPolicy"));
    }
    let full = params(level("full").unwrap(), Method::ThreadFork);
    assert_eq!((full["approvalPolicy"].clone(), full["sandbox"].clone()), (json!("never"), json!("danger-full-access")));
    assert!(!full.contains_key("config"));
}

#[test]
fn a_turn_carries_the_structured_policy() {
    let p = params(level("edits-network").unwrap(), Method::TurnStart);
    assert_eq!(p["sandboxPolicy"]["type"], "workspaceWrite");
    assert_eq!(p["sandboxPolicy"]["networkAccess"], true);
    assert_eq!(p["sandboxPolicy"]["writableRoots"], json!([]));
    assert!(!p.contains_key("sandbox") && !p.contains_key("config"));
    assert_eq!(params(level("supervised").unwrap(), Method::TurnStart)["approvalPolicy"], "untrusted");
}

#[test]
fn merge_adds_the_level_beside_role_config_and_refuses_a_request_already_carrying_one() {
    let edits = level("edits").unwrap();
    let mut request = json!({"cwd": "/p", "config": {"agents.task.description": "x"}});
    merge(&mut request, edits, Method::ThreadStart).unwrap();
    assert_eq!(request["config"]["agents.task.description"], "x");
    assert_eq!(request["config"]["sandbox_workspace_write"]["writable_roots"], json!([]));
    assert_eq!(request["sandbox"], "workspace-write");
    for key in LEVEL_KEYS {
        let mut smuggled = json!({ key: "never" });
        assert!(merge(&mut smuggled, edits, Method::TurnStart).is_err(), "{key}");
    }
    let mut smuggled = json!({"config": {"sandbox_workspace_write": {"network_access": true}}});
    assert!(merge(&mut smuggled, edits, Method::ThreadStart).is_err());
}

#[test]
fn agreement_compares_approval_reviewer_and_the_whole_sandbox() {
    let edits = level("edits").unwrap();
    let reported = json!({"approvalPolicy": "on-request", "approvalsReviewer": "user", "sandbox": {
        "type": "workspaceWrite", "writableRoots": [], "networkAccess": false,
        "excludeTmpdirEnvVar": true, "excludeSlashTmp": true}});
    assert_eq!(agreement(edits, &reported), Agreement::Agrees);
    let mut widened = reported.clone();
    widened["sandbox"]["writableRoots"] = json!(["/Users/someone/elsewhere"]);
    assert!(matches!(agreement(edits, &widened), Agreement::Differs(d) if d[0].starts_with("sandbox=")));
    let mut reviewer = reported.clone();
    reviewer["approvalsReviewer"] = json!("auto_review");
    assert!(matches!(agreement(edits, &reviewer), Agreement::Differs(_)));
    let read_only = json!({"approvalPolicy": "untrusted", "approvalsReviewer": "user",
                           "sandbox": {"type": "readOnly", "networkAccess": false}});
    assert_eq!(agreement(level("supervised").unwrap(), &read_only), Agreement::Agrees);
}

#[test]
fn an_unsafe_home_path_is_found_in_any_component_as_written_and_as_resolved() {
    let base = tmp("home");
    let fine = base.join("App Data").join("homes").join("account");
    std::fs::create_dir_all(&fine).unwrap();
    assert_eq!(unsafe_home_component(&fine), None);
    for (i, (name, c)) in [("has $x", '$'), ("has `x`", '`'), ("has \"x\"", '"'), ("has \\x", '\\')].into_iter().enumerate() {
        let owner = base.join(name);
        let home = owner.join("App Data").join("home");
        std::fs::create_dir_all(&home).unwrap();
        assert_eq!(unsafe_home_component(&home), Some((c, owner.clone())), "{name}");
        let link = base.join(format!("link-{i}"));
        std::os::unix::fs::symlink(&home, &link).unwrap();
        assert_eq!(unsafe_home_component(&link).map(|(c, _)| c), Some(c), "through a link: {name}");
    }
    std::fs::remove_dir_all(&base).unwrap();
}

#[test]
fn a_double_quote_in_the_project_path_refuses_every_sandboxed_level_but_not_full_access() {
    let base = tmp("dq");
    let project = base.join("my \"quoted\" project");
    std::fs::create_dir_all(&project).unwrap();
    for level in levels() {
        let refused = refusal(level, &project, &[], None);
        if level.sandboxed() {
            assert_eq!(refused, Some(Refusal::ProjectPathBreaksSandbox), "{}", level.id);
        } else {
            assert_eq!(refused, None, "{}", level.id);
        }
    }
    std::fs::remove_dir_all(&base).unwrap();
}

#[test]
fn an_edits_level_is_refused_for_a_project_at_in_or_containing_an_app_folder_by_identity() {
    let base = tmp("folders");
    let home_folder = base.join("person");
    let app_data = home_folder.join("Library").join("Application Support").join("Chirality");
    let codex_home = app_data.join("homes").join("account");
    let working = home_folder.join("Library").join("Application Support").join("Chirality Working Files");
    let elsewhere = home_folder.join("projects").join("bridge");
    for d in [&codex_home, &working, &elsewhere] {
        std::fs::create_dir_all(d).unwrap();
    }
    let protected: [(&'static str, &Path); 3] =
        [("app-data", &app_data), ("codex-home", &codex_home), ("working-files", &working)];
    let edits = level("edits").unwrap();
    // A project that contains the App data folder (the person's home folder), one in it, and one that is it.
    for (project, reaches) in [(&home_folder, "app-data"), (&codex_home, "app-data"), (&app_data, "app-data"),
                               (&working, "working-files")] {
        assert_eq!(refusal(edits, project, &protected, None),
                   Some(Refusal::EditsReachAppFolders { folder: project.to_path_buf(), reaches }), "{project:?}");
    }
    // Through a link to the home folder: by identity, not by name.
    let link = base.join("alias-of-home");
    std::os::unix::fs::symlink(&home_folder, &link).unwrap();
    assert!(matches!(refusal(edits, &link, &protected, None), Some(Refusal::EditsReachAppFolders { .. })));
    // A project elsewhere is admitted; supervised and full access are not refused by this rule.
    assert_eq!(refusal(edits, &elsewhere, &protected, None), None);
    assert_eq!(refusal(level("supervised").unwrap(), &home_folder, &protected, None), None);
    assert_eq!(refusal(level("full").unwrap(), &home_folder, &protected, None), None);
    // The no-project folder, in the App data folder by construction, is exempt.
    let no_project = app_data.join("conversations-without-a-project");
    std::fs::create_dir_all(&no_project).unwrap();
    assert_eq!(refusal(edits, &no_project, &protected, Some(&no_project)), None);
    assert!(refusal(edits, &no_project, &protected, None).is_some());
    std::fs::remove_dir_all(&base).unwrap();
}

#[test]
fn a_lookup_that_fails_refuses() {
    let base = tmp("missing");
    let protected: [(&'static str, &Path); 1] = [("app-data", &base.join("does-not-exist"))];
    let project = base.join("project");
    std::fs::create_dir_all(&project).unwrap();
    assert!(matches!(refusal(level("edits").unwrap(), &project, &protected, None),
                     Some(Refusal::EditsReachAppFolders { .. })));
    std::fs::remove_dir_all(&base).unwrap();
}

#[test]
fn a_malformed_table_is_refused() {
    assert!(parse("{}").is_err());
    let doubled = TABLE.replacen("\"id\": \"edits-network\"", "\"id\": \"edits\"", 1);
    assert!(parse(&doubled).is_err());
    let inconsistent = TABLE.replacen("\"workspaceWrite\": null", "\"workspaceWrite\": {}", 1);
    assert!(parse(&inconsistent).is_err());
}

#[test]
fn the_level_ledger_rows_are_valid_under_0_6_only_and_carry_no_decision_actor() {
    let current: Value = serde_json::from_str(include_str!(
        "../resources/runtime_core/recovery.app-ledger-entry.schema.json")).unwrap();
    let before: Value = serde_json::from_str(include_str!(
        "../resources/runtime_core/recovery.app-ledger-entry.v0.5.schema.json")).unwrap();
    assert_eq!(current["$id"], "urn:chirality:app-v4:del-01-02:app-ledger-entry:0.6");
    let current = jsonschema::options().offline().build(&current).unwrap();
    let before = jsonschema::options().offline().build(&before).unwrap();
    let rows = [
        (include_str!("../resources/runtime_core/recovery.app-ledger-entry.level-chosen.default.valid.json"), true),
        (include_str!("../resources/runtime_core/recovery.app-ledger-entry.level-chosen.conversation.valid.json"), true),
        (include_str!("../resources/runtime_core/recovery.app-ledger-entry.level-sent.valid.json"), true),
        (include_str!("../resources/runtime_core/recovery.app-ledger-entry.level-reported.valid.json"), true),
        (include_str!("../resources/runtime_core/recovery.app-ledger-entry.level-chosen.no-digest.invalid.json"), false),
        (include_str!("../resources/runtime_core/recovery.app-ledger-entry.level-chosen.unknown-scope.invalid.json"), false),
        (include_str!("../resources/runtime_core/recovery.app-ledger-entry.level-chosen.actor.invalid.json"), false),
    ];
    for (bytes, valid) in rows {
        let row: Value = serde_json::from_str(bytes).unwrap();
        assert_eq!(current.is_valid(&row), valid, "{}", row["entryId"]);
        assert!(!before.is_valid(&row), "a 0.5 reader refuses {}", row["entryId"]);
    }
}
