//! Immutable complete S1 publications; all IO is outside Host custody gates.
use super::*;
use crate::{
    distribution_preflight::{selection::Selected, Artifact},
    distribution_s1::{self, Files},
};
const OBSERVED: &str = ".chirality-s1/observed.json";
const LIFECYCLE: &str = ".chirality-s1/lifecycle.json";
const FACTS: &str = ".chirality-s1/preflight.json";
const TRANSPORT: &str = ".chirality-s1/transport.json";
#[derive(Clone, Serialize)]
#[serde(rename_all = "camelCase")]
pub(crate) struct S1Reference {
    format: &'static str,
    publication: String,
    generation: Value,
    observed: Artifact,
    lifecycle: Option<Artifact>,
    transport: Artifact,
    reader: Value,
    #[serde(skip)]
    files: Files,
    #[serde(skip)]
    publication_id: (u64, u64),
}
fn artifact_ref(path: &str, bytes: &[u8]) -> Artifact {
    Artifact {
        path: path.into(),
        sha256: digest(bytes),
    }
}
fn parent(root: &File, path: &str, create: bool) -> Result<(File, String), String> {
    let mut parts = path.split('/').peekable();
    let mut fd = root.try_clone().map_err(error)?;
    while let Some(part) = parts.next() {
        component(part)?;
        if parts.peek().is_none() {
            return Ok((fd, part.into()));
        }
        let child = if create {
            mkdir(&fd, part, false)?
        } else {
            open_at(&fd, part, true)?
        };
        private(&child, true)?;
        if create {
            child.sync_all().map_err(error)?;
            fd.sync_all().map_err(error)?;
        }
        fd = child;
    }
    Err("empty artifact path".into())
}
fn read_member(dir: &File, path: &str, hash: &str) -> Result<Vec<u8>, String> {
    let (parent, name) = parent(dir, path, false)?;
    read_exact(&parent, &name, hash)
}
fn layout(
    files: &Files,
) -> Result<std::collections::BTreeMap<String, Option<(String, u64)>>, String> {
    let mut map = std::collections::BTreeMap::new();
    map.insert(".".into(), None);
    for (path, raw) in files {
        for part in path.split('/') {
            component(part)?;
        }
        if map
            .insert(path.clone(), Some((digest(raw), raw.len() as u64)))
            .is_some()
        {
            return Err("publication file/directory collision".into());
        }
        let mut parent = Path::new(path).parent();
        while let Some(p) = parent {
            let p = p.to_str().ok_or("invalid path")?;
            if !p.is_empty() {
                if map.get(p).is_some_and(Option::is_some) {
                    return Err("publication file ancestor collision".into());
                }
                map.entry(p.into()).or_insert(None);
            }
            parent = Path::new(p).parent();
        }
    }
    Ok(map)
}
impl Store {
    #[cfg(test)]
    pub(crate) fn before_s1_audit(&self, hook: impl FnOnce() + Send + 'static) {
        *self.before_audit.lock().unwrap() = Some(Box::new(hook));
    }
    /// Caller cannot manufacture Selected; production factory uses the compiled
    /// anchor, and the only alternative constructor is cfg(test).
    pub(crate) fn open_selected(
        app: &Path,
        vendor: &Path,
        namespaces: Arc<NativeNamespaceBindings>,
        selected: Selected,
    ) -> Result<Arc<Self>, String> {
        guard_vendor_domain(&app.join("runtime/distribution"), selected.source())?;
        selected.recheck()?;
        let mut store = Self::open(app, vendor, namespaces)?;
        Arc::get_mut(&mut store)
            .ok_or("store unexpectedly shared")?
            .selected = Some(selected);
        store.guard_s1(&store.authority.lease()?)?;
        Ok(store)
    }
    fn guard_s1(&self,lease:&NamespaceLease<'_>) -> Result<File, String> {
        let root = self.guard(lease)?;
        if let Some(selected) = &self.selected {
            guard_vendor_domain(&self.root, selected.source())?;
            selected.recheck()?;
        }
        Ok(root)
    }
    pub(crate) fn publish_observed(
        &self,
        g: &Value,
        mut observation: Value,
        facts: Value,
    ) -> Result<S1Reference, String> {
        let lease=self.authority.lease()?;
        self.guard_s1(&lease)?;
        self.generation(&lease,g)?;
        if observation["generation"] != *g {
            return Err("observation generation differs".into());
        }
        let mut files = self
            .selected
            .as_ref()
            .map(|s| s.files().clone())
            .unwrap_or_default();
        if files
            .keys()
            .any(|p| p == ".chirality-s1" || p.starts_with(".chirality-s1/"))
        {
            return Err("selected artifact collides with reserved publication paths".into());
        }
        if let Some(selected) = &self.selected {
            observation["expected_reference"] =
                serde_json::to_value(selected.expected_ref()).map_err(error)?;
            observation["adoption_attestation"] =
                serde_json::to_value(selected.attestation_ref()).map_err(error)?;
        }
        let raw = serde_json::to_vec(&facts).map_err(error)?;
        let evidence = serde_json::to_value(artifact_ref(FACTS, &raw)).map_err(error)?;
        files.insert(FACTS.into(), raw);
        for check in observation["checks"]
            .as_object_mut()
            .ok_or("checks absent")?
            .values_mut()
        {
            check["evidence"] = evidence.clone();
        }
        if distribution_s1::observed(&observation, &files, self.selected.as_ref())?
            != "unverifiable"
        {
            return Err("pre-spawn observation contradiction; no launch".into());
        }
        files.insert(
            OBSERVED.into(),
            serde_json::to_vec(&observation).map_err(error)?,
        );
        self.publish_s1(&lease,g, files, false)
    }
    pub(crate) fn publish_lt09(
        &self,
        g: &Value,
        prior: &S1Reference,
        event: &Value,
    ) -> Result<S1Reference, String> {
        let lease=self.authority.lease()?;
        self.read_s1_leased(&lease,g, prior)?;
        if event["transitionId"] != "LT-09" || event["generation"] != *g {
            return Err("only actual same-generation LT-09 supported".into());
        }
        let mut files = prior.files.clone();
        files.remove(TRANSPORT);
        let envelope = json!({"format":"lifecycle-event.s1","legacy_event":event,"verification_artifact":prior.observed,"verification_generation":g});
        distribution_s1::lifecycle(&envelope, &files, self.selected.as_ref())?;
        files.insert(
            LIFECYCLE.into(),
            serde_json::to_vec(&envelope).map_err(error)?,
        );
        self.publish_s1(&lease,g, files, true)
    }
    fn publish_s1(
        &self,
        lease:&NamespaceLease<'_>,
        g: &Value,
        mut files: Files,
        lifecycle: bool,
    ) -> Result<S1Reference, String> {
        self.generation(&lease,g)?;
        let root = self.guard_s1(&lease)?;
        let name = util::opaque_id("s1-")?;
        let staging = format!(".pending-{name}");
        let transport = json!({"format":"distribution-closure-transport.s3","method":"selected-s1-contract-closure.s3","sourceAssociation":self.selected.as_ref().map(Selected::association),"mirrorLocator":self.root.join(&name),"generation":g,"entries":files.iter().map(|(path,raw)|artifact_ref(path,raw)).collect::<Vec<_>>(),"reader":distribution_s1::identity(),"limit":"Creation correspondence only; no future integrity, issuer, qualification or live custody assertion"});
        files.insert(
            TRANSPORT.into(),
            serde_json::to_vec(&transport).map_err(error)?,
        );
        layout(&files)?;
        if files.values().map(Vec::len).sum::<usize>() > 32 * 1024 * 1024 {
            return Err("publication closure byte limit".into());
        }
        let dir = mkdir(&root, &staging, true)?;
        for (path, raw) in &files {
            let (parent, name) = parent(&dir, path, true)?;
            write_new(&parent, &name, raw)?;
            parent.sync_all().map_err(error)?;
        }
        dir.sync_all().map_err(error)?;
        self.guard_s1(&lease)?;
        self.generation(&lease,g)?;
        if id(&dir)? != id(&open_at(&root, &staging, true)?)? {
            return Err("staging directory changed".into());
        }
        publish_rename(&root, &staging, &name)?;
        root.sync_all().map_err(error)?;
        let reference = S1Reference {
            format: "distribution-s1-reference.s3",
            publication: name,
            generation: g.clone(),
            observed: artifact_ref(OBSERVED, &files[OBSERVED]),
            lifecycle: if lifecycle {
                Some(artifact_ref(LIFECYCLE, &files[LIFECYCLE]))
            } else {
                None
            },
            transport: artifact_ref(TRANSPORT, &files[TRANSPORT]),
            reader: distribution_s1::identity(),
            files,
            publication_id: id(&dir)?,
        };
        self.read_s1_leased(&lease,g, &reference)?;
        Ok(reference)
    }
    pub(crate) fn read_s1(&self,g:&Value,reference:&S1Reference)->Result<Value,String>{let lease=self.authority.lease()?;self.read_s1_leased(&lease,g,reference)}
    fn read_s1_leased(&self,lease:&NamespaceLease<'_>, g: &Value, reference: &S1Reference) -> Result<Value, String> {
        self.generation(&lease,g)?;
        if &reference.generation != g {
            return Err("foreign S1 generation".into());
        }
        let root = self.guard_s1(&lease)?;
        let dir = open_at(&root, &reference.publication, true)?;
        private(&dir, true)?;
        if id(&dir)? != reference.publication_id {
            return Err("S1 publication replaced".into());
        }
        let mut files = Files::new();
        for (path, expected) in &reference.files {
            files.insert(path.clone(), read_member(&dir, path, &digest(expected))?);
        }
        if let Some(selected) = &self.selected {
            selected.check_mirror(&files)?;
        }
        let transport: Value = serde_json::from_slice(&files[TRANSPORT]).map_err(error)?;
        distribution_s1::shape(
            &transport,
            include_str!(
                "../resources/distribution-successor/distribution-closure-transport.s3.schema.json"
            ),
        )?;
        let expected_entries = files
            .iter()
            .filter(|(p, _)| p.as_str() != TRANSPORT)
            .map(|(path, raw)| artifact_ref(path, raw))
            .collect::<Vec<_>>();
        if transport["format"] != "distribution-closure-transport.s3"
            || transport["method"] != "selected-s1-contract-closure.s3"
            || transport["generation"] != *g
            || transport["sourceAssociation"]
                != self
                    .selected
                    .as_ref()
                    .map(Selected::association)
                    .unwrap_or(Value::Null)
            || transport["mirrorLocator"] != json!(self.root.join(&reference.publication))
            || transport["entries"] != serde_json::to_value(expected_entries).map_err(error)?
            || transport["reader"] != distribution_s1::identity()
        {
            return Err("transport association differs".into());
        }
        let observed: Value = serde_json::from_slice(&files[OBSERVED]).map_err(error)?;
        if observed["generation"] != *g {
            return Err("S1 observation generation differs".into());
        }
        let outcome = distribution_s1::observed(&observed, &files, self.selected.as_ref())?;
        let lifecycle = if reference.lifecycle.is_some() {
            let value: Value = serde_json::from_slice(&files[LIFECYCLE]).map_err(error)?;
            distribution_s1::lifecycle(&value, &files, self.selected.as_ref())?;
            Some(value)
        } else {
            None
        };
        #[cfg(test)]
        if let Some(hook) = self.before_audit.lock().unwrap().take() {
            hook();
        }
        let inventory =
            crate::distribution_preflight::scan(&self.root.join(&reference.publication))?;
        let expected = layout(&files)?;
        if inventory.entries.len() != expected.len() {
            return Err("S1 closure extra/missing entry".into());
        }
        for e in inventory.entries {
            match expected.get(&e.path) {
                Some(None) if e.kind == "dir" && e.mode == 0o700 => (),
                Some(Some((hash, size)))
                    if e.kind == "file"
                        && e.mode == 0o600
                        && e.sha256.as_ref() == Some(hash)
                        && e.size == Some(*size) =>
                {
                    ()
                }
                _ => return Err("S1 final inventory differs".into()),
            }
        }
        if id(&dir)? != id(&open_at(&root, &reference.publication, true)?)? {
            return Err("S1 publication changed".into());
        }
        self.guard_s1(&lease)?;
        self.generation(&lease,g)?;
        Ok(
            json!({"reference":reference,"artifact":observed,"lifecycle":lifecycle,"transport":transport,"outcome":outcome,"standing":"unverified-development","readStanding":"S1 shape/semantics and exact closure checked at this read; no future integrity or live custody assertion","unsupportedEnvelopes":"Only actual LT-09 is published; pre-spawn/restart/other legacy envelopes unavailable"}),
        )
    }
}
