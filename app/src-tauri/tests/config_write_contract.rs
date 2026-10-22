//! Opt-in stock supplier observation with invented configuration; no App command or person act.
//! Native notifications may contain OS metadata. All raw exchanges/diagnostics stay private.
#![cfg(target_os = "macos")]
#![allow(dead_code)] // The real home-resource seam also supplies unrelated home classes.
use chirality_app_v4_lib::storage;
#[path = "../src/home_resources.rs"]
mod home_resources;
use home_resources::{HomeClass, OwnedHomePlan, ResourceState, SharedResourceTargets};
use serde_json::{json, Value};
use sha2::{Digest, Sha256};
use std::fs::{self, File, OpenOptions};
use std::io::{BufRead, BufReader, Read, Write};
use std::os::unix::{
    fs::{MetadataExt, OpenOptionsExt, PermissionsExt},
    process::CommandExt,
};
use std::path::{Path, PathBuf};
use std::process::{Child, ChildStdin, Command, Stdio};
use std::sync::mpsc::{self, Receiver};
use std::thread;
use std::time::{Duration, Instant};

type Result<T> = std::result::Result<T, String>;
const BINARY_SHA: &str = "112fae7a5a1223e673c8a1791d32338f37df8b527ff1159bb8adac6c4dbf1b4b";
const ARCHIVE_SHA: &str = "fc789bcd655d903f92e1a23c8dc5315ba38f43b3586eafb7bd3b195970b57466";
const BEFORE: &str = "http://fixture-before.invalid/v1";
const AFTER: &str = "http://fixture-after.invalid/v1";
const SCHEMA: &str =
    include_str!("../resources/supplier/0.160.0/codex_app_server_protocol.v2.schemas.json");

fn io<T>(r: std::io::Result<T>) -> Result<T> {
    r.map_err(|e| e.to_string())
}
fn require(ok: bool, message: &str) -> Result<()> {
    if ok {
        Ok(())
    } else {
        Err(message.into())
    }
}
fn private_file(path: &Path) -> Result<File> {
    io(OpenOptions::new()
        .write(true)
        .create_new(true)
        .mode(0o600)
        .open(path))
}
fn save(path: &Path, value: &Value) -> Result<()> {
    let mut f = private_file(path)?;
    io(f.write_all(&serde_json::to_vec_pretty(value).map_err(|e| e.to_string())?))
}
fn digest(path: &Path) -> Result<String> {
    let mut f = io(File::open(path))?;
    let mut hash = Sha256::new();
    let mut block = [0; 65536];
    loop {
        let n = io(f.read(&mut block))?;
        if n == 0 {
            break;
        }
        hash.update(&block[..n]);
    }
    Ok(format!("{:x}", hash.finalize()))
}
fn dir(path: &Path) -> Result<()> {
    io(fs::create_dir(path))?;
    io(fs::set_permissions(path, fs::Permissions::from_mode(0o700)))
}
fn fresh_root() -> Result<PathBuf> {
    let mut template = b"/private/tmp/chirality-linked-config-proof.XXXXXX\0".to_vec();
    let raw = unsafe { libc::mkdtemp(template.as_mut_ptr().cast()) };
    require(!raw.is_null(), "private proof root creation failed")?;
    let path = PathBuf::from(
        unsafe { std::ffi::CStr::from_ptr(raw) }
            .to_str()
            .map_err(|_| "root encoding")?,
    );
    require(
        io(fs::canonicalize(&path))? == path,
        "proof root must be physical",
    )?;
    Ok(path)
}
fn physical(path: &Path, directory: bool) -> Result<fs::Metadata> {
    require(
        path.is_absolute() && path.starts_with("/private/tmp"),
        "input must be explicitly beneath /private/tmp",
    )?;
    let m = io(fs::symlink_metadata(path))?;
    require(
        !m.file_type().is_symlink() && (if directory { m.is_dir() } else { m.is_file() }),
        "input type differs",
    )?;
    require(io(fs::canonicalize(path))? == path, "input alias refused")?;
    require(
        m.uid() == unsafe { libc::geteuid() },
        "input ownership differs",
    )?;
    Ok(m)
}
struct Input {
    root: PathBuf,
    binary: PathBuf,
    binding: Value,
}
impl Input {
    fn guarded() -> Result<Self> {
        // These guards precede supplier lookup, proof/home creation and any ambient config access.
        require(
            std::env::var("CHIRALITY_CONFIG_WRITE_CONTRACT").as_deref()
                == Ok("stock-0.160-invented-only"),
            "NOT RUN: set CHIRALITY_CONFIG_WRITE_CONTRACT=stock-0.160-invented-only explicitly",
        )?;
        let root = PathBuf::from(
            std::env::var_os("CHIRALITY_CONFIG_WRITE_INPUT")
                .ok_or("NOT RUN: explicit NEW owned stock input required")?,
        );
        let expected = std::env::var("CHIRALITY_CONFIG_WRITE_BINDING_SHA256")
            .map_err(|_| "NOT RUN: handed-off binding SHA256 required")?;
        require(
            expected.len() == 64 && expected.bytes().all(|c| c.is_ascii_hexdigit()),
            "binding hash invalid",
        )?;
        let root_meta = physical(&root, true)?;
        require(
            root_meta.mode() & 0o7777 == 0o700,
            "input root must be private0700",
        )?;
        let binding_path = root.join("input-binding.json");
        let binding_meta = physical(&binding_path, false)?;
        require(
            binding_meta.mode() & 0o7777 == 0o600 && binding_meta.len() <= 65536,
            "private bounded binding required",
        )?;
        require(
            digest(&binding_path)? == expected,
            "input binding SHA256 mismatch; return to input owner",
        )?;
        let binding: Value =
            serde_json::from_slice(&io(fs::read(&binding_path))?).map_err(|e| e.to_string())?;
        require(
            binding["root"]["path"] == root.to_str().ok_or("input path encoding")?,
            "binding root differs",
        )?;
        require(
            binding["root"]["inode"].as_u64() == Some(root_meta.ino())
                && binding["root"]["dev"].as_u64() == Some(root_meta.dev())
                && binding["root"]["uid"].as_u64() == Some(root_meta.uid() as u64)
                && binding["root"]["gid"].as_u64() == Some(root_meta.gid() as u64),
            "bound input directory replaced",
        )?;
        let binary = root.join("extracted/package/vendor/aarch64-apple-darwin/bin/codex");
        let archive = root.join("codex-0.160.0-darwin-arm64.tgz");
        for (path, key, size, sha) in [
            (&binary, "nativeBinary", 241555024, BINARY_SHA),
            (&archive, "archive", 134311083, ARCHIVE_SHA),
        ] {
            let meta = physical(path, false)?;
            require(
                meta.len() == size && binding[key]["size"] == size && binding[key]["sha256"] == sha,
                "bound stock size/hash declaration differs",
            )?;
            require(
                binding[key]["path"] == path.to_str().ok_or("stock path encoding")?
                    && binding[key]["inode"].as_u64() == Some(meta.ino())
                    && binding[key]["dev"].as_u64() == Some(meta.dev())
                    && binding[key]["uid"].as_u64() == Some(meta.uid() as u64)
                    && binding[key]["gid"].as_u64() == Some(meta.gid() as u64)
                    && binding[key]["mode"].as_u64() == Some((meta.mode() & 0o7777) as u64),
                "stock input identity differs",
            )?;
            require(
                digest(path)? == sha,
                "stock SHA256 mismatch; return to input owner",
            )?;
        }
        require(
            physical(&binary, false)?.mode() & 0o7777 == 0o755
                && physical(&archive, false)?.mode() & 0o7777 == 0o600,
            "stock binary/archive permissions differ",
        )?;
        // Full vendor/helper layout is retained under the input owner's bound warrant; no re-inventory.
        Ok(Self {
            root,
            binary,
            binding,
        })
    }
}

