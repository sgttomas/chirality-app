use super::*;
use crate::{
    connector_git::tests::Repo,
    connector_route_store::{self, ProjectRouteStore},
    connector_source::{self, Question, Session},
};
use std::{fs, sync::Mutex};
fn prepared() -> (Repo, Mutex<Session>, PrepareInput) { prepared_layout(false) }
fn prepared_layout(existing_store:bool) -> (Repo, Mutex<Session>, PrepareInput) {
    let r = Repo::new("sha1");
    if existing_store {fs::create_dir_all(r.root.join(".chirality/records/connectors/route-accounts")).unwrap();}
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
    assert_eq!(
        registry.lock().unwrap().retained(t, g).unwrap().unwrap()["entries"][0]["status"],
        "published"
    );
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
            "reread" => {
                connector_source::select(&s, &i.session_token, &i.generation, || {
                    Ok(Some(r.root.join("literal [*].txt")))
                })
                .unwrap();
            }
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
fn connector_materialization_exact_serialized_limit_and_partial_side() {
    let (r, s, mut i) = prepared();
    let e = s
        .lock()
        .unwrap()
        .materialization_evidence(&i.session_token, &i.generation, &i.git_reference)
        .unwrap();
    i.gaps.push(GapInput {
        gap: "x".into(),
        effect: "Explicit caller gap".into(),
        responsible: Responsibility {
            standing: "unassigned".into(),
            identity: None,
        },
    });
    let first = compose(&e, &i, "app-fixture").unwrap();
    let size = serde_json::to_vec(&first).unwrap().len();
    i.gaps[0].gap = "x".repeat(BYTE_LIMIT - size + 1);
    let exact = compose(&e, &i, "app-fixture").unwrap();
    assert_eq!(serde_json::to_vec(&exact).unwrap().len(), BYTE_LIMIT);
    let reference = ProjectRouteStore::open(&r.root)
        .unwrap()
        .write(&exact)
        .unwrap();
    assert_eq!(
        ProjectRouteStore::open(&r.root)
            .unwrap()
            .resolve(&reference)
            .unwrap()
            .account,
        exact
    );
    let missing = "0".repeat(40);
    let p = s
        .lock()
        .unwrap()
        .prepare(
            &r.root,
            Question {
                id: "partial".into(),
                text: "Known at, missing since".into(),
                asked_revision: r.id("at").into(),
                since_revision: Some(missing.clone()),
            },
            "partial".into(),
            None,
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
        r.id("at"),
        Some(&missing),
    )
    .unwrap();
    i.git_reference = git["git"]["result"]["reference"].as_str().unwrap().into();
    i.sources.truncate(1);
    i.sources[0].reference = git["git"]["result"]["observation"]["at"]["object"]["reference"]
        .as_str()
        .unwrap()
        .into();
    i.sources[0].anchors.clear();
    i.interpretations.clear();
    i.gaps.clear();
    let partial = account(&s, &i);
    assert_eq!(partial["sources"].as_array().unwrap().len(), 1);
    assert_eq!(partial["gaps"][0]["context"]["side"], "since");
    assert_eq!(partial["gaps"][0]["origin"], "observed_git_failure");
}

fn reconstruction_input(
    s: &Mutex<Session>,
    mut draft: PrepareInput,
) -> crate::connector_reconstruction::Input {
    draft.interpretations.clear();
    let v = connector_source::git_anchor(
        s,
        &draft.session_token,
        &draft.generation,
        &draft.git_reference,
        "at",
        1,
        1,
        None,
    )
    .unwrap();
    let anchor = v["git"]["result"]["anchors"]
        .as_array()
        .unwrap()
        .last()
        .unwrap()["reference"]
        .as_str()
        .unwrap()
        .to_string();
    draft.sources[0].anchors.push(anchor.clone());
    let since = draft.sources[1].anchors[0].clone();
    crate::connector_reconstruction::Input {
        draft,
        pairs: vec![crate::connector_reconstruction::PairInput {
            key: "pair".into(),
            since_anchor: since.clone(),
            at_anchor: anchor.clone(),
        }],
        claims: vec![crate::connector_reconstruction::ClaimInput {
            key: "claim".into(),
            statement: "The selected record text differs; no completion proved".into(),
            asserted_by: "Caller".into(),
            asserted_role: "agent".into(),
            scope: "record_change".into(),
            anchors: vec![since.clone(), anchor],
            pairs: vec!["pair".into()],
        }],
        contradictions: vec![],
        reports: vec![crate::connector_reconstruction::ReportInput {
            duty: "locate_compare".into(),
            reported_by: "Reporter".into(),
            reported_actor: Some("Unverified actor".into()),
            reported_status: "performed".into(),
            reason: "Record claim only".into(),
            anchors: vec![since],
        }],
    }
}
#[test]
fn connector_reconstruction_joined_private_git_publication_cold() {
    let (r, s, i) = prepared();
    let input = reconstruction_input(&s, i);
    let registry = Mutex::new(Registry::default());
    let view = crate::connector_reconstruction::prepare(&registry, &s, input, &r.root).unwrap();
    let entry = &view["entries"][0];
    assert_eq!(entry["draft"]["account"]["formatVersion"], "0.4");
    let done = publish(
        &registry,
        &s,
        entry["token"].as_str().unwrap(),
        entry["generation"].as_str().unwrap(),
        &r.root,
    )
    .unwrap();
    assert_eq!(done["entries"][0]["status"], "published");
    let store = ProjectRouteStore::open(&r.root).unwrap();
    let cold = store.discover();
    assert_eq!(cold.accounts.len(), 1);
    let a = &cold.accounts[0].account;
    assert_eq!(a["formatVersion"], "0.4");
    assert_eq!(a["facts"].as_array().unwrap().len(), 2);
    assert_eq!(a["comparisons"][0]["relation"], "different_excerpt_bytes");
    assert_eq!(
        a["contribution_reports"][0]["performance_verification"],
        "not_established"
    );
    assert_ne!(a["duties"][0]["standing"], "performed");
    assert_eq!(
        publish(
            &registry,
            &s,
            entry["token"].as_str().unwrap(),
            entry["generation"].as_str().unwrap(),
            &r.root
        )
        .unwrap(),
        done
    );
}
#[test]
fn connector_reconstruction_retained_source_negative_shapes() {
    let good: Value = serde_json::from_str(include_str!(
        "../resources/connector_route/record_reconstruction_v04.fixture.json"
    ))
    .unwrap();
    connector_route_store::validate_account(&good).unwrap();
    let mut nul = good.clone();
    let bytes = b"status:\0pending\n";
    nul["sources"][0]["excerpts"][0]["text"] = json!(std::str::from_utf8(bytes).unwrap());
    nul["sources"][0]["excerpts"][0]["byte_end"] = json!(bytes.len());
    nul["sources"][0]["excerpts"][0]["sha256"] = json!(crate::util::sha256_hex(bytes));
    assert!(connector_route_store::validate_account(&nul)
        .unwrap_err()
        .to_string()
        .contains("NUL excerpt"));
    let mut cases = vec![];
    let mut a = good.clone();
    a["sources"][0]["excerpts"][0]["anchor"] = json!("L99-L1");
    a["facts"][0]["anchor"] = json!("L99-L1");
    cases.push(a);
    let mut a = good.clone();
    a["sources"][0]["excerpts"][0]["byte_start"] = json!(1);
    a["sources"][0]["excerpts"][0]["byte_end"] = json!(17);
    cases.push(a);
    let mut a = good.clone();
    a["evidence"]["selected_path"] = json!("bad\0path");
    for s in a["sources"].as_array_mut().unwrap() {
        s["path"] = json!("bad\0path");
    }
    cases.push(a);
    let mut a = good.clone();
    let gap = json!({"origin":"observed_git_failure","gap":"Invented","effect":"Missing","responsible":{"standing":"unassigned","identity":null},"context":{"side":"at","requested_commit":a["question"]["at_revision"],"path":"record.md"}});
    a["gaps"].as_array_mut().unwrap().push(gap);
    cases.push(a);
    let mut a = good.clone();
    a["question"]["since_revision"] = json!("c".repeat(64));
    a["evidence"]["git_request"]["since"] = json!("c".repeat(64));
    a["sources"][0]["revision"] = json!("c".repeat(64));
    a["sources"][0]["provenance"]["object_format"] = json!("sha256");
    for k in ["commit", "root_tree", "blob"] {
        a["sources"][0]["provenance"][k] = json!("c".repeat(64));
    }
    cases.push(a);
    for (n, a) in cases.iter().enumerate() {
        assert!(
            connector_route_store::validate_account(a).is_err(),
            "source negative {n}"
        );
    }
    for pointer in [
        "/facts/0/statement",
        "/claims/0/fact_ids/0",
        "/contribution_reports/0/fact_ids/0",
    ] {
        let mut a = good.clone();
        *a.pointer_mut(pointer).unwrap() = json!("forged");
        assert!(connector_route_store::validate_account(&a).is_err());
    }
}
#[test]
fn connector_reconstruction_hot_forgery_and_contradiction() {
    let (_r, s, i) = prepared();
    let mut input = reconstruction_input(&s, i);
    let e = s
        .lock()
        .unwrap()
        .materialization_evidence(
            &input.draft.session_token,
            &input.draft.generation,
            &input.draft.git_reference,
        )
        .unwrap();
    let mut c = input.claims[0].clone();
    c.key = "opposing".into();
    c.statement = "<script>Competing claim</script>".into();
    input.claims.push(c);
    input
        .contradictions
        .push(crate::connector_reconstruction::ContradictionInput {
            claims: vec!["claim".into(), "opposing".into()],
            description: "Unresolved conflict".into(),
            effect: "Answer unresolved".into(),
            responsible: Responsibility {
                standing: "unassigned".into(),
                identity: None,
            },
        });
    let a = crate::connector_reconstruction::compose(&e, &input, "app-test").unwrap();
    assert_eq!(a["claims"].as_array().unwrap().len(), 2);
    assert!(a["gaps"]
        .as_array()
        .unwrap()
        .iter()
        .any(|g| g["gap"] == "Unresolved conflict"));
    let mut bad = input.clone();
    bad.reports[0].anchors = vec!["rs:forged-act".into()];
    assert!(crate::connector_reconstruction::compose(&e, &bad, "app-test").is_err());
    let mut bad = input.clone();
    bad.pairs[0].since_anchor = bad.pairs[0].at_anchor.clone();
    assert!(crate::connector_reconstruction::compose(&e, &bad, "app-test").is_err());
    let mut bad = input;
    bad.draft.sources.pop();
    assert!(crate::connector_reconstruction::compose(&e, &bad, "app-test").is_err());
}
#[test]
fn connector_reconstruction_partial_gaps_only_and_equal_excerpts() {
    let (_r, s, i) = prepared();
    let mut input = reconstruction_input(&s, i);
    let mut e = s
        .lock()
        .unwrap()
        .materialization_evidence(
            &input.draft.session_token,
            &input.draft.generation,
            &input.draft.git_reference,
        )
        .unwrap();
    let since_ref = input.draft.sources[1].reference.clone();
    // Synthetic completed failure changes only the private test evidence; no missing side source fabricated.
    e.since = Some(Err(crate::connector_git_process::Failure::side(
        "missing-object",
        "Constructed absence",
    )));
    input.draft.sources.retain(|x| x.reference != since_ref);
    input.pairs.clear();
    input.claims.clear();
    input.reports.clear();
    let partial = crate::connector_reconstruction::compose(&e, &input, "app-test").unwrap();
    assert_eq!(partial["sources"].as_array().unwrap().len(), 1);
    assert_eq!(partial["comparisons"], json!([]));
    e.at = Err(crate::connector_git_process::Failure::side(
        "missing-object",
        "Constructed absence",
    ));
    input.draft.sources.clear();
    let empty = crate::connector_reconstruction::compose(&e, &input, "app-test").unwrap();
    for key in ["facts", "comparisons", "claims", "contribution_reports"] {
        assert_eq!(empty[key], json!([]));
    }
    let mut mixed = empty;
    mixed["question"]["since_revision"] = json!("c".repeat(64));
    mixed["evidence"]["git_request"]["since"] = json!("c".repeat(64));
    for g in mixed["gaps"].as_array_mut().unwrap() {
        if g["context"]["side"] == "since" {
            g["context"]["requested_commit"] = json!("c".repeat(64));
        }
    }
    assert!(connector_route_store::validate_account(&mixed).is_err());
    let mut same: Value = serde_json::from_str(include_str!(
        "../resources/connector_route/record_reconstruction_v04.fixture.json"
    ))
    .unwrap();
    let old = same["sources"][0]["excerpts"][0].clone();
    for k in ["text", "sha256", "byte_end"] {
        same["sources"][1]["excerpts"][0][k] = old[k].clone();
    }
    same["facts"][1]["statement"] = json!(format!(
        "Observed excerpt e-at at {}; content SHA-256 {}.",
        "b".repeat(40),
        old["sha256"].as_str().unwrap()
    ));
    same["comparisons"][0]["relation"] = json!("same_excerpt_bytes");
    same["conclusions"]["supported"][1]["statement"] = same["facts"][1]["statement"].clone();
    same["conclusions"]["supported"][2]["statement"]=json!("Selected excerpts f-since and f-at: same_excerpt_bytes; no whole-record or substantive-change conclusion.");
    connector_route_store::validate_account(&same).unwrap();
    assert_ne!(same["sources"][0]["sha256"], same["sources"][1]["sha256"]);
}
#[test]
fn connector_reconstruction_shared_capacity_stale_and_uncertainty() {
    let (r, s, i) = prepared();
    let input = reconstruction_input(&s, i.clone());
    let reg = Mutex::new(Registry::default());
    for n in 0..64 {
        let v = if n % 2 == 0 {
            crate::connector_reconstruction::prepare(&reg, &s, input.clone(), &r.root).unwrap()
        } else {
            prepare(&reg, &s, i.clone(), &r.root).unwrap()
        };
        assert_eq!(v["used"], n + 1);
        assert_eq!(
            v["entries"]
                .as_array()
                .unwrap()
                .iter()
                .filter(|e| e["status"] == "prepared")
                .count(),
            1
        );
    }
    assert!(
        crate::connector_reconstruction::prepare(&reg, &s, input.clone(), &r.root)
            .unwrap_err()
            .contains("capacity")
    );
    let reg = Mutex::new(Registry::default());
    let frozen =
        crate::connector_reconstruction::prepare(&reg, &s, input.clone(), &r.root).unwrap();
    let (t, g) = current_draft(&frozen);
    let uncertain = super::registry::publish_with(&reg, &s, t, g, &r.root, |store, a| {
        reg.lock().unwrap().cancel(t, g).unwrap();
        store.test_write_uncertain(a)
    })
    .unwrap();
    assert_eq!(uncertain["entries"][0]["status"], "uncertain");
    let outcome = uncertain["entries"][0]["outcomeText"].clone();
    *s.lock().unwrap() = Session::default();
    assert_eq!(
        reg.lock().unwrap().reconcile(t, g).unwrap()["entries"][0]["outcomeText"],
        outcome
    );
    assert_eq!(
        publish(&reg, &s, t, g, &r.root).unwrap()["entries"][0]["outcomeText"],
        outcome
    );
    let (r, s, i) = prepared();
    let input = reconstruction_input(&s, i);
    let reg = Mutex::new(Registry::default());
    let frozen =
        crate::connector_reconstruction::prepare(&reg, &s, input.clone(), &r.root).unwrap();
    let (t, g) = current_draft(&frozen);
    connector_source::select(
        &s,
        &input.draft.session_token,
        &input.draft.generation,
        || Ok(None),
    )
    .unwrap();
    let refused = super::registry::publish_with(&reg, &s, t, g, &r.root, |_, _| {
        panic!("stale cancelled source must not write")
    })
    .unwrap();
    assert_eq!(refused["entries"][0]["status"], "refused");
}
#[test]
fn connector_reconstruction_byte_limit_and_cold_forgery_boundary() {
    let (r, s, i) = prepared();
    let mut input = reconstruction_input(&s, i);
    let e = s
        .lock()
        .unwrap()
        .materialization_evidence(
            &input.draft.session_token,
            &input.draft.generation,
            &input.draft.git_reference,
        )
        .unwrap();
    input.draft.gaps.push(GapInput {
        gap: "x".into(),
        effect: "Caller gap".into(),
        responsible: Responsibility {
            standing: "unassigned".into(),
            identity: None,
        },
    });
    let initial = crate::connector_reconstruction::compose(&e, &input, "app-test").unwrap();
    let size = serde_json::to_vec(&initial).unwrap().len();
    input.draft.gaps[0].gap = "x".repeat(BYTE_LIMIT - size + 1);
    let exact = crate::connector_reconstruction::compose(&e, &input, "app-test").unwrap();
    assert_eq!(serde_json::to_vec(&exact).unwrap().len(), BYTE_LIMIT);
    let store = ProjectRouteStore::open(&r.root).unwrap();
    let bound = store.write(&exact).unwrap();
    assert_eq!(store.resolve(&bound).unwrap().account, exact);
    input.draft.gaps[0].gap.push('x');
    assert!(crate::connector_reconstruction::compose(&e, &input, "app-test").is_err());
    input.draft.gaps[0].gap = "\u{1}".repeat(BYTE_LIMIT / 6);
    assert!(crate::connector_reconstruction::compose(&e, &input, "app-test").is_err());
    let file = r.root.join(&bound.relative_path);
    let mut padded = fs::read(&file).unwrap();
    padded.push(b' ');
    fs::write(file, padded).unwrap();
    let read = store.discover();
    assert!(read.accounts.is_empty());
    assert!(read
        .issues
        .iter()
        .any(|x| x.detail.contains("acquisition already occurred")));
    let mut forged = e;
    let a = &mut forged.anchors[0];
    a["text"] = json!("forged\n");
    a["sha256"] = json!(crate::util::sha256_hex(b"forged\n"));
    input.draft.gaps.clear();
    assert!(crate::connector_reconstruction::compose(&forged, &input, "app-test").is_err());
}
#[test]
fn connector_reconstruction_prepublication_refusals_and_atomic_stale_freeze() {
    for cause in ["root", "duplicate", "incomplete", "reread", "cancel"] {
        let (r, s, i) = prepared();
        let input = reconstruction_input(&s, i);
        let reg = Mutex::new(Registry::default());
        let frozen =
            crate::connector_reconstruction::prepare(&reg, &s, input.clone(), &r.root).unwrap();
        let (t, g) = current_draft(&frozen);
        let moved = r.root.with_extension("moved");
        match cause {
            "root" => {
                fs::rename(&r.root, &moved).unwrap();
                fs::create_dir(&r.root).unwrap();
            }
            "duplicate" => {
                ProjectRouteStore::open(&r.root)
                    .unwrap()
                    .write(&frozen["entries"][0]["draft"]["account"])
                    .unwrap();
            }
            "incomplete" => fs::write(r.root.join(".chirality"), b"not directory").unwrap(),
            "reread" => {
                connector_source::select(
                    &s,
                    &input.draft.session_token,
                    &input.draft.generation,
                    || Ok(Some(r.root.join("literal [*].txt"))),
                )
                .unwrap();
            }
            _ => {
                reg.lock().unwrap().cancel(t, g).unwrap();
            }
        }
        let result = super::registry::publish_with(&reg, &s, t, g, &r.root, |_, _| {
            panic!("refused path called writer")
        })
        .unwrap();
        assert!(matches!(
            result["entries"][0]["status"].as_str(),
            Some("refused" | "cancelled")
        ));
        if cause == "root" {
            fs::remove_dir(&r.root).unwrap();
            fs::rename(&moved, &r.root).unwrap();
        }
    }
    let (r, s, i) = prepared();
    let input = reconstruction_input(&s, i);
    let reg = Mutex::new(Registry::default());
    let failed = super::registry::prepare_composed(
        &reg,
        &s,
        input.draft.clone(),
        &r.root,
        || {
            connector_source::select(
                &s,
                &input.draft.session_token,
                &input.draft.generation,
                || Ok(None),
            )
            .unwrap();
        },
        |e, _, recorder| crate::connector_reconstruction::compose(e, &input, recorder),
    );
    assert!(failed.is_err());
    assert_eq!(reg.lock().unwrap().view()["used"], 0);
}

// Actual constructed Git -> injected selection -> immutable draft -> real publication.
// This helper does not mint a published entry or reconstruct custody from JSON.
pub(crate) fn published_fixture(
    version: &str,
) -> (Repo, Mutex<Session>, Mutex<Registry>, String, String) {
    let (r, s, i) = prepared();
    let registry = Mutex::new(Registry::default());
    let v = if version == "0.4" {
        crate::connector_reconstruction::prepare(
            &registry,
            &s,
            reconstruction_input(&s, i),
            &r.root,
        )
        .unwrap()
    } else {
        prepare(&registry, &s, i, &r.root).unwrap()
    };
    let (t, g) = current_draft(&v);
    let (t, g) = (t.to_owned(), g.to_owned());
    let result = publish(&registry, &s, &t, &g, &r.root).unwrap();
    assert_eq!(result["entries"][0]["status"], "published");
    (r, s, registry, t, g)
}
pub(crate) fn direct_account() -> Value {
    let (_r, s, i) = prepared();
    account(&s, &i)
}
#[test]
fn connector_materialization_recheck_actual_publications_survive_source_close_without_mutating_outcome(
) {
    for version in ["0.3", "0.4"] {
        let (r, s, reg, t, g) = published_fixture(version);
        let original = reg.lock().unwrap().view();
        *s.lock().unwrap() = Session::default();
        let result = recheck(&reg, &t, &g, || Ok(r.root.clone())).unwrap();
        assert_eq!(result["inspection"]["status"], "current_match");
        assert_eq!(result["inspection"]["observed"]["formatVersion"], version);
        assert_eq!(reg.lock().unwrap().view(), original);
        assert_eq!(reg.lock().unwrap().test_resources().0, 1);
        assert_eq!(reg.lock().unwrap().test_resources().2, 0);
        assert_eq!(
            recheck(&reg, &t, "forged", || Ok(r.root.clone())).unwrap_err()["kind"],
            "invalid_token"
        );
        reg.lock().unwrap().test_forget_published(&t);
        assert_eq!(
            recheck(&reg, &t, &g, || Ok(r.root.clone())).unwrap_err()["kind"],
            "unavailable"
        );
    }
}
#[test]
fn connector_materialization_recheck_offlock_busy_entry_cut_and_safe_unwind() {
    let (r, _s, reg, t, g) = published_fixture("0.3");
    let result = super::registry::recheck_using(
        &reg,
        &t,
        &g,
        || Ok(r.root.clone()),
        |store, binding, path| {
            assert!(reg.try_lock().is_ok(), "I/O does not hold registry mutex");
            assert_eq!(
                recheck(&reg, &t, &g, || Ok(r.root.clone())).unwrap_err()["kind"],
                "busy"
            );
            store.inspect_published(binding, path)
        },
    )
    .unwrap();
    assert_eq!(result["inspection"]["status"], "current_match");
    let stale = super::registry::recheck_using(
        &reg,
        &t,
        &g,
        || Ok(r.root.clone()),
        |store, binding, path| {
            reg.lock().unwrap().test_change_entry_cut(&t);
            store.inspect_published(binding, path)
        },
    )
    .unwrap_err();
    assert_eq!(stale["kind"], "stale");
    let panic = std::panic::catch_unwind(std::panic::AssertUnwindSafe(|| {
        super::registry::recheck_using(
            &reg,
            &t,
            &g,
            || Ok(r.root.clone()),
            |_, _, _| panic!("injected inspection unwind"),
        )
    }));
    assert!(panic.is_err());
    assert_eq!(reg.lock().unwrap().test_lease(), None);
    let newer = std::cell::Cell::new(0);
    let stale = super::registry::recheck_using(
        &reg,
        &t,
        &g,
        || Ok(r.root.clone()),
        |_, _, _| {
            newer.set(reg.lock().unwrap().test_replace_lease());
            json!({"status":"current_match"})
        },
    )
    .unwrap_err();
    assert_eq!(stale["kind"], "stale");
    assert_eq!(
        reg.lock().unwrap().test_lease(),
        Some(newer.get()),
        "old Drop must not clear newer lease"
    );
}
#[test]
fn connector_materialization_recheck_project_change_discards_completed_observation() {
    let (r, _s, reg, t, g) = published_fixture("0.3");
    let mut calls = 0;
    let result = super::registry::recheck_using(
        &reg,
        &t,
        &g,
        || {
            calls += 1;
            Ok(if calls == 1 {
                r.root.clone()
            } else {
                r.root.join("different")
            })
        },
        |store, binding, path| store.inspect_published(binding, path),
    )
    .unwrap_err();
    assert_eq!(result["kind"], "stale");
    assert_eq!(reg.lock().unwrap().test_lease(), None);
    assert_eq!(
        recheck(&reg, &t, &g, || Ok(r.root.clone())).unwrap()["inspection"]["status"],
        "current_match"
    );
}

#[test]
fn connector_materialization_recheck_no_custody_for_prepared_or_uncertain_and_original_attempt_unchanged(
) {
    let (r, s, i) = prepared();
    let reg = Mutex::new(Registry::default());
    let v = prepare(&reg, &s, i, &r.root).unwrap();
    let (t, g) = current_draft(&v);
    assert_eq!(
        recheck(&reg, t, g, || Ok(r.root.clone())).unwrap_err()["kind"],
        "unavailable"
    );
    let v = super::registry::publish_with(&reg, &s, t, g, &r.root, |store, a| {
        store.test_write_uncertain(a)
    })
    .unwrap();
    assert_eq!(v["entries"][0]["status"], "uncertain");
    assert_eq!(
        recheck(&reg, t, g, || Ok(r.root.clone())).unwrap_err()["kind"],
        "unavailable"
    );
    assert_eq!(reg.lock().unwrap().view(), v);
    assert_eq!(reg.lock().unwrap().test_resources().0, 0);
}
#[test]
fn connector_materialization_recheck_successful_write_installation_failure_preserves_exceptional_result(
) {
    let (r, s, i) = prepared();
    let reg = Mutex::new(Registry::default());
    let v = prepare(&reg, &s, i, &r.root).unwrap();
    let (t, g) = current_draft(&v);
    let result = super::registry::publish_with(&reg, &s, t, g, &r.root, |store, a| {
        let binding = store.write(a)?;
        let _ = std::panic::catch_unwind(std::panic::AssertUnwindSafe(|| {
            let _guard = reg.lock().unwrap();
            panic!("injected installation poison");
        }));
        Ok(binding)
    })
    .unwrap_err();
    assert!(
        result.contains("published"),
        "actual result retained: {result}"
    );
    assert!(result.contains("sha256"));
    assert_eq!(
        recheck(&reg, t, g, || Ok(r.root.clone())).unwrap_err()["kind"],
        "unavailable"
    );
    assert_eq!(reg.lock().err().unwrap().into_inner().test_resources().0, 0);
}
#[test]
fn connector_materialization_recheck_sixty_four_successes_retain_bounded_roots_without_payloads() {
    let (r, s, mut input) = prepared_layout(true);
    input.sources.clear();
    input.interpretations.clear();
    let reg = Mutex::new(Registry::default());
    let mut first = None;
    for n in 0..64 {
        let v = prepare(&reg, &s, input.clone(), &r.root).unwrap();
        let (t, g) = current_draft(&v);
        if n == 0 {
            first = Some((t.to_owned(), g.to_owned()));
        }
        let v = publish(&reg, &s, t, g, &r.root).unwrap();
        assert!(v["entries"]
            .as_array()
            .unwrap()
            .iter()
            .all(|e| e["status"] == "published"));
    }
    let (t, g) = first.unwrap();
    let before = reg.lock().unwrap().view();
    let (resources, metadata, payload) = reg.lock().unwrap().test_resources();
    assert_eq!(resources, 64);
    assert_eq!(payload, 0);
    println!("retained typed custody explicit allocation capacities: {metadata} bytes, {resources} root Files; excludes allocator bookkeeping/registry outcomes/other App state");
    assert!(prepare(&reg, &s, input, &r.root)
        .unwrap_err()
        .contains("capacity"));
    assert_eq!(
        recheck(&reg, &t, &g, || Ok(r.root.clone())).unwrap()["inspection"]["status"],
        "current_match"
    );
    assert_eq!(reg.lock().unwrap().view(), before);
}
#[test]
fn connector_materialization_recheck_unrelated_entry_change_does_not_stale_original() {
    let (r, s, mut input) = prepared_layout(true);
    input.sources.clear();
    input.interpretations.clear();
    let reg = Mutex::new(Registry::default());
    let v = prepare(&reg, &s, input.clone(), &r.root).unwrap();
    let (t, g) = current_draft(&v);
    publish(&reg, &s, t, g, &r.root).unwrap();
    let other = prepare(&reg, &s, input, &r.root).unwrap();
    let (ot, og) = current_draft(&other);
    let result=super::registry::recheck_using(&reg,t,g,||Ok(r.root.clone()),|store,binding,path|{let payload_bytes=reg.lock().unwrap().test_resources().2;assert!(payload_bytes>0,"a separate frozen payload coexists with inspection");let result=store.inspect_published(binding,path);println!("simultaneous frozen payload capacity: {payload_bytes}; direct read capped at1MiB+sentinel; parsed/schema allocations additional, not a total bound");reg.lock().unwrap().cancel(ot,og).unwrap();result}).unwrap();
    assert_eq!(result["inspection"]["status"], "current_match");
}

#[test]
fn connector_materialization_recheck_concurrent_backend_request_does_not_queue_or_read() {
    let (r, _s, reg, t, g) = published_fixture("0.3");
    let start = std::sync::Barrier::new(2);
    let finish = std::sync::Barrier::new(2);
    std::thread::scope(|scope| {
        let first = scope.spawn(|| {
            super::registry::recheck_using(
                &reg,
                &t,
                &g,
                || Ok(r.root.clone()),
                |store, binding, path| {
                    start.wait();
                    finish.wait();
                    store.inspect_published(binding, path)
                },
            )
        });
        start.wait();
        let second = super::registry::recheck_using(
            &reg,
            &t,
            &g,
            || Ok(r.root.clone()),
            |_, _, _| panic!("second inspection must never run"),
        );
        assert_eq!(second.unwrap_err()["kind"], "busy");
        finish.wait();
        assert_eq!(
            first.join().unwrap().unwrap()["inspection"]["status"],
            "current_match"
        );
    });
    let before = reg.lock().unwrap().view();
    fs::write(
        r.root.join("literal [*].txt"),
        "Changed unrelated working source",
    )
    .unwrap();
    fs::write(
        r.root.join(".git/config"),
        "changed invalid Git config; no Git operation allowed",
    )
    .unwrap();
    for _ in 0..2 {
        assert_eq!(
            recheck(&reg, &t, &g, || Ok(r.root.clone())).unwrap()["inspection"]["status"],
            "current_match"
        );
    }
    assert_eq!(reg.lock().unwrap().view(), before);
}
