//! Connected producer -> immutable selection -> compatibility -> supplied text checks.
//! Invented acts and transport results exercise boundaries, never establish a person's act.
mod util {
    pub fn sha256_hex(bytes: &[u8]) -> String {
        use sha2::{Digest, Sha256};
        Sha256::digest(bytes)
            .iter()
            .map(|b| format!("{b:02x}"))
            .collect()
    }
}
#[path = "../src/execution_compatibility.rs"]
mod execution_compatibility;
#[path = "../src/role_supply.rs"]
mod role_supply;
#[path = "../src/workflow_declaration.rs"]
mod workflow_declaration;
#[path = "../src/workflow_workspace.rs"]
mod workflow_workspace;
use serde_json::json;
use std::collections::{BTreeMap, BTreeSet};
use workflow_declaration::Reading;
use workflow_workspace::*;
fn package(extra: &str) -> Snapshot {
    let text = format!("---\nname: example\n---\n# Method\nWork against the brief.\n{extra}");
    Snapshot::from_files(BTreeMap::from([
        ("WORKFLOW.md".into(), text.into_bytes()),
        (
            "resources/checklist.md".into(),
            b"Check the outputs.\n".to_vec(),
        ),
    ]))
    .unwrap()
}
fn declared(doc: serde_json::Value) -> String {
    format!(
        "```workflow-declaration\n{}\n```\n",
        serde_json::to_string(&doc).unwrap()
    )
}
fn doc() -> serde_json::Value {
    json!({"declaration_contract_version":"WD-v0.8","required_tools":[{"name":"read","class":"host_operation","operation":"example.read","purpose":"Read basis","necessity":"required","stages":["Method"]}],"checkpoints":[],"returned_outputs":[],"returned_evidence":[]})
}
fn act(review: &Review) -> RegistrationAdapterClaim {
    RegistrationAdapterClaim {
        act_ref: "act:invented-test-double".into(),
        subject: review.identity.clone(),
        reviewed_draft: review.draft_key.clone(),
        review_ref: review.review_ref.clone(),
        prior: review.prior.clone(),
    }
}
#[test]
fn producer_consumer_unit() {
    let snapshot = package(&declared(doc()));
    let id = snapshot
        .identity("project", "project-A", "example", None)
        .unwrap();
    let review = Review::open(
        snapshot.clone(),
        &snapshot,
        snapshot.revision(),
        id,
        None,
        DraftKey {
            draft_location: "project".into(),
            draft_root: "project-A/.chirality/workflow-drafts".into(),
            name: "example".into(),
        },
        "review:fixture".into(),
    )
    .unwrap();
    let registered =
        RegistrationClaimMatch::compare(&review, &snapshot, None, act(&review)).unwrap();
    assert_eq!(registered.claimed_act_ref(), "act:invented-test-double");
    assert_eq!(registered.identity(), &review.identity);
    assert!(!registered.selection_eligible());
    let selected_snapshot = registered.snapshot().clone();
    let selected_id = selected_snapshot
        .identity("bundled", "test-double-release", "example", None)
        .unwrap();
    let selection = Selection::synthetic_shipped(selected_snapshot, selected_id).unwrap();
    let declaration = selection.snapshot().declaration().unwrap();
    assert_eq!(declaration.reading, Reading::Recognized);
    let env = execution_compatibility::Environment {
        catalog: Some(BTreeMap::from([(
            "example.read".into(),
            execution_compatibility::Operation {
                version: "1".into(),
                exposure: Some(true),
                availability: Some(true),
            },
        )])),
        channel_enabled: true,
        ..Default::default()
    };
    let check = execution_compatibility::Compatibility::check(&declaration, &env);
    assert_eq!(check.result, execution_compatibility::Check::Compatible);
    assert!(check.checkpoints_are_guidance);
    let text = selection
        .run_start_text("run:fixture", "Read the named object.")
        .unwrap();
    assert!(text.contains(selection.snapshot().workflow_text()));
    assert!(text.contains("Workflow finished: bundled:example"));
    assert_eq!(selection.identity().origin, "bundled");
}
#[test]
fn registered_bytes_and_collision_origins_do_not_rebind() {
    let old = package("");
    let id = old.identity("project", "P", "example", None).unwrap();
    let review = Review::open(
        old.clone(),
        &old,
        old.revision(),
        id.clone(),
        None,
        DraftKey {
            draft_location: "project".into(),
            draft_root: "P/.chirality/workflow-drafts".into(),
            name: "example".into(),
        },
        "review:old".into(),
    )
    .unwrap();
    let matched = RegistrationClaimMatch::compare(&review, &old, None, act(&review)).unwrap();
    assert!(!matched.selection_eligible());
    let selected = Selection::synthetic_shipped(
        old.clone(),
        old.identity("bundled", "test-double-release", "example", None)
            .unwrap(),
    )
    .unwrap();
    let selected_id = selected.identity().clone();
    let new = package("Changed content");
    let entries = [
        new.identity("project", "P", "example", None).unwrap(),
        new.identity("user", "U", "example", None).unwrap(),
        new.identity("bundled", "B", "example", None).unwrap(),
    ];
    assert_eq!(collisions("example", &entries).len(), 3);
    assert_eq!(selected.identity(), &selected_id);
    assert_eq!(selected.snapshot().workflow_text(), old.workflow_text());
    assert_ne!(new.revision(), old.revision());
    assert!(RegistrationClaimMatch::compare(&review, &new, None, act(&review)).is_err());
    assert!(
        RegistrationClaimMatch::compare(&review, &old, Some(&entries[0]), act(&review)).is_err()
    );
    let mut wrong = act(&review);
    wrong.subject = entries[1].clone();
    assert!(RegistrationClaimMatch::compare(&review, &old, None, wrong).is_err());
}
#[test]
fn snapshot_hygiene_and_symlinks_refuse() {
    assert!(Snapshot::from_files(BTreeMap::from([("WORKFLOW.md".into(), vec![255])])).is_err());
    assert!(Snapshot::from_files(BTreeMap::from([
        ("WORKFLOW.md".into(), b"prose".to_vec()),
        ("../escape".into(), vec![])
    ]))
    .is_err());
    // RV1 includes OS bytes; HY4 separately refuses review registration.
    let os = Snapshot::from_files(BTreeMap::from([
        (
            "WORKFLOW.md".into(),
            b"---\nname: example\n---\nprose".to_vec(),
        ),
        (".DS_Store".into(), vec![]),
    ]))
    .unwrap();
    let os_id = os.identity("project", "P", "example", None).unwrap();
    assert!(Review::open(
        os.clone(),
        &os,
        os.revision(),
        os_id,
        None,
        DraftKey {
            draft_location: "project".into(),
            draft_root: "P/drafts".into(),
            name: "example".into()
        },
        "review:os".into()
    )
    .is_err());

    let dir = TempDir::new();
    package("").publish_new(&dir.0.join("revision")).unwrap();
    let snap = Snapshot::capture(&dir.0.join("revision")).unwrap();
    let id = snap
        .identity("bundled", "release-fixture", "example", None)
        .unwrap();
    let selection = Selection::synthetic_shipped(snap, id).unwrap();
    selection.verify_store(&dir.0.join("revision")).unwrap();
    std::fs::write(dir.0.join("revision/resources/checklist.md"), b"tampered").unwrap();
    assert!(selection.verify_store(&dir.0.join("revision")).is_err());
    #[cfg(unix)]
    {
        std::os::unix::fs::symlink(
            dir.0.join("revision/WORKFLOW.md"),
            dir.0.join("revision/link"),
        )
        .unwrap();
        assert!(Snapshot::capture(&dir.0.join("revision")).is_err());
    }
}
#[test]
fn carriage_declared_empty_absent_unknown_duplicate() {
    assert!(
        workflow_declaration::extract("```text\n```workflow-declaration\n{}\n```\n```")
            .unwrap()
            .is_none()
    );
    assert!(
        workflow_declaration::extract("> ```workflow-declaration\n> {}\n> ```")
            .unwrap()
            .is_none()
    );
    assert!(
        workflow_declaration::extract("    ```workflow-declaration\n{}\n    ```")
            .unwrap()
            .is_none()
    );
    assert!(workflow_declaration::extract(
        "```workflow-declaration\n{}\n```\n~~~workflow-declaration\n{}\n~~~"
    )
    .is_err());
    assert!(workflow_declaration::parse_unique("{\"a\":{\"x\":1,\"x\":2}}").is_err());
    let absent = workflow_declaration::read("Method only").unwrap();
    assert_eq!(absent.categories["required_tools"], Reading::Undeclared);
    let empty = workflow_declaration::read(&declared(
        json!({"declaration_contract_version":"WD-v0.8","required_tools":[]}),
    ))
    .unwrap();
    assert_eq!(empty.categories["required_tools"], Reading::DeclaredEmpty);
    let unknown = workflow_declaration::read(&declared(
        json!({"declaration_contract_version":"future","required_tools":[]}),
    ))
    .unwrap();
    assert_eq!(unknown.reading, Reading::NotEstablished);
    assert!(unknown.raw.is_some());
    let mut d = doc();
    let el = d["required_tools"][0].clone();
    d["required_tools"].as_array_mut().unwrap().push(el);
    let duplicate = workflow_declaration::read(&declared(d)).unwrap();
    assert!(duplicate.elements["required_tools"]
        .iter()
        .all(|e| e.reading == Reading::NotEstablished));
}
#[test]
fn maintained_design_examples_validate_with_element_failures_retained() {
    let valid: serde_json::Value = serde_json::from_str(include_str!(
        "../resources/workflow_role/workflow-declaration.valid.example.json"
    ))
    .unwrap();
    let r = workflow_declaration::read(&declared(valid)).unwrap();
    assert!(
        r.elements
            .values()
            .flatten()
            .all(|e| e.reading == Reading::Recognized),
        "{r:?}"
    );
    let invalid: serde_json::Value = serde_json::from_str(include_str!(
        "../resources/workflow_role/workflow-declaration.invalid.example.json"
    ))
    .unwrap();
    let r = workflow_declaration::read(&declared(invalid)).unwrap();
    assert!(r
        .elements
        .values()
        .flatten()
        .any(|e| e.reading != Reading::Recognized));
    assert!(r.raw.is_some());
}
#[test]
fn tool_compatibility_missing_optional_unknown_and_guidance() {
    let mut d = doc();
    d["required_tools"][0]["versions"] = json!(["2"]);
    let decl = workflow_declaration::read(&declared(d.clone())).unwrap();
    let mut env = execution_compatibility::Environment {
        catalog: Some(BTreeMap::new()),
        channel_enabled: true,
        ..Default::default()
    };
    assert_eq!(
        execution_compatibility::Compatibility::check(&decl, &env).result,
        execution_compatibility::Check::Unsupported
    );
    env.catalog.as_mut().unwrap().insert(
        "example.read".into(),
        execution_compatibility::Operation {
            version: "1".into(),
            exposure: Some(true),
            availability: None,
        },
    );
    assert_eq!(
        execution_compatibility::Compatibility::check(&decl, &env).tools[0].outcome,
        execution_compatibility::Outcome::VersionMismatch
    );
    env.catalog
        .as_mut()
        .unwrap()
        .get_mut("example.read")
        .unwrap()
        .version = "2".into();
    env.channel_enabled = false;
    assert_eq!(
        execution_compatibility::Compatibility::check(&decl, &env).tools[0].outcome,
        execution_compatibility::Outcome::ChannelNotEnabled
    );
    d["required_tools"][0]["necessity"] = json!("optional");
    d["required_tools"][0]["fallback"] = json!("Return without read");
    let optional = workflow_declaration::read(&declared(d)).unwrap();
    assert_eq!(
        execution_compatibility::Compatibility::check(&optional, &env).result,
        execution_compatibility::Check::Compatible
    );
    let prose = workflow_declaration::read("No declared tools").unwrap();
    assert_eq!(
        execution_compatibility::Compatibility::check(&prose, &env).result,
        execution_compatibility::Check::NotEstablished
    );
}
#[test]
fn delegation_missing_signal_wins_over_unread_other_signal() {
    let d = json!({"declaration_contract_version":"WD-v0.8","required_tools":[{"name":"delegate","class":"harness_capability","capability":"agent-delegation","purpose":"bounded work","necessity":"required","stages":["Method"]}]});
    let decl = workflow_declaration::read(&declared(d)).unwrap();
    let mut env = execution_compatibility::Environment {
        harness_pin: Some("App Codex 0.158.0".into()),
        harness_signals: Some(json!({"provider_capabilities":{"namespaceTools":false}})),
        ..Default::default()
    };
    assert_eq!(
        execution_compatibility::Compatibility::check(&decl, &env).result,
        execution_compatibility::Check::Unsupported
    );
    env.harness_signals = Some(json!({}));
    assert_eq!(
        execution_compatibility::Compatibility::check(&decl, &env).result,
        execution_compatibility::Check::NotEstablished
    );
}
#[test]
fn four_roles_supply_only_at_start_preserve_byte_provenance() {
    use role_supply::*;
    let common = Guidance::seeded(
        "AGENTS.md",
        "fixture",
        "Common ü guidance".as_bytes().to_vec(),
        "Common ü guidance".as_bytes(),
    )
    .unwrap();
    for r in Role::ALL {
        let text = format!("{} instruction", r.name());
        let role = Guidance::seeded(
            &format!("agents/AGENT_{}.md", r.name()),
            "fixture",
            text.as_bytes().to_vec(),
            text.as_bytes(),
        )
        .unwrap();
        let c = Composition::new(&common, Some((r, &role)), true).unwrap();
        c.verify().unwrap();
        assert_eq!(c.carried["baseInstructions"], "not-set");
        assert_eq!(
            c.carried["developerInstructions"]["parts"]
                .as_array()
                .unwrap()
                .len(),
            2
        );
        let params = c.start_params().unwrap();
        assert!(check_role_inputs("thread/resume", &params).is_err());
        assert!(check_role_inputs("thread/fork", &params).is_err());
        let rec = c
            .start_record(
                "sup:fixture",
                "conversation:fixture",
                "req:fixture",
                1,
                None,
            )
            .unwrap();
        assert_eq!(rec["adoption"], "unknown");
        assert_eq!(rec["outcome"], "unknown-no-response");
        let mut broken = c.clone();
        broken.text.push('x');
        assert!(broken.verify().is_err());
        assert_eq!(limit(r, &role)["standing"], "stated-not-enforced");
        assert_eq!(Role::TASK.child_roles(), &[]);
        if r == Role::TASK {
            assert!(Composition::new(&common, Some((r, &role)), false).is_err())
        } else {
            assert!(Composition::new(&common, Some((r, &role)), false).is_ok())
        }
    }
    let none = Composition::new(&common, None, false).unwrap();
    assert_eq!(
        none.carried["developerInstructions"]["parts"]
            .as_array()
            .unwrap()
            .len(),
        1
    );
    assert!(check_role_inputs("thread/start", &json!({"config":{"agents.max_depth":2}})).is_err());
    let task = Guidance::seeded(
        "agents/AGENT_TASK.md",
        "fixture",
        b"changed".to_vec(),
        b"default",
    )
    .unwrap();
    assert_eq!(limit(Role::TASK, &task)["standing"], "unknown");
    let names = BTreeSet::from(["TASK".into()]);
    assert!(none
        .child_status(Some(&names), true)
        .iter()
        .all(|v| v["status"] == "not-supplied"));
}
#[test]
fn role_records_validate_and_supply_never_adoption() {
    use role_supply::*;
    let common = Guidance::seeded("AGENTS.md", "fixture", b"Common".to_vec(), b"Common").unwrap();
    let c = Composition::new(&common, None, false).unwrap();
    let schema: serde_json::Value = serde_json::from_str(include_str!(
        "../resources/workflow_role/role-supply-record.schema.json"
    ))
    .unwrap();
    let validator = jsonschema::options().offline().build(&schema).unwrap();
    for response in [
        None,
        Some(json!({"error":{"code":-1}})),
        Some(
            json!({"result":{"thread":{"id":"actual-thread","agentRole":null},"instructionSources":[]}}),
        ),
    ] {
        let r = c
            .start_record(
                "sup:fixture",
                "conversation:fixture",
                "req:fixture",
                1,
                response.as_ref(),
            )
            .unwrap();
        validator.validate(&r).unwrap();
        assert_eq!(r["adoption"], "unknown");
    }
}
struct TempDir(std::path::PathBuf);
impl TempDir {
    fn new() -> Self {
        let mut bytes = [0u8; 16];
        getrandom::fill(&mut bytes).unwrap();
        let p = std::env::temp_dir().join(format!(
            "chirality-workflow-role-{}",
            util::sha256_hex(&bytes)
        ));
        std::fs::create_dir(&p).unwrap();
        Self(p)
    }
}
impl Drop for TempDir {
    fn drop(&mut self) {
        let _ = std::fs::remove_dir_all(&self.0);
    }
}