fn schema(name: &str, value: &Value) -> Result<()> {
    let mut s: Value = serde_json::from_str(SCHEMA).map_err(|e| e.to_string())?;
    s["$ref"] = json!(format!("#/definitions/{name}"));
    let validator = jsonschema::options()
        .with_draft(jsonschema::Draft::Draft7)
        .offline()
        .build(&s)
        .map_err(|e| e.to_string())?;
    require(
        validator.is_valid(value),
        &format!("pinned {name} schema refused; inspect private exchange"),
    )
}

struct Case {
    root: PathBuf,
    cwd: PathBuf,
    plan: OwnedHomePlan,
    target: PathBuf,
}
impl Case {
    fn new(proof: &Path, name: &str) -> Result<Self> {
        let root = proof.join(name);
        dir(&root)?;
        for name in [
            "shared",
            "app-data",
            "os-home",
            "tmp",
            "work",
            "xdg-config",
            "xdg-data",
            "xdg-cache",
            "xdg-state",
        ] {
            dir(&root.join(name))?;
        }
        dir(&root.join("shared/skills"))?;
        let config = format!("# Invented-only linked configuration contract fixture.\ncli_auth_credentials_store = \"file\"\nmodel_provider = \"fixture_normal\"\nmodel = \"fixture-no-model\"\n[features]\nplugins = false\n[analytics]\nenabled = false\n[model_providers.fixture_normal]\nname = \"Invented anonymous normal\"\nbase_url = \"{BEFORE}\" # endpoint comment\nwire_api = \"responses\"\nrequires_openai_auth = false\n[model_providers.\"fixture.dot\"]\nname = \"Invented dotted identity\"\nbase_url = \"http://fixture-dotted.invalid/v1\"\nwire_api = \"responses\"\nrequires_openai_auth = false\n[model_providers.fixture]\nname = \"Invented sibling\"\nbase_url = \"http://fixture-sibling.invalid/v1\"\nwire_api = \"responses\"\nrequires_openai_auth = false\n");
        io(private_file(&root.join("shared/config.toml"))?.write_all(config.as_bytes()))?;
        private_file(&root.join("shared/AGENTS.md"))?;
        let plan = OwnedHomePlan::new(
            root.join("app-data"),
            root.join("app-data/account"),
            HomeClass::Account,
            Some(SharedResourceTargets {
                config_toml: root.join("shared/config.toml"),
                global_agents_md: root.join("shared/AGENTS.md"),
                skills: root.join("shared/skills"),
            }),
        )?;
        let prepared = plan.prepare()?;
        require(
            prepared
                .resources
                .iter()
                .all(|r| r.state == ResourceState::Linked),
            "real plan did not prepare three links",
        )?;
        // A second prepare exercises the actual create-only path, never repairs a conflict.
        let before = snapshot(
            &root.join("app-data/account/config.toml"),
            &root.join("shared/config.toml"),
        )?;
        plan.prepare()?;
        require(
            before
                == snapshot(
                    &root.join("app-data/account/config.toml"),
                    &root.join("shared/config.toml"),
                )?,
            "prepare changed existing objects",
        )?;
        let target = plan.resolved_config_write_target()?;
        require(
            target == root.join("shared/config.toml") && target.starts_with(&root),
            "resolved target escaped case",
        )?;
        Ok(Self {
            cwd: root.join("work"),
            root,
            plan,
            target,
        })
    }
    fn state(&self) -> Result<Value> {
        snapshot(&self.plan.native_path().join("config.toml"), &self.target)
    }
}
fn snapshot(link: &Path, target: &Path) -> Result<Value> {
    let l = io(fs::symlink_metadata(link))?;
    let t = io(fs::symlink_metadata(target))?;
    require(
        l.file_type().is_symlink() && t.is_file() && !t.file_type().is_symlink(),
        "link/target type changed",
    )?;
    let bytes = io(fs::read(target))?;
    let parsed: toml::Value =
        toml::from_str(std::str::from_utf8(&bytes).map_err(|_| "fixture TOML encoding")?)
            .map_err(|e| e.to_string())?;
    Ok(
        json!({"link":{"dev":l.dev(),"inode":l.ino(),"mode":l.mode(),"rawTarget":io(fs::read_link(link))?},
        "target":{"dev":t.dev(),"inode":t.ino(),"mode":t.mode(),"uid":t.uid(),"gid":t.gid(),"nlink":t.nlink(),"bytes":String::from_utf8(bytes).map_err(|_| "fixture bytes encoding")?,"semantics":parsed}}),
    )
}

