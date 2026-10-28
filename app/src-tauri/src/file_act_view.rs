//! Read-only A4/A6/A7 claims, separate from decision-package A16 semantics.
//! Cold capture files are readable claims, never proof of native origin; a
//! capture counts only when sealed under a key this installation holds.
use crate::{
    act_policy::ContentIdentity,
    standing::{compare, CurrentContent, Lapse},
    util::{sha256_hex, FILE_IDENTITY_METHOD},
};
use serde_json::{json, Value};
use std::{
    collections::{HashMap, HashSet},
    path::Path,
};

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub(crate) struct FileSource {
    device: u64,
    inode: u64,
}
impl FileSource {
    fn of(metadata: &std::fs::Metadata) -> Self {
        use std::os::unix::fs::MetadataExt;
        Self {
            device: metadata.dev(),
            inode: metadata.ino(),
        }
    }
    pub(crate) fn directory_at(path: &Path) -> Result<Self, String> {
        crate::storage::check_path(path)?;
        let file = crate::records_index::open_directory(path).map_err(|e| e.to_string())?;
        let metadata = file.metadata().map_err(|e| e.to_string())?;
        let named = std::fs::symlink_metadata(path).map_err(|e| e.to_string())?;
        if !metadata.is_dir() || !named.is_dir() || Self::of(&metadata) != Self::of(&named) {
            return Err("Physical source directory changed during observation".into());
        }
        Ok(Self::of(&metadata))
    }
    pub(crate) fn at(path: &Path) -> Result<Self, String> {
        crate::storage::check_path(path)?;
        let file = crate::records_index::open_log(path).map_err(|e| e.to_string())?;
        let metadata = file.metadata().map_err(|e| e.to_string())?;
        if !metadata.is_file() {
            return Err("Not a regular source log".into());
        }
        let named = std::fs::symlink_metadata(path).map_err(|e| e.to_string())?;
        if !named.is_file() || Self::of(&metadata) != Self::of(&named) {
            return Err("Source file changed during observation".into());
        }
        Ok(Self::of(&metadata))
    }
}

