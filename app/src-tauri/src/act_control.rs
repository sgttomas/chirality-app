//! App act control, A16 "decide" only.
//!
//! DEL-01-04 APP_ACT_CONTROL.md (AAC-v0.3):
//! - §1.2 row A16: one decision package per act, wording "decide", no decline,
//!   actor the person, subject bound by the package file's content identity,
//!   the alternative chosen, relation to its `act_request`;
//! - §2 AI-9: the package reaches the control as a runtime value from the decision
//!   view; absent or changed package file -> not offered; fewer than two alternatives
//!   -> not offered;
//! - §3 transitions AX-01, AX-02, AX-03, AX-04, AX-05, AX-06, AX-08, AX-12, AX-13,
//!   and the refusals listed under the table (capture from AC-1, second capture);
//! - §4.1 steps 2-7 (compose from authoritative sources, present, re-read identity,
//!   capture evidence, write the record), AK-c, AK-e;
//! - §5.1 offer + offer digest, §5.2 capture evidence, §5.3 the RS entry;
//! - §6.1 NA-3/NA-4: only a host-native confirmation captures (the Tauri layer
//!   presents a native dialog; see lib.rs); §7 the person's identity.
//!
//! The RS `human_act` body follows DEL-04-03 RECORD_SEMANTICS.md §6.1 (A16 rows)
//! and HA-11; act class from DEL-04-01 ACT_AND_POLICY_CONTRACT.md §2.1 (A16,
//! "person's act (V4-PM-04)").

use crate::canonical::{offer_digest, OFFER_DIGEST_METHOD};
use crate::records::{self, APP_INTERFACE};
use crate::recorder::LOG;
use crate::util::{file_identity, now_rfc3339, FILE_IDENTITY_METHOD};
use serde_json::{json, Value};
use std::collections::HashMap;
use std::path::{Path, PathBuf};

pub const CAPTURE_STORE: &str = ".chirality/captures";
const STANDING: &str = "no arrival: a standing act (RC-6)";

#[derive(Clone, Copy, Debug, PartialEq)]
pub enum InputSource {
    /// The host-owned native confirmation (§6.2 P-2).
    HostNativeConfirmation,
    WebviewScript,
    AgentTool,
    AppRule,
}

impl InputSource {
    fn label(self) -> &'static str {
        match self {
            InputSource::HostNativeConfirmation => "host-native-confirmation",
            InputSource::WebviewScript => "a webview script",
            InputSource::AgentTool => "an agent tool",
            InputSource::AppRule => "an App rule",
        }
    }
}

#[derive(Clone, Debug, PartialEq)]
pub enum OfferState {
    Composed,  // AC-1
    Presented, // AC-2
    Captured,  // AC-3
    Dismissed, // AC-5
    Stale,     // AC-6
    Recorded,  // AC-7
    RecordPending, // AC-8
}

pub struct OfferSlot {
    pub offer: Value,
    pub state: OfferState,
    pub package_path: PathBuf,
}

pub struct ActControl {
    pub workspace: PathBuf,
    pub offers: HashMap<String, OfferSlot>,
    counter: u64,
}

/// The person as the App observes them (AAC §7; RS $defs/person; identity never verified).
pub fn person(display_name: Option<&str>, os_account: Option<&str>) -> Value {
    let mut p = json!({"identityVerified": false});
    if let Some(n) = display_name.filter(|s| !s.is_empty()) {
        p["displayName"] = json!(n);
    }
    if let Some(a) = os_account.filter(|s| !s.is_empty()) {
        p["osAccount"] = json!(a);
    }
    // Codex account: absent unless Codex reports one (never guessed); not signed in here.
    p
}

impl ActControl {
    pub fn new(workspace: &Path) -> Self {
        ActControl { workspace: workspace.to_path_buf(), offers: HashMap::new(), counter: 0 }
    }

