use super::*;
use crate::{
    connector_git::tests::Repo,
    connector_route_store::{self, ProjectRouteStore},
    connector_source::{self, Question, Session},
};
use std::{fs, sync::Mutex};
fn prepared() -> (Repo, Mutex<Session>, PrepareInput) {
    let r = Repo::new("sha1");
    let mut s = Session::default();
    let prepared = s
        .prepare(
            &r.root,
            Question {
                id: "Q-materialization".into(),
                text: "What evidence is retained?".into(),
                asked_revision: r.id("at").into(),
                since_revision: Some(r.id("since").into()),
            },
            "partial".into(),
            None,
        )
        .unwrap();
    let s = Mutex::new(s);
    let token = prepared["sessionToken"].as_str().unwrap();
    let generation = prepared["generation"].as_str().unwrap();
    let selected = connector_source::select(&s, token, generation, || {
        Ok(Some(r.root.join("literal [*].txt")))
    })
    .unwrap();
    let git = connector_source::git_read(
        &s,
        token,
        generation,
        selected["observation"]["reference"].as_str().unwrap(),
        r.id("at"),
        Some(r.id("since")),
    )
    .unwrap();
    let reference = git["git"]["result"]["reference"].as_str().unwrap();
    let anchor = connector_source::git_anchor(
        &s,
        token,
        generation,
        reference,
        "since",
        1,
        2,
        Some("old\r\né\n"),
    )
    .unwrap();
    let a = anchor["git"]["result"]["anchors"][0]["reference"]
        .as_str()
        .unwrap()
        .to_owned();
    let at = git["git"]["result"]["observation"]["at"]["object"]["reference"]
        .as_str()
        .unwrap()
        .to_owned();
    let since = git["git"]["result"]["observation"]["since"]["object"]["reference"]
        .as_str()
        .unwrap()
        .to_owned();
    let input:PrepareInput=serde_json::from_value(json!({"sessionToken":token,"generation":generation,"gitReference":reference,"connector":"pec","sources":[{"reference":at,"role":"Current comparison bytes","anchors":[]},{"reference":since,"role":"Earlier comparison bytes","anchors":[a]}],"interpretations":[{"statement":"<script>Caller comparison</script>","assertedBy":"Caller supplied name","sourceReferences":[since],"anchorReferences":[a]}],"gaps":[],"unsupported":[],"duties":[{"duty":"locate_compare","standing":"prepared","reason":"Caller says evidence prepared only"},{"duty":"review_integrate","standing":"outstanding","reason":"Review not performed"},{"duty":"cross_undertaking_coordination","standing":"outstanding","reason":"No coordination act"}]})).unwrap();
    (r, s, input)
}
fn account(s: &Mutex<Session>, i: &PrepareInput) -> Value {
    let e = s
        .lock()
        .unwrap()
        .materialization_evidence(&i.session_token, &i.generation, &i.git_reference)
        .unwrap();
    compose(&e, i, "app-fixture-instance").unwrap()
}
#[test]
fn connector_materialization_private_evidence_compact_mapping_and_schema() {
    let (_r, s, i) = prepared();
    let v = account(&s, &i);
    connector_route_store::validate_account(&v).unwrap();
    assert_eq!(v["facts"], json!([]));
    assert_eq!(v["conclusions"]["supported"], json!([]));
    assert_eq!(v["recorder"]["kind"], "app");
    assert_eq!(
        v["evidence"]["selection_mechanism"],
        "synthetic_test_callback"
    );
    assert_eq!(v["sources"][1]["excerpts"][0]["text"], "old\r\né\n");
    assert_eq!(v["sources"][1]["excerpts"][0]["byte_end"], 8);
    assert_eq!(v["gaps"][0]["responsible"]["identity"], Value::Null);
    assert!(!v.to_string().contains("rawCommitHex"));
    assert!(!v.to_string().contains("admin"));
    let e = s
        .lock()
        .unwrap()
        .materialization_evidence(&i.session_token, &i.generation, &i.git_reference)
        .unwrap();
    assert_eq!(
        v["evidence"]["association_sha256"],
        crate::util::sha256_hex(&serde_json::to_vec(&e.association).unwrap())
    );
    assert_eq!(
        v["sources"][1]["provenance"]["traversal_sha256"],
        crate::util::sha256_hex(
            &serde_json::to_vec(&e.since.unwrap().unwrap().view["traversed"]).unwrap()
        )
    );
}
#[test]
fn connector_materialization_semantics_reject_schema_false_positives() {
    let (_r, s, i) = prepared();
    let v = account(&s, &i);
    let validators = crate::schema_validation::compile_targets(
        &[
            (
                "draft",
                include_str!(
                    "../resources/connector_route/connector.route-account.v0.3.schema.json"
                ),
            ),
            (
                "standing",
                include_str!("../resources/connector_route/connector.standing.schema.json"),
            ),
        ],
        &["urn:chirality:app-v4:del-07-02:route-account:0.3"],
        &[
            "urn:chirality:app-v4:del-07-02:route-account:0.3",
            "urn:chirality:app-v4:del-07-02:connector-standing:0.1",
        ],
    )
    .unwrap();
    for change in 0..4 {
        let mut bad = v.clone();
        match change {
            0 => bad["duties"][1] = bad["duties"][0].clone(),
            1 => bad["sources"][0]["revision"] = json!("0".repeat(40)),
            2 => bad["interpretations"][0]["source_ids"] = json!(["missing"]),
            _ => bad["sources"][1]["excerpts"][0]["sha256"] = json!("0".repeat(64)),
        };
        assert!(
            validators[0].is_valid(&bad),
            "fixture must isolate semantic false positive"
        );
        assert!(connector_route_store::validate_account(&bad).is_err());
    }
    for (key, value) in [("facts", json!([{}])), ("standing", json!("completed"))] {
        let mut bad = v.clone();
        bad[key] = value;
        assert!(connector_route_store::validate_account(&bad).is_err());
    }
}
#[test]
fn connector_materialization_refuses_forged_selections_and_question_mismatch() {
    let (_r, s, i) = prepared();
    let e = s
        .lock()
        .unwrap()
        .materialization_evidence(&i.session_token, &i.generation, &i.git_reference)
        .unwrap();
    let mut bad = i.clone();
    bad.sources[0].reference = "forged".into();
    assert!(compose(&e, &bad, "app").is_err());
    bad = i.clone();
    bad.sources[0].role = " ".into();
    assert!(compose(&e, &bad, "app").is_err());
    bad = i.clone();
    bad.sources[0].anchors = bad.sources[1].anchors.clone();
    assert!(compose(&e, &bad, "app").is_err());
    let mut e = e;
    e.question["askedRevision"] = json!("caller differs");
    assert!(compose(&e, &i, "app").unwrap_err().contains("mismatch"));
}
#[test]
fn connector_materialization_gaps_only_utf8_and_escaped_size_limits() {
    let (r, s, mut i) = prepared();
    let missing = "0".repeat(40);
    let p = s
        .lock()
        .unwrap()
        .prepare(
            &r.root,
            Question {
                id: "Q-gap".into(),
                text: "Missing locally".into(),
                asked_revision: missing.clone(),
                since_revision: Some(missing.clone()),
            },
            "absent".into(),
            Some("Assigned by caller".into()),
        )
        .unwrap();
    i.session_token = p["sessionToken"].as_str().unwrap().into();
    i.generation = p["generation"].as_str().unwrap().into();
    let local = connector_source::select(&s, &i.session_token, &i.generation, || {
        Ok(Some(r.root.join("literal [*].txt")))
    })
    .unwrap();
    let git = connector_source::git_read(
        &s,
        &i.session_token,
        &i.generation,
        local["observation"]["reference"].as_str().unwrap(),
        &missing,
        Some(&missing),
    )
    .unwrap();
    i.git_reference = git["git"]["result"]["reference"].as_str().unwrap().into();
    i.sources.clear();
    i.interpretations.clear();
    let v = account(&s, &i);
    assert_eq!(v["sources"], json!([]));
    assert_eq!(
        v["gaps"]
            .as_array()
            .unwrap()
            .iter()
            .filter(|g| g["origin"] == "observed_git_failure")
            .count(),
        2
    );
    assert_eq!(
        v["gaps"][0]["responsible"]["identity"],
        "Assigned by caller"
    );
    assert!(
        !r.root.join(".chirality").exists(),
        "prepare must not publish"
    );
    let mut e = s
        .lock()
        .unwrap()
        .materialization_evidence(&i.session_token, &i.generation, &i.git_reference)
        .unwrap();
    use std::os::unix::ffi::OsStringExt;
    e.relative = std::ffi::OsString::from_vec(b"bad-\xff".to_vec()).into();
    assert!(compose(&e, &i, "app").unwrap_err().contains("UTF-8"));
    e.relative = "literal [*].txt".into();
    i.gaps.push(GapInput {
        gap: "\u{1}".repeat(180000),
        effect: "Caller text whose escaped bytes exceed cap".into(),
        responsible: Responsibility {
            standing: "unassigned".into(),
            identity: None,
        },
    });
    assert!(compose(&e, &i, "app").unwrap_err().contains("1MiB"));
}
#[test]
fn connector_materialization_real_writer_cold_semantics_and_original_byte_cap() {
    let (r, s, i) = prepared();
    let v = account(&s, &i);
    let store = ProjectRouteStore::open(&r.root).unwrap();
    let reference = store.write(&v).unwrap();
    assert_eq!(store.resolve(&reference).unwrap().account, v);
    let path = r.root.join(&reference.relative_path);
    let mut bytes = serde_json::to_vec(&v).unwrap();
    bytes.extend(vec![b' '; BYTE_LIMIT]);
    fs::write(&path, bytes).unwrap();
    let cold = store.discover();
    assert!(cold.accounts.is_empty());
    assert!(cold
        .issues
        .iter()
        .any(|e| e.detail.contains("original bytes")));
    fs::remove_file(path).unwrap();
    let old: Value = serde_json::from_str(include_str!(
        "../../tests/fixtures/connector-route-source-walk.json"
    ))
    .unwrap();
    let oldref = store.write(&old).unwrap();
    let mut bytes = serde_json::to_vec(&old).unwrap();
    bytes.extend(vec![b' '; BYTE_LIMIT]);
    fs::write(r.root.join(oldref.relative_path), bytes).unwrap();
    let cold = store.discover();
    assert_eq!(
        cold.accounts.len(),
        1,
        "old version acquisition semantics unchanged"
    );
    assert_eq!(cold.accounts[0].account["formatVersion"], "0.2");
}
fn current_draft(v: &Value) -> (&str, &str) {
    let e = v["entries"]
        .as_array()
        .unwrap()
        .iter()
        .find(|e| e["status"] == "prepared")
        .unwrap();
    (
        e["token"].as_str().unwrap(),
        e["generation"].as_str().unwrap(),
    )
}
#[test]
fn connector_materialization_once_only_actual_outcome_survives_cancel_and_new_session() {
    let (r, s, i) = prepared();
    let registry = Mutex::new(Registry::default());
    let prepared = prepare(&registry, &s, i.clone(), &r.root).unwrap();
    let (t, g) = current_draft(&prepared);
    let published =
        super::registry::publish_with(&registry, &s, t, g, &r.root, |store, account| {
            std::thread::scope(|scope| {
                let duplicate = scope.spawn(|| {
                    super::registry::publish_with(&registry, &s, t, g, &r.root, |_, _| {
                        panic!("concurrent duplicate write")
                    })
                });
                assert_eq!(duplicate.join().unwrap().unwrap()["inflight"], t);
            });
            let cancelled = registry.lock().unwrap().cancel(t, g).unwrap();
            assert_eq!(cancelled["inflight"], t);
            assert!(prepare(&registry, &s, i.clone(), &r.root)
                .unwrap_err()
                .contains("in flight"));
            s.lock()
                .unwrap()
                .prepare(
                    &r.root,
                    Question {
                        id: "new".into(),
                        text: "New question after write start".into(),
                        asked_revision: "new".into(),
                        since_revision: None,
                    },
                    "absent".into(),
                    None,
                )
                .unwrap();
            store.write(account)
        })
        .unwrap();
    let e = &published["entries"][0];
    assert_eq!(e["status"], "published");
    assert!(e["draft"].is_null());
    let again = super::registry::publish_with(&registry, &s, t, g, &r.root, |_, _| {
        panic!("repeat must never invoke writer")
    })
    .unwrap();
    assert_eq!(again["entries"][0]["outcomeText"], e["outcomeText"]);
    assert_eq!(registry.lock().unwrap().retained(t,g).unwrap().unwrap()["entries"][0]["status"],"published");
    assert_eq!(
        ProjectRouteStore::open(&r.root)
            .unwrap()
            .discover()
            .accounts
            .len(),
        1
    );
    assert!(
        publish(&Mutex::new(Registry::default()), &s, t, g, &r.root).is_err(),
        "new instance cannot revive token"
    );
}
#[test]
fn connector_materialization_retention_capacity_atomic_replacement_and_stale_freeze() {
    let (r, s, i) = prepared();
    let registry = Mutex::new(Registry::default());
    let first = prepare(&registry, &s, i.clone(), &r.root).unwrap();
    let mut bad = i.clone();
    bad.sources[0].role.clear();
    assert!(prepare(&registry, &s, bad, &r.root).is_err());
    assert_eq!(registry.lock().unwrap().view(), first);
    for n in 2..=64 {
        let v = prepare(&registry, &s, i.clone(), &r.root).unwrap();
        assert_eq!(v["used"], n);
        assert_eq!(
            v["entries"]
                .as_array()
                .unwrap()
                .iter()
                .filter(|e| !e["draft"].is_null())
                .count(),
            1
        );
        let (t, g) = current_draft(&v);
        registry.lock().unwrap().cancel(t, g).unwrap();
    }
    let before = registry.lock().unwrap().view();
    assert!(prepare(&registry, &s, i.clone(), &r.root)
        .unwrap_err()
        .contains("capacity"));
    assert_eq!(registry.lock().unwrap().view(), before);
    let empty = Mutex::new(Registry::default());
    assert!(
        super::registry::prepare_with(&empty, &s, i.clone(), &r.root, || {
            connector_source::select(&s, &i.session_token, &i.generation, || Ok(None)).unwrap();
        })
        .is_err()
    );
    assert_eq!(empty.lock().unwrap().view()["used"], 0);
}
#[test]
fn connector_materialization_uncertainty_reconciliation_preserves_original_attempt() {
    let (r, s, i) = prepared();
    let registry = Mutex::new(Registry::default());
    let prepared = prepare(&registry, &s, i.clone(), &r.root).unwrap();
    let (t, g) = current_draft(&prepared);
    let uncertain =
        super::registry::publish_with(&registry, &s, t, g, &r.root, |store, account| {
            store.test_write_uncertain(account)
        })
        .unwrap();
    assert_eq!(uncertain["entries"][0]["status"], "uncertain");
    let original = uncertain["entries"][0]["outcomeText"].clone();
    assert!(original.as_str().unwrap().contains("attempt"));
    let reconciled = registry.lock().unwrap().reconcile(t, g).unwrap();
    assert_eq!(reconciled["entries"][0]["outcomeText"], original);
    assert_eq!(reconciled["entries"][0]["status"], "uncertain");
    assert!(reconciled["entries"][0]["reconciliationText"]
        .as_str()
        .unwrap()
        .contains("observed_after_uncertainty"));
    let repeated = super::registry::publish_with(&registry, &s, t, g, &r.root, |_, _| {
        panic!("uncertain token cannot retry")
    })
    .unwrap();
    assert_eq!(repeated["used"], 1);
    // Publication added the account directory and changed the observed root metadata.
    // A genuinely new draft obtains a new explicit Git observation, not an implicit retry.
    let mut i = i;
    let evidence = s
        .lock()
        .unwrap()
        .materialization_evidence(&i.session_token, &i.generation, &i.git_reference)
        .unwrap();
    let fresh = connector_source::git_read(
        &s,
        &i.session_token,
        &i.generation,
        &evidence.local_reference,
        r.id("at"),
        Some(r.id("since")),
    )
    .unwrap();
    i.git_reference = fresh["git"]["result"]["reference"].as_str().unwrap().into();
    for (choice, side) in i.sources.iter_mut().zip(["at", "since"]) {
        choice.reference = fresh["git"]["result"]["observation"][side]["object"]["reference"]
            .as_str()
            .unwrap()
            .into();
        choice.anchors.clear();
    }
    i.interpretations.clear();
    for _ in 1..64 {
        let v = prepare(&registry, &s, i.clone(), &r.root).unwrap();
        let (a, b) = current_draft(&v);
        registry.lock().unwrap().cancel(a, b).unwrap();
    }
    assert!(prepare(&registry, &s, i, &r.root).is_err());
    let retained = registry.lock().unwrap().view();
    let e = retained["entries"]
        .as_array()
        .unwrap()
        .iter()
        .find(|e| e["token"] == t)
        .unwrap();
    assert_eq!(e["outcomeText"], original);
    assert_eq!(e["status"], "uncertain");
}
#[test]
fn connector_materialization_prepublication_root_duplicate_incomplete_and_cancel_refuse() {
    for cause in ["root", "duplicate", "incomplete", "cancel", "reread"] {
        let (r, s, i) = prepared();
        let registry = Mutex::new(Registry::default());
        let draft = prepare(&registry, &s, i.clone(), &r.root).unwrap();
        let (t, g) = current_draft(&draft);
        let moved = r.root.with_extension("moved");
        match cause {
            "root" => {
                fs::rename(&r.root, &moved).unwrap();
                fs::create_dir(&r.root).unwrap();
            }
            "duplicate" => {
                ProjectRouteStore::open(&r.root)
                    .unwrap()
                    .write(&draft["entries"][0]["draft"]["account"])
                    .unwrap();
            }
            "reread" => { connector_source::select(&s,&i.session_token,&i.generation,||Ok(Some(r.root.join("literal [*].txt")))).unwrap(); },
            "incomplete" => {
                fs::write(r.root.join(".chirality"), b"not a directory").unwrap();
            }
            _ => {
                registry.lock().unwrap().cancel(t, g).unwrap();
            }
        }
        let result = super::registry::publish_with(&registry, &s, t, g, &r.root, |_, _| {
            panic!("preflight must refuse writer")
        })
        .unwrap();
        assert!(matches!(
            result["entries"][0]["status"].as_str(),
            Some("refused" | "cancelled")
        ));
        if cause == "root" {
            fs::remove_dir(&r.root).unwrap();
            fs::rename(moved, &r.root).unwrap();
        }
    }
}
#[test]
fn connector_materialization_exact_serialized_limit_and_partial_side(){
    let(r,s,mut i)=prepared();let e=s.lock().unwrap().materialization_evidence(&i.session_token,&i.generation,&i.git_reference).unwrap();
    i.gaps.push(GapInput{gap:"x".into(),effect:"Explicit caller gap".into(),responsible:Responsibility{standing:"unassigned".into(),identity:None}});
    let first=compose(&e,&i,"app-fixture").unwrap();let size=serde_json::to_vec(&first).unwrap().len();i.gaps[0].gap="x".repeat(BYTE_LIMIT-size+1);
    let exact=compose(&e,&i,"app-fixture").unwrap();assert_eq!(serde_json::to_vec(&exact).unwrap().len(),BYTE_LIMIT);let reference=ProjectRouteStore::open(&r.root).unwrap().write(&exact).unwrap();assert_eq!(ProjectRouteStore::open(&r.root).unwrap().resolve(&reference).unwrap().account,exact);
    let missing="0".repeat(40);let p=s.lock().unwrap().prepare(&r.root,Question{id:"partial".into(),text:"Known at, missing since".into(),asked_revision:r.id("at").into(),since_revision:Some(missing.clone())},"partial".into(),None).unwrap();
    i.session_token=p["sessionToken"].as_str().unwrap().into();i.generation=p["generation"].as_str().unwrap().into();
    let local=connector_source::select(&s,&i.session_token,&i.generation,||Ok(Some(r.root.join("literal [*].txt")))).unwrap();let git=connector_source::git_read(&s,&i.session_token,&i.generation,local["observation"]["reference"].as_str().unwrap(),r.id("at"),Some(&missing)).unwrap();
    i.git_reference=git["git"]["result"]["reference"].as_str().unwrap().into();i.sources.truncate(1);i.sources[0].reference=git["git"]["result"]["observation"]["at"]["object"]["reference"].as_str().unwrap().into();i.sources[0].anchors.clear();i.interpretations.clear();i.gaps.clear();
    let partial=account(&s,&i);assert_eq!(partial["sources"].as_array().unwrap().len(),1);assert_eq!(partial["gaps"][0]["context"]["side"],"since");assert_eq!(partial["gaps"][0]["origin"],"observed_git_failure");
}