#[test]
fn supply_reads_all_pages_and_never_assumes_send_is_verified() {
    let expected = "exact ü workflow bytes";
    let mut calls = vec![];
    let check = compare_untrusted_pages(expected, "turn:fixture", "client:fixture", |cursor| {
        calls.push(cursor.map(String::from));
        Ok(if cursor.is_none() {
            json!({"data":[{"turnId":"turn:fixture","item":{"type":"userMessage","id":"other","clientId":"other","content":[{"type":"text","text":"wrong"}]}}],"nextCursor":"next"})
        } else {
            json!({"data":[{"turnId":"turn:fixture","item":{"type":"userMessage","id":"match","clientId":"client:fixture","content":[{"type":"text","text":expected}]}}],"nextCursor":null})
        })
    });
    assert_eq!(check.state, UntrustedPageComparisonState::EqualClaimedText);
    assert_eq!(check.item.as_deref(), Some("match"));
    assert_eq!(calls, vec![None, Some("next".into())]);
    assert_eq!(check.adoption, "unknown");
    let failed = compare_untrusted_pages(expected, "turn:fixture", "client:fixture", |_| {
        Err("unreadable".into())
    });
    assert_eq!(failed.state, UntrustedPageComparisonState::Unreadable);
    let different = compare_untrusted_pages(expected, "turn:fixture", "client:fixture", |_| {
        Ok(
            json!({"data":[{"turnId":"turn:fixture","item":{"type":"userMessage","id":"fallback","content":[{"type":"text","text":"changed"}]}}],"nextCursor":null}),
        )
    });
    assert_eq!(
        different.state,
        UntrustedPageComparisonState::TextDiffersWorkflowBytesDiffer
    );
    assert_eq!(different.located_by.as_deref(), Some("first_user_message"));
    let repeated = compare_untrusted_pages(expected, "turn:fixture", "client:fixture", |_| {
        Ok(json!({"data":[],"nextCursor":"same"}))
    });
    assert_eq!(repeated.state, UntrustedPageComparisonState::Unreadable);
}
#[test]
fn role_compatibility_is_fixed_and_no_role_is_explicit() {
    let mut d = doc();
    d["compatible_roles"] = json!(["WORKING_ITEMS"]);
    let declaration = workflow_declaration::read(&declared(d)).unwrap();
    let env = execution_compatibility::Environment::default();
    let result = execution_compatibility::Compatibility::check_for_role(&declaration, &env, None);
    assert_eq!(result.result, execution_compatibility::Check::Unsupported);
    assert!(result.findings.iter().any(|s| s.contains("no role")));
}

