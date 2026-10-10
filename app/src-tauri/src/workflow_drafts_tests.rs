//! Draft workspace checks: D-2 observation and hygiene, §5.1 states, D-3
//! attribution, D-4 transitions, TT-3 composer sources and TT-4 pointers.
use super::*;
use std::collections::BTreeMap;

struct Scratch(PathBuf);
impl Scratch {
    fn new() -> Self {
        let p = fs::canonicalize(std::env::temp_dir())
            .unwrap()
            .join(crate::util::opaque_id("chirality-drafts-").unwrap());
        fs::create_dir(&p).unwrap();
        Self(p)
    }
    fn owner(&self) -> LibraryOwner {
        let mut owner = LibraryOwner::open(self.0.clone(), "project", "fixture-project").unwrap();
        owner.attach_app_kept_bases(&self.app_data()).unwrap();
        owner
    }
    fn app_data(&self) -> PathBuf {
        self.0.join("app-data")
    }
    fn draft(&self, name: &str) -> PathBuf {
        self.0.join(DRAFTS).join(name)
    }
    fn put(&self, name: &str, body: &str) -> PathBuf {
        let p = self.draft(name);
        fs::create_dir_all(&p).unwrap();
        fs::write(p.join("WORKFLOW.md"), format!("---\nname: {name}\n---\n# Method\n{body}\n")).unwrap();
        fs::write(p.join("notes.txt"), b"notes\n").unwrap();
        p
    }
}
impl Drop for Scratch {
    fn drop(&mut self) {
        let _ = fs::remove_dir_all(&self.0);
    }
}
fn none() -> Value {
    json!([])
}
fn observe(owner: &LibraryOwner, previous: Option<&[ObservedDraft]>, items: &Value, app_made: &BTreeMap<String, String>) -> DraftObservation {
    owner.observe_drafts(previous, &Attribution { native_items: items, app_made }, &|_| None)
}
fn row<'a>(o: &'a DraftObservation, name: &str) -> &'a Value {
    o.drafts.iter().find(|d| d["name"] == name).unwrap_or_else(|| panic!("{name} not listed: {:?}", o.drafts))
}

#[test]
fn a_written_draft_is_listed_with_content_identity_and_no_invented_attribution_or_base() {
    let s = Scratch::new();
    s.put("load-check", "Check loads.");
    let o = observe(&s.owner(), None, &none(), &BTreeMap::new());
    let d = row(&o, "load-check");
    assert_eq!(d["state"], "draft");
    assert_eq!(d["fileCount"], 2);
    assert_eq!(d["content"]["method"], SNAPSHOT_METHOD);
    assert_eq!(d["content"]["value"], Snapshot::capture(&s.draft("load-check")).unwrap().revision());
    assert!(d["schemaLimit"].is_null(), "draft_reference conforms to WR: {}", d["schemaLimit"]);
    assert_eq!(d["reference"]["base_recorded_by"], "none");
    assert!(d["base"].is_null() && d["baseLimit"].as_str().unwrap().contains("U-WR-12"));
    // D-3: no supplier item and no App action: "not observed", nothing inferred.
    assert_eq!(d["attribution"], json!({"kind":"not observed"}));
    assert!(d["tryLimit"].is_null() && d["reviewLimit"].is_null());
    assert!(o.transitions.is_empty(), "the first observation is a baseline");
    assert!(d["standing"].as_str().unwrap().contains("not a registered workflow"));
}

