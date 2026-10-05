//! Source/API seam checks; invented native frames establish no real supplier witness.
mod util {
    pub fn sha256_hex(bytes: &[u8]) -> String {
        use sha2::{Digest, Sha256};
        Sha256::digest(bytes)
            .iter()
            .map(|b| format!("{b:02x}"))
            .collect()
    }
}
#[path = "../src/role_lifecycle.rs"]
mod role_lifecycle;
#[path = "../src/role_supply.rs"]
mod role_supply;
use role_lifecycle::*;
use role_supply::*;
use serde_json::{json, Value};
use std::collections::BTreeMap;
fn generation(home: &str, n: u64) -> Value {
    json!({"appSession":"session-A","home":home,"spawnCounter":n})
}
fn composition(role: Option<Role>, suffix: &str) -> Composition {
    let common = Guidance::seeded(
        "AGENTS.md",
        "test-release",
        format!("Common ü bytes{suffix}\r\n").into_bytes(),
        b"default common",
    )
    .unwrap();
    let guidance = role.map(|r| {
        Guidance::seeded(
            &format!("agents/AGENT_{}.md", r.name()),
            "test-release",
            format!("{} role text{suffix}\r\n", r.name()).into_bytes(),
            b"default role",
        )
        .unwrap()
    });
    Composition::new(&common, role.zip(guidance.as_ref()), true).unwrap()
}
fn frame(id: u64, thread: &str) -> Value {
    json!({"id":id,"result":{"thread":{"id":thread,"cliVersion":"0.160.0","createdAt":1,"updatedAt":2,"cwd":"/test/work","ephemeral":false,"modelProvider":"chosen-provider","preview":"native transcript sentinel","projectId":null,"sessionId":"native-session","source":"appServer","status":{"type":"idle"},"turns":[],"agentRole":null},
 "model":"reported-model","modelProvider":"chosen-provider","cwd":"/test/work","approvalPolicy":"on-request","approvalsReviewer":"user","sandbox":{"type":"readOnly"},"instructionSources":["/native/project/AGENTS.md"]}})
}

