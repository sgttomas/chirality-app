use super::*;
use crate::connector_source_fs::{Root, LIMIT};
use std::fs;
struct Scratch(PathBuf);
impl Scratch {
    fn new() -> Self {
        let p = std::env::temp_dir().join(opaque_id("source-test-").unwrap());
        fs::create_dir(&p).unwrap();
        Self(p.canonicalize().unwrap())
    }
    fn file(&self, name: &str, bytes: &[u8]) -> PathBuf {
        let p = self.0.join(name);
        fs::write(&p, bytes).unwrap();
        p
    }
}
impl Drop for Scratch {
    fn drop(&mut self) {
        let _ = fs::remove_dir_all(&self.0);
    }
}
fn question() -> Question {
    Question {
        id: "Q-source".into(),
        text: "What is actually readable?".into(),
        asked_revision: "typed-request-not-evidence".into(),
        since_revision: Some("typed-since".into()),
    }
}
fn prepare(root: &Path) -> (Mutex<Session>, String, String) {
    let mut s = Session::default();
    let v = s.prepare(root, question(), "absent".into(), None).unwrap();
    (
        Mutex::new(s),
        v["sessionToken"].as_str().unwrap().into(),
        v["generation"].as_str().unwrap().into(),
    )
}
#[test]
fn connector_source_exact_bytes_limits_and_rejections() {
    let t = Scratch::new();
    let root = Root::open(&t.0).unwrap();
    for bytes in [vec![], b"\xef\xbb\xbfhello\r\n".to_vec(), vec![b'x'; LIMIT]] {
        let p = t.file("text", &bytes);
        let r = root.read(&p).unwrap();
        assert_eq!(r.bytes, bytes);
    }
    for bytes in [vec![b'x'; LIMIT + 1], vec![0], vec![0xff]] {
        let p = t.file("bad", &bytes);
        assert!(root.read(&p).is_err());
    }
    assert!(root.read(&t.0.join("missing")).is_err());
    assert!(root.read(&t.0).is_err());
    let outside = Scratch::new();
    assert!(root.read(&outside.file("outside", b"outside")).is_err());
    assert!(root.read(Path::new("relative")).is_err());
    assert!(root.read(&t.0.join("../escape")).is_err());
}
#[cfg(unix)]
#[test]
fn connector_source_descriptor_symlink_fifo_permissions_and_path_changes() {
    use std::os::unix::{
        ffi::OsStrExt,
        fs::{symlink, PermissionsExt},
    };
    let t = Scratch::new();
    let root = Root::open(&t.0).unwrap();
    let p = t.file("source", b"old");
    symlink(&p, t.0.join("link")).unwrap();
    assert!(root.read(&t.0.join("link")).is_err());
    fs::create_dir(t.0.join("inner")).unwrap();
    t.file("inner/child", b"child");
    symlink(t.0.join("inner"), t.0.join("alias")).unwrap();
    assert!(root.read(&t.0.join("alias/child")).is_err());
    let fifo = t.0.join("fifo");
    let name = std::ffi::CString::new(fifo.as_os_str().as_bytes()).unwrap();
    assert_eq!(unsafe { libc::mkfifo(name.as_ptr(), 0o600) }, 0);
    let mut child = std::process::Command::new(std::env::current_exe().unwrap())
        .args([
            "--exact",
            "connector_source::tests::connector_source_fifo_worker",
            "--nocapture",
        ])
        .env("CHIRALITY_CSP_FIFO_FIXTURE", &fifo)
        .spawn()
        .unwrap();
    let deadline = std::time::Instant::now() + std::time::Duration::from_secs(4);
    loop {
        if let Some(status) = child.try_wait().unwrap() {
            assert!(status.success());
            break;
        }
        if std::time::Instant::now() > deadline {
            child.kill().unwrap();
            let _ = child.wait();
            panic!("FIFO reader exceeded bounded completion");
        }
        std::thread::sleep(std::time::Duration::from_millis(10));
    }
    fs::set_permissions(&p, fs::Permissions::from_mode(0)).unwrap();
    assert!(root.read(&p).is_err());
    fs::set_permissions(&p, fs::Permissions::from_mode(0o600)).unwrap();
    assert!(root
        .read_with(&p, |stage| if stage == "opened" {
            fs::write(&p, b"changed length").unwrap();
        })
        .unwrap_err()
        .contains("Mutation"));
    assert!(root
        .read_with(&p, |stage| if stage == "read" {
            fs::rename(&p, t.0.join("old")).unwrap();
            fs::write(&p, b"replacement").unwrap();
        })
        .is_err());
    let child = t.0.join("inner/child");
    assert!(root
        .read_with(&child, |stage| if stage == "read" {
            fs::rename(t.0.join("inner"), t.0.join("moved")).unwrap();
            fs::create_dir(t.0.join("inner")).unwrap();
            fs::write(&child, b"replacement").unwrap();
        })
        .is_err());
    let renamed = t.0.with_extension("moved");
    fs::rename(&t.0, &renamed).unwrap();
    assert!(root.verify().is_err());
    fs::rename(&renamed, &t.0).unwrap();
}
#[test]
fn connector_source_all_contract_anchor_examples_and_mismatch() {
    for (text, start, end, from, to, expected) in [
        ("a\nb\n", 1, 1, 0, 2, "a\n"),
        ("a\nb\n", 2, 2, 2, 4, "b\n"),
        ("a\r\nb\n", 1, 1, 0, 3, "a\r\n"),
        ("a\r\nb\n", 1, 2, 0, 5, "a\r\nb\n"),
        ("a\nb", 2, 2, 2, 3, "b"),
        ("\n", 1, 1, 0, 1, "\n"),
        ("é\nb", 1, 1, 0, 3, "é\n"),
    ] {
        let v = excerpt(text.as_bytes(), start, end, Some(expected)).unwrap();
        assert_eq!(v["byteStart"], from);
        assert_eq!(v["byteEnd"], to);
        assert_eq!(v["text"], expected);
        assert_eq!(v["sha256"], sha256_hex(expected.as_bytes()));
    }
    for (text, start, end) in [
        ("", 1, 1),
        ("a\n", 2, 2),
        ("a", 0, 1),
        ("a\nb", 2, 1),
        ("a", 1, 2),
    ] {
        assert!(excerpt(text.as_bytes(), start, end, None).is_err());
    }
    assert!(excerpt(b"a\r\n", 1, 1, Some("a\n")).is_err());
    assert_eq!(
        excerpt("\u{feff}é\n".as_bytes(), 1, 1, None).unwrap()["byteEnd"],
        6
    );
}
#[test]
fn connector_source_session_snapshot_cancel_reread_and_no_cold_recreation() {
    let t = Scratch::new();
    let p = t.file("selected", b"revision A\nline2");
    let (s, token, generation) = prepare(&t.0);
    let first = select(&s, &token, &generation, || Ok(Some(p.clone()))).unwrap();
    let observed = first["observation"].clone();
    assert_eq!(observed["read"]["sha256"], sha256_hex(b"revision A\nline2"));
    assert_eq!(observed["read"]["byteLength"], 16);
    assert_eq!(observed["question"]["id"], "Q-source");
    assert_eq!(observed["read"]["selectedPath"], native_path_identity(&p));
    fs::write(&p, b"revision B\n").unwrap();
    assert_eq!(s.lock().unwrap().snapshot()["observation"], observed);
    let cancelled = select(&s, &token, &generation, || Ok(None)).unwrap();
    assert_eq!(cancelled["operation"], "cancelled");
    assert_eq!(cancelled["observation"]["historical"], true);
    assert_eq!(
        cancelled["observation"]["read"]["observedAt"],
        observed["read"]["observedAt"]
    );
    let reread = select(&s, &token, &generation, || Ok(Some(p.clone()))).unwrap();
    assert_ne!(reread["observation"]["reference"], observed["reference"]);
    assert_ne!(
        reread["observation"]["read"]["sha256"],
        observed["read"]["sha256"]
    );
    let r = reread["observation"]["reference"].as_str().unwrap();
    assert!(Session::default()
        .anchor(&token, &generation, r, 1, 1, None)
        .is_err());
    assert!(s
        .lock()
        .unwrap()
        .anchor(&token, &generation, "forged-path-or-hash", 1, 1, None)
        .is_err());
    assert_eq!(fs::read_dir(&t.0).unwrap().count(), 1); // no persistence directories
}
#[test]
fn connector_source_stale_completions_reentrancy_and_revision_assertions() {
    let t = Scratch::new();
    let p = t.file("source", b"Revision: abc123\n");
    let (s, token, generation) = prepare(&t.0);
    let stale = select(&s, &token, &generation, || {
        assert!(select(&s, &token, &generation, || panic!("must not pick")).is_err());
        s.lock()
            .unwrap()
            .prepare(
                &t.0,
                question(),
                "failing".into(),
                Some("assigned manager".into()),
            )
            .unwrap();
        Ok(Some(p.clone()))
    });
    assert!(stale.is_err());
    assert_eq!(s.lock().unwrap().snapshot()["operation"], "prepared");
    let v = s.lock().unwrap().snapshot();
    let token = v["sessionToken"].as_str().unwrap();
    let generation = v["generation"].as_str().unwrap();
    let v = select(&s, token, generation, || Ok(Some(p))).unwrap();
    let r = v["observation"]["reference"].as_str().unwrap();
    let v = s
        .lock()
        .unwrap()
        .revision(
            token,
            generation,
            r,
            "caller_assertion",
            "0123456789abcdef",
            None,
        )
        .unwrap();
    assert_eq!(v["observation"]["revision"]["kind"], "caller_assertion");
    let v = s
        .lock()
        .unwrap()
        .anchor(token, generation, r, 1, 1, Some("Revision: abc123\n"))
        .unwrap();
    let a = v["observation"]["anchors"][0]["reference"]
        .as_str()
        .unwrap();
    let v = s
        .lock()
        .unwrap()
        .revision(
            token,
            generation,
            r,
            "source_text_located",
            "Caller says this is a revision",
            Some(a),
        )
        .unwrap();
    assert_eq!(v["observation"]["revision"]["kind"], "source_text_located");
    assert!(v["observation"]["revision"]["limit"]
        .as_str()
        .unwrap()
        .contains("unverified"));
    assert!(s
        .lock()
        .unwrap()
        .revision(token, generation, r, "git_verified", "abc", None)
        .is_err());
    let v = s
        .lock()
        .unwrap()
        .anchor(token, generation, r, 1, 1, Some("different"))
        .unwrap();
    assert!(v["gaps"]
        .as_array()
        .unwrap()
        .iter()
        .any(|g| g["reason"].as_str().unwrap().contains("mismatch")));
    assert_eq!(v["gaps"][0]["responsible"], "assigned manager");
    for key in ["sources", "facts", "account", "conclusions", "duties"] {
        assert!(v.get(key).is_none());
    }
}
#[test]
fn connector_source_trigger_continuity_and_forged_question_fields() {
    let t = Scratch::new();
    let mut s = Session::default();
    let mut prior = None;
    for trigger in ["absent", "stale", "partial", "failing"] {
        let v = s.prepare(&t.0, question(), trigger.into(), None).unwrap();
        if let Some(q) = &prior {
            assert_eq!(&v["question"], q);
        }
        prior = Some(v["question"].clone());
        assert!(v["gaps"][0]["responsible"].is_null());
    }
    assert!(serde_json::from_value::<Question>(
        json!({"id":"q","text":"t","askedRevision":"r","path":"/forged","sha256":"forged"})
    )
    .is_err());
}

