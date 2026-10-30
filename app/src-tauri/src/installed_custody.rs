//! Process-local installed-integrity observation for the explicitly selected S1 route.
//! Serialized observations are evidence, never a constructor of live authority.
//! No signing identity is selected by this implementation.
use serde_json::{json, Value};
use sha2::{Digest, Sha256};
use std::path::Path;

/// Owner selection must bind the production bundle identifier AND publisher to an
/// independent certificate anchor. Never use the running App's designated requirement,
/// an environment value, resource, configuration, or caller-supplied requirement.
pub(crate) const COMPILED_PUBLISHER_REQUIREMENT: Option<&str> = None;
pub(crate) const STATIC_VALIDATION_FLAGS: u32 = (1 << 29) | 1 | (1 << 3) | (1 << 4);
pub(crate) const DYNAMIC_VALIDATION_FLAGS: u32 = 1 << 29;
const OBSERVER: &str = "macos-security-framework.s4.v1";
const LIMITS: [&str; 5] = [
    "Validation assumes a trusted stable installed bundle and parent path; parent writability is not checked and hostile same-user or administrator mutation remains possible",
    "Checks are bounded observations, not an atomic snapshot or an immutable check-to-exec guarantee",
    "No App Management protection, quarantine, notarization, Gatekeeper, revocation or installation witness is established",
    "Nested code is checked in Security.framework standard locations; other sealed resources are checked as resources",
    "Signing information including dynamic signature flags is disk-backed; running-process assurance comes from SecCodeCheckValidity against the compiled requirement",
];
fn digest(bytes: &[u8]) -> String {
    format!("{:x}", Sha256::digest(bytes))
}

/// Fields are private, and there is deliberately no Deserialize implementation.
#[derive(Debug)]
pub(crate) struct InstalledCustody {
    facts: Value,
    #[cfg(test)]
    synthetic_snapshot: Option<String>,
}
impl InstalledCustody {
    pub(crate) fn evidence(&self) -> Value {
        self.facts.clone()
    }

    /// Fresh validation immediately before spawn; never reload a serialized observation.
    pub(crate) fn recheck(&self, resources: &Path) -> Result<Self, String> {
        #[cfg(test)]
        if let Some(expected) = &self.synthetic_snapshot {
            let actual = synthetic_for_tests(resources)?;
            if actual.synthetic_snapshot.as_ref() != Some(expected) || actual.facts != self.facts {
                return Err("synthetic installed bundle changed before spawn".into());
            }
            return Ok(actual);
        }
        let current = observe(resources)?;
        if current.facts != self.facts {
            return Err("installed App signing or location facts changed before spawn".into());
        }
        Ok(current)
    }
}

/// `resources` is a placement assertion, compared to the independently resolved
/// running App. It never selects the bundle or publisher checked by Security.
pub(crate) fn observe(resources: &Path) -> Result<InstalledCustody, String> {
    let requirement = build_gate(
        COMPILED_PUBLISHER_REQUIREMENT,
        cfg!(debug_assertions),
        cfg!(target_os = "macos"),
    )?;
    #[cfg(target_os = "macos")]
    {
        native::observe(resources, requirement)
    }
    #[cfg(not(target_os = "macos"))]
    {
        let _ = (resources, requirement);
        Err("installed integrity unavailable on this platform".into())
    }
}

fn build_gate(requirement: Option<&str>, debug: bool, macos: bool) -> Result<&str, String> {
    let requirement = requirement
        .ok_or("installed integrity unavailable: compiled publisher requirement is not selected")?;
    if debug {
        return Err("installed integrity unavailable in a debug build".into());
    }
    if !macos {
        return Err("installed integrity unavailable on this platform".into());
    }
    Ok(requirement)
}

fn closed(value: &Value, keys: &[&str]) -> Result<(), String> {
    let object = value
        .as_object()
        .ok_or("installed observation object required")?;
    if object.len() != keys.len() || keys.iter().any(|key| !object.contains_key(*key)) {
        return Err("installed observation has missing or unknown fields".into());
    }
    Ok(())
}
fn string<'a>(value: &'a Value, key: &str) -> Result<&'a str, String> {
    value[key]
        .as_str()
        .filter(|s| !s.is_empty())
        .ok_or_else(|| format!("installed observation {key} missing"))
}
fn signing(value: &Value) -> Result<(), String> {
    closed(
        value,
        &[
            "cdhash",
            "identifier",
            "team_identifier",
            "signature_flags",
            "get_task_allow",
        ],
    )?;
    let hash = string(value, "cdhash")?;
    if hash.len() != 40
        || !hash
            .bytes()
            .all(|b| b.is_ascii_digit() || (b'a'..=b'f').contains(&b))
    {
        return Err("installed observation cdhash invalid".into());
    }
    if value["get_task_allow"] != false {
        return Err("installed development entitlement is not excluded".into());
    }
    string(value, "identifier")?;
    string(value, "team_identifier")?;
    let flags = value["signature_flags"]
        .as_u64()
        .ok_or("installed signature flags missing")?;
    if flags > u32::MAX as u64 || flags & 2 != 0 || flags & 0x10000 == 0 {
        return Err("installed App is ad-hoc or lacks hardened runtime".into());
    }
    Ok(())
}

