//! Inherited-environment removals observed from the child's side on every
//! supplier start path, and the configuration identity that records them.
//! A stand-in supplier (a Python script) dumps its own environment; the real
//! supplier is never executed.
use super::*;
use std::collections::BTreeMap;
use std::os::unix::fs::PermissionsExt;

/// The decided removals, held here as this test's own literals and not read
/// from the host's table: each name with the class code the record gives it.
/// Every expectation below comes from these lists; the host's table is compared
/// with them once, in `the_hosts_table_is_the_decided_list`.
pub(super) const DECIDED: [(&str, &str); 24] = [
    ("OPENAI_API_KEY", "credential-custody/credential-variable"),
    ("CODEX_API_KEY", "credential-custody/credential-variable"),
    ("CODEX_ACCESS_TOKEN", "credential-custody/credential-variable"),
    ("OPENAI_ORG_ID", "credential-custody/credential-variable"),
    ("OPENAI_PROJECT_ID", "credential-custody/credential-variable"),
    ("AZURE_OPENAI_API_KEY", "credential-custody/credential-variable"),
    ("ANTHROPIC_API_KEY", "credential-custody/credential-variable"),
    ("CODEX_AUTH", "credential-custody/credential-bearing"),
    ("CODEX_CONNECTORS_TOKEN", "credential-custody/credential-bearing"),
    ("CODEX_GITHUB_PERSONAL_ACCESS_TOKEN", "credential-custody/credential-bearing"),
    ("CODEX_GUARDIAN_DECISIONS_API_KEY", "credential-custody/credential-bearing"),
    ("CODEX_EXEC_SERVER_NOISE_AUTH_TOKEN", "credential-custody/credential-bearing"),
    ("CODEX_APP_SERVER_LOGIN_ISSUER", "credential-custody/sign-in-or-token-refresh"),
    ("CODEX_APP_SERVER_LOGIN_CLIENT_ID", "credential-custody/sign-in-or-token-refresh"),
    ("CODEX_AUTHAPI_BASE_URL", "credential-custody/sign-in-or-token-refresh"),
    ("CODEX_REFRESH_TOKEN_URL_OVERRIDE", "credential-custody/sign-in-or-token-refresh"),
    ("CODEX_REVOKE_TOKEN_URL_OVERRIDE", "credential-custody/sign-in-or-token-refresh"),
    ("CODEX_AGENT_IDENTITY_AUTHAPI_BASE_URL", "credential-custody/sign-in-or-token-refresh"),
    ("CODEX_AGENT_IDENTITY_JWKS_BASE_URL", "credential-custody/sign-in-or-token-refresh"),
    ("CODEX_APP_SERVER_CHATGPT_BASE_URL", "credential-custody/sign-in-or-token-refresh"),
    ("CODEX_SQLITE_HOME", "home-separation"),
    ("CODEX_ROLLOUT_TRACE_ROOT", "home-separation"),
    ("CODEX_PLUGIN_METRICS_OUTPUT", "home-separation"),
    ("CODEX_TUI_SESSION_LOG_PATH", "home-separation"),
];
/// The names whose values a configuration record treats as secret: the earlier
/// seven credential variables and the five credential-bearing names.
const DECIDED_SECRET: [&str; 12] = [
    "OPENAI_API_KEY",
    "CODEX_API_KEY",
    "CODEX_ACCESS_TOKEN",
    "OPENAI_ORG_ID",
    "OPENAI_PROJECT_ID",
    "AZURE_OPENAI_API_KEY",
    "ANTHROPIC_API_KEY",
    "CODEX_AUTH",
    "CODEX_CONNECTORS_TOKEN",
    "CODEX_GITHUB_PERSONAL_ACCESS_TOKEN",
    "CODEX_GUARDIAN_DECISIONS_API_KEY",
    "CODEX_EXEC_SERVER_NOISE_AUTH_TOKEN",
];
/// Neither set nor removed; only its presence is recorded.
const PRESENCE_ONLY: &str = "CODEX_INTERNAL_APP_SERVER_REMOTE_CONTROL_DISABLED";
/// Removed only by the successor plan.
pub(super) const WRAPPER: [&str; 2] = ["CODEX_MANAGED_PACKAGE_ROOT", "CODEX_MANAGED_BY_NPM"];
/// Decided as kept, and a name on no list: neither may be removed.
const KEPT: [&str; 2] = ["CODEX_CA_CERTIFICATE", "CODEX_EXEC_SERVER_URL"];
const VISIBLE: &str = "CHIRALITY_SYNTHETIC_VISIBLE";
const DUMP: &str = "CHIRALITY_CHILD_ENV_DUMP";
const EXPECT: &str = "CHIRALITY_CHILD_ENV_EXPECT_PRESENCE";
const DONE: &str = "CHILD-ENV-INNER-COMPLETE";
const INNER: &str = "hosting::child_environment_tests::child_environment_inner_observed_on_every_start_path";

