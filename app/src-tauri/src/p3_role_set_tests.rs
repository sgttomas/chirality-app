use crate::role_supply::*;
use crate::runtime_session::{
    compose_role, role_default, seed_instructions, COMMON_DEFAULT, INSTRUCTION_RELEASE,
};
use crate::util::sha256_hex;
use serde_json::{json, Value};

#[test]
fn p3_exact_role_set_refuses_malformed_supply_for_every_selection() {
    let common = Guidance::seeded(
        "AGENTS.md",
        INSTRUCTION_RELEASE,
        COMMON_DEFAULT.to_vec(),
        COMMON_DEFAULT,
    )
    .unwrap();
    let base: Value = serde_json::from_slice(BUNDLED_ROLE_SET).unwrap();
    let mut cases = vec![b"not json".to_vec()];
    for mode in 0..7 {
        let mut bad = base.clone();
        match mode {
            0 => {
                bad["roles"].as_array_mut().unwrap().pop();
            }
            1 => bad["roles"][3] = bad["roles"][0].clone(),
            2 => bad["roles"][3]["name"] = json!("FIFTH"),
            3 => {
                bad["roles"][0]["default_for_new_chat"] = json!(true);
                bad["roles"][1]["default_for_new_chat"] = json!(true);
            }
            4 => bad["roles"][3]["delegation"] = json!("may-delegate"),
            5 => bad["roles"][0]["guidance_file"] = json!("../outside.md"),
            _ => bad["roles"][1]["child_roles"] = json!(["HELP_HUMAN"]),
        }
        cases.push(serde_json::to_vec(&bad).unwrap());
    }
    for bytes in cases {
        for role in std::iter::once(None).chain(Role::ALL.into_iter().map(Some)) {
            let active = role.map(|r| {
                Guidance::seeded(
                    &format!("agents/AGENT_{}.md", r.name()),
                    INSTRUCTION_RELEASE,
                    role_default(r).to_vec(),
                    role_default(r),
                )
                .unwrap()
            });
            assert!(
                Composition::with_role_set(&common, role.zip(active.as_ref()), true, &bytes)
                    .unwrap_err()
                    .starts_with("role-set-invalid")
            );
        }
    }
}

#[test]
fn p3_actual_seeded_start_preserves_identity_and_modified_guidance() {
    let root = std::env::temp_dir().join(format!(
        "p3-role-set-{}",
        crate::util::opaque_id("test").unwrap()
    ));
    seed_instructions(&root).unwrap();
    assert!(
        !root.join("roles.json").exists(),
        "read-only role set must not be seeded as editable guidance"
    );
    assert_eq!(bundled_role_set().unwrap().default_role(), None);
    for role in [
        None,
        Some(Role::HELP_HUMAN),
        Some(Role::HELPS_HUMANS),
        Some(Role::WORKING_ITEMS),
    ] {
        let composition = compose_role(&root, role).unwrap();
        assert_eq!(composition.role_set_identity(), &content(BUNDLED_ROLE_SET));
        let params = composition.start_params().unwrap();
        assert_eq!(params["developerInstructions"], composition.text);
        assert!(params.get("baseInstructions").is_none());
        for response in [
            None,
            Some(json!({"error":{"message":"fixture"}})),
            Some(json!({"result":{"thread":{"id":"fixture-thread"}}})),
        ] {
            let record = composition
                .start_record("sup:p3", "pending", "req:p3", 1, response.as_ref())
                .unwrap();
            assert_eq!(record["selection"]["roleSet"], content(BUNDLED_ROLE_SET));
            assert_eq!(record["adoption"], "unknown");
        }
    }
    std::fs::write(root.join("AGENTS.md"), "person edited guidance").unwrap();
    let modified = compose_role(&root, None).unwrap();
    assert_eq!(modified.text, "person edited guidance");
    assert_eq!(
        modified.carried["developerInstructions"]["parts"][0]["source"]["state"],
        "modified"
    );
    std::fs::remove_file(root.join("AGENTS.md")).unwrap();
    assert!(compose_role(&root, None).is_err());
    std::fs::remove_dir_all(root).unwrap();
}

