//! The development model address (DEL-01-05).
//!
//! A development build can be told, by the startup input
//! `CHIRALITY_DEV_OPENAI_BASE_URL`, to pass a same-machine address to the
//! account home's Codex as the command-line session setting
//! `openai_base_url`. At the pin a session setting outranks the person's and
//! the project's configuration files, so the built-in provider's model
//! requests go to that address whatever a file in the home says. A system
//! managed configuration and managed preferences outrank a session setting
//! (supplier `codex-rs/config/src/loader/mod.rs`), so a home is not started
//! with the setting while either is present. The release configuration never
//! consults the input (`development_inputs_admitted` in `lib.rs`).
//!
//! What this holds: where the built-in provider's model requests are
//! addressed, and its model list unless a model catalogue address is
//! configured. What it does not hold: that catalogue address
//! (`model_providers.openai.model_catalog_url`), sign-in, token,
//! plugin, connector and analytics addresses, clients the supplier builds for
//! direct routing, redirects, and anything Codex itself starts. Loopback
//! restricts where the request goes; it does not make whatever listens there
//! trusted.
//!
//! A home started with the setting must hold no credential, because the
//! listener may be a stand-in that records what it receives. So: a home whose
//! start configuration carries the setting is not started while its sign-in
//! file is present (by name only, never opened); sign-in is refused in it; and
//! the separate key home is not prepared at all. Not held: a sign-in kept in
//! the login keychain, and a file placed from outside the App after the last
//! check (a start refused for that at App start-up, after the setting was
//! applied, does not show its reason until the person starts Codex).

use crate::hosting::HostConfig;
use std::ffi::OsString;

/// The startup input's name.
pub(crate) const INPUT: &str = "CHIRALITY_DEV_OPENAI_BASE_URL";
/// The session setting's key, as passed to Codex after `-c`.
const SETTING: &str = "openai_base_url=";

pub(crate) const INVALID: &str = "The development model address in CHIRALITY_DEV_OPENAI_BASE_URL is not a literal same-machine address (http or https on 127.0.0.1 or [::1], with an optional port and a plain path). Codex was not started.";
pub(crate) const HOLDS_SIGN_IN: &str = "This development launch sends this home's model requests to a local stand-in, and the home holds a sign-in file, or it could not be established that it holds none. Codex was not started in it.";
pub(crate) const MANAGED: &str = "This development launch sends this home's model requests to a local stand-in, and a system or managed Codex configuration, which could send them elsewhere, is present, or it could not be established that none is. Codex was not started in it.";
pub(crate) const SIGN_IN_OFF: &str = "This development launch sends the account home's model requests to a local stand-in, so sign-in is off. Nothing was sent.";
pub(crate) const KEY_ENTRY_OFF: &str = "This development launch sends the account home's model requests to a local stand-in, so key entry is off. No key home was prepared or started.";

/// A literal loopback address and nothing else: `http://` or `https://`, then
/// `127.0.0.1` or `[::1]`, an optional port from 1 to 65535 with no leading
/// zero, and an optional path of letters, digits and `. _ ~ / -`. No name is
/// accepted (`localhost` included), so nothing is resolved; no user or
/// password part, query or fragment. Every accepted byte is safe inside a TOML
/// basic string and a session-setting argument. The rule is the local model
/// address rule.
pub(crate) fn loopback_address(text: &str) -> bool {
    if text.len() > 2048 {
        return false;
    }
    let Some(rest) = text
        .strip_prefix("http://")
        .or_else(|| text.strip_prefix("https://"))
    else {
        return false;
    };
    let Some(rest) = rest
        .strip_prefix("127.0.0.1")
        .or_else(|| rest.strip_prefix("[::1]"))
    else {
        return false;
    };
    let (port, path) = rest.split_at(rest.find('/').unwrap_or(rest.len()));
    if !port.is_empty() {
        let Some(digits) = port.strip_prefix(':') else {
            return false;
        };
        if digits.is_empty()
            || digits.len() > 5
            || digits.starts_with('0')
            || !digits.bytes().all(|b| b.is_ascii_digit())
            || !digits.parse::<u32>().is_ok_and(|p| (1..=65535).contains(&p))
        {
            return false;
        }
    }
    path.bytes()
        .all(|b| b.is_ascii_alphanumeric() || b"._~/-".contains(&b))
}

