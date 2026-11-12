//! Invented records exercise the actual selected-workspace native read path.
use super::*;
use crate::{records_store, util};
use std::path::PathBuf;

struct Fixture {
    root: PathBuf,
    project: PathBuf,
    graph: Value,
    log: Vec<Value>,
}
impl Fixture {
    fn new() -> Self {
        Self::with_store(true)
    }
    /// The store is given but the App's start has not created it, so no
    /// records store exists until a writer creates one.
    fn not_started() -> Self {
        Self::with_store(false)
    }
    fn with_store(started: bool) -> Self {
        let root = std::env::temp_dir()
            .canonicalize()
            .unwrap()
            .join(util::opaque_id("fleet-views-").unwrap());
        let project = root.join("project");
        std::fs::create_dir_all(&project).unwrap();
        let store = Some(Ok(records_store::Store {
            root: root.join("store"),
            placement: records_store::Placement::Test,
            limits: vec![],
        }));
        if started {
            records_store::use_store_for_test(store);
        } else {
            records_store::use_store_not_started_for_test(store);
            records_store::restore_configured_for_test(records_store::configured_for_test());
        }
        let graph = record(
            "work_graph",
            "fl:graph",
            json!({"revision":1,"projectDagRef":"none (invented)","items":[
                item("W1",vec![]),item("W2",vec![json!({"kind":"item","ref":"W1"})]),
                item("W3",vec![json!({"kind":"input","ref":"inputs/style.txt"})]),
                item("W4",vec![json!({"kind":"decision","ref":"rec:request"})])
            ]}),
        );
        let mut f = Self {
            root,
            project,
            graph,
            log: vec![],
        };
        f.select();
        f
    }
    fn put(&self, relative: &str, bytes: &[u8]) {
        let p = self.project.join(FOLDER).join(relative);
        std::fs::create_dir_all(p.parent().unwrap()).unwrap();
        std::fs::write(p, bytes).unwrap();
    }
    fn select(&mut self) {
        let bytes = serde_json::to_vec_pretty(&self.graph).unwrap();
        self.put("graphs/U/r1.json", &bytes);
        self.log.retain(|r| r["kind"] != "current_graph");
        self.log.insert(0,record("current_graph","fl:selector",json!({"graph":"fl:graph","graphContent":{"method":util::FILE_IDENTITY_METHOD,"value":util::sha256_hex(&bytes)}})));
    }
    fn flush(&self) {
        let mut bytes = Vec::new();
        for r in &self.log {
            super::super::validator().unwrap().validate(r).unwrap();
            bytes.extend(serde_json::to_vec(r).unwrap());
            bytes.push(b'\n');
        }
        self.put("coordination.fleet.jsonl", &bytes);
    }
    fn read(&self) -> Value {
        self.read_packet()["workspace"].clone()
    }
    fn read_packet(&self) -> Value {
        self.flush();
        let inventory = super::super::tests::inventory(&self.root);
        let packet = crate::read_fleet_records_for_workspace(Some(&self.project)).unwrap();
        assert_eq!(
            super::super::tests::inventory(&self.root),
            inventory,
            "the selected-workspace read writes no record, identity, lock or cache"
        );
        packet
    }
    fn ret(&mut self, id: &str, item: &str) {
        self.log.push(record("return_recorded",id,json!({"workItem":item,"returnedBy":who("executor","agent"),"returned":[{"kind":"file","ref":"result.txt"}],"evidence":[{"kind":"file","ref":"result.txt"}]})));
    }
    fn integrate(&mut self, id: &str, item: &str, ret: &str) {
        self.log.push(record("integration_recorded",id,json!({"workItem":item,"returnRef":ret,"integrator":who("manager","agent"),"evidence":[{"kind":"commit","ref":"invented commit"}]})));
    }
}
impl Drop for Fixture {
    fn drop(&mut self) {
        records_store::use_store_for_test(None);
        let _ = std::fs::remove_dir_all(&self.root);
    }
}
fn who(identity: &str, kind: &str) -> Value {
    json!({"kind":kind,"identity":identity,"role":"WORKING_ITEMS"})
}
fn record(kind: &str, id: &str, body: Value) -> Value {
    json!({"format":"chirality.fleet.record","formatVersion":"0.1","kind":kind,"recordId":id,"undertaking":"U","recorder":who("manager","agent"),"writtenAt":"invented time","body":body})
}
fn item(id: &str, needs: Vec<Value>) -> Value {
    json!({"itemId":id,"outcome":format!("Outcome {id}"),"owner":who("executor","agent"),"selected":true,"needs":needs,"next":"review the result"})
}
fn view(workspace: &Value) -> &Value {
    &workspace["undertakings"][0]
}
fn work<'a>(v: &'a Value, id: &str) -> &'a Value {
    v["waiting"]
        .as_array()
        .unwrap()
        .iter()
        .find(|r| r["item"] == id)
        .unwrap()
}
fn brief(id: &str, preparer: &str) -> Value {
    let mut value: Value = serde_json::from_str(include_str!(
        "../../tests/fixtures/FX-FL1/briefs/W1.json"
    ))
    .unwrap();
    value["recordId"] = json!(format!("fl:{id}"));
    value["undertaking"] = json!("U");
    value["body"]["briefId"] = json!(id);
    value["body"]["preparedBy"] = who(preparer, "agent");
    value
}
fn queued<'a>(packet: &'a Value, reference: &str) -> &'a Value {
    view(&packet["workspace"])["queue"]
        .as_array()
        .unwrap()
        .iter()
        .find(|r| r["returnRef"] == reference)
        .unwrap()
}

