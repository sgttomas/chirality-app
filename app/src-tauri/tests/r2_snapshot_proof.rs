//! Dedicated dormant proof binary. No App library call, process spawn or production activation.
#![cfg(any(target_os = "macos", target_os = "linux"))]
#[path = "../src/r2_snapshot_proof.rs"]
mod proof;
use proof::*;
use std::{
    alloc::{GlobalAlloc, Layout, System},
    cell::Cell,
    fs,
    io::Write,
    os::unix::fs::{symlink, MetadataExt, PermissionsExt},
    path::PathBuf,
    sync::atomic::{AtomicU64, Ordering},
};
thread_local! {static METER:Cell<bool>=const{Cell::new(false)};static REQUESTED:Cell<usize>=const{Cell::new(0)};}
struct Meter;
unsafe impl GlobalAlloc for Meter {
    unsafe fn alloc(&self, l: Layout) -> *mut u8 {
        account(l.size());
        System.alloc(l)
    }
    unsafe fn alloc_zeroed(&self, l: Layout) -> *mut u8 {
        account(l.size());
        System.alloc_zeroed(l)
    }
    unsafe fn realloc(&self, p: *mut u8, l: Layout, n: usize) -> *mut u8 {
        account(n);
        System.realloc(p, l, n)
    }
    unsafe fn dealloc(&self, p: *mut u8, l: Layout) {
        System.dealloc(p, l)
    }
}
#[global_allocator]
static ALLOCATOR: Meter = Meter;
fn account(n: usize) {
    let _ = METER.try_with(|on| {
        if on.get() {
            let _ = REQUESTED.try_with(|v| v.set(v.get().checked_add(n).unwrap_or(usize::MAX)));
        }
    });
}
fn measured<T>(label: &str, retained: usize, f: impl FnOnce() -> T) -> T {
    struct Stop;
    impl Drop for Stop {
        fn drop(&mut self) {
            METER.with(|x| x.set(false));
        }
    }
    REQUESTED.with(|n| n.set(retained));
    METER.with(|x| x.set(true));
    let stop = Stop;
    let result = f();
    drop(stop);
    let total = REQUESTED.with(Cell::get);
    println!("R2 allocation upper bound {label}: {total} bytes (retained capacities + cumulative allocation requests; not RSS)");
    assert!(
        total <= 1048576,
        "{label}: measured upper bound {total} exceeds selected1MiB"
    );
    result
}
fn budget() -> TestBudget {
    TestBudget {
        n: 2,
        s: 32768,
        d: 4096,
        t: 0,
        q: 262144,
        artifacts: 32,
        refs: 64,
        entries: 64,
        members: 512,
        depth: 16,
        id: 128,
        text: 16384,
    }
}
struct Root(PathBuf);
impl Root {
    fn new() -> Self {
        static NEXT: AtomicU64 = AtomicU64::new(1);
        let stamp = std::time::SystemTime::now()
            .duration_since(std::time::UNIX_EPOCH)
            .unwrap()
            .as_nanos();
        let p = std::env::temp_dir().join(format!(
            "r2-proof-owned-{stamp}-{}",
            NEXT.fetch_add(1, Ordering::Relaxed)
        ));
        fs::create_dir(&p).unwrap();
        fs::set_permissions(&p, fs::Permissions::from_mode(0o700)).unwrap();
        Self(p)
    }
    fn ns(&self) -> PathBuf {
        self.0.join("r2-proof-fixture")
    }
    fn journal(&self, index: u64) -> PathBuf {
        self.ns().join(format!("journal-{index}"))
    }
    fn retained(&self) -> usize {
        std::mem::size_of::<Self>() + self.0.capacity()
    }
}
impl Drop for Root {
    fn drop(&mut self) {
        let _ = fs::remove_dir_all(&self.0);
    }
}
fn pass(_: Point) -> Result<(), String> {
    Ok(())
}
fn fail_at(wanted: Point) -> impl FnMut(Point) -> Result<(), String> {
    move |p| {
        if p == wanted {
            Err(format!("injected cut {p:?}"))
        } else {
            Ok(())
        }
    }
}
fn setup() -> (Root, Session, JournalConfirmed) {
    let r = Root::new();
    let (mut s, c) = Session::initialize(&r.0, budget(), "constructed-ns", &mut pass).unwrap();
    assert!(c.acknowledgment.starts_with("NamespaceConfirmed"));
    let j = s
        .admit("constructed-journal", "constructed-undertaking", &mut pass)
        .unwrap();
    assert_eq!(
        fs::metadata(r.ns()).unwrap().permissions().mode() & 0o777,
        0o700
    );
    for p in [
        r.ns().join("lock"),
        r.ns().join("control"),
        r.journal(0).join("admission"),
        r.journal(0).join("A"),
        r.journal(0).join("B"),
    ] {
        assert_eq!(fs::metadata(p).unwrap().permissions().mode() & 0o777, 0o600);
    }
    (r, s, j)
}
fn snapshot(revision: u64, previous: Option<String>) -> Snapshot {
    let artifacts = vec![
        Artifact::new(
            "base",
            ArtifactKind::ConstructedBase,
            include_str!("../resources/connector_route/record_reconstruction_v04.fixture.json"),
        ),
        Artifact::new(
            "answer",
            ArtifactKind::ConstructedAnswer,
            "constructed answer; no emission",
        ),
        Artifact::new(
            "review",
            ArtifactKind::ConstructedReview,
            "constructed review; not manager performance",
        ),
        Artifact::new(
            "intent",
            ArtifactKind::InjectedIntent,
            "constructed request intention; dispatch unknown",
        ),
        Artifact::new(
            "outcome",
            ArtifactKind::InjectedUnknownOutcome,
            "unknown whether effect happened; no retry permission",
        ),
        Artifact::new(
            "account",
            ArtifactKind::InjectedAccountReference,
            "injected definite BoundReference fact; no CRP operation",
        ),
    ];
    let required = artifacts.iter().map(|a| a.id.clone()).collect();
    let mut s = Snapshot::fixture(
        "constructed-ns",
        "constructed-journal",
        "constructed-undertaking",
        revision,
        previous,
        artifacts,
        required,
    );
    s.unresolved_attempts = List(vec!["original-injected-attempt".into()]);
    s.injected = InjectedFacts {
        intent: Some("intent".into()),
        unknown_outcome: Some("outcome".into()),
        confirmed_account: Some("account".into()),
    };
    s
}
fn next(s: &Session) -> Snapshot {
    let old = s.observe(0).unwrap().unwrap();
    snapshot(old.snapshot.revision + 1, Some(old.descriptor_sha256))
}
fn rewrite_descriptor(r: &Root, change: impl FnOnce(&mut Descriptor)) {
    let p = r.journal(0).join("descriptor");
    let mut d: Descriptor = serde_json::from_slice(&fs::read(&p).unwrap()).unwrap();
    change(&mut d);
    fs::write(p, serde_json::to_vec(&d).unwrap()).unwrap();
}
fn rewrite_selected(r: &Root, change: impl FnOnce(&mut Snapshot)) {
    let d: Descriptor =
        serde_json::from_slice(&fs::read(r.journal(0).join("descriptor")).unwrap()).unwrap();
    let name = match d.slot {
        Slot::A => "A",
        Slot::B => "B",
    };
    let p = r.journal(0).join(name);
    let mut s: Snapshot = serde_json::from_slice(&fs::read(&p).unwrap()).unwrap();
    change(&mut s);
    let bytes = serde_json::to_vec(&s).unwrap();
    fs::write(p, &bytes).unwrap();
    rewrite_descriptor(r, |d| {
        d.length = bytes.len() as u64;
        d.sha256 = digest(&bytes);
    });
}
#[test]
fn r2_survival() {
    let (r, mut s, j) = setup();
    let first = snapshot(1, None);
    s.commit(&j, &first, &mut pass).unwrap();
    drop(s);
    let mut s = Session::open_observed(&r.0, budget()).unwrap();
    let old = s.observe(0).unwrap().unwrap();
    assert_eq!(old.snapshot, first);
    assert!(old.original_acknowledgment.contains("Unavailable"));
    let (_, journals) = s.confirm_existing(&mut pass).unwrap();
    let j = &journals[0];
    for revision in 2..=3 {
        let value = next(&s);
        assert_eq!(value.revision, revision);
        s.commit(j, &value, &mut pass).unwrap();
    }
    drop(s);
    let observed = Session::open_observed(&r.0, budget())
        .unwrap()
        .observe(0)
        .unwrap()
        .unwrap();
    assert_eq!(observed.descriptor.slot, Slot::A);
    assert_eq!(observed.snapshot.required, first.required);
    assert_eq!(observed.snapshot.artifacts, first.artifacts);
    assert_eq!(
        observed.snapshot.unresolved_attempts,
        first.unresolved_attempts
    );
    assert!(observed.freshness.contains("Unproven"));
}
#[test]
fn r2_dropped_artifact() {
    let (_r, mut s, j) = setup();
    s.commit(&j, &snapshot(1, None), &mut pass).unwrap();
    let mut value = next(&s);
    value.required.0.retain(|x| x != "review");
    value.artifacts.0.retain(|x| x.id != "review");
    assert!(s
        .commit(&j, &value, &mut pass)
        .unwrap_err()
        .detail
        .contains("required identity"));
    assert_eq!(s.observe(0).unwrap().unwrap().snapshot.revision, 1);
}
#[test]
fn r2_rebound_id() {
    let (_r, mut s, j) = setup();
    s.commit(&j, &snapshot(1, None), &mut pass).unwrap();
    let mut value = next(&s);
    value.artifacts.0[0] = Artifact::new("base", ArtifactKind::ConstructedBase, "changed bytes");
    assert!(s
        .commit(&j, &value, &mut pass)
        .unwrap_err()
        .detail
        .contains("rebound"));
    for field in ["identity", "revision", "predecessor"] {
        let mut changed = next(&s);
        match field {
            "identity" => changed.namespace = "other".into(),
            "revision" => changed.revision += 1,
            _ => changed.previous = Some("0".repeat(64)),
        }
        assert!(s
            .commit(&j, &changed, &mut pass)
            .unwrap_err()
            .detail
            .contains("identity/revision/predecessor"));
        assert_eq!(s.observe(0).unwrap().unwrap().snapshot.revision, 1);
    }
}
#[test]
fn r2_mutable_ref() {
    let (_r, mut s, j) = setup();
    let mut value = snapshot(1, None);
    value.required.0.push("slot-A/reference-only".into());
    assert!(s
        .commit(&j, &value, &mut pass)
        .unwrap_err()
        .detail
        .contains("embedded required"));
    let mut json = serde_json::to_value(snapshot(1, None)).unwrap();
    json.as_object_mut()
        .unwrap()
        .insert("slot_reference".into(), serde_json::json!("A"));
    assert!(decode::<Snapshot>(&serde_json::to_vec(&json).unwrap(), 32768, &budget()).is_err());
}
#[test]
fn r2_capacity() {
    let mut b = budget();
    assert_eq!(b.reservation().unwrap(), 163840);
    b.q = 163840;
    b.validate().unwrap();
    b.q -= 1;
    assert!(b.validate().is_err());
    let r = Root::new();
    let mut b = budget();
    b.n = 1;
    let (mut s, _) = Session::initialize(&r.0, b.clone(), "constructed-ns", &mut pass).unwrap();
    let j = s
        .admit("constructed-journal", "constructed-undertaking", &mut pass)
        .unwrap();
    assert!(s.admit("second", "second", &mut pass).is_err());
    s.commit(&j, &snapshot(1, None), &mut pass).unwrap();
    for cap in [800u64, 1500] {
        let r = Root::new();
        let mut b = budget();
        b.s = cap;
        let (mut s, _) = Session::initialize(&r.0, b, "constructed-ns", &mut pass).unwrap();
        let j = s
            .admit("constructed-journal", "constructed-undertaking", &mut pass)
            .unwrap();
        let result = s.commit(&j, &snapshot(1, None), &mut pass);
        if serde_json::to_vec(&snapshot(1, None)).unwrap().len() as u64 > cap {
            assert_eq!(result.unwrap_err().standing, Standing::NotCommitted);
        }
    }
    let original = snapshot(1, None);
    let length = serde_json::to_vec(&original).unwrap().len();
    for delta in [0usize, 1] {
        let r = Root::new();
        let mut b = budget();
        b.s = (length - delta) as u64;
        let (mut s, _) = Session::initialize(&r.0, b, "constructed-ns", &mut pass).unwrap();
        let j = s
            .admit("constructed-journal", "constructed-undertaking", &mut pass)
            .unwrap();
        assert_eq!(s.commit(&j, &original, &mut pass).is_ok(), delta == 0);
    }
    // D covers immutable metadata and descriptor; force a descriptor-only shortage.
    let (r, mut s, j) = setup();
    s.commit(&j, &original, &mut pass).unwrap();
    let dlen = fs::metadata(r.journal(0).join("descriptor")).unwrap().len();
    drop(s);
    for delta in [0u64, 1] {
        let r = Root::new();
        let mut b = budget();
        b.d = dlen - delta;
        let (mut s, _) = Session::initialize(&r.0, b, "constructed-ns", &mut pass).unwrap();
        let j = s
            .admit("constructed-journal", "constructed-undertaking", &mut pass)
            .unwrap();
        assert_eq!(s.commit(&j, &original, &mut pass).is_ok(), delta == 0);
    }
}
#[test]
fn r2_no_policy() {
    for which in ["n", "s", "d", "q", "overflow", "retirement"] {
        let mut b = budget();
        match which {
            "n" => b.n = 0,
            "s" => b.s = 0,
            "d" => b.d = 0,
            "q" => b.q = 0,
            "overflow" => {
                b.n = u64::MAX;
                b.s = u64::MAX;
            }
            _ => b.t = 1,
        };
        let r = Root::new();
        let error = Session::initialize(&r.0, b, "n", &mut pass).unwrap_err();
        assert_eq!(error.standing, Standing::NoBootstrapOrAdmissionAttempt);
        assert!(!r.ns().exists());
    }
    let absent: Option<TestBudget> = None;
    assert!(absent.is_none(), "no fallback budget constructor exists");
}
#[test]
fn r2_no_retire() {
    for status in [Status::ConstructedTerminal, Status::ConstructedCancelled] {
        let (r, mut s, j) = setup();
        let mut snap = snapshot(1, None);
        snap.status = status;
        s.commit(&j, &snap, &mut pass).unwrap();
        s.admit("second", "second", &mut pass).unwrap();
        assert!(s.admit("third", "third", &mut pass).is_err());
        drop(s);
        let mut s = Session::open_observed(&r.0, budget()).unwrap();
        s.confirm_existing(&mut pass).unwrap();
        assert!(s.admit("third", "third", &mut pass).is_err());
    }
}
#[test]
fn r2_write_cuts() {
    let stages = [
        Step::InactiveWrite,
        Step::InactiveSync,
        Step::InactiveReadback,
        Step::DescriptorCreate,
        Step::DescriptorWrite,
        Step::DescriptorSync,
        Step::SelectionRecheck,
        Step::DescriptorReplace,
        Step::CommitDirectorySync,
        Step::CommitReadback,
        Step::CommitAck,
    ];
    for (stage_index, stage) in stages.into_iter().enumerate() {
        for edge in [Edge::Before, Edge::After] {
            let (r, mut s, j) = setup();
            s.commit(&j, &snapshot(1, None), &mut pass).unwrap();
            let value = next(&s);
            let error = s
                .commit(&j, &value, &mut fail_at((stage, edge)))
                .unwrap_err();
            let uncertain = stage_index > 7 || (stage_index == 7 && edge == Edge::After);
            assert_eq!(
                error.standing,
                if uncertain {
                    Standing::Uncertain
                } else {
                    Standing::NotCommitted
                },
                "{stage:?}/{edge:?}"
            );
            if stage != Step::InactiveWrite || edge != Edge::Before {
                assert!(error.attempt.is_some());
                assert!(
                    s.commit(&j, &value, &mut pass).is_err(),
                    "no automatic retry"
                );
            }
            drop(s);
            let observed = Session::open_observed(&r.0, budget())
                .unwrap()
                .observe(0)
                .unwrap()
                .unwrap();
            assert_eq!(observed.snapshot.revision, if uncertain { 2 } else { 1 });
            assert!(observed.original_acknowledgment.contains("Unavailable"));
        }
    }
}
#[test]
fn r2_torn() {
    for target in ["descriptor", "A"] {
        let (r, mut s, j) = setup();
        s.commit(&j, &snapshot(1, None), &mut pass).unwrap();
        drop(s);
        fs::write(r.journal(0).join(target), b"{\"format\":").unwrap();
        let s = Session::open_observed(&r.0, budget()).unwrap();
        assert!(s.observe(0).is_err());
    }
}
#[test]
fn r2_fork() {
    let (r, mut s, j) = setup();
    s.commit(&j, &snapshot(1, None), &mut pass).unwrap();
    s.admit("second", "second", &mut pass).unwrap();
    let mut a: Admission =
        serde_json::from_slice(&fs::read(r.journal(1).join("admission")).unwrap()).unwrap();
    a.journal = "constructed-journal".into();
    fs::write(
        r.journal(1).join("admission"),
        serde_json::to_vec(&a).unwrap(),
    )
    .unwrap();
    assert!(s.observe(0).unwrap_err().detail.contains("duplicate"));
}
#[test]
fn r2_growth() {
    let (r, mut s, j) = setup();
    s.commit(&j, &snapshot(1, None), &mut pass).unwrap();
    drop(s);
    let dir = fs::File::open(r.journal(0)).unwrap();
    let error = read_file_with(&dir, "A", 32768, || {
        fs::OpenOptions::new()
            .append(true)
            .open(r.journal(0).join("A"))
            .unwrap()
            .write_all(&vec![b' '; 32768])
            .unwrap();
    })
    .unwrap_err();
    assert!(error.contains("sentinel"));
    assert!(read_bounded(&b"12345"[..], 4).is_err());
    assert_eq!(read_bounded(&b"1234"[..], 4).unwrap(), b"1234");
}
#[test]
fn r2_enum() {
    let (r, mut s, _) = setup();
    for i in 0..65 {
        fs::write(r.ns().join(format!("unknown-{i}")), b"x").unwrap();
    }
    let error = s.admit("next", "next", &mut pass).unwrap_err();
    assert!(error.detail.contains("entry/issue bound"));
    assert!(error.observed_entries.len() <= 64);
}
#[test]
fn r2_lock() {
    let (r, s, _) = setup();
    assert!(Session::open_observed(&r.0, budget())
        .unwrap_err()
        .detail
        .contains("Busy"));
    fs::rename(r.ns().join("lock"), r.ns().join("old-lock")).unwrap();
    fs::write(r.ns().join("lock"), b"").unwrap();
    assert!(s
        .observe(0)
        .unwrap_err()
        .detail
        .contains("lock entry substituted"));
}
#[test]
fn r2_rollback() {
    let (r, mut s, j) = setup();
    s.commit(&j, &snapshot(1, None), &mut pass).unwrap();
    let descriptor = fs::read(r.journal(0).join("descriptor")).unwrap();
    let raw = fs::read(r.journal(0).join("A")).unwrap();
    let value = next(&s);
    s.commit(&j, &value, &mut pass).unwrap();
    drop(s);
    fs::write(r.journal(0).join("descriptor"), descriptor).unwrap();
    fs::write(r.journal(0).join("A"), raw).unwrap();
    let observed = Session::open_observed(&r.0, budget())
        .unwrap()
        .observe(0)
        .unwrap()
        .unwrap();
    assert_eq!(observed.snapshot.revision, 1);
    assert!(observed.freshness.contains("Unproven"));
}
#[test]
fn r2_intent_gap() {
    let (r, mut s, j) = setup();
    s.commit(&j, &snapshot(1, None), &mut pass).unwrap();
    drop(s);
    let mut s = Session::open_observed(&r.0, budget()).unwrap();
    let old = s.observe(0).unwrap().unwrap();
    assert_eq!(
        old.snapshot.unresolved_attempts.0,
        ["original-injected-attempt"]
    );
    let (_, js) = s.confirm_existing(&mut pass).unwrap();
    let mut value = next(&s);
    value.unresolved_attempts.0.clear();
    assert!(s
        .commit(&js[0], &value, &mut pass)
        .unwrap_err()
        .detail
        .contains("implicitly resolved"));
}
#[test]
fn r2_account_confirmed() {
    let (_r, mut s, j) = setup();
    s.commit(&j, &snapshot(1, None), &mut pass).unwrap();
    let injected_definite_account = String::from(
        "constructed definite BoundReference retained separately in live test custody",
    );
    let value = next(&s);
    let error = s
        .commit(
            &j,
            &value,
            &mut fail_at((Step::CommitDirectorySync, Edge::Before)),
        )
        .unwrap_err();
    assert_eq!(error.standing, Standing::Uncertain);
    assert!(injected_definite_account.contains("definite BoundReference"));
    assert_eq!(error.attempt.as_ref().unwrap().operation, "snapshot");
    assert_eq!(error.attempt.as_ref().unwrap().revision, Some(2));
}
#[test]
fn r2_ack_missing() {
    let (r, mut s, j) = setup();
    let error = s
        .commit(
            &j,
            &snapshot(1, None),
            &mut fail_at((Step::CommitAck, Edge::Before)),
        )
        .unwrap_err();
    assert_eq!(error.standing, Standing::Uncertain);
    let original = error.attempt.unwrap();
    drop(s);
    let mut s = Session::open_observed(&r.0, budget()).unwrap();
    let observed = s.observe(0).unwrap().unwrap();
    assert!(observed.original_acknowledgment.contains("Unavailable"));
    let (c, journals) = s.confirm_existing(&mut pass).unwrap();
    assert!(c.acknowledgment.contains("original"));
    assert!(journals[0].acknowledgment.contains("unknown"));
    assert!(!original.identity.is_empty());
}
#[test]
fn r2_bounds() {
    let r = Root::new();
    let retained = r.retained() + std::mem::size_of::<TestBudget>() + 128;
    let (mut s, _) = measured("bootstrap", retained, || {
        Session::initialize(&r.0, budget(), "constructed-ns", &mut pass)
    })
    .unwrap();
    let j = measured(
        "admission",
        r.retained() + s.retained_capacity() + 256,
        || s.admit("constructed-journal", "constructed-undertaking", &mut pass),
    )
    .unwrap();
    let mut value = snapshot(1, None);
    value.artifacts.0.push(Artifact::new(
        "large",
        ArtifactKind::RecordedData,
        &"x".repeat(1000),
    ));
    value.required.0.push("large".into());
    for i in 7..32 {
        let id = format!("artifact-{i}");
        value
            .artifacts
            .0
            .push(Artifact::new(&id, ArtifactKind::RecordedData, ""));
        value.required.0.push(id);
    }
    value.unresolved_attempts = List(
        (0..64)
            .map(|i| format!("attempt-{i:03}-{}", "x".repeat(116)))
            .collect(),
    );
    for _ in 1..63 {
        value.gaps.0.push("x".into());
    }
    let size = serde_json::to_vec(&value).unwrap().len();
    let extra = 32768 - size;
    value.gaps.0.push("x".repeat(extra.saturating_sub(3)));
    let raw = serde_json::to_vec(&value).unwrap();
    assert_eq!(raw.len(), 32768);
    drop(raw);
    let retained = r.retained()
        + s.retained_capacity()
        + value.retained_capacity()
        + j.journal.capacity()
        + j.undertaking.capacity()
        + j.admission_sha256.capacity()
        + std::mem::size_of::<JournalConfirmed>();
    let receipt = measured("boundary first commit", retained, || {
        s.commit(&j, &value, &mut pass)
    })
    .unwrap();
    value.revision = 2;
    value.previous = Some(receipt.descriptor_sha256);
    let gap = value.gaps.0.last_mut().unwrap();
    gap.truncate(gap.len() - 62);
    assert_eq!(serde_json::to_vec(&value).unwrap().len(), 32768);
    let retained = r.retained()
        + s.retained_capacity()
        + value.retained_capacity()
        + j.journal.capacity()
        + j.undertaking.capacity()
        + j.admission_sha256.capacity()
        + 512;
    measured("boundary successor commit", retained, || {
        s.commit(&j, &value, &mut pass)
    })
    .unwrap();
    drop(value);
    drop(j);
    drop(s);
    let s = measured(
        "cold independent open",
        r.retained() + std::mem::size_of::<TestBudget>(),
        || Session::open_observed(&r.0, budget()),
    )
    .unwrap();
    let observed = measured(
        "boundary selected read",
        r.retained() + s.retained_capacity(),
        || s.observe(0),
    )
    .unwrap()
    .unwrap();
    assert_eq!(observed.raw.len(), 32768);
    drop(observed);
    let mut s = s;
    let retained = r.retained() + s.retained_capacity();
    measured("cold confirm-existing", retained, || {
        s.confirm_existing(&mut pass)
    })
    .unwrap();
    drop(s);
}
#[test]
fn r2_no_capability() {
    let (r, mut s, j) = setup();
    let mut value = snapshot(1, None);
    value.artifacts.0.push(Artifact::new(
        "grant-text",
        ArtifactKind::RecordedData,
        "role/grant/native receipt strings are historical test data only",
    ));
    value.required.0.push("grant-text".into());
    s.commit(&j, &value, &mut pass).unwrap();
    drop(s);
    let observed = Session::open_observed(&r.0, budget())
        .unwrap()
        .observe(0)
        .unwrap()
        .unwrap();
    assert!(observed
        .original_acknowledgment
        .contains("not original confirmation or CAM custody"));
}
#[test]
fn r2_no_activation() {
    let lib = include_str!("../src/lib.rs");
    let cargo = include_str!("../Cargo.toml");
    assert!(!lib.contains("r2_snapshot_proof"));
    assert!(!cargo.contains("r2_snapshot_proof"));
    assert!(include_str!("../src/r2_snapshot_proof.rs").contains("#![cfg(all(test,"));
}
#[test]
fn r2_cold_repeat() {
    let (r, mut s, j) = setup();
    let value = snapshot(1, None);
    let receipt = s.commit(&j, &value, &mut pass).unwrap();
    let bytes = fs::read(r.journal(0).join("A")).unwrap();
    assert_eq!(receipt.revision, 1);
    assert!(receipt.acknowledgment.contains("Confirmed"));
    drop(s);
    for _ in 0..3 {
        let s = Session::open_observed(&r.0, budget()).unwrap();
        let observed = s.observe(0).unwrap().unwrap();
        assert_eq!(observed.raw, bytes);
        assert_eq!(observed.snapshot, value);
        assert_eq!(observed.descriptor_sha256, receipt.descriptor_sha256);
    }
}
#[test]
fn r2_bootstrap_cuts_and_new_confirmation() {
    for stage in [
        Step::NamespaceMkdir,
        Step::RootSync,
        Step::LockCreate,
        Step::LockSync,
        Step::LockDirectorySync,
        Step::ControlCreate,
        Step::ControlWrite,
        Step::ControlSync,
        Step::ControlDirectorySync,
        Step::ControlReadback,
        Step::NamespaceAck,
    ] {
        for edge in [Edge::Before, Edge::After] {
            let r = Root::new();
            let error = Session::initialize(
                &r.0,
                budget(),
                "constructed-ns",
                &mut fail_at((stage, edge)),
            )
            .unwrap_err();
            let before = stage == Step::NamespaceMkdir && edge == Edge::Before;
            assert_eq!(
                error.standing,
                if before {
                    Standing::NoBootstrapOrAdmissionAttempt
                } else {
                    Standing::IncompleteOrUncertainBootstrap
                }
            );
            assert_eq!(error.attempt.is_none(), before);
            if !before {
                assert!(r.ns().exists());
                assert!(Session::initialize(&r.0, budget(), "constructed-ns", &mut pass).is_err());
                if let Ok(mut observed) = Session::open_observed(&r.0, budget()) {
                    let forged = JournalConfirmed {
                        index: 0,
                        journal: "constructed-journal".into(),
                        undertaking: "constructed-undertaking".into(),
                        acknowledgment: "caller string is not confirmation",
                        directory_identity: Identity {
                            device: 0,
                            inode: 0,
                        },
                        admission_identity: Identity {
                            device: 0,
                            inode: 0,
                        },
                        admission_sha256: String::new(),
                    };
                    assert!(observed
                        .commit(&forged, &snapshot(1, None), &mut pass)
                        .is_err());
                    let (confirmation, _) = observed.confirm_existing(&mut pass).unwrap();
                    assert!(confirmation
                        .acknowledgment
                        .contains("original bootstrap/attempt acknowledgment unknown"));
                }
            }
        }
    }
}
#[test]
fn r2_admission_cuts_reserve_or_block() {
    for stage in [
        Step::JournalMkdir,
        Step::JournalParentSync,
        Step::AdmissionCreate,
        Step::AdmissionWrite,
        Step::AdmissionSync,
        Step::SlotACreate,
        Step::SlotASync,
        Step::SlotBCreate,
        Step::SlotBSync,
        Step::AdmissionDirectorySync,
        Step::AdmissionParentSync,
        Step::AdmissionReadback,
        Step::AdmissionAck,
    ] {
        for edge in [Edge::Before, Edge::After] {
            let r = Root::new();
            let (mut s, _) =
                Session::initialize(&r.0, budget(), "constructed-ns", &mut pass).unwrap();
            let error = s
                .admit(
                    "constructed-journal",
                    "constructed-undertaking",
                    &mut fail_at((stage, edge)),
                )
                .unwrap_err();
            let before = stage == Step::JournalMkdir && edge == Edge::Before;
            assert_eq!(
                error.standing,
                if before {
                    Standing::NoBootstrapOrAdmissionAttempt
                } else {
                    Standing::IncompleteOrUncertainAdmission
                }
            );
            assert_eq!(error.attempt.is_none(), before);
            if !before {
                assert!(s.admit("retry", "retry", &mut pass).is_err());
                let forged = JournalConfirmed {
                    index: 0,
                    journal: "constructed-journal".into(),
                    undertaking: "constructed-undertaking".into(),
                    acknowledgment: "not admitted",
                    directory_identity: Identity {
                        device: 0,
                        inode: 0,
                    },
                    admission_identity: Identity {
                        device: 0,
                        inode: 0,
                    },
                    admission_sha256: String::new(),
                };
                assert!(s.commit(&forged, &snapshot(1, None), &mut pass).is_err());
                drop(s);
                let mut cold = Session::open_observed(&r.0, budget()).unwrap();
                match cold.confirm_existing(&mut pass) {
                    Ok((c, journals)) => {
                        assert!(c.acknowledgment.contains("unknown"));
                        assert_eq!(journals[0].index, 0);
                        assert_eq!(
                            cold.admit("different", "different", &mut pass)
                                .unwrap()
                                .index,
                            1
                        );
                    }
                    Err(_) => assert!(cold.admit("different", "different", &mut pass).is_err()),
                }
            }
        }
    }
}
fn duplicate(bytes: &[u8], key: &str, value: &str) -> Vec<u8> {
    let s = std::str::from_utf8(bytes).unwrap();
    format!("{},\"{key}\":{value}}}", &s[..s.len() - 1]).into_bytes()
}
#[test]
fn r2_codec_actual_duplicate_keys_and_exact_structural_bounds() {
    assert_eq!(scan(br#"{"first":0}"#, 16, 512).unwrap(), 1);
    let object = |n: usize| {
        format!(
            "{{{}}}",
            (0..n)
                .map(|i| format!("\"k{i}\":0"))
                .collect::<Vec<_>>()
                .join(",")
        )
    };
    assert_eq!(scan(object(512).as_bytes(), 16, 512).unwrap(), 512);
    assert!(scan(object(513).as_bytes(), 16, 512).is_err());
    let escaped = br#"{"a":"punctuation: , [ ] { } and escaped quote \" : ,","b":0}"#;
    serde_json::from_slice::<serde_json::Value>(escaped).unwrap();
    assert_eq!(scan(escaped, 16, 512).unwrap(), 2);
    let nested = |n| format!("{}0{}", "[".repeat(n), "]".repeat(n));
    scan(nested(16).as_bytes(), 16, 512).unwrap();
    assert!(scan(nested(17).as_bytes(), 16, 512).is_err());
    for count in [32, 33] {
        let mut values = vec![serde_json::json!("id"); count];
        if count == 33 {
            values[32] = serde_json::json!({"must_not_decode_as_string":true});
        }
        let raw = serde_json::to_vec(&values).unwrap();
        let parsed = decode::<List<String, 32>>(&raw, 32768, &budget());
        if count == 32 {
            assert_eq!(parsed.unwrap().0.len(), 32);
        } else {
            assert!(parsed.unwrap_err().contains("before decoding next item"));
        }
    }
    assert!(decode::<Refs>(
        &serde_json::to_vec(&vec!["id"; 65]).unwrap(),
        32768,
        &budget()
    )
    .unwrap_err()
    .contains("before decoding"));
    for target in ["control", "admission", "descriptor", "snapshot"] {
        let (r, mut s, j) = setup();
        s.commit(&j, &snapshot(1, None), &mut pass).unwrap();
        drop(s);
        let path = match target {
            "control" => r.ns().join("control"),
            "admission" => r.journal(0).join("admission"),
            "descriptor" => r.journal(0).join("descriptor"),
            _ => r.journal(0).join("A"),
        };
        let key = if target == "control" {
            "namespace"
        } else {
            "journal"
        };
        let text = if target == "control" {
            "\"constructed-ns\""
        } else {
            "\"constructed-journal\""
        };
        let raw = duplicate(&fs::read(&path).unwrap(), key, text);
        fs::write(path, &raw).unwrap();
        if target == "snapshot" {
            rewrite_descriptor(&r, |d| {
                d.length = raw.len() as u64;
                d.sha256 = digest(&raw);
            });
        }
        if target == "control" {
            assert!(Session::open_observed(&r.0, budget())
                .unwrap_err()
                .detail
                .contains("duplicate field"));
        } else {
            assert!(Session::open_observed(&r.0, budget())
                .unwrap()
                .observe(0)
                .unwrap_err()
                .detail
                .contains("duplicate field"));
        }
    }
    let value = snapshot(1, None);
    let raw = serde_json::to_vec(&value).unwrap();
    let mut trailing = raw.clone();
    trailing.extend_from_slice(b" true");
    assert!(decode::<Snapshot>(&trailing, 32768, &budget()).is_err());
    assert!(decode::<Snapshot>(&raw[..raw.len() - 1], 32768, &budget()).is_err());
    let mut invalid = raw.clone();
    invalid[0] = 0xff;
    assert!(decode::<Snapshot>(&invalid, 32768, &budget()).is_err());
    let overflow = String::from_utf8(raw)
        .unwrap()
        .replace("\"revision\":1", "\"revision\":18446744073709551616");
    assert!(decode::<Snapshot>(overflow.as_bytes(), 32768, &budget()).is_err());
    for change in ["unknown", "text", "id", "duplicates", "required", "attempt"] {
        let (r, mut s, j) = setup();
        s.commit(&j, &snapshot(1, None), &mut pass).unwrap();
        drop(s);
        if change == "unknown" {
            let p = r.journal(0).join("A");
            let raw = duplicate(&fs::read(&p).unwrap(), "arbitrary_metadata", "{}");
            fs::write(p, &raw).unwrap();
            rewrite_descriptor(&r, |d| {
                d.length = raw.len() as u64;
                d.sha256 = digest(&raw);
            });
        } else {
            rewrite_selected(&r, |s| match change {
                "text" => {
                    s.artifacts.0[0] =
                        Artifact::new("base", ArtifactKind::ConstructedBase, &"x".repeat(16385))
                }
                "id" => s.artifacts.0[0].id = "x".repeat(129),
                "duplicates" => s.artifacts.0.push(s.artifacts.0[0].clone()),
                "required" => s.required.0.push(s.required.0[0].clone()),
                _ => s
                    .unresolved_attempts
                    .0
                    .push(s.unresolved_attempts.0[0].clone()),
            });
        }
        assert!(
            Session::open_observed(&r.0, budget())
                .unwrap()
                .observe(0)
                .is_err(),
            "{change}"
        );
    }
}
#[test]
fn r2_identity_root_symlink_refused() {
    let target = Root::new();
    let alias = Root::new();
    let path = alias.0.join("root-alias");
    symlink(&target.0, &path).unwrap();
    assert!(
        Session::initialize(&path, budget(), "constructed-ns", &mut pass).is_err(),
        "root alias must not silently follow"
    );
    assert!(!target.ns().exists());
}
#[test]
fn r2_identity_missing_known_admission_not_forgotten() {
    let (r, mut s, _) = setup();
    fs::remove_dir_all(r.journal(0)).unwrap();
    assert!(
        s.confirm_existing(&mut pass).is_err(),
        "confirmation must retain known occupied admission rather than forget/reuse it"
    );
    assert!(s.admit("replacement", "replacement", &mut pass).is_err());
}
#[test]
fn r2_identity_descriptor_substitution_before_replace() {
    let (r, mut s, j) = setup();
    s.commit(&j, &snapshot(1, None), &mut pass).unwrap();
    let value = next(&s);
    let mut hook = |p| {
        if p == (Step::SelectionRecheck, Edge::Before) {
            let path = r.journal(0).join("descriptor");
            let bytes = fs::read(&path).unwrap();
            fs::rename(&path, r.0.join("observed-old-descriptor")).unwrap();
            fs::write(path, bytes).unwrap();
        }
        Ok(())
    };
    let error = s.commit(&j, &value, &mut hook).unwrap_err();
    assert_eq!(error.standing, Standing::NotCommitted);
    assert!(error.detail.contains("descriptor identity"));
    assert_eq!(s.observe(0).unwrap().unwrap().snapshot.revision, 1);
}
#[test]
fn r2_identity_admission_substitution_refused() {
    let (r, mut s, j) = setup();
    let path = r.journal(0).join("admission");
    let bytes = fs::read(&path).unwrap();
    fs::rename(&path, r.0.join("observed-old-admission")).unwrap();
    fs::write(path, bytes).unwrap();
    let error = s.commit(&j, &snapshot(1, None), &mut pass).unwrap_err();
    assert_eq!(error.standing, Standing::NotCommitted);
    assert!(error.detail.contains("admission identity"));
    assert_eq!(fs::metadata(r.journal(0).join("A")).unwrap().len(), 0);
}
#[test]
fn r2_identity_resync_substitution_refused() {
    let (r, mut s, j) = setup();
    s.commit(&j, &snapshot(1, None), &mut pass).unwrap();
    drop(s);
    let mut s = Session::open_observed(&r.0, budget()).unwrap();
    let mut hook = |p| {
        if p == (Step::ConfirmReadback, Edge::Before) {
            let path = r.journal(0).join("A");
            let bytes = fs::read(&path).unwrap();
            fs::rename(&path, r.0.join("old-selected-snapshot")).unwrap();
            fs::write(path, bytes).unwrap();
        }
        Ok(())
    };
    assert!(s
        .confirm_existing(&mut hook)
        .unwrap_err()
        .detail
        .contains("file identity/metadata changed during resync"));
    assert!(s.commit(&j, &snapshot(1, None), &mut pass).is_err());
}
#[test]
fn r2_entry_budget_before_mutation() {
    let r = Root::new();
    let mut b = budget();
    b.entries = 5;
    let (mut s, _) = Session::initialize(&r.0, b, "constructed-ns", &mut pass).unwrap();
    let error = s
        .admit("constructed-journal", "constructed-undertaking", &mut pass)
        .unwrap_err();
    assert_eq!(error.standing, Standing::NoBootstrapOrAdmissionAttempt);
    assert!(!r.journal(0).exists());
    let r = Root::new();
    let mut b = budget();
    b.entries = 6;
    let (mut s, _) = Session::initialize(&r.0, b, "constructed-ns", &mut pass).unwrap();
    let j = s
        .admit("constructed-journal", "constructed-undertaking", &mut pass)
        .unwrap();
    let error = s.commit(&j, &snapshot(1, None), &mut pass).unwrap_err();
    assert!(error.attempt.is_none());
    assert!(!r.journal(0).join("descriptor.tmp").exists());
    assert_eq!(fs::metadata(r.journal(0).join("A")).unwrap().len(), 0);
    for limit in [7, 8] {
        let r = Root::new();
        let mut b = budget();
        b.entries = limit;
        let (mut s, _) = Session::initialize(&r.0, b, "constructed-ns", &mut pass).unwrap();
        let j = s
            .admit("constructed-journal", "constructed-undertaking", &mut pass)
            .unwrap();
        s.commit(&j, &snapshot(1, None), &mut pass).unwrap();
        let value = next(&s);
        let result = s.commit(&j, &value, &mut pass);
        if limit == 7 {
            assert!(result.unwrap_err().attempt.is_none());
            assert_eq!(s.observe(0).unwrap().unwrap().snapshot.revision, 1);
        } else {
            result.unwrap();
        }
    }
}
fn postreplace_admission_substitution(cut: Point) {
    let (r, mut s, j) = setup();
    s.commit(&j, &snapshot(1, None), &mut pass).unwrap();
    let value = next(&s);
    let path = r.journal(0).join("admission");
    let original = fs::read(&path).unwrap();
    let original_inode = fs::metadata(&path).unwrap().ino();
    let mut hook = |point| {
        if point == cut {
            fs::rename(&path, r.0.join("original-admission-after-replace")).unwrap();
            fs::write(&path, &original).unwrap();
            fs::set_permissions(&path, fs::Permissions::from_mode(0o600)).unwrap();
            assert_ne!(fs::metadata(&path).unwrap().ino(), original_inode);
            assert_eq!(fs::read(&path).unwrap(), original);
        }
        Ok(())
    };
    let result = s.commit(&j, &value, &mut hook);
    assert!(
        matches!(&result,Err(e)if e.standing==Standing::Uncertain),
        "{cut:?} must not confirm a substituted admission: {result:?}"
    );
    let error = result.unwrap_err();
    assert!(error.detail.contains("admission identity"));
    assert_eq!(error.attempt.as_ref().unwrap().revision, Some(2));
    assert!(r.0.join("original-admission-after-replace").exists());
    assert_eq!(fs::read(&path).unwrap(), original);
    assert!(s.commit(&j, &value, &mut pass).is_err());
    drop(s);
    let observed = Session::open_observed(&r.0, budget())
        .unwrap()
        .observe(0)
        .unwrap()
        .unwrap();
    assert_eq!(observed.snapshot.revision, 2);
    assert!(observed.original_acknowledgment.contains("Unavailable"));
}
#[test]
fn r2_postreplace_admission_directory_sync() {
    postreplace_admission_substitution((Step::CommitDirectorySync, Edge::After));
}
#[test]
fn r2_postreplace_admission_readback_before() {
    postreplace_admission_substitution((Step::CommitReadback, Edge::Before));
}
