use super::*;
use std::sync::{
    atomic::{AtomicBool, Ordering},
    Arc,
};
pub(crate) struct Repo {
    pub(crate) root: PathBuf,
    vector: Value,
}
impl Repo {
    pub(crate) fn new(format: &str) -> Self {
        let root = std::env::temp_dir().join(crate::util::opaque_id("git-test-").unwrap());
        fs::create_dir(&root).unwrap();
        let root = root.canonicalize().unwrap();
        fs::create_dir_all(root.join(".git/objects")).unwrap();
        fs::create_dir(root.join(".git/refs")).unwrap();
        fs::write(root.join(".git/HEAD"), b"ref: refs/heads/moved\n").unwrap();
        fs::write(
            root.join(".git/config"),
            if format == "sha256" {
                "[core]\nrepositoryformatversion=1\nbare=false\n[extensions]\nobjectformat=sha256\n"
            } else {
                "[core]\nrepositoryformatversion=0\nbare=false\n"
            },
        )
        .unwrap();
        let all: Value = serde_json::from_str(include_str!(
            "../../tests/fixtures/connector-git/vectors.json"
        ))
        .unwrap();
        let vector = all[format].clone();
        for o in vector["objects"].as_array().unwrap() {
            let id = o["oid"].as_str().unwrap();
            let path = root.join(".git/objects").join(&id[..2]);
            fs::create_dir_all(&path).unwrap();
            fs::write(
                path.join(&id[2..]),
                unhex(o["compressed"].as_str().unwrap()),
            )
            .unwrap();
        }
        fs::write(
            root.join("literal [*].txt"),
            b"dirty local bytes, not a commit\n",
        )
        .unwrap();
        Self { root, vector }
    }
    pub(crate) fn id(&self, key: &str) -> &str {
        self.vector[key].as_str().unwrap()
    }
    fn control() -> Control {
        Control::new(Arc::new(AtomicBool::new(false)))
    }
}
impl Drop for Repo {
    fn drop(&mut self) {
        let _ = fs::remove_dir_all(&self.root);
    }
}
fn unhex(s: &str) -> Vec<u8> {
    s.as_bytes()
        .chunks_exact(2)
        .map(|p| u8::from_str_radix(std::str::from_utf8(p).unwrap(), 16).unwrap())
        .collect()
}
fn snapshot(root: &Path) -> BTreeMap<PathBuf, Vec<u8>> {
    let mut out = BTreeMap::new();
    let mut stack = vec![root.to_path_buf()];
    while let Some(p) = stack.pop() {
        for e in fs::read_dir(p).unwrap() {
            let p = e.unwrap().path();
            if p.is_dir() {
                stack.push(p);
            } else {
                out.insert(p.strip_prefix(root).unwrap().into(), fs::read(p).unwrap());
            }
        }
    }
    out
}
#[test]
fn connector_git_independent_vectors_dirty_worktree_two_pins_and_no_writes() {
    for format in ["sha1", "sha256"] {
        let r = Repo::new(format);
        let before = snapshot(&r.root);
        let result = read(
            &r.root,
            Path::new("literal [*].txt"),
            r.id("at"),
            Some(r.id("since")),
            &Repo::control(),
        )
        .unwrap();
        assert_eq!(result.at.as_ref().unwrap().view["blob"], r.id("new"));
        assert_eq!(
            result.since.as_ref().unwrap().as_ref().unwrap().view["blob"],
            r.id("old")
        );
        assert_eq!(result.at.as_ref().unwrap().bytes, b"new\n\n");
        assert_eq!(
            result.since.as_ref().unwrap().as_ref().unwrap().bytes,
            "old\r\né\n".as_bytes()
        );
        assert!(!result.at.as_ref().unwrap().raw_objects.is_empty());
        assert_eq!(result.view()["status"], "complete");
        assert_eq!(snapshot(&r.root), before);
        let same = read(
            &r.root,
            Path::new("literal [*].txt"),
            r.id("at"),
            Some(r.id("same")),
            &Repo::control(),
        )
        .unwrap();
        assert!(same.view()["comparison"]
            .as_str()
            .unwrap()
            .starts_with("identical"));
    }
}
#[test]
fn connector_git_partial_missing_noncommit_invalid_and_corruption() {
    let r = Repo::new("sha1");
    let missing = "0".repeat(40);
    let partial = read(
        &r.root,
        Path::new("literal [*].txt"),
        r.id("at"),
        Some(&missing),
        &Repo::control(),
    )
    .unwrap();
    assert_eq!(partial.view()["status"], "partial");
    let wrong = read(
        &r.root,
        Path::new("literal [*].txt"),
        r.id("old"),
        None,
        &Repo::control(),
    )
    .unwrap();
    assert_eq!(wrong.view()["status"], "gaps-only");
    for id in [
        "HEAD",
        "--help",
        "0123",
        " ABC",
        "A123",
        &format!("{}^", r.id("at")),
    ] {
        assert!(read(
            &r.root,
            Path::new("literal [*].txt"),
            id,
            None,
            &Repo::control()
        )
        .is_err());
    }
    let original = r.id("new");
    let alternate = r.vector["objects"]
        .as_array()
        .unwrap()
        .iter()
        .find(|o| o["oid"] == r.id("old"))
        .unwrap();
    fs::write(
        r.root
            .join(".git/objects")
            .join(&original[..2])
            .join(&original[2..]),
        unhex(alternate["compressed"].as_str().unwrap()),
    )
    .unwrap();
    let corrupt = read(
        &r.root,
        Path::new("literal [*].txt"),
        r.id("at"),
        None,
        &Repo::control(),
    )
    .unwrap();
    assert_eq!(corrupt.view()["status"], "gaps-only");
}
#[test]
fn connector_git_abort_after_completed_side_and_changed_association() {
    let r = Repo::new("sha1");
    let c = Repo::control();
    let result = read_with(
        &r.root,
        Path::new("literal [*].txt"),
        r.id("at"),
        Some(r.id("since")),
        &c,
        |stage| {
            if stage == "after_at" {
                c.cancel.store(true, Ordering::SeqCst);
            }
            Ok(())
        },
    );
    assert_eq!(result.err().unwrap().kind, "cancelled");
    let c = Repo::control();
    let e = read_with(
        &r.root,
        Path::new("literal [*].txt"),
        r.id("at"),
        None,
        &c,
        |stage| {
            if stage == "before_publish" {
                fs::write(r.root.join(".git/HEAD"), b"ref: refs/heads/changed\n").unwrap();
            }
            Ok(())
        },
    )
    .err()
    .unwrap();
    assert_eq!(e.kind, "association_changed");
}
#[test]
fn connector_git_linked_backlink_and_layout_refusals() {
    use std::os::unix::fs::symlink;
    let r = Repo::new("sha1");
    let linked = r.root.join("linked");
    fs::create_dir(&linked).unwrap();
    let admin = r.root.join(".git/worktrees/fixture");
    fs::create_dir_all(&admin).unwrap();
    fs::write(
        linked.join(".git"),
        format!("gitdir: {}\n", admin.display()),
    )
    .unwrap();
    fs::write(
        admin.join("gitdir"),
        format!("{}\n", linked.join(".git").display()),
    )
    .unwrap();
    fs::write(admin.join("commondir"), b"../..\n").unwrap();
    fs::write(admin.join("HEAD"), b"ref: refs/heads/fixture\n").unwrap();
    assert!(read(
        &linked,
        Path::new("literal [*].txt"),
        r.id("at"),
        None,
        &Repo::control()
    )
    .unwrap()
    .at
    .is_ok());
    fs::write(admin.join("gitdir"), b"/wrong/backlink\n").unwrap();
    assert!(read(
        &linked,
        Path::new("literal [*].txt"),
        r.id("at"),
        None,
        &Repo::control()
    )
    .is_err());
    let sub = r.root.join("sub");
    fs::create_dir(&sub).unwrap();
    assert!(read(&sub, Path::new("file"), r.id("at"), None, &Repo::control()).is_err());
    fs::create_dir_all(r.root.join(".git/objects/info")).unwrap();
    fs::write(r.root.join(".git/objects/info/alternates"), b"/outside\n").unwrap();
    assert!(read(
        &r.root,
        Path::new("literal [*].txt"),
        r.id("at"),
        None,
        &Repo::control()
    )
    .is_err());
    fs::remove_file(r.root.join(".git/objects/info/alternates")).unwrap();
    symlink("/outside", r.root.join(".git/objects/symlink")).unwrap();
    assert!(read(
        &r.root,
        Path::new("literal [*].txt"),
        r.id("at"),
        None,
        &Repo::control()
    )
    .is_err());
}

