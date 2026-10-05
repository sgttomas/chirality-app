# V1-ACT-R1 — same-reviewer repair backcheck

2026-10-04. **NOT READY: ACT-6 remains blocking at this frozen R1 candidate.** ACT-1/2/3/4/5/7/8 have supported bounded repairs; trustworthy persistent cold replay remains required unfinished work under CC-CUST and is not closed by this backcheck.

Independent TASK `/root/group_a_execution/contract_reviewer`, native descendant of WORKING_ITEMS `/root/group_a_execution`; supplied Codex gpt-6.1-sol/medium, no substitution/diversity claim or delegation. Applied already-loaded software-code-review. Read exact successor return, repaired source/test/UI files, original findings, V0-CUST and relevant admitted custody semantics. All nine R1 output hashes matched before/after checking. Original V1-ACT and P0-ACT remain historical. No product, Design or Git changes; no network, auth, downloads or live Codex/model execution. Only durable review output is this file. Temporary harness/workspace removed after execution; test actors remain native-event stand-ins.

## Remaining actionable blocking finding

**ACT-6-R1 [P1] A new confirmation can overtake an older hot pending submission.**

Locations: `app/src-tauri/src/act_control.rs`, confirm's direct recover_capture call (`account_delay=true`) versus recover_pending's sorted native-event queue; `app/src-tauri/src/lib.rs` decision_view currently identifies packages before pending recovery. The repaired writer correctly retains observedAt and appends delay limits during an explicit batch retry, but that is not applied at the next fresh append.

Concrete trigger independently reproduced:

1. Compose/present two package offers A and B.
2. Introduce a torn suffix in the owning log; confirm A through the native-event test stand-in. A remains hot and AC-8 pending.
3. Restore the exact pre-fault log bytes as explicit **test fixture** repair. Confirm fresh B before calling recover_pending. B returns AC-7 and appends immediately.
4. Call recovery. The original A appends after B, yielding human-act order **B,A**, despite native-event order **A,B**.

Impact: RS W-2 requires pending entries in their original order at the next append/retry, before continuation. Besides reordered provenance, decision views deriving latest acts from log order can prefer an earlier decision after a later one. The existing hot_pending_batch test makes both acts fail, then retries together; it does not cover a later fresh success while A is already pending. A new recorder request/limit append on Refresh can similarly pass ahead of pending act flush because lib.rs calls identify_packages first.

Repair direction: put the writer-owned pending queue into the append/continuation boundary. Flush admitted hot pending submissions in native-event order before any new corresponding append, or refuse/hold that append until the queue is reconciled. Preserve stable IDs, captured facts/observedAt, W-1 validation, batch acts-before-delay-limits, cold unverified hold and already-recorded backlink-only behavior. Reconcile the recorder/Refresh ordering without making unsigned cold files authorize an act. Add both pending-A/fresh-B and pending-A/new-recorder-input regressions; do not weaken the ordering oracle.

## Original finding dispositions

| Finding | Backcheck |
|---|---|
| ACT-1 native-origin replay | Private native_captures proof is populated only by the normal native confirmation path, never reconstructed from JSON. Cold schema-valid matching files cannot append a new act; they retain exact origin-held wording. Existing matching claims permit only backlink repair with an explicit unverified-origin limit. Targeted forged-pending and publication-before-submission cold cases inspect unchanged bytes/no minted ID/no new log. Containment repair passes; actual admitted persistent replay remains unfinished as CC-CUST requires. |
| ACT-2 atomic/durable publication | Complete synced temporary evidence is published via create-new hard link; backlink uses atomic rename. ensure_directory persists new ancestry and ancestor linkage; sync_publication covers log file and owning directories through project/library root, including existing-match recovery. Targeted partial-temp and directory-sync injection traverse the production helper. Source/fault coverage addresses original defects; no physical process-kill/power-loss guarantee claimed. |
| ACT-3 content snapshots | Recorder and compose parse/hash one observed byte buffer via package_snapshot; field/hash identity comes from that buffer. Confirmation separately compares current bytes. Alternating observed-buffer/file replacement test covers source fidelity without tolerating mismatch. Pass. |
| ACT-4 R-5 completeness | Per-log expected sequence detects first gap, duplicates, gaps and reorder as limits. Append/recovery gate on those limits. Gap/duplicate/out-of-order fixture covers no append/backlink, keeping malformed/partial/duplicate-record checks. Pass. |
| ACT-5 recorded versus backlink | Durable matching/append result remains AC-7 with backlinkPending/statusDetail on annotation failure. UI includes AC-7 backlink/delay-pending diagnostics; corrected test retains durable-record oracle and annotation-only retry. Pass. |
| ACT-6 delay account/order | Original observedAt, writer pending ID, referenced `record write failed`, repeated-limit de-dup and explicit batch ordering are implemented. Next-fresh-append integration remains failed as ACT-6-R1 above. |
| ACT-7 writer-owned identity | AAC durably publishes capture first; records::prepare_capture_submission then mints the writer ID. Mutable writer submission retained in hot memory before persistence; failed persistence does not remint. Failure-before-durability test observes no reservation. Cold publication-only capture holds without inventing submission. Pass at bounded hot implementation. |
| ACT-8 no-write census | Recursive census now covers project/decisions, legacy records and .chirality; deliberate relocated capture modification changes the census. Original no-write check now observes owning evidence tree. Pass. |

