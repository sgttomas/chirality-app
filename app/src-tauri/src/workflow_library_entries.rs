//! Explicit opened-library discovery. Cached observations are display data;
//! only an owning listing can bind chosen entries to an in-place review.
use super::*;
use std::collections::BTreeMap;
use std::os::unix::fs::MetadataExt;

const PUBLISHED: &str = ".chirality/workflows";
const STANDING: &str = "explicit library observation; files are not registration, selection or an act; refresh to observe changes";

pub(super) fn directory_source(path: &Path) -> Result<Value, String> {
    storage::check_path(path)?;
    let mut facts = Vec::new();
    for part in path.ancestors() {
        let metadata =
            fs::symlink_metadata(part).map_err(|e| format!("library source unavailable: {e}"))?;
        if !metadata.is_dir() || metadata.file_type().is_symlink() {
            return Err("library source is not a plain directory".into());
        }
        facts.push(json!({"path":crate::attachments::native_path_identity(part),"device":metadata.dev(),"inode":metadata.ino()}));
    }
    Ok(json!(facts))
}

struct ListedEntry {
    name: String,
    revision: String,
    source: Value,
    slot: Vec<Value>,
}
pub(crate) struct EntryListing {
    reference: String,
    library: String,
    root_source: Option<Value>,
    selected: BTreeMap<String, ListedEntry>,
    view: Value,
}
impl EntryListing {
    pub(crate) fn observe(owner: &LibraryOwner, library: &str) -> Self {
        let reference =
            crate::util::opaque_id("workflow-library-listing:").expect("listing identity");
        let mut listing = Self {
            reference: reference.clone(),
            library: library.into(),
            root_source: None,
            selected: BTreeMap::new(),
            view: json!({"reference":reference,"libraryRef":library,"observedAt":crate::util::now_rfc3339(),"state":"observed",
                "source":{"origin":owner.origin,"sourceRoot":owner.source_root,"root":crate::attachments::native_path_identity(&owner.root)},
                "entries":[],"limits":[],"standing":STANDING}),
        };
        if let Err(cause) = listing.scan(owner) {
            listing.selected.clear();
            listing.view["state"] = json!("unavailable");
            listing.view["limits"] = json!([cause]);
        }
        listing
    }
    fn scan(&mut self, owner: &LibraryOwner) -> Result<(), String> {
        let root = directory_source(&owner.root)?;
        // A malformed/incomplete ledger cannot establish that a slot has no
        // registration. It closes review eligibility, never becomes LS-2.
        let ledger = read_ledger(&owner.root)?;
        let folder = owner.root.join(PUBLISHED);
        match fs::symlink_metadata(&folder) {
            Err(error) if error.kind() == std::io::ErrorKind::NotFound => {
                self.view["state"] = json!("absent");
                self.root_source = Some(root);
                return Ok(());
            }
            Err(error) => return Err(format!("library entry folder unreadable: {error}")),
            Ok(_) => {}
        }
        directory_source(&folder)?;
        let mut paths = fs::read_dir(&folder)
            .map_err(|e| format!("library entries unreadable: {e}"))?
            .map(|entry| entry.map(|entry| entry.path()))
            .collect::<Result<Vec<_>, _>>()
            .map_err(|e| format!("library entry listing incomplete: {e}"))?;
        paths.sort();
        let mut rows = Vec::new();
        for path in paths {
            let name = path.file_name().and_then(|name| name.to_str());
            let reference = crate::util::opaque_id("workflow-library-entry:")?;
            let mut row = json!({"reference":reference,"name":name.unwrap_or("unreadable native name"),"path":crate::attachments::native_path_identity(&path),
                "content":Value::Null,"state":"not established","reviewable":false,"findings":[]});
            let read = (|| {
                let name = name
                    .filter(|name| super::super::valid_name(name))
                    .ok_or("HY-2: library entry name is not a valid workflow name")?;
                let source = directory_source(&path)?;
                drafts::prescan(&path)?;
                let snapshot = Snapshot::capture(&path)?;
                if directory_source(&path)? != source {
                    return Err("entry source changed while observed".to_owned());
                }
                // Source tuple validation is separate from hygiene/name checks.
                snapshot.identity(&owner.origin, &owner.source_root, name, None)?;
                let slot = slot_lines(&ledger, &owner.origin, &owner.source_root, name)
                    .into_iter()
                    .collect::<Vec<_>>();
                let prior = latest(&slot)?;
                let mut findings = snapshot.hygiene_findings();
                if super::super::declared_name(&snapshot).as_deref() != Some(name) {
                    findings
                        .push("HY-2: front-matter name differs from the library entry name".into());
                }
                row["content"] = json!({"method":SNAPSHOT_METHOD,"value":snapshot.revision()});
                row["fileCount"] = json!(snapshot.files().len());
                row["bytes"] = json!(snapshot.files().values().map(Vec::len).sum::<usize>());
                row["findings"] = json!(findings);
                match prior {
                    Some(identity) => {
                        let line = slot
                            .iter()
                            .rev()
                            .find(|line| line["outcome"] == "registered")
                            .ok_or("registered slot line unavailable")?;
                        match owner.standing_as_read(line, &identity) {
                            Ok(_) if identity.revision == snapshot.revision() => {
                                row["state"] = json!("registered copy as read");
                                row["limit"] = json!("Use the registered revision's Select or Refine controls; this listing restores no hot selection authority");
                            }
                            Ok(_) => {
                                row["state"] = json!("library copy changed outside registration");
                                row["limit"] = json!("Registered revisions are retained; review a draft made from the registered revision, not this copy as a new in-place entry");
                            }
                            Err(cause) => {
                                row["state"] =
                                    json!("registration record incomplete or unreadable");
                                row["limit"] = json!(cause);
                            }
                        }
                    }
                    None => {
                        row["state"] = json!("present without registration record");
                        if findings.is_empty() {
                            row["reviewable"] = json!(true);
                            self.selected.insert(
                                reference.clone(),
                                ListedEntry {
                                    name: name.into(),
                                    revision: snapshot.revision().into(),
                                    source,
                                    slot,
                                },
                            );
                        } else {
                            row["limit"] =
                                json!("Refusing hygiene findings; not offered for review");
                        }
                    }
                }
                Ok::<(), String>(())
            })();
            if let Err(cause) = read {
                row["limit"] = json!(cause);
            }
            rows.push(row);
        }
        if directory_source(&owner.root)? != root || read_ledger(&owner.root)? != ledger {
            return Err("library source or ledger changed while observed; refresh entries".into());
        }
        self.root_source = Some(root);
        self.view["entries"] = json!(rows);
        Ok(())
    }
    pub(crate) fn view(&self) -> Value {
        self.view.clone()
    }
    fn validate(
        &self,
        owner: &LibraryOwner,
        library: &str,
        listing: &str,
        refs: &[String],
    ) -> Result<Vec<String>, String> {
        if self.library != library || self.reference != listing {
            return Err("The displayed library observation changed; refresh before review".into());
        }
        if self.root_source.as_ref() != Some(&directory_source(&owner.root)?) {
            return Err("Original observed library source changed; no review retarget".into());
        }
        if refs.is_empty() {
            return Err("Choose one or more listed entries".into());
        }
        let ledger = read_ledger(&owner.root)?;
        let mut seen = std::collections::BTreeSet::new();
        let mut names = Vec::new();
        for reference in refs {
            if !seen.insert(reference) {
                return Err("Duplicate chosen library entry".into());
            }
            let entry = self
                .selected
                .get(reference)
                .ok_or("Chosen entry is absent or was not offered for review")?;
            let path = owner.root.join(PUBLISHED).join(&entry.name);
            if directory_source(&path)? != entry.source {
                return Err("Original listed entry source changed; refresh before review".into());
            }
            drafts::prescan(&path)?;
            let snapshot = Snapshot::capture(&path)?;
            if snapshot.revision() != entry.revision
                || !snapshot.hygiene_findings().is_empty()
                || directory_source(&path)? != entry.source
            {
                return Err("Listed entry content changed; refresh before review".into());
            }
            let slot: Vec<_> = slot_lines(&ledger, &owner.origin, &owner.source_root, &entry.name)
                .into_iter()
                .collect();
            if slot != entry.slot || latest(&slot)?.is_some() {
                return Err(
                    "Listed entry registration standing changed; refresh before review".into(),
                );
            }
            names.push(entry.name.clone());
        }
        Ok(names)
    }
    pub(crate) fn review(
        &self,
        owner: &LibraryOwner,
        library: &str,
        listing: &str,
        refs: &[String],
    ) -> Result<ReviewSession, String> {
        let names = self.validate(owner, library, listing, refs)?;
        let mut review = owner.review_in_place(&names)?;
        let current = review.current()?;
        let frozen: Vec<_> = current.ordered_bindings().collect();
        if frozen.len() != refs.len()
            || frozen.iter().zip(refs).any(|(binding, reference)| {
                self.selected[reference].revision != binding.subject().revision
            })
        {
            return Err(
                "Frozen in-place review differs from chosen listed content; refresh entries".into(),
            );
        }
        drop(current);
        self.validate(owner, library, listing, refs)?;
        let mut sources = vec![(
            owner.root.clone(),
            self.root_source
                .clone()
                .ok_or("original library source absent")?,
        )];
        sources.extend(refs.iter().map(|reference| {
            let entry = &self.selected[reference];
            (
                owner.root.join(PUBLISHED).join(&entry.name),
                entry.source.clone(),
            )
        }));
        review.listed_sources = Some(ListedSources(sources));
        review.current()?;
        Ok(review)
    }
}