enum Incoming {
    Frame(Value),
    End,
    Invalid,
}
struct Native {
    child: Child,
    stdin: Option<ChildStdin>,
    incoming: Receiver<Incoming>,
    reader: Option<thread::JoinHandle<()>>,
    log: File,
    counter: u64,
    closed: bool,
    root: PathBuf,
}
impl Native {
    fn open(input: &Input, case: &Case, overrides: &[String]) -> Result<Self> {
        require(
            io(fs::metadata("/usr/bin/sandbox-exec"))?.mode() & 0o111 != 0,
            "network-deny isolation unavailable",
        )?;
        let profile = case.root.join("network.sb");
        let quoted = serde_json::to_string(&case.root).map_err(|e| e.to_string())?;
        // Tighten the maintained fixture_sandbox pattern: no localhost exceptions,
        // no descendants, and writes confined to this fresh case. No unsandboxed fallback.
        let policy = format!("(version 1)\n(allow default)\n(deny network*)\n(deny file-read* (subpath \"/Users\"))\n(deny file-read* (subpath \"/private/etc/codex\") (subpath \"/etc/codex\"))\n(deny process-fork)\n(deny file-write*)\n(allow file-write* (subpath {quoted}) (literal \"/dev/null\"))\n");
        io(private_file(&profile)?.write_all(policy.as_bytes()))?;
        let mut cmd = Command::new("/usr/bin/sandbox-exec");
        cmd.arg("-f")
            .arg(&profile)
            .arg(&input.binary)
            .args(["-c", "cli_auth_credentials_store=\"file\""]);
        for value in overrides {
            cmd.arg("-c").arg(value);
        }
        cmd.arg("app-server")
            .env_clear()
            .env("PATH", "/usr/bin:/bin:/usr/sbin:/sbin")
            .env("LC_ALL", "C")
            .env("HOME", case.root.join("os-home"))
            .env("CODEX_HOME", case.plan.native_path())
            .env("TMPDIR", case.root.join("tmp"))
            .env("XDG_CONFIG_HOME", case.root.join("xdg-config"))
            .env("XDG_DATA_HOME", case.root.join("xdg-data"))
            .env("XDG_CACHE_HOME", case.root.join("xdg-cache"))
            .env("XDG_STATE_HOME", case.root.join("xdg-state"))
            .current_dir(&case.cwd)
            .stdin(Stdio::piped())
            .stdout(Stdio::piped())
            .stderr(Stdio::from(private_file(&case.root.join("stderr.log"))?));
        // Finish fallible file creation before spawning. Establish the cleanup owner
        // immediately on spawn, before extracting pipes, starting a reader or recording PID.
        let log = private_file(&case.root.join("exchanges.jsonl"))?;
        let mut process_log = private_file(&case.root.join("process.json"))?;
        let child = io(cmd.process_group(0).spawn())?;
        let (tx, incoming) = mpsc::channel();
        let mut native = Self {
            child,
            stdin: None,
            incoming,
            reader: None,
            log,
            counter: 0,
            closed: false,
            root: case.root.clone(),
        };
        native.stdin = native.child.stdin.take();
        let stdout = native.child.stdout.take().ok_or("owned stdout absent")?;
        native.reader = Some(io(thread::Builder::new()
            .name("config-contract-stdout".into())
            .spawn(move || {
                let mut stream = BufReader::new(stdout);
                loop {
                    let mut bytes = Vec::new();
                    match stream
                        .by_ref()
                        .take(4 * 1024 * 1024 + 1)
                        .read_until(b'\n', &mut bytes)
                    {
                        Ok(0) => break,
                        Ok(n) if n <= 4 * 1024 * 1024 => {
                            let message = serde_json::from_slice(&bytes)
                                .map(Incoming::Frame)
                                .unwrap_or(Incoming::Invalid);
                            if tx.send(message).is_err() {
                                return;
                            }
                        }
                        _ => {
                            let _ = tx.send(Incoming::Invalid);
                            break;
                        }
                    }
                }
                let _ = tx.send(Incoming::End);
            }))?);
        io(writeln!(
            process_log,
            "{}",
            json!({"pid":native.child.id(),"pgid":native.child.id(),"binary":input.binary,"network":"deny all","fork":"denied","environment":"cleared; fixed system PATH, LC_ALL=C and fresh HOME/CODEX_HOME/TMPDIR/XDG roots","inputRoot":input.root})
        ))?;
        Ok(native)
    }
    fn record(&mut self, direction: &str, frame: &Value) -> Result<()> {
        io(writeln!(
            self.log,
            "{}",
            json!({"direction":direction,"frame":frame})
        ))?;
        io(self.log.flush())
    }
    fn send(&mut self, method: &str, params: Value) -> Result<Value> {
        require(
            matches!(
                method,
                "initialize" | "initialized" | "config/read" | "config/batchWrite"
            ),
            "RPC outside fixture allowlist",
        )?;
        self.counter += 1;
        let id = self.counter;
        let mut frame = json!({"id":id,"method":method,"params":params});
        if method == "initialized" {
            frame.as_object_mut().unwrap().remove("id");
        }
        self.record("sent", &frame)?;
        let input = self.stdin.as_mut().ok_or("owned stdin closed")?;
        io(writeln!(input, "{frame}"))?;
        io(input.flush())?;
        if method == "initialized" {
            return Ok(Value::Null);
        }
        let deadline = Instant::now() + Duration::from_secs(10);
        loop {
            require(
                Instant::now() < deadline,
                "native response timeout/outcome unknown; no replay",
            )?;
            match self
                .incoming
                .recv_timeout(deadline.saturating_duration_since(Instant::now()))
            {
                Ok(Incoming::Frame(reply)) => {
                    self.record("received", &reply)?;
                    // No server request is answered. Numeric ID equality is insufficient without frame kind.
                    require(
                        reply.get("method").is_none() || reply.get("id").is_none(),
                        "unexpected supplier request: stop without answering",
                    )?;
                    if reply.get("id").is_some() {
                        require(
                            reply["id"] == id
                                && (reply.get("result").is_some() ^ reply.get("error").is_some()),
                            "unmatched/malformed native response",
                        )?;
                        return Ok(reply);
                    }
                }
                Ok(Incoming::End) => {
                    return Err(
                        "native EOF; isolation/protocol condition unestablished; no replay".into(),
                    )
                }
                Ok(Incoming::Invalid) => {
                    return Err("malformed/oversize native output; no replay".into())
                }
                Err(_) => return Err("native response timeout/outcome unknown; no replay".into()),
            }
        }
    }
    fn initialize(&mut self) -> Result<()> {
        let r = self.send("initialize", json!({"clientInfo":{"name":"linked_config_invented_contract","version":"0.0.0"},"capabilities":{"experimentalApi":true}}))?;
        require(
            r.get("result").is_some(),
            "native initialize refused; isolation/protocol obstacle",
        )?;
        self.send("initialized", json!({}))?;
        Ok(())
    }
    fn read(&mut self, case: &Case) -> Result<Value> {
        let params = json!({"includeLayers":true,"cwd":case.cwd});
        schema("ConfigReadParams", &params)?;
        let frame = self.send("config/read", params)?;
        let result = frame
            .get("result")
            .ok_or("native config read refused")?
            .clone();
        schema("ConfigReadResponse", &result)?;
        Ok(result)
    }
    fn close(&mut self) -> Result<()> {
        if self.closed {
            return Ok(());
        }
        self.stdin.take(); // Supported EOF first. Keep leader unreaped through the last group operation.
        let pid = self.child.id() as i32;
        let mut signals = Vec::new();
        let mut last = json!({});
        for (signal, budget) in [(0, 500), (libc::SIGTERM, 500), (libc::SIGKILL, 3000)] {
            if signal != 0 {
                original_exit(pid)?;
                let rc = unsafe { libc::killpg(pid, signal) };
                require(
                    rc == 0 || std::io::Error::last_os_error().raw_os_error() == Some(libc::ESRCH),
                    "owned group signal failed",
                )?;
                signals.push(signal);
            }
            let deadline = Instant::now() + Duration::from_millis(budget);
            loop {
                let exit = original_exit(pid)?;
                let (live, members) = group_members(pid, exit)?;
                last = json!({"leaderExited":exit,"live":live,"members":members});
                if exit && live == 0 {
                    let status = io(self.child.wait())?; // no numeric group operation after this reap
                    self.closed = true;
                    if let Some(reader) = self.reader.take() {
                        let deadline = Instant::now() + Duration::from_secs(1);
                        while !reader.is_finished() && Instant::now() < deadline {
                            thread::sleep(Duration::from_millis(10));
                        }
                        require(reader.is_finished(), "owned stdout reader did not finish")?;
                        reader.join().map_err(|_| "owned reader panicked")?;
                    }
                    save(
                        &self.root.join("cleanup.json"),
                        &json!({"eof":true,"signals":signals,"lastGroup":last,"status":status.to_string(),"reaped":true,"detachedDescendants":"process-fork denied by case sandbox"}),
                    )?;
                    return Ok(());
                }
                if Instant::now() >= deadline {
                    break;
                }
                thread::sleep(Duration::from_millis(25));
            }
        }
        save(
            &self.root.join("cleanup-unknown.json"),
            &json!({"eof":true,"signals":signals,"lastGroup":last,"reaped":false}),
        )?;
        Err("owned process cleanup not established; retain original unreaped identity".into())
    }
}
impl Drop for Native {
    fn drop(&mut self) {
        if !self.closed {
            let _ = self.close();
        }
    }
}
fn original_exit(pid: i32) -> Result<bool> {
    let mut info = unsafe { std::mem::zeroed::<libc::siginfo_t>() };
    let rc = unsafe {
        libc::waitid(
            libc::P_PID,
            pid as libc::id_t,
            &mut info,
            libc::WEXITED | libc::WNOHANG | libc::WNOWAIT,
        )
    };
    require(
        rc == 0,
        "original child reservation unavailable; no numeric fallback",
    )?;
    Ok(info.si_pid == pid)
}
fn group_members(pgid: i32, exited: bool) -> Result<(usize, Value)> {
    // Same exact-group selector as process_group_custody.rs, never PROC_ALL_PIDS.
    let mut pids = [0i32; 1024];
    unsafe {
        *libc::__error() = 0;
    }
    let n = unsafe {
        libc::proc_listpids(
            2,
            pgid as u32,
            pids.as_mut_ptr().cast(),
            std::mem::size_of_val(&pids) as i32,
        )
    };
    require(
        n >= 0
            && (n != 0 || std::io::Error::last_os_error().raw_os_error() == Some(0))
            && (n as usize) < std::mem::size_of_val(&pids)
            && n % 4 == 0,
        "owned-group census unavailable/incomplete",
    )?;
    let mut rows = Vec::new();
    let mut live = 0;
    for &pid in &pids[..n as usize / 4] {
        require(pid > 0, "invalid owned-group member")?;
        if pid == pgid && exited {
            rows.push(json!({"pid":pid,"status":"original reserved exited leader"}));
            continue;
        }
        let mut b = unsafe { std::mem::zeroed::<libc::proc_bsdinfo>() };
        let required = std::mem::size_of_val(&b);
        let count = unsafe {
            libc::proc_pidinfo(
                pid,
                libc::PROC_PIDTBSDINFO,
                0,
                (&mut b as *mut libc::proc_bsdinfo).cast(),
                required as i32,
            )
        };
        require(
            count as usize == required && b.pbi_pid == pid as u32 && b.pbi_pgid == pgid as u32,
            "owned-group member association unavailable",
        )?;
        if b.pbi_status != libc::SZOMB {
            live += 1;
        }
        rows.push(json!({"pid":pid,"pgid":b.pbi_pgid,"status":b.pbi_status}));
    }
    Ok((live, json!(rows)))
}

