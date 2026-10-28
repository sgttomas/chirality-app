//! Actual owning metadata sources; these tests perform no supplier/model turn.
use chirality_app_v4_lib::{
    attachments::{self, SelectedTextAttachment},
    hosting::attachment_custody::{read_metadata, rpc_key, AttachmentCustody, REDACTED_ERROR},
    util,
};
use serde_json::{json, Value};
fn scratch() -> std::path::PathBuf {
    let root = std::env::temp_dir().join(util::opaque_id("attachment-custody-").unwrap());
    std::fs::create_dir(&root).unwrap();
    root.canonicalize().unwrap()
}
fn generation() -> Value {
    json!({"appSession":"session-é","home":"home-家","spawnCounter":1})
}
fn prepared(root: &std::path::Path) -> (attachments::PreparedAttachmentList, Value) {
    let path = root.join("source.txt");
    std::fs::write(&path, "Exact file bytes\n家").unwrap();
    let source = SelectedTextAttachment::from_native_selection(path, None).unwrap();
    let token = attachments::new_submission_ref().unwrap();
    let list = attachments::prepare_ordered(&[source], &token, "2026-10-05T00:00:00Z").unwrap();
    let client = json!({"recordKind":"client-request","generation":generation(),"requestIdentity":1,"method":"turn/start","initiator":{"kind":"person-directed"},"writeResult":"not-attempted","outcome":"prepared-not-sent","submissionAssociation":{"submissionRef":token,"threadId":"thread","supplyRefs":list.supply_refs()}});
    (list, client)
}
#[test]
fn actual_array_client_publication_exact_readback_typed_keys_and_cold_claim_limits() {
    let root = scratch();
    let owner = AttachmentCustody::open(&root.join("app"), &root.join("codex")).unwrap();
    let (list, client) = prepared(&root);
    owner
        .publish_prepared(&list.supply_records(), &client)
        .unwrap();
    assert_eq!(
        read_metadata(&owner.supplies_path(list.submission_ref()).unwrap()).unwrap(),
        json!(list.supply_records())
    );
    assert_eq!(
        read_metadata(&owner.client_path(&generation(), &json!(1)).unwrap()).unwrap(),
        client
    );
    assert_ne!(rpc_key(&json!(1)).unwrap(), rpc_key(&json!("1")).unwrap());
    let view = owner.resolve_cold(list.submission_ref());
    assert!(view["nativeTurnRef"].is_null());
    assert_eq!(view["automaticRetry"], false);
    assert_eq!(view["clientMetadata"]["outcome"], "prepared-not-sent");
    assert!(view["dispatch"].as_str().unwrap().contains("unknown"));
    assert!(owner
        .publish_prepared(&list.supply_records(), &client)
        .is_err());
    let all = std::fs::read_to_string(owner.supplies_path(list.submission_ref()).unwrap()).unwrap();
    assert!(!all.contains("Exact file bytes"));
    assert!(
        !std::fs::read_to_string(owner.client_path(&generation(), &json!(1)).unwrap())
            .unwrap()
            .contains("Exact file bytes")
    );
    std::fs::remove_dir_all(root).unwrap();
}
#[test]
fn actual_source_corruption_key_mismatch_and_special_descriptor_are_unavailable() {
    let root = scratch();
    let owner = AttachmentCustody::open(&root.join("app"), &root.join("codex")).unwrap();
    let (list, client) = prepared(&root);
    owner
        .publish_prepared(&list.supply_records(), &client)
        .unwrap();
    let path = owner.client_path(&generation(), &json!(1)).unwrap();
    let mut wrong = client.clone();
    wrong["requestIdentity"] = json!("1");
    std::fs::write(&path, serde_json::to_vec(&wrong).unwrap()).unwrap();
    assert!(owner
        .resolve_cold(list.submission_ref())
        .get("clientMetadata")
        .is_none());
    std::fs::write(&path, serde_json::to_vec(&client).unwrap()).unwrap();
    std::fs::write(owner.supplies_path(list.submission_ref()).unwrap(), b"[").unwrap();
    assert!(owner
        .check_prepared(&list.supply_records(), &client)
        .is_err());
    assert!(owner
        .resolve_cold(list.submission_ref())
        .get("clientMetadata")
        .is_none());
    #[cfg(unix)]
    {
        use std::os::unix::ffi::OsStrExt;
        let fifo = root.join("metadata.fifo");
        let name = std::ffi::CString::new(fifo.as_os_str().as_bytes()).unwrap();
        assert_eq!(unsafe { libc::mkfifo(name.as_ptr(), 0o600) }, 0);
        assert!(read_metadata(&fifo).unwrap_err().contains("regular"));
    }
    std::fs::remove_dir_all(root).unwrap();
}
#[test]
fn allowlisted_actual_error_code_redaction_and_malformed_error_unknown() {
    let root = scratch();
    let owner = AttachmentCustody::open(&root.join("app"), &root.join("codex")).unwrap();
    let (list, mut client) = prepared(&root);
    owner
        .publish_prepared(&list.supply_records(), &client)
        .unwrap();
    client["writeResult"] = json!("written");
    client["outcome"] = json!("pending");
    client["sendPosition"] = json!(1);
    let response = json!({"id":1,"error":{"code":-32600,"message":"secret-native-payload","data":{"credential":"secret-data"}}});
    let mut raw = client.clone();
    raw["outcome"] = json!("response-observed-error");
    raw["responseReceiptPosition"] = json!(7);
    raw["error"] = response["error"].clone();
    assert!(owner.replace_observation(&raw).is_err());
    let (projected, limit) =
        chirality_app_v4_lib::hosting::attachment_custody::project_observation(
            &client,
            Some(&response),
            Some(7),
        )
        .unwrap();
    assert!(limit.is_none());
    assert_eq!(projected["error"]["code"], -32600);
    assert_eq!(projected["error"]["message"], REDACTED_ERROR);
    owner.replace_observation(&projected).unwrap();
    let bytes =
        std::fs::read_to_string(owner.client_path(&generation(), &json!(1)).unwrap()).unwrap();
    assert!(!bytes.contains("secret-native-payload"));
    assert!(!bytes.contains("secret-data"));
    let (malformed, limit) =
        chirality_app_v4_lib::hosting::attachment_custody::project_observation(
            &client,
            Some(&json!({"id":1,"error":{"message":"missing code"}})),
            Some(8),
        )
        .unwrap();
    assert_eq!(malformed["outcome"], "unknown-no-response");
    assert!(malformed.get("error").is_none());
    assert!(limit.is_some());
    assert!(owner.replace_observation(&malformed).is_err());
    assert!(owner.resolve_cold(list.submission_ref())["nativeTurnRef"].is_null());
    std::fs::remove_dir_all(root).unwrap();
}
#[test]
fn explicit_root_no_overlap_no_fallback_and_immutable_client_binding() {
    let root = scratch();
    assert!(
        AttachmentCustody::open(std::path::Path::new("relative"), &root.join("codex")).is_err()
    );
    assert!(AttachmentCustody::open(&root.join("codex/nested"), &root.join("codex")).is_err());
    let owner = AttachmentCustody::open(&root.join("app"), &root.join("codex")).unwrap();
    let (list, client) = prepared(&root);
    owner
        .publish_prepared(&list.supply_records(), &client)
        .unwrap();
    let mut wrong = client.clone();
    wrong["submissionAssociation"]["threadId"] = json!("different");
    assert!(owner.replace_observation(&wrong).is_err());
    assert_eq!(
        read_metadata(&owner.client_path(&generation(), &json!(1)).unwrap()).unwrap(),
        client
    );
    std::fs::remove_dir_all(root).unwrap();
}

