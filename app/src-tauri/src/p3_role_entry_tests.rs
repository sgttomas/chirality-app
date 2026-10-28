use super::*;
fn stores() -> (PathBuf, PathBuf, PathBuf) {
    let base = std::env::temp_dir()
        .canonicalize()
        .unwrap()
        .join(util::opaque_id("p3-entry-").unwrap());
    let editable = base.join("editable");
    let package = base.join("package");
    runtime_session::seed_instructions(&editable).unwrap();
    runtime_session::seed_instructions(&package).unwrap();
    std::fs::write(package.join("roles.json"), role_supply::BUNDLED_ROLE_SET).unwrap();
    std::fs::write(
        package.join("ROLE_SET_SOURCE_BINDING.json"),
        include_bytes!("../resources/instructions/ROLE_SET_SOURCE_BINDING.json"),
    )
    .unwrap();
    (base, editable, package)
}
#[test]
fn p3_entry_native_mode_has_explicit_development_and_strict_package_routes() {
    let (base, editable, package) = stores();
    let (composition, standing) = prepare_role_entry(&editable, None, true, || {
        panic!("development does not select a package root")
    })
    .unwrap();
    assert_eq!(standing["standing"], "development-embedded-candidate");
    assert_eq!(
        composition.role_set_identity(),
        &role_supply::content(role_supply::BUNDLED_ROLE_SET)
    );
    let (_, standing) = prepare_role_entry(
        &editable,
        Some(role_supply::Role::HELP_HUMAN),
        false,
        || Ok(package.clone()),
    )
    .unwrap();
    assert_eq!(standing["standing"], "package-correspondence-verified");
    std::fs::remove_file(package.join("roles.json")).unwrap();
    let error = prepare_role_entry(&editable, None, false, || Ok(package)).unwrap_err();
    let refusal = refused_role_entry(None, &error);
    assert_eq!(refusal["state"], "refused-before-send");
    assert_eq!(
        refusal["roleSet"],
        role_supply::content(role_supply::BUNDLED_ROLE_SET)
    );
    assert_eq!(refusal["adoption"], "unknown");
    assert!(prepare_role_entry(&editable, None, false, || Err(
        "resource root unavailable".into()
    ))
    .is_err());
    std::fs::remove_file(editable.join("AGENTS.md")).unwrap();
    assert!(prepare_role_entry(&editable, None, true, || unreachable!()).is_err());
    std::fs::remove_dir_all(base).unwrap();
}
#[test]
fn p3_entry_host_metadata_uses_the_exact_four_role_asset() {
    let metadata = role_set_metadata();
    assert_eq!(metadata["available"], true);
    assert_eq!(metadata["roles"].as_array().unwrap().len(), 4);
    assert!(metadata["defaultRole"].is_null());
    // ROLE SL-1: TASK stays a standing role but is not offered as a conversation role.
    assert_eq!(
        metadata["conversationRoles"],
        json!(["HELP_HUMAN", "HELPS_HUMANS", "WORKING_ITEMS"])
    );
    assert!(metadata["roles"].as_array().unwrap().iter().any(|r| r["name"] == "TASK"));
    assert_eq!(
        metadata["identity"],
        role_supply::content(role_supply::BUNDLED_ROLE_SET)
    );
}
#[test]
fn p3_entry_task_start_is_refused_before_send_and_task_guidance_stays_for_delegation() {
    let (base, editable, _package) = stores();
    let error = prepare_role_entry(&editable, Some(role_supply::Role::TASK), true, || {
        unreachable!()
    })
    .unwrap_err();
    assert!(error.contains("not a primary entry"), "{error}");
    assert_eq!(refused_role_entry(Some(role_supply::Role::TASK), &error)["state"], "refused-before-send");
    for role in [role_supply::Role::HELP_HUMAN, role_supply::Role::HELPS_HUMANS, role_supply::Role::WORKING_ITEMS] {
        prepare_role_entry(&editable, Some(role), true, || unreachable!()).unwrap();
    }
    // The shipped TASK guidance is still composed for a delegated child.
    let common = role_supply::Guidance::read_seeded(&editable, "AGENTS.md", runtime_session::INSTRUCTION_RELEASE, runtime_session::COMMON_DEFAULT).unwrap();
    let task = role_supply::Guidance::read_seeded(&editable, "agents/AGENT_TASK.md", runtime_session::INSTRUCTION_RELEASE, runtime_session::role_default(role_supply::Role::TASK)).unwrap();
    role_supply::Composition::new(&common, Some((role_supply::Role::TASK, &task)), true).unwrap();
    std::fs::remove_dir_all(base).unwrap();
}

#[test]
fn p3_entry_compiled_tauri_mode_matches_declared_production_feature() {
    assert_eq!(tauri::is_dev(), !cfg!(feature = "custom-protocol"));
}
