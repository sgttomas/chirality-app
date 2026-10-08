use super::*;
#[cfg(not(feature = "synthetic-distribution-anchor"))]
#[test]
fn compiled_anchor_disabled_never_resolves_resources_in_any_native_mode() {
    assert_eq!(
        observe_startup(|| panic!("disabled helper must not resolve or read resources"))
            ["standing"],
        "disabled"
    );
    assert!(!crate::distribution_preflight::production_available());
}
#[cfg(all(feature = "synthetic-distribution-anchor", debug_assertions))]
mod active {
    use super::*;
    use crate::distribution_preflight::digest;
    struct Fixture(PathBuf);
    impl Fixture {
        fn new() -> Self {
            let root = std::env::temp_dir()
                .canonicalize()
                .unwrap()
                .join(crate::util::opaque_id("compiled-anchor-").unwrap());
            std::fs::create_dir_all(root.join("distribution-development-reference")).unwrap();
            for (name, bytes) in enabled::FILES {
                std::fs::write(
                    root.join("distribution-development-reference").join(name),
                    bytes,
                )
                .unwrap();
            }
            Self(root)
        }
        fn resource(&self, name: &str) -> PathBuf {
            self.0.join("distribution-development-reference").join(name)
        }
        fn observe(&self) -> Value {
            observe_startup(|| Ok(self.0.clone()))
        }
    }
    impl Drop for Fixture {
        fn drop(&mut self) {
            let _ = std::fs::remove_dir_all(&self.0);
        }
    }
    #[test]
    fn compiled_anchor_actual_resource_check_is_startup_only_and_unverifiable() {
        let f = Fixture::new();
        let calls = std::cell::Cell::new(0);
        let snapshot = observe_startup(|| {
            calls.set(calls.get() + 1);
            Ok(f.0.clone())
        });
        assert_eq!(calls.get(), 1);
        assert_eq!(snapshot["outcome"], "compiled-bytes-matched");
        assert_eq!(snapshot["standing"], "development-unverifiable");
        assert_eq!(snapshot["currentTrust"], false);
        assert!(!crate::distribution_preflight::production_available());
        std::fs::write(f.resource("expected.json"), b"changed").unwrap();
        assert_eq!(
            snapshot["outcome"], "compiled-bytes-matched",
            "retained snapshot is not recomputed/current trust"
        );
        assert_eq!(f.observe()["outcome"], "refused");
    }
    #[test]
    fn compiled_anchor_refuses_consistent_replacement_missing_extra_type_and_link() {
        let f = Fixture::new();
        let mut expected: Value = serde_json::from_slice(enabled::FILES[1].1).unwrap();
        expected["author"] = json!("replacement author");
        let bytes = serde_json::to_vec(&expected).unwrap();
        let mut attestation: Value = serde_json::from_slice(enabled::FILES[2].1).unwrap();
        attestation["author"] = expected["author"].clone();
        attestation["expected_reference"]["sha256"] = json!(digest(&bytes));
        let attest_bytes = serde_json::to_vec(&attestation).unwrap();
        let mut selection: Value = serde_json::from_slice(enabled::FILES[0].1).unwrap();
        selection["expected"]["sha256"] = json!(digest(&bytes));
        selection["attestation"]["sha256"] = json!(digest(&attest_bytes));
        for (name, bytes) in [
            ("expected.json", bytes),
            ("attestation.json", attest_bytes),
            (
                "build-selection.s2.json",
                serde_json::to_vec(&selection).unwrap(),
            ),
        ] {
            std::fs::write(f.resource(name), bytes).unwrap();
        }
        assert_eq!(f.observe()["outcome"], "refused");
        for case in 0..4 {
            let f = Fixture::new();
            let path = f.resource("expected.json");
            if case == 0 {
                std::fs::write(f.resource("extra"), b"extra").unwrap();
            } else {
                std::fs::remove_file(&path).unwrap();
                if case == 2 {
                    std::fs::create_dir(path).unwrap();
                } else if case == 3 {
                    std::os::unix::fs::symlink(f.resource("synthetic-evidence.json"), path)
                        .unwrap();
                }
            }
            assert_eq!(f.observe()["outcome"], "refused");
        }
    }
    #[test]
    fn compiled_anchor_fixed_schemas_and_relations_are_consistent() {
        let values: Vec<Value> = enabled::FILES
            .iter()
            .map(|(_, b)| serde_json::from_slice(b).unwrap())
            .collect();
        for (value, schema) in [
            (
                &values[1],
                include_str!(
                    "../resources/distribution-successor/expected-reference.s1.schema.json"
                ),
            ),
            (
                &values[2],
                include_str!(
                    "../resources/distribution-successor/adoption-attestation.s1.schema.json"
                ),
            ),
        ] {
            let schema: Value = serde_json::from_str(schema).unwrap();
            jsonschema::validator_for(&schema)
                .unwrap()
                .validate(value)
                .unwrap();
        }
        assert_eq!(values[0]["format"], "build-selection.s2");
        assert_eq!(
            values[0]["schema_ids"],
            json!(["expected-reference.s1", "adoption-attestation.s1"])
        );
        assert_eq!(values[0]["expected"], values[2]["expected_reference"]);
        for (key, index) in [("expected", 1), ("attestation", 2)] {
            assert_eq!(values[0][key]["path"], enabled::FILES[index].0);
            assert_eq!(values[0][key]["sha256"], digest(enabled::FILES[index].1));
        }
        for (value, pointers) in [
            (
                &values[1],
                vec![
                    "/label_evidence",
                    "/generation_correspondence",
                    "/generated/provenance",
                    "/generated/version_advance",
                    "/archive/acquisition_authorization",
                    "/archive/custody",
                    "/archive/extraction_procedure",
                ],
            ),
            (
                &values[2],
                vec![
                    "/review_evidence",
                    "/adoption/through_help_human",
                    "/adoption/evidence",
                ],
            ),
        ] {
            for pointer in pointers {
                assert_eq!(
                    value.pointer(pointer).unwrap(),
                    &json!({"path":"synthetic-evidence.json","sha256":digest(enabled::FILES[3].1)})
                );
            }
        }
        assert_eq!(values[1]["author"], values[2]["author"]);
        assert_ne!(values[2]["author"], values[2]["independent_reviewer"]);
        assert_eq!(values[1]["pin"], values[1]["generated"]["pin"]);
    }
}