#[test]
fn descriptor_validates_against_unchanged_design_and_body_is_exact() {
    let snapshot = package("Body without normalization\r\n");
    assert_eq!(snapshot.files().len(), 2);
    let id = snapshot
        .identity("project", "project-A", "example", None)
        .unwrap();
    let review = Review::open(
        snapshot.clone(),
        &snapshot,
        snapshot.revision(),
        id,
        None,
        DraftKey {
            draft_location: "project".into(),
            draft_root: "project-A/.chirality/workflow-drafts".into(),
            name: "example".into(),
        },
        "review:fixture".into(),
    )
    .unwrap();
    assert_eq!(review.snapshot().revision(), snapshot.revision());
    let wd: serde_json::Value = serde_json::from_str(workflow_declaration::SCHEMA).unwrap();
    let wr: serde_json::Value = serde_json::from_str(include_str!(
        "../resources/workflow_role/workspace-registration.schema.json"
    ))
    .unwrap();
    let mut registry = jsonschema::Registry::new();
    for schema in [wd, wr.clone()] {
        registry = registry
            .add(schema["$id"].as_str().unwrap(), schema.clone())
            .unwrap();
    }
    let registry = registry.prepare().unwrap();
    let validator = jsonschema::options()
        .with_registry(&registry)
        .offline()
        .build(&json!({"$ref":format!("{}#/$defs/a15_descriptor",wr["$id"].as_str().unwrap())}))
        .unwrap();
    validator.validate(&review.descriptor()).unwrap();
    let matched = RegistrationClaimMatch::compare(&review, &snapshot, None, act(&review)).unwrap();
    assert!(!matched.selection_eligible());
    let selection = Selection::synthetic_shipped(
        snapshot.clone(),
        snapshot
            .identity("bundled", "test-double-release", "example", None)
            .unwrap(),
    )
    .unwrap();
    let params = selection
        .run_turn_params(
            "thread:fixture",
            "run:fixture",
            ".chirality/workflow-revisions/example",
            "Person brief",
            "client:fixture",
        )
        .unwrap();
    assert_eq!(params["input"][1]["text"], "Person brief");
    let text = params["input"][0]["text"].as_str().unwrap();
    let rev = &snapshot.revision()[..12];
    let begin = format!("<<<chirality-workflow example@{rev} begin>>>\n");
    let end = format!("\n<<<chirality-workflow example@{rev} end>>>");
    assert_eq!(
        &text[text.find(&begin).unwrap() + begin.len()..text.rfind(&end).unwrap()],
        snapshot.workflow_text()
    );
    assert!(text.ends_with("end>>>"));
    let bytes_equal = compare_untrusted_pages(text, "turn:fixture", "client:fixture", |_| {
        Ok(
            json!({"data":[{"turnId":"turn:fixture","item":{"type":"userMessage","id":"u","clientId":"client:fixture","content":[{"type":"text","text":format!("changed wrapper\n{text}")}]}}],"nextCursor":null}),
        )
    });
    assert_eq!(
        bytes_equal.state,
        UntrustedPageComparisonState::TextDiffersWorkflowBytesEqual
    );
}
#[test]
fn seeded_guidance_missing_symlink_and_modified_bytes_refuse_or_report() {
    let dir = TempDir::new();
    std::fs::write(dir.0.join("AGENTS.md"), b"changed").unwrap();
    let guidance =
        role_supply::Guidance::read_seeded(&dir.0, "AGENTS.md", "fixture", b"default").unwrap();
    assert!(guidance.modified());
    assert_eq!(guidance.bytes(), b"changed");
    assert!(
        role_supply::Guidance::read_seeded(&dir.0, "../outside", "fixture", b"default").is_err()
    );
    #[cfg(unix)]
    {
        std::fs::remove_file(dir.0.join("AGENTS.md")).unwrap();
        std::os::unix::fs::symlink("missing", dir.0.join("AGENTS.md")).unwrap();
        assert!(
            role_supply::Guidance::read_seeded(&dir.0, "AGENTS.md", "fixture", b"default").is_err()
        );
    }
}