#[test]
fn hygiene_refusals_list_the_draft_not_valid_with_its_finding() {
    let s = Scratch::new();
    let os = s.put("os-file", "x");
    fs::write(os.join(".DS_Store"), b"\0\x01").unwrap();
    let hidden = s.put("hidden-ok", "x");
    fs::write(hidden.join(".editorconfig"), b"root = true\n").unwrap();
    let renamed = s.put("folder-name", "x");
    fs::write(renamed.join("WORKFLOW.md"), "---\nname: other-name\n---\n# M\n").unwrap();
    let bad = s.draft("Bad_Name");
    fs::create_dir_all(&bad).unwrap();
    fs::write(bad.join("WORKFLOW.md"), "---\nname: Bad_Name\n---\n").unwrap();
    let missing = s.draft("no-method");
    fs::create_dir_all(&missing).unwrap();
    fs::write(missing.join("notes.txt"), b"n").unwrap();
    let latin = s.draft("not-utf8");
    fs::create_dir_all(&latin).unwrap();
    fs::write(latin.join("WORKFLOW.md"), b"---\nname: not-utf8\n---\n\xff\xfe").unwrap();
    let o = observe(&s.owner(), None, &none(), &BTreeMap::new());
    let code = |name: &str| row(&o, name)["reference"]["findings"][0]["code"].as_str().map(str::to_owned);
    assert_eq!(row(&o, "os-file")["state"], "not valid");
    assert_eq!(code("os-file").as_deref(), Some("HY-4 operating-system file"));
    assert_eq!(row(&o, "hidden-ok")["state"], "draft", "other hidden files are allowed (HY-4)");
    assert_eq!(code("folder-name").as_deref(), Some("HY-2 name"));
    assert_eq!(code("Bad_Name").as_deref(), Some("HY-2 name"));
    assert_eq!(code("no-method").as_deref(), Some("HY-1 no WORKFLOW.md"));
    assert_eq!(code("not-utf8").as_deref(), Some("HY-7 not UTF-8"));
    for name in ["os-file", "folder-name", "Bad_Name", "no-method", "not-utf8"] {
        let d = row(&o, name);
        assert_eq!(d["state"], "not valid", "{name}");
        assert!(d["reviewLimit"].as_str().unwrap().starts_with("cannot be reviewed for registration (DS-5)"), "{name}");
        assert!(d["schemaLimit"].is_null(), "{name}: {}", d["schemaLimit"]);
    }
    assert!(row(&o, "no-method")["reference"]["content"]["not_established"].is_string());
}

#[test]
fn the_size_bound_is_checked_before_any_file_is_read() {
    let s = Scratch::new();
    let big = s.put("too-many", "x");
    for i in 0..MAX_FILES {
        fs::write(big.join(format!("f{i:04}.txt")), b"x").unwrap();
    }
    let o = observe(&s.owner(), None, &none(), &BTreeMap::new());
    let d = row(&o, "too-many");
    assert_eq!(d["state"], "not valid");
    assert_eq!(d["reference"]["findings"][0]["code"], "HY-5 size bound");
    assert!(d["reference"]["content"]["not_established"].as_str().unwrap().starts_with("HY-5"));
    assert!(s.owner().draft_trial_sources("too-many").unwrap_err().contains("HY-5"));
}

#[cfg(unix)]
#[test]
fn links_are_never_followed_and_drafts_outside_the_library_are_refused() {
    use std::os::unix::fs::symlink;
    let s = Scratch::new();
    let outside = Scratch::new();
    let elsewhere = outside.put("elsewhere", "outside the library");
    // A draft entry that is a link to a folder outside the library.
    fs::create_dir_all(s.0.join(DRAFTS)).unwrap();
    symlink(&elsewhere, s.draft("linked")).unwrap();
    // A link inside an otherwise ordinary draft (HY-3).
    let inner = s.put("inner-link", "x");
    symlink(elsewhere.join("WORKFLOW.md"), inner.join("borrowed.md")).unwrap();
    let o = observe(&s.owner(), None, &none(), &BTreeMap::new());
    assert_eq!(row(&o, "linked")["state"], "not valid");
    assert_eq!(row(&o, "linked")["reference"]["findings"][0]["code"], "HY-3 non-regular entry");
    assert!(row(&o, "linked")["schemaLimit"].is_null());
    assert_eq!(row(&o, "inner-link")["state"], "not valid");
    assert_eq!(row(&o, "inner-link")["reference"]["findings"][0]["code"], "HY-3 non-regular entry");
    let owner = s.owner();
    for name in ["linked", "inner-link"] {
        assert!(owner.draft_trial_sources(name).is_err(), "{name} must not be tried");
    }
    // Names that would leave the drafts folder are not draft names.
    for name in ["../elsewhere", "a/b", "..", ""] {
        assert!(owner.draft_trial_sources(name).unwrap_err().contains("Not a draft name"), "{name}");
    }
    // A drafts folder that is itself a link lists nothing.
    let t = Scratch::new();
    fs::create_dir_all(t.0.join(".chirality")).unwrap();
    symlink(outside.0.join(DRAFTS), t.0.join(DRAFTS)).unwrap();
    let o = observe(&t.owner(), None, &none(), &BTreeMap::new());
    assert!(o.drafts.is_empty());
    assert!(o.limit.unwrap().contains("refused"));
    assert!(t.owner().draft_trial_sources("elsewhere").is_err());
}

