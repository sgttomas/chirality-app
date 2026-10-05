# V1-ACT — independent frozen product review

2026-10-04. Verdict: **NOT READY for P0-ACT fan-in; blocking findings require owner repair and independent backcheck.** W-1 validation/API propagation itself preserves the gate; no new defect found in the reviewed validation API/schema-copy path. Moving hosting.rs/hosting_contract/handshake repairs are excluded from this verdict. Manager lib/UI/Node bytes are bound below rather than claimed to equal their author's older hashes.

## Scope and independence

Independent TASK `/root/group_a_execution/contract_reviewer`, delegated-harness-native child of WORKING_ITEMS `/root/group_a_execution`; supplied Codex gpt-6.1-sol/medium, no substitution/diversity claim or descendants. Loaded repository software-code-review skill again on explicit commission; prior instruction/source origins are in V0-BASIS and V0-RX/A/P/ID reviews. Reviewer did not implement this lane. Durable write only this file. Read full current act/recorder/records/storage/view/util/validation/lib/UI/Node files and relevant tests/maintained resources; compared removed behavior against source HEAD cb5a88b29ac10fc0c09f9b6a44f497ab917e8a71. Existing actor return hashes matched except the two explicitly manager-owned lib/UI supersessions. API return and all its outputs matched. No downloads, auth, credentials, live/model execution, Design change or Git mutation.

## Blocking findings

### ACT-1 [P1] File-based pending recovery can cause a native human-act record without a native event

Locations: `app/src-tauri/src/act_control.rs:353` and `:391–465`; `app/src-tauri/src/lib.rs:110`.

Trigger: a writer places a schema-valid capture and matching pending sidecar in the writable project capture store, with `inputSource: host-native-confirmation`, an unused recordId and log selector LOG; no native button has been pressed. Refresh/decision_view automatically calls recover_pending. The code checks schema, equal bytes and empty/complete logs, then appends `human_act` through APP_INTERFACE. No check establishes that either input originated from the capture side's native event; `inputSource` text is merely supplied file content.

Impact: this is an active file-drop replay path producing an App direct-capture act, contrary to AAC NA-1/NA-3 and HA-1. It differs from the separately stated residual risk that another same-user process can forge an entire existing unsigned log: here the App itself promotes untrusted files into its own new record. Schema validity and byte agreement are not native-capture provenance.

Repair: make replay require admitted host-native capture custody, with a recoverable distinction from imported project bytes. If native provenance cannot be established under the current unsealed implementation, retain the original files with an explicit unverified-origin limit and refuse automatic new human_act append; do not infer an act from file text or silently adopt SEAL-2/authenticity qualification. A concrete product custody choice must preserve the separately selected native-only control. Add a negative regression for matching fabricated pending/capture files followed by refresh/recovery, with no human_act written. Any changed recovery boundary must be reviewed against CC-A's actual-capture recovery obligation rather than waived.

### ACT-2 [P1] Capture publication and recovery durability do not meet the reviewed atomic persistence contract

Locations: `app/src-tauri/src/storage.rs:80–94`; `app/src-tauri/src/act_control.rs:455–462`; `app/src-tauri/src/records.rs:229–241`.

Trigger: partial capture write or process termination occurs during create_json's direct write into the final pathname; or append's directory sync fails after the log's file sync, followed by recovery finding the entry. create_json does not publish a fully synced temporary file atomically as AAC §5.2a requires. Recovery syncs log files only, not their owning directory metadata, yet treats the previously uncertain record as durable. Newly created parent directory chains also receive only immediate-parent sync.

Impact: incomplete final capture/pending files can become visible; an uncertain log publication can acquire a capture backlink and recorded/durable claim without re-establishing required filesystem publication durability. Existing tests simulate append/backlink state by rewriting files, so their passing result does not exercise these failure points.

Repair: create durable complete evidence in the owning directory, atomically publish without overwriting a pre-existing capture, persist required owning directory metadata (including newly created directory ancestry), and ensure existing-match recovery establishes the same log publication durability before backlink/recorded claims. Preserve complete old capture on backlink failure. Add narrowly injected partial-publication and directory-sync-failure cases; actual process-kill/fsync native witnesses remain separate limits until exercised.

### ACT-3 [P1] Package data and its recorded/bound identity come from separate reads

