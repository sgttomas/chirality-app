// Included beside role_r3_run_tests.rs in workflow_root_tests. This is an
// invented fake-peer journey through actual native producers and cold readers;
// it is not the separate week-later host reconstruction witness.
struct PortableReconstructionCleanup(Vec<PathBuf>);
impl Drop for PortableReconstructionCleanup {
    fn drop(&mut self) {
        for path in &self.0 {
            let _ = std::fs::remove_dir_all(path);
        }
    }
}
fn portable_reconstruction_choose_store(path: &std::path::Path) {
    crate::records_store::use_store_for_test(Some(Ok(crate::records_store::Store {
        root: path.into(),
        placement: crate::records_store::Placement::Test,
        limits: vec![],
    })));
}
fn portable_reconstruction_page(
    capability: &crate::records_access::RecordsCapability,
    project: &std::path::Path,
    arguments: Value,
    call: &mut u64,
) -> Value {
    *call += 1;
    let request = crate::records_access::Call {
        app_session: "invented-cold-reader".into(),
        generation: "invented-reader-generation".into(),
        request: json!(*call),
        thread: "invented-reader-thread".into(),
        turn: "invented-reader-turn".into(),
        call: format!("portable-reconstruction-{call}"),
        arguments,
    };
    let reply = capability.answer(&request, Some(project.to_str().unwrap()));
    assert_eq!(reply["success"], true, "{reply}");
    let text = reply["contentItems"][0]["text"].as_str().unwrap();
    assert!(text.len() <= 32 * 1024);
    let document: Value = serde_json::from_str(text).unwrap();
    assert!(document["standing"]
        .as_str()
        .unwrap()
        .contains("Quoted evidence"));
    let log = capability.snapshot()["readLog"]
        .as_str()
        .unwrap()
        .to_owned();
    let accounted: Value = serde_json::from_str(
        std::fs::read_to_string(log)
            .unwrap()
            .lines()
            .last()
            .unwrap(),
    )
    .unwrap();
    assert_eq!(accounted["returned"]["bytes"], text.len());
    assert_eq!(
        accounted["returned"]["content"]["value"],
        crate::util::sha256_hex(text.as_bytes())
    );
    document
}

