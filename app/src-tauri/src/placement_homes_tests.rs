//! The records store's placement check compares the store with each Codex
//! home where that home is in fact used. A relative home given on the
//! explicit environment route is resolved by its child under the child's
//! working folder, not the App's own; the check compares it there. Invented
//! folders only; no supplier is started.
use super::*;
use std::path::{Path, PathBuf};

/// One test's own root under the temporary folder, made new by that test
/// (never a folder already there) and removed when the test's thread ends:
/// after its assertions, or after a failure, which still shows. It removes
/// nothing but the root it made.
struct TestRoot(PathBuf);
impl Drop for TestRoot {
    fn drop(&mut self) {
        let _ = std::fs::remove_dir_all(&self.0);
    }
}
thread_local! { static ROOT: std::cell::RefCell<Option<TestRoot>> = const { std::cell::RefCell::new(None) }; }
/// A new folder for invented material, in this test's own root.
fn folder(prefix: &str) -> PathBuf {
    ROOT.with(|root| {
        let mut root = root.borrow_mut();
        let base = &root.get_or_insert_with(|| {
            let made = std::env::temp_dir().join(crate::util::opaque_id("placement-test-").unwrap());
            std::fs::create_dir(&made).unwrap();
            TestRoot(std::fs::canonicalize(made).unwrap())
        }).0;
        let p = base.join(crate::util::opaque_id(prefix).unwrap());
        std::fs::create_dir(&p).unwrap();
        p
    })
}
/// A relative name that names nothing in the App's own working folder.
const RELATIVE: &str = "invented-relative-codex-home";

#[test]
fn a_relative_home_is_never_compared_from_the_apps_own_folder() {
    assert!(!std::env::current_dir().unwrap().join(RELATIVE).exists(), "the App's own folder holds no folder of that name");
    let cwd = folder("placement-child-cwd-");
    let data = folder("placement-data-");
    let mut cfg = hosting::HostConfig::new(PathBuf::from("/invented/bin/codex"), PathBuf::from(RELATIVE), folder("placement-probe-"), cwd.clone());
    cfg.records_project = false;
    let homes = codex_homes_from([&cfg].into_iter(), None, |_| None);
    // The folder the child uses as its Codex home.
    let used = cwd.join(RELATIVE);
    std::fs::create_dir_all(&used).unwrap();
    // At start-up (for_app), with a store inside it: refused.
    let started = records_store::for_app(Some(used.join("records")), Ok(&data), true, None, &homes);
    assert!(started.as_ref().is_err_and(|e| e.contains("Codex home")), "start-up placement: {started:?}");
    // When the person chooses a location (choose_location): refused.
    let chosen = records_store::choose_location(&data, &used.join("records"), None, &homes);
    assert!(chosen.as_ref().is_err_and(|e| e.contains("Codex home")), "a chosen location: {chosen:?}");
    // A store elsewhere is still admitted at start-up.
    let elsewhere = folder("placement-elsewhere-").join("records");
    assert!(records_store::for_app(Some(elsewhere), Ok(&data), true, None, &homes).is_ok());
    let _ = (std::fs::remove_dir_all(&cwd), std::fs::remove_dir_all(&data));
}

/// The development case the trace found: explicit environment inputs with
/// no workspace give the supplier the temporary folder as its working
/// folder; a relative CHIRALITY_CODEX_HOME is then a folder there, and the
/// development override, which may name a temporary folder, is refused
/// inside it.
#[test]
fn the_development_route_never_places_the_store_inside_the_childs_home() {
    let data = folder("placement-dev-data-");
    let input = |key: &str| match key {
        "CHIRALITY_CODEX_BIN" => Some("/invented/bin/codex".into()),
        "CHIRALITY_CODEX_HOME" => Some(RELATIVE.into()),
        _ => None,
    };
    let launch = explicit_environment_launch(input, &Ok(data.clone()), &Err("no resources".into()), true, || Ok(folder("placement-dev-probe-"))).unwrap();
    let cfg = launch.host_config.unwrap();
    assert_eq!(cfg.cwd, std::env::temp_dir(), "no workspace: the temporary folder");
    let used = cfg.cwd.join(RELATIVE);
    let homes = codex_homes_from([&cfg].into_iter(), Some(&data), input);
    let placed = records_store::for_app(Some(used.join("records")), Ok(&data), true, None, &homes);
    assert!(placed.as_ref().is_err_and(|e| e.contains("Codex home")), "{placed:?}");
    let _ = std::fs::remove_dir_all(&data);
}