fn sent_start(id: u64, c: &Composition) -> Value {
    json!({"id":id,"method":"thread/start","params":{"developerInstructions":c.text,"model":"chosen-model","modelProvider":"chosen-provider","cwd":"/test/work"}})
}
fn sent_metadata(id: u64, method: &str) -> Value {
    json!({"id":id,"method":method,"params":{"threadId":"original-thread"}})
}
fn binding(role: Option<Role>) -> RoleBinding {
    let c = composition(role, "");
    PreparedStart::new(
        "home-A",
        generation("home-A", 1),
        json!(1),
        "request:start",
        "sup:original",
        &c,
    )
    .unwrap()
    .observe(
        &generation("home-A", 1),
        &sent_start(1, &c),
        &frame(1, "original-thread"),
    )
    .unwrap()
}
#[test]
fn original_buffers_survive_real_file_edits_and_future_notice_only() {
    let original = composition(Some(Role::HELP_HUMAN), " original");
    let prepared = PreparedStart::new(
        "home-A",
        generation("home-A", 1),
        json!(9),
        "request:9",
        "sup:9",
        &original,
    )
    .unwrap();
    let expected = prepared.guidance_params();
    let mut modified = original.clone();
    modified.text = "future bytes".into();
    let bound = prepared
        .observe(
            &generation("home-A", 1),
            &sent_start(9, &original),
            &frame(9, "thread-9"),
        )
        .unwrap();
    let before = bound.evidence();
    assert_eq!(
        before["binding"]["original"]["text"],
        expected["developerInstructions"]
    );
    assert_eq!(
        before["binding"]["observation"]["generation"],
        generation("home-A", 1)
    );
    assert!(before.to_string().contains("Common ü bytes original"));
    assert!(!before.to_string().contains("native transcript"));
    let tmp = TempDir::new();
    std::fs::create_dir(tmp.0.join("agents")).unwrap();
    std::fs::write(tmp.0.join("AGENTS.md"), b"changed common").unwrap();
    std::fs::write(
        tmp.0.join("agents/AGENT_HELP_HUMAN.md"),
        b"different future role file",
    )
    .unwrap();
    let current = BTreeMap::from([
        (
            "AGENTS.md".into(),
            Ok(std::fs::read(tmp.0.join("AGENTS.md")).unwrap()),
        ),
        (
            "agents/AGENT_HELP_HUMAN.md".into(),
            Ok(std::fs::read(tmp.0.join("agents/AGENT_HELP_HUMAN.md")).unwrap()),
        ),
    ]);
    let changes = bound.changes(&current);
    assert_eq!(changes.len(), 2);
    assert!(changes
        .iter()
        .all(|c| c["appliesTo"] == "future-conversations"
            && c["currentConversationRoleChanged"] == false));
    assert_eq!(bound.evidence(), before);
    assert_eq!(
        bound.role_in_force("home-A", "thread-9"),
        RoleInForce::AppObserved {
            role: Some(Role::HELP_HUMAN),
            supply_ref: "sup:9".into()
        }
    );
    assert!(bound
        .changes(&BTreeMap::new())
        .iter()
        .all(|c| c["reason"] == "missing"));
}
#[test]
fn full_generation_and_request_correlation_are_not_name_matching() {
    let c = composition(Some(Role::WORKING_ITEMS), "");
    for changed in [
        generation("home-B", 1),
        generation("home-A", 2),
        json!({"appSession":"session-B","home":"home-A","spawnCounter":1}),
    ] {
        let pending = PreparedStart::new(
            "home-A",
            generation("home-A", 1),
            json!(1),
            "req:1",
            "sup:1",
            &c,
        )
        .unwrap();
        assert!(pending
            .observe(&changed, &sent_start(1, &c), &frame(1, "t"))
            .is_err());
    }
    for bad in [
        json!(1),
        json!({"appSession":"s","home":"home-A"}),
        json!({"appSession":"s","home":"home-A","spawnCounter":0}),
        json!({"appSession":"s","home":"home-B","spawnCounter":1}),
    ] {
        assert!(PreparedStart::new("home-A", bad, json!(1), "r", "sup:r", &c).is_err());
    }
    for f in [
        frame(2, "t"),
        json!({"id":1,"error":{"code":-1}}),
        json!({"id":1,"result":{"thread":{"id":""}}}),
    ] {
        let pending = PreparedStart::new(
            "home-A",
            generation("home-A", 1),
            json!(1),
            "req:1",
            "sup:1",
            &c,
        )
        .unwrap();
        assert!(pending
            .observe(&generation("home-A", 1), &sent_start(1, &c), &f)
            .is_err());
    }
}
#[test]
fn malformed_or_mixed_source_binding_refuses_before_native_start() {
    let original = composition(Some(Role::HELP_HUMAN), "");
    let mut variants = vec![];
    let mut c = original.clone();
    c.carried["developerInstructions"]["parts"][1]["role"] = json!("TASK");
    variants.push(c);
    let mut c = original.clone();
    c.role = Some(Role::WORKING_ITEMS);
    variants.push(c);
    let mut c = original.clone();
    c.carried["developerInstructions"]["parts"][0]["source"]["release"] = json!("");
    variants.push(c);
    let mut c = original.clone();
    c.carried["developerInstructions"]["parts"]
        .as_array_mut()
        .unwrap()
        .pop();
    variants.push(c);
    let mut c = original.clone();
    c.text.push_str("tampered");
    variants.push(c);
    let mut c = original.clone();
    c.carried["baseInstructions"] = json!("replacement");
    variants.push(c);
    let mut c = original.clone();
    c.carried["developerInstructions"]["parts"][0]["source"]
        .as_object_mut()
        .unwrap()
        .remove("defaultContent");
    variants.push(c);
    let mut c = original.clone();
    c.carried["developerInstructions"]["parts"][0]["source"]["state"] = json!("default");
    variants.push(c);
    for c in variants {
        assert!(PreparedStart::new(
            "home-A",
            generation("home-A", 1),
            json!(1),
            "req:1",
            "sup:1",
            &c
        )
        .is_err());
    }
}
#[test]
fn exact_resume_packet_has_no_new_role_guidance_destination_or_policy() {
    let bound = binding(Some(Role::HELP_HUMAN));
    let old = bound.evidence();
    let current = generation("home-A", 2);
    let resume = bound
        .resume("home-A", current.clone(), json!(7), "req:resume")
        .unwrap();
    assert_eq!(resume.method(), "thread/resume");
    assert_eq!(resume.params(), json!({"threadId":"original-thread"}));
    assert_eq!(resume.home(), "home-A");
    assert_eq!(resume.generation(), &current);
    assert_eq!(resume.request_id(), &json!(7));
    assert_eq!(resume.request_ref(), "req:resume");
    let mut native = frame(7, "original-thread");
    native["result"]["thread"]["agentRole"] = json!("TASK");
    let resumed = resume
        .observe(&current, &sent_metadata(7, "thread/resume"), &native)
        .unwrap();
    assert_eq!(resumed.evidence(), old);
    assert!(bound
        .resume("home-B", generation("home-B", 1), json!(8), "req:8")
        .is_err());
    let mismatch = bound
        .resume("home-A", current.clone(), json!(9), "req:9")
        .unwrap();
    assert!(mismatch
        .observe(
            &current,
            &sent_metadata(9, "thread/resume"),
            &frame(9, "another-thread")
        )
        .is_err());
}
#[test]
fn fork_inherits_only_original_app_binding_and_native_source_relation() {
    let bound = binding(Some(Role::WORKING_ITEMS));
    let current = generation("home-A", 2);
    let fork = bound
        .fork("home-A", current.clone(), json!(4), "req:fork", "sup:fork")
        .unwrap();
    assert_eq!(fork.method(), "thread/fork");
    assert_eq!(fork.params(), json!({"threadId":"original-thread"}));
    let mut response = frame(4, "new-fork");
    response["result"]["thread"]["forkedFromId"] = json!("original-thread");
    response["result"]["thread"]["agentRole"] = json!("TASK");
    let inherited = fork
        .observe(&current, &sent_metadata(4, "thread/fork"), &response)
        .unwrap();
    assert_eq!(inherited.thread(), "new-fork");
    assert_eq!(inherited.home(), bound.home());
    assert_eq!(inherited.supply_ref(), "sup:fork");
    assert_eq!(
        inherited.evidence()["binding"]["original"],
        bound.evidence()["binding"]["original"]
    );
    assert_eq!(
        inherited.evidence()["binding"]["origin"]["kind"],
        "inherited-fork"
    );
    assert_eq!(inherited.evidence()["adoption"], "unknown");
    let bad = bound
        .fork("home-A", current.clone(), json!(5), "req:5", "sup:5")
        .unwrap();
    assert!(bad
        .observe(
            &current,
            &sent_metadata(5, "thread/fork"),
            &frame(5, "unrelated-fork")
        )
        .is_err());
}
#[test]
fn imported_files_missing_and_foreign_bindings_remain_unknown() {
    let bound = binding(Some(Role::HELP_HUMAN));
    let serialized = bound.evidence();
    let mut registry = RoleBindings::default();
    assert!(matches!(
        registry.selected_role("home-A", "original-thread"),
        RoleInForce::Unknown { .. }
    ));
    assert!(matches!(
        RoleBindings::imported_role(&serialized),
        RoleInForce::Unknown { .. }
    ));
    let mut tampered = serialized.clone();
    tampered["binding"]["original"]["role"] = json!("TASK");
    for imported in [
        serialized,
        tampered,
        json!({"format":"chirality.role.binding/0.1"}),
        json!(null),
    ] {
        assert!(matches!(
            RoleBindings::imported_role(&imported),
            RoleInForce::Unknown { .. }
        ));
    }
    registry.insert(bound.clone()).unwrap();
    assert!(matches!(
        registry.selected_role("home-B", "original-thread"),
        RoleInForce::Unknown { .. }
    ));
    assert!(matches!(
        registry.selected_role("home-A", "other-thread"),
        RoleInForce::Unknown { .. }
    ));
    let c = composition(Some(Role::HELPS_HUMANS), "replacement");
    let replacement = PreparedStart::new(
        "home-A",
        generation("home-A", 1),
        json!(10),
        "req:10",
        "sup:replacement",
        &c,
    )
    .unwrap()
    .observe(
        &generation("home-A", 1),
        &sent_start(10, &c),
        &frame(10, "original-thread"),
    )
    .unwrap();
    assert!(registry.insert(replacement).is_err());
    assert_eq!(
        registry
            .get("home-A", "original-thread")
            .unwrap()
            .evidence(),
        bound.evidence()
    );
    let none = binding(None);
    assert_eq!(
        none.role_in_force("home-A", "original-thread"),
        RoleInForce::AppObserved {
            role: None,
            supply_ref: "sup:original".into()
        }
    );
}
struct TempDir(std::path::PathBuf);
impl TempDir {
    fn new() -> Self {
        let mut bytes = [0; 16];
        getrandom::fill(&mut bytes).unwrap();
        let path =
            std::env::temp_dir().join(format!("role-lifecycle-{}", util::sha256_hex(&bytes)));
        std::fs::create_dir(&path).unwrap();
        Self(path)
    }
}
impl Drop for TempDir {
    fn drop(&mut self) {
        let _ = std::fs::remove_dir_all(&self.0);
    }
}