/// Applied once, at startup, to the account home's start configuration.
///
/// `admitted` is `development_inputs_admitted`: when it is false the input is
/// not consulted at all. When the input is set, its value is passed as a
/// session setting if it is a literal loopback address; any other value is a
/// refusal, never a fallback to unset. The start conditions are checked here
/// as well as at every start, so that at startup the reason is the home's
/// stated configuration problem and not a start that silently did not happen.
/// An earlier refusal of the configuration is kept as it was.
pub(crate) fn apply(
    config: Result<HostConfig, String>,
    admitted: bool,
    input: impl Fn(&str) -> Option<OsString>,
) -> Result<HostConfig, String> {
    if !admitted {
        return config;
    }
    let Some(value) = input(INPUT) else {
        return config;
    };
    let mut config = config?;
    let value = value
        .into_string()
        .ok()
        .filter(|value| loopback_address(value))
        .ok_or(INVALID)?;
    config.session_flags.push(format!("{SETTING}\"{value}\""));
    check_start(&config)?;
    Ok(config)
}

/// Whether this start configuration carries the setting. Only `apply` puts it
/// there, so in the release configuration this is never true.
pub(crate) fn set(config: &HostConfig) -> bool {
    config
        .session_flags
        .iter()
        .any(|flag| flag.starts_with(SETTING))
}

/// Before every start: a home whose Codex would carry the setting is started
/// only when no system or managed Codex configuration is present (either
/// outranks a session setting) and its sign-in file is established absent.
/// The sign-in file is looked at by name only (`symlink_metadata`, which
/// cannot open it). Anything other than "not found" refuses, an unreadable
/// folder included.
pub(crate) fn check_start(config: &HostConfig) -> Result<(), String> {
    check_start_with(config, crate::native_local_provider::require_no_admin_layers)
}
fn check_start_with(
    config: &HostConfig,
    no_managed_configuration: impl FnOnce() -> Result<(), String>,
) -> Result<(), String> {
    if !set(config) {
        return Ok(());
    }
    no_managed_configuration().map_err(|_| MANAGED)?;
    // The home the child uses: it is given `config.cwd` as its working folder and resolves a
    // relative CODEX_HOME there, so the sign-in file is looked for in the folder resolved the same way.
    match std::fs::symlink_metadata(config.cwd.join(&config.codex_home).join("auth.json")) {
        Err(error) if error.kind() == std::io::ErrorKind::NotFound => Ok(()),
        _ => Err(HOLDS_SIGN_IN.into()),
    }
}

/// Sign-in is off in a home whose Codex carries the setting.
pub(crate) fn check_sign_in(config: &Result<HostConfig, String>) -> Result<(), String> {
    match config {
        Ok(config) if set(config) => Err(SIGN_IN_OFF.into()),
        _ => Ok(()),
    }
}

/// The separate key home's start configuration is cloned from the account
/// home's, so it would carry the setting too. It is not prepared or started
/// at all while the account home carries it.
pub(crate) fn check_key_home(account: &Result<HostConfig, String>) -> Result<(), String> {
    match account {
        Ok(config) if set(config) => Err(KEY_ENTRY_OFF.into()),
        _ => Ok(()),
    }
}

#[cfg(all(test, unix))]
mod tests {
    use super::*;
    use crate::hosting::Host;
    use std::os::unix::fs::PermissionsExt;
    use std::path::{Path, PathBuf};
    use std::sync::atomic::{AtomicUsize, Ordering};
    use std::sync::Arc;
    use std::time::Duration;

    const ADDRESS: &str = "http://127.0.0.1:9/v1";

