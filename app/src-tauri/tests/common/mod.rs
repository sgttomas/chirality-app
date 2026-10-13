//! Temporary directories owned by one test, allocated below the system temp root.
use std::ops::Deref;
use std::path::{Path, PathBuf};
use std::process::Command;

pub struct ScratchDirectory(PathBuf);

/// RS §13.8: this test binary's records store, named explicitly (the
/// override variable when set, else one temporary store for the process);
/// never the App data folder.
pub fn records_store() {
    static ONCE: std::sync::Once = std::sync::Once::new();
    ONCE.call_once(|| {
        use chirality_app_v4_lib::records_store::{configure, Placement, Store, OVERRIDE_ENV};
        let root = std::env::var_os(OVERRIDE_ENV)
            .filter(|p| !p.is_empty())
            .map(PathBuf::from)
            .unwrap_or_else(|| std::env::temp_dir().join(format!("chirality-integration-records-{}", std::process::id())));
        configure(Ok(Store { root, placement: Placement::Override, limits: vec![] }));
    });
}

impl ScratchDirectory {
    pub fn new(prefix: &str) -> Self {
        records_store();

        let template = std::env::temp_dir().join(format!("{prefix}.XXXXXX"));
        let out = Command::new("mktemp")
            .arg("-d")
            .arg(&template)
            .output()
            .expect("mktemp must be available for the scratch directory");
        assert!(
            out.status.success(),
            "mktemp failed: {}",
            String::from_utf8_lossy(&out.stderr)
        );
        let path = PathBuf::from(
            String::from_utf8(out.stdout)
                .expect("mktemp path is UTF-8")
                .trim(),
        );
        assert!(
            path.is_absolute() && path.is_dir(),
            "mktemp must return an absolute directory"
        );
        // Codex reports its home canonically, including platform temp-root symlinks.
        Self(std::fs::canonicalize(path).expect("scratch directory resolves"))
    }
}

impl Deref for ScratchDirectory {
    type Target = Path;
    fn deref(&self) -> &Path {
        &self.0
    }
}

impl Drop for ScratchDirectory {
    fn drop(&mut self) {
        if let Err(error) = std::fs::remove_dir_all(&self.0) {
            eprintln!("scratch cleanup failed for {}: {error}", self.0.display());
            // Preserve the original assertion when unwinding, but fail a normal test.
            assert!(std::thread::panicking(), "scratch directory cleanup failed");
        }
    }
}

pub fn evidence_output() -> PathBuf {
    // The Node schema runner owns this directory until every validator completes.
    // Standalone Cargo runs retain their exports under Cargo's test output root.
    std::env::var_os("CHIRALITY_TEST_OUTPUT_DIRECTORY")
        .map(PathBuf::from)
        .unwrap_or_else(|| PathBuf::from(env!("CARGO_TARGET_TMPDIR")).join("skeleton-output"))
}

/// A log's bytes with every complete line linked again to the one before (RS
/// §13.8 Tamper-evidence): a fixture's in-place edit, made consistent as the
/// App would have written it. An unlinked edit reads as a broken chain.
#[allow(dead_code)]
pub fn rechain(bytes: &[u8]) -> Vec<u8> {
    use chirality_app_v4_lib::record_lines::{line_identity, link};
    let mut out = Vec::new();
    let mut previous: Option<String> = None;
    let mut parts: Vec<&[u8]> = bytes.split(|b| *b == b'\n').collect();
    let tail = parts.pop().unwrap_or(b"");
    for raw in parts {
        let line = match serde_json::from_slice::<serde_json::Value>(raw) {
            Ok(mut v) if v.is_object() => {
                v["prevLine"] = link(previous.as_deref());
                serde_json::to_vec(&v).unwrap()
            }
            _ => raw.to_vec(),
        };
        previous = Some(line_identity(&line));
        out.extend(&line);
        out.push(b'\n');
    }
    out.extend(tail);
    out
}
