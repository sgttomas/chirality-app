// S1 Design — Compiled build-selection implementation: real Host wiring with invented trees, plus read-only stock comparison.
use super::*;

fn fixture() -> Fixture {
    Fixture::new("open(os.path.join(os.environ['CODEX_HOME'],'probed'),'w').close()")
}
fn assert_no_execution(f: &Fixture, host: &Host) {
    assert!(!f.root.join("probe/probed").exists(), "version probe must not execute");
    assert!(host.child.lock().unwrap().is_none());
    assert!(host.snapshot()["generation"].is_null());
}
fn selected(f: &Fixture, change: impl FnOnce(&mut Value)) -> Result<Selected, String> {
    let source = f.root.join("reference-source");
    let inventory = serde_json::to_value(tree::scan(&f.root.join("vendor")).unwrap()).unwrap();
    let mut anchor = tree::selection::fixture_files(&source, &inventory, "reference/expected.json");
    let write = |path: &str, value: &Value| {
        let raw = serde_json::to_vec(value).unwrap();
        std::fs::write(source.join(path), &raw).unwrap();
        json!({"path":path,"sha256":tree::digest(&raw)})
    };
    let mut e: Value = serde_json::from_slice(&std::fs::read(source.join("reference/expected.json")).unwrap()).unwrap();
    change(&mut e);
    let er = write("reference/expected.json", &e);
    let mut a: Value = serde_json::from_slice(&std::fs::read(source.join("reference/attestation.json")).unwrap()).unwrap();
    a["expected_reference"] = er.clone();
    let ar = write("reference/attestation.json", &a);
    let mut s: Value = serde_json::from_slice(&std::fs::read(source.join(&anchor.path)).unwrap()).unwrap();
    s["expected"] = er;
    s["attestation"] = ar;
    anchor.sha256 = write(&anchor.path, &s)["sha256"].as_str().unwrap().into();
    Selected::fixture(&source, anchor)
}

#[test]
fn s2_matching_selected_tree_publishes_passes_but_never_custody_or_verified() {
    let f = fixture(); let host = Arc::new(Host::new()); let data = attach_selected_store(&host, &f, Some("reference/expected.json"));
    let ready = host.start(&f.cfg, "fixture").unwrap();
    assert!(f.root.join("probe/probed").exists());
    assert_eq!(ready["distributionSuccessor"]["referenceComparison"]["outcome"], "equal");
    assert_eq!(ready["supplierStanding"], "unverified-development");
    let e = host.distribution_evidence(&ready["generation"])["evidence"].clone();
    let observation = &e["artifact"];
    for name in ["tree", "reference", "generated", "label"] { assert_eq!(observation["checks"][name]["outcome"], "pass", "{name}"); }
    assert_eq!(observation["checks"]["custody"]["outcome"], "missing");
    assert_eq!(observation["outcome"], "unverifiable");
    assert!(host.lifecycle_events().iter().all(|e| e["transitionId"] != "LT-04"));
    let root = data.join("runtime/distribution").join(e["reference"]["publication"].as_str().unwrap());
    let files: crate::distribution_s1::Files = e["transport"]["entries"].as_array().unwrap().iter()
        .map(|e| { let p = e["path"].as_str().unwrap(); (p.into(), std::fs::read(root.join(p)).unwrap()) }).collect();
    let store = host.distribution_store.lock().unwrap().as_ref().unwrap().as_ref().unwrap().clone();
    assert_eq!(crate::distribution_s1::observed(observation, &files, store.selected()).unwrap(), "unverifiable");
    let mut false_custody = observation.clone(); false_custody["checks"]["custody"]["outcome"] = json!("pass");
    assert!(crate::distribution_s1::observed(&false_custody, &files, store.selected()).unwrap_err().contains("custody issuer unsupported"));
    host.stop("fixture", "comparison complete").unwrap();
}