    /// A stand-in supplier that records the arguments it was started with and
    /// answers `initialize`. Never the real supplier.
    fn fixture() -> (PathBuf, HostConfig) {
        let root = std::fs::canonicalize(std::env::temp_dir())
            .unwrap()
            .join(crate::util::opaque_id("dev-model-address-").unwrap());
        for name in ["account", "probe"] {
            std::fs::create_dir_all(root.join(name)).unwrap();
        }
        let peer = root.join("owned-peer.py");
        std::fs::write(
            &peer,
            r#"#!/usr/bin/python3
import sys,json,os
here=os.path.dirname(os.path.abspath(__file__))
if '--version' in sys.argv:
    print('codex-cli 0.167.0'); sys.exit(0)
with open(os.path.join(here,'argv.jsonl'),'a') as f: f.write(json.dumps(sys.argv[1:])+'\n')
for line in sys.stdin:
    frame=json.loads(line)
    if frame.get('method')=='initialize':
        sys.stdout.write(json.dumps({'id':frame['id'],'result':{'userAgent':'unqualified-root-owned-fixture'}})+'\n'); sys.stdout.flush()
"#,
        )
        .unwrap();
        std::fs::set_permissions(&peer, std::fs::Permissions::from_mode(0o700)).unwrap();
        let mut cfg = HostConfig::new(peer, root.join("account"), root.join("probe"), root.clone());
        cfg.allow_unverified_dev = true;
        cfg.wait_limit = Duration::from_secs(5);
        (root, cfg)
    }
    /// The arguments of every start of the stand-in supplier, in order.
    fn started_with(root: &Path) -> Vec<Vec<String>> {
        std::fs::read_to_string(root.join("argv.jsonl"))
            .unwrap_or_default()
            .lines()
            .map(|line| serde_json::from_str(line).unwrap())
            .collect()
    }
    fn carries_setting(arguments: &[String]) -> bool {
        arguments.iter().any(|argument| argument.contains("openai_base_url"))
    }
    fn given(value: &'static str) -> impl Fn(&str) -> Option<OsString> {
        move |name| (name == INPUT).then(|| OsString::from(value))
    }

    #[test]
    fn dev_model_address_accepts_only_a_literal_loopback_address() {
        for ok in [
            "http://127.0.0.1",
            "http://127.0.0.1:9/v1",
            "https://127.0.0.1:65535/v1",
            "http://[::1]:8000/v1",
            "https://[::1]",
            "http://127.0.0.1:1/a/b-c_d.e~f/",
        ] {
            assert!(loopback_address(ok), "{ok}");
        }
        for bad in [
            "",
            // No name is resolved: localhost and every other name are refused.
            "http://localhost:9/v1",
            "http://localhost.:9/v1",
            "http://example.invalid/v1",
            "http://127.0.0.1.example.invalid/v1",
            "http://127.0.0.1example.invalid/v1",
            // Other addresses, including other loopback spellings.
            "http://127.0.0.2:9/v1",
            "http://127.1:9/v1",
            "http://0.0.0.0:9/v1",
            "http://192.168.1.5:9/v1",
            "http://[::ffff:127.0.0.1]:9/v1",
            "http://[0:0:0:0:0:0:0:1]:9/v1",
            "http://::1:9/v1",
            // No user or password part.
            "http://user@127.0.0.1:9/v1",
            "http://user:secret@127.0.0.1:9/v1",
            "http://127.0.0.1@example.invalid/v1",
            "http://127.0.0.1:9@example.invalid/v1",
            // Scheme.
            "127.0.0.1:9/v1",
            "ftp://127.0.0.1:9/v1",
            "ws://127.0.0.1:9/v1",
            "HTTP://127.0.0.1:9/v1",
            // Port.
            "http://127.0.0.1:/v1",
            "http://127.0.0.1:0/v1",
            "http://127.0.0.1:09/v1",
            "http://127.0.0.1:65536/v1",
            "http://127.0.0.1:99999/v1",
            "http://127.0.0.1:9x/v1",
            // Query, fragment, quoting and space.
            "http://127.0.0.1:9/v1?x=1",
            "http://127.0.0.1:9/v1#f",
            "http://127.0.0.1:9/v1\"",
            "http://127.0.0.1:9/v1\\",
            " http://127.0.0.1:9/v1",
            "http://127.0.0.1:9/v1 ",
            "http://127.0.0.1:9/v1\n",
            "http://127.0.0.1:9/%2e",
        ] {
            assert!(!loopback_address(bad), "{bad:?}");
        }
        assert!(!loopback_address(&format!("http://127.0.0.1/{}", "a".repeat(2048))));
    }