fn canary(name: &str) -> String {
    format!("SYNTHETIC-CANARY-{name}-not-a-real-value")
}
pub(super) fn decided_names() -> impl Iterator<Item = &'static str> {
    DECIDED.iter().map(|(name, _)| *name)
}
fn sorted<'a>(names: impl IntoIterator<Item = &'a str>) -> Vec<&'a str> {
    let mut names: Vec<_> = names.into_iter().collect();
    names.sort();
    names
}
/// Every name the parent sets to a canary: the decided removals, the successor
/// wrapper settings, the kept names and the presence-only name.
fn canary_names() -> Vec<&'static str> {
    decided_names().chain(WRAPPER).chain(KEPT).chain([PRESENCE_ONLY]).collect()
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
            cmd.env_remove(PRESENCE_ONLY);
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
        if name != PRESENCE_ONLY {
            assert_eq!(std::env::var(name).unwrap(), canary(name), "parent canary {name}");
        }
    }
    assert_eq!(std::env::var_os(PRESENCE_ONLY).is_some(), present);
    for successor in [false, true] {
        let stand = Stand::new(successor);
        let host = Arc::new(Host::new());
        host.start(&stand.cfg, "fixture").unwrap();
        let snapshot = host.snapshot();
        let path = if successor { "successor" } else { "ordinary" };
        let expected: Vec<(&str, &str)> = DECIDED.iter().copied().chain(WRAPPER.iter().filter(|_| successor).map(|name| (*name, "launcher-wrapper"))).collect();
        let dumps: BTreeMap<_, _> = ["probe", "server"].into_iter().map(|kind| (kind, stand.dump(kind))).collect();
        for (kind, env) in &dumps {
            for (name, _) in &expected {
                assert!(!env.contains_key(*name), "{path} {kind}: {name} reached the child");
            }
            for name in KEPT {
                assert_eq!(env.get(name), Some(&canary(name)), "{path} {kind}: {name} not kept");
            }
            assert_eq!(env.get(VISIBLE).map(String::as_str), Some("ordinary"), "{path} {kind}: unrelated variable not kept");
            assert_eq!(env.get(PRESENCE_ONLY), present.then(|| canary(PRESENCE_ONLY)).as_ref(), "{path} {kind}: presence-only variable changed");
            if !successor {
                for name in WRAPPER {
                    assert_eq!(env.get(name), Some(&canary(name)), "ordinary {kind}: {name} is removed only by the successor plan");
                }
            }
        }
        // The record names exactly the decided removals, and exactly what the
        // app-server child lacks among the names the parent set.
        let server = &dumps["server"];
        let observed = sorted(canary_names().into_iter().filter(|n| std::env::var_os(n).is_some() && !server.contains_key(*n)));
        let conf = &snapshot["configurationIdentity"];
        let recorded: Vec<&str> = conf["removedEnvironment"].as_array().unwrap().iter().map(|v| v.as_str().unwrap()).collect();
        assert_eq!(sorted(recorded.iter().copied()), sorted(expected.iter().map(|(name, _)| *name)), "{path}: recorded list is not the decided list");
        assert_eq!(sorted(recorded.iter().copied()), observed, "{path}: recorded removals differ from the child's observed environment");
        // Each decided name has exactly one class entry, with its decided class.
        let classes = conf["removedEnvironmentClasses"].as_array().unwrap();
        assert_eq!(classes.len(), expected.len(), "{path}: class entries");
        for (name, class) in &expected {
            let entries: Vec<_> = classes.iter().filter(|entry| entry["name"] == *name).collect();
            assert_eq!(entries.len(), 1, "{path}: class entries for {name}");
            assert_eq!(entries[0]["class"], *class, "{path}: class of {name}");
            assert!(entries[0]["reason"].as_str().unwrap().contains("by name"));
        }
        let presence = conf["inheritedEnvironmentPresence"].as_object().unwrap();
        assert_eq!(presence.keys().collect::<Vec<_>>(), [PRESENCE_ONLY]);
        assert_eq!(presence[PRESENCE_ONLY]["inAppEnvironmentAtStart"], expect.as_str());
        assert_eq!(snapshot["versionIdentity"]["configurationIdentity"], *conf);
        let text = serde_json::to_string(&snapshot).unwrap();
        assert!(!text.contains("SYNTHETIC-CANARY"), "{path}: a canary value was recorded");
        host.stop("fixture", "done").unwrap();
    }
    println!("{DONE}");
}

/// The one place the host's table is read: it must be the decided list, name
/// for name and class for class, with the decided redactions and presence name.
#[test]
fn the_hosts_table_is_the_decided_list() {
    assert_eq!(sorted(decided_names()).windows(2).filter(|pair| pair[0] == pair[1]).count(), 0, "a decided name is listed twice");
    let mut table: Vec<(&str, &str)> = REMOVED_ENVIRONMENT.iter().map(|(name, class)| (*name, class.code())).collect();
    table.sort();
    let mut decided = DECIDED.to_vec();
    decided.sort();
    assert_eq!(table, decided);
    assert_eq!(sorted(removed_environment_names()), sorted(decided_names()));
    assert_eq!(sorted(secret_environment_names()), sorted(DECIDED_SECRET));
    for name in DECIDED_SECRET {
        let class = DECIDED.iter().find(|(n, _)| *n == name).unwrap().1;
        assert!(class == "credential-custody/credential-variable" || class == "credential-custody/credential-bearing", "{name}");
    }
    assert_eq!(DECIDED.iter().filter(|(_, class)| class.starts_with("credential-custody/credential-")).count(), DECIDED_SECRET.len());
    assert_eq!(RECORDED_PRESENCE_ONLY, PRESENCE_ONLY);
    for name in KEPT.into_iter().chain([PRESENCE_ONLY]).chain(WRAPPER) {
        assert!(!removed_environment_names().any(|listed| listed == name), "{name} must not be on the host's list");
    }
    let (plain, classes) = removed_environment_record(&WRAPPER);
    assert_eq!(sorted(plain.iter().copied()), sorted(decided_names().chain(WRAPPER)));
    for name in WRAPPER {
        let entry = classes.iter().find(|entry| entry["name"] == name).unwrap();
        assert_eq!(entry["class"], "launcher-wrapper");
    }
    for present in [true, false] {
        let record = presence_only_record(present);
        assert_eq!(record[PRESENCE_ONLY]["inAppEnvironmentAtStart"], if present { "present" } else { "absent" });
    }
}