fn layer_version(read: &Value, case: &Case) -> Result<String> {
    let layers = read["layers"]
        .as_array()
        .ok_or("actual config layers absent")?;
    let mut found = Vec::new();
    for layer in layers {
        if layer["name"]["type"] != "user" || !layer["name"]["profile"].is_null() {
            continue;
        }
        let path = PathBuf::from(
            layer["name"]["file"]
                .as_str()
                .ok_or("native user layer file missing")?,
        );
        require(
            path.starts_with(&case.root),
            "native user layer outside invented root",
        )?;
        require(
            io(fs::canonicalize(&path))? == case.target,
            "actual user layer does not identify resolved target",
        )?;
        let a = io(fs::metadata(&path))?;
        let b = io(fs::metadata(&case.target))?;
        require(
            (a.dev(), a.ino()) == (b.dev(), b.ino()),
            "layer and target object relationship differs",
        )?;
        require(
            layer["disabledReason"].is_null(),
            "actual user layer disabled",
        )?;
        found.push(
            layer["version"]
                .as_str()
                .ok_or("native layer version missing")?
                .to_owned(),
        );
    }
    require(
        found.len() == 1 && !found[0].is_empty(),
        "unique native target version unestablished",
    )?;
    Ok(found.remove(0))
}
fn write_params(case: &Case, version: &str, key: &str, value: Value) -> Result<Value> {
    require(
        case.plan.resolved_config_write_target()? == case.target
            && case.target.starts_with(&case.root),
        "target relationship changed before write",
    )?;
    let params = json!({"filePath":case.target,"expectedVersion":version,"reloadUserConfig":false,"edits":[{"keyPath":key,"value":value,"mergeStrategy":"replace"}]});
    schema("ConfigBatchWriteParams", &params)?;
    Ok(params)
}
fn accepted_write(reply: &Value, case: &Case) -> Result<Value> {
    let r = reply
        .get("result")
        .ok_or("native explicit-target write refused; inspect effects; do not fallback")?
        .clone();
    schema("ConfigWriteResponse", &r)?;
    require(
        r["filePath"] == case.target.to_str().ok_or("target encoding")?
            && io(fs::canonicalize(&case.target))? == case.target,
        "native returned noncanonical/different target",
    )?;
    require(
        r["version"].as_str().is_some_and(|v| !v.is_empty()),
        "native new version absent",
    )?;
    Ok(r)
}
fn endpoint_case(input: &Input, proof: &Path) -> Result<()> {
    let case = Case::new(proof, "endpoint")?;
    let mut native = Native::open(input, &case, &[])?;
    let outcome = (|| {
        native.initialize()?;
        let read = native.read(&case)?;
        let v1 = layer_version(&read, &case)?;
        let before = case.state()?;
        save(&case.root.join("before.json"), &before)?;
        let params = write_params(
            &case,
            &v1,
            "model_providers.fixture_normal.base_url",
            json!(AFTER),
        )?;
        let reply = native.send("config/batchWrite", params);
        // Always inspect owned effects before interpreting an error/lost acknowledgement. Never replay.
        let after = case.state()?;
        save(&case.root.join("after.json"), &after)?;
        let reply = reply?;
        let result = accepted_write(&reply, &case)?;
        let reread = native.read(&case)?;
        require(
            before["link"] == after["link"],
            "receiving link identity/type/raw target changed",
        )?;
        let mut expected = before["target"]["semantics"].clone();
        expected["model_providers"]["fixture_normal"]["base_url"] = json!(AFTER);
        require(
            after["target"]["semantics"] == expected,
            "endpoint write changed sibling provider/other settings",
        )?;
        require(
            reread["config"]["model_providers"]["fixture_normal"]["base_url"] == AFTER,
            "write acknowledgement did not establish effective reread",
        )?;
        let v2 = layer_version(&reread, &case)?;
        require(
            v2 == result["version"] && v2 != v1,
            "reread/write version relationship differs",
        )?;
        require(
            result["status"] == "ok" && result["overriddenMetadata"].is_null(),
            "unexpected endpoint override",
        )?;
        save(
            &case.root.join("effects.json"),
            &json!({"status":"observed","receivingLinkUnchanged":true,"targetInodeReplaced":before["target"]["inode"] != after["target"]["inode"],"targetModeBefore":before["target"]["mode"],"targetModeAfter":after["target"]["mode"],"bytesChanged":before["target"]["bytes"] != after["target"]["bytes"],"semantics":"only endpoint changed; siblings/settings preserved","nativeVersionBefore":v1,"nativeVersionAfter":v2,"writeResponse":result}),
        )?;
        Ok(())
    })();
    if let Err(e) = &outcome {
        save(
            &case.root.join("obstacle.json"),
            &json!({"condition":e,"writeReplay":false}),
        )?;
    }
    let cleanup = native.close();
    outcome.and(cleanup)
}