#[test]
fn fleet_views_native_adapter_examination_attribution_tracks_selected_brief_source() {
    let mut f = Fixture::new();
    f.put(
        "briefs/original.json",
        &serde_json::to_vec(&brief("brief:original", "original preparer")).unwrap(),
    );
    f.put(
        "briefs/replacement.json",
        &serde_json::to_vec(&brief("brief:replacement", "current preparer")).unwrap(),
    );
    f.graph["body"]["items"][0]["brief"] = json!("brief:original");
    f.select();
    f.ret("fl:named-return", "W1");
    f.log.last_mut().unwrap()["body"]["brief"] = json!("brief:original");
    f.ret("fl:optional-return", "W1");
    let before = f.read_packet();
    assert_eq!(queued(&before, "fl:named-return")["examines"], "original preparer (prepared the brief)");
    assert_eq!(queued(&before, "fl:optional-return")["examines"], "original preparer (prepared the brief)");

    // A real new revision and selector change the graph route, not the
    // return's explicit brief reference. Both brief files remain readable.
    let mut next = f.graph.clone();
    next["recordId"] = json!("fl:graph-next");
    next["body"]["revision"] = json!(2);
    next["body"]["supersedes"] = json!("fl:graph");
    next["body"]["items"][0]["brief"] = json!("brief:replacement");
    let bytes = serde_json::to_vec_pretty(&next).unwrap();
    f.put("graphs/U/r2.json", &bytes);
    f.log.push(record("current_graph", "fl:selector-next", json!({
        "graph":"fl:graph-next","graphContent":{"method":util::FILE_IDENTITY_METHOD,"value":util::sha256_hex(&bytes)}
    })));
    let after = f.read_packet();
    let named = queued(&after, "fl:named-return");
    let optional = queued(&after, "fl:optional-return");
    assert_eq!(named["examines"], queued(&before, "fl:named-return")["examines"]);
    assert_eq!(named["examinesProvenance"], queued(&before, "fl:named-return")["examinesProvenance"]);
    assert_eq!(named["examinesProvenance"]["basis"], "return-brief");
    assert_eq!(named["examinesProvenance"]["briefId"], "brief:original");
    assert_eq!(named["examinesProvenance"]["referenceSource"]["recordId"], "fl:named-return");
    assert_eq!(named["examinesProvenance"]["briefSource"]["recordId"], "fl:brief:original");
    assert_eq!(optional["examines"], "current preparer (prepared the brief)");
    assert_eq!(optional["examinesProvenance"]["basis"], "current-graph-brief");
    assert_eq!(optional["examinesProvenance"]["briefId"], "brief:replacement");
    assert_eq!(optional["examinesProvenance"]["referenceSource"]["recordId"], "fl:graph-next");
    assert_eq!(optional["examinesProvenance"]["briefSource"]["recordId"], "fl:brief:replacement");
    assert_eq!(named["state"], "awaiting review");
    assert_eq!(optional["state"], "awaiting review");
    assert!(optional["examiner"].is_null());
    assert!(f.log.iter().find(|r| r["recordId"] == "fl:optional-return").unwrap()["body"].get("brief").is_none());
    println!("FLEET_ATTRIBUTION_DTO:{}", json!({"before":before,"after":after}));
}

#[test]
fn fleet_views_native_adapter_examination_attribution_unresolved_sources_keep_limits() {
    let mut cases = serde_json::Map::new();
    for case in ["missing", "invalid", "conflicting", "duplicate", "other-item", "other-undertaking", "no-graph-brief", "duplicate-no-graph-brief"] {
        let mut f = Fixture::new();
        f.graph["body"]["items"][0]["brief"] = json!("brief:current");
        f.select();
        f.put("briefs/current.json", &serde_json::to_vec(&brief("brief:current", "current preparer")).unwrap());
        let mut named = brief("brief:named", "named preparer");
        match case {
            "invalid" => { named["body"].as_object_mut().unwrap().remove("preparedBy"); }
            "other-item" => named["body"]["workItem"] = json!("W2"),
            "other-undertaking" => named["undertaking"] = json!("another"),
            "conflicting" | "duplicate" | "duplicate-no-graph-brief" => {
                let mut conflict = named.clone();
                if case == "conflicting" { conflict["recordId"] = json!("fl:other-brief-record"); }
                conflict["body"]["preparedBy"] = who("conflicting preparer", "agent");
                f.put("briefs/conflict.json", &serde_json::to_vec(&conflict).unwrap());
            }
            "no-graph-brief" => {
                f.graph["body"]["items"][0].as_object_mut().unwrap().remove("brief");
                f.select();
            }
            _ => {}
        }
        if case == "duplicate-no-graph-brief" {
            f.graph["body"]["items"][0].as_object_mut().unwrap().remove("brief");
            f.select();
        }
        if case != "missing" { f.put("briefs/named.json", &serde_json::to_vec(&named).unwrap()); }
        f.ret("fl:named-return", "W1");
        f.log.last_mut().unwrap()["body"]["brief"] = json!("brief:named");
        f.ret("fl:optional-return", "W1");
        let packet = f.read_packet();
        let named = queued(&packet, "fl:named-return");
        let optional = queued(&packet, "fl:optional-return");
        assert_eq!(named["examinesProvenance"]["basis"], "return-brief");
        assert_eq!(named["examinesProvenance"]["briefId"], "brief:named");
        assert_eq!(named["examinesProvenance"]["referenceSource"]["recordId"], "fl:named-return");
        assert_eq!(optional["examinesProvenance"]["basis"], "current-graph-brief");
        if matches!(case, "no-graph-brief" | "duplicate-no-graph-brief") {
            assert_eq!(named["examines"], if case == "no-graph-brief" { "named preparer (prepared the brief)" } else { "examiner not established" });
            assert_eq!(optional["examines"], "examiner not established");
            assert!(optional["examinesProvenance"]["briefId"].is_null());
            assert!(optional["examinesProvenance"]["briefSource"].is_null());
        } else {
            assert_eq!(named["examines"], "examiner not established", "{case}: no current-graph or executor fallback");
            assert!(named["examinesProvenance"]["briefSource"].is_null());
            assert_eq!(optional["examines"], "current preparer (prepared the brief)");
            assert_eq!(optional["examinesProvenance"]["briefId"], "brief:current");
            assert_eq!(optional["examinesProvenance"]["briefSource"]["recordId"], "fl:brief:current");
        }
        if case == "invalid" { assert!(packet["limits"].to_string().contains("schema invalid")); }
        if matches!(case, "duplicate" | "duplicate-no-graph-brief") {
            assert!(packet["limits"].to_string().contains("duplicate/conflicting recordId"));
            assert_eq!(view(&packet["workspace"])["queueComplete"], false);
            assert_eq!(view(&packet["workspace"])["currentGraphEstablished"], false);
        }
        cases.insert(case.into(), packet);
    }
    println!("FLEET_ATTRIBUTION_LIMITS_DTO:{}", Value::Object(cases));
}

