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
    assert_eq!(DEFAULT_LEVEL, Some("full"), "the App's default level is full access in the shipped build");
    assert!(DEFAULT_LEVEL.map_or(true, |id| level(id).is_some()));
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
fn a_refused_home_path_is_found_in_any_component_as_written_and_as_resolved() {
    let base = tmp("home");
    let fine = base.join("App Data").join("homes").join("account");
    std::fs::create_dir_all(&fine).unwrap();
    assert_eq!(refused_home_component(&fine), None);
    for (i, (name, c)) in [("has $x", '$'), ("has `x`", '`'), ("has \"x\"", '"'), ("has \\x", '\\')].into_iter().enumerate() {
        let owner = base.join(name);
        let home = owner.join("App Data").join("home");
        std::fs::create_dir_all(&home).unwrap();
        assert_eq!(refused_home_component(&home), Some((c, owner.clone())), "{name}");
        let link = base.join(format!("link-{i}"));
        std::os::unix::fs::symlink(&home, &link).unwrap();
        assert_eq!(refused_home_component(&link).map(|(c, _)| c), Some(c), "through a link: {name}");
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
        (include_str!("../resources/runtime_core/recovery.app-ledger-entry.level-chosen.with-confirmation.invalid.json"), false),
        (include_str!("../resources/runtime_core/recovery.app-ledger-entry.level-chosen.unknown-scope.invalid.json"), false),
        (include_str!("../resources/runtime_core/recovery.app-ledger-entry.level-chosen.actor.invalid.json"), false),
    ];
    let mut inherited = json!({"kind":"level_inherited","session":"session:invented","entryId":"level-inherited:invented",
        "at":"2026-11-15T00:00:00Z","scope":{"kind":"conversation","home":"home:invented","threadId":"thread:invented"},
        "level":recorded_values(level("full").unwrap()),"origin":"app-default","chosen":null,"chosenAt":null});
    assert!(current.is_valid(&inherited));
    assert!(!before.is_valid(&inherited));
    inherited["origin"]=json!("session-only");
    assert!(!current.is_valid(&inherited),"session-only associations cannot be persisted");
    inherited["origin"]=json!("chosen");
    assert!(!current.is_valid(&inherited),"a chosen origin needs its actual choice reference and time");
    inherited["chosen"]=json!("level-chosen:invented");inherited["chosenAt"]=json!("2026-11-15T00:00:00Z");
    assert!(current.is_valid(&inherited));
    inherited["actor"]=json!("person:invented");
    assert!(!current.is_valid(&inherited),"an association is not an act");
    for (bytes, valid) in rows {
        let row: Value = serde_json::from_str(bytes).unwrap();
        assert_eq!(current.is_valid(&row), valid, "{}", row["entryId"]);
        assert!(!before.is_valid(&row), "a 0.5 reader refuses {}", row["entryId"]);
    }
}

// ---- DEL-01-01: the project trust case table, with the App's own choice ----

/// A reading of `case` for an invented folder, with the App's `choice`.
fn reading(case: TrustCase, choice: Option<AppTrust>) -> TrustReading {
    let mut r = TrustReading::not_read(PathBuf::from("/invented/project"), TRUST_READ_FAILED, None);
    r.case = case;
    r.choice = choice;
    r.read_at = Some("2026-11-19T00:00:00Z".into());
    r
}
fn trusted() -> TrustCase { TrustCase::Trusted { key: "/invented/project".into() } }
fn marked_untrusted() -> TrustCase { TrustCase::MarkedUntrusted { key: "/invented/project".into() } }
fn not_read() -> TrustCase { TrustCase::NotRead { reason: TRUST_READ_FAILED.into(), detail: None } }
fn on() -> AppTrust { AppTrust::OnBySetup }
fn off() -> AppTrust { AppTrust::OffBySwitch { at: "2026-11-19T01:00:00Z".into() } }
fn choice_not_read() -> AppTrust { AppTrust::NotRead { detail: Some("invented store limit".into()) } }

