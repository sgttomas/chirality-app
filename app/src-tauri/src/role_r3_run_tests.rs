// Actual Host-issued private start/fork receipts through Root's actual run
// lifecycle and fresh durable correspondence. Invented owned supplier only.
struct RoleR3Store(PathBuf);
impl RoleR3Store {
    fn new() -> Self {
        let path =
            std::env::temp_dir().join(crate::util::opaque_id("role-r3-store-").unwrap());
        crate::records_store::use_store_for_test(Some(Ok(crate::records_store::Store {
            root: path.clone(),
            placement: crate::records_store::Placement::Test,
            limits: vec![],
        })));
        Self(path)
    }
}
impl Drop for RoleR3Store {
    fn drop(&mut self) {
        crate::records_store::use_store_for_test(None);
        let _ = std::fs::remove_dir_all(&self.0);
    }
}
fn role_r3_composition(
    role: Option<crate::role_supply::Role>,
    modified: bool,
) -> crate::role_supply::Composition {
    use crate::role_supply::{Composition, Guidance};
    let common = Guidance::seeded(
        "AGENTS.md",
        INSTRUCTION_RELEASE,
        COMMON_DEFAULT.to_vec(),
        COMMON_DEFAULT,
    )
    .unwrap();
    let selected = role.map(|r| {
        let default = role_default(r);
        let bytes = if modified {
            [default, b"\nOwn role alteration.\r\n"].concat()
        } else {
            default.to_vec()
        };
        (
            r,
            Guidance::seeded(
                &format!("agents/AGENT_{}.md", r.name()),
                INSTRUCTION_RELEASE,
                bytes,
                default,
            )
            .unwrap(),
        )
    });
    Composition::new(&common, selected.as_ref().map(|(r, g)| (*r, g)), false).unwrap()
}
fn role_r3_start(peer: &Peer, composition: &crate::role_supply::Composition) -> String {
    let home = &peer.home;
    home.history
        .lock()
        .unwrap()
        .configure_role_log(&peer.fixture.root);
    let supply = crate::util::opaque_id("sup:").unwrap();
    let receipt = home
        .host
        .thread_start_with_guidance_dispatch(
            &peer.generation,
            peer.fixture.root.to_str().unwrap(),
            "fixture-model",
            "fixture-provider",
            &composition.text,
        )
        .unwrap();
    home.history
        .lock()
        .unwrap()
        .start_dispatched_selected(receipt.clone(), composition, &supply, None, Some(false))
        .unwrap();
    let status = home
        .host
        .source_request_wait(&receipt, Duration::from_secs(2))
        .unwrap();
    home.history.lock().unwrap().reconcile(&home.host);
    let thread = status["response"]["result"]["thread"]["id"]
        .as_str()
        .unwrap()
        .to_owned();
    assert!(home
        .history
        .lock()
        .unwrap()
        .binding(peer.generation["home"].as_str().unwrap(), &thread)
        .is_some());
    thread
}
fn role_r3_open(peer: &Peer, root: &mut WorkflowRootSession, thread: &str) -> String {
    let (review, revision) = review_of(root);
    root.select_hot_registered_copy(
        &crate::workflow_selection::Chat::in_home(&peer.home, thread),
        &review,
        &revision,
    )
    .unwrap();
    let reference = root
        .prepare_run(
            peer.home.clone(),
            &peer.generation,
            thread,
            "role receiving test".into(),
            peer.project(),
        )
        .unwrap();
    let run = root.runs[&reference].clone();
    run.lock().unwrap().send().unwrap();
    reference
}
fn role_r3_entry(peer: &Peer, reference: &str) -> Value {
    peer.fixture
        .rs_entries()
        .into_iter()
        .find(|e| {
            e["runId"] == reference
                && e["kind"] == "supplied_guidance"
                && e["body"]["supplyForm"]
                    .as_str()
                    .unwrap_or("")
                    .starts_with("role guidance")
        })
        .unwrap()
}
#[test]
fn role_r3_actual_start_run_and_cold_sources_keep_original_limits_after_edit() {
    let _store = RoleR3Store::new();
    let peer = Peer::new();
    let composition = role_r3_composition(Some(crate::role_supply::Role::HELP_HUMAN), true);
    let thread = role_r3_start(&peer, &composition);
    let mut root = peer.registered();
    let reference = role_r3_open(&peer, &mut root, &thread);
    let entry = role_r3_entry(&peer, &reference);
    let entries = peer.fixture.rs_entries();
    let own = entries
        .iter()
        .filter(|e| e["runId"] == reference)
        .collect::<Vec<_>>();
    assert_eq!(own[0]["kind"], "run_opened");
    assert_eq!(own[0]["body"]["seatRole"], "HELP_HUMAN");
    assert_eq!(own[1], &entry);
    std::fs::write(peer.fixture.root.join("AGENTS.md"), b"changed later").unwrap();
    let before = peer.wire();
    let bytes =
        std::fs::read(crate::records::supply::run_log(&peer.fixture.root, &reference).unwrap())
            .unwrap();
    let quoted = crate::role_observations::read_r3(&peer.fixture.root, &entry);
    assert_eq!(
        quoted["state"], "quoted historical correspondence",
        "{quoted}"
    );
    assert_eq!(quoted["sourceBytes"]["composed"], composition.text);
    assert!(quoted["limitAccount"]["limits"]
        .as_array()
        .unwrap()
        .iter()
        .all(|l| l["standing"] == "unknown"));
    assert_eq!(quoted["currentRoleAuthorityRestored"], false);
    assert_eq!(quoted["adoption"], "unknown");
    let cold = HistorySession::default();
    assert_eq!(
        cold.role(peer.generation["home"].as_str().unwrap(), &thread)["standing"],
        "unknown"
    );
    let project =
        crate::workflow_workspace::publication::ProjectRecords::open(&peer.fixture.root).unwrap();
    let view = crate::records::supply::read_project_supply(&project);
    assert_eq!(
        view["roleSupplies"][0]["state"],
        "quoted historical correspondence"
    );
    assert_eq!(peer.wire(), before);
    assert_eq!(
        std::fs::read(crate::records::supply::run_log(&peer.fixture.root, &reference).unwrap())
            .unwrap(),
        bytes
    );
}
#[test]
fn role_r3_ctime_only_change_keeps_receipt_but_same_bytes_inode_replacement_refuses() {
    use std::os::unix::fs::{MetadataExt, PermissionsExt};
    let _store = RoleR3Store::new();
    let peer = Peer::new();
    let composition = role_r3_composition(Some(crate::role_supply::Role::HELP_HUMAN), false);
    let thread = role_r3_start(&peer, &composition);
    let cap = peer.home.history.lock().unwrap()
        .role_publication(peer.generation["home"].as_str().unwrap(), &thread)
        .unwrap().unwrap();
    cap.verify(&peer.fixture.root).unwrap();
    let folder = crate::records_store::attach(&peer.fixture.root, false)
        .unwrap().dir.unwrap().join("role-supply");
    let path = folder.join("observations.jsonl");
    let original = std::fs::read(&path).unwrap();
    let before = std::fs::metadata(&path).unwrap();
    let deadline = std::time::Instant::now() + Duration::from_secs(2);
    let mut mode = before.permissions().mode();
    let after = loop {
        mode ^= 0o100;
        std::fs::set_permissions(&path, std::fs::Permissions::from_mode(mode)).unwrap();
        let after = std::fs::metadata(&path).unwrap();
        if (after.ctime(), after.ctime_nsec()) != (before.ctime(), before.ctime_nsec()) {
            break after;
        }
        assert!(std::time::Instant::now() < deadline, "fixture ctime did not change");
        std::thread::sleep(Duration::from_millis(2));
    };
    assert_ne!((before.ctime(), before.ctime_nsec()), (after.ctime(), after.ctime_nsec()));
    assert_eq!((before.dev(), before.ino()), (after.dev(), after.ino()));
    assert_eq!((before.len(), before.mtime(), before.mtime_nsec()),
               (after.len(), after.mtime(), after.mtime_nsec()));
    assert_eq!(std::fs::read(&path).unwrap(), original);
    cap.verify(&peer.fixture.root).unwrap();
    let mut root = peer.registered();
    let reference = role_r3_open(&peer, &mut root, &thread);
    let entry = role_r3_entry(&peer, &reference);
    let quoted = crate::role_observations::read_r3(&peer.fixture.root, &entry);
    assert_eq!(quoted["state"], "quoted historical correspondence", "{quoted}");
    assert_eq!(quoted["sourceBytes"]["composed"], composition.text);
    assert_eq!(quoted["currentRoleAuthorityRestored"], false);
    assert_eq!(std::fs::read(&path).unwrap(), original);
    // Retain the original inode so this is a real, byte-identical replacement,
    // with no possibility of the filesystem reusing the old inode number.
    std::fs::rename(&path, folder.join("held-original-log")).unwrap();
    std::fs::write(&path, &original).unwrap();
    let replaced = std::fs::metadata(&path).unwrap();
    assert_ne!((before.dev(), before.ino()), (replaced.dev(), replaced.ino()));
    assert_eq!(cap.verify(&peer.fixture.root).unwrap_err(),
        "original role publication physical log/folder was replaced");
    assert_eq!(std::fs::read(&path).unwrap(), original);
}