#[test]
fn fleet_views_native_adapter_preserves_return_review_integration_and_rebuild() {
    let mut f = Fixture::new();
    f.ret("fl:return", "W1");
    f.log.push(record("review_recorded","fl:review",json!({"workItem":"W1","returnRef":"fl:return","reviewer":who("independent reviewer","agent"),"verdict":"no blocking findings","findings":[]})));
    let before = f.read();
    let v = view(&before);
    assert_eq!(v["queue"][0]["state"], "reviewed — awaiting integration");
    assert_eq!(
        v["queue"][0]["examines"], "examiner not established",
        "executor is never invented as examiner"
    );
    assert_eq!(work(v, "W1")["category"], "returned");
    assert_eq!(work(v, "W2")["category"], "waiting");
    f.integrate("fl:integration", "W1", "fl:return");
    let after = f.read();
    let v = view(&after);
    assert_eq!(v["queue"], json!([]));
    assert_eq!(work(v, "W1")["category"], "done");
    assert_eq!(work(v, "W2")["category"], "ready");
    assert_eq!(
        work(v, "W4")["category"],
        "unknown",
        "a decision request is never satisfied from presence"
    );
    f.flush();
    let inventory = super::super::tests::inventory(&f.root);
    assert_eq!(
        crate::read_fleet_records_for_workspace(Some(&f.project)).unwrap()["workspace"],
        after
    );
    assert_eq!(
        super::super::tests::inventory(&f.root),
        inventory,
        "rebuild writes no source, identity, lock or cache"
    );
    println!("FLEET_WORKSPACE_DTO:{}", after);
    println!("FLEET_WORKSPACE_REVIEW_DTO:{}", before);
}

#[test]
fn fleet_views_keeps_each_unintegrated_return_and_newer_return_reopens_dependency() {
    let mut f = Fixture::new();
    f.ret("fl:first", "W1");
    f.ret("fl:second", "W1");
    assert_eq!(view(&f.read())["queue"].as_array().unwrap().len(), 2);
    f.integrate("fl:old-integrated", "W1", "fl:first");
    let w = f.read();
    let v = view(&w);
    assert_eq!(v["queue"].as_array().unwrap().len(), 1);
    assert_eq!(v["queue"][0]["returnRef"], "fl:second");
    assert_eq!(work(v, "W2")["category"], "waiting");
}

#[test]
fn fleet_views_return_survives_item_removal_from_current_graph() {
    let mut f = Fixture::new();
    f.ret("fl:pending-return", "W1");
    f.graph["body"]["items"]
        .as_array_mut()
        .unwrap()
        .retain(|i| i["itemId"] != "W1");
    f.select();
    let w = f.read();
    let v = view(&w);
    assert_eq!(v["queue"].as_array().unwrap().len(), 1);
    assert_eq!(v["queue"][0]["returnRef"], "fl:pending-return");
    assert_eq!(v["queue"][0]["inCurrentGraph"], false);
    assert_eq!(work(v, "W2")["category"], "unknown");
    f.integrate("fl:removed-integrated", "W1", "fl:pending-return");
    assert_eq!(view(&f.read())["queue"], json!([]));
}

#[test]
fn fleet_views_brief_owner_is_bound_to_the_same_item_and_undertaking() {
    let mut f = Fixture::new();
    let mut brief: Value = serde_json::from_str(include_str!(
        "../../tests/fixtures/FX-FL1/briefs/W1.json"
    ))
    .unwrap();
    brief["undertaking"] = json!("U");
    brief["body"]["workItem"] = json!("W2");
    f.put("briefs/W1.json", &serde_json::to_vec(&brief).unwrap());
    f.graph["body"]["items"][0]["brief"] = json!("brief:W1");
    f.select();
    assert_eq!(
        work(view(&f.read()), "W1")["category"],
        "unknown",
        "another item's brief cannot establish this assignment"
    );
    f.ret("fl:bounded-return", "W1");
    f.log.last_mut().unwrap()["body"]["brief"] = json!("brief:W1");
    assert_eq!(
        view(&f.read())["queue"][0]["examines"],
        "examiner not established"
    );
    brief["body"]["workItem"] = json!("W1");
    f.put("briefs/W1.json", &serde_json::to_vec(&brief).unwrap());
    let w = f.read();
    assert!(view(&w)["queue"][0]["examines"]
        .as_str()
        .unwrap()
        .contains("prepared the brief"));
}

#[test]
fn fleet_views_orphan_review_or_integration_never_restores_ready_or_done() {
    for kind in ["review_recorded", "integration_recorded"] {
        let mut f = Fixture::new();
        let body = if kind == "review_recorded" {
            json!({"workItem":"W1","returnRef":"fl:missing","reviewer":who("reviewer","agent"),"verdict":"no blocking findings","findings":[]})
        } else {
            json!({"workItem":"W1","returnRef":"fl:missing","integrator":who("manager","agent"),"evidence":[{"kind":"commit","ref":"invented"}]})
        };
        f.log.push(record(kind, "fl:orphan", body));
        let w = f.read();
        assert_eq!(work(view(&w), "W1")["category"], "unknown");
        assert_eq!(view(&w)["queueComplete"], false);
        f.ret("fl:missing", "W2");
        let w = f.read();
        assert_eq!(
            work(view(&w), "W1")["category"],
            "unknown",
            "same identity for another item's return is not a relation"
        );
    }
}

#[test]
fn fleet_views_same_id_changed_project_observation_has_no_exact_counterpart() {
    let mut f = Fixture::new();
    f.put("inputs/style.txt", b"style");
    let raw=include_str!("../../tests/fixtures/FX-FL1/coordination.fleet.jsonl");
    let mut dispatch: Value = raw
        .lines()
        .filter_map(|l| serde_json::from_str::<Value>(l).ok())
        .find(|r| r["kind"] == "dispatch_observed")
        .unwrap();
    dispatch["undertaking"] = json!("U");
    let dir = records_store::attach(&f.project, true)
        .unwrap()
        .dir
        .unwrap();
    std::fs::create_dir_all(dir.join("fleet")).unwrap();
    let mut original = serde_json::to_vec(&dispatch).unwrap();
    original.push(b'\n');
    std::fs::write(dir.join("fleet/coordination.fleet.jsonl"), &original).unwrap();
    dispatch["body"]["childThread"] = json!("changed-child-with-the-same-record-id");
    f.log.push(dispatch);
    let w = f.read();
    let v = view(&w);
    assert_eq!(v["queueComplete"], false);
    assert_eq!(work(v, "W3")["category"], "ready (qualified)");
    assert_eq!(work(v, "W3")["readinessQualified"], true);
}