/// The release case the trace found: the production branch of the explicit
/// environment route, with no workspace, gives the supplier the App data
/// folder as its working folder; CHIRALITY_CODEX_HOME=records then makes the
/// child's Codex home the default records store itself. Composed here as
/// that branch composes it (`successor::production_config`, the working
/// folder the workspace or else the App data folder). The App data folder
/// lies under the temporary folder in this test, so the store is refused as
/// a temporary folder too; what this test holds is that it is also refused
/// as the Codex home, which the comparison from the App's own folder missed.
#[test]
fn the_release_route_never_takes_the_default_store_for_anything_but_the_childs_home() {
    assert!(!std::env::current_dir().unwrap().join("records").exists(), "the App's own folder holds no records folder");
    let data = folder("placement-release-data-");
    let cfg = hosting::successor::production_config(folder("placement-release-resources-"), PathBuf::from("records"), folder("placement-release-probe-"), data.clone());
    let input = |key: &str| (key == "CHIRALITY_CODEX_HOME").then(|| "records".into());
    let homes = codex_homes_from([&cfg].into_iter(), Some(&data), input);
    assert_eq!(cfg.cwd.join(&cfg.codex_home), data.join("records"), "the child's Codex home is the default store");
    let placed = records_store::for_app(None, Ok(&data), false, None, &homes);
    assert!(placed.as_ref().is_err_and(|e| e.contains("Codex home")), "{placed:?}");
    let _ = std::fs::remove_dir_all(&data);
}

/// The same release case through the route itself, in a build with the
/// distribution-successor feature (run with --features distribution-successor).
#[cfg(feature = "distribution-successor")]
#[test]
fn the_release_environment_route_never_takes_the_default_store_for_anything_but_the_childs_home() {
    let data = folder("placement-release-route-data-");
    let resources = folder("placement-release-route-resources-");
    let input = |key: &str| (key == "CHIRALITY_CODEX_HOME").then(|| "records".into());
    let launch = explicit_environment_launch(input, &Ok(data.clone()), &Ok(resources), false, || Ok(folder("placement-release-route-probe-"))).unwrap();
    let cfg = launch.host_config.unwrap();
    assert_eq!(cfg.cwd, data, "no workspace: the App data folder");
    let homes = codex_homes_from([&cfg].into_iter(), Some(&data), input);
    let placed = records_store::for_app(None, Ok(&data), false, None, &homes);
    assert!(placed.as_ref().is_err_and(|e| e.contains("Codex home")), "{placed:?}");
    let _ = std::fs::remove_dir_all(&data);
}

/// Absolute homes behave as before: a store inside one is refused, one
/// outside admitted, whatever the working folders.
#[test]
fn absolute_homes_are_compared_as_before() {
    let home = folder("placement-absolute-home-");
    let data = folder("placement-absolute-data-");
    let cfg = hosting::HostConfig::new(PathBuf::from("/invented/bin/codex"), home.clone(), folder("placement-absolute-probe-"), folder("placement-absolute-cwd-"));
    let homes = codex_homes_from([&cfg].into_iter(), None, |_| None);
    assert!(homes.contains(&home));
    assert!(records_store::for_app(Some(home.join("records")), Ok(&data), true, None, &homes).is_err_and(|e| e.contains("Codex home")));
    assert!(records_store::for_app(Some(folder("placement-absolute-elsewhere-").join("records")), Ok(&data), true, None, &homes).is_ok());
    let _ = (std::fs::remove_dir_all(&home), std::fs::remove_dir_all(&data));
}

