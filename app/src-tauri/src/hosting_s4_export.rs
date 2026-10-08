// Test-only transport for the Group B synthetic consumer fixture.
use super::*;
use std::{
    collections::BTreeMap,
    fs,
    io::Write,
    os::unix::fs::{OpenOptionsExt, PermissionsExt},
};
fn hex(s: &str, n: usize) -> bool {
    s.len() == n
        && s.bytes()
            .all(|b| b.is_ascii_digit() || (b'a'..=b'f').contains(&b))
}
fn safe_path(s: &str) -> Result<(), String> {
    if s.is_empty()
        || s.starts_with('/')
        || s.contains('\\')
        || s.split('/').any(|p| p.is_empty() || p == "." || p == "..")
    {
        return Err("unsafe member path".into());
    }
    Ok(())
}
fn snapshot(root: &std::path::Path) -> Result<BTreeMap<String, Vec<u8>>, String> {
    let inventory = tree::scan(root)?;
    let mut files = BTreeMap::new();
    for entry in &inventory.entries {
        if entry.kind == "file" {
            safe_path(&entry.path)?;
            let bytes = fs::read(root.join(&entry.path)).map_err(|e| e.to_string())?;
            if Some(tree::digest(&bytes)) != entry.sha256 || Some(bytes.len() as u64) != entry.size
            {
                return Err("member changed while copying".into());
            }
            files.insert(entry.path.clone(), bytes);
        }
    }
    if tree::scan(root)? != inventory {
        return Err("source inventory changed".into());
    }
    Ok(files)
}
fn members(files: &BTreeMap<String, Vec<u8>>) -> Value {
    json!(files
        .iter()
        .map(|(path, raw)| json!({"path":path,"sha256":tree::digest(raw),"size":raw.len()}))
        .collect::<Vec<_>>())
}
fn exact(files: &BTreeMap<String, Vec<u8>>, r: &Value) -> Result<(), String> {
    let p = r["path"].as_str().ok_or("missing path")?;
    safe_path(p)?;
    let bytes = files.get(p).ok_or("missing member")?;
    if r["sha256"] != tree::digest(bytes) {
        return Err("member digest differs".into());
    }
    Ok(())
}
fn verify(
    read: &Value,
    files: &BTreeMap<String, Vec<u8>>,
    source: Option<&BTreeMap<String, Vec<u8>>>,
    lt09: &Value,
) -> Result<(), String> {
    if read["state"] != "read"
        || read["evidence"]["lifecycle"]["legacy_event"] != *lt09
        || lt09["transitionId"] != "LT-09"
    {
        return Err("successful actual read/LT09 required".into());
    }
    let e = &read["evidence"];
    let reference = &e["reference"];
    for (key, value) in [
        ("observed", &e["artifact"]),
        ("lifecycle", &e["lifecycle"]),
        ("transport", &e["transport"]),
    ] {
        exact(files, &reference[key])?;
        let raw = &files[reference[key]["path"].as_str().unwrap()];
        if serde_json::from_slice::<Value>(raw).map_err(|e| e.to_string())? != *value {
            return Err("readback bytes differ".into());
        }
    }
    let entries = e["transport"]["entries"]
        .as_array()
        .ok_or("entries absent")?;
    if files.len() != entries.len() + 1 {
        return Err("publication membership differs".into());
    }
    let mut declared = BTreeMap::new();
    for entry in entries {
        exact(files, entry)?;
        let p = entry["path"].as_str().unwrap();
        if declared.insert(p.to_owned(), files[p].clone()).is_some() {
            return Err("duplicate member".into());
        }
    }
    let selected: BTreeMap<_, _> = declared
        .into_iter()
        .filter(|(p, _)| !p.starts_with(".chirality-s1/"))
        .collect();
    match source {
        Some(source) if !e["transport"]["sourceAssociation"].is_null() && *source == selected => (),
        None if e["transport"]["sourceAssociation"].is_null() && selected.is_empty() => (),
        _ => return Err("selected source closure differs".into()),
    }
    Ok(())
}
fn write_files(root: &std::path::Path, files: &BTreeMap<String, Vec<u8>>) -> Result<(), String> {
    fs::create_dir(root).map_err(|e| e.to_string())?;
    fs::set_permissions(root, fs::Permissions::from_mode(0o700)).map_err(|e| e.to_string())?;
    for (path, bytes) in files {
        safe_path(path)?;
        let file = root.join(path);
        fs::create_dir_all(file.parent().unwrap()).map_err(|e| e.to_string())?;
        let mut fd = fs::OpenOptions::new()
            .write(true)
            .create_new(true)
            .mode(0o600)
            .custom_flags(libc::O_NOFOLLOW)
            .open(file)
            .map_err(|e| e.to_string())?;
        fd.write_all(bytes).map_err(|e| e.to_string())?;
    }
    Ok(())
}
fn export(
    host: &Host,
    g: &Value,
    data: &std::path::Path,
    source: Option<&std::path::Path>,
    output: &std::path::Path,
    producer: Value,
    candidate: Value,
) -> Result<(), String> {
    if !hex(producer["sourceRevision"].as_str().unwrap_or(""), 40)
        || !hex(
            producer["harnessExecutableSha256"].as_str().unwrap_or(""),
            64,
        )
        || candidate
            != json!({"revision":"INVENTED-S4-APP-REVISION","buildIdentity":"INVENTED-S4-APP-BUILD","standing":"invented-consumer-fixture"})
    {
        return Err("explicit fixture identity required".into());
    }
    let parent = output.parent().ok_or("output parent absent")?;
    let canonical = parent.canonicalize().map_err(|e| e.to_string())?;
    if canonical != parent
        || !(canonical.starts_with(
            std::env::temp_dir()
                .canonicalize()
                .map_err(|e| e.to_string())?,
        ) || canonical.starts_with("/private/tmp"))
    {
        return Err("output requires physical temporary parent".into());
    }
    safe_path(
        output
            .file_name()
            .and_then(|s| s.to_str())
            .ok_or("output name absent")?,
    )?;
    let read = host.distribution_evidence(g);
    if read["state"] != "read" {
        return Err("native held read unavailable".into());
    }
    let name = read["evidence"]["reference"]["publication"]
        .as_str()
        .ok_or("publication missing")?;
    safe_path(name)?;
    let files = snapshot(&data.join("runtime/distribution").join(name))?;
    let originals = source.map(snapshot).transpose()?;
    let lt09 = host
        .lifecycle_events()
        .into_iter()
        .find(|e| e["transitionId"] == "LT-09" && e["generation"] == *g)
        .ok_or("actual LT09 missing")?;
    verify(&read, &files, originals.as_ref(), &lt09)?;
    if host.distribution_evidence(g) != read {
        return Err("native read changed during export".into());
    }
    fs::create_dir(output).map_err(|e| e.to_string())?;
    fs::set_permissions(output, fs::Permissions::from_mode(0o700)).map_err(|e| e.to_string())?;
    write_files(&output.join("publication"), &files)?;
    if let Some(ref originals) = originals {
        write_files(&output.join("selected-source"), originals)?;
    }
    if snapshot(&output.join("publication"))? != files {
        return Err("export copy differs".into());
    }
    if let Some(ref originals) = originals {
        if snapshot(&output.join("selected-source"))? != *originals {
            return Err("original source copy differs".into());
        }
    }
    let exchange = json!({"format":"group-b-s1-reader-exchange.v1","case":if source.is_some(){"selected"}else{"unselected"},"readback":read,"actualLt09":lt09,"members":members(&files),"producer":producer,"applicationCandidate":candidate,"selectedSourceMembers":originals.as_ref().map(members)});
    let mut fd = fs::OpenOptions::new()
        .write(true)
        .create_new(true)
        .mode(0o600)
        .open(output.join("exchange.json"))
        .map_err(|e| e.to_string())?;
    fd.write_all(&serde_json::to_vec_pretty(&exchange).unwrap())
        .map_err(|e| e.to_string())?;
    Ok(())
}
fn inputs() -> (Value, Value) {
    let revision = std::process::Command::new("git")
        .args(["rev-parse", "HEAD"])
        .output()
        .unwrap();
    assert!(revision.status.success());
    let executable = std::env::current_exe().unwrap();
    let mut features = Vec::new();
    if cfg!(feature = "custom-protocol") {
        features.push("custom-protocol");
    }
    if cfg!(feature = "distribution-successor") {
        features.push("distribution-successor");
    }
    (
        json!({"sourceRevision":String::from_utf8(revision.stdout).unwrap().trim(),"harnessExecutableSha256":tree::digest(&fs::read(executable).unwrap()),"command":std::env::args().collect::<Vec<_>>(),"features":features,"kind":"synthetic-host-test"}),
        json!({"revision":"INVENTED-S4-APP-REVISION","buildIdentity":"INVENTED-S4-APP-BUILD","standing":"invented-consumer-fixture"}),
    )
}
#[test]
#[ignore = "explicit offline Group B fixture export; set CHIRALITY_S4_EXPORT_ROOT"]
fn export_group_b_s4_selected_and_unselected() {
    let root =
        PathBuf::from(std::env::var_os("CHIRALITY_S4_EXPORT_ROOT").expect("explicit output root"));
    // Caller creates the private parent; each case is exclusively created here.
    for selected in [false, true] {
        let f = Fixture::new("pass");
        let host = Arc::new(Host::new());
        let data = attach_selected_store(&host, &f, selected.then_some("reference/expected.json"));
        let ready = host.start(&f.cfg, "fixture").unwrap();
        let (producer, candidate) = inputs();
        let source = f.root.join("reference-source");
        let result = export(
            &host,
            &ready["generation"],
            &data,
            selected.then_some(source.as_path()),
            &root.join(if selected { "selected" } else { "unselected" }),
            producer,
            candidate,
        );
        host.stop("fixture", "export complete").unwrap();
        result.unwrap();
    }
}
#[test]
fn exporter_refuses_unavailable_existing_destination_and_tampered_bytes() {
    let f = Fixture::new("pass");
    let host = Arc::new(Host::new());
    let data = attach_store(&host, &f);
    let (producer, candidate) = inputs();
    let out = f.root.join("exchange");
    assert!(export(
        &host,
        &json!({}),
        &data,
        None,
        &out,
        producer.clone(),
        candidate.clone()
    )
    .is_err());
    assert!(!out.exists());
    let ready = host.start(&f.cfg, "fixture").unwrap();
    let g = &ready["generation"];
    export(
        &host,
        g,
        &data,
        None,
        &out,
        producer.clone(),
        candidate.clone(),
    )
    .unwrap();
    assert!(export(&host, g, &data, None, &out, producer, candidate).is_err());
    let read = host.distribution_evidence(g);
    let e: Value = serde_json::from_slice(&fs::read(out.join("exchange.json")).unwrap()).unwrap();
    let pristine = snapshot(&out.join("publication")).unwrap();
    let mut duplicate = read.clone();
    let entry = duplicate["evidence"]["transport"]["entries"][0].clone();
    duplicate["evidence"]["transport"]["entries"]
        .as_array_mut()
        .unwrap()
        .push(entry);
    assert!(verify(&duplicate, &pristine, None, &e["actualLt09"]).is_err());
    assert!(verify(&read, &pristine, Some(&pristine), &e["actualLt09"]).is_err());
    let mut wrong = read.clone();
    wrong["state"] = json!("unavailable");
    assert!(verify(&wrong, &pristine, None, &e["actualLt09"]).is_err());
    let mut files = pristine;
    files.values_mut().next().unwrap().push(0);
    assert!(verify(&read, &files, None, &e["actualLt09"]).is_err());
    host.stop("fixture", "negative export complete").unwrap();
    for p in ["", "/absolute", "a/../b", "a//b", "a\\b", "."] {
        assert!(safe_path(p).is_err());
    }
}