W-1/schema/API assets and Cargo dependency/checksum sets were not changed by R1 and were not subjected to a blanket repeated review/test. Existing author results (12 library, 17 act_storage, 4 decide_flow, 6 schema and npm build) remain author observations at their reported candidate; they do not establish repair of the connected-order defect. Kernel advisory locking does not establish fsync durability; no actual process death witness was added by this reviewer.

## Focused independent regression evidence

Parent released and granted the build-resource slot for this check. Reviewer used a temporary `rustc --test` harness linked to the already built current candidate library, so no product source or Cargo output was edited. Slot released immediately after the focused result.

Compile command, with temporary path substituted at runtime:

```sh
rustc --edition=2021 --test <reviewer-temp>/order.rs \
  --extern chirality_app_v4_lib=<app>/src-tauri/target/debug/deps/libchirality_app_v4_lib.rlib \
  --extern serde_json=<app>/src-tauri/target/debug/deps/libserde_json-285cf9e31e3ede2e.rlib \
  -L dependency=<app>/src-tauri/target/debug/deps \
  -L native=<each existing app/src-tauri/target/debug/build/*/out directory> \
  -o <reviewer-temp>/order-test
REVIEW_TMP_ROOT=<canonical reviewer-temp>/workspace \
REVIEW_FIXTURE=<app>/tests/fixtures/FX-DP1/project/decisions \
  <reviewer-temp>/order-test --nocapture
```

Compile exit 0. Focused test exit **101**, 0 passed / 1 failed at the final ordering assertion. Exact output:

```text
actual act order: ["rec:app:e4443650-d3e6-49fb-9a4e-6a3945980f54","rec:app:ead11543-2feb-47e7-ad1b-1799874f5aff"]
expected original native-event order: ["rec:app:ead11543-2feb-47e7-ad1b-1799874f5aff","rec:app:e4443650-d3e6-49fb-9a4e-6a3945980f54"]
assertion left == right failed: RS W-2: older pending A must precede fresh B at the next append
```

Harness SHA-256 `a3ec482c37c4e500036035b8abf154dbebf74c0cbc4d7cfe010929f8d089155e`. Cached linked App rlib SHA-256 `53aac37ded70ffee638553e70ddcaee64d34396120f3d933faafcd077090af6a`. The library includes separately repaired hosting code, but this harness calls no hosting/supplier function and gives no hosting verdict. A first harness launch failed before the scenario at the expected /var symlink guard; canonicalizing the reviewer-owned temp root corrected test setup. No product guard or criterion changed.

Exact harness input:

