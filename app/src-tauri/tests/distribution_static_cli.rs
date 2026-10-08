#![cfg(unix)]
use chirality_app_v4_lib::distribution_preflight::{equal, scan, Inventory};
use std::{
    fs,
    os::unix::fs::{symlink, PermissionsExt},
    path::{Path, PathBuf},
    process::{Command, Output},
};
struct Fixture(PathBuf);
impl Fixture {
    fn new() -> Self {
        let root = std::env::temp_dir().canonicalize().unwrap().join(format!(
            "distribution-static-{}",
            chirality_app_v4_lib::util::opaque_id("fixture-").unwrap()
        ));
        fs::create_dir(&root).unwrap();
        fs::create_dir(root.join("bin")).unwrap();
        fs::write(root.join("bin/entry"), b"invented executable bytes\n").unwrap();
        fs::set_permissions(root.join("bin/entry"), fs::Permissions::from_mode(0o755)).unwrap();
        Self(root)
    }
}
impl Drop for Fixture {
    fn drop(&mut self) {
        let _ = fs::remove_dir_all(&self.0);
    }
}
fn invoke(args: &[&std::ffi::OsStr]) -> Output {
    Command::new(
        std::env::var_os("DISTRIBUTION_STATIC_BIN")
            .expect("set DISTRIBUTION_STATIC_BIN to the explicitly built scanner example"),
    )
    .args(args)
    .output()
    .unwrap()
}
fn observed(root: &Path) -> (Inventory, Vec<u8>) {
    let out = invoke(&["scan".as_ref(), root.as_os_str()]);
    assert!(
        out.status.success(),
        "{}",
        String::from_utf8_lossy(&out.stderr)
    );
    assert!(out.stderr.is_empty());
    assert!(out.stdout.ends_with(b"\n"));
    (serde_json::from_slice(&out.stdout).unwrap(), out.stdout)
}
#[test]
#[ignore = "requires explicitly built scanner and DISTRIBUTION_STATIC_BIN"]
fn scanner_binary_outputs_complete_stable_inventory_without_tree_writes() {
    let f = Fixture::new();
    let before = scan(&f.0).unwrap();
    let stamp = fs::metadata(f.0.join("bin/entry"))
        .unwrap()
        .modified()
        .unwrap();
    let (first, bytes) = observed(&f.0);
    let (second, repeated) = observed(&f.0);
    assert!(equal(&before, &first));
    assert!(equal(&first, &second));
    assert_eq!(bytes, repeated);
    assert_eq!(
        stamp,
        fs::metadata(f.0.join("bin/entry"))
            .unwrap()
            .modified()
            .unwrap()
    );
    assert!(first
        .entries
        .iter()
        .any(|e| e.path == "." && e.kind == "dir"));
    assert!(first.entries.iter().any(|e| e.path == "bin/entry"
        && e.mode == 0o755
        && e.size.is_some()
        && e.sha256.is_some()));
}
#[test]
#[ignore = "requires explicitly built scanner and DISTRIBUTION_STATIC_BIN"]
fn scanner_binary_detects_bytes_modes_and_file_to_directory_changes() {
    let f = Fixture::new();
    let (original, _) = observed(&f.0);
    fs::write(f.0.join("bin/entry"), b"mutated").unwrap();
    assert!(!equal(&original, &observed(&f.0).0));
    let (bytes_changed, _) = observed(&f.0);
    fs::set_permissions(f.0.join("bin/entry"), fs::Permissions::from_mode(0o644)).unwrap();
    let (mode_changed, _) = observed(&f.0);
    assert!(!equal(&bytes_changed, &mode_changed));
    assert_eq!(
        bytes_changed.manifest_sha256, mode_changed.manifest_sha256,
        "mode checking requires full inventory"
    );
    fs::remove_file(f.0.join("bin/entry")).unwrap();
    fs::create_dir(f.0.join("bin/entry")).unwrap();
    assert!(!equal(&mode_changed, &observed(&f.0).0));
}
#[test]
#[ignore = "requires explicitly built scanner and DISTRIBUTION_STATIC_BIN"]
fn scanner_binary_refuses_symlinks_hardlinks_wrong_root_and_bad_arguments() {
    let f = Fixture::new();
    symlink("entry", f.0.join("bin/link")).unwrap();
    let out = invoke(&["scan".as_ref(), f.0.as_os_str()]);
    assert!(!out.status.success());
    assert!(out.stdout.is_empty());
    fs::remove_file(f.0.join("bin/link")).unwrap();
    fs::hard_link(f.0.join("bin/entry"), f.0.join("bin/hard")).unwrap();
    assert!(!invoke(&["scan".as_ref(), f.0.as_os_str()]).status.success());
    for args in [
        vec![],
        vec!["scan".as_ref()],
        vec!["scan".as_ref(), "relative".as_ref()],
        vec!["unknown".as_ref(), f.0.as_os_str()],
        vec!["scan".as_ref(), f.0.join("bin/entry").as_os_str()],
    ] {
        let out = invoke(&args);
        assert!(!out.status.success());
        assert!(out.stdout.is_empty());
        assert!(!out.stderr.is_empty());
    }
}