#[test]
fn connector_source_fifo_worker() {
    let Some(path) = std::env::var_os("CHIRALITY_CSP_FIFO_FIXTURE") else {
        return;
    };
    let path = PathBuf::from(path);
    let root = Root::open(path.parent().unwrap()).unwrap();
    assert!(root.read(&path).is_err());
}
#[test]
fn connector_source_failure_continuity_and_lossless_selected_name() {
    use std::os::unix::ffi::OsStringExt;
    let t = Scratch::new();
    let name = if cfg!(target_os = "linux") {
        std::ffi::OsString::from_vec(b"source-\xff".to_vec())
    } else {
        std::ffi::OsString::from("source-é")
    };
    let p = t.0.join(name);
    fs::write(&p, b"original").unwrap();
    let (s, token, generation) = prepare(&t.0);
    let first = select(&s, &token, &generation, || Ok(Some(p.clone()))).unwrap();
    assert_eq!(
        first["observation"]["read"]["selectedPath"],
        native_path_identity(&p)
    );
    assert_eq!(
        !first["observation"]["read"]["pathDisplayLimit"].is_null(),
        p.to_str().is_none()
    );
    for outcome in [
        Err("synthetic picker failure".into()),
        Ok(Some(t.0.join("missing"))),
    ] {
        let failed = select(&s, &token, &generation, || outcome).unwrap();
        assert_eq!(failed["operation"], "failed");
        assert_eq!(failed["observation"]["historical"], true);
        assert_eq!(
            failed["observation"]["reference"],
            first["observation"]["reference"]
        );
        assert_eq!(failed["question"], first["question"]);
        assert_eq!(failed["gaps"].as_array().unwrap().len(), 2);
    }
    let moved = t.0.with_extension("moved");
    fs::rename(&t.0, &moved).unwrap();
    let changed = select(&s, &token, &generation, || {
        panic!("changed association must refuse before picker")
    })
    .unwrap();
    assert_eq!(changed["operation"], "failed");
    assert_eq!(changed["observation"]["historical"], true);
    fs::rename(&moved, &t.0).unwrap();
    assert!(select(&s, "forged", &generation, || panic!(
        "forged token must not pick"
    ))
    .is_err());
    assert!(select(&s, &token, "forged", || panic!(
        "forged generation must not pick"
    ))
    .is_err());
}

