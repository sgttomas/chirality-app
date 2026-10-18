use super::*;
use crate::records_store::{Placement, Store};
use std::os::unix::{ffi::OsStrExt, fs::PermissionsExt};
struct Fixture {
    root: PathBuf,
    project: PathBuf,
    store: PathBuf,
}
impl Fixture {
    fn new() -> Self {
        let mut template = CString::new(
            std::env::temp_dir().join("role-observation-test-XXXXXX").as_os_str().as_bytes(),
        ).unwrap().into_bytes_with_nul();
        assert!(!unsafe { libc::mkdtemp(template.as_mut_ptr().cast()) }.is_null());
        let root = PathBuf::from(std::ffi::OsStr::from_bytes(&template[..template.len() - 1]))
            .canonicalize().unwrap();
        let project = root.join("project");
        std::fs::create_dir_all(&project).unwrap();
        let store = root.join("store");
        records_store::use_store_for_test(Some(Ok(Store {
            root: store.clone(),
            placement: Placement::Test,
            limits: vec![],
        })));
        Self {
            root,
            project,
            store,
        }
    }
    fn log(&self) -> RoleLog {
        RoleLog::open(&self.project).unwrap()
    }
    fn directory(&self) -> PathBuf {
        records_store::attach(&self.project, false)
            .unwrap()
            .dir
            .unwrap()
            .join(FOLDER)
    }
    fn append(&self, log: &RoleLog, supply: &str, outcome: &str) -> Value {
        let c = composition();
        log.append(observation(supply, outcome), Some(&c)).unwrap()
    }
}
impl Drop for Fixture {
    fn drop(&mut self) {
        records_store::use_store_for_test(None);
        let _ = std::fs::remove_dir_all(&self.root);
    }
}
fn composition() -> role_supply::Composition {
    let common = role_supply::Guidance::seeded(
        "AGENTS.md",
        "fixture-release",
        b"Common \xc3\xa9\r\n".to_vec(),
        b"default",
    )
    .unwrap();
    let role = role_supply::Guidance::seeded(
        "agents/AGENT_HELP_HUMAN.md",
        "fixture-release",
        b"Role exact\r\n".to_vec(),
        b"default",
    )
    .unwrap();
    role_supply::Composition::new(&common, Some((role_supply::Role::HELP_HUMAN, &role)), false)
        .unwrap()
}
fn observation(supply: &str, outcome: &str) -> Value {
    let c = composition();
    row(supply,"thread-start",Some("thread"),json!({"home":"home","generation":{"appSession":"fixture","home":"home","spawnCounter":1},"requestIdentity":1,"requestRef":"private-fixture-receipt","method":"thread/start","writeResult":"written","outcome":if outcome=="supplied"{"response-observed-result"}else{"pending"},"sourceCurrent":true}),json!({"role":"HELP_HUMAN","preselected":null,"roleSet":c.role_set_identity()}),outcome,Some(c.carried),json!({"instructionSources":null,"agentRole":null,"forkedFromId":null}),json!({}),None).unwrap()
}
#[test]
fn schema_bytes_match_and_fresh_reader_keeps_exact_app_sources_without_role_authority() {
    assert_eq!(
        SCHEMA.as_bytes(),
        include_bytes!(
            "../../../execution/PKG-02/DEL-02-04/Design/role-supply-observation.schema.json"
        )
    );
    let f = Fixture::new();
    let log = f.log();
    let p = f.append(&log, "sup:one", "supplied");
    assert_eq!(p["state"], "written");
    std::fs::write(f.project.join("AGENTS.md"), b"future edited copy").unwrap();
    let cold = f.log().read("home", Some("thread"));
    assert_eq!(cold["observations"].as_array().unwrap().len(), 1);
    assert_eq!(
        cold["observations"][0]["sourceBytes"]["composed"],
        composition().text
    );
    assert_eq!(
        cold["observations"][0]["sourceBytes"]["parts"][0]["text"],
        "Common é\r\n"
    );
    assert_eq!(cold["currentRoleAuthorityRestored"], false);
    assert_eq!(
        crate::role_lifecycle::RoleBindings::default().selected_role("home", "thread"),
        crate::role_lifecycle::RoleInForce::Unknown {
            reason: "original App supply binding not established".into()
        }
    );
    assert!(cold.to_string().contains("unverified"));
    assert!(f.log().read("other-home", Some("thread"))["observations"]
        .as_array()
        .unwrap()
        .is_empty());
}
#[test]
fn unknown_and_late_observations_append_without_rewriting_original() {
    let f = Fixture::new();
    let log = f.log();
    f.append(&log, "sup:one", "unknown");
    let path = f.directory().join(LOG);
    let before = std::fs::read(&path).unwrap();
    f.append(&log, "sup:one", "supplied");
    assert!(std::fs::read(path).unwrap().starts_with(&before));
    let view = log.read("home", None);
    let rows = view["observations"].as_array().unwrap();
    assert_eq!(rows.len(), 2);
    assert_eq!(rows[0]["record"]["outcome"], "unknown");
    assert_eq!(rows[1]["record"]["outcome"], "supplied");
    assert_ne!(
        rows[0]["record"]["observationId"],
        rows[1]["record"]["observationId"]
    );
    assert_eq!(
        std::fs::read_dir(f.directory().join("content"))
            .unwrap()
            .count(),
        4 // composition, two source parts, and original immutable limits
    );
}
// The fourth payload is bound to the same original composition; the unknown
// wait row and late success retain distinct observations without new content.

