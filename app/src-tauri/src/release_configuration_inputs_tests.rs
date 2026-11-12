// Included in desktop_startup's tests. The release configuration (built with
// distribution-successor, not a development run) admits no development
// startup input; every other build honours them as before. cfg!(feature)
// cannot change inside one build, so the hosted successor job runs these with
// the feature and the default suites run them without it.
use super::*;
use std::cell::RefCell;
use std::collections::BTreeMap;
use std::ffi::OsString;

const RELEASE: bool = cfg!(feature = "distribution-successor");

/// Every name the environment route or startup honoured, with an invented value.
fn invented(root: &Path) -> BTreeMap<&'static str, OsString> {
    let at = |name: &str| root.join("invented-environment").join(name).into_os_string();
    BTreeMap::from([
        ("CHIRALITY_CODEX_BIN", at("vendor/bin/codex")),
        ("CHIRALITY_CODEX_HOME", at("account-home")),
        ("CHIRALITY_WORKSPACE", at("project")),
        ("CHIRALITY_KEY_HOME", at("key-home")),
        ("CHIRALITY_SHARED_CONFIG", at("shared/config.toml")),
        ("CHIRALITY_SHARED_AGENTS", at("shared/AGENTS.md")),
        ("CHIRALITY_SHARED_SKILLS", at("shared/skills")),
        ("CHIRALITY_CODEX_EXPECTED_SHA256", "0".repeat(64).into()),
        ("CHIRALITY_ALLOW_UNVERIFIED", "1".into()),
        ("CHIRALITY_DISTRIBUTION_SUCCESSOR", "1".into()),
        ("CHIRALITY_RECORDS_STORE", at("records")),
        ("CHIRALITY_RECORDS_VERIFY_SECS", "7".into()),
        ("CODEX_HOME", at("person-codex-home")),
    ])
}

/// A reader over `values` that records every name it is asked for.
struct Recorder {
    values: BTreeMap<&'static str, OsString>,
    asked: RefCell<Vec<String>>,
}
impl Recorder {
    fn new(values: BTreeMap<&'static str, OsString>) -> Self {
        Self { values, asked: RefCell::new(Vec::new()) }
    }
    fn read(&self, key: &str) -> Option<OsString> {
        self.asked.borrow_mut().push(key.to_owned());
        self.values.get(key).cloned()
    }
    fn asked(&self) -> Vec<String> {
        self.asked.borrow().clone()
    }
    fn path(&self, key: &str) -> PathBuf {
        PathBuf::from(&self.values[key])
    }
}

fn refuse(key: &str) -> Option<OsString> {
    panic!("the release configuration asked the environment for {key}")
}

#[test]
fn release_configuration_inputs_rule_for_this_build() {
    assert!(crate::development_inputs_admitted(true), "a development run admits its inputs in every build");
    assert_eq!(
        crate::development_inputs_admitted(false),
        !RELEASE,
        "a built bundle admits development inputs exactly when it lacks distribution-successor"
    );
}

/// The launch fields that select binary, home, project and shared paths.
fn chosen(launch: &Launch) -> (Option<PathBuf>, Option<PathBuf>, [Option<PathBuf>; 3], Option<(PathBuf, PathBuf, PathBuf, bool, bool, bool)>) {
    let cfg = launch.host_config.as_ref().ok().map(|cfg| {
        (
            cfg.codex_bin.clone(),
            cfg.codex_home.clone(),
            cfg.cwd.clone(),
            cfg.allow_unverified_dev,
            cfg.expected_sha256.is_some(),
            matches!(cfg.distribution, Some(crate::hosting::successor::Distribution::Production { .. })),
        )
    });
    (launch.workspace.clone(), launch.key_path.clone(), launch.shared_paths.clone(), cfg)
}

#[test]
fn release_configuration_inputs_never_select_the_environment_route() {
    if !RELEASE {
        return;
    }
    for saved in [true, false] {
        let f = Fixture::new();
        if saved {
            let mut setup = f.setup();
            f.prepare(&mut setup, false);
        }
        // With nothing set.
        let mut empty = f.setup();
        let nothing = crate::explicit_environment_launch(|_| None, false, || panic!("no environment probe"));
        assert!(nothing.is_none());
        let baseline = empty.resolve(nothing, false, || f.probe());
        let baseline_state = empty.view()["launch"]["state"].clone();
        drop(empty);
        // Every honoured name set, through the reader startup uses.
        let recorder = Recorder::new(invented(&f.root));
        let env = crate::explicit_environment_launch(|key| recorder.read(key), false, || panic!("no environment probe"));
        assert!(env.is_none(), "the environment route is not selectable");
        assert!(recorder.asked().is_empty(), "the reader was asked for {:?}", recorder.asked());
        assert!(crate::explicit_environment_launch(refuse, false, || panic!("no environment probe")).is_none());
        let mut setup = f.setup();
        let launch = setup.resolve(env, false, || f.probe());
        let state = setup.view()["launch"]["state"].clone();
        assert_eq!(state, baseline_state);
        assert_eq!(state, if saved { "saved-request" } else { "setup-required" });
        assert_eq!(chosen(&launch), chosen(&baseline));
        assert_eq!(launch.source, baseline.source);
        if saved {
            let cfg = launch.host_config.as_ref().unwrap();
            assert!(matches!(cfg.distribution, Some(crate::hosting::successor::Distribution::Production { .. })));
            assert_eq!(cfg.codex_bin, f.resources.join("codex/bin/codex"));
            assert!(!cfg.allow_unverified_dev && cfg.expected_sha256.is_none());
            for key in ["CHIRALITY_CODEX_HOME", "CHIRALITY_WORKSPACE"] {
                assert_ne!(cfg.codex_home, recorder.path(key));
                assert_ne!(cfg.cwd, recorder.path(key));
            }
            assert!(launch.workspace.is_none() && launch.key_path.is_none());
        } else {
            assert!(launch.host_config.is_err());
        }
    }
}