#[test]
fn regression_list_nested_fences_are_not_declarations() {
    let block = declared(json!({"declaration_contract_version":"WD-v0.8","required_tools":[]}));
    for prefix in ["- item", "1. item", "- outer\n  - nested"] {
        let indent = if prefix.starts_with("1.") { 3 } else { 2 };
        let nested = block
            .lines()
            .map(|line| format!("{}{line}", " ".repeat(indent)))
            .collect::<Vec<_>>()
            .join("\n");
        let text = format!("{prefix}\n{nested}\n");
        assert_eq!(
            workflow_declaration::extract(&text).unwrap(),
            None,
            "{text}"
        );
        assert_eq!(
            workflow_declaration::read(&text).unwrap().reading,
            Reading::Undeclared
        );
    }
    let list_example = format!(
        "- Example\n\n{}\n\n{}",
        block
            .lines()
            .map(|l| format!("  {l}"))
            .collect::<Vec<_>>()
            .join("\n"),
        block
    );
    assert_eq!(
        workflow_declaration::extract(&list_example).unwrap(),
        Some(
            serde_json::to_string(
                &json!({"declaration_contract_version":"WD-v0.8","required_tools":[]})
            )
            .unwrap()
        )
    );
    let root = format!("- item\n\n{}", block);
    assert!(workflow_declaration::extract(&root).unwrap().is_some());
    let indented_root = block
        .lines()
        .map(|l| format!("  {l}"))
        .collect::<Vec<_>>()
        .join("\n");
    assert!(workflow_declaration::extract(&indented_root)
        .unwrap()
        .is_some());
}
#[test]
fn regression_missing_or_unknown_necessity_cannot_produce_compatible() {
    let env = execution_compatibility::Environment::default();
    // A known missing required tool wins over an independent unread necessity.
    let mut mixed = doc();
    let mut malformed = mixed["required_tools"][0].clone();
    malformed.as_object_mut().unwrap().remove("necessity");
    malformed["name"] = json!("unknown");
    mixed["required_tools"]
        .as_array_mut()
        .unwrap()
        .push(malformed);
    let decl = workflow_declaration::read(&declared(mixed)).unwrap();
    let known_missing = execution_compatibility::Environment {
        catalog: Some(BTreeMap::new()),
        channel_enabled: true,
        ..Default::default()
    };
    assert_eq!(
        execution_compatibility::Compatibility::check(&decl, &known_missing).result,
        execution_compatibility::Check::Unsupported
    );
    for necessity in [None, Some(json!("future")), Some(json!(false))] {
        let mut d = doc();
        let tool = d["required_tools"][0].as_object_mut().unwrap();
        tool.remove("necessity");
        if let Some(value) = necessity {
            tool.insert("necessity".into(), value);
        }
        let decl = workflow_declaration::read(&declared(d)).unwrap();
        let check = execution_compatibility::Compatibility::check(&decl, &env);
        assert_eq!(
            check.tools[0].outcome,
            execution_compatibility::Outcome::NotEstablished
        );
        assert_eq!(check.result, execution_compatibility::Check::NotEstablished);
    }
}
#[test]
fn reviewed_package_identity_matches_independent_vectors_and_all_file_bytes() {
    let fixture: serde_json::Value = serde_json::from_str(include_str!(
        "../resources/workflow_role/identity-vectors.json"
    ))
    .unwrap();
    assert_eq!(fixture["method"], SNAPSHOT_METHOD);
    for vector in fixture["vectors"].as_array().unwrap() {
        let mut files = BTreeMap::new();
        for file in vector["files"].as_array().unwrap() {
            let hex = file["hex"].as_str().unwrap();
            let bytes = (0..hex.len())
                .step_by(2)
                .map(|i| u8::from_str_radix(&hex[i..i + 2], 16).unwrap())
                .collect();
            files.insert(file["path"].as_str().unwrap().into(), bytes);
        }
        let snapshot = Snapshot::from_files(files.clone()).unwrap();
        assert_eq!(snapshot.revision(), vector["digest"].as_str().unwrap());
        assert_eq!(snapshot.manifest().len(), files.len());
        let mut crlf = files.clone();
        crlf.insert("WORKFLOW.md".into(), b"workflow\r\n".to_vec());
        assert_ne!(
            snapshot.revision(),
            Snapshot::from_files(crlf).unwrap().revision()
        );
        let mut metadata = files.clone();
        metadata.insert(".DS_Store".into(), b"metadata".to_vec());
        assert_ne!(
            snapshot.revision(),
            Snapshot::from_files(metadata).unwrap().revision()
        );
        let mut manifest = files.clone();
        manifest.insert(
            "content-manifest.json".into(),
            b"manifest participates".to_vec(),
        );
        assert_ne!(
            snapshot.revision(),
            Snapshot::from_files(manifest).unwrap().revision()
        );
        let mut binary = files.clone();
        binary.get_mut("resource.bin").unwrap().push(1);
        assert_ne!(
            snapshot.revision(),
            Snapshot::from_files(binary).unwrap().revision()
        );
        let mut renamed = files.clone();
        let bytes = renamed.remove("resource.bin").unwrap();
        renamed.insert("resources/renamed.bin".into(), bytes);
        assert_ne!(
            snapshot.revision(),
            Snapshot::from_files(renamed).unwrap().revision()
        );
        let dir = TempDir::new();
        snapshot.publish_new(&dir.0.join("one")).unwrap();
        std::fs::create_dir_all(dir.0.join("one/empty/nested")).unwrap();
        assert_eq!(
            Snapshot::capture(&dir.0.join("one")).unwrap().revision(),
            snapshot.revision()
        );
        snapshot.publish_new(&dir.0.join("two")).unwrap();
        assert_eq!(
            Snapshot::capture(&dir.0.join("two")).unwrap().revision(),
            snapshot.revision()
        );
    }
    let abc = role_supply::content(b"abc");
    assert_eq!(abc["method"], "chirality.app.exact-bytes.sha256/v1");
    assert_eq!(
        abc["value"],
        "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"
    );
    assert_ne!(
        role_supply::content(b"a\nb"),
        role_supply::content(b"a\r\nb")
    );
}

