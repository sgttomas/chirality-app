//! DEL-02-04: the App's delegation guidance as one more part of the guidance
//! supplied at a conversation's start (REQ-002, REQ-007; AC-002, AC-005,
//! AC-007). Expected bytes come from the files on disk and the scope's
//! framing; digests are computed here with SHA-256 directly, not product code.
use crate::role_supply::{Composition, Role};
use crate::runtime_session::{compose_role, compose_role_from, missing_guidance_reason, seed_instructions};
use serde_json::{json, Value};
use sha2::{Digest, Sha256};
use std::path::{Path, PathBuf};

const DELEGATION: &str = "DELEGATION_RECORDS.md";

fn sha(bytes: &[u8]) -> String {
    Sha256::digest(bytes).iter().map(|b| format!("{b:02x}")).collect()
}
fn shipped(path: &str) -> Vec<u8> {
    std::fs::read(Path::new(env!("CARGO_MANIFEST_DIR")).join("resources/instructions").join(path)).unwrap()
}
/// Roles whose role-set row may delegate, read from the shipped data itself.
fn delegating_roles() -> Vec<Role> {
    let set: Value = serde_json::from_slice(&shipped("roles.json")).unwrap();
    set["roles"]
        .as_array()
        .unwrap()
        .iter()
        .filter(|r| r["delegation"] == "may-delegate")
        .map(|r| serde_json::from_value(r["name"].clone()).unwrap())
        .collect()
}
struct Temp(PathBuf);
impl Temp {
    fn new() -> Self {
        let p = std::env::temp_dir().canonicalize().unwrap().join(crate::util::opaque_id("delegation-guidance-").unwrap());
        std::fs::create_dir(&p).unwrap();
        Self(p)
    }
    fn store(&self) -> PathBuf {
        self.0.join("instructions")
    }
}
impl Drop for Temp {
    fn drop(&mut self) {
        let _ = std::fs::remove_dir_all(&self.0);
    }
}
fn role_path(role: Role) -> String {
    format!("agents/AGENT_{}.md", role.name())
}
/// What the scope says is carried: product guidance; then, with a role, a
/// heading line naming it and the role document; then, for a role that may
/// delegate, a heading line and the delegation guidance.
fn expected(store: &Path, role: Option<Role>, delegation: bool) -> Vec<u8> {
    let mut bytes = std::fs::read(store.join("AGENTS.md")).unwrap();
    if let Some(role) = role {
        bytes.extend_from_slice(format!("\n\n# Active role: {}\n\n", role.name()).as_bytes());
        bytes.extend(std::fs::read(store.join(role_path(role))).unwrap());
    }
    if delegation {
        bytes.extend_from_slice(b"\n\n# Delegation guidance\n\n");
        bytes.extend(std::fs::read(store.join(DELEGATION)).unwrap());
    }
    bytes
}
fn parts(c: &Composition) -> Vec<Value> {
    c.carried["developerInstructions"]["parts"].as_array().unwrap().clone()
}
fn carried_bytes(c: &Composition) -> Vec<u8> {
    let params = c.start_params().unwrap();
    assert!(params.get("baseInstructions").is_none(), "base instructions are never set");
    params["developerInstructions"].as_str().unwrap().as_bytes().to_vec()
}