// Change metadata only, and prove the filesystem actually gave this inode a
// different ctime. Never pass vacuously on a coarse timestamp filesystem.
fn change_ctime_only(path: &Path) {
    let before = std::fs::metadata(path).unwrap();
    let bytes = std::fs::read(path).unwrap();
    let deadline = std::time::Instant::now() + std::time::Duration::from_secs(2);
    let mut mode = before.permissions().mode();
    let after = loop {
        mode ^= 0o100;
        std::fs::set_permissions(path, std::fs::Permissions::from_mode(mode)).unwrap();
        let after = std::fs::metadata(path).unwrap();
        if (after.ctime(), after.ctime_nsec()) != (before.ctime(), before.ctime_nsec()) {
            break after;
        }
        assert!(std::time::Instant::now() < deadline, "fixture ctime did not change");
        std::thread::sleep(std::time::Duration::from_millis(2));
    };
    assert_ne!((before.ctime(), before.ctime_nsec()), (after.ctime(), after.ctime_nsec()));
    assert_eq!((before.dev(), before.ino()), (after.dev(), after.ino()));
    assert_eq!((before.len(), before.mtime(), before.mtime_nsec()),
               (after.len(), after.mtime(), after.mtime_nsec()));
    assert_eq!(std::fs::read(path).unwrap(), bytes);
}

#[test]
fn ctime_only_change_before_read_and_append_keeps_quoted_sources() {
    let f = Fixture::new();
    let log = f.log();
    f.append(&log, "sup:first", "supplied");
    let path = f.directory().join(LOG);
    let original = std::fs::read(&path).unwrap();
    let before = log.read("home", Some("thread"));
    change_ctime_only(&path);
    let cold = f.log().read("home", Some("thread"));
    assert_eq!(cold, before);
    assert_eq!(cold["observations"][0]["sourceBytes"]["composed"], composition().text);
    assert_eq!(cold["currentRoleAuthorityRestored"], false);
    assert!(cold["standing"].as_str().unwrap().contains("unverified"));
    f.append(&log, "sup:later", "unknown");
    assert!(std::fs::read(&path).unwrap().starts_with(&original));
    assert_eq!(f.log().read("home", Some("thread"))["observations"].as_array().unwrap().len(), 2);
}