/// An empty configured home is an invalid input, refused by name: never
/// compared, so it neither overlaps every store nor none. Given on the
/// development route (CHIRALITY_CODEX_HOME="").
#[test]
fn an_empty_configured_home_is_refused_as_an_invalid_input() {
    let data = folder("placement-empty-data-");
    // A workspace, so the supplier's working folder is not where the store
    // is: an empty home joined to it would name only the workspace.
    let workspace = folder("placement-empty-workspace-");
    let input = |key: &str| match key {
        "CHIRALITY_CODEX_BIN" => Some("/invented/bin/codex".into()),
        "CHIRALITY_CODEX_HOME" => Some("".into()),
        "CHIRALITY_WORKSPACE" => Some(workspace.clone().into()),
        _ => None,
    };
    let launch = explicit_environment_launch(input, &Ok(data.clone()), &Err("no resources".into()), true, || Ok(folder("placement-empty-probe-"))).unwrap();
    let cfg = launch.host_config.unwrap();
    assert!(cfg.codex_home.as_os_str().is_empty(), "the route accepts the empty home");
    let homes = codex_homes_from([&cfg].into_iter(), Some(&data), input);
    let placed = records_store::for_app(Some(folder("placement-empty-elsewhere-").join("records")), Ok(&data), true, None, &homes);
    assert!(placed.as_ref().is_err_and(|e| e.contains("empty path, an invalid input")), "{placed:?}");
    let _ = (std::fs::remove_dir_all(&data), std::fs::remove_dir_all(&workspace));
}

/// The local provider's Codex home, which the bootstrap plans in the App
/// data folder before any host configuration exists for it, is protected at
/// the person's choice and at start-up alike.
#[test]
fn the_local_providers_home_is_protected_before_it_is_bound() {
    let data = folder("placement-local-data-");
    let local = runtime_session::local_provider_home(&data);
    assert_eq!(local, data.join("codex-omlx"), "the path the bootstrap plans");
    assert!(!local.exists(), "planned, not yet created");
    // No host configuration at all: only the App data folder is known.
    let homes = codex_homes_from(std::iter::empty(), Some(&data), |_| None);
    let chosen = records_store::choose_location(&data, &local.join("records"), None, &homes);
    assert!(chosen.as_ref().is_err_and(|e| e.contains("Codex home")), "the person's choice: {chosen:?}");
    // A location chosen earlier, read at start-up.
    std::fs::write(data.join(records_store::CHOICE_FILE), serde_json::to_vec(&serde_json::json!({"location": local.join("records").display().to_string()})).unwrap()).unwrap();
    let started = records_store::for_app(None, Ok(&data), false, None, &homes);
    assert!(started.as_ref().is_err_and(|e| e.contains("Codex home")), "start-up: {started:?}");
    let _ = std::fs::remove_dir_all(&data);
}

/// Raw environment values are compared from the App's own folder, as
/// before: an inherited relative CODEX_HOME that no child uses never refuses
/// a store under a configured working folder.
#[test]
fn an_unused_inherited_codex_home_never_refuses_an_unrelated_store() {
    let data = folder("placement-inherited-data-");
    let cfg = hosting::successor::production_config(folder("placement-inherited-resources-"), folder("placement-inherited-account-"), folder("placement-inherited-probe-"), data.clone());
    let input = |key: &str| (key == "CODEX_HOME").then(|| "invented-unused-home".into());
    let homes = codex_homes_from([&cfg].into_iter(), Some(&data), input);
    let chosen = records_store::choose_location(&data, &data.join("invented-unused-home").join("records"), None, &homes);
    assert!(chosen.as_ref().map_or_else(|e| !e.contains("Codex home"), |_| true), "never refused as a Codex home: {chosen:?}");
    let _ = std::fs::remove_dir_all(&data);
}

/// The bootstrap and placement agree on the local provider's home: the
/// folder the bootstrap plans is the folder placement protects, from the one
/// function both use (so a later change to where it is cannot leave the
/// store's protection behind).
#[test]
fn the_bootstrap_plans_the_local_home_placement_protects() {
    let data = folder("placement-agree-data-");
    let root = folder("placement-agree-root-");
    for home in ["account", "probe"] { std::fs::create_dir_all(root.join(home)).unwrap(); }
    let cfg = hosting::HostConfig::new(PathBuf::from("/invented/bin/codex"), root.join("account"), root.join("probe"), root.clone());
    let bootstrap = runtime_session::freeze_root_home_descriptors(&data, &cfg, None, [None, None, None]).unwrap();
    let planned = bootstrap.local_plan().unwrap().native_path().to_path_buf();
    assert_eq!(planned, runtime_session::local_provider_home(&data));
    assert!(codex_homes_from([&cfg].into_iter(), Some(&data), |_| None).contains(&planned), "placement protects the planned folder");
    let _ = (std::fs::remove_dir_all(&data), std::fs::remove_dir_all(&root));
}

