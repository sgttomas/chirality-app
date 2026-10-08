//! C3-U-READ-01: inspect cold recorded claims in the host's explicit project.
//! No source reading, publication, held-reference resolution, or actor act.
use crate::{
    attachments,
    connector_route_store::{Discovery, ProjectRouteStore},
    recovery::ExplicitAppProjectContext,
};
use serde_json::{json, Value};
use std::path::Path;

pub fn availability(
    workspace: Option<&Path>,
    context: &ExplicitAppProjectContext,
    limit: Option<&str>,
) -> Value {
    let refusal = if workspace.is_none() {
        Some(("no_project", "No explicit App project is associated."))
    } else if limit.is_some() {
        Some((
            "invalid_association",
            "The App project association could not be established.",
        ))
    } else if context.reference().is_none() {
        Some((
            "unknown_association",
            "The workspace has no known explicit App project association.",
        ))
    } else if !workspace.unwrap().is_absolute() {
        Some((
            "invalid_association",
            "The associated project path is not absolute.",
        ))
    } else {
        let path = workspace.unwrap();
        let reference = path
            .to_str()
            .map(str::to_owned)
            .unwrap_or_else(|| attachments::native_path_identity(path).to_string());
        (context.reference() != Some(reference.as_str())).then_some((
            "association_mismatch",
            "The workspace and explicit App project reference disagree.",
        ))
    };
    match refusal {
        Some((status, reason)) => {
            json!({"enabled":false,"status":status,"reason":reason,"detail":limit})
        }
        None => {
            json!({"enabled":true,"status":"available","projectReference":context.reference(),"reason":"Explicit project association only; no actor authority inferred."})
        }
    }
}

pub fn read(
    workspace: Option<&Path>,
    context: &ExplicitAppProjectContext,
    limit: Option<&str>,
) -> Value {
    let access = availability(workspace, context, limit);
    if access["enabled"] != true {
        return json!({"status":"unavailable","availability":access});
    }
    match ProjectRouteStore::open(workspace.unwrap()) {
        Ok(store) => project(store.discover()),
        Err(error) => json!({"status":"project_open_failed","error":error}),
    }
}

