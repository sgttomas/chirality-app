//! Observations of the pinned supplier itself, started through the host's own start.
//!
//! These tests need CHIRALITY_CODEX_BIN (the stock 0.167.0 binary), as `tests/handshake.rs`
//! does, and keep its rule: without it they fail, unless CHIRALITY_SKIP_CODEX=1 is set
//! explicitly. A skipped run is not an observation. Every folder is invented and made below
//! `std::env::temp_dir()`: a fresh Codex home nobody has signed in to, never a real one. No
//! sign-in, no credential, no model turn.
//!
//! What each test establishes, and what it does not, is said on the test.

use crate::hosting::{Host, HostConfig};
use serde_json::{json, Value};
use std::path::{Path, PathBuf};
use std::sync::Arc;

/// A fresh home's configuration: plugins and analytics off, nothing else.
const FRESH_HOME: &str = "[features]\nplugins = false\n\n[analytics]\nenabled = false\n";
/// The same, with a stand-in provider at an address where nothing listens, as `tests/handshake.rs` uses.
const STAND_IN_HOME: &str = "model_provider = \"skeleton_local\"\nmodel = \"skeleton-no-model\"\n\n[model_providers.skeleton_local]\nname = \"skeleton local (no server running)\"\nbase_url = \"http://127.0.0.1:9/v1\"\nwire_api = \"responses\"\n\n[features]\nplugins = false\n\n[analytics]\nenabled = false\n";

struct Scratch(PathBuf);
impl Scratch {
    fn new(prefix: &str) -> Self {
        let root = std::env::temp_dir().canonicalize().unwrap().join(crate::util::opaque_id(prefix).unwrap());
        std::fs::create_dir(&root).unwrap();
        Self(root)
    }
    fn dir(&self, name: &str) -> PathBuf {
        let path = self.0.join(name);
        std::fs::create_dir_all(&path).unwrap();
        path
    }
}
impl Drop for Scratch {
    fn drop(&mut self) {
        let _ = std::fs::remove_dir_all(&self.0);
    }
}

/// The supplier's binary, or None where the run was skipped explicitly.
fn supplier() -> Option<String> {
    match std::env::var("CHIRALITY_CODEX_BIN") {
        Ok(bin) => Some(bin),
        Err(_) if std::env::var("CHIRALITY_SKIP_CODEX").as_deref() == Ok("1") => {
            eprintln!("SKIPPED explicitly: CHIRALITY_SKIP_CODEX=1");
            None
        }
        Err(_) => panic!("CHIRALITY_CODEX_BIN is not set (set CHIRALITY_SKIP_CODEX=1 to skip explicitly)"),
    }
}

fn config(bin: &str, home: &Path, probe: &Path, cwd: &Path) -> HostConfig {
    let mut cfg = HostConfig::new(bin.into(), home.to_path_buf(), probe.to_path_buf(), cwd.to_path_buf());
    cfg.expected_sha256 = std::env::var("CHIRALITY_CODEX_EXPECTED_SHA256").ok();
    cfg.allow_unverified_dev = true;
    cfg
}

/// The supplier's reply to a configuration reading for `cwd`, layers included: the whole reply
/// frame, so that an error reply can be told from a result.
fn reading(host: &Host, cwd: &Path) -> Value {
    host.request("config/read", json!({"cwd": cwd.to_str().unwrap(), "includeLayers": true}), json!({"kind": "person-directed"}))
        .expect("the configuration reading was written and answered")
}

fn layers(result: &Value) -> Vec<Value> {
    result["layers"].as_array().expect("the reading returned its layers").clone()
}

/// The layers the reading reports for the `.codex` folder at `dot_codex`, whatever spelling the
/// supplier gives the path.
fn project_layers_for(result: &Value, dot_codex: &Path) -> Vec<Value> {
    let wanted = dot_codex.canonicalize().unwrap();
    layers(result)
        .into_iter()
        .filter(|layer| {
            layer["name"]["type"] == "project"
                && layer["name"]["dotCodexFolder"].as_str().is_some_and(|folder| Path::new(folder).canonicalize().ok().as_deref() == Some(wanted.as_path()))
        })
        .collect()
}