#[test]
fn regression_visual_tab_columns_preserve_root_and_contained_fences() {
    // Includes the reviewer's exact '-\tExample' + blank + two-space fence.
    // Expected root/container readings were checked by an independent installed
    // CommonMark parser; product code has no dependency on that local tool.
    let fixture: serde_json::Value = serde_json::from_str(include_str!(
        "../resources/workflow_role/tab-carriage-cases.json"
    ))
    .unwrap();
    for case in fixture["cases"].as_array().unwrap() {
        let text = case["text"].as_str().unwrap();
        assert_eq!(
            workflow_declaration::extract(text).unwrap().is_some(),
            case["expected_root"].as_bool().unwrap(),
            "{text:?}"
        );
    }
}

#[test]
fn commonmark_container_html_and_eof_contract_controls() {
    for source in [
        "<div>\n```workflow-declaration\n{}\n```\n</div>",
        "<!--\n```workflow-declaration\n{}\n```\n-->",
        "> - example\n>   ```workflow-declaration\n>   {}\n>   ```",
        "- example\n\n  > ```workflow-declaration\n  > {}\n  > ```",
    ] {
        assert!(
            workflow_declaration::locate(source).unwrap().is_none(),
            "{source}"
        );
    }
    let unterminated = "```workflow-declaration\n{\"declaration_contract_version\":\"WD-v0.8\"}";
    let block = workflow_declaration::locate(unterminated).unwrap().unwrap();
    assert_eq!(
        workflow_declaration::parse_unique(&block.json_text).unwrap()
            ["declaration_contract_version"],
        "WD-v0.8"
    );
    assert_eq!(block.block_bytes.end, unterminated.len());
    let nested="````example\n```workflow-declaration\n{}\n```\n````\n\n```workflow-declaration\n{\"declaration_contract_version\":\"WD-v0.8\"}\n```";
    assert!(workflow_declaration::locate(nested).unwrap().is_some());
}
#[test]
fn commonmark_original_source_ranges_and_package_bytes_remain_exact() {
    let source="---\r\nname: example\r\n---\r\n# Méthod\r\n\r\n  ```workflow-declaration\r\n  {\"declaration_contract_version\":\"WD-v0.8\",\"required_tools\":[]}\r\n  ```\r\n";
    let located = workflow_declaration::locate(source).unwrap().unwrap();
    let raw = &source.as_bytes()[located.block_bytes.clone()];
    assert!(raw.windows(2).any(|b| b == b"\r\n"));
    assert!(std::str::from_utf8(raw)
        .unwrap()
        .contains("```workflow-declaration"));
    assert_eq!(
        located.block_bytes.start,
        source.find("  ```workflow-declaration").unwrap() + 2
    );
    for range in &located.text_bytes {
        assert!(range.start >= located.block_bytes.start && range.end <= located.block_bytes.end);
        assert!(source.is_char_boundary(range.start) && source.is_char_boundary(range.end));
    }
    let snapshot = Snapshot::from_files(BTreeMap::from([(
        "WORKFLOW.md".into(),
        source.as_bytes().to_vec(),
    )]))
    .unwrap();
    let before = snapshot.files()["WORKFLOW.md"].clone();
    assert_eq!(
        snapshot.declaration().unwrap().categories["required_tools"],
        Reading::DeclaredEmpty
    );
    assert_eq!(snapshot.files()["WORKFLOW.md"], before);
    assert_eq!(snapshot.workflow_text(), source);
}