Locations: `app/src-tauri/src/recorder.rs:107–119`; `app/src-tauri/src/act_control.rs:139–151`.

Trigger: a package changes between file_identity's read and the subsequent read parsed as the package. The recorder can record new fields with the old content identity. Compose can show new alternatives/purpose/scope while binding the old hash; if original bytes are restored before confirm, the final old-hash check passes for text sourced from different bytes.

Impact: source-faithful package mapping and native act binding no longer describe one observed content snapshot. This defeats CI-4's exact confirmed scope/content binding and AK-c despite each schema object validating.

Repair: read bytes once at each observation, calculate hash and parse/validate that exact buffer, and build every body/offer field from it. Confirmation should compare the single confirmation snapshot to that offer identity. Add controlled alternating/replaced snapshot tests showing recorded body/hash and confirmed native text/content always agree. Do not solve by tolerating a hash mismatch.

### ACT-4 [P1] Recovery treats writer-local sequence gaps and duplicate sequence numbers as complete history

Locations: `app/src-tauri/src/records.rs:28–71`; `app/src-tauri/src/storage.rs:153–176`; replay completeness gate `act_control.rs:423`.

Trigger: a discovered log contains individually schema-valid records with unique record IDs but seq [1,3] or [1,1]. read_log validates JSON/schema and read_all detects duplicate recordId, but neither enforces R-5 writer-log continuity. A missing human-act append can therefore be considered definitely absent and replayed, or contradictory history can be treated as complete.

Impact: RS R-5 gaps/duplicates are unreported and AAC §5.2a's complete-history condition for automatic replay is not met. This is not W-0 torn-tail repair, which the author correctly leaves unimplemented.

Repair: detect writer-log gaps/duplicates/out-of-order sequence as completeness limits and hold append/recovery accordingly. Preserve historical bytes. Add sequence-gap/duplicate fixtures and assert no new append/backlink. Do not remove the existing partial/invalid-log checks.

### ACT-5 [P2] Durable acts become AC-8 when only the backlink annotation fails

Location: `app/src-tauri/src/act_control.rs:477–478`; test `tests/act_storage.rs` backlink_failure_stays_pending_then_recovers_without_append; UI captureRecovery filter.

Trigger: valid durable human_act append succeeds, then adding capture.recordId fails. The return says AC-8 record pending although it simultaneously carries recordDurable true. The regression encodes that changed state.

Impact: AAC §5.2a explicitly says verified append stays AC-7 recorded with “act recorded; capture record link pending”. The current UI calls it pending rather than separating the recorded act from the failed annotation, and offer state stays RecordPending.

Repair: retain AC-7 once record durability is established; represent/display backlinkPending and its cause separately and retry only the annotation. Keep AC-8 for genuinely uncertain/unwritten records. Repair the test oracle to the reviewed state rule; this restores, rather than weakens, the criterion.

### ACT-6 [P2] Late writes omit the required delay evidence and original observedAt header

Locations: `app/src-tauri/src/records.rs:212–222`; `app/src-tauri/src/act_control.rs:463–472`.

Trigger: the captured act is pending after a refused/failed append and later successfully written. write_pending appends the human_act only; no subsequent `evidence_limit` “record write failed” is written and no original observedAt is supplied in its completed header. captureTime preserves an act fact but does not implement the W-2 entry delay account.

Impact: RS W-2/AAC AX-14 late-write provenance is missing even though the API claims pending recovery implementation. Tests check unchanged capture facts/ID but not the required ordered delay entry.

Repair: writer-owned pending submission retains original observedAt, reports late-write status, and writes the required referenced failure limit after pending entries in order. Keep the minted ID and original captureTime. Add the actual pending/relaunch fixture's expected late-entry/failure-limit pair without duplicating an already durable act.

### ACT-7 [P2] AAC reserves the record ID before durable capture rather than using writer-owned submission minting

Location: `app/src-tauri/src/act_control.rs:332–335`.

Trigger: confirm obtains rec:app ID itself and persists it in a pending sidecar before publishing capture. AAC §5.2a states record identity minting belongs to DEL-04-03 and “no record identity is reserved or fabricated by AAC at capture.” This implementation moves that responsibility into capture preparation.