/// Evidence validation only. Even a valid record cannot construct InstalledCustody.
/// The containing reader must separately join exact artifact bytes, selection,
/// complete generation and full inventory. This is not a signature on that record.
pub(crate) fn validate_evidence(value: &Value) -> Result<(), String> {
    closed(
        value,
        &[
            "observer",
            "standing",
            "requirement_sha256",
            "static_validation_flags",
            "dynamic_validation_flags",
            "static",
            "dynamic",
            "location",
            "custody_assumption",
            "limits",
        ],
    )?;
    if value["observer"] != OBSERVER
        || value["custody_assumption"] != "trusted-stable-installed-bundle-and-parent-path"
        || value["static_validation_flags"] != STATIC_VALIDATION_FLAGS
        || value["dynamic_validation_flags"] != DYNAMIC_VALIDATION_FLAGS
        || value["limits"] != json!(LIMITS)
    {
        return Err("installed observation semantic revision, flags or limits differ".into());
    }
    let requirement = match value["standing"].as_str() {
        Some("installed-observation") => COMPILED_PUBLISHER_REQUIREMENT
            .ok_or("installed evidence has no independently compiled publisher selection")?,
        #[cfg(test)]
        Some("synthetic-source-fixture") => SYNTHETIC_REQUIREMENT,
        _ => return Err("installed observation standing unsupported".into()),
    };
    if value["requirement_sha256"] != digest(requirement.as_bytes()) {
        return Err("installed observation requirement digest differs".into());
    }
    signing(&value["static"])?;
    signing(&value["dynamic"])?;
    if value["static"] != value["dynamic"] {
        return Err("installed static and dynamic signing facts differ".into());
    }
    let location = &value["location"];
    closed(
        location,
        &[
            "bundle",
            "executable",
            "resources",
            "parent",
            "translocation",
            "app_translocation_path_component",
        ],
    )?;
    let bundle = Path::new(string(location, "bundle")?);
    let executable = Path::new(string(location, "executable")?);
    let resources = Path::new(string(location, "resources")?);
    let parent = Path::new(string(location, "parent")?);
    if !bundle.is_absolute()
        || bundle.extension().and_then(|s| s.to_str()) != Some("app")
        || bundle.parent() != Some(parent)
        || executable.parent() != Some(bundle.join("Contents/MacOS").as_path())
        || resources != bundle.join("Contents/Resources")
        || bundle.components().any(|p| {
            matches!(
                p,
                std::path::Component::ParentDir | std::path::Component::CurDir
            )
        })
        || location["translocation"] != "not-established"
        || location["app_translocation_path_component"].as_bool()
            != Some(
                bundle
                    .components()
                    .any(|p| p.as_os_str() == "AppTranslocation"),
            )
    {
        return Err("installed observation location facts differ".into());
    }
    Ok(())
}

#[cfg(any(target_os = "macos", test))]
fn facts(
    requirement: &str,
    standing: &str,
    static_info: Value,
    dynamic_info: Value,
    bundle: &Path,
    executable: &Path,
    resources: &Path,
) -> Result<Value, String> {
    let parent = bundle.parent().ok_or("installed bundle has no parent")?;
    for path in [bundle, executable, resources, parent] {
        if path.to_str().is_none() {
            return Err("installed location is not UTF-8".into());
        }
    }
    let value = json!({
        "observer":OBSERVER,"standing":standing,"requirement_sha256":digest(requirement.as_bytes()),
        "static_validation_flags":STATIC_VALIDATION_FLAGS,"dynamic_validation_flags":DYNAMIC_VALIDATION_FLAGS,
        "static":static_info,"dynamic":dynamic_info,
        "location":{"bundle":bundle,"executable":executable,"resources":resources,"parent":parent,
            "translocation":"not-established","app_translocation_path_component":bundle.components().any(|p| p.as_os_str()=="AppTranslocation")},
        "custody_assumption":"trusted-stable-installed-bundle-and-parent-path","limits":LIMITS
    });
    validate_evidence(&value)?;
    Ok(value)
}

