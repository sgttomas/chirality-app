use super::*;
use crate::{
    connector_route_view,
    recovery::{AppProjectSource, ExplicitAppProjectContext},
};
use std::{
    fs,
    os::unix::fs::{symlink, MetadataExt},
    path::PathBuf,
};
struct Fixture {
    root: PathBuf,
    account: Value,
    base: BoundReference,
    path: PathBuf,
}
impl Drop for Fixture {
    fn drop(&mut self) {
        let _ = fs::remove_dir_all(&self.root);
    }
}
impl Fixture {
    fn new() -> Self {
        let root =
            std::env::temp_dir().join(format!("ao-cold-{}", crate::util::opaque_id("").unwrap()));
        fs::create_dir(&root).unwrap();
        let store = ProjectRouteStore::open(&root).unwrap();
        let base: Value = serde_json::from_str(include_str!(
            "../resources/connector_route/record_reconstruction_v04.fixture.json"
        ))
        .unwrap();
        let bound = store.write(&base).unwrap();
        let bytes = fs::read(root.join(&bound.relative_path)).unwrap();
        let mut a: Value = serde_json::from_str::<Value>(include_str!(
            "../resources/connector_route/contribution_evidence_v01.fixture.json"
        ))
        .unwrap()["account"]
            .clone();
        for k in ["review", "plan", "integration", "integration_attempt"] {
            a[k] = Value::Null;
        }
        let id = store.project_identity();
        a["base_account"]["relative_path"] = json!(bound.relative_path);
        a["base_account"]["sha256"] = json!(bound.sha256);
        a["base_account"]["byte_length"] = json!(bytes.len());
        a["base_account"]["project_identity"] =
            json!({"device":id.device.to_string(),"inode":id.inode.to_string()});
        let mut body: Value =
            serde_json::from_str(a["answer"]["artifact"]["text"].as_str().unwrap()).unwrap();
        body["account_sha256"] = a["base_account"]["sha256"].clone();
        Self::body(&mut a, body);
        a["gaps"].as_array_mut().unwrap().push(json!({"gap":"Manager review and integration outstanding","effect":"No reviewed or integrated answer","responsibility":"manager"}));
        let path = root
            .join(DIRECTORY)
            .join("22222222-2222-4222-8222-222222222222.json");
        let f = Self {
            root,
            account: a,
            base: bound,
            path,
        };
        f.save();
        f
    }
    fn body(a: &mut Value, v: Value) {
        let text = serde_json::to_string(&v).unwrap();
        let sha = crate::util::sha256_hex(text.as_bytes());
        a["answer"]["artifact"] = json!({"text":text,"byte_length":text.len(),"sha256":sha});
        a["answer"]["receipt"]["content_sha256"] = json!(sha);
    }
    fn save(&self) {
        fs::write(&self.path, serde_json::to_vec(&self.account).unwrap()).unwrap();
    }
    fn read(&self) -> Discovery {
        ProjectRouteStore::open(&self.root).unwrap().discover()
    }
    fn refused(&self, kind: ErrorKind) {
        let d = self.read();
        assert!(!d
            .accounts
            .iter()
            .any(|a| a.reference.format_version == "0.5"));
        assert!(d.issues.iter().any(|i| i.kind == kind), "{:?}", d.issues);
    }
}
fn metadata(p: &std::path::Path) -> (u64, u64, u64, i64, i64, i64, i64) {
    let m = fs::metadata(p).unwrap();
    (
        m.dev(),
        m.ino(),
        m.len(),
        m.mtime(),
        m.mtime_nsec(),
        m.ctime(),
        m.ctime_nsec(),
    )
}
#[test]
fn connector_answer_only_actual_read_projection_and_write_barrier() {
    let mut f = Fixture::new();
    let mut body: Value =
        serde_json::from_str(f.account["answer"]["artifact"]["text"].as_str().unwrap()).unwrap();
    body["answer_text"] =
        json!("<script>Recorded answer</script> — no truth or actual authorship proved");
    Fixture::body(&mut f.account, body);
    f.account["answer"]["receipt"]["generation"]["spawnCounter"] = json!("900719925474099312345");
    f.save();
    let before = (
        metadata(&f.root),
        metadata(&f.root.join(DIRECTORY)),
        metadata(&f.path),
        metadata(&f.root.join(&f.base.relative_path)),
    );
    assert_eq!(
        validate_account(&f.account).unwrap_err().kind,
        ErrorKind::UnsupportedFormat
    );
    assert_eq!(
        ProjectRouteStore::open(&f.root)
            .unwrap()
            .write(&f.account)
            .unwrap_err()
            .kind,
        ErrorKind::UnsupportedFormat
    );
    let context = ExplicitAppProjectContext::known(
        f.root.to_str().unwrap(),
        AppProjectSource::ConfiguredDirectory,
    )
    .unwrap();
    let view = connector_route_view::read(Some(&f.root), &context, None);
    assert_eq!(view["accounts"].as_array().unwrap().len(), 2, "{view}");
    let a = view["accounts"]
        .as_array()
        .unwrap()
        .iter()
        .find(|a| a["formatVersion"] == "0.5")
        .unwrap();
    assert_eq!(a["answerOnly"]["answer"]["question_id"], "Q1");
    assert!(a["answerOnly"]["limit"]
        .as_str()
        .unwrap()
        .contains("do not authenticate"));
    let fresh = connector_route_view::read(Some(&f.root), &context, None);
    assert_eq!(fresh, view);
    let d = f.read();
    let reference = d
        .accounts
        .iter()
        .find(|a| a.reference.format_version == "0.5")
        .unwrap()
        .reference
        .clone();
    assert!(ProjectRouteStore::open(&f.root)
        .unwrap()
        .resolve(&reference)
        .is_ok());
    assert_eq!(
        before,
        (
            metadata(&f.root),
            metadata(&f.root.join(DIRECTORY)),
            metadata(&f.path),
            metadata(&f.root.join(&f.base.relative_path))
        )
    );
    if let Some(path) = std::env::var_os("CHIRALITY_AO_VIEW_EXPORT") {
        fs::write(path, serde_json::to_vec(&view).unwrap()).unwrap();
    }
}
#[test]
fn connector_answer_only_full_and_each_unadopted_subset_refused() {
    let full: Value = serde_json::from_str::<Value>(include_str!(
        "../resources/connector_route/contribution_evidence_v01.fixture.json"
    ))
    .unwrap()["account"]
        .clone();
    crate::connector_answer_only::shape(&full).unwrap();
    for key in [
        "all",
        "review",
        "plan",
        "integration",
        "integration_attempt",
    ] {
        let mut f = Fixture::new();
        if key == "all" {
            for k in ["review", "plan", "integration"] {
                f.account[k] = full[k].clone();
            }
        } else if key == "integration_attempt" {
            f.account[key] = json!({"request_reference":"recorded","target_path":"workgraph.md","standing":"uncertain","detail":"Outcome unknown"});
        } else {
            f.account[key] = full[key].clone();
        }
        crate::connector_answer_only::shape(&f.account).unwrap();
        f.save();
        f.refused(ErrorKind::UnsupportedSubset);
    }
}
#[test]
fn connector_answer_only_base_negatives_and_race() {
    for kind in [
        "hash",
        "length",
        "id",
        "question",
        "root",
        "missing",
        "link",
        "oversize",
        "semantic",
        "duplicate",
        "race",
    ] {
        let mut f = Fixture::new();
        let path = f.root.join(&f.base.relative_path);
        match kind {
            "hash" => f.account["base_account"]["sha256"] = json!("0".repeat(64)),
            "length" => f.account["base_account"]["byte_length"] = json!(1),
            "id" => f.account["base_account"]["account_id"] = json!("ra:other"),
            "question" => f.account["question_id"] = json!("other"),
            "root" => f.account["base_account"]["project_identity"]["inode"] = json!("0"),
            "missing" => {
                fs::rename(&path, path.with_extension("moved")).unwrap();
            }
            "link" => {
                let moved = path.with_extension("moved");
                fs::rename(&path, &moved).unwrap();
                symlink(moved, &path).unwrap();
            }
            "oversize" => {
                let mut b = fs::read(&path).unwrap();
                b.resize(crate::connector_answer_only::LIMIT + 1, b' ');
                fs::write(&path, b).unwrap();
            }
            "semantic" => {
                let mut b: Value = serde_json::from_slice(&fs::read(&path).unwrap()).unwrap();
                b["facts"][0]["statement"] = json!("forged");
                fs::write(&path, serde_json::to_vec(&b).unwrap()).unwrap();
            }
            "duplicate" => {
                fs::copy(
                    &path,
                    f.root
                        .join(DIRECTORY)
                        .join("33333333-3333-4333-8333-333333333333.json"),
                )
                .unwrap();
            }
            _ => {}
        }
        f.save();
        if kind == "race" {
            let store = ProjectRouteStore::open(&f.root).unwrap();
            let d = store.discover_using(None, |_| {
                let bytes = fs::read(&path).unwrap();
                fs::rename(&path, path.with_extension("old")).unwrap();
                fs::write(&path, bytes).unwrap();
            });
            assert!(!d
                .accounts
                .iter()
                .any(|a| a.reference.format_version == "0.5"));
            assert!(d
                .issues
                .iter()
                .any(|i| i.kind == ErrorKind::UnresolvedReference));
        } else {
            f.refused(if kind == "question" {
                ErrorKind::InvalidAccount
            } else {
                ErrorKind::UnresolvedReference
            });
        }
    }
}
#[test]
fn connector_answer_only_strict_messages_receipts_and_reference_negatives() {
    for kind in [
        "outer-duplicate",
        "embedded-duplicate",
        "base-duplicate",
        "whitespace",
        "length",
        "gap",
        "unknown-ref",
        "duplicate-ref",
        "duplicate-claim",
        "method",
        "source-identity",
        "source-position",
        "generation",
        "unknown-message",
        "message-review",
        "unknown-version",
    ] {
        let mut f = Fixture::new();
        let mut body: Value =
            serde_json::from_str(f.account["answer"]["artifact"]["text"].as_str().unwrap())
                .unwrap();
        match kind {
            "outer-duplicate" => {
                let b = serde_json::to_string(&f.account).unwrap();
                fs::write(
                    &f.path,
                    format!("{},\"question_id\":\"Q1\"}}", &b[..b.len() - 1]),
                )
                .unwrap();
                f.refused(ErrorKind::InvalidAccount);
                continue;
            }
            "embedded-duplicate" => {
                let text = f.account["answer"]["artifact"]["text"].as_str().unwrap();
                let text = format!("{},\"kind\":\"answer\"}}", &text[..text.len() - 1]);
                let sha = crate::util::sha256_hex(text.as_bytes());
                f.account["answer"]["artifact"] =
                    json!({"text":text,"byte_length":text.len(),"sha256":sha});
                f.account["answer"]["receipt"]["content_sha256"] = json!(sha);
            }
            "base-duplicate" => {
                let path = f.root.join(&f.base.relative_path);
                let b = fs::read_to_string(&path).unwrap();
                let bytes = format!("{},\"formatVersion\":\"0.4\"}}", &b[..b.len() - 1]);
                fs::write(path, &bytes).unwrap();
                f.account["base_account"]["byte_length"] = json!(bytes.len());
                f.account["base_account"]["sha256"] =
                    json!(crate::util::sha256_hex(bytes.as_bytes()));
            }
            "whitespace" => {
                f.account["answer"]["artifact"]["text"] = json!(format!(
                    " {}",
                    f.account["answer"]["artifact"]["text"].as_str().unwrap()
                ))
            }
            "length" => f.account["answer"]["artifact"]["byte_length"] = json!(1),
            "gap" => {
                body["retained_gap_pointers"] = json!([]);
                Fixture::body(&mut f.account, body);
            }
            "unknown-ref" => {
                body["claims"][0]["fact_ids"] = json!(["unknown"]);
                Fixture::body(&mut f.account, body);
            }
            "duplicate-ref" => {
                body["claims"][0]["fact_ids"] = json!(["f-at", "f-at"]);
                Fixture::body(&mut f.account, body);
            }
            "duplicate-claim" => {
                let mut other = body["claims"][0].clone();
                other["statement"] = json!("Different text, same ID");
                body["claims"].as_array_mut().unwrap().push(other);
                Fixture::body(&mut f.account, body);
            }
            "method" => {
                f.account["answer"]["receipt"]["sources"][0]["method"] =
                    json!("sha256:original_rpc_wire")
            }
            "source-identity" => {
                f.account["answer"]["receipt"]["sources"][1]["identity"] =
                    f.account["answer"]["receipt"]["sources"][0]["identity"].clone()
            }
            "source-position" => {
                f.account["answer"]["receipt"]["response_receipt_position"] =
                    f.account["answer"]["receipt"]["item_receipt_position"].clone()
            }
            "generation" => f.account["answer"]["receipt"]["generation"]["home"] = json!("foreign"),
            "unknown-message" => {
                body["formatVersion"] = json!("0.9");
                Fixture::body(&mut f.account, body);
            }
            "message-review" => {
                body["kind"] = json!("manager_review");
                Fixture::body(&mut f.account, body);
            }
            _ => f.account["formatVersion"] = json!("0.6"),
        }
        f.save();
        f.refused(if kind == "base-duplicate" {
            ErrorKind::UnresolvedReference
        } else if kind == "unknown-version" {
            ErrorKind::UnsupportedFormat
        } else {
            ErrorKind::InvalidAccount
        });
    }
}
#[test]
fn connector_answer_only_caps_growth_and_changed_known_version() {
    let f = Fixture::new();
    let mut raw = fs::read(&f.path).unwrap();
    raw.resize(crate::connector_answer_only::LIMIT, b' ');
    fs::write(&f.path, &raw).unwrap();
    let d = f.read();
    let a = d
        .accounts
        .iter()
        .find(|a| a.reference.format_version == "0.5")
        .unwrap();
    let held = a.reference.clone();
    assert_eq!(a.byte_length, crate::connector_answer_only::LIMIT);
    raw.push(b' ');
    fs::write(&f.path, &raw).unwrap();
    f.refused(ErrorKind::InvalidAccount);
    let store = ProjectRouteStore::open(&f.root).unwrap();
    assert!(store
        .resolve(&held)
        .unwrap_err()
        .detail
        .contains("sentinel"));
    f.save();
    let dir = fs::File::open(f.root.join(DIRECTORY)).unwrap();
    let name = f.path.file_name().unwrap().to_str().unwrap();
    let err = platform::read_account_mode(
        &dir,
        name,
        &held.relative_path,
        held.directories.clone(),
        Some("0.5"),
        || {
            use std::io::Write;
            let mut file = fs::OpenOptions::new().append(true).open(&f.path).unwrap();
            file.write_all(&vec![b' '; crate::connector_answer_only::LIMIT])
                .unwrap();
        },
    )
    .unwrap_err();
    assert!(err.detail.contains("sentinel"), "{err}");
    let base = f.root.join(&f.base.relative_path);
    let name = base.file_name().unwrap().to_str().unwrap();
    let err = platform::read_account_mode(
        &dir,
        name,
        &f.base.relative_path,
        f.base.directories.clone(),
        Some("0.4"),
        || {
            use std::io::Write;
            fs::OpenOptions::new()
                .append(true)
                .open(&base)
                .unwrap()
                .write_all(&vec![b' '; crate::connector_answer_only::LIMIT])
                .unwrap();
        },
    )
    .unwrap_err();
    assert!(err.detail.contains("sentinel"));
    let mut f = Fixture::new();
    let held = f
        .read()
        .accounts
        .into_iter()
        .find(|a| a.reference.format_version == "0.5")
        .unwrap()
        .reference;
    f.account["formatVersion"] = json!("0.4");
    f.save();
    assert!(ProjectRouteStore::open(&f.root)
        .unwrap()
        .resolve(&held)
        .unwrap_err()
        .detail
        .contains("version changed"));
}
#[test]
fn connector_answer_only_fabricated_historical_receipt_stays_unverified() {
    let mut f = Fixture::new();
    // JSON Schema integers may use integral decimal spelling; these lengths are <=1MiB.
    f.account["base_account"]["byte_length"]=json!(f.account["base_account"]["byte_length"].as_u64().unwrap() as f64);
    f.account["answer"]["artifact"]["byte_length"]=json!(f.account["answer"]["artifact"]["byte_length"].as_u64().unwrap() as f64);

    f.account["answer"]["receipt"]["request_reference"] = json!("invented-recorded-request");
    f.account["answer"]["receipt"]["sources"][0]["identity"] = json!("invented-recorded-request");
    f.account["answer"]["receipt"]["liveness_at_recording"] =
        json!("historical_after_source_close");
    for (key, value) in [
        ("dispatch_receipt_floor", "900719925474099300000"),
        ("item_receipt_position", "900719925474099300001"),
        ("terminal_receipt_position", "900719925474099300002"),
        ("response_receipt_position", "900719925474099300003"),
    ] {
        f.account["answer"]["receipt"][key] = json!(value);
    }
    f.account["known_conflicts"] = json!([{"reference":"another-recorded-answer","sha256":"0".repeat(64),"effect":"Unresolved conflict; no winner"}]);
    f.save();
    let d = f.read();
    let a = d
        .accounts
        .iter()
        .find(|a| a.reference.format_version == "0.5")
        .unwrap();
    assert!(a.answer_only.as_ref().unwrap()["limit"]
        .as_str()
        .unwrap()
        .contains("do not authenticate"));
    assert_eq!(
        a.account["answer"]["receipt"]["item_receipt_position"],
        "900719925474099300001"
    );
    assert_eq!(a.account["known_conflicts"].as_array().unwrap().len(), 1);
}
#[test]
fn connector_answer_only_positive_message02_review_is_not_downgraded() {
    let message: Value = serde_json::from_str(include_str!(
        "../../tests/fixtures/contribution_content_review_v02.fixture.json"
    ))
    .unwrap();
    let schema: Value = serde_json::from_str(include_str!(
        "../../tests/fixtures/connector.contribution-message.v0.2.schema.json"
    ))
    .unwrap();
    jsonschema::validator_for(&schema)
        .unwrap()
        .validate(&message)
        .unwrap();
    let mut f = Fixture::new();
    Fixture::body(&mut f.account, message.clone());
    f.save();
    f.refused(ErrorKind::InvalidAccount);
    let mut f = Fixture::new();
    let full: Value = serde_json::from_str::<Value>(include_str!(
        "../resources/connector_route/contribution_evidence_v01.fixture.json"
    ))
    .unwrap()["account"]
        .clone();
    f.account["review"] = full["review"].clone();
    let text = serde_json::to_string(&message).unwrap();
    let sha = crate::util::sha256_hex(text.as_bytes());
    f.account["review"]["artifact"] = json!({"text":text,"byte_length":text.len(),"sha256":sha});
    f.account["review"]["receipt"]["content_sha256"] = json!(sha);
    crate::connector_answer_only::shape(&f.account).unwrap();
    f.save();
    f.refused(ErrorKind::UnsupportedSubset);
}