#[test]
fn release_configuration_inputs_honoured_by_development_builds() {
    let f = Fixture::new();
    // A development run in every build; a built bundle without the feature
    // (the examination candidates) as well.
    let cases: &[bool] = if RELEASE { &[true] } else { &[true, false] };
    for &is_dev in cases {
        let recorder = Recorder::new(invented(&f.root));
        let launch = crate::explicit_environment_launch(|key| recorder.read(key), is_dev, || f.probe())
            .expect("a development build selects the environment route");
        let mut setup = f.setup();
        let launch = setup.resolve(Some(launch), is_dev, || panic!("the environment route is exclusive"));
        assert_eq!(setup.view()["launch"]["state"], "environment");
        let cfg = launch.host_config.as_ref().unwrap();
        assert_eq!(cfg.codex_bin, recorder.path("CHIRALITY_CODEX_BIN"));
        assert_eq!(cfg.codex_home, recorder.path("CHIRALITY_CODEX_HOME"));
        assert_eq!(cfg.cwd, recorder.path("CHIRALITY_WORKSPACE"));
        assert_eq!(cfg.expected_sha256.as_deref(), Some("0".repeat(64).as_str()));
        assert!(cfg.allow_unverified_dev);
        assert_eq!(
            matches!(cfg.distribution, Some(crate::hosting::successor::Distribution::Development { .. })),
            is_dev,
            "the development successor tree is taken only in a development run"
        );
        assert_eq!(launch.workspace, Some(recorder.path("CHIRALITY_WORKSPACE")));
        assert_eq!(launch.key_path, Some(recorder.path("CHIRALITY_KEY_HOME")));
        assert_eq!(
            launch.shared_paths,
            ["CHIRALITY_SHARED_CONFIG", "CHIRALITY_SHARED_AGENTS", "CHIRALITY_SHARED_SKILLS"].map(|key| Some(recorder.path(key)))
        );
    }
}

#[test]
fn release_configuration_inputs_leave_records_location_and_timing_alone() {
    let f = Fixture::new();
    let values = invented(&f.root);
    let person_home = PathBuf::from(&values["CODEX_HOME"]);
    for is_dev in [false, true] {
        // The rule stated independently of the function under test.
        let admitted = is_dev || !RELEASE;
        let recorder = Recorder::new(values.clone());
        assert_eq!(
            crate::records_override(|key| recorder.read(key), is_dev),
            admitted.then(|| recorder.path("CHIRALITY_RECORDS_STORE"))
        );
        assert_eq!(
            crate::records_store::override_from(|key| recorder.read(key), is_dev),
            admitted.then(|| values["CHIRALITY_RECORDS_STORE"].clone())
        );
        assert_eq!(
            crate::records_index::verify_interval_from(|key| recorder.read(key).and_then(|v| v.into_string().ok()), is_dev),
            if admitted { 7 } else { crate::records_index::VERIFY_INTERVAL }
        );
        let homes = crate::codex_homes_from(std::iter::empty(), |key| recorder.read(key), is_dev);
        assert!(homes.contains(&person_home), "the person's own Codex home is kept out of the records store in every build");
        for key in ["CHIRALITY_CODEX_HOME", "CHIRALITY_KEY_HOME"] {
            assert_eq!(homes.contains(&recorder.path(key)), admitted);
        }
        if !admitted {
            assert_eq!(recorder.asked(), ["CODEX_HOME"], "only the person's own CODEX_HOME is consulted");
            assert_eq!(crate::records_override(refuse, is_dev), None);
            assert_eq!(crate::records_store::override_from(refuse, is_dev), None);
            assert_eq!(
                crate::records_index::verify_interval_from(|key| refuse(key).and_then(|v| v.into_string().ok()), is_dev),
                crate::records_index::VERIFY_INTERVAL
            );
        }
    }
}