#[test]
fn row_1_a_settings_reading_that_is_not_whole_and_current_is_untrusted_whatever_the_apps_choice() {
    for choice in [None, Some(on()), Some(AppTrust::OnBySwitch { at: "t".into() }), Some(off()), Some(AppTrust::NoChoice), Some(choice_not_read())] {
        let r = reading(not_read(), choice.clone());
        assert_eq!((r.row(), r.trust_level()), (TrustRow::SettingsNotRead, "untrusted"), "{choice:?}");
        assert_eq!(r.status()["lines"], json!([TRUST_NOT_READ, TRUST_UNTRUSTED_SENT]), "the existing sentences for their case");
    }
    // A stale reading is a reading that is not current: never trusted, the App's on included.
    let mut r = reading(trusted(), Some(on()));
    r.generation = Some(json!({"generation": 1, "configWrites": 0}));
    assert_eq!(r.stale().trust_level(), "untrusted");
}

#[test]
fn row_2_the_persons_untrusted_mark_wins_over_the_apps_on() {
    for choice in [None, Some(on()), Some(AppTrust::OnBySwitch { at: "t".into() }), Some(AppTrust::NoChoice)] {
        let r = reading(marked_untrusted(), choice.clone());
        assert_eq!((r.row(), r.trust_level()), (TrustRow::MarkedUntrusted, "untrusted"), "{choice:?}");
        assert_eq!(r.status()["case"], "marked-untrusted");
        assert_eq!(r.status()["lines"], json!([TRUST_MARKED_UNTRUSTED, TRUST_UNTRUSTED_SENT]));
    }
    assert_eq!(reading(marked_untrusted(), Some(on())).status()["appChoice"], "on", "the view can say the App's on was overridden");
}

#[test]
fn row_3_the_apps_off_wins_over_the_settings_trusted_mark() {
    for case in [trusted(), TrustCase::Unmarked] {
        let r = reading(case.clone(), Some(off()));
        assert_eq!((r.row(), r.trust_level()), (TrustRow::SwitchedOff, "untrusted"), "{case:?}");
        let status = r.status();
        assert_eq!(status["case"], "switched-off");
        assert_eq!(status["lines"], json!(["Chirality's choice for this project is off (switched off in Chirality at 2026-11-19T01:00:00Z), so the App sent an untrusted entry for the project root shown below."]));
        assert_eq!(status["appChoiceAt"], "2026-11-19T01:00:00Z");
    }
}

#[test]
fn row_4_the_settings_trusted_mark_is_trusted_as_now() {
    for choice in [None, Some(on()), Some(AppTrust::NoChoice)] {
        let r = reading(trusted(), choice.clone());
        assert_eq!((r.row(), r.trust_level()), (TrustRow::MarkedTrusted, "trusted"), "{choice:?}");
        assert_eq!(r.status()["case"], "trusted");
        assert_eq!(r.status()["lines"], json!([format!("{TRUST_TRUSTED_PREFIX}2026-11-19T00:00:00Z{TRUST_TRUSTED_SUFFIX}")]));
    }
}

#[test]
fn row_5_unmarked_with_the_apps_on_is_trusted_and_says_why() {
    let r = reading(TrustCase::Unmarked, Some(on()));
    assert_eq!((r.row(), r.trust_level()), (TrustRow::AppOn, "trusted"));
    assert_eq!(r.status()["case"], "app-on-by-setup");
    assert_eq!(r.status()["lines"], json!(["Chirality's choice for this project is on (you set it up in Chirality and have not switched its trust off), so the App sent a trusted entry for the project root shown below."]));
    assert_eq!(r.projects(), json!({"/invented/project": {"trust_level": "trusted"}}));
    let r = reading(TrustCase::Unmarked, Some(AppTrust::OnBySwitch { at: "2026-11-19T02:00:00Z".into() }));
    assert_eq!((r.row(), r.trust_level()), (TrustRow::AppOn, "trusted"));
    assert_eq!(r.status()["lines"], json!(["Chirality's choice for this project is on (switched on in Chirality at 2026-11-19T02:00:00Z), so the App sent a trusted entry for the project root shown below."]));
}