#[test]
fn role_r3_actual_fork_uses_distinct_observation_and_exact_parent_source() {
    let _store = RoleR3Store::new();
    let peer = Peer::new();
    let composition = role_r3_composition(Some(crate::role_supply::Role::WORKING_ITEMS), false);
    let parent = role_r3_start(&peer, &composition);
    let result = crate::conversation_roles::fork_conversation(
        &peer.home,
        &peer.generation,
        &parent,
        Duration::from_secs(2),
    )
    .unwrap();
    let fork = result["thread"]["threadId"].as_str().unwrap().to_owned();
    let mut root = peer.registered();
    let reference = role_r3_open(&peer, &mut root, &fork);
    let entry = role_r3_entry(&peer, &reference);
    assert_eq!(
        entry["body"]["supplyForm"],
        "role guidance inherited at fork"
    );
    let quoted = crate::role_observations::read_r3(&peer.fixture.root, &entry);
    assert_eq!(
        quoted["state"], "quoted historical correspondence",
        "{quoted}"
    );
    let rows = quoted["sourceObservations"].as_array().unwrap();
    assert_eq!(rows.len(), 2);
    assert_ne!(rows[0]["observationId"], rows[1]["observationId"]);
    assert_eq!(rows[0]["thread"], fork);
    assert_eq!(rows[1]["thread"], parent);
    assert_eq!(quoted["sourceBytes"]["composed"], composition.text);
    assert!(quoted["limitAccount"]["limits"]
        .as_array()
        .unwrap()
        .iter()
        .all(|l| l["standing"] == "stated-not-enforced"));
    let frames = peer.wire();
    let fork_frame = frames
        .iter()
        .find(|f| f["method"] == "thread/fork")
        .unwrap();
    assert!(fork_frame["params"].get("developerInstructions").is_none());
}
#[test]
fn role_r3_no_role_and_unconfirmed_landed_publication_do_not_invent_authority() {
    let _store = RoleR3Store::new();
    let peer = Peer::new();
    let composition = role_r3_composition(None, false);
    let thread = role_r3_start(&peer, &composition);
    let mut root = peer.registered();
    let reference = role_r3_open(&peer, &mut root, &thread);
    let quoted =
        crate::role_observations::read_r3(&peer.fixture.root, &role_r3_entry(&peer, &reference));
    assert_eq!(quoted["limitAccount"]["role"], "none");
    assert_eq!(quoted["limitAccount"]["limits"], json!([]));
    crate::role_observations::FAIL_AFTER_FILE_SYNC.with(|f| f.set(true));
    let later = role_r3_start(&peer, &composition);
    assert!(peer
        .home
        .history
        .lock()
        .unwrap()
        .role_publication(peer.generation["home"].as_str().unwrap(), &later)
        .is_err());
    let before = peer.wire();
    let later_run = role_r3_open(&peer, &mut root, &later);
    assert!(!peer
        .fixture
        .rs_entries()
        .iter()
        .any(|e| e["runId"] == later_run && e["kind"] == "supplied_guidance"));
    let history = crate::role_observations::RoleLog::open(&peer.fixture.root)
        .unwrap()
        .read(peer.generation["home"].as_str().unwrap(), Some(&later));
    assert_eq!(history["observations"][0]["record"]["outcome"], "supplied");
    assert!(peer
        .home
        .history
        .lock()
        .unwrap()
        .role_publication(peer.generation["home"].as_str().unwrap(), &later)
        .is_err());
    assert_eq!(
        peer.wire().len(),
        before.len() + 1,
        "only the person's explicit run start was sent"
    );
}
#[test]
fn role_r3_equal_thread_ids_in_distinct_homes_projects_and_parent_alias_refuse() {
    let _store = RoleR3Store::new();
    let a = Peer::new();
    let b = Peer::new();
    let c = role_r3_composition(Some(crate::role_supply::Role::HELP_HUMAN), false);
    let ta = role_r3_start(&a, &c);
    let tb = role_r3_start(&b, &c);
    assert_eq!(ta, tb);
    let cap = a
        .home
        .history
        .lock()
        .unwrap()
        .role_publication(a.generation["home"].as_str().unwrap(), &ta)
        .unwrap()
        .unwrap();
    assert!(cap
        .verify_target(&a.fixture.root, b.generation["home"].as_str().unwrap(), &tb)
        .is_err());
    assert!(cap
        .verify_target(&b.fixture.root, a.generation["home"].as_str().unwrap(), &ta)
        .is_err());
    let mut root = a.registered();
    let run = role_r3_open(&a, &mut root, &ta);
    let entry = role_r3_entry(&a, &run);
    assert_eq!(
        crate::role_observations::read_r3(&b.fixture.root, &entry)["state"],
        "limited"
    );
    let role_dir = crate::records_store::attach(&a.fixture.root, false)
        .unwrap()
        .dir
        .unwrap()
        .join("role-supply");
    let held = role_dir.with_file_name("held-original-role");
    std::fs::rename(&role_dir, &held).unwrap();
    std::os::unix::fs::symlink(&held, &role_dir).unwrap();
    assert!(cap.verify(&a.fixture.root).is_err());
    assert_eq!(
        crate::role_observations::read_r3(&a.fixture.root, &entry)["state"],
        "limited"
    );
    std::fs::remove_file(&role_dir).unwrap();
    std::fs::rename(&held, &role_dir).unwrap();
    assert!(cap.verify(&a.fixture.root).is_ok());
    let old = a
        .fixture
        .root
        .with_file_name(crate::util::opaque_id("role-r3-project-held-").unwrap());
    std::fs::rename(&a.fixture.root, &old).unwrap();
    std::fs::create_dir(&a.fixture.root).unwrap();
    assert!(cap
        .verify(&a.fixture.root)
        .unwrap_err()
        .contains("replaced"));
    std::fs::remove_dir(&a.fixture.root).unwrap();
    std::fs::rename(&old, &a.fixture.root).unwrap();
}
#[test]
fn role_r3_pending_write_rechecks_original_limit_payload_and_retries_once() {
    let _store = RoleR3Store::new();
    let peer = Peer::new();
    let composition = role_r3_composition(Some(crate::role_supply::Role::HELP_HUMAN), false);
    let thread = role_r3_start(&peer, &composition);
    let mut root = peer.registered();
    let (review, revision) = review_of(&root);
    root.select_hot_registered_copy(
        &crate::workflow_selection::Chat::in_home(&peer.home, &thread),
        &review,
        &revision,
    )
    .unwrap();
    let reference = root
        .prepare_run(
            peer.home.clone(),
            &peer.generation,
            &thread,
            "held role write".into(),
            peer.project(),
        )
        .unwrap();
    let log = crate::records::supply::run_log(&peer.fixture.root, &reference).unwrap();
    std::fs::create_dir_all(&log).unwrap();
    let run = root.runs[&reference].clone();
    run.lock().unwrap().send().unwrap();
    let (id, at) = {
        let r = run.lock().unwrap();
        let e = r
            .entries
            .iter()
            .find(|e| e.kind == "supplied_guidance")
            .unwrap();
        assert!(e.pending());
        (e.record_id.clone(), e.observed_at.clone())
    };
    let role_dir = crate::records_store::attach(&peer.fixture.root, false)
        .unwrap()
        .dir
        .unwrap()
        .join("role-supply");
    let quoted = crate::role_observations::RoleLog::open(&peer.fixture.root)
        .unwrap()
        .read(peer.generation["home"].as_str().unwrap(), Some(&thread));
    let key = quoted["observations"][0]["record"]["appBytes"]["limitAccount"]["content"]["value"]
        .as_str()
        .unwrap();
    let payload = role_dir.join("content").join(format!("{key}.utf8"));
    let original = std::fs::read(&payload).unwrap();
    std::fs::remove_file(&payload).unwrap();
    std::fs::remove_dir(&log).unwrap();
    run.lock().unwrap().retry_records().unwrap();
    assert!(!peer
        .fixture
        .rs_entries()
        .iter()
        .any(|e| e["recordId"] == id));
    std::fs::write(&payload, &original).unwrap();
    run.lock().unwrap().retry_records().unwrap();
    run.lock().unwrap().retry_records().unwrap();
    let records = peer.fixture.rs_entries();
    let entries = records
        .iter()
        .filter(|e| e["recordId"] == id)
        .collect::<Vec<_>>();
    assert_eq!(entries.len(), 1);
    assert_eq!(entries[0]["observedAt"], at);
    assert_eq!(
        crate::role_observations::read_r3(&peer.fixture.root, entries[0])["state"],
        "quoted historical correspondence"
    );
}
#[test]
fn role_r3_import_and_disposal_keep_source_admission_and_old_receipt_limits() {
    let _store = RoleR3Store::new();
    let peer = Peer::new();
    let c = role_r3_composition(None, false);
    let thread = role_r3_start(&peer, &c);
    let cap = peer
        .home
        .history
        .lock()
        .unwrap()
        .role_publication(peer.generation["home"].as_str().unwrap(), &thread)
        .unwrap()
        .unwrap();
    let legacy = peer
        .fixture
        .root
        .join(".chirality/records/acts/legacy.jsonl");
    std::fs::create_dir_all(legacy.parent().unwrap()).unwrap();
    crate::records::append(
        &legacy,
        "evidence_limit",
        &crate::records::APP_WRITER,
        json!({"label":"missing receipt","detail":"invented external legacy entry"}),
    )
    .unwrap();
    assert!(cap.verify(&peer.fixture.root).is_err());
    assert_eq!(
        crate::role_observations::RoleLog::open(&peer.fixture.root)
            .unwrap()
            .read(peer.generation["home"].as_str().unwrap(), Some(&thread))["complete"],
        false
    );
    crate::records_store::import(&peer.fixture.root).unwrap();
    assert!(cap.verify(&peer.fixture.root).is_ok());
    let mut root = peer.registered();
    let run = role_r3_open(&peer, &mut root, &thread);
    let entry = role_r3_entry(&peer, &run);
    root.runs[&run].lock().unwrap().end_run(None, None).unwrap();
    assert_eq!(
        crate::role_observations::read_r3(&peer.fixture.root, &entry)["state"],
        "quoted historical correspondence"
    );
    peer.home
        .host
        .stop("owned fixture settled", "retention condition")
        .unwrap();
    let actor = crate::act_control::person(Some("Invented fixture"), Some("fixture-os"));
    let observed = json!({"fixture":"no live human act"});
    let apply = |action, bag: Option<&std::path::Path>| {
        let plan =
            crate::records_retention::prepare(&peer.fixture.root, action, bag, &actor, &observed)?;
        crate::records_retention::apply(plan, &actor, &observed)
    };
    apply("close", None).unwrap();
    let bag = PathBuf::from("/private/tmp")
        .join(crate::util::opaque_id("role-r3-disposal-export-").unwrap());
    crate::records_export::export(&peer.fixture.root, &bag).unwrap();
    apply("dispose", Some(&bag)).unwrap();
    assert!(cap.verify(&peer.fixture.root).is_err());
    assert_eq!(
        crate::role_observations::read_r3(&peer.fixture.root, &entry)["state"],
        "limited"
    );
    crate::records_export::verify(&bag).unwrap();
    std::fs::remove_dir_all(&bag).unwrap();
}
#[test]
fn role_r3_same_project_equal_thread_ids_cross_home_and_run_context_substitution_refuse() {
    let _store = RoleR3Store::new();
    let a = Peer::new();
    let b = Peer::new();
    let log = Arc::new(crate::role_observations::RoleLog::open(&a.fixture.root).unwrap());
    a.home
        .history
        .lock()
        .unwrap()
        .configure_role_log_source(Ok(log.clone()));
    b.home
        .history
        .lock()
        .unwrap()
        .configure_role_log_source(Ok(log));
    let c = role_r3_composition(Some(crate::role_supply::Role::HELP_HUMAN), false);
    let ta = role_r3_start(&a, &c);
    let tb = role_r3_start(&b, &c);
    assert_eq!(ta, tb);
    let mut root = a.registered();
    let ra = role_r3_open(&a, &mut root, &ta);
    // Existing durable RE-4 remains conservative for bare IDs; end A before B.
    root.runs[&ra].lock().unwrap().end_run(None, None).unwrap();
    let (review, revision) = review_of(&root);
    root.select_hot_registered_copy(
        &crate::workflow_selection::Chat::in_home(&b.home, &tb),
        &review,
        &revision,
    )
    .unwrap();
    let rb = root
        .prepare_run(
            b.home.clone(),
            &b.generation,
            &tb,
            "second native home".into(),
            Some(&a.fixture.root),
        )
        .unwrap();
    root.runs[&rb].lock().unwrap().send().unwrap();
    let ea = role_r3_entry(&a, &ra);
    let eb = role_r3_entry(&a, &rb);
    let qa = crate::role_observations::read_r3(&a.fixture.root, &ea);
    let qb = crate::role_observations::read_r3(&a.fixture.root, &eb);
    assert_eq!(qa["state"], "quoted historical correspondence", "{qa}");
    assert_eq!(qb["state"], "quoted historical correspondence", "{qb}");
    assert_ne!(qa["runContext"]["home"], qb["runContext"]["home"]);
    assert_eq!(qa["runContext"]["home"], a.generation["home"]);
    assert_eq!(qb["runContext"]["home"], b.generation["home"]);
    let decode = |e: &Value| {
        serde_json::from_str::<Value>(
            e["body"]["supplyRecord"]["ref"]
                .as_str()
                .unwrap()
                .strip_prefix("role-run:v1:")
                .unwrap(),
        )
        .unwrap()
    };
    let mut wrong = decode(&ea);
    wrong[1] = decode(&eb)[1].clone();
    let mut body = ea["body"].clone();
    body["supplyRecord"]["ref"] = json!(format!("role-run:v1:{wrong}"));
    body["sourceIdentity"] = eb["body"]["sourceIdentity"].clone();
    let mut claim = crate::records::supply::PendingRunEntry::new(
        "supplied_guidance",
        body,
        crate::util::now_rfc3339(),
    )
    .unwrap();
    let stored =
        crate::records::supply::append_run_entry(&a.fixture.root, &ra, &mut claim).unwrap();
    assert_eq!(
        crate::role_observations::read_r3(&a.fixture.root, &stored)["state"],
        "limited"
    );
    let mut wrong_run = crate::records::supply::PendingRunEntry::new(
        "supplied_guidance",
        ea["body"].clone(),
        crate::util::now_rfc3339(),
    )
    .unwrap();
    let stored =
        crate::records::supply::append_run_entry(&a.fixture.root, &rb, &mut wrong_run).unwrap();
    assert_eq!(
        crate::role_observations::read_r3(&a.fixture.root, &stored)["state"],
        "limited"
    );
}
#[test]
fn role_r3_context_landed_unconfirmed_retries_original_private_bytes_without_native_send() {
    let _store = RoleR3Store::new();
    let peer = Peer::new();
    let c = role_r3_composition(None, false);
    let thread = role_r3_start(&peer, &c);
    let mut root = peer.registered();
    crate::role_observations::FAIL_CONTEXT_AFTER_FILE_SYNC.with(|f| f.set(true));
    let run = role_r3_open(&peer, &mut root, &thread);
    let held = root.runs[&run].clone();
    let (id, at) = {
        let r = held.lock().unwrap();
        let e = r
            .entries
            .iter()
            .find(|e| e.kind == "supplied_guidance")
            .unwrap();
        assert!(e.pending());
        assert!(e.failure.as_deref().unwrap().contains("unconfirmed"));
        (e.record_id.clone(), e.observed_at.clone())
    };
    let wire = peer.wire();
    held.lock().unwrap().retry_records().unwrap();
    held.lock().unwrap().retry_records().unwrap();
    let entries = peer.fixture.rs_entries();
    let found = entries
        .iter()
        .filter(|e| e["recordId"] == id)
        .collect::<Vec<_>>();
    assert_eq!(found.len(), 1);
    assert_eq!(found[0]["observedAt"], at);
    assert_eq!(
        crate::role_observations::read_r3(&peer.fixture.root, found[0])["state"],
        "quoted historical correspondence"
    );
    assert_eq!(peer.wire(), wire);
}
#[test]
fn role_r3_ended_context_and_entry_retries_hold_activity_against_another_controller() {
    let _store = RoleR3Store::new();
    let peer = Peer::new();
    let c = role_r3_composition(None, false);
    let thread = role_r3_start(&peer, &c);
    let mut root = peer.registered();
    crate::role_observations::FAIL_CONTEXT_AFTER_FILE_SYNC.with(|f| f.set(true));
    let reference = role_r3_open(&peer, &mut root, &thread);
    let held = root.runs[&reference].clone();
    let (id, at, context_key) = {
        let r = held.lock().unwrap();
        let entry = r
            .entries
            .iter()
            .find(|e| e.kind == "supplied_guidance")
            .unwrap();
        assert!(entry.pending());
        let context: Value = serde_json::from_str(
            entry.body["supplyRecord"]["ref"]
                .as_str()
                .unwrap()
                .strip_prefix("role-run:v1:")
                .unwrap(),
        )
        .unwrap();
        (
            entry.record_id.clone(),
            entry.observed_at.clone(),
            context[2]["content"]["value"].as_str().unwrap().to_owned(),
        )
    };
    let content = crate::records_store::attach(&peer.fixture.root, false)
        .unwrap()
        .dir
        .unwrap()
        .join("role-supply/content");
    let payload = content.join(format!("{context_key}.utf8"));
    let bytes = std::fs::read(&payload).unwrap();
    std::fs::remove_file(&payload).unwrap();
    std::fs::create_dir(&payload).unwrap();
    held.lock().unwrap().end_run(None, None).unwrap();
    peer.home
        .host
        .stop("owned fixture settled", "pending recording lifetime test")
        .unwrap();
    let second = WorkflowRootSession::default();
    let actor = crate::act_control::person(Some("Invented fixture"), Some("fixture-os"));
    let observed = json!({"fixture":"no live human act"});
    let close = || {
        second.retention_ready()?;
        crate::records_retention::prepare(&peer.fixture.root, "close", None, &actor, &observed)
    };
    second.retention_ready().unwrap();
    assert!(root.retention_ready().is_err());
    assert!(held.lock().unwrap().has_pending_records());
    assert!(close().err().unwrap().contains("Project activity"));
    // Context can now be confirmed, but the following R3 append is independently held.
    std::fs::remove_dir(&payload).unwrap();
    std::fs::write(&payload, &bytes).unwrap();
    let log = crate::records::supply::run_log(&peer.fixture.root, &reference).unwrap();
    let saved_log = log.with_extension("held-log");
    std::fs::rename(&log, &saved_log).unwrap();
    std::fs::create_dir(&log).unwrap();
    held.lock().unwrap().retry_records().unwrap();
    assert!(held.lock().unwrap().has_pending_records());
    assert!(close().err().unwrap().contains("Project activity"));
    std::fs::remove_dir(&log).unwrap();
    std::fs::rename(&saved_log, &log).unwrap();
    held.lock().unwrap().retry_records().unwrap();
    assert!(!held.lock().unwrap().has_pending_records());
    root.retention_ready().unwrap();
    let entries = peer.fixture.rs_entries();
    let found = entries
        .iter()
        .filter(|e| e["recordId"] == id)
        .collect::<Vec<_>>();
    assert_eq!(found.len(), 1);
    assert_eq!(found[0]["observedAt"], at);
    assert!(entries.iter().any(|e| e["kind"] == "evidence_limit"
        && e["body"]["subjectRef"] == id
        && e["body"]["label"] == "record write failed"));
    let plan = close().unwrap();
    crate::records_retention::apply(plan, &actor, &observed).unwrap();
}
#[test]
fn role_r3_cold_owning_run_preserves_regular_missing_torn_and_invalid_readings() {
    let _store = RoleR3Store::new();
    let peer = Peer::new();
    let thread = role_r3_start(&peer, &role_r3_composition(None, false));
    let mut root = peer.registered();
    let reference = role_r3_open(&peer, &mut root, &thread);
    let entry = role_r3_entry(&peer, &reference);
    let log = crate::records::supply::run_log(&peer.fixture.root, &reference).unwrap();
    let bytes = std::fs::read(&log).unwrap();
    let read = || crate::role_observations::read_r3(&peer.fixture.root, &entry);
    assert_eq!(read()["state"], "quoted historical correspondence");
    std::fs::remove_file(&log).unwrap();
    assert_eq!(read()["state"], "limited");
    // Preserve the R3 itself; the separate torn tail exercises the source limit.
    std::fs::write(&log, [&bytes[..], b"{\"invented-torn-tail\":"].concat()).unwrap();
    let torn = read();
    assert_eq!(torn["state"], "limited");
    assert!(torn["limits"].to_string().contains("partial"), "{torn}");
    std::fs::write(
        &log,
        [&bytes[..], b"{\"invented-invalid-record\":true}\n"].concat(),
    )
    .unwrap();
    assert_eq!(read()["state"], "limited");
    std::fs::write(
        &log,
        [
            &bytes[..],
            b"{\"invented-invalid-record\":true}\n{\"torn-tail\":",
        ]
        .concat(),
    )
    .unwrap();
    let (_, expected_limits) = crate::records::read_log(&log);
    let mixed = read();
    assert_eq!(mixed["state"], "limited");
    assert_eq!(
        mixed["limits"][0],
        format!("role R3 owning run source incomplete: {expected_limits:?}")
    );
    std::fs::write(&log, &bytes).unwrap();
    assert_eq!(read()["state"], "quoted historical correspondence");
}
#[test]
fn role_r3_cold_owning_run_refuses_fifo_without_producer_eof() {
    use std::os::unix::{ffi::OsStrExt, fs::OpenOptionsExt};
    let store = RoleR3Store::new();
    let peer = Peer::new();
    let thread = role_r3_start(&peer, &role_r3_composition(None, false));
    let mut root = peer.registered();
    let reference = role_r3_open(&peer, &mut root, &thread);
    let entry = role_r3_entry(&peer, &reference);
    let log = crate::records::supply::run_log(&peer.fixture.root, &reference).unwrap();
    let bytes = std::fs::read(&log).unwrap();
    std::fs::remove_file(&log).unwrap();
    let name = std::ffi::CString::new(log.as_os_str().as_bytes()).unwrap();
    assert_eq!(unsafe { libc::mkfifo(name.as_ptr(), 0o600) }, 0);
    let owner = std::fs::OpenOptions::new()
        .read(true)
        .write(true)
        .custom_flags(libc::O_NONBLOCK)
        .open(&log)
        .unwrap();
    let project = peer.fixture.root.clone();
    let test_store = crate::records_store::Store {
        root: store.0.clone(),
        placement: crate::records_store::Placement::Test,
        limits: vec![],
    };
    let (tx, rx) = std::sync::mpsc::channel();
    let worker = std::thread::spawn(move || {
        crate::records_store::use_store_for_test(Some(Ok(test_store)));
        let reading = crate::role_observations::read_r3(&project, &entry);
        crate::records_store::use_store_for_test(None);
        tx.send(reading).unwrap();
    });
    let before_eof = rx.recv_timeout(Duration::from_secs(2)).ok();
    drop(owner);
    worker.join().unwrap();
    std::fs::remove_file(&log).unwrap();
    std::fs::write(&log, &bytes).unwrap();
    assert!(
        before_eof.is_some(),
        "cold R3 source read waited for a nonregular producer's EOF"
    );
    let read = before_eof.unwrap();
    assert_eq!(read["state"], "limited", "{read}");
    assert_eq!(read["currentRoleAuthorityRestored"], false);
}
#[test]
fn role_r3_cold_owning_run_refuses_leaf_links_and_parent_aliases() {
    let _store = RoleR3Store::new();
    let peer = Peer::new();
    let thread = role_r3_start(&peer, &role_r3_composition(None, false));
    let mut root = peer.registered();
    let reference = role_r3_open(&peer, &mut root, &thread);
    let entry = role_r3_entry(&peer, &reference);
    let log = crate::records::supply::run_log(&peer.fixture.root, &reference).unwrap();
    let original = log.with_extension("held");
    std::fs::rename(&log, &original).unwrap();
    let read = || crate::role_observations::read_r3(&peer.fixture.root, &entry);
    std::os::unix::fs::symlink(&original, &log).unwrap();
    assert_eq!(read()["state"], "limited");
    std::fs::remove_file(&log).unwrap();
    std::fs::hard_link(&original, &log).unwrap();
    assert_eq!(read()["state"], "limited");
    std::fs::remove_file(&log).unwrap();
    std::fs::rename(&original, &log).unwrap();
    let parent = log.parent().unwrap();
    let moved = parent.with_extension("held");
    std::fs::rename(parent, &moved).unwrap();
    std::os::unix::fs::symlink(&moved, parent).unwrap();
    assert_eq!(read()["state"], "limited");
    std::fs::remove_file(parent).unwrap();
    std::fs::rename(&moved, parent).unwrap();
    assert_eq!(read()["state"], "quoted historical correspondence");
}
#[test]
fn role_r3_cold_owning_run_refuses_parent_replacement_during_descriptor_open() {
    let _store = RoleR3Store::new();
    let peer = Peer::new();
    let thread = role_r3_start(&peer, &role_r3_composition(None, false));
    let mut root = peer.registered();
    let reference = role_r3_open(&peer, &mut root, &thread);
    let entry = role_r3_entry(&peer, &reference);
    let log = crate::records::supply::run_log(&peer.fixture.root, &reference).unwrap();
    let parent = log.parent().unwrap().to_owned();
    let moved = parent.with_extension("held");
    let for_hook = parent.clone();
    let moved_hook = moved.clone();
    let _hook = crate::records_index::log_open_hook_for_test(&log, Some(&parent), 0, move || {
        std::fs::rename(&for_hook, &moved_hook).unwrap();
        std::fs::create_dir(&for_hook).unwrap();
    });
    let read = crate::role_observations::read_r3(&peer.fixture.root, &entry);
    std::fs::remove_dir(&parent).unwrap();
    std::fs::rename(&moved, &parent).unwrap();
    assert_eq!(read["state"], "limited", "{read}");
    assert_eq!(
        crate::role_observations::read_r3(&peer.fixture.root, &entry)["state"],
        "quoted historical correspondence"
    );
}
#[test]
fn role_r3_cold_owning_run_refuses_same_bytes_replacement_at_final_named_check() {
    let _store = RoleR3Store::new();
    let peer = Peer::new();
    let thread = role_r3_start(&peer, &role_r3_composition(None, false));
    let mut root = peer.registered();
    let reference = role_r3_open(&peer, &mut root, &thread);
    let entry = role_r3_entry(&peer, &reference);
    let log = crate::records::supply::run_log(&peer.fixture.root, &reference).unwrap();
    let bytes = std::fs::read(&log).unwrap();
    let original = log.with_extension("held");
    let for_hook = log.clone();
    let held_hook = original.clone();
    let copy = bytes.clone();
    let _hook = crate::records_index::log_open_hook_for_test(&log, None, 1, move || {
        std::fs::rename(&for_hook, &held_hook).unwrap();
        std::fs::write(&for_hook, &copy).unwrap();
    });
    let read = crate::role_observations::read_r3(&peer.fixture.root, &entry);
    assert!(original.is_file(), "the final named-file substitution ran");
    std::fs::remove_file(&log).unwrap();
    std::fs::rename(&original, &log).unwrap();
    assert_eq!(read["state"], "limited", "{read}");
    assert_eq!(
        crate::role_observations::read_r3(&peer.fixture.root, &entry)["state"],
        "quoted historical correspondence"
    );
}
// Invented recorded corrections retain actual schema/sequence/chain semantics;
// the fixture does not claim a human correction or an App publication callback.
fn role_r3_correction_fixture(
    log: &std::path::Path,
    original: &Value,
    target: &str,
    wrong_kind: bool,
) -> Value {
    use std::io::Write;
    let bytes = std::fs::read(log).unwrap_or_default();
    let (prior, limits) = crate::records::read_log(log);
    assert!(limits.is_empty());
    let mut record = original.clone();
    record["recordId"] = json!(crate::util::opaque_id("rec:app:").unwrap());
    record["seq"] = json!(
        prior
            .iter()
            .filter_map(|e| e["seq"].as_u64())
            .max()
            .unwrap_or(0)
            + 1
    );
    record["corrects"] = json!(target);
    record["correctionReason"] = json!("Invented fixture correction");
    let last = bytes
        .strip_suffix(b"\n")
        .unwrap_or(&bytes)
        .rsplit(|b| *b == b'\n')
        .next()
        .filter(|b| !b.is_empty());
    record["prevLine"] =
        crate::record_lines::link(last.map(crate::record_lines::line_identity).as_deref());
    if wrong_kind {
        record["kind"] = json!("evidence_limit");
        record["body"] =
            json!({"label":"missing receipt","detail":"Invented wrong-kind correction source"});
    } else {
        record["body"]["content"] =
            crate::role_supply::content(b"Invented substitute role composition");
    }
    crate::schema_validation::bundled()
        .unwrap()
        .validate(&record)
        .unwrap();
    std::fs::create_dir_all(log.parent().unwrap()).unwrap();
    let mut file = std::fs::OpenOptions::new()
        .create(true)
        .append(true)
        .open(log)
        .unwrap();
    file.write_all(&serde_json::to_vec(&record).unwrap())
        .unwrap();
    file.write_all(b"\n").unwrap();
    file.sync_all().unwrap();
    record
}
#[test]
fn role_r3_cold_dto_discloses_correction_without_replacing_original_quote() {
    let _store = RoleR3Store::new();
    let peer = Peer::new();
    let composition = role_r3_composition(None, false);
    let thread = role_r3_start(&peer, &composition);
    let mut root = peer.registered();
    let reference = role_r3_open(&peer, &mut root, &thread);
    let original = role_r3_entry(&peer, &reference);
    let log = crate::records::supply::run_log(&peer.fixture.root, &reference).unwrap();
    let correction = role_r3_correction_fixture(
        &log,
        &original,
        original["recordId"].as_str().unwrap(),
        false,
    );
    let wire = peer.wire();
    let project =
        crate::workflow_workspace::publication::ProjectRecords::open(&peer.fixture.root).unwrap();
    let dto = crate::records::supply::read_project_supply(&project);
    let quote = dto["roleSupplies"]
        .as_array()
        .unwrap()
        .iter()
        .find(|e| e["recordId"] == original["recordId"])
        .unwrap();
    assert_eq!(
        quote["state"], "quoted historical correspondence",
        "{quote}"
    );
    assert_eq!(quote["sourceBytes"]["composed"], composition.text);
    assert_eq!(quote["correctedBy"], json!([correction["recordId"]]));
    assert_eq!(
        quote["currentClaimStanding"],
        "corrected recorded claim; original quote retained"
    );
    assert!(quote["limits"].to_string().contains("has corrections"));
    assert_eq!(quote["currentRoleAuthorityRestored"], false);
    assert_eq!(peer.wire(), wire);
}
#[test]
fn role_r3_cold_dto_retains_cross_log_branches_and_invalid_correction_limits() {
    let _store = RoleR3Store::new();
    let peer = Peer::new();
    let thread = role_r3_start(&peer, &role_r3_composition(None, false));
    let mut root = peer.registered();
    let reference = role_r3_open(&peer, &mut root, &thread);
    let original = role_r3_entry(&peer, &reference);
    let own = crate::records::supply::run_log(&peer.fixture.root, &reference).unwrap();
    let a = role_r3_correction_fixture(
        &own,
        &original,
        original["recordId"].as_str().unwrap(),
        false,
    );
    let other = crate::storage::project_log(
        &peer.fixture.root,
        Some(&reference),
        "invented-role-correction-writer",
    )
    .unwrap();
    let b = role_r3_correction_fixture(
        &other,
        &original,
        original["recordId"].as_str().unwrap(),
        false,
    );
    let branched = crate::role_observations::read_r3(&peer.fixture.root, &original);
    let mut ids = vec![a["recordId"].clone(), b["recordId"].clone()];
    ids.sort_by(|a, b| a.as_str().cmp(&b.as_str()));
    assert_eq!(branched["correctedBy"], json!(ids));
    assert_eq!(
        branched["currentClaimStanding"],
        "unresolved recorded relations; original quote only"
    );
    assert_eq!(
        branched["correctionGroups"][0]["resolution"],
        "ambiguous/unresolved correction branches"
    );
    let wrong = role_r3_correction_fixture(
        &other,
        &original,
        original["recordId"].as_str().unwrap(),
        true,
    );
    let invalid = crate::role_observations::read_r3(&peer.fixture.root, &original);
    assert!(invalid["relationDiagnostics"]
        .as_array()
        .unwrap()
        .iter()
        .any(|d| d["recordId"] == wrong["recordId"]
            && d["reason"] == "nonconformant correction: reason/same-kind rule"));
    assert_eq!(invalid["state"], "quoted historical correspondence");
    let missing =
        role_r3_correction_fixture(&own, &original, "rec:app:invented-absent-target", false);
    let unknown = crate::role_observations::read_r3(&peer.fixture.root, &missing);
    assert_eq!(unknown["relationLimit"], "unresolvable correction target");
    assert_eq!(unknown["currentRoleAuthorityRestored"], false);
}
#[test]
fn role_r3_cold_context_source_root_must_match_actual_selection_and_opened_source() {
    let _store = RoleR3Store::new();
    let peer = Peer::new();
    let thread = role_r3_start(&peer, &role_r3_composition(None, false));
    let mut root = peer.registered();
    let reference = role_r3_open(&peer, &mut root, &thread);
    let original = role_r3_entry(&peer, &reference);
    let before = crate::role_observations::read_r3(&peer.fixture.root, &original);
    assert_eq!(before["state"], "quoted historical correspondence");
    let mut context = before["runContext"].clone();
    context["scope"]["sourceRoot"] = json!("invented:wrong-library-source");
    let bytes = serde_json::to_vec(&context).unwrap();
    let payload = json!({"content":crate::role_supply::content(&bytes),"byteLength":bytes.len()});
    let content = crate::records_store::attach(&peer.fixture.root, false)
        .unwrap()
        .dir
        .unwrap()
        .join("role-supply/content");
    std::fs::write(
        content.join(format!(
            "{}.utf8",
            payload["content"]["value"].as_str().unwrap()
        )),
        &bytes,
    )
    .unwrap();
    let mut tuple: Value = serde_json::from_str(
        original["body"]["supplyRecord"]["ref"]
            .as_str()
            .unwrap()
            .strip_prefix("role-run:v1:")
            .unwrap(),
    )
    .unwrap();
    tuple[2] = payload;
    let mut body = original["body"].clone();
    body["supplyRecord"]["ref"] = json!(format!("role-run:v1:{tuple}"));
    let mut claim = crate::records::supply::PendingRunEntry::new(
        "supplied_guidance",
        body,
        crate::util::now_rfc3339(),
    )
    .unwrap();
    let recorded =
        crate::records::supply::append_run_entry(&peer.fixture.root, &reference, &mut claim)
            .unwrap();
    assert_eq!(
        crate::role_observations::read_r3(&peer.fixture.root, &recorded)["state"],
        "limited"
    );
    assert_eq!(
        crate::role_observations::read_r3(&peer.fixture.root, &original)["state"],
        "quoted historical correspondence"
    );
}
#[test]
fn role_r3_cold_closed_kept_project_quotes_without_a_write_path() {
    let _store = RoleR3Store::new();
    let peer = Peer::new();
    let thread = role_r3_start(&peer, &role_r3_composition(None, false));
    let mut root = peer.registered();
    let reference = role_r3_open(&peer, &mut root, &thread);
    let entry = role_r3_entry(&peer, &reference);
    root.runs[&reference]
        .lock()
        .unwrap()
        .end_run(None, None)
        .unwrap();
    peer.home
        .host
        .stop("owned fixture settled", "cold closed read test")
        .unwrap();
    let actor = crate::act_control::person(Some("Invented fixture"), Some("fixture-os"));
    let observed = json!({"fixture":"no live human act"});
    let plan =
        crate::records_retention::prepare(&peer.fixture.root, "close", None, &actor, &observed)
            .unwrap();
    crate::records_retention::apply(plan, &actor, &observed).unwrap();
    assert!(crate::records_store::write_dir(&peer.fixture.root).is_err());
    let wire = peer.wire();
    let quote = crate::role_observations::read_r3(&peer.fixture.root, &entry);
    assert_eq!(
        quote["state"], "quoted historical correspondence",
        "{quote}"
    );
    assert_eq!(quote["currentRoleAuthorityRestored"], false);
    let project =
        crate::workflow_workspace::publication::ProjectRecords::open(&peer.fixture.root).unwrap();
    let dto = crate::records::supply::read_project_supply(&project);
    assert!(dto["roleSupplies"]
        .as_array()
        .unwrap()
        .iter()
        .any(|r| r["recordId"] == entry["recordId"]
            && r["state"] == "quoted historical correspondence"));
    assert_eq!(peer.wire(), wire);
}
#[test]
fn role_r3_cold_public_dto_preserves_prior_global_duplicate_identity_limits() {
    let _store = RoleR3Store::new();
    let peer = Peer::new();
    let thread = role_r3_start(&peer, &role_r3_composition(None, false));
    let mut root = peer.registered();
    let reference = role_r3_open(&peer, &mut root, &thread);
    let original = role_r3_entry(&peer, &reference);
    let log = crate::records::supply::run_log(&peer.fixture.root, &reference).unwrap();
    let non_role = crate::records::append_project(
        &peer.fixture.root,
        None,
        "invented-non-role-source",
        "evidence_limit",
        &crate::records::APP_WRITER,
        json!({"label":"missing receipt","detail":"Invented non-role claim"}),
    )
    .unwrap();
    let other =
        crate::storage::project_log(&peer.fixture.root, None, "invented-non-role-source").unwrap();
    std::fs::copy(&log, log.with_file_name("invented-copy.jsonl")).unwrap();
    std::fs::copy(&other, other.with_file_name("invented-other-copy.jsonl")).unwrap();
    // The previous set reader puts all torn tails after ordinary limits and
    // duplicate warnings, independently of which source was enumerated first.
    let source = std::fs::read(&other).unwrap();
    std::fs::write(
        &other,
        [
            &source[..],
            b"{\"invented-invalid-record\":true}\n{\"invented-torn-tail\":",
        ]
        .concat(),
    )
    .unwrap();
    let (prior, prior_limits) = crate::storage::read_all(&peer.fixture.root);
    assert_eq!(
        prior_limits
            .iter()
            .filter(|l| l.starts_with("duplicate record identity:"))
            .count(),
        3
    );
    let wire = peer.wire();
    let project =
        crate::workflow_workspace::publication::ProjectRecords::open(&peer.fixture.root).unwrap();
    let dto = crate::records::supply::read_project_supply(&project);
    assert_eq!(dto["rsLimits"], json!(prior_limits));
    let (read, limits, _) = crate::role_observations::read_project_sources(&peer.fixture.root);
    assert_eq!(read, prior, "all readable duplicate copies stay retained");
    assert_eq!(json!(limits), dto["rsLimits"]);
    assert_eq!(
        read.iter()
            .filter(|e| e["recordId"] == non_role["recordId"])
            .count(),
        2
    );
    assert_eq!(
        dto["roleSupplies"]
            .as_array()
            .unwrap()
            .iter()
            .filter(|e| e["recordId"] == original["recordId"])
            .count(),
        2
    );
    assert_eq!(peer.wire(), wire);
}