fn observed_case(
    input: &Input,
    proof: &Path,
    name: &str,
    overrides: &[String],
    observe: impl FnOnce(&Case, &mut Native) -> Result<Value>,
) -> Result<()> {
    let case = Case::new(proof, name)?;
    save(&case.root.join("before.json"), &case.state()?)?;
    let mut native = Native::open(input, &case, overrides)?;
    let outcome = native
        .initialize()
        .and_then(|()| observe(&case, &mut native));
    // Preserve owned effects even when a reply is lost/refused or a case assertion fails.
    let effects = match case.state() {
        Ok(v) => v,
        Err(e) => json!({"observationUnavailable":e,"writeReplay":false}),
    };
    let saved = save(&case.root.join("after.json"), &effects);
    let recorded = match &outcome {
        Ok(value) => save(&case.root.join("effects.json"), value),
        Err(e) => save(
            &case.root.join("obstacle.json"),
            &json!({"condition":e,"writeReplay":false}),
        ),
    };
    let cleanup = native.close();
    outcome.map(|_| ()).and(saved).and(recorded).and(cleanup)
}
fn unchanged(before: &Value, after: &Value) -> Result<()> {
    require(
        before == after,
        "refused write changed link/target bytes, semantics, permissions or identity",
    )
}
fn endpoint_semantics(before: &Value, after: &Value, id: &str, value: &str) -> Result<()> {
    require(before["link"] == after["link"], "receiving symlink changed")?;
    let mut expected = before["target"]["semantics"].clone();
    expected["model_providers"][id]["base_url"] = json!(value);
    require(
        after["target"]["semantics"] == expected,
        "key path changed another setting/provider identity",
    )
}
fn error_frame(reply: &Value) -> Result<&Value> {
    require(
        reply.get("result").is_none(),
        "native unexpectedly accepted the negative control; inspect effects",
    )?;
    let error = reply.get("error").ok_or("native error frame absent")?;
    require(
        error["code"].as_i64().is_some() && error["message"].as_str().is_some(),
        "native error shape unestablished",
    )?;
    Ok(error)
}
fn stale_case(input: &Input, proof: &Path) -> Result<()> {
    observed_case(input, proof, "stale-version", &[], |case, native| {
        let first = native.read(case)?;
        let v1 = layer_version(&first, case)?;
        let before = case.state()?;
        let bytes = before["target"]["bytes"]
            .as_str()
            .ok_or("fixture bytes absent")?;
        let edited = bytes.replacen(
            "model = \"fixture-no-model\"",
            "model = \"fixture-external-edit\"",
            1,
        );
        require(
            edited != bytes,
            "controlled external edit did not change fixture",
        )?;
        // Controlled fixture actor, not a native write or a fabricated native version.
        io(fs::write(&case.target, edited.as_bytes()))?;
        let external = case.state()?;
        save(&case.root.join("external-edit.json"), &external)?;
        require(
            before["target"]["inode"] == external["target"]["inode"],
            "controlled edit unexpectedly replaced target",
        )?;
        let reply = native.send(
            "config/batchWrite",
            write_params(
                case,
                &v1,
                "model_providers.fixture_normal.base_url",
                json!(AFTER),
            )?,
        );
        let after = case.state()?;
        save(&case.root.join("after-write.json"), &after)?;
        let reply = reply?;
        let error = error_frame(&reply)?;
        unchanged(&external, &after)?;
        let reread = native.read(case)?;
        let v2 = layer_version(&reread, case)?;
        require(
            v2 != v1
                && reread["config"]["model"] == "fixture-external-edit"
                && reread["config"]["model_providers"]["fixture_normal"]["base_url"] == BEFORE,
            "stale negative control reread differs",
        )?;
        Ok(
            json!({"status":"actual-native-error-after-real-stale-version","nativeError":error,"readVersionV1":v1,"rereadVersionAfterExternalEdit":v2,"fixtureExternalEdit":"root model only, in place","writeAttempts":1,"retry":false,"effectsUnchangedFromExternalEdit":true}),
        )
    })
}
fn override_case(input: &Input, proof: &Path) -> Result<()> {
    const OVERRIDE: &str = "http://fixture-override.invalid/v1";
    observed_case(
        input,
        proof,
        "higher-layer",
        &[format!(
            "model_providers.fixture_normal.base_url=\"{OVERRIDE}\""
        )],
        |case, native| {
            let read = native.read(case)?;
            let version = layer_version(&read, case)?;
            require(
                read["config"]["model_providers"]["fixture_normal"]["base_url"] == OVERRIDE,
                "actual higher-layer input not effective",
            )?;
            let layers = read["layers"].as_array().ok_or("actual layers absent")?;
            require(
                layers.iter().any(|l| {
                    l["name"]["type"] == "sessionFlags"
                        && l["config"]["model_providers"]["fixture_normal"]["base_url"] == OVERRIDE
                }),
                "actual controlled CLI layer absent",
            )?;
            let before = case.state()?;
            let reply = native.send(
                "config/batchWrite",
                write_params(
                    case,
                    &version,
                    "model_providers.fixture_normal.base_url",
                    json!(AFTER),
                )?,
            );
            let after = case.state()?;
            save(&case.root.join("after-write.json"), &after)?;
            let reply = reply?;
            if reply.get("error").is_some() {
                let error = error_frame(&reply)?;
                unchanged(&before, &after)?;
                return Ok(
                    json!({"status":"actual-refusal","nativeError":error,"writeAttempts":1,"effectiveBefore":OVERRIDE,"retry":false}),
                );
            }
            let result = accepted_write(&reply, case)?;
            endpoint_semantics(&before, &after, "fixture_normal", AFTER)?;
            let reread = native.read(case)?;
            require(
                reread["config"]["model_providers"]["fixture_normal"]["base_url"] == OVERRIDE,
                "higher layer not effective after acknowledged user write",
            )?;
            require(
                layer_version(&reread, case)? == result["version"],
                "override write and user-layer version differ",
            )?;
            if result["status"] == "okOverridden" {
                require(
                    result["overriddenMetadata"]["overridingLayer"]["name"]["type"]
                        == "sessionFlags"
                        && result["overriddenMetadata"]["effectiveValue"] == OVERRIDE,
                    "actual override metadata does not identify controlled effective layer/value",
                )?;
            }
            Ok(
                json!({"status":"observed-write-and-effective-override","writeResponse":result,"effectiveReread":OVERRIDE,"writtenUserValue":AFTER,"targetInodeReplaced":before["target"]["inode"] != after["target"]["inode"],"loadedThreads":"none created","reloadUserConfig":false,"writeAttempts":1}),
            )
        },
    )
}
fn diagnostic_case(input: &Input, proof: &Path) -> Result<()> {
    const VALUE: &str = "INVENTED_VALUE_ONLY_A7";
    observed_case(
        input,
        proof,
        "diagnostic-INVENTED_PATH_ONLY_A7",
        &[],
        |case, native| {
            let read = native.read(case)?;
            let version = layer_version(&read, case)?;
            let before = case.state()?;
            // Deliberately wrong endpoint type, carrying invented NONSECRET material only.
            let reply = native.send(
                "config/batchWrite",
                write_params(
                    case,
                    &version,
                    "model_providers.fixture_normal.base_url",
                    json!({"inventedDiagnosticMarker":VALUE}),
                )?,
            );
            let after = case.state()?;
            save(&case.root.join("after-write.json"), &after)?;
            let reply = reply?;
            let error = error_frame(&reply)?;
            unchanged(&before, &after)?;
            let text = serde_json::to_string(error).map_err(|e| e.to_string())?;
            Ok(
                json!({"status":"actual-invalid-value-refusal","nativeError":error,"errorReflectsTargetPath":text.contains(case.target.to_str().ok_or("target encoding")?),"errorReflectsPathMarker":text.contains("INVENTED_PATH_ONLY_A7"),"errorReflectsValueMarker":text.contains(VALUE),"errorReflectsKeyPath":text.contains("model_providers.fixture_normal.base_url"),"publicSummary":"Configuration write was refused; native diagnostic withheld.","limit":"invented-only reflection observation; no App error-handling/privacy implementation or secret guarantee","writeAttempts":1,"effectsUnchanged":true}),
            )
        },
    )
}
fn quoted_identity_case(input: &Input, proof: &Path) -> Result<()> {
    observed_case(input, proof, "quoted-provider-id", &[], |case, native| {
        let read = native.read(case)?;
        let version = layer_version(&read, case)?;
        require(
            read["config"]["model_providers"]
                .get("fixture.dot")
                .is_some(),
            "actual dotted provider identity absent",
        )?;
        let before = case.state()?;
        // Submit the quoted segment literally. Never split/reinterpret the provider ID,
        // retry alternative escapes, or replace a whole provider definition after refusal.
        let key = "model_providers.\"fixture.dot\".base_url";
        let reply = native.send(
            "config/batchWrite",
            write_params(case, &version, key, json!(AFTER))?,
        );
        let after = case.state()?;
        save(&case.root.join("after-write.json"), &after)?;
        let reply = reply?;
        if reply.get("error").is_some() {
            let error = error_frame(&reply)?;
            unchanged(&before, &after)?;
            return Ok(
                json!({"status":"quoted-segment-refused; escaping unsupported/unestablished","nativeError":error,"keyPath":key,"writeAttempts":1,"fallback":false}),
            );
        }
        let result = accepted_write(&reply, case)?;
        endpoint_semantics(&before, &after, "fixture.dot", AFTER)?;
        let reread = native.read(case)?;
        require(
            reread["config"]["model_providers"]["fixture.dot"]["base_url"] == AFTER,
            "native reread did not preserve dotted provider identity",
        )?;
        require(
            layer_version(&reread, case)? == result["version"],
            "quoted provider write/reread versions differ",
        )?;
        Ok(
            json!({"status":"quoted-segment-observed","keyPath":key,"writeResponse":result,"exactProviderId":"fixture.dot","siblingsAndOtherSettingsPreserved":true,"writeAttempts":1,"targetInodeReplaced":before["target"]["inode"] != after["target"]["inode"]}),
        )
    })
}