/// The folder where the App allocates its account homes is reserved: a
/// store equal to it, inside it (a planned home included, before it exists)
/// or containing it is refused, with that reason, at the person's choice and
/// at start-up; a store beside it in the App data folder is still allowed.
#[test]
fn the_account_homes_folder_is_reserved_before_any_home_is_planned() {
    let data = folder("placement-namespace-data-");
    let reserved = desktop_startup::desktop_account_homes(&data);
    assert!(!reserved.exists(), "nothing planned or created yet");
    let homes = codex_homes_from(std::iter::empty(), Some(&data), |_| None);
    let refused = |location: &Path| records_store::choose_location(&data, location, None, &homes).is_err_and(|e| e.contains("reserved for the App's account homes"));
    assert!(refused(&reserved), "equal to it");
    assert!(refused(&reserved.join("account-invented").join("records")), "inside it");
    // A planned home, through the real planner, before it exists.
    let mut desktop = desktop_startup::DesktopSetup::new(Ok(data.clone()), Err("invented resources unused by a preview".into()));
    let planned = PathBuf::from(desktop.preview_new_settings(None).unwrap()["accountHome"].as_str().unwrap());
    assert!(!planned.exists() && refused(&planned.join("records")), "inside a planned home");
    // Containing it: the whole App data folder chosen as the store.
    let containing = records_store::choose_location(&data, &data, None, &homes);
    assert!(containing.as_ref().is_err_and(|e| e.contains("reserved for the App's account homes")), "containing it: {containing:?}");
    // At start-up, a location chosen earlier inside it.
    std::fs::write(data.join(records_store::CHOICE_FILE), serde_json::to_vec(&serde_json::json!({"location": planned.join("records").display().to_string()})).unwrap()).unwrap();
    let started = records_store::for_app(None, Ok(&data), false, None, &homes);
    assert!(started.as_ref().is_err_and(|e| e.contains("reserved for the App's account homes")), "start-up: {started:?}");
    // Beside it: never refused as reserved (this App data folder lies under
    // the temporary folder in tests, so it is refused as temporary instead).
    std::fs::remove_file(data.join(records_store::CHOICE_FILE)).unwrap();
    for beside in [data.join("records"), data.join("another-store")] {
        let placed = records_store::choose_location(&data, &beside, None, &homes);
        assert!(placed.as_ref().map_or_else(|e| !e.contains("reserved"), |_| true), "beside it: {placed:?}");
    }
    let default = records_store::for_app(None, Ok(&data), false, None, &homes);
    assert!(default.as_ref().map_or_else(|e| !e.contains("reserved"), |_| true), "the default store: {default:?}");
    let _ = std::fs::remove_dir_all(&data);
}

/// The desktop planner, its parent-location check and placement share one
/// calculation of the reserved folder: the planner plans its home as a new
/// leaf directly in it. This fails if the planner ever plans one outside.
#[test]
fn the_desktop_planner_plans_inside_the_reserved_folder() {
    let data = folder("placement-desktop-agree-");
    let mut desktop = desktop_startup::DesktopSetup::new(Ok(data.clone()), Err("invented resources unused by a preview".into()));
    let planned = PathBuf::from(desktop.preview_new_settings(None).unwrap()["accountHome"].as_str().unwrap());
    assert_eq!(planned.parent(), Some(desktop_startup::desktop_account_homes(&data).as_path()), "planned as a new leaf in the reserved folder");
    let _ = std::fs::remove_dir_all(&data);
}