fn ready(host: &Arc<Host>, cfg: &HostConfig) -> Value {
    let ready = host.start(cfg, "pinned supplier observation").expect("start reaches ready");
    assert_eq!(ready["state"], "ready");
    assert_eq!(ready["versionIdentity"]["observedVersionLabel"], "codex-cli 0.167.0", "the supplier started is the pinned one");
    assert_eq!(ready["versionIdentity"]["handshakeConsistency"], "consistent");
    ready
}

/// The pinned supplier starts and completes its handshake with the development model address
/// set, through the one place the App applies that input and the host's own start.
///
/// Establishes: `dev_model_address::apply` puts the setting on the account home's start
/// configuration; the host starts the pinned supplier with it in a fresh home; the supplier
/// accepts it (it reaches ready, and its own configuration reading reports the setting from the
/// session layer and as the effective value); the home holds no sign-in file afterwards.
///
/// Does not establish: where a model request goes (no turn is run and nothing listens at the
/// address), or that a launch made this way is contained. Those rest on the reading of the
/// supplier's source.
#[cfg(not(feature = "distribution-successor"))]
#[test]
fn the_pinned_codex_starts_with_the_development_address_set() {
    let Some(bin) = supplier() else { return };
    let scratch = Scratch::new("pinned-input-");
    let (home, probe, cwd) = (scratch.dir("home"), scratch.dir("probe"), scratch.dir("work"));
    std::fs::write(home.join("config.toml"), FRESH_HOME).unwrap();
    const ADDRESS: &str = "http://127.0.0.1:9/v1";
    let setting = format!("openai_base_url=\"{ADDRESS}\"");

    // The App's one application point, with the gate a build of this configuration has when it
    // is not a development run, and the input given as the environment would give it.
    let admitted = crate::development_inputs_admitted(false);
    assert!(admitted, "a build without the release feature admits development inputs");
    let cfg = crate::dev_model_address::apply(Ok(config(&bin, &home, &probe, &cwd)), admitted, |name| {
        (name == crate::dev_model_address::INPUT).then(|| ADDRESS.into())
    })
    .expect("a literal same-machine address in a fresh home is applied");
    assert!(crate::dev_model_address::set(&cfg));
    assert_eq!(cfg.session_flags.iter().filter(|flag| flag.starts_with("openai_base_url=")).collect::<Vec<_>>(), [&setting]);

    let host = Arc::new(Host::new());
    let ready = ready(&host, &cfg);
    let identity = &ready["versionIdentity"]["configurationIdentity"];
    assert!(identity["sessionFlags"].as_array().unwrap().contains(&json!(setting)), "the start's recorded settings name it: {identity}");
    let arguments: Vec<&str> = identity["arguments"].as_array().unwrap().iter().filter_map(Value::as_str).collect();
    assert!(arguments.windows(2).any(|pair| pair == ["-c", setting.as_str()]), "the supplier was given it as a session setting: {arguments:?}");

    // What the supplier itself reports of its configuration, read after the start.
    let reply = reading(&host, &cwd);
    let result = reply.get("result").unwrap_or_else(|| panic!("the reading was refused by the supplier: {reply}"));
    let carrying: Vec<Value> = layers(result).into_iter().filter(|layer| !layer["config"]["openai_base_url"].is_null()).collect();
    assert_eq!(carrying.len(), 1, "exactly one layer carries the address: {carrying:?}");
    assert_eq!(carrying[0]["name"]["type"], "sessionFlags");
    assert!(carrying[0]["disabledReason"].is_null());
    assert_eq!(carrying[0]["config"]["openai_base_url"], ADDRESS);
    assert_eq!(result["config"]["openai_base_url"], ADDRESS, "the effective configuration carries the address");

    assert!(matches!(std::fs::symlink_metadata(home.join("auth.json")), Err(error) if error.kind() == std::io::ErrorKind::NotFound), "the home holds no sign-in file");
    host.stop("the test", "test end").unwrap();
    assert_eq!(host.state(), "stopped");
}