#[test]
fn commonmark_decoded_info_aliases_are_not_reserved_literal_declarations() {
    for info in ["workflow&#45;declaration", r"workflow\-declaration"] {
        let alias = format!("```{info}\n{{}}\n```\n");
        assert!(
            workflow_declaration::locate(&alias).unwrap().is_none(),
            "{info}"
        );
        let literal =
            "~~~ \tworkflow-declaration \t\n{\"declaration_contract_version\":\"WD-v0.8\"}\n~~~";
        let combined = format!("{alias}\n{literal}");
        let block = workflow_declaration::locate(&combined).unwrap().unwrap();
        assert_eq!(block.block_bytes.start, combined.find("~~~").unwrap());
        assert_eq!(
            workflow_declaration::parse_unique(&block.json_text).unwrap()
                ["declaration_contract_version"],
            "WD-v0.8"
        );
    }
    for prefix in ["", " ", "  ", "   "] {
        let source = format!("{prefix}``` \tworkflow-declaration \t\r\n{{}}\r\n{prefix}```");
        assert!(workflow_declaration::locate(&source).unwrap().is_some());
    }
}

#[test]
fn untrusted_page_bytes_and_adapter_matches_never_grant_authority() {
    let snap = package("");
    let id = snap.identity("project", "P", "example", None).unwrap();
    let review = Review::open(
        snap.clone(),
        &snap,
        snap.revision(),
        id,
        None,
        DraftKey {
            draft_location: "project".into(),
            draft_root: "P/drafts".into(),
            name: "example".into(),
        },
        "review:data".into(),
    )
    .unwrap();
    let matched = RegistrationClaimMatch::compare(&review, &snap, None, act(&review)).unwrap();
    assert!(!matched.selection_eligible());
    assert_eq!(
        matched.evidence()["registrationAuthority"],
        "unverified adapter claim"
    );
    let selected = Selection::synthetic_shipped(
        snap.clone(),
        snap.identity("bundled", "test-double-release", "example", None)
            .unwrap(),
    )
    .unwrap();
    let expected = selected
        .run_start_text("run:fixture", "workflow-revisions/example")
        .unwrap();
    for (observed, state) in [
        (
            expected.clone(),
            UntrustedPageComparisonState::EqualClaimedText,
        ),
        (
            format!("prefix\n{expected}"),
            UntrustedPageComparisonState::TextDiffersWorkflowBytesEqual,
        ),
        (
            expected.replace(
                "<<<chirality-workflow example@",
                "<<<chirality-workflow foreign@",
            ),
            UntrustedPageComparisonState::TextDiffersWorkflowBytesDiffer,
        ),
    ] {
        let result = compare_untrusted_pages(&expected, "turn:test", "client:test", |_| {
            Ok(
                json!({"data":[{"turnId":"turn:test","item":{"type":"userMessage","id":"untrusted","clientId":"client:test","content":[{"type":"text","text":observed}]}}],"nextCursor":null}),
            )
        });
        assert_eq!(result.state, state);
        assert!(result.evidence_limits[0].contains("not native verification"));
        assert_eq!(result.adoption, "unknown");
        assert!(!serde_json::to_string(&result)
            .unwrap()
            .contains("\"verified\""));
    }
}
