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
/// The whole store folder as it stands: every entry under it, by relative
/// name, with its kind, its bytes (or a link's target), inode and
/// modification time. Two equal listings mean nothing was written, replaced
/// or removed between them.
fn tree(store: &Path) -> Vec<(String, String, Vec<u8>, u64, i64, i64)> {
    use std::os::unix::fs::MetadataExt;
    fn walk(root: &Path, dir: &Path, out: &mut Vec<(String, String, Vec<u8>, u64, i64, i64)>) {
        for entry in std::fs::read_dir(dir).unwrap() {
            let path = entry.unwrap().path();
            let m = std::fs::symlink_metadata(&path).unwrap();
            let name = path.strip_prefix(root).unwrap().to_string_lossy().into_owned();
            let (kind, bytes) = if m.file_type().is_symlink() {
                ("link", std::fs::read_link(&path).unwrap().to_string_lossy().into_owned().into_bytes())
            } else if m.is_dir() {
                ("dir", vec![])
            } else {
                ("file", std::fs::read(&path).unwrap_or_else(|_| b"<unreadable>".to_vec()))
            };
            out.push((name, kind.to_owned(), bytes, m.ino(), m.mtime(), m.mtime_nsec()));
            if m.is_dir() && !m.file_type().is_symlink() {
                walk(root, &path, out);
            }
        }
    }
    let root = std::fs::symlink_metadata(store).unwrap();
    let mut out = vec![(".".to_owned(), "dir".to_owned(), vec![], root.ino(), root.mtime(), root.mtime_nsec())];
    walk(store, store, &mut out);
    out.sort();
    out
}

/// Two App starts (the store check at App start, twice) and a composition in
/// every conversation role and with no role, on an existing store. Asserts
/// that the whole store folder is unchanged by name, bytes, inode and
/// modification time, and returns each composition's result.
fn start_without_writing(store: &Path) -> Vec<(Option<Role>, Result<Composition, String>)> {
    let before = tree(store);
    let checked = [seed_instructions(store), seed_instructions(store)];
    let results: Vec<_> = [None, Some(Role::HELP_HUMAN), Some(Role::HELPS_HUMANS), Some(Role::WORKING_ITEMS)]
        .into_iter().map(|role| (role, compose_role(store, role))).collect();
    assert_eq!(tree(store), before, "an existing store was written, replaced or removed");
    for result in checked {
        result.unwrap();
    }
    results
}

/// The delegation guidance is absent: each delegating start is refused with
/// the missing-file sentence, and no role is supplied the product guidance alone.
fn assert_absent_refuses_delegating_roles_only(store: &Path, results: Vec<(Option<Role>, Result<Composition, String>)>) {
    assert!(std::fs::symlink_metadata(store.join(DELEGATION)).is_err(), "the delegation guidance appeared");
    for (role, result) in results {
        match role {
            None => assert_eq!(carried_bytes(&result.unwrap()), std::fs::read(store.join("AGENTS.md")).unwrap()),
            Some(role) => assert_eq!(result.unwrap_err(), missing_guidance_reason(store, DELEGATION, false, None), "{role:?}"),
        }
    }
}

/// The delegation guidance is present: each delegating start is supplied the
/// bytes on disk as they are, and returns the delegation part of each.
fn assert_present_is_read_as_it_is(store: &Path, results: Vec<(Option<Role>, Result<Composition, String>)>) -> Vec<Value> {
    let mut supplied = vec![];
    for (role, result) in results {
        let c = result.unwrap();
        assert_eq!(carried_bytes(&c), expected(store, role, role.is_some()), "{role:?}");
        if role.is_some() {
            supplied.push(parts(&c)[2].clone());
        }
    }
    supplied
}

