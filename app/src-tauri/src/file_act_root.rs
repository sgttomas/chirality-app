//! Root-owned hot file offers. Display references cannot reconstruct custody.
use crate::{
    act_control::{ActControl, FileActKind, FileActOfferRef},
    runtime_session::HomeSession,
};
use serde_json::{json, Value};
use std::{
    collections::BTreeMap,
    path::Path,
    sync::{Arc, Mutex},
};

#[derive(Default)]
pub(crate) struct FileActRoot {
    pub offers: BTreeMap<String, Arc<Mutex<FileActReview>>>,
}
pub(crate) struct FileActReview {
    pub offer: FileActOfferRef,
    pub home: Arc<HomeSession>,
    pub context: Value,
    pub preview: Value,
    pub attempted: bool,
    pub status: Value,
}
impl FileActRoot {
    pub fn compose(
        &mut self,
        control: &mut ActControl,
        path: &Path,
        kind: FileActKind,
        scope: &str,
        purpose: &str,
        home: Arc<HomeSession>,
        context: Value,
    ) -> Result<Value, String> {
        let offer = control.compose_file_act(path, kind, scope, purpose)?;
        let (facts, bytes) = control.file_act_preview(&offer)?;
        let preview = json!({"reference":offer.id(),"offer":facts,"byteLength":bytes.len(),"utf8":std::str::from_utf8(bytes).ok(),"hex":bytes.iter().map(|b|format!("{b:02x}")).collect::<String>(),"previewStanding":"exact frozen bytes; selection and preview are not act evidence"});
        let reference = offer.id().to_owned();
        self.offers.insert(
            reference,
            Arc::new(Mutex::new(FileActReview {
                offer,
                home,
                context,
                preview: preview.clone(),
                attempted: false,
                status: json!({"state":"composed; no capture","recorded":false}),
            })),
        );
        Ok(preview)
    }
    pub fn get(&self, id: &str) -> Result<Arc<Mutex<FileActReview>>, String> {
        self.offers
            .get(id)
            .cloned()
            .ok_or("Original hot file offer unavailable; review again".into())
    }
    pub fn snapshot(&self) -> Value {
        json!(self.offers.iter().map(|(reference,owner)|match owner.try_lock(){
            Ok(owner)=>json!({"reference":reference,"offer":owner.preview["offer"],"attempted":owner.attempted,"status":owner.status}),
            Err(_)=>json!({"reference":reference,"state":"original native operation pending"}),
        }).collect::<Vec<_>>())
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    fn fixture() -> (std::path::PathBuf, Arc<HomeSession>) {
        let root = std::fs::canonicalize(std::env::temp_dir())
            .unwrap()
            .join(crate::util::opaque_id("file-root-").unwrap());
        std::fs::create_dir(&root).unwrap();
        std::fs::write(root.join("output.txt"), b"reviewed bytes\n").unwrap();
        let home = Arc::new(
            HomeSession::new(
                crate::home_resources::HomeClass::Account,
                Arc::new(crate::hosting::Host::new()),
                Err("synthetic offline fixture".into()),
            )
            .unwrap(),
        );
        (root, home)
    }
    #[test]
    fn each_kind_keeps_original_offer_and_exact_preview_after_file_change() {
        let (root, home) = fixture();
        let mut control = ActControl::new(&root);
        let mut session = FileActRoot::default();
        for kind in [FileActKind::Check, FileActKind::Approve, FileActKind::Rely] {
            std::fs::write(root.join("output.txt"), b"reviewed bytes\n").unwrap();
            let preview = session
                .compose(
                    &mut control,
                    &root.join("output.txt"),
                    kind,
                    "explicit scope",
                    "explicit purpose",
                    home.clone(),
                    json!({"offline":"fixture"}),
                )
                .unwrap();
            let reference = preview["reference"].as_str().unwrap();
            let owner = session.get(reference).unwrap();
            std::fs::write(root.join("output.txt"), b"different").unwrap();
            let owner = owner.lock().unwrap();
            assert_eq!(owner.preview["utf8"], "reviewed bytes\n");
            assert_eq!(owner.preview["offer"]["actKind"], kind.code());
            assert_eq!(
                control.file_act_preview(&owner.offer).unwrap().1,
                b"reviewed bytes\n"
            );
            assert!(!owner.attempted);
        }
        assert!(session.get("renderer fabricated reference").is_err());
        assert_eq!(session.offers.len(), 3);
        assert!(!root.join(".chirality/records").exists());
        std::fs::remove_dir_all(root).unwrap();
    }
    #[test]
    fn root_snapshot_does_not_wait_for_native_owner_and_preserves_original() {
        let (root, home) = fixture();
        let mut control = ActControl::new(&root);
        let mut session = FileActRoot::default();
        let preview = session
            .compose(
                &mut control,
                &root.join("output.txt"),
                FileActKind::Check,
                "scope",
                "purpose",
                home,
                json!({}),
            )
            .unwrap();
        let owner = session.get(preview["reference"].as_str().unwrap()).unwrap();
        let held = owner.lock().unwrap();
        assert_eq!(
            session.snapshot()[0]["state"],
            "original native operation pending"
        );
        drop(held);
        assert_eq!(
            session.snapshot()[0]["status"]["state"],
            "composed; no capture"
        );
        std::fs::remove_dir_all(root).unwrap();
    }
}
