//! Synthetic selection-port→production receiving→main-process memory checks.
//! Native picker/window interaction is not executed by these checks.
use chirality_app_v4_lib::runtime_session::{
    receive_external_selection, ExternalObservationSession,
};
use serde_json::{json, Value};
use std::path::{Path, PathBuf};
use std::sync::Mutex;
struct Scratch(PathBuf);
impl Scratch {
    fn new() -> Self {
        let root = std::env::temp_dir()
            .join(chirality_app_v4_lib::util::opaque_id("i4-integration-").unwrap());
        std::fs::create_dir(&root).unwrap();
        Self(root)
    }
    fn write(&self, name: &str, bytes: &[u8]) -> PathBuf {
        let path = self.0.join(name);
        std::fs::write(&path, bytes).unwrap();
        path
    }
}
impl Drop for Scratch {
    fn drop(&mut self) {
        std::fs::remove_dir_all(&self.0).unwrap();
    }
}
fn fixture(name: &str) -> Vec<u8> {
    std::fs::read(
        Path::new(env!("CARGO_MANIFEST_DIR"))
            .join("resources/catalog_adapter")
            .join(name),
    )
    .unwrap()
}
fn select(
    state: &Mutex<ExternalObservationSession>,
    catalog: &Path,
    read: &Path,
    counterpart: Option<&Path>,
) -> Value {
    receive_external_selection(
        state,
        |stage| {
            Ok(Some(match stage {
                "catalog" => catalog.to_path_buf(),
                "read" => read.to_path_buf(),
                _ => counterpart.unwrap().to_path_buf(),
            }))
        },
        || counterpart.is_some(),
    )
    .unwrap()
}
#[test]
fn complete_documents_path_identity_standing_and_missing_comparison_survive_main_memory_snapshot() {
    let scratch = Scratch::new();
    let catalog = scratch.write("catalog.json", &fixture("catalog.example-valid.json"));
    let mut read: Value =
        serde_json::from_slice(&fixture("read_result.example-valid.json")).unwrap();
    read["views"][0]["diagnostics"] = json!([{"diagnostic_identity":"synthetic:diag","severity":"warning","statement":"synthetic source limit","attachments":[{"attaches_to":"row","reference":"S-2"}]}]);
    let raw = serde_json::to_vec_pretty(&read).unwrap();
    let path = scratch.write("résultat-Δ.json", &raw);
    let state = Mutex::new(ExternalObservationSession::default());
    let received = select(&state, &catalog, &path, None);
    assert_eq!(received["selection"]["state"], "loaded");
    assert_eq!(
        received["selection"]["counterpartSelection"],
        "not-requested"
    );
    let observation = &received["observation"];
    assert_eq!(observation["read"]["originalDocument"], read);
    assert_eq!(observation["read"]["originalBytes"], json!(raw));
    assert_eq!(observation["read"]["displayPath"], path.to_str().unwrap());
    #[cfg(unix)]
    {
        use std::os::unix::ffi::OsStrExt;
        assert_eq!(
            observation["read"]["selectedPath"]["bytes"],
            json!(path.as_os_str().as_bytes())
        );
    }
    assert_eq!(observation["hostOrigin"], "unverified");
    assert_eq!(observation["qualification"], "not_established");
    assert_eq!(
        observation["currencyMeaning"],
        "as reported in this observation"
    );
    assert_eq!(observation["comparison"], "host_table_not_supplied");
    assert_eq!(observation["dispatch"], "none");
    // Source files changing after selection cannot change this memory snapshot.
    std::fs::write(path, b"{}").unwrap();
    assert_eq!(state.lock().unwrap().snapshot(), received);
}
#[test]
fn counterpart_comparison_and_cancelled_or_failed_replacement_leave_prior_supplied_bytes() {
    let scratch = Scratch::new();
    let catalog = scratch.write("catalog.json", &fixture("catalog.example-valid.json"));
    let raw = fixture("read_result.example-valid.json");
    let read = scratch.write("read.json", &raw);
    let counterpart = scratch.write("counterpart.json", &raw);
    let state = Mutex::new(ExternalObservationSession::default());
    let original = select(&state, &catalog, &read, Some(&counterpart));
    assert_eq!(
        original["observation"]["comparison"],
        "same_meaningful_supplied_content"
    );
    assert_eq!(
        original["observation"]["comparisonScope"],
        "supplied_documents_only"
    );
    for cancel in ["catalog", "read", "counterpart"] {
        let received = receive_external_selection(
            &state,
            |stage| {
                if stage == cancel {
                    Ok(None)
                } else {
                    Ok(Some(if stage == "catalog" {
                        catalog.clone()
                    } else {
                        read.clone()
                    }))
                }
            },
            || true,
        )
        .unwrap();
        assert_eq!(received["selection"]["state"], "cancelled");
        assert_eq!(received["selection"]["stage"], cancel);
        assert_eq!(received["selection"]["previousObservationRetained"], true);
        assert_eq!(received["observation"], original["observation"]);
    }
    assert!(receive_external_selection(
        &state,
        |_| Err("synthetic native selection failure".into()),
        || false
    )
    .is_err());
    let failed = state.lock().unwrap().snapshot();
    assert_eq!(failed["selection"]["state"], "selection-failed");
    assert_eq!(failed["observation"], original["observation"]);
}
#[test]
fn unavailable_nonunicode_selection_is_read_once_and_remains_tagged_with_display_limit() {
    let scratch = Scratch::new();
    let catalog = scratch.write("catalog.json", &fixture("catalog.example-valid.json"));
    #[cfg(unix)]
    let missing = {
        use std::os::unix::ffi::OsStringExt;
        scratch
            .0
            .join(std::ffi::OsString::from_vec(b"read-\xff.json".to_vec()))
    };
    #[cfg(not(unix))]
    let missing = scratch.0.join("missing.json");
    let state = Mutex::new(ExternalObservationSession::default());
    let received = select(&state, &catalog, &missing, None);
    let read = &received["observation"]["read"];
    assert_eq!(read["assessment"], "unavailable");
    assert!(read["originalDocument"].is_null());
    assert!(read["originalBytes"].is_null());
    assert!(read["reason"].is_string());
    #[cfg(unix)]
    {
        use std::os::unix::ffi::OsStrExt;
        assert_eq!(read["selectedPath"]["encoding"], "unix_bytes");
        assert_eq!(
            read["selectedPath"]["bytes"],
            json!(missing.as_os_str().as_bytes())
        );
        assert!(read["pathDisplayLimit"].as_str().unwrap().contains("lossy"));
    }
    serde_json::to_vec(&received).unwrap();
}
#[test]
fn malformed_selected_bytes_are_visible_and_reentrant_selection_is_refused() {
    let scratch = Scratch::new();
    let catalog = scratch.write("catalog.json", &fixture("catalog.example-valid.json"));
    let path = scratch.write("read.json", b"{");
    let state = Mutex::new(ExternalObservationSession::default());
    let received = receive_external_selection(
        &state,
        |stage| {
            assert!(receive_external_selection(
                &state,
                |_| panic!("reentrant picker must never execute"),
                || false
            )
            .is_err());
            Ok(Some(if stage == "catalog" {
                catalog.clone()
            } else {
                path.clone()
            }))
        },
        || false,
    )
    .unwrap();
    assert_eq!(received["observation"]["read"]["assessment"], "malformed");
    assert_eq!(
        received["observation"]["read"]["originalBytes"],
        json!(b"{")
    );
    assert_eq!(received["observation"]["hostOrigin"], "unverified");
    assert!(received["observation"]["reportedCurrency"].is_null());
}
