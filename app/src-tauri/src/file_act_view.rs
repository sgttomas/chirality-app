//! Read-only A4/A6/A7 claims, separate from decision-package A16 semantics.
//! Cold capture files are readable claims, never proof of native origin.
use crate::{
    act_policy::ContentIdentity,
    standing::{compare, CurrentContent, Lapse},
    util::{sha256_hex, FILE_IDENTITY_METHOD},
};
use serde_json::{json, Value};
use std::{collections::HashSet, path::Path};

fn bytes(root: &Path, path: &Path) -> Result<Vec<u8>, String> {
    use std::{
        io::Read,
        os::unix::fs::{MetadataExt, OpenOptionsExt},
    };
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
    if std::fs::canonicalize(root).map_err(|e| e.to_string())? != root
        || std::fs::canonicalize(path).map_err(|e| e.to_string())? != path
    {
        return Err("Alias refused".into());
    }
    let mut file = std::fs::OpenOptions::new()
        .read(true)
        .custom_flags(libc::O_NOFOLLOW | libc::O_NONBLOCK)
        .open(path)
        .map_err(|e| e.to_string())?;
    let before = file.metadata().map_err(|e| e.to_string())?;
    if !before.is_file() {
        return Err("Not a regular file".into());
    }
    let mut bytes = Vec::new();
    file.read_to_end(&mut bytes).map_err(|e| e.to_string())?;
    let stamp = |m: &std::fs::Metadata| {
        (
            m.dev(),
            m.ino(),
            m.len(),
            m.mtime(),
            m.mtime_nsec(),
            m.ctime(),
            m.ctime_nsec(),
        )
    };
    let after = file.metadata().map_err(|e| e.to_string())?;
    crate::storage::check_path(path)?;
    let named = std::fs::metadata(path).map_err(|e| e.to_string())?;
    if stamp(&before) != stamp(&after) || stamp(&after) != stamp(&named) {
        return Err("File changed during observation".into());
    }
    Ok(bytes)
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
fn capture(root: &Path, body: &Value) -> Result<Value, String> {
    let refs = body["captureEvidence"]
        .as_array()
        .ok_or("Capture reference missing")?;
    if refs.len() != 1 {
        return Err("One original capture reference required".into());
    }
    let id = refs[0]["ref"].as_str().ok_or("Capture identity missing")?;
    let capture: Value =
        serde_json::from_slice(&bytes(root, &crate::storage::capture_path(root, id))?)
            .map_err(|e| e.to_string())?;
    crate::schema_validation::validate_capture(&capture)?;
    if capture["captureId"] != id {
        return Err("Capture identity mismatch".into());
    }
    Ok(capture)
}
// Read one nonblocking regular-file snapshot; preserve RS sequence and partial-line
// limits before passing schema-readable claims to the shared correction projector.
fn read_log(root: &Path, path: &Path) -> (Vec<Value>, Vec<String>) {
    let data = match bytes(root, path) {
        Ok(b) => b,
        Err(e) => return (Vec::new(), vec![e]),
    };
    let text = match std::str::from_utf8(&data) {
        Ok(t) => t,
        Err(e) => return (Vec::new(), vec![e.to_string()]),
    };
    let mut entries = Vec::new();
    let mut limits = Vec::new();
    let mut expected = 1u64;
    let count = text.lines().count();
    for (n, line) in text.lines().enumerate() {
        if line.trim().is_empty() {
            continue;
        }
        if n + 1 == count && !text.ends_with('\n') {
            limits.push(format!("{}: partial final entry not read", path.display()));
            continue;
        }
        match serde_json::from_str::<Value>(line) {
            Ok(v) => match crate::schema_validation::bundled()
                .and_then(|validator| validator.validate(&v))
            {
                Ok(()) => {
                    let seq = v["seq"].as_u64().unwrap();
                    if seq != expected {
                        limits.push(format!(
                            "{}: incomplete sequence at line {}",
                            path.display(),
                            n + 1
                        ));
                    }
                    expected = seq.saturating_add(1);
                    entries.push(v);
                }
                Err(e) => limits.push(e),
            },
            Err(e) => limits.push(e.to_string()),
        }
    }
    (entries, limits)
}
pub(crate) fn read(root: &Path) -> Value {
    let mut claims = Vec::new();
    let mut complete = HashSet::new();
    let mut limits = Vec::new();
    let paths = crate::storage::discover(root).unwrap_or_else(|e| {
        limits.push(e);
        Vec::new()
    });
    for path in paths {
        if let Err(e) = crate::storage::check_path(&path) {
            limits.push(e);
            continue;
        }
        let (records, errors) = read_log(root, &path);
        let log = path.to_string_lossy().into_owned();
        if errors.is_empty() {
            complete.insert(log.clone());
        }
        limits.extend(errors);
        claims.extend(
            records
                .into_iter()
                .map(|record| json!({"source":{"log":log,"seq":record["seq"]},"record":record})),
        );
    }
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
        let mut row_limits=vec!["identity not verified".to_owned(),"Readable record/capture claims do not verify native origin; no professional certification".into()];
        let found = capture(root, b);
        let captured = found.as_ref().ok();
        if let Err(e) = &found {
            row_limits.push(e.clone());
        }
        let correspondence = captured.is_some_and(|c| {
            c["actKind"] == *kind
                && c["choice"] == if decline { "decline" } else { "act" }
                && if decline {
                    c["actor"] == b["actor"]
                        && c["boundSubject"] == b["subject"]
                        && c["capturedAt"] == b["time"]
                } else {
                    c["actor"] == b["decisionActor"]
                        && c["boundSubject"] == b["boundSubject"]
                        && c["boundContent"] == b["boundContent"]
                        && c["scope"] == b["scope"]
                        && c["purpose"] == b["purpose"]
                        && c["capturedAt"] == b["captureTime"]
                        && b["recordingMode"] == "direct capture"
                }
        });
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
        let history: Vec<_> = relations["claims"]
            .as_array()
            .into_iter()
            .flatten()
            .filter(|candidate| {
                let e = &candidate["record"];
                let lb = &e["body"];
                let resolved = relations["correctionGroups"]
                    .as_array()
                    .into_iter()
                    .flatten()
                    .any(|group| {
                        group["sourceIncomplete"] == false
                            && group["currentCandidates"]
                                .as_array()
                                .is_some_and(|ids| ids.len() == 1 && ids[0] == e["recordId"])
                    });
                resolved
                    && e["kind"] == "act_lapsed"
                    && lb["act"]["recordId"] == record["recordId"]
                    && lb["act"]["actKind"] == *kind
                    && lb["referents"]
                        .as_array()
                        .is_some_and(|refs| refs.len() == 1 && refs[0] == subject)
                    && lb["c0"] == bound
                    && ((matches!(lb["state"].as_str(), Some("lapsed" | "partially lapsed"))
                        && lb["c1"]["method"] == bound["method"]
                        && lb["c1"]["value"].as_str().is_some_and(|v| !v.is_empty())
                        && lb["c1"] != bound)
                        || (lb["state"] == "lapsed (subject absent)"
                            && lb["c1"] == "subject absent"))
            })
            .cloned()
            .collect();
        let comparison = compare(
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
            !history.is_empty(),
        );
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
        rows.push(json!({"recordId":record["recordId"],"kind":kind,"event":if decline{"declined this act"}else{"recorded human-act claim"},"actor":actor,"recordedBy":record["recorder"],"subject":subject,"boundContent":bound,"scope":if decline{captured.map(|c|c["scope"].clone()).unwrap_or(Value::Null)}else{b["scope"].clone()},"purpose":if decline{captured.map(|c|c["purpose"].clone()).unwrap_or(Value::Null)}else{b["purpose"].clone()},"recordingMode":b["recordingMode"],"lapseHistoryClaims":history,"captureCorrespondence":correspondence,"captureEvidence":b["captureEvidence"],"captureTime":if decline{b["time"].clone()}else{b["captureTime"].clone()},"comparison":comparison_label,"currentContent":current.map(|c|json!({"method":c.method,"value":c.value})),"source":claim["source"],"correctedBy":claim["correctedBy"],"identityResolution":claim["identityResolution"],"relationLimit":claim["relationLimit"],"limits":row_limits}));
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