#[test]
fn delegating_roles_start_with_product_role_then_delegation_bytes_as_on_disk() {
    let t = Temp::new();
    let store = t.store();
    seed_instructions(&store).unwrap();
    // Invented, edited copies: the person's bytes are what is carried.
    std::fs::write(store.join("AGENTS.md"), "Invented product guidance ü\r\n").unwrap();
    std::fs::write(store.join(DELEGATION), "Invented delegation guidance ✓\r\n").unwrap();
    let roles = delegating_roles();
    assert_eq!(roles, [Role::HELP_HUMAN, Role::HELPS_HUMANS, Role::WORKING_ITEMS]);
    for role in roles {
        std::fs::write(store.join(role_path(role)), format!("Invented {} document\n", role.name())).unwrap();
        let c = compose_role(&store, Some(role)).unwrap();
        let want = expected(&store, Some(role), true);
        assert_eq!(carried_bytes(&c), want, "{role:?}");
        let prepared = crate::role_lifecycle::PreparedStart::new("home", json!({"appSession":"s","home":"home","spawnCounter":1}), json!(1), "req:1", "sup:1", &c).unwrap();
        assert_eq!(prepared.guidance_params(), json!({"developerInstructions": String::from_utf8(want.clone()).unwrap()}));
        assert_eq!(c.carried["compositionFormat"], "chirality.role.compose/0.3");
        assert_eq!(c.carried["baseInstructions"], "not-set");
        assert_eq!(c.carried["developerInstructions"]["content"]["value"], sha(&want));
        let p = parts(&c);
        assert_eq!(p.len(), 3);
        for (part, (kind, path)) in p.iter().zip([("product-guidance", "AGENTS.md".to_owned()), ("role-guidance", role_path(role)), ("delegation-guidance", DELEGATION.to_owned())]) {
            let file = std::fs::read(store.join(&path)).unwrap();
            assert_eq!(part["kind"], kind);
            assert_eq!(part["source"]["path"], path.as_str());
            assert_eq!(part["content"]["method"], "chirality.app.exact-bytes.sha256/v1");
            assert_eq!(part["content"]["value"], sha(&file), "{path}");
            // A role document modified by the person still gets the delegation
            // text; each part's own state is recorded.
            assert_eq!(part["source"]["state"], "modified", "{path}");
            let offset = part["offset"].as_u64().unwrap() as usize;
            assert_eq!(&want[offset..offset + part["length"].as_u64().unwrap() as usize], file.as_slice());
        }
        assert!(p[2].get("role").is_none());
    }
    // No role: the product guidance alone.
    let none = compose_role(&store, None).unwrap();
    assert_eq!(carried_bytes(&none), std::fs::read(store.join("AGENTS.md")).unwrap());
    assert_eq!(parts(&none).len(), 1);
    // TASK is not a conversation role.
    assert!(compose_role(&store, Some(Role::TASK)).is_err());
}

#[test]
fn unedited_store_supplies_the_shipped_delegation_text_as_default() {
    let t = Temp::new();
    seed_instructions(&t.store()).unwrap();
    let c = compose_role(&t.store(), Some(Role::HELP_HUMAN)).unwrap();
    let part = &parts(&c)[2];
    assert_eq!(part["content"]["value"], sha(&shipped(DELEGATION)));
    assert_eq!(part["source"]["state"], "default");
    assert_eq!(part["source"]["reviewedDefault"]["content"]["value"], sha(&shipped(DELEGATION)));
    assert_eq!(part["source"]["seedHistory"]["status"], "declared");
    assert!(carried_bytes(&c).ends_with(&shipped(DELEGATION)));
}

fn namespace_reading(root: &Path) -> Value {
    std::fs::create_dir_all(root.join("home")).unwrap();
    std::fs::write(root.join("home/config.toml"), "").unwrap();
    json!({"config":{"agents":null},"origins":{},"layers":[{"name":{"type":"sessionFlags"},"version":"s","config":{}},{"name":{"type":"user","file":root.join("home/config.toml"),"profile":null},"version":"u","config":{}},{"name":{"type":"system","file":root.join("system/config.toml")},"version":"y","config":{}}]})
}

#[test]
fn a_delegated_manager_is_given_the_text_and_a_task_child_is_not() {
    let t = Temp::new();
    let store = t.store();
    seed_instructions(&store).unwrap();
    std::fs::write(store.join(DELEGATION), "Invented delegation guidance for children\n").unwrap();
    let delegation = std::fs::read(store.join(DELEGATION)).unwrap();
    let reading = namespace_reading(&t.0);
    for parent in [Role::HELP_HUMAN, Role::HELPS_HUMANS, Role::WORKING_ITEMS] {
        let mut c = compose_role(&store, Some(parent)).unwrap();
        crate::child_roles::prepare(&mut c, crate::child_roles::Namespace::observe(&reading), &store, &t.0);
        c.verify().unwrap();
        assert_eq!(c.children.len(), parent.child_roles().len());
        for child in &c.children {
            let envelope: toml::Value = toml::from_str(std::str::from_utf8(&child.envelope).unwrap()).unwrap();
            let given = envelope["developer_instructions"].as_str().unwrap().as_bytes();
            let manager = delegating_roles().contains(&child.role);
            assert_eq!(given, expected(&store, Some(child.role), manager).as_slice(), "{parent:?} -> {:?}", child.role);
            if child.role == Role::TASK {
                assert!(!given.windows(delegation.len()).any(|w| w == delegation.as_slice()));
                assert!(!String::from_utf8_lossy(given).contains("# Delegation guidance"));
            }
            let supplied = c.carried["nativeChildRoles"].as_array().unwrap().iter()
                .find(|r| r["role"] == json!(child.role) && r["status"] == "supplied").unwrap();
            assert_eq!(supplied["composed"]["value"], sha(given));
        }
    }
}