#[test]
#[ignore = "actual supplier: explicit invented-only flag and bound NEW input required; never ordinary CI"]
fn stock_linked_config_write_contract() {
    let input = Input::guarded().unwrap_or_else(|e| panic!("{e}"));
    let selection = std::env::var("CHIRALITY_CONFIG_WRITE_CASES").unwrap_or_else(|_| "all".into());
    assert!(
        matches!(selection.as_str(), "all" | "endpoint" | "remaining"),
        "NOT RUN: cases must be all, endpoint or remaining"
    );
    let proof = fresh_root().expect("private proof root");
    eprintln!(
        "private invented-only contract root: {}; cases={selection}",
        proof.display()
    );
    save(&proof.join("input.json"),&json!({"root":input.root,"binary":input.binary,"binarySha256":BINARY_SHA,"archiveSha256":ARCHIVE_SHA,"bindingRoot":input.binding["root"],"vendorWarrant":input.binding["vendorTree"],"limit":"input-owner fullvendor warrant reused; no version probe, App, account, model, server or person act"})).unwrap();
    let result: Result<()> = (|| {
        if selection != "remaining" {
            endpoint_case(&input, &proof)?;
        }
        if selection != "endpoint" {
            stale_case(&input, &proof)?;
            override_case(&input, &proof)?;
            diagnostic_case(&input, &proof)?;
            quoted_identity_case(&input, &proof)?;
        }
        Ok(())
    })();
    if let Err(e) = result {
        save(&proof.join("obstacle.json"),&json!({"condition":e,"result":"unestablished; inspect private effects, never replay a lost write"})).unwrap();
        panic!("supplier contract unestablished; inspect private proof root (diagnostic withheld)");
    }
    eprintln!("selected contract observations retained privately; unselected cases were NOT RUN; no App/person/qualification claim");
}