```rust
use chirality_app_v4_lib::{act_control::{person,ActControl,InputSource},recorder::{identify_packages,LOG},records};
use serde_json::json;
use std::path::PathBuf;
#[test]
fn older_hot_pending_must_precede_fresh_native_confirmation(){
 let root=PathBuf::from(std::env::var_os("REVIEW_TMP_ROOT").unwrap());
 std::fs::create_dir_all(root.join("project/decisions")).unwrap();
 let fixture=PathBuf::from(std::env::var_os("REVIEW_FIXTURE").unwrap());
 for name in ["PKG-1.json","PKG-2.json"]{std::fs::copy(fixture.join(name),root.join("project/decisions").join(name)).unwrap();}
 let requests=identify_packages(&root).unwrap();let mut ac=ActControl::new(&root);let actor=person(Some("Review fixture"),Some("review"));
 let mut ids=vec![];
 for req in &requests {let offer=ac.compose_a16(req["recordId"].as_str().unwrap()).unwrap();let id=offer["offerId"].as_str().unwrap().to_owned();ac.confirmation_text(&id,"ALT-1",&actor).unwrap();ac.present(&id).unwrap();ids.push(id);}
 let before=std::fs::read(root.join(LOG)).unwrap();let mut torn=before.clone();torn.extend(b"{torn");std::fs::write(root.join(LOG),torn).unwrap();
 let a=ac.confirm(&ids[0],"ALT-1",InputSource::HostNativeConfirmation,actor.clone()).unwrap();assert_eq!(a["state"],"AC-8 record pending");
 std::fs::write(root.join(LOG),before).unwrap();
 let b=ac.confirm(&ids[1],"ALT-1",InputSource::HostNativeConfirmation,actor).unwrap();assert_eq!(b["state"],"AC-7 recorded");
 ac.recover_pending().unwrap();
 let entries=records::read_log(&root.join(LOG)).0;let acts:Vec<_>=entries.iter().filter(|e|e["kind"]=="human_act").map(|e|e["body"]["relations"]["requestRef"].clone()).collect();
 let expected=vec![requests[0]["recordId"].clone(),requests[1]["recordId"].clone()];
 println!("actual act order: {}",json!(acts));println!("expected original native-event order: {}",json!(expected));
 assert_eq!(acts,expected,"RS W-2: older pending A must precede fresh B at the next append");
}
```

## Exact repaired candidate reviewed

| File | SHA-256 |
|---|---|
| `projects/chirality-app-v4/app/src-tauri/src/act_control.rs` | `f4975dad3bc902fc3c2ee2c6ff797f7bd5e2393efea2936d74dbb9af80201791` |
| `projects/chirality-app-v4/app/src-tauri/src/recorder.rs` | `96e6c17a34aae58928d7f9339b5e5af7205265c856fc8dd077253ae8f9604ad4` |
| `projects/chirality-app-v4/app/src-tauri/src/records.rs` | `cc61f735ab8dfa987081b5f50d37bd0a8b93c340c80cc5bd72266a307c588fea` |
| `projects/chirality-app-v4/app/src-tauri/src/decision_view.rs` | `051dab738e09895d9b81b3e65891aab843681b585922b0572ac959a309f7762c` |
| `projects/chirality-app-v4/app/src-tauri/src/storage.rs` | `ae8439c47b86a3225bf46e893bfa1159a2189d0cc8579692d468a78ea9267d77` |
| `projects/chirality-app-v4/app/src-tauri/src/util.rs` | `3033b37e0f360ccc2f43e4cd1d55d0d7d8305b19479e741693fd5d772f9f6d5c` |
| `projects/chirality-app-v4/app/src-tauri/tests/decide_flow.rs` | `7b0297fc11fdaf008f84264053a3939db95da947b1486039e42ae48087b57cd7` |
| `projects/chirality-app-v4/app/src-tauri/tests/act_storage.rs` | `c5f3fcecbd1331a52e89a6eb07e4f23df99456d22f85ad818ed9888c88f87e84` |
| `projects/chirality-app-v4/app/src/App.tsx` | `9c80295a3eab50970bc9ba5e668cdc36ca0acf347cc6c4c356b964477e8f415a` |

P0-ACT-R1.md SHA-256 `fb8d9eb89dfbf3c2313e548498c07d4f17d348a6c46b5b625239224a4fd99fb3`. V0-CUST source-only READY `111c7098fff7f4e7c46825716fdc7db6bd6dd80bf48efaca3c31f2ff620a5a41`; its required-persistent-replay limitation is preserved. Re-freeze the corrected connected queue/continuation candidate and rerun/backcheck this failure plus affected delay/refusal behavior before product fan-in.