#[test]
fn transitions_follow_observed_changes_with_truthful_attribution() {
    let s = Scratch::new();
    let owner = s.owner();
    let empty = BTreeMap::new();
    let base = observe(&owner, None, &none(), &empty);
    assert!(base.transitions.is_empty());
    let path = s.put("load-check", "first");
    let o1 = observe(&owner, Some(&base.observed), &none(), &empty);
    assert_eq!(o1.transitions.len(), 1);
    let t = &o1.transitions[0];
    assert_eq!((t["event"].as_str(), t["from"].as_str(), t["to"].as_str()), (Some("written"), Some("absent"), Some("draft")));
    assert_eq!(t["attribution"], json!({"kind":"not observed"}));
    // A supplier fileChange item naming a file in the folder attributes the change.
    fs::write(path.join("WORKFLOW.md"), "---\nname: load-check\n---\nsecond\n").unwrap();
    let items = json!([
        {"threadId":"T","turnId":"u","observedOrder":3,"native":{"id":"fc-1","type":"fileChange","status":"completed","changes":[{"path":path.join("WORKFLOW.md").display().to_string(),"kind":{"type":"update"},"diff":""}]}},
        {"threadId":"T","turnId":"u","observedOrder":4,"native":{"id":"fc-rel","type":"fileChange","changes":[{"path":"WORKFLOW.md","kind":{"type":"update"},"diff":""}]}},
        {"threadId":"T","turnId":"u","observedOrder":5,"native":{"id":"cmd","type":"commandExecution","command":path.display().to_string()}}
    ]);
    let o2 = observe(&owner, Some(&o1.observed), &items, &empty);
    assert_eq!(o2.transitions[0]["event"], "changed");
    assert_eq!(o2.transitions[0]["attribution"], json!({"kind":"file change item","thread":"T","item":"fc-1"}), "a relative path or a command is not attribution");
    // Content the App wrote itself reads "app action".
    let mut app = BTreeMap::new();
    let written = s.put("refined", "app copy");
    app.insert("refined".to_owned(), Snapshot::capture(&written).unwrap().revision().to_owned());
    let o3 = observe(&owner, Some(&o2.observed), &none(), &app);
    let t = o3.transitions.iter().find(|t| t["draft"]["name"] == "refined").unwrap();
    assert_eq!(t["attribution"], json!({"kind":"app action"}));
    fs::write(written.join("notes.txt"), b"edited by the person\n").unwrap();
    let o4 = observe(&owner, Some(&o3.observed), &none(), &app);
    assert_eq!(row(&o4, "refined")["attribution"], json!({"kind":"not observed"}), "edited after the App wrote it");
    fs::remove_dir_all(&path).unwrap();
    let o5 = observe(&owner, Some(&o4.observed), &none(), &app);
    let gone = o5.transitions.iter().find(|t| t["event"] == "removed").unwrap();
    assert_eq!((gone["draft"]["name"].as_str(), gone["to"].as_str()), (Some("load-check"), Some("removed")));
    for t in o1.transitions.iter().chain(&o2.transitions).chain(&o3.transitions).chain(&o5.transitions) {
        crate::workflow_workspace::wr_validate("draft_transition", t).unwrap();
        assert!(t.get("a15_record").is_none() && t["event"] != "registered", "observation never claims registration");
    }
}

#[test]
fn review_states_come_from_the_caller_and_never_from_files() {
    let s = Scratch::new();
    s.put("load-check", "x");
    let owner = s.owner();
    let empty = BTreeMap::new();
    let items = none();
    let attribution = Attribution { native_items: &items, app_made: &empty };
    let o = owner.observe_drafts(None, &attribution, &|n| (n == "load-check").then(|| "under review".to_owned()));
    assert_eq!(row(&o, "load-check")["state"], "under review");
    let o2 = owner.observe_drafts(Some(&o.observed), &attribution, &|_| Some("changed since review".to_owned()));
    assert_eq!(o2.transitions[0]["event"], "review stale");
    // A file claiming registration does not make the draft registered.
    fs::write(s.draft("load-check").join("REGISTERED"), b"registered: yes\n").unwrap();
    let o3 = observe(&owner, None, &none(), &empty);
    assert_eq!(row(&o3, "load-check")["state"], "draft");
}