    #[test]
    fn dev_model_address_apply_passes_a_valid_value_refuses_any_other_and_is_not_consulted_when_not_admitted() {
        let (root, cfg) = fixture();
        // Unset: nothing changes, and only this one name was asked for.
        let asked = AtomicUsize::new(0);
        let unset = apply(Ok(cfg.clone()), true, |name| {
            assert_eq!(name, INPUT);
            asked.fetch_add(1, Ordering::SeqCst);
            None
        })
        .unwrap();
        assert_eq!((unset.session_flags.clone(), asked.load(Ordering::SeqCst)), (cfg.session_flags.clone(), 1));
        assert!(!set(&unset));
        // Set and valid: exactly one setting is added, after the existing ones.
        let applied = apply(Ok(cfg.clone()), true, given(ADDRESS)).unwrap();
        let mut expected = cfg.session_flags.clone();
        expected.push("openai_base_url=\"http://127.0.0.1:9/v1\"".into());
        assert_eq!(applied.session_flags, expected);
        assert!(set(&applied));
        // Set and anything else: a refusal with the fixed reason, never a fallback to unset.
        for bad in ["", "http://localhost:9/v1", "https://api.example.invalid/v1", "http://user@127.0.0.1:9/v1", "unset", "0"] {
            assert_eq!(apply(Ok(cfg.clone()), true, given(bad)).unwrap_err(), INVALID, "{bad:?}");
        }
        #[cfg(unix)]
        {
            use std::os::unix::ffi::OsStringExt;
            let not_text = OsString::from_vec(b"http://127.0.0.1:9/\xff".to_vec());
            assert_eq!(apply(Ok(cfg.clone()), true, move |_| Some(not_text.clone())).unwrap_err(), INVALID);
        }
        // An earlier refusal is kept as it was.
        assert_eq!(apply(Err("earlier".into()), true, given(ADDRESS)).unwrap_err(), "earlier");
        // Not admitted: the input is never consulted and nothing changes.
        let untouched = apply(Ok(cfg.clone()), false, |_| panic!("the input must not be consulted")).unwrap();
        assert_eq!(untouched.session_flags, cfg.session_flags);
        std::fs::remove_dir_all(root).unwrap();
    }

    #[test]
    fn dev_model_address_reaches_the_arguments_the_supplier_is_started_with_and_the_configuration_identity() {
        // Unset: the stand-in supplier is started without the setting.
        let (root, cfg) = fixture();
        let host = Arc::new(Host::new());
        host.start(&apply(Ok(cfg.clone()), true, |_| None).unwrap(), "fixture").unwrap();
        let starts = started_with(&root);
        assert_eq!(starts.len(), 1);
        assert!(!carries_setting(&starts[0]), "{starts:?}");
        assert!(!host.snapshot()["configurationIdentity"].to_string().contains("openai_base_url"));
        host.stop("fixture", "test ended").unwrap();
        std::fs::remove_dir_all(root).unwrap();
        // Set: the setting is on the command line, as `-c openai_base_url="..."`, at every
        // start of that home, and the configuration identity records it with its value.
        let (root, cfg) = fixture();
        let cfg = apply(Ok(cfg), true, given(ADDRESS)).unwrap();
        let host = Arc::new(Host::new());
        host.start(&cfg, "fixture").unwrap();
        host.stop("fixture", "restart").unwrap();
        host.start(&cfg, "fixture restart").unwrap();
        let starts = started_with(&root);
        assert_eq!(starts.len(), 2);
        for arguments in &starts {
            let at = arguments.iter().position(|a| a == "openai_base_url=\"http://127.0.0.1:9/v1\"").expect("the setting is passed");
            assert_eq!(arguments[at - 1], "-c");
            assert_eq!(arguments.last().map(String::as_str), Some("app-server"));
            assert_eq!(arguments.iter().filter(|a| a.contains("openai_base_url")).count(), 1);
        }
        let identity = host.snapshot()["configurationIdentity"].clone();
        assert!(identity["sessionFlags"].as_array().unwrap().iter().any(|f| f == "openai_base_url=\"http://127.0.0.1:9/v1\""), "{identity}");
        host.stop("fixture", "test ended").unwrap();
        std::fs::remove_dir_all(root).unwrap();
    }