#[test]
fn ctime_only_change_inside_read_or_before_append_still_refuses_mutation() {
    let f = Fixture::new();
    let log = f.log();
    f.append(&log, "sup:first", "supplied");
    let path = f.directory().join(LOG);
    let original = std::fs::read(&path).unwrap();
    let at = path.clone();
    METADATA_BEFORE_READ.with(|slot| {
        *slot.borrow_mut() = Some(Box::new(move || change_ctime_only(&at)));
    });
    let folder = directory(&f.directory()).unwrap();
    assert_eq!(RoleLog::read_lines_bounded(&folder, &f.directory(), Some(original.len()))
        .err().unwrap(), "role observation log changed during read");
    let at = path.clone();
    BEFORE_APPEND.with(|slot| {
        *slot.borrow_mut() = Some(Box::new(move || change_ctime_only(&at)));
    });
    assert_eq!(log.append(observation("sup:later", "unknown"), Some(&composition())).unwrap_err(),
        "role observation log changed or was replaced before append; no replacement written");
    assert_eq!(std::fs::read(&path).unwrap(), original);
    // Refusal of an unstable operation is separate from later stable reading.
    let cold = f.log().read("home", Some("thread"));
    assert_eq!(cold["observations"].as_array().unwrap().len(), 1);
    assert!(cold["limits"].as_array().unwrap().is_empty());
}
#[test]
fn corruption_missing_payload_and_duplicate_identity_are_visible_not_promoted() {
    let f = Fixture::new();
    let log = f.log();
    f.append(&log, "sup:one", "supplied");
    let view = log.read("home", None);
    let row = &view["observations"][0]["record"];
    let id = row["appBytes"]["composed"]["content"]["value"]
        .as_str()
        .unwrap();
    let path = f.directory().join("content").join(format!("{id}.utf8"));
    std::fs::write(&path, b"changed").unwrap();
    let view = log.read("home", None);
    assert!(view["observations"][0]["sourceBytes"].is_null());
    assert!(!view["observations"][0]["limits"]
        .as_array()
        .unwrap()
        .is_empty());
    assert!(log
        .append(observation("sup:two", "supplied"), Some(&composition()))
        .is_err());
    std::fs::remove_file(&path).unwrap();
    let view = log.read("home", None);
    assert!(view["observations"][0]["sourceBytes"].is_null());
    assert_eq!(view["currentRoleAuthorityRestored"], false);
    let file = f.directory().join(LOG);
    let mut bytes = std::fs::read(&file).unwrap();
    bytes.extend_from_slice(b"torn");
    std::fs::write(file, bytes).unwrap();
    assert_eq!(log.read("home", None)["complete"], false);
    assert!(log
        .append(observation("sup:two", "unknown"), Some(&composition()))
        .unwrap_err()
        .contains("torn"));
}
#[test]
fn role_only_payload_exports_without_hiding_new_in_place_legacy() {
    let f = Fixture::new();
    let log = f.log();
    f.append(&log, "sup:one", "supplied");
    assert!(!records_store::home(&f.project).unwrap().store_mode);
    let bag = f.root.join("bag");
    crate::records_export::export(&f.project, &bag).unwrap();
    assert!(crate::records_export::verify(&bag).is_ok());
    let standalone = std::process::Command::new("python3")
        .arg(bag.join("verify.py"))
        .arg(&bag)
        .output()
        .unwrap();
    assert!(
        standalone.status.success(),
        "{}",
        String::from_utf8_lossy(&standalone.stderr)
    );
    assert!(String::from_utf8_lossy(&standalone.stdout)
        .contains("not origin, chain semantics or human acts"));
    assert!(bag.join("data/role-supply/observations.jsonl").exists());
    let heads: Value =
        serde_json::from_slice(&std::fs::read(bag.join("records-chain-heads.json")).unwrap())
            .unwrap();
    let role = heads["logs"]
        .as_array()
        .unwrap()
        .iter()
        .find(|head| head["log"] == RELATIVE_LOG)
        .unwrap();
    assert_eq!(role["chain"]["lines"], 1);
    assert_eq!(role["chain"]["linked"], true);
    assert_eq!(
        role["chain"]["head"],
        record_lines::line_identity(
            std::fs::read(f.directory().join(LOG))
                .unwrap()
                .strip_suffix(b"\n")
                .unwrap()
        )
    );
    let current = crate::records_index::chain_heads(&f.project);
    assert!(current["logs"]
        .as_array()
        .unwrap()
        .iter()
        .any(|head| head["log"]
            .as_str()
            .is_some_and(|path| path.ends_with(RELATIVE_LOG))
            && head["head"] == role["chain"]["head"]));
    assert_eq!(heads["formatVersion"], "0.2");
    // A valid checksummed tag still must cover this format's actual head.
    let mut omitted = heads.clone();
    omitted["logs"] = json!([]);
    let bytes = serde_json::to_vec(&omitted).unwrap();
    std::fs::write(bag.join("records-chain-heads.json"), &bytes).unwrap();
    let tags = std::fs::read_to_string(bag.join("tagmanifest-sha256.txt")).unwrap();
    let tags = tags
        .lines()
        .map(|line| {
            if line.ends_with("  records-chain-heads.json") {
                format!(
                    "{}  records-chain-heads.json",
                    crate::util::sha256_hex(&bytes)
                )
            } else {
                line.to_owned()
            }
        })
        .collect::<Vec<_>>()
        .join("\n")
        + "\n";
    std::fs::write(bag.join("tagmanifest-sha256.txt"), tags).unwrap();
    assert!(crate::records_export::verify(&bag)
        .unwrap_err()
        .contains("chain heads differ"));
    // The original0.1 profile permitted arbitrary payload names but promised
    // only RS heads. Preserve its byte/admin verification with that limit.
    omitted["formatVersion"] = json!("0.1");
    let bytes = serde_json::to_vec(&omitted).unwrap();
    std::fs::write(bag.join("records-chain-heads.json"), &bytes).unwrap();
    let tags = std::fs::read_to_string(bag.join("tagmanifest-sha256.txt")).unwrap();
    let tags = tags
        .lines()
        .map(|line| {
            if line.ends_with("  records-chain-heads.json") {
                format!(
                    "{}  records-chain-heads.json",
                    crate::util::sha256_hex(&bytes)
                )
            } else {
                line.to_owned()
            }
        })
        .collect::<Vec<_>>()
        .join("\n")
        + "\n";
    std::fs::write(bag.join("tagmanifest-sha256.txt"), tags).unwrap();
    let verified = crate::records_export::verify(&bag).unwrap();
    assert!(verified["chainHeadProfile"]
        .as_str()
        .unwrap()
        .contains("role supply log heads unestablished"));
    let standalone = std::process::Command::new("python3")
        .arg(bag.join("verify.py"))
        .arg(&bag)
        .output()
        .unwrap();
    assert!(
        standalone.status.success(),
        "{}",
        String::from_utf8_lossy(&standalone.stderr)
    );
    assert!(String::from_utf8_lossy(&standalone.stdout)
        .contains("not origin, chain semantics or human acts"));
    let current =
        crate::records_export::matches_current(&f.directory().parent().unwrap(), &bag, false)
            .unwrap();
    assert_eq!(current["chainHeadProfile"], verified["chainHeadProfile"]);
    let legacy = f.project.join("records/coordination.rs.jsonl");
    std::fs::create_dir_all(legacy.parent().unwrap()).unwrap();
    std::fs::write(&legacy, b"in-place original\n").unwrap();
    assert!(!records_store::home(&f.project).unwrap().store_mode);
    assert!(storage::discover(&f.project).unwrap().contains(&legacy));
    assert!(log
        .append(observation("sup:two", "unknown"), Some(&composition()))
        .unwrap_err()
        .contains("import"));
    assert_eq!(log.read("home", None)["complete"], false);
    assert!(crate::records_export::export(&f.project, &f.root.join("blocked-bag")).is_err());
}
#[test]
fn substituted_content_directory_and_payload_do_not_confirm_publication() {
    for payload in [false, true] {
        let f = Fixture::new();
        let log = f.log();
        let c = composition();
        // First publish a valid source so the second append reuses retained bytes.
        f.append(&log, "sup:before", "supplied");
        let content = f.directory().join("content");
        BEFORE_APPEND.with(|slot| {
            *slot.borrow_mut() = Some(Box::new(move || {
                if payload {
                    let leaf = format!(
                        "{}.utf8",
                        role_supply::content(c.text.as_bytes())["value"]
                            .as_str()
                            .unwrap()
                    );
                    std::fs::rename(content.join(&leaf), content.join("detached")).unwrap();
                    std::fs::write(content.join(leaf), c.text.as_bytes()).unwrap();
                } else {
                    std::fs::rename(&content, content.with_file_name("detached-content")).unwrap();
                    std::fs::create_dir(&content).unwrap();
                }
            }))
        });
        assert!(log
            .append(observation("sup:after", "supplied"), Some(&composition()))
            .unwrap_err()
            .contains("replaced"));
        assert_eq!(
            std::fs::read_to_string(f.directory().join(LOG))
                .unwrap()
                .lines()
                .count(),
            1
        );
    }
}
#[test]
fn unavailable_store_and_project_or_leaf_substitution_never_redirect() {
    let f = Fixture::new();
    let log = f.log();
    records_store::use_store_for_test(Some(Err("invented store refusal".into())));
    assert!(log
        .append(observation("sup:one", "unknown"), Some(&composition()))
        .unwrap_err()
        .contains("invented store refusal"));
    assert_eq!(log.read("home", None)["complete"], false);
    records_store::use_store_for_test(Some(Ok(Store {
        root: f.store.clone(),
        placement: Placement::Test,
        limits: vec![],
    })));
    f.append(&log, "sup:one", "supplied");
    let source = f.directory().join(LOG);
    let other = f.root.join("outside");
    std::fs::write(&other, b"sentinel").unwrap();
    std::fs::remove_file(&source).unwrap();
    std::os::unix::fs::symlink(&other, &source).unwrap();
    assert!(log
        .append(observation("sup:two", "unknown"), Some(&composition()))
        .is_err());
    assert_eq!(std::fs::read(&other).unwrap(), b"sentinel");
    assert_eq!(log.read("home", None)["complete"], false);
    std::fs::rename(&f.project, f.root.join("former-project")).unwrap();
    std::fs::create_dir(&f.project).unwrap();
    assert!(log
        .append(observation("sup:three", "unknown"), Some(&composition()))
        .unwrap_err()
        .contains("replaced"));
    assert_eq!(log.read("home", None)["complete"], false);
}
#[test]
fn close_hold_dispose_and_old_openers_preserve_existing_retention_boundary() {
    let f = Fixture::new();
    let log = f.log();
    f.append(&log, "sup:one", "supplied");
    let actor = crate::act_control::person(Some("Invented fixture"), Some("fixture-os"));
    let observed = json!({"fixture":"test seam only; no live human act"});
    let apply = |action, bag: Option<&Path>| {
        let plan = crate::records_retention::prepare(&f.project, action, bag, &actor, &observed)?;
        crate::records_retention::apply(plan, &actor, &observed)
    };
    apply("set-hold", None).unwrap();
    apply("close", None).unwrap();
    assert!(log
        .append(observation("sup:two", "unknown"), Some(&composition()))
        .is_err());
    assert_eq!(
        log.read("home", None)["observations"]
            .as_array()
            .unwrap()
            .len(),
        1
    );
    let bag = f.root.join("closed-bag");
    crate::records_export::export(&f.project, &bag).unwrap();
    assert!(apply("dispose", Some(&bag))
        .unwrap_err()
        .contains("legal hold"));
    apply("release-hold", None).unwrap();
    let bag = f.root.join("disposal-bag");
    crate::records_export::export(&f.project, &bag).unwrap();
    apply("dispose", Some(&bag)).unwrap();
    assert_eq!(log.read("home", None)["complete"], false);
    assert!(log
        .append(observation("sup:three", "unknown"), Some(&composition()))
        .is_err());
    assert!(crate::records_export::verify(&bag).is_ok());
}
#[test]
fn legacy_02_keeps_its_exact_evidence_and_unknown_home() {
    let f = Fixture::new();
    let log = f.log();
    let dir = records_store::write_dir(&f.project).unwrap().join(FOLDER);
    std::fs::create_dir(&dir).unwrap();
    let old = composition()
        .start_record("sup:old", "thread", "old-request", 1, None)
        .unwrap();
    let mut bytes = serde_json::to_vec(&old).unwrap();
    bytes.push(b'\n');
    std::fs::write(dir.join(LOG), &bytes).unwrap();
    let view = log.read("home", None);
    assert_eq!(view["observations"][0]["record"], old);
    assert_eq!(view["observations"][0]["legacy"], true);
    assert!(!view["observations"][0]["limits"]
        .as_array()
        .unwrap()
        .is_empty());
    assert!(log.read("home", Some("thread"))["observations"]
        .as_array()
        .unwrap()
        .is_empty());
    f.append(&log, "sup:new", "supplied");
    assert!(std::fs::read(dir.join(LOG)).unwrap().starts_with(&bytes));
}
#[test]
fn concurrent_writers_keep_one_complete_chained_log() {
    let f = Fixture::new();
    let log = std::sync::Arc::new(f.log());
    let mut workers = vec![];
    for worker in 0..2 {
        let log = log.clone();
        let store = f.store.clone();
        workers.push(std::thread::spawn(move || {
            records_store::use_store_for_test(Some(Ok(Store {
                root: store,
                placement: Placement::Test,
                limits: vec![],
            })));
            for n in 0..5 {
                log.append(
                    observation(&format!("sup:{worker}-{n}"), "supplied"),
                    Some(&composition()),
                )
                .unwrap();
            }
            records_store::use_store_for_test(None);
        }));
    }
    for worker in workers {
        worker.join().unwrap();
    }
    let view = log.read("home", None);
    assert!(view["limits"].as_array().unwrap().is_empty());
    assert_eq!(view["observations"].as_array().unwrap().len(), 10);
}

