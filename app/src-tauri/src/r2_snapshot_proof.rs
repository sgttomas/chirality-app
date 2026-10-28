//! R2-PROOF-01-B2. Included only by its integration test, never the App library.
#![cfg(all(test, any(target_os = "macos", target_os = "linux")))]
use serde::{
    de::{self, DeserializeSeed, SeqAccess, Visitor},
    Deserialize, Deserializer, Serialize,
};
use sha2::{Digest, Sha256};
use std::{
    ffi::{CStr, CString, OsStr},
    fmt,
    fs::{File, OpenOptions},
    io::{Read, Write},
    marker::PhantomData,
    os::{
        fd::{AsRawFd, FromRawFd, IntoRawFd},
        unix::{
            ffi::OsStrExt,
            fs::{MetadataExt, OpenOptionsExt},
        },
    },
    path::{Path, PathBuf},
    sync::atomic::{AtomicU64, Ordering},
};
const NS: &str = "r2-proof-fixture";
const VERSION: &str = "test-1";
const METHOD: &str = "sha256:original_r2_proof_fixture_bytes_v1";
const CONTROL: &str = "chirality.r2.proof-control";
const DESCRIPTOR: &str = "chirality.r2.proof-descriptor";
const SNAPSHOT: &str = "chirality.r2.proof-snapshot";
type Check<T> = Result<T, String>;
pub fn digest(bytes: &[u8]) -> String {
    format!("{:x}", Sha256::digest(bytes))
}
#[derive(Clone, Debug, Serialize)]
pub struct TestBudget {
    pub n: u64,
    pub s: u64,
    pub d: u64,
    pub t: u64,
    pub q: u64,
    pub artifacts: usize,
    pub refs: usize,
    pub entries: usize,
    pub members: usize,
    pub depth: usize,
    pub id: usize,
    pub text: usize,
}
impl TestBudget {
    pub fn reservation(&self) -> Check<u64> {
        let per = self
            .s
            .checked_mul(2)
            .and_then(|x| self.d.checked_mul(3).and_then(|d| x.checked_add(d)))
            .ok_or("reservation overflow")?;
        self.n
            .checked_mul(per)
            .and_then(|x| self.d.checked_mul(2).and_then(|d| x.checked_add(d)))
            .ok_or("reservation overflow".into())
    }
    pub fn validate(&self) -> Check<()> {
        let reserve = self.reservation()?;
        ensure(
            self.n > 0 && self.s > 0 && self.d > 0 && self.q > 0,
            "missing/zero test policy",
        )?;
        ensure(
            self.n <= 2 && self.s <= 32768 && self.d <= 4096 && self.q <= 262144 && self.t == 0,
            "outside downward-only test policy; no retirement",
        )?;
        for (v, max) in [
            (self.artifacts, 32),
            (self.refs, 64),
            (self.entries, 64),
            (self.members, 512),
            (self.depth, 16),
            (self.id, 128),
            (self.text, 16384),
        ] {
            ensure(v > 0 && v <= max, "invalid subordinate test bound")?;
        }
        ensure(
            self.entries >= 2,
            "namespace control/lock require two entries",
        )?;
        ensure(reserve <= self.q, "worst-case reservation exceeds Q")
    }
    fn policy(&self) -> Check<String> {
        Ok(digest(
            &serde_json::to_vec(self).map_err(|e| e.to_string())?,
        ))
    }
}
fn ensure(ok: bool, reason: &str) -> Check<()> {
    if ok {
        Ok(())
    } else {
        Err(reason.into())
    }
}
#[derive(Clone, Debug, PartialEq, Eq, Serialize)]
#[serde(transparent)]
pub struct List<T, const N: usize>(pub Vec<T>);
impl<'de, T: Deserialize<'de>, const N: usize> Deserialize<'de> for List<T, N> {
    fn deserialize<D: Deserializer<'de>>(d: D) -> Result<Self, D::Error> {
        struct Seed<T> {
            allowed: bool,
            p: PhantomData<T>,
        }
        impl<'de, T: Deserialize<'de>> DeserializeSeed<'de> for Seed<T> {
            type Value = T;
            fn deserialize<D: Deserializer<'de>>(self, d: D) -> Result<T, D::Error> {
                if !self.allowed {
                    return Err(de::Error::custom(
                        "sequence item limit before decoding next item",
                    ));
                }
                T::deserialize(d)
            }
        }
        struct V<T, const N: usize>(PhantomData<T>);
        impl<'de, T: Deserialize<'de>, const N: usize> Visitor<'de> for V<T, N> {
            type Value = List<T, N>;
            fn expecting(&self, f: &mut fmt::Formatter) -> fmt::Result {
                write!(f, "at most {N} items")
            }
            fn visit_seq<A: SeqAccess<'de>>(self, mut a: A) -> Result<Self::Value, A::Error> {
                let mut out = Vec::new();
                while let Some(v) = a.next_element_seed(Seed {
                    allowed: out.len() < N,
                    p: PhantomData,
                })? {
                    out.push(v);
                }
                Ok(List(out))
            }
        }
        d.deserialize_seq(V::<T, N>(PhantomData))
    }
}
pub type Refs = List<String, 64>;
#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct Control {
    pub format: String,
    pub version: String,
    pub method: String,
    pub kind: String,
    pub namespace: String,
    pub policy: String,
}
#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct Admission {
    pub format: String,
    pub version: String,
    pub method: String,
    pub kind: String,
    pub namespace: String,
    pub journal: String,
    pub undertaking: String,
    pub slot: u64,
    pub revision: u64,
    pub selected: Option<String>,
    pub reservation: u64,
    pub policy: String,
}
#[derive(Clone, Copy, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub enum Slot {
    A,
    B,
}
impl Slot {
    fn name(self) -> &'static str {
        match self {
            Self::A => "A",
            Self::B => "B",
        }
    }
    fn other(self) -> Self {
        match self {
            Self::A => Self::B,
            Self::B => Self::A,
        }
    }
}
#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct Descriptor {
    pub format: String,
    pub version: String,
    pub method: String,
    pub namespace: String,
    pub journal: String,
    pub revision: u64,
    pub slot: Slot,
    pub length: u64,
    pub sha256: String,
    pub previous: Option<String>,
    pub policy: String,
}
#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub enum ArtifactKind {
    ConstructedBase,
    ConstructedAnswer,
    ConstructedReview,
    InjectedIntent,
    InjectedUnknownOutcome,
    InjectedAccountReference,
    RecordedData,
}
#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct Artifact {
    pub id: String,
    pub kind: ArtifactKind,
    pub text: String,
    pub byte_length: u64,
    pub sha256: String,
}
impl Artifact {
    pub fn new(id: &str, kind: ArtifactKind, text: &str) -> Self {
        Self {
            id: id.into(),
            kind,
            text: text.into(),
            byte_length: text.len() as u64,
            sha256: digest(text.as_bytes()),
        }
    }
    fn capacity(&self) -> usize {
        self.id.capacity() + self.text.capacity() + self.sha256.capacity()
    }
}
#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub enum Status {
    ConstructedInProgress,
    ConstructedTerminal,
    ConstructedCancelled,
}
#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct InjectedFacts {
    pub intent: Option<String>,
    pub unknown_outcome: Option<String>,
    pub confirmed_account: Option<String>,
}
#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct Snapshot {
    pub format: String,
    pub version: String,
    pub method: String,
    pub namespace: String,
    pub journal: String,
    pub undertaking: String,
    pub revision: u64,
    pub previous: Option<String>,
    pub status: Status,
    pub gaps: Refs,
    pub artifacts: List<Artifact, 32>,
    pub required: Refs,
    pub unresolved_attempts: Refs,
    pub injected: InjectedFacts,
}
impl Snapshot {
    pub fn fixture(
        namespace: &str,
        journal: &str,
        undertaking: &str,
        revision: u64,
        previous: Option<String>,
        artifacts: Vec<Artifact>,
        required: Vec<String>,
    ) -> Self {
        Self {
            format: SNAPSHOT.into(),
            version: VERSION.into(),
            method: METHOD.into(),
            namespace: namespace.into(),
            journal: journal.into(),
            undertaking: undertaking.into(),
            revision,
            previous,
            status: Status::ConstructedInProgress,
            gaps: List(vec![
                "Constructed data; no live capability or original acknowledgment inferred".into(),
            ]),
            artifacts: List(artifacts),
            required: List(required),
            unresolved_attempts: List(vec![]),
            injected: InjectedFacts {
                intent: None,
                unknown_outcome: None,
                confirmed_account: None,
            },
        }
    }
    pub fn retained_capacity(&self) -> usize {
        std::mem::size_of::<Self>()
            + self.format.capacity()
            + self.version.capacity()
            + self.method.capacity()
            + self.namespace.capacity()
            + self.journal.capacity()
            + self.undertaking.capacity()
            + self.previous.as_ref().map_or(0, String::capacity)
            + self.artifacts.0.capacity() * std::mem::size_of::<Artifact>()
            + self
                .artifacts
                .0
                .iter()
                .map(Artifact::capacity)
                .sum::<usize>()
            + [&self.gaps.0, &self.required.0, &self.unresolved_attempts.0]
                .iter()
                .map(|v| {
                    v.capacity() * std::mem::size_of::<String>()
                        + v.iter().map(String::capacity).sum::<usize>()
                })
                .sum::<usize>()
            + [
                &self.injected.intent,
                &self.injected.unknown_outcome,
                &self.injected.confirmed_account,
            ]
            .iter()
            .map(|x| x.as_ref().map_or(0, String::capacity))
            .sum::<usize>()
    }
}
fn ident(s: &str, b: &TestBudget) -> Check<()> {
    ensure(
        !s.is_empty() && s.len() <= b.id && !s.contains('\0'),
        "identifier bound",
    )
}
fn hash(s: &str) -> Check<()> {
    ensure(
        s.len() == 64
            && s.bytes()
                .all(|x| x.is_ascii_digit() || (b'a'..=b'f').contains(&x)),
        "SHA256 spelling",
    )
}
fn header(f: &str, v: &str, m: &str, expected: &str) -> Check<()> {
    ensure(
        f == expected && v == VERSION && m == METHOD,
        "fixture format/version/method mismatch",
    )
}
fn refs(v: &Refs, b: &TestBudget) -> Check<()> {
    ensure(v.0.len() <= b.refs, "reference/issue count")?;
    for (i, x) in v.0.iter().enumerate() {
        ident(x, b)?;
        ensure(
            !v.0[..i].contains(x),
            "duplicate reference/attempt identity",
        )?;
    }
    Ok(())
}
fn validate_snapshot(s: &Snapshot, b: &TestBudget) -> Check<()> {
    header(&s.format, &s.version, &s.method, SNAPSHOT)?;
    for x in [&s.namespace, &s.journal, &s.undertaking] {
        ident(x, b)?;
    }
    ensure(s.revision > 0, "snapshot revision zero")?;
    if let Some(h) = &s.previous {
        hash(h)?;
    }
    ensure(
        (s.revision == 1) == s.previous.is_none(),
        "predecessor/revision mismatch",
    )?;
    ensure(
        s.artifacts.0.len() <= b.artifacts && s.gaps.0.len() <= b.refs,
        "artifact/gap count",
    )?;
    for g in &s.gaps.0 {
        ensure(!g.is_empty() && g.len() <= b.text, "gap text bound")?;
    }
    refs(&s.required, b)?;
    refs(&s.unresolved_attempts, b)?;
    for (i, a) in s.artifacts.0.iter().enumerate() {
        ident(&a.id, b)?;
        ensure(
            !s.artifacts.0[..i].iter().any(|x| x.id == a.id),
            "duplicate artifact ID",
        )?;
        ensure(
            a.text.len() <= b.text && a.text.len() as u64 == a.byte_length,
            "artifact decoded byte bound",
        )?;
        hash(&a.sha256)?;
        ensure(
            digest(a.text.as_bytes()) == a.sha256,
            "artifact bytes/hash mismatch",
        )?;
    }
    for id in &s.required.0 {
        ensure(
            s.artifacts.0.iter().any(|a| &a.id == id),
            "missing embedded required artifact; no slot/external resolver",
        )?;
    }
    for (id, kind) in [
        (&s.injected.intent, ArtifactKind::InjectedIntent),
        (
            &s.injected.unknown_outcome,
            ArtifactKind::InjectedUnknownOutcome,
        ),
        (
            &s.injected.confirmed_account,
            ArtifactKind::InjectedAccountReference,
        ),
    ] {
        if let Some(id) = id {
            ident(id, b)?;
            ensure(
                s.required.0.contains(id)
                    && s.artifacts.0.iter().any(|a| &a.id == id && a.kind == kind),
                "injected fact must reference matching required embedded constructed artifact",
            )?;
        }
    }
    Ok(())
}
fn successor(old: &Snapshot, new: &Snapshot) -> Check<()> {
    for id in &old.required.0 {
        ensure(new.required.0.contains(id), "required identity disappeared")?;
    }
    for id in &old.unresolved_attempts.0 {
        ensure(
            new.unresolved_attempts.0.contains(id),
            "uncertain attempt implicitly resolved",
        )?;
    }
    for a in &old.artifacts.0 {
        if let Some(n) = new.artifacts.0.iter().find(|n| n.id == a.id) {
            ensure(n == a, "artifact identity rebound")?;
        }
    }
    Ok(())
}
/// Nonallocating full-buffer structural budget; serde separately validates syntax.
pub fn scan(bytes: &[u8], depth_limit: usize, member_limit: usize) -> Check<usize> {
    let (mut quoted, mut escaped, mut depth, mut members) = (false, false, 0usize, 0usize);
    for &c in bytes {
        if quoted {
            if escaped {
                escaped = false;
            } else if c == b'\\' {
                escaped = true;
            } else if c == b'"' {
                quoted = false;
            }
            continue;
        }
        match c {
            b'"' => quoted = true,
            b'{' | b'[' => {
                depth = depth.checked_add(1).ok_or("depth overflow")?;
                ensure(depth <= depth_limit, "nesting bound")?;
            }
            b'}' | b']' => {
                depth = depth.checked_sub(1).ok_or("unbalanced structure")?;
            }
            b':' => {
                members = members.checked_add(1).ok_or("member overflow")?;
                ensure(members <= member_limit, "object member bound")?;
            }
            _ => {}
        }
    }
    ensure(!quoted && !escaped && depth == 0, "incomplete structure")?;
    Ok(members)
}
pub fn decode<T: for<'de> Deserialize<'de>>(bytes: &[u8], cap: u64, b: &TestBudget) -> Check<T> {
    ensure(bytes.len() as u64 <= cap, "raw codec bound")?;
    scan(bytes, b.depth, b.members)?;
    let mut d = serde_json::Deserializer::from_slice(bytes);
    let v = T::deserialize(&mut d).map_err(|e| e.to_string())?;
    d.end().map_err(|e| e.to_string())?;
    Ok(v)
}
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub struct Identity {
    pub device: u64,
    pub inode: u64,
}
fn identity(f: &File) -> Check<Identity> {
    let m = f.metadata().map_err(|e| e.to_string())?;
    Ok(Identity {
        device: m.dev(),
        inode: m.ino(),
    })
}
#[derive(PartialEq, Eq)]
struct Stamp {
    identity: Identity,
    length: u64,
    links: u64,
    mode: u32,
    mtime: i64,
    mtime_ns: i64,
    ctime: i64,
    ctime_ns: i64,
}
fn stamp(f: &File) -> Check<Stamp> {
    let m = f.metadata().map_err(|e| e.to_string())?;
    Ok(Stamp {
        identity: identity(f)?,
        length: m.len(),
        links: m.nlink(),
        mode: m.mode(),
        mtime: m.mtime(),
        mtime_ns: m.mtime_nsec(),
        ctime: m.ctime(),
        ctime_ns: m.ctime_nsec(),
    })
}
fn root_open(p: &Path) -> Check<File> {
    OpenOptions::new()
        .read(true)
        .custom_flags(libc::O_DIRECTORY | libc::O_NOFOLLOW | libc::O_CLOEXEC)
        .open(p)
        .map_err(|e| e.to_string())
}
fn at(parent: &File, name: &str, flags: i32) -> Check<File> {
    ensure(
        !name.is_empty() && !name.contains(['/', '\0']),
        "single component required",
    )?;
    let n = CString::new(name).unwrap();
    let fd = unsafe {
        libc::openat(
            parent.as_raw_fd(),
            n.as_ptr(),
            flags | libc::O_NOFOLLOW | libc::O_CLOEXEC | libc::O_NONBLOCK,
            0o600,
        )
    };
    if fd < 0 {
        Err(std::io::Error::last_os_error().to_string())
    } else {
        Ok(unsafe { File::from_raw_fd(fd) })
    }
}
fn directory(parent: &File, name: &str) -> Check<File> {
    at(parent, name, libc::O_RDONLY | libc::O_DIRECTORY)
}
fn mkdir(parent: &File, name: &str) -> Check<()> {
    let n = CString::new(name).unwrap();
    if unsafe { libc::mkdirat(parent.as_raw_fd(), n.as_ptr(), 0o700) } < 0 {
        return Err(std::io::Error::last_os_error().to_string());
    }
    Ok(())
}
fn regular(f: &File, cap: u64) -> Check<()> {
    let m = f.metadata().map_err(|e| e.to_string())?;
    ensure(
        m.is_file() && m.nlink() == 1,
        "regular single-link file required",
    )?;
    ensure(m.len() <= cap, "metadata byte limit")
}
fn exclusive(parent: &File, name: &str) -> Check<File> {
    let f = at(parent, name, libc::O_RDWR | libc::O_CREAT | libc::O_EXCL)?;
    regular(&f, 0)?;
    Ok(f)
}
fn sync(f: &File) -> Check<()> {
    f.sync_all()
        .map_err(|e| format!("test-fsync-v1 failed; no fallback: {e}"))
}
fn lock(f: &File) -> Check<()> {
    if unsafe { libc::flock(f.as_raw_fd(), libc::LOCK_EX | libc::LOCK_NB) } == 0 {
        return Ok(());
    }
    let e = std::io::Error::last_os_error();
    if matches!(e.raw_os_error(), Some(libc::EWOULDBLOCK)) {
        Err("Busy: independent exclusive reader/writer lock".into())
    } else {
        Err(format!("unsupported/failed flock: {e}"))
    }
}
fn names(dir: &File, limit: usize) -> Check<Vec<String>> {
    let fd = directory(dir, ".")?.into_raw_fd();
    let stream = unsafe { libc::fdopendir(fd) };
    if stream.is_null() {
        unsafe { libc::close(fd) };
        return Err(std::io::Error::last_os_error().to_string());
    }
    let result = (|| {
        let mut out = Vec::new();
        loop {
            #[cfg(target_os = "macos")]
            let errno = unsafe { libc::__error() };
            #[cfg(target_os = "linux")]
            let errno = unsafe { libc::__errno_location() };
            unsafe { *errno = 0 };
            let ent = unsafe { libc::readdir(stream) };
            if ent.is_null() {
                ensure(unsafe { *errno } == 0, "directory enumeration error")?;
                break;
            }
            let bytes = unsafe { CStr::from_ptr((*ent).d_name.as_ptr()) }.to_bytes();
            if bytes == b"." || bytes == b".." {
                continue;
            }
            ensure(
                out.len() < limit,
                "entry/issue bound before next allocation",
            )?;
            out.push(
                std::str::from_utf8(bytes)
                    .map_err(|_| "nonUTF8 unexpected entry")?
                    .to_owned(),
            );
        }
        Ok(out)
    })();
    let close = unsafe { libc::closedir(stream) };
    if close != 0 {
        return Err("directory close error".into());
    }
    result
}
/// Reads actual cap+sentinel, irrespective of preceding metadata. Exposed only in this private test module.
pub fn read_bounded(reader: impl Read, cap: u64) -> Check<Vec<u8>> {
    ensure(cap > 0 && cap <= 32768, "known fixture file cap required")?;
    let mut bytes = Vec::with_capacity((cap + 1) as usize);
    reader
        .take(cap.checked_add(1).ok_or("sentinel overflow")?)
        .read_to_end(&mut bytes)
        .map_err(|e| e.to_string())?;
    ensure(bytes.len() as u64 <= cap, "actual byte sentinel exceeded")?;
    Ok(bytes)
}
fn read_file(parent: &File, name: &str, cap: u64) -> Check<(Vec<u8>, Identity)> {
    read_file_with(parent, name, cap, || {})
}
pub fn read_file_with(
    parent: &File,
    name: &str,
    cap: u64,
    after_stat: impl FnOnce(),
) -> Check<(Vec<u8>, Identity)> {
    let file = at(parent, name, libc::O_RDONLY)?;
    regular(&file, cap)?;
    let before = file.metadata().map_err(|e| e.to_string())?;
    let id = identity(&file)?;
    after_stat();
    let bytes = read_bounded(&file, cap)?;
    let after = file.metadata().map_err(|e| e.to_string())?;
    regular(&file, cap)?;
    ensure(
        before.len() == after.len()
            && before.mtime() == after.mtime()
            && before.mtime_nsec() == after.mtime_nsec()
            && before.ctime() == after.ctime()
            && before.ctime_nsec() == after.ctime_nsec(),
        "file changed during read",
    )?;
    ensure(
        identity(&at(parent, name, libc::O_RDONLY)?)? == id,
        "entry changed during read",
    )?;
    Ok((bytes, id))
}
struct LimitedWriter<'a> {
    file: &'a mut File,
    cap: u64,
    count: u64,
    hash: Sha256,
}
impl Write for LimitedWriter<'_> {
    fn write(&mut self, b: &[u8]) -> std::io::Result<usize> {
        if self
            .count
            .checked_add(b.len() as u64)
            .is_none_or(|n| n > self.cap)
        {
            return Err(std::io::Error::other("stream serialization cap"));
        }
        let n = self.file.write(b)?;
        self.hash.update(&b[..n]);
        self.count += n as u64;
        Ok(n)
    }
    fn flush(&mut self) -> std::io::Result<()> {
        self.file.flush()
    }
}
fn write_exact<T: Serialize>(file: &mut File, v: &T, cap: u64) -> Check<(u64, String)> {
    let mut writer = LimitedWriter {
        file,
        cap,
        count: 0,
        hash: Sha256::new(),
    };
    serde_json::to_writer(&mut writer, v).map_err(|e| e.to_string())?;
    Ok((writer.count, format!("{:x}", writer.hash.finalize())))
}
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum Step {
    NamespaceMkdir,
    RootSync,
    LockCreate,
    LockSync,
    LockDirectorySync,
    ControlCreate,
    ControlWrite,
    ControlSync,
    ControlDirectorySync,
    ControlReadback,
    NamespaceAck,
    JournalMkdir,
    JournalParentSync,
    AdmissionCreate,
    AdmissionWrite,
    AdmissionSync,
    SlotACreate,
    SlotASync,
    SlotBCreate,
    SlotBSync,
    AdmissionDirectorySync,
    AdmissionParentSync,
    AdmissionReadback,
    AdmissionAck,
    InactiveWrite,
    InactiveSync,
    InactiveReadback,
    DescriptorCreate,
    DescriptorWrite,
    DescriptorSync,
    SelectionRecheck,
    DescriptorReplace,
    CommitDirectorySync,
    CommitReadback,
    CommitAck,
    ConfirmSync,
    ConfirmReadback,
}
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum Edge {
    Before,
    After,
}
pub type Point = (Step, Edge);
pub type Hook<'a> = dyn FnMut(Point) -> Check<()> + 'a;
fn step<T>(hook: &mut Hook<'_>, s: Step, operation: impl FnOnce() -> Check<T>) -> Check<T> {
    hook((s, Edge::Before))?;
    let value = operation()?;
    hook((s, Edge::After))?;
    Ok(value)
}
#[derive(Clone, Debug, PartialEq, Eq)]
pub enum Standing {
    NoBootstrapOrAdmissionAttempt,
    IncompleteOrUncertainBootstrap,
    IncompleteOrUncertainAdmission,
    NotCommitted,
    Uncertain,
}
#[derive(Clone, Debug)]
pub struct Attempt {
    pub identity: String,
    pub operation: &'static str,
    pub revision: Option<u64>,
}
fn attempt(operation: &'static str, revision: Option<u64>) -> Check<Attempt> {
    static NEXT: AtomicU64 = AtomicU64::new(1);
    let n = NEXT
        .fetch_update(Ordering::Relaxed, Ordering::Relaxed, |x| x.checked_add(1))
        .map_err(|_| "test attempt counter exhausted")?;
    Ok(Attempt {
        identity: format!("constructed-attempt-{n}"),
        operation,
        revision,
    })
}
#[derive(Clone, Debug)]
pub struct Failure {
    pub standing: Standing,
    pub attempt: Option<Attempt>,
    pub detail: String,
    pub observed_entries: Vec<String>,
}
fn failure(
    standing: Standing,
    attempt: Option<Attempt>,
    detail: String,
    dir: Option<&File>,
    limit: usize,
) -> Failure {
    let observed_entries = dir
        .map(|d| {
            names(d, limit)
                .unwrap_or_else(|e| vec![format!("observed enumeration unavailable: {e}")])
        })
        .unwrap_or_default();
    Failure {
        standing,
        attempt,
        detail,
        observed_entries,
    }
}
#[derive(Debug)]
pub struct NamespaceConfirmed {
    pub acknowledgment: &'static str,
}
#[derive(Clone, Debug)]
pub struct JournalConfirmed {
    pub index: u64,
    pub journal: String,
    pub undertaking: String,
    pub acknowledgment: &'static str,
    pub directory_identity: Identity,
    pub admission_identity: Identity,
    pub admission_sha256: String,
}
#[derive(Debug)]
pub struct CommitConfirmed {
    pub revision: u64,
    pub descriptor_sha256: String,
    pub acknowledgment: &'static str,
}
#[derive(Debug)]
pub struct SelectedStateObserved {
    pub snapshot: Snapshot,
    pub raw: Vec<u8>,
    pub descriptor: Descriptor,
    pub descriptor_sha256: String,
    pub descriptor_identity: Identity,
    pub snapshot_identity: Identity,
    pub original_acknowledgment: &'static str,
    pub freshness: &'static str,
}
#[derive(Debug)]
pub struct Session {
    path: PathBuf,
    root: File,
    namespace_dir: File,
    lock_file: File,
    root_id: Identity,
    ns_id: Identity,
    lock_id: Identity,
    control_id: Identity,
    control_sha: String,
    control: Control,
    budget: TestBudget,
    confirmed: bool,
    journals: Vec<u64>,
    blocked: bool,
}
fn exists(dir: &File, name: &str) -> Check<bool> {
    let n = CString::new(name).unwrap();
    let mut stat = std::mem::MaybeUninit::<libc::stat>::uninit();
    let rc = unsafe {
        libc::fstatat(
            dir.as_raw_fd(),
            n.as_ptr(),
            stat.as_mut_ptr(),
            libc::AT_SYMLINK_NOFOLLOW,
        )
    };
    if rc == 0 {
        Ok(true)
    } else {
        let e = std::io::Error::last_os_error();
        if e.raw_os_error() == Some(libc::ENOENT) {
            Ok(false)
        } else {
            Err(e.to_string())
        }
    }
}
fn slot_name(index: u64) -> Check<&'static str> {
    match index {
        0 => Ok("journal-0"),
        1 => Ok("journal-1"),
        _ => Err("fixture journal slot outside closed set".into()),
    }
}
fn validate_control(c: &Control, b: &TestBudget) -> Check<()> {
    header(&c.format, &c.version, &c.method, CONTROL)?;
    ensure(c.kind == "namespace", "wrong control kind")?;
    ident(&c.namespace, b)?;
    hash(&c.policy)?;
    ensure(c.policy == b.policy()?, "test policy identity changed")
}
fn validate_admission(a: &Admission, c: &Control, b: &TestBudget, index: u64) -> Check<()> {
    header(&a.format, &a.version, &a.method, CONTROL)?;
    ensure(
        a.kind == "admission"
            && a.namespace == c.namespace
            && a.policy == c.policy
            && a.slot == index
            && index < b.n
            && a.revision == 0
            && a.selected.is_none(),
        "admission identity/policy/revision mismatch",
    )?;
    ident(&a.journal, b)?;
    ident(&a.undertaking, b)?;
    ensure(
        a.reservation == b.s * 2 + b.d * 3,
        "admission reservation mismatch",
    )
}
fn validate_descriptor(d: &Descriptor, a: &Admission, b: &TestBudget) -> Check<()> {
    header(&d.format, &d.version, &d.method, DESCRIPTOR)?;
    ensure(
        d.namespace == a.namespace
            && d.journal == a.journal
            && d.policy == a.policy
            && d.revision > 0
            && d.length > 0
            && d.length <= b.s,
        "descriptor identity/revision/length mismatch",
    )?;
    hash(&d.sha256)?;
    if let Some(p) = &d.previous {
        hash(p)?;
    }
    ensure(
        (d.revision == 1) == d.previous.is_none(),
        "descriptor predecessor/revision mismatch",
    )
}
impl Session {
    pub fn initialize(
        path: &Path,
        budget: TestBudget,
        namespace: &str,
        hook: &mut Hook<'_>,
    ) -> Result<(Self, NamespaceConfirmed), Failure> {
        let pre = (|| {
            budget.validate()?;
            ident(namespace, &budget)?;
            ensure(
                path.is_absolute()
                    && !path
                        .components()
                        .any(|c| matches!(c, std::path::Component::ParentDir)),
                "explicit absolute fixture root required",
            )?;
            let path = path.to_path_buf();
            let root = root_open(&path)?;
            ensure(
                !exists(&root, NS)?,
                "existing namespace is occupied; no initialization fallback",
            )?;
            let id = identity(&root)?;
            let a = attempt("bootstrap", None)?;
            Ok((path, root, id, a))
        })();
        let (path, root, root_id, a) = pre.map_err(|e| {
            failure(
                Standing::NoBootstrapOrAdmissionAttempt,
                None,
                e,
                None,
                budget.entries,
            )
        })?;
        let mut attempted = false;
        let work = (|| -> Check<Self> {
            step(hook, Step::NamespaceMkdir, || {
                attempted = true;
                mkdir(&root, NS)
            })?;
            let namespace_dir = directory(&root, NS)?;
            let ns_id = identity(&namespace_dir)?;
            step(hook, Step::RootSync, || sync(&root))?;
            let lock_file = step(hook, Step::LockCreate, || exclusive(&namespace_dir, "lock"))?;
            lock(&lock_file)?;
            let lock_id = identity(&lock_file)?;
            step(hook, Step::LockSync, || sync(&lock_file))?;
            step(hook, Step::LockDirectorySync, || sync(&namespace_dir))?;
            let control = Control {
                format: CONTROL.into(),
                version: VERSION.into(),
                method: METHOD.into(),
                kind: "namespace".into(),
                namespace: namespace.into(),
                policy: budget.policy()?,
            };
            let mut file = step(hook, Step::ControlCreate, || {
                exclusive(&namespace_dir, "control")
            })?;
            let control_id = identity(&file)?;
            let (_, control_sha) = step(hook, Step::ControlWrite, || {
                write_exact(&mut file, &control, budget.d)
            })?;
            step(hook, Step::ControlSync, || sync(&file))?;
            step(hook, Step::ControlDirectorySync, || sync(&namespace_dir))?;
            step(hook, Step::ControlReadback, || {
                let (raw, id) = read_file(&namespace_dir, "control", budget.d)?;
                let parsed: Control = decode(&raw, budget.d, &budget)?;
                ensure(
                    parsed == control && id == control_id && digest(&raw) == control_sha,
                    "control readback mismatch",
                )
            })?;
            ensure(
                identity(&root_open(&path)?)? == root_id
                    && identity(&directory(&root, NS)?)? == ns_id
                    && identity(&at(&namespace_dir, "lock", libc::O_RDONLY)?)? == lock_id,
                "bootstrap entry identity changed",
            )?;
            regular(&lock_file, budget.d)?;
            regular(&file, budget.d)?;
            let entries = names(&namespace_dir, budget.entries)?;
            ensure(
                entries.len() == 2
                    && entries.iter().any(|x| x == "control")
                    && entries.iter().any(|x| x == "lock"),
                "unexpected namespace bootstrap set",
            )?;
            step(hook, Step::NamespaceAck, || Ok(()))?;
            Ok(Self {
                path: path.clone(),
                root: root.try_clone().map_err(|e| e.to_string())?,
                namespace_dir,
                lock_file,
                root_id,
                ns_id,
                lock_id,
                control_id,
                control_sha,
                control,
                budget: budget.clone(),
                confirmed: true,
                journals: vec![],
                blocked: false,
            })
        })();
        work.map(|s| {
            (
                s,
                NamespaceConfirmed {
                    acknowledgment: "NamespaceConfirmed: this completed bootstrap only",
                },
            )
        })
        .map_err(|e| {
            let ns = directory(&root, NS).ok();
            failure(
                if attempted {
                    Standing::IncompleteOrUncertainBootstrap
                } else {
                    Standing::NoBootstrapOrAdmissionAttempt
                },
                attempted.then_some(a),
                e,
                ns.as_ref(),
                budget.entries,
            )
        })
    }
    pub fn open_observed(path: &Path, budget: TestBudget) -> Result<Self, Failure> {
        let result = (|| -> Check<Self> {
            budget.validate()?;
            ensure(
                path.is_absolute()
                    && !path
                        .components()
                        .any(|c| matches!(c, std::path::Component::ParentDir)),
                "explicit absolute fixture root required",
            )?;
            let path = path.to_path_buf();
            let root = root_open(&path)?;
            let root_id = identity(&root)?;
            let namespace_dir = directory(&root, NS)?;
            let ns_id = identity(&namespace_dir)?;
            let lock_file = at(&namespace_dir, "lock", libc::O_RDWR)?;
            regular(&lock_file, budget.d)?;
            lock(&lock_file)?;
            let lock_id = identity(&lock_file)?;
            let (raw, control_id) = read_file(&namespace_dir, "control", budget.d)?;
            let control: Control = decode(&raw, budget.d, &budget)?;
            validate_control(&control, &budget)?;
            let session = Self {
                path,
                root,
                namespace_dir,
                lock_file,
                root_id,
                ns_id,
                lock_id,
                control_id,
                control_sha: digest(&raw),
                control,
                budget,
                confirmed: false,
                journals: vec![],
                blocked: false,
            };
            session.check()?;
            Ok(session)
        })();
        result.map_err(|e| {
            failure(
                Standing::NoBootstrapOrAdmissionAttempt,
                None,
                format!("cold state unresolved; original acknowledgment unavailable: {e}"),
                None,
                64,
            )
        })
    }
    fn check(&self) -> Check<()> {
        ensure(
            identity(&root_open(&self.path)?)? == self.root_id,
            "root entry identity changed",
        )?;
        ensure(
            identity(&directory(&self.root, NS)?)? == self.ns_id,
            "namespace entry identity changed",
        )?;
        let current = at(&self.namespace_dir, "lock", libc::O_RDWR)?;
        regular(&current, self.budget.d)?;
        ensure(
            identity(&current)? == self.lock_id && identity(&self.lock_file)? == self.lock_id,
            "stable lock entry substituted",
        )?;
        let (raw, id) = read_file(&self.namespace_dir, "control", self.budget.d)?;
        ensure(
            id == self.control_id && digest(&raw) == self.control_sha,
            "control identity/bytes changed",
        )?;
        let c: Control = decode(&raw, self.budget.d, &self.budget)?;
        validate_control(&c, &self.budget)?;
        ensure(c == self.control, "control mismatch")
    }
    fn inventory(&self) -> Check<Vec<Admission>> {
        self.check()?;
        let list = names(&self.namespace_dir, self.budget.entries)?;
        ensure(
            list.iter().any(|s| s == "lock") && list.iter().any(|s| s == "control"),
            "missing namespace control/lock",
        )?;
        let mut count = list.len();
        let mut bytes = 0u64;
        let mut admissions = Vec::new();
        for name in list {
            if name == "lock" || name == "control" {
                let f = at(&self.namespace_dir, &name, libc::O_RDONLY)?;
                regular(&f, self.budget.d)?;
                bytes = bytes
                    .checked_add(f.metadata().map_err(|e| e.to_string())?.len())
                    .ok_or("actual quota overflow")?;
                continue;
            }
            let index = match name.as_str() {
                "journal-0" => 0,
                "journal-1" => 1,
                _ => {
                    return Err(
                        "unknown namespace entry blocks accounting; never ignored/reclaimed".into(),
                    )
                }
            };
            ensure(
                index < self.budget.n,
                "journal exceeds N; occupied, not reusable",
            )?;
            let dir = directory(&self.namespace_dir, &name)?;
            let entries = names(&dir, self.budget.entries.saturating_sub(count))?;
            count = count
                .checked_add(entries.len())
                .ok_or("entry count overflow")?;
            ensure(count <= self.budget.entries, "namespace entry budget")?;
            for required in ["admission", "A", "B"] {
                ensure(
                    entries.iter().any(|x| x == required),
                    "incomplete journal admission blocks namespace",
                )?;
            }
            for entry in &entries {
                let cap = match entry.as_str() {
                    "admission" | "descriptor" | "descriptor.tmp" => self.budget.d,
                    "A" | "B" => self.budget.s,
                    _ => return Err("unknown/orphan journal entry blocks accounting".into()),
                };
                let f = at(&dir, entry, libc::O_RDONLY)?;
                regular(&f, cap)?;
                bytes = bytes
                    .checked_add(f.metadata().map_err(|e| e.to_string())?.len())
                    .ok_or("actual byte count overflow")?;
                ensure(bytes <= self.budget.q, "actual logical file bytes exceed Q")?;
            }
            let (raw, _) = read_file(&dir, "admission", self.budget.d)?;
            let a: Admission = decode(&raw, self.budget.d, &self.budget)?;
            validate_admission(&a, &self.control, &self.budget, index)?;
            ensure(
                !admissions
                    .iter()
                    .any(|x: &Admission| x.journal == a.journal || x.undertaking == a.undertaking),
                "duplicate journal/undertaking identity; no winner",
            )?;
            if entries.iter().any(|x| x == "descriptor") {
                let (raw, _) = read_file(&dir, "descriptor", self.budget.d)?;
                let d: Descriptor = decode(&raw, self.budget.d, &self.budget)?;
                validate_descriptor(&d, &a, &self.budget)?;
            }
            admissions.push(a);
        }
        ensure(bytes <= self.budget.q, "actual logical file bytes exceed Q")?;
        for known in &self.journals {
            ensure(
                admissions.iter().any(|a| a.slot == *known),
                "previously confirmed journal disappeared; no slot reuse",
            )?;
        }
        self.check()?;
        Ok(admissions)
    }
    fn reserve_entries(&self, additional: usize) -> Check<()> {
        let entries = names(&self.namespace_dir, self.budget.entries)?;
        let mut count = entries.len();
        for name in entries {
            match name.as_str() {
                "lock" | "control" => {}
                "journal-0" | "journal-1" => {
                    let dir = directory(&self.namespace_dir, &name)?;
                    count = count
                        .checked_add(names(&dir, self.budget.entries.saturating_sub(count))?.len())
                        .ok_or("entry reservation overflow")?;
                }
                _ => return Err("unknown namespace entry blocks reservation".into()),
            }
        }
        ensure(
            count
                .checked_add(additional)
                .is_some_and(|n| n <= self.budget.entries),
            "entry reservation would exceed bound before mutation",
        )
    }
    fn journal(&self, index: u64) -> Check<(File, Admission)> {
        let list = self.inventory()?;
        let admission = list
            .into_iter()
            .find(|a| a.slot == index)
            .ok_or("missing admitted journal")?;
        let dir = directory(&self.namespace_dir, slot_name(index)?)?;
        Ok((dir, admission))
    }
    fn selected(&self, dir: &File, a: &Admission) -> Check<Option<SelectedStateObserved>> {
        if !exists(dir, "descriptor")? {
            ensure(
                !exists(dir, "descriptor.tmp")?,
                "unacknowledged descriptor staging; no selected revision",
            )?;
            for slot in ["A", "B"] {
                let f = at(dir, slot, libc::O_RDONLY)?;
                regular(&f, 0)?;
            }
            return Ok(None);
        }
        let (raw, descriptor_identity) = read_file(dir, "descriptor", self.budget.d)?;
        let descriptor: Descriptor = decode(&raw, self.budget.d, &self.budget)?;
        validate_descriptor(&descriptor, a, &self.budget)?;
        let descriptor_sha256 = digest(&raw);
        drop(raw);
        let (raw, snapshot_identity) = read_file(dir, descriptor.slot.name(), self.budget.s)?;
        ensure(
            raw.len() as u64 == descriptor.length && digest(&raw) == descriptor.sha256,
            "selected snapshot raw bytes mismatch",
        )?;
        let snapshot: Snapshot = decode(&raw, self.budget.s, &self.budget)?;
        validate_snapshot(&snapshot, &self.budget)?;
        ensure(
            snapshot.namespace == a.namespace
                && snapshot.journal == a.journal
                && snapshot.undertaking == a.undertaking
                && snapshot.revision == descriptor.revision
                && snapshot.previous == descriptor.previous,
            "selected identity/revision/predecessor mismatch",
        )?;
        Ok(Some(SelectedStateObserved {
            snapshot,
            raw,
            descriptor,
            descriptor_sha256,
            descriptor_identity,
            snapshot_identity,
            original_acknowledgment:
                "Unavailable: SelectedStateObserved is not original confirmation or CAM custody",
            freshness:
                "Unproven without external freshness anchor; coherent rollback can look consistent",
        }))
    }
    pub fn observe(&self, index: u64) -> Result<Option<SelectedStateObserved>, Failure> {
        (self.journal(index).and_then(|(dir, a)| {
            let id = identity(&dir)?;
            let selected = self.selected(&dir, &a)?;
            self.check()?;
            ensure(
                identity(&directory(&self.namespace_dir, slot_name(index)?)?)? == id,
                "journal entry changed during read",
            )?;
            Ok(selected)
        }))
        .map_err(|e| {
            failure(
                Standing::NotCommitted,
                None,
                e,
                Some(&self.namespace_dir),
                self.budget.entries,
            )
        })
    }
    pub fn confirm_existing(
        &mut self,
        hook: &mut Hook<'_>,
    ) -> Result<(NamespaceConfirmed, Vec<JournalConfirmed>), Failure> {
        self.confirmed = false;
        // Retain known occupied slots even if a later confirmation fails.
        // A live failed attempt is not erased by observing matching bytes.
        let result = (|| -> Check<Vec<JournalConfirmed>> {
            let list = self.inventory()?;
            let mut confirmed = Vec::new();
            let mut sets = Vec::new();
            for a in &list {
                let dir = directory(&self.namespace_dir, slot_name(a.slot)?)?;
                let mut files = Vec::new();
                for name in names(&dir, self.budget.entries)? {
                    files.push((name.clone(), stamp(&at(&dir, &name, libc::O_RDONLY)?)?));
                }
                sets.push((a.slot, identity(&dir)?, files));
            }
            step(hook, Step::ConfirmSync, || {
                sync(&self.root)?;
                sync(&self.namespace_dir)?;
                sync(&self.lock_file)?;
                sync(&at(&self.namespace_dir, "control", libc::O_RDONLY)?)?;
                for a in &list {
                    let dir = directory(&self.namespace_dir, slot_name(a.slot)?)?;
                    ensure(
                        !exists(&dir, "descriptor.tmp")?,
                        "staging leftover blocks new confirmation; no repair",
                    )?;
                    self.selected(&dir, a)?;
                    for name in names(&dir, self.budget.entries)? {
                        sync(&at(&dir, &name, libc::O_RDONLY)?)?;
                    }
                    sync(&dir)?;
                }
                sync(&self.namespace_dir)
            })?;
            step(hook, Step::ConfirmReadback, || {
                self.check()?;
                let again = self.inventory()?;
                for (index, id, files) in &sets {
                    let dir = directory(&self.namespace_dir, slot_name(*index)?)?;
                    ensure(
                        identity(&dir)? == *id,
                        "journal identity changed during resync",
                    )?;
                    for (name, expected) in files {
                        ensure(
                            stamp(&at(&dir, name, libc::O_RDONLY)?)? == *expected,
                            "file identity/metadata changed during resync",
                        )?;
                    }
                }
                ensure(again == list, "admission changed during confirmation")?;
                for a in &again {
                    let dir = directory(&self.namespace_dir, slot_name(a.slot)?)?;
                    self.selected(&dir, a)?;
                    let (raw, admission_identity) = read_file(&dir, "admission", self.budget.d)?;
                    confirmed.push(JournalConfirmed{index:a.slot,journal:a.journal.clone(),undertaking:a.undertaking.clone(),directory_identity:identity(&dir)?,admission_identity,admission_sha256:digest(&raw),acknowledgment:"New current confirmation only; original admission acknowledgment unknown"});
                }
                Ok(())
            })?;
            Ok(confirmed)
        })();
        result.map(|journals|{self.confirmed=true;self.journals=journals.iter().map(|a|a.index).collect();(NamespaceConfirmed{acknowledgment:"New current confirmation only; original bootstrap/attempt acknowledgment unknown"},journals)}).map_err(|e|failure(Standing::NoBootstrapOrAdmissionAttempt,None,format!("confirm-existing refused without entry repair: {e}"),Some(&self.namespace_dir),self.budget.entries))
    }
    pub fn admit(
        &mut self,
        journal: &str,
        undertaking: &str,
        hook: &mut Hook<'_>,
    ) -> Result<JournalConfirmed, Failure> {
        let pre = (|| {
            ensure(
                self.confirmed && !self.blocked,
                "current confirmed namespace required",
            )?;
            ident(journal, &self.budget)?;
            ident(undertaking, &self.budget)?;
            let list = self.inventory()?;
            self.reserve_entries(4)?; // Journal directory, admission and two placeholders.
            ensure(
                !list
                    .iter()
                    .any(|a| a.journal == journal || a.undertaking == undertaking),
                "journal/undertaking identity occupied",
            )?;
            let index = (0..self.budget.n)
                .find(|i| !list.iter().any(|a| a.slot == *i))
                .ok_or("N capacity occupied; no retirement/reuse")?;
            ensure(self.budget.reservation()? <= self.budget.q, "Q reservation")?;
            Ok((index, attempt("admission", None)?))
        })();
        let (index, a) = pre.map_err(|e| {
            failure(
                Standing::NoBootstrapOrAdmissionAttempt,
                None,
                e,
                Some(&self.namespace_dir),
                self.budget.entries,
            )
        })?;
        let mut attempted = false;
        let mut observed_dir = None;
        let result = (|| -> Check<JournalConfirmed> {
            step(hook, Step::JournalMkdir, || {
                attempted = true;
                mkdir(&self.namespace_dir, slot_name(index)?)
            })?;
            let dir = directory(&self.namespace_dir, slot_name(index)?)?;
            let dir_id = identity(&dir)?;
            observed_dir = Some(dir.try_clone().map_err(|e| e.to_string())?);
            step(hook, Step::JournalParentSync, || sync(&self.namespace_dir))?;
            let admission = Admission {
                format: CONTROL.into(),
                version: VERSION.into(),
                method: METHOD.into(),
                kind: "admission".into(),
                namespace: self.control.namespace.clone(),
                journal: journal.into(),
                undertaking: undertaking.into(),
                slot: index,
                revision: 0,
                selected: None,
                reservation: self.budget.s * 2 + self.budget.d * 3,
                policy: self.control.policy.clone(),
            };
            let mut file = step(hook, Step::AdmissionCreate, || exclusive(&dir, "admission"))?;
            let admission_id = identity(&file)?;
            let (_, admission_sha) = step(hook, Step::AdmissionWrite, || {
                write_exact(&mut file, &admission, self.budget.d)
            })?;
            step(hook, Step::AdmissionSync, || sync(&file))?;
            let a = step(hook, Step::SlotACreate, || exclusive(&dir, "A"))?;
            let a_id = identity(&a)?;
            step(hook, Step::SlotASync, || sync(&a))?;
            let b = step(hook, Step::SlotBCreate, || exclusive(&dir, "B"))?;
            let b_id = identity(&b)?;
            step(hook, Step::SlotBSync, || sync(&b))?;
            ensure(
                !exists(&dir, "descriptor")? && !exists(&dir, "descriptor.tmp")?,
                "unexpected first descriptor",
            )?;
            step(hook, Step::AdmissionDirectorySync, || sync(&dir))?;
            step(hook, Step::AdmissionParentSync, || {
                sync(&self.namespace_dir)
            })?;
            step(hook, Step::AdmissionReadback, || {
                self.check()?;
                ensure(
                    identity(&directory(&self.namespace_dir, slot_name(index)?)?)? == dir_id,
                    "journal directory changed",
                )?;
                let names = names(&dir, self.budget.entries)?;
                ensure(
                    names.len() == 3
                        && ["admission", "A", "B"]
                            .iter()
                            .all(|x| names.iter().any(|n| n == x)),
                    "incomplete/unexpected initial set",
                )?;
                let (raw, id) = read_file(&dir, "admission", self.budget.d)?;
                let parsed: Admission = decode(&raw, self.budget.d, &self.budget)?;
                ensure(
                    parsed == admission && id == admission_id && digest(&raw) == admission_sha,
                    "admission readback mismatch",
                )?;
                for (name, id) in [("A", a_id), ("B", b_id)] {
                    let (bytes, actual) = read_file(&dir, name, self.budget.s)?;
                    ensure(
                        bytes.is_empty() && id == actual,
                        "placeholder changed/nonempty",
                    )?;
                }
                self.inventory()?;
                Ok(())
            })?;
            step(hook, Step::AdmissionAck, || Ok(()))?;
            Ok(JournalConfirmed {
                index,
                journal: journal.into(),
                undertaking: undertaking.into(),
                acknowledgment: "AdmissionConfirmed: this completed admission only",
                directory_identity: dir_id,
                admission_identity: admission_id,
                admission_sha256: admission_sha,
            })
        })();
        match result {
            Ok(receipt) => {
                self.journals.push(index);
                Ok(receipt)
            }
            Err(e) => {
                if attempted {
                    self.blocked = true;
                }
                Err(failure(
                    if attempted {
                        Standing::IncompleteOrUncertainAdmission
                    } else {
                        Standing::NoBootstrapOrAdmissionAttempt
                    },
                    attempted.then_some(a),
                    e,
                    observed_dir.as_ref().or(Some(&self.namespace_dir)),
                    self.budget.entries,
                ))
            }
        }
    }
    fn check_admission(&self, dir: &File, journal: &JournalConfirmed) -> Check<()> {
        let (raw, id) = read_file(dir, "admission", self.budget.d)?;
        ensure(
            identity(dir)? == journal.directory_identity
                && id == journal.admission_identity
                && digest(&raw) == journal.admission_sha256,
            "confirmed admission identity/bytes changed",
        )
    }
    pub fn commit(
        &mut self,
        journal: &JournalConfirmed,
        new: &Snapshot,
        hook: &mut Hook<'_>,
    ) -> Result<CommitConfirmed, Failure> {
        let pre = (|| -> Check<_> {
            ensure(
                self.confirmed && !self.blocked && self.journals.contains(&journal.index),
                "current namespace/admission confirmation required; no retry after error",
            )?;
            let (dir, a) = self.journal(journal.index)?;
            ensure(
                a.journal == journal.journal && a.undertaking == journal.undertaking,
                "admission receipt differs",
            )?;
            self.check_admission(&dir, journal)?;
            ensure(
                !exists(&dir, "descriptor.tmp")?,
                "descriptor staging occupied; no automatic unlink/retry",
            )?;
            self.reserve_entries(1)?; // Exclusive temporary; rename adds no further entry.
            let old = self.selected(&dir, &a)?;
            let revision = old
                .as_ref()
                .map_or(0, |o| o.descriptor.revision)
                .checked_add(1)
                .ok_or("revision overflow")?;
            let previous = old.as_ref().map(|o| o.descriptor_sha256.clone());
            let previous_identity = old.as_ref().map(|o| o.descriptor_identity);
            let inactive = old.as_ref().map_or(Slot::A, |o| o.descriptor.slot.other());
            validate_snapshot(new, &self.budget)?;
            ensure(
                new.namespace == a.namespace
                    && new.journal == a.journal
                    && new.undertaking == a.undertaking
                    && new.revision == revision
                    && new.previous == previous,
                "new snapshot identity/revision/predecessor differs",
            )?;
            if let Some(old) = old {
                successor(&old.snapshot, new)?;
            }
            let dir_id = identity(&dir)?;
            Ok((
                dir,
                a,
                dir_id,
                revision,
                previous,
                previous_identity,
                inactive,
                attempt("snapshot", Some(revision))?,
            ))
        })();
        let (dir, admission, dir_id, revision, previous, previous_identity, inactive, a) = pre
            .map_err(|e| {
                failure(
                    Standing::NotCommitted,
                    None,
                    e,
                    Some(&self.namespace_dir),
                    self.budget.entries,
                )
            })?;
        let (mut attempted, mut replacing) = (false, false);
        let result = (|| -> Check<CommitConfirmed> {
            let mut file = at(&dir, inactive.name(), libc::O_RDWR)?;
            regular(&file, self.budget.s)?;
            let file_id = identity(&file)?;
            let (length, sha256) = step(hook, Step::InactiveWrite, || {
                attempted = true;
                file.set_len(0).map_err(|e| e.to_string())?;
                write_exact(&mut file, new, self.budget.s)
            })?;
            step(hook, Step::InactiveSync, || sync(&file))?;
            step(hook, Step::InactiveReadback, || {
                let (raw, id) = read_file(&dir, inactive.name(), self.budget.s)?;
                ensure(
                    id == file_id && raw.len() as u64 == length && digest(&raw) == sha256,
                    "inactive readback bytes differ",
                )?;
                let parsed: Snapshot = decode(&raw, self.budget.s, &self.budget)?;
                validate_snapshot(&parsed, &self.budget)?;
                ensure(&parsed == new, "inactive readback semantic mismatch")
            })?;
            let descriptor = Descriptor {
                format: DESCRIPTOR.into(),
                version: VERSION.into(),
                method: METHOD.into(),
                namespace: admission.namespace.clone(),
                journal: admission.journal.clone(),
                revision,
                slot: inactive,
                length,
                sha256,
                previous: previous.clone(),
                policy: admission.policy.clone(),
            };
            let mut temporary = step(hook, Step::DescriptorCreate, || {
                exclusive(&dir, "descriptor.tmp")
            })?;
            let tmp_id = identity(&temporary)?;
            let (_, descriptor_sha256) = step(hook, Step::DescriptorWrite, || {
                write_exact(&mut temporary, &descriptor, self.budget.d)
            })?;
            step(hook, Step::DescriptorSync, || sync(&temporary))?;
            step(hook, Step::SelectionRecheck, || {
                self.check()?;
                ensure(
                    identity(&directory(&self.namespace_dir, slot_name(journal.index)?)?)?
                        == dir_id,
                    "journal entry changed",
                )?;
                ensure(
                    identity(&at(&dir, "descriptor.tmp", libc::O_RDONLY)?)? == tmp_id,
                    "descriptor temporary substituted",
                )?;
                if let Some(expected) = &previous {
                    let (raw, old_identity) = read_file(&dir, "descriptor", self.budget.d)?;
                    ensure(
                        Some(old_identity) == previous_identity,
                        "old descriptor identity substituted",
                    )?;
                    ensure(
                        digest(&raw) == *expected,
                        "old descriptor changed before replacement",
                    )?;
                } else {
                    ensure(
                        !exists(&dir, "descriptor")?,
                        "unexpected descriptor before first commit",
                    )?;
                }
                self.check_admission(&dir, journal)?;
                ensure(
                    identity(&at(&dir, inactive.name(), libc::O_RDONLY)?)? == file_id,
                    "inactive slot identity substituted",
                )?;
                let inventory = self.inventory()?;
                ensure(
                    inventory.iter().any(|x| x == &admission),
                    "admission changed before replacement",
                )
            })?;
            step(hook, Step::DescriptorReplace, || {
                replacing = true;
                let from = CString::new("descriptor.tmp").unwrap();
                let to = CString::new("descriptor").unwrap();
                if unsafe {
                    libc::renameat(dir.as_raw_fd(), from.as_ptr(), dir.as_raw_fd(), to.as_ptr())
                } < 0
                {
                    return Err(std::io::Error::last_os_error().to_string());
                }
                Ok(())
            })?;
            step(hook, Step::CommitDirectorySync, || sync(&dir))?;
            step(hook, Step::CommitReadback, || {
                self.check()?;
                ensure(
                    identity(&directory(&self.namespace_dir, slot_name(journal.index)?)?)?
                        == dir_id,
                    "journal entry changed after replace",
                )?;
                let observed = self
                    .selected(&dir, &admission)?
                    .ok_or("missing selected snapshot")?;
                ensure(
                    observed.descriptor == descriptor
                        && observed.descriptor_identity == tmp_id
                        && observed.snapshot_identity == file_id
                        && observed.descriptor_sha256 == descriptor_sha256
                        && &observed.snapshot == new,
                    "post-replacement exact readback differs",
                )?;
                // The immutable admission may have been replaced after selection recheck.
                // Revalidate its held identity/hash before acknowledging this attempt.
                self.check_admission(&dir, journal)
            })?;
            step(hook, Step::CommitAck, || Ok(()))?;
            Ok(CommitConfirmed{revision,descriptor_sha256,acknowledgment:"Confirmed: selected test-fsync-v1 checks completed; no power-loss or actor guarantee"})
        })();
        match result {
            Ok(receipt) => Ok(receipt),
            Err(e) => {
                if attempted {
                    self.blocked = true;
                }
                Err(failure(
                    if replacing {
                        Standing::Uncertain
                    } else {
                        Standing::NotCommitted
                    },
                    attempted.then_some(a),
                    e,
                    Some(&dir),
                    self.budget.entries,
                ))
            }
        }
    }
    pub fn retained_capacity(&self) -> usize {
        std::mem::size_of::<Self>()
            + self.path.capacity()
            + self.control_sha.capacity()
            + self.control.format.capacity()
            + self.control.version.capacity()
            + self.control.method.capacity()
            + self.control.kind.capacity()
            + self.control.namespace.capacity()
            + self.control.policy.capacity()
            + self.journals.capacity() * std::mem::size_of::<u64>()
    }
}