fn legacy_store(t: &Temp) -> PathBuf {
    // A store first seeded by a release without the delegation guidance: five
    // files and a first seed record naming those five.
    let store = t.store();
    std::fs::create_dir_all(store.join("agents")).unwrap();
    let mut created = vec![];
    for (path, bytes) in std::iter::once(("AGENTS.md".to_owned(), shipped("AGENTS.md")))
        .chain(Role::ALL.into_iter().map(|r| (role_path(r), shipped(&role_path(r)))))
    {
        std::fs::write(store.join(&path), &bytes).unwrap();
        created.push(json!({"path":path,"defaultContent":{"method":"chirality.app.exact-bytes.sha256/v1","value":sha(&bytes)}}));
    }
    let record = json!({"format":"chirality.instruction-seed-record/1","release":"an-earlier-release","created":created,"preserved":[]});
    std::fs::write(store.join(".seed-record.json"), format!("{record}\n")).unwrap();
    store
}
fn snapshot(store: &Path) -> Vec<(String, Vec<u8>, (u64, i64, i64))> {
    use std::os::unix::fs::MetadataExt;
    let mut out = vec![];
    for path in ["AGENTS.md", ".seed-record.json"].into_iter().map(str::to_owned).chain(Role::ALL.into_iter().map(role_path)) {
        let m = std::fs::symlink_metadata(store.join(&path)).unwrap();
        out.push((path.clone(), std::fs::read(store.join(&path)).unwrap(), (m.ino(), m.mtime(), m.mtime_nsec())));
    }
    out
}

#[test]
fn store_seeded_into_an_empty_folder_holds_every_shipped_default() {
    let t = Temp::new();
    seed_instructions(&t.store()).unwrap();
    for path in ["AGENTS.md".to_owned(), DELEGATION.to_owned()].into_iter().chain(Role::ALL.into_iter().map(role_path)) {
        assert_eq!(std::fs::read(t.store().join(&path)).unwrap(), shipped(&path), "{path}");
    }
    let record: Value = serde_json::from_slice(&std::fs::read(t.store().join(".seed-record.json")).unwrap()).unwrap();
    assert!(record["created"].as_array().unwrap().iter().any(|e| e["path"] == DELEGATION));
    assert!(!t.store().join(".seed-addition-DELEGATION_RECORDS.json").exists());
}

#[test]
fn a_store_that_predates_the_file_gains_it_once_and_nothing_else_changes() {
    let t = Temp::new();
    let store = legacy_store(&t);
    std::fs::write(store.join("agents/AGENT_HELP_HUMAN.md"), "The person's edited HELP_HUMAN\n").unwrap();
    let before = snapshot(&store);
    seed_instructions(&store).unwrap();
    assert_eq!(snapshot(&store), before, "a file already in the store was touched");
    assert_eq!(std::fs::read(store.join(DELEGATION)).unwrap(), shipped(DELEGATION));
    let addition: Value = serde_json::from_slice(&std::fs::read(store.join(".seed-addition-DELEGATION_RECORDS.json")).unwrap()).unwrap();
    assert_eq!(addition["format"], "chirality.instruction-seed-addition/1");
    assert_eq!(addition["created"][0]["path"], DELEGATION);
    assert_eq!(addition["created"][0]["defaultContent"]["value"], sha(&shipped(DELEGATION)));
    let c = compose_role(&store, Some(Role::HELP_HUMAN)).unwrap();
    let p = parts(&c);
    assert_eq!(p[1]["source"]["state"], "modified");
    assert_eq!(p[2]["source"]["state"], "default");
    assert_eq!(p[2]["source"]["seedHistory"]["record"]["path"], ".seed-addition-DELEGATION_RECORDS.json");
    assert_eq!(p[1]["source"]["seedHistory"]["record"]["path"], ".seed-record.json");
    // A later start adds nothing again.
    let added = std::fs::read(store.join(".seed-addition-DELEGATION_RECORDS.json")).unwrap();
    seed_instructions(&store).unwrap();
    assert_eq!(std::fs::read(store.join(".seed-addition-DELEGATION_RECORDS.json")).unwrap(), added);
    // Once placed, its absence is the person's: refused, never restored.
    std::fs::remove_file(store.join(DELEGATION)).unwrap();
    assert_missing_refuses_and_no_role_starts(&store);
}