Impact: the implementation violates the reviewed capture/writer ownership and ordering protocol. UUID shape and stable retry ID are useful but do not authorize the alternate protocol.

Repair: durably publish actual capture first, then submit it to a writer-owned pending/reservation API which mints and retains the record identity as W-2 state; recover an interruption between publication and submission from admitted original capture custody, not current package data. Keep initial capture.recordId absent until an actual durable entry is verified. If a different protocol is needed, obtain named contract change and review rather than silently changing §5.2a.

## Non-blocking test/evidence finding

**ACT-8 [P2] No-write view hash witness no longer covers the relocated evidence tree.** `tests/decide_flow.rs:hashes` enumerates only project/decisions and records. New logs/captures live under .chirality, so before/after equality would now pass if derive rewrote the actual record/capture set. Add the current owning evidence roots to the recursive census. Current derive implementation is read-only; this is a weakened coverage gap, not a detected write.

## Supported parts and remaining limits

- W-1 validates the completed header/body before append, retains cached setup failures, requires local declared-ID resources and rejects retrieval/fallback. Package/offer/capture APIs reject complete malformed objects. Maintained schema/fixture mapping is explicit; independent `python3 app/src-tauri/schemas/sync.py` exited 0 with six resources matching source bytes/hashes/IDs. No new validation API correctness defect found.
- Current CI-4 mapping preserves package/request scope while applying exactly the absence label to confirmed offer/capture/act; requester identity stays absent with the exact separate limit. Node checks raw declared schemas and five request/limit/request/limit/act entries with negative controls. Fixture counter identities are replaced by governed random/reference invariants rather than silently accepted legacy equality. Source read races remain ACT-3.
- Production IPC exposes compose and a native-dialog decide wrapper, not InputSource or a direct capture command. Full authoritative native text and frozen choice/actor/digest are checked. This protects the normal button path; ACT-1 concerns the separate automatic filesystem replay path.
- Local writer flock is a kernel advisory lock on a held file descriptor; OS process death releases that descriptor lock. It does not prove file durability and has not been independently subjected to an actual process-kill test here. Cross-process/app cooperation and network filesystem limits stay explicit. Existing thread contention tests support only their actual exercised scope.
- UUIDv4 entropy path is fallible and no counter/clock fallback exists; cross-log identity collisions in discovered roots refuse. Existing fixture/host IDs remain opaque. Selected roots, library APIs and legacy in-place discovery are present; actual A15 capture implementation remains outside this bounded A16 lane as author states.
- Manager model/provider input starts blank, requires explicit strings before UI start, and is passed to the owning host API. Generation/standing/network text has distinct information wording. Hosting behavior and its currently moving repair are excluded, so this is not a network/default/provider qualification verdict.
- Current schema/API/library/act tests are author's passing observations in P0-ACT, not independent reviewer reruns. Cargo resource was reserved to hosting repair; no Cargo checks were run by this reviewer. Confirmed findings above follow the actual source/control paths and reviewed obligations; owner should add meaningful negative/fault cases during repair. No actual native human act, process-kill or OS fsync fault injection is claimed.

## Return and repair boundary

Return ACT-1…7 to implementation/design owners for bounded repair; ACT-8 to test owner. Preserve original source history and frozen returns. Re-freeze corrected files and recheck affected coupled writer/control/recovery/UI/tests before fan-in. Report any criterion conflict rather than narrowing checks. No final acceptance/release or broader authenticity qualification is inferred.

## Exact reviewed hashes