#[cfg(target_os = "macos")]
mod native {
    use super::*;
    use std::{
        ffi::{c_char, c_void, CString},
        os::unix::ffi::OsStrExt,
        path::PathBuf,
        ptr,
    };
    type Ref = *const c_void;
    type Status = i32;
    // Values and ABI checked against the installed macOS SDK's SecCode.h,
    // SecStaticCode.h, CSCommon.h and CoreFoundation headers. No subprocesses,
    // SecAssessment, requirement extraction, trust-anchor derivation or network.
    #[link(name = "Security", kind = "framework")]
    extern "C" {
        fn SecRequirementCreateWithString(text: Ref, flags: u32, out: *mut Ref) -> Status;
        fn SecStaticCodeCreateWithPath(path: Ref, flags: u32, out: *mut Ref) -> Status;
        fn SecStaticCodeCheckValidity(code: Ref, flags: u32, requirement: Ref) -> Status;
        fn SecCodeCopySelf(flags: u32, out: *mut Ref) -> Status;
        fn SecCodeCheckValidity(code: Ref, flags: u32, requirement: Ref) -> Status;
        fn SecCodeCopySigningInformation(code: Ref, flags: u32, out: *mut Ref) -> Status;
        static kSecCodeInfoUnique: Ref;
        static kSecCodeInfoIdentifier: Ref;
        static kSecCodeInfoTeamIdentifier: Ref;
        static kSecCodeInfoFlags: Ref;
        static kSecCodeInfoMainExecutable: Ref;
        static kSecCodeInfoEntitlementsDict: Ref;
    }
    #[link(name = "CoreFoundation", kind = "framework")]
    extern "C" {
        fn CFRelease(value: Ref);
        fn CFGetTypeID(value: Ref) -> usize;
        fn CFStringGetTypeID() -> usize;
        fn CFDataGetTypeID() -> usize;
        fn CFNumberGetTypeID() -> usize;
        fn CFDictionaryGetTypeID() -> usize;
        fn CFURLGetTypeID() -> usize;
        fn CFBooleanGetTypeID() -> usize;
        fn CFBooleanGetValue(value: Ref) -> u8;
        fn CFStringCreateWithCString(allocator: Ref, string: *const c_char, encoding: u32) -> Ref;
        fn CFStringGetCString(value: Ref, buffer: *mut c_char, size: isize, encoding: u32) -> u8;
        fn CFStringGetLength(value: Ref) -> isize;
        fn CFStringGetMaximumSizeForEncoding(length: isize, encoding: u32) -> isize;
        fn CFURLCreateFromFileSystemRepresentation(
            allocator: Ref,
            bytes: *const u8,
            len: isize,
            directory: u8,
        ) -> Ref;
        fn CFURLGetFileSystemRepresentation(
            url: Ref,
            resolve: u8,
            buffer: *mut u8,
            max: isize,
        ) -> u8;
        fn CFDictionaryGetValue(dictionary: Ref, key: Ref) -> Ref;
        fn CFNumberGetValue(number: Ref, kind: i32, out: *mut c_void) -> u8;
        fn CFDataGetLength(data: Ref) -> isize;
        fn CFDataGetBytePtr(data: Ref) -> *const u8;
    }
    struct Owned(Ref);
    impl Drop for Owned {
        fn drop(&mut self) {
            unsafe { CFRelease(self.0) }
        }
    }
    fn owned(value: Ref) -> Result<Owned, String> {
        if value.is_null() {
            Err("Security/CoreFoundation returned a null object".into())
        } else {
            Ok(Owned(value))
        }
    }
    fn status(code: Status, operation: &str) -> Result<(), String> {
        if code == 0 {
            Ok(())
        } else {
            Err(format!(
                "installed integrity {operation} failed (OSStatus {code})"
            ))
        }
    }
    fn copy(operation: &str, f: impl FnOnce(*mut Ref) -> Status) -> Result<Owned, String> {
        let mut value = ptr::null();
        status(f(&mut value), operation)?;
        owned(value)
    }
    const UTF8: u32 = 0x08000100;
    fn cf_string(text: &str) -> Result<Owned, String> {
        let c = CString::new(text).map_err(|_| "invalid compiled requirement string")?;
        owned(unsafe { CFStringCreateWithCString(ptr::null(), c.as_ptr(), UTF8) })
    }
    unsafe fn typed(value: Ref, expected: usize) -> Result<Ref, String> {
        if value.is_null() || CFGetTypeID(value) != expected {
            Err("Security signing information missing or has wrong type".into())
        } else {
            Ok(value)
        }
    }
    unsafe fn text(value: Ref) -> Result<String, String> {
        let value = typed(value, CFStringGetTypeID())?;
        let max = CFStringGetMaximumSizeForEncoding(CFStringGetLength(value), UTF8);
        if !(0..=65536).contains(&max) {
            return Err("Security signing string oversized".into());
        }
        let mut bytes = vec![0; max as usize + 1];
        if CFStringGetCString(value, bytes.as_mut_ptr().cast(), bytes.len() as isize, UTF8) == 0 {
            return Err("Security signing string invalid".into());
        }
        let end = bytes
            .iter()
            .position(|b| *b == 0)
            .ok_or("unterminated signing string")?;
        String::from_utf8(bytes[..end].to_vec())
            .map_err(|_| "Security signing string not UTF-8".into())
    }
    unsafe fn path(value: Ref) -> Result<PathBuf, String> {
        let value = typed(value, CFURLGetTypeID())?;
        let mut bytes = vec![0; 16384];
        if CFURLGetFileSystemRepresentation(value, 1, bytes.as_mut_ptr(), bytes.len() as isize) == 0
        {
            return Err("Security executable URL unavailable".into());
        }
        let end = bytes
            .iter()
            .position(|b| *b == 0)
            .ok_or("unterminated executable URL")?;
        Path::new(std::ffi::OsStr::from_bytes(&bytes[..end]))
            .canonicalize()
            .map_err(|_| "Security executable path cannot be resolved".into())
    }
    // SecCodeCopySigningInformation reports disk-backed signing information,
    // including kSecCodeInfoFlags. It is not a second independent kernel proof.
    // SecCodeCheckValidity below supplies the running-process requirement check.
    unsafe fn signing_info(code: Ref, executable: &Path) -> Result<Value, String> {
        let info = copy("copy signing information", |out| {
            SecCodeCopySigningInformation(code, 1 << 1, out)
        })?;
        typed(info.0, CFDictionaryGetTypeID())?;
        let get = |key| CFDictionaryGetValue(info.0, key);
        if path(get(kSecCodeInfoMainExecutable))? != executable {
            return Err("running and installed executable locations disagree".into());
        }
        let hash = typed(get(kSecCodeInfoUnique), CFDataGetTypeID())?;
        if CFDataGetLength(hash) != 20 {
            return Err("Security cdhash has unexpected length".into());
        }
        let bytes = CFDataGetBytePtr(hash);
        if bytes.is_null() {
            return Err("Security cdhash is null".into());
        }
        let hash = std::slice::from_raw_parts(bytes, 20)
            .iter()
            .map(|b| format!("{b:02x}"))
            .collect::<String>();
        let flags = typed(get(kSecCodeInfoFlags), CFNumberGetTypeID())?;
        let mut number: i64 = 0;
        if CFNumberGetValue(
            flags,
            4, /* kCFNumberSInt64Type */
            (&mut number as *mut i64).cast(),
        ) == 0
            || number < 0
        {
            return Err("Security signature flags invalid".into());
        }
        // Any present get-task-allow must be the boolean false. Unknown type fails.
        let entitlements = get(kSecCodeInfoEntitlementsDict);
        if !entitlements.is_null() {
            typed(entitlements, CFDictionaryGetTypeID())?;
            let key = cf_string("com.apple.security.get-task-allow")?;
            let allow = CFDictionaryGetValue(entitlements, key.0);
            if !allow.is_null()
                && (typed(allow, CFBooleanGetTypeID()).is_err() || CFBooleanGetValue(allow) != 0)
            {
                return Err("development get-task-allow entitlement is not permitted".into());
            }
        }
        let value = json!({"cdhash":hash,"identifier":text(get(kSecCodeInfoIdentifier))?,"team_identifier":text(get(kSecCodeInfoTeamIdentifier))?,"signature_flags":number,"get_task_allow":false});
        signing(&value)?;
        Ok(value)
    }
    pub(super) fn observe(resources: &Path, requirement: &str) -> Result<InstalledCustody, String> {
        let executable = std::env::current_exe()
            .and_then(|p| p.canonicalize())
            .map_err(|_| "running executable cannot be resolved")?;
        let macos = executable
            .parent()
            .ok_or("running executable has no parent")?;
        let contents = macos
            .parent()
            .ok_or("running executable is not in an App bundle")?;
        let bundle = contents
            .parent()
            .ok_or("running executable is not in an App bundle")?;
        if macos.file_name().and_then(|s| s.to_str()) != Some("MacOS")
            || contents.file_name().and_then(|s| s.to_str()) != Some("Contents")
            || bundle.extension().and_then(|s| s.to_str()) != Some("app")
        {
            return Err("running executable is not in an installed App bundle".into());
        }
        let expected_resources = bundle.join("Contents/Resources");
        let actual_resources = resources
            .canonicalize()
            .map_err(|_| "installed resources cannot be resolved")?;
        if actual_resources != expected_resources || !actual_resources.is_dir() {
            return Err(
                "supplied resource placement is not the running App bundle's Resources".into(),
            );
        }
        unsafe {
            let requirement_text = cf_string(requirement)?;
            let requirement_ref = copy("compile publisher requirement", |out| {
                SecRequirementCreateWithString(requirement_text.0, 0, out)
            })?;
            let bytes = bundle.as_os_str().as_bytes();
            let url = owned(CFURLCreateFromFileSystemRepresentation(
                ptr::null(),
                bytes.as_ptr(),
                bytes.len() as isize,
                1,
            ))?;
            let static_code = copy("open installed App", |out| {
                SecStaticCodeCreateWithPath(url.0, 0, out)
            })?;
            status(
                SecStaticCodeCheckValidity(
                    static_code.0,
                    STATIC_VALIDATION_FLAGS,
                    requirement_ref.0,
                ),
                "static strict/all-architecture/nested/resource validation",
            )?;
            let running_code = copy("resolve own process", |out| SecCodeCopySelf(0, out))?;
            // Dynamic validity checks the running process and its host. Static-only
            // flags cannot upgrade this API to full bundle resource validation.
            status(
                SecCodeCheckValidity(running_code.0, DYNAMIC_VALIDATION_FLAGS, requirement_ref.0),
                "dynamic publisher validation",
            )?;
            let static_info = signing_info(static_code.0, &executable)?;
            let dynamic_info = signing_info(running_code.0, &executable)?;
            let evidence = facts(
                requirement,
                "installed-observation",
                static_info,
                dynamic_info,
                bundle,
                &executable,
                &actual_resources,
            )?;
            Ok(InstalledCustody {
                facts: evidence,
                #[cfg(test)]
                synthetic_snapshot: None,
            })
        }
    }
}