#[test]
fn row_6_otherwise_untrusted_as_now_and_a_folder_that_is_not_the_apps_project_is_exactly_as_before() {
    for choice in [None, Some(AppTrust::NoChoice)] {
        let r = reading(TrustCase::Unmarked, choice.clone());
        assert_eq!((r.row(), r.trust_level()), (TrustRow::Unmarked, "untrusted"), "{choice:?}");
        assert_eq!(r.status()["case"], "unmarked");
        assert_eq!(r.status()["lines"], json!([TRUST_UNTRUSTED_SENT]));
    }
    // No App project: the status is today's, with no field of the App's choice.
    let status = reading(TrustCase::Unmarked, None).status();
    assert!(status.get("appChoice").is_none());
}

#[test]
fn row_7_an_unreadable_choice_is_untrusted_over_every_mark() {
    for case in [trusted(), TrustCase::Unmarked, marked_untrusted()] {
        let r = reading(case.clone(), Some(choice_not_read()));
        assert_eq!((r.row(), r.trust_level()), (TrustRow::ChoiceNotRead, "untrusted"), "{case:?}");
        let status = r.status();
        assert_eq!(status["case"], "choice-not-read");
        assert_eq!(status["lines"], json!(["The App could not read its record of this project's trust choice, so it sent an untrusted entry for the project root shown below."]));
        assert_eq!(status["detail"], json!({"text": "invented store limit", "standing": NOT_THE_APPS_TEXT}));
    }
}

#[test]
fn the_apps_sentences_say_tried_to_send_for_an_unwritten_frame() {
    for (case, choice, want) in [
        (TrustCase::Unmarked, on(), "Chirality's choice for this project is on (you set it up in Chirality and have not switched its trust off), so the App tried to send a trusted entry for the project root shown below."),
        (TrustCase::Unmarked, AppTrust::OnBySwitch { at: "T".into() }, "Chirality's choice for this project is on (switched on in Chirality at T), so the App tried to send a trusted entry for the project root shown below."),
        (trusted(), off(), "Chirality's choice for this project is off (switched off in Chirality at 2026-11-19T01:00:00Z), so the App tried to send an untrusted entry for the project root shown below."),
        (trusted(), choice_not_read(), "The App could not read its record of this project's trust choice, so it tried to send an untrusted entry for the project root shown below."),
    ] {
        let status = reading(case, Some(choice)).status_for_write(false);
        assert_eq!(status["lines"], json!([want]));
        assert_eq!(status["sent"], Value::Null);
    }
}