#[test]
fn s2_tree_differences_refuse_before_probe_or_child() {
    for case in ["content", "extra", "missing", "mode", "empty-directory", "symlink", "fifo", "hard-link"] {
        let f = fixture(); let host = Arc::new(Host::new()); attach_selected_store(&host, &f, Some("reference/expected.json"));
        let vendor = f.root.join("vendor");
        match case {
            "content" => { let bin=vendor.join("bin/codex"); let mut bytes=std::fs::read(&bin).unwrap(); bytes.extend_from_slice(b"# changed but still executable\n"); std::fs::write(bin, bytes).unwrap(); },
            "extra" => std::fs::write(vendor.join("extra"), b"extra").unwrap(),
            "missing" => std::fs::remove_file(vendor.join("codex-package.json")).unwrap(),
            "mode" => std::fs::set_permissions(vendor.join("bin/codex"), std::fs::Permissions::from_mode(0o500)).unwrap(),
            "empty-directory" => std::fs::create_dir(vendor.join("extra-empty")).unwrap(),
            "symlink" => std::os::unix::fs::symlink("bin/codex", vendor.join("alias")).unwrap(),
            "fifo" => { use std::os::unix::ffi::OsStrExt; let path = std::ffi::CString::new(vendor.join("pipe").as_os_str().as_bytes()).unwrap(); assert_eq!(unsafe { libc::mkfifo(path.as_ptr(), 0o600) }, 0); }
            "hard-link" => std::fs::hard_link(vendor.join("bin/codex"), vendor.join("alias")).unwrap(),
            _ => unreachable!(),
        }
        let error = host.start(&f.cfg, "fixture").unwrap_err(); assert!(error.contains("mismatch:"), "{case}: {error}");
        assert_no_execution(&f, &host);
    }
}

#[test]
fn s2_wrong_label_refuses_after_comparison_without_server_child() {
    let f = Fixture::new("open(os.path.join(os.environ['CODEX_HOME'],'probed'),'w').close(); print('codex-cli 0.161.0'); sys.exit(0)");
    let host = Arc::new(Host::new()); attach_selected_store(&host, &f, Some("reference/expected.json"));
    assert!(host.start(&f.cfg, "fixture").unwrap_err().contains("observed version label"));
    assert!(f.root.join("probe/probed").exists()); assert!(host.child.lock().unwrap().is_none()); assert!(host.snapshot()["generation"].is_null());
    let store=host.distribution_store.lock().unwrap().as_ref().unwrap().as_ref().unwrap().clone();
    assert!(prepare(f.cfg.distribution.as_ref().unwrap(), &f.cfg, &json!({}), Reference::Selected(store.selected().unwrap())).err().unwrap().contains("observed version label"));
}

#[test]
fn s2_altered_reference_pin_generated_and_launcher_refuse_before_probe() {
    for case in ["pin", "generated", "launcher"] {
        let f = fixture();
        let reference = selected(&f, |e| match case {
            "pin" => { e["pin"] = json!("0.161.0"); e["generated"]["pin"] = json!("0.161.0"); },
            "generated" => e["generated"]["manifest_sha256"] = json!("0".repeat(64)),
            "launcher" => e["launcher"]["removed_wrapper_variables"] = json!(["CODEX_MANAGED_BY_NPM"]),
            _ => unreachable!(),
        });
        if case == "launcher" {
            assert!(reference.is_err(), "the closed launcher schema refuses the altered convention");
            assert!(!f.root.join("probe/probed").exists());
            continue;
        }
        let reference = reference.unwrap();
        let error = prepare(f.cfg.distribution.as_ref().unwrap(), &f.cfg, &json!({}), Reference::Selected(&reference)).err().unwrap();
        assert!(error.contains("mismatch:"), "{case}: {error}"); assert!(!f.root.join("probe/probed").exists());
    }
}

#[test]
fn s2_post_setup_reference_tamper_refuses_before_probe() {
    for case in ["selection", "expected", "dependency", "root"] {
        let f = fixture(); let host = Arc::new(Host::new()); attach_selected_store(&host, &f, Some("reference/expected.json"));
        let source = f.root.join("reference-source");
        match case {
            "selection" => std::fs::write(source.join("selection/build.json"), b"changed").unwrap(),
            "expected" => std::fs::write(source.join("reference/expected.json"), b"changed").unwrap(),
            "dependency" => std::fs::write(source.join("evidence/expected/0.json"), b"changed").unwrap(),
            "root" => { let aside = f.root.join("original-reference"); std::fs::rename(&source, &aside).unwrap(); copy_files(&aside, &source); },
            _ => unreachable!(),
        }
        let error = host.start(&f.cfg, "fixture").unwrap_err(); assert_no_execution(&f, &host); assert!(error.contains("selected reference closure"), "{case}: {error}");
    }
}

