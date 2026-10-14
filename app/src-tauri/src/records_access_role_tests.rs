// Actual Host-issued R3 fixtures through the ordinary capability. The owned
// synthetic supplier is not a provider/human witness and creates no authority.
fn records_access_role_call(n: u64, run: &str) -> crate::records_access::Call {
    crate::records_access::Call {
        app_session: "fixture-app".into(),
        generation: "fixture-generation".into(),
        request: json!(n),
        thread: "fixture-thread".into(),
        turn: "fixture-turn".into(),
        call: format!("role-call-{n}"),
        arguments: json!({"operation":"read_run","run":run,"limit":50}),
    }
}
fn records_access_role_answer(
    cap: &crate::records_access::RecordsCapability,
    peer: &Peer,
    run: &str,
    n: u64,
) -> Value {
    let reply = cap.answer(
        &records_access_role_call(n, run),
        Some(peer.fixture.root.to_str().unwrap()),
    );
    assert_eq!(reply["success"], true, "{reply}");
    serde_json::from_str(reply["contentItems"][0]["text"].as_str().unwrap()).unwrap()
}
fn records_access_role_item<'a>(document: &'a Value, entry: &Value) -> &'a Value {
    document["items"]
        .as_array()
        .unwrap()
        .iter()
        .find(|v| v["quoted"]["recordId"] == entry["recordId"])
        .unwrap()
}
#[test]
fn records_access_role_actual_start_fork_and_no_role_preserve_r3_and_read_accounting() {
    for (role, fork) in [
        (Some(crate::role_supply::Role::HELP_HUMAN), false),
        (Some(crate::role_supply::Role::WORKING_ITEMS), true),
        (None, false),
    ] {
        let _store = RoleR3Store::new();
        let peer = Peer::new();
        let composition = role_r3_composition(role, false);
        let parent = role_r3_start(&peer, &composition);
        let thread = if fork {
            crate::conversation_roles::fork_conversation(
                &peer.home,
                &peer.generation,
                &parent,
                Duration::from_secs(2),
            )
            .unwrap()["thread"]["threadId"]
                .as_str()
                .unwrap()
                .to_owned()
        } else {
            parent.clone()
        };
        let mut root = peer.registered();
        let run = role_r3_open(&peer, &mut root, &thread);
        let entry = role_r3_entry(&peer, &run);
        let cap = crate::records_access::RecordsCapability::new(&peer.fixture.root).unwrap();
        let document = records_access_role_answer(&cap, &peer, &run, 1);
        let item = records_access_role_item(&document, &entry);
        assert_eq!(item["quoted"], entry, "original R3 is unchanged");
        let reading = &item["supplierReading"];
        assert_eq!(
            reading["state"], "historical role metadata available",
            "{reading}"
        );
        assert_eq!(reading["role"], role.map_or("none", |r| r.name()));
        assert_eq!(reading["adoption"], "unknown");
        assert_eq!(reading["currentRoleAuthorityRestored"], false);
        assert_eq!(
            reading["lineage"].as_array().unwrap().len(),
            if fork { 2 } else { 1 }
        );
        assert_eq!(reading["runContext"]["thread"], thread);
        assert!(
            reading["limits"]
                .as_array()
                .unwrap()
                .iter()
                .any(|v| v == "wr-check-omitted")
        );
        if role.is_none() {
            assert_eq!(reading["limitAccount"]["limits"], json!([]));
        }
        let text = serde_json::to_string(reading).unwrap();
        for withheld in [
            "sourceBytes",
            "sourceObservations",
            "scope",
            "requestIdentity",
            "generation",
            composition.text.as_str(),
            peer.fixture.root.to_str().unwrap(),
        ] {
            assert!(!text.contains(withheld), "{withheld} escaped: {text}");
        }
        let log = cap.snapshot()["readLog"].as_str().unwrap().to_owned();
        let logged: Value = serde_json::from_str(
            std::fs::read_to_string(log)
                .unwrap()
                .lines()
                .last()
                .unwrap(),
        )
        .unwrap();
        let final_text = serde_json::to_string(&document).unwrap();
        assert_eq!(logged["returned"]["bytes"], final_text.len());
        assert_eq!(
            logged["returned"]["content"]["value"],
            crate::util::sha256_hex(final_text.as_bytes())
        );
        let definition = crate::records_access::definition();
        assert_eq!(
            definition["inputSchema"]["properties"]["operation"]["enum"],
            json!(["list_runs", "read_run", "read_acts"])
        );
        if fork {
            assert!(
                peer.wire()
                    .iter()
                    .find(|f| f["method"] == "thread/fork")
                    .unwrap()["params"]
                    .get("dynamicTools")
                    .is_none()
            );
        }
    }
}
fn records_access_role_dir(peer: &Peer) -> PathBuf {
    crate::records_store::attach(&peer.fixture.root, false)
        .unwrap()
        .dir
        .unwrap()
        .join("role-supply")
}
fn records_access_role_context(entry: &Value, peer: &Peer) -> PathBuf {
    let tuple: Value = serde_json::from_str(
        entry["body"]["supplyRecord"]["ref"]
            .as_str()
            .unwrap()
            .strip_prefix("role-run:v1:")
            .unwrap(),
    )
    .unwrap();
    records_access_role_dir(peer).join("content").join(format!(
        "{}.utf8",
        tuple[2]["content"]["value"].as_str().unwrap()
    ))
}
fn records_access_role_omitted(
    cap: &crate::records_access::RecordsCapability,
    peer: &Peer,
    run: &str,
    entry: &Value,
    n: u64,
    code: &str,
) {
    let document = records_access_role_answer(cap, peer, run, n);
    let item = records_access_role_item(&document, entry);
    assert_eq!(item["quoted"], *entry);
    assert_eq!(
        item["supplierReading"]["state"], "historical role metadata omitted",
        "{item}"
    );
    assert!(
        item["supplierReading"]["limits"]
            .as_array()
            .unwrap()
            .iter()
            .any(|v| v == code),
        "{item}"
    );
    assert_eq!(
        item["supplierReading"]["currentRoleAuthorityRestored"],
        false
    );
}
#[test]
fn records_access_role_warm_cross_log_corrections_and_incomplete_sources_qualify_original() {
    let _store = RoleR3Store::new();
    let peer = Peer::new();
    let thread = role_r3_start(&peer, &role_r3_composition(None, false));
    let mut root = peer.registered();
    let run = role_r3_open(&peer, &mut root, &thread);
    let entry = role_r3_entry(&peer, &run);
    let cap = crate::records_access::RecordsCapability::new(&peer.fixture.root).unwrap();
    assert_eq!(
        records_access_role_item(&records_access_role_answer(&cap, &peer, &run, 1), &entry)["supplierReading"]
            ["state"],
        "historical role metadata available"
    );
    let path =
        crate::storage::project_log(&peer.fixture.root, None, "invented-role-correction-writer")
            .unwrap();
    role_r3_correction_fixture(&path, &entry, entry["recordId"].as_str().unwrap(), false);
    records_access_role_omitted(&cap, &peer, &run, &entry, 2, "role-record-has-corrections");
    let bytes = std::fs::read(&path).unwrap();
    std::fs::write(
        &path,
        [
            bytes.as_slice(),
            b"{\"PRIVATE-PARSER-CANARY\":\"REFUSED-AUX\"}\n",
        ]
        .concat(),
    )
    .unwrap();
    records_access_role_omitted(&cap, &peer, &run, &entry, 3, "role-record-relation-unknown");
    let text = records_access_role_answer(&cap, &peer, &run, 4).to_string();
    assert!(!text.contains("PRIVATE-PARSER-CANARY") && !text.contains("REFUSED-AUX"));
}
#[test]
fn records_access_role_missing_tampered_alias_fifo_and_validator_errors_never_leak_or_reconstruct()
{
    for mode in ["missing", "tampered", "alias", "fifo", "parser"] {
        let _store = RoleR3Store::new();
        let peer = Peer::new();
        let thread = role_r3_start(&peer, &role_r3_composition(None, false));
        let mut root = peer.registered();
        let run = role_r3_open(&peer, &mut root, &thread);
        let entry = role_r3_entry(&peer, &run);
        let path = records_access_role_context(&entry, &peer);
        let raw = std::fs::read(&path).unwrap();
        match mode {
            "tampered" => {
                let mut changed = raw.clone();
                changed[0] = b'!';
                std::fs::write(&path, changed).unwrap();
            }
            "parser" => {
                std::fs::write(records_access_role_dir(&peer).join("observations.jsonl"),b"{\"format\":\"PRIVATE-VALIDATOR-CANARY\",\"arbitrary\":\"RAW-AUX-GUIDANCE\"}\n").unwrap();
            }
            other => {
                std::fs::remove_file(&path).unwrap();
                match other {
                    "alias" => {
                        let moved = path.with_extension("saved");
                        std::fs::write(&moved, &raw).unwrap();
                        std::os::unix::fs::symlink(&moved, &path).unwrap();
                    }
                    "fifo" => {
                        let name = std::ffi::CString::new(path.to_str().unwrap()).unwrap();
                        assert_eq!(unsafe { libc::mkfifo(name.as_ptr(), 0o600) }, 0);
                    }
                    _ => {}
                }
            }
        }
        let cap = crate::records_access::RecordsCapability::new(&peer.fixture.root).unwrap();
        records_access_role_omitted(&cap, &peer, &run, &entry, 1, "role-source-unavailable");
        let document = records_access_role_answer(&cap, &peer, &run, 2);
        let reading = &records_access_role_item(&document, &entry)["supplierReading"];
        let text = reading.to_string();
        for hidden in [
            "PRIVATE-VALIDATOR-CANARY",
            "RAW-AUX-GUIDANCE",
            path.to_str().unwrap(),
            "sourceBytes",
            "scope",
        ] {
            assert!(!text.contains(hidden), "{mode}: {text}");
        }
    }
}
#[test]
fn records_access_role_descriptor_budget_rejects_newline_free_and_racing_growth() {
    use std::io::Write;
    for racing in [false, true] {
        let _store = RoleR3Store::new();
        let peer = Peer::new();
        let thread = role_r3_start(&peer, &role_r3_composition(None, false));
        let mut root = peer.registered();
        let run = role_r3_open(&peer, &mut root, &thread);
        let entry = role_r3_entry(&peer, &run);
        let path = records_access_role_dir(&peer).join("observations.jsonl");
        if racing {
            crate::role_observations::METADATA_BEFORE_READ.with(|h| {
                *h.borrow_mut() = Some(Box::new(move || {
                    let mut out = std::fs::OpenOptions::new().append(true).open(path).unwrap();
                    out.write_all(&vec![b'x'; 1024 * 1024 + 1]).unwrap();
                    out.sync_all().unwrap();
                }))
            });
        } else {
            std::fs::write(&path, vec![b'x'; 1024 * 1024 + 1]).unwrap();
        }
        let cap = crate::records_access::RecordsCapability::new(&peer.fixture.root).unwrap();
        records_access_role_omitted(&cap, &peer, &run, &entry, 1, "role-source-budget-omitted");
        assert!(crate::role_observations::METADATA_BEFORE_READ.with(|h| h.borrow().is_none()));
    }
}
struct RecordsAccessRoleSnapshot(Vec<Value>);
impl crate::records_access::RecordsSource for RecordsAccessRoleSnapshot {
    fn read(&self) -> crate::records_access::Corpus {
        crate::records_access::Corpus {
            entries: self
                .0
                .iter()
                .cloned()
                .enumerate()
                .map(|(n, entry)| crate::records_access::SourcedEntry {
                    entry,
                    log: "invented-snapshot.jsonl".into(),
                    line: n + 1,
                })
                .collect(),
            limits: vec![],
        }
    }
}
fn records_access_role_snapshot_cap(
    peer: &Peer,
    entries: Vec<Value>,
    dir: &std::path::Path,
) -> crate::records_access::RecordsCapability {
    crate::records_access::RecordsCapability::with_source(
        &peer.fixture.root,
        Box::new(RecordsAccessRoleSnapshot(entries)),
        dir.join(crate::util::opaque_id("reads-").unwrap()),
    )
    .unwrap()
}
#[test]
fn records_access_role_other_project_and_relation_budget_do_not_expose_foreign_or_large_sources() {
    let store = RoleR3Store::new();
    let peer = Peer::new();
    let thread = role_r3_start(&peer, &role_r3_composition(None, false));
    let mut root = peer.registered();
    let run = role_r3_open(&peer, &mut root, &thread);
    let entry = role_r3_entry(&peer, &run);
    let mut foreign = entry.clone();
    let mut tuple: Value = serde_json::from_str(
        entry["body"]["supplyRecord"]["ref"]
            .as_str()
            .unwrap()
            .strip_prefix("role-run:v1:")
            .unwrap(),
    )
    .unwrap();
    tuple[0] = json!("FOREIGN-PROJECT-CANARY");
    foreign["body"]["supplyRecord"]["ref"] = json!(format!("role-run:v1:{tuple}"));
    let cap = records_access_role_snapshot_cap(&peer, vec![foreign.clone()], &store.0);
    records_access_role_omitted(&cap, &peer, &run, &foreign, 1, "role-source-other-project");
    assert!(!records_access_role_item(&records_access_role_answer(&cap,&peer,&run,2),&foreign)["supplierReading"].to_string().contains("FOREIGN-PROJECT-CANARY"));
    let mut records = peer.fixture.rs_entries();
    let mut large = crate::records::envelope(
        "evidence_limit",
        &crate::records::APP_WRITER,
        json!({"label":"missing receipt","detail":"HIDDEN-LARGE-CORRECTION".repeat(30_000)}),
        "rec:app:large-relation".into(),
        1,
        None,
        None,
    );
    large["corrects"] = entry["recordId"].clone();
    large["correctionReason"] = json!("Invented wrong-kind fixture");
    records.push(large);
    let cap = records_access_role_snapshot_cap(&peer, records, &store.0);
    records_access_role_omitted(&cap, &peer, &run, &entry, 3, "role-source-budget-omitted");
    assert!(
        !records_access_role_answer(&cap, &peer, &run, 4)
            .to_string()
            .contains("HIDDEN-LARGE-CORRECTION")
    );
}
#[test]
fn records_access_role_deep_fork_companion_is_stubbed_before_original_page_or_cursor() {
    let _store = RoleR3Store::new();
    let peer = Peer::new();
    let mut thread = role_r3_start(&peer, &role_r3_composition(None, false));
    for _ in 0..6 {
        thread = crate::conversation_roles::fork_conversation(
            &peer.home,
            &peer.generation,
            &thread,
            Duration::from_secs(2),
        )
        .unwrap()["thread"]["threadId"]
            .as_str()
            .unwrap()
            .to_owned();
    }
    let mut root = peer.registered();
    let run = role_r3_open(&peer, &mut root, &thread);
    let entry = role_r3_entry(&peer, &run);
    let cap = crate::records_access::RecordsCapability::new(&peer.fixture.root).unwrap();
    records_access_role_omitted(&cap, &peer, &run, &entry, 1, "role-companion-size-omitted");
    let document = records_access_role_answer(&cap, &peer, &run, 2);
    assert_eq!(document["next"], Value::Null);
    assert!(document["items"].as_array().unwrap().len() >= 2);
    assert!(document.to_string().len() <= crate::records_access::RESPONSE_LIMIT);
}
#[test]
fn records_access_role_actual_rpc_reply_has_enriched_read_log_before_supplier_observes_it() {
    use std::time::Instant;
    // Actual Host workers require a process store; the fixture's usual
    // thread-local override alone deliberately does not cross worker threads.
    struct RestoreStore(Result<crate::records_store::Store, String>);
    impl Drop for RestoreStore {
        fn drop(&mut self) {
            crate::records_store::configure(self.0.clone());
        }
    }
    let _restore = RestoreStore(crate::records_store::current());
    let _store = RoleR3Store::new();
    crate::records_store::configure(crate::records_store::current());
    let peer = Peer::new();
    let thread = role_r3_start(
        &peer,
        &role_r3_composition(Some(crate::role_supply::Role::HELP_HUMAN), false),
    );
    let mut root = peer.registered();
    let run = role_r3_open(&peer, &mut root, &thread);
    let entry = role_r3_entry(&peer, &run);
    peer.home
        .host
        .stop("owned fixture only", "metadata RPC setup")
        .unwrap();
    let script = peer.fixture.root.join("owned-peer.py");
    let source = std::fs::read_to_string(&script).unwrap();
    let hook = r#" elif method is None and f.get('id')=='role-records-call':
  import hashlib
  text=f['result']['contentItems'][0]['text']
  with open(mode('records-log')) as log:last=json.loads(log.readlines()[-1])
  with open('role-capability-observed.json','w') as out:json.dump({'reply':f,'read':last,'digest':hashlib.sha256(text.encode()).hexdigest(),'bytes':len(text.encode())},out)
  continue
 elif method=='turn/start' and mode('records-run'):
  emit({'id':f['id'],'result':{'turn':turn()}})
  emit({'id':'role-records-call','method':'item/tool/call','params':{'threadId':f['params']['threadId'],'turnId':'turn','callId':'role-records-call','tool':'chirality_records_read_v1','namespace':None,'arguments':{'operation':'read_run','run':mode('records-run')}}})
  continue
"#;
    assert_eq!(source.matches(" elif method=='turn/start':").count(), 1);
    std::fs::write(
        &script,
        source.replace(
            " elif method=='turn/start':",
            &format!("{hook} elif method=='turn/start':"),
        ),
    )
    .unwrap();
    let cap = Arc::new(crate::records_access::RecordsCapability::new(&peer.fixture.root).unwrap());
    peer.home.host.configure_records_capability(cap);
    peer.set_mode("records-run", &run);
    peer.set_mode(
        "records-log",
        crate::records_store::read_log_path(&peer.fixture.root)
            .unwrap()
            .to_str()
            .unwrap(),
    );
    let generation = peer.relaunch();
    peer.home
        .host
        .turn_start_text(
            &generation,
            "thread",
            "Rebuild context from the recorded run.",
        )
        .unwrap();
    let path = peer.fixture.root.join("role-capability-observed.json");
    let until = Instant::now() + Duration::from_secs(5);
    while !path.exists() {
        assert!(
            Instant::now() < until,
            "no owned supplier reply: {}",
            peer.home.host.snapshot()["serverRequests"]
        );
        std::thread::sleep(Duration::from_millis(10));
    }
    let observed: Value = serde_json::from_slice(&std::fs::read(path).unwrap()).unwrap();
    let document: Value = serde_json::from_str(
        observed["reply"]["result"]["contentItems"][0]["text"]
            .as_str()
            .unwrap(),
    )
    .unwrap();
    let item = records_access_role_item(&document, &entry);
    assert_eq!(item["quoted"], entry);
    assert_eq!(
        item["supplierReading"]["state"],
        "historical role metadata available"
    );
    assert_eq!(
        observed["read"]["returned"]["content"]["value"],
        observed["digest"]
    );
    assert_eq!(observed["read"]["returned"]["bytes"], observed["bytes"]);
    assert_eq!(
        observed["read"]["requestIdentity"],
        json!("\"role-records-call\"")
    );
    let starts: Vec<_> = peer
        .wire()
        .into_iter()
        .filter(|f| f["method"] == "thread/start")
        .collect();
    assert!(
        starts.last().unwrap()["params"]["dynamicTools"]
            .as_array()
            .unwrap()
            .iter()
            .any(|v| v == &crate::records_access::definition())
    );
    let status = peer.home.host.snapshot();
    assert!(
        !status.to_string().contains("supplierReading"),
        "request records never retain capability contents"
    );
}
#[test]
fn records_access_role_modified_guidance_and_hidden_context_are_metadata_only() {
    use crate::role_supply::{Composition, Guidance, Role};
    let _store = RoleR3Store::new();
    let peer = Peer::new();
    let common = Guidance::seeded(
        "AGENTS.md",
        INSTRUCTION_RELEASE,
        COMMON_DEFAULT.to_vec(),
        COMMON_DEFAULT,
    )
    .unwrap();
    let default = role_default(Role::HELPS_HUMANS);
    let role = Guidance::seeded(
        "agents/AGENT_HELPS_HUMANS.md",
        INSTRUCTION_RELEASE,
        [default, b"\nRAW-GUIDANCE-PRIVACY-CANARY\n"].concat(),
        default,
    )
    .unwrap();
    let composition = Composition::new(&common, Some((Role::HELPS_HUMANS, &role)), false).unwrap();
    let thread = role_r3_start(&peer, &composition);
    let mut root = peer.registered();
    let run = role_r3_open(&peer, &mut root, &thread);
    let entry = role_r3_entry(&peer, &run);
    let cap = crate::records_access::RecordsCapability::new(&peer.fixture.root).unwrap();
    let document = records_access_role_answer(&cap, &peer, &run, 1);
    let reading = &records_access_role_item(&document, &entry)["supplierReading"];
    assert_eq!(
        reading["state"], "historical role metadata available",
        "{reading}"
    );
    assert!(
        reading["limitAccount"]["limits"]
            .as_array()
            .unwrap()
            .iter()
            .all(|l| l["standing"] == "unknown")
    );
    assert!(!document.to_string().contains("RAW-GUIDANCE-PRIVACY-CANARY"));
    let raw = std::fs::read(records_access_role_context(&entry, &peer)).unwrap();
    let original: Value = serde_json::from_slice(&raw).unwrap();
    for (n, validator) in [(2, false), (3, true)] {
        let mut context = original.clone();
        context["scope"]["holdingLibrary"] = json!("HIDDEN-LIBRARY-CONTEXT-CANARY");
        if validator {
            context["observedTurnStatus"] = json!({"PRIVATE-VALIDATOR-CANARY":"raw context"});
        }
        let bytes = serde_json::to_vec(&context).unwrap();
        let payload =
            json!({"content":crate::role_supply::content(&bytes),"byteLength":bytes.len()});
        std::fs::write(
            records_access_role_dir(&peer).join("content").join(format!(
                "{}.utf8",
                payload["content"]["value"].as_str().unwrap()
            )),
            bytes,
        )
        .unwrap();
        let mut tuple: Value = serde_json::from_str(
            entry["body"]["supplyRecord"]["ref"]
                .as_str()
                .unwrap()
                .strip_prefix("role-run:v1:")
                .unwrap(),
        )
        .unwrap();
        tuple[2] = payload;
        let mut body = entry["body"].clone();
        body["supplyRecord"]["ref"] = json!(format!("role-run:v1:{tuple}"));
        let mut pending = crate::records::supply::PendingRunEntry::new(
            "supplied_guidance",
            body,
            crate::util::now_rfc3339(),
        )
        .unwrap();
        let claim =
            crate::records::supply::append_run_entry(&peer.fixture.root, &run, &mut pending)
                .unwrap();
        let document = records_access_role_answer(&cap, &peer, &run, n);
        let item = records_access_role_item(&document, &claim);
        assert_eq!(item["quoted"], claim);
        assert_eq!(
            item["supplierReading"]["state"],
            if validator {
                "historical role metadata omitted"
            } else {
                "historical role metadata available"
            },
            "{item}"
        );
        for canary in [
            "RAW-GUIDANCE-PRIVACY-CANARY",
            "HIDDEN-LIBRARY-CONTEXT-CANARY",
            "PRIVATE-VALIDATOR-CANARY",
        ] {
            assert!(!document.to_string().contains(canary));
        }
        assert!(
            item["supplierReading"]["limits"]
                .as_array()
                .unwrap()
                .iter()
                .any(|c| c == "wr-check-omitted")
        );
    }
}
#[test]
fn records_access_role_role_log_substitution_during_read_is_unavailable() {
    let _store = RoleR3Store::new();
    let peer = Peer::new();
    let thread = role_r3_start(&peer, &role_r3_composition(None, false));
    let mut root = peer.registered();
    let run = role_r3_open(&peer, &mut root, &thread);
    let entry = role_r3_entry(&peer, &run);
    let path = records_access_role_dir(&peer).join("observations.jsonl");
    let raw = std::fs::read(&path).unwrap();
    crate::role_observations::METADATA_BEFORE_READ.with(|h| {
        *h.borrow_mut() = Some(Box::new(move || {
            std::fs::rename(&path, path.with_extension("old")).unwrap();
            std::fs::write(path, raw).unwrap();
        }))
    });
    let cap = crate::records_access::RecordsCapability::new(&peer.fixture.root).unwrap();
    records_access_role_omitted(&cap, &peer, &run, &entry, 1, "role-source-unavailable");
}
#[test]
fn records_access_role_original_large_r3_stub_never_reads_its_references_or_changes_cursor() {
    let store = RoleR3Store::new();
    let peer = Peer::new();
    let thread = role_r3_start(&peer, &role_r3_composition(None, false));
    let mut root = peer.registered();
    let run = role_r3_open(&peer, &mut root, &thread);
    let mut entry = role_r3_entry(&peer, &run);
    entry["body"]["supplyRecord"]["ref"] =
        json!("x".repeat(crate::records_access::ENTRY_LIMIT + 1));
    let cap = records_access_role_snapshot_cap(&peer, vec![entry.clone(), entry.clone()], &store.0);
    let mut call = records_access_role_call(1, &run);
    call.arguments["limit"] = json!(1);
    let reply = cap.answer(&call, peer.fixture.root.to_str());
    let document: Value =
        serde_json::from_str(reply["contentItems"][0]["text"].as_str().unwrap()).unwrap();
    assert_eq!(document["next"], "o:1");
    let item = &document["items"][0];
    assert_eq!(item["quoted"]["recordId"], entry["recordId"]);
    assert!(item["quoted"]["omitted"].is_string());
    assert!(item.get("supplierReading").is_none());
}
#[test]
fn records_access_role_companion_page_overflow_preserves_all_originals_and_next() {
    use crate::records_access::RecordsSource;
    let store = RoleR3Store::new();
    let peer = Peer::new();
    let thread = role_r3_start(&peer, &role_r3_composition(None, false));
    let mut root = peer.registered();
    let run = role_r3_open(&peer, &mut root, &thread);
    let entry = role_r3_entry(&peer, &run);
    // Invented additional quoted R3/context claims, not native receipts. A
    // longer native-shaped identity exercises the companion's page budget;
    // its file provenance remains explicitly unverified, never native authority.
    let mut context: Value =
        serde_json::from_slice(&std::fs::read(records_access_role_context(&entry, &peer)).unwrap())
            .unwrap();
    context["nativeTurn"] = json!(format!("turn:{}", "x".repeat(450)));
    let bytes = serde_json::to_vec(&context).unwrap();
    let reference = json!({"content":crate::role_supply::content(&bytes),"byteLength":bytes.len()});
    std::fs::write(
        records_access_role_dir(&peer).join("content").join(format!(
            "{}.utf8",
            reference["content"]["value"].as_str().unwrap()
        )),
        bytes,
    )
    .unwrap();
    let mut tuple: Value = serde_json::from_str(
        entry["body"]["supplyRecord"]["ref"]
            .as_str()
            .unwrap()
            .strip_prefix("role-run:v1:")
            .unwrap(),
    )
    .unwrap();
    tuple[2] = reference;
    let mut body = entry["body"].clone();
    body["supplyRecord"]["ref"] = json!(format!("role-run:v1:{tuple}"));
    for _ in 0..30 {
        let mut pending = crate::records::supply::PendingRunEntry::new(
            "supplied_guidance",
            body.clone(),
            crate::util::now_rfc3339(),
        )
        .unwrap();
        crate::records::supply::append_run_entry(&peer.fixture.root, &run, &mut pending).unwrap();
    }
    struct Limited(crate::records_access::Corpus);
    impl RecordsSource for Limited {
        fn read(&self) -> crate::records_access::Corpus {
            crate::records_access::Corpus {
                entries: self.0.entries.clone(),
                limits: vec!["invented incomplete source qualification".into()],
            }
        }
    }
    let corpus = crate::records_access::ProjectPaths::new(&peer.fixture.root).read();
    assert!(corpus.limits.is_empty());
    let baseline = crate::records_access::RecordsCapability::with_source(
        &peer.fixture.root,
        Box::new(Limited(corpus)),
        store.0.join("baseline-page-reads.jsonl"),
    )
    .unwrap();
    let actual = crate::records_access::RecordsCapability::new(&peer.fixture.root).unwrap();
    let response = |cap: &crate::records_access::RecordsCapability, n| {
        let mut call = records_access_role_call(n, &run);
        call.arguments["cursor"] = json!("o:1");
        let reply = cap.answer(&call, peer.fixture.root.to_str());
        assert_eq!(reply["success"], true);
        serde_json::from_str::<Value>(reply["contentItems"][0]["text"].as_str().unwrap()).unwrap()
    };
    let baseline = response(&baseline, 1);
    let document = response(&actual, 2);
    assert_eq!(document["next"], baseline["next"]);
    assert!(document["next"].is_string());
    assert_eq!(
        document["items"].as_array().unwrap().len(),
        baseline["items"].as_array().unwrap().len()
    );
    let strip = |v: &Value| {
        let mut v = v.clone();
        for item in v["items"].as_array_mut().unwrap() {
            item.as_object_mut().unwrap().remove("supplierReading");
        }
        v["items"].clone()
    };
    assert_eq!(
        strip(&document),
        strip(&baseline),
        "companion bounds never change original representation or position"
    );
    assert!(document.to_string().len() <= crate::records_access::RESPONSE_LIMIT);
    assert!(
        document["items"]
            .as_array()
            .unwrap()
            .iter()
            .any(|i| i["supplierReading"]["limits"]
                .as_array()
                .is_some_and(|l| l.iter().any(|c| c == "role-companion-page-budget-omitted"))),
        "actual page budget should be reached by the controlled large companions"
    );
}