    /// AX-01 / AX-02. Compose an A16 offer for the `act_request` `request_ref`.
    pub fn compose_a16(&mut self, request_ref: &str) -> Result<Value, String> {
        let (entries, _) = records::read_log(&self.workspace.join(LOG));
        let req = entries
            .iter()
            .find(|e| e["recordId"] == json!(request_ref) && e["kind"] == "act_request")
            .ok_or_else(|| format!("not offered: no act_request {request_ref} in the record"))?;
        let b = &req["body"];
        if b["form"] != "decision package file" || b["actKind"] != "A16" {
            return Err("not offered: the control serves A16 only on a decision package (AAC §1.2)".into());
        }
        let rel = b["evidence"]["ref"].as_str().ok_or("not offered: the request names no package file")?;
        let path = self.workspace.join(rel);
        // AI-1 / AI-9: the subject's identity at compose.
        let now = file_identity(&path).ok_or("not offered: the subject's content identity is not obtainable")?;
        if b["evidence"]["claimedIdentity"].as_str() != Some(now.as_str()) {
            return Err("not offered: the package file changed since the request was recorded (AI-9)".into());
        }
        // NA-2: compose from authoritative sources: the package file itself and the record.
        let pkg: Value = serde_json::from_slice(&std::fs::read(&path).map_err(|e| e.to_string())?)
            .map_err(|e| format!("not offered: package file unreadable: {e}"))?;
        let alts = pkg["alternatives"].as_array().cloned().unwrap_or_default();
        if alts.len() < 2 {
            return Err("not offered: the package names fewer than two alternatives (AI-9)".into());
        }
        let scope = pkg.get("scope").and_then(|s| s.as_str()).unwrap_or("");
        if scope.is_empty() {
            // CONTRACT_ISSUES CI-4: the package file may omit scope; the offer requires it.
            return Err("not offered: the package names no scope, which the offer requires (aac.offer scope minLength 1)".into());
        }
        self.counter += 1;
        let offer_id = format!("offer:{}:{}", request_ref.trim_start_matches("rec:").replace(':', "-"), self.counter);
        let mut offer = json!({
            "format": "chirality.aac.offer", "formatVersion": "0.3", "offerId": offer_id,
            "actKind": "A16", "wording": "decide",
            "subject": {"class": "App file", "ref": rel,
                        "contentIdentity": {"method": FILE_IDENTITY_METHOD, "value": now}},
            "scope": scope, "purpose": pkg["purpose"], "actorRequirement": "the person",
            "declineAvailable": false, "answers": {"standing": STANDING},
            "requestRef": request_ref, "composedAt": now_rfc3339(),
            "alternatives": alts.iter().map(|a| json!({
                "id": a["id"], "statement": a["statement"], "consequences": a["consequences"]})).collect::<Vec<_>>(),
        });
        let digest = offer_digest(&offer)?;
        offer["offerDigest"] = json!({"method": OFFER_DIGEST_METHOD, "value": digest});
        self.offers.insert(offer_id.clone(), OfferSlot { offer: offer.clone(), state: OfferState::Composed, package_path: path });
        Ok(offer)
    }

    /// AX-03: the host shows the offer in its native confirmation.
    pub fn present(&mut self, offer_id: &str) -> Result<(), String> {
        let s = self.offers.get_mut(offer_id).ok_or("no such offer")?;
        if s.state != OfferState::Composed {
            return Err(format!("cannot present an offer in state {:?}", s.state));
        }
        s.state = OfferState::Presented;
        Ok(())
    }

    /// AX-05.
    pub fn dismiss(&mut self, offer_id: &str) {
        if let Some(s) = self.offers.get_mut(offer_id) {
            if s.state == OfferState::Presented {
                s.state = OfferState::Dismissed;
            }
        }
    }

    /// The text the native confirmation shows, composed by the host from the offer (§6.2 P-2).
    pub fn confirmation_text(&self, offer_id: &str, alternative: &str, actor: &Value) -> Result<String, String> {
        let s = self.offers.get(offer_id).ok_or("no such offer")?;
        let o = &s.offer;
        let alt = o["alternatives"].as_array().unwrap().iter().find(|a| a["id"] == json!(alternative))
            .ok_or("the package names no such alternative")?;
        let who = [actor.get("displayName"), actor.get("osAccount")].iter()
            .filter_map(|v| v.and_then(|x| x.as_str())).collect::<Vec<_>>().join(" / ");
        let cons = alt["consequences"].as_array().unwrap().iter()
            .filter_map(|c| c.as_str()).map(|c| format!("  - {c}")).collect::<Vec<_>>().join("\n");
        Ok(format!(
            "Decide (A16)\n\nPackage: {}\nContent identity: {}\nPurpose: {}\nScope: {}\n\nChosen alternative: {} — {}\nConsequences:\n{}\n\nActor: {} (identity not verified)\nAnswers: {}\nNo decline exists for A16; Cancel closes the control.",
            o["subject"]["ref"].as_str().unwrap_or(""),
            o["subject"]["contentIdentity"]["value"].as_str().unwrap_or(""),
            o["purpose"].as_str().unwrap_or(""),
            o["scope"].as_str().unwrap_or(""),
            alternative, alt["statement"].as_str().unwrap_or(""), cons, who, STANDING))
    }