#[test]
fn fleet_views_selector_matches_exact_bytes_and_never_falls_back() {
    let mut f = Fixture::new();
    assert_eq!(view(&f.read())["currentGraphEstablished"], true);
    let path = f.project.join(FOLDER).join("graphs/U/r1.json");
    let mut bytes = std::fs::read(&path).unwrap();
    bytes.push(b' ');
    std::fs::write(&path, &bytes).unwrap();
    assert!(
        view(&f.read())["graph"].is_null(),
        "even JSON-equivalent whitespace changes the bound bytes"
    );
    f.select();
    f.log.push(record("current_graph","fl:latest",json!({"graph":"fl:absent","graphContent":{"method":util::FILE_IDENTITY_METHOD,"value":"abc"}})));
    assert!(
        view(&f.read())["graph"].is_null(),
        "missing latest selector target cannot fall back"
    );
    f.log.pop();
    f.log[0]["body"]["graphContent"]["method"] =
        json!("file content identity (method unselected; TEST VALUE: sha-256 of the file bytes)");
    assert!(
        view(&f.read())["graph"].is_null(),
        "a prototype identity is never relabelled"
    );
}

#[test]
fn fleet_views_incomplete_log_suppresses_readiness_and_queue_completeness() {
    let mut f = Fixture::new();
    f.ret("fl:known-return", "W1");
    f.integrate("fl:known-integration", "W1", "fl:known-return");
    f.flush();
    use std::io::Write;
    let p = f.project.join(FOLDER).join("coordination.fleet.jsonl");
    std::fs::OpenOptions::new()
        .append(true)
        .open(p)
        .unwrap()
        .write_all(b"{\"kind\":")
        .unwrap();
    let w = crate::read_fleet_records_for_workspace(Some(&f.project)).unwrap()["workspace"].clone();
    let v = view(&w);
    assert_eq!(v["queueComplete"], false);
    assert_eq!(v["currentGraphEstablished"], false);
    assert_eq!(
        work(v, "W1")["category"],
        "done",
        "known recorded integration is retained"
    );
    for id in ["W2", "W3", "W4"] {
        assert_eq!(work(v, id)["category"], "unknown");
    }
}

#[test]
fn fleet_views_scopes_undertakings_and_refuses_duplicate_items_and_records() {
    let mut f = Fixture::new();
    let mut other = record(
        "external_result",
        "fl:other",
        json!({"workItem":"W1","owner":who("outside","external"),"result":[{"kind":"file","ref":"other.txt"}]}),
    );
    other["undertaking"] = json!("another");
    f.log.push(other);
    let w = f.read();
    let v = w["undertakings"]
        .as_array()
        .unwrap()
        .iter()
        .find(|v| v["undertaking"] == "U")
        .unwrap();
    assert_ne!(work(v, "W1")["category"], "done");
    let duplicate = f.graph["body"]["items"][0].clone();
    f.graph["body"]["items"]
        .as_array_mut()
        .unwrap()
        .push(duplicate);
    f.select();
    assert!(view(&f.read())["graph"].is_null());
}

#[test]
fn fleet_views_reads_inputs_without_following_links_or_escaping_fleet() {
    let mut f = Fixture::new();
    f.put("inputs/style.txt", b"style");
    assert_eq!(work(view(&f.read()), "W3")["category"], "ready");
    std::fs::remove_file(f.project.join(FOLDER).join("inputs/style.txt")).unwrap();
    std::os::unix::fs::symlink(
        "/etc/passwd",
        f.project.join(FOLDER).join("inputs/style.txt"),
    )
    .unwrap();
    assert_eq!(work(view(&f.read()), "W3")["category"], "unknown");
    f.graph["body"]["items"][2]["needs"][0]["ref"] = json!("../private");
    f.select();
    assert_eq!(work(view(&f.read()), "W3")["category"], "unknown");
    f.graph["body"]["items"][2]["needs"][0]["ref"] = json!("inputs/pipe");
    f.select();
    use std::os::unix::ffi::OsStrExt;
    let name = std::ffi::CString::new(
        f.project
            .join(FOLDER)
            .join("inputs/pipe")
            .as_os_str()
            .as_bytes(),
    )
    .unwrap();
    assert_eq!(unsafe { libc::mkfifo(name.as_ptr(), 0o600) }, 0);
    assert_eq!(
        work(view(&f.read()), "W3")["category"],
        "unknown",
        "special files fail without blocking"
    );
}

fn connector_record() -> Value {
    json!({"record_id":"receiving:invented","response_standing":{"connector":"domains","envelope":"adopted","condition":"current","claim_tier":"admitted","supports_reliance":true,"reasons":[{"facet":"envelope","value":"adopted","basis":"invented admitted fixture"}]},"claims":[],"route":{"needed":false}})
}
#[test]
fn fleet_views_connector_needs_preserve_standing_claim_gaps_and_routes() {
    let mut f = Fixture::new();
    f.graph["body"]["items"][2]["needs"][0] =
        json!({"kind":"connector","ref":"inputs/source.json","connector":"domains"});
    f.select();
    assert_eq!(work(view(&f.read()), "W3")["category"], "waiting");
    let mut source = connector_record();
    f.put("inputs/source.json", &serde_json::to_vec(&source).unwrap());
    assert_eq!(work(view(&f.read()), "W3")["category"], "ready");
    let mut claim = source["response_standing"].clone();
    claim["supports_reliance"] = json!(false);
    claim["condition"] = json!("unknown");
    source["claims"] = json!([{"claim_id":"c3","standing":claim}]);
    f.put("inputs/source.json", &serde_json::to_vec(&source).unwrap());
    assert_eq!(
        work(view(&f.read()), "W3")["category"],
        "unknown",
        "record-level reliance cannot hide an unrelied claim"
    );
    source["route"] = json!({"needed":true,"account_ref":"ra:source"});
    f.put("inputs/source.json", &serde_json::to_vec(&source).unwrap());
    let w = f.read();
    let row = work(view(&w), "W3");
    assert_eq!(row["category"], "ready");
    assert!(row.to_string().contains("c3"));
    assert!(row.to_string().contains("ra:source"));
    source["response_standing"]["condition"] = json!("stale");
    f.put("inputs/source.json", &serde_json::to_vec(&source).unwrap());
    assert_eq!(
        work(view(&f.read()), "W3")["category"],
        "unknown",
        "stale+claims reliance is nonconformant"
    );
    source = connector_record();
    source["response_standing"]["supports_reliance"] = json!(false);
    source["response_standing"]["condition"] = json!("stale");
    f.put("inputs/source.json", &serde_json::to_vec(&source).unwrap());
    assert_eq!(work(view(&f.read()), "W3")["category"], "waiting");
    f.graph["body"]["items"][2]["needs"][0] = json!({"kind":"input","ref":"inputs/source.json"});
    f.select();
    assert_eq!(
        work(view(&f.read()), "W3")["category"],
        "unknown",
        "connector presence is not ordinary input satisfaction"
    );
}