#[test]
fn accepted_compact_json_storage_codec_literal_independent_vectors() {
    use chirality_app_v4_lib::hosting::attachment_custody::generation_key;
    assert_eq!(
        rpc_key(&json!(1)).unwrap(),
        "6b86b273ff34fce19d6b804eff5a3f5747ada4eaa22f1d49c01e52ddb7875b4b"
    );
    assert_eq!(
        rpc_key(&json!("1")).unwrap(),
        "391552c099c101b131feaf24c5795a6a15bc8ec82015424e0d2b4274a369a0bf"
    );
    assert_eq!(
        generation_key(&generation()).unwrap(),
        "0188b4fbe1747213423edda03f92163cbeb803158632f2e4e13d0d9ad86ec27d"
    );
    assert_eq!(
        generation_key(&json!({"appSession":"session-é","home":"home-家","spawnCounter":2}))
            .unwrap(),
        "6ed56a98d0d9319106bb3f95a82a078a8fd944d484c6eb15fe8a2a2ac96959fd"
    );
    assert_eq!(
        generation_key(&json!({"appSession":"other","home":"home-家","spawnCounter":1})).unwrap(),
        "7c5cbfbbc9945683af51d49bb234deaf7767a0386b7bb7d8fe12691da5d9430d"
    );
}
#[test]
fn actual_owning_leaf_and_lock_hard_aliases_refuse_but_user_selection_is_not_vetoed() {
    let root = scratch();
    let owner = AttachmentCustody::open(&root.join("app"), &root.join("codex")).unwrap();
    let (list, client) = prepared(&root);
    std::fs::hard_link(root.join("source.txt"), root.join("user-source-alias.txt")).unwrap();
    assert!(SelectedTextAttachment::from_native_selection(
        root.join("user-source-alias.txt"),
        None
    )
    .is_ok());
    owner
        .publish_prepared(&list.supply_records(), &client)
        .unwrap();
    let supplies = owner.supplies_path(list.submission_ref()).unwrap();
    let alias = root.join("supply-alias.json");
    std::fs::hard_link(&supplies, &alias).unwrap();
    assert!(read_metadata(&supplies)
        .unwrap_err()
        .contains("hard aliases"));
    assert!(owner
        .check_prepared(&list.supply_records(), &client)
        .is_err());
    assert!(owner
        .resolve_cold(list.submission_ref())
        .get("clientMetadata")
        .is_none());
    std::fs::remove_file(alias).unwrap();
    let path = owner.client_path(&generation(), &json!(1)).unwrap();
    let alias = root.join("client-alias.json");
    std::fs::hard_link(&path, &alias).unwrap();
    assert!(owner
        .resolve_cold(list.submission_ref())
        .get("clientMetadata")
        .is_none());
    assert!(owner.replace_observation(&client).is_err());
    std::fs::remove_file(alias).unwrap();
    let lock = owner.root().join("runtime/hosting/.client-custody.lock");
    let alias = root.join("lock-alias");
    std::fs::hard_link(&lock, &alias).unwrap();
    let (second, next) = prepared(&root);
    assert!(owner
        .publish_prepared(&second.supply_records(), &next)
        .unwrap_err()
        .contains("hard aliases"));
    assert!(!owner
        .supplies_path(second.submission_ref())
        .unwrap()
        .exists());
    assert!(owner
        .resolve_cold(list.submission_ref())
        .get("clientMetadata")
        .is_none());
    std::fs::remove_file(alias).unwrap();
    assert!(owner
        .resolve_cold(list.submission_ref())
        .get("clientMetadata")
        .is_some());
    std::fs::remove_dir_all(root).unwrap();
}
