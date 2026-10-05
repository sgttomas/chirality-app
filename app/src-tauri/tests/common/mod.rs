//! Temporary directories owned by one test, allocated below the system temp root.
use std::ops::Deref;
use std::path::{Path, PathBuf};
use std::process::Command;

pub struct ScratchDirectory(PathBuf);

impl ScratchDirectory {
    pub fn new(prefix: &str) -> Self {
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