fn bytes(root: &Path, path: &Path) -> Result<Vec<u8>, String> {
    observed_bytes(root, path)
        .map(|(bytes, _, _)| bytes)
        .map_err(|e| e.message)
}
struct ByteReadError {
    message: String,
    may_be_absent: bool,
}
impl From<String> for ByteReadError {
    fn from(message: String) -> Self {
        Self {
            message,
            may_be_absent: false,
        }
    }
}
impl From<&str> for ByteReadError {
    fn from(message: &str) -> Self {
        message.to_owned().into()
    }
}
impl ByteReadError {
    fn named_file(e: std::io::Error) -> Self {
        Self {
            may_be_absent: e.kind() == std::io::ErrorKind::NotFound,
            message: e.to_string(),
        }
    }
}
/// The stamp belongs to the opened bytes, after the same-file and final
/// named-file checks. A later re-stat could name a replacement's bytes.
fn observed_bytes(
    root: &Path,
    path: &Path,
) -> Result<(Vec<u8>, crate::records_index::Stamp, FileSource), ByteReadError> {
    use std::{io::Read, os::unix::fs::OpenOptionsExt};
    if !path.is_absolute()
        || !path.starts_with(root)
        || path == root
        || path.components().any(|c| {
            matches!(
                c,
                std::path::Component::ParentDir | std::path::Component::CurDir
            )
        })
    {
        return Err("Not a contained physical file reference".into());
    }
    crate::storage::check_path(root)?;
    crate::storage::check_path(path)?;
    if std::fs::canonicalize(root).map_err(|e| e.to_string())? != root {
        return Err("Alias refused".into());
    }
    if std::fs::canonicalize(path).map_err(ByteReadError::named_file)? != path {
        return Err("Alias refused".into());
    }
    let mut file = std::fs::OpenOptions::new()
        .read(true)
        .custom_flags(libc::O_NOFOLLOW | libc::O_NONBLOCK)
        .open(path)
        .map_err(ByteReadError::named_file)?;
    let before = file.metadata().map_err(|e| e.to_string())?;
    if !before.is_file() {
        return Err("Not a regular file".into());
    }
    let mut bytes = Vec::new();
    file.read_to_end(&mut bytes).map_err(|e| e.to_string())?;
    let after = file.metadata().map_err(|e| e.to_string())?;
    #[cfg(test)]
    capture_test_hook(path, CaptureReadStage::BeforeNamedCheck);
    crate::storage::check_path(path)?;
    let named = std::fs::metadata(path).map_err(|e| e.to_string())?;
    let stamp = crate::records_index::Stamp::of(&after);
    if crate::records_index::Stamp::of(&before) != stamp
        || stamp != crate::records_index::Stamp::of(&named)
    {
        return Err("File changed during observation".into());
    }
    Ok((bytes, stamp, FileSource::of(&after)))
}
/// Strict physical subject observation, shared with the explicit metadata
/// observer. Unlike a canonicalized alias, this is exactly the captured path.
pub(crate) fn current_content(root: &Path, path: &Path) -> crate::checkpoint_recorder::Current {
    use crate::checkpoint_recorder::Current;
    match observed_bytes(root, path) {
        Ok((bytes, _, _)) => Current::Present(sha256_hex(&bytes)),
        Err(error) if error.may_be_absent && subject_absent(root, path) => Current::Absent,
        Err(error) => Current::Unavailable(error.message),
    }
}
fn subject_absent(root: &Path, path: &Path) -> bool {
    path.is_absolute()
        && path.starts_with(root)
        && path != root
        && path.components().all(|c| {
            !matches!(
                c,
                std::path::Component::ParentDir | std::path::Component::CurDir
            )
        })
        && crate::storage::check_path(root).is_ok()
        && crate::storage::check_path(path).is_ok()
        && std::fs::symlink_metadata(path).is_err_and(|e| e.kind() == std::io::ErrorKind::NotFound)
}
fn identity(v: &Value) -> ContentIdentity {
    ContentIdentity {
        method: v["method"].as_str().unwrap_or("").into(),
        value: v["value"].as_str().unwrap_or("").into(),
    }
}
/// A missing capture is cacheable only when absence was observed relative to
/// an opened physical owning folder whose identity/stamp still matched its name.
/// Byte errors of any other kind do not acquire this absence proof.
fn stable_capture_absence(path: &Path) -> Option<crate::records_index::Stamp> {
    use std::{
        ffi::CString,
        os::{
            fd::AsRawFd,
            unix::{ffi::OsStrExt, fs::OpenOptionsExt},
        },
    };
    let folder = path.parent()?;
    crate::storage::check_path(folder).ok()?;
    if std::fs::canonicalize(folder).ok()? != folder {
        return None;
    }
    let directory = std::fs::OpenOptions::new()
        .read(true)
        .custom_flags(libc::O_NOFOLLOW | libc::O_NONBLOCK | libc::O_DIRECTORY)
        .open(folder)
        .ok()?;
    let before = directory.metadata().ok()?;
    if !before.is_dir() {
        return None;
    }
    let name = CString::new(path.file_name()?.as_bytes()).ok()?;
    let mut metadata = std::mem::MaybeUninit::<libc::stat>::uninit();
    let result = unsafe {
        libc::fstatat(
            directory.as_raw_fd(),
            name.as_ptr(),
            metadata.as_mut_ptr(),
            libc::AT_SYMLINK_NOFOLLOW,
        )
    };
    if result != -1 || std::io::Error::last_os_error().kind() != std::io::ErrorKind::NotFound {
        return None;
    }
    let after = directory.metadata().ok()?;
    crate::storage::check_path(folder).ok()?;
    let named = std::fs::symlink_metadata(folder).ok()?;
    let stamp = crate::records_index::Stamp::of(&after);
    if !named.is_dir()
        || crate::records_index::Stamp::of(&before) != stamp
        || stamp != crate::records_index::Stamp::of(&named)
    {
        return None;
    }
    Some(stamp)
}
pub(crate) struct CaptureWatch {
    pub path: std::path::PathBuf,
    pub stamp: Option<crate::records_index::Stamp>,
    /// Only a proved absence depends on its owning folder's unchanged stamp.
    pub absent_folder_stamp: Option<crate::records_index::Stamp>,
}
/// A capture read and the source actually attempted. Stable opened bytes can
/// be watched even when decoding or verification refuses them. A failed source
/// resolution or ambiguous byte observation must be retried; a specifically
/// proved absence can be watched in its checked physical owning folder.
pub(crate) struct CaptureRead {
    pub result: Result<Value, String>,
    pub watch: Option<CaptureWatch>,
    pub reusable: bool,
}
/// The one capture object a file act or decline record cites, read from the
/// capture store and schema-checked (SP-3, RS R-8). Shared with the checkpoint recorder.
pub(crate) fn capture(root: &Path, body: &Value) -> Result<Value, String> {
    observe_capture(root, body).result
}
pub(crate) fn observe_capture(root: &Path, body: &Value) -> CaptureRead {
    let mut watch = None;
    let mut reusable = false;
    let result = (|| {
        let refs = body["captureEvidence"]
            .as_array()
            .ok_or("Capture reference missing")?;
        if refs.len() != 1 {
            return Err("One original capture reference required".into());
        }
        let id = refs[0]["ref"].as_str().ok_or("Capture identity missing")?;
        #[cfg(test)]
        capture_test_hook(root, CaptureReadStage::BeforeResolve);
        let path = crate::storage::capture_path(root, id)?;
        let bytes = match observed_bytes(path.parent().ok_or("capture has no folder")?, &path) {
            Ok((bytes, stamp, _)) => {
                watch = Some(CaptureWatch {
                    path: path.clone(),
                    stamp: Some(stamp),
                    absent_folder_stamp: None,
                });
                reusable = true;
                bytes
            }
            Err(e) => {
                let absent_folder_stamp = e
                    .may_be_absent
                    .then(|| stable_capture_absence(&path))
                    .flatten();
                reusable = absent_folder_stamp.is_some();
                // An ambiguous failure's stamp is descriptive only. A proved
                // absence keeps None, never a later replacement's metadata.
                let stamp = if reusable {
                    None
                } else {
                    std::fs::symlink_metadata(&path)
                        .ok()
                        .map(|m| crate::records_index::Stamp::of(&m))
                };
                watch = Some(CaptureWatch {
                    path: path.clone(),
                    stamp,
                    absent_folder_stamp,
                });
                #[cfg(test)]
                if reusable {
                    capture_test_hook(&path, CaptureReadStage::AfterAbsenceRead);
                }
                return Err(e.message);
            }
        };
        #[cfg(test)]
        capture_test_hook(&path, CaptureReadStage::AfterFileRead);
        let capture: Value = serde_json::from_slice(&bytes).map_err(|e| e.to_string())?;
        crate::schema_validation::validate_capture(&capture)?;
        if capture["captureId"] != id {
            return Err("Capture identity mismatch".into());
        }
        // AAC §6.3 SEAL-C: only a capture sealed under a key this installation
        // holds is the App act control's capture (AAC §6.3 / EXEC §2.4–2.5, R-1).
        crate::capture_seal::verify(root, &capture)?;
        Ok(capture)
    })();
    CaptureRead {
        result,
        watch,
        reusable,
    }
}
#[cfg(test)]
#[derive(Clone, Copy, PartialEq, Eq)]
pub(crate) enum CaptureReadStage {
    BeforeResolve,
    BeforeNamedCheck,
    AfterFileRead,
    AfterAbsenceRead,
}
#[cfg(test)]
thread_local! {
    static CAPTURE_READ_HOOK: std::cell::RefCell<Option<(std::path::PathBuf, CaptureReadStage, Box<dyn FnOnce()>)>> = const { std::cell::RefCell::new(None) };
}
#[cfg(test)]
pub(crate) struct CaptureReadHookGuard;
#[cfg(test)]
impl Drop for CaptureReadHookGuard {
    fn drop(&mut self) {
        CAPTURE_READ_HOOK.with(|h| *h.borrow_mut() = None);
    }
}
#[cfg(test)]
pub(crate) fn capture_read_hook_for_test(
    path: &Path,
    stage: CaptureReadStage,
    hook: impl FnOnce() + 'static,
) -> CaptureReadHookGuard {
    CAPTURE_READ_HOOK.with(|h| *h.borrow_mut() = Some((path.to_path_buf(), stage, Box::new(hook))));
    CaptureReadHookGuard
}
#[cfg(test)]
fn capture_test_hook(path: &Path, stage: CaptureReadStage) {
    let hook = CAPTURE_READ_HOOK.with(|h| {
        let matches = h
            .borrow()
            .as_ref()
            .is_some_and(|(p, s, _)| p == path && *s == stage);
        matches.then(|| h.borrow_mut().take().unwrap().2)
    });
    if let Some(hook) = hook {
        hook();
    }
}
/// Whether a file act or decline record says what its capture says: kind,
/// choice, actor, subject, time and, for an act, content, scope, purpose and
/// direct capture. Shared with the checkpoint recorder.
pub(crate) fn corresponds(c: &Value, record: &Value) -> bool {
    let b = &record["body"];
    let decline = record["kind"] == "act_declined";
    let kind = if decline {
        &b["declinedKind"]
    } else {
        &b["actKind"]
    };
    c["actKind"] == *kind
        && c["choice"] == if decline { "decline" } else { "act" }
        && c["answers"].get("runId") == record.get("runId")
        && c["answers"].get("arrival") == if decline {b.get("arrival")}else{b["relations"].get("arrivalAnswered")}
        && c.get("requestRef") == if decline {b.get("requestRef")}else{b["relations"].get("requestRef")}
        // The add-once backlink, once present, names this record (AAC §5.2a).
        && c.get("recordId").is_none_or(|linked| *linked == record["recordId"])
        && if decline {
            c["actor"] == b["actor"] && c["boundSubject"] == b["subject"] && c["capturedAt"] == b["time"]
        } else {
            c["actor"] == b["decisionActor"]
                && c["boundSubject"] == b["boundSubject"]
                && c["boundContent"] == b["boundContent"]
                && c["scope"] == b["scope"]
                && c["purpose"] == b["purpose"]
                && c["capturedAt"] == b["captureTime"]
                && b["recordingMode"] == "direct capture"
        }
}
// Read one nonblocking regular-file snapshot; preserve RS sequence and partial-line
// limits before passing schema-readable claims to the shared correction projector.
fn read_log(
    root: &Path,
    path: &Path,
) -> (Vec<Value>, Vec<String>, Option<String>, Option<FileSource>) {
    let (data, _, source) = match observed_bytes(root, path) {
        Ok(snapshot) => snapshot,
        Err(e) => return (Vec::new(), vec![e.message], None, None),
    };
    // R-2 as RS §13.8 reads it: one entry or one group per line (a group
    // taken whole), each line linked to the one before; a torn line W-0
    // terminated and named is never read (and is not a chain link).
    let name = path.display().to_string();
    let parsed = crate::record_lines::parse(&data, &name, 0, 0, 1, Default::default());
    let mut entries = Vec::new();
    let mut limits = Vec::new();
    for line in parsed.lines {
        limits.extend(line.limits);
        entries.extend(line.entries);
    }
    let partial = parsed
        .partial_tail
        .map(|_| format!("{name}: partial final entry not read"));
    (entries, limits, partial, Some(source))
}
pub(crate) struct SourceClaims {
    pub claims: Vec<Value>,
    pub complete: HashSet<String>,
    pub limits: Vec<String>,
    pub files: HashMap<String, FileSource>,
    /// Non-tail source failures remain distinct from an owning writer's W-0
    /// tail. The read-only presentation still reports both in `limits`.
    pub incomplete: bool,
    pub partial_logs: HashSet<String>,
}
/// One nonblocking source read, retaining the physical log identity of the
/// bytes read. Readable duplicate copies remain distinct source claims.
pub(crate) fn source_claims(root: &Path) -> SourceClaims {
    let mut claims = Vec::new();
    let mut complete = HashSet::new();
    let mut limits = Vec::new();
    let mut files = HashMap::new();
    let mut incomplete = false;
    let mut partial_logs = HashSet::new();
    let paths = crate::storage::discover(root).unwrap_or_else(|e| {
        incomplete = true;
        limits.push(e);
        Vec::new()
    });
    for path in paths {
        if let Err(e) = crate::storage::check_path(&path) {
            incomplete = true;
            limits.push(e);
            continue;
        }
        // Contained in the project's records store subtree, or in the project.
        let base =
            crate::records_store::project_dir_of(&path).unwrap_or_else(|| root.to_path_buf());
        let (records, errors, partial, physical) = read_log(&base, &path);
        let log = path.to_string_lossy().into_owned();
        if let Some(physical) = physical {
            files.insert(log.clone(), physical);
        }
        if errors.is_empty() && partial.is_none() {
            complete.insert(log.clone());
        }
        incomplete |= !errors.is_empty();
        limits.extend(errors);
        if let Some(partial) = partial {
            partial_logs.insert(log.clone());
            limits.push(partial);
        }
        claims.extend(
            records
                .into_iter()
                .map(|record| json!({"source":{"log":log,"seq":record["seq"]},"record":record})),
        );
    }
    SourceClaims {
        claims,
        complete,
        limits,
        files,
        incomplete,
        partial_logs,
    }
}
pub(crate) fn read(root: &Path) -> Value {
    let source = source_claims(root);
    let SourceClaims {
        claims,
        complete,
        limits,
        ..
    } = &source;
    let relations =
        crate::decision_view::record_relations::project_from_read_claims(&claims, &complete);
    let mut rows = Vec::new();
    for claim in relations["claims"].as_array().into_iter().flatten() {
        let record = &claim["record"];
        let b = &record["body"];
        let decline = record["kind"] == "act_declined";
        let kind = if decline {
            &b["declinedKind"]
        } else {
            &b["actKind"]
        };
        if !(decline || record["kind"] == "human_act")
            || !matches!(kind.as_str(), Some("A4" | "A6" | "A7"))
        {
            continue;
        }
        let mut row_limits=vec!["identity not verified".to_owned(),"Readable record/capture claims do not verify native origin; a verified capture seal shows only that a holder of this App installation's key wrote the capture (AAC §6.3 SEAL-C); no professional certification".into()];
        let found = capture(root, b);
        let captured = found.as_ref().ok();
        if let Err(e) = &found {
            row_limits.push(e.clone());
        }
        let correspondence = captured.is_some_and(|c| corresponds(c, record));
        if !correspondence {
            row_limits.push(
                "Capture correspondence unavailable or differs; no evidenced current act derived"
                    .into(),
            );
        }
        let subject = if decline {
            b["subject"][0].clone()
        } else {
            b["boundSubject"][0].clone()
        };
        let bound = if decline {
            captured
                .map(|c| c["boundContent"][0].clone())
                .unwrap_or(Value::Null)
        } else {
            b["boundContent"][0].clone()
        };
        let path = Path::new(subject.as_str().unwrap_or(""));
        let observed = bytes(root, path);
        let current = observed.as_ref().ok().map(|bytes| ContentIdentity {
            method: FILE_IDENTITY_METHOD.into(),
            value: sha256_hex(bytes),
        });
        let history = crate::file_act_lapse::display_history(record, &source, &relations);
        let observed_lapse = history.claims.iter().any(|c| {
            matches!(
                c["record"]["body"]["state"].as_str(),
                Some("lapsed" | "lapsed (subject absent)" | "partially lapsed")
            )
        });
        let comparison = if bound["method"] != FILE_IDENTITY_METHOD {
            Lapse::Incomparable
        } else {
            compare(
                &identity(&bound),
                current
                    .as_ref()
                    .map(CurrentContent::Present)
                    .unwrap_or_else(|| {
                        if subject_absent(root, path) {
                            CurrentContent::Absent
                        } else {
                            CurrentContent::Unavailable
                        }
                    }),
                observed_lapse,
            )
        };
        let comparison_label = match comparison {
            Lapse::NotLapsed => {
                "current bytes match recorded identity; past lapse history not established"
            }
            Lapse::Lapsed => "lapsed comparison: current content differs",
            Lapse::Incomparable => "identity methods incomparable",
            Lapse::SubjectAbsent => "lapsed comparison: subject absent",
            Lapse::MatchesAgainAfterLapse => "matches c0 again after recorded lapse claim",
            _ => "current content unavailable; lapse unknown",
        };
        if let Err(e) = observed {
            row_limits.push(e);
        }
        let actor = if decline {
            b["actor"].clone()
        } else {
            b["decisionActor"].clone()
        };
        if *kind == "A7" && !decline {
            row_limits.push(
                "Professional standing is the person's own recorded statement; not verified".into(),
            );
        }
        rows.push(json!({"recordId":record["recordId"],"kind":kind,"event":if decline{"declined this act"}else{"recorded human-act claim"},"actor":actor,"recordedBy":record["recorder"],"subject":subject,"boundContent":bound,"scope":if decline{captured.map(|c|c["scope"].clone()).unwrap_or(Value::Null)}else{b["scope"].clone()},"purpose":if decline{captured.map(|c|c["purpose"].clone()).unwrap_or(Value::Null)}else{b["purpose"].clone()},"recordingMode":b["recordingMode"],"lapseHistoryClaims":history.claims,"lapseHistoryLimitedClaims":history.limited,"lapseHistoryLimits":history.limits,"captureCorrespondence":correspondence,"captureEvidence":b["captureEvidence"],"captureTime":if decline{b["time"].clone()}else{b["captureTime"].clone()},"comparison":comparison_label,"currentContent":current.map(|c|json!({"method":c.method,"value":c.value})),"source":claim["source"],"correctedBy":claim["correctedBy"],"identityResolution":claim["identityResolution"],"relationLimit":claim["relationLimit"],"limits":row_limits}));
    }
    json!({"view":"App file acts and declines; read-only source claims","rows":rows,"correctionGroups":relations["correctionGroups"],"diagnostics":relations["diagnostics"],"limits":limits,"standing":"Checking, engineering approval and professional reliance remain distinct; no acceptance, execution, request settlement or native provenance is inferred"})
}
#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn empty_reader_does_not_create_store() {
        let root = std::fs::canonicalize(std::env::temp_dir())
            .unwrap()
            .join(crate::util::opaque_id("file-reader-").unwrap());
        std::fs::create_dir(&root).unwrap();
        let result = read(&root);
        assert!(result["rows"].as_array().unwrap().is_empty());
        assert_eq!(std::fs::read_dir(&root).unwrap().count(), 0);
        std::fs::remove_dir(root).unwrap();
    }
    #[test]
    fn subject_reader_refuses_alias_and_outside() {
        let root = std::fs::canonicalize(std::env::temp_dir())
            .unwrap()
            .join(crate::util::opaque_id("file-reader-").unwrap());
        std::fs::create_dir(&root).unwrap();
        std::fs::write(root.join("a"), b"frozen").unwrap();
        std::os::unix::fs::symlink(root.join("a"), root.join("alias")).unwrap();
        assert!(bytes(&root, &root.join("alias")).is_err());
        assert!(bytes(&root, Path::new("/etc/hosts")).is_err());
        assert_eq!(bytes(&root, &root.join("a")).unwrap(), b"frozen");
        std::fs::remove_dir_all(root).unwrap();
    }
}
