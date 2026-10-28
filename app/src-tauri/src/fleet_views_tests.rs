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
        let root = std::env::temp_dir()
            .canonicalize()
            .unwrap()
            .join(util::opaque_id("fleet-views-").unwrap());
        let project = root.join("project");
        std::fs::create_dir_all(&project).unwrap();
        records_store::use_store_for_test(Some(Ok(records_store::Store {
            root: root.join("store"),
            placement: records_store::Placement::Test,
            limits: vec![],
        })));
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
        "../../../execution/PKG-06/DEL-06-01/Design/prototype/fixtures/FX-FL1/briefs/W1.json"
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
        "../../../execution/PKG-06/DEL-06-01/Design/prototype/fixtures/FX-FL1/briefs/W1.json"
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
    let raw=include_str!("../../../execution/PKG-06/DEL-06-01/Design/prototype/fixtures/FX-FL1/coordination.fleet.jsonl");
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
    let raw=include_str!("../../../execution/PKG-06/DEL-06-01/Design/prototype/fixtures/FX-FL1/coordination.fleet.jsonl");
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