#[test]
fn fleet_views_forged_project_dispatch_does_not_promote_execution() {
    let mut f = Fixture::new();
    f.graph["body"]["items"][0]["brief"] = json!("brief:W1");
    f.select();
    let raw=include_str!("../../tests/fixtures/FX-FL1/coordination.fleet.jsonl");
    let mut dispatch: Value = raw
        .lines()
        .filter_map(|l| serde_json::from_str::<Value>(l).ok())
        .find(|r| r["kind"] == "dispatch_observed")
        .unwrap();
    dispatch["undertaking"] = json!("U");
    dispatch["body"]["association"]["brief"] = json!("brief:W1");
    f.log.push(dispatch);
    let w = f.read();
    let v = view(&w);
    assert_eq!(work(v, "W1")["category"], "unknown");
    assert_eq!(v["queue"], json!([]));
    assert_eq!(v["queueComplete"], false);
}

#[test]
fn fleet_views_changed_snapshot_has_no_usable_projection_and_census_cannot_rebase() {
    let f = Fixture::new();
    f.flush();
    let path = f.project.join(FOLDER).join("graphs/U/r1.json");
    let changed = path.clone();
    super::super::AFTER_READ.with(|h| {
        *h.borrow_mut() = Some(Box::new(move || {
            let mut b = std::fs::read(&changed).unwrap();
            b.push(b' ');
            std::fs::write(changed, b).unwrap();
        }))
    });
    let w = crate::read_fleet_records_for_workspace(Some(&f.project)).unwrap();
    assert!(view(&w["workspace"])["graph"].is_null());
    let mut census = Census::default();
    census.read(&path).unwrap();
    std::fs::write(&path, b"new bytes").unwrap();
    assert!(census.read(&path).is_err());
    assert!(census.unchanged().is_err());
}

#[test]
fn fleet_views_corrections_do_not_silently_choose_conflicting_returns() {
    let mut f = Fixture::new();
    f.ret("fl:first", "W1");
    f.ret("fl:correction", "W1");
    f.log.last_mut().unwrap()["corrects"] = json!("fl:first");
    f.log.last_mut().unwrap()["correctionReason"] = json!("correct returned file");
    let w = f.read();
    assert_eq!(view(&w)["queue"].as_array().unwrap().len(), 1);
    assert_eq!(view(&w)["queue"][0]["returnRef"], "fl:correction");
    f.ret("fl:competing", "W1");
    f.log.last_mut().unwrap()["corrects"] = json!("fl:first");
    f.log.last_mut().unwrap()["correctionReason"] = json!("competing correction");
    let w = f.read();
    assert_eq!(view(&w)["queueComplete"], false);
    assert_eq!(work(view(&w), "W1")["category"], "unknown");
}

// Decision needs (DEL-06-01 Need and AC-005; DEL-06-02 AC-002). A test cannot
// perform a person's confirmation. Each act record below is an invented claim,
// schema-checked and written to the store's act log the way the decision
// reader tests write theirs; it stands for the record of a person's act and
// shows only how a need reads such a record.
struct Decision {
    dir: PathBuf,
    package: PathBuf,
    act: Value,
}
fn decision_fixture(f: &Fixture) -> Decision {
    let dir = records_store::attach(&f.project, true).unwrap().dir.unwrap();
    let bytes = include_bytes!("../../tests/fixtures/FX-DP1/project/decisions/PKG-1.json");
    let package = f.project.join("decisions/PKG-1.json");
    std::fs::create_dir_all(package.parent().unwrap()).unwrap();
    std::fs::write(&package, bytes).unwrap();
    let entries: Vec<Value> = include_str!("../../tests/fixtures/FX-DP1/records/coordination.rs.jsonl")
        .lines()
        .map(|l| serde_json::from_str(l).unwrap())
        .collect();
    let mut request = entries[0].clone();
    request["recordId"] = json!("rec:request");
    request["recorder"]["identity"] = json!("writer:request");
    request["body"]["evidence"]["ref"] = json!("decisions/PKG-1.json");
    request["body"]["evidence"]["method"] = json!(util::FILE_IDENTITY_METHOD);
    request["body"]["evidence"]["claimedIdentity"] = json!(util::sha256_hex(bytes));
    let mut act = entries[2].clone();
    act["body"]["decisionActor"] = json!({"displayName":"invented person; no person's act","osAccount":"invented","identityVerified":false});
    act["body"]["boundSubject"] = json!(["decision package rec:request"]);
    act["body"]["boundContent"] = json!([{"method":util::FILE_IDENTITY_METHOD,"value":util::sha256_hex(bytes)}]);
    act["body"]["relations"]["requestRef"] = json!("rec:request");
    act_log(&dir, "00-request", &request);
    Decision { dir, package, act }
}
fn act_log(dir: &Path, name: &str, entry: &Value) {
    crate::schema_validation::bundled().unwrap().validate(entry).unwrap();
    std::fs::create_dir_all(dir.join("acts")).unwrap();
    std::fs::write(dir.join(format!("acts/{name}.jsonl")), serde_json::to_string(entry).unwrap() + "\n").unwrap();
}
fn act(d: &Decision, id: &str, alternative: &str) -> Value {
    let mut a = d.act.clone();
    a["recordId"] = json!(format!("rec:{id}"));
    a["seq"] = json!(1);
    a["recorder"]["identity"] = json!(format!("writer:{id}"));
    a["body"]["captureEvidence"][0]["ref"] = json!(format!("cap:{id}"));
    a["body"]["relations"]["alternativeChosen"] = json!(alternative);
    a
}
fn decision_need(w: &Value) -> (String, Value) {
    let row = work(view(w), "W4");
    (row["category"].as_str().unwrap().to_owned(), row["needs"][0].clone())
}