/// The delegation guidance is absent and the App placed nothing: a start in
/// each role that may delegate is refused with the missing-file reason; a
/// start with no role carries the product guidance alone; once the person
/// puts the file back, a delegating start is supplied it.
fn assert_missing_refuses_and_no_role_starts(store: &Path) {
    seed_instructions(store).unwrap();
    assert!(!store.join(DELEGATION).exists(), "the App put the file back");
    for role in delegating_roles() {
        assert_eq!(compose_role(store, Some(role)).unwrap_err(), missing_guidance_reason(store, DELEGATION, false, None), "{role:?}");
    }
    let none = compose_role(store, None).unwrap();
    assert_eq!(carried_bytes(&none), std::fs::read(store.join("AGENTS.md")).unwrap());
    // The person's own act; the App offers no restore control (see the PR).
    std::fs::write(store.join(DELEGATION), shipped(DELEGATION)).unwrap();
    let c = compose_role(store, Some(Role::HELP_HUMAN)).unwrap();
    assert_eq!(carried_bytes(&c), expected(store, Some(Role::HELP_HUMAN), true));
    assert_eq!(parts(&c)[2]["source"]["state"], "default");
}

#[test]
fn without_a_readable_seed_record_nothing_is_placed_and_the_file_reads_as_missing() {
    let corrupt: [(&str, fn(&Path)); 4] = [
        ("deleted", |p| std::fs::remove_file(p).unwrap()),
        ("corrupted", |p| std::fs::write(p, b"{\"format\":").unwrap()),
        ("names other paths", |p| std::fs::write(p, br#"{"format":"chirality.instruction-seed-record/1","release":"r","created":[],"preserved":[]}"#).unwrap()),
        ("linked", |p| {
            let target = p.with_file_name("record-elsewhere.json");
            std::fs::rename(p, &target).unwrap();
            std::os::unix::fs::symlink(&target, p).unwrap();
        }),
    ];
    for (case, apply) in corrupt {
        // A store seeded with the file, then the file deleted and the record lost.
        let t = Temp::new();
        let store = t.store();
        seed_instructions(&store).unwrap();
        std::fs::remove_file(store.join(DELEGATION)).unwrap();
        apply(&store.join(".seed-record.json"));
        assert_missing_refuses_and_no_role_starts(&store);
        assert!(!store.join(".seed-addition-DELEGATION_RECORDS.json").exists(), "{case}");
        // An older store whose record is lost likewise gains nothing.
        let t = Temp::new();
        let store = legacy_store(&t);
        apply(&store.join(".seed-record.json"));
        assert_missing_refuses_and_no_role_starts(&store);
        assert!(!store.join(".seed-addition-DELEGATION_RECORDS.json").exists(), "{case}");
    }
}

#[test]
fn a_store_seeded_with_the_file_never_has_it_restored_and_a_present_file_is_kept() {
    let t = Temp::new();
    seed_instructions(&t.store()).unwrap();
    std::fs::remove_file(t.store().join(DELEGATION)).unwrap();
    assert_missing_refuses_and_no_role_starts(&t.store());

    // An older store where the person already has a file of that name.
    let t = Temp::new();
    let store = legacy_store(&t);
    std::fs::write(store.join(DELEGATION), "The person's own notes\n").unwrap();
    seed_instructions(&store).unwrap();
    assert_eq!(std::fs::read(store.join(DELEGATION)).unwrap(), b"The person's own notes\n");
    let addition: Value = serde_json::from_slice(&std::fs::read(store.join(".seed-addition-DELEGATION_RECORDS.json")).unwrap()).unwrap();
    assert_eq!(addition["preserved"], json!([{"path":DELEGATION,"origin":"unknown"}]));
    let c = compose_role(&store, Some(Role::WORKING_ITEMS)).unwrap();
    assert_eq!(parts(&c)[2]["source"]["state"], "modified");
    assert_eq!(parts(&c)[2]["source"]["seedHistory"], json!({"status":"unestablished","reason":"preserved-path"}));
}

#[test]
fn an_edit_between_two_starts_reaches_the_second_only() {
    let t = Temp::new();
    let store = t.store();
    seed_instructions(&store).unwrap();
    let first = compose_role(&store, Some(Role::HELP_HUMAN)).unwrap();
    let first_text = first.text.clone();
    std::fs::write(store.join(DELEGATION), "Edited between starts\n").unwrap();
    let second = compose_role(&store, Some(Role::HELP_HUMAN)).unwrap();
    assert_eq!(first.text, first_text);
    assert!(first.text.as_bytes().ends_with(&shipped(DELEGATION)));
    assert_eq!(carried_bytes(&second), expected(&store, Some(Role::HELP_HUMAN), true));
    assert_eq!(parts(&second)[2]["source"]["state"], "modified");
    assert_eq!(parts(&second)[2]["content"]["value"], sha(b"Edited between starts\n"));
}

#[test]
fn each_unreadable_delegation_file_refuses_the_start_without_a_default() {
    use std::os::unix::fs::PermissionsExt;
    let cases: [(&str, fn(&Path)); 4] = [
        ("missing", |p| std::fs::remove_file(p).unwrap()),
        ("unreadable", |p| std::fs::set_permissions(p, std::fs::Permissions::from_mode(0o000)).unwrap()),
        ("linked", |p| {
            let target = p.with_file_name("elsewhere.md");
            std::fs::write(&target, "Readable bytes elsewhere\n").unwrap();
            std::fs::remove_file(p).unwrap();
            std::os::unix::fs::symlink(&target, p).unwrap();
        }),
        ("not UTF-8", |p| std::fs::write(p, [0xff, 0xfe, b'\n']).unwrap()),
    ];
    for (case, apply) in cases {
        let t = Temp::new();
        let store = t.store();
        seed_instructions(&store).unwrap();
        let file = store.join(DELEGATION);
        apply(&file);
        if case == "unreadable" && std::fs::read(&file).is_ok() {
            continue; // a privileged test user reads any mode
        }
        for role in delegating_roles() {
            assert!(compose_role(&store, Some(role)).is_err(), "{case}: {role:?}");
        }
        // The store stays usable: only starts that read this file are refused.
        seed_instructions(&store).unwrap();
        assert!(compose_role(&store, None).is_ok(), "{case}");
        assert!(std::fs::symlink_metadata(&file).is_err() || std::fs::read(&file).map_or(true, |b| b != shipped(DELEGATION)), "{case}: default substituted");
        let _ = std::fs::set_permissions(&file, std::fs::Permissions::from_mode(0o600));
    }
}

#[test]
fn supply_records_validate_with_the_new_part_and_earlier_records_still_read() {
    let schema: Value = serde_json::from_str(include_str!("../resources/workflow_role/role-supply-record.schema.json")).unwrap();
    let validator = jsonschema::options().offline().build(&schema).unwrap();
    let t = Temp::new();
    seed_instructions(&t.store()).unwrap();
    let c = compose_role(&t.store(), Some(Role::HELP_HUMAN)).unwrap();
    let record = c.start_record("sup:new", "thread", "req", 1, None).unwrap();
    validator.validate(&record).unwrap();
    // As recorded before this change: format 0.2, product guidance and role.
    let p = parts(&c);
    let end = (p[1]["offset"].as_u64().unwrap() + p[1]["length"].as_u64().unwrap()) as usize;
    let text = c.text[..end].to_owned();
    let mut carried = c.carried.clone();
    carried["compositionFormat"] = json!("chirality.role.compose/0.2");
    carried["developerInstructions"] = json!({"content":{"method":"chirality.app.exact-bytes.sha256/v1","value":sha(text.as_bytes())},"byteLength":text.len(),"parts":p[..2].to_vec()});
    let old = Composition::quoted(Some(Role::HELP_HUMAN), c.role_set_identity().clone(), text, carried.clone()).unwrap();
    validator.validate(&old.start_record("sup:old", "thread", "req", 1, None).unwrap()).unwrap();
    // A 0.2 composition never had a delegation part, and none may claim one.
    let mut mislabelled = record.clone();
    mislabelled["carried"]["compositionFormat"] = json!("chirality.role.compose/0.2");
    assert!(validator.validate(&mislabelled).is_err());
    assert!(Composition::quoted(Some(Role::HELP_HUMAN), c.role_set_identity().clone(), c.text.clone(), mislabelled["carried"].clone()).is_err());
    // Neither no role nor TASK carries it.
    for role in ["none", "TASK"] {
        let mut wrong = record.clone();
        wrong["selection"]["role"] = json!(role);
        assert!(validator.validate(&wrong).is_err(), "{role}");
    }
}

/// Fill the text's `<...>` placeholders with values of the kind each names.
fn fill(block: &str) -> String {
    let mut out = String::new();
    let mut rest = block;
    while let Some(start) = rest.find('<') {
        let Some(len) = rest[start..].find('>') else { break };
        let name = &rest[start + 1..start + len];
        out.push_str(&rest[..start]);
        out.push_str(if name.contains("SHA-256") {
            "0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef"
        } else if name.contains("recordId") {
            "fl:example.other"
        } else if name == "unique within the project" {
            "example.1"
        } else if name == "date and time" {
            "2026-11-12T09:00:00Z"
        } else if name.contains("role") {
            "HELP_HUMAN"
        } else {
            "example"
        });
        rest = &rest[start + len + 1..];
    }
    out.push_str(rest);
    out
}

#[test]
fn the_shipped_texts_record_skeletons_are_valid_records() {
    let text = std::str::from_utf8(crate::runtime_session::DELEGATION_DEFAULT).unwrap();
    assert_eq!(text.as_bytes(), shipped(DELEGATION).as_slice());
    let blocks: Vec<&str> = text.split("```json\n").skip(1).map(|b| b.split("```").next().unwrap()).collect();
    let fleet: Value = serde_json::from_str(include_str!("../schemas/fleet.record.schema.json")).unwrap();
    let fleet = jsonschema::options().offline().build(&fleet).unwrap();
    let mut package: Value = serde_json::from_str(include_str!("../schemas/checkpoint-record-entries.schema.json")).unwrap();
    package["$ref"] = json!("#/$defs/decisionPackageFile");
    let package = jsonschema::options().offline().build(&package).unwrap();
    // The first block is the shared header, written into every record.
    let header = blocks[0].trim().replace("\"kind\": \"<kind>\",", "");
    let mut kinds = vec![];
    for block in &blocks[1..] {
        if block.trim_start().starts_with("{\"format\": \"chirality.decision-package\"") {
            let value: Value = serde_json::from_str(&fill(block)).unwrap();
            package.validate(&value).unwrap();
            kinds.push("decision package".to_owned());
            continue;
        }
        for record in block.trim().split("\n{HEADER").map(|r| if r.starts_with("{HEADER") { r.to_owned() } else { format!("{{HEADER{r}") }) {
            let record = record.replacen("{HEADER, ", &format!("{{{}, ", header.trim_end()), 1);
            let value: Value = serde_json::from_str(&fill(&record)).unwrap_or_else(|e| panic!("{e}: {record}"));
            fleet.validate(&value).unwrap_or_else(|e| panic!("{}: {e}", value["kind"]));
            kinds.push(value["kind"].as_str().unwrap().to_owned());
        }
    }
    assert_eq!(kinds, ["brief", "work_graph", "current_graph", "return_recorded", "review_recorded", "integration_recorded", "basis_changed", "decision package"]);
    // Every record kind the text names is either reserved to the App, in the
    // sentence that forbids it, or one an agent writes and has a skeleton above
    // that validates. A kind named without one fails here.
    let schema: Value = serde_json::from_str(include_str!("../schemas/fleet.record.schema.json")).unwrap();
    let format_kinds: Vec<String> = schema["$defs"]["header"]["properties"]["kind"]["enum"].as_array().unwrap()
        .iter().map(|k| k.as_str().unwrap().to_owned()).collect();
    let forbidding = text.split("Never write a line of kind ").nth(1).unwrap().split(", and never name").next().unwrap();
    let reserved: Vec<&String> = format_kinds.iter().filter(|k| forbidding.contains(&format!("`{k}`"))).collect();
    assert_eq!(reserved, ["dispatch_observed", "child_observed", "observation_ended", "related_conversation"]);
    for kind in &format_kinds {
        let named = text.contains(&format!("`{kind}`")) || text.contains(&format!("\"kind\": \"{kind}\""));
        if named && !reserved.contains(&kind) {
            assert!(kinds.contains(kind), "the text names `{kind}` for an agent to write without a valid skeleton");
        }
        if reserved.contains(&kind) {
            assert!(!kinds.contains(kind), "the text gives a skeleton for App-reserved `{kind}`");
        }
    }
    // The places the text names are the places the App reads.
    assert!(text.contains(&format!("`{}/<name>.json`", crate::recorder::DECISIONS_DIR)));
    for place in ["`.chirality/fleet/`", "`briefs/<item>.json`", "`graphs/<undertaking>/r<n>.json`", "`coordination.fleet.jsonl`", "chirality.app.exact-bytes.sha256/v1"] {
        assert!(text.contains(place), "{place}");
    }
    assert_eq!(crate::util::FILE_IDENTITY_METHOD, "chirality.app.exact-bytes.sha256/v1");
}

/// Words that would offer something the App does not have for a guidance file.
fn assert_offers_only_what_exists(reason: &str) {
    let lower = reason.to_lowercase();
    for offer in ["restore", "button", "click", "command", "setting", "menu", "reset", "repair"] {
        assert!(!lower.contains(offer), "the refusal offers `{offer}`: {reason}");
    }
    assert!(lower.contains("does not put a guidance file back by itself"), "{reason}");
}

#[test]
fn each_missing_guidance_file_is_refused_as_the_code_does_in_words_a_person_can_act_on() {
    let conversation: [Option<Role>; 4] = [None, Some(Role::HELP_HUMAN), Some(Role::HELPS_HUMANS), Some(Role::WORKING_ITEMS)];
    let files: Vec<String> = ["AGENTS.md".to_owned(), DELEGATION.to_owned()].into_iter().chain(Role::ALL.into_iter().map(role_path)).collect();
    for path in &files {
        // Found missing at a start, after the App started.
        let t = Temp::new();
        let store = t.store();
        seed_instructions(&store).unwrap();
        std::fs::remove_file(store.join(path)).unwrap();
        for role in conversation {
            let reads = path == "AGENTS.md"
                || role.is_some_and(|r| *path == role_path(r) || (*path == DELEGATION && r.may_delegate()));
            let result = compose_role(&store, role);
            if !reads {
                assert!(result.is_ok(), "{path} missing: {role:?} start");
                continue;
            }
            let reason = result.unwrap_err();
            assert_eq!(reason, missing_guidance_reason(&store, path, false, None));
            assert!(reason.contains(&store.display().to_string()) && reason.contains(&store.join(path).display().to_string()), "{reason}");
            assert_offers_only_what_exists(&reason);
            // A start with no role is offered exactly where it works.
            let no_role_works = compose_role(&store, None).is_ok();
            assert_eq!(reason.contains("start with no role"), no_role_works, "{reason}");
            assert_eq!(no_role_works, path != "AGENTS.md", "{path}");
            assert!(reason.contains("The shipped default is the copy the App carries."), "{reason}");
            // An installed build names its verified packaged copy.
            let packaged = Path::new(env!("CARGO_MANIFEST_DIR")).join("resources/instructions");
            crate::runtime_session::verify_production_instructions_root(&packaged).unwrap();
            let named = compose_role_from(&store, role, Some(&packaged)).unwrap_err();
            assert!(named.contains(&format!("The shipped default to copy from is {}.", packaged.join(path).display())), "{named}");
            assert!(packaged.join(path).is_file());
        }
        // Found missing by the store check when the App starts: every start is
        // refused until the App starts again, so no start is offered; the
        // delegation guidance is not part of that check.
        let checked = seed_instructions(&store);
        if path == DELEGATION {
            checked.unwrap();
        } else {
            let reason = checked.unwrap_err();
            assert_eq!(reason, missing_guidance_reason(&store, path, true, None));
            assert_offers_only_what_exists(&reason);
            assert!(!reason.contains("no role") && reason.contains("No conversation can start until it is back") && reason.contains("quit and reopen the App"), "{reason}");
        }
    }
}
