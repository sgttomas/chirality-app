# Frozen proposed Root API — file-act core

Private App source: `/private/tmp/chirality-file-act-core-r1-qjq4v6uf/app`.
Only prepared, not compiled, tested, integrated or qualified.

All these items are crate-visible through `crate::act_control`:

```rust
pub(crate) enum FileActKind { Check, Approve, Rely }
pub(crate) struct FileActOfferRef { /* private; no Clone/serde/factory */ }
impl FileActOfferRef { fn id(&self) -> &str; }
impl ActControl {
    fn compose_file_act(&mut self, path: &Path, kind: FileActKind,
                        scope: &str, purpose: &str) -> Result<FileActOfferRef, String>;
    fn file_act_preview(&self, offer: &FileActOfferRef)
        -> Result<(&Value, &[u8]), String>;
    fn dismiss_file_act(&mut self, offer: &FileActOfferRef);
    fn continue_file_act(&mut self, offer: &FileActOfferRef) -> Result<Value, String>;
}
fn confirm_file_native(app: &tauri::AppHandle, control: &mut ActControl,
                       offer: &FileActOfferRef,
                       observe: impl FnMut() -> Result<(Value, Value), String>)
    -> Result<Option<Value>, String>;
```

Root retains the opaque offer reference in owning state; expose a display ID only to renderer. Root resolves an explicit selected App file/output to its physical absolute path inside the current workspace. `compose_file_act` reads/binds exact bytes and requires explicit nonempty scope/purpose. The preview is the original bound byte buffer; rendering newer bytes as this preview is invalid. Selection/preview are no act evidence.

Native entry is async/off the UI thread. Root retains original ActControl ownership while the dialog is open; do not acquire Root/home locks in an order that recurs into the control lock. `observe` reads actual current actor and current owning workspace/home/session context from Root, before and after the dialog. It must not return renderer-supplied actor/context. Actor needs observed nonempty OS account, identityVerified:false; optional App name and Codex account follow the existing actor facility. A7 native wording explicitly makes professional standing the person's own statement. A6 wording explicitly names the accountable person's statement.

`confirm_file_native` itself freezes the offer, shows a three-button native dialog (exact act wording / Decline this act / Cancel), admits only actual native custom result labels, rereads observed context and current file content, and constructs the opaque event. There is no production native flag, event constructor or serde path. `Ok(None)` is dismiss/cancel, no capture. `Ok(Some(value))` reports AC-7 recorded or AC-8 original capture pending; an error before capture has no act. Definite first capture failure captures nothing. Uncertain publication and admitted-capture record failure are separate states, with continuation rules specified below.

This first core API is standing-only (`answers.standing`), not arrival/request receiving. Do not synthesize arrival or request references. All existing A15/A16 functions and public signatures are unchanged. No Root/UI or file-act reader has been implemented. Root consumer must keep file acts/declines separate from decision-package A16 views, display A7/identity limits, and preserve the exact capture/record standing. General lapse reading and other applicable entry surfaces remain its work.

## V5 repair — superseding failure semantics

Signatures are unchanged. Definite initial capture-lock or prepublication failure returns an error explicitly saying nothing captured, dismisses/consumes that offer, and adds no admitted hot capture or retry identity. The person must review/confirm a new offer. Native input alone is not admission.

An attempted publication with failed/uncertain durability returns `state: capture publication uncertain`, `captureId`, `captureDurability: not established`, `recorded: false`, `writeFailure`. Original native facts stay in the original offer's separate uncertain slot, outside the admitted writer queue. This state is neither AC-7 nor AC-8; never render it as a recorded or record-pending act. `continue_file_act` on the same retained original reference reads the stored capture, requires exact original-fact equality and successful complete publication sync, then admits it and drains the record queue. It never creates/rewrites absent or mismatching uncertain bytes. Missing/unreadable/mismatching bytes retain the uncertainty result. Generic `recover_pending` cannot admit this original uncertain event; a cold file remains unverified.

Only after complete durable publication does the capture enter the ordinary hot queue; subsequent record failure remains AC-8 with original facts and ordinary ordered retry, without recapture. Generic refresh handles those already admitted captures. Read/source checks now use O_NONBLOCK | O_NOFOLLOW plus descriptor regular-file validation, including replacements after the named precheck. No API claim of event/capture chronological ordering is added for uncertainty not yet admitted; capture timestamps remain original observations.

Actual native three-button/context/cancellation behavior remains unobserved.