#[test]
fn fleet_views_decision_need_unknown_when_act_records_cannot_be_read() {
    let f = Fixture::not_started();
    let (category, need) = decision_need(&f.read());
    assert_eq!((category.as_str(), need["state"].as_str()), ("unknown", Some("unknown")), "no records store: act records absent");
    assert!(need["why"].as_str().unwrap().contains("act records not read"), "{need}");
    assert!(!f.root.join("store").exists(), "reading creates no records store");

    // A writer creates the store (attach with mint, as recording does).
    let dir = records_store::attach(&f.project, true).unwrap().dir.unwrap();
    let (category, need) = decision_need(&f.read());
    assert_eq!((category.as_str(), need["state"].as_str()), ("unknown", Some("unknown")), "no request record");
    assert!(need["why"].as_str().unwrap().contains("rec:request names no decision request"), "{need}");
    assert!(!dir.join("acts").exists(), "reading creates no act log");

    let d = decision_fixture(&f);
    act_log(&d.dir, "10-act", &act(&d, "act", "ALT-2"));
    assert_eq!(decision_need(&f.read()).1["state"], "satisfied");
    use std::io::Write;
    std::fs::OpenOptions::new().append(true).open(d.dir.join("acts/10-act.jsonl")).unwrap()
        .write_all(b"{\"kind\":\n").unwrap();
    let (category, need) = decision_need(&f.read());
    assert_eq!((category.as_str(), need["state"].as_str()), ("unknown", Some("unknown")), "an unreadable act line leaves the need unknown, never ready");
    assert!(need["why"].as_str().unwrap().contains("not fully read"), "{need}");
}

#[test]
fn fleet_views_decision_need_is_met_only_by_the_persons_recorded_act_of_the_named_kind() {
    let f = Fixture::new();
    let d = decision_fixture(&f);
    let (category, need) = decision_need(&f.read());
    assert_eq!((category.as_str(), need["state"].as_str()), ("waiting", Some("outstanding")), "no act recorded");
    let why = need["why"].as_str().unwrap();
    assert!(why.contains("no recorded act of the person of kind A16") && why.contains("rec:request") && why.contains("records-store:acts/"), "{why}");
    assert_eq!(need["request"]["packageFile"], "decisions/PKG-1.json");

    // An act of another kind citing the request decides nothing.
    let mut other = act(&d, "other-kind", "ALT-2");
    other["body"]["actKind"] = json!("A13");
    other["body"]["relations"].as_object_mut().unwrap().remove("alternativeChosen");
    act_log(&d.dir, "10-other-kind", &other);
    let (category, need) = decision_need(&f.read());
    assert_eq!((category.as_str(), need["state"].as_str()), ("waiting", Some("outstanding")));
    assert!(need["why"].as_str().unwrap().contains("rec:other-kind: an act of kind A13"), "{need}");

    // A decide act choosing an alternative the package does not name.
    act_log(&d.dir, "20-unnamed", &act(&d, "unnamed", "ALT-9"));
    let (category, need) = decision_need(&f.read());
    assert_eq!((category.as_str(), need["state"].as_str()), ("waiting", Some("outstanding")));
    assert!(need["why"].as_str().unwrap().contains("rec:unnamed: act not counted"), "{need}");

    // The recorded act of the person: of the named kind, citing the request
    // and choosing a named alternative. No other act is required before it.
    act_log(&d.dir, "30-act", &act(&d, "act", "ALT-2"));
    let w = f.read();
    let (category, need) = decision_need(&w);
    assert_eq!((category.as_str(), need["state"].as_str()), ("ready", Some("satisfied")), "{need}");
    let decision = &need["decision"];
    assert_eq!(decision["act"], "rec:act");
    assert_eq!(decision["alternativeChosen"], "ALT-2");
    assert!(decision["decidedBy"].as_str().unwrap().contains("identity not verified"));
    assert_eq!(decision["decisionActor"]["displayName"], "invented person; no person's act");
    assert_eq!(decision["recorder"]["identity"], "writer:act", "the recorder is kept apart from the actor");
    assert_eq!(decision["scope"], d.act["body"]["scope"]);
    assert_eq!(decision["purpose"], d.act["body"]["purpose"]);
    assert_eq!(decision["boundContent"], d.act["body"]["boundContent"]);
    assert_eq!(decision["lapse"], "not lapsed");
    let why = need["why"].as_str().unwrap();
    assert!(why.contains("act rec:act (records-store:acts/") && why.contains("seq 1"), "{why}");

    // Lapse: the package file changes after the decision.
    std::fs::write(&d.package, b"{\"edited\":true}").unwrap();
    let (category, need) = decision_need(&f.read());
    assert_eq!((category.as_str(), need["state"].as_str()), ("waiting", Some("outstanding")), "{need}");
    let why = need["why"].as_str().unwrap();
    assert!(why.contains("rec:act") && why.contains("lapse: lapsed") && why.contains("does not settle"), "{why}");
    // An absent package file: the decision view reads it as lapsed (subject absent).
    std::fs::remove_file(&d.package).unwrap();
    let (category, need) = decision_need(&f.read());
    assert_eq!((category.as_str(), need["state"].as_str()), ("waiting", Some("outstanding")));
    assert_eq!(need["decision"]["lapse"], "lapsed (subject absent)");
}

#[test]
fn fleet_views_unordered_decisions_leave_the_decision_need_unknown() {
    let f = Fixture::new();
    let d = decision_fixture(&f);
    act_log(&d.dir, "10-first", &act(&d, "first", "ALT-1"));
    act_log(&d.dir, "20-second", &act(&d, "second", "ALT-2"));
    let (category, need) = decision_need(&f.read());
    assert_eq!((category.as_str(), need["state"].as_str()), ("unknown", Some("unknown")));
    let why = need["why"].as_str().unwrap();
    assert!(why.contains("order the records do not establish") && why.contains("rec:first") && why.contains("rec:second"), "{why}");
}

#[test]
fn fleet_views_decision_records_changed_during_the_read_are_not_used() {
    let f = Fixture::new();
    let d = decision_fixture(&f);
    act_log(&d.dir, "10-act", &act(&d, "act", "ALT-2"));
    assert_eq!(decision_need(&f.read()).1["state"], "satisfied");
    f.flush();
    for changed in [d.dir.join("acts/10-act.jsonl"), d.package.clone()] {
        super::super::AFTER_READ.with(|h| {
            *h.borrow_mut() = Some(Box::new(move || {
                let mut b = std::fs::read(&changed).unwrap();
                b.push(b'\n');
                std::fs::write(changed, b).unwrap();
            }))
        });
        let packet = crate::read_fleet_records_for_workspace(Some(&f.project)).unwrap();
        let v = view(&packet["workspace"]);
        assert!(v["graph"].is_null() && v["waiting"] == json!([]), "no need is presented from a changed snapshot: {v}");
        assert!(packet["limits"].to_string().contains("changed while reading"));
    }
}