#[test]
fn connector_source_failed_read_gap_survives_successful_historical_anchor() {
    let t = Scratch::new();
    let p = t.file("source", b"old\n");
    let (s, token, generation) = prepare(&t.0);
    let first = select(&s, &token, &generation, || Ok(Some(p.clone()))).unwrap();
    let r = first["observation"]["reference"].as_str().unwrap();
    let failed = select(&s, &token, &generation, || {
        Err("DISTINCT_READ_FAILURE".into())
    })
    .unwrap();
    assert!(failed.to_string().contains("DISTINCT_READ_FAILURE"));
    let anchored = s
        .lock()
        .unwrap()
        .anchor(&token, &generation, r, 1, 1, None)
        .unwrap();
    assert!(
        anchored.to_string().contains("DISTINCT_READ_FAILURE"),
        "historical anchor erased unresolved failed-read reason"
    );
    assert_eq!(anchored["operation"], "failed");
    assert_eq!(anchored["observation"]["historical"], true);
    assert_eq!(
        anchored["observation"]["read"],
        first["observation"]["read"]
    );
    let cancelled = select(&s, &token, &generation, || Ok(None)).unwrap();
    assert!(cancelled.to_string().contains("DISTINCT_READ_FAILURE"));
    let recovered = select(&s, &token, &generation, || Ok(Some(p))).unwrap();
    assert!(!recovered.to_string().contains("DISTINCT_READ_FAILURE"));
    assert_eq!(recovered["operation"], "observed");
}
#[test]
fn connector_source_failed_read_and_anchor_mismatch_keep_independent_gaps() {
    let t = Scratch::new();
    let p = t.file("source", b"old\n");
    let (s, token, generation) = prepare(&t.0);
    let first = select(&s, &token, &generation, || Ok(Some(p.clone()))).unwrap();
    let r = first["observation"]["reference"].as_str().unwrap();
    fs::remove_file(&p).unwrap();
    let failed = select(&s, &token, &generation, || Ok(Some(p))).unwrap();
    let read_reason = failed["gaps"][1]["reason"].as_str().unwrap().to_owned();
    let mismatch = s
        .lock()
        .unwrap()
        .anchor(&token, &generation, r, 1, 1, Some("new\n"))
        .unwrap();
    assert!(
        mismatch["gaps"]
            .as_array()
            .unwrap()
            .iter()
            .any(|g| g["reason"] == read_reason),
        "anchor mismatch replaced failed-read cause"
    );
    assert!(mismatch.to_string().contains("Expected excerpt mismatch"));
    assert_eq!(mismatch["operation"], "failed");
    let anchored = s
        .lock()
        .unwrap()
        .anchor(&token, &generation, r, 1, 1, Some("old\n"))
        .unwrap();
    assert!(anchored["gaps"]
        .as_array()
        .unwrap()
        .iter()
        .any(|g| g["reason"] == read_reason));
    assert!(!anchored.to_string().contains("Expected excerpt mismatch"));
    assert_eq!(
        anchored["observation"]["read"],
        first["observation"]["read"]
    );
}