#[test]
fn a_trusted_projects_settings_file_that_stops_a_start_is_one_dated_message_with_codexs_reason_whole() {
    let base = tmp("settings-refusal");
    let project = base.canonicalize().unwrap();
    let cwd = project.join("sub");
    std::fs::create_dir_all(cwd.join(".codex")).unwrap();
    std::fs::create_dir_all(project.join(".codex")).unwrap();
    let mut r = TrustReading::not_read(cwd.clone(), TRUST_READ_FAILED, None);
    r.case = TrustCase::Unmarked;
    r.choice = Some(on());
    assert_eq!((r.root.clone(), r.trust_level()), (cwd.clone(), "trusted"), "no .git: the folder is its own root");
    // A parse error naming the project's file: the App names no file; Codex's reason is given whole.
    let file = cwd.join(".codex").join("config.toml");
    let parse = json!({"code": -32600, "message": format!("failed to load configuration: {}: TOML parse error at line 1, column 5", file.display())});
    let mut said = project_settings_refusal(&r, &parse).unwrap();
    assert_eq!(said.get("lines"), None, "dated when its outcome is applied");
    project_settings_dated(&mut said, "2026-11-19T06:00:00.000Z");
    assert_eq!(said["lines"], json!([format!("{PROJECT_SETTINGS_AT_BEFORE}2026-11-19T06:00:00.000Z{PROJECT_SETTINGS_AT_AFTER}")]));
    assert_eq!(said["at"], "2026-11-19T06:00:00.000Z");
    assert_eq!((said["filesHeading"].as_str(), said["files"].clone()), (Some(PROJECT_SETTINGS_FILES), json!([{"path": file.to_string_lossy(), "where": IN_PROJECT_FOLDER}])));
    assert_eq!((said["codexReasonLabel"].as_str(), said["codexReason"].clone()), (Some(PROJECT_SETTINGS_REASON), json!({"text": parse["message"], "standing": NOT_THE_APPS_TEXT})));
    assert_eq!(said["remedy"], PROJECT_SETTINGS_REMEDY);
    for gone in ["attributed", "fileSentence", "filesAboveProject"] { assert_eq!(said.get(gone), None, "{gone}"); }
    // A key no longer supported: the same one form, the files from the root to the folder.
    let mut below = TrustReading::not_read(cwd.clone(), TRUST_READ_FAILED, None);
    (below.root, below.binding.root) = (project.clone(), Some(project.clone()));
    below.case = TrustCase::Unmarked;
    below.choice = Some(on());
    let unsupported = json!({"code": -32600, "message": "failed to load configuration: `invented_key` is no longer supported; remove it from config.toml"});
    let said = project_settings_refusal(&below, &unsupported).unwrap();
    assert_eq!(said["files"], json!([{"path": project.join(".codex/config.toml").to_string_lossy(), "where": IN_FOLDER_ABOVE},
        {"path": cwd.join(".codex/config.toml").to_string_lossy(), "where": IN_PROJECT_FOLDER}]));
    // Not this case: an untrusted entry's refusal, another code, another beginning.
    let mut untrusted = r.clone();
    untrusted.choice = Some(off());
    assert_eq!(project_settings_refusal(&untrusted, &parse), None, "an untrusted entry's refusal is left as it is");
    assert_eq!(project_settings_refusal(&r, &json!({"code": -32603, "message": parse["message"]})), None);
    assert_eq!(project_settings_refusal(&r, &json!({"code": -32600, "message": "invalid request: failed to load configuration:"})), None);
    std::fs::remove_dir_all(base).unwrap();
}

// ---- Repair after the independent review ----

fn user_layer(config: Value) -> Value { json!({"name": {"type": "user", "file": "/invented/config.toml"}, "config": config}) }
fn layers(user: Vec<Value>) -> Value { json!({"config": {}, "origins": {}, "layers": user}) }

#[test]
fn an_unusable_settings_shape_is_a_limited_reading_never_an_absent_mark() {
    let root = tmp("mark-shapes").canonicalize().unwrap();
    let key = root.to_string_lossy().into_owned();
    // Absent marks: no projects, no entry, an entry without trust_level.
    for config in [json!({}), json!({"projects": {}}), json!({"projects": {"/elsewhere": {"trust_level": 7}}}), json!({"projects": {key.clone(): {}}})] {
        assert_eq!(person_mark(&layers(vec![user_layer(config.clone())]), &root), Ok(TrustCase::Unmarked), "{config}");
    }
    // Unusable: not taken for absent.
    for config in [json!("text"), json!(null), json!([]), json!({"projects": "text"}), json!({"projects": {key.clone(): "trusted"}}),
                   json!({"projects": {key.clone(): {"trust_level": "yes"}}}), json!({"projects": {key.clone(): {"trust_level": true}}})] {
        assert_eq!(person_mark(&layers(vec![user_layer(config.clone())]), &root), Err(TRUST_READ_LIMITED.into()), "{config}");
    }
    let missing = json!({"name": {"type": "user", "file": "/invented/config.toml"}});
    assert_eq!(person_mark(&layers(vec![missing]), &root), Err(TRUST_READ_LIMITED.into()), "a user layer with no config");
    // The marks as before.
    for (level, case) in [("trusted", TrustCase::Trusted { key: key.clone() }), ("untrusted", TrustCase::MarkedUntrusted { key: key.clone() })] {
        assert_eq!(person_mark(&layers(vec![user_layer(json!({"projects": {key.clone(): {"trust_level": level}}}))]), &root), Ok(case));
    }
    std::fs::remove_dir_all(root).unwrap();
}