| File | SHA-256 |
|---|---|
| `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-GROUP-A-20261004/changes/P0-ACT.md` | `c2df54c60d6e08a0b5d0d143555ae8a19afaaa57ec8c15783d2e31d04ee7714f` |
| `projects/chirality-app-v4/app/src-tauri/src/act_control.rs` | `5a1de69dd988adc23bb3f4aaa06a76ef357062bd72e6fcbc4ad0f64f0661c5c3` |
| `projects/chirality-app-v4/app/src-tauri/src/recorder.rs` | `162c03a488a184ddd3982059fe3c7cad11791cdb92e3f2daaef12ff8a01406c5` |
| `projects/chirality-app-v4/app/src-tauri/src/records.rs` | `72ef071a92533986e1a7221ab2693839cdc5d4796682fd19eb9288b1ca7014ca` |
| `projects/chirality-app-v4/app/src-tauri/src/decision_view.rs` | `636798c6b36e6a3295fb4b55b7c7ee9a11c3dce520b5e9bae241f12d3f41f4f4` |
| `projects/chirality-app-v4/app/src-tauri/src/storage.rs` | `a5314b4acb64a52fd338a293a9e2b973cb213b921ced4597c121d4d9f4064197` |
| `projects/chirality-app-v4/app/src-tauri/src/util.rs` | `50cfa90c75e4cb7b52de76e99313a266290f818b8e8456817b69188e10626b22` |
| `projects/chirality-app-v4/app/src-tauri/Cargo.toml` | `2d89ee516e013d3e8990c15a2eaeebb1ce08588934a26193bfb93b604e4f7d31` |
| `projects/chirality-app-v4/app/src-tauri/Cargo.lock` | `2fad2d658b3ffaf7b3973d5ab7da693788613f7462eaeca9d4b6b9ad826f7012` |
| `projects/chirality-app-v4/app/src-tauri/tests/decide_flow.rs` | `174d4acfb9c2ebcb84600344f2f1855bbd456a0d3fa213bc1682b3509e60e247` |
| `projects/chirality-app-v4/app/src-tauri/tests/act_storage.rs` | `4c8770dd161bd67bd017115a46a4c9ff2860543ba7bf6c86745644583531876b` |
| `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-GROUP-A-20261004/changes/P0-VALIDATION-API.md` | `7073295d74df978773f6031cd176b3d09e61ad0a8e38146d9901c0f0ef41c692` |
| `projects/chirality-app-v4/app/src-tauri/src/schema_validation.rs` | `8877920b116537a7f942a6b20cc1562ff302d7b16572c8b4632dd72d3cf62441` |
| `projects/chirality-app-v4/app/src-tauri/tests/schema_validation.rs` | `1022c3026430fc3d3c14f86adb29e021df99f0b5bc9973578f8d24cac22a6985` |
| `projects/chirality-app-v4/app/src-tauri/schemas/sync.py` | `65640c13b5540a756379bab7f39c01aa303df5521ec0f420ca00f0050ff36200` |
| `projects/chirality-app-v4/app/src-tauri/schemas/manifest.json` | `7c11acfe9f4088b1c4703970341df82ebe2fc23c9938458b8f636af623d2ead5` |
| `projects/chirality-app-v4/app/src-tauri/schemas/aac.offer.schema.json` | `f2091fcf2583b6863370ba51d86f4c8671dbae5bbd6fe0e39046154d98c7d066` |
| `projects/chirality-app-v4/app/src-tauri/schemas/aac.capture-evidence.schema.json` | `4405a1228e5982d948eb82776aaaf54d966d4305f8829a656473a523ad1ca4ba` |
| `projects/chirality-app-v4/app/src-tauri/schemas/fixtures/aac.offer.example.valid.json` | `f80957322793888d13e0c48c2cc312f91ff38b7cf6c60b622a103cb8cf7e967f` |
| `projects/chirality-app-v4/app/src-tauri/schemas/fixtures/aac.capture-evidence.example.valid.json` | `e086bdafb4d24c13f24e8fecee151bd803633294adc51d43ed16fe8523528da4` |
| `projects/chirality-app-v4/app/src-tauri/schemas/fixtures/decision-package-file.example.valid.json` | `3ea08ff575698e769784e0c4788a21c01be81020ad0a3c0534114f5c87895fbe` |
| `projects/chirality-app-v4/app/src-tauri/src/lib.rs` | `f548844056aad1fe30841abb07657a3e14f13e57430091834b1fc48219353461` |
| `projects/chirality-app-v4/app/src/App.tsx` | `5d21e457faad9b4b97805f6570f6e159e7a4c453d216a984269889cfe7265902` |
| `projects/chirality-app-v4/app/tests/validate-records.test.mjs` | `8b0011f2d00b457527fcfea2e37f4c616be57e893abb84282a3128e0bcfd8a07` |

Prior contract review basis: V0-RX, V0-P, V0-ID and separately commissioned V0-A; current AAC §5.2a/§6, RS §14 W-1/W-2/R-5 and owner-selected §13.7 remain governing. This reviewer did not reapprove a substituted contract.