#[test]
fn fleet_views_package_swapped_in_during_the_read_never_settles_the_need() {
    // The real package changed after the decision, so the decision has lapsed.
    // A concurrent writer swaps a decoy folder holding the decided bytes into
    // the package's place for the moment it is read, then swaps the real one back.
    let f = Fixture::new();
    let d = decision_fixture(&f);
    act_log(&d.dir, "10-act", &act(&d, "act", "ALT-2"));
    // The package sits one folder below decisions/, so the swap changes only
    // the package's own ancestry.
    let decided = std::fs::read(&d.package).unwrap();
    let deep = f.project.join("decisions/deep/PKG-1.json");
    std::fs::create_dir_all(deep.parent().unwrap()).unwrap();
    std::fs::write(&deep, b"{\"edited\":\"after the decision\"}").unwrap();
    let mut request: Value = serde_json::from_slice(&std::fs::read(d.dir.join("acts/00-request.jsonl")).unwrap()).unwrap();
    request["body"]["evidence"]["ref"] = json!("decisions/deep/PKG-1.json");
    act_log(&d.dir, "00-request", &request);
    let (_, need) = decision_need(&f.read());
    assert_eq!(need["state"], "outstanding", "{need}");
    f.flush();
    let folder = deep.parent().unwrap().to_owned();
    let real = folder.with_file_name("deep-real");
    let mut swapped = false;
    super::DECISION_READ.with(|h| {
        *h.borrow_mut() = Some(Box::new(move |point| {
            if point == "before-package" && !swapped {
                std::fs::rename(&folder, &real).unwrap();
                std::fs::create_dir(&folder).unwrap();
                std::fs::write(folder.join("PKG-1.json"), &decided).unwrap();
                swapped = true;
            } else if point == "after-derive" && swapped {
                std::fs::remove_dir_all(&folder).unwrap();
                std::fs::rename(&real, &folder).unwrap();
                swapped = false;
            }
        }))
    });
    let packet = crate::read_fleet_records_for_workspace(Some(&f.project)).unwrap();
    super::DECISION_READ.with(|h| *h.borrow_mut() = None);
    let v = view(&packet["workspace"]);
    let w4 = v["waiting"].as_array().unwrap().iter().find(|r| r["item"] == "W4");
    if let Some(row) = w4 {
        assert_ne!(row["needs"][0]["state"], "satisfied", "{row}");
        assert_ne!(row["category"], "ready", "{row}");
    }
}

#[test]
fn fleet_views_decision_need_named_by_the_package_file_path() {
    // The App's guidance tells an agent to name the package file it can see.
    let f = Fixture::new();
    let path_need = |f: &mut Fixture, reference: &str| {
        f.graph["body"]["items"][3]["needs"][0] = json!({"kind":"decision","ref":reference});
        f.select();
        decision_need(&f.read())
    };
    let mut f = f;
    let d = decision_fixture(&f);
    // A package file with no request recorded for it yet.
    std::fs::write(f.project.join("decisions/order.json"), b"{\"invented\":\"order package\"}").unwrap();
    let (category, need) = path_need(&mut f, "decisions/order.json");
    assert_eq!((category.as_str(), need["state"].as_str()), ("waiting", Some("outstanding")), "{need}");
    assert!(need["why"].as_str().unwrap().contains("decisions/order.json has not yet been recorded as a request"), "{need}");
    // A path that names no file, and one that is not contained.
    for reference in ["decisions/absent.json", "../decisions/PKG-1.json", "/etc/hosts"] {
        let (category, need) = path_need(&mut f, reference);
        assert_eq!((category.as_str(), need["state"].as_str()), ("unknown", Some("unknown")), "{reference}: {need}");
    }
    // A link is not followed.
    std::os::unix::fs::symlink(&d.package, f.project.join("decisions/linked.json")).unwrap();
    let (_, need) = path_need(&mut f, "decisions/linked.json");
    assert_eq!(need["state"], "unknown", "{need}");
    // The recorded request's package: outstanding with no act, then satisfied.
    let (category, need) = path_need(&mut f, "decisions/PKG-1.json");
    assert_eq!((category.as_str(), need["state"].as_str()), ("waiting", Some("outstanding")), "{need}");
    let why = need["why"].as_str().unwrap();
    assert!(why.contains("package file decisions/PKG-1.json") && why.contains("rec:request"), "{why}");
    act_log(&d.dir, "10-act", &act(&d, "act", "ALT-2"));
    let (category, need) = path_need(&mut f, "decisions/PKG-1.json");
    assert_eq!((category.as_str(), need["state"].as_str()), ("ready", Some("satisfied")), "{need}");
    // Lapse is judged on the file's current content.
    std::fs::write(&d.package, b"{\"edited\":true}").unwrap();
    let (_, need) = path_need(&mut f, "decisions/PKG-1.json");
    assert_eq!(need["state"], "outstanding", "{need}");
    assert!(need["why"].as_str().unwrap().contains("lapse: lapsed"), "{need}");
}

#[test]
fn fleet_views_decision_need_by_path_reconciles_several_requests_for_one_file() {
    let mut f = Fixture::new();
    let d = decision_fixture(&f);
    // A second request for the same file and content, answered the other way.
    let mut second: Value = serde_json::from_slice(&std::fs::read(d.dir.join("acts/00-request.jsonl")).unwrap()).unwrap();
    second["recordId"] = json!("rec:request-again");
    act_log(&d.dir, "01-request-again", &second);
    act_log(&d.dir, "10-act", &act(&d, "act", "ALT-2"));
    let mut other = act(&d, "other", "ALT-1");
    other["body"]["relations"]["requestRef"] = json!("rec:request-again");
    other["body"]["boundSubject"] = json!(["decision package rec:request-again"]);
    act_log(&d.dir, "20-other", &other);
    f.graph["body"]["items"][3]["needs"][0] = json!({"kind":"decision","ref":"decisions/PKG-1.json"});
    f.select();
    let (category, need) = decision_need(&f.read());
    assert_eq!((category.as_str(), need["state"].as_str()), ("unknown", Some("unknown")), "{need}");
    assert!(need["why"].as_str().unwrap().contains("order the records do not establish"), "{need}");
}

