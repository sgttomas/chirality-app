//! Explicit M-A home resources. No defaults, credential/content reads, native calls or registry.
//! Filesystem observations do not qualify Codex discovery or an atomic later config write.
use crate::storage;
use sha2::{Digest, Sha256};
use std::path::{Component, Path, PathBuf};

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub enum HomeClass {
    Account,
    ApiKey,
    Probe,
}
impl HomeClass {
    pub fn as_str(self) -> &'static str {
        match self {
            Self::Account => "account",
            Self::ApiKey => "api-key",
            Self::Probe => "probe",
        }
    }
}
#[derive(Clone, Debug, Eq, PartialEq)]
pub struct SharedResourceTargets {
    pub config_toml: PathBuf,
    pub global_agents_md: PathBuf,
    pub skills: PathBuf,
}
#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub enum ResourceState {
    Linked,
    TargetMissing,
    TargetTypeMismatch,
    Conflict,
    NotSupplied,
}
#[derive(Clone, Debug)]
pub struct ResourceObservation {
    pub name: &'static str,
    pub destination: PathBuf,
    pub intended_target: Option<PathBuf>,
    pub state: ResourceState,
    pub limit: Option<String>,
}
#[derive(Clone, Debug)]
pub struct HomeObservation {
    pub class: HomeClass,
    pub native_path: PathBuf,
    pub opaque_home_id: String,
    pub resources: Vec<ResourceObservation>,
}
impl HomeObservation {
    /// Presentation only; never use this string as a native path or identity.
    pub fn display_path(&self) -> String {
        self.native_path.display().to_string()
    }
}
#[derive(Clone, Debug)]
pub struct OwnedHomePlan {
    app_data_root: PathBuf,
    home_path: PathBuf,
    class: HomeClass,
    shared: Option<SharedResourceTargets>,
}
/// Explicit receiving reference, not an App-data ownership or resource-setup claim.
/// Existing account/probe references may live outside the new-home allocation root.
#[derive(Clone, Debug)]
pub struct ExistingHomeReference {
    native_path: PathBuf,
    class: HomeClass,
}
impl ExistingHomeReference {
    pub fn new(native_path: PathBuf, class: HomeClass) -> Result<Self, String> {
        if class == HomeClass::ApiKey {
            return Err("API-key home requires the owning-home plan".into());
        }
        let reference = Self { native_path, class };
        reference.check()?;
        Ok(reference)
    }
    fn check(&self) -> Result<(), String> {
        clean_absolute(&self.native_path)?;
        storage::check_path(&self.native_path)?;
        let metadata = std::fs::symlink_metadata(&self.native_path)
            .map_err(|e| format!("explicit existing home unavailable: {e}"))?;
        if !metadata.is_dir() {
            return Err("explicit existing home is not a directory".into());
        }
        Ok(())
    }
    pub fn native_path(&self) -> &Path {
        &self.native_path
    }
    pub fn class(&self) -> HomeClass {
        self.class
    }
    pub fn opaque_home_id(&self) -> String {
        path_home_id(&self.native_path)
    }
    /// No shared-resource or directory-ownership claim follows from receiving this reference.
    pub fn inspect(&self) -> Result<HomeObservation, String> {
        self.check()?;
        Ok(HomeObservation {
            class: self.class,
            native_path: self.native_path.clone(),
            opaque_home_id: self.opaque_home_id(),
            resources: Vec::new(),
        })
    }
}
#[derive(Clone, Copy, Debug)]
pub enum HomeBinding<'a> {
    Owned(&'a OwnedHomePlan),
    Existing(&'a ExistingHomeReference),
}
impl<'a> HomeBinding<'a> {
    fn check(self) -> Result<(), String> {
        match self {
            Self::Owned(plan) => plan.check_owned_directory(),
            Self::Existing(reference) => reference.check(),
        }
    }
    pub fn native_path(self) -> &'a Path {
        match self {
            Self::Owned(plan) => plan.native_path(),
            Self::Existing(reference) => reference.native_path(),
        }
    }
}
fn path_home_id(path: &Path) -> String {
    format!(
        "app-home:{:x}",
        Sha256::digest(path.as_os_str().as_encoded_bytes())
    )
}
fn clean_absolute(path: &Path) -> Result<(), String> {
    if !path.is_absolute()
        || path
            .components()
            .any(|c| matches!(c, Component::ParentDir | Component::CurDir))
    {
        return Err("explicit absolute path without relative aliases required".into());
    }
    Ok(())
}
/// Resolve the existing ancestor using the host filesystem, retaining each missing native suffix.
/// This is a current relationship observation, not a guarantee about future creation/replacement.
fn observed_location(path: &Path) -> Result<PathBuf, String> {
    observed_location_with_links(path, 0)
}
fn observed_location_with_links(path: &Path, links: usize) -> Result<PathBuf, String> {
    if links > 40 {
        return Err("path relationship unavailable: source link cycle/depth".into());
    }
    let mut ancestor = path;
    let mut suffix = Vec::new();
    loop {
        match std::fs::symlink_metadata(ancestor) {
            Ok(metadata) => {
                let mut resolved = if metadata.file_type().is_symlink() {
                    let target = std::fs::read_link(ancestor)
                        .map_err(|e| format!("source link unavailable: {e}"))?;
                    let target = if target.is_absolute() {
                        target
                    } else {
                        ancestor
                            .parent()
                            .ok_or("source link parent unavailable")?
                            .join(target)
                    };
                    observed_location_with_links(&target, links + 1)?
                } else {
                    std::fs::canonicalize(ancestor)
                        .map_err(|e| format!("existing path source unavailable: {e}"))?
                };
                for component in suffix.iter().rev() {
                    resolved.push(component);
                }
                return Ok(resolved);
            }
            Err(e) if e.kind() == std::io::ErrorKind::NotFound => {
                let name = ancestor
                    .file_name()
                    .ok_or("existing path ancestor not established")?;
                suffix.push(name.to_os_string());
                ancestor = ancestor
                    .parent()
                    .ok_or("existing path ancestor not established")?;
            }
            Err(e) => return Err(format!("path relationship unavailable: {e}")),
        }
    }
}
impl OwnedHomePlan {
    pub fn new(
        app_data_root: PathBuf,
        home_path: PathBuf,
        class: HomeClass,
        shared: Option<SharedResourceTargets>,
    ) -> Result<Self, String> {
        clean_absolute(&app_data_root)?;
        clean_absolute(&home_path)?;
        if home_path == app_data_root || !home_path.starts_with(&app_data_root) {
            return Err(
                "owned home must be an explicit strict descendant of the App-data root".into(),
            );
        }
        match (class, &shared) {
            (HomeClass::Probe, Some(_)) => return Err("probe receives no shared resources".into()),
            (HomeClass::Account | HomeClass::ApiKey, None) => {
                return Err("shared native resource references not established".into())
            }
            _ => {}
        }
        if let Some(s) = &shared {
            for p in [&s.config_toml, &s.global_agents_md, &s.skills] {
                clean_absolute(p)?;
                if p.starts_with(&home_path) {
                    return Err("shared source cannot refer into its receiving home".into());
                }
            }
        }
        storage::check_path(&home_path)?;
        let plan = Self {
            app_data_root,
            home_path,
            class,
            shared,
        };
        plan.check_owned_directory()?;
        Ok(plan)
    }
    pub fn native_path(&self) -> &Path {
        &self.home_path
    }
    pub fn class(&self) -> HomeClass {
        self.class
    }
    /// Existing HOST convention; class is not this opaque identity, and bytes are never lossy display.
    pub fn opaque_home_id(&self) -> String {
        path_home_id(&self.home_path)
    }
    fn check_owned_directory(&self) -> Result<(), String> {
        storage::check_path(&self.home_path)?;
        if !self.home_path.starts_with(&self.app_data_root) {
            return Err("owning location changed".into());
        }
        let receiving = observed_location(&self.home_path)?;
        if let Some(shared) = &self.shared {
            for target in [
                &shared.config_toml,
                &shared.global_agents_md,
                &shared.skills,
            ] {
                // Unavailable shared resources remain visible source limits, not a native-start veto.
                if observed_location(target).is_ok_and(|location| location.starts_with(&receiving))
                {
                    return Err("shared source resolves into its receiving home".into());
                }
            }
        }
        Ok(())
    }
    fn targets(&self) -> [(&'static str, Option<&Path>, bool); 3] {
        match &self.shared {
            Some(s) => [
                ("config.toml", Some(&s.config_toml), false),
                ("AGENTS.md", Some(&s.global_agents_md), false),
                ("skills", Some(&s.skills), true),
            ],
            None => [
                ("config.toml", None, false),
                ("AGENTS.md", None, false),
                ("skills", None, true),
            ],
        }
    }
    fn observe(
        &self,
        name: &'static str,
        target: Option<&Path>,
        directory: bool,
    ) -> ResourceObservation {
        let destination = self.home_path.join(name);
        let mut out = ResourceObservation {
            name,
            destination: destination.clone(),
            intended_target: target.map(Path::to_path_buf),
            state: ResourceState::Conflict,
            limit: None,
        };
        let metadata = match std::fs::symlink_metadata(&destination) {
            Ok(m) => m,
            Err(e) if e.kind() == std::io::ErrorKind::NotFound => {
                out.state = ResourceState::NotSupplied;
                out.limit = target.map(|_| "expected link not present".into());
                return out;
            }
            Err(e) => {
                out.limit = Some(format!("resource location unavailable: {e}"));
                return out;
            }
        };
        let Some(target) = target else {
            out.limit =
                Some("probe has an existing resource; preserved, not shared by this module".into());
            return out;
        };
        if !metadata.file_type().is_symlink() {
            out.limit = Some("existing non-link preserved; no overwrite or copy".into());
            return out;
        }
        match std::fs::read_link(&destination) {
            Ok(actual) if actual == target => {}
            Ok(_) => {
                out.limit =
                    Some("link target differs from explicit intended source; preserved".into());
                return out;
            }
            Err(e) => {
                out.limit = Some(format!("link target unavailable: {e}"));
                return out;
            }
        }
        match std::fs::metadata(target) {
            Ok(m) if (directory && m.is_dir()) || (!directory && m.is_file()) => {
                out.state = ResourceState::Linked
            }
            Ok(_) => {
                out.state = ResourceState::TargetTypeMismatch;
                out.limit = Some("shared target has wrong file type".into());
            }
            Err(e) if e.kind() == std::io::ErrorKind::NotFound => {
                out.state = ResourceState::TargetMissing;
                out.limit = Some("shared target missing; no fallback/copy".into());
            }
            Err(e) => {
                out.state = ResourceState::Conflict;
                out.limit = Some(format!("shared target unavailable: {e}"));
            }
        }
        out
    }
    pub fn inspect(&self) -> Result<HomeObservation, String> {
        self.check_owned_directory()?;
        Ok(HomeObservation {
            class: self.class,
            native_path: self.home_path.clone(),
            opaque_home_id: self.opaque_home_id(),
            resources: self
                .targets()
                .into_iter()
                .map(|(n, t, d)| self.observe(n, t, d))
                .collect(),
        })
    }
    /// Caller invokes only for its actual owning-home setup event. No startup/credential policy here.
    pub fn prepare(&self) -> Result<HomeObservation, String> {
        self.check_owned_directory()?;
        storage::ensure_directory(&self.home_path)?;
        for (name, target, _) in self.targets() {
            let Some(target) = target else {
                continue;
            };
            self.check_owned_directory()?;
            let destination = self.home_path.join(name);
            // symlink creation is create-only, including existing/dangling links and ordinary files.
            #[cfg(unix)]
            match std::os::unix::fs::symlink(target, &destination) {
                Ok(()) => storage::sync_dir(&self.home_path)?,
                Err(e) if e.kind() == std::io::ErrorKind::AlreadyExists => {}
                Err(e) => return Err(format!("resource link creation failed: {e}")),
            }
            #[cfg(not(unix))]
            return Err(
                "resource linking is not established on this platform; no copy fallback".into(),
            );
        }
        self.inspect()
    }
    /// Point-in-time target observation only. Later person-directed native write still needs version/source checks.
    pub fn resolved_config_write_target(&self) -> Result<PathBuf, String> {
        self.check_owned_directory()?;
        let source = self
            .shared
            .as_ref()
            .ok_or("probe has no shared config write target")?;
        if self
            .observe("config.toml", Some(&source.config_toml), false)
            .state
            != ResourceState::Linked
        {
            return Err("intended shared config link/regular target not established".into());
        }
        let resolved = std::fs::canonicalize(&source.config_toml)
            .map_err(|e| format!("config target unavailable: {e}"))?;
        if self
            .observe("config.toml", Some(&source.config_toml), false)
            .state
            != ResourceState::Linked
        {
            return Err("config link changed during observation".into());
        }
        Ok(resolved)
    }
}
/// Root must revalidate the entire receiving set, including probe, at binding/setup.
/// No persistent registry: observations do not exclude a later external directory replacement.
pub fn validate_distinct_homes(homes: &[&OwnedHomePlan]) -> Result<(), String> {
    let bindings: Vec<_> = homes.iter().map(|home| HomeBinding::Owned(home)).collect();
    validate_home_bindings(&bindings)
}
/// Source receiving check across explicit existing and App-owned plans; no root coercion/registry.
pub fn validate_home_bindings(homes: &[HomeBinding<'_>]) -> Result<(), String> {
    for (i, home) in homes.iter().enumerate() {
        home.check()?;
        for other in &homes[..i] {
            let current = home.native_path();
            let previous = other.native_path();
            if current.starts_with(previous) || previous.starts_with(current) {
                return Err("home bindings overlap; no auth/state sharing".into());
            }
            let a = observed_location(current)?;
            let b = observed_location(previous)?;
            if a.starts_with(&b) || b.starts_with(&a) {
                return Err("home bindings resolve to overlapping actual directories".into());
            }
        }
    }
    Ok(())
}

pub fn validate_distinct_account_homes(
    account: &OwnedHomePlan,
    key: &OwnedHomePlan,
) -> Result<(), String> {
    if account.class != HomeClass::Account || key.class != HomeClass::ApiKey {
        return Err("account/key classes required".into());
    }
    validate_distinct_homes(&[account, key])?;
    if account.shared != key.shared {
        return Err("account/key shared native resource references differ".into());
    }
    Ok(())
}