    #[test]
    fn dev_model_address_does_not_start_a_home_that_holds_a_sign_in_file() {
        let (root, cfg) = fixture();
        let cfg = apply(Ok(cfg), true, given(ADDRESS)).unwrap();
        let sign_in = cfg.codex_home.join("auth.json");
        // Present: refused before the supplier or its label probe is started, and at
        // startup the configuration itself is refused with the same reason.
        std::fs::write(&sign_in, b"INVENTED").unwrap();
        let mut plain = cfg.clone();
        plain.session_flags.pop();
        assert!(!set(&plain));
        assert_eq!(apply(Ok(plain), true, given(ADDRESS)).unwrap_err(), HOLDS_SIGN_IN);
        let host = Arc::new(Host::new());
        assert_eq!(host.start(&cfg, "fixture").unwrap_err(), HOLDS_SIGN_IN);
        assert!(started_with(&root).is_empty());
        assert!(host.snapshot()["generation"].is_null());
        // A dangling link by that name is still a present name.
        std::fs::remove_file(&sign_in).unwrap();
        std::os::unix::fs::symlink(root.join("nowhere"), &sign_in).unwrap();
        assert_eq!(check_start(&cfg).unwrap_err(), HOLDS_SIGN_IN);
        std::fs::remove_file(&sign_in).unwrap();
        // A folder that cannot be searched: absence is not established, so it refuses.
        std::fs::set_permissions(&cfg.codex_home, std::fs::Permissions::from_mode(0o000)).unwrap();
        let unreadable = check_start(&cfg);
        std::fs::set_permissions(&cfg.codex_home, std::fs::Permissions::from_mode(0o700)).unwrap();
        assert_eq!(unreadable.unwrap_err(), HOLDS_SIGN_IN);
        // Absent: it starts, with the setting.
        host.start(&cfg, "fixture").unwrap();
        assert!(carries_setting(&started_with(&root)[0]));
        host.stop("fixture", "test ended").unwrap();
        // A system or managed Codex configuration outranks the setting: present, or not
        // established absent, refuses, before the sign-in file is considered.
        assert_eq!(check_start_with(&cfg, || Err("present".into())).unwrap_err(), MANAGED);
        assert!(check_start_with(&cfg, || Ok(())).is_ok());
        // Without the setting neither is looked at and the home starts as before.
        let (plain_root, plain) = fixture();
        std::fs::write(plain.codex_home.join("auth.json"), b"INVENTED").unwrap();
        assert!(check_start(&plain).is_ok());
        assert!(check_start_with(&plain, || panic!("not consulted without the setting")).is_ok());
        let host = Arc::new(Host::new());
        host.start(&plain, "fixture").unwrap();
        host.stop("fixture", "test ended").unwrap();
        for root in [root, plain_root] {
            std::fs::remove_dir_all(root).unwrap();
        }
    }