#[test]
fn connector_git_hostile_configuration_promised_miss_and_transport_sentinels() {
    use std::io::Write;
    use std::os::unix::fs::PermissionsExt;
    let r = Repo::new("sha1");
    let marker = r.root.join("helper-was-run");
    let script = r.root.join("hostile-helper");
    fs::write(
        &script,
        format!("#!/bin/sh\necho forbidden > '{}'\n", marker.display()),
    )
    .unwrap();
    fs::set_permissions(&script, fs::Permissions::from_mode(0o700)).unwrap();
    let listener = std::net::TcpListener::bind("127.0.0.1:0").unwrap();
    listener.set_nonblocking(true).unwrap();
    let port = listener.local_addr().unwrap().port();
    let mut config = fs::OpenOptions::new()
        .append(true)
        .open(r.root.join(".git/config"))
        .unwrap();
    write!(config,"[remote \"origin\"]\nurl = http://127.0.0.1:{port}/missing\npromisor = true\npartialclonefilter = blob:none\n[credential]\nhelper = {}\n[core]\nsshCommand = {}\n[filter \"hostile\"]\nsmudge = {}\nclean = {}\n[alias]\ncat-file = !{}\n[include]\npath = {}\n",script.display(),script.display(),script.display(),script.display(),script.display(),r.root.join("hostile-include").display()).unwrap();
    fs::write(
        r.root.join("hostile-include"),
        format!(
            "[core]\nfsmonitor = {}\n[diff \"hostile\"]\ntextconv = {}\n",
            script.display(),
            script.display()
        ),
    )
    .unwrap();
    fs::write(
        r.root.join(".gitattributes"),
        b"* filter=hostile diff=hostile\n",
    )
    .unwrap();
    fs::create_dir(r.root.join(".git/hooks")).unwrap();
    fs::copy(&script, r.root.join(".git/hooks/post-checkout")).unwrap();
    fs::create_dir(r.root.join(".git/objects/pack")).unwrap();
    fs::write(r.root.join(".git/objects/pack/fixture.promisor"), b"").unwrap();
    fs::create_dir_all(r.root.join(".git/refs/replace")).unwrap();
    fs::write(
        r.root.join(".git/refs/replace").join(r.id("at")),
        format!("{}\n", r.id("since")),
    )
    .unwrap();
    let before = snapshot(&r.root);
    let c = Repo::control();
    let result = read(
        &r.root,
        Path::new("literal [*].txt"),
        r.id("at"),
        Some(&"0".repeat(40)),
        &c,
    )
    .unwrap();
    assert_eq!(result.view()["status"], "partial");
    assert_eq!(result.at.unwrap().bytes, b"new\n\n");
    assert!(!marker.exists());
    assert!(matches!(listener.accept(),Err(e) if e.kind()==std::io::ErrorKind::WouldBlock));
    assert_eq!(snapshot(&r.root), before);
    let a = Association::open(&r.root, Path::new("literal [*].txt"), &Repo::control()).unwrap();
    let e = Engine::create(&a.objects, "sha1", &Repo::control()).unwrap();
    let helper = e.helper.clone();
    assert!(!fs::read_to_string(helper.join("config"))
        .unwrap()
        .contains("remote"));
    drop(e);
    assert!(!helper.exists());
    assert_eq!(snapshot(&r.root), before);
}
#[test]
fn connector_git_supervisor_caps_deadline_cancellation_and_cleanup() {
    use std::os::unix::fs::PermissionsExt;
    let r = Repo::new("sha1");
    let a = Association::open(&r.root, Path::new("literal [*].txt"), &Repo::control()).unwrap();
    let mut e = Engine::create(&a.objects, "sha1", &Repo::control()).unwrap();
    let fake = r.root.join("supervisor-fixture");
    fs::write(&fake, b"#!/bin/sh\nprintf 'oversized output'\n").unwrap();
    fs::set_permissions(&fake, fs::Permissions::from_mode(0o700)).unwrap();
    e.executable = fake.clone();
    let failure = e
        .run(&a.objects, &[], b"", 3, &Repo::control())
        .unwrap_err();
    assert_eq!(failure.kind, "limit");
    assert!(!failure.whole);
    fs::write(&fake, b"#!/bin/sh\nwhile :; do :; done\n").unwrap();
    let mut c = Repo::control();
    c.deadline = std::time::Instant::now() + std::time::Duration::from_millis(40);
    let failure = e.run(&a.objects, &[], b"", 3, &c).unwrap_err();
    assert_eq!(failure.kind, "deadline");
    assert!(failure.whole);
    let c = Repo::control();
    c.cancel.store(true, Ordering::SeqCst);
    assert_eq!(
        e.run(&a.objects, &[], b"", 3, &c).unwrap_err().kind,
        "cancelled"
    );
    e.executable = r.root.join("absent-git");
    assert!(
        e.run(&a.objects, &[], b"", 3, &Repo::control())
            .unwrap_err()
            .whole
    );
}
#[test]
fn connector_git_unknown_format_and_side_budget() {
    let r = Repo::new("sha1");
    let c = Repo::control();
    let a = Association::open(&r.root, Path::new("literal [*].txt"), &c).unwrap();
    let e = Engine::create(&a.objects, "sha1", &c).unwrap();
    let mut budget = 8 * 1048576 - 1;
    assert_eq!(
        object(&e, &a, r.id("new"), "blob", &mut budget, &c)
            .unwrap_err()
            .kind,
        "limit"
    );
    for format in ["sha512", "unknown"] {
        let contents = format!(
            "[core]\nrepositoryformatversion=1\nbare=false\n[extensions]\nobjectformat={format}\n"
        );
        fs::write(r.root.join(".git/config"), contents).unwrap();
        assert!(
            Association::open(&r.root, Path::new("literal [*].txt"), &Repo::control()).is_err()
        );
    }
}
#[test]
fn connector_git_raw_tree_modes_encoding_and_payload_boundaries() {
    for format in ["sha1", "sha256"] {
        let r = Repo::new(format);
        for name in ["executable", "blob_max", "commit_max", "tree_max"] {
            let id = r.vector["cases"][name].as_str().unwrap();
            let result = read(
                &r.root,
                Path::new("literal [*].txt"),
                id,
                None,
                &Repo::control(),
            )
            .unwrap();
            assert!(result.at.is_ok(), "{format} {name}: {:?}", result.at.err());
        }
        for name in [
            "symlink",
            "gitlink",
            "duplicate",
            "truncated",
            "malformed",
            "blob_over",
            "commit_over",
            "tree_over",
            "nul",
            "encoding",
        ] {
            let id = r.vector["cases"][name].as_str().unwrap();
            let result = read(
                &r.root,
                Path::new("literal [*].txt"),
                r.id("at"),
                Some(id),
                &Repo::control(),
            )
            .unwrap();
            assert_eq!(result.view()["status"], "partial", "{format} {name}");
            assert!(result.at.is_ok());
            assert!(result.since.unwrap().is_err(), "{name}");
        }
        for (name, path) in [
            ("unicode", PathBuf::from("é.txt")),
            ("nonutf8", {
                use std::os::unix::ffi::OsStringExt;
                PathBuf::from(std::ffi::OsString::from_vec(b"raw-\xff".to_vec()))
            }),
        ] {
            let id = r.vector["cases"][name].as_str().unwrap();
            let result = read(&r.root, &path, id, None, &Repo::control()).unwrap();
            assert_eq!(result.at.unwrap().bytes, b"new\n\n");
        }
    }
}
#[test]
fn connector_git_metadata_caps_unknown_extensions_bare_nested_and_depth() {
    let r = Repo::new("sha1");
    let config = r.root.join(".git/config");
    let original = fs::read(&config).unwrap();
    for data in [
        vec![b'x'; 1048577],
        b"[core]\nbare=true\n".to_vec(),
        b"[extensions]\nunrecognized=true\n".to_vec(),
    ] {
        fs::write(&config, data).unwrap();
        assert!(
            Association::open(&r.root, Path::new("literal [*].txt"), &Repo::control()).is_err()
        );
    }
    fs::write(config, original).unwrap();
    fs::create_dir(r.root.join("nested")).unwrap();
    fs::create_dir(r.root.join("nested/.git")).unwrap();
    assert!(Association::open(&r.root, Path::new("nested/file"), &Repo::control()).is_err());
    let mut deep = r.root.join(".git/objects");
    for _ in 0..130 {
        deep = deep.join("x");
        fs::create_dir(&deep).unwrap();
    }
    assert_eq!(
        Association::open(&r.root, Path::new("literal [*].txt"), &Repo::control())
            .err()
            .unwrap()
            .kind,
        "capability"
    );
}
#[test]
fn connector_git_supervised_framing_hash_stderr_and_child_reap() {
    use std::os::unix::fs::PermissionsExt;
    let r = Repo::new("sha1");
    let a = Association::open(&r.root, Path::new("literal [*].txt"), &Repo::control()).unwrap();
    let mut e = Engine::create(&a.objects, "sha1", &Repo::control()).unwrap();
    let fake = r.root.join("fixed-test-executable");
    fs::write(&fake, b"#!/bin/sh\nexit 129\n").unwrap();
    fs::set_permissions(&fake, fs::Permissions::from_mode(0o700)).unwrap();
    e.executable = fake.clone();
    assert_eq!(
        e.run(&a.objects, &[], b"", 20, &Repo::control())
            .unwrap_err()
            .kind,
        "command"
    );
    for (payload, expected) in [
        (format!("{} blob 5\\nnew\\n", r.id("new")), "framing"),
        (
            format!("{} blob 5\\nnew\\n\\n\\n", r.id("new")),
            "integrity",
        ),
    ] {
        fs::write(&fake,format!("#!/bin/sh\n/bin/cat >/dev/null\nfor arg do if [ \"$arg\" = hash-object ]; then printf '{}\\n'; exit; fi; done\nprintf '{}'\n","0".repeat(40),payload)).unwrap();
        assert_eq!(
            object(&e, &a, r.id("new"), "blob", &mut 0, &Repo::control())
                .unwrap_err()
                .kind,
            expected
        );
    }
    fs::write(
        &fake,
        b"#!/bin/sh\ni=0; while [ $i -lt 17000 ]; do printf x >&2; i=$((i+1)); done\n",
    )
    .unwrap();
    assert_eq!(
        e.run(&a.objects, &[], b"", 20, &Repo::control())
            .unwrap_err()
            .kind,
        "limit"
    );
    let pidfile = r.root.join("fixture-pid");
    fs::write(
        &fake,
        format!(
            "#!/bin/sh\nprintf '%s' $$ > '{}'\nwhile :; do :; done\n",
            pidfile.display()
        ),
    )
    .unwrap();
    let mut c = Repo::control();
    c.deadline = std::time::Instant::now() + std::time::Duration::from_millis(50);
    assert_eq!(
        e.run(&a.objects, &[], &vec![b'x'; 1048576], 20, &c)
            .unwrap_err()
            .kind,
        "deadline"
    );
    let pid = fs::read_to_string(pidfile).unwrap().parse::<i32>().unwrap();
    assert_eq!(unsafe { libc::kill(pid, 0) }, -1);
    assert_eq!(
        std::io::Error::last_os_error().raw_os_error(),
        Some(libc::ESRCH)
    );
}
#[test]
fn connector_git_actual_inherited_environment_is_not_authority() {
    if std::env::var_os("CGP_ENVIRONMENT_TEST_CHILD").is_some() {
        let r=Repo::new("sha1");
        let result=read(&r.root,Path::new("literal [*].txt"),r.id("at"),None,&Repo::control()).unwrap();
        assert_eq!(result.at.unwrap().bytes,b"new\n\n");return;
    }
    let output=std::process::Command::new(std::env::current_exe().unwrap())
        .args(["--exact","connector_git::tests::connector_git_actual_inherited_environment_is_not_authority"])
        .env("CGP_ENVIRONMENT_TEST_CHILD","1")
        .env("GIT_CONFIG_COUNT","1").env("GIT_CONFIG_KEY_0","core.repositoryformatversion").env("GIT_CONFIG_VALUE_0","999")
        .env("GIT_DIR","/unavailable-injected-repository").env("GIT_WORK_TREE","/unavailable-injected-worktree")
        .env("GIT_OBJECT_DIRECTORY","/unavailable-injected-objects").env("GIT_ALTERNATE_OBJECT_DIRECTORIES","/unavailable-alternates")
        .env("GIT_EXEC_PATH","/unavailable-injected-helpers").env("GIT_CONFIG_GLOBAL","/unavailable-injected-config")
        .output().unwrap();
    assert!(output.status.success(),"sanitized child failed: {}",String::from_utf8_lossy(&output.stderr));
}