#[test]
#[ignore = "requires explicitly built scanner and DISTRIBUTION_STATIC_BIN"]
fn scanner_compare_uses_public_equal_and_distinguishes_difference_from_error() {
    let f = Fixture::new();
    let (inventory, bytes) = observed(&f.0);
    let expected = f.0.join("expected.json");
    let actual = f.0.join("actual.json");
    fs::write(&expected, &bytes).unwrap();
    fs::write(&actual, &bytes).unwrap();
    let compare = || invoke(&["compare".as_ref(), expected.as_os_str(), actual.as_os_str()]);
    let out = compare();
    assert!(out.status.success());
    assert_eq!(out.stdout, b"{\"equal\":true}\n");
    let mut changed = inventory.clone();
    changed.entries[0].mode ^= 0o100;
    fs::write(&actual, serde_json::to_vec(&changed).unwrap()).unwrap();
    let out = compare();
    assert!(out.status.success());
    assert_eq!(out.stdout, b"{\"equal\":false}\n");
    changed = inventory.clone();
    changed.entries.push(changed.entries[0].clone());
    fs::write(&actual, serde_json::to_vec(&changed).unwrap()).unwrap();
    assert_eq!(compare().stdout, b"{\"equal\":false}\n");
    fs::write(&actual, b"{}").unwrap();
    let out = compare();
    assert!(!out.status.success());
    assert!(out.stdout.is_empty());
}

#[test]
#[ignore = "requires explicitly built scanner and DISTRIBUTION_STATIC_BIN"]
fn scanner_compare_refuses_fifo_links_directories_and_oversize_without_hanging() {
    use std::os::unix::ffi::OsStrExt;
    use std::process::Stdio;
    use std::time::{Duration, Instant};
    let f = Fixture::new();
    let (_, bytes) = observed(&f.0);
    let regular = f.0.join("regular.json");
    fs::write(&regular, bytes).unwrap();
    let linked = f.0.join("linked.json");
    symlink(&regular, &linked).unwrap();
    let fifo = f.0.join("fifo");
    let name = std::ffi::CString::new(fifo.as_os_str().as_bytes()).unwrap();
    assert_eq!(unsafe { libc::mkfifo(name.as_ptr(), 0o600) }, 0);
    let oversized = f.0.join("oversized.json");
    fs::File::create(&oversized)
        .unwrap()
        .set_len(64 * 1024 * 1024 + 1)
        .unwrap();
    for bad in [&linked, &fifo, &f.0, &oversized] {
        for (left, right) in [(bad, &regular), (&regular, bad)] {
            let mut child = Command::new(std::env::var_os("DISTRIBUTION_STATIC_BIN").unwrap())
                .arg("compare")
                .arg(left)
                .arg(right)
                .stdout(Stdio::piped())
                .stderr(Stdio::piped())
                .spawn()
                .unwrap();
            let deadline = Instant::now() + Duration::from_secs(3);
            loop {
                if child.try_wait().unwrap().is_some() {
                    break;
                }
                if Instant::now() >= deadline {
                    let _ = child.kill();
                    let _ = child.wait();
                    panic!("compare hung on nonregular/link/oversized input");
                }
                std::thread::sleep(Duration::from_millis(10));
            }
            let output = child.wait_with_output().unwrap();
            assert!(!output.status.success());
            assert!(output.stdout.is_empty());
            assert!(!output.stderr.is_empty());
        }
    }
}