/// (e) First seeding into an empty location creates the six guidance files and
/// one seed record naming them, and nothing else.
#[test]
fn first_seeding_creates_the_six_files_and_one_seed_record_and_nothing_else() {
    let t = Temp::new();
    seed_instructions(&t.store()).unwrap();
    let listing: Vec<(String, String)> = tree(&t.store()).into_iter().map(|(name, kind, ..)| (name, kind)).collect();
    let mut want: Vec<(String, String)> = [".", "agents"].iter().map(|n| (n.to_string(), "dir".to_owned()))
        .chain(["AGENTS.md", DELEGATION, ".seed-record.json"].iter().map(|n| (n.to_string(), "file".to_owned())))
        .chain(Role::ALL.into_iter().map(|r| (role_path(r), "file".to_owned()))).collect();
    want.sort();
    assert_eq!(listing, want);
    for path in ["AGENTS.md".to_owned(), DELEGATION.to_owned()].into_iter().chain(Role::ALL.into_iter().map(role_path)) {
        assert_eq!(std::fs::read(t.store().join(&path)).unwrap(), shipped(&path), "{path}");
    }
    let record: Value = serde_json::from_slice(&std::fs::read(t.store().join(".seed-record.json")).unwrap()).unwrap();
    let mut named: Vec<&str> = record["created"].as_array().unwrap().iter().map(|e| e["path"].as_str().unwrap()).collect();
    named.sort();
    let mut six: Vec<String> = ["AGENTS.md".to_owned(), DELEGATION.to_owned()].into_iter().chain(Role::ALL.into_iter().map(role_path)).collect();
    six.sort();
    assert_eq!(named, six);
    // A later start writes nothing.
    start_without_writing(&t.store());
}

/// (a) An older store, first seeded without the delegation guidance: nothing
/// is written; the delegating roles are refused and no role starts.
#[test]
fn an_older_store_without_the_file_is_never_written_and_refuses_the_delegating_roles_only() {
    let t = Temp::new();
    let store = legacy_store(&t);
    std::fs::write(store.join("agents/AGENT_HELP_HUMAN.md"), "The person's edited HELP_HUMAN\n").unwrap();
    let results = start_without_writing(&store);
    assert_absent_refuses_delegating_roles_only(&store, results);
}