#[test]
fn s2_failed_or_required_missing_store_refuses_before_probe() {
    for required_missing in [false, true] {
        let f = fixture(); let host = Arc::new(Host::new()); let mut cfg = f.cfg.clone();
        if required_missing { cfg.require_distribution_artifacts = true; }
        else { host.configure_distribution_store(Err("compiled closure digest mismatch".into())); }
        assert!(host.start(&cfg, "fixture").is_err()); assert_no_execution(&f, &host);
    }
}

#[test]
fn s2_explicit_missing_reference_account_stays_unverifiable() {
    let f = fixture(); let host = Arc::new(Host::new()); attach_store(&host, &f);
    let store = host.distribution_store.lock().unwrap().take().unwrap().unwrap();
    host.configure_distribution_store(crate::distribution_store::Store::with_reference_limit(store, "fixture: no reference supplied".into()));
    let ready = host.start(&f.cfg, "fixture").unwrap();
    assert_eq!(ready["supplierStanding"], "unverified-development");
    assert_eq!(ready["distributionSuccessor"]["referenceComparison"]["outcome"], "unavailable");
    assert!(ready["verification"]["reason"].as_str().unwrap().contains("no reference supplied"), "{ready}");
    host.stop("fixture", "gap complete").unwrap();
}

#[test]
fn s2_production_matching_and_mismatched_trees_never_execute() {
    for mismatch in [false, true] {
        let f = fixture(); let reference = selected(&f, |_| {}).unwrap();
        let resources = f.root.join("resources"); std::fs::create_dir(&resources).unwrap(); std::fs::rename(f.root.join("vendor"), resources.join("codex")).unwrap();
        if mismatch { std::fs::write(resources.join("codex/extra"), b"extra").unwrap(); }
        let error = prepare(&Distribution::Production { resources }, &f.cfg, &json!({}), Reference::Selected(&reference)).err().unwrap();
        assert!(error.contains(if mismatch { "mismatch:" } else { "complete tree equals" }), "{error}");
        assert!(!f.root.join("probe/probed").exists());
    }
}

fn copy_files(source: &Path, destination: &Path) {
    std::fs::create_dir_all(destination).unwrap();
    for entry in std::fs::read_dir(source).unwrap() { let entry = entry.unwrap(); let to = destination.join(entry.file_name());
        if entry.file_type().unwrap().is_dir() { copy_files(&entry.path(), &to); } else { std::fs::copy(entry.path(), to).unwrap(); }
    }
}

#[test]
fn s2_compiled_stock_reference_resolves_exact_closure_and_refuses_tampered_copy() {
    let source = development_reference_root().unwrap(); let reference = Selected::production(&source).unwrap();
    assert_eq!(reference.expected_ref().sha256, "754eebae912023aebe40cab157c0882081bec2d1d9db518627986526371a2a37");
    assert_eq!(reference.attestation_ref().sha256, "09e1fae9d243462132803d868174b70ddae111bde2106aa2351ebfe74c793fe9");
    let e = reference.expected().unwrap(); assert_eq!(e["inventory"]["entries"].as_array().unwrap().len(), 53);
    assert!(e["inventory"]["manifest_sha256"].as_str().unwrap().starts_with("327effb9"));
    assert_eq!(e["generated"]["manifest_sha256"], GENERATED_MANIFEST_SHA256);
    let f = fixture(); let copied = f.root.join("copied-reference"); copy_files(&source, &copied);
    Selected::production(&copied).unwrap(); std::fs::write(copied.join(reference.expected_ref().path.as_str()), b"changed").unwrap();
    assert!(Selected::production(&copied).is_err());
}

#[test]
#[ignore = "requires an explicitly supplied existing stock vendor tree; reads only"]
fn s2_existing_stock_vendor_tree_matches_without_execution() {
    let root = PathBuf::from(std::env::var_os("CHIRALITY_TEST_VENDOR_ROOT").expect("supply existing vendor tree explicitly"));
    let reference = Selected::production(&development_reference_root().unwrap()).unwrap();
    assert_eq!(compare_to_reference(&reference, &tree::scan(&root).unwrap()).unwrap()["outcome"], "equal");
}