/// The pinned supplier reads a `.codex/config.toml` in a folder above its working folder only
/// where a `.git` marker is found at that folder or above it.
///
/// The signal, and why it shows a read and not only an application: the supplier reports every
/// `.codex` folder its search visits as a layer in the reading's reply, enabled or disabled; and
/// a `config.toml` that exists but cannot be read as a file fails the whole reading, whatever
/// the project's trust. So with the parent's `config.toml` made a folder:
///
/// (a) no marker anywhere above the working folder: the reading succeeds and reports no project
///     layer. The parent's `.codex` was not visited and its `config.toml` not attempted.
/// (b) a `.git` marker at the parent, nothing else changed: the same reading fails, naming that
///     file. This is the positive control: an attempted read is visible by this signal.
/// (c) the folder replaced by a readable file carrying a recognisable harmless setting: the
///     reading succeeds, reports a project layer for that folder, disabled (a fresh home trusts
///     nothing), carrying the setting; the effective configuration does not carry it.
///
/// Establishes that for `config.toml` in an ancestor's `.codex`, in a fresh home, by the
/// configuration reading, for the folder the supplier was started in. It says nothing of agent
/// instruction files, skills, git or any other route by which the supplier finds files, and
/// nothing of a home that trusts the project.
#[test]
fn the_pinned_codex_reads_an_ancestors_codex_folder_only_up_to_a_git_marker() {
    let Some(bin) = supplier() else { return };
    let scratch = Scratch::new("pinned-search-");
    let (home, probe) = (scratch.dir("home"), scratch.dir("probe"));
    let parent = scratch.dir("parent");
    let work = scratch.dir("parent/between/work");
    std::fs::write(home.join("config.toml"), STAND_IN_HOME).unwrap();
    let dot_codex = parent.join(".codex");
    let file = dot_codex.join("config.toml");
    std::fs::create_dir_all(&file).unwrap(); // a folder where the file would be

    // What is above the working folder, by presence only. Case (a) is only what it claims where
    // no folder above holds a `.git` entry, and the invented parent's is the only `.codex`.
    let (mut git_above, mut codex_above) = (Vec::new(), Vec::new());
    for folder in work.ancestors() {
        if std::fs::symlink_metadata(folder.join(".git")).is_ok() { git_above.push(folder.to_path_buf()); }
        if std::fs::symlink_metadata(folder.join(".codex")).is_ok() { codex_above.push(folder.to_path_buf()); }
    }
    assert!(git_above.is_empty(), "a folder above the working folder holds a .git entry, so case (a) cannot be made here: {git_above:?}");
    assert_eq!(codex_above, [parent.clone()], "only the invented parent holds a .codex entry above the working folder");

    let host = Arc::new(Host::new());
    ready(&host, &config(&bin, &home, &probe, &work));

    // (a) No marker: not visited, not attempted.
    let reply = reading(&host, &work);
    let result = reply.get("result").unwrap_or_else(|| panic!("(a) with no marker the reading failed, so something attempted the parent's file: {reply}"));
    let project: Vec<Value> = layers(result).into_iter().filter(|layer| layer["name"]["type"] == "project").collect();
    assert!(project.is_empty(), "(a) with no marker the supplier reports a project layer: {project:?}");

    // (b) A marker at the parent: the attempt is visible.
    std::fs::create_dir(parent.join(".git")).unwrap();
    std::fs::write(parent.join(".git/HEAD"), "ref: refs/heads/main\n").unwrap();
    let reply = reading(&host, &work);
    assert!(reply.get("result").is_none(), "(b) with a marker at the parent the reading succeeded although the parent's config.toml cannot be read as a file: {reply}");
    let message = reply["error"]["message"].as_str().unwrap_or_default().to_owned();
    assert!(message.contains("config.toml"), "(b) the failure does not name the file: {reply}");

    // (c) A readable file: loaded, disabled, not applied.
    std::fs::remove_dir(&file).unwrap();
    std::fs::write(&file, "model_verbosity = \"high\"\n").unwrap();
    let reply = reading(&host, &work);
    let result = reply.get("result").unwrap_or_else(|| panic!("(c) the reading failed: {reply}"));
    let found = project_layers_for(result, &dot_codex);
    assert_eq!(found.len(), 1, "(c) one project layer for the parent's .codex: {:?}", layers(result));
    assert!(found[0]["disabledReason"].as_str().is_some_and(|reason| !reason.is_empty()), "(c) a fresh home trusts nothing, so the layer is disabled: {}", found[0]);
    assert_eq!(found[0]["config"]["model_verbosity"], "high", "(c) the disabled layer's contents are in the reply");
    assert!(result["config"]["model_verbosity"].is_null(), "(c) a disabled layer is not applied: {}", result["config"]);

    host.stop("the test", "test end").unwrap();
    assert_eq!(host.state(), "stopped");
}