#[test]
fn where_the_two_spellings_of_the_root_carry_conflicting_marks_untrusted_wins() {
    let base = tmp("mark-spellings").canonicalize().unwrap();
    let real = base.join("real");
    std::fs::create_dir_all(&real).unwrap();
    let alias = base.join("alias");
    std::os::unix::fs::symlink(&real, &alias).unwrap();
    let (canonical, given) = (real.to_string_lossy().into_owned(), alias.to_string_lossy().into_owned());
    assert_eq!(trust_lookup_keys(&alias), vec![canonical.clone(), given.clone()]);
    for (first, second) in [("trusted", "untrusted"), ("untrusted", "trusted")] {
        let config = json!({"projects": {canonical.clone(): {"trust_level": first}, given.clone(): {"trust_level": second}}});
        assert!(matches!(person_mark(&layers(vec![user_layer(config)]), &alias), Ok(TrustCase::MarkedUntrusted { .. })), "{first} {second}");
    }
    std::fs::remove_dir_all(base).unwrap();
}

#[test]
fn the_settings_files_are_listed_by_name_from_the_bound_root_down_to_the_folder_as_resolved() {
    let base = tmp("settings-files").canonicalize().unwrap();
    let (root, cwd) = (base.join("repo"), base.join("repo").join("project"));
    std::fs::create_dir_all(cwd.join(".codex")).unwrap();
    std::fs::create_dir_all(root.join(".git")).unwrap();
    std::fs::write(root.join(".git").join("HEAD"), b"ref: refs/heads/main\n").unwrap();
    let mut r = TrustReading::not_read(cwd.clone(), TRUST_READ_FAILED, None);
    r.case = TrustCase::Unmarked;
    r.choice = Some(on());
    assert_eq!((r.binding.root.clone(), r.binding.resolved.clone()), (Some(root.clone()), Some(cwd.clone())));
    let error = json!({"code": -32600, "message": "failed to load configuration: invented"});
    let (above, own) = (root.join(".codex").join("config.toml"), cwd.join(".codex").join("config.toml"));
    let listed = json!([{"path": above.to_string_lossy(), "where": IN_FOLDER_ABOVE}, {"path": own.to_string_lossy(), "where": IN_PROJECT_FOLDER}]);
    assert_eq!(project_settings_refusal(&r, &error).unwrap()["files"], listed);
    // The folder named through a link: Codex finds the root from the folder as given (the link's own folders hold
    // no .git), so the bound root is that folder as resolved, and its file alone is listed.
    let alias = base.join("alias");
    std::os::unix::fs::symlink(&cwd, &alias).unwrap();
    let mut linked = TrustReading::not_read(alias.clone(), TRUST_READ_FAILED, None);
    linked.case = TrustCase::Unmarked;
    linked.choice = Some(on());
    assert_eq!((linked.binding.root.clone(), linked.binding.resolved.clone()), (Some(cwd.clone()), Some(cwd.clone())));
    assert_eq!(project_settings_refusal(&linked, &error).unwrap()["files"], json!([{"path": own.to_string_lossy(), "where": IN_PROJECT_FOLDER}]));
    // By name alone: a .codex at the root that is a link elsewhere is listed by its name, and nothing it points to.
    let outside = base.join("outside");
    std::fs::create_dir_all(&outside).unwrap();
    std::os::unix::fs::symlink(&outside, root.join(".codex")).unwrap();
    let said = project_settings_refusal(&r, &error).unwrap();
    assert_eq!(said["files"], listed);
    assert!(!said.to_string().contains(&outside.display().to_string()));
    // A folder outside the root: the root's file alone.
    assert_eq!(project_settings_files(&root, &outside), vec![(above.clone(), false)]);
    assert_eq!(project_settings_files(&root, &root), vec![(above, true)]);
    std::fs::remove_dir_all(base).unwrap();
}
