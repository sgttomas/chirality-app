//! A workflow's own text, read for a person before they choose it or before a
//! run starts (DEL-02-02 AC-010, journey 1: "sees its source and revision").
//!
//! This is a read and nothing else. It resolves the workflow through the same
//! resolution a selection and a run use (`select_bundle_package` for an entry
//! of the included catalogue, `verify_store` for the conversation's current
//! selection) and returns the `WORKFLOW.md` text of the bytes that resolution
//! holds, which are the bytes a run's text is composed from. It creates no file
//! or folder and changes no selection, library, run or record. A caller's name
//! is looked up in the compiled catalogue; it is never joined to a folder.
//!
//! What it says of the text is only what the host established: which identity
//! it was read for, and that the bytes read hashed to that identity's revision
//! when read. It says nothing of what the workflow requires, whether its tools
//! or files are available, or whether it will work (RELEASE_LIMITATIONS LIM-008).
//! When the bytes cannot be tied to the identity, no text is returned.
use crate::workflow_workspace::{Selection, WorkflowIdentity};
use serde::Deserialize;
use serde_json::{json, Value};
use std::path::Path;

/// What the person asked to read, as the view showed it.
#[derive(Clone, Debug, Deserialize)]
#[serde(rename_all = "camelCase", deny_unknown_fields)]
pub(crate) struct Target {
    /// "included": an entry of the App's included catalogue, by `name`.
    /// "selection": the workflow chosen for the context's conversation (or the
    /// inspected one when the context names no conversation), of any origin.
    pub kind: String,
    #[serde(default)]
    pub name: Option<String>,
    /// The revision the view showed. A different revision now is refused.
    pub revision: String,
}

pub(crate) const INCLUDED: &str = "included";
pub(crate) const SELECTION: &str = "selection";

/// The state of a read whose bytes matched the identity.
pub(crate) const READ: &str = "read";
/// The state of a read that returned no text.
pub(crate) const REFUSED: &str = "refused";

/// The standing said with the text: what the host established, and no more.
pub(crate) const STANDING: &str = "read by the App when asked; its files hashed to this revision's identity when read; nothing in the text was checked or run";

fn target_view(target: &Target) -> Value {
    json!({"kind":target.kind,"name":target.name,"revision":target.revision})
}

/// A refusal: the reason in plain words, the host's own cause where there is
/// one, and no text.
pub(crate) fn refused(target: &Target, identity: Option<&WorkflowIdentity>, reason: &str, cause: Option<&str>) -> Value {
    json!({"state":REFUSED,"target":target_view(target),"identity":identity.map(|i|json!(i)),
        "reason":reason,"cause":cause,"standing":"no text was returned"})
}

/// The text of `selection`, which a resolution has just read from `package`,
/// after `verify_store` reads `package` again and the held bytes are compared
/// with the identity. `revision` is the revision the view showed.
fn resolved(target: &Target, selection: &Selection, package: &Path) -> Value {
    let identity = selection.identity();
    if identity.revision != target.revision {
        return refused(target, Some(identity), "the workflow shown is not the one the App holds now; wait for the view to refresh, then read it again", None);
    }
    let snapshot = selection.snapshot();
    if snapshot.revision() != identity.revision {
        return refused(target, Some(identity), "the files the App holds for this workflow do not match its revision", None);
    }
    if let Err(cause) = selection.verify_store(package) {
        return refused(target, Some(identity), "the App could not read this revision's files and tie them to its identity", Some(&cause));
    }
    let text = snapshot.workflow_text();
    let files = snapshot
        .files()
        .iter()
        .filter(|(path, _)| path.as_str() != "WORKFLOW.md")
        .map(|(path, bytes)| json!({"path":path,"bytes":bytes.len()}))
        .collect::<Vec<_>>();
    json!({"state":READ,"target":target_view(target),"identity":identity,"text":text,"bytes":text.len(),
        "files":files,"matched":true,"standing":STANDING})
}

/// An entry of the included catalogue, by name, resolved from this App's own
/// installed workflow resources (`bundle`, or why none) exactly as selecting it
/// would resolve it, without selecting it.
pub(crate) fn included(bundle: Result<std::path::PathBuf, String>, target: &Target) -> Value {
    use crate::workflow_workspace::production_catalog::ProductionCatalog;
    let Some(name) = target.name.as_deref() else {
        return refused(target, None, "no included workflow was named", None);
    };
    let catalog = match ProductionCatalog::load() {
        Ok(catalog) => catalog,
        Err(cause) => return refused(target, None, "the App's list of included workflows is not available", Some(&cause)),
    };
    // Looked up, never joined: a name the compiled catalogue does not hold
    // reaches no folder.
    let Ok(identity) = catalog.identity(name) else {
        return refused(target, None, "no workflow included with this App has that name", None);
    };
    if identity.revision != target.revision {
        return refused(target, Some(identity), "the workflow shown is not the one the App holds now; wait for the view to refresh, then read it again", None);
    }
    let root = match bundle {
        Ok(root) => root,
        Err(cause) => return refused(target, Some(identity), "the App's included workflows could not be verified", Some(&cause)),
    };
    match catalog.select_bundle_package(&root, name) {
        Ok(package) => resolved(target, package.selection(), package.package_path()),
        Err(cause) => refused(target, Some(identity), "the App could not read this revision's files and tie them to its identity", Some(&cause)),
    }
}

/// The conversation's current selection (or the inspected one), of any origin,
/// at the location it was resolved from.
pub(crate) fn chosen(choice: Option<(&Selection, &Path)>, target: &Target) -> Value {
    if target.name.is_some() {
        return refused(target, None, "a chosen workflow is read without a name", None);
    }
    match choice {
        None => refused(target, None, "no workflow is chosen for this conversation now", None),
        Some((selection, package)) => resolved(target, selection, package),
    }
}

/// The two targets, and nothing else.
pub(crate) fn kind_known(target: &Target) -> Result<(), String> {
    match target.kind.as_str() {
        INCLUDED | SELECTION => Ok(()),
        _ => Err("Unknown workflow text target; nothing read".into()),
    }
}
