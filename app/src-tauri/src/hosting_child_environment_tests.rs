//! Inherited-environment removals observed from the child's side on every
//! supplier start path, and the configuration identity that records them.
//! A stand-in supplier (a Python script) dumps its own environment; the real
//! supplier is never executed.
use super::*;
use std::collections::BTreeMap;
use std::os::unix::fs::PermissionsExt;

const WRAPPER: [&str; 2] = ["CODEX_MANAGED_PACKAGE_ROOT", "CODEX_MANAGED_BY_NPM"];
const CA: &str = "CODEX_CA_CERTIFICATE";
const VISIBLE: &str = "CHIRALITY_SYNTHETIC_VISIBLE";
const DUMP: &str = "CHIRALITY_CHILD_ENV_DUMP";
const EXPECT: &str = "CHIRALITY_CHILD_ENV_EXPECT_PRESENCE";
const DONE: &str = "CHILD-ENV-INNER-COMPLETE";
const INNER: &str = "hosting::child_environment_tests::child_environment_inner_observed_on_every_start_path";

fn canary(name: &str) -> String {
    format!("SYNTHETIC-CANARY-{name}-not-a-real-value")
}
/// Every name the parent sets to a canary: the listed removals, the successor
/// wrapper settings, and the variables that must pass through.
fn canary_names() -> Vec<&'static str> {
    removed_environment_names().chain(WRAPPER).chain([CA, RECORDED_PRESENCE_ONLY]).collect()
}

/// Runs the inner test in a fresh test process whose own (parent) environment
/// carries every canary, once with the presence-only variable set and once
/// without it.
#[test]
fn child_environment_lacks_removed_names_and_keeps_the_rest_on_every_start_path() {
    let dump = std::env::temp_dir().canonicalize().unwrap().join(opaque_id("child-env-dump-").unwrap());
    std::fs::create_dir(&dump).unwrap();
    for present in [true, false] {
        let mut cmd = Command::new(std::env::current_exe().unwrap());
        cmd.args(["--ignored", "--exact", INNER, "--nocapture", "--test-threads=1"]);
        for name in canary_names() {
            cmd.env(name, canary(name));
        }
        if !present {
            cmd.env_remove(RECORDED_PRESENCE_ONLY);
        }
        // The dump location is itself an unrelated inherited variable.
        cmd.env(VISIBLE, "ordinary").env(DUMP, &dump).env(EXPECT, if present { "present" } else { "absent" });
        let output = cmd.output().unwrap();
        let stdout = String::from_utf8_lossy(&output.stdout);
        assert!(output.status.success(), "inner run failed (presence {present}): {stdout}\n{}", String::from_utf8_lossy(&output.stderr));
        assert!(stdout.contains(DONE), "inner test did not run: {stdout}");
    }
    std::fs::remove_dir_all(dump).unwrap();
}