/// Raw environment values are given to placement as main resolved them:
/// one of which nothing exists in the App's own folder refuses nothing (it
/// never matched in main); one whose ancestor exists there is compared, as
/// main compared it.
#[test]
fn raw_values_are_compared_as_main_compared_them() {
    let data = folder("placement-raw-data-");
    let here = std::env::current_dir().unwrap();
    assert!(!here.join("invented-unused-home").exists() && here.join("src").is_dir());
    // Nothing of it exists: no refusal at the App's folder.
    let nothing = codex_homes_from(std::iter::empty(), Some(&data), |key| (key == "CODEX_HOME").then(|| "invented-unused-home".into()));
    let chosen = records_store::choose_location(&data, &here.join("invented-unused-home").join("records"), None, &nothing);
    assert!(chosen.as_ref().map_or_else(|e| !e.contains("Codex home"), |_| true), "no false refusal: {chosen:?}");
    // An ancestor exists: compared from the App's folder, as main did.
    let partly = codex_homes_from(std::iter::empty(), Some(&data), |key| (key == "CODEX_HOME").then(|| "src/invented-home".into()));
    let refused = records_store::choose_location(&data, &here.join("src/invented-home/records"), None, &partly);
    assert!(refused.as_ref().is_err_and(|e| e.contains("Codex home")), "compared as main compared it: {refused:?}");
    let _ = std::fs::remove_dir_all(&data);
}

/// The reservation is computed from the App data folder the start uses, and
/// `for_app` needs complete protected-home inputs to answer truly: given no
/// App data it cannot compute the reservation, and as a function it still
/// admits an explicit override. The App's start never gives it that input.
/// When App data cannot be resolved and held, admission refuses the start
/// (`admitted_startup`). Start-up's consumers then, as this test observes
/// through the real chain:
/// 1. configure the records store with the admission's refusal, not with
///    `for_app`'s answer (which would be the override store, admitted);
/// 2. open and create nothing at the override, though start-up's store
///    creation, project attachment and line-file recovery all run;
/// 3. leave nothing later in the process to fall back to it: the configured
///    refusal is what every later reader is given (`current()` consults the
///    override variable only when nothing is configured).
#[test]
fn a_start_without_app_data_places_no_records_store() {
    let root = folder("placement-no-data-");
    // What App data would have been, and an override in its reserved folder.
    let would_be = root.join("app-data");
    let store = desktop_startup::desktop_account_homes(&would_be).join("not-planned").join("records");
    let home = root.join("environment-home").into_os_string();
    let environment = |key: &str| -> Option<std::ffi::OsString> {
        match key {
            "CHIRALITY_CODEX_BIN" => Some("/invented/bin/codex".into()),
            "CHIRALITY_CODEX_HOME" => Some(home.clone()),
            "CHIRALITY_ALLOW_UNVERIFIED" => Some("1".into()),
            _ => None,
        }
    };
    let saved = records_store::configured_for_test();
    let (desktop, inputs) = crate::admitted_startup(environment, Err("platform App data unavailable (invented)".into()), Err("invented resources".into()), true, || Err("no probe home without held App data".into()));
    let desktop_startup::RootInputs { launch, data, allow_operational } = inputs;
    assert!(!allow_operational, "nothing operational is admitted without App data");
    let (state, home) = crate::freeze_startup_state(launch, std::sync::Arc::new(std::sync::Mutex::new(desktop)), serde_json::Value::Null);
    // As `run` gives it: the override as the environment names it.
    crate::initialize_startup_consumers(&state, &home, data, allow_operational, true, Some(store.clone()), None, [None, None, None]);
    let configured = records_store::configured_for_test();
    let later = records_store::current();
    // Asked so that an examination failure fails the test: only NotFound is "not there".
    let after_read = [&store, &would_be].map(|p| std::fs::symlink_metadata(p).err().map(|e| e.kind()));
    records_store::restore_configured_for_test(saved);
    // 1. The store start-up configured is the admission's refusal.
    let refusal = match &configured { Some(Err(e)) => e.clone(), other => panic!("for_app's answer, not the admission's refusal, was configured: {other:?}") };
    assert!(refusal.contains("not admitted") && refusal.contains("platform App data unavailable (invented)"), "{refusal}");
    // 3. Every later reader is given that refusal; nothing falls back.
    assert_eq!(later.as_ref().err(), Some(&refusal), "no later fallback to the override: {later:?}");
    // 2. Nothing opened or created the override, or the App data it would be in.
    assert_eq!(after_read, [Some(std::io::ErrorKind::NotFound); 2], "no store placed, opened or created");
    let _ = std::fs::remove_dir_all(&root);
}