#[test]
fn replacement_between_read_and_append_and_unconfirmed_flush_keep_source_truth() {
    let f = Fixture::new();
    let log = f.log();
    f.append(&log, "sup:first", "supplied");
    let path = f.directory().join(LOG);
    let displaced = f.root.join("original-log");
    let at = path.clone();
    let saved = displaced.clone();
    BEFORE_APPEND.with(|slot| {
        *slot.borrow_mut() = Some(Box::new(move || {
            std::fs::rename(&at, &saved).unwrap();
            std::fs::write(&at, b"sentinel").unwrap();
        }))
    });
    assert!(log
        .append(observation("sup:second", "unknown"), Some(&composition()))
        .unwrap_err()
        .contains("replaced"));
    assert_eq!(std::fs::read(&path).unwrap(), b"sentinel");
    std::fs::remove_file(&path).unwrap();
    std::fs::rename(&displaced, &path).unwrap();
    FAIL_AFTER_FILE_SYNC.with(|fail| fail.set(true));
    assert!(log
        .append(observation("sup:third", "supplied"), Some(&composition()))
        .unwrap_err()
        .contains("unconfirmed"));
    let fresh = f.log().read("home", None);
    assert_eq!(fresh["observations"].as_array().unwrap().len(), 2);
    assert_eq!(fresh["observations"][1]["record"]["supplyId"], "sup:third");
    assert_eq!(fresh["currentRoleAuthorityRestored"], false);
    assert!(fresh["standing"].as_str().unwrap().contains("unverified"));
}
#[test]
fn contradictory_h5_and_carrier_and_duplicate_observation_ids_are_refused() {
    let f = Fixture::new();
    let log = f.log();
    let mut wrong = observation("sup:bad", "supplied");
    wrong["carried"]["developerInstructions"]["byteLength"] = json!(123);
    assert!(log
        .append(wrong, Some(&composition()))
        .unwrap_err()
        .contains("carrier"));
    f.append(&log, "sup:first", "supplied");
    let path = f.directory().join(LOG);
    let mut original: Value =
        serde_json::from_slice(std::fs::read(&path).unwrap().strip_suffix(b"\n").unwrap()).unwrap();
    original["request"]["generation"]["home"] = json!("another-home");
    let mut bytes = serde_json::to_vec(&original).unwrap();
    bytes.push(b'\n');
    std::fs::write(&path, &bytes).unwrap();
    assert_eq!(log.read("home", None)["complete"], false);
    original["request"]["generation"]["home"] = json!("home");
    let mut second = original.clone();
    let raw = serde_json::to_vec(&original).unwrap();
    second["seq"] = json!(2);
    second["prevLine"] = record_lines::link(Some(&record_lines::line_identity(&raw)));
    let mut bytes = raw;
    bytes.push(b'\n');
    bytes.extend_from_slice(&serde_json::to_vec(&second).unwrap());
    bytes.push(b'\n');
    std::fs::write(path, bytes).unwrap();
    assert_eq!(log.read("home", None)["complete"], false);
}
#[test]
fn mixed_observation_01_02_log_heads_and_export_keep_declared_schemas(){
    assert_eq!(OLD_SCHEMA.as_bytes(),include_bytes!("../../../execution/PKG-02/DEL-02-04/Design/role-supply-observation-0.1.schema.json"));
    assert_eq!(include_bytes!("../resources/workflow_role/role-limit-observation.schema.json"),include_bytes!("../../../execution/PKG-02/DEL-02-04/Design/role-limit-observation.schema.json"));
    let f=Fixture::new();let log=f.log();let c=composition();let mut old=observation("sup:old","supplied");old["formatVersion"]=json!("0.1");log.append(old,Some(&c)).unwrap();
    let prefix=std::fs::read(f.directory().join(LOG)).unwrap();f.append(&log,"sup:current","supplied");
    assert!(std::fs::read(f.directory().join(LOG)).unwrap().starts_with(&prefix));
    let read=log.read("home",Some("thread"));assert_eq!(read["observations"].as_array().unwrap().len(),2);
    assert_eq!(read["observations"][0]["record"]["formatVersion"],"0.1");assert_eq!(read["observations"][1]["record"]["formatVersion"],"0.3");
    assert!(read["observations"][0]["record"]["appBytes"].get("limitAccount").is_none());assert!(read["observations"][1]["record"]["appBytes"]["limitAccount"].is_object());
    let before=project_chain_head(&f.project).unwrap().unwrap();let bag=f.root.join("mixed-bag");crate::records_export::export(&f.project,&bag).unwrap();crate::records_export::verify(&bag).unwrap();
    let copied=copied_chain_head(&bag.join("data/role-supply/observations.jsonl"));
    assert_eq!(before["lines"],2);assert!(before["head"].as_str().is_some());
    for key in ["lines","linked","head"]{assert_eq!(before[key],copied[key],"{key}");}
}
fn native_child_record_fixture(f: &Fixture) -> (crate::role_supply::Composition, Value) {
    let root = &f.root;
    let instructions = root.join("instructions");
    crate::runtime_session::seed_instructions(&instructions).unwrap();
    std::fs::create_dir(root.join("native-home")).unwrap();
    std::fs::write(root.join("native-home/config.toml"), "").unwrap();
    std::fs::create_dir(root.join("app-data")).unwrap();
    let reading = json!({"config":{},"origins":{},"layers":[{"name":{"type":"user","file":root.join("native-home/config.toml"),"profile":null},"version":"user","config":{}},{"name":{"type":"system","file":root.join("absent-system/config.toml")},"version":"system","config":{}}]});
    let mut c = crate::runtime_session::compose_role(
        &instructions,
        Some(crate::role_supply::Role::HELP_HUMAN),
    )
    .unwrap();
    crate::child_roles::prepare(
        &mut c,
        crate::child_roles::Namespace::observe(&reading),
        &instructions,
        &root.join("app-data"),
    );
    let mut row = observation("sup:native-children", "supplied");
    row["carried"] = c.carried.clone();
    row["selection"]["roleSet"] = c.role_set_identity().clone();
    (c, row)
}
#[test]
fn native_children_quoted_payload_exact_set_missing_duplicate_and_mislabel_are_unavailable() {
    let f = Fixture::new();
    let log = f.log();
    let (c, row) = native_child_record_fixture(&f);
    log.append(row, Some(&c)).unwrap();
    let read = log.read("home", Some("thread"));
    assert_eq!(
        read["observations"][0]["sourceBytes"]["nativeChildren"]
            .as_array()
            .unwrap()
            .len(),
        3
    );
    let (_, folder, _, _) = log.location(false).unwrap().unwrap();
    let (rows, _, _) = RoleLog::read_lines(&folder, &f.directory()).unwrap();
    let payloads = child(&folder, "content", false).unwrap().unwrap();
    for case in ["missing", "drop-one", "duplicate", "mislabel"] {
        let mut bad = rows[0].clone();
        match case {
            "missing" => {
                bad["appBytes"]
                    .as_object_mut()
                    .unwrap()
                    .remove("nativeChildren");
            }
            "drop-one" => {
                bad["appBytes"]["nativeChildren"]
                    .as_array_mut()
                    .unwrap()
                    .pop();
            }
            "duplicate" => {
                let copied = bad["appBytes"]["nativeChildren"][0].clone();
                bad["appBytes"]["nativeChildren"]
                    .as_array_mut()
                    .unwrap()
                    .push(copied);
            }
            "mislabel" => {
                bad["appBytes"]["nativeChildren"][0]["carried"]["developerInstructions"]["parts"]
                    [1]["role"] = json!("TASK");
            }
            _ => unreachable!(),
        };
        let path = f.root.join(format!("saved-{case}.json"));
        std::fs::write(&path, serde_json::to_vec(&bad).unwrap()).unwrap();
        let saved: Value = serde_json::from_slice(&std::fs::read(path).unwrap()).unwrap();
        assert!(
            RoleLog::source_bytes(Some(&payloads), &saved).is_err(),
            "{case}"
        );
    }
}
#[test]
fn native_children_canonical_guidance_and_publication_failure_rows_remain_readable() {
    for reason in ["child-guidance-unavailable", "child-file-unavailable"] {
        let f = Fixture::new();
        let log = f.log();
        let (mut c, mut row) = native_child_record_fixture(&f);
        c.children.clear();
        c.carried["nativeChildRoles"] = json!([{ "role":"HELP_HUMAN","status":"not-supplied","reason":"not-offered-by-role"},{"role":"HELPS_HUMANS","status":"not-supplied","reason":reason},{"role":"WORKING_ITEMS","status":"not-supplied","reason":reason},{"role":"TASK","status":"not-supplied","reason":reason}]);
        row["carried"] = c.carried.clone();
        log.append(row, Some(&c)).unwrap();
        let read = log.read("home", Some("thread"));
        assert_eq!(
            read["observations"].as_array().unwrap().len(),
            1,
            "{reason}: {read}"
        );
        assert!(read["observations"][0]["sourceBytes"].is_object(), "{read}");
        assert_eq!(
            read["observations"][0]["record"]["carried"]["nativeChildRoles"][1]["reason"],
            reason
        );
    }
}
#[test]
fn native_children_mixed_01_02_03_preserves_previous_schema_bytes_and_rows() {
    assert_eq!(
        PREVIOUS_SCHEMA.as_bytes(),
        include_bytes!(
            "../../../execution/PKG-02/DEL-02-04/Design/role-supply-observation-0.2.schema.json"
        )
    );
    let f = Fixture::new();
    let log = f.log();
    let c = composition();
    for (version, supply) in [("0.1", "sup:01"), ("0.2", "sup:02"), ("0.3", "sup:03")] {
        let mut row = observation(supply, "supplied");
        row["formatVersion"] = json!(version);
        log.append(row, Some(&c)).unwrap();
    }
    let read = log.read("home", Some("thread"));
    assert_eq!(
        read["observations"]
            .as_array()
            .unwrap()
            .iter()
            .map(|r| r["record"]["formatVersion"].as_str().unwrap())
            .collect::<Vec<_>>(),
        vec!["0.1", "0.2", "0.3"]
    );
    assert!(read["observations"]
        .as_array()
        .unwrap()
        .iter()
        .all(|r| r["sourceBytes"].is_object()));
}
#[test]
fn native_children_quoted_original_limit_and_common_source_mismatches_are_unavailable() {
    let f = Fixture::new();
    let log = f.log();
    let (c, row) = native_child_record_fixture(&f);
    log.append(row, Some(&c)).unwrap();
    let (_, folder, _, _) = log.location(false).unwrap().unwrap();
    let (rows, _, _) = RoleLog::read_lines(&folder, &f.directory()).unwrap();
    let payloads = child(&folder, "content", false).unwrap().unwrap();
    for case in [
        "wrong-limit-role-set",
        "modified-source-stated-limit",
        "different-common",
    ] {
        let mut bad = rows[0].clone();
        let original_account =
            crate::conversation_roles::frozen_limit_account(&c.children[0].composition).unwrap();
        let mut account = original_account;
        match case {
            "wrong-limit-role-set" => account["roleSet"]["value"] = json!("0".repeat(64)),
            "modified-source-stated-limit" => {
                bad["appBytes"]["nativeChildren"][0]["carried"]["developerInstructions"]["parts"]
                    [1]["source"]["state"] = json!("modified");
                account["roleGuidance"]["source"] = bad["appBytes"]["nativeChildren"][0]["carried"]
                    ["developerInstructions"]["parts"][1]["source"]
                    .clone();
            }
            "different-common" => {
                let role = c.children[0].role;
                let common = crate::role_supply::Guidance::seeded(
                    "AGENTS.md",
                    crate::runtime_session::INSTRUCTION_RELEASE,
                    b"Different common guidance\n".to_vec(),
                    crate::runtime_session::COMMON_DEFAULT,
                )
                .unwrap();
                let guidance = crate::role_supply::Guidance::read_seeded(
                    &f.root.join("instructions"),
                    &format!("agents/AGENT_{}.md", role.name()),
                    crate::runtime_session::INSTRUCTION_RELEASE,
                    crate::runtime_session::role_default(role),
                )
                .unwrap();
                let changed =
                    crate::role_supply::Composition::new(&common, Some((role, &guidance)), true)
                        .unwrap();
                let composed = RoleLog::publish_bytes(&payloads, changed.text.as_bytes())
                    .unwrap()
                    .0;
                let envelope = format!(
                    "developer_instructions = {}\n",
                    serde_json::to_string(&changed.text).unwrap()
                );
                let file = RoleLog::publish_bytes(&payloads, envelope.as_bytes())
                    .unwrap()
                    .0;
                let mut parts = vec![];
                for part in changed.carried["developerInstructions"]["parts"]
                    .as_array()
                    .unwrap()
                {
                    let start = part["offset"].as_u64().unwrap() as usize;
                    let len = part["length"].as_u64().unwrap() as usize;
                    parts.push(
                        RoleLog::publish_bytes(
                            &payloads,
                            &changed.text.as_bytes()[start..start + len],
                        )
                        .unwrap()
                        .0,
                    );
                }
                bad["appBytes"]["nativeChildren"][0]["carried"] = changed.carried.clone();
                bad["appBytes"]["nativeChildren"][0]["composed"] = composed.clone();
                bad["appBytes"]["nativeChildren"][0]["parts"] = json!(parts);
                bad["appBytes"]["nativeChildren"][0]["file"] = file.clone();
                for supplied in bad["carried"]["nativeChildRoles"].as_array_mut().unwrap() {
                    if supplied["role"] == role.name() {
                        supplied["composed"] = composed["content"].clone();
                        supplied["file"] = file["content"].clone();
                    }
                }
                account = crate::conversation_roles::frozen_limit_account(&changed).unwrap();
            }
            _ => unreachable!(),
        }
        bad["appBytes"]["nativeChildren"][0]["limitAccount"] =
            RoleLog::publish_bytes(&payloads, &serde_json::to_vec(&account).unwrap())
                .unwrap()
                .0;
        let saved = f.root.join(format!("saved-{case}.json"));
        std::fs::write(&saved, serde_json::to_vec(&bad).unwrap()).unwrap();
        let bad: Value = serde_json::from_slice(&std::fs::read(saved).unwrap()).unwrap();
        assert!(
            RoleLog::source_bytes(Some(&payloads), &bad).is_err(),
            "{case}"
        );
    }
}