    /// AX-04, AX-06, AX-08, then AX-12/AX-13. Returns {state, capture, record?}.
    pub fn confirm(&mut self, offer_id: &str, alternative: &str, source: InputSource, actor: Value) -> Result<Value, String> {
        if source != InputSource::HostNativeConfirmation {
            // AX-04 (CAP-4): unchanged; nothing captured.
            return Err(format!("not operable from {}", source.label()));
        }
        let ws = self.workspace.clone();
        let slot = self.offers.get_mut(offer_id).ok_or("no such offer")?;
        match slot.state {
            OfferState::Presented => {}
            OfferState::Composed => return Err("refused: capture from an offer not presented".into()),
            ref s => return Err(format!("refused: the offer is {s:?}; a second capture is refused")),
        }
        let o = slot.offer.clone();
        if !o["alternatives"].as_array().unwrap().iter().any(|a| a["id"] == json!(alternative)) {
            return Err("refused: the package names no such alternative; nothing captured".into());
        }
        // NA-4: the confirmation is for the presented offer (identity and digest).
        if offer_digest(&o)? != o["offerDigest"]["value"].as_str().unwrap_or("") {
            return Err("refused: offer digest does not match the presented offer".into());
        }
        // AK-c: re-read the subject's identity (§4.1 step 5).
        let now = file_identity(&slot.package_path);
        if now.as_deref() != o["subject"]["contentIdentity"]["value"].as_str() {
            slot.state = OfferState::Stale; // AX-06
            return Err("content changed since it was shown: review it again (AC-6); nothing captured".into());
        }
        // §4.1 step 6: capture evidence (§5.2), before any record (AK-e).
        let request_ref = o["requestRef"].as_str().unwrap().to_string();
        let capture_id = format!("cap:decide-{}", offer_id.trim_start_matches("offer:"));
        let bound = o["subject"]["contentIdentity"].clone();
        let mut capture = json!({
            "format": "chirality.aac.capture-evidence", "formatVersion": "0.3",
            "captureId": capture_id, "offerId": offer_id, "offerDigest": o["offerDigest"],
            "choice": "act", "actKind": "A16", "actor": actor,
            "boundSubject": [format!("decision package {request_ref}")],
            "boundContent": [bound],
            "scope": o["scope"], "purpose": o["purpose"], "capturedAt": now_rfc3339(),
            "surface": "App interface", "inputSource": "host-native-confirmation",
            "answers": o["answers"], "requestRef": request_ref, "alternativeChosen": alternative,
            "evidenceLimits": ["identity not verified"],
        });
        let store = ws.join(CAPTURE_STORE);
        let cap_file = store.join(format!("{}.json", capture_id.replace(':', "_")));
        let write_cap = |c: &Value| -> Result<(), String> {
            std::fs::create_dir_all(&store).map_err(|e| e.to_string())?;
            let mut bytes = serde_json::to_vec_pretty(c).map_err(|e| e.to_string())?;
            bytes.push(b'\n');
            std::fs::write(&cap_file, bytes).map_err(|e| e.to_string())
        };
        if let Err(e) = write_cap(&capture) {
            return Err(format!("the capture store cannot be written ({e}); nothing captured, nothing counts"));
        }
        slot.state = OfferState::Captured; // AX-08
        // §4.1 step 7 / §5.3: the RS human_act, direct capture, through the writer.
        let body = json!({
            "actKind": "A16",
            "actClass": {"value": "person's act (V4-PM-04)"},
            "decisionActor": capture["actor"],
            "recordingMode": "direct capture",
            "boundSubject": capture["boundSubject"],
            "boundContent": capture["boundContent"],
            "scope": capture["scope"], "purpose": capture["purpose"],
            "captureEvidence": [{"kind": "capture evidence", "ref": capture_id, "resolutionAtWrite": "resolved"}],
            "captureTime": capture["capturedAt"],
            "evidenceLimits": ["identity not verified"],
            "relations": {"requestRef": request_ref, "alternativeChosen": alternative},
        });
        match records::append(&ws.join(LOG), "human_act", &APP_INTERFACE, body) {
            Ok(rec) => {
                slot.state = OfferState::Recorded; // AX-12
                // §5.2: "the RS record identity once written" (CONTRACT_ISSUES CI-6).
                capture["recordId"] = rec["recordId"].clone();
                let _ = write_cap(&capture);
                Ok(json!({"state": "AC-7 recorded", "capture": capture, "record": rec,
                          "captureFile": cap_file.display().to_string()}))
            }
            Err(e) => {
                slot.state = OfferState::RecordPending; // AX-13; late write (W-2) not in the skeleton
                Ok(json!({"state": "AC-8 record pending", "capture": capture, "writeFailure": e}))
            }
        }
    }
}
