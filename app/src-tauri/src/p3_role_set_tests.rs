use crate::role_supply::*;
use crate::runtime_session::{
    compose_role, role_default, seed_instructions, COMMON_DEFAULT, INSTRUCTION_RELEASE,
};
use crate::util::sha256_hex;
use serde_json::{json, Value};

// Documentary correspondence is separate from the exact identities of the
// shipped role set and guidance. Each selected passage is length framed.
fn documentary_input(bytes: &[u8], selectors: &Value) -> Result<Vec<u8>, String> {
    let text = std::str::from_utf8(bytes).map_err(|e| e.to_string())?;
    let mut output = Vec::new();
    for selector in selectors.as_array().ok_or("missing selectors")? {
        let selected = if let Some(heading) = selector["heading"].as_str() {
            let lines: Vec<&str> = text.split_inclusive('\n').collect();
            let starts: Vec<usize> = lines
                .iter()
                .enumerate()
                .filter_map(|(i, line)| {
                    (line.trim_end_matches(['\r', '\n']) == heading).then_some(i)
                })
                .collect();
            if starts.len() != 1 {
                return Err("heading missing or repeated".into());
            }
            let level = heading.chars().take_while(|c| *c == '#').count();
            let start = starts[0];
            let end = (start + 1..lines.len())
                .find(|i| {
                    let count = lines[*i].chars().take_while(|c| *c == '#').count();
                    count > 0 && count <= level && lines[*i].as_bytes().get(count) == Some(&b' ')
                })
                .unwrap_or(lines.len());
            lines[start..end].concat()
        } else {
            let prefix = selector["linePrefix"]
                .as_str()
                .ok_or("missing line prefix")?;
            let lines: Vec<&str> = text
                .split_inclusive('\n')
                .filter(|line| line.starts_with(prefix))
                .collect();
            if lines.len() != 1 {
                return Err("clause missing or repeated".into());
            }
            if prefix.starts_with("- **REQ-") {
                // These declared inputs are single-line list items. A new
                // continuation is changed meaning, not an excluded note.
                let following = text
                    .split_inclusive('\n')
                    .skip_while(|line| !line.starts_with(prefix))
                    .skip(1);
                for line in following {
                    if line.starts_with("- ") || line.starts_with('#') {
                        break;
                    }
                    if !line.trim().is_empty() {
                        return Err("requirement continuation needs a new selector".into());
                    }
                }
            }
            if let Some(columns) = selector["columns"].as_array() {
                let cells: Vec<&str> = lines[0]
                    .trim_end_matches(['\r', '\n'])
                    .trim_matches('|')
                    .split('|')
                    .collect();
                let values: Result<Vec<&str>, String> = columns
                    .iter()
                    .map(|column| {
                        let i = column.as_u64().ok_or("invalid column")? as usize;
                        cells.get(i).copied().ok_or_else(|| "missing column".into())
                    })
                    .collect();
                values?.join("|")
            } else {
                lines[0].to_owned()
            }
        };
        output.extend_from_slice(&(selected.len() as u64).to_be_bytes());
        output.extend_from_slice(selected.as_bytes());
    }
    Ok(output)
}

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
        let common = &composition.carried["developerInstructions"]["parts"][0];
        assert_eq!(common["content"], content(COMMON_DEFAULT));
        assert_eq!(common["offset"], 0);
        assert_eq!(common["length"], COMMON_DEFAULT.len());
        assert_eq!(
            common["source"]["reviewedDefault"]["content"],
            content(COMMON_DEFAULT)
        );
        assert_eq!(common["source"]["state"], "default");
        assert_eq!(
            &composition.text.as_bytes()[..COMMON_DEFAULT.len()],
            COMMON_DEFAULT
        );
        match role {
            None => assert_eq!(composition.text.as_bytes(), COMMON_DEFAULT),
            Some(role) => {
                let part = &composition.carried["developerInstructions"]["parts"][1];
                let offset = part["offset"].as_u64().unwrap() as usize;
                assert_eq!(&composition.text.as_bytes()[offset..], role_default(role));
                assert_eq!(part["content"], content(role_default(role)));
                assert_eq!(part["length"], role_default(role).len());
            }
        }
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
    assert_eq!(
        &composition.text.as_bytes()[..COMMON_DEFAULT.len()],
        COMMON_DEFAULT
    );
    assert_eq!(
        composition.carried["developerInstructions"]["parts"][0]["content"],
        content(COMMON_DEFAULT)
    );
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
        .nth(2)
        .unwrap();
    for source in binding["sources"].as_array().unwrap() {
        // Preserve the original binding identity; resolve its historical locator
        // against the independently rooted App project.
        let relative = source["repositoryPath"]
            .as_str()
            .unwrap()
            .strip_prefix("projects/chirality-app-v4/")
            .expect("source binding must name this App project");
        let bytes = std::fs::read(repo.join(relative)).unwrap();
        let input = if source.get("selectors").is_some() {
            documentary_input(&bytes, &source["selectors"]).unwrap()
        } else {
            bytes
        };
        assert_eq!(source["sha256"], sha256_hex(&input));
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
fn p3_documentary_binding_ignores_unread_notes_and_refuses_changed_role_meaning() {
    let text = "# Design\n\n### 4.1 Role set\n\nExactly four roles.\n\n### 4.2 Notes\n\nOld implementation note.\n";
    let selectors = json!([{"heading":"### 4.1 Role set"}]);
    let basis = documentary_input(text.as_bytes(), &selectors).unwrap();
    assert_eq!(
        basis,
        documentary_input(
            text.replace("Old implementation note.", "New implementation note.")
                .as_bytes(),
            &selectors
        )
        .unwrap()
    );
    assert_ne!(
        basis,
        documentary_input(
            text.replace("Exactly four", "Exactly five").as_bytes(),
            &selectors
        )
        .unwrap()
    );
    assert!(documentary_input(
        text.replace("### 4.1 Role set", "### 4.1 Renamed")
            .as_bytes(),
        &selectors
    )
    .is_err());
    assert!(documentary_input(
        format!("{text}\n### 4.1 Role set\nDuplicate\n").as_bytes(),
        &selectors
    )
    .is_err());
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