#[test]
fn fleet_views_decision_matching_again_after_a_recorded_lapse_stays_outstanding() {
    let f = Fixture::new();
    let d = decision_fixture(&f);
    let a = act(&d, "act", "ALT-2");
    act_log(&d.dir, "10-act", &a);
    // An invented recorded lapse observation: the package changed, then
    // returned to the decided content.
    act_log(&d.dir, "20-lapse", &json!({"format":"chirality.rs.record","formatVersion":"0.1","recordId":"rec:lapse","kind":"act_lapsed",
        "recorder":{"role":"App writer","identity":"writer:lapse"},"context":{"surface":"App"},"seq":1,"writtenAt":"invented",
        "body":{"act":{"recordId":"rec:act","actKind":"A16","capturedAt":a["body"]["captureTime"],"capturingSurface":"app_act_control"},
            "state":"lapsed","referents":a["body"]["boundSubject"],"c0":a["body"]["boundContent"][0],
            "c1":{"method":util::FILE_IDENTITY_METHOD,"value":"changed-invented"},"time":"invented"}}));
    let (category, need) = decision_need(&f.read());
    assert_eq!((category.as_str(), need["state"].as_str()), ("waiting", Some("outstanding")), "{need}");
    assert_eq!(need["decision"]["lapse"], "matches c0 again after observed lapse");
}

/// Every file and folder below `root`, for comparing before and after a read.
fn listing(root: &Path) -> std::collections::BTreeMap<PathBuf, Value> {
    super::super::tests::inventory(root)
}
fn decision_command(project: &Path) -> Value {
    crate::runtime_session::read_decision_packages(project)
}

#[test]
fn fleet_views_decision_reads_create_nothing_where_no_store_exists() {
    let f = Fixture::not_started();
    f.flush();
    let before = listing(&f.root);
    let packet = crate::read_fleet_records_for_workspace(Some(&f.project)).unwrap();
    let (_, need) = decision_need(&packet["workspace"]);
    assert_eq!(need["state"], "unknown", "{need}");
    assert!(need["why"].as_str().unwrap().contains("not created yet"), "{need}");
    let view = decision_command(&f.project);
    assert_eq!(view["rows"], json!([]));
    assert_eq!(listing(&f.root), before, "neither read creates a store, identity or lock");
    assert!(!f.root.join("store").exists());
}

#[test]
fn fleet_views_decision_reads_create_nothing_at_a_redirected_store_alias() {
    let f = Fixture::new();
    // The configured store is an alias of the real one.
    let real = f.root.join("store-real");
    std::fs::create_dir_all(&real).unwrap();
    let alias = f.root.join("store-alias");
    std::os::unix::fs::symlink(&real, &alias).unwrap();
    records_store::use_store_for_test(Some(Ok(records_store::Store {
        root: alias.clone(),
        placement: records_store::Placement::Test,
        limits: vec![],
    })));
    let d = decision_fixture(&f);
    act_log(&d.dir, "10-act", &act(&d, "act", "ALT-2"));
    assert_eq!(decision_need(&f.read()).1["state"], "satisfied");
    f.flush();
    // A cold process, and the alias redirected to an empty folder: once before
    // the read, and once after the store's identity was inspected.
    let empty = f.root.join("empty");
    std::fs::create_dir_all(&empty).unwrap();
    let redirect = {
        let (alias, empty) = (alias.clone(), empty.clone());
        move || {
            std::fs::remove_file(&alias).unwrap();
            std::os::unix::fs::symlink(&empty, &alias).unwrap();
        }
    };
    let restore = |alias: &Path| {
        std::fs::remove_file(alias).unwrap();
        std::os::unix::fs::symlink(&real, alias).unwrap();
    };
    for during in [false, true] {
        // A cold process: the store is given, not started, and none is opened.
        records_store::use_store_not_started_for_test(Some(Ok(records_store::Store {
            root: alias.clone(),
            placement: records_store::Placement::Test,
            limits: vec![],
        })));
        records_store::restore_configured_for_test(records_store::configured_for_test());
        let subtrees = |root: &Path| ["project", "store-real", "empty"].map(|n| listing(&root.join(n)));
        let before = subtrees(&f.root);
        if during {
            let mut redirect = Some(redirect.clone());
            super::DECISION_READ.with(|h| {
                *h.borrow_mut() = Some(Box::new(move |point| {
                    if point == "after-identity" {
                        if let Some(go) = redirect.take() {
                            go()
                        }
                    }
                }))
            });
        } else {
            redirect();
        }
        let packet = crate::read_fleet_records_for_workspace(Some(&f.project)).unwrap();
        super::DECISION_READ.with(|h| *h.borrow_mut() = None);
        let w4 = view(&packet["workspace"])["waiting"].as_array().unwrap().iter().find(|r| r["item"] == "W4").cloned();
        let command = decision_command(&f.project);
        if during {
            // The read opened the real store before the redirect and stays
            // bound to it: what it reads comes from the store it inspected.
            assert_eq!(records_store::opened_existing().unwrap().0, real.canonicalize().unwrap());
        } else {
            // Redirected before any open: no store there, so nothing is read.
            let row = w4.expect("W4 is listed");
            assert_eq!(row["needs"][0]["state"], "unknown", "{row}");
            assert!(row["needs"][0]["why"].as_str().unwrap().contains("not created yet"), "{row}");
            assert!(array(&command["rows"]).iter().all(|r| r["state"] != "decided"), "{command}");
        }
        // The test itself changes only the alias in the fixture's root, so the
        // project, the real store and the empty folder are compared. The one
        // known exception is the derived index under the real store's indexes/.
        let mut after = subtrees(&f.root);
        after[1].retain(|p, _| !p.starts_with("indexes"));
        let mut expected = before.clone();
        expected[1].retain(|p, _| !p.starts_with("indexes"));
        assert_eq!(after, expected, "during={during}: nothing created in the project, the empty folder or the real store");
        assert_eq!(std::fs::read_dir(&empty).unwrap().count(), 0);
        restore(&alias);
    }
}

#[test]
fn fleet_views_decision_need_is_unknown_when_the_act_is_bound_to_other_content_than_its_request() {
    // The request claims other package content than the act was bound to: the
    // need cannot be settled by that act and reads unknown, naming both.
    let f = Fixture::new();
    let d = decision_fixture(&f);
    let mut request: Value = serde_json::from_slice(&std::fs::read(d.dir.join("acts/00-request.jsonl")).unwrap()).unwrap();
    request["body"]["evidence"]["claimedIdentity"] = json!("invented-other-content");
    act_log(&d.dir, "00-request", &request);
    act_log(&d.dir, "10-act", &act(&d, "act", "ALT-2"));
    let (category, need) = decision_need(&f.read());
    assert_eq!((category.as_str(), need["state"].as_str()), ("unknown", Some("unknown")), "{need}");
    let why = need["why"].as_str().unwrap();
    assert!(why.contains("invented-other-content") && why.contains("package identity"), "{why}");
}

#[path = "decision_claims_property_tests.rs"]
mod decision_claims_property;
