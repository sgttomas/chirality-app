//! CGP restricted installed-Git envelope. No shell, inherited config or writes to source.
use std::{
    path::{Path, PathBuf},
    sync::{
        atomic::{AtomicBool, AtomicUsize, Ordering},
        Arc,
    },
    time::{Duration, Instant},
};
#[derive(Debug, Clone)]
pub struct Failure {
    pub kind: &'static str,
    pub detail: String,
    pub whole: bool,
}
impl Failure {
    pub fn side(kind: &'static str, s: impl Into<String>) -> Self {
        Self {
            kind,
            detail: s.into(),
            whole: false,
        }
    }
    pub fn abort(kind: &'static str, s: impl Into<String>) -> Self {
        Self {
            kind,
            detail: s.into(),
            whole: true,
        }
    }
}
pub type Result<T> = std::result::Result<T, Failure>;
pub struct Control {
    pub cancel: Arc<AtomicBool>,
    pub deadline: Instant,
    stderr: AtomicUsize,
}
impl Control {
    pub fn new(cancel: Arc<AtomicBool>) -> Self {
        Self {
            cancel,
            deadline: Instant::now() + Duration::from_secs(10),
            stderr: AtomicUsize::new(0),
        }
    }
    pub fn check(&self) -> Result<()> {
        if self.cancel.load(Ordering::SeqCst) {
            Err(Failure::abort("cancelled", "Git request cancelled"))
        } else if Instant::now() >= self.deadline {
            Err(Failure::abort(
                "deadline",
                "Overall Git request deadline exceeded",
            ))
        } else {
            Ok(())
        }
    }
}
pub struct Engine {
    pub helper: PathBuf,
    pub executable: PathBuf,
    pub version: String,
    identity: serde_json::Value,
    helper_identity: (u64, u64),
}
impl Engine {
    pub fn create(objects: &Path, format: &str, control: &Control) -> Result<Self> {
        use std::os::unix::fs::DirBuilderExt;
        let helper = std::env::temp_dir().join(
            crate::util::opaque_id("connector-git-")
                .map_err(|e| Failure::abort("supervision", e))?,
        );
        std::fs::DirBuilder::new()
            .mode(0o700)
            .create(&helper)
            .map_err(|e| Failure::abort("supervision", e.to_string()))?;
        let mut engine = Self {
            helper,
            executable: PathBuf::from("/usr/bin/git"),
            version: String::new(),
            identity: serde_json::Value::Null,
            helper_identity: (0, 0),
        };
        {
            use std::os::unix::fs::MetadataExt;
            let m = std::fs::symlink_metadata(&engine.helper)
                .map_err(|e| Failure::abort("supervision", e.to_string()))?;
            engine.helper_identity = (m.dev(), m.ino());
        }
        for name in ["objects", "refs"] {
            std::fs::create_dir(engine.helper.join(name))
                .map_err(|e| Failure::abort("supervision", e.to_string()))?;
        }
        std::fs::write(engine.helper.join("HEAD"), b"ref: refs/heads/unused\n")
            .map_err(|e| Failure::abort("supervision", e.to_string()))?;
        let config = if format == "sha256" {
            "[core]\nrepositoryformatversion = 1\nbare = true\n[extensions]\nobjectformat = sha256\n"
        } else {
            "[core]\nrepositoryformatversion = 0\nbare = true\n"
        };
        std::fs::write(engine.helper.join("config"), config)
            .map_err(|e| Failure::abort("supervision", e.to_string()))?;
        engine.identity = executable_identity(&engine.executable)?;
        engine.version =
            String::from_utf8(engine.run(objects, &["--version"], b"", 1024, control)?)
                .map_err(|_| Failure::abort("capability", "Git version is not UTF-8"))?;
        if !engine.version.starts_with("git version ") {
            return Err(Failure::abort(
                "capability",
                "Unrecognized installed Git version response",
            ));
        }
        if !engine
            .run(
                objects,
                &["cat-file", "--batch", "--no-use-mailmap"],
                b"",
                1,
                control,
            )?
            .is_empty()
        {
            return Err(Failure::abort(
                "capability",
                "Unexpected cat-file capability response",
            ));
        }
        Ok(engine)
    }
    pub fn identity(&self) -> serde_json::Value {
        serde_json::json!({"executable":self.executable,"version":self.version.trim_end(),"identity":self.identity,"standing":"same installed Git for reads and rehash; not independent cryptography or compromised-binary protection","isolation":"cleared environment and minimal private config; no OS network sandbox claim"})
    }
    pub fn verify(&self) -> Result<()> {
        if executable_identity(&self.executable)? != self.identity {
            Err(Failure::abort("capability", "Git executable changed"))
        } else {
            Ok(())
        }
    }
    pub fn run(
        &self,
        objects: &Path,
        args: &[&str],
        input: &[u8],
        cap: usize,
        control: &Control,
    ) -> Result<Vec<u8>> {
        use std::{
            io::{Read, Write},
            os::unix::{io::AsRawFd, process::CommandExt},
            process::{Command, Stdio},
        };
        control.check()?;
        let mut command = Command::new(&self.executable);
        command
            .env_clear()
            .env("PATH", "")
            .env("HOME", &self.helper)
            .env("XDG_CONFIG_HOME", &self.helper)
            .env("GIT_CONFIG_NOSYSTEM", "1")
            .env("GIT_CONFIG_SYSTEM", "/dev/null")
            .env("GIT_CONFIG_GLOBAL", "/dev/null")
            .env("GIT_TERMINAL_PROMPT", "0")
            .env("GIT_ALLOW_PROTOCOL", "")
            .env("GIT_PROTOCOL_FROM_USER", "0")
            .env("GIT_OBJECT_DIRECTORY", objects)
            .env("LC_ALL", "C")
            .arg("--no-pager")
            .arg("--no-lazy-fetch")
            .arg("--no-replace-objects")
            .arg("--no-optional-locks")
            .arg(format!("--git-dir={}", self.helper.display()))
            .arg("-c")
            .arg("protocol.allow=never")
            .args(args)
            .current_dir(&self.helper)
            .stdin(Stdio::piped())
            .stdout(Stdio::piped())
            .stderr(Stdio::piped());
        unsafe {
            command.pre_exec(|| {
                if libc::setpgid(0, 0) != 0 {
                    return Err(std::io::Error::last_os_error());
                }
                Ok(())
            });
        }
        let mut child = command
            .spawn()
            .map_err(|e| Failure::abort("capability", format!("Installed Git unavailable: {e}")))?;
        let pid = child.id() as i32;
        let mut stdin = child.stdin.take();
        let mut stdout = child.stdout.take().unwrap();
        let mut stderr = child.stderr.take().unwrap();
        let mut output = Vec::new();
        let mut errors = Vec::new();
        let mut sent = 0;
        let mut out_end = false;
        let mut err_end = false;
        let result = (|| {
            for fd in [
                stdin.as_ref().unwrap().as_raw_fd(),
                stdout.as_raw_fd(),
                stderr.as_raw_fd(),
            ] {
                let flags = unsafe { libc::fcntl(fd, libc::F_GETFL) };
                if flags < 0
                    || unsafe { libc::fcntl(fd, libc::F_SETFL, flags | libc::O_NONBLOCK) } < 0
                {
                    return Err(Failure::abort(
                        "supervision",
                        "Cannot establish nonblocking pipe supervision",
                    ));
                }
            }
            loop {
                control.check()?;
                if let Some(pipe) = stdin.as_mut() {
                    if sent == input.len() {
                        stdin = None;
                    } else {
                        match pipe.write(&input[sent..]) {
                            Ok(0) => {
                                return Err(Failure::side(
                                    "framing",
                                    "Git closed input before payload completed",
                                ))
                            }
                            Ok(n) => sent += n,
                            Err(e) if e.kind() == std::io::ErrorKind::WouldBlock => {}
                            Err(e) => return Err(Failure::side("command", e.to_string())),
                        }
                    }
                }
                for (reader, buffer, ended, limit, is_error) in [
                    (
                        &mut stdout as &mut dyn Read,
                        &mut output,
                        &mut out_end,
                        cap,
                        false,
                    ),
                    (
                        &mut stderr as &mut dyn Read,
                        &mut errors,
                        &mut err_end,
                        16384,
                        true,
                    ),
                ] {
                    let mut bytes = [0u8; 8192];
                    match reader.read(&mut bytes) {
                        Ok(0) => *ended = true,
                        Ok(n) => {
                            if buffer.len() + n > limit
                                || (is_error
                                    && control.stderr.fetch_add(n, Ordering::SeqCst) + n > 16384)
                            {
                                return Err(Failure::side(
                                    "limit",
                                    "Git output/stderr cap exceeded",
                                ));
                            }
                            buffer.extend_from_slice(&bytes[..n]);
                        }
                        Err(e) if e.kind() == std::io::ErrorKind::WouldBlock => {}
                        Err(e) => return Err(Failure::abort("supervision", e.to_string())),
                    }
                }
                if let Some(status) = child
                    .try_wait()
                    .map_err(|e| Failure::abort("supervision", e.to_string()))?
                {
                    if out_end && err_end {
                        if !status.success() {
                            return Err(Failure::side(
                                "command",
                                format!(
                                    "Git refused operation: {}",
                                    String::from_utf8_lossy(&errors)
                                ),
                            ));
                        }
                        if sent != input.len() {
                            return Err(Failure::side(
                                "framing",
                                "Git exited before accepting whole input",
                            ));
                        }
                        return Ok(output);
                    }
                }
                std::thread::sleep(Duration::from_millis(1));
            }
        })();
        // Always close pipes and kill the isolated group on error, then boundedly reap.
        drop(stdin);
        drop(stdout);
        drop(stderr);
        if result.is_err() {
            unsafe {
                libc::kill(-pid, libc::SIGKILL);
            }
        }
        let cleanup = Instant::now() + Duration::from_secs(1);
        loop {
            match child.try_wait() {
                Ok(Some(_)) => break,
                Ok(None) if Instant::now() < cleanup => {
                    std::thread::sleep(Duration::from_millis(1))
                }
                _ => {
                    return Err(Failure::abort(
                        "supervision",
                        "Unable to establish child termination/reap",
                    ))
                }
            }
        }
        result
    }
}
fn executable_identity(path: &Path) -> Result<serde_json::Value> {
    use std::os::unix::fs::MetadataExt;
    let m = std::fs::metadata(path).map_err(|e| Failure::abort("capability", e.to_string()))?;
    if !m.is_file() {
        return Err(Failure::abort(
            "capability",
            "Git executable is not a regular file",
        ));
    }
    Ok(
        serde_json::json!({"device":m.dev().to_string(),"inode":m.ino().to_string(),"length":m.len().to_string(),"mtime":m.mtime().to_string(),"mtimeNs":m.mtime_nsec().to_string()}),
    )
}
impl Drop for Engine {
    fn drop(&mut self) {
        use std::os::unix::fs::MetadataExt;
        if std::fs::symlink_metadata(&self.helper)
            .is_ok_and(|m| m.is_dir() && (m.dev(), m.ino()) == self.helper_identity)
        {
            let _ = std::fs::remove_dir_all(&self.helper);
        }
    }
}