    /// A relative home is the folder the child resolves it to, under the working folder it is
    /// given, not a folder of that name under the App's own working folder: the sign-in file is
    /// looked for there, at startup and before every start.
    #[test]
    fn dev_model_address_looks_for_the_sign_in_file_where_the_child_resolves_a_relative_home() {
        let (root, cfg) = fixture();
        let mut relative = apply(Ok(cfg), true, given(ADDRESS)).unwrap();
        relative.cwd = root.clone();
        relative.codex_home = PathBuf::from("account");
        assert!(!std::env::current_dir().unwrap().join("account").join("auth.json").exists());
        std::fs::write(root.join("account").join("auth.json"), b"INVENTED").unwrap();
        assert_eq!(check_start(&relative).unwrap_err(), HOLDS_SIGN_IN);
        let mut plain = relative.clone();
        plain.session_flags.pop();
        assert_eq!(apply(Ok(plain), true, given(ADDRESS)).unwrap_err(), HOLDS_SIGN_IN);
        let host = Arc::new(Host::new());
        assert_eq!(host.start(&relative, "fixture").unwrap_err(), HOLDS_SIGN_IN);
        assert!(started_with(&root).is_empty());
        std::fs::remove_dir_all(root).unwrap();
    }

    #[test]
    fn dev_model_address_turns_sign_in_and_the_key_home_off_only_where_the_setting_is() {
        let (root, cfg) = fixture();
        let with = Ok(apply(Ok(cfg.clone()), true, given(ADDRESS)).unwrap());
        assert_eq!(check_sign_in(&with).unwrap_err(), SIGN_IN_OFF);
        assert_eq!(check_key_home(&with).unwrap_err(), KEY_ENTRY_OFF);
        for without in [Ok(cfg), Err("no supplier".to_owned())] {
            assert!(check_sign_in(&without).is_ok() && check_key_home(&without).is_ok());
        }
        std::fs::remove_dir_all(root).unwrap();
    }

    /// The release configuration: built with `distribution-successor` and not a development
    /// run. With the input present in the process environment, read through the same reader
    /// startup uses, nothing of this module applies: the supplier's arguments carry no
    /// built-in provider address on any start, a home holding a sign-in file starts as it
    /// always did, and sign-in and the key home are not refused.
    #[cfg(feature = "distribution-successor")]
    #[test]
    fn dev_model_address_release_configuration_applies_none_of_it_with_the_input_in_the_environment() {
        assert!(!crate::development_inputs_admitted(false), "built with the feature and not a development run");
        assert!(crate::development_inputs_admitted(true), "a development run of the same build admits them");
        std::env::set_var(INPUT, ADDRESS);
        let (root, cfg) = fixture();
        let asked = AtomicUsize::new(0);
        let released = apply(Ok(cfg.clone()), crate::development_inputs_admitted(false), |name| {
            asked.fetch_add(1, Ordering::SeqCst);
            std::env::var_os(name)
        })
        .unwrap();
        assert_eq!(asked.load(Ordering::SeqCst), 0, "the environment is not consulted");
        assert_eq!(released.session_flags, cfg.session_flags);
        std::fs::write(released.codex_home.join("auth.json"), b"INVENTED").unwrap();
        let host = Arc::new(Host::new());
        host.start(&released, "fixture").unwrap();
        host.stop("fixture", "restart").unwrap();
        host.start(&released, "fixture restart").unwrap();
        let starts = started_with(&root);
        assert_eq!(starts.len(), 2);
        assert!(starts.iter().all(|arguments| !carries_setting(arguments)), "{starts:?}");
        assert!(!host.snapshot()["configurationIdentity"].to_string().contains("openai_base_url"));
        let released = Ok(released);
        assert!(check_sign_in(&released).is_ok() && check_key_home(&released).is_ok());
        host.stop("fixture", "test ended").unwrap();
        // The same environment, a development run of the same build: admitted, and there
        // the sign-in file refuses.
        assert_eq!(apply(Ok(cfg.clone()), crate::development_inputs_admitted(true), |name| std::env::var_os(name)).unwrap_err(), HOLDS_SIGN_IN);
        std::fs::remove_file(cfg.codex_home.join("auth.json")).unwrap();
        let admitted = apply(Ok(cfg), crate::development_inputs_admitted(true), |name| std::env::var_os(name)).unwrap();
        assert!(set(&admitted));
        std::env::remove_var(INPUT);
        std::fs::remove_dir_all(root).unwrap();
    }
}