fn project(discovery: Discovery) -> Value {
    // JSON text keeps every supported account field and u64 binding identity out
    // of JavaScript's numeric conversion. These strings are displayed, never run.
    let accounts: Vec<Value> = discovery.accounts.into_iter().map(|observed| json!({
        "relativePath":observed.reference.relative_path,
        "accountId":observed.reference.account_id,
        "formatVersion":observed.account["formatVersion"],
        "standing":observed.account.get("standing"),
        "draftSources":if observed.account["formatVersion"]=="0.3" {observed.account["sources"].clone()}else{Value::Null},
        "interpretations":observed.account.get("interpretations"),
        "questionText":observed.account["question"]["text"].as_str(),
        "gaps":observed.account["gaps"],
        "duties":observed.account["duties"],
        "bindingText":serde_json::to_string_pretty(&observed.reference).unwrap(),
        "accountText":serde_json::to_string_pretty(&observed.account).unwrap(),
        "sections":([("Question", "question"), ("Trigger", "trigger"), ("Sources and revisions", "sources"), ("Anchored facts", "facts"), ("Gaps, effects and responsibility", "gaps"), ("Supported, unsupported and prohibited conclusions", "conclusions"), ("Duties", "duties"), ("Recorder", "recorder"), ("Written time", "written_at"), ("Time provenance", "written_at_source")].iter().chain(if observed.account["formatVersion"]=="0.3" {[("Draft standing","standing"),("Compact evidence receipt and limits","evidence"),("Unreviewed caller interpretations","interpretations")].as_slice()}else{&[]}).map(|(label,key)|json!({"label":label,"text":observed.account.get(*key).map(|value|serde_json::to_string_pretty(value).unwrap()).unwrap_or_else(||"Not recorded".into())})).collect::<Vec<_>>()),
        "sourceCount":observed.account["sources"].as_array().map_or(0, Vec::len),
    })).collect();
    json!({"status":"observed","projectDisplay":discovery.resolved_project.to_string_lossy(),
        "projectIdentityText":attachments::native_path_identity(&discovery.resolved_project).to_string(),
        "directoryAbsent":discovery.directory_absent,"enumerationComplete":discovery.enumeration_complete,
        "accounts":accounts,"issues":discovery.issues,"byAccountId":discovery.by_account_id})
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::recovery::AppProjectSource;
    use std::fs;
    fn known(path: &Path) -> ExplicitAppProjectContext {
        ExplicitAppProjectContext::known(
            &path
                .to_str()
                .map(str::to_owned)
                .unwrap_or_else(|| attachments::native_path_identity(path).to_string()),
            AppProjectSource::ConfiguredDirectory,
        )
        .unwrap()
    }
    #[test]
    fn connector_route_view_refuses_unknown_mismatched_and_missing_associations() {
        let path = Path::new("/unopened-fixture-project");
        assert_eq!(
            availability(None, &known(path), None)["status"],
            "no_project"
        );
        assert_eq!(
            availability(Some(path), &ExplicitAppProjectContext::unknown(), None)["status"],
            "unknown_association"
        );
        assert_eq!(
            availability(Some(path), &known(Path::new("/different-fixture")), None)["status"],
            "association_mismatch"
        );
        assert_eq!(
            availability(Some(path), &known(path), Some("invalid"))["status"],
            "invalid_association"
        );
        assert_eq!(
            availability(
                Some(Path::new("relative")),
                &known(Path::new("relative")),
                None
            )["status"],
            "invalid_association"
        );
        assert_eq!(
            read(Some(path), &known(path), None)["status"],
            "project_open_failed"
        );
    }
    #[test]
    fn connector_route_view_absent_directory_read_creates_nothing() {
        let path = std::env::temp_dir().join(crate::util::opaque_id("route-view-test-").unwrap());
        fs::create_dir(&path).unwrap();
        let context = known(&path);
        let result = read(Some(&path), &context, None);
        assert_eq!(result["status"], "observed");
        assert_eq!(result["directoryAbsent"], true);
        assert_eq!(result["enumerationComplete"], true);
        assert_eq!(fs::read_dir(&path).unwrap().count(), 0);
        fs::remove_dir(&path).unwrap();
    }
    #[test]
    fn connector_route_view_preserves_claims_duplicates_issues_and_files() {
        let path = std::env::temp_dir().join(crate::util::opaque_id("route-view-test-").unwrap());
        fs::create_dir(&path).unwrap();
        let store = ProjectRouteStore::open(&path).unwrap();
        let mut value: Value = serde_json::from_str(include_str!(
            "../../tests/fixtures/connector-route-source-walk.json"
        ))
        .unwrap();
        value["facts"][0]["data"] = json!({"integer":9007199254740993u64});
        let first = store.write(&value).unwrap();
        let second = store.write(&value).unwrap();
        let directory = path.join(".chirality/records/connectors/route-accounts");
        fs::write(
            directory.join("12345678-1234-4234-8234-123456789abc.json"),
            b"{broken",
        )
        .unwrap();
        fs::write(
            directory.join("12345678-1234-4234-8234-123456789abd.json"),
            br#"{"formatVersion":"future"}"#,
        )
        .unwrap();
        fn snapshot(directory: &Path) -> std::collections::BTreeMap<String, Vec<u8>> {
            fs::read_dir(directory)
                .unwrap()
                .map(|entry| {
                    let entry = entry.unwrap();
                    (
                        entry.file_name().to_str().unwrap().into(),
                        fs::read(entry.path()).unwrap(),
                    )
                })
                .collect()
        }
        let before = snapshot(&directory);
        let result = read(Some(&path), &known(&path), None);
        assert_eq!(snapshot(&directory), before);
        assert_eq!(result["accounts"].as_array().unwrap().len(), 2);
        assert_eq!(
            result["byAccountId"][value["account_id"].as_str().unwrap()]
                .as_array()
                .unwrap()
                .len(),
            2
        );
        let text = result.to_string();
        for required in [
            "DuplicateIdentity",
            "InvalidAccount",
            "UnsupportedFormat",
            "9007199254740993",
            &first.relative_path,
            &second.relative_path,
        ] {
            assert!(text.contains(required), "{required}");
        }
        for account in result["accounts"].as_array().unwrap() {
            assert_eq!(
                serde_json::from_str::<Value>(account["accountText"].as_str().unwrap()).unwrap(),
                value
            );
            assert_eq!(account["questionText"], value["question"]["text"]);
        }
        let mut discovery = store.discover();
        discovery.enumeration_complete = false;
        assert_eq!(project(discovery)["enumerationComplete"], false);
        fs::remove_dir_all(&path).unwrap();
    }
    #[cfg(unix)]
    #[test]
    fn connector_route_view_lossless_nonunicode_association() {
        use std::os::unix::ffi::OsStringExt;
        let path =
            std::path::PathBuf::from(std::ffi::OsString::from_vec(b"/fixture-\xff".to_vec()));
        assert_eq!(
            availability(Some(&path), &known(&path), None)["enabled"],
            true
        );
    }
}