/// (b) Files a development home may hold under the names an earlier build of
/// this change used are untouched and change nothing.
#[test]
fn files_under_names_an_earlier_build_used_are_untouched_and_change_nothing() {
    let earlier = [
        (".seed-addition-DELEGATION_RECORDS.json", r#"{"format":"chirality.instruction-seed-addition/1","release":"r","created":[{"path":"DELEGATION_RECORDS.md","defaultContent":{"method":"chirality.app.exact-bytes.sha256/v1","value":"0000000000000000000000000000000000000000000000000000000000000000"}}],"preserved":[]}"#),
        (".seed-addition-DELEGATION_RECORDS.begun.json", r#"{"format":"chirality.instruction-seed-addition-begun/1","path":"DELEGATION_RECORDS.md"}"#),
        (".DELEGATION_RECORDS.md.placing", "Invented scratch bytes\n"),
    ];
    // Absent, and present as a person's own file.
    for present in [false, true] {
        let t = Temp::new();
        let store = legacy_store(&t);
        for (name, bytes) in earlier {
            std::fs::write(store.join(name), bytes).unwrap();
        }
        if present {
            std::fs::write(store.join(DELEGATION), "The person's own delegation notes\n").unwrap();
        }
        let results = start_without_writing(&store);
        for (name, bytes) in earlier {
            assert_eq!(std::fs::read(store.join(name)).unwrap(), bytes.as_bytes(), "{name}");
        }
        if present {
            for part in assert_present_is_read_as_it_is(&store, results) {
                assert_eq!(part["source"]["state"], "modified");
                assert_eq!(part["source"]["seedHistory"], json!({"status":"unestablished","reason":"missing"}));
            }
        } else {
            assert_absent_refuses_delegating_roles_only(&store, results);
        }
    }
}

/// (c) The older store after the person copies the shipped default in by hand:
/// supplied in the delegating roles as the default, its seed history
/// unestablished, and nothing written.
#[test]
fn an_older_store_with_the_default_copied_in_by_hand_is_supplied_it_and_never_written() {
    let t = Temp::new();
    let store = legacy_store(&t);
    std::fs::copy(Path::new(env!("CARGO_MANIFEST_DIR")).join("resources/instructions").join(DELEGATION), store.join(DELEGATION)).unwrap();
    let results = start_without_writing(&store);
    for part in assert_present_is_read_as_it_is(&store, results) {
        assert_eq!(part["source"]["path"], DELEGATION);
        assert_eq!(part["source"]["state"], "default");
        assert_eq!(part["content"]["value"], sha(&shipped(DELEGATION)));
        assert_eq!(part["source"]["reviewedDefault"]["content"]["value"], sha(&shipped(DELEGATION)));
        assert_eq!(part["source"]["seedHistory"], json!({"status":"unestablished","reason":"missing"}));
    }
}

/// (d) A store whose seed record is absent or unreadable, with the delegation
/// guidance present and absent, in a store first seeded with it and in an
/// older one: nothing is written; present is read as it is; absent refuses
/// the delegating roles only.
#[test]
fn without_a_readable_seed_record_nothing_is_written_and_the_file_is_read_as_it_is() {
    let records: [(&str, fn(&Path)); 4] = [
        ("absent", |p| std::fs::remove_file(p).unwrap()),
        ("corrupted", |p| std::fs::write(p, b"{\"format\":").unwrap()),
        ("names other paths", |p| std::fs::write(p, br#"{"format":"chirality.instruction-seed-record/1","release":"r","created":[],"preserved":[]}"#).unwrap()),
        ("linked", |p| {
            let target = p.with_file_name("record-elsewhere.json");
            std::fs::rename(p, &target).unwrap();
            std::os::unix::fs::symlink(&target, p).unwrap();
        }),
    ];
    for (case, apply) in records {
        for older in [false, true] {
            for present in [false, true] {
                let t = Temp::new();
                let store = if older { legacy_store(&t) } else {
                    seed_instructions(&t.store()).unwrap();
                    std::fs::remove_file(t.store().join(DELEGATION)).unwrap();
                    t.store()
                };
                if present {
                    std::fs::write(store.join(DELEGATION), "The person's own delegation notes\n").unwrap();
                }
                apply(&store.join(".seed-record.json"));
                let results = start_without_writing(&store);
                if present {
                    for part in assert_present_is_read_as_it_is(&store, results) {
                        assert_eq!(part["source"]["state"], "modified", "{case}");
                        assert_eq!(part["source"]["seedHistory"]["status"], "unestablished", "{case}");
                    }
                } else {
                    assert_absent_refuses_delegating_roles_only(&store, results);
                }
            }
        }
    }
}

/// A store first seeded with the delegation guidance, the file then removed by
/// the person: nothing puts it back, the delegating roles are refused, no role
/// starts, and the person's own copy back is supplied.
#[test]
fn a_removed_delegation_file_is_not_put_back_and_a_copy_back_by_hand_is_supplied() {
    let t = Temp::new();
    let store = t.store();
    seed_instructions(&store).unwrap();
    std::fs::remove_file(store.join(DELEGATION)).unwrap();
    let results = start_without_writing(&store);
    assert_absent_refuses_delegating_roles_only(&store, results);
    std::fs::write(store.join(DELEGATION), shipped(DELEGATION)).unwrap();
    for part in assert_present_is_read_as_it_is(&store, start_without_writing(&store)) {
        assert_eq!(part["source"]["state"], "default");
        assert_eq!(part["source"]["seedHistory"]["status"], "declared");
    }
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
            // With no verified path at hand, the place named is the fixed one
            // inside an installed application, and nothing about this run.
            assert!(reason.contains("The shipped default is the copy the App carries"), "{reason}");
            #[cfg(target_os = "macos")]
            assert!(reason.ends_with(&format!("in an installed copy it is inside the application, at Contents/Resources/instructions/{path}.")), "{reason}");
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

/// The place a refusal names inside an installed application is the one
/// every bundle configuration gives the instruction defaults.
#[test]
fn the_installed_place_a_refusal_names_is_where_every_bundle_configuration_puts_the_defaults() {
    let app = Path::new(env!("CARGO_MANIFEST_DIR"));
    let mut configurations = vec![app.join("tauri.conf.json")];
    for entry in std::fs::read_dir(app.join("../packaging/unsigned")).unwrap() {
        let path = entry.unwrap().path();
        if path.file_name().and_then(|n| n.to_str()).is_some_and(|n| n.starts_with("tauri.") && n.ends_with(".conf.json")) {
            configurations.push(path);
        }
    }
    assert!(configurations.len() > 1);
    for configuration in configurations {
        let value: Value = serde_json::from_slice(&std::fs::read(&configuration).unwrap()).unwrap();
        assert_eq!(value["bundle"]["resources"]["resources/instructions/"], "instructions/", "{}", configuration.display());
    }
    // macOS application bundles hold their resources at Contents/Resources.
    assert_eq!(crate::runtime_session::PACKAGED_INSTRUCTIONS, "Contents/Resources/instructions");
    for path in ["AGENTS.md", DELEGATION] {
        assert!(app.join("resources/instructions").join(path).is_file());
    }
}