#[test]
fn p3_identity_hashes_exact_role_set_bytes_and_task_stays_stated() {
    let common = Guidance::seeded(
        "AGENTS.md",
        INSTRUCTION_RELEASE,
        COMMON_DEFAULT.to_vec(),
        COMMON_DEFAULT,
    )
    .unwrap();
    let task = Guidance::seeded(
        "agents/AGENT_TASK.md",
        INSTRUCTION_RELEASE,
        role_default(Role::TASK).to_vec(),
        role_default(Role::TASK),
    )
    .unwrap();
    let mut spaced = BUNDLED_ROLE_SET.to_vec();
    spaced.push(b'\n');
    let composition =
        Composition::with_role_set(&common, Some((Role::TASK, &task)), true, &spaced).unwrap();
    assert_ne!(composition.role_set_identity(), &content(BUNDLED_ROLE_SET));
    assert_eq!(composition.role_set_identity(), &content(&spaced));
    assert_eq!(limit(Role::TASK, &task)["standing"], "stated-not-enforced");
    assert!(composition
        .child_status(None, false)
        .iter()
        .all(|v| v["status"] == "not-supplied"));
}

#[test]
fn p3_production_binding_matches_current_guidance_and_sources() {
    let binding: Value = serde_json::from_slice(include_bytes!(
        "../resources/instructions/ROLE_SET_SOURCE_BINDING.json"
    ))
    .unwrap();
    assert_eq!(binding["roleSet"]["sha256"], sha256_hex(BUNDLED_ROLE_SET));
    let repo = std::path::Path::new(env!("CARGO_MANIFEST_DIR"))
        .ancestors()
        .nth(4)
        .unwrap();
    for source in binding["sources"].as_array().unwrap() {
        let bytes = std::fs::read(repo.join(source["repositoryPath"].as_str().unwrap())).unwrap();
        assert_eq!(source["sha256"], sha256_hex(&bytes));
    }
    for source in binding["guidance"].as_array().unwrap() {
        let path = source["path"].as_str().unwrap();
        let bytes = if path == "AGENTS.md" {
            COMMON_DEFAULT
        } else {
            role_default(
                Role::ALL
                    .into_iter()
                    .find(|r| path == format!("agents/AGENT_{}.md", r.name()))
                    .unwrap(),
            )
        };
        assert_eq!(source["sha256"], sha256_hex(bytes));
        assert_eq!(source["byteLength"], bytes.len());
    }
}

#[test]
fn p3_actual_package_correspondence_refuses_missing_tampered_and_linked_files() {
    use crate::runtime_session::verify_production_instructions_root;
    let parent = std::env::temp_dir().canonicalize().unwrap();
    let root = parent.join(crate::util::opaque_id("p3-package-").unwrap());
    seed_instructions(&root).unwrap();
    let roles = root.join("roles.json");
    std::fs::write(&roles, BUNDLED_ROLE_SET).unwrap();
    let binding = include_bytes!("../resources/instructions/ROLE_SET_SOURCE_BINDING.json");
    std::fs::write(root.join("ROLE_SET_SOURCE_BINDING.json"), binding).unwrap();
    assert_eq!(
        verify_production_instructions_root(&root).unwrap()["roleSet"],
        content(BUNDLED_ROLE_SET)
    );
    std::fs::write(&roles, b"{}").unwrap();
    assert!(verify_production_instructions_root(&root).is_err());
    std::fs::remove_file(&roles).unwrap();
    assert!(verify_production_instructions_root(&root).is_err());
    std::fs::write(&roles, BUNDLED_ROLE_SET).unwrap();
    std::fs::write(root.join("agents/AGENT_TASK.md"), "tampered").unwrap();
    assert!(verify_production_instructions_root(&root).is_err());
    std::fs::remove_file(root.join("agents/AGENT_TASK.md")).unwrap();
    #[cfg(unix)]
    {
        std::os::unix::fs::symlink(root.join("AGENTS.md"), root.join("agents/AGENT_TASK.md"))
            .unwrap();
        assert!(verify_production_instructions_root(&root).is_err());
    }
    std::fs::remove_dir_all(root).unwrap();
}