struct Stand {
    root: PathBuf,
    cfg: HostConfig,
}
impl Stand {
    fn new(successor: bool) -> Self {
        let root = std::env::temp_dir().canonicalize().unwrap().join(opaque_id("child-env-").unwrap());
        for d in ["vendor/bin", "vendor/codex-path", "vendor/codex-resources", "account", "probe"] {
            std::fs::create_dir_all(root.join(d)).unwrap();
        }
        std::fs::write(root.join("vendor/codex-package.json"), b"{}\n").unwrap();
        let bin = root.join("vendor/bin/codex");
        std::fs::write(&bin, r#"#!/usr/bin/env python3
import os,sys,json
def dump(kind):
 with open(os.path.join(os.environ['CHIRALITY_CHILD_ENV_DUMP'],kind+'.json'),'w') as f: json.dump(dict(os.environ),f)
if '--version' in sys.argv:
 dump('probe'); print('codex-cli 0.167.0'); sys.exit(0)
dump('server')
for line in sys.stdin:
 f=json.loads(line)
 if 'id' in f:
  print(json.dumps({'id':f['id'],'result':{'userAgent':'codex/0.167.0'}}),flush=True)
"#).unwrap();
        std::fs::set_permissions(&bin, std::fs::Permissions::from_mode(0o700)).unwrap();
        let mut cfg = HostConfig::new(bin.clone(), root.join("account"), root.join("probe"), root.clone());
        if successor {
            cfg.distribution = Some(successor::Distribution::development_from_binary(&bin).unwrap());
        }
        cfg.allow_unverified_dev = true;
        cfg.wait_limit = Duration::from_secs(2);
        Self { root, cfg }
    }
    fn dump(&self, kind: &str) -> BTreeMap<String, String> {
        let path = PathBuf::from(std::env::var_os(DUMP).unwrap()).join(format!("{kind}.json"));
        let env = serde_json::from_slice(&std::fs::read(&path).unwrap()).unwrap();
        std::fs::remove_file(path).unwrap();
        env
    }
}
impl Drop for Stand {
    fn drop(&mut self) {
        let _ = std::fs::remove_dir_all(&self.root);
    }
}

#[test]
#[ignore = "run by child_environment_lacks_removed_names_and_keeps_the_rest_on_every_start_path with canaries in its environment"]
fn child_environment_inner_observed_on_every_start_path() {
    let expect = std::env::var(EXPECT).expect("run through the outer test");
    let present = expect == "present";
    for name in canary_names() {
        if name != RECORDED_PRESENCE_ONLY {
            assert_eq!(std::env::var(name).unwrap(), canary(name), "parent canary {name}");
        }
    }
    assert_eq!(std::env::var_os(RECORDED_PRESENCE_ONLY).is_some(), present);
    for successor in [false, true] {
        let stand = Stand::new(successor);
        let host = Arc::new(Host::new());
        host.start(&stand.cfg, "fixture").unwrap();
        let snapshot = host.snapshot();
        let path = if successor { "successor" } else { "ordinary" };
        let mut expected_removed: Vec<&str> = removed_environment_names().collect();
        if successor {
            expected_removed.extend(WRAPPER);
        }
        let dumps: BTreeMap<_, _> = ["probe", "server"].into_iter().map(|kind| (kind, stand.dump(kind))).collect();
        for (kind, env) in &dumps {
            for name in &expected_removed {
                assert!(!env.contains_key(*name), "{path} {kind}: {name} reached the child");
            }
            for (name, _) in REMOVED_ENVIRONMENT.iter().filter(|(_, c)| *c == RemovalClass::CredentialVariable) {
                assert!(!env.contains_key(*name), "{path} {kind}: earlier credential name {name} reached the child");
            }
            assert_eq!(env.get(CA), Some(&canary(CA)), "{path} {kind}: {CA} not kept");
            assert_eq!(env.get(VISIBLE).map(String::as_str), Some("ordinary"), "{path} {kind}: unrelated variable not kept");
            assert_eq!(env.get(RECORDED_PRESENCE_ONLY), present.then(|| canary(RECORDED_PRESENCE_ONLY)).as_ref(), "{path} {kind}: presence-only variable changed");
            if !successor {
                for name in WRAPPER {
                    assert_eq!(env.get(name), Some(&canary(name)), "ordinary {kind}: {name} is removed only by the successor plan");
                }
            }
        }
        // The record names exactly what the app-server child lacks among the
        // names the parent set, and nothing else.
        let server = &dumps["server"];
        let observed: Vec<&str> = canary_names().into_iter().filter(|n| std::env::var_os(n).is_some() && !server.contains_key(*n)).collect();
        let conf = &snapshot["configurationIdentity"];
        let recorded: Vec<&str> = conf["removedEnvironment"].as_array().unwrap().iter().map(|v| v.as_str().unwrap()).collect();
        assert_eq!(recorded, expected_removed, "{path}: recorded list");
        let mut a = recorded.clone();
        a.sort();
        let mut b = observed.clone();
        b.sort();
        assert_eq!(a, b, "{path}: recorded removals differ from the child's observed environment");
        let classes = conf["removedEnvironmentClasses"].as_array().unwrap();
        assert_eq!(classes.len(), recorded.len());
        for (entry, name) in classes.iter().zip(&recorded) {
            assert_eq!(entry["name"], *name);
            let class = REMOVED_ENVIRONMENT.iter().find(|(n, _)| n == name).map(|(_, c)| *c).unwrap_or(RemovalClass::LauncherWrapper);
            assert_eq!(entry["class"], class.code(), "{path}: class of {name}");
            assert!(entry["reason"].as_str().unwrap().contains("by name"));
        }
        assert_eq!(conf["inheritedEnvironmentPresence"][RECORDED_PRESENCE_ONLY]["inAppEnvironmentAtStart"], expect.as_str());
        assert_eq!(snapshot["versionIdentity"]["configurationIdentity"], *conf);
        let text = serde_json::to_string(&snapshot).unwrap();
        assert!(!text.contains("SYNTHETIC-CANARY"), "{path}: a canary value was recorded");
        host.stop("fixture", "done").unwrap();
    }
    println!("{DONE}");
}

#[test]
fn removal_classes_and_secret_redactions_are_by_name() {
    let earlier = ["OPENAI_API_KEY", "CODEX_API_KEY", "CODEX_ACCESS_TOKEN", "OPENAI_ORG_ID", "OPENAI_PROJECT_ID", "AZURE_OPENAI_API_KEY", "ANTHROPIC_API_KEY"];
    let names: Vec<_> = removed_environment_names().collect();
    assert_eq!(&names[..7], &earlier, "the earlier seven stay removed, first and in order");
    let mut unique = names.clone();
    unique.sort();
    unique.dedup();
    assert_eq!(unique.len(), names.len());
    assert_eq!(names.len(), 24);
    for kept in [CA, RECORDED_PRESENCE_ONLY, "CODEX_EXEC_SERVER_URL"] {
        assert!(!names.contains(&kept), "{kept} must not be removed");
    }
    let secret = secret_environment_names();
    for name in earlier {
        assert!(secret.contains(&name), "existing redaction {name} kept");
    }
    for (name, class) in REMOVED_ENVIRONMENT {
        assert_eq!(secret.contains(name), matches!(class, RemovalClass::CredentialVariable | RemovalClass::CredentialBearing), "{name}");
    }
    let (plain, classes) = removed_environment_record(&WRAPPER);
    assert_eq!(plain.len(), 26);
    assert_eq!(classes[25]["class"], "launcher-wrapper");
    for absent in [false, true] {
        let record = presence_only_record(!absent);
        assert_eq!(record[RECORDED_PRESENCE_ONLY]["inAppEnvironmentAtStart"], if absent { "absent" } else { "present" });
    }
}