#[test]
fn trial_sources_pre_fill_text_files_with_the_draft_reference_and_name_what_is_not_attached() {
    let s = Scratch::new();
    let path = s.put("load-check", "x");
    fs::create_dir_all(path.join("resources")).unwrap();
    fs::write(path.join("resources/checklist.md"), b"- one\n").unwrap();
    fs::write(path.join("diagram.bin"), [0u8, 1, 2, 3]).unwrap();
    let sources = s.owner().draft_trial_sources("load-check").unwrap();
    let names: Vec<String> = sources.selections.iter().map(|sel| sel.snapshot()["displayName"].as_str().unwrap().to_owned()).collect();
    assert_eq!(names, ["WORKFLOW.md (draft load-check)", "notes.txt (draft load-check)", "checklist.md (draft load-check)"], "WORKFLOW.md first, then UTF-8 path order");
    assert_eq!(sources.not_attached.len(), 1);
    assert_eq!(sources.not_attached[0]["path"], "diagram.bin");
    assert!(sources.not_attached[0]["reason"].as_str().unwrap().contains("AT-10"));
    let expected = Snapshot::capture(&path).unwrap();
    assert_eq!(sources.content, json!({"method":SNAPSHOT_METHOD,"value":expected.revision()}));
    assert_eq!(sources.key, json!({"draft_location":"project","draft_root":s.0.join(DRAFTS).display().to_string(),"name":"load-check"}));
    for sel in &sources.selections {
        let draft = &sel.snapshot()["draft"];
        assert_eq!(draft["standing"], "draft — not a registered workflow; this conversation is not a workflow run");
        assert_eq!(draft["content"], sources.content);
        assert!(draft.get("draft_root").is_none(), "the NIR supply record names no extra element");
        assert_eq!(sel.snapshot()["standing"], "selected; not sent");
        // The supply record a send would carry conforms to NIR with its draft element.
        let prepared = sel.prepare_for_source(&sel.native_path(), &crate::attachments::new_submission_ref().unwrap(), "2026-10-10T00:00:00Z").unwrap();
        assert_eq!(prepared.supply_record()["draft"]["name"], "load-check");
    }
    // A WORKFLOW.md that cannot go as text refuses the whole pre-fill.
    let big = s.put("too-long", "x");
    fs::write(big.join("WORKFLOW.md"), format!("---\nname: too-long\n---\n{}", "a".repeat(TEXT_FILE_BOUND))).unwrap();
    assert!(s.owner().draft_trial_sources("too-long").unwrap_err().contains("WORKFLOW.md cannot go as a text element"));
    assert!(s.owner().draft_trial_sources("absent").unwrap_err().contains("not found"));
}

#[test]
fn trial_pointers_survive_a_new_process_and_unreadable_ones_are_reported() {
    let s = Scratch::new();
    s.put("load-check", "x");
    let sources = s.owner().draft_trial_sources("load-check").unwrap();
    let mut store = TrialPointers::open(&s.app_data());
    assert!(store.for_draft(&sources.key).is_empty());
    let pointer = store.record(&sources.key, &sources.content, "thread-1").unwrap();
    assert_eq!(pointer["standing"], TRIAL_STANDING);
    assert!(pointer.get("workflow").is_none() && pointer.get("run").is_none(), "a pointer names no workflow identity or run");
    // A new process reads the pointer back from the App data folder.
    let reopened = TrialPointers::open(&s.app_data());
    assert_eq!(reopened.for_draft(&sources.key), vec![pointer.clone()]);
    assert!(reopened.limits().is_empty());
    // A damaged pointer is named, never silently dropped or rewritten.
    let dir = s.app_data().join(TRIAL_POINTERS);
    fs::write(dir.join("damaged.json"), b"{\"record_kind\":\"trial_pointer\"}").unwrap();
    let damaged = TrialPointers::open(&s.app_data());
    assert_eq!(damaged.for_draft(&sources.key).len(), 1);
    assert!(damaged.limits()[0].contains("damaged.json"));
    assert_eq!(fs::read(dir.join("damaged.json")).unwrap(), b"{\"record_kind\":\"trial_pointer\"}");
    // Without an App data folder a pointer is kept in memory only, and says so.
    let mut memory = TrialPointers::default();
    memory.record(&sources.key, &sources.content, "thread-2").unwrap();
    assert_eq!(memory.for_draft(&sources.key).len(), 1);
    assert!(memory.limits()[0].contains("process memory only"));
    // The schema refuses a pointer that names a workflow identity.
    let mut bad = pointer;
    bad["workflow"] = json!({"name":"load-check"});
    assert!(crate::workflow_workspace::wr_validate("trial_pointer", &bad).is_err());
}

