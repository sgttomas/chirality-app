//! Trial core checks (WR §17 steps 1–4): the shared composer and the trial
//! text (WR-VC-21), TX-7 folder labels and supply copies (CI-32), the TT-8
//! trial snapshot and its destination handling, and the TT-4 trial link store.
use super::*;
use crate::workflow_workspace::package_copy::{write_content_copy, BEFORE_PUBLISH};
use crate::workflow_workspace::{
    compose_run_text, files_folder, FidelityDifference, FilesFolderBasis, PreparedRunText, RunScope, Selection,
    SUPPLY_AREA,
};
use std::os::unix::fs::symlink;

struct Scratch(PathBuf);
impl Scratch {
    fn new() -> Self {
        let p = fs::canonicalize(std::env::temp_dir())
            .unwrap()
            .join(crate::util::opaque_id("chirality-trials-").unwrap());
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
    /// A draft with a text supporting file and a binary one.
    fn put(&self, name: &str, body: &str) -> PathBuf {
        let p = self.draft(name);
        fs::create_dir_all(p.join("resources")).unwrap();
        fs::write(p.join("WORKFLOW.md"), format!("---\nname: {name}\n---\n# Method\n{body}\n")).unwrap();
        fs::write(p.join("notes.txt"), b"notes\n").unwrap();
        fs::write(p.join("resources/table.bin"), [0u8, 159, 146, 150]).unwrap();
        p
    }
    fn listed(&self, name: &str) -> String {
        Snapshot::capture(&self.draft(name)).unwrap().revision().to_owned()
    }
    fn prepare(&self, name: &str) -> Result<PreparedTrial, String> {
        self.owner().prepare_trial(name, &self.listed(name), 1, Some(&self.0), None)
    }
}
impl Drop for Scratch {
    fn drop(&mut self) {
        let _ = fs::remove_dir_all(&self.0);
    }
}
fn entries(dir: &Path) -> Vec<String> {
    let mut v: Vec<String> = fs::read_dir(dir)
        .map(|d| d.filter_map(Result::ok).map(|e| e.file_name().to_string_lossy().into_owned()).collect())
        .unwrap_or_default();
    v.sort();
    v
}
fn scope(run: &str, store: &Path) -> RunScope {
    RunScope {
        run: run.into(),
        conversation: "thread-test".into(),
        home: "home-test".into(),
        generation: json!({"appSession":"session-test","home":"home-test","spawnCounter":1}),
        source_root: "fixture-project".into(),
        holding_library: "fixture-project".into(),
        selection_ref: "selection-test".into(),
        revision_store: store.to_path_buf(),
    }
}

// WR-VC-21 (AC-009, VER-007): the trial text, less its header, equals the run
// text composed after registering the same content into the target slot, apart
// from the run reference and the files line's folder; no chain line; nothing
// is recorded.
#[test]
fn trial_text_less_its_header_is_the_run_text_a_registered_run_of_the_same_content_receives() {
    let s = Scratch::new();
    s.put("load-check", "Check the loads.");
    let trial = s.prepare("load-check").unwrap();
    let text = &trial.text;
    let snapshot = Snapshot::capture(&s.draft("load-check")).unwrap();
    // The same bytes registered into the target slot (SP-2), held in the store.
    let store = s.0.join(".chirality/workflow-revisions/load-check/key/load-check");
    fs::create_dir_all(store.parent().unwrap()).unwrap();
    snapshot.publish_new(&store).unwrap();
    let identity = snapshot.identity("project", "fixture-project", "load-check", None).unwrap();
    let selection = Selection::synthetic_registered(snapshot.clone(), identity.clone()).unwrap();
    let files = files_folder(&snapshot, &identity, &store, &s.0, None).unwrap();
    assert_eq!(files.basis, FilesFolderBasis::ProjectRelative);
    let run = PreparedRunText::start(&selection, scope("run:workflow:fixture", &store), &files.label, None).unwrap();
    let expected = run
        .text()
        .replace("run run:workflow:fixture.", &format!("run {}.", text.reference()))
        .replace(&format!("folder \"{}\"", files.label), &format!("folder \"{}\"", text.snapshot_folder()));
    assert_eq!(text.run_text(), expected, "same composer, same content");
    // Line by line: only the start line (run reference) and the files line (folder) differ.
    let (trial_lines, run_lines): (Vec<_>, Vec<_>) = (text.run_text().lines().collect(), run.text().lines().collect());
    assert_eq!(trial_lines.len(), run_lines.len());
    let differing: Vec<usize> = (0..run_lines.len()).filter(|&i| trial_lines[i] != run_lines[i]).collect();
    assert_eq!(differing, vec![0, 2], "start line and files line only");
    assert!(run_lines[2].starts_with("[Chirality] Other files of this revision, in the folder"));
    assert!(text.run_text().contains("notes.txt (sha256 ") && text.run_text().contains("resources/table.bin (sha256 "));
    assert!(!text.text().contains("Previous workflow run ended"), "no chain line");
    // The header (TT-3, WR-TRIAL-1) and the whole text.
    let rev12 = &snapshot.revision()[..12];
    assert_eq!(
        text.header(),
        format!("[Chirality] Workflow trial 1 of draft project:load-check, content {rev12} (trial {}). Not registered; not a workflow run. The lines below are the run text a registered run of this exact content would receive, except its run reference and the folder named for other files.", text.reference())
    );
    assert_eq!(text.text(), format!("{}\n{}", text.header(), text.run_text()));
    assert!(text.text().ends_with(&format!("<<<chirality-workflow load-check@{rev12} end>>>")));
    assert_eq!(text.identity(), crate::role_supply::content(text.text().as_bytes()));
    assert_eq!(text.bytes(), text.text().len());
    assert!(valid_trial_reference(text.reference()));
    assert_eq!(
        text.snapshot_folder(),
        format!(".chirality/workflow-trials/load-check/{}/load-check", storage::key(snapshot.revision()))
    );
    // TT-2: preparing a trial opens no run and writes no run_text, supply_check or record.
    assert!(!s.0.join(".chirality/records").exists(), "nothing recorded for a trial");
    assert!(TrialLinks::open(&s.app_data()).for_draft(&trial.key).is_empty(), "no link before a send");
    assert_eq!(trial.content, json!({"method":SNAPSHOT_METHOD,"value":snapshot.revision()}));
    // The composer refuses an absolute or empty folder label (TX-7).
    for bad in ["/Users/someone/project/.chirality/x", "", "~", "~/../x", "a/../b", "folder\"quoted"] {
        assert!(compose_run_text(&identity, &snapshot, "run:x", bad).is_err(), "{bad:?}");
    }
    assert!(compose_run_text(&identity, &snapshot, "run:x", "~/.chirality/workflow-revisions/x").is_ok());
}

#[test]
fn a_draft_with_a_refusing_finding_or_changed_while_read_is_not_tried_and_nothing_is_composed() {
    let s = Scratch::new();
    let os = s.put("os-file", "x");
    fs::write(os.join(".DS_Store"), b"\0").unwrap();
    assert!(s.owner().prepare_trial("os-file", "as listed", 1, Some(&s.0), None).unwrap_err().starts_with("cannot be tried: HY-4"));
    let renamed = s.put("renamed", "x");
    fs::write(renamed.join("WORKFLOW.md"), "---\nname: other\n---\n").unwrap();
    assert!(s.owner().prepare_trial("renamed", "as listed", 1, Some(&s.0), None).unwrap_err().contains("HY-2"));
    let linked = s.put("linked", "x");
    symlink("/etc/hosts", linked.join("borrowed.txt")).unwrap();
    assert!(s.owner().prepare_trial("linked", "as listed", 1, Some(&s.0), None).unwrap_err().contains("HY-3"), "a link in the draft is never followed");
    // Listed identity no longer current.
    s.put("load-check", "first");
    let listed = s.listed("load-check");
    fs::write(s.draft("load-check").join("notes.txt"), b"edited\n").unwrap();
    assert_eq!(
        s.owner().prepare_trial("load-check", &listed, 1, Some(&s.0), None).unwrap_err(),
        "the draft changed while it was read; try again"
    );
    // Changed while the snapshot was being written: refused after the copy.
    let listed = s.listed("load-check");
    let draft = s.draft("load-check");
    BEFORE_PUBLISH.with(|h| *h.borrow_mut() = Some(Box::new(move |_| fs::write(draft.join("notes.txt"), b"during\n").unwrap())));
    assert_eq!(
        s.owner().prepare_trial("load-check", &listed, 1, Some(&s.0), None).unwrap_err(),
        "the draft changed while it was read; try again"
    );
    // A folder outside the project and the home folder cannot be named.
    s.put("elsewhere", "x");
    let other = Scratch::new();
    let refused = s.owner().prepare_trial("elsewhere", &s.listed("elsewhere"), 1, Some(&other.0), None).unwrap_err();
    assert!(refused.contains("inside neither the opened project nor the home folder"), "{refused}");
    assert!(!s.0.join(".chirality/workflow-trials/elsewhere").exists(), "nothing written before the label is known");
    // The home folder names a user-library snapshot `~/`-relative.
    let in_home = s.owner().prepare_trial("elsewhere", &s.listed("elsewhere"), 3, Some(&other.0), Some(&s.0)).unwrap();
    assert!(in_home.text.snapshot_folder().starts_with("~/.chirality/workflow-trials/elsewhere/"));
    assert!(in_home.text.header().starts_with("[Chirality] Workflow trial 3 of draft project:elsewhere"));
}

// TT-8: content-addressed, reused when identical, refused (never replaced) when
// it holds other bytes, recreated after the person deletes it.
#[test]
fn trial_snapshots_are_content_addressed_reused_never_replaced_and_recreated_after_deletion() {
    let s = Scratch::new();
    s.put("load-check", "x");
    let first = s.prepare("load-check").unwrap();
    assert!(!first.snapshot.reused);
    let folder = first.snapshot.path.clone();
    assert_eq!(Snapshot::capture(&folder).unwrap().files(), Snapshot::capture(&s.draft("load-check")).unwrap().files());
    let second = s.prepare("load-check").unwrap();
    assert!(second.snapshot.reused && second.snapshot.path == folder, "trials of one version share it");
    assert_ne!(first.text.reference(), second.text.reference(), "each trial has its own reference");
    let owner = s.owner();
    let revision = s.listed("load-check");
    assert_eq!(owner.trial_snapshot_standing("load-check", &revision), CopyStanding::Current);
    // An agent writes in the snapshot (D3): standing says so; the next Try refuses and changes nothing.
    fs::write(folder.join("notes.txt"), b"agent wrote here\n").unwrap();
    assert!(matches!(owner.trial_snapshot_standing("load-check", &revision), CopyStanding::Changed(_)));
    let refused = s.prepare("load-check").unwrap_err();
    assert!(refused.contains("holds other bytes") && refused.ends_with("not replaced"), "{refused}");
    assert_eq!(fs::read(folder.join("notes.txt")).unwrap(), b"agent wrote here\n", "never rewritten");
    // Deleted by the person: the trial's bytes are not available; Try again recreates it.
    fs::remove_dir_all(&folder).unwrap();
    assert!(matches!(owner.trial_snapshot_standing("load-check", &revision), CopyStanding::NotAvailable(_)));
    let again = s.prepare("load-check").unwrap();
    assert!(!again.snapshot.reused && Snapshot::capture(&folder).unwrap().revision() == revision);
    assert!(entries(folder.parent().unwrap()).iter().all(|e| !e.starts_with(".staging-")), "no staging left");
}

// Destination handling of the shared writer (supply copies and trial
// snapshots): a link at or above the destination is never followed, a
// non-folder or a folder with a FIFO or other bytes is refused, and a link
// planted in the race before publication is refused by the exclusive rename.
#[test]
fn copy_destinations_refuse_links_fifos_and_other_bytes_without_following_or_blocking() {
    let s = Scratch::new();
    s.put("load-check", "x");
    let snapshot = Snapshot::capture(&s.draft("load-check")).unwrap();
    let outside = Scratch::new();
    let dest = |n: &str| s.0.join(".chirality/workflow-supply").join(n).join("key").join(n);
    // A link already at the destination.
    let d = dest("pre-link");
    fs::create_dir_all(d.parent().unwrap()).unwrap();
    symlink(&outside.0, &d).unwrap();
    assert!(write_content_copy(&snapshot, &d).unwrap_err().contains("symlink"));
    assert!(entries(&outside.0).is_empty(), "nothing written through the link");
    // A link planted after the checks, just before publication.
    let d = dest("race-link");
    let target = outside.0.clone();
    BEFORE_PUBLISH.with(|h| *h.borrow_mut() = Some(Box::new(move |dest: &Path| symlink(&target, dest).unwrap())));
    let raced = write_content_copy(&snapshot, &d).unwrap_err();
    assert!(raced.contains("is a symbolic link; it is not followed"), "{raced}");
    assert!(entries(&outside.0).is_empty(), "nothing written through the planted link");
    assert!(entries(d.parent().unwrap()).iter().all(|e| !e.starts_with(".staging-")), "staging removed");
    assert!(fs::symlink_metadata(&d).unwrap().file_type().is_symlink(), "the planted link is left as it is");
    // An ancestor that is a link.
    let area = s.0.join(".chirality/workflow-trials");
    symlink(&outside.0, &area).unwrap();
    assert!(write_content_copy(&snapshot, &area.join("x/key/x")).unwrap_err().contains("symlink"));
    assert!(entries(&outside.0).is_empty());
    // A regular file at the destination.
    let d = dest("a-file");
    fs::create_dir_all(d.parent().unwrap()).unwrap();
    fs::write(&d, b"x").unwrap();
    assert!(write_content_copy(&snapshot, &d).unwrap_err().contains("is not a folder"));
    // An existing folder holding a FIFO: refused without blocking.
    let d = dest("fifo");
    fs::create_dir_all(&d).unwrap();
    let fifo = std::ffi::CString::new(d.join("pipe").to_str().unwrap()).unwrap();
    // SAFETY: a NUL-terminated path in this test's own scratch folder.
    assert_eq!(unsafe { libc::mkfifo(fifo.as_ptr(), 0o600) }, 0);
    let started = std::time::Instant::now();
    assert!(write_content_copy(&snapshot, &d).unwrap_err().contains("cannot be read as a package"));
    assert!(started.elapsed() < std::time::Duration::from_secs(5));
    // An existing folder with a subset of the files is "other bytes".
    let d = dest("partial");
    fs::create_dir_all(&d).unwrap();
    fs::write(d.join("WORKFLOW.md"), snapshot.files()["WORKFLOW.md"].clone()).unwrap();
    assert!(write_content_copy(&snapshot, &d).unwrap_err().contains("holds other bytes"));
    // A concurrent writer of the same content wins the race: reused, not an error.
    let d = dest("same");
    let other = snapshot.clone();
    BEFORE_PUBLISH.with(|h| {
        *h.borrow_mut() = Some(Box::new(move |dest: &Path| {
            fs::create_dir_all(dest.parent().unwrap()).unwrap();
            other.publish_new(dest).unwrap();
        }))
    });
    let copy = write_content_copy(&snapshot, &d).unwrap();
    assert!(copy.reused);
    // An EMPTY folder planted after the checks: the exclusive rename refuses
    // it (a plain rename would replace it), and the empty folder is no package.
    let d = dest("race-empty");
    BEFORE_PUBLISH.with(|h| *h.borrow_mut() = Some(Box::new(move |dest: &Path| fs::create_dir(dest).unwrap())));
    let refused = write_content_copy(&snapshot, &d).unwrap_err();
    assert!(refused.contains("cannot be read as a package") && refused.ends_with("not replaced"), "{refused}");
    assert!(entries(&d).is_empty(), "the planted folder is left as it is");
    // A staging folder left by an interrupted (crashed) write is reported, left alone.
    let d = dest("crashed");
    fs::create_dir_all(d.parent().unwrap().join(".staging-old")).unwrap();
    let copy = write_content_copy(&snapshot, &d).unwrap();
    assert!(copy.leftovers.len() == 1 && copy.leftovers[0].contains(".staging-old"), "{:?}", copy.leftovers);
    assert!(d.parent().unwrap().join(".staging-old").is_dir());
    // Bytes that change between the write and the naming are caught by the
    // recomputation: refused, and the folder is left as it is.
    let d = dest("tampered");
    BEFORE_PUBLISH.with(|h| {
        *h.borrow_mut() = Some(Box::new(move |dest: &Path| {
            let parent = dest.parent().unwrap();
            let staging = fs::read_dir(parent).unwrap().filter_map(Result::ok).find(|e| e.file_name().to_string_lossy().starts_with(".staging-")).unwrap();
            fs::write(staging.path().join("notes.txt"), b"swapped\n").unwrap();
        }))
    });
    let refused = write_content_copy(&snapshot, &d).unwrap_err();
    assert!(refused.contains("does not recompute"), "{refused}");
    assert_eq!(fs::read(d.join("notes.txt")).unwrap(), b"swapped\n", "never removed or rewritten by the App");
}

// TX-7 (CI-32): (a) project-relative, (b) `~/`-relative, (c) a supply copy in
// the project, written once, reused, recreated after deletion; refused with
// the cause when it cannot be written; nothing for a WORKFLOW.md-only package.
#[test]
fn files_folder_names_project_or_home_relative_folders_or_a_supply_copy_and_refuses_otherwise() {
    let project = Scratch::new();
    let home = Scratch::new();
    let elsewhere = Scratch::new();
    let package = |root: &Path| -> (PathBuf, Snapshot) {
        let p = root.join("holding/load-check");
        fs::create_dir_all(&p).unwrap();
        fs::write(p.join("WORKFLOW.md"), "---\nname: load-check\n---\n# M\n").unwrap();
        fs::write(p.join("REVIEW-NOTES.md"), "notes\n").unwrap();
        let snapshot = Snapshot::capture(&p).unwrap();
        (p, snapshot)
    };
    let (in_project, snapshot) = package(&project.0);
    let identity = snapshot.identity("bundled", "release", "load-check", None).unwrap();
    let a = files_folder(&snapshot, &identity, &in_project, &project.0, Some(&home.0)).unwrap();
    assert_eq!((a.label.as_str(), &a.basis), ("holding/load-check", &FilesFolderBasis::ProjectRelative));
    let (in_home, _) = package(&home.0);
    let b = files_folder(&snapshot, &identity, &in_home, &project.0, Some(&home.0)).unwrap();
    assert_eq!((b.label.as_str(), &b.basis), ("~/holding/load-check", &FilesFolderBasis::HomeRelative));
    let (outside, _) = package(&elsewhere.0);
    let c = files_folder(&snapshot, &identity, &outside, &project.0, Some(&home.0)).unwrap();
    let supply = format!(".chirality/{SUPPLY_AREA}/load-check/{}/load-check", storage::key(snapshot.revision()));
    assert_eq!(c.label, supply);
    let FilesFolderBasis::SupplyCopy { path, reused: false } = &c.basis else { panic!("{c:?}") };
    assert_eq!(Snapshot::capture(path).unwrap().files(), snapshot.files());
    assert!(c.describe()["retention"].as_str().unwrap().contains("never rewritten or removed by the App"));
    let again = files_folder(&snapshot, &identity, &outside, &project.0, None).unwrap();
    assert!(matches!(again.basis, FilesFolderBasis::SupplyCopy { reused: true, .. }));
    // Deleted: the next run start recreates it.
    fs::remove_dir_all(path).unwrap();
    let recreated = files_folder(&snapshot, &identity, &outside, &project.0, None).unwrap();
    assert!(matches!(recreated.basis, FilesFolderBasis::SupplyCopy { reused: false, .. }));
    // Changed by someone else: refused, never rewritten.
    fs::write(path.join("REVIEW-NOTES.md"), "changed\n").unwrap();
    let refused = files_folder(&snapshot, &identity, &outside, &project.0, None).unwrap_err();
    assert!(refused.starts_with("other files of this revision could not be supplied:") && refused.contains("holds other bytes"), "{refused}");
    assert_eq!(fs::read(path.join("REVIEW-NOTES.md")).unwrap(), b"changed\n");
    // Cannot be written: the area is a file.
    let blocked = Scratch::new();
    fs::create_dir_all(blocked.0.join(".chirality")).unwrap();
    fs::write(blocked.0.join(".chirality").join(SUPPLY_AREA), b"not a folder").unwrap();
    let refused = files_folder(&snapshot, &identity, &outside, &blocked.0, None).unwrap_err();
    assert!(refused.starts_with("other files of this revision could not be supplied:"), "{refused}");
    // WORKFLOW.md only: no files line and nothing written, wherever it is held.
    let only = elsewhere.0.join("only/solo");
    fs::create_dir_all(&only).unwrap();
    fs::write(only.join("WORKFLOW.md"), "---\nname: solo\n---\n").unwrap();
    let solo = Snapshot::capture(&only).unwrap();
    let solo_id = solo.identity("bundled", "release", "solo", None).unwrap();
    let none = files_folder(&solo, &solo_id, &only, &blocked.0, None).unwrap();
    assert_eq!((none.label.as_str(), &none.basis), ("", &FilesFolderBasis::NoOtherFiles));
    // An identity that does not name these bytes is refused before anything is written.
    let other_id = solo.identity("bundled", "release", "load-check", None).unwrap();
    assert!(files_folder(&snapshot, &other_id, &outside, &project.0, None).is_err());
}

fn sent(kind: TrialKind) -> SentTrial {
    SentTrial {
        kind,
        authoring_conversation: "thread-authoring".into(),
        client_message: "workflow-trial-message:1".into(),
        turn: Some("turn-1".into()),
        clean_conversation: (kind == TrialKind::Clean).then(|| "thread-clean".into()),
    }
}

// TT-4: create-once links written on acknowledgment, surviving a new process,
// one per trial, listed per draft newest first with their observations.
#[test]
fn trial_links_are_create_once_survive_relaunch_and_list_per_draft_with_observations() {
    let s = Scratch::new();
    s.put("load-check", "x");
    let mut store = TrialLinks::open(&s.app_data());
    let first = s.prepare("load-check").unwrap();
    // An earlier attachment pointer for the same draft stays valid and listed as such.
    let earlier = store.record(&first.key, &json!({"method":SNAPSHOT_METHOD,"value":"older"}), "thread-0").unwrap();
    let link = store.record_sent(&first, &sent(TrialKind::Delegated)).unwrap();
    assert_eq!(link["standing"], LINK_STANDING);
    assert_eq!(link["conversation"], "thread-authoring");
    assert_eq!(link["trial"]["kind"], "delegated");
    assert!(link["trial"]["clean_conversation"].is_null());
    assert_eq!(link["trial"]["text_identity"], first.text.identity());
    assert!(link.get("workflow").is_none() && link.get("run").is_none(), "no workflow identity or run");
    let file = s.app_data().join(TRIAL_POINTERS).join(format!("trial-{}.json", first.text.reference().trim_start_matches("trial:")));
    assert!(file.is_file(), "named by the trial reference");
    // Retrying the same acknowledgment returns the same link; a different send is refused.
    assert_eq!(store.record_sent(&first, &sent(TrialKind::Delegated)).unwrap(), link);
    let mut other = sent(TrialKind::Delegated);
    other.authoring_conversation = "thread-elsewhere".into();
    assert!(store.record_sent(&first, &other).unwrap_err().contains("one link per trial"));
    assert_eq!(store.next_sequence(&first.key), 2);
    // A clean trial of the next version.
    fs::write(s.draft("load-check").join("notes.txt"), b"v2\n").unwrap();
    let second = s.owner().prepare_trial("load-check", &s.listed("load-check"), store.next_sequence(&first.key), Some(&s.0), None).unwrap();
    assert_eq!(second.text.sequence(), 2);
    let clean = store.record_sent(&second, &sent(TrialKind::Clean)).unwrap();
    assert_eq!((clean["conversation"].as_str(), clean["trial"]["clean_conversation"].as_str()), (Some("thread-clean"), Some("thread-clean")));
    let mut bad = sent(TrialKind::Clean);
    bad.clean_conversation = None;
    assert!(store.record_sent(&second, &bad).is_err());
    // Observations (TT-9, TT-10).
    store.record_observation(first.text.reference(), TrialObservation::SubAgentLinked { child_thread: "child-1".into(), by_person: false }).unwrap();
    let reading = first.text.fidelity(&[first.text.text()]);
    store.record_observation(first.text.reference(), TrialObservation::Fidelity { read_thread: Some("child-1".into()), reading, limits: vec![] }).unwrap();
    store.record_observation(first.text.reference(), TrialObservation::SubAgentUnlinked { child_thread: "child-1".into() }).unwrap();
    let back = store
        .record_observation(second.text.reference(), TrialObservation::BroughtBack { target_conversation: "thread-authoring".into(), transcript: "[Chirality] Trial 2 transcript".into(), shortenings: vec![] })
        .unwrap();
    assert_eq!(back["transcript"]["bytes"], 30);
    assert!(store.record_observation("trial:00000000-0000-4000-8000-000000000000", TrialObservation::SubAgentUnlinked { child_thread: "x".into() }).unwrap_err().contains("no trial link"));
    // A new process reads everything back.
    let reopened = TrialLinks::open(&s.app_data());
    assert!(reopened.limits().is_empty(), "{:?}", reopened.limits());
    assert_eq!(reopened.for_draft(&first.key).len(), 3);
    assert_eq!(reopened.observations(first.text.reference()).len(), 3);
    assert_eq!(reopened.next_sequence(&first.key), 3);
    let rows = reopened.trials_for_draft(&first.key, Some(&s.listed("load-check")));
    assert_eq!(rows.len(), 3);
    assert_eq!((rows[0]["kind"].as_str(), rows[0]["version"].as_str()), (Some("clean"), Some("current")), "newest first");
    assert_eq!(rows[0]["broughtBack"][0]["to"], "thread-authoring");
    assert_eq!((rows[1]["kind"].as_str(), rows[1]["version"].as_str()), (Some("delegated"), Some("earlier")));
    assert_eq!(rows[1]["subAgent"]["state"], "sub-agent not linked", "the latest observation (unlinked) stands");
    assert_eq!(rows[1]["fidelity"]["state"], "verbatim");
    assert_eq!(rows[1]["fidelity"]["header_present"], true);
    assert_eq!(rows[2]["kind"], "earlier attachment trial");
    assert_eq!(rows[2]["link"], earlier);
    // Memory only without an App data folder, and says so.
    let mut memory = TrialLinks::default();
    memory.record_sent(&first, &sent(TrialKind::Delegated)).unwrap();
    assert!(memory.limits()[0].contains("process memory only"));
}

// Torn or damaged records are reported, never hidden or rewritten; hidden
// staging leftovers and non-.json entries are reported, not read as records;
// a record's file name must name it.
#[test]
fn damaged_links_and_observations_are_reported_not_hidden_or_rewritten() {
    let s = Scratch::new();
    s.put("load-check", "x");
    let trial = s.prepare("load-check").unwrap();
    let mut store = TrialLinks::open(&s.app_data());
    let link = store.record_sent(&trial, &sent(TrialKind::Delegated)).unwrap();
    let observed = store.record_observation(trial.text.reference(), TrialObservation::SubAgentLinked { child_thread: "c".into(), by_person: true }).unwrap();
    assert_eq!(observed["linked_by"], "by the person");
    let dir = s.app_data().join(TRIAL_POINTERS);
    // A torn record (a truncated write by something other than the App's atomic writer).
    let torn = dir.join("trial-11111111-1111-4111-8111-111111111111.json");
    let bytes = serde_json::to_vec(&link).unwrap();
    fs::write(&torn, &bytes[..bytes.len() / 2]).unwrap();
    // A copy of the link under another trial's name.
    fs::write(dir.join("trial-22222222-2222-4222-8222-222222222222.json"), &bytes).unwrap();
    // An observation of a trial with no link here.
    let mut orphan = observed.clone();
    orphan["trial"] = json!("trial:33333333-3333-4333-8333-333333333333");
    orphan["observation_id"] = json!("trial-observation:44444444-4444-4444-8444-444444444444");
    fs::write(dir.join("observation-44444444-4444-4444-8444-444444444444.json"), serde_json::to_vec(&orphan).unwrap()).unwrap();
    // A hidden staging leftover from an interrupted write, a FIFO and a link.
    fs::write(dir.join(".trial-x.json.0.tmp"), b"{").unwrap();
    let fifo = std::ffi::CString::new(dir.join("pipe.json").to_str().unwrap()).unwrap();
    // SAFETY: a NUL-terminated path in this test's own scratch folder.
    assert_eq!(unsafe { libc::mkfifo(fifo.as_ptr(), 0o600) }, 0);
    symlink(dir.join(format!("trial-{}.json", trial.text.reference().trim_start_matches("trial:"))), dir.join("alias.json")).unwrap();
    let started = std::time::Instant::now();
    let reopened = TrialLinks::open(&s.app_data());
    assert!(started.elapsed() < std::time::Duration::from_secs(5), "nothing blocked on the FIFO");
    let limits = reopened.limits().join("\n");
    for name in ["trial-11111111", "trial-22222222", "cites trial", "pipe.json", "alias.json"] {
        assert!(limits.contains(name), "{name} missing from {limits}");
    }
    assert!(limits.contains("staging file left by an interrupted write") && limits.contains(".trial-x"), "staging leftovers reported: {limits}");
    assert_eq!(reopened.for_draft(&trial.key), vec![link], "the intact link is still listed");
    assert_eq!(reopened.observations(trial.text.reference()), vec![observed]);
    assert_eq!(fs::read(&torn).unwrap(), &bytes[..bytes.len() / 2], "never rewritten");
    // An uncertain create-once write is settled by reading the file back.
    let mut store = TrialLinks::open(&s.app_data());
    let value = json!({"record_kind":"probe"});
    store.keep("probe.json", &value).unwrap();
    store.keep("probe.json", &value).unwrap();
    assert!(store.keep("probe.json", &json!({"record_kind":"other"})).unwrap_err().contains("nothing overwritten"));
}

// TT-9 readings, pure: verbatim with and without the header, the three
// differences, and not checked when nothing can be read.
#[test]
fn fidelity_readings_follow_tt9() {
    let s = Scratch::new();
    s.put("load-check", "x");
    let t = s.prepare("load-check").unwrap().text;
    let run = t.run_text().to_owned();
    match t.fidelity(&["Please run this.", t.text()]) {
        FidelityReading::Verbatim { header_present: true, observed } => assert_eq!(observed, crate::role_supply::content(t.text().as_bytes())),
        other => panic!("{other:?}"),
    }
    let wrapped = format!("Do this exactly:\n{run}\nThanks");
    assert!(matches!(t.fidelity(&[&wrapped]), FidelityReading::Verbatim { header_present: false, .. }));
    let reframed = run.replacen("[Chirality] Workflow run start:", "Workflow:", 1);
    assert!(matches!(t.fidelity(&[&reframed]), FidelityReading::Differs { difference: FidelityDifference::FramingDiffers, .. }));
    let rebodied = run.replacen("# Method", "# Changed method", 1);
    assert!(matches!(t.fidelity(&[&rebodied]), FidelityReading::Differs { difference: FidelityDifference::BodyDiffers, .. }));
    assert!(matches!(t.fidelity(&["Summarize the workflow for me."]), FidelityReading::Differs { difference: FidelityDifference::WorkflowNotFound, .. }));
    assert!(matches!(t.fidelity(&[]), FidelityReading::NotChecked { .. }));
    // Every reading forms a conforming observation.
    let mut store = TrialLinks::open(&s.app_data());
    let trial = s.prepare("load-check").unwrap();
    store.record_sent(&trial, &sent(TrialKind::Clean)).unwrap();
    for reading in [t.fidelity(&[&wrapped]), t.fidelity(&[&reframed]), t.fidelity(&[]), FidelityReading::NotChecked { limits: vec![] }] {
        let limits = if matches!(reading, FidelityReading::NotChecked { .. }) { vec!["read failed: page 2".into()] } else { vec![] };
        store.record_observation(trial.text.reference(), TrialObservation::Fidelity { read_thread: Some("thread-clean".into()), reading, limits }).unwrap();
    }
}

// WR §8 conformance instances (WR-VC-11): every valid instance conforms and
// every invalid one is refused, against the App's resource copy of the schema.
#[test]
fn design_conformance_instances_hold_against_the_resource_schema() {
    let valid = include_str!("../../../execution/PKG-02/DEL-02-02/Design/workspace-registration.valid.examples.jsonl");
    let mut kinds = std::collections::BTreeSet::new();
    for line in valid.lines().filter(|l| !l.trim().is_empty()) {
        let v: Value = serde_json::from_str(line).unwrap();
        let kind = v["record_kind"].as_str().unwrap().to_owned();
        crate::workflow_workspace::wr_validate(&kind, &v).unwrap_or_else(|e| panic!("{kind}: {e}"));
        kinds.insert(kind);
    }
    assert!(kinds.contains("trial_pointer") && kinds.contains("trial_observation"));
    let invalid: Vec<Value> =
        serde_json::from_str(include_str!("../../../execution/PKG-02/DEL-02-02/Design/workspace-registration.invalid.examples.json")).unwrap();
    for case in invalid {
        let kind = case["kind"].as_str().unwrap();
        assert!(crate::workflow_workspace::wr_validate(kind, &case["instance"]).is_err(), "{} accepted", case["case"]);
    }
}

// Observations of one trial are strictly ordered by time: the clock is read
// again until it passes the latest observation (bounded).
#[test]
fn observation_times_strictly_increase_over_the_latest() {
    let mut readings = vec!["2026-10-10T00:00:00.006Z", "2026-10-10T00:00:00.005Z", "2026-10-10T00:00:00.005Z"];
    let mut waits = 0;
    let t = later_than(Some("2026-10-10T00:00:00.005Z"), || readings.pop().unwrap().to_owned(), || waits += 1);
    assert_eq!((t.as_str(), waits), ("2026-10-10T00:00:00.006Z", 2));
    assert_eq!(later_than(None, || "x".to_owned(), || panic!("no wait without a latest")), "x");
    // Through the store: an observation pre-seeded 20 ms in the future is
    // still followed by a strictly later one.
    let s = Scratch::new();
    s.put("load-check", "x");
    let trial = s.prepare("load-check").unwrap();
    let mut store = TrialLinks::open(&s.app_data());
    store.record_sent(&trial, &sent(TrialKind::Delegated)).unwrap();
    let first = store.record_observation(trial.text.reference(), TrialObservation::SubAgentLinked { child_thread: "c".into(), by_person: false }).unwrap();
    let future = loop {
        let now = crate::util::now_rfc3339();
        let ms: u32 = now[20..23].parse().unwrap();
        if ms <= 970 {
            break format!("{}{:03}Z", &now[..20], ms + 20);
        }
        std::thread::sleep(std::time::Duration::from_millis(10));
    };
    let mut seeded = first.clone();
    seeded["time"] = json!(future);
    seeded["observation_id"] = json!("trial-observation:55555555-5555-4555-8555-555555555555");
    fs::write(s.app_data().join(TRIAL_POINTERS).join("observation-55555555-5555-4555-8555-555555555555.json"), serde_json::to_vec(&seeded).unwrap()).unwrap();
    let mut store = TrialLinks::open(&s.app_data());
    assert!(store.limits().is_empty(), "{:?}", store.limits());
    let next = store.record_observation(trial.text.reference(), TrialObservation::SubAgentUnlinked { child_thread: "c".into() }).unwrap();
    assert!(next["time"].as_str().unwrap() > future.as_str(), "{} after {future}", next["time"]);
}

// A non-hidden entry that is not a `.json` file is reported, not dropped.
#[test]
fn non_json_entries_in_the_link_store_are_reported() {
    let s = Scratch::new();
    let dir = s.app_data().join(TRIAL_POINTERS);
    fs::create_dir_all(dir.join("sub")).unwrap();
    fs::write(dir.join("trial-66666666-6666-4666-8666-666666666666"), b"{}").unwrap();
    fs::write(dir.join("UPPER.JSON"), b"{}").unwrap();
    let limits = TrialLinks::open(&s.app_data()).limits().join("\n");
    for name in ["sub", "trial-66666666-6666-4666-8666-666666666666", "UPPER.JSON"] {
        assert!(limits.contains(&format!("not a record (not a .json file), not listed: {}", dir.join(name).display())), "{name}: {limits}");
    }
}

// An attached App data folder whose trial folder is refused (a link in its
// path) refuses writes with the cause; only a store with no App data folder
// at all keeps records in memory.
#[test]
fn a_refused_app_data_folder_refuses_writes_instead_of_keeping_them_in_memory() {
    let s = Scratch::new();
    s.put("load-check", "x");
    let trial = s.prepare("load-check").unwrap();
    let elsewhere = Scratch::new();
    fs::create_dir_all(s.app_data().join("runtime")).unwrap();
    symlink(&elsewhere.0, s.app_data().join("runtime/wr")).unwrap();
    let mut store = TrialLinks::open(&s.app_data());
    assert!(store.limits()[0].contains("symlink"));
    let refused = store.record_sent(&trial, &sent(TrialKind::Delegated)).unwrap_err();
    assert!(refused.contains("refused") && refused.contains("symlink"), "{refused}");
    assert!(store.link(trial.text.reference()).is_none(), "nothing kept in memory");
    assert!(store.record(&trial.key, &trial.content, "thread").is_err());
    assert!(entries(&elsewhere.0).is_empty());
}