// Separate creation observations. The original five-case entry and helpers above
// retain their existing behavior; no whole-definition warrant is inferred from them.
const CREATION_ID: &str = "fixture.new";
const CREATION_KEY: &str = "model_providers.\"fixture.new\"";
fn creation_definition() -> Value {
    json!({"name":"Invented new anonymous provider","base_url":"http://fixture-new.invalid/v1","wire_api":"responses","requires_openai_auth":false})
}
fn creation_user_layer<'a>(read: &'a Value, case: &Case) -> Result<&'a Value> {
    layer_version(read, case)?; // Unique, enabled user file; same canonical target AND object.
    read["layers"]
        .as_array()
        .unwrap()
        .iter()
        .find(|l| l["name"]["type"] == "user" && l["name"]["profile"].is_null())
        .ok_or_else(|| "creation user layer unavailable".into())
}
fn creation_absent(read: &Value, case: &Case) -> Result<()> {
    let layer = creation_user_layer(read, case)?;
    for map in [
        &layer["config"]["model_providers"],
        &read["config"]["model_providers"],
    ] {
        require(
            map.as_object()
                .is_some_and(|m| !m.contains_key(CREATION_ID)),
            "literal creation ID not proven absent from both native user and effective maps",
        )?;
    }
    Ok(())
}
fn creation_entry(path: &Path, content: bool) -> Value {
    // Failure evidence must survive a changed type or invalid TOML. Never follow
    // a substituted target symlink, including after a lost write acknowledgement.
    let observed = (|| -> Result<Value> {
        let m = io(fs::symlink_metadata(path))?;
        let mut out = json!({"dev":m.dev(),"inode":m.ino(),"mode":m.mode(),"uid":m.uid(),"gid":m.gid(),"nlink":m.nlink(),
            "type":if m.file_type().is_symlink(){"symlink"}else if m.is_file(){"regular"}else if m.is_dir(){"directory"}else{"other"}});
        if m.file_type().is_symlink() {
            out["rawTarget"] = json!(io(fs::read_link(path))?);
        }
        if content && m.is_file() {
            let mut f = io(OpenOptions::new()
                .read(true)
                .custom_flags(libc::O_NOFOLLOW)
                .open(path))?;
            let held = io(f.metadata())?;
            require(
                (held.dev(), held.ino()) == (m.dev(), m.ino()),
                "target changed during effect observation",
            )?;
            let mut bytes = Vec::new();
            io(f.read_to_end(&mut bytes))?;
            out["bytes"] =
                json!(String::from_utf8(bytes).map_err(|_| "target encoding unavailable")?);
            out["semantics"] = match toml::from_str::<toml::Value>(out["bytes"].as_str().unwrap()) {
                Ok(value) => json!(value),
                Err(e) => json!({"tomlObservationError":e.to_string()}),
            };
        }
        Ok(out)
    })();
    observed.unwrap_or_else(|e| json!({"observationUnavailable":e}))
}
fn creation_state(case: &Case) -> Value {
    json!({"link":creation_entry(&case.plan.native_path().join("config.toml"),false),"target":creation_entry(&case.target,true)})
}
struct CreationAttempt {
    reply: Result<Value>,
    after: Value,
    reread: Result<Value>,
}
fn creation_attempt(
    case: &Case,
    native: &mut Native,
    version: &str,
    value: Value,
) -> Result<CreationAttempt> {
    let params = write_params(case, version, CREATION_KEY, value)?;
    let reply = native.send("config/batchWrite", params); // Exactly one attempt; no retry or rollback.
    let after = creation_state(case);
    save(&case.root.join("after-write.json"), &after)?;
    let reread = native.read(case);
    save(
        &case.root.join("attempt.json"),
        &json!({"reply":match &reply {Ok(v)=>json!({"frame":v}),Err(e)=>json!({"unknown":e})},
        "reread":match &reread {Ok(v)=>json!({"response":v}),Err(e)=>json!({"unavailable":e})},"writeAttempts":1,"replay":false}),
    )?;
    Ok(CreationAttempt {
        reply,
        after,
        reread,
    })
}
fn creation_matches(
    before: &Value,
    after: &Value,
    first: &Value,
    reread: &Value,
    case: &Case,
    definition: &Value,
) -> Result<()> {
    require(
        before["link"] == after["link"] && after["link"]["type"] == "symlink",
        "creation changed receiving link identity/type/raw destination",
    )?;
    require(
        after["target"]["type"] == "regular",
        "creation target is no longer regular",
    )?;
    let mut expected_file = before["target"]["semantics"].clone();
    expected_file["model_providers"][CREATION_ID] = definition.clone();
    require(
        after["target"]["semantics"] == expected_file,
        "whole-object edit changed siblings, selection/model or unrelated file semantics",
    )?;
    let mut expected_user = creation_user_layer(first, case)?["config"].clone();
    expected_user["model_providers"][CREATION_ID] = definition.clone();
    require(
        creation_user_layer(reread, case)?["config"] == expected_user,
        "native user layer did not report the exact literal ID/full requested object",
    )?;
    // Config/read materializes supplier-default fields in effective provider rows.
    // Derive that shape from the same read's anonymous four-field sibling, then
    // require the ENTIRE effective config, including every other row, to agree.
    let mut expected_effective = first["config"].clone();
    let mut row = first["config"]["model_providers"]["fixture_normal"].clone();
    require(
        row.is_object(),
        "effective sibling/default shape unavailable",
    )?;
    for (key, value) in definition
        .as_object()
        .ok_or("definition is not an object")?
    {
        row[key] = value.clone();
    }
    expected_effective["model_providers"][CREATION_ID] = row;
    require(
        reread["config"] == expected_effective,
        "effective full definition/defaults or other configuration differs",
    )
}
fn creation_case(
    input: &Input,
    proof: &Path,
    name: &str,
    observe: impl FnOnce(&Case, &mut Native) -> Result<Value>,
) -> Result<()> {
    creation_seeded_case(input, proof, name, None, observe)
}
fn creation_seeded_case(
    input: &Input,
    proof: &Path,
    name: &str,
    seed: Option<Value>,
    observe: impl FnOnce(&Case, &mut Native) -> Result<Value>,
) -> Result<()> {
    let case = Case::new(proof, name)?;
    if let Some(seed) = seed {
        creation_fixture_insert(&case, &seed)?;
    }
    save(&case.root.join("prepared.json"), &creation_state(&case))?;
    let mut native = Native::open(input, &case, &[])?;
    let outcome = native
        .initialize()
        .and_then(|()| observe(&case, &mut native));
    let after = save(
        &case.root.join("final-filesystem.json"),
        &creation_state(&case),
    );
    let recorded = match &outcome {
        Ok(effects) => save(&case.root.join("effects.json"), effects),
        Err(e) => save(
            &case.root.join("obstacle.json"),
            &json!({"condition":e,"replay":false}),
        ),
    };
    let cleanup = native.close();
    outcome.map(|_| ()).and(after).and(recorded).and(cleanup)
}
fn creation_fixture_insert(case: &Case, definition: &Value) -> Result<()> {
    // Controlled fixture actor only. Append one known four-field definition;
    // retain the existing selected provider/model, bytes and target object.
    require(
        case.plan.resolved_config_write_target()? == case.target,
        "fixture insert target changed",
    )?;
    require(
        definition.as_object().is_some_and(|m| m.len() == 4)
            && definition["requires_openai_auth"] == false,
        "fixture seed shape differs",
    )?;
    let addition = format!("\n[model_providers.\"fixture.new\"]\nname = {}\nbase_url = {}\nwire_api = {}\nrequires_openai_auth = false\n",
        serde_json::to_string(&definition["name"]).map_err(|e|e.to_string())?,
        serde_json::to_string(&definition["base_url"]).map_err(|e|e.to_string())?,
        serde_json::to_string(&definition["wire_api"]).map_err(|e|e.to_string())?);
    io(OpenOptions::new()
        .append(true)
        .custom_flags(libc::O_NOFOLLOW)
        .open(&case.target))?
    .write_all(addition.as_bytes())
    .map_err(|e| e.to_string())
}
fn creation_external_definition() -> Value {
    json!({"name":"Invented external existing provider","base_url":"http://fixture-external.invalid/v1","wire_api":"responses","requires_openai_auth":false})
}
fn creation_has_error_tag(value: &Value, tag: &str) -> bool {
    match value {
        Value::String(s) => s == tag,
        Value::Array(a) => a.iter().any(|v| creation_has_error_tag(v, tag)),
        Value::Object(o) => o.values().any(|v| creation_has_error_tag(v, tag)),
        _ => false,
    }
}
fn provider_creation_stale(input: &Input, proof: &Path) -> Result<()> {
    creation_case(input, proof, "creation-stale-collision", |case, native| {
        let first = native.read(case)?;
        creation_absent(&first, case)?;
        let v1 = layer_version(&first, case)?;
        let before = creation_state(case);
        let external_definition = creation_external_definition();
        creation_fixture_insert(case, &external_definition)?;
        let external = creation_state(case);
        save(&case.root.join("external-edit.json"), &external)?;
        require(
            before["target"]["inode"] == external["target"]["inode"],
            "controlled external edit unexpectedly replaced target",
        )?;
        let changed = native.read(case)?;
        let v_external = layer_version(&changed, case)?;
        require(
            v_external != v1,
            "controlled insertion did not produce a distinct native version",
        )?;
        creation_matches(
            &before,
            &external,
            &first,
            &changed,
            case,
            &external_definition,
        )?;
        save(&case.root.join("before-write.json"), &external)?;
        let attempt = creation_attempt(case, native, &v1, creation_definition())?;
        let reply = attempt.reply?;
        let error = error_frame(&reply)?;
        require(
            error["code"] == -32600
                && creation_has_error_tag(&error["data"], "configVersionConflict"),
            "genuine stale-version error tag unestablished; no collision inference",
        )?;
        require(
            external == attempt.after,
            "stale write changed the external definition or other file/link effects",
        )?;
        let reread = attempt.reread?;
        require(
            layer_version(&reread, case)? == v_external
                && reread["config"] == changed["config"]
                && creation_user_layer(&reread, case)?["config"]
                    == creation_user_layer(&changed, case)?["config"],
            "stale reread did not preserve external definition/configuration",
        )?;
        Ok(
            json!({"status":"actual-stale-version-conflict","nativeError":error,"nativeVersionAbsentRead":v1,"nativeVersionControlledInsertion":v_external,
            "absenceBeforeExternalInsert":true,"sameIdExternallyCreated":true,"externalDefinition":external_definition,"externalDefinitionAndOtherEffectsPreserved":true,
            "writeAttempts":1,"retry":false,"limit":"version conflict only, not a provider-name collision oracle or universal arbitrary-writer exclusion"}),
        )
    })
}
fn provider_creation_existing(input: &Input, proof: &Path) -> Result<()> {
    creation_seeded_case(
        input,
        proof,
        "creation-existing-fresh",
        Some(creation_external_definition()),
        |case, native| {
            let first = native.read(case)?;
            let version = layer_version(&first, case)?;
            let layer = creation_user_layer(&first, case)?;
            require(
                layer["config"]["model_providers"][CREATION_ID] == creation_external_definition()
                    && first["config"]["model_providers"]
                        .get(CREATION_ID)
                        .is_some(),
                "same literal provider ID not already present at fresh native read",
            )?;
            let before = creation_state(case);
            save(&case.root.join("before-write.json"), &before)?;
            let definition = creation_definition();
            let attempt = creation_attempt(case, native, &version, definition.clone())?;
            let reply = attempt.reply?;
            let reread = attempt.reread?;
            if reply.get("error").is_some() {
                let error = error_frame(&reply)?;
                require(
                    before == attempt.after,
                    "existing-ID refusal changed filesystem effects",
                )?;
                require(
                    reread["config"] == first["config"],
                    "existing-ID refusal changed effective config",
                )?;
                return Ok(
                    json!({"status":"actual-existing-id-refusal","nativeError":error,"sameIdPresentAtFreshRead":true,"effectsUnchanged":true,
                "writeAttempts":1,"retry":false,"limit":"one native refusal, not a universal create-if-absent protection"}),
                );
            }
            let result = accepted_write(&reply, case)?;
            creation_matches(&before, &attempt.after, &first, &reread, case, &definition)?;
            require(
                result["version"] == layer_version(&reread, case)? && result["version"] != version,
                "existing-ID write/reread versions differ",
            )?;
            require(
                result["status"] == "ok" && result["overriddenMetadata"].is_null(),
                "existing-ID control unexpectedly overridden",
            )?;
            Ok(
                json!({"status":"actual-existing-id-replaced","sameIdPresentAtFreshRead":true,"writeResponse":result,"oldDefinition":creation_external_definition(),"newDefinition":definition,
            "siblingsSelectionModelAndOtherSettingsPreserved":true,"receivingLinkUnchanged":true,"targetInodeReplaced":before["target"]["inode"]!=attempt.after["target"]["inode"],"writeAttempts":1,"retry":false,
            "limit":"replace accepts an existing ID at its fresh version; not create-only protection or product overwrite permission"}),
            )
        },
    )
}
fn provider_creation_malformed(input: &Input, proof: &Path) -> Result<()> {
    const MARKER: &str = "INVENTED_CREATION_VALUE_A9";
    creation_case(
        input,
        proof,
        "creation-malformed-INVENTED_CREATION_PATH_A9",
        |case, native| {
            let first = native.read(case)?;
            creation_absent(&first, case)?;
            let version = layer_version(&first, case)?;
            let before = creation_state(case);
            save(&case.root.join("before-write.json"), &before)?;
            let mut malformed = creation_definition();
            malformed["name"] = json!(MARKER);
            malformed["wire_api"] = json!(17); // Malformed field inside the one complete object.
            let attempt = creation_attempt(case, native, &version, malformed)?;
            let reply = attempt.reply?;
            let error = error_frame(&reply)?;
            let error_text = serde_json::to_string(error).map_err(|e| e.to_string())?;
            let error_facts = json!({"nativeError":error,"errorReflectsValueMarker":error_text.contains(MARKER),
            "errorReflectsPathMarker":error_text.contains("INVENTED_CREATION_PATH_A9"),
            "errorReflectsFullTarget":error_text.contains(case.target.to_str().ok_or("target encoding")?),
            "errorReflectsProviderId":error_text.contains(CREATION_ID),"fileAndLinkUnchanged":before==attempt.after});
            save(&case.root.join("diagnostic-reflection.json"), &error_facts)?;
            // Inspect actual state independently; an error alone proves no absence of effects.
            require(
                before == attempt.after,
                "malformed-definition error had changed filesystem effects; no retry/rollback",
            )?;
            let reread = attempt.reread?;
            creation_absent(&reread, case)?;
            require(
                reread["config"] == first["config"] && layer_version(&reread, case)? == version,
                "malformed definition changed actual reread",
            )?;
            Ok(
                json!({"status":"actual-malformed-whole-definition-refused","reflection":error_facts,"actualRereadUnchanged":true,"writeAttempts":1,"retry":false,
            "publicSummary":"Provider creation was refused; native diagnostic withheld.","limit":"one invented-only error reflection observation, no general nonreflection or implemented App privacy guarantee"}),
            )
        },
    )
}
fn provider_creation_positive(input: &Input, proof: &Path) -> Result<()> {
    creation_case(input, proof, "absent-replace", |case, native| {
        let first = native.read(case)?;
        creation_absent(&first, case)?;
        let v1 = layer_version(&first, case)?;
        let before = creation_state(case);
        save(&case.root.join("before-write.json"), &before)?;
        require(
            before["target"]["semantics"]["model_providers"]
                .as_object()
                .is_some_and(|m| !m.contains_key(CREATION_ID)),
            "fixture file did not prove literal ID absent",
        )?;
        let definition = creation_definition();
        let attempt = creation_attempt(case, native, &v1, definition.clone())?;
        let reply = attempt.reply?;
        let reread = attempt.reread?;
        if reply.get("error").is_some() {
            error_frame(&reply)?;
            save(
                &case.root.join("refusal.json"),
                &json!({"nativeError":reply["error"],"fileUnchanged":before==attempt.after,"actualReread":reread,"upsertAttempted":false}),
            )?;
            return Err("whole-definition replace genuinely refused; no creation warrant or same-case fallback".into());
        }
        let result = accepted_write(&reply, case)?;
        creation_matches(&before, &attempt.after, &first, &reread, case, &definition)?;
        let v2 = layer_version(&reread, case)?;
        require(
            result["version"] == v2 && v2 != v1,
            "creation acknowledgement and actual reread versions differ",
        )?;
        require(
            result["status"] == "ok" && result["overriddenMetadata"].is_null(),
            "creation baseline unexpectedly overridden",
        )?;
        Ok(
            json!({"status":"actual-absent-provider-created","userAndEffectiveAbsenceBefore":true,"exactQuotedProviderId":CREATION_ID,"keyPath":CREATION_KEY,"requestedObject":definition,
            "writeResponse":result,"nativeVersionBefore":v1,"nativeVersionAfter":v2,"receivingLinkUnchanged":true,"targetInodeReplaced":before["target"]["inode"]!=attempt.after["target"]["inode"],
            "targetModeBefore":before["target"]["mode"],"targetModeAfter":attempt.after["target"]["mode"],"siblingsSelectionModelAndOtherSettingsPreserved":true,"writeAttempts":1,"replay":false,
            "limit":"supplier contract only; no App adoption, create-only primitive, person act, provenance, filesystem CAS or atomic target/profile commit"}),
        )
    })
}