#[test]
fn the_sixteen_mebibyte_bound_refuses_listing_trial_capture_and_review() {
    let s = Scratch::new();
    let big = s.put("too-big", "x");
    let used = fs::metadata(big.join("WORKFLOW.md")).unwrap().len() + fs::metadata(big.join("notes.txt")).unwrap().len();
    // One byte over the bound in total.
    fs::write(big.join("data.txt"), vec![b'a'; (MAX_BYTES - used + 1) as usize]).unwrap();
    let o = observe(&s.owner(), None, &none(), &BTreeMap::new());
    assert_eq!(row(&o, "too-big")["reference"]["findings"][0]["code"], "HY-5 size bound");
    assert!(s.owner().draft_trial_sources("too-big").unwrap_err().contains("HY-5"));
    // The capture's running budget refuses on its own, whatever the metadata said.
    assert!(Snapshot::capture(&big).unwrap_err().starts_with("HY-5"));
    let refused = s.owner().review_draft("too-big", "listed").err().unwrap();
    assert!(refused.starts_with("DS-5: HY-5"), "{refused}");
    // Exactly at the bound is within it.
    fs::write(big.join("data.txt"), vec![b'a'; (MAX_BYTES - used) as usize]).unwrap();
    assert!(Snapshot::capture(&big).is_ok());
    assert!(prescan(&big).is_ok());
}

#[test]
fn review_of_a_new_workflow_is_refused_as_ds6_when_the_draft_changed_since_listing() {
    let s = Scratch::new();
    let path = s.put("brand-new", "first");
    let owner = s.owner();
    let listed = owner.listed_draft_revision("brand-new").unwrap();
    assert!(owner.latest_registered("brand-new").unwrap().is_none(), "no prior revision in the slot");
    fs::write(path.join("notes.txt"), b"edited after listing\n").unwrap();
    let refused = owner.review_draft("brand-new", &listed).err().unwrap();
    assert!(refused.starts_with("DS-6"), "{refused}");
}

#[cfg(unix)]
#[test]
fn a_fifo_or_a_link_in_a_package_is_refused_without_blocking_or_following() {
    use std::os::unix::fs::symlink;
    let s = Scratch::new();
    let fifo_draft = s.put("with-fifo", "x");
    let fifo = std::ffi::CString::new(fifo_draft.join("pipe").to_str().unwrap()).unwrap();
    // SAFETY: a NUL-terminated path in this test's own scratch folder.
    assert_eq!(unsafe { libc::mkfifo(fifo.as_ptr(), 0o600) }, 0);
    let started = std::time::Instant::now();
    assert!(Snapshot::capture(&fifo_draft).unwrap_err().starts_with("HY-3"), "a FIFO is never read");
    let o = observe(&s.owner(), None, &none(), &BTreeMap::new());
    assert_eq!(row(&o, "with-fifo")["reference"]["findings"][0]["code"], "HY-3 non-regular entry");
    assert!(started.elapsed() < std::time::Duration::from_secs(5), "nothing blocked on the FIFO");
    // A file or folder that is a link is refused by the descriptor walk itself.
    let outside = Scratch::new();
    let target = outside.put("target", "outside bytes");
    let linked_file = s.put("linked-file", "x");
    symlink(target.join("WORKFLOW.md"), linked_file.join("borrowed.md")).unwrap();
    assert!(Snapshot::capture(&linked_file).unwrap_err().starts_with("HY-3"));
    let linked_dir = s.put("linked-dir", "x");
    symlink(&target, linked_dir.join("resources")).unwrap();
    assert!(Snapshot::capture(&linked_dir).unwrap_err().starts_with("HY-3"));
    // The package root itself is opened no-follow.
    symlink(&target, s.0.join("root-link")).unwrap();
    assert!(Snapshot::capture(&s.0.join("root-link")).is_err());
}

#[test]
fn pointer_listing_problems_are_reported_not_dropped() {
    let s = Scratch::new();
    let mut store = TrialPointers::open(&s.app_data());
    assert!(store.limits().is_empty());
    let key = json!({"draft_location":"project","draft_root":"/r","name":"n"});
    store.record(&key, &json!({"method":"m","value":"v"}), "thread").unwrap();
    // A pointer entry that is not a regular file is named in the limits.
    fs::create_dir(s.app_data().join(TRIAL_POINTERS).join("folder.json")).unwrap();
    let reopened = TrialPointers::open(&s.app_data());
    assert_eq!(reopened.for_draft(&key).len(), 1);
    assert!(reopened.limits().iter().any(|l| l.contains("folder.json")), "{:?}", reopened.limits());
}