#[test]
fn substituted_outbound_guidance_or_override_on_resume_cannot_bind() {
    let c = composition(Some(Role::HELP_HUMAN), "");
    let pending = PreparedStart::new(
        "home-A",
        generation("home-A", 1),
        json!(1),
        "req:1",
        "sup:1",
        &c,
    )
    .unwrap();
    let mut sent = sent_start(1, &c);
    sent["params"]["developerInstructions"] = json!("different actual supplied bytes");
    assert!(pending
        .observe(
            &generation("home-A", 1),
            &sent,
            &frame(1, "original-thread")
        )
        .is_err());
    let b = binding(Some(Role::HELP_HUMAN));
    let gen = generation("home-A", 2);
    let resume = b.resume("home-A", gen.clone(), json!(2), "req:2").unwrap();
    let mut request = sent_metadata(2, "thread/resume");
    request["params"]["developerInstructions"] = json!("edited role");
    assert!(resume
        .observe(&gen, &request, &frame(2, "original-thread"))
        .is_err());
}

#[test]
fn minimal_or_malformed_native_results_do_not_establish_app_role() {
    let c = composition(Some(Role::HELP_HUMAN), "");
    let minimal = json!({"id":1,"result":{"thread":{"id":"thread"}}});
    let mut malformed = frame(1, "thread");
    malformed["result"]["thread"]["agentRole"] = json!({"name":"TASK"});
    let mut results = vec![minimal, malformed];
    for key in [
        "model",
        "modelProvider",
        "cwd",
        "approvalPolicy",
        "approvalsReviewer",
        "sandbox",
    ] {
        let mut f = frame(1, "thread");
        f["result"].as_object_mut().unwrap().remove(key);
        results.push(f);
    }
    for key in ["cliVersion", "source", "status", "turns"] {
        let mut f = frame(1, "thread");
        f["result"]["thread"].as_object_mut().unwrap().remove(key);
        results.push(f);
    }
    for f in results {
        let pending = PreparedStart::new(
            "home-A",
            generation("home-A", 1),
            json!(1),
            "req:1",
            "sup:1",
            &c,
        )
        .unwrap();
        assert!(pending
            .observe(&generation("home-A", 1), &sent_start(1, &c), &f)
            .is_err());
    }
    let b = binding(Some(Role::HELP_HUMAN));
    let g = generation("home-A", 2);
    for is_fork in [false, true] {
        let method = if is_fork {
            "thread/fork"
        } else {
            "thread/resume"
        };
        let pending = if is_fork {
            b.fork("home-A", g.clone(), json!(3), "req:3", "sup:3")
                .unwrap()
        } else {
            b.resume("home-A", g.clone(), json!(3), "req:3").unwrap()
        };
        let mut f = frame(3, if is_fork { "fork" } else { "original-thread" });
        f["result"]["thread"]["forkedFromId"] = json!("original-thread");
        f["result"].as_object_mut().unwrap().remove("sandbox");
        assert!(pending.observe(&g, &sent_metadata(3, method), &f).is_err());
    }
}
#[test]
fn native_owner_settings_are_reported_without_false_base_preservation_or_config_veto() {
    let c = composition(Some(Role::HELP_HUMAN), "");
    let p = PreparedStart::new(
        "home-A",
        generation("home-A", 1),
        json!(1),
        "req:1",
        "sup:1",
        &c,
    )
    .unwrap();
    let mut sent = sent_start(1, &c);
    sent["params"]["baseInstructions"] = json!("user-selected-native-base-private");
    sent["params"]["config"] = json!({"user_choice":"private-config-value"});
    sent["params"]["approvalPolicy"] = json!("never");
    let b = p
        .observe(&generation("home-A", 1), &sent, &frame(1, "thread"))
        .unwrap();
    let e = b.evidence();
    let account = &e["binding"]["observation"]["role_carrier_observation"];
    assert_eq!(account["baseInstructionsPresent"], true);
    assert_eq!(account["configPresent"], true);
    assert_eq!(
        account["nativeBaseAndConfigurationPreservation"],
        "not-established-by-role-binding"
    );
    assert!(account["nonRoleSettingKeys"]
        .as_array()
        .unwrap()
        .contains(&json!("approvalPolicy")));
    assert_eq!(
        e["binding"]["observation"]["reported_settings"]["model"],
        "reported-model"
    );
    assert!(!e.to_string().contains("user-selected-native-base-private"));
    assert!(!e.to_string().contains("private-config-value"));
}