#[test]
#[ignore = "actual provider creation supplier case: separate opt-in plus bound input; never ordinary CI"]
fn stock_linked_provider_creation_contract() {
    require(
        std::env::var("CHIRALITY_PROVIDER_CREATION_CONTRACT").as_deref()
            == Ok("stock-0.160-invented-only"),
        "NOT RUN: set CHIRALITY_PROVIDER_CREATION_CONTRACT=stock-0.160-invented-only explicitly",
    )
    .unwrap_or_else(|e| panic!("{e}"));
    let selection =
        std::env::var("CHIRALITY_PROVIDER_CREATION_CASES").unwrap_or_else(|_| "all".into());
    require(
        matches!(
            selection.as_str(),
            "all" | "positive" | "remaining" | "existing-and-malformed"
        ),
        "NOT RUN: creation cases must be all, positive, remaining or existing-and-malformed",
    )
    .unwrap_or_else(|e| panic!("{e}"));
    let input = Input::guarded().unwrap_or_else(|e| panic!("{e}"));
    let proof = fresh_root().expect("private provider-creation proof root");
    eprintln!(
        "private provider-creation contract root: {}; cases={selection}",
        proof.display()
    );
    save(&proof.join("input.json"),&json!({"root":input.root,"binary":input.binary,"binarySha256":BINARY_SHA,"archiveSha256":ARCHIVE_SHA,"bindingRoot":input.binding["root"],"vendorWarrant":input.binding["vendorTree"],
        "limit":"reused authenticated immutable fullvendor warrant; no inventory, version probe, App, account, server, model or person act"})).unwrap();
    let result: Result<()> = (|| {
        if matches!(selection.as_str(), "all" | "positive") {
            provider_creation_positive(&input, &proof)?;
        }
        if selection != "positive" {
            if selection != "existing-and-malformed" {
                provider_creation_stale(&input, &proof)?;
            }
            provider_creation_existing(&input, &proof)?;
            provider_creation_malformed(&input, &proof)?;
        }
        Ok(())
    })();
    if let Err(e) = result {
        save(&proof.join("obstacle.json"),&json!({"condition":e,"result":"creation contract unestablished; inspect owned effects; never replay"})).unwrap();
        panic!("provider-creation contract unestablished; private diagnostic withheld");
    }
    eprintln!("selected provider-creation observations retained privately; no product/person/qualification claim");
}