#[cfg(test)]
const SYNTHETIC_REQUIREMENT: &str = "anchor apple generic and certificate leaf[subject.OU] = \"SYNTHETIC0\" and identifier \"invalid.example.synthetic\"";

/// Source-fixture seam, absent from production. This does not run Security or sign
/// anything, and its explicitly synthetic evidence never qualifies a package.
#[cfg(test)]
pub(crate) fn synthetic_for_tests(resources: &Path) -> Result<InstalledCustody, String> {
    fn walk(path: &Path, base: &Path, bytes: &mut Vec<u8>) -> Result<(), String> {
        let metadata = std::fs::symlink_metadata(path).map_err(|e| e.to_string())?;
        if metadata.file_type().is_symlink() {
            return Err("synthetic resource link refused".into());
        }
        bytes.extend_from_slice(
            path.strip_prefix(base)
                .map_err(|e| e.to_string())?
                .as_os_str()
                .as_encoded_bytes(),
        );
        bytes.push(0);
        bytes.extend_from_slice(&metadata.len().to_le_bytes());
        #[cfg(unix)]
        {
            use std::os::unix::fs::PermissionsExt;
            bytes.extend_from_slice(&metadata.permissions().mode().to_le_bytes());
        }

        if metadata.is_dir() {
            let mut entries = std::fs::read_dir(path)
                .map_err(|e| e.to_string())?
                .map(|e| e.map(|x| x.path()))
                .collect::<Result<Vec<_>, _>>()
                .map_err(|e| e.to_string())?;
            entries.sort();
            for entry in entries {
                walk(&entry, base, bytes)?;
            }
        } else if metadata.is_file() {
            bytes.extend_from_slice(&std::fs::read(path).map_err(|e| e.to_string())?);
        } else {
            return Err("synthetic resource type refused".into());
        }
        Ok(())
    }
    let resources = resources.canonicalize().map_err(|e| e.to_string())?;
    let bundle = resources
        .parent()
        .and_then(Path::parent)
        .ok_or("synthetic bundle layout required")?;
    let executable = bundle.join("Contents/MacOS/synthetic-app");
    let info = json!({"cdhash":"a".repeat(40),"identifier":"invalid.example.synthetic","team_identifier":"SYNTHETIC0","signature_flags":65536,"get_task_allow":false});
    let evidence = facts(
        SYNTHETIC_REQUIREMENT,
        "synthetic-source-fixture",
        info.clone(),
        info,
        bundle,
        &executable,
        &resources,
    )?;
    let mut bytes = Vec::new();
    walk(&resources, &resources, &mut bytes)?;
    Ok(InstalledCustody {
        facts: evidence,
        synthetic_snapshot: Some(digest(&bytes)),
    })
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn compiled_absence_never_observes_or_accepts_external_authority() {
        assert!(COMPILED_PUBLISHER_REQUIREMENT.is_none());
        assert!(observe(Path::new(
            "/caller-selected/Untrusted.app/Contents/Resources"
        ))
        .unwrap_err()
        .contains("not selected"));
        assert!(validate_evidence(&Value::Null).is_err());
        assert!(validate_evidence(&json!({"outcome":"pass"})).is_err());
    }
    #[test]
    fn unsigned_adhoc_missing_hardening_and_wrong_cdhash_are_rejected() {
        assert!(signing(&json!({})).is_err());
        let mut info = json!({"cdhash":"a".repeat(40),"identifier":"invalid.example.synthetic","team_identifier":"SYNTHETIC0","signature_flags":65536,"get_task_allow":false});
        assert!(signing(&info).is_ok());
        info["signature_flags"] = json!(65538);
        assert!(signing(&info).is_err());
        info["signature_flags"] = json!(0);
        assert!(signing(&info).is_err());
        info["signature_flags"] = json!(65536);
        info["cdhash"] = json!("opaque");
        assert!(signing(&info).is_err());
    }

    #[test]
    fn none_debug_and_nonmacos_cannot_pass_build_gate() {
        assert!(build_gate(None, false, true).is_err());
        assert!(build_gate(Some(SYNTHETIC_REQUIREMENT), true, true).is_err());
        assert!(build_gate(Some(SYNTHETIC_REQUIREMENT), false, false).is_err());
        assert_eq!(STATIC_VALIDATION_FLAGS, 0x20000019);
        assert_eq!(DYNAMIC_VALIDATION_FLAGS, 0x20000000);
    }
    #[test]
    fn synthetic_evidence_is_closed_and_resource_mutation_revokes_recheck() {
        let root = std::env::temp_dir().join(format!(
            "s4-observer-{}-{}",
            std::process::id(),
            std::time::SystemTime::now()
                .duration_since(std::time::UNIX_EPOCH)
                .unwrap()
                .as_nanos()
        ));
        let resources = root.join("Synthetic.app/Contents/Resources");
        std::fs::create_dir_all(&resources).unwrap();
        std::fs::write(
            resources.join("non-codex-resource.txt"),
            b"sealed fixture bytes",
        )
        .unwrap();
        let observation = synthetic_for_tests(&resources).unwrap();
        let evidence = observation.evidence();
        assert!(validate_evidence(&evidence).is_ok());
        assert!(observation.recheck(&resources).is_ok());
        for (pointer, replacement) in [
            ("/observer", json!("unknown")),
            ("/standing", json!("installed-observation")),
            ("/requirement_sha256", json!("0".repeat(64))),
            ("/static_validation_flags", json!(0)),
            ("/dynamic_validation_flags", json!(STATIC_VALIDATION_FLAGS)),
            ("/dynamic/cdhash", json!("b".repeat(40))),
            ("/static/signature_flags", json!(65538)),
            ("/static/get_task_allow", json!(true)),
            ("/location/resources", json!("/caller-supplied/Resources")),
            ("/location/translocation", json!("not-translocated")),
        ] {
            let mut mutated = evidence.clone();
            *mutated.pointer_mut(pointer).unwrap() = replacement;
            assert!(validate_evidence(&mutated).is_err(), "{pointer}");
        }
        let mut unknown = evidence.clone();
        unknown["authority"] = json!(true);
        assert!(validate_evidence(&unknown).is_err());
        std::fs::write(resources.join("non-codex-resource.txt"), b"modified bytes").unwrap();
        assert!(observation
            .recheck(&resources)
            .unwrap_err()
            .contains("changed before spawn"));
        std::fs::remove_dir_all(root).unwrap();
    }
}