#[test]
fn records_store_portable_reconstruction_cold_consumers_keep_role_wr_decision_and_unknown_sources() {
    for (moved_root, lost_link) in [(false, false), (true, false), (true, true)] {
        let source_store = RoleR3Store::new();
        let base = std::env::temp_dir()
            .canonicalize()
            .unwrap()
            .join(crate::util::opaque_id("portable-reconstruction-").unwrap());
        std::fs::create_dir(&base).unwrap();
        let mut peer = Peer::new();
        let original_project = peer.fixture.root.clone();
        let moved_project = base.join("moved-project");
        let _cleanup = PortableReconstructionCleanup(vec![original_project.clone(), base.clone()]);
        let composition = role_r3_composition(Some(crate::role_supply::Role::HELP_HUMAN), true);
        let thread = role_r3_start(&peer, &composition);
        let home_reference = peer.generation["home"].as_str().unwrap().to_owned();
        let mut live_root = peer.registered();
        let run = role_r3_open(&peer, &mut live_root, &thread);
        let role_entry = role_r3_entry(&peer, &run);
        // The native check requires this exact original conversation selected
        // with its turns loaded; Peer::select_history hardcodes "thread".
        let list = peer
            .home
            .history
            .lock()
            .unwrap()
            .history_mut()
            .unwrap()
            .list_threads(None, crate::native_history::Direction::Asc)
            .unwrap();
        peer.receive(list);
        peer.home
            .history
            .lock()
            .unwrap()
            .history_mut()
            .unwrap()
            .select(&thread)
            .unwrap();
        let turns = peer
            .home
            .history
            .lock()
            .unwrap()
            .history_mut()
            .unwrap()
            .turns_page(None, crate::native_history::Direction::Asc)
            .unwrap();
        peer.receive(turns);
        let checked = live_root.runs[&run]
            .lock()
            .unwrap()
            .check_native_supply()
            .unwrap();
        assert_eq!(checked["check"]["state"], "verified", "{checked}");
        let missing = crate::records::append_project(
            &original_project,
            Some(&run),
            "invented-portable-evidence-observer",
            "evidence_limit",
            &crate::records::APP_WRITER,
            json!({"label":"missing receipt","subjectRef":"invented:unavailable-host-receipt",
                "detail":"Host outcome unobserved; source resolution supplies no success."}),
        )
        .unwrap();
        live_root.runs[&run]
            .lock()
            .unwrap()
            .end_run(None, None)
            .unwrap();

        // One ordinary native A16 gives the decision reader a content-bound
        // source claim; the test never converts it into professional reliance.
        std::fs::create_dir_all(original_project.join("project/decisions")).unwrap();
        let decision = original_project.join("project/decisions/PKG-1.json");
        std::fs::copy(
            std::path::Path::new(env!("CARGO_MANIFEST_DIR"))
                .join("../tests/fixtures/FX-DP1/project/decisions/PKG-1.json"),
            &decision,
        )
        .unwrap();
        let decision_bytes = std::fs::read(&decision).unwrap();
        let actor = crate::act_control::person(
            Some("Invented portable reader fixture"),
            Some("fixture-account"),
        );
        let observed = json!({"fixture":"owned fake-peer and native confirmation doubles; no live person/provider"});
        let request = crate::recorder::identify_packages(&original_project)
            .unwrap()
            .remove(0);
        let mut control = crate::act_control::ActControl::new(&original_project);
        let offer = control
            .compose_a16(request["recordId"].as_str().unwrap())
            .unwrap();
        let offer_id = offer["offerId"].as_str().unwrap();
        control
            .confirmation_text(offer_id, "ALT-2", &actor)
            .unwrap();
        control.present(offer_id).unwrap();
        let performed = control
            .confirm(
                offer_id,
                "ALT-2",
                crate::act_control::InputSource::HostNativeConfirmation,
                actor.clone(),
            )
            .unwrap();
        assert_eq!(performed["state"], "AC-7 recorded");
        let source_entries = peer.fixture.rs_entries();
        let workflow_entry = source_entries
            .iter()
            .find(|entry| {
                entry["runId"] == run
                    && entry["kind"] == "supplied_guidance"
                    && entry["body"]["supplyForm"] == "workflow run start (turn text)"
            })
            .unwrap()
            .clone();
        let source_ids: std::collections::BTreeSet<_> = source_entries
            .iter()
            .map(|entry| entry["recordId"].as_str().unwrap().to_owned())
            .collect();
        let run_ids: Vec<_> = source_entries
            .iter()
            .filter(|entry| entry["runId"] == run)
            .map(|entry| entry["recordId"].as_str().unwrap().to_owned())
            .collect();
        let source_attachment = crate::records_store::attach(&original_project, false).unwrap();
        let project_id = source_attachment.project.unwrap();
        let source_dir = source_attachment.dir.unwrap();
        drop(control);
        drop(live_root);
        peer.home
            .host
            .stop(
                "portable records fixture settled",
                "no live state crosses export",
            )
            .unwrap();
        // Transfer ownership of the already-produced project out of Fixture's
        // cleanup, then drop the original Host/history/registered-run owners.
        peer.fixture.root = base.join("retired-fixture-cleanup");
        drop(peer);
        let project = if moved_root {
            std::fs::rename(&original_project, &moved_project).unwrap();
            crate::records_store::adopt(&moved_project).unwrap();
            moved_project.clone()
        } else {
            original_project.clone()
        };
        let source_payload = crate::records_package::payload_inventory(&source_dir).unwrap();
        let exported = base.join("exported-records");
        crate::records_export::export(&project, &exported).unwrap();
        let export_identity = std::fs::read(exported.join("tagmanifest-sha256.txt")).unwrap();

        let destination = base.join("destination-store");
        portable_reconstruction_choose_store(&destination);
        let unused_startup = if lost_link {
            // Actual startup sees a project with a lost link and mints Q.
            // Restoration must select source P without rewriting Q's ledger.
            std::fs::remove_file(project.join(crate::records_store::PROJECT_LINK)).unwrap();
            let startup = crate::records_store::attach(&project, true).unwrap();
            let unused_id = startup.project.unwrap();
            assert_ne!(unused_id, project_id);
            let unused_dir = startup.dir.unwrap();
            let bytes = std::fs::read(unused_dir.join("project.json")).unwrap();
            let payload = crate::records_package::payload_inventory(&unused_dir).unwrap();
            assert_eq!(payload.len(), 1, "startup Q must remain provably unused");
            Some((unused_dir, bytes, payload))
        } else {
            None
        };
        let plan = if lost_link {
            crate::records_store::package::prepare_restore(&project, &exported, &actor, &observed)
        } else {
            crate::records_store::package::prepare(&project, &exported, &actor, &observed)
        }
        .unwrap();
        let imported = crate::records_store::package::apply(plan, &actor, &observed).unwrap();
        assert_eq!(imported["projectId"], project_id);
        if let Some((unused_dir, bytes, payload)) = &unused_startup {
            assert_eq!(
                std::fs::read(unused_dir.join("project.json")).unwrap(),
                *bytes
            );
            assert_eq!(
                crate::records_package::payload_inventory(unused_dir).unwrap(),
                *payload
            );
            let link: Value = serde_json::from_slice(
                &std::fs::read(project.join(crate::records_store::PROJECT_LINK)).unwrap(),
            )
            .unwrap();
            assert_eq!(link["projectId"], project_id);
        }
        let destination_dir = crate::records_store::attach(&project, false)
            .unwrap()
            .dir
            .unwrap();
        let preserved = crate::records_package::payload_inventory(&destination_dir).unwrap();
        for (path, member) in &source_payload {
            assert_eq!(preserved.get(path), Some(member), "{path}");
        }
        let empty_history = HistorySession::default();
        assert_eq!(
            empty_history.role(&home_reference, &thread)["standing"],
            "unknown"
        );
        assert!(WorkflowRootSession::default().runs.is_empty());

        let cold_project =
            crate::workflow_workspace::publication::ProjectRecords::open(&project).unwrap();
        let quoted = crate::role_observations::read_r3(&project, &role_entry);
        assert_eq!(
            quoted["state"], "quoted historical correspondence",
            "{quoted}"
        );
        assert_eq!(quoted["sourceBytes"]["composed"], composition.text);
        assert_eq!(quoted["adoption"], "unknown");
        assert_eq!(quoted["currentRoleAuthorityRestored"], false);
        assert!(quoted["limitAccount"]["limits"]
            .as_array()
            .unwrap()
            .iter()
            .all(|limit| limit["standing"] == "unknown"));
        let correspondence =
            crate::records::supply::read_correspondence(&cold_project, &workflow_entry);
        assert_eq!(
            correspondence.standing,
            crate::records::supply::ReadStanding::HistoricalCorrespondence,
            "{correspondence:?}"
        );
        let supply = crate::records::supply::read_project_supply(&cold_project);
        assert!(supply["standing"]
            .as_str()
            .unwrap()
            .contains("no live native witness"));
        assert!(supply["records"]
            .as_array()
            .unwrap()
            .iter()
            .any(|record| record["kind"] == "supply_check"
                && record["r3"].as_array().is_some_and(|entries| entries
                    .iter()
                    .any(|entry| entry["recordId"] == workflow_entry["recordId"]
                        && entry["standing"] == "HistoricalCorrespondence"))));
        let lifecycle = crate::records::supply::read_project_runs(&cold_project, &[]).view();
        assert!(
            lifecycle["limits"].as_array().unwrap().is_empty(),
            "{lifecycle}"
        );
        let recorded_run = lifecycle["runs"]
            .as_array()
            .unwrap()
            .iter()
            .find(|entry| entry["run"] == run)
            .unwrap();
        assert_eq!(recorded_run["state"], "ended");
        assert_eq!(recorded_run["conversation"], thread);
        let mut cold_root = WorkflowRootSession::default();
        let reopened = cold_root.reopen(&project, &[]).unwrap();
        assert_eq!(reopened["runs"], lifecycle["runs"]);
        assert!(
            cold_root.runs.is_empty(),
            "cold display restores no live run owner"
        );

        let capability = crate::records_access::RecordsCapability::new(&project).unwrap();
        let mut call = 0;
        let listing = portable_reconstruction_page(
            &capability,
            &project,
            json!({"operation":"list_runs","limit":1}),
            &mut call,
        );
        assert!(listing["items"]
            .as_array()
            .unwrap()
            .iter()
            .any(|item| item["run"]["runId"] == run));
        let mut cursor = None;
        let mut read_ids = Vec::new();
        let mut role_companions = 0;
        let mut missing_returned = false;
        loop {
            let mut arguments = json!({"operation":"read_run","run":run,"limit":1});
            if let Some(value) = cursor {
                arguments["cursor"] = value;
            }
            let page = portable_reconstruction_page(&capability, &project, arguments, &mut call);
            assert!(page["limits"].as_array().unwrap().is_empty(), "{page}");
            for item in page["items"].as_array().unwrap() {
                let id = item["quoted"]["recordId"].as_str().unwrap().to_owned();
                assert!(item["source"]["log"]
                    .as_str()
                    .unwrap()
                    .starts_with("records-store:"));
                assert!(item["source"]["line"].as_u64().unwrap() > 0);
                if item["quoted"]["recordId"] == role_entry["recordId"] {
                    assert_eq!(item["quoted"], role_entry);
                    let reading = &item["supplierReading"];
                    assert_eq!(
                        reading["state"], "historical role metadata available",
                        "{reading}"
                    );
                    assert_eq!(reading["currentRoleAuthorityRestored"], false);
                    assert_eq!(reading["adoption"], "unknown");
                    assert!(reading["limits"]
                        .as_array()
                        .unwrap()
                        .iter()
                        .any(|limit| limit == "wr-check-omitted"));
                    assert!(!reading.to_string().contains(&composition.text));
                    role_companions += 1;
                }
                if item["quoted"]["recordId"] == missing["recordId"] {
                    assert_eq!(item["quoted"]["body"], missing["body"]);
                    missing_returned = true;
                }
                if item["quoted"]["recordId"] == workflow_entry["recordId"] {
                    assert!(
                        item.get("supplierReading").is_none(),
                        "role-only capability metadata scope remains intact"
                    );
                    assert_eq!(item["quoted"]["body"]["supplyCheck"], "verified");
                    assert_eq!(item["quoted"]["body"]["adoption"], "unknown");
                }
                read_ids.push(id);
            }
            cursor = page["next"].as_str().map(|next| json!(next));
            if cursor.is_none() {
                break;
            }
            assert!(
                call < 100,
                "pagination must advance over this bounded fixture"
            );
        }
        assert_eq!(read_ids, run_ids);
        assert_eq!(role_companions, 1);
        assert!(missing_returned);
        let acts = portable_reconstruction_page(
            &capability,
            &project,
            json!({"operation":"read_acts","limit":50}),
            &mut call,
        );
        assert!(acts["items"]
            .as_array()
            .unwrap()
            .iter()
            .any(|item| item["quoted"]["recordId"] == performed["record"]["recordId"]));

        let original_decision = crate::runtime_session::read_decision_packages(&project);
        let projection = &original_decision["rows"][0]["decision"];
        assert_eq!(projection["act"], performed["record"]["recordId"]);
        assert_eq!(projection["lapse"], "not lapsed");
        assert!(projection["captureProvenance"]
            .as_str()
            .unwrap()
            .contains("not verified"));
        let decision = project.join("project/decisions/PKG-1.json");
        let mut edited: Value = serde_json::from_slice(&decision_bytes).unwrap();
        edited["purpose"] = json!(
            "Changed local content after import; original decision remains bound to prior bytes"
        );
        std::fs::write(&decision, serde_json::to_vec_pretty(&edited).unwrap()).unwrap();
        let changed = crate::runtime_session::read_decision_packages(&project);
        assert_eq!(
            changed["rows"][0]["decision"]["act"],
            performed["record"]["recordId"]
        );
        assert_eq!(
            changed["rows"][0]["decision"]["lapse"],
            "lapsed — the package changed after the decision"
        );
        std::fs::write(&decision, &decision_bytes).unwrap();

        let (after, limits) = crate::storage::read_all(&project);
        assert!(limits.is_empty(), "{limits:?}");
        assert_eq!(
            after
                .iter()
                .map(|entry| entry["recordId"].as_str().unwrap().to_owned())
                .collect::<std::collections::BTreeSet<_>>(),
            source_ids
        );
        assert_eq!(
            crate::records_package::payload_inventory(&source_dir).unwrap(),
            source_payload
        );
        assert_eq!(
            std::fs::read(exported.join("tagmanifest-sha256.txt")).unwrap(),
            export_identity
        );
        let current = crate::records_package::payload_inventory(&destination_dir).unwrap();
        for (path, member) in &source_payload {
            assert_eq!(current.get(path), Some(member), "reader rewrote {path}");
        }
        assert!(crate::records_export::verify(&exported).is_ok());
        if let Some((unused_dir, bytes, payload)) = &unused_startup {
            assert_eq!(
                std::fs::read(unused_dir.join("project.json")).unwrap(),
                *bytes
            );
            assert_eq!(
                crate::records_package::payload_inventory(unused_dir).unwrap(),
                *payload,
                "cold consumers must stay associated with restored P rather than startup Q"
            );
        }
        assert!(source_store.0.is_dir());
    }
}
