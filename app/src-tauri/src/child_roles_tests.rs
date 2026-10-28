use super::*;
fn root() -> PathBuf {
    let p = std::env::temp_dir()
        .canonicalize()
        .unwrap()
        .join(crate::util::opaque_id("child-roles-").unwrap());
    std::fs::create_dir(&p).unwrap();
    p
}
fn setup() -> (PathBuf, Value) {
    let root = root();
    std::fs::create_dir(root.join("home")).unwrap();
    std::fs::write(root.join("home/config.toml"), "").unwrap();
    let reading = json!({"config":{"agents":null},"origins":{},"layers":[{"name":{"type":"sessionFlags"},"version":"s","config":{"cli_auth_credentials_store":"file"}},{"name":{"type":"user","file":root.join("home/config.toml"),"profile":null},"version":"u","config":{}},{"name":{"type":"system","file":root.join("system/config.toml")},"version":"y","config":{}}]});
    (root, reading)
}
fn role_file(path: &Path, name: &str) {
    std::fs::create_dir_all(path.parent().unwrap()).unwrap();
    std::fs::write(path,format!("name = {name:?}\ndescription = \"synthetic role\"\ndeveloper_instructions = \"PERSONAL_SOURCE_CANARY\"\n")).unwrap();
}
fn parent(root: &Path, role: Option<Role>) -> Composition {
    crate::runtime_session::seed_instructions(&root.join("instructions")).unwrap();
    crate::runtime_session::compose_role(&root.join("instructions"), role).unwrap()
}
#[test]
fn native_children_alias_recursive_and_content_currency() {
    let (root, mut reading) = setup();
    role_file(&root.join("home/agents/nested/misleading.toml"), "TASK");
    role_file(&root.join("alias.toml"), "WORKING_ITEMS");
    reading["layers"][1]["config"]["agents"] =
        json!({"ALIAS":{"config_file":root.join("alias.toml"),"description":"alias"}});
    let observed = Namespace::observe(&reading).unwrap();
    assert!(observed.contains(Role::TASK));
    assert!(observed.contains(Role::WORKING_ITEMS));
    assert!(observed.names.contains("ALIAS"));
    observed.recheck().unwrap();
    role_file(&root.join("home/agents/nested/misleading.toml"), "OTHER");
    assert!(
        observed.recheck().is_err(),
        "deletion of prior collision cannot promote availability"
    );
    std::fs::remove_dir_all(root).unwrap();
}
#[test]
fn native_children_unknown_origins_and_links_withhold() {
    let (root, reading) = setup();
    for kind in ["mdm", "enterpriseManaged", "packagedDefaults", "future"] {
        let mut r = reading.clone();
        r["layers"][0]["name"] = json!({"type":kind});
        assert!(Namespace::observe(&r).is_err());
    }
    let mut profile = reading.clone();
    profile["layers"][1]["name"]["profile"] = json!("named");
    assert!(Namespace::observe(&profile).is_err());
    std::os::unix::fs::symlink(root.join("home/config.toml"), root.join("linked.toml")).unwrap();
    let mut linked = reading.clone();
    linked["layers"][1]["name"]["file"] = json!(root.join("linked.toml"));
    assert!(Namespace::observe(&linked).is_err());
    std::fs::create_dir(root.join("home/agents")).unwrap();
    std::os::unix::fs::symlink(&root, root.join("home/agents/linked")).unwrap();
    assert!(Namespace::observe(&reading).is_err());
    std::fs::remove_dir_all(root).unwrap();
}
#[test]
fn native_children_disabled_project_is_not_read() {
    let (root, mut reading) = setup();
    reading["layers"].as_array_mut().unwrap().push(json!({"name":{"type":"project","dotCodexFolder":root.join("project/.codex")},"version":"p","config":{},"disabledReason":"untrusted"}));
    role_file(&root.join("project/.codex/agents/task.toml"), "TASK");
    assert!(!Namespace::observe(&reading).unwrap().contains(Role::TASK));
    reading["layers"][3]
        .as_object_mut()
        .unwrap()
        .remove("disabledReason");
    assert!(Namespace::observe(&reading).unwrap().contains(Role::TASK));
    std::fs::remove_dir_all(root).unwrap();
}
#[test]
fn native_children_matrix_exact_bytes_reuse_and_tamper() {
    let (root, reading) = setup();
    for role in [
        None,
        Some(Role::HELP_HUMAN),
        Some(Role::HELPS_HUMANS),
        Some(Role::WORKING_ITEMS),
    ] {
        let mut p = parent(&root, role);
        let n = Namespace::observe(&reading).unwrap();
        prepare(&mut p, Ok(n), &root.join("instructions"), &root);
        p.verify().unwrap();
        assert_eq!(
            p.children.len(),
            role.map(|r| r.child_roles().len()).unwrap_or(0)
        );
        for child in &p.children {
            let parsed: toml::Value =
                toml::from_str(std::str::from_utf8(&child.envelope).unwrap()).unwrap();
            assert_eq!(
                parsed["developer_instructions"].as_str(),
                Some(child.composition.text.as_str())
            );
            child.recheck().unwrap();
            assert!(child
                .composition
                .text
                .starts_with(std::str::from_utf8(crate::runtime_session::COMMON_DEFAULT).unwrap()));
        }
    }
    let mut p = parent(&root, Some(Role::WORKING_ITEMS));
    prepare(
        &mut p,
        Namespace::observe(&reading),
        &root.join("instructions"),
        &root,
    );
    let child = p.children[0].clone();
    std::fs::set_permissions(
        &child.path,
        std::os::unix::fs::PermissionsExt::from_mode(0o600),
    )
    .unwrap();
    std::fs::write(&child.path, "tampered").unwrap();
    assert!(child.recheck().is_err());
    let mut again = parent(&root, Some(Role::WORKING_ITEMS));
    prepare(
        &mut again,
        Namespace::observe(&reading),
        &root.join("instructions"),
        &root,
    );
    assert!(again.children.is_empty());
    assert_eq!(std::fs::read_to_string(child.path).unwrap(), "tampered");
    std::fs::remove_dir_all(root).unwrap();
}
#[test]
fn native_children_whole_observation_depth_and_entry_budgets() {
    let (root, reading) = setup();
    let mut at = root.join("home/agents");
    for _ in 0..34 {
        at = at.join("next");
    }
    std::fs::create_dir_all(&at).unwrap();
    assert!(Namespace::observe(&reading).is_err());
    std::fs::remove_dir_all(root.join("home/agents")).unwrap();
    std::fs::create_dir(root.join("home/agents")).unwrap();
    for n in 0..4097 {
        std::fs::write(root.join(format!("home/agents/{n}.txt")), "").unwrap();
    }
    assert!(Namespace::observe(&reading).is_err());
    std::fs::remove_dir_all(root).unwrap();
}
#[test]
fn native_children_explicit_owned_config_link_does_not_share_agents_siblings() {
    let (root, reading) = setup();
    std::fs::create_dir(root.join("shared")).unwrap();
    std::fs::write(root.join("shared/config.toml"), "").unwrap();
    role_file(&root.join("shared/agents/task.toml"), "TASK");
    std::fs::remove_file(root.join("home/config.toml")).unwrap();
    std::os::unix::fs::symlink(
        root.join("shared/config.toml"),
        root.join("home/config.toml"),
    )
    .unwrap();
    assert!(Namespace::observe(&reading).is_err());
    let link = ConfigLink::observed(
        root.join("home/config.toml"),
        root.join("shared/config.toml"),
    )
    .unwrap();
    let observed = Namespace::observe_linked(&reading, Some(link)).unwrap();
    assert!(!observed.contains(Role::TASK));
    observed.recheck().unwrap();
    std::fs::write(
        root.join("shared/config.toml"),
        "[agents.TASK]\ndescription = \"person\"\n",
    )
    .unwrap();
    assert!(observed.recheck().is_err());
    std::fs::remove_dir_all(root).unwrap();
}
#[test]
fn native_children_malformed_or_unwitnessed_role_file_shape_withholds() {
    let (root, reading) = setup();
    let path = root.join("home/agents/role.toml");
    std::fs::create_dir_all(path.parent().unwrap()).unwrap();
    for bytes in ["name = \"OTHER\"\ndescription = [1]\ndeveloper_instructions = \"person\"\n","name = \"OTHER\"\ndescription = \"person\"\ndeveloper_instructions = [1]\n","name = \"OTHER\"\ndescription = \"person\"\ndeveloper_instructions = \"person\"\nmodel = \"unwitnessed\"\n"]{std::fs::write(&path,bytes).unwrap();assert!(Namespace::observe(&reading).is_err());}
    std::fs::remove_dir_all(root).unwrap();
}
